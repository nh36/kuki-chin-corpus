from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


CANDIDATES_PATH = ROOT / "output/publication_review/candidates_ki_reflexive_middle.tsv"
DOSSIER_PATH = ROOT / "output/publication_review/dossier_ki_reflexive_middle_scope.md"
SLICE_PATH = ROOT / "output/publication_review/grammar_ki_reflexive_middle_print_slice.md"
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_ki_reflexive_middle.md"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _normalize(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", " ", text.lower()).strip()


def test_ki_reflexive_middle_packet_files_exist() -> None:
    assert CANDIDATES_PATH.exists()
    assert DOSSIER_PATH.exists()
    assert SLICE_PATH.exists()
    assert REVIEW_NOTES_PATH.exists()


def test_ki_reflexive_middle_candidate_tsv_has_required_columns() -> None:
    rows = _rows()
    assert rows

    required_columns = {
        "candidate_id",
        "topic",
        "candidate_form",
        "base_or_parse",
        "construction_type",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "candidate_status",
        "why_selected",
        "caveat",
    }
    assert required_columns.issubset(rows[0].keys())

    for row in rows:
        assert not row["tedim_text"].startswith("[")
        assert not row["segmentation"].startswith("[")
        assert not row["translation"].startswith("[")


def test_ki_reflexive_middle_slice_is_grammar_facing_and_avoids_internal_workflow_prose() -> None:
    text = _text()
    lower = text.lower()

    assert "# Overview of `ki-` reflexive / reciprocal / middle-like marking" in text
    assert "candidate tsv" not in lower
    assert "dossier" not in lower
    assert "review notes" not in lower
    assert "output/publication_review/" not in lower
    assert "scripts/" not in lower
    assert "tests/" not in lower
    assert "docs/" not in lower
    assert " packet " not in f" {lower} "


def test_ki_reflexive_middle_slice_has_inventory_table_and_required_distinctions() -> None:
    text = _text()
    lower = text.lower()

    assert "Current `ki-` inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text

    for required in (
        "reflexive / reciprocal / middle-like",
        "reciprocal",
        "middle or subject-affected",
        "Passive-like or agent-defocused evidence",
        "Lexicalized or frozen `ki-` boundary",
        "Boundary with derivation, VP stacking, transitivity, and prefix/agreement",
        "boundary material",
    ):
        assert required.lower() in lower


def test_ki_reflexive_middle_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:ki-[^)]+\).*?(?=^\(@ex:ki-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_ki_reflexive_middle_slice_examples_have_resolvable_sources() -> None:
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


def test_ki_reflexive_middle_slice_formal_examples_are_candidate_backed() -> None:
    rows = _rows()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    by_source: dict[str, list[str]] = {}
    for row in rows:
        by_source.setdefault(row["source_reference"], []).append(_normalize(row["tedim_text"]))

    assert examples
    for example in examples:
        source = assembler.resolve_example_source(example, bible)
        assert source in by_source, example.label
        tedim_norm = _normalize(example.tedim)
        assert any(
            candidate == tedim_norm or candidate in tedim_norm or tedim_norm in candidate
            for candidate in by_source[source]
        ), example.label


def test_ki_reflexive_middle_promoted_rows_are_used_in_formal_examples() -> None:
    rows = _rows()
    promoted = [
        row
        for row in rows
        if row.get("print_status") in {"print_ready", "print_usable_with_caveat"}
    ]

    bible = load_bible(BIBLE_PATH)
    example_sources = {
        assembler.resolve_example_source(example, bible)
        for example in assembler.parse_examples(_text())
    }

    assert promoted
    for row in promoted:
        assert row["source_reference"] in example_sources


def test_ki_reflexive_middle_slice_keeps_boundaries_visible() -> None:
    text = _text()
    lower = text.lower()

    assert "Lexicalized or frozen `ki-` boundary" in text
    assert "Boundary with derivation, VP stacking, transitivity, and prefix/agreement" in text
    assert "`kipan`" in text
    assert "`ki-phuak`" in text
    assert "`ki-piak-na`" in text
    assert "remain boundary material" in lower


def test_ki_reflexive_middle_slice_keeps_scope_narrow_and_rejects_raw_count_promotion() -> None:
    lower = _text().lower()

    assert "does not claim a full voice chapter" in lower
    assert "a full transitivity chapter" in lower
    assert "a full prefix/agreement chapter" in lower
    assert "a full derivation chapter" in lower
    assert "a full vp-slot template" in lower
    assert "raw report counts are not treated as grammar facts" in lower
