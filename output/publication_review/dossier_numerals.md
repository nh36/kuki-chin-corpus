---
title: "Tedim Numerals Evidence Dossier"
---

# Numerals dossier

## Scope and status

This is the first dossier for the numerals retrofit. The controlling candidate layer now exists at `output/publication_review/candidates_numerals.tsv`, and `numerals` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. Grammar, dictionary, and review-note print slices for numerals have **not** yet begun.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, record analyzer/export caveats explicitly, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

`candidates_numerals.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not raw string hits and not generated-report counts, control the dossier. The intended reading order is `candidates_numerals.tsv` -> `dossier_numerals.md` -> future `grammar_numerals_print_slice.md` / `dictionary_numerals_print_slice.md` / `review_notes_numerals.md`.

The current extractor route is curated. It does **not** search every `khat`, `nih`, `kua`, `sawm`, `za`, or numeral-looking token in the corpus. Before writing this dossier, every accepted or accepted-with-caveat row was rechecked against the analyzer export, and the current `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` values were confirmed against `data/ctd_analysis/tokens.tsv`.

## Core findings

The current candidate layer supports seven narrow conclusions:

1. basic post-nominal counting phrases are already represented by `kum nih` and `ni sagih`;
2. compound tens are represented by `kum sawmkua`;
3. ordinals are represented by `nihna`;
4. occurrence-counting or multiplicative material is represented by export-backed `sawmvei`;
5. large biblical number phrases are visible through the Genesis 5:27 row;
6. `kua` ambiguity is now controlled explicitly on both the numeral and interrogative sides;
7. `khat` remains on the numeral/indefinite boundary, and distributive reduplication remains deferred because the expected repeated numeral span is not currently analyzer-backed.

The dossier therefore keeps numerals narrow. It does not broaden the packet into a raw search over all numeral-looking tokens, and it does not import the generated report's raw count tables into the evidence layer.

## Accepted / usable evidence

### Genesis 11:10 and Genesis 7:10: basic counting phrases

`num_card_gen11_10_kum_nih` and `num_card_gen7_10_ni_sagih` are the cleanest accepted rows in the current packet:

- `kum nih`
- `ni sagih`

Both rows are analyzer-backed without special export noise in the relevant window. They establish that the candidate layer already has conservative examples of post-nominal year and day counting without requiring a general numeral survey.

### Genesis 5:9: `kum sawmkua`

`num_compound_gen5_9_kum_sawmkua` is the accepted compound-ten row:

> `kum sawmkua`

This row is important because it keeps numeral `kua = nine` visible inside a clearly numeral construction. The analyzer/export caveat is in the lemma and POS layer rather than in the segmentation: the segmentation and gloss are clear (`sawm-kua`, `ten-nine`), but the current lemma export is flattened to `kum | sawm` and the POS span is `N | N`. That caveat should be recorded, not normalized away silently, because the compound-ten reading is constructionally secure even when the export labels are simplified.

### Genesis 7:11: `nihna`

`num_ordinal_gen7_11_nihna` is the current accepted ordinal row:

> `nihna`

The analyzer confirms the segmentation `nih-na` and the gloss `two-NMLZ`. The main export caveat is that `pos_span` is `N`. That should be treated as a label limitation in the current export, not as a reason to reject the row as ordinal evidence.

### Genesis 31:7: `sawmvei`

`num_mult_gen31_7_sawmvei` is the accepted-with-caveat occurrence-counting row:

> `sawmvei`

The dossier keeps the fused export-backed form as the control. The generated report paraphrases this example as `vei sawm`, but that wording should not be silently substituted into the candidate layer or later print prose without saying so explicitly. The current analyzer export preserves `sawm-vei` with gloss `ten-times`, lemma `sawm`, and POS `N`, so `sawmvei` is the form that controls this pass.

### Genesis 5:27: large-number phrase

`num_large_gen5_27_kum_zakua_kum_sawmguk_kua` keeps a large-number phrase visible:

> `kum zakua le kum sawmguk le kua`

This row is accepted with caveat because the numeral context is clear, but several export quirks need to stay visible. The hundred-plus-nine material is compressed into `zakua` rather than a fully separated `za ... kua` sequence, and the final standalone `kua` is glossed as `who` even though the wider construction is numeral, not interrogative. The dossier should therefore treat this as a stable large-number row with explicit analyzer caveats rather than as a fully polished print anchor.

### Genesis 32:24: `mi khat`

`num_boundary_gen32_24_mi_khat` remains accepted with caveat:

> `mi khat`

This is useful because it is analyzer-backed and keeps `khat` visible in the packet. It is not a simple unqualified print anchor for bare numeral `one`, however. The English context "a man" shows exactly why this row belongs on the numeral/indefinite boundary rather than inside an uncomplicated cardinal paradigm.

## Kua ambiguity

`Kua` needs its own control section because it has two live readings in the current repository:

1. numeral `nine` in numeral constructions such as `sawmkua` and the Genesis 5:27 large-number row;
2. interrogative `who` in the already-stabilized interrogatives packet.

The blocked numerals false-friend row is Genesis 48:8:

> `Hihte kua ahi hiam?`

That row stays excluded from numerals because `kua` there is interrogative `who`, not numeral `nine`. Future numerals prose must therefore never use raw `kua` hits as numeral evidence without constructional context.

## Khat boundary

`Mi khat` is retained because it is analyzer-backed and genuinely useful, but it remains boundary evidence rather than a plain numeral exemplar. The clause is numerically relevant because it contains `khat`, yet the English context "a man" shows why this row can slide toward indefinite reference.

The dossier therefore keeps `mi khat` as accepted-with-caveat boundary material. It links forward to later quantifier work, but it does **not** start a quantifiers retrofit inside the numerals packet.

## Ordinals

`Nihna` is the current accepted ordinal candidate, and it is enough to keep the ordinal subsection visible in this first dossier. The generated report also mentions suppletive `masa` for `first`, but the present candidate layer does not yet promote `masa`, so the dossier leaves it deferred.

The ordinal evidence should therefore stay narrow. This is not yet a full ordinal paradigm.

## Multiplicative / occurrence counting

The current candidate-backed row is `sawmvei`. That matters because it keeps a compact occurrence-counting expression in view without forcing the dossier to build a full classifier system.

Methodologically, the export-backed fused form controls this pass. The generated report wording `vei sawm` should not be substituted silently for the analyzer-backed row.

## Distributive material

The generated report mentions distributive `sagih sagih`, and the current candidate layer keeps that temptation visible through the deferred row `num_dist_gen7_2_sagih_sagih`.

That row is intentionally **not** accepted. In the current export window, Genesis 7:2 preserves only a single `sagih` token, so the expected reduplicated distributive span is not currently analyzer-backed. Distributive reduplication therefore remains deferred and not print-ready in this first dossier.

## Blocked, deferred, and not-yet-covered material

The following limits remain important:

- blocked interrogative `kua` stays outside the numerals packet;
- caveated `mi khat` remains boundary evidence rather than a plain `one` example;
- deferred distributive `sagih sagih` remains visible but not promoted;
- `masa` remains deferred rather than being promoted as the first ordinal anchor;
- classifiers beyond the compact `sawmvei` row remain deferred;
- broad quantifier work remains deferred;
- raw frequency counts remain excluded from the candidate-controlled evidence layer.

## Print implications

### Safe for a future grammar slice

The following material is candidate-backed and safe to carry forward into a later grammar slice:

- basic cardinal phrases such as `kum nih` and `ni sagih`;
- compound-ten evidence with `kum sawmkua`;
- ordinal `nihna`;
- occurrence-counting `sawmvei`, with its fused-export caveat;
- large-number phrase evidence from Genesis 5:27, with explicit analyzer caveats;
- `kua` as numeral only in constructionally numeral contexts.

### Not yet print-safe

The following material should stay out of the first print-facing slice:

- raw frequency counts or count tables from the generated report;
- any treatment of every raw `kua` hit as numeral `nine`;
- `mi khat` as an uncomplicated bare `one` example;
- `sagih sagih` as though the current export already confirmed reduplicated distributive material;
- a full classifier system built from one compact `sawmvei` row;
- quantifier prose imported into the numerals packet.

## Next steps

The next numerals step after this dossier should be:

1. draft `output/publication_review/grammar_numerals_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_numerals_print_slice.md`;
3. then add `output/publication_review/review_notes_numerals.md`.

The dossier is now the interpretive control for that later slice work, but the numerals packet is not yet complete.
