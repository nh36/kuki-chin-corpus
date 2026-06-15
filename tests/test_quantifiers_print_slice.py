from pathlib import Path


SLICE = Path("output/publication_review/grammar_quantifiers_print_slice.md")


def _text() -> str:
    return SLICE.read_text(encoding="utf-8")


def test_quantifiers_print_slice_exists() -> None:
    assert SLICE.exists(), "Quantifiers print slice must exist"


def test_quantifiers_print_slice_avoids_internal_apparatus() -> None:
    text = _text()

    for forbidden in (
        "coverage_normalization_audit.md",
        "current packet",
        "print slice",
        "candidate layer",
        "this commit",
    ):
        assert forbidden not in text


def test_quantifiers_print_slice_has_inventory_examples_and_core_forms() -> None:
    text = _text()

    assert "Quantifier inventory" in text
    assert text.count("(@ex:quant-") >= 4

    for required in (
        "khempeuh",
        "pawlkhat",
        "mi khat",
        "kuamah",
        "bangmah",
        "tampi tak",
        "mi tampi",
        "zaw",
        "mahmah",
        "peuhpeuh",
        "tawm",
    ):
        assert required in text


def test_quantifiers_print_slice_keeps_boundary_caveats_visible() -> None:
    text = _text()

    for required in (
        "Boundary with numerals",
        "Boundary with NP structure and negation",
        "khat",
        "negation licensing",
        "bang-family",
        "indefinite-like",
        "noun phrase",
        "deferred",
    ):
        assert required in text


def test_quantifiers_print_slice_keeps_deferred_material_clear() -> None:
    text = _text()

    assert "Deferred material" in text
    for required in (
        "does not yet settle",
        "full free-choice",
        "indefinite uses",
        "intensifier",
        "degree",
        "NP template",
    ):
        assert required in text


def test_quantifiers_print_slice_avoids_raw_report_counts() -> None:
    text = _text()

    for forbidden in ("5,191", "4,712", "3,021", "2,244", "1,100"):
        assert forbidden not in text
