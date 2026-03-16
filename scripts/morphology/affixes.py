"""
Tedim Chin Affix System

This module defines the complete affix inventory with:
- Clear PREFIX vs SUFFIX distinction
- Derivational vs inflectional classification
- Suffix ordering constraints

Morphological template:
  PRON.PREFIX + ROOT + DERIV.SUFFIX* + INFL.SUFFIX*

Examples:
  ka-gen-sak-na     = 1SG-speak-CAUS-NMLZ (my causing to speak)
  a-bawl-khia-in    = 3SG-make-out-ERG (he making out)
  ki-zum-pih-te     = REFL-bow-APPL-PL (bowing for each other)
"""

# =============================================================================
# PREFIXES (attach BEFORE root)
# =============================================================================

PREFIXES = {
    # === Pronominal prefixes (subject agreement) ===
    'ka': {
        'gloss': '1SG',
        'category': 'pronominal',
        'description': 'First person singular subject',
    },
    'na': {
        'gloss': '2SG', 
        'category': 'pronominal',
        'description': 'Second person singular subject',
    },
    'a': {
        'gloss': '3SG',
        'category': 'pronominal', 
        'description': 'Third person singular subject',
    },
    'i': {
        'gloss': '1PL.INCL',
        'category': 'pronominal',
        'description': 'First person plural inclusive',
    },
    
    # === Object prefixes (portmanteau subject+object) ===
    'kong': {
        'gloss': '1SG→3',
        'category': 'object',
        'description': 'I do to him/them',
    },
    'hong': {
        'gloss': '3→1',
        'category': 'object',
        'description': 'He/they do to me/us',
    },
    
    # === Reflexive/reciprocal prefix ===
    'ki': {
        'gloss': 'REFL',
        'category': 'reflexive',
        'description': 'Reflexive/reciprocal/middle voice',
    },
}


# =============================================================================
# DERIVATIONAL SUFFIXES (change meaning/category, closer to root)
# =============================================================================

DERIVATIONAL_SUFFIXES = {
    # === Causative/applicative ===
    'sak': {
        'gloss': 'CAUS',
        'category': 'valency',
        'description': 'Causative (make X do)',
        'order': 1,
    },
    'pih': {
        'gloss': 'APPL',
        'category': 'valency',
        'description': 'Applicative (do for/with X)',
        'order': 1,
    },
    
    # === Directional/aspectual ===
    'khia': {
        'gloss': 'out',
        'category': 'directional',
        'description': 'Outward motion/exit',
        'order': 2,
    },
    'lut': {
        'gloss': 'in',
        'category': 'directional',
        'description': 'Inward motion/entry',
        'order': 2,
    },
    'kik': {
        'gloss': 'back',
        'category': 'directional',
        'description': 'Return/repetitive',
        'order': 2,
    },
    'cip': {
        'gloss': 'tight',
        'category': 'manner',
        'description': 'Tightly/firmly',
        'order': 2,
    },
    'gawp': {
        'gloss': 'INTENS',
        'category': 'intensifier',
        'description': 'Intensive/completive',
        'order': 2,
    },
    
    # === Completive/resultative ===
    'zo': {
        'gloss': 'COMPL',
        'category': 'aspect',
        'description': 'Completive (finish V-ing)',
        'order': 3,
    },
    'khin': {
        'gloss': 'PERF',
        'category': 'aspect', 
        'description': 'Perfective/already',
        'order': 3,
    },
    'khinta': {
        'gloss': 'COMPL',
        'category': 'aspect',
        'description': 'Completive (zo + khin + ta)',
        'order': 3,
    },
    
    # === Modal ===
    'thei': {
        'gloss': 'able',
        'category': 'modal',
        'description': 'Abilitative (can/able to)',
        'order': 4,
    },
    'nuam': {
        'gloss': 'want',
        'category': 'modal',
        'description': 'Desiderative (want to)',
        'order': 4,
    },
}


