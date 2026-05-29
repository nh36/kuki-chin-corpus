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
    assert "grammar_interrogatives_print_slice.md" in text
    assert "dictionary_interrogatives_print_slice.md" in text
    assert "review_notes_interrogatives.md" in text
    assert "first analyzer-aware candidate layer, curated extractor route, candidate-controlled dossier, first grammar slice, first dictionary slice, and review notes now exist" in text
    assert "Hold interrogatives stable for human review" in text
    assert "candidates_numerals.tsv" in text
    assert "tests/test_numerals_candidates.py" in text
    assert "dossier_numerals.md" in text
    assert "grammar_numerals_print_slice.md" in text
    assert "tests/test_numerals_print_slice.py" in text
    assert "dictionary_numerals_print_slice.md" in text
    assert "tests/test_numerals_dictionary_slice.py" in text
    assert "review_notes_numerals.md" in text
    assert "tests/test_numerals_review_notes.py" in text
    assert "first analyzer-aware candidate layer, curated extractor route, candidate-controlled dossier, first grammar slice, first dictionary slice, and review notes now exist; the packet is ready for human review at the current slice maturity level" in text
    assert "candidates_quantifiers.tsv" in text
    assert "tests/test_quantifiers_candidates.py" in text
    assert "tests/test_quantifiers_dossier.py" in text
    assert "tests/test_quantifiers_print_slice.py" in text
    assert "first grammar slice now exist" in text
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
    assert "grammar_interrogatives_print_slice.md" in text
    assert "dictionary_interrogatives_print_slice.md" in text
    assert "review_notes_interrogatives.md" in text
    assert "candidates_numerals.tsv" in text
    assert "dossier_numerals.md" in text
    assert "grammar_numerals_print_slice.md" in text
    assert "dictionary_numerals_print_slice.md" in text
    assert "review_notes_numerals.md" in text
    assert "ready for human review at the current slice maturity level" in text
    assert "candidates_quantifiers.tsv" in text
    assert "dossier_quantifiers.md" in text
    assert "grammar_quantifiers_print_slice.md" in text
    assert "keeps explicit overlap controls for `khat`, `kuamah`, and bang-family `bangmah`" in text
    assert "The quantifiers grammar print slice now exists, but the dictionary and review-note slices have not yet begun" in text
    assert "1. [ ] Continue the quantifiers retrofit from `grammar_quantifiers_print_slice.md` into `dictionary_quantifiers_print_slice.md` without broadening into review-note work, coordinators, sentence-final particles, or broad degree/intensifier prose." in text
    assert "2. [ ] Keep demonstratives/deixis, negation, pronouns/clusivity, stem alternation, case marking, interrogatives, and numerals stable for maintenance and human review." in text
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
    assert "grammar_interrogatives_print_slice.md" in text
    assert "dictionary_interrogatives_print_slice.md" in text
    assert "review_notes_interrogatives.md" in text
    assert "hold stable for maintenance and human review" in text
    assert "candidates_interrogatives.tsv" in text
    assert "candidates_numerals.tsv" in text
    assert "dossier_numerals.md" in text
    assert "grammar_numerals_print_slice.md" in text
    assert "dictionary_numerals_print_slice.md" in text
    assert "review_notes_numerals.md" in text
    assert "hold stable for maintenance and human review" in text
    assert "candidates_quantifiers.tsv" in text
    assert "dossier_quantifiers.md" in text
    assert "grammar_quantifiers_print_slice.md" in text
    assert "active narrow retrofit; the quantifiers grammar print slice now exists, but dictionary and review-note slices have not yet begun" in text
    assert "Deferred future or non-slice topics" in text
    for deferred in ("broad TAM / aspect / modal", "directionals", "chrestomathy", "Mizo/lus"):
        assert deferred in text
