import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from analyze_morphemes import analyze_sentence, analyze_word  # noqa: E402


CANDIDATES_PATH = ROOT / "output/publication_review/candidates_pronouns.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"


def load_candidates():
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_tokens():
    csv.field_size_limit(10**7)
    with TOKENS_PATH.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def get_token(verse_id: str, token_index: str):
    for row in load_tokens():
        if row["verse_id"] == verse_id and row["token_index"] == token_index:
            return row
    raise AssertionError(f"Missing token row for {verse_id}:{token_index}")


def test_direct_analyzer_keeps_lexical_ko_available_but_disambiguates_clear_pronoun_frames():
    assert analyze_word("ko") == ("ko", "long")

    for sentence in ("ko tawh", "ko tungah", "ko a' hi", "ko a dingin"):
        rows = analyze_sentence(sentence)
        assert rows[0][1] == "ko"
        assert rows[0][2] == "1PL.EXCL.PRO"


def test_regenerated_export_marks_ko_as_pronoun_in_audited_contexts():
    for verse_id, token_index in (("01024055", "14"), ("02020019", "27")):
        row = get_token(verse_id, token_index)
        assert row["normalized_form"] == "ko"
        assert row["gloss"] == "1PL.EXCL.PRO"
        assert row["pos"] == "PRON"
        assert row["usage_type"] == "grammatical"
        assert row["function_type"] == "1PL"


def test_ko_candidate_row_now_uses_pronoun_export_not_long_adj():
    rows = load_candidates()
    by_construction = {row["construction_id"]: row for row in rows}

    ko_row = by_construction["ko-exclusive"]

    assert ko_row["candidate_status"] == "accepted"
    assert ko_row["gloss_span"] == "1PL.EXCL.PRO | COM"
    assert ko_row["pos_span"] == "PRON | FUNC"
    assert "long" not in ko_row["gloss_span"]
    assert "ADJ" not in ko_row["pos_span"]


def test_pronoun_analyzer_quality_guard_keeps_kote_and_false_friend_boundaries():
    rows = load_candidates()
    by_construction = {row["construction_id"]: row for row in rows}

    assert by_construction["kote-exclusive"]["candidate_status"] == "accepted"
    assert by_construction["kei-negator"]["candidate_status"] == "excluded"
    assert by_construction["ei-exclusive-context"]["candidate_status"] != "accepted"
    assert by_construction["eite-inclusive-context"]["candidate_status"] == "needs_review"
    assert by_construction["eite-exclusive-context"]["candidate_status"] == "needs_review"
