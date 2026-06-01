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

from assemble_publication_review_preview import (
    SOURCE_AUDIT_EXCEPTIONS,
    parse_examples,
    resolve_example_source,
)
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


def _source_examples() -> list[tuple[str, str]]:
    bible = load_bible(BIBLE_PATH)
    examples = []
    for example in parse_examples(_text()):
        if example.label != "review-preview-warning":
            resolved_source = resolve_example_source(example, bible)
            if resolved_source:
                examples.append((example.label, resolved_source))
    return examples


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
        "Overview of noun phrase structure",
        "Simple noun stems",
        "Agreement versus possession routing",
        "Causative `-sak`",
        ):
        assert required in text


def test_assembled_preview_includes_normalized_numerals_section() -> None:
    text = _text()

    for required in (
        "normalized publication-facing numerals section",
        "Overview of the numeral system",
        "Cardinal numerals",
        "Decimal composition",
        "Counting phrases and word order",
        "Classifier-like and counting expressions",
        "Distributive numerals",
        "Ambiguity controls",
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
    normalized = _normalize(lower)

    assert TEX_PATH.exists(), "Assembled grammar review preview TeX must exist"
    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" in lower
    assert "\\tdim{sih} is the clean intransitive anchor for the first slice." in lower
    assert "\\tdim{hawl} is the clean transitive anchor for the first slice." in lower
    assert "\\tdim{mahmah} is the main full-reduplication intensifier anchor." in lower
    assert "with \\tdim{ciangin} as the clearest current anchor." in lower
    assert "overview of noun phrase structure" in normalized
    assert "routing contrast, with \\tdim{kanei} as the clearest agreement anchor" in lower
    assert "cardinal numerals" in lower
    assert "decimal composition" in lower
    assert "occurrence-counting" in lower or "occurrence counting" in lower


def test_assembled_preview_tex_uses_real_citation_and_gb4e_machinery() -> None:
    tex = _tex_text()

    assert "[@" not in tex
    assert "\\usepackage[]{natbib}" in tex
    assert "\\setcitestyle{authoryear,round,semicolon}" in tex
    assert "\\bibliographystyle{plainnat}" in tex
    assert "\\bibliography{../../literature/bibliography.bib}" in tex
    assert "\\citep{henderson1965, zamngaihcing2017}" in tex
    assert "\\usepackage{gb4e}" in tex
    assert "\\newcommand{\\tdim}[1]{\\textit{#1}}" in tex
    assert "\\newcommand{\\tdimword}[1]{\\textit{#1}}" in tex
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
    assert "\\gll \\tdimword{" in block
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


def test_assembled_preview_tex_systematically_preserves_example_sources_after_translation() -> None:
    tex = _tex_text()
    missing = []

    for label, rendered_source in _source_examples():
        if label in SOURCE_AUDIT_EXCEPTIONS:
            continue
        block = _tex_example_block(label)
        glt_line = next(line for line in block.splitlines() if line.startswith("\\glt "))
        if rendered_source not in glt_line:
            missing.append(f"{label}: {rendered_source}")

    assert not missing, f"Missing source references after translation: {missing}"


def test_assembled_preview_tex_keeps_expected_sources_for_known_examples() -> None:
    assert "\\glt 'This is the book of the generations of Adam.' (Genesis 5:1)" in _tex_example_block("ex:dem-hih")
    assert "(Genesis 1:6)" in _tex_example_block("ex:dem-tua")
    assert "(Genesis 1:3)" in _tex_example_block("ex:dem-tua-ciangin")
    assert "(Exodus 14:30)" in _tex_example_block("ex:dem-tua-bangin")
    assert "(Genesis 4:5)" in _tex_example_block("ex:neg-lo")


def test_assembled_preview_tex_includes_normalized_numerals_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()

    assert text.count("(@ex:num-") >= 4
    assert tex.count("\\label{ex:num-") >= 4

    for required in ("khat", "nih", "thum", "li", "nga", "guk", "sagih", "giat", "kua", "sawm", "za", "sing", "tul"):
        assert required in text.lower()
        assert required in tex.lower()

    for required in ("Cardinal numerals", "Decimal composition", "ni li", "kum sawm le nih", "sawmvei"):
        assert required.lower() in pdf.lower()


def test_assembled_preview_tex_keeps_numerals_example_sources_after_translation() -> None:
    assert "(Genesis 11:10)" in _tex_example_block("ex:num-kum-nih")
    assert "(Genesis 7:10)" in _tex_example_block("ex:num-ni-sagih")
    assert "(John 11:39)" in _tex_example_block("ex:num-ni-li")
    assert "(Genesis 5:9)" in _tex_example_block("ex:num-sawmkua")
    assert "(Matthew 9:20)" in _tex_example_block("ex:num-kum-sawm-le-nih")
    assert "(Genesis 7:11)" in _tex_example_block("ex:num-nihna")
    assert "(Genesis 31:7)" in _tex_example_block("ex:num-sawmvei")


def test_assembled_preview_numerals_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 11:10)" in tex
    assert "(John 11:39)" in tex or "(Matthew 9:20)" in tex or "no suitable Gospel example" in _text()


