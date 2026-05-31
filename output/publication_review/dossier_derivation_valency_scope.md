---
title: "Tedim Derivation / Valency Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for derivation and valency. The controlling candidate layer now exists at `output/publication_review/candidates_derivation_valency.tsv`. This dossier is not a grammar print slice and not a full verbal morphology chapter.

The packet is intentionally small. Its job is to identify a narrow future print-facing sub-scope for derivation / valency while keeping clear boundaries with VP structure / stacking, TAM, directionals, negation, pronouns/prefixes, and transitivity. A grammar print slice now exists at `output/publication_review/grammar_derivation_valency_print_slice.md`, and review notes now exist at `output/publication_review/review_notes_derivation_valency.md`, but no dictionary slice exists yet for derivation/valency.

# Architecture control

`output/publication_review/whole_grammar_coverage_audit.md` and `output/publication_review/review_notes_vp_structure_stacking.md` are the reasons this scope was selected now.

The whole-grammar audit identified derivation and valency as a first-band missing domain and also kept transitivity adjacent to that domain rather than treating it as solved elsewhere. The VP structure / suffix stacking review notes then made the next packet choice more specific: `ciahsakkik`, `bawlsakthei`, `paikhiatsak`, `-sak`, `-pih`, and `ki-` were all repeatedly deferred out of the VP packet and into this derivation/valency packet.

