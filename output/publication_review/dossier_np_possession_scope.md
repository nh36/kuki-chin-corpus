---
title: "Tedim NP Structure / Possession Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for NP structure and possession. The controlling layer is `output/publication_review/candidates_np_possession.tsv`.

This dossier is not a grammar print slice. It is not a full noun-phrase or possession chapter. A narrow grammar print slice now exists at `output/publication_review/grammar_np_possession_print_slice.md`, but dictionary and review-note slices for NP structure / possession do not yet exist.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` and `output/publication_review/review_notes_nominalization.md` identify NP structure / possession as the next substantive missing domain after the completed nominalization packet. The audit explicitly says that NP structure and possession remain report-backed but not fully lifted, while nominalization, case, and prefix-routing boundaries repeatedly run into nominal syntax and possessor or nominal-host questions.

`docs/grammar/grammar_source_map.json`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `docs/SKELETON_GRAMMAR.md` are the architecture and planning controls for this packet. They show that Tedim has report-backed noun-domain material but no already-completed publication-review packet for NP structure / possession. `docs/grammar/grammar_source_map.json` only gives partial architecture through `pronominal-prefixes`; it does not itself resolve a full NP-structure or possession packet.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/03-noun-06-np-structure.md`
- `docs/grammar/reports/04-np-07-possession.md`
- `docs/grammar/lit-reviews/04-np-07-possession-lit.md`
- `docs/grammar/morphemes/01-prefixes.md`

These files are evidence sources, not the controlling editorial layer. The controlling editorial layer for this packet is `output/publication_review/candidates_np_possession.tsv`.

`tests/test_prefix_agr_poss.py` is regression evidence and a boundary control rather than a license to reopen the completed prefix/agreement routing packet. It matters here because nominal-host possession repeatedly touches the AGR-versus-POSS contrast, but this packet should not collapse back into the prefix/agreement slice.

# Candidate groups

The current candidate layer is intentionally small and split into a few groups.

## Basic NP ordering and modifier structure

The cleanest current NP-order rows are `hih mite`, `mi khat`, and `mi khempeuh`. Together they support a conservative head-order statement: demonstratives can precede the noun, while numerals and quantifier-like modifiers can follow the noun.

These rows are safer than broader adjective or stative-modifier claims, because stative or property material can slide toward predicate or clause-level analysis more quickly than the basic demonstrative, numeral, and quantifier rows do.

## Possession and possessor-possessed structure

The possession side of the candidate layer keeps three small but useful rows visible:

- `ka pa` for nominal-host possessive-prefix routing where the NP or possession side is primary;
- `Topa' inn` for apostrophe-marked full-NP possession if that analysis is kept;
- `a pa' inn` for layered possessor-possessed structure combining prefix possession and apostrophe possession.

These are strong enough for scoping, but they are not yet equally safe as print-facing anchors. `ka pa` is the cleanest nominal-host possession row. `Topa' inn` and `a pa' inn` are real and important, but they carry more boundary pressure from genitive analysis, apostrophe interpretation, and the completed prefix/agreement packet.

## Cross-packet boundary rows

The candidate layer also keeps a few rows visible precisely because they should **not** lead the first print-facing claim:

- `Topa' tungah` as possessive NP plus case or relator material;
- `ka suahna leitang` as nominalization/NP overlap.

These rows help define the boundaries of the packet more clearly than they help define its first print slice.

# Existing packet boundaries

This packet must stay explicit about its boundaries with already completed packets.

## Prefix/agreement boundary

`output/publication_review/review_notes_prefix_agreement.md` remains the completed routing packet for AGR-versus-POSS contrasts such as `kanei` versus `kainn`. NP structure / possession can reuse that result as a boundary control, but it should not re-argue the entire prefix paradigm here. In this packet, possessive-prefix material is only included when the nominal-host possession side is primary.

## Pronouns boundary

`output/publication_review/review_notes_pronouns.md` remains the completed pronouns/clusivity packet. Independent pronoun possessors, inclusive or exclusive possessive paradigms, and person-marking questions that primarily belong to pronoun inventory should stay there rather than being widened into the first NP structure / possession slice.

## Case-marking and relators boundary

`output/publication_review/review_notes_case_marking.md` and `output/publication_review/review_notes_relators_postpositions.md` remain the boundary controls for case-marked and relator-adjacent NPs. Rows such as `Topa' tungah` show that possession can run directly into those domains, but that is a reason to keep them boundary-controlled, not a reason to absorb case marking or relators into the first slice.

## Nominalization boundary

`output/publication_review/review_notes_nominalization.md` remains the boundary control for nominalized noun-headed material. Rows such as `ka suahna leitang` and noun-headed nominalized forms show that NP structure can overlap with nominalization, but the current `-na` packet should not be dissolved into this one.

# Deferred material

Several kinds of material should remain deferred at this candidate/scoping stage.

1. Tone-marked or literature-only genitive claims such as `-á` should remain deferred until they are tied more tightly to corpus-backed, packet-safe rows.
2. Bare prefix surfaces such as isolated `a`, `ka`, or `na` should remain deferred when they are analyzer-noisy outside a controlled nominal host.
3. Pronoun-led possessor rows such as `amah a pa` or broader independent-possessor constructions should remain boundary material while pronoun routing stays settled in the completed pronoun packet.
4. Relator-adjacent and case-closed possession rows such as `Topa' tungah` should remain boundary-only.
5. Nominalized noun-headed rows such as `ka suahna leitang` or nominalized person-head material should remain boundary-only.
6. Report-only counts and any broad recursive possession chapter claim should remain outside the first slice.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer was a **basic NP ordering** grammar slice rather than a possession slice, and that narrow grammar slice now exists at `output/publication_review/grammar_np_possession_print_slice.md`.

That grammar slice leads with `hih mite`, `mi khat`, and `mi khempeuh`, because those rows let the packet make a small structural claim without reopening the completed prefix/agreement packet, the pronoun packet, or the apostrophe/genitive debates. Possession is still important in this packet, but the safest possession material remains more boundary-heavy than the cleanest NP-order rows.

The next step after that grammar slice should be NP structure / possession review notes rather than a dictionary slice. If possession is chosen before review notes, the safest fallback remains a separate possessor/possessive-prefix sub-scope led by `ka pa`, not a broad possession chapter.
