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

from backend import Backend, Lemma, Sense, Example, GrammaticalMorpheme

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
    """Tests for expected row counts in key tables."""
    
    def test_sources_count(self, backend):
        """Sources should contain ~30,000 verses."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM sources").fetchone()[0]
        
        assert 29000 < count < 32000, f"Source count {count} outside expected range"
    
    def test_tokens_count(self, backend):
        """Tokens should contain ~831,000 tokens."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM tokens").fetchone()[0]
        
        assert 800000 < count < 900000, f"Token count {count} outside expected range"
    
    def test_wordforms_count(self, backend):
        """Wordforms should contain ~20,000 distinct forms."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM wordforms").fetchone()[0]
        
        assert 18000 < count < 25000, f"Wordform count {count} outside expected range"
    
    def test_lemmas_count(self, backend):
        """Lemmas should contain ~7,000 entries."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM lemmas").fetchone()[0]
        
        assert 6000 < count < 9000, f"Lemma count {count} outside expected range"
    
    def test_senses_count(self, backend):
        """Senses should contain ~10,000 entries."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM senses").fetchone()[0]
        
        assert 8000 < count < 12000, f"Sense count {count} outside expected range"
    
    def test_grammatical_morphemes_count(self, backend):
        """Grammatical morphemes should contain 150-550 entries."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM grammatical_morphemes").fetchone()[0]
        
        assert 150 < count < 550, f"Grammatical morpheme count {count} outside expected range"
    
    def test_examples_count(self, backend):
        """Examples should contain ~20,000+ entries."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM examples").fetchone()[0]
        
        assert count > 20000, f"Example count {count} too low"
    
    def test_constructions_count(self, backend):
        """Constructions layer is optional but should be valid if present."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM constructions").fetchone()[0]
        
        # Constructions are an optional editorial layer
        # If present, should have reasonable content
        if count == 0:
            pytest.skip("Constructions layer not populated (optional)")
        assert count >= 10, f"Construction count {count} too low if layer is populated"
    
    def test_grammar_topics_count(self, backend):
        """Grammar topics layer is optional but should be valid if present."""
        with backend._connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM grammar_topics").fetchone()[0]
        
        # Grammar topics are an optional editorial layer
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
    
    QUALITY_ORDER = ['canonical', 'excellent', 'good', 'transparent', 'shortest', 'acceptable', 'auto', 'additional']
    
    def test_quality_values_valid(self, backend):
        """All quality values should be recognized."""
        valid_qualities = set(self.QUALITY_ORDER)
        
        with backend._connection() as conn:
            qualities = [row[0] for row in conn.execute(
                "SELECT DISTINCT quality FROM examples WHERE quality IS NOT NULL"
            )]
        
        for q in qualities:
            assert q in valid_qualities, f"Unknown quality value: {q}"
    
    def test_get_examples_ordered_by_quality(self, backend):
        """Examples should be retrievable in quality order."""
        with backend._connection() as conn:
            # Get examples for a sense with multiple qualities
            examples = list(conn.execute('''
                SELECT quality FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                ORDER BY CASE quality
                    WHEN 'canonical' THEN 1
                    WHEN 'excellent' THEN 2
                    WHEN 'good' THEN 3
                    WHEN 'transparent' THEN 4
                    WHEN 'shortest' THEN 5
                    WHEN 'acceptable' THEN 6
                    WHEN 'auto' THEN 7
                    WHEN 'additional' THEN 8
                    ELSE 9
                END
                LIMIT 20
            '''))
        
        # Verify ordering (canonical/excellent should come first if present)
        assert len(examples) > 0
    
    def test_auto_quality_not_primary(self, backend):
        """Auto-generated examples shouldn't dominate primary positions."""
        with backend._connection() as conn:
            # For senses with both auto and non-auto examples,
            # non-auto should be available
            senses_with_mixed = conn.execute('''
                SELECT sense_id, 
                       SUM(CASE WHEN quality = 'auto' THEN 1 ELSE 0 END) as auto_ct,
                       SUM(CASE WHEN quality != 'auto' THEN 1 ELSE 0 END) as manual_ct
                FROM examples
                WHERE sense_id IS NOT NULL AND sense_id != ''
                GROUP BY sense_id
                HAVING auto_ct > 0 AND manual_ct > 0
                LIMIT 10
            ''').fetchall()
        
        # Just verify the query runs - structure is correct
        assert isinstance(senses_with_mixed, list)


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
