from pathlib import Path


CHECKPOINT_PATH = Path("output/publication_review/post_normalization_coverage_checkpoint.md")


def _text() -> str:
    return CHECKPOINT_PATH.read_text(encoding="utf-8")


def test_post_normalization_coverage_checkpoint_exists() -> None:
    assert CHECKPOINT_PATH.exists(), "Post-normalization checkpoint must exist"


def test_post_normalization_coverage_checkpoint_reports_current_preview_status() -> None:
    text = _text()
    lower = text.lower()

    assert "Current grammar-facing preview status" in text
    assert "much more homogeneous" in text
    assert "not a finished grammar" in text
    assert "review-readiness work" in text
    assert "automatic new-packet sequence" in text
    assert "source-balance and stale-prose review" in text


def test_post_normalization_coverage_checkpoint_lists_normalized_sections_and_gaps() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Normalized sections",
        "coordinators",
        "reduplication",
        "Narrow-but-acceptable review-note packets",
        "Explicit gaps",
        "phonology / tone",
        "verb paradigms",
        "broader discourse beyond the current sentence-final slice",
        "switch-reference / relative-clause work remains boundary-heavy inside clause linkage",
    ):
        assert required in text

    assert "chrestomathy" in lower
    assert "mizo/lus" in lower


def test_post_normalization_coverage_checkpoint_recommends_review_readiness_over_new_packets() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Possible next editorial passes",
        "source-balance and stale-prose review across the assembled grammar review preview",
        "minor source-balance cleanup only where a normalized section is still skewed",
        "human review of the narrow review-note packets",
        "no new first-pass packet",
        "Run a source-balance and stale-prose review across the assembled grammar review preview.",
        "Do not open another new linguistic section automatically.",
    ):
        assert required in text

    assert "new first-pass packet" in lower
