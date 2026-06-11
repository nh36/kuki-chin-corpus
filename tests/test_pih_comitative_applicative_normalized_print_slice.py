from __future__ import annotations

from pathlib import Path
import csv
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import assemble_publication_review_preview as assembler

from interlinear_latex import load_bible


CANDIDATES_PATH = ROOT / "output/publication_review/candidates_pih_comitative_applicative.tsv"
DOSSIER_PATH = ROOT / "output/publication_review/dossier_pih_comitative_applicative_scope.md"
SLICE_PATH = ROOT / "output/publication_review/grammar_pih_comitative_applicative_print_slice.md"
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_pih_comitative_applicative.md"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _normalize(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", " ", text.lower()).strip()


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_pih_comitative_applicative_packet_files_exist() -> None:
    assert CANDIDATES_PATH.exists()
    assert DOSSIER_PATH.exists()
    assert SLICE_PATH.exists()
    assert REVIEW_NOTES_PATH.exists()


# ---------------------------------------------------------------------------
# Candidate TSV structure
# ---------------------------------------------------------------------------


def test_pih_comitative_applicative_candidate_tsv_has_required_columns() -> None:
    rows = _rows()
    assert rows

    required_columns = {
        "candidate_id",
        "topic",
        "candidate_form",
        "base_or_parse",
        "stem_form",
        "construction_type",
        "source_reference",
        "source_zone",
        "tedim_text",
        "segmentation",
        "gloss",
        "translation",
        "candidate_status",
        "print_status",
        "why_selected",
        "caveat",
    }
    assert required_columns.issubset(rows[0].keys())


def test_pih_comitative_applicative_candidate_tsv_has_no_placeholder_rows() -> None:
    rows = _rows()
    assert rows
    for row in rows:
        assert not row["tedim_text"].startswith("["), row["candidate_id"]
        assert not row["segmentation"].startswith("["), row["candidate_id"]
        assert not row["translation"].startswith("["), row["candidate_id"]


def test_pih_comitative_applicative_candidate_tsv_has_ot_and_gospel_promoted_rows() -> None:
    rows = _rows()
    promoted = [r for r in rows if r.get("print_status") in {"print_ready", "print_usable_with_caveat"}]
    assert promoted

    source_zones = {r["source_zone"] for r in promoted}
    assert "Old Testament" in source_zones, "No Old Testament promoted candidate"
    assert "Gospels" in source_zones, "No Gospel promoted candidate"


def test_pih_comitative_applicative_candidate_tsv_keeps_nominal_pih_as_boundary() -> None:
    rows = _rows()
    nominal_rows = [r for r in rows if "nominal" in r.get("construction_type", "").lower()]
    assert nominal_rows, "Expected at least one nominal -pih boundary row"
    for row in nominal_rows:
        assert row.get("print_status") in {"boundary_only", "blocked"}, (
            f"Nominal -pih row {row['candidate_id']} must not be print_ready"
        )


# ---------------------------------------------------------------------------
# Grammar slice: grammar-facing prose
# ---------------------------------------------------------------------------


def test_pih_comitative_applicative_slice_is_grammar_facing() -> None:
    text = _text()
    lower = text.lower()

    assert "# Overview of verbal `-pih` comitative applicative" in text
    assert "candidate tsv" not in lower
    assert "dossier" not in lower
    assert "review notes" not in lower
    assert "output/publication_review/" not in lower
    assert "scripts/" not in lower
    assert "tests/" not in lower
    assert "docs/" not in lower
    assert " packet " not in f" {lower} "


def test_pih_comitative_applicative_slice_has_inventory_table() -> None:
    text = _text()
    assert "Current `-pih` inventory" in text
    assert "| Form or pattern | Rough function | Example context | Current grammar-facing status | Boundary issue |" in text


def test_pih_comitative_applicative_slice_distinguishes_required_categories() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "comitative applicative",
        "form ii",
        "stem 2",
        "nominal",
        "boundary",
        "boundary with nominal",
        "boundary with directionals",
    ):
        assert required.lower() in lower, f"Expected {required!r} in grammar slice"


def test_pih_comitative_applicative_slice_keeps_nominal_pih_as_boundary() -> None:
    text = _text()
    lower = text.lower()

    assert "nominal" in lower
    # Nominal forms must appear in boundary discussion, not as promoted evidence
    assert "innkuanpihte" in text or "innkuanpih" in text
    assert "mipihte" in text
    assert "boundary" in lower
    # No nominal row promoted in formal examples
    for label in ("@ex:pih-nominal-innkuanpih", "@ex:pih-nominal-mipihte"):
        assert label not in text, f"Nominal row {label!r} must not appear as a formal example"


def test_pih_comitative_applicative_slice_rejects_overclaiming() -> None:
    lower = _text().lower()

    assert "does not claim to solve the full comitative system" in lower or "lies outside the present narrow account" in lower
    assert "full applicative" in lower or "full applicative chapter" in lower or "full applicative typology" in lower
    assert "full valency" in lower or "full valency chapter" in lower
    assert "full derivation" in lower or "full derivational morphology" in lower


def test_pih_comitative_applicative_slice_avoids_raw_report_count_promotion() -> None:
    lower = _text().lower()
    # The slice uses corpus frequencies in the dossier but must not promote raw counts
    # as grammar facts in the slice itself
    assert "raw report counts are not" in lower or "frequencies do not convert directly" in lower or "individual frequencies do not convert" in lower


# ---------------------------------------------------------------------------
# Formal examples: source references, resolution, and candidate backing
# ---------------------------------------------------------------------------


def test_pih_comitative_applicative_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:pih-[^)]+\).*?(?=^\(@ex:pih-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), (
            f"Example block missing source-after-translation:\n{block[:300]}"
        )


def test_pih_comitative_applicative_slice_examples_have_resolvable_sources() -> None:
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, f"Example {example.label} source not resolved"


def test_pih_comitative_applicative_slice_formal_examples_are_candidate_backed() -> None:
    rows = _rows()
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    by_source: dict[str, list[str]] = {}
    for row in rows:
        by_source.setdefault(row["source_reference"], []).append(_normalize(row["tedim_text"]))

    assert examples
    for example in examples:
        source = assembler.resolve_example_source(example, bible)
        assert source in by_source, (
            f"Example {example.label} source {source!r} not found in candidate TSV"
        )
        tedim_norm = _normalize(example.tedim)
        assert any(
            candidate == tedim_norm or candidate in tedim_norm or tedim_norm in candidate
            for candidate in by_source[source]
        ), f"Example {example.label} Tedim text not matched in candidate TSV for source {source!r}"


def test_pih_comitative_applicative_promoted_rows_are_used_in_formal_examples() -> None:
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
        assert row["source_reference"] in example_sources, (
            f"Promoted candidate {row['candidate_id']} source {row['source_reference']!r} "
            f"not used in any formal example"
        )
