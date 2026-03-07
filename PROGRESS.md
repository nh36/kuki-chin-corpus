# Kuki-Chin Corpus Project: Progress Report

## Project Overview

This project builds digital philology infrastructure for Kuki-Chin languages, focusing on:
1. Bible corpus collection and alignment (20 languages)
2. Bootstrap lexicon generation via PMI-based word alignment
3. Morphological analysis and Leipzig-style glossing (starting with Tedim)

## Completed Phases

### Phase 1: Corpus Collection ✓
- Scraped Bibles from multiple sources (bible.com, ebible.org)
- 20 Kuki-Chin languages with aligned verses
- 31,105 verses per language
- Master file: `data/verses_aligned.tsv`

### Phase 2: Bootstrap Lexicons ✓
- Generated pairwise lexicons using PMI scoring
- Context disambiguation with top English glosses
- Lexicons stored in `data/lexicons/` (e.g., `ctd_lexicon.tsv`)
- ~4,000 entries per language

### Phase 3: Verse Glosser ✓
- Created glossing tool with confidence scoring
- Handles high/medium/low confidence items
- Uses PMI scores and context for disambiguation

### Phase 4: Leipzig Morphological Analyzer ✓
- Focus: Tedim Chin (ctd)
- **Current coverage: 98.99% of tokens**
- Handles: prefixes, stems, suffixes, compounds, reduplication

## Current Analyzer Performance (2026-03-07)

### Overall Statistics
```
Total tokens:   761,347
Glossed:        754,006 (99.04%)
Unknown:          7,341 (0.96%)
```

### Analyzer Components (Current)

1. **Function Words** (~100 entries)
   - Pronouns, demonstratives, particles
   - TAM markers, negation, question words

2. **Verb Stems** (~190 entries)
   - Stem I/II alternation (mu/muh, za/zak, thei/theih)
   - Motion, perception, cognition, speech, transfer verbs
   - Reflexive bases for ki- decomposition

3. **Noun Stems** (~170 entries)
   - Religious, social, kinship, body part terms
   - Place, time, abstract nouns

4. **Compound Words** (~400 entries)
   - Noun+LOC: tungah, sungah, kiangah
   - Verb+NMLZ: mawhna, biakna, nuntakna
   - Noun+Noun: tapa, biakinn, lungsim
   - Reflexive: kibawl, kipan, kisai

5. **Productive Morphology**
   - Prefix stripping: ka-, na-, a-, kong-, hong-, ki-
   - Suffix handling: -na (NMLZ), -te (PL), -in (ERG), -ah (LOC)
   - **Reduplication**: X~X patterns (zelzel → zel~RED)
   - **Recursive ki-**: ki-STEM-SUFFIX decomposition

## File Structure

```
Kuki-Chin/
├── data/
│   ├── verses_aligned.tsv      # Master corpus (20 languages)
│   └── lexicons/
│       └── ctd_lexicon.tsv     # Tedim bootstrap lexicon
├── scripts/
│   ├── analyze_morphemes.py    # Leipzig analyzer (~1,700 lines)
│   ├── lemmatizer.py           # Lemmatization module
│   ├── henderson_ocr.py        # OCR pipeline for Henderson
│   └── spelling_explorer.py    # Spelling variation analysis
├── analysis/
│   ├── spelling_analysis.json  # Quantitative spelling analysis
│   └── spelling_variation_report.txt
└── literature/
    ├── RESOURCES.md            # Available secondary literature
    ├── DESIDERATA.md           # Needed resources
    └── tedim-ctd/
        ├── MORPHEME_INVENTORY.md  # Morpheme documentation
        └── ocr/                    # Henderson OCR output
            ├── henderson_65a_combined.txt
            └── henderson_65a_text/
```

## Completed Workstreams

### Workstream 1: Short-term Improvements ✓

**Goal:** Add stems/compounds to reach 95% → **Achieved 98.99%**

**Completed:**
- Added ~90 more verb stems (Round 2-4)
- Implemented reduplication handling (91 forms)
- Added recursive ki- prefix decomposition (1,158 forms)
- Fixed case-sensitivity bugs in morpheme matching
- Added proper noun + suffix handling

### Workstream 2: Henderson Digitization (In Progress)

**Goal:** Extract vocabulary lists from Henderson 1965 via OCR

**Completed:**
- Henderson 1965a: 48 pages OCR'd (~5,000 lines)
- OCR quality: Good for linguistic content
- Created iterative error correction pipeline

**Remaining work:**
- Parse OCR output for vocabulary entries
- Extract glossed word lists
- Cross-reference with analyzer lexicon
- OCR Henderson 1965b and "Two Texts"

### Workstream 3: Spelling Variation ✓

**Findings:**
- Most "variation" is grammatical Stem I/II alternation
- True orthographic variation is minimal
- **Recommendation:** No aggressive normalization needed

## Remaining Unknown Words (~1%)

The remaining 7,672 unknown tokens (1.01%) fall into these categories:

| Category | Est. % | Examples |
|----------|--------|----------|
| Very rare vocabulary (hapax) | ~40% | dongun, veipi, utzaw |
| Complex ki- forms not yet handled | ~25% | kiam, kinga, kiphut |
| Proper nouns not in list | ~15% | Minor biblical names |
| Dialectal/archaic forms | ~10% | Variant spellings |
| Potential loan words | ~10% | peel, vot, seek |

## Progress Log

| Date | Coverage | Δ | Action |
|------|----------|---|--------|
| 2026-03-06 | 84.2% | - | Baseline |
| 2026-03-06 | 86.4% | +2.2 | Punctuation fix |
| 2026-03-06 | 87.9% | +1.5 | Proper nouns |
| 2026-03-06 | 90.2% | +2.3 | Expanded stems |
| 2026-03-06 | 90.6% | +0.4 | Suffix handling |
| 2026-03-07 | 92.3% | +1.7 | Compounds + bug fixes |
| 2026-03-07 | 98.99% | +6.7 | Verb stems, ki- prefix, reduplication |
| 2026-03-07 | 99.04% | +0.05 | Philological analysis, 16 new stems |

## Current Phase: Quality Assurance & Refinement

### Immediate Next Steps

1. [ ] Audit development documentation (ensure all work is recorded)
2. [ ] Extract vocabulary from Henderson OCR output
3. [ ] Analyze remaining ~7,600 unknown tokens philologically
4. [ ] Identify loan words and determine if analyzable
5. [ ] Cross-reference Henderson with remaining unknowns

### Questions for Remaining Unknowns

For each remaining unknown word:
1. What Bible verses does it appear in?
2. What is the corresponding KJV English text?
3. Can meaning be confidently inferred from context?
4. Is it a variant spelling of a known word?
5. Is it a loan word? If so, from what language?
6. Does Henderson 1965 document it?

---

*Last updated: 2026-03-07 09:00 UTC*
*Coverage: 99.04% | Tokens: 754,006/761,347 | Unknown: 7,341*
