from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TSV_PATH = REPO_ROOT / "output" / "publication_review" / "candidates_noun_domain.tsv"


def test_noun_domain_candidates_file_exists() -> None:
    assert TSV_PATH.exists()


def test_noun_domain_candidates_header_and_curated_rows() -> None:
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


def test_noun_domain_candidates_cover_simple_nouns_compounds_and_proper_nouns() -> None:
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "gam",
        "aksi / aksi-te",
        "minam",
        "thugen",
        "Abraham",
        "Topa",
    ):
        assert required in text


def test_noun_domain_candidates_keep_transparency_and_opaque_rows_visible() -> None:
    text = TSV_PATH.read_text(encoding="utf-8")

    for required in (
        "transparent_compound",
        "opaque_lexicalized_compound",
        "compound_transparency_boundary",
        "sanggam",
        "singnai",
        "kholhna",
    ):
        assert required in text
