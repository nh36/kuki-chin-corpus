from pathlib import Path


RECON_PATH = Path("output/publication_review/report_to_grammar_coverage_reconciliation.md")


def _text() -> str:
    return RECON_PATH.read_text(encoding="utf-8")


def test_report_to_grammar_coverage_reconciliation_exists() -> None:
    assert RECON_PATH.exists(), "Reconciliation audit must exist"


def test_reconciliation_names_controlling_source_architecture() -> None:
    text = _text()

    for required in (
        "docs/SKELETON_GRAMMAR.md",
        "docs/grammar/GRAMMAR_SOURCE_INVENTORY.md",
        "docs/grammar/grammar_source_map.json",
        "docs/grammar/reports/",
        "docs/grammar/lit-reviews/",
        "docs/grammar/morphemes/",
        "docs/grammar/README_ANALYZER_GAPS.md",
        "docs/grammar/ANALYZER_LITERATURE_GAPS.md",
        "docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md",
        "docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md",
        "output/grammar/grammar_full.md",
        "output/publication_review/assembled_grammar_review_preview.md",
    ):
        assert required in text


def test_reconciliation_includes_source_to_preview_matrix() -> None:
    text = _text()

    assert "Source-to-preview matrix" in text
    assert "| Domain | Source files / source category |" in text
    assert "Coverage type" in text


def test_reconciliation_includes_major_domains_and_analyzer_topics() -> None:
    text = _text()

    for required in (
        "phonology and tone",
        "Bible-example verified",
        "simple nouns",
        "compound nouns",
        "proper nouns",
        "noun domain generally",
        "NP structure",
        "possession",
        "case marking",
        "relators / postpositions",
        "demonstratives / deixis",
        "pronouns / clusivity",
        "pronominal prefixes / agreement",
        "object-prefix or inverse-like `hong-` / `kong-`",
        "reflexive / reciprocal / middle-like `ki-`",
        "verb paradigms",
        "stem alternation",
        "transitivity",
        "TAM / aspect / modal",
        "directionals",
        "VP structure",
        "suffix combinations / stacking",
        "derivation / valency",
        "`-sak`",
        "`-pih`",
        "nominalization",
        "reduplication",
        "interrogatives",
        "negation",
        "quantifiers",
        "numerals",
        "coordinators",
        "sentence-final particles",
        "subordination",
        "switch reference",
        "same-subject and different-subject clause linkage",
        "relative clauses",
        "broader discourse beyond sentence-final particles",
        "tone in `-a` case marker",
        "conditioned variants (`-pah` / `-pak` / `-lawh`)",
        "`-thei/-theih`",
        "habituals (`ngei` / `gige` / `zel`)",
    ):
        assert required in text


def test_reconciliation_distinguishes_required_coverage_types() -> None:
    text = _text().lower()

    for required in (
        "core section",
        "narrow slice",
        "boundary-only",
        "mentioned only",
        "packetized",
        "blocked",
        "deferred",
    ):
        assert required in text


def test_reconciliation_explicitly_states_preview_is_not_complete_grammar() -> None:
    text = _text().lower()

    assert "not yet a complete tedim grammar" in text
    assert "coverage-reconciliation task" in text or "architecture-focused" in text


def test_reconciliation_recommends_substantive_next_target_not_admin_handoff() -> None:
    text = _text()
    lower = text.lower()

    assert "# 4. Recommendation for the next substantive packet" in text
    assert "Synchronization update:" in text
    assert "same-subject and different-subject clause linkage has now been stabilized" in lower
    assert "Current active substantive target: relative clauses." in text
    assert "report-alignment stabilized" in lower
    assert "human-review handoff" not in lower


def test_reconciliation_includes_switch_reference_implementation_sketch() -> None:
    text = _text()

    for required in (
        "# 5. Implementation sketch for the active relative-clause target",
        "output/publication_review/candidates_relative_clauses.tsv",
        "output/publication_review/dossier_relative_clauses_scope.md",
        "output/publication_review/grammar_relative_clauses_print_slice.md",
        "output/publication_review/relative_clauses_source_alignment_diagnostic.md",
        "output/publication_review/review_notes_relative_clauses.md",
        "Core relative anchor: `a bawl mi`",
        "Supporting relative-like material: `omte`",
        "Boundary rows: `omna`, `muhna-ah`, ordinary `ciangin`, purposive `dingin`, support-only `ahih ciangin`, and report-only `a om lai` / `a gen thu`",
    ):
        assert required in text
