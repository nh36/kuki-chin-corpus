from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_demonstratives_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_demonstratives_normalization.tsv"
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
    window = prose[match.end() : match.end() + 180]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in glosses)


def test_demonstratives_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_demonstratives_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert "Scope" not in text.splitlines()[:12]
    assert "Editorial summary" not in text
    assert "editorial summary" not in lower
    assert "# Overview of demonstratives and deixis in this section" in text
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)


def test_demonstratives_normalized_print_slice_has_required_structure_and_content() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Current demonstrative inventory",
        "Core demonstratives: hih and tua",
        "Plural demonstratives",
        "Adnominal and pronominal uses",
        "Discourse and temporal deixis",
        "Manner constructions with bangin",
        "Deferred forms:",
        "Boundary with interrogatives and quantifiers",
        "Deferred material",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text
    assert "`hih`" in text and "`tua`" in text
    assert "`hihte`" in text and "`tuate`" in text
    assert "`hih bangin`" in text and "`tua bangin`" in text
    assert "`tua ciangin`" in text and "`tua ahih ciangin`" in text
    assert "`hi`" in text and "`hih ciangin`" in text
    assert "`kua`" in text and "`bang`" in text and "`kuamah`" in text and "`bangmah`" in text
    assert "`huā`" in text
    assert "copular" in lower
    assert "sentence-final" in lower
    assert "clause linkage" in lower


def test_demonstratives_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:dem-[^)]+\)", text, re.MULTILINE))
    has_explanation_for_fewer = "Several issues remain outside the present account." in text
    assert example_count >= 7 or has_explanation_for_fewer

    assert re.search(r"\(@ex:dem-[^)]+\)\s+(Genesis|Exodus|Jeremiah)\s+\d+:\d+", text)
    assert (
        re.search(r"\(@ex:dem-[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)
        or "No equally clean Gospel example is currently used" in text
    )


def test_demonstratives_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:dem-[^)]+\).*?(?=^\(@ex:dem-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_demonstratives_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_demonstratives_normalized_print_slice_avoids_internal_project_terms_and_raw_count_claims() -> None:
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
        "output/",
        "docs/",
    ):
        assert forbidden not in lower_body

    assert "raw occurrence counts are not treated as grammar facts" in lower_body


def test_demonstratives_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "hih": ("this",),
        "tua": ("that", "aforementioned"),
        "hihte": ("these",),
        "tuate": ("those",),
        "-te": ("plural",),
        "hih bangin": ("like this", "thus"),
        "tua bangin": ("like that", "thus"),
        "tua ciangin": ("then", "at that time"),
        "tua ahih ciangin": ("when that was so", "then"),
        "hi": ("be", "copula"),
        "hih ciangin": ("when this", "when doing thus"),
        "huā": ("distal demonstrative",),
        "kua": ("who",),
        "bang": ("what",),
        "kuamah": ("nobody",),
        "bangmah": ("nothing",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_demonstratives_normalization_supplement_exists_and_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    header = SUPPLEMENT_PATH.read_text(encoding="utf-8").splitlines()[0].split("\t")

    for column in (
        "example_id",
        "demonstrative_topic",
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
