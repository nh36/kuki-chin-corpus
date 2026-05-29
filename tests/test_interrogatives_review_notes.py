from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / "output/publication_review/review_notes_interrogatives.md"


def test_interrogatives_review_notes_exists() -> None:
    assert NOTES_PATH.exists()


def test_interrogatives_review_notes_names_control_files_and_core_analysis() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    for required in (
        "candidates_interrogatives.tsv",
        "dossier_interrogatives.md",
        "grammar_interrogatives_print_slice.md",
        "dictionary_interrogatives_print_slice.md",
        "Genesis 24:23",
        "WH + `hiam`",
        "`bang`",
        "`kua`",
        "`bangci`",
        "`banghangin`",
    ):
        assert required in text


def test_interrogatives_review_notes_keep_deferred_and_blocked_material_explicit() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "bang hiam cih" in lower
    assert "not promoted" in lower or "later treatment" in lower or "stay out of print" in lower
    assert "Bang hang hiam cih leh" in text
    assert "a hiam ciat uh" in text or "langnih a hiam namsau" in text
    assert "bangmah" in text
    assert "bangin" in text
    assert "`maw`, `ham`, and `em`" in text
    assert "remain deferred" in lower


def test_interrogatives_review_notes_record_analyzer_caveats_and_avoid_overclaims() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "`NUM`" in text or "NUM" in text
    assert "`like`" in text or "like" in text
    assert "bang | hang-in" in text
    assert "5,230" not in text
    assert "10,000+" not in text
    assert "hiam is always clause-final" not in lower
    assert "ready for human review" in lower or "current slice maturity level" in lower
