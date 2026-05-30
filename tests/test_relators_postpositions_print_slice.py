from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_relators_postpositions_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_relators_postpositions_print_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()

    assert SLICE_PATH.exists()
    assert "candidates_relators_postpositions.tsv" in text
    assert "dossier_relators_postpositions_scope.md" in text


def test_relators_postpositions_print_slice_names_case_marking_boundary_control() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "candidates_case_marking.tsv",
        "dossier_case_marking.md",
        "grammar_case_marking_print_slice.md",
        "dictionary_case_markers_print_slice.md",
        "review_notes_case_marking.md",
    ):
        assert required in text

    assert "boundary control" in lower
    assert "not a rewrite of the case-marking packet" in lower


def test_relators_postpositions_print_slice_covers_core_relator_noun_anchors() -> None:
    text = _text()

    for required in (
        "kiang",
        "lak",
        "sung",
        "tung",
        "pualam",
    ):
        assert required in text

    assert "relational nouns or relational stems" in text
    assert "not simply bare case suffixes" in text


def test_relators_postpositions_print_slice_keeps_postpositions_boundary_controlled() -> None:
    text = _text()

    for required in ("pan", "panin", "tawh"):
        assert required in text

    assert "separate or relator-hosted source postposition" in text
    assert "source form with structural caution" in text
    assert "separate accompaniment or associative postposition" in text


def test_relators_postpositions_print_slice_keeps_boundary_material_out_of_core_claims() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "nuai",
        "mai",
        "tawhin",
        "kiangah",
        "sungah",
        "tungah",
        "lakpan",
        "kipan",
        "kipanin",
    ):
        assert required in text

    assert "raw report counts are not evidence" in lower
    assert "deferred or boundary-only" in lower


def test_relators_postpositions_print_slice_does_not_claim_later_surfaces_exist() -> None:
    text = _text()
    lower = text.lower()

    assert "dictionary print slice" in text
    assert "review notes do **not** yet exist" in text
    assert "review notes now exist" not in lower
