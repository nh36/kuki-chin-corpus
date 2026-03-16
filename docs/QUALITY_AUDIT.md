# Morphological Analyzer Quality Audit Programme

## Overview

This document describes the systematic quality audit process developed after achieving 99%+ coverage on Tedim Chin. The audit revealed that **coverage ≠ correctness** - rapid vocabulary expansion introduced systematic errors that must be identified and corrected before the methodology is applied to other languages.

**Status:** In Progress  
**Language:** Tedim Chin (ctd)  
**Coverage:** 99.9998% (832,202/832,204 tokens)  
**Audit Start:** 2026-03-15

---

## Problem Statement

During rapid vocabulary expansion (230 rounds of additions), errors accumulated:

| Error Type | Example | Frequency |
|------------|---------|-----------|
| Wrong segmentation | `sinso` → `sin-so` (no "sin=die" root) | Common |
| Wrong gloss | `sinso` = "die-remain" (should be "be.angry") | Common |
| Duplicate entries | 3x `sinsona` with different glosses | Moderate |
| Inconsistent terminology | `suang` = "rock" vs "stone" | Moderate |
| Missed transparency | `sinsona` as opaque (actually `sinso-na`) | Common |
| Missing disambiguation | `lamna` = build/dance (needs context) | Occasional |

These errors will propagate to 19 other Kuki-Chin Bible analyses if not corrected.

---

## Audit Phases

### Phase 1: Structural Integrity Checks

#### 1.1 Duplicate Entry Detection
**Goal:** Find all words appearing 2+ times in COMPOUND_WORDS with different glosses.

**Method:**
```python
from collections import defaultdict
entries = defaultdict(list)
for line_num, (word, (seg, gloss)) in enumerate(COMPOUND_WORDS.items()):
    entries[word].append((line_num, seg, gloss))
duplicates = {w: e for w, e in entries.items() if len(e) > 1}
```

**Resolution:** For each duplicate:
1. Check KJV for actual meaning(s)
2. If same meaning: remove duplicates, keep canonical entry
3. If different meanings: add disambiguation rules

**Status:** ⬜ Not started

#### 1.2 Conflicting Segmentations
**Goal:** Find entries where same word has different segmentation.

**Example Found:**
- `sinsona` at line 8366: `sin-son-a` (die-remain-LOC)
- `sinsona` at line 15277: `sinsona` (wrath - opaque)
- Correct: `sinso-na` (be.angry-NMLZ)

**Status:** ⬜ Not started

#### 1.3 Partial Gloss Completion
**Goal:** Resolve all entries containing `?` in gloss.

**Method:**
```bash
grep "'?'" scripts/analyze_morphemes.py | wc -l
```

**Status:** ⬜ Not started

---

### Phase 2: Semantic Verification

#### 2.1 Root Meaning Verification
**Goal:** Verify each root in ROOTS against 3+ corpus examples.

**Priority:** Start with high-frequency roots (>100 occurrences).

**Method:**
```bash
# For each root:
grep "\broot\b" bibles/extracted/ctd/ctd-x-bible.txt | head -5
# Cross-reference with KJV
```

**Status:** ⬜ Not started

#### 2.2 Opacity Audit
**Goal:** Check if "opaque" lexemes are actually transparent derivations.

**Pattern to check:** `XYZna` where `XYZ` might be a verb/adjective + `-na` (NMLZ)

**Example Fixed:**
- `sinsona` was glossed as opaque "wrath"
- Investigation found `sinso` = "be.angry" (verb, 16x in corpus)
- Correct: `sinsona` = `sinso-na` = "be.angry-NMLZ"

**Status:** 🔄 In progress (1 fixed, ~500 to check)

#### 2.3 Gloss Consistency
**Goal:** Normalize terminology across all entries.

**Issues Found:**
- `suang` glossed as both "rock" and "stone" → normalize to "stone"
- Various suffix inconsistencies

**Status:** 🔄 In progress

---

### Phase 3: Disambiguation Completeness

