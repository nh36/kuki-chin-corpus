from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_PATH = (
    ROOT / "output/publication_review/whole_grammar_coverage_checkpoint_after_reduplication.md"
)


def _text() -> str:
    return CHECKPOINT_PATH.read_text(encoding="utf-8")


def test_checkpoint_after_reduplication_exists() -> None:
    assert CHECKPOINT_PATH.exists(), "Coverage checkpoint after reduplication must exist"


def test_checkpoint_names_controlling_architecture_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_audit.md",
        "PROGRESS.md",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "SKELETON_GRAMMAR.md",
        "grammar_source_map.json",
    ):
        assert required in text


def test_checkpoint_names_packet_review_notes_and_reduplication_maturity() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "review_notes_demonstratives.md",
        "review_notes_negation.md",
        "review_notes_pronouns.md",
        "review_notes_stem_alternation.md",
        "review_notes_case_marking.md",
        "review_notes_interrogatives.md",
        "review_notes_directionals.md",
        "review_notes_sentence_final_particles.md",
        "review_notes_relators_postpositions.md",
        "review_notes_tam.md",
        "review_notes_vp_structure_stacking.md",
        "review_notes_derivation_valency.md",
        "review_notes_prefix_agreement.md",
        "review_notes_clause_linkage.md",
        "review_notes_nominalization.md",
        "review_notes_np_possession.md",
        "review_notes_noun_domain.md",
        "review_notes_reduplication.md",
    ):
        assert required in text

    assert "review-note maturity" in lower
    assert "reduplication" in lower


def test_checkpoint_identifies_narrow_packet_maturity_and_second_pass_gaps() -> None:
    text = _text()
    lower = text.lower()

    assert "deliberately narrow slice maturity" in lower
    for required in (
        "beyond `-sak`",
        "beyond `ciangin`",
        "beyond `-na`",
        "beyond simple noun stems",
        "beyond intensifying full reduplication",
        "hong-/kong- object-prefix or inverse-like rows",
    ):
        assert required in text


def test_checkpoint_identifies_remaining_unpacketized_or_blocked_domains() -> None:
    text = _text()
    lower = text.lower()

    assert "phonology/tone" in lower
    assert "transitivity" in lower
    assert "report-backed but unpacketized" in lower
    assert "blocked or theory-heavy" in lower


def test_checkpoint_includes_do_not_expand_yet_and_concrete_next_task() -> None:
    text = _text()
    lower = text.lower()

    assert "# Do-not-expand-yet list" in text
    assert "transitivity candidate/scoping packet" in lower
    assert "next agent task" in lower
    assert "does not create a new grammar, dictionary, or review-note slice" in lower
