from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = REPO_ROOT / "output" / "publication_review" / "grammar_np_possession_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_np_possession_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "NP structure / possession grammar slice must exist"


def test_np_possession_print_slice_avoids_internal_apparatus_language() -> None:
    lower = _text().lower()

    for forbidden in (
        "# scope",
        "current packet",
        "current section depends on",
        "coverage-normalization standard",
        "candidate evidence",
        "print-ready",
        "print-usable",
        "workflow",
        "review-note maturity",
    ):
        assert forbidden not in lower


def test_np_possession_print_slice_has_fuller_section_structure() -> None:
    text = _text()

    for required in (
        "Overview of noun phrase structure",
        "NP pattern inventory",
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Boundary with numerals and quantifiers",
        "Boundary with pronouns, prefix/agreement, case, and relators",
        "Deferred material",
    ):
        assert required in text


def test_np_possession_print_slice_keeps_core_forms_and_boundaries_visible() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "hih mite",
        "ni li",
        "kum sawm le nih",
        "mi khempeuh",
        "mi pawlkhat",
        "mi tampi",
        "na pa' inn-ah",
        "a zi' min",
    ):
        assert required in text

    assert "Topa' inn" in text or ("`Topa'` 'Lord'" in text and "`inn` 'house'" in text)
    assert "a pa' inn" in text or ("`a` 'his'" in text and "`pa'` 'father'" in text and "`inn` 'house'" in text)
    assert "Topa' tungah" in text or ("`Topa'` 'Lord'" in text and "`tungah` 'on'" in text)
    assert "ka suahna leitang" in text or ("`ka` 'my'" in text and "`suahna` 'birth-NMLZ'" in text and "`leitang` 'land'" in text)

    assert "possessor-before-possessed order" in lower
    assert "full possession paradigm" in lower
    assert "apostrophe marking" in lower


def test_np_possession_print_slice_avoids_raw_report_counts() -> None:
    lower = _text().lower()

    for forbidden in ("5,191", "4,712", "3,021", "2,244", "1,100", "12x", "24x", "frequency table"):
        assert forbidden not in lower
