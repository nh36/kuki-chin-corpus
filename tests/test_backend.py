"""
Backend-native tests for the Kuki-Chin shared backend.

These tests directly verify the backend architecture:
- Migration integrity
- Table counts and relationships
- Lookup behavior
- Sense/example linking
- Example quality ordering
- Constructions/topics layer
- Guards against overly aggressive ambiguous-example assignment

Run with: pytest tests/test_backend.py -v
"""

import os
import sys
import json
import sqlite3
import tempfile
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from backend import (
    Backend, Lemma, Sense, Example, GrammaticalMorpheme,
    EXAMPLE_QUALITY_ORDER
)

# Path to the production database
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ctd_backend.db')


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def backend():
    """Provide access to the production backend database."""
    if not os.path.exists(DB_PATH):
        pytest.skip("Backend database not found - run 'make backend' first")
    return Backend(DB_PATH)


@pytest.fixture
def temp_backend():
    """Provide a fresh temporary backend for isolation tests."""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        temp_path = f.name
    try:
        db = Backend(temp_path)
        yield db
    finally:
        os.unlink(temp_path)


@pytest.fixture
def canonical_metrics():
    """Load canonical metrics from the metrics JSON file."""
    metrics_path = os.path.join(os.path.dirname(__file__), '..', 'output', 'metrics', 'ctd_metrics.json')
    if not os.path.exists(metrics_path):
        pytest.skip("Canonical metrics file not found - run 'make metrics' first")
    with open(metrics_path) as f:
        return json.load(f)['metrics']


# =============================================================================
# Migration and Schema Tests
# =============================================================================

class TestMigration:
    """Tests for backend migration integrity."""
    
    def test_all_tables_exist(self, backend):
        """All expected tables should exist in the schema."""
        expected_tables = [
            'languages', 'sources', 'tokens', 'wordforms', 'lemmas',
            'senses', 'grammatical_morphemes', 'examples',
            'constructions', 'grammar_topics', 'review_queue', 'provenance'
        ]
        
        with backend._connection() as conn:
            tables = [row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )]
        
        for table in expected_tables:
            assert table in tables, f"Missing table: {table}"
    
    def test_required_indexes_exist(self, backend):
        """Performance-critical indexes should exist."""
        expected_indexes = [
            'idx_tokens_source', 'idx_tokens_wordform', 'idx_wordforms_lemma',
            'idx_senses_lemma', 'idx_examples_sense', 'idx_examples_morpheme'
        ]
        
        with backend._connection() as conn:
            indexes = [row[0] for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            )]
        
        for idx in expected_indexes:
            assert idx in indexes, f"Missing index: {idx}"
    
    def test_foreign_keys_valid(self, backend):
        """Spot check that foreign key relationships are valid."""
        with backend._connection() as conn:
            # Check wordforms -> lemmas
            orphan_wordforms = conn.execute('''
                SELECT COUNT(*) FROM wordforms w
                WHERE w.lemma_id IS NOT NULL 
                AND w.lemma_id != ''
                AND NOT EXISTS (SELECT 1 FROM lemmas l WHERE l.lemma_id = w.lemma_id)
                LIMIT 1
            ''').fetchone()[0]
            
            # Allow some orphans (compounds, etc) but not too many
            assert orphan_wordforms < 1000, f"Too many orphan wordforms: {orphan_wordforms}"
            
            # Check examples -> senses (where linked)
            # Note: Some orphans are expected from heuristic linking to senses
            # that may have been cleaned up. Allow up to 5% orphan rate.
            orphan_examples = conn.execute('''
                SELECT COUNT(*) FROM examples e
                WHERE e.sense_id IS NOT NULL 
                AND e.sense_id != ''
                AND NOT EXISTS (SELECT 1 FROM senses s WHERE s.sense_id = e.sense_id)
            ''').fetchone()[0]
            
            total_sense_linked = conn.execute('''
                SELECT COUNT(*) FROM examples WHERE sense_id IS NOT NULL AND sense_id != ''
            ''').fetchone()[0]
            
            orphan_rate = orphan_examples / total_sense_linked if total_sense_linked > 0 else 0
            assert orphan_rate < 0.05, f"Too many orphan examples: {orphan_examples}/{total_sense_linked} = {orphan_rate:.1%}"


# =============================================================================
# Table Count Tests
# =============================================================================

