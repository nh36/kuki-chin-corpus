from pathlib import Path


DOSSIER_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/dossier_sentence_final_particles.md"


def test_sentence_final_particles_dossier_exists_and_keeps_candidate_layer_controlling() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert DOSSIER_PATH.exists()
    assert "candidates_sentence_final_particles.tsv" in text
    assert "Candidate rows, not raw string hits and not generated-report counts, control the dossier." in text
    assert "does **not** search every `hi`, `hiam`, `in`, `un`, `tahen`, `hen`, `aw`, `ta`, `zo`" in text


def test_sentence_final_particles_dossier_keeps_hi_hiam_and_tahen_conservative() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "`ahi hi`" in text
    assert "not a bare declarative `hi` example" in text
    assert "`thusim lo hi`" in text
    assert "must not reopen `lo`" in text
    assert "`Hihte kua ahi hiam?`" in text or "Genesis 48:8" in text
    assert "interrogatives-overlap control" in text
    assert "should not reopen `hiam` analysis" in text or "should not reopen or duplicate interrogatives prose" in text
    assert "`hi tahen`" in text
    assert "lexical `army` / `N`" in text
    assert "fused `tahen` and split `ta hen`" in text or "split `ta hen`" in text


def test_sentence_final_particles_dossier_keeps_imperatives_aw_ta_and_zo_narrow() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "`Khuavak om hen`" in text
    assert "optative evidence" in text
    assert "`teembaw khat bawl in`" in text
    assert "`ERG` / `FUNC`" in text
    assert "case-marker overlap" in text
    assert "`gingsak un`" in text
    assert "imperative-plural anchor" in text
    assert "`Gam khempeuh aw`" in text
    assert "vocative or exclamative boundary material" in text
    assert "not print-ready" in text
    assert "`mangngilh ta hi`" in text
    assert "needs-review" in text or "needs-review because `ta` is exported as `child` / `FUNC`" in text
    assert "Broad TAM remains deferred." in text
    assert "`zo`" in text
    assert "lexical `south` / `N`" in text


def test_sentence_final_particles_dossier_avoids_raw_counts_and_sets_next_step() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for banned in ("24,754", "1,000", "858", "764", "5,230", "150", "230", "137", "670", "39", "2,306", "1,144", "577", "167+", "338"):
        assert banned not in text

    assert "grammar, dictionary, and review-note print slices for sentence-final particles have **not** yet begun" in text
    assert "grammar_sentence_final_particles_print_slice.md" in text
    assert "dictionary_sentence_final_particles_print_slice.md" in text
    assert "review_notes_sentence_final_particles.md" in text
    assert "Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred." in text
