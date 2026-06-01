---
title: "Assembled Tedim Grammar Review Preview"
---

# Review preview status

This is a review preview, not a finished grammar. It is assembled from first-pass publication-review packets and is controlled by `output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md`, `output/publication_review/whole_grammar_coverage_checkpoint_after_reduplication.md`, `output/publication_review/whole_grammar_coverage_audit.md`, `docs/SKELETON_GRAMMAR.md`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `PROGRESS.md`.

`output/publication_review/review_notes_transitivity.md` brought the current transitivity packet to review-note maturity, and the post-transitivity checkpoint now treats the packet set as stable enough for a review preview. This document is not a new grammar slice, not a dictionary slice, and not a human-review packet. It is intended to help human review and direct editing, not to certify completion.

Many sections remain deliberately narrow. Missing or blocked domains are marked explicitly. Within the currently packetized domains, every review-note packet included below has a corresponding grammar print slice, so the visible gap markers in this preview are the major blocked or still-unpacketized domains rather than missing grammar slices inside the completed packet set.

# PDF/build status

The repository has documented grammar-report and dictionary generation targets in `Makefile`, and `scripts/export_interlinear.py` can compile interlinear `.tex` output with XeLaTeX, but there is no documented publication-review grammar PDF assembly path for these Markdown print slices. No final PDF has been produced for this preview.

To make a PDF later, the repository would need a documented publication-review build target or template-driven assembly path that is explicitly scoped to these review-preview Markdown slices.

# Known narrow-slice limitations

- VP structure / suffix stacking: currently anchored by `bawlzoding`.
- derivation / valency: currently anchored by `-sak`.
- prefix/agreement: currently anchored by `kanei / kainn`.
- clause linkage: currently anchored by `ciangin`.
- nominalization: currently anchored by `-na / bawlna`.
- NP structure / possession: currently anchored by `hih mite`, `mi khat`, `mi khempeuh`.
- noun domain: currently anchored by `gam` and `aksi / aksi-te`.
- reduplication: currently anchored by `mahmah / taktak`, with `peuhpeuh` secondary.
- transitivity: currently anchored by `sih / suak` versus `hawl / en`.

# Major unresolved domains

- [MAJOR GAP: phonology/tone remains blocked or theory-heavy.]
- [MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]
- [MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]
- [MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]

Second-pass expansions such as `-pih`, `ki-`, hong-/kong-, switch reference, relative clauses, transparent compounds, wider reduplication, and labile/ambitransitive transitivity remain outside this first-pass assembled review preview.

# Assembled review preview order

## 1. Phonology and tone

[MAJOR GAP: phonology/tone remains blocked or theory-heavy.]

The architecture sources still expect a phonology and tone chapter, but the current publication-review packet set does not yet provide a print-safe first-pass slice for that domain.

## 2. Deixis, pronouns, and nominal domain

### Demonstratives / deixis

**Grammar slice:** `grammar_demonstratives_print_slice.md`  
**Dictionary slice:** `dictionary_demonstratives_print_slice.md`

This preview opens the nominal side with the current demonstratives/deixis slice as the first deictic section. It remains a first-pass publication-review slice rather than a full deictic chapter.

### Pronouns / clusivity

**Grammar slice:** `grammar_pronouns_print_slice.md`  
**Dictionary slice:** `dictionary_pronouns_print_slice.md`

The pronominal section remains a narrow pronouns/clusivity slice. It is included here as an assembled review section, not as a claim that the whole pronominal or prefixal system has been completed.

### NP structure / possession

**Grammar slice:** `grammar_np_possession_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The current NP structure / possession section stays anchored by `hih mite`, `mi khat`, and `mi khempeuh`. Nominal-host possession, possessor chains, and broader prefix-agreement overlap remain outside this first-pass assembled section.

### Noun domain

**Grammar slice:** `grammar_noun_domain_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The noun-domain section remains deliberately narrow and is anchored by `gam` plus supporting `aksi / aksi-te` evidence. It does not yet expand into a full noun chapter, a compound-noun chapter, or a proper-name chapter.

### Case marking

**Grammar slice:** `grammar_case_marking_print_slice.md`  
**Dictionary slice:** `dictionary_case_markers_print_slice.md`

The case-marking section is included as the current narrow case/postposition slice. It remains the editorial model for how conservative packetized grammar prose should look in this assembled preview.

### Relators / postpositions

**Grammar slice:** `grammar_relators_postpositions_print_slice.md`  
**Dictionary slice:** `dictionary_relators_postpositions_print_slice.md`

The relator/postposition section remains a relator-led and case-boundary-controlled slice rather than a full NP-oblique chapter.

### Numerals

**Grammar slice:** `grammar_numerals_print_slice.md`  
**Dictionary slice:** `dictionary_numerals_print_slice.md`

The numeral section is assembled here because it already has aligned grammar and dictionary print slices. It remains a narrow first-pass numeral packet rather than a full quantity system chapter.

### Quantifiers

**Grammar slice:** `grammar_quantifiers_print_slice.md`  
**Dictionary slice:** `dictionary_quantifiers_print_slice.md`

