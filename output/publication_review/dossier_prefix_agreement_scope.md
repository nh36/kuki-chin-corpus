---
title: "Tedim Prefix / Agreement / Object-Prefix Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for pronominal prefixes, agreement, possessive-prefix routing, and object-prefix/inverse material. The controlling candidate layer now exists at `output/publication_review/candidates_prefix_agreement.tsv`.

This dossier remains the candidate/scoping pass rather than the print slice itself. It is also not a rewrite of the completed pronouns/clusivity packet. A first narrow grammar print slice now exists at `output/publication_review/grammar_prefix_agreement_print_slice.md`. Dictionary and review-note slices for prefix/agreement do **not** yet exist.

The packet stays narrow on purpose. Its job is to identify a small future print-facing prefix scope while keeping clear boundaries with the completed pronouns/clusivity packet, the current derivation/valency packet, and the constructional VP structure / suffix stacking packet.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` and `output/publication_review/review_notes_derivation_valency.md` are the main reasons this scope was selected now.

The whole-grammar audit identifies pronominal prefixes / agreement / possessive prefixes and object-prefix or inverse material as a first-band domain that remains only partially lifted. The derivation / valency review notes then make the remaining boundary more specific: `ki-` still sits at the edge between prefix/agreement work and reflexive/middle work, and the next missing domain repeatedly includes `hong-`, `kong-`, and possessive-versus-agreement routing.

This packet is also architecture-controlled by `docs/grammar/grammar_source_map.json`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `docs/SKELETON_GRAMMAR.md`. The source map routes the packet through `pronominal-prefixes`, `inverse-hong`, and `reflexive-ki`, while the inventory and skeleton grammar show that the prefix system cuts across pronouns, possession, and verbal agreement rather than belonging to only one completed packet.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/05-verb-03-agreement.md`
- `docs/grammar/reports/06-func-01-pronouns.md`
- `docs/grammar/reports/04-np-07-possession.md`
- `docs/grammar/morphemes/01-prefixes.md`
- `docs/grammar/lit-reviews/06-func-01-pronouns-lit.md`
- `docs/grammar/lit-reviews/04-np-07-possession-lit.md`
- `docs/grammar/DISAMBIGUATION.md`

The key existing evidence/control test is `tests/test_prefix_agr_poss.py`. That test is especially important because it gives the packet a regression-backed answer to the core routing question: the same prefix family is glossed as agreement on verbs and as possession on nouns. The candidate TSV is therefore the controlling layer for what gets promoted later, while the reports, literature files, and disambiguation notes are discovery and interpretation sources.

`output/publication_review/review_notes_pronouns.md` is also a boundary-control source. It confirms that pronouns/clusivity already has a completed packet and that `hong-` and `kong-` only entered that packet under cautious, manually reviewed treatment. This new packet should therefore focus on the still-unlifted prefix system rather than reopening the independent-pronoun paradigm.

# Candidate groups

## Subject/agreement prefixes

The evidence for subject/agreement prefixes is broad across the agreement report, the pronoun report, and the prefixes morpheme file. Henderson-style concord and ZNC-style prefix paradigms both keep `ka-`, `na-`, `a-`, and `i-` visible.

The cleanest current future print anchor is `kanei`. It is regression-backed in `tests/test_prefix_agr_poss.py`, analyzer-stable as `ka-nei / 1SG-have`, and narrow enough to represent the verbal agreement side of the prefix system without reopening the entire pronoun packet.

The `i-` series remains important but is not yet a first print anchor here. `ipai` stays in the candidate TSV only as boundary material, because the inclusive/exclusive editorial problem is already owned by the completed pronouns/clusivity packet and the raw analyzer output for `ipai` is still noisy.

## Possessive prefixes and agreement-versus-possession routing

The boundary between agreement prefixes and possessive prefixes is the safest core issue for this packet. The same surface prefix family appears before verbs and nouns, but the repository now has a strong routing control through `tests/test_prefix_agr_poss.py`.

