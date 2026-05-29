---
title: "Review Notes: Tedim Interrogatives Print Slice"
---

# What works

The interrogatives packet is now aligned at the current candidate-first maturity level. It has `candidates_interrogatives.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_interrogatives.md`, `grammar_interrogatives_print_slice.md`, `dictionary_interrogatives_print_slice.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_interrogatives.tsv` and `dossier_interrogatives.md`, not by raw report counts or by broad string searches over every `hiam` or `bang` form.

The core analysis is now synchronized in the right way. Clause-final `hiam` is controlled by the attested Genesis 24:23 example `Na pa inn-ah kote giah nading a awng ding hiam`, not by the older generated-report paraphrase `Inn-ah hong tum theih na hiam`. WH + `hiam` is represented by `bang`, `kua`, `bangci`, and `banghangin`. Embedded `bang hiam cih` material is visible in the packet but not promoted into the core print examples. Blocked rows are also explicit, so raw-search false friends are much less likely to leak into print examples by accident.

The packet is also appropriately narrow. Formulaic `Bang hang hiam cih leh`, lexical or non-interrogative `a hiam` material, and bang-family false friends such as `bangmah` and `bangin` are all recorded as controls rather than recycled as print anchors. Comparison particles `maw`, `ham`, and `em` remain deferred, which is the right choice for a first narrow interrogatives slice rather than a full sentence-final particle chapter.

# What does not yet work

The packet is intentionally narrow and still does not describe the full interrogative system. `Hiam` remains the core marker represented here, but it still has lexical or non-interrogative false friends. Bang-family material remains dangerous because `bangmah` and `bangin` are not ordinary `bang` questions even though raw string matching can surface them.

Analyzer/export caveats also remain visible. `Kua` is still tagged as `NUM` in the analyzer export, `bang` in Exodus 16:15 is glossed as `like`, and `banghangin` is exported as `bang | hang-in`. Those caveats do not overturn the packet's clause-level readings, but they do need to remain explicit in the dossier and aligned print slices.

Embedded `bang hiam cih` material also still needs a later treatment of complementation or embedded questions. The current packet keeps it visible, but correctly stops short of treating it as an ordinary independent clause-final `hiam` example. Likewise, `maw`, `ham`, and `em` remain outside the present slice.

# Print-slice cautions

The following claims are now safe at the current print-facing maturity level:

- `hiam` as a candidate-backed question particle in the current print packet;
- clause-final `hiam` in accepted yes/no evidence;
- WH + `hiam` as the represented content-question pattern;
- `bang`, `kua`, `bangci`, and `banghangin` as the current candidate-backed WH evidence.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- "always clause-final" wording;
- the older Genesis 24:23 paraphrase `Inn-ah hong tum theih na hiam` as a print anchor;
- embedded `bang hiam cih` as an ordinary independent-clause example;
- formulaic `Bang hang hiam cih leh`;
- lexical or non-interrogative `a hiam` rows such as `a hiam ciat uh` and `langnih a hiam namsau`;
- `bangmah` and `bangin` as ordinary `bang` evidence;
- `maw`, `ham`, and `em` as part of the core `hiam` / WH slice.

# Recommended next editorial task

With these review notes added, the interrogatives packet is now ready for human review at the current slice maturity level. Any later interrogatives changes should come from a specific reviewer-identified defect, not from another open-ended polishing pass.

The next substantive repository task after this commit should therefore be a deliberately chosen next narrow retrofit target from the remaining inventory rather than more interrogatives work. Likely next deferred candidates include numerals, quantifiers, coordinators, and sentence-final particles, while broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages should remain deferred until they are explicitly chosen.
