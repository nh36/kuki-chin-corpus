---
title: "Review Notes: Tedim VP Structure / Suffix Stacking Print Slice"
---

# What works

The VP structure / suffix stacking packet is now aligned at its current constructional maturity level. It has a candidate TSV, a scoping dossier, a grammar print slice, and tests: `candidates_vp_structure_stacking.tsv`, `dossier_vp_structure_stacking_scope.md`, `grammar_vp_structure_stacking_print_slice.md`, and the associated test files. Those controlling files should be read together with the supporting/background sources `docs/grammar/reports/05-verb-02-vp-structure.md`, `docs/grammar/reports/05-verb-10-combinations.md`, and the regression evidence in `tests/test_vp_slots.py`.

The packet’s single safe first-slice claim is now stable. `bawlzoding` is the central print-usable-with-caveat anchor, and the grammar slice keeps the claim narrow: the current evidence supports the ordering observation `verb stem + completive/aspectual material + irrealis/modal material`. The row is usable because it is constructional VP-stacking evidence, not because every analyzer label on it is already semantically perfect. The current analyzer gloss remains noisy (`make-south-IRR`), so the packet is right to use the form as suffix-order evidence without over-trusting that gloss.

The surrounding packet boundaries also now work in a stable way. `tests/test_vp_slots.py` gives the packet real regression evidence rather than report-only discovery. `bawlzo` and `pokhia` remain already-owned baseline rows from completed packets, not new VP claims: `bawlzo` stays under the TAM packet, and `pokhia` stays under the directionals packet. Those boundaries remain explicit through `review_notes_tam.md`, `review_notes_directionals.md`, `review_notes_negation.md`, `review_notes_sentence_final_particles.md`, and `review_notes_relators_postpositions.md`.

# Why there is no ordinary dictionary slice yet

There is no ordinary dictionary slice yet because this packet is constructional rather than lexical. `Bawlzoding` is useful because it shows suffix ordering, not because it should become a dictionary headword.

That distinction matters editorially. The safe first-slice claim is about a multi-suffix verbal complex, not about promoting `bawlzoding` as a lexical entry. Dictionary treatment should remain with the morphemes and packet domains already handled elsewhere, especially the TAM and directional material that supply `bawlzo` and `pokhia` as completed-packet baselines.

# What does not yet work

This packet does not provide a full VP chapter. It does not provide a full suffix-slot template. It does not provide a derivation/valency analysis, and it does not provide a clause-linkage or subordination analysis.

It also does not reopen TAM, directionals, negation, sentence-final particles, or relators/postpositions through one constructional stacking row. That restraint is a strength, not a weakness. The packet is useful precisely because it keeps its claim smaller than a broad verbal rewrite.

# Boundary and deferred material

The packet’s deferred and boundary-only rows are now explicit.

- `khia-ta` remains TAM/directional overlap rather than first-slice core VP evidence.
- `ciahsakkik`, `bawlsakthei`, and `paikhiatsak` remain derivation/valency-heavy stacks and should wait for the derivation/valency packet.
- `khiathei ding om lo` remains TAM-negation overlap rather than clean core VP-stack evidence.
- `dingin` remains clause-bound irrealis/subordination material and should wait for a subordination packet.
- any broad VP slot template remains out of scope for this packet.
- any attempt to reopen TAM, directionals, negation, sentence-final particles, or relators/postpositions through this packet remains out of scope.

These deferrals are the main reason the next missing first-band domain is now clearer than it was before. The packet repeatedly reaches derivation-heavy material and then has to stop.

# Recommended next editorial task

With review notes added, the VP structure / suffix stacking packet is now ready for human review at its current constructional maturity level.

The next substantive missing first-band domain should be derivation / valency candidate scoping. The current VP packet repeatedly defers `-sak`, `-pih`, `ki-`, and other derivation-heavy stacks to that future packet, so derivation / valency is now the clearest next narrow scope after human review of the present constructional packet.
