# Copilot instructions for Kuki-Chin

## Build, test, and lint commands

- **Python version:** CI runs on Python 3.11.
- **Rebuild the Tedim backend:** `make backend`
- **Sanity-check the backend:** `make backend-check`
- **Regenerate canonical metrics:** `make metrics`
- **Check docs against canonical metrics:** `make metrics-check`
- **Generate publication outputs:** `make dictionary-draft`, `make grammar-draft`, `make outputs`
- **Check generated outputs are internally consistent:** `make output-check` or `python3 scripts/check_output_consistency.py`
- **Full test suite:** `python3 -m pytest tests/ -v --tb=short`
- **Single test file:** `python3 -m pytest tests/test_backend.py -v`
- **Single test:** `python3 -m pytest tests/test_metrics.py::TestMetricsConsistency::test_no_metric_drift -q`
- **Lint/type-check:** no dedicated lint or type-check command is defined in `Makefile` or CI.
- **Important:** `README.md` still mentions `make test`, but the current repository runs tests with `pytest` directly.

## High-level architecture

This repository has a multi-language corpus/bootstrapping side and a Tedim-first publication pipeline.

1. Hand-authored linguistic knowledge lives mainly in `scripts/analyze_morphemes.py`, `scripts/morphology/`, and supporting docs under `docs/`.
2. Tedim analysis exports in `data/ctd_analysis/*.tsv` are the canonical intermediate layer. They are regenerated from the analyzer/export pipeline and then loaded into SQLite.
3. `scripts/backend.py migrate --tsv-dir data/ctd_analysis --db data/ctd_backend.db` builds the normalized backend described in `docs/BACKEND_SPEC.md`. Dictionary, metrics, lookup, and grammar generators read this DB rather than re-parsing TSVs.
4. Publication scripts write canonical artifacts under `output/`, especially `output/metrics/`, `output/dictionary/`, `output/grammar/`, and the editorial/publication dashboards.
5. CI exercises that Tedim pipeline in order: `make backend`, `make metrics`, `pytest`, `make metrics-check`, `make outputs`, and `python3 scripts/check_output_consistency.py`.
6. The broader repo also contains aligned Bible corpora, lexicons, and a bootstrap path for new languages (`scripts/bootstrap_language.py`), but the database/output pipeline is currently centered on Tedim (`ctd`).

## Key conventions

- Treat `data/ctd_analysis/*.tsv` as committed canonical intermediates and `data/ctd_backend.db` as a regenerable derived artifact. Do not hand-edit the database.
- Treat `output/metrics/ctd_metrics.json` as the canonical source for headline metrics. `README.md` and `PROGRESS.md` are supposed to be synced from it via `scripts/sync_docs_to_metrics.py`, not updated independently.
- Do not hand-edit stamped files under `output/`; regenerate them. `scripts/check_output_consistency.py` expects commit stamps in generated artifacts and flags mixed-stamp outputs.
- Preserve backend ID conventions from `docs/BACKEND_SPEC.md`: source IDs `BBCCCVVV`, wordform IDs are normalized forms, lemma IDs are citation forms, sense IDs are `lemma.n`, and morpheme IDs are `form.gloss.category`.
- Example ranking is semantic, not cosmetic: backend APIs and tests rely on `canonical > excellent > good > transparent > shortest > acceptable > auto > additional`.
- The `constructions` and `grammar_topics` layers are optional and may legitimately be empty; tests and metrics treat zero counts as acceptable.
- Many tests assume generated artifacts already exist. If backend or metrics tests skip because files are missing, rebuild with `make backend` and/or `make metrics` before debugging test logic.
