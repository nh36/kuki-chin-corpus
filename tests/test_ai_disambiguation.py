"""
Test ai/Ai disambiguation:
- ai (lowercase) = lot (for casting/divination)
- Ai (capitalized) = proper noun (city name)

Round 201 fixes.
"""
import sys
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

def test_ai_lowercase_is_lot():
    """ai = lot (for divination/casting lots)"""
    seg, gloss = analyze_word('ai')
    assert gloss == 'lot', f"Expected 'lot', got '{gloss}'"

def test_ai_capitalized_is_proper_noun():
    """Ai = proper noun (city name)"""
    seg, gloss = analyze_word('Ai')
    assert gloss == 'AI', f"Expected 'AI' (proper noun), got '{gloss}'"

def test_aite_is_lot_plural():
    """aite = lot-PL (lots, charms)"""
    seg, gloss = analyze_word('aite')
    assert seg == 'ai-te', f"Expected 'ai-te', got '{seg}'"
    assert gloss == 'lot-PL', f"Expected 'lot-PL', got '{gloss}'"

def test_aisanna_is_divination():
    """aisanna = lot-cast-NMLZ (divination)"""
    seg, gloss = analyze_word('aisanna')
    assert seg == 'ai-san-na', f"Expected 'ai-san-na', got '{seg}'"
    assert gloss == 'lot-cast-NMLZ', f"Expected 'lot-cast-NMLZ', got '{gloss}'"

def test_aisan_is_magician():
    """aisan = magician (lexicalized compound)"""
    seg, gloss = analyze_word('aisan')
    assert gloss == 'magician', f"Expected 'magician', got '{gloss}'"

def test_ainn_is_house_possessive():
    """ainn = a-inn = 3SG.POSS-house (his house)
    
    Must not be parsed as ai-nn (lot-?)
    """
    seg, gloss = analyze_word('ainn')
    assert seg == 'a-inn', f"Expected 'a-inn', got '{seg}'"
    assert gloss == '3SG.POSS-house', f"Expected '3SG.POSS-house', got '{gloss}'"

if __name__ == '__main__':
    test_ai_lowercase_is_lot()
    test_ai_capitalized_is_proper_noun()
    test_aite_is_lot_plural()
    test_aisanna_is_divination()
    test_aisan_is_magician()
    test_ainn_is_house_possessive()
    print("All ai disambiguation tests passed!")
