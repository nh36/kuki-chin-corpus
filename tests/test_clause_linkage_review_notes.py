from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_clause_linkage.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_clause_linkage_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Clause-linkage review notes must exist"


def test_clause_linkage_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_clause_linkage.tsv",
        "dossier_clause_linkage_scope.md",
        "grammar_clause_linkage_print_slice.md",
        "docs/grammar/reports/08-clause-01-subordination.md",
        "docs/grammar/reports/08-clause-02-switch-reference.md",
        "docs/grammar/reports/08-clause-03-relatives.md",
        "docs/grammar/lit-reviews/08-clause-03-subordination-lit.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_tam.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_clause_linkage_review_notes_keep_temporal_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "ciangin" in text
    assert "temporal subordination anchor" in lower
    assert "tua ciangin" in text
    assert "ciang-in" in text
    assert "dingin" in text
    assert "caveated purposive or clause-bound irrealis overlap row" in lower
    assert "candidate-controlled evidence for temporal subordination" in lower


def test_clause_linkage_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "constructional/clausal rather than lexical" in lower
    assert "ready for human review at its current temporal-subordination slice maturity level" in lower


def test_clause_linkage_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "VERB-in",
        "ngenin",
        "ahih ciangin",
        "a bawl mi",
        "omna",
        "muhna-ah",
        "leh",
        "hangin",
        "bangin",
        "report-only relative-clause counts involving `a-`",
    ):
        assert required in text

    assert "not provide a full complex-sentence chapter" in lower
    assert "not provide a full switch-reference chapter" in lower
    assert "not provide a full relative-clause chapter" in lower
    assert "not provide a full subordination inventory" in lower
    assert "not provide a full account of nominalized clauses" in lower
    assert "nominalization" in lower
