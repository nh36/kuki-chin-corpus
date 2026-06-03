from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_relators_postpositions_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_relators_postpositions_print_slice_exists_and_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert SLICE_PATH.exists()
    assert "Current relator / postposition inventory" in text
    assert "Spatial relator nouns" in text
    assert "Relator plus case-like marking" in text
    assert "Several issues remain outside the present account." in text
    assert "# Editorial scope" not in text
    for forbidden in ("candidate tsv", "dossier", "review notes", "packet", "print slice", "publication-review"):
        assert forbidden not in lower


def test_relators_postpositions_print_slice_keeps_core_forms_visible() -> None:
    text = _text()

    for required in (
        "kiang",
        "lak",
        "sung",
        "tung",
        "pualam",
        "sungah",
        "tungah",
        "kiangah",
        "lakpan",
    ):
        assert required in text
