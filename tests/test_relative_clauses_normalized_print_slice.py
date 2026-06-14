from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler
import grammar_pdf_quality_gate as gate


OUTPUT_DIR = ROOT / "output" / "publication_review"
CANDIDATES_PATH = OUTPUT_DIR / "candidates_relative_clauses.tsv"
DIAGNOSTIC_PATH = OUTPUT_DIR / "relative_clauses_source_alignment_diagnostic.md"
DOSSIER_PATH = OUTPUT_DIR / "dossier_relative_clauses_scope.md"
SLICE_PATH = OUTPUT_DIR / "grammar_relative_clauses_print_slice.md"
REVIEW_NOTES_PATH = OUTPUT_DIR / "review_notes_relative_clauses.md"
VERIFICATION_PATH = OUTPUT_DIR / "relative_clauses_example_verification.md"
PREVIEW_PATH = OUTPUT_DIR / "assembled_grammar_review_preview.md"
TEX_PATH = OUTPUT_DIR / "assembled_grammar_review_preview.tex"
BIBLE_PATH = ROOT / "bibles" / "extracted" / "ctd" / "ctd-x-bible.txt"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _candidate_rows() -> tuple[list[str], list[dict[str, str]]]:
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def _normalize_label(label: str) -> str:
    return label.split("ex:", 1)[-1]


def _tex_example_block(label: str) -> str:
    tex = _text(TEX_PATH)
    tex_label = label if label.startswith("ex:") else f"ex:{label}"
    start = tex.index(f"\\label{{{tex_label}}}")
    block_start = tex.rfind("\\begin{exe}", 0, start)
    block_end = tex.index("\\end{exe}", start) + len("\\end{exe}")
    return tex[block_start:block_end]


def test_relative_clauses_packet_files_exist() -> None:
    for path in (
        CANDIDATES_PATH,
        DIAGNOSTIC_PATH,
        DOSSIER_PATH,
        SLICE_PATH,
        REVIEW_NOTES_PATH,
        VERIFICATION_PATH,
        PREVIEW_PATH,
        TEX_PATH,
    ):
        assert path.exists(), path


