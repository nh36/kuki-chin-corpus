from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_quantifiers.md"


def test_quantifiers_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_quantifiers_dossier_names_control_layer_and_protocol() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "candidates_quantifiers.tsv" in text
    assert "candidate rows, not raw string hits and not generated-report counts" in lower
    assert "scripts/publication_review/extract_candidates.py" in text


def test_quantifiers_dossier_mentions_core_rows_and_boundaries() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for required in (
        "khempeuh",
        "pawlkhat",
        "mi khat",
        "kuamah mu lo",
        "bangmah om lo hi",
        "tampi tak",
        "vanglian zaw",
        "hau mahmah",
    ):
        assert required in text

    assert "peuhpeuh" in lower
    assert "tawm" in lower
    assert "deferred" in lower
    assert "not print-ready" in lower
    assert "numeral/indefinite boundary" in lower or "boundary evidence" in lower


def test_quantifiers_dossier_keeps_overlap_controls_and_blocked_material_visible() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "negative-licensed" in lower or "negative licensing" in lower
    assert "negation packet" in lower
    assert "bang-family" in lower or "interrogative-overlap" in lower
    assert "tua bangmah hi-in" in lower or "exodus 27:11" in lower
    assert "blocked" in lower
    assert "broad adjective or adverb chapter" in lower or "general comparison or degree-modification chapter" in lower
    assert "edge rows" in lower or "caveated boundary evidence" in lower


def test_quantifiers_dossier_avoids_raw_counts_and_marks_next_step() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    for banned in ("5,191", "4,712", "664", "525", "735", "1,351", "13,000+"):
        assert banned not in text

    assert "grammar, dictionary, and review-note print slices for quantifiers have **not** yet begun" in lower
    assert "grammar_quantifiers_print_slice.md" in text
