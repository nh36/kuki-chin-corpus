---
title: "Verb paradigms report-alignment diagnostic"
---

# Diagnostic question

Does the current `Verb paradigms` section represent the report-backed paradigm system as a whole, or is it more accurately a finite-predicate-frame first slice inside a broader unresolved paradigm domain?

# 1) What the paradigm-table report actually contains

The paradigm-table report (`docs/grammar/reports/05-verb-00-paradigm-tables.md`) is a mixed discovery surface, not a directly print-safe grammar layer.

| Report component | What it contains | Alignment consequence |
| --- | --- | --- |
| Actual paradigm tables | Repeating TAM / pronominal / voice-valency / nominalization tables for `om`, `pai`, `ci`, `gen`, `nei`, `mu`, `bawl`, `pia`, `za`, `lut` with first citations | Useful for scoping domains, but each row still needs candidate-level review before promotion |
| Corpus-backed rows | Many rows with real verse citations and plausible segmentations | Candidate-backed rows can be promoted when clause-level evidence is clean |
| Generated or artifact-prone rows | Table rows such as `ka pai -> kap-ai -> weep-persecute`, `a pai -> ap-ai -> press-persecute`, `ka mu -> kam-u -> mouth-elder.sibling`, and `ka lut -> kal-ut -> middle-will` | These are report-table artifacts and must remain blocked/deferred |
| Person-marking claims | `docs/grammar/reports/05-verb-03-agreement.md` includes full `pai` paradigms with `0x` attestations (for example `i-pai`, `ka-pai-uh`) | Report-table-only paradigms are not promoted without independent candidate/corpus support |
| TAM/negation/modal rows | `docs/grammar/reports/05-verb-04-tam.md` and `docs/grammar/reports/05-verb-07-modal.md` include stacked rows and `-pah/-pak/-lawh` NEG.ABIL variants | Keep as boundary or analyzer-gap material in this slice |
| Stem alternation rows | Form I/Form II material (`mu/muh`, `nei/neih`) overlaps `docs/grammar/reports/05-verb-01-stems.md` | Keep finite-frame section narrow; do not reopen full stem system here |
| Object-prefix/inverse-like rows | `kong-/hong-` rows appear in paradigm and agreement reports | Keep under boundary control; core analysis remains in hong/kong packet |
| Analyzer-gap/unresolved rows | `docs/grammar/ANALYZER_LITERATURE_GAPS.md` marks unresolved conditioning for `-pah/-pak/-lawh` | Explicitly blocked until conditioning is resolved |

# 2) What is candidate-backed in the current slice

## Promoted and supporting rows

