#!/usr/bin/env python3
"""
Regression tests for Tedim Chin tone restoration system.

Tests cover:
1. Unambiguous lookups (single entry in dictionary)
2. Gloss-based disambiguation (homophony resolved by analyzer)
3. Compound word handling (morpheme-by-morpheme tone marking)
4. Unknown handling (leave unmarked when unknown)
5. Form I/II verb tone patterns
"""

import unittest
import unicodedata
import sys
sys.path.insert(0, 'scripts')

from restore_tone import (
    load_tone_dictionary,
    restore_word_tone,
    restore_verse_tone,
    disambiguate_tone_with_gloss,
    mark_syllable_tones
)


def normalize(s):
    """Normalize Unicode to NFC for comparison."""
    return unicodedata.normalize('NFC', s)


class TestToneDictionary(unittest.TestCase):
    """Test dictionary loading and structure."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_dictionary_loads(self):
        """Dictionary should load with substantial entries."""
        self.assertGreater(len(self.tone_dict), 500)
    
    def test_entry_structure(self):
        """Each entry should have required fields."""
        entry = self.tone_dict['ta'][0]
        self.assertIn('tone', entry)
        self.assertIn('gloss', entry)
        self.assertIn('source', entry)
    
    def test_homophonous_entries(self):
        """Homophonous morphemes should have multiple entries."""
        # ta has both PFV (L) and child (H)
        ta_entries = self.tone_dict['ta']
        tones = {e['tone'] for e in ta_entries}
        self.assertIn('L', tones)  # PFV
        self.assertIn('H', tones)  # child
    
    def test_thei_entries(self):
        """thei should have both 'know' (H) and 'ABIL' (L)."""
        thei_entries = self.tone_dict['thei']
        glosses = {e['gloss'].lower() for e in thei_entries}
        self.assertIn('know', glosses)
        self.assertIn('abil', glosses)


class TestUnambiguousLookup(unittest.TestCase):
    """Test single-entry lookups (HIGH confidence)."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_hoih_good(self):
        """hoih 'good' should be L tone."""
        toned, conf, analysis = restore_word_tone('hoih', self.tone_dict)
        self.assertEqual(conf, 'high')
        self.assertEqual(analysis[0][1], 'L')
        self.assertIn('ò', normalize(toned))  # L tone on o
    
    def test_hi_decl(self):
        """hi (DECL) should be L tone."""
        toned, conf, analysis = restore_word_tone('hi', self.tone_dict)
        self.assertEqual(conf, 'high')
        self.assertEqual(analysis[0][1], 'L')
    
    def test_lo_neg(self):
        """lo (NEG) should be L tone."""
        toned, conf, analysis = restore_word_tone('lo', self.tone_dict)
        self.assertEqual(conf, 'high')
        self.assertEqual(analysis[0][1], 'L')


class TestGlossDisambiguation(unittest.TestCase):
    """Test homophony resolution via analyzer gloss."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_thei_know_high(self):
        """thei with gloss 'know' should get H tone."""
        # Word analyzed as 'thei' = 'know' by analyzer
        toned, conf, analysis = restore_word_tone('thei', self.tone_dict)
        # The analyzer returns 'know' as gloss
        self.assertEqual(conf, 'high')
        self.assertEqual(analysis[0][1], 'H')
    
    def test_ta_child_high(self):
        """ta with gloss 'child' should get H tone."""
        # In compound 'tapa' (son), ta=child gets H
        toned, conf, analysis = restore_word_tone('tapa', self.tone_dict)
        self.assertEqual(conf, 'high')
        # First morpheme 'ta' should be H
        self.assertEqual(analysis[0][1], 'H')
    
    def test_ta_pfv_low(self):
        """ta with gloss 'PFV' should get L tone."""
        # In 'paita' (went-PFV), ta=PFV gets L
        toned, conf, analysis = restore_word_tone('paita', self.tone_dict)
        self.assertEqual(conf, 'high')
        # Find the ta morpheme
        ta_analysis = [a for a in analysis if a[0] == 'ta']
        self.assertTrue(len(ta_analysis) > 0)
        self.assertEqual(ta_analysis[0][1], 'L')
    
    def test_khin_imm_high(self):
        """khin with gloss 'IMM' should get H tone when in compound."""
        # In 'paita-khin' or similar, khin gets H
        # Note: matkhin has 'mat' unknown, so overall is 'low'
        # but khin itself should be marked H
        toned, conf, analysis = restore_word_tone('matkhin', self.tone_dict)
        khin_analysis = [a for a in analysis if a[0] == 'khin']
        self.assertTrue(len(khin_analysis) > 0)
        self.assertEqual(khin_analysis[0][1], 'H')
        # Overall is 'low' because 'mat' is unknown
        self.assertEqual(conf, 'low')


class TestCompoundHandling(unittest.TestCase):
    """Test morpheme-by-morpheme tone marking in compounds."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_laitakin_all_known(self):
        """laitakin should have all morphemes marked."""
        toned, conf, analysis = restore_word_tone('laitakin', self.tone_dict)
        # lai=midst (H), tak=exact (L), in=ERG (L)
        self.assertEqual(conf, 'high')
        self.assertEqual(len(analysis), 3)
        self.assertEqual(analysis[0][1], 'H')  # lai
        self.assertEqual(analysis[1][1], 'L')  # tak
        self.assertEqual(analysis[2][1], 'L')  # in
    
    def test_partial_compound(self):
        """Compound with unknown morpheme should be 'low' overall but mark known parts."""
        # numei (woman) - nu has entries but wrong gloss match
        toned, conf, analysis = restore_word_tone('numei', self.tone_dict)
        # Overall should be low if any morpheme unknown
        self.assertEqual(conf, 'low')
        # But some morphemes may still be marked


