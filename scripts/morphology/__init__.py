# Tedim Chin Morphology Module
# Refactored architecture with clear separation of concerns

from .inventory import MORPHEME_INVENTORY
from .affixes import PREFIXES, DERIVATIONAL_SUFFIXES, INFLECTIONAL_SUFFIXES, SUFFIX_ORDER
from .opaque import OPAQUE_LEXEMES
from .proper_nouns import PROPER_NOUNS

__all__ = [
    'MORPHEME_INVENTORY',
    'PREFIXES', 
    'DERIVATIONAL_SUFFIXES',
    'INFLECTIONAL_SUFFIXES',
    'SUFFIX_ORDER',
    'OPAQUE_LEXEMES',
    'PROPER_NOUNS',
]
