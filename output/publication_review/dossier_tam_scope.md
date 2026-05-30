---
title: "Tedim TAM / Aspect / Modal Scoping Dossier"
---

# TAM / aspect / modal scoping dossier

## Scope and status

This is the first scoping and candidate pass for the TAM / aspect / modal packet. The controlling candidate layer now exists at `output/publication_review/candidates_tam.tsv`. The main discovery source for this first pass is `docs/grammar/reports/05-verb-04-tam.md`, while `tests/test_habitual_markers.py` and `tests/test_vp_slots.py` provide the cleanest existing analyzer-backed evidence for compact habitual, aspectual, modal, and VP-slot claims.

Nearby verb-domain material matters only as boundary control. `docs/grammar/reports/05-verb-06-directional.md` and `output/publication_review/review_notes_directionals.md` help show where TAM analysis would immediately spill into directionals or broad VP-slot prose if it is not kept narrow.

This dossier is therefore **not** a full TAM grammar slice. It is a conservative scoping document whose job is to identify a small curated candidate set, separate that set from overlap or deferred material, and define the safest next print-facing sub-scope. Grammar, dictionary, and review-note print slices for TAM have **not** yet begun.

## Evidence protocol

`candidates_tam.tsv` is the controlling evidence layer for the present analysis. Candidate rows, not generated-report raw counts and not a broad search over every TAM-looking suffix, control the dossier. The intended reading order is `candidates_tam.tsv` -> `dossier_tam_scope.md` -> any future narrow TAM grammar slice.

`docs/grammar/reports/05-verb-04-tam.md` is used here as a discovery source, not as finished print prose and not as authority for raw frequency claims. The first scoping pass therefore prefers explicit test-backed anchors such as `paingei`, `neigige`, `paizel`, `kilawmta`, `bawlzo`, `hongpaikik`, `omding`, and `bawlthei` over broad report-driven generalization.

## Core findings

The current scoping pass supports five narrow conclusions:

1. the cleanest current TAM candidates are compact analyzer-backed verb-plus-suffix anchors already covered by `tests/test_habitual_markers.py` and `tests/test_vp_slots.py`;
2. some report-visible forms, especially `dingin`, are real discovery clues but are too clause-bound for the safest first print-facing TAM slice;
3. `-thei` and `-ding` become noisy quickly when negation and irrealis stack together;
4. `-ta` and `-zo` require sentence-final overlap controls, and TAM stacking quickly runs into directionals or general VP-slot problems;
5. the safest next print-facing sub-scope is a narrow grammar slice limited to compact suffixal TAM anchors, not a full TAM chapter.

## Relatively clean TAM / aspect / modal candidates

The current candidate layer is strongest where the repository already has compact analyzer-backed tests:

- `paingei` -> `pai-ngei` -> `go-EXP`
- `neigige` -> `nei-gige` -> `have-HAB`
- `paizel` -> `pai-zel` -> `go-HAB.CONT`
- `kilawmta` -> `ki-lawm-ta` -> `REFL-worthy-PFV`
- `bawlzo` -> `bawl-zo` -> `make-COMPL`
- `hongpaikik` -> `hong-pai-kik` -> `3→1-go-ITER`
- `omding` -> `om-ding` -> `exist-IRR`
- `bawlthei` -> `bawl-thei` -> `make-ABIL`

These rows are safer than the broad report examples because they are compact, already regression-tested, and easier to interpret without importing generated-report counts. Even here the packet should stay construction-controlled. `Paizel` still borders broader continuative territory, `kilawmta` still needs sentence-final caution around `-ta`, and `bawlzo` must be kept distinct from bare `zo` boundary material.

## Construction-bound or clause-position candidates

The first scoping pass also needs to record forms that are visible but not yet safe as the first print-facing TAM anchors.

`Dingin` is the clearest example. `docs/grammar/reports/05-verb-04-tam.md` repeatedly highlights `ding-in -> IRR-ERG`, which shows that `-ding` is genuinely part of the discovery layer. But `dingin` is clause-bound material, not the safest first modal suffix anchor. `Omding` is therefore the better starting point for a later grammar slice.

`Pailai` also belongs here. `tests/test_vp_slots.py` keeps `pailai` visible as a possible prospective candidate, but the current analyzer output is `pai-lai -> go-midst`, not a clean unambiguous prospective reading. `-lai` should therefore stay deferred in the first slice.

