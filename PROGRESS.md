# Kuki-Chin Corpus Project: Progress Report

## Project Overview

This project builds digital philology infrastructure for Kuki-Chin languages, focusing on:
1. Bible corpus collection and alignment (20 languages)
2. Bootstrap lexicon generation via PMI-based word alignment
3. **Morphological analysis and Leipzig-style glossing (Tedim Chin complete)**

## Tedim Chin: Current State

### Corpus Metrics (as of 2026-04)

| Metric | Value |
|--------|-------|
| Corpus tokens | 831,152 |
| Lemmas (headwords) | 7,339 |
| Senses | 9,962 |
| Grammatical morphemes | 485 |
| Linked examples | 26,898 |
| Senses with examples | 5,812 (58%) |
| Coverage (known POS) | 100.0% |


### Review Queue (Resolved)

The formal review queue tracked ambiguous wordforms needing disambiguation:

| Priority | Resolved | Description |
|----------|----------|-------------|
| High | 22 | Core function words (a, hi, na, etc.) |
| Medium | 212 | Compounds, plurals, nominalizations |
| Low | 3 | Example linking edge cases |
| **Total** | **237** | All resolved |

Each item received a documented resolution (primary POS, analysis notes).

### Live Editorial Work

Beyond the formal review queue, ongoing editorial tasks remain:

| Task | Count | Status |
|------|-------|--------|
| Polysemous lemmas | ~975 | Need context-sensitive disambiguation |
| Senses without examples | ~4,150 | 42% of senses lack corpus examples |
| Constructions layer | 0 | Not yet populated |
| Grammar topics layer | 0 | Not yet populated |

Run `make editorial-blockers` for the current prioritized work list.

### Generated Outputs

| Output | Path | Command |
|--------|------|---------|
| Metrics JSON | `output/metrics/ctd_metrics.json` | `make metrics` |
| Editorial blockers | `output/editorial_blockers.md` | `make editorial-blockers` |
| Draft dictionary | `output/dictionary/draft_dictionary.md` | `make dictionary-draft` |
| Draft grammar | `output/grammar/draft_grammar.md` | `make grammar-draft` |

### Dictionary Composition

| Category | Entries |
|----------|---------|
| Nouns | ~2,100 |
| Verbs | ~770 |
| Proper nouns | ~4,060 |
| Pronouns | ~300 |
| Function words | ~100 |

### Quality Assurance

- **53 backend tests** ensuring data integrity
- **Compound transparency audit** in `docs/compound_transparency_audit.md`
- **Polysemy disambiguation** with POLYSEMOUS_ROOTS system

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

### Phase 4: Tedim Chin Morphological Analyzer ✓ COMPLETE

**Coverage: 100%** — Production-ready Leipzig-style glossing

Key features:
- Prefix stripping: ka-, na-, a-, kong-, hong-, ki-
- Suffix handling: -na (NMLZ), -te (PL), -in (ERG), -ah (LOC), -ding (IRR)
- Stem I/II alternation: mu/muh, za/zak, thei/theih
- Reduplication: X~X patterns (zelzel → zel~RED)
- Compound analysis with transparency tracking
- Proper noun handling with suffix attachment
- Polysemy disambiguation via context

### Phase 5: Quality Audit ✓

- Compound transparency audit (`docs/compound_transparency_audit.md`)
- Opaque lexeme documentation (`docs/opaque_lexemes.md`)
- 64 regression tests (`tests/regression_tests.md`)
- Polysemy documentation for homophonous roots

### Phase 6: Bootstrap Pipeline for New Languages ✓

**Script:** `scripts/bootstrap_language.py`

To avoid repeating the painful manual process that was required for Tedim Chin,
a unified bootstrap pipeline now automates the path from a bilingual Bible corpus
to a working initial morphological analyzer in a single command.

