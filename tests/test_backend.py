"""
Backend-native tests for the Tedim SQLite backend.

These checks stay focused on the backend API and schema that this branch
actually owns. They intentionally do not require unrelated metrics,
dictionary-draft, or example-linking pipeline modules.
"""

import os
import re
import sys
import tempfile

import pytest

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from backend import (
    Backend,
    Example,
    EXAMPLE_QUALITY_ORDER,
    GrammaticalMorpheme,
    Lemma,
    QUALITY_ORDER_SQL,
    Sense,
)


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ctd_backend.db')


@pytest.fixture
def backend():
    """Provide access to the production backend database."""
    if not os.path.exists(DB_PATH):
        pytest.skip("Backend database not found - run 'make backend' first")
    return Backend(DB_PATH)


@pytest.fixture
def temp_backend():
    """Provide a fresh temporary backend for isolated API tests."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_path = f.name
    try:
        db = Backend(temp_path)
        yield db
    finally:
        os.unlink(temp_path)


class TestMigration:
    """Tests for backend migration integrity."""

    def test_all_tables_exist(self, backend):
        expected_tables = [
            'languages', 'sources', 'tokens', 'wordforms', 'lemmas',
            'senses', 'grammatical_morphemes', 'examples',
            'constructions', 'grammar_topics', 'review_queue', 'provenance',
        ]

        with backend._connection() as conn:
            tables = [row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )]

        for table in expected_tables:
            assert table in tables, f"Missing table: {table}"

    def test_required_indexes_exist(self, backend):
        expected_indexes = [
            'idx_tokens_source', 'idx_tokens_wordform', 'idx_wordforms_lemma',
            'idx_senses_lemma', 'idx_examples_sense', 'idx_examples_morpheme',
        ]

        with backend._connection() as conn:
            indexes = [row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            )]

        for idx in expected_indexes:
            assert idx in indexes, f"Missing index: {idx}"

    def test_foreign_key_sanity(self, backend):
        with backend._connection() as conn:
            orphan_wordforms = conn.execute('''
                SELECT COUNT(*) FROM wordforms w
                WHERE w.lemma_id IS NOT NULL
                  AND w.lemma_id != ''
                  AND NOT EXISTS (
                      SELECT 1 FROM lemmas l WHERE l.lemma_id = w.lemma_id
                  )
            ''').fetchone()[0]

            orphan_examples = conn.execute('''
                SELECT COUNT(*) FROM examples e
                WHERE e.sense_id IS NOT NULL
                  AND e.sense_id != ''
                  AND NOT EXISTS (
                      SELECT 1 FROM senses s WHERE s.sense_id = e.sense_id
                  )
            ''').fetchone()[0]

            total_sense_linked = conn.execute('''
                SELECT COUNT(*) FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
            ''').fetchone()[0]

        assert orphan_wordforms < 1000
        orphan_rate = orphan_examples / total_sense_linked if total_sense_linked else 0
        assert orphan_rate < 0.05


class TestTableCounts:
    """Tests for stable backend size ranges."""

    def test_counts_within_expected_ranges(self, backend):
        ranges = {
            'sources': (30000, 31000),
            'tokens': (820000, 840000),
            'wordforms': (20000, 21500),
            'lemmas': (7000, 7600),
            'senses': (9500, 10250),
            'grammatical_morphemes': (450, 550),
            'examples': (21000, 23000),
        }

        with backend._connection() as conn:
            for table, (minimum, maximum) in ranges.items():
                count = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]
                assert minimum <= count <= maximum, (
                    f"{table} count {count} outside expected range {minimum}-{maximum}"
                )

    def test_optional_construction_tables_may_be_empty(self, backend):
        with backend._connection() as conn:
            constructions = conn.execute(
                'SELECT COUNT(*) FROM constructions'
            ).fetchone()[0]
            topics = conn.execute(
                'SELECT COUNT(*) FROM grammar_topics'
            ).fetchone()[0]

        assert constructions >= 0
        assert topics >= 0


class TestLookupBehavior:
    """Tests for core lookup behavior."""

    def test_get_lemma_exists(self, backend):
        lemma = backend.get_lemma('pai')
        assert lemma is not None
        assert lemma.lemma_id == 'pai'
        assert lemma.pos in ('V', 'FUNC', 'N')

    def test_get_lemma_not_exists(self, backend):
        assert backend.get_lemma('xyznonexistent') is None

    def test_get_senses_for_lemma(self, backend):
        senses = backend.get_senses('pai')
        assert senses
        assert all(isinstance(sense, Sense) for sense in senses)
        assert all(sense.lemma_id == 'pai' for sense in senses)

    def test_polysemous_hi_has_decl_sense(self, backend):
        senses = backend.get_senses('hi')
        glosses = {sense.gloss for sense in senses}
        assert 'DECL' in glosses

    def test_get_morpheme_by_form_finds_ergative_in(self, backend):
        morphemes = backend.get_morpheme_by_form('in')
        assert morphemes
        assert any(
            morpheme.gloss == 'ERG' and morpheme.category == 'case_marker'
            for morpheme in morphemes
        )

    def test_high_frequency_lexical_lemmas_have_examples(self, backend):
        high_freq_lexical = ['tua', 'le', 'mi', 'ci', 'amah']

        with backend._connection() as conn:
            for lemma_id in high_freq_lexical:
                count = conn.execute('''
                    SELECT COUNT(*) FROM examples e
                    JOIN senses s ON e.sense_id = s.sense_id
                    WHERE s.lemma_id = ?
                ''', (lemma_id,)).fetchone()[0]
                assert count > 0, f"High-frequency lemma '{lemma_id}' has no examples"


class TestExampleQualityOrdering:
    """Tests for canonical example quality ordering."""

    def test_quality_constant_contains_expected_levels(self):
        assert EXAMPLE_QUALITY_ORDER == [
            'canonical',
            'excellent',
            'good',
            'transparent',
            'shortest',
            'acceptable',
            'auto',
            'additional',
        ]

    def test_quality_order_sql_matches_constant(self):
        matches = re.findall(r"WHEN '([^']+)' THEN (\d+)", QUALITY_ORDER_SQL)
        order_map = {quality: int(rank) for quality, rank in matches}

        for rank, quality in enumerate(EXAMPLE_QUALITY_ORDER, start=1):
            assert order_map[quality] == rank

    def test_existing_example_qualities_are_known(self, backend):
        valid = set(EXAMPLE_QUALITY_ORDER)

        with backend._connection() as conn:
            qualities = [
                row[0]
                for row in conn.execute(
                    "SELECT DISTINCT quality FROM examples WHERE quality IS NOT NULL"
                )
            ]

        for quality in qualities:
            assert quality in valid, f"Unknown quality value: {quality}"

    def test_temp_backend_orders_sense_examples_by_quality(self, temp_backend):
        temp_backend.add_lemma(Lemma(
            lemma_id='test',
            citation_form='test',
            pos='V',
            entry_type='lexical',
            primary_gloss='test',
        ))
        temp_backend.add_sense(Sense(
            sense_id='test.1',
            lemma_id='test',
            sense_num=1,
            pos='V',
            gloss='TEST',
        ))

        temp_backend.add_example(Example(
            example_id=0,
            source_id='s1',
            sense_id='test.1',
            tedim_text='late',
            quality='additional',
        ))
        temp_backend.add_example(Example(
            example_id=0,
            source_id='s2',
            sense_id='test.1',
            tedim_text='best',
            quality='canonical',
        ))
        temp_backend.add_example(Example(
            example_id=0,
            source_id='s3',
            sense_id='test.1',
            tedim_text='mid',
            quality='transparent',
        ))

        examples = temp_backend.get_examples_for_sense('test.1', limit=10)
        assert [example.quality for example in examples] == [
            'canonical', 'transparent', 'additional'
        ]

    def test_temp_backend_orders_morpheme_examples_by_quality(self, temp_backend):
        temp_backend.add_grammatical_morpheme(GrammaticalMorpheme(
            morpheme_id='test.MORPH',
            form='test',
            gloss='TST',
            function='test morpheme',
            category='particle',
        ))

        temp_backend.add_example(Example(
            example_id=0,
            source_id='s1',
            morpheme_id='test.MORPH',
            tedim_text='late',
            quality='additional',
        ))
        temp_backend.add_example(Example(
            example_id=0,
            source_id='s2',
            morpheme_id='test.MORPH',
            tedim_text='good',
            quality='good',
        ))
        temp_backend.add_example(Example(
            example_id=0,
            source_id='s3',
            morpheme_id='test.MORPH',
            tedim_text='best',
            quality='canonical',
        ))

        examples = temp_backend.get_examples_for_morpheme('test.MORPH', limit=10)
        assert [example.quality for example in examples] == [
            'canonical', 'good', 'additional'
        ]


class TestBackendStatistics:
    """Tests for backend summary statistics."""

    def test_stats_cover_core_tables(self, backend):
        stats = backend.get_stats()

        for key in [
            'sources', 'tokens', 'wordforms', 'lemmas',
            'senses', 'grammatical_morphemes', 'examples',
            'review_open', 'review_resolved',
        ]:
            assert key in stats
            assert stats[key] >= 0
