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
- Demonstratives/deixis remains the protocol-backed pilot topic and is now a maintenance/human-review topic at the publication-review evidence layer.
- The negation evidence dossier at `output/publication_review/dossier_negation.md` has now been converted into a synchronized grammar slice, dictionary slice, review notes, a corrected generated-report caveat, and an analyzer-aware candidate file at `output/publication_review/candidates_negation.tsv`.
- The negation packet treats `lo`, `loh`, and `kei` as part of one negation system, and Genesis 2:25 plus the old `V lo uh` prohibitive analysis now remain blocked both in packet prose and in the new candidate layer.
- The negation candidate retrofit has now been hardened with explicit notes for analyzer/export caveats such as `Loh`/`Nadingin` export artifacts, `Nawn` as a `PROP`-like lemma/POS value, and the excluded Genesis 2:25 `uh` row.
- Negation is now a hardened retrospective retrofit under the candidate-first workflow.
- Pronouns / clusivity now also have a hardened analyzer-aware candidate file at `output/publication_review/candidates_pronouns.tsv`, with stable accepted pronoun rows, both `ko` and `kote` explicit as exclusive evidence, unresolved `ei/eite` rows, and an excluded negative `kei` false friend.
- Pronouns / clusivity now has a hardened candidate layer, with `ei/eite` still unresolved and `ko/kote` handled as exclusive evidence.
- The pronoun / clusivity retrofit exposed a systematic analyzer/export quality issue for `ko`, and that issue has now been addressed upstream in `scripts/analyze_morphemes.py` through explicit ambiguity handling, context-sensitive pronominal disambiguation, and pronoun-first POS routing in the relevant frames.
- A dedicated analyzer-quality dossier now lives at `output/publication_review/dossier_analyzer_pronoun_quality.md`, and it now records both the diagnosis and the follow-up fix while explicitly treating philological discourse evidence as the control rather than Henderson alone or the analyzer's concord table alone.
- A cross-topic analyzer-aware publication-review evidence protocol now lives at `docs/publication_review/EVIDENCE_PROTOCOL.md`.
- The evidence protocol now has a documented candidate-extraction workflow in `docs/publication_review/CANDIDATE_EXTRACTION.md`.
- Demonstratives/deixis is the pilot topic for the new candidate-extraction layer in `output/publication_review/candidates_demonstratives.tsv`, and the committed TSV is reproducible from `scripts/publication_review/extract_candidates.py`.
- A retrospective evidence-protocol audit now exists at `output/publication_review/evidence_protocol_retrofit_audit.md`.
- Earlier publication-review packets are now being checked against the newer candidate-first standard rather than treated as automatically protocol-complete.
- Stem alternation now has an analyzer-aware candidate TSV at `output/publication_review/candidates_stem_alternation.tsv`.
- Stem alternation also now has a broader corpus audit, but `output/publication_review/stem_alternation_corpus_audit.tsv` is generated locally and intentionally untracked; the tracked compact outputs are `stem_alternation_environment_summary.tsv`, `stem_alternation_pair_summary.tsv`, and `stem_alternation_example_matrix.tsv`.
- Stem alternation now has a tracked lexical inventory, promotable examples table, manual promotion review, citation shortlist, syntactic-context matrix, and pair-discussion plan.
- Stem alternation now also has a first working prose draft at `output/publication_review/grammar_stem_alternation_section_draft.md`.
- Stem alternation is now ready for human review at the current slice maturity level and should not be further polished until other slices catch up.
- Case marking has now been retrofitted through `output/publication_review/candidates_case_marking.tsv`, `output/publication_review/dossier_case_marking.md`, a curated extractor route, LF-stable reproducible candidate output, aligned grammar and dictionary slices, updated review notes, and tests protecting the main distinctions.
- Interrogatives now has `output/publication_review/candidates_interrogatives.tsv`, a curated extractor route, a first interpretive dossier at `output/publication_review/dossier_interrogatives.md`, a first grammar print slice at `output/publication_review/grammar_interrogatives_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_interrogatives_print_slice.md`, and review notes at `output/publication_review/review_notes_interrogatives.md`; the packet stays controlled by the candidate/dossier layer and is now ready for human review at the current slice maturity level.
- Numerals now has `output/publication_review/candidates_numerals.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first interpretive dossier at `output/publication_review/dossier_numerals.md`, a first grammar print slice at `output/publication_review/grammar_numerals_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_numerals_print_slice.md`, and review notes at `output/publication_review/review_notes_numerals.md`; the packet stays controlled by the candidate/dossier/print-slice layer, keeps `kua = who` blocked as a numeral false friend, keeps `khat` on the numeral/indefinite boundary, and is now ready for human review at the current slice maturity level.
- Quantifiers now has `output/publication_review/candidates_quantifiers.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first interpretive dossier at `output/publication_review/dossier_quantifiers.md`, a first grammar print slice at `output/publication_review/grammar_quantifiers_print_slice.md`, and a first dictionary print slice at `output/publication_review/dictionary_quantifiers_print_slice.md`; the packet remains controlled by the candidate/dossier/grammar layer and keeps explicit overlap controls for `khat`, `kuamah`, and bang-family `bangmah`. The quantifiers dictionary print slice now exists, but review-note work has not yet begun.
- Future print slices should use analyzer-aware candidate files before drafting grammar or dictionary prose, so dossiers start from filtered evidence rather than from raw-string cleanup.
- Demonstratives/deixis, negation, pronouns/clusivity, stem alternation, case marking, and interrogatives are now maintenance/human-review topics at the publication-review evidence layer.
- `data/ctd_analysis/tokens.tsv` remains generated local build output and is intentionally untracked, so candidate-extractor reproducibility tests skip cleanly when it is absent and regenerate locally when needed.
- The quantifiers grammar print slice now exists, but the dictionary and review-note slices have not yet begun; coordinators and sentence-final particles remain later narrow candidates, while broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
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

1. [ ] Continue the quantifiers retrofit from `dictionary_quantifiers_print_slice.md` into `review_notes_quantifiers.md` without broadening into coordinators, sentence-final particles, or broad degree/intensifier prose.
2. [ ] Keep demonstratives/deixis, negation, pronouns/clusivity, stem alternation, case marking, interrogatives, and numerals stable for maintenance and human review.
3. [ ] Keep coordinators, sentence-final particles, broad TAM, directionals, chrestomathy, Mizo/lus, and the other Kuki-Chin languages deferred while quantifiers remains the active narrow retrofit.

---

*Last updated: 2026-05-29*  
*Tedim Chin coverage: 100% (850,906 tokens)*  
*Mizo (lus) initial coverage: 82.24% (bootstrap pipeline)*
