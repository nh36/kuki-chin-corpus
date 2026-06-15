from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_numerals_print_slice.md"


def test_numerals_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_numerals_print_slice_has_fuller_grammar_structure() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    assert "Overview of the numeral system" in text
    assert "Cardinal inventory" in text
    assert "Compound numerals" in text
    assert "Noun-plus-numeral word order" in text
    assert "Ordinals and the `-na` boundary" in text
    assert "Multiplicative and counting expressions" in text
    assert "Ambiguity controls: `kua` and `khat`" in text
    assert "Deferred and boundary material" in text


def test_numerals_print_slice_includes_core_examples() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for required in (
        "kum nih",
        "ni sagih",
        "kum sawmkua",
        "nihna",
        "sawmvei",
        "mi khat",
        "kum zakua le kum sawmguk le kua",
    ):
        assert required in text


def test_numerals_print_slice_handles_kua_and_khat_cautiously() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "hihte kua ahi hiam" in lower
    assert "interrogative" in lower
    assert "do not overgeneralize indefinite-like uses as pure numeral syntax" in lower
    assert "mi khat" in lower


def test_numerals_print_slice_keeps_compound_and_boundary_caveats_visible() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "nine [export: who]" in text
    assert "the final token gloss" in lower
    assert "no equally clean gospel example is currently used for this construction." in lower


def test_numerals_print_slice_avoids_internal_workflow_prose_and_raw_counts() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x"):
        assert banned not in text
    for banned in ("current packet", "candidate layer", "print slice", "the workflow", "this commit"):
        assert banned not in lower
