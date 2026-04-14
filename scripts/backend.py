#!/usr/bin/env python3
"""
Kuki-Chin Shared Backend

SQLite-based backend for dictionary and grammar generation.
Provides a unified data layer for both dictionary lookups and grammar reports.

Usage:
    from backend import Backend
    
    db = Backend('data/ctd_backend.db')
    entry = db.get_lemma('pai')
    senses = db.get_senses('pai')
    examples = db.get_examples_for_sense('pai.1')
"""

import os
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from contextlib import contextmanager


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class Source:
    """A source text (verse)."""
    source_id: str
    iso: str
    book_code: str
    chapter: int
    verse: int
    text: str
    text_normalized: str
    kjv_text: str = ''
    token_count: int = 0


@dataclass
class Lemma:
    """A dictionary headword."""
    lemma_id: str
    citation_form: str
    pos: str
    entry_type: str  # lexical, grammatical, mixed
    primary_gloss: str
    token_count: int = 0
    form_count: int = 0
    is_polysemous: bool = False
    needs_review: bool = False
    entry_status: str = 'auto'
    notes: str = ''


@dataclass
class Sense:
    """A distinct meaning/function of a lemma."""
    sense_id: str
    lemma_id: str
    sense_num: int
    pos: str
    gloss: str
    definition: str = ''
    usage_type: str = 'lexical'  # lexical, grammatical, mixed
    frequency: int = 0
    is_primary: bool = False
    notes: str = ''


@dataclass
class GrammaticalMorpheme:
    """An affix, clitic, particle, or grammaticalized form."""
    morpheme_id: str
    form: str
    gloss: str
    function: str
    category: str
    subcategory: str = ''
    position: str = 'suffix'  # prefix, suffix, clitic, particle
    frequency: int = 0
    environments: str = ''
    is_polysemous: bool = False
    lexical_source_id: str = ''
    status: str = 'auto'
    notes: str = ''


@dataclass
class Example:
    """A curated example sentence."""
    example_id: int
    source_id: str
    sense_id: str = ''
    morpheme_id: str = ''
    target_form: str = ''
    tedim_text: str = ''
    segmented: str = ''
    glossed: str = ''
    kjv_text: str = ''
    quality: str = 'acceptable'
    example_type: str = 'sense'
    notes: str = ''


@dataclass
class ReviewItem:
    """An item requiring manual review."""
    review_id: int
    entity_type: str
    entity_id: str
    reason: str
    priority: str = 'medium'
    status: str = 'open'
    assigned_to: str = ''
    resolution: str = ''
    created_at: str = ''
    resolved_at: str = ''


# =============================================================================
# Backend Class
# =============================================================================

