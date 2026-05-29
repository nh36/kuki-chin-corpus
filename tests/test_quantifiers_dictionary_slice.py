from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/dictionary_quantifiers_print_slice.md"


def test_quantifiers_dictionary_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_quantifiers_dictionary_slice_names_control_and_cross_reference_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_quantifiers.tsv" in text
    assert "dossier_quantifiers.md" in text
    assert "grammar_quantifiers_print_slice.md" in text
    assert "analyzer dictionaries" in lower
    assert "machine dictionary files" in lower


def test_quantifiers_dictionary_slice_has_required_entries() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for heading in (
        "## khempeuh",
        "## pawlkhat",
        "## khat",
        "## kuamah",
        "## bangmah",
        "## tampi",
        "## peuhpeuh",
        "## tawm",
        "## zaw",
        "## mahmah",
    ):
        assert heading in text


def test_quantifiers_dictionary_slice_keeps_core_examples_and_caveats() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "vantung leitung le a sunga omte khempeuh" in text
    assert "universal anchor" in lower
    assert "raw `khempeuh` harvesting" in text

    assert "pawlkhat" in text
    assert "partitive or alternative-grouping" in lower
    assert "uncomplicated bare `some`" in text

    assert "mi khat" in text
    assert "numeral/indefinite boundary" in lower or "boundary evidence" in lower

    assert "kuamah mu lo" in text
    assert "negative-licensed" in lower
    assert "negation overlap" in lower or "negation-overlap" in lower

    assert "bangmah om lo hi" in text
    assert "bang-family" in lower or "interrogative-overlap" in lower
    assert "tua bangmah hi-in" in lower
    assert "blocked" in lower

    assert "tampi tak" in text
    assert "broad adjective/adverb chapter" in lower


def test_quantifiers_dictionary_slice_keeps_deferred_and_edge_material_narrow() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "mi peuhpeuh" in text
    assert "deferred" in lower
    assert "not print-ready" in lower

    assert "tawm" in lower
    assert "produce" in lower or "noisy" in lower

    assert "vanglian zaw" in text
    assert "edge row" in lower
    assert "full comparison chapter" in lower

    assert "hau mahmah" in text
    assert "full intensifier or degree-modification chapter" in lower


def test_quantifiers_dictionary_slice_avoids_raw_counts_and_marks_next_step() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("5,191", "4,712", "664", "525", "735", "1,351", "13,000+"):
        assert banned not in text

    assert "review_notes_quantifiers.md" in text or "review-note work has not yet begun" in lower
