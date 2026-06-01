from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from interlinear_latex import analyze_text, build_gll_lines, load_bible, reference_to_verse_id
from restore_tone import load_tone_dictionary


PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
TEX_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.tex"
PDF_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.pdf"
SCRIPT_PATH = ROOT / "scripts/assemble_publication_review_preview.py"
BIBLE_PATH = ROOT / "bibles" / "extracted" / "ctd" / "ctd-x-bible.txt"


def _text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _tex_text() -> str:
    return TEX_PATH.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _tex_example_block(label: str) -> str:
    tex = _tex_text()
    start = tex.index(f"\\label{{{label}}}")
    block_start = tex.rfind("\\begin{exe}", 0, start)
    block_end = tex.index("\\end{exe}", start) + len("\\end{exe}")
    return tex[block_start:block_end]


@lru_cache(maxsize=1)
def _tone_dict() -> dict[str, list[dict[str, str]]]:
    return load_tone_dictionary()


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


def test_assembled_preview_tex_uses_real_citation_and_gb4e_machinery() -> None:
    tex = _tex_text()

    assert "[@" not in tex
    assert "\\usepackage[]{natbib}" in tex
    assert "\\setcitestyle{authoryear,round,semicolon}" in tex
    assert "\\bibliographystyle{plainnat}" in tex
    assert "\\bibliography{../../literature/bibliography.bib}" in tex
    assert "\\citep{henderson1965, zamngaihcing2017}" in tex
    assert "\\usepackage{gb4e}" in tex
    assert "\\newcounter{reviewchapter}" in tex
    assert "\\renewcommand{\\thexnumi}{\\arabic{reviewchapter}.\\arabic{xnumi}}" in tex
    assert "\\begin{exe}" in tex
    assert "\\ex \\label{ex:dem-hih}" in tex
    assert "\\ex \\label{ex:dem-tua-ciangin}" in tex
    assert "\\ex \\label{ex:pro-amah}" in tex
    assert "\\gll " in tex
    assert "\\glt " in tex
    assert "Abbreviations" in tex


def test_assembled_preview_tex_contains_real_interlinear_example_content() -> None:
    block = _tex_example_block("ex:dem-hih")

    assert "\\begin{exe}" in block
    assert "\\gll H" in block
    assert "\\textsc{prox}" in block
    assert "\\textsc{top}" in block
    assert "\\glt 'This is the book of the generations of Adam.' (Genesis 5:1)" in block


def test_assembled_preview_tex_uses_shared_analyzer_output_for_known_bible_example() -> None:
    analysis = analyze_text("Hih pen Adam' suanlekhakte' laibu ahi hi.", _tone_dict())
    object_line, gloss_line = build_gll_lines(analysis)
    block = _tex_example_block("ex:dem-hih")

    assert object_line in block
    assert gloss_line in block


def test_assembled_preview_tex_places_bible_reference_after_translation() -> None:
    block = _tex_example_block("ex:dem-hih")

    assert "\\glt 'This is the book of the generations of Adam.' (Genesis 5:1)" in block
    assert block.index("\\glt") < block.index("Genesis 5:1")
    assert "Genesis 5:1\n\\gll" not in block


def test_assembled_preview_tex_eliminates_old_raw_example_block_prose() -> None:
    tex = _tex_text()

    assert "\\begin{reviewexample}" not in tex
    assert "\\reviewobjectline{" not in tex
    assert "\\reviewtranslation{" not in tex
    assert "a. Tedim:" not in tex
    assert "b. Segmentation:" not in tex
    assert "c. Gloss:" not in tex
    assert "d. Translation:" not in tex


def test_assembled_preview_assembler_reuses_shared_interlinear_helper() -> None:
    script_text = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "from interlinear_latex import (" in script_text
    assert "analyze_text" in script_text
    assert "build_gll_lines" in script_text
    assert "generate_abbreviations_section" in script_text
    assert "generate_gb4e_setup" in script_text
    assert "reference_to_verse_id" in script_text
    assert "analyzer-derived interlinear unavailable; using slice segmentation/gloss fallback" in script_text


def test_assembled_preview_bible_reference_mapping_hits_existing_ctd_bible_data() -> None:
    verse_id = reference_to_verse_id("Genesis 5:1")
    bible = load_bible(BIBLE_PATH)

    assert verse_id == "01005001"
    assert verse_id in bible
    assert "Adam" in bible[verse_id]


def test_assembled_preview_pdf_exists_and_is_non_empty() -> None:
    assert PDF_PATH.exists(), "Assembled grammar review preview PDF must exist"
    assert PDF_PATH.stat().st_size > 0, "Assembled grammar review preview PDF must be non-empty"


def test_assembled_preview_pdf_text_shows_parenthetical_citations_and_numbered_examples() -> None:
    pdf_text = _pdf_text()
    normalized = _normalize(pdf_text)
    lower = normalized.lower()

    assert "[@" not in pdf_text
    assert "[Henderson" not in pdf_text
    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" in lower
    assert "abbreviations" in lower
    assert "references" in lower
    assert re.search(r"\(Henderson,\s*1965.{0,20}Cing,\s*2017\)", normalized)
    assert "(2.1)" in pdf_text
    assert re.search(r"\(3\.\d+\)", pdf_text)
    assert re.search(r"\(4\.\d+\)", pdf_text)
    assert "Genesis 5:1" in pdf_text
    assert "book of the generations of Adam." in pdf_text
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
