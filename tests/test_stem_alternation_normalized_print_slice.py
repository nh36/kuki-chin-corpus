from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_stem_alternation_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_stem_alternation_normalization.tsv"
BIB_PATH = ROOT / "literature/bibliography.bib"


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


def test_stem_alternation_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_stem_alternation_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert "# Overview of stem alternation" in text
    assert "draft argument plan" not in lower
    assert "eventual prose" not in lower
    assert "next commit" not in lower
    assert "writing order" not in lower
    assert "quotation-safe layer" not in lower
    assert "## Scope" not in text
    assert "## Editorial scope" not in text
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)


def test_stem_alternation_normalized_print_slice_has_required_structure() -> None:
    text = _text()

    for required in (
        "Overview of stem alternation",
        "Stem alternation inventory",
        "Core alternation patterns",
        "Grammatical environments for alternants",
        "Relation to prefix/agreement",
        "Relation to TAM and directionals",
        "Formal examples",
        "Dictionary-facing implications",
        "Deferred questions",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Lexical meaning | Form I | Form II | Diagnostic environment | Source | Status |" in text
    assert "| Pattern | Representative pairs | What current evidence supports | What remains open |" in text


def test_stem_alternation_normalized_print_slice_explains_stem_terminology() -> None:
    text = _text()
    lower = text.lower()
    bibliography = BIB_PATH.read_text(encoding="utf-8")

    assert "@book{henderson1965" in bibliography
    assert "@phdthesis{zamngaihcing2017" in bibliography
    assert "Form I / Form II" in text
    assert "Stem 1 / Stem 2" in text
    assert "[@henderson1965; @zamngaihcing2017]" in text
    assert "does not claim that the full verb-stem paradigm is already complete" in lower


def test_stem_alternation_normalized_print_slice_discusses_controlled_pairs_and_environments() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "mu / muh",
        "ne / nek",
        "nei / neih",
        "za / zak",
        "pia / piak",
        "nusia / nusiat",
        "thei / theih",
        "piang / pian",
        "ngai / ngaih",
        "honkhia / honkhiat",
        "ciangin",
        "ni-in",
        "kipan",
        "nadingin",
        "-na",
        "mi",
    ):
        assert required in text

    assert "finite" in lower
    assert "dependent" in lower
    assert "nominalized" in lower


def test_stem_alternation_normalized_print_slice_coordinates_with_prefix_tam_directionals() -> None:
    text = _text()
    lower = text.lower()

    assert "Relation to prefix/agreement" in text
    assert "`ka-nei`" in text
    assert "agreement-before-verbal-host" in lower or "prefix/agreement chapter" in lower

    assert "Relation to TAM and directionals" in text
    assert "`-ding`" in text
    assert "directional" in lower
    assert "dedicated chapters" in lower or "dedicated chapter" in lower


def test_stem_alternation_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    example_count = len(re.findall(r"^\(@ex:stem-[^)]+\)", text, re.MULTILINE))
    assert example_count >= 8

    assert re.search(r"\(@ex:stem-[^)]+\)\s+(Genesis|Exodus|Psalms|2 Samuel)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:stem-[^)]+\)\s+(Luke|Matthew|Mark|John)\s+\d+:\d+", text)


def test_stem_alternation_normalized_print_slice_avoids_internal_workflow_language() -> None:
    text = _text()
    lower = text.lower()

    for forbidden in (
        "packet",
        "candidate layer",
        "candidate tsv",
        "dossier",
        "review notes",
        "print slice",
        "workflow",
        "publication-review",
        "boundary row",
        "boundary material",
    ):
        assert forbidden not in lower


def test_stem_alternation_normalized_print_slice_glosses_key_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "mu / muh": ("see",),
        "ne / nek": ("eat",),
        "nei / neih": ("have",),
        "za / zak": ("hear", "listen"),
        "pia / piak": ("give",),
        "nusia / nusiat": ("leave", "forsake"),
        "thei / theih": ("know", "be able"),
        "piang / pian": ("be born", "arise"),
        "ciangin": ("when",),
        "ni-in": ("on the day", "when"),
        "kipan": ("from", "since"),
        "nadingin": ("in order to",),
        "-na": ("nominalizer",),
        "mi": ("person", "one who"),
        "ka-nei": ("1SG-have",),
        "neih mi": ("have.II person",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_stem_alternation_normalized_print_slice_has_deferred_questions_requested_scope() -> None:
    text = _text()
    lower = text.lower()

    assert "Deferred questions" in text
    for required in (
        "full verb-stem paradigm",
        "historical origin",
        "tonal alternations",
        "complete conditioning environments",
        "interaction with the full TAM inventory",
        "interaction with the full directional system",
        "full lexical coverage",
    ):
        assert required.lower() in lower


def test_stem_alternation_examples_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    for column in (
        "example_id",
        "stem_topic",
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
        assert column in reader.fieldnames

    assert any(row["source_zone"] == "Old Testament" for row in rows)
    assert any(row["source_zone"] == "Gospels" for row in rows)
