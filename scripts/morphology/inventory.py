"""
Tedim Chin Morpheme Inventory

Single source of truth for all morphemes with:
- Clear category (verb_root, noun_root, suffix, prefix)
- Gloss
- Polysemy documented explicitly
- Notes on usage/restrictions

This replaces the overlapping VERB_STEMS, NOUN_STEMS, TAM_SUFFIXES, etc.
"""

# =============================================================================
# MORPHEME INVENTORY
# =============================================================================

MORPHEME_INVENTORY = {
    # === VERB ROOTS ===
    'bawl': {
        'category': 'verb_root',
        'gloss': 'make',
        'frequency': 500,
    },
    'gen': {
        'category': 'verb_root',
        'gloss': 'speak',
        'frequency': 400,
    },
    'sep': {
        'category': 'verb_root',
        'gloss': 'work',  # Aligned with VERB_STEMS
        'frequency': 300,
    },
    'pai': {
        'category': 'verb_root',
        'gloss': 'go',
        'frequency': 600,
    },
    'tum': {
        'category': 'verb_root',
        'gloss': 'strike',
        'frequency': 200,
    },
    'zang': {
        'category': 'verb_root',
        'gloss': 'use',
        'frequency': 150,
    },
    'tung': {
        'category': 'verb_root',
        'gloss': 'arrive',
        'frequency': 180,
    },
    'muh': {
        'category': 'verb_root',
        'gloss': 'see.II',  # Henderson Form II
        'frequency': 300,
    },
    'mu': {
        'category': 'verb_root',
        'gloss': 'see.I',  # Henderson Form I
        'form': 'I',
        'frequency': 250,
    },
    'thei': {
        'category': 'verb_root',
        'gloss': 'know.I',  # Henderson Form I
        'polysemy': ['know (verb)', 'able (suffix)'],
        'frequency': 200,
    },
    'theih': {
        'category': 'verb_root',
        'gloss': 'know.II',
        'form': 'II',  # Form II of thei
        'frequency': 150,
    },
    'lut': {
        'category': 'verb_root',
        'gloss': 'enter',
        'polysemy': ['enter (verb)', 'in (directional suffix)'],
        'frequency': 180,
    },
    'khia': {
        'category': 'verb_root',
        'gloss': 'exit',
        'polysemy': ['exit (verb)', 'out (directional suffix)'],
        'frequency': 200,
    },
    'zum': {
        'category': 'verb_root',
        'gloss': 'bow',
        'frequency': 100,
    },
    'dam': {
        'category': 'verb_root',
        'gloss': 'be.well',  # Aligned with VERB_STEMS
        'frequency': 150,
    },
    'hot': {
        'category': 'verb_root',
        'gloss': 'save',
        'frequency': 120,
    },
    'heek': {
        'category': 'verb_root',
        'gloss': 'fold',
        'frequency': 15,
        'note': 'wink=eye-fold, twine=fold-together, betray=fold (give up)',
    },
    'thuah': {
        'category': 'verb_root',
        'gloss': 'gird',
        'polysemy': ['gird (verb: fasten around)', 'always (habitual aspect suffix)'],
        'frequency': 20,
        'note': 'Two distinct uses: as verb root and as aspectual suffix',
    },
    
    # === NOUN ROOTS ===
    'inn': {
        'category': 'noun_root',
        'gloss': 'house',
        'frequency': 400,
    },
    'sung': {
        'category': 'noun_root',
        'gloss': 'inside',
        'frequency': 500,
    },
    'lu': {
        'category': 'noun_root',
        'gloss': 'head',
        'frequency': 200,
    },
    'lung': {
        'category': 'noun_root',
        'gloss': 'heart',
        'frequency': 300,
    },
    'mei': {
        'category': 'noun_root',
        'gloss': 'fire',
        'polysemy': ['fire', 'female (Tibeto-Burman cognate *mei)'],
        'frequency': 150,
    },
    'tui': {
        'category': 'noun_root',
        'gloss': 'water',
        'frequency': 200,
    },
    'gam': {
        'category': 'noun_root',
        'gloss': 'land',
        'frequency': 350,
    },
    'mi': {
        'category': 'noun_root',
        'gloss': 'person',
        'frequency': 600,
    },
    'mik': {
        'category': 'noun_root',
        'gloss': 'eye',
        'frequency': 100,
    },
    'khua': {
        'category': 'noun_root',
        'gloss': 'town',
        'frequency': 200,
    },
    'thu': {
        'category': 'noun_root',
        'gloss': 'word',
        'frequency': 500,
    },
    'puan': {
        'category': 'noun_root',
        'gloss': 'cloth',
        'frequency': 80,
    },
    'buk': {
        'category': 'noun_root',
        'gloss': 'ambush',  # Aligned with NOUN_STEMS
        'polysemy': ['ambush', 'shelter/booth'],
        'frequency': 50,
    },
    'sa': {
        'category': 'noun_root',
        'gloss': 'flesh',
        'polysemy': ['flesh/meat', 'animal'],
        'frequency': 150,
    },
    'nam': {
        'category': 'noun_root',
        'gloss': 'kind',  # Aligned with NOUN_STEMS (minam = people-kind)
        'polysemy': ['kind/type', 'hair'],
        'frequency': 100,
    },
    'tang': {
        'category': 'noun_root',
        'gloss': 'stand',
        'polysemy': ['stand (verb)', 'leader/chief (person who stands)'],
        'frequency': 150,
    },
    'sing': {
        'category': 'noun_root',
        'gloss': 'tree',
        'frequency': 120,
    },
    'nai': {
        'category': 'noun_root',
        'gloss': 'precious',
        'frequency': 30,
    },
    'suang': {
        'category': 'noun_root',
        'gloss': 'stone',
        'frequency': 100,
    },
    'hawm': {
        'category': 'noun_root',
        'gloss': 'counsel',
        'polysemy': ['counsel', 'hollow/cave (suanghawm = stone-hollow = cave)'],
        'frequency': 80,
    },
    
    # === POLYSEMOUS ROOTS (important to document) ===
    'kal': {
        'category': 'noun_root',
        'gloss': 'liver',
        'polysemy': ['liver (body part)', 'middle (spatial, used in kikal, lamkal)'],
        'note': 'Two distinct meanings: kal₁=liver, kal₂=middle',
        'frequency': 50,
    },
    'lo': {
        'category': 'noun_root',
        'gloss': 'field',
        'polysemy': ['field (noun: lopa=farmer)', 'NEG (negation suffix)'],
        'note': 'Homophonous: lo=field vs lo=NEG',
        'frequency': 100,
    },
    'thau': {
        'category': 'noun_root',
        'gloss': 'fat',
        'frequency': 30,
    },
    'sau': {
        'category': 'adjective_root',
        'gloss': 'long',
        'frequency': 80,
    },
    'thum': {
        'category': 'numeral',
        'gloss': 'three',
        'frequency': 200,
    },
    'guk': {
        'category': 'numeral',
        'gloss': 'six',
        'frequency': 100,
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_morpheme(form: str) -> dict:
    """Get morpheme info, or None if not in inventory."""
    return MORPHEME_INVENTORY.get(form)


def get_gloss(form: str) -> str:
    """Get the primary gloss for a morpheme."""
    info = MORPHEME_INVENTORY.get(form)
    if info:
        return info['gloss']
    return None


def get_category(form: str) -> str:
    """Get the category of a morpheme."""
    info = MORPHEME_INVENTORY.get(form)
    if info:
        return info['category']
    return None


def has_polysemy(form: str) -> bool:
    """Check if a morpheme has documented polysemy."""
    info = MORPHEME_INVENTORY.get(form)
    return info and 'polysemy' in info


def get_all_senses(form: str) -> list:
    """Get all documented senses for a polysemous morpheme."""
    info = MORPHEME_INVENTORY.get(form)
    if info and 'polysemy' in info:
        return info['polysemy']
    if info:
        return [info['gloss']]
    return []


def validate_consistency(verb_stems: dict, noun_stems: dict) -> list:
    """
    Validate that MORPHEME_INVENTORY is consistent with main dictionaries.
    
    Returns list of inconsistencies found.
    """
    issues = []
    
    for form, info in MORPHEME_INVENTORY.items():
        cat = info.get('category', '')
        inv_gloss = info.get('gloss', '')
        
        if 'verb' in cat:
            if form in verb_stems:
                stem_gloss = verb_stems[form]
                if stem_gloss.lower() != inv_gloss.lower():
                    issues.append(f"VERB gloss mismatch: {form} = '{inv_gloss}' (inventory) vs '{stem_gloss}' (VERB_STEMS)")
        
        if 'noun' in cat:
            if form in noun_stems:
                stem_gloss = noun_stems[form]
                if stem_gloss.lower() != inv_gloss.lower():
                    issues.append(f"NOUN gloss mismatch: {form} = '{inv_gloss}' (inventory) vs '{stem_gloss}' (NOUN_STEMS)")
    
    return issues
