from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "output/publication_review/candidates_case_marking.tsv"
DOSSIER_PATH = ROOT / "output/publication_review/dossier_case_marking.md"
GRAMMAR_PATH = ROOT / "output/publication_review/grammar_case_marking_print_slice.md"
DICTIONARY_PATH = ROOT / "output/publication_review/dictionary_case_markers_print_slice.md"
PROGRESS_PATH = ROOT / "PROGRESS.md"

REQUIRED_COLUMNS = {
    "candidate_id",
    "topic",
    "construction_id",
    "marker",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
}


def load_candidates():
    with CANDIDATES_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        rows = list(reader)
    return reader.fieldnames, rows


def test_case_marking_candidates_file_exists_with_required_columns():
    header, rows = load_candidates()

    assert CANDIDATES_PATH.exists()
    assert set(header) == REQUIRED_COLUMNS
    assert rows
    assert {row["topic"] for row in rows} == {"case_marking"}


def test_case_marking_candidates_cover_required_marker_types():
    _, rows = load_candidates()

    acceptedish = {"accepted", "accepted_with_caveat"}
    assert any(
        row["marker"] == "in"
        and row["construction_type"] == "ergative_agent"
        and row["candidate_status"] in acceptedish
        for row in rows
    )
    assert any(
        row["marker"] == "ah"
        and row["construction_type"] == "locative_place"
        and row["candidate_status"] in acceptedish
        for row in rows
    )
    assert any(
        row["marker"] == "pan"
        and row["candidate_status"] in acceptedish
        for row in rows
    )
    assert any(
        row["marker"] == "panin"
        and row["candidate_status"] in acceptedish
        for row in rows
    )
    assert any(
        row["marker"] == "tawh"
        and row["candidate_status"] in acceptedish
        for row in rows
    )
    assert any(
        row["marker"] == "relator_noun_plus_case"
        and row["candidate_status"] in acceptedish
        for row in rows
    )


def test_case_marking_includes_in_ambiguity_and_tawh_split():
    _, rows = load_candidates()

    in_rows = [row for row in rows if row["marker"] == "in"]
    assert any(
        row["construction_type"] == "ergative_agent" and row["candidate_status"] == "accepted"
        for row in in_rows
    )
    assert any(
        row["candidate_status"] in {"needs_review", "excluded"}
        and row["construction_type"] in {"ambiguous_homograph", "analyzer_noise", "review_needed"}
        for row in in_rows
    )

    tawh_rows = [row for row in rows if row["marker"] == "tawh"]
    assert any(row["construction_type"] == "comitative_accompaniment" for row in tawh_rows)
    assert any(row["construction_type"] == "material_or_instrumental_extension" for row in tawh_rows)


def test_case_marking_keeps_panin_conservative_and_relators_distinct():
    _, rows = load_candidates()

    panin_row = next(row for row in rows if row["marker"] == "panin")
    assert panin_row["candidate_status"] == "accepted_with_caveat"
    assert panin_row["print_status"] == "print_usable_with_caveat"
    assert "conservative" in panin_row["notes"].lower() or "without forcing" in panin_row["notes"].lower()

    relator_rows = [row for row in rows if row["marker"] == "relator_noun_plus_case"]
    assert relator_rows
    assert all(row["construction_type"] == "relator_noun_spatial" for row in relator_rows)
    assert all("relator" in row["notes"].lower() for row in relator_rows)

    a_row = next(row for row in rows if row["marker"] == "a")
    assert a_row["candidate_status"] == "deferred"
    assert a_row["print_status"] == "blocked"
    assert "does not cleanly separate" in a_row["why_excluded"].lower()


def test_case_marking_slice_files_remain_stable_and_progress_mentions_untracked_stem_audit():
    grammar_text = GRAMMAR_PATH.read_text(encoding="utf-8")
    dictionary_text = DICTIONARY_PATH.read_text(encoding="utf-8")
    progress_text = PROGRESS_PATH.read_text(encoding="utf-8")

    for needle in ["Kain in", "laizangah", "lakpan", "inn panin", "kei tawh", "leivui tawh"]:
        assert needle in grammar_text or needle in dictionary_text

    assert "generated locally and intentionally untracked" in progress_text
    assert "`stem_alternation_environment_summary.tsv`, `stem_alternation_pair_summary.tsv`, and `stem_alternation_example_matrix.tsv`" in progress_text
    assert "stem_alternation_corpus_audit.tsv` is generated locally and intentionally untracked" in progress_text


def test_case_marking_dossier_exists_and_describes_manual_candidate_layer():
    text = DOSSIER_PATH.read_text(encoding="utf-8")

    assert DOSSIER_PATH.exists()
    assert "candidates_case_marking.tsv" in text
    assert "manually curated analyzer-aware candidate layer" in text
    assert "not" in text.lower() and "supported extractor topic" in text.lower()
    assert "`case_marking`" in text


def test_case_marking_dossier_routes_key_claims_conservatively():
    text = DOSSIER_PATH.read_text(encoding="utf-8")
    lower_text = text.lower()

    assert "Kain in" in text
    assert "Genesis 4:3" in text
    assert "ciangin" in text
    assert "ambiguity-control row" in lower_text
    assert "not as a case example" in lower_text

    assert "`-a`" in text
    assert "deferred" in lower_text
    assert "does **not** promote `-a`" in text or "do **not** promote `-a`" in text

    assert "panin" in lower_text
    assert "print-usable with caveat" in lower_text
    assert "not the final structural analysis" in lower_text or "should not force a fully settled compositional analysis" in lower_text

    assert "accompaniment" in lower_text
    assert "material or instrumental" in lower_text or "material or means" in lower_text
    assert "plain noun-plus-locative" in lower_text
    assert "relator-noun-plus-case" in lower_text
    assert "pos_span=func" in lower_text
    assert "export limitation" in lower_text
