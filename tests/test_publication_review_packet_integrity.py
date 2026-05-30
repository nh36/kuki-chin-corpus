import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_REVIEW_DIR = REPO_ROOT / "output" / "publication_review"
HANDOFF_PATH = PUBLICATION_REVIEW_DIR / "human_review_handoff.md"

EXPECTED_TOPICS = {
    "demonstratives/deixis",
    "negation",
    "pronouns/clusivity",
    "stem alternation",
    "case marking",
    "interrogatives",
    "numerals",
    "quantifiers",
    "coordinators",
    "sentence-final particles",
}

EXPECTED_CANDIDATE_FILES = {
    "candidates_demonstratives.tsv",
    "candidates_negation.tsv",
    "candidates_pronouns.tsv",
    "candidates_stem_alternation.tsv",
    "candidates_case_marking.tsv",
    "candidates_interrogatives.tsv",
    "candidates_numerals.tsv",
    "candidates_quantifiers.tsv",
    "candidates_coordinators.tsv",
    "candidates_sentence_final_particles.tsv",
}

RETROFIT_SEQUENCE_REVIEW_NOTES = {
    "review_notes_numerals.md",
    "review_notes_quantifiers.md",
    "review_notes_coordinators.md",
    "review_notes_sentence_final_particles.md",
}

FORBIDDEN_NEW_PACKET_FILES = {
    "candidates_tam.tsv",
    "dossier_tam.md",
    "grammar_tam_print_slice.md",
    "dictionary_tam_print_slice.md",
    "review_notes_tam.md",
    "candidates_directionals.tsv",
    "dossier_directionals.md",
    "grammar_directionals_print_slice.md",
    "dictionary_directionals_print_slice.md",
    "review_notes_directionals.md",
}


def _parse_review_ready_table():
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    rows = {}
    capture = False

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if line == "# Review-ready packets":
            capture = True
            continue

        if capture and line.startswith("# ") and line != "# Review-ready packets":
            break

        if not capture or not line.startswith("|"):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or cells[0] in {"Topic", "---"}:
            continue

        topic, candidate, dossier, grammar, dictionary, review_notes = cells[:6]
        rows[topic] = {
            "candidate": re.findall(r"`([^`]+)`", candidate),
            "dossier": re.findall(r"`([^`]+)`", dossier),
            "grammar": re.findall(r"`([^`]+)`", grammar),
            "dictionary": re.findall(r"`([^`]+)`", dictionary),
            "review_notes": re.findall(r"`([^`]+)`", review_notes),
        }

    return rows


def test_handoff_review_ready_packets_are_file_backed():
    rows = _parse_review_ready_table()

    assert set(rows) == EXPECTED_TOPICS

    for topic, surfaces in rows.items():
        assert surfaces["candidate"], f"{topic} is missing a candidate TSV in the handoff table"
        assert surfaces["dossier"], f"{topic} is missing a dossier entry in the handoff table"
        assert surfaces["grammar"], f"{topic} is missing a grammar slice in the handoff table"
        assert surfaces["dictionary"], f"{topic} is missing a dictionary slice in the handoff table"
        assert surfaces["review_notes"], f"{topic} is missing review notes in the handoff table"

        for filenames in surfaces.values():
            for filename in filenames:
                assert (PUBLICATION_REVIEW_DIR / filename).exists(), f"Missing file listed in handoff: {filename}"


def test_candidate_tsvs_exist_for_all_candidate_first_packets():
    for filename in EXPECTED_CANDIDATE_FILES:
        assert (PUBLICATION_REVIEW_DIR / filename).exists()


def test_retrofit_sequence_review_notes_exist():
    for filename in RETROFIT_SEQUENCE_REVIEW_NOTES:
        assert (PUBLICATION_REVIEW_DIR / filename).exists()


def test_handoff_keeps_next_action_as_human_review():
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    assert "No further narrow publication-review packet should be started automatically." in text
    assert "The next substantive action should be human review of the completed packets." in text
    assert "select one new scope explicitly" in text


def test_handoff_keeps_deferred_scopes_deferred():
    text = HANDOFF_PATH.read_text(encoding="utf-8")

    for required in (
        "broad TAM / aspect / modal",
        "directionals",
        "relators/postpositions as a separate packet",
        "chrestomathy",
        "Mizo/lus",
        "other Kuki-Chin languages",
    ):
        assert required in text


def test_no_new_tam_or_directionals_packet_files_exist():
    for filename in FORBIDDEN_NEW_PACKET_FILES:
        assert not (PUBLICATION_REVIEW_DIR / filename).exists()
