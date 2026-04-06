#!/usr/bin/env python3
"""
Test homophone disambiguation for ngen, kei, and khui.

These tests verify that context-based disambiguation works correctly:
- ngen: 'pray' (default) vs 'net' (fishing context)
- kei: 'NEG' (default) vs '1SG.PRO' (with sangin/tawh)
- khui: 'sew' (fixed from incorrect 'fold')
"""

import sys
sys.path.insert(0, 'scripts')

from analyze_morphemes import analyze_word, analyze_sentence

def run_tests():
    """Run all disambiguation tests."""
    passed = 0
    failed = 0
    
    # ====================
    # NGEN TESTS
    # ====================
    
    # Test 1: ngen alone defaults to 'pray'
    seg, gloss = analyze_word('ngen')
    if gloss == 'pray':
        print("✓ test_ngen_default_pray")
        passed += 1
    else:
        print(f"✗ test_ngen_default_pray: expected 'pray', got '{gloss}'")
        failed += 1
    
    # Test 2: ngen in fishing context (with nga 'fish')
    result = analyze_sentence("an nga a ngen leh")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_ngen_with_nga_is_net")
        passed += 1
    else:
        print(f"✗ test_ngen_with_nga_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 3: ngen with tuili (lake) = net
    result = analyze_sentence("tuili ah ngen a")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_ngen_with_tuili_is_net")
        passed += 1
    else:
        print(f"✗ test_ngen_with_tuili_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 4: ngen with khawl (rest/cease) = net (mending nets)
    result = analyze_sentence("ngen khawl in")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_ngen_with_khawl_is_net")
        passed += 1
    else:
        print(f"✗ test_ngen_with_khawl_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 5: ngen with thu (word) = pray (prayer context)
    result = analyze_sentence("thu ka ngen hi")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'pray':
        print("✓ test_ngen_with_thu_is_pray")
        passed += 1
    else:
        print(f"✗ test_ngen_with_thu_is_pray: expected 'pray', got '{ngen_gloss}'")
        failed += 1
    
    # ====================
    # KEI TESTS
    # ====================
    
    # Test 6: kei alone defaults to NEG
    seg, gloss = analyze_word('kei')
    if gloss == 'NEG':
        print("✓ test_kei_default_neg")
        passed += 1
    else:
        print(f"✗ test_kei_default_neg: expected 'NEG', got '{gloss}'")
        failed += 1
    
    # Test 7: kei + sangin = 1SG.PRO (than me)
    result = analyze_sentence("kei sangin lianzaw")
    kei_gloss = next((g for w, s, g, _ in result if w == 'kei'), None)
    if kei_gloss == '1SG.PRO':
        print("✓ test_kei_sangin_is_pronoun")
        passed += 1
    else:
        print(f"✗ test_kei_sangin_is_pronoun: expected '1SG.PRO', got '{kei_gloss}'")
        failed += 1
    
    # Test 8: kei + tawh = 1SG.PRO (with me)
    result = analyze_sentence("kei tawh om")
    kei_gloss = next((g for w, s, g, _ in result if w == 'kei'), None)
    if kei_gloss == '1SG.PRO':
        print("✓ test_kei_tawh_is_pronoun")
        passed += 1
    else:
        print(f"✗ test_kei_tawh_is_pronoun: expected '1SG.PRO', got '{kei_gloss}'")
        failed += 1
    
    # Test 9: kei + ka = 1SG.PRO (emphatic I)
    result = analyze_sentence("kei ka cih")
    kei_gloss = next((g for w, s, g, _ in result if w == 'kei'), None)
    if kei_gloss == '1SG.PRO':
        print("✓ test_kei_ka_is_pronoun")
        passed += 1
    else:
        print(f"✗ test_kei_ka_is_pronoun: expected '1SG.PRO', got '{kei_gloss}'")
        failed += 1
    
    # Test 10: verb + kei = NEG (negation)
    result = analyze_sentence("a om kei hi")
    kei_gloss = next((g for w, s, g, _ in result if w == 'kei'), None)
    if kei_gloss == 'NEG':
        print("✓ test_verb_kei_is_neg")
        passed += 1
    else:
        print(f"✗ test_verb_kei_is_neg: expected 'NEG', got '{kei_gloss}'")
        failed += 1
    
    # Test 11: ne kei = NEG (eat not)
    result = analyze_sentence("na ne kei ding")
    kei_gloss = next((g for w, s, g, _ in result if w == 'kei'), None)
    if kei_gloss == 'NEG':
        print("✓ test_ne_kei_is_neg")
        passed += 1
    else:
        print(f"✗ test_ne_kei_is_neg: expected 'NEG', got '{kei_gloss}'")
        failed += 1
    
    # ====================
    # KHUI TESTS
    # ====================
    
    # Test 12: khui = sew (not fold)
    seg, gloss = analyze_word('khui')
    if gloss == 'sew':
        print("✓ test_khui_is_sew")
        passed += 1
    else:
        print(f"✗ test_khui_is_sew: expected 'sew', got '{gloss}'")
        failed += 1
    
    # Test 13: khuituah = sew-do
    seg, gloss = analyze_word('khuituah')
    if 'sew' in gloss.lower():
        print("✓ test_khuituah_compound")
        passed += 1
    else:
        print(f"✗ test_khuituah_compound: expected gloss with 'sew', got '{gloss}'")
        failed += 1
    
    # ====================
    # SUMMARY
    # ====================
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
