from pathlib import Path


SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/dictionary_tam_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_tam_dictionary_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()
    lower = text.lower()

    assert SLICE_PATH.exists()
    assert "candidates_tam.tsv" in text
    assert "dossier_tam_scope.md" in text
    assert "grammar_tam_print_slice.md" in text
    assert "analyzer dictionaries" in lower
    assert "machine dictionary files" in lower
    assert "not a machine-dictionary edit and not a full tam chapter" in lower


def test_tam_dictionary_slice_has_required_entry_headings_and_anchor_forms() -> None:
    text = _text()

    for heading in (
        "## `-ngei`",
        "## `-gige`",
        "## `-zel`",
        "## `-ta`",
        "## `-zo`",
        "## `-kik`",
        "## `-ding`",
        "## `-thei`",
    ):
        assert heading in text

    for anchor in (
        "paingei",
        "neigige",
        "paizel",
        "kilawmta",
        "bawlzo",
        "hongpaikik",
        "omding",
        "bawlthei",
    ):
        assert anchor in text


def test_tam_dictionary_slice_keeps_required_caveats_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "broader continuative aspect" in lower
    assert "construction-controlled" in lower
    assert "sentence-final overlap caveat" in lower
    assert "bare-`zo` and sentence-final overlap caveat" in text
    assert "motion/return chapter" in lower
    assert "`dingin` and clause-bound caveat" in text
    assert "negation/irrealis-stack caveat" in lower
    assert "khiathei ding om lo" in text


def test_tam_dictionary_slice_keeps_overlap_and_deferred_material_not_dictionary_ready() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "pailai",
        "dingin",
        "khiathei ding om lo",
        "mangngilh ta hi",
        "khia-ta",
        "bawlzoding",
        "bawlsakthei",
        "`-nawn`",
        "`-khin`",
    ):
        assert required in text

    assert "not dictionary-ready" in lower
    assert "deferred" in lower


def test_tam_dictionary_slice_does_not_claim_review_notes_exist() -> None:
    text = _text()
    lower = text.lower()

    assert "review-note work for TAM has not yet begun" in text
    assert "review_notes_tam.md" in text
    assert "review notes now exist" not in lower