def test_assembled_preview_includes_normalized_quantifiers_section() -> None:
    text = _text()

    for required in (
        "normalized publication-facing quantifiers section",
        "Overview of quantification in Tedim",
        "Quantifier inventory",
        "Universal / total quantifiers",
        "Existential / indefinite-like quantifiers",
        "Quantifiers and negation",
        "Quantifiers and noun phrase structure",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_noun_domain_section() -> None:
    text = _text()

    for required in (
        "normalized publication-facing noun domain section",
        "Overview of the noun domain",
        "Current noun-domain inventory",
        "Simple noun stems",
        "Plural marking with -te",
        "Human nouns and common nouns",
        "Nouns in larger phrases",
        "Compounds and proper nouns",
        "Nominalization boundary",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_np_possession_section() -> None:
    text = _text()

    for required in (
        "normalized publication-facing NP structure / possession section",
        "Overview of noun phrase structure",
        "Current NP pattern inventory",
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_tex_includes_normalized_np_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:np-") >= 4
    assert tex.count("\\label{ex:np-") >= 4

    for required in ("hih mite", "mi khat", "mi khempeuh", "ni li", "na pa' inn-ah", "Current NP pattern inventory"):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in ("Current NP pattern inventory", "hih mite", "mi khempeuh", "na pa", "ni li"):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_keeps_np_example_sources_after_translation() -> None:
    assert "(Exodus 5:5)" in _tex_example_block("ex:np-hih-mite")
    assert "(John 11:39)" in _tex_example_block("ex:np-ni-li")
    assert "(Luke 2:1)" in _tex_example_block("ex:np-mi-khempeuh")
    assert "(Genesis 24:23)" in _tex_example_block("ex:np-poss-na-pa-inn")
    assert "(Genesis 3:20)" in _tex_example_block("ex:np-poss-a-zi-min")


def test_assembled_preview_np_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Exodus 5:5)" in tex or "(Genesis 24:23)" in tex or "(Genesis 3:20)" in tex
    assert "(John 11:39)" in tex or "(Luke 2:1)" in tex or "no suitable Gospel example was found" in text


def test_assembled_preview_tex_includes_normalized_noun_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:noun-") >= 4
    assert tex.count("\\label{ex:noun-") >= 4

    for required in ("Current noun-domain inventory", "gam", "aksi-te", "hih mite", "mi khempeuh", "minam khat"):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in ("Current noun-domain inventory", "gam", "aksi-te", "hih mite", "mi khempeuh"):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_keeps_noun_example_sources_after_translation() -> None:
    assert "(Genesis 2:5)" in _tex_example_block("ex:noun-gam")
    assert "(Matthew 2:2)" in _tex_example_block("ex:noun-aksi")
    assert "(Genesis 1:16)" in _tex_example_block("ex:noun-aksi-te")
    assert "(Exodus 5:5)" in _tex_example_block("ex:noun-hih-mite")
    assert "(Luke 2:1)" in _tex_example_block("ex:noun-mi-khempeuh")
    assert "(Genesis 11:6)" in _tex_example_block("ex:noun-minam-khat")


def test_assembled_preview_noun_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 2:5)" in tex or "(Genesis 1:16)" in tex or "(Exodus 5:5)" in tex
    assert "(Matthew 2:2)" in tex or "(Luke 2:1)" in tex or "no suitable Gospel example was found" in text


def test_assembled_preview_tex_includes_normalized_quantifiers_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()

    assert text.count("(@ex:quant-") >= 4
    assert tex.count("\\label{ex:quant-") >= 4

    for required in ("khempeuh", "pawlkhat", "kuamah", "bangmah", "tampi", "Quantifier inventory"):
        assert required.lower() in text.lower()
        assert required.lower() in tex.lower()

    for required in ("Quantifier inventory", "mi khempeuh", "mi pawlkhat", "mi tampi"):
        assert required.lower() in pdf.lower()


def test_assembled_preview_tex_keeps_quantifiers_example_sources_after_translation() -> None:
    assert "(Genesis 2:1)" in _tex_example_block("ex:quant-khempeuh")
    assert "(Luke 2:1)" in _tex_example_block("ex:quant-mi-khempeuh")
    assert "(Matthew 2:1)" in _tex_example_block("ex:quant-mi-pawlkhat")
    assert "(Exodus 2:12)" in _tex_example_block("ex:quant-kuamah")
    assert "(John 3:27)" in _tex_example_block("ex:quant-kuamah-bangmah")
    assert "(Mark 6:34)" in _tex_example_block("ex:quant-mi-tampi")


def test_assembled_preview_quantifiers_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 2:1)" in tex or "(Exodus 2:12)" in tex
    assert "(Luke 2:1)" in tex or "(Matthew 2:1)" in tex or "(Mark 6:34)" in tex or "(John 3:27)" in tex or "no suitable Gospel example was found" in text


