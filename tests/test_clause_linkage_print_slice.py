from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_clause_linkage_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_clause_linkage_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Clause-linkage grammar slice must exist"


def test_clause_linkage_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_clause_linkage.tsv",
        "dossier_clause_linkage_scope.md",
        "docs/grammar/reports/08-clause-01-subordination.md",
        "docs/grammar/reports/08-clause-02-switch-reference.md",
        "docs/grammar/reports/08-clause-03-relatives.md",
        "docs/grammar/lit-reviews/08-clause-03-subordination-lit.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_tam.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_clause_linkage_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "ciangin" in text
    assert "temporal subordination anchor" in lower
    assert "dingin" in text
    assert "caveated purposive or clause-bound irrealis overlap row" in lower
    assert "tua ciangin" in text
    assert "ciang-in" in text


def test_clause_linkage_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "VERB-in",
        "ngenin",
        "ahih ciangin",
        "a bawl mi",
        "omna",
        "muhna-ah",
        "leh",
        "hangin",
        "bangin",
    ):
        assert required in text

    assert "stays outside" in lower or "stay outside" in lower or "candidate-layer material" in lower
    assert "report-only relative-clause counts involving `a-`" in text


def test_clause_linkage_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full complex-sentence chapter" in lower
    assert "not a full switch-reference chapter" in lower
    assert "not a full relative-clause chapter" in lower
    assert "no dictionary slice exists yet for clause linkage" in lower
    assert "clause-linkage review notes rather than a dictionary slice" in lower
    assert "dictionary slice now exists" not in lower
    assert "review-note slices already exist" not in lower
