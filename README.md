# Kuki-Chin Bible Corpus & Morphological Analysis

A digital philology infrastructure for Kuki-Chin languages, featuring:
- **20 Bible corpora** aligned by verse (422,676 unique wordforms)
- **Tedim Chin morphological analyzer** achieving **100% coverage** (771,190 tokens)
- **Shared SQLite backend** serving both dictionary and grammar generation
- Bootstrap lexicons and interlinear glossing tools

## 🎉 Milestone: Tedim Chin Analyzer at 100% Coverage

The Tedim Chin (ctd) morphological analyzer is production-ready:
- **771,190 tokens** fully analyzed with Leipzig-style glossing
- **7,000+ dictionary entries** (compounds, stems, function words, proper nouns)
- **336 automated tests** (including 43 backend-native tests)
- Comprehensive documentation in `docs/` and `tests/`

## Architecture

For Tedim Chin, the system follows a **backend-centered workflow**:

```
┌─────────────────────────────────────────────────────────────────────┐
│  AUTHORING LAYER                                                    │
│  scripts/analyze_morphemes.py + export scripts                      │
│  (Human-curated analyzer with lexicon, rules, disambiguation)       │
└────────────────────────────┬────────────────────────────────────────┘
                             │ make export-analysis
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  INTERMEDIATE ARTIFACTS (data/ctd_analysis/*.tsv)                   │
│  sources.tsv, tokens.tsv, wordforms.tsv, lemmas.tsv, senses.tsv,    │
│  examples.tsv, grammatical_morphemes.tsv                            │
└────────────────────────────┬────────────────────────────────────────┘
                             │ make backend
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  NORMALIZED BACKEND (data/ctd_backend.db)                           │
│  SQLite database: stable IDs, linked senses, quality-ranked         │
│  examples, constructions, grammar topics, review queue              │
└────────────────────────────┬────────────────────────────────────────┘
                             │ make grammar-reports / make dictionary
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  OUTPUTS                                                            │
│  Grammar reports, dictionary entries, lookup results, statistics    │
└─────────────────────────────────────────────────────────────────────┘
```

**Key principle:** The SQLite backend is the canonical serving layer. Grammar reports and dictionary outputs are generated from it, not directly from the analyzer.

## Current Corpus Status

**20 Bible versions across 19 languages, 422,676 unique wordforms**

### Full Bible Coverage (13 languages, 66 books each)

| Language | ISO | Verses | Wordforms | Source |
|----------|-----|--------|-----------|--------|
| English (KJV) | eng | 31,101 | 28,862 | bible.com |
| Thadou Chin | tcz | 31,104 | 70,520 | bible.com |
| Paite Chin | pck | 31,082 | 32,931 | bible.com |
| Zotung Chin | czt | 30,968 | 21,853 | bible.com (ZB16) |
| Hakha Chin | cnh | 30,808 | 19,659 | bible.com |
| Mizo | lus | 30,489 | 26,218 | bible.com |
| Tedim Chin | ctd | 30,422 | 27,599 | bible.com |
| Falam Chin | cfm | 30,262 | 23,442 | bible.com |
| Ngawn Chin | cnw | 30,147 | 24,942 | bible.com |
| Khumi Chin | cnk | 29,862 | 15,383 | bible.com |
| Cho Chin | csh | 29,839 | 19,634 | bible.com |
| Siyin Chin | csy | 29,811 | 20,863 | bible.com |
| Bawm Chin | bgr | 29,721 | 17,715 | bible.com |

### New Testament Only (5 languages, 27 books each)

| Language | ISO | Verses | Wordforms | Source |
|----------|-----|--------|-----------|--------|
| Lautu Chin | clt | 7,938 | 8,798 | bible.com |
| Zyphe Chin | zyp | 7,930 | 7,849 | bible.com |
| Matu Chin | hlt | 7,880 | 8,562 | bible.com |
| Lemi (Eastern Khumi) | cek | 7,817 | 4,489 | bible.com |
| Mro (Khimi) | cmr | 7,770 | 4,381 | bible.com |

