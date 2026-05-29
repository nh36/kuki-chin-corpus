from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_quantifiers_print_slice.md"


def test_quantifiers_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_quantifiers_print_slice_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_quantifiers.tsv" in text
    assert "dossier_quantifiers.md" in text
    assert "controlled by `candidates_quantifiers.tsv` and `dossier_quantifiers.md`" in lower


def test_quantifiers_print_slice_includes_core_examples() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for required in (
        "khempeuh",
        "pawlkhat",
        "mi khat",
        "kuamah mu lo",
        "bangmah om lo hi",
        "tampi tak",
        "vanglian zaw",
        "hau mahmah",
    ):
        assert required in text


def test_quantifiers_print_slice_handles_deferred_and_blocked_material() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "mi peuhpeuh" in lower or "peuhpeuh" in lower
    assert "tawm" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower
    assert "tua bangmah hi-in" in lower or "exodus 27:11" in lower
    assert "blocked control" in lower


def test_quantifiers_print_slice_keeps_boundary_and_overlap_caveats_visible() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "numeral/indefinite boundary" in lower
    assert "does not treat `khat` as an uncomplicated quantifier anchor" in lower
    assert "negative-licensed" in lower
    assert "cross-reference, not reopen, the stabilized negation packet" in lower
    assert "bang-family false friends" in lower or "interrogatives packet" in lower


def test_quantifiers_print_slice_keeps_degree_and_edge_rows_narrow() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "degree or quantity anchor" in lower
    assert "full adjective or adverb chapter" in lower
    assert "edge material" in lower or "edge rows" in lower
    assert "full comparison or intensifier chapter" in lower


def test_quantifiers_print_slice_avoids_broadening_and_marks_next_step() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("5,191", "4,712", "664", "525", "735", "1,351", "13,000+"):
        assert banned not in text
    assert "dictionary print slice" in lower
    assert "review-note work has not yet begun" in lower
    assert "dictionary_quantifiers_print_slice.md" not in text
    assert "review_notes_quantifiers.md" not in text
