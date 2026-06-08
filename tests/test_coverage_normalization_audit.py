from pathlib import Path


AUDIT_PATH = Path("output/publication_review/coverage_normalization_audit.md")


def _text() -> str:
    return AUDIT_PATH.read_text(encoding="utf-8")


def test_coverage_normalization_audit_exists() -> None:
    assert AUDIT_PATH.exists(), "Coverage normalization audit must exist"


def test_coverage_normalization_audit_names_current_controlling_sources() -> None:
    text = _text()

    for required in (
        "assembled_grammar_review_preview.md",
        "post_normalization_coverage_checkpoint.md",
        "whole_grammar_coverage_audit.md",
        "whole_grammar_coverage_checkpoint_after_reduplication.md",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "SKELETON_GRAMMAR.md",
        "PROGRESS.md",
    ):
        assert required in text


def test_coverage_normalization_audit_has_current_section_state_tables() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "Normalized grammar-facing sections",
        "Narrow but acceptable review-note packets",
        "Explicit gaps",
        "Deferred scopes",
        "Post-normalization conclusion",
        "Examples in current print slice",
        "Source distribution",
        "Inventory / paradigm?",
        "Current prose depth",
        "Recommended next action",
    ):
        assert required in text

    assert "| Coordinators | 8 (OT 5 / Gospel 3) | checked but OT-leaning | yes | normalized section |" in text
    assert "| Reduplication | 6 (OT 3 / Gospel 3) | balanced | yes | normalized section |" in text
    assert "source-balance review, then hold stable" in text
    assert "NP vs clause coordination table" not in lower
    assert "zero formal examples" not in lower
    assert "reduplication is only a narrow slice" not in lower


def test_coverage_normalization_audit_keeps_major_gaps_and_deferred_scopes_visible() -> None:
    text = _text()
    lower = text.lower()

    assert "Phonology / tone" in text
    assert "Verb paradigms" in text
    assert "Broader discourse" in text
    assert "Switch-reference and relative clauses stay boundary-heavy" in text
    assert "Chrestomathy and Mizo/lus remain deferred." in text
    assert "major gap" in lower


def test_coverage_normalization_audit_recommends_review_readiness_work() -> None:
    text = _text()
    lower = text.lower()

    assert "source-balance and stale-prose review across the assembled preview" in text
    assert "review-readiness work" in lower
    assert "not an automatic new-packet sequence" in text
    assert "not a new first-pass packet" in lower