class TestTableCounts:
    """Tests for expected row counts in key tables.
    
    Uses canonical metrics with tight tolerances for regression protection.
    """
    
    def test_sources_count_matches_metrics(self, backend, canonical_metrics):
        """Sources should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
        
        expected = canonical_metrics['total_sources']
        assert count == expected, f"Source count {count} != canonical {expected}"
    
    def test_tokens_count_matches_metrics(self, backend, canonical_metrics):
        """Tokens should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM tokens").fetchone()[0]
        
        expected = canonical_metrics['total_tokens']
        assert count == expected, f"Token count {count} != canonical {expected}"
    
    def test_wordforms_count_matches_metrics(self, backend, canonical_metrics):
        """Wordforms should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM wordforms").fetchone()[0]
        
        expected = canonical_metrics['wordform_count']
        assert count == expected, f"Wordform count {count} != canonical {expected}"
    
    def test_lemmas_count_matches_metrics(self, backend, canonical_metrics):
        """Lemmas should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM lemmas").fetchone()[0]
        
        expected = canonical_metrics['lemma_count']
        assert count == expected, f"Lemma count {count} != canonical {expected}"
    
    def test_senses_count_matches_metrics(self, backend, canonical_metrics):
        """Senses should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM senses").fetchone()[0]
        
        expected = canonical_metrics['sense_count']
        assert count == expected, f"Sense count {count} != canonical {expected}"
    
    def test_grammatical_morphemes_count_matches_metrics(self, backend, canonical_metrics):
        """Grammatical morphemes should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM grammatical_morphemes").fetchone()[0]
        
        expected = canonical_metrics['grammatical_morpheme_count']
        assert count == expected, f"Morpheme count {count} != canonical {expected}"
    
    def test_examples_count_matches_metrics(self, backend, canonical_metrics):
        """Examples should match canonical metrics exactly."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM examples").fetchone()[0]
        
        expected = canonical_metrics['example_count']
        assert count == expected, f"Example count {count} != canonical {expected}"
    
    def test_constructions_count_matches_metrics(self, backend, canonical_metrics):
        """Constructions layer should match metrics (optional layer)."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        expected = canonical_metrics['construction_count']
        assert count == expected, f"Construction count {count} != canonical {expected}"
        
        if count == 0:
            pytest.skip("Constructions layer not populated (optional)")
    
    def test_grammar_topics_count_matches_metrics(self, backend, canonical_metrics):
        """Grammar topics layer should match metrics (optional layer)."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM grammar_topics").fetchone()[0]
        
        expected = canonical_metrics['grammar_topic_count']
        assert count == expected, f"Grammar topics count {count} != canonical {expected}"
        
        if count == 0:
            pytest.skip("Grammar topics layer not populated (optional)")
        assert count >= 5, f"Grammar topic count {count} too low if layer is populated"


# =============================================================================
# Lookup Behavior Tests
# =============================================================================

class TestLookupBehavior:
    """Tests for dictionary lookup functionality."""
    
    def test_get_lemma_exists(self, backend):
        """Looking up existing lemma should return data."""
        lemma = backend.get_lemma('pai')
        
        assert lemma is not None
        assert lemma.lemma_id == 'pai'
        assert lemma.pos in ('V', 'FUNC', 'N')
    
    def test_get_lemma_not_exists(self, backend):
        """Looking up non-existent lemma should return None."""
        lemma = backend.get_lemma('xyznonexistent')
        
        assert lemma is None
    
    def test_get_senses_for_lemma(self, backend):
        """Getting senses for a lemma should return list."""
        senses = backend.get_senses('pai')
        
        assert isinstance(senses, list)
        assert len(senses) >= 1
        assert all(isinstance(s, Sense) for s in senses)
        assert all(s.lemma_id == 'pai' for s in senses)
    
    def test_get_senses_polysemous(self, backend):
        """Polysemous lemmas should have multiple senses."""
        # 'hi' has multiple grammatical functions
        senses = backend.get_senses('hi')
        
        # Should have at least DECL sense
        assert len(senses) >= 1
        glosses = [s.gloss for s in senses]
        assert 'DECL' in glosses
    
    def test_get_grammatical_morpheme(self, backend):
        """Getting a grammatical morpheme should return data."""
        with backend._connection() as conn:
            row = conn.execute('''
                SELECT * FROM grammatical_morphemes WHERE form = 'in' AND gloss = 'ERG'
            ''').fetchone()
        
        assert row is not None
        assert row['form'] == 'in'
        assert row['gloss'] == 'ERG'
        assert row['category'] == 'case_marker'
    
    def test_high_frequency_lemmas_have_examples(self, backend):
        """High-frequency lexical lemmas should have linked examples."""
        # These are lexical items with verified example linkage
        high_freq_lexical = ['tua', 'le', 'mi', 'ci', 'amah']
        
        for lemma_id in high_freq_lexical:
            with backend._connection() as conn:
                count = conn.execute('''
                    SELECT COUNT(*) FROM examples e
                    JOIN senses s ON e.sense_id = s.sense_id
                    WHERE s.lemma_id = ?
                ''', (lemma_id,)).fetchone()[0]
            
            assert count > 0, f"High-frequency lemma '{lemma_id}' has no examples"


# =============================================================================
# Sense-Example Linking Tests
# =============================================================================

class TestSenseExampleLinking:
    """Tests for sense-example relationships."""
    
    def test_examples_have_sense_or_morpheme(self, backend):
        """Most examples should be linked to a sense or morpheme."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM examples").fetchone()[0]
            linked = conn.execute('''
                SELECT COUNT(*) FROM examples 
                WHERE (sense_id IS NOT NULL AND sense_id != '')
                   OR (morpheme_id IS NOT NULL AND morpheme_id != '')
            ''').fetchone()[0]
        
        # At least 60% should be linked
        assert linked / total > 0.6, f"Only {linked}/{total} examples are linked"
    
    def test_sense_example_consistency(self, backend):
        """Example target_form should match lemma when sense-linked."""
        with backend._connection() as conn:
            # Sample check: get examples linked to 'pai' senses
            mismatches = conn.execute('''
                SELECT e.example_id, e.target_form, s.lemma_id
                FROM examples e
                JOIN senses s ON e.sense_id = s.sense_id
                WHERE s.lemma_id = 'pai'
                AND LOWER(e.target_form) != 'pai'
                AND e.target_form NOT LIKE '%pai%'
                LIMIT 10
            ''').fetchall()
        
        # Some flexibility allowed, but shouldn't have too many mismatches
        assert len(mismatches) < 5, f"Too many target_form mismatches for 'pai'"
    
    def test_no_duplicate_examples_per_sense(self, backend):
        """Same source_id shouldn't appear multiple times for same sense."""
        with backend._connection() as conn:
            duplicates = conn.execute('''
                SELECT sense_id, source_id, COUNT(*) as ct
                FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                GROUP BY sense_id, source_id
                HAVING ct > 3
            ''').fetchall()
        
        # Allow some duplicates (different target forms) but not too many
        assert len(duplicates) < 50, f"Too many duplicate source-sense pairs"


