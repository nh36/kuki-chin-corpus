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
- Case marking is now the fifth normalized coverage section after numerals, quantifiers, NP structure / possession, and noun domain: `output/publication_review/grammar_case_marking_print_slice.md` has been expanded into a publication-facing section with a compact inventory, controlled OT/Gospel examples, explicit relator/possession/transitivity boundaries, and a checked normalization supplement at `output/publication_review/examples_case_marking_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the expanded case marking section, while preserving the review-preview framing and non-final warnings.
- Coverage normalization has paused for now so the assembled grammar review preview can be pushed toward a more grammar-facing draft style rather than simply widening section coverage.
- A grammar-facing PDF style pass has begun: `scripts/assemble_publication_review_preview.py` now builds the committed review preview in grammar-facing mode, with numbered sections, lighter front matter, and grammar-oriented TeX quote handling.
- The assembler now suppresses internal apparatus such as Scope sections and source-slice markers in the normalized nominal-domain chapters and enforces grammar-style presentation there, including inline Tedim gloss quoting and preserved object-language italics in the rebuilt Markdown, TeX, and PDF preview outputs.
- Coverage normalization is now explicitly paused while the current normalized sections are held to grammar-facing publication checks rather than widened further.
- A hard grammar-facing quality gate now exists at `scripts/grammar_pdf_quality_gate.py`, with a companion report at `output/publication_review/grammar_facing_quality_report.md`.
- The committed assembled review preview is now generated in grammar-facing mode and must pass the source, blank-section, workflow-prose, gloss, quote, and subsection-example checks before commit.
- New sections must pass these grammar-facing style and source-reference checks before they are committed into the assembled preview.
- The grammar-facing quality gate has now been strengthened further rather than widened to another normalized topic.
- The grammar-facing quality gate now enforces stricter per-construction example-balance expectations, so substantive subsections default to paired Old Testament and Gospel formal examples unless a grammar-facing explanation is stated.
- Source references after examples are now enforced from example metadata, immediately preceding prose, normalization TSV supplements, and Bible-text inference, with conflicting sources treated as hard failures.
- In-text Tedim glossing in the normalized sections is now glossary-linted against the generated grammar-facing TeX rather than treated as a loose prose preference.
- One-example subsections and blank sections are now blocked in grammar-facing mode unless they carry a real grammar-facing explanation or other substantive content.
- Coverage normalization remains paused until the already-normalized sections pass these stricter grammar-facing checks.
- The grammar-facing quality gate is now good enough to resume coverage normalization without weakening the review-preview guardrails.
- Relators / postpositions is now the next normalized section after case marking, with a grammar-facing inventory, paired OT/Gospel examples, and explicit case-marking and NP-boundary prose.
- The assembled grammar review preview PDF has been rebuilt with the normalized relators / postpositions section while keeping the review-preview framing and non-final warnings.
- Interrogatives is now the next normalized section after demonstratives and deixis: `output/publication_review/grammar_interrogatives_print_slice.md` has been rewritten as grammar-facing prose with a compact interrogative inventory, controlled formal examples, explicit boundary/deferred treatment, and a rebuilt preview PDF under the hard gate.
- Sentence-final particles is now the next normalized section after interrogatives: `output/publication_review/grammar_sentence_final_particles_print_slice.md` has been rewritten as grammar-facing prose with a compact inventory, controlled OT/Gospel formal examples for `ahi hi`, `lo hi`, `hen`, `in`, and `un`, and explicit boundary/deferred treatment for `hiam`, `aw`, `tahen`, `ta`, and `zo`.
- The assembled grammar review preview PDF has been rebuilt with the normalized sentence-final particles section while keeping the review-preview framing and non-final warnings.
- Negation is now the next normalized section after sentence-final particles: `output/publication_review/grammar_negation_print_slice.md` has been rewritten as grammar-facing prose with a compact negation inventory, paired Old Testament and Gospel formal examples across core constructions, and explicit deferred boundaries.
- The assembled grammar review preview PDF has been rebuilt with the normalized negation section while keeping the review-preview framing and non-final warnings.
- `scripts/run_publication_review_checks.py` remains the standard one-command validation workflow for publication-review checks.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized sentence-final particles section is committed only after the rebuilt review preview passes that hard gate.
- Numerals now has `output/publication_review/candidates_numerals.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first interpretive dossier at `output/publication_review/dossier_numerals.md`, a first grammar print slice at `output/publication_review/grammar_numerals_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_numerals_print_slice.md`, and review notes at `output/publication_review/review_notes_numerals.md`; the packet stays controlled by the candidate/dossier/print-slice layer, keeps `kua = who` blocked as a numeral false friend, keeps `khat` on the numeral/indefinite boundary, and is now ready for human review at the current slice maturity level.
- Quantifiers now has `output/publication_review/candidates_quantifiers.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first interpretive dossier at `output/publication_review/dossier_quantifiers.md`, a first grammar print slice at `output/publication_review/grammar_quantifiers_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_quantifiers_print_slice.md`, and review notes at `output/publication_review/review_notes_quantifiers.md`; the packet remains controlled by the candidate/dossier/grammar layer and keeps explicit overlap controls for `khat`, `kuamah`, and bang-family `bangmah`. The quantifiers review notes now exist and the quantifiers packet is ready for human review at the current slice maturity level.
- Coordinators now has `output/publication_review/candidates_coordinators.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first candidate-controlled dossier at `output/publication_review/dossier_coordinators.md`, a first grammar print slice at `output/publication_review/grammar_coordinators_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_coordinators_print_slice.md`, and review notes at `output/publication_review/review_notes_coordinators.md`; the packet remains narrow, with `le` as the NP anchor, explicit `leh` and `a` overlap controls, deferred lexical-export `mawh`, and caveated `ahih hangin` / `ahih kei leh` boundary rows. The coordinators packet is now ready for human review at the current slice maturity level.
- Coordinators has now been normalized in the grammar-facing chapter pass, and reduplication has now been normalized as the next section with a compact inventory, OT/Gospel formal examples for `mahmah` and `taktak` plus secondary `peuhpeuh`, and explicit boundary controls for `ni ni`, `leuleu`, and deferred expressive/report-only rows.
- A post-normalization coverage/status checkpoint now exists at `output/publication_review/post_normalization_coverage_checkpoint.md`, and the next batch is a source-balance/stale-prose review rather than another first-pass packet.
- A consistency-drift and invariant audit now exists for the assembled grammar review preview.
- Sentence-final particles now has `output/publication_review/candidates_sentence_final_particles.tsv`, curated extractor support in `scripts/publication_review/extract_candidates.py`, a first candidate-controlled dossier at `output/publication_review/dossier_sentence_final_particles.md`, a first grammar print slice at `output/publication_review/grammar_sentence_final_particles_print_slice.md`, a first dictionary print slice at `output/publication_review/dictionary_sentence_final_particles_print_slice.md`, and review notes at `output/publication_review/review_notes_sentence_final_particles.md`; the packet remains narrow, with `ahi hi` and `lo hi` as caveated declarative overlap rows, `hiam` kept as interrogatives-overlap control, `hen` / `in` / `un` kept construction-bound, and `aw` / `tahen` / `ta` / `zo` kept as caveated boundary material. The packet is now ready for human review at the current slice maturity level.
- A compact human-review handoff now exists at `output/publication_review/human_review_handoff.md`; it is a reviewer-orientation index only and does not start a new linguistic packet.
- A final publication-review packet-integrity check now exists at `tests/test_publication_review_packet_integrity.py`.
- Directionals is now the next normalized section after relators / postpositions. `output/publication_review/grammar_directionals_print_slice.md` has been expanded into a grammar-facing section with a compact directional inventory, controlled Old Testament and Gospel formal examples where the evidence allows them, explicit deictic and TAM/VP-structure boundaries, and a checked normalization supplement at `output/publication_review/examples_directionals_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized directionals section while keeping the review-preview framing and non-final warnings.
- TAM / aspect / modal is now the next normalized section after directionals. `output/publication_review/grammar_tam_print_slice.md` has been expanded into a grammar-facing section with a compact TAM inventory, controlled Old Testament and Gospel formal examples across the safe anchors, explicit negation/sentence-final and directional/VP-structure boundary prose, and a checked normalization supplement at `output/publication_review/examples_tam_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized TAM section while keeping the review-preview framing and non-final warnings.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized TAM section is committed only after the rebuilt review preview passes that hard gate.
- VP structure / suffix stacking is now the next normalized section after TAM. `output/publication_review/grammar_vp_structure_stacking_print_slice.md` has been expanded into a grammar-facing section with a compact stacking inventory, controlled Old Testament and Gospel formal examples where the evidence allows them, and explicit TAM/directional, modal/negation, derivational, and clause-linkage boundary prose, together with a checked normalization supplement at `output/publication_review/examples_vp_structure_stacking_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized VP structure / suffix stacking section while keeping the review-preview framing and non-final warnings.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized VP structure / suffix stacking section is committed only after the rebuilt review preview passes that hard gate.
- Derivation / valency is now the next normalized section after VP structure / suffix stacking. `output/publication_review/grammar_derivation_valency_print_slice.md` has been expanded into a grammar-facing section with a compact derivation inventory, controlled Old Testament and Gospel formal examples around `paisak`, `muhsak`, and `ciahsakkik`, and explicit `-pih`, `ki-`, VP-stacking, and transitivity boundary prose, together with a checked normalization supplement at `output/publication_review/examples_derivation_valency_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized derivation / valency section while keeping the review-preview framing and non-final warnings.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized derivation / valency section is committed only after the rebuilt review preview passes that hard gate.
- Transitivity is now the next normalized section after derivation / valency. `output/publication_review/grammar_transitivity_print_slice.md` has been expanded into a grammar-facing section with a compact transitivity inventory, controlled Old Testament and Gospel formal examples around `sih`, `suak`, `en`, and the `mu / muh` boundary, plus a cautious `hawl` row and explicit stem-alternation, derivation, case, and prefix boundary prose, together with a checked normalization supplement at `output/publication_review/examples_transitivity_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized transitivity section while keeping the review-preview framing and non-final warnings.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized transitivity section is committed only after the rebuilt review preview passes that hard gate.
- Stem alternation is now the next normalized section after transitivity. `output/publication_review/grammar_stem_alternation_print_slice.md` has been expanded into a grammar-facing section with a controlled Form I / Form II overview, distribution-by-context discussion, core and promoted pair coverage, and explicit difficult/blocked boundary treatment, together with a checked normalization supplement at `output/publication_review/examples_stem_alternation_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized stem alternation section while keeping the review-preview framing and non-final warnings.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized stem alternation section is committed only after the rebuilt review preview passes that hard gate.
- Nominalization is now the next normalized section after stem alternation. `output/publication_review/grammar_nominalization_print_slice.md` has been expanded into a grammar-facing section with a compact nominalization inventory, controlled Old Testament and Gospel formal examples, explicit stem-alternation and clause/case boundary treatment, and a checked normalization supplement at `output/publication_review/examples_nominalization_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized nominalization section while keeping the review-preview framing and non-final warnings.
- Publication-review validation is now centralized in `scripts/run_publication_review_checks.py`, so the standard one-command workflow is `python3 scripts/run_publication_review_checks.py`.
- `scripts/run_publication_review_checks.py` remains the standard one-command validation workflow for publication-review checks.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized nominalization section is committed only after the rebuilt review preview passes that hard gate.
- Relators / postpositions now has review notes as well as its candidate-first scoping layer, grammar slice, and dictionary slice: `output/publication_review/candidates_relators_postpositions.tsv`, `output/publication_review/dossier_relators_postpositions_scope.md`, `output/publication_review/grammar_relators_postpositions_print_slice.md`, `output/publication_review/dictionary_relators_postpositions_print_slice.md`, and `output/publication_review/review_notes_relators_postpositions.md` now keep the packet relator-led and case-boundary-controlled around `kiang`, `lak`, `sung`, `tung`, cautiously `pualam`, and boundary-controlled `pan`, `panin`, and `tawh`, while leaving `nuai`, `mai`, `tawhin`, raw report counts, and `kipan` / `kipanin` out of the first core slice.
- A whole-grammar coverage audit now exists at `output/publication_review/whole_grammar_coverage_audit.md`; it makes explicit that the current publication-review packets are complete only for the domains already lifted into `output/publication_review/`, while broader Tedim architecture domains such as phonology/tone, NP structure, possession, VP structure, derivation/valency, nominalization, and clause-linkage domains still need a coverage/priority decision before any printable full grammar bundle is assembled.
- VP structure / suffix stacking now has review notes at `output/publication_review/review_notes_vp_structure_stacking.md` as well as its candidate TSV, scoping dossier, and grammar print slice. The packet is now complete at its current constructional maturity level without an ordinary dictionary slice, because the safe first-slice claim is about suffix ordering rather than a lexical headword: `bawlzoding` remains the central print-usable-with-caveat aspect-plus-irrealis anchor, `bawlzo` and `pokhia` remain already-owned baseline rows, and `khia-ta`, `khiathei ding om lo`, `dingin`, `ciahsakkik`, `bawlsakthei`, and `paikhiatsak` remain overlap or deferred material.
- Derivation / valency now has a candidate TSV, a scoping dossier, a narrow grammar print slice, and review notes at `output/publication_review/candidates_derivation_valency.tsv`, `output/publication_review/dossier_derivation_valency_scope.md`, `output/publication_review/grammar_derivation_valency_print_slice.md`, and `output/publication_review/review_notes_derivation_valency.md`. The packet is now ready for human review at its current `-sak` slice maturity level without a dictionary slice: `paisak` remains the causative anchor, `muhsak` remains the benefactive or applicative-like split row, the Form I plus `-sak` versus Form II plus `-sak` contrast remains protected by `tests/test_sak_caus_benf.py`, and `paipih`, `kisep`, `kigen`, `ciahsakkik`, `bawlsakthei`, `paikhiatsak`, `piangsak`, and `mipihte` remain boundary or deferred material while the `-sak` lexical split waits for human/editorial review.
- Pronominal prefixes / agreement / object-prefix systems now also has review notes at `output/publication_review/review_notes_prefix_agreement.md`, so the first prefix/agreement packet is complete at its current routing-slice maturity level without a dictionary slice. The current packet stays tightly limited to agreement-versus-possession routing: `kanei` remains the verbal agreement anchor (`ka-nei`, `1SG-have`), `kainn` remains the nominal possessive-routing anchor (`ka-inn`, `1SG.POSS-house`), `tests/test_prefix_agr_poss.py` remains the regression control, and `ainn`, `ipai`, `hongmu`, `kongmu`, `kipan`, apostrophe possession, broader possessor syntax, and broader pronoun/clusivity paradigms remain boundary or deferred material rather than being widened into a full agreement, possession, inverse, or pronoun chapter.
- Clause linkage now has review notes at `output/publication_review/review_notes_clause_linkage.md` as well as its candidate TSV, scoping dossier, and narrow grammar print slice. The packet is now ready for human review at its current temporal-subordination slice maturity level without a dictionary slice: `ciangin` remains the temporal subordination anchor, `tua ciangin` / `ciang-in` remain the clearest controlled form and segmentation, `dingin` remains only a caveated clause-bound purposive or irrealis overlap row, and `VERB-in`, `ngenin`, `ahih ciangin`, `a bawl mi`, `omna`, `muhna-ah`, `leh`, `hangin`, `bangin`, and broader complex-sentence claims remain boundary or deferred material rather than being widened into a full clause-linkage chapter.
- Prefix / agreement is now the next normalized section after clause linkage. `output/publication_review/grammar_prefix_agreement_print_slice.md` has been expanded into a grammar-facing section with a compact prefix-routing inventory, controlled Old Testament and Gospel formal examples around `kanei` / `ka-nei` and `kainn` / `ka-inn`, and explicit pronoun, relative-clause, object-prefix/inverse-like, `ki-`, and apostrophe-possession boundary prose, together with a checked normalization supplement at `output/publication_review/examples_prefix_agreement_normalization.tsv`.
- The assembled grammar review preview PDF has been rebuilt with the normalized prefix / agreement section while keeping the review-preview framing and non-final warnings.
- `scripts/run_publication_review_checks.py` remains the standard one-command validation workflow for publication-review checks.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized prefix / agreement section is committed only after the rebuilt review preview passes that hard gate.
- Pronouns / pronominal marking is now the next normalized section after prefix / agreement. `output/publication_review/grammar_pronouns_print_slice.md` has been rewritten as grammar-facing prose with a compact personal-pronoun inventory, controlled formal examples, and explicit boundary/deferred treatment.
- The assembled grammar review preview PDF has been rebuilt with the normalized pronouns / pronominal marking section while keeping the review-preview framing and non-final warnings.
- `scripts/run_publication_review_checks.py` remains the standard one-command validation workflow for publication-review checks.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized pronouns / pronominal marking section is committed only after the rebuilt review preview passes that hard gate.
- Demonstratives and deixis is now the next normalized section after pronouns / pronominal marking. `output/publication_review/grammar_demonstratives_print_slice.md` has been rewritten as grammar-facing prose with a compact demonstrative inventory, controlled formal examples, and explicit boundary/deferred treatment.
- The assembled grammar review preview PDF has been rebuilt with the normalized demonstratives and deixis section while keeping the review-preview framing and non-final warnings.
- `scripts/run_publication_review_checks.py` remains the standard one-command validation workflow for publication-review checks.
- The grammar-facing quality gate remains mandatory for new normalized sections, and the normalized demonstratives and deixis section is committed only after the rebuilt review preview passes that hard gate.
- Nominalization now has review notes at `output/publication_review/review_notes_nominalization.md` as well as its candidate TSV, scoping dossier, and narrow grammar print slice. The packet is now ready for human review at its current `-na` slice maturity level without a dictionary slice: `-na` remains the productive deverbal nominalization anchor, `bawlna` remains the controlled form, `bawl-na` remains the segmentation, `make-NMLZ / making, creation` remains the controlled gloss/function, and `bawlpa`, `hong pai mi`, `omna`, `muhna-ah`, `kumpipa`, `Topa`, `a bawl mi`, bare `na`, and report-only counts remain boundary or deferred material rather than being widened into a full nominalization chapter.
- NP structure / possession now has review notes at `output/publication_review/review_notes_np_possession.md` as well as its candidate TSV, scoping dossier, and narrow grammar print slice. The packet is now ready for human review at its current basic-NP-ordering slice maturity level without a dictionary slice: `hih mite` remains the demonstrative-before-noun anchor with `hih mi-te` / `PROX person-PL`, `mi khat` remains the head-noun plus numeral anchor with `person one`, and `mi khempeuh` remains the head-noun plus quantifier anchor with `mi khem-peuh` / `person all`, while `ka pa`, `Topa' inn`, `a pa' inn`, `Topa' tungah`, `ka suahna leitang`, isolated prefix surfaces, pronoun-led possessor rows, `-á`, report-only counts, and any broad noun-phrase, possession, prefix/agreement, case, relator, or recursive possession claim remain boundary or deferred material rather than being widened into a full noun-phrase or possession chapter.
- The noun domain now has a first candidate-scoping packet at `output/publication_review/candidates_noun_domain.tsv` plus `output/publication_review/dossier_noun_domain_scope.md`. The current packet keeps `gam` and `aksi / aksi-te` as the cleanest simple-noun anchors, keeps `minam` and `thugen` visible as transparent-compound candidates, keeps `sanggam`, `singnai`, and `kholhna` explicit as opaque or boundary-heavy compound material, keeps `Abraham` visible as the cleanest proper-name row while holding `Topa` as title-like boundary material, and recommends a narrow simple-noun-stem grammar slice as the safest next print-facing step rather than a broad noun chapter, a compound overview, or a proper-noun chapter.
- The noun domain now also has a first narrow grammar print slice at `output/publication_review/grammar_noun_domain_print_slice.md`. The current print-facing claim stays tightly limited to simple free noun stems: `gam` is the main anchor, `gam-te`, `gam-'`, `gam-in`, `gam-ah`, and `gam-te-ah` remain the controlled plural and case-like evidence, and `aksi / aksi-te` remains the supporting plural row, while `minam`, `thugen`, `singnai`, `sanggam`, `kholhna`, `Abraham`, `Topa`, `lamethuai`, possessor syntax, pronoun-led or person-head material, relator/postposition or case-dominated noun rows, and broader noun-domain claims remain boundary or deferred material rather than being widened into a full noun, compound, or proper-noun chapter.
- The noun domain now also has review notes at `output/publication_review/review_notes_noun_domain.md`, so the packet is complete at its current simple-noun-stem slice maturity level without a dictionary slice. The packet is now ready for human review as a grammar-facing noun-domain foundation: `gam` remains the main simple free noun stem anchor, `gam-te`, `gam-'`, `gam-in`, `gam-ah`, and `gam-te-ah` remain the controlled plural and case-like evidence, `aksi / aksi-te` remains the supporting plural row, and `minam`, `thugen`, `singnai`, `lamethuai`, `sanggam`, `kholhna`, `Abraham`, `Topa`, `Topa' inn`, pronoun-led or person-head material, relator/postposition or case-dominated noun rows, analyzer-noisy rows, report-only counts, and any broad noun, compound, proper-noun, or dictionary/chrestomathy routing claim remain boundary or deferred material.
- Reduplication now has a first candidate-scoping packet at `output/publication_review/candidates_reduplication.tsv` plus `output/publication_review/dossier_reduplication_scope.md`. The current packet keeps `mahmah` as the clearest full-reduplication anchor, keeps `taktak` and `peuhpeuh` visible as the strongest productive-looking support rows, and keeps `ni ni`, `leuleu`, `gengen`, `kawikawi`, and `theithei` explicit as syntactic, TAM/VP-boundary, verbal, lexicalized-looking, or report-only reduplication material; the safest next print-facing sub-scope is now a very narrow full-reduplication grammar slice led by `mahmah` rather than an aspectual or lexicalized reduplication chapter.
- Reduplication now also has a first narrow grammar print slice at `output/publication_review/grammar_reduplication_print_slice.md`. The current print-facing claim stays tightly limited to full reduplication used in intensification: `mahmah` with `mah~mah` and `EMPH~EMPH / very, truly` is the main anchor, `pha mahmah hi` is the supported worked example, `taktak` with `tak~tak` and `TRUE~TRUE / truly, certainly` remains the closest support row, and `peuhpeuh` with `peuh~peuh` and `each~each / every, each` remains only secondary distributive evidence, while `ni ni`, `leuleu`, `gengen`, `kawikawi`, `theithei`, report-only table rows, analyzer-noisy or whole-system claims, and any broad derivation or dictionary claim remain boundary or deferred material rather than being widened into a full reduplication chapter.
- Reduplication now also has review notes at `output/publication_review/review_notes_reduplication.md`, so the packet is complete at its current full-reduplication-intensifier slice maturity level without a dictionary slice. The packet is now ready for human review as a grammar-facing constructional packet: `mahmah` with `mah~mah` and `EMPH~EMPH / very, truly` remains the main intensifier anchor, `pha mahmah hi` remains the worked example, `taktak` with `tak~tak` and `TRUE~TRUE / truly, certainly` remains the closest support row, `peuhpeuh` with `peuh~peuh` and `each~each / every, each` remains only secondary distributive evidence, and `ni ni`, `leuleu`, `gengen`, `kawikawi`, `theithei`, `bangbang`, `bekbek`, `zenzen`, `tuamtuam`, analyzer-noisy rows, whole-system claims, and any broad derivation or dictionary-entry claim remain boundary or deferred material. Before opening another new packet, the next editorial step should now be a whole-grammar coverage checkpoint so the remaining gaps can be reassessed at the same maturity level.
- That whole-grammar coverage checkpoint now exists at `output/publication_review/whole_grammar_coverage_checkpoint_after_reduplication.md`. Its current recommendation is to hold the narrow review-note packets stable for human review and open transitivity next as a candidate/scoping packet, because phonology/tone remains more blocked and theory-heavy while transitivity is still report-backed but unpacketized.
- Transitivity now has a first candidate-scoping packet at `output/publication_review/candidates_transitivity.tsv` plus `output/publication_review/dossier_transitivity_scope.md`. The current packet keeps `sih` and `suak` as the safest current intransitive anchors, keeps `hawl` and `en` as the cleanest current transitive rows, and keeps `mu` / `muh`, `nei` / `neih`, `pia`, `tom`, and `piangsak` explicit as stem-alternation, prefix/agreement, case-marking, or derivation/valency boundary material; the safest next print-facing sub-scope is now a narrow clean intransitive/transitive contrast rather than an ambitransitive or full verb-class chapter.
- Transitivity now also has a first narrow grammar print slice at `output/publication_review/grammar_transitivity_print_slice.md`. The current print-facing claim stays tightly limited to a clean intransitive/transitive contrast: `sih / die` is the clean intransitive anchor, `suak / become` remains supporting intransitive evidence, `hawl / seek` is the clean transitive anchor, and `en / look.at` remains only supporting transitive evidence, while `mu / muh`, `za / zak`, `nei / neih`, `ngai / ngaih`, `piangsak`, `pia`, `gen`, `tom`, `hong`, `ki`, `dawt`, `bei`, `pia(k)sak`, case-dominated rows, derivation-heavy rows, prefix/agreement-heavy rows, and analyzer-noisy, lexicalized, report-only, or whole-system verb-class claims remain boundary or deferred material rather than being widened into a full valency or verb-class chapter. The next step should be transitivity review notes rather than a dictionary slice.
- Transitivity now also has review notes at `output/publication_review/review_notes_transitivity.md`, so the current packet is complete at its clean-contrast slice maturity level without a dictionary slice. The packet is grammar-facing and argument-structure-oriented rather than lexical: `sih / die` remains the clean intransitive anchor, `suak / become` remains supporting intransitive evidence, `hawl / seek` remains the clean transitive anchor, `en / look.at` remains supporting transitive evidence, and `mu / muh`, `za / zak`, `nei / neih`, `ngai / ngaih`, `piangsak`, `pia`, `gen`, `tom`, `hong`, `ki`, `dawt`, `bei`, `pia(k)sak`, case-dominated rows, derivation-heavy rows, prefix/agreement-heavy rows, and analyzer-noisy, lexicalized, report-only, or whole-system verb-class claims remain boundary or deferred material. The next editorial step should be a second whole-grammar coverage checkpoint after transitivity rather than a dictionary slice or immediate second-pass expansion.
- That second whole-grammar coverage checkpoint now exists at `output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md`. Its current recommendation is to hold the publication-review packet set stable for human review rather than opening another first-pass packet or second-pass expansion immediately, because phonology/tone remains blocked, verb paradigms and broader discourse remain only partly packet-shaped, and no remaining report-backed non-blocked domain is currently comparable to transitivity as a new candidate-first packet.
- The assembled review preview now exists as a real inline draft at `output/publication_review/assembled_grammar_review_preview.md`, with companion LaTeX and PDF outputs at `output/publication_review/assembled_grammar_review_preview.tex` and `output/publication_review/assembled_grammar_review_preview.pdf`. It is still explicitly a review preview rather than a finished grammar or final publication PDF, but it now inlines the actual current grammar print-slice prose in grammar order, keeps source-slice lines and the narrow anchors `bawlzoding`, `-sak`, `kanei / kainn`, `ciangin`, `-na / bawlna`, `hih mite`, `mi khat`, `mi khempeuh`, `gam`, `aksi / aksi-te`, `mahmah / taktak` with secondary `peuhpeuh`, and `sih / suak` versus `hawl / en`, and marks phonology/tone, verb paradigms, broader discourse, and analyzer-gap topics as explicit major gaps. The preview is reproducible with `python3 scripts/assemble_publication_review_preview.py`, which assembles the Markdown, generates the TeX source through Pandoc with natbib/BibTeX citation processing, routes slice example blocks through the shared `scripts/interlinear_latex.py` analyzer and gb4e machinery, keeps source references systematically after the free translation, now enriches headerless Bible examples with inferred verse references before TeX generation so the source audit catches them upstream, adds the shared abbreviations section, italicizes Tedim object-language tiers and publication-facing inline Tedim forms while leaving technical paths and commands monospace, and builds the review-preview PDF with XeLaTeX.
- Coverage normalization planning now has `output/publication_review/coverage_normalization_audit.md` plus `tests/test_coverage_normalization_audit.py`. The project has moved from packet completion and preview assembly to chapter-by-chapter coverage normalization planning, using `assembled_grammar_review_preview.md`, `whole_grammar_coverage_checkpoint_after_transitivity.md`, `whole_grammar_coverage_audit.md`, `GRAMMAR_SOURCE_INVENTORY.md`, `SKELETON_GRAMMAR.md`, and `PROGRESS.md` as controlling sources. The audit keeps the review-preview warnings in place, treats numerals as the first pilot for a fuller homogeneous section standard, and keeps phonology/tone plus verb paradigms visible as major gaps rather than pretending the grammar is finished.
- Coverage normalization has now begun in the publication-facing grammar itself. Numerals is the first pilot normalized section: `grammar_numerals_print_slice.md` now includes a real inventory table, multiple controlled interlinear examples, a checked Old Testament/Gospel source-balance supplement at `examples_numerals_normalization.tsv`, explicit ambiguity controls for `kua` and `khat`, and a fuller publication-facing discussion of decimal composition, ordinals, counting phrases, classifier-like material, and deferred distributive reduplication. The assembled grammar review preview PDF has been rebuilt with that expanded numerals section while still remaining a review preview rather than a finished grammar.
- Quantifiers is now the second normalized coverage section after numerals. `grammar_quantifiers_print_slice.md` has been expanded from a narrow packet slice into a fuller publication-facing section with a compact quantifier inventory, multiple controlled interlinear examples, explicit noun-phrase/negation/boundary discussion, and a checked Old Testament/Gospel source-balance supplement at `examples_quantifiers_normalization.tsv`. The assembled grammar review preview PDF has been rebuilt with the expanded quantifiers section while still remaining a review preview rather than a finished grammar.
- NP structure / possession is now the third normalized coverage section after numerals and quantifiers. `grammar_np_possession_print_slice.md` has been expanded from a narrow packet slice into a fuller publication-facing section with an NP pattern inventory, multiple controlled interlinear examples, an OT/Gospel source-balance supplement at `examples_np_possession_normalization.tsv`, explicit demonstrative/numeral/quantifier NP-order discussion, and a cautious possession subsection that keeps broader genitive, relator, and possessive-paradigm issues deferred. The assembled grammar review preview PDF has been rebuilt with the expanded NP structure / possession section while still remaining a review preview rather than a finished grammar.
- Noun domain is now the fourth normalized coverage section after numerals, quantifiers, and NP structure / possession. `grammar_noun_domain_print_slice.md` has been expanded from a narrow packet slice into a fuller publication-facing section with a noun-domain inventory, multiple controlled interlinear examples, a checked OT/Gospel source-balance supplement at `examples_noun_domain_normalization.tsv`, and explicit proper-name, compound, and nominalization boundary notes. The assembled grammar review preview PDF has been rebuilt with the expanded noun domain section while still remaining a review preview rather than a finished grammar.
- Future print slices should use analyzer-aware candidate files before drafting grammar or dictionary prose, so dossiers start from filtered evidence rather than from raw-string cleanup.
- Demonstratives/deixis, negation, pronouns/clusivity, stem alternation, and case marking are now maintenance/human-review topics at the publication-review evidence layer, while interrogatives has already been normalized.
- `data/ctd_analysis/tokens.tsv` remains generated local build output and is intentionally untracked, so candidate-extractor reproducibility tests skip cleanly when it is absent and regenerate locally when needed.
- The quantifiers packet is now ready for human review at the current slice maturity level; the coordinators review notes now exist and the coordinators packet is now ready for human review at the current slice maturity level; the sentence-final particles review notes now exist and the sentence-final particles packet is now ready for human review at the current slice maturity level; the directionals review notes now exist, so the directionals packet is also ready for human review at the current slice maturity level; and broad TAM now has review notes too, so the TAM packet is now ready for human review at the current slice maturity level. Chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
- The quantifiers packet is now ready for human review at the current slice maturity level; the coordinators review notes now exist and the coordinators packet is now ready for human review at the current slice maturity level; the sentence-final particles review notes now exist and the sentence-final particles packet is now ready for human review at the current slice maturity level; the directionals review notes now exist, so the directionals packet is also ready for human review at the current slice maturity level; broad TAM now has review notes too, so the TAM packet is now ready for human review at the current slice maturity level; and relators / postpositions now has review notes too, so that packet is also ready for human review at the current slice maturity level. Chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
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

