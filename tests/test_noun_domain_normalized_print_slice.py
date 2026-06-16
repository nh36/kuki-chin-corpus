from __future__ import annotations

import re
from pathlib import Path


GRAMMAR_PATH = Path("output/publication_review/grammar_noun_domain_print_slice.md")
SUPPLEMENT_PATH = Path("output/publication_review/examples_noun_domain_normalization.tsv")


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def _example_labels() -> list[str]:
    return re.findall(r"^\(@ex:(noun-[^)]+)\)", _text(), flags=re.MULTILINE)


def test_noun_domain_normalized_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "grammar_noun_domain_print_slice.md must exist"


def test_noun_domain_normalized_print_slice_avoids_internal_prose() -> None:
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
        "coverage-normalization",
        "raw report-only noun lists",
    ):
        assert forbidden not in lower


def test_noun_domain_normalized_print_slice_has_inventory_and_core_anchors() -> None:
    text = _text()

    assert "# Noun-domain inventory" in text
    assert "| Form or pattern | Function | Status | Notes |" in text

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
    ):
        assert required in text


def test_noun_domain_normalized_print_slice_discusses_required_domains() -> None:
    text = _text()
    lower = text.lower()

    for heading in (
        "# Simple lexical nouns",
        "# Human noun mi",
        "# Plural marking with -te",
        "# Compounds",
        "# Proper names and titles",
        "# Boundary with NP structure and nominalization",
        "# Deferred material",
    ):
        assert heading in text

    for required in (
        "simple lexical nouns",
        "human noun `mi`",
        "plural marking with `-te`",
        "transparent compounds",
        "title-like",
        "nominalization",
        "NP structure",
        "mi khat",
        "mi khempeuh",
        "mi pawlkhat",
        "mi tampi",
    ):
        assert required.lower() in lower


def test_noun_domain_normalized_print_slice_keeps_boundaries_explicit() -> None:
    lower = _text().lower()

    for required in (
        "full noun classification",
        "full plural system",
        "classifier-like nouns",
        "complete compound typology",
        "nominalized nouns",
        "proper-name syntax",
        "title morphology",
        "full relation between nouns and np structure",
    ):
        assert required in lower


def test_noun_domain_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    assert len(_example_labels()) >= 6
    assert "Genesis 2:5" in text
    assert "Matthew 2:2" in text
    assert "Genesis 1:16" in text
    assert "Exodus 5:5" in text
    assert "Genesis 32:24" in text
    assert "Luke 2:1" in text
    assert "Genesis 11:6" in text
    assert "Genesis 4:23" in text
    assert "Matthew 1:1" in text


def test_noun_domain_normalized_print_slice_avoids_raw_count_promotion() -> None:
    lower = _text().lower()

    assert "12x" not in lower
    assert "24x" not in lower
    assert "report frequency" not in lower
    assert "frequency table" not in lower


def test_noun_domain_examples_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists(), "examples_noun_domain_normalization.tsv must exist"

    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "noun_topic",
        "candidate_form",
        "construction_type",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "example_quality",
        "print_status",
        "why_selected",
        "caveat",
    ):
        assert column in header


def test_noun_domain_examples_supplement_includes_ot_and_gospel_rows() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8")

    assert "Old Testament" in text
    assert "Gospels" in text
    assert "Genesis 2:5" in text
    assert "Matthew 1:1" in text or "Luke 2:1" in text or "Matthew 2:2" in text


def test_noun_domain_examples_supplement_does_not_mark_unvetted_rows_print_ready() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8").lower()

    assert "raw hit" not in text
    assert "report-only\tprint-ready" not in text
