from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


CANDIDATES_PATH = ROOT / "output/publication_review/candidates_verb_paradigms.tsv"
DOSSIER_PATH = ROOT / "output/publication_review/dossier_verb_paradigms_scope.md"
SLICE_PATH = ROOT / "output/publication_review/grammar_verb_paradigms_print_slice.md"
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_verb_paradigms.md"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"

ALLOWED_DIAGNOSTIC_VALUES = {
    "finite_frame_diagnostic",
    "person_marking_diagnostic",
    "paradigm_supporting",
    "tam_boundary",
    "negation_boundary",
    "stem_alternation_boundary",
    "object_prefix_boundary",
    "analyzer_gap_blocked",
    "lexicalized_or_unclear",
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


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _slice_text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _review_notes_text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_verb_paradigm_packet_files_exist() -> None:
    assert CANDIDATES_PATH.exists()
    assert DOSSIER_PATH.exists()
    assert SLICE_PATH.exists()
    assert REVIEW_NOTES_PATH.exists()


def test_verb_paradigm_candidate_tsv_has_required_columns() -> None:
    rows = _rows()
    assert rows

    required_columns = {
        "candidate_id",
        "topic",
        "candidate_form",
        "base_or_parse",
        "predicate_type",
        "person_configuration",
        "tam_negation_profile",
        "stem_form_status",
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


def test_verb_paradigm_candidate_tsv_has_no_placeholder_rows() -> None:
    for row in _rows():
        assert not row["tedim_text"].startswith("["), row["candidate_id"]
        assert not row["segmentation"].startswith("["), row["candidate_id"]
        assert not row["translation"].startswith("["), row["candidate_id"]


def test_verb_paradigm_candidate_tsv_tracks_required_diagnostic_categories() -> None:
    rows = _rows()
    diagnostic_statuses = {row["diagnostic_status"] for row in rows}
    candidate_statuses = {row["candidate_status"] for row in rows}
    print_statuses = {row["print_status"] for row in rows}

    assert diagnostic_statuses <= ALLOWED_DIAGNOSTIC_VALUES
    assert candidate_statuses <= ALLOWED_STATUS_VALUES
    assert print_statuses <= ALLOWED_PRINT_VALUES

    for required in (
        "finite_frame_diagnostic",
        "person_marking_diagnostic",
        "paradigm_supporting",
        "tam_boundary",
        "negation_boundary",
        "stem_alternation_boundary",
        "object_prefix_boundary",
        "analyzer_gap_blocked",
        "lexicalized_or_unclear",
    ):
        assert required in diagnostic_statuses


def test_verb_paradigm_report_rows_are_not_promoted_as_core_grammar_rows() -> None:
    rows = _rows()
    report_rows = [row for row in rows if row["source_zone"] == "Report table"]

    assert report_rows
    for row in report_rows:
        assert row["print_status"] in {"boundary_only", "blocked"}
        assert row["candidate_status"] in {"deferred", "blocked"}


def test_verb_paradigm_slice_is_grammar_facing() -> None:
    lower = _slice_text().lower()

    for forbidden in (
        "candidate tsv",
        "dossier",
        "review notes",
        "packet",
        "print slice",
        "publication-review",
        "output/publication_review/",
        "scripts/",
        "tests/",
        "docs/",
    ):
        assert forbidden not in lower


def test_verb_paradigm_slice_has_compact_inventory_table_and_required_categories() -> None:
    text = _slice_text()
    lower = text.lower()

    assert "Basic finite paradigm inventory" in text
    assert "| Category | Anchor forms | Current status | Why kept narrow |" in text

    for required in (
        "finite-frame anchors",
        "person-marking anchors",
        "tam boundary material",
        "negation boundary material",
        "stem-alternation boundary material",
        "object-prefix boundary material",
        "analyzer-gap or blocked material",
    ):
        assert required in lower


def test_verb_paradigm_slice_examples_keep_source_after_translation() -> None:
    text = _slice_text()
    blocks = re.findall(r"(?ms)^\(@ex:vp-[^)]+\).*?(?=^\(@ex:vp-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_verb_paradigm_slice_examples_have_resolvable_sources() -> None:
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_slice_text())

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_verb_paradigm_slice_promoted_examples_come_from_candidate_layer() -> None:
    rows = _rows()
    promoted_sources = {
        row["source_reference"]
        for row in rows
        if row["print_status"] in {"print_ready", "print_usable_with_caveat", "supporting_candidate"}
    }
    example_sources = {example.source for example in assembler.parse_examples(_slice_text())}

    assert example_sources <= promoted_sources


def test_verb_paradigm_slice_keeps_scope_narrow_and_nonexhaustive() -> None:
    lower = _slice_text().lower()

    assert "not a complete verbal paradigm system" in lower
    assert "not a full tam chapter" in lower
    assert "not a full negation chapter" in lower
    assert "not a full stem-alternation chapter" in lower
    assert "not a full agreement chapter" in lower
    assert "not a full object-prefix chapter" in lower
    assert "not a full transitivity chapter" in lower
    assert "not a full voice chapter" in lower


def test_verb_paradigm_slice_does_not_turn_report_counts_into_grammar_facts() -> None:
    text = _slice_text()
    lower = text.lower()

    assert "raw report counts are not used as grammar facts" in lower
    assert not re.search(r"\b\d{1,3}(?:,\d{3})+\b", text)


def test_verb_paradigm_review_notes_cover_required_human_checks() -> None:
    lower = _review_notes_text().lower()

    for required in (
        "finite predicate frames",
        "person-marking claims",
        "tam, negation, stem alternation, or object-prefix",
        "selected verbs",
        "report-table artifacts",
        "overstate the state of the full paradigm system",
    ):
        assert required in lower
