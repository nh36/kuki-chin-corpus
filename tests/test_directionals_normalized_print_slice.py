from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_directionals_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_directionals_normalization.tsv"


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
    window = prose[match.end() : match.end() + 160]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_directionals_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_directionals_normalized_print_slice_has_inventory_and_core_sections() -> None:
    text = _text()

    assert "Current directional inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "Outward and away direction" in text
    assert "Upward direction and directionals in the verb phrase" in text
    assert "Toward direction with `-sawn`" in text
    assert "Downward direction with `-suk`" in text
    assert "Deictic boundary" in text
    assert "TAM and VP-structure boundary" in text
    assert "Several issues remain outside the present account." in text


def test_directionals_normalized_print_slice_discusses_safe_contrasts_and_boundaries() -> None:
    text = _text()

    for required in (
        "pokhia",
        "nawhkhiat",
        "hotkhiatna",
        "kilaktoh",
        "kahtohna",
        "paitoh",
        "piasawn",
        "paisuk",
        "tawplam",
        "`va-` 'away'",
        "`hong-` 'toward the deictic center'",
        "before `ding` 'irrealis / prospective'",
    ):
        assert required in text


def test_directionals_normalized_print_slice_has_multiple_formal_examples() -> None:
    text = _text()

    assert len(re.findall(r"^\(@ex:dir-[^)]+\)", text, re.MULTILINE)) >= 4


def test_directionals_normalized_print_slice_shows_old_testament_and_gospel_examples() -> None:
    text = _text()

    assert re.search(r"\(@ex:dir-[^)]+\)\s+(Genesis|Exodus|Numbers|Deuteronomy|Ezra)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:dir-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_directionals_normalized_print_slice_uses_explicit_notes_for_imbalanced_subsections() -> None:
    text = _text()

    assert "No equally clean Gospel example is currently used for this construction, so the section keeps the compact Old Testament anchors." in text
    assert "This construction is rare in the controlled evidence, so one example is used here and broader source balancing remains outside the present account." in text


def test_directionals_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
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


def test_directionals_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "-khia": ("outward", "out"),
        "-khiat": ("away",),
        "-toh": ("upward", "up"),
        "-sawn": ("toward",),
        "-suk": ("downward", "down"),
        "-lam": ("sideward", "toward a side", "side"),
        "hotkhiatna": ("salvation",),
        "kahtohna": ("going up", "ascent"),
        "paitoh": ("go-accompany", "accompany"),
        "tawplam": ("toward the side", "at the edge", "side"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_directionals_examples_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()

    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")
    for column in (
        "example_id",
        "directional_topic",
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


def test_directionals_examples_supplement_includes_old_testament_and_gospel_rows() -> None:
    text = SUPPLEMENT_PATH.read_text(encoding="utf-8")

    assert "\tOld Testament\t" in text
    assert "\tGospels\t" in text
