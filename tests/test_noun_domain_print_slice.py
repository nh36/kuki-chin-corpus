from pathlib import Path


GRAMMAR_PATH = Path("output/publication_review/grammar_noun_domain_print_slice.md")


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_noun_domain_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "normalized noun domain print slice should exist"


def test_noun_domain_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_noun_domain.tsv",
        "dossier_noun_domain.md",
        "review_notes_noun_domain.md",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
    ):
        assert required in text


def test_noun_domain_print_slice_has_normalized_structure_and_anchors() -> None:
    text = _text()

    for heading in (
        "# Scope",
        "# Overview of the noun domain",
        "# Current noun-domain inventory",
        "# Simple noun stems",
        "# Plural marking with -te",
        "# Human nouns and common nouns",
        "# Nouns in larger phrases",
        "# Compounds and proper nouns",
        "# Nominalization boundary",
        "# Deferred and boundary material",
        "# Summary",
    ):
        assert heading in text

    for anchor in ("gam", "aksi", "aksi-te", "mi", "mite", "mi khempeuh", "minam"):
        assert anchor in text


def test_noun_domain_print_slice_keeps_boundaries_cautious() -> None:
    lower = _text().lower()

    assert "candidate evidence" in lower
    assert "explicit caveat" in lower or "explicit caveats" in lower
    assert "does not yet" in lower or "not yet enough" in lower
    assert "full noun-domain chapter" in lower
    assert "raw report-only noun lists" in lower
