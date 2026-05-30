from pathlib import Path


NOTES_PATH = Path("output/publication_review/review_notes_directionals.md")


def _text() -> str:
    return NOTES_PATH.read_text(encoding="utf-8")


def test_directionals_review_notes_exist() -> None:
    assert NOTES_PATH.exists(), "directionals review notes must exist"


def test_directionals_review_notes_name_controlling_files() -> None:
    text = _text()
    assert "candidates_directionals.tsv" in text
    assert "dossier_directionals.md" in text
    assert "grammar_directionals_print_slice.md" in text
    assert "dictionary_directionals_print_slice.md" in text


def test_directionals_review_notes_mark_packet_aligned_and_review_ready() -> None:
    text = _text()
    assert "current candidate-first maturity level" in text
    assert "ready for human review at the current slice maturity level" in text


def test_directionals_review_notes_cover_safe_anchors() -> None:
    text = _text()
    for required in (
        "pokhia",
        "nawhkhiat",
        "hotkhiatna",
        "kilaktoh",
        "paitoh",
        "kahtohna",
        "tawplam",
        "piasawn",
        "paisuk",
    ):
        assert required in text

    assert "outward `-khia`" in text
    assert "away `-khiat`" in text
    assert "analyzer-label caveat" in text
    assert "nominalized `-khiat-na` boundary material" in text
    assert "upward `-toh`" in text
    assert "comitative/accompany caveat" in text
    assert "nominalized `-toh-na` boundary material" in text
    assert "direction/side/manner boundary material" in text
    assert "cautious toward `-sawn`" in text
    assert "corpus-backed downward evidence through `paisuk`" in text


def test_directionals_review_notes_keep_blocked_and_deferred_material_explicit() -> None:
    text = _text()
    assert "go-accompany" in text
    for required in ("uilut", "paiphei", "`cip`", "`tang`"):
        assert required in text
    assert "deferred or not print-ready" in text


def test_directionals_review_notes_exclude_raw_count_claims_and_raw_harvesting() -> None:
    text = _text()
    for banned in (
        "1,006",
        "180",
        "39",
        "24",
        "13",
        "zero-attestation",
        "zero attestations",
        "0-count",
    ):
        assert banned not in text
    assert "raw suffix harvesting" in text
    assert "raw generated-report counts outside the evidence layer" in text


def test_directionals_review_notes_keep_broader_scopes_deferred() -> None:
    text = _text()
    assert "Broad TAM" in text
    assert "chrestomathy" in text
    assert "Mizo/lus" in text
    assert "other Kuki-Chin languages remain deferred" in text
    assert "should not begin a new grammar packet automatically" in text
