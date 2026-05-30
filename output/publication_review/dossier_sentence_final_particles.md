---
title: "Tedim Sentence-Final Particles Evidence Dossier"
---

# Sentence-final particles dossier

## Scope and status

This is the first dossier for the sentence-final particles retrofit. The controlling candidate layer now exists at `output/publication_review/candidates_sentence_final_particles.tsv`, and `sentence_final_particles` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. grammar, dictionary, and review-note print slices for sentence-final particles have **not** yet begun.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, keep analyzer/export caveats explicit, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

`candidates_sentence_final_particles.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not raw string hits and not generated-report counts, control the dossier. The intended reading order is `candidates_sentence_final_particles.tsv` -> `dossier_sentence_final_particles.md` -> future `grammar_sentence_final_particles_print_slice.md` / `dictionary_sentence_final_particles_print_slice.md` / `review_notes_sentence_final_particles.md`.

The current extractor route is curated. It does **not** search every `hi`, `hiam`, `in`, `un`, `tahen`, `hen`, `aw`, `ta`, `zo`, or other particle-looking token in the corpus. Before writing this dossier, each accepted or accepted-with-caveat row was rechecked against `data/ctd_analysis/tokens.tsv`, and the current `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` values were confirmed against the analyzer export. Generated-report raw count tables remain consultable only as discovery aids and do not control the present analysis.

## Core findings

The current candidate layer supports seven narrow conclusions:

1. declarative `hi` is visible only through caveated `ahi hi` and `lo hi` rows, not through a bare unrestricted `hi` anchor;
2. `hiam` is overlap-control material only because the interrogatives packet is already stabilized;
3. `hen` has one usable optative row in `Khuavak om hen`;
4. `in` and `un` both represent imperative material, but `in` has case-marker overlap while `un` is currently the cleaner anchor;
5. `aw` is visible as vocative or exclamative boundary material, but it is not print-ready as a settled sentence-final mood particle;
6. `tahen`, `ta`, and `zo` remain deferred or needs-review because the current export is too noisy for clean particle claims;
7. broad TAM remains outside this packet.

The dossier therefore keeps sentence-final particles narrow. It does not broaden the packet into a raw search over particle-looking tokens, and it does not import generated-report raw count claims into the evidence layer.

## Accepted / usable evidence

### Genesis 1:13: `ahi hi`

`sfp_hi_gen1_13_ahi_hi` is accepted with caveat:

> `ahi hi`

The hardening pass confirms that the selected window is analyzer-backed as `ahi | hi`, glossed `be.3SG | DECL`, with lemma/POS `ahi | hi` and `V | FUNC`. This is the packet's clearest current declarative row, but it is not a bare declarative `hi` example. The row bundles copular `ahi` with final `hi`, so it cannot license raw `hi` harvesting or a claim that every clause-final `hi` token is sentence-final declarative.

### Genesis 4:5: `thusim lo hi`

`sfp_hi_gen4_5_lo_hi` is also accepted with caveat:

> `thusim lo hi`

The current analyzer-backed span is `thusim | lo | hi`, with gloss `parable | NEG | DECL`. The row is useful because it keeps a negative-plus-declarative environment visible inside the packet, but it overlaps the stabilized negation packet and must not reopen `lo`. Future sentence-final prose can cite this row only as negation-overlap evidence with explicit caveat.

### Genesis 1:3: `Khuavak om hen`

`sfp_hen_gen1_3_khuavak_om_hen` is accepted with caveat:

> `Khuavak om hen`

The checked analyzer window is `Khuavak | om | hen`, glossed `light | exist | JUSS`. This is the current usable optative row. The dossier therefore treats `hen` as narrow optative evidence, but it keeps the report-versus-export caveat explicit: the candidate is the analyzer-backed `om hen` row, not report-style `ta hen` wording.

### Genesis 6:14: `teembaw khat bawl in`

`sfp_in_gen6_14_teembaw_khat_bawl_in` is accepted with caveat:

> `teembaw khat bawl in`

The hardening pass confirms the selected span exactly as `teembaw | khat | bawl | in`, with `in` exported as `ERG` / `FUNC`. This keeps singular imperative `in` visible, but only with a case-marker-overlap warning. The dossier also keeps the lexical-form caveat explicit: the analyzer-backed candidate has `teembaw`, not report-style `lawng`.

### Psalms 100:1: `gingsak un`

`sfp_un_ps100_1_gingsak_un` is accepted and currently print-ready:

> `gingsak un`

The selected analyzer window is tight and clean: `ging-sak | un`, glossed `sound-CAUS | IMP.PL`. This is the strongest current imperative anchor in the packet. The dossier keeps the span narrow so nearby `aw` material in the same verse does not get absorbed into the `un` row.

### Psalms 100:1: `Gam khempeuh aw`

`sfp_aw_ps100_1_gam_khempeuh_aw` is accepted with caveat but not print-ready:

> `Gam khempeuh aw`

The checked span is `Gam | khempeuh | aw`, with the export glossing `aw` as lexical `voice` and giving `N` in `pos_span`. This keeps `aw` visible in the packet as vocative or exclamative boundary material, but not as a settled sentence-final mood particle. The same verse also contains another `aw` inside `lungdamna aw`, so the dossier keeps the constructional ambiguity explicit.

## Deferred / needs-review evidence

### Genesis 48:8: `Hihte kua ahi hiam?`

`sfp_hiam_gen48_8_overlap_control` remains deferred and not print-ready:

> `Hihte kua ahi hiam?`

This row exists only as interrogatives-overlap control. The checked analyzer window is `Hihte | kua | ahi | hiam`, but the export keeps the quotation/punctuation artifact in the first lemma field and gives `kua` the export profile `who` with `NUM`. Those quirks are useful reminders that the sentence-final packet should not reopen `hiam` analysis here. `Hiam` belongs to the stabilized interrogatives packet, and this dossier treats Genesis 48:8 only as cross-reference material.

### Genesis 9:25: `hi tahen`

`sfp_tahen_gen9_25_hi_tahen` remains deferred:

> `hi tahen`

The current export gives `hi | tahen` with gloss `DECL | army` and `FUNC | N`, so `tahen` is not currently a clean jussive particle row. The verse may also contain split `ta hen` material elsewhere, but that is exactly why the dossier must stay conservative: it should not silently normalize fused `tahen` and split `ta hen` into a clean jussive example before a better analyzer-backed row exists.

### Genesis 40:23: `mangngilh ta hi`

`sfp_ta_gen40_23_mangngilh_ta_hi` remains needs-review and not print-ready:

> `mangngilh ta hi`

The checked analyzer window is `mangngilh | ta | hi`, but the export glosses `ta` as `child` and keeps it in `FUNC` rather than as a clean perfective particle. This is therefore TAM-overlap boundary material only, not settled aspectual evidence.

### Genesis 1:28: `zo`

`sfp_zo_gen1_28_zo_boundary` remains deferred:

> `zo`

The current export still glosses this token as lexical `south` with `N` in `pos_span`. `Zo` therefore remains deferred in the sentence-final packet and cannot yet support a clean completive analysis.

## Declarative hi and copula overlap

`Ahi hi` is useful because it keeps declarative `hi` visible in a compact clause-final window, but it is not a bare `hi` anchor. The sentence-final packet must therefore distinguish sentence-final `hi` from copular `ahi`.

`Thusim lo hi` is also useful, but it overlaps negation and must not reopen the stabilized negation packet. Future prose should distinguish bare sentence-final `hi`, copula-plus-declarative `ahi hi`, and negative `lo hi` environments rather than collapsing them into one undifferentiated declarative category.

The resulting caution is simple: do **not** claim that every `hi` token is sentence-final declarative, and do **not** treat the current dossier as permission for raw `hi` harvesting.

## Hiam overlap with interrogatives

`Hiam` is already treated in the interrogatives packet. The sentence-final particle dossier may cross-reference it because clause-final question particles do border the same domain, but this packet should not reopen or duplicate interrogatives prose.

That is why Genesis 48:8 is deferred and not print-ready here. The row keeps `Hihte kua ahi hiam?` visible only as overlap-control material, with quotation/punctuation noise and the `kua = NUM` export caveat left explicit rather than normalized away.

## Jussive and optative material

The current usable optative row is:

> `Khuavak om hen`

That row is analyzer-backed and sufficient to keep `hen` visible in the dossier as narrow optative evidence.

`Hi tahen`, by contrast, remains deferred because the current export treats `tahen` as lexical `army` / `N` rather than as a clean jussive particle. The dossier therefore does **not** silently normalize `hi tahen` or possible split `ta hen` material into a clean jussive example. It also does not turn the present packet into a broad mood chapter.

## Imperative in and un

The packet currently has two imperative rows:

- `teembaw khat bawl in`
- `gingsak un`

`In` is useful only with caveat. Its selected span is analyzer-backed, but the export still glosses `in` as `ERG` / `FUNC`, and there is obvious case-marker overlap. The dossier therefore keeps `in` as singular-imperative evidence only with an explicit overlap warning and without reopening case marking.

`Un` is currently cleaner. `Gingsak un` gives a compact imperative-plural anchor and is the stronger imperative row for later print-facing slice work. Even so, the dossier does **not** license raw `in` or `un` harvesting across the corpus.

## Aw as vocative/exclamative boundary material

`Gam khempeuh aw` keeps `aw` visible in the packet, but only as vocative or exclamative boundary material. The analyzer currently glosses `aw` as `voice` and gives `N` in the checked `pos_span`, which is not strong evidence for a settled sentence-final mood particle.

The same Psalm verse also contains another `aw` in `lungdamna aw`. That duplication matters because it shows how quickly raw `aw` harvesting would mix vocative, lexical, and possible exclamative material. The dossier therefore keeps `aw` out of print-ready status and treats it only as boundary material.

## Ta and zo as TAM-overlap boundary material

`Mangngilh ta hi` keeps `ta hi` visible in the packet, but the row remains needs-review because `ta` is exported as `child` / `FUNC` rather than as a clean perfective marker.

`Zo` remains deferred because the checked export still glosses it as lexical `south` / `N` rather than as a clean completive particle.

Both rows therefore remain TAM-overlap boundary material only. They keep potentially relevant forms visible without letting the sentence-final dossier broaden into a full aspect or mood chapter. Broad TAM remains deferred.

## Print implications

### Safe for a future grammar slice

The following material is candidate-backed and safe to carry forward into a later grammar slice:

- `ahi hi` as copula-plus-declarative evidence with caveat;
- `thusim lo hi` as negation-plus-declarative evidence with caveat;
- `Khuavak om hen` as optative evidence with caveat;
- `gingsak un` as the comparatively clean plural-imperative anchor;
- `teembaw khat bawl in` as singular-imperative evidence only with case-overlap caveat.

### Not yet print-safe

The following material should stay out of the first print-facing slice:

- raw count tables or generated-report count claims;
- bare `hi` as a general declarative particle without constructional caveat;
- `hiam` as new sentence-final evidence rather than as interrogatives cross-reference;
- `tahen` as settled jussive evidence based on the current `hi tahen` export;
- `aw` as a settled sentence-final mood particle;
- `ta` or `zo` as settled aspectual particles;
- broad TAM or full mood/aspect chapters.

## Next steps

The next sentence-final particles step after this dossier should be:

1. draft `output/publication_review/grammar_sentence_final_particles_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_sentence_final_particles_print_slice.md`;
3. then add `output/publication_review/review_notes_sentence_final_particles.md`.

The dossier is now the interpretive control for that later slice work, and grammar, dictionary, and review-note print slices for sentence-final particles have **not** yet begun. Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
