from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = REPO_ROOT / "output" / "publication_review" / "dossier_reduplication_scope.md"


def test_reduplication_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_reduplication_scope_dossier_names_required_sources() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for required in (
        "output/publication_review/whole_grammar_coverage_audit.md",
        "output/publication_review/review_notes_noun_domain.md",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/SKELETON_GRAMMAR.md",
        "docs/grammar/grammar_source_map.json",
        "docs/grammar/reports/07-deriv-02-reduplication.md",
        "output/publication_review/review_notes_derivation_valency.md",
        "output/publication_review/review_notes_nominalization.md",
        "output/publication_review/review_notes_vp_structure_stacking.md",
        "output/publication_review/review_notes_noun_domain.md",
        "output/publication_review/review_notes_tam.md",
    ):
        assert required in text


def test_reduplication_scope_dossier_describes_current_packet_stage() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8").lower()

    assert "first candidate/scoping pass" in text
    assert "not a grammar print slice" in text
    assert "not a dictionary slice" in text
    assert "not a full derivation chapter" in text
    assert "grammar_reduplication_print_slice.md" in text
    assert "dictionary and review-note slices do not yet exist for reduplication" in text


def test_reduplication_scope_dossier_keeps_clean_and_boundary_rows_visible() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for required in (
        "mahmah",
        "taktak",
        "peuhpeuh",
        "ni ni",
        "leuleu",
        "gengen",
        "kawikawi",
        "theithei",
        "narrow grammar print slice",
        "grammar_reduplication_print_slice.md",
    ):
        assert required in text
