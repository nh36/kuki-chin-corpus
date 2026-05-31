---
title: "Review Notes: Tedim Derivation / Valency Print Slice"
---

# What works

The derivation / valency packet is now aligned at its current `-sak` slice maturity level. It has a candidate TSV, a scoping dossier, a narrow grammar print slice, and tests: `candidates_derivation_valency.tsv`, `dossier_derivation_valency_scope.md`, `grammar_derivation_valency_print_slice.md`, and the associated test files. Those controlling files should be read together with the supporting/background sources `docs/grammar/reports/05-verb-08-derivational.md`, `docs/grammar/reports/05-verb-09-valency.md`, `docs/grammar/morphemes/06-derivational.md`, `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`, and the regression evidence in `tests/test_sak_caus_benf.py`.

The packet’s safe first grammar claim is now stable. `paisak` is the causative `-sak` anchor, `muhsak` is the benefactive or applicative-like `-sak` split row, and `tests/test_sak_caus_benf.py` keeps the Form I plus `-sak` versus Form II plus `-sak` contrast explicit in the regression layer. That is the right level of claim for the current packet: strong enough to separate the two uses in print, but still cautious enough to leave open whether the contrast is best treated as two readings of one suffix or two editorial subsections of the same suffixal domain.

The surrounding boundaries also now work in a stable way. `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, `output/publication_review/review_notes_pronouns.md`, `tests/test_vp_slots.py`, and `tests/test_prefix_agr_poss.py` keep the packet narrow against VP stacking, TAM, directionals, pronouns/prefixes, and agreement issues.

# Why there is no dictionary slice yet

There is no dictionary slice yet because the `-sak` lexical treatment should wait for human/editorial review of the causative versus benefactive/applicative-like split.

The packet is ready for human review as a narrow grammar slice, but a dictionary layer now would risk overclaiming exactly the question the packet is still keeping open. The present packet can safely separate `paisak` and `muhsak` in print as controlled grammar evidence without pretending that the final lexical treatment of `-sak` has already been settled.

# What does not yet work

This packet does not provide a full derivation chapter. It does not provide a full valency chapter. It does not provide a full verbal morphology chapter.

It also does not yet provide a full `-pih` account, a full `ki-` account, a full transitivity account, or a full derivation-heavy stacking account. That restraint is useful. The packet works because it keeps the first claim smaller than the unresolved architecture around it.

# Boundary and deferred material

The packet’s deferred and boundary-only rows are now explicit.

- `paipih` remains outside the first core slice because `-pih` is still applicative/comitative/benefactive unresolved.
- `kisep` and `kigen` remain outside the first core slice because `ki-` still needs separate reflexive/middle/passive-like treatment and prefix/agreement boundary control.
- `ciahsakkik`, `bawlsakthei`, and `paikhiatsak` remain derivation-heavy stacks interacting with aspect, modal, or directional material rather than clean first-slice anchors.
- `piangsak` remains lexicalized/transitivity-adjacent rather than a clean productive `-sak` anchor.
- `mipihte` remains nominal or lexicalized `pih` boundary material rather than verbal derivation evidence.
- broader transitivity, VP stacking, TAM, directionals, pronouns/prefixes, and agreement issues remain outside the first derivation / valency slice.

These deferrals are also why the current packet should stop here. It is better to hand off a narrow stable `-sak` slice than to force `-pih`, `ki-`, stacking, or transitivity into premature print prose.

# Recommended next editorial task

With review notes added, the derivation / valency packet is now ready for human review at its current `-sak` slice maturity level.

The next substantive missing first-band domain should be pronominal prefixes / agreement / object-prefix systems. The remaining first-band audit repeatedly flags `hong-`, `kong-`, prefix/agreement, possessive-versus-agreement routing, and `ki-` boundary issues, so that domain is now the clearest next packet after human review of the current derivation / valency slice.
