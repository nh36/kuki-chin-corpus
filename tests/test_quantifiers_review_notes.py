from pathlib import Path


NOTES = Path("output/publication_review/review_notes_quantifiers.md")


def _text() -> str:
    return NOTES.read_text(encoding="utf-8")


def test_quantifiers_review_notes_exists() -> None:
    assert NOTES.exists(), "Quantifiers review notes must exist"


def test_quantifiers_review_notes_names_packet_surfaces() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "grammar_numerals_print_slice.md",
        "candidates_quantifiers.tsv",
        "dossier_quantifiers.md",
        "grammar_quantifiers_print_slice.md",
        "review_notes_quantifiers.md",
        "examples_quantifiers_normalization.tsv",
        "docs/grammar/reports/06-func-05-quantifiers.md",
    ):
        assert required in text


def test_quantifiers_review_notes_tracks_core_analysis_and_boundaries() -> None:
    text = _text()

    for required in (
        "khempeuh",
        "pawlkhat",
        "mi khat",
        "kuamah",
        "bangmah",
        "tampi tak",
        "mi tampi",
        "zaw",
        "mahmah",
        "peuhpeuh",
        "tawm",
        "candidate evidence",
        "explicit caveats",
    ):
        assert required in text


def test_quantifiers_review_notes_records_gospel_balance() -> None:
    text = _text()

    for required in (
        "Luke 2:1",
        "Matthew 2:1",
        "Mark 6:34",
        "John 3:27",
        "Old Testament",
        "Gospel",
        "does not produce a cleaner replacement for the classic `mi khat` boundary row".replace("does not", "did not"),
    ):
        assert required in text


def test_quantifiers_review_notes_marks_normalized_maturity() -> None:
    text = _text()

    for required in (
        "second normalized coverage section after numerals",
        "review preview rather than a finished grammar",
        "ready for human review at the current normalized coverage level",
        "Phonology/tone and verb paradigms remain major non-homogeneous gaps",
    ):
        assert required in text
