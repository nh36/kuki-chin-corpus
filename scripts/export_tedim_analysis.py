#!/usr/bin/env python3
"""
Export Tedim Chin Bible Analysis Pipeline

Processes the entire Tedim Bible corpus through the morphological analyzer
and produces structured outputs for dictionary and grammar work.

Output files:
    data/ctd_analysis/verses.tsv          - Verse-level metadata
    data/ctd_analysis/tokens.tsv          - Token-level full analysis
    data/ctd_analysis/wordforms.tsv       - Type-level wordform table
    data/ctd_analysis/lemmas.tsv          - Lemma table (dictionary seed)
    data/ctd_analysis/grammatical_morphemes.tsv - Grammatical morpheme inventory
    data/ctd_analysis/examples.tsv        - Curated examples bank
    data/ctd_analysis/ambiguities.tsv     - Review queue for uncertain analyses
    data/ctd_analysis/coverage_report.md  - Coverage statistics

Usage:
    python scripts/export_tedim_analysis.py [--output-dir DIR]

The script is deterministic: running twice on the same input produces identical output.
"""

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
import hashlib

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from analyze_morphemes import (
    analyze_word, analyze_sentence,
    VERB_STEMS, NOUN_STEMS, VERB_STEM_PAIRS, ATOMIC_GLOSSES,
    FUNCTION_WORDS, PROPER_NOUNS, TRANSPARENT_PROPER_NOUNS,
    TAM_SUFFIXES, CASE_MARKERS, NOMINALIZERS,
    PRONOMINAL_PREFIXES, OBJECT_PREFIXES,
    is_proper_noun, get_morpheme_gloss
)
from morphology.compounds import COMPOUND_WORDS

# =============================================================================
# GLOSS MAPPING: Convert analyzer glosses to English meanings
# =============================================================================

# Map common grammatical glosses to human-readable descriptions
GLOSS_TO_ENGLISH = {
    # Pronominal
    '1SG': 'I/my', '2SG': 'you/your', '3SG': 'he/she/it',
    '1PL': 'we/our', '1PL.INCL': 'we.inclusive', '1PL.EXCL': 'we.exclusive',
    '2PL': 'you.all', '3PL': 'they/their',
    # TAM
    'PST': 'past', 'FUT': 'future', 'PERF': 'perfect', 'PFV': 'perfective',
    'PROG': 'progressive', 'HAB': 'habitual', 'CONT': 'continuous',
    'IRR': 'irrealis', 'PROSP': 'prospective',
    # Case
    'ERG': 'ergative', 'LOC': 'locative', 'ABL': 'ablative',
    'COM': 'comitative', 'DAT': 'dative', 'GEN': 'genitive',
    # Derivation
    'NMLZ': 'nominalizer', 'CAUS': 'causative', 'APPL': 'applicative',
    'REFL': 'reflexive', 'RECIP': 'reciprocal',
    # Other
    'PL': 'plural', 'NEG': 'negative', 'Q': 'question',
    'IMP': 'imperative', 'HORT': 'hortative', 'DECL': 'declarative',
    'EMPH': 'emphatic', 'TOP': 'topic', 'FOC': 'focus',
    'ABIL': 'ability', 'COP': 'copula', 'EXCL': 'exclamative',
    'SIM': 'similative', 'DIR': 'directional',
    # Verbs with grammaticalized uses
    'be': 'be', 'do': 'do', 'go': 'go', 'come': 'come',
    'say': 'say', 'give': 'give', 'take': 'take', 'see': 'see',
    # Common stems
    'exist': 'exist/be', 'become': 'become', 'stand': 'stand',
}

# Known polysemous forms that need review
POLYSEMOUS_FORMS = {
    'hi': ['be', 'DECL', 'this'],
    'in': ['ERG', 'house', 'IMP'],
    'hong': ['come.DIR', 'DIR'],
    'ta': ['PFV', 'child'],
    'te': ['PL', 'small'],
    'na': ['2SG', 'NMLZ', 'pain'],
    'za': ['hundred', 'hear'],
    'zo': ['finish', 'able'],
    'pan': ['ABL', 'board', 'think'],
    'tung': ['arrive', 'on/above'],
    'thei': ['ABIL', 'know', 'fruit'],
    'khat': ['one', 'a/some'],
    'ding': ['PROSP', 'stand', 'IRR'],
    'bang': ['SIM', 'what', 'wall'],
    'tawh': ['COM', 'already'],
}

# High-frequency items that need strict sanity checking
# Maps lemma -> dominant function based on corpus analysis
HIGH_FREQUENCY_SEMANTIC_MAP = {
    'hi': {'dominant': 'DECL', 'type': 'grammatical', 'note': 'sentence-final declarative marker (88% of uses)'},
    'ding': {'dominant': 'IRR', 'type': 'grammatical', 'note': 'irrealis/prospective marker'},
    'hong': {'dominant': 'DIR', 'type': 'grammatical', 'note': 'directional (toward speaker)'},
    'ci': {'dominant': 'say', 'type': 'lexical', 'note': 'quotative verb'},
    'ahi': {'dominant': 'be.3SG', 'type': 'grammatical', 'note': 'copula 3rd person'},
    'ahih': {'dominant': 'be.NOM', 'type': 'grammatical', 'note': 'copula nominalized'},
    'tung': {'dominant': 'on', 'type': 'lexical', 'note': 'on/above; also "arrive"'},
    'om': {'dominant': 'exist', 'type': 'lexical', 'note': 'exist/be present'},
    'pai': {'dominant': 'go', 'type': 'lexical', 'note': 'go (not pour)'},
    'pan': {'dominant': 'ABL', 'type': 'grammatical', 'note': 'ablative case marker'},
    'thei': {'dominant': 'know', 'type': 'lexical', 'note': 'know/able (not fig)'},
    'thu': {'dominant': 'word', 'type': 'lexical', 'note': 'word/matter (not portion)'},
    'mu': {'dominant': 'see', 'type': 'lexical', 'note': 'see (not kiss)'},
    'kha': {'dominant': 'spirit', 'type': 'lexical', 'note': 'spirit/month (polysemous)'},
    'khat': {'dominant': 'one', 'type': 'lexical', 'note': 'one/a (numeral/article)'},
    'ta': {'dominant': 'PFV', 'type': 'grammatical', 'note': 'perfective aspect marker'},
    'te': {'dominant': 'PL', 'type': 'grammatical', 'note': 'plural marker'},
    'in': {'dominant': 'ERG', 'type': 'grammatical', 'note': 'ergative case marker'},
    'na': {'dominant': 'NMLZ', 'type': 'grammatical', 'note': 'nominalizer (also 2SG prefix)'},
    'lai': {'dominant': 'place', 'type': 'lexical', 'note': 'place/middle'},
    'mahmah': {'dominant': 'very', 'type': 'lexical', 'note': 'intensifier'},
}

# Glosses that are clearly grammatical (not lexical)
GRAMMATICAL_GLOSSES = {
    'DECL', 'IRR', 'PROSP', 'PFV', 'PL', 'ERG', 'LOC', 'ABL', 'COM', 'DAT',
    'NMLZ', 'CAUS', 'APPL', '1SG', '2SG', '3SG', '1PL', '2PL', '3PL',
    '1PL.INCL', '1PL.EXCL', 'REFL', 'RECIP', 'NEG', 'Q', 'IMP', 'HORT',
    'EMPH', 'TOP', 'FOC', 'PERF', 'CONT', 'HAB', 'DIR', 'CVB', 'QUOT',
}

def is_grammatical_gloss(gloss: str) -> bool:
    """Check if a gloss is purely grammatical."""
    if not gloss:
        return False
    # Check base gloss (before hyphen)
    base = gloss.split('-')[0] if '-' in gloss else gloss
    # Check for .I/.II verb forms
    if '.' in base:
        base = base.split('.')[0]
    return base.upper() == base and base in GRAMMATICAL_GLOSSES