This scope is also architecture-controlled by `docs/grammar/grammar_source_map.json`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `docs/SKELETON_GRAMMAR.md`. The source map routes the core packet through `causative-sak`, `benefactive-sak`, `applicative-pih`, and `reflexive-ki`, while the inventory and skeleton grammar show that derivation/valency sits inside a larger verbal-morphology chapter that should not be rewritten all at once.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/05-verb-08-derivational.md`
- `docs/grammar/reports/05-verb-09-valency.md`
- `docs/grammar/reports/05-verb-10-combinations.md`
- `docs/grammar/reports/05-verb-12-transitivity.md`
- `docs/grammar/morphemes/06-derivational.md`
- `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`

Existing tests also matter as evidence/control:

- `tests/test_sak_caus_benf.py` keeps the Form I / Form II distinction around `-sak` explicit at analyzer level.
- `tests/test_vp_slots.py` keeps derivation-heavy stacks such as `bawlsakthei` visible and shows where derivation runs into VP stacking.
- `tests/test_prefix_agr_poss.py` is only boundary control, but it matters because `ki-` is prefixal and the derivation packet must not collapse into a broad prefix/agreement rewrite.

The candidate TSV is the controlling layer for this packet. The reports, morpheme file, and literature review are discovery and interpretation sources; they do not themselves decide what becomes future print-facing evidence.

# Candidate groups

## `-sak`

The safest current candidate group is `-sak`, but it is safest only if the packet keeps causative and benefactive rows separate in the candidate layer.

`Paisak` is the clearest current causative anchor. It is analyzer-backed, regression-backed through `tests/test_sak_caus_benf.py`, and already aligned with the `causative-sak` route in `docs/grammar/grammar_source_map.json`. That makes it the safest future print-facing candidate for a narrow `-sak` grammar slice.

`Muhsak` is the clearest current benefactive split row. It gives the packet direct regression evidence that Form II plus `-sak` should not be flattened back into a simple causative line. At the same time, the literature still leaves open whether the grammar should present causative and benefactive `-sak` as two functions of one suffix or as two separate editorial subsections. The packet therefore treats the split as real enough for candidate control but still theoretically unsettled at the level of later prose framing.

That leads to the current dossier answer for `-sak`: the packet should proceed as if the causative versus benefactive split is real and useful for future print anchors, while still preserving the unresolved higher-level question of whether these are two readings of one suffix or two editorially separate subtopics.

## `-pih`

`Paipih` is the strongest current `-pih` candidate because the reports already provide a compact corpus row and the analyzer keeps its segmentation stable as `pai-pih`. Even so, the packet must keep the function label cautious.

The literature repeatedly treats `-pih` as a comitative applicative associated with Stem II behavior, while the report glosses and analyzer output are broad enough to leave applicative, associative, benefactive, and comitative readings partly unresolved. `Mipihte` sharpens that caution further: it shows that some pih-looking strings are nominal or lexicalized and should not be promoted as verbal derivation evidence.

That leads to the current dossier answer for `-pih`: the packet has one future anchor candidate, but the function label remains unresolved enough that a later slice must stay narrow and construction-controlled.

## `ki-`

`Ki-` clearly belongs in this packet, but it is the least settled candidate group.

The evidence layers describe `ki-` as reflexive, reciprocal, middle, and passive-like. `Kisep` is the clearest semantically transparent verbal reflexive row now available in the evidence set, so it is the best future anchor candidate. `Kigen`, by contrast, is important boundary evidence but not a safe first anchor, because the analyzer gloss is lexicalized and the form sits on the middle/passive-like edge of the category.

The dossier answer for `ki-` is therefore mixed: productive verbal reflexive `ki-` probably deserves a future slice, but the packet must keep lexicalized ki- stems and prefix/agreement overlap explicit. This packet should not absorb the whole prefix system, and it should not reuse `ki-` material that really belongs under the completed pronoun/prefix packet or a future agreement packet.

## Derivation-heavy stacks

`Ciahsakkik`, `bawlsakthei`, and `paikhiatsak` are the clearest derivation-heavy stacks already deferred by `review_notes_vp_structure_stacking.md`. They belong in this packet as discovery evidence, because they show where derivation interacts with aspect, modals, and directionals.

They are not yet safe first print anchors. `Ciahsakkik` still depends on aspect interaction, `bawlsakthei` still depends on modal/TAM interaction, and `paikhiatsak` still depends on directional interaction. They help define the packet boundary more than they define the first grammar slice.

## Transitivity-adjacent evidence

The transitivity report should stay adjacent but not be absorbed into the first derivation/valency slice. `Piangsak` is the clearest current transitivity-adjacent row because it is causative-looking, highly lexicalized, and strongly transitive in `docs/grammar/reports/05-verb-12-transitivity.md`.

That is exactly why it should remain adjacent evidence rather than a first print anchor. The first derivation packet should not become a lexical transitivity chapter.

# Existing packet boundaries

This packet must remain narrow against already completed or partly completed packet domains:

- `output/publication_review/review_notes_vp_structure_stacking.md` already owns the constructional stacking packet and should not be reopened through derivation-heavy stacks.
- `output/publication_review/review_notes_tam.md` already owns compact TAM anchors and should not be reopened through `bawlsakthei` or other modal stacks.
- `output/publication_review/review_notes_directionals.md` already owns directional anchors and should not be reopened through `paikhiatsak`.
- `output/publication_review/review_notes_negation.md` remains boundary control for stacks that drift into negative modal territory.
- `output/publication_review/review_notes_pronouns.md` and `tests/test_prefix_agr_poss.py` remain boundary control for prefixal material, especially `ki-`, so this packet does not become a broad agreement or possessive-prefix chapter.

Transitivity also stays adjacent rather than absorbed. `docs/grammar/reports/05-verb-12-transitivity.md` is essential evidence for argument structure, but the packet should use it to sharpen derivation decisions, not to replace a future transitivity packet.

# Deferred material

The following material should stay deferred in this first candidate/scoping packet:

- lexicalized or analyzer-opaque `ki-` forms such as `kigen`, plus nominalized or lexicalized `ki-` stems such as `kipat` and `kipan`;
- nominal or lexicalized `-pih` material such as `mipihte`;
- derivation-heavy stacks whose main value is overlap with VP stacking, TAM, or directionals, such as `ciahsakkik`, `bawlsakthei`, and `paikhiatsak`;
- transitivity rows that are useful adjacent evidence but not yet derivation anchors, such as `piangsak`;
- prefix/agreement-heavy material involving `hong-`, `kong-`, or the broader prefix system;
- broader lexical causative material such as suppletive or aspiration-based causatives, which belongs in background interpretation for now rather than in the first print-facing sub-scope.

The common principle is that the first derivation/valency slice should start from the clearest productive morphology, not from the noisiest interactions.

# Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate/scoping layer is a **narrow `-sak` grammar slice**, not a full derivation chapter.

More specifically, the safest route is a very small grammar print slice that starts from:

1. `paisak` as the clearest causative anchor;
2. `muhsak` as the clearest benefactive split row;
3. explicit caveat language that keeps open whether the packet is describing two readings of one suffix or two editorial subsections of the same suffixal domain.

`-pih` and `ki-` should remain present in the dossier and candidate layer, but they are not yet as clean as `-sak` for the first print-facing slice. Transitivity should stay adjacent, and the derivation-heavy stacks should remain deferred boundary material until the packet has a stable core.