### Mark Only (2 versions)

| Language | ISO | Verses | Wordforms | Source |
|----------|-----|--------|-----------|--------|
| Zokam | zom | 678 | 27,461 | paralleltext.info (1994) |
| Zotung (MBS 2002) | czt-mbs | 667 | 11,515 | paralleltext.info |

**Note:** Zotung has two different translations: ZB16 (full Bible) and Myanmar Bible Society 2002 (Mark only).

## Data Format

### Bible Text Files

Each language directory in `bibles/extracted/{iso}/` contains:
- `{iso}-x-bible.txt` - Bible text (TSV: verse_id TAB text)
- `{iso}-x-bible.wordforms` - Word frequency list (TSV: word TAB count)
- `datapackage.json` - Metadata
- `README.md` - Source documentation

### Verse ID Format

`BBCCCVVV` where:
- BB = Book number (01=Genesis, 40=Matthew, 66=Revelation)
- CCC = Chapter (001-150)
- VVV = Verse (001-176)

Example: `41001001` = Mark 1:1 (book 41, chapter 1, verse 1)

### Processed Data

In `data/`:
- `verses_aligned.tsv` - All verses aligned by verse_id across all languages
- `wordforms_by_language.tsv` - Complete wordform inventory (422,676 entries)
- `language_stats.tsv` - Per-language statistics
- `alignment_stats.tsv` - Coverage statistics per language

### Bootstrap Lexicons

In `data/lexicons/`:
- `{iso}_lexicon.tsv` - Word-pair associations ranked by confidence
- Columns: `kc_word`, `kc_freq`, `eng_gloss`, `pmi_score`, `pair_count`, `confidence`, `rank`

Generated via bag-of-words co-occurrence analysis: for each aligned verse pair,
we compute the cross-product of English and Kuki-Chin words and track which
pairings recur most consistently. Sorted by confidence (stability), then PMI.

Lexicon sizes range from ~600 entries (Mark-only) to ~16,000 entries (full Bible).

## Project Goals

1. **Tedim Chin morphological analyzer** ✅ COMPLETE
   - Leipzig-style interlinear glossing at 100% coverage
   - See `scripts/analyze_morphemes.py` (~19,000 lines)

2. **Shared backend architecture** ✅ COMPLETE
   - SQLite backend serving dictionary and grammar from same data
   - See `docs/BACKEND_SPEC.md` for specification

3. **Reader volumes** (Matthew, Mark, Luke–Acts) with:
   - Original Kuki-Chin text
   - Leipzig-style interlinear glossing
   - English translation (from KJV, aligned by verse)

4. **Per-language dictionaries** extracted from backend

5. **Comparative dictionary** across all Kuki-Chin languages with reconstructions

6. **Scale to remaining 18 languages** using Tedim methodology (see `docs/METHODOLOGY.md`)

## Scripts

### Core Components

| Script | Purpose |
|--------|---------|
| `scripts/analyze_morphemes.py` | **Tedim Chin morphological analyzer** (authoring layer) |
| `scripts/backend.py` | **SQLite backend** - normalized serving layer |
| `scripts/lookup_word.py` | Dictionary lookup (reads from backend) |
| `scripts/export_analysis.py` | Export analyzer data to TSV |
| `scripts/report_utils.py` | Shared report utilities |

### Backend & Generation

| Script | Purpose |
|--------|---------|
| `scripts/check_backend.py` | Verify backend integrity |
| `scripts/link_examples_to_senses.py` | Link examples to senses, generate corpus examples |
| `scripts/generate_tam_report_backend.py` | TAM report from backend |
| `scripts/generate_case_report_backend.py` | Case marking report from backend |
| `scripts/generate_grammar_from_backend.py` | Grammar constructions report |
| `scripts/generate_sample_entries_backend.py` | Dictionary entries from backend |

### Corpus Processing

