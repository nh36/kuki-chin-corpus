import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_coordinators.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTEDISH = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "coordinator_type",
    "coordinator_form",
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
    return [row for row in load_rows() if row["coordinator_form"] == form]


def test_coordinators_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"coordinators"}


def test_coordinators_candidate_file_keeps_np_le_anchor() -> None:
    rows = load_rows()

    assert any(
        row["coordinator_type"] == "np_conjunction"
        and row["coordinator_form"] == "le"
        and row["construction_type"] == "np_le"
        and row["candidate_status"] in ACCEPTEDISH
        and "vantung" in row["surface_span"].lower()
        and "leitung" in row["surface_span"].lower()
        for row in rows
    )


def test_coordinators_candidate_file_keeps_leh_as_boundary_material() -> None:
    leh_rows = rows_for("leh")

    assert leh_rows
    assert any(
        row["construction_type"] == "conditional_leh"
        and row["candidate_status"] in {"accepted_with_caveat", "needs_review", "deferred"}
        and (
            "conditional" in row["why_selected"].lower()
            or "conditional" in row["why_excluded"].lower()
            or "boundary" in row["notes"].lower()
        )
        for row in leh_rows
    )


def test_coordinators_candidate_file_keeps_a_caveated_and_pairs_it_with_false_friend_control() -> None:
    a_rows = rows_for("a")

    assert a_rows
    assert any(
        row["construction_type"] == "sequential_a"
        and row["candidate_status"] in {"accepted_with_caveat", "needs_review", "deferred"}
        and (
            "3sg" in row["notes"].lower()
            or "func" in row["notes"].lower()
            or "caveat" in row["why_excluded"].lower()
        )
        for row in a_rows
    )
    assert any(
        row["construction_type"] == "agreement_a_false_friend"
        and row["candidate_status"] == "excluded"
        and row["print_status"] == "blocked"
        for row in a_rows
    )


def test_coordinators_candidate_file_keeps_mawh_and_ahih_material_conservative() -> None:
    mawh_rows = rows_for("mawh")
    ahih_hangin_rows = rows_for("ahih hangin")
    ahih_kei_leh_rows = rows_for("ahih kei leh")

    assert mawh_rows
    assert any(
        row["candidate_status"] in {"deferred", "needs_review"}
        and (
            "lexical" in row["why_excluded"].lower()
            or "alternative-question" in row["why_selected"].lower()
            or "disjunction" in row["why_selected"].lower()
        )
        for row in mawh_rows
    )

    assert ahih_hangin_rows
    assert any(
        row["coordinator_type"] == "adversative"
        and row["candidate_status"] in ACCEPTEDISH | {"deferred"}
        and (
            "hangin" in row["notes"].lower()
            or "adversative" in row["why_selected"].lower()
            or "adversative" in row["why_excluded"].lower()
        )
        for row in ahih_hangin_rows
    )

    assert ahih_kei_leh_rows
    assert any(
        row["coordinator_type"] == "conditional_adversative"
        and row["candidate_status"] in {"accepted_with_caveat", "needs_review", "deferred"}
        for row in ahih_kei_leh_rows
    )


def test_coordinators_candidate_file_includes_explicit_overlap_controls() -> None:
    rows = load_rows()

    assert any(
        row["construction_type"] in {"agreement_a_false_friend", "conditional_leh"}
        for row in rows
    )


def test_coordinators_candidate_file_avoids_generated_report_raw_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("11,122", "3,370", "78,120", "144", "1,422", "203", "15,000+"):
        assert banned not in text


def test_coordinators_extractor_is_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "coordinators" in result.stdout.strip().splitlines()


def test_coordinators_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_coordinators.tsv"
    run_extractor("coordinators", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")


def test_candidate_files_remain_lf_only() -> None:
    for path in sorted((ROOT / "output/publication_review").glob("candidates_*.tsv")):
        data = path.read_bytes()
        assert b"\r\n" not in data, f"{path} contains CRLF line endings"
        assert b"\r" not in data, f"{path} contains bare CR line endings"
