---
title: "Tedim Chin Grammar Review Slice: Numerals"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
suppress-bibliography: true
reference-section-title: "References"
---

# Scope

This is now a normalized publication-facing numerals section, not just the first narrow slice. It is controlled by `candidates_numerals.tsv` and `dossier_numerals.md`, and it is additionally checked against `review_notes_numerals.md`, `coverage_normalization_audit.md`, and `examples_numerals_normalization.tsv`.

The section still keeps candidate discipline. Printed claims and formal examples come from candidate evidence in `candidates_numerals.tsv` or from newly checked normalization examples in `examples_numerals_normalization.tsv`, not from raw generated-report counts and not from broad string searches over every numeral-looking form. The separate dictionary print slice still exists, but this section now aims to read like a real grammar section rather than a packet-status note.

# Overview of the numeral system

The current evidence supports a cautious but fuller overview of the Tedim numeral system. Tedim is described in the literature as a decimal system, with `sawm` 'ten' as the decimal base and `za` 'hundred' as the next larger base above the first two-digit range [@zamngaihcing2017; @henderson1965]. The Bible-backed review packet confirms that basic cardinals, compound tens, larger-number expressions, `-na` ordinals such as `nihna` 'second', and at least one occurrence-counting expression such as `sawmvei` 'ten times' are all securely part of the current publication-facing section.

This normalized section therefore includes:

- decimal structure and the most useful cardinal bases;
- basic cardinal numerals and noun-plus-numeral counting phrases;
- compound tens and one Gospel teen expression;
- hundreds, thousands, and larger units only where the evidence is safe;
- ordinals with `-na`, anchored by `nihna`;
- counting expressions and classifier-like material, but only cautiously;
- occurrence-counting `sawmvei`;
- explicit ambiguity controls for `kua` and `khat`;
- distributive reduplication only as deferred material.

What it does **not** do is claim that the whole numeral chapter is finished. It does not promote raw generated-report counts as grammar facts, it does not normalize a full classifier system from thin evidence, and it does not import quantifier prose or dubious analyzer output without candidate control.

# Cardinal numerals

The table below gives the core numeral inventory needed for the present section. It is publication-facing orientation rather than a raw frequency table: the point is to show the basic system, while the formal examples below remain restricted to candidate-controlled or newly checked normalization rows.

| Value | Form | Current status in this section |
|---|---|---|
| 1 | `khat` | basic numeral; keep numeral/indefinite overlap explicit |
| 2 | `nih` | clean basic cardinal |
| 3 | `thum` | basic cardinal recognized in the report/literature layer |
| 4 | `li` | basic cardinal recognized in the report/literature layer |
| 5 | `nga` | basic cardinal recognized in the report/literature layer |
| 6 | `guk` | basic cardinal recognized in the report/literature layer |
| 7 | `sagih` | clean basic cardinal in current examples |
| 8 | `giat` | basic cardinal recognized in the report/literature layer |
| 9 | `kua` | numeral `nine` only in constructionally numeral contexts |
| 10 | `sawm` | ten base |
| 100 | `za` | hundred base |
| 1,000 | `sing` | thousand base; not fully normalized in this pass |
| 10,000 | `tul` | larger unit recognized in the report/literature layer; not fully normalized in this pass |

The table does not by itself authorize every form for immediate print-heavy exposition. It gives the normalized section a visible inventory, while the examples below keep the actual printed claims small and checked.

# Decimal composition

The safest current descriptive claim is that Tedim builds higher numerals through decimal composition, but the publication-facing section should phrase that conservatively. The report and literature support a decimal structure [@zamngaihcing2017; @henderson1965], while the current packet gives two especially useful checked examples: one Old Testament compound-ten anchor and one Gospel counted-noun expression with a compound numeral.

Genesis 5:9 remains the best controlled compound-ten anchor:

