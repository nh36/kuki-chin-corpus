# Analysis Working Directory

This directory contains intermediate analysis files generated during
morphological analyzer development. These are working files, not final outputs.

## Contents

| File/Directory | Description |
|----------------|-------------|
| `hapax_analysis.md` | Analysis of words occurring only once |
| `unknown_word_analysis.md` | Investigation of unknown words |
| `conflict_investigation.md` | Resolving gloss conflicts |
| `residual_reports/` | Word-by-word investigations |
| `*.tsv` | Working data files |

## TSV Files

| File | Description |
|------|-------------|
| `compound_entries.tsv` | All compound entries extracted |
| `duplicates_conflicts.tsv` | Conflicting duplicate entries |
| `genuine_polysemy.tsv` | True polysemous words |
| `residual_fully_unknown.tsv` | Words with no analysis |
| `residual_partial.tsv` | Words with partial analysis |
| `spelling_variation_report.txt` | Spelling variants |
| `unknown_words_full.tsv` | Complete unknown word list |

## Note

These files document the development process and may contain
superseded analyses. For final documentation, see `docs/`.
