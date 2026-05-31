---
title: "Review Notes: Tedim NP Structure / Possession Print Slice"
---

# What works

The NP structure / possession packet is now aligned at its current basic-NP-ordering slice maturity level. It now has a candidate TSV, a scoping dossier, a narrow grammar print slice, and tests: `candidates_np_possession.tsv`, `dossier_np_possession_scope.md`, `grammar_np_possession_print_slice.md`, and the associated test files. Those controlling files should be read together with the supporting/background sources `docs/grammar/reports/03-noun-06-np-structure.md`, `docs/grammar/reports/04-np-07-possession.md`, `docs/grammar/lit-reviews/04-np-07-possession-lit.md`, and `docs/grammar/morphemes/01-prefixes.md`.

The packet’s safe first grammar claim is now stable. `hih mite` is the demonstrative-before-noun anchor, `hih mi-te` is the controlled segmentation, and `PROX person-PL` is the controlled gloss. `mi khat` is the head-noun plus numeral anchor, with `person one` as the controlled gloss. `mi khempeuh` is the head-noun plus quantifier anchor, with `mi khem-peuh` as the controlled segmentation and `person all` as the controlled gloss. That is the right level of claim for the current packet: strong enough to say that Tedim has candidate-controlled evidence for basic NP ordering, with demonstratives preceding the noun and numerals and quantifier-like modifiers following the noun, but still narrow enough to stop short of a full noun-phrase chapter.

The surrounding boundaries also now work in a stable way. `output/publication_review/review_notes_prefix_agreement.md`, `output/publication_review/review_notes_pronouns.md`, `output/publication_review/review_notes_case_marking.md`, `output/publication_review/review_notes_relators_postpositions.md`, `output/publication_review/review_notes_nominalization.md`, and `tests/test_prefix_agr_poss.py` keep the packet narrow against prefix/agreement routing, pronoun inventory, case-marking and relator adjacency, and nominalized noun-headed overlap.

# Why there is no dictionary slice

There is no dictionary slice because this packet is structural/syntactic rather than lexical. It should not create dictionary entries for `hih mite`, `mi khat`, `mi khempeuh`, `ka pa`, `Topa' inn`, or other NP strings.

That restraint is especially important because possession, possessor-possessed structure, apostrophe or genitive analysis, prefix/agreement routing, and nominalized noun-headed material remain unsettled. The current packet is about a narrow basic NP-ordering claim, not about exporting a stable lexical-headword layer from mixed structural and boundary-heavy evidence.

# What does not yet work

This packet does not provide a full noun-phrase chapter. It does not provide a full possession chapter. It does not provide a full prefix/agreement chapter. It does not provide a full case or relator chapter. It does not provide a full recursive possession account.

It also does not yet provide a settled editorial account of apostrophe/genitive possession, layered possessor-possessed structure, or how nominal-host possession should be separated from the completed prefix/agreement routing packet. That restraint is useful. The packet works because it keeps the first claim smaller than the unresolved noun-domain architecture around it.

# Boundary and deferred material

The packet’s deferred and boundary-only rows are now explicit.

- `ka pa` remains outside the first core slice because possession and possessive-prefix routing still interact with the completed prefix/agreement packet.
- `Topa' inn` remains outside the first core slice because apostrophe/genitive analysis still needs a separate possession sub-scope.
- `a pa' inn` remains outside the first core slice because layered possessor-possessed structure crosses prefix possession and apostrophe possession.
- `Topa' tungah` remains outside the first core slice because possessive NP plus relator/case material remains shared with case marking and relators/postpositions.
- `ka suahna leitang` remains outside the first core slice because nominalized noun-headed material remains shared with nominalization.
- isolated `a`, `ka`, or `na` prefix surfaces remain outside the first core slice because they are analyzer-noisy away from controlled nominal hosts.
- pronoun-led possessor rows such as `amah a pa` remain outside the first core slice because they still sit between NP structure, possession, and the completed pronoun packet.
- tone-marked or literature-only genitive claims such as `-á` remain outside the first core slice because they are not yet tied tightly enough to corpus-backed first-slice anchors.
- report-only counts remain outside the first core slice because attestation alone does not make a row safe for the first print-facing claim.
- any broad noun-phrase, possession, prefix/agreement, case, relator, or recursive possession chapter claim remains outside the first core slice because the current packet is only a narrow basic-NP-ordering slice.

These deferrals are also why the current packet should stop here. It is better to hand off a narrow stable NP-ordering slice than to force the broader noun-domain architecture into premature print prose.

# Recommended next editorial task

With review notes added, the NP structure / possession packet is now ready for human review at its current basic-NP-ordering slice maturity level.

The next substantive missing domain should be simple nouns / compounds / proper nouns, because `output/publication_review/whole_grammar_coverage_audit.md` still treats noun stem classes and lexical noun structure as report-backed but unlifted, and the current NP packet now depends on a clearer noun-domain foundation.
