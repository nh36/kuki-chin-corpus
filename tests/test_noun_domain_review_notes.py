from pathlib import Path


NOTES_PATH = Path("output/publication_review/review_notes_noun_domain.md")


def _text() -> str:
    return NOTES_PATH.read_text(encoding="utf-8")


def test_review_notes_file_exists() -> None:
    assert NOTES_PATH.exists(), "noun domain review notes should exist"


def test_review_notes_name_normalized_packet_surfaces() -> None:
    text = _text()

    for required in (
        "numerals",
        "quantifiers",
        "NP structure / possession",
        "assembled grammar review preview PDF",
    ):
        assert required in text


def test_review_notes_track_normalized_noun_domain_scope() -> None:
    lower = _text().lower()

    assert "publication-facing" in lower
    assert "simple lexical noun stems" in lower
    assert "plural marking with `-te`" in _text()
    assert "nouns as heads inside counted and quantified phrases" in lower


def test_review_notes_record_gospel_search_result() -> None:
    lower = _text().lower()

    assert "gospel" in lower
    assert "ama aksi" in lower
    assert "mi khempeuh" in lower
    assert "ot-led" in lower
