from pathlib import Path


AUDIT_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/evidence_protocol_retrofit_audit.md"


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
    assert "Negation first" in text
    assert "candidates_negation.tsv" in text