1. [ ] Keep demonstratives/deixis, negation, pronouns/clusivity, stem alternation, case marking, numerals, quantifiers, coordinators, sentence-final particles, and directionals stable for maintenance and human review; interrogatives is already normalized.
2. [ ] Keep broad TAM / aspect / modal stable at the current candidate/scoping/grammar/dictionary/review-note packet and limit any later TAM edits to reviewer-identified corrections or an explicitly chosen new narrow scope.
3. [ ] Keep relators / postpositions stable at the current candidate/scoping/grammar/dictionary/review-note packet and limit later edits to reviewer-identified corrections or an explicitly chosen new narrow scope.
4. [ ] Keep VP structure / suffix stacking limited to the current candidate/scoping/grammar packet until a later commit explicitly drafts either a very narrow dictionary slice or a different selected packet.
5. [ ] Keep clause linkage enhanced with repaired construction-to-example alignment and tightened normalization supplement, now ready for human review at the current temporal-subordination slice maturity level.
6. [ ] Keep chrestomathy, Mizo/lus, and the other Kuki-Chin languages deferred until they are explicitly chosen as a new scope.

---

*Last updated: 2026-06-09*  
*Tedim Chin coverage: 100% (850,906 tokens)*  
*Mizo (lus) initial coverage: 82.24% (bootstrap pipeline)*
