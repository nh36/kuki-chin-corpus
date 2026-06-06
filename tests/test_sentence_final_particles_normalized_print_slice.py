from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_sentence_final_particles_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_sentence_final_particles_normalization.tsv"
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
    window = prose[match.end() : match.end() + 190]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_sentence_final_particles_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_sentence_final_particles_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert "Editorial summary" not in text
    assert "editorial summary" not in lower
    assert "candidates_sentence_final_particles.tsv" not in text
    assert "dossier_sentence_final_particles.md" not in text
    assert "print-facing draft" not in lower
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)
    assert "# Overview of sentence-final particles in Tedim" in text


def test_sentence_final_particles_normalized_print_slice_has_required_structure_and_content() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Sentence-final particle inventory",
        "Declarative `hi` with copula overlap",
        "Negative-plus-declarative `lo hi`",
        "Optative or jussive `hen`",
        "Imperative `in` and `un`",
        "`Hiam` as interrogatives overlap",
        "`Aw` as vocative or exclamative boundary",
        "`Tahen`, `ta`, and `zo` as deferred TAM-overlap material",
        "Deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    for item in ("`hi`", "`ahi hi`", "`lo hi`", "`hen`", "`in`", "`un`", "`hiam`", "`aw`", "`tahen`", "`ta`", "`zo`"):
        assert item in text
    assert "question particle" in lower
    assert "vocative / exclamative boundary" in lower
    assert "deferred jussive-looking form" in lower


def test_sentence_final_particles_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:sfp-[^)]+\)", text, re.MULTILINE))

    assert example_count >= 8
    assert re.search(r"\(@ex:sfp-[^)]+\)\s+(Genesis|Psalms?)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:sfp-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_sentence_final_particles_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:sfp-[^)]+\).*?(?=^\(@ex:sfp-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\((?:Genesis|Psalms?|Matthew|Mark|Luke|John)\s+\d+:\d+\)$", block, re.MULTILINE), block


def test_sentence_final_particles_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_sentence_final_particles_normalized_print_slice_keeps_required_boundaries_visible() -> None:
    text = _text()
    lower = text.lower()

    assert "does not reopen independent `hiam` analysis" in lower
    assert "`Gam khempeuh aw` 'all lands!'" in text
    assert "`David suan Josef aw` 'Joseph, son of David!'" in text
    assert "`tahen` 'deferred jussive-looking form'" in text
    assert "`ta` 'perfective / change-of-state boundary'" in text
    assert "`zo` 'completive boundary'" in text


def test_sentence_final_particles_normalized_print_slice_has_no_blockquote_example_placeholders() -> None:
    text = _text()

    assert not re.search(r"(?m)^\s*>\s+", text)


def test_sentence_final_particles_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
    text = _text()
    body = text.lower()

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
        "24,754",
        "5,230",
    ):
        assert forbidden not in body


def test_sentence_final_particles_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "hi": ("declarative",),
        "ahi hi": ("be.3SG DECL", "it was"),
        "lo hi": ("NEG DECL",),
        "hen": ("jussive", "optative"),
        "in": ("imperative",),
        "un": ("plural imperative",),
        "hiam": ("question particle",),
        "aw": ("vocative", "exclamative"),
        "tahen": ("deferred jussive-looking form",),
        "ta": ("perfective", "change-of-state"),
        "zo": ("completive",),
        "Khuavak om hen": ("let there be light",),
        "teembaw khat bawl in": ("make an ark",),
        "gingsak un": ("make a joyful noise",),
        "Gam khempeuh aw": ("all lands",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_sentence_final_particles_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "sfp_topic",
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
