from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SLICE_PATH = ROOT / "output/publication_review/grammar_relators_postpositions_print_slice.md"


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
    window = prose[match.end() : match.end() + 140]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_relators_postpositions_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_relators_postpositions_normalized_print_slice_has_inventory_and_core_sections() -> None:
    text = _text()

    assert "Current relator / postposition inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "Spatial relator nouns" in text
    assert "Relator plus case-like marking" in text
    assert "Postpositional phrase structure" in text
    assert "Case-marking boundary" in text
    assert "Possession and NP-structure boundary" in text
    assert "Several issues remain outside the present account." in text


def test_relators_postpositions_normalized_print_slice_has_multiple_formal_examples() -> None:
    text = _text()

    assert len(re.findall(r"^\(@ex:rel-[^)]+\)", text, re.MULTILINE)) >= 4


def test_relators_postpositions_normalized_print_slice_shows_old_testament_and_gospel_examples() -> None:
    text = _text()

    assert re.search(r"\(@ex:rel-[^)]+\)\s+(Genesis|Exodus)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:rel-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_relators_postpositions_normalized_print_slice_avoids_internal_project_terms_and_raw_counts() -> None:
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


def test_relators_postpositions_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()

    expectations = {
        "sung": ("inside", "within"),
        "tung": ("on", "upon"),
        "kiang": ("beside", "near"),
        "lak": ("among", "midst"),
        "pualam": ("outside",),
        "sungah": ("inside", "in"),
        "tungah": ("on", "upon"),
        "kiangah": ("beside", "near"),
        "lakpan": ("from among",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form
