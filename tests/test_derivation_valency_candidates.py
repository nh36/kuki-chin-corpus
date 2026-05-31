from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = ROOT / "output/publication_review/candidates_derivation_valency.tsv"


def _rows() -> list[list[str]]:
    lines = TSV_PATH.read_text(encoding="utf-8").strip().splitlines()
    return [line.split("\t") for line in lines]


def test_derivation_valency_candidates_exists() -> None:
    assert TSV_PATH.exists(), "Derivation / valency candidate TSV must exist"


def test_derivation_valency_candidates_has_expected_header() -> None:
    rows = _rows()
    header = rows[0]

    assert header == [
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
    ]


def test_derivation_valency_candidates_has_curated_rows() -> None:
    rows = _rows()
    body = rows[1:]
    text = TSV_PATH.read_text(encoding="utf-8")

    assert len(body) >= 8

    for required in (
        "paisak",
        "muhsak",
        "paipih",
        "kisep",
        "ciahsakkik",
    ):
        assert required in text

    assert "-sak" in text
    assert "-pih" in text
    assert "ki-" in text
    assert "accepted" in text
    assert "deferred" in text

