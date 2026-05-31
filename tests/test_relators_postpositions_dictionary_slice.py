from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/dictionary_relators_postpositions_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_relators_postpositions_dictionary_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()
    lower = text.lower()

    assert SLICE_PATH.exists()
    assert "candidates_relators_postpositions.tsv" in text
    assert "dossier_relators_postpositions_scope.md" in text
    assert "grammar_relators_postpositions_print_slice.md" in text
    assert "boundary control" in lower
    assert "not a machine-dictionary edit" in lower
    assert "not a rewrite of the case-marking packet" in lower


def test_relators_postpositions_dictionary_slice_names_case_marking_boundary_control() -> None:
    text = _text()

    for required in (
        "candidates_case_marking.tsv",
        "dossier_case_marking.md",
        "grammar_case_marking_print_slice.md",
        "dictionary_case_markers_print_slice.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_relators_postpositions_dictionary_slice_has_required_entries() -> None:
    text = _text()

    for heading in (
        "## `kiang`",
        "## `lak`",
        "## `sung`",
        "## `tung`",
        "## `pualam`",
        "## `pan`",
        "## `panin`",
        "## `tawh`",
    ):
        assert heading in text

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


def test_relators_postpositions_dictionary_slice_keeps_boundary_material_out_of_core_entries() -> None:
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

    assert "boundary material" in lower
    assert "raw generated-report counts are not dictionary evidence" in lower


def test_relators_postpositions_dictionary_slice_names_review_notes_surface() -> None:
    text = _text()

    assert "review_notes_relators_postpositions.md" in text
    assert "ready for human review at the current slice maturity level" in text
