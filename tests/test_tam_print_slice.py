from pathlib import Path


SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/grammar_tam_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_tam_print_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()

    assert SLICE_PATH.exists()
    assert "Current TAM inventory" in text
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

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text


def test_tam_print_slice_keeps_required_caveats_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "sentence-final particles" in lower
    assert "directionals and vp structure" in lower
    assert "clause-bound `dingin`" in lower
    assert "khiathei ding om lo" in text


def test_tam_print_slice_keeps_overlap_and_deferred_material_out_of_scope() -> None:
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


def test_tam_print_slice_does_not_claim_later_tam_surfaces_exist() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate tsv" not in lower
    assert "dossier" not in lower
    assert "# Editorial scope" not in text
