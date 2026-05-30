from pathlib import Path


HANDOFF_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/human_review_handoff.md"


def test_publication_review_handoff_exists_and_names_review_ready_packets():
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert HANDOFF_PATH.exists()
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
    ):
        assert required in text


def test_publication_review_handoff_describes_packet_surfaces_and_review_state():
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert "candidate TSVs" in text
    assert "dossiers" in text
    assert "grammar slices" in text
    assert "dictionary slices" in text
    assert "review notes" in text
    assert "human review / maintenance" in text
    assert "open-ended polishing" in text
    assert "raw generated-report counts as evidence" in text
    assert "deferred rows without analyzer-backed candidates" in text


def test_publication_review_handoff_keeps_selected_scope_and_remaining_deferred_scopes_clear():
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for required in (
        "broad TAM / aspect / modal",
        "chrestomathy",
        "Mizo/lus",
        "other Kuki-Chin languages",
    ):
        assert required in text

    assert "directionals has now been explicitly selected as the next candidate-first packet" in text
    assert "No further narrow publication-review packet should be started automatically." in text
    assert "select one new scope explicitly" in text
    assert "fresh candidate-first plan" in text
