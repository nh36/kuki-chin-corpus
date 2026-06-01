from pathlib import Path


GRAMMAR_PATH = Path("output/publication_review/grammar_noun_domain_print_slice.md")
SUPPLEMENT_PATH = Path("output/publication_review/examples_noun_domain_normalization.tsv")


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_noun_domain_normalized_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "grammar_noun_domain_print_slice.md must exist"


def test_noun_domain_normalized_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_noun_domain.tsv",
        "dossier_noun_domain.md",
        "review_notes_noun_domain.md",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/grammar/reports/03-noun-01-simple.md",
        "docs/grammar/reports/03-noun-02-compounds.md",
        "docs/grammar/reports/03-noun-03-proper.md",
        "docs/grammar/reports/03-noun-04-plural.md",
        "docs/grammar/reports/03-noun-05-nominalization.md",
    ):
        assert required in text


def test_noun_domain_normalized_print_slice_has_inventory_and_safe_anchors() -> None:
    text = _text()

    assert "| Form or pattern | Rough function | Example context | Current print status | Main boundary issue |" in text

    for anchor in ("gam", "aksi", "aksi-te", "mi", "mite"):
        assert anchor in text


def test_noun_domain_normalized_print_slice_discusses_required_domains() -> None:
    text = _text()

    for heading in (
        "# Simple noun stems",
        "# Plural marking with -te",
        "# Human nouns and common nouns",
        "# Nouns in larger phrases",
        "# Compounds and proper nouns",
        "# Nominalization boundary",
        "# Deferred and boundary material",
    ):
        assert heading in text

    lower = text.lower()
    assert "mi khat" in lower
    assert "mi khempeuh" in lower
    assert "mi pawlkhat" in lower
    assert "mi tampi" in lower
    assert "proper names" in lower
    assert "derived nouns and nominalized forms remain shared with the nominalization section" in lower


def test_noun_domain_normalized_print_slice_keeps_claims_cautious() -> None:
    lower = _text().lower()

    assert "candidate evidence" in lower
    assert "explicit caveat" in lower or "explicit caveats" in lower
    assert "not yet enough for a full noun-domain chapter" in lower
    assert "raw report-only noun lists" in lower


def test_noun_domain_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    assert text.count("(@ex:noun-") >= 4
    assert "Genesis " in text or "Exodus " in text
    assert any(gospel in text for gospel in ("Matthew ", "Mark ", "Luke ", "John "))


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


def test_noun_domain_examples_supplement_does_not_mark_unvetted_rows_print_ready() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8").lower()

    assert "raw hit" not in text
    assert "report-only\tprint-ready" not in text
