from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = REPO_ROOT / "output" / "publication_review" / "grammar_reduplication_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_reduplication_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Reduplication grammar slice must exist"


def test_reduplication_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_reduplication.tsv",
        "dossier_reduplication_scope.md",
        "docs/grammar/reports/07-deriv-02-reduplication.md",
        "review_notes_derivation_valency.md",
        "review_notes_nominalization.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_noun_domain.md",
        "review_notes_tam.md",
    ):
        assert required in text


def test_reduplication_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

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


def test_reduplication_print_slice_keeps_boundary_material_outside() -> None:
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
        "Any broad derivation chapter claim",
        "Any dictionary-entry claim",
    ):
        assert required in text

    assert "stay outside" in lower or "stays outside" in lower or "boundary material" in lower


def test_reduplication_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full derivation chapter" in lower
    assert "not a full reduplication chapter" in lower
    assert "not a dictionary slice" in lower
    assert "not a tam/aspect or vp-structure slice" in lower
    assert "dictionary slice now exists" not in lower
    assert "review_notes_reduplication.md" in text
