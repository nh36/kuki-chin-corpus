---
title: "Tedim Coordinators Evidence Dossier"
---

# Coordinators dossier

## Scope and status

This is the first dossier for the coordinators retrofit. The controlling candidate layer now exists at `output/publication_review/candidates_coordinators.tsv`, and `coordinators` is now a supported curated topic in `scripts/publication_review/extract_candidates.py`. Grammar, dictionary, and review-note print slices for coordinators have **not** yet begun.

This dossier is therefore not a print grammar section. Its job is to interpret the current candidate layer conservatively, record analyzer/export caveats explicitly, and define what is and is not ready for later print-facing slice work.

## Evidence protocol

`candidates_coordinators.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not raw string hits and not generated-report counts, control the dossier. The intended reading order is `candidates_coordinators.tsv` -> `dossier_coordinators.md` -> future `grammar_coordinators_print_slice.md` / `dictionary_coordinators_print_slice.md` / `review_notes_coordinators.md`.

The current extractor route is curated. It does **not** search every `le`, `leh`, `a`, `mawh`, `ahih hangin`, `ahih kei leh`, `ciangin`, `hangin`, or other coordinator-looking token in the corpus. Before writing this dossier, every accepted or accepted-with-caveat row was rechecked against the analyzer export, and the current `token_indices`, `segmentation_span`, `gloss_span`, `lemma_span`, and `pos_span` values were confirmed against `data/ctd_analysis/tokens.tsv`. The generated coordinator report remains consultable as a discovery aid, but its raw count tables do not control the present analysis.

## Core findings

The current candidate layer supports seven narrow conclusions:

1. NP coordination is securely represented by `le` in Genesis 1:1 `vantung le leitung`;
2. `leh` is visible only as conditional or boundary material in the current layer, not as a clean print-ready clause conjunction;
3. sequential `a` is visible only as caveated boundary material and is paired with a blocked agreement-`a` false friend;
4. `mawh` remains deferred because the current export still gives lexical `sin` / `V` material rather than a clean disjunction or alternative-question candidate;
5. `Ahih hangin` is usable only as a caveated adversative connector;
6. `ahih kei leh` is useful only as conditional-adversative boundary material, not as a simple coordinator;
7. broader `ciangin` and `hangin` temporal/causal/subordinator material remains outside the first coordinator packet.

The dossier therefore keeps coordinators narrow. It does not broaden the packet into a raw search over coordinator-looking tokens, and it does not import generated-report raw count tables into the evidence layer.

## Accepted / usable evidence

### Genesis 1:1: `vantung le leitung`

`coord_le_gen1_1_vantung_le_leitung` is the clean accepted NP-coordination anchor:

> `vantung le leitung`

This row is print-ready and analyzer-backed without special export noise in the selected window. It is the safe NP-conjunction anchor for a later narrow grammar claim that `le` joins noun phrases.

That conclusion must stay narrow. The row supports future coordinator prose anchored in `vantung le leitung`, but it does **not** license broad raw `le` harvesting. A separate blocked `le` row was not created in the first pass; overgeneration is controlled here by curated selection rather than by a large raw-hit control list.

### Genesis 2:10: `luang a tua mun panin gun hong kikhenin`

`coord_a_gen2_10_sequential_linker` remains accepted with caveat:

> `luang a tua mun panin gun hong kikhenin`

The hardening pass confirms that the current candidate window is exactly the analyzer-backed export span. It is **not** print-ready, however. The analyzer still exports the relevant `a` as `3SG` / `FUNC`, so the row can only function as caveated boundary evidence for possible sequential linkage, not as an uncomplicated coordinator anchor.

### Genesis 3:4: `Ahih hangin`

`coord_ahih_hangin_gen3_4_adversative` remains accepted with caveat:

> `Ahih hangin`

This row is usable with caveat and currently `print_usable_with_caveat`. It is the packet's best adversative connector evidence, but the dossier keeps the internal analysis visible: the export still supports reading the form as `ahih` plus `hang-in`, so this should not open a full causal or subordinator treatment.

### Exodus 12:3: `ahih kei leh`

`coord_ahih_kei_leh_exod12_3_boundary` remains accepted with caveat:

> `ahih kei leh`

This row is analyzer-backed and useful, but it is **not** print-ready. The construction is conditional-adversative boundary material rather than a simple coordinator, and it overlaps with both negation and conditional `leh`. The dossier keeps that overlap visible without reopening the stabilized negation packet.

## Needs-review / deferred / blocked evidence

### Genesis 13:9: `veilam na lak leh kei taklamah ka pai ding hi`

`coord_leh_gen13_9_conditional_boundary` remains `needs_review` and `not_print_ready`:

> `veilam na lak leh kei taklamah ka pai ding hi`

This row keeps `leh` visible in the packet, but only as conditional or boundary material. It is not a clean print-ready clause-conjunction row. The analyzer/export caveat also needs to stay explicit: within this selected window, `kei` is glossed as `NEG` even though the wider English context is "I will go." That caveat should be recorded as an export issue inside the row, not used to reopen the pronouns or negation packets.

### Genesis 1:1: `a piangsak`

`coord_a_gen1_1_agreement_false_friend` remains excluded and blocked:

> `a piangsak`

This is the main false-friend control for the coordinator packet. The export gives `a` here as ordinary `3SG` / `FUNC` material before `piangsak`, not as a coordinator or even as usable sequential-linkage evidence.

### Genesis 6:3: `mawh`

`coord_mawh_gen6_3_lexical_control` remains deferred:

> `mawh`

The current analyzer export still gives lexical `sin` / `V` material rather than a clean disjunction or alternative-question row. `Mawh` therefore remains visible only as deferred analyzer-noise or lexical-control material and is not print-ready.

## NP coordination with `le`

`Vantung le leitung` is the current safe anchor for NP coordination with `le`. It supports a future narrow grammar claim that `le` joins noun phrases in the current packet.

That claim must remain tightly controlled. The dossier does **not** license broad raw `le` harvesting, and it does **not** treat every `le` token as coordinator evidence. A separate blocked `le` row was not needed in the first pass because overgeneration is being controlled by curated selection rather than by a broad token sweep.

## Leh boundary material

The current candidate layer does **not** yet contain a clean accepted simple clause-conjunction `leh` row. Genesis 13:9 keeps `leh` visible only as conditional or boundary material:

> `veilam na lak leh kei taklamah ka pai ding hi`

Future coordinator prose must therefore not flatten conditional `leh` into a simple printed "`and`" analysis. The row also carries an analyzer/export caveat: `kei` is glossed as `NEG` in the selected window even though the wider English context is "I will go." That caveat belongs in the dossier precisely so it can stay visible without reopening the negation or pronouns packets.

## Sequential `a` and agreement-`a` false friends

`A` is high-risk material in this packet because it is extremely frequent and often exported as `3SG` / `FUNC` rather than as a coordinator. The candidate-controlled dossier therefore keeps only one caveated sequential-linkage row:

> `luang a tua mun panin gun hong kikhenin`

and pairs it with one blocked false friend:

> `a piangsak`

This pairing matters methodologically. The Genesis 2:10 row keeps possible sequential linkage visible, but it remains accepted-with-caveat and not print-ready. The Genesis 1:1 row prevents raw `a` harvesting from flooding the packet with agreement or other functional material. No print claim about `a` should be built until better candidate evidence exists.

## Disjunction and alternative questions with `mawh`

The generated report mentions `mawh` as disjunction and as possible alternative-question material. The current candidate layer does not yet support that as print evidence.

The only current row is the deferred Genesis 6:3 control:

> `mawh`

in which the export gives lexical `sin` / `V` material rather than disjunction. `Mawh` therefore remains deferred and not print-ready in this first dossier. Report-only schematic examples such as `mi mawh ganhing mawh` or `pai ding mawh om ding mawh` must not be used as evidence unless a later analyzer-backed row is actually located.

## Adversative and conditional-adversative material

`Ahih hangin` is the current usable adversative connector, but only with caveat:

> `Ahih hangin`

This row can support later adversative prose, yet it remains internally analyzable and overlaps with broader `hangin` material. The dossier therefore treats it as a narrow adversative connector without starting a full causal or subordinator section.

`Ahih kei leh` is also useful, but only as conditional-adversative boundary evidence:

> `ahih kei leh`

It should not be flattened into a simple coordinator. Its overlap with negation and conditional `leh` stays visible in the dossier, but that overlap does not reopen the negation packet.

## Deferred and not-yet-covered material

The following limits remain important:

- clean simple clause-conjunction `leh` remains deferred;
- clean `mawh` disjunction or alternative-question evidence remains deferred;
- a full sequential-`a` analysis remains deferred;
- `ciangin` and broader `hangin` temporal/causal subordinator material remain deferred;
- full clause-chaining or converb coordination remains deferred;
- sentence-final particles remain deferred rather than being imported into the coordinator packet;
- raw frequency tables remain excluded from the candidate-controlled evidence layer;
- broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain outside the scope of this dossier.

## Print implications

### Safe for a future grammar slice

The following material is candidate-backed and safe to carry forward into a later grammar slice:

- `le` as the current NP-conjunction anchor, anchored by `vantung le leitung`;
- `Ahih hangin` as an adversative connector with explicit internal-analysis and `hangin` caveats;
- `ahih kei leh` as conditional-adversative boundary material with explicit caveats;
- sequential `a` only as warning or boundary evidence, not as a core print claim;
- `mawh` only as deferred material, not as current print evidence.

### Not yet print-safe

The following material should stay out of the first print-facing slice:

- raw count tables or generated-report count claims;
- treating every raw `le` or `leh` token as coordinator evidence;
- treating conditional `leh` as a simple printed "`and`";
- treating raw `a` as uncomplicated coordinator evidence;
- promoting `mawh` from report-only examples;
- a full temporal or causal subordinator section;
- sentence-final particles imported into coordinator prose.

## Next steps

The next coordinators step after this dossier should be:

1. draft `output/publication_review/grammar_coordinators_print_slice.md`;
2. only after that, if useful, draft `output/publication_review/dictionary_coordinators_print_slice.md`;
3. then add `output/publication_review/review_notes_coordinators.md`.

The dossier is now the interpretive control for that later slice work, but grammar, dictionary, and review-note slices for coordinators have **not** yet begun. Sentence-final particles, broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.
