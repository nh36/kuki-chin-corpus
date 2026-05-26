# Kuki-Chin Corpus Project: Progress Report

## Project Overview

This project builds digital philology infrastructure for Kuki-Chin languages, focusing on:
1. Bible corpus collection and alignment (20 languages)
2. Bootstrap lexicon generation via PMI-based word alignment
3. **Morphological analysis and Leipzig-style glossing (Tedim Chin complete)**

## 🎉 MILESTONE: 100% Coverage Achieved

**Date:** 2026-03-17  
**Coverage:** 100% (771,190/771,201 tokens, excluding metadata and tokenization artifacts)

The Tedim Chin morphological analyzer is now **production-ready** for Leipzig-style interlinear glossing.

### Analyzer Statistics (Current)

```
Total tokens:      771,201 (real words, excluding metadata)
Fully analyzed:    771,190 (100.00%)
Partial:                11 (tokenization artifacts only)
Unknown:                 0 (0.00%)
```

### Dictionary Size

| Category | Entries | Notes |
|----------|---------|-------|
| Function words | ~150 | Closed class (pronouns, particles, TAM) |
| Verb stems | ~2,000+ | Including Stem I/II alternations |
| Noun stems | ~800+ | Including body parts, kinship, etc. |
| Compound words | ~3,500+ | Pre-analyzed transparent compounds |
| Proper nouns | ~2,500+ | Biblical names with suffix handling |
| Atomic glosses | ~300+ | Compositional elements |
| **Total entries** | **~7,000+** | In `scripts/analyze_morphemes.py` |

### Quality Assurance

- **64 regression tests** in `tests/regression_tests.md`
- **Compound transparency audit** in `docs/compound_transparency_audit.md`
- **Opaque lexeme documentation** in `docs/opaque_lexemes.md`
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

## Recent Tedim publication-review work

- The case-marking grammar/dictionary review packet is now the editorial model for Tedim print-facing slices.
- The pronoun grammar slice, dictionary slice, and review notes have been created in `output/publication_review/`.
- A separate pronoun clusivity dossier has been created at `output/publication_review/dossier_pronoun_clusivity.md`.
- A safe partial correction is now in place: `ko/kote` is treated as exclusive, while `ei/eite` remains under review pending further evidence.
- The pronoun slice is now polished enough to serve as the model for the next print-facing grammar-and-dictionary section, provided the unresolved `ei/eite` question stays explicitly flagged.
- A third print-review packet on verb stem alternation has now been expanded and synchronized in `output/publication_review/` with a grammar slice, a dictionary slice, review notes, and a supporting evidence dossier.
- The stem-alternation packet treats case-marking and pronouns as completed editorial models, argues that the Form I / Form II contrast is real, and now includes a Bible-corpus coverage table plus cautious `za ~ zak` and `nusia ~ nusiat` expansions.
- The negation evidence dossier at `output/publication_review/dossier_negation.md` has now been converted into a synchronized grammar slice, dictionary slice, review notes, a corrected generated-report caveat, and an analyzer-aware candidate file at `output/publication_review/candidates_negation.tsv`.
- The negation packet treats `lo`, `loh`, and `kei` as part of one negation system, and Genesis 2:25 plus the old `V lo uh` prohibitive analysis now remain blocked both in packet prose and in the new candidate layer.
- The negation candidate retrofit has now been hardened with explicit notes for analyzer/export caveats such as `Loh`/`Nadingin` export artifacts, `Nawn` as a `PROP`-like lemma/POS value, and the excluded Genesis 2:25 `uh` row.
- Demonstratives/deixis remains the protocol pilot topic, while negation is now the first retrospective retrofit under the candidate-first workflow.
- Pronouns / clusivity now also have a hardened analyzer-aware candidate file at `output/publication_review/candidates_pronouns.tsv`, with stable accepted pronoun rows, both `ko` and `kote` explicit as exclusive evidence, unresolved `ei/eite` rows, and an excluded negative `kei` false friend.
- The pronoun candidate layer intentionally preserves the unresolved `ei/eite` issue instead of forcing a global inclusive/exclusive label from analyzer export alone.
- A cross-topic analyzer-aware publication-review evidence protocol now lives at `docs/publication_review/EVIDENCE_PROTOCOL.md`.
- The evidence protocol now has a documented candidate-extraction workflow in `docs/publication_review/CANDIDATE_EXTRACTION.md`.
- Demonstratives/deixis is the pilot topic for the new candidate-extraction layer in `output/publication_review/candidates_demonstratives.tsv`, and the committed TSV is reproducible from `scripts/publication_review/extract_candidates.py`.
- A retrospective evidence-protocol audit now exists at `output/publication_review/evidence_protocol_retrofit_audit.md`.
- Earlier publication-review packets are now being checked against the newer candidate-first standard rather than treated as automatically protocol-complete.
- Demonstratives is already protocol-backed, and negation now has a hardened analyzer-aware candidate layer with caveats documented rather than hidden.
- Pronouns / clusivity is now a hardened retrospective retrofit, and `ei/eite` remains explicitly unresolved even after the added `ko/kote` evidence.
- Future print slices should use analyzer-aware candidate files before drafting grammar or dictionary prose, so dossiers start from filtered evidence rather than from raw-string cleanup.
- With the pronoun candidate layer now hardened, the next retrofit step can be stem alternation.
- Chrestomathy work and all Mizo/lus work remain deferred while the Tedim publication-review sequence continues one narrow slice at a time.

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

1. [ ] Begin the stem alternation retrofit now that the pronoun / clusivity candidate layer has been hardened.
2. [ ] Keep broad TAM, directionals, chrestomathy, Mizo/lus, and the other Kuki-Chin languages deferred while the Tedim packet is expanded one narrow topic at a time.
3. [ ] Keep the unresolved `ei/eite` question flagged in any later person-marking work unless new evidence settles it.

---

*Last updated: 2026-05-26*  
*Tedim Chin coverage: 100% (850,906 tokens)*  
*Mizo (lus) initial coverage: 82.24% (bootstrap pipeline)*
