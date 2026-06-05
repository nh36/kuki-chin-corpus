from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_derivation_valency_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_derivation_valency_normalization.tsv"


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


def test_derivation_valency_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_derivation_valency_normalized_print_slice_has_inventory_and_core_sections() -> None:
    text = _text()

    assert "Current derivation / valency inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "Causative `-sak`" in text
    assert "Benefactive and applicative-like `-sak`" in text
    assert "The practical split within `-sak`" in text
    assert "Boundary with `-pih`" in text
    assert "Boundary with `ki-`" in text
    assert "Boundary with VP stacking" in text
    assert "Boundary with transitivity" in text
    assert "Several issues remain outside the present account." in text


def test_derivation_valency_normalized_print_slice_discusses_safe_anchors_and_boundaries() -> None:
    text = _text()

    for required in (
        "paisak",
        "muhsak",
        "Form I plus `-sak`",
        "Form II plus `-sak`",
        "paipih",
        "mipihte",
        "kisep",
        "kigen",
        "ciahsakkik",
        "bawlsakthei",
        "paikhiatsak",
        "piangsak",
    ):
        assert required in text


def test_derivation_valency_normalized_print_slice_has_multiple_formal_examples() -> None:
    text = _text()

    assert len(re.findall(r"^\(@ex:deriv-[^)]+\)", text, re.MULTILINE)) >= 4


def test_derivation_valency_normalized_print_slice_shows_old_testament_and_gospel_examples() -> None:
    text = _text()

    assert re.search(r"\(@ex:deriv-[^)]+\)\s+(Exodus|Habakkuk|Genesis)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:deriv-[^)]+\)\s+(Mark|John|Luke|Matthew)\s+\d+:\d+", text)


def test_derivation_valency_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
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

    assert "# Scope" not in text
    assert "# Editorial scope" not in text
    assert not re.search(r"\b\d{1,3}(?:,\d{3})+\b", text)


def test_derivation_valency_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "-sak": ("causative", "benefactive"),
        "paisak": ("cause to go", "go-CAUS"),
        "muhsak": ("show", "make see"),
        "-pih": ("with", "accompanying"),
        "paipih": ("go with", "accompany"),
        "mipihte": ("companions", "associated people"),
        "ki-": ("reflexive", "passive-like"),
        "kisep": ("REFL-work", "do by oneself"),
        "kigen": ("be said", "it is said"),
        "ciahsakkik": ("send back", "return"),
        "bawlsakthei": ("can cause to make", "make-CAUS-ABIL"),
        "paikhiatsak": ("cause to go out", "go out"),
        "piangsak": ("cause to be born", "create"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_derivation_valency_examples_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    for column in (
        "example_id",
        "derivation_topic",
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
