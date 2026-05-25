import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
COMMITTED_CANDIDATES_PATH = ROOT / "output/publication_review/candidates_demonstratives.tsv"


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
    assert result.stdout.strip().splitlines() == ["demonstratives"]


def test_demonstratives_candidates_are_reproducible(tmp_path):
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / "candidates_demonstratives.tsv"
    run_extractor("demonstratives", "--output", str(output_path))

    assert output_path.exists()
    assert COMMITTED_CANDIDATES_PATH.exists()
    assert output_path.read_text(encoding="utf-8") == COMMITTED_CANDIDATES_PATH.read_text(encoding="utf-8")
