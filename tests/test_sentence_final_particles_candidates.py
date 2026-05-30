import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_sentence_final_particles.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTEDISH = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "particle_type",
    "particle_form",
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
    return [row for row in load_rows() if row["particle_form"] == form]


def test_sentence_final_particle_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"sentence_final_particles"}


def test_sentence_final_particle_candidate_file_keeps_hi_narrow_and_overlap_controlled() -> None:
    hi_rows = rows_for("hi")

    assert hi_rows
    assert any(
        row["candidate_status"] in ACCEPTEDISH
        and row["construction_type"] in {"copula_plus_declarative_ahi_hi", "declarative_hi"}
        and row["reference"] == "Genesis 1:13"
        and "ahi hi" in row["surface_span"].lower()
        for row in hi_rows
    )
    assert any(
        "copula" in row["why_excluded"].lower() or "copula" in row["notes"].lower()
        for row in hi_rows
        if row["reference"] == "Genesis 1:13"
    )
    assert any(
        row["particle_type"] == "negation_overlap"
        and row["construction_type"] == "neg_plus_declarative_lo_hi"
        and "negation" in row["notes"].lower()
        for row in hi_rows
    )


def test_sentence_final_particle_candidate_file_keeps_hiam_as_overlap_control_only() -> None:
    hiam_rows = rows_for("hiam")

    assert hiam_rows
    assert all(row["particle_type"] == "interrogative_overlap" for row in hiam_rows)
    assert all(row["construction_type"] == "interrogative_hiam_overlap_control" for row in hiam_rows)
    assert all(row["candidate_status"] in {"deferred", "accepted_with_caveat"} for row in hiam_rows)
    assert all(
        "interrogatives packet" in row["why_excluded"].lower() or "cross-reference" in row["notes"].lower()
        for row in hiam_rows
    )


def test_sentence_final_particle_candidate_file_keeps_hen_tahen_and_imperatives_conservative() -> None:
    tahen_rows = rows_for("tahen")
    hen_rows = rows_for("hen")
    in_rows = rows_for("in")
    un_rows = rows_for("un")

    assert tahen_rows
    assert any(
        row["construction_type"] == "jussive_tahen"
        and row["candidate_status"] in {"deferred", "accepted_with_caveat", "needs_review"}
        and (
            "army" in row["why_excluded"].lower()
            or "tahen" in row["why_selected"].lower()
            or "ta hen" in row["notes"].lower()
        )
        for row in tahen_rows
    )

    assert hen_rows
    assert any(
        row["construction_type"] == "optative_hen"
        and row["candidate_status"] in ACCEPTEDISH | {"deferred"}
        and ("optative" in row["notes"].lower() or "optative" in row["why_excluded"].lower())
        for row in hen_rows
    )

    assert in_rows
    assert any(
        row["particle_type"] == "imperative_singular"
        and row["construction_type"] == "imperative_in"
        and row["candidate_status"] in ACCEPTEDISH | {"needs_review", "deferred"}
        and (
            "case" in row["why_excluded"].lower()
            or "harvesting" in row["why_excluded"].lower()
            or "overlap" in row["notes"].lower()
        )
        for row in in_rows
    )

    assert un_rows
    assert any(
        row["particle_type"] == "imperative_plural"
        and row["construction_type"] == "imperative_un"
        and row["candidate_status"] in ACCEPTEDISH | {"deferred"}
        for row in un_rows
    )


def test_sentence_final_particle_candidate_file_keeps_aw_ta_and_zo_as_boundary_material() -> None:
    aw_rows = rows_for("aw")
    ta_rows = rows_for("ta")
    zo_rows = rows_for("zo")

    assert aw_rows
    assert any(
        row["particle_type"] == "exclamative_vocative"
        and row["construction_type"] in {"exclamative_aw", "vocative_aw"}
        and row["candidate_status"] in ACCEPTEDISH | {"deferred", "needs_review"}
        for row in aw_rows
    )

    assert ta_rows or zo_rows
    if ta_rows:
        assert all(row["particle_type"] in {"aspectual_boundary", "tam_overlap"} for row in ta_rows)
        assert all(row["construction_type"] in {"aspect_plus_decl_ta_hi", "perfective_ta_boundary"} for row in ta_rows)
        assert all(row["candidate_status"] in {"accepted_with_caveat", "needs_review", "deferred"} for row in ta_rows)
    if zo_rows:
        assert all(row["particle_type"] in {"aspectual_boundary", "tam_overlap", "deferred"} for row in zo_rows)
        assert all(row["construction_type"] in {"completive_zo_boundary", "analyzer_noise"} for row in zo_rows)
        assert all(row["candidate_status"] in {"accepted_with_caveat", "needs_review", "deferred"} for row in zo_rows)


def test_sentence_final_particle_candidate_file_avoids_generated_report_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("24,754", "1,000", "858", "764", "5,230", "150", "230", "137", "670", "39", "2,306", "1,144", "577", "167+", "338"):
        assert banned not in text


def test_sentence_final_particle_extractor_is_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "sentence_final_particles" in result.stdout.strip().splitlines()


def test_sentence_final_particle_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_sentence_final_particles.tsv"
    run_extractor("sentence_final_particles", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")


def test_candidate_files_remain_lf_only() -> None:
    for path in sorted((ROOT / "output/publication_review").glob("candidates_*.tsv")):
        data = path.read_bytes()
        assert b"\r\n" not in data, f"{path} contains CRLF line endings"
        assert b"\r" not in data, f"{path} contains bare CR line endings"
