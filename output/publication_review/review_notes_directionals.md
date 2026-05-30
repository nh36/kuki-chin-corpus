---
title: "Review Notes: Tedim Directionals Print Slice"
---

# What works

The directionals packet is now aligned at the current candidate-first maturity level. It has `candidates_directionals.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_directionals.md`, `grammar_directionals_print_slice.md`, `dictionary_directionals_print_slice.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_directionals.tsv`, interpreted through `dossier_directionals.md`, and cross-checked against `grammar_directionals_print_slice.md` plus `dictionary_directionals_print_slice.md`, not by raw generated-report counts and not by broad string searches over directional-looking forms.

The core analysis is now synchronized in the right way. `Pokhia` is the clean outward `-khia` anchor. `Nawhkhiat` is usable as away `-khiat` evidence only with its analyzer-label caveat. `Hotkhiatna` keeps nominalized `-khiat-na` boundary material visible without being flattened into a finite directional predicate. `Kilaktoh` is the usable upward `-toh` anchor, but only with the explicit polysemy and comitative/accompany caveat supplied by blocked `paitoh`. `Kahtohna` keeps nominalized `-toh-na` boundary material visible. `Tawplam` remains direction/side/manner boundary material rather than a clean verbal directional suffix. `Piasawn` is the current cautious toward `-sawn` row. `Paisuk` is the packet's corpus-backed downward `-suk` row. `uilut`, `paiphei`, `cip`, and `tang` remain deferred or not print-ready.

# What does not yet work

The packet is intentionally narrow and does not yet describe the full directional system. It does not yet support raw suffix harvesting over every `khia`, `khiat`, `toh`, `lam`, `sawn`, `lut`, `suk`, `phei`, `cip`, or `tang` ending, and it does not yet treat all lexicalized directional-looking forms as print-ready directional evidence.

It also does not build a full VP-slot chapter, a full TAM or aspect account, or a broader lexical rewrite. Nominalized `-na` forms should not be promoted as if they were finite directional predicates, and `-lut`, `-phei`, `-cip`, plus `-tang` should not be promoted without cleaner analyzer-backed corpus rows than the current packet provides. Generated-report raw count tables remain outside the candidate layer.

# Analyzer/export and overlap caveats

The main analyzer/export and overlap caveats are now explicit and manageable. `Nawhkhiat` keeps away `-khiat` visible, but the export still labels the selected lemma/POS as `nawh` / `N`, so the row must carry an analyzer-label caution. `Hotkhiatna` and `kahtohna` keep directional morphology visible under nominalization, but both remain boundary material rather than simple finite directional predicates. `Kilaktoh` is usable as upward `-toh`, but it must stay paired with blocked `paitoh`, which remains lexicalized `go-accompany` / comitative-overlap material rather than upward evidence.

`Tawplam` keeps `-lam` visible only as direction/side/manner boundary material because the export profile remains nominal (`tawp` / `N`). `Piasawn` is more useful than kinship-heavy or lexicalized-looking `-sawn` rows, but it still needs a construction-controlled reading. `Paisuk` matters because it gives `-suk` a corpus-backed candidate row rather than leaving the suffix supported only by analyzer tests. `uilut`, `paiphei`, `cip`, and `tang` remain deferred because the current analyzer-backed corpus rows are not yet clean print-safe anchors.

These caveats are not reasons to reopen the packet. They are reasons to keep the candidate TSV, dossier, grammar slice, dictionary slice, and review notes aligned and to keep raw generated-report counts outside the evidence layer.

# Print-slice cautions

The following claims are safe at the current slice maturity level:

- `-khia` as outward evidence through `pokhia`;
- `-khiat` as away evidence through `nawhkhiat`, only with analyzer-label caveat;
- `-khiat-na` through `hotkhiatna` only as nominalized boundary material;
- `-toh` as upward evidence through `kilaktoh`, only with the `paitoh` comitative/accompany caveat;
- `-toh-na` through `kahtohna` only as nominalized boundary material;
- `-lam` only as direction/side/manner boundary material through `tawplam`;
- `-sawn` only as cautious toward evidence through `piasawn`;
- `-suk` only as corpus-backed downward evidence through `paisuk`.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- raw suffix harvesting over directional-looking spellings;
- `paitoh` as upward `-toh`;
- nominalized `-na` forms treated as equivalent to finite directional predicates;
- `-lut`, `-phei`, `-cip`, and `-tang` promoted without cleaner analyzer-backed corpus rows;
- broad VP-slot or TAM prose;
- chrestomathy, Mizo/lus, and other Kuki-Chin languages.

# Recommended next editorial task

With these review notes added, the directionals packet is now ready for human review at the current slice maturity level. Any later directionals changes should come from a specific reviewer-identified defect, not from another open-ended polishing pass.

The next substantive repository task after this commit should not begin a new grammar packet automatically. It should be human review of the completed packets. Broad TAM, chrestomathy, Mizo/lus, and other Kuki-Chin languages remain deferred until they are explicitly chosen as a new scope.
