#!/usr/bin/env python3
"""
Bootstrap Morphological Analyzer for Kuki-Chin Languages

This script automates the initial scaffolding of a morphological analyzer for
any Kuki-Chin language that has:
  1. A Bible corpus in bibles/extracted/{ISO}/{ISO}-x-bible.txt
  2. A PMI lexicon in data/lexicons/{ISO}_lexicon.tsv
  3. The KJV English Bible in bibles/extracted/eng/eng-x-bible.txt

It generates:
  - scripts/analyze_morphemes_{ISO}.py  -- ready-to-run scaffold analyzer
  - analysis/{ISO}_bootstrap_report.md  -- summary + iterative work plan

The scaffold starts with ~50-65% coverage (proper nouns + function word
candidates + common stems) and is designed for rapid iterative improvement
using the philological cross-reference method (look up unknowns in KJV).

Usage:
    python scripts/bootstrap_analyzer.py <ISO>
    python scripts/bootstrap_analyzer.py lus          # Mizo
    python scripts/bootstrap_analyzer.py cfm          # Falam Chin
    python scripts/bootstrap_analyzer.py --dry-run lus  # report only, no files written

The "painful" path for Tedim Chin (ctd) took 15+ iterative sessions because
we started from scratch.  This script compresses Phase 1 (bootstrap) to a
single command, so you can start iterating immediately from a ~60% baseline.

Pipeline overview
-----------------
1. Preprocess corpus (Unicode normalization, verse extraction)
2. Build word-frequency distribution
3. Load PMI lexicon → candidate glosses for every word
4. Detect proper nouns (capitalized words with low lowercase ratio)
5. Seed FUNCTION_WORDS from top-N most-frequent words
6. Classify remaining words as VERB_STEMS / NOUN_STEMS via PMI
7. Write scaffold analyze_morphemes_{ISO}.py
8. Write analysis/{ISO}_bootstrap_report.md
"""

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
BIBLES_DIR = REPO_ROOT / "bibles" / "extracted"
LEXICONS_DIR = REPO_ROOT / "data" / "lexicons"
ANALYSIS_DIR = REPO_ROOT / "analysis"
SCRIPTS_DIR = REPO_ROOT / "scripts"

# ---------------------------------------------------------------------------
# Unicode normalisation (mirrors preprocess_corpus.py)
# ---------------------------------------------------------------------------
UNICODE_REPLACEMENTS = {
    "\u2019": "'",   # RIGHT SINGLE QUOTATION MARK
    "\u2018": "'",   # LEFT SINGLE QUOTATION MARK
    "\u201c": '"',   # LEFT DOUBLE QUOTATION MARK
    "\u201d": '"',   # RIGHT DOUBLE QUOTATION MARK
    "\u00a0": " ",   # NON-BREAKING SPACE
    "\u2013": "-",   # EN DASH
    "\u2014": "-",   # EM DASH
    "\ufeff": "",    # BOM
}


def normalize_unicode(text: str) -> str:
    for old, new in UNICODE_REPLACEMENTS.items():
        text = text.replace(old, new)
    return text


# ---------------------------------------------------------------------------
# Biblical name set – used to cross-check PMI glosses
# ---------------------------------------------------------------------------
# These are the most common biblical proper names found in the KJV.
# If a target-language word's top PMI gloss is in this set, it is almost
# certainly a proper noun (a phonological adaptation of the biblical name).
BIBLICAL_NAMES = frozenset({
    # Persons – OT
    "aaron", "abdon", "abednego", "abel", "abiathar", "abiezer", "abigail",
    "abihail", "abihu", "abijah", "abimelech", "abinadab", "abinoam",
    "abiram", "abishai", "abner", "abraham", "absalom", "achan", "achish",
    "adah", "adam", "adonijah", "agag", "ahab", "ahaz", "ahijah", "ahimaaz",
    "ahimelech", "ahithophel", "amaziah", "ammon", "amnon", "amos", "ananias",
    "araunah", "asaph", "asher", "athaliah", "baal", "baasha", "balaam",
    "balak", "barak", "barnabas", "barabbas", "bartholomew", "baruch",
    "bathsheba", "belshazzar", "benjamin", "bezalel", "bilhah",
    "boaz", "cain", "caleb", "canaan", "cornelius", "cyrus",
    "dan", "daniel", "dathan", "david", "deborah", "delilah",
    "dinah", "eli", "elijah", "elisha", "eliab", "eliezer", "elizur",
    "enoch", "esau", "esther", "eve", "ezekiel", "ezra",
    "gad", "gedeon", "gideon", "goliath", "habakkuk", "hagar",
    "ham", "haman", "hannah", "hazael", "hezekiah", "hiram",
    "hosea", "hur", "ishmael", "issachar", "jabez", "jacob", "jairus",
    "japheth", "jeremiah", "jeroboam", "jesse", "jethro", "joab",
    "joash", "job", "joel", "john", "jonah", "jonathan", "joseph",
    "joshua", "josiah", "judah", "korah", "laban", "lazarus", "leah",
    "levi", "lot", "malachi", "manasseh", "meshach", "micah", "michal",
    "miriam", "mordecai", "moses", "naaman", "nabal", "naboth", "nadab",
    "naomi", "naphtali", "nathan", "nebuchadnezzar", "nehemiah", "noah",
    "obadiah", "omri", "paul", "peter", "pharaoh", "phinehas", "potiphar",
    "rachel", "rebekah", "rehoboam", "reuben", "ruth", "samson", "samuel",
    "saul", "seth", "shadrach", "shem", "shimei", "simeon", "sisera",
    "solomon", "stephen", "tamar", "timothy", "titus", "uzziah",
    "zechariah", "zedekiah", "zelophehad", "zephaniah", "zerubbabel",
    "zilpah", "zimri", "zion",
    # NT persons
    "andrew", "barnabas", "bartholomew", "cleopas", "herod", "james",
    "jesus", "joseph", "judas", "luke", "mark", "mary", "matthew",
    "nathaniel", "nicodemus", "philip", "pilate", "priscilla", "silas",
    "stephen", "thomas", "zacchaeus", "zacharias",
    # Places – OT/NT (common)
    "arabia", "aram", "assyria", "babylon", "bethel", "bethlehem",
    "canaan", "carmel", "damascus", "edom", "egypt", "euphrates",
    "galilee", "gath", "gaza", "gilead", "hebron", "horeb", "jerusalem",
    "jordan", "judah", "moab", "moriah", "nazareth", "nineveh", "philistia",
    "samaria", "sinai", "zion",
    # Variant / shortened forms common in Bible
    "nego", "shadrach", "meshach", "abram", "sarai", "jehovah",
    "israelite", "israel", "israelites",
})


