# Kuki-Chin Bible Readers & Comparative Lexicon

Pipeline for producing linguistic readers, dictionaries, and comparative lexical resources from Bible translations in Kuki-Chin languages.

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

1. **Reader volumes** (Matthew, Mark, Luke–Acts) with:
   - Original Kuki-Chin text
   - Leipzig-style interlinear glossing
   - English translation (from KJV, aligned by verse)

2. **Per-language dictionaries** extracted from complete Bible

3. **Comparative dictionary** across all Kuki-Chin languages with reconstructions

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/extract_bibles.sh` | Extract original paralleltext.info zip files |
| `scripts/scrape_bible.py` | Scrape Bibles from bible.com |
| `scripts/build_wordform_inventory.py` | Build unified wordform list across all languages |
| `scripts/build_verse_alignment.py` | Create aligned verse table for parallel comparison |
| `scripts/build_bootstrap_lexicon.py` | Generate word co-occurrence lexicons for all languages |
| `scripts/lookup_word.py` | Interactive lookup tool (forward and reverse) |

## Directory Structure

```
Kuki-Chin/
├── *.zip                  # Original paralleltext.info archives
├── bibles/
│   └── extracted/         # 20 language directories
│       ├── eng/           # English KJV (reference)
│       ├── bgr/           # Bawm Chin
│       ├── ...            # Other languages
│       └── czt-mbs/       # Zotung MBS 2002 (variant translation)
├── data/
│   ├── verses_aligned.tsv
│   ├── wordforms_by_language.tsv
│   ├── language_stats.tsv
│   └── alignment_stats.tsv
├── scripts/               # Processing pipelines
└── README.md
```

## Usage

```bash
# Scrape a Bible from bible.com
python scripts/scrape_bible.py --version-id 1 --iso eng --abbrev KJV --name "King James Version"

# Build wordform inventory
python scripts/build_wordform_inventory.py

# Build verse alignment table
python scripts/build_verse_alignment.py

# Generate bootstrap lexicons for all languages
python scripts/build_bootstrap_lexicon.py

# Look up a word (KC -> English)
python scripts/lookup_word.py ctd tapa
# Output: son (91.5% confidence), and, the, of, he...

# Reverse lookup (English -> KC words across all languages)
python scripts/lookup_word.py --all -r water
# Output: tui-related words in most languages (tuithawl, tuidam, tuiahte, etc.)

# Look up English word in a specific language
python scripts/lookup_word.py -r ctd water
```

## Data Sources

- **bible.com**: Primary source for most Bibles (scraped)
- **paralleltext.info**: Original corpus (Mayer & Cysouw) - Mark only for most languages

## License

Bible texts are © their respective publishers (primarily Bible Society of Myanmar, Bible League, etc.).
See individual Bible metadata for copyright information.
