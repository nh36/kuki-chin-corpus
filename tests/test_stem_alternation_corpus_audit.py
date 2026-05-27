import csv
import importlib.util
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/publication_review/audit_stem_alternation_corpus.py"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
ENV_SUMMARY_PATH = ROOT / "output/publication_review/stem_alternation_environment_summary.tsv"
PAIR_SUMMARY_PATH = ROOT / "output/publication_review/stem_alternation_pair_summary.tsv"
EXAMPLE_MATRIX_PATH = ROOT / "output/publication_review/stem_alternation_example_matrix.tsv"
LEXICAL_INVENTORY_PATH = ROOT / "output/publication_review/stem_alternation_lexical_inventory.tsv"
PROMOTABLE_EXAMPLES_PATH = ROOT / "output/publication_review/stem_alternation_promotable_examples.tsv"

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

REQUIRED_PAIR_COLUMNS = {
    "pair_id",
    "form_i",
    "form_ii",
    "publication_status",
    "form_i_total",
    "form_ii_total",
    "notes",
}

REQUIRED_MATRIX_COLUMNS = {
    "pair_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "stem_side",
    "attested_form",
    "environment",
    "environment_count_for_side",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss_span",
    "lemma",
    "pos",
    "local_context",
    "kjv",
    "print_status",
    "selection_reason",
    "notes",
}

FALLBACK_ACCEPTED_CANDIDATE_ROW_KEYS = {
    ("mu-muh", "01001004", "8"),
    ("mu-muh", "01019019", "3"),
    ("ne-nek", "01002017", "12"),
    ("ne-nek", "01002017", "23"),
    ("nei-neih", "01011030", "5"),
    ("nei-neih", "10023008", "1"),
    ("pia-piak", "01003012", "8"),
    ("pia-piak", "01003012", "13"),
    ("za-zak", "01024052", "6"),
    ("nusia-nusiat", "05002014", "22"),
}


def load_tsv(path: Path):
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return set(reader.fieldnames or []), rows


