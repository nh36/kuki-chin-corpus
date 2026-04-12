# Generalization Notes: Tedim-Specific Assumptions

This document identifies Tedim Chin-specific assumptions in the current
backend implementation that will need modification before scaling to
other Kuki-Chin languages.

## Current State

The shared backend was built using Tedim Chin (ctd) as the pilot language.
Tedim has:
- A complete morphological analyzer (100% coverage, ~11,500 lines)
- Full Bible corpus (~831,000 tokens)
- Rich inflectional and derivational morphology
- Well-documented in Henderson 1965

Other Kuki-Chin languages in the repo (Mizo, Falam, Hakha, etc.) have:
- Bootstrap lexicons from PMI alignment
- Partial analyzers (70-85% coverage)
- Less complete grammatical documentation

---

## Tedim-Specific Assumptions

### 1. Form I / Form II Verb Alternation

**Assumption**: Verbs have two stems (indicative vs. subjunctive) that differ
by open/closed syllable shape.

```
Form I (open): mu, nei, za
Form II (closed): muh, neih, zak
```

**Backend impact**: The `senses` table currently doesn't distinguish Form I/II.
The analyzer handles this, but the backend treats them as the same lemma.

**Generalization needed**:
- Some KC languages (Mizo) have similar alternations
- Others (Falam, Hakha) may have different patterns
- Need `stem_form` field in wordforms with values like `form_i`, `form_ii`, `invariant`

### 2. Pronominal Prefix Paradigm

**Assumption**: Subject agreement prefixes are `ka- na- a- i-` (1SG, 2SG, 3SG, 1PL.INCL).

**Backend impact**: The `grammatical_morphemes` table has these as fixed entries.

