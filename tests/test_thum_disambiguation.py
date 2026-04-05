#!/usr/bin/env python3
"""
Regression tests for thum homophone disambiguation.

thum has three meanings in Tedim Chin:
1. 'three' (numeral) - in numeric contexts: ni thum, kum thum, tapa thum
2. 'entreat' (verb) - with 1SG/2SG markers: kong thum, hong thum
3. 'mourn' (verb) - with weeping context: kapin thum, dahin thum

Tests verify correct disambiguation based on sentence context.
"""

import unittest
import sys
sys.path.insert(0, 'scripts')

from analyze_morphemes import (
    analyze_word,
    analyze_word_with_context,
    analyze_sentence,
    AMBIGUOUS_MORPHEMES
)


class TestThumAmbiguousMorphemes(unittest.TestCase):
    """Test that thum is registered as ambiguous with all three meanings."""
    
    def test_thum_in_ambiguous_morphemes(self):
        """thum should be in AMBIGUOUS_MORPHEMES."""
        self.assertIn('thum', AMBIGUOUS_MORPHEMES)
    
    def test_thum_has_three_meanings(self):
        """thum should have three meanings: three, entreat, mourn."""
        entries = AMBIGUOUS_MORPHEMES['thum']
        glosses = {e[0] for e in entries}
        self.assertIn('three', glosses)
        self.assertIn('entreat', glosses)
        self.assertIn('mourn', glosses)


class TestThumStandalone(unittest.TestCase):
    """Test standalone thum defaults to numeral."""
    
    def test_standalone_thum_is_three(self):
        """Standalone thum should default to 'three'."""
        seg, gloss = analyze_word('thum')
        self.assertEqual(gloss, 'three')


class TestThumNumeral(unittest.TestCase):
    """Test thum as numeral in numeric contexts."""
    
    def test_ni_thum_day_three(self):
        """ni thum = day three."""
        result = analyze_sentence('ni thum ni')
        glosses = [g for w, s, g, b in result]
        self.assertEqual(glosses[1], 'three')
    
    def test_kum_thum_year_three(self):
        """kum thum = year three."""
        seg, gloss = analyze_word_with_context('thum', 'kum', 'a')
        self.assertEqual(gloss, 'three')
    
    def test_tapa_thum_three_sons(self):
        """tapa thum = three sons."""
        seg, gloss = analyze_word_with_context('thum', 'tapa', 'a')
        self.assertEqual(gloss, 'three')
    
    def test_mi_thum_three_people(self):
        """mi thum = three people."""
        seg, gloss = analyze_word_with_context('thum', 'mi', 'na')
        self.assertEqual(gloss, 'three')


class TestThumEntreat(unittest.TestCase):
    """Test thum as 'entreat' with 1SG/2SG object markers."""
    
    def test_kong_thum_i_entreat(self):
        """kong thum = I entreat (1SG→3 object marker)."""
        seg, gloss = analyze_word_with_context('thum', 'kong', 'hi')
        self.assertEqual(gloss, 'entreat')
    
    def test_hong_thum_you_entreat(self):
        """hong thum = [you] entreat [me] (3→1 object marker)."""
        seg, gloss = analyze_word_with_context('thum', 'hong', 'ing')
        self.assertEqual(gloss, 'entreat')
    
    def test_sentence_kong_thum_hi(self):
        """Full sentence: kong thum hi = I entreat DECL."""
        result = analyze_sentence('kong thum hi')
        glosses = [g for w, s, g, b in result]
        self.assertEqual(glosses[1], 'entreat')
    
    def test_sentence_topa_tungah_kong_thum(self):
        """Topa tungah kong thum hi = I entreat unto LORD."""
        result = analyze_sentence('Topa tungah kong thum hi')
        glosses = [g for w, s, g, b in result]
        self.assertIn('entreat', glosses)


class TestThumMourn(unittest.TestCase):
    """Test thum as 'mourn' with weeping context."""
    
    def test_kapin_thum_weep_mourn(self):
        """kapin thum = weep-ERG mourn."""
        seg, gloss = analyze_word_with_context('thum', 'kapin', 'hi')
        self.assertEqual(gloss, 'mourn')
    
    def test_kapin_a_thum_looking_back_2(self):
        """kapin a thum = weep-ERG 3SG mourn (kapin 2 words back)."""
        seg, gloss = analyze_word_with_context('thum', 'a', 'uh', 'kapin')
        self.assertEqual(gloss, 'mourn')
    
    def test_sentence_kapin_a_thum_uh(self):
        """Full sentence: kapin a thum uh hi."""
        result = analyze_sentence('kapin a thum uh hi')
        glosses = [g for w, s, g, b in result]
        self.assertEqual(glosses[2], 'mourn')
    
    def test_dahin_thum_wail_mourn(self):
        """dahin thum = wail-ERG mourn."""
        seg, gloss = analyze_word_with_context('thum', 'dahin', 'hi')
        self.assertEqual(gloss, 'mourn')


class TestThumCompounds(unittest.TestCase):
    """Test thum in compound words."""
    
    def test_thumsak_entreat_caus(self):
        """thumsak = entreat-CAUS (intercede)."""
        seg, gloss = analyze_word('thumsak')
        self.assertIn('entreat', gloss.lower())
        self.assertIn('caus', gloss.lower())
    
    def test_thumthum_mourn_redup(self):
        """thumthum = mourn~REDUP (mourn sore)."""
        seg, gloss = analyze_word('thumthum')
        self.assertIn('mourn', gloss.lower())
    
    def test_thumvei_three_times(self):
        """thumvei = three times."""
        seg, gloss = analyze_word('thumvei')
        self.assertIn('three', gloss.lower())
    
    def test_sawmthum_thirteen(self):
        """sawmthum = ten-three (thirteen)."""
        seg, gloss = analyze_word('sawmthum')
        self.assertIn('ten', gloss.lower())
        self.assertIn('three', gloss.lower())


class TestThumBibleVerses(unittest.TestCase):
    """Test thum disambiguation on actual Bible verses."""
    
    def test_gen_19_2_entreat(self):
        """GEN 19:2 - kong thum hi = I entreat."""
        # "Ka tote aw, kong thum hi."
        result = analyze_sentence('kong thum hi')
        glosses = [g for w, s, g, b in result]
        self.assertEqual(glosses[1], 'entreat')
    
    def test_gen_1_13_numeral(self):
        """GEN 1:13 - ni thum ni = day three day."""
        # "ni thum ni ahi hi"
        result = analyze_sentence('ni thum ni ahi hi')
        glosses = [g for w, s, g, b in result]
        self.assertEqual(glosses[1], 'three')
    
    def test_2sam_19_1_mourn(self):
        """2SAM 19:1 - kapin thum = weeping mourn."""
        # "kumpipa kapin thum hi"
        result = analyze_sentence('kumpipa kapin thum hi')
        glosses = [g for w, s, g, b in result]
        self.assertIn('mourn', glosses)


if __name__ == '__main__':
    unittest.main(verbosity=2)