def load_audit_module():
    spec = importlib.util.spec_from_file_location("stem_audit_module", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_stem_alternation_corpus_audit_outputs_exist():
    assert SCRIPT_PATH.exists()
    assert ENV_SUMMARY_PATH.exists()
    assert PAIR_SUMMARY_PATH.exists()
    assert EXAMPLE_MATRIX_PATH.exists()
    assert LEXICAL_INVENTORY_PATH.exists()
    assert PROMOTABLE_EXAMPLES_PATH.exists()


def test_stem_alternation_example_matrix_has_required_columns_and_core_pairs():
    pair_header, pair_rows = load_tsv(PAIR_SUMMARY_PATH)
    matrix_header, matrix_rows = load_tsv(EXAMPLE_MATRIX_PATH)

    assert REQUIRED_PAIR_COLUMNS <= pair_header
    assert REQUIRED_MATRIX_COLUMNS <= matrix_header

    pair_ids = {row["pair_id"] for row in pair_rows} | {row["pair_id"] for row in matrix_rows}
    for required in {"mu-muh", "ne-nek", "nei-neih", "pia-piak", "za-zak", "nusia-nusiat"}:
        assert required in pair_ids


def test_stem_alternation_example_matrix_keeps_form_i_and_form_ii_for_core_pairs():
    _, rows = load_tsv(EXAMPLE_MATRIX_PATH)

    for pair_id in {"mu-muh", "ne-nek", "nei-neih"}:
        sides = {row["stem_side"] for row in rows if row["pair_id"] == pair_id}
        assert {"form_i", "form_ii"} <= sides


def test_stem_alternation_example_matrix_has_at_most_one_row_per_pair_side_environment():
    _, rows = load_tsv(EXAMPLE_MATRIX_PATH)

    seen = set()
    for row in rows:
        key = (row["pair_id"], row["stem_side"], row["environment"])
        assert key not in seen
        seen.add(key)


def test_stem_alternation_environment_summary_and_matrix_have_required_buckets():
    env_header, env_rows = load_tsv(ENV_SUMMARY_PATH)
    _, matrix_rows = load_tsv(EXAMPLE_MATRIX_PATH)

    assert REQUIRED_ENV_COLUMNS <= env_header
    environments = {row["environment"] for row in env_rows} | {row["environment"] for row in matrix_rows}

    assert "finite_main_or_matrix" in environments
    assert "nominalized_na" in environments
    assert "negative_clause" in environments
    assert environments & {"dependent_temporal_ciangin", "dependent_temporal_ni_in", "clause_linking_kipan"}


def test_stem_alternation_example_matrix_never_promotes_review_or_excluded_environments():
    _, rows = load_tsv(EXAMPLE_MATRIX_PATH)

    unknown_rows = [row for row in rows if row["environment"] == "unknown_or_needs_review"]
    assert unknown_rows
    assert all(row["print_status"] == "needs_analyzer_review" for row in unknown_rows)

    for blocked_environment in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        blocked_rows = [row for row in rows if row["environment"] == blocked_environment]
        assert blocked_rows
        assert all(row["print_status"] == "exclude_for_now" for row in blocked_rows)


def test_stem_alternation_promoted_matrix_rows_are_exact_candidate_rows_or_manual_allowlist():
    module = load_audit_module()
    _, rows = load_tsv(EXAMPLE_MATRIX_PATH)

    if TOKENS_PATH.exists():
        accepted_candidate_row_keys = module.load_accepted_candidate_row_keys(module.build_pair_inventory())
    else:
        accepted_candidate_row_keys = FALLBACK_ACCEPTED_CANDIDATE_ROW_KEYS

    manual_allowlist = set(module.MANUAL_REVIEW_ROW_ALLOWLIST)
    noisy_forms = {"piangsak", "ngaihsutna", "ngaihsun", "honkhiat", "honkhia", "hu", "huh", "luimu", "muhdah"}

    for row in rows:
        row_key = (row["pair_id"], row["verse_id"], row["token_index"])
        if row["print_status"] == "print_ready":
            assert row_key in accepted_candidate_row_keys

        if row["print_status"] == "print_usable_with_caveat":
            assert row_key in accepted_candidate_row_keys or row_key in manual_allowlist
            assert row["environment"] not in {"unknown_or_needs_review", "causative_or_derivational_sak", "compound_or_lexicalized"}
            assert row["normalized_form"] not in noisy_forms


def test_stem_alternation_example_matrix_keeps_noisy_families_out_of_clean_print_ready_evidence():
    _, pair_rows = load_tsv(PAIR_SUMMARY_PATH)
    _, matrix_rows = load_tsv(EXAMPLE_MATRIX_PATH)
    pair_map = {row["pair_id"]: row for row in pair_rows}

    assert pair_map["ngai-ngaih"]["publication_status"] in {"dossier_only", "needs_analyzer_review"}
    assert pair_map["ngai-ngaih"]["publication_status"] != "print_ready"
    assert pair_map["honkhia-honkhiat"]["publication_status"] == "exclude_for_now"
    assert pair_map["hu-huh"]["publication_status"] == "exclude_for_now"

    ngai_rows = [row for row in matrix_rows if row["pair_id"] == "ngai-ngaih"]
    assert ngai_rows
    assert all(row["print_status"] != "print_ready" for row in ngai_rows)

    honkhia_rows = [row for row in matrix_rows if row["pair_id"] == "honkhia-honkhiat"]
    assert honkhia_rows
    assert all(row["print_status"] == "exclude_for_now" for row in honkhia_rows)

    hu_rows = [row for row in matrix_rows if row["pair_id"] == "hu-huh"]
    assert hu_rows
    assert all(row["print_status"] == "exclude_for_now" for row in hu_rows)

    assert not any(row["pair_id"] == "pia-piak" and row["normalized_form"] == "piangsak" for row in matrix_rows)
    piangsak_rows = [row for row in matrix_rows if row["normalized_form"] == "piangsak"]
    if piangsak_rows:
        assert all(row["pair_id"] == "piang-pian" for row in piangsak_rows)
        assert all(row["print_status"] == "exclude_for_now" for row in piangsak_rows)

    noisy_rows = [
        row for row in matrix_rows
        if row["normalized_form"] in {"ngaihsutna", "honkhiat", "piangsak"}
        or row["pair_id"] in {"honkhia-honkhiat", "hu-huh"}
    ]
    assert noisy_rows
    assert all(row["print_status"] in {"exclude_for_now", "dossier_only"} for row in noisy_rows)


def test_stem_alternation_example_matrix_is_reproducible_when_tokens_export_is_available(tmp_path, monkeypatch):
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; skipping local regeneration check")

    module = load_audit_module()
    monkeypatch.setattr(module, "OUTPUT_DIR", tmp_path)
    monkeypatch.setattr(module, "CORPUS_AUDIT_PATH", tmp_path / "stem_alternation_corpus_audit.tsv")
    monkeypatch.setattr(module, "ENV_SUMMARY_PATH", tmp_path / "stem_alternation_environment_summary.tsv")
    monkeypatch.setattr(module, "PAIR_SUMMARY_PATH", tmp_path / "stem_alternation_pair_summary.tsv")
    monkeypatch.setattr(module, "EXAMPLE_MATRIX_PATH", tmp_path / "stem_alternation_example_matrix.tsv")
    monkeypatch.setattr(module, "LEXICAL_INVENTORY_PATH", tmp_path / "stem_alternation_lexical_inventory.tsv")
    monkeypatch.setattr(module, "PROMOTABLE_EXAMPLES_PATH", tmp_path / "stem_alternation_promotable_examples.tsv")

    module.write_corpus_audit()

    assert (tmp_path / "stem_alternation_example_matrix.tsv").read_text(encoding="utf-8") == EXAMPLE_MATRIX_PATH.read_text(encoding="utf-8")
    assert (tmp_path / "stem_alternation_lexical_inventory.tsv").read_text(encoding="utf-8") == LEXICAL_INVENTORY_PATH.read_text(encoding="utf-8")
    assert (tmp_path / "stem_alternation_promotable_examples.tsv").read_text(encoding="utf-8") == PROMOTABLE_EXAMPLES_PATH.read_text(encoding="utf-8")
