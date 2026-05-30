from pathlib import Path


DOSSIER_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/dossier_tam_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_tam_scope_dossier_exists_and_names_sources() -> None:
    text = _text()

    assert DOSSIER_PATH.exists()
    assert "docs/grammar/reports/05-verb-04-tam.md" in text
    assert "tests/test_habitual_markers.py" in text
    assert "tests/test_vp_slots.py" in text
    assert "docs/grammar/reports/05-verb-06-directional.md" in text
    assert "review_notes_directionals.md" in text


def test_tam_scope_dossier_keeps_candidate_layer_controlling_and_conservative() -> None:
    text = _text()

    assert "candidates_tam.tsv" in text
    assert "This dossier is therefore **not** a full TAM grammar slice." in text
    assert "Candidate rows, not generated-report raw counts and not a broad search over every TAM-looking suffix, control the dossier." in text
    assert "discovery source, not as finished print prose" in text


def test_tam_scope_dossier_separates_clean_candidates_from_overlap_and_deferred_material() -> None:
    text = _text()

    for heading in (
        "## Relatively clean TAM / aspect / modal candidates",
        "## Construction-bound or clause-position candidates",
        "## Forms overlapping with negation",
        "## Forms overlapping with sentence-final particles",
        "## Forms overlapping with directionals or VP-slot material",
        "## Deferred or not yet safe",
    ):
        assert heading in text


def test_tam_scope_dossier_names_clean_anchors_and_overlap_controls() -> None:
    text = _text()

    for required in (
        "paingei",
        "neigige",
        "paizel",
        "kilawmta",
        "bawlzo",
        "hongpaikik",
        "omding",
        "bawlthei",
        "pailai",
        "dingin",
        "khiathei ding om lo",
        "mangngilh ta hi",
        "khia-ta",
        "bawlzoding",
    ):
        assert required in text


def test_tam_scope_dossier_sets_next_scope_without_claiming_later_surfaces() -> None:
    text = _text()

    assert "The safest next print-facing sub-scope" in text
    assert "grammar_tam_print_slice.md" in text
    assert "dictionary_tam_print_slice.md" in text
    assert "review_notes_tam.md" in text
    assert "do **not** yet exist" in text
    assert "Grammar, dictionary, and review-note print slices for TAM have **not** yet begun." in text
