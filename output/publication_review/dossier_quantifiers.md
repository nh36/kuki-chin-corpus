---
title: "Tedim Quantifiers Evidence Dossier"
---

# Quantifiers dossier

## Scope and status

This is the first dossier for the quantifiers retrofit. The controlling candidate layer now exists at `output/publication_review/candidates_quantifiers.tsv`, and `quantifiers` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. Grammar, dictionary, and review-note print slices for quantifiers have **not** yet begun.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, record analyzer/export caveats explicitly, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

`candidates_quantifiers.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not raw string hits and not generated-report counts, control the dossier. The intended reading order is `candidates_quantifiers.tsv` -> `dossier_quantifiers.md` -> future `grammar_quantifiers_print_slice.md` / `dictionary_quantifiers_print_slice.md` / `review_notes_quantifiers.md`.

The current extractor route is curated. It does **not** search every `khempeuh`, `peuhpeuh`, `khat`, `pawlkhat`, `kuamah`, `bangmah`, `tampi`, `tawm`, `zaw`, `mahmah`, or other quantifier-looking token in the corpus. Before writing this dossier, every accepted or accepted-with-caveat row was rechecked against the analyzer export, and the current `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` values were confirmed against `data/ctd_analysis/tokens.tsv`.

## Core findings

The current candidate layer supports eight narrow conclusions:

1. universal quantifier evidence is currently represented by `khempeuh`;
2. existential or partitive evidence is represented by `pawlkhat`, but only with a partitive-grouping caveat;
3. `mi khat` remains on the numeral/indefinite boundary rather than functioning as a simple quantifier anchor;
4. negative quantifier evidence is represented by `kuamah mu lo` and `bangmah om lo hi` only in clearly negative-licensed contexts;
5. degree or quantity evidence is currently represented by `tampi tak`;
6. `vanglian zaw` and `hau mahmah` are usable only as comparative or intensifier edge rows;
7. `mi peuhpeuh` and `tawm` remain deferred and not print-ready;
8. bang-family material outside clear negative licensing, especially `tua bangmah hi-in`, remains blocked.

The dossier therefore keeps quantifiers narrow. It does not broaden the packet into a raw search over all quantifier-looking tokens, and it does not import the generated report's raw count tables into the evidence layer.

## Accepted / usable evidence

### Genesis 2:1: `khempeuh`

`quant_univ_gen2_1_khempeuh` is the current accepted universal anchor:

> `vantung leitung le a sunga omte khempeuh`

The hardening pass confirms that this larger scoped noun phrase is exactly the analyzer-backed window in the current export. The row should stay narrow and constructional: it is the current universal anchor, not a warrant for broad count claims or raw `khempeuh` harvesting.

### Genesis 32:8: `pawlkhat`

`quant_exist_gen32_8_pawlkhat` is the accepted-with-caveat existential or partitive row:

> `pawlkhat`

This row is useful because the later `pawlkhat` token is cleanly analyzer-backed. The dossier keeps the caveat explicit, however: Genesis 32:8 supports a partitive or alternative-grouping reading ("one company ... the other company"), not an uncomplicated bare `some` entry. The opening `Pawlkhatah` token remains noisy in the export and must not be silently substituted for the clean later control token.

### Genesis 32:24: `mi khat`

`quant_boundary_gen32_24_mi_khat` remains accepted with caveat:

> `mi khat`

This row is useful because it keeps `khat` visible in the quantifiers dossier without pretending that the packet now has a plain article-like `one` entry. The English context still shows why it belongs on the numeral/indefinite boundary rather than inside a simple quantifier paradigm.

### Exodus 2:12: `kuamah mu lo`

`quant_neg_exod2_12_kuamah` is the accepted-with-caveat negative-quantifier row:

> `kuamah mu lo`

The analyzer-backed window is clean, but the row is usable only with a negation-overlap caveat. The present dossier keeps it as quantifier evidence in a licensed negative clause without reopening the already stabilized negation packet.

### Genesis 39:9: `bangmah om lo hi`

`quant_neg_gen39_9_bangmah` is the accepted-with-caveat `bangmah` row:

> `bangmah om lo hi`

This is usable because the negative licensing is explicit in the analyzer-backed clause. It still needs two caveats: it belongs only in a negative-licensed environment, and it must remain separated from broader bang-family or interrogative-overlap material elsewhere in the repository.

### Genesis 17:2: `tampi tak`

`quant_degree_gen17_2_tampi_tak` is the current degree or quantity anchor:

> `tampi tak`

The analyzer confirms the compact window, and the dossier keeps it as quantity or degree evidence. It should not be used to start a broad adjective or adverb chapter.

### Genesis 26:16 and Genesis 13:2: `vanglian zaw` and `hau mahmah`

`quant_comp_gen26_16_zaw` and `quant_int_gen13_2_hau_mahmah` remain accepted with caveat:

- `vanglian zaw`
- `hau mahmah`

These are useful edge rows because they keep comparative and intensifier material visible in the packet. They remain edge rows only, however: the dossier should not treat them as the start of a full comparison or intensifier chapter.

## Universal and distributive-universal material

`Khempeuh` is the current accepted universal anchor, and it is enough to keep a universal subsection visible in the first dossier. The packet does **not** yet build a full universal system from that single accepted row.

`Peuhpeuh` is represented only by the deferred row `quant_dist_gen31_32_mi_peuhpeuh`:

> `mi peuhpeuh`

The present example remains deferred because it behaves more like free-choice `whoever / any person` material than like a settled distributive-universal print anchor. The dossier therefore keeps `peuhpeuh` visible as deferred and not print-ready, rather than promoting it prematurely or collapsing it into the same function as `khempeuh`.

## Existential / partitive material

`Pawlkhat` is useful but caveated. Genesis 32:8 preserves a clean later `pawlkhat` token, but the construction points to partitive or alternative-grouping evidence rather than to a simple bare existential quantifier.

That distinction matters methodologically. The noisy opening `Pawlkhatah` form should not be silently substituted for the accepted control row, and the dossier should not flatten the verse into a generic `some` example without saying so explicitly.

## Khat boundary

`Mi khat` is reused from the numerals packet as boundary evidence. Its job in the quantifiers dossier is to prevent the packet from absorbing numeral `khat` as an uncomplicated article-like quantifier.

The row therefore remains accepted-with-caveat boundary material rather than a simple quantifier anchor. It points to a live boundary between numeral and indefinite readings, but it does **not** reopen a broader numerals discussion here.

## Negative quantifiers and negation overlap

`Kuamah mu lo` and `bangmah om lo hi` are both usable only in negative-licensed contexts in this first pass. Both rows are accepted with caveat rather than plain accepted rows because the quantifier reading depends on a clear negative clause.

This section should cross-reference, not reopen, the stabilized negation packet. The present dossier only records that the quantifier layer can safely reuse these clauses when the negative licensing is explicit.

## Bang-family false friends

`Bangmah` needs a second caution beyond simple negative licensing: it also sits inside the broader bang-family that has already produced false-friend problems elsewhere in the repository.

The blocked control row is Exodus 27:11:

> `tua bangmah hi-in`

That row remains excluded and blocked because it is not ordinary negative-quantifier evidence. The point is to prevent quantifiers from absorbing `bangmah` hits outside clear negative-quantifier environments and to respect the already-stabilized interrogatives packet, where bang-family false friends also had to be controlled.

## Degree, comparative, and intensifier edge rows

`Tampi tak` is the current degree or quantity anchor. It is compact, analyzer-backed, and safe to keep visible in the dossier.

`Vanglian zaw` and `hau mahmah` are also useful, but only as edge rows. They keep the packet aware of comparative and intensifier material without turning quantifiers into a general comparison or degree-modification chapter. The dossier should therefore treat them as caveated boundary evidence rather than as the basis for a full adjective/adverb analysis.

## Deferred and not-yet-covered material

The following limits remain important:

- deferred `peuhpeuh` remains visible but not print-ready;
- deferred `tawm` remains visible but not print-ready because the current export glosses it as `produce`;
- a full universal or distributive-universal system remains deferred;
- a full degree or intensifier system remains deferred;
- a full comparative system remains deferred;
- raw frequency tables remain excluded from the candidate-controlled evidence layer;
- coordinators and sentence-final particles remain deferred rather than being imported into the quantifiers packet.

## Print implications

### Safe for a future grammar slice

The following material is candidate-backed and safe to carry forward into a later grammar slice:

- `khempeuh` as the current universal anchor;
- `pawlkhat` as partitive or existential evidence with explicit caveat;
- `khat` only as numeral/indefinite boundary evidence;
- `kuamah mu lo` and `bangmah om lo hi` as negative-licensed quantifier evidence with caveats;
- `tampi tak` as degree or quantity evidence;
- `vanglian zaw` and `hau mahmah` only as edge rows if they are cited with explicit caveats.

### Not yet print-safe

The following material should stay out of the first print-facing slice:

- raw count tables or generated-report count claims;
- `peuhpeuh` as though it were already settled distributive-universal evidence;
- `tawm` as though the current export already confirmed a settled low-quantity row;
- `bangmah` outside clear negative licensing;
- `khat` as an uncomplicated article-like quantifier;
- a full degree, intensifier, or comparative chapter;
- coordinators or sentence-final particles imported into quantifier prose.

## Next steps

The next quantifiers step after this dossier should be:

1. draft `output/publication_review/grammar_quantifiers_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_quantifiers_print_slice.md`;
3. then add `output/publication_review/review_notes_quantifiers.md`.

The dossier is now the interpretive control for that later slice work, but the quantifiers packet is not yet complete.
