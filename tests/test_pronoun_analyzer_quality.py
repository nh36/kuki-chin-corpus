import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_pronouns.tsv"


def load_candidates():
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def test_ko_candidate_retains_explicit_export_caveat_until_analyzer_fix():
    rows = load_candidates()
    by_construction = {row["construction_id"]: row for row in rows}

    ko_row = by_construction["ko-exclusive"]

    assert ko_row["candidate_status"] == "accepted"
    assert "gloss `long`" in ko_row["notes"]
    assert "POS `ADJ`" in ko_row["notes"]


def test_pronoun_analyzer_quality_guard_keeps_kote_and_false_friend_boundaries():
    rows = load_candidates()
    by_construction = {row["construction_id"]: row for row in rows}

    assert by_construction["kote-exclusive"]["candidate_status"] == "accepted"
    assert by_construction["kei-negator"]["candidate_status"] == "excluded"
    assert by_construction["ei-exclusive-context"]["candidate_status"] != "accepted"
