from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_vp_structure_stacking_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_vp_structure_stacking_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "VP structure / stacking grammar slice must exist"


def test_vp_structure_stacking_print_slice_names_control_and_support_sources() -> None:
    text = _text()

    for required in (
        "candidates_vp_structure_stacking.tsv",
        "dossier_vp_structure_stacking_scope.md",
        "docs/grammar/reports/05-verb-02-vp-structure.md",
        "docs/grammar/reports/05-verb-10-combinations.md",
        "tests/test_vp_slots.py",
    ):
        assert required in text


def test_vp_structure_stacking_print_slice_names_boundary_controls() -> None:
    text = _text()

    for required in (
        "review_notes_tam.md",
        "review_notes_directionals.md",
        "review_notes_negation.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_relators_postpositions.md",
    ):
        assert required in text


def test_vp_structure_stacking_print_slice_keeps_bawlzoding_central() -> None:
    text = _text()
    lower = text.lower()

    assert "bawlzoding" in text
    assert "central first-slice stack" in lower
    assert "aspect plus irrealis stacking" in lower
    assert "verb stem + completive/aspectual material + irrealis/modal material" in text
    assert "aspectual material can precede irrealis/modal material" in lower
    assert "make-south-irr" in lower


def test_vp_structure_stacking_print_slice_keeps_boundaries_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "bawlzo" in text
    assert "pokhia" in text

    for required in (
        "khia-ta",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "khiathei ding om lo",
        "dingin",
    ):
        assert required in text

    assert "already owned by the tam packet" in lower
    assert "already owned by the directionals packet" in lower
    assert "derivation/valency-heavy stacks" in lower
    assert "tam-negation overlap" in lower
    assert "clause-bound irrealis or subordination material" in lower


def test_vp_structure_stacking_print_slice_stays_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full vp chapter" in lower
    assert "dictionary and review-note slices for vp structure / suffix stacking do not yet exist" in lower
    assert "dictionary slice now exists" not in lower
    assert "review notes now exist" not in lower

