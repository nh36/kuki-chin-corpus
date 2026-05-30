---
title: "Review Notes: Tedim Coordinators Print Slice"
---

# What works

The coordinators packet is now aligned at the current candidate-first maturity level. It has `candidates_coordinators.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_coordinators.md`, `grammar_coordinators_print_slice.md`, `dictionary_coordinators_print_slice.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_coordinators.tsv` and `dossier_coordinators.md`, not by raw generated-report counts and not by broad string searches over coordinator-looking forms.

The core analysis is now synchronized in the right way. `Le` is the current safe NP-conjunction anchor, represented by Genesis 1:1 `vantung le leitung`, and it does not license raw `le` harvesting. `Leh` is visible, but only as conditional or boundary evidence rather than as a clean print-ready simple clause conjunction. The Genesis 13:9 row `veilam na lak leh kei taklamah ka pai ding hi` keeps the `kei = NEG` export caveat visible without reopening pronouns or negation. Sequential `a` is visible only as caveated boundary evidence in `luang a tua mun panin gun hong kikhenin`, and it stays paired with the blocked agreement or function control `a piangsak`. `Mawh` remains deferred because the current export is lexical or analyzer-noise material glossed as `sin` / `V` rather than disjunction. `Ahih hangin` is usable as an adversative connector with an internal-analysis and `hangin` caveat, while `ahih kei leh` is useful only as conditional-adversative boundary material rather than as a simple coordinator.

# What does not yet work

The packet is intentionally narrow and does not yet describe the full coordination system. It does not yet have a clean accepted simple clause-conjunction `leh` row, it does not yet have clean `mawh` disjunction or alternative-question evidence, and it does not yet solve sequential `a` or clause-chaining or converb coordination.

It also does not build a full temporal or causal subordinator treatment for `ciangin` or `hangin`, and it does not touch sentence-final particles. Generated-report raw frequency tables remain outside the candidate layer and should not be allowed back into the print packet.

# Analyzer/export and overlap caveats

The main analyzer/export caveats are now explicit and manageable. Genesis 13:9 keeps `leh` visible only as conditional or boundary material, and `kei` is glossed as `NEG` in the export despite the wider "I will go" context. Genesis 2:10 sequential `a` is exported as `3SG` / `FUNC`, so it remains caveated and not print-ready. Genesis 1:1 `a piangsak` remains blocked agreement or function material rather than coordinator evidence. Genesis 6:3 `mawh` remains lexical or analyzer-noise material glossed as `sin` / `V`. `Ahih hangin` remains internally analyzable as `ahih` + `hang-in`. `Ahih kei leh` overlaps with negation and conditional `leh`, but that overlap should not reopen negation.

These caveats are not reasons to reopen the packet. They are reasons to keep the candidate, dossier, grammar, and dictionary layers aligned and to preserve explicit editorial notes where the export is flatter than the constructional analysis.

# Print-slice cautions

The following claims are safe at the current slice maturity level:

- `le` as NP conjunction, anchored by `vantung le leitung`;
- `Ahih hangin` as adversative connector with caveat;
- `ahih kei leh` as conditional-adversative boundary material with caveat;
- `leh`, `a`, and `mawh` only as boundary, deferred, or warning material.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- treating every `le`, `leh`, or `a` token as coordinator evidence;
- treating conditional `leh` as simple clause-conjunction "`and`";
- accepting `mawh` as disjunction from report-only examples;
- building a full sequential-`a` analysis;
- building a full clause-chaining or converb coordination account;
- importing sentence-final particles or broad TAM into coordinator prose.

# Recommended next editorial task

With these review notes added, the coordinators packet is now ready for human review at the current slice maturity level. Any later coordinators changes should come from a specific reviewer-identified defect, not from another open-ended polishing pass.

The next substantive repository task after this commit should therefore not be more coordinators polishing. It should be a deliberately chosen next narrow retrofit target from the remaining inventory. Sentence-final particles remains the likely next deferred narrow target, while broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages should remain deferred.
