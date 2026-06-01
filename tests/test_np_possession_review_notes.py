from pathlib import Path


REVIEW_NOTES = Path("output/publication_review/review_notes_np_possession.md")


def _text() -> str:
    return REVIEW_NOTES.read_text(encoding="utf-8")


def test_review_notes_file_exists() -> None:
    assert REVIEW_NOTES.exists(), "Expected NP/possession review notes to exist"


def test_review_notes_name_normalized_packet_surfaces() -> None:
    text = _text()
    for required in (
        "candidates_np_possession.tsv",
        "dossier_np_possession.md",
        "grammar_np_possession_print_slice.md",
        "examples_np_possession_normalization.tsv",
    ):
        assert required in text


def test_review_notes_track_normalized_np_and_possession_split() -> None:
    text = _text()
    assert "Structural NP rows remain the safest anchors" in text
    assert "Possession is now printable with caveats" in text
    assert "No clean full possessive paradigm is yet printed." in text


def test_review_notes_record_gospel_search_result() -> None:
    text = _text()
    assert "John 11:39" in text
    assert "Luke 2:1" in text
    assert "No equally clean Gospel possession example was found" in text

