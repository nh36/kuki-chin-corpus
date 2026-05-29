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


def test_publication_evidence_protocol_marks_case_marking_as_next_planned_retrofit():
    text = PROTOCOL_PATH.read_text(encoding="utf-8")

    assert "third completed retrospective retrofit" in text
    assert "Case marking is the next planned retrofit" in text
    assert "should start from analyzer-aware candidates rather than from raw string searches" in text


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
