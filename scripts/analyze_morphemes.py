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

# Common function words with glosses - expanded with frequencies
FUNCTION_WORDS = {
    # === Conjunctions & Connectors ===
    'le': 'and',             # 10,942
    'leh': 'and/or',         # 2,921
    'ahihleh': 'if',         # 335
    'hitaleh': 'if.so',      # 295
    'hangin': 'because',     # 3,461
    'bangin': 'like',        # 3,886
    'manin': 'therefore',    # 2,790
    'zongin': 'although',    # 1,970
    'ciangin': 'then',       # 9,297
    'inla': 'and.then',      # ~838
    
    # === Topic/Focus Particles ===
    'mah': 'EMPH',           # 1,540
    'pen': 'TOP',            # 4,541
    'zong': 'also',          # 3,320
    'bek': 'only',           # 782
    
    # === Quantifiers ===
    'khempeuh': 'all',       # 4,783
    'peuhpeuh': 'every',     # 431
    'tampi': 'many',         # 727
    'teltel': 'each',
    
    # === Demonstratives ===
    'tua': 'DIST',           # 9,156 (sentence-initial)
    'hih': 'PROX',           # 4,025
    'tua': 'that',
    'hih': 'this',
    'Tua': 'that',           # capitalized sentence-initial
    
    # === Copula/Auxiliary ===
    'ci': 'say',             # 5,954
    'cih': 'say.NOM',        # 2,827
    'ahi': 'be.3SG',         # 7,409
    'ahih': 'be.3SG.REL',
    'hi': 'DECL',            # 35,961
    'om': 'exist',           # 5,068
    
    # === Independent Pronouns ===
    'amah': '3SG.PRO',       # 4,404
    'amaute': '3PL.PRO',     # 4,590
    'keimah': '1SG.PRO',     # 656
    'nangmah': '2SG.PRO',    # 435
    'amau': '3PL.PRO',
    'note': '2PL.PRO',       # 3,016
    'kote': '1PL.PRO',       # 649
    'nang': '2SG.PRO',
    'nangma': '2SG.self',    # emphatic 2SG
    'keima': '1SG.self',     # emphatic 1SG
    'eite': '1PL.PRO',       # we (exclusive)
    
    # === Pronominal Markers (standalone) ===
    'ka': '1SG',
    'na': '2SG',
    'a': '3SG',              # 58,363 (also generic article)
    'i': '1PL.INCL',
    'kong': '1SG→3',         # 1,945
    'hong': '3→1',           # 15,358
    'nong': '2→1',           # 720
    
    # === Case Markers (standalone) ===
    'in': 'ERG',             # 22,726
    'ah': 'LOC',
    'uh': 'PL',              # 21,924
    'un': 'PL.IMP',
    'tawh': 'COM',           # 7,572
    'panin': 'ABL',          # 4,296
    'sangin': 'COMP',        # 517
    'dong': 'until',         # 647
    
    # === Negation ===
    'lo': 'NEG',             # 6,018
    'kei': 'NEG.EMPH',       # 6,487
    'loh': 'NEG.NOM',        # 885
    'loin': 'NEG.ERG',       # 873
    'kuamah': 'nobody',      # 595
    'bangmah': 'nothing',    # 495
    
    # === Question ===
    'hiam': 'Q',             # 2,766
    
    # === TAM Markers ===
    'ding': 'PROSP',         # 18,980
    'dingin': 'PROSP.ERG',   # 4,798
    'nadingin': '2SG.PROSP.ERG',  # 1,635
    'nadingun': '2PL.PROSP.IMP',  # 656
    'ta': 'PFV',             # 1,106
    'zo': 'COMPL',
    'kik': 'ITER',
    'nawn': 'CONT',          # 1,022
    'khin': 'IMM',           # 893
    'khit': 'SEQ',           # 996
    
    # === Relational/Nominalizers ===
    'mi': 'person/REL',      # 4,221
    'te': 'PL',
    'na': 'NMLZ',
    
    # === Numbers ===
    'khat': 'one',           # 4,303
    'nih': 'two',            # 598
    'thum': 'three',         # 626
    'li': 'four',
    'nga': 'five',
    'guk': 'six',
    'sagih': 'seven',
    'giat': 'eight',
    'kua': 'nine',
    'sawm': 'ten',           # 679
    'sawmnih': 'twenty',     # 263
    'za': 'hundred',
    'tul': 'thousand',
    
    # === Locative/Relational Nouns ===
    'sung': 'inside',        # 2,208
    'tung': 'on',            # 1,413
    'kiang': 'beside',       # 597
    'lai': 'midst',          # 1,032
    'lak': 'among',          # 552
    'mai': 'front',
    
    # === Adverbs ===
    'mahmah': 'very',
    'tawntung': 'forever',   # 679
    'tu': 'now',
    
    # === Interrogatives/Comparatives ===
    'bang': 'what/like',     # often in compounds
    'kua': 'who',
}

