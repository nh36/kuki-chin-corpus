---
title: "Review Notes: Tedim Numerals Print Slice"
---

# What works

The numerals packet is now aligned at the current candidate-first maturity level. It has `candidates_numerals.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_numerals.md`, `grammar_numerals_print_slice.md`, `dictionary_numerals_print_slice.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_numerals.tsv` and `dossier_numerals.md`, not by raw generated-report counts and not by broad string searches over every numeral-looking form.

The core analysis is now synchronized in the right way. Basic noun-plus-numeral counting examples are represented by `kum nih` and `ni sagih`. Compound-ten `sawmkua` is represented and also controls `kua = nine` in numeral context. Ordinal `nihna` is represented, while `masa` remains deferred. Occurrence-counting `sawmvei` is represented as the export-backed fused form rather than being silently replaced by report wording `vei sawm`. The Genesis 5:27 large-number row `kum zakua le kum sawmguk le kua` is usable with explicit analyzer caveats. `Kua` ambiguity is controlled by the fact that `Hihte kua ahi hiam?` / Genesis 48:8 remains blocked as numeral evidence. `Mi khat` is kept on the numeral/indefinite boundary, and distributive `sagih sagih` remains deferred because the current analyzer export does not support the repeated span.

# What does not yet work

The packet is intentionally narrow and does not yet describe the full numeral system. It does not yet include a full cardinal paradigm, it does not build a full ordinal paradigm, and `masa` remains deferred rather than promoted as a print anchor for `first`.

The packet also does not yet solve classifier or counting systems beyond `sawmvei`. Distributive reduplication remains not print-ready. `Khat` still overlaps with indefinite or quantifier work, and `kua` still requires constructional control because it can also mean `who`. Generated-report raw frequency tables remain outside the candidate layer and should not be allowed back into the print packet.

# Analyzer/export caveats

The main analyzer/export caveats are now explicit and manageable. `Sawmkua` has good segmentation and gloss, but the lemma/POS export is flattened (`kum | sawm`, `N | N`). `Nihna` has `pos_span = N`, which should be treated as a label caveat rather than as a rejection of the ordinal analysis. `Sawmvei` is the export-backed fused form, so generated-report `vei sawm` should not be substituted silently. In Genesis 5:27, the final `kua` is glossed as `who` in the export even though the constructional reading is numeral `nine`. In Genesis 7:2, the current export preserves only one `sagih` token, so `sagih sagih` remains deferred.

These caveats are not reasons to reopen the packet. They are reasons to keep the candidate, dossier, grammar, and dictionary layers aligned and to preserve explicit editorial notes where the export remains flatter than the constructional analysis.

# Print-slice cautions

The following claims are safe at the current slice maturity level:

- noun-plus-numeral counting examples with `kum nih` and `ni sagih`;
- compound-ten `sawmkua`;
- ordinal `nihna`;
- occurrence-counting `sawmvei` with caveat;
- large-number phrase evidence with caveat;
- `kua` as numeral only in constructionally numeral contexts;
- `mi khat` only as boundary evidence.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- a full numeral paradigm;
- `masa` as a promoted ordinal entry;
- `sagih sagih` as accepted distributive reduplication;
- a full classifier system;
- treating every raw `kua` as numeral `nine`;
- treating `mi khat` as an uncomplicated bare `one` example;
- quantifier prose imported into numerals.

# Recommended next editorial task

With these review notes added, the numerals packet is now ready for human review at the current slice maturity level. Any later numerals changes should come from a specific reviewer-identified defect, not from another open-ended polishing pass.

The next substantive repository task after this commit should therefore be a deliberately chosen next narrow retrofit target from the remaining inventory rather than more numerals polishing. Likely next deferred candidates include quantifiers, coordinators, and sentence-final particles. Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages should remain deferred.
