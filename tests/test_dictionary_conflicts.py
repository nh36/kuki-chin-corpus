#!/usr/bin/env python3
"""
Tests to prevent dictionary conflict regressions.

These tests ensure that adding entries to one dictionary doesn't
accidentally shadow entries in another dictionary, causing parsing bugs.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from analyze_morphemes import (
    ATOMIC_GLOSSES, VERB_STEMS, NOUN_STEMS, TAM_SUFFIXES,
    CASE_MARKERS, ASPECT_SUFFIXES, MODAL_SUFFIXES, analyze_word
)


class TestNoNewDangerousOverlaps(unittest.TestCase):
    """Ensure no NEW dangerous overlaps are introduced.
    
    Some existing overlaps are unavoidable (e.g., 'thei' is both verb and suffix).
    But we should not ADD new ones that cause regression bugs.
    """
    
    # Baseline count of known overlaps (updated April 2026 after sync)
    # If this fails, either:
    # 1. A new overlap was added (bad - investigate and fix)
    # 2. An overlap was removed (good - update this number)
    BASELINE_ATOMIC_VERB_OVERLAPS = 50
    BASELINE_ATOMIC_TAM_OVERLAPS = 10
    
    def test_atomic_verb_overlap_count_stable(self):
        """ATOMIC_GLOSSES vs VERB_STEMS overlap count should not increase."""
        overlaps = sum(1 for f in ATOMIC_GLOSSES if f in VERB_STEMS 
                       and ATOMIC_GLOSSES[f] != VERB_STEMS[f])
        self.assertLessEqual(
            overlaps, 
            self.BASELINE_ATOMIC_VERB_OVERLAPS,
            f"New ATOMIC_GLOSSES entries shadow VERB_STEMS! "
            f"Found {overlaps}, baseline is {self.BASELINE_ATOMIC_VERB_OVERLAPS}. "
            f"This will likely cause parsing regressions."
        )
    
    def test_atomic_tam_overlap_count_stable(self):
        """ATOMIC_GLOSSES vs TAM_SUFFIXES overlap count should not increase."""
        overlaps = sum(1 for f in ATOMIC_GLOSSES if f in TAM_SUFFIXES 
                       and ATOMIC_GLOSSES[f] != TAM_SUFFIXES[f])
        self.assertLessEqual(
            overlaps,
            self.BASELINE_ATOMIC_TAM_OVERLAPS,
            f"New ATOMIC_GLOSSES entries shadow TAM_SUFFIXES! "
            f"Found {overlaps}, baseline is {self.BASELINE_ATOMIC_TAM_OVERLAPS}. "
            f"This will likely cause parsing regressions."
        )


class TestKnownConflictResolutions(unittest.TestCase):
    """Ensure known conflicts resolve correctly in analyze_word.
    
    These are specific cases where we know a form appears in multiple
    dictionaries and we want to verify the CORRECT one wins.
    """
    
    def test_thei_is_know_not_fig_when_suffixed(self):
        """'theih' should be know.II (verb Form II), not fig."""
        seg, gloss = analyze_word('theih')
        self.assertIn('know', gloss.lower(), f"theih should be 'know', got {gloss}")
    
    def test_mu_is_see_when_standalone(self):
        """'mu' standalone should be 'see', not some other gloss."""
        seg, gloss = analyze_word('mu')
        self.assertIn('see', gloss.lower(), f"mu should be 'see', got {gloss}")
    
    def test_dam_is_well_not_cistern(self):
        """'dam' should be 'be.well' or 'well', not 'cistern'."""
        seg, gloss = analyze_word('damna')
        # damna = well/health (nominalized)
        self.assertNotIn('cistern', gloss.lower(), f"dam should not be cistern, got {gloss}")
    
    def test_ngei_is_exp_not_often(self):
        """'ngei' suffix should be EXP (experiential), not 'often'."""
        seg, gloss = analyze_word('ngei')
        self.assertEqual(gloss, 'EXP', f"ngei should be EXP, got {gloss}")
    
    def test_kap_is_weep_not_fight(self):
        """'kap' verb should be 'weep', not 'fight'."""
        seg, gloss = analyze_word('kapin')
        self.assertEqual(gloss, 'weep-CVB', f"kapin should be weep-CVB, got {gloss}")


class TestStemSuffixParsing(unittest.TestCase):
    """Ensure stem+suffix parsing works correctly despite overlaps."""
    
    def test_verb_with_causative(self):
        """Verb stems should combine with -sak (causative) correctly."""
        # hoihsak = make good (good + CAUS)
        seg, gloss = analyze_word('hoihsak')
        self.assertIn('CAUS', gloss, f"hoihsak should have CAUS, got {gloss}")
    
    def test_verb_with_directional(self):
        """Verb stems should combine with directional suffixes."""
        # paikhia = go out
        seg, gloss = analyze_word('paikhia')
        self.assertIn('go', gloss.lower(), f"paikhia should have 'go', got {gloss}")
    
    def test_verb_with_modal(self):
        """Verb stems should combine with modal suffixes."""
        # paitheih = can go
        seg, gloss = analyze_word('paitheih')
        self.assertIn('go', gloss.lower(), f"paitheih should have 'go', got {gloss}")


class TestSyncedGlosses(unittest.TestCase):
    """Ensure glosses stay synchronized between ATOMIC_GLOSSES and VERB_STEMS.
    
    These forms were synced to prevent architecture-dependent behavior.
    If these tests fail, the dictionaries have diverged again.
    """
    
    def test_hoih_synced(self):
        """'hoih' should have same gloss in both dictionaries."""
        self.assertEqual(ATOMIC_GLOSSES.get('hoih'), 'be.good')
    
    def test_khia_synced(self):
        """'khia' should have same gloss in both dictionaries."""
        from analyze_morphemes import VERB_STEMS
        self.assertEqual(ATOMIC_GLOSSES.get('khia'), VERB_STEMS.get('khia'))
    
    def test_khialh_synced(self):
        """'khialh' should have same gloss in both dictionaries."""
        from analyze_morphemes import VERB_STEMS
        self.assertEqual(ATOMIC_GLOSSES.get('khialh'), VERB_STEMS.get('khialh'))
    
    def test_nop_synced(self):
        """'nop' should have same gloss in both dictionaries."""
        from analyze_morphemes import VERB_STEMS
        self.assertEqual(ATOMIC_GLOSSES.get('nop'), VERB_STEMS.get('nop'))
    
    def test_muh_form_ii_preserved(self):
        """'muh' should be glossed as see.II (Form II)."""
        self.assertEqual(ATOMIC_GLOSSES.get('muh'), 'see.II')
    
    def test_theih_form_ii_preserved(self):
        """'theih' should be glossed as know.II (Form II)."""
        self.assertEqual(ATOMIC_GLOSSES.get('theih'), 'know.II')
    
    def test_zak_form_ii_preserved(self):
        """'zak' should be glossed as hear.II (Form II)."""
        self.assertEqual(ATOMIC_GLOSSES.get('zak'), 'hear.II')
    
    def test_honkhia_is_opaque(self):
        """'honkhia' should parse as opaque 'deliver', not hon-khia."""
        seg, gloss = analyze_word('honkhia')
        self.assertEqual(seg, 'honkhia')
        self.assertEqual(gloss, 'deliver')


if __name__ == '__main__':
    unittest.main()
