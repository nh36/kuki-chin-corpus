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


def test_numerals_normalized_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_numerals.tsv",
        "dossier_numerals.md",
        "review_notes_numerals.md",
    ):
        assert required in text


def test_numerals_normalized_print_slice_replaces_stale_packet_state_prose() -> None:
    lower = _text().lower()

    assert "dictionary and review-note slices have not yet begun" not in lower
    assert "normalized publication-facing numerals section" in lower


def test_numerals_normalized_print_slice_includes_base_inventory_table() -> None:
    text = _text()
    lower = text.lower()

    assert "| Value | Form | Current status in this section |" in text
    for form in (
        "khat",
        "nih",
        "thum",
        "li",
        "nga",
        "guk",
        "sagih",
        "giat",
        "kua",
        "sawm",
        "za",
        "sing",
        "tul",
    ):
        assert form in lower


def test_numerals_normalized_print_slice_covers_required_topics() -> None:
    text = _text()
    lower = text.lower()

    assert "Decimal composition" in text
    assert "Ordinals" in text
    assert "nihna" in lower
    assert "sawmvei" in lower
    assert "mi khat" in lower
    assert "kua" in lower
    assert "nine" in lower
    assert "who" in lower
    assert "Distributive numerals" in text
    assert "sagih sagih" in lower
    assert "deferred" in lower


def test_numerals_normalized_print_slice_contains_multiple_formal_examples() -> None:
    examples = _examples()

    assert len(examples) >= 4
    assert any(source.startswith("Genesis") for _, source in examples)
    assert any(source.startswith(("Matthew", "Mark", "Luke", "John")) for _, source in examples)


def test_numerals_normalized_print_slice_uses_old_testament_and_gospel_examples_or_explicit_note() -> None:
    text = _text()
    examples = _examples()
    has_ot = any(source.startswith("Genesis") for _, source in examples)
    has_gospel = any(source.startswith(("Matthew", "Mark", "Luke", "John")) for _, source in examples)

    assert has_ot
    assert has_gospel or "no suitable Gospel" in text


def test_numerals_normalized_print_slice_avoids_raw_generated_report_counts() -> None:
    text = _text()
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x", "Corpus Count", "Total numeral tokens"):
        assert banned not in text
    assert "candidate evidence" in lower
    assert "explicit caveats" in lower or "caveat" in lower


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
