# Kuki-Chin Morphological Analyzer: Lessons Learned & Bug Log

## Overview

This document captures specific issues encountered during the development of morphological analyzers for Kuki-Chin languages, beginning with Tedim Chin (ctd). It documents wrong turns, bugs discovered, solutions, and best practices for applying this methodology to additional languages.

**Target Languages (18+):** Bawm (bgr), Falam (cfm), Hakha (cnh), Khumi (cnk, cek), Mizo (lus), Nga'la/Hlawng (hlt), Sizang (csy), Tedim (ctd), Zotung (czt), Zomi (zom), and others.

---

## 1. Critical Bugs & Their Fixes

### Bug 1: Over-Decomposition of Short Stems

**Discovery:** Words like "sim" (read) were being incorrectly analyzed as "si-m" (be-?)

**Root Cause:** The prefix-stripping algorithm tried "si-" prefix before checking if "sim" was a known stem.

**Fix:** Reorder lookup priority:
```python
# CORRECT ORDER:
1. Check COMPOUND_WORDS first
2. Check full-word stems (VERB_STEMS, NOUN_STEMS)
3. THEN try prefix/suffix stripping
```

**Prevention:** Always add known compounds/words BEFORE enabling decomposition rules.

---

### Bug 2: Case Sensitivity Mismatches

**Discovery:** "Tua" (sentence-initial "that") wasn't matching "tua" in dictionary.

**Root Cause:** Dictionary lookup was case-sensitive by default.

**Fix:** 
```python
def lookup(word):
    if word in DICTIONARY:
        return DICTIONARY[word]
    if word.lower() in DICTIONARY:
        return DICTIONARY[word.lower()]
    return None
```

**Prevention:** Always implement case-folding fallback in lookup functions.

---

### Bug 3: Unicode Apostrophe vs ASCII Apostrophe

**Discovery:** Possessive forms like "Topa'" weren't being recognized; forms with curly apostrophes were being misanalyzed.

**Root Cause:** Corpus uses U+2019 (RIGHT SINGLE QUOTATION MARK), code checked for U+0027 (APOSTROPHE).

