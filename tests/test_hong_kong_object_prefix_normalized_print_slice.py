from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


CANDIDATES_PATH = ROOT / "output/publication_review/candidates_hong_kong_object_prefix.tsv"
DOSSIER_PATH = ROOT / "output/publication_review/dossier_hong_kong_object_prefix_scope.md"
SLICE_PATH = ROOT / "output/publication_review/grammar_hong_kong_object_prefix_print_slice.md"
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_hong_kong_object_prefix.md"
PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"

ALLOWED_DIAGNOSTIC_VALUES = {
    "object_prefix_diagnostic",
    "compatible_not_diagnostic",
    "deictic_venitive_boundary",
    "lexicalized_or_unclear",
    "blocked",
}

ALLOWED_STATUS_VALUES = {
    "accepted",
    "accepted_with_caveat",
    "deferred",
    "blocked",
}

ALLOWED_PRINT_VALUES = {
    "print_ready",
    "print_usable_with_caveat",
    "supporting_candidate",
    "boundary_only",
    "blocked",
}


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _preview_text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_hong_kong_object_prefix_packet_files_exist() -> None:
    assert CANDIDATES_PATH.exists()
    assert DOSSIER_PATH.exists()
    assert SLICE_PATH.exists()
    assert REVIEW_NOTES_PATH.exists()


def test_hong_kong_object_prefix_candidate_tsv_has_required_columns() -> None:
    rows = _rows()
    assert rows

    required_columns = {
        "candidate_id",
        "topic",
        "candidate_form",
        "base_or_parse",
        "construction_type",
        "person_configuration",
        "predicate_type",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "candidate_status",
        "print_status",
        "diagnostic_status",
        "why_selected",
        "caveat",
    }
    assert required_columns.issubset(rows[0].keys())


def test_hong_kong_object_prefix_candidate_tsv_has_no_placeholder_rows() -> None:
    rows = _rows()
    for row in rows:
        assert not row["tedim_text"].startswith("["), row["candidate_id"]
        assert not row["segmentation"].startswith("["), row["candidate_id"]
        assert not row["translation"].startswith("["), row["candidate_id"]


def test_hong_kong_object_prefix_candidate_tsv_covers_core_support_boundary_and_blocked_rows() -> None:
    rows = _rows()
    forms = {row["candidate_form"] for row in rows}
    required = {
        "hongbia",
        "kongpia",
        "kongkoih",
        "hongmu",
        "kongmu",
        "hongzui",
        "hongsawl",
        "hongpai",
        "hongbei",
        "hongsuahna",
        "kongci",
        "konggenkik",
        "hong-an-huan-sak",
        "kong-bawl-sak",
    }
    assert required.issubset(forms)


def test_hong_kong_object_prefix_candidate_tsv_statuses_are_controlled() -> None:
    rows = _rows()
    by_form = {row["candidate_form"]: row for row in rows}
    diagnostic_statuses = {row["diagnostic_status"] for row in rows}
    candidate_statuses = {row["candidate_status"] for row in rows}
    print_statuses = {row["print_status"] for row in rows}

    assert diagnostic_statuses <= ALLOWED_DIAGNOSTIC_VALUES
    assert candidate_statuses <= ALLOWED_STATUS_VALUES
    assert print_statuses <= ALLOWED_PRINT_VALUES

    assert "object_prefix_diagnostic" in diagnostic_statuses
    assert "compatible_not_diagnostic" in diagnostic_statuses
    assert "deictic_venitive_boundary" in diagnostic_statuses
    assert "lexicalized_or_unclear" in diagnostic_statuses
    assert "blocked" in diagnostic_statuses

    assert "accepted" in candidate_statuses
    assert "accepted_with_caveat" in candidate_statuses
    assert "deferred" in candidate_statuses
    assert "blocked" in candidate_statuses

    for form in ("hongbia", "kongpia", "kongkoih"):
        assert by_form[form]["diagnostic_status"] == "object_prefix_diagnostic"
    for form in ("hongmu", "kongmu", "hongzui", "hongsawl"):
        assert by_form[form]["diagnostic_status"] == "compatible_not_diagnostic"
    for form in ("hongpai", "hongbei"):
        assert by_form[form]["diagnostic_status"] == "deictic_venitive_boundary"
    for form in ("hongsuahna", "kongci", "konggenkik"):
        assert by_form[form]["diagnostic_status"] == "lexicalized_or_unclear"


