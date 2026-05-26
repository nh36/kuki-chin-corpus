import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
COMMITTED_CANDIDATE_PATHS = {
    "demonstratives": ROOT / "output/publication_review/candidates_demonstratives.tsv",
    "negation": ROOT / "output/publication_review/candidates_negation.tsv",
    "pronouns": ROOT / "output/publication_review/candidates_pronouns.tsv",
    "stem_alternation": ROOT / "output/publication_review/candidates_stem_alternation.tsv",
}


def run_extractor(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )


def test_candidate_extractor_lists_supported_topics():
    result = run_extractor("--list-topics")
    assert result.stdout.strip().splitlines() == ["demonstratives", "negation", "pronouns", "stem_alternation"]


@pytest.mark.parametrize("topic", ["demonstratives", "negation", "pronouns", "stem_alternation"])
def test_candidates_are_reproducible(tmp_path, topic):
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / f"candidates_{topic}.tsv"
    run_extractor(topic, "--output", str(output_path))

    assert output_path.exists()
    committed_path = COMMITTED_CANDIDATE_PATHS[topic]
    assert committed_path.exists()
    assert output_path.read_text(encoding="utf-8") == committed_path.read_text(encoding="utf-8")