The quantifier section remains a narrow packet with overlap cautions still controlled against numerals, negation, and sentence-level material.

## 3. Predicate structure and verbal morphology

### Stem alternation

**Grammar slice:** `grammar_stem_alternation_print_slice.md`  
**Dictionary slice:** `dictionary_stem_alternation_print_slice.md`

The assembled verbal section begins with the current stem-alternation slice. It remains useful as a first-pass alternation section but does not settle paradigms, transitivity, or the whole VP system.

### Verb paradigms

[MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]

`docs/grammar/reports/05-verb-00-paradigm-tables.md` still exists as report-backed evidence, but the current publication-review packet set does not yet provide a dedicated paradigm packet or assembled grammar slice.

### Prefix / agreement

**Grammar slice:** `grammar_prefix_agreement_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The current prefix/agreement section remains tightly centered on `kanei / kainn` as an agreement-versus-possession routing contrast. It should not yet be read as a whole prefix paradigm, inverse chapter, or object-prefix chapter.

### Transitivity

**Grammar slice:** `grammar_transitivity_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The current transitivity section is a narrow clean-contrast slice anchored by `sih / suak` versus `hawl / en`. It is explicitly a grammar-facing argument-structure section rather than a lexical-headword or full verb-class treatment.

### VP structure / suffix stacking

**Grammar slice:** `grammar_vp_structure_stacking_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The VP structure section remains anchored by `bawlzoding` and is included here as a narrow constructional slice rather than as a complete account of suffix ordering or predicate architecture.

### TAM / aspect / modal

**Grammar slice:** `grammar_tam_print_slice.md`  
**Dictionary slice:** `dictionary_tam_print_slice.md`

The TAM section remains the current compact suffixal slice and should not be mistaken for a full TAM or VP-stacking chapter.

### Directionals

**Grammar slice:** `grammar_directionals_print_slice.md`  
**Dictionary slice:** `dictionary_directionals_print_slice.md`

The directional section remains assembled as a narrow packet around the currently stabilized directional anchors rather than a full directional or motion-event chapter.

### Derivation / valency

**Grammar slice:** `grammar_derivation_valency_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The derivation/valency section remains anchored by `-sak` and should be read as a first-pass valency-changing slice, not as a whole derivation chapter and not as a settled lexical split.

### Nominalization

**Grammar slice:** `grammar_nominalization_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The nominalization section remains anchored by `-na / bawlna` and does not yet widen into a fuller agentive, relative, or case-hosting nominalization account.

### Clause linkage

**Grammar slice:** `grammar_clause_linkage_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The clause-linkage section remains anchored by `ciangin` as the first stable temporal-subordination slice. Switch reference and relative-clause material remain outside this first-pass assembled prose.

## 4. Clause type, discourse-facing material, and expressive morphology

### Negation

**Grammar slice:** `grammar_negation_print_slice.md`  
**Dictionary slice:** `dictionary_negation_print_slice.md`

The negation section remains a narrow but fully packetized first-pass slice. It is included here as assembled review material, not as a claim that all negation/discourse overlap has been resolved.

### Interrogatives

**Grammar slice:** `grammar_interrogatives_print_slice.md`  
**Dictionary slice:** `dictionary_interrogatives_print_slice.md`

The interrogatives section remains a current review-ready slice and still keeps broader clause-linkage and discourse interaction under control rather than expanding them here.

### Sentence-final particles

**Grammar slice:** `grammar_sentence_final_particles_print_slice.md`  
**Dictionary slice:** `dictionary_sentence_final_particles_print_slice.md`

The sentence-final section remains a narrow review-ready packet and should not be mistaken for a full discourse chapter.

### Coordinators

**Grammar slice:** `grammar_coordinators_print_slice.md`  
**Dictionary slice:** `dictionary_coordinators_print_slice.md`

The coordinator section is included here because it already has print-facing grammar and dictionary slices. It remains a narrow packet and does not replace fuller clause-linkage or discourse treatment.

### Reduplication

**Grammar slice:** `grammar_reduplication_print_slice.md`  
**Dictionary slice:** none by design for this grammar-facing packet

The reduplication section remains anchored by `mahmah / taktak`, with `peuhpeuh` kept secondary. It is a first-pass intensifier-led slice rather than a whole-system reduplication chapter.

### Broader discourse

[MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]

Only the current sentence-final particle slice is assembled here. Broader discourse organization remains only partly surfaced and still overlaps clause linkage, sentence-final material, and generated-summary territory.

### Analyzer-gap caution

[MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]

Current assembled prose still depends on unresolved analyzer-gap boundaries around tone in `-a`, conditioned variants, `hong-`, `-sak`, `-pih`, and other cross-packet issues. Those are reasons to hold this preview stable for human review, not reasons to call the grammar complete.

# End state of this preview

This assembled review preview is a Markdown-only review aid built from the current first-pass publication-review slices. It does not claim that the whole grammar is finished, it does not claim that a final PDF has been produced, and it should be used to support human review and stabilization rather than to certify a completed Tedim reference grammar.
