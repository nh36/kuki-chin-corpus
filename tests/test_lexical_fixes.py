#!/usr/bin/env python3
"""
Regression tests for lexical fixes.

Tests verify correct analysis of words that were previously mis-analyzed
due to incorrect compound entries or missing lexical entries.
"""

import unittest
import sys
sys.path.insert(0, 'scripts')

from analyze_morphemes import analyze_word


class TestSamzangHair(unittest.TestCase):
    """Test that samzang is correctly analyzed as 'hair'.
    
    Previously mis-analyzed as 'sam-zang' = 'throw-INSTR'.
    All 8 corpus occurrences mean 'hair':
    - Judg 20:16: "at an hair breadth"
    - 1Sam 14:45: "not one hair of his head fall"
    - 2Sam 14:11: "not one hair of thy son fall"
    - 1Kgs 1:52: "not an hair of him fall"
    - Ps 69:4: "hairs of mine head"
    - Prov 23:7: contextual
    - Matt 5:36: "one hair white or black"
    - Luke 21:18: "not an hair of your head perish"
    """
    
    def test_samzang_is_hair(self):
        """samzang should be atomic 'hair', not 'throw-INSTR'."""
        seg, gloss = analyze_word('samzang')
        self.assertEqual(seg, 'samzang')
        self.assertEqual(gloss, 'hair')
    
    def test_samzangte_is_hair_plural(self):
        """samzangte should be 'hair-PL'."""
        seg, gloss = analyze_word('samzangte')
        self.assertEqual(seg, 'samzang-te')
        self.assertEqual(gloss, 'hair-PL')
    
    def test_samzang_not_throw_instr(self):
        """Verify samzang is NOT parsed as sam-zang throw-INSTR."""
        seg, gloss = analyze_word('samzang')
        self.assertNotIn('throw', gloss)
        self.assertNotIn('INSTR', gloss)


class TestKapinWeep(unittest.TestCase):
    """Test that kapin is correctly analyzed as 'weep-CVB'.
    
    Previously incorrectly listed as kapin='among' in STEMS.
    Corpus analysis: 43/44 occurrences (97.7%) are 'kap-in' = 'weep-CVB'.
    
    One edge case (Judg 20:16): 'samzang kapin' in "sling stones at an hair
    breadth" - meaning possibly "precisely/touching" but we treat as weep-CVB
    since it's an outlier. Noted in grammar documentation.
    """
    
    def test_kapin_is_weep_cvb(self):
        """kapin should parse compositionally as 'kap-in' = 'weep-CVB'."""
        seg, gloss = analyze_word('kapin')
        self.assertEqual(seg, 'kap-in')
        self.assertEqual(gloss, 'weep-CVB')
    
    def test_kapin_not_among(self):
        """Verify kapin is NOT analyzed as 'among'."""
        seg, gloss = analyze_word('kapin')
        self.assertNotEqual(gloss, 'among')
        self.assertNotIn('among', gloss)
    
    def test_kap_is_weep(self):
        """Base form kap should mean 'weep'."""
        seg, gloss = analyze_word('kap')
        self.assertEqual(seg, 'kap')
        self.assertEqual(gloss, 'weep')


if __name__ == '__main__':
    unittest.main()
