from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_negation_print_slice.md"
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


def test_negation_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_negation_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert not re.search(r"(?im)^#\s*summary\s*$", text)
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)
    assert "candidates_negation.tsv" not in text
    assert "dossier_negation.md" not in text
    assert "review_notes_negation.md" not in text

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
    ):
        assert forbidden not in lower


def test_negation_normalized_print_slice_has_required_structure_and_topics() -> None:
    text = _text()
    lower = text.lower()

    assert "# Overview of negation in Tedim" in text
    assert "Negation inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "Clause-level negation with `lo`" in text
    assert "Dependent and derived negation with `loh`" in text
    assert "`kei` in prohibitives and irrealis-heavy negation" in text
    assert "Ordinary plural negative predicates are not automatically prohibitive" in text
    assert "`V lo uh` is not automatically a prohibitive" in text
    assert "Negative existence and absence" in text
    assert "Cessative `nawn lo`" in text
    assert "Ability and inability" in text
    assert "Negative polarity items" in text
    assert "filtered, manually checked" in lower
    assert "Deferred material" in text
    assert "Several issues remain outside the present account." in text
    assert "raw exact-string counts overgenerate" in lower


def test_negation_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:neg-[^)]+\)", text, re.MULTILINE))

    assert example_count >= 6
    assert re.search(r"\(@ex:neg-[^)]+\)\s+(Genesis|Exodus|Leviticus|Numbers|Psalms?)\s+\d+:\d+", text)
    assert re.search(r"\(@ex:neg-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)


def test_negation_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:neg-[^)]+\).*?(?=^\(@ex:neg-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(
            r"^d\. Translation: .+\((?:Genesis|Exodus|Leviticus|Numbers|Psalms?|Matthew|Mark|Luke|John)\s+\d+:\d+\)$",
            block,
            re.MULTILINE,
        ), block


def test_negation_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_negation_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "lo": ("NEG",),
        "lo hi": ("NEG DECL",),
        "loh": ("dependent / derived NEG",),
        "loh ding-a": ("NEG.DEP IRR-LOC/FUNC", "NEG.DEP IRR-ERG"),
        "kei": ("NEG / prohibitive NEG",),
        "kei in": ("NEG IMP.SG",),
        "kei un": ("NEG IMP.PL",),
        "maizum lo uh hi": ("they were not ashamed",),
        "om lo hi": ("not exist / be absent",),
        "nei lo hi": ("not have",),
        "nawn lo": ("no longer", "not again"),
        "thei lo": ("cannot", "not know"),
        "theih loh": ("not being able", "dependent inability"),
        "kuamah": ("nobody",),
        "bangmah": ("nothing",),
        "tua bangmah hi-in": ("likewise", "in that way"),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_negation_normalized_print_slice_avoids_raw_report_counts_as_grammar_facts() -> None:
    text = _text()

    assert not re.search(r"\b\d{1,3}(?:,\d{3})+\b", text)
    assert "10,000+" not in text
