from pathlib import Path


SLICE_PATH = Path("output/publication_review/dictionary_directionals_print_slice.md")


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_directionals_dictionary_slice_exists() -> None:
    assert SLICE_PATH.exists(), "directionals dictionary print slice must exist"


def test_directionals_dictionary_slice_names_controlling_and_cross_reference_files() -> None:
    text = _text()
    assert "candidates_directionals.tsv" in text
    assert "dossier_directionals.md" in text
    assert "grammar_directionals_print_slice.md" in text


def test_directionals_dictionary_slice_says_it_does_not_edit_machine_dictionary_or_analyzer_files() -> None:
    text = _text()
    assert "do not imply changes to analyzer dictionaries, machine dictionary files, or lexical source tables" in text


def test_directionals_dictionary_slice_has_all_expected_entry_headings() -> None:
    text = _text()
    for heading in (
        "## `-khia`",
        "## `-khiat`",
        "## `-khiat-na`",
        "## `-toh`",
        "## `-toh-na`",
        "## `-lam`",
        "## `-sawn`",
        "## `-suk`",
        "## `-lut`",
        "## `-phei`",
        "## `-cip`",
        "## `-tang`",
    ):
        assert heading in text


def test_directionals_dictionary_slice_treats_khia_as_outward() -> None:
    text = _text()
    assert "pokhia" in text
    assert "outward direction" in text or "outward motion" in text


def test_directionals_dictionary_slice_treats_khiat_with_caveated_away_evidence() -> None:
    text = _text()
    assert "nawhkhiat" in text
    assert "away anchor" in text or "away directional suffix" in text
    assert "analyzer-label caveat" in text


def test_directionals_dictionary_slice_treats_khiat_na_as_nominalized_boundary_material() -> None:
    text = _text()
    assert "hotkhiatna" in text
    assert "`-khiat-na`" in text
    assert "nominalized boundary material" in text


def test_directionals_dictionary_slice_treats_toh_as_upward_with_overlap_caveat() -> None:
    text = _text()
    assert "kilaktoh" in text
    assert "upward `-toh`" in text
    assert "polysemous" in text
    assert "comitative/accompany caveat" in text


def test_directionals_dictionary_slice_blocks_paitoh_as_comitative_overlap() -> None:
    text = _text()
    assert "paitoh" in text
    assert "go-accompany" in text
    assert "not upward-directional evidence" in text


def test_directionals_dictionary_slice_treats_toh_na_as_nominalized_boundary_material() -> None:
    text = _text()
    assert "kahtohna" in text
    assert "`-toh-na`" in text
    assert "nominalized boundary material" in text


def test_directionals_dictionary_slice_keeps_lam_as_boundary_material() -> None:
    text = _text()
    assert "tawplam" in text
    assert "direction/side/manner boundary material" in text


def test_directionals_dictionary_slice_treats_sawn_cautiously() -> None:
    text = _text()
    assert "piasawn" in text
    assert "cautious toward `-sawn`" in text


def test_directionals_dictionary_slice_treats_suk_as_corpus_backed() -> None:
    text = _text()
    assert "paisuk" in text
    assert "corpus-backed downward `-suk`" in text
    assert "rather than analyzer inventory alone" in text


def test_directionals_dictionary_slice_defers_lut_phei_cip_and_tang() -> None:
    text = _text()
    for form in ("uilut", "paiphei", "`Cip`", "`Tang`"):
        assert form in text
    assert "deferred / not print-ready" in text


def test_directionals_dictionary_slice_avoids_raw_count_claims() -> None:
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


def test_directionals_dictionary_slice_sets_review_notes_as_next_step() -> None:
    text = _text()
    assert "review_notes_directionals.md" in text
    assert "review-note work has not yet begun" in text


def test_directionals_dictionary_slice_keeps_broader_work_deferred() -> None:
    text = _text()
    assert "TAM" in text
    assert "Chrestomathy" in text
    assert "Mizo/lus" in text
    assert "other Kuki-Chin language work remain out of scope" in text
