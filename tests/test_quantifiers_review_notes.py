from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / "output/publication_review/review_notes_quantifiers.md"


def test_quantifiers_review_notes_exists() -> None:
    assert NOTES_PATH.exists()


def test_quantifiers_review_notes_name_control_files() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    for required in (
        "candidates_quantifiers.tsv",
        "dossier_quantifiers.md",
        "grammar_quantifiers_print_slice.md",
        "dictionary_quantifiers_print_slice.md",
    ):
        assert required in text


def test_quantifiers_review_notes_cover_core_analysis() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

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
        assert required in lower

    assert "mi peuhpeuh" in lower or "peuhpeuh" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower
    assert "tawm" in lower
    assert "numeral/indefinite boundary" in lower or "boundary evidence" in lower
    assert "negative-licensed" in lower
    assert "negation overlap" in lower or "negation-overlap" in lower
    assert "bang-family" in lower or "interrogative-overlap" in lower
    assert "tua bangmah hi-in" in lower or "exodus 27:11" in lower
    assert "blocked" in lower or "warn" in lower


def test_quantifiers_review_notes_keep_scope_narrow() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "broad adjective/adverb" in lower
    assert "full degree/intensifier/comparative chapter" in lower
    assert "edge rows" in lower or "edge row" in lower

    for banned in ("5,191", "4,712", "664", "525", "735", "1,351", "13,000+"):
        assert banned not in text


def test_quantifiers_review_notes_mark_review_ready_and_future_scope() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ready for human review" in lower or "current slice maturity level" in lower
    assert "coordinators" in lower
    assert "sentence-final particles" in lower
    assert "broad tam" in lower
    assert "directionals" in lower
    assert "chrestomathy" in lower
    assert "mizo/lus" in lower
    assert "other kuki-chin languages" in lower
