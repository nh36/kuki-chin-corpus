from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_derivation_valency_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_derivation_valency_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Derivation / valency grammar slice must exist"


def test_derivation_valency_print_slice_names_control_and_support_sources() -> None:
    text = _text()

    for required in (
        "candidates_derivation_valency.tsv",
        "dossier_derivation_valency_scope.md",
        "docs/grammar/reports/05-verb-08-derivational.md",
        "docs/grammar/reports/05-verb-09-valency.md",
        "docs/grammar/morphemes/06-derivational.md",
        "docs/grammar/lit-reviews/05-verb-09-valency-lit.md",
        "tests/test_sak_caus_benf.py",
    ):
        assert required in text


def test_derivation_valency_print_slice_keeps_sak_core_claim_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "paisak" in text
    assert "causative anchor" in lower
    assert "muhsak" in text
    assert "benefactive or applicative-like split row" in lower
    assert "Form I plus `-sak`" in text
    assert "Form II plus `-sak`" in text
    assert "two readings of one suffix or two editorial subsections" in lower


def test_derivation_valency_print_slice_keeps_boundary_material_outside() -> None:
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

    assert "stay outside" in lower or "stays outside" in lower
    assert "tests/test_vp_slots.py" in text
    assert "tests/test_prefix_agr_poss.py" in text


def test_derivation_valency_print_slice_stays_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full derivation chapter" in lower
    assert "not a full valency chapter" in lower
    assert "not a full verbal morphology chapter" in lower
    assert "no dictionary slice exists yet for derivation/valency" in lower
    assert "review notes rather than a dictionary layer" in lower
    assert "dictionary slice now exists" not in lower