def test_relative_clauses_candidate_tsv_has_expected_schema_and_rows() -> None:
    fieldnames, rows = _candidate_rows()
    expected_columns = [
        "candidate_id",
        "topic",
        "candidate_form",
        "construction_type",
        "head_or_head_like_element",
        "relative_clause_span",
        "target_span",
        "mi_status",
        "head_role",
        "head_role_verification",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "candidate_status",
        "print_status",
        "example_display_status",
        "diagnostic_status",
        "why_selected",
        "boundary_reason",
        "caveat",
    ]

    assert fieldnames == expected_columns
    assert rows

    by_id = {row["candidate_id"]: row for row in rows}
    expected_ids = {
        "rc-abawlmi-ex30p38",
        "rc-omte-gen2p1",
        "rc-omna-gen4p16",
        "rc-muhnaah-gen6p11",
        "rc-aomlai-report",
        "rc-agenthu-report",
        "rc-ciangin-gen1p3",
        "rc-dingin-gen1p14",
        "rc-bawlin-gen11p4",
        "rc-semin-deut10p20",
        "rc-ahihciangin-gen1p21",
    }
    assert set(by_id) == expected_ids

    expectations = {
        "rc-abawlmi-ex30p38": ("accepted", "print_ready", "formal_example", "mi_headed_relative_like_diagnostic"),
        "rc-omte-gen2p1": ("accepted_with_caveat", "supporting_candidate", "supporting_example", "headless_relative_support"),
        "rc-omna-gen4p16": ("accepted_with_caveat", "boundary_only", "boundary_row", "nominalization_boundary"),
        "rc-muhnaah-gen6p11": ("accepted_with_caveat", "boundary_only", "boundary_row", "case_marked_nominalization_boundary"),
        "rc-aomlai-report": ("needs_review", "report_only", "report_only", "relative_like_support"),
        "rc-agenthu-report": ("needs_review", "report_only", "report_only", "relative_like_support"),
        "rc-ciangin-gen1p3": ("deferred", "boundary_only", "boundary_row", "ordinary_subordination_boundary"),
        "rc-dingin-gen1p14": ("deferred", "boundary_only", "boundary_row", "ordinary_subordination_boundary"),
        "rc-bawlin-gen11p4": ("deferred", "boundary_only", "boundary_row", "clause_linkage_boundary"),
        "rc-semin-deut10p20": ("deferred", "boundary_only", "boundary_row", "clause_linkage_boundary"),
        "rc-ahihciangin-gen1p21": ("deferred", "boundary_only", "boundary_row", "clause_linkage_boundary"),
    }

    for candidate_id, (candidate_status, print_status, display_status, diagnostic_status) in expectations.items():
        row = by_id[candidate_id]
        assert row["candidate_status"] == candidate_status
        assert row["print_status"] == print_status
        assert row["example_display_status"] == display_status
        assert row["diagnostic_status"] == diagnostic_status
        assert row["source_reference"]
        assert row["why_selected"]
        assert row["caveat"]

    assert by_id["rc-abawlmi-ex30p38"]["head_or_head_like_element"] == "mi (person head noun)"
    assert by_id["rc-abawlmi-ex30p38"]["relative_clause_span"] == "a bawl"
    assert by_id["rc-abawlmi-ex30p38"]["target_span"] == "a bawl"
    assert by_id["rc-abawlmi-ex30p38"]["mi_status"] == "head_noun"
    assert by_id["rc-abawlmi-ex30p38"]["head_role_verification"] == "subject_verified"
    assert by_id["rc-omte-gen2p1"]["head_or_head_like_element"] == "none (headless/free)"
    assert by_id["rc-omte-gen2p1"]["relative_clause_span"] == "om-te"
    assert by_id["rc-omte-gen2p1"]["target_span"] == "om-te"
    assert by_id["rc-omte-gen2p1"]["mi_status"] == "not_applicable"
    assert by_id["rc-omte-gen2p1"]["head_role_verification"] == "headless_or_free_ambiguous"
    assert by_id["rc-omna-gen4p16"]["relative_clause_span"] == "om-na"
    assert by_id["rc-omna-gen4p16"]["target_span"] == "om-na"
    assert by_id["rc-omna-gen4p16"]["mi_status"] == "not_applicable"
    assert by_id["rc-omna-gen4p16"]["head_role_verification"] == "nominalized_frame"
    assert by_id["rc-omna-gen4p16"]["boundary_reason"] == "nominalization overlap"
    assert by_id["rc-muhnaah-gen6p11"]["relative_clause_span"] == "muh-na-ah"
    assert by_id["rc-muhnaah-gen6p11"]["target_span"] == "muh-na-ah"
    assert by_id["rc-muhnaah-gen6p11"]["mi_status"] == "not_applicable"
    assert by_id["rc-muhnaah-gen6p11"]["head_role_verification"] == "case_marked_nominalized_frame"
    assert by_id["rc-muhnaah-gen6p11"]["boundary_reason"] == "nominalization + case overlap"
    assert by_id["rc-omte-gen2p1"]["boundary_reason"] == "headless/free relative vs plural nominalization ambiguity"
    assert by_id["rc-aomlai-report"]["boundary_reason"] == "source unresolved"
    assert by_id["rc-ciangin-gen1p3"]["boundary_reason"] == "ordinary temporal subordination"
    assert by_id["rc-dingin-gen1p14"]["boundary_reason"] == "purposive / clause-bound irrealis"
    assert by_id["rc-ciangin-gen1p3"]["source_zone"] == "Old Testament"
    assert by_id["rc-aomlai-report"]["source_zone"] == "report"


def test_relative_clauses_diagnostic_covers_report_and_label_decision() -> None:
    text = _text(DIAGNOSTIC_PATH)
    lower = text.lower()

    for required in (
        "docs/grammar/reports/08-clause-03-relatives.md",
        "a bawl mi",
        "omte",
        "a om lai",
        "a gen thu",
        "omna",
        "muhna-ah",
        "ciangin",
        "dingin",
        "bawlin",
        "semin",
        "ahih ciangin",
        "Safest print-facing label",
        "`mi`-headed and nominalized relative-like constructions",
    ):
        assert required in text

    for required in (
        "nominalization",
        "case-marked nominalization",
        "ordinary subordination",
        "clause-linkage",
        "boundary",
        "full relative-clause system",
        "full nominalization system",
        "full np structure",
        "full case system",
        "full subordination chapter",
        "full discourse system",
    ):
        assert required in lower


def test_relative_clauses_example_verification_exists_and_covers_key_examples() -> None:
    text = _text(VERIFICATION_PATH)
    lower = text.lower()

    for required in (
        "a bawl mi",
        "omte",
        "omna",
        "muhna-ah",
    ):
        assert required in text

    for required_lower in (
        "exodus 30:38",
        "genesis 2:1",
        "genesis 4:16",
        "genesis 6:11",
        "status of",
        "head or head-like element",
        "recommendation",
        "remain promoted",
        "remain supporting",
        "remain boundary",
        "promoted diagnostic",
        "supporting evidence",
        "nominalization boundary",
        "case-marked nominalization boundary",
    ):
        assert required_lower in lower

