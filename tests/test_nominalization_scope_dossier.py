from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_nominalization_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_nominalization_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "Nominalization scope dossier must exist"


def test_nominalization_scope_dossier_names_selection_and_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "review_notes_clause_linkage.md",
        "docs/grammar/reports/07-nmlz-01-deverbal.md",
        "docs/grammar/morphemes/06-derivational.md",
    ):
        assert required in text


def test_nominalization_scope_dossier_names_boundaries_and_status() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "candidates_clause_linkage.tsv",
        "review_notes_clause_linkage.md",
        "review_notes_case_marking.md",
        "review_notes_derivation_valency.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text

    assert "candidate/scoping pass" in lower
    assert "not a grammar print slice" in lower
    assert "grammar, dictionary, and review-note slices for nominalization do **not** yet exist" in lower
