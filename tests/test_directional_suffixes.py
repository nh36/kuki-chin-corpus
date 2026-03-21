#!/usr/bin/env python3
"""
Regression tests for directional suffix glossing.

Tests that -suk, -phei, -toh, and other directional suffixes are glossed
correctly as directionals (DOWN, HORIZ, UP) rather than as causatives.

Based on ZNC §5.8.2.3 three-way elevational system:
- -toh: UP (upward motion)
- -suk: DOWN (downward motion)  
- -phei: HORIZ (horizontal/level motion)

Note: -toh is polysemous - it can mean UP (elevational) or "with" (comitative).
The compound entries disambiguate based on semantic context.
"""

import sys
import unittest
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

class TestDirectionalSuffixes(unittest.TestCase):
    """Test directional suffix glossing."""
    
    def test_suk_as_down_suffix(self):
        """Test that -suk is glossed as DOWN when used as suffix."""
        test_cases = [
            ('paisuk', 'go-DOWN'),
            ('kumsuk', 'bow-DOWN'),
            ('ensuk', 'look-DOWN'),
            ('khiasuk', 'exit-DOWN'),
            ('lumsuk', 'rest-DOWN'),
        ]
        for word, expected_gloss in test_cases:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss, 
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_suk_with_applicative(self):
        """Test -suk with applicative -pih."""
        result = analyze_word('paipihsuk')
        self.assertIsNotNone(result)
        seg, gloss = result
        self.assertEqual(gloss, 'go-APPL-DOWN')
    
    def test_suk_as_prefix(self):
        """Test suk- as prefix in compounds."""
        test_cases = [
            ('sukgawp', 'DOWN-grasp'),
            ('sukkhak', 'DOWN-restrain'),
        ]
        for word, expected_gloss in test_cases:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_toh_polysemy(self):
        """Test that -toh handles UP vs comitative correctly.
        
        -toh is polysemous:
        - With motion verbs: often comitative "go with"
        - With other verbs: can be elevational "UP"
        Compound entries disambiguate.
        """
        # paitoh is lexicalized as "go-accompany" (comitative)
        result = analyze_word('paitoh')
        self.assertIsNotNone(result)
        seg, gloss = result
        self.assertEqual(gloss, 'go-accompany', 
            f"paitoh should be 'go-accompany', got '{gloss}'")
    
    def test_suk_not_causative(self):
        """Ensure -suk is NOT glossed as CAUS or make.become."""
        test_words = ['paisuk', 'kumsuk', 'ensuk', 'khiasuk', 'lumsuk']
        for word in test_words:
            result = analyze_word(word)
            self.assertIsNotNone(result)
            seg, gloss = result
            self.assertNotIn('CAUS', gloss, 
                f"{word} should not contain CAUS, got '{gloss}'")
            self.assertNotIn('make.become', gloss,
                f"{word} should not contain make.become, got '{gloss}'")

class TestDirectionalSuffixInventory(unittest.TestCase):
    """Test that directional suffixes are in the correct dictionaries."""
    
    def test_directional_suffixes_dict(self):
        """Test DIRECTIONAL_SUFFIXES contains correct entries."""
        from analyze_morphemes import DIRECTIONAL_SUFFIXES
        
        # Note: some entries use lowercase, some uppercase
        expected = {
            'khia': 'out',
            'khiat': 'away',
            'lut': 'in',
            'toh': 'UP',
            'suk': 'DOWN',
            'phei': 'HORIZ',
        }
        for suffix, gloss in expected.items():
            self.assertIn(suffix, DIRECTIONAL_SUFFIXES,
                f"{suffix} should be in DIRECTIONAL_SUFFIXES")
            self.assertEqual(DIRECTIONAL_SUFFIXES[suffix], gloss,
                f"DIRECTIONAL_SUFFIXES['{suffix}'] should be '{gloss}'")
    
    def test_tam_suffixes_consistent(self):
        """Test TAM_SUFFIXES has consistent directional glosses."""
        from analyze_morphemes import TAM_SUFFIXES
        
        # These should match DIRECTIONAL_SUFFIXES
        self.assertEqual(TAM_SUFFIXES.get('suk'), 'DOWN')
        self.assertEqual(TAM_SUFFIXES.get('toh'), 'UP')

if __name__ == '__main__':
    unittest.main(verbosity=2)