**Examples:**
- `Topa'` = `Topa\u2019` (Lord's) - curly apostrophe
- Not `Topa'` = `Topa\u0027` - straight apostrophe

**Fix (2026-03-08):** Normalize curly apostrophes to straight at the start of `analyze_word()`:
```python
# In analyze_word(), after clean_word():
word = word.replace('\u2019', "'").replace('\u2018', "'")
```

This single fix improved coverage from 98.49% to 98.51% (+200 tokens) by allowing all apostrophe-variant words to match dictionary entries.

**Prevention:** Always normalize Unicode quotation marks early in the analysis pipeline. Use `repr(text)` to inspect actual codepoints.

---

### Bug 4: Stem I/II Not Both Registered

**Discovery:** Coverage would fluctuate based on which verb form appeared.

**Root Cause:** Only Stem I or Stem II was added, not both.

**Example:**
```python
# WRONG - only one form:
VERB_STEMS = {'mu': 'see'}

# CORRECT - both forms:
VERB_STEMS = {'mu': 'see', 'muh': 'see'}
```

**Prevention:** When adding a verb, always ask: "Does this verb have Stem I/II alternation?" Common patterns:
- Final vowel (Stem I) → final `-h` (Stem II): `nei/neih`, `mu/muh`
- Final consonant (Stem I) → final `-k` or `-ng` (Stem II): `za/zak`

---

### Bug 5: Hyphen Handling Inconsistency

**Discovery:** "ka-ut" (my son) wasn't matching, but "kaut" was.

**Root Cause:** Some words written with hyphens, others without.

**Fix:** Check both forms:
```python
def analyze_word(word):
    # First check compound dictionary
    if word in COMPOUND_WORDS:
        return COMPOUND_WORDS[word]
    
    # If has hyphen, try analyzing parts
    if '-' in word:
        parts = word.split('-')
        glosses = [analyze_part(p) for p in parts]
        return ('-'.join(parts), '-'.join(glosses))
    
    # Continue with other analysis...
```

---

### Bug 6: Greedy Prefix Matching

**Discovery:** "hongpih" was analyzed as "hong-pih" (3→1-accompany), but "ho-ngpih" was tried first (nonsense).

**Root Cause:** Prefix list included "ho-" before "hong-", and greedy matching took first match.

**Fix:** Sort prefixes by length (longest first):
```python
PREFIXES = sorted(['ka', 'na', 'a', 'kong', 'hong', 'ki', 'nong', ...], 
                  key=len, reverse=True)
```

---

### Bug 7: Recursive Decomposition Loops

**Discovery:** Certain words caused infinite loops or very deep recursion.

**Root Cause:** Recursive suffix stripping without a base case check.

**Fix:**
```python
def analyze_recursive(word, depth=0):
    if depth > 5:  # Maximum recursion depth
        return (word, '?')
    if len(word) < 2:  # Minimum stem length
        return (word, '?')
    # ... continue analysis
```

---

### Bug 8: N+N Compound Remaining Morpheme Gloss Lookup Failure

**Discovery (2026-03-13):** Words like `khutlum` (palm) were being glossed as `hand-?` despite `lum` having a gloss in ATOMIC_GLOSSES.

**Root Cause:** After successful stem parsing (finding `khut` = hand), the remaining morpheme `lum` was marked with `?` without checking if it existed in ATOMIC_GLOSSES, NOUN_STEMS, or VERB_STEMS.

**Location:** Lines 14834-14848 in `analyze_word()`, in the stem parsing section.

**Fix:**
```python
# After: remaining = word[len(stem):]
# BEFORE (wrong): remaining_gloss = '?'
# AFTER (correct):
if remaining_lower in ATOMIC_GLOSSES:
    remaining_gloss = ATOMIC_GLOSSES[remaining_lower]
elif remaining_lower in NOUN_STEMS:
    remaining_gloss = NOUN_STEMS[remaining_lower]
elif remaining_lower in VERB_STEMS:
    remaining_gloss = VERB_STEMS[remaining_lower]
elif remaining_lower in VERB_STEM_PAIRS:
    remaining_gloss = VERB_STEM_PAIRS[remaining_lower]
else:
    remaining_gloss = '?'
```

**Impact:** +952 tokens fixed (from 828,200 to 829,152).

**Prevention:** When decomposing compounds, always check ALL gloss dictionaries for remaining morphemes before marking as unknown.

---

### Bug 9: Greedy Single-Character Prefix Parsing

**Discovery (2026-03-13):** Word `innpiah` (great house, palace) was being analyzed as `i-nnpiah` (1PL.INCL-?) instead of `inn-pi-ah` (house-big-LOC).

**Root Cause:** Single-character prefix `i-` was being stripped even when the word started with a longer known stem (`inn` = house). The algorithm found `i-` as a valid prefix and stripped it, leaving `nnpiah` which couldn't be parsed.

**Location:** Lines 14526-14560 in `analyze_word()`, in the prefix stripping section.

**Fix:** Before stripping a single-character prefix, check three conditions:
```python
# Don't strip single-char prefix if:
# 1. Remainder starts with doubled consonant (suggests gemination, not prefix)
if len(remainder) >= 2 and remainder[0] == remainder[1] and remainder[0] in 'bcdfghjklmnpqrstvwxyz':
    continue  # Skip this prefix
    
# 2. Full word is a known stem  
if word_lower in NOUN_STEMS or word_lower in VERB_STEMS:
    continue  # Skip this prefix
    
# 3. A longer stem exists starting with this character
if any(word_lower.startswith(stem) and len(stem) > 1 
       for stem in list(NOUN_STEMS.keys()) + list(VERB_STEMS.keys())):
    continue  # Skip this prefix
```

**Impact:** +76 tokens fixed.

**Prevention:** Single-character prefix stripping is dangerous. Add protective checks to avoid stripping when the word clearly starts with a longer stem.

---

## 2. Wrong Turns (Approaches That Didn't Work)

### Wrong Turn 1: Aggressive Spelling Normalization

**What We Tried:** Normalize all spelling variations early (e.g., "th" → "t" in some contexts).

**Why It Failed:** 
- Some "variations" were actually meaningful distinctions
- Conflated genuinely different morphemes
- Lost phonological information

**Lesson:** Don't normalize spelling until you understand the morphology. Keep original forms and document variation patterns separately.

---

### Wrong Turn 2: Pure Rule-Based Decomposition

**What We Tried:** Rely entirely on prefix/suffix stripping rules without a compound dictionary.

**Why It Failed:**
- Many compounds don't decompose transparently
- Some "prefixes" are actually part of the stem
- Over-decomposition everywhere

**Lesson:** Build a substantial compound dictionary FIRST, then add decomposition rules carefully.

---

### Wrong Turn 3: Copying Morpheme Inventories from Literature

**What We Tried:** Use Henderson 1965's morpheme inventory directly.

**Why It Failed:**
- Corpus contains vocabulary not in Henderson
- Henderson's transcription differs from Bible orthography
- Some glosses needed updating to Leipzig conventions

**Lesson:** Secondary literature is a GUIDE, not a substitute for corpus-driven analysis.

---

### Wrong Turn 4: Batch Dictionary Additions Without Testing

**What We Tried:** Add 50+ dictionary entries at once before re-testing coverage.

**Why It Failed:**
- Typos and errors accumulated
- Hard to identify which entry caused a bug
- Bugs compounded (wrong entries affected other analyses)

**Lesson:** Add entries in small batches (10-20), test after each batch.

---

### Wrong Turn 5: Prioritizing Rare Words Over Patterns

**What We Tried:** Manually add every rare word encountered.

**Why It Failed:**
- Diminishing returns: each word adds tiny coverage
- Time-consuming
- Many rare words follow productive patterns

**Lesson:** Focus on PATTERNS, not individual items. If 50 words follow the same suffix pattern, add the suffix rule, not 50 dictionary entries.

---

## 3. Coverage Plateau Points

| Coverage | Typical Blockers | Solution |
|----------|-----------------|----------|
| 60% | Missing function words | Add top 100 frequency items |
| 75% | Missing common verbs | Add verb stems (both Stem I/II) |
| 85% | Missing compounds | Build COMPOUND_WORDS dictionary |
| 92% | Missing ki-/reflexive forms | Add ki- prefix rule with proper stems |
| 95% | Missing reduplication | Add reduplication pattern handler |
| 97% | Rare vocabulary, proper nouns | Philological analysis, add proper noun list |
| 98% | Unicode issues, edge cases | Normalize apostrophes (U+2019→U+0027) |
| 99% | Gloss lookup bugs, greedy parsing | Fix remaining morpheme lookups (Bug 8), protect prefix stripping (Bug 9) |
| 99.5%+ | Hapax, dialectal forms, loans | Document but don't chase exhaustively |

---

## 4. Debugging Techniques

### Technique 1: Coverage Delta Testing
```bash
# Before change
python3 -c "..." > coverage_before.txt

# Make change

# After change
python3 -c "..." > coverage_after.txt

# Compare
diff coverage_before.txt coverage_after.txt
```

### Technique 2: Single-Word Testing
```bash
python3 scripts/analyze_morphemes.py "wordform"
# Shows: Word: wordform
#        Segmented: ...
#        Gloss: ...
```

### Technique 3: Verse Context Testing
```bash
# Find all verses containing a word
grep "targetword" bibles/extracted/ctd/ctd-x-bible.txt

# Analyze in KJV context
grep "VERSE.ID" bibles/extracted/eng/eng-x-bible.txt
```

### Technique 4: Top Unknown Words
```python
# After running coverage test, print top unknown words
for word, count in sorted(unknown_words.items(), key=lambda x: -x[1])[:20]:
    print(f"{count:5d}x  {word}")
```

---

## 5. Quality Checks

### Check 1: No Regression
After any change, coverage should not DECREASE (unless intentionally removing wrong analyses).

### Check 2: Sample Accuracy
Randomly sample 20 analyzed words, manually verify correctness:
```python
import random
analyzed_words = [w for w in all_words if '?' not in analyze_word(w)[1]]
sample = random.sample(analyzed_words, 20)
for w in sample:
    seg, gl = analyze_word(w)
    print(f"{w:20s} -> {seg:30s} = {gl}")
    # Manually check if this is correct
```

### Check 3: Homophone Awareness
Words like "a" (3SG, LOC, and generic article) need context disambiguation. The analyzer should pick the most common gloss but document alternatives.

### Check 4: No Phantom Morphemes
If a gloss contains "?", the word is not fully analyzed. Never ship an analyzer that produces "?" in supposedly-analyzed output.

---

## 6. Summary: Top 10 Rules for Future Languages

1. **Function words first** - They cover 60% of tokens
2. **Compound dictionary before decomposition rules**
3. **Always add both Stem I and Stem II for verbs**
4. **Sort prefixes/suffixes by length (longest first)**
5. **Handle Unicode apostrophes (U+2019)**
6. **Test after every 10-20 additions**
7. **Cross-reference with KJV for unknown vocabulary**
8. **Document, don't normalize, spelling variation**
9. **Accept 97% as "excellent" - don't chase 100%**
10. **Keep detailed logs of what was added and why**
11. **PREPROCESSING FIRST** - Clean corpus artifacts before analysis (see Section 7)

---

## 7. Corpus Preprocessing Pipeline (Critical Foundation)

### The Problem We Discovered

During Tedim Chin development, we encountered web scraping artifacts being treated as vocabulary:
- `scraped`, `https`, `www`, `bible.com`, `copyright` appeared as "unknown words"
- These were handled ad-hoc by adding them to FGN (foreign) entries
- This pollutes the lexicon and masks the true coverage

**Root Cause:** Metadata embedded in corpus text files leaked into analysis.

### Recommended Architecture

**Before (problematic):**
```
bibles/extracted/ctd/ctd-x-bible.txt
├── # language_name: Tedim Chin    ← Metadata mixed with text
├── # URL: https://www.bible.com  
├── 01001001  In the beginning...  ← Verse data
└── ...
```

**After (clean separation):**
```
bibles/extracted/ctd/
├── metadata.json           ← All provenance info
├── ctd-x-bible.txt         ← Pure verse text only
└── ctd-x-bible.raw.txt     ← Original scrape (archival)
```

### metadata.json Schema

```json
{
  "language_name": "Tedim Chin",
  "iso_639_3": "ctd",
  "source": {
    "url": "https://www.bible.com/bible/368",
    "scrape_date": "2026-03-01",
    "scrape_tool": "bible_scraper.py v1.0"
  },
  "copyright": {
    "holder": "See bible.com for copyright information",
    "usage_terms": "For research purposes"
  },
  "preprocessing": {
    "date": "2026-03-13",
    "steps": ["removed_metadata_lines", "normalized_unicode", "removed_html_artifacts"]
  },
  "statistics": {
    "total_verses": 31102,
    "total_tokens": 851068,
    "unique_tokens": 45230
  }
}
```

### Preprocessing Script (scripts/preprocess_corpus.py)

Should perform these steps IN ORDER:

1. **Extract metadata** - Parse `#`-prefixed lines into JSON
2. **Remove metadata lines** - Leave only `VERSE_ID\ttext` lines
3. **Normalize Unicode**:
   - `\u2019` → `'` (curly apostrophe → straight)
   - `\u2018` → `'`
   - `\u201c`/`\u201d` → `"` (curly quotes)
   - NBSP → space
4. **Remove HTML artifacts** - `&amp;`, `&nbsp;`, stray tags
5. **Validate format** - Every line matches `^[0-9]{8}\t.+$`
6. **Archive original** - Keep `.raw.txt` for provenance

### Why This Matters for 18 Languages

If preprocessing isn't standardized:
- Each language's analyzer will have ad-hoc FGN entries for the same artifacts
- Coverage comparisons across languages will be inconsistent
- Bugs will be replicated 18 times
- Foreign word lists will bloat with metadata terms

### Action Items for This Project

1. [ ] Create `scripts/preprocess_corpus.py` 
2. [ ] Generate `metadata.json` for all 20 extracted languages
3. [ ] Clean existing `.txt` files (archive originals as `.raw.txt`)
4. [ ] Remove FGN entries for metadata artifacts (scraped, https, etc.)
5. [ ] Update scraping scripts to output clean format from start

---

## 8. Hierarchical Compound Analysis System

### Discovery

During Tedim Chin analysis, we discovered that long compounds have nested structure:

```
singnamtui = sing + namtui = sing + (nam + tui)
         = tree + perfume = tree + (smell + water)
         = "spices"
```

Simply glossing `singnamtui = spices` loses the compositional semantics.

### Solution: Multi-Level Representation

We implemented a system that captures BOTH:
- **Lexical gloss**: The established meaning (`spices`)
- **Compositional gloss**: The morpheme-by-morpheme breakdown (`tree-(smell-water)`)

### Data Structures

```python
@dataclass
class CompoundStructure:
    morphemes: list[str]          # ['sing', 'nam', 'tui']
    segmentation: str              # 'sing-nam-tui'
    bracketing: str                # 'sing-(nam-tui)'
    compositional_gloss: str       # 'tree-(smell-water)'
    lexical_gloss: str             # 'spices'
    head_position: str             # 'left' or 'right'

# Atomic morpheme meanings
ATOMIC_GLOSSES = {
    'sing': 'tree', 'nam': 'smell', 'tui': 'water',
    'lung': 'heart', 'dam': 'healthy', 'kham': 'afraid',
    # ... 80+ entries
}

# Known binary compounds
BINARY_COMPOUNDS = {
    'namtui': ('nam-tui', 'smell-water', 'perfume'),
    'lungdam': ('lung-dam', 'heart-healthy', 'joy'),
    # ... 55+ entries
}

# Known ternary compounds with constituency
TERNARY_COMPOUNDS = {
    'singnamtui': ('sing', 'namtui', 'right', 'spices'),  # sing + (namtui)
    'lungdamte': ('lungdam', 'te', 'left', 'joyful.ones'),  # (lungdam) + te
    # ... 70+ entries
}
```

### Key Insight: Constituency Matters

- `sing-nam-tui` = `sing + (nam-tui)` = tree + perfume (right-headed)
- `lung-dam-te` = `(lung-dam) + te` = joy + PL (left-headed)

The system must know WHERE the primary break is.

### Position-Aware Disambiguation

Some morphemes have different meanings depending on position:

```python
AMBIGUOUS_ATOMIC = {
    'te': {
        'default': 'small',
        'as_suffix': 'PL',        # lungdamte = joyful.ones (PL)
        'as_modifier': 'small',   # tepa = small.person
    },
    'pi': {
        'default': 'big',
        'as_suffix': 'AUG',
    },
}
```

### Applicability to Other Languages

This pattern is common across Tibeto-Burman:
- **Mizo (lus)**: Similar compounding with transparent semantics
- **Hakha (cnh)**: Related morpheme inventory
- **Falam (cfm)**: Cognate compounds

The ATOMIC_GLOSSES will need language-specific entries, but the architecture transfers.

---

## 9. Development Workflow Recommendations

### Phase 1: Corpus Preparation (Do First!)
1. Run preprocessing script
2. Generate metadata.json
3. Validate format
4. Calculate baseline statistics (token count, unique words)

### Phase 2: High-Frequency Foundation
1. Extract top 500 word forms
2. Add function words (pronouns, demonstratives, conjunctions)
3. Add top 100 verbs (both Stem I and II)
4. Target: 70% coverage

### Phase 3: Morphological Rules
1. Add prefix rules (sorted by length, longest first)
2. Add suffix rules
3. Add reduplication patterns
4. Handle ki-/reflexive forms
5. Target: 90% coverage

### Phase 4: Compound Dictionary
1. Build COMPOUND_WORDS dictionary for known compounds
2. Add hierarchical analysis for complex compounds
3. Add proper noun list
4. Target: 97% coverage

### Phase 5: Long Tail
1. KJV cross-reference for unknown vocabulary
2. Handle Unicode edge cases
3. Document but don't exhaustively chase hapax
4. Target: 99%+ coverage

### Testing Discipline
- Test coverage after every 10-20 additions
- Never merge changes that decrease coverage (unless intentional)
- Keep git commits small and well-documented
- Sample-check accuracy, not just coverage

---

## 10. Top 15 Rules for Future Languages

1. **PREPROCESS FIRST** - Extract metadata, clean artifacts before any analysis
2. **Function words first** - They cover 60% of tokens
3. **Compound dictionary before decomposition rules**
4. **Always add both Stem I and Stem II for verbs**
5. **Sort prefixes/suffixes by length (longest first)**
6. **Handle Unicode apostrophes (U+2019)**
7. **Test after every 10-20 additions**
8. **Cross-reference with KJV for unknown vocabulary**
9. **Document, don't normalize, spelling variation**
10. **Accept 97% as "excellent" - don't chase 100%**
11. **Keep detailed logs of what was added and why**
12. **Implement hierarchical compound analysis for complex morphology**
13. **Use position-aware disambiguation for ambiguous morphemes**
14. **Separate metadata from text in structured JSON**
15. **Archive raw scrapes; work from cleaned versions**

---

*Document version: 2.0*  
*Last updated: 2026-03-13*
*Languages covered: Tedim Chin (ctd) - methodology applicable to 18+ Kuki-Chin languages*