**Generalization needed**:
- Other KC languages have different paradigms (some mark object, some don't)
- Mizo has `ka- i- a-` but different plural markers
- Need language-specific prefix inventories, not a single shared table

### 3. Case Marker Inventory

**Assumption**: Case markers include `in` (ERG), `ah` (LOC), `pan` (ABL), etc.

**Backend impact**: These are hard-coded in category `case_marker`.

**Generalization needed**:
- Case inventories vary across KC languages
- Some languages have additional cases or different forms
- Need language-parameterized case marker lists

### 4. TAM Suffix Set

**Assumption**: TAM suffixes like `ding` (IRR), `ta` (PFV), `zo` (COMPL) are universal.

**Backend impact**: These are tagged in `grammatical_morphemes` with category `tam_suffix`.

**Generalization needed**:
- TAM systems differ significantly across KC
- Some languages have tense marking, others are primarily aspect-based
- Need per-language TAM inventories with language-specific glosses

### 5. Sentence-Final Particles

**Assumption**: `hi` marks declarative, `hiam` marks questions, etc.

**Backend impact**: These are in `sentence_final` category.

**Generalization needed**:
- Different languages have different SFP inventories
- Mizo uses `a ni`, Hakha uses different forms
- Need language-specific SFP entries

### 6. Compound Structure

**Assumption**: Tedim compounds follow `N-N`, `V-V`, `N-V` patterns with
specific combinatorics (e.g., `ki-` reflexive prefix).

**Backend impact**: The compounds are handled in analyzer, not backend.

**Generalization needed**:
- Compound patterns vary by language
- Need `compound_patterns` table linking to language

### 7. Orthographic Conventions

**Assumption**: Tedim uses `kh`, `th`, `ph`, `ng` digraphs for aspirates/velars.

**Backend impact**: Phonotactic validation uses Tedim consonant inventory.

**Generalization needed**:
- Different KC languages have different orthographies
- Some use different digraphs or additional characters
- Need per-language orthographic rules

### 8. KJV Alignment

**Assumption**: English translations come from KJV alignment via `verses_aligned.tsv`.

**Backend impact**: `sources.kjv_text` stores the aligned English.

**Generalization needed**:
- This works for all KC languages with Bible data
- Non-Bible corpora won't have this field
- Should rename to `translation_text` with `translation_language` field

---

## Schema Changes for Generalization

### Add `language` FK to All Tables

Currently implicit (database per language). For cross-language queries:

```sql
ALTER TABLE grammatical_morphemes ADD COLUMN iso TEXT;
ALTER TABLE constructions ADD COLUMN iso TEXT;
```

Or keep separate databases but add cross-database query support.

### Add Language-Specific Parameters Table

```sql
CREATE TABLE language_params (
    iso TEXT,
    param_key TEXT,
    param_value TEXT,
    PRIMARY KEY (iso, param_key)
);

-- Examples:
INSERT INTO language_params VALUES
    ('ctd', 'has_form_i_ii', 'true'),
    ('ctd', 'case_markers', 'in,ah,pan,sung,tung,nuai'),
    ('lus', 'has_form_i_ii', 'true'),
    ('lus', 'case_markers', 'in,ah,atangin');
```

### Add Morpheme Equivalence Table

For cross-language comparison:

```sql
CREATE TABLE morpheme_equivalences (
    concept_id TEXT,  -- e.g., 'ergative_case'
    iso TEXT,
    form TEXT,
    gloss TEXT,
    PRIMARY KEY (concept_id, iso)
);

-- Examples:
INSERT INTO morpheme_equivalences VALUES
    ('ergative_case', 'ctd', 'in', 'ERG'),
    ('ergative_case', 'lus', 'in', 'ERG'),
    ('perfective', 'ctd', 'ta', 'PFV'),
    ('perfective', 'lus', 'ta', 'PFV');
```

---

## Implementation Priority

### Phase 1: Single-Language Backend (Current)
- ✅ Tedim backend working
- ✅ Dictionary lookup from backend
- ✅ Grammar report from backend

### Phase 2: Multi-Language Schema
1. Add `iso` column to all entity tables
2. Add `language_params` table
3. Migrate Mizo (lus) data as second language

### Phase 3: Cross-Language Features
1. Add `morpheme_equivalences` table
2. Build comparative grammar report generator
3. Add cognate detection for cross-KC vocabulary

### Phase 4: Non-Bible Corpora
1. Abstract `sources` table to support non-verse texts
2. Add generic sentence/paragraph segmentation
3. Support other translation languages beyond KJV

---

## Testing Generalization

Before adding a new language, verify:

1. **Analyzer coverage** ≥ 80% tokens
2. **Prefix inventory** documented
3. **Case markers** identified
4. **TAM suffixes** identified
5. **Form I/II** behavior (if applicable)
6. **SFP inventory** documented

Migration checklist for new language:

```bash
# 1. Export analysis to TSV
python scripts/export_{lang}_analysis.py

# 2. Migrate to backend
python scripts/backend.py migrate --tsv-dir data/{lang}_analysis --db data/{lang}_backend.db --iso {lang}

# 3. Verify lookup
python scripts/lookup_word.py {lang} <common_word>

# 4. Generate test report
python scripts/generate_tam_report_backend.py --db data/{lang}_backend.db
```

---

## Known Cross-KC Patterns

These features appear across multiple KC languages and can be generalized:

| Feature | Tedim | Mizo | Falam | Hakha |
|---------|-------|------|-------|-------|
| Ergative `in` | ✓ | ✓ | ✓ | ✓ |
| Perfective `ta` | ✓ | ✓ | ? | ? |
| Reflexive `ki-` | ✓ | ✓ | ✓ | ✓ |
| Form I/II | ✓ | ✓ | ? | ? |
| SFP declarative | `hi` | `a ni` | ? | ? |

These can eventually be modeled as shared constructions with language-specific
realizations.

---

## Summary

The current backend is functional for Tedim and provides a solid foundation.
Scaling to other KC languages requires:

1. **Schema additions**: `iso` columns, `language_params`, `morpheme_equivalences`
2. **Code changes**: Language-parameterized functions instead of Tedim-specific constants
3. **Documentation**: Per-language grammatical inventories
4. **Testing**: Verify reports generate correctly for each new language

The architecture is sound; generalization is primarily a matter of adding
language parameters and avoiding hard-coded Tedim assumptions.
