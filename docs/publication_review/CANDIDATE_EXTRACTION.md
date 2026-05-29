# Candidate Extraction Workflow

## Purpose

`scripts/publication_review/extract_candidates.py` generates analyzer-aware publication-review candidate files. These files sit between raw analyzer export and dossier writing, so future print-facing grammar and dictionary work starts from explicit candidate rows rather than from raw string searches alone.

## Current support

Current supported extractor topics:

- `demonstratives`
- `negation`
- `pronouns`
- `stem_alternation`

The current demonstratives implementation is a curated pilot. Negation is the first hardened retrospective retrofit under the same candidate-first architecture, pronouns / clusivity is the second retrofit topic, and stem alternation is now the third retrofit topic. All four use curated, analyzer-validated candidate specs so publication-review work can start from explicit accepted, deferred, excluded, and needs-review rows.

Manual candidate layer without extractor support yet:

- `case_marking`

`output/publication_review/candidates_case_marking.tsv` now exists as a manually curated candidate layer, but do **not** treat `case_marking` as a supported extractor topic until the extractor route itself exists.

## Required input

The extractor currently requires:

- `data/ctd_analysis/tokens.tsv`

If that file is missing, regenerate it with:

```bash
python3 scripts/export_tedim_analysis.py
```

`data/ctd_analysis/tokens.tsv` is generated local build output and may be absent in a clean checkout. Candidate-extractor tests should therefore skip gracefully when it is absent or regenerate it locally; they should not require the file to be tracked in git.

## Running the extractor

List supported topics:

```bash
python3 scripts/publication_review/extract_candidates.py --list-topics
```

Regenerate the demonstratives candidate file:

```bash
python3 scripts/publication_review/extract_candidates.py demonstratives
```

Regenerate the negation candidate file:

```bash
python3 scripts/publication_review/extract_candidates.py negation
```

Regenerate the pronoun candidate file:

```bash
python3 scripts/publication_review/extract_candidates.py pronouns
```

Regenerate the stem alternation candidate file:

```bash
python3 scripts/publication_review/extract_candidates.py stem_alternation
```

Expected output:

- `output/publication_review/candidates_demonstratives.tsv`
- `output/publication_review/candidates_negation.tsv`
- `output/publication_review/candidates_pronouns.tsv`
- `output/publication_review/candidates_stem_alternation.tsv`

## Workflow position

Candidate files fit into the publication-review workflow like this:

`candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`

The candidate file is the evidence layer. The dossier interprets that evidence. Any later print-facing slice should promote only manually reviewed examples from the candidate layer.

Stem alternation now needs three linked output layers in addition to that curated candidate TSV:

1. **Full local row-level audit** — `output/publication_review/stem_alternation_corpus_audit.tsv`
   - generated from the local analyzer export;
   - intentionally untracked in git because it is too large for GitHub-friendly review;
   - useful when doing broad corpus analysis or regenerating compact derivatives.
2. **Tracked summary tables** — `output/publication_review/stem_alternation_environment_summary.tsv` and `output/publication_review/stem_alternation_pair_summary.tsv`
   - compact tracked summaries of pair totals and environment distributions.
3. **Tracked representative example matrix** — `output/publication_review/stem_alternation_example_matrix.tsv`
   - one representative example per verb pair × stem side × inferred environment;
   - intended to support interpretive review and eventual write-up.

In other words, stem alternation now has both:

1. a curated candidate layer for print-safe or explicitly blocked packet evidence; and
2. a broader corpus audit layer for mapping Form I / Form II distribution across environments, with tracked summaries and a tracked example matrix for GitHub review.

Case marking should begin differently. It is not a broad verb-pair distributional audit like stem alternation. The retrofit should start with a curated candidate TSV for markers such as `-in`, `-ah`, `-a`, `-pan`, `-panin`, `-tawh`, and relator-noun-plus-case constructions. Relator nouns should not be flattened into bare case suffixes in the candidate layer.

## What the current extractor does

For the current demonstratives, negation, pronoun, and stem-alternation layers, the extractor:

1. loads `data/ctd_analysis/tokens.tsv`;
2. looks up curated verse/token windows;
3. validates expected normalized forms for those windows;
4. writes accepted, deferred, and excluded candidate rows with analyzer-backed spans and review notes.

This means the current extractor is reproducible and inspectable, but intentionally conservative. It does not yet attempt broad automatic discovery across the corpus.

## How to add a future topic

A future topic should not be added until it has:

- a topic name;
- stable construction IDs;
- accepted, deferred, and excluded examples;
- analyzer-token windows for each candidate row;
- expected normalized forms for those windows;
- reasons for inclusion or exclusion;
- tests or documentation checks.

In practice, that means adding:

1. a `build_<topic>_specs()` function in `scripts/publication_review/extract_candidates.py`;
2. a route for that topic in `build_specs(topic)`;
3. a committed `output/publication_review/candidates_<topic>.tsv` file;
4. tests or documentation checks that confirm the committed file remains valid and reproducible.

## Why the current layers are curated

The first demonstratives implementation, the first negation retrofit, the first pronoun retrofit, and the first stem-alternation retrofit are intentionally curated because publication-review work needs explicit reviewable evidence rows more than it needs a broad automatic discovery engine. Future automation may expand candidate discovery, but publication-review examples must still be analyzer-backed, construction-checked, and manually reviewed before they reach print prose.
