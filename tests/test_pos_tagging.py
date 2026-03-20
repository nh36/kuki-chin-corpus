#!/usr/bin/env python3
"""
Tests for POS tagging functionality.

These tests ensure that:
1. Word classes are correctly identified
2. Verbs are distinguished from nouns
3. Agreement markers are recognized
4. Subordinators and sentence-final markers are tagged
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_morphemes import (
    analyze_word,
    get_word_class,
    VERB_STEMS,
    DEMONSTRATIVES,
    NUMERALS,
    QUANTIFIERS,
    PROPERTY_WORDS,
    COORDINATOR,
    SUBORDINATORS,
    PRONOUNS,
    NEGATION,
)


class TestPOSTagging(unittest.TestCase):
    """Test POS tagging accuracy."""
    
    def test_demonstratives(self):
        """Demonstratives should be tagged as DEM."""
        for word in ['hih', 'tua', 'tuate', 'hihte']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'DEM', f"{word} should be DEM")
    
    def test_numerals(self):
        """Numerals should be tagged as NUM."""
        for word in ['khat', 'nih', 'thum', 'li', 'nga', 'sawm', 'za']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'NUM', f"{word} should be NUM")
    
    def test_quantifiers(self):
        """Quantifiers should be tagged as QUANT."""
        for word in ['khempeuh', 'tampi', 'pawlkhat']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'QUANT', f"{word} should be QUANT")
    
    def test_property_words(self):
        """Property words should be tagged as PROP."""
        for word in ['hoih', 'sia', 'lian', 'neu']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'PROP', f"{word} should be PROP")
    
    def test_coordinator(self):
        """Coordinator 'le' should be tagged as COORD."""
        seg, gloss = analyze_word('le')
        self.assertEqual(get_word_class('le', gloss), 'COORD')
    
    def test_subordinators(self):
        """Subordinators should be tagged as SUBORD."""
        for word in ['ciangin', 'hangin', 'bangin', 'dingin']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'SUBORD', f"{word} should be SUBORD")
    
    def test_negation(self):
        """Negation markers should be tagged as NEG."""
        for word in ['lo', 'kei']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'NEG', f"{word} should be NEG")
    
    def test_agreement_markers(self):
        """Agreement markers should be tagged as AGR."""
        for word in ['a', 'ka', 'na', 'i']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'AGR', f"{word} should be AGR")
    
    def test_case_markers(self):
        """Case markers should be tagged as CASE."""
        for word in ['in', 'ah', 'tawh']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'CASE', f"{word} should be CASE")
    
    def test_sentence_final(self):
        """Sentence-final markers should be tagged as SFIN."""
        for word in ['hi', 'hiam', 'hen']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'SFIN', f"{word} should be SFIN")
    
    def test_verbs_basic(self):
        """Basic verb stems should be tagged as V."""
        # Note: 'za' is ambiguous (hear vs hundred), 'om' is PROP (stative verb)
        for word in ['mu', 'muh', 'zak', 'nei', 'pai', 'ci', 'bawl']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'V', f"{word} should be V")
    
    def test_verbs_with_suffixes(self):
        """Verbs with suffixes should be tagged as V."""
        for word in ['muding', 'paikik', 'omta', 'nehzo']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'V', f"{word} should be V")
    
    def test_verbs_compound(self):
        """Compound verbs (verb + directional) should be tagged as V."""
        # These are verb + directional combinations
        test_cases = [
            ('paisuak', 'go + become'),  # go-out
            ('hongpai', 'come + go'),
            ('piangsak', 'cause birth'),
        ]
        for word, desc in test_cases:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'V', f"{word} ({desc}) should be V")
    
    def test_proper_nouns(self):
        """Proper nouns should be tagged as N.PROP."""
        for word in ['Pasian', 'Moses', 'Israel', 'Abraham']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'N.PROP', f"{word} should be N.PROP")
    
    def test_plural_nouns(self):
        """Plural nouns should be tagged as N.PL."""
        seg, gloss = analyze_word('mite')
        self.assertEqual(get_word_class('mite', gloss), 'N.PL')
    
    def test_pronouns(self):
        """Pronouns should be tagged as PRO."""
        for word in ['amah', 'eite', 'amaute']:
            seg, gloss = analyze_word(word)
            self.assertEqual(get_word_class(word, gloss), 'PRO', f"{word} should be PRO")


class TestPOSDictionaries(unittest.TestCase):
    """Test that POS dictionaries are well-formed."""
    
    def test_subordinators_dict_exists(self):
        """SUBORDINATORS dict should exist and have entries."""
        self.assertIsInstance(SUBORDINATORS, dict)
        self.assertGreater(len(SUBORDINATORS), 5)
    
    def test_pronouns_dict_exists(self):
        """PRONOUNS dict should exist and have entries."""
        self.assertIsInstance(PRONOUNS, dict)
        self.assertGreater(len(PRONOUNS), 5)
    
    def test_no_overlap_demonstratives_quantifiers(self):
        """Demonstratives and quantifiers should not overlap."""
        overlap = set(DEMONSTRATIVES.keys()) & set(QUANTIFIERS.keys())
        self.assertEqual(len(overlap), 0, f"Overlap: {overlap}")
    
    def test_no_overlap_numerals_quantifiers(self):
        """Numerals and quantifiers should not overlap."""
        overlap = set(NUMERALS.keys()) & set(QUANTIFIERS.keys())
        self.assertEqual(len(overlap), 0, f"Overlap: {overlap}")


if __name__ == '__main__':
    unittest.main()