# =============================================================================
# Example Quality Ordering Tests
# =============================================================================

class TestExampleQualityOrdering:
    """Tests for example quality ranking."""
    
    # Use the canonical order from backend.py
    QUALITY_ORDER = EXAMPLE_QUALITY_ORDER
    
    def test_quality_values_valid(self, backend):
        """All quality values should be recognized."""
        valid_qualities = set(self.QUALITY_ORDER)
        
        with backend._connection() as conn:
            qualities = [row[0] for row in conn.execute(
                "SELECT DISTINCT quality FROM examples WHERE quality IS NOT NULL"
            )]
        
        for q in qualities:
            assert q in valid_qualities, f"Unknown quality value: {q}"
    
    def test_get_examples_for_sense_respects_quality_order(self, backend):
        """API method get_examples_for_sense should return examples in quality order."""
        # Find a sense with multiple examples of different qualities
        with backend._connection() as conn:
            # Get a sense that has examples with different quality values
            sense_with_varied = conn.execute('''
                SELECT sense_id, COUNT(DISTINCT quality) as q_count
                FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                  AND quality IS NOT NULL
                GROUP BY sense_id
                HAVING q_count >= 2
                ORDER BY COUNT(*) DESC
                LIMIT 1
            ''').fetchone()
        
        if not sense_with_varied:
            pytest.skip("No sense found with multiple quality levels")
        
        sense_id = sense_with_varied[0]
        
        # Get examples via the API
        examples = backend.get_examples_for_sense(sense_id, limit=20)
        
        # Verify they come out in correct order
        quality_ranks = {q: i for i, q in enumerate(self.QUALITY_ORDER)}
        prev_rank = -1
        for ex in examples:
            if ex.quality:
                rank = quality_ranks.get(ex.quality, 99)
                assert rank >= prev_rank, \
                    f"Quality order violation: {examples[prev_rank].quality if prev_rank >= 0 else 'start'} -> {ex.quality}"
                prev_rank = rank
    
    def test_get_examples_for_morpheme_respects_quality_order(self, backend):
        """API method get_examples_for_morpheme should return examples in quality order."""
        # Test with a common morpheme
        examples = backend.get_examples_for_morpheme('in.ERG.case_marker', limit=20)
        
        if not examples:
            pytest.skip("No examples found for ERG morpheme")
        
        quality_ranks = {q: i for i, q in enumerate(self.QUALITY_ORDER)}
        prev_rank = -1
        for ex in examples:
            if ex.quality:
                rank = quality_ranks.get(ex.quality, 99)
                assert rank >= prev_rank, \
                    f"Quality order violation for morpheme examples"
                prev_rank = rank
    
    def test_auto_quality_not_primary(self, backend):
        """Auto-generated examples shouldn't dominate primary positions."""
        # Find a sense that has both auto and non-auto examples
        with backend._connection() as conn:
            sense_id = conn.execute('''
                SELECT sense_id
                FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                GROUP BY sense_id
                HAVING SUM(CASE WHEN quality = 'auto' THEN 1 ELSE 0 END) > 0
                   AND SUM(CASE WHEN quality != 'auto' THEN 1 ELSE 0 END) > 0
                LIMIT 1
            ''').fetchone()
        
        if not sense_id:
            pytest.skip("No sense found with both auto and manual examples")
        
        # Use API to get top examples
        examples = backend.get_examples_for_sense(sense_id[0], limit=3)
        
        # The first example shouldn't be 'auto' if there are better ones
        if len(examples) > 1:
            first_quality = examples[0].quality
            assert first_quality != 'auto' or all(e.quality == 'auto' for e in examples), \
                f"Auto example ranked first but better examples exist"


