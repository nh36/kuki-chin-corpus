import csv
import re
from pathlib import Path


SLICE = Path("output/publication_review/grammar_quantifiers_print_slice.md")
SUPPLEMENT = Path("output/publication_review/examples_quantifiers_normalization.tsv")


def _text() -> str:
    return SLICE.read_text(encoding="utf-8")


def _example_labels() -> list[str]:
    return re.findall(r"^\(@ex:(quant-[^)]+)\)", _text(), flags=re.MULTILINE)


def test_quantifiers_normalized_print_slice_exists() -> None:
    assert SLICE.exists(), "Normalized quantifiers print slice must exist"


def test_quantifiers_normalized_print_slice_avoids_internal_prose() -> None:
    text = _text()

    # Grammar-facing sections should not expose internal workflow language
    for forbidden in (
        "current packet",
        "print slice",
        "candidate layer",
        "this commit",
        "workflow",
        "coverage_normalization_audit.md",
    ):
        assert forbidden not in text


def test_quantifiers_normalized_print_slice_has_inventory_table() -> None:
    text = _text()

    assert "Quantifier inventory" in text
    assert "| Form | Provisional function | Current status | Notes |" in text
    assert "khempeuh" in text
    assert "pawlkhat" in text
    assert "kuamah" in text
    assert "bangmah" in text


def test_quantifiers_normalized_print_slice_has_formal_examples() -> None:
    assert len(_example_labels()) >= 4


def test_quantifiers_normalized_print_slice_covers_core_quantifier_types() -> None:
    text = _text()

    for required in (
        "# Universal quantification",
        "# Existential / partitive-like quantification",
        "# Negative quantifiers and negation",
        "# Quantity expressions",
        "# Boundary with numerals",
        "# Boundary with NP structure and negation",
        "# Deferred material",
        "khempeuh",
        "pawlkhat",
        "kuamah",
        "bangmah",
        "tampi",
    ):
        assert required in text


def test_quantifiers_normalized_print_slice_keeps_boundaries_explicit() -> None:
    text = _text()

    for required in (
        "Boundary with numerals",
        "Boundary with NP structure and negation",
        "khat",
        "negation licensing",
        "indefinite-like",
        "noun phrase",
        "deferred",
    ):
        assert required in text


def test_quantifiers_normalized_print_slice_has_old_testament_and_gospel_examples() -> None:
    text = _text()

    assert "Genesis 2:1" in text or "Genesis 32:24" in text or "Exodus 2:12" in text
    assert "Luke 2:1" in text or "Matthew 2:1" in text or "Mark 6:34" in text or "John 3:27" in text or "no suitable Gospel example was found" in text


def test_quantifiers_normalized_print_slice_avoids_raw_report_counts() -> None:
    text = _text()

    for forbidden in ("5,191", "4,712", "3,021", "2,244", "1,100"):
        assert forbidden not in text


def test_quantifiers_normalized_print_slice_keeps_caveats_and_deferred() -> None:
    text = _text()

    assert "Deferred material" in text
    assert any(phrase in text for phrase in (
        "does not yet settle",
        "remains",
        "deferred",
        "boundary",
        "construction-sensitive",
    ))
    assert "with caveat" in text


def test_quantifiers_normalization_supplement_exists_and_has_required_columns() -> None:
    assert SUPPLEMENT.exists(), "Quantifier normalization supplement must exist"

    with SUPPLEMENT.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    assert "source_zone" in reader.fieldnames
    assert "example_quality" in reader.fieldnames
    assert any(row["source_zone"] == "Old Testament" for row in rows)
    assert any(row["source_zone"] == "Gospels" for row in rows)
    assert all(row["print_status"] != "print_ready" or row["example_quality"] in {"high", "medium"} for row in rows)
