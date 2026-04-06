"""
Round 201: Final coverage fixes for 100% token coverage.

Tests for:
- dante (manner-PL)
- suksiatsakte (plunderers)
- suksiatsakte' (their plunderers)
"""
import sys
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

def test_dante():
    """dante = dan-te = manner-PL (ways/customs)"""
    seg, gloss = analyze_word('dante')
    assert seg == 'dan-te', f"Expected 'dan-te', got '{seg}'"
    assert gloss == 'manner-PL', f"Expected 'manner-PL', got '{gloss}'"

def test_suksiatsakte():
    """suksiatsakte = plunderers (causative verb + PL)"""
    seg, gloss = analyze_word('suksiatsakte')
    assert seg == 'suk-siat-sak-te', f"Expected 'suk-siat-sak-te', got '{seg}'"
    assert gloss == 'make-destroy-CAUS-PL', f"Expected 'make-destroy-CAUS-PL', got '{gloss}'"

def test_suksiatsakte_poss():
    """suksiatsakte' = their plunderers"""
    seg, gloss = analyze_word("suksiatsakte'")
    assert seg == "suk-siat-sak-te'", f"Expected \"suk-siat-sak-te'\", got '{seg}'"
    assert gloss == 'make-destroy-CAUS-PL.POSS', f"Expected 'make-destroy-CAUS-PL.POSS', got '{gloss}'"

if __name__ == '__main__':
    test_dante()
    test_suksiatsakte()
    test_suksiatsakte_poss()
    print("All Round 201 coverage tests passed!")