class Backend:
    """
    SQLite backend for Kuki-Chin corpus data.
    
    Provides unified access to dictionary and grammar data.
    """
    
    SCHEMA = '''
    -- Language metadata
    CREATE TABLE IF NOT EXISTS languages (
        iso TEXT PRIMARY KEY,
        name TEXT,
        family TEXT DEFAULT 'Kuki-Chin',
        source_bible TEXT,
        analyzer_module TEXT,
        notes TEXT
    );
    
    -- Source texts (verses)
    CREATE TABLE IF NOT EXISTS sources (
        source_id TEXT PRIMARY KEY,
        iso TEXT,
        book_code TEXT,
        chapter INTEGER,
        verse INTEGER,
        text TEXT,
        text_normalized TEXT,
        kjv_text TEXT,
        token_count INTEGER DEFAULT 0,
        FOREIGN KEY (iso) REFERENCES languages(iso)
    );
    
    -- Token occurrences
    CREATE TABLE IF NOT EXISTS tokens (
        token_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        position INTEGER,
        surface TEXT,
        normalized TEXT,
        wordform_id TEXT,
        is_sentence_final INTEGER DEFAULT 0,
        FOREIGN KEY (source_id) REFERENCES sources(source_id),
        FOREIGN KEY (wordform_id) REFERENCES wordforms(wordform_id)
    );
    
    -- Wordforms (types)
    CREATE TABLE IF NOT EXISTS wordforms (
        wordform_id TEXT PRIMARY KEY,
        surface TEXT,
        normalized TEXT,
        lemma_id TEXT,
        segmentation TEXT,
        gloss TEXT,
        pos TEXT,
        frequency INTEGER DEFAULT 0,
        is_ambiguous INTEGER DEFAULT 0,
        status TEXT DEFAULT 'auto',
        FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id)
    );
    
    -- Lemmas (dictionary headwords)
    CREATE TABLE IF NOT EXISTS lemmas (
        lemma_id TEXT PRIMARY KEY,
        citation_form TEXT,
        pos TEXT,
        entry_type TEXT DEFAULT 'lexical',
        primary_gloss TEXT,
        token_count INTEGER DEFAULT 0,
        form_count INTEGER DEFAULT 0,
        is_polysemous INTEGER DEFAULT 0,
        needs_review INTEGER DEFAULT 0,
        entry_status TEXT DEFAULT 'auto',
        notes TEXT
    );
    
    -- Senses
    CREATE TABLE IF NOT EXISTS senses (
        sense_id TEXT PRIMARY KEY,
        lemma_id TEXT,
        sense_num INTEGER,
        pos TEXT,
        gloss TEXT,
        definition TEXT,
        usage_type TEXT DEFAULT 'lexical',
        frequency INTEGER DEFAULT 0,
        is_primary INTEGER DEFAULT 0,
        notes TEXT,
        FOREIGN KEY (lemma_id) REFERENCES lemmas(lemma_id)
    );
    
    -- Grammatical morphemes
    CREATE TABLE IF NOT EXISTS grammatical_morphemes (
        morpheme_id TEXT PRIMARY KEY,
        form TEXT,
        gloss TEXT,
        function TEXT,
        category TEXT,
        subcategory TEXT,
        position TEXT DEFAULT 'suffix',
        frequency INTEGER DEFAULT 0,
        environments TEXT,
        is_polysemous INTEGER DEFAULT 0,
        lexical_source_id TEXT,
        status TEXT DEFAULT 'auto',
        notes TEXT
    );
    
    -- Examples
    CREATE TABLE IF NOT EXISTS examples (
        example_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        sense_id TEXT,
        morpheme_id TEXT,
        target_form TEXT,
        tedim_text TEXT,
        segmented TEXT,
        glossed TEXT,
        kjv_text TEXT,
        quality TEXT DEFAULT 'acceptable',
        example_type TEXT DEFAULT 'sense',
        notes TEXT,
        FOREIGN KEY (source_id) REFERENCES sources(source_id),
        FOREIGN KEY (sense_id) REFERENCES senses(sense_id),
        FOREIGN KEY (morpheme_id) REFERENCES grammatical_morphemes(morpheme_id)
    );
    
    -- Constructions (grammar patterns)
    CREATE TABLE IF NOT EXISTS constructions (
        construction_id TEXT PRIMARY KEY,
        name TEXT,
        category TEXT,
        pattern TEXT,
        description TEXT,
        morpheme_ids TEXT,
        frequency INTEGER DEFAULT 0,
        example_ids TEXT,
        status TEXT DEFAULT 'draft'
    );
    
    -- Grammar topics
    CREATE TABLE IF NOT EXISTS grammar_topics (
        topic_id TEXT PRIMARY KEY,
        title TEXT,
        parent_id TEXT,
        display_order INTEGER,
        description TEXT,
        construction_ids TEXT,
        morpheme_ids TEXT,
        status TEXT DEFAULT 'draft',
        FOREIGN KEY (parent_id) REFERENCES grammar_topics(topic_id)
    );
    
    -- Review queue
    CREATE TABLE IF NOT EXISTS review_queue (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT,
        entity_id TEXT,
        reason TEXT,
        priority TEXT DEFAULT 'medium',
        assigned_to TEXT,
        status TEXT DEFAULT 'open',
        resolution TEXT,
        created_at TEXT,
        resolved_at TEXT
    );
    
    -- Provenance tracking
    CREATE TABLE IF NOT EXISTS provenance (
        provenance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity_type TEXT,
        entity_id TEXT,
        source TEXT,
        confidence REAL,
        evidence TEXT,
        created_at TEXT,
        updated_at TEXT
    );
    
    -- Indexes for common queries
    CREATE INDEX IF NOT EXISTS idx_tokens_source ON tokens(source_id);
    CREATE INDEX IF NOT EXISTS idx_tokens_wordform ON tokens(wordform_id);
    CREATE INDEX IF NOT EXISTS idx_wordforms_lemma ON wordforms(lemma_id);
    CREATE INDEX IF NOT EXISTS idx_senses_lemma ON senses(lemma_id);
    CREATE INDEX IF NOT EXISTS idx_examples_sense ON examples(sense_id);
    CREATE INDEX IF NOT EXISTS idx_examples_morpheme ON examples(morpheme_id);
    CREATE INDEX IF NOT EXISTS idx_gram_category ON grammatical_morphemes(category);
    CREATE INDEX IF NOT EXISTS idx_review_status ON review_queue(status, priority);
    '''
    
    def __init__(self, db_path: str):
        """Initialize backend with database path."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        with self._connection() as conn:
            conn.executescript(self.SCHEMA)
    
    @contextmanager
    def _connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    # =========================================================================
    # Language Methods
    # =========================================================================
    
    def add_language(self, iso: str, name: str, source_bible: str = '',
                     analyzer_module: str = '', notes: str = ''):
        """Add or update language metadata."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO languages 
                (iso, name, family, source_bible, analyzer_module, notes)
                VALUES (?, ?, 'Kuki-Chin', ?, ?, ?)
            ''', (iso, name, source_bible, analyzer_module, notes))
    
    def get_language(self, iso: str) -> Optional[Dict]:
        """Get language metadata."""
        with self._connection() as conn:
            row = conn.execute(
                'SELECT * FROM languages WHERE iso = ?', (iso,)
            ).fetchone()
            return dict(row) if row else None
    
    # =========================================================================
    # Source Methods
    # =========================================================================
    
    def add_source(self, source: Source):
        """Add or update a source verse."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO sources
                (source_id, iso, book_code, chapter, verse, text, 
                 text_normalized, kjv_text, token_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (source.source_id, source.iso, source.book_code,
                  source.chapter, source.verse, source.text,
                  source.text_normalized, source.kjv_text, source.token_count))
    
    def get_source(self, source_id: str) -> Optional[Source]:
        """Get a source verse by ID."""
        with self._connection() as conn:
            row = conn.execute(
                'SELECT * FROM sources WHERE source_id = ?', (source_id,)
            ).fetchone()
            if row:
                return Source(**dict(row))
            return None
    
    def get_sources_for_book(self, book_code: str) -> List[Source]:
        """Get all verses for a book."""
        with self._connection() as conn:
            rows = conn.execute(
                'SELECT * FROM sources WHERE book_code = ? ORDER BY source_id',
                (book_code,)
            ).fetchall()
            return [Source(**dict(row)) for row in rows]
    
    # =========================================================================
    # Lemma Methods
    # =========================================================================
    
    def add_lemma(self, lemma: Lemma):
        """Add or update a lemma."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO lemmas
                (lemma_id, citation_form, pos, entry_type, primary_gloss,
                 token_count, form_count, is_polysemous, needs_review,
                 entry_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (lemma.lemma_id, lemma.citation_form, lemma.pos,
                  lemma.entry_type, lemma.primary_gloss, lemma.token_count,
                  lemma.form_count, int(lemma.is_polysemous),
                  int(lemma.needs_review), lemma.entry_status, lemma.notes))
    
    def get_lemma(self, lemma_id: str) -> Optional[Lemma]:
        """Get a lemma by ID."""
        with self._connection() as conn:
            row = conn.execute(
                'SELECT * FROM lemmas WHERE lemma_id = ?', (lemma_id,)
            ).fetchone()
            if row:
                d = dict(row)
                d['is_polysemous'] = bool(d['is_polysemous'])
                d['needs_review'] = bool(d['needs_review'])
                return Lemma(**d)
            return None
    
    def search_lemmas(self, query: str, pos: str = None, 
                      limit: int = 50) -> List[Lemma]:
        """Search lemmas by citation form or gloss."""
        with self._connection() as conn:
            sql = '''
                SELECT * FROM lemmas 
                WHERE (citation_form LIKE ? OR primary_gloss LIKE ?)
            '''
            params = [f'%{query}%', f'%{query}%']
            if pos:
                sql += ' AND pos = ?'
                params.append(pos)
            sql += ' ORDER BY token_count DESC LIMIT ?'
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d['is_polysemous'] = bool(d['is_polysemous'])
                d['needs_review'] = bool(d['needs_review'])
                results.append(Lemma(**d))
            return results
    
    def get_lemmas_by_pos(self, pos: str, entry_type: str = None,
                          min_freq: int = 0, limit: int = 100) -> List[Lemma]:
        """Get lemmas filtered by POS and optionally entry type."""
        with self._connection() as conn:
            sql = 'SELECT * FROM lemmas WHERE pos = ? AND token_count >= ?'
            params = [pos, min_freq]
            if entry_type:
                sql += ' AND entry_type = ?'
                params.append(entry_type)
            sql += ' ORDER BY token_count DESC LIMIT ?'
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d['is_polysemous'] = bool(d['is_polysemous'])
                d['needs_review'] = bool(d['needs_review'])
                results.append(Lemma(**d))
            return results
    
    # =========================================================================
    # Sense Methods
    # =========================================================================
    
    def add_sense(self, sense: Sense):
        """Add or update a sense."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO senses
                (sense_id, lemma_id, sense_num, pos, gloss, definition,
                 usage_type, frequency, is_primary, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (sense.sense_id, sense.lemma_id, sense.sense_num,
                  sense.pos, sense.gloss, sense.definition, sense.usage_type,
                  sense.frequency, int(sense.is_primary), sense.notes))
    
    def get_senses(self, lemma_id: str) -> List[Sense]:
        """Get all senses for a lemma."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT * FROM senses WHERE lemma_id = ?
                ORDER BY is_primary DESC, frequency DESC
            ''', (lemma_id,)).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d['is_primary'] = bool(d['is_primary'])
                results.append(Sense(**d))
            return results
    
    def get_sense(self, sense_id: str) -> Optional[Sense]:
        """Get a specific sense."""
        with self._connection() as conn:
            row = conn.execute(
                'SELECT * FROM senses WHERE sense_id = ?', (sense_id,)
            ).fetchone()
            if row:
                d = dict(row)
                d['is_primary'] = bool(d['is_primary'])
                return Sense(**d)
            return None
    
    # =========================================================================
    # Grammatical Morpheme Methods
    # =========================================================================
    
    def add_grammatical_morpheme(self, morpheme: GrammaticalMorpheme):
        """Add or update a grammatical morpheme."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO grammatical_morphemes
                (morpheme_id, form, gloss, function, category, subcategory,
                 position, frequency, environments, is_polysemous,
                 lexical_source_id, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (morpheme.morpheme_id, morpheme.form, morpheme.gloss,
                  morpheme.function, morpheme.category, morpheme.subcategory,
                  morpheme.position, morpheme.frequency, morpheme.environments,
                  int(morpheme.is_polysemous), morpheme.lexical_source_id,
                  morpheme.status, morpheme.notes))
    
    def get_grammatical_morphemes(self, category: str = None,
                                   position: str = None) -> List[GrammaticalMorpheme]:
        """Get grammatical morphemes, optionally filtered."""
        with self._connection() as conn:
            sql = 'SELECT * FROM grammatical_morphemes WHERE 1=1'
            params = []
            if category:
                sql += ' AND category = ?'
                params.append(category)
            if position:
                sql += ' AND position = ?'
                params.append(position)
            sql += ' ORDER BY frequency DESC'
            
            rows = conn.execute(sql, params).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d['is_polysemous'] = bool(d['is_polysemous'])
                results.append(GrammaticalMorpheme(**d))
            return results
    
    def get_morpheme_by_form(self, form: str) -> List[GrammaticalMorpheme]:
        """Get all morphemes with a given form."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT * FROM grammatical_morphemes 
                WHERE form = ? ORDER BY frequency DESC
            ''', (form,)).fetchall()
            results = []
            for row in rows:
                d = dict(row)
                d['is_polysemous'] = bool(d['is_polysemous'])
                results.append(GrammaticalMorpheme(**d))
            return results
    
    # =========================================================================
    # Example Methods
    # =========================================================================
    
    def add_example(self, example: Example) -> int:
        """Add an example, returns example_id."""
        with self._connection() as conn:
            cursor = conn.execute('''
                INSERT INTO examples
                (source_id, sense_id, morpheme_id, target_form, tedim_text,
                 segmented, glossed, kjv_text, quality, example_type, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (example.source_id, example.sense_id, example.morpheme_id,
                  example.target_form, example.tedim_text, example.segmented,
                  example.glossed, example.kjv_text, example.quality,
                  example.example_type, example.notes))
            return cursor.lastrowid
    
    def get_examples_for_sense(self, sense_id: str, 
                                limit: int = 5) -> List[Example]:
        """Get examples for a sense."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT * FROM examples 
                WHERE sense_id = ?
                ORDER BY 
                    CASE quality 
                        WHEN 'excellent' THEN 1 
                        WHEN 'good' THEN 2 
                        WHEN 'acceptable' THEN 3
                        ELSE 4
                    END
                LIMIT ?
            ''', (sense_id, limit)).fetchall()
            return [Example(**dict(row)) for row in rows]
    
    def get_examples_for_morpheme(self, morpheme_id: str,
                                   limit: int = 5) -> List[Example]:
        """Get examples for a grammatical morpheme."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT * FROM examples 
                WHERE morpheme_id = ?
                ORDER BY 
                    CASE quality 
                        WHEN 'excellent' THEN 1 
                        WHEN 'good' THEN 2 
                        WHEN 'acceptable' THEN 3
                        ELSE 4
                    END
                LIMIT ?
            ''', (morpheme_id, limit)).fetchall()
            return [Example(**dict(row)) for row in rows]
    
    def get_examples_for_lemma(self, lemma_id: str, 
                                limit: int = 10) -> List[Example]:
        """Get examples for any sense of a lemma."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT e.* FROM examples e
                JOIN senses s ON e.sense_id = s.sense_id
                WHERE s.lemma_id = ?
                ORDER BY 
                    s.is_primary DESC,
                    CASE e.quality 
                        WHEN 'excellent' THEN 1 
                        WHEN 'good' THEN 2 
                        WHEN 'acceptable' THEN 3
                        ELSE 4 
                    END
                LIMIT ?
            ''', (lemma_id, limit)).fetchall()
            return [Example(**dict(row)) for row in rows]
    
    # =========================================================================
    # Review Queue Methods
    # =========================================================================
    
    def add_review_item(self, entity_type: str, entity_id: str, 
                        reason: str, priority: str = 'medium') -> int:
        """Add an item to the review queue."""
        import datetime
        with self._connection() as conn:
            cursor = conn.execute('''
                INSERT INTO review_queue
                (entity_type, entity_id, reason, priority, status, created_at)
                VALUES (?, ?, ?, ?, 'open', ?)
            ''', (entity_type, entity_id, reason, priority,
                  datetime.datetime.now().isoformat()))
            return cursor.lastrowid
    
    def get_review_items(self, status: str = 'open', 
                         priority: str = None,
                         entity_type: str = None,
                         limit: int = 50) -> List[ReviewItem]:
        """Get items from the review queue."""
        with self._connection() as conn:
            sql = 'SELECT * FROM review_queue WHERE status = ?'
            params = [status]
            if priority:
                sql += ' AND priority = ?'
                params.append(priority)
            if entity_type:
                sql += ' AND entity_type = ?'
                params.append(entity_type)
            sql += ''' ORDER BY 
                CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                created_at
                LIMIT ?'''
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            return [ReviewItem(**dict(row)) for row in rows]
    
    def resolve_review_item(self, review_id: int, resolution: str):
        """Mark a review item as resolved."""
        import datetime
        with self._connection() as conn:
            conn.execute('''
                UPDATE review_queue 
                SET status = 'resolved', resolution = ?, resolved_at = ?
                WHERE review_id = ?
            ''', (resolution, datetime.datetime.now().isoformat(), review_id))
    
    # =========================================================================
    # Sense Query Methods
    # =========================================================================
    
    def get_sense_distribution(self, lemma_id: str) -> Dict[str, int]:
        """Get distribution of examples across senses for a lemma."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT e.sense_id, COUNT(*) as count
                FROM examples e
                JOIN senses s ON e.sense_id = s.sense_id
                WHERE s.lemma_id = ?
                GROUP BY e.sense_id
                ORDER BY count DESC
            ''', (lemma_id,)).fetchall()
            return {row['sense_id']: row['count'] for row in rows}
    
    # =========================================================================
    # Wordform Methods
    # =========================================================================
    
    def add_wordform(self, wordform_id: str, surface: str, normalized: str,
                     lemma_id: str, segmentation: str, gloss: str, pos: str,
                     frequency: int = 0, is_ambiguous: bool = False,
                     status: str = 'auto'):
        """Add or update a wordform."""
        with self._connection() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO wordforms
                (wordform_id, surface, normalized, lemma_id, segmentation,
                 gloss, pos, frequency, is_ambiguous, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (wordform_id, surface, normalized, lemma_id, segmentation,
                  gloss, pos, frequency, int(is_ambiguous), status))
    
    def get_wordform(self, wordform_id: str) -> Optional[Dict]:
        """Get a wordform by ID."""
        with self._connection() as conn:
            row = conn.execute(
                'SELECT * FROM wordforms WHERE wordform_id = ?', (wordform_id,)
            ).fetchone()
            return dict(row) if row else None
    
    def get_wordforms_for_lemma(self, lemma_id: str) -> List[Dict]:
        """Get all wordforms for a lemma."""
        with self._connection() as conn:
            rows = conn.execute('''
                SELECT * FROM wordforms WHERE lemma_id = ?
                ORDER BY frequency DESC
            ''', (lemma_id,)).fetchall()
            return [dict(row) for row in rows]
    
    # =========================================================================
    # Bulk Operations
    # =========================================================================
    
    def bulk_add_lemmas(self, lemmas: List[Lemma]):
        """Add multiple lemmas efficiently."""
        with self._connection() as conn:
            conn.executemany('''
                INSERT OR REPLACE INTO lemmas
                (lemma_id, citation_form, pos, entry_type, primary_gloss,
                 token_count, form_count, is_polysemous, needs_review,
                 entry_status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [(l.lemma_id, l.citation_form, l.pos, l.entry_type,
                   l.primary_gloss, l.token_count, l.form_count,
                   int(l.is_polysemous), int(l.needs_review),
                   l.entry_status, l.notes) for l in lemmas])
    
    def bulk_add_senses(self, senses: List[Sense]):
        """Add multiple senses efficiently."""
        with self._connection() as conn:
            conn.executemany('''
                INSERT OR REPLACE INTO senses
                (sense_id, lemma_id, sense_num, pos, gloss, definition,
                 usage_type, frequency, is_primary, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [(s.sense_id, s.lemma_id, s.sense_num, s.pos, s.gloss,
                   s.definition, s.usage_type, s.frequency,
                   int(s.is_primary), s.notes) for s in senses])
    
    def bulk_add_sources(self, sources: List[Source]):
        """Add multiple sources efficiently."""
        with self._connection() as conn:
            conn.executemany('''
                INSERT OR REPLACE INTO sources
                (source_id, iso, book_code, chapter, verse, text,
                 text_normalized, kjv_text, token_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', [(s.source_id, s.iso, s.book_code, s.chapter, s.verse,
                   s.text, s.text_normalized, s.kjv_text, s.token_count)
                  for s in sources])
    
    # =========================================================================
    # Statistics
    # =========================================================================
    
    def get_stats(self) -> Dict[str, int]:
        """Get corpus statistics."""
        with self._connection() as conn:
            stats = {}
            for table in ['sources', 'tokens', 'wordforms', 'lemmas', 
                          'senses', 'grammatical_morphemes', 'examples']:
                row = conn.execute(f'SELECT COUNT(*) FROM {table}').fetchone()
                stats[table] = row[0]
            
            # Review queue breakdown
            for status in ['open', 'resolved']:
                row = conn.execute(
                    'SELECT COUNT(*) FROM review_queue WHERE status = ?',
                    (status,)
                ).fetchone()
                stats[f'review_{status}'] = row[0]
            
            return stats


# =============================================================================
# Migration Script
# =============================================================================

def migrate_from_tsv(tsv_dir: str, db_path: str, iso: str = 'ctd'):
    """
    Migrate existing TSV exports to SQLite backend.
    
    Args:
        tsv_dir: Directory containing TSV files (e.g., data/ctd_analysis)
        db_path: Path to output SQLite database
        iso: ISO code for the language
    """
    import csv
    
    db = Backend(db_path)
    tsv_dir = Path(tsv_dir)
    
    # Add language
    db.add_language(iso, 'Tedim Chin' if iso == 'ctd' else iso,
                    f'bibles/extracted/{iso}/{iso}-x-bible.txt',
                    f'analyze_morphemes_{iso}' if iso != 'ctd' else 'analyze_morphemes')
    
    print(f"Migrating {iso} data from {tsv_dir} to {db_path}...")
    
    # Migrate verses/sources
    verses_file = tsv_dir / 'verses.tsv'
    if verses_file.exists():
        print("  Loading verses...")
        sources = []
        with open(verses_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                source_id = row.get('verse_id', row.get('source_id', ''))
                if not source_id or source_id.startswith('#'):
                    continue
                sources.append(Source(
                    source_id=source_id,
                    iso=iso,
                    book_code=source_id[:2] if len(source_id) >= 2 else '',
                    chapter=int(source_id[2:5]) if len(source_id) >= 5 else 0,
                    verse=int(source_id[5:8]) if len(source_id) >= 8 else 0,
                    text=row.get('tedim_text', row.get('text', '')),
                    text_normalized=row.get('tedim_text', row.get('text', '')).lower(),
                    kjv_text=row.get('kjv_text', ''),
                    token_count=int(row.get('token_count', 0) or 0)
                ))
        db.bulk_add_sources(sources)
        print(f"    Loaded {len(sources)} verses")
    
    # Migrate lemmas
    lemmas_file = tsv_dir / 'lemmas.tsv'
    if lemmas_file.exists():
        print("  Loading lemmas...")
        lemmas = []
        with open(lemmas_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                lemma_id = row.get('lemma', '')
                if not lemma_id or lemma_id.startswith('#'):
                    continue
                
                # Determine entry type
                is_gram = row.get('is_grammatical', '0') == '1'
                entry_type = 'grammatical' if is_gram else 'lexical'
                if row.get('entry_type'):
                    entry_type = row['entry_type']
                
                # Get primary gloss - fall back to first gloss_candidate if empty
                primary_gloss = row.get('primary_gloss', '')
                if not primary_gloss or primary_gloss == '?':
                    gloss_candidates = row.get('gloss_candidates', '')
                    if gloss_candidates:
                        primary_gloss = gloss_candidates.split('|')[0]
                
                lemmas.append(Lemma(
                    lemma_id=lemma_id,
                    citation_form=row.get('citation_form', lemma_id),
                    pos=row.get('pos', ''),
                    entry_type=entry_type,
                    primary_gloss=primary_gloss,
                    token_count=int(row.get('token_count', 0) or 0),
                    form_count=int(row.get('form_count', 0) or 0),
                    is_polysemous=row.get('is_polysemous', '0') == '1',
                    needs_review=row.get('needs_review', '0') == '1',
                    entry_status=row.get('entry_status', 'auto'),
                    notes=row.get('notes', '')
                ))
        db.bulk_add_lemmas(lemmas)
        print(f"    Loaded {len(lemmas)} lemmas")
    
    # Migrate senses
    senses_file = tsv_dir / 'senses.tsv'
    if senses_file.exists():
        print("  Loading senses...")
        senses = []
        with open(senses_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                sense_id = row.get('sense_id', '')
                if not sense_id or sense_id.startswith('#'):
                    continue
                senses.append(Sense(
                    sense_id=sense_id,
                    lemma_id=row.get('lemma', ''),
                    sense_num=int(row.get('sense_num', 1) or 1),
                    pos=row.get('pos', ''),
                    gloss=row.get('gloss', ''),
                    definition=row.get('definition', ''),
                    usage_type=row.get('usage_type', 'lexical') or 'lexical',
                    frequency=int(row.get('frequency', 0) or 0),
                    is_primary=row.get('is_primary', '0') == '1',
                    notes=row.get('notes', '')
                ))
        db.bulk_add_senses(senses)
        print(f"    Loaded {len(senses)} senses")
    
    # Migrate grammatical morphemes
    gram_file = tsv_dir / 'grammatical_morphemes.tsv'
    if gram_file.exists():
        print("  Loading grammatical morphemes...")
        count = 0
        with open(gram_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                form = row.get('form', '')
                if not form or form.startswith('#'):
                    continue
                
                morpheme_id = row.get('function_id', 
                    f"{form}.{row.get('gloss', '')}.{row.get('category', '')}")
                
                db.add_grammatical_morpheme(GrammaticalMorpheme(
                    morpheme_id=morpheme_id,
                    form=form,
                    gloss=row.get('gloss', ''),
                    function=row.get('gloss', ''),
                    category=row.get('category', ''),
                    subcategory=row.get('subcategory', ''),
                    position='prefix' if 'prefix' in row.get('category', '') else 'suffix',
                    frequency=int(row.get('frequency', 0) or 0),
                    environments=row.get('clean_environments', row.get('environments', '')),
                    is_polysemous=row.get('is_polysemous', '0') == '1',
                    status=row.get('status', 'auto'),
                    notes=''
                ))
                count += 1
        print(f"    Loaded {count} grammatical morphemes")
    
    # Migrate examples
    examples_file = tsv_dir / 'examples.tsv'
    if examples_file.exists():
        print("  Loading examples...")
        count = 0
        with open(examples_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                source_id = row.get('verse_id', '')
                if not source_id or source_id.startswith('#'):
                    continue
                
                db.add_example(Example(
                    example_id=0,  # Auto-assigned
                    source_id=source_id,
                    sense_id=row.get('sense_id', ''),
                    morpheme_id='',
                    target_form=row.get('item_id', ''),
                    tedim_text=row.get('tedim_text', ''),
                    segmented=row.get('segmented', ''),
                    glossed=row.get('glossed', ''),
                    kjv_text=row.get('kjv_text', ''),
                    quality=row.get('example_quality', 'acceptable'),
                    example_type=row.get('item_type', 'lemma'),
                    notes=''
                ))
                count += 1
        print(f"    Loaded {count} examples")
    
    # Migrate wordforms
    wordforms_file = tsv_dir / 'wordforms.tsv'
    if wordforms_file.exists():
        print("  Loading wordforms...")
        count = 0
        with open(wordforms_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                surface = row.get('surface_form', '')
                if not surface or surface.startswith('#'):
                    continue
                
                normalized = row.get('normalized_form', surface.lower())
                wordform_id = normalized  # Use normalized form as ID
                
                db.add_wordform(
                    wordform_id=wordform_id,
                    surface=surface,
                    normalized=normalized,
                    lemma_id=row.get('lemma', ''),
                    segmentation=row.get('segmentation', ''),
                    gloss=row.get('gloss', ''),
                    pos=row.get('pos', ''),
                    frequency=int(row.get('frequency', 0) or 0),
                    is_ambiguous=row.get('is_ambiguous', '0') == '1',
                    status=row.get('status', 'auto')
                )
                count += 1
        print(f"    Loaded {count} wordforms")
    
    # Migrate tokens (batch insert for performance)
    tokens_file = tsv_dir / 'tokens.tsv'
    if tokens_file.exists():
        print("  Loading tokens (this may take a moment)...")
        with db._connection() as conn:
            count = 0
            batch = []
            batch_size = 10000
            
            with open(tokens_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f, delimiter='\t')
                for row in reader:
                    source_id = row.get('verse_id', '')
                    if not source_id or source_id.startswith('#'):
                        continue
                    
                    normalized = row.get('normalized_form', row.get('surface_form', '').lower())
                    
                    batch.append((
                        source_id,
                        int(row.get('token_index', 0) or 0),
                        row.get('surface_form', ''),
                        normalized,
                        normalized,  # wordform_id = normalized
                        1 if row.get('is_sentence_final', '0') == '1' else 0
                    ))
                    count += 1
                    
                    if len(batch) >= batch_size:
                        conn.executemany('''
                            INSERT INTO tokens 
                            (source_id, position, surface, normalized, wordform_id, is_sentence_final)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', batch)
                        batch = []
                        print(f"    ... {count:,} tokens")
            
            # Final batch
            if batch:
                conn.executemany('''
                    INSERT INTO tokens 
                    (source_id, position, surface, normalized, wordform_id, is_sentence_final)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', batch)
        
        print(f"    Loaded {count:,} tokens")
    
    # Migrate ambiguities to review queue
    ambig_file = tsv_dir / 'ambiguities.tsv'
    if ambig_file.exists():
        print("  Loading review items from ambiguities...")
        count = 0
        with open(ambig_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                if row.get('status') == 'needs_review':
                    db.add_review_item(
                        entity_type='wordform',
                        entity_id=row.get('normalized_form', row.get('surface_form', '')),
                        reason=row.get('review_reasons', 'ambiguous'),
                        priority='high' if int(row.get('frequency', 0) or 0) > 1000 else 'medium'
                    )
                    count += 1
        print(f"    Loaded {count} review items")
    
    # Build morpheme_id index from grammatical_morphemes for example linking
    print("  Linking examples to morphemes...")
    morpheme_index = {}  # Maps (form, gloss) -> morpheme_id
    with db._connection() as conn:
        rows = conn.execute('SELECT morpheme_id, form, gloss FROM grammatical_morphemes').fetchall()
        for row in rows:
            key = (row['form'].lower(), row['gloss'].upper())
            morpheme_index[key] = row['morpheme_id']
    
    # Now re-process examples to derive morpheme_id from glossed field
    linked_count = 0
    unlinked = []  # Collect items needing review
    
    with db._connection() as conn:
        examples = conn.execute('''
            SELECT example_id, glossed, target_form, example_type FROM examples
        ''').fetchall()
        
        for ex in examples:
            example_id = ex['example_id']
            glossed = ex['glossed'] or ''
            target = ex['target_form'] or ''
            ex_type = ex['example_type']
            
            # Skip lemma examples - they're already sense-linked
            if ex_type == 'lemma':
                continue
            
            # Try to find morpheme matches in the gloss
            morpheme_id = None
            
            # Parse glossed string for morpheme glosses
            # Format is typically: stem-SUFFIX or PREFIX-stem-SUFFIX
            parts = glossed.replace('.', '-').split('-')
            
            for part in parts:
                part_upper = part.upper().strip()
                target_lower = target.lower().strip()
                
                # Check if this part matches a known grammatical morpheme
                key = (target_lower, part_upper)
                if key in morpheme_index:
                    morpheme_id = morpheme_index[key]
                    break
                
                # Also try just the gloss with common forms
                for form in [target_lower, target_lower.rstrip('aeiou')]:
                    key = (form, part_upper)
                    if key in morpheme_index:
                        morpheme_id = morpheme_index[key]
                        break
                if morpheme_id:
                    break
            
            if morpheme_id:
                conn.execute('''
                    UPDATE examples SET morpheme_id = ? WHERE example_id = ?
                ''', (morpheme_id, example_id))
                linked_count += 1
            elif ex_type == 'morpheme' and target:
                # Collect for review (add outside this connection)
                unlinked.append((example_id, target, glossed[:50]))
    
    # Add review items for unlinked morpheme examples (outside the connection)
    review_count = 0
    for example_id, target, glossed_snippet in unlinked:
        db.add_review_item(
            entity_type='example',
            entity_id=str(example_id),
            reason=f'Could not link morpheme example: target={target}, glossed={glossed_snippet}',
            priority='low'
        )
        review_count += 1
    
    print(f"    Linked {linked_count} examples to morphemes, {review_count} sent to review")
    
    # Generate morpheme examples from corpus if we have few linked examples
    print("  Generating additional morpheme examples from corpus...")
    
    # First, collect all the data we need
    examples_to_add = []
    
    with db._connection() as conn:
        # Get morphemes that have few or no examples
        morphemes = conn.execute('''
            SELECT gm.morpheme_id, gm.form, gm.gloss, gm.category,
                   COUNT(e.example_id) as example_count
            FROM grammatical_morphemes gm
            LEFT JOIN examples e ON gm.morpheme_id = e.morpheme_id
            GROUP BY gm.morpheme_id
            HAVING example_count < 3
            ORDER BY gm.frequency DESC
            LIMIT 100
        ''').fetchall()
        
        for morph in morphemes:
            morpheme_id = morph['morpheme_id']
            form = morph['form']
            gloss = morph['gloss']
            
            # Find tokens containing this morpheme in their gloss
            pattern = f'%{gloss}%'
            candidates = conn.execute('''
                SELECT wf.normalized, wf.segmentation, wf.gloss, 
                       s.source_id, s.text, s.kjv_text
                FROM wordforms wf
                JOIN tokens t ON wf.wordform_id = t.wordform_id
                JOIN sources s ON t.source_id = s.source_id
                WHERE wf.gloss LIKE ?
                AND wf.segmentation LIKE ?
                GROUP BY s.source_id
                ORDER BY RANDOM()
                LIMIT 5
            ''', (pattern, f'%{form}%')).fetchall()
            
            morpheme_example_count = 0
            for cand in candidates:
                # Check if we already have an example from this source
                existing = conn.execute('''
                    SELECT 1 FROM examples 
                    WHERE morpheme_id = ? AND source_id = ?
                ''', (morpheme_id, cand['source_id'])).fetchone()
                
                if not existing:
                    examples_to_add.append(Example(
                        example_id=0,
                        source_id=cand['source_id'],
                        sense_id='',
                        morpheme_id=morpheme_id,
                        target_form=cand['normalized'],
                        tedim_text=cand['text'],
                        segmented=cand['segmentation'],
                        glossed=cand['gloss'],
                        kjv_text=cand['kjv_text'] or '',
                        quality='auto',
                        example_type='morpheme',
                        notes='auto-generated from corpus'
                    ))
                    morpheme_example_count += 1
                    if morpheme_example_count >= 3:
                        break
    
    # Now add examples outside the connection
    added_examples = 0
    for example in examples_to_add:
        db.add_example(example)
        added_examples += 1
    
    # Migration summary
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)
    
    # Count examples by type
    with db._connection() as conn:
        # Examples with sense_id from TSV
        direct_sense = conn.execute('''
            SELECT COUNT(*) FROM examples 
            WHERE sense_id IS NOT NULL AND sense_id != '' 
            AND example_type = 'lemma'
        ''').fetchone()[0]
        
        # Examples linked to morphemes
        morpheme_linked = conn.execute('''
            SELECT COUNT(*) FROM examples 
            WHERE morpheme_id IS NOT NULL AND morpheme_id != ''
        ''').fetchone()[0]
        
        # Auto-generated examples
        auto_generated = conn.execute('''
            SELECT COUNT(*) FROM examples 
            WHERE quality = 'auto' AND notes LIKE '%auto-generated%'
        ''').fetchone()[0]
        
        # Total examples
        total_examples = conn.execute('SELECT COUNT(*) FROM examples').fetchone()[0]
    
    print(f"\nExamples:")
    print(f"  Direct from TSV (with sense_id): {direct_sense:,}")
    print(f"  Linked to morphemes (heuristic): {linked_count:,}")
    print(f"  Auto-generated from corpus:      {added_examples:,}")
    print(f"  Sent to review (unlinked):       {review_count:,}")
    print(f"  Total examples:                  {total_examples:,}")
    
    # Print full stats
    stats = db.get_stats()
    print(f"\nDatabase statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:,}")
    
    print("\n" + "=" * 60)
    
    return db


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Kuki-Chin Backend')
    subparsers = parser.add_subparsers(dest='command')
    
    # migrate command
    migrate_parser = subparsers.add_parser('migrate', 
        help='Migrate TSV exports to SQLite')
    migrate_parser.add_argument('--tsv-dir', default='data/ctd_analysis',
        help='Directory containing TSV files')
    migrate_parser.add_argument('--db', default='data/ctd_backend.db',
        help='Output database path')
    migrate_parser.add_argument('--iso', default='ctd',
        help='ISO code for the language')
    
    # stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.add_argument('--db', default='data/ctd_backend.db',
        help='Database path')
    
    # lookup command
    lookup_parser = subparsers.add_parser('lookup', help='Look up a word')
    lookup_parser.add_argument('word', help='Word to look up')
    lookup_parser.add_argument('--db', default='data/ctd_backend.db',
        help='Database path')
    
    args = parser.parse_args()
    
    if args.command == 'migrate':
        migrate_from_tsv(args.tsv_dir, args.db, args.iso)
    
    elif args.command == 'stats':
        db = Backend(args.db)
        stats = db.get_stats()
        print("Database statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value:,}")
    
    elif args.command == 'lookup':
        db = Backend(args.db)
        lemma = db.get_lemma(args.word)
        if lemma:
            print(f"\n{lemma.citation_form} ({lemma.pos})")
            print(f"  Gloss: {lemma.primary_gloss}")
            print(f"  Type: {lemma.entry_type}")
            print(f"  Frequency: {lemma.token_count:,}")
            
            senses = db.get_senses(args.word)
            if senses:
                print(f"\n  Senses ({len(senses)}):")
                for s in senses:
                    marker = '*' if s.is_primary else ' '
                    print(f"    {marker}{s.sense_num}. {s.gloss} ({s.usage_type}, freq={s.frequency:,})")
            
            examples = db.get_examples_for_lemma(args.word, limit=3)
            if examples:
                print(f"\n  Examples ({len(examples)}):")
                for e in examples:
                    print(f"    {e.source_id}: {e.tedim_text[:60]}...")
                    print(f"      {e.glossed[:60]}...")
        else:
            # Try search
            results = db.search_lemmas(args.word, limit=10)
            if results:
                print(f"No exact match. Similar entries:")
                for r in results:
                    print(f"  {r.citation_form}: {r.primary_gloss} ({r.pos})")
            else:
                print(f"No entries found for '{args.word}'")
    
    else:
        parser.print_help()
