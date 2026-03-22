#!/usr/bin/env python3
"""
Bootstrap Pipeline: Bible Corpus → Morphological Analyzer
==========================================================

Takes a bilingual Bible corpus (target language + KJV English) and produces
all the building blocks for a morphological analyzer, following the methodology
developed for Tedim Chin (ctd), which achieved 100% coverage after ~10 days
of iterative work.

The "painful" parts of the Tedim process were:
  - Manually looking up every unknown word in KJV to infer its meaning
  - Running coverage tests after each change to see if progress was made
  - Starting from scratch each time for a new language

This script automates those steps so you can go from a raw Bible text to a
working initial analyzer in a single command.

Key outputs (written to analysis/{lang}/):
  1. {lang}.wordfreq.tsv       - Word frequency inventory, sorted by count
  2. {lang}.work_queue.tsv     - Unknown words ranked by frequency, each with
                                  up to 5 English verse contexts  → this is the
                                  core "work queue" that drives manual enrichment
  3. {lang}_analyzer.py        - Initial analyzer pre-populated with:
                                  * Proper nouns from the bootstrap lexicon
                                  * High-frequency content words as stem candidates
  4. {lang}.coverage.txt       - Coverage report showing % tokens analyzed

The workflow mirrors the Tedim Chin methodology:
  Phase 1 (automated): preprocess → inventory → lexicon → analyzer → coverage
  Phase 2 (iterative): open work_queue.tsv, add words to {lang}_analyzer.py,
                        re-run with --steps coverage,queue, repeat

Usage:
    # Full pipeline (recommended first run):
    python scripts/bootstrap_language.py lus

    # Specify which English Bible to align against:
    python scripts/bootstrap_language.py lus --english-iso eng

    # Only regenerate coverage + work queue after enriching the analyzer:
    python scripts/bootstrap_language.py lus --steps coverage,queue

    # Run a specific subset of steps:
    python scripts/bootstrap_language.py lus --steps preprocess,inventory

    # Set minimum frequency threshold for work queue entries:
    python scripts/bootstrap_language.py lus --min-freq 2

Available steps (default: all):
    preprocess  - Normalize Unicode (curly quotes → straight, etc.)
    inventory   - Count word frequencies from the Bible text
    lexicon     - Build PMI-based bilingual bootstrap lexicon
    analyzer    - Generate initial {lang}_analyzer.py from template + lexicon
    coverage    - Measure how many tokens the analyzer currently handles
    queue       - Generate prioritized work queue (unknowns + English contexts)
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
BIBLES_DIR = BASE_DIR / "bibles" / "extracted"
DATA_DIR = BASE_DIR / "data"
ANALYSIS_DIR = BASE_DIR / "analysis"
SCRIPTS_DIR = BASE_DIR / "scripts"

# ---------------------------------------------------------------------------
# Unicode normalization (same rules as preprocess_corpus.py)
# ---------------------------------------------------------------------------

UNICODE_REPLACEMENTS = {
    "\u2019": "'",  # RIGHT SINGLE QUOTATION MARK → apostrophe
    "\u2018": "'",  # LEFT SINGLE QUOTATION MARK  → apostrophe
    "\u201c": '"',  # LEFT DOUBLE QUOTATION MARK
    "\u201d": '"',  # RIGHT DOUBLE QUOTATION MARK
    "\u00a0": " ",  # NO-BREAK SPACE → regular space
    "\u2013": "-",  # EN DASH
    "\u2014": "-",  # EM DASH
    "\ufeff": "",   # BOM
}


def normalize_unicode(text: str) -> str:
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


# ---------------------------------------------------------------------------
# Step 1 – Preprocess
# ---------------------------------------------------------------------------

def step_preprocess(lang_dir: Path, lang: str) -> Path:
    """
    Normalize the Bible text in-place (or create a cleaned copy).

    - Strips leading metadata lines (starting with #)
    - Applies Unicode normalization
    - Validates that every line matches BBCCCVVV<TAB>text format

    Returns the path to the cleaned Bible text file.
    """
    candidates = list(lang_dir.glob(f"{lang}-x-bible*.txt"))
    if not candidates:
        raise FileNotFoundError(
            f"No Bible text found in {lang_dir}. "
            f"Expected a file matching {lang}-x-bible*.txt"
        )
    src = candidates[0]

    raw_backup = src.with_suffix(".raw.txt")
    if not raw_backup.exists():
        raw_backup.write_bytes(src.read_bytes())
        print(f"  Backed up original to {raw_backup.name}")

    lines = raw_backup.read_text(encoding="utf-8").splitlines()

    verse_lines: List[str] = []
    skipped_meta = 0
    skipped_bad = 0
    normalized = 0

    for line in lines:
        if not line.strip():
            continue
        if line.startswith("#"):
            skipped_meta += 1
            continue
        clean = normalize_unicode(line)
        if clean != line:
            normalized += 1
        if not re.match(r"^\d{8}\t.+", clean):
            skipped_bad += 1
            continue
        verse_lines.append(clean)

    src.write_text("\n".join(verse_lines) + "\n", encoding="utf-8")
    print(
        f"  {len(verse_lines)} verses kept, "
        f"{skipped_meta} metadata lines skipped, "
        f"{normalized} lines normalized, "
        f"{skipped_bad} malformed lines skipped"
    )
    return src


# ---------------------------------------------------------------------------
# Step 2 – Inventory
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[^\W\d_]+(?:'[^\W\d_]+)*", re.UNICODE)


def tokenize_verse(text: str) -> List[str]:
    """Extract word tokens from a verse text (Unicode-aware, no digits)."""
    return WORD_RE.findall(text)


def load_verses(bible_path: Path) -> Dict[str, str]:
    """Load verse_id → text from a preprocessed Bible file."""
    verses: Dict[str, str] = {}
    for line in bible_path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t", 1)
        if len(parts) == 2:
            verses[parts[0]] = parts[1]
    return verses


def step_inventory(bible_path: Path, out_dir: Path, lang: str) -> Counter:
    """
    Count all word tokens in the Bible text.

    Writes {lang}.wordfreq.tsv (word<TAB>count, sorted by count desc).
    Returns a Counter mapping word → count.
    """
    verses = load_verses(bible_path)
    freq: Counter = Counter()
    for text in verses.values():
        freq.update(tokenize_verse(text))

    out_path = out_dir / f"{lang}.wordfreq.tsv"
    with out_path.open("w", encoding="utf-8") as f:
        f.write("word\tcount\n")
        for word, count in freq.most_common():
            f.write(f"{word}\t{count}\n")

    total = sum(freq.values())
    print(
        f"  {len(freq):,} unique word types, "
        f"{total:,} total tokens → {out_path.name}"
    )
    return freq


# ---------------------------------------------------------------------------
# Step 3 – Lexicon  (thin wrapper around build_bootstrap_lexicon.py)
# ---------------------------------------------------------------------------

def step_lexicon(lang: str, english_iso: str) -> Path:
    """
    Build (or reuse a cached) bootstrap PMI lexicon for this language.

    Returns the path to the lexicon TSV.
    """
    lexicon_path = DATA_DIR / "lexicons" / f"{lang}_lexicon.tsv"
    if lexicon_path.exists():
        print(f"  Using existing lexicon: {lexicon_path}")
        return lexicon_path

    # Import build function from sibling script
    sys.path.insert(0, str(SCRIPTS_DIR))
    from build_bootstrap_lexicon import build_bootstrap_lexicon  # noqa: PLC0415

    eng_dir = BIBLES_DIR / english_iso
    kc_dir = BIBLES_DIR / lang

    print(f"  Building lexicon ({lang} ↔ {english_iso}) …")
    build_bootstrap_lexicon(eng_dir, kc_dir, lexicon_path)
    print(f"  Wrote {lexicon_path}")
    return lexicon_path


# ---------------------------------------------------------------------------
# Step 4 – Analyzer generation
# ---------------------------------------------------------------------------

# These English glosses typically signal proper nouns (biblical names).
_BIBLICAL_INDICATORS = {
    "aaron", "abraham", "adam", "cain", "david", "elijah", "elisha",
    "esau", "eve", "ezekiel", "ezra", "god", "israel", "jacob", "jesus",
    "john", "jonah", "joseph", "joshua", "judah", "lord", "mary", "moses",
    "noah", "paul", "peter", "pharaoh", "samuel", "saul", "satan",
    "solomon", "stephen",
}

# English glosses that suggest a function-word role.
_FUNCTION_GLOSSES = {
    # Copula / aux
    "be", "have", "do", "will", "shall", "would", "should",
    # Conjunctions / particles
    "and", "but", "or", "if", "then", "when", "where", "because",
    "therefore", "thus", "so", "yet", "also", "even",
    # Prepositions / postpositions
    "in", "on", "at", "to", "from", "with", "by", "of", "for",
    "into", "unto", "upon", "through", "between", "among", "before",
    "after", "until",
    # Pronouns
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "this", "that", "these", "those",
    # TAM / mood
    "not", "no", "never", "already", "now", "again", "still",
    "say", "tell",
}


def _load_lexicon_top1(lexicon_path: Path) -> Dict[str, Tuple[int, str, float]]:
    """
    Load rank-1 entries from the bootstrap lexicon.

    Returns {kc_word: (kc_freq, eng_gloss, confidence)}.
    """
    entries: Dict[str, Tuple[int, str, float]] = {}
    with lexicon_path.open(encoding="utf-8") as f:
        header = f.readline()  # skip header
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 7:
                continue
            kc_word, kc_freq_s, eng_gloss, pmi_s, pair_s, conf_s, rank_s = parts[:7]
            if rank_s.strip() != "1":
                continue
            try:
                kc_freq = int(kc_freq_s)
                confidence = float(conf_s)
            except ValueError:
                continue
            entries[kc_word] = (kc_freq, eng_gloss.lower(), confidence)
    return entries


def _is_proper_noun(word: str, eng_gloss: str) -> bool:
    """Heuristic: does this lexicon entry look like a proper noun?"""
    if word and word[0].isupper():
        return True
    if eng_gloss.lower() in _BIBLICAL_INDICATORS:
        return True
    return False


def _classify_entry(
    word: str, kc_freq: int, eng_gloss: str, confidence: float
) -> Optional[str]:
    """
    Return category: 'proper_noun', 'function_word', 'verb_stem',
    'noun_stem', or None (skip).
    """
    if kc_freq < 2:
        return None
    if _is_proper_noun(word, eng_gloss):
        return "proper_noun"
    wl = word.lower()
    if len(wl) <= 2 and kc_freq > 50:
        return "function_word"
    if eng_gloss in _FUNCTION_GLOSSES:
        return "function_word"
    # Simple English POS heuristic: verbs often end in common verb suffixes
    if any(
        eng_gloss.endswith(s)
        for s in ("e", "fy", "en", "ize", "ise", "ect", "end", "ent")
    ) and kc_freq < 500:
        return "verb_stem"
    return "noun_stem"


def step_generate_analyzer(
    lang: str,
    lang_name: str,
    lexicon_path: Path,
    out_dir: Path,
) -> Path:
    """
    Generate an initial {lang}_analyzer.py by populating the template
    with entries from the bootstrap lexicon.

    Writes to scripts/{lang}_analyzer.py.
    Returns path to generated file.
    """
    entries = _load_lexicon_top1(lexicon_path)

    proper_nouns: Dict[str, str] = {}
    function_words: Dict[str, str] = {}
    verb_stems: Dict[str, str] = {}
    noun_stems: Dict[str, str] = {}

    for word, (kc_freq, eng_gloss, confidence) in sorted(
        entries.items(), key=lambda x: -x[1][0]
    ):
        cat = _classify_entry(word, kc_freq, eng_gloss, confidence)
        if cat is None:
            continue
        if cat == "proper_noun":
            proper_nouns[word] = eng_gloss.upper() if word[0].isupper() else eng_gloss
        elif cat == "function_word":
            function_words[word.lower()] = eng_gloss
        elif cat == "verb_stem":
            verb_stems[word.lower()] = eng_gloss
        else:
            noun_stems[word.lower()] = eng_gloss

    def _dict_lines(d: Dict[str, str], indent: int = 4) -> str:
        pad = " " * indent
        if not d:
            return f"{pad}# (empty – add entries manually)"
        lines = []
        for k, v in sorted(d.items()):
            # escape single quotes inside key/value
            k_esc = k.replace("'", "\\'")
            v_esc = str(v).replace("'", "\\'")
            lines.append(f"{pad}'{k_esc}': '{v_esc}',")
        return "\n".join(lines)

    analyzer_content = f'''\
#!/usr/bin/env python3
"""
{lang_name} ({lang}) Morphological Analyzer
{'=' * (len(lang_name) + len(lang) + 26)}

Auto-generated by bootstrap_language.py from the PMI bootstrap lexicon.
Entries are seed values only – review and refine them as you work through
the work queue (analysis/{lang}/{lang}.work_queue.tsv).

The priority-based lookup order (same as Tedim Chin reference analyzer):
  1. Opaque lexemes     → whole-word lookup, overrides everything
  2. Proper nouns       → case-sensitive lookup
  3. Function words     → closed-class items
  4. Compound words     → pre-analyzed to prevent over-decomposition
  5. Verb stems         → lexical verb roots
  6. Noun stems         → lexical noun roots
  7. Morphological rules→ prefix/suffix stripping on the remainder

Usage:
    python scripts/{lang}_analyzer.py <word>
    python scripts/{lang}_analyzer.py --coverage   # measure corpus coverage
    python scripts/{lang}_analyzer.py --queue      # reprint work queue
"""

import re
import sys
from pathlib import Path

LANGUAGE_ISO = "{lang}"
LANGUAGE_NAME = "{lang_name}"

BASE_DIR = Path(__file__).resolve().parent.parent

# =============================================================================
# DICTIONARIES
# =============================================================================

# Whole-word opaque lexemes (non-compositional; checked before decomposition)
OPAQUE_LEXEMES: dict[str, str] = {{
    # Add entries like: 'lupna': 'bed',
}}

# Proper nouns (biblical names, place names) – case-sensitive lookup
PROPER_NOUNS: dict[str, str] = {{
{_dict_lines(proper_nouns)}
}}

# Function words (closed class: pronouns, particles, conjunctions, TAM markers)
FUNCTION_WORDS: dict[str, str] = {{
{_dict_lines(function_words)}
}}

# Compound words – pre-analyzed to prevent greedy decomposition.
# IMPORTANT: never remove entries here; add disambiguation compounds instead.
COMPOUND_WORDS: dict[str, tuple[str, str]] = {{
    # Format: 'compound': ('seg-men-ta-tion', 'gloss-by-morpheme'),
    # e.g.  'biakinn': ('biak-inn', 'worship-house'),
}}

# Verb stems (add both Stem I and Stem II forms if the language alternates)
VERB_STEMS: dict[str, str] = {{
{_dict_lines(verb_stems)}
}}

# Noun stems
NOUN_STEMS: dict[str, str] = {{
{_dict_lines(noun_stems)}
}}

# =============================================================================
# AFFIXES  –  edit to match the target language\'s morphology
# =============================================================================

# Prefixes: [(form, gloss), ...] – sorted longest-first to prevent greedy matches
PREFIXES: list[tuple[str, str]] = [
    # e.g. ('ka', '1SG'), ('na', '2SG'), ('ki', 'REFL'),
]

# Derivational suffixes (applied before inflectional)
DERIV_SUFFIXES: list[tuple[str, str]] = [
    # e.g. ('sak', 'CAUS'), ('pih', 'APPL'),
]

# Inflectional suffixes (applied after derivational)
INFL_SUFFIXES: list[tuple[str, str]] = [
    # e.g. ('te', 'PL'), ('in', 'ERG'), ('ah', 'LOC'),
]

# =============================================================================
# ANALYSIS
# =============================================================================

_WORD_RE = re.compile(r"[^\\W\\d_]+(?:\'[^\\W\\d_]+)*", re.UNICODE)


def _normalize(word: str) -> str:
    for old, new in (("\\u2019", "\'"), ("\\u2018", "\'")):
        word = word.replace(old, new)
    return word


def analyze_word(word: str) -> tuple[str, str]:
    """
    Return (segmentation, gloss) for a single word token.
    Unknown words get gloss \'UNK\'.
    """
    word = _normalize(word)
    wl = word.lower()

    # 1. Opaque lexemes
    if wl in OPAQUE_LEXEMES:
        return wl, OPAQUE_LEXEMES[wl]

    # 2. Proper nouns (case-sensitive)
    if word in PROPER_NOUNS:
        return word, PROPER_NOUNS[word]

    # 3. Function words
    if wl in FUNCTION_WORDS:
        return wl, FUNCTION_WORDS[wl]

    # 4. Compound words
    if wl in COMPOUND_WORDS:
        return COMPOUND_WORDS[wl]

    # 5. Verb stems
    if wl in VERB_STEMS:
        return wl, VERB_STEMS[wl]

    # 6. Noun stems
    if wl in NOUN_STEMS:
        return wl, NOUN_STEMS[wl]

    # 7. Prefix stripping (longest first)
    for prefix, pg in sorted(PREFIXES, key=lambda x: -len(x[0])):
        if wl.startswith(prefix) and len(wl) > len(prefix):
            remainder = wl[len(prefix):]
            if remainder in VERB_STEMS:
                return f"{{prefix}}-{{remainder}}", f"{{pg}}-{{VERB_STEMS[remainder]}}"
            if remainder in NOUN_STEMS:
                return f"{{prefix}}-{{remainder}}", f"{{pg}}-{{NOUN_STEMS[remainder]}}"

    # 8. Suffix stripping (inflectional then derivational)
    all_suffixes = INFL_SUFFIXES + DERIV_SUFFIXES
    for suffix, sg in sorted(all_suffixes, key=lambda x: -len(x[0])):
        if wl.endswith(suffix) and len(wl) > len(suffix):
            stem = wl[: -len(suffix)]
            if stem in VERB_STEMS:
                return f"{{stem}}-{{suffix}}", f"{{VERB_STEMS[stem]}}-{{sg}}"
            if stem in NOUN_STEMS:
                return f"{{stem}}-{{suffix}}", f"{{NOUN_STEMS[stem]}}-{{sg}}"

    # 9. Simple reduplication (X~X)
    if len(wl) >= 4 and len(wl) % 2 == 0:
        half = len(wl) // 2
        if wl[:half] == wl[half:]:
            base = wl[:half]
            for d in (VERB_STEMS, NOUN_STEMS):
                if base in d:
                    return f"{{base}}~RED", f"{{d[base]}}~INTNS"

    # 10. Possessive apostrophe
    if word.endswith("\'"):
        stem = word[:-1].lower()
        for d in (NOUN_STEMS, VERB_STEMS):
            if stem in d:
                return f"{{stem}}\'", f"{{d[stem]}}.POSS"
        if word[:-1] in PROPER_NOUNS:
            return f"{{word[:-1]}}\'", f"{{PROPER_NOUNS[word[:-1]]}}.POSS"

    return word, "UNK"


def analyze_text(text: str) -> list[tuple[str, str, str]]:
    """Return [(word, segmentation, gloss), ...] for all tokens in text."""
    return [(w, *analyze_word(w)) for w in _WORD_RE.findall(text)]


def get_coverage(
    corpus_file: Path | None = None,
) -> dict[str, int | float]:
    """Compute coverage on the {lang} Bible corpus."""
    if corpus_file is None:
        corpus_file = (
            BASE_DIR / "bibles" / "extracted" / LANGUAGE_ISO
            / f"{{LANGUAGE_ISO}}-x-bible.txt"
        )
    total = 0
    unknown = 0
    unk_counter: dict[str, int] = {{}}
    with corpus_file.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("\\t", 1)
            if len(parts) < 2:
                continue
            for word in _WORD_RE.findall(parts[1]):
                total += 1
                _, gloss = analyze_word(word)
                if gloss == "UNK":
                    unknown += 1
                    unk_counter[word] = unk_counter.get(word, 0) + 1
    coverage = (total - unknown) / total * 100 if total else 0.0
    return {{
        "total": total,
        "analyzed": total - unknown,
        "unknown": unknown,
        "coverage": coverage,
        "top_unknowns": sorted(unk_counter.items(), key=lambda x: -x[1])[:20],
    }}


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{{LANGUAGE_NAME}} ({{LANGUAGE_ISO}}) Morphological Analyzer")
        print(f"Proper nouns : {{len(PROPER_NOUNS):,}}")
        print(f"Function words: {{len(FUNCTION_WORDS):,}}")
        print(f"Verb stems   : {{len(VERB_STEMS):,}}")
        print(f"Noun stems   : {{len(NOUN_STEMS):,}}")
        print(f"Compounds    : {{len(COMPOUND_WORDS):,}}")
        print(f"\\nUsage: python {{sys.argv[0]}} <word>")
        print(f"       python {{sys.argv[0]}} --coverage")
        sys.exit(0)

    if sys.argv[1] == "--coverage":
        stats = get_coverage()
        print(f"Coverage: {{stats[\'coverage\']:.2f}}%  "
              f"({{stats[\'analyzed\']:,}} / {{stats[\'total\']:,}} tokens)")
        print("\\nTop unknowns:")
        for word, cnt in stats["top_unknowns"]:
            print(f"  {{word:<25}} {{cnt:>6,}}x")
    else:
        word = sys.argv[1]
        seg, gloss = analyze_word(word)
        print(f"{{word}}  →  {{seg}}  =  {{gloss}}")
'''

    out_path = SCRIPTS_DIR / f"{lang}_analyzer.py"
    out_path.write_text(analyzer_content, encoding="utf-8")
    print(
        f"  Generated {out_path.name}  "
        f"({len(proper_nouns):,} proper nouns, "
        f"{len(function_words):,} function words, "
        f"{len(verb_stems):,} verb stems, "
        f"{len(noun_stems):,} noun stems)"
    )
    return out_path


# ---------------------------------------------------------------------------
# Step 5 – Coverage
# ---------------------------------------------------------------------------

def step_coverage(
    lang: str,
    bible_path: Path,
    analyzer_path: Path,
    out_dir: Path,
) -> Tuple[float, Counter]:
    """
    Import the generated analyzer and measure token coverage.

    Returns (coverage_percent, unknown_counter).
    """
    sys.path.insert(0, str(SCRIPTS_DIR))

    # Force fresh import even if module was previously cached
    mod_name = analyzer_path.stem
    if mod_name in sys.modules:
        del sys.modules[mod_name]

    import importlib.util  # noqa: PLC0415

    spec = importlib.util.spec_from_file_location(mod_name, analyzer_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    verses = load_verses(bible_path)
    total = 0
    unknown_counter: Counter = Counter()

    for text in verses.values():
        for word in tokenize_verse(text):
            total += 1
            _, gloss = mod.analyze_word(word)
            if gloss == "UNK":
                unknown_counter[word] += 1

    analyzed = total - sum(unknown_counter.values())
    coverage = analyzed / total * 100 if total else 0.0

    out_path = out_dir / f"{lang}.coverage.txt"
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"Coverage report for {lang}\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total tokens : {total:,}\n")
        f.write(f"Analyzed     : {analyzed:,}\n")
        f.write(f"Unknown      : {sum(unknown_counter.values()):,}\n")
        f.write(f"Coverage     : {coverage:.2f}%\n\n")
        f.write("Top 50 unknown word types (by token frequency):\n")
        f.write("-" * 40 + "\n")
        for word, cnt in unknown_counter.most_common(50):
            f.write(f"  {word:<30} {cnt:>6,}\n")

    print(
        f"  Coverage: {coverage:.2f}%  "
        f"({analyzed:,} / {total:,} tokens, "
        f"{len(unknown_counter):,} unknown types)"
    )
    return coverage, unknown_counter


# ---------------------------------------------------------------------------
# Step 6 – Work queue
# ---------------------------------------------------------------------------

def step_work_queue(
    lang: str,
    bible_path: Path,
    eng_bible_path: Path,
    unknown_counter: Counter,
    out_dir: Path,
    min_freq: int = 2,
    max_contexts: int = 5,
) -> Path:
    """
    Generate a prioritized work queue: for every unknown word (freq >= min_freq),
    show up to max_contexts aligned English verse contexts.

    This is the core tool for manual lexicon enrichment: open the TSV,
    read the English context, decide the meaning, add the word to the
    {lang}_analyzer.py, then re-run --steps coverage,queue.

    Output columns:
        rank        – priority rank (most frequent first)
        word        – unknown word form
        freq_tokens – how many tokens in corpus
        freq_verses – how many distinct verses it appears in
        eng_context – pipe-separated English verse texts (up to max_contexts)
        kc_context  – corresponding target-language verse texts
    """
    # Index: word → [verse_id, ...]
    print(f"  Indexing verses for {len(unknown_counter)} unknown types …")
    verses = load_verses(bible_path)
    word_verse_index: Dict[str, List[str]] = defaultdict(list)
    for verse_id, text in verses.items():
        for word in tokenize_verse(text):
            if word in unknown_counter:
                word_verse_index[word].append(verse_id)

    # Load English for context
    eng_verses: Dict[str, str] = {}
    if eng_bible_path.exists():
        eng_verses = load_verses(eng_bible_path)
    else:
        print(f"  Warning: English Bible not found at {eng_bible_path}")

    out_path = out_dir / f"{lang}.work_queue.tsv"
    candidates = [
        (word, cnt)
        for word, cnt in unknown_counter.most_common()
        if cnt >= min_freq
    ]

    with out_path.open("w", encoding="utf-8") as f:
        f.write(
            "rank\tword\tfreq_tokens\tfreq_verses\teng_context\tkc_context\n"
        )
        for rank, (word, token_freq) in enumerate(candidates, 1):
            verse_ids = word_verse_index.get(word, [])
            # Deduplicate but preserve order
            seen: set = set()
            unique_verse_ids: List[str] = []
            for vid in verse_ids:
                if vid not in seen:
                    seen.add(vid)
                    unique_verse_ids.append(vid)

            sample_ids = unique_verse_ids[:max_contexts]
            eng_ctx = " | ".join(
                eng_verses.get(vid, "").replace("\t", " ")
                for vid in sample_ids
            )
            kc_ctx = " | ".join(
                verses.get(vid, "").replace("\t", " ")
                for vid in sample_ids
            )
            f.write(
                f"{rank}\t{word}\t{token_freq}\t{len(unique_verse_ids)}"
                f"\t{eng_ctx}\t{kc_ctx}\n"
            )

    singleton_count = sum(1 for _, cnt in unknown_counter.items() if cnt < min_freq)
    print(
        f"  Work queue: {len(candidates):,} entries "
        f"(freq ≥ {min_freq}), "
        f"{singleton_count:,} singletons omitted → {out_path.name}"
    )
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _find_eng_bible(english_iso: str) -> Path:
    eng_dir = BIBLES_DIR / english_iso
    # Prefer clean (preprocessed) files; exclude .raw.txt backups
    candidates = sorted(
        p for p in eng_dir.glob(f"{english_iso}-x-bible*.txt")
        if ".raw." not in p.name
    )
    if not candidates:
        candidates = sorted(eng_dir.glob(f"{english_iso}-x-bible*.txt"))
    if not candidates:
        raise FileNotFoundError(
            f"English Bible not found in {eng_dir}. "
            f"Expected a file matching {english_iso}-x-bible*.txt"
        )
    return candidates[0]


def _get_lang_name(lang: str) -> str:
    """Try to read the language name from metadata or datapackage.json."""
    for meta_file in (
        BIBLES_DIR / lang / "datapackage.json",
        BIBLES_DIR / lang / "metadata.json",
    ):
        if meta_file.exists():
            import json  # noqa: PLC0415

            data = json.loads(meta_file.read_text(encoding="utf-8"))
            for key in ("language_name", "name", "title"):
                if key in data:
                    return data[key]
    # Fall back to scanning metadata comments in the Bible text file
    candidates = list((BIBLES_DIR / lang).glob(f"{lang}-x-bible*.txt"))
    if candidates:
        for line in candidates[0].read_text(encoding="utf-8").splitlines()[:10]:
            if line.startswith("# language_name:"):
                return line.split(":", 1)[1].strip()
    return lang.upper()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Bootstrap a morphological analyzer from a bilingual Bible corpus.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "lang",
        help="ISO 639-3 code for the target language (e.g. lus, tcz, pck)",
    )
    parser.add_argument(
        "--english-iso",
        default="eng",
        metavar="ISO",
        help="ISO code for the English reference Bible (default: eng)",
    )
    parser.add_argument(
        "--steps",
        default="preprocess,inventory,lexicon,analyzer,coverage,queue",
        metavar="STEP[,STEP…]",
        help=(
            "Comma-separated list of steps to run. "
            "Available: preprocess, inventory, lexicon, analyzer, coverage, queue. "
            "Default: all steps."
        ),
    )
    parser.add_argument(
        "--min-freq",
        type=int,
        default=2,
        metavar="N",
        help="Minimum token frequency to include in work queue (default: 2)",
    )
    parser.add_argument(
        "--max-contexts",
        type=int,
        default=5,
        metavar="N",
        help="Max English verse contexts per unknown word in work queue (default: 5)",
    )
    args = parser.parse_args()

    steps = {s.strip() for s in args.steps.split(",")}
    lang = args.lang
    english_iso = args.english_iso

    lang_dir = BIBLES_DIR / lang
    if not lang_dir.is_dir():
        print(f"Error: {lang_dir} not found.", file=sys.stderr)
        print(
            f"Available languages: "
            + ", ".join(d.name for d in sorted(BIBLES_DIR.iterdir()) if d.is_dir()),
            file=sys.stderr,
        )
        sys.exit(1)

    out_dir = ANALYSIS_DIR / lang
    out_dir.mkdir(parents=True, exist_ok=True)

    lang_name = _get_lang_name(lang)
    print(f"\n{'='*60}")
    print(f"Bootstrap pipeline: {lang_name} ({lang})")
    print(f"{'='*60}\n")

    # ------------------------------------------------------------------ #
    print("── Step 1: Preprocess ─────────────────────────────────────")
    if "preprocess" in steps:
        bible_path = step_preprocess(lang_dir, lang)
    else:
        # Prefer the clean (preprocessed) file; exclude .raw.txt backups
        candidates = sorted(
            p for p in lang_dir.glob(f"{lang}-x-bible*.txt")
            if ".raw." not in p.name
        )
        if not candidates:
            # Fall back to raw backup if no clean file exists
            candidates = sorted(lang_dir.glob(f"{lang}-x-bible*.txt"))
        if not candidates:
            print(f"  ERROR: no Bible text found in {lang_dir}")
            sys.exit(1)
        bible_path = candidates[0]
        print(f"  (skipped) using {bible_path.name}")

    # ------------------------------------------------------------------ #
    print("\n── Step 2: Inventory ──────────────────────────────────────")
    if "inventory" in steps:
        freq = step_inventory(bible_path, out_dir, lang)
    else:
        freq_path = out_dir / f"{lang}.wordfreq.tsv"
        if freq_path.exists():
            freq = Counter()
            for line in freq_path.read_text(encoding="utf-8").splitlines()[1:]:
                parts = line.split("\t")
                if len(parts) == 2:
                    freq[parts[0]] = int(parts[1])
            print(f"  (skipped) loaded {len(freq):,} entries from {freq_path.name}")
        else:
            print("  (skipped) – no cached inventory found; building anyway")
            freq = step_inventory(bible_path, out_dir, lang)

    # ------------------------------------------------------------------ #
    print("\n── Step 3: Lexicon ────────────────────────────────────────")
    if "lexicon" in steps:
        lexicon_path = step_lexicon(lang, english_iso)
    else:
        lexicon_path = DATA_DIR / "lexicons" / f"{lang}_lexicon.tsv"
        if lexicon_path.exists():
            print(f"  (skipped) using {lexicon_path}")
        else:
            print("  (skipped) – no lexicon found; building anyway")
            lexicon_path = step_lexicon(lang, english_iso)

    # ------------------------------------------------------------------ #
    print("\n── Step 4: Analyzer ───────────────────────────────────────")
    analyzer_path = SCRIPTS_DIR / f"{lang}_analyzer.py"
    if "analyzer" in steps:
        analyzer_path = step_generate_analyzer(lang, lang_name, lexicon_path, out_dir)
    else:
        if analyzer_path.exists():
            print(f"  (skipped) using existing {analyzer_path.name}")
        else:
            print("  (skipped) – no analyzer found; generating anyway")
            analyzer_path = step_generate_analyzer(
                lang, lang_name, lexicon_path, out_dir
            )

    # ------------------------------------------------------------------ #
    print("\n── Step 5: Coverage ───────────────────────────────────────")
    unknown_counter: Counter = Counter()
    if "coverage" in steps:
        _, unknown_counter = step_coverage(lang, bible_path, analyzer_path, out_dir)
    else:
        print("  (skipped)")

    # ------------------------------------------------------------------ #
    print("\n── Step 6: Work queue ─────────────────────────────────────")
    if "queue" in steps:
        if not unknown_counter:
            # Need to compute unknowns even if coverage step was skipped
            print("  (computing unknowns first …)")
            _, unknown_counter = step_coverage(lang, bible_path, analyzer_path, out_dir)
        eng_bible_path = _find_eng_bible(english_iso)
        step_work_queue(
            lang,
            bible_path,
            eng_bible_path,
            unknown_counter,
            out_dir,
            min_freq=args.min_freq,
            max_contexts=args.max_contexts,
        )
    else:
        print("  (skipped)")

    # ------------------------------------------------------------------ #
    print(f"\n{'='*60}")
    print(f"Pipeline complete.  Outputs in: {out_dir}/")
    print(f"  {lang}.wordfreq.tsv       – word frequency inventory")
    print(f"  {lang}.coverage.txt       – coverage report")
    print(f"  {lang}.work_queue.tsv     – unknowns + English contexts")
    print(f"  (scripts/{lang}_analyzer.py)  – initial analyzer to enrich")
    print()
    print("Next steps:")
    print(f"  1. Open analysis/{lang}/{lang}.work_queue.tsv")
    print(f"  2. For each high-frequency unknown word, infer its meaning")
    print(f"     from the English verse context column")
    print(f"  3. Add the word to scripts/{lang}_analyzer.py")
    print(f"     (FUNCTION_WORDS, NOUN_STEMS, VERB_STEMS, or PROPER_NOUNS)")
    print(f"  4. Re-run:  python scripts/bootstrap_language.py {lang}")
    print(f"              --steps coverage,queue")
    print(f"  5. Repeat until coverage exceeds your target (aim for ≥ 95%)")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
