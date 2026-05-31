from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_derivation_valency_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_derivation_valency_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "Derivation / valency scope dossier must exist"


def test_derivation_valency_scope_dossier_names_selection_and_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "review_notes_vp_structure_stacking.md",
        "docs/grammar/reports/05-verb-08-derivational.md",
        "docs/grammar/reports/05-verb-09-valency.md",
        "docs/grammar/reports/05-verb-10-combinations.md",
        "docs/grammar/reports/05-verb-12-transitivity.md",
        "docs/grammar/morphemes/06-derivational.md",
        "docs/grammar/lit-reviews/05-verb-09-valency-lit.md",
        "tests/test_sak_caus_benf.py",
        "tests/test_vp_slots.py",
    ):
        assert required in text


def test_derivation_valency_scope_dossier_names_boundary_controls() -> None:
    text = _text()

    for required in (
        "review_notes_vp_structure_stacking.md",
        "review_notes_tam.md",
        "review_notes_directionals.md",
        "review_notes_negation.md",
        "review_notes_pronouns.md",
        "tests/test_prefix_agr_poss.py",
    ):
        assert required in text


def test_derivation_valency_scope_dossier_is_scoping_not_print_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate/scoping pass" in lower
    assert "not a grammar print slice" in lower
    assert "not a full verbal morphology chapter" in lower
    assert "grammar, dictionary, and review-note slices for derivation/valency do **not** yet exist" in lower


def test_derivation_valency_scope_dossier_covers_main_candidate_groups() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "`-sak`",
        "`-pih`",
        "`ki-`",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "piangsak",
    ):
        assert required in text

    assert "narrow `-sak` grammar slice" in lower
    assert "causative" in lower
    assert "benefactive" in lower
    assert "applicative" in lower
    assert "reflexive" in lower
