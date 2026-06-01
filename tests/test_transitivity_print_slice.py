from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_transitivity_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_transitivity_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Transitivity grammar slice must exist"


def test_transitivity_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_transitivity.tsv",
        "dossier_transitivity_scope.md",
        "docs/grammar/reports/05-verb-12-transitivity.md",
        "review_notes_derivation_valency.md",
        "review_notes_stem_alternation.md",
        "review_notes_prefix_agreement.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_tam.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_transitivity_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "sih" in text
    assert "clean intransitive anchor" in lower
    assert "sih / die" in text
    assert "suak" in text
    assert "supporting intransitive evidence" in lower
    assert "suak / become" in text
    assert "hawl" in text
    assert "clean transitive anchor" in lower
    assert "hawl / seek" in text
    assert "en" in text
    assert "supporting transitive evidence" in lower
    assert "en / look.at" in text


def test_transitivity_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

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
        "ki",
        "dawt",
        "bei",
        "pia(k)sak",
        "case-dominated rows",
        "derivation-heavy rows",
        "prefix/agreement-heavy rows",
        "analyzer-noisy, lexicalized, report-only, or whole-system verb-class claims",
    ):
        assert required in text

    assert "stay outside" in lower or "stays outside" in lower or "boundary material" in lower


def test_transitivity_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full valency chapter" in lower
    assert "not a full verb-class chapter" in lower
    assert "not a dictionary slice" in lower
    assert "not a full argument-structure account" in lower
    assert "dictionary_transitivity" not in lower
    assert "review_notes_transitivity" not in lower
