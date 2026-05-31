from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAMMAR_PATH = REPO_ROOT / "output" / "publication_review" / "grammar_noun_domain_print_slice.md"


def _text() -> str:
    return GRAMMAR_PATH.read_text(encoding="utf-8")


def test_noun_domain_print_slice_exists() -> None:
    assert GRAMMAR_PATH.exists(), "Noun-domain grammar slice must exist"


def test_noun_domain_print_slice_names_control_support_and_boundaries() -> None:
    text = _text()

    for required in (
        "candidates_noun_domain.tsv",
        "dossier_noun_domain_scope.md",
        "docs/grammar/reports/03-noun-01-simple.md",
        "docs/grammar/reports/03-noun-02-compounds.md",
        "docs/grammar/reports/03-noun-03-proper.md",
        "docs/grammar/compound_transparency_audit.md",
        "docs/grammar/opaque_lexemes.md",
        "review_notes_np_possession.md",
        "review_notes_nominalization.md",
        "review_notes_relators_postpositions.md",
        "review_notes_case_marking.md",
        "review_notes_pronouns.md",
    ):
        assert required in text


def test_noun_domain_print_slice_keeps_first_claim_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "gam" in text
    assert "main simple free noun stem anchor" in lower
    assert "gam-te" in text
    assert "gam-'" in text
    assert "gam-in" in text
    assert "gam-ah" in text
    assert "gam-te-ah" in text
    assert "aksi / aksi-te" in text
    assert "supporting plural row" in lower or "supporting plural evidence" in lower


def test_noun_domain_print_slice_keeps_boundary_material_outside() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "minam",
        "thugen",
        "singnai",
        "sanggam",
        "kholhna",
        "Abraham",
        "Topa",
        "lamethuai",
        "Topa' inn",
        "Pronoun-led possessors",
        "person-head material",
        "relator/postposition or case-dominated noun rows",
        "analyzer-noisy, report-only, or count-only noun-domain claims",
        "Any broad noun chapter claim",
    ):
        assert required in text

    assert "stay outside" in lower or "stays outside" in lower or "boundary material" in lower


def test_noun_domain_print_slice_stays_packet_narrow() -> None:
    text = _text()
    lower = text.lower()

    assert "not a full noun chapter" in lower
    assert "not a compound-noun chapter" in lower
    assert "not a proper-noun chapter" in lower
    assert "not a dictionary slice" in lower
    assert "dictionary slice now exists" not in lower
    assert "no dictionary slice exists" in lower
