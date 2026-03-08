# Tedim Chin Analyzer: Lessons Learned & Bug Log

## Overview

This document captures specific issues encountered during the development of the Tedim Chin (ctd) morphological analyzer, including wrong turns, bugs discovered, and their solutions. This is intended as a reference for future language work.

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
| 98.5%+ | Hapax, dialectal forms, loans | Document but don't chase exhaustively |

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

---

*Document version: 1.0*  
*Last updated: 2026-03-07*
