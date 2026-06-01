from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
TEX_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.tex"
PDF_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.pdf"
SCRIPT_PATH = ROOT / "scripts/assemble_publication_review_preview.py"


def _text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _tex_text() -> str:
    return TEX_PATH.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@lru_cache(maxsize=1)
def _pdf_text() -> str:
    pdftotext = shutil.which("pdftotext")
    if pdftotext:
        with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
            subprocess.run(
                [pdftotext, str(PDF_PATH), tmp.name],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            return Path(tmp.name).read_text(encoding="utf-8", errors="replace")

    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover - environment-dependent skip
        pytest.skip(f"No PDF text extraction tool available: {exc}")

    reader = PdfReader(str(PDF_PATH))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


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


def test_assembled_preview_tex_exists_and_keeps_preview_status() -> None:
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


def test_assembled_preview_tex_uses_real_citation_and_example_machinery() -> None:
    tex = _tex_text()

    assert "[@" not in tex
    assert "\\usepackage[]{natbib}" in tex
    assert "\\bibliographystyle{plainnat}" in tex
    assert "\\bibliography{../../literature/bibliography.bib}" in tex
    assert "\\citep{henderson1965, zamngaihcing2017}" in tex
    assert "\\newcounter{reviewchapter}" in tex
    assert "\\renewcommand{\\thereviewexample}{\\arabic{reviewchapter}.\\arabic{reviewexample}}" in tex
    assert "\\begin{reviewexample}{ex:dem-hih}{Genesis 5:1}" in tex
    assert "\\begin{reviewexample}{ex:dem-tua-ciangin}{Genesis 1:3}" in tex
    assert "\\begin{reviewexample}{ex:pro-amah}{}" in tex
    assert "\\reviewobjectline{" in tex
    assert "\\reviewtranslation{" in tex


def test_assembled_preview_tex_contains_real_interlinear_example_content() -> None:
    tex = _tex_text()
    start = tex.index("\\begin{reviewexample}{ex:dem-hih}{Genesis 5:1}")
    end = tex.index("\\end{reviewexample}", start)
    block = tex[start:end]

    assert "Hih pen Adam’ suanlekhakte’ laibu ahi hi." in block
    assert "hih & pen \\\\" in block
    assert "\\textsc{prox} & \\textsc{top} \\\\" in block
    assert '\\reviewtranslation{"This is the book of the generations of Adam."}' in block


def test_assembled_preview_tex_eliminates_old_raw_example_block_prose() -> None:
    tex = _tex_text()

    assert "a. Tedim:" not in tex
    assert "b. Segmentation:" not in tex
    assert "c. Gloss:" not in tex
    assert "d. Translation:" not in tex


def test_assembled_preview_pdf_exists_and_is_non_empty() -> None:
    assert PDF_PATH.exists(), "Assembled grammar review preview PDF must exist"
    assert PDF_PATH.stat().st_size > 0, "Assembled grammar review preview PDF must be non-empty"


def test_assembled_preview_pdf_text_shows_resolved_citations_and_numbered_examples() -> None:
    pdf_text = _pdf_text()
    normalized = _normalize(pdf_text)
    lower = normalized.lower()

    assert "[@" not in pdf_text
    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" in lower
    assert "references" in lower
    assert "henderson" in lower
    assert "(2.1)" in pdf_text
    assert "(3.1)" in pdf_text
    assert "(4.1)" in pdf_text
    assert "Genesis 5:1" in pdf_text
    assert "Full reduplication as intensification" in pdf_text


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
