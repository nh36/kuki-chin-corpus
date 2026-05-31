from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_nominalization_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_nominalization_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Nominalization grammar slice must exist"


def test_nominalization_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_nominalization.tsv",
        "dossier_nominalization_scope.md",
        "docs/grammar/reports/07-nmlz-01-deverbal.md",
        "docs/grammar/morphemes/06-derivational.md",
        "docs/grammar/grammar_source_map.json",
        "docs/SKELETON_GRAMMAR.md",
        "candidates_clause_linkage.tsv",
        "review_notes_clause_linkage.md",
        "review_notes_case_marking.md",
        "review_notes_derivation_valency.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_nominalization_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "`-na` is the clearest productive deverbal nominalizer" in text or "-na is the clearest productive deverbal nominalizer" in lower
    assert "bawlna" in text
    assert "bawl-na" in text
    assert "make-NMLZ" in text
    assert "productive deverbal nominalization" in lower


def test_nominalization_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "bawlpa",
        "hong pai mi",
        "omna",
        "muhna-ah",
        "kumpipa",
        "Topa",
        "a bawl mi",
        "bare `na`",
        "report-only counts",
    ):
        assert required in text

    assert "stays outside" in lower or "stay outside" in lower or "boundary material" in lower


def test_nominalization_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full nominalization chapter" in lower
    assert "not a full derivation chapter" in lower
    assert "not a full relative-clause chapter" in lower
    assert "not a full case-routing chapter" in lower
    assert "nominalization review notes rather than a dictionary slice" in lower
    assert "dictionary slice now exists" not in lower
    assert "review-note slices already exist" not in lower
