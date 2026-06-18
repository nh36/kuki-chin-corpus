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
QUALITY_REPORT_PATH = ROOT / "output/publication_review/grammar_facing_quality_report.md"
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


def test_assembled_preview_quality_report_exists_and_is_clean() -> None:
    assert QUALITY_REPORT_PATH.exists(), "Grammar-facing quality report must exist"
    report = QUALITY_REPORT_PATH.read_text(encoding="utf-8")

    assert "- Issues: 0" in report
    assert "- All configured grammar-facing quality gates passed." in report


def test_assembled_preview_is_explicitly_a_review_preview() -> None:
    text = _text()
    lower = text.lower()

    assert "review preview, not a finished grammar" in lower
    assert "assembled draft of the current tedim grammar sections" in lower
    assert "end-of-section caveats remain visible" in lower


def test_assembled_preview_frontmatter_suppresses_internal_workflow_apparatus() -> None:
    text = _text()
    lower = text.lower()

    for forbidden in (
        "whole_grammar_coverage_checkpoint_after_transitivity.md",
        "whole_grammar_coverage_checkpoint_after_reduplication.md",
        "whole_grammar_coverage_audit.md",
        "skeleton_grammar.md",
        "grammar_source_inventory.md",
        "source slice:",
        "pdf/build status",
        "known narrow-slice limitations",
        "end state of this preview",
        ):
        assert forbidden not in lower


def test_assembler_defaults_to_grammar_facing_mode_and_runs_quality_gate() -> None:
    script = SCRIPT_PATH.read_text(encoding="utf-8")

    assert 'parser.add_argument(\n        "--grammar-facing",' in script
    assert "default=True" in script
    assert 'help="build the grammar-facing review preview (default)"' in script
    assert "if args.grammar_facing:\n        run_quality_gate(TEX_OUTPUT)" in script


def test_assembled_preview_includes_phonology_and_tone_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of phonology and tone in Tedim",
        "Orientation table",
        "Segmental phonology",
        "Orthography and syllable shape",
        "Tone status",
        "The blocked -a issue",
        "Boundaries with stem alternation, TAM, `-pih`, and verb paradigms",
        "What can be printed now",
    ):
        assert required in text

    for required in (
        "overview of phonology and tone in tedim",
        "orientation table",
        "segmental phonology",
        "orthography and syllable shape",
        "tone status",
        "the blocked -a issue",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert "a full discussion of phonology and tone is not yet included" not in text.lower()


def test_assembled_preview_includes_normalized_interrogatives_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of interrogatives in Tedim",
        "Interrogative inventory",
        "Clause-final `hiam` 'question particle'",
        "WH + `hiam` content questions",
        "Embedded-question boundary",
        "Blocked false friends and non-interrogative `hiam`",
        "Deferred comparison particles",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    for required in (
        "overview of interrogatives in tedim",
        "interrogative inventory",
        "question particle",
        "wh +",
        "embedded-question boundary",
        "blocked false friends and non-interrogative",
        "deferred comparison particles",
        "several issues remain outside the present account.",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert text.count("(@ex:int-") >= 10
    assert tex.count("\\label{ex:int-") >= 10
    assert "interrogative inventory" in pdf.lower()


def test_assembled_preview_includes_normalized_sentence_final_particles_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of sentence-final particles in Tedim",
        "Sentence-final particle inventory",
        "Declarative `hi` with copula overlap",
        "Negative-plus-declarative `lo hi`",
        "Optative or jussive `hen`",
        "Imperative `in` and `un`",
        "`Hiam` as interrogatives overlap",
        "`Aw` as vocative or exclamative boundary",
        "`Tahen`, `ta`, and `zo` as deferred TAM-overlap material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    for required in (
        "overview of sentence-final particles in tedim",
        "sentence-final particle inventory",
        "declarative",
        "negative-plus-declarative",
        "optative or jussive",
        "imperative",
        "interrogatives overlap",
        "vocative or exclamative boundary",
        "deferred tam-overlap material",
        "several issues remain outside the present account.",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert text.count("(@ex:sfp-") >= 8
    assert tex.count("\\label{ex:sfp-") >= 8
    assert "sentence-final particle inventory" in pdf.lower()


def test_assembled_preview_includes_normalized_negation_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of negation in Tedim",
        "Negation inventory",
        "Clause-level negation with `lo`",
        "Dependent and derived negation with `loh`",
        "`kei` in prohibitives and irrealis-heavy negation",
        "Ordinary plural negative predicates are not automatically prohibitive",
        "Negative existence and absence",
        "Cessative `nawn lo`",
        "Ability and inability",
        "Negative polarity items",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    for required in (
        "overview of negation in tedim",
        "negation inventory",
        "clause-level negation with",
        "dependent and derived negation with",
        "prohibitives and irrealis-heavy negation",
        "negative existence and absence",
        "ability and inability",
        "negative polarity items",
        "several issues remain outside the present account.",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert text.count("(@ex:neg-") >= 10
    assert tex.count("\\label{ex:neg-") >= 10
    assert "negation inventory" in normalized_pdf


def test_assembled_preview_tex_keeps_negation_example_sources_after_translation() -> None:
    assert "(Genesis 4:5)" in _tex_example_block("ex:neg-lo")
    assert "(Matthew 2:10)" in _tex_example_block("ex:neg-lo-matt2-10")
    assert "(Genesis 3:11)" in _tex_example_block("ex:neg-loh")
    assert "(Matthew 5:19)" in _tex_example_block("ex:neg-loh-matt5-19")
    assert "(Genesis 22:12)" in _tex_example_block("ex:neg-kei")
    assert "(Mark 1:25)" in _tex_example_block("ex:neg-kei-mark1-25")
    assert "(Genesis 37:24)" in _tex_example_block("ex:neg-om-lo-gen37-24")
    assert "(John 14:30)" in _tex_example_block("ex:neg-nei-lo-john14-30")
    assert "(Genesis 8:12)" in _tex_example_block("ex:neg-nawn-lo-gen8-12")
    assert "(Matthew 28:6)" in _tex_example_block("ex:neg-nawn-lo-matt28-6")
    assert "(Genesis 27:23)" in _tex_example_block("ex:neg-thei-lo")
    assert "(John 9:4)" in _tex_example_block("ex:neg-theih-loh-john9-4")
    assert "(Exodus 2:12)" in _tex_example_block("ex:neg-kuamah")
    assert "(Matthew 22:46)" in _tex_example_block("ex:neg-kuamah-matt22-46")


def test_assembled_preview_negation_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 4:5)" in tex or "(Exodus 2:12)" in tex
    assert "(Matthew 2:10)" in tex or "(Mark 1:25)" in tex or "(John 14:30)" in tex


def test_assembled_preview_includes_normalized_coordinators_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of coordinators in Tedim",
        "Coordinator inventory",
        "NP coordination with `le`",
        "Conditional and boundary `leh`",
        "Sequential `a` and agreement false friends",
        "Deferred `mawh` material",
        "Adversative `Ahih hangin`",
        "Conditional-adversative `ahih kei leh`",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    for required in (
        "overview of coordinators in tedim",
        "coordinator inventory",
        "np coordination with",
        "conditional and boundary",
        "sequential",
        "deferred",
        "adversative",
        "conditional-adversative",
        "several issues remain outside the present account.",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert text.count("(@ex:coord-") >= 7
    assert tex.count("\\label{ex:coord-") >= 7
    assert "coordinator inventory" in normalized_pdf


def test_assembled_preview_tex_keeps_coordinators_example_sources_after_translation() -> None:
    assert "(Genesis 1:1)" in _tex_example_block("ex:coord-le-np")
    assert "(Matthew 24:35)" in _tex_example_block("ex:coord-le-np-matt24-35")
    assert "(Genesis 13:9)" in _tex_example_block("ex:coord-leh-boundary")
    assert "(Genesis 2:10)" in _tex_example_block("ex:coord-a-sequential-boundary")
    assert "(Genesis 3:4)" in _tex_example_block("ex:coord-ahih-hangin")
    assert "(Mark 3:4)" in _tex_example_block("ex:coord-ahih-hangin-mark3-4")
    assert "(Exodus 12:3)" in _tex_example_block("ex:coord-ahih-kei-leh")
    assert "(Matthew 11:3)" in _tex_example_block("ex:coord-ahih-kei-leh-matt11-3")


def test_assembled_preview_coordinators_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 1:1)" in tex or "(Exodus 12:3)" in tex
    assert "(Matthew 24:35)" in tex or "(Mark 3:4)" in tex or "(Matthew 11:3)" in tex


def test_assembled_preview_includes_normalized_reduplication_section() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    normalized_tex = _normalize(tex.lower())
    normalized_pdf = _normalize(pdf.lower())

    for required in (
        "Overview of reduplication in Tedim",
        "Reduplication inventory",
        "Full reduplication as intensification",
        "Secondary distributive reduplication",
        "Boundary and deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    for required in (
        "overview of reduplication in tedim",
        "reduplication inventory",
        "full reduplication as intensification",
        "secondary distributive reduplication",
        "boundary and deferred material",
        "several issues remain outside the present account.",
    ):
        assert required in normalized_tex
        assert required in normalized_pdf

    assert text.count("(@ex:red-") >= 6
    assert tex.count("\\label{ex:red-") >= 6
    assert "reduplication inventory" in normalized_pdf


def test_assembled_preview_tex_keeps_reduplication_example_sources_after_translation() -> None:
    assert "(Genesis 1:31)" in _tex_example_block("ex:red-mahmah-gen1-31")
    assert "(Matthew 2:3)" in _tex_example_block("ex:red-mahmah-matt2-3")
    assert "(Genesis 27:24)" in _tex_example_block("ex:red-taktak-gen27-24")
    assert "(Matthew 27:54)" in _tex_example_block("ex:red-taktak-matt27-54")
    assert "(Genesis 18:14)" in _tex_example_block("ex:red-peuhpeuh-gen18-14")
    assert "(Matthew 10:11)" in _tex_example_block("ex:red-peuhpeuh-matt10-11")


def test_assembled_preview_reduplication_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 1:31)" in tex or "(Genesis 27:24)" in tex or "(Genesis 18:14)" in tex
    assert "(Matthew 2:3)" in tex or "(Matthew 27:54)" in tex or "(Matthew 10:11)" in tex


def test_assembled_preview_tex_keeps_sentence_final_particles_example_sources_after_translation() -> None:
    assert "(Genesis 1:13)" in _tex_example_block("ex:sfp-ahi-hi-gen1-13")
    assert "(Matthew 1:1)" in _tex_example_block("ex:sfp-ahi-hi-matt1-1")
    assert "(Genesis 4:5)" in _tex_example_block("ex:sfp-lo-hi-gen4-5")
    assert "(Matthew 2:10)" in _tex_example_block("ex:sfp-lo-hi-matt2-10")
    assert "(Genesis 1:3)" in _tex_example_block("ex:sfp-hen-gen1-3")
    assert "(Matthew 6:9)" in _tex_example_block("ex:sfp-hen-matt6-9")
    assert "(Genesis 6:14)" in _tex_example_block("ex:sfp-in-gen6-14")
    assert "(Luke 23:34)" in _tex_example_block("ex:sfp-in-luke23-34")
    assert "(Psalms 100:1)" in _tex_example_block("ex:sfp-un-ps100-1")
    assert "(Matthew 3:3)" in _tex_example_block("ex:sfp-un-matt3-3")


def test_assembled_preview_sentence_final_particles_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 1:13)" in tex or "(Genesis 4:5)" in tex or "(Psalms 100:1)" in tex
    assert "(Matthew 1:1)" in tex or "(Matthew 6:9)" in tex or "(Luke 23:34)" in tex


