---
title: "Coverage Normalization Audit for the Assembled Grammar Review Preview"
---

# Purpose and controlling sources

This is a chapter-by-chapter coverage normalization audit for `output/publication_review/assembled_grammar_review_preview.md`. It is an editorial planning document, not a new grammar packet, not a rewrite of every chapter, and not a claim that the grammar is finished.

The controlling sources for this audit are:

- `output/publication_review/assembled_grammar_review_preview.md`
- `output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md`
- `output/publication_review/whole_grammar_coverage_audit.md`
- `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`
- `docs/SKELETON_GRAMMAR.md`
- `PROGRESS.md`

The audit also cross-checks the current grammar print slices, review notes, candidate TSVs, dossiers, and source reports for the topics already assembled into the review-preview PDF.

# Working diagnosis

The assembled PDF is now useful as a review preview, but it is not yet homogeneous as a grammar. The main unevenness is not PDF formatting. It is that some chapters already read like medium-draft grammar sections, while others still read like first-pass narrow slice packets, argument plans, or gap markers.

The audit answers the current editorial questions as follows:

1. **Which topics have fuller upstream evidence than the current print slice shows?** Numerals, quantifiers, coordinators, sentence-final particles, relators/postpositions, broad TAM / aspect / modal, clause linkage, noun domain, and stem alternation all have fuller upstream report or dossier coverage than the current PDF prose now exposes.
2. **Which print slices are too cursory for a homogeneous grammar PDF?** Numerals, quantifiers, coordinators, sentence-final particles, relators/postpositions, TAM, directionals, prefix/agreement, NP structure / possession, noun domain, reduplication, clause linkage, nominalization, VP structure / suffix stacking, derivation / valency, and transitivity remain narrow slices rather than chapter-normalized sections.
3. **Which topics have too few examples or no real examples?** Many mid-grammar sections still have zero formal interlinear example blocks in the current print slice: relators/postpositions, TAM, stem alternation, prefix/agreement, NP structure / possession, noun domain, transitivity, VP structure / suffix stacking, derivation / valency, nominalization, clause linkage, and reduplication.
4. **Which topics draw too heavily on Genesis or early Old Testament material?** Demonstratives, pronouns, and negation are currently Old Testament-heavy in the assembled preview, and several other slices still fail to surface enough source metadata to show balance clearly. The current preview should not become a grammar of Genesis.
5. **Which topics need tables or paradigms to look like real grammar sections?** Numerals, pronouns, stem alternation, prefix/agreement, TAM, directionals, clause linkage, noun domain, NP structure / possession, and verb paradigms all need explicit tables or paradigms if they are to look like normalized publication-facing grammar sections.
6. **Which topics are genuinely blocked or theory-heavy and should stay as gaps?** Phonology/tone and verb paradigms should stay as explicit major gaps for now. Switch reference, relative clauses, broad possession theory, and whole-system valency classes also remain theory-heavy or boundary-heavy enough that they should not be forced into premature full prose.
7. **Which topic should be expanded first as a pilot?** Numerals is the best first pilot expansion target. It already has candidate, dossier, grammar, dictionary, and review-note layers; its upstream report is much fuller than the current print slice; and its current thinness is mainly an editorial underdevelopment problem rather than a blocked-evidence problem.

# Chapter-by-chapter diagnosis

## Chapter 1: phonology and tone

The assembled preview is correct to keep phonology/tone visible as a major unresolved domain. `docs/SKELETON_GRAMMAR.md` and `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md` show that the project has literature-backed material here, but the publication-review layer still does not have a packetized print slice comparable to the nominal, verbal, or discourse-facing packets.

This should remain a gap in the review preview. It is a real chapter-scale omission, not a cosmetic defect, and it is too theory-heavy to normalize opportunistically inside the current commit series.

## Chapter 2: deixis, pronouns, and nominal domain

Demonstratives and pronouns are among the stronger review-preview sections, but they still rely heavily on Old Testament examples and would benefit from a more explicit chapter-scale standard for source balance and paradigm presentation.

