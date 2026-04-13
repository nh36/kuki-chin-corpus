# Tedim Chin Analysis Scripts

This directory contains Python scripts for morphological analysis and the backend-centered workflow.

## Architecture

Scripts are organized into three layers:

1. **Authoring Layer** - Human-curated analyzer
2. **Backend Layer** - Normalized SQLite database
3. **Generation Layer** - Reports and outputs from backend

## Core Components

### Authoring Layer

| Script | Description |
|--------|-------------|
| `analyze_morphemes.py` | **Main morphological analyzer** - 100% coverage on Tedim Bible |
| `export_analysis.py` | Export analyzer data to TSV files |

### Backend Layer

| Script | Description |
|--------|-------------|
| `backend.py` | **SQLite backend** - schema, migration, API |
| `check_backend.py` | Verify backend integrity and counts |
| `link_examples_to_senses.py` | Link examples to senses, generate corpus examples |

### Generation Layer (Backend-Driven)

| Script | Description |
|--------|-------------|
| `generate_tam_report_backend.py` | TAM report with corpus examples |
| `generate_case_report_backend.py` | Case markers with examples |
| `generate_grammar_from_backend.py` | Grammar constructions and topics |
| `generate_sample_entries_backend.py` | Dictionary entries |
| `lookup_word.py` | Dictionary lookup (reads from backend) |

### Shared Utilities

| Script | Description |
|--------|-------------|
| `report_utils.py` | Shared utilities for report generation |
| `lemmatizer.py` | Extract lemmas from analyzed forms |

## Canonical Workflow

```bash
# 1. Edit the analyzer (add vocabulary, fix glosses)
#    scripts/analyze_morphemes.py

# 2. Export to TSV
python scripts/export_analysis.py

# 3. Rebuild backend
make backend

# 4. Verify integrity
make backend-check

# 5. Link examples to senses
make link-examples

# 6. Generate outputs
make grammar-reports
make dictionary
```

Or use the Makefile targets directly:

```bash
make backend          # Steps 2-3
make link-examples    # Step 5
make grammar-reports  # Step 6 (grammar)
make dictionary       # Step 6 (dictionary)
```

## Legacy Report Generators

These scripts generate reports directly from the analyzer (pre-backend):

| Script | Output | Status |
|--------|--------|--------|
| `generate_paradigm.py` | Noun paradigm tables | Legacy |
| `generate_verb_stems_report.py` | Verb stem inventory | Legacy |
| `generate_tam_report.py` | TAM suffixes | Superseded by `*_backend.py` |
| `generate_vp_slots_report.py` | VP slot analysis | Legacy |
| `generate_valency_report.py` | Valency patterns | Legacy |

New development should use the backend-driven generators.

## Data Processing Scripts

| Script | Description |
|--------|-------------|
| `extract_bibles.sh` | Extract Bible texts from zip files |
| `preprocess_corpus.py` | Normalize corpus text |
| `build_verse_alignment.py` | Align parallel Bible verses |
| `build_wordform_inventory.py` | Extract unique wordforms |
| `build_bootstrap_lexicon.py` | Create initial lexicon |
| `scrape_bible.py` | Scrape Bibles from bible.com |

## Usage Examples

```bash
# Analyze a word
python3 -c "
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word
print(analyze_word('biakinnpi'))  # ('biak-inn-pi', 'pray-house-big')
"

# Look up a word using the backend
python scripts/lookup_word.py ctd tapa
# Output: son (91.5% confidence), child, boy...

# Reverse lookup
python scripts/lookup_word.py -r ctd water
# Output: tui, tuipi, tuibang...

# Check backend statistics
python scripts/check_backend.py
```

## Testing

```bash
# Run all tests (336 tests)
python -m pytest tests/ -q

# Run backend-native tests only (43 tests)
python -m pytest tests/test_backend.py -v
```

## See Also

- `docs/BACKEND_SPEC.md` for backend schema and API
- `docs/README.md` for documentation overview
- `tests/` for test suite
