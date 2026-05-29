import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_numerals.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTED_STATUSES = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "numeral_type",
    "numeral_value",
    "numeral_form",
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


def test_numerals_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"numerals"}


def test_numerals_candidate_file_covers_core_cardinal_ordinal_and_counting_rows() -> None:
    accepted_rows = [row for row in load_rows() if row["candidate_status"] in ACCEPTED_STATUSES]

    assert any(row["numeral_type"] in {"cardinal", "compound_cardinal"} for row in accepted_rows)
    assert any(row["numeral_type"] == "ordinal" for row in accepted_rows)
    assert any(row["numeral_type"] in {"classifier_counting", "multiplicative", "distributive"} for row in accepted_rows)


def test_numerals_candidate_file_keeps_kua_ambiguity_explicit() -> None:
    rows = load_rows()
    accepted_rows = [row for row in rows if row["candidate_status"] in ACCEPTED_STATUSES]

    assert any(
        row["numeral_form"] and "kua" in row["numeral_form"] and row["numeral_type"] in {"cardinal", "compound_cardinal", "large_number"}
        for row in accepted_rows
    )

    false_friend_rows = [
        row
        for row in rows
        if row["construction_type"] == "kua_who_false_friend"
    ]
    assert false_friend_rows
    assert all(row["candidate_status"] == "excluded" for row in false_friend_rows)
    assert all(row["print_status"] == "blocked" for row in false_friend_rows)
    assert any("who" in row["why_excluded"].lower() for row in false_friend_rows)


def test_numerals_candidate_file_keeps_khat_boundary_caveated() -> None:
    rows = [
        row
        for row in load_rows()
        if row["construction_type"] == "khat_indefinite_boundary" or row["numeral_form"] == "khat"
    ]

    assert rows
    assert all(row["candidate_status"] != "accepted" for row in rows)
    assert all(
        row["numeral_type"] == "indefinite_or_quantifier_overlap" or "boundary" in row["notes"].lower()
        for row in rows
    )
    assert all(row["print_status"] in {"print_usable_with_caveat", "not_print_ready", "blocked"} for row in rows)


def test_numerals_candidate_file_tracks_distributive_material_conservatively() -> None:
    rows = [row for row in load_rows() if row["construction_type"] == "numeral_reduplication"]

    assert rows
    if not any(row["candidate_status"] in ACCEPTED_STATUSES for row in rows):
        assert any(row["candidate_status"] in {"deferred", "needs_review"} for row in rows)
        assert any("not yet analyzer-backed" in row["why_excluded"].lower() or "analyzer" in row["why_excluded"].lower() for row in rows)


def test_numerals_candidate_file_avoids_raw_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("9,000+", "4,712", "541"):
        assert banned not in text


def test_numerals_extractor_lists_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "numerals" in result.stdout.strip().splitlines()


def test_numerals_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_numerals.tsv"
    run_extractor("numerals", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")
