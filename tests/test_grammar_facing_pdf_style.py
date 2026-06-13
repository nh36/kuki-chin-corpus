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

import assemble_publication_review_preview as assembler
import grammar_pdf_quality_gate as gate

from restore_tone import load_tone_dictionary


PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
TEX_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.tex"
PDF_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.pdf"
QUALITY_REPORT_PATH = ROOT / "output/publication_review/grammar_facing_quality_report.md"
BIBLE_PATH = ROOT / "bibles" / "extracted" / "ctd" / "ctd-x-bible.txt"


def _text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _tex_text() -> str:
    return TEX_PATH.read_text(encoding="utf-8")


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


@lru_cache(maxsize=1)
def _quality_result() -> tuple[list[str], dict[str, object]]:
    return gate.gather_quality_issues(TEX_PATH)


@lru_cache(maxsize=1)
def _section_blocks() -> dict[str, gate.MarkdownBlock]:
    return {
        block.title: block
        for block in gate.split_markdown_blocks(_text())
        if block.level == 2 and block.title in gate.TARGET_SECTION_TITLES
    }


@lru_cache(maxsize=1)
def _tone_dict() -> dict[str, list[dict[str, str]]]:
    return load_tone_dictionary()


def _section_text(title: str) -> str:
    lines = _text().splitlines()
    blocks = gate.split_markdown_blocks(_text())
    for index, block in enumerate(blocks):
        if block.level == 2 and block.title == title:
            end_line = len(lines)
            for later in blocks[index + 1 :]:
                if later.level <= 2:
                    end_line = later.start_line - 1
                    break
            return "\n".join(lines[block.start_line - 1 : end_line])
    raise AssertionError(f"Missing section: {title}")


def test_grammar_facing_quality_gate_passes_cleanly() -> None:
    issues, summary = _quality_result()
    report = QUALITY_REPORT_PATH.read_text(encoding="utf-8")

    assert issues == []
    assert summary["issues"] == 0
    assert "- All configured grammar-facing quality gates passed." in report
    assert f"- Pages: {summary['pages']}" in report


def test_grammar_facing_target_sections_are_not_blank_in_markdown_or_tex() -> None:
    markdown_blocks = gate.split_markdown_blocks(_text())
    tex_blocks = gate.split_tex_blocks(_tex_text())

    for block in markdown_blocks:
        if block.level in {2, 3} and (
            block.title in gate.TARGET_SECTION_TITLES
            or (block.parent_titles and block.parent_titles[-1] in gate.TARGET_SECTION_TITLES)
        ):
            assert gate.markdown_block_has_substance(
                block
            ), f"Blank Markdown section: {' > '.join((*block.parent_titles, block.title))}"

    for block in tex_blocks:
        if block.level in {2, 3} and block.title != "References" and (
            block.title in gate.TARGET_SECTION_TITLES
            or (block.parent_titles and block.parent_titles[-1] in gate.TARGET_SECTION_TITLES)
        ):
            assert gate.tex_block_has_substance(
                block
            ), f"Blank TeX section: {' > '.join((*block.parent_titles, block.title))}"


def test_grammar_facing_body_suppresses_internal_workflow_terms() -> None:
    body_tex = gate.tex_body(_tex_text()).replace(r"\_", "_")
    body_pdf = gate.pdf_body(_pdf_text())

    for pattern, description in gate.TEX_INTERNAL_PATTERNS:
        assert not pattern.search(body_tex), f"Internal prose in TeX body ({description})"
    for pattern, description in gate.PDF_INTERNAL_PATTERNS:
        assert not pattern.search(body_pdf), f"Internal prose in PDF body ({description})"


def test_grammar_facing_examples_keep_sources_after_glt() -> None:
    bible = assembler.load_bible(BIBLE_PATH)
    tex_examples = gate.parse_tex_examples(_tex_text())

    missing = []
    for example in gate.collect_example_records(_text(), bible):
        if example.label == "review-preview-warning":
            continue
        glt_line = tex_examples.get(example.label, "")
        if example.source and f"({example.source})" not in glt_line:
            missing.append(f"{example.label}: {example.source}")

    assert not missing, f"Missing source references after translation: {missing}"


def test_grammar_facing_contextual_source_is_attached_before_tex_generation() -> None:
    markdown = """
## Numerals

In Ezra 2:23, the numeral appears in a simple counting clause.

(@ex:quality-gate-ezra)
a. Tedim: Anathoth mite, zakhat sawmnih-le-giat.
b. Segmentation: Anathoth mite za-khat sawm-nih le giat
c. Gloss: Anathoth people hundred-one ten-two and eight
d. Translation: The people of Anathoth were one hundred twenty-eight.
""".strip()

    bible = assembler.load_bible(BIBLE_PATH)
    enriched = assembler.enrich_example_headers(markdown, bible)
    example = assembler.parse_examples(enriched)[0]
    latex = assembler.example_to_latex_block(example, bible, _tone_dict())

    assert "(@ex:quality-gate-ezra) Ezra 2:23" in enriched
    assert assembler.resolve_example_source(example, bible) == "Ezra 2:23"
    assert r"\glt \glossquote{The people of Anathoth were one hundred twenty-eight.} (Ezra 2:23)" in latex


