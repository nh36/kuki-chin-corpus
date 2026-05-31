from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_nominalization.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_nominalization_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Nominalization review notes must exist"


def test_nominalization_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_nominalization.tsv",
        "dossier_nominalization_scope.md",
        "grammar_nominalization_print_slice.md",
        "docs/grammar/reports/07-nmlz-01-deverbal.md",
        "docs/grammar/morphemes/06-derivational.md",
        "docs/grammar/grammar_source_map.json",
        "docs/SKELETON_GRAMMAR.md",
        "candidates_clause_linkage.tsv",
        "review_notes_clause_linkage.md",
        "review_notes_case_marking.md",
        "review_notes_derivation_valency.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_nominalization_review_notes_keep_na_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "-na" in text
    assert "productive deverbal nominalization anchor" in lower
    assert "bawlna" in text
    assert "bawl-na" in text
    assert "make-NMLZ" in text
    assert "candidate-controlled evidence for productive deverbal nominalization with `-na`" in text or "candidate-controlled evidence for productive deverbal nominalization with `-na`" in lower


def test_nominalization_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "constructional/morphological rather than lexical" in lower
    assert "ready for human review at its current `-na` slice maturity level" in text


def test_nominalization_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "bawlpa",
        "hong pai mi",
        "omna",
        "muhna-ah",
        "kumpipa",
        "Topa",
        "a bawl mi",
        "bare `na`",
        "report-only counts",
    ):
        assert required in text

    assert "not provide a full nominalization chapter" in lower
    assert "not provide a full derivation chapter" in lower
    assert "not provide a full relative-clause chapter" in lower
    assert "not provide a full case-routing chapter" in lower
    assert "not provide a full agentive `-pa` / `-mi` treatment" in text
    assert "not provide a full nominalized-relative account" in lower
    assert "NP structure / possession" in text
