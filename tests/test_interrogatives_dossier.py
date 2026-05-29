from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOSSIER_PATH = ROOT / "output/publication_review/dossier_interrogatives.md"


def test_interrogatives_dossier_exists() -> None:
    assert DOSSIER_PATH.exists()


def test_interrogatives_dossier_tracks_candidate_control_and_core_patterns() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "candidates_interrogatives.tsv" in text
    assert "candidate rows, not raw string hits, control the present analysis" in text.lower()
    assert "clause-final `hiam`" in text
    assert "WH + `hiam`" in text
    for item in ("`bang`", "`kua`", "`bangci`", "`banghangin`"):
        assert item in text


def test_interrogatives_dossier_keeps_embedded_and_blocked_material_conservative() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "bang hiam cih thei lo uh hi" in text
    assert "not print-ready" in text
    assert "Bang hang hiam cih leh" in text
    assert "blocked" in text
    assert "sharp-two-edged-sword" in text
    assert "bangmah" in text
    assert "bangin" in text
    assert "`maw`, `ham`, and `em`" in text
    assert "remain deferred" in text
