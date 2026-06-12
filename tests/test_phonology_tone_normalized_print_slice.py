from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_REVIEW_DIR = ROOT / "output" / "publication_review"

CANDIDATES_PATH = PUBLICATION_REVIEW_DIR / "candidates_phonology_tone.tsv"
DOSSIER_PATH = PUBLICATION_REVIEW_DIR / "dossier_phonology_tone_scope.md"
SLICE_PATH = PUBLICATION_REVIEW_DIR / "grammar_phonology_tone_print_slice.md"
REVIEW_NOTES_PATH = PUBLICATION_REVIEW_DIR / "review_notes_phonology_tone.md"
DIAGNOSTIC_PATH = PUBLICATION_REVIEW_DIR / "phonology_tone_source_alignment_diagnostic.md"

ALLOWED_CANDIDATE_STATUSES = {"accepted", "accepted_with_caveat", "deferred", "blocked"}
ALLOWED_PRINT_STATUSES = {"print_ready", "print_usable_with_caveat", "boundary_only", "blocked"}
ALLOWED_DIAGNOSTIC_STATUSES = {
    "segment_inventory_support",
    "orthography_support",
    "phonotactic_support",
    "tone_literature_support",
    "tone_boundary",
    "a_tone_blocked",
    "morphophonology_boundary",
    "analyzer_gap_blocked",
    "unresolved_or_conflicting",
}


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_phonology_tone_packet_files_exist() -> None:
    for path in (CANDIDATES_PATH, DOSSIER_PATH, SLICE_PATH, REVIEW_NOTES_PATH, DIAGNOSTIC_PATH):
        assert path.exists(), f"Missing expected file: {path.name}"


def test_phonology_tone_candidate_tsv_has_required_columns_and_statuses() -> None:
    rows = _rows()
    assert rows

    required_columns = {
        "candidate_id",
        "topic",
        "candidate_form",
        "evidence_type",
        "source_reference",
        "source_zone",
        "orthographic_form",
        "phonological_claim",
        "tone_claim",
        "morphophonological_context",
        "candidate_status",
        "print_status",
        "diagnostic_status",
        "why_selected",
        "caveat",
    }
    assert required_columns.issubset(rows[0].keys())

    evidence_types = {row["evidence_type"] for row in rows}
    assert {"literature_backed", "orthography_backed", "analyzer_gap", "unresolved"}.issubset(evidence_types)

    candidate_statuses = {row["candidate_status"] for row in rows}
    print_statuses = {row["print_status"] for row in rows}
    diagnostic_statuses = {row["diagnostic_status"] for row in rows}

    assert candidate_statuses <= ALLOWED_CANDIDATE_STATUSES
    assert print_statuses <= ALLOWED_PRINT_STATUSES
    assert diagnostic_statuses <= ALLOWED_DIAGNOSTIC_STATUSES

    assert any(row["candidate_status"] == "blocked" for row in rows)
    assert any(row["print_status"] == "blocked" for row in rows)


def test_phonology_tone_candidate_tsv_covers_required_categories() -> None:
    rows = _rows()
    forms = {row["candidate_form"] for row in rows}
    required_forms = {
        "consonant inventory",
        "vowel inventory",
        "syllable shape",
        "practical orthography",
        "three-tone system",
        "grammatical tone",
        "-a",
        "tone sandhi",
        "Form I / Form II",
        "TAM / aspect / modal",
        "-pih",
        "verb paradigms",
    }
    assert required_forms.issubset(forms)

    for row in rows:
        for field in ("candidate_id", "topic", "candidate_form", "why_selected", "caveat"):
            value = row[field].strip()
            assert value
            assert not value.startswith("[")
            assert "TBD" not in value
            assert "TODO" not in value


def test_phonology_tone_candidate_tsv_has_no_placeholder_rows() -> None:
    rows = _rows()
    assert rows

    for row in rows:
        for field, raw_value in row.items():
            value = raw_value.strip()
            assert value
            assert not value.startswith("[")
            assert "TBD" not in value
            assert "TODO" not in value


def test_phonology_tone_diagnostic_discusses_required_topics_and_decision() -> None:
    text = _text(DIAGNOSTIC_PATH).lower()

    for required in (
        "segmental phonology",
        "tone",
        "-a",
        "orthography",
        "analyzer-gap",
        "stem alternation",
        "tam",
        "-pih",
        "verb paradigms",
        "safe to print now",
        "blocked",
        "literature-only wording",
    ):
        assert required in text, required


def test_phonology_tone_slice_is_grammar_facing_and_table_driven() -> None:
    text = _text(SLICE_PATH)
    lower = text.lower()

    for forbidden in ("candidate tsv", "dossier", "packet", "review notes", "output/publication_review/", "scripts/", "docs/"):
        assert forbidden not in lower

    for required in (
        "Overview of phonology and tone in Tedim",
        "Orientation table",
        "Segmental phonology",
        "Orthography and syllable shape",
        "Tone status",
        "The blocked -a issue",
        "Boundaries with stem alternation, TAM, `-pih`, and verb paradigms",
        "Deferred material",
        "What can be printed now",
    ):
        assert required in text

    assert "| Area | Conservative claim | Evidence status | Caveat |" in text
    assert "analyzer-gap" not in lower
    assert "a full phoneme table, a full tone-sandhi account, and a complete tone analysis remain deferred." in lower
    assert "blocked -a warning" in lower
    assert "-pih" in text and "with / accompanying" in text


def test_phonology_tone_slice_includes_minimal_formal_tone_example() -> None:
    text = _text(SLICE_PATH)
    assert re.findall(r"(?m)^\(@ex:[^)]+\)", text)
    assert "(@ex:phon-tone-triplet) source unavailable" in text
    assert "minimal three-tone contrast" in text


def test_phonology_tone_review_notes_cover_human_checkpoints() -> None:
    text = _text(REVIEW_NOTES_PATH).lower()

    for required in (
        "consonant and vowel claims",
        "orthography",
        "three-tone summary",
        "blocked `-a` issue",
        "analyzer-gap cautions",
        "phoneme table",
        "orientation section",
    ):
        assert required in text
