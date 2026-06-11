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
DIAGNOSTIC_PATH = ROOT / "output/publication_review/pih_stem_alternation_diagnostic.md"
BIBLE_PATH = ROOT / "bibles/extracted/ctd/ctd-x-bible.txt"

ALLOWED_STEM_DIAGNOSTIC_VALUES = {
    "diagnostic_form_ii",
    "compatible_not_diagnostic",
    "literature_backed",
    "morphophonological_boundary",
    "lexicalized_or_unclear",
    "blocked",
}


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def _diagnostic_text() -> str:
    return DIAGNOSTIC_PATH.read_text(encoding="utf-8")


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _normalize(text: str) -> str:
    return re.sub(r"[^0-9a-z]+", " ", text.lower()).strip()


def test_pih_comitative_applicative_packet_files_exist() -> None:
    assert CANDIDATES_PATH.exists()
    assert DOSSIER_PATH.exists()
    assert SLICE_PATH.exists()
    assert REVIEW_NOTES_PATH.exists()
    assert DIAGNOSTIC_PATH.exists()


def test_pih_stem_diagnostic_discusses_required_topics_and_forms() -> None:
    text = _diagnostic_text().lower()

    for required in (
        "form ii",
        "stem 2",
        "paipih",
        "pai / paih",
        "nekpih",
        "tunpih",
        "hopih",
        "hehpih",
        "ompih",
        "paikhiatpih",
    ):
        assert required in text, required


def test_pih_stem_diagnostic_gives_a_decision_not_only_uncertainty() -> None:
    text = _diagnostic_text().lower()

    assert "best-supported decision" in text or "best current conclusion" in text or "decision for grammar-facing phrasing" in text
    assert "stem 2 selection is the best-supported analysis" in text or "best treated as a stem 2 / form ii selecting suffix" in text
    assert "paipih" in text and ("morphophonological" in text or "compatible" in text)


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
        "stem_diagnostic_status",
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


def test_pih_comitative_applicative_candidate_tsv_covers_required_forms() -> None:
    forms = {row["candidate_form"] for row in _rows()}
    required = {"paipih", "nekpih", "tunpih", "hopih", "hehpih", "ompih", "paikhiatpih"}
    assert required.issubset(forms)


def test_pih_comitative_applicative_candidate_tsv_has_stem_diagnostic_statuses() -> None:
    rows = _rows()
    statuses = {row["stem_diagnostic_status"] for row in rows}

    assert statuses <= ALLOWED_STEM_DIAGNOSTIC_VALUES
    assert "diagnostic_form_ii" in statuses
    assert "morphophonological_boundary" in statuses
    assert "compatible_not_diagnostic" in statuses
    assert "blocked" in statuses


def test_pih_comitative_applicative_candidate_tsv_keeps_nominal_pih_as_boundary() -> None:
    rows = _rows()
    nominal_rows = [r for r in rows if "nominal" in r.get("construction_type", "").lower()]
    assert nominal_rows, "Expected at least one nominal -pih boundary row"
    for row in nominal_rows:
        assert row.get("print_status") in {"boundary_only", "blocked"}, (
            f"Nominal -pih row {row['candidate_id']} must not be print-ready"
        )
        assert row.get("stem_diagnostic_status") == "blocked"


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
        "Boundary with nominal",
        "Boundary with directionals",
    ):
        assert required.lower() in lower


def test_pih_comitative_applicative_slice_reflects_diagnostic_conclusion() -> None:
    text = _text().lower()

    assert "stem 2 selecting" in text or "form ii restriction" in text
    assert "diagnostic row" in text and "nekpih" in text
    assert "morphophonological-boundary" in text and "paipih" in text
    assert "compatible but not independently diagnostic" in text or "compatible but not diagnostic" in text


def test_pih_comitative_applicative_slice_does_not_claim_corpus_alone_proves_form_ii_rule() -> None:
    lower = _text().lower()
    assert "corpus alone does not prove" in lower or "corpus alone does not" in lower


def test_pih_comitative_applicative_slice_does_not_treat_paipih_as_unproblematic() -> None:
    lower = _text().lower()
    assert "paipih" in lower
    assert "pai / paih" in lower
    assert "morphophonological" in lower


def test_pih_comitative_applicative_slice_dingin_glossing_is_harmonized() -> None:
    text = _text()
    lower = text.lower()

    assert "ding-in" in text
    assert "IRR-ERG" in text
    assert "NMLZ-ERG" not in text
    assert "clause-bound irrealis" in lower or "purposive" in lower


def test_pih_comitative_applicative_slice_keeps_nominal_pih_as_boundary() -> None:
    text = _text()
    lower = text.lower()

    assert "nominal" in lower
    assert "innkuanpihte" in text or "innkuanpih" in text
    assert "mipihte" in text
    for label in ("@ex:pih-nominal-innkuanpih", "@ex:pih-nominal-mipihte"):
        assert label not in text


def test_pih_comitative_applicative_slice_rejects_overclaiming() -> None:
    lower = _text().lower()

    assert "full applicative" in lower
    assert "full valency" in lower
    assert "full derivational morphology" in lower or "full derivation" in lower
    assert "full vp-slot template" in lower
    assert "complete comitative system" in lower


def test_pih_comitative_applicative_slice_avoids_raw_report_count_promotion() -> None:
    lower = _text().lower()
    assert "frequencies do not convert directly" in lower or "individual frequencies do not convert" in lower or "raw report counts are not" in lower


def test_pih_comitative_applicative_slice_examples_keep_source_after_translation() -> None:
    text = _text()
    blocks = re.findall(r"(?ms)^\(@ex:pih-[^)]+\).*?(?=^\(@ex:pih-|\Z)", text)

    assert blocks
    for block in blocks:
        assert re.search(r"^d\. Translation: .+\([^)]+\d+:\d+\)$", block, re.MULTILINE), block


def test_pih_comitative_applicative_slice_examples_have_resolvable_sources() -> None:
    bible = load_bible(BIBLE_PATH)
    examples = assembler.parse_examples(_text())

    assert examples
    for example in examples:
        resolved = assembler.resolve_example_source(example, bible)
        assert resolved, example.label


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
        assert source in by_source, example.label
        tedim_norm = _normalize(example.tedim)
        assert any(
            candidate == tedim_norm or candidate in tedim_norm or tedim_norm in candidate
            for candidate in by_source[source]
        ), example.label


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
        assert row["source_reference"] in example_sources

