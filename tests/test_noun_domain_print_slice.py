from pathlib import Path


GRAMMAR_PATH = Path("output/publication_review/grammar_noun_domain_print_slice.md")


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_noun_domain_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "normalized noun domain print slice should exist"


def test_noun_domain_print_slice_avoids_internal_apparatus_language() -> None:
    lower = _text().lower()

    for forbidden in (
        "# scope",
        "current packet",
        "candidate evidence",
        "current print status",
        "print-ready",
        "print-usable",
        "workflow",
        "review-note maturity",
    ):
        assert forbidden not in lower


def test_noun_domain_print_slice_has_fuller_section_structure() -> None:
    text = _text()

    for required in (
        "Overview of the noun domain",
        "Noun-domain inventory",
        "Simple lexical nouns",
        "Human noun mi",
        "Plural marking with -te",
        "Compounds",
        "Proper names and titles",
        "Boundary with NP structure and nominalization",
        "Deferred material",
    ):
        assert required in text


def test_noun_domain_print_slice_keeps_core_forms_and_boundaries_visible() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "gam",
        "aksi",
        "aksi-te",
        "mi",
        "mite",
        "minam",
        "thugen",
        "Abraham",
        "Topa",
        "sanggam",
        "singnai",
        "kholhna",
        "No equally clean Old Testament example is currently used here",
        "Abraham' suan",
    ):
        assert required in text

    for required in (
        "simple lexical nouns",
        "plural marking with `-te`",
        "human noun `mi`",
        "transparent compounds",
        "title-like",
        "nominalization section",
        "np structure",
    ):
        assert required in lower


def test_noun_domain_print_slice_avoids_raw_report_counts() -> None:
    lower = _text().lower()

    for forbidden in ("12x", "24x", "report frequency", "frequency table"):
        assert forbidden not in lower
