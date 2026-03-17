# Kuki-Chin Morphological Analyzer: Replication Guide

Step-by-step instructions for building a morphological analyzer for a new
Kuki-Chin language, based on the Tedim Chin (ctd) reference implementation.

## Prerequisites

1. **Bible corpus** in target language
   - Full Bible preferred (OT+NT, ~30,000 verses)
   - Format: `verse_id<TAB>text` (one verse per line)
   - Located in `bibles/extracted/{ISO}/`

2. **English parallel** (KJV)
   - Verse-aligned for cross-referencing
   - Located in `data/verses_aligned.tsv`

3. **Reference grammar** (helpful but not required)
   - Prefix/suffix inventories
   - Stem alternation patterns
   - Orthographic conventions

## Phase 1: Bootstrap (Days 1-2)

### Step 1.1: Generate word frequency list

```bash
# Extract all words with frequencies
cut -f2 bibles/extracted/{ISO}/{ISO}-x-bible.txt | \
  tr ' ' '\n' | sort | uniq -c | sort -rn > temp_wordfreq.txt

# Top 100 words are mostly function words
head -100 temp_wordfreq.txt
```

### Step 1.2: Seed FUNCTION_WORDS (~60% coverage)

Manually classify top 100 words:
- Pronouns: ka, na, a, i, ei (1SG, 2SG, 3SG, 1PL.INCL, 1PL.EXCL)
- Demonstratives: hih, tua, kha (this, that, that.DIST)
- Particles: hi, leh, le, pen (DECL, if, and, TOP)
- TAM markers: ding, zo, ta, khin (IRR, COMPL, PFV, IMM)
- Negation: lo, kei (NEG)

```python
FUNCTION_WORDS = {
    'ka': '1SG',
    'na': '2SG',
    'a': '3SG',
    'hi': 'DECL',
    # ... ~100-150 entries
}
```

### Step 1.3: Basic prefix/suffix rules

Most Kuki-Chin languages share:

**Prefixes:**
- Pronominal: ka-, na-, a-, i-, ei-
- Object: kong-, hong-
- Reflexive: ki-

**Suffixes:**
- Case: -in (ERG), -ah (LOC), -te (PL)
- TAM: -ding (IRR), -zo (COMPL), -ta (PFV)
- Derivational: -na (NMLZ), -pa (NMLZ.AG), -sak (CAUS)

**Expected coverage after Phase 1:** 60-70%

---

## Phase 2: Iterative Expansion (Days 3-5)

### Step 2.1: Unknown word investigation cycle

```
┌────────────────────────────────────────────────┐
│  1. Run coverage test                          │
│  2. Get top 20 unknown words by frequency      │
│  3. For each word:                             │
│     a. Find Bible verses containing word       │
│     b. Look up KJV English for those verses    │
│     c. Infer meaning from English context      │
│     d. Analyze morphological structure         │
│     e. Add to appropriate dictionary           │
│  4. Test coverage again                        │
│  5. Repeat until <3% unknown                   │
└────────────────────────────────────────────────┘
```

### Step 2.2: Philological cross-reference method

```bash
# Find unknown word in corpus
word="ihmut"
grep -m3 ".*\b$word\b" bibles/extracted/{ISO}/{ISO}-x-bible.txt

# Get verse IDs
verse=$(grep -m1 ".*\b$word\b" bibles/extracted/{ISO}/{ISO}-x-bible.txt | cut -f1)

# Look up English
grep "^$verse" data/verses_aligned.tsv | cut -f3
```

### Step 2.3: Compound dictionary building

For words that shouldn't decompose (would give wrong meaning):

```python
COMPOUND_WORDS = {
    'biakinn': ('biak-inn', 'worship-house'),  # temple
    'lungdam': ('lung-dam', 'heart-well'),     # joy
    # Add when algorithmic decomposition would fail
}
```

**Expected coverage after Phase 2:** 90-95%

---

## Phase 3: Edge Cases (Days 6-7)

### Step 3.1: Proper nouns

