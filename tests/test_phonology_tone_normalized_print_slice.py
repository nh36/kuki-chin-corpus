from __future__ import annotations

import csv
import re
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_REVIEW_DIR = ROOT / "output" / "publication_review"

CANDIDATES_PATH = PUBLICATION_REVIEW_DIR / "candidates_phonology_tone.tsv"
DOSSIER_PATH = PUBLICATION_REVIEW_DIR / "dossier_phonology_tone_scope.md"
SLICE_PATH = PUBLICATION_REVIEW_DIR / "grammar_phonology_tone_print_slice.md"
REVIEW_NOTES_PATH = PUBLICATION_REVIEW_DIR / "review_notes_phonology_tone.md"
DIAGNOSTIC_PATH = PUBLICATION_REVIEW_DIR / "phonology_tone_source_alignment_diagnostic.md"
VERIFICATION_PATH = PUBLICATION_REVIEW_DIR / "phonology_tone_bible_example_verification.md"
ASSEMBLED_TEX_PATH = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.tex"

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

PROMOTABLE_BIBLE_EVIDENCE_TYPES = {
    "true_minimal_pair",
    "near_minimal_pair",
    "homographic_lexical_grammatical_contrast",
    "supporting_bible_attestation",
}


def _rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_diacritic(text: str) -> bool:
    return any(unicodedata.combining(ch) for ch in unicodedata.normalize("NFD", text))


def test_phonology_tone_packet_files_exist() -> None:
    for path in (
        CANDIDATES_PATH,
        DOSSIER_PATH,
        SLICE_PATH,
        REVIEW_NOTES_PATH,
        DIAGNOSTIC_PATH,
        VERIFICATION_PATH,
    ):
        assert path.exists(), f"Missing expected file: {path.name}"


def test_phonology_tone_candidate_tsv_schema_and_classification_inventory() -> None:
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
        "near_minimal_pair",
        "homographic_lexical_grammatical_contrast",
        "supporting_bible_attestation",
        "orthography_support",
        "analyzer_gap_blocked",
        "unresolved_or_conflicting",
    }.issubset(evidence_types)

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

    candidate_statuses = {row["candidate_status"] for row in rows}
    print_statuses = {row["print_status"] for row in rows}
    diagnostic_statuses = {row["diagnostic_status"] for row in rows}

    assert candidate_statuses <= ALLOWED_CANDIDATE_STATUSES
    assert print_statuses <= ALLOWED_PRINT_STATUSES
    assert diagnostic_statuses <= ALLOWED_DIAGNOSTIC_STATUSES

    assert any(row["candidate_status"] == "blocked" for row in rows)
    assert any(row["print_status"] == "blocked" for row in rows)


def test_phonology_tone_verification_file_covers_required_pairs_references_and_decisions() -> None:
    text = _text(VERIFICATION_PATH)
    lower = text.lower()

    for required in (
        "ta / -ta",
        "thei / -thei",
        "hi / hi",
        "Genesis 11:30",
        "Matthew 4:4",
        "Genesis 4:9",
        "Matthew 7:21",
        "Genesis 16:13",
    ):
        assert required in text, required

    for pair in ("ta / -ta", "thei / -thei", "hi / hi"):
        start = lower.find(pair)
        assert start >= 0
        window = lower[start : start + 1200]
        assert ("decision:" in window) or ("| decision |" in window)


def test_nungta_is_explicitly_justified_if_kept_print_facing() -> None:
    rows = _rows()
    ta_rows = [row for row in rows if row["candidate_form"] == "ta / -ta"]
    assert ta_rows
    ta_row = ta_rows[0]

    verification = _text(VERIFICATION_PATH).lower()
    slice_text = _text(SLICE_PATH).lower()

    if ta_row["print_status"] in {"print_ready", "print_usable_with_caveat"}:
        assert "nungta" in verification
        assert "nung-ta" in verification
        assert "analyzer" in verification
        assert "supporting_bible_attestation" in verification
    else:
        # If ta/-ta is not print-facing, ensure nungta is not used as PFV print evidence.
        print_facing_table_lines = [
            line
            for line in slice_text.splitlines()
            if "|" in line and BIBLE_REFERENCE_RE.search(line)
        ]
        assert all("nungta" not in line for line in print_facing_table_lines)


def test_print_facing_bible_rows_have_bible_references_and_precise_classification() -> None:
    rows = _rows()
    bible_rows = [
        row
        for row in rows
        if row["print_status"] in {"print_ready", "print_usable_with_caveat"}
        and row["evidence_type"] in PROMOTABLE_BIBLE_EVIDENCE_TYPES
    ]
    assert len(bible_rows) >= 2

    for row in bible_rows:
        assert BIBLE_REFERENCE_RE.search(row["source_reference"])
        assert row["candidate_status"] in {"accepted", "accepted_with_caveat"}
        assert row["caveat"].strip()

    assert any(row["evidence_type"] == "literature_backed_tone_claim" for row in rows)


