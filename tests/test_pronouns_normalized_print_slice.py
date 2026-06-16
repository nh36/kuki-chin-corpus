from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_pronouns_print_slice.md"
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


def test_pronouns_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_pronouns_normalized_print_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert not text.lstrip().startswith("# Scope")
    assert "Scope" not in text.splitlines()[:12]
    assert "Editorial summary" not in text
    assert "editorial summary" not in lower
    assert "# Overview of Tedim pronouns" in text
    assert not re.search(r"(?:output|tests|scripts|docs)/[A-Za-z0-9_./\\-]+", text)


def test_pronouns_normalized_print_slice_has_required_structure_and_content() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Pronoun inventory",
        "Independent personal pronouns",
        "First-person plural forms and clusivity",
        "Second- and third-person forms",
        "Pronouns and possession",
        "Independent pronouns versus prefix/agreement marking",
        "Pronouns with case and relator marking",
        "Emphatic pronouns in -mah",
        "Reflexive and reciprocal ki- boundary",
        "Participant-oriented hong- and kong- boundary",
        "Boundary with demonstratives, interrogatives, quantifiers, and wider agreement",
        "Deferred questions",
        "Several issues remain outside the present account.",
    ):
        assert required in text

    assert "| Domain | Controlled forms | Function | Status | Notes |" in text
    assert "`amah`" in text and "`note`" in text
    assert "`eite`" in text and "`kote`" in text
    assert "`na-`" in text and "`a-`" in text and "`i-`" in text
    assert "`kanei`" in text and "`ka-nei`" in text and "`kainn`" in text and "`ka-inn`" in text
    assert "`keimah`" in text and "`nangmah`" in text
    assert "`ki-`" in text and "`ki-gawm`" in text
    assert "`hong-`" in text and "`kong-`" in text
    assert "`hih`" in text and "`tua`" in text and "`kua`" in text
    assert "`kuamah`" in text and "`bangmah`" in text
    assert "not treated here as independent pronouns" in lower
    assert "prefix/agreement section" in lower
    assert "ka pa" in lower and "na pa" in lower
    assert "case system and relator/postposition structure remain" in lower


def test_pronouns_normalized_print_slice_has_formal_examples_and_source_balance() -> None:
    text = _text()
    example_count = len(re.findall(r"^\(@ex:[^)]+\)", text, re.MULTILINE))
    has_explanation_for_fewer = "Several issues remain outside the present account." in text
    assert example_count >= 6 or has_explanation_for_fewer

    assert re.search(r"\(@ex:[^)]+\)\s+(Genesis|Exodus|Jeremiah)\s+\d+:\d+", text)
    assert (
        re.search(r"\(@ex:[^)]+\)\s+(Matthew|Mark|Luke|John)\s+\d+:\d+", text)
        or "No equally clean Gospel example is currently used" in text
    )


def test_pronouns_normalized_print_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:[^)]+\).*?(?=^\(@ex:|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_pronouns_normalized_print_slice_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_pronouns_normalized_print_slice_avoids_internal_project_terms_and_raw_count_claims() -> None:
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
        "generated report",
    ):
        assert forbidden not in lower_body


def test_pronouns_normalized_print_slice_glosses_key_tedim_forms_in_prose() -> None:
    text = _text()
    expectations = {
        "kei": ("I / me",),
        "nang": ("you",),
        "amah": ("he / she / it",),
        "eite": ("we", "inclusive"),
        "kote": ("we", "exclusive"),
        "note": ("you.PL", "you plural"),
        "amaute": ("they",),
        "kanei": ("I have",),
        "ka-nei": ("1SG-have",),
        "kainn": ("my house",),
        "ka-inn": ("1SG.POSS-house",),
        "na-": ("second-person singular possessive",),
        "a-": ("third-person possessive",),
        "i-": ("first-person plural possessive",),
        "keimah": ("I myself",),
        "nangmah": ("you yourself",),
        "ki-": ("reflexive", "reciprocal", "middle-like"),
        "ki-gawm": ("join together",),
        "hong-": ("participant-oriented",),
        "kong-": ("participant-oriented",),
        "hih": ("this",),
        "tua": ("that",),
        "kua": ("who",),
        "kuamah": ("nobody",),
        "bangmah": ("nothing",),
    }

    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form
