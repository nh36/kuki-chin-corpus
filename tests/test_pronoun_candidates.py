import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_pronouns.tsv"

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


def test_pronoun_candidate_file_exists_with_required_columns():
    assert CANDIDATES_PATH.exists()
    header, _ = load_candidates()
    assert REQUIRED_COLUMNS <= header


def test_pronoun_candidate_file_keeps_core_pronouns_and_exclusive_kote():
    _, rows = load_candidates()

    accepted = {
        row["construction_id"]
        for row in rows
        if row["candidate_status"] == "accepted"
    }
    for required in {"kei-pronoun", "kote-exclusive"}:
        assert required in accepted


def test_pronoun_candidate_file_keeps_ei_series_unresolved_and_negative_kei_out():
    _, rows = load_candidates()

    unresolved_rows = [
        row for row in rows
        if row["construction_id"].startswith(("ei", "eite"))
    ]
    assert unresolved_rows
    assert any(row["candidate_status"] in {"needs_review", "deferred"} for row in unresolved_rows)
    assert not any(
        row["candidate_status"] == "accepted"
        and row["construction_id"] in {"ei-clusivity", "eite-inclusive-context", "eite-exclusive-context"}
        for row in unresolved_rows
    )

    kei_negator_rows = [row for row in rows if row["construction_id"] == "kei-negator"]
    assert kei_negator_rows
    assert all(row["candidate_status"] != "accepted" for row in kei_negator_rows)
