from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT_PATH = (
    ROOT / "output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md"
)


def _text() -> str:
    return CHECKPOINT_PATH.read_text(encoding="utf-8")


def test_checkpoint_after_transitivity_exists() -> None:
    assert CHECKPOINT_PATH.exists(), "Coverage checkpoint after transitivity must exist"


def test_checkpoint_after_transitivity_names_controlling_architecture_sources() -> None:
    text = _text()

    for required in (
        "whole_grammar_coverage_checkpoint_after_reduplication.md",
        "whole_grammar_coverage_audit.md",
        "PROGRESS.md",
        "GRAMMAR_SOURCE_INVENTORY.md",
        "SKELETON_GRAMMAR.md",
        "grammar_source_map.json",
    ):
        assert required in text


def test_checkpoint_after_transitivity_names_review_note_packets() -> None:
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
        "review_notes_transitivity.md",
    ):
        assert required in text

    assert "review-note maturity" in lower
    assert "transitivity" in lower


def test_checkpoint_after_transitivity_identifies_narrow_slice_completion() -> None:
    text = _text()
    lower = text.lower()

    assert "deliberately narrow slice maturity" in lower
    for required in (
        "bawlzoding",
        "`-sak`",
        "kanei / kainn",
        "ciangin",
        "`-na / bawlna`",
        "hih mite",
        "mi khat",
        "mi khempeuh",
        "gam",
        "aksi / aksi-te",
        "mahmah / taktak",
        "sih / suak",
        "hawl / en",
    ):
        assert required in text


def test_checkpoint_after_transitivity_discusses_remaining_domains() -> None:
    text = _text()
    lower = text.lower()

    assert "phonology/tone" in lower
    assert "verb paradigms" in lower
    assert "broader discourse" in lower or "discourse" in lower
    assert "analyzer-gap topics" in lower


def test_checkpoint_after_transitivity_has_clear_decision_and_next_task() -> None:
    text = _text()
    lower = text.lower()

    assert "# Decision" in text
    assert "no remaining report-backed, non-blocked domain clearly comparable to transitivity" in lower
    assert "recommended next agent task" in lower
    assert "human-review handoff" in lower or "stabilization/handoff" in lower
    assert "does not create a new grammar, dictionary, or review-note slice" in lower
