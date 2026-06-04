from pathlib import Path


SLICE_PATH = Path("output/publication_review/grammar_directionals_print_slice.md")


def _text() -> str:
    return SLICE_PATH.read_text(encoding="utf-8")


def test_directionals_print_slice_exists() -> None:
    assert SLICE_PATH.exists(), "directionals grammar print slice must exist"


def test_directionals_print_slice_keeps_grammar_facing_directional_coverage() -> None:
    text = _text()

    for required in (
        "Overview of directional expressions",
        "Current directional inventory",
        "Outward and away direction",
        "Upward direction and directionals in the verb phrase",
        "Toward direction with `-sawn`",
        "Downward direction with `-suk`",
        "Deictic boundary",
        "TAM and VP-structure boundary",
        "Several issues remain outside the present account.",
    ):
        assert required in text


def test_directionals_print_slice_keeps_main_anchors_and_boundaries_visible() -> None:
    text = _text()

    for required in (
        "pokhia",
        "nawhkhiat",
        "hotkhiatna",
        "kilaktoh",
        "kahtohna",
        "paitoh",
        "piasawn",
        "paisuk",
        "tawplam",
    ):
        assert required in text
