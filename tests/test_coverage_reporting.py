#!/usr/bin/env python3
"""
Coverage Reporting Tests

These tests verify that coverage measurement is accurate and consistent.
They are separate from morphological parsing tests.

Key requirements:
1. URL fragments and non-word tokens must not be counted
2. Pure punctuation must not be counted as unknown
3. Coverage percentage must be calculated correctly
4. Results must be reproducible
"""

import sys
import re
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_morphemes import analyze_word


def is_tedim_word(token: str) -> bool:
    """
    Determine if a token is a valid Tedim word that should be counted.
    
    Excludes:
    - Pure punctuation
    - URL fragments (http, www, bible, com, etc.)
    - Numeric-only tokens
    - Empty strings
    """
    # Strip surrounding punctuation
    clean = re.sub(r'^[^\w\'\']+|[^\w\'\']+$', '', token)
    
    # Must have alphabetic content
    if not clean or not re.search(r'[a-zA-Z]', clean):
        return False
    
    # Exclude URL fragments
    url_fragments = {'http', 'https', 'www', 'com', 'org', 'bible', 'biblecom'}
    if clean.lower() in url_fragments:
        return False
    
    # Exclude tokens that look like URLs
    if clean.lower().startswith('http') or 'www' in clean.lower():
        return False
    
    return True


def count_coverage(bible_path: str) -> dict:
    """
    Count coverage statistics for the Bible text.
    
    Returns dict with:
    - total: count of valid Tedim words
    - full: words with complete glosses
    - partial: words with ? in gloss
    - unknown: words with no gloss
    """
    total, full, partial, unknown = 0, 0, 0, 0
    
    with open(bible_path) as f:
        for line in f:
            if not line.strip() or '\t' not in line:
                continue
            verse_id, text = line.strip().split('\t', 1)
            
            for token in text.split():
                if not is_tedim_word(token):
                    continue
                
                # Clean for analysis
                clean = re.sub(r'^[^\w\'\']+|[^\w\'\']+$', '', token)
                
                total += 1
                result = analyze_word(clean)
                
                if result and result[1]:
                    if '?' in result[1]:
                        partial += 1
                    else:
                        full += 1
                else:
                    unknown += 1
    
    return {
        'total': total,
        'full': full,
        'partial': partial,
        'unknown': unknown,
        'coverage': 100 * full / total if total > 0 else 0
    }


class TestCoverageReporting(unittest.TestCase):
    """Tests for coverage measurement accuracy."""
    
    @classmethod
    def setUpClass(cls):
        """Set up paths."""
        cls.repo_root = Path(__file__).parent.parent
        cls.bible_path = cls.repo_root / 'bibles/extracted/ctd/ctd-x-bible.txt'
    
    def test_url_fragments_not_counted(self):
        """URL fragments should not be counted as words."""
        url_tokens = [
            'httpswwwbiblecombible368',
            'biblecom',
            'http',
            'https',
            'www',
        ]
        for token in url_tokens:
            self.assertFalse(
                is_tedim_word(token),
                f"URL fragment '{token}' should not be counted as a word"
            )
    
    def test_punctuation_not_counted(self):
        """Pure punctuation should not be counted."""
        punct_tokens = [
            '"', '"', "'", ',', '.', '!', '?',
            '—', '--',
        ]
        for token in punct_tokens:
            self.assertFalse(
                is_tedim_word(token),
                f"Punctuation '{repr(token)}' should not be counted as a word"
            )
    
    def test_valid_tedim_words_counted(self):
        """Valid Tedim words should be counted."""
        valid_words = [
            'Pasian', 'tungah', 'mite', 'khempeuh',
            'pan', 'kipan', 'langpangin', "mite'",
        ]
        for word in valid_words:
            self.assertTrue(
                is_tedim_word(word),
                f"Valid word '{word}' should be counted"
            )
    
    def test_no_unknown_words(self):
        """There should be zero unknown words (100% coverage)."""
        if not self.bible_path.exists():
            self.skipTest("Bible file not found")
        
        stats = count_coverage(str(self.bible_path))
        self.assertEqual(
            stats['unknown'], 0,
            f"Expected 0 unknown words, got {stats['unknown']}"
        )
    
    def test_no_partial_glosses(self):
        """There should be zero partial glosses."""
        if not self.bible_path.exists():
            self.skipTest("Bible file not found")
        
        stats = count_coverage(str(self.bible_path))
        self.assertEqual(
            stats['partial'], 0,
            f"Expected 0 partial glosses, got {stats['partial']}"
        )
    
    def test_coverage_is_100_percent(self):
        """Coverage should be 100%."""
        if not self.bible_path.exists():
            self.skipTest("Bible file not found")
        
        stats = count_coverage(str(self.bible_path))
        self.assertEqual(
            stats['coverage'], 100.0,
            f"Expected 100% coverage, got {stats['coverage']:.4f}%"
        )
    
    def test_total_word_count_stable(self):
        """Total word count should be stable (within expected range)."""
        if not self.bible_path.exists():
            self.skipTest("Bible file not found")
        
        stats = count_coverage(str(self.bible_path))
        # Expected range based on known corpus size
        self.assertGreater(stats['total'], 825000)
        self.assertLess(stats['total'], 835000)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
