from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / "output/publication_review/review_notes_coordinators.md"


def test_coordinators_review_notes_exists() -> None:
    assert NOTES_PATH.exists()


def test_coordinators_review_notes_name_control_files() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    for required in (
        "candidates_coordinators.tsv",
        "dossier_coordinators.md",
        "grammar_coordinators_print_slice.md",
        "dictionary_coordinators_print_slice.md",
    ):
        assert required in text


def test_coordinators_review_notes_cover_core_analysis() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "vantung le leitung" in lower
    assert "safe NP-conjunction anchor".lower() in lower
    assert "does not license raw `le` harvesting" in lower

    assert "veilam na lak leh kei taklamah ka pai ding hi" in lower or "genesis 13:9" in lower
    assert "conditional or boundary evidence" in lower or "conditional or boundary material" in lower
    assert "not by broad string searches" in lower
    assert "without reopening pronouns or negation" in lower

    assert "luang a tua mun panin gun hong kikhenin" in lower
    assert "caveated boundary evidence" in lower
    assert "not print-ready" in lower

    assert "a piangsak" in lower
    assert "blocked agreement or function control" in lower or "blocked agreement or function material" in lower

    assert "mawh" in lower
    assert "sin" in lower
    assert "deferred" in lower
    assert "rather than disjunction" in lower

    assert "ahih hangin" in lower
    assert "adversative connector" in lower
    assert "internal-analysis" in lower or "internally analyzable" in lower

    assert "ahih kei leh" in lower
    assert "conditional-adversative boundary material" in lower
    assert "should not reopen negation" in lower


def test_coordinators_review_notes_record_export_caveats() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "`kei = NEG`" in text or "glossed as `neg`" in lower
    assert "`3SG` / `FUNC`" in text or "`3sg` / `func`" in lower
    assert "`sin` / `V`" in text or "`sin` / `v`" in lower
    assert "`ahih` + `hang-in`" in text or "internally analyzable as `ahih` + `hang-in`" in lower


def test_coordinators_review_notes_avoid_raw_counts_and_mark_review_ready() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("11,122", "3,370", "78,120", "144", "1,422", "203", "15,000+"):
        assert banned not in text

    assert "ready for human review" in lower or "current slice maturity level" in lower
    assert "sentence-final particles" in lower
    assert "broad tam" in lower
    assert "directionals" in lower
    assert "chrestomathy" in lower
    assert "mizo/lus" in lower
    assert "other kuki-chin languages" in lower
