from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = REPO_ROOT / "output" / "publication_review" / "candidates_reduplication.tsv"


def test_reduplication_candidates_file_exists() -> None:
    assert TSV_PATH.exists()


def test_reduplication_candidates_header_and_curated_rows() -> None:
    lines = TSV_PATH.read_text(encoding="utf-8").strip().splitlines()

    assert lines
    assert lines[0].split("\t") == [
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
    assert len(lines) >= 8


def test_reduplication_candidates_cover_core_reduplication_material() -> None:
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "mahmah",
        "taktak",
        "peuhpeuh",
        "ni ni",
        "leuleu",
        "gengen",
        "kawikawi",
        "theithei",
    ):
        assert required in text


def test_reduplication_candidates_keep_productive_and_lexicalized_material_visible() -> None:
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "full_reduplication_anchor",
        "full_reduplication_support",
        "syntactic_reduplication_temporal",
        "verbal_reduplication_candidate",
        "lexicalized_reduplicative_looking_form",
        "tam_boundary_reduplicative_looking_form",
        "print_ready",
        "boundary_only",
    ):
        assert required in text
