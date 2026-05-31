---
title: "Tedim VP Structure / Suffix Stacking Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for VP structure and suffix stacking. The controlling candidate layer now exists at `output/publication_review/candidates_vp_structure_stacking.tsv`. This dossier is not a grammar print slice and not a full VP chapter.

The packet is intentionally small. Its job is to decide which VP-slot or suffix-stacking patterns are clean enough to become future print-facing anchors, which patterns are already owned by completed packets, and which patterns should remain deferred because they belong primarily to derivation/valency, negation, sentence-final particles, agreement/prefixes, or subordination. The grammar, dictionary, and review-note print slices for VP structure/stacking do **not** yet exist.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` selected this scope. That audit identified **VP structure** and **suffix combinations / stacking** as first-band missing domains and said that a coverage/priority decision should come before any printable full grammar bundle.

The architecture control for this packet is therefore broader than the two VP reports alone:

- `output/publication_review/whole_grammar_coverage_audit.md` is the reason this scope was chosen now;
- `docs/grammar/grammar_source_map.json` is the canonical topic/construction layer, but it routes this domain only indirectly through topics such as `perfective-ta`, `completive-zo`, `irrealis-ding`, `ability-thei-theih`, `directional-suffixes`, `causative-sak`, `benefactive-sak`, `applicative-pih`, `reflexive-ki`, `negation-lo-kei`, and `major-subordination`;
- `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md` and `docs/SKELETON_GRAMMAR.md` make clear that VP structure and suffix combinations are larger than the already completed TAM and directional packets.

# Evidence protocol

`docs/grammar/reports/05-verb-02-vp-structure.md` and `docs/grammar/reports/05-verb-10-combinations.md` are the main discovery and evidence sources for this first pass. `tests/test_vp_slots.py` is the main existing regression evidence because it already protects a few analyzer-backed slot and stack parses.

The candidate TSV is the controlling layer for this packet. Generated-report counts and report tables are discovery aids only. This dossier should therefore be read in the order:

1. `candidates_vp_structure_stacking.tsv`
2. `dossier_vp_structure_stacking_scope.md`
3. any later narrow grammar slice, if one is explicitly chosen

# Existing packet boundaries

This packet must stay narrow because several nearby domains are already completed and should **not** be reopened accidentally.

- The TAM packet (`candidates_tam.tsv`, `dossier_tam_scope.md`, `review_notes_tam.md`) already owns compact anchors such as `bawlzo`, `omding`, `bawlthei`, and the overlap controls `dingin`, `khiathei ding om lo`, and `khia-ta`.
- The directionals packet (`candidates_directionals.tsv`, `dossier_directionals.md`, `review_notes_directionals.md`) already owns compact directional anchors such as `pokhia` and the cautions around directional stacking or analyzer noise.
- The negation packet (`review_notes_negation.md`) already owns clause-level negation and should not be reopened through negative modal stacks.
- The sentence-final particles packet (`review_notes_sentence_final_particles.md`) already owns clause-final overlap and should not be reopened through full-clause `ta hi`, `zo`, or similar material.
- The relators/postpositions packet (`candidates_relators_postpositions.tsv`, `review_notes_relators_postpositions.md`) remains relevant as a boundary control because many VP-report examples contain locative or relator-hosted phrases that are clause-internal context, not VP-slot evidence.

The first VP packet should therefore aim at what is genuinely missing: construction-controlled evidence for VP slot ordering or multi-suffix stacking that is **not already** a completed TAM, directional, negation, sentence-final, or relator/postposition claim.

# Candidate groups

## Simple VP slot-order baselines

The simplest post-stem material is already packeted elsewhere. `bawlzo` and `pokhia` are useful here only as baseline boundary anchors showing that the repository already has compact V+ASPECT and V+DIR evidence. Those rows do **not** justify a new VP slice by themselves because they are already owned by the TAM and directionals packets.

That matters methodologically. The new packet should not start by redescribing completed packets as if they were new VP evidence.

## Aspect plus modal stacking

`Bawlzoding` is the clearest genuinely missing stack in the current repository. `tests/test_vp_slots.py` already keeps it visible as a combined aspect-plus-modal form, and it shows the ordering question directly: completive material appears before irrealis material inside one verbal complex.

The row is still caveated because the current analyzer gloss is noisy (`make-south-IRR`). Even so, `bawlzoding` is the strongest current candidate for a later narrow print-facing suffix-stacking slice precisely because it is already regression-backed and because it reaches beyond the completed TAM packet without yet requiring a full derivation chapter.

## TAM plus directional stacking

`Khia-ta` is real discovery evidence, but it is still boundary material rather than a clean new anchor. The current TAM packet already keeps it visible as directional-plus-aspect overlap, and the directionals packet already warns against broad VP-slot expansion through directional material.

This makes `khia-ta` important for scoping but not yet safe for print. It is a cross-packet warning row, not the lead example for a first VP slice.

## Derivational plus aspect or modal stacking

`Ciahsakkik`, `bawlsakthei`, and `paikhiatsak` show that multi-suffix verbal complexes are unquestionably real in the reports and tests. They also show why the packet must stay conservative. Once `-sak`, `-pih`, or other derivational material enters the stack, the analysis quickly becomes a derivation/valency problem rather than a clean VP-slot-order problem.

For that reason these rows are discovery-worthy but deferred. They belong in the candidate layer so the packet records them explicitly, but they should wait for the derivation/valency packet before they are turned into print-facing grammar claims.

## Negative modal or clause-bound stacks

`Khiathei ding om lo` and `dingin` show the other main boundary problem. Some visible stacks are real, but they are not primarily VP-slot evidence. `Khiathei ding om lo` is already a TAM-negation overlap control, while `dingin` belongs as much to clause linkage and subordination as it does to VP morphology.

These rows therefore stay in the packet only as boundary evidence. They explain why a first VP slice must remain narrower than “all available verbal stacks”.

# Deferred material

The following material should stay deferred in this first VP candidate/scoping packet:

- derivation/valency-heavy stacks involving `-sak`, `-pih`, `ki-`, or other valency-changing material as the main issue;
- agreement and prefix domains such as `hong-`, `kong-`, and broader object-prefix ordering, which belong with the future prefix/agreement packet;
- clause-bound or subordinating material such as `dingin`, which belongs with the future subordination packet;
- negation-dominated stacks such as `khiathei ding om lo`, which should remain controlled by the negation and TAM packets;
- sentence-final overlap material that would reopen the sentence-final particles packet;
- noisy or lexicalized report rows that appear in generated reports but are not yet clean analyzer-backed print anchors.

The common principle is the same as in the completed packets: discovery evidence should be retained, but raw report visibility is not enough to make something print-ready.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer is **not** a full VP chapter and **not** a broad stacking inventory.

The safest next step would be a **narrower subset**: a small grammar print slice on suffix stacking across already-completed packets, led by the clearest genuinely missing stack `bawlzoding` and supported by a few boundary-controlled order diagnostics from the completed TAM and directionals packets. That later slice should still leave derivational stacks, negation-heavy stacks, and clause-bound `dingin` material out of the core prose.

In other words, if this packet moves to a grammar slice later, it should begin with **narrow suffix stacking**, not with an attempt to rewrite the whole VP chapter.
