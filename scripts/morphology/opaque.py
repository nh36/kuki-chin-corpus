"""
Opaque Lexemes in Tedim Chin

These are words that LOOK like they could be decomposed into morphemes,
but the compositional meaning does NOT match the actual meaning.

Each entry includes:
- The opaque form and its actual meaning
- The "would-be parse" showing what WOULD happen without the override
- Evidence from KJV cross-reference

Format:
  'word': {
      'gloss': 'actual_meaning',
      'would_be_parse': ('seg-men-ta-tion', 'would-be-gloss'),
      'evidence': 'KJV reference showing actual meaning',
      'frequency': N,
  }
"""

OPAQUE_LEXEMES = {
    # === Kinship/person terms ===
    'sanggam': {
        'gloss': 'brother',
        'would_be_parse': ('sang-gam', 'high-land'),
        'evidence': 'Gen 4 - Cain and Abel as brothers',
        'frequency': 150,
    },
    
    # === Body/nature ===
    'lungno': {
        'gloss': 'worm',
        'would_be_parse': ('lung-no', 'heart-young'),
        'evidence': 'Job 25:6, Ps 22:6 - clearly "worm" creature',
        'frequency': 8,
    },
    'luanghawm': {
        'gloss': 'carcass',
        'would_be_parse': ('luang-hawm', 'flow-counsel'),
        'evidence': 'Lev 26:30 - dead body/corpse',
        'frequency': 39,
    },
    
    # === Objects ===
    'zungbuh': {
        'gloss': 'ring',
        'would_be_parse': ('zung-buh', 'root-rice'),
        'evidence': 'Gen 41:42 - Pharaoh\'s signet ring',
        'frequency': 15,
    },
    'singluang': {
        'gloss': 'beam',
        'would_be_parse': ('sing-luang', 'tree-flow'),
        'evidence': 'Wooden beam/timber in construction',
        'frequency': 12,
    },
    'lingkung': {
        'gloss': 'thorns',
        'would_be_parse': ('ling-kung', 'turn-?'),
        'evidence': 'Thorny plants/brambles',
        'frequency': 8,
    },
    'keelmul': {
        'gloss': 'goathair',
        'would_be_parse': ('keel-mul', 'goat-hair'),
        'evidence': 'Goat hair fabric - actually semi-transparent',
        'frequency': 6,
    },
    'thumu': {
        'gloss': 'trumpet',
        'would_be_parse': ('thu-mu', 'word-see'),
        'evidence': 'Judg 7:20 - trumpets in battle',
        'frequency': 28,
    },
    
    # === Abstract concepts ===
    'kholhna': {
        'gloss': 'divination',
        'would_be_parse': ('kholh-na', 'divine-NMLZ'),
        'evidence': 'Divination/sorcery - but kholh not otherwise attested as verb',
        'frequency': 12,
    },
    'lupna': {
        'gloss': 'bed',
        'would_be_parse': ('lup-na', 'bow.down-NMLZ'),
        'evidence': 'Matt 9:6 - "take up thy bed" - clearly furniture',
        'frequency': 85,
    },
    'zatui': {
        'gloss': 'medicine',
        'would_be_parse': ('za-tui', 'hear.I-water'),
        'evidence': 'Jer 8:22 - balm/medicine',
        'frequency': 13,
    },
    'golhguk': {
        'gloss': 'bribe',
        'would_be_parse': ('golh-guk', 'oppose-six'),
        'evidence': 'Exod 23:8, Deut 16:19 - bribery',
        'frequency': 5,
    },
    
    # === Spatial/relational ===
    'kikal': {
        'gloss': 'between',
        'would_be_parse': ('ki-kal', 'REFL-liver'),
        'evidence': 'Gen 1:6 - "between the waters" - spatial meaning',
        'frequency': 119,
        'note': 'kal₂ = middle (spatial) is distinct from kal₁ = liver (body part)',
    },
    
    # === Religious/cultural ===
    'singtawng': {
        'gloss': 'stock',
        'would_be_parse': ('sing-tawng', 'tree-?'),
        'evidence': 'Jer 2:27 - wooden idol/stock',
        'frequency': 5,
    },
    'aisan': {
        'gloss': 'magician',
        'would_be_parse': ('ai-san', '?-?'),
        'evidence': 'Gen 41:8 - Pharaoh\'s magicians',
        'frequency': 4,
    },
    'bangtan': {
        'gloss': 'shield',
        'would_be_parse': ('bang-tan', 'what-?'),
        'evidence': 'Military shield/buckler',
        'frequency': 30,
    },
    
    # === Work-related (IMPORTANT: na- is NOT a prefix!) ===
    'nasep': {
        'gloss': 'work',
        'would_be_parse': ('na-sep', '2SG-do'),  # NOT NMLZ-do because -na is suffix!
        'evidence': 'Gen 2:2 - God\'s work of creation',
        'frequency': 573,
        'note': 'Cannot be NMLZ-do because -na is a SUFFIX not prefix',
    },
    'nasem': {
        'gloss': 'servant',
        'would_be_parse': ('na-sem', '2SG-serve'),
        'evidence': 'Servant/minister - cf. nasemte (servants)',
        'frequency': 350,
        'note': 'Cannot be NMLZ-serve because -na is a SUFFIX not prefix',
    },
    
    # === Other ===
    'cingtaak': {
        'gloss': 'dwarf',
        'would_be_parse': ('cing-taak', 'grow-?'),
        'evidence': 'Lev 21:20 - physical condition',
        'frequency': 1,
    },
    'banbuh': {
        'gloss': 'armlet',
        'would_be_parse': ('ban-buh', 'hand-rice'),
        'evidence': 'Num 31:50 - arm jewelry',
        'frequency': 2,
    },
    'bulom': {
        'gloss': 'ruin',
        'would_be_parse': ('bu-lom', 'group-?'),
        'evidence': 'Ruined/desolate place',
        'frequency': 10,
    },
    'cimawh': {
        'gloss': 'oppress',
        'would_be_parse': ('ci-mawh', 'say-guilt'),
        'evidence': 'Oppression/affliction',
        'frequency': 8,
    },
}


def get_opaque_gloss(word: str) -> tuple:
    """
    Get the opaque gloss for a word.
    Returns (word, gloss) if opaque, None otherwise.
    """
    if word in OPAQUE_LEXEMES:
        return (word, OPAQUE_LEXEMES[word]['gloss'])
    return None


def get_would_be_parse(word: str) -> tuple:
    """
    Get what the parse WOULD be if we didn't treat this as opaque.
    Useful for debugging and documentation.
    """
    if word in OPAQUE_LEXEMES:
        return OPAQUE_LEXEMES[word]['would_be_parse']
    return None


def is_opaque(word: str) -> bool:
    """Check if a word is in the opaque lexicon."""
    return word in OPAQUE_LEXEMES
