# Publication-Review Evidence Protocol

## Purpose

This document defines the evidence workflow for future Tedim publication-review packets. The goal is to stop treating raw string searches and generated grammar reports as the first real evidence layer for print-facing grammar and dictionary work.

## Workflow shift

### Old / unsafe workflow

`raw Bible text -> raw string search or generated report -> dossier cleans false positives -> print slice`

This workflow is useful for discovery, but it pushes too much cleanup burden into the dossier stage. It also makes it too easy for raw string matches such as `hi` or apparent `hih ciangin` hits to enter the candidate pool before the analyzer has filtered obvious false friends.

### New / preferred workflow

`raw Bible text -> morphological analyzer/export -> analyzer-aware candidate extraction -> construction-level filtering -> dossier -> grammar/dictionary print slice`

This workflow requires publication-review work to start from analyzer-confirmed tokens and then move upward to constructional interpretation. Dossiers should interpret and evaluate already-filtered candidate evidence. They should not be the first place where raw-string noise is cleaned up.

## Evidence levels

### Level 0: Raw hit

- A string occurs in the Bible text.
- This is useful only as a discovery clue.
- It is not enough for print-facing grammar or dictionary prose.

### Level 1: Analyzer-confirmed token

- The token or morpheme is confirmed in analyzer output, with segmentation, gloss, lemma, POS, usage type, or function type.
- This should normally be the minimum threshold for a publication-review candidate.

### Level 2: Construction-confirmed example

- The surrounding context confirms the relevant grammatical construction.
- Example: `tua ciangin` functions as a discourse-temporal linker, not merely as raw adjacency of two strings.

### Level 3: Print-safe example

- The example has been manually checked in context.
- It has a verse reference.
- It is short enough to cite cleanly.
- It directly supports the grammatical claim being made.

## Required policy

1. Generated grammar reports are discovery and orientation layers, not final evidence authorities.
2. Raw regex searches are allowed only as secondary discovery tools or sanity checks.
3. Every future print slice should be based on analyzer-aware candidates.
4. Dossiers should evaluate filtered candidate evidence, not perform the first major cleanup of raw-string noise.
5. If analyzer output and raw search disagree, the discrepancy should be recorded and investigated rather than silently resolved by hand.

## Candidate files

Candidate files are the working evidence layer between analyzer export and the dossier.

- Location: `output/publication_review/candidates_<topic>.tsv`
- Examples:
  - `output/publication_review/candidates_demonstratives.tsv`
  - `output/publication_review/candidates_negation.tsv`
  - `output/publication_review/candidates_interrogatives.tsv`

Candidate files may include both accepted and rejected rows. Excluded or deferred rows are not noise; they document where raw discovery overgenerated or where analyzer-aware review blocked a tempting but unsafe example.

## Standard candidate-file schema

| Column | Meaning |
| --- | --- |
| `candidate_id` | Stable unique identifier for the row. |
| `topic` | Publication-review topic, e.g. `demonstratives`. |
| `construction_id` | Normalized construction or headword label. |
| `verse_id` | Numeric verse identifier from aligned/exported data. |
| `reference` | Human-readable verse reference. |
| `surface_span` | Actual Tedim surface span being evaluated. |
| `token_indices` | Comma-separated analyzer token indices for the selected span. |
| `segmentation_span` | Analyzer segmentation for the selected span. |
| `gloss_span` | Analyzer gloss span for the selected span. |
| `lemma_span` | Analyzer lemma span for the selected span. |
| `pos_span` | Analyzer POS span for the selected span. |
| `kjv` | English alignment used for quick review. |
| `candidate_status` | Current outcome for the row. |
| `confidence` | Confidence in the current classification. |
| `why_selected` | Why the row is worth keeping in the candidate file. |
| `why_excluded` | Why the row cannot currently support print prose, if applicable. |
| `manual_review_status` | Manual review state for the row. |
| `notes` | Freeform reviewer notes. |

### Candidate statuses

- `accepted`
- `excluded`
- `needs_review`
- `deferred`

### Confidence levels

- `high`
- `medium`
- `low`

### Manual review status

Suggested values:

- `unreviewed`
- `reviewed`
- `needs_followup`

## Extraction rules

1. Start from analyzer export when available. For Tedim, the primary source is `data/ctd_analysis/tokens.tsv`.
2. Use raw string search only as a fallback discovery clue, and mark that fallback explicitly in notes or exclusion fields.
3. Preserve analyzer-aware spans in the candidate row so later dossier work can cite actual token indices, segmentation, glossing, and POS information.
4. Promote examples to print prose only after they reach Level 3.

## Curated pilots and future automation

The current demonstratives extractor is curated and analyzer-validated. That is acceptable for publication-review work because print examples must still be manually reviewed even when candidate extraction is reproducible.

Future work may add more automatic discovery, but automatic discovery should never bypass the evidence levels defined above. The key guarantee is not full automation. It is that every promoted example has an explicit candidate row with analyzer-backed spans, review status, and a documented reason for acceptance, exclusion, or deferral.

## Pilot topic: demonstratives/deixis

The first pilot under this protocol is `output/publication_review/candidates_demonstratives.tsv`.

That file records:

- accepted analyzer-aware candidates for `hih`, `tua`, `hihte`, `tuate`, `hih bangin`, `tua bangin`, `tua ciangin`, and `tua ahih ciangin`;
- deferred handling of `hi`;
- exclusion of the old Genesis 6:22 `hih bangin` misread;
- exclusion of the old Genesis 18:10 `hih ciangin` claim;
- a flagged John 1:19 `hi` example showing why raw discovery cannot treat `hi` as a settled demonstrative headword.

The pilot establishes the rule for future topics: candidate extraction should happen before dossier prose, and the dossier should then explain what the candidate layer supports, rejects, or leaves unresolved.