**Key features:**
- **Automated setup** – one command runs all steps: preprocess → inventory → lexicon → analyzer → coverage → work queue
- **Work queue** – the core output: every unknown word ranked by frequency, each with up to 5 aligned English verse contexts so meanings can be inferred without manual cross-referencing
- **Initial analyzer** – pre-populated with ~5,000 entries from the bootstrap lexicon (proper nouns, function word candidates, stem candidates)
- **Coverage baseline** – immediately shows how many tokens the initial analyzer handles

**Mizo (lus) initial results:**
```
Total tokens  : 844,734
Analyzed      : 694,722  (82.24%)
Unknown types : 13,663
Work queue    : 6,318 entries (freq ≥ 2) + English contexts
```

**Usage:**
```bash
# Full pipeline (first run for a new language):
python scripts/bootstrap_language.py lus

# After manually adding words to scripts/lus_analyzer.py, re-check progress:
python scripts/bootstrap_language.py lus --steps coverage,queue
```

Outputs go to `analysis/{lang}/`:
- `{lang}.wordfreq.tsv`   – word frequency inventory
- `{lang}.coverage.txt`  – coverage report
- `{lang}.work_queue.tsv`– unknowns + English contexts (the work driver)

And to `scripts/`:
- `{lang}_analyzer.py`   – initial analyzer to iteratively enrich

## Progress Log

| Date | Coverage | Δ | Action |
|------|----------|---|--------|
| 2026-03-06 | 84.2% | - | Baseline |
| 2026-03-06 | 90.6% | +6.4 | Function words, proper nouns, stems |
| 2026-03-07 | 97.25% | +6.65 | Philological compound expansion |
| 2026-03-08 | 98.51% | +1.26 | Quality-focused vocabulary |
| 2026-03-09 | 99.00% | +0.49 | Push to 99% milestone |
| 2026-03-10 | 99.47% | +0.47 | Algorithmic suffix parsing |
| 2026-03-11 | 99.90% | +0.43 | Hyphenated compounds |
| 2026-03-13 | 99.99% | +0.09 | Architecture refactor |
| 2026-03-15 | 100.00% | +0.01 | Final vocabulary + quality audit |
| 2026-03-17 | 100.00% | - | Regression tests (64), documentation |

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/METHODOLOGY.md` | Replication guide for new languages |
| `docs/opaque_lexemes.md` | Transparent vs opaque compound decisions |
| `docs/compound_transparency_audit.md` | Audit results for compound analysis |
| `docs/LESSONS_LEARNED.md` | Error patterns and solutions |
| `docs/QUALITY_AUDIT.md` | Semantic verification methodology |
| `tests/regression_tests.md` | 64 regression tests with expected outputs |

## Philological Method

For each unknown/partial word:
1. Grep all Bible verses where the word occurs
2. Extract verse IDs and look up KJV English parallel
3. Infer meaning from English context
4. Verify morphological structure is consistent
5. Add to appropriate dictionary with segmentation and gloss

```bash
# Example: Find meaning of unknown word "ihmut"
verse=$(grep -m1 "	.*\bihmut\b" bibles/extracted/ctd/ctd-x-bible.txt | cut -f1)
grep "^$verse	" data/verses_aligned.tsv | cut -f3
# Output: "And the LORD God caused a deep sleep to fall..."
# → ihmut = "deep.sleep"
```

## Next Steps

1. ✅ Tedim Chin analyzer complete (100% coverage)
2. ✅ Bootstrap pipeline (`scripts/bootstrap_language.py`) for rapid replication
3. ✅ Backend-driven workflow (`make backend`, `make metrics`)
4. [ ] Mizo (lus) analyzer – iterate on `scripts/lus_analyzer.py` using `analysis/lus/lus.work_queue.tsv`
5. [ ] Generate Leipzig-glossed sample chapters (Matthew, Mark)
6. [ ] Scale methodology to remaining 17 Kuki-Chin languages
7. [ ] Henderson vocabulary extraction for supplementary entries
8. [ ] Build comparative dictionary across languages

---

*Last updated: 2026-04-13*  
*Run `make metrics` for current Tedim Chin statistics*  
*Mizo (lus) initial coverage: 82.24% (bootstrap pipeline)*
