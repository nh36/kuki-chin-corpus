from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES_PATH = ROOT / "output/publication_review/review_notes_numerals.md"


def test_numerals_review_notes_exists() -> None:
    assert NOTES_PATH.exists()


def test_numerals_review_notes_names_control_files() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    for required in (
        "candidates_numerals.tsv",
        "dossier_numerals.md",
        "grammar_numerals_print_slice.md",
        "dictionary_numerals_print_slice.md",
    ):
        assert required in text


def test_numerals_review_notes_mentions_core_analysis() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")

    for required in (
        "kum nih",
        "ni sagih",
        "sawmkua",
        "nihna",
        "sawmvei",
        "mi khat",
        "kum zakua le kum sawmguk le kua",
        "masa",
    ):
        assert required in text


def test_numerals_review_notes_keep_boundaries_and_blocked_material_explicit() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "hihte kua ahi hiam" in lower or "genesis 48:8" in lower
    assert "blocked" in lower or "warn" in lower
    assert "numeral/indefinite boundary" in lower or "boundary evidence" in lower
    assert "sagih sagih" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower


def test_numerals_review_notes_record_export_caveats() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "export-backed fused form" in lower
    assert "`vei sawm`" in text

    caveat_hits = 0
    for required in (
        "glossed as `who`",
        "pos_span = N",
        "lemma/POS export is flattened",
        "export-backed fused form",
    ):
        if required in text or required.lower() in lower:
            caveat_hits += 1
    assert caveat_hits >= 2


def test_numerals_review_notes_avoid_raw_counts_and_mark_next_stage() -> None:
    text = NOTES_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x"):
        assert banned not in text

    assert "ready for human review" in lower or "current slice maturity level" in lower
    assert "quantifiers" in lower
    assert "coordinators" in lower
    assert "sentence-final particles" in lower
    assert "broad tam" in lower
    assert "directionals" in lower
    assert "chrestomathy" in lower
    assert "mizo/lus" in lower
    assert "other kuki-chin languages" in lower
