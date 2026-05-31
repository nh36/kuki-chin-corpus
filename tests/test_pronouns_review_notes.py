from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_NOTES_PATH = ROOT / "output/publication_review/review_notes_pronouns.md"


def _text() -> str:
    return REVIEW_NOTES_PATH.read_text(encoding="utf-8")


def test_pronouns_review_notes_exists() -> None:
    assert REVIEW_NOTES_PATH.exists(), "Pronouns review notes must exist"


def test_pronouns_review_notes_keeps_core_review_state() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "dossier_pronoun_clusivity.md",
        "candidates_pronouns.tsv",
        "hong-",
        "kong-",
    ):
        assert required in text

    assert "independent pronouns" in lower
    assert "clusivity" in lower
    assert "possessive prefixes and verbal agreement prefixes" in lower


def test_pronouns_review_notes_keeps_ei_under_review() -> None:
    text = _text()
    lower = text.lower()

    assert "ko/kote" in text
    assert "ei/eite" in text
    assert "under review" in lower