def get_english_gloss(stem: str, analyzer_gloss: str) -> str:
    """
    Get English meaning for a stem, using analyzer data.
    
    Priority:
    1. HIGH_FREQUENCY_SEMANTIC_MAP (corpus-validated dominant glosses)
    2. If analyzer_gloss is clearly lexical (not all caps), use it
    3. VERB_STEMS / NOUN_STEMS
    4. COMPOUND_WORDS
    5. Grammatical gloss mapping
    6. The analyzer gloss itself as fallback
    """
    stem_lower = stem.lower()
    
    # 1. Check HIGH_FREQUENCY_SEMANTIC_MAP for corpus-validated glosses
    if stem_lower in HIGH_FREQUENCY_SEMANTIC_MAP:
        sem_info = HIGH_FREQUENCY_SEMANTIC_MAP[stem_lower]
        # Return the dominant gloss (which is corpus-validated)
        return sem_info['dominant']
    
    # 2. If analyzer_gloss is clearly lexical (not all caps), prefer it
    if analyzer_gloss and not analyzer_gloss.isupper():
        # Strip Form II markers for cleaner output
        clean_gloss = analyzer_gloss.replace('.I', '').replace('.II', '')
        if clean_gloss.isalpha():
            return clean_gloss
    
    # 3. Check VERB_STEMS
    if stem_lower in VERB_STEMS:
        gloss = VERB_STEMS[stem_lower]
        return gloss.replace('.I', '').replace('.II', '')
    
    # 4. Check NOUN_STEMS
    if stem_lower in NOUN_STEMS:
        return NOUN_STEMS[stem_lower]
    
    # 5. Check ATOMIC_GLOSSES (but not for polysemous items)
    if stem_lower in ATOMIC_GLOSSES and stem_lower not in POLYSEMOUS_FORMS:
        return ATOMIC_GLOSSES[stem_lower]
    
    # 6. Check COMPOUND_WORDS for stem
    if stem_lower in COMPOUND_WORDS:
        _, gloss = COMPOUND_WORDS[stem_lower]
        # Convert compound gloss format
        if '-' in gloss:
            # e.g., 'disciple-PL' -> 'disciple'
            base_gloss = gloss.split('-')[0]
            if base_gloss and not base_gloss.isupper():
                return base_gloss
        elif not gloss.isupper():
            return gloss
    
    # 7. Map grammatical glosses
    if analyzer_gloss in GLOSS_TO_ENGLISH:
        return GLOSS_TO_ENGLISH[analyzer_gloss]
    
    # 8. Try first part of hyphenated gloss
    if '-' in analyzer_gloss:
        first = analyzer_gloss.split('-')[0]
        if first in GLOSS_TO_ENGLISH:
            return GLOSS_TO_ENGLISH[first]
        if not first.isupper() and first.isalpha():
            return first
    
    # 9. If it's not all caps (grammatical marker), use as-is
    if analyzer_gloss and not analyzer_gloss.isupper():
        return analyzer_gloss
    
    # 10. Fallback
    return '?'

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TokenAnalysis:
    """Full analysis of a single token."""
    verse_id: str
    token_index: int
    surface_form: str
    normalized_form: str
    segmentation: str
    gloss: str
    lemma: str
    pos: str  # N, V, ADV, FUNC, PROP, etc.
    stem_form: str
    stem_alternation: str  # 'I', 'II', or ''
    prefix_chain: str
    suffix_chain: str
    is_proper_noun: bool
    is_ambiguous: bool
    confidence: str  # 'high', 'medium', 'low', 'unknown'
    kjv_text: str
    
@dataclass
class WordformEntry:
    """Type-level wordform aggregation."""
    surface_form: str
    normalized_form: str
    lemma: str
    segmentation: str
    gloss: str
    pos: str
    frequency: int = 0
    first_verse: str = ''
    sample_verses: List[str] = field(default_factory=list)
    is_ambiguous: bool = False
    status: str = 'auto'  # auto, needs_review, reviewed

@dataclass
class SenseEntry:
    """A single sense/meaning of a lemma."""
    sense_id: str  # e.g., "sih.1" for first sense of sih
    gloss: str  # English gloss for this sense
    pos: str  # POS for this sense (may differ from other senses)
    frequency: int = 0  # Token count for this sense
    is_primary: bool = False  # True if this is the dominant sense
    is_grammatical: bool = False  # True if this sense is grammatical function
    example_verses: List[Tuple[str, str, str, str, str]] = field(default_factory=list)
    inflected_forms: Set[str] = field(default_factory=set)
    notes: str = ''

@dataclass 
class LemmaEntry:
    """Lemma-level dictionary entry with multiple senses."""
    lemma: str
    citation_form: str
    pos: str  # Primary POS (most frequent)
    primary_gloss: str = ''  # Best English gloss (corpus-validated)
    gloss_candidates: List[str] = field(default_factory=list)  # All gloss candidates
    review_gloss_summary: str = ''  # For ambiguous items: "be | DECL | this"
    all_glosses: Set[str] = field(default_factory=set)  # All attested glosses
    gloss_counts: Dict[str, int] = field(default_factory=dict)  # Frequency per gloss
    english_glosses: Set[str] = field(default_factory=set)  # English meanings
    inflected_forms: Set[str] = field(default_factory=set)
    token_count: int = 0
    form_count: int = 0
    derivational_family: Set[str] = field(default_factory=set)
    compounds: Set[str] = field(default_factory=set)
    collocates: Dict[str, int] = field(default_factory=dict)
    example_verses: List[Tuple[str, str, str, str, str]] = field(default_factory=list)  # (verse_id, tedim, kjv, segmented, glossed)
    # Sense tracking
    senses: List[SenseEntry] = field(default_factory=list)  # Multiple senses for this lemma
    pos_variants: Dict[str, int] = field(default_factory=dict)  # POS -> frequency (for headword splitting)
    polysemy_notes: str = ''
    grammaticalization_notes: str = ''
    is_polysemous: bool = False
    needs_review: bool = False
    entry_status: str = 'auto'  # 'clean', 'polysemous_review', 'mixed_lex_gram', 'unsafe_gloss'
    is_grammatical: bool = False  # True if primarily grammatical function

@dataclass
class GrammaticalMorpheme:
    """Grammatical morpheme entry."""
    form: str
    gloss: str
    category: str  # case, tam, particle, nominalizer, prefix, etc.
    subcategory: str = ''  # More specific classification
    frequency: int = 0
    environments: Set[str] = field(default_factory=set)  # prefix, suffix, clitic, etc.
    example_verses: List[Tuple[str, str, str, str, str]] = field(default_factory=list)  # With segmented/glossed
    ambiguity_notes: str = ''
    review_reasons: List[str] = field(default_factory=list)
    status: str = 'auto'
    is_polysemous: bool = False

@dataclass
class ExampleEntry:
    """Curated example for dictionary/grammar."""
    item_type: str  # 'lemma' or 'morpheme'
    item_id: str  # lemma or morpheme form
    verse_id: str
    tedim_text: str
    segmented: str
    glossed: str
    kjv_text: str
    example_quality: str  # 'shortest', 'canonical', 'transparent', 'marked'
    word_count: int

# =============================================================================
# MORPHEME CLASSIFICATION (Context-Sensitive)
# =============================================================================

# Define grammatical categories with their gloss patterns
# Format: category -> {form: set of valid glosses for this form in this category}
MORPHEME_CATEGORIES = {
    'case_marker': {
        'in': {'ERG'},  # Ergative (not IMP, not house)
        'ah': {'LOC', 'DAT'},  # Locative/dative
        'pan': {'ABL'},  # Ablative (not 'board' or 'think')
        'tawh': {'COM'},  # Comitative (not 'already')
    },
    'tam_suffix': {
        'ta': {'PFV'},  # Perfective (not 'child')
        'zo': {'COMPL'},  # Completive (not 'finish')
        'khin': {'COMPL'},
        'lai': {'CONT', 'still'},
        'zel': {'CONT'},
        'ngei': {'EXPER'},
        'gige': {'HAB'},
        'kik': {'again'},
        'pah': {'INCH', 'immediately'},
        'sak': {'CAUS', 'BEN'},
        'pih': {'APPL'},
    },
    'irrealis_marker': {
        'ding': {'IRR', 'PROSP'},  # NOT case marker
        'dingin': {'IRR', 'PROSP'},
    },
    'plural_marker': {
        'te': {'PL'},  # NOT nominalizer
        'uh': {'PL'},
    },
    'nominalizer': {
        'na': {'NMLZ'},  # Only when gloss is NMLZ, not 2SG
    },
    'pronominal_prefix': {
        'ka': {'1SG'},
        'na': {'2SG'},  # Only when gloss is 2SG, not NMLZ
        'a': {'3SG'},
        'i': {'1PL.INCL'},
        'ei': {'1PL.EXCL'},
    },
    'object_marker': {
        'hong': {'1SG.OBJ', '1PL.OBJ', 'DIR'},  # Directional/object
        'min': {'2SG.OBJ'},
    },
    'sentence_final': {
        'hi': {'DECL'},  # Only sentence-final declarative
        'hiam': {'Q'},
        'hen': {'HORT'},
        'ang': {'FUT'},
        've': {'EMPH'},
        'eh': {'EXCL'},
    },
    'auxiliary': {
        'thei': {'ABIL'},  # Ability (not 'know' or 'fruit')
        'theih': {'ABIL.II'},
        'nuam': {'want'},
    },
    'directional_verb': {
        'khia': {'out'},
        'lut': {'in'},
        'pai': {'go'},
        'hong': {'come'},  # As main verb
        'kik': {'back'},
        'tung': {'arrive', 'up'},
        'tang': {'down'},
    },
    'particle': {
        'pen': {'TOP'},
        'zong': {'also'},
        'mah': {'EMPH'},
        'bek': {'only'},
        'peuh': {'every', 'any'},
        'leh': {'and', 'if'},
        'le': {'and'},
    },
    'copula': {
        'ahi': {'COP', 'be.3SG'},
        'ahih': {'COP.REL', 'be.3SG.REL'},
    },
}

