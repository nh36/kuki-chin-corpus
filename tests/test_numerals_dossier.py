from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_numerals.md"


def test_numerals_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_numerals_dossier_names_control_layer_and_protocol() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_numerals.tsv" in text
    assert "candidate rows, not raw string hits and not generated-report counts" in lower
    assert "scripts/publication_review/extract_candidates.py" in text


def test_numerals_dossier_mentions_core_rows_and_boundaries() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

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

    assert "hihte kua ahi hiam" in lower or "genesis 48:8" in lower
    assert "numeral `nine`" in text or "numeral `nine`" in lower
    assert "interrogative `who`" in text or "interrogative `who`" in lower
    assert "numeral/indefinite boundary" in lower or "boundary evidence" in lower


def test_numerals_dossier_keeps_export_caveats_and_deferred_material_visible() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "`vei sawm`" in text
    assert "fused export-backed form" in lower
    assert "sagih sagih" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower
    assert "glossed as `who`" in text or "glossed as `who`" in lower
    assert "`pos_span` is `N`" in text or "pos_span" in lower
    assert "lemma export is flattened" in lower or "lemma export" in lower


def test_numerals_dossier_avoids_raw_counts_and_marks_next_step() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("9,000+", "4,712", "541", "750x"):
        assert banned not in text

    assert "grammar, dictionary, and review-note print slices for numerals have **not** yet begun" in lower
    assert "grammar_numerals_print_slice.md" in text
