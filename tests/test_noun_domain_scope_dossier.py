from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = REPO_ROOT / "output" / "publication_review" / "dossier_noun_domain_scope.md"


def test_noun_domain_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_noun_domain_scope_dossier_names_required_sources() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for required in (
        "output/publication_review/whole_grammar_coverage_audit.md",
        "output/publication_review/review_notes_np_possession.md",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/SKELETON_GRAMMAR.md",
        "docs/grammar/grammar_source_map.json",
        "docs/grammar/reports/03-noun-01-simple.md",
        "docs/grammar/reports/03-noun-02-compounds.md",
        "docs/grammar/reports/03-noun-03-proper.md",
        "docs/grammar/compound_transparency_audit.md",
        "docs/grammar/opaque_lexemes.md",
        "output/publication_review/review_notes_np_possession.md",
        "output/publication_review/review_notes_nominalization.md",
        "output/publication_review/review_notes_relators_postpositions.md",
        "output/publication_review/review_notes_case_marking.md",
        "output/publication_review/review_notes_pronouns.md",
    ):
        assert required in text


def test_noun_domain_scope_dossier_describes_current_packet_stage() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8").lower()

    assert "first candidate/scoping pass" in text
    assert "not a grammar print slice" in text
    assert "not a dictionary slice" in text
    assert "not a full noun chapter" in text
    assert "grammar_noun_domain_print_slice.md" in text
    assert "dictionary and review-note slices do not yet exist for the noun domain" in text


def test_noun_domain_scope_dossier_recommends_simple_noun_stems_next() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "simple noun stem" in text
    assert "grammar_noun_domain_print_slice.md" in text
    assert "gam" in text
    assert "aksi / aksi-te" in text
    assert "minam" in text
    assert "thugen" in text
    assert "Abraham" in text