# Verb stems - expanded from corpus frequency analysis
# Note: Some verbs have Stem I (basic) and Stem II (modified) forms
VERB_STEMS = {
    # Existence/State (high frequency)
    'om': 'exist',           # 5,068
    'hi': 'be',              # copula
    'ahi': 'be.3SG',         # 7,409
    'ahih': 'be.3SG.REL',    # relativized copula
    'suak': 'become',        # 605
    'teng': 'dwell',         # 859
    'dam': 'be.well',        # health state
    'hoih': 'be.good',       # 641
    
    # Motion verbs
    'pai': 'go',             # 2,350
    'va': 'go.and',          # 817
    'lut': 'enter',
    'khia': 'exit',
    'tung': 'arrive',
    'zui': 'follow',         # 504
    'ciahpai': 'go.home',
    'liahpai': 'return',
    'zuan': 'cross',
    
    # Perception verbs (with stem alternation)
    'mu': 'see.I',           # 962 (Stem I)
    'muh': 'see.II',         # 501 (Stem II)
    'za': 'hear.I',          # 652 (Stem I)
    'zak': 'hear.II',        # (Stem II)
    'ngai': 'listen.I',
    'ngaih': 'listen.II',
    
    # Cognition verbs (with stem alternation)
    'thei': 'know.I',        # 2,543 (Stem I)
    'theih': 'know.II',      # 1,383 (Stem II / passive)
    'um': 'believe',
    'ngaihsun': 'think',     # 409 "mind-think"
    'lung': 'feel',          # emotional state
    
    # Speech verbs
    'ci': 'say',             # 5,954
    'cih': 'say.NOM',        # 2,827
    'gen': 'speak',          # 2,416
    'hilh': 'teach',
    'thugen': 'preach',      # 353 "word-speak"
    'sam': 'call',
    'sampah': 'proclaim',
    'kiko': 'cry.out',
    'paupai': 'gossip',
    
    # Transfer/Possession
    'pia': 'give',           # 2,202
    'piak': 'give.to',       # 781
    'lak': 'take',           # 552
    'nei': 'have',           # 1,770
    'koih': 'put',           # 592
    'sawl': 'send',          # 541
    
    # Action verbs
    'bawl': 'make',          # 1,532
    'sem': 'serve',          # 603
    'uk': 'rule',            # 664
    'that': 'kill',
    'tat': 'strike',
    'ne': 'eat',             # 552
    'thuak': 'suffer',       # 535
    'phum': 'immerse',
    'vak': 'walk',
    'tawp': 'end',
    'ding': 'stand',
    'to': 'sit',
    'tut': 'sleep',
    'suk': 'make.become',
    'khen': 'divide',
    'gelh': 'write',
    
    # Reflexive/reciprocal (ki- prefix)
    'kipan': 'begin',        # ki-pan "REFL-begin"
    'kisai': 'concern',
    'kisik': 'repent',
    'kikhia': 'depart',
    'kibawl': 'be.done',     # 338
    'kibang': 'be.alike',    # 612
    'kikhel': 'differ',
    'kituah': 'meet',
    'kikhen': 'separate',
    
    # Causative/applicative (-sak, -pih)
    'paisak': 'send',        # pai-sak "go-CAUS"
    'damsak': 'heal',        # dam-sak "well-CAUS"
    'paipih': 'accompany',   # 599 pai-pih "go-APPL"
    'honkhia': 'bring.out',
    
    # Additional common verbs from corpus
    'nuam': 'want',
    'it': 'love',
    'zol': 'redeem',
    'hong': 'come/open',
    'ciapteh': 'receive',
    'nuntak': 'live',        # nun-tak "life-firm"
}

