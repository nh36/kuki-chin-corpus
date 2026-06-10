from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


SLICE_PATH = ROOT / "output/publication_review/grammar_clause_linkage_print_slice.md"
SUPPLEMENT_PATH = ROOT / "output/publication_review/examples_clause_linkage_normalization.tsv"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _rows() -> list[dict[str, str]]:
    with SUPPLEMENT_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


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


def test_clause_linkage_normalized_print_slice_exists() -> None:
    assert SLICE_PATH.exists()


def test_clause_linkage_normalized_print_slice_has_required_tiered_structure() -> None:
    text = _text()

    for required in (
        "# Overview of clause linkage in this section",
        "# Core temporal subordination: ciangin",
        "# Purposive or clause-bound irrealis boundary: dingin",
        "# Same-subject converb linkage boundary: VERB-in and ngenin",
        "# Different-subject temporal linkage boundary: ahih ciangin",
        "# Prenominal relative-clause boundary: a bawl mi",
        "# Nominalized relative and clause-like form boundary: omna",
        "# Nominalization-plus-case boundary: muhna-ah",
        "# Deferred and boundary material",
    ):
        assert required in text

    assert "switch-reference" in text.lower()
    assert "relative-clause" in text.lower()
    assert "broader report-inventory rows" in text
    assert "Raw occurrence counts are not treated as grammar facts" in text


def test_clause_linkage_normalized_print_slice_avoids_stale_workflow_language() -> None:
    lower = _text().lower()
    for forbidden in (
        "candidate tsv",
        "dossier",
        "review notes",
        "packet complete",
        "this packet is now complete",
        "ready for human review",
        "dictionary and review-note slices have not yet begun",
    ):
        assert forbidden not in lower


def test_clause_linkage_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:clause-[^)]+\).*?(?=^\(@ex:clause-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(
            r"^d\. Translation: .+\((?:Genesis|Exodus|Judges|Matthew|Mark|Luke|John)\s+\d+:\d+\)$",
            block,
            re.MULTILINE,
        ), block


def test_clause_linkage_examples_have_resolvable_sources() -> None:
    text = _text()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(text)

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_clause_linkage_genesis_1_26_is_not_used_as_print_ready_example() -> None:
    text = _text()
    rows = _rows()

    assert "(@ex:clause-ciangin-gen1p26)" not in text
    assert not any(
        row.get("source_reference") == "Genesis 1:26"
        and row.get("print_status") in {"print_ready", "print_usable_with_caveat"}
        for row in rows
    )


def test_clause_linkage_running_prose_glosses_key_forms() -> None:
    text = _text()
    expectations = {
        "ciangin": ("when", "temporal subordination"),
        "dingin": ("in order to", "purpose"),
        "ngenin": ("pray-CVB",),
        "ahih ciangin": ("when",),
        "a bawl mi": ("person who",),
        "muhna-ah": ("in seeing", "in the sight"),
    }
    for form, glosses in expectations.items():
        assert _first_prose_occurrence_has_gloss(text, form, glosses), form


def test_clause_linkage_normalization_supplement_has_expected_columns() -> None:
    assert SUPPLEMENT_PATH.exists()
    rows = _rows()

    assert rows
    for column in (
        "example_id",
        "clause_linkage_topic",
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
        assert column in rows[0]


def test_clause_linkage_normalization_supplement_has_no_placeholder_rows() -> None:
    rows = _rows()
    assert rows

    for row in rows:
        tedim = row.get("tedim_text", "")
        seg = row.get("segmentation", "")
        trans = row.get("translation", "")
        assert not tedim.startswith("[")
        assert not seg.startswith("[")
        assert "[Gospel example" not in tedim
        assert "[Gospel example" not in seg
        assert "[Gospel translation]" not in trans


def test_clause_linkage_candidate_form_alignment_for_core_rows() -> None:
    rows = _rows()
    assert rows

    core_forms = {"ciangin", "dingin", "ngenin", "ahih ciangin", "a bawl mi", "muhna-ah"}
    promoted_statuses = {"print_ready", "print_usable_with_caveat"}

    for row in rows:
        candidate_form = row.get("candidate_form", "").strip().lower()
        if candidate_form not in core_forms or row.get("print_status") not in promoted_statuses:
            continue

        tedim = re.sub(r"[*_]+", "", row.get("tedim_text", "").lower())
        tedim = re.sub(r"\s+", " ", tedim).strip()

        if candidate_form == "ahih ciangin":
            assert "ahih ciangin" in tedim
        elif candidate_form == "a bawl mi":
            assert "a bawl mi" in tedim
        else:
            assert candidate_form in tedim, f"{row['example_id']} missing {candidate_form}: {tedim}"


def test_clause_linkage_abawlmi_rows_match_labeled_construction() -> None:
    rows = _rows()
    for row in rows:
        if row.get("candidate_form", "").strip().lower() != "a bawl mi":
            continue
        tedim = re.sub(r"[*_]+", "", row.get("tedim_text", "").lower())
        assert "a bawl mi" in tedim


def test_clause_linkage_remains_boundary_controlled_not_full_system() -> None:
    text = _text().lower()
    assert "full switch-reference chapter" not in text
    assert "full relative-clause chapter" not in text
    assert "full complex-sentence chapter" not in text

    deferred = text.split("# deferred and boundary material", 1)[-1]
    for required in ("switch-reference", "relative-clause", "discourse"):
        assert required in deferred