def classify_morpheme_contextual(morpheme: str, gloss: str, position: str, 
                                 is_final: bool = False, full_gloss: str = '') -> Tuple[str, str, bool]:
    """
    Classify a morpheme using context-sensitive rules.
    
    Args:
        morpheme: The morpheme form
        gloss: The gloss for this specific morpheme
        position: 'prefix', 'stem', 'suffix', or 'standalone'
        is_final: Whether this is the final morpheme in the word
        full_gloss: The full word gloss for context
    
    Returns:
        (type, category, is_polysemous) where:
        - type: 'grammatical', 'lexical', or 'ambiguous'
        - category: specific category like 'case_marker', 'tam_suffix', etc.
        - is_polysemous: whether this form needs review
    """
    m_lower = morpheme.lower()
    g_upper = gloss.upper() if gloss else ''
    
    # Check if this is a known polysemous form
    is_polysemous = m_lower in POLYSEMOUS_FORMS
    
    # Check each category with gloss matching
    for category, forms in MORPHEME_CATEGORIES.items():
        if m_lower in forms:
            valid_glosses = forms[m_lower]
            # Check if the actual gloss matches expected glosses for this category
            if g_upper in valid_glosses or gloss in valid_glosses:
                return ('grammatical', category, is_polysemous)
    
    # Special handling for ambiguous cases based on position and context
    
    # 'na' as prefix = 2SG, as suffix = NMLZ
    if m_lower == 'na':
        if position == 'prefix' and g_upper == '2SG':
            return ('grammatical', 'pronominal_prefix', True)
        elif position == 'suffix' and g_upper == 'NMLZ':
            return ('grammatical', 'nominalizer', True)
        elif g_upper == '2SG':
            return ('grammatical', 'pronominal_prefix', True)
        elif g_upper == 'NMLZ':
            return ('grammatical', 'nominalizer', True)
        # Unknown use
        return ('ambiguous', 'unknown', True)
    
    # 'hi' at end of sentence = DECL, otherwise lexical verb 'be'
    if m_lower == 'hi':
        if is_final and g_upper == 'DECL':
            return ('grammatical', 'sentence_final', True)
        elif gloss.lower() in ('be', 'this', 'prox'):
            return ('lexical', 'verb', True)
        return ('ambiguous', 'copula_or_decl', True)
    
    # 'ding' is TAM/irrealis, not case
    if m_lower == 'ding':
        if g_upper in ('IRR', 'PROSP'):
            return ('grammatical', 'irrealis_marker', True)
        elif gloss.lower() == 'stand':
            return ('lexical', 'verb', True)
        return ('grammatical', 'irrealis_marker', True)  # Default to grammatical
    
    # 'te' is plural marker, not nominalizer
    if m_lower == 'te':
        if g_upper == 'PL':
            return ('grammatical', 'plural_marker', True)
        elif gloss.lower() == 'small':
            return ('lexical', 'adjective', True)
        return ('grammatical', 'plural_marker', True)
    
    # 'in' as suffix = ERG, as standalone/prefix = different
    if m_lower == 'in':
        if position == 'suffix' and g_upper == 'ERG':
            return ('grammatical', 'case_marker', True)
        elif g_upper == 'IMP':
            return ('grammatical', 'sentence_final', True)
        elif gloss.lower() == 'house':
            return ('lexical', 'noun', True)
        return ('grammatical', 'case_marker', True)
    
    # 'hong' as directional vs object marker
    if m_lower == 'hong':
        if position == 'prefix':
            return ('grammatical', 'object_marker', True)
        elif gloss.lower() in ('come', 'come.dir'):
            return ('grammatical', 'directional_verb', True)
        return ('grammatical', 'directional_verb', True)
    
    # Check if it's a known lexical stem
    if m_lower in VERB_STEMS:
        return ('lexical', 'verb', is_polysemous)
    if m_lower in NOUN_STEMS:
        return ('lexical', 'noun', is_polysemous)
    if m_lower in VERB_STEM_PAIRS:
        return ('lexical', 'verb_ii', is_polysemous)
    
    # Check function words
    if m_lower in FUNCTION_WORDS:
        return ('grammatical', 'function_word', is_polysemous)
    
    # Check if gloss suggests grammatical function
    gram_glosses = {'ERG', 'LOC', 'ABL', 'COM', 'DAT', 'GEN', 'POSS',
                    'PL', 'SG', 'NMLZ', 'CAUS', 'APPL', 'REFL', 'RECIP',
                    'PST', 'FUT', 'PERF', 'PROG', 'HAB', 'CONT', 'PFV',
                    '1SG', '2SG', '3SG', '1PL', '2PL', '3PL',
                    'Q', 'NEG', 'IMP', 'HORT', 'DECL', 'EXCL',
                    'IRR', 'PROSP', 'ABIL', 'COP', 'TOP', 'EMPH'}
    if g_upper in gram_glosses:
        return ('grammatical', 'inflection', is_polysemous)
    
    # Default to lexical unknown
    return ('lexical', 'unknown', is_polysemous)


def classify_morpheme(morpheme: str, gloss: str, position: str = 'suffix') -> Tuple[str, str]:
    """
    Legacy wrapper for classify_morpheme_contextual.
    
    Returns:
        (category, subcategory) - e.g., ('grammatical', 'case') or ('lexical', 'verb')
    """
    mtype, cat, _ = classify_morpheme_contextual(morpheme, gloss, position)
    return (mtype, cat)

def extract_lemma(surface: str, segmentation: str, gloss: str, pos: str) -> str:
    """
    Extract the lemma (citation form) from an analyzed word.
    
    For verbs: use Form I if available
    For nouns: use bare stem
    For proper nouns: use title case
    """
    # Handle proper nouns
    if pos == 'PROP':
        return surface.title()
    
    # Parse segmentation to find stem
    parts = segmentation.replace("'", '').split('-')
    if not parts:
        return surface.lower()
    
    # Find the main stem (usually first non-prefix part)
    stem = parts[0].lower()
    
    # Skip prefixes
    prefix_forms = set(PRONOMINAL_PREFIXES.keys()) | set(OBJECT_PREFIXES.keys()) | {'ki', 'a', 'na', 'i'}
    for i, part in enumerate(parts):
        p_lower = part.lower()
        if p_lower not in prefix_forms:
            stem = p_lower
            break
    
    # For Form II verbs, try to get Form I
    if stem in VERB_STEM_PAIRS:
        form_i, _ = VERB_STEM_PAIRS[stem]
        return form_i
    
    # Check if it's a known stem
    if stem in VERB_STEMS or stem in NOUN_STEMS:
        return stem
    
    return stem

def determine_pos(segmentation: str, gloss: str, surface: str) -> str:
    """Determine part of speech from analysis."""
    gloss_upper = gloss.upper()
    seg_lower = segmentation.lower()
    
    # Proper nouns (all caps gloss)
    if gloss == surface.upper() and surface[0].isupper():
        return 'PROP'
    
    # Check for grammatical markers in gloss
    if any(g in gloss_upper for g in ['ERG', 'LOC', 'ABL', 'COM', 'DAT']):
        # Has case marking - check stem
        pass
    
    # Find stem in segmentation
    parts = seg_lower.replace("'", '').split('-')
    for part in parts:
        if part in VERB_STEMS or part in VERB_STEM_PAIRS:
            return 'V'
        if part in NOUN_STEMS:
            return 'N'
    
    # Check gloss patterns
    if 'NMLZ' in gloss_upper:
        return 'N'
    if any(t in gloss_upper for t in ['PST', 'FUT', 'PERF', 'PROG', 'ABIL', 'CAUS']):
        return 'V'
    
    # Function words
    first_part = parts[0] if parts else ''
    if first_part in FUNCTION_WORDS:
        return 'FUNC'
    
    return 'UNK'

