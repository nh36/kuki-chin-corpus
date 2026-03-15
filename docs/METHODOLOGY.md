# Kuki-Chin Morphological Analyzer Methodology

## Overview

This document describes the methodology developed for building a morphological analyzer for Tedim Chin (ctd), designed to be replicated across 19 Kuki-Chin languages. The goal is Leipzig-style glossing with 95%+ token coverage.

**Reference Implementation:** `scripts/analyze_morphemes.py` (Tedim Chin)  
**Coverage Achieved:** 99.9998% (832,202 of 832,204 tokens)  
**Development Time:** ~15 sessions of iterative work + quality audit

---

## 1. Data Requirements

### 1.1 Bible Corpus (Essential)
- Full Bible text (OT+NT) in target language
- Verse-aligned with KJV English for philological cross-referencing
- Format: `verse_id<TAB>text` (one verse per line)
- Expected size: ~30,000 verses, ~800,000 tokens

### 1.2 Secondary Literature (Helpful)
- Reference grammar (especially Henderson 1965 for Tedim)
- Dictionaries and wordlists
- Linguistic sketches
- Previous glossed texts if available

### 1.3 Parallel English (Essential)
- KJV English Bible aligned by verse
- Used to infer meanings of unknown words philologically

---

## 2. Analyzer Architecture

The analyzer follows a **priority-based lookup** strategy:

```
1. FUNCTION_WORDS    → Check closed-class words first
2. COMPOUND_WORDS    → Check compound dictionary (prevents over-decomposition)  
3. PROPER_NOUNS      → Check biblical names
4. NOUN_STEMS        → Check noun vocabulary
5. VERB_STEMS        → Check verb vocabulary
6. MORPHOLOGICAL     → Attempt prefix/suffix stripping
```

### 2.1 Dictionary Structure

```python
# Function words (closed class) - ~100-150 entries
FUNCTION_WORDS = {
    'le': 'and',           # conjunction
    'hi': 'DECL',          # declarative particle
    'ka': '1SG',           # pronominal prefix
    ...
}

# Compound words (pre-analyzed) - ~400-800 entries
COMPOUND_WORDS = {
    'biakinn': ('biak-inn', 'pray-house'),       # temple
    'lungsim': ('lung-sim', 'heart-mind'),       # inner being
    ...
}

# Verb stems (with Stem I/II alternation) - ~200-300 entries
VERB_STEMS = {
    'mu': 'see',           # Stem I (before vowel)
    'muh': 'see',          # Stem II (before consonant/pause)
    ...
}

# Noun stems - ~200-300 entries
NOUN_STEMS = {
    'inn': 'house',
    'mi': 'person',
    ...
}
```

### 2.2 Morphological Rules

After dictionary lookup fails, attempt rule-based decomposition:

```python
PREFIXES = ['ka-', 'na-', 'a-', 'kong-', 'hong-', 'ki-', ...]
SUFFIXES = ['-te', '-in', '-ah', '-na', '-sak', '-ding', '-zo', ...]

# Prefix stripping
for prefix in PREFIXES:
    if word.startswith(prefix):
        remainder = word[len(prefix):]
        if remainder in STEMS:
            return f"{prefix}{remainder}", f"{PREFIXES[prefix]}-{STEMS[remainder]}"

# Suffix stripping
for suffix in SUFFIXES:
    if word.endswith(suffix):
        stem = word[:-len(suffix)]
        if stem in STEMS:
            return f"{stem}-{suffix}", f"{STEMS[stem]}-{SUFFIXES[suffix]}"
```

### 2.3 Special Handling

#### Reduplication
```python
# Detect X~X patterns
if len(word) >= 4 and word[:len(word)//2] == word[len(word)//2:]:
    base = word[:len(word)//2]
    return f"{base}~RED", f"{analyze(base)[1]}~INTNS"
```

#### Apostrophe/Possessive
```python
# Handle U+2019 RIGHT SINGLE QUOTATION MARK as possessive
if word.endswith('\u2019') or word.endswith("'"):
    stem = word[:-1]
    return f"{stem}'", f"{analyze(stem)[1]}.POSS"
```

#### Stem I/II Alternation
Many Kuki-Chin verbs have two forms:
- **Stem I:** Used before vowel-initial suffixes or in certain grammatical contexts
- **Stem II:** Used before consonant-initial suffixes or clause-finally

```python
# Example: mu/muh (see), nei/neih (have), za/zak (fear)
VERB_STEMS = {
    'mu': 'see',      # Stem I
    'muh': 'see',     # Stem II
    ...
}
```

---

## 3. Development Workflow

### Phase 1: Bootstrap (Days 1-2)

1. **Load corpus and tokenize**
   ```python
   tokens = []
   for line in corpus:
       verse_id, text = line.split('\t', 1)
       tokens.extend(text.split())
   ```

2. **Build frequency distribution**
   ```python
   from collections import Counter
   freq = Counter(tokens)
   # Most common 100 words are usually function words
   ```

3. **Seed dictionaries with high-frequency items**
   - Top 100 words: manually classify as function words, nouns, verbs
   - Use parallel English to determine meanings

