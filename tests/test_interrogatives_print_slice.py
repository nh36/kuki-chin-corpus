from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_interrogatives_print_slice.md"


def test_interrogatives_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_interrogatives_print_slice_names_control_files_and_core_patterns() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    assert "candidates_interrogatives.tsv" in text
    assert "dossier_interrogatives.md" in text
    assert "clause-final `hiam`" in text
    assert "WH + `hiam`" in text
    for item in ("`bang`", "`kua`", "`bangci`", "`banghangin`"):
        assert item in text


def test_interrogatives_print_slice_uses_attested_yes_no_clause_and_not_old_paraphrase() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    assert "Na pa inn-ah kote giah nading a awng ding hiam" in text
    assert "Tedim: Inn-ah hong tum theih na hiam" not in text


def test_interrogatives_print_slice_keeps_deferred_and_blocked_material_out_of_core_analysis() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "bang hiam cih thei lo uh hi" in text
    assert "deferred" in lower or "not promoted" in lower or "not print-ready" in lower
    assert "Bang hang hiam cih leh" in text
    assert "formulaic explanatory frame" in lower
    assert "langnih a hiam namsau" in text
    assert "bangmah" in text
    assert "bangin" in text
    assert "`maw`, `ham`, and `em`" in text
    assert "remain deferred" in lower


def test_interrogatives_print_slice_avoids_raw_count_claims_and_overstrong_generalizations() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "5,230" not in text
    assert "10,000+" not in text
    assert "always clause-final" not in lower