def test_phonology_tone_no_print_facing_placeholders_or_question_mark_glosses() -> None:
    rows = _rows()
    print_rows = [row for row in rows if row["print_status"] in {"print_ready", "print_usable_with_caveat"}]
    for row in print_rows:
        combined = " ".join(
            (
                row["source_reference"],
                row["phonological_claim"],
                row["tone_claim"],
                row["why_selected"],
                row["caveat"],
            )
        ).lower()
        assert "source unavailable" not in combined
        assert "placeholder" not in combined
        assert "todo" not in combined
        assert "speculative morphology" not in combined
        assert "?" not in combined

    slice_text = _text(SLICE_PATH)
    gloss_lines = re.findall(r"(?m)^c\. Gloss:\s*(.+)$", slice_text)
    assert gloss_lines
    assert all("?" not in gloss for gloss in gloss_lines)


def test_phonology_tone_diagnostic_and_dossier_cover_required_scope() -> None:
    diagnostic = _text(DIAGNOSTIC_PATH).lower()
    for required in (
        "literature-backed tables",
        "small number of bible-attested",
        "support form existence and contextual use",
        "tone analysis attached to them remains literature-backed",
        "orthography is unmarked",
        "ta / -ta",
        "thei / -thei",
        "hi / hi",
        "keep `-a` blocked",
    ):
        assert required in diagnostic, required

    dossier = _text(DOSSIER_PATH).lower()
    for required in (
        "verified bible-attested examples",
        "bible-attested minimal pairs",
        "bible-attested near-minimal pairs",
        "literature-only tone contrasts",
        "blocked or unavailable examples",
        "absence from bible corpus",
        "ambiguous spelling",
        "lack of source-resolved meaning",
        "unresolved tone analysis",
    ):
        assert required in dossier, required


def test_phonology_tone_slice_separates_orthography_from_literature_tone_analysis() -> None:
    text = _text(SLICE_PATH)
    lower = text.lower()

    for required in (
        "Overview of phonology and tone in Tedim",
        "Orientation table",
        "Bible-attested minimal and near-minimal sets",
        "Short Bible examples",
        "The blocked -a issue",
        "Boundaries with stem alternation, TAM, `-pih`, and verb paradigms",
        "What can be printed now",
    ):
        assert required in text

    assert "Tone-marked or phonological form from the literature" in text
    assert "Short Bible examples are printed in ordinary Bible spelling" in text
    assert "tone-marked forms are restricted to the literature column" in text
    assert (
        "the bible orthography is useful for locating lexical items in context, but the tone contrast itself is taken from the phonological literature"
        in lower
    )
    assert "tone is not consistently represented in ordinary printed spelling" in lower


def test_phonology_examples_do_not_silently_tone_mark_object_language_words() -> None:
    slice_text = _text(SLICE_PATH)
    tedim_lines = re.findall(r"(?m)^a\. Tedim:\s*(.+)$", slice_text)
    assert len(tedim_lines) >= 2
    assert all(not _has_diacritic(line) for line in tedim_lines)

    tex = _text(ASSEMBLED_TEX_PATH)
    tex_lines = tex.splitlines()
    phon_gll_lines: list[str] = []
    for idx, line in enumerate(tex_lines):
        if line.strip().startswith(r"\ex \label{ex:phon-"):
            for j in range(idx + 1, min(idx + 8, len(tex_lines))):
                candidate = tex_lines[j].strip()
                if candidate.startswith(r"\gll "):
                    phon_gll_lines.append(candidate.removeprefix(r"\gll ").split(r" \\")[0])
                    break

    assert len(phon_gll_lines) >= 2
    assert all(not _has_diacritic(line) for line in phon_gll_lines)


def test_review_notes_cover_requested_human_checks() -> None:
    text = _text(REVIEW_NOTES_PATH).lower()
    for required in (
        "genuinely near-minimal",
        "verse actually support",
        "nungta",
        "lexical/grammatical",
        "separate bible attestation of forms from literature-backed tone analysis",
        "too speculative",
        "blocked `-a`",
    ):
        assert required in text


def test_unresolved_a_and_analyzer_gap_material_remain_blocked() -> None:
    rows = _rows()
    a_rows = [row for row in rows if row["candidate_form"] == "-a"]
    assert a_rows
    a_row = a_rows[0]
    assert a_row["candidate_status"] == "blocked"
    assert a_row["print_status"] == "blocked"
    assert a_row["evidence_type"] == "analyzer_gap_blocked"

    slice_text = _text(SLICE_PATH)
    assert "keep `-a` blocked" in slice_text
