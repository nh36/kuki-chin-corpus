# Candidate Extraction Workflow

## Purpose

`scripts/publication_review/extract_candidates.py` generates analyzer-aware publication-review candidate files. These files sit between raw analyzer export and dossier writing, so future print-facing grammar and dictionary work starts from explicit candidate rows rather than from raw string searches alone.

## Current support

Current supported topics:

- `demonstratives`
- `negation`

The current demonstratives implementation is a curated pilot, and negation is the first retrospective retrofit under the same candidate-first architecture. Both use curated, analyzer-validated candidate specs so publication-review work can start from explicit accepted, deferred, and excluded rows.

## Required input

The extractor currently requires:

- `data/ctd_analysis/tokens.tsv`

If that file is missing, regenerate it with:

```bash
python3 scripts/export_tedim_analysis.py
```

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

Expected output:

- `output/publication_review/candidates_demonstratives.tsv`
- `output/publication_review/candidates_negation.tsv`

## Workflow position

Candidate files fit into the publication-review workflow like this:

`candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`

The candidate file is the evidence layer. The dossier interprets that evidence. Any later print-facing slice should promote only manually reviewed examples from the candidate layer.

## What the current extractor does

For the current demonstratives and negation layers, the extractor:

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

The first demonstratives implementation and the first negation retrofit are intentionally curated because publication-review work needs explicit reviewable evidence rows more than it needs a broad automatic discovery engine. Future automation may expand candidate discovery, but publication-review examples must still be analyzer-backed, construction-checked, and manually reviewed before they reach print prose.