| Script | Purpose |
|--------|---------|
| `scripts/extract_bibles.sh` | Extract original paralleltext.info zip files |
| `scripts/scrape_bible.py` | Scrape Bibles from bible.com |
| `scripts/build_wordform_inventory.py` | Build unified wordform list |
| `scripts/build_verse_alignment.py` | Create aligned verse table |
| `scripts/build_bootstrap_lexicon.py` | Generate word co-occurrence lexicons |

## Directory Structure

```
Kuki-Chin/
├── *.zip                  # Original paralleltext.info archives
├── bibles/
│   └── extracted/         # 20 language directories
│       ├── eng/           # English KJV (reference)
│       ├── ctd/           # Tedim Chin (primary analysis target)
│       └── ...            # Other languages
├── data/
│   ├── ctd_analysis/      # Intermediate TSV exports (generated)
│   │   ├── sources.tsv
│   │   ├── tokens.tsv
│   │   ├── wordforms.tsv
│   │   ├── lemmas.tsv
│   │   ├── senses.tsv
│   │   └── ...
│   ├── ctd_backend.db     # SQLite backend (generated, gitignored)
│   ├── verses_aligned.tsv
│   ├── wordforms_by_language.tsv
│   └── lexicons/          # Bootstrap lexicons per language
├── docs/
│   ├── README.md          # Documentation guide
│   ├── BACKEND_SPEC.md    # Backend specification
│   ├── SKELETON_GRAMMAR.md # Grammar overview
│   ├── GENERALIZATION_NOTES.md # Notes for scaling to other languages
│   ├── grammar/           # Grammar reference materials
│   │   ├── reports/       # Generated grammar reports (33 files)
│   │   │   ├── 03-noun-*.md   # Nominal morphology (Ch 3)
│   │   │   ├── 05-verb-*.md   # Verbal morphology (Ch 5)
│   │   │   └── ...
│   │   └── ...
│   └── methodology/       # How to build analyzers
│       ├── METHODOLOGY.md
│       └── REPLICATION_GUIDE.md
├── scripts/
│   ├── README.md          # Script documentation
│   ├── analyze_morphemes.py # Tedim analyzer (authoring layer)
│   ├── backend.py         # SQLite backend (serving layer)
│   ├── lookup_word.py     # Dictionary lookup
│   ├── generate_*_backend.py # Backend-driven report generators
│   └── report_utils.py    # Shared utilities
├── tests/
│   ├── test_backend.py    # Backend-native tests (43 tests)
│   ├── test_export_analysis.py
│   └── ...                # 336 total tests
├── output/                # Generated reports
│   ├── grammar_constructions.md
│   ├── grammar_full.md
│   ├── tam_report_backend.md
│   └── ...
├── Makefile               # Build targets (backend, grammar-reports, etc.)
├── PROGRESS.md            # Development history
└── README.md
```

## Quick Start

```bash
# Rebuild the backend from exported analysis
make backend

# Verify backend integrity
make backend-check

# Link examples to senses (sense disambiguation)
make link-examples

# Generate grammar reports from backend
make grammar-reports

# Generate dictionary outputs from backend
make dictionary

# Look up a word using the backend
python scripts/lookup_word.py ctd tapa

# Run all tests
python -m pytest tests/ -q
```

## Workflow

The canonical workflow for Tedim Chin is:

1. **Edit** `scripts/analyze_morphemes.py` (add vocabulary, fix glosses)
2. **Export** analysis to TSV: `python scripts/export_analysis.py`
3. **Rebuild** backend: `make backend`
4. **Link** examples to senses: `make link-examples`
5. **Generate** outputs: `make grammar-reports` or `make dictionary`

The backend database (`data/ctd_backend.db`) is a generated artifact and should not be committed to git. It can always be rebuilt from the TSV exports.

## Data Sources

- **bible.com**: Primary source for most Bibles (scraped)
- **paralleltext.info**: Original corpus (Mayer & Cysouw) - Mark only for most languages

## License

Bible texts are © their respective publishers (primarily Bible Society of Myanmar, Bible League, etc.).
See individual Bible metadata for copyright information.
