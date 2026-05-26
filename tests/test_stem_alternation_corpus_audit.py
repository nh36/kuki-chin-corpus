import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/publication_review/audit_stem_alternation_corpus.py"
CORPUS_AUDIT_PATH = ROOT / "output/publication_review/stem_alternation_corpus_audit.tsv"
ENV_SUMMARY_PATH = ROOT / "output/publication_review/stem_alternation_environment_summary.tsv"
PAIR_SUMMARY_PATH = ROOT / "output/publication_review/stem_alternation_pair_summary.tsv"

REQUIRED_CORPUS_COLUMNS = {
    "pair_id",
    "form_i",
    "form_ii",
    "attested_form",
    "stem_form",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss",
    "lemma",
    "pos",
    "stem_alternation",
    "prefix_chain",
    "suffix_chain",
    "usage_type",
    "function_type",
    "local_context",
    "kjv",
    "inferred_environment",
    "environment_confidence",
    "print_status",
    "notes",
}

REQUIRED_ENV_COLUMNS = {
    "pair_id",
    "form_i",
    "form_ii",
    "environment",
    "form_i_count",
    "form_ii_count",
    "total_count",
    "representative_references",
    "notes",
}


def load_tsv(path: Path):
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return set(reader.fieldnames or []), rows


def test_stem_alternation_corpus_audit_outputs_exist():
    assert SCRIPT_PATH.exists()
    assert CORPUS_AUDIT_PATH.exists()
    assert ENV_SUMMARY_PATH.exists()
    assert PAIR_SUMMARY_PATH.exists()


def test_stem_alternation_corpus_audit_has_required_columns_and_core_pairs():
    header, rows = load_tsv(CORPUS_AUDIT_PATH)
    pair_header, pair_rows = load_tsv(PAIR_SUMMARY_PATH)

    assert REQUIRED_CORPUS_COLUMNS <= header
    assert "pair_id" in pair_header

    pair_ids = {row["pair_id"] for row in pair_rows} | {row["pair_id"] for row in rows}
    for required in {"mu-muh", "ne-nek", "nei-neih", "za-zak", "pia-piak", "nusia-nusiat"}:
        assert required in pair_ids


def test_stem_alternation_environment_summary_has_required_buckets():
    header, rows = load_tsv(ENV_SUMMARY_PATH)

    assert REQUIRED_ENV_COLUMNS <= header
    environments = {row["environment"] for row in rows}

    assert "finite_main_or_matrix" in environments
    assert "nominalized_na" in environments
    assert environments & {"dependent_temporal_ciangin", "dependent_temporal_ni_in", "clause_linking_kipan"}


def test_stem_alternation_corpus_audit_keeps_noisy_forms_out_of_simple_promoted_evidence():
    _, rows = load_tsv(CORPUS_AUDIT_PATH)

    piangsak_rows = [row for row in rows if row["normalized_form"] == "piangsak"]
    assert piangsak_rows
    assert all(row["inferred_environment"] == "causative_or_derivational_sak" for row in piangsak_rows)
    assert all(row["print_status"] == "exclude_for_now" for row in piangsak_rows)

    ngaihsutna_rows = [row for row in rows if row["normalized_form"] == "ngaihsutna"]
    assert ngaihsutna_rows
    assert all(row["inferred_environment"] == "compound_or_lexicalized" for row in ngaihsutna_rows)
    assert all(row["print_status"] == "exclude_for_now" for row in ngaihsutna_rows)
