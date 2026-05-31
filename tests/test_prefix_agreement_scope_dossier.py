from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_prefix_agreement_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_prefix_agreement_scope_dossier_exists() -> None:
    assert DOSSIER_PATH.exists(), "Prefix/agreement scope dossier must exist"


def test_prefix_agreement_scope_dossier_names_selection_and_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "review_notes_derivation_valency.md",
        "docs/grammar/reports/05-verb-03-agreement.md",
        "docs/grammar/reports/06-func-01-pronouns.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "docs/grammar/lit-reviews/06-func-01-pronouns-lit.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/DISAMBIGUATION.md",
        "tests/test_prefix_agr_poss.py",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_prefix_agreement_scope_dossier_names_main_candidate_groups() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "kanei",
        "kainn",
        "hongmu",
        "kongmu",
        "kipan",
        "ipai",
    ):
        assert required in lower

    assert "agreement-versus-possession routing grammar slice" in lower
    assert "hong-" in lower
    assert "kong-" in lower
    assert "ki-" in lower


def test_prefix_agreement_scope_dossier_stays_candidate_only() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate/scoping pass" in lower
    assert "rather than the print slice itself" in lower
    assert "grammar_prefix_agreement_print_slice.md" in text
    assert "not a rewrite of the completed pronouns/clusivity packet" in lower
    assert "dictionary and review-note slices for prefix/agreement do **not** yet exist" in lower
