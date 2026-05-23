"""
Tests for Tedim sample dictionary draft generation.

These checks keep lexical sample outputs from surfacing obvious
grammatical, unknown-gloss, or review-only entries as draft-ready
dictionary material.
"""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from backend import Backend, Lemma
from generate_sample_entries_backend import generate_sample_entries, select_sample_lemmas


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ctd_backend.db')


@pytest.fixture
def backend():
    """Provide access to the production Tedim backend database."""
    if not os.path.exists(DB_PATH):
        pytest.skip("Backend database not found - run 'make backend' first")
    return Backend(DB_PATH)


@pytest.fixture
def temp_backend():
    """Provide an isolated backend for dictionary-generator unit tests."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_path = f.name
    try:
        db = Backend(temp_path)
        yield db
    finally:
        os.unlink(temp_path)


def add_lemma(
    db: Backend,
    lemma_id: str,
    pos: str,
    gloss: str,
    *,
    token_count: int,
    entry_type: str = 'lexical',
    needs_review: bool = False,
) -> None:
    """Insert a minimal lemma row for generator tests."""
    db.add_lemma(
        Lemma(
            lemma_id=lemma_id,
            citation_form=lemma_id,
            pos=pos,
            entry_type=entry_type,
            primary_gloss=gloss,
            token_count=token_count,
            form_count=1,
            needs_review=needs_review,
        )
    )


def test_lexical_noun_generation_excludes_unknown_gloss_entries(temp_backend):
    add_lemma(temp_backend, 'uh', 'N', '?', token_count=1000)
    add_lemma(temp_backend, 'mi', 'N', 'person', token_count=900)

    entries, audit = select_sample_lemmas(temp_backend, pos='N', limit=10)

    assert [entry.lemma_id for entry in entries] == ['mi']
    assert audit.skipped_unknown_gloss == 1


def test_lexical_verb_generation_excludes_empty_gloss_entries(temp_backend):
    add_lemma(temp_backend, 'ahi', 'V', '', token_count=1000)
    add_lemma(temp_backend, 'ci', 'V', 'say', token_count=900)

    entries, audit = select_sample_lemmas(temp_backend, pos='V', limit=10)

    assert [entry.lemma_id for entry in entries] == ['ci']
    assert audit.skipped_empty_gloss == 1


def test_lexical_generation_excludes_needs_review_by_default(temp_backend):
    add_lemma(temp_backend, 'pia', 'V', 'give', token_count=1000, needs_review=True)
    add_lemma(temp_backend, 'gen', 'V', 'speak', token_count=900)

    entries, audit = select_sample_lemmas(temp_backend, pos='V', limit=10)

    assert [entry.lemma_id for entry in entries] == ['gen']
    assert audit.skipped_needs_review == 1


def test_grammatical_entries_are_excluded_from_lexical_verb_samples(temp_backend):
    add_lemma(temp_backend, 'ding', 'V', 'IRR', token_count=1200, entry_type='grammatical', needs_review=True)
    add_lemma(temp_backend, 'ci', 'V', 'say', token_count=1000)

    lexical_entries, lexical_audit = select_sample_lemmas(temp_backend, pos='V', limit=10)
    grammatical_entries, grammatical_audit = select_sample_lemmas(
        temp_backend, entry_type='grammatical', limit=10
    )

    assert [entry.lemma_id for entry in lexical_entries] == ['ci']
    assert lexical_audit.skipped_entry_type_mismatch == 1
    assert [entry.lemma_id for entry in grammatical_entries] == ['ding']
    assert grammatical_audit.emitted == 1


def test_generated_sample_file_includes_audit_summary(temp_backend):
    add_lemma(temp_backend, 'uh', 'N', '?', token_count=1000)
    add_lemma(temp_backend, 'mi', 'N', 'person', token_count=900)

    lines = generate_sample_entries(temp_backend, pos='N', limit=10)
    content = '\n'.join(lines)

    assert "## Generation Audit" in content
    assert "Skipped for `?` primary_gloss" in content
    assert "Sample/draft output only" in content


def test_generated_grammatical_sample_includes_review_policy_note(temp_backend):
    add_lemma(
        temp_backend,
        'ding',
        'V',
        'IRR',
        token_count=1200,
        entry_type='grammatical',
        needs_review=True,
    )

    lines = generate_sample_entries(temp_backend, entry_type='grammatical', limit=10)
    content = '\n'.join(lines)

    assert "- **Include needs_review entries:** yes (grammatical sample policy)" in content
    assert "Grammatical samples include particles, pronouns, determiners, clitics, and other function items." in content
    assert "## ding" in content
    assert "⚠️ *Needs review*" in content


def test_uh_is_not_first_lexical_noun_entry_in_production_backend(backend):
    entries, _ = select_sample_lemmas(backend, pos='N', limit=10)

    assert entries
    assert entries[0].lemma_id != 'uh'
    assert all(entry.lemma_id != 'uh' for entry in entries)


def test_lexical_verb_sample_excludes_ding_hong_and_ahi_in_production_backend(backend):
    entries, _ = select_sample_lemmas(backend, pos='V', limit=20)
    entry_ids = {entry.lemma_id for entry in entries}

    assert 'ding' not in entry_ids
    assert 'hong' not in entry_ids
    assert 'ahi' not in entry_ids


def test_ding_routes_to_grammatical_sample_in_production_backend(backend):
    entries, _ = select_sample_lemmas(backend, entry_type='grammatical', limit=20)
    entry_ids = {entry.lemma_id for entry in entries}

    assert 'ding' in entry_ids


def test_production_grammatical_sample_header_matches_review_policy(backend):
    content = '\n'.join(generate_sample_entries(backend, entry_type='grammatical', limit=5))

    assert "- **Include needs_review entries:** yes (grammatical sample policy)" in content
