from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_transitivity_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_transitivity_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "Transitivity scope dossier must exist"


def test_transitivity_scope_dossier_names_control_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_checkpoint_after_reduplication.md",
        "whole_grammar_coverage_audit.md",
        "docs/grammar/reports/05-verb-12-transitivity.md",
        "review_notes_derivation_valency.md",
        "review_notes_stem_alternation.md",
        "review_notes_prefix_agreement.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_tam.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_transitivity_scope_dossier_describes_candidate_stage_only() -> None:
    text = _text().lower()

    assert "first candidate/scoping pass" in text
    assert "not a grammar print slice" in text
    assert "not a dictionary slice" in text
    assert "not a full valency or verb-class chapter" in text
    assert "grammar, dictionary, and review-note slices do not yet exist for transitivity" in text


def test_transitivity_scope_dossier_keeps_candidate_groups_and_next_scope_visible() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "sih",
        "suak",
        "hawl",
        "mu / muh",
        "piangsak",
        "nei / neih",
        "hong",
        "ki",
    ):
        assert required in text

    assert "clean intransitive/transitive contrast" in lower
    assert "ambitransitive/labile" in lower