The biggest chapter-2 normalization problems are NP structure / possession, noun domain, numerals, quantifiers, and relators/postpositions:

- NP structure / possession currently advances one safe NP-ordering claim, not a real possession chapter.
- Noun domain currently advances one safe simple-noun claim, not a real noun chapter.
- Numerals has the clearest case where the report layer is much fuller than the current slice.
- Quantifiers is a narrow packet that remains structurally thin and example-light.
- Relators/postpositions is analytically useful, but it still reads like a boundary-controlled first packet rather than a normalized grammar section.

Case marking is closer to the current editorial model than the other nominal-domain sections. It is not complete at book-chapter scale, but it is less urgent than numerals, noun domain, or NP structure / possession.

## Chapter 3: predicate structure and verbal morphology

This is the most uneven chapter in the assembled preview.

Stem alternation has the richest upstream scaffolding, but the current grammar slice is still explicitly a draft argument plan. It already says that the eventual grammar should have a small core showcase table, a larger promoted-pair inventory table, a pair-by-pair discussion section, a one-sided or same-form coverage table, and a blocked/analyzer-noise table or appendix paragraph. That is exactly the kind of fuller normalization standard the PDF still lacks.

Prefix/agreement, transitivity, VP structure / suffix stacking, TAM, directionals, derivation / valency, nominalization, and clause linkage are all useful first packets, but most remain narrow anchor-led sections with limited formal example presentation and no chapter-scale paradigms.

Verb paradigms remain a major unresolved domain. The preview is right to keep that gap visible rather than pretending that the existing narrow packets already add up to a full verbal morphology chapter.

## Chapter 4: clause type, discourse-facing material, and expressive morphology

Negation and interrogatives are closer to medium-draft review-preview prose than the rest of chapter 4, though both would still benefit from more source-balanced example selection.

Sentence-final particles, coordinators, and reduplication still read as narrow first packets rather than normalized grammar sections:

- sentence-final particles remains overlap-heavy with TAM and clause type;
- coordinators is currently led by a narrow conjunction anchor rather than a broader coordination system;
- reduplication is still a narrow intensifier-led slice, not a fuller derivational or expressive chapter.

Broader discourse should remain an explicit gap. The current preview is correct to keep it visibly unfinished instead of filling it with thin placeholder prose.

# Homogeneous target standard for normalized publication-facing sections

For each already packetized grammar topic, a normalized publication-facing section should usually include:

- a short overview of the category or construction;
- an inventory table or paradigm where appropriate;
- a discussion of form and function;
- at least two good interlinear examples where the construction is common enough;
- balanced example sourcing where possible;
- an explicit boundary/deferred-material paragraph;
- citations to the main literature where available;
- no stale claims about packets not existing when they now exist;
- no raw generated-report counts promoted without candidate control.

This is the homogeneous target standard for normalized publication-facing sections. The point is not to erase the packet history. The point is to convert chapter prose from narrow packet status reports into grammar-facing sections that still preserve the packet layer's caution and evidence control.

# Example selection policy

The first criterion is how well the example illustrates the grammatical point. The second criterion is source balance.

Where there are many good examples of a construction, prefer at least one Old Testament example and one Gospel example.

Do not let the grammar become a grammar of Genesis simply because Genesis supplies many early and easy hits.

Do not force an Old Testament/Gospel pair if the best example is elsewhere or the construction is rare.

Acts, Pauline letters, Catholic epistles, and Revelation are acceptable when they provide the clearest evidence.

The candidate/example extraction machinery should record book, chapter, verse, broad source zone, and example-quality notes.

The broad Bible source zones for this workflow are:

- Old Testament
- Gospels
- Acts
- Pauline letters
- Catholic epistles
- Revelation

When these zones are assigned in extraction or assembly tooling, they should use the existing book-number mapping in `scripts/interlinear_latex.py` rather than a divergent Bible-book mapping.

# Cross-cutting normalization findings

## Fuller upstream evidence than the current print slices show

The clearest cases are:

