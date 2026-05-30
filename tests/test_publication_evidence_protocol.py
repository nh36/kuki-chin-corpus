import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_PATH = ROOT / "docs/publication_review/EVIDENCE_PROTOCOL.md"
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_demonstratives.tsv"

REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
}


def load_candidates():
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        rows = list(reader)
        return set(reader.fieldnames or []), rows


def test_publication_evidence_protocol_exists():
    assert PROTOCOL_PATH.exists()


def test_publication_evidence_protocol_marks_case_marking_coordinators_interrogatives_numerals_and_quantifiers_as_curated_retrofits():
    text = PROTOCOL_PATH.read_text(encoding="utf-8")

    assert "third completed retrospective retrofit" in text
    assert "candidates_case_marking.tsv" in text
    assert "plus a curated extractor route" in text
    assert "intentionally narrow rather than a broad automatic case-marker search" in text
    assert "should continue to start from analyzer-aware candidates rather than from raw string searches" in text
    assert "Coordinators has now begun as the next narrow retrofit under this workflow." in text
    assert "candidates_coordinators.tsv" in text
    assert "clean `le` NP-conjunction anchor" in text
    assert "conditional `leh` and sequential-versus-agreement `a`" in text
    assert "keeps `mawh` visible only as deferred lexical-export material" in text
    assert "Interrogatives is now a completed narrow retrofit packet under this workflow." in text
    assert "candidates_interrogatives.tsv" in text
    assert "focuses on clause-final `hiam`, selected WH-question windows" in text
    assert "explicit blocked false friends" in text
    assert "Numerals is now a completed current-slice packet under this workflow." in text
    assert "candidates_numerals.tsv" in text
    assert "blocks interrogative `kua = who` as a numeral false friend" in text
    assert "keeps `khat` on the numeral-versus-indefinite boundary" in text
    assert "Quantifiers is now a completed current-slice packet under this workflow." in text
    assert "candidates_quantifiers.tsv" in text
    assert "preserves overlap controls for `khat`, `kuamah`, and bang-family `bangmah`" in text
    assert "ready for human review at the current slice maturity level" in text


def test_demonstratives_candidate_file_has_required_columns():
    assert CANDIDATES_PATH.exists()
    header, _ = load_candidates()
    assert REQUIRED_COLUMNS <= header


def test_demonstratives_candidate_file_keeps_core_accepted_and_bad_examples_unaccepted():
    _, rows = load_candidates()

    accepted = {
        row["construction_id"]
        for row in rows
        if row["candidate_status"] == "accepted"
    }
    for required in {"hih", "tua", "hihte", "tuate", "tua-ciangin"}:
        assert required in accepted

    for row in rows:
        if row["construction_id"] in {"hi", "hih-ciangin"}:
            assert row["candidate_status"] != "accepted"

        if row["reference"] == "Genesis 6:22" and row["construction_id"] == "hih-bangin":
            assert row["candidate_status"] != "accepted"

        if row["reference"] == "John 1:19" and row["construction_id"] == "hi":
            assert row["candidate_status"] != "accepted"
