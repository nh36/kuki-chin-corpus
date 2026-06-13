from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler
import grammar_pdf_quality_gate as gate


SLICE_PATH = ROOT / "output/publication_review/grammar_switch_reference_print_slice.md"
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_switch_reference.tsv"
DIAGNOSTIC_PATH = ROOT / "output/publication_review/switch_reference_source_alignment_diagnostic.md"
VERIFICATION_PATH = ROOT / "output/publication_review/switch_reference_example_verification.md"
PREVIEW_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.md"
TEX_PATH = ROOT / "output/publication_review/assembled_grammar_review_preview.tex"
BIBLE_PATH = ROOT / "bibles" / "extracted" / "ctd" / "ctd-x-bible.txt"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _candidate_rows() -> tuple[list[str], list[dict[str, str]]]:
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def _normalize_example_label(label: str) -> str:
    return label.split("ex:", 1)[-1]


def _tex_example_block(label: str) -> str:
    tex = _text(TEX_PATH)
    tex_label = label if label.startswith("ex:") else f"ex:{label}"
    start = tex.index(f"\\label{{{tex_label}}}")
    block_start = tex.rfind("\\begin{exe}", 0, start)
    block_end = tex.index("\\end{exe}", start) + len("\\end{exe}")
    return tex[block_start:block_end]


def test_switch_reference_packet_files_exist() -> None:
    for path in (
        CANDIDATES_PATH,
        DIAGNOSTIC_PATH,
        VERIFICATION_PATH,
        SLICE_PATH,
        ROOT / "output/publication_review/dossier_switch_reference_scope.md",
        ROOT / "output/publication_review/review_notes_switch_reference.md",
    ):
        assert path.exists(), path


def test_switch_reference_candidate_tsv_has_expected_columns_and_display_decisions() -> None:
    fieldnames, rows = _candidate_rows()
    expected_columns = [
        "candidate_id",
        "topic",
        "candidate_form",
        "construction_type",
        "target_token",
        "nearby_in_tokens",
        "in_token_disambiguation",
        "subject_relation",
        "linked_clause_subject",
        "matrix_or_following_clause_subject",
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
        "caveat",
    ]

    assert fieldnames == expected_columns
    assert rows

    by_id = {row["candidate_id"]: row for row in rows}
    assert set(by_id) == {
        "sr-bawlin-gen11p4",
        "sr-semin-deut10p20",
        "sr-ahih-ciangin-gen1p21",
        "sr-ngenin-gen41p55",
        "sr-ciangin-gen1p3",
        "sr-dingin-gen1p14",
        "sr-abawlmi-ex30p38",
        "sr-omna-gen4p16",
        "sr-muhnaah-gen6p11",
    }

    expectations = {
        "sr-bawlin-gen11p4": ("same_subject", "same_subject_diagnostic", "print_ready", "trimmed_excerpt"),
        "sr-semin-deut10p20": ("same_subject", "same_subject_diagnostic", "print_ready", "full_verse_justified"),
        "sr-ahih-ciangin-gen1p21": ("ambiguous", "switch_reference_like_support", "supporting_candidate", "table_row_only"),
        "sr-ngenin-gen41p55": ("unrecoverable", "blocked_or_unresolved", "blocked", "blocked"),
        "sr-ciangin-gen1p3": ("not_diagnostic", "temporal_subordination_boundary", "boundary_only", "table_row_only"),
        "sr-dingin-gen1p14": ("not_diagnostic", "purposive_boundary", "boundary_only", "table_row_only"),
        "sr-abawlmi-ex30p38": ("not_diagnostic", "relative_clause_boundary", "boundary_only", "table_row_only"),
        "sr-omna-gen4p16": ("not_diagnostic", "nominalization_boundary", "boundary_only", "table_row_only"),
        "sr-muhnaah-gen6p11": ("not_diagnostic", "nominalization_boundary", "boundary_only", "table_row_only"),
    }

    for candidate_id, (subject_relation, diagnostic_status, print_status, display_status) in expectations.items():
        row = by_id[candidate_id]
        assert row["subject_relation"] == subject_relation
        assert row["diagnostic_status"] == diagnostic_status
        assert row["print_status"] == print_status
        assert row["example_display_status"] == display_status
        assert row["source_reference"]
        assert row["target_token"]
        assert row["nearby_in_tokens"] is not None
        assert row["in_token_disambiguation"]
        assert row["candidate_status"]
        assert row["why_selected"]
        assert row["caveat"]
        assert "source unavailable" not in row["source_reference"].lower()
        assert not row["source_reference"].startswith("[")

    bawlin = by_id["sr-bawlin-gen11p4"]
    assert "amaute in" in bawlin["nearby_in_tokens"]
    assert "nadingin" in bawlin["nearby_in_tokens"]
    assert "a dawn in" in bawlin["nearby_in_tokens"]
    assert "lamin" in bawlin["nearby_in_tokens"]
    assert "converb" in bawlin["in_token_disambiguation"].lower()

    semin = by_id["sr-semin-deut10p20"]
    assert "beel-in" in semin["nearby_in_tokens"]
    assert "2SG" in semin["in_token_disambiguation"]
    assert "not a target" in semin["in_token_disambiguation"].lower() or "boundary" in semin["in_token_disambiguation"].lower()

    ahih = by_id["sr-ahih-ciangin-gen1p21"]
    assert "relative marker" in ahih["in_token_disambiguation"].lower()
    assert "table_row_only" in ahih["example_display_status"]

    ngenin = by_id["sr-ngenin-gen41p55"]
    assert "net-IN" in ngenin["in_token_disambiguation"] or "pray-CVB" in ngenin["in_token_disambiguation"]
    assert "blocked" in ngenin["example_display_status"]


