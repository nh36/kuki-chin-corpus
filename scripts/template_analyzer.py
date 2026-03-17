#!/usr/bin/env python3
"""
Kuki-Chin Morphological Analyzer Template
==========================================

Template for building Leipzig-style morphological analyzers for Kuki-Chin languages.
Copy this file and customize the dictionaries for your target language.

Based on: Tedim Chin (ctd) analyzer achieving 100% coverage

Usage:
    python template_analyzer.py <word>
    
    # Or import as module:
    from template_analyzer import analyze_word
    seg, gloss = analyze_word("word")
"""

import re
import sys

# =============================================================================
# CONFIGURATION - Customize for your language
# =============================================================================

LANGUAGE_ISO = "xxx"  # ISO 639-3 code
LANGUAGE_NAME = "Language Name"

# =============================================================================
# DICTIONARIES - Fill these with your language data
# =============================================================================

# Function words: closed-class items (pronouns, particles, conjunctions)
# These are checked first and returned as-is
FUNCTION_WORDS = {
    # Pronouns
    'ka': '1SG',
    'na': '2SG', 
    'a': '3SG',
    # Demonstratives
    'hih': 'this',
    'tua': 'that',
    # Particles
    'hi': 'DECL',
    'le': 'and',
    'leh': 'if',
    # TAM markers
    'ding': 'IRR',
    # Add more...
}

# Verb stems (both Form I and Form II if applicable)
VERB_STEMS = {
    'mu': 'see',      # Form I
    'muh': 'see',     # Form II
    'nei': 'have',    # Form I
    'neih': 'have',   # Form II
    'gen': 'speak',
    'pai': 'go',
    # Add more verbs...
}

# Noun stems
NOUN_STEMS = {
    'mi': 'person',
    'inn': 'house',
    'khua': 'village',
    'tui': 'water',
    'lung': 'heart',
    # Add more nouns...
}

# Proper nouns (biblical names, place names)
PROPER_NOUNS = {
    'Zeisu': 'JESUS',
    'Mose': 'MOSES',
    'David': 'DAVID',
    # Add more proper nouns...
}

# Compound words - pre-analyzed to prevent over-decomposition
# Format: 'compound': ('segmentation', 'gloss')
COMPOUND_WORDS = {
    'biakinn': ('biak-inn', 'worship-house'),  # temple
    'lungdam': ('lung-dam', 'heart-well'),     # joy
    # Add compounds that shouldn't be decomposed algorithmically
}

# Opaque lexemes - words that look compositional but aren't
OPAQUE_LEXEMES = {
    'lupna': 'bed',       # Not lup-na
    'zatui': 'medicine',  # Not za-tui
    # Add opaque words
}

# Polysemous morphemes with context rules
# Format: 'morpheme': [(meaning, context), ...]
AMBIGUOUS_MORPHEMES = {
    'za': [
        ('hear', 'verbal'),      # With verbal morphology
        ('hundred', 'numeral'),  # In number contexts
    ],
    'na': [
        ('2SG', 'standalone'),   # As pronoun
        ('NMLZ', 'suffix'),      # As suffix
    ],
    # Add more polysemous roots
}

# =============================================================================
# AFFIXES
# =============================================================================

# Prefixes: (prefix, gloss)
PREFIXES = [
    ('kong', '3→1'),
    ('hong', '3→1/2'),
    ('ki', 'REFL'),
    ('ka', '1SG'),
    ('na', '2SG'),
    ('a', '3SG'),
    ('i', '1PL.INCL'),
    ('ei', '1PL.EXCL'),
]

# Derivational suffixes (applied before inflectional)
DERIV_SUFFIXES = [
    ('sak', 'CAUS'),
    ('pih', 'APPL'),
    ('kik', 'REVERT'),
    ('khia', 'DIR.out'),
    ('lut', 'DIR.in'),
    ('theih', 'ABIL'),
    ('gawp', 'INTENS'),
]

# Inflectional suffixes (applied after derivational)
INFL_SUFFIXES = [
    ('te', 'PL'),
    ('in', 'ERG'),
    ('ah', 'LOC'),
    ('ding', 'IRR'),
    ('zo', 'COMPL'),
    ('ta', 'PFV'),
    ('na', 'NMLZ'),
    ('pa', 'NMLZ.AG'),
]

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def normalize_input(word):
    """Normalize unicode variants."""
    # Curly apostrophe to straight
    word = word.replace('\u2019', "'")
    word = word.replace('\u2018', "'")
    return word

