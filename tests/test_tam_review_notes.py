from pathlib import Path


NOTES_PATH = Path("output/publication_review/review_notes_tam.md")


def _text() -> str:
    return NOTES_PATH.read_text(encoding="utf-8")


def test_tam_review_notes_exist() -> None:
    assert NOTES_PATH.exists(), "TAM review notes must exist"


def test_tam_review_notes_name_controlling_files() -> None:
    text = _text()
    for required in (
        "candidates_tam.tsv",
        "dossier_tam_scope.md",
        "grammar_tam_print_slice.md",
        "dictionary_tam_print_slice.md",
    ):
        assert required in text


def test_tam_review_notes_mark_packet_aligned_and_review_ready() -> None:
    text = _text()
    assert "current slice maturity level" in text
    assert "ready for human review at the current slice maturity level" in text
    assert "first TAM packet, not a full TAM chapter" in text


def test_tam_review_notes_cover_first_slice_anchors() -> None:
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
    ):
        assert required in text

    assert "`-ngei`" in text
    assert "`-gige`" in text
    assert "`-zel`" in text
    assert "`-ta`" in text
    assert "`-zo`" in text
    assert "`-kik`" in text
    assert "`-ding`" in text
    assert "`-thei`" in text


def test_tam_review_notes_keep_required_caveats_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "construction-control caveat" in lower
    assert "sentence-final overlap caveat" in lower
    assert "bare-`zo` and sentence-final overlap caveat" in text
    assert "motion/return caveat" in lower
    assert "`dingin` and clause-bound caveat" in text
    assert "negation/irrealis-stack caveat" in lower


def test_tam_review_notes_keep_deferred_material_outside_first_slice() -> None:
    text = _text()

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


def test_tam_review_notes_name_packet_contents() -> None:
    text = _text()
    lower = text.lower()

    assert "candidate" in lower
    assert "scoping dossier" in lower
    assert "grammar" in lower
    assert "dictionary" in lower
    assert "tests" in lower
