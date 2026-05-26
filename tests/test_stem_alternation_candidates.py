import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_stem_alternation.tsv"

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


def test_stem_alternation_candidate_file_exists_with_required_columns():
    assert CANDIDATES_PATH.exists()
    header, _ = load_candidates()
    assert REQUIRED_COLUMNS <= header


def test_stem_alternation_candidate_file_keeps_core_pairs_and_caveated_expansions():
    _, rows = load_candidates()

    accepted_rows = [row for row in rows if row["candidate_status"] == "accepted"]
    accepted_constructions = {row["construction_id"] for row in accepted_rows}

    assert {"mu-muh", "ne-nek", "nei-neih"} <= accepted_constructions
    assert "za-zak" in accepted_constructions
    assert "nusia-nusiat" in accepted_constructions


def test_stem_alternation_candidate_file_keeps_noisy_pairs_out_of_accepted_set():
    _, rows = load_candidates()

    by_candidate = {row["candidate_id"]: row for row in rows}
    by_construction = {}
    for row in rows:
        by_construction.setdefault(row["construction_id"], []).append(row)

    assert any(row["candidate_status"] in {"excluded", "needs_review"} for row in rows)
    assert by_candidate["stem-piangsak-noise-gen-1-1"]["candidate_status"] == "excluded"
    assert by_candidate["stem-ngaihsutna-noise-gen-6-5"]["candidate_status"] == "excluded"
    assert by_candidate["stem-honkhiat-rev-6-1"]["candidate_status"] == "excluded"
    assert by_candidate["stem-theihna-gen-2-17"]["candidate_status"] == "needs_review"
    assert by_candidate["stem-pianna-gen-10-29"]["candidate_status"] == "needs_review"
    assert all(row["candidate_status"] != "accepted" for row in by_construction["ngai-ngaih-family"])
