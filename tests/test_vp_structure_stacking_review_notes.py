from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_vp_structure_stacking.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_vp_structure_stacking_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "VP structure / stacking review notes must exist"


def test_vp_structure_stacking_review_notes_name_control_and_support_files() -> None:
    text = _text()

    for required in (
        "candidates_vp_structure_stacking.tsv",
        "dossier_vp_structure_stacking_scope.md",
        "grammar_vp_structure_stacking_print_slice.md",
        "docs/grammar/reports/05-verb-02-vp-structure.md",
        "docs/grammar/reports/05-verb-10-combinations.md",
        "tests/test_vp_slots.py",
    ):
        assert required in text


def test_vp_structure_stacking_review_notes_name_boundary_controls() -> None:
    text = _text()

    for required in (
        "review_notes_tam.md",
        "review_notes_directionals.md",
        "review_notes_negation.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_relators_postpositions.md",
    ):
        assert required in text


def test_vp_structure_stacking_review_notes_keep_bawlzoding_central() -> None:
    text = _text()
    lower = text.lower()

    assert "bawlzoding" in text
    assert "central print-usable-with-caveat anchor" in lower
    assert "verb stem + completive/aspectual material + irrealis/modal material" in text
    assert "make-south-irr" in lower
    assert "tests/test_vp_slots.py" in text
    assert "bawlzo" in text
    assert "pokhia" in text
    assert "already-owned baseline rows" in lower


def test_vp_structure_stacking_review_notes_keep_boundary_material_deferred() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "khia-ta",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "khiathei ding om lo",
        "dingin",
    ):
        assert required in text

    assert "tam/directional overlap" in lower
    assert "derivation/valency-heavy stacks" in lower
    assert "tam-negation overlap" in lower
    assert "clause-bound irrealis/subordination material" in lower
    assert "broad vp slot template" in lower


def test_vp_structure_stacking_review_notes_explain_no_dictionary_slice_and_next_domain() -> None:
    text = _text()
    lower = text.lower()

    assert "there is no ordinary dictionary slice yet because this packet is constructional rather than lexical" in lower
    assert "ready for human review at its current constructional maturity level" in lower
    assert "derivation / valency candidate scoping" in lower