#### 3.1 Homophonous Root Inventory
**Goal:** List all roots with 2+ distinct meanings.

**Found So Far:**
| Root | Meaning 1 | Meaning 2 | Meaning 3 | Status |
|------|-----------|-----------|-----------|--------|
| lam | way/path | build | dance | ✅ Disambiguated |
| sin | near | - | - | ✅ Verified (not "die" or "trust") |
| keen | crag/cliff | - | - | ✅ Fixed |
| sinso | be.angry | - | - | ✅ Fixed |

**Status:** 🔄 In progress

#### 3.2 Context-Dependent Analysis
**Goal:** Identify words requiring multi-word compound entries for disambiguation.

**Pattern:** When meaning depends on surrounding words, add explicit entries.

**Example:**
```python
# lamna defaults to 'build-NMLZ' (more common)
'lamna': ('lam-na', 'build-NMLZ'),

# Dance contexts via explicit multi-word compounds:
'le lamna': ('le lam-na', 'and dance-NMLZ'),        # Ex 32:19
'taunate lamna': ('tauna-te lam-na', 'mourn-PL dance-NMLZ'),  # Ps 30:11
```

**Status:** ✅ Implemented for `lamna`

---

### Phase 4: Cross-Validation

#### 4.1 Algorithmic Consistency
**Goal:** Verify BINARY/TERNARY_COMPOUNDS produce expected outputs.

**Status:** ⬜ Not started

#### 4.2 Regression Testing
**Goal:** After each fix batch, verify coverage ≥99.99%.

**Current:** 99.9998% (2 partials: numbers 144, 000)

**Status:** ✅ Ongoing

---

### Phase 5: Documentation

#### 5.1 Error Pattern Documentation
**Goal:** Categorize all errors found with frequencies and root causes.

**Status:** 🔄 In progress (this document)

#### 5.2 Methodology Improvements
**Goal:** Update workflow to prevent error recurrence.

**Added:**
- Verification checklist for new entries
- KJV cross-reference requirement
- Etymology check before addition

**Status:** ✅ Done (LESSONS_LEARNED.md updated)

#### 5.3 Replication Guide
**Goal:** Write guide for applying audit to 19 other Bibles.

**Status:** ⬜ Not started

---

## Verification Checklist for New Entries

Before adding ANY vocabulary entry:

- [ ] **KJV verification**: Check 3+ occurrences against English translation
- [ ] **Segmentation validation**: Every morpheme exists in ROOTS/STEMS
- [ ] **Consistency check**: Same morpheme = same gloss everywhere
- [ ] **Homophone check**: If multiple meanings, add to POLYSEMOUS_ROOTS
- [ ] **Transparency check**: For `XYZna`, verify base `XYZ` exists first
- [ ] **Duplicate check**: `grep` for existing entries before adding
- [ ] **Phonotactic check**: No illegal onset clusters (see below)

---

## Phonotactic Constraints

Tedim Chin has strict phonotactic constraints that prohibit certain consonant clusters at morpheme onset. Any segmentation that creates such clusters is WRONG.

### Illegal Onset Clusters

```python
ILLEGAL_ONSETS = {
    # Stop + Stop
    'pt', 'pk', 'tp', 'tk', 'kp', 'kt',
    # Stop + Fricative
    'ps', 'ts', 'ks', 'bs', 'ds', 'gs',
    # Nasal/Liquid/Continuant + Stop
    'mp', 'mt', 'mk', 'np', 'nt', 'nk',
    'lp', 'lt', 'lk', 'rp', 'rt', 'rk',
    # Fricative/Continuant + Stop
    'zp', 'zt', 'zk', 'vp', 'vt', 'vk',
    'hp', 'ht', 'hk', 'hs',
    # Triple clusters
    'tph', 'kph', 'pph', 'pkh', 'tkh', 'skh'
}
```

### Examples of Violations Fixed