def test_assembled_preview_tex_keeps_expected_sources_for_examples_2_11_to_2_14() -> None:
    assert "(Genesis 13:8)" in _tex_example_block("ex:pro-eite")
    assert "(Genesis 34:9)" in _tex_example_block("ex:pro-kote")
    assert "(Genesis 24:23)" in _tex_example_block("ex:poss-na")
    assert "(Genesis 3:20)" in _tex_example_block("ex:poss-a")


def test_assembled_preview_tex_italicizes_tedim_example_tier_without_italicizing_gloss_tier() -> None:
    block = _tex_example_block("ex:dem-hih")

    assert "\\tdimword{" in block
    assert "\\gll \\tdimword{" in block
    assert "\\textsc{prox}" in block
    gloss_line = next(line for line in block.splitlines() if "\\textsc{prox}" in line)
    assert "\\tdimword{" not in gloss_line


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
    assert "format_inline_tedim" in script_text
    assert "reference_to_verse_id" in script_text
    assert "analyzer-derived interlinear unavailable; using slice segmentation/gloss fallback" in script_text
    assert "audit_example_sources" in script_text


def test_assembled_preview_tex_distinguishes_inline_tedim_from_technical_paths() -> None:
    tex = _tex_text()

    assert "\\texttt{output/publication\\_review/grammar\\_transitivity\\_print\\_slice.md}" in tex
    assert "\\texttt{python3\\ scripts/assemble\\_publication\\_review\\_preview.py}" in tex
    assert "\\tdim{hih}" in tex
    assert "\\tdim{tua}" in tex
    assert "\\tdim{mahmah}" in tex
    assert "\\tdim{ciangin}" in tex
    assert "\\tdim{gam}" in tex


def test_assembled_preview_gap_and_review_status_text_are_not_aggressively_italicized() -> None:
    tex = _tex_text()

    assert "{[}MAJOR GAP: phonology/tone remains blocked or theory-heavy.{]}" in tex
    assert "\\tdim{review preview, not a finished grammar}" not in tex


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


def test_assembled_preview_pdf_text_keeps_source_references_systematically() -> None:
    pdf_text = _pdf_text()

    assert "book of the generations of Adam.’ (Genesis 5:1)" in pdf_text or "book of the generations of Adam.' (Genesis 5:1)" in pdf_text
    assert "(Genesis 1:6)" in pdf_text
    assert "(Genesis 1:3)" in pdf_text
    assert "(Exodus 14:30)" in pdf_text
    assert "(Genesis 4:5)" in pdf_text


def test_assembled_preview_pdf_text_keeps_sources_for_examples_2_11_to_2_14() -> None:
    pdf_text = _pdf_text()

    assert "(2.11)" in pdf_text and "(Genesis 13:8)" in pdf_text
    assert "(2.12)" in pdf_text and "(Genesis 34:9)" in pdf_text
    assert "(2.13)" in pdf_text and "(Genesis 24:23)" in pdf_text
    assert "(2.14)" in pdf_text and "(Genesis 3:20)" in pdf_text


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
