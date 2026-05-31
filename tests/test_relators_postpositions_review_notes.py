from pathlib import Path


NOTES_PATH = Path("output/publication_review/review_notes_relators_postpositions.md")


def _text() -> str:
    return NOTES_PATH.read_text(encoding="utf-8")


def test_relators_postpositions_review_notes_exist() -> None:
    assert NOTES_PATH.exists(), "Relators/postpositions review notes must exist"


def test_relators_postpositions_review_notes_name_controlling_files() -> None:
    text = _text()

    for required in (
        "candidates_relators_postpositions.tsv",
        "dossier_relators_postpositions_scope.md",
        "grammar_relators_postpositions_print_slice.md",
        "dictionary_relators_postpositions_print_slice.md",
    ):
        assert required in text


def test_relators_postpositions_review_notes_name_case_marking_boundary_control() -> None:
    text = _text()

    for required in (
        "candidates_case_marking.tsv",
        "dossier_case_marking.md",
        "grammar_case_marking_print_slice.md",
        "dictionary_case_markers_print_slice.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_relators_postpositions_review_notes_mark_packet_aligned_and_review_ready() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate TSV" in text
    assert "scoping dossier" in lower
    assert "grammar print slice" in lower
    assert "dictionary print slice" in lower
    assert "tests" in lower
    assert "ready for human review at the current slice maturity level" in text
    assert "not a rewrite of the case-marking packet" in lower
    assert "not a broad postposition inventory" in lower


def test_relators_postpositions_review_notes_cover_first_slice_forms() -> None:
    text = _text()

    for required in (
        "kiang",
        "lak",
        "sung",
        "tung",
        "pualam",
        "pan",
        "panin",
        "tawh",
    ):
        assert required in text


def test_relators_postpositions_review_notes_keep_boundary_material_outside_first_slice() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "nuai",
        "mai",
        "tawhin",
        "kipan",
        "kipanin",
        "kiangah",
        "sungah",
        "tungah",
        "lakpan",
    ):
        assert required in text

    assert "raw generated-report counts as evidence" in lower
    assert "shared" in lower or "boundary" in lower

