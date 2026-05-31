from pathlib import Path


AUDIT_PATH = Path("output/publication_review/whole_grammar_coverage_audit.md")


def _text() -> str:
    return AUDIT_PATH.read_text(encoding="utf-8")


def test_whole_grammar_coverage_audit_exists() -> None:
    assert AUDIT_PATH.exists(), "Whole-grammar coverage audit must exist"


def test_whole_grammar_coverage_audit_names_controlling_architecture_sources() -> None:
    text = _text()

    for required in (
        "grammar_source_map.json",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "SKELETON_GRAMMAR.md",
        "grammar_full.md",
        "remaining_retrofit_inventory.md",
        "human_review_handoff.md",
    ):
        assert required in text


def test_whole_grammar_coverage_audit_describes_grammar_full_as_non_final() -> None:
    text = _text()
    lower = text.lower()

    assert "grammar_full.md" in text
    assert "drafting/integration output, not proof of completeness" in lower


def test_whole_grammar_coverage_audit_lists_completed_packets() -> None:
    text = _text()

    for required in (
        "demonstratives/deixis",
        "negation",
        "pronouns/clusivity",
        "stem alternation",
        "case marking",
        "interrogatives",
        "numerals",
        "quantifiers",
        "coordinators",
        "sentence-final particles",
        "directionals",
        "broad TAM / aspect / modal",
        "relators/postpositions",
    ):
        assert required in text


def test_whole_grammar_coverage_audit_lists_uncovered_or_partial_domains() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "phonology and tone",
        "simple nouns",
        "compound nouns",
        "proper nouns",
        "NP structure",
        "possession",
        "pronominal prefixes / agreement / possessive prefixes",
        "VP structure",
        "transitivity",
        "derivation and valency",
        "reduplication",
        "nominalization",
        "subordination",
        "switch reference",
        "relative clauses",
    ):
        assert required in text

    assert "partially covered by an existing packet but not fully lifted" in lower
    assert "current report/literature evidence exists but no packet yet" in lower


def test_whole_grammar_coverage_audit_says_whole_grammar_is_not_complete_and_defers_print() -> None:
    text = _text()
    lower = text.lower()

    assert "whole Tedim grammar is **not** yet complete at the same maturity level" in text
    assert "coverage/priority decision before printing a full grammar bundle" in lower
    assert "do **not** print a full tedim grammar bundle yet" in lower
