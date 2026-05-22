# Kuki-Chin Bible Corpus & Morphological Analysis

A digital philology infrastructure for Kuki-Chin languages, featuring:
- **20 Bible corpora** aligned by verse (422,676 unique wordforms)
- **Tedim Chin morphological analyzer** with Leipzig-style glossing
- **SQLite backend** for normalized dictionary/grammar data
- Bootstrap lexicons and interlinear glossing tools

## Current publication priority

The current publication phase is focused on the **Tedim Chin** package: **grammar, dictionary, and chrestomathy/reader**.
Scaling the same workflow to **Mizo/lus** and the remaining Kuki-Chin languages is a later phase, after the Tedim publication outputs are in publishable form.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Authoring Layer                              │
│  scripts/analyze_morphemes.py → data/ctd_analysis/*.tsv        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Backend (SQLite)                             │
│  data/ctd_backend.db ← scripts/backend.py                      │
│  Tables: lemmas, senses, wordforms, examples, morphemes...     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Publication Outputs                          │
│  output/dictionary/  output/grammar/  output/metrics/          │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Build the backend from TSV exports
make backend

# Run the standard test workflow
make test

# Generate backend-driven drafting outputs
make grammar-reports
make dictionary
```

Standard workflow commands:

- `make backend` - rebuild the Tedim SQLite backend
- `make backend-check` - verify backend counts and integrity
- `make grammar-reports` - generate backend-driven grammar reports, including the integration dashboard
- `make dictionary` - generate backend-driven dictionary sample outputs
- `make test` - run the analyzer test runner, rebuild backend, then run the full pytest suite

## Tedim Chin: Current Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Corpus tokens | 831,152 | Full Bible text |
| Lemmas | 7,339 | All with glosses |
| Senses | 9,962 | Including polysemous items |
| Grammatical morphemes | 485 | Affixes and clitics |
| Corpus examples | 26,898 | Linked to senses/morphemes |
| Coverage (known POS) | 100.0% | Full morphological analysis |
| Senses with examples | 5,812 | 58% of senses |

Regenerate metrics: `make metrics` → `output/metrics/ctd_metrics.json`

### Test Coverage

| Suite | Tests | Purpose |
|-------|-------|---------|
| Backend tests | 61 | Database integrity, API behavior, end-to-end workflow |
| Export tests | 56 | TSV export correctness |
| Orthography tests | 71 | Normalization and tone restoration |
| Metrics tests | 10 | Publication readiness gates |
| Other analyzer tests | 166 | POS tagging, morphology, disambiguation |
| **Total** | **364** | |

Run tests: `make test` for the standard workflow, `make test-backend` for the backend-native pytest suite, or `python3 -m pytest tests/` for direct pytest.