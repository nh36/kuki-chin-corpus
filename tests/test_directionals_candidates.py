import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_directionals.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTEDISH = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "directional_type",
    "directional_form",
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


def rows_for(form: str) -> list[dict[str, str]]:
    return [row for row in load_rows() if row["directional_form"] == form]


def test_directionals_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"directionals"}


def test_directionals_candidate_file_keeps_khia_or_khiat_as_accepted_evidence() -> None:
    rows = load_rows()

    assert any(
        row["directional_form"] in {"khia", "khiat"}
        and row["candidate_status"] in ACCEPTEDISH
        for row in rows
    )


def test_directionals_candidate_file_keeps_toh_upward_and_comitative_overlap_explicit() -> None:
    toh_rows = rows_for("toh")

    assert toh_rows
    assert any(
        row["directional_type"] == "upward"
        and row["construction_type"] == "verb_toh_up"
        and row["candidate_status"] in ACCEPTEDISH | {"deferred"}
        for row in toh_rows
    )
    assert any(
        row["directional_type"] == "comitative_overlap"
        and row["construction_type"] == "toh_comitative_overlap"
        and row["candidate_status"] == "excluded"
        and ("accompany" in row["why_excluded"].lower() or "comitative" in row["notes"].lower())
        for row in toh_rows
    )


def test_directionals_candidate_file_keeps_lam_caveated_or_deferred() -> None:
    lam_rows = rows_for("lam")

    assert lam_rows
    assert all(
        row["construction_type"] == "lam_nominal_or_directional_boundary"
        or row["candidate_status"] == "deferred"
        for row in lam_rows
    )
    assert all(
        row["candidate_status"] != "accepted"
        for row in lam_rows
    )
    assert any(
        "boundary" in row["notes"].lower() or "manner" in row["why_excluded"].lower()
        for row in lam_rows
    )


def test_directionals_candidate_file_represents_sawn_lut_suk_phei_cip_and_tang_conservatively() -> None:
    for form in ("sawn", "lut", "suk", "phei", "cip", "tang"):
        form_rows = rows_for(form)
        assert form_rows, f"missing directionals row for {form}"

    assert any(
        row["directional_form"] == "sawn"
        and row["candidate_status"] in ACCEPTEDISH | {"deferred", "needs_review"}
        and ("toward" in row["notes"].lower() or "toward" in row["gloss_span"].lower())
        for row in rows_for("sawn")
    )
    assert any(
        row["directional_form"] == "suk"
        and row["candidate_status"] in ACCEPTEDISH
        and row["construction_type"] == "verb_suk_down"
        for row in rows_for("suk")
    )
    for form in ("lut", "phei", "cip", "tang"):
        assert all(
            row["candidate_status"] in {"deferred", "needs_review", "excluded"}
            for row in rows_for(form)
        )
        assert any(
            "defer" in row["notes"].lower()
            or "not yet" in row["notes"].lower()
            or "not yet" in row["why_excluded"].lower()
            or "not candidate-backed" in row["notes"].lower()
            for row in rows_for(form)
        )


def test_directionals_candidate_file_avoids_generated_report_raw_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in (
        "1,006",
        "180 for -khiat",
        "39 for -toh",
        "24 for -lam",
        "13 for -sawn",
        "0-count",
        "zero attestations",
        "zero-attestation",
    ):
        assert banned not in text


def test_directionals_extractor_is_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "directionals" in result.stdout.strip().splitlines()


def test_directionals_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_directionals.tsv"
    run_extractor("directionals", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")


def test_candidate_files_remain_lf_only() -> None:
    for path in sorted((ROOT / "output/publication_review").glob("candidates_*.tsv")):
        data = path.read_bytes()
        assert b"\r\n" not in data, f"{path} contains CRLF line endings"
        assert b"\r" not in data, f"{path} contains bare CR line endings"
