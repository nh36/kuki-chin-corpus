from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_reduplication.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_reduplication_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Reduplication review notes must exist"


def test_reduplication_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_reduplication.tsv",
        "dossier_reduplication_scope.md",
        "grammar_reduplication_print_slice.md",
        "docs/grammar/reports/07-deriv-02-reduplication.md",
        "review_notes_derivation_valency.md",
        "review_notes_nominalization.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_noun_domain.md",
        "review_notes_tam.md",
    ):
        assert required in text


def test_reduplication_review_notes_keep_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate TSV" in text
    assert "scoping dossier" in lower
    assert "narrow grammar print slice" in lower
    assert "tests" in lower
    assert "mahmah" in text
    assert "main full-reduplication intensifier anchor" in lower
    assert "mah~mah" in text
    assert "EMPH~EMPH / very, truly" in text
    assert "pha mahmah hi" in text
    assert "taktak" in text
    assert "closest support row" in lower
    assert "tak~tak" in text
    assert "TRUE~TRUE / truly, certainly" in text
    assert "peuhpeuh" in text
    assert "secondary distributive evidence" in lower
    assert "peuh~peuh" in text
    assert "each~each / every, each" in text
    assert "candidate-controlled evidence for full reduplication used in intensification" in text


def test_reduplication_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "grammar-facing and constructional packet rather than a lexical-headword packet" in lower


def test_reduplication_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "ni ni",
        "leuleu",
        "gengen",
        "kawikawi",
        "theithei",
        "bangbang",
        "bekbek",
        "zenzen",
        "tuamtuam",
        "analyzer-noisy, count-only, or theory-heavy whole-system claims",
        "broad derivation chapter claims",
        "dictionary-entry claims",
    ):
        assert required in text

    assert "full reduplication chapter" in lower
    assert "full derivation chapter" in lower
    assert "full tam/aspect account" in lower
    assert "full vp-structure account" in lower
    assert "dictionary slice" in lower
    assert "whole-system reduplication analysis" in lower


def test_reduplication_review_notes_recommend_coverage_checkpoint() -> None:
    text = _text()
    lower = text.lower()

    assert "ready for human review at its current full-reduplication-intensifier slice maturity level" in text
    assert "whole-grammar coverage checkpoint" in lower
    assert "rather than starting another new packet immediately" in lower