4. **Implement basic prefix/suffix stripping**
   - Start with most productive affixes
   - Tedim: ka-, na-, a-, -te, -in, -ah

### Phase 2: Iterative Expansion (Days 3-5)

This is the core work phase. Follow this cycle:

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  ① Run coverage test                            │
│  ② Identify top 20 unknown words                │
│  ③ For each unknown:                            │
│     a. Find all Bible verses where it occurs    │
│     b. Cross-reference with KJV English         │
│     c. Infer meaning from context               │
│     d. Analyze morphological structure          │
│     e. Add to appropriate dictionary            │
│  ④ Repeat until <3% unknown                     │
│                                                  │
└──────────────────────────────────────────────────┘
```

#### Example: Philological Analysis

```
Unknown word: "ihmut" (appears 28x)

Step 1: Find verses
$ grep "ihmut" bibles/extracted/ctd/ctd-x-bible.txt
GEN.2.21: ... ihmut sa mahmahtak ah ...
GEN.15.12: ... ni a tum dawnin ihmut sa a tun ...

Step 2: Cross-reference with KJV
GEN.2.21 (KJV): "And the LORD God caused a deep sleep to fall..."
GEN.15.12 (KJV): "...a deep sleep fell upon Abram..."

Step 3: Infer meaning
"ihmut" = "deep sleep" (always occurs in "deep sleep" contexts)

Step 4: Analyze structure
ih- = "sleep" prefix? mut = "deep"? 
Or: compound noun "sleep.deep"