@pytest.mark.parametrize(
    ("lead_in", "expected_source"),
    [
        ("In Ezra 2:23, the numeral appears in a simple counting clause.", "Ezra 2:23"),
        ("Ezra 2:23 gives a compact counting phrase.", "Ezra 2:23"),
        ("Genesis 5:1 supplies the proximal demonstrative anchor.", "Genesis 5:1"),
        ("Matthew 2:4 shows the agentive-marked NP clearly.", "Matthew 2:4"),
        ("Luke 2:1 gives a clean noun-plus-quantifier phrase.", "Luke 2:1"),
        ("John 11:39 gives a counted noun phrase.", "John 11:39"),
        ("Mark 6:34 supplies the quantity phrase.", "Mark 6:34"),
    ],
)
def test_grammar_facing_contextual_source_patterns_are_attached_before_tex_generation(
    lead_in: str, expected_source: str
) -> None:
    markdown = f"""
## Numerals

{lead_in}

(@ex:quality-gate-context)
a. Tedim: Anathoth mite, zakhat sawmnih-le-giat.
b. Segmentation: Anathoth mite za-khat sawm-nih le giat
c. Gloss: Anathoth people hundred-one ten-two and eight
d. Translation: The people of Anathoth were one hundred twenty-eight.
""".strip()

    bible = assembler.load_bible(BIBLE_PATH)
    enriched = assembler.enrich_example_headers(markdown, bible)

    assert f"(@ex:quality-gate-context) {expected_source}" in enriched


def test_grammar_facing_tsv_source_is_attached_before_tex_generation() -> None:
    markdown = """
## Quantifiers

The noun-plus-quantifier boundary is illustrated again here.

(@ex:quality-gate-tsv)
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: a man / one person
""".strip()

    bible = assembler.load_bible(BIBLE_PATH)
    enriched = assembler.enrich_example_headers(markdown, bible)
    example = assembler.parse_examples(enriched)[0]
    latex = assembler.example_to_latex_block(example, bible, _tone_dict())

    assert "(@ex:quality-gate-tsv) Genesis 32:24" in enriched
    assert r"\glt \glossquote{a man / one person} (Genesis 32:24)" in latex


def test_grammar_facing_conflicting_example_sources_fail_loudly() -> None:
    markdown = """
## Quantifiers

(@ex:quality-gate-conflict) Genesis 1:1
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: a man / one person
""".strip()

    bible = assembler.load_bible(BIBLE_PATH)

    with pytest.raises(RuntimeError, match=r"Conflicting example sources for ex:quality-gate-conflict: .*Genesis 1:1.*Genesis 32:24"):
        assembler.enrich_example_headers(markdown, bible)


