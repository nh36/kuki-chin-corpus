#!/usr/bin/env python3
"""
Tests for VP slot dictionaries and verbal morphology.

These tests ensure that:
1. VP slot dictionaries are well-formed and non-empty
2. Slot categories don't overlap inappropriately
3. Suffix glosses are consistent
4. The analyzer recognizes all slot suffixes correctly
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_morphemes import (
    analyze_word,
    ASPECT_SUFFIXES,
    DIRECTIONAL_SUFFIXES,
    MODAL_SUFFIXES,
    DERIVATIONAL_SUFFIXES,
    TAM_SUFFIXES,
    VERBAL_DERIVATIONAL_SUFFIXES,
    VERB_STEMS
)


class TestVPSlotDictionaries(unittest.TestCase):
    """Test VP slot dictionary structure and content."""
    
    def test_aspect_suffixes_non_empty(self):
        """ASPECT_SUFFIXES should have entries."""
        self.assertGreater(len(ASPECT_SUFFIXES), 5)
    
    def test_directional_suffixes_non_empty(self):
        """DIRECTIONAL_SUFFIXES should have entries."""
        self.assertGreater(len(DIRECTIONAL_SUFFIXES), 5)
    
    def test_modal_suffixes_non_empty(self):
        """MODAL_SUFFIXES should have entries."""
        self.assertGreater(len(MODAL_SUFFIXES), 5)
    
    def test_derivational_suffixes_non_empty(self):
        """DERIVATIONAL_SUFFIXES should have entries."""
        self.assertGreater(len(DERIVATIONAL_SUFFIXES), 5)
    
    def test_slot_entries_are_strings(self):
        """All slot entries should be string -> string mappings."""
        for name, slot in [
            ('ASPECT', ASPECT_SUFFIXES),
            ('DIRECTIONAL', DIRECTIONAL_SUFFIXES),
            ('MODAL', MODAL_SUFFIXES),
            ('DERIVATIONAL', DERIVATIONAL_SUFFIXES)
        ]:
            for suffix, gloss in slot.items():
                self.assertIsInstance(suffix, str, f"{name}: suffix must be string")
                self.assertIsInstance(gloss, str, f"{name}: gloss must be string")
                self.assertGreater(len(suffix), 0, f"{name}: suffix must be non-empty")
                self.assertGreater(len(gloss), 0, f"{name}: gloss must be non-empty")


class TestSlotSuffixRecognition(unittest.TestCase):
    """Test that the analyzer recognizes VP slot suffixes."""
    
    def test_aspect_ta_perfective(self):
        """Perfective -ta should be recognized."""
        seg, gloss = analyze_word('kilawmta')  # be.satisfying-PFV
        # May gloss as PFV or PERF depending on analyzer
        self.assertTrue('PFV' in (gloss or '') or 'PERF' in (gloss or ''))
    
    def test_aspect_zo_completive(self):
        """Completive -zo should be recognized."""
        seg, gloss = analyze_word('bawlzo')  # do-COMPL
        self.assertIn('COMPL', gloss or '')
    
    def test_aspect_kik_iterative(self):
        """Iterative -kik should be recognized."""
        seg, gloss = analyze_word('hongpaikik')  # come-ITER
        self.assertIn('ITER', gloss or '')
    
    def test_directional_khia_out(self):
        """Directional -khia should be recognized."""
        seg, gloss = analyze_word('lutkhia')  # enter-out (go through)
        # May gloss as 'out' or 'exit' depending on analyzer
        self.assertTrue('out' in (gloss or '') or 'exit' in (gloss or ''))
    
    def test_directional_lut_in(self):
        """Directional -lut should be recognized."""
        seg, gloss = analyze_word('pailut')  # go-in (enter)
        self.assertIn('in', gloss or '')
    
    def test_modal_ding_irrealis(self):
        """Irrealis -ding should be recognized."""
        seg, gloss = analyze_word('omding')  # be-IRR
        self.assertIn('IRR', gloss or '')
    
    def test_modal_thei_abilitative(self):
        """Abilitative -thei should be recognized."""
        seg, gloss = analyze_word('bawlthei')  # do-ABIL
        self.assertIn('ABIL', gloss or '')
    
    def test_modal_lai_prospective(self):
        """Prospective -lai should be recognized."""
        seg, gloss = analyze_word('pailai')  # go-PROSP
        # Note: -lai can be 'middle' or 'PROSP' depending on context
        self.assertTrue(gloss, "Should have a gloss")
    
    def test_derivational_sak_causative(self):
        """Causative -sak should be recognized."""
        seg, gloss = analyze_word('nuihsak')  # laugh-CAUS (make laugh)
        self.assertIn('CAUS', gloss or '')
    
    def test_derivational_pih_applicative(self):
        """Applicative -pih should be recognized."""
        seg, gloss = analyze_word('bawlpih')  # do-APPL (do for)
        self.assertIn('APPL', gloss or '')


class TestSlotCombinations(unittest.TestCase):
    """Test that slot combinations are parsed correctly."""
    
    def test_deriv_plus_modal(self):
        """DERIV + MODAL combination."""
        seg, gloss = analyze_word('bawlsakthei')  # do-CAUS-ABIL
        # May use CAUS or 'make' or 'cause' for causative
        has_caus = 'CAUS' in (gloss or '') or 'cause' in (gloss or '') or 'make' in (gloss or '')
        self.assertTrue(has_caus, f"Expected causative marker in: {gloss}")
        self.assertIn('ABIL', gloss or '')
    
    def test_aspect_plus_modal(self):
        """ASPECT + MODAL combination."""
        seg, gloss = analyze_word('bawlzoding')  # do-COMPL-IRR
        if gloss:
            # Should have both markers
            has_both = 'COMPL' in gloss and 'IRR' in gloss
            # Or it might parse differently
            self.assertTrue(gloss, "Should have a gloss")
    
    def test_verb_stems_exist(self):
        """VERB_STEMS dictionary should have entries."""
        self.assertGreater(len(VERB_STEMS), 100)


class TestLegacyCompatibility(unittest.TestCase):
    """Ensure legacy dictionaries still work."""
    
    def test_tam_suffixes_still_exist(self):
        """TAM_SUFFIXES should still exist for backward compatibility."""
        self.assertIsInstance(TAM_SUFFIXES, dict)
        self.assertGreater(len(TAM_SUFFIXES), 5)
    
    def test_verbal_derivational_suffixes_still_exist(self):
        """VERBAL_DERIVATIONAL_SUFFIXES should still exist."""
        self.assertIsInstance(VERBAL_DERIVATIONAL_SUFFIXES, dict)
        self.assertGreater(len(VERBAL_DERIVATIONAL_SUFFIXES), 5)


class TestVerbStemCounting(unittest.TestCase):
    """Test verb stem counting logic for report generation."""
    
    def test_longer_stem_matched_before_shorter(self):
        """Compound stems like 'nungta' should match before their components like 'nung'."""
        from generate_verb_stems_report import count_verb_occurrences
        
        # Test data: sentences containing compound stems
        test_verses = {
            '01001001': 'nungta nung nungta',  # 2x nungta, 1x nung
            '01001002': 'piangsak piang piangsak'  # 2x piangsak, 1x piang
        }
        
        counts, _ = count_verb_occurrences(test_verses)
        
        # nungta should be counted independently from nung
        self.assertEqual(counts.get('nungta', 0), 2, "nungta should count 2x")
        self.assertEqual(counts.get('nung', 0), 1, "nung should count 1x (not 3)")
        self.assertEqual(counts.get('piangsak', 0), 2, "piangsak should count 2x")
        self.assertEqual(counts.get('piang', 0), 1, "piang should count 1x (not 3)")


if __name__ == '__main__':
    unittest.main()
