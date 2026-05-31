---
title: "Tedim Prefix / Agreement Grammar Print Slice"
---

# Editorial scope

This is the first narrow prefix/agreement grammar slice for Tedim. It is controlled by `output/publication_review/candidates_prefix_agreement.tsv` and `output/publication_review/dossier_prefix_agreement_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-03-agreement.md`, `docs/grammar/reports/04-np-07-possession.md`, `docs/grammar/morphemes/01-prefixes.md`, `docs/grammar/lit-reviews/04-np-07-possession-lit.md`, `docs/grammar/DISAMBIGUATION.md`, and the regression evidence in `tests/test_prefix_agr_poss.py`.

This is not a full agreement chapter, not a full possession chapter, not a full object-prefix or inverse chapter, and not a rewrite of the completed pronouns/clusivity packet. It also stays narrow against `output/publication_review/review_notes_pronouns.md`, `output/publication_review/review_notes_derivation_valency.md`, and `output/publication_review/review_notes_vp_structure_stacking.md`.

The present slice therefore covers only the agreement-versus-possession routing contrast, with `kanei` as the clearest agreement anchor and `kainn` as the clearest possessive-routing anchor. No dictionary slice exists yet for prefix/agreement, because this packet is still establishing a controlled routing claim rather than a lexical headword layer. The packet now proceeds through review notes rather than through a lexical headword layer.

# Agreement versus possession routing

The first safe prefix/agreement claim is a routing contrast. Before verbs, the shared pronominal prefix family may be routed as agreement; before nouns, the same family may be routed as possession.

`Kanei` and `kainn` are the core pair for that contrast. `Kanei` keeps the prefix family on a verbal host, while `kainn` keeps it on a nominal host. `tests/test_prefix_agr_poss.py` is the key regression control here, because it explicitly requires verb-side AGR glossing to stay distinct from noun-side POSS glossing.

That is enough for the first print-facing claim. The slice does not need to resolve every larger prefix question before stating that host type already controls a safe agreement-versus-possession routing contrast in the current candidate layer.

# Agreement anchor: kanei

`Kanei` is the clearest verbal agreement anchor in the packet. The candidate TSV marks it as the main AGR-side row, and `tests/test_prefix_agr_poss.py` protects the glossing as `ka-nei` / `1SG-have`.

The grammar claim here is deliberately limited. At the current slice maturity level, `kanei` supports only the routing statement that the shared prefix family can surface as verbal agreement before a verb host. This is strong enough for a narrow print slice, but still smaller than a full agreement chapter or a full prefix paradigm.

# Possessive anchor: kainn

`Kainn` is the clearest possessive-routing anchor in the packet. The candidate TSV marks it as the nominal counterpart to `kanei`, and `tests/test_prefix_agr_poss.py` protects the glossing as `ka-inn` / `1SG.POSS-house`.

The grammar claim again stays small. At the current slice maturity level, `kainn` supports the routing statement that the same prefix family can be analyzed as possessive before a noun host. This is enough to justify a first print-facing contrast without pretending that the project already has a full possession chapter or a full possessor-syntax account.

# Why this is not just pronouns again

The completed pronouns/clusivity packet already handles independent pronouns, clusivity, and the broader pronoun paradigm through `output/publication_review/review_notes_pronouns.md`.

This slice is doing something narrower. It is about prefix routing across verbal and nominal hosts, not about reopening the independent-pronoun paradigm. That is why `kanei` and `kainn` are better first anchors here than `ipai`, `ko`, `ei`, or any broader person-paradigm table.

# Boundary material

The rest of the candidate packet stays outside the first grammar slice because each row is still dominated by another unresolved boundary.

`ainn` stays outside because the broader `a-` family overlaps with verbal agreement, relativizer-like material, and other domains. It is useful boundary evidence, but not the first clean routing anchor.

`ipai` stays outside because inclusive/exclusive `i-` material belongs first to the completed pronouns/clusivity packet rather than to this first routing slice.

`hongmu` and `kongmu` stay outside because object-prefix or inverse-like material still needs a later dedicated sub-scope with tighter directional and inverse controls.

`kipan` stays outside because `ki-` reflexive or middle material remains boundary-only between prefix/agreement and derivation/valency.

Apostrophe possession and broader possessor syntax also stay outside because this is not a full possession chapter.

# Safe first-slice claim

At the current slice maturity level, the safest prefix/agreement claim is that Tedim has candidate-controlled evidence for routing a shared pronominal prefix family differently by host type: `kanei` supports verbal agreement routing, while `kainn` supports nominal possessive routing.

That claim is deliberately smaller than a full agreement chapter, smaller than a full possession chapter, smaller than a full object-prefix or inverse chapter, and smaller than a rewritten pronoun packet.

# Recommended next step

This packet now properly proceeds to prefix/agreement review notes rather than to a dictionary slice, because it is a routing/analysis packet rather than a lexical headword packet.

If the project later wants one more prefix step after review notes and human review, the next sub-scope should be a separate hong-/kong- object-prefix or inverse candidate expansion rather than a dictionary layer.
