#!/usr/bin/env python3
"""
Regression tests for -thei/-theih abilitative allomorphy in Tedim Chin.

Based on ZNC (2017) §5.7.4 (pp. 150-153):
- Form I verb + -thei = abilitative (can do)
- Form II verb + -theih = abilitative (allomorphic variant)

Both receive ABIL gloss (not 'can') for consistency with Leipzig conventions.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analyze_morphemes import analyze_word


def test_thei_standalone():
    """Standalone thei = 'know'"""
    result = analyze_word('thei')
    assert result is not None
    seg, gloss = result
    assert 'know' in gloss.lower(), f"Expected 'know' in gloss, got {gloss}"


def test_theih_standalone():
    """Standalone theih = 'know.II' (Form II)"""
    result = analyze_word('theih')
    assert result is not None
    seg, gloss = result
    assert 'know' in gloss.lower() or 'II' in gloss, f"Expected 'know' or Form II in gloss, got {gloss}"


def test_form_i_plus_thei():
    """Form I verb + thei = ABIL"""
    result = analyze_word('tuthei')  # tu 'sit' (Form I) + thei
    assert result is not None
    seg, gloss = result
    assert 'ABIL' in gloss, f"Expected ABIL in gloss, got {gloss}"


def test_form_ii_plus_theih():
    """Form II verb + theih = ABIL"""
    result = analyze_word('nektheih')  # nek 'eat' (Form II) + theih
    assert result is not None
    seg, gloss = result
    assert 'ABIL' in gloss, f"Expected ABIL in gloss, got {gloss}"


def test_abil_gloss_standardization():
    """All -theih compounds should use ABIL, not 'can'"""
    test_words = [
        'paitheih',     # go-ABIL
        'zattheih',     # hear-ABIL
        'septheih',     # work-ABIL
        'zuihtheih',    # follow-ABIL
        'bawltheih',    # make-ABIL
    ]
    
    for word in test_words:
        result = analyze_word(word)
        assert result is not None, f"{word} returned None"
        seg, gloss = result
        assert 'ABIL' in gloss, f"{word}: Expected ABIL in gloss, got {gloss}"
        assert 'can' not in gloss.lower(), f"{word}: Found 'can' instead of ABIL in {gloss}"


def test_theih_with_nmlz():
    """-theih can combine with -na (NMLZ)"""
    result = analyze_word('kisaktheihna')
    assert result is not None
    seg, gloss = result
    assert 'ABIL' in gloss, f"Expected ABIL in gloss, got {gloss}"
    assert 'NMLZ' in gloss, f"Expected NMLZ in gloss, got {gloss}"


def test_thutheih_compound():
    """thutheih 'knowledge' (lexicalized compound)"""
    result = analyze_word('thutheih')
    assert result is not None
    seg, gloss = result
    # This is a lexicalized compound, may be 'word-know' or 'knowledge'


if __name__ == '__main__':
    tests = [
        test_thei_standalone,
        test_theih_standalone,
        test_form_i_plus_thei,
        test_form_ii_plus_theih,
        test_abil_gloss_standardization,
        test_theih_with_nmlz,
        test_thutheih_compound,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
