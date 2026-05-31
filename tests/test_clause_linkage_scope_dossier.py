from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_clause_linkage_scope.md"
USER_RELATIVE_PATH = ROOT / "docs/grammar/reports/08-clause-03-relative-clauses.md"
REPO_RELATIVE_PATH = ROOT / "docs/grammar/reports/08-clause-03-relatives.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_clause_linkage_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "Clause-linkage scope dossier must exist"


def test_clause_linkage_scope_dossier_names_selection_and_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "review_notes_prefix_agreement.md",
        "docs/grammar/reports/08-clause-01-subordination.md",
        "docs/grammar/reports/08-clause-02-switch-reference.md",
        "docs/grammar/lit-reviews/08-clause-03-subordination-lit.md",
    ):
        assert required in text


def test_clause_linkage_scope_dossier_handles_relative_report_path_explicitly() -> None:
    text = _text()
    lower = text.lower()

    assert not USER_RELATIVE_PATH.exists()
    assert REPO_RELATIVE_PATH.exists()
    assert "08-clause-03-relative-clauses.md" in text
    assert "08-clause-03-relatives.md" in text
    assert "absent" in lower
    assert "rather than inventing a missing source" in lower


def test_clause_linkage_scope_dossier_names_boundaries_and_status() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "review_notes_sentence_final_particles.md",
        "review_notes_tam.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text

    assert "candidate/scoping pass" in lower
    assert "not a grammar print slice" in lower
    assert "grammar, dictionary, and review-note slices for clause linkage do **not** yet exist" in lower
