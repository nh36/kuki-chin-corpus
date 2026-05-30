from pathlib import Path


DOSSIER_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/dossier_directionals.md"


def test_directionals_dossier_exists_and_keeps_candidate_layer_controlling() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert DOSSIER_PATH.exists()
    assert "candidates_directionals.tsv" in text
    assert "Candidate rows, not raw suffix searches and not generated-report counts, control the dossier." in text
    assert "does **not** search every word ending in `khia`, `khiat`, `toh`, `lam`, `sawn`, `lut`, `suk`, `phei`, `cip`, or `tang`" in text


def test_directionals_dossier_keeps_khia_khiat_and_nominalized_khiat_narrow() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "`pokhia`" in text
    assert "outward `-khia`" in text or "-khia` can mark outward motion or direction" in text
    assert "`nawhkhiat`" in text
    assert "away-directional `-khiat`" in text or "away evidence" in text
    assert "`hotkhiatna`" in text
    assert "`-khiat-na`" in text
    assert "boundary evidence" in text


def test_directionals_dossier_keeps_toh_lam_and_sawn_caveated() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "`kilaktoh`" in text
    assert "upward `-toh`" in text
    assert "`kahtohna`" in text
    assert "`-toh-na`" in text
    assert "`paitoh`" in text
    assert "comitative/accompany" in text
    assert "not simply \"UP\" in all contexts" in text
    assert "`tawplam`" in text
    assert "`-lam`" in text
    assert "direction/side/manner boundary material" in text
    assert "`piasawn`" in text
    assert "`-sawn`" in text
    assert "construction-controlled" in text


def test_directionals_dossier_keeps_suk_and_deferred_forms_conservative() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert "`paisuk`" in text
    assert "`-suk`" in text
    assert "corpus-backed" in text
    assert "analyzer tests do support `-suk`" in text.lower()
    assert "corpus-backed candidate rows" in text
    for required in ("`uilut`", "`paiphei`", "`cip`", "`tang`"):
        assert required in text
    assert "`-lut`" in text
    assert "`-phei`" in text
    assert "`-cip`" in text
    assert "`-tang`" in text
    assert "deferred or blocked material" in text


def test_directionals_dossier_avoids_raw_counts_and_sets_next_step() -> None:
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    for banned in (
        "1,006",
        "180 for -khiat",
        "39 for -toh",
        "24 for -lam",
        "13 for -sawn",
        "zero-attestation",
        "zero attestations",
        "0-count",
    ):
        assert banned not in text

    assert "Grammar, dictionary, and review-note print slices for directionals have **not** yet begun." in text
    assert "grammar_directionals_print_slice.md" in text
    assert "dictionary_directionals_print_slice.md" in text
    assert "review_notes_directionals.md" in text
    assert "Broad TAM, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred." in text
