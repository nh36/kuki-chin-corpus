from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_relators_postpositions_scope.md"


def _text() -> str:
    return DOSSIER_PATH.read_text(encoding="utf-8")


def test_relators_postpositions_scope_dossier_exists_and_names_sources() -> None:
    text = _text()

    assert DOSSIER_PATH.exists()
    assert "docs/grammar/reports/03-noun-04-relators.md" in text
    assert "docs/grammar/reports/03-noun-05-postpositions.md" in text


def test_relators_postpositions_scope_dossier_names_case_marking_boundary_control() -> None:
    text = _text()

    for required in (
        "candidates_case_marking.tsv",
        "dossier_case_marking.md",
        "grammar_case_marking_print_slice.md",
        "dictionary_case_markers_print_slice.md",
        "review_notes_case_marking.md",
    ):
        assert required in text


def test_relators_postpositions_scope_dossier_keeps_candidate_layer_controlling() -> None:
    text = _text()
    lower = text.lower()

    assert "candidates_relators_postpositions.tsv" in text
    assert "This dossier is therefore **not** a grammar print slice." in text
    assert "generated reports are discovery sources only" in lower
    assert "Candidate rows, not generated-report raw counts" in text
    assert "grammar_relators_postpositions_print_slice.md" in text


def test_relators_postpositions_scope_dossier_distinguishes_relator_nouns_from_postpositions() -> None:
    text = _text()

    for heading in (
        "# Relator-noun candidates",
        "# Postposition candidates",
        "# Case-marking boundary",
        "# Deferred or boundary material",
        "# Safest next print-facing sub-scope",
    ):
        assert heading in text

    for required in (
        "kiang",
        "lak",
        "sung",
        "tung",
        "pualam",
        "nuai",
        "mai",
        "pan",
        "panin",
        "tawh",
        "tawhin",
    ):
        assert required in text


def test_relators_postpositions_scope_dossier_does_not_claim_later_surfaces_exist() -> None:
    text = _text()
    lower = text.lower()

    assert "have **not** yet begun" in text
    assert "dictionary_relators_postpositions_print_slice.md" in text
    assert "review_notes_relators_postpositions.md" in text
    assert "ready for human review" not in lower


def test_relators_postpositions_scope_dossier_sets_dictionary_slice_as_next_step() -> None:
    text = _text()

    assert "first narrow grammar print slice for relators/postpositions now exists" in text
    assert "The next step should therefore be a relators/postpositions dictionary print slice" in text