def test_grammar_facing_key_tedim_forms_are_glossed_on_first_prose_mention() -> None:
    expectations = {
        "Stem alternation": (
            "mu / muh",
            "ne / nek",
            "nei / neih",
            "za / zak",
            "pia / piak",
            "nusia / nusiat",
            "bia / biak",
            "thei / theih",
            "piang / pian",
            "zui / zuih",
            "khial / khialh",
            "kia / kiak",
            "sawlkhia / sawlkhiat",
            "ngai / ngaih",
            "pua / puak",
            "pai / paih",
            "tua / tuah",
            "tua / tuak",
            "mi",
        ),
        "Numerals": ("khat", "nih", "sawm", "kua"),
        "Quantifiers": ("khempeuh", "pawlkhat", "kuamah", "bangmah", "tampi"),
        "NP structure / possession": ("hih", "mi", "mi khat", "ni li", "kum sawm le nih"),
        "Noun domain": ("gam", "aksi", "aksi-te", "mi khempeuh", "Abraham' suan David"),
        "Case marking": ("-ah", "-in", "-pan", "-panin", "-tawh", "khua-ah", "Kain in", "lakpan"),
        "Relators / postpositions": ("sung", "tung", "kiang", "lak", "pualam", "sungah", "tungah", "kiangah", "lakpan"),
        "Transitivity": (
            "sih",
            "suak",
            "hawl",
            "en",
            "mu / muh",
            "za / zak",
            "nei / neih",
            "ngai / ngaih",
            "piangsak",
            "pia",
            "gen",
            "tom",
            "hong",
            "ki-",
            "pia(k)sak",
        ),
        "Derivation / valency": (
            "-sak",
            "paisak",
            "muhsak",
            "-pih",
            "paipih",
            "mipihte",
            "ki-",
            "kisep",
            "kigen",
            "ciahsakkik",
            "bawlsakthei",
            "paikhiatsak",
            "piangsak",
        ),
        "VP structure / suffix stacking": (
            "bawlzoding",
            "khia-ta",
            "khiathei ding om lo",
            "ciahsakkik",
            "paikhiatsak",
            "bawlsakthei",
            "dingin",
        ),
        "TAM / aspect / modal": (
            "-ta",
            "-zo",
            "-gige",
            "-zel",
            "-ding",
            "-thei",
            "-kik",
            "-ngei",
            "dingin",
            "pailai",
            "khia-ta",
            "bawlzoding",
            "bawlsakthei",
        ),
        "Directionals": (
            "-khia",
            "-khiat",
            "-toh",
            "-sawn",
            "-suk",
            "-lam",
            "pokhia",
            "nawhkhiat",
            "kilaktoh",
            "piasawn",
            "paisuk",
            "hotkhiatna",
            "kahtohna",
            "paitoh",
            "tawplam",
        ),
        "Demonstratives / deixis": (
            "hih",
            "tua",
            "hihte",
            "tuate",
            "hih bangin",
            "tua bangin",
            "tua ciangin",
            "tua ahih ciangin",
            "hih ciangin",
            "huā",
            "kua",
            "kuamah",
            "bangmah",
        ),
        "Negation": (
            "lo hi",
            "loh",
            "loh ding-a",
            "kei in",
            "kei un",
            "maizum lo uh hi",
            "om lo hi",
            "nei lo hi",
            "nawn lo",
            "thei lo",
            "theih loh",
            "kuamah",
            "bangmah",
        ),
        "Interrogatives": (
            "hiam",
            "bang",
            "kua",
            "bangci",
            "banghangin",
            "bang hiam cih",
            "Bang hang hiam cih leh",
            "langnih a hiam namsau",
            "a hiam ciat uh",
            "bangmah",
            "bangin",
            "maw",
            "ham",
            "em",
        ),
        "Sentence-final particles": (
            "ahi hi",
            "lo hi",
            "hen",
            "in",
            "un",
            "hiam",
            "aw",
            "tahen",
            "Khuavak om hen",
            "teembaw khat bawl in",
            "gingsak un",
            "Gam khempeuh aw",
        ),
        "Coordinators": (
            "le",
            "vantung le leitung",
            "leh",
            "a piangsak",
            "mawh",
            "Ahih hangin",
            "ahih kei leh",
        ),
        "Reduplication": (
            "mahmah",
            "taktak",
            "peuhpeuh",
            "pha mahmah hi",
        ),
        "Prefix / agreement": (
            "kanei",
            "ka-nei",
            "kainn",
            "ka-inn",
            "ka-",
            "ainn",
            "ipai",
            "hongmu",
            "kongmu",
            "kipan",
            "a bawl mi",
        ),
        "Hong / kong object-prefix or inverse-like": (
            "hong",
            "kong",
            "hongbia",
            "kongpia",
            "kongkoih",
            "hongmu",
            "kongmu",
        ),
        "Pronouns / clusivity": (
            "kei",
            "nang",
            "amah",
            "eite",
            "kote",
            "note",
            "amaute",
            "na-",
            "i-",
            "keimah",
            "nangmah",
            "ki-",
            "ki-gawm",
            "kuamah",
            "bangmah",
        ),
        "Nominalization": (
            "bawlna",
            "bawl-na",
            "-pa",
            "-mi",
            "hong pai mi",
            "omna",
            "muhna-ah",
            "kumpipa",
            "Topa",
            "a bawl mi",
        ),
        "Clause linkage": (
            "ciangin",
            "tua ciangin",
            "ciang-in",
            "dingin",
            "ding-in",
            "ngenin",
            "VERB-in",
            "ahih ciangin",
            "a bawl mi",
            "omna",
            "muhna-ah",
            "leh",
            "hangin",
            "bangin",
        ),
        "Same-subject and different-subject clause linkage": (
            "bawlin",
            "semin",
            "VERB-in",
            "ahih ciangin",
            "ciangin",
            "dingin",
            "ngenin",
            "a bawl mi",
            "omna",
            "muhna-ah",
        ),
    }

    for section_title, forms in expectations.items():
        block = _section_blocks()[section_title]
        for form in forms:
            assert gate.first_prose_occurrence_has_gloss(
                block.content, form, gate.GLOSSARY_REQUIREMENTS[form][0]
            ), f"{section_title} does not gloss the first prose mention of {form!r}"


