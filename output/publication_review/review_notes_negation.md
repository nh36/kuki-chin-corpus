---
title: "Review Notes: Tedim Negation"
---

# What works

This packet is strong enough to serve as a real print-facing negation model. The grammar slice reads as continuous prose, keeps the treatment narrow, and starts from the point the dossier established most clearly: Tedim negation cannot be reduced to `lo` alone. The resulting packet is better than the older generated negation report because it gives the reader a system rather than a single over-promoted marker.

The best part of the packet is the choice of examples. Ordinary clause-level `lo`, dependent `loh`, and prohibitive or irrealis-heavy `kei` are all represented with manually checked Bible verses rather than with raw dashboard counts. That makes the main editorial claims supportable in print: `lo` is the safest clause-level starting point, `loh` belongs in dependent and derived environments, and `kei` is central to real prohibitives.

The dictionary slice also now looks viable. Treating `lo`, `loh`, and `kei` as separate but connected entries gives the reader a clearer picture than a single undifferentiated "negation" entry would. The constructional entries `nawn lo` and `thei lo / theih loh` further show that the packet can handle grammar as a mix of particles and recurring constructions without sliding into a full TAM chapter.

# What does not yet work

The generated negation report remains too simple to serve as final print prose. It is still useful as discovery scaffolding, but it over-centres `lo`, underplays `kei`, and does not explain `loh` well enough. The slice therefore depends on the dossier and the aligned Bible corpus rather than on the generated report alone.

The current corpus evidence is strong, but not rigid enough to justify a one-line rule such as "`kei` is only first-person realis" or "`loh` is always Stem 2". The `lo` / `loh` / `kei` distribution is clearly real in the Bible data, but the packet is right to keep the rule system slightly hedged rather than pretending that every environment is already solved.

The NPI material still needs manual filtering. `Kuamah` and `bangmah` are good print material only when the examples are checked by hand, because raw exact-string searches overgenerate. `Kuamah` can be contaminated by non-pronominal strings, and `bangmah` has non-NPI uses such as `tua bangmah hi-in`.

Most importantly, the slice stays deliberately narrow. It does not attempt a full TAM treatment, and it does not move into directionals. That limit is a strength here, not a weakness.

# Citation and source audit

The grammar slice cites only bibliography keys that already exist in `literature/bibliography.bib`: `@henderson1965` and `@zamngaihcing2017`. No new bibliographic metadata was needed.

Source use is appropriately layered. The literature review establishes the expectation that Tedim negation includes both `-kei` and `-lou/-louh`; the generated report shows where the current backend remains too simple; the dossier records the corrected evidence picture; and the aligned Bible corpus supplies the actual print examples.

# Candidate-layer note

Negation now also has an analyzer-aware candidate file at `output/publication_review/candidates_negation.tsv`. That layer records accepted, excluded, and deferred rows for the main negation constructions, including the old Genesis 2:25 `lo uh` pitfall and non-negative or non-NPI false friends such as pronoun `kei` and lexical `bangmah` expressions.

The packet should now be read in the order `candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`. That keeps the grammar and dictionary slices anchored to analyzer-backed candidate rows rather than to raw string searches or report-level shortcuts.

# Analyzer/export caveats in the candidate layer

The candidate file uses analyzer-export spans, but some lemma and POS fields are still imperfect. Accepted status therefore rests on a three-part combination: analyzer-confirmed surface or token windows, manual verse review, and the constructional interpretation already established in the dossier and print packet.

The main caveats are visible in a small number of rows. In accepted dependent-negation rows, `loh` still exports with `Loh` and `PROP`-like values, and in Exodus 10:5 the following purposive token `nadingin` also surfaces with `PROP`-like export metadata. In the accepted cessative row, `nawn` currently exports as `Nawn` with POS `PROP` even though the construction itself is clear in context. In excluded Genesis 2:25, the export currently treats `uh` as POS `N`, which is another reminder that analyzer-backed does not mean analyzer-infallible.

These artifacts are not fatal for the current packet because the candidate layer is not pretending to be a fully automatic truth source. It is an auditable bridge between analyzer output and manual publication-review judgment. The important guarantee is that every promoted or excluded negation example now has an explicit analyzer-backed span and an explicit note when the export metadata itself is noisy.

# Report-correction notes

The generated negation report is useful but too simple. Its most serious error for print purposes is the prohibitive section: Genesis 2:25 `maizum lo uh hi` is not a prohibitive and must not be used that way. It is an ordinary declarative plural negative clause, "they were not ashamed".

The print packet therefore corrects three report-level problems explicitly. First, the negation system is not flattened to `lo`. Second, `V lo uh` is not presented as the prohibitive construction. Third, `loh` is represented as a real dependent or derived negative form rather than ignored as orthographic noise.

This hardening pass also cleaned workflow language out of the grammar slice, added explicit biblical references to every example block in the grammar and dictionary slices, and minimally corrected the old negation report so that it no longer points readers to Genesis 2:25 as a prohibitive.

The underlying analysis was not changed in this pass. The packet still treats `lo`, `loh`, and `kei` as parts of one negation system, still distinguishes `thei lo` from `theih loh`, and still keeps the NPI section tied to manually checked examples rather than raw exact-string counts.

# Dictionary integration notes

Dictionary integration now looks strong enough for print. `Lo`, `loh`, and `kei` should all be represented directly rather than folded into a single catch-all negator entry. That is the only way the dictionary can reflect the actual distribution seen in the corpus and in the grammar slice.

The packet also shows that negation needs both lexical and constructional entries. `Kuamah` and `bangmah` work as negative-polarity entries once the examples are filtered. `Nawn lo` and `thei lo / theih loh` work better as constructional entries because their print value lies in the recurring pattern, not in a single isolated morpheme.

The one necessary caveat is example filtering. `Kei` is homographic with the 1SG pronoun, and `kuamah` / `bangmah` overgenerate under raw string search. The present packet handles that correctly by relying on manually checked examples rather than on raw counts alone.

# Decision for next slice

With this cleanup and the standard validation rerun, the negation dossier, grammar slice, dictionary slice, and review notes can be treated as synchronized enough for the current publication-review workflow. Negation can now stand with the case-marking, pronoun, and stem-alternation packets as a stable narrow model.

The next substantive step should be to choose another narrow print-facing topic. It should not be a broad TAM chapter, and it should not move into directionals, chrestomathy, or Mizo/lus. The priority is to keep building the Tedim packet one synchronized narrow topic at a time.