| Wrong | Correct | Rule |
|-------|---------|------|
| `ka-pkhia` | `kap-khia` | No `pk` cluster |
| `ki-psak-na` | `kip-sak-na` | No `ps` cluster |
| `na-ksiat` | `nak-siat` | No `ks` cluster |
| `ka-htoh-na` | `kah-toh-na` | No `ht` cluster |
| `ki-lkel` | `kil-kel` | No `lk` cluster |

### Phonotactic Audit Script

```python
import re

ILLEGAL_ONSETS = {'ps', 'pt', 'pk', 'ts', 'tp', 'tk', 'ks', 'kp', 'kt', 
                   'bs', 'bp', 'bk', 'ds', 'dp', 'dk', 'gs', 'gp', 'gt', 'gk',
                   'ms', 'mp', 'mt', 'mk', 'ns', 'np', 'nt', 'nk',
                   'ls', 'lp', 'lt', 'lk', 'rs', 'rp', 'rt', 'rk',
                   'zs', 'zp', 'zt', 'zk', 'vs', 'vp', 'vt', 'vk',
                   'hs', 'hp', 'ht', 'hk'}

def check_phonotactics(segmentation):
    """Check if segmentation violates phonotactic constraints."""
    morphemes = segmentation.replace("'", "").split('-')
    violations = []
    for m in morphemes:
        if len(m) >= 2 and m[:2].lower() in ILLEGAL_ONSETS:
            violations.append((m, m[:2]))
    return violations

# Run on all entries
with open('scripts/analyze_morphemes.py', 'r') as f:
    content = f.read()
pattern = r"'([^']+)':\s*\('([^']+)',\s*'([^']+)'\)"
for word, seg, gloss in re.findall(pattern, content):
    v = check_phonotactics(seg)
    if v:
        print(f"VIOLATION: {word}: {seg} = {gloss}")
        print(f"  Morphemes with illegal onsets: {v}")
```

---

## Audit Progress Tracking

| Phase | Task | Status | Notes |
|-------|------|--------|-------|
| 1.1 | Duplicate detection | ✅ | 583 duplicates found, 353 removed |
| 1.2 | Segmentation conflicts | ✅ | Phonotactic audit complete |
| 1.3 | Partial gloss completion | ✅ | 0 partials remaining |
| 1.4 | Phonotactic audit | ✅ | 15 violations fixed |
| 2.1 | Root verification | ⬜ | ~2,000 roots |
| 2.2 | Opacity audit | 🔄 | 1 fixed |
| 2.3 | Gloss consistency | 🔄 | suang normalized |
| 3.1 | Homophone inventory | 🔄 | 4 documented |
| 3.2 | Context-dependent | ✅ | lamna done |
| 4.1 | Algorithm testing | ⬜ | |
| 4.2 | Regression testing | ✅ | Ongoing |
| 5.1 | Error documentation | 🔄 | This document |
| 5.2 | Methodology update | ✅ | Done |
| 5.3 | Replication guide | ⬜ | |

---

## Commits During Audit

| Commit | Description |
|--------|-------------|
| `a6b9c28` | Normalize suang glosses, lamna ambiguity |
| `894c2a6` | Proper lamna disambiguation via compounds |
| `55b0457` | Fix sinsona', suangkeen glosses |
| `d1d7765` | Remove erroneous sinsona segmentations |
| `6622815` | Fix sinso/sinsona etymology |
| `bf1f73a` | Create systematic quality audit documentation |
| `6dff427` | Remove 327 duplicate/partial entries |
| `b4eabb6` | Resolve 26 problematic partial-vs-complete conflicts |
| `9efb103` | Create analysis files for 207 same-seg conflicts |
| `cc0e07a` | Fix phonotactic violations and 22 remaining partials |
| `1b9e09f` | Fix additional phonotactic violations (ht/lk clusters) |

---

## Current Coverage

**100.0000%** (852,286/852,286 tokens)
- Full analyses: 852,286
- Partial analyses: 0
- Unknown tokens: 0

---

*Document version: 1.1*  
*Created: 2026-03-15*  
*Last Updated: 2026-03-16*
*Maintainer: Kuki-Chin Corpus Project*
