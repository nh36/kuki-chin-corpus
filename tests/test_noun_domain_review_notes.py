from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_noun_domain.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_noun_domain_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Noun-domain review notes must exist"


def test_noun_domain_review_notes_name_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_noun_domain.tsv",
        "dossier_noun_domain_scope.md",
        "grammar_noun_domain_print_slice.md",
        "docs/grammar/reports/03-noun-01-simple.md",
        "docs/grammar/reports/03-noun-02-compounds.md",
        "docs/grammar/reports/03-noun-03-proper.md",
        "docs/grammar/compound_transparency_audit.md",
        "docs/grammar/opaque_lexemes.md",
        "review_notes_np_possession.md",
        "review_notes_nominalization.md",
        "review_notes_relators_postpositions.md",
        "review_notes_case_marking.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_noun_domain_review_notes_keep_simple_noun_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "gam" in text
    assert "main simple free noun stem anchor" in lower
    assert "gam-te" in text
    assert "gam-'" in text
    assert "gam-in" in text
    assert "gam-ah" in text
    assert "gam-te-ah" in text
    assert "aksi / aksi-te" in text
    assert "supporting plural evidence" in lower
    assert "candidate-controlled evidence for simple free noun stems that can host ordinary plural and case-like marking" in text


def test_noun_domain_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice" in lower
    assert "grammar-facing rather than lexical" in lower
    assert "ready for human review at its current simple-noun-stem slice maturity level" in text


def test_noun_domain_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "minam",
        "thugen",
        "singnai",
        "lamethuai",
        "sanggam",
        "kholhna",
        "Abraham",
        "Topa",
        "Topa' inn",
        "pronoun-led possessors",
        "person-head material",
        "relator/postposition or case-dominated noun rows",
        "analyzer-noisy, report-only, or count-only noun-domain claims",
        "dictionary/chrestomathy routing claim",
        "reduplication",
    ):
        assert required in text

    assert "not provide a full noun chapter" in lower
    assert "not provide a full compound-noun chapter" in lower
    assert "not provide a full proper-noun chapter" in lower
    assert "not provide a full noun inflection chapter" in lower
    assert "not provide a dictionary slice" in lower
    assert "not provide a full chrestomathy/dictionary routing account" in lower
