#!/usr/bin/env python3
"""
Tedim Chin morphological analyzer for Leipzig-style glossing.

Analyzes Tedim words and produces morpheme-by-morpheme glosses
following Leipzig Glossing Rules conventions.

Usage:
    python analyze_morphemes.py <word>
    python analyze_morphemes.py --verse <verse_id>
    python analyze_morphemes.py --file <input_file>
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Optional

# =============================================================================
# MORPHEME INVENTORY
# =============================================================================

# Pronominal prefixes (subject/possessor)
PRONOMINAL_PREFIXES = {
    'ka': '1SG',
    'na': '2SG', 
    'a': '3SG',
    'i': '1PL.INCL',
}

# Object/direction prefixes
OBJECT_PREFIXES = {
    'kong': '1SG→3',  # I do to him/them
    'hong': '3→1',    # He/they do to me/us
}

# Case markers / postpositions (often cliticized)
CASE_MARKERS = {
    'in': 'ERG',      # Ergative/instrumental
    'ah': 'LOC',      # Locative
    'tawh': 'COM',    # Comitative "with"
    'panin': 'ABL',   # Ablative "from"
}

# TAM suffixes
TAM_SUFFIXES = {
    'ding': 'PROSP',  # Prospective/future
    'ta': 'PFV',      # Perfective
    'zo': 'COMPL',    # Completive
    'kik': 'ITER',    # Iterative
    'nawn': 'CONT',   # Continuative
    'khin': 'IMM',    # Immediate
}

# Sentence-final particles
FINAL_PARTICLES = {
    'hi': 'DECL',     # Declarative
    'hiam': 'Q',      # Interrogative
}

# Negation
NEGATION = {
    'lo': 'NEG',
    'kei': 'NEG.EMPH',
}

# Demonstratives
DEMONSTRATIVES = {
    'hih': 'PROX',    # this
    'tua': 'DIST',    # that
}

# Nominalizers and plurals
NOMINALIZERS = {
    'mi': 'NMLZ.AG',  # Agent nominalizer
    'na': 'NMLZ',     # Nominalizer suffix
    'te': 'PL',       # Plural
    'uh': 'PL',       # Plural (separate word)
}

# Common function words with glosses
FUNCTION_WORDS = {
    # Conjunctions
    'le': 'and',
    'leh': 'and/or',
    'ahihleh': 'if',
    'hangin': 'because',
    'bangin': 'like',
    'manin': 'therefore',
    'zongin': 'although',
    # Particles
    'mah': 'EMPH',
    'pen': 'TOP',
    'zong': 'also',
    'khempeuh': 'all',
    # Adverbs/connectors
    'ciangin': 'then',
    'tua': 'DIST',
    'hih': 'PROX',
    # Copula/auxiliary
    'ci': 'say',
    'ahi': 'be.3SG',
    'ahih': 'be.3SG.REL',
    'hi': 'DECL',
    'om': 'exist',
    # Pronouns (full forms)
    'amah': '3SG.PRO',
    'amaute': '3PL.PRO',
    'keimah': '1SG.PRO',
    'nangmah': '2SG.PRO',
    'amau': '3PL.PRO',
    'note': '2PL.PRO',
    'kote': '1PL.PRO',
    'nang': '2SG.PRO',
    # Pronominal markers (when standalone)
    'ka': '1SG',
    'na': '2SG',
    'a': '3SG',
    'i': '1PL.INCL',
    'kong': '1SG→3',
    'hong': '3→1',
    # Case markers as separate words
    'in': 'ERG',
    'ah': 'LOC',
    'uh': 'PL',
    'un': 'PL.IMP',
    # Negation
    'lo': 'NEG',
    'kei': 'NEG.EMPH',
    # Question
    'hiam': 'Q',
    # TAM
    'ding': 'PROSP',
    'dingin': 'PROSP.LOC',
    'nadingin': '2SG.PROSP.LOC',
    'ta': 'PFV',
    # Relative/nominalizers
    'mi': 'REL/person',
    # Numbers  
    'khat': 'one',
    'nih': 'two',
    'thum': 'three',
    'li': 'four',
    'nga': 'five',
    'guk': 'six',
    'sagih': 'seven',
    'giat': 'eight',
    'kua': 'nine',
    'sawm': 'ten',
}

# Verb stems (common ones)
VERB_STEMS = {
    'om': 'exist',
    'hi': 'be',
    'pai': 'go',
    'hong': 'come',
    'nei': 'have',
    'ci': 'say',
    'gen': 'speak',
    'hilh': 'teach',
    'thei': 'know',
    'mu': 'see',
    'muh': 'see',
    'za': 'hear',
    'zak': 'hear',
    'bawl': 'make/do',
    'pia': 'give',
    'lak': 'take',
    'it': 'love',
    'um': 'believe',
    'sawl': 'send',
    'phum': 'immerse',
    'vak': 'walk',
    'kiko': 'cry.out',
    'kipan': 'begin',
    'kisai': 'concern',
    'kisikin': 'repent',
    'ngai': 'hear/listen',
    'tung': 'arrive',
    'kikhia': 'depart',
    'tat': 'strike',
    'that': 'kill',
    'dam': 'heal',
    'nuam': 'want',
    'tawp': 'end',
    'ding': 'stand',
    'to': 'sit',
    'tut': 'sleep',
    'suak': 'become',
    'suk': 'make.become',
    'khia': 'exit',
    'lut': 'enter',
    'zui': 'follow',
    'khen': 'divide',
    'piak': 'give.to',
    'sam': 'call',
    'sampah': 'call.out',
    'gelh': 'write',
}

# Noun stems (common ones)  
NOUN_STEMS = {
    'Pasian': 'God',
    'Topa': 'Lord',
    'mi': 'person',
    'mite': 'people',
    'pa': 'father',
    'pate': 'fathers',
    'nu': 'mother',
    'tapa': 'son',
    'tapate': 'sons',
    'gam': 'land',
    'khua': 'town',
    'khuapi': 'city',
    'inn': 'house',
    'biakinn': 'temple',
    'thu': 'word',
    'thuthak': 'truth',
    'thuhilhna': 'teaching',
    'hun': 'time',
    'ni': 'day',
    'zan': 'night',
    'lampi': 'way',
    'tui': 'water',
    'mawhna': 'sin',
    'aw': 'voice',
    'mai': 'face',
    'khut': 'hand',
    'min': 'name',
    'kum': 'year',
    'lungsim': 'heart',
    'leitung': 'earth',
    'vantung': 'heaven',
    'zi': 'wife',
    'mipa': 'man',
    'numei': 'woman',
    'mun': 'place',
    'Lungdamna': 'gospel',
    'biakna': 'worship/altar',
    'kamsang': 'prophet',
    'kamtai': 'messenger',
    'siangtho': 'holy',
    'kumpipa': 'king',
    'kumpi': 'king',
    'nasemte': 'servants',
    'nasempa': 'servant',
    'siampi': 'priest',
    'siampite': 'priests',
    'galte': 'enemies',
    'sanggamte': 'brothers',
}

# Proper nouns (don't gloss)
PROPER_NOUNS = {
    'Jesuh', 'Jesus', 'Khrih', 'Christ', 'Johan', 'John',
    'Isaiah', 'Jordan', 'Galilee', 'Jerusalem', 'Judea',
    'Israel', 'David', 'Moses', 'Simon', 'Andru', 'James',
    'Peter', 'Zebedi', 'Nazareth', 'Kapernaum',
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def clean_word(word: str) -> str:
    """Remove punctuation from word."""
    return re.sub(r'[.,;:!?\'"()]+$', '', word)

def is_proper_noun(word: str) -> bool:
    """Check if word is a proper noun."""
    clean = clean_word(word)
    return clean in PROPER_NOUNS or (clean[0].isupper() if clean else False)

def analyze_word(word: str) -> Tuple[str, str]:
    """
    Analyze a Tedim word and return (segmentation, gloss).
    
    Returns:
        Tuple of (segmented_form, gloss)
        e.g., ("a-pai", "3SG-go")
    """
    original = word
    word = clean_word(word)
    
    if not word:
        return ('', '')
    
    # Check if proper noun
    if is_proper_noun(word):
        return (word, word.upper())
    
    # Check function words first (full match)
    word_lower = word.lower()
    if word_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_lower])
    
    # Check common compounds with locatives
    COMPOUND_WORDS = {
        'sungah': ('sung-ah', 'inside-LOC'),
        'tungah': ('tung-ah', 'on-LOC'),
        'kiangah': ('kiang-ah', 'beside-LOC'),
        'tangtungah': ('tangtung-ah', 'upon-LOC'),
        'ci-in': ('ci-in', 'say-QUOT'),
        'kigelhna': ('ki-gelh-na', 'REFL-write-NMLZ'),
        'tuiphum': ('tui-phum', 'water-immerse'),
        'bawlkhol': ('bawl-khol', 'make-prepare'),
        'kipankhia': ('ki-pan-khia', 'REFL-begin-exit'),
        'maisak': ('mai-sak', 'face-CAUS'),
        'sunga': ('sung-a', 'inside-LOC'),
        'panin': ('panin', 'ABL'),
        'kihongin': ('ki-hong-in', 'REFL-open-ERG'),
        'gamlakah': ('gam-lak-ah', 'land-midst-LOC'),
        'paisak': ('pai-sak', 'go-CAUS'),
        'kumsuk': ('kum-suk', 'bow-CAUS'),
        'thawhkhiat': ('thawh-khiat', 'rise-emerge'),
        'mahmah': ('mahmah', 'very'),
        'lungkim': ('lung-kim', 'heart-please'),
        'thakhat': ('tha-khat', 'spirit-one'),
        # More compounds from Bible
        'thuhilhna': ('thu-hilh-na', 'word-teach-NMLZ'),
        'hunhoih': ('hun-hoih', 'time-good'),
        'tungta': ('tung-ta', 'arrive-PFV'),
        'kipanta': ('ki-pan-ta', 'REFL-begin-PFV'),
        'kisikkik': ('ki-sik-kik', 'REFL-repent-ITER'),
        'suaksak': ('suak-sak', 'become-CAUS'),
        'khempeuhte': ('khempeuh-te', 'all-PL'),
    }
    if word_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_lower]
    
    # Check noun stems
    if word in NOUN_STEMS:
        return (word, NOUN_STEMS[word])
    
    # Check verb stems
    if word in VERB_STEMS:
        return (word, VERB_STEMS[word])
    
    # Try morphological decomposition
    segments = []
    glosses = []
    remaining = word
    
    # 1. Check for pronominal prefix
    for prefix, gloss in sorted(OBJECT_PREFIXES.items(), key=lambda x: -len(x[0])):
        if remaining.lower().startswith(prefix):
            segments.append(prefix)
            glosses.append(gloss)
            remaining = remaining[len(prefix):]
            break
    else:
        for prefix, gloss in sorted(PRONOMINAL_PREFIXES.items(), key=lambda x: -len(x[0])):
            if remaining.lower().startswith(prefix) and len(remaining) > len(prefix):
                segments.append(prefix)
                glosses.append(gloss)
                remaining = remaining[len(prefix):]
                break
    
    # 2. Check for verb/noun stem
    stem_found = False
    for stem, gloss in sorted(VERB_STEMS.items(), key=lambda x: -len(x[0])):
        if remaining.lower().startswith(stem):
            segments.append(stem)
            glosses.append(gloss)
            remaining = remaining[len(stem):]
            stem_found = True
            break
    
    if not stem_found:
        for stem, gloss in sorted(NOUN_STEMS.items(), key=lambda x: -len(x[0])):
            if remaining.lower().startswith(stem):
                segments.append(stem)
                glosses.append(gloss)
                remaining = remaining[len(stem):]
                stem_found = True
                break
    
    # 3. Check for suffixes on remaining
    if remaining:
        # Check TAM suffixes
        for suffix, gloss in sorted(TAM_SUFFIXES.items(), key=lambda x: -len(x[0])):
            if remaining.lower() == suffix or remaining.lower().endswith(suffix):
                if remaining.lower() == suffix:
                    segments.append(suffix)
                    glosses.append(gloss)
                    remaining = ''
                    break
        
        # Check case markers
        for case, gloss in sorted(CASE_MARKERS.items(), key=lambda x: -len(x[0])):
            if remaining.lower() == case:
                segments.append(case)
                glosses.append(gloss)
                remaining = ''
                break
        
        # Check final particles
        for particle, gloss in FINAL_PARTICLES.items():
            if remaining.lower() == particle:
                segments.append(particle)
                glosses.append(gloss)
                remaining = ''
                break
        
        # Check nominalizers
        for nom, gloss in NOMINALIZERS.items():
            if remaining.lower().endswith(nom) and len(remaining) > len(nom):
                base = remaining[:-len(nom)]
                segments.append(base)
                glosses.append('?')  # Unknown base
                segments.append(nom)
                glosses.append(gloss)
                remaining = ''
                break
    
    # If we still have remaining, add it as unknown
    if remaining:
        if segments:
            segments.append(remaining)
            glosses.append('?')
        else:
            # No decomposition found - try lexicon lookup
            lexicon_gloss = lookup_lexicon(word.lower())
            if lexicon_gloss:
                return (word, lexicon_gloss)
            segments = [word]
            glosses = ['?']
    
    # Build output
    if len(segments) > 1:
        segmented = '-'.join(segments)
        gloss = '-'.join(glosses)
    else:
        segmented = segments[0] if segments else word
        gloss = glosses[0] if glosses else '?'
    
    return (segmented, gloss)


# Lexicon cache
_lexicon_cache = None

def load_lexicon():
    """Load the Tedim lexicon."""
    global _lexicon_cache
    if _lexicon_cache is not None:
        return _lexicon_cache
    
    lexicon_file = Path(__file__).parent.parent / 'data' / 'lexicons' / 'ctd_lexicon.tsv'
    _lexicon_cache = {}
    
    if lexicon_file.exists():
        with open(lexicon_file) as f:
            next(f)  # skip header
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    kc_word = parts[0].lower()
                    eng_gloss = parts[2]
                    # Only take the first (best) gloss for each word
                    if kc_word not in _lexicon_cache:
                        _lexicon_cache[kc_word] = eng_gloss
    
    return _lexicon_cache

def lookup_lexicon(word: str) -> Optional[str]:
    """Look up a word in the lexicon."""
    lexicon = load_lexicon()
    return lexicon.get(word.lower())


def gloss_sentence(sentence: str) -> List[Tuple[str, str, str]]:
    """
    Gloss a full sentence.
    
    Returns:
        List of (original, segmented, gloss) tuples
    """
    words = sentence.split()
    results = []
    
    for word in words:
        segmented, gloss = analyze_word(word)
        results.append((word, segmented, gloss))
    
    return results


def format_interlinear(results: List[Tuple[str, str, str]], 
                       show_segmentation: bool = True) -> str:
    """Format results as interlinear text."""
    lines = []
    
    # Line 1: Original
    originals = [r[0] for r in results]
    
    # Line 2: Segmented (optional)
    segmented = [r[1] for r in results]
    
    # Line 3: Gloss
    glosses = [r[2] for r in results]
    
    # Calculate widths
    if show_segmentation:
        widths = [max(len(o), len(s), len(g)) + 2 
                  for o, s, g in zip(originals, segmented, glosses)]
    else:
        widths = [max(len(o), len(g)) + 2 for o, g in zip(originals, glosses)]
    
    # Build lines
    line1 = ''.join(o.ljust(w) for o, w in zip(originals, widths))
    if show_segmentation:
        line2 = ''.join(s.ljust(w) for s, w in zip(segmented, widths))
        line3 = ''.join(g.ljust(w) for g, w in zip(glosses, widths))
        return f"{line1}\n{line2}\n{line3}"
    else:
        line2 = ''.join(g.ljust(w) for g, w in zip(glosses, widths))
        return f"{line1}\n{line2}"


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_morphemes.py <word>")
        print("       python analyze_morphemes.py --sentence 'Tedim sentence here'")
        sys.exit(1)
    
    if sys.argv[1] == '--sentence':
        sentence = ' '.join(sys.argv[2:])
        results = gloss_sentence(sentence)
        print(format_interlinear(results, show_segmentation=True))
        
    elif sys.argv[1] == '--verse':
        # Load verse from corpus
        verse_id = sys.argv[2]
        verses_file = Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv'
        
        with open(verses_file) as f:
            header = f.readline().strip().split('\t')
            ctd_col = None
            for i, col in enumerate(header):
                if col.startswith('ctd'):
                    ctd_col = i
                    break
            
            if ctd_col is None:
                print("Error: Tedim column not found")
                sys.exit(1)
            
            for line in f:
                parts = line.strip().split('\t')
                if parts[0] == verse_id:
                    if ctd_col < len(parts) and parts[ctd_col]:
                        print(f"Verse: {verse_id}")
                        print(f"Reference: {parts[1]}")
                        print()
                        results = gloss_sentence(parts[ctd_col])
                        print(format_interlinear(results, show_segmentation=True))
                    else:
                        print(f"No Tedim text for verse {verse_id}")
                    break
            else:
                print(f"Verse {verse_id} not found")
    
    else:
        # Single word
        word = sys.argv[1]
        segmented, gloss = analyze_word(word)
        print(f"Word:      {word}")
        print(f"Segmented: {segmented}")
        print(f"Gloss:     {gloss}")


if __name__ == '__main__':
    main()