def test_assembled_preview_tex_keeps_interrogatives_example_sources_after_translation() -> None:
    assert "(Genesis 24:23)" in _tex_example_block("ex:int-hiam-gen24-23")
    assert "(Matthew 6:25)" in _tex_example_block("ex:int-hiam-matt6-25")
    assert "(Genesis 48:8)" in _tex_example_block("ex:int-kua-gen48-8")
    assert "(Matthew 16:15)" in _tex_example_block("ex:int-kua-matt16-15")
    assert "(Genesis 3:13)" in _tex_example_block("ex:int-bangci-gen3-13")
    assert "(Matthew 12:26)" in _tex_example_block("ex:int-bangci-matt12-26")


def test_assembled_preview_interrogatives_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 24:23)" in tex
    assert "(Matthew 6:25)" in tex
    assert "(Luke 23:34)" in tex


def test_assembled_preview_does_not_claim_finished_grammar_or_pdf() -> None:
    text = _text()
    lower = text.lower()

    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" not in lower


def test_assembled_preview_includes_actual_slice_prose() -> None:
    text = _text()

    for required in (
        "Overview of Form I / Form II stem alternation",
        "Overview of basic finite verb paradigms in Tedim",
        "Basic finite paradigm inventory",
        "Current stem alternation overview",
        "Overview of transitivity contrasts",
        "Current transitivity inventory",
        "Full reduplication as intensification",
        "Core temporal subordination: ciangin",
        "Deverbal nominalization with `-na`",
        "Overview of noun phrase structure",
            "Simple lexical nouns",
        "Agreement versus possession routing",
        "Causative `-sak`",
        ):
        assert required in text


