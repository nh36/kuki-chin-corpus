from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/dictionary_interrogatives_print_slice.md"


def test_interrogatives_dictionary_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_interrogatives_dictionary_slice_names_control_and_cross_reference_files() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    assert "candidates_interrogatives.tsv" in text
    assert "dossier_interrogatives.md" in text
    assert "grammar_interrogatives_print_slice.md" in text


def test_interrogatives_dictionary_slice_has_core_entries() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    for heading in ("## hiam", "## bang", "## kua", "## bangci", "## banghangin"):
        assert heading in text


def test_interrogatives_dictionary_slice_keeps_attested_hiam_example_and_not_old_main_paraphrase() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    assert "Na pa inn-ah kote giah nading a awng ding hiam" in text
    assert "Tedim: Inn-ah hong tum theih na hiam" not in text


def test_interrogatives_dictionary_slice_covers_bang_kua_bangci_and_banghangin_with_caveats() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Bang ahi hiam?" in text
    assert "bangmah" in text
    assert "bangin" in text
    assert "Hihte kua ahi hiam?" in text
    assert "`NUM`" in text or "NUM" in text
    assert "Bangci a hici gamtat na hi hiam?" in text
    assert "bang hangin na mai sia ahi hiam" in text
    assert "bang | hang-in" in text
    assert "segmentation caveat" in lower


def test_interrogatives_dictionary_slice_keeps_embedded_blocked_and_deferred_material_conservative() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")
    lower = text.lower()

    assert "Bang hiam cih thei lo uh hi" in text
    assert "not yet promoted" in lower or "not yet a full draft-ready dictionary entry" in lower or "deferred" in lower
    assert "Bang hang hiam cih leh" in text
    assert "a hiam ciat uh" in text
    assert "langnih a hiam namsau" in text
    assert "`maw`, `ham`, and `em`" in text
    assert "remain deferred" in lower


def test_interrogatives_dictionary_slice_avoids_raw_counts_and_machine_dictionary_edits() -> None:
    text = SLICE_PATH.read_text(encoding="utf-8")

    assert "5,230" not in text
    assert "10,000+" not in text
    assert "machine dictionary files" in text
