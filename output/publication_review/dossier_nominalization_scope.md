---
title: "Tedim Nominalization Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for nominalization. The controlling candidate layer now exists at `output/publication_review/candidates_nominalization.tsv`.

This dossier remains the candidate/scoping pass rather than the print slice itself, and it is not a full derivation or relative-clause chapter. A first narrow grammar print slice now exists at `output/publication_review/grammar_nominalization_print_slice.md`. Dictionary and review-note slices for nominalization do **not** yet exist.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` and `output/publication_review/review_notes_clause_linkage.md` are the main reasons this scope was selected now.

The whole-grammar audit identifies nominalization as the next substantive missing domain after the current clause-linkage packet. The clause-linkage review notes then make that priority explicit by naming nominalization as the next follow-on domain because `omna` and `muhna-ah` show that relative clauses and clause-linkage boundaries repeatedly run into nominalization and case-routing questions.

This packet is also architecture-controlled by `docs/grammar/grammar_source_map.json`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `docs/SKELETON_GRAMMAR.md`. Those files keep `nominalization-na` and `agentive-pa-mi` inside the same broader chapter area while also showing that the packet has to stay narrower than a full derivation chapter or a full relative-clause chapter.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/07-nmlz-01-deverbal.md`
- `docs/grammar/morphemes/06-derivational.md`

The nominalization report is the main direct evidence source. `docs/grammar/morphemes/06-derivational.md` is much thinner for nominalization than for `-sak` or `-pih`, but it still matters as a boundary-control source because the repository routes nominalization near derivational morphology and the file helps show that nominalization should not be collapsed into the current derivation/valency packet.

Those source files are discovery and evidence layers, not the controlling layer. The controlling layer is `output/publication_review/candidates_nominalization.tsv`, which records which rows are currently clean enough to carry forward toward print and which rows must stay boundary-only or deferred.

# Candidate groups

## `-na`

`-na` is the cleanest current nominalization anchor. `docs/grammar/reports/07-nmlz-01-deverbal.md` treats it as the main action/result nominalizer, `docs/grammar/grammar_source_map.json` routes it as `nominalization-na`, and `docs/SKELETON_GRAMMAR.md` keeps it as the first nominalizer subsection.

That makes `-na` the safest future print-facing row. A form such as `bawlna` is narrow enough to lead a later grammar slice without forcing the packet to solve relative clauses, case routing, or all agentive nominalization at the same time.

## `-pa`

`-pa` is also real nominalization evidence, but it is less clean than `-na`. The report clearly includes agentive `-pa` forms such as `bawlpa`, but the same report also surfaces title-like or lexicalized rows such as `kumpipa` and `Topa`.

The safest interpretation is therefore to keep `-pa` explicit in the candidate layer while refusing to let it lead the first print slice. The packet has to distinguish productive agentive nominalization from lexicalized title-like nouns before `-pa` can be a stable print anchor.

## `-mi`

`-mi` needs to stay explicit because `docs/grammar/grammar_source_map.json` and `docs/SKELETON_GRAMMAR.md` both treat it as part of the same agentive nominalization area as `-pa`.

At the same time, `-mi` is more boundary-heavy than `-na`. The deverbal report summarizes `mi-` as person-denoting material, while the clause-linkage packet already shows that forms like `a bawl mi` overlap with relative-clause analysis. The current packet should therefore keep `-mi` visible, but not pretend that its nominalization status is already isolated from clause linkage.

## Nominalized relatives and clause-derived nominals

`Omna` is the clearest current overlap row. It shows that nominalization is not only a deverbal derivation topic but also part of the relative-clause and clause-linkage architecture.

That overlap is useful, but it should remain controlled. `Omna` belongs in the candidate layer now because it makes the architecture honest, not because it is already safer than `-na`.

## Nominalization plus case boundary rows

`Muhna-ah` is the clearest current nominalization-plus-case boundary row. It shows why nominalization cannot be separated cleanly from case routing.

It should remain deferred for the first slice. The row is valuable as boundary evidence, but it belongs to later work that coordinates nominalization with case marking and clause linkage.

# Existing packet boundaries

Nominalization has to stay narrow against several existing packets and boundary files.

- `output/publication_review/candidates_clause_linkage.tsv` and `output/publication_review/review_notes_clause_linkage.md` are the main boundary controls for `omna`, `muhna-ah`, and relative-clause overlap material.
- `output/publication_review/review_notes_case_marking.md` is boundary control for nominalization-plus-case routing, especially rows like `muhna-ah`.
- `output/publication_review/review_notes_derivation_valency.md` is boundary control against collapsing nominalization into the already completed `-sak` packet or into a broad derivational chapter.
- `output/publication_review/review_notes_prefix_agreement.md` is boundary control for `a-` overlap in relative-clause-adjacent material such as `a bawl mi`.
- `output/publication_review/review_notes_pronouns.md` is boundary control against reopening person-marking or pronominal material while discussing human-head nominalization.

These boundaries explain why the packet is still only at the candidate/scoping stage.

# Deferred material

Several important rows should remain deferred for now.

- lexicalized or title-like `-pa` nouns such as `kumpipa` and `Topa` should remain outside the first slice because they blur productive nominalization with lexical category.
- `omna` should remain accepted only with caveat because it is still shared with relative-clause and clause-linkage analysis.
- `muhna-ah` should remain deferred because nominalization-plus-case routing belongs partly to case marking rather than to a pure nominalization slice.
- `a bawl mi` and similar human-head relative rows should remain cross-packet material because they still sit between nominalization, relative clauses, and prefix/agreement questions.
- bare `na` remains analyzer-noisy as a surface form because the source map already warns that `na` is also a high-frequency pronominal form.
- report summaries around `mi-` versus `-mi` should remain candidate-controlled because the packet still needs a conservative editorial decision about how person-head material is best normalized in print.

The packet should also avoid overclaiming from report-only counts. High attestation alone does not make a row clean enough to lead the first print slice.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer is a **very narrow `-na` grammar slice**, not a broad nominalization chapter.

More specifically, the safest route is a compact grammar print slice centered on:

1. `-na` as the clearest productive deverbal nominalizer;
2. one controlled anchor such as `bawlna`;
3. explicit boundary notes saying that `-pa`, `-mi`, `omna`, and `muhna-ah` remain candidate-layer or boundary material rather than the first print-facing claim.