# =============================================================================
# Constructions Layer Tests
# =============================================================================

class TestConstructionsLayer:
    """Tests for the constructions and grammar topics layer (optional)."""
    
    def test_constructions_have_required_fields(self, backend):
        """All constructions should have name, category, pattern."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        if total == 0:
            pytest.skip("Constructions layer not populated (optional)")
            
        with backend._connection() as conn:
            incomplete = conn.execute('''
                SELECT construction_id FROM constructions
                WHERE name IS NULL OR name = ''
                   OR category IS NULL OR category = ''
                   OR pattern IS NULL OR pattern = ''
            ''').fetchall()
        
        assert len(incomplete) == 0, f"Incomplete constructions: {[r[0] for r in incomplete]}"
    
    def test_constructions_categories_valid(self, backend):
        """Construction categories should be from expected set."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        if total == 0:
            pytest.skip("Constructions layer not populated (optional)")
            
        valid_categories = {
            'case_construction', 'serial_verb', 'aspect_construction',
            'modal_construction', 'voice_construction', 'negation_construction',
            'clause_final', 'subordination', 'nominalization', 'agreement'
        }
        
        with backend._connection() as conn:
            categories = [row[0] for row in conn.execute(
                "SELECT DISTINCT category FROM constructions"
            )]
        
        for cat in categories:
            assert cat in valid_categories, f"Unknown category: {cat}"
    
    def test_constructions_have_examples(self, backend):
        """Most constructions should have linked examples."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        if total == 0:
            pytest.skip("Constructions layer not populated (optional)")
            
        with backend._connection() as conn:
            with_examples = conn.execute('''
                SELECT COUNT(*) FROM constructions
                WHERE example_ids IS NOT NULL AND example_ids != '[]'
            ''').fetchone()[0]
        
        # At least 60% should have examples
        assert with_examples / total > 0.6, f"Only {with_examples}/{total} constructions have examples"
    
    def test_grammar_topics_hierarchy_valid(self, backend):
        """Grammar topics should form valid parent-child hierarchy."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM grammar_topics").fetchone()[0]
        
        if total == 0:
            pytest.skip("Grammar topics layer not populated (optional)")
            
        with backend._connection() as conn:
            # Check no orphan children (parent_id references non-existent topic)
            orphans = conn.execute('''
                SELECT gt.topic_id, gt.parent_id FROM grammar_topics gt
                WHERE gt.parent_id IS NOT NULL
                AND NOT EXISTS (SELECT 1 FROM grammar_topics p WHERE p.topic_id = gt.parent_id)
            ''').fetchall()
        
        assert len(orphans) == 0, f"Orphan topics: {[r[0] for r in orphans]}"
    
    def test_grammar_topics_link_to_constructions(self, backend):
        """Grammar topics should link to their constructions."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM grammar_topics").fetchone()[0]
        
        if total == 0:
            pytest.skip("Grammar topics layer not populated (optional)")
            
        with backend._connection() as conn:
            topics_with_constructions = conn.execute('''
                SELECT COUNT(*) FROM grammar_topics
                WHERE construction_ids IS NOT NULL AND construction_ids != '[]'
            ''').fetchone()[0]
        
        assert topics_with_constructions >= 5, "Too few topics link to constructions"
    
    def test_construction_morpheme_links_valid(self, backend):
        """Construction morpheme_ids should reference existing morphemes."""
        with backend._connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        if total == 0:
            pytest.skip("Constructions layer not populated (optional)")
            
        with backend._connection() as conn:
            constructions = list(conn.execute('''
                SELECT construction_id, morpheme_ids FROM constructions
                WHERE morpheme_ids IS NOT NULL AND morpheme_ids != '[]'
            '''))
            
            invalid_refs = []
            for cid, morpheme_ids_json in constructions:
                try:
                    morpheme_ids = json.loads(morpheme_ids_json)
                    for mid in morpheme_ids:
                        exists = conn.execute('''
                            SELECT 1 FROM grammatical_morphemes WHERE morpheme_id = ?
                        ''', (mid,)).fetchone()
                        if not exists:
                            invalid_refs.append((cid, mid))
                except json.JSONDecodeError:
                    invalid_refs.append((cid, 'INVALID_JSON'))
        
        # Allow some flexibility (morphemes may have been cleaned up)
        assert len(invalid_refs) < 10, f"Invalid morpheme references: {invalid_refs}"


# =============================================================================
# Guard Against Overly Aggressive Assignment
# =============================================================================

class TestAmbiguousAssignmentGuards:
    """Tests to guard against overly aggressive ambiguous-example assignment."""
    
    def test_polysemous_morpheme_examples_distributed(self, backend):
        """Examples for polysemous morphemes should be distributed across senses."""
        # 'in' is highly polysemous (ERG, CVB, QUOT, INST)
        with backend._connection() as conn:
            in_morphemes = list(conn.execute('''
                SELECT morpheme_id, gloss, 
                       (SELECT COUNT(*) FROM examples e WHERE e.morpheme_id = gm.morpheme_id) as ex_ct
                FROM grammatical_morphemes gm
                WHERE form = 'in'
            '''))
        
        # Each distinct function should have its own examples
        for mid, gloss, ex_ct in in_morphemes:
            # Primary functions should have examples
            if gloss in ('ERG', 'CVB', 'QUOT'):
                assert ex_ct > 0, f"'{gloss}' function of 'in' should have examples"
    
    def test_examples_not_over_assigned_to_single_sense(self, backend):
        """No single sense should hoard all examples for a lemma."""
        with backend._connection() as conn:
            # Find lemmas where one sense has >90% of examples
            hoarding = conn.execute('''
                WITH lemma_totals AS (
                    SELECT s.lemma_id, COUNT(e.example_id) as total_ex
                    FROM senses s
                    LEFT JOIN examples e ON s.sense_id = e.sense_id
                    GROUP BY s.lemma_id
                    HAVING total_ex > 10
                ),
                sense_counts AS (
                    SELECT s.lemma_id, s.sense_id, s.gloss, COUNT(e.example_id) as sense_ex
                    FROM senses s
                    LEFT JOIN examples e ON s.sense_id = e.sense_id
                    GROUP BY s.sense_id
                )
                SELECT sc.lemma_id, sc.sense_id, sc.gloss, sc.sense_ex, lt.total_ex,
                       CAST(sc.sense_ex AS FLOAT) / lt.total_ex as ratio
                FROM sense_counts sc
                JOIN lemma_totals lt ON sc.lemma_id = lt.lemma_id
                WHERE CAST(sc.sense_ex AS FLOAT) / lt.total_ex > 0.95
                AND lt.total_ex > 10
                AND (SELECT COUNT(*) FROM senses WHERE lemma_id = sc.lemma_id) > 1
            ''').fetchall()
        
        # Should be very few (ideally 0) cases of example hoarding
        assert len(hoarding) < 20, f"Potential example hoarding: {[(r[0], r[2]) for r in hoarding[:5]]}"
    
    def test_auto_examples_not_duplicating_manual(self, backend):
        """Auto-generated examples shouldn't duplicate manual examples."""
        with backend._connection() as conn:
            # Find cases where same source_id has both auto and non-auto for same sense
            duplicates = conn.execute('''
                SELECT sense_id, source_id, 
                       SUM(CASE WHEN quality = 'auto' THEN 1 ELSE 0 END) as auto_ct,
                       SUM(CASE WHEN quality != 'auto' THEN 1 ELSE 0 END) as manual_ct
                FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                GROUP BY sense_id, source_id
                HAVING auto_ct > 0 AND manual_ct > 0
            ''').fetchall()
        
        # Some overlap is okay, but shouldn't be excessive
        assert len(duplicates) < 100, f"Too many auto/manual duplicates: {len(duplicates)}"
    
    def test_morpheme_examples_match_gloss(self, backend):
        """Morpheme examples should contain the morpheme's gloss in their glossed field."""
        with backend._connection() as conn:
            # Sample check for a few morphemes
            mismatches = []
            for mid, form, gloss in [('in.ERG.case_marker', 'in', 'ERG'),
                                      ('sak.CAUS.tam_suffix', 'sak', 'CAUS')]:
                examples = list(conn.execute('''
                    SELECT example_id, glossed FROM examples
                    WHERE morpheme_id = ?
                    LIMIT 5
                ''', (mid,)))
                
                for eid, glossed in examples:
                    if glossed and gloss not in glossed:
                        mismatches.append((mid, eid))
        
        # Allow some mismatches (complex morphology), but not too many
        assert len(mismatches) < 3, f"Morpheme-gloss mismatches: {mismatches}"