# Noun stems - expanded from corpus frequency analysis
NOUN_STEMS = {
    # Divine/Religious (high frequency in Bible)
    'Pasian': 'God',         # 5,308
    'Topa': 'Lord',          # 7,486
    'biakna': 'worship',     # 1,236 biak-na
    'biakinn': 'temple',     # 741 biak-inn
    'siangtho': 'holy',      # 476
    'thupha': 'blessing',    # 479 thu-pha
    'mawhna': 'sin',         # 688 mawh-na
    'Lungdamna': 'gospel',   # 296 lungdam-na
    'nuntakna': 'life',      # 394 nuntak-na
    'thuciamna': 'promise',  # 374 thuciam-na
    'vangliatna': 'power',   # 282
    
    # Social terms
    'mi': 'person',          # 4,221
    'mite': 'people',        # 6,569
    'minam': 'nation',       # 596
    'kumpipa': 'king',       # 1,563
    'kumpi': 'king',
    'siampi': 'priest',      # 357
    'siampite': 'priests',   # 255
    'nasemte': 'servants',   # 389
    'nasempa': 'servant',
    'galte': 'enemies',
    'kamsang': 'prophet',
    'kamtai': 'messenger',
    
    # Kinship
    'pa': 'father',          # 2,265
    'pate': 'fathers',
    'nu': 'mother',          # 619
    'tapa': 'son',           # 1,906
    'tapate': 'sons',        # 411
    'tanu': 'daughter',
    'sanggam': 'brother',
    'sanggamte': 'brothers',
    'zi': 'wife',            # 339
    'mipa': 'man',
    'numei': 'woman',
    
    # Body parts
    'khut': 'hand',          # 854
    'mai': 'face',
    'lungsim': 'heart',      # 957 lung-sim
    'kha': 'spirit',         # 748
    'sa': 'flesh',           # 573
    'lu': 'head',
    'ke': 'foot',
    'mit': 'eye',
    'bil': 'ear',
    'ka': 'mouth',
    
    # Place/Location
    'gam': 'land',           # 2,586
    'khua': 'town',          # 919
    'khuapi': 'city',        # 1,050
    'inn': 'house',          # 715
    'mun': 'place',          # 820
    'leitung': 'earth',      # 717
    'leitang': 'earth',      # 462 (variant)
    'vantung': 'heaven',     # 419
    'lampi': 'way',
    
    # Time terms
    'hun': 'time',           # 1,208
    'ni': 'day',             # 1,191
    'kum': 'year',           # 868
    'zan': 'night',
    'tawntung': 'forever',   # 679
    
    # Abstract terms
    'thu': 'word',           # 5,516
    'thuthak': 'truth',
    'thuhilhna': 'teaching',
    'tui': 'water',
    'aw': 'voice',
    'min': 'name',
    
    # Other common nouns
    'ngeina': 'knowledge',   # 327 ngei-na
    'siatna': 'destruction', # 350 siat-na
    'khialhna': 'sin',       # 328 khialh-na
    'gamtatna': 'kingdom',   # 300 gamtat-na
}

