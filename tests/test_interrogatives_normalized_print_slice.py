from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_interrogatives_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_interrogatives_normalization.tsv"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _strip_examples_and_tables(text: str) -> str:
    lines = text.splitlines()
    kept: list[str] = []
    skip_example = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("(@ex:"):
            skip_example = True
            continue
        if skip_example:
            if not stripped:
                skip_example = False
            continue
        if stripped.startswith("|"):
            continue
        kept.append(line)
    return "\n".join(kept)


def _first_prose_occurrence_has_gloss(text: str, form: str, glosses: tuple[str, ...]) -> bool:
    prose = _strip_examples_and_tables(text)
    match = re.search(rf"`{re.escape(form)}`", prose)
    if not match:
        return True
    window = prose[match.end() : match.end() + 180]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_interrogatives_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_interrogatives_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert "Editorial summary" not in text
    assert "editorial summary" not in lower
    assert "candidates_interrogatives.tsv" not in text
    assert "dossier_interrogatives.md" not in text
    assert "print-facing draft" not in lower
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)
    assert "# Overview of interrogatives in Tedim" in text


def test_interrogatives_normalized_print_slice_has_required_structure_and_content() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Interrogative inventory",
        "Clause-final `hiam` 'question particle'",
        "WH + `hiam` content questions",
        "`bang` 'what'",
        "`kua` 'who'",
        "`bangci` 'how'",
        "`banghangin` 'why'",
        "Embedded-question boundary",
        "Blocked false friends and non-interrogative `hiam`",
        "Deferred comparison particles",
        "Deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    for item in ("`hiam`", "`bang`", "`kua`", "`bangci`", "`banghangin`", "`bang hiam cih`", "`bangmah`", "`bangin`", "`maw`", "`ham`", "`em`"):
        assert item in text
    assert "question particle" in lower
    assert "what ... saying" in lower
    assert "question/comparison particle" in lower


def test_interrogatives_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:int-[^)]+\)", text, re.MULTILINE))

    assert example_count >= 10
    assert re.search(r"\(@ex:int-[^)]+\)\s+(Genesis|Exodus|Luke|Matthew)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:int-[^)]+\)\s+(Matthew|Luke)\s+\d+:\d+", text)


def test_interrogatives_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:int-[^)]+\).*?(?=^\(@ex:int-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_interrogatives_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_interrogatives_normalized_print_slice_keeps_banghangin_as_a_formal_example() -> None:
    text = _text()

    assert "bang hangin na mai sia ahi hiam" in text
    assert "Bang hangin puansilh ding lunghimawh na hi uh hiam?" in text


def test_interrogatives_normalized_print_slice_keeps_boundary_material_visible() -> None:
    text = _text()
    lower = text.lower()

    assert "bang hiam cih thei lo uh hi" in text
    assert "Bang hang hiam cih leh" in text
    assert "langnih a hiam namsau" in text
    assert "a hiam ciat uh" in text
    assert "`maw` 'question/comparison particle'" in text
    assert "`ham` 'question/comparison particle'" in text
    assert "`em` 'question/comparison particle'" in text
    assert "remain deferred" in lower


def test_interrogatives_normalized_print_slice_avoids_internal_project_terms_and_raw_count_claims() -> None:
    text = _text()
    lower = text.lower()
    body = lower

    for forbidden in (
        "packet",
        "candidate tsv",
        "dossier",
        "review notes",
        "coverage normalization",
        "print slice",
        "publication-review",
        "current pass",
        "tests/",
        "scripts/",
        "output/",
        "docs/",
        "5,230",
        "10,000+",
    ):
        assert forbidden not in body


def test_interrogatives_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "hiam": ("question particle",),
        "bang": ("what",),
        "kua": ("who",),
        "bangci": ("how",),
        "banghangin": ("why",),
        "bang hiam cih": ("what ... saying",),
        "Bang hang hiam cih leh": ("because / for this reason",),
        "langnih a hiam namsau": ("two-edged sword",),
        "a hiam ciat uh": ("each of them",),
        "bangmah": ("nothing",),
        "bangin": ("as / how",),
        "maw": ("question/comparison particle",),
        "ham": ("question/comparison particle",),
        "em": ("question/comparison particle",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_interrogatives_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "interrogative_topic",
        "candidate_form",
        "construction_type",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "example_quality",
        "print_status",
        "why_selected",
        "caveat",
    ):
        assert column in header
