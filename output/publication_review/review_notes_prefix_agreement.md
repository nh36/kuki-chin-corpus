---
title: "Review Notes: Tedim Prefix / Agreement Print Slice"
---

# What works

The prefix/agreement packet is now aligned at its current routing-slice maturity level. It has a candidate TSV, a scoping dossier, a narrow grammar print slice, and tests: `candidates_prefix_agreement.tsv`, `dossier_prefix_agreement_scope.md`, `grammar_prefix_agreement_print_slice.md`, and the associated test files. Those controlling files should be read together with the supporting/background sources `docs/grammar/reports/05-verb-03-agreement.md`, `docs/grammar/reports/04-np-07-possession.md`, `docs/grammar/morphemes/01-prefixes.md`, `docs/grammar/lit-reviews/04-np-07-possession-lit.md`, `docs/grammar/DISAMBIGUATION.md`, and the regression evidence in `tests/test_prefix_agr_poss.py`.

The packet’s safe first grammar claim is now stable. `kanei` is the verbal agreement anchor, `kainn` is the nominal possessive-routing anchor, `kanei` keeps the gloss `ka-nei` / `1SG-have`, `kainn` keeps the gloss `ka-inn` / `1SG.POSS-house`, and `tests/test_prefix_agr_poss.py` keeps the agreement-versus-possession routing contrast explicit in the regression layer. That is the right level of claim for the current packet: strong enough to state that a shared pronominal prefix family can be routed differently by host type, but still narrow enough to stop short of a full prefix paradigm.

The surrounding boundaries also now work in a stable way. `output/publication_review/review_notes_pronouns.md`, `output/publication_review/review_notes_derivation_valency.md`, and `output/publication_review/review_notes_vp_structure_stacking.md` keep the packet narrow against independent-pronoun and clusivity work, reflexive/middle `ki-` boundary work, and constructional VP-stacking issues.

# Why there is no dictionary slice

There is no dictionary slice because this packet is routing/analysis-based rather than lexical. It should not create dictionary entries for `kanei` or `kainn`.

The current packet is about how a shared pronominal prefix family is analyzed on different host types, not about whether `kanei` and `kainn` should be exported as lexical headwords. That is why the packet is complete with review notes and without a dictionary layer.

# What does not yet work

This packet does not provide a full agreement chapter. It does not provide a full possession chapter. It does not provide a full object-prefix or inverse chapter. It does not provide a full pronoun chapter. It does not provide a full prefix paradigm.

It also does not yet provide a full account of apostrophe possession, broader possessor syntax, broader `a-`-family routing, inclusive/exclusive `i-` routing, hong-/kong- object-prefix selection, or reflexive/middle `ki-` behavior. That restraint is useful. The packet works because it keeps the first claim smaller than the unresolved architecture around it.

# Boundary and deferred material

The packet’s deferred and boundary-only rows are now explicit.

- `ainn` remains outside the first core slice because the broader `a-` family overlaps with verbal agreement and other domains.
- `ipai` remains outside the first core slice because inclusive/exclusive `i-` material belongs first to the completed pronouns/clusivity packet.
- `hongmu` and `kongmu` remain outside the first core slice because object-prefix or inverse-like material still needs a later dedicated sub-scope.
- `kipan` remains outside the first core slice because `ki-` reflexive or middle material remains boundary-only between prefix/agreement and derivation/valency.
- apostrophe possession and broader possessor syntax remain outside the first core slice because this packet is not a full possession chapter.
- broader independent-pronoun and clusivity paradigms remain outside the first core slice because they belong to the completed pronouns/clusivity packet.

These deferrals are also why the current packet should stop here. It is better to hand off a narrow stable routing slice than to force the broader prefix system, possession chapter, or pronoun chapter into premature print prose.

# Recommended next editorial task

With review notes added, the prefix/agreement packet is now ready for human review at its current routing-slice maturity level.

The next substantive missing first-band domain should be clause linkage: subordination / switch reference / relative clauses. The remaining audit still treats those as report-backed but unlifted, and they remain a major architecture gap before any full grammar print bundle should be considered.
