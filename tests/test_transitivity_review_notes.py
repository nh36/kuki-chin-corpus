from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_transitivity.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_transitivity_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Transitivity review notes must exist"


def test_transitivity_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_transitivity.tsv",
        "dossier_transitivity_scope.md",
        "grammar_transitivity_print_slice.md",
        "docs/grammar/reports/05-verb-12-transitivity.md",
        "review_notes_derivation_valency.md",
        "review_notes_stem_alternation.md",
        "review_notes_prefix_agreement.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_tam.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_transitivity_review_notes_keep_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate TSV" in text
    assert "scoping dossier" in lower
    assert "narrow grammar print slice" in lower
    assert "tests" in lower
    assert "sih" in text
    assert "clean intransitive anchor" in lower
    assert "sih / die" in text
    assert "suak" in text
    assert "supporting intransitive evidence" in lower
    assert "suak / become" in text
    assert "hawl" in text
    assert "clean transitive anchor" in lower
    assert "hawl / seek" in text
    assert "en" in text
    assert "supporting transitive evidence" in lower
    assert "en / look.at" in text
    assert "candidate-controlled evidence for a narrow intransitive/transitive contrast" in text


def test_transitivity_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "grammar-facing and argument-structure-oriented packet rather than a lexical-headword packet" in lower


def test_transitivity_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "mu / muh",
        "za / zak",
        "nei / neih",
        "ngai / ngaih",
        "piangsak",
        "pia",
        "gen",
        "tom",
        "hong",
        "ki",
        "dawt",
        "bei",
        "pia(k)sak",
        "case-dominated rows",
        "derivation-heavy rows",
        "prefix/agreement-heavy rows",
        "analyzer-noisy, lexicalized, report-only, or whole-system verb-class claims",
    ):
        assert required in text

    assert "full transitivity chapter" in lower
    assert "full valency chapter" in lower
    assert "full verb-class chapter" in lower
    assert "full argument-structure account" in lower
    assert "dictionary slice" in lower
    assert "whole-system treatment of labile/ambitransitive behavior" in lower


def test_transitivity_review_notes_recommend_second_checkpoint() -> None:
    text = _text()
    lower = text.lower()

    assert "ready for human review at its current clean-contrast slice maturity level" in text
    assert "second whole-grammar coverage checkpoint after transitivity" in lower
    assert "report-backed non-blocked domains remain unpacketized after transitivity" in lower
