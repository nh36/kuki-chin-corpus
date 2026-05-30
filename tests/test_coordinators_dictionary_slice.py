from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/dictionary_coordinators_print_slice.md"


def test_coordinators_dictionary_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_coordinators_dictionary_slice_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_coordinators.tsv" in text
    assert "dossier_coordinators.md" in text
    assert "grammar_coordinators_print_slice.md" in text
    assert "analyzer dictionaries" in lower
    assert "machine dictionary files" in lower


def test_coordinators_dictionary_slice_has_required_entries() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for heading in (
        "## le",
        "## leh",
        "## a",
        "## mawh",
        "## ahih hangin",
        "## ahih kei leh",
    ):
        assert heading in text


def test_coordinators_dictionary_slice_keeps_core_anchor_and_boundary_material() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "vantung le leitung" in text
    assert "safe NP-conjunction anchor".lower() in lower
    assert "does **not** license broad raw `le` harvesting" in lower

    assert "veilam na lak leh kei taklamah ka pai ding hi" in text or "Genesis 13:9" in text
    assert "conditional or boundary material" in lower
    assert "not draft-ready as simple clause coordinator" in lower or "not print-ready as simple clause conjunction" in lower
    assert "glossed as `NEG`" in text or "glossed as `neg`" in lower
    assert "not reopen pronouns or negation" in lower


def test_coordinators_dictionary_slice_keeps_a_and_mawh_conservative() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "luang a tua mun panin gun hong kikhenin" in text
    assert "not print-ready as a core coordinator example" in lower or "not print-ready as coordinator" in lower
    assert "3SG" in text or "3sg" in lower
    assert "FUNC" in text or "func" in lower

    assert "a piangsak" in lower
    assert "blocked as agreement or function material" in lower

    assert "mawh" in lower
    assert "sin" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower
    assert "disjunction or alternative-question material" in lower


def test_coordinators_dictionary_slice_keeps_ahih_material_conservative() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Ahih hangin" in text
    assert "adversative connector anchor" in lower
    assert "internally analyzable as `ahih` + `hang-in`" in lower or "internal-analysis caveat" in lower

    assert "ahih kei leh" in lower
    assert "conditional-adversative boundary expression" in lower or "conditional-adversative boundary" in lower
    assert "overlaps with negation and conditional `leh`" in lower or "overlaps with negation and conditional leh" in lower
    assert "should not be flattened into plain" in lower


def test_coordinators_dictionary_slice_avoids_broadening_and_marks_next_step() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("11,122", "3,370", "78,120", "144", "1,422", "203", "15,000+"):
        assert banned not in text

    assert "review-note work for coordinators has not yet begun" in lower or "review_notes_coordinators.md" in text
    for deferred in ("sentence-final particles", "broad tam", "directionals", "chrestomathy", "mizo/lus", "other kuki-chin"):
        assert deferred in lower
