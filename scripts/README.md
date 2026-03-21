# Tedim Chin Analysis Scripts

This directory contains Python scripts for morphological analysis and report generation.

## Core Analyzer

| Script | Description |
|--------|-------------|
| `analyze_morphemes.py` | **Main morphological analyzer** - 100% coverage on Tedim Bible |
| `report_utils.py` | Shared utilities for report generation |

## Report Generators

Reports are output to `docs/grammar/reports/` (repository root).

### Noun Reports

| Script | Output | Description |
|--------|--------|-------------|
| `generate_paradigm.py` | `docs/grammar/reports/03-noun-01-simple.md` etc | Noun paradigm tables |
| `generate_relator_report.py` | `docs/grammar/reports/03-noun-04-relators.md` | Relator nouns |
| `generate_postposition_report.py` | `docs/grammar/reports/03-noun-05-postpositions.md` | Free postpositions |
| `generate_np_report.py` | `docs/grammar/reports/03-noun-06-np-structure.md` | NP structure patterns |

### Verb Reports

| Script | Output | Description |
|--------|--------|-------------|
| `generate_verb_stems_report.py` | `docs/grammar/reports/05-verb-01-stems.md` | Verb stem inventory |
| `generate_vp_report.py` | `docs/grammar/reports/05-verb-02-vp-structure.md` | VP template |
| `generate_pronominal_report.py` | `docs/grammar/reports/05-verb-03-agreement.md` | Agreement prefixes |
| `generate_tam_report.py` | `docs/grammar/reports/05-verb-04-tam.md` | TAM suffixes |
| `generate_vp_slots_report.py` | `docs/grammar/reports/05-verb-05-*.md` | Aspect/Dir/Modal/Deriv |
| `generate_valency_report.py` | `docs/grammar/reports/05-verb-09-valency.md` | Valency/voice |

### Other Reports

| Script | Output | Description |
|--------|--------|-------------|
| `generate_nominalization_report.py` | `docs/grammar/reports/07-nmlz-01-deverbal.md` | Nominalization |

## Utility Scripts

| Script | Description |
|--------|-------------|
| `gloss_verse.py` | Gloss a single verse interactively |
| `lookup_word.py` | Look up a word in the analyzer |
| `lemmatizer.py` | Extract lemmas from analyzed forms |
| `spelling_explorer.py` | Analyze spelling variations |

## Data Processing

| Script | Description |
|--------|-------------|
| `extract_bibles.sh` | Extract Bible texts from zip files |
| `preprocess_corpus.py` | Normalize corpus text |
| `build_verse_alignment.py` | Align parallel Bible verses |
| `build_wordform_inventory.py` | Extract unique wordforms |
| `build_bootstrap_lexicon.py` | Create initial lexicon |

## Usage

```bash
# Analyze a word
python3 scripts/analyze_morphemes.py

# Generate all verb reports
python3 scripts/generate_verb_stems_report.py
python3 scripts/generate_tam_report.py
python3 scripts/generate_vp_slots_report.py
python3 scripts/generate_valency_report.py
python3 scripts/generate_pronominal_report.py
python3 scripts/generate_nominalization_report.py
python3 scripts/generate_vp_report.py

# Generate noun reports
python3 scripts/generate_np_report.py
python3 scripts/generate_relator_report.py
python3 scripts/generate_postposition_report.py
```

## Testing

```bash
# Run all tests
python3 tests/test_coverage_reporting.py
python3 tests/test_vp_slots.py
```
