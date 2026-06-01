from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = REPO_ROOT / "output" / "publication_review" / "grammar_np_possession_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_np_possession_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "NP structure / possession grammar slice must exist"


def test_np_possession_print_slice_names_control_files() -> None:
    text = _text()

    for required in (
        "coverage_normalization_audit.md",
        "candidates_np_possession.tsv",
        "dossier_np_possession.md",
        "review_notes_np_possession.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
    ):
        assert required in text


def test_np_possession_print_slice_has_normalized_structure_and_anchors() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Overview of noun phrase structure",
        "Current NP pattern inventory",
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Deferred and boundary material",
        "hih mite",
        "mi khat",
        "mi khempeuh",
        "ni li",
    ):
        assert required in text

    assert "candidate evidence" in lower
    assert "explicit caveats" in lower


def test_np_possession_print_slice_keeps_possession_cautious() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "na pa' inn-ah",
        "a zi' min",
        "Topa' inn",
        "a pa' inn",
        "Topa' tungah",
        "ka suahna leitang",
    ):
        assert required in text

    assert "not enough for a full possession paradigm" in lower or "does not yet justify a full possession paradigm" in lower
    assert "raw generated-report counts" in lower or "report-only" in lower