def test_grammar_facing_tex_gloss_lint_rejects_unglossed_running_prose_forms() -> None:
    bad_block = gate.TexBlock(
        level=3,
        title="Quantifiers and noun phrase structure",
        parent_titles=("Quantifiers",),
        content=r"\tdim{mi khat} remains a boundary row in the discussion.",
        start_line=100,
    )
    good_block = gate.TexBlock(
        level=3,
        title="Quantifiers and noun phrase structure",
        parent_titles=("Quantifiers",),
        content=r"\tdim{mi khat} \glossquote{one person / a person} remains a boundary row in the discussion.",
        start_line=100,
    )

    assert gate.find_first_missing_tex_gloss(
        "Quantifiers",
        [bad_block],
        "mi khat",
        gate.GLOSSARY_REQUIREMENTS["mi khat"][0],
        gate.GLOSSARY_REQUIREMENTS["mi khat"][1],
    )
    assert (
        gate.find_first_missing_tex_gloss(
            "Quantifiers",
            [good_block],
            "mi khat",
            gate.GLOSSARY_REQUIREMENTS["mi khat"][0],
            gate.GLOSSARY_REQUIREMENTS["mi khat"][1],
        )
        is None
    )


def test_grammar_facing_quote_handling_is_clean_and_tedim_apostrophes_survive() -> None:
    tex = _tex_text()
    body_tex = gate.tex_body(tex)
    quote_check_text = re.sub(r"\\tdimword\{[^}]*\}|\\tdim\{[^}]*\}|\\glossquote\{[^}]*\}", "", body_tex)
    quote_check_text = re.sub(r"``[^']+''", "", quote_check_text)

    assert r"\newcommand{\glossquote}[1]{`#1'}" in tex
    assert not any(character in body_tex for character in "‘’“”")
    assert not re.search(r"(?<![A-Za-z])'[^'\n{}\\]+'(?![A-Za-z])", quote_check_text)
    for preserved in ("pa' inn", "Abraham' suan", "Topa' inn", "na pa' inn-ah"):
        assert preserved in tex


def test_grammar_facing_one_example_subsections_have_visible_explanations() -> None:
    offenders = []
    for block in gate.split_markdown_blocks(_text()):
        if block.level != 3 or not block.parent_titles:
            continue
        if block.parent_titles[-1] not in gate.TARGET_SECTION_TITLES:
            continue
        if gate.SUBSECTION_IGNORE_RE.search(block.title):
            continue
        if gate.subsection_example_count(block) == 1 and not gate.ONE_EXAMPLE_NOTE_RE.search(block.content):
            offenders.append(f"{block.parent_titles[-1]} > {block.title}")

    assert not offenders, f"One-example subsections need an explicit grammar-facing note: {offenders}"


def test_grammar_facing_ot_only_subsections_have_visible_explanations() -> None:
    offenders = []
    bible = assembler.load_bible(BIBLE_PATH)
    examples = gate.collect_example_records(_text(), bible)
    for block in gate.split_markdown_blocks(_text()):
        if block.level != 3 or not block.parent_titles or block.parent_titles[-1] not in gate.TARGET_SECTION_TITLES:
            continue
        subsection_examples = [
            example
            for example in examples
            if len(example.heading_path) >= 2
            and example.heading_path[-1] == block.title
            and example.heading_path[-2] == block.parent_titles[-1]
            and example.source
        ]
        zones = {gate.source_zone(example.source) for example in subsection_examples}
        if subsection_examples and "Gospel" not in zones:
            if not gate.ONE_EXAMPLE_NOTE_RE.search(block.content):
                offenders.append(f"{block.parent_titles[-1]} > {block.title}")

    assert not offenders, f"OT-only subsections need an explicit explanation: {offenders}"


def test_grammar_facing_sections_keep_old_testament_and_gospel_balance() -> None:
    offenders = []
    bible = assembler.load_bible(BIBLE_PATH)
    examples = gate.collect_example_records(_text(), bible)

    for section_title in gate.TARGET_SECTION_TITLES:
        section_examples = [example for example in examples if section_title in example.heading_path and example.source]
        zones = {gate.source_zone(example.source) for example in section_examples}
        if section_examples and not {"OT", "Gospel"}.issubset(zones):
            block = _section_blocks()[section_title]
            if not gate.ONE_EXAMPLE_NOTE_RE.search(block.content):
                offenders.append(section_title)

    assert not offenders, f"Sections need both OT and Gospel evidence: {offenders}"


def test_grammar_facing_normalized_sections_keep_tables_examples_and_caveats() -> None:
    text = _text()
    tex = _tex_text()

    for section_title in gate.TARGET_SECTION_TITLES:
        section_text = _section_text(section_title)
        assert "|" in section_text, f"{section_title} lost its visible table"
        assert "(@ex:" in section_text, f"{section_title} lost its formal examples"

    assert "Deferred and boundary material" in text
    assert "deferred" in tex.lower()
    assert "boundary material" in tex.lower()
    assert "candidate row" not in text.lower()