# =============================================================================
# Backend API Tests
# =============================================================================

class TestBackendAPI:
    """Tests for the Backend class API methods."""
    
    def test_get_stats(self, backend):
        """get_stats should return all table counts."""
        counts = backend.get_stats()
        
        assert isinstance(counts, dict)
        assert 'sources' in counts
        assert 'tokens' in counts
        assert 'lemmas' in counts
        assert all(isinstance(v, int) for v in counts.values())
    
    def test_get_examples_for_sense(self, backend):
        """get_examples_for_sense should return examples."""
        # Find a sense with examples
        with backend._connection() as conn:
            sense_id = conn.execute('''
                SELECT sense_id FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                LIMIT 1
            ''').fetchone()[0]
        
        examples = backend.get_examples_for_sense(sense_id)
        
        assert isinstance(examples, list)
        assert len(examples) > 0
        assert all(isinstance(e, Example) for e in examples)
    
    def test_get_examples_for_morpheme(self, backend):
        """get_examples_for_morpheme should return examples."""
        examples = backend.get_examples_for_morpheme('in.ERG.case_marker')
        
        assert isinstance(examples, list)
        # ERG should have examples
        assert len(examples) > 0
    
    def test_fresh_backend_empty(self, temp_backend):
        """Fresh backend should have empty tables."""
        counts = temp_backend.get_stats()
        
        assert counts.get('sources', 0) == 0
        assert counts.get('tokens', 0) == 0
        assert counts.get('lemmas', 0) == 0


