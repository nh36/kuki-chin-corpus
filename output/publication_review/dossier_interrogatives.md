---
title: "Tedim Interrogatives Evidence Dossier"
---

# Interrogatives dossier

## Scope and status

This is the first dossier for the interrogatives retrofit. The controlling candidate layer now exists at `output/publication_review/candidates_interrogatives.tsv`, and `interrogatives` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. Grammar and dictionary print slices for interrogatives have **not** started yet.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, record analyzer/export caveats explicitly, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

Candidate rows, not raw string hits, control the present analysis. The dossier should be read in the order `candidates_interrogatives.tsv` -> `dossier_interrogatives.md` -> future `grammar_interrogatives_print_slice.md` / `dictionary_interrogatives_print_slice.md` / `review_notes_interrogatives.md`.

The current extractor route is curated. It does **not** search every surface occurrence of `hiam`, `bang`, or `kua`, and it does **not** treat every report example as automatically print-safe. The hardening pass for this dossier rechecked every accepted or accepted-with-caveat row against the analyzer export and confirmed that `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` all match the current `data/ctd_analysis/tokens.tsv` windows.

## Core findings

The current candidate layer supports four narrow conclusions:

1. clause-final `hiam` is the main yes/no question particle in the current packet;
2. WH + `hiam` is the core content-question pattern represented so far;
3. the present candidate-backed WH inventory is `bang`, `kua`, `bangci`, and `banghangin`;
4. embedded `bang hiam cih ...` material is visible, but still under review and not print-ready.

The dossier therefore keeps interrogatives narrow. It does not broaden the packet into a general search over all `hiam`, all `bang` forms, or all other sentence-final particles.

## Accepted / usable evidence

### Genesis 24:23: clause-final yes/no `hiam`

`int_hiam_gen24_23_awng_ding_hiam` is the accepted-with-caveat yes/no anchor for clause-final `hiam`. The attested analyzer-backed clause is:

> `Na pa inn-ah kote giah nading a awng ding hiam`

The hardening pass confirms that this is the actual exported window. The older report paraphrase `Inn-ah hong tum theih na hiam` must **not** be silently projected back onto the candidate layer.

This row also records an export-boundary caveat: the surface span keeps the final quotation mark on `hiam?”` because the analyzer export attaches punctuation to the last token in that window. That is an export artifact, not a reason to reject the clause as interrogative evidence.

### Genesis 48:8 and 2 Samuel 22:32: `kua ... hiam`

`int_kua_gen48_8_hihte_kua_ahi_hiam` and `int_kua_2sam22_32_topa_longal_pasian_kua_hiam` are accepted-with-caveat `kua ... hiam` rows. They support the content-question pattern WH + `hiam`, and they keep `kua` visible as the current candidate-backed who-question item.

Both rows carry the same analyzer export caveat: `kua` is tagged as `NUM` in the export. That should be treated as an analyzer labeling limitation, not as evidence against the interrogative reading. Genesis 48:8 also preserves an opening quotation mark in the exported `surface_span` / `lemma_span` (`“Hihte`), so that punctuation attachment should be recorded as an export artifact rather than normalized away silently.

### Exodus 16:15: `Bang ahi hiam?`

`int_bang_exod16_15_bang_ahi_hiam` is the compact accepted-with-caveat what-question anchor:

> `Bang ahi hiam?`

The clause is analyzer-backed and should remain in the dossier as core `bang` evidence. The main caveat is lexical/exportal: the analyzer glosses `bang` here as `like`. That gloss is not enough to overturn the larger clause-level interrogative reading, so the row remains usable with caveat rather than rejected.

### Genesis 3:13: `Bangci ... hiam`

`int_bangci_gen3_13_bangci_hici_gamtat_na_hi_hiam` is the cleanest accepted row in the current packet. It supports `bangci` as current candidate-backed how-question evidence and is the strongest present WH + `hiam` row for later print use.

This row matters methodologically because it should stay visible as `bangci`, not be flattened into a generic `bang` bucket.

