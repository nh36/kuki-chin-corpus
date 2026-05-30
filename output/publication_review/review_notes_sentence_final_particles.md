---
title: "Review Notes: Tedim Sentence-Final Particles Print Slice"
---

# What works

The sentence-final particles packet is now aligned at the current candidate-first maturity level. It has `candidates_sentence_final_particles.tsv`, a curated extractor route in `scripts/publication_review/extract_candidates.py`, `dossier_sentence_final_particles.md`, `grammar_sentence_final_particles_print_slice.md`, `dictionary_sentence_final_particles_print_slice.md`, `review_notes_sentence_final_particles.md`, and tests covering the main distinctions. The grammar and dictionary slices are controlled by `candidates_sentence_final_particles.tsv` and `dossier_sentence_final_particles.md`, not by raw generated-report counts and not by broad string searches over particle-looking forms.

The core analysis is now synchronized in the right way. `Hi` is visible only through the construction-controlled `ahi hi` and `thusim lo hi` rows. `Ahi hi` is copula-plus-declarative evidence, not bare `hi` evidence. `Thusim lo hi` is negation-overlap evidence and does not reopen negation. `Hiam` remains controlled by the stabilized interrogatives packet. `Khuavak om hen` is the current usable optative row. `Teembaw khat bawl in` keeps singular imperative `in` visible only with `ERG` / `FUNC` and case-overlap caveats. `Gingsak un` is the cleanest current plural-imperative anchor. `Gam khempeuh aw` remains vocative or exclamative boundary material rather than settled sentence-final mood evidence. The `hi tahen`, `mangngilh ta hi`, and `zo` rows remain deferred or needs-review because the export is noisy.

# What does not yet work

The packet is intentionally narrow and does not yet describe the full sentence-final particle system. It does not yet provide a bare `hi` declarative anchor, it does not reopen `hiam` or the interrogatives packet, and it does not yet promote `tahen` as settled jussive evidence.

It also does not yet promote `aw` as a settled sentence-final mood particle, and it does not yet promote `ta` or `zo` as settled aspectual particles. The packet does not build a full mood, aspect, or TAM chapter, and generated-report raw frequency tables remain outside the candidate layer.

# Analyzer/export and overlap caveats

The main caveats are now explicit and manageable. `Ahi hi` bundles copular `ahi` plus final `hi`, so it cannot license raw `hi` harvesting. `Thusim lo hi` overlaps negation and should cross-reference, not reopen, the negation packet. `Hihte kua ahi hiam?` is overlap control for the interrogatives packet, so `hiam` should not be reanalyzed here. The `hi tahen` row remains deferred because `tahen` is exported as `army` / `N`, and fused `tahen` versus split `ta hen` noise should remain visible. `Khuavak om hen` is analyzer-backed as `om hen` and should not be replaced by report-style `ta hen`.

`Teembaw khat bawl in` keeps singular imperative `in` visible, but the export still gives `in` as `ERG` / `FUNC`, so the row has case-marker overlap. `Gingsak un` is the clean anchor, but nearby `aw` material in the same verse must not be absorbed. `Gam khempeuh aw` has `aw` exported as `voice` / `N` and remains boundary material only. The `mangngilh ta hi` row has `ta` exported as `child` / `FUNC` and remains TAM-overlap material. The `zo` row is exported as `south` / `N` and remains deferred.

# Print-slice cautions

The following claims are safe at the current slice maturity level:

- `ahi hi` as copula-plus-declarative evidence with caveat;
- `thusim lo hi` as negation-plus-declarative evidence with caveat;
- `Khuavak om hen` as optative evidence with caveat;
- `teembaw khat bawl in` as singular imperative evidence only with case-overlap caveat;
- `gingsak un` as the clean plural-imperative anchor;
- `hiam` only as interrogatives cross-reference.

The following should stay out of print for now:

- raw frequency counts from generated reports;
- bare `hi` as a general declarative particle;
- `hiam` as new sentence-final evidence;
- `tahen` as settled jussive;
- `aw` as settled exclamative or mood particle;
- `ta` and `zo` as settled aspectual particles;
- broad TAM or full mood/aspect chapters;
- directionals, chrestomathy, Mizo/lus, or other Kuki-Chin languages.

# Recommended next editorial task

With these review notes added, the sentence-final particles packet is now ready for human review at the current slice maturity level. Any later sentence-final changes should come from a specific reviewer-identified defect rather than from another open-ended polishing pass.

The next substantive repository task after this commit should not be more sentence-final particles polishing. It should be a deliberately chosen new scope from the remaining inventory only if one is explicitly selected. Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin languages remain deferred.
