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

BIBLE_REFERENCE_RE = re.compile(
    r"\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|"
    r"1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Songs|Isaiah|"
    r"Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|"
    r"Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1 Corinthians|2 Corinthians|Galatians|"
    r"Ephesians|Philippians|Colossians|1 Thessalonians|2 Thessalonians|1 Timothy|2 Timothy|Titus|Philemon|"
    r"Hebrews|James|1 Peter|2 Peter|1 John|2 John|3 John|Jude|Revelation)\s+\d+:\d+\b"
)


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
    assert {
        "literature_backed_tone_claim",
        "bible_attested_example",
        "bible_attested_minimal_pair",
        "near_minimal_pair",
        "orthography_support",
        "analyzer_gap_blocked",
        "unresolved_or_conflicting",
    }.issubset(evidence_types)

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
        "hi / hi",
        "thei / -thei",
        "ta / -ta",
        "-a",
        "tone sandhi",
        "Form I / Form II",
        "TAM / aspect / modal",
        "-pih",
        "verb paradigms",
    }
    assert required_forms.issubset(forms)


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


def test_phonology_tone_candidate_tsv_distinguishes_bible_attested_and_literature_only_claims() -> None:
    rows = _rows()
    bible_rows = [
        row
        for row in rows
        if row["evidence_type"] in {"bible_attested_example", "bible_attested_minimal_pair", "near_minimal_pair"}
    ]
    assert len(bible_rows) >= 2
    assert all(BIBLE_REFERENCE_RE.search(row["source_reference"]) for row in bible_rows)
    assert any(row["evidence_type"] == "literature_backed_tone_claim" for row in rows)


def test_phonology_tone_no_print_facing_source_unavailable_or_question_mark_glosses() -> None:
    rows = _rows()
    print_rows = [row for row in rows if row["print_status"] in {"print_ready", "print_usable_with_caveat"}]

    for row in print_rows:
        combined = " ".join((row["source_reference"], row["phonological_claim"], row["tone_claim"], row["caveat"]))
        assert "source unavailable" not in combined.lower()
        assert "?" not in combined


def test_phonology_tone_diagnostic_discusses_required_topics_and_decision() -> None:
    text = _text(DIAGNOSTIC_PATH).lower()

    for required in (
        "segmental phonology",
        "tone",
        "-a",
        "orthography",
        "small number of bible-attested",
        "tone analysis attached to them remains literature-backed",
        "safe to print now",
        "blocked",
        "literature-only wording",
        "stem alternation",
        "tam",
        "-pih",
        "verb paradigms",
    ):
        assert required in text, required


def test_phonology_tone_dossier_has_requested_scope_buckets() -> None:
    text = _text(DOSSIER_PATH).lower()
    for required in (
        "bible-attested minimal pairs",
        "bible-attested near-minimal pairs",
        "literature-only tone contrasts",
        "blocked or unavailable examples",
        "absence from bible corpus",
        "ambiguous spelling",
        "unresolved tone assignment",
    ):
        assert required in text


def test_phonology_tone_slice_is_grammar_facing_and_hybrid_evidence() -> None:
    text = _text(SLICE_PATH)
    lower = text.lower()

    for forbidden in ("candidate tsv", "dossier", "packet", "review notes", "output/publication_review/", "scripts/", "docs/"):
        assert forbidden not in lower

    for required in (
        "Overview of phonology and tone in Tedim",
        "Orientation table",
        "Bible-attested minimal and near-minimal sets",
        "Short Bible examples",
        "Tone status",
        "The blocked -a issue",
        "Boundaries with stem alternation, TAM, `-pih`, and verb paradigms",
        "Deferred material",
        "What can be printed now",
    ):
        assert required in text

    assert "| Area | Conservative claim | Evidence status | Caveat |" in text
    assert "| Form as printed in the Bible | Tone-marked or phonological form from the literature | Meaning | Bible source | Evidence type | Caveat |" in text
    assert "source unavailable" not in lower
    assert "question-mark" not in lower
    assert "the bible orthography is useful for locating lexical items in context, but the tone contrast itself is taken from the phonological literature" in lower
    assert "tone is not consistently represented in ordinary printed spelling" in lower
    assert "keep `-a` blocked" in text


def test_phonology_tone_slice_has_at_least_two_source_resolved_bible_examples() -> None:
    text = _text(SLICE_PATH)
    headers = re.findall(r"(?m)^\(@ex:[^)]+\)\s+([^\n]+)$", text)
    assert len(headers) >= 2
    assert all(BIBLE_REFERENCE_RE.search(source) for source in headers)

    refs = BIBLE_REFERENCE_RE.findall(text)
    assert len(set(refs)) >= 4

    gloss_lines = re.findall(r"(?m)^c\. Gloss:\s*(.+)$", text)
    assert gloss_lines
    assert all("?" not in gloss for gloss in gloss_lines)


def test_phonology_tone_slice_marks_tone_claims_as_literature_backed_when_using_bible_forms() -> None:
    text = _text(SLICE_PATH)
    table_lines = [line for line in text.splitlines() if "|" in line and BIBLE_REFERENCE_RE.search(line)]
    assert table_lines
    assert all("literature_backed_tone_claim" in line for line in table_lines)


def test_phonology_tone_review_notes_cover_human_checkpoints() -> None:
    text = _text(REVIEW_NOTES_PATH).lower()

    for required in (
        "genuinely minimal or near-minimal",
        "tone values attached to the selected bible-attested forms",
        "verses actually support the meanings",
        "separate bible attestation of forms from literature-backed tone analysis",
        "too speculative",
        "blocked `-a` issue",
    ):
        assert required in text