# ---------------------------------------------------------------------------
# Helper: tokenize a verse line
# ---------------------------------------------------------------------------
def tokenize(text: str) -> list[str]:
    """Split text into word tokens, stripping leading/trailing punctuation."""
    tokens = []
    for tok in text.split():
        # Strip outer punctuation but keep internal apostrophes
        tok = re.sub(r"^[^\w']+", "", tok)
        tok = re.sub(r"[^\w']+$", "", tok)
        if tok and re.search(r"[a-zA-Z\u00C0-\u024F\u1E00-\u1EFF]", tok):
            tokens.append(tok)
    return tokens


# ---------------------------------------------------------------------------
# Step 1 – load & preprocess Bible corpus
# ---------------------------------------------------------------------------
def load_corpus(iso: str) -> tuple[list[tuple[str, str]], Counter]:
    """
    Load a Bible corpus from bibles/extracted/{iso}/{iso}-x-bible*.txt.

    Returns
    -------
    verses : list of (verse_id, text) tuples
    freq   : Counter mapping wordform → total count
    """
    iso_dir = BIBLES_DIR / iso
    candidates = sorted(iso_dir.glob(f"{iso}-x-bible*.txt"))
    if not candidates:
        raise FileNotFoundError(
            f"No Bible file found at {iso_dir}/{iso}-x-bible*.txt"
        )
    bible_path = candidates[0]
    print(f"  Bible: {bible_path.name}")

    verses = []
    freq: Counter = Counter()

    with open(bible_path, encoding="utf-8") as fh:
        for line in fh:
            line = normalize_unicode(line.rstrip("\n"))
            if line.startswith("#") or not line.strip():
                continue
            if "\t" not in line:
                continue
            verse_id, text = line.split("\t", 1)
            text = text.strip()
            verses.append((verse_id, text))
            freq.update(tokenize(text))

    print(f"  Verses: {len(verses):,}  Tokens: {sum(freq.values()):,}  Types: {len(freq):,}")
    return verses, freq


