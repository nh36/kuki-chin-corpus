from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_sentence_final_particles_print_slice.md"


def test_sentence_final_particles_print_slice_exists_and_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert SLICE_PATH.exists()
    assert "candidates_sentence_final_particles.tsv" in text
    assert "dossier_sentence_final_particles.md" in text
    assert "controlled by `candidates_sentence_final_particles.tsv` and `dossier_sentence_final_particles.md`" in lower


def test_sentence_final_particles_print_slice_keeps_hi_hiam_and_hen_conservative() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "ahi hi" in text
    assert "copula-plus-declarative evidence" in lower
    assert "not a bare `hi` example" in lower
    assert "thusim lo hi" in text
    assert "negation-overlap evidence only" in lower
    assert "should not reopen `lo`" in lower
    assert "Hihte kua ahi hiam?" in text or "Genesis 48:8" in text
    assert "interrogatives packet" in lower
    assert "should not reopen or duplicate `hiam` analysis" in lower or "should not reopen or duplicate hiam analysis" in lower
    assert "Khuavak om hen" in text
    assert "optative evidence with caveat" in lower
    assert "report-style `ta hen` wording" in text


def test_sentence_final_particles_print_slice_keeps_imperatives_and_boundary_material_narrow() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "teembaw khat bawl in" in text
    assert "`ERG` / `FUNC`" in text or "erg" in lower
    assert "case-marker and export caveat" in lower or "case-overlap caveat" in lower
    assert "report-style `lawng`" in text
    assert "gingsak un" in text
    assert "clean plural-imperative anchor" in lower
    assert "Gam khempeuh aw" in text
    assert "vocative or exclamative boundary material" in lower
    assert "not settled sentence-final mood evidence" in lower
    assert "hi tahen" in text
    assert "`army` / `N`" in text or "`army` / `n`" in lower
    assert "fused `tahen` or split `ta hen`" in text or "split `ta hen`" in text
    assert "mangngilh ta hi" in text
    assert "needs-review tam-overlap material" in lower
    assert "zo" in text
    assert "`south` / `N`" in text or "`south` / `n`" in lower


def test_sentence_final_particles_print_slice_avoids_raw_counts_and_sets_next_step() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("24,754", "1,000", "858", "764", "5,230", "150", "230", "137", "670", "39", "2,306", "1,144", "577", "167+", "338"):
        assert banned not in text

    assert "dictionary print slice" in lower
    assert "dictionary and review-note slices have not yet begun" in lower
    assert "review_notes_sentence_final_particles.md" not in text
    for deferred in ("broad tam", "directionals", "chrestomathy", "mizo/lus", "other kuki-chin"):
        assert deferred in lower
