# Kuki-Chin Bible Readers & Comparative Lexicon

Pipeline for producing linguistic readers, dictionaries, and comparative lexical resources from Bible translations in Kuki-Chin languages.

## Data Sources

### Available Bibles (9 languages)

| Language | ISO 639-3 | File | Year | Full Bible |
|----------|-----------|------|------|------------|
| Bawm Chin | bgr | `bgr-x-bible.zip` | | Yes |
| Falam Chin | cfm | `cfm-x-bible.zip` | | Yes |
| Hakha Chin | cnh | `cnh-x-bible.zip` | | Yes |
| Mizo | lus | `lus-x-bible-1959.zip` | 1959 | Yes |
| Nga'la (Mara) | hlt | `hlt-x-bible.zip` | | Yes |
| Sizang (Siyin) | csy | `csy-x-bible.zip` | | Yes |
| Tedim Chin | ctd | `ctd-x-bible.zip` | 2010 | Yes |
| Zo | zom | `zom-x-bible.zip` | | Yes |
| Zotung | czt | `czt-x-bible.zip` | | Yes |

### Additional Bibles Available for Scraping

From bible.com (see `Kuki-Chin bible list.rtf`):
- Khumi, Lautu, Matu, Lemi (Eastern Khumi), Mro (Khimi), Cho, Paite, Thadou, Zyphe

## Data Format

Source: [paralleltext.info](http://paralleltext.info/) Parallel Bible Corpus

Each zip contains:
- `{iso}-x-bible.txt` - Full Bible text (TSV: verse_id TAB text)
- `{iso}-x-bible.wordforms` - Word frequency list (TSV: word TAB count)
- `{iso}-x-bible.mtx` - Sparse matrix (Matrix Market format) for cross-linguistic alignment
- `versenames.txt` - Universal verse ID reference
- `datapackage.json` - Metadata
- `README.md` - Format documentation

### Verse ID Format

`BBCCCVVV` where:
- BB = Book number (01=Genesis, 40=Matthew, etc.)
- CCC = Chapter
- VVV = Verse

## Project Goals

1. **Reader volumes** (Matthew, Mark, Luke–Acts) with:
   - Original Kuki-Chin text
   - Leipzig-style interlinear glossing
   - English translation

2. **Per-language dictionaries** extracted from complete Bible

3. **Comparative dictionary** across all Kuki-Chin languages with reconstructions

## Directory Structure

```
Kuki-Chin/
├── *.zip                  # Original Bible archives
├── bibles/
│   └── extracted/         # Extracted text files
├── data/                  # Processed data (TSV/JSON)
├── scripts/               # Processing pipelines
├── docs/                  # Documentation
└── README.md
```

## Usage

```bash
# Extract all Bibles
./scripts/extract_bibles.sh

# Build wordform inventory
python scripts/build_wordform_inventory.py
```

## License

Bible texts are © their respective publishers (primarily Bible Society of Myanmar).
Corpus format from paralleltext.info project (Mayer & Cysouw).