(@ex:num-sawmkua) Genesis 5:9
a. Tedim: kum sawmkua
b. Segmentation: kum | sawm-kua
c. Gloss: year | ten-nine
d. Translation: 'ninety years'

Matthew 9:20 gives a good Gospel counted-noun expression with a compound numeral:

(@ex:num-kum-sawm-le-nih) Matthew 9:20
a. Tedim: kum sawm le nih
b. Segmentation: kum | sawm | le | nih
c. Gloss: year | ten | and | two
d. Translation: 'twelve years'

These two rows are enough to support a modest decimal-composition claim. `Sawmkua` shows a clean compound-ten pattern and keeps numeral-side `kua = nine` visible in a securely numeral context. `Kum sawm le nih` shows that a counted noun can also host a larger compound numeral in Gospel material, which helps the section avoid becoming a grammar of Genesis.

The section should still stop short of a full typology of every higher numeral pattern. The report mentions wider two-digit and larger-number combinations, but the present normalized section only promotes the best checked examples.

Hundreds, thousands, and larger-number expressions are real parts of the system, but they need more caution than the simple and compound-ten rows. The current large-number anchor remains useful because it shows real biblical number style, not because every detail of the analyzer export is already polished:

(@ex:num-large) Genesis 5:27
a. Tedim: kum zakua le kum sawmguk le kua
b. Segmentation: kum | za-kua | le | kum | sawm-guk | le | kua
c. Gloss: year | hundred-nine | and | year | ten-six | and | nine [export: who]
d. Translation: 'nine hundred sixty and nine years'

This is still a print-usable-with-caveat example. The wider construction is clearly numeral, but the export compresses `za-kua`, and the final `kua` is glossed as `who` in the current export layer. The normalized section therefore keeps the row with its analyzer caveat visible instead of pretending that the export is already perfect.

# Ordinals

The safest current ordinal claim is that Tedim has `-na` ordinal formation, with `nihna` as the best controlled anchor. This is consistent with the report and literature [@zamngaihcing2017].

(@ex:num-nihna) Genesis 7:11
a. Tedim: nihna
b. Segmentation: nih-na
c. Gloss: two-NMLZ
d. Translation: 'second'

`Nihna` is the current print-ready ordinal row. The dossier already notes that `pos_span = N` in the export; that is a label caveat, not a reason to reject the ordinal analysis.

`Masa` remains visible but deferred. Gospel material such as Matthew 10:2 confirms that `masa` is a live background form for 'first', but the present section does not yet promote it as the normalized ordinal anchor because the current candidate-controlled packet is still built around `nihna`, not around a full ordinal paradigm or a full contrast between `masa` and `khatna`-type forms.

# Counting phrases and word order

The clearest current word-order claim is still modest: noun-plus-numeral patterns are securely attested. Counted nouns such as `kum` 'year' and `ni` 'day' clearly precede the numeral in the best current examples, and the normalized section now keeps both Old Testament and Gospel evidence visible for that pattern.

(@ex:num-kum-nih) Genesis 11:10
a. Tedim: kum nih
b. Segmentation: kum | nih
c. Gloss: year | two
d. Translation: 'two years'

(@ex:num-ni-sagih) Genesis 7:10
a. Tedim: ni sagih
b. Segmentation: ni | sagih
c. Gloss: day | seven
d. Translation: 'seven days'

(@ex:num-ni-li) John 11:39
a. Tedim: ni li
b. Segmentation: ni | li
c. Gloss: day | four
d. Translation: 'four days'

These are clean counted-noun examples, and they justify a real publication-facing statement that noun-plus-numeral order is well supported. The normalized section should still avoid overclaiming a complete typology of numeral placement. The broader report layer contains more patterns, and the literature discusses wider numeral syntax, but the checked publication-facing section should stop at what the current examples support directly.

The Gospel search for this pilot found good counted-noun examples such as `ni li` and `kum sawm le nih`. That is enough to improve source balance. It does **not** mean that every numeral construction in the section now has an equally good Gospel counterpart.

