# Tedim Chin Morphological Analyzer: Error Patterns

This document catalogs common error patterns discovered during analyzer development,
to help avoid similar issues when building analyzers for other Kuki-Chin languages.

## 1. Over-Segmentation Errors

### Pattern: Short stem matches part of longer word

**Example:**
```
"sim" incorrectly analyzed as "si-m" (be-?)
```

**Cause:** Greedy prefix/suffix stripping

**Solution:** Add explicit COMPOUND_WORDS entry to intercept:
```python
COMPOUND_WORDS['sim'] = ('sim', 'read')
```

**Prevention:** Check COMPOUND_WORDS before decomposition

### Pattern: Opaque compound mistaken for transparent

**Example:**
```
"lupna" wrongly → "lup-na" (bow-NMLZ)
Correct → "lupna" (bed) - opaque lexeme
```

**Cause:** Productive -na suffix matches coincidentally

**Solution:** Add to OPAQUE_LEXEMES with "would-be parse" documentation

**Frequency:** ~25 cases identified

---

## 2. Under-Segmentation Errors

### Pattern: Valid morpheme boundary not recognized

**Example:**
```
"nasepna" stuck as whole word
Correct → "nasep-na" (work-NMLZ)
```

**Cause:** Missing stem in VERB_STEMS

**Solution:** Add stem to appropriate dictionary

**Prevention:** Frequency-first vocabulary building

---

## 3. Gloss Inconsistency

### Pattern: Same morpheme glossed differently

**Example:**
```
"suang" glossed as both "stone" and "rock" in different compounds
```

**Cause:** Ad-hoc additions without checking existing glosses

**Solution:** Canonical gloss normalization audit

**Prevention:** 
1. Check existing glosses before adding new entry
2. Use `grep -r "suang" scripts/analyze_morphemes.py` first

---

## 4. Homophone Confusion

### Pattern: Wrong meaning selected for polysemous root

**Example:**
```
"kham" → "gold" (correct in most contexts)
But: "kikham" → should be "REFL-forbid", not "REFL-gold"
```

**Cause:** Missing context-based disambiguation

**Solution:** Add to AMBIGUOUS_MORPHEMES with context rules:
```python
'kham': [
    ('gold', 'standalone'),
    ('forbid', 'with_ki'),
]
```

**Prevention:** Document all homophones with ≥2 distinct meanings

---

## 5. Form I/II Confusion

### Pattern: Stem I and Stem II not both recognized

**Example:**
```
"mu" (see.I) recognized but "muh" (see.II) returns UNK
```

**Cause:** Only one form in dictionary

**Solution:** Add both forms:
```python
VERB_STEMS = {
    'mu': 'see',   # Form I
    'muh': 'see',  # Form II
}
```

**Prevention:** For each verb, check if both forms exist in corpus

---

## 6. Proper Noun Errors

### Pattern: Proper noun decomposed as common word

**Example:**
```
"Sin" (person name) → "sin" (near)
"Lot" (person name) → "lot" (cast lots)
```

**Cause:** Case-insensitive matching without proper noun check

**Solution:** 
1. Check PROPER_NOUNS before lowercase fallback
2. Preserve original case in output

**Prevention:** Proper noun dictionary checked early in pipeline

---

## 7. Ghost Entries

### Pattern: Meaning added that doesn't exist in corpus

**Example:**
```
"awk" given meaning "ram" (from English association?)
Actual corpus meaning: "trap/snare"
```

**Cause:** Inference without corpus verification

**Solution:** Remove ghost entries, verify all via KJV cross-reference

**Prevention:** Require 3+ corpus occurrences before adding meaning

---

## 8. Segmentation Boundary Errors

### Pattern: Morpheme boundary placed incorrectly

**Example:**
```
"tuucin" wrongly → "tuu-cin" (?)
Correct → "tuu-cin" (sheep-tend) = shepherd
But "tuu" alone is rare - could be "tuucin" opaque
```

**Cause:** Uncertain morpheme boundaries for rare words

**Solution:** Cross-reference with known compounds sharing same elements

---

## 9. Suffix Order Violations

### Pattern: Impossible suffix combinations analyzed

**Example:**
```
*"-na-sak" (NMLZ-CAUS) - impossible order
Correct: "-sak-na" (CAUS-NMLZ)
```

**Cause:** No suffix ordering validation

**Solution:** Implement suffix order checking:
```
DERIV (-sak, -pih, -kik) must precede INFL (-na, -te, -in)
```

---

## 10. Unicode/Encoding Issues

### Pattern: Apostrophe variants not handled

**Example:**
```
"Topa'" with U+2019 (RIGHT SINGLE QUOTATION MARK) not recognized
"Topa'" with U+0027 (APOSTROPHE) works
```

**Cause:** Input not normalized

**Solution:** Normalize input at entry:
```python
word = word.replace('\u2019', "'")  # Curly → straight
```

---

## Error Frequency Summary

| Error Type | Frequency | Impact | Fix Difficulty |
|------------|-----------|--------|----------------|
| Over-segmentation | High | Medium | Easy (add compound) |
| Under-segmentation | Medium | Low | Easy (add stem) |
| Gloss inconsistency | High | Low | Medium (audit) |
| Homophone confusion | Medium | High | Medium (add rules) |
| Form I/II confusion | Medium | Medium | Easy (add forms) |
| Proper noun errors | Low | Medium | Easy (check order) |
| Ghost entries | Low | High | Medium (verify) |
| Boundary errors | Low | High | Hard (research) |
| Suffix order | Rare | Medium | Medium (validate) |
| Unicode issues | Common | Low | Easy (normalize) |

---

## Quality Assurance Checklist

Before adding any entry:

- [ ] Verify meaning via KJV (3+ occurrences)
- [ ] Check for existing entries (`grep` first)
- [ ] Consistent with existing glosses
- [ ] Document homophones in AMBIGUOUS_MORPHEMES
- [ ] Add regression test for edge cases
- [ ] Check both Form I and Form II for verbs

---

*Last updated: 2026-03-17*
*Part of Phase 5: Error Documentation*
