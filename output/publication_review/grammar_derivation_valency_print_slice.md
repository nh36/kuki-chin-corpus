---
title: "Tedim Derivation / Valency Grammar Print Slice"
---

# Editorial scope

This is the first narrow derivation / valency grammar slice for Tedim. It is controlled by `output/publication_review/candidates_derivation_valency.tsv` and `output/publication_review/dossier_derivation_valency_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-08-derivational.md`, `docs/grammar/reports/05-verb-09-valency.md`, `docs/grammar/morphemes/06-derivational.md`, `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`, and the regression evidence in `tests/test_sak_caus_benf.py`.

This is not a full derivation chapter, not a full valency chapter, and not a full verbal morphology chapter. It also does not reopen adjacent packet domains already controlled through `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, `output/publication_review/review_notes_pronouns.md`, `tests/test_vp_slots.py`, and `tests/test_prefix_agr_poss.py`.

The present slice therefore covers only the first safe `-sak` claim: `paisak` as the clearest causative anchor and `muhsak` as the clearest benefactive or applicative-like split row. No dictionary slice exists yet for derivation/valency, because the packet still leaves the `-sak` lexical split open for later editorial review.

# Causative `-sak`

`paisak` is the safest causative anchor for the first print-facing derivation / valency claim. The candidate layer marks it as the main future `-sak` causative anchor, and `docs/grammar/reports/05-verb-09-valency.md` already lists it among the common `-sak` forms.

The safe grammar claim is deliberately narrow. The current evidence supports a productive Form I plus `-sak` causative pattern, with `paisak` as the candidate-controlled row that shows the pattern most cleanly. `tests/test_sak_caus_benf.py` protects that contrast explicitly by requiring `paisak` to gloss as `go-CAUS` rather than as a benefactive or lexicalized exception.

That is enough for the first core claim. The slice does not need to generalize over every `-sak` form in the reports before saying that a productive causative use is visible.

# Benefactive / applicative-like `-sak`

`muhsak` is the safest benefactive or applicative-like split row in the current packet. The candidate layer keeps it distinct from the plain causative line, and `tests/test_sak_caus_benf.py` protects that distinction by requiring Form II plus `-sak` rows to keep the `.II` marker and a `BENF` gloss.

The print claim here also stays narrow. The current evidence supports keeping Form II plus `-sak` distinct from the plain causative line in the candidate layer, with `muhsak` as the clearest first-row anchor. The literature and morpheme files justify describing this as benefactive or applicative-like material, but the slice should not pretend that every higher-level label choice is already settled.

This is why `muhsak` belongs in the first slice even though it is more caveated than `paisak`. It is the clearest compact row showing that the `-sak` domain is not exhausted by a simple causative paraphrase.

# Editorial treatment of the `-sak` split

The grammar can therefore treat the `paisak` versus `muhsak` contrast as a controlled split in the first print slice. The evidence is strong enough to keep Form I plus `-sak` and Form II plus `-sak` apart in the editorial layer.

At the same time, the slice should keep open the higher-level question of whether this contrast is best described as two readings of one suffix or two editorial subsections of the same suffixal domain. `docs/grammar/lit-reviews/05-verb-09-valency-lit.md` and `docs/grammar/morphemes/06-derivational.md` both support cautious wording here: the split is real enough for candidate control, but the final theoretical framing should stay smaller than a full chapter claim.

This first slice therefore adopts a practical editorial solution rather than a maximal theoretical one. It prints the causative and benefactive/applicative-like uses as separate controlled subsections while leaving open whether a later chapter should collapse them back into one suffix with two readings.

# Boundary material

The rest of the candidate packet remains outside the first grammar slice because each row is still dominated by another unresolved boundary.

`paipih` stays outside the first grammar slice because `-pih` still carries applicative, comitative, associative, and benefactive uncertainty. `mipihte` stays outside because it is nominal or lexicalized `pih` boundary material rather than a clean verbal anchor.

`kisep` and `kigen` stay outside because `ki-` still needs a separate reflexive, middle, and passive-like treatment, and because the packet must keep prefix/agreement boundary control explicit through `output/publication_review/review_notes_pronouns.md` and `tests/test_prefix_agr_poss.py`.

`ciahsakkik`, `bawlsakthei`, and `paikhiatsak` stay outside because they are derivation-heavy stacks interacting respectively with aspect, modal, and directional material. Those rows remain visible through `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, and `tests/test_vp_slots.py`, but they are not the first core derivation anchor.

`piangsak` stays outside because it is lexicalized or transitivity-adjacent rather than a clean productive `-sak` anchor.

# Safe first-slice claim

At the current slice maturity level, the safest derivation / valency claim is that Tedim has candidate-controlled evidence for a productive `-sak` domain, with `paisak` supporting a causative use and `muhsak` supporting a distinct benefactive or applicative-like use.

That claim is deliberately smaller than a full derivation chapter, smaller than a full valency chapter, and smaller than a full verbal morphology chapter. It does not settle the whole `-pih` system, the whole `ki-` system, derivation-heavy stacking, or transitivity as a separate domain.

# Recommended next step

After this grammar slice, the next step should be review notes rather than a dictionary layer, because a dictionary layer would risk overclaiming beyond the current candidate-controlled evidence before the `-sak` lexical split is reviewed.