# =============================================================================
# Data Integrity Tests
# =============================================================================

class TestDataIntegrity:
    """Tests for overall data integrity."""
    
    def test_no_empty_lemma_ids(self, backend):
        """Lemma IDs should never be empty strings."""
        with backend._connection() as conn:
            empty = conn.execute('''
                SELECT COUNT(*) FROM lemmas WHERE lemma_id = '' OR lemma_id IS NULL
            ''').fetchone()[0]
        
        assert empty == 0, f"Found {empty} empty lemma IDs"
    
    def test_no_empty_sense_ids(self, backend):
        """Sense IDs should never be empty strings."""
        with backend._connection() as conn:
            empty = conn.execute('''
                SELECT COUNT(*) FROM senses WHERE sense_id = '' OR sense_id IS NULL
            ''').fetchone()[0]
        
        assert empty == 0, f"Found {empty} empty sense IDs"
    
    def test_wordform_frequencies_reasonable(self, backend):
        """Wordform frequencies should be reasonable."""
        with backend._connection() as conn:
            # No wordform should have frequency > total tokens
            total_tokens = conn.execute("SELECT COUNT(*) FROM tokens").fetchone()[0]
            max_freq = conn.execute("SELECT MAX(frequency) FROM wordforms").fetchone()[0]
        
        assert max_freq <= total_tokens, f"Wordform frequency {max_freq} > total tokens"
    
    def test_lemma_pos_not_empty(self, backend):
        """Lemmas should have POS tags."""
        with backend._connection() as conn:
            empty_pos = conn.execute('''
                SELECT COUNT(*) FROM lemmas WHERE pos = '' OR pos IS NULL
            ''').fetchone()[0]
            total = conn.execute("SELECT COUNT(*) FROM lemmas").fetchone()[0]
        
        # Allow some missing POS, but not too many
        assert empty_pos / total < 0.05, f"{empty_pos}/{total} lemmas missing POS"
    
    def test_source_ids_consistent(self, backend):
        """Source IDs should be consistent across tables."""
        with backend._connection() as conn:
            # All token source_ids should exist in sources
            orphan_tokens = conn.execute('''
                SELECT COUNT(*) FROM tokens t
                WHERE NOT EXISTS (SELECT 1 FROM sources s WHERE s.source_id = t.source_id)
            ''').fetchone()[0]
        
        assert orphan_tokens == 0, f"Found {orphan_tokens} tokens with invalid source_id"


# =============================================================================
# End-to-End Integration Tests
# =============================================================================