def extract_affixes(segmentation: str, gloss: str) -> Tuple[str, str]:
    """Extract prefix and suffix chains from segmentation."""
    parts = segmentation.replace("'", '').split('-')
    gloss_parts = gloss.split('-')
    
    if len(parts) <= 1:
        return ('', '')
    
    prefixes = []
    suffixes = []
    
    # Known prefix forms
    prefix_forms = set(PRONOMINAL_PREFIXES.keys()) | set(OBJECT_PREFIXES.keys()) | {'ki', 'a'}
    
    # Find stem position (first non-prefix lexical item)
    stem_idx = 0
    for i, part in enumerate(parts):
        if part.lower() not in prefix_forms:
            stem_idx = i
            break
    
    # Everything before stem is prefix
    for i in range(stem_idx):
        prefixes.append(parts[i])
    
    # Everything after stem is suffix (simplified)
    for i in range(stem_idx + 1, len(parts)):
        suffixes.append(parts[i])
    
    return ('-'.join(prefixes), '-'.join(suffixes))

def get_stem_alternation(segmentation: str, gloss: str) -> str:
    """Detect Form I/II alternation."""
    if '.II' in gloss:
        return 'II'
    if '.I' in gloss:
        return 'I'
    
    # Check if stem is in VERB_STEM_PAIRS
    parts = segmentation.replace("'", '').split('-')
    for part in parts:
        if part.lower() in VERB_STEM_PAIRS:
            return 'II'
    
    return ''

def assess_confidence(segmentation: str, gloss: str) -> str:
    """Assess analysis confidence."""
    if '?' in gloss:
        if gloss.startswith('?'):
            return 'unknown'
        return 'low'
    
    # Check for ambiguous patterns
    if gloss.count('-') > 4:  # Very complex analysis
        return 'medium'
    
    return 'high'

# =============================================================================
# DATA LOADING
# =============================================================================

