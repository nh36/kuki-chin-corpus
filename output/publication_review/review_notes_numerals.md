---
title: "Review Notes: Tedim Numerals Print Slice"
---

# What works

The numerals packet is no longer only a first narrow slice. It now has `candidates_numerals.tsv`, `dossier_numerals.md`, `grammar_numerals_print_slice.md`, `dictionary_numerals_print_slice.md`, `review_notes_numerals.md`, the coverage target in `coverage_normalization_audit.md`, and the checked source-balance supplement `examples_numerals_normalization.tsv`. The grammar section is still controlled by candidate evidence and explicit caveats, not by raw generated-report counts and not by broad string searches over every numeral-looking form.

The normalized section now has the expected publication-facing components: a base numeral inventory table, a fuller overview of the decimal system, multiple formal examples, explicit source-balance improvement through Gospel examples, a classifier-like subsection that stays cautious, and a short descriptive summary rather than a packet-status ending.

The core analysis remains synchronized in the right way. `kum nih` and `ni sagih` remain useful Old Testament counted-noun anchors. `ni li` (John 11:39) and `kum sawm le nih` (Matthew 9:20) now supply clean Gospel evidence for the normalized section. `sawmkua` remains the main compound-ten control and the strongest numeral-side control for `kua = nine`. `nihna` remains the safe ordinal anchor. `sawmvei` remains the export-backed fused form rather than report paraphrase `vei sawm`. The Genesis 5:27 large-number row `kum zakua le kum sawmguk le kua` remains usable with explicit analyzer caveats. `mi khat` remains on the numeral/indefinite boundary, and distributive `sagih sagih` remains deferred because the current analyzer export does not support the repeated span.

# What still needs caution

The normalized section is fuller, but it is not a finished numeral chapter. It still does not build a full classifier system, it does not normalize every larger-number pattern, and it does not turn raw report metadata into publication prose. `Pa`, `nu`, `zat`, and `tei` remain promising classifier-like background material rather than fully normalized subsection anchors.

The large-number and occurrence-counting rows still need their earlier export caveats. `Sawmkua` has clear segmentation and gloss, but the lemma/POS export is flattened. `Nihna` still has `pos_span = N`. `Sawmvei` remains the export-backed fused form, so generated-report wording `vei sawm` should not be substituted silently. In Genesis 5:27, the final `kua` is still glossed as `who` in the export even though the wider construction is clearly numeral.

`Masa` remains visible but not promoted. Gospel material such as Matthew 10:2 confirms that `masa` is real background evidence for 'first', but the normalized section still keeps `nihna` as the controlled ordinal anchor and treats `masa` as deferred or needing separate confirmation before it becomes a printed ordinal anchor.

# Gospel search and source balance

The numerals pilot followed the example-selection policy in `coverage_normalization_audit.md`: first criterion example quality, second criterion source balance. The normalization search checked `data/verses_aligned.tsv` and `bibles/extracted/ctd/ctd-x-bible.txt` directly and recorded the promoted rows in `examples_numerals_normalization.tsv`.

The search succeeded in finding two good Gospel examples worth promoting:

- John 11:39 `ni li` for a clean noun-plus-numeral counting phrase;
- Matthew 9:20 `kum sawm le nih` for a counted-noun expression with a compound numeral.

The search did **not** produce a Gospel ordinal row clean enough to replace the current `nihna` anchor, and it did not produce a cleaner Gospel `khat` boundary row than Genesis 32:24 `mi khat`. Matthew 10:2 `a masa-in` remains useful background evidence only, not a new promoted ordinal anchor.

# Boundaries and blocked material

The packet still needs the same high-value controls as before.

- Genesis 48:8 `Hihte kua ahi hiam?` remains the blocked `kua = who` false friend and must stay outside numerals.
- `Mi khat` remains numeral/indefinite boundary evidence rather than an uncomplicated bare `one` example.
- `Sagih sagih` remains deferred and not print-ready.
- Raw generated-report counts remain outside the publication-facing grammar section.
- Quantifier prose is still outside the numerals packet even where `khat` overlaps with later quantifier work.

# Current maturity and next use

Numerals is now the first coverage-normalization pilot rather than only a first current-slice packet. It is ready for human review at that higher maturity level: the section is fuller, source-balanced where the checked material allows it, and explicit about what remains caveated or deferred.

Any later numerals changes should still be specific and controlled. The next plausible numerals work would be a later classifier or ordinal expansion only if new checked evidence supports it. Quantifiers, coordinators, sentence-final particles, broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages should still remain outside this numerals pilot.
