---
title: "Tedim Chin Dictionary Review Slice: Numerals"
---

# Editorial scope

These are short print-facing dictionary drafts for the numerals slice. They are aligned to `candidates_numerals.tsv`, interpreted through `dossier_numerals.md`, and cross-referenced to `grammar_numerals_print_slice.md`. They preserve candidate-backed numeral constructions, analyzer/export caveats, and blocked false friends rather than turning the packet into a raw search over every `khat`, `nih`, `kua`, `sawm`, or other numeral-looking form.

These entries are editorial review material only. They do not imply changes to analyzer dictionaries, machine dictionary files, or lexical source tables. Review-note work for numerals has not yet begun.

## nih

Category: numeral

Gloss: `NUM`; 'two'

Cross-reference: *Grammar review slice, "Basic cardinal counting phrases"*

Status: draft-ready

`Nih` is currently represented by the accepted counting phrase `kum nih`. This is enough to support a conservative numeral entry for `two` without turning the packet into a full paradigm or a broad search across every numeral environment.

(@dict:nih-1)
a. Tedim: kum nih
b. Segmentation: kum | nih
c. Gloss: year | two
d. Translation: 'two years'

## sagih

Category: numeral

Gloss: `NUM`; 'seven'

Cross-reference: *Grammar review slice, "Basic cardinal counting phrases"*

Status: draft-ready with deferred distributive control

`Sagih` is currently represented by the accepted phrase `ni sagih`. The generated numerals report also mentions distributive `sagih sagih`, but the candidate layer keeps that material deferred because the current analyzer export preserves only a single `sagih` token in Genesis 7:2. The dictionary entry should therefore keep plain `seven` visible without printing distributive reduplication as though it were already analyzer-backed.

(@dict:sagih-1)
a. Tedim: ni sagih
b. Segmentation: ni | sagih
c. Gloss: day | seven
d. Translation: 'seven days'

## sawmkua

Category: compound numeral

Gloss: 'ninety'

Cross-reference: *Grammar review slice, "Compound tens"*

Status: draft-ready with export caveat

`Sawmkua` is the clearest current compound numeral entry. It shows a compound-ten structure and is also the strongest numeral-side control for `kua = nine`. The segmentation and gloss are clear (`sawm-kua`, `ten-nine`), but the current lemma/POS export is flattened (`kum | sawm`, `N | N`), so that caveat should stay visible in the prose rather than being normalized away.

(@dict:sawmkua-1)
a. Tedim: kum sawmkua
b. Segmentation: kum | sawm-kua
c. Gloss: year | ten-nine
d. Translation: 'ninety years'

## nihna

Category: ordinal numeral

Gloss: 'second'

Cross-reference: *Grammar review slice, "Ordinals"*

Status: draft-ready with analyzer label caveat

`Nihna` is the current candidate-backed ordinal anchor. The analyzer confirms `nih-na` and `two-NMLZ`, while the export labels the form with `pos_span = N`. That label should be treated as an analyzer caveat, not as a reason to reject the ordinal reading. The generated report's `masa` 'first' remains deferred and should not be promoted through this entry.

(@dict:nihna-1)
a. Tedim: nihna
b. Segmentation: nih-na
c. Gloss: two-NMLZ
d. Translation: 'second'

## sawmvei

Category: multiplicative / occurrence-counting numeral expression

Gloss: 'ten times'

Cross-reference: *Grammar review slice, "Occurrence counting / multiplicative form"*

Status: draft-ready with export caveat

`Sawmvei` keeps occurrence-counting visible in the packet, but it does so under an explicit export control. The generated report paraphrases the form as `vei sawm`, while the candidate layer keeps the export-backed fused form `sawmvei`. The dictionary slice should therefore not silently replace `sawmvei` with `vei sawm`, and it should not use one compact row to build a full classifier system.

(@dict:sawmvei-1)
a. Tedim: sawmvei
b. Segmentation: sawm-vei
c. Gloss: ten-times
d. Translation: 'ten times'

## kua (numeral-side use)

Category: numeral with interrogative overlap

Gloss: 'nine' in numeral constructions; `who` in interrogative clauses

Cross-reference: *Grammar review slice, "`Kua` ambiguity"*

Status: usable only with constructional control

The numerals packet does not support a raw, context-free dictionary entry for every surface `kua` hit. Instead, it supports numeral-side `kua` only in constructionally numeral contexts such as `sawmkua` and the Genesis 5:27 large-number phrase. The same surface form is interrogative `who` in Genesis 48:8 `Hihte kua ahi hiam?`, so that row remains blocked as numeral evidence and belongs to the interrogatives packet.

(@dict:kua-1)
a. Tedim: kum zakua le kum sawmguk le kua
b. Segmentation: kum | za-kua | le | kum | sawm-guk | le | kua
c. Gloss: year | hundred-nine | and | year | ten-six | and | nine [export: who]
d. Translation: 'nine hundred sixty and nine years'

Editorial note: this large-number phrase is usable only with explicit caveats. The analyzer compresses `za-kua`, and the candidate TSV glosses the final `kua` as `who`; the reader-facing `nine` gloss is therefore an editorial correction justified by the numeral construction, not a hidden normalization.

## khat

Category: numeral / indefinite overlap

Gloss: 'one; a, an'

Cross-reference: *Grammar review slice, "`Khat` and the numeral/indefinite boundary"*

Status: usable with boundary caution

`Khat` is currently represented by analyzer-backed `mi khat`, but that row remains boundary evidence rather than an uncomplicated bare numeral `one` entry. Its English context "a man" shows why the dictionary slice has to keep numeral and indefinite reference visibly linked here. This entry therefore supports `one person` / `a man` as a controlled boundary note and does not start the later quantifiers retrofit.

(@dict:khat-1)
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: 'a man' / 'one person'

## Deferred and blocked material

The current dictionary slice stays narrow. `Sagih sagih` remains deferred and not print-ready because the analyzer export does not currently confirm the repeated numeral span. `Masa` remains deferred rather than being promoted as the first ordinal entry. Raw generated-report frequency tables are excluded. The packet also does not yet build a full classifier system, and future numerals prose must not treat raw `kua` matching as numeral evidence.

The next step after this dictionary slice is `review_notes_numerals.md`.
