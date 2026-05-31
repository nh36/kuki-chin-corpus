from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = REPO_ROOT / "output" / "publication_review" / "grammar_np_possession_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_np_possession_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "NP structure / possession grammar slice must exist"


def test_np_possession_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_np_possession.tsv",
        "dossier_np_possession_scope.md",
        "docs/grammar/reports/03-noun-06-np-structure.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "review_notes_prefix_agreement.md",
        "review_notes_pronouns.md",
        "review_notes_case_marking.md",
        "review_notes_relators_postpositions.md",
        "review_notes_nominalization.md",
        "tests/test_prefix_agr_poss.py",
    ):
        assert required in text


def test_np_possession_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "hih mite" in text
    assert "demonstrative-before-noun anchor" in lower
    assert "mi khat" in text
    assert "head-noun plus numeral anchor" in lower
    assert "mi khempeuh" in text
    assert "head-noun plus quantifier anchor" in lower
    assert "hih mi-te" in text
    assert "PROX person-PL" in text
    assert "person one" in text
    assert "mi khem-peuh" in text
    assert "person all" in text


def test_np_possession_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "ka pa",
        "Topa' inn",
        "a pa' inn",
        "Topa' tungah",
        "ka suahna leitang",
        "isolated `a`, `ka`, or `na` prefix surfaces",
        "amah a pa",
        "`-á`",
        "report-only counts",
        "broad recursive possession chapter claim",
    ):
        assert required in text

    assert "stay outside" in lower or "stays outside" in lower or "boundary material" in lower


def test_np_possession_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full noun-phrase chapter" in lower
    assert "not a full possession chapter" in lower
    assert "not a full prefix/agreement chapter" in lower
    assert "not a full case or relator chapter" in lower
    assert "review notes rather than a dictionary slice" in lower
    assert "dictionary slice now exists" not in lower
    assert "review-note slices already exist" not in lower
