from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
TEX_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.tex"
PDF_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.pdf"
SCRIPT_PATH = ROOT / "scripts/assemble_publication_review_preview.py"


def _text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _tex_text() -> str:
    return TEX_PATH.read_text(encoding="utf-8")


def test_assembled_grammar_review_preview_exists() -> None:
    assert PREVIEW_PATH.exists(), "Assembled grammar review preview must exist"


def test_assembled_preview_is_explicitly_a_review_preview() -> None:
    text = _text()
    lower = text.lower()

    assert "review preview, not a finished grammar" in lower
    assert "assembled from first-pass publication-review slices" in lower
    assert "intended to help human review and direct editing" in lower


def test_assembled_preview_names_controlling_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_checkpoint_after_transitivity.md",
        "whole_grammar_coverage_checkpoint_after_reduplication.md",
        "whole_grammar_coverage_audit.md",
        "SKELETON_GRAMMAR.md",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "PROGRESS.md",
    ):
        assert required in text


def test_assembled_preview_names_key_narrow_slice_anchors() -> None:
    text = _text()

    for required in (
        "bawlzoding",
        "`-sak`",
        "kanei / kainn",
        "ciangin",
        "`-na / bawlna`",
        "hih mite",
        "mi khat",
        "mi khempeuh",
        "`gam`",
        "aksi / aksi-te",
        "mahmah / taktak",
        "peuhpeuh",
        "sih / suak",
        "hawl / en",
    ):
        assert required in text


def test_assembled_preview_marks_major_gaps() -> None:
    text = _text()

    assert "[MAJOR GAP: phonology/tone remains blocked or theory-heavy.]" in text
    assert "[MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]" in text
    assert "[MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]" in text
    assert "[MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]" in text


def test_assembled_preview_does_not_claim_finished_grammar_or_pdf() -> None:
    text = _text()
    lower = text.lower()

    assert "does not claim that the whole grammar is finished" in lower
    assert "review preview pdf, not a final publication pdf" in lower


def test_assembled_preview_includes_actual_slice_prose() -> None:
    text = _text()

    for required in (
        "Clean intransitive anchor: sih",
        "Clean transitive anchor: hawl",
        "Full reduplication as intensification",
        "Temporal subordination: ciangin",
        "Deverbal nominalization with `-na`",
        "Basic NP ordering",
        "Simple noun stems",
        "Agreement versus possession routing",
        "Causative `-sak`",
    ):
        assert required in text


def test_assembled_preview_includes_source_lines_for_inserted_slices() -> None:
    text = _text()

    for required in (
        "Source slice: `output/publication_review/grammar_transitivity_print_slice.md`",
        "Source slice: `output/publication_review/grammar_reduplication_print_slice.md`",
        "Source slice: `output/publication_review/grammar_clause_linkage_print_slice.md`",
    ):
        assert required in text


def test_assembled_preview_tex_exists_and_includes_slice_content() -> None:
    tex = _tex_text()
    lower = tex.lower()

    assert TEX_PATH.exists(), "Assembled grammar review preview TeX must exist"
    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" in lower
    assert "\\texttt{sih} is the clean intransitive anchor for the first slice." in lower
    assert "\\texttt{hawl} is the clean transitive anchor for the first slice." in lower
    assert "\\texttt{mahmah} is the main full-reduplication intensifier anchor." in lower
    assert "with \\texttt{ciangin} as the clearest current anchor." in lower
    assert "basic np ordering" in lower
    assert "routing contrast, with \\texttt{kanei} as the clearest agreement anchor" in lower


def test_assembled_preview_pdf_exists_and_is_non_empty() -> None:
    assert PDF_PATH.exists(), "Assembled grammar review preview PDF must exist"
    assert PDF_PATH.stat().st_size > 0, "Assembled grammar review preview PDF must be non-empty"


def test_assembly_script_is_reproducible_for_markdown_and_tex() -> None:
    markdown_before = PREVIEW_PATH.read_bytes()
    tex_before = TEX_PATH.read_bytes()

    subprocess.run(
        ["python3", str(SCRIPT_PATH), "--skip-pdf"],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )

    assert PREVIEW_PATH.read_bytes() == markdown_before
    assert TEX_PATH.read_bytes() == tex_before
