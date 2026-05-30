from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_coordinators_print_slice.md"


def test_coordinators_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_coordinators_print_slice_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_coordinators.tsv" in text
    assert "dossier_coordinators.md" in text
    assert "controlled by `candidates_coordinators.tsv` and `dossier_coordinators.md`" in lower


def test_coordinators_print_slice_includes_core_anchor_and_boundary_material() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for required in (
        "vantung le leitung",
        "veilam na lak leh kei taklamah ka pai ding hi",
        "luang a tua mun panin gun hong kikhenin",
        "a piangsak",
        "mawh",
        "Ahih hangin",
        "ahih kei leh",
    ):
        assert required in text

    assert "safe NP-conjunction anchor".lower() in lower
    assert "does **not** license broad raw `le` harvesting" in lower
    assert "conditional or boundary material" in lower
    assert "not as a clean simple clause-conjunction anchor" in lower or "not as a clean simple clause conjunction anchor" in lower


def test_coordinators_print_slice_keeps_export_caveats_and_false_friends_visible() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "glossed as `NEG`" in text or "glossed as `neg`" in lower
    assert "not used to reopen the pronouns or negation packets" in lower
    assert "3SG" in text or "3sg" in lower
    assert "FUNC" in text or "func" in lower
    assert "warning or boundary evidence only" in lower
    assert "blocked agreement or function material" in lower
    assert "false-friend control prevents raw `a` harvesting" in lower


def test_coordinators_print_slice_keeps_mawh_and_ahih_material_conservative() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "lexical or analyzer-noise material glossed as `sin` / `V`" in text or "lexical or analyzer-noise material glossed as `sin` / `v`" in lower
    assert "not print-ready" in lower
    assert "disjunction or alternative-question material" in lower
    assert "internally analyzable as `ahih` + `hang-in`" in lower or "internally analyzable" in lower
    assert "conditional-adversative boundary material" in lower
    assert "should not reopen the stabilized negation packet" in lower


def test_coordinators_print_slice_avoids_broadening_and_marks_next_step() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("11,122", "3,370", "78,120", "144", "1,422", "203", "15,000+"):
        assert banned not in text

    assert "dictionary print slice" in lower
    assert "dictionary and review-note slices have not yet begun" in lower or "dictionary and review-note work have not yet begun" in lower
    assert "dictionary_coordinators_print_slice.md" not in text
    assert "review_notes_coordinators.md" not in text
    for deferred in ("sentence-final particles", "broad tam", "directionals", "chrestomathy", "mizo/lus", "other kuki-chin"):
        assert deferred in lower
