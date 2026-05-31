from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_np_possession.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_np_possession_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "NP structure / possession review notes must exist"


def test_np_possession_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_np_possession.tsv",
        "dossier_np_possession_scope.md",
        "grammar_np_possession_print_slice.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
        "review_notes_case_marking.md",
        "review_notes_relators_postpositions.md",
        "review_notes_nominalization.md",
        "tests/test_prefix_agr_poss.py",
    ):
        assert required in text


def test_np_possession_review_notes_keep_np_order_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "hih mite" in text
    assert "demonstrative-before-noun anchor" in lower
    assert "hih mi-te" in text
    assert "PROX person-PL" in text
    assert "mi khat" in text
    assert "head-noun plus numeral anchor" in lower
    assert "person one" in text
    assert "mi khempeuh" in text
    assert "head-noun plus quantifier anchor" in lower
    assert "mi khem-peuh" in text
    assert "person all" in text
    assert "candidate-controlled evidence for basic NP ordering" in text


def test_np_possession_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "structural/syntactic rather than lexical" in lower
    assert "ready for human review at its current basic-NP-ordering slice maturity level" in text


def test_np_possession_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "ka pa",
        "Topa' inn",
        "a pa' inn",
        "Topa' tungah",
        "ka suahna leitang",
        "isolated `a`, `ka`, or `na` prefix surfaces",
        "amah a pa",
        "`-á`",
        "report-only counts",
    ):
        assert required in text

    assert "not provide a full noun-phrase chapter" in lower
    assert "not provide a full possession chapter" in lower
    assert "not provide a full prefix/agreement chapter" in lower
    assert "not provide a full case or relator chapter" in lower
    assert "not provide a full recursive possession account" in lower
    assert "simple nouns / compounds / proper nouns" in text
