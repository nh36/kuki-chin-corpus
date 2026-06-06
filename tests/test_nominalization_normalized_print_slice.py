from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_nominalization_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_nominalization_normalization.tsv"


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


def test_nominalization_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_nominalization_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Editorial scope")
    assert "# Overview of nominalization in this section" in text
    assert "Scope" not in text.splitlines()[:12]
    assert "editorial scope" not in lower
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)


def test_nominalization_normalized_print_slice_has_required_structure() -> None:
    text = _text()

    for required in (
        "Current nominalization inventory",
        "Deverbal nominalization with `-na`",
        "Nominalization and stem alternation",
        "Agentive or person-head nominalization boundary",
        "Nominalized relatives and clause-derived nominalization boundary",
        "Nominalization plus case boundary",
        "Lexicalized and title-like boundary material",
        "Deferred and boundary material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text


def test_nominalization_normalized_print_slice_discusses_safe_core_and_boundaries() -> None:
    text = _text()
    lower = text.lower()

    assert "productive deverbal" in lower
    assert "`-na`" in text
    assert "`bawlna`" in text or "`ciaptehna`" in text
    assert "Nominalization and stem alternation" in text
    assert "`-pa`" in text and "`-mi`" in text
    assert "boundary" in lower
    assert "`omna`" in text or "`a bawl mi`" in text
    assert "`muhna-ah`" in text
    assert "`kumpipa`" in text and "`Topa`" in text


def test_nominalization_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:nmlz-[^)]+\)", text, re.MULTILINE))
    has_explanation_for_fewer = "Several issues remain outside the present account." in text
    assert example_count >= 4 or has_explanation_for_fewer

    assert re.search(r"\(@ex:nmlz-[^)]+\)\s+(Genesis|Exodus|Judges|Zechariah)\s+\d+:\d+", text)
    assert (
        re.search(r"\(@ex:nmlz-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)
        or "No equally clean Gospel example is currently used" in text
    )


def test_nominalization_normalized_print_slice_avoids_internal_project_terms_and_raw_count_claims() -> None:
    text = _text()
    lower = text.lower()
    if lower.startswith("---"):
        parts = lower.split("---", 2)
        lower_body = parts[2] if len(parts) == 3 else lower
    else:
        lower_body = lower

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
    ):
        assert forbidden not in lower_body

    assert "report-only counts" not in lower_body
    assert "raw occurrence counts are not treated as grammar facts" in lower_body


def test_nominalization_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "-na": ("nominalizer",),
        "bawlna": ("making", "creation"),
        "bawl-na": ("make-NMLZ",),
        "-pa": ("agentive", "person"),
        "-mi": ("person", "one who"),
        "hong pai mi": ("one who came", "person who came"),
        "omna": ("place", "being", "existence"),
        "muhna-ah": ("in seeing", "in the sight"),
        "kumpipa": ("king",),
        "Topa": ("Lord",),
        "a bawl mi": ("one who made", "person who made"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_nominalization_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    for column in (
        "example_id",
        "nominalization_topic",
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