### Genesis 4:6: `banghangin ... hiam`

`int_banghangin_gen4_6_mai_sia_ahi_hiam` is the accepted-with-caveat reason-question row. The analyzer exports the relevant sequence as:

> `bang | hang-in | na | mai | sia | ahi | hiam`

The dossier still treats this as `banghangin` / reason-question evidence. The split `bang` + `hang-in` is an export/segmentation fact that needs to be recorded, but it is not a reason to collapse the row into raw `bang` evidence or to reject the reason-question reading.

## Embedded-question material

`int_embedded_exod16_15_bang_hiam_cih_thei_lo_uh_hi` keeps:

> `bang hiam cih thei lo uh hi`

visible in the packet. This is useful evidence for later treatment of interrogative complements or nominalized question clauses, but it should **not** yet be promoted as an ordinary independent clause-final `hiam` example.

The row therefore remains under review and not print-ready. It belongs in the dossier because it shows that the interrogatives packet needs a separate embedded-question subsection later, not because it is already safe for the first print slice.

## Blocked false friends and controls

The blocked rows are analytically important because they prevent raw-search leakage into future print work.

### Formulaic reason frame

`int_formulaic_gen3_20_bang_hang_hiam_cih_leh` records:

> `Bang hang hiam cih leh`

This is blocked because it is a formulaic explanatory frame, not an ordinary clause-final `hiam` question. It remains useful as a control row precisely so that formulaic reason expressions do not get recycled as basic interrogative examples.

### Lexical or non-interrogative `a hiam ...`

`int_falsefriend_2kings11_11_a_hiam_ciat_uh` keeps `a hiam ciat uh` blocked. The point is not that `hiam` disappears from the surface string, but that this sequence is not functioning as core interrogative-particle evidence.

`int_falsefriend_rev1_16_langnih_a_hiam_namsau` does the same for Revelation 1:16:

> `langnih a hiam namsau`

This sharp-two-edged-sword material is a lexical false friend already guarded by `tests/test_grammar_integration.py`, and it must stay blocked in the dossier as well.

### Bang-family false friends

`int_falsefriend_gen9_21_bangmah` and `int_falsefriend_gen1_7_bangin` keep two crucial bang-family blockers visible:

- `bangmah` is lexical/negative-polarity material, not ordinary interrogative `bang`;
- `bangin` is comparison-like or non-core material, not a what-question.

These controls matter because they show why the dossier must stay candidate-driven rather than broadening into a raw search over all `bang` forms.

## Deferred comparison particles

Existing reports mention `maw`, `ham`, and `em`, but they remain deferred in this first dossier pass. They are not part of the current core `hiam` evidence, and this dossier does not build a comparison-particle section yet.

That deferral is intentional. The present packet first stabilizes clause-final `hiam`, WH + `hiam`, blocked formulaic frames, and blocked lexical false friends before it expands into a broader sentence-final particle comparison.

## Print implications

### Safe for a future grammar slice

The following claims are now candidate-backed and safe to carry forward into a later grammar slice:

- clause-final `hiam` as a question marker, with the explicit caveat that not every surface `hiam` row is print-safe;
- WH + `hiam` as a content-question pattern;
- `bang`, `kua`, `bangci`, and `banghangin` as the current candidate-backed WH evidence.

### Not yet print-safe

The following material should remain out of the first print-facing slice:

- embedded `bang hiam cih ...` material;
- formulaic `Bang hang hiam cih leh` reason frames;
- lexical or non-interrogative `a hiam ...` sequences;
- bang-family compounds or comparative/non-core material such as `bangmah` and `bangin`;
- deferred comparison particles `maw`, `ham`, and `em`.

## Next steps

The next interrogatives step after this dossier should be:

1. draft `output/publication_review/grammar_interrogatives_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_interrogatives_print_slice.md`;
3. then add `output/publication_review/review_notes_interrogatives.md`.

The dossier is now the interpretive control for that later slice work, but the interrogatives packet is not yet complete.
