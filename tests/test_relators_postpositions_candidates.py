import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_relators_postpositions.tsv"

REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "candidate_group",
    "candidate_form",
    "construction_type",
    "source_type",
    "source_reference",
    "anchor_form",
    "segmentation_span",
    "gloss_span",
    "rough_function",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
}


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_relators_postpositions_candidates_file_exists_and_has_curated_rows() -> None:
    rows = _rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"relators_postpositions"}
    assert len(rows) >= 10


def test_relators_postpositions_candidates_include_core_relator_nouns() -> None:
    forms = {row["candidate_form"] for row in _rows()}

    for required in ("kiang", "lak", "sung", "tung"):
        assert required in forms


def test_relators_postpositions_candidates_include_requested_postpositions() -> None:
    forms = {row["candidate_form"] for row in _rows()}

    for required in ("pan", "panin", "tawh", "tawhin"):
        assert required in forms


def test_relators_postpositions_candidates_keep_boundary_and_deferred_material_visible() -> None:
    rows = _rows()

    assert any(
        row["candidate_form"] == "pualam" and row["candidate_status"] == "accepted_with_caveat"
        for row in rows
    )
    assert any(
        row["candidate_form"] == "nuai" and row["candidate_status"] == "needs_review"
        for row in rows
    )
    assert any(
        row["candidate_form"] == "mai" and row["candidate_status"] == "needs_review"
        for row in rows
    )
    assert any(
        row["candidate_form"] == "tawhin" and row["candidate_status"] == "deferred"
        for row in rows
    )


def test_relators_postpositions_candidates_avoid_generated_report_count_claims() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("18,367", "13,384", "7,808", "4,556", "4,388", "7,336"):
        assert banned not in text
