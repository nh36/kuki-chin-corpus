from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_derivation_valency.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_derivation_valency_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Derivation / valency review notes must exist"


def test_derivation_valency_review_notes_name_control_and_support_files() -> None:
    text = _text()

    for required in (
        "candidates_derivation_valency.tsv",
        "dossier_derivation_valency_scope.md",
        "grammar_derivation_valency_print_slice.md",
        "docs/grammar/reports/05-verb-08-derivational.md",
        "docs/grammar/reports/05-verb-09-valency.md",
        "docs/grammar/morphemes/06-derivational.md",
        "docs/grammar/lit-reviews/05-verb-09-valency-lit.md",
        "tests/test_sak_caus_benf.py",
    ):
        assert required in text


def test_derivation_valency_review_notes_name_boundary_controls() -> None:
    text = _text()

    for required in (
        "review_notes_vp_structure_stacking.md",
        "review_notes_tam.md",
        "review_notes_directionals.md",
        "review_notes_pronouns.md",
        "tests/test_vp_slots.py",
        "tests/test_prefix_agr_poss.py",
    ):
        assert required in text


def test_derivation_valency_review_notes_keep_sak_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "paisak" in text
    assert "causative `-sak` anchor" in lower
    assert "muhsak" in text
    assert "benefactive or applicative-like `-sak` split row" in lower
    assert "Form I plus `-sak`" in text
    assert "Form II plus `-sak`" in text
    assert "two readings of one suffix or two editorial subsections" in lower


def test_derivation_valency_review_notes_explain_no_dictionary_slice() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no dictionary slice yet" in lower
    assert "`-sak` lexical treatment should wait for human/editorial review" in lower
    assert "ready for human review at its current `-sak` slice maturity level" in lower


def test_derivation_valency_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "paipih",
        "kisep",
        "kigen",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "piangsak",
        "mipihte",
    ):
        assert required in text

    assert "not provide a full derivation chapter" in lower
    assert "not provide a full valency chapter" in lower
    assert "not provide a full verbal morphology chapter" in lower
    assert "pronominal prefixes / agreement / object-prefix systems" in lower

