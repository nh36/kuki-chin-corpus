from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_transitivity_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_transitivity_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Transitivity grammar slice must exist"


def test_transitivity_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert "# Editorial scope" not in text
    assert "current transitivity inventory" in lower
    assert "candidates_transitivity.tsv" not in text
    assert "dossier_transitivity_scope.md" not in text


def test_transitivity_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "sih" in text
    assert "suak" in text
    assert "hawl" in text
    assert "en" in text
    assert "full verb-class inventory" in lower or "full verb-class chapter" in lower
    assert "argument-structure chapter" in lower


def test_transitivity_print_slice_keeps_boundary_material_visible() -> None:
    text = _text()

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
        "ki-",
        "pia(k)sak",
    ):
        assert required in text
