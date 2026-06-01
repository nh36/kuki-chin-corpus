from __future__ import annotations

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


def _text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _tex_text() -> str:
    return TEX_PATH.read_text(encoding="utf-8")


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


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalized_domain_only(text: str) -> str:
    return text.split("# 3. Predicate structure and verbal morphology", 1)[0]


def _normalized_domain_only_pdf(text: str) -> str:
    parts = re.split(r"\b3\s+Predicate structure and verbal morphology\b", text, maxsplit=1, flags=re.IGNORECASE)
    return parts[0]


def test_grammar_facing_output_suppresses_internal_scope_and_workflow_terms() -> None:
    text = _normalized_domain_only(_text()).lower()
    tex = _tex_text().lower()
    pdf = _normalized_domain_only_pdf(_pdf_text()).lower()

    for forbidden in (
        "\n# scope\n",
        "editorial scope",
        "candidate tsv",
        "dossier",
        "review notes",
        "print slice",
        "publication-review",
        "coverage normalization",
        "packet maturity",
    ):
        assert forbidden not in text
        assert forbidden not in pdf

    assert "\\section*{scope}" not in tex


def test_grammar_facing_output_uses_numbered_sections_and_subsections() -> None:
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex)

    assert r"\section{Phonology and tone}" in tex
    assert r"\section{Deixis, pronouns, and nominal" in tex
    assert r"\subsection{NP structure / possession}" in tex
    assert r"\subsection{Numerals}" in tex
    assert "Deixis, pronouns, and nominal domain" in tex_normalized
    assert re.search(r"\n2\s+Deixis, pronouns, and nominal domain", pdf)
    assert re.search(r"\n2\.\d+\s+NP structure / possession", pdf)


def test_grammar_facing_output_glosses_key_inline_tedim_forms() -> None:
    tex = _normalize(_tex_text())

    for required in (
        r"\tdim{gam} \glossquote{land / country}",
        r"\tdim{aksi} \glossquote{star}",
        r"\tdim{mi} \glossquote{person}",
        r"\tdim{mite} \glossquote{people}",
        r"\tdim{sawm} \glossquote{ten}",
        r"\tdim{khempeuh} \glossquote{all}",
        r"\tdim{hih} \glossquote{this}",
    ):
        assert required in tex


def test_grammar_facing_output_fixes_quote_handling_and_preserves_tedim_apostrophes() -> None:
    tex = _tex_text()

    assert r"\newcommand{\glossquote}[1]{`#1'}" in tex
    assert r"\glt \glossquote{This is the book of the generations of Adam.} (Genesis 5:1)" in tex
    assert r"\glt '" not in tex
    assert r"\tdim{na pa' inn-ah}" in tex
    assert r"\tdim{Abraham' suan David}" in tex
    assert r"\tdim{Topa' inn}" in tex


def test_grammar_facing_output_keeps_deferred_notes_visible_without_candidate_row_language() -> None:
    text = _text().lower()
    pdf = _pdf_text().lower()

    assert "deferred and boundary material" in text
    assert "deferred and boundary material" in pdf
    assert "candidate row" not in text
    assert "candidate row" not in pdf
