from __future__ import annotations

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


def test_np_possession_normalized_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_np_possession.tsv",
        "dossier_np_possession.md",
        "review_notes_np_possession.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
    ):
        assert required in text


def test_np_possession_normalized_print_slice_has_inventory_and_safe_anchors() -> None:
    text = _text()

    assert "| Pattern | Example form | Rough function | Current print status | Main boundary issue |" in text

    for required in (
        "hih mite",
        "mi khat",
        "mi khempeuh",
        "mi pawlkhat",
        "mi tampi",
        "ni li",
        "kum sawm le nih",
    ):
        assert required in text


def test_np_possession_normalized_print_slice_discusses_required_domains() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Deferred and boundary material",
    ):
        assert required in text

    assert "noun-plus-numeral order" in lower
    assert "noun-plus-quantifier" in lower
    assert "demonstrative-before-noun" in lower
    assert "candidate evidence" in lower
    assert "explicit caveats" in lower


def test_np_possession_normalized_print_slice_keeps_possession_cautious() -> None:
    text = _text()
    lower = text.lower()

    assert "no equally clean gospel possession row was found" in lower
    assert "do not yet justify a full paradigm of possessive prefixes" in lower
    assert "full possession paradigm is still deferred" in lower


def test_np_possession_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    assert text.count("(@ex:np-") >= 4
    assert "Exodus 5:5" in text
    assert "Genesis 24:23" in text
    assert "John 11:39" in text
    assert "Luke 2:1" in text


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
