from pathlib import Path


REPORT_PATH = Path(__file__).resolve().parents[1] / "docs/grammar/reports/06-func-01-pronouns.md"


def test_pronoun_report_uses_partial_clusivity_correction():
    text = REPORT_PATH.read_text()

    for banned in (
        "kote (INCL)",
        "eite (EXCL)",
        "inclusive (kote)",
        "exclusive (eite)",
    ):
        assert banned not in text

    assert "`kote` as exclusive" in text
    assert "`eite` as a first-person plural form still needing further clusivity review" in text
