from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output" / "publication_review" / "grammar_np_possession_print_slice.md"
EXAMPLES_PATH = ROOT / "output" / "publication_review" / "examples_np_possession_normalization.tsv"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def _examples_text() -> str:
    return EXAMPLES_PATH.read_text(encoding="utf-8")


def test_np_possession_normalized_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Normalized NP structure / possession slice must exist"


def test_np_possession_normalized_print_slice_avoids_internal_scope_and_workflow_language() -> None:
    lower = _text().lower()

    for forbidden in (
        "# scope",
        "current packet",
        "current section depends on",
        "candidate evidence",
        "coverage-normalization standard",
        "print status",
        "print-ready",
        "print-usable",
        "current pass",
        "workflow",
        "review-note maturity",
    ):
        assert forbidden not in lower


def test_np_possession_normalized_print_slice_has_inventory_and_safe_anchors() -> None:
    text = _text()

    assert "# NP pattern inventory" in text
    assert "| Pattern | Example form | Function | Status | Boundary notes |" in text

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

    assert "mi khat" in text or ("`mi` 'person'" in text and "`khat` 'one'" in text)


def test_np_possession_normalized_print_slice_discusses_required_domains() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Boundary with numerals and quantifiers",
        "Boundary with pronouns, prefix/agreement, case, and relators",
        "Deferred material",
    ):
        assert required in text

    assert "noun-plus-numeral order" in lower
    assert "noun-plus-quantifier order" in lower
    assert "possessor-before-possessed order" in lower


def test_np_possession_normalized_print_slice_keeps_boundaries_explicit() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "khat",
        "khempeuh",
        "pawlkhat",
        "tampi",
        "prefix/agreement",
        "case marking",
        "relator",
    ):
        assert required in text

    assert "Topa' tungah" in text or ("`Topa'` 'Lord'" in text and "`tungah` 'on'" in text)
    assert "ka suahna leitang" in text or ("`ka` 'my'" in text and "`suahna` 'birth-NMLZ'" in text and "`leitang` 'land'" in text)

    assert "full possession paradigm" in lower
    assert "apostrophe marking" in lower
    assert "recursive or chained possessive structures" in lower


def test_np_possession_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_blocks = re.findall(
        r"^\(@ex:np-[^)]+\).+\n"
        r"a\. Tedim: .+\n"
        r"b\. Segmentation: .+\n"
        r"c\. Gloss: .+\n"
        r"d\. Translation: .+\n",
        text,
        flags=re.MULTILINE,
    )

    assert text.count("(@ex:np-") >= 6
    assert len(example_blocks) >= 6
    assert "Exodus 5:5" in text or "Genesis 24:23" in text
    assert "John 11:39" in text or "Luke 2:1" in text or "Matthew 2:1" in text or "Mark 6:34" in text


def test_np_possession_normalized_print_slice_avoids_raw_count_promotion() -> None:
    lower = _text().lower()

    assert "12x" not in lower
    assert "24x" not in lower
    assert "report frequency" not in lower
    assert "frequency table" not in lower


def test_np_possession_examples_supplement_exists_and_has_expected_columns() -> None:
    text = _examples_text()

    assert EXAMPLES_PATH.exists(), "NP/possession normalization supplement must exist"

    header = text.splitlines()[0]
    for required in (
        "example_id",
        "np_topic",
        "candidate_form",
        "construction_type",
        "source_reference",
        "source_zone",
        "example_quality",
        "print_status",
        "caveat",
    ):
        assert required in header


def test_np_possession_examples_supplement_includes_ot_and_gospel_rows() -> None:
    text = _examples_text()

    assert "\tOld Testament\t" in text
    assert "\tGospels\t" in text
    assert "Exodus 5:5" in text
    assert "John 11:39" in text or "Luke 2:1" in text


def test_np_possession_examples_supplement_does_not_mark_unvetted_rows_print_ready() -> None:
    lines = _examples_text().splitlines()[1:]
    control_row = next(line for line in lines if line.startswith("npnorm-poss-a-pa-inn-control\t"))

    assert "\tdeferred\t" in control_row