def test_relative_clauses_dossier_and_review_notes_record_scope() -> None:
    dossier = _text(DOSSIER_PATH)
    notes = _text(REVIEW_NOTES_PATH)

    for required in (
        "`mi`-headed and nominalized relative-like constructions",
        "a bawl mi",
        "omte",
        "omna",
        "muhna-ah",
        "a om lai",
        "a gen thu",
        "ciangin",
        "dingin",
        "bawlin",
        "semin",
        "ahih ciangin",
    ):
        assert required in dossier
        assert required in notes or required in dossier


def test_relative_clauses_print_slice_has_required_structure_and_boundaries() -> None:
    text = _text(SLICE_PATH)
    lower = text.lower()

    for required in (
        "`mi`-headed and nominalized relative-like constructions",
        "# Overview",
        "# Relative-like inventory",
        "# `mi`-headed relatives",
        "# Plural relative-like support",
        "# Nominalization boundary",
        "# Case-marked nominalization boundary",
        "# Ordinary subordination and clause-linkage boundary",
        "# Deferred material",
        "# Summary",
        "No equally clean Gospel example is currently used for this construction",
        "No equally clean Gospel example is currently used here",
        "a bawl mi",
        "omte",
        "omna",
        "muhna-ah",
        "ciangin",
        "dingin",
        "bawlin",
        "semin",
        "ahih ciangin",
        "a om lai",
        "a gen thu",
    ):
        assert required in text

    for forbidden in (
        "full relative-clause system",
        "full nominalization system",
        "full np structure chapter",
        "full case system",
        "full subordination chapter",
        "full discourse system",
    ):
        assert forbidden not in lower


def test_relative_clauses_formal_examples_are_source_resolved_and_use_same_source_mechanism() -> None:
    bible = assembler.load_bible(BIBLE_PATH)
    preview_text = _text(PREVIEW_PATH)
    tex_text = _text(TEX_PATH)
    tex_examples = {
        _normalize_label(label): glt_line
        for label, glt_line in gate.parse_tex_examples(tex_text).items()
    }
    examples = {
        _normalize_label(example.label): example
        for example in assembler.parse_examples(preview_text)
        if _normalize_label(example.label).startswith("rc-")
    }
    candidate_rows = {row["candidate_form"]: row for row in _candidate_rows()[1]}

    assert set(examples) == {"rc-abawlmi-ex30", "rc-omte-gen2"}

    expected = {
        "rc-abawlmi-ex30": ("a bawl mi", "Exodus 30:38"),
        "rc-omte-gen2": ("omte", "Genesis 2:1"),
    }

    for label, (candidate_form, expected_source) in expected.items():
        example = examples[label]
        assert assembler.resolve_example_source(example, bible) == expected_source
        assert f"({expected_source})" in tex_examples[label]
        assert f"({expected_source})" in _tex_example_block(label)
        assert candidate_rows[candidate_form]["source_reference"] == expected_source
        assert candidate_rows[candidate_form]["print_status"] in {"print_ready", "supporting_candidate"}


def test_relative_clauses_boundary_rows_remain_boundary_controlled() -> None:
    _, rows = _candidate_rows()
    by_id = {row["candidate_id"]: row for row in rows}

    for candidate_id in (
        "rc-omna-gen4p16",
        "rc-muhnaah-gen6p11",
        "rc-ciangin-gen1p3",
        "rc-dingin-gen1p14",
        "rc-bawlin-gen11p4",
        "rc-semin-deut10p20",
        "rc-ahihciangin-gen1p21",
    ):
        assert by_id[candidate_id]["print_status"] == "boundary_only"
        assert by_id[candidate_id]["candidate_status"] in {"deferred", "accepted_with_caveat"}

    for candidate_id in ("rc-aomlai-report", "rc-agenthu-report"):
        assert by_id[candidate_id]["print_status"] == "report_only"
        assert by_id[candidate_id]["candidate_status"] == "needs_review"

    preview = _text(PREVIEW_PATH)
    for forbidden in (
        "(@ex:rc-aomlai-report)",
        "(@ex:rc-agenthu-report)",
        "(@ex:rc-ciangin-gen1p3)",
        "(@ex:rc-dingin-gen1p14)",
        "(@ex:rc-bawlin-gen11p4)",
        "(@ex:rc-semin-deut10p20)",
        "(@ex:rc-ahihciangin-gen1p21)",
    ):
        assert forbidden not in preview


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
