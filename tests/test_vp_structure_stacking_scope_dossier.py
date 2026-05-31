from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_vp_structure_stacking_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_vp_structure_stacking_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "VP structure / stacking scope dossier must exist"


def test_vp_structure_stacking_scope_dossier_names_architecture_selection_and_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "docs/grammar/reports/05-verb-02-vp-structure.md",
        "docs/grammar/reports/05-verb-10-combinations.md",
        "tests/test_vp_slots.py",
        "docs/grammar/grammar_source_map.json",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/SKELETON_GRAMMAR.md",
    ):
        assert required in text


def test_vp_structure_stacking_scope_dossier_names_boundary_control_packets() -> None:
    text = _text()

    for required in (
        "candidates_tam.tsv",
        "dossier_tam_scope.md",
        "review_notes_tam.md",
        "candidates_directionals.tsv",
        "dossier_directionals.md",
        "review_notes_directionals.md",
        "review_notes_negation.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_relators_postpositions.md",
    ):
        assert required in text


def test_vp_structure_stacking_scope_dossier_is_scoping_not_print_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate/scoping pass" in lower
    assert "not a grammar print slice" in lower
    assert "not a full vp chapter" in lower
    assert "grammar, dictionary, and review-note print slices for vp structure/stacking do **not** yet exist" in lower


def test_vp_structure_stacking_scope_dossier_recommends_narrower_subset() -> None:
    text = _text()
    lower = text.lower()

    assert "bawlzoding" in text
    assert "narrower subset" in lower
    assert "narrow suffix stacking" in lower

