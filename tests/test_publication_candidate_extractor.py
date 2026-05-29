import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/publication_review/extract_candidates.py"
TOKENS_PATH = ROOT / "data/ctd_analysis/tokens.tsv"
COMMITTED_CANDIDATE_PATHS = {
    "demonstratives": ROOT / "output/publication_review/candidates_demonstratives.tsv",
    "case_marking": ROOT / "output/publication_review/candidates_case_marking.tsv",
    "interrogatives": ROOT / "output/publication_review/candidates_interrogatives.tsv",
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
    assert result.stdout.strip().splitlines() == [
        "demonstratives",
        "case_marking",
        "interrogatives",
        "negation",
        "pronouns",
        "stem_alternation",
    ]


def test_candidate_extraction_doc_marks_case_marking_and_interrogatives_as_supported_but_curated():
    text = (ROOT / "docs/publication_review/CANDIDATE_EXTRACTION.md").read_text(encoding="utf-8")

    assert "Current supported extractor topics:" in text
    assert "- `case_marking`" in text
    assert "- `interrogatives`" in text
    assert "extractor-supported through the same curated candidate route" in text
    assert "rather than doing a broad automatic case-marker search" in text
    assert "Relator nouns should not be flattened into bare case suffixes" in text
    assert "interrogatives has now joined that supported set through a narrow curated route" in text
    assert "It is **not** a broad automatic search for all `hiam`, `bang`, or `kua` hits." in text
    assert "explicit blocked false friends" in text


def test_committed_candidate_files_use_lf_line_endings():
    for path in COMMITTED_CANDIDATE_PATHS.values():
        data = path.read_bytes()
        assert b"\r\n" not in data, f"{path} contains CRLF line endings"
        assert b"\r" not in data, f"{path} contains bare CR line endings"


@pytest.mark.parametrize("topic", ["demonstratives", "case_marking", "interrogatives", "negation", "pronouns", "stem_alternation"])
def test_candidates_are_reproducible(tmp_path, topic):
    if not TOKENS_PATH.exists():
        pytest.skip("data/ctd_analysis/tokens.tsv is absent; candidate reproducibility cannot be checked")

    output_path = tmp_path / f"candidates_{topic}.tsv"
    run_extractor(topic, "--output", str(output_path))

    assert output_path.exists()
    committed_path = COMMITTED_CANDIDATE_PATHS[topic]
    assert committed_path.exists()
    assert output_path.read_text(encoding="utf-8") == committed_path.read_text(encoding="utf-8")
