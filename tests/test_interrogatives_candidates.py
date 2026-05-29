import csv
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_interrogatives.tsv"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"

ACCEPTED_STATUSES = {"accepted", "accepted_with_caveat"}
REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "interrogative_type",
    "question_word",
    "particle",
    "construction_type",
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
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
}


def run_extractor(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def load_rows() -> list[dict[str, str]]:
    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return list(reader)


def test_interrogatives_candidate_file_exists_and_has_required_columns() -> None:
    rows = load_rows()

    assert CANDIDATES_PATH.exists()
    assert rows
    assert REQUIRED_COLUMNS.issubset(rows[0].keys())
    assert {row["topic"] for row in rows} == {"interrogatives"}


def test_interrogatives_candidate_file_covers_core_hiam_and_wh_evidence() -> None:
    rows = load_rows()
    accepted_rows = [row for row in rows if row["candidate_status"] in ACCEPTED_STATUSES]

    assert any(row["construction_type"] == "clause_final_hiam" for row in accepted_rows)
    assert any(row["construction_type"] == "wh_plus_hiam" for row in accepted_rows)

    accepted_question_words = {row["question_word"] for row in accepted_rows if row["question_word"]}
    assert {"bang", "kua", "bangci", "banghangin"} <= accepted_question_words


def test_interrogatives_candidate_file_keeps_embedded_and_formulaic_rows_conservative() -> None:
    rows = {row["candidate_id"]: row for row in load_rows()}

    embedded = rows["int_embedded_exod16_15_bang_hiam_cih_thei_lo_uh_hi"]
    assert embedded["candidate_status"] == "needs_review"
    assert embedded["print_status"] == "not_print_ready"

    formulaic = rows["int_formulaic_gen3_20_bang_hang_hiam_cih_leh"]
    assert formulaic["interrogative_type"] == "rhetorical_or_formulaic"
    assert formulaic["construction_type"] == "formulaic_reason_expression"
    assert formulaic["candidate_status"] == "excluded"
    assert formulaic["print_status"] == "blocked"


def test_interrogatives_candidate_file_blocks_lexical_hiam_and_bang_false_friends() -> None:
    rows = {row["candidate_id"]: row for row in load_rows()}

    rev_false_friend = rows["int_falsefriend_rev1_16_langnih_a_hiam_namsau"]
    assert rev_false_friend["candidate_status"] == "excluded"
    assert rev_false_friend["print_status"] == "blocked"
    assert "sharp/two-edged" in rev_false_friend["why_selected"]

    lexical_false_friend = rows["int_falsefriend_2kings11_11_a_hiam_ciat_uh"]
    assert lexical_false_friend["candidate_status"] == "excluded"
    assert lexical_false_friend["print_status"] == "blocked"

    bangmah = rows["int_falsefriend_gen9_21_bangmah"]
    bangin = rows["int_falsefriend_gen1_7_bangin"]
    assert bangmah["candidate_status"] == "excluded"
    assert bangmah["print_status"] == "blocked"
    assert bangin["candidate_status"] == "excluded"
    assert bangin["print_status"] == "blocked"


def test_interrogatives_candidate_file_does_not_promote_comparison_particles() -> None:
    rows = load_rows()

    accepted_particles = {
        row["particle"]
        for row in rows
        if row["candidate_status"] in ACCEPTED_STATUSES and row["particle"]
    }
    assert {"maw", "ham", "em"}.isdisjoint(accepted_particles)
    assert any("Comparison particles `maw`, `ham`, and `em` remain deferred" in row["notes"] for row in rows)


def test_interrogatives_extractor_lists_supported_topic() -> None:
    result = run_extractor("--list-topics")
    assert "interrogatives" in result.stdout.strip().splitlines()


def test_interrogatives_candidates_are_reproducible_when_tokens_exist(tmp_path) -> None:
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_interrogatives.tsv"
    run_extractor("interrogatives", "--output", str(output_path))

    assert output_path.exists()
    assert output_path.read_text(encoding="utf-8") == CANDIDATES_PATH.read_text(encoding="utf-8")
