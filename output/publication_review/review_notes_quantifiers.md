---
title: "Review Notes: Tedim Quantifiers Print Slice"
---

# What works

The quantifiers packet is now aligned at the current candidate-first maturity level. It has `candidates_quantifiers.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_quantifiers.md`, `grammar_quantifiers_print_slice.md`, `dictionary_quantifiers_print_slice.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_quantifiers.tsv` and `dossier_quantifiers.md`, not by raw generated-report counts and not by broad string searches over every quantifier-looking form.

The core analysis is now synchronized in the right way. `Khempeuh` is the current universal anchor. `Pawlkhat` is treated as partitive or alternative-grouping evidence rather than as an uncomplicated bare `some` entry. `Mi khat` is kept on the numeral/indefinite boundary. `Kuamah mu lo` and `bangmah om lo hi` are usable only in negative-licensed contexts. `Tua bangmah hi-in` remains blocked as ordinary quantifier evidence. `Tampi tak` is the current degree/quantity anchor. `Vanglian zaw` and `hau mahmah` are kept as comparative or intensifier edge rows. `Peuhpeuh` and `tawm` remain deferred and not print-ready.

# What does not yet work

The packet is intentionally narrow and does not yet describe the full quantifier system. It does not yet build a full universal or distributive system, and `peuhpeuh` remains deferred because the current `mi peuhpeuh` row behaves more like free-choice `whoever / any person` material than settled distributive-universal evidence.

`Tawm` also remains deferred because the current export glosses it as `produce`, so the low-quantity reading is too noisy for print promotion. `Khat` still overlaps with numerals and indefinites. `Kuamah` and `bangmah` still require negative licensing, and `bangmah` still has bang-family or interrogative-overlap risks. `Tampi`, `zaw`, and `mahmah` should not become a broad adjective/adverb, degree, intensifier, or comparative chapter. Generated-report raw frequency tables remain outside the candidate layer.

# Analyzer/export and overlap caveats

The current caveats are explicit enough to keep the packet stable. `Pawlkhat` is clean only in the later Genesis 32:8 token, so the noisy opening `Pawlkhatah` should not be substituted. `Mi khat` is boundary evidence reused from the numerals packet. `Kuamah mu lo` and `bangmah om lo hi` are quantifier evidence only with clear negative licensing and negation overlap. `Tua bangmah hi-in` remains blocked. `Mi peuhpeuh` remains deferred. `Tawm` remains export-noisy because the current gloss is `produce`. `Vanglian zaw` and `hau mahmah` remain edge rows rather than a broader system.

# Print-slice cautions

The following claims are safe at the current slice maturity level:

- `khempeuh` as the current universal anchor;
- `pawlkhat` as partitive or existential evidence with caveat;
- `khat` only as numeral/indefinite boundary evidence;
- `kuamah` and `bangmah` only in negative-licensed contexts;
- `tampi tak` as degree/quantity evidence;
- `zaw` and `mahmah` as edge rows only.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- `peuhpeuh` as settled distributive-universal evidence;
- `tawm` as settled low-quantity evidence;
- `bangmah` outside clear negative licensing;
- `khat` as an uncomplicated article-like quantifier;
- a full universal/distributive system;
- a full degree/intensifier/comparative chapter;
- coordinators or sentence-final particles imported into quantifier prose.

# Recommended next editorial task

With these review notes added, the quantifiers packet is now ready for human review at the current slice maturity level. Any later quantifiers changes should come from a specific reviewer-identified defect, not from another open-ended polishing pass.

The next substantive repository task after this commit should therefore be a deliberately chosen next narrow retrofit target from the remaining inventory rather than more quantifiers polishing. Likely next deferred candidates include coordinators and sentence-final particles. Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages should remain deferred.
