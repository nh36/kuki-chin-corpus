from pathlib import Path


GRAMMAR_PATH = Path("output/publication_review/grammar_case_marking_print_slice.md")
SUPPLEMENT_PATH = Path("output/publication_review/examples_case_marking_normalization.tsv")


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_case_marking_normalized_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "grammar_case_marking_print_slice.md must exist"


def test_case_marking_normalized_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_case_marking.tsv",
        "dossier_case_marking.md",
        "review_notes_case_marking.md",
        "examples_case_marking_normalization.tsv",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/grammar/morphemes/02-case-markers.md",
        "docs/grammar/lit-reviews/03-noun-05-postpositions-lit.md",
        "docs/grammar/reports/03-noun-04-relators.md",
        "docs/grammar/reports/03-noun-05-postpositions.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/reports/05-verb-12-transitivity.md",
        "output/grammar/case_marking_report.md",
    ):
        assert required in text


def test_case_marking_normalized_print_slice_has_inventory_and_supported_markers() -> None:
    text = _text()

    assert "| Marker or pattern | Rough function | Example context | Current print status | Main boundary issue |" in text

    for required in ("-ah", "-in", "-pan", "-panin", "-tawh", "na pa' inn-ah", "lakpan"):
        assert required in text


def test_case_marking_normalized_print_slice_discusses_required_domains() -> None:
    text = _text()
    lower = text.lower()

    for heading in (
        "# Overview of case-like marking",
        "# Current case-marking inventory",
        "# Locative and goal marking with -ah",
        "# Agentive, ergative, or instrumental marking with -in",
        "# Genitive / possessive boundary",
        "# Case marking and relators/postpositions",
        "# Case marking and argument structure",
        "# Deferred and boundary material",
    ):
        assert heading in text

    assert "ciangin" in lower
    assert "candidate evidence" in lower
    assert "explicit caveat" in lower or "explicit caveats" in lower
    assert "not yet enough for a full case paradigm" in lower
    assert "raw generated-report counts" in lower


def test_case_marking_normalized_print_slice_keeps_claims_cautious() -> None:
    lower = _text().lower()

    assert "does not settle whether the apostrophe" in lower
    assert "does not **not**" not in lower
    assert "full case paradigm" in lower
    assert "report-only" in lower or "raw report-only" in lower
    assert "raw `-in`" in _text() or "raw -in" in lower


def test_case_marking_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    assert text.count("(@ex:case-") >= 4
    assert "Genesis " in text or "Exodus " in text
    assert any(gospel in text for gospel in ("Matthew ", "Mark ", "Luke ", "John "))


def test_case_marking_normalized_print_slice_avoids_raw_count_promotion() -> None:
    lower = _text().lower()

    assert "12x" not in lower
    assert "24x" not in lower
    assert "report frequency" not in lower
    assert "frequency table" not in lower


def test_case_marking_examples_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists(), "examples_case_marking_normalization.tsv must exist"

    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "case_topic",
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


def test_case_marking_examples_supplement_includes_ot_and_gospel_rows() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8")

    assert "\tOld Testament\t" in text
    assert "\tGospels\t" in text


def test_case_marking_examples_supplement_does_not_mark_unvetted_rows_print_ready() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8").lower()

    assert "raw hit" not in text
    assert "report-only\tprint-ready" not in text
