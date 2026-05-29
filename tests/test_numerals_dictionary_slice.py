from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/dictionary_numerals_print_slice.md"


def test_numerals_dictionary_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_numerals_dictionary_slice_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_numerals.tsv" in text
    assert "dossier_numerals.md" in text
    assert "grammar_numerals_print_slice.md" in text
    assert "machine dictionary files" in lower


def test_numerals_dictionary_slice_includes_core_entries_and_examples() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for required in (
        "## nih",
        "## sagih",
        "## sawmkua",
        "## nihna",
        "## sawmvei",
        "## kua (numeral-side use)",
        "## khat",
        "kum nih",
        "ni sagih",
        "kum sawmkua",
        "nihna",
        "sawmvei",
        "mi khat",
        "kum zakua le kum sawmguk le kua",
    ):
        assert required in text


def test_numerals_dictionary_slice_keeps_kua_and_khat_cautious() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "hihte kua ahi hiam" in lower or "genesis 48:8" in lower
    assert "blocked as numeral evidence" in lower or "belongs to the interrogatives packet" in lower
    assert "boundary evidence" in lower or "numeral and indefinite reference" in lower
    assert "does not start the later quantifiers retrofit" in lower


def test_numerals_dictionary_slice_keeps_export_caveats_and_deferred_material_visible() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "`vei sawm`" in text
    assert "export-backed fused form `sawmvei`" in lower or "export-backed fused form `sawmvei`" in text
    assert "sagih sagih" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower

    caveat_hits = 0
    for required in (
        "nine [export: who]",
        "pos_span = N",
        "lemma/POS export is flattened",
        "export-backed fused form `sawmvei`",
    ):
        if required in text or required in lower:
            caveat_hits += 1
    assert caveat_hits >= 2


def test_numerals_dictionary_slice_avoids_broadening() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x"):
        assert banned not in text

    assert "full classifier system" in lower
    assert "raw search over every" in lower
    assert "review-note work for numerals has not yet begun" in lower or "review_notes_numerals.md" in text
