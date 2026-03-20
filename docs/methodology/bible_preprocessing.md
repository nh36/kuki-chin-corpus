# Bible Text Preprocessing

When extracting Bible texts from bible.com or other sources, apply these normalization steps before analysis.

## 1. Apostrophe Normalization (REQUIRED)

Bible.com renders text with typographic curly quotes. These must be normalized to ASCII straight quotes for consistent processing.

**Characters to normalize:**
- `'` (U+2019, RIGHT SINGLE QUOTATION MARK) → `'` (U+0027, APOSTROPHE)
- `'` (U+2018, LEFT SINGLE QUOTATION MARK) → `'` (U+0027, APOSTROPHE)

**Why this matters:**
Tedim Chin uses apostrophes in contractions like `ke'n` (1SG.PRO), `hi'ng` (be-EMPH), `kua'n` (nobody-EMPH). If curly quotes are not normalized, tokenization splits these into fragments (`ke` + `n`), causing false "unknown" tokens.

**Command:**
```python
content = content.replace('\u2019', "'").replace('\u2018', "'")
```

Or with sed:
```bash
sed -i "s/'/'/g; s/'/'/g" bibles/extracted/*/??-x-bible.txt
```

## 2. Verify Metadata Lines

Ensure metadata lines start with `#` so they can be skipped during analysis:
```
# language_name:Tedim Chin
# closest ISO 639-3:ctd
```

Coverage scripts should skip lines starting with `#`.

## Checklist for New Bible Extractions

- [ ] Extract text from source
- [ ] Normalize curly quotes to straight quotes
- [ ] Verify metadata lines have `#` prefix
- [ ] Run coverage check to verify tokenization works
