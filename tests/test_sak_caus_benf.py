#!/usr/bin/env python3
"""
Regression tests for -sak causative/benefactive distinction.

Based on Otsuka (2009): 
- Form I + -sak = CAUS (causative)
- Form II + -sak = BENF (benefactive)

Form I: mu, ci, nei, thei, tua, bawl, gen, etc.
Form II: muh, cih, neih, theih, tuah, bawlh, genh, etc.
"""

import sys
import unittest
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word, VERB_STEM_PAIRS

class TestSakCausBenf(unittest.TestCase):
    """Test -sak CAUS/BENF distinction based on verb stem form."""
    
    def test_form_ii_plus_sak_is_benf(self):
        """Test that Form II stems + -sak get BENF gloss."""
        form_ii_words = [
            ('muhsak', 'see.II-BENF'),
            ('cihsak', 'say.II-BENF'),
            ('neihsak', 'have.II-BENF'),
            ('theihsak', 'know.II-BENF'),
            ('tuahsak', 'do.II-BENF'),
            ('bawlhsak', 'make.II-BENF'),
            ('genhsak', 'speak.II-BENF'),
        ]
        for word, expected_gloss in form_ii_words:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_form_ii_marker_in_gloss(self):
        """Test that Form II stems get .II marker in gloss."""
        for word in ['muhsak', 'tuahsak', 'bawlhsak']:
            result = analyze_word(word)
            self.assertIsNotNone(result)
            seg, gloss = result
            self.assertIn('.II', gloss,
                f"{word} should have .II marker, got '{gloss}'")
    
    def test_form_i_plus_sak_is_caus(self):
        """Test that non-Form-II stems + -sak get CAUS gloss."""
        form_i_words = [
            ('damsak', 'well-CAUS'),  # dam is not alternating
            ('paisak', 'go-CAUS'),    # pai is not alternating
        ]
        for word, expected_gloss in form_i_words:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_lexicalized_sak_compounds(self):
        """Test that some V+sak compounds are lexicalized."""
        # These are treated as single morphemes with their own meanings
        lexicalized = [
            ('musak', 'show'),       # mu+sak → show (not *see-CAUS)
            ('tungsak', 'lift.up'),  # tung+sak → lift up
        ]
        for word, expected_gloss in lexicalized:
            result = analyze_word(word)
            self.assertIsNotNone(result, f"{word} should be analyzed")
            seg, gloss = result
            self.assertEqual(gloss, expected_gloss,
                f"{word}: expected '{expected_gloss}', got '{gloss}'")
    
    def test_benf_not_caus_for_form_ii(self):
        """Ensure Form II + sak is NEVER glossed as CAUS."""
        form_ii_stems = ['muh', 'cih', 'neih', 'theih', 'tuah', 'bawlh', 'genh']
        for stem in form_ii_stems:
            word = f"{stem}sak"
            result = analyze_word(word)
            if result:
                seg, gloss = result
                # Should have BENF, not CAUS
                self.assertIn('BENF', gloss,
                    f"{word} should have BENF, got '{gloss}'")
                self.assertNotIn('-CAUS', gloss,
                    f"{word} should not have CAUS after Form II, got '{gloss}'")


class TestVerbStemPairs(unittest.TestCase):
    """Test the VERB_STEM_PAIRS dictionary structure."""
    
    def test_verb_stem_pairs_format(self):
        """Test that VERB_STEM_PAIRS has correct format."""
        # Format: form_ii: (form_i, gloss)
        for form_ii, value in VERB_STEM_PAIRS.items():
            self.assertIsInstance(value, tuple,
                f"VERB_STEM_PAIRS['{form_ii}'] should be tuple")
            self.assertEqual(len(value), 2,
                f"VERB_STEM_PAIRS['{form_ii}'] should be (form_i, gloss)")
            form_i, gloss = value
            self.assertIsInstance(form_i, str)
            self.assertIsInstance(gloss, str)
    
    def test_common_verb_pairs(self):
        """Test common verb Form I/II pairs are present."""
        expected_pairs = {
            'muh': ('mu', 'see'),
            'cih': ('ci', 'say'),
            'neih': ('nei', 'have'),
            'theih': ('thei', 'know'),
            'tuah': ('tua', 'do'),
            'bawlh': ('bawl', 'make'),
            'genh': ('gen', 'speak'),
        }
        for form_ii, (form_i, gloss) in expected_pairs.items():
            self.assertIn(form_ii, VERB_STEM_PAIRS,
                f"'{form_ii}' should be in VERB_STEM_PAIRS")
            actual_form_i, actual_gloss = VERB_STEM_PAIRS[form_ii]
            self.assertEqual(actual_form_i, form_i,
                f"VERB_STEM_PAIRS['{form_ii}'] Form I should be '{form_i}'")
            self.assertEqual(actual_gloss, gloss,
                f"VERB_STEM_PAIRS['{form_ii}'] gloss should be '{gloss}'")


if __name__ == '__main__':
    unittest.main(verbosity=2)