Step 5: Add to dictionary
COMPOUND_WORDS['ihmut'] = ('ihmut', 'deep.sleep')
```

### Phase 3: Edge Cases (Days 6-7)

Address remaining problematic items:
- **Rare vocabulary**: Hapax legomena, archaic terms
- **Proper nouns**: Biblical names with suffixes
- **Loan words**: Modern vocabulary (identified by phonology)
- **Dialectal forms**: Variant spellings

### Phase 4: Validation

1. **Coverage check**: Must exceed 95%
2. **Accuracy audit**: Sample 100 random analyzed tokens, verify correctness
3. **Bug hunting**: Look for over-analysis (e.g., "sim" being split as "si-m")

---

## 4. Common Pitfalls & Solutions

### 4.1 Over-Decomposition

**Problem:** Short stems match parts of longer words
```
"sim" → incorrectly analyzed as "si-m" (be-?)
```

**Solution:** Add compounds to COMPOUND_WORDS first (checked before decomposition)
```python
COMPOUND_WORDS['sim'] = ('sim', 'read')  # Prevents si- prefix stripping
```

### 4.2 Stem I/II Confusion

**Problem:** Same verb appears with different final consonant
```
"nei" vs "neih" (have)
"mu" vs "muh" (see)
```

**Solution:** Add both forms to VERB_STEMS
```python
VERB_STEMS = {
    'nei': 'have',   # Stem I
    'neih': 'have',  # Stem II
    ...
}
```

### 4.3 Apostrophe Encoding

**Problem:** Possessive marker uses U+2019 (RIGHT SINGLE QUOTATION MARK), not ASCII apostrophe
```
"Topa'" (Lord's) uses U+2019, not U+0027
```

**Solution:** Handle both in code
```python
if word.endswith('\u2019') or word.endswith("'"):
    # possessive handling
```

### 4.4 Case Sensitivity

**Problem:** Sentence-initial capitalization
```
"Tua" (that, sentence-initial) vs "tua" (that)
```

**Solution:** Try lowercase if initial lookup fails
```python
if word not in DICTIONARY:
    word = word.lower()
    if word in DICTIONARY:
        # use lowercase match
```

### 4.5 Hyphenated Compounds

**Problem:** Some compounds written with hyphen, some without
```
"ka-ut" vs "kaut" (my son)
```

**Solution:** Check both forms, prefer hyphenated if present
```python
if '-' in word:
    parts = word.split('-')
    # analyze each part separately
```

### 4.6 Diminishing Returns

**Problem:** Below 1% unknown, effort per token increases dramatically

**Solution:** 
- Accept 95-97% as "good enough" for most purposes
- Document remaining unknowns for later lexical work
- Focus on patterns, not individual items

---

### 5.1 Dictionary Size Guidelines

Based on Tedim experience, expect approximately:

| Category | Entries | Coverage Contribution |
|----------|---------|----------------------|
| Function words | 100-150 | ~60% |
| Verb stems | 2,000+ | ~15% |
| Noun stems | 800+ | ~10% |
| Compound words (simple) | 500-1,000 | ~8% |
| Hierarchical compounds | 300-600 | ~3% |
| Proper nouns | 2,500+ | ~2% |
| Atomic glosses | 300+ | (compositional) |
| **Total** | **~7,000+** | **~99%** |

---

## 6. Quality Metrics

### 6.1 Coverage Tiers

| Tier | Coverage | Status |
|------|----------|--------|
| 🟢 Excellent | ≥99% | Production-ready Leipzig glossing |
| 🟢 Very Good | 97-99% | Full Leipzig glossing ready |
| 🟡 Good | 93-97% | Usable with some gaps |
| 🟠 Developing | 85-93% | Significant work needed |
| 🔴 Initial | <85% | Early stage |

### 6.2 Accuracy Audit

Sample 100 random fully-analyzed tokens:
- **True positive**: Correct segmentation AND gloss (target: ≥95)
- **False positive**: Wrong segmentation OR gloss (target: ≤5)

Common false positive types:
- Over-decomposition (e.g., "simna" → "si-m-na" instead of "sim-na")
- Wrong homophone (e.g., "a" = 3SG vs LOC)
- Missing compound (decomposed when should be unit)

---

## 7. Scaling to New Languages

### Pre-work Checklist

- [ ] Bible corpus extracted and cleaned
- [ ] Verse alignment with KJV verified
- [ ] Reference grammar located (if available)
- [ ] Word frequency list generated
- [ ] Language-specific orthographic conventions noted

### Adaptation Required

1. **Prefix/suffix inventories**: Vary by language
2. **Stem alternation patterns**: May differ from Tedim
3. **Orthographic conventions**: Apostrophe usage, hyphenation, capitalization
4. **Function word inventory**: Core items similar but not identical

### Estimated Timeline Per Language

| Phase | Duration | Coverage |
|-------|----------|----------|
| Bootstrap | 1-2 days | 60-70% |
| Iterative expansion | 3-5 days | 85-95% |
| Edge cases | 1-2 days | 95-97% |
| Push to 99%+ | 2-3 days | 99%+ |
| Quality audit | 1-2 days | (verification) |
| **Total** | **8-14 days** | **99%+ verified** |

---

## 8. Post-Coverage Quality Audit (NEW)

**Critical Discovery:** Coverage ≠ Correctness. After achieving 99%+ coverage, systematic verification revealed:
- Duplicate entries with conflicting glosses
- Wrong segmentations (guessed morpheme boundaries)
- Wrong glosses (no KJV verification)
- Transparent derivations misclassified as opaque

### Audit Programme (5 Phases)

**Phase 1: Structural Integrity**
- Find duplicate entries (same word, 2+ different glosses)
- Find conflicting segmentations
- Complete all partial glosses (entries with `?`)

**Phase 2: Semantic Verification**
- Verify each root against 3+ corpus examples via KJV
- Check if "opaque" entries are actually transparent
- Normalize terminology (e.g., "stone" not "rock" for `suang`)

**Phase 3: Disambiguation**
- Inventory all homophonous roots
- Verify disambiguation rules exist in POLYSEMOUS_ROOTS
- Add explicit compound entries for context-dependent meanings

**Phase 4: Cross-Validation**
- Test BINARY/TERNARY_COMPOUNDS produce expected outputs
- Run regression tests after each fix batch

**Phase 5: Documentation**
- Document error patterns found
- Update LESSONS_LEARNED.md
- Create verification checklist for new entries

### New Entry Verification Checklist

Before adding ANY vocabulary entry:
- [ ] KJV verification (3+ occurrences)
- [ ] Segmentation uses only known morphemes
- [ ] No duplicate entries exist (grep first)
- [ ] Consistent with existing glosses
- [ ] Homophones documented in POLYSEMOUS_ROOTS

See `docs/LESSONS_LEARNED.md` Section 11 for detailed audit methodology.

---

## 8. File Outputs

### 8.1 Analyzer Script
```
scripts/analyze_morphemes.py       # Main analyzer
scripts/analyze_morphemes_{ISO}.py # Language-specific (future)
```

### 8.2 Documentation
```
docs/METHODOLOGY.md                # This document
docs/{ISO}_MORPHEME_INVENTORY.md   # Per-language morpheme documentation
```

### 8.3 Analysis Outputs
```
analysis/{ISO}_coverage_report.txt  # Coverage statistics
analysis/{ISO}_unknown_words.tsv    # Remaining unknowns for manual review
```

---

## 9. Lessons Learned

### What Worked Well

1. **Philological cross-referencing with KJV** - Most effective for unknown vocabulary
2. **Frequency-based prioritization** - High-frequency items yield most coverage gain
3. **Compound dictionary before decomposition** - Prevents over-analysis
4. **Iterative small commits** - Easy to identify when bugs were introduced

### What Didn't Work

1. **Aggressive normalization early** - Risk of conflating distinct forms
2. **Relying solely on dictionaries** - Need productive rules too
3. **Ignoring case/punctuation** - These encode real information
4. **Batch additions without testing** - Bugs compound quickly

### Recommendations for Future Languages

1. Start with function words (highest frequency, closed class)
2. Build compound dictionary aggressively before decomposition rules
3. Document Stem I/II patterns early
4. Keep parallel KJV always accessible
5. Test coverage after every 20-30 additions
6. Don't chase 100% - 97% is excellent

---

*Document version: 3.0*  
*Last updated: 2026-03-15*  
*Based on: Tedim Chin (ctd) analyzer development + quality audit*
