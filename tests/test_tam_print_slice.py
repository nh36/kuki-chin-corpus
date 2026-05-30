from pathlib import Path


SLICE_PATH = Path(__file__).resolve().parents[1] / "output/publication_review/grammar_tam_print_slice.md"


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_tam_print_slice_exists_and_names_controlling_evidence() -> None:
    text = _text()

    assert SLICE_PATH.exists()
    assert "candidates_tam.tsv" in text
    assert "dossier_tam_scope.md" in text
    assert "controlled by `candidates_tam.tsv` and `dossier_tam_scope.md`" in text
    assert "It is not a full TAM chapter." in text


def test_tam_print_slice_limits_first_slice_anchors_to_selected_compact_forms() -> None:
    text = _text()

    for required in (
        "paingei",
        "neigige",
        "paizel",
        "kilawmta",
        "bawlzo",
        "hongpaikik",
        "omding",
        "bawlthei",
    ):
        assert required in text

    assert "The first-slice TAM anchors are limited to `-ngei`, `-gige`, `-zel`, `-ta`, `-zo`, `-kik`, `-ding`, and `-thei`" in text


def test_tam_print_slice_keeps_required_caveats_explicit() -> None:
    text = _text()
    lower = text.lower()

    assert "broader continuative aspect" in lower
    assert "construction-controlled" in lower
    assert "sentence-final overlap caveat" in lower
    assert "bare `zo`" in text
    assert "motion/return chapter" in lower
    assert "dingin and clause-bound caveat" in lower
    assert "negation/irrealis-stack caveat" in lower
    assert "khiathei ding om lo" in text


def test_tam_print_slice_keeps_overlap_and_deferred_material_out_of_scope() -> None:
    text = _text()
    lower = text.lower()

    for required in (
        "pailai",
        "dingin",
        "khiathei ding om lo",
        "mangngilh ta hi",
        "khia-ta",
        "bawlzoding",
        "bawlsakthei",
        "`-nawn`",
        "`-khin`",
    ):
        assert required in text

    assert "remain out of this first grammar slice" in lower


def test_tam_print_slice_does_not_claim_later_tam_surfaces_exist() -> None:
    text = _text()
    lower = text.lower()

    assert "dictionary slice now exists" in lower
    assert "review-note work has not yet begun" in lower
    assert "review notes now exist" not in lower