def analyze_word(word):
    """
    Analyze a word and return (segmentation, gloss).
    
    Returns:
        tuple: (segmented_form, gloss)
        
    Example:
        >>> analyze_word('biakinn')
        ('biak-inn', 'worship-house')
    """
    original = word
    word = normalize_input(word)
    word_lower = word.lower()
    
    # 1. Check opaque lexemes first
    if word_lower in OPAQUE_LEXEMES:
        return (word_lower, OPAQUE_LEXEMES[word_lower])
    
    # 2. Check proper nouns (case-sensitive)
    if word in PROPER_NOUNS:
        return (word, PROPER_NOUNS[word])
    
    # 3. Check function words
    if word_lower in FUNCTION_WORDS:
        return (word_lower, FUNCTION_WORDS[word_lower])
    
    # 4. Check compound words
    if word_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_lower]
    
    # 5. Check simple stems
    if word_lower in VERB_STEMS:
        return (word_lower, VERB_STEMS[word_lower])
    if word_lower in NOUN_STEMS:
        return (word_lower, NOUN_STEMS[word_lower])
    
    # 6. Try prefix stripping
    for prefix, prefix_gloss in PREFIXES:
        if word_lower.startswith(prefix):
            remainder = word_lower[len(prefix):]
            if remainder in VERB_STEMS:
                return (f"{prefix}-{remainder}", f"{prefix_gloss}-{VERB_STEMS[remainder]}")
            if remainder in NOUN_STEMS:
                return (f"{prefix}-{remainder}", f"{prefix_gloss}-{NOUN_STEMS[remainder]}")
    
    # 7. Try suffix stripping
    for suffix, suffix_gloss in INFL_SUFFIXES + DERIV_SUFFIXES:
        if word_lower.endswith(suffix):
            stem = word_lower[:-len(suffix)]
            if stem in VERB_STEMS:
                return (f"{stem}-{suffix}", f"{VERB_STEMS[stem]}-{suffix_gloss}")
            if stem in NOUN_STEMS:
                return (f"{stem}-{suffix}", f"{NOUN_STEMS[stem]}-{suffix_gloss}")
    
    # 8. Check for reduplication (X~X patterns)
    if len(word_lower) >= 4 and len(word_lower) % 2 == 0:
        half = len(word_lower) // 2
        if word_lower[:half] == word_lower[half:]:
            base = word_lower[:half]
            if base in VERB_STEMS:
                return (f"{base}~RED", f"{VERB_STEMS[base]}~INTNS")
            if base in NOUN_STEMS:
                return (f"{base}~RED", f"{NOUN_STEMS[base]}~INTNS")
    
    # 9. Handle possessive apostrophe
    if word.endswith("'"):
        stem = word[:-1].lower()
        if stem in NOUN_STEMS:
            return (f"{stem}'", f"{NOUN_STEMS[stem]}.POSS")
        if stem in PROPER_NOUNS:
            return (f"{stem}'", f"{PROPER_NOUNS[stem]}.POSS")
    
    # 10. Unknown - return as-is
    return (word, 'UNK')


def analyze_text(text):
    """Analyze all words in a text."""
    words = re.findall(r"[\w'']+", text)
    results = []
    for word in words:
        seg, gloss = analyze_word(word)
        results.append((word, seg, gloss))
    return results


def get_coverage(corpus_file):
    """Calculate coverage on a corpus file."""
    with open(corpus_file) as f:
        text = f.read()
    
    words = re.findall(r"[\w'']+", text)
    total = len(words)
    unknown = sum(1 for w in words if analyze_word(w)[1] == 'UNK')
    
    coverage = (total - unknown) / total * 100
    return {
        'total': total,
        'analyzed': total - unknown,
        'unknown': unknown,
        'coverage': coverage
    }


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    if len(sys.argv) > 1:
        word = sys.argv[1]
        seg, gloss = analyze_word(word)
        print(f"{word}: {seg} = {gloss}")
    else:
        print(f"Kuki-Chin Morphological Analyzer Template")
        print(f"Language: {LANGUAGE_NAME} ({LANGUAGE_ISO})")
        print(f"\nUsage: python {sys.argv[0]} <word>")
        print(f"\nDictionary sizes:")
        print(f"  Function words: {len(FUNCTION_WORDS)}")
        print(f"  Verb stems: {len(VERB_STEMS)}")
        print(f"  Noun stems: {len(NOUN_STEMS)}")
        print(f"  Proper nouns: {len(PROPER_NOUNS)}")
        print(f"  Compounds: {len(COMPOUND_WORDS)}")
