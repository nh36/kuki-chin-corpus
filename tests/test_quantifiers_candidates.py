import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_quantifiers.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTED_STATUSES = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "quantifier_type",
    "quantifier_form",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
}


def run_extractor(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def load_rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def matching_rows(*, form: str) -> list[dict[str, str]]:
    return [row for row in load_rows() if row["quantifier_form"] == form]


def test_quantifiers_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"quantifiers"}


def test_quantifiers_candidate_file_keeps_core_universal_and_existential_rows() -> None:
    rows = load_rows()
    accepted_rows = [row for row in rows if row["candidate_status"] in ACCEPTED_STATUSES]

    assert any(
        row["quantifier_type"] == "universal"
        and row["quantifier_form"] == "khempeuh"
        and row["candidate_status"] in ACCEPTED_STATUSES
        for row in accepted_rows
    )
    assert any(
        row["quantifier_type"] == "existential"
        and row["quantifier_form"] == "pawlkhat"
        and row["construction_type"] == "pawlkhat_partitive"
        for row in accepted_rows
    )


def test_quantifiers_candidate_file_keeps_khat_boundary_explicit() -> None:
    rows = matching_rows(form="khat")

    assert rows
    assert all(row["candidate_status"] != "accepted" for row in rows)
    assert all(row["quantifier_type"] == "numeral_indefinite_boundary" for row in rows)
    assert all("boundary" in row["notes"].lower() or "numeral" in row["notes"].lower() for row in rows)
    assert all(row["print_status"] in {"print_usable_with_caveat", "not_print_ready", "blocked"} for row in rows)


def test_quantifiers_candidate_file_keeps_kuamah_and_bangmah_overlap_controls() -> None:
    kuamah_rows = matching_rows(form="kuamah")
    bangmah_rows = matching_rows(form="bangmah")

    assert kuamah_rows
    assert bangmah_rows
    assert any(row["candidate_status"] in ACCEPTED_STATUSES for row in kuamah_rows)
    assert any("negation" in row["notes"].lower() for row in kuamah_rows if row["candidate_status"] in ACCEPTED_STATUSES)

    accepted_bangmah_rows = [row for row in bangmah_rows if row["candidate_status"] in ACCEPTED_STATUSES]
    assert accepted_bangmah_rows
    assert any(
        "negat" in row["notes"].lower() and ("interrogative" in row["notes"].lower() or "bang-family" in row["notes"].lower())
        for row in accepted_bangmah_rows
    )

    blocked_bangmah_rows = [
        row
        for row in bangmah_rows
        if row["construction_type"] == "interrogative_overlap_control"
    ]
    assert blocked_bangmah_rows
    assert all(row["candidate_status"] == "excluded" for row in blocked_bangmah_rows)
    assert all(row["print_status"] == "blocked" for row in blocked_bangmah_rows)


def test_quantifiers_candidate_file_keeps_degree_and_edge_rows_conservative() -> None:
    rows = load_rows()

    assert any(
        row["quantifier_type"] == "degree"
        and row["quantifier_form"] == "tampi"
        and row["candidate_status"] in ACCEPTED_STATUSES
        for row in rows
    )

    by_form = {
        "peuhpeuh": matching_rows(form="peuhpeuh"),
        "tawm": matching_rows(form="tawm"),
        "zaw": matching_rows(form="zaw"),
        "mahmah": matching_rows(form="mahmah"),
    }
    for form, form_rows in by_form.items():
        assert form_rows, f"missing quantifier control row for {form}"
        assert any(
            row["candidate_status"] in ACCEPTED_STATUSES | {"deferred", "needs_review"}
            for row in form_rows
        )

    assert all(
        row["candidate_status"] in {"deferred", "needs_review"}
        for row in by_form["peuhpeuh"] + by_form["tawm"]
    )
    assert all(
        row["print_status"] == "not_print_ready"
        for row in by_form["peuhpeuh"] + by_form["tawm"]
    )


def test_quantifiers_candidate_file_avoids_generated_report_raw_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("5,191", "4,712", "664", "525", "735", "1,351", "13,000+"):
        assert banned not in text


def test_quantifiers_extractor_lists_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "quantifiers" in result.stdout.strip().splitlines()


def test_quantifiers_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_quantifiers.tsv"
    run_extractor("quantifiers", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")


def test_candidate_files_remain_lf_only() -> None:
    for path in sorted((ROOT / "output/publication_review").glob("candidates_*.tsv")):
        data = path.read_bytes()
        assert b"\r\n" not in data, f"{path} contains CRLF line endings"
        assert b"\r" not in data, f"{path} contains bare CR line endings"