# Classifier-like and counting expressions

The report and literature mention classifier-like material and counting expressions, but the current normalized section should stay selective. Only the rows that are candidate-controlled or newly checked for this pilot should be promoted.

The safest current occurrence-counting row is still `sawmvei`:

(@ex:num-sawmvei) Genesis 31:7
a. Tedim: sawmvei
b. Segmentation: sawm-vei
c. Gloss: ten-times
d. Translation: 'ten times'

The generated report paraphrases this as `vei sawm`, but the current analyzer export preserves the fused form `sawmvei`. That export-backed `sawmvei` form means the fused form should control the present slice.

`Mi khat` remains valuable boundary evidence:

(@ex:num-mi-khat) Genesis 32:24
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: 'a man' / 'one person'

This is why the section discusses `mi khat` here but does not treat it as an uncomplicated bare numeral `one` example. It should not be treated as an uncomplicated bare numeral `one` example. It sits exactly on the numeral/indefinite boundary.

The classifier-like material can therefore be summarized cautiously:

| Expression or form | Current treatment | Reason |
|---|---|---|
| `mi khat` | print-usable with caveat | numeral/indefinite boundary, not a simple classifier row |
| `sawmvei` | print-usable with caveat | clear occurrence-counting expression |
| `pa`, `nu`, `zat`, `tei` | deferred | promising report/literature material, but not normalized in this pass |

This means the section can talk about classifier-like and counting expressions without pretending that the full classifier system has already been normalized. It also means the section does not start a quantifiers retrofit here.

# Distributive numerals

Distributive numerals remain deferred in this pilot. The previous generated-report claim for distributive `sagih sagih` is not print-ready because the current analyzer/candidate layer still does not support the repeated span in the key Genesis 7:2 row. The generated report is useful background orientation, but it should not outrun the current checked evidence.

This is exactly the kind of place where normalization must stay disciplined. The normalized section can say that distributive reduplication is a promising area in the report and literature, but it should still defer `sagih sagih` until the analyzer-backed evidence is clean enough to promote.

# Ambiguity controls

Two ambiguity controls remain central to the section: `kua` 'nine' must stay in clearly numeral contexts so that it is not confused with the interrogative form `kua` 'who', and `khat` 'one' still needs explicit boundary notes where numeral and indefinite-like uses overlap.

| Form | Numeral-side use | Competing use | Current print policy |
|---|---|---|---|
| `kua` | `sawmkua`; Genesis 5:27 large-number phrase | interrogative `who` | print only in constructionally numeral contexts |
| `khat` | basic cardinal 'one' | indefinite-like readings such as `mi khat` | keep explicit boundary notes; do not overgeneralize article-like use |

The blocked `kua` control remains Genesis 48:8:

> Hihte kua ahi hiam?

That row belongs to the interrogatives packet, not to numerals. Future numerals prose must therefore not use raw `kua` hits as numeral evidence.

The `khat` side of the control is different. `Khat` is unquestionably part of the numeral inventory, but not every `khat` example is equally good as a bare numeral illustration. The best currently controlled boundary row is still `mi khat`, and no cleaner Gospel `khat` boundary example was strong enough to replace it in this pilot.

# Summary

The normalized numerals section now supports a genuine publication-facing description. Tedim has a decimal numeral system with basic cardinals, compound tens, larger bases such as `za`, `sing`, and `tul`, `-na` ordinals, noun-plus-numeral counting phrases, and at least one compact occurrence-counting expression. The section now includes multiple formal examples, a visible inventory table, and both Old Testament and Gospel evidence where the checked material allows it.

At the same time, the section keeps the important boundaries explicit. `Sawmvei` remains tied to its fused-export caveat; the Genesis 5:27 large-number phrase remains usable only with analyzer caveats; `mi khat` remains boundary evidence; `kua` must stay constructionally controlled; and distributive `sagih sagih` remains deferred until the repeated span is genuinely analyzer-backed.