`Kanei` and `kainn` are the clearest routing pair. `kanei` stays verbal and glosses as `1SG-have`; `kainn` stays nominal and glosses as `1SG.POSS-house`. That makes them the strongest future print-facing anchors in the whole packet.

`Ainn` is useful adjacent evidence because it keeps the dominant third-person possessive prefix in scope, but it is more caveated than `kainn`. The shared `a-` family also overlaps with verbal agreement and other grammar domains, so it is safer as boundary support than as the first print anchor.

## hong- and kong- object-prefix or inverse-like material

The packet also needs a small controlled hong-/kong- group, because this material is clearly part of the unresolved prefix system.

`Hongmu` and `kongmu` are the clearest candidate rows. Both are analyzer-stable, both are visible in the agreement and pronoun reports, and both are explicitly routed by `docs/grammar/grammar_source_map.json` plus `docs/grammar/morphemes/01-prefixes.md`.

Their status is still caveated. The sources disagree or only partly align on whether these should be described primarily as object prefixes, inverse markers, directional markers, or mixed directional/inverse material. The safest current dossier answer is that `hong-` and `kong-` are strong enough to remain in the candidate layer and later print prose, but not yet strong enough to lead the first print slice.

## ki- boundary material

`Ki-` belongs in this packet only as boundary material.

`Output/publication_review/review_notes_derivation_valency.md` explicitly deferred reflexive or middle-like `ki-` issues into this broader prefix/agreement domain, but that does not mean the first prefix slice should absorb them. `Kipan` is the clearest current boundary row because it is analyzer-stable as `ki-pan / REFL-begin` and already lives at the boundary between pronouns, derivation/valency, and broader prefixal marking.

The packet answer for `ki-` is therefore narrow: it should remain visible in the candidate layer, but it should stay out of the first print slice until a separate reflexive/middle/passive-like treatment is chosen.

# Existing packet boundaries

This packet must stay narrow against several existing packets:

- `output/publication_review/review_notes_pronouns.md` already owns the pronouns/clusivity packet, including the `ko/kote` versus `ei/eite` problem. Independent pronouns, emphatics, and clusivity should not be reopened here.
- `output/publication_review/review_notes_derivation_valency.md` already records that reflexive or middle-like `ki-` belongs on the boundary between derivation/valency and prefix work. This packet should not treat `ki-` as solved.
- `output/publication_review/review_notes_vp_structure_stacking.md` remains boundary control against turning prefix combinations into a new VP-stacking packet.

The possession report is also only partly absorbed here. This packet is about prefix routing, not about a full possession chapter, apostrophe possession, or full possessor syntax.

# Deferred material

The following material should stay deferred in this first candidate/scoping packet:

- `ipai` and broader `i-` clusivity material, because the pronouns/clusivity packet already owns the inclusive/exclusive editorial problem;
- broader `a-` agreement, relativizer, and shared-surface issues that need more disambiguation than the first routing slice can carry;
- `hong-` plus broader directional or benefactive interactions, because the source map and morpheme file still flag inverse constraints as needing explicit verification;
- `ki-` reflexive, reciprocal, middle, or passive-like material such as `kipan`, because it still belongs to a separate cross-packet treatment;
- lexicalized or analyzer-noisy raw strings whose prefix analysis is unstable outside carefully controlled contexts;
- independent-pronoun and clusivity paradigms already completed in `review_notes_pronouns.md`.

The common principle is that the first slice should promote only the rows that are both semantically clear and regression-protected.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer is a **very narrow agreement-versus-possession routing grammar slice**, not a hong-/kong- slice.

More specifically, the safest route is a compact grammar print slice centered on:

1. `kanei` as the clearest agreement anchor;
2. `kainn` as the clearest possessive-routing anchor;
3. `tests/test_prefix_agr_poss.py` as the regression control keeping verb-side AGR and noun-side POSS distinct.

`Hongmu` and `kongmu` should stay visible as a second-tier future sub-scope, but their directional versus inverse framing is still more caveated than the AGR-versus-POSS routing pair. `Ki-` should remain boundary-only until its reflexive or middle-like status is packeted separately.
