from pathlib import Path


AUDIT_PATH = Path("output/publication_review/coverage_normalization_audit.md")


def _text() -> str:
    return AUDIT_PATH.read_text(encoding="utf-8")


def test_coverage_normalization_audit_exists() -> None:
    assert AUDIT_PATH.exists(), "Coverage normalization audit must exist"


def test_coverage_normalization_audit_names_controlling_sources() -> None:
    text = _text()

    for required in (
        "assembled_grammar_review_preview.md",
        "whole_grammar_coverage_checkpoint_after_transitivity.md",
        "whole_grammar_coverage_audit.md",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "SKELETON_GRAMMAR.md",
        "PROGRESS.md",
    ):
        assert required in text


def test_coverage_normalization_audit_defines_target_standard() -> None:
    text = _text()
    lower = text.lower()

    assert "Homogeneous target standard for normalized publication-facing sections" in text
    assert "a short overview of the category or construction" in lower
    assert "an inventory table or paradigm where appropriate" in lower
    assert "at least two good interlinear examples where the construction is common enough" in lower
    assert "balanced example sourcing where possible" in lower
    assert "an explicit boundary/deferred-material paragraph" in lower
    assert "citations to the main literature where available" in lower
    assert "no stale claims about packets not existing when they now exist" in lower
    assert "no raw generated-report counts promoted without candidate control" in lower


def test_coverage_normalization_audit_includes_example_selection_policy() -> None:
    text = _text()
    lower = text.lower()

    assert "Example selection policy" in text
    assert "The first criterion is how well the example illustrates the grammatical point." in text
    assert "The second criterion is source balance." in text
    assert "prefer at least one Old Testament example and one Gospel example" in text
    assert "Do not let the grammar become a grammar of Genesis" in text
    assert "Acts, Pauline letters, Catholic epistles, and Revelation are acceptable" in text
    assert "book, chapter, verse, broad source zone, and example-quality notes" in text
    for zone in (
        "Old Testament",
        "Gospels",
        "Acts",
        "Pauline letters",
        "Catholic epistles",
        "Revelation",
    ):
        assert zone in text
    assert "scripts/interlinear_latex.py" in text
    assert "divergent bible-book mapping" in lower


def test_coverage_normalization_audit_includes_required_table_columns() -> None:
    text = _text()

    for column in (
        "Grammar topic",
        "Current PDF section",
        "Upstream source reports/lit reviews",
        "Candidate/dossier layer exists?",
        "Grammar print slice exists?",
        "Review notes exist?",
        "Number of examples in current print slice",
        "Bible source distribution of examples",
        "Has table/paradigm?",
        "Current prose depth",
        "Main reason section is thin",
        "Expansion priority",
        "Recommended next action",
    ):
        assert column in text


def test_coverage_normalization_audit_treats_numerals_as_worked_case() -> None:
    text = _text()
    lower = text.lower()

    assert "Numerals as a worked diagnostic case" in text
    assert "docs/grammar/reports/06-func-03-numerals.md" in text
    assert "grammar_numerals_print_slice.md" in text
    assert "The numerals report is fuller than the current print slice." in text
    assert "The current numerals PDF section is mainly an underdeveloped print-slice problem, not an assembly problem." in text
    assert "Numerals is therefore the recommended pilot expansion target" in text
    assert "digits, tens/hundreds/thousands, compound formation, ordinals, classifiers, numeral syntax, distributive and multiplicative expressions, and large-number contexts" in lower


def test_coverage_normalization_audit_keeps_major_gaps_visible_and_non_final() -> None:
    text = _text()
    lower = text.lower()

    assert "Phonology / tone" in text
    assert "Verb paradigms" in text
    assert "major gap" in lower
    assert "does not claim that the grammar is finished" in lower
    assert "not a new grammar packet" in lower
