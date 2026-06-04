from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_tam_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_tam_normalization.tsv"


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
    window = prose[match.end() : match.end() + 170]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_tam_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_tam_normalized_print_slice_has_inventory_and_core_sections() -> None:
    text = _text()

    assert "Current TAM inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "Perfect, completive, and change-of-state material" in text
    assert "Habitual, continuative, and experiential aspect" in text
    assert "Prospective and irrealis marking" in text
    assert "Ability and modal marking" in text
    assert "Repetition and return marking" in text
    assert "Boundary with negation and sentence-final particles" in text
    assert "Boundary with directionals and VP structure" in text
    assert "Several issues remain outside the present account." in text


def test_tam_normalized_print_slice_discusses_safe_anchors_and_boundaries() -> None:
    text = _text()

    for required in (
        "-ngei",
        "-gige",
        "-zel",
        "-ta",
        "-zo",
        "-kik",
        "-ding",
        "-thei",
        "paingei",
        "dingin",
        "khiathei ding om lo",
        "mangngilh ta hi",
        "khia-ta",
        "bawlzoding",
        "bawlsakthei",
    ):
        assert required in text


def test_tam_normalized_print_slice_has_multiple_formal_examples() -> None:
    text = _text()

    assert len(re.findall(r"^\(@ex:tam-[^)]+\)", text, re.MULTILINE)) >= 8


def test_tam_normalized_print_slice_shows_old_testament_and_gospel_examples() -> None:
    text = _text()

    assert re.search(r"\(@ex:tam-[^)]+\)\s+(Genesis|Exodus|Leviticus|Psalms?)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:tam-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_tam_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
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


def test_tam_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "-ngei": ("ever", "experiential"),
        "-gige": ("habitually", "always"),
        "-zel": ("continuative", "keep doing"),
        "-ta": ("completive", "change-of-state"),
        "-zo": ("already", "completive"),
        "-ding": ("prospective", "irrealis"),
        "-thei": ("can", "be able"),
        "-kik": ("again", "back"),
        "dingin": ("clause-bound", "for"),
        "pailai": ("go-midst", "prospective"),
        "khia-ta": ("out-PFV", "out"),
        "bawlzoding": ("make-COMPL-IRR", "completive"),
        "bawlsakthei": ("make-CAUS-ABIL", "abilitative"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_tam_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)

    assert rows
    assert "source_zone" in reader.fieldnames
    assert "example_quality" in reader.fieldnames
    assert any(row["source_zone"] == "Old Testament" for row in rows)
    assert any(row["source_zone"] == "Gospels" for row in rows)
