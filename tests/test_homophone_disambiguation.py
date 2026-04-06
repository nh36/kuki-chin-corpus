#!/usr/bin/env python3
"""
Test homophone disambiguation for ngen, kei, khui, and hu.

These tests verify that context-based disambiguation works correctly:
- ngen: 'pray' (default) vs 'net' (fishing context)
- kei: 'NEG' (default) vs '1SG.PRO' (with sangin/tawh)
- khui: 'sew' (fixed from incorrect 'fold')
- hu: 'help' (default) vs 'breath' (with nuntakna or in idiom 'hu tawpna')
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
    # ADDITIONAL NGEN TESTS
    # ====================
    
    # Test 14: ngente (plural nets) with nusia (abandon)
    result = analyze_sentence("a ngente uh nusia-in")
    ngente_gloss = next((g for w, s, g, _ in result if 'ngente' in w.lower()), None)
    if ngente_gloss == 'net-PL':
        print("✓ test_ngente_with_nusia")
        passed += 1
    else:
        print(f"✗ test_ngente_with_nusia: expected 'net-PL', got '{ngente_gloss}'")
        failed += 1
    
    # Test 15: ngen with gunkuang (boat) = net
    result = analyze_sentence("gunkuang tung ah ngen uh")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_ngen_with_gunkuang")
        passed += 1
    else:
        print(f"✗ test_ngen_with_gunkuang: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 16: ngen with ngabeng (fisherman) = net
    result = analyze_sentence("ngabengte in ngen tawh")
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_ngen_with_ngabeng")
        passed += 1
    else:
        print(f"✗ test_ngen_with_ngabeng: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 17: Mark 1:16 full verse - ngen should be net
    verse_16 = "Galilee Tuili gei tawnin Jesuh a pai laitakin Simon le a nau Andru ngabengte ahih manun ngen tawh nga khuhin a om a mu hi"
    result = analyze_sentence(verse_16)
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_mark_1_16_ngen_is_net")
        passed += 1
    else:
        print(f"✗ test_mark_1_16_ngen_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 18: Mark 1:18 - abandoning nets
    verse_18 = "Amau tegel in zong a ngen uh nusia-in Jesuh a zuipah uh hi"
    result = analyze_sentence(verse_18)
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_mark_1_18_ngen_is_net")
        passed += 1
    else:
        print(f"✗ test_mark_1_18_ngen_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # Test 19: Mark 1:19 - mending nets in boat
    verse_19 = "Tawmkhat a pai khit ciangin Zebedi tapa James le a nau Johan zong a gunkuang tung uhah a ngen uh khui-in a om a mu leuleu hi"
    result = analyze_sentence(verse_19)
    ngen_gloss = next((g for w, s, g, _ in result if w == 'ngen'), None)
    if ngen_gloss == 'net':
        print("✓ test_mark_1_19_ngen_is_net")
        passed += 1
    else:
        print(f"✗ test_mark_1_19_ngen_is_net: expected 'net', got '{ngen_gloss}'")
        failed += 1
    
    # ====================
    # HU TESTS (breath vs help)
    # ====================
    
    # Test 20: hu alone defaults to 'help'
    seg, gloss = analyze_word('hu')
    if gloss == 'help':
        print("✓ test_hu_default_help")
        passed += 1
    else:
        print(f"✗ test_hu_default_help: expected 'help', got '{gloss}'")
        failed += 1
    
    # Test 21: "nuntakna hu" = breath of life (Gen 2:7)
    result = analyze_sentence("nuntakna hu sang suk hi")
    hu_gloss = next((g for w, s, g, _ in result if w == 'hu'), None)
    if hu_gloss == 'breath':
        print("✓ test_hu_after_nuntakna_is_breath")
        passed += 1
    else:
        print(f"✗ test_hu_after_nuntakna_is_breath: expected 'breath', got '{hu_gloss}'")
        failed += 1
    
    # Test 22: "hu tawpna" = give up ghost (Gen 25:8)
    result = analyze_sentence("a hu tawpna sang a")
    hu_gloss = next((g for w, s, g, _ in result if w == 'hu'), None)
    if hu_gloss == 'breath':
        print("✓ test_hu_tawpna_is_breath")
        passed += 1
    else:
        print(f"✗ test_hu_tawpna_is_breath: expected 'breath', got '{hu_gloss}'")
        failed += 1
    
    # Test 23: "hu sang" = give up ghost (alternative form)
    result = analyze_sentence("nunung pen a hu sang")
    hu_gloss = next((g for w, s, g, _ in result if w == 'hu'), None)
    if hu_gloss == 'breath':
        print("✓ test_hu_sang_is_breath")
        passed += 1
    else:
        print(f"✗ test_hu_sang_is_breath: expected 'breath', got '{hu_gloss}'")
        failed += 1
    
    # Test 24: "hong hu" = help (verb) - should NOT be breath
    result = analyze_sentence("nang ka hong hu ding")
    hu_gloss = next((g for w, s, g, _ in result if w == 'hu'), None)
    if hu_gloss == 'help':
        print("✓ test_hong_hu_is_help")
        passed += 1
    else:
        print(f"✗ test_hong_hu_is_help: expected 'help', got '{hu_gloss}'")
        failed += 1
    
    # ====================
    # SUMMARY
    # ====================
    print(f"\n{passed} passed, {failed} failed")
    return failed == 0

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