# =============================================================================
# INFLECTIONAL SUFFIXES (don't change category, outer position)
# =============================================================================

INFLECTIONAL_SUFFIXES = {
    # === Nominalizers ===
    'na': {
        'gloss': 'NMLZ',
        'category': 'nominalization',
        'description': 'Nominalizer (V → N: the act of V-ing)',
        'order': 10,
        'note': 'ALWAYS A SUFFIX, never a prefix!',
    },
    'pa': {
        'gloss': 'NMLZ.AG',
        'category': 'nominalization',
        'description': 'Agent nominalizer (one who V-s)',
        'order': 10,
    },
    
    # === Case markers ===
    'in': {
        'gloss': 'ERG',
        'category': 'case',
        'description': 'Ergative/instrumental',
        'order': 20,
    },
    'ah': {
        'gloss': 'LOC',
        'category': 'case',
        'description': 'Locative',
        'order': 20,
    },
    'un': {
        'gloss': 'PL.IMP',
        'category': 'case',
        'description': 'Plural imperative',
        'order': 20,
    },
    
    # === Number ===
    'te': {
        'gloss': 'PL',
        'category': 'number',
        'description': 'Plural',
        'order': 15,
    },
    
    # === TAM markers ===
    'ding': {
        'gloss': 'PROSP',
        'category': 'tam',
        'description': 'Prospective/future',
        'order': 25,
    },
    'lai': {
        'gloss': 'PROG',
        'category': 'tam',
        'description': 'Progressive (V-ing)',
        'order': 25,
    },
    'ta': {
        'gloss': 'PERF',
        'category': 'tam',
        'description': 'Perfective particle',
        'order': 30,
    },
}


# =============================================================================
# SUFFIX ORDERING CONSTRAINTS
# =============================================================================

SUFFIX_ORDER = {
    # Order value: lower = closer to root
    # 1-4: Derivational (closest to root)
    # 10-15: Nominalizers, number
    # 20-25: Case, TAM
    # 30+: Final particles
    
    'valid_sequences': [
        # ROOT + DERIV + INFL
        ('sak', 'na'),        # speak-CAUS-NMLZ
        ('sak', 'na', 'te'),  # speak-CAUS-NMLZ-PL
        ('khia', 'in'),       # go-out-ERG
        ('zo', 'ta'),         # do-COMPL-PERF
        ('na', 'te'),         # NMLZ-PL
        ('na', 'in'),         # NMLZ-ERG (as noun)
        ('te', 'in'),         # PL-ERG
        ('te', 'ah'),         # PL-LOC
    ],
    
    'invalid_sequences': [
        # INFL cannot precede DERIV
        ('na', 'sak'),        # *NMLZ-CAUS (wrong order)
        ('te', 'na'),         # *PL-NMLZ (wrong order)
        ('in', 'na'),         # *ERG-NMLZ (wrong order)
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_prefix(morpheme: str) -> bool:
    """Check if a morpheme is a valid prefix."""
    return morpheme in PREFIXES


def is_suffix(morpheme: str) -> bool:
    """Check if a morpheme is a valid suffix."""
    return morpheme in DERIVATIONAL_SUFFIXES or morpheme in INFLECTIONAL_SUFFIXES


def get_suffix_order(morpheme: str) -> int:
    """Get ordering value for a suffix (lower = closer to root)."""
    if morpheme in DERIVATIONAL_SUFFIXES:
        return DERIVATIONAL_SUFFIXES[morpheme].get('order', 5)
    if morpheme in INFLECTIONAL_SUFFIXES:
        return INFLECTIONAL_SUFFIXES[morpheme].get('order', 20)
    return 100  # Unknown suffix goes last


def validate_suffix_sequence(suffixes: list) -> bool:
    """Check if a sequence of suffixes is in valid order."""
    orders = [get_suffix_order(s) for s in suffixes]
    return orders == sorted(orders)  # Must be monotonically increasing
