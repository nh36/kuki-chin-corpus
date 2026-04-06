"""Tests for proper noun homophone disambiguation.

These words have both common word and proper noun meanings:
- Lowercase = common word (ham=full, no=young, pau=speak, etc.)
- Capitalized = proper noun (Ham son of Noah, No city, Pau king, etc.)
"""

import sys
sys.path.insert(0, 'scripts')

from analyze_morphemes import analyze_word

def test_ham_common_word():
    """ham (lowercase) = full/also/cover"""
    seg, gloss = analyze_word('ham')
    assert gloss == 'full', f"Expected 'full', got '{gloss}'"

def test_ham_proper_noun():
    """Ham (capitalized) = son of Noah"""
    seg, gloss = analyze_word('Ham')
    assert gloss == 'HAM', f"Expected 'HAM', got '{gloss}'"

def test_no_common_word():
    """no (lowercase) = young"""
    seg, gloss = analyze_word('no')
    assert gloss == 'young', f"Expected 'young', got '{gloss}'"

def test_no_proper_noun():
    """No (capitalized) = Egyptian city"""
    seg, gloss = analyze_word('No')
    assert gloss == 'NO', f"Expected 'NO', got '{gloss}'"

def test_pau_common_word():
    """pau (lowercase) = speak"""
    seg, gloss = analyze_word('pau')
    assert gloss == 'speak', f"Expected 'speak', got '{gloss}'"

def test_pau_proper_noun():
    """Pau (capitalized) = Edomite king"""
    seg, gloss = analyze_word('Pau')
    assert gloss == 'PAU', f"Expected 'PAU', got '{gloss}'"

def test_sem_common_word():
    """sem (lowercase) = serve"""
    seg, gloss = analyze_word('sem')
    assert gloss == 'serve', f"Expected 'serve', got '{gloss}'"

def test_sem_proper_noun():
    """Sem (capitalized) = Greek form of Shem"""
    seg, gloss = analyze_word('Sem')
    assert gloss == 'SEM', f"Expected 'SEM', got '{gloss}'"

def test_suah_common_word():
    """suah (lowercase) = birth"""
    seg, gloss = analyze_word('suah')
    assert gloss == 'birth', f"Expected 'birth', got '{gloss}'"

def test_suah_proper_noun():
    """Suah (capitalized) = Asherite name"""
    seg, gloss = analyze_word('Suah')
    assert gloss == 'SUAH', f"Expected 'SUAH', got '{gloss}'"

def test_phut_common_word():
    """phut (lowercase) = spray/erect"""
    seg, gloss = analyze_word('phut')
    assert gloss == 'spray', f"Expected 'spray', got '{gloss}'"

def test_phut_proper_noun():
    """Phut (capitalized) = son of Ham (alternate spelling)"""
    seg, gloss = analyze_word('Phut')
    assert gloss == 'PHUT', f"Expected 'PHUT', got '{gloss}'"

def test_puah_common_word():
    """puah (lowercase) = divine/bet"""
    seg, gloss = analyze_word('puah')
    assert gloss == 'divine', f"Expected 'divine', got '{gloss}'"

def test_puah_proper_noun():
    """Puah (capitalized) = Hebrew midwife / judge's father"""
    seg, gloss = analyze_word('Puah')
    assert gloss == 'PUAH', f"Expected 'PUAH', got '{gloss}'"

def test_en_common_word():
    """en (lowercase) = look"""
    seg, gloss = analyze_word('en')
    assert gloss == 'look', f"Expected 'look', got '{gloss}'"

def test_en_with_suffix():
    """ente = look-PL"""
    seg, gloss = analyze_word('ente')
    assert 'look' in gloss, f"Expected 'look' in gloss, got '{gloss}'"


if __name__ == '__main__':
    import unittest
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
