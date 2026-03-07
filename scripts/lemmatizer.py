#!/usr/bin/env python3
"""
Tedim Chin Lemmatizer

Groups inflected forms under common lemmas, handling:
1. Stem I/II alternation (e.g., mu/muh, za/zak, thei/theih)
2. Pronominal prefix stripping (ka-, na-, a-, kong-, hong-)
3. TAM suffix stripping (ding, ta, zo, kik)
4. Plural suffix stripping (-te, -uh)

Based on Henderson 1965 and VanBik 2009.
"""

from typing import Optional, Tuple

# =============================================================================
# STEM ALTERNATION PATTERNS
# =============================================================================

# Stem I -> Stem II mappings (Stem I is citation form)
# Pattern: Stem I + h = Stem II (for many verbs)
# Pattern: Stem I + k = Stem II (for some verbs)

STEM_PAIRS = {
    # Perception verbs (Stem I / Stem II)
    'mu': 'muh',       # see
    'za': 'zak',       # hear
    'ngai': 'ngaih',   # listen/desire
    
    # Cognition verbs
    'thei': 'theih',   # know
    
    # Possession/State verbs
    'nei': 'neih',     # have
    'zui': 'zuih',     # follow
    
    # Transfer verbs
    'pia': 'piak',     # give
    'la': 'lak',       # take
    'koih': 'koih',    # put (already Stem II?)
    
    # Other verbs
    'hu': 'huh',       # blow
    'si': 'sih',       # die/be
    'lua': 'luah',     # exceed
    'zaw': 'zawh',     # be able
    'tha': 'thah',     # ?
    'pua': 'puah',     # carry
    'khial': 'khialh', # err
    'ne': 'nek',       # eat
    'va': 'vak',       # walk
    'sa': 'sak',       # build/CAUS
}

# Reverse mapping: Stem II -> Stem I (lemma)
STEM2_TO_LEMMA = {v: k for k, v in STEM_PAIRS.items()}

# =============================================================================
# PRONOMINAL PREFIXES
# =============================================================================

PRONOMINAL_PREFIXES = [
    'kong',  # 1SG→3 (longest first)
    'hong',  # 3→1
    'nong',  # 2→1
    'ka',    # 1SG
    'na',    # 2SG
    'a',     # 3SG
    'i',     # 1PL.INCL
]

# =============================================================================
# SUFFIXES
# =============================================================================

# TAM suffixes (in order of application, longest first)
TAM_SUFFIXES = [
    'dingin',  # PROSP-ERG
    'ding',    # PROSP
    'khin',    # IMM
    'khit',    # SEQ
    'nawn',    # CONT
    'kik',     # ITER
    'ta',      # PFV
    'zo',      # COMPL
]

# Nominal suffixes
NOMINAL_SUFFIXES = [
    'te',   # PL
    'na',   # NMLZ
]

# Case suffixes
CASE_SUFFIXES = [
    'in',   # ERG
    'ah',   # LOC
]

# =============================================================================
# LEMMATIZATION FUNCTIONS
# =============================================================================

def strip_prefix(word: str) -> Tuple[str, Optional[str]]:
    """
    Strip pronominal prefix from word.
    Returns (remaining, prefix) or (word, None) if no prefix.
    """
    word_lower = word.lower()
    for prefix in PRONOMINAL_PREFIXES:
        if word_lower.startswith(prefix) and len(word_lower) > len(prefix):
            remaining = word_lower[len(prefix):]
            # Don't strip if remaining is too short
            if len(remaining) >= 2:
                return (remaining, prefix)
    return (word_lower, None)


def strip_suffix(word: str, suffix_list: list) -> Tuple[str, Optional[str]]:
    """
    Strip suffix from word.
    Returns (remaining, suffix) or (word, None) if no suffix.
    """
    for suffix in suffix_list:
        if word.endswith(suffix) and len(word) > len(suffix):
            remaining = word[:-len(suffix)]
            if len(remaining) >= 2:
                return (remaining, suffix)
    return (word, None)


