# Tedim Chin Bible Analysis Export

This directory contains the full morphological analysis of the Tedim Chin Bible corpus, structured for dictionary and grammar work.

## Files

### Core Data Files

| File | Description | Rows |
|------|-------------|------|
| `verses.tsv` | Verse-level metadata with original text | ~30,000 |
| `tokens.tsv` | Token-level full analysis (one row per word) | ~831,000 |
| `wordforms.tsv` | Type-level aggregation (distinct word forms) | ~22,000 |
| `lemmas.tsv` | Lemma-level dictionary seed | ~8,000 |
| `grammatical_morphemes.tsv` | Grammatical morpheme inventory (keyed by form+gloss) | ~480 |
| `examples.tsv` | Curated examples bank with segmented/glossed forms | ~24,000 |
| `ambiguities.tsv` | Review queue for uncertain analyses | ~4,000 |
| `coverage_report.md` | Coverage statistics and summary | - |
| `sample_entries.md` | 100 sample dictionary entries | - |

### File Formats

All TSV files use tab-separated values with a header row.

#### verses.tsv
```
verse_id    book    chapter    verse    tedim_text    word_count    kjv_text
```

#### tokens.tsv
```
verse_id    token_index    surface_form    normalized_form    segmentation    gloss
lemma    pos    stem_form    stem_alternation    prefix_chain    suffix_chain
is_proper_noun    is_ambiguous    confidence    kjv_text
```

| Field | Description |
|-------|-------------|
| `segmentation` | Morpheme boundaries marked with hyphens |
| `gloss` | Leipzig-style morpheme-by-morpheme gloss |
| `lemma` | Citation form (Form I for verbs) |
| `pos` | Part of speech: V, N, FUNC, PROP, UNK |
| `stem_alternation` | 'I', 'II', or '' for verb stem form |
| `confidence` | 'high', 'medium', 'low', 'unknown' |

#### wordforms.tsv
```
surface_form    normalized_form    lemma    segmentation    gloss    pos
frequency    first_verse    sample_verses    is_ambiguous    status
```

#### lemmas.tsv
```
lemma    citation_form    pos    primary_gloss    english_glosses    all_glosses
inflected_forms    token_count    form_count    is_polysemous    needs_review
compounds    top_collocates    example_verses    polysemy_notes    grammaticalization_notes
```

| Field | Description |
|-------|-------------|
| `primary_gloss` | Best English gloss (from analyzer dictionaries) |
| `english_glosses` | All attested English translations |
| `all_glosses` | All glosses including grammatical tags |
| `is_polysemous` | 1 if known polysemous form |
| `needs_review` | 1 if flagged for manual review |

#### grammatical_morphemes.tsv
```
form    gloss    category    subcategory    frequency    environments
example_verses    ambiguity_notes    is_polysemous    review_reasons    status
```

The file is keyed by (form, gloss) pairs, so polysemous morphemes like `-na` 
have separate entries for each function (NMLZ vs 2SG).

Categories include:
- `case_marker` - Case markers (ERG, LOC, ABL, etc.)
- `tam_suffix` - Tense-aspect-mood markers
- `irrealis_marker` - Irrealis/prospective marker (-ding)
- `nominalizer` - Nominalizing suffixes (-na NMLZ)
- `pronominal_prefix` - Person agreement prefixes (ka-, na-, a-)
- `object_marker` - Object/direction markers (kong-, hong-)
- `plural_marker` - Plural suffix (-te PL)
- `sentence_final` - Sentence-final markers (hi, e)
- `directional_verb` - Directional verbs (pai, hong, etc.)
- `auxiliary` - Auxiliary verbs
- `particle` - Discourse/focus particles
- `function_word` - General function words

#### examples.tsv
```
item_type    item_id    verse_id    tedim_text    kjv_text    segmented    glossed    example_quality    word_count
```

| Field | Description |
|-------|-------------|
| `segmented` | Morpheme-segmented form of target word |
| `glossed` | Interlinear gloss of target word |
| `example_quality` | Type of example selected |

Example quality values (aspirational - currently uses `shortest`, `canonical`, `transparent`):
- `shortest` - Shortest verse containing the item
- `canonical` - Most typical usage
- `transparent` - Clear morphological structure with minimal affixation
- `marked` - Secondary or unusual function (future)

#### ambiguities.tsv
```
normalized_form    surface_form    frequency    segmentation    gloss    pos
alt_segmentations    lemma    alt_lemmas    alt_pos    confidence    review_reasons    issue
```

| Field | Description |
|-------|-------------|
| `alt_segmentations` | Number of different segmentations attested |
| `alt_lemmas` | Other lemmas this form maps to |
| `alt_pos` | Other POS assignments for this form |
| `review_reasons` | Specific flags (e.g., `known_polysemous`, `multi_lemma:2`) |

Forms are flagged for review when they have:
- Multiple segmentations for the same surface form
- Multiple lemma assignments
- Multiple POS assignments
- Known polysemy (hi, hong, ta, te, na, in, etc.)
- UNK POS assignment
- Partial gloss (contains '?')

## Regenerating

To regenerate all files:

```bash
python scripts/export_tedim_analysis.py
```

To generate sample dictionary entries:

```bash
python scripts/generate_sample_entries.py
```

The scripts are deterministic: running twice produces identical output.

## Usage Examples

### Find all forms of a lemma
```bash
grep "^pai\t" lemmas.tsv | cut -f7
```

### Get examples for a grammatical morpheme
```bash
grep "^morpheme\tna\t" examples.tsv
```

### Find verbs with Form II alternation
```bash
awk -F'\t' '$10=="II"' tokens.tsv | cut -f7 | sort -u
```

### List case markers by frequency
```bash
awk -F'\t' '$3=="case_marker"' grammatical_morphemes.tsv | sort -t$'\t' -k5 -rn
```

### Find polysemous lemmas needing review
```bash
awk -F'\t' '$10==1 && $11==1' lemmas.tsv | cut -f1,4
```

## Notes

- Proper nouns are marked with POS=PROP and glossed in ALL CAPS
- Form I/II verb alternation (Henderson 1965) is tracked in `stem_alternation`
- The `ambiguities.tsv` file contains items flagged for human review (~4,000 items)
- Multi-word glosses use dots (e.g., `look.at`, `come.DIR`)
- Polysemous morphemes have separate rows per function in `grammatical_morphemes.tsv`