# ---------------------------------------------------------------------------
# Step 2 – load PMI lexicon
# ---------------------------------------------------------------------------
def load_lexicon(iso: str) -> dict[str, list[tuple[str, float]]]:
    """
    Load data/lexicons/{iso}_lexicon.tsv.

    Returns
    -------
    lex : dict mapping kc_word → [(eng_gloss, confidence), ...] (rank-ordered)
    """
    lex_path = LEXICONS_DIR / f"{iso}_lexicon.tsv"
    if not lex_path.exists():
        print(f"  ⚠ Lexicon not found: {lex_path}")
        print("    Run: python scripts/build_bootstrap_lexicon.py")
        return {}

    lex: dict[str, list[tuple[str, float]]] = defaultdict(list)
    with open(lex_path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("kc_word") or not line.strip():
                continue
            parts = line.strip().split("\t")
            if len(parts) < 7:
                continue
            word, _, gloss, _, _, confidence, _ = parts[:7]
            try:
                conf = float(confidence)
            except ValueError:
                conf = 0.0
            lex[word].append((gloss.lower(), conf))

    print(f"  Lexicon: {len(lex):,} entries")
    return dict(lex)


# ---------------------------------------------------------------------------
# Step 3 – load KJV for context lookup utility (verse text only)
# ---------------------------------------------------------------------------
def load_kjv() -> dict[str, str]:
    """Load KJV Bible as {verse_id: text}."""
    kjv_dir = BIBLES_DIR / "eng"
    candidates = sorted(kjv_dir.glob("eng-x-bible*.txt"))
    if not candidates:
        print("  ⚠ KJV Bible not found – cross-reference lookup unavailable")
        return {}
    kjv: dict[str, str] = {}
    with open(candidates[0], encoding="utf-8") as fh:
        for line in fh:
            line = normalize_unicode(line.rstrip("\n"))
            if line.startswith("#") or "\t" not in line:
                continue
            vid, text = line.split("\t", 1)
            kjv[vid] = text.strip()
    print(f"  KJV: {len(kjv):,} verses loaded")
    return kjv


# ---------------------------------------------------------------------------
# Step 4 – word classification
# ---------------------------------------------------------------------------

def _pmi_gloss(word: str, lex: dict) -> str | None:
    """Return the highest-confidence PMI gloss for a word (or its lowercase)."""
    for key in (word, word.lower(), word.title()):
        entries = lex.get(key)
        if entries:
            return entries[0][0]
    return None


def _is_biblical_name_gloss(gloss: str | None) -> bool:
    """Return True if the gloss string looks like a biblical proper name."""
    if not gloss:
        return False
    return gloss.lower() in BIBLICAL_NAMES


def classify_words(
    freq: Counter,
    lex: dict,
    function_word_top_n: int = 150,
) -> dict:
    """
    Classify corpus wordforms into four buckets:

    proper_nouns    – capitalized, rarely/never lowercase
    function_words  – top-N most-frequent words (any POS; highest leverage)
    verb_stems      – medium-frequency content words with verbal PMI glosses
    noun_stems      – medium-frequency content words with nominal PMI glosses
    unknowns        – everything else, sorted by frequency (iterative work list)

    Parameters
    ----------
    freq   : Counter of all wordforms
    lex    : PMI lexicon dict
    function_word_top_n : how many top-frequency words to treat as function
             word candidates (default 150, matching Tedim experience)

    Returns
    -------
    dict with keys: proper_nouns, function_words, verb_stems, noun_stems, unknowns
    """

    # Build case-pair map: lowercase → set of all seen capitalizations
    lower_to_forms: dict[str, Counter] = defaultdict(Counter)
    for word, cnt in freq.items():
        lower_to_forms[word.lower()][word] += cnt

    # Top-N frequency words (case-folded to unique lowercase keys, keep highest form)
    # We track which surface form is most common for display purposes.
    freq_lower: Counter = Counter()
    form_for_lower: dict[str, str] = {}
    for word, cnt in freq.items():
        wl = word.lower()
        freq_lower[wl] += cnt
        if wl not in form_for_lower or cnt > freq.get(form_for_lower[wl], 0):
            form_for_lower[wl] = word

    top_n_lower = {w for w, _ in freq_lower.most_common(function_word_top_n)}

    # --- Proper noun detection -------------------------------------------
    # A word is likely a proper noun when:
    #   (a) it appears significantly more often capitalized than lowercase, AND
    #   (b) its lowercase form is NOT a top-N function word candidate, AND
    #   (c) either the capitalised form is the dominant form OR its top PMI
    #       gloss is a known biblical name.
    proper_nouns: dict[str, str] = {}

    for wl, forms in lower_to_forms.items():
        total = sum(forms.values())
        if total < 2:
            continue  # Too rare to classify reliably

        cap_forms = {f: c for f, c in forms.items() if f[0].isupper()}
        cap_total = sum(cap_forms.values())
        cap_ratio = cap_total / total

        if cap_ratio < 0.85:
            continue  # Appears too often lowercase to be a proper noun
        if wl in top_n_lower:
            continue  # High-frequency → function word candidate, not proper noun

        # Pick the most-common capitalised surface form
        surface = max(cap_forms, key=cap_forms.get)

        # Get PMI gloss for the capitalised form
        pmi = _pmi_gloss(surface, lex) or _pmi_gloss(wl, lex)

        if _is_biblical_name_gloss(pmi):
            gloss = f"PN.{pmi.upper()}"  # biblical name
        elif pmi and pmi.istitle():
            gloss = f"PN.{pmi.upper()}"  # capitalised PMI gloss
        else:
            # Unknown proper noun – use the surface form as a gloss placeholder
            gloss = f"PN"

        proper_nouns[surface] = gloss

    # --- Function words (top-N, excluding already classified proper nouns) -
    function_words: dict[str, str] = {}
    for wl in top_n_lower:
        surface = form_for_lower.get(wl, wl)
        if surface in proper_nouns or wl in {p.lower() for p in proper_nouns}:
            continue  # Already a proper noun
        pmi = _pmi_gloss(surface, lex) or _pmi_gloss(wl, lex) or "?"
        function_words[wl] = pmi   # Use lowercase key for lookup table

    # --- English gloss POS heuristics ---
    VERB_GLOSSES = {
        "go", "come", "say", "speak", "see", "hear", "know", "give", "take",
        "make", "do", "eat", "drink", "die", "live", "be", "have", "get",
        "put", "stand", "sit", "walk", "run", "fall", "rise", "carry",
        "bring", "send", "find", "tell", "ask", "call", "follow", "help",
        "serve", "rule", "build", "plant", "sow", "reap", "wash", "pray",
        "sin", "forgive", "love", "hate", "fear", "trust", "believe",
        "seek", "keep", "hold", "open", "close", "break", "destroy",
        "kill", "smite", "dwell", "abide", "return", "depart", "enter",
        "cast", "throw", "pour", "anoint", "bless", "curse", "swear",
        "worship", "offer", "sacrifice", "teach", "preach", "write",
        "read", "weep", "rejoice", "suffer", "heal", "raise", "save",
        "redeem", "create", "fill", "gather", "scatter", "divide",
        "answer", "obey", "disobey", "arise", "appear", "turn", "shew",
        "show", "command", "forbid", "receive", "give", "increase",
        "decrease", "dwell", "endure", "exist", "become", "start",
        "finish", "begin", "end", "remember", "forget", "choose",
        "appoint", "send", "come", "go", "bring", "lead", "pass",
        "happen", "fall", "rise", "draw", "pull", "push", "lift",
        "lay", "set", "place", "meet", "greet", "visit", "guard",
    }

    NOUN_GLOSSES = {
        "man", "woman", "person", "people", "son", "daughter", "father",
        "mother", "brother", "sister", "king", "lord", "god", "servant",
        "slave", "enemy", "priest", "prophet", "judge", "warrior",
        "house", "city", "land", "country", "field", "mountain", "valley",
        "river", "sea", "water", "fire", "stone", "bread", "wine",
        "gold", "silver", "blood", "flesh", "heart", "hand", "eye",
        "day", "night", "year", "time", "word", "name", "law", "covenant",
        "prayer", "offering", "sacrifice", "temple", "altar", "tent",
        "sword", "bow", "army", "tribe", "clan", "family", "generation",
        "sin", "iniquity", "righteousness", "glory", "honor", "fear",
        "love", "peace", "joy", "sorrow", "anger", "grace", "mercy",
        "blessing", "curse", "life", "death", "soul", "spirit", "flesh",
        "heaven", "earth", "wilderness", "desert", "tree", "fruit",
        "sheep", "ox", "horse", "bird", "fish", "bread", "milk",
        "oil", "garment", "robe", "crown", "throne", "gate", "wall",
        "voice", "mouth", "face", "head", "foot", "way", "path",
        "nation", "gentile", "hebrew", "israelite", "child", "infant",
        "elder", "leader", "captain", "servant", "slave", "prisoner",
        "thing", "matter", "work", "deed", "sign", "wonder", "dream",
    }

    already_classified = set(function_words.keys()) | {p.lower() for p in proper_nouns}

    verb_stems: dict[str, str] = {}
    noun_stems: dict[str, str] = {}
    unknowns: list[tuple[int, str, str]] = []  # (freq, word, pmi_gloss)

    for word, cnt in freq.most_common():
        wl = word.lower()
        if wl in already_classified:
            continue
        if word in proper_nouns or wl in {p.lower() for p in proper_nouns}:
            continue
        if cnt < 2:
            # Hapax / near-hapax: put in unknowns list (too rare to classify)
            pmi = _pmi_gloss(word, lex) or _pmi_gloss(wl, lex) or "?"
            unknowns.append((cnt, wl, pmi))
            continue

        pmi = _pmi_gloss(word, lex) or _pmi_gloss(wl, lex)
        if pmi and pmi.lower() in VERB_GLOSSES:
            verb_stems[wl] = pmi.lower()
            already_classified.add(wl)
        elif pmi and pmi.lower() in NOUN_GLOSSES:
            noun_stems[wl] = pmi.lower()
            already_classified.add(wl)
        else:
            unknowns.append((cnt, wl, pmi or "?"))

    # Sort unknowns by descending frequency (highest-impact work first)
    unknowns.sort(key=lambda x: -x[0])

    return {
        "proper_nouns": proper_nouns,
        "function_words": function_words,
        "verb_stems": verb_stems,
        "noun_stems": noun_stems,
        "unknowns": unknowns,
        "freq": freq,
    }


# ---------------------------------------------------------------------------
# Step 5 – estimate initial coverage (before any manual work)
# ---------------------------------------------------------------------------
def estimate_coverage(freq: Counter, classified: dict) -> dict:
    """
    Quick coverage estimate: what fraction of tokens can the scaffold gloss?

    Only counts entries that have a real (non-'?') gloss, so the estimate
    matches what the generated scaffold's --coverage command will report.
    """
    proper_lower = {w.lower() for w in classified["proper_nouns"]}
    # Function words may have '?' as gloss (PMI couldn't align them well);
    # those are in the scaffold but will be flagged as unknowns at runtime.
    func_confirmed = {
        w for w, g in classified["function_words"].items() if g and g != "?"
    }
    verb_lower = set(classified["verb_stems"].keys())
    noun_lower = set(classified["noun_stems"].keys())

    covered_types = proper_lower | func_confirmed | verb_lower | noun_lower
    covered_tokens = sum(cnt for word, cnt in freq.items() if word.lower() in covered_types)
    total_tokens = sum(freq.values())

    return {
        "total_tokens": total_tokens,
        "covered_tokens": covered_tokens,
        "coverage_pct": 100 * covered_tokens / total_tokens if total_tokens else 0,
        "proper_noun_types": len(classified["proper_nouns"]),
        "function_word_types": len(classified["function_words"]),
        "verb_stem_types": len(classified["verb_stems"]),
        "noun_stem_types": len(classified["noun_stems"]),
        "unknown_types": len(classified["unknowns"]),
    }


# ---------------------------------------------------------------------------
# Step 6 – generate the scaffold analyzer script
# ---------------------------------------------------------------------------

def _py_dict_entry(word: str, gloss: str, comment: str = "") -> str:
    """Format a single Python dictionary entry line."""
    w = repr(word)
    g = repr(gloss)
    if comment:
        return f"    {w}: {g},  # {comment}"
    return f"    {w}: {g},"


# ---------------------------------------------------------------------------
# Scaffold boilerplate (static Python code embedded in the generated file)
# These strings are written verbatim and do NOT go through .format(), so
# they can contain any Python syntax including { and } characters.
# ---------------------------------------------------------------------------

_SCAFFOLD_IMPORTS = '''\
import re
import sys
from pathlib import Path
from collections import Counter
'''

_SCAFFOLD_ENGINE = '''\
# =============================================================================
# MORPHOLOGICAL RULES
# =============================================================================
# These are common Kuki-Chin affix patterns.  VERIFY each one for this language
# before relying on it for coverage.
#
# The safest approach: add verified patterns, comment out others.

# Pronominal / agreement prefixes (check these against high-frequency words)
PREFIXES = {
    # Edit these to match actual patterns for this language:
    "ka":   "1SG",        # [VERIFY] cf. Tedim ka-, Mizo ka-
    "na":   "2SG",        # [VERIFY] cf. Tedim na-, Mizo na-/nang-
    "a":    "3SG",        # [VERIFY] cf. Tedim a-, Mizo a-
    "i":    "1PL.INCL",   # [VERIFY] cf. Tedim i-
    "ki":   "REFL",       # [VERIFY] cf. Tedim ki- (reflexive/reciprocal)
    "kan":  "1PL.EXCL",   # [VERIFY] cf. Mizo kan-
    "an":   "3PL",        # [VERIFY] cf. Mizo an-
}

# Case / TAM / derivational suffixes
SUFFIXES = {
    # Edit these to match actual patterns for this language:
    "in":   "ERG",        # [VERIFY] Ergative in Tedim; NMLZ in some KC langs
    "ah":   "LOC",        # [VERIFY] Locative in Tedim
    "te":   "PL",         # [VERIFY] Plural across many KC languages
    "na":   "NMLZ",       # [VERIFY] Nominalizer in Tedim
    "ding": "IRR",        # [VERIFY] Irrealis in Tedim; "tur" in Mizo?
    "zo":   "COMPL",      # [VERIFY] Completive in Tedim
    "ta":   "PFV",        # [VERIFY] Perfective in Tedim
    "sak":  "CAUS",       # [VERIFY] Causative across many KC languages
    "pih":  "APPL",       # [VERIFY] Applicative in Tedim
    "kik":  "ITER",       # [VERIFY] Iterative in Tedim
    "nawn": "CONT",       # [VERIFY] Continuative in Tedim
    "khin": "IMM",        # [VERIFY] Immediate in Tedim
    "khia": "out",        # [VERIFY] Directional suffix
    "lut":  "in",         # [VERIFY] Directional suffix
    "toh":  "UP",         # [VERIFY] Elevational directional
    "suk":  "DOWN",       # [VERIFY] Elevational directional
}


# =============================================================================
# ANALYSIS ENGINE
# =============================================================================

def normalize_word(word: str) -> str:
    """Strip punctuation, normalize apostrophes."""
    word = word.replace("\\u2019", "'").replace("\\u2018", "'")
    word = re.sub(r"^[^\\w\\']+|[^\\w\\']+$", "", word)
    return word


def analyze_word(word: str) -> tuple[str, str]:
    """
    Analyze a single word token and return (segmented_form, gloss).

    Priority order (following Tedim architecture):
      1. FUNCTION_WORDS   -- closed class, highest frequency
      2. COMPOUND_WORDS   -- pre-analyzed to prevent over-decomposition
      3. PROPER_NOUNS     -- biblical names + detected proper nouns
      4. VERB_STEMS       -- lexical verbs
      5. NOUN_STEMS       -- lexical nouns
      6. Prefix stripping -- productive morphological rules
      7. Suffix stripping -- productive morphological rules
      8. Unknown          -- return (word, "?")
    """
    if not word:
        return ("", "")

    clean = normalize_word(word)
    if not clean:
        return (word, "")

    # Possessive apostrophe handling (common in KC languages)
    if clean.endswith("'"):
        base = clean[:-1]
        seg, gloss = analyze_word(base)
        if gloss and gloss != "?":
            return (seg + "'", gloss + ".POSS")

    # 1. Function words (case-insensitive)
    result = FUNCTION_WORDS.get(clean) or FUNCTION_WORDS.get(clean.lower())
    if result:
        return (clean, result)

    # 2. Compound words (exact match first)
    compound = COMPOUND_WORDS.get(clean) or COMPOUND_WORDS.get(clean.lower())
    if compound:
        return compound  # returns (segmented_form, gloss) tuple

    # 3. Proper nouns (case-sensitive lookup, then title-case fallback)
    if clean in PROPER_NOUNS:
        return (clean, PROPER_NOUNS[clean])
    proper_lower = {p.lower(): (p, g) for p, g in PROPER_NOUNS.items()}
    if clean.lower() in proper_lower:
        canon, gloss_pn = proper_lower[clean.lower()]
        return (clean, gloss_pn)
    # Unknown capitalised word -> treat as proper noun with suffix check
    if clean[0].isupper() and clean.lower() not in VERB_STEMS and clean.lower() not in NOUN_STEMS:
        for suf, suf_gloss in SUFFIXES.items():
            if clean.endswith(suf) and len(clean) > len(suf) + 1:
                base = clean[:-len(suf)]
                if base.lower() in proper_lower:
                    _, gloss_base = proper_lower[base.lower()]
                    return (base + "-" + suf, gloss_base + "-" + suf_gloss)
        return (clean, "PN")

    # 4. Verb stems
    vstem = VERB_STEMS.get(clean.lower())
    if vstem:
        return (clean, vstem)

    # 5. Noun stems
    nstem = NOUN_STEMS.get(clean.lower())
    if nstem:
        return (clean, nstem)

    # 6. Prefix stripping (longest-match first)
    for prefix in sorted(PREFIXES, key=len, reverse=True):
        if clean.lower().startswith(prefix) and len(clean) > len(prefix) + 1:
            remainder = clean[len(prefix):]
            rem_seg, rem_gloss = analyze_word(remainder)
            if rem_gloss and rem_gloss != "?":
                return (prefix + "-" + rem_seg, PREFIXES[prefix] + "-" + rem_gloss)

    # 7. Suffix stripping (longest-match first)
    for suffix in sorted(SUFFIXES, key=len, reverse=True):
        if clean.lower().endswith(suffix) and len(clean) > len(suffix) + 1:
            stem = clean[:-len(suffix)]
            stem_seg, stem_gloss = analyze_word(stem)
            if stem_gloss and stem_gloss != "?":
                return (stem_seg + "-" + suffix, stem_gloss + "-" + SUFFIXES[suffix])

    # 8. Unknown
    return (clean, "?")


# =============================================================================
# COVERAGE MEASUREMENT
# =============================================================================

def is_word_token(token: str) -> bool:
    """Return True if token is a real word (not punctuation or URL)."""
    clean = re.sub(r"^[^\\w\\']+|[^\\w\\']+$", "", token)
    if not clean or not re.search(r"[a-zA-Z\\u00C0-\\u024F\\u1E00-\\u1EFF]", clean):
        return False
    url_fragments = {"http", "https", "www", "com", "org", "bible"}
    if clean.lower() in url_fragments:
        return False
    if clean.lower().startswith("http") or "www" in clean.lower():
        return False
    return True


def check_coverage(verbose: bool = False) -> dict:
    """Measure coverage over the full Bible corpus."""
    if not BIBLE_PATH.exists():
        print(f"Error: Bible file not found: {BIBLE_PATH}")
        sys.exit(1)

    total, full, partial, unknown = 0, 0, 0, 0
    unknown_words: Counter = Counter()
    partial_words: list = []

    with open(BIBLE_PATH, encoding="utf-8") as fh:
        for line in fh:
            line = line.replace("\\u2019", "'").replace("\\u2018", "'").rstrip("\\n")
            if line.startswith("#") or "\\t" not in line:
                continue
            _, text = line.split("\\t", 1)
            for token in text.split():
                if not is_word_token(token):
                    continue
                clean = re.sub(r"^[^\\w\\']+|[^\\w\\']+$", "", token)
                total += 1
                _, gloss = analyze_word(clean)
                if not gloss or gloss == "?":
                    unknown += 1
                    unknown_words[clean] += 1
                elif "?" in gloss:
                    partial += 1
                    partial_words.append((clean, gloss))
                else:
                    full += 1

    coverage = 100 * full / total if total else 0
    result = {
        "total": total,
        "full": full,
        "partial": partial,
        "unknown": unknown,
        "coverage_pct": coverage,
    }
    if verbose:
        result["unknown_words"] = unknown_words
        result["partial_words"] = partial_words
    return result


# =============================================================================
# PHILOLOGICAL LOOKUP HELPER
# =============================================================================

def kjv_context(word: str, max_verses: int = 3) -> None:
    """
    Print KJV English parallel verses for a word.

    This is the core philological method:
      1. Find Bible verses containing the word
      2. Look up KJV English for those verse IDs
      3. Infer meaning from English context
    """
    iso_dir = BIBLE_PATH.parent
    kjv_path = iso_dir.parent / "eng" / "eng-x-bible.txt"

    verse_ids = []
    with open(BIBLE_PATH, encoding="utf-8") as fh:
        for line in fh:
            if "\\t" not in line or line.startswith("#"):
                continue
            vid, text = line.split("\\t", 1)
            if re.search(r"\\b" + re.escape(word) + r"\\b", text, re.IGNORECASE):
                verse_ids.append(vid)
                if len(verse_ids) >= max_verses:
                    break

    if not verse_ids:
        print(f"  '{word}' not found in corpus")
        return

    kjv: dict[str, str] = {}
    if kjv_path.exists():
        with open(kjv_path, encoding="utf-8") as fh:
            for line in fh:
                if "\\t" not in line or line.startswith("#"):
                    continue
                vid, text = line.split("\\t", 1)
                if vid in verse_ids:
                    kjv[vid] = text.strip()

    print(f"\\nKJV context for '{word}':")
    for vid in verse_ids:
        print(f"  [{vid}] {kjv.get(vid, '(KJV not available)')}")


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

def main():
    iso = BIBLE_PATH.parent.name
    if len(sys.argv) < 2:
        print(f"Usage: python analyze_morphemes_{iso}.py <word>")
        print(f"       python analyze_morphemes_{iso}.py --coverage [-v]")
        print(f"       python analyze_morphemes_{iso}.py --lookup <word>")
        sys.exit(1)

    if sys.argv[1] == "--coverage":
        verbose = "-v" in sys.argv or "--verbose" in sys.argv
        result = check_coverage(verbose=verbose)
        print(f"Total tokens:  {result['total']:,}")
        print(f"Full glosses:  {result['full']:,} ({result['coverage_pct']:.4f}%)")
        print(f"Partial:       {result['partial']:,}")
        print(f"Unknown:       {result['unknown']:,}")
        if verbose and result.get("unknown_words"):
            print("\\nTop 30 unknowns (by frequency):")
            for w, cnt in result["unknown_words"].most_common(30):
                seg, gloss = analyze_word(w)
                print(f"  {cnt:5d}x  {w:<25} -> {gloss}")

    elif sys.argv[1] == "--lookup":
        if len(sys.argv) < 3:
            print(f"Usage: python analyze_morphemes_{iso}.py --lookup <word>")
            sys.exit(1)
        kjv_context(sys.argv[2])

    else:
        word = sys.argv[1]
        seg, gloss = analyze_word(word)
        print(f"Word:      {word}")
        print(f"Segmented: {seg}")
        print(f"Gloss:     {gloss}")


if __name__ == "__main__":
    main()
'''

REPORT_TEMPLATE = '''\
# {lang_name} ({iso}) Bootstrap Report

Generated: {today}
Script: `scripts/bootstrap_analyzer.py`

## Initial Coverage Estimate

| Metric | Value |
|--------|-------|
| Total corpus tokens | {total_tokens:,} |
| Tokens auto-covered | {covered_tokens:,} |
| **Estimated coverage** | **{coverage_pct:.1f}%** |

Coverage breakdown by source:

| Category | Types | Coverage source |
|----------|-------|-----------------|
| Proper nouns | {proper_noun_types:,} | Capitalisation + biblical name detection |
| Function words | {function_word_types:,} | Top-{function_word_top_n} most-frequent words |
| Verb stems | {verb_stem_types:,} | PMI alignment (verbal glosses) |
| Noun stems | {noun_stem_types:,} | PMI alignment (nominal glosses) |
| **Unknown types remaining** | **{unknown_types:,}** | Needs manual work |

## Generated Files

- `scripts/analyze_morphemes_{iso}.py` — scaffold analyzer (run immediately!)
- `analysis/{iso}_bootstrap_report.md` — this file

## Immediate Next Steps

### Step 1: Run coverage check (do this now)

```bash
python scripts/analyze_morphemes_{iso}.py --coverage
```

### Step 2: Inspect top unknowns

```bash
python scripts/analyze_morphemes_{iso}.py --coverage -v
```

### Step 3: Investigate each unknown with KJV cross-reference

```bash
# Built-in lookup tool:
python scripts/analyze_morphemes_{iso}.py --lookup <WORD>

# Or manual bash approach:
word="<WORD>"
verse=$(grep -m1 "\\t.*\\b$word\\b" bibles/extracted/{iso}/{iso}-x-bible.txt | cut -f1)
grep "^$verse\\t" data/verses_aligned.tsv | cut -f3   # KJV English
```

### Step 4: Add to the appropriate dictionary

- If it\'s a function word (closed class, grammatical) → add to `FUNCTION_WORDS`
- If it\'s a verb → add to `VERB_STEMS`
- If it\'s a noun → add to `NOUN_STEMS`
- If it\'s a compound → add to `COMPOUND_WORDS` (prevents over-decomposition)
- If it\'s a proper noun → add to `PROPER_NOUNS`

### Step 5: Verify affix patterns

Open `scripts/analyze_morphemes_{iso}.py` and check the `PREFIXES` and `SUFFIXES`
dicts.  Each is marked `[VERIFY]` — use corpus evidence to confirm or remove.

The most productive approach: look at the top unknown words and check whether
they can be analyzed as known_stem + affix.

## Top 50 Unknown Word Types (sorted by frequency)

| Rank | Frequency | Word | PMI candidate gloss |
|------|-----------|------|---------------------|
{unknowns_table}

## Affix Investigation Queries

Use these bash commands to investigate potential affixes in the corpus:

```bash
# How many words end in each suffix candidate?
for suffix in in ah na te tûr rawh; do
  count=$(grep -o "\\\\b[a-z]*$suffix\\\\b" bibles/extracted/{iso}/{iso}-x-bible.txt | sort -u | wc -l)
  echo "$suffix: $count unique types"
done

# Most frequent words ending in a specific suffix
suffix="te"  # change this
cut -f2 bibles/extracted/{iso}/{iso}-x-bible.txt | tr \' \'\\\\n\' | \\
  grep "$suffix\\$" | sort | uniq -c | sort -rn | head -20
```

## Coverage Improvement Log

| Date | Coverage | Action |
|------|----------|--------|
| {today} | {coverage_pct:.1f}% | Auto-bootstrapped |

---
*Generated by `scripts/bootstrap_analyzer.py`*
'''


def generate_scaffold(iso: str, lang_name: str, classified: dict, coverage: dict) -> str:
    """
    Build the content of the scaffold analyze_morphemes_{iso}.py file.

    Returns the full file content as a string.

    Note: We build the file by concatenating sections rather than using a
    single .format() call, because the engine code contains Python dict
    literals {{ }} that would collide with str.format() placeholders.
    """
    today = date.today().isoformat()
    parts: list[str] = []

    # ── header / docstring ───────────────────────────────────────────────────
    parts.append(f'''\
#!/usr/bin/env python3
"""
{lang_name} ({iso}) Morphological Analyzer — SCAFFOLD
Auto-generated {today} by bootstrap_analyzer.py

COVERAGE STATUS (estimated at generation time): {coverage["coverage_pct"]:.1f}%

HOW TO USE THIS SCAFFOLD
========================
1. Run coverage check immediately:
       python scripts/analyze_morphemes_{iso}.py --coverage

2. Identify the top unknowns:
       python scripts/analyze_morphemes_{iso}.py --coverage -v

3. For each unknown word, look it up using the philological method:
       python scripts/analyze_morphemes_{iso}.py --lookup <WORD>

4. Add the word to the appropriate dictionary below.

5. Common Kuki-Chin affixes (VERIFY these for {lang_name}):
   Prefixes: a- (3SG?), ka- (1SG?), na- (2SG?), kan- (1PL.EXCL?),
             ki- (REFL/RECIP?), an- (3PL?)
   Suffixes: -te (PL?), -in (ERG? or NMLZ?), -ah (LOC?), -na (NMLZ?),
             -tûr (IRR/PURP?), -ta (PFV?), -rawh (HORT?)

CONFIDENCE MARKERS IN COMMENTS
================================
  [AUTO-PN]     Proper noun auto-detected (capitalised, rare lowercase)
  [PMI:gloss]   Gloss suggested by PMI co-occurrence alignment
  [FREQ:N]      Frequency in corpus
  [VERIFY]      Needs manual verification against KJV
  [?]           PMI alignment was ambiguous; use philological method
"""

''')

    # ── imports ──────────────────────────────────────────────────────────────
    parts.append(_SCAFFOLD_IMPORTS)
    parts.append("\n")

    # ── BIBLE_PATH ───────────────────────────────────────────────────────────
    parts.append(f'''\
# =============================================================================
# CONFIGURATION
# =============================================================================

# Path to the Bible corpus for coverage measurement
BIBLE_PATH = (
    Path(__file__).parent.parent
    / "bibles" / "extracted" / "{iso}" / "{iso}-x-bible.txt"
)

''')

    # ── FUNCTION_WORDS ───────────────────────────────────────────────────────
    fw_lines = []
    for word, gloss in sorted(classified["function_words"].items()):
        cnt = classified["freq"].get(word, 0) + classified["freq"].get(word.title(), 0)
        fw_lines.append(_py_dict_entry(word, gloss, f"FREQ:{cnt} [VERIFY]"))
    fw_block = "\n".join(fw_lines) if fw_lines else "    # (none auto-detected)"

    parts.append(f'''\
# =============================================================================
# FUNCTION WORDS  (closed-class, ~60-70% of tokens)
# =============================================================================
# These are the {len(classified["function_words"])} most-frequent word forms in the corpus.
# Each gloss is the highest-confidence PMI candidate — verify against KJV!
# Pattern: word -> Leipzig-style gloss or English translation
#
# IMPORTANT: Tedim experience shows that getting these ~150 words right
# delivers the biggest coverage gains.  Work through them systematically.
#
FUNCTION_WORDS = {{
{fw_block}
}}

''')

    # ── VERB_STEMS ───────────────────────────────────────────────────────────
    vs_lines = []
    for word, gloss in sorted(classified["verb_stems"].items()):
        cnt = classified["freq"].get(word, 0)
        vs_lines.append(_py_dict_entry(word, gloss, f"FREQ:{cnt} [PMI:{gloss}] [VERIFY]"))
    vs_block = "\n".join(vs_lines) if vs_lines else "    # (none auto-detected)"

    parts.append(f'''\
# =============================================================================
# VERB STEMS
# =============================================================================
# Auto-classified via PMI alignment.  Verify each gloss against KJV.
# Add Form I / Form II alternations here (e.g., mu/muh for Tedim "see").
# Kuki-Chin typically marks Form II by adding -h or -k to Form I stem.
#
VERB_STEMS = {{
{vs_block}
}}

''')

    # ── NOUN_STEMS ───────────────────────────────────────────────────────────
    ns_lines = []
    for word, gloss in sorted(classified["noun_stems"].items()):
        cnt = classified["freq"].get(word, 0)
        ns_lines.append(_py_dict_entry(word, gloss, f"FREQ:{cnt} [PMI:{gloss}] [VERIFY]"))
    ns_block = "\n".join(ns_lines) if ns_lines else "    # (none auto-detected)"

    parts.append(f'''\
# =============================================================================
# NOUN STEMS
# =============================================================================
# Auto-classified via PMI alignment.  Verify each gloss against KJV.
#
NOUN_STEMS = {{
{ns_block}
}}

''')

    # ── COMPOUND_WORDS ───────────────────────────────────────────────────────
    parts.append('''\
# =============================================================================
# COMPOUND WORDS
# =============================================================================
# Pre-analyzed compounds that must not be decomposed by prefix/suffix rules.
# Format: surface_form -> (segmented_form, gloss)
# Add entries here when algorithmic decomposition gives the WRONG result.
#
COMPOUND_WORDS = {
    # Add compounds as you discover them:
    # 'biakinn': ('biak-inn', 'worship-house'),  # example from Tedim
}

''')

    # ── PROPER_NOUNS ─────────────────────────────────────────────────────────
    pn_lines = []
    for word in sorted(classified["proper_nouns"]):
        gloss = classified["proper_nouns"][word]
        cnt = classified["freq"].get(word, 0)
        pn_lines.append(_py_dict_entry(word, gloss, f"FREQ:{cnt} [AUTO-PN]"))
    pn_block = "\n".join(pn_lines) if pn_lines else "    # (none auto-detected)"

    parts.append(f'''\
# =============================================================================
# PROPER NOUNS  ({len(classified["proper_nouns"])} auto-detected)
# =============================================================================
# Words auto-detected as proper nouns because they appear >=85% capitalised
# and their lowercase form is not a high-frequency function word.
#
# Gloss format: PN.NAME (biblical name)  or  PN (name not in known list)
#
# NOTE: Suffix handling - many proper nouns take case suffixes (-in, -ah, -a).
# The analyze_word() function below handles these automatically.
#
PROPER_NOUNS = {{
{pn_block}
}}

''')

    # ── Engine (morphological rules + analysis functions) ────────────────────
    parts.append(_SCAFFOLD_ENGINE)

    return "".join(parts)


def generate_report(iso: str, lang_name: str, classified: dict, coverage: dict,
                    function_word_top_n: int) -> str:
    """Build the content of the bootstrap report Markdown file."""
    today = date.today().isoformat()

    unknowns_table_rows = []
    for rank, (cnt, word, pmi) in enumerate(classified["unknowns"][:50], start=1):
        unknowns_table_rows.append(f"| {rank} | {cnt:,} | `{word}` | {pmi} |")
    unknowns_table = "\n".join(unknowns_table_rows) if unknowns_table_rows else "| — | — | — | — |"

    return REPORT_TEMPLATE.format(
        lang_name=lang_name,
        iso=iso,
        today=today,
        total_tokens=coverage["total_tokens"],
        covered_tokens=coverage["covered_tokens"],
        coverage_pct=coverage["coverage_pct"],
        proper_noun_types=coverage["proper_noun_types"],
        function_word_types=coverage["function_word_types"],
        verb_stem_types=coverage["verb_stem_types"],
        noun_stem_types=coverage["noun_stem_types"],
        unknown_types=coverage["unknown_types"],
        function_word_top_n=function_word_top_n,
        unknowns_table=unknowns_table,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def get_lang_name(iso: str) -> str:
    """Try to get the language name from the datapackage.json."""
    dp = BIBLES_DIR / iso / "datapackage.json"
    if dp.exists():
        import json
        with open(dp) as f:
            data = json.load(f)
        return data.get("language_name", iso)
    # Fall back to metadata in the Bible text header
    candidates = sorted((BIBLES_DIR / iso).glob(f"{iso}-x-bible*.txt"))
    if candidates:
        with open(candidates[0], encoding="utf-8") as f:
            for line in f:
                if line.startswith("# language_name:"):
                    return line.split(":", 1)[1].strip()
    return iso


def main():
    parser = argparse.ArgumentParser(
        description="Bootstrap a morphological analyzer scaffold for a Kuki-Chin language.",
        epilog="Example: python scripts/bootstrap_analyzer.py lus"
    )
    parser.add_argument("iso", help="ISO 639-3 language code (e.g. lus, cfm, cnh)")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print report only; do not write any files"
    )
    parser.add_argument(
        "--function-words", type=int, default=150, metavar="N",
        help="Number of top-frequency words to seed as function word candidates (default: 150)"
    )
    args = parser.parse_args()

    iso = args.iso.lower()
    # Validate ISO code: must be 2-4 lowercase alphanumeric characters,
    # optionally followed by a hyphen+extension (e.g. czt-mbs).
    # This prevents any path traversal or injection via the iso argument.
    if not re.match(r'^[a-z]{2,4}(-[a-z]{1,6})?$', iso):
        print(f"ERROR: Invalid ISO code '{iso}'. Must be 2-4 lowercase letters (e.g. lus, cfm).")
        sys.exit(1)
    function_word_top_n = args.function_words

    print(f"\n{'='*60}")
    print(f"Bootstrap Analyzer: {iso.upper()}")
    print(f"{'='*60}")

    # Validate prerequisites
    iso_dir = BIBLES_DIR / iso
    if not iso_dir.is_dir():
        print(f"ERROR: Language directory not found: {iso_dir}")
        print("  Available languages:", ", ".join(
            d.name for d in sorted(BIBLES_DIR.iterdir()) if d.is_dir()
        ))
        sys.exit(1)

    lang_name = get_lang_name(iso)
    print(f"Language: {lang_name} ({iso})\n")

    # Step 1: Load corpus
    print("Step 1: Loading corpus...")
    verses, freq = load_corpus(iso)

    # Step 2: Load PMI lexicon
    print("\nStep 2: Loading PMI lexicon...")
    lex = load_lexicon(iso)

    # Step 3: Load KJV (optional, only for reporting)
    print("\nStep 3: Loading KJV (for cross-reference reporting)...")
    kjv = load_kjv()

    # Step 4: Classify words
    print(f"\nStep 4: Classifying words (top-{function_word_top_n} as function word candidates)...")
    classified = classify_words(freq, lex, function_word_top_n=function_word_top_n)
    print(f"  Proper nouns detected:  {len(classified['proper_nouns']):,}")
    print(f"  Function word seeds:    {len(classified['function_words']):,}")
    print(f"  Verb stem seeds:        {len(classified['verb_stems']):,}")
    print(f"  Noun stem seeds:        {len(classified['noun_stems']):,}")
    print(f"  Unknowns (to work on):  {len(classified['unknowns']):,}")

    # Step 5: Estimate coverage
    coverage = estimate_coverage(freq, classified)
    print(f"\nEstimated initial coverage: {coverage['coverage_pct']:.1f}%")
    print(f"  (from {coverage['covered_tokens']:,} / {coverage['total_tokens']:,} tokens)")

    # Step 6: Generate scaffold
    print("\nStep 6: Generating scaffold...")
    scaffold_content = generate_scaffold(iso, lang_name, classified, coverage)
    report_content = generate_report(iso, lang_name, classified, coverage, function_word_top_n)

    if args.dry_run:
        print("\n[DRY RUN] Would write:")
        print(f"  scripts/analyze_morphemes_{iso}.py  ({len(scaffold_content):,} chars)")
        print(f"  analysis/{iso}_bootstrap_report.md   ({len(report_content):,} chars)")
        print("\n--- First 40 lines of scaffold ---")
        for line in scaffold_content.split("\n")[:40]:
            print(" ", line)
        return

    # Write scaffold
    scaffold_path = SCRIPTS_DIR / f"analyze_morphemes_{iso}.py"
    with open(scaffold_path, "w", encoding="utf-8") as f:
        f.write(scaffold_content)
    print(f"  Wrote: {scaffold_path}")

    # Write report
    ANALYSIS_DIR.mkdir(exist_ok=True)
    report_path = ANALYSIS_DIR / f"{iso}_bootstrap_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    print(f"  Wrote: {report_path}")

    print(f"\n{'='*60}")
    print("DONE!  Next steps:")
    print(f"  1. Run: python scripts/analyze_morphemes_{iso}.py --coverage")
    print(f"  2. Run: python scripts/analyze_morphemes_{iso}.py --coverage -v")
    print(f"  3. Investigate unknowns with: python scripts/analyze_morphemes_{iso}.py --lookup <word>")
    print(f"  4. Read: analysis/{iso}_bootstrap_report.md")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
