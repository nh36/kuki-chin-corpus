# Tedim Chin Documentation

This directory contains documentation for Tedim Chin analysis and the shared backend architecture.

## Architecture Overview

The Tedim Chin system uses a **backend-centered workflow**:

1. **Authoring Layer** (`scripts/analyze_morphemes.py`)
   - Human-curated morphological analyzer
   - Lexicon with compounds, stems, function words
   - Disambiguation rules for homophonous forms

2. **Intermediate Exports** (`data/ctd_analysis/*.tsv`)
   - Generated TSV files from the analyzer
   - sources, tokens, wordforms, lemmas, senses, examples, grammatical_morphemes

3. **Normalized Backend** (`data/ctd_backend.db`)
   - SQLite database with stable IDs and relationships
   - Senses linked to examples with quality rankings
   - Constructions and grammar topics layer
   - Review queue for uncertain items

4. **Outputs** (grammar reports, dictionary entries)
   - All generated from the backend, not directly from analyzer
   - See `output/` for generated reports

## Key Documents

| Document | Description |
|----------|-------------|
| `BACKEND_SPEC.md` | **Backend specification** - schema, API, workflow |
| `SKELETON_GRAMMAR.md` | Grammar overview (working draft) |
| `GENERALIZATION_NOTES.md` | Notes for scaling to other Kuki-Chin languages |

## Directory Structure

```
docs/
├── BACKEND_SPEC.md      # Backend specification (read first)
├── SKELETON_GRAMMAR.md  # Main grammar overview
├── GENERALIZATION_NOTES.md # Scaling notes
├── grammar/             # Reference materials
│   ├── reports/         # Generated grammar reports
│   ├── noun/            # Noun-specific docs
│   ├── verb/            # Verb-specific docs
│   ├── DISAMBIGUATION.md
│   └── MORPHEME_INVENTORY.md
├── methodology/         # How the analyzer was built
│   ├── METHODOLOGY.md
│   ├── REPLICATION_GUIDE.md
│   └── QUALITY_AUDIT.md
└── archive/             # Superseded documents
```

## Grammar Reports

Grammar reports in `grammar/reports/` are now generated from the backend:

```bash
# Generate all grammar reports
make grammar-reports
```

Reports are organized by chapter:

| Prefix | Chapter | Content |
|--------|---------|---------|
| `03-noun-` | Ch 3: Nominal Morphology | Nouns, postpositions, NP structure |
| `04-np-` | Ch 4: Noun Phrases | Possession |
| `05-verb-` | Ch 5: Verbal Morphology | Verbs, TAM, agreement, valency |
| `06-func-` | Ch 6: Function Words | Pronouns, demonstratives, negation |
| `07-*` | Ch 7: Derivation | Nominalization, reduplication |
| `08-clause-` | Ch 8: Clause Structure | Subordination, switch reference |
| `09-sent-` | Ch 9: Sentence Types | Interrogatives |
| `10-disc-` | Ch 10: Discourse | Sentence-final particles |

## Backend-Driven Outputs

New outputs are generated from the backend in `output/`:

| File | Description |
|------|-------------|
| `grammar_constructions.md` | Constructions organized by category |
| `grammar_full.md` | Full grammar organized by topics |
| `tam_report_backend.md` | TAM morphemes with corpus examples |
| `case_report_backend.md` | Case markers with examples |
| `sample_entries_*.md` | Dictionary entry samples |

## Regenerating Outputs

```bash
# Canonical workflow
make backend          # Rebuild from TSV exports
make backend-check    # Verify integrity
make link-examples    # Link examples to senses
make grammar-reports  # Generate grammar outputs
make dictionary       # Generate dictionary outputs
```

## See Also

- `BACKEND_SPEC.md` for the backend schema and API
- `scripts/README.md` for script documentation
- `PROGRESS.md` (repo root) for development history