- **Numerals:** `docs/grammar/reports/06-func-03-numerals.md` already describes digits, tens/hundreds/thousands, compound formation, ordinals, classifiers, numeral syntax, distributive and multiplicative expressions, and large-number contexts.
- **Stem alternation:** the current grammar slice is explicitly an argument plan for a fuller section with multiple tables and contrastive subsections.
- **Clause linkage:** the reports already span subordination, switch reference, and relative clauses, while the current print slice only lifts `ciangin` as the safe first anchor and keeps the rest secondary.
- **Noun domain / NP structure / possession:** the current slices only lift small safe claims even though the report and literature layers cover much broader noun and NP structure.
- **TAM, directionals, sentence-final particles, coordinators, relators/postpositions, and quantifiers:** each has a real packet, but each current slice deliberately suppresses wider system coverage.

## Sections that are too cursory or example-light

The most obvious example-light sections are the ones whose print slices still have zero formal interlinear example blocks: relators/postpositions, TAM, stem alternation, prefix/agreement, NP structure / possession, noun domain, transitivity, VP structure / suffix stacking, derivation / valency, nominalization, clause linkage, and reduplication.

That does not make those packets worthless. It does mean the current PDF still mixes true section prose with packet-stage summary prose. Coverage normalization should bring more of those sections to the point where at least two interlinear examples and one visible organizing table are normal rather than exceptional.

## Sections that need tables or paradigms

The most urgent table/paradigm needs are:

- numerals: base inventory plus decimal composition and ordinals;
- stem alternation: core showcase table, promoted-pair table, and a blocked/noise table;
- prefix/agreement: host-type routing table and later a cautiously bounded paradigm table;
- pronouns / clusivity: a more final-looking paradigm table with explicit clusivity caution;
- TAM: compact suffix inventory table tied to narrow anchors;
- directionals: a controlled directional inventory table that distinguishes promoted anchors from deferred rows;
- clause linkage: a small anchor table separating temporal subordination, switch-reference evidence, and relative-clause evidence;
- noun domain and NP structure / possession: a compact modifier-order / possession paradigm;
- verb paradigms: still missing as a major gap and should remain visibly missing.

## Stale packet-state prose that normalization should remove

Several grammar slices still say things such as "Dictionary and review-note slices have not yet begun" even though later packet surfaces now exist. This is an editorial normalization problem, not a linguistic problem. A normalized publication-facing section should not keep stale packet-state prose once the packet has moved on.

# Numerals as a worked diagnostic case

Numerals is the clearest worked example of the difference between packet completion and chapter normalization.

The relevant layers are:

- `docs/grammar/reports/06-func-03-numerals.md`
- `output/publication_review/candidates_numerals.tsv`
- `output/publication_review/dossier_numerals.md`
- `output/publication_review/grammar_numerals_print_slice.md`
- `output/publication_review/review_notes_numerals.md`
- `output/publication_review/assembled_grammar_review_preview.md`

The numerals report is fuller than the current print slice. The report already includes digits, tens/hundreds/thousands, compound formation, ordinals, classifiers, numeral syntax, distributive and multiplicative expressions, and large-number contexts.

By contrast, `grammar_numerals_print_slice.md` deliberately lifts only a small candidate-backed subset: two basic counting phrases, one compound-ten example, one ordinal, one occurrence-counting form, one large-number phrase with caveats, and explicit `kua`/`khat` controls.

The current numerals PDF section is mainly an underdeveloped print-slice problem, not an assembly problem.

That is exactly why numerals is the best first pilot for the new fuller standard. The packet already has real evidence control, but the publication-facing section still needs:

- a base numeral inventory table;
- decimal composition;
- ordinals;
- classifier/counting expressions, with caution;
- syntax of noun-plus-numeral and numeral-plus-noun patterns;
- multiplicative/occurrence-counting forms;
- distributive reduplication, if and only if candidate evidence supports it;
- large-number expressions with analyzer caveats;
- at least one Old Testament example and one Gospel example where suitable examples exist.

