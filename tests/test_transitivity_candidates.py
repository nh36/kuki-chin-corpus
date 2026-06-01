import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_transitivity.tsv"


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_transitivity_candidates_exists() -> None:
    assert CANDIDATES_PATH.exists(), "Transitivity candidates TSV must exist"


def test_transitivity_candidates_have_expected_header_and_curated_rows() -> None:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        header = next(reader)

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

    rows = _rows()
    assert len(rows) >= 8


def test_transitivity_candidates_include_intransitive_and_transitive_material() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for required in (
        "clean_intransitive_anchor",
        "clean_transitive_anchor",
        "sih",
        "suak",
        "hawl",
        "en",
    ):
        assert required in text


def test_transitivity_candidates_include_alternation_and_boundary_material() -> None:
    text = CANDIDATES_PATH.read_text(encoding="utf-8")

    for required in (
        "ambitransitive_or_labile",
        "mu",
        "muh",
        "prefix_agreement_boundary",
        "nei / neih",
        "case_marking_ditransitive_boundary",
        "pia",
        "valency_changing_or_lexicalized_boundary",
        "piangsak",
    ):
        assert required in text
