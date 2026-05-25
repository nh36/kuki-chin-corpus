from pathlib import Path


GRAMMAR_SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/grammar_demonstratives_print_slice.md"
DICTIONARY_SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/dictionary_demonstratives_print_slice.md"
REVIEW_NOTES_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/review_notes_demonstratives.md"
REPORT_PATH = Path(__file__).resolve().parents[1] / "docs/grammar/reports/06-func-02-demonstratives.md"


def test_demonstratives_packet_keeps_deferred_forms_out_of_headwords():
    grammar = GRAMMAR_SLICE_PATH.read_text()
    dictionary = DICTIONARY_SLICE_PATH.read_text()

    assert "## hi\n" not in dictionary
    assert "## hih ciangin\n" not in dictionary

    assert "`Hi` should be deferred." in grammar
    assert "`Hih ciangin` should also be deferred." in grammar


def test_demonstratives_packet_excludes_known_bad_examples():
    grammar = GRAMMAR_SLICE_PATH.read_text()
    dictionary = DICTIONARY_SLICE_PATH.read_text()

    for banned in (
        "Genesis 6:22",
        "John 1:19",
    ):
        assert banned not in grammar
        assert banned not in dictionary


def test_demonstratives_report_carries_correction_note():
    report = REPORT_PATH.read_text()
    notes = REVIEW_NOTES_PATH.read_text()

    assert "exact-token `hi` is deferred" in report
    assert "Genesis 6:22 has `tua bangmahin` rather than plain `hih bangin`" in report
    assert "John 1:19 is not a clean `hi` demonstrative example" in report
    assert "The analyzer already contains a demonstrative inventory." in notes
