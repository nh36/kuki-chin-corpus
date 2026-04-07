# Tedim Chin Bible Analysis Export

This directory contains the full morphological analysis of the Tedim Chin Bible corpus, structured for dictionary and grammar work.

## Files

### Core Data Files

| File | Description | Rows |
|------|-------------|------|
| `verses.tsv` | Verse-level metadata with original text | ~30,000 |
| `tokens.tsv` | Token-level full analysis (one row per word) | ~831,000 |
| `wordforms.tsv` | Type-level aggregation (distinct word forms) | ~22,000 |
| `lemmas.tsv` | Lemma-level dictionary seed | ~6,700 |
| `grammatical_morphemes.tsv` | Grammatical morpheme inventory | ~200 |
| `examples.tsv` | Curated examples bank | ~20,000 |
| `ambiguities.tsv` | Review queue for uncertain analyses | varies |
| `coverage_report.md` | Coverage statistics and summary | - |

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
lemma    citation_form    pos    glosses    inflected_forms    token_count
form_count    compounds    top_collocates    example_verses
polysemy_notes    grammaticalization_notes
```

#### grammatical_morphemes.tsv
```
form    gloss    category    frequency    environments    example_verses
ambiguity_notes    status
```

Categories include:
- `case` - Case markers (ERG, LOC, ABL, etc.)
- `tam` - Tense-aspect-mood markers
- `nominalizer` - Nominalizing suffixes
- `pronominal_prefix` - Person agreement prefixes
- `object_prefix` - Object markers
- `particle` - Discourse/focus particles
- `sentence_final` - Sentence-final markers
- `directional` - Directional morphemes
- `auxiliary` - Auxiliary verbs
- `function` - General function words

#### examples.tsv
```
item_type    item_id    verse_id    tedim_text    kjv_text    example_quality    word_count
```

Example quality values:
- `shortest` - Shortest verse containing the item
- `canonical` - Most typical usage
- `transparent` - Clear morphological structure
- `marked` - Secondary or unusual function

## Regenerating

To regenerate all files:

```bash
python scripts/export_tedim_analysis.py
```

Options:
- `--output-dir DIR` - Output directory (default: `data/ctd_analysis`)
- `--bible PATH` - Path to Tedim Bible TSV
- `--kjv PATH` - Path to aligned KJV translations

The script is deterministic: running twice produces identical output.

## Usage Examples

### Find all forms of a lemma
```bash
grep "^pai\t" lemmas.tsv | cut -f5
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
awk -F'\t' '$3=="case"' grammatical_morphemes.tsv | sort -t$'\t' -k4 -rn
```

## Notes

- Proper nouns are marked with POS=PROP and glossed in ALL CAPS
- Form I/II verb alternation (Henderson 1965) is tracked in `stem_alternation`
- The `ambiguities.tsv` file contains items flagged for human review
- Multi-word glosses use dots (e.g., `look.at`, `come.DIR`)
