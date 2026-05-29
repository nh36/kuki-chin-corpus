---
title: "Review Notes: Tedim Case-Marking Print Slice"
---

# What works

The revised slice now reads more like a draft chapter than like an internal dashboard. The grammar prose is anchored to the main descriptive literature, the examples are presented in a stable Pandoc-friendly format, and the dictionary entries are now closer to reader-facing print copy. The section on `-tawh` is materially better because it no longer treats Genesis 2:7 and Genesis 2:21 as if they were ordinary accompaniment examples; it now distinguishes accompaniment from material or instrument-like extension.

The ergative section is also stronger than before. A candidate-backed example from Genesis 4:3 now allows the chapter and dictionary slice to print `-in` as a real grammatical entry rather than leaving it entirely abstract. This is the right kind of intervention for the slice: small, explicit, and editorially controlled rather than algorithmically overconfident.

The packet is also now aligned with the candidate-first protocol. It has `candidates_case_marking.tsv`, `dossier_case_marking.md`, an extractor route in `scripts/publication_review/extract_candidates.py`, and LF-stable reproducible candidate output. That means the print slices can now be reviewed against an explicit evidence layer rather than against ad hoc manual selection alone.

# What does not yet work

The packet is now reproducible, but it should still remain conservative. Homographic `-in` rows such as `ciangin` remain a live ambiguity risk, `-a` still cannot be cleanly separated from `-ah` and other functional material, and `-panin` still needs a structural caveat even where it is accepted as source-marking evidence.

The source discussion around relator nouns also still needs discipline. `lakpan` is best treated as source marking on a relator noun, not as a bare suffix example, and source-vs-relator-noun boundaries remain part of the packet rather than a separable afterthought. Likewise, `-tawh` still needs to stay split between accompaniment and material/instrumental extension.

Analyzer export caveats also remain visible. Some locative and relator rows surface with tags such as `pos_span=FUNC` even where the editorial grammar still treats the base as nominal or relational. Those labels are useful as export metadata, but they are not decisive enough to replace the packet's grammatical analysis.

The citation-key problem is now resolved: the grammar slice cites only keys that exist in `literature/bibliography.bib`. Henderson, Zam Ngaih Cing, Otsuka, and the Sukte grammar now all resolve under Pandoc without ad hoc review-draft keys.

# Bibliography correction note

The uploaded source PDFs were checked directly and the Tedim bibliography entries were corrected against those files. This includes the Otsuka causative, applicative, Burmese loanwords, and voice papers, the Otsuka-Kurabe directional-affixes handout, and the Zam Ngaih Cing thesis metadata used by the case-marking slice.

Two uncertainties remain explicit in the bibliography. The exact venue and year of the Otsuka-Kurabe directional-affixes handout still need independent confirmation beyond the uploaded PDF, so the entry is kept conservative. The Zam thesis is cited here as 2017 following Otsuka’s own reference lists, while the local split PDF filenames still contain 2018.

# Recommended next editorial task

The next task should still be reviewing this case-marking slice itself rather than moving on to a new section. The specific questions are now clearer: how narrowly the packet should continue to gate `-in`, whether `-panin` should remain a cautious source-marking entry, how strongly the final chapter should foreground relator nouns, and how much weight to give analyzer POS/export labels when they look flatter than the editorial analysis.

# Decision for next slice

This case-marking slice is now good enough to serve as the model for the next print-facing grammar and dictionary slice. The main remaining editorial question is how fully relator nouns should be integrated into the printed chapter structure, but that question is now clear enough to carry forward as a controlled design decision rather than a blocker.
