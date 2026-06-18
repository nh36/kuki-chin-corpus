from pathlib import Path


SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/grammar_tam_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_tam_print_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()

    assert SLICE_PATH.exists()
    assert "TAM / aspect / modal inventory" in text
    assert "Overview of TAM / aspect / modal marking" in text
    assert "Deferred questions" in text
    assert "Several issues remain outside the present account." in text


def test_tam_print_slice_limits_first_slice_anchors_to_selected_compact_forms() -> None:
    text = _text()

    for required in (
        "-ngei",
        "-gige",
        "-zel",
        "-ta",
        "-zo",
        "-kik",
        "-ding",
        "-thei",
    ):
        assert required in text

    assert "| Form | Approximate function | Position / host relation | Diagnostic example | Source | Status |" in text


def test_tam_print_slice_keeps_required_coordination_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "relation to stem alternation" in lower
    assert "form i / form ii" in lower
    assert "relation to prefix/agreement" in lower
    assert "relation to directionals and vp structure" in lower


def test_tam_print_slice_keeps_deferred_questions_explicit() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "pailai",
        "dingin",
        "khiathei ding om lo",
        "mangngilh ta hi",
        "khia-ta",
        "bawlzoding",
        "bawlsakthei",
        "`-nawn`",
        "`-khin`",
    ):
        assert required in text

    assert "outside the present account" in lower


def test_tam_print_slice_avoids_stale_internal_phrasing() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate tsv" not in lower
    assert "dossier" not in lower
    assert "boundary material" not in lower
    assert "# Editorial scope" not in text
