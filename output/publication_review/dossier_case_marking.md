---
title: "Tedim Case-Marking Evidence Dossier"
---

# Case-marking dossier

## Evidence-layer status

Case marking is an older publication-review slice family that now has a manually curated analyzer-aware candidate layer at `output/publication_review/candidates_case_marking.tsv`. That file is the current evidence control for the packet, but `case_marking` is **not** yet a supported extractor topic in `scripts/publication_review/extract_candidates.py`. The present candidate layer is therefore a curated retrofit rather than a corpus-wide automatic search.

The packet should now be read in the order `candidates_case_marking.tsv` -> `dossier_case_marking.md` -> `grammar_case_marking_print_slice.md` / `dictionary_case_markers_print_slice.md` -> `review_notes_case_marking.md`. This keeps the print slices conservative: the new candidate layer explains which existing claims are supported directly, which ones remain caveated, and which ones stay blocked for now.

## Candidate summary

| Construction | Candidate rows | Current reading |
| --- | --- | --- |
| ergative `-in` | `case_in_gen4_3_kain_in` | accepted print anchor |
| locative `-ah` | `case_ah_gen11_28_khuaah` | accepted plain locative control |
| directional/allative `-a` | `case_a_gen2_7_a_review` | deferred pending cleaner analyzer support |
| source `-pan` | `case_pan_matt5_19_lakpan` | accepted with caveat as source marking on a relator noun |
| source `-panin` | `case_panin_gen12_1_inn_panin` | accepted with caveat as source-marking evidence, but structurally conservative |
| comitative/accompaniment `-tawh` | `case_tawh_gen14_24_kei_tawh` | accepted accompaniment anchor |
| material/instrumental extension of `-tawh` | `case_tawh_gen2_7_leivui_tawh` | accepted with caveat as extension use |
| relator-noun-plus-case constructions | `case_relator_gen1_6_laizangah`, `case_relator_gen1_14_vantungah`, `case_relator_gen2_19_kiangah`, `case_relator_gen1_11_sungah`, `case_relator_gen1_2_tungah`, `case_pan_matt5_19_lakpan` | keep distinct from bare suffix examples |
| ambiguity/noise controls | `case_in_gen1_3_ciangin_review`, `case_a_gen2_7_a_review` | show why raw string extraction would overgenerate |

## Ergative `-in`

`case_in_gen4_3_kain_in` remains the accepted anchor for ergative `-in`. Genesis 4:3 gives a clean `Kain in` span with a proper-noun-plus-ergative analysis, and it is still suitable as the main print example in the grammar and dictionary slices.

The packet is right to keep the `-in` discussion narrow. `case_in_gen1_3_ciangin_review` shows why raw `-in` extraction overgenerates: forms such as `ciangin` can be conjunctional or other non-case material rather than nominal ergative case. The dossier therefore treats `ciangin` as an ambiguity-control row, not as a case example.

## Locative `-ah`

The candidate layer supports keeping locative `-ah` in the packet, but it also shows that the packet should preserve two subtypes:

1. plain noun-plus-locative evidence such as `case_ah_gen11_28_khuaah` (`khua-ah`);
2. relator-noun-plus-case constructions such as `laizangah`, `vantungah`, `kiangah`, `sungah`, and `tungah`.

This distinction matters because the current print slice already mixes a simple locative reading with spatially relational stems. That is analytically right, but the two should not be flattened into one undifferentiated `-ah` bucket.

The analyzer export also needs to be read carefully here. Several locative or relator rows show `pos_span=FUNC`, even where the grammatical analysis treats the base as nominal or relational. That should be read as an export limitation rather than as decisive proof that the base is not noun-like. In practice, rows such as `khua-ah`, `lai-zang-ah`, and `vantung-ah` are still useful evidence for the packet, but their POS labels are not the final analysis by themselves.

## Directional/allative `-a`

