from pathlib import Path


AUDIT_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/evidence_protocol_retrofit_audit.md"
PROGRESS_PATH = Path(__file__).resolve().parents[1] / "PROGRESS.md"


def test_publication_retrofit_audit_exists_and_names_core_packets():
    text = AUDIT_PATH.read_text()

    assert AUDIT_PATH.exists()

    for required in (
        "demonstratives/deixis",
        "negation",
        "pronouns",
        "stem alternation",
        "case marking",
    ):
        assert required in text


def test_publication_retrofit_audit_recommends_priority():
    text = AUDIT_PATH.read_text()

    assert "Recommended retrofit order" in text
    assert "**Case marking packet review next**" in text
    assert "candidates_case_marking.tsv" in text
    assert "extractor route still absent" in text
    assert "candidates_negation.tsv" in text
    assert "candidates_pronouns.tsv" in text
    assert "candidates_stem_alternation.tsv" in text
    assert "stem_alternation_corpus_audit.tsv" in text
    assert "stem_alternation_example_matrix.tsv" in text
    assert "working prose draft" in text or "grammar_stem_alternation_section_draft.md" in text
    assert "dictionary_case_markers_print_slice.md" in text
    assert "no standalone dossier" in text or "no dossier located" in text


def test_progress_marks_case_marking_as_next_retrofit_and_stem_as_review_ready():
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "## Recent Tedim publication-review work" in text
    assert "Demonstratives/deixis remains the protocol-backed pilot" in text
    assert "first working prose draft" in text
    assert "Stem alternation is now ready for human review" in text
    assert "generated locally and intentionally untracked" in text
    assert "`stem_alternation_environment_summary.tsv`, `stem_alternation_pair_summary.tsv`, and `stem_alternation_example_matrix.tsv`" in text
    assert "candidates_case_marking.tsv" in text
    assert "1. [ ] Use the new case-marking candidate layer to review the existing case-marking packet conservatively." in text
    assert "2. [ ] Keep stem alternation stable pending human review." in text
    assert "review the new stem-alternation corpus audit against the packet prose before moving to case marking" not in lower_text