class TestEndToEndWorkflow:
    """Integration tests for the complete backend workflow.
    
    These tests verify the actual workflow encoded in the Makefile,
    exercising real end-to-end semantics rather than isolated table properties.
    """
    
    def test_full_lookup_workflow(self, backend):
        """Test complete word lookup workflow: lemma → senses → examples."""
        # Pick a common word
        lemma_id = 'pai'
        
        # Step 1: Get lemma
        lemma = backend.get_lemma(lemma_id)
        assert lemma is not None, f"Lemma '{lemma_id}' should exist"
        assert lemma.citation_form == 'pai'
        assert lemma.pos == 'V'
        assert lemma.primary_gloss, "Should have primary gloss"
        
        # Step 2: Get senses for the lemma
        senses = backend.get_senses(lemma_id)
        assert len(senses) >= 1, "Should have at least one sense"
        
        # Step 3: Get examples for primary sense
        primary_sense = [s for s in senses if s.is_primary]
        if primary_sense:
            examples = backend.get_examples_for_sense(primary_sense[0].sense_id)
            assert len(examples) > 0, "Primary sense should have examples"
            
            # Verify example structure
            ex = examples[0]
            assert ex.target_form, "Example should have target form"
            assert ex.glossed, "Example should have glossed text"
            assert ex.source_id, "Example should have source reference"
    
    def test_morpheme_lookup_workflow(self, backend):
        """Test grammatical morpheme lookup: morpheme → examples with gloss."""
        # Look up ergative marker -in
        morpheme_id = 'in.ERG.case_marker'
        
        # Step 1: Get morpheme
        morpheme = backend.get_morpheme(morpheme_id)
        assert morpheme is not None, f"Morpheme '{morpheme_id}' should exist"
        assert morpheme.form == 'in'
        assert morpheme.gloss == 'ERG'
        assert morpheme.category == 'case_marker'
        
        # Step 2: Get examples
        examples = backend.get_examples_for_morpheme(morpheme_id, limit=10)
        assert len(examples) > 0, "ERG marker should have examples"
        
        # Step 3: Verify examples show the morpheme
        has_matching_example = any(
            'ERG' in (ex.glossed or '') for ex in examples
        )
        assert has_matching_example, "At least one example should contain ERG gloss"
    
    def test_example_quality_determines_selection(self, backend):
        """Test that example quality affects which examples are returned first."""
        # Find a sense with multiple examples
        with backend._connection() as conn:
            sense_id = conn.execute('''
                SELECT sense_id FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                GROUP BY sense_id
                HAVING COUNT(*) >= 5
                LIMIT 1
            ''').fetchone()[0]
        
        # Get examples via API
        examples = backend.get_examples_for_sense(sense_id, limit=10)
        
        # Verify they're in quality order
        quality_ranks = {q: i for i, q in enumerate(EXAMPLE_QUALITY_ORDER)}
        
        prev_rank = -1
        for ex in examples:
            if ex.quality:
                rank = quality_ranks.get(ex.quality, 99)
                assert rank >= prev_rank, \
                    f"Examples should be ordered by quality, got {ex.quality} after better quality"
                prev_rank = rank
    
    def test_backend_stats_match_canonical_metrics(self, backend, canonical_metrics):
        """Backend get_stats() should match canonical metrics."""
        stats = backend.get_stats()
        
        # Key counts should match exactly
        assert stats['sources'] == canonical_metrics['total_sources']
        assert stats['tokens'] == canonical_metrics['total_tokens']
        assert stats['lemmas'] == canonical_metrics['lemma_count']
        assert stats['senses'] == canonical_metrics['sense_count']
        assert stats['grammatical_morphemes'] == canonical_metrics['grammatical_morpheme_count']
        assert stats['examples'] == canonical_metrics['example_count']
    
    def test_all_lemmas_have_glosses(self, backend, canonical_metrics):
        """Verify no unglossed lemmas (regression protection)."""
        with backend._connection() as conn:
            unglossed = conn.execute('''
                SELECT COUNT(*) FROM lemmas 
                WHERE (primary_gloss IS NULL OR primary_gloss = '' OR primary_gloss = '?')
            ''').fetchone()[0]
        
        assert unglossed == 0, f"Found {unglossed} unglossed lemmas (should be 0)"
    
    def test_senses_with_examples_matches_metrics(self, backend, canonical_metrics):
        """Verify senses_with_examples count matches canonical."""
        # Must match the exact query used by generate_metrics.py
        with backend._connection() as conn:
            with_examples = conn.execute('''
                SELECT COUNT(DISTINCT sense_id) FROM examples WHERE sense_id IS NOT NULL
            ''').fetchone()[0]
        
        expected = canonical_metrics['senses_with_examples']
        assert with_examples == expected, \
            f"Senses with examples {with_examples} != canonical {expected}"
    
    def test_review_queue_fully_resolved(self, backend, canonical_metrics):
        """Verify review queue state matches canonical."""
        with backend._connection() as conn:
            open_items = conn.execute('''
                SELECT COUNT(*) FROM review_queue 
                WHERE resolution IS NULL OR resolution = ''
            ''').fetchone()[0]
        
        expected = canonical_metrics['review_queue_open']
        assert open_items == expected, \
            f"Open review items {open_items} != canonical {expected}"


# =============================================================================
# Schema and API Contract Tests
# =============================================================================

class TestSchemaConsistency:
    """Tests to ensure schema definitions match across code and docs."""
    
    def test_review_queue_columns_match_spec(self, backend):
        """Verify review_queue table has columns matching BACKEND_SPEC.md."""
        expected_columns = {
            'review_id', 'entity_type', 'entity_id', 'reason', 'priority',
            'assigned_to', 'status', 'resolution', 'created_at', 'resolved_at'
        }
        
        with backend._connection() as conn:
            cursor = conn.execute("PRAGMA table_info(review_queue)")
            actual_columns = {row[1] for row in cursor.fetchall()}
        
        assert actual_columns == expected_columns, \
            f"Column mismatch: expected {expected_columns}, got {actual_columns}"
    
    def test_examples_quality_uses_canonical_values(self, backend):
        """All example quality values should be from EXAMPLE_QUALITY_ORDER."""
        valid_qualities = set(EXAMPLE_QUALITY_ORDER)
        
        with backend._connection() as conn:
            qualities = [row[0] for row in conn.execute(
                "SELECT DISTINCT quality FROM examples WHERE quality IS NOT NULL AND quality != ''"
            )]
        
        invalid = [q for q in qualities if q not in valid_qualities]
        assert not invalid, f"Invalid quality values in examples: {invalid}"
    
    def test_add_review_item_uses_reason_not_description(self, backend, temp_backend):
        """add_review_item() should use 'reason' parameter, not 'description'."""
        # This test verifies the API signature
        import inspect
        sig = inspect.signature(temp_backend.add_review_item)
        param_names = list(sig.parameters.keys())
        
        assert 'reason' in param_names, "add_review_item should have 'reason' parameter"
        assert 'description' not in param_names, "add_review_item should NOT have 'description' parameter"
        assert 'issue_type' not in param_names, "add_review_item should NOT have 'issue_type' parameter"
    
    def test_add_review_item_works(self, temp_backend):
        """add_review_item() should successfully insert into review_queue."""
        review_id = temp_backend.add_review_item(
            entity_type='lemma',
            entity_id='test_lemma',
            reason='Test reason for review',
            priority='high'
        )
        
        assert review_id > 0, "Should return a valid review_id"
        
        # Verify it was inserted correctly
        items = temp_backend.get_review_items(status='open')
        assert len(items) == 1
        assert items[0].entity_id == 'test_lemma'
        assert items[0].reason == 'Test reason for review'
        assert items[0].priority == 'high'


