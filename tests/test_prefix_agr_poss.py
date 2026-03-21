#!/usr/bin/env python3
"""
Regression tests for pronominal prefix AGR/POSS distinction.

Based on Henderson (1965):
- ka-/na-/a- on VERBS = agreement markers (1SG, 2SG, 3SG)
- ka-/na-/a- on NOUNS = possessive markers (1SG.POSS, 2SG.POSS, 3SG.POSS)
"""

import sys
import unittest
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word, PRONOMINAL_PREFIXES

class TestPrefixAgrPoss(unittest.TestCase):
    """Test agreement vs possessive distinction for pronominal prefixes."""
    
    def test_prefix_plus_noun_is_poss(self):
        """Test that prefix + noun gets POSS gloss."""
        # inn = house (noun)
        test_cases = [
            ('kainn', '1SG.POSS-house'),
            ('nainn', '2SG.POSS-house'),
            ('ainn', '3SG.POSS-house'),
        ]
        for word, expected_gloss in test_cases:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_prefix_plus_verb_is_agr(self):
        """Test that prefix + verb keeps AGR gloss (no POSS)."""
        # nei = have (verb)
        test_cases = [
            ('kanei', '1SG-have'),
            ('nanei', '2SG-have'),
        ]
        for word, expected_gloss in test_cases:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_prefix_plus_form_ii_verb_is_agr(self):
        """Test that prefix + Form II verb keeps AGR gloss."""
        test_cases = [
            ('kaneih', '1SG-have.II'),
            ('naneih', '2SG-have.II'),
        ]
        for word, expected_gloss in test_cases:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_poss_marker_format(self):
        """Test that POSS markers have correct format."""
        result = analyze_word('kainn')
        self.assertIsNotNone(result)
        seg, gloss = result
        self.assertIn('.POSS', gloss, f"Should have .POSS suffix, got '{gloss}'")
        self.assertTrue(gloss.startswith('1SG.POSS'),
            f"Should start with 1SG.POSS, got '{gloss}'")
    
    def test_agr_no_poss_marker(self):
        """Test that AGR markers do NOT have .POSS suffix."""
        test_words = ['kanei', 'nanei', 'kaneih', 'naneih']
        for word in test_words:
            result = analyze_word(word)
            if result:
                seg, gloss = result
                self.assertNotIn('.POSS', gloss,
                    f"{word} should not have .POSS, got '{gloss}'")


class TestPronominalPrefixes(unittest.TestCase):
    """Test the PRONOMINAL_PREFIXES dictionary."""
    
    def test_pronominal_prefixes_exist(self):
        """Test that expected prefixes are defined."""
        expected = {'ka': '1SG', 'na': '2SG', 'a': '3SG', 'i': '1PL.INCL'}
        for prefix, gloss in expected.items():
            self.assertIn(prefix, PRONOMINAL_PREFIXES,
                f"'{prefix}' should be in PRONOMINAL_PREFIXES")
            self.assertEqual(PRONOMINAL_PREFIXES[prefix], gloss,
                f"PRONOMINAL_PREFIXES['{prefix}'] should be '{gloss}'")


if __name__ == '__main__':
    unittest.main(verbosity=2)
