from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_derivation_valency_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_derivation_valency_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Derivation / valency grammar slice must exist"


def test_derivation_valency_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert "# Editorial scope" not in text
    assert "current derivation / valency inventory" in lower
    assert "candidates_derivation_valency.tsv" not in text
    assert "dossier_derivation_valency_scope.md" not in text


def test_derivation_valency_print_slice_keeps_sak_core_claim_explicit() -> None:
    text = _text()

    assert "paisak" in text
    assert "muhsak" in text
    assert "Form I plus `-sak`" in text
    assert "Form II plus `-sak`" in text
    assert "final theoretical status of the split remains open" in text


def test_derivation_valency_print_slice_keeps_boundary_material_visible() -> None:
    text = _text()

    for required in (
        "paipih",
        "mipihte",
        "kisep",
        "kigen",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "piangsak",
    ):
        assert required in text
