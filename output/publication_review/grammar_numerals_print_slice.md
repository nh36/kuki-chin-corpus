---
title: "Tedim Chin Grammar Review Slice: Numerals"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
suppress-bibliography: true
reference-section-title: "References"
---

# Scope

This is a short print-facing draft section on numerals in Tedim Chin, controlled by `candidates_numerals.tsv` and `dossier_numerals.md`. It covers only a small candidate-backed set: basic cardinal counting phrases, compound tens, one ordinal form, one occurrence-counting or multiplicative form, one large-number phrase with caveats, and explicit ambiguity controls for `kua` and `khat`.

It does not yet attempt a full numeral paradigm, a full classifier system, a full account of distributive reduplication, quantifiers, or generated-report frequency tables. Dictionary and review-note slices have not yet begun.

# Numerals in outline

The current candidate-backed packet supports a narrow generalization. Simple cardinals can follow a counted noun in examples such as `kum nih` and `ni sagih`. Compound tens are represented by `sawmkua`, ordinal formation is represented by `nihna`, occurrence-counting is represented by `sawmvei`, and large biblical number expressions are visible but need caveats. Across the packet, `kua` and `khat` require constructional controls rather than raw-string treatment.

# Basic cardinal counting phrases

The cleanest basic counting phrases in the current packet are Genesis 11:10 and Genesis 7:10.

(@ex:num-kum-nih)
a. Tedim: kum nih
b. Segmentation: kum | nih
c. Gloss: year | two
d. Translation: 'two years'

(@ex:num-ni-sagih)
a. Tedim: ni sagih
b. Segmentation: ni | sagih
c. Gloss: day | seven
d. Translation: 'seven days'

These are clean post-nominal counting phrases. The printed claim should stay modest: they show candidate-backed noun-plus-numeral counting, not a full word-order typology for every numeral construction in the language.

# Compound tens

Genesis 5:9 gives the clearest current compound-ten example:

(@ex:num-sawmkua)
a. Tedim: kum sawmkua
b. Segmentation: kum | sawm-kua
c. Gloss: year | ten-nine
d. Translation: 'ninety years'

`Sawmkua` matters for two reasons. First, it shows a compound-ten structure. Second, it is the strongest current numeral-side control for `kua = nine`. The dossier also keeps one analyzer/export caveat visible: the segmentation and gloss support the compound reading, but the lemma and POS layer is flattened (`kum | sawm`, `N | N`). That caveat should stay in the prose rather than being silently normalized away.

# Ordinals

Genesis 7:11 supplies the current ordinal anchor:

(@ex:num-nihna)
a. Tedim: nihna
b. Segmentation: nih-na
c. Gloss: two-NMLZ
d. Translation: 'second'

`Nihna` is the current candidate-backed ordinal example. The generated report mentions `masa` 'first', but `masa` is not promoted in this slice, and this section does not attempt a full ordinal paradigm. The dossier also records that `pos_span = N` in the export; that is a label caveat, not a reason to reject the ordinal analysis.

# Occurrence counting / multiplicative form

Genesis 31:7 keeps one compact occurrence-counting form in view:

(@ex:num-sawmvei)
a. Tedim: sawmvei
b. Segmentation: sawm-vei
c. Gloss: ten-times
d. Translation: 'ten times'

The generated report paraphrases this as `vei sawm`, but the candidate layer uses export-backed `sawmvei`, and that fused form should control the present slice. This row is enough to keep occurrence-counting visible, but it is not enough to build a full classifier system.

# Large-number phrase

Genesis 5:27 gives one usable large-number phrase, but only with explicit caveats:

(@ex:num-large)
a. Tedim: kum zakua le kum sawmguk le kua
b. Segmentation: kum | za-kua | le | kum | sawm-guk | le | kua
c. Gloss: year | hundred-nine | and | year | ten-six | and | nine [export: who]
d. Translation: 'nine hundred sixty and nine years'

This construction is numeral, not interrogative. The dossier is nevertheless explicit about the export caveats: the analyzer compresses `za-kua`, and the final `kua` is glossed as `who` in the candidate TSV even though the constructional context is numeral. The print gloss therefore keeps `nine` reader-facing while marking the export gloss in the example line. This makes the row usable with caveat, but not a fully polished anchor for a larger large-number section.

# `Kua` ambiguity

`Kua` needs an explicit control note in the printed grammar. In constructionally numeral contexts such as `sawmkua` and the Genesis 5:27 large-number phrase, `kua` is numeral `nine`. In interrogative clauses, however, `kua` is also `who`.

The blocked control in the numerals packet is Genesis 48:8:

> Hihte kua ahi hiam?

That row belongs to the interrogatives packet, not to numerals. Future numerals prose must therefore not use raw `kua` hits as numeral evidence.

# `Khat` and the numeral/indefinite boundary

Genesis 32:24 gives a useful but boundary-marked example:

(@ex:num-mi-khat)
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: 'a man' / 'one person'

`Mi khat` is analyzer-backed and worth keeping visible, but its English context "a man" shows why it should not be treated as an uncomplicated bare numeral `one` example. The packet therefore keeps it as numeral/indefinite boundary evidence and does not start a quantifiers retrofit here.

# Distributive reduplication deferred

The generated report claims distributive `sagih sagih` for 'by sevens', but the candidate layer keeps that material deferred. In the current analyzer export window, Genesis 7:2 preserves only a single `sagih` token. Distributive reduplication therefore remains not print-ready in this slice, and `sagih sagih` should not be printed as though it were already analyzer-backed.

# Editorial summary

This slice now safely supports six modest claims: noun-plus-numeral counting examples are printable; compound-ten `sawmkua` is candidate-backed; ordinal `nihna` is candidate-backed; occurrence-counting `sawmvei` remains visible with a fused-export caveat; one large-number phrase is usable with explicit analyzer caveats; and the packet has explicit controls for `kua` and `khat`.

What remains deferred is equally important: raw frequency counts, full numeral paradigms, `masa`, distributive reduplication, a full classifier system, quantifier overlap, and raw `kua` matching. The next step after this grammar slice is the dictionary print slice, while review-note work has not yet begun.
