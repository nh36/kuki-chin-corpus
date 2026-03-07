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
- Current coverage: **92.8%** of tokens
- Handles: prefixes, stems, suffixes, compounds

## Current Analyzer Performance

### Overall Statistics
```
Total tokens:   831,408
Glossed:        771,935 (92.8%)
Unknown:         59,473 (7.2%)
```

### Coverage by Book
| Book     | Coverage |
|----------|----------|
| John     | 95.0%    |
| Genesis  | 94.5%    |
| Luke     | 93.1%    |
| Matthew  | 93.0%    |
| Mark     | 93.0%    |
| Exodus   | 92.9%    |
| Romans   | 92.8%    |
| Psalms   | 91.4%    |
| Isaiah   | 91.1%    |

### Analyzer Components

1. **Function Words** (~100 entries)
   - Pronouns, demonstratives, particles
   - TAM markers, negation, question words

2. **Verb Stems** (~120 entries)
   - Stem I/II alternation (mu/muh, za/zak, thei/theih)
   - Motion, perception, cognition, speech, transfer verbs

3. **Noun Stems** (~150 entries)
   - Religious, social, kinship, body part terms
   - Place, time, abstract nouns

4. **Compound Words** (~300 entries)
   - Noun+LOC: tungah, sungah, kiangah
   - Verb+NMLZ: mawhna, biakna, nuntakna
   - Noun+Noun: tapa, biakinn, lungsim
   - Reflexive: kibawl, kipan, kisai

5. **Productive Morphology**
   - Prefix stripping: ka-, na-, a-, kong-, hong-, ki-
   - Suffix handling: -na (NMLZ), -te (PL), -in (ERG), -ah (LOC)

## File Structure

```
Kuki-Chin/
├── data/
│   ├── verses_aligned.tsv      # Master corpus (20 languages)
│   └── lexicons/
│       └── ctd_lexicon.tsv     # Tedim bootstrap lexicon
├── scripts/
│   ├── analyze_morphemes.py    # Leipzig analyzer (1385 lines)
│   └── lemmatizer.py           # Lemmatization module
└── literature/
    ├── RESOURCES.md            # Available secondary literature
    ├── DESIDERATA.md           # Needed resources
    └── tedim-ctd/
        └── MORPHEME_INVENTORY.md  # Morpheme documentation
```

## Remaining Unknown Categories

Analysis of the ~7% unknown tokens:

1. **Rare vocabulary** (hapax legomena, low-frequency words)
2. **Proper nouns not in list** (minor characters, places)
3. **Productive morphology** (novel compound formations)
4. **Orthographic variants** (spelling differences)

## Recommendations for Further Improvement

### To reach 95%+ coverage:

1. **Add more stems** (~200 more needed)
   - Systematic extraction of remaining high-frequency unknown stems
   - Cross-reference with Henderson 1965 vocabulary lists

2. **Improve productive decomposition**
   - Better handling of double suffixes (-na-te, -na-in)
   - Recursive prefix stripping for ki-ka-, ki-hong- combinations

3. **Handle reduplication**
   - Pattern matching for X-X forms (semsem, tuamtuam)

4. **Expand proper noun list**
   - Extract all capitalized words from corpus
   - Add minor biblical characters and places

### To reach 97%+ coverage:

5. **Integrate full Henderson vocabulary**
   - Digitize word lists from Henderson 1965
   - Add with proper stem alternation marking

6. **Add contextual disambiguation**
   - Use surrounding words to choose between homophone glosses
   - Integrate with verse-level context

## Next Steps

1. [ ] Add ~200 more verb/noun stems from frequency analysis
2. [ ] Implement recursive morphological decomposition
3. [ ] Handle reduplication patterns
4. [ ] Expand proper noun coverage
5. [ ] Begin Leipzig glossing output format
6. [ ] Create web interface for glossed text display

---

*Last updated: 2026-03-07*
*Coverage: 92.8% | Tokens: 771,935/831,408*
