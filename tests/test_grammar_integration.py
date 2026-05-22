"""
Tests for the Tedim grammar integration layer.

These checks keep grammar-drafting outputs conservative when the backend
contains ambiguous or incomplete example links.
"""

import os
import sys
import sqlite3
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from grammar_integration import audit_examples_for_entry, load_source_map, select_examples_for_entry
from generate_grammar_integration_report import generate_report


DB_PATH = Path(__file__).resolve().parent.parent / 'data' / 'ctd_backend.db'
SOURCE_MAP_PATH = Path(__file__).resolve().parent.parent / 'docs' / 'grammar' / 'grammar_source_map.json'


@pytest.fixture
def conn():
    """Open the production Tedim backend for integration checks."""
    if not DB_PATH.exists():
        pytest.skip("Backend database not found - run 'make backend' first")
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def source_map():
    """Load the Tedim grammar source map."""
    return load_source_map(SOURCE_MAP_PATH)


def get_entry(source_map, topic_id):
    """Return one topic mapping by ID."""
    return next(entry for entry in source_map['topic_mappings'] if entry['topic_id'] == topic_id)


def test_ergative_marking_refuses_unsafe_examples(conn, source_map):
    """Ergative output should not surface misleading -in examples as draft-safe."""
    entry = get_entry(source_map, 'ergative-marking')
    safe = select_examples_for_entry(conn, entry, limit=2)
    reviewed = select_examples_for_entry(conn, entry, limit=2, include_non_safe=True)

    assert safe == []
    assert reviewed
    assert all(example['selection_status'] == 'rejected' for example in reviewed)


def test_comitative_marking_selects_plain_tawh(conn, source_map):
    """Comitative output should prefer bare COM examples over ki-tawh reflexives."""
    entry = get_entry(source_map, 'comitative-marking')
    safe = select_examples_for_entry(conn, entry, limit=2)

    assert safe
    assert all(example['morpheme_id'] == 'tawh.COM.case_marker' for example in safe)
    assert all(example['segmented'] == 'tawh' for example in safe)
    assert all(example['glossed'] == 'COM' for example in safe)


def test_declarative_hi_excludes_decl_poss_examples(conn, source_map):
    """Declarative hi should refuse DECL.POSS rows rather than mislabel them as DECL."""
    entry = get_entry(source_map, 'declarative-hi')
    safe = select_examples_for_entry(conn, entry, limit=2)
    reviewed = select_examples_for_entry(conn, entry, limit=2, include_non_safe=True)

    assert safe == []
    assert reviewed
    assert all(example['selection_status'] == 'rejected' for example in reviewed)


def test_pronominal_prefixes_distinguish_agreement_and_possession(conn, source_map):
    """The topic-level selector should keep a- agreement and possessive a separate."""
    entry = get_entry(source_map, 'pronominal-prefixes')
    safe = select_examples_for_entry(conn, entry, limit=2)

    morpheme_ids = {example['morpheme_id'] for example in safe}
    assert 'a.3SG.pronominal_prefix' in morpheme_ids
    assert 'a.3SG.POSS.function_word' in morpheme_ids


def test_benefactive_sak_stays_out_of_safe_drafting_examples(conn, source_map):
    """Benefactive -sak should stay out of drafting output until the backend distinguishes it."""
    entry = get_entry(source_map, 'benefactive-sak')
    safe = select_examples_for_entry(conn, entry, limit=2)
    reviewed = select_examples_for_entry(conn, entry, limit=2, include_non_safe=True)

    assert safe == []
    assert reviewed
    assert all(example['selection_status'] == 'fallback only' for example in reviewed)
    assert all(example['matched_fields'] == ['fallback text search'] for example in reviewed)


def test_directionals_reject_tuni_in_and_keep_it_out_of_drafting(conn, source_map):
    """Directional selection should reject Tuni-in and keep only directional suffix examples."""
    entry = get_entry(source_map, 'directional-suffixes')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=3)

    assert safe
    assert all(example['segmented'] != 'Tuni-in' for example in safe)
    assert all(example['drafting_quality'] in {'exemplar', 'usable'} for example in safe)
    assert any(example['selection_status'] == 'rejected' and example['segmented'] == 'Tuni-in' for example in audit)


def test_nominalization_prefers_nuntak_na(conn, source_map):
    """Nominalization should keep productive-looking -na and reject pa-na."""
    entry = get_entry(source_map, 'nominalization-na')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=3)

    assert [example['segmented'] for example in safe] == ['nuntak-na']
    assert any(example['selection_status'] == 'rejected' and example['segmented'] == 'pa-na' for example in audit)


def test_interrogative_hiam_excludes_formulaic_reason_expression(conn, source_map):
    """Interrogative hiam should keep ordinary questions and reject Bang hang hiam formulas."""
    entry = get_entry(source_map, 'interrogative-hiam')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=3)

    assert safe
    assert all('Bang hang hiam ci' not in example['tedim_text'] for example in safe)
    assert any(example['selection_status'] == 'rejected' for example in audit)


def test_ability_prefers_transparent_abilitative_examples(conn, source_map):
    """Ability examples should prefer transparent mu-/pau-thei rows over opaque cithei forms."""
    entry = get_entry(source_map, 'ability-thei-theih')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=4)

    assert {example['segmented'] for example in safe} == {'mu-thei-in', 'pau-thei-in'}
    assert any(example['drafting_quality'] == 'safe_but_poor' for example in audit)
    assert all(example['segmented'] != 'ci-thei-sak-kik' for example in safe)


def test_topic_marker_pen_keeps_bad_backend_rows_out_of_drafting(conn, source_map):
    """Topic marker pen should show rejected linked rows and no draft-ready example yet."""
    entry = get_entry(source_map, 'topic-marker-pen')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=3)

    assert safe == []
    assert any(example['selection_status'] == 'rejected' for example in audit)
    assert any(example['selection_status'] == 'fallback only' for example in audit)


def test_agentive_prefers_clear_agent_nominalization(conn, source_map):
    """Agent nominalization should use tax-collector AGT examples, not fallback Genesis rows."""
    entry = get_entry(source_map, 'agentive-pa-mi')
    safe = select_examples_for_entry(conn, entry, limit=2)
    audit = audit_examples_for_entry(conn, entry, limit=4)

    assert safe
    assert safe[0]['segmented'] == 'siah-dong-pa'
    assert safe[0]['drafting_quality'] == 'exemplar'
    assert all(example['source_id'] != '01001001' for example in safe)
    assert any(example['selection_status'] == 'rejected' for example in audit)


def test_integration_report_declares_source_map_canonical(tmp_path):
    """When backend topic tables are empty, the report should name the source map as canonical."""
    output_path = tmp_path / 'integration_report.md'
    content = generate_report(str(DB_PATH), str(SOURCE_MAP_PATH), output_path)

    assert 'Canonical topic/construction layer' in content
    assert 'docs/grammar/grammar_source_map.json' in content
    assert 'schema placeholders' in content
