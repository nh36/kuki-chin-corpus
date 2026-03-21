#!/usr/bin/env python3
"""
Regression tests for habitual/experiential markers in Tedim Chin.

Based on ZNC (2017) §6.6.2.3 which describes a 4-way habitual system:
- ngei (EXP): Experiential "have done X before"
- gige (HAB): Habitual "always/regularly do X"
- zel (HAB.CONT): Continuative habitual "keep doing X"
- (plus past tense variant: V-ngei hi = used to V)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from analyze_morphemes import analyze_word


def test_ngei_experiential():
    """ngei marks experiential 'have done before'"""
    result = analyze_word('ngei')
    assert result is not None
    seg, gloss = result
    assert 'EXP' in gloss, f"Expected EXP in gloss, got {gloss}"


def test_ngei_with_verb():
    """Verb + ngei = experiential"""
    result = analyze_word('paingei')
    assert result is not None
    seg, gloss = result
    assert 'pai' in seg.lower(), f"Expected 'pai' in segmentation: {seg}"
    assert 'ngei' in seg.lower(), f"Expected 'ngei' in segmentation: {seg}"
    assert 'EXP' in gloss, f"Expected EXP in gloss: {gloss}"


def test_gige_habitual():
    """gige marks habitual 'always/regularly'"""
    result = analyze_word('gige')
    assert result is not None
    seg, gloss = result
    assert 'HAB' in gloss, f"Expected HAB in gloss, got {gloss}"


def test_gige_with_verb():
    """Verb + gige = habitual"""
    result = analyze_word('neigige')
    assert result is not None
    seg, gloss = result
    assert 'gige' in seg.lower(), f"Expected 'gige' in segmentation: {seg}"
    assert 'HAB' in gloss, f"Expected HAB in gloss: {gloss}"


def test_zel_habitual_continuative():
    """zel marks habitual continuative 'keep doing'"""
    result = analyze_word('paizel')
    assert result is not None
    seg, gloss = result
    assert 'zel' in seg.lower(), f"Expected 'zel' in segmentation: {seg}"
    assert 'HAB' in gloss, f"Expected HAB in gloss: {gloss}"


def test_zel_with_prefix():
    """Prefix + verb + zel = habitual continuative"""
    result = analyze_word('kazel')
    assert result is not None
    seg, gloss = result
    assert 'zel' in seg.lower(), f"Expected 'zel' in segmentation: {seg}"
    assert 'HAB' in gloss, f"Expected HAB in gloss: {gloss}"


def test_muhngei_experiential():
    """muh-ngei = have seen before (Form II + EXP)"""
    result = analyze_word('muhngei')
    assert result is not None
    seg, gloss = result
    assert 'ngei' in seg.lower(), f"Expected 'ngei' in segmentation: {seg}"
    assert 'EXP' in gloss, f"Expected EXP in gloss: {gloss}"


if __name__ == '__main__':
    tests = [
        test_ngei_experiential,
        test_ngei_with_verb,
        test_gige_habitual,
        test_gige_with_verb,
        test_zel_habitual_continuative,
        test_zel_with_prefix,
        test_muhngei_experiential,
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
