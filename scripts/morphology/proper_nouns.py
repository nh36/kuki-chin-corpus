"""
Tedim Chin Proper Nouns

Biblical names and place names.
These are not analyzed morphologically.
"""

PROPER_NOUNS = {
    # === Divine names ===
    'Pasian': 'GOD',
    'Topa': 'Lord',
    'Jesuh': 'JESUS',
    'Khrih': 'CHRIST',
    
    # === Patriarchs ===
    'Abraham': 'ABRAHAM',
    'Isaac': 'ISAAC',
    'Jacob': 'JACOB',
    'Israel': 'ISRAEL',
    'Moses': 'MOSES',
    'Aaron': 'AARON',
    'David': 'DAVID',
    'Solomon': 'SOLOMON',
    
    # === Places ===
    'Jerusalem': 'JERUSALEM',
    'Bethlehem': 'BETHLEHEM',
    'Egypt': 'EGYPT',
    'Judah': 'JUDAH',
    'Galilee': 'GALILEE',
    'Jordan': 'JORDAN',
    'Sinai': 'SINAI',
    
    # === New Testament ===
    'Peter': 'PETER',
    'Paul': 'PAUL',
    'John': 'JOHN',
    'Mary': 'MARY',
    'Pilate': 'PILATE',
    
    # Many more... (extracted from original analyzer)
}


def is_proper_noun(word: str) -> bool:
    """Check if a word is a proper noun (case-insensitive on first char)."""
    # Proper nouns start with capital letter
    if word and word[0].isupper():
        return word in PROPER_NOUNS or word.capitalize() in PROPER_NOUNS
    return False


def get_proper_noun_gloss(word: str) -> str:
    """Get gloss for proper noun, or None."""
    if word in PROPER_NOUNS:
        return PROPER_NOUNS[word]
    if word.capitalize() in PROPER_NOUNS:
        return PROPER_NOUNS[word.capitalize()]
    return None
