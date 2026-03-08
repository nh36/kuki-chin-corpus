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
- **Current coverage: 97.76% of tokens**
- Handles: prefixes, stems, suffixes, compounds, reduplication

## Current Analyzer Performance (2026-03-08)

### Overall Statistics
```
Total tokens:      831,340
Fully analyzed:    812,734 (97.76%)
Partial:            13,068 (1.57%)  -- has some morphemes glossed
Unknown:             5,538 (0.67%)  -- completely unknown
```

### Quality Assurance (Allomorph Audit)
```
-te (Plural) suffix audit:
  Correctly analyzed:    26,700+ tokens
  Unknown base + -te:     ~1,700 tokens (down from 2,360)
  Flagged issues:           ~200 cases (down from 361)

Session accomplishments:
- Created allomorph_audit.py for systematic quality checks
- Fixed 200+ over-segmentation bugs via protective COMPOUND_WORDS entries
- Verified -te is a single allomorph (no -ite, -ate variants)
- Distribution: vowel-final (66%), consonant-final (34%)
- Pushed from 97.57% to 97.76% via philological expansion
```

### Analyzer Components (Current)

1. **Function Words** (~120 entries)
   - Pronouns, demonstratives, particles
   - TAM markers, negation, question words

2. **Verb Stems** (~280 entries)
   - Stem I/II alternation (mu/muh, za/zak, thei/theih)
   - Motion, perception, cognition, speech, transfer verbs
   - Reflexive bases for ki- decomposition

3. **Noun Stems** (~260 entries)
   - Religious, social, kinship, body part terms
   - Place, time, abstract nouns
   - Session 6 additions: hing, vun, thal, innsa, gamsa, etc.

4. **Compound Words** (~1,550 entries)
   - Noun+LOC: tungah, sungah, kiangah
   - Verb+NMLZ: mawhna, biakna, nuntakna
   - Noun+Noun: tapa, biakinn, lungsim
   - Reflexive: kibawl, kipan, kisai
   - Philologically verified via KJV cross-referencing
   - **Over-segmentation guards**: protective entries for hingte, innsate, etc.
   - **Session additions (Rounds 22-37)**: 200+ new entries

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
| 2026-03-07 | 97.02% | +4.7 | Philological expansion to 97% |
| 2026-03-07 | 97.21% | +0.19 | Quality-focused expansion |
| 2026-03-07 | 97.25% | +0.04 | Bug fixes (namte, alang) |
| 2026-03-08 | 97.44% | +0.19 | Session 6 Rounds 1-6 |
| 2026-03-08 | 97.50% | +0.06 | Session 6 Rounds 7-8 |
| 2026-03-08 | 97.57% | +0.07 | Session 6 Rounds 9-10 |
| 2026-03-08 | 97.63% | +0.06 | Allomorph audit, Rounds 11-22 |
| 2026-03-08 | 97.65% | +0.02 | Rounds 23-25 vocabulary |
| 2026-03-08 | 97.67% | +0.02 | Rounds 26-28 vocabulary |
| 2026-03-08 | 97.69% | +0.02 | Rounds 29-30 vocabulary |
| 2026-03-08 | 97.71% | +0.02 | Rounds 31-32 vocabulary |
| 2026-03-08 | 97.73% | +0.02 | Rounds 33-34 vocabulary |
| 2026-03-08 | 97.75% | +0.02 | Rounds 35-36 vocabulary |
| 2026-03-08 | 97.76% | +0.01 | Round 37 vocabulary |

## Current Phase: Quality-Focused Expansion

**Coverage: 97.76% fully analyzed | 1.57% partial | 0.67% unknown**

### Session 7 Accomplishments (2026-03-08)

1. **Vocabulary additions via philological analysis**
   - Added ~200 new compound word entries (Rounds 22-37)
   - All verified via KJV English cross-referencing
   - Categories: biblical terminology, body parts, legal terms, measurements
   
2. **Notable additions by round:**
   - Round 22: tuletate, khainiangte, puantungsilhte, ekte, bilngongte
   - Rounds 23-25: haksatna, kithatte, kiseelte, hangte, meivakkhuamte
   - Rounds 26-28: tokhom, hanciam, galkapbu, taau, puansilh, phunna
   - Rounds 29-30: gialpi, palsatin, semsem, zawt, musane, limtak
   - Rounds 31-32: kongpuankhai, vawh, baan, liangko, pataukoh, gelhsa
   - Rounds 33-34: ukpipa, vangtaang, kiphuh, phelkhia, kangtum, siahuaizaw
   - Rounds 35-36: kiliatsakna, kiselna, nuntakzia, damdam, maitai
   - Round 37: zineipa, meivakna, innteek, pianpih, zukham, thaneem

3. **Quality audits**
   - Ran allomorph_audit.py to check for over-segmentation
   - Flagged issues down from 361 to ~200
   - Coverage: 97.76% (up from 97.57%)

### Remaining Work (~2.2% = 18,606 tokens)

| Category | Est. % | Examples |
|----------|--------|----------|
| Rare vocabulary (hapax) | ~40% | dongun, veipi, utzaw |
| Complex compounds not yet handled | ~30% | kongpuankhai, puanmongteep |
| Proper nouns with unusual suffixes | ~15% | Minor biblical names |
| Dialectal/archaic forms | ~10% | Variant spellings |
| Potential loan words | ~5% | sapfaia, peel, vot |

### Philological Method Used

For each unknown/partial word:
1. Grep all Bible verses where the word occurs
2. Extract verse IDs and look up KJV English parallel
3. Infer meaning from English context
4. Verify morphological structure is consistent
5. Add to COMPOUND_WORDS with segmentation and gloss

This method ensures all entries are semantically verified against actual usage.

### Next Steps

1. [x] Continue systematic unknown word investigation (freq 6-7)
2. [ ] Push toward 98% coverage
3. [ ] Document truly unanalyzable items for future research
4. [ ] Try Henderson vocabulary extraction for remaining gaps
5. [ ] Generate Leipzig-glossed sample chapters
6. [ ] Prepare methodology for scaling to other 18 languages

---

*Last updated: 2026-03-08*
*Coverage: 97.76% fully analyzed | 1.57% partial | 0.67% unknown*
