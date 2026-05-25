import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_negation.tsv"

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


def test_negation_candidate_file_exists_with_required_columns():
    assert CANDIDATES_PATH.exists()
    header, _ = load_candidates()
    assert REQUIRED_COLUMNS <= header


def test_negation_candidate_file_keeps_core_accepted_and_old_false_friend_out():
    _, rows = load_candidates()

    accepted = {
        row["construction_id"]
        for row in rows
        if row["candidate_status"] == "accepted"
    }
    for required in {"lo", "loh", "kei-prohibitive", "thei-lo"}:
        assert required in accepted

    for row in rows:
        if row["reference"] == "Genesis 2:25":
            assert row["candidate_status"] != "accepted"

        if row["surface_span"] == "maizum lo uh hi":
            assert row["candidate_status"] != "accepted"

        if row["construction_id"] == "lo-uh-prohibitive":
            assert row["candidate_status"] != "accepted"