The candidate layer intentionally keeps `case_a_gen2_7_a_review` deferred. The current export does not yet safely extract allative or directional `-a` without heavy contamination from pronominal or other functional `a` tokens, so the dossier does **not** promote `-a` into a print-ready case marker.

This also means the packet should not collapse `-a` into `-ah`. The candidate file correctly keeps them separate. A future analyzer or extractor improvement would be needed before `-a` can be used confidently in print.

## Source `-pan`

`case_pan_matt5_19_lakpan` supports the existing slice's treatment of `-pan` as source marking, but it does so on a relator noun rather than as a bare suffix example. The segmentation `lak-pan` matters: this is source marking on `lak`, not just an abstract suffix floating free of spatial nominal structure.

That is an important positive result for the packet. It supports keeping case marking and relator nouns in the same editorial discussion rather than splitting them into unrelated chapters.

## Source `-panin`

`case_panin_gen12_1_inn_panin` is accepted as source-marking evidence and is print-usable with caveat. The candidate row therefore supports the current packet's conservative stance: `inn panin` can already be cited as a source expression, but the dossier should not force a fully settled compositional analysis.

The analyzer segmentation `pan-in` is useful evidence, but it is not the final structural analysis by itself. For now, the safest packet-level claim is that `-panin` belongs in the same source-marking domain as `-pan`, while the exact structural account remains under review.

## Comitative / associative `-tawh`

The candidate layer confirms that the packet is right to distinguish two uses of `-tawh`:

- `case_tawh_gen14_24_kei_tawh` is the clean accompaniment anchor;
- `case_tawh_gen2_7_leivui_tawh` is a material or means extension.

This split should remain explicit in both grammar and dictionary work. The packet is strongest when it does **not** collapse both rows under a vague English gloss such as *with*. Core accompaniment is real, but so is the extension into material or instrumental readings.

## Relator nouns

The relator-noun-plus-case rows are not just extra suffix examples. `laizangah`, `vantungah`, `kiangah`, `sungah`, `tungah`, and `lakpan` show that Tedim spatial grammar often builds phrases on relational stems that then host locative or source marking.

The dossier therefore keeps a two-layer analysis:

1. markers such as `-ah`, `-pan`, `-panin`, and `-tawh`;
2. relational nouns or stems such as `lak`, `sung`, `kiang`, `tung`, `laizang`, and `vantung` that combine with those markers.

This is the main interpretive payoff of the candidate layer. The existing case-marking packet should preserve relator nouns as part of the same discussion, not flatten them into a suffix-only inventory.

## Packet review decision

| Item | Candidate support | Current print-slice status | Recommended action |
| --- | --- | --- | --- |
| `-in` | `case_in_gen4_3_kain_in` accepted; `case_in_gen1_3_ciangin_review` blocked as ambiguity control | existing grammar and dictionary already use `Kain in` conservatively | keep current `-in` example and continue treating raw `-in` extraction as unsafe |
| `-ah` | plain locative control plus several relator-noun-plus-case rows | current slices already illustrate both simple and relational locatives | keep `-ah`, but continue to clarify simple locative vs relator-noun examples |
| `-a` | only deferred review row | not safely represented in the packet as a candidate-backed marker | keep `-a` deferred |
| `-pan` | accepted-with-caveat source row on `lak-pan` | current slices already treat it as source marking | keep `-pan` as source on a relator noun, not as a bare suffix example |
| `-panin` | accepted-with-caveat source row with conservative note | current slices already describe it cautiously | keep `-panin` as source-marking evidence, but preserve the structural caveat |
| `-tawh` | one accepted accompaniment row and one accepted-with-caveat extension row | current slices already distinguish the two uses | keep `-tawh` split between accompaniment and material/instrumental extension |
| relator nouns | multiple accepted relator-noun-plus-case rows plus `lakpan` | current slices already flag relator nouns as important | preserve relator nouns as part of the case/postposition discussion |