def test_hong_kong_object_prefix_slice_is_grammar_facing() -> None:
    text = _text().lower()

    assert "candidate tsv" not in text
    assert "dossier" not in text
    assert "review notes" not in text
    assert "packet" not in text
    assert "print slice" not in text
    assert "publication-review" not in text
    assert "output/publication_review/" not in text
    assert "scripts/" not in text
    assert "tests/" not in text
    assert "docs/" not in text


def test_hong_kong_object_prefix_slice_has_inventory_table() -> None:
    text = _text()
    assert "Current hong and kong inventory" in text
    assert "| Form | Proposed parse | Source | Current grammar-facing status | Diagnostic status | Boundary issue |" in text


def test_hong_kong_object_prefix_slice_distinguishes_required_categories() -> None:
    text = _text().lower()

    for required in (
        "hong",
        "kong",
        "hongbia",
        "kongpia",
        "kongkoih",
        "hongmu",
        "kongmu",
        "hongpai",
        "hongbei",
        "hongsuahna",
        "kongci",
        "konggenkik",
        "object-prefix_diagnostic",
        "compatible_not_diagnostic",
        "deictic_venitive_boundary",
        "lexicalized_or_unclear",
        "blocked",
        "Safest hong and kong rows",
        "Support but not diagnostic rows",
        "Boundary with deictic / venitive hong",
        "Boundary with lexicalized or unclear rows",
        "Boundary with transitivity, valency, and pronoun/agreement overlap",
        "Deferred material",
        "Summary",
    ):
        assert required.lower() in text


def test_hong_kong_object_prefix_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:hk-[^)]+\).*?(?=^\(@ex:hk-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_hong_kong_object_prefix_slice_examples_have_resolvable_sources() -> None:
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_hong_kong_object_prefix_slice_promoted_examples_come_from_candidate_tsv() -> None:
    rows = _rows()
    candidate_sources = {row["source_reference"] for row in rows if row["candidate_status"] != "blocked"}
    example_sources = {example.source for example in assembler.parse_examples(_text())}

    assert example_sources <= candidate_sources


def test_hong_kong_object_prefix_slice_keeps_deictic_hong_boundary_controlled() -> None:
    rows = _rows()
    boundary_rows = [row for row in rows if row["candidate_form"] in {"hongpai", "hongbei"}]

    assert boundary_rows
    for row in boundary_rows:
        assert row["diagnostic_status"] == "deictic_venitive_boundary"
        assert row["print_status"] == "boundary_only"


def test_hong_kong_object_prefix_slice_does_not_overclaim() -> None:
    lower = _text().lower()

    assert "not a full agreement chapter" in lower
    assert "not a full inverse-system chapter" in lower
    assert "without claiming a full system" in lower
    assert "full person-prefix paradigm" not in lower
    assert "full transitivity chapter" not in lower
    assert "full valency chapter" not in lower
    assert "full deictic-motion system" not in lower
    assert "raw report counts do not decide the analysis" in lower
    assert "motion-heavy rows stay boundary material" in lower


def test_hong_kong_object_prefix_preview_places_section_near_prefix_agreement() -> None:
    preview = _preview_text()

    section_title = "Hong / kong object-prefix or inverse-like"
    assert section_title in preview
    assert preview.index(section_title) > preview.index("Prefix / agreement")
    assert preview.index(section_title) < preview.index("Transitivity")
    assert preview.index(section_title) < preview.index("Directionals")
