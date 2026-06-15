from __future__ import annotations

import csv
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_numerals_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_numerals_normalization.tsv"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _examples() -> list[tuple[str, str]]:
    text = _text()
    pattern = re.compile(r"^\(@ex:(num-[^)]+)\)(?:\s+(.+))?$", re.MULTILINE)
    return [(label, source or "") for label, source in pattern.findall(text)]


def test_numerals_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_numerals_normalized_print_slice_has_overview_and_inventory_table() -> None:
    text = _text()
    lower = text.lower()

    assert "Overview of the numeral system" in text
    assert "| Value | Numeral | Notes |" in text
    for form in ("khat", "nih", "thum", "li", "nga", "guk", "sagih", "giat", "kua", "sawm", "za", "sing", "tul"):
        assert form in lower


def test_numerals_normalized_print_slice_avoids_internal_packet_status_prose() -> None:
    lower = _text().lower()

    for banned in (
        "current packet",
        "print slice",
        "candidate layer",
        "the workflow",
        "this commit",
        "publication-review",
    ):
        assert banned not in lower


def test_numerals_normalized_print_slice_covers_required_grammar_topics() -> None:
    text = _text()
    lower = text.lower()

    assert "Compound numerals" in text
    assert "Noun-plus-numeral word order" in text
    assert "Ordinals and the `-na` boundary" in text
    assert "Multiplicative and counting expressions" in text
    assert "Ambiguity controls: `kua` and `khat`" in text
    assert "Deferred and boundary material" in text

    assert "kum sawmkua" in lower
    assert "kum sawm le nih" in lower
    assert "kum zakua le kum sawmguk le kua" in lower
    assert "kum nih" in lower
    assert "ni sagih" in lower
    assert "ni li" in lower
    assert "nihna" in lower
    assert "sawmvei" in lower
    assert "mi khat" in lower
    assert "kua" in lower
    assert "interrogative" in lower


def test_numerals_normalized_print_slice_contains_several_formal_examples() -> None:
    examples = _examples()

    assert len(examples) >= 7
    assert any(source.startswith("Genesis") for _, source in examples)
    assert any(source.startswith(("Matthew", "Mark", "Luke", "John")) for _, source in examples)


def test_numerals_normalized_print_slice_formal_examples_keep_all_interlinear_lines() -> None:
    lines = _text().splitlines()

    for index, line in enumerate(lines):
        if not line.startswith("(@ex:"):
            continue
        assert index + 4 < len(lines), f"Incomplete example block starting at: {line}"
        assert lines[index + 1].startswith("a. Tedim:"), f"Missing Tedim line after {line}"
        assert lines[index + 2].startswith("b. Segmentation:"), f"Missing segmentation line after {line}"
        assert lines[index + 3].startswith("c. Gloss:"), f"Missing gloss line after {line}"
        assert lines[index + 4].startswith("d. Translation:"), f"Missing translation line after {line}"


def test_numerals_normalized_print_slice_has_ot_and_gospel_coverage() -> None:
    text = _text()
    examples = _examples()
    has_ot = any(source.startswith("Genesis") for _, source in examples)
    has_gospel = any(source.startswith(("Matthew", "Mark", "Luke", "John")) for _, source in examples)

    assert has_ot
    assert has_gospel or "No equally clean Gospel example is currently used for this construction." in text


def test_numerals_normalized_print_slice_avoids_raw_generated_report_counts() -> None:
    text = _text()
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x", "Corpus Count", "Total numeral tokens"):
        assert banned not in text
    assert "decimal structure" in lower


def test_numerals_normalization_supplement_exists_and_has_required_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    assert "source_zone" in reader.fieldnames
    assert "example_quality" in reader.fieldnames
    assert any(row["source_zone"] == "Old Testament" for row in rows)
    assert any(row["source_zone"] == "Gospels" for row in rows)
    assert all(row["print_status"] in {"print_ready", "print_usable_with_caveat", "deferred"} for row in rows)
    assert not any(
        row["print_status"] == "print_ready" and "raw" in (row["why_selected"] + " " + row["caveat"]).lower()
        for row in rows
    )


def test_numerals_normalized_print_slice_keeps_required_boundary_paragraph() -> None:
    lower = _text().lower()

    assert "does not yet settle the full classifier system" in lower
    assert "full quantification patterns" in lower
    assert "indefinite-like uses of `khat`" in lower
    assert "interrogative-side `kua` behavior" in lower
    assert "broader np syntax" in lower
