from pathlib import Path


SLICE = Path("output/publication_review/grammar_quantifiers_print_slice.md")


def _text() -> str:
    return SLICE.read_text(encoding="utf-8")


def test_quantifiers_print_slice_exists() -> None:
    assert SLICE.exists(), "Quantifiers print slice must exist"


def test_quantifiers_print_slice_names_normalization_controls() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "grammar_numerals_print_slice.md",
        "candidates_quantifiers.tsv",
        "dossier_quantifiers.md",
        "review_notes_quantifiers.md",
        "docs/grammar/reports/06-func-05-quantifiers.md",
        "examples_quantifiers_normalization.tsv",
    ):
        assert required in text


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
        "does not treat `khat` as an uncomplicated quantifier anchor",
        "cross-reference, not reopen, the stabilized negation packet",
        "negative-licensed",
        "bang-family",
        "blocked control",
        "candidate evidence",
        "explicit caveats",
        "noun-phrase",
    ):
        assert required in text


def test_quantifiers_print_slice_keeps_edge_rows_narrow() -> None:
    text = _text()

    for required in (
        "broad adjective/adverb chapter",
        "comparison or intensifier chapter",
        "edge rows only",
        "free-choice",
        "deferred",
        "not the start of a broad adjective/adverb chapter",
    ):
        assert required in text


def test_quantifiers_print_slice_avoids_raw_report_counts() -> None:
    text = _text()

    for forbidden in ("5,191", "4,712", "3,021", "2,244", "1,100"):
        assert forbidden not in text
