from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = REPO_ROOT / "output" / "publication_review" / "dossier_np_possession_scope.md"


def test_np_possession_scope_dossier_exists():
    assert DOSSIER_PATH.exists()


def test_np_possession_scope_dossier_names_required_sources():
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for required in (
        "output/publication_review/whole_grammar_coverage_audit.md",
        "output/publication_review/review_notes_nominalization.md",
        "docs/grammar/grammar_source_map.json",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/SKELETON_GRAMMAR.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "output/publication_review/review_notes_prefix_agreement.md",
        "output/publication_review/review_notes_pronouns.md",
        "output/publication_review/review_notes_case_marking.md",
        "output/publication_review/review_notes_relators_postpositions.md",
        "output/publication_review/review_notes_nominalization.md",
        "tests/test_prefix_agr_poss.py",
    ):
        assert required in text


def test_np_possession_scope_dossier_is_candidate_scoping_only():
    text = DOSSIER_PATH.read_text(encoding="utf-8").lower()

    assert "first candidate/scoping pass" in text
    assert "not a grammar print slice" in text
    assert "grammar print slice now exists" in text
    assert "dictionary and review-note slices for np structure / possession do not yet exist" in text
    assert "not a full noun-phrase or possession chapter" in text


def test_np_possession_scope_dossier_recommends_basic_np_order_next():
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "basic NP ordering" in text
    assert "grammar_np_possession_print_slice.md" in text
    assert "hih mite" in text
    assert "mi khat" in text
    assert "mi khempeuh" in text
    assert "ka pa" in text