The same caution applies to report-only summary items such as `-nawn` and `-khin`. `docs/grammar/reports/05-verb-04-tam.md` lists them in the overview, but this first scoping pass does not yet have equally clean anchors for them from the present evidence layer, so they should remain outside the first print-facing TAM sub-scope.

## Forms overlapping with negation

The report's `-thei` material shows immediately why the packet must stay narrow. `Khiathei ding om lo` bundles abilitative `-thei` with `ding` and `lo`, so it is useful as overlap control but not as the model for first-pass TAM prose.

That overlap matters methodologically. The repository already has a stabilized negation packet, so the TAM packet should not reopen negation by treating negative modal strings as if they were clean standalone TAM anchors. For the first print-facing TAM work, `bawlthei` is safer than `khiathei ding om lo` or similar negative-modal strings.

## Forms overlapping with sentence-final particles

`-ta` and `-zo` do not live in isolation. The existing sentence-final particles packet already keeps `mangngilh ta hi` visible as TAM-overlap boundary material, and it also keeps bare `zo` deferred as lexical or sentence-final boundary material rather than clean completive evidence.

Those cross-packet controls are important here because they explain why `kilawmta` and `bawlzo` can be usable only with constructional caveat. The first TAM slice should stay with compact suffixed verbs and should not drift into clause-final `ta hi`, bare `zo`, or sentence-final particle analysis.

## Forms overlapping with directionals or VP-slot material

`Khia-ta` is the clearest report-level reminder that TAM stacking quickly runs into directionals. The TAM report itself lists `khia-ta`, and the completed directionals packet already warns against reopening broad VP-slot prose through directional-looking material. `Khia-ta` should therefore stay an overlap control, not a first TAM anchor.

`Tests/test_vp_slots.py` also keeps broader stacking visible through forms such as `bawlzoding` and `bawlsakthei`. Those tests are valuable discovery evidence, but they show why the first TAM slice must stay compact. The current analyzer output for `bawlzoding` is noisy, and the causative-plus-modal stacks belong to a later interaction pass rather than to the first TAM grammar slice.

## Deferred or not yet safe

The current scoping pass should defer the following material from the first print-facing TAM slice:

- `pailai` as a prospective candidate still entangled with lexical `lai`;
- `dingin` and similar clause-bound `-ding` forms;
- negative modal strings such as `khiathei ding om lo`;
- sentence-final overlap material such as `mangngilh ta hi` and bare `zo`;
- directional or broader VP-slot stacks such as `khia-ta` and `bawlzoding`;
- report-summary items such as `-nawn` and `-khin` that do not yet have equally clean anchors in the current evidence layer.

The common pattern is the same across all of them: they are discovery-worthy, but they are not yet the safest first print-facing TAM evidence.

## Existing test-backed evidence

The repository already has useful evidence for a narrow TAM packet.

`tests/test_habitual_markers.py` directly supports:

- experiential `-ngei` through `paingei` and `muhngei`;
- habitual `-gige` through `neigige`;
- habitual continuative `-zel` through `paizel` and `kazel`.

`tests/test_vp_slots.py` directly supports:

- perfective `-ta` through `kilawmta`;
- completive `-zo` through `bawlzo`;
- iterative `-kik` through `hongpaikik`;
- irrealis `-ding` through `omding`;
- abilitative `-thei` through `bawlthei`;
- prospective-candidate `-lai` through `pailai`;
- broader VP-slot interactions through `bawlzoding` and `bawlsakthei`.

That means the first TAM packet does not need to start from the noisiest generated-report examples. It can start from the repository's own explicit test-backed anchors.

## Safest next print-facing sub-scope

The safest next print-facing sub-scope after this candidate layer is a narrow grammar slice limited to compact suffixal TAM anchors:

- experiential / habitual material: `-ngei`, `-gige`, `-zel`;
- compact aspectual material: `-ta`, `-zo`, `-kik`;
- compact modal material: `-ding`, `-thei`.

That future slice should keep `-lai`, `dingin`, negation-overlap strings, sentence-final overlap rows, directional overlaps, and TAM stacking out of scope. It should also stay candidate-first and should not try to turn `docs/grammar/reports/05-verb-04-tam.md` into a full TAM chapter in one pass.

## Not yet started

This commit does **not** complete a TAM grammar print slice, dictionary print slice, or review notes. `grammar_tam_print_slice.md`, `dictionary_tam_print_slice.md`, and `review_notes_tam.md` do **not** yet exist, and this dossier does not claim otherwise.