| Candidate form | Source reference | Corpus/report status | Person configuration | Finite-frame shape | TAM/negation profile | Stem-form status | What it proves now |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ka nei hi` | Genesis 21:7 | corpus-backed | 1SG subject | person-marked predicate + clause-final `hi` | declarative `hi` | nonalternating Form I | finite-frame diagnostic anchor |
| `a en uh hi` | Matthew 27:36 | corpus-backed | 3SG + plural `uh` | finite predicate + `uh` + clause-final `hi` | declarative `hi` | no stem claim | finite-frame diagnostic anchor with plural caveat |
| `na si ding hi` | Genesis 2:17 | corpus-backed | 2SG subject | person-marked predicate + `ding` + `hi` | irrealis + declarative | no stem claim | person-marking diagnostic; also TAM boundary |
| `a suak hi` | Genesis 26:13 | corpus-backed | 3SG subject | person-marked finite predicate + `hi` | declarative `hi` | no stem claim | person-marking diagnostic |
| `ka nei kei hi` | John 4:17 | corpus-backed | 1SG subject | person-marked finite predicate + negation + `hi` | negation + declarative | no stem claim | person-marking diagnostic; also negation boundary |
| `nei / neih` | Genesis 11:30; 2 Samuel 23:8 | corpus-backed | variable | finite plus derived environments | mixed | Form I/Form II family | paradigm-supporting only, not a full stem claim |

## Boundary, blocked, and report-table-only rows

| Candidate form | Source reference | Corpus/report status | Current diagnostic status | Why not promoted as core finite evidence |
| --- | --- | --- | --- | --- |
| `ta nei lo hi` | Genesis 11:30 | corpus-backed | negation_boundary | belongs primarily to negation section |
| `lutthei ding uh hi` | Matthew 7:21 | corpus-backed | tam_boundary | belongs primarily to TAM/modal stacking section |
| `mu`; `muh` | Genesis 6:8; Matthew 2:10 | corpus-backed | stem_alternation_boundary | belongs primarily to Form I/Form II treatment |
| `hong bia`; `kong koih` | Matthew 4:9; Genesis 41:41 | corpus-backed | object_prefix_boundary | belongs primarily to hong/kong analysis |
| `i pai` | agreement report table | report-table-only | report_table_only | `0x` paradigm row; not independently candidate-backed |
| `ka pai` (`kap-ai` artifact) | paradigm-table report | report-table-only | lexicalized_or_unclear | segmentation/gloss artifact in report row |
| `-pah/-pak/-lawh` | analyzer-gap + modal reports | analyzer-gap-blocked | analyzer_gap_blocked | conditioning unresolved |

# 3) Does the packet overstate “verb paradigms”?

Yes, if read as a fuller paradigm slice. The safe framing is:

- **Verb paradigms section title retained**, but
- **content interpreted as a finite-predicate-frame and person-marked-predicate first slice**, not a full paradigm account.

This keeps the file naming stable while making claims accurate.

# 4) Check of current promoted examples

| Example | What it proves | Keep promoted? | Segmentation/gloss consistency | Context load |
| --- | --- | --- | --- | --- |
| Genesis 21:7 `ka nei hi` | 1SG-marked finite predicate frame with clause-final `hi` | yes, with caveat | consistent with prefix/agreement (`ka-`) and finite-frame segmentation (`ka-nei`) | clause is longer, but predicate frame remains clear |
| Matthew 27:36 `a en uh hi` | finite frame with `a` + predicate + plural `uh` + `hi` | yes, with caveat | consistent with agreement/TAM boundary treatment for `uh` | low context load; clean anchor |
| Genesis 2:17 `na si ding hi` | 2SG-marked finite predicate with irrealis + `hi` | yes, with TAM boundary caveat | consistent with TAM section treatment of `ding` | moderate context load; finite frame still clear |
| Genesis 26:13 `a suak hi` | compact 3SG finite predicate frame | yes | consistent with person-prefix segmentation and simple glossing | low context load |
| John 4:17 `ka nei kei hi` | 1SG-marked finite predicate with overt negation + `hi` | yes, with negation caveat | consistent with negation overlap (`kei`) and segmented analysis (`ka-nei`) | quote context present but predicate frame is explicit |

# 5) Orthography versus segmentation

The stabilized convention for this slice is:

- use **surface orthography** in inventory and running prose (`ka nei hi`, `ka nei kei hi`, `hong bia`, `kong koih`);
- use **segmented analysis** in segmentation tiers or explicit parse fields (`ka-nei`, `ka-nei-kei`, `hong-bia`, `kong-koih`).

This distinction is now synchronized across the grammar slice, candidate TSV, and dossier.

# 6) Role of `hi` in this slice

`Hi` is treated here as a **clause-final declarative element present in selected finite frames**. It is not used as an independent proof of the whole sentence-final-particle system, and it is not claimed as a dedicated finite marker for all clause types. Detailed sentence-final analysis remains in the sentence-final particles and TAM/negation overlap sections.

# 7) Report-table artifacts that remain blocked or deferred

- `ka pai`/`a pai`-type report artifacts (`kap-ai`, `ap-ai`) remain non-promoted because segmentation/gloss output is unreliable.
- inclusive `i` rows such as `i-pai` remain report-table-only until corpus-backed candidate evidence is curated.
- `-pah / -pak / -lawh` remain analyzer-gap-blocked because conditioning is unresolved.
- conditioned negative-ability variants therefore remain outside grammar-facing promotion.

# 8) Diagnostic conclusion and packet updates

Current safe claim:

1. The section can safely claim **finite predicate frames plus person-marked finite anchors**.
2. It should be explicitly framed as a **finite-predicate-frame/person-marked-predicate first slice** within the broader verb-paradigm domain.
3. The five promoted examples remain promoted, with TAM/negation/plural caveats retained where relevant.
4. Report-table-only rows remain blocked or deferred and are not promoted.
5. Remaining fuller-paradigm work (full person-prefix grid, full TAM/negation integration, full stem alternation, full object-prefix integration, and unresolved analyzer-gap variants) is deferred to later dedicated treatment.

Implemented in this stabilization pass:

- candidate TSV now records explicit corpus vs report status (`evidence_status`) and includes `report_table_only` diagnostic labeling;
- dossier now includes report-alignment conclusions;
- grammar prose now frames the section as finite-frame/person-marked first slice and distinguishes surface forms from segmented analysis;
- review notes now target framing strength, `hi` scope, orthography/segmentation consistency, and report-table artifact filtering.