Numerals is therefore the recommended pilot expansion target for coverage normalization.

# Recommended normalization sequence

1. **Pilot first:** numerals.
2. **Second wave after the pilot model is proven:** quantifiers, coordinators, sentence-final particles, noun domain, and NP structure / possession.
3. **Third wave:** stem alternation, prefix/agreement, TAM, directionals, clause linkage, nominalization, derivation / valency, VP structure / suffix stacking, and transitivity.
4. **Hold as visible gaps unless explicitly re-scoped:** phonology/tone, verb paradigms, broader discourse, and the theory-heavier switch-reference/relative-clause problem space.

# Audit table

| Grammar topic | Current PDF section | Upstream source reports/lit reviews | Candidate/dossier layer exists? | Grammar print slice exists? | Review notes exist? | Number of examples in current print slice | Bible source distribution of examples | Has table/paradigm? | Current prose depth | Main reason section is thin | Expansion priority | Recommended next action |
|---|---|---|---|---|---|---:|---|---|---|---|---|---|
| Phonology / tone | Chapter 1: Phonology and tone | `GRAMMAR_SOURCE_INVENTORY.md`; phonology/tone lit reviews | No publication-review packet yet | No | No | 0 | gap only | No | placeholder/gap | literature exists but no packetized print layer | Blocked | keep visible as a major gap |
| Demonstratives / deixis | Chapter 2: Demonstratives / deixis | demonstratives report + lit review | Yes | Yes | Yes | 8 | assembled preview currently Old Testament-heavy | No | medium draft | usable packet, but source balance is narrow | Medium | later rebalance with at least one Gospel example if available |
| Pronouns / clusivity | Chapter 2: Pronouns / clusivity | pronouns report + lit review + clusivity dossier | Yes | Yes | Yes | 11 | assembled preview currently Old Testament-heavy | Yes | medium draft | needs a more final paradigm and wider source balance | Medium | normalize paradigm presentation after numerals pilot |
| NP structure / possession | Chapter 2: NP structure / possession | `03-noun-06-np-structure.md`; `04-np-07-possession.md`; possession lit review | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only first NP-ordering claim is lifted; possession remains boundary-heavy | High | expand to a real possession/NP subsection with a compact paradigm and examples |
| Noun domain | Chapter 2: Noun domain | `03-noun-01-simple.md`; `03-noun-02-compounds.md`; `03-noun-03-proper.md` | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only simple noun anchors are lifted; compounds/proper nouns remain deferred | High | expand after numerals with a simple-noun plus transparent-compound normalization pass |
| Case marking | Chapter 2: Case marking | case-marker morpheme file; postpositions report/lit review | Yes | Yes | Yes | 7 | assembled preview shows mostly Old Testament with at least one Gospel example | No | relatively developed draft | already the strongest editorial model, but still lacks a normalized chapter-scale table | Low | keep stable; reuse as normalization model |
| Relators / postpositions | Chapter 2: Relators / postpositions | `03-noun-04-relators.md`; `03-noun-05-postpositions.md`; postpositions lit review | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | boundary-controlled prose still outweighs chapter-level exposition | High | add a relator inventory table and two good interlinear examples later |
| Numerals | Chapter 2: Numerals | `docs/grammar/reports/06-func-03-numerals.md` | Yes | Yes | Yes | 7 | current slice under-surfaces sources; assembled preview already skews Old Testament | No | narrow slice | report is much fuller than slice; current section is intentionally tiny | Pilot | make this the first fuller normalized chapter section |
| Quantifiers | Chapter 2: Quantifiers | quantifiers report | Yes | Yes | Yes | 8 | current slice largely does not surface source balance cleanly | No | narrow slice | packet remains controlled but too small for a chapter-like section | High | second-wave expansion with better example balance and a compact inventory table |
| Stem alternation | Chapter 3: Stem alternation | stem reports + stem lit review + matrix/inventory files | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | sketch | current slice is still an argument plan, not normalized prose | High | turn the existing plan into core showcase, promoted-pair, and blocked/noise tables |
| Verb paradigms | Chapter 3: Verb paradigms | skeleton grammar; source inventory; report layer | No publication-review packet yet | No | No | 0 | gap only | No | placeholder/gap | major unresolved morphology domain still lacks packetization | Blocked | keep visible as a major gap |
| Prefix / agreement | Chapter 3: Prefix / agreement | agreement report; possession report; prefixes morpheme file | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only host-type routing contrast is lifted | High | build a compact routing table and add review-grade examples later |
| Transitivity | Chapter 3: Transitivity | `05-verb-12-transitivity.md` | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | clean anchors exist, but the chapter still reads like a packet summary | Medium | add two or more interlinear contrasts and a small argument-structure table later |
| VP structure / suffix stacking | Chapter 3: VP structure / suffix stacking | VP/combinations reports; `tests/test_vp_slots.py` | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | single anchor `bawlzoding` cannot carry a full chapter feel | Medium | later add a minimal stack-order table and one or two extra controlled examples |
| TAM / aspect / modal | Chapter 3: TAM / aspect / modal | TAM/aspect/modal reports + aspect lit review | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | many categories exist upstream, but current slice only surfaces compact anchors | High | add a compact suffix inventory table and balanced examples after numerals pilot |
| Directionals | Chapter 3: Directionals | directional report + lit review | Yes | Yes | Yes | 8 | current slice largely does not surface source balance cleanly; assembled preview is still mostly Old Testament-backed | No | narrow slice | good packet, but still anchor-led and table-less | Medium | add a controlled promoted-vs-deferred directional table |
| Derivation / valency | Chapter 3: Derivation / valency | derivational and valency reports; derivational morpheme file; valency lit review | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only `-sak` split is normalized; broader derivation remains deferred | Medium | later add a small `-sak` contrast table before any broader expansion |
| Nominalization | Chapter 3: Nominalization | `07-nmlz-01-deverbal.md`; derivational morpheme file | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only first safe `-na` claim is lifted | Medium | add two examples and a compact nominalization-function table later |
| Clause linkage | Chapter 3: Clause linkage | subordination, switch-reference, and relatives reports; subordination lit review | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | only `ciangin` is lifted; switch reference and relatives remain backgrounded | High | later split normalization into temporal subordination plus boundary table |
| Negation | Chapter 4: Negation | negation report + lit review | Yes | Yes | Yes | 5 | assembled preview currently Old Testament-heavy | No | medium draft | stronger than most chapter-4 slices, but still needs source rebalance | Medium | keep stable until a source-balance pass |
| Interrogatives | Chapter 4: Interrogatives | interrogatives report + lit review | Yes | Yes | Yes | 4 | current slice does not yet surface balance clearly | No | medium draft | usable packet but still light on explicit distribution and source balance | Medium | add one Gospel or Acts example when available |
| Sentence-final particles | Chapter 4: Sentence-final particles | sentence-final report + lit review | Yes | Yes | Yes | 5 | current slice partly surfaces Old Testament examples but remains imbalance-prone | No | narrow slice | overlap-heavy and still organized as a cautious first packet | High | later add a small function table plus better-balanced examples |
| Coordinators | Chapter 4: Coordinators | coordinators report | Yes | Yes | Yes | 5 | current slice only partly surfaces source balance; assembled preview is still OT-leaning | No | narrow slice | narrow `le`-led anchor does not yet read like a chapter | High | second-wave expansion with NP vs clause coordination table |
| Reduplication | Chapter 4: Reduplication | `07-deriv-02-reduplication.md` | Yes | Yes | Yes | 0 | source balance not yet visible in formal blocks | No | narrow slice | currently limited to intensifier-led first claim | Medium | later add intensifier vs distributive table and more examples if evidence allows |

# End state

This audit does not claim that the grammar is finished. It defines the next editorial problem more precisely: the repository has enough packeted material to assemble a useful review preview, but it still needs a coverage normalization pass so the already packetized topics read like a more homogeneous grammar rather than a mixture of strong sections, narrow slices, and explicit gaps.
