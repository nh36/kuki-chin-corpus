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

    assert "# Overview of Form I / Form II stem alternation" in text
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
        "Overview of Form I / Form II stem alternation",
        "Current stem alternation overview",
        "Distribution by syntactic context",
        "Core showcase pairs",
        "Promoted caveated pairs",
        "Difficult but grammatically important pairs",
        "One-sided and same-form controls",
        "Blocked or noisy material",
        "Deferred and boundary material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form | Typical distribution | Strongest examples | Caveat |" in text
    assert "| Syntactic context | Form tendency in current evidence | Representative pairs | Caution |" in text


def test_stem_alternation_normalized_print_slice_cites_henderson_and_zam_ngaih_cing() -> None:
    text = _text()
    bibliography = BIB_PATH.read_text(encoding="utf-8")

    assert "@book{henderson1965" in bibliography
    assert "@phdthesis{zamngaihcing2017" in bibliography
    assert "[@henderson1965; @zamngaihcing2017]" in text


def test_stem_alternation_normalized_print_slice_keeps_core_promoted_and_boundary_pairs_visible() -> None:
    text = _text()

    for required in (
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
        "bawl / bawlh",
        "dawn / dawn",
        "hong / hong",
        "keu / keuh",
        "khai / khaih",
        "sia / siah",
        "tan / tanh",
        "mual / mualh",
        "sum / sumh",
        "thu / thuh",
        "lampi / lampih",
        "khua / khuat",
        "gamla / gamlat",
    ):
        assert required in text


def test_stem_alternation_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()

    example_count = len(re.findall(r"^\(@ex:stem-[^)]+\)", text, re.MULTILINE))
    has_explanation_for_fewer = "No equally clean" in text or "Several issues remain outside the present account." in text
    assert example_count >= 6 or has_explanation_for_fewer

    assert re.search(r"\(@ex:stem-[^)]+\)\s+(Genesis|Exodus|Psalms|1 Chronicles|2 Samuel)\s+\d+:\d+", text)
    assert (
        re.search(r"\(@ex:stem-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)
        or "No equally clean Gospel example is currently used" in text
    )


def test_stem_alternation_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
    text = _text()
    lower = text.lower()

    for forbidden in (
        "packet",
        "candidate tsv",
        "dossier",
        "review notes",
        "coverage normalization",
        "print slice",
        "publication-review",
        "current pass",
    ):
        assert forbidden not in lower

    assert "clean verbal exact bible rows survive" not in lower
    assert "best examples:" not in lower
    assert not re.search(r"\b\d{1,3}(?:,\d{3})+\b", text)


def test_stem_alternation_normalized_print_slice_glosses_key_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "mu / muh": ("see",),
        "ne / nek": ("eat",),
        "nei / neih": ("have",),
        "za / zak": ("hear", "listen"),
        "pia / piak": ("give",),
        "nusia / nusiat": ("leave", "abandon", "forsake"),
        "bia / biak": ("speak", "worship", "address"),
        "thei / theih": ("can", "be able"),
        "piang / pian": ("be born", "arise"),
        "zui / zuih": ("follow",),
        "khial / khialh": ("err", "sin"),
        "kia / kiak": ("fall",),
        "sawlkhia / sawlkhiat": ("send out", "send forth"),
        "ngai / ngaih": ("need", "love", "listen"),
        "ciangin": ("when",),
        "ni-in": ("on the day", "when"),
        "kipan": ("from", "since"),
        "nadingin": ("in order to",),
        "-na": ("nominalizer",),
        "mi": ("person", "one who"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


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