def test_assembled_preview_includes_normalized_numerals_section() -> None:
    text = _text()

    for required in (
        "Overview of the numeral system",
        "Cardinal inventory",
        "Compound numerals",
        "Noun-plus-numeral word order",
        "Ordinals and the `-na` boundary",
        "Multiplicative and counting expressions",
        "Ambiguity controls: `kua` and `khat`",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_hides_source_slice_lines() -> None:
    text = _text()

    for forbidden in (
        "Source slice: `output/publication_review/grammar_transitivity_print_slice.md`",
        "Source slice: `output/publication_review/grammar_reduplication_print_slice.md`",
        "Source slice: `output/publication_review/grammar_clause_linkage_print_slice.md`",
    ):
        assert forbidden not in text


def test_assembled_preview_tex_exists_and_keeps_preview_status() -> None:
    tex = _tex_text()
    lower = tex.lower()
    normalized = _normalize(lower)

    assert TEX_PATH.exists(), "Assembled grammar review preview TeX must exist"
    assert "review preview, not a finished grammar" in lower
    assert "\\setcounter{secnumdepth}{3}" in tex
    assert "\\setcounter{tocdepth}{2}" in tex
    assert "overview of form i / form ii stem alternation" in normalized
    assert "overview of basic finite verb paradigms in tedim" in normalized
    assert "basic finite paradigm inventory" in normalized
    assert "current stem alternation overview" in normalized
    assert "overview of transitivity contrasts" in normalized
    assert "\\tdim{sih}" in lower
    assert "\\tdim{hawl}" in lower
    assert "\\tdim{mahmah} is the main full-reduplication intensifier anchor." in lower
    assert "\\tdim{ciangin}" in lower
    assert "overview of noun phrase structure" in normalized
    assert "\\tdim{kanei}" in lower
    assert "cardinal inventory" in lower
    assert "compound numerals" in lower
    assert "overview of interrogatives in tedim" in normalized
    assert "interrogative inventory" in normalized
    assert "overview of sentence-final particles in tedim" in normalized
    assert "sentence-final particle inventory" in normalized
    assert "\\tdim{hiam}" in lower
    assert "\\tdim{hen}" in lower
    assert "\\tdim{bangci}" in lower
    assert "occurrence-counting" in lower or "occurrence counting" in lower


def test_assembled_preview_pdf_exists_and_is_non_empty() -> None:
    assert PDF_PATH.exists(), "Assembled grammar review preview PDF must exist"
    assert PDF_PATH.stat().st_size > 0, "Assembled grammar review preview PDF must not be empty"


def test_assembled_preview_tex_uses_real_citation_and_gb4e_machinery() -> None:
    tex = _tex_text()

    assert "[@" not in tex
    assert "\\usepackage[]{natbib}" in tex
    assert "\\setcitestyle{authoryear,round,semicolon}" in tex
    assert "\\bibliographystyle{plainnat}" in tex
    assert "\\bibliography{../../literature/bibliography.bib}" in tex
    assert "\\citep{henderson1965, zamngaihcing2017}" in tex
    assert "\\usepackage{gb4e}" in tex
    assert "\\glossquote" in tex
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
    assert "\\glt \\glossquote{This is the book of the generations of Adam.} (Genesis 5:1)" in block


def test_assembled_preview_tex_uses_shared_analyzer_output_for_known_bible_example() -> None:
    analysis = analyze_text("Hih pen Adam' suanlekhakte' laibu ahi hi.", _tone_dict())
    object_line, gloss_line = build_gll_lines(analysis)
    block = _tex_example_block("ex:dem-hih")

    assert object_line in block
    assert gloss_line in block


def test_assembled_preview_tex_places_bible_reference_after_translation() -> None:
    block = _tex_example_block("ex:dem-hih")

    assert "\\glt \\glossquote{This is the book of the generations of Adam.} (Genesis 5:1)" in block
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
    assert "\\glt \\glossquote{This is the book of the generations of Adam.} (Genesis 5:1)" in _tex_example_block("ex:dem-hih")
    assert "(Matthew 1:21)" in _tex_example_block("ex:dem-tua")
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

    for required in ("Cardinal inventory", "Compound numerals", "ni li", "kum sawm le nih", "sawmvei"):
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
        "Overview of quantification in Tedim",
        "Quantifier inventory",
        "Universal quantification",
        "Existential / partitive-like quantification",
        "Negative quantifiers and negation",
        "Quantity expressions",
        "Boundary with numerals",
        "Boundary with NP structure and negation",
        "Deferred material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_demonstratives_section() -> None:
    text = _text()

    for required in (
        "Demonstratives / deixis",
        "Overview of demonstratives and deixis in this section",
        "Current demonstrative inventory",
        "Core demonstratives: hih and tua",
        "Plural demonstratives",
        "Adnominal and pronominal uses",
        "Discourse and temporal deixis",
        "Manner constructions with bangin",
        "Deferred forms:",
        "Boundary with interrogatives and quantifiers",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_noun_domain_section() -> None:
    text = _text()

    for required in (
        "Overview of the noun domain",
        "Noun-domain inventory",
        "Simple lexical nouns",
        "Human noun mi",
        "Plural marking with -te",
        "Compounds",
        "Proper names and titles",
        "Boundary with NP structure and nominalization",
        "Deferred material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_np_possession_section() -> None:
    text = _text()

    for required in (
        "Overview of noun phrase structure",
        "NP pattern inventory",
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Boundary with numerals and quantifiers",
        "Boundary with pronouns, prefix/agreement, case, and relators",
        "Deferred material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_case_marking_section() -> None:
    text = _text()

    for required in (
        "Overview of case-like marking",
        "Current case-marking inventory",
        "Locative and goal marking with -ah",
        "Agentive, ergative, or instrumental marking with -in",
        "Genitive / possessive boundary",
        "Case marking and relators/postpositions",
        "Case marking and argument structure",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_relators_postpositions_section() -> None:
    text = _text()

    for required in (
        "Relators / postpositions",
        "Overview of relators and postpositions",
        "Current relator / postposition inventory",
        "Spatial relator nouns",
        "Relator plus case-like marking",
        "Postpositional phrase structure",
        "Case-marking boundary",
        "Possession and NP-structure boundary",
        "Deferred and boundary material",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_directionals_section() -> None:
    text = _text()

    for required in (
        "Directionals",
        "Overview of directional expressions",
        "Current directional inventory",
        "Outward and away direction",
        "Upward direction and directionals in the verb phrase",
        "Toward direction with `-sawn`",
        "Downward direction with `-suk`",
        "Deictic boundary",
        "TAM and VP-structure boundary",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_tam_section() -> None:
    text = _text()

    for required in (
        "TAM / aspect / modal",
        "Overview of TAM / aspect / modal marking",
        "Current TAM inventory",
        "Perfect, completive, and change-of-state material",
        "Habitual, continuative, and experiential aspect",
        "Prospective and irrealis marking",
        "Ability and modal marking",
        "Repetition and return marking",
        "Boundary with negation and sentence-final particles",
        "Boundary with directionals and VP structure",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_vp_section() -> None:
    text = _text()

    for required in (
        "VP structure / suffix stacking",
        "Overview of VP structure and suffix stacking",
        "Current VP stacking inventory",
        "Aspect plus irrealis stacking",
        "Directional and TAM boundary in the verbal complex",
        "Ability, irrealis, and negation at the VP boundary",
        "Derivational stacking and valency overlap",
        "Clause-linking boundary with `dingin`",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_derivation_section() -> None:
    text = _text()

    for required in (
        "Derivation / valency",
        "Overview of derivation and valency change",
        "Current derivation / valency inventory",
        "Causative `-sak`",
        "Benefactive and applicative-like `-sak`",
        "The practical split within `-sak`",
        "Boundary with `-pih`",
        "Boundary with `ki-`",
        "Boundary with VP stacking",
        "Boundary with transitivity",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_prefix_agreement_section() -> None:
    text = _text()

    for required in (
        "Prefix / agreement",
        "Overview of prefixal person marking",
        "Prefix inventory and routing",
        "Agreement before verbal hosts",
        "Possession before nominal hosts",
        "Agreement versus possession routing",
        "The a- family and third-person marking",
        "Relation to pronouns",
        "Participant-oriented hong- and kong- boundary",
        "Reflexive and middle ki- boundary",
        "Apostrophe possession and broader possession syntax",
        "Deferred questions",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_pronouns_section() -> None:
    text = _text()

    for required in (
        "Pronouns / clusivity",
        "Overview of Tedim pronouns",
        "Pronoun inventory",
        "Independent personal pronouns",
        "First-person plural forms and clusivity",
        "Second- and third-person forms",
        "Pronouns and possession",
        "Independent pronouns versus prefix/agreement marking",
        "Pronouns with case and relator marking",
        "Emphatic pronouns in -mah",
        "Reflexive and reciprocal ki- boundary",
        "Participant-oriented hong- and kong- boundary",
        "Boundary with demonstratives, interrogatives, quantifiers, and wider agreement",
        "Deferred questions",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_nominalization_section() -> None:
    text = _text()

    for required in (
        "Nominalization",
        "Overview of nominalization in this section",
        "Current nominalization inventory",
        "Deverbal nominalization with `-na`",
        "Nominalization and stem alternation",
        "Agentive or person-head nominalization boundary",
        "Nominalized relatives and clause-derived nominalization boundary",
        "Nominalization plus case boundary",
        "Lexicalized and title-like boundary material",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_clause_linkage_section() -> None:
    text = _text()

    for required in (
        "Clause linkage",
        "Overview of clause linkage in this section",
        "Core temporal subordination: ciangin",
        "Purposive or clause-bound irrealis boundary: dingin",
        "Same-subject converb linkage boundary: VERB-in and ngenin",
        "Different-subject temporal linkage boundary: ahih ciangin",
        "Prenominal relative-clause boundary: a bawl mi",
        "Nominalized relative and clause-like form boundary: omna",
        "Nominalization-plus-case boundary: muhna-ah",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_transitivity_section() -> None:
    text = _text()

    for required in (
        "Transitivity",
        "Overview of transitivity contrasts",
        "Current transitivity inventory",
        "Intransitive predicates",
        "Transitive predicates",
        "The narrow intransitive / transitive contrast",
        "Boundary with stem alternation and labile behavior",
        "Boundary with derivation / valency",
        "Boundary with case marking and argument structure",
        "Boundary with prefix/agreement and voice-like material",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_includes_normalized_stem_alternation_section() -> None:
    text = _text()

    for required in (
        "Stem alternation",
        "Overview of Form I / Form II stem alternation",
        "Current stem alternation overview",
        "Distribution by syntactic context",
        "Core showcase pairs",
        "Promoted caveated pairs",
        "Difficult but grammatically important pairs",
        "One-sided and same-form controls",
        "Blocked or noisy material",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_assembled_preview_tex_includes_normalized_np_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:np-") >= 6
    assert tex.count("\\label{ex:np-") >= 6

    for required in ("hih mite", "mi khat", "mi khempeuh", "mi tampi", "ni li", "na pa' inn-ah", "NP pattern inventory"):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in ("NP pattern inventory", "hih mite", "mi khempeuh", "na pa", "ni li"):
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


def test_assembled_preview_tex_includes_normalized_case_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:case-") >= 4
    assert tex.count("\\label{ex:case-") >= 4

    for required in ("Current case-marking inventory", "Kain in", "khua-ah", "na pa' inn-ah", "lakpan"):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in ("Current case-marking inventory", "kain in", "khua-ah", "lakpan"):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_keeps_case_example_sources_after_translation() -> None:
    assert "(Genesis 4:3)" in _tex_example_block("ex:case-in-kain")
    assert "(Matthew 2:4)" in _tex_example_block("ex:case-in-herod")
    assert "(Genesis 11:28)" in _tex_example_block("ex:case-ah-khua")
    assert "(Matthew 8:8)" in _tex_example_block("ex:case-ah-inn")
    assert "(Genesis 24:23)" in _tex_example_block("ex:case-poss-na-pa-inn")
    assert "(Luke 2:11)" in _tex_example_block("ex:case-relator-david-khuapi-sungah")
    assert "(Matthew 5:19)" in _tex_example_block("ex:case-relator-lakpan")


def test_assembled_preview_case_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 4:3)" in tex or "(Genesis 11:28)" in tex or "(Genesis 24:23)" in tex
    assert "(Matthew 2:4)" in tex or "(Matthew 8:8)" in tex or "(Luke 2:11)" in tex or "(Matthew 5:19)" in tex


def test_assembled_preview_tex_includes_normalized_demonstratives_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:dem-") >= 7
    assert tex.count("\\label{ex:dem-") >= 7

    for required in (
        "Current demonstrative inventory",
        "Core demonstratives: hih and tua",
        "Plural demonstratives",
        "Adnominal and pronominal uses",
        "Discourse and temporal deixis",
        "Manner constructions with bangin",
        "hihte",
        "tuate",
        "tua ciangin",
        "tua ahih ciangin",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current demonstrative inventory",
        "Core demonstratives: hih and tua",
        "Plural demonstratives",
        "Discourse and temporal deixis",
        "Manner constructions with bangin",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_relators_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:rel-") >= 6
    assert tex.count("\\label{ex:rel-") >= 6

    for required in (
        "Current relator / postposition inventory",
        "Spatial relator nouns",
        "Relator plus case-like marking",
        "Postpositional phrase structure",
        "sungah",
        "tungah",
        "kiangah",
        "lakpan",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current relator / postposition inventory",
        "Spatial relator nouns",
        "Relator plus case-like marking",
        "lakpan",
        "from among the women",
        "from the Father",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_directionals_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:dir-") >= 5
    assert tex.count("\\label{ex:dir-") >= 5

    for required in (
        "Current directional inventory",
        "Outward and away direction",
        "Upward direction and directionals in the verb phrase",
        "Toward direction with",
        "Downward direction with",
        "pokhia",
        "nawhkhiat",
        "kilaktoh",
        "piasawn",
        "paisuk",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current directional inventory",
        "Outward and away direction",
        "kilaktoh",
        "piasawn",
        "came down",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_tam_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:tam-") >= 8
    assert tex.count("\\label{ex:tam-") >= 8

    for required in (
        "Current TAM inventory",
        "Perfect, completive, and change-of-state material",
        "Habitual, continuative, and experiential aspect",
        "Prospective and irrealis marking",
        "Ability and modal marking",
        "Repetition and return marking",
        "paingei",
        "gige",
        "ding",
        "thei",
        "kik",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current TAM inventory",
        "Perfect, completive, and change-of-state material",
        "Prospective and irrealis marking",
        "Ability and modal marking",
        "Repetition and return marking",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_vp_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:vp-") >= 6
    assert tex.count("\\label{ex:vp-") >= 6

    for required in (
        "Current VP stacking inventory",
        "Aspect plus irrealis stacking",
        "Directional and TAM boundary in the verbal complex",
        "Ability, irrealis, and negation at the VP boundary",
        "Derivational stacking and valency overlap",
        "bawlzoding",
        "ciahsakkik",
        "paikhiatsak",
        "khiathei ding om lo",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current VP stacking inventory",
        "Aspect plus irrealis stacking",
        "Derivational stacking and valency overlap",
        "ciahsakkik",
        "they will be able to enter",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_derivation_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:deriv-") >= 6
    assert tex.count("\\label{ex:deriv-") >= 6

    for required in (
        "Current derivation / valency inventory",
        "Causative `-sak`",
        "Benefactive and applicative-like `-sak`",
        "The practical split within `-sak`",
        "Boundary with VP stacking",
        "paisak",
        "muhsak",
        "ciahsakkik",
        "piangsak",
    ):
        assert required.lower() in text.lower()

    for required in (
        "Current derivation / valency inventory",
        "Causative",
        "Benefactive and applicative-like",
        "The practical split within",
        "Boundary with VP stacking",
        "paisak",
        "muhsak",
        "ciahsakkik",
        "piangsak",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current derivation / valency inventory",
        "causative",
        "benefactive and applicative-like",
        "paisak",
        "muhsak",
        "ciahsakkik",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_includes_normalized_prefix_agreement_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:pref-") >= 4
    assert tex.count("\\label{ex:pref-") >= 4

    for required in (
        "Prefix inventory and routing",
        "Agreement before verbal hosts",
        "Possession before nominal hosts",
        "Agreement versus possession routing",
        "The a- family and third-person marking",
        "Participant-oriented hong- and kong- boundary",
        "Reflexive and middle ki- boundary",
    ):
        assert required.lower() in text.lower()

    for required in (
        "prefix inventory and routing",
        "agreement before verbal hosts",
        "possession before nominal hosts",
        "agreement versus possession routing",
        "the a- family and third-person marking",
        "participant-oriented hong- and kong- boundary",
        "reflexive and middle ki- boundary",
        "kanei",
        "kainn",
        "hongmu",
        "kongmu",
        "kipan",
        "topa' inn",
    ):
        assert required.lower() in tex_normalized

    for required in (
        "prefix inventory and routing",
        "agreement before verbal hosts",
        "possession before nominal hosts",
        "agreement versus possession routing",
        "participant-oriented hong- and kong- boundary",
        "kanei",
        "kainn",
    ):
        assert required in pdf_normalized


def test_assembled_preview_tex_includes_normalized_pronouns_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    pronoun_example_count = (
        text.count("(@ex:pro-")
        + text.count("(@ex:poss-")
        + text.count("(@ex:emph-")
        + text.count("(@ex:refl-")
        + text.count("(@ex:hong-")
        + text.count("(@ex:kong-")
    )
    assert pronoun_example_count >= 8
    assert tex.count("\\label{ex:pro-") >= 4

    for required in (
        "pronoun inventory",
        "independent personal pronouns",
        "first-person plural forms and clusivity",
        "second- and third-person forms",
        "pronouns and possession",
        "independent pronouns versus prefix/agreement marking",
        "pronouns with case and relator marking",
        "emphatic pronouns in -mah",
        "reflexive and reciprocal ki- boundary",
        "participant-oriented hong- and kong- boundary",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "pronoun inventory",
        "independent personal pronouns",
        "first-person plural forms and clusivity",
        "pronouns and possession",
        "emphatic pronouns in -mah",
    ):
        assert required in pdf_normalized


def test_assembled_preview_tex_includes_normalized_nominalization_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:nmlz-") >= 4
    assert tex.count("\\label{ex:nmlz-") >= 4

    for required in (
        "Current nominalization inventory",
        "Deverbal nominalization with `-na`",
        "Nominalization and stem alternation",
        "Nominalization plus case boundary",
        "Lexicalized and title-like boundary material",
    ):
        assert required.lower() in text.lower()

    for required in (
        "bawlna",
        "bawl-na",
        "muhna-ah",
    ):
        assert required.lower() in text.lower()

    for required in (
        "current nominalization inventory",
        "deverbal nominalization with",
        "nominalization and stem alternation",
        "nominalization plus case boundary",
        "lexicalized and title-like boundary material",
        r"\tdim{-na}",
        "bawlna",
        "bawl-na",
        "muhna-ah",
    ):
        assert required.lower() in tex_normalized

    for required in (
        "current nominalization inventory",
        "deverbal nominalization with",
        "nominalization and stem alternation",
        "nominalization plus case boundary",
        "bawlna",
    ):
        assert required in pdf_normalized


def test_assembled_preview_tex_includes_normalized_clause_linkage_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:clause-") >= 4
    assert tex.count("\\label{ex:clause-") >= 4

    for required in (
       "Core temporal subordination: ciangin",
       "Purposive or clause-bound irrealis boundary: dingin",
       "Same-subject converb linkage boundary",
       "Different-subject temporal linkage boundary",
       "Prenominal relative-clause boundary",
       "ciangin",
       "tua ciangin",
       "dingin",
       "ngenin",
    ):
       assert required.lower() in text.lower()

    for required in (
       "core temporal subordination: ciangin",
       "purposive or clause-bound irrealis",
       "tua ciangin",
       "ngenin",
       "a bawl mi",
    ):
       assert required.lower() in tex_normalized

    for required in (
       "core temporal subordination",
       "temporal subordination",
       "ciangin",
       "tua ciangin",
    ):
       assert required in pdf_normalized


def test_assembled_preview_tex_includes_normalized_stem_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:stem-") >= 6
    assert tex.count("\\label{ex:stem-") >= 6

    for required in (
        "Current stem alternation overview",
        "Distribution by syntactic context",
        "Core showcase pairs",
        "Promoted caveated pairs",
        "mu / muh",
        "ne / nek",
        "nei / neih",
        "ciangin",
        "ni-in",
        "kipan",
        "nadingin",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "current stem alternation overview",
        "distribution by syntactic context",
        "core showcase pairs",
        "promoted caveated pairs",
    ):
        assert required in pdf_normalized


def test_assembled_preview_tex_includes_normalized_transitivity_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:trans-") >= 8
    assert tex.count("\\label{ex:trans-") >= 8

    for required in (
        "Current transitivity inventory",
        "Intransitive predicates",
        "Transitive predicates",
        "The narrow intransitive / transitive contrast",
        "Boundary with stem alternation and labile behavior",
        "sih",
        "suak",
        "hawl",
        "en",
        "mu / muh",
        "piangsak",
    ):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in (
        "Current transitivity inventory",
        "intransitive predicates",
        "transitive predicates",
        "sih",
        "suak",
        "hawl",
        "en",
    ):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_keeps_relators_example_sources_after_translation() -> None:
    assert "(Mark 2:2)" in _tex_example_block("ex:rel-pualam-kongkhak")
    assert "(Genesis 24:11)" in _tex_example_block("ex:rel-pualam-khuapi")
    assert "(Luke 2:11)" in _tex_example_block("ex:rel-sungah-david-khuapi")
    assert "(Genesis 1:2)" in _tex_example_block("ex:rel-tungah-tua-tui")
    assert "(Genesis 2:19)" in _tex_example_block("ex:rel-kiangah-mipa")
    assert "(Matthew 5:19)" in _tex_example_block("ex:rel-lakpan")
    assert "(John 6:45)" in _tex_example_block("ex:rel-kiang-panin-pa")
    assert "(Exodus 2:7)" in _tex_example_block("ex:rel-lak-panin-numeite")


def test_assembled_preview_tex_keeps_directionals_example_sources_after_translation() -> None:
    assert "(Genesis 2:5)" in _tex_example_block("ex:dir-pokhia")
    assert "(Deuteronomy 9:4)" in _tex_example_block("ex:dir-nawhkhiat")
    assert "(Numbers 9:17)" in _tex_example_block("ex:dir-kilaktoh-num9")
    assert "(Luke 9:51)" in _tex_example_block("ex:dir-kilaktoh-luke9")
    assert "(Ezra 9:9)" in _tex_example_block("ex:dir-piasawn")
    assert "(Luke 20:31)" in _tex_example_block("ex:dir-nausawn")
    assert "(Genesis 11:5)" in _tex_example_block("ex:dir-paisuk")


def test_assembled_preview_tex_keeps_tam_example_sources_after_translation() -> None:
    assert "(Exodus 1:12)" in _tex_example_block("ex:tam-kihta-exod1")
    assert "(Matthew 4:4)" in _tex_example_block("ex:tam-nungta-matt4")
    assert "(Exodus 34:27)" in _tex_example_block("ex:tam-bawlzo-exod34")
    assert "(Matthew 7:14)" in _tex_example_block("ex:tam-zuizo-matt7")
    assert "(Luke 4:16)" in _tex_example_block("ex:tam-paingei-luke4")
    assert "(Psalms 33:15)" in _tex_example_block("ex:tam-gige-ps33")
    assert "(Luke 20:20)" in _tex_example_block("ex:tam-gige-luke20")
    assert "(Exodus 33:11)" in _tex_example_block("ex:tam-zel-exod33")
    assert "(Genesis 2:17)" in _tex_example_block("ex:tam-ding-gen2")
    assert "(Matthew 1:23)" in _tex_example_block("ex:tam-ding-matt1")
    assert "(Genesis 41:16)" in _tex_example_block("ex:tam-thei-gen41")
    assert "(Matthew 7:21)" in _tex_example_block("ex:tam-thei-matt7")
    assert "(Genesis 3:19)" in _tex_example_block("ex:tam-kik-gen3")
    assert "(Matthew 2:12)" in _tex_example_block("ex:tam-kik-matt2")


def test_assembled_preview_tex_keeps_vp_example_sources_after_translation() -> None:
    assert "(Deuteronomy 32:30)" in _tex_example_block("ex:vp-taisakzo-ding-deut32")
    assert "(Genesis 20:13)" in _tex_example_block("ex:vp-paikhiatsak-gen20")
    assert "(Luke 9:51)" in _tex_example_block("ex:vp-kilaktoh-ding-luke9")
    assert "(Genesis 41:16)" in _tex_example_block("ex:vp-khiathei-gen41")
    assert "(Matthew 7:21)" in _tex_example_block("ex:vp-lutthei-ding-matt7")
    assert "(Genesis 24:54)" in _tex_example_block("ex:vp-ciahsakkik-gen24")
    assert "(Mark 12:3)" in _tex_example_block("ex:vp-ciahsakkik-mark12")


def test_assembled_preview_tex_keeps_demonstratives_example_sources_after_translation() -> None:
    assert "(Genesis 5:1)" in _tex_example_block("ex:dem-hih")
    assert "(Matthew 1:21)" in _tex_example_block("ex:dem-tua")
    assert "(Genesis 10:20)" in _tex_example_block("ex:dem-hihte")
    assert "(Luke 6:14)" in _tex_example_block("ex:dem-tuate")
    assert "(Exodus 32:9)" in _tex_example_block("ex:dem-adnominal-hih")
    assert "(Matthew 12:49)" in _tex_example_block("ex:dem-pronominal-hihte")
    assert "(Genesis 1:3)" in _tex_example_block("ex:dem-tua-ciangin")
    assert "(Matthew 28:19)" in _tex_example_block("ex:dem-tua-ahih-ciangin")
    assert "(Matthew 6:9)" in _tex_example_block("ex:dem-hih-bangin")
    assert "(Exodus 14:30)" in _tex_example_block("ex:dem-tua-bangin")


def test_assembled_preview_tex_keeps_derivation_example_sources_after_translation() -> None:
    assert "(Exodus 10:7)" in _tex_example_block("ex:deriv-paisak-exod10")
    assert "(Mark 10:14)" in _tex_example_block("ex:deriv-paisak-mark10")
    assert "(Habakkuk 2:2)" in _tex_example_block("ex:deriv-muhsak-hab2")
    assert "(John 9:26)" in _tex_example_block("ex:deriv-muhsak-john9")
    assert "(Genesis 24:54)" in _tex_example_block("ex:deriv-ciahsakkik-gen24")
    assert "(Mark 12:3)" in _tex_example_block("ex:deriv-ciahsakkik-mark12")


def test_assembled_preview_tex_keeps_prefix_agreement_example_sources_after_translation() -> None:
    assert "(Genesis 21:7)" in _tex_example_block("ex:pref-kanei-gen21")
    assert "(John 4:17)" in _tex_example_block("ex:pref-kanei-john4")
    assert "(Genesis 15:3)" in _tex_example_block("ex:pref-kainn-gen15")
    assert "(Luke 7:6)" in _tex_example_block("ex:pref-kainn-luke7")
    assert "(Exodus 30:38)" in _tex_example_block("ex:pref-abawlmi-exod30")
    assert "(Matthew 13:41)" in _tex_example_block("ex:pref-abawlmi-matt13")
    assert "(Jeremiah 7:11)" in _tex_example_block("ex:pref-kongmu-jer7")
    assert "(Matthew 25:37)" in _tex_example_block("ex:pref-hongmu-matt25")


def test_assembled_preview_tex_keeps_pronouns_example_sources_after_translation() -> None:
    assert "(Genesis 3:20)" in _tex_example_block("ex:pro-amah")
    assert "(Matthew 5:13)" in _tex_example_block("ex:pro-note")
    assert "(Genesis 13:8)" in _tex_example_block("ex:pro-eite")
    assert "(Genesis 34:9)" in _tex_example_block("ex:pro-kote")
    assert "(Genesis 24:23)" in _tex_example_block("ex:poss-na")
    assert "(Luke 2:49)" in _tex_example_block("ex:poss-ka-pa-inn")
    assert "(Genesis 3:20)" in _tex_example_block("ex:poss-a")
    assert "(Genesis 4:13)" in _tex_example_block("ex:emph-keimah")
    assert "(Matthew 8:22)" in _tex_example_block("ex:emph-nangmah")
    assert "(Genesis 2:24)" in _tex_example_block("ex:refl-ki")
    assert "(Matthew 19:5)" in _tex_example_block("ex:refl-ki-matt19")
    assert "(Matthew 25:37)" in _tex_example_block("ex:hong-prefix")
    assert "(Genesis 41:41)" in _tex_example_block("ex:kong-prefix")


def test_assembled_preview_tex_keeps_nominalization_example_sources_after_translation() -> None:
    assert "(Genesis 2:17)" in _tex_example_block("ex:nmlz-theihna-gen2")
    assert "(Matthew 1:1)" in _tex_example_block("ex:nmlz-ciaptehna-matt1")
    assert "(Genesis 2:9)" in _tex_example_block("ex:nmlz-stem-theihna-gen2")
    assert "(Matthew 7:5)" in _tex_example_block("ex:nmlz-stem-theihna-matt7")
    assert "(Genesis 6:11)" in _tex_example_block("ex:nmlz-muhna-ah-gen6")
    assert "(Luke 19:27)" in _tex_example_block("ex:nmlz-muhna-ah-luke19")


def test_assembled_preview_tex_keeps_clause_linkage_example_sources_after_translation() -> None:
    assert "(Genesis 1:3)" in _tex_example_block("ex:clause-ciangin-gen1p3")
    assert "(Genesis 1:14)" in _tex_example_block("ex:clause-dingin-gen1p14")
    assert "(Genesis 41:55)" in _tex_example_block("ex:clause-ngenin-gen41p55")
    assert "(Genesis 1:21)" in _tex_example_block("ex:clause-ahih-ciangin-gen1p21")
    assert "(Genesis 6:11)" in _tex_example_block("ex:clause-muhnaah-gen6p11")
    assert "(Luke 19:27)" in _tex_example_block("ex:clause-muhnaah-luke19p27")


def test_assembled_preview_tex_keeps_stem_example_sources_after_translation() -> None:
    assert "(Genesis 1:4)" in _tex_example_block("ex:stem-mu-gen1")
    assert "(Genesis 19:1)" in _tex_example_block("ex:stem-muh-gen19")
    assert "(Genesis 2:17)" in _tex_example_block("ex:stem-ne-gen2")
    assert "(Genesis 2:17)" in _tex_example_block("ex:stem-nek-gen2")
    assert "(Genesis 11:30)" in _tex_example_block("ex:stem-nei-gen11")
    assert "(2 Samuel 23:8)" in _tex_example_block("ex:stem-neih-2sam23")
    assert "(Psalms 43:3)" in _tex_example_block("ex:stem-sawlkhia-ps43")
    assert "(Luke 22:35)" in _tex_example_block("ex:stem-sawlkhiat-luke22")


def test_assembled_preview_tex_keeps_transitivity_example_sources_after_translation() -> None:
    assert "(Genesis 11:28)" in _tex_example_block("ex:trans-sih-gen11")
    assert "(Matthew 22:27)" in _tex_example_block("ex:trans-sih-matt22")
    assert "(Genesis 26:13)" in _tex_example_block("ex:trans-suak-gen26")
    assert "(Matthew 12:25)" in _tex_example_block("ex:trans-suak-matt12")
    assert "(1 Chronicles 13:7)" in _tex_example_block("ex:trans-hawl-1chr13")
    assert "(Genesis 1:31)" in _tex_example_block("ex:trans-en-gen1")
    assert "(Matthew 27:36)" in _tex_example_block("ex:trans-en-matt27")
    assert "(Genesis 6:8)" in _tex_example_block("ex:trans-mu-gen6")
    assert "(Matthew 2:10)" in _tex_example_block("ex:trans-muh-matt2")


def test_assembled_preview_stem_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 1:4)" in tex or "(Genesis 2:17)" in tex or "(Psalms 43:3)" in tex
    assert "(Luke 22:35)" in tex or "No equally clean Gospel example is currently used" in text


def test_assembled_preview_demonstratives_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 5:1)" in tex or "(Genesis 10:20)" in tex or "(Genesis 1:3)" in tex or "(Exodus 14:30)" in tex
    assert "(Matthew 1:21)" in tex or "(Luke 6:14)" in tex or "(Matthew 12:49)" in tex or "(Matthew 28:19)" in tex or "(Matthew 6:9)" in tex or "No equally clean Gospel example is currently used" in text


def test_assembled_preview_relators_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 24:11)" in tex or "(Genesis 1:2)" in tex or "(Genesis 2:19)" in tex or "(Exodus 2:7)" in tex
    assert "(Mark 2:2)" in tex or "(Luke 2:11)" in tex or "(Matthew 5:19)" in tex or "(John 6:45)" in tex or "no equally clean Gospel" in text


def test_assembled_preview_directionals_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 2:5)" in tex or "(Deuteronomy 9:4)" in tex or "(Numbers 9:17)" in tex or "(Ezra 9:9)" in tex
    assert "(Luke 9:51)" in tex or "(Luke 20:31)" in tex


def test_assembled_preview_tam_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()

    assert "(Genesis 2:17)" in tex or "(Genesis 3:19)" in tex or "(Exodus 1:12)" in tex or "(Exodus 34:27)" in tex
    assert "(Matthew 1:23)" in tex or "(Matthew 2:12)" in tex or "(Matthew 4:4)" in tex or "(Matthew 7:14)" in tex or "(Matthew 7:21)" in tex or "(Luke 4:16)" in tex or "(Luke 20:20)" in tex


def test_assembled_preview_vp_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Deuteronomy 32:30)" in tex or "(Genesis 20:13)" in tex or "(Genesis 41:16)" in tex or "(Genesis 24:54)" in tex
    assert "(Luke 9:51)" in tex or "(Matthew 7:21)" in tex or "(Mark 12:3)" in tex or "No equally clean Gospel example is currently used for this exact construction" in text


def test_assembled_preview_derivation_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Exodus 10:7)" in tex or "(Habakkuk 2:2)" in tex or "(Genesis 24:54)" in tex
    assert "(Mark 10:14)" in tex or "(John 9:26)" in tex or "(Mark 12:3)" in tex or "No equally clean Gospel example is currently used for this exact construction" in text


def test_assembled_preview_prefix_agreement_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 21:7)" in tex or "(Genesis 15:3)" in tex or "(Exodus 30:38)" in tex or "(Jeremiah 7:11)" in tex
    assert "(John 4:17)" in tex or "(Luke 7:6)" in tex or "(Matthew 13:41)" in tex or "(Matthew 25:37)" in tex or "No equally clean Gospel example is currently used" in text


def test_assembled_preview_pronouns_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 3:20)" in tex or "(Genesis 13:8)" in tex or "(Genesis 34:9)" in tex or "(Genesis 24:23)" in tex
    assert "(Matthew 5:13)" in tex or "(Luke 2:49)" in tex or "(Matthew 8:22)" in tex or "(Matthew 19:5)" in tex or "(Matthew 25:37)" in tex or "No equally clean Gospel example is currently used for this construction" in text


def test_assembled_preview_nominalization_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 2:17)" in tex or "(Genesis 2:9)" in tex or "(Genesis 6:11)" in tex or "(Judges 7:14)" in tex
    assert "(Matthew 1:1)" in tex or "(Matthew 7:5)" in tex or "(Luke 19:27)" in tex or "(John 6:37)" in tex or "No equally clean Gospel example is currently used" in text


def test_assembled_preview_clause_linkage_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 1:3)" in tex or "(Genesis 1:21)" in tex or "(Genesis 1:26)" in tex or "(Genesis 1:14)" in tex or "(Genesis 41:55)" in tex or "(Genesis 6:11)" in tex
    assert "(Matthew 7:5)" in tex or "(Luke 19:27)" in tex or "No equally" in text


def test_assembled_preview_transitivity_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 11:28)" in tex or "(Genesis 26:13)" in tex or "(Genesis 1:31)" in tex or "(Genesis 6:8)" in tex or "(1 Chronicles 13:7)" in tex
    assert "(Matthew 22:27)" in tex or "(Matthew 12:25)" in tex or "(Matthew 27:36)" in tex or "(Matthew 2:10)" in tex or "No equally clean Gospel example is currently used for this exact `hawl` row" in text


def test_assembled_preview_tex_includes_normalized_noun_inventory_and_examples() -> None:
    text = _text()
    tex = _tex_text()
    pdf = _pdf_text()
    tex_normalized = _normalize(tex.lower())
    pdf_normalized = _normalize(pdf.lower())

    assert text.count("(@ex:noun-") >= 6
    assert tex.count("\\label{ex:noun-") >= 6

    for required in ("Noun-domain inventory", "gam", "aksi-te", "hih mite", "mi khempeuh", "minam", "thugen", "Abraham' suan"):
        assert required.lower() in text.lower()
        assert required.lower() in tex_normalized

    for required in ("Noun-domain inventory", "gam", "aksi-te", "hih mite", "mi khempeuh"):
        assert required.lower() in pdf_normalized


def test_assembled_preview_tex_keeps_noun_example_sources_after_translation() -> None:
    assert "(Genesis 2:5)" in _tex_example_block("ex:noun-gam")
    assert "(Matthew 2:2)" in _tex_example_block("ex:noun-aksi")
    assert "(Genesis 1:16)" in _tex_example_block("ex:noun-aksi-te")
    assert "(Exodus 5:5)" in _tex_example_block("ex:noun-hih-mite")
    assert "(Luke 2:1)" in _tex_example_block("ex:noun-mi-khempeuh")
    assert "(Genesis 11:6)" in _tex_example_block("ex:noun-minam-khat")
    assert "(Genesis 4:23)" in _tex_example_block("ex:noun-thugen")
    assert "(Matthew 1:1)" in _tex_example_block("ex:noun-abraham-suan-david")


def test_assembled_preview_noun_examples_include_old_testament_and_gospel_sources() -> None:
    tex = _tex_text()
    text = _text()

    assert "(Genesis 2:5)" in tex or "(Genesis 1:16)" in tex or "(Exodus 5:5)" in tex or "(Genesis 11:6)" in tex or "(Genesis 4:23)" in tex
    assert "(Matthew 2:2)" in tex or "(Luke 2:1)" in tex or "(Matthew 1:1)" in tex


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
    assert "(Luke 2:49)" in _tex_example_block("ex:poss-ka-pa-inn")
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
    assert "load_normalization_supplements" in script_text
    assert "resolve_example_source_metadata" in script_text


def test_assembled_preview_tex_distinguishes_inline_tedim_from_technical_paths() -> None:
    tex = _tex_text()

    assert "\\texttt{output/publication\\_review/grammar\\_transitivity\\_print\\_slice.md}" not in tex
    assert "\\texttt{python3\\ scripts/assemble\\_publication\\_review\\_preview.py}" not in tex
    assert "\\tdim{hih}" in tex
    assert "\\tdim{tua}" in tex
    assert "\\tdim{mahmah}" in tex
    assert "\\tdim{ciangin}" in tex
    assert "\\tdim{gam}" in tex


def test_assembled_preview_tex_glosses_multiword_running_prose_forms_in_normalized_sections() -> None:
    tex = _normalize(_tex_text())

    for required in (
        r"\tdim{mi khat} \glossquote{one person / a person}",
        r"\tdim{mi khempeuh} \glossquote{all people}",
        r"\tdim{mi pawlkhat} \glossquote{some people}",
        r"\tdim{mi tampi} \glossquote{many people}",
        r"\tdim{ni li} \glossquote{four days}",
        r"\tdim{khua-ah} \glossquote{in the town}",
        r"\tdim{Kain in} \glossquote{Cain as agent}",
        r"\tdim{lakpan} \glossquote{from among}",
        r"\tdim{sung} \glossquote{inside}",
        r"\tdim{kiang} \glossquote{beside / near}",
        r"\tdim{pualam} \glossquote{outside}",
        r"\tdim{sungah} \glossquote{inside / in}",
        r"\tdim{Abraham' suan} in Matthew 1:1",
        r"\glossquote{David, descendant of Abraham} (Matthew 1:1)",
        r"\tdim{-na} \glossquote{nominalizer}",
        r"\tdim{bawlna} \glossquote{making / creation}",
        r"\tdim{hong pai mi} \glossquote{one who came}",
        r"\tdim{muhna-ah} \glossquote{in seeing / in the sight of}",
        r"\tdim{kumpipa} \glossquote{king}",
        r"\tdim{Topa} \glossquote{Lord}",
    ):
        assert required in tex
    assert r"\tdim{kum sawm le nih} \glossquote{twelve years}" in tex


def test_assembled_preview_tex_keeps_grammar_facing_explanations_for_ot_led_subsections() -> None:
    text = _text()

    assert "No equally clean Gospel possession row was found" in text
    assert "No equally clean Gospel source or accompaniment row is currently used here" in text
    assert "No equally clean Gospel example is currently used for this construction." in text


def test_assembled_preview_gap_and_review_status_text_are_not_aggressively_italicized() -> None:
    tex = _tex_text()
    normalized = _normalize(tex)

    assert (
        "The current phonology and tone section is deliberately cautious: the literature supports a modest "
        "segmental summary, practical spelling is only indirect evidence, and the tone-sensitive \\tdim{-a} "
        "distinction remains blocked."
    ) in normalized
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
    assert "abbreviations" in lower
    assert "references" in lower
    assert re.search(r"\(Henderson,\s*1965.{0,20}Cing,\s*2017\)", normalized)
    assert "(1.1)" in pdf_text
    assert re.search(r"\(3\.\d+\)", pdf_text)
    assert re.search(r"\(4\.\d+\)", pdf_text)
    assert "Genesis 5:1" in pdf_text
    assert "book of the generations of Adam." in pdf_text
    assert "Full reduplication as intensification" in pdf_text


def test_assembled_preview_pdf_text_keeps_source_references_systematically() -> None:
    pdf_text = _pdf_text()

    assert "book of the generations of Adam" in pdf_text
    assert "(Genesis 5:1)" in pdf_text
    assert "(Matthew 1:21)" in pdf_text
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
