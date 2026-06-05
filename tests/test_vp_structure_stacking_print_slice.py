from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_vp_structure_stacking_print_slice.md"


def test_vp_structure_stacking_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_vp_structure_stacking_print_slice_is_grammar_facing() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Overview of VP structure and suffix stacking" in text
    assert "# Editorial scope" not in text
    assert "packet" not in lower
    assert "candidate tsv" not in lower
