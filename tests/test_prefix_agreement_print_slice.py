from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_prefix_agreement_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_prefix_agreement_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Prefix / agreement grammar slice must exist"


def test_prefix_agreement_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_prefix_agreement.tsv",
        "dossier_prefix_agreement_scope.md",
        "docs/grammar/reports/05-verb-03-agreement.md",
        "docs/grammar/reports/04-np-07-possession.md",
        "docs/grammar/morphemes/01-prefixes.md",
        "docs/grammar/lit-reviews/04-np-07-possession-lit.md",
        "docs/grammar/DISAMBIGUATION.md",
        "tests/test_prefix_agr_poss.py",
        "review_notes_pronouns.md",
        "review_notes_derivation_valency.md",
        "review_notes_vp_structure_stacking.md",
    ):
        assert required in text


def test_prefix_agreement_print_slice_keeps_routing_claim_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "kanei" in text
    assert "verbal agreement anchor" in lower
    assert "kainn" in text
    assert "possessive-routing anchor" in lower
    assert "ka-nei" in text
    assert "1SG-have" in text
    assert "ka-inn" in text
    assert "1SG.POSS-house" in text
    assert "agreement-versus-possession routing contrast" in lower


def test_prefix_agreement_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "ainn",
        "ipai",
        "hongmu",
        "kongmu",
        "kipan",
    ):
        assert required in text

    assert "stays outside" in lower or "stay outside" in lower or "boundary-only" in lower
    assert "apostrophe possession" in lower


def test_prefix_agreement_print_slice_stays_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full agreement chapter" in lower
    assert "not a full possession chapter" in lower
    assert "not a full object-prefix or inverse chapter" in lower
    assert "not a rewrite of the completed pronouns/clusivity packet" in lower
    assert "no dictionary slice exists yet for prefix/agreement" in lower
    assert "review notes rather than through a lexical headword layer" in lower
    assert "review notes rather than to a dictionary slice" in lower
    assert "dictionary slice now exists" not in lower
