from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = REPO_ROOT / "output" / "publication_review" / "candidates_np_possession.tsv"


def test_np_possession_candidates_file_exists():
    assert TSV_PATH.exists()


def test_np_possession_candidates_header_and_curated_rows():
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
    assert len(lines) >= 7


def test_np_possession_candidates_cover_np_structure_and_possession():
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "hih mite",
        "mi khat",
        "mi khempeuh",
        "ka pa",
        "Topa' inn",
        "a pa' inn",
    ):
        assert required in text


def test_np_possession_candidates_keep_boundary_rows_visible():
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "Topa' tungah",
        "ka suahna leitang",
        "possessive_prefix_nominal_host",
        "double_possession_chain",
        "nominalized_possessed_np_boundary",
    ):
        assert required in text
