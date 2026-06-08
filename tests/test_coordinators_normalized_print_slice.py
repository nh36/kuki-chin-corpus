from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_coordinators_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_coordinators_normalization.tsv"
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
    window = prose[match.end() : match.end() + 220]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_coordinators_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_coordinators_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert not re.search(r"(?im)^#\s*summary\s*$", text)
    assert "dictionary and review-note slices have not yet begun" not in lower
    assert "dictionary and review-note work have not yet begun" not in lower
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)

    for forbidden in (
        "packet",
        "candidate tsv",
        "dossier",
        "review notes",
        "coverage normalization",
        "print slice",
        "publication-review",
        "current pass",
        "ready for human review",
    ):
        assert forbidden not in lower


def test_coordinators_normalized_print_slice_has_required_structure_and_distinctions() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "# Overview of coordinators in Tedim",
        "Coordinator inventory",
        "NP coordination with `le`",
        "Conditional and boundary `leh`",
        "Sequential `a` and agreement false friends",
        "Deferred `mawh` material",
        "Adversative `Ahih hangin`",
        "Conditional-adversative `ahih kei leh`",
        "Deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "`vantung le leitung` 'heaven and earth'" in text
    assert "do not flatten conditional `leh`" in text
    assert "`a piangsak` '3SG/FUNC + create'" in text
    assert "Report-only schematic strings" in text
    assert "does not present a full coordination, subordination, converb, or discourse system." in lower


def test_coordinators_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:coord-[^)]+\)", text, re.MULTILINE))

    assert example_count >= 7
    assert re.search(r"\(@ex:coord-[^)]+\)\s+(Genesis|Exodus|Leviticus|Numbers|Psalms?)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:coord-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_coordinators_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:coord-[^)]+\).*?(?=^\(@ex:coord-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(
            r"^d\. Translation: .+\((?:Genesis|Exodus|Leviticus|Numbers|Psalms?|Matthew|Mark|Luke|John)\s+\d+:\d+\)$",
            block,
            re.MULTILINE,
        ), block


def test_coordinators_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_coordinators_normalized_print_slice_keeps_required_boundaries_visible() -> None:
    text = _text()
    lower = text.lower()

    assert "No equally clean Gospel example is currently used for this construction." in text
    assert "not promoted as grammar evidence" in lower
    assert "not a simple coordinator" in lower
    assert "`ciangin` 'when', broader `hangin` 'because'" in text
    assert "sentence-final particles and broader discourse-organization domains" in lower


def test_coordinators_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "le": ("NP coordinator",),
        "vantung le leitung": ("heaven and earth",),
        "leh": ("if / when",),
        "a": ("sequential linker", "3SG/FUNC overlap"),
        "a piangsak": ("3SG/FUNC", "create"),
        "mawh": ("deferred disjunction material",),
        "Ahih hangin": ("but / however",),
        "ahih kei leh": ("otherwise / if not",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_coordinators_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "coordinator_topic",
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

    text = SUPPLEMENT_PATH.read_text(encoding="utf-8")
    assert "\tOT\t" in text
    assert "\tGospel\t" in text
