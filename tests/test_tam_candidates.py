import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_tam.tsv"

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


def test_tam_candidates_file_exists_and_has_curated_rows() -> None:
    rows = _rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"tam"}
    assert len(rows) >= 10


def test_tam_candidates_keep_clean_test_backed_anchors_visible() -> None:
    anchors = {row["anchor_form"] for row in _rows()}

    for required in (
        "paingei",
        "neigige",
        "paizel",
        "kilawmta",
        "bawlzo",
        "hongpaikik",
        "omding",
        "bawlthei",
    ):
        assert required in anchors


def test_tam_candidates_record_clause_bound_and_deferred_material() -> None:
    rows = _rows()

    assert any(
        row["anchor_form"] == "pailai"
        and row["candidate_status"] == "deferred"
        and "lexical" in row["rough_function"].lower()
        for row in rows
    )
    assert any(
        row["anchor_form"] == "dingin"
        and row["candidate_status"] == "deferred"
        and "clause" in row["candidate_group"]
        for row in rows
    )


def test_tam_candidates_keep_overlap_controls_explicit() -> None:
    rows = _rows()

    assert any(
        row["candidate_group"] == "negation_overlap"
        and "khiathei ding om lo" in row["anchor_form"]
        for row in rows
    )
    assert any(
        row["candidate_group"] == "sentence_final_overlap"
        and "mangngilh ta hi" in row["anchor_form"]
        for row in rows
    )
    assert any(
        row["candidate_group"] == "directional_overlap"
        and "khia-ta" in row["anchor_form"]
        for row in rows
    )


def test_tam_candidates_avoid_generated_report_counts() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for banned in ("28047x", "7573x", "5680x", "4095x", "3085x", "1749x", "1262x", "1069x"):
        assert banned not in text
