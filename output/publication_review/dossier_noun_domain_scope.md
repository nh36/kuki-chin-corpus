---
title: "Tedim Noun Domain Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for simple nouns, compound nouns, and proper nouns. The controlling layer is `output/publication_review/candidates_noun_domain.tsv`.

This dossier is not a grammar print slice, not a dictionary slice, and not a full noun chapter. Grammar, dictionary, and review-note slices do not yet exist for the noun domain.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` and `output/publication_review/review_notes_np_possession.md` identify simple nouns / compounds / proper nouns as the next missing noun-domain foundation after the NP-ordering packet.

`docs/grammar/GRAMMAR_SOURCE_INVENTORY.md` and `docs/SKELETON_GRAMMAR.md` show that noun stems, compounds, and proper nouns already have report-backed evidence but no publication-review packet yet. `docs/grammar/grammar_source_map.json` was checked only to confirm the architecture gap: simple nouns, compound nouns, and proper nouns do not yet have a clean dedicated topic layer there.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/03-noun-01-simple.md`
- `docs/grammar/reports/03-noun-02-compounds.md`
- `docs/grammar/reports/03-noun-03-proper.md`
- `docs/grammar/compound_transparency_audit.md`
- `docs/grammar/opaque_lexemes.md`

Those files are evidence sources, not the controlling editorial layer. The controlling editorial layer for this packet is `output/publication_review/candidates_noun_domain.tsv`.

# Candidate groups

The current candidate layer is intentionally small and divided into a few noun-domain groups.

## Simple noun stems

The safest simple noun anchors are `gam` and `aksi / aksi-te`.

`gam` is the cleanest current simple noun stem because the report gives clear evidence for the nominal template through `gam`, `gam-te`, `gam-'`, `gam-in`, `gam-ah`, and the explicit plural-plus-case form `gam-te-ah`. That makes it genuinely useful for grammar prose rather than merely as a lexical item.

`aksi / aksi-te` is useful because it keeps plural marking visible on an ordinary simple noun without needing to reopen NP structure or possession. It is a better simple-noun support row than a large list of one-off lexical items would be.

## Transparent compounds

The clearest current compound candidates are `minam` and `thugen`.

These rows are useful because their segmentations remain readable (`mi-nam`, `thu-gen`) and the compound report shows ordinary nominal behavior, including plural and case forms. They are good candidates for later grammar prose about transparent compounds, but they are still more lexical than the cleanest simple noun anchors.

## Opaque and lexicalized compounds

The noun-domain packet also needs explicit negative evidence.

`sanggam` is the clearest opaque lexicalized compound row: the segmentation `sang-gam` does not support the actual meaning 'brother'. `singnai` is a compound-transparency boundary row rather than a clean opaque case, because `docs/grammar/compound_transparency_audit.md` treats it as updated while `docs/grammar/opaque_lexemes.md` still keeps its etymology uneasy enough that it should not be promoted into a first compound slice.

`kholhna` is also important, but mainly as a warning that some noun-like forms are better treated as lexicalized nominals or nominalization-boundary material than as clean noun-domain anchors.

## Proper nouns

`Abraham` is the cleanest proper-noun anchor because the proper-noun report shows stable absolutive and genitive behavior without much extra structural complexity.

`Topa` should remain only as a title-like or lexicalized proper-name boundary row. It is too entangled with genitive/apostrophe behavior, theological title status, and NP-possession material to serve as a clean first proper-noun anchor.

# Existing packet boundaries

This packet must stay explicit about its boundaries with already completed packets.

## NP structure / possession boundary

`output/publication_review/review_notes_np_possession.md` remains the active noun-domain boundary control for NP ordering, possession, and apostrophe/genitive material. Rows such as `Topa' inn` or broader possessor syntax belong there rather than in the first noun-domain slice.

## Nominalization boundary

`output/publication_review/review_notes_nominalization.md` remains the boundary control for nominalized noun-headed material. Rows such as `kholhna` should stay deferred because they are better treated as lexicalized or nominalization-adjacent nouns than as clean noun-domain anchors.

## Relators / postpositions and case-marking boundary

`output/publication_review/review_notes_relators_postpositions.md` and `output/publication_review/review_notes_case_marking.md` remain the boundary controls for noun-hosted relators, case behavior, and forms whose main value is in oblique-marking syntax rather than noun-domain structure.

## Pronouns boundary

`output/publication_review/review_notes_pronouns.md` remains the boundary control for person-marking and pronoun inventory. Pronoun-led possessors or person-head material should not be pulled into the first noun-domain slice just because they contain noun-like strings.

# Deferred material

Several kinds of material should remain deferred at this candidate/scoping stage.

1. Opaque or lexicalized compounds such as `sanggam` should remain outside the first print-facing claim.
2. Compound-transparency problem rows such as `singnai` and `lamethuai` should remain outside the first print-facing claim until their etymology and compositional status are more stable.
3. Title-like or theological proper-name material such as `Topa` should remain boundary-only.
4. Nominalized lexical nouns such as `kholhna` or other `-na`-looking nouns should remain boundary-only with nominalization.
5. Rows that mainly matter for NP structure, possession, relators/postpositions, case marking, or pronouns should remain in those packets rather than being re-homed here.
6. Analyzer-noisy, report-only, or count-only noun-domain claims should remain outside the first slice.
7. Any broad noun chapter claim should remain outside the first slice.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer is a **simple noun stem** grammar slice rather than a compound or proper-noun slice.

That next step could safely lead with `gam` as the main anchor and use `aksi / aksi-te` as the supporting plural row. This would let the packet make a small noun-domain claim about simple free stems and ordinary nominal inflection without forcing transparency decisions for compounds or mostly lexical-inventory decisions for proper nouns.

Transparent compounds such as `minam` and `thugen` should remain visible as likely second-step material after that. Proper nouns should remain mostly tertiary or boundary material unless a later task explicitly chooses a separate name-focused scope.
