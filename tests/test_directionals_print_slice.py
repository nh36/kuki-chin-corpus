from pathlib import Path


SLICE_PATH = Path("output/publication_review/grammar_directionals_print_slice.md")


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_directionals_print_slice_exists() -> None:
    assert SLICE_PATH.exists(), "directionals grammar print slice must exist"


def test_directionals_print_slice_names_controlling_evidence() -> None:
    text = _text()
    assert "candidates_directionals.tsv" in text
    assert "dossier_directionals.md" in text
    assert "controlled by" in text


def test_directionals_print_slice_uses_candidate_control_not_raw_searches() -> None:
    text = _text()
    assert "raw suffix counts" in text
    assert "raw `khia` harvesting" in text


def test_directionals_print_slice_treats_khia_as_outward() -> None:
    text = _text()
    assert "pokhia" in text
    assert "outward `-khia`" in text


def test_directionals_print_slice_treats_khiat_as_away_with_caveat() -> None:
    text = _text()
    assert "nawhkhiat" in text
    assert "away `-khiat`" in text
    assert "accepted with caveat" in text


def test_directionals_print_slice_treats_hotkhiatna_as_nominalized_boundary_material() -> None:
    text = _text()
    assert "hotkhiatna" in text
    assert "`-khiat-na`" in text
    assert "nominalized boundary material" in text


def test_directionals_print_slice_treats_toh_as_upward_with_caveat() -> None:
    text = _text()
    assert "kilaktoh" in text
    assert "upward `-toh`" in text
    assert "polysemy caveat" in text


def test_directionals_print_slice_blocks_paitoh_as_comitative_overlap() -> None:
    text = _text()
    assert "paitoh" in text
    assert "comitative/accompany" in text
    assert "must not imply that every `-toh` token is upward-directional evidence" in text


def test_directionals_print_slice_treats_kahtohna_as_nominalized_boundary_material() -> None:
    text = _text()
    assert "kahtohna" in text
    assert "`-toh-na`" in text
    assert "nominalized boundary material" in text


def test_directionals_print_slice_keeps_lam_as_boundary_material() -> None:
    text = _text()
    assert "tawplam" in text
    assert "direction/side/manner boundary material" in text


def test_directionals_print_slice_treats_sawn_cautiously() -> None:
    text = _text()
    assert "piasawn" in text
    assert "cautious toward `-sawn`" in text


def test_directionals_print_slice_treats_suk_as_corpus_backed() -> None:
    text = _text()
    assert "paisuk" in text
    assert "corpus-backed downward `-suk`" in text
    assert "rather than analyzer inventory alone" in text


def test_directionals_print_slice_defers_lut_phei_cip_tang() -> None:
    text = _text()
    assert "uilut" in text
    assert "paiphei" in text
    assert "`cip`" in text
    assert "`tang`" in text
    assert "deferred or not print-ready" in text


def test_directionals_print_slice_avoids_raw_count_claims() -> None:
    text = _text()
    banned = [
        "1,006",
        "180 for -khiat",
        "39 for -toh",
        "24 for -lam",
        "13 for -sawn",
        "zero-attestation",
        "zero attestations",
        "0-count",
    ]
    for snippet in banned:
        assert snippet not in text


def test_directionals_print_slice_does_not_start_dictionary_or_review_notes() -> None:
    text = _text()
    assert "dictionary print slice" in text
    assert "Dictionary and review-note work have not yet begun." in text
    assert "review_notes_directionals.md" not in text


def test_directionals_print_slice_keeps_broader_work_deferred() -> None:
    text = _text()
    assert "Broad TAM" in text
    assert "chrestomathy" in text
    assert "Mizo/lus" in text
    assert "other Kuki-Chin language work remain deferred" in text