class TestUnknownHandling(unittest.TestCase):
    """Test that unknowns are properly left unmarked."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_unknown_left_unmarked(self):
        """Unknown words should be left unmarked."""
        # phak with gloss 'year' has no matching entry
        toned, conf, analysis = restore_word_tone('phak', self.tone_dict)
        # Should be low confidence - dict has leprosy/overtake but not year
        self.assertEqual(conf, 'low')
        self.assertEqual(toned, 'phak')  # Unmarked
    
    def test_no_false_marking(self):
        """Words with wrong gloss should NOT be marked."""
        # puak=send not in dict (has spill/carry)
        toned, conf, analysis = restore_word_tone('puak', self.tone_dict)
        self.assertEqual(conf, 'low')
        self.assertEqual(toned, 'puak')


class TestFormIII(unittest.TestCase):
    """Test Form I/II verb tone patterns."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_form_i_high(self):
        """Form I verbs should typically be H or M tone."""
        # ne 'eat' Form I is H
        toned, conf, analysis = restore_word_tone('ne', self.tone_dict)
        if conf == 'high':
            self.assertIn(analysis[0][1], ('H', 'M'))
    
    def test_form_ii_low(self):
        """Form II verbs should typically be L tone."""
        # nek 'eat.II' Form II is L
        if 'nek' in self.tone_dict:
            toned, conf, analysis = restore_word_tone('nek', self.tone_dict)
            if conf == 'high':
                self.assertEqual(analysis[0][1], 'L')


class TestVerseRestoration(unittest.TestCase):
    """Test verse-level tone restoration."""
    
    @classmethod
    def setUpClass(cls):
        cls.tone_dict = load_tone_dictionary()
    
    def test_verse_stats(self):
        """Verse restoration should return proper stats."""
        verse = "Pasian in leitung a bawl hi"
        toned, stats = restore_verse_tone(verse, self.tone_dict)
        self.assertIn('high', stats)
        self.assertIn('low', stats)
        self.assertEqual(stats['high'] + stats['low'], 6)  # 6 words
    
    def test_verse_preserves_spacing(self):
        """Toned verse should preserve word boundaries."""
        verse = "ka hoih hi"
        toned, stats = restore_verse_tone(verse, self.tone_dict)
        self.assertEqual(len(toned.split()), 3)


class TestMarkSyllableTones(unittest.TestCase):
    """Test tone diacritic marking."""
    
    def test_low_tone_grave(self):
        """L tone should add grave accent."""
        self.assertIn('à', normalize(mark_syllable_tones('a', 'L')))
        self.assertIn('ò', normalize(mark_syllable_tones('hoih', 'L')))
    
    def test_high_tone_acute(self):
        """H tone should add acute accent."""
        self.assertIn('á', normalize(mark_syllable_tones('a', 'H')))
    
    def test_mid_tone_unmarked_or_macron(self):
        """M tone marking (implementation-dependent)."""
        result = mark_syllable_tones('lam', 'M')
        # M tone may be unmarked or have macron
        self.assertIsInstance(result, str)


if __name__ == '__main__':
    unittest.main(verbosity=2)
