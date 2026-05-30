---
title: "Tedim Directionals Evidence Dossier"
---

# Directionals dossier

## Scope and status

This is the first dossier for the directionals packet. The controlling candidate layer now exists at `output/publication_review/candidates_directionals.tsv`, and `directionals` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. Grammar, dictionary, and review-note print slices for directionals have **not** yet begun.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, keep analyzer/export caveats explicit, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

`candidates_directionals.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not raw suffix searches and not generated-report counts, control the dossier. The intended reading order is `candidates_directionals.tsv` -> `dossier_directionals.md` -> future `grammar_directionals_print_slice.md` / `dictionary_directionals_print_slice.md` / `review_notes_directionals.md`.

The current extractor route is curated. It does **not** search every word ending in `khia`, `khiat`, `toh`, `lam`, `sawn`, `lut`, `suk`, `phei`, `cip`, or `tang`. Before writing this dossier, every accepted or accepted-with-caveat row was rechecked against `data/ctd_analysis/tokens.tsv`, and the current `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` values were confirmed against the analyzer export. Generated-report raw count tables remain consultable only as discovery aids and do not control the present analysis.

## Core findings

The current candidate layer supports eight narrow conclusions:

1. `-khia` has the cleanest outward anchor in `pokhia`;
2. `-khiat` is visible through one away-directional row plus nominalized `-khiat-na` boundary material;
3. `-toh` is visible through one upward row plus an explicit comitative/accompany blocker;
4. `-lam` is visible only as direction/side/manner boundary material;
5. `-sawn` is visible only cautiously and remains construction-controlled;
6. `-suk` now has one corpus-backed downward row, but it still should not be generalized from analyzer inventory alone;
7. `-lut`, `-phei`, `-cip`, and `-tang` remain deferred or not print-ready because the current TSV does not yet supply clean print-safe anchors for them;
8. broad VP/TAM analysis remains outside this packet.

The dossier therefore keeps directionals narrow. It does not broaden the packet into a raw search over directional-looking endings, and it does not import generated-report raw count claims into the evidence layer.

## Accepted / usable evidence

### Genesis 2:5: `pokhia`

`dir_khia_gen2_5_pokhia` is the clean accepted outward anchor:

> `pokhia`

The hardening pass confirms that the selected span is analyzer-backed as `po-khia`, glossed `grow-out`, with lemma/POS `po` and `V`. This is the safest current anchor for outward `-khia`.

That conclusion must stay narrow. `Pokhia` supports a later print claim that `-khia` can mark outward motion or direction, but it does **not** license raw `khia` harvesting or a claim that every orthographic `khia` sequence is directional evidence.

### Deuteronomy 9:4: `nawhkhiat`

`dir_khiat_deut9_4_nawhkhiat` remains accepted with caveat:

> `nawhkhiat`

The checked analyzer span is `nawh-khiat`, glossed `hurry-away`. The construction is useful because it keeps away-directional `-khiat` visible in a compact row rather than leaving the suffix represented only by report discovery.

The caveat is at the export layer. The current lemma/POS values remain `nawh` and `N`, so the row should be treated as construction-backed away evidence with an analyzer label caution, not as an uncomplicated finite-verb showcase. Future prose must keep `-khiat` construction-controlled rather than flattening every `...khiat` token into the same directional claim.

### Exodus 14:13: `hotkhiatna`

`dir_khiatna_exod14_13_hotkhiatna` remains accepted with caveat:

> `hotkhiatna`

The hardening pass confirms `hot-khiat-na`, glossed `save-away-NMLZ`, with nominal export profile `hot` / `N`. This row is useful because it keeps `-khiat-na` visible inside the same packet as `nawhkhiat`.

The row is boundary evidence, not a second simple finite directional anchor. It may be print-usable with caveat later, but it should not be treated as identical to finite-looking away-directional predicates.

### Numbers 9:17: `kilaktoh`

`dir_toh_num9_17_kilaktoh` remains accepted with caveat:

> `kilaktoh`

The checked analyzer span is `ki-lak-toh`, glossed `REFL-take-UP`, with lemma/POS `lak` and `V`. This is the current upward `-toh` anchor.

The row is usable only with the packet's explicit polysemy caution. `Kilaktoh` supports upward `-toh`, but it does not authorize a raw equation of `-toh = UP` in all contexts.

### Deuteronomy 32:50: `kahtohna`

`dir_tohna_deut32_50_kahtohna` remains accepted with caveat:

> `kahtohna`

The selected analyzer span is `kah-toh-na`, glossed `climb-up-NMLZ`. This keeps nominalized `-toh-na` material visible inside the packet.

Like `hotkhiatna`, this is boundary material rather than a simple finite directional predicate. It may help later print prose explain how directional morphology remains visible under nominalization, but it should not be treated as the sole basis for an unrestricted finite `-toh` claim.

### Genesis 30:9: `tawplam`

`dir_lam_gen30_9_tawplam` remains accepted with caveat:

> `tawplam`

The checked analyzer span is `tawp-lam`, glossed `end-TOWARD`, with lemma/POS `tawp` and `N`. This is exactly why the row remains boundary evidence only. It keeps `-lam` visible in the directionals packet without pretending the current layer already supports a simple clean verbal directional suffix analysis.

Future prose should therefore treat `-lam` as direction/side/manner boundary material unless a later candidate layer adds a clearer verbal anchor.

### Ezra 9:9: `piasawn`

`dir_sawn_ezra9_9_piasawn` remains accepted with caveat:

> `piasawn`

The hardening pass confirms `pia-sawn`, glossed `give-toward`, with lemma/POS `pia` and `V`. This is cleaner for the first dossier than kinship-heavy or otherwise ambiguous `-sawn` rows.

The construction still needs caution. `Piasawn` is usable as toward evidence, but the dossier must keep `-sawn` construction-controlled because easy hits can drift into kinship, lexicalized, or continuative-looking material.

### Genesis 11:5: `paisuk`

`dir_suk_gen11_5_paisuk` remains accepted with caveat:

> `paisuk`

The checked analyzer span is `pai-suk`, glossed `go-DOWN`, with lemma/POS `pai` and `V`. This gives the packet one corpus-backed downward row and confirms that `-suk` is not present only because of analyzer unit-test inventory.

That matters methodologically. Analyzer tests do support `-suk`, but the print-facing packet should still rely on corpus-backed candidate rows such as `paisuk`, not on analyzer inventory alone.

## Blocked / overlap-control evidence

### Exodus 34:24: `paitoh`

`dir_toh_exod34_24_paitoh_overlap` is the packet's explicit blocked overlap row:

> `paitoh`

This row matters because `-toh` is not simply "UP" in all contexts. The current candidate layer keeps `kilaktoh` as the usable upward row, but it pairs that with `paitoh` as an excluded comitative/accompany control.

That control also matches the existing analyzer tests, where `paitoh` is treated as lexicalized `go-accompany`. Future grammar prose must therefore present upward `-toh` together with the comitative/accompany caveat rather than implying that every `-toh` token is directional.

## Nominalized directional forms

The current packet contains two explicit nominalized directional rows:

- `hotkhiatna` -> `hot-khiat-na` -> `save-away-NMLZ`
- `kahtohna` -> `kah-toh-na` -> `climb-up-NMLZ`

These rows keep directional morphology visible under nominalization, and they are useful because they show how `-khiat` and `-toh` remain morphologically legible even where the export is not presenting a simple finite predicate.

They should not, however, be treated as identical to simple finite directional verbs. At most they are print-usable with caveat, and they cannot stand alone as the only support for a finite directional suffix claim.

## -lam boundary material

`Tawplam` is the current `-lam` row, and it should stay boundary material:

> `tawplam`

The row clearly involves direction, side, or manner territory, but the export profile remains nominal (`tawp` / `N`) and the packet does not yet have a clean verbal `-lam` anchor. Candidate evidence should therefore not silently turn every `-lam` form into a clean verbal directional suffix.

Future grammar wording should keep `-lam` cautious and construction-bound until a later packet stage can phrase it more fully.

## Deferred material

Several forms remain visible only as deferred or blocked material in this first dossier:

- `uilut` keeps `-lut` visible as analyzer-listed inward material, but the current corpus-backed row is not yet a clean print-safe inward anchor;
- `paiphei` keeps `-phei` visible, but the current export gloss `go-enter` does not justify a clean horizontal directional claim;
- `cip` remains report-visible but analyzer-noise-bound in the current packet, with lexical `cip = tight` rather than directional evidence;
- `tang` remains report-visible but not candidate-backed as clean endpoint-directional evidence, because the current export gloss is lexical `embed`;
- analyzer-test-only support should not promote any additional directional form unless the packet also has a corpus-backed candidate row.

The same caution applies to `-sawn` and `-suk` in a different way: they are no longer absent from the packet, but they still should not be generalized from inventory or unit tests alone.

## Print implications

### Safe for a future grammar slice

The following material is candidate-backed and safe to carry forward into a later grammar slice:

- `-khia` as outward evidence, anchored by `pokhia`;
- `-khiat` as away evidence, anchored by `nawhkhiat`, with explicit analyzer label caution;
- nominalized `-khiat-na` material through `hotkhiatna`, only with boundary caveat;
- `-toh` as upward evidence through `kilaktoh`, only with explicit comitative/accompany caution;
- nominalized `-toh-na` material through `kahtohna`, only with boundary caveat;
- `-lam` only as direction/side/manner boundary material;
- `-sawn` only through the current cautious `piasawn` row;
- `-suk` only through the current corpus-backed `paisuk` row with its recorded caveat.

### Not yet print-safe

The following material should stay out of the first print-facing slice:

- raw generated-report counts or count claims;
- treating every `khia`, `khiat`, `toh`, `lam`, `sawn`, `lut`, `suk`, `phei`, `cip`, or `tang` ending as directional evidence;
- treating `paitoh` as upward `-toh`;
- treating nominalized `-na` forms as equivalent to finite directional verbs;
- promoting `-lut`, `-phei`, `-cip`, or `-tang` without cleaner analyzer-backed corpus rows than the current TSV provides;
- broad VP-slot prose or broad TAM analysis.

## Next steps

The next directionals step after this dossier should be:

1. draft `output/publication_review/grammar_directionals_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_directionals_print_slice.md`;
3. then add `output/publication_review/review_notes_directionals.md`.

The dossier is now the interpretive control for that later slice work, but grammar, dictionary, and review-note print slices for directionals have **not** yet begun. Broad TAM, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
