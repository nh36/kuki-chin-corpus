from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_coordinators.md"


def test_coordinators_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_coordinators_dossier_names_control_layer_and_protocol() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_coordinators.tsv" in text
    assert "candidate rows, not raw string hits and not generated-report counts" in lower
    assert "scripts/publication_review/extract_candidates.py" in text
    assert "does **not** search every `le`, `leh`, `a`, `mawh`, `ahih hangin`, `ahih kei leh`, `ciangin`, `hangin`" in lower


def test_coordinators_dossier_mentions_core_rows_and_boundaries() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
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

    assert "safe np-conjunction anchor" in lower or "np coordination with `le`" in lower
    assert "does **not** license broad raw `le` harvesting" in lower
    assert "conditional or boundary material" in lower
    assert "not a clean print-ready clause-conjunction row" in lower or "not a clean print-ready clause conjunction" in lower
    assert "kei` is glossed as `neg`" in lower or "glossed as `neg`" in lower
    assert "without reopening the negation or pronouns packets" in lower


def test_coordinators_dossier_keeps_caveats_and_deferred_material_visible() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "accepted with caveat" in lower
    assert "not print-ready" in lower
    assert "3sg" in lower and "func" in lower
    assert "agreement-`a` false friend" in lower or "agreement-a false friend" in lower
    assert "lexical `sin` / `v`" in lower or "lexical `sin` / `v` material" in lower
    assert "disjunction or alternative-question" in lower
    assert "internally analyzable" in lower
    assert "hangin" in lower
    assert "conditional-adversative boundary material" in lower
    assert "sentence-final particles remain deferred" in lower


def test_coordinators_dossier_avoids_raw_counts_and_marks_next_step() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("11,122", "3,370", "78,120", "144", "1,422", "203", "15,000+"):
        assert banned not in text

    assert "grammar, dictionary, and review-note print slices for coordinators have **not** yet begun" in lower
    assert "grammar_coordinators_print_slice.md" in text
    for deferred in ("broad tam", "directionals", "chrestomathy", "mizo/lus", "other kuki-chin"):
        assert deferred in lower