def normalize_stem(stem: str) -> str:
    """
    Normalize Stem II to Stem I (citation form).
    """
    if stem in STEM2_TO_LEMMA:
        return STEM2_TO_LEMMA[stem]
    return stem


def lemmatize(word: str) -> Tuple[str, list]:
    """
    Lemmatize a Tedim word.
    
    Returns:
        (lemma, morphemes) where morphemes is a list of (morpheme, gloss) tuples
    """
    original = word
    word = word.lower()
    morphemes = []
    
    # 1. Strip pronominal prefix
    stem, prefix = strip_prefix(word)
    if prefix:
        morphemes.append((prefix, get_prefix_gloss(prefix)))
    
    # 2. Strip TAM suffix
    stem, tam = strip_suffix(stem, TAM_SUFFIXES)
    
    # 3. Strip case suffix (if TAM wasn't found)
    case = None
    if not tam:
        stem, case = strip_suffix(stem, CASE_SUFFIXES)
    
    # 4. Strip nominal suffix
    stem, nom = strip_suffix(stem, NOMINAL_SUFFIXES)
    
    # 5. Normalize stem (Stem II -> Stem I)
    lemma = normalize_stem(stem)
    
    # Build morpheme list
    morphemes.append((lemma, 'STEM'))
    if nom:
        morphemes.append((nom, get_suffix_gloss(nom)))
    if tam:
        morphemes.append((tam, get_suffix_gloss(tam)))
    if case:
        morphemes.append((case, get_suffix_gloss(case)))
    
    return (lemma, morphemes)


def get_prefix_gloss(prefix: str) -> str:
    """Get gloss for prefix."""
    glosses = {
        'ka': '1SG',
        'na': '2SG',
        'a': '3SG',
        'i': '1PL.INCL',
        'kong': '1SG→3',
        'hong': '3→1',
        'nong': '2→1',
    }
    return glosses.get(prefix, '?')


def get_suffix_gloss(suffix: str) -> str:
    """Get gloss for suffix."""
    glosses = {
        # TAM
        'ding': 'PROSP',
        'dingin': 'PROSP.ERG',
        'ta': 'PFV',
        'zo': 'COMPL',
        'kik': 'ITER',
        'nawn': 'CONT',
        'khin': 'IMM',
        'khit': 'SEQ',
        # Nominal
        'te': 'PL',
        'na': 'NMLZ',
        # Case
        'in': 'ERG',
        'ah': 'LOC',
    }
    return glosses.get(suffix, '?')


def format_analysis(lemma: str, morphemes: list) -> str:
    """Format lemma and morphemes for display."""
    morph_str = '-'.join(m for m, g in morphemes)
    gloss_str = '-'.join(g for m, g in morphemes)
    return f"{morph_str}\t{gloss_str}\t[lemma: {lemma}]"


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python lemmatizer.py <word> [word2] ...")
        print("       python lemmatizer.py --test")
        sys.exit(1)
    
    if sys.argv[1] == '--test':
        # Test cases
        test_words = [
            'mu', 'muh', 'kamu', 'kamuh',
            'thei', 'theih', 'katheih', 'natheih',
            'za', 'zak', 'hongza', 'hongzak',
            'piak', 'kongpiak', 'hongpiak',
            'paidingin', 'kapaiding', 
            'mite', 'mitena', 'mitete',
            'biakna', 'mawhna',
        ]
        print("Lemmatization Test:")
        print("-" * 60)
        for word in test_words:
            lemma, morphemes = lemmatize(word)
            print(f"{word:15} -> {format_analysis(lemma, morphemes)}")
    else:
        for word in sys.argv[1:]:
            lemma, morphemes = lemmatize(word)
            print(f"{word}: {format_analysis(lemma, morphemes)}")
