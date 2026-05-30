from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / "output/publication_review/review_notes_sentence_final_particles.md"


def test_sentence_final_particles_review_notes_exist_and_name_control_files() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    assert NOTES_PATH.exists()
    assert "candidates_sentence_final_particles.tsv" in text
    assert "dossier_sentence_final_particles.md" in text
    assert "grammar_sentence_final_particles_print_slice.md" in text
    assert "dictionary_sentence_final_particles_print_slice.md" in text


def test_sentence_final_particles_review_notes_keep_hi_hiam_and_hen_conservative() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ahi hi" in text
    assert "copula-plus-declarative evidence" in lower
    assert "not bare `hi` evidence" in lower
    assert "thusim lo hi" in text
    assert "negation-overlap evidence" in lower
    assert "does not reopen negation" in lower or "should cross-reference, not reopen, the negation packet" in lower
    assert "Hihte kua ahi hiam?" in text or "Genesis 48:8" in text
    assert "interrogatives packet" in lower
    assert "should not be reanalyzed here" in lower or "does not reopen `hiam`" in lower
    assert "Khuavak om hen" in text
    assert "usable optative row" in lower
    assert "report-style `ta hen`" in text


def test_sentence_final_particles_review_notes_keep_imperatives_and_boundary_material_narrow() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "teembaw khat bawl in" in text
    assert "`ERG` / `FUNC`" in text or "erg" in lower
    assert "case-overlap caveat" in lower or "case-marker overlap" in lower
    assert "gingsak un" in text
    assert "cleanest current plural-imperative anchor" in lower
    assert "Gam khempeuh aw" in text
    assert "vocative or exclamative boundary material" in lower
    assert "rather than settled sentence-final mood evidence" in lower or "boundary material only" in lower
    assert "hi tahen" in text
    assert "`army` / `N`" in text or "`army` / `n`" in lower
    assert "fused `tahen` versus split `ta hen`" in text or "split `ta hen`" in text
    assert "mangngilh ta hi" in text
    assert "tam-overlap material" in lower
    assert "zo" in text
    assert "`south` / `N`" in text or "`south` / `n`" in lower


def test_sentence_final_particles_review_notes_avoid_raw_counts_and_mark_review_ready() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("24,754", "1,000", "858", "764", "5,230", "150", "230", "137", "670", "39", "2,306", "1,144", "577", "167+", "338"):
        assert banned not in text

    assert "ready for human review at the current slice maturity level" in lower
    for deferred in ("broad tam", "directionals", "chrestomathy", "mizo/lus", "other kuki-chin"):
        assert deferred in lower