def load_bible_data(bible_path: str, kjv_path: str = None) -> Dict[str, Dict]:
    """Load Bible verses and optional KJV translations."""
    verses = {}
    
    # Load Tedim Bible
    with open(bible_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                verse_id = parts[0]
                text = parts[1]
                verses[verse_id] = {'tedim': text, 'kjv': ''}
    
    # Load KJV if available
    if kjv_path and os.path.exists(kjv_path):
        with open(kjv_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    verse_id = parts[0]
                    kjv_text = parts[2]
                    if verse_id in verses:
                        verses[verse_id] = {'tedim': verses[verse_id]['tedim'], 'kjv': kjv_text}
    
    return verses

def normalize_form(word: str) -> str:
    """Normalize a surface form for consistent matching."""
    # Convert curly quotes to straight
    word = word.replace(''', "'").replace(''', "'")
    word = word.replace('"', '"').replace('"', '"')
    # Lowercase for matching
    return word.lower()


def _finalize_lemma_gloss(lem: LemmaEntry) -> None:
    """
    Finalize primary gloss using corpus frequency evidence.
    
    Strategy:
    1. For known high-frequency items, use curated semantic map
    2. For polysemous items, use frequency-dominant gloss (if >70%)
    3. Otherwise, mark for review with gloss summary
    """
    lemma_lower = lem.lemma.lower()
    
    # Build gloss candidates sorted by frequency
    sorted_glosses = sorted(lem.gloss_counts.items(), key=lambda x: -x[1])
    lem.gloss_candidates = [g for g, _ in sorted_glosses[:5]]
    
    # Check for known high-frequency semantic mappings
    if lemma_lower in HIGH_FREQUENCY_SEMANTIC_MAP:
        sem_info = HIGH_FREQUENCY_SEMANTIC_MAP[lemma_lower]
        
        # Check if corpus supports the expected dominant gloss
        if sorted_glosses:
            top_gloss, top_count = sorted_glosses[0]
            dominance = top_count / lem.token_count if lem.token_count > 0 else 0
            
            # If the item is primarily grammatical, mark it
            if sem_info['type'] == 'grammatical':
                lem.is_grammatical = True
                
                # Check if grammatical use dominates (>60%)
                gram_count = sum(c for g, c in lem.gloss_counts.items() 
                               if is_grammatical_gloss(g))
                gram_ratio = gram_count / lem.token_count if lem.token_count > 0 else 0
                
                if gram_ratio > 0.6:
                    # Use expected grammatical gloss
                    lem.primary_gloss = sem_info['dominant']
                    lem.entry_status = 'clean' if gram_ratio > 0.8 else 'polysemous_review'
                else:
                    # Mixed use - needs review
                    lem.primary_gloss = ''
                    lem.review_gloss_summary = ' | '.join(lem.gloss_candidates[:3])
                    lem.entry_status = 'mixed_lex_gram'
                    lem.needs_review = True
            else:
                # Lexical item - use corpus-dominant lexical gloss
                lexical_glosses = [(g, c) for g, c in sorted_glosses 
                                  if not is_grammatical_gloss(g)]
                if lexical_glosses:
                    lem.primary_gloss = get_english_gloss(lem.lemma, lexical_glosses[0][0])
                    lex_dominance = lexical_glosses[0][1] / lem.token_count
                    if lex_dominance > 0.7:
                        lem.entry_status = 'clean'
                    else:
                        lem.entry_status = 'polysemous_review'
                        lem.needs_review = True
                else:
                    lem.primary_gloss = sem_info['dominant']
        
        lem.grammaticalization_notes = sem_info.get('note', '')
        return
    
    # For non-high-frequency items, use corpus evidence
    if not sorted_glosses:
        lem.primary_gloss = '?'
        lem.entry_status = 'unsafe_gloss'
        lem.needs_review = True
        return
    
    top_gloss, top_count = sorted_glosses[0]
    dominance = top_count / lem.token_count if lem.token_count > 0 else 0
    
    # Check for grammatical vs lexical split
    gram_count = sum(c for g, c in lem.gloss_counts.items() if is_grammatical_gloss(g))
    lex_count = lem.token_count - gram_count
    
    # Strong grammatical dominance
    if gram_count > lex_count * 2 and gram_count > 100:
        lem.is_grammatical = True
        lem.primary_gloss = top_gloss
        lem.entry_status = 'clean'
        return
    
    # Mixed lexical-grammatical
    if gram_count > 0 and lex_count > 0 and min(gram_count, lex_count) / max(gram_count, lex_count) > 0.2:
        lem.entry_status = 'mixed_lex_gram'
        lem.review_gloss_summary = ' | '.join(lem.gloss_candidates[:3])
        lem.needs_review = True
        # Use the dominant non-grammatical gloss
        lex_glosses = [(g, c) for g, c in sorted_glosses if not is_grammatical_gloss(g)]
        if lex_glosses:
            lem.primary_gloss = get_english_gloss(lem.lemma, lex_glosses[0][0])
        else:
            lem.primary_gloss = top_gloss
        return
    
    # Clear dominance (>70%) - assign confidently
    if dominance > 0.7:
        lem.primary_gloss = get_english_gloss(lem.lemma, top_gloss)
        lem.entry_status = 'clean'
        return
    
    # Multiple competing glosses - polysemous review
    if len(sorted_glosses) >= 2:
        second_count = sorted_glosses[1][1]
        competition_ratio = second_count / top_count if top_count > 0 else 0
        
        if competition_ratio > 0.3:
            # Significant competition between glosses
            lem.entry_status = 'polysemous_review'
            lem.review_gloss_summary = ' | '.join(lem.gloss_candidates[:3])
            lem.needs_review = True
            lem.is_polysemous = True
            # Still set primary to most frequent
            lem.primary_gloss = get_english_gloss(lem.lemma, top_gloss)
            return
    
    # Default: use top gloss
    lem.primary_gloss = get_english_gloss(lem.lemma, top_gloss)
    lem.entry_status = 'clean' if dominance > 0.5 else 'polysemous_review'
    if lem.entry_status == 'polysemous_review':
        lem.needs_review = True


def _build_senses(lem: LemmaEntry) -> None:
    """
    Build sense entries from collected gloss and POS data.
    
    Strategy:
    - Different POS = different headwords (stored as separate senses with pos marker)
    - Same POS, different English gloss = different senses of same headword
    - Merge analyzer glosses that resolve to the same English gloss
    - Group examples by the sense they attest
    """
    # Step 1: Map each analyzer gloss to (POS, English gloss)
    # This will let us merge glosses that are really the same meaning
    gloss_to_english = {}
    gloss_to_pos = {}
    
    for analyzer_gloss, count in lem.gloss_counts.items():
        # Determine POS
        if is_grammatical_gloss(analyzer_gloss):
            pos = 'FUNC'
            eng_gloss = analyzer_gloss  # Keep grammatical glosses as-is
        else:
            # Use the most common POS variant for lexical glosses
            if lem.pos_variants:
                lex_pos = [(p, c) for p, c in lem.pos_variants.items() if p not in ('FUNC', 'UNK')]
                if lex_pos:
                    pos = max(lex_pos, key=lambda x: x[1])[0]
                else:
                    pos = lem.pos
            else:
                pos = lem.pos
            # Get English gloss
            eng_gloss = get_english_gloss(lem.lemma, analyzer_gloss)
        
        gloss_to_english[analyzer_gloss] = eng_gloss
        gloss_to_pos[analyzer_gloss] = pos
    
    # Step 2: Group by (POS, English gloss) and sum frequencies
    # Key: (pos, english_gloss) -> {total_freq, analyzer_glosses}
    sense_groups = {}
    for analyzer_gloss, count in lem.gloss_counts.items():
        pos = gloss_to_pos[analyzer_gloss]
        eng = gloss_to_english[analyzer_gloss]
        key = (pos, eng)
        
        if key not in sense_groups:
            sense_groups[key] = {
                'frequency': 0,
                'analyzer_glosses': [],
                'is_grammatical': is_grammatical_gloss(analyzer_gloss)
            }
        sense_groups[key]['frequency'] += count
        sense_groups[key]['analyzer_glosses'].append(analyzer_gloss)
    
    # Step 3: Sort senses by frequency (highest first)
    # Primary sense should be the most frequent regardless of POS
    sorted_senses = sorted(sense_groups.items(), 
                          key=lambda x: -x[1]['frequency'])
    
    # Step 4: Build sense entries
    lem.senses = []
    sense_num = 1
    
    for (pos, eng_gloss), data in sorted_senses:
        sense = SenseEntry(
            sense_id=f"{lem.lemma}.{sense_num}",
            gloss=eng_gloss,
            pos=pos,
            frequency=data['frequency'],
            is_primary=(sense_num == 1),
            is_grammatical=data['is_grammatical']
        )
        
        # Find examples that match any of the analyzer glosses for this sense
        matching_glosses = set(data['analyzer_glosses'])
        for ex in lem.example_verses:
            verse_id, tedim, kjv, seg, full_gloss = ex
            first_gloss = full_gloss.split('-')[0] if '-' in full_gloss else full_gloss
            if first_gloss in matching_glosses and len(sense.example_verses) < 5:
                sense.example_verses.append(ex)
                sense.inflected_forms.add(seg.split('-')[0] if '-' in seg else seg)
        
        lem.senses.append(sense)
        sense_num += 1
    
    # Update lemma's primary POS to the most frequent one
    if lem.pos_variants:
        lem.pos = max(lem.pos_variants.items(), key=lambda x: x[1])[0]


# =============================================================================
# MAIN ANALYSIS PIPELINE
# =============================================================================

def analyze_corpus(verses: Dict[str, Dict]) -> Tuple[List[TokenAnalysis], Dict, Dict, Dict]:
    """
    Analyze entire corpus, producing token-level analyses and aggregations.
    
    Returns:
        tokens: List of TokenAnalysis
        wordforms: Dict[normalized_form, WordformEntry]
        lemmas: Dict[lemma, LemmaEntry]
        gram_morphemes: Dict[form, GrammaticalMorpheme]
    """
    tokens = []
    wordforms = {}
    lemmas = {}
    gram_morphemes = {}
    
    # Track collocations (word pairs)
    collocations = defaultdict(lambda: defaultdict(int))
    
    # Process verses in deterministic order
    for verse_id in sorted(verses.keys()):
        verse_data = verses[verse_id]
        tedim_text = verse_data['tedim']
        kjv_text = verse_data.get('kjv', '')
        
        # Use sentence-level analysis for context-aware disambiguation
        # This handles homophones like thum (three/entreat/mourn), ngen (pray/net),
        # kei (NEG/1SG.PRO), hu (help/breath) based on surrounding words
        sentence_analysis = analyze_sentence(tedim_text)
        
        # Tokenize
        words = tedim_text.split()
        prev_lemma = None
        
        for idx, word in enumerate(words):
            # Clean punctuation for analysis
            clean_word = word.strip('.,;:!?"\'')
            if not clean_word:
                continue
            
            # Use sentence-level analysis if available (context-aware)
            if idx < len(sentence_analysis):
                _, segmentation, gloss, _ = sentence_analysis[idx]
            else:
                # Fallback to word-level analysis
                segmentation, gloss = analyze_word(clean_word)
            normalized = normalize_form(clean_word)
            
            # Determine properties
            pos = determine_pos(segmentation, gloss, clean_word)
            lemma = extract_lemma(clean_word, segmentation, gloss, pos)
            prefix_chain, suffix_chain = extract_affixes(segmentation, gloss)
            stem_alt = get_stem_alternation(segmentation, gloss)
            confidence = assess_confidence(segmentation, gloss)
            is_proper = pos == 'PROP'
            is_ambig = '?' in gloss or confidence in ('low', 'unknown')
            
            # Find stem form
            parts = segmentation.replace("'", '').split('-')
            stem_form = lemma
            for part in parts:
                p_lower = part.lower()
                if p_lower in VERB_STEMS or p_lower in NOUN_STEMS or p_lower in VERB_STEM_PAIRS:
                    stem_form = p_lower
                    break
            
            # Create token analysis
            token = TokenAnalysis(
                verse_id=verse_id,
                token_index=idx,
                surface_form=clean_word,
                normalized_form=normalized,
                segmentation=segmentation,
                gloss=gloss,
                lemma=lemma,
                pos=pos,
                stem_form=stem_form,
                stem_alternation=stem_alt,
                prefix_chain=prefix_chain,
                suffix_chain=suffix_chain,
                is_proper_noun=is_proper,
                is_ambiguous=is_ambig,
                confidence=confidence,
                kjv_text=kjv_text
            )
            tokens.append(token)
            
            # Aggregate wordforms
            wf_key = (normalized, segmentation, gloss)
            if wf_key not in wordforms:
                wordforms[wf_key] = WordformEntry(
                    surface_form=clean_word,
                    normalized_form=normalized,
                    lemma=lemma,
                    segmentation=segmentation,
                    gloss=gloss,
                    pos=pos,
                    first_verse=verse_id,
                    is_ambiguous=is_ambig,
                    status='needs_review' if is_ambig else 'auto'
                )
            wf = wordforms[wf_key]
            wf.frequency += 1
            if len(wf.sample_verses) < 5:
                wf.sample_verses.append(verse_id)
            
            # Aggregate lemmas (skip unknowns and function words for main lemma table)
            if confidence != 'unknown' and pos not in ('FUNC',):
                if lemma not in lemmas:
                    lemmas[lemma] = LemmaEntry(
                        lemma=lemma,
                        citation_form=lemma,
                        pos=pos,
                        is_polysemous=lemma.lower() in POLYSEMOUS_FORMS,
                        needs_review=pos == 'UNK' or lemma.lower() in POLYSEMOUS_FORMS
                    )
                lem = lemmas[lemma]
                
                # Track POS variants for this lemma (for headword splitting)
                lem.pos_variants[pos] = lem.pos_variants.get(pos, 0) + 1
                
                # Collect all attested glosses with frequency counts
                first_gloss = gloss.split('-')[0] if '-' in gloss else gloss
                lem.all_glosses.add(first_gloss)
                lem.gloss_counts[first_gloss] = lem.gloss_counts.get(first_gloss, 0) + 1
                
                # Track if this is a grammatical use
                if is_grammatical_gloss(first_gloss):
                    lem.is_grammatical = True
                
                # Try to get English meaning
                eng = get_english_gloss(stem_form, first_gloss)
                if eng and eng != '?':
                    lem.english_glosses.add(eng)
                
                lem.inflected_forms.add(normalized)
                lem.token_count += 1
                
                # Store examples with their specific gloss for sense-level tracking
                # Format: (verse_id, tedim, kjv, segmented, full_gloss)
                if len(lem.example_verses) < 20:  # Store more examples for sense selection
                    lem.example_verses.append((verse_id, tedim_text, kjv_text, segmentation, gloss))
                
                # Track collocations
                if prev_lemma and prev_lemma != lemma:
                    collocations[prev_lemma][lemma] += 1
                    collocations[lemma][prev_lemma] += 1
            
            # Extract grammatical morphemes using context-sensitive classification
            gloss_parts = gloss.split('-')
            seg_parts = segmentation.replace("'", '').split('-')
            is_final_word = (idx == len(words) - 1)
            
            for i, (seg_part, gloss_part) in enumerate(zip(seg_parts, gloss_parts)):
                position = 'prefix' if i == 0 else ('suffix' if i == len(seg_parts) - 1 else 'stem')
                is_final_morph = (i == len(seg_parts) - 1)
                
                cat_type, cat_sub, is_poly = classify_morpheme_contextual(
                    seg_part, gloss_part, position, 
                    is_final=is_final_morph and is_final_word,
                    full_gloss=gloss
                )
                
                if cat_type == 'grammatical':
                    # Use form+gloss as key to distinguish polysemous uses
                    gm_key = (seg_part.lower(), gloss_part)
                    if gm_key not in gram_morphemes:
                        gram_morphemes[gm_key] = GrammaticalMorpheme(
                            form=seg_part.lower(),
                            gloss=gloss_part,
                            category=cat_sub,
                            is_polysemous=is_poly
                        )
                    gm = gram_morphemes[gm_key]
                    gm.frequency += 1
                    gm.environments.add(position)
                    
                    # Only store examples where the morpheme is in the expected position
                    # and the gloss matches the grammatical function
                    position_valid = (
                        (position == 'prefix' and cat_sub in ('pronominal_prefix', 'directional_prefix', 'reflexive_prefix')) or
                        (position == 'suffix' and cat_sub in ('case_marker', 'tam_suffix', 'nominalizer', 'plural_marker', 'possessive', 'relativizer')) or
                        (position == 'stem' and cat_sub in ('sentence_final', 'quotative', 'auxiliary', 'function_word', 'conjunction'))
                    )
                    if len(gm.example_verses) < 10 and position_valid:
                        gm.example_verses.append((verse_id, tedim_text, kjv_text, segmentation, gloss))
            
            prev_lemma = lemma if pos not in ('FUNC', 'UNK', 'PROP') else prev_lemma
    
    # Post-process: finalize glosses using corpus frequency evidence
    for lemma_key, lem in lemmas.items():
        if lemma_key in collocations:
            lem.collocates = dict(sorted(
                collocations[lemma_key].items(),
                key=lambda x: -x[1]
            )[:20])
        lem.form_count = len(lem.inflected_forms)
        
        # Determine primary gloss using corpus frequency evidence
        _finalize_lemma_gloss(lem)
        
        # Build sense entries from gloss/POS data
        _build_senses(lem)
    
    return tokens, wordforms, lemmas, gram_morphemes

def select_examples(lemmas: Dict[str, LemmaEntry], 
                    gram_morphemes: Dict,
                    target_per_item: int = 5) -> List[ExampleEntry]:
    """
    Select high-quality examples for each lemma and grammatical morpheme.
    
    Selection criteria:
    - shortest: Shortest verse containing the item
    - canonical: Most frequent/typical usage
    - transparent: Clear morphological structure (few affixes)
    - marked: Secondary or less prototypical function
    
    Examples now include segmented and glossed forms.
    """
    examples = []
    
    # Process lemmas
    for lemma, entry in lemmas.items():
        if not entry.example_verses:
            continue
        
        # example_verses format: (verse_id, tedim, kjv, segmented, glossed)
        # Sort by verse length to find shortest
        sorted_by_len = sorted(entry.example_verses, key=lambda x: len(x[1]))
        
        selected = set()
        
        # 1. Shortest clear example
        if sorted_by_len:
            ex = sorted_by_len[0]
            if ex[0] not in selected:
                # ex format: (verse_id, tedim, kjv, segmented, glossed)
                segmented = ex[3] if len(ex) > 3 else ''
                glossed = ex[4] if len(ex) > 4 else ''
                examples.append(ExampleEntry(
                    item_type='lemma',
                    item_id=lemma,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented=segmented,
                    glossed=glossed,
                    kjv_text=ex[2],
                    example_quality='shortest',
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
        
        # Find transparent example (minimal affixation)
        transparent_found = False
        for ex in sorted_by_len:
            if len(selected) >= target_per_item:
                break
            if ex[0] in selected:
                continue
            segmented = ex[3] if len(ex) > 3 else ''
            # Prefer examples with minimal segmentation (fewer hyphens)
            if segmented and segmented.count('-') <= 2:
                glossed = ex[4] if len(ex) > 4 else ''
                examples.append(ExampleEntry(
                    item_type='lemma',
                    item_id=lemma,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented=segmented,
                    glossed=glossed,
                    kjv_text=ex[2],
                    example_quality='transparent',
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
                transparent_found = True
                break
        
        # Fill remaining with canonical/additional examples
        for ex in entry.example_verses:
            if len(selected) >= target_per_item:
                break
            if ex[0] not in selected:
                segmented = ex[3] if len(ex) > 3 else ''
                glossed = ex[4] if len(ex) > 4 else ''
                quality = 'canonical' if len(selected) == 1 else 'additional'
                examples.append(ExampleEntry(
                    item_type='lemma',
                    item_id=lemma,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented=segmented,
                    glossed=glossed,
                    kjv_text=ex[2],
                    example_quality=quality,
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
    
    # Process grammatical morphemes
    for key, entry in gram_morphemes.items():
        if not entry.example_verses:
            continue
        
        # Sort by verse length to find shortest
        sorted_by_len = sorted(entry.example_verses, key=lambda x: len(x[1]))
        selected = set()
        
        for i, ex in enumerate(sorted_by_len[:target_per_item]):
            if ex[0] not in selected:
                quality = 'shortest' if i == 0 else ('canonical' if i == 1 else 'additional')
                segmented = ex[3] if len(ex) > 3 else ''
                glossed = ex[4] if len(ex) > 4 else ''
                examples.append(ExampleEntry(
                    item_type='morpheme',
                    item_id=entry.form,  # Use the form, not the key (form, gloss)
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented=segmented,
                    glossed=glossed,
                    kjv_text=ex[2],
                    example_quality=quality,
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
    
    return examples

def collect_ambiguities(tokens: List[TokenAnalysis], 
                        wordforms: Dict, lemmas: Dict) -> List[Dict]:
    """
    Collect ambiguous analyses into a comprehensive review queue.
    
    Flag items when:
    - Same normalized form maps to multiple segmentations
    - Same normalized form maps to multiple lemmas
    - Same form has both lexical and grammatical analyses
    - Form belongs to known polysemous inventory
    - Form has unstable POS assignment
    - Gloss contains '?' 
    - POS is UNK
    """
    ambiguities = []
    seen = set()
    
    # Track forms with multiple analyses
    form_to_segmentations = defaultdict(set)
    form_to_lemmas = defaultdict(set)
    form_to_pos = defaultdict(set)
    form_to_tokens = defaultdict(list)
    
    for token in tokens:
        nf = token.normalized_form
        form_to_segmentations[nf].add(token.segmentation)
        form_to_lemmas[nf].add(token.lemma)
        form_to_pos[nf].add(token.pos)
        form_to_tokens[nf].append(token)
    
    # Build review queue
    for nf, token_list in form_to_tokens.items():
        if nf in seen:
            continue
        
        review_reasons = []
        first_token = token_list[0]
        freq = len(token_list)
        
        # Check for multiple segmentations
        if len(form_to_segmentations[nf]) > 1:
            review_reasons.append(f'multi_segmentation:{len(form_to_segmentations[nf])}')
        
        # Check for multiple lemmas
        if len(form_to_lemmas[nf]) > 1:
            review_reasons.append(f'multi_lemma:{len(form_to_lemmas[nf])}')
        
        # Check for multiple POS
        if len(form_to_pos[nf]) > 1:
            review_reasons.append(f'multi_pos:{"|".join(sorted(form_to_pos[nf]))}')
        
        # Check for known polysemous forms
        if nf in POLYSEMOUS_FORMS:
            review_reasons.append('known_polysemous')
        
        # Check for unknown
        if first_token.pos == 'UNK':
            review_reasons.append('pos_unknown')
        
        # Check for partial gloss
        if '?' in first_token.gloss:
            review_reasons.append('partial_gloss')
        
        # Check for low confidence
        if first_token.confidence in ('low', 'unknown'):
            review_reasons.append(f'confidence_{first_token.confidence}')
        
        # Add to queue if any issues found
        if review_reasons:
            seen.add(nf)
            ambiguities.append({
                'surface_form': first_token.surface_form,
                'normalized_form': nf,
                'segmentation': first_token.segmentation,
                'alt_segmentations': '|'.join(sorted(form_to_segmentations[nf] - {first_token.segmentation})),
                'gloss': first_token.gloss,
                'lemma': first_token.lemma,
                'alt_lemmas': '|'.join(sorted(form_to_lemmas[nf] - {first_token.lemma})),
                'pos': first_token.pos,
                'alt_pos': '|'.join(sorted(form_to_pos[nf] - {first_token.pos})),
                'confidence': first_token.confidence,
                'first_verse': first_token.verse_id,
                'frequency': freq,
                'review_reasons': '|'.join(review_reasons),
                'status': 'pending_review'
            })
    
    return sorted(ambiguities, key=lambda x: -x['frequency'])

# =============================================================================
# OUTPUT WRITERS
# =============================================================================

def write_verses_tsv(verses: Dict[str, Dict], output_path: str):
    """Write verse-level metadata."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['verse_id', 'book', 'chapter', 'verse', 'tedim_text', 
                        'word_count', 'kjv_text'])
        
        for verse_id in sorted(verses.keys()):
            data = verses[verse_id]
            book = verse_id[:2]
            chapter = verse_id[2:5].lstrip('0')
            verse = verse_id[5:].lstrip('0')
            word_count = len(data['tedim'].split())
            
            writer.writerow([
                verse_id, book, chapter, verse,
                data['tedim'], word_count, data.get('kjv', '')
            ])

def write_tokens_tsv(tokens: List[TokenAnalysis], output_path: str):
    """Write token-level analysis table."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'verse_id', 'token_index', 'surface_form', 'normalized_form',
            'segmentation', 'gloss', 'lemma', 'pos', 'stem_form',
            'stem_alternation', 'prefix_chain', 'suffix_chain',
            'is_proper_noun', 'is_ambiguous', 'confidence', 'kjv_text'
        ])
        
        for token in tokens:
            writer.writerow([
                token.verse_id, token.token_index, token.surface_form,
                token.normalized_form, token.segmentation, token.gloss,
                token.lemma, token.pos, token.stem_form, token.stem_alternation,
                token.prefix_chain, token.suffix_chain,
                '1' if token.is_proper_noun else '0',
                '1' if token.is_ambiguous else '0',
                token.confidence, token.kjv_text
            ])

def write_wordforms_tsv(wordforms: Dict, output_path: str):
    """Write type-level wordform table."""
    # Convert to list and sort by frequency
    wf_list = sorted(wordforms.values(), key=lambda x: -x.frequency)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'surface_form', 'normalized_form', 'lemma', 'segmentation',
            'gloss', 'pos', 'frequency', 'first_verse', 'sample_verses',
            'is_ambiguous', 'status'
        ])
        
        for wf in wf_list:
            writer.writerow([
                wf.surface_form, wf.normalized_form, wf.lemma,
                wf.segmentation, wf.gloss, wf.pos, wf.frequency,
                wf.first_verse, '|'.join(wf.sample_verses[:5]),
                '1' if wf.is_ambiguous else '0', wf.status
            ])

def write_lemmas_tsv(lemmas: Dict[str, LemmaEntry], output_path: str):
    """Write lemma table (dictionary seed)."""
    # Sort by token count
    lem_list = sorted(lemmas.values(), key=lambda x: -x.token_count)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'lemma', 'citation_form', 'pos', 'primary_gloss', 'gloss_candidates',
            'review_gloss_summary', 'english_glosses', 'all_glosses', 'gloss_counts',
            'inflected_forms', 'token_count', 'form_count', 
            'compounds', 'top_collocates', 'example_verses', 
            'is_polysemous', 'is_grammatical', 'needs_review', 'entry_status',
            'polysemy_notes', 'grammaticalization_notes',
            'sense_count', 'pos_variants'
        ])
        
        for lem in lem_list:
            # Format collocates as "word:count" pairs
            colloc_str = '|'.join(f"{k}:{v}" for k, v in list(lem.collocates.items())[:10])
            # Format examples as verse IDs
            ex_str = '|'.join(ex[0] for ex in lem.example_verses[:5])
            # Format gloss counts
            gloss_counts_str = '|'.join(f"{g}:{c}" for g, c in 
                sorted(lem.gloss_counts.items(), key=lambda x: -x[1])[:10])
            # Format POS variants
            pos_var_str = '|'.join(f"{p}:{c}" for p, c in 
                sorted(lem.pos_variants.items(), key=lambda x: -x[1])[:5])
            
            writer.writerow([
                lem.lemma, lem.citation_form, lem.pos,
                lem.primary_gloss,
                '|'.join(lem.gloss_candidates[:5]) if lem.gloss_candidates else '',
                lem.review_gloss_summary,
                '|'.join(sorted(lem.english_glosses)) if lem.english_glosses else '',
                '|'.join(sorted(lem.all_glosses)) if lem.all_glosses else '',
                gloss_counts_str,
                '|'.join(sorted(lem.inflected_forms)[:20]),
                lem.token_count, lem.form_count,
                '|'.join(sorted(lem.compounds)),
                colloc_str, ex_str,
                '1' if lem.is_polysemous else '0',
                '1' if lem.is_grammatical else '0',
                '1' if lem.needs_review else '0',
                lem.entry_status,
                lem.polysemy_notes, lem.grammaticalization_notes,
                len(lem.senses), pos_var_str
            ])


def write_senses_tsv(lemmas: Dict[str, LemmaEntry], output_path: str):
    """Write expanded sense table for dictionary building."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'sense_id', 'lemma', 'sense_num', 'pos', 'gloss', 
            'frequency', 'is_primary', 'is_grammatical',
            'inflected_forms', 'example_verses', 'notes'
        ])
        
        # Sort lemmas by frequency, then output all senses
        for lem in sorted(lemmas.values(), key=lambda x: -x.token_count):
            for i, sense in enumerate(lem.senses):
                ex_str = '|'.join(ex[0] for ex in sense.example_verses[:3])
                forms_str = '|'.join(sorted(sense.inflected_forms)[:10])
                
                writer.writerow([
                    sense.sense_id, lem.lemma, i + 1, sense.pos, sense.gloss,
                    sense.frequency, '1' if sense.is_primary else '0',
                    '1' if sense.is_grammatical else '0',
                    forms_str, ex_str, sense.notes
                ])


def write_grammatical_morphemes_tsv(gram_morphemes: Dict, output_path: str):
    """Write grammatical morphemes table."""
    # Sort by frequency
    gm_list = sorted(gram_morphemes.values(), key=lambda x: -x.frequency)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'form', 'gloss', 'category', 'subcategory', 'frequency', 'environments',
            'example_verses', 'is_polysemous', 'review_reasons', 'status'
        ])
        
        for gm in gm_list:
            ex_str = '|'.join(ex[0] for ex in gm.example_verses[:5])
            
            writer.writerow([
                gm.form, gm.gloss, gm.category, gm.subcategory, gm.frequency,
                '|'.join(sorted(gm.environments)), ex_str,
                '1' if gm.is_polysemous else '0',
                '|'.join(gm.review_reasons) if gm.review_reasons else '',
                gm.status
            ])

def write_examples_tsv(examples: List[ExampleEntry], output_path: str):
    """Write curated examples bank."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'item_type', 'item_id', 'verse_id', 'tedim_text',
            'segmented', 'glossed', 'kjv_text', 'example_quality', 'word_count'
        ])
        
        for ex in examples:
            writer.writerow([
                ex.item_type, ex.item_id, ex.verse_id, ex.tedim_text,
                ex.segmented, ex.glossed, ex.kjv_text, 
                ex.example_quality, ex.word_count
            ])

def write_ambiguities_tsv(ambiguities: List[Dict], output_path: str):
    """Write ambiguity review queue."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'surface_form', 'normalized_form', 'segmentation', 'alt_segmentations',
            'gloss', 'lemma', 'alt_lemmas', 'pos', 'alt_pos', 'confidence',
            'first_verse', 'frequency', 'review_reasons', 'status'
        ])
        
        for amb in ambiguities:
            writer.writerow([
                amb['surface_form'], amb['normalized_form'],
                amb['segmentation'], amb.get('alt_segmentations', ''),
                amb['gloss'], amb.get('lemma', ''), amb.get('alt_lemmas', ''),
                amb['pos'], amb.get('alt_pos', ''), amb['confidence'],
                amb['first_verse'], amb['frequency'],
                amb.get('review_reasons', ''), amb['status']
            ])

def write_coverage_report(tokens: List[TokenAnalysis], wordforms: Dict,
                          lemmas: Dict, gram_morphemes: Dict,
                          ambiguities: List[Dict], output_path: str):
    """Write coverage statistics report."""
    total_tokens = len(tokens)
    
    # More nuanced coverage categories:
    # - fully_analyzed: high/medium confidence AND known POS
    # - needs_review: known POS but has issues (polysemous, multi-analysis)
    # - partial: low confidence (has ?)
    # - unknown: confidence unknown OR POS is UNK
    
    fully_analyzed = sum(1 for t in tokens 
                         if t.confidence in ('high', 'medium') and t.pos != 'UNK')
    needs_review = sum(1 for t in tokens 
                       if t.confidence in ('high', 'medium') and t.pos != 'UNK'
                       and t.normalized_form in POLYSEMOUS_FORMS)
    partial = sum(1 for t in tokens if t.confidence == 'low')
    pos_unknown = sum(1 for t in tokens if t.pos == 'UNK')
    gloss_unknown = sum(1 for t in tokens if t.confidence == 'unknown')
    
    # Effective coverage excludes UNK POS tokens
    effective_analyzed = fully_analyzed - needs_review  # Non-ambiguous fully analyzed
    coverage = 100 * fully_analyzed / total_tokens if total_tokens else 0
    effective_coverage = 100 * effective_analyzed / total_tokens if total_tokens else 0
    
    # POS distribution
    pos_counts = defaultdict(int)
    for t in tokens:
        pos_counts[t.pos] += 1
    
    # Count lemmas needing review
    lemmas_need_review = sum(1 for l in lemmas.values() if l.needs_review)
    lemmas_polysemous = sum(1 for l in lemmas.values() if l.is_polysemous)
    
    report = f"""# Tedim Chin Bible Analysis Coverage Report

Generated: {__import__('datetime').datetime.now().isoformat()}

## Overall Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total tokens | {total_tokens:,} | 100% |
| Fully analyzed (known POS) | {fully_analyzed:,} | {100*fully_analyzed/total_tokens:.2f}% |
| Fully analyzed (non-ambiguous) | {effective_analyzed:,} | {100*effective_analyzed/total_tokens:.2f}% |
| Needs review (polysemous) | {needs_review:,} | {100*needs_review/total_tokens:.2f}% |
| Partial analysis (has ?) | {partial:,} | {100*partial/total_tokens:.2f}% |
| Unknown POS | {pos_unknown:,} | {100*pos_unknown/total_tokens:.2f}% |
| Unknown gloss | {gloss_unknown:,} | {100*gloss_unknown/total_tokens:.4f}% |

**Lexicographic Coverage: {coverage:.2f}%** (tokens with known POS)
**Effective Coverage: {effective_coverage:.2f}%** (excluding ambiguous items)

## Inventory Counts

| Category | Count |
|----------|-------|
| Distinct wordforms | {len(wordforms):,} |
| Lemmas | {len(lemmas):,} |
| Lemmas needing review | {lemmas_need_review:,} |
| Polysemous lemmas | {lemmas_polysemous:,} |
| Grammatical morphemes | {len(gram_morphemes):,} |
| Items in review queue | {len(ambiguities):,} |

## Part of Speech Distribution

| POS | Count | Percentage |
|-----|-------|------------|
"""
    for pos in sorted(pos_counts.keys()):
        count = pos_counts[pos]
        pct = 100 * count / total_tokens
        report += f"| {pos} | {count:,} | {pct:.2f}% |\n"
    
    report += f"""
## Grammatical Morpheme Categories

| Category | Count | Total Frequency |
|----------|-------|-----------------|
"""
    cat_counts = defaultdict(lambda: {'count': 0, 'freq': 0})
    for gm in gram_morphemes.values():
        cat_counts[gm.category]['count'] += 1
        cat_counts[gm.category]['freq'] += gm.frequency
    
    for cat in sorted(cat_counts.keys()):
        data = cat_counts[cat]
        report += f"| {cat} | {data['count']} | {data['freq']:,} |\n"
    
    report += f"""
## Top 20 Lemmas by Frequency

| Lemma | POS | Gloss | Token Count | Form Count |
|-------|-----|-------|-------------|------------|
"""
    top_lemmas = sorted(lemmas.values(), key=lambda x: -x.token_count)[:20]
    for lem in top_lemmas:
        gloss = lem.primary_gloss if lem.primary_gloss else '?'
        report += f"| {lem.lemma} | {lem.pos} | {gloss} | {lem.token_count:,} | {lem.form_count} |\n"
    
    # Summarize review reasons
    reason_counts = defaultdict(int)
    for amb in ambiguities:
        for reason in amb.get('review_reasons', '').split('|'):
            if reason:
                reason_counts[reason.split(':')[0]] += 1
    
    report += f"""
## Ambiguity Summary

- Total items in review queue: {len(ambiguities)}
- Known polysemous forms: {sum(1 for a in ambiguities if 'known_polysemous' in a.get('review_reasons', ''))}
- Multiple segmentations: {reason_counts.get('multi_segmentation', 0)}
- Multiple lemmas: {reason_counts.get('multi_lemma', 0)}
- Multiple POS: {reason_counts.get('multi_pos', 0)}
- Unknown POS: {reason_counts.get('pos_unknown', 0)}
- Partial glosses: {reason_counts.get('partial_gloss', 0)}

### Top 10 Most Frequent Review Items

| Form | Frequency | Review Reasons |
|------|-----------|----------------|
"""
    for amb in ambiguities[:10]:
        reasons = amb.get('review_reasons', 'unknown')
        report += f"| {amb['surface_form']} | {amb['frequency']} | {reasons} |\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Export Tedim Chin Bible analysis for dictionary/grammar work'
    )
    parser.add_argument('--output-dir', default='data/ctd_analysis',
                        help='Output directory for TSV files')
    parser.add_argument('--bible', default='bibles/extracted/ctd/ctd-x-bible.txt',
                        help='Path to Tedim Bible TSV')
    parser.add_argument('--kjv', default='data/verses_aligned.tsv',
                        help='Path to aligned KJV translations')
    args = parser.parse_args()
    
    # Resolve paths relative to repo root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    
    bible_path = os.path.join(repo_root, args.bible)
    kjv_path = os.path.join(repo_root, args.kjv)
    output_dir = os.path.join(repo_root, args.output_dir)
    
    os.makedirs(output_dir, exist_ok=True)
    
    print("Loading Bible data...")
    verses = load_bible_data(bible_path, kjv_path)
    print(f"  Loaded {len(verses):,} verses")
    
    print("Analyzing corpus...")
    tokens, wordforms, lemmas, gram_morphemes = analyze_corpus(verses)
    print(f"  Analyzed {len(tokens):,} tokens")
    print(f"  Found {len(wordforms):,} distinct wordforms")
    print(f"  Found {len(lemmas):,} lemmas")
    print(f"  Found {len(gram_morphemes):,} grammatical morphemes")
    
    print("Selecting examples...")
    examples = select_examples(lemmas, gram_morphemes)
    print(f"  Selected {len(examples):,} examples")
    
    print("Collecting ambiguities...")
    ambiguities = collect_ambiguities(tokens, wordforms, lemmas)
    print(f"  Found {len(ambiguities):,} ambiguous forms")
    
    print("Writing output files...")
    
    write_verses_tsv(verses, os.path.join(output_dir, 'verses.tsv'))
    print(f"  Written: verses.tsv")
    
    write_tokens_tsv(tokens, os.path.join(output_dir, 'tokens.tsv'))
    print(f"  Written: tokens.tsv")
    
    write_wordforms_tsv(wordforms, os.path.join(output_dir, 'wordforms.tsv'))
    print(f"  Written: wordforms.tsv")
    
    write_lemmas_tsv(lemmas, os.path.join(output_dir, 'lemmas.tsv'))
    print(f"  Written: lemmas.tsv")
    
    write_senses_tsv(lemmas, os.path.join(output_dir, 'senses.tsv'))
    print(f"  Written: senses.tsv")
    
    write_grammatical_morphemes_tsv(gram_morphemes, 
                                     os.path.join(output_dir, 'grammatical_morphemes.tsv'))
    print(f"  Written: grammatical_morphemes.tsv")
    
    write_examples_tsv(examples, os.path.join(output_dir, 'examples.tsv'))
    print(f"  Written: examples.tsv")
    
    write_ambiguities_tsv(ambiguities, os.path.join(output_dir, 'ambiguities.tsv'))
    print(f"  Written: ambiguities.tsv")
    
    write_coverage_report(tokens, wordforms, lemmas, gram_morphemes, ambiguities,
                          os.path.join(output_dir, 'coverage_report.md'))
    print(f"  Written: coverage_report.md")
    
    print("\nDone!")
    print(f"Output directory: {output_dir}")

if __name__ == '__main__':
    main()