# Proper nouns (don't gloss with lowercase - return as-is with uppercase marker)
PROPER_NOUNS = {
    'Jesuh', 'Jesus', 'Khrih', 'Christ', 'Johan', 'John',
    'Isaiah', 'Jordan', 'Galilee', 'Jerusalem', 'Judea',
    'Israel', 'David', 'Moses', 'Simon', 'Andru', 'James',
    'Peter', 'Zebedi', 'Nazareth', 'Kapernaum', 'Topa',
    'Pasian', 'Nangma', 'Zeisu', 'Kristu', 'Pilate',
    'Abraham', 'Jakobu', 'Johane', 'Herod', 'Maria',
    'Bethlehem', 'Egypt', 'Nazaret', 'Samaria', 'Roma',
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def clean_word(word: str) -> str:
    """Remove punctuation from word, including quotes and apostrophes at word boundaries."""
    # Handle curly quotes and other Unicode punctuation
    word = re.sub(r'^["\'"\'\[\(\«„"]+', '', word)  # Leading quotes/brackets
    word = re.sub(r'[.,;:!?"\'\"\'\)\]\»"\']+$', '', word)  # Trailing punctuation
    word = re.sub(r"'+$", '', word)  # Trailing apostrophes (possessives in some styles)
    return word

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
    
    # Check common compounds - EXPANDED from corpus frequency analysis
    COMPOUND_WORDS = {
        # === Noun + LOC Compounds (very common pattern) ===
        'sungah': ('sung-ah', 'inside-LOC'),
        'tungah': ('tung-ah', 'on-LOC'),
        'kiangah': ('kiang-ah', 'beside-LOC'),
        'tangtungah': ('tangtung-ah', 'upon-LOC'),
        'maih': ('mai-ah', 'front-LOC'),  # contracted
        'lai-ah': ('lai-ah', 'midst-LOC'),
        'lakah': ('lak-ah', 'among-LOC'),
        'munah': ('mun-ah', 'place-LOC'),
        'innah': ('inn-ah', 'house-LOC'),
        'khuaah': ('khua-ah', 'town-LOC'),
        'gamah': ('gam-ah', 'land-LOC'),
        'vantungah': ('vantung-ah', 'heaven-LOC'),
        'leitungah': ('leitung-ah', 'earth-LOC'),
        
        # === Verb + Quotative Compounds ===
        'ci-in': ('ci-in', 'say-QUOT'),
        'cih': ('ci-h', 'say-NOM'),  # nominalized
        'ciin': ('ci-in', 'say-QUOT'),
        'a ci hi': ('a ci hi', '3SG say DECL'),
        
        # === TAM Compounds ===
        'dingin': ('ding-in', 'PROSP-ERG'),
        'nadingin': ('na-ding-in', '2SG-PROSP-ERG'),
        'nadingun': ('na-ding-un', '2SG-PROSP-IMP'),
        'adingin': ('a-ding-in', '3SG-PROSP-ERG'),
        'kadingin': ('ka-ding-in', '1SG-PROSP-ERG'),
        'nading': ('na-ding', '2SG-PROSP'),
        'ading': ('a-ding', '3SG-PROSP'),
        'kading': ('ka-ding', '1SG-PROSP'),
        'tungta': ('tung-ta', 'arrive-PFV'),
        'kipanta': ('ki-pan-ta', 'REFL-begin-PFV'),
        'om ta': ('om ta', 'exist PFV'),
        
        # === Verb + NMLZ Compounds (very productive) ===
        'thuhilhna': ('thu-hilh-na', 'word-teach-NMLZ'),
        'mawhna': ('mawh-na', 'err-NMLZ'),
        'nuntakna': ('nuntak-na', 'live-NMLZ'),
        'thuciamna': ('thuciam-na', 'promise-NMLZ'),
        'siatna': ('siat-na', 'destroy-NMLZ'),
        'khialhna': ('khialh-na', 'wrong-NMLZ'),
        'ngeina': ('ngei-na', 'know-NMLZ'),
        'gamtatna': ('gamtat-na', 'rule.land-NMLZ'),
        'biakna': ('biak-na', 'worship-NMLZ'),
        'vangliatna': ('vangliat-na', 'strong-NMLZ'),
        'lungdamna': ('lungdam-na', 'rejoice-NMLZ'),
        'damna': ('dam-na', 'well-NMLZ'),
        'kingaihna': ('ki-ngaih-na', 'REFL-desire-NMLZ'),
        'kisikna': ('ki-sik-na', 'REFL-turn-NMLZ'),
        
        # === Noun + Noun Compounds ===
        'tapa': ('ta-pa', 'child-male'),
        'tanu': ('ta-nu', 'child-female'),
        'biakinn': ('biak-inn', 'worship-house'),
        'khuapi': ('khua-pi', 'village-big'),
        'leitung': ('lei-tung', 'land-on'),
        'leitang': ('lei-tang', 'land-?'),
        'vantung': ('van-tung', 'sky-on'),
        'lungsim': ('lung-sim', 'stone-mind'),
        'minam': ('mi-nam', 'person-kind'),
        'kumpipa': ('kumpi-pa', 'king-male'),
        'nasempa': ('nasem-pa', 'work.serve-male'),
        'thupha': ('thu-pha', 'word-good'),
        'thuthak': ('thu-thak', 'word-true'),
        
        # === Reflexive/Middle Compounds ===
        'kibawl': ('ki-bawl', 'REFL-make'),
        'kibang': ('ki-bang', 'REFL-same'),
        'kipan': ('ki-pan', 'REFL-begin'),
        'kisai': ('ki-sai', 'REFL-concern'),
        'kisik': ('ki-sik', 'REFL-turn'),
        'kituah': ('ki-tuah', 'REFL-meet'),
        'kikhen': ('ki-khen', 'REFL-divide'),
        'kigelhna': ('ki-gelh-na', 'REFL-write-NMLZ'),
        'kipankhia': ('ki-pan-khia', 'REFL-begin-exit'),
        'kihongin': ('ki-hong-in', 'REFL-open-ERG'),
        'kikhel': ('ki-khel', 'REFL-differ'),
        
        # === Causative Compounds ===
        'paisak': ('pai-sak', 'go-CAUS'),
        'damsak': ('dam-sak', 'well-CAUS'),
        'suaksak': ('suak-sak', 'become-CAUS'),
        'maisak': ('mai-sak', 'face-CAUS'),
        'kumsuk': ('kum-suk', 'bow-CAUS'),
        
        # === Applicative Compounds ===
        'paipih': ('pai-pih', 'go-APPL'),
        'honpih': ('hon-pih', 'come-APPL'),
        
        # === Aspectual/Directional Compounds ===
        'thawhkhiat': ('thawh-khiat', 'rise-emerge'),
        'honkhia': ('hon-khia', 'come-exit'),
        'paikhia': ('pai-khia', 'go-exit'),
        'lutkhia': ('lut-khia', 'enter-exit'),
        'bawlkhol': ('bawl-khol', 'make-prepare'),
        'tuiphum': ('tui-phum', 'water-immerse'),
        
        # === Temporal Compounds ===
        'hunhoih': ('hun-hoih', 'time-good'),
        'tawntung': ('tawn-tung', 'ever-always'),
        'nipi': ('ni-pi', 'day-great'),
        
        # === Intensifiers/Emphasis ===
        'mahmah': ('mahmah', 'very'),
        'lungkim': ('lung-kim', 'heart-full'),  # "pleased"
        'thakhat': ('tha-khat', 'spirit-one'),
        
        # === Quantifier Compounds ===
        'khempeuhte': ('khempeuh-te', 'all-PL'),
        'peuhpeuh': ('peuh-peuh', 'DISTR-DISTR'),
        
        # === Common Connectors ===
        'ciangin': ('ciang-in', 'then-ERG'),
        'hangin': ('hang-in', 'because-ERG'),
        'bangin': ('bang-in', 'like-ERG'),
        'manin': ('man-in', 'reason-ERG'),
        'zongin': ('zong-in', 'although-ERG'),
        'ahihleh': ('a-hi-h-leh', '3SG-be-NOM-if'),
        'hitaleh': ('hi-ta-leh', 'be-PFV-if'),
        'laitakin': ('lai-tak-in', 'midst-exact-ERG'),
        
        # === Negation Compounds ===
        'loh': ('lo-h', 'NEG-NOM'),
        'loin': ('lo-in', 'NEG-ERG'),
        'kuamah': ('kua-mah', 'who-EMPH'),  # "nobody"
        'bangmah': ('bang-mah', 'what-EMPH'),  # "nothing"
        
        # === Postposition + LOC ===
        'panin': ('panin', 'ABL'),  # "from"
        'sangin': ('sang-in', 'high-ERG'),  # "than"
        'tawh': ('tawh', 'COM'),  # "with"
        
        # === Pronoun Compounds ===
        'keimah': ('kei-mah', '1SG.base-EMPH'),
        'nangmah': ('nang-mah', '2SG.base-EMPH'),
        'amah': ('a-mah', '3SG-EMPH'),
        'amaute': ('a-mau-te', '3-PL.base-PL'),
        
        # === Iterative/Continuative ===
        'kisikkik': ('ki-sik-kik', 'REFL-turn-ITER'),
        'nawnkik': ('nawn-kik', 'still-ITER'),
        
        # === Common -in forms (verb/noun + ERG) ===
        'pai-in': ('pai-in', 'go-ERG'),
        'om-in': ('om-in', 'exist-ERG'),
        'thu-in': ('thu-in', 'word-ERG'),
        'nusia-in': ('nusia-in', 'abandon-ERG'),
        'paikhia-in': ('pai-khia-in', 'go-exit-ERG'),
        'zui-in': ('zui-in', 'follow-ERG'),
        
        # === Additional noun compounds ===
        'kikhopna': ('ki-khop-na', 'REFL-gather-NMLZ'),
        'natna': ('nat-na', 'ill-NMLZ'),
        'gamdaihna': ('gam-daih-na', 'land-wide-NMLZ'),
        'paina': ('pai-na', 'go-NMLZ'),
        'khuami': ('khua-mi', 'town-person'),
        'mawhnate': ('mawh-na-te', 'err-NMLZ-PL'),
        
        # === Additional plurals ===
        'gilote': ('gilo-te', 'enemy-PL'),
        'dawite': ('dawi-te', 'demon-PL'),
        
        # === Adverbial compounds ===
        'nakpitakin': ('nak-pi-tak-in', 'strong-big-exact-ERG'),
        
        # === Additional common forms ===
        'an': ('an', '3PL.POSS'),  # 3rd plural possessive
        'pan': ('pan', 'begin/side'),
        'leitang': ('lei-tang', 'land-?'),
        'thute': ('thu-te', 'word-PL'),
        'tu-in': ('tu-in', 'now-ERG'),
        'tuate': ('tua-te', 'DIST-PL'),
        'ciang': ('ciang', 'then'),
        'neih': ('nei-h', 'have-NOM'),
        'ni-in': ('ni-in', 'day-ERG'),
        'nai': ('nai', 'near'),
        'omna': ('om-na', 'exist-NMLZ'),
        'gamtat': ('gam-tat', 'land-rule'),
        'gimna': ('gim-na', 'suffer-NMLZ'),
        'kham': ('kham', 'forbid'),
        'thuman': ('thu-man', 'word-reason'),
        
        # === Miscellaneous High-Frequency ===
        'gamlakah': ('gam-lak-ah', 'land-midst-LOC'),
        'inla': ('in-la', 'ERG-and'),
        'sunga': ('sung-a', 'inside-3SG'),
        'tunga': ('tung-a', 'on-3SG'),
        'ama': ('a-ma', '3SG-self'),
        'nau': ('nau', 'child'),
        'aana': ('a-ana', '3SG-child.PL'),
        'pah': ('pah', 'do.so'),
        'hileh': ('hi-leh', 'be-if'),
        'unla': ('un-la', 'PL.IMP-and'),
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
