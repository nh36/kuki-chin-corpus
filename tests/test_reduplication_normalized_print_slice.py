from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_reduplication_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_reduplication_normalization.tsv"
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


def test_reduplication_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_reduplication_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert "# Editorial scope" not in text
    assert "editorial scope" not in lower
    assert "dictionary and review-note slices have not yet begun" not in lower
    assert "candidate tsv" not in lower
    assert "dossier" not in lower
    assert "review notes" not in lower


def test_reduplication_normalized_print_slice_has_required_structure_and_distinctions() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "# Overview of reduplication in Tedim",
        "Reduplication inventory",
        "Full reduplication as intensification",
        "Secondary distributive reduplication",
        "Boundary and deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "`mahmah` is the main full-reduplication intensifier anchor." in text
    assert "`pha mahmah hi` remains central" in text
    assert "`taktak` is the closest support row" in lower
    assert "quantifier or free-choice behavior" in lower

    for form in ("`ni ni`", "`leuleu`", "`gengen`", "`kawikawi`", "`theithei`", "`bangbang`", "`bekbek`", "`zenzen`", "`tuamtuam`"):
        assert form in text

    assert (
        "does not present a full reduplication, derivation, TAM/aspect, VP-structure, expressive-morphology, or dictionary-entry system."
        in text
    )


def test_reduplication_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:red-[^)]+\)", text, re.MULTILINE))

    assert example_count >= 6
    assert re.search(r"\(@ex:red-[^)]+\)\s+(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|1 Chronicles)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:red-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_reduplication_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:red-[^)]+\).*?(?=^\(@ex:red-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(
            r"^d\. Translation: .+\((?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|1 Chronicles|Matthew|Mark|Luke|John)\s+\d+:\d+\)$",
            block,
            re.MULTILINE,
        ), block


def test_reduplication_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_reduplication_normalized_print_slice_glosses_key_running_prose_forms() -> None:
    text = _text()
    expectations = {
        "mahmah": ("very, truly",),
        "taktak": ("truly, certainly",),
        "peuhpeuh": ("every, each",),
        "pha mahmah hi": ("good very DECL",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_reduplication_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "reduplication_topic",
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
