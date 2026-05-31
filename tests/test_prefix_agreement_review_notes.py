from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_prefix_agreement.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_prefix_agreement_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Prefix/agreement review notes must exist"


def test_prefix_agreement_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_prefix_agreement.tsv",
        "dossier_prefix_agreement_scope.md",
        "grammar_prefix_agreement_print_slice.md",
        "docs/grammar/reports/05-verb-03-agreement.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/DISAMBIGUATION.md",
        "tests/test_prefix_agr_poss.py",
        "review_notes_pronouns.md",
        "review_notes_derivation_valency.md",
        "review_notes_vp_structure_stacking.md",
    ):
        assert required in text


def test_prefix_agreement_review_notes_keep_routing_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "kanei" in text
    assert "verbal agreement anchor" in lower
    assert "kainn" in text
    assert "nominal possessive-routing anchor" in lower
    assert "ka-nei" in text
    assert "1SG-have" in text
    assert "ka-inn" in text
    assert "1SG.POSS-house" in text
    assert "agreement-versus-possession routing contrast" in lower


def test_prefix_agreement_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "routing/analysis-based rather than lexical" in lower
    assert "ready for human review at its current routing-slice maturity level" in lower


def test_prefix_agreement_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "ainn",
        "ipai",
        "hongmu",
        "kongmu",
        "kipan",
        "apostrophe possession",
        "broader possessor syntax",
    ):
        assert required in text

    assert "not provide a full agreement chapter" in lower
    assert "not provide a full possession chapter" in lower
    assert "not provide a full object-prefix or inverse chapter" in lower
    assert "not provide a full pronoun chapter" in lower
    assert "not provide a full prefix paradigm" in lower
    assert "clause linkage: subordination / switch reference / relative clauses" in lower
