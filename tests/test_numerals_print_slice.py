from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_numerals_print_slice.md"


def test_numerals_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_numerals_print_slice_names_control_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_numerals.tsv" in text
    assert "dossier_numerals.md" in text
    assert "controlled by `candidates_numerals.tsv` and `dossier_numerals.md`" in lower


def test_numerals_print_slice_includes_core_examples() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for required in (
        "kum nih",
        "ni sagih",
        "kum sawmkua",
        "nihna",
        "sawmvei",
        "mi khat",
        "kum zakua le kum sawmguk le kua",
    ):
        assert required in text


def test_numerals_print_slice_handles_kua_and_khat_cautiously() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "hihte kua ahi hiam" in lower or "genesis 48:8" in lower
    assert "must therefore not use raw `kua` hits as numeral evidence" in lower
    assert "numeral/indefinite boundary" in lower
    assert "should not be treated as an uncomplicated bare numeral `one` example" in lower


def test_numerals_print_slice_keeps_export_caveats_and_deferred_material_visible() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "`vei sawm`" in text
    assert "export-backed `sawmvei`" in text or "export-backed `sawmvei`" in lower
    assert "sagih sagih" in lower
    assert "not print-ready" in lower
    caveat_hits = 0
    for required in (
        "nine [export: who]",
        "pos_span = N",
        "lemma and POS layer is flattened",
        "fused form should control the present slice",
    ):
        if required in text or required in lower:
            caveat_hits += 1
    assert caveat_hits >= 2


def test_numerals_print_slice_avoids_broadening() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x"):
        assert banned not in text
    assert "full classifier system" in lower
    assert "does not start a quantifiers retrofit here" in lower
    assert "dictionary print slice" in lower or "dictionary and review-note slices have not yet begun" in lower