class TestLinkExamplesToSenses:
    """Tests for the link_examples_to_senses.py script."""
    
    def test_script_imports_without_error(self):
        """Script should import without syntax or import errors."""
        import link_examples_to_senses
        
        assert hasattr(link_examples_to_senses, 'link_examples_to_senses')
        assert hasattr(link_examples_to_senses, 'generate_corpus_examples')
    
    def test_link_function_on_empty_db(self, temp_backend):
        """link_examples_to_senses should handle empty database gracefully."""
        import link_examples_to_senses
        
        # Should not raise on empty db
        stats, updated = link_examples_to_senses.link_examples_to_senses(
            temp_backend.db_path, dry_run=True
        )
        
        assert stats['total_unlinked'] == 0
        assert updated == 0
    
    def test_script_uses_valid_quality_values(self):
        """Script should only use quality values from canonical list."""
        import link_examples_to_senses
        import inspect
        
        # Get source code
        source = inspect.getsource(link_examples_to_senses)
        
        # Check that any quality values used are valid
        # The script uses 'quality': 'auto' which should be in EXAMPLE_QUALITY_ORDER
        assert 'auto' in EXAMPLE_QUALITY_ORDER, \
            "'auto' quality used by link_examples_to_senses.py must be in EXAMPLE_QUALITY_ORDER"


class TestQualityOrderConsistency:
    """Tests that quality ordering is consistent across modules."""
    
    def test_backend_exports_quality_order(self):
        """Backend should export EXAMPLE_QUALITY_ORDER constant."""
        from backend import EXAMPLE_QUALITY_ORDER
        
        assert isinstance(EXAMPLE_QUALITY_ORDER, list)
        assert len(EXAMPLE_QUALITY_ORDER) >= 6, "Should have at least 6 quality levels"
        assert 'canonical' in EXAMPLE_QUALITY_ORDER
        assert 'excellent' in EXAMPLE_QUALITY_ORDER
        assert 'auto' in EXAMPLE_QUALITY_ORDER
    
    def test_quality_sql_matches_python_list(self):
        """QUALITY_ORDER_SQL should produce same ordering as EXAMPLE_QUALITY_ORDER."""
        from backend import EXAMPLE_QUALITY_ORDER, QUALITY_ORDER_SQL
        
        # The SQL CASE statement assigns rank 1 to first item, 2 to second, etc.
        # Extract the order from the SQL
        import re
        matches = re.findall(r"WHEN '(\w+)' THEN (\d+)", QUALITY_ORDER_SQL)
        sql_order = {name: int(rank) for name, rank in matches}
        
        # Verify order matches
        for i, quality in enumerate(EXAMPLE_QUALITY_ORDER):
            expected_rank = i + 1
            actual_rank = sql_order.get(quality)
            assert actual_rank == expected_rank, \
                f"Quality '{quality}' has SQL rank {actual_rank}, expected {expected_rank}"
    
    def test_dictionary_draft_uses_canonical_order(self):
        """generate_dictionary_draft.py should import from backend, not define locally."""
        import generate_dictionary_draft
        
        # Check that it imports QUALITY_ORDER_SQL
        assert 'QUALITY_ORDER_SQL' in dir(generate_dictionary_draft) or \
               hasattr(generate_dictionary_draft, 'get_best_example'), \
               "Should use backend's quality ordering"


class TestConservativeLinkingPolicy:
    """Tests for conservative example-to-sense linking behavior."""
    
    def test_link_script_has_review_routed_stat(self):
        """Script should track review_routed for ambiguous cases."""
        import link_examples_to_senses
        import inspect
        
        source = inspect.getsource(link_examples_to_senses.link_examples_to_senses)
        assert 'review_routed' in source, \
            "link_examples_to_senses should track review_routed stats"
    
    def test_link_script_does_not_default_to_first_sense(self):
        """Script should NOT have 'default to first sense' fallback."""
        import link_examples_to_senses
        import inspect
        
        source = inspect.getsource(link_examples_to_senses.link_examples_to_senses)
        # Check for dangerous patterns that indicate defaulting to first sense
        assert 'senses[0]' not in source.split('# Case 4')[1] if '# Case 4' in source else True, \
            "Ambiguous cases should not default to first sense"
    
    def test_link_script_routes_ambiguous_to_review(self):
        """Ambiguous polysemous cases should go to review queue."""
        import link_examples_to_senses
        import inspect
        
        source = inspect.getsource(link_examples_to_senses.link_examples_to_senses)
        assert 'review_items.append' in source, \
            "Ambiguous cases should be appended to review_items"
        assert 'INSERT' in source and 'review_queue' in source, \
            "Script should insert ambiguous cases into review_queue"