Biblical names need special handling:
- Add to PROPER_NOUNS dictionary
- Handle suffixes on proper nouns: Mose-in, Zeisu-ah

```python
PROPER_NOUNS = {
    'Zeisu': 'JESUS',
    'Mose': 'MOSES',
    # ~2,500 entries for full Bible
}
```

### Step 3.2: Form I/II verb alternation

Many Kuki-Chin verbs have two stems:
- Form I: Before vowels, sentence-finally (indicative)
- Form II: Before consonants, in adjunctive phrases

```python
VERB_STEMS = {
    'mu': 'see',    # Form I
    'muh': 'see',   # Form II
    'nei': 'have',  # Form I  
    'neih': 'have', # Form II
}
```

### Step 3.3: Reduplication

Handle X~X patterns:
```python
# Detect reduplication
if len(word) >= 4:
    half = len(word) // 2
    if word[:half] == word[half:]:
        base = word[:half]
        return f"{base}~RED", f"{analyze(base)}-INTNS"
```

**Expected coverage after Phase 3:** 97-99%

---

## Phase 4: Quality Audit (Days 8-10)

### Step 4.1: Duplicate check

```bash
# Find duplicate entries
grep "'" scripts/analyze_morphemes.py | \
  cut -d"'" -f2 | sort | uniq -d
```

### Step 4.2: Semantic verification

Sample 100 random analyzed tokens:
1. Check segmentation is morphologically valid
2. Verify gloss against corpus usage
3. Fix errors found

### Step 4.3: Homophone documentation

For each root with multiple meanings:
1. Add to AMBIGUOUS_MORPHEMES
2. Document disambiguation context
3. Add regression test

### Step 4.4: Regression test suite

Create tests for all fixed bugs:

```python
tests = [
    ('ding', 'IRR'),          # Not 'stand'
    ('Sin', 'SIN'),           # Proper noun, not 'near'
    ('khuamial', 'darkness'), # Opaque, not 'town-dark'
]

for word, expected in tests:
    seg, gloss = analyze_word(word)
    assert expected in gloss, f"{word}: got {gloss}"
```

**Expected coverage after Phase 4:** 99%+

---

## Phase 5: Documentation

### Required documentation

1. **MORPHEME_INVENTORY.md** - All prefixes, suffixes, stems
2. **DISAMBIGUATION.md** - Homophone handling rules
3. **ERROR_PATTERNS.md** - Common mistakes and fixes
4. **regression_tests.md** - All test cases

---

## Estimated Timeline

| Phase | Duration | Coverage |
|-------|----------|----------|
| Bootstrap | 1-2 days | 60-70% |
| Expansion | 3-5 days | 90-95% |
| Edge cases | 1-2 days | 97-99% |
| Quality audit | 2-3 days | 99%+ |
| Documentation | 1-2 days | - |
| **Total** | **8-14 days** | **99%+ verified** |

---

## Language-Specific Adaptations

### Orthographic differences

| Feature | Tedim | Falam | Hakha |
|---------|-------|-------|-------|
| Apostrophe | ' (possessive) | ' | ' |
| Tone marking | None | None | Variable |
| NG spelling | ng | ng | ng |

### Morphological differences

Some Kuki-Chin languages may have:
- Different pronominal prefixes
- Additional TAM markers
- Different suffix orders
- Tone-conditioned allomorphy

**Always verify patterns against actual corpus data.**

---

## Reusable Components

From the Tedim analyzer:

1. **Architecture** - Priority-based lookup order
2. **Suffix stripping** - Recursive decomposition
3. **Reduplication detection** - X~X pattern matching
4. **Proper noun handling** - Case preservation + suffix
5. **Unicode normalization** - Apostrophe variants

Copy `scripts/analyze_morphemes.py` and replace:
- FUNCTION_WORDS
- VERB_STEMS, NOUN_STEMS
- COMPOUND_WORDS
- PROPER_NOUNS

Keep the analysis logic unchanged.

---

*Last updated: 2026-03-17*
*Based on: Tedim Chin analyzer (100% coverage, 850,906 tokens)*