def test_switch_reference_example_verification_covers_required_items() -> None:
    text = _text(VERIFICATION_PATH)
    lower = text.lower()

    for required in (
        "Example verification summary",
        "Genesis 11:4",
        "Deuteronomy 10:20",
        "bawlin",
        "semin",
        "ahih ciangin",
        "ngenin",
        "bawl-in",
        "sem-in",
        "beel-in",
        "amaute in",
        "nadingin",
        "a dawn in",
        "lamin",
        "trimmed excerpt",
        "full verse, justified",
        "table row only",
        "same",
        "ambiguous",
        "unrecoverable",
    ):
        assert required in text

    assert "Nearby `-in` tokens and control" in text
    assert "2SG" in text
    assert "boundary material" in lower


def test_switch_reference_diagnostic_discusses_the_report_and_label_decision() -> None:
    text = _text(DIAGNOSTIC_PATH)
    lower = text.lower()

    for required in (
        "What the report claims",
        "same-subject",
        "different-subject",
        "VERB-in",
        "ahih ciangin",
        "ciangin",
        "dingin",
        "relative_clause_boundary",
        "same-subject and different-subject clause linkage",
        "switch-reference",
        "Display note",
        "switch_reference_example_verification.md",
    ):
        assert required in text

    assert "too strong" in lower
    assert "support only" in lower
    assert "demote" in lower
    assert "boundary" in lower
    assert "relative-clause" in lower


def test_switch_reference_print_slice_uses_a_single_clear_section_title_and_compact_examples() -> None:
    text = _text(PREVIEW_PATH)
    lower = text.lower()

    assert text.count("## Same-subject and different-subject clause linkage") == 1
    assert text.count("### Same-subject and different-subject clause linkage") == 0
    assert "Overview of the current evidence" in text
    assert "Current display inventory" in text
    assert "Promoted same-subject evidence" in text
    assert "Support-only and boundary material" in text
    assert "Deferred material" in text
    assert "trimmed excerpt" in lower
    assert "full verse justified" in lower
    assert "bawl-in" in text
    assert "beel-in" in text


def test_switch_reference_formal_examples_resolve_and_keep_sources_after_translation() -> None:
    bible = assembler.load_bible(BIBLE_PATH)
    examples = [
        example
        for example in assembler.parse_examples(_text(PREVIEW_PATH))
        if "sr-" in example.label
    ]
    tex_examples = gate.parse_tex_examples(_text(TEX_PATH))
    by_label = {_normalize_example_label(example.label): example for example in examples}
    tex_examples = {_normalize_example_label(label): glt_line for label, glt_line in tex_examples.items()}

    assert set(by_label) == {"sr-bawlin-gen11p4", "sr-semin-deut10p20"}

    candidate_rows = {row["candidate_id"]: row for row in _candidate_rows()[1]}
    assert candidate_rows["sr-bawlin-gen11p4"]["print_status"] == "print_ready"
    assert candidate_rows["sr-semin-deut10p20"]["print_status"] == "print_ready"

    for label, expected_source in (
        ("sr-bawlin-gen11p4", "Genesis 11:4"),
        ("sr-semin-deut10p20", "Deuteronomy 10:20"),
    ):
        example = by_label[label]
        assert assembler.resolve_example_source(example, bible) == expected_source
        assert tex_examples[label].endswith(f"({expected_source})")
        assert f"({expected_source})" in _tex_example_block(label)


def test_switch_reference_boundary_rows_remain_boundary_controlled() -> None:
    _, rows = _candidate_rows()
    by_id = {row["candidate_id"]: row for row in rows}

    for candidate_id in (
        "sr-ciangin-gen1p3",
        "sr-dingin-gen1p14",
        "sr-abawlmi-ex30p38",
        "sr-omna-gen4p16",
        "sr-muhnaah-gen6p11",
    ):
        row = by_id[candidate_id]
        assert row["print_status"] == "boundary_only"
        assert row["example_display_status"] == "table_row_only"
        assert row["diagnostic_status"].endswith("boundary")
