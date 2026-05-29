from pathlib import Path


AUDIT_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/evidence_protocol_retrofit_audit.md"
INVENTORY_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/remaining_retrofit_inventory.md"
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
    assert "**Case marking packet review next**" not in text
    assert "candidates_case_marking.tsv" in text
    assert "candidates_interrogatives.tsv" in text
    assert "LF-stable reproducible output" in text
    assert "aligned grammar slice" in text
    assert "aligned dictionary slice" in text
    assert "updated review notes" in text
    assert "tests protecting the main distinctions" in text
    assert "dossier_interrogatives.md" in text
    assert "first analyzer-aware candidate layer, curated extractor route, and candidate-controlled dossier now exist" in text
    assert "Continue the active interrogatives retrofit through the candidate-first sequence" in text
    assert "candidates_negation.tsv" in text
    assert "candidates_pronouns.tsv" in text
    assert "candidates_stem_alternation.tsv" in text
    assert "stem_alternation_corpus_audit.tsv" in text
    assert "stem_alternation_example_matrix.tsv" in text
    assert "working prose draft" in text or "grammar_stem_alternation_section_draft.md" in text
    assert "dictionary_case_markers_print_slice.md" in text
    assert "dossier_case_marking.md" in text


def test_progress_marks_current_packets_as_review_ready_and_not_case_marking_next():
    text = PROGRESS_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "## Recent Tedim publication-review work" in text
    assert "Demonstratives/deixis remains the protocol-backed pilot" in text
    assert "first working prose draft" in text
    assert "Stem alternation is now ready for human review" in text
    assert "generated locally and intentionally untracked" in text
    assert "`stem_alternation_environment_summary.tsv`, `stem_alternation_pair_summary.tsv`, and `stem_alternation_example_matrix.tsv`" in text
    assert "candidates_case_marking.tsv" in text
    assert "candidates_interrogatives.tsv" in text
    assert "dossier_interrogatives.md" in text
    assert "aligned grammar and dictionary slices" in text
    assert "The active next publication-review task is now the first interrogatives grammar print slice" in text
    assert "Demonstratives/deixis, negation, pronouns/clusivity, stem alternation, and case marking are now maintenance/human-review topics" in text
    assert "1. [ ] Use `candidates_interrogatives.tsv` plus `dossier_interrogatives.md` to draft `output/publication_review/grammar_interrogatives_print_slice.md`; dictionary and review-note slices have not started yet." in text
    assert "2. [ ] Keep demonstratives/deixis, negation, pronouns/clusivity, stem alternation, and case marking stable for maintenance and human review." in text
    assert "Use the new case-marking candidate layer to review the existing case-marking packet conservatively." not in text
    assert "inventory the remaining existing publication-review slices and grammar reports" not in lower_text
    assert "review the new stem-alternation corpus audit against the packet prose before moving to case marking" not in lower_text


def test_remaining_retrofit_inventory_exists_and_distinguishes_current_vs_future_topics():
    text = INVENTORY_PATH.read_text(encoding="utf-8")

    assert INVENTORY_PATH.exists()
    assert "Existing publication-review packets already at the candidate-first level" in text
    for required in (
        "demonstratives/deixis",
        "negation",
        "pronouns / clusivity",
        "stem alternation",
        "case marking",
    ):
        assert required in text

    assert "interrogatives" in text
    assert "dossier_interrogatives.md" in text
    assert "active retrofit; use the dossier to draft the grammar slice; dictionary and review notes not started" in text
    assert "candidates_interrogatives.tsv" in text
    assert "Deferred future or non-slice topics" in text
    for deferred in ("broad TAM / aspect / modal", "directionals", "chrestomathy", "Mizo/lus"):
        assert deferred in text
