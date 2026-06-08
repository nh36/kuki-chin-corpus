from pathlib import Path


AUDIT_PATH = Path("output/publication_review/consistency_drift_invariant_audit.md")
PREVIEW_PATH = Path("output/publication_review/assembled_grammar_review_preview.md")


def _audit_text() -> str:
    return AUDIT_PATH.read_text(encoding="utf-8")


def _preview_text() -> str:
    return PREVIEW_PATH.read_text(encoding="utf-8")


def test_consistency_drift_invariant_audit_exists() -> None:
    assert AUDIT_PATH.exists(), "Consistency drift audit must exist"


def test_consistency_drift_invariant_audit_names_core_invariants() -> None:
    text = _audit_text()

    for required in (
        "Current review-preview status",
        "Invariant checklist",
        "Grammar prose stays grammar-facing",
        "Formal examples keep source references after translation",
        "Claims stay evidence-controlled",
        "Boundary / deferred material stays bounded",
        "Preview says it is not finished",
        "Explicit gaps stay explicit",
        "Deferred scopes stay deferred",
        "Source balance is recorded, not optimized",
    ):
        assert required in text


def test_consistency_drift_invariant_audit_mentions_source_balance_and_scope_limits() -> None:
    text = _audit_text()

    for required in (
        "Numerals",
        "Pronouns / clusivity",
        "Stem alternation",
        "Directionals",
        "Clause linkage",
        "phonology/tone",
        "verb paradigms",
        "broader discourse beyond the current sentence-final particle material",
        "switch-reference and relative clauses as boundary-heavy inside clause linkage",
        "chrestomathy",
        "Mizo/lus",
        "other Kuki-Chin languages",
    ):
        assert required in text


def test_consistency_drift_invariant_audit_recommends_review_readiness() -> None:
    text = _audit_text().lower()

    assert "review-readiness and human-review preparation" in text
    assert "do not open another first-pass packet automatically" in text


def test_assembled_preview_keeps_nonfinal_and_drops_obvious_workflow_phrases() -> None:
    text = _preview_text()
    lower = text.lower()

    assert "not a finished grammar" in lower

    for forbidden in (
        "dictionary and review-note slices have not yet begun",
        "candidate tsv",
        "deferred disjunction candidate",
        "prospective candidate",
        "table-only candidates",
        "ready for human review",
        "packet complete",
        "this packet is now complete",
    ):
        assert forbidden not in lower
