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


def test_assembled_preview_gap_sections_use_grammar_facing_prose() -> None:
    text = _text()

    for required in (
        "A full discussion of phonology and tone is not yet included in this review preview.",
        "A full discussion of verbal paradigms is not yet included in this draft.",
        "A fuller treatment of discourse structure is not yet included in this draft.",
        "Several cross-cutting morphological issues remain unresolved and are not yet integrated into this draft.",
    ):
        assert required in text


def test_assembled_preview_does_not_claim_finished_grammar_or_pdf() -> None:
    text = _text()
    lower = text.lower()

    assert "review preview, not a finished grammar" in lower
    assert "not a final publication pdf" not in lower


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
        "Overview of the numeral system",
        "Cardinal numerals",
        "Decimal composition",
        "Counting phrases and word order",
        "Classifier-like and counting expressions",
        "Distributive numerals",
        "Ambiguity controls",
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
    assert "\\tdim{sih} is the clean intransitive anchor for the first slice." in lower
    assert "\\tdim{hawl} is the clean transitive anchor for the first slice." in lower
    assert "\\tdim{mahmah} is the main full-reduplication intensifier anchor." in lower
    assert "\\tdim{ciangin}" in lower
    assert "overview of noun phrase structure" in normalized
    assert "\\tdim{kanei}" in lower
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
        "Overview of noun phrase structure",
        "Current NP pattern inventory",
        "Demonstratives and nouns",
        "Numerals and nouns",
        "Quantifiers and nouns",
        "Possession",
        "Deferred and boundary material",
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


def test_assembled_preview_tex_keeps_derivation_example_sources_after_translation() -> None:
    assert "(Exodus 10:7)" in _tex_example_block("ex:deriv-paisak-exod10")
    assert "(Mark 10:14)" in _tex_example_block("ex:deriv-paisak-mark10")
    assert "(Habakkuk 2:2)" in _tex_example_block("ex:deriv-muhsak-hab2")
    assert "(John 9:26)" in _tex_example_block("ex:deriv-muhsak-john9")
    assert "(Genesis 24:54)" in _tex_example_block("ex:deriv-ciahsakkik-gen24")
    assert "(Mark 12:3)" in _tex_example_block("ex:deriv-ciahsakkik-mark12")


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
        r"\tdim{Abraham' suan David} \glossquote{David, descendant of Abraham}",
    ):
        assert required in tex
    assert r"\tdim{kum sawm le nih} \glossquote{twelve years}" in tex


def test_assembled_preview_tex_keeps_grammar_facing_explanations_for_ot_led_subsections() -> None:
    text = _text()

    for required in (
        "No equally good Gospel ordinal example is currently used here",
        "No equally clean Gospel possession row was found",
        "No equally clean Gospel source or accompaniment row is currently used here",
        "No equally clean Gospel classifier-like example is currently used here",
    ):
        assert required in text


def test_assembled_preview_gap_and_review_status_text_are_not_aggressively_italicized() -> None:
    tex = _tex_text()
    normalized = _normalize(tex)

    assert "A full discussion of phonology and tone is not yet included in this review preview." in normalized
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
    assert "(2.1)" in pdf_text
    assert re.search(r"\(3\.\d+\)", pdf_text)
    assert re.search(r"\(4\.\d+\)", pdf_text)
    assert "Genesis 5:1" in pdf_text
    assert "book of the generations of Adam." in pdf_text
    assert "Full reduplication as intensification" in pdf_text


def test_assembled_preview_pdf_text_keeps_source_references_systematically() -> None:
    pdf_text = _pdf_text()

    assert "book of the generations of Adam" in pdf_text
    assert "(Genesis 5:1)" in pdf_text
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
