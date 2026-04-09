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

# Import refactored morphology module
from morphology import (
    OPAQUE_LEXEMES,
    PREFIXES,
    DERIVATIONAL_SUFFIXES,
    INFLECTIONAL_SUFFIXES,
)
from morphology.opaque import is_opaque, get_opaque_gloss
from morphology.affixes import is_prefix, is_suffix, validate_suffix_sequence, get_suffix_order
from morphology.compounds import COMPOUND_WORDS

# =============================================================================
# PHONOTACTIC CONSTRAINTS
# =============================================================================
#
# Tedim Chin has strict phonotactic constraints on word/morpheme onsets.
# These constraints prevent impossible segmentations like *hto, *kp, etc.
#
# Based on corpus analysis (831,431 tokens):
# - No true consonant clusters in native words
# - Aspirates (kh, th, ph) and velar nasal (ng) are single phonemes
# - Only foreign words (loanwords, proper nouns) violate these constraints
#
# =============================================================================

# Valid word/morpheme-initial consonant patterns
# These are the ONLY valid onsets for native Tedim morphemes
VALID_ONSETS = frozenset({
    # Single consonants
    'b', 'c', 'd', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 's', 't', 'v', 'z',
    # Aspirates (single phonemes, written as digraphs)
    'kh', 'th', 'ph',
    # Velar nasal (single phoneme)
    'ng',
    # Vowel-initial (empty onset)
    '',
})

# Vowels for onset extraction
VOWELS = frozenset('aeiou')


def get_onset(morpheme: str) -> str:
    """
    Extract the onset (initial consonant cluster) from a morpheme.
    
    Args:
        morpheme: A morpheme string
        
    Returns:
        The onset consonants, or '' for vowel-initial morphemes
        
    Examples:
        >>> get_onset('khua')
        'kh'
        >>> get_onset('thu')
        'th'
        >>> get_onset('om')
        ''
        >>> get_onset('pa')
        'p'
        >>> get_onset('ngai')
        'ng'
    """
    if not morpheme:
        return ''
    
    # Check for aspirates/ng first (2-char onsets)
    if len(morpheme) >= 2:
        digraph = morpheme[:2]
        if digraph in {'kh', 'th', 'ph', 'ng'}:
            return digraph
    
    # Single consonant or vowel
    if morpheme[0] in VOWELS:
        return ''
    
    # Return all initial consonants (for detecting invalid clusters)
    i = 0
    while i < len(morpheme) and morpheme[i] not in VOWELS:
        i += 1
    return morpheme[:i]


def is_valid_onset(morpheme: str) -> bool:
    """
    Check if a morpheme has a phonotactically valid onset.
    
    This validates that the morpheme begins with a legal Tedim Chin
    consonant pattern. Invalid onsets indicate a segmentation error.
    
    Args:
        morpheme: A morpheme string to validate
        
    Returns:
        True if the onset is valid, False otherwise
        
    Examples:
        >>> is_valid_onset('khua')   # kh is valid aspirate
        True
        >>> is_valid_onset('hto')    # *ht cluster is invalid
        False
        >>> is_valid_onset('om')     # vowel-initial is valid
        True
        >>> is_valid_onset('ngai')   # ng is valid
        True
        >>> is_valid_onset('pta')    # *pt cluster is invalid
        False
    """
    onset = get_onset(morpheme)
    return onset in VALID_ONSETS


def validate_segmentation(segments: List[str]) -> Tuple[bool, Optional[str]]:
    """
    Validate that all morphemes in a segmentation have valid onsets.
    
    Args:
        segments: List of morpheme strings
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if all segments have valid onsets
        - error_message: Description of the first invalid segment, or None
        
    Examples:
        >>> validate_segmentation(['ka', 'pai'])
        (True, None)
        >>> validate_segmentation(['ka', 'hto'])
        (False, "Invalid onset 'ht' in morpheme 'hto'")
    """
    for seg in segments:
        # Skip empty segments and punctuation
        if not seg or not seg[0].isalpha():
            continue
        # Use lowercase for phonotactic check (case doesn't affect phonology)
        if not is_valid_onset(seg.lower()):
            onset = get_onset(seg.lower())
            return (False, f"Invalid onset '{onset}' in morpheme '{seg}'")
    return (True, None)


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

# =============================================================================
# PRONOMINAL CONCORD (Henderson 1965, pp. 32-33)
# =============================================================================
#
# Henderson describes pronominal concord between nominal subjects and verbal
# prefixes. This helps disambiguate phrase structure:
#
# Concordant pairs (nominal → prefix):
#   - kei, keimah (I, myself) → ka-
#   - nang, nangmah (you.SG, yourself) → na-
#   - amah, ama (he/she/it) → a-
#   - ei, eite (we.INCL) → i-
#   - ko, kote (we.EXCL) → ka-
#   - no, note (you.PL) → na-
#   - Most other nouns (3rd person) → a-
#
# Key insight: Pronominal concord distinguishes SUBJECTIVE from ADJUNCTIVE
# phrases. Subjective phrases have concord; adjunctive phrases do NOT.
#
# Example: "Dahpa in lo a kuan nuam kei a"
#   - "Dahpa" (subject) concords with "a" prefix in "a kuan"
#   - "lo" (field) does NOT concord - it's in an adjunctive phrase
#
# =============================================================================

PRONOMINAL_CONCORD = {
    # Pronoun/noun → expected prefix for concord
    'kei': 'ka',        # 1SG
    'keimah': 'ka',     # 1SG emphatic
    'nang': 'na',       # 2SG
    'nangmah': 'na',    # 2SG emphatic
    'amah': 'a',        # 3SG
    'ama': 'a',         # 3SG (short form)
    'ei': 'i',          # 1PL.INCL
    'eite': 'i',        # 1PL.INCL
    'ko': 'ka',         # 1PL.EXCL
    'kote': 'ka',       # 1PL.EXCL
    'no': 'na',         # 2PL
    'note': 'na',       # 2PL
    # Default for other nouns (3rd person)
    '_default': 'a',
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
    'a': 'LOC',       # Locative (short form)
    'tawh': 'COM',    # Comitative "with"
    'pan': 'ABL',     # Ablative "from"
    # panin: handled as pan-in (ABL-ERG) via suffix stripping
}

# =============================================================================
# VP SLOT CATEGORIES
# =============================================================================
# The verbal template is: VERB-(DERIV)-(ASPECT)-(DIR)-(MODAL)
# Each slot has its own dictionary for clear categorization

# ASPECT SUFFIXES - mark viewpoint/completion of event
ASPECT_SUFFIXES = {
    'ta': 'PFV',        # Perfective (completed action)
    'zo': 'COMPL',      # Completive (able to complete)
    'kik': 'ITER',      # Iterative (again)
    'nawn': 'CONT',     # Continuative (still doing)
    'khin': 'IMM',      # Immediate (already/just)
    'mang': 'COMPL',    # Completive (completely)
    'kim': 'fully',     # Completive (fully)
    'zawh': 'finish',   # Completive (finish V-ing)
    'khit': 'COMPL',    # Sequential/completive
    'to': 'CONT',       # Continuative
    'zel': 'HAB.CONT',  # Habitual continuative (ZNC §6.6.2.3) - continuing to do
    'gige': 'HAB',      # Habitual (ZNC §6.6.2.3) - always does
}

# DIRECTIONAL SUFFIXES - indicate path/direction of motion
# ZNC (2018) §5.8.2.3 documents 3-way elevational system: -toh UP, -suk DOWN, -phei HORIZ
DIRECTIONAL_SUFFIXES = {
    'khia': 'out',      # Outward motion
    'khiat': 'away',    # Away from
    'lut': 'in',        # Inward motion
    'toh': 'UP',        # Upward motion (elevational) - ZNC: -tɔù
    'suk': 'DOWN',      # Downward motion (elevational) - ZNC: -sùk (was missing)
    'phei': 'HORIZ',    # Horizontal/level motion - ZNC: -pʰeī (was missing)
    'cip': 'down',      # Downward/tightly (questionable - may be lexical)
    'tang': 'arrive',   # Arrival at endpoint (questionable - may be lexical)
    'sawn': 'toward',   # Motion toward (questionable - may be lexical)
    'lam': 'TOWARD',    # Goal directional - ZNC: -lám
}

# MODAL SUFFIXES - express modality (possibility, necessity, volition)
MODAL_SUFFIXES = {
    'ding': 'IRR',      # Irrealis/future
    'thei': 'ABIL',     # Abilitative (can/able)
    'theih': 'ABIL',    # Abilitative Form II
    'nuam': 'want',     # Desiderative (want to)
    'nop': 'want',      # Desiderative variant
    'pah': 'NEG.ABIL',  # Negative ability
    'pak': 'NEG.ABIL',  # Unable variant
    'lawh': 'NEG.ABIL', # Unable
    'kul': 'must',      # Deontic necessity
    'lai': 'PROSP',     # Prospective (about to)
    'mawk': 'perhaps',  # Dubitative
    'ngei': 'EXP',      # Experiential (have done before)
}

# DERIVATIONAL SUFFIXES - change valency or add semantic content
DERIVATIONAL_SUFFIXES = {
    'sak': 'CAUS',      # Causative (Form I) / Benefactive (Form II)
    # NOTE: -suk is DIRECTIONAL (DOWN), not causative - see DIRECTIONAL_SUFFIXES
    'pih': 'APPL',      # Applicative (benefactive)
    'khawm': 'COM',     # Comitative (together)
    'gawp': 'INTENS',   # Intensive (forcefully)
    'nasa': 'INTENS',   # Intensive (strongly)
    'zah': 'fear',      # Fear/respect
    'hak': 'INTENS',    # Intensive variant
    'tawm': 'DIMIN',    # Diminutive (a bit)
    'khak': 'RES',      # Resultative
    'zaw': 'MORE',      # Comparative
    'lua': 'too',       # Excessive
    'tel': 'each',      # Distributive
    'khop': 'together', # Collective
    'loh': 'NEG',       # Negative result
    'suak': 'become',   # Inchoative
}

# Legacy TAM_SUFFIXES kept for backward compatibility
TAM_SUFFIXES = {
    # Tense/Aspect markers
    'ding': 'IRR',    # Irrealis
    'ta': 'PFV',        # Perfective (completed action)
    'zo': 'COMPL',      # Completive (able to complete)
    'kik': 'ITER',      # Iterative (again)
    'nawn': 'CONT',     # Continuative
    'khin': 'IMM',      # Immediate/intensifier
    'sa': 'PAST',       # Past tense
    # Directional/motion suffixes (aspectual) - ZNC §5.8.2.3
    'khia': 'out',      # Directional out
    'khiat': 'away',    # Directional away
    'lut': 'in',        # Directional in
    'toh': 'UP',        # Upward (elevational) - ZNC: -tɔù
    'suk': 'DOWN',      # Downward (elevational) - ZNC: -sùk
    'phei': 'HORIZ',    # Horizontal/level - ZNC: -pʰeī
    'to': 'CONT',       # Continuative
    'cip': 'tightly',   # Intensifier (firmly/tightly)
    # Habitual markers - ZNC §6.6.2.3
    'zel': 'HAB.CONT',  # Habitual continuative (continuing to do)
    'gige': 'HAB',      # Habitual (always does)
    # Other aspect markers
    'mang': 'COMPL',    # Completive (completely)
    'kim': 'fully',     # Completive (fully)
    'san': 'at',        # Locative relation
    'sim': 'ITER',      # Iterative variant
    'lam': 'TOWARD',    # Goal directional - ZNC: -lám
    'zia': 'manner',    # Manner nominal
    'sakin': 'CAUS.ERG', # Causative + ergative
    'sakkik': 'CAUS.ITER', # Causative + iterative
    'sakzo': 'CAUS.COMPL', # Causative + completive
    # Temporal/boundary markers
    'teng': 'until',    # Temporal boundary
    'kha': 'still',     # Persistive (still/yet)
    'zawh': 'finish',   # Completive (finish V-ing)
}

# Derivational suffixes (change verb meaning/valency)
VERBAL_DERIVATIONAL_SUFFIXES = {
    'sak': 'CAUS',      # Causative (Form I) / Benefactive (Form II) - see STEM_DEPENDENT_GLOSSES
    'pih': 'APPL',      # Applicative (with/for) - Form II only
    'khawm': 'COM',     # Comitative (together)
    'gawp': 'INTENS',   # Intensive (forcefully)
    'thei': 'ABIL',     # Abilitative (can/able)
    'theih': 'ABIL',    # Abilitative Form II variant
    'nuam': 'want',     # Desiderative (want to)
    'nop': 'want',      # Desiderative variant
    'pah': 'NEG.ABIL',  # Negative ability (cannot)
    'pak': 'NEG.ABIL',  # Unable (variant)
    'lawh': 'NEG.ABIL', # Unable
    'tawm': 'DIMIN',    # Diminutive (a bit)
    'khak': 'RES',      # Resultative
    'khit': 'COMPL',    # Completive variant
    'zaw': 'MORE',      # Comparative (more)
    'lua': 'too',       # Excessive (too much)
    'mawk': 'perhaps',  # Dubitative
    'lai': 'middle',    # Temporal middle (while V-ing)
    'takin': 'really',  # Emphatic adverbializer
    'nasa': 'INTENS',   # Intensive (strongly)
    'zah': 'INTENS',    # Intensive (greatly/fear)
    'sawn': 'toward',   # Directional toward
    'thuah': 'always',  # Habitual (repeatedly)
    'tel': 'each',      # Distributive (each/every)
    'khop': 'together', # Collective
    'hak': 'INTENS',    # Intensive variant
    'loh': 'NEG',       # Negative result
    'pi': 'AUG',        # Augmentative (big/great) - NOT comparative; see -zaw for true comparative
    'pa': 'NMLZ.AG',    # Agent nominalizer (one who V-s)
    'ngei': 'EXP',      # Experiential (have V-ed before, know how to V)
}

# Combined strippable suffixes for morphological analysis
# This combines TAM, derivational, and case suffixes for unified suffix stripping
STRIPPABLE_SUFFIXES = {**TAM_SUFFIXES, **VERBAL_DERIVATIONAL_SUFFIXES, **CASE_MARKERS}

# Additional suffixes that can appear in verbal complexes
ADDITIONAL_VERBAL_SUFFIXES = {
    'khap': 'forbid',   # Prohibitive
    'suak': 'become',   # Inchoative (become)
    'sung': 'inside',   # Locative (within)
    # nin: removed - NOT an ERG variant; words ending in -nin parsed differently
    'min': 'ERG',       # Ergative variant
    'nateng': 'NMLZ.until', # Nominalized + until
    'kikin': 'ITER.ERG',    # Iterative + ergative
    'neu': 'small',     # Diminutive
    'luat': 'exceed',   # Excessive
    'bawl': 'do',       # Light verb (do/make)
    'zang': 'use',      # Instrumental
    # Round 154 additions - second batch
    'tat': 'COMPL',     # Completive (completely)
    'siang': 'well',    # Manner (properly/well)
    'kawm': 'nearly',   # Approximative
    'phat': 'EMPH',     # Emphatic/intensive
    'zawk': 'MORE',     # Comparative variant
    'hawm': 'together', # Collective
    'bu': 'group',      # Collective/group
    'sawm': 'ten',      # Numeric (also: attempt)
    'huai': 'CAUS',     # Causative variant
    'beng': 'straight', # Adverbializer (directly)
    'dang': 'other',    # Other/different
    'sia': 'bad',       # Deteriorative (wrongly)
    'lan': 'appear',    # Evidential
    'pha': 'good',      # Evaluative (well)
    'lah': 'ADV',       # Adverbializer
    'ha': 'PL',         # Plural variant (archaic)
    'kin': 'quickly',   # Manner (quickly)
    # Round 154 additions - third batch
    'siat': 'spoil',    # Destructive
    'zawl': 'easy',     # Evaluative (easily)
    'khai': 'INSTR',    # Instrumental
    'vat': 'suddenly',  # Sudden/quick
    'kholh': 'INTENS',  # Intensive (denounce)
    'thang': 'spread',  # Extent (spread out)
    'dai': 'quiet',     # Manner (quietly)
    'sun': 'during',    # Temporal (during)
    'aimang': 'COMPL',  # Completive (all gone)
    'nai': 'near',      # Proximity
    'tak': 'truly',     # Emphatic
    'pen': 'TOP',       # Topic (already in FUNCTION_WORDS but also suffix)
    # Round 154 additions - fourth batch
    'lo': 'NEG',        # Negative
    'kip': 'keep',      # Keep/maintain (thukip = keep word)
    'lian': 'great',    # Augmentative (greatly)
    'mai': 'only',      # Restrictive
    'ham': 'also',      # Additive
    'am': 'also',       # Additive variant
    'no': 'young',      # Diminutive
    'kak': 'INTENS',    # Intensive
    # Round 154 additions - fifth batch
    'tuam': 'different', # Manner (differently)
    'dak': 'suddenly',   # Manner (suddenly) - variant of vat
    'khem': 'all',       # Totality (all/completely)
    'ang': 'like',       # Similative (like/as)
    'nu': 'female',      # Gender marker
    'na': 'NMLZ',        # Nominalizer (also in NOMINALIZERS)
}

# NOTE: 'te'' (PL.POSS) handled separately in possessive section

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

# =============================================================================
# WORD CLASSES FOR NP STRUCTURE
# =============================================================================
# These dictionaries organize words by part of speech for NP chunking and
# structural analysis. Each category is used by the NP structure report.

# Demonstratives (prenominal)
DEMONSTRATIVES = {
    'hih': 'PROX',      # this (4,025x)
    'tua': 'DIST',      # that (9,156x)
    'tuate': 'DIST.PL', # those
    'hihte': 'PROX.PL', # these
}

# Numerals (post-nominal, directly follow nouns - no classifiers)
NUMERALS = {
    'khat': 'one',       # 4,303x - mi khat = one person
    'nih': 'two',        # 598x
    'thum': 'three',     # 626x
    'li': 'four',
    'nga': 'five',
    'guk': 'six',
    'sagih': 'seven',
    'giat': 'eight',
    'kua': 'nine',
    'sawm': 'ten',       # 679x
    'za': 'hundred',
    'tul': 'thousand',
}

# Quantifiers (post-nominal, follow NP)
QUANTIFIERS = {
    'khempeuh': 'all',      # 4,783x - mi khempeuh = all people
    'peuhpeuh': 'every',    # 431x - mi peuhpeuh = every person  
    'tampi': 'many',        # 727x - mi tampi = many people
    'teltel': 'each',       # teltel-in = each in turn
    'vekpi': 'altogether',  # 213x - all together
    'tuamtuam': 'various',  # 59x - different kinds
    'khatpeuh': 'any',      # 79x - mi khatpeuh = anyone
    'pawlkhat': 'some',     # 394x - some (of them)
}

# Property words (stative verbs that can be attributive or predicative)
# Predicative: a hoih = it is good (3SG + property)
# Attributive: mi hoih = good person (N + property)
PROPERTY_WORDS = {
    'hoih': 'good',         # 170x predicative, 30x attributive
    'sia': 'evil',          # 163x predicative - a sia = it is evil
    'lian': 'big',          # 124x - a lian = it is big
    'neu': 'small',         # 39x - a neu = it is small
    'gim': 'suffering',     # 57x - a gim = suffering
    'tha': 'strong',        # 24x - a tha = it is strong
    'ha': 'difficult',      # 12x - a ha = it is difficult
    'nuam': 'pleasant',     # 21x - a nuam = it is pleasant
    'tam': 'many',          # 54x - a tam = they are many
    'tawm': 'few',          # 12x - a tawm = they are few
    'sau': 'long',          # 22x - a sau = it is long
    'toih': 'short',        # rare
    'dau': 'deep',          # 5x - a dau = it is deep
    'bel': 'wide',          # 7x - a bel = it is wide
    'man': 'expensive',     # 18x attributive - thu man = valuable word
    'mang': 'obedient',     # 35x - thu mang = obey (word + obey)
    'om': 'exist',          # 1868x - a om = it exists (also PROPERTY_WORDS for attributive use)
    'pha': 'good',          # 221x - a pha = it is good (quality)
    'thei': 'able',         # 176x - a thei = able to (modal use)
    # Additional property words from corpus analysis
    'taang': 'beautiful',   # a taang = it is beautiful
    'bal': 'tired',         # a bal = tired/weary
    'lat': 'strong',        # a lat = strong
    'sawt': 'long.time',    # a sawt = long time
    'ko': 'long',           # a ko = long (time/space)
    'kibang': 'like',       # kibang = same/like
}

# Coordinator (single morpheme in Tedim Chin)
COORDINATOR = {
    'le': 'and',            # 10,942x - N le N = N and N
}

# Adverbs (manner, degree, time modifiers)
ADVERBS = {
    # Manner adverbs
    'takin': 'truly',       # intensifier "really/truly"
    'tak': 'truly',         # intensifier base
    'hawm': 'together',     # "together/jointly"
    'kawi': 'forth',        # directional "forth"
    'langpang': 'against',  # adversative (also in RELATOR_NOUNS)
    'dai': 'still',         # "still/silent"
    'nail': 'always',       # "always/continuously"
    'mawk': 'perhaps',      # epistemic "perhaps/maybe"
    'nai': 'still',         # "still/yet/near"
    'ngei': 'ever',         # experiential "ever/never" (with NEG)
    # Degree adverbs
    'tham': 'very',         # degree intensifier
    'bek': 'only',          # restrictive
    'zong': 'also',         # additive
}

# Temporal connectives (clause-linking temporal words)
# Note: ciangin/hangin/bangin are SUBORDINATORS - check SUBORDINATORS dict
# Note: tua is a DEMONSTRATIVE - check DEMONSTRATIVES dict
TEMPORAL_CONNECTIVES = {
    'ciang': 'then',        # "then/when" - base form (not ciangin which is subordinator)
    'tu': 'now',            # "now"
    'tuni': 'today',        # "today"
    'zingsang': 'tomorrow', # "tomorrow"
    'nitak': 'yesterday',   # "yesterday"
}

# Expanded quantifiers
QUANTIFIERS_EXTENDED = {
    'ciat': 'each',         # distributive "each/every"
    'gawp': 'all',          # "all/entire"
    'peuh': 'every',        # "every/any"
    'kip': 'firm',          # "firm/all" (intensive)
    'ma': 'alone',          # "alone/only"
    'tam': 'many',          # "many" - quantifier sense (also in PROPERTY_WORDS)
}

# Nominalizers and plurals
NOMINALIZERS = {
    'mi': 'NMLZ.AG',  # Agent nominalizer
    'na': 'NMLZ',     # Nominalizer suffix
    'te': 'PL',       # Noun plural
    'uh': '2/3PL',    # 2nd/3rd person plural agreement clitic (separate word)
}

# =============================================================================
# AMBIGUOUS MORPHEMES - Contextual Disambiguation System
# =============================================================================
#
# PURPOSE:
# This system handles morphemes with multiple meanings (polysemy) by selecting
# the contextually appropriate gloss. Without this, single-gloss dictionaries
# would assign incorrect meanings to common words.
#
# ARCHITECTURE:
# 1. AMBIGUOUS_MORPHEMES dict: Lists all meanings for each polysemous morpheme
#    Format: morpheme -> [(meaning1, context_desc), (meaning2, context_desc), ...]
#
# 2. disambiguate_morpheme() function: Applies contextual rules to select meaning
#    Uses context dict with keys: position, prev_morpheme, next_morpheme,
#    has_prefix, has_suffix, has_ki_prefix, in_compound
#
# INTEGRATION:
# - For standalone words: Called in analyze_word() before FUNCTION_WORDS lookup
# - For morphemes in compounds: Called when stripping prefixes/suffixes
# - Context is built from the morphological analysis state
#
# ADDING NEW AMBIGUOUS MORPHEMES:
# 1. Add entry to AMBIGUOUS_MORPHEMES with all meanings
# 2. Add elif branch in disambiguate_morpheme() with rules
# 3. Rules should prioritize corpus frequency and grammatical context
# 4. Always include a sensible default (most common meaning)
#
# EXAMPLES:
# - za: 'hear' (verb, 283x) vs 'hundred' (numeral, 73x)
#   Rule: 'hundred' after kum/sawm, 'hear' otherwise
# - vei: 'sick' (standalone) vs 'wave' (with suffix) vs 'time' (after numeral)
#   Rule: context-dependent selection
#
# =============================================================================

AMBIGUOUS_MORPHEMES = {
    # za: 'hear' (verb) vs 'hundred' (number)
    # - 'hundred' when following kum/sawm or before tul, or standalone in number context
    # - 'hear' when with verbal morphology (prefixes ka/na/a, suffixes -te/-na/-in)
    'za': [
        ('hear', 'verbal'),      # Primary: with verbal morphology
        ('hundred', 'numeral'),  # After kum/sawm, before tul
    ],
    
    # la: 'take' (verb) vs 'and' (sequential conjunction) vs 'donkey' (noun)
    # - 'take' most common (la-in = taking, amah la = took him)
    # - 'and' after imperatives (hen la = let... and)
    # - 'donkey' rare (late = donkeys)
    'la': [
        ('take', 'verbal'),      # Primary: with verbal morphology
        ('and.SEQ', 'after_imperative'),  # After hen (imperative)
        ('donkey', 'nominal'),   # As noun (rare)
    ],
    
    # na: '2SG' (pronoun) vs 'NMLZ' (nominalizer suffix)
    # - '2SG' when standalone or as prefix
    # - 'NMLZ' when suffix on verbs (verb-na)
    'na': [
        ('2SG', 'standalone'),   # Standalone word
        ('NMLZ', 'suffix'),      # As suffix on verbs
    ],
    
    # pa: 'father' (noun) vs 'NMLZ.AG' (agentive nominalizer)
    # - 'father' standalone or with possessive (ka pa = my father)
    # - 'NMLZ.AG' as suffix creating agent nouns (verb-pa = one who verbs)
    'pa': [
        ('male', 'standalone'),  # Standalone noun: male/son/father (kinship term)
        ('NMLZ.AG', 'suffix'),   # Agentive nominalizer
    ],
    
    # man: 'finish' vs 'reason' vs 'catch/take' vs 'price'
    # - 'finish' in "a man khit" = finished
    # - 'reason' in "ahih manin" = therefore (frozen form)
    # - 'catch' in "amah man" = caught him
    # - 'price' in "a man" = its price
    'man': [
        ('finish', 'with_khit'),   # a man khit = finished
        ('catch', 'verbal'),       # with verbal morphology
        ('reason', 'in_manin'),    # frozen in manin
        ('price', 'nominal'),      # as noun
    ],
    
    # hang: 'reason' vs 'mighty/stallion'
    # - 'reason' in "bang hang hiam" = why (99% of occurrences)
    # - 'mighty' rare, possibly not in Bible text
    'hang': [
        ('reason', 'default'),     # Default meaning
        ('mighty', 'rare'),        # Rare meaning
    ],
    
    # vei: 'time/instance' vs 'sick/faint'
    # - 'time' in khatvei = once, nihvei = twice
    # - 'sick/faint' in phukhong vei = faint from hunger
    'vei': [
        ('time', 'with_numeral'),  # After numerals (sagih vei = seven times)
        ('wave', 'with_verb_morphology'),  # Wave offering (vei-a piak = wave-LOC give)
        ('sick', 'standalone'),    # Standalone or with illness words
    ],
    'pha': [
        ('good', 'as_suffix'),     # Evaluative suffix (thu-pha = word-good = blessing)
        ('branch', 'standalone'),  # Noun: branch/limb
    ],
    'kham': [
        ('gold', 'standalone'),    # Noun: gold (ngun le kham = silver and gold)
        ('forbid', 'with_ki'),     # Verb: forbid (ki-kham = REFL-forbid)
    ],
    
    # hi: 'be' (copula) vs 'DECL' (sentence-final particle)
    # Henderson 1965: hi is declarative particle sentence-finally
    # As copula when preceded by subject prefix (ka-hi, a-hi)
    'hi': [
        ('DECL', 'sentence_final'),  # Sentence-final declarative particle
        ('be', 'with_prefix'),       # Copula with pronominal prefix
    ],
    
    # hih: 'this' (proximal demonstrative) vs Form II of 'hi' (be)
    # Henderson: hih as Form II appears in inconclusive sentences/before predicates
    # - 'this' when modifying nouns (hih pa = this person)
    # - 'be.II' in manner clauses (a hih bangin = as it being)
    'hih': [
        ('this', 'before_noun'),     # Proximal demonstrative (hih pa, hih thu)
        ('be.II', 'in_clause'),      # Form II of hi in subordinate clauses
    ],
    
    # tu: 'now' (temporal) vs 'sit' (verb)
    # - 'now' in tu-in = now-ERG (temporal adverb)
    # - 'sit' as verb stem (tu-a = sit-LOC = sitting)
    'tu': [
        ('now', 'temporal'),         # Temporal adverb (most common)
        ('sit', 'verbal'),           # Sit (less common)
    ],
    
    # tuh: 'sow' vs Form II of 'tu' (sit)
    # Henderson: tuh is Form II of tu, but also lexicalized as 'sow'
    # - 'sow' in agricultural contexts (khai tuh = plant seed)
    # - 'sit.II' rare (would be subordinate clause with sitting)
    'tuh': [
        ('sow', 'agricultural'),     # Sow/plant (primary meaning in Bible)
        ('sit.II', 'rare'),          # Form II of tu (rare)
    ],
    
    # kah: 'climb/ascend' vs 'fight' vs 'cry'
    # - 'climb' in motion contexts (kah-to = climb-up = ascend)
    # - 'fight' in conflict contexts (kah-na = fight-NMLZ)  
    # - 'cry/weep' (kap variant?)
    'kah': [
        ('climb', 'motion'),         # Climb/ascend (kah-to = ascend)
        ('fight', 'conflict'),       # Fight
    ],
    
    # sa: 'flesh' (noun) vs 'PERF' (perfective suffix on verbs)
    # - 'flesh' standalone or with nominal morphology
    # - 'PERF' after verb stems (muh-sa = seen, nei-sa = had)
    'sa': [
        ('flesh', 'nominal'),        # Noun: flesh, meat, wild game
        ('PERF', 'after_verb'),      # Perfective aspect after verbs
    ],
    
    # ta: 'child' (noun) vs 'PFV' (perfective aspect)
    # - 'child' in compounds (ta-pa = son, ta-nu = daughter), after possessive (a ta)
    # - 'PFV' after verbs when followed by sentence-final (ta hen, ta hi, ta uh)
    'ta': [
        ('child', 'nominal'),        # Noun: child, offspring
        ('PFV', 'after_verb'),       # Perfective aspect marker
    ],
    
    # thei: 'know' (verb) vs 'ABIL' (abilitative suffix) vs 'fig' (noun)
    # - 'know' when main verb with pronominal prefix (ka thei, na thei, a thei)
    # - 'ABIL' when follows another verb (mu thei = can see, ne thei = can eat)
    # - 'fig' in theigah (fig tree) - rare
    'thei': [
        ('know', 'main_verb'),       # Main verb: know
        ('ABIL', 'after_verb'),      # Abilitative: can/able
        ('fig', 'in_compound'),      # Noun: fig (rare)
    ],
    
    # tung: 'on/upon' (relational noun) vs 'arrive' (verb)
    # - 'on' when followed by -ah (tung-ah = on-LOC)
    # - 'arrive' with verbal morphology
    'tung': [
        ('on', 'with_ah'),           # Relational noun + LOC
        ('arrive', 'verbal'),        # Motion verb
    ],
    
    # === Henderson 1965: Form I/II Disambiguation ===
    # Verbs have two forms: Form I (indicative, sentence-final) and 
    # Form II (subjunctive, in adjunctive phrases/non-final predicates)
    # The following entries help disambiguate these patterns
    
    # sung: 'inside' (relational noun) vs 'high' (adjective)
    # - 'inside' with -ah (sung-ah = inside-LOC, a sungah = in it)
    # - 'high' less common in Bible
    'sung': [
        ('inside', 'relational'),    # Relational noun (default)
        ('high', 'adjective'),       # Rare adjective use
    ],
    
    # kiang: 'beside/near' (relational noun) vs 'separate' (verb)
    # - 'beside' with -ah (kiang-ah = beside-LOC)
    'kiang': [
        ('beside', 'relational'),    # Relational noun (default)
        ('separate', 'verbal'),      # Verb: separate/be.different
    ],
    
    # lak: 'among/middle' (relational noun)
    # - 'among' with -ah (lak-ah = among-LOC)
    'lak': [
        ('among', 'relational'),     # Relational noun (default)
    ],
    
    # mai: 'face/front' (relational noun) vs 'end/edge' (noun)
    # - 'face' most common, 'front' with -ah
    'mai': [
        ('face', 'nominal'),         # Body part / front
        ('front', 'relational'),     # Relational: in front of
    ],
    
    # nuai: 'below/under' (relational noun)
    'nuai': [
        ('below', 'relational'),     # Relational noun
    ],
    
    # lam: 'road/way/side' (noun) vs 'manner' (nominalizer) vs 'build' (verb) vs 'dance' (verb)
    # CRITICAL: Four distinct homophonous roots
    # - lam1: road/way/path (noun) - lampi, lamzin, lamkaih, lamliante
    # - lam2: build (verb) - lamkik "rebuild", lamkikna "rebuilding"  
    # - lam3: dance (verb) - lamna "dancing"
    # - lam4: manner nominalizer (with verbs) - V-lam = way of V-ing
    'lam': [
        ('way', 'nominal'),          # Noun: road, path, way
        ('side', 'relational'),      # Relational: that side
        ('build', 'before_kik'),     # Verb: build (only before -kik)
        ('dance', 'before_na'),      # Verb: dance (only before -na)
        ('manner', 'with_verb'),     # Manner nominalizer after verbs
    ],
    
    # zo: 'able/finish' (completive) vs 'south' (direction) vs ethnic 'Zo'
    'zo': [
        ('COMPL', 'after_verb'),     # Completive aspect (can complete)
        ('south', 'directional'),    # Direction (rare)
    ],
    
    # in: 'ERG' (ergative case) vs 'house' vs 'QUOT' (quotative) vs 'CVB' (converb)
    # - 'ERG' as suffix on NPs (marks transitive agent)
    # - 'CVB' as suffix on verbs (same-subject sequential, "having VERBed")
    # - 'house' as standalone or with suffix
    # - 'QUOT' after ci 'say'
    # Disambiguation: -in on verb stem = CVB, on noun = ERG
    'in': [
        ('ERG', 'case_marker'),      # Ergative case on nouns (most common)
        ('CVB', 'converb'),          # Converb on verbs (same-subject sequential)
        ('house', 'nominal'),        # Noun: house (standalone)
        ('QUOT', 'after_ci'),        # Quotative after ci 'say'
    ],
    
    # mang: 'dream/vision' (noun) vs 'obey' (verb) vs 'fly' (verb/rare)
    # - 'dream' in "mang sungah" = in a dream, "mang man" = dream
    # - 'obey' in "thu mang" = obey word, "ka mang" = I obey
    # - 'fly' rare, mainly in compounds
    'mang': [
        ('dream', 'standalone'),     # Noun: dream, vision (55+ occurrences)
        ('obey', 'with_thu'),        # Verb: obey (143+ occurrences with thu)
        ('fly', 'in_compound'),      # Rare: fly (2x, mainly in galkapmang)
    ],
    
    # ah: 'LOC' (locative) vs 'DAT' (dative/allative)
    # Henderson distinguishes positional (-ah) from directional (goal)
    'ah': [
        ('LOC', 'locative'),         # Locative case (at/in/on)
        ('DAT', 'dative'),           # Dative/goal (to)
    ],
    
    # te: 'PL' (plural) vs diminutive
    # - 'PL' on nouns (mi-te = people)
    # - Diminutive in some compounds
    'te': [
        ('PL', 'plural'),            # Plural marker (default)
        ('DIM', 'diminutive'),       # Diminutive (rare)
    ],
    
    # thum: 'three' (numeral) vs 'entreat' (verb) vs 'mourn' (verb)
    # - 'three' in numeral contexts (ni thum = day three, kum thum = year three) ~200x
    # - 'entreat' with 1SG/2SG markers: kong thum, hong thum ~140x
    # - 'mourn' with kapin (weep): kapin thum, or 3SG in mourning context ~25x
    # Disambiguation: kong/hong → entreat; kapin → mourn; ni/kum/kha → three
    'thum': [
        ('three', 'numeral'),        # Numeral (default in numeric contexts)
        ('entreat', 'verbal'),       # Verb: entreat, beseech, implore (kong/hong thum)
        ('mourn', 'verbal'),         # Verb: mourn, lament, bewail (kapin thum)
    ],
    
    # pi: 'grandmother/big' vs 'also/give'
    # - 'big' as intensifier (khua-pi = big-town = city)
    # - 'grandmother' standalone
    'pi': [
        ('big', 'intensifier'),      # Intensifier (default in compounds)
        ('grandmother', 'kinship'),  # Kinship term
        ('also', 'additive'),        # Additive particle
    ],
    
    # hen: 'JUSS' (jussive) vs 'tie' (verb)
    # - 'JUSS' sentence-final (om hen = let there be) ~500x
    # - 'tie' as verb with prefixes/suffixes (hong hen = tie me, hen uh = they tied) ~50x
    # Context: JUSS when sentence-final; tie with object prefixes or plural uh
    'hen': [
        ('JUSS', 'sentence_final'),  # Jussive/optative "let/may" (default)
        ('tie', 'verbal'),           # Verb: tie, bind (with hong-, hen uh, etc.)
    ],
    
    # mu: 'see' (Form I) - Form II is 'muh'
    # Henderson: mu (Form I) in conclusive sentences, muh (Form II) elsewhere
    'mu': [
        ('see.I', 'form_i'),         # Form I (indicative)
    ],
    
    # ci: 'say' (Form I) - Form II is 'cih'
    # Henderson: ci 'say' is highly grammaticalized as quotative marker
    'ci': [
        ('say', 'quotative'),        # Quotative verb (default)
    ],
    
    # lawm: 'worthy/suitable' (verb/adj) vs 'friend' (noun) vs 'lamb' (noun)
    # - 'worthy' with ki- prefix (ki-lawm = REFL-worthy = be fitting/worthy) - 258x
    # - 'friend' in compounds (lawmte = friends)
    # - 'lamb' very rare
    'lawm': [
        ('worthy', 'with_ki'),       # With ki- prefix: be worthy/suitable
        ('friend', 'nominal'),       # Friend (noun)
        ('lamb', 'rare'),            # Lamb (rare in Bible)
    ],
    
    # hut: 'arm' (weapon) vs 'shelter' (noun/verb)
    # - 'arm' (weapon) with hut (6x)
    # - 'shelter' in kihut = refuge (ki-hut-na = shelter-NMLZ)
    'hut': [
        ('shelter', 'with_ki'),      # Refuge with ki- prefix
        ('arm', 'weapon'),           # Weapon/armament
    ],
    
    # luang: 'flow' (verb) vs 'corpse' (noun)
    # - 'flow' with water/liquid subjects, often reduplicated (luan-luang)
    # - 'corpse' in death/burial contexts
    'luang': [
        ('flow', 'verbal'),          # Flow (water, blood)
        ('corpse', 'nominal'),       # Corpse/dead body
    ],
    
    # hong: 'come' (verb) vs '3→1' (directional marker)
    # - Verb: 'open' (hong-khia = open-out), 'come' standalone
    # - Directional: hong-pai = toward speaker (3→1 direction)
    # The 3→1 marker is a grammaticalized prefix, not standalone
    'hong': [
        ('3→1', 'prefix'),           # Directional: toward 1st person
        ('open', 'verbal'),          # Open (door, etc.)
        ('come', 'standalone'),      # Come (rare standalone)
    ],
    
    # nga: 'endure' (verb) vs 'five' (numeral)
    # - 'five' in numeral contexts (sagih-nga = seven-five = 75)
    # - 'endure' as verb stem
    'nga': [
        ('five', 'numeral'),         # Five (in counting)
        ('endure', 'verbal'),        # Endure/tolerate
    ],
    
    # ding: 'stand' (verb) vs 'IRR' (irrealis marker)
    # - 'stand' as main verb (ding-in = standing)
    # - 'IRR' as TAM suffix indicating future/intention
    'ding': [
        ('IRR', 'suffix'),         # Irrealis marker (most common)
        ('stand', 'verbal'),         # Stand (rare as main verb)
    ],
    
    # ngen: 'pray' (verb) vs 'net' (noun)
    # Dictionary: "ngen (len), n. net, fishing net"
    # - 'pray' with thu = "pray word" = pray/petition/ask
    # - 'net' in fishing contexts (with nga = fish, tuili = lake/river)
    # Context: fishing vocabulary → net; prayer vocabulary → pray
    'ngen': [
        ('pray', 'verbal'),          # Pray, petition (default; most common)
        ('net', 'nominal'),          # Fishing net (Mark 1:16-19)
    ],
    
    # kei: 'NEG' (negation) vs '1SG.PRO' (pronoun)
    # Dictionary: kei (adv) = "not in no manner"; kei (pro) = "I, myself"
    # - NEG: negative marker in verb phrases (V kei = not V)
    # - 1SG.PRO: first person pronoun "I, me" (kei sangin = "than me")
    # Context: after verb → NEG; with postpositions/sangin → 1SG.PRO
    'kei': [
        ('NEG', 'negation'),         # Negative marker (default in verbal contexts)
        ('1SG.PRO', 'pronoun'),      # First person pronoun "I, me"
    ],
    
    # hu: 'help' (verb) vs 'breath' (noun)
    # Dictionary: hu (n) = "breath"; hu (v) = "to block" (but Bible shows 'help')
    # - help: verbal action "to help/protect" (hong hu = help you)
    # - breath: noun, esp. in "nuntakna hu" = breath of life
    # Context: after 'nuntakna' → breath; in 'hu tawpna/sang' idiom → breath
    'hu': [
        ('help', 'verb'),            # Help/protect (default verbal meaning)
        ('breath', 'noun'),          # Breath, in 'breath of life' and 'give up ghost'
    ],
}

# English metadata words that appear in Bible file headers (not Tedim text)
# These should be glossed as themselves to avoid mis-parsing
METADATA_WORDS = {
    'available': 'available',
    'information': 'information',
    'ctd': 'CTD',           # ISO 639-3 code
    'scraped': 'scraped',
    'from': 'from',
    'original': 'original',
    'source': 'source',
    'https': 'HTTPS',
    'www': 'WWW',
    'bible': 'bible',
    'com': 'COM',
}

# ============================================================================
# POSTPOSITIONS
# ============================================================================
# These are FREE words that follow nouns, NOT bound suffixes.
# Unlike case markers (-in, -ah), these are written separately.
# Example: "pa tawh" (with father) = two words, NOT "*patawh"
# ============================================================================
POSTPOSITIONS = {
    'tawh': 'COM',       # comitative "with" - 7,806 occurrences as standalone
                         # Example: "amah tawh" = with him, "mei tawh" = with fire
    'tawhin': 'COM.ERG', # comitative+ergative (instrumental) - 2 occurrences
                         # Example: "mei tawhin moh a em hi" = he roasted bread with fire
    'pan': 'ABL',        # ablative "from" - 603 standalone, also bound to proper nouns
                         # Example: "sung pan" = from inside, "Jerusalempan" = from-Jerusalem
    'panin': 'ABL.ERG',  # ablative+ergative - very common with relator nouns
                         # Example: "sung panin" = from inside (as agent)
}

# ============================================================================
# RELATOR NOUNS (Spatial/Relational Postpositions)
# ============================================================================
# These are NOUNS with spatial meanings that function like postpositions.
# They take a genitive-marked possessor and can themselves be case-marked.
# Pattern: [Possessor-GEN] [Relator-CASE]
# Example: mite' sungah = people-GEN inside-LOC = "among the people"
#
# Unlike true postpositions (tawh, pan), these have full nominal morphology:
# - Can take locative: tungah, sungah, lakah, kiangah
# - Can take ergative: tungin, sungin, lakin
# - Can take ablative: tung pan, sung pan, lak pan (usually written separately)
# ============================================================================
RELATOR_NOUNS = {
    # Core spatial relators (high frequency)
    'tung': 'on',        # 1,491 standalone; 6,072 as tungah; 84 as tungin
                         # inn' tungah = on the house
    'sung': 'inside',    # 2,289 standalone; 3,205 as sungah
                         # inn' sungah = in the house
    'kiang': 'beside',   # 611 standalone; 4,208 as kiangah
                         # pa' kiangah = beside father
    'lak': 'among',      # 564 standalone; 769 as lakah
                         # mite' lakah = among the people
    'mai': 'front',      # 1,353 standalone (also "face")
                         # pa' maiah = in front of father
    'nuai': 'below',     # 203 standalone
                         # inn' nuaiah = below the house
    'lang': 'side',      # 45 standalone (also "clear")
                         # langkhat = one side
    # Derived spatial relators
    'pualam': 'outside', # 62 as pualamah = outside (pua-lam = other-direction)
    'langpang': 'against', # 39 standalone; 63 as langpangin
                           # amah langpangin = against him
                           # Etymology: lang 'side' + pang 'near' → adversative spatial
    # Note: These can combine with case markers and postpositions:
    # sung-ah (inside-LOC), sung pan (inside from), sung panin (inside from-ERG)
}

# Common function words with glosses - expanded with frequencies
FUNCTION_WORDS = {
    # === Conjunctions & Connectors ===
    'le': 'and',             # 10,942
    'la': 'take',            # Round 155: primary meaning is 'take' (also 'and.SEQ' after hen)
    'masa': 'first',         # Round 155: a masa = the first (not ma-sa)
    'sia': 'evil',           # Round 155: a sia = evil (not si-a)
    'leh': 'and',         # 2,921
    
    # Sentence-initial function words (prevent proper noun treatment)
    'Tu-in': 'now-ERG',      # Sentence-initial 'tu-in'
    'Siangtho': 'holy',      # Sentence-initial 'siangtho'
    'ahihleh': 'if',         # 335
    'hitaleh': 'if.so',      # 295
    'hang': 'reason',        # Round 155: fix - "bang hang hiam" = why (not stallion)
    # hangin, bangin, manin, zongin, ciangin removed - use transparent ERG analysis
    # e.g. ciangin → ciang-in = then-ERG (shows morphological structure)
    'man': 'finish',         # Round 155: a man khit = finished (also catch/wrong)
    'inla': 'and.then',      # ~838
    'napi': 'but',   # 279x - contrastive conjunction
    'hinapi': 'but', # 156x - variant with hi-
    'hinapi-in': 'but.ERG',  # 126x - hinapi with ergative
    'hinapiin': 'but.ERG',   # variant without hyphen
    'mateng': 'until',       # 185x - temporal "until"
    'matengin': 'until',     # 99x - variant with -in
    'veve': 'still',     # 142x - temporal adverb (reduplication)
    'tuazawh': 'after.that', # 7x - "after that, then" (sentence-initial)
    
    # === Purpose/Infinitive markers (NOT 2SG!) ===
    'nading': 'PURP',        # 1140x - "in order to, for (purpose)" 
    'nadingin': 'PURP.ERG',  # 1671x - purpose marker with ergative
    
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
    'vekpi': 'altogether',   # 213x "all (of), total"
    'tuamtuam': 'various',   # 59x - "different kinds, various" (reduplication)
    'ciatin': 'each.kind.ERG', # 45x - "after its kind" (ciat + -in)
    'ciatciatin': 'each.kind~REDUP', # 20x - "each after their kind" (reduplicated)
    
    # === Adverbs - Temporal/Iterative ===
    'leuleu': 'again',       # 193x - reduplication of leu
    'leu': 'again',          # base form for leuleu
    # nitakin removed - parses transparently as ni-tak-in = day-exact-ERG
    'nihin': 'today',        # 35x - "today" (ni-hin = day-this) - keep for correct gloss
    
    # === Verbal particles ===
    'kawmin': 'while',       # 39x - "while, as" (temporal subordinator)
    'itin': 'lovingly',      # 41x - "lovingly, kindly" (it-in)
    'nangawnin': 'henceforth', # 43x - "from now on, forever"
    'nangawnah': 'forever',  # 36x - variant with -ah
    
    # === Interrogatives ===
    'bangci': 'how',         # 36x - "how" (interrogative adverb)
    'bangciin': 'how.ERG',   # variant with -in
    'bangci-in': 'how.ERG',  # hyphenated variant
    
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
    'hi': 'DECL',            # 35,961 - declarative sentence-final
    # hen removed from FUNCTION_WORDS - it's ambiguous (JUSS vs 'tie')
    # Standalone 'hen' handled via AMBIGUOUS_MORPHEMES with default JUSS
    'rawh': 'HORT',          # 0x in Bible - hortative (polite imperative)
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
    'nomau': '2PL.PRO',      # 62x - "you (plural)" (alternative form)
    "nomau'": '2PL.POSS',    # 44x - "your (plural)" with possessive marker
    "ke'n": '1SG.PRO',       # 63x - "I" (contraction of kei) - straight quote
    "ke\u2019n": '1SG.PRO',   # curly quote version
    "keima-a'": '1SG.self.GEN', # 31x - "my own" - straight quote
    "keima-a\u2019": '1SG.self.GEN', # curly quote version
    'kei': '1SG.PRO',        # "I"
    'nangmahmah': '2SG.EMPH.REDUP', # 23x - "you yourself" (emphatic reduplication)
    "kua'n": 'nobody.EMPH',  # 9x - "nobody" variant - straight quote
    "kua\u2019n": 'nobody.EMPH', # curly quote version
    
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
    'uh': '2/3PL',           # 21,924 - 2nd/3rd person plural agreement clitic
    'un': 'IMP.PL',          # Imperative plural (2PL command)
    'tawh': 'COM',           # 7,572
    # panin: now parsed as pan-in (ABL-ERG) via suffix stripping
    # sangin removed - use transparent ERG analysis: sang-in = high-ERG (comparative)
    'dong': 'until',         # 647
    
    # Combinations with plural uh-
    'uhah': '2/3PL.LOC',     # 507x - "in your/their (plural)"
    'uhleh': '2/3PL.if',     # 306x - "if you (plural)"
    'uha': '2/3PL.LOC',      # 56x - variant of uhah
    'ulian': 'PL.elder',     # 96x - needs analysis (could be elder-great)
    'ung': 'PL.FUT',         # 30x - plural future marker
    'up': 'PL.Q',            # 60x - plural question marker
    
    # === Military vocabulary ===
    # kidona removed - parses transparently as ki-don-a = REFL-war-LOC
    
    # === Nature vocabulary ===
    # tuipi removed - parses transparently as tui-pi = water-big ("sea")
    
    # === Negation ===
    'lo': 'NEG',             # 6,018
    'kei': 'NEG.EMPH',       # 6,487
    # loh and loin removed - parse transparently as lo-h, lo-in
    'kuamah': 'nobody',      # 595
    'bangmah': 'nothing',    # 495
    
    # === Question ===
    'hiam': 'Q',             # 2,766
    
    # === TAM Markers ===
    'ding': 'IRR',         # 18,980
    # dingin and nadingun removed - parse transparently as ding-in, na-ding-un
    'ta': 'PFV',             # 1,106
    'zo': 'COMPL',
    'kik': 'ITER',
    'nawn': 'CONT',          # 1,022
    'khin': 'IMM',           # 893
    'khit': 'SEQ',           # 996
    
    # === Relational/Nominalizers ===
    'mi': 'person',      # 4,221
    'te': 'PL',
    # Note: 'na' is 2SG in FUNCTION_WORDS (line 295), -na is NMLZ as suffix
    
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
    # sawmnih removed - parses transparently as sawm-nih = ten-two ("twenty")
    'za': 'hundred',         # In number context (kum za = 100 years); also 'hear' - see AMBIGUOUS_MORPHEMES
    'tul': 'thousand',
    
    # === Locative/Relational Nouns ===
    'sung': 'inside',        # 2,208
    'tung': 'on',            # 1,413
    'kiang': 'beside',       # 597
    'lai': 'midst',          # 1,032
    'lak': 'among',          # 552
    'mai': 'front',
    'ban': 'besides',        # 85x - "beside X", often banah "in addition to"
    'pualam': 'outside',     # 60x - "without, outside"
    'nuai': 'below',         # 42x - "under"
    
    # === Adverbs ===
    'mahmah': 'very',
    # tawntung removed - parses transparently as tawn-tung = ever-always ("forever")
    'tu': 'now',
    
    # === Interrogatives/Comparatives ===
    'bang': 'like',     # often in compounds
    'kua': 'who',
}

# =============================================================================
# VERB STEM ALTERNATION (Form I / Form II)
# =============================================================================
#
# Based on Henderson 1965 "Tiddim Chin: A Descriptive Analysis of Two Texts"
#
# Tedim Chin verbs have two forms:
# - Form I (Indicative): Used in conclusive sentences (final predicative phrase)
# - Form II (Subjunctive): Used in inconclusive sentences and adjunctive phrases
#
# Form II is derived from Form I by phonological rules:
# 1. For verbs with long final syllable + Tone 1/2: Add -h, change to Tone 3
#    Examples: mu → muh (see), thei → theih (know), nei → neih (have)
#
# 2. For some verbs: Add -k instead of -h
#    Examples: za → zak (hear), pia → piak (give), ne → nek (eat)
#
# 3. For verbs ending in -ng: Change to -n (velar → alveolar)
#    This pattern is less common in the Bible corpus
#
# The analyzer recognizes both forms and glosses them appropriately.
# Form II verbs get the same base gloss as Form I (the alternation is 
# grammatical, not lexical).
#
# =============================================================================

VERB_STEM_PAIRS = {
    # Primary verb alternation pairs: Form I → Form II
    # Format: form_ii: (form_i, base_gloss)
    
    # +h alternation (most common)
    'muh': ('mu', 'see'),           # 503x Form II / 967x Form I
    'theih': ('thei', 'know'),      # 1385x / 2579x
    'neih': ('nei', 'have'),        # 416x / 1803x
    'cih': ('ci', 'say'),           # 2827x / 5971x
    'zuih': ('zui', 'follow'),      # 170x / 509x
    'ngaih': ('ngai', 'think'),     # 52x / 434x
    'neh': ('ne', 'eat'),           # 17x / 560x
    'siah': ('sia', 'decay'),       # 61x / 220x
    'khialh': ('khial', 'err'),     # 54x / 177x
    'luah': ('lua', 'exceed'),      # 192x / 111x
    'puah': ('pua', 'bet'),         # 66x / 153x
    'tuah': ('tua', 'do'),          # 47x / (tua usually demonstrative)
    'tanh': ('tan', 'spread'),      # 71x / 22x
    'genh': ('gen', 'speak'),       # Form II of gen
    'bawlh': ('bawl', 'make'),      # Form II of bawl
    'omh': ('om', 'exist'),         # Form II of om
    'paih': ('pai', 'go'),          # Form II of pai
    
    # hi/hih - copula "be" alternation
    # Henderson: hi (Form I) in conclusive/declarative sentences
    #           hih (Form II) in inconclusive sentences, before other predicates
    # NOTE: hih is ALSO 'this' (proximal demonstrative) - context determines meaning
    # - hih as Form II: "a hih bangin" = "as it being" (manner clause)
    # - hih as PROX: "hih pa" = "this person"
    'hih': ('hi', 'be'),            # Form II of hi (copula) - disambiguate vs 'this'
    
    # tu/tuh - sit verb alternation (also tuh='sow' lexicalized)
    # Henderson: tu (Form I) 'sit', tuh (Form II)
    # NOTE: tuh is primarily 'sow' in Bible corpus - context determines
    'tuh': ('tu', 'sit'),           # Form II of tu (sit) - vs lexicalized 'sow'
    
    # +k alternation
    'zak': ('za', 'hear'),          # 347x / 664x
    'piak': ('pia', 'give'),        # 797x / 2209x
    'nek': ('ne', 'eat'),           # 199x / 560x (both +h and +k exist)
    'biak': ('bia', 'worship'),     # 212x / 219x
    'puak': ('pua', 'spill'),       # 239x / 153x
    'tuak': ('tua', 'meet'),        # 100x (verbal, not demonstrative)
    'muk': ('mu', 'see'),           # 24x (alternative Form II)
    'kiak': ('kia', 'fear'),        # 8x / 66x
    
    # +t alternation (for stems ending in -a)
    # Henderson: Some stems add -t for Form II
    'nusiat': ('nusia', 'abandon'),     # Form II of nusia
    'kidot': ('kido', 'fight'),         # Form II of kido  
    'husiat': ('husia', 'tempest'),     # Form II of husia
    'honkhiat': ('honkhia', 'bring.out'), # Form II of honkhia
    'sawlkhiat': ('sawlkhia', 'send.forth'), # Form II of sawlkhia
    'hawlkhiat': ('hawlkhia', 'drive.out'), # Form II of hawlkhia
    'tuahphat': ('tuahpha', 'quickly'),  # Form II of tuahpha
    'dipkuat': ('dipkua', 'haste'),     # Form II of dipkua
    'gamlat': ('gamla', 'wilderness'),  # Form II of gamla (nominal)
    
    # Additional -h forms from corpus (now handled via VERB_STEM_PAIRS, not TAM_SUFFIXES)
    'noh': ('no', 'young'),             # young.II
    'sumh': ('sum', 'money'),           # money.II (nominalized)
    'mualh': ('mual', 'mountain'),      # mountain.II
    'thuh': ('thu', 'word'),            # word.II
    'khaih': ('khai', 'hold'),          # hold.II
    'keuh': ('keu', 'dig'),             # dig.II
    'khoh': ('kho', 'labor'),           # labor.II
    'vialh': ('vial', 'encircle'),      # encircle.II
    'lampih': ('lampi', 'way'),         # way.II
    
    # Conflicting stems - need special disambiguation
    # khot: labor.II vs kho-te (labor-PL) - see FORM_II_DISAMBIGUATION
    # khuat: dig.II vs khua-te (town-PL) - see FORM_II_DISAMBIGUATION
    'khot': ('kho', 'labor'),           # labor.II (disambiguate vs kho-te)
    'khuat': ('khua', 'town'),          # NOTE: This is khua.II, not dig.II!
}

# Form II stems that conflict with stem+suffix patterns
# These require special handling in analyze_word() to check context
FORM_II_DISAMBIGUATION = {
    'khot': {
        'form_ii_of': 'kho',
        'conflicts_with': ('kho', 'te'),  # kho-te = labor-PL
        'prefer_segmented_when': ['te', 'in', 'ah'],  # When followed by these suffixes
    },
    'khuat': {
        'form_ii_of': 'khua', 
        'conflicts_with': ('khua', 'te'),  # khua-te = town-PL
        'prefer_segmented_when': ['te', 'in', 'ah', 'pi'],
    },
}

# Reverse lookup: Form I → Form II (for reference)
FORM_I_TO_II = {v[0]: (k, v[1]) for k, v in VERB_STEM_PAIRS.items()}


def is_form_ii_verb(stem: str) -> tuple:
    """
    Check if a stem is a Form II verb and return its analysis.
    
    Henderson 1965: Form II verbs are marked by:
    - Addition of -h to Form I stems ending in vowels
    - Addition of -k to some Form I stems  
    - Change of final -ng to -n
    
    Args:
        stem: The verb stem to check
        
    Returns:
        Tuple of (is_form_ii, form_i, base_gloss) or (False, None, None)
    """
    # Direct lookup in VERB_STEM_PAIRS
    if stem in VERB_STEM_PAIRS:
        form_i, gloss = VERB_STEM_PAIRS[stem]
        return (True, form_i, gloss)
    
    # Heuristic: stems ending in -h might be Form II
    # Check if removing -h gives a known Form I verb
    if stem.endswith('h') and len(stem) > 1:
        possible_form_i = stem[:-1]
        if possible_form_i in VERB_STEMS:
            gloss = VERB_STEMS[possible_form_i]
            # Remove .I suffix if present
            if gloss.endswith('.I'):
                gloss = gloss[:-2]
            return (True, possible_form_i, gloss)
    
    # Heuristic: stems ending in -k might be Form II
    if stem.endswith('k') and len(stem) > 1:
        possible_form_i = stem[:-1]
        if possible_form_i in VERB_STEMS:
            gloss = VERB_STEMS[possible_form_i]
            if gloss.endswith('.I'):
                gloss = gloss[:-2]
            return (True, possible_form_i, gloss)
    
    # Not a recognized Form II
    return (False, None, None)

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
    'sih': 'die',            # death
    'sil': 'wipe',     # sil-khia = wipe away
    'nung': 'live',          # life
    'piang': 'be.born',      # birth
    'hen': 'tie',            # ~50x - tie/bind (hencip, kihen, henin, henna)
    
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
    'ciah': 'return',        # 360
    'ciahkik': 'return.again',
    
    # Perception verbs (with stem alternation)
    'mu': 'see.I',           # 962 (Stem I)
    'muh': 'see.II',         # 501 (Stem II)
    'za': 'hear.I',          # 652 (Stem I)
    'zak': 'hear.II',        # (Stem II)
    'ngai': 'listen.I',
    'ngaih': 'listen.II',
    'en': 'look',
    'leen': 'fly',           # fly (Job 5:7, Ezek 1:24)
    
    # Cognition verbs (with stem alternation)
    'thei': 'know.I',        # 2,543 (Stem I)
    'theih': 'know.II',      # 1,383 (Stem II / passive)
    'um': 'believe',
    'ngaihsun': 'think',     # 409 "mind-think"
    'ngaihsut': 'consider',  # 210
    'lung': 'feel',          # emotional state
    'deih': 'want',          # 279
    'nuam': 'want',
    
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
    'pau': 'speak',          # 240
    
    # Transfer/Possession
    'pia': 'give',           # 2,202
    'piak': 'give.to',       # 781
    'lak': 'take',           # 552
    'nei': 'have',           # 1,770
    'koih': 'put',           # 592
    'sawl': 'send',          # 541
    'sak': 'cause',          # 220 causative
    
    # Action verbs
    'bawl': 'make',          # 1,532
    'sem': 'serve',          # 603
    'sep': 'work',           # 127
    'uk': 'rule',            # 664
    'that': 'kill',
    'tat': 'strike',
    'sat': 'strike',         # 214
    'ne': 'eat',             # 552
    'nek': 'eat.II',
    'thuak': 'suffer',       # 535
    'phum': 'immerse',
    'vak': 'walk',
    'tawp': 'end',
    'ding': 'stand',
    'to': 'sit',
    'ton': 'pull',           # "pull, draw" (tonsak = cause.to.pull)
    'tut': 'sleep',
    # NOTE: 'suk' as standalone is rare - usually directional suffix -suk (DOWN)
    'khen': 'divide',
    'khecin': 'sharp',       # 18x - sharp (adj) - khecinte = sharp-PL
    'gelh': 'write',
    'kap': 'weep',           # 185
    'zah': 'fear',           # 182
    'zawh': 'be.able',       # 178
    'khial': 'err',          # 177
    'nusia': 'abandon',      # 173
    # Note: nusiat (Form II) now in VERB_STEM_PAIRS, not here
    'pil': 'learn',          # 242
    'siam': 'be.skilled',    # 174
    'lup': 'bow.down',       # 140
    'kem': 'guard',          # 147
    'zang': 'use',           # 198
    'duh': 'want',      # 30x - "want, love, desire"
    'muan': 'trust',         # 30x - "trust, rely on"
    'vel': 'around',         # 29x - "around, approximately"
    'im': 'hide',            # 33x - "hide" (im ding = shall hide)
    'u': 'elder.sibling',    # 28x - "elder brother/sister"
    'nungta': 'live',        # 29x - "be alive, live" (variant of nuntak)
    'limci': 'promise',      # 32x - "promise, sign" (lim-ci)
    
    # Reflexive/reciprocal (ki- prefix)
    'kipat': 'begin',        # Round 155: variant of kipan (a kipat = in the beginning)
    'kipan': 'begin',        # ki-pan "REFL-begin"
    'kizom': 'unite',        # Round 155: be united/joined
    'kisai': 'concern',
    'kisik': 'repent',
    'kikhia': 'depart',
    'kibawl': 'be.done',     # 338
    'kibang': 'be.alike',    # 612
    'kikhel': 'differ',
    'kituah': 'meet',
    'kikhen': 'separate',
    'kilem': 'prepare',      # 131
    'khakun': 'be.cast.down', # Ps 42:5, 42:11, 43:5 "disquieted" (khakunkun = REDUP)
    
    # Causative/applicative (-sak, -pih)
    'paisak': 'send',        # pai-sak "go-CAUS"
    'damsak': 'heal',        # dam-sak "well-CAUS"
    'paipih': 'accompany',   # 599 pai-pih "go-APPL"
    'honkhia': 'bring.out',
    # Note: honkhiat (Form II) now in VERB_STEM_PAIRS
    'piangsak': 'cause.birth', # 221
    'tungsak': 'lift.up',    # 197
    'paikhiat': 'send.away', # 202
    
    # Additional common verbs from corpus
    'it': 'love',
    'zol': 'redeem',
    'hong': 'come',
    'ciapteh': 'receive',
    'nuntak': 'live',        # nun-tak "life-firm"
    'minthan': 'bless',      # 253
    'hehpih': 'be.angry',    # 233
    'zahtak': 'honor',       # 148
    'lungdam': 'rejoice',    # 154
    
    # Additional verb stems from frequency analysis (Round 2)
    'huam': 'surround',      # 27x
    'buang': 'be.confused',  # 21x
    'ngeisa': 'desire',      # 15x
    'dem': 'blame',          # 12x
    'phong': 'reveal',       # 11x
    'ngian': 'endure',       # 11x
    'buak': 'fight',         # 10x
    'laih': 'replace',       # 10x
    'gawm': 'seize',         # 9x
    'hawl': 'seek',          # 9x
    'pung': 'increase',      # 12x
    'hoi': 'arrange',        # 15x
    'zuat': 'prepare',       # 13x
    'ngah': 'get',           # common
    'let': 'return',         # 10x
    'dial': 'call',          # 10x
    'vial': 'encircle',      # 10x
    'tangtun': 'arrive',     # 10x
    'hawm': 'join',
    'cim': 'pierce',
    'zop': 'join',           # 10x
    'kho': 'labor',          # 10x
    # Note: khot='labor.II' removed - conflicts with kho-te (labor-PL)
    'puah': 'divine',
    'dokkik': 'oppose',      # 10x
    'dinkhiat': 'stand.up',  # 10x
    'zem': 'be.straight',    # 11x
    'sel': 'slice',          # 11x
    'khum': 'cover',         # 14x
    'hisak': 'make.known',   # 19x
    'neih': 'have.II',       # 16x (Stem II of nei)
    'sithei': 'be.possible', # 17x
    'veng': 'guard',         # 15x
    'mangkhin': 'faint',     # 14x
    'guang': 'carry',        # 12x
    'thadah': 'forgive',     # 12x
    'uih': 'bark',           # 12x
    'vekin': 'like',         # 12x
    'gimthuak': 'suffer',    # 12x
    'manphazaw': 'succeed',  # 12x
    'bangcih': 'how.say',    # 12x
    'siansak': 'sanctify',   # 12x
    'huhau': 'surround',     # 12x
    'geelsa': 'mark',        # 11x
    'sunglam': 'inside.way', # 11x
    'notkhia': 'bring.out',  # 9x
    'kunsuk': 'bend.down',   # 9x
    'vukcip': 'cover.over',  # 9x
    
    # Additional verb stems (Round 3 - remaining unknowns)
    'bat': 'bind',           # for kibat
    'tuam': 'promise',       # for kituam
    'phut': 'spray',         # for kiphut  
    'lakkhiat': 'snatch',    # ki-lakkhiat "take-away"
    'limbawl': 'prepare',    # 26x
    'khinsa': 'mock',        # 28x
    'hamtang': 'be.strong',  # 15x
    'liang': 'shine',        # 15x
    'khitsa': 'leave',       # 15x
    'lobuang': 'disturb',    # 14x
    'diak': 'be.different',  # 14x
    'galtai': 'be.captive',  # 13x
    'taleng': 'gather',      # 13x
    'huai': 'dread',         # 12x
    'dei': 'say',            # 11x - variant of ci
    'ngongtat': 'oppose',    # 10x
    'mal': 'be.dry',         # 14x
    'ven': 'protect',        # 14x
    'seek': 'sweep',         # 17x
    'vot': 'vote',           # 11x (loan word)
    'puakkik': 'return',     # 11x
    'hite': 'hate',          # 2x - "hate" (verb) - a hite kei = "hate me"
    'lampial': 'scatter',    # 19x - "drive away, scatter, stray"
    
    # Round 4 - more verb stems from remaining unknowns
    'am': 'sink',            # for kiam (ki-am)
    'mat': 'grasp',          # for kimat (ki-mat)
    'cian': 'announce',      # for kician (ki-cian)
    'pawlthei': 'join',      # for kipawlthei
    'teh': 'measure',        # for kiteh
    'kham': 'forbid',        # for kikham
    'kep': 'clutch',         # for kikep
    'khem': 'restrain',      # for kikhem
    'luh': 'plunder',        # for kiluh (be plundered, robbed)
    'khezaw': 'lame', # 6x - "lame, crippled" (khezawte = lame people)
    'pua': 'carry.on.back',  # for kipua
    'sit': 'cut.off',        # for kisit
    'nga': 'endure',         # for kinga
    'awk': 'snare',          # 67x - "catch, snare, trap" (awkin=snared)
    # Note: tuh='dispute' conflicts with tuh='sow' in COMPOUND_WORDS; use kituhna compound instead
    'peel': 'peel',          # 12x
    'peng': 'break.into',    # 10x
    'hum': 'cover',          # 10x
    'tuamin': 'cover',       # 18x - cover/wrap (1Ki 19:13 "wrapped face")
    'taka': 'truly',         # 9x
    'tanau': 'orphan',       # 9x (noun)
    've': 'do',              # 9x
    'ngeingai': 'truly.want', # 9x
    
    # Round 5 - philologically verified stems from Bible context analysis
    # Each entry verified by examining English verse contexts
    'ba': 'owe',             # 11x - Matt 18:23-24 "owed ten thousand talents"
    'nolh': 'reject',        # 9x - 1Sam 15:23 "rejected the word", "abhorred"
    'kunh': 'entreat',       # 9x - Judg 13:8 "intreated the LORD"
    'siim': 'feast',         # 9x - Job 1:4 "feasted in their houses"
    'vul': 'flourish',       # 9x - Ps 1:3 "like a tree planted" (cf. Henderson informant)
    'tot': 'contend',        # 9x (via kitot) - Num 27:14 "rebelled/strife"
    'nial': 'argue',         # 9x (via kinial) - Job 9:3 "contend/answer"
    'siat': 'spoil',         # 9x (via kisiat) - Ps 18:37 "pursued/overtaken"
    'samsiat': 'destroy',    # compound sam-siat (call-spoil = destroy)
    'lawnthal': 'overthrow', # 9x - Ex 15:7 "overthrown them"
    'zomlai': 'journey',     # 9x - Gen 35:21 "journeyed"
    'lianlua': 'too.much',   # 9x - Num 11:14 "too heavy for me"
    'thakhatthu': 'suddenly', # 9x - Num 12:4 "suddenly", Lev 26:16 "terror"
    'tuakun': 'meet',        # 9x - Prov 22:2 "meet together"
    'sungtawng': 'within',   # 10x - 1Ki 6:19 "in the house within", "oracle"
    'dongun': 'boundary',    # 14x - Lev 23:22 "corners of thy field"
    'utzaw': 'destruction',  # 11x - Job 7:15 "death", Isa 65:12 "slaughter"
    
    # Round 6 - additional verbs from residual analysis
    'puak': 'send',          # 239x - Gen 37:32 "sent/brought", Gen 38:17 "send"
    'ngak': 'wait',          # 102x - Gen 8:12 "stayed", Gen 49:18 "waited"
    'ngam': 'dare',          # 128x - (context shows "venture/dare")
    'hawlkhia': 'drive.out', # 119x - Gen 3:24 "drove out the man"
    # Note: hawlkhiat (Form II) now in VERB_STEM_PAIRS
    'vei': 'sick',           # 71x - Gen 25:29 "he was faint" (sick/faint/exhausted)
    'zenzen': 'at.all',      # 53x - intensifier (often with negation "not at all")
    'mengmeng': 'quickly',   # 50x - reduplication "hastily, speedily" (Gen 18:6)
    'meng': 'quick',         # base for mengmeng
    'kantan': 'cross.over',  # 45x - "pass over, cross" (NOT kan-tan)
    'khahkhia': 'deliver',   # 46x - "deliver, rescue" (NOT khah-khia)
    'lungkia': 'dismay',     # 43x - "be dismayed, terrified"
    'tawlngak': 'rest',      # 45x - "rest" (base for tawlngakna)
    'sitbaang': 'blemish',   # 43x - "blemish" (without blemish)
    'ut': 'will',       # 44x - "will, desire" (base for utna)
    'buai': 'confuse',       # 41x - "confusion, astonishment" (base for buaina)
    'tuang': 'ride',         # 43x - "ride" (tuangte = riders, horsemen)
    'hon': 'flock',          # 41x - "flock, herd" (honte = flocks)
    'ngetsak': 'pray',  # 61x - causative of nget (request)
    
    # === Recently discovered verb stems (from partial analysis) ===
    'ap': 'press',    # 53x - ki-ap = submit (reflexive)
    'at': 'cut',             # 53x - ki-at = circumcise (reflexive cut)
    'bia': 'worship',        # 49x - bia-in = worshipping
    'biak': 'worship', # 211x - "worship, serve" (biak nading = for serving)
    'gamtat': 'kingdom',     # base for gamtatna, gamtatnasa
    'phat': 'praise',        # 70x - "praise, bless, commend" (kiphatsakna = pride)
    'phatsak': 'glorify',    # 45x - "glorify" (phat + CAUS)
    'zeet': 'tempt',         # 48x - "tempt, test" (ze-et hyphenated)
    'khangsak': 'raise.up',  # 39x - "raise up generations" (khang + CAUS)
    'lasak': 'take.CAUS',    # 39x - "take away" (la + sak)
    
    # === Session 2: More verb stems from philological analysis ===
    'kantan': 'cross.over',  # 44x - "cross over, fly across" (vantung kantanin = fly across heaven)
    'sawlkhia': 'send.forth', # 37x - "send forth, expel"
    # Note: sawlkhiat (Form II) now in VERB_STEM_PAIRS
    'lumkhawm': 'lie.with',  # 37x - "lie with, sleep with"
    'sepsak': 'serve', # 35x - "cause to work, serve"
    'khaktan': 'restrain',   # 35x - "restrain, prevent" (khak-tan)
    'vangik': 'burden', # 35x - "burden" (between two burdens)
    'cimawh': 'oppress',     # 39x - "oppress" (a zawng a cimawh = oppressed)
    
    # === Session 3: Additional verb stems ===
    'khuh': 'cover',         # 36x - "cover" (kh-uh vs cover.I, but better as standalone)
    'sap': 'call',    # 33x - "call, summon" (Faro in Moses sap = Pharaoh called Moses)
    'ngat': 'seek',   # 33x - "seek (omens), divine"
    'ciam': 'promise',       # 33x - "promise" (thuciam = thu-ciam = word-promise = covenant)
    'it': 'love',            # base for "itte" (it-te = love-PL?)
    'gamta': 'send.away',    # 50x - "send away" (hong hawlkhia = sent away)
    'dawng': 'receive',  # 387x - "get, receive, fetch" (bawngno a dawng = fetched a calf)
    'luan': 'flow',          # 32x - "flow" (luanna = flowing)
    'khiat': 'depart', # 32x - "depart, leave"
    'pian': 'create',   # 32x - "create, be born" (piansak = creation work)
    'bei': 'finish',     # 32x - "end, finish" (beina = ending)
    'pan': 'plead',          # 32x - "plead, argue for"
    'kido': 'fight',         # 31x - "fight" = ki-do REFL-fight (galkidona = warfare)
    # Note: kidot (Form II) now in VERB_STEM_PAIRS
    'ciah': 'return',        # 31x - "return" (ciahsak = send back)
    'khol': 'denounce',      # 31x - "denounce" (genkhol = speak denounce)
    'nuih': 'laugh',         # 31x - "laugh" (nuihsan = laugh at)
    'simmawh': 'blaspheme',  # 31x - "blaspheme"
    'khual': 'sojourn',      # 30x - "sojourn, visit" (khualmi = stranger)
    'zah': 'fear',   # 30x - "fear, respect" (zahzah = reduplicated)
    'kihtak': 'dread',       # 30x - "dread" (kihtakna = dread)
    'suahtak': 'redeem',     # 30x - "redeem" (suahtakna = redemption)
    'nop': 'willing',   # 52x - "willing, want" (a numei in nang hong zuih nop)
    'ngaih': 'love',   # 33x - "think lovingly of, love"
    'muhdah': 'trouble',     # 29x - "trouble, make stink"
    'geel': 'plan',  # 29x - "plan, design" (geelna = pattern)
    'teel': 'choose',        # 28x - "choose" (teelna = choice)
    'mindai': 'shame',       # 29x - "shame" (mindaina = shame)
    'sep': 'work',           # 28x - "work" (sepnate = works)
    'ngaihsut': 'think', # 27x - "think, imagine" (ngaihsutnate = thoughts)
    'lot': 'cast',           # 7x - "cast, throw, shoot" (KJV "cast", "shot")
    
    # === Newly discovered stems from rare words analysis ===
    'dawn': 'top',               # 8x - Gen 11:4 "tower whose top may reach unto heaven"
    'dawnkim': 'drink.all',      # Mark 14:23 "they all drank of it"
    'dawntheih': 'able.to.drink', # Matt 20:22 "are ye able to drink"
    'dawntuah': 'meet',          # 24x - Gen 24:17, Josh 9:11 "go to meet them"
    'nkhiat': 'set.forward',     # Num 10:5-6 "set forward" (dinkhiat = stand-forward)
    'nsak': 'redeem',    # ki-nsak = be redeemed, hinsakna = redemption
    'leentheih': 'fly',          # Job 39:26 "doth the hawk fly"
    'kitamzan': 'broken',        # Ps 34:18 "broken heart" (REFL-many-break = completely broken)
    'nawlkhin': 'ways',          # Job 21:14 "knowledge of thy ways" (nawl-khin as compound)
    'kiphatna': 'praise',        # Ps 9:14 "show forth all thy praise"
    'sumngo': 'rotten',          # Job 41:27 "brass as rotten wood"
    'lungngaihngaih': 'meditate', # Ps 63:4 "meditate on thee" (reduplication of ngaih)
    'khuisatna': 'groaning',     # Ps 38:9 "my groaning is not hid"
    'kuampi': 'valley',          # Ps 65:13 "valleys covered with corn"
    'lunggulh': 'delight',       # Ps 68:30 "people that delight in war"
    'tauna': 'mourning',         # Ps 30:11 "turned my mourning into dancing"
    'husia': 'tempest',          # Ps 55:8 "windy storm and tempest"
    # Note: husiat (Form II) now in VERB_STEM_PAIRS
    'kisut': 'spoil',            # Ps 68:12 "divided the spoil"
    'lip': 'scale',              # Job 41:15 "his scales are his pride"
    'maiphut': 'confront',       # Ps 17:13 "disappoint him" (mai-phut = face-??)
    'thalpaih': 'cast.down',     # Ps 17:13 "cast him down" (thal-paih = bow-go?)
    'lungtaii': 'rejoice',       # Ps 19:5 "rejoiceth as a strong man"
    'maikhingsak': 'shame',      # Ps 40:15 "desolate for their shame"
    'ngtanpih': 'excellency',    # Ps 47:4 "excellency of Jacob" (a-ngtanpih)
    'nnlelo': 'family',          # Ps 68:6 "setteth the solitary in families"
    'sahpi': 'thick.cloud',      # Ps 18:12 "thick clouds passed"
    'ncip': 'compass',           # Ps 49:5 "iniquity compass me about"
    
    # === More rare vocabulary from KJV cross-reference ===
    'serafim': 'seraphim',       # Isa 6:2 (Hebrew loanword)
    'kithukhat': 'rage',         # Ps 2:1 "why do the heathen rage"
    'phulet': 'pass',            # Ps 18:12 "thick clouds passed"
    'denkhap': 'dash.in.pieces', # Ps 2:9 "dash them in pieces"
    'kikhawlpa': 'companion',    # Ps 119:63 "I am a companion"
    'haltui': 'dross',           # Isa 1:25 "purge away thy dross"
    'guakbek': 'desolate',       # Ps 25:16 "I am desolate and afflicted"
    'suamlum': 'murder',         # Ps 94:6 "murder the fatherless"
    'lengsawn': 'hearing',       # Isa 11:3 "hearing of his ears"
    'meikhuka': 'hearth',        # Isa 30:14 "take fire from the hearth"
    'kultaltui': 'pitch',        # Isa 34:9 "streams turned into pitch"
    'taankhiat': 'shine.forth',  # Isa 62:1 "righteousness go forth as brightness"
    'sunletzo': 'bridle',        # Job 41:13 "his double bridle"
    'bunzo': 'pierce',           # Job 41:26 "sword cannot hold/pierce"
    'kithawithawi': 'be.raised', # Jer 6:22 "great nation shall be raised"
    'gimneih': 'fear',           # Ps 31:11 "a fear to mine acquaintance"
    'haipau': 'vile',            # Job 40:4 "I am vile"
    'hehmai': 'boldness',        # Eccl 8:1 "boldness of his face"
    'sesing': 'juniper',         # Ps 120:4 "coals of juniper"
    'huihkua': 'treasury',       # Ps 135:7 "wind out of his treasuries"
    'kiphawkmawh': 'pass.over',  # Prov 19:11 "pass over a transgression"
    'likto': 'lift.up',          # Isa 10:15 "staff should lift up itself"
    'gopa': 'slay',              # Isa 66:3 "killeth an ox is as if he slew"
    'mettom': 'utmost.corner',   # Jer 9:26 "in the utmost corners"
    'kiallai': 'be.satisfied',   # Isa 9:20 "they shall not be satisfied"
    'kheguak': 'barefoot',       # Isa 20:2 "walking naked and barefoot"
    'goih': 'visit',             # Jer 3:16 "neither shall they visit it"
    'lehlamin': 'upside.down',   # Isa 29:16 "turning of things upside down"
    'sunlum': 'reach',           # Jer 4:10 "sword reacheth unto the soul"
    'kiget': 'eunuch',           # Isa 56:3 "neither let the eunuch say"
    'beemlepang': 'provision',   # Ps 132:15 "abundantly bless her provision"
    'phialphiah': 'swallow',     # Ps 84:3 "swallow hath found a house"
    'hawktui': 'troubled',       # Prov 25:26 "troubled fountain"
    'dipkua': 'haste',           # Ps 48:5 "troubled, and hasted away"
    # Note: dipkuat (Form II) now in VERB_STEM_PAIRS
    'leikeu': 'dry.land',        # Ps 66:6 "turned the sea into dry land"
    'haihuaipi': 'vanity',       # Jer 10:15 "vanity, work of errors"
    'ngik': 'roar',              # Isa 5:30 "roar like the roaring of the sea"
    'lela': 'rejoice',           # Prov 13:9 "light of the righteous rejoiceth"
    # Note: 'khi' and 'ku' removed - too short, cause mis-segmentation
    'taat': 'bend',              # Ps 7:12 "bent his bow, made it ready"
    'kopkopin': 'chariot',       # Isa 21:7 "saw a chariot with horsemen"
    'meiizun': 'night.dew',      # Song 5:2 "locks with drops of the night"
    'logam': 'fruitful.place',   # Jer 4:26 "the fruitful place was a wilderness"
    'kisatnim': 'bruised',       # Isa 53:5 "he was bruised for our iniquities"
    'phusuakin': 'pass.on',      # Prov 22:3 "the simple pass on, and are punished"
    'guahciin': 'continual.drip', # Prov 19:13 "continual dropping"
    'dipkuasak': 'sprinkle',     # Isa 52:15 "so shall he sprinkle many nations"
    # Note: leilaka removed - conflicts with leilak-ah parsing
    'phitsan': 'hiss',           # Jer 19:8 "astonished and hiss"
    'dongsim': 'ask.secretly',   # Jer 37:17 "asked him secretly"
    'hailawh': 'be.mad',         # Jer 25:16 "drink, and be moved, and be mad"
    'kimap': 'live',    # Jer 38:17 "thy soul shall live"
    'khelkhiatsak': 'put.out.eyes', # Jer 39:7 "put out Zedekiah's eyes"
    'koizaw': 'stand',           # Jer 44:28 "whose words shall stand"
    'kiphamat': 'meet',          # Jer 51:31 "run to meet another"
    'taikhiasim': 'flee',        # Jer 52:7 "all the men of war fled"
    'kisuai': 'pomegranate',     # Jer 52:22 "network and pomegranates"
    'pekpak': 'swoon',           # Lam 2:12 "when they swooned as the wounded"
    'kimkotteng': 'brightness',  # Ezek 1:4 "brightness was about it"
    
    # === Session 4 Round 9: More verb stems for -sak causatives ===
    'khialh': 'err',     # khialhsak = cause to sin
    'piasak': 'cause.give',  # pia-sak = give-CAUS
    'siatsak': 'destroy',    # siat-sak = spoil-CAUS
    'khamsak': 'preserve',   # kham-sak = keep-CAUS
    'paikhiasak': 'send.away', # pai-khia-sak = go-out-CAUS
    'vaihawmsak': 'arrange', # va-i-hawm-sak = go.and-?-together-CAUS
    'zahhuaisak': 'triumph', # zah-huai-sak = fear-dread-CAUS
    'pungsak': 'increase',   # pung-sak = grow-CAUS
    'zuisak': 'follow.for',  # zui-sak = follow-CAUS
    'piaksak': 'give.for',   # piak-sak = give.to-CAUS
    'kangsak': 'raise.up',   # kang-sak = generation-CAUS
    'nopsak': 'please',      # nop-sak = willing-CAUS
    'nungsak': 'revive',     # nung-sak = live-CAUS
    'lungkhamsak': 'encourage', # lungkham-sak = courage-CAUS
    
    # === Session 5: Base verbs for ki- decomposition ===
    'nawh': 'hurry',         # kinawh = REFL-hurry
    'kholh': 'accompany',    # kikholh = REFL-accompany (be with)
    'lawi': 'dislocate',     # kilawi = REFL-dislocate (out of joint)
    'diah': 'dip',           # kidiah = REFL-dip (put in water)
    'khin': 'move',          # kikhin = REFL-move (set forward)
    'phah': 'spread',        # kiphah = REFL-spread (spread forth)
    'sut': 'spoil',          # kisut = REFL-spoil
    'nitsak': 'defile',      # kinitsak = REFL-defile
    'nit': 'defile',         # base for nitsak
    'phel': 'clear',         # kiphel = REFL-clear
    'tamzan': 'break.many',  # kitamzan = broken
    'hem': 'remove',         # hemkhia = remove-exit
    'meeng': 'branch',       # meengkhia = branch-exit
    'hazat': 'jealous',      # hazatna = jealousy
    'luang': 'flow',         # luangkhia = flow out
    'guta': 'destroyer',     # gutate = destroyers
    'tang': 'take.hold',     # kitang = take hold of each other
    'keek': 'tear',          # kikeek = be rent
    'lawh': 'spread',        # kilawh = spread
    'kalh': 'lock',          # kikalh = be locked
    'behlap': 'burden',      # kibehlap = be a burden
    'hotkhiat': 'save',      # kihotkhiat = be saved
    'thatlum': 'slay',       # kithatlum = be slain
    'lamdang': 'different',  # kilamdang = be different
    'tangval': 'young.man',  # tangvalte = young men
    'pil': 'learn',          # pilvang = be wise
    'mawh': 'guilty',        # Round 155: i mawh = we are guilty
    # Round 155: add commonly mis-segmented stems
    'zawng': 'poor',         # zawngkhal = wear.out
    'zawngkhal': 'tire.out', # tire/wear out
    'zanei': 'official',     # zanei = palace official/steward
    'zuihzawh': 'receive',   # zuihzawh = receive/accept (compound verb)
    'zuihkhak': 'obstruct',  # zuihkhak = obstruct following
    'zung': 'ring',          # zungbuh = signet ring
    'zungpi': 'chief.ring',  # large signet ring  
    'zungthuk': 'engraved.ring', # engraved ring
    'zukham': 'intoxicated', # zukhamna = drunkenness
    'zuauthei': 'liar',      # zuautheite = liars
    'zuauphuah': 'dark.saying', # understanding dark sentences
    'zelzel': 'repeatedly',  # again and again
    'zeek': 'account',       # give an account
    'zuahzuah': 'little.by.little', # reduplication meaning gradually
    'zualsakin': 'gradually', # another form
    'vum': 'breath',          # breath of
    'vokcing': 'swineherd',   # pig keeper
    'vankisut': 'proud',      # van-kisut = sky-lofty = proud
    'tuzaw': 'appointed.time', # at the appointed time
    'tuzawh': 'appointed.time', # variant
    'tunkhit': 'shut.in',     # trapped/enclosed
    'tunkhak': 'obstruct',    # block/obstruct
    'tulak': 'forest',        # wood country
    'ulenau': 'brethren',     # brothers/brethren
    'uplah': 'doubt',         # doubt
    'tuma': 'eloquent',       # able to speak
    'tukhang': 'this.generation', # from this generation
    'theu': 'cease',          # stop/satisfy
    'themcik': 'a.little',    # even a little
    'thawlpi': 'wine.vat',    # pressfat for wine
    'thawhbat': 'butter',     # smoother than butter
    'thanuam': 'diligent',    # hand of the diligent
    'thaneihteng': 'strength', # my strength
    'thakbawl': 'rejoice',    # rejoice over
    'tenkhak': 'dwell',       # sojourn/dwell
    'teeptum': 'drive.away',  # driven away
    'tawk': 'be.drunk',       # make drunk
    'tawizawh': 'spider',     # spider
    'tamkim': 'upright',      # uprightness
    'zongpa': 'wisdom',       # getteth wisdom
    'zingsol': 'morning.star', # morning star
    'uisan': 'glutton',       # winebibber/riotous eater
    'tuithuk': 'deep',        # the deep/abyss
    'tuikhukpi': 'pool',      # pools of water
    'tuikhu': 'fountain',     # fountain of the deep
    'tuibuak': 'water',       # water (verb - he that watereth)
    'tuatcil': 'trample',     # tread/trample
    'tuahpha': 'quickly',     # found so quickly
    # Note: tuahphat (Form II) now in VERB_STEM_PAIRS
    'vatmai': 'defeat',       # discomfit
    'valkhong': 'redeem',     # redeem the time
    'vawhzo': 'pierce',       # nose pierceth
    'vekun': 'shut.up',       # cities shut up
    'velval': 'bitter',       # become bitter
    'zinleleeng': 'temperate', # self-controlled
    'zinkhia': 'wander',      # wander from
    'zineih': 'wed',          # wife of youth
    'zik': 'wife',            # variant of zi (wife)
    'ziauziau': 'go.about',   # gad about
    'zavei': 'reproof',       # reproof
    'zahzahun': 'feathered',  # feathered fowl
    'zahkona': 'distress',    # distress
    'tovang': 'dig',          # dig in the wall
    'tomlam': 'count',        # number our days
    'tokgawpin': 'divide',    # divided the sea
    'thusit': 'condemn',      # condemn him
    'thusel': 'resist',       # resist
    'thuphawk': 'wise',       # wise men
    'thupalsat': 'transgressor', # transgressors
    'thunem': 'restore',      # restore
    'thuksak': 'plead',       # plead the cause
    'thukpi': 'flood',        # upon the flood
    'thukihilh': 'reproof',   # reproof/instruction
    'thuahkhawm': 'gather',   # gathered (figs)
    'then': 'thousand',       # thousands of
    'theipuam': 'herb',       # manner of herbs
    'thangtat': 'honest',     # walk honestly
    'thaltawi': 'archer',     # archers hit him
    'thalsing': 'myrrh',      # smell of myrrh
    'thalpeu': 'bend',        # bend their tongues
    
    # Round 164: Reduplication base verbs from remaining partials
    # NOTE: Short stems (di, ho, sen, cip, tup, hel) moved to COMPOUND_WORDS 
    # to prevent over-segmentation - they're only valid in reduplication context
    'lek': 'appear',          # appear/seem (leklek = appearing repeatedly)
    'gaih': 'grieve',         # lament/grieve (gaihgaih = grieving/lamenting)
    'kut': 'press',           # press/urge (kutkut = pressing urgently)
    'dua': 'quiet',           # be quiet/still (duadua = very quiet)
    'ngeu': 'shake',          # shake (ngeungeu = shaking)
    'vuau': 'pour.forth',     # pour forth (vuauvuau = poured forth)
    'viau': 'be.fragrant',    # be fragrant (viauviau = fragrant)
    'phang': 'stammer',       # stammer (phangphang = stammering)
    'hut': 'neigh',           # neigh (huthut = neighing)
    'gap': 'look.at.each.other',  # mutual gaze (gapgap = looking at each other)
    'thop': 'oppress',        # oppress/vex (thopthop = oppressing)
    'lit': 'pine.away',       # pine away/mourn (litlit = pining away)
    'giau': 'wait.upon',      # wait upon (giaugiau = waiting upon)
    
    # Round 164: Nominalization base verbs from remaining partials
    'ngolh': 'chasten',       # chasten/fast (ngolhna = chastening/fasting)
    'mangngilh': 'forget',    # forget (mangngilhna = forgetfulness)
    'niamsak': 'bow',         # bow/humble (niamsakna = humbling)
    'gilvah': 'be.satisfied', # be satisfied (gilvahna = satisfaction)
    'dimdiam': 'socket',      # socket/base (dimdiamna = sockets)
    'kinetniam': 'relieve',   # relieve oppressed (kinetniamna = relief)
    'meihal': 'burnt.offering', # burnt offering (meihalna = burnt offering)
    'kosiat': 'revile',       # revile/reproach (kosiatna = reviling)
    # kihen removed - parses as ki-hen = REFL-tie (be bound)
    'kolbulh': 'stocks',      # put in stocks (kolbulhna = stocks)
    'kilei': 'buy',           # buy (kileina = purchase)
    'hehsuah': 'provoke.jealousy', # provoke to jealousy (hehsuahna = jealousy)
    'kicip': 'breach',        # breach/gap (kicipna = breach)
    
    # Round 164 continued: More partials from KJV cross-reference
    'aisanna': 'familiar.spirit',  # familiar spirit/wizard (Lev 19:31)
    'naugil': 'door',              # door (of womb) - "shut not doors"
    'balgawp': 'die.naturally',    # die of itself/be torn
    'nikten': 'dust',              # dust (as the dust)
    'sawtta': 'great',             # great (number of days is great)
    'khawh': 'till',               # till the ground
    'nencip': 'compass',           # compass about
    'siahil': 'wonder',            # wonder (as a wonder to many)
    'lunggimhuai': 'painful',      # painful/difficult
    'sameh': 'provide',            # provide/give (bread, flesh)
    'ngal': 'leap',                # leap (have legs to leap)
    'palhin': 'flourish',          # flourish/sprout
    'lungsimmawl': 'brutish',      # brutish/foolish
    'khansihsak': 'take.away',     # take away
    'kinengniamte': 'oppressed',   # the oppressed (as noun)
    'meipi': 'fire',               # fire/large fire
    'meikuang': 'flaming',         # flaming (sword)
    'kamguh': 'speak.rashly',      # speak rashly/unadvisedly
    'khuaipi': 'bees',             # bees (like bees)
    'mitsuan': 'watch',            # watch/look on
    
    # Round 164 batch 3: More partials from KJV
    'kawma': 'chew',               # chew (ere it was chewed)
    'zaak': 'spread',              # spread (net is spread)
    'engkha': 'envy',              # envy/choose (envy thou not)
    'iplah': 'take',               # take (when ye take)
    'tangtawnga': 'beginning',     # beginning/old (of old)
    'cinasak': 'make.sick',        # make sick (maketh heart sick)
    'maitaisak': 'make.cheerful',  # make cheerful (cheerful countenance)
    'kidon': 'beaten',             # kido-n = fight-INV = "be beaten" (2x)
    'awklawh': 'snare',            # snare/get a snare
    'mitphiat': 'set.eyes',        # set eyes (set thine eyes upon)
    # NOTE: 'mana' removed - causes over-segmentation with manawh (direct toward)
    'omtual': 'dwelling',          # house/dwelling (house of mourning)
    'ngiano': 'fox',               # fox (the foxes)
    'khuto': 'pillar',             # pillar (pillars of smoke)
    'hialhial': 'twins',           # twins (that are twins)
    'lungzuangin': 'lovesick',     # sick of love
    'kikhawl': 'walk.with',        # walk with (walked with God)
    'keenhawm': 'cave',            # cave (caves of earth)
    'maiput': 'countenance',       # countenance (shew of countenance)
    'singbul': 'root',             # root (serpent's root)
    'nasiazaw': 'more',            # more/further (bring more)
    'patpuan': 'weave',            # weave (weave networks)
    'khansuah': 'bring.forth',     # bring forth (bring forth children)
    'keutumin': 'mourn',           # mourn/languish
    'mutgawp': 'drive.back',       # go back/drive back (caused sea to go back)
    'ciil': 'refined',             # refined (well refined)
    'migit': 'mercy',              # mercy (thy mercy)
    'kheuh': 'branch',             # branch (consume the branches)
    'manawh': 'direct.toward',     # direct toward / set face toward (35x)
    
    # Round 164 batch 4: More bases from -te plural forms
    # NOTE: 'zuau' removed - causes over-segmentation with zuauthu (lie/dissemble)
    # 'taina' removed - conflicts with other taina words
    'meiipi': 'leprous',           # leprous/cloud (became leprous, white as snow)
    'kisapna': 'need',             # need (what needeth it?)
    'leii': 'tongue',              # tongue (hide under tongue)
    'taksing': 'fir.tree',         # fir tree (fir trees)
    'suangmai': 'smooth.stone',    # smooth stone (five smooth stones)
    
    # Round 165: More stems from KJV cross-reference
    'kawikawi': 'to.and.fro',      # to and fro (went forth to and fro)
    'nengniami': 'deceive',        # deceive (hath deceived)
    'khawhletzo': 'barbed',        # barbed/speared (barbed irons)
    'ansite': 'chaff',             # chaff (be as chaff)
    'nipsak': 'settle',            # settle/soften (settlest/makest soft)
    'mizuau': 'deceitful',         # deceitful (lying lips, deceitful tongue)
    'ngaihbaan': 'fair',           # fair (very fair to look upon)
    'suanna': 'expectation',       # expectation/hope (hope of unjust men)
    'hauhpak': 'vanity',           # vanity (wealth gotten by vanity)
    'kanna': 'grey.hair',          # grey hair (beauty is grey head)
    'ciingin': 'fit',              # fit/keep (fitted in thy lips)
    'khataang': 'dim',             # dim/darkened (be not darkened)
    'gamsimtham': 'confusion',     # confusion (line of confusion)
    'palhkhia': 'blossom',         # blossom (blossom as rose)
    'saipa': 'steward',            # steward (over the house)
    'muangkha': 'trust',           # trust (make you trust)
    'pialpih': 'turn.aside',       # turn aside (turned him aside)
    'mibum': 'sorcerer',           # sorcerer (multitude of sorceries)
    'kikoih': 'restore',           # restore (me he restored)
    'satzan': 'loose',             # loose (loose the loins)
    'beellekuang': 'dish',         # dish/bowl (his dishes)
    'singtawng': 'stock',          # stock/tree trunk (saying to a stock)
    'khoppih': 'lie.with',         # lie with (been lien with)
    'maizumlawh': 'confounded',    # confounded (is confounded)
    'gammong': 'end',              # end (one end to the other)
    
    # Round 165 batch 2: More stems from KJV
    'sazuk': 'hind',               # hind/female deer (the hind calved)
    'mutmang': 'fan',              # fan/bereave (fan them with a fan)
    'mulkim': 'horrible',          # horrible (a very horrible thing)
    'maap': 'afterward',           # afterward/deliver
    'kibuluh': 'spoil',            # spoil (they that spoil thee)
    'loteng': 'field',             # field (all the fields)
    'sawtveipi': 'evidence',       # evidence (evidence of the purchase)
    'khapsa': 'promise',           # promise (that I have promised)
    'khahkhiatsa': 'let.go.free',  # let go free (let go free)
    'laitui': 'ink',               # ink (wrote them with ink)
    'ngawlin': 'evil',             # evil (have done evil)
    'noleno': 'cut.self',          # cut self (cut thyself)
    'bahgawp': 'fled',             # fled (fled because of force)
    'bangsakin': 'bring.again',    # bring again (bring again captivity)
    'innsia': 'desolate',          # desolate (become heaps)
    'hanciam': 'wrestle',          # wrestle (great wrestlings)
    'kauhkauh': 'tears',           # tears (tears on her cheeks)
    'lunggimnate': 'distress',     # distress (I am in distress)
    'tano': 'give.suck',           # give suck (give suck to young)
    'khepek': 'legs',              # legs (legs above their feet)
    'khupin': 'stretch',           # stretch (wings stretched upward)
    'khaging': 'noise',            # noise (noise of their wings)
    'khup': 'pit',                 # pit/close (went into the pit)
    'heuhau': 'amber',             # amber (colour of amber)
    'sitawm': 'die.of.itself',     # die of itself (that which dieth)
    'hihlohlam': 'in.vain',        # in vain (said in vain)
    'hua': 'garden',               # garden (planted a garden)
    'khazap': 'touch',             # touch (wings touched one another)
    'hawkkhiat': 'strip',          # strip (they stript Joseph)
    'guaih': 'reward',             # reward (givest a reward)
    'puanteng': 'nakedness',       # nakedness (discover thy nakedness)
    'dotnop': 'prosper',           # prosper (shall it prosper)
    
    # Round 166: High-frequency stems
    'huang': 'village',            # village/field (39x) - not same as hua (garden)
    'huan': 'garden',              # garden (huanah = garden-LOC) - 11x (overrides 'bread' compound)
    
    # Round 167: Hapax analysis stems - must be in VERB_STEMS for suffix parsing
    # NOTE: Short stems can cause over-segmentation conflicts. Resolution strategy:
    # - Add explicit COMPOUND_WORDS entries for high-frequency conflicting forms
    # - Longer compound matches take precedence over stem+suffix parsing
    'thak': 'new',                 # new/renew (bawlthak = make-new, khangthak = generation-new)
    'ngkawm': 'commit.adultery',   # adulterer (ngkawmte = adulterers, ngkawmna = adultery)
    # NOTE: psak removed - was creating invalid *ps onset. kipsak is ki-piak-sak contraction
    'ngek': 'tender',              # tender/tip (nongek = young ones, dawnngek = top/tip)
    'khip': 'veil',                # veil/cover (khipte = veils)
    'hop': 'snare',                # snare (duhhopna = desire-snare = temptation)
    # NOTE: psa removed - was creating invalid onset
    'mun': 'rare',                 # rare (genmun = rare word) - NOTE: also 'spot' in other contexts
    'dek': 'low',                  # low/cheap (sidek = low pit, sumdek = cheap)
    # Round 167h: More stems from partial-gloss analysis
    'em': 'bake',                  # bake (emna = bake-NMLZ, baking place)
    # 'zak' removed - it's a verb 'hear' (Form II of za), not a noun 'proclaim'
    'zaw': 'leap',                 # leap (kanzaw = 1SG-leap, sugawpzo/zaw compounds)
    'pial': 'stray',               # stray/err (pialsakin = stray-CAUS-ERG)
    'tai': 'rebuke',               # rebuke (tainate = rebuke-NMLZ-PL) - NOTE: short form, taii is full form
    'taii': 'rebuke',              # rebuke (taii-in = rebuke-ERG) - full form
    'isan': 'own',                 # own (naisan = 2SG-own)
    'tama': 'repair',              # repair (lettamate = return-repair-PL)
    'hin': 'life',                 # life/breath (hintheihna = life-know-NMLZ)
    'huam': 'possession',          # possession (khuapihuam = city-possession)
    'tawi': 'carry',               # carry/hold (167x) - a tawi = he carried
    # Round 167j: More stems from Gospel partials
    'zuih': 'follow',              # follow (galzuih = far-follow, nungzuih = behind-follow)
    'hual': 'roll',                # roll (hualin = roll-ERG)
    'kiim': 'border',              # border (khuakiim = town-border)
    
    # Round 190: Hapax verbs from KJV cross-reference
    'tukkhiat': 'pluck.off',       # 1x Gen 8:11 - olive leaf "pluckt off"
    'niamsuk': 'let.down',         # 1x Gen 24:18 - "let down her pitcher"
    # Note: tun (arrive) already in NOUN_STEMS line 4156 - tunpih = arrive-APPL = bring
    
    # === Lexicon internalization (2024-03-18) ===
    # Verbs from external ctd_lexicon.tsv
    'nasep': 'work',         # 345x
    'ngen': 'pray',          # 329x
    'phawk': 'remember',     # 328x
    'huh': 'help',           # 299x
    'khawm': 'gather',       # 252x
    'hal': 'burn',           # 173x
    'suan': 'plant',         # 171x
    'hanga': 'offer',        # 170x
    'dot': 'ask',            # 128x
    'lamtak': 'know',        # 82x
    'ten': 'dwell',          # 68x
    'kia': 'fall',           # 66x
    'lawng': 'touch',        # 57x
    'hetloin': 'fear',       # 56x - compound
    'tuh': 'sow',            # 29x
    'huhpa': 'helper',       # 26x - nominalized
    'din': 'stand',          # 23x
    'longal': 'save',        # 21x
    'phetun': 'hear',        # 18x
    'kisil': 'wash',         # 17x
    'phawkkha': 'remember',  # 17x
    'kuaitan': 'break',      # 15x
    'maw': 'see',            # 14x
    'boksuk': 'fall',        # 14x - compound
    'zuaupi': 'see',         # 14x
    'bok': 'fall',           # 13x
    'lencip': 'hold',        # 13x
    'dok': 'draw',           # 12x
    'kuaihtansak': 'break',  # 12x - causative
    'pulh': 'fall',          # 11x
    'tusuk': 'sit',          # 10x
    'huging': 'hear',        # 10x
    'lawngkha': 'touch',     # 8x
    'bua': 'pour',           # 8x
    'kipuaseh': 'cut',       # 5x
    'lehhei': 'turn',        # 3x
    'kitawng': 'strive',     # 15x - final lexicon internalization
    'tawng': 'contend',      # 13x - base verb (kitawng = ki- + tawng)
    
    # Additional verbs from corpus analysis (export POS consolidation)
    'tun': 'arrive',         # arrive at destination
    'pha': 'multiply',       # increase/branch
    'ging': 'believe',       # believe/trust
    'kal': 'go',             # go/walk
    'ning': 'think',         # think/consider
    'kulh': 'steal',         # steal/rob
    'kici': 'call.PASS',     # be called (ki-ci)
    'kicing': 'enough',      # enough/full/sufficient (64x) - distinct from kici
    'pah': 'do.so',          # do thus
    'tum': 'complete',       # complete/finish (also "all")
    'tuu': 'climb',          # climb/ascend
    'tawm': 'produce',       # produce/yield (also 'few')
    'do': 'rise',            # rise/rebel
    'san': 'flee',           # flee/escape
    'tho': 'rise',           # rise/awaken
    'dah': 'put',            # put/place
    'tuan': 'ride',          # ride/mount
    'het': 'trouble',        # trouble/disturb
    'kang': 'suffer',        # suffer/endure
    'pat': 'stroke',         # stroke/strike
    'hu': 'help',            # help/assist
    'puk': 'attack',         # attack/ambush
    'lel': 'escape',         # escape/desperate
    'ling': 'pile',          # pile/heap
    'khawl': 'rest',         # rest/cease
    'zat': 'use',            # use/employ
    'tel': 'know',           # know/understand
    'lawn': 'throw',         # throw/cast
    'dawi': 'fear',          # fear/be afraid
    'mong': 'hem',           # hem/edge
    'leng': 'wander',        # wander/roam
    'gan': 'bear',           # bear/carry (also 'cattle')
    'kan': 'stay',           # stay/remain
    'zin': 'travel',         # travel/journey
    # Note: zel is HAB.CONT suffix, not verb 'scatter'
    'sawh': 'correct',       # correct/rectify
    'hhuai': 'abominate',    # abominate/detest
    'kiat': 'fall',          # fall down
    'ing': 'be.able',        # be able/can
    'theh': 'throw',         # throw/hurl
    'kaih': 'lead',          # lead/guide
    'pelh': 'escape',        # escape/flee
    'zum': 'bow',            # bow/bend
    'vat': 'go.quickly',     # go quickly
    'vawh': 'call',          # call/name
    'thawh': 'rise',         # rise/get up
    'cina': 'sick',          # be sick
    'sawp': 'wrap',          # wrap/cover
    'khih': 'bind',          # bind/tie
    'sim': 'count',          # count/reckon
    'phu': 'carry',          # carry (on back)
    'kul': 'seal',           # seal/tar
    'thuah': 'gird',         # gird/wrap
    'gol': 'divide',         # divide/separate
    'ip': 'cover',           # cover/hide
    'neng': 'oppress',       # oppress/press
    'gawh': 'touch',         # touch/contact
    'zal': 'spread',         # spread out
    'khek': 'change',        # change/exchange
    'taan': 'withhold',      # withhold/restrain
    'mut': 'see',            # see/perceive
    'met': 'shear',          # shear/cut
    'vet': 'do',             # do/act
    'lom': 'wave',           # wave/shake
}






# Noun stems - expanded from corpus frequency analysis
NOUN_STEMS = {
    # Divine/Religious (high frequency in Bible)
    # Note: Pasian, Topa, Lungdamna moved to PROPER_NOUNS
    'pasian': 'god',         # lowercase variant for compounds
    'topa': 'lord',          # lowercase variant for compounds
    'biakna': 'worship',     # 1,236 biak-na
    'biakinn': 'temple',     # 741 biak-inn
    'siangtho': 'holy',      # 476
    'thupha': 'blessing',    # 479 thu-pha
    'mawhna': 'sin',         # 688 mawh-na
    # Lungdamna moved to PROPER_NOUNS
    'nuntakna': 'life',      # 394 nuntak-na
    'thuciamna': 'promise',  # 374 thuciam-na
    'vangliatna': 'power',   # 282
    'thukham': 'law',        # 210
    
    # Social terms
    'mi': 'person',          # 4,221
    'minam': 'nation',       # 596
    'mihing': 'human',       # 354
    'kumpipa': 'king',       # 1,563
    'kumpi': 'king',
    'siampi': 'priest',      # 357
    'siampipa': 'high.priest', # 172
    'nasempa': 'servant',
    'kicial': 'hired',       # 18x - hired servant (kicial nasempa)
    'gal': 'enemy',          # enemy/war (base stem for galte, galkap, galmi, etc.)
    'galkap': 'soldier',     # 233
    'galhiam': 'adversary',  # 50x - man of war / opponent
    'galhang': 'warrior',    # 39x - man of war
    'galkhat': 'battle',     # 36x - war-strike (battle)
    # galkah moved to BINARY_COMPOUNDS as gal-kah (war-fight = warfare)
    'galdo': 'campaign',     # 32x - go forth to war
    'galvil': 'war.camp',    # 16x - military camp
    'galvan': 'armour',      # 9x - war equipment
    'galmatin': 'overthrown', # 17x - war-defeat (undone by war)
    'kamsang': 'prophet',
    'kamtai': 'messenger',
    'upa': 'elder',          # 162
    'mihon': 'poor.person',  # 216
    'midang': 'other.person', # 181
    'migilo': 'enemy',       # 179
    
    # Kinship
    'pa': 'male',          # 2,265 - male kinship term (father/son depending on context)
    'nu': 'female',          # 619 - female kinship term (mother/daughter depending on context)
    'tapa': 'son',           # 1,906
    'tanu': 'daughter',
    'sanggam': 'brother',     # Opaque lexeme (not sang+gam compound)
    'sanggampa': 'brother',  # 210
    'zi': 'wife',            # 339
    'pasal': 'husband',      # 359
    'mipa': 'man',
    'numei': 'woman',
    'suanlekhak': 'genealogy', # 224
    'innkuan': 'household',  # 205
    
    # Body parts
    'khut': 'hand',          # 854
    'khutsung': 'palm',      # 158
    'mai': 'face',
    'maitang': 'forehead',   # 137
    'lungsim': 'heart',      # 957 lung-sim
    'kha': 'spirit',         # 748
    'sa': 'flesh',           # 573
    'lu': 'head',
    'ke': 'foot',
    'mit': 'eye',
    'bil': 'ear',
    'kam': 'mouth',           # kam = mouth (NOT ka)
    
    # Place/Location
    'gam': 'land',           # 2,586
    'khua': 'town',          # 919
    'khuapi': 'city',        # 1,050
    'inn': 'house',          # 715
    'mun': 'place',          # 820
    'mung': 'place',         # variant form
    'kal': 'middle',         # middle/between - enables ki-kal = REFL-middle = between
    'nun': 'knop',           # decorative bud on lampstand (KJV "knop") - 16x
    'leitung': 'earth',      # 717
    'leitang': 'earth',      # 462 (variant)
    'vantung': 'heaven',     # 419
    'vantungmi': 'angel',    # 247
    'lampi': 'way',
    'van': 'sky',            # 227
    'mual': 'mountain',      # 283
    'mualtung': 'mountaintop', # 202
    'tuipi': 'sea',          # 270
    
    # Time terms
    'hun': 'time',           # 1,208
    'ni': 'day',             # 1,191
    'kum': 'year',           # 868
    'zan': 'night',
    'zing': 'morning',       # Round 155: add morning (prevents zi-ng mis-segmentation)
    'zingsang': 'morning',   # full form
    'tawntung': 'forever',   # 679
    'nisuah': 'birth.day',   # 169
    'khang': 'generation',   # 213
    
    # Abstract terms
    'thu': 'word',           # 5,516
    'thuthak': 'truth',
    'thuhilhna': 'teaching',
    'thupiak': 'commandment', # 241
    'thupiakna': 'commandment.NMLZ', # 184
    'tui': 'water',
    'aw': 'voice',
    'min': 'name',
    'nam': 'kind',     # 177
    'mawhnei': 'sinner',     # 24x - mawh (guilty/sin) + nei (have) = sin-having
    
    # Other common nouns
    'ngeina': 'knowledge',   # 327 ngei-na
    'siatna': 'destruction', # 350 siat-na
    'khialhna': 'sin',       # 328 khialh-na
    'gamtatna': 'kingdom',   # 300 gamtat-na
    'sihna': 'death',        # 268
    'deihna': 'desire',      # 244
    'pilna': 'learning',     # 227
    'hehpihna': 'wrath',     # 225
    'nasepna': 'work.NMLZ',  # 174
    'ngaihsutna': 'thought', # 175
    'ukna': 'rule.NMLZ',     # 138
    'upna': 'belief',        # 258
    'itna': 'love.NMLZ',     # 299
    'hoihna': 'goodness',    # 108
    'lum': 'warm',           # 149
    'puan': 'cloth',         # 168
    'beh': 'tribe',          # 173
    'omlai': 'dwelling',     # 236
    'lote': 'non-X',         # 230
    'milim': 'idol',         # 230
    'khuavak': 'light',      # 188
    'khuamial': 'darkness',  # 123x - atmosphere-dark → darkness (parallel to khuavak)
    'sakol': 'donkey',       # 155
    'anlum': 'food',         # 145
    'ganhing': 'animal',     # 164
    'gankhahna': 'pasture',  # 3x - "pasture" (gan=animal + khah=tend + na=NMLZ)
    'sang': 'high',          # 209
    'nin': 'day',            # 200 variant
    'bawng': 'cattle',       # 31x + many compounds (bawngtal, bawngpi, etc.)
    'tuuno': 'lamb',         # 127x - young sheep (Gen 22:7, 2 Sam 12:6)
    'ganbuk': 'fold',        # animal fold/pen
    'kilungso': 'wait.patiently',  # rest in the LORD
    'phuang': 'upright',     # perfect/upright
    # kidona removed - parses transparently as ki-don-a = REFL-war-LOC = "battle"
    'sakhital': 'hart', # 4x - deer species
    'tuzum': 'harrow',       # 2x - farming tool
    'khuahun': 'season',     # 2x - khua (town/weather) + hun (time)
    
    # === Rare word stems (from KJV cross-reference) ===
    # Discovered via synoptic parallel analysis
    'nneng': 'crumb',        # annengte = 3SG-crumb-PL (Matt 15:27, Luke 16:21)
    'nkungno': 'rootless',   # ankungnote = scorched/no root (Matt 13:6, Mark 4:6)  
    'nhai': 'gluttonous',    # anhai = 3SG-gluttonous (Matt 11:19, Luke 7:34)
    'lsak': 'salt',   # alsakkik = salt losing savour (Matt 5:13, Mark 9:50)
    'phung': 'plain',   # 41x - plain, or fort/siege-tower (context-dependent)
    
    # === Additional stems from corpus frequency analysis ===
    # Social/occupational
    'tangval': 'youth',       # tangvalte = youths
    'naupang': 'child',       # naupangte = children
    'luang': 'corpse',
    'nungak': 'girl',        # 73
    'tuuhon': 'poor.person', # tuuhonte
    'mihoih': 'righteous',   # 70
    'mihai': 'wise',         # 89
    'misi': 'dead',          # 70
    'mihonpi': 'noble',      # mihonpite
    
    # Nominalizations (productive -na pattern)
    'lamet': 'example',      # lametna = example.NMLZ
    'phattua': 'reward',     # phattuamna
    'haksat': 'difficult',   # haksatna
    'gualzawh': 'transgress', # gualzawhna
    'tawntung': 'eternity',  # tawntungna
    'mahmah': 'very',        # mahmahna
    'pian': 'birth',         # pianna
    'lut': 'enter',          # lutna
    'neih': 'have',          # neihna
    'muh': 'see',            # muhna
    'lau': 'fear',           # launa
    'lawm': 'worthy',        # kilawm (258x) = REFL-worthy = be fitting/suitable
    'kah': 'fight',          # kahna
    'lin': 'hope',           # lina
    'sik': 'repent',         # sikna
    'dik': 'straight',       # dikna
    'hat': 'strong',         # hatna
    'dal': 'hinder',         # dalna
    'buk': 'ambush',         # bukna
    
    # Places/locations
    'mailam': 'front',       # 64
    'mualtung': 'mountaintop', # mualtungah
    'zawl': 'open.space',    # zawlte
    'gamla': 'wilderness',   # 57
    # Note: gamlat (Form II) now in VERB_STEM_PAIRS
    'meikhuk': 'furnace',    # 27x - meikhukah = furnace-LOC (mei=fire + khuk=place)
    
    # Body parts / objects
    'lukhu': 'crown',        # 59
    'kongzing': 'harp',      # 59
    'kammal': 'jawbone',     # 59
    'vatgawp': 'bird',       # 55
    'mittaw': 'blind',       # 47
    'sum': 'money',          # sumte
    'kent': 'cubit',         # kente
    'leeng': 'chariot',      # leengte = 68
    'bawngtal': 'ox',        # bawngtalte = oxen 212x
    'sabuai': 'sheep',       # 60
    'sawltak': 'servant',    # 56
    'khuaizu': 'locust',     # 60
    'nak': 'nose',           # 77x - "nostrils, nose" (NOT na-k!)
    'ngasa': 'fish',         # 62x - "fish"
    'lungsim': 'heart',      # 57x - "heart, bowels, inner being"
    
    # Action-related
    'khaici': 'sow',         # 58 (farmer)
    'kamsangpa': 'prophet',  # 58
    'vaihawm': 'counsel',    # 63
    'muanhuai': 'trust',     # 57
    'minthang': 'glory',     # 57
    'thusim': 'parable',     # 60
    'thuhoih': 'good.news',  # 47
    'laksak': 'redeem',      # 54
    'ninsak': 'strengthen',  # 52
    'lungdamsak': 'comfort', # 50
    'nusia': 'forsake',      # 50
    'musak': 'show',         # 46
    
    # Plurals (productive -te pattern)
    'sagih': 'seven',        # sagihte
    'sawmgiat': 'seventy',   # 55
    'zathum': 'three.hundred', # 52
    'zali': 'four.hundred',  # 51
    'zawsop': 'judge',       # 52
    'ukpi': 'governor',      # 53
    'siamte': 'craftsmen',
    'ante': 'them',          # 50
    'pente': 'things',
    'khete': 'some',
    'khaute': 'which',
    'suangte': 'descendants',
    'bawlte': 'makers',
    'pute': 'ancestors',
    'taute': 'children',
    'humpinelkai': 'lion',   # 125x - "lion"
    'nuamsa': 'prosperous',  # 51x - "well, prosperous, at ease"
    
    # Miscellaneous high-frequency
    'ken': 'only',           # 112
    'panun': 'toward',       # 101
    'mudah': 'easy',         # 97
    'paisan': 'god',         # 91 variant spelling
    'annel': 'meal',         # 76
    'alang': 'side',         # 73 - NOT vine! "in the side thereof"
    'kangtum': 'brass',      # 72
    'kawm': 'edge',          # 70
    'keel': 'heel',          # 85
    'zaguk': 'winepress',    # 65
    'umcih': 'hope',         # 64
    'ihih': 'this.be',       # 64 = i-hih
    'letsong': 'gift',       # 76x - "gift, portion"
    'baih': 'early',         # 49x - "early" (in 'tho baih' = rise early)
    'cin': 'said',           # 61
    'kampau': 'voice',       # 61
    'hit': 'that',           # 61
    'khai': 'hold',          # 61
    'keu': 'dig',            # 59
    # Note: khuat='dig.II' removed - conflicts with khua-te (town-PL)
    'maimang': 'shame',      # 59
    'khah': 'choke',         # 62
    'nakleh': 'otherwise',   # 56
    'hiang': 'know',         # 54
    'khialh': 'sin',         # 54
    'sau': 'long',           # 52
    'luppih': 'lay.down',    # 51
    'lungmuang': 'trust',    # 51
    'lunghimawh': 'fear',    # 51
    'samsia': 'destroy',     # 50
    'pianzia': 'nature',     # 50
    'gammi': 'citizen',      # 47
    'namkim': 'rainbow',     # 46
    'sauveipi': 'flock',     # 46
    'mipil': 'wise.person',  # 47
    'aksi': 'star',          # 48x - "star" (vana aksi = star of heaven)
    'lutang': 'head-leader', # 56x - "duke, chief" (lu=head + tang=leader)
    'ciatah': 'each',        # 48x - "each, every"
    'tuam': 'promise',       # base for phattuamna, tuamtuam
    'guh': 'bone',           # 44x - "bone" (guhte = bones)
    'liat': 'great',         # 44x - "great, much" (liatna = greatness)
    # kapin: removed - actually kap-in "weep-ERG" in 89% of cases (39/44)
    # The one "among" case (Judg 20:16) is unclear and may be compositional
    'innkuanpih': 'household', # 46x - "household" (inn-kuan-pih)
    # khuampi moved to BINARY_COMPOUNDS as khuam-pi (pillar-great)
    'ngawng': 'neck',        # 43x - "neck"
    'ngaihno': 'beloved',    # 42x - "beloved" (O thou whom my soul loveth)
    'et': 'care',            # 41x - base for etna (caring, keeping)
    'nget': 'request',       # 41x - base for ngetna (request, petition)
    'kiman': 'profit',       # 41x - base for kimanna (profitable)
    'kimang': 'profit',      # 68x - variant of kiman (what profit)
    'maangmuh': 'vision',    # 42x - base for maangmuhna (vision)
    # tuikulh moved to BINARY_COMPOUNDS as tui-kulh (water-surround = island)
    'puantualpi': 'robe',  # 40x - "coat of many colors"
    
    # === na- words that are NOT 2SG prefix! ===
    # These are independent lexemes, not na- + X
    'nasem': 'servant',      # 350x - "servant, young man" (NOT 2SG-serve)
    'nasia': 'severe',       # 60x - "severe, great, terrible" (NOT 2SG-bad)
    'nalamdang': 'miracle',  # 76x - "miracle, wonder, sign" (NOT 2SG-way-other)
    'naita': 'near',         # 36x - "near, approaching" (NOT 2SG-love)
    'natui': 'discharge',    # 22x - "bodily discharge, issue" (NOT 2SG-water)
    'naupa': 'younger.sibling', # 21x - "younger brother/sibling" (NOT 2SG-elder)
    'nakpi': 'night',        # 42x - "night" (NOT 2SG-big)
    
    # Additional stems for compound parsing
    'sia': 'evil',           # siate = evil-PL; also 'bad' in siapa (elder)
    'suah': 'birth',         # nisuah = day-birth = birthday
    'pul': 'tremble',        # pulnat = tremble-hurt = terror
    'sin': 'near',           # sinte = near-PL
    'giah': 'camp',          # giahte = camp-PL
    
    # === Session 2: More noun stems from philological analysis ===
    'hiang': 'branch',       # 41x - "branch" (a hiangte = its branches)
    'ausan': 'scarlet',      # 39x - "scarlet (color)" (a ausan puante = scarlet cloths)
    'luanghawm': 'carcass',  # 39x - "carcass, corpse" (humpinelkai luanghawm = lion carcass)
    'gamkhing': 'desolate',  # 38x - "desolate, empty land"
    # bawngno moved to BINARY_COMPOUNDS as bawng-no (cattle-young = calf)
    'thumvei': 'three.times', # 36x - "three times" (thum + vei)
    'vakhu': 'dove',         # 35x - "dove"
    'khualzin': 'journey',   # 35x - "journey, travel" (khua + zin)
    'manna': 'manna',        # 35x - biblical manna (loanword)
    'cingtaak': 'dwarf',     # 35x - "dwarf, short person"
    
    # === Session 2: More nouns from philological analysis ===
    'kammal': 'word', # 38x - "word, speech" (kammalte = words)
    'kampau': 'voice',       # used in kampauna (voice-NMLZ)
    'gamhluah': 'heir',      # 35x - "heir" (gam-hluah = land-inherit)
    'tunna': 'end',   # 35x - "end, border" (Jordan tunna = end of Jordan)
    'omzia': 'welfare',      # 34x - "welfare, condition" (om-zia = exist-manner)
    'tual': 'place', # base for puantualpi
    
    # === Session 3: More nouns from philological analysis ===
    'kongkha': 'door',       # 38x - "door" (kongkhakte = doors)
    'pawl': 'group',  # 33x - "group, companions, allies"
    'kauphe': 'locust',      # 33x - "locust" (kauphe hon = locusts)
    'beel': 'pan',      # 33x - "pan, bowl" (beelte = pans)
    'khak': 'offspring',     # 34x - "offspring, generation" (a khakte = his generations)
    'sunga': 'inside',       # 34x - "inside, in" (khuasunga = in the town)
    'sing': 'tree',     # 33x - "tree, wood" (singte = trees)
    'singkung': 'tree',      # 32x - "tree" (singkungte = trees) - fuller form
    'nuam': 'pleased',       # 32x - "pleased, comfortable" (lungnuam = heart-pleased)
    'hon': 'flock',    # 31x - "flock, swarm" (honpi = great multitude)
    'khat': 'one',           # numeral "one"
    'lang': 'side',          # "side" (langkhat = one side, langpang = against)
    'mial': 'darkness',      # 31x - "darkness" (khua mial = darkness)
    'dang': 'other',         # "other" (nidang = day-other = before)
    'ham': 'full',           # "full" (khangham = full of years)
    'an': 'food',       # 30x - "rice, food" (anlak = harvest)
    'ai': 'lot',        # lot for casting/divination (ai san = cast lots)
    'nawi': 'butter',        # "butter" (bawngnawi = cow-butter)
    'kalaoh': 'camel',       # 30x - "camel" (kalaohte = camels)
    'liangko': 'shoulder',   # 29x - "shoulder"
    'phaknat': 'leprosy',    # 31x - "leprosy" (skin disease)
    'no': 'young',           # "young" (khangno = youngest)
    'aksi': 'star',          # 32x - "star" (aksite = stars)
    'aisan': 'magician',     # 29x - "magician, sorcerer"
    'ukpi': 'duke',          # 29x - "duke, chief"
    'lungtang': 'breastplate', # 29x - "breastplate" (lung-tang = heart-place)
    'sila': 'servant',       # 29x - "servant, slave"
    'zineu': 'concubine',    # 28x - "concubine" (zi-neu = wife-lesser)
    'lim': 'sign',           # 29x - "sign" (limte = signs)
    'mangbuh': 'barley',     # 28x - "barley"
    'kuang': 'trough',   # 28x - "trough, box" (kuangte = kneadingtroughs)
    'thau': 'fat',           # 27x - "fat" (thaute = fats)
    'thaltang': 'arrow',     # 27x - "arrow" (thaltangte = arrows)
    'cing': 'faithful',      # 33x - "faithful" (cingte = faithful ones)
    'si': 'die',             # verb "die" (si ding = shall die)
    'sim': 'count',          # 356x - verb "count, number"
    'silh': 'clothe',        # 116x - verb "clothe"
    'siang': 'holy',         # 114x - adjective "holy" (base of siangthosak)
    'lianpi': 'army',        # 27x - "army" (lianpite = armies)
    'peengkul': 'trumpet',   # 27x - "trumpet"
    'lai': 'middle',     # 26x - "tip, middle" (laite = tips)
    'lasa': 'pillar',        # 26x - "pillar" (lasate = pillars)
    'sisan': 'blood',        # 135x - "blood"
    'laibu': 'book',         # 121x - "book" (laibu ahi hi = the book of)
    'silngo': 'feast',  # 78x - "meal, feast" (unleavened bread context)
    
    # === Session 6 Round 11: Allomorph audit additions ===
    # Stems needed to prevent over-segmentation with -te suffix
    'hing': 'alive',         # hingte = alive-PL
    'vun': 'skin',           # vunte = skin-PL
    'thal': 'bow',           # thalte = bow-PL (weapon)
    'taneu': 'child.small',  # taneute = little ones
    'teipi': 'spear',        # teipite = spears
    'hisak': 'proud',        # kihisakte = proud ones
    'gial': 'spotted',       # gialte = spotted ones
    'anpal': 'firstfruit',   # anpalte = firstfruits
    'vanglian': 'mighty',    # vangliante = mighty ones
    'pawi': 'feast',         # pawite = feasts
    'delh': 'overcome',      # delhte = conquerors  
    'zuak': 'sell',          # zuakte = sellers
    
    # === Round 190: Hapax vocabulary from KJV cross-reference ===
    'tapeeng': 'twins',      # 1x Gen 25:24 - "twins in her womb"
    'bemeh': 'lentils',      # 1x Gen 25:34 - "pottage of lentiles"
    'khaleh': 'perhaps',     # 1x Gen 24:5 - "Peradventure" (what if)
    'moken': 'dowry',        # 1x Gen 30:20 - "good dowry"
    'thacial': 'wages',      # 1x Gen 30:18 - "my hire/wages"
    'tausangpi': 'tower',    # 1x Gen 11:5 - "tower" (tau-sang-pi = ?-high-big)
    'lanu': 'she.ass',       # 1x Gen 12:16 - "she asses" (la-nu = donkey-female)
    'zual': 'wild',          # 1x Gen 16:12 - "wild man"
    'lehkhak': 'shut',       # 1x Gen 19:6 - "shut the door"
    'manlang': 'hastily',    # 36x - "hastily, quickly" (manlangin = hastily-ERG)
    'daitui': 'dew',         # 1x Gen 27:39 - "dew of heaven" (dai-tui = ?-water)
    'kheh': 'peel',          # 1x Gen 30:37 - "pilled/peeled" (strakes)
    'khehsa': 'peeled',      # 1x Gen 30:38 - "peeled rods" (kheh-sa = peel-PERF)
    'bungsuk': 'pour.out',   # 1x Gen 24:20 - "emptied her pitcher"
    'innlelo': 'homeless',   # 2x Ps 68:6 - "solitary in families" (inn-lelo = house-less)
    'sumkhek': 'moneychanger', # 2x Mark 11:15 - "moneychangers" (sum-khek = money-change)
    'angtanpih': 'pride',    # 2x Ps 47:4 - "excellency" (pride/glory)
    'anhai': 'gluttonous',   # 2x Matt 11:19 - "gluttonous" (an-hai = food-greedy)
    'neel': 'smooth',        # 1x Gen 27:16 - "smooth of his neck"
    'phawng': 'hunting',     # 1x Gen 49:9 - (lion hunting context)
    'balzan': 'torn.by.beasts', # 1x Gen 31:39 - "torn of beasts"
    'supna': 'loss',         # 1x Gen 31:39 - "I bare the loss" (supnate = losses)
    # suangkhuam moved to BINARY_COMPOUNDS as suang-khuam (stone-pillar)
    'pomcip': 'embrace',     # 1x Gen 33:4 - "embraced" (pom-cip = hug-tight)
    'lungphamawh': 'weak',   # 1x Gen 33:13 - "tender" (lung-pha-mawh = heart-good-not)
    'naudom': 'childbirth',  # 1x Gen 35:17 - "hard labour" in childbirth
    'mavansak': 'prosper',   # 1x Gen 39:3 - "made to prosper"
    'mohlawh': 'whitebread', # 1x Gen 40:16 - "white baskets/bakemeats"
    'theem': 'blasted',      # 1x Gen 41:23 - "blasted with east wind"
    'kamphen': 'interpreter', # 1x Gen 42:23 - "interpreter between them"
    'pistakhio': 'pistachio', # 1x Gen 43:11 - pistachio nuts (loanword)
    'suakmasa': 'firstborn', # 1x Gen 43:33 - "firstborn" order (suak-masa = born-first)
    'moilai': 'youngest',    # 1x Gen 44:20 - "child of old age" (youngest)
    'mawkval': 'waste',      # 1x Gen 47:19 - "why should we die/waste"
    'kipaihpehsak': 'cross.hands', # 1x Gen 48:14 - "guiding his hands wittingly"
    
    # === Round 190b: More hapax from KJV cross-reference ===
    'khelkom': 'thigh.hollow', # 1x Gen 32:25 - "hollow of his thigh"
    'khelpi': 'thigh',       # 1x Gen 32:31 - "halted upon his thigh"
    'bom': 'blossom',        # 1x Gen 40:10 - "blossoms shot forth"
    'domsak': 'midwife',     # 1x Exod 1:15 - "midwives" (dom-sak = birth-help)
    'nausuah': 'birthstool', # 1x Exod 1:16 - "upon the stools" (nau-suah = child-emerge)
    'phansak': 'daub',       # 1x Exod 2:3 - "daubed with slime/pitch"
    'kitap': 'anguish',      # 1x Exod 6:9 - "anguish of spirit"
    'mangbuhman': 'wheat',   # 1x Exod 9:32 - "wheat and rie"
    'innzom': 'neighbor',    # 1x Exod 12:4 - "neighbour next unto his house"
    'mehteh': 'bitter.herbs', # 1x Exod 12:8 - "with bitter herbs"
    'kithamuan': 'triumph',  # 1x Exod 14:8 - "triumphed gloriously"
    'dimval': 'excess',      # 1x Exod 16:18 - "had nothing over"
    'dimlah': 'lack',        # 1x Exod 16:18 - "had no lack"
    'mawhzon': 'quarrel',    # 1x Exod 17:7 - "chiding/quarreling"
    'vanging': 'thunder',    # 1x Exod 20:18 - "thunderings"
    'tupkhiat': 'knock.out', # 1x Exod 21:27 - "smite out tooth"
    'piklup': 'gore',        # 1x Exod 21:28 - "ox gore" (horn-pierce)
    'leetkhia': 'firstfruit', # 1x Exod 22:29 - "first of ripe fruits"
    'lokhul': 'fallow',      # 1x Exod 23:11 - "let it rest" (lo-khul = field-rest)
    'suangphahpek': 'pavement', # 1x Exod 24:10 - "paved work of sapphire"
    'bangpian': 'as.if',     # 1x Exod 24:10 - "as it were"
    'liangkaih': 'join',     # 1x Exod 28:7 - "joined at the edges"
    'guklam': 'steal',       # 1x Gen 31:32 - "Rachel had stolen them"
    'kibangmah': 'likewise', # 1x Gen 32:19 - "on this manner"
    'kinenniam': 'afflict',  # 1x Exod 1:12 - "the more they afflicted"
    'kibatloh': 'differ',    # 1x Exod 1:19 - "not as the Egyptian women"
    'kuangzawn': 'trough',   # 1x Exod 2:16 - "filled the troughs"
    'dengtan': 'smite',      # 1x Exod 9:25 - "hail smote"
    'masiah': 'before',      # 1x Exod 10:14 - "before them/beforetime"
    'vuhsak': 'bore.through', # 1x Exod 21:6 - "bore his ear"
    'bakbak': 'ravin',       # 1x Gen 49:27 - "ravin as a wolf" (reduplication)
    'khawilevulh': 'womb',   # 1x Gen 49:25 - "blessings of the womb"
    'tuipiakna': 'watering.trough', # 1x Gen 30:38 - "watering troughs"
    'puangin': 'speckled',   # 1x Gen 31:10 - "ringstraked, speckled, grisled"
    
    # === Round 190c: Leviticus/Numbers hapax ===
    'khuangbai': 'bald.locust', # 1x Lev 11:22 - "bald locust"
    'innhikpi': 'weasel',    # 1x Lev 11:29 - "weasel"
    'tawlbawkpi': 'ferret',  # 1x Lev 11:30 - "ferret/lizard"
    'tangteuh': 'chameleon', # 1x Lev 11:30 - "chameleon"
    'tol': 'bald',           # 1x Lev 13:40 - "bald head"
    'puankek': 'torn.clothes', # 1x Lev 13:45 - "clothes rent"
    'kizutna': 'mortar',     # 1x Lev 14:45 - "morter of the house"
    'saanin': 'cast.lots',   # 1x Lev 16:8 - "cast lots" (saa-nin?)
    'kisunen': 'beaten',     # 1x Lev 16:12 - "beaten sweet incense"
    'hawkmai': 'glean',      # 1x Lev 19:10 - "glean thy vineyard"
    'thukan': 'scourging',   # 1x Lev 19:20 - "scourging"
    'kinailua': 'confusion', # 1x Lev 20:12 - "wrought confusion"
    'nawlhui': 'beard.corner', # 1x Lev 21:5 - "corner of beard"
    'kisunna': 'anointing',  # 1x Lev 21:10 - "anointing oil poured"
    'khelbai': 'lame',       # 1x Lev 21:18 - "a lame man"
    'elkul': 'hunchback',    # 1x Lev 21:20 - "crookbackt"
    'tomlua': 'superfluous', # 1x Lev 22:23 - "superfluous/lacking"
    'lonawl': 'field.corner', # 1x Lev 23:22 - "corners of thy field"
    'singhiangpi': 'palm.branch', # 1x Lev 23:40 - "branches of palm trees"
    'gialhek': 'willow',     # 1x Lev 23:40 - "willows of the brook"
    'tensak': 'cause.dwell', # 1x Lev 23:43 - "made to dwell in booths"
    'kisuzan': 'pressed',    # 1x Lev 24:2 - "olive beaten/pressed"
    'anlui': 'old.store',    # 1x Lev 25:22 - "old fruit/store"
    'tuat': 'reckon',        # 1x Lev 25:52 - "count with him"
    'dingtang': 'upright',   # 1x Lev 26:13 - "go upright"
    'tawiteh': 'by.weight',  # 1x Lev 26:26 - "deliver by weight"
    'kiphupai': 'stumble',   # 1x Lev 26:37 - "fall one upon another"
    'pelhzah': 'abhor',      # 1x Lev 26:44 - "will not abhor them"
    'nengneng': 'pin',       # 1x Num 3:36 - "pins" (reduplication)
    'meikhuam': 'candlestick', # 1x Num 4:9 - "candlestick of the light"
    'luakkhia': 'remove.ashes', # 1x Num 4:13 - "take away ashes"
    'tomkhano': 'moment',    # 1x Num 4:20 - "when covered" (tom-kha-no)
    'tuuvun': 'badger.skin', # 1x Num 4:25 - "badgers' skins"
    'phawkkik': 'memorial',  # 1x Num 5:18 - "memorial offering"
    # NOTE: 'teem' and 'teemsak' removed - conflict with teembaw (ark, 124x)
    
    # === Round 190d: Exodus/Leviticus hapax ===
    'kizim': 'hole',         # 1x Exod 28:32 - "hole in the top"
    'kihelhsak': 'alternate', # 1x Exod 28:34 - "bell and pomegranate"
    'pheituam': 'linen.breeches', # 1x Exod 28:42 - "linen breeches"
    'sabak': 'inwards',      # 1x Exod 29:17 - "inwards and legs"
    'stak': 'stacte',        # 1x Exod 30:34 - spice (loanword)
    'onikha': 'onycha',      # 1x Exod 30:34 - spice (loanword)
    'galbanum': 'galbanum',  # 1x Exod 30:34 - spice (loanword)
    'tunsuk': 'delay',       # 1x Exod 32:1 - "Moses delayed"
    'takhialsak': 'make.naked', # 1x Exod 32:25 - "made them naked"
    'phiatmai': 'blot.out',  # 1x Exod 32:32 - "blot me out"
    'tungnun': 'find.grace', # 1x Exod 33:16 - "found grace"
    'tuami': 'face',         # 1x Exod 33:20 - "see my face"
    'tukkilh': 'bracelet',   # 1x Exod 35:22 - "bracelets"
    'valzaw': 'too.much',    # 1x Exod 36:7 - "sufficient and too much"
    'bupkhat': 'tache',      # 1x Exod 36:13 - "fifty taches"
    'luzepna': 'chapiter',   # 1x Exod 36:38 - "chapiters/capitals"
    'zimna': 'binding',      # 1x Exod 39:23 - "hole of an habergeon"
    'kihelh': 'bell',        # 1x Exod 39:25 - "golden bell"
    'sungvan': 'within',     # 1x Exod 40:9 - "anoint all within"
    'sanen': 'piece',        # 1x Lev 1:8 - "lay the parts"
    'heektat': 'fold-cut',   # 1x Lev 1:15 - "wring off" (fold + cut)
    'heeksat': 'fold-apart', # 1x Lev 5:8 - "divide asunder" (NOT offer)
    'lohkik': 'make.amends', # 1x Lev 5:16 - "make amends"
    'kithehkhak': 'sprinkle', # 1x Lev 6:27 - "sprinkled"
    'kithehkha': 'sprinkle', # 1x Lev 6:27 - variant
    'kihuanna': 'boiling',   # 1x Lev 6:28 - "sodden/boiled"
    'taaubeelin': 'rinse',   # 1x Lev 6:28 - "scoured and rinsed"
    'meithau': 'rump.fat',   # 1x Lev 7:3 - "rump and fat"
    'bilteep': 'ear.tip',    # 1x Lev 8:24 - "tip of right ear"
    'kiphuhna': 'lifting',   # 1x Num 9:17 - "cloud was taken up"
    'gindan': 'alarm',       # 1x Num 10:7 - "blow, but not alarm"
    'nungdal': 'rearward',   # 1x Num 10:25 - "rearward of the camp"
    # lamhilh moved to BINARY_COMPOUNDS as lam-hilh (way-teach = guide)
    'ikkhiat': 'loathsome',  # 1x Num 11:20 - "come out at nostrils"
    'kiciamteh': 'enrolled', # 1x Num 11:26 - "of them that were written"
    
    # === Round 190e: Deuteronomy/Joshua hapax ===
    'tamzawk': 'more.numerous', # 1x Deut 7:7 - "more in number"
    'tuulekeelno': 'young.cattle', # 1x Deut 7:13 - "young of thy cattle"
    'khanlua': 'little.by.little', # 1x Deut 7:22 - "by little and little"
    'kithawi': 'hot.displeasure', # 1x Deut 9:19 - "hot displeasure"
    'ninikikhol': 'festival.day', # 1x Deut 13:16 - "gather all the spoil"
    'simsakhi': 'pygarg',    # 1x Deut 14:5 - "wild goat/pygarg"
    'zosakhi': 'chamois',    # 1x Deut 14:5 - "chamois"
    'sakikh': 'cud.chewer',  # 1x Deut 14:7 - "chew the cud"
    'samuat': 'pelican',     # 1x Deut 14:17 - "pelican"
    'dapphahin': 'aul',      # 1x Deut 15:17 - "take an aul"
    'khengval': 'presumptuously', # 1x Deut 17:12 - "do presumptuously"
    'phula': 'hot.heart',    # 1x Deut 19:6 - "while his heart is hot"
    'meidawilawh': 'fearful', # 1x Deut 20:8 - "fearful and fainthearted"
    'kithuneih': 'minister', # 1x Deut 21:5 - "priests minister"
    'lungkhauh': 'stubborn', # 1x Deut 21:18 - "stubborn son"
    'phottohsakkik': 'lift.up', # 1x Deut 22:4 - "help him lift up"
    'tangban': 'battlement', # 1x Deut 22:8 - "make a battlement"
    'heisakzaw': 'turn.curse', # 1x Deut 23:5 - "turned curse to blessing"
    'tulzum': 'paddle',      # 1x Deut 23:13 - "paddle upon thy weapon"
    'ankhing': 'victuals',   # 1x Deut 23:19 - "usury of victuals"
    'zantaamsak': 'sleep.with.pledge', # 1x Deut 24:12 - "sleep with his pledge"
    'kineihna': 'controversy', # 1x Deut 25:1 - "controversy between men"
    'sattansak': 'cut.off.hand', # 1x Deut 25:12 - "cut off her hand"
    'netniamna': 'affliction', # 1x Deut 26:7 - "affliction and bondage"
    'seeng': 'basket',       # 1x Deut 28:5 - "blessed thy basket"
    'nuaikiat': 'open.heavens', # 1x Deut 28:12 - "open his good treasure"
    'keutumna': 'consumption', # 1x Deut 28:22 - "consumption and fever"
    'kiptaka': 'find.ease',  # 1x Deut 28:65 - "find no ease"
    'ngunlekham': 'idol',    # 1x Deut 29:17 - "idols of wood and stone"
    'phiatkhiat': 'root.out', # 1x Deut 29:17 - "root that beareth gall"
    'lotgawp': 'brimstone',  # 1x Deut 29:23 - "brimstone and salt"
    'gamtangzo': 'go.over',  # 1x Deut 31:2 - "go out and come in"
    'lehdozaw': 'rebellion', # 1x Deut 31:27 - "rebellion and stiff neck"
    'siatgamtat': 'utterly.corrupt', # 1x Deut 31:29 - "utterly corrupt"
    'guahmal': 'drop.as.rain', # 1x Deut 32:2 - "doctrine shall drop"
    'balkham': 'enlargeth',  # 1x Deut 33:20 - "enlargeth Gad"
    'lamzan': 'observe.law', # 1x Josh 1:7 - "observe to do"
    'sunlezanin': 'day.and.night', # 1x Josh 1:8 - "day and night"
    'zialkhia': 'roll.away', # 1x Josh 5:9 - "rolled away reproach"
    'tumsuak': 'continual.blow', # 1x Josh 6:13 - "going on and blowing"
    'namun': 'brought.by.tribes', # 1x Josh 7:14 - "by your tribes"
    'zingtung': 'early.morning', # 1x Josh 8:14 - "early in the morning"
    'lehdelh': 'look.behind', # 1x Josh 8:20 - "looked behind them"
    'hingmat': 'take.alive', # 1x Josh 8:23 - "took alive"
    
    # === Round 190f: Ruth/Samuel hapax ===
    'laam': 'wife',          # 1x Judg 21:23 - "took them wives"
    'tunitak': 'too.old',    # 1x Ruth 1:12 - "too old to have husband"
    'lunggimzaw': 'long.tarry', # 1x Ruth 1:13 - "tarry for them"
    'anvui': 'gleaning',     # 1x Ruth 2:2 - "glean ears of corn"
    'kuankha': 'gleaned',    # 1x Ruth 2:3 - "gleaned in the field"
    'anlom': 'sheaf',        # 1x Ruth 2:7 - "gather after the reapers"
    # hen removed - it's the verb 'tie' (hen-te = bundles/handfuls), not a separate word
    'ankhamval': 'parched.corn', # 1x Ruth 2:14 - "parched corn"
    'kuankhop': 'glean.close', # 1x Ruth 2:21 - "keep close by"
    'leem': 'mark.place',    # 1x Ruth 3:4 - "mark the place"
    'anphual': 'heap.of.corn', # 1x Ruth 3:7 - "end of the heap"
    'kikhek': 'redeeming',   # 1x Ruth 4:7 - "manner of redeeming"
    'daupaina': 'enemy.dwelling', # 1x 1Sam 2:32 - "enemy in habitation"
    'mitlawt': 'eyes.fail',  # 1x 1Sam 2:33 - "consume thine eyes"
    'thalpuk': 'fell.backward', # 1x 1Sam 4:18 - "fell backward"
    'thacingzaw': 'goodlier', # 1x 1Sam 9:2 - "goodlier than he"
    'kawngsa': 'shoulder',   # 1x 1Sam 9:24 - "cook took up shoulder"
    'khuangneu': 'garrison', # 1x 1Sam 10:5 - "garrison of Philistines"
    'sot': 'respite',        # 1x 1Sam 11:3 - "give us seven days"
    'huathuai': 'garrison',  # 1x 1Sam 13:4 - "smitten a garrison"
    'leivang': 'discovered', # 1x 1Sam 14:11 - "discovered themselves"
    'tawnlang': 'half.acre', # 1x 1Sam 14:14 - "half acre of land"
    'kitawhnawi': 'tumult',  # 1x 1Sam 14:19 - "tumult increased"
    'thukzawh': 'adjured',   # 1x 1Sam 14:24 - "Saul had adjured"
    'lehzuihkik': 'turn.again', # 1x 1Sam 15:25 - "turn again with me"
    'kilang': 'height',      # 1x 1Sam 16:7 - "height of stature"
    'teibul': 'spear.staff', # 1x 1Sam 17:7 - "staff of his spear"
    'lawngpi': 'weaver.beam', # 1x 1Sam 17:7 - "weaver's beam"
    'teipak': 'spear.head',  # 1x 1Sam 17:7 - "spear's head"
    'sathaukhal': 'cheese',  # 1x 1Sam 17:18 - "ten cheeses"
    'makaipi': 'champion',   # 1x 1Sam 17:23 - "the champion"
    'kihaimuan': 'anger',    # 1x 1Sam 17:28 - "Eliab's anger"
    'galdalna': 'armour',    # 1x 1Sam 17:39 - "his armour"
    'teikhawh': 'spear',     # 1x 1Sam 17:45 - "sword and spear"
    'galkidal': 'weapons',   # 1x 1Sam 18:4 - "sword and bow"
    'khuangtung': 'meet',    # 1x 1Sam 18:6 - "women came out"
    'matutzawh': 'behave.wisely', # 1x 1Sam 18:15 - "behaved wisely"
    'teep': 'foreskin',      # 1x 1Sam 18:27 - "foreskins"
    'tunzaw': 'go.forth',    # 1x 1Sam 18:30 - "princes went forth"
    'kiheikhial': 'anger.kindled', # 1x 1Sam 20:30 - "anger kindled"
    'dahzaw': 'arise.out',   # 1x 1Sam 20:41 - "arose out of place"
    'kulhkongkhak': 'city.gate', # 1x 1Sam 21:13 - "in their hands"
    
    # === Round 190g: 2 Samuel/1 Kings hapax ===
    'thupeel': 'froward',    # 1x 2Sam 22:27 - "with the froward"
    'khauhpen': 'steel.bow', # 1x 2Sam 22:35 - "bow of steel"
    'sunlet': 'consume',     # 1x 2Sam 22:39 - "consumed them"
    'tuankhamin': 'beat.small', # 1x 2Sam 22:43 - "beat them small"
    'laphuak': 'last.words', # 1x 2Sam 23:1 - "last words of David"
    'hikcip': 'hand.clave',  # 1x 2Sam 23:10 - "hand clave unto sword"
    'hanzia': 'far.be.it',   # 1x 2Sam 23:17 - "far from me"
    'tamngaikop': 'piped',   # 1x 1Kgs 1:40 - "piped with pipes"
    'thawnkham': 'rejoiced', # 1x 1Kgs 1:40 - "rejoiced greatly"
    'heksuk': 'strong',      # 1x 1Kgs 2:2 - "be thou strong"
    'hektoh': 'show.thyself', # 1x 1Kgs 2:2 - "shew thyself a man"
    'gimkhop': 'affliction', # 1x 1Kgs 2:26 - "all my father's affliction"
    'thahzawh': 'asked',     # 1x 1Kgs 3:11 - "thou hast asked"
    'sanang': 'fat.oxen',    # 1x 1Kgs 4:23 - "fat oxen"
    'zaptel': 'dromedary',   # 1x 1Kgs 4:28 - "dromedaries"
    'puknah': 'hyssop',      # 1x 1Kgs 4:33 - "hyssop that springeth"
    'nilh': 'anointing',     # 1x 1Kgs 5:1 - "anointed him king"
    'kiphuk': 'hewing',      # 1x 1Kgs 5:6 - "hew cedar trees"
    'bungpi': 'measures',    # 1x 1Kgs 5:11 - "twenty measures"
    'singbek': 'cubit.broad', # 1x 1Kgs 6:6 - "cubits broad"
    'kitawh': 'quarry',      # 1x 1Kgs 6:7 - "stone made ready"
    'lambeh': 'chamber',     # 1x 1Kgs 6:8 - "chambers against house"
    'innsual': 'floor',      # 1x 1Kgs 6:30 - "floor of the house"
    'tukimin': 'open.flower', # 1x 1Kgs 6:32 - "open flowers"
    'zalesawmnga': 'fifty.cubits', # 1x 1Kgs 7:2 - "fifty cubits"
    'suangat': 'costly.stones', # 1x 1Kgs 7:9 - "costly stones"
    'khutpeekmai': 'handbreadth', # 1x 1Kgs 7:26 - "hand breadth thick"
    'limliam': 'ledges',     # 1x 1Kgs 7:29 - "between the ledges"
    'pei': 'wheel',          # 1x 1Kgs 7:32 - "work of the wheels"
    'peikual': 'chariot.wheel', # 1x 1Kgs 7:33 - "chariot wheel"
    'peikalh': 'axletree',   # 1x 1Kgs 7:33 - "axletrees"
    'bul': 'nave',           # 1x 1Kgs 7:33 - "naves"
    'vangsung': 'laver',     # 1x 1Kgs 7:38 - "ten lavers"
    'khukdin': 'kneeling',   # 1x 1Kgs 8:54 - "kneeling on his knees"
    # innkhuam moved to BINARY_COMPOUNDS as inn-khuam (house-pillar = pillar)
    'utong': 'peacock',      # 1x 1Kgs 10:22 - "peacocks"
    'zuibup': 'follow.fully', # 1x 1Kgs 11:6 - "went not fully after"
    'thuhaksa': 'grievous.yoke', # 1x 1Kgs 12:4 - "made our yoke grievous"
    'ngawhdawn': 'roughly',  # 1x 1Kgs 12:13 - "answered roughly"
    'leilulam': 'rebel',     # 1x 1Kgs 12:19 - "rebelled against"
    'thugik': 'sound.of.feet', # 1x 1Kgs 14:6 - "sound of her feet"
    'pusawn': 'walked.in.sins', # 1x 1Kgs 15:26 - "walked in sins"
    'kihalnel': 'besieged',  # 1x 1Kgs 16:17 - "went up and besieged"
    'mohneu': 'little.meal', # 1x 1Kgs 17:13 - "little cake first"
    'peem': 'widow.son',     # 1x 1Kgs 17:20 - "widow's son"
    'sikzum': 'cut.themselves', # 1x 1Kgs 18:28 - "cut themselves"
    'awngsuak': 'prophesied', # 1x 1Kgs 18:29 - "prophesied midday past"
    'heikik': 'turn.back',   # 1x 1Kgs 18:37 - "turned their heart back"
    'dimzawh': 'suffice',    # 1x 1Kgs 20:10 - "dust shall suffice"
    
    # === Round 190h: Chronicles hapax ===
    'kisehkhenna': 'division', # 1x 1Chr 24:1 - "divisions of sons of Aaron"
    'lekua': 'nineteenth',   # 1x 1Chr 25:26 - "nineteenth lot"
    'kikantel': 'chief',     # 1x 1Chr 26:31 - "Jerijah the chief"
    'khengak': 'stand.up',   # 1x 1Chr 28:2 - "stood up upon feet"
    'tungnun': 'find.grace', # 1x 1Chr 28:11 - "David gave pattern"
    'suangpak': 'onyx.stones', # 1x 1Chr 29:2 - "onyx stones"
    'puandum': 'purple.cloth', # 1x 2Chr 2:7 - "cunning in purple"
    'phuk': 'hewers',        # 1x 2Chr 2:10 - "hewers that cut"
    'kisuvui': 'beaten.wheat', # 1x 2Chr 2:10 - "beaten wheat"
    'sangkil': 'post',       # 1x 2Chr 3:7 - "beams, posts"
    'awh': 'chain',          # 1x 2Chr 3:16 - "chains in oracle"
    'sikkeuka': 'fleshhook', # 1x 2Chr 4:16 - "fleshhooks"
    'kipuak': 'bethink',     # 1x 2Chr 6:37 - "bethink themselves"
    'kitut': 'captivity',    # 1x 2Chr 6:38 - "land of captivity"
    'kulhnei': 'fenced.city', # 1x 2Chr 17:2 - "fenced cities"
    'mawklot': 'at.venture', # 1x 2Chr 18:33 - "at a venture"
    'heikhiat': 'take.heed', # 1x 2Chr 19:7 - "take heed"
    'lehthuk': 'reward',     # 1x 2Chr 20:11 - "how they reward"
    'dosak': 'fear',         # 1x 2Chr 20:29 - "fear of God"
    'tolhkhiat': 'loosen',   # 1x 2Chr 21:15 - "disease of bowels"
    'gilnat': 'bowels',      # 1x 2Chr 21:15 - "bowels fall out"
    'hawhsuk': 'heal',       # 1x 2Chr 22:6 - "to be healed"
    'hawh': 'wound',         # 1x 2Chr 22:7 - "destruction"
    'sen': 'hide',           # 1x 2Chr 22:11 - "hid him"
    'khon': 'levy',          # 1x 2Chr 24:6 - "collection"
    'themlen': 'throw.down', # 1x 2Chr 25:12 - "cast them down"
    'sucim': 'war.against',  # 1x 2Chr 26:6 - "warred against"
    'suangtang': 'sling.stone', # 1x 2Chr 26:14 - "shields and spears"
    'set': 'engine',         # 1x 2Chr 26:15 - "engines"
    'galsimna': 'war',       # 1x 2Chr 27:7 - "all his wars"
    'gimsakzaw': 'distress', # 1x 2Chr 28:20 - "distressed him"
    'ngentel': 'flay',       # 1x 2Chr 29:34 - "could not flay"
    'sianthosaksa': 'sanctify', # 1x 2Chr 29:34 - "sanctified"
    'kikhat': 'one.heart',   # 1x 2Chr 30:12 - "one heart"
    'mansiang': 'foundation', # 1x 2Chr 31:7 - "lay foundation"
    'sehkhen': 'east.gate',  # 1x 2Chr 31:14 - "porter toward east"
    'kikep': 'genealogy',    # 1x 2Chr 31:18 - "genealogy of all"
    'awn': 'encourage',      # 1x 2Chr 32:6 - "encouraged them"
    'linglawnsak': 'affright', # 1x 2Chr 32:18 - "affright them"
    'lelun': 'gods.of.people', # 1x 2Chr 32:19 - "gods of people"
    'khongkhai': 'pass.through.fire', # 1x 2Chr 33:6 - "through fire"
    'ciangto': 'build.wall', # 1x 2Chr 33:14 - "built a wall"
    'tep': 'carpenters',     # 1x 2Chr 34:11 - "carpenters and builders"
    'tecipanna': 'covenant', # 1x 2Chr 34:31 - "made a covenant"
    'khenkhen': 'divide',    # 1x 2Chr 35:5 - "divide yourselves"
    'kinawh': 'meddle',      # 1x 2Chr 35:21 - "meddle not"
    'kimu': 'abomination',   # 1x 2Chr 36:8 - "his abominations"
    
    # === Round 190i: Joshua/Judges hapax ===
    'ainungin': 'Anakims',   # 1x Jos 7:22 - "sons of Anak"
    'siknazat': 'repent',    # 1x Jos 8:29 - "repentance"
    'lik': 'turn.back',      # 1x Jos 8:29 - "turned back"
    'khatzong': 'certain',   # 1x Jos 8:35 - "one" (a certain one)
    'kiphop': 'harden',      # 1x Jos 9:4 - "hardened hearts"
    'atgawp': 'send.away',   # 1x Jos 9:13 - "sent us away"
    'tom': 'grow',           # 1x Jos 9:27 - "grew up"
    'liknelh': 'turn.aside', # 1x Jos 10:18 - "roll stones"
    'kuankhawm': 'glean',    # 1x Jos 10:24 - "gleaning together"
    'gunkuam': 'Girgashite', # 1x Jos 11:2 - ethnic group
    'thah': 'slay',          # 1x Jos 13:22 - "slain"
    'luidung': 'riverbank',  # 1x Jos 15:7 - "by the river"
    'mongciik': 'south',     # 1x Jos 15:21 - "southward"
    'hawmthawh': 'mingle',   # 1x Jos 22:16 - "mingles with"
    'lehnawt': 'overturn',   # 1x Jos 23:5 - "overturn them"
    # 'tunpi': REMOVED - conflicts with tunpi=hornet-big. Use tun-pih (kneel-APPL) instead
    'nengkia': 'drive.out',  # 1x Jdg 1:7 - "driven out"
    'sungpa': 'husband',     # 1x Jdg 1:16 - "father-in-law"
    'lehgamtat': 'possess',  # 1x Jdg 2:2 - "possess the land"
    'alun': 'oak',           # 1x Jdg 2:15 - "oak tree"
    'nisuhkung': 'noon',     # 1x Jdg 4:5 - "noontime"
    'gimluat': 'affliction', # 1x Jdg 4:21 - "great affliction"
    'koptai': 'prance',      # 1x Jdg 5:22 - "prancing" (horse hooves stamping)
    'khetbuk': 'stamp',      # 1x Jdg 5:26 - "pounding"
    'kinim': 'believe',      # 1x Jdg 5:30 - "trusted"
    'tuumul': 'barley',      # 1x Jdg 6:38 - "barley loaf"
    'kuancil': 'glean',      # 1x Jdg 8:1 - "gleaning"
    'bingphawn': 'company',  # 1x Jdg 8:11 - "company of men"
    'suun': 'noon',          # 1x Jdg 8:18 - "midday"
    'dupsan': 'tread.down',  # 1x Jdg 8:26 - "trodden"
    'kamhan': 'oracle',      # 1x Jdg 9:38 - "speak boldly"
    'dengkham': 'border',    # 1x Jdg 9:53 - "border city"
    'thudamin': 'peaceful',  # 1x Jdg 11:13 - "peaceably"
    'suankhiat': 'deliver',  # 1x Jdg 11:24 - "deliver out"
    'halnelh': 'stumble',    # 1x Jdg 12:1 - "stumbled"
    'moliah': 'Moabitess',   # 1x Jdg 14:20 - "Moabite woman"
    'meilah': 'torch',       # 1x Jdg 15:5 - "firebrands"
    'komdep': 'heap',        # 1x Jdg 15:19 - "heaps upon heaps"
    'patkhau': 'jawbone',    # 1x Jdg 16:9 - "jawbone of ass"
    'thalkhau': 'quiver',    # 1x Jdg 16:9 - "bow quiver"
    'buangawp': 'confuse',   # 1x Jdg 20:5 - "confounded"
    'lanluat': 'exceed',     # 1x Jdg 20:10 - "exceedingly"
    'ihkik': 'sleep',        # 1x Jdg 20:23 - "lay down to sleep"
    'kikalsung': 'between',  # 1x Jdg 20:42 - "in the midst"
    'suahloh': 'swear',      # 1x Jdg 21:22 - "oath"
    'ipen': 'gather',        # 1x Ruth 2:20 - "gathered"
    'ihkhiattoh': 'lie.with', # 1x 1Sam 2:14 - "lie down together"
    'kipiak': 'present',     # 1x 1Sam 2:29 - "offerings"
    
    # === Round 190j: Genesis-Deuteronomy suffix fixes ===
    'tuakpe': 'happen',      # 1x Gen 4:15 - "meet/happen to"
    'khelg': 'flee',         # 1x Gen 32:25 - "hollow of thigh"
    'paikhiato': 'send.forth', # 1x Exo 33:15 - "send forth"
    'sakhati': 'cause',      # 1x Exo 37:8 - "made of it"
    'biaknatau': 'idol',     # 1x Exo 38:30 - "worship place"
    'tlup': 'generation',    # 1x Lev 10:6 - "whole assembly"
    'phukhia': 'hew.out',    # 1x Lev 13:20 - "hewn out"
    'teemsak': 'swell.cause', # 5x Num 5:21-27 - "cause to swell"
    'olna': 'spy.report',    # 1x Num 13:19 - "report of spies"
    'pal': 'spy',            # 1x Num 13:20 - "spies"
    'almang': 'widow',       # 1x Num 14:9 - "alone/widow"
    'phunsan': 'fall.upon',  # 1x Num 14:29 - "fell down"
    'khupnelh': 'bow.knee',  # 1x Num 16:33 - "kneel down"
    'nguumkhia': 'bud.forth', # 1x Num 17:8 - "budded"
    'akin': 'certainly',     # 1x Num 17:8 - "indeed"
    'vu': 'bee',             # 1x Num 19:9 - "bee/fly"
    'gimbawl': 'distress',   # 1x Num 20:15 - "distressed"
    'gupha': 'fiery.serpent', # 1x Num 21:6 - "fiery serpent"
    'kikhungsuk': 'discouraged', # 1x Num 21:13 - "discouraged"
    'kimuhsuk': 'abhor',     # 1x Num 21:20 - "abhor"
    'wcikah': 'vineyard',    # 1x Num 22:24 - "path of vineyards"
    'mawlpih': 'curse',      # 1x Num 22:29 - "curse"
    'dinlam': 'westward',    # 1x Num 22:34 - "direction"
    'tunai': 'rich',         # 1x Num 24:17 - "wealthy"
    'suntang': 'zealous',    # 1x Num 25:4 - "zealous"
    'khelpil': 'thigh.hollow', # 1x Num 25:18 - "hollow of thigh"
    'seel': 'basket',        # 1x Num 26:9 - "basket"
    'leenggahzucil': 'chariot.wheel', # 1x Num 28:7 - "chariot wheel"
    'gingkhia': 'inherit',   # 1x Num 30:2 - "inheritance"
    'kingah': 'obtain',      # 1x Num 31:27 - "obtained"
    'tuusiah': 'earring',    # 1x Num 31:37 - "earrings"
    'pelhem': 'tablet',      # 1x Num 31:49 - "tablets"
    'banbuh': 'armlet',      # 1x Num 31:50 - "bracelet"
    'khi': 'chain',          # 1x Num 31:50 - "chains"
    'lamgal': 'war',         # 1x Num 32:19 - "war"
    # taanggam moved to BINARY_COMPOUNDS as taang-gam (beautiful-land = suburb)
    'daihual': 'revenger',   # 1x Num 35:27 - "avenger"
    'lenkip': 'every',       # 1x Deu 4:4 - "everyone"
    'sungtengun': 'among',   # 1x Deu 11:5 - "in midst of"
    'wmvalh': 'desire',      # 1x Deu 11:6 - "desire"
    'ninkikhol': 'daily',    # 1x Deu 13:16 - "day by day"
    'ga': 'hook',            # 1x Deu 19:3 - "hook/goad"
    
    # === Round 190k: Samuel hapax with disambiguation ===
    'tuami': 'face',         # 1x Gen 30:40 - "face/countenance"
    
    # Disambiguation: Add short stems WITH explicit compounds to prevent over-parsing
    # Pattern: Add the short stem, then add longer words that shouldn't be parsed with it
    
    # teem (swell) - add teembaw as explicit compound
    'teem': 'swell',         # 1x Num 5:27 - "belly swell"
    'teembaw': 'ark',        # 124x - DISAMBIGUATION: ark, not swell+baw
    
    # gih (pierce) - gihna means 'tremble' not 'pierce-NMLZ'
    'gih': 'pierce',         # 1x 2Sam 14:26 - "pierce"
    'gihna': 'tremble',      # 18x - DISAMBIGUATION: tremble (separate root)
    
    # ho (crowd) - hong/hon/hoih are separate roots
    'ho': 'crowd',           # 1x 2Sam 3:27 - "crowd"
    # hong/hon/hoih already in dictionary as separate stems - no conflict if ho is checked last
    
    # dawt (love) - dawtna/dawtsak are compounds of dawt
    'dawt': 'love',          # 1x 2Sam 2:16 - "beloved"
    'dawtna': 'love.NMLZ',   # Already correctly parsed as dawt-na, this is redundant but safe
    
    # huat (hate) - same as dawt, compounds work
    'huat': 'hate',          # 1x 2Sam 10:6 - "hatred"
    
    # baak (debt) - ba is separate root, baak shouldn't parse as ba+ak
    'baak': 'debt',          # 1x 2Sam 6:19 - "debt"
    
    # lee (which) - leeng is chariot (separate root)
    'lee': 'which.REL',      # 1x 2Sam 2:18 - "who/which"  
    'leeng': 'chariot',      # 169x - DISAMBIGUATION: chariot (separate root)
    'leenggahzu': 'chariot.wheel', # Already compound
    'leenggui': 'chariot.body',    # Already compound
    
    # meet already exists in dictionary - no need to add
    
    'khitah': 'chain.for',   # 1x Num 25:13 - "chained"
    'ihkhiatsak': 'lie.down', # 1x Deu 25:9 - "lie down"
    'laitengun': 'midst',    # 1x Deu 31:11 - "in the midst"
    'bawlsaksa': 'doer',     # 1x 1Sam 12:24 - "workers"
    'gkhutah': 'handbreadth', # 1x 1Sam 13:21 - "handspan"
    'isuksak': 'restore',    # 1x 1Sam 21:13 - "restore"
    'kiselsim': 'humble',    # 1x 1Sam 23:23 - "humbled"
    'metna': 'lick',         # 1x 1Sam 25:4 - "licking"
    'theimoh': 'know.not',   # 1x 1Sam 25:18 - "not knowing"
    'lotkhiat': 'draw.out',  # 1x 1Sam 25:29 - "sling out"
    'zahkoh': 'fear',        # 1x 1Sam 25:39 - "feared"
    'maikun': 'face.to',     # 1x 1Sam 25:41 - "face to face"
    'kikap': 'fight',        # 1x 1Sam 26:10 - "battle"
    'uili': 'vile',          # 1x 1Sam 26:20 - "vile person"
    'tawnpuk': 'cave',       # 1x 1Sam 28:20 - "cave"
    'dawtlet': 'secretly',   # 1x 1Sam 31:4 - "secretly"
    'khuakulhah': 'stronghold', # 1x 1Sam 31:10 - "fortress"
    # banbulh moved to BINARY_COMPOUNDS as ban-bulh (arm-bind = bracelet)
    'lengsuak': 'prince',    # 1x 2Sam 2:23 - "nobleman"
    'bangtan': 'shield',     # 1x 2Sam 2:26 - "shield"
    'sawtlai': 'long.time',  # 1x 2Sam 2:26 - "long while"
    'susiazaw': 'worse',     # 1x 2Sam 4:11 - "more wicked"
    'lathuah': 'smite',      # 1x 2Sam 5:13 - "smite"
    'pulak': 'declare',      # 1x 2Sam 7:27 - "reveal"
    'zothawh': 'accomplish', # 1x 2Sam 11:23 - "prevail"
    'maipuksuk': 'bow.face', # 1x 2Sam 14:22 - "bow face down"
    'wivak': 'surround',     # 1x 2Sam 15:20 - "surround"
    'thuko': 'lie.down',     # 1x 2Sam 15:28 - "tarry"
    'phehkeu': 'scatter',    # 1x 2Sam 16:1 - "scatter"
    'uisi': 'viper',         # 1x 2Sam 16:9 - "dead dog"
    
    # === Round 190l: Remaining suffix/stem fixes ===
    'manlan': 'hastily',     # 1x Gen 27:20 - appears as manlan not manlang
    'tuami': 'face',         # (from Round 190k) - face/countenance
    'sakhati': 'cause',      # 1x Exo 37:8 - variant of sak
    # 'ih': REMOVED - was incorrectly glossed as 'lie.down'. kaihna actually means 'furrow/plow-area'
    'kaihna': 'furrow',      # 1x 1Sam 14:14 - "half acre" (area a yoke of oxen can plow)
    'zalh': 'lazy',          # 1x 2Kgs 17:19 - "slothful"
    'leibeel': 'pot',       # earthen vessel/clay pot (not "lazy person")
    'bepi': 'idle',          # 1x 2Kgs 17:28 - "idle person"
    'ngel': 'wander',        # 1x 2Kgs 18:11 - "wandering"
    'makhelh': 'backslide',  # 1x 2Kgs 18:23 - "backsliding"
    'kamneem': 'soft.word',  # 1x 2Kgs 19:7 - "soft words"
    'awngsuk': 'open.mouth', # 1x 2Kgs 22:14 - "open wide"
    'psap': 'sob',           # 1x Psa 2:46 - "sobbing" (foreign pattern)
    'zaptel': 'flutter',     # 1x Psa 4:28 - "fluttering"
    'cipnelh': 'cringe',     # 1x Psa 20:30 - "cringe"
    'petlum': 'swallow.up',  # 1x Psa 20:36 - "swallow up"
    'zakphet': 'hearing',    # 1x Psa 21:16 - "hearing"
    'samulpuan': 'sackcloth', # 1x Prov 1:8 - "sackcloth"
    'tatolh': 'revolve',     # 1x Prov 2:21 - "revolving"
    'lukolh': 'roll.up',     # 1x Prov 2:23 - "roll up"
    'pomlai': 'middle',      # 1x Prov 3:3 - "midst"
    'ganpi': 'great.one',    # 1x Prov 3:17 - "great ones"
    'kuantoh': 'glean.together', # 1x Prov 3:21 - "gleaning"
    'mehbeel': 'ember',      # 1x Prov 4:39 - "ember/coal"
    'atnen': 'offering',     # 1x Prov 4:39 - "offering" (variant)
    'kun': 'bow',            # 1x Prov 5:18 - "bow down" (kunna = bow-NMLZ)
    'nungdelh': 'alive',     # 1x Prov 5:20 - "living"
    'kitankhiat': 'depart.from', # 1x Prov 6:31 - "departed from"
    'kial': 'hunger',        # 36x - "want/hunger/famine" (gilkial = stomach-hunger = bowels)
    'khuacing': 'town.gate', # 1x Prov 9:14 - "city gate"
    'meltheih': 'know.face', # 1x Prov 10:11 - "recognize"
    'siakkhiat': 'die.away', # 1x Prov 10:17 - "die away"
    'ekbuk': 'vomit',        # 1x Prov 10:27 - "vomit"
    'siakkhia': 'die.out',   # 1x Prov 10:28 - "die out"
    
    # === Round 193: Systematic hapax analysis ===
    'nungguh': 'rump',       # 1x Lev 3:9 - "the whole rump" (animal anatomy)
    'vutvang': 'hole',       # 1x 2Kgs 12:9 - "bored a hole" in chest lid
    'simzel': 'invade',      # 1x 2Kgs 13:20 - "bands invaded the land"
    'lahkim': 'pattern',     # 1x 2Kgs 16:10 - "the fashion/pattern of altar"
    'balkhiat': 'rend',      # 1x 2Kgs 17:21 - "rent Israel from house of David"
    'cilun': 'dwell.begin',  # 1x 2Kgs 17:25 - "beginning of their dwelling"
    'kikhap': 'pledge',      # 1x 2Kgs 18:23 - "give pledges/wager"
    'lehnawhzo': 'turn.away.able', # 1x 2Kgs 18:24 - "turn away the face"
    'vankia': 'prey',        # 1x 2Kgs 21:14 - "become a prey and spoil"
    'gat': 'weave',          # 1x 2Kgs 23:7 - "where women wove hangings"
    # khakunin: now parses transparently as khakun-in (be.cast.down-ERG)
    # Note: thuap means 'span' (measurement) - see COMPOUND_WORDS line ~9950
    # ngahthuap = get-allowance (compound) in 2Kgs 25:30
    'tunu': 'daughter',      # 1x 1Chr 1:50 - variant of tanu (daughter)
    'hansuah': 'stir.up',    # 1x 1Chr 5:26 - "stirred up the spirit"
    'pheeng': 'pan',         # 1x 1Chr 9:31 - "things made in pans"
    'thagol': 'height',      # 1x 1Chr 11:23 - "of great stature/height"
    'phinna': 'provoke',     # 1x 2Kgs 23:26 - "provocations"
    'nuak': 'return',        # 1x 2Sam 17:23 - "gat him home" (returned home)
    'bulom': 'ruin',         # 1x 2Kgs 19:25 - "ruinous heaps"
    'angkawm': 'adultery',   # 2x Jer 5:7, 9:2 - "committed adultery", "adulterers"
    'ipip': 'endure',        # 2x Jer 20:9, Rom 9:22 - "forbearing/longsuffering"
    'bulh': 'bind',          # 1x Jer 20:2 - "stocks" (restraining device)
    'bum': 'deceive',        # 1x Isa 47:12 - "sorceries/deception"
    'bengbeng': 'slap',      # 1x 2Cor 11:20 - "smite on face"
    'bung': 'tablet',        # 1x Isa 3:20 - "tablets" (ornamental jewelry)
    'awng': 'young',         # 1x Gen 33:13 - "herds with young"
    'pel': 'break',          # 1x Rom 1:31 - "covenantbreakers" (ciampel = promise-break)
    'tehteh': 'beseech',     # 1x Isa 64:9 - "we beseech thee"
    'dapphah': 'precious.cloth', # 1x Ezek 27:20 - "precious clothes for chariots"
    'del': 'tremble',        # 1x James 2:19 - "devils tremble"
    'dimsak': 'fill',        # 1x Zeph 1:9 - "fill masters' houses"
    'gaisak': 'birth',       # 1x Matt 1:18 - "birth of Jesus Christ"
    # galpan moved to BINARY_COMPOUNDS as gal-pan (war-side = fortress)
    'eh': 'cleave',          # 1x Eccl 10:9 - "cleaveth wood" (not interjection here)
    'makaih': 'leader',      # 1x Isa 9:16 - "leaders"
    'mangzo': 'profit',      # 1x Heb 12:11 - "yieldeth/profitable"
    'mawl': 'mad',           # 1x Eccl 1:17 - "madness"
    'meidawi': 'sober.mind', # 1x 2Tim 1:7 - "sound mind"
    # suanghawm moved to BINARY_COMPOUNDS as suang-hawm (rock-hollow = cave)
    'vuk': 'ice',            # 1x Job 38:29 - "ice"
    'val': 'young.man',      # 1x 1Cor 15:6 - "brethren" (young men)
    'piksan': 'stubborn',    # 1x Prov 16:30 - "froward"
    'phuah': 'thunder',      # 1x Mark 3:17 - "thunder"
    'thagui': 'sinew',       # 1x Job 10:11 - "sinews"
    'tal': 'buffalo',        # 1x Isa 34:7 - "unicorns/wild ox"
    'taak': 'comb',          # 1x Psa 19:10 - "honeycomb"
    'ngim': 'bitter',        # 1x Psa 64:3 - "bitter"
    'taltang': 'forehead',   # 7x Exod/1Sam - "forehead"
    'zulhzau': 'backslide',  # 1x Jer 3:22 - "backsliding"
    'zulhtat': 'shame',      # 1x Isa 54:4 - "shame"
    'zuausiam': 'deceive',   # 1x Dan 11:21 - "flatteries"
    'zuaugen': 'transgress.speak', # 1x Prov 12:13 - "transgression"
    'zuauthu': 'transgression',    # 1x Josh 7:11 - "transgressed"
    'zuk': 'lightning',      # 1x Job 28:26 - "lightning"
    'zuksak': 'diminish',    # 1x 1Kgs 17:14 - "waste"
    'zom': 'continue',       # 1x Ezra 5:5 - "cease" (negate continue)
    'zinzin': 'journey',     # 1x 2Cor 11:26 - "journeyings" (REDUP)
    'zindo': 'affection',    # 1x 2Cor 7:15 - "affection"
    'zeizai': 'armory',      # 1x SoS 4:4 - "armoury"
    'vutluahna': 'snuffer',  # 7x Exod/Num/1Kgs - "snuffers" (candle tool)
    'ziazua': 'excellent',   # 1x Esth 1:4 - "excellent majesty"
    'zial': 'uncover',       # 1x Ezek 4:7 - "uncovered"
    'zialkhol': 'prepare.to.go', # 1x Jer 46:19 - "furnish/prepare"
    'zialin': 'stand',       # 1x SoS 2:9 - "standeth"
    'zialetong': 'way',      # 1x Isa 2:3 - "ways"
    'zawh': 'able',          # Common, but need stem for COMPOUND
    'zatna': 'scarcity',     # 1x Mic 6:10 - "scant measure"
    'zahko': 'trust',        # 1x Psa 119:42 - "trust"
    'vanzat': 'rigging',     # 1x Acts 27:19 - "tackling"
    'unau': 'sibling',       # 1x Mark 3:17 - "brothers" (u+nau)
    'upmawhna': 'suspicion', # 1x 1Tim 6:4 - "evil surmisings"
    'vaikhakna': 'bone',     # 1x Heb 11:22 - "bones"
    'vahui': 'fitly.set',    # 1x SoS 5:12 - "fitly set"
    'tuulebawng': 'flock',   # 1x Jer 3:24 - "flocks"
    'zongsat': 'enslave',    # 1x 2Pet 2:19 - "bondage"
    'zongpah': 'opportunity', # 1x Matt 26:16 - "opportunity"
    'zolua': 'wounded',      # 1x Jer 37:10 - "wounded"
    'zakma': 'hear.before',  # 1x Col 1:5 - "heard before"
    'vuak': 'beat',          # 1x Prov 23:35 - "beaten"
    'vengvang': 'slaughter', # 1x Ezek 26:15 - "slaughter"
    'tuikuangpi': 'basin.big', # 1x Jer 27:18 - "vessels"
    'tuanthu': 'fable',      # 1x 2Pet 1:16 - "fables"
    'thuvaan': 'companion',  # 1x Ezra 4:9 - "companions"
    'tumtheih': 'kind',      # 1x Dan 3:10 - "all kinds"
    'tumsuk': 'draught',     # 1x Matt 15:17 - "draught"
    'totawm': 'cistern',     # 1x Jer 2:13 - "cisterns"
    'thupina': 'pleasant.thing', # 1x Lam 1:7 - "pleasant things"
    'thupiangsa': 'clearing', # 1x 2Cor 7:11 - "clearing"
    'thumong': 'end',        # 1x Isa 47:7 - "latter end"
    'thutanna': 'judgment', # 1x Psa 97:2 - "judgment"
    'thukimnasa': 'covenant', # 1x Isa 33:8 - "covenant"
    'sialh': 'tomorrow',     # 1x Prov 27:1 - "tomorrow"
    'sial': 'chase',         # For sialpai etc
    'siasa': 'evil.thing',   # For siasate
    'sawkkhawm': 'betray',   # 1x Luke 22:21 - "betrayeth"
    'sankhit': 'receive',    # 1x Acts 8:14 - "received"
    'taal': 'fall',          # 1x Psa 56:13 - "falling"
    'tanzum': 'joint',       # 1x SoS 7:1 - "joints"
    'tawhtang': 'key',       # 1x Matt 16:19 - "keys"
    'tawlnga': 'work',       # 1x Heb 4:10 - "works"
    'teeknu': 'mother.in.law', # 1x Ruth 1:14 - "mother in law"
    'teeksia': 'father.in.law', # - "father in law"
    'tawmkha': 'few',        # 1x Jer 44:28 - "remnant"
    'tawmno': 'small',       # 1x Luke 12:32 - "little"
    'tenpak': 'dwell.tent',  # 1x Jer 35:7 - "dwell in tents"
    'tenpih': 'marry',       # 1x Matt 5:32 - "marry"
    'telkheh': 'remind',     # 1x Rom 15:15 - "remind"
    'tennop': 'desire',      # 1x Jer 42:22 - "desire"
    'tentheih': 'dwell',     # 1x Jer 33:12 - "habitation"
    'teepkang': 'medicine',  # 1x Prov 17:22 - "medicine"
    'tei': 'prudent',        # 1x 1Cor 1:19 - "prudent"
    'teitei': 'persistent',  # 1x Luke 11:8 - "importunity"
    'tangngol': 'caterpillar', # 1x Psa 105:34 - "caterpillars"
    'maan': 'shadow',        # 1x Jer 48:45 - "shadow"
    'manglian': 'governor',  # 1x Dan 3:3 - "governors"
    'mawkphat': 'flatter',   # 1x Prov 29:5 - "flattereth"
    'meilak': 'break',       # 1x Isa 30:14 - "breaking"
    'meimapi': 'sore',       # 1x Isa 1:6 - "sores"
    'miaimuai': 'myriad',    # 1x Rev 5:11 - "ten thousand"
    'migina': 'upright',     # 1x Prov 2:21 - "upright"
    'miniam': 'meek',        # 1x Psa 149:4 - "meek"
    'mithuman': 'righteous', # 1x Prov 28:1 - "righteous"
    'mivom': 'leopard',      # 1x Jer 13:23 - "leopard"
    'monu': 'daughter.in.law', # 1x Matt 10:35 - "daughter in law"
    'ban': 'arm',            # 1x Dan 2:32 - "arms"
    'bawk': 'mule',          # 1x 1Chr 12:40 - "mules"
    'biang': 'spice',        # 1x SoS 5:13 - "spices"
    'ciimsa': 'counsel',     # 1x Prov 1:5 - "counsels"
    'anvai': 'dry',          # 1x Jer 4:11 - "dry wind"
    'anzap': 'winnow',       # 1x Matt 3:12 - "fan"
    'dawilut': 'overcome',   # 1x Acts 19:16 - "overcame"
    'cilphih': 'spit',       # 1x Isa 50:6 - "spitting"
    'cingh': 'poor',         # 1x Prov 14:21 - "poor"
    'nawng': 'wrong',        # For nawngkai etc
    'nawk': 'convert',       # 1x Acts 15:3 - "conversion"
    'nakvang': 'nostril',    # 1x Psa 18:8 - "nostrils"
    'palhngulh': 'stray',    # 1x Psa 106:39 - "whoring"
    'pangbet': 'correct',    # 1x Prov 22:15 - "correction"
    'phamawh': 'necessary',  # 1x Titus 3:14 - "necessary"
    'phok': 'turn',          # 1x Isa 42:16 - "paths"
    'phualpi': 'merchant.city', # 1x Isa 23:11 - "merchant cities"
    'pheek': 'bed',          # 1x Acts 5:15 - "beds"
    'phuhsa': 'planted',     # 1x Jer 45:4 - "planted"
    'gai': 'conceive',       # 39x - "conceive" (become pregnant)
    'galkisim': 'war.signal', # 1x Jer 4:21 - "standard/trumpet"
    'gawhna': 'understanding', # 1x Mark 12:33 - "understanding"
    'gawng': 'lean',         # 1x Ezek 34:20 - "lean cattle"
    'gehsa': 'bull',         # 1x Isa 34:7 - "bullocks"
    'gialbem': 'leopard',    # 1x Isa 11:6 - "leopard"
    'gimpiak': 'afflict',    # 1x Psa 88:15 - "afflicted"
    'gimsak': 'judge',       # 1x Isa 59:9 - "judgment"
    'ginalopi': 'polluted',  # 1x Mal 1:7 - "polluted"
    'gisuang': 'boundary',   # 1x Job 24:2 - "landmarks"
    'gitta': 'sparrow',      # 1x Matt 10:29 - "sparrows"
    'guah': 'rain',          # for guahtui compound (rain-water)
    
    # === Lexicon internalization (2024-03-18) ===
    # These words were previously only in external ctd_lexicon.tsv
    # Now internalized for self-contained analyzer
    
    # High-frequency nouns (>100x)
    'lam': 'way',            # 883x - road, path, direction
    'lian': 'great',         # 364x - big, large, chief
    'peuhmah': 'whosoever',  # 355x - anyone (indefinite pronoun)
    'mei': 'fire',           # 350x
    'mang': 'dream',         # 349x
    'namsau': 'sword',       # 347x
    'pumpi': 'body',         # 336x - physical body
    'ngun': 'silver',        # 294x
    'suang': 'stone',        # 293x
    'pu': 'grandfather',     # 256x - also ancestor
    'heh': 'anger',          # 253x
    'manun': 'sin',          # 242x
    'tahen': 'army',         # 230x - also "amen" (homophone)
    'tokhom': 'throne',      # 198x
    'pang': 'side',          # 191x
    'khe': 'foot',           # 188x
    'gun': 'river',          # 169x - also place name element
    'takpi': 'indeed',       # 167x - emphatic adverb
    'hai': 'cup',            # 167x
    'beek': 'only',          # 165x - "neither" in context
    'sehnel': 'wilderness',  # 152x
    'leilu': 'north',        # 149x
    'seh': 'appoint',        # 146x
    'tuutal': 'ram',         # 144x
    'teci': 'witness',       # 143x
    'tegel': 'both',         # 140x - "two together"
    'leitaw': 'south',       # 126x
    'thaman': 'reward',      # 126x
    'tuni': 'today',         # 121x
    'makai': 'prince',       # 118x
    'dim': 'full',           # 117x
    'lecin': 'offend',       # 112x
    'taklam': 'right',       # 110x - right side
    'dih': 'consider',       # 109x
    'thuk': 'deep',          # 105x
    'thong': 'prison',       # 104x
    'huih': 'wind',          # 102x
    'muang': 'trust',        # 101x
    'neu': 'small',          # 101x
    
    # Medium-frequency nouns (50-100x)
    'tulkhat': 'thousand',   # 96x - one thousand
    'phuak': 'utter',        # 95x - pronounce, call
    'meii': 'cloud',         # 95x
    'lehang': 'verily',      # 93x
    'sungteng': 'nine',      # 92x
    'zu': 'wine',            # 92x
    'guan': 'spirit',        # 92x
    'tham': 'moreover',      # 90x
    'lupna': 'bed',          # 90x
    'lianzaw': 'greater',    # 87x
    'oliv': 'olive',         # 86x
    'tha': 'strength',       # 86x
    'don': 'regard',         # 84x
    'tawlkhat': 'little',    # 83x
    'koi': 'whence',         # 83x
    'leivui': 'dust',        # 81x
    'tacil': 'firstborn',    # 81x
    'han': 'sepulchre',      # 79x - grave, tomb
    'manpha': 'precious',    # 78x
    'kuama': 'charge',       # 78x
    'taamtak': 'cedar',      # 75x
    'tanvei': 'long',        # 73x
    'zuau': 'lie',           # 72x - falsehood
    'kivui': 'bury',         # 71x
    'phak': 'year',          # 69x
    'gik': 'shekel',         # 69x
    'phazah': 'number',      # 68x
    'meigong': 'widow',      # 66x
    'gunkuang': 'ship',      # 66x
    'vasa': 'bird',          # 63x
    'zut': 'overlay',        # 62x
    'tulnih': 'two.thousand', # 62x
    'hau': 'rich',           # 61x
    'zon': 'seek',           # 61x
    'pek': 'everlasting',    # 60x
    'tuk': 'stumble',        # 57x
    'dung': 'length',        # 56x
    'lampang': 'side',       # 54x
    'phot': 'first',         # 53x
    'suangmanpha': 'precious.stone', # 53x
    'vive': 'thing',         # 52x
    'ngitnget': 'continually', # 52x
    'po': 'grow',            # 51x
    'suangpi': 'rock',       # 51x
    'maang': 'vision',       # 50x
    
    # Lower-frequency nouns (20-50x)
    'thehthang': 'scatter',  # 48x
    'suangtum': 'stone',     # 48x
    'leihawm': 'pit',        # 47x
    'go': 'kill',            # 47x
    'dawimangpa': 'devil',   # 47x
    'kiu': 'corner',         # 46x
    'tamzaw': 'greater',     # 46x
    'tawn': 'loaf',          # 46x
    'den': 'neither',        # 45x
    'hanthawn': 'exhort',    # 43x
    'belh': 'refuge',        # 43x
    'pupi': 'ancestor',      # 42x - forefathers
    'kimkot': 'round',       # 42x
    'gul': 'viper',          # 42x
    'leimong': 'end',        # 42x
    'gual': 'row',           # 41x
    'taam': 'tarry',         # 41x
    'kimkhat': 'half',       # 40x
    'ha': 'tooth',           # 40x
    'tulthum': 'three.thousand', # 40x
    'mangthang': 'perish',   # 40x
    'pusuak': 'mouth',       # 40x
    'tuaci': 'man',          # 39x
    'themkhat': 'part',      # 39x
    'se': 'dragon',          # 38x
    'taangko': 'proclaim',   # 38x
    'tausang': 'tower',      # 37x
    'bawngno': 'calf',       # 37x
    'hankhuk': 'sepulchre',  # 36x
    'tulli': 'four.thousand', # 35x
    'eima': 'our.god',       # 34x
    'hehnem': 'comfort',     # 34x
    'meikhu': 'smoke',       # 34x
    'leitawi': 'lend',       # 34x
    'kual': 'ring',          # 34x
    'giak': 'lodge',         # 33x
    'thawl': 'bottle',       # 32x
    'harp': 'harp',          # 32x
    'bel': 'trust',          # 32x
    'mawknapi': 'vanity',    # 31x
    'lamen': 'hope',         # 31x
    'khristian': 'brother',  # 31x
    'tawsaw': 'oak',         # 30x
    'khedap': 'shoe',        # 30x
    'hoh': 'today',          # 30x
    'tulnga': 'five.thousand', # 30x
    'leinuai': 'hell',       # 30x
    'suangpek': 'table',     # 29x
    'leiba': 'debt',         # 29x
    'lehhek': 'betray',      # 29x
    'moh': 'cake',           # 28x
    'kisiansuah': 'sanctify', # 28x
    'pumkhat': 'body',       # 28x
    'kin': 'god',            # 27x
    'khu': 'smoke',          # 27x
    'phei': 'woof',          # 27x
    'diang': 'rejoice',      # 27x
    'tulsagih': 'seven.thousand', # 27x
    'gitloh': 'wick',        # 26x
    'zekai': 'tarry',        # 26x
    'tavuan': 'bear',        # 26x
    'melhoih': 'fair',       # 25x
    'vut': 'ash',            # 25x
    'gum': 'pit',            # 25x
    'mul': 'hair',           # 24x
    'haltum': 'firebrand',   # 24x
    'liam': 'wound',         # 24x
    'tuancil': 'tread',      # 24x
    'dawl': 'chamber',       # 23x
    'maa': 'prosper',        # 23x
    'phiat': 'name',         # 23x
    'kol': 'loose',          # 23x
    'mangmat': 'dream',      # 23x
    'hell': 'hell',          # 23x
    'gunpi': 'river',        # 22x
    'vom': 'black',          # 22x
    'koh': 'thanksgiving',   # 22x
    'denglum': 'stone',      # 22x
    'jubilee': 'jubilee',    # 22x
    'dawivei': 'devil',      # 22x
    'bokvak': 'creep',       # 21x
    'tawlet': 'window',      # 21x
    'phalbi': 'winter',      # 21x
    'buan': 'clay',          # 21x
    'kheel': 'repent',       # 21x
    'phun': 'murmur',        # 21x
    'kih': 'abhor',          # 21x
    'tulguk': 'six.thousand', # 21x
    'tee': 'glitter',        # 21x
    'hangtakin': 'boldly',   # 21x
    'hawk': 'roar',          # 21x
    'hahkat': 'man',         # 21x
    'tuucing': 'shepherd',   # 20x
    'kimkota': 'round',      # 20x
    'bual': 'pool',          # 20x
    'thutheihna': 'knowledge', # 20x
    'gige': 'HAB',           # 20x - habitual "always" (ZNC §6.6.2.3)
    'thawhkik': 'resurrection', # 20x
    
    # Lower-frequency nouns (10-20x)
    'khek': 'change',        # 19x
    'myrrh': 'myrrh',        # 19x
    'zumhuai': 'shame',      # 19x
    'hakkol': 'yoke',        # 19x
    'dawm': 'god',           # 19x
    'gungal': 'river',       # 19x
    'thangzak': 'snare',     # 18x
    'vil': 'watch',          # 18x
    'bupa': 'centurion',     # 18x
    'pusuah': 'lord',        # 17x
    'pumpeeng': 'whole',     # 17x
    'hupa': 'shield',        # 17x
    'meet': 'usury',         # 17x
    'sungun': 'day',         # 17x
    'komau': 'thus',         # 17x
    'huihlak': 'air',        # 16x
    'ek': 'dung',            # 16x
    'ui': 'dog',             # 16x
    'seu': 'ephah',          # 16x
    'moi': 'young',          # 15x
    'tuucingpa': 'shepherd', # 15x
    'gilpi': 'cover',        # 15x
    'pakan': 'spoon',        # 15x
    'daitakin': 'quietly',   # 15x
    'golzaw': 'arch',        # 15x
    'vanpi': 'heaven',       # 15x
    'sehthumsuah': 'third',  # 15x
    'lano': 'colt',          # 14x
    'ngenthang': 'net',      # 14x
    'tazen': 'god',          # 14x
    'leiseek': 'brick',      # 13x
    'ciing': 'barren',       # 13x
    'leisung': 'earth',      # 13x
    'molhtum': 'stave',      # 13x
    'makpa': 'law',          # 13x
    'beeng': 'smite',        # 13x
    'dide': 'lord',          # 13x
    'tamngai': 'pipe',       # 12x
    'meh': 'pottage',        # 12x
    'suangcian': 'heap',     # 12x
    'tentan': 'imagination', # 12x
    'biing': 'hin',          # 12x
    'khul': 'fire',          # 12x
    'phin': 'provoke',       # 12x
    'guam': 'valley',        # 12x
    'khebai': 'lame',        # 12x
    'tambong': 'bath',       # 12x
    'lianpa': 'king',        # 12x
    'haihuai': 'foolishness', # 12x
    'kohkhit': 'thank',      # 12x
    'onik': 'onyx',          # 11x
    'meiphualpi': 'lake',    # 11x
    'lamlak': 'counsellor',  # 11x
    'buhtu': 'straw',        # 11x
    'tuum': 'water',         # 11x
    'geihual': 'crown',      # 11x
    'sek': 'hammer',         # 11x
    'eknel': 'cud',          # 11x
    'tulgiat': 'eighteen.thousand', # 11x
    'sual': 'floor',         # 11x
    'phiaukawi': 'sickle',   # 11x
    'mothak': 'bride',       # 11x
    'lamsang': 'evil',       # 11x
    'pingpei': 'whirlwind',  # 11x
    'tuumcip': 'water',      # 10x
    'almond': 'almond',      # 10x
    'tubang': 'morrow',      # 10x
    'tuzan': 'night',        # 10x
    'maavang': 'prosper',    # 10x
    'vompi': 'bear',         # 10x
    'tonu': 'mistress',      # 9x
    'bem': 'round',          # 9x
    'bit': 'full',           # 9x
    'zungbuh': 'ring',       # 9x
    'beem': 'homer',         # 9x
    'lawnsuk': 'down',       # 9x
    'guntui': 'river',       # 9x
    'liamma': 'wound',       # 9x
    'buannawng': 'mire',     # 9x
    'mantak': 'verily',      # 9x
    'donga': 'day',          # 8x
    'leilam': 'bow',         # 8x
    'meimatum': 'boil',      # 8x
    'vok': 'swine',          # 8x
    'mettol': 'head',        # 8x
    'mangmu': 'tribute',     # 8x
    'kuahawm': 'bottomless', # 8x
    'pukkhak': 'lest',       # 8x
    'liik': 'hand',          # 7x
    'tanzau': 'large',       # 7x
    'jasper': 'jasper',      # 7x
    'khutpi': 'thumb',       # 7x
    'liak': 'lord',          # 7x
    'kuamsung': 'valley',    # 7x
    'tamlawh': 'lamentation', # 7x
    'suplawh': 'lose',       # 7x
    'hagawi': 'gnash',       # 7x
    'thampek': 'good',       # 7x
    'gawt': 'hand',          # 6x
    'gulhgawng': 'ill',      # 6x
    'emerald': 'emerald',    # 6x
    'iik': 'breast',         # 6x
    'song': 'image',         # 6x
    'leilesuang': 'mason',   # 6x
    'suat': 'yoke',          # 6x
    'darik': 'dram',         # 6x
    'bualtui': 'water',      # 6x
    'kuum': 'firmament',     # 6x
    'efah': 'ephah',         # 5x
    'topaz': 'topaz',        # 5x
    'gerah': 'gerah',        # 5x
    'luak': 'vomit',         # 5x
    'zune': 'drink',         # 5x
    'epel': 'apple',         # 5x
    'lolai': 'field',        # 5x
    'suangtumpi': 'stone',   # 4x
    'awi': 'warm',           # 4x
    'supai': 'down',         # 2x
    'sunthapai': 'long',     # 2x
    
    # Additional nouns from corpus analysis (export POS consolidation)
    'tau': 'altar',          # altar/tower (NOT signal)
    'gim': 'suffering',      # suffering/toil
    'vei': 'time',           # time/occasion
    'lung': 'heart',         # heart/stone
    # Note: mite should be analyzed as mi-te (person-PL), not a lexeme
    'nungzui': 'disciple',   # disciple/follower
    'pi': 'grandmother',     # grandmother/ancestor
    'gei': 'edge',           # edge/border
    'sai': 'ashes',          # ashes/dust
    'sun': 'basket',         # basket
    'hei': 'path',           # path/way
    'vui': 'dust',           # dust/powder
    'gah': 'branch',         # branch/bough
    'khuam': 'darkness',     # darkness/night
    'kung': 'trunk',         # trunk/tree
    'lah': 'lamp',           # lamp/light
    'lui': 'river',          # river/stream
    'kim': 'nation',         # nation (also 'whole')
    'khan': 'generation',    # generation/age
    'kuam': 'plain',         # plain/valley
    'khau': 'rope',          # rope/cord
    'sal': 'slave',          # slave/servant
    'cil': 'beginning',      # beginning/origin
    'mel': 'appearance',     # appearance/form
    'guak': 'back',          # back/rear
    'bu': 'heap',            # heap/group
    'zia': 'manner',         # manner/way
    'mawhsak': 'adversary',  # adversary/enemy
    'lehdo': 'rebellious',   # rebellious one
    'khuk': 'pool',          # pool/knee
    'hel': 'hell',           # hell/underworld
    # Note: 'gamh' removed - there is no Form II of 'gam', it was conflicting with gam-hal
    'gilo': 'enemy',         # enemy/foe
    'cik': 'fountain',       # fountain/spring
    'len': 'net',            # net/snare
    'phet': 'twin',          # twin
    'phual': 'field',        # field/plain
    'paktat': 'fornication', # fornication/harlotry
    'dum': 'siege.mound',    # siege mound
    'peek': 'breadth',       # breadth/width
    'zai': 'song',           # song/psalm
    'kawng': 'road',         # road/path
    'teek': 'master',        # master/lord
    'gu': 'tree',            # tree (variant)
    'zo': 'south',           # south
    'kop': 'pair',           # pair/couple
    'dalna': 'hindrance',    # hindrance/obstacle
    'gak': 'trap',           # trap/snare
    'liah': 'circuit',       # circuit/round
    'siit': 'sacrifice',     # sacrifice/offering
    'pum': 'body',           # body/trunk
    'nawl': 'place',         # place/area
    'sungnung': 'inner.room', # inner room/chamber
    'leilak': 'dust',        # dust (variant)
    'nuh': 'mother',         # mother
    'liim': 'wing',          # wing
    'thongkia': 'prison',    # prison/jail
    'mo': 'bride',           # bride
    'meima': 'wound',        # wound/injury
}


# Noun stem type classification
# Types: free (standalone attestation), bound (compounds only), ghost (not attested)
# Auto-generated from corpus analysis
NOUN_STEM_TYPES = {
    'ainungin': 'bound',
    'aisan': 'free',
    'akin': 'bound',
    'aksi': 'free',
    'alang': 'free',
    'almang': 'bound',
    'alun': 'bound',
    'an': 'free',
    'angkawm': 'free',
    'angtanpih': 'free',
    'anhai': 'free',
    'ankhamval': 'bound',
    'ankhing': 'free',
    'anlom': 'free',
    'anlui': 'free',
    'anlum': 'free',
    'annel': 'free',
    'anpal': 'free',
    'anphual': 'free',
    'ante': 'free',
    'anvai': 'free',
    'anvui': 'free',
    'anzap': 'bound',
    'atgawp': 'bound',
    'atnen': 'free',
    'ausan': 'free',
    'aw': 'free',
    'awh': 'free',
    'awn': 'free',
    'awng': 'free',
    'awngsuak': 'free',
    'awngsuk': 'free',
    'baak': 'free',
    'baih': 'free',
    'bakbak': 'free',
    'balkham': 'free',
    'balkhiat': 'free',
    'balzan': 'free',
    'ban': 'free',
    'banbuh': 'bound',
    'bangpian': 'free',
    'bangtan': 'free',
    'bawk': 'free',
    'bawlsaksa': 'bound',
    'bawlte': 'free',
    'bawng': 'free',
    'bawngtal': 'free',
    'beel': 'free',
    'beh': 'free',
    'bemeh': 'free',
    'bengbeng': 'bound',
    'bepi': 'free',
    'biakinn': 'free',
    'biakna': 'free',
    'biaknatau': 'free',
    'biang': 'free',
    'bil': 'free',
    'bilteep': 'free',
    'bingphawn': 'free',
    'bom': 'free',
    'buangawp': 'bound',
    'buk': 'free',
    'bul': 'free',
    'bulh': 'free',
    'bulom': 'bound',
    'bum': 'free',
    'bung': 'free',
    'bungpi': 'free',
    'bungsuk': 'free',
    'bupkhat': 'free',
    'ciangto': 'free',
    'ciatah': 'free',
    'ciimsa': 'bound',
    'cilphih': 'free',
    'cilun': 'free',
    'cin': 'free',
    'cing': 'free',
    'cingh': 'free',
    'cingtaak': 'free',
    'cipnelh': 'free',
    'dahzaw': 'free',
    'daihual': 'free',
    'daitui': 'free',
    'dal': 'free',
    'dang': 'free',
    'dapphah': 'bound',
    'dapphahin': 'free',
    'daupaina': 'free',
    'dawilut': 'bound',
    'dawt': 'free',
    'dawtlet': 'free',
    'dawtna': 'ghost',
    'deihna': 'free',
    'del': 'bound',
    'delh': 'free',
    'dengkham': 'free',
    'dengtan': 'free',
    'dik': 'free',
    'dimlah': 'free',
    'dimsak': 'free',
    'dimval': 'free',
    'dimzawh': 'free',
    'dingtang': 'free',
    'dinlam': 'free',
    'domsak': 'bound',
    'dosak': 'free',
    'dupsan': 'free',
    'eh': 'free',
    'ekbuk': 'free',
    'elkul': 'free',
    'et': 'free',
    'ga': 'free',
    'gai': 'free',
    'gaisak': 'free',
    'gal': 'free',
    'galbanum': 'free',
    'galdalna': 'free',
    'galdo': 'free',
    'galhang': 'free',
    'galhiam': 'free',
    'galkap': 'free',
    'galkhat': 'free',
    'galkidal': 'bound',
    'galkisim': 'bound',
    'galmatin': 'free',
    'galsimna': 'free',
    'galvan': 'free',
    'galvil': 'free',
    'gam': 'free',
    'gamhluah': 'free',
    'gamkhing': 'free',
    'gamla': 'free',
    'gammi': 'free',
    'gamtangzo': 'free',
    'gamtatna': 'free',
    'ganbuk': 'free',
    'ganhing': 'free',
    'gankhahna': 'free',
    'ganpi': 'bound',
    'gat': 'free',
    'gawhna': 'free',
    'gawng': 'free',
    'gehsa': 'free',
    'giah': 'free',
    'gial': 'free',
    'gialbem': 'free',
    'gialhek': 'free',
    'gih': 'free',
    'gihna': 'free',
    'gilnat': 'bound',
    'gimbawl': 'free',
    'gimkhop': 'bound',
    'gimluat': 'free',
    'gimpiak': 'free',
    'gimsak': 'free',
    'gimsakzaw': 'free',
    'ginalopi': 'bound',
    'gindan': 'free',
    'gingkhia': 'free',
    'gisuang': 'free',
    'gitta': 'free',
    'gkhutah': 'bound',
    'guah': 'free',
    'guahmal': 'free',
    'gualzawh': 'free',
    'guh': 'free',
    'guklam': 'free',
    'gunkuam': 'free',
    'gupha': 'free',
    'haksat': 'free',
    'halnelh': 'free',
    'ham': 'free',
    'hansuah': 'free',
    'hanzia': 'free',
    'hat': 'free',
    'hawh': 'free',
    'hawhsuk': 'free',
    'hawkmai': 'free',
    'hawmthawh': 'free',
    'heeksat': 'free',
    'heektat': 'free',
    'hehpihna': 'free',
    'heikhiat': 'bound',
    'heikik': 'bound',
    'heisakzaw': 'free',
    'heksuk': 'free',
    'hektoh': 'bound',
    'hiang': 'free',
    'hikcip': 'free',
    'hing': 'free',
    'hingmat': 'free',
    'hisak': 'free',
    'hit': 'bound',
    'ho': 'free',
    'hoihna': 'free',
    'hon': 'free',
    'huat': 'free',
    'huathuai': 'free',
    'humpinelkai': 'free',
    'hun': 'free',
    'ihih': 'free',
    'ihkhiatsak': 'bound',
    'ihkhiattoh': 'bound',
    'ihkik': 'bound',
    'ikkhiat': 'free',
    'inn': 'free',
    'innhikpi': 'free',
    'innkuan': 'free',
    'innkuanpih': 'free',
    'innlelo': 'free',
    'innsual': 'bound',
    'innzom': 'free',
    'ipen': 'bound',
    'ipip': 'bound',
    'isuksak': 'bound',
    'itna': 'free',
    'kah': 'free',
    'kaihna': 'free',
    'kal': 'free',
    'kalaoh': 'free',
    'kam': 'free',
    'kamhan': 'bound',
    'kammal': 'free',
    'kamneem': 'free',
    'kampau': 'free',
    'kamphen': 'free',
    'kamsang': 'free',
    'kamsangpa': 'free',
    'kamtai': 'free',
    'kangtum': 'free',
    # kapin: removed from 'free' - it's kap-in "weep-ERG"
    'kauphe': 'free',
    'kawm': 'free',
    'kawngsa': 'free',
    'ke': 'ghost',  # 'foot' - not attested; 'ke' in corpus is ke'n (1SG-ERG)
    'keel': 'free',
    'ken': 'free',
    'kent': 'ghost',
    'keu': 'free',
    'keutumna': 'free',
    'kha': 'free',
    'khah': 'free',
    'khai': 'free',
    'khaici': 'free',
    'khak': 'free',
    'khaleh': 'free',
    'khang': 'free',
    'khanlua': 'free',
    'khat': 'free',
    'khatzong': 'free',
    'khauhpen': 'bound',
    'khaute': 'free',
    'khawilevulh': 'free',
    'kheh': 'free',
    'khehsa': 'free',
    'khelbai': 'free',
    'khelg': 'bound',
    'khelkom': 'free',
    'khelpi': 'free',
    'khelpil': 'bound',
    'khengak': 'free',
    'khengval': 'bound',
    'khenkhen': 'bound',
    'khetbuk': 'free',
    'khete': 'free',
    'khi': 'free',
    'khialh': 'free',
    'khialhna': 'free',
    'khitah': 'free',
    'khon': 'free',
    'khongkhai': 'free',
    'khua': 'free',
    'khuacing': 'free',
    'khuahun': 'free',
    'khuaizu': 'free',
    'khuakulhah': 'free',
    'khualzin': 'free',
    'khuamial': 'free',
    'khuangbai': 'free',
    'khuangneu': 'free',
    'khuangtung': 'free',
    'khuapi': 'free',
    'khuavak': 'free',
    'khukdin': 'free',
    'khupnelh': 'bound',
    'khut': 'free',
    'khutpeekmai': 'free',
    'khutsung': 'free',
    'kial': 'free',
    'kibangmah': 'bound',
    'kibatloh': 'bound',
    'kiciamteh': 'free',
    'kihaimuan': 'bound',
    'kihalnel': 'bound',
    'kiheikhial': 'free',
    'kihelh': 'free',
    'kihelhsak': 'free',
    'kihuanna': 'free',
    'kikalsung': 'free',
    'kikantel': 'free',
    'kikap': 'bound',
    'kikep': 'free',
    'kikhap': 'bound',
    'kikhat': 'free',
    'kikhek': 'free',
    'kikhungsuk': 'free',
    'kilang': 'free',
    'kilungso': 'free',
    'kiman': 'free',
    'kimang': 'free',
    'kimu': 'free',
    'kimuhsuk': 'free',
    'kinailua': 'free',
    'kinawh': 'free',
    'kineihna': 'free',
    'kinenniam': 'free',
    'kingah': 'free',
    'kinim': 'free',
    'kipaihpehsak': 'bound',
    'kiphop': 'free',
    'kiphuhna': 'free',
    'kiphuk': 'free',
    'kiphupai': 'free',
    'kipiak': 'free',
    'kiptaka': 'free',
    'kipuak': 'free',
    'kisehkhenna': 'free',
    'kiselsim': 'bound',
    'kisunen': 'free',
    'kisunna': 'bound',
    'kisuvui': 'free',
    'kisuzan': 'free',
    'kitankhiat': 'free',
    'kitap': 'bound',
    'kitawh': 'free',
    'kitawhnawi': 'bound',
    'kithamuan': 'bound',
    'kithawi': 'free',
    'kithehkha': 'free',
    'kithehkhak': 'free',
    'kithuneih': 'bound',
    'kitut': 'free',
    'kizim': 'free',
    'kizutna': 'free',
    'komdep': 'free',
    'kongkha': 'bound',
    'kongzing': 'free',
    'koptai': 'bound',
    'kuancil': 'free',
    'kuang': 'free',
    'kuangzawn': 'free',
    'kuankha': 'free',
    'kuankhawm': 'free',
    'kuankhop': 'free',
    'kuantoh': 'free',
    'kulhkongkhak': 'bound',
    'kulhnei': 'free',
    'kum': 'free',
    'kumpi': 'free',
    'kumpipa': 'free',
    'kun': 'free',
    'laam': 'free',
    'lahkim': 'bound',
    'lai': 'free',
    'laibu': 'free',
    'laitengun': 'free',
    'laksak': 'free',
    'lambeh': 'bound',
    'lamet': 'free',
    'lamgal': 'free',
    'lampi': 'free',
    'lamzan': 'free',
    'lang': 'free',
    'lanluat': 'free',
    'lanu': 'free',
    'laphuak': 'free',
    'lasa': 'free',
    'lathuah': 'free',
    'lau': 'free',
    'lawm': 'free',
    'lawngpi': 'free',
    'lee': 'free',
    'leem': 'free',
    'leeng': 'free',
    'leenggahzu': 'free',
    'leenggahzucil': 'free',
    'leenggui': 'free',
    'leetkhia': 'bound',
    'lehdelh': 'free',
    'lehdozaw': 'free',
    'lehgamtat': 'free',
    'lehkhak': 'free',
    'lehnawhzo': 'free',
    'lehnawt': 'free',
    'lehthuk': 'free',
    'lehzuihkik': 'free',
    'leibeel': 'free',
    'leilulam': 'free',
    'leitang': 'free',
    'leitung': 'free',
    'leivang': 'free',
    'lekua': 'bound',
    'lelun': 'free',
    'lengsuak': 'free',
    'lenkip': 'free',
    'letsong': 'free',
    'liangkaih': 'free',
    'liangko': 'free',
    'lianpi': 'free',
    'liat': 'free',
    'lik': 'free',
    'liknelh': 'free',
    'lim': 'free',
    'limliam': 'free',
    'lin': 'free',
    'linglawnsak': 'free',
    'lohkik': 'free',
    'lokhul': 'bound',
    'lonawl': 'free',
    'lote': 'free',
    'lotgawp': 'bound',
    'lotkhiat': 'free',
    'lsak': 'bound',
    'lu': 'free',
    'luakkhia': 'free',
    'luang': 'free',
    'luanghawm': 'free',
    'luidung': 'free',
    'lukhu': 'free',
    'lukolh': 'free',
    'lum': 'free',
    'lungdamsak': 'free',
    'lunggimzaw': 'free',
    'lunghimawh': 'free',
    'lungkhauh': 'free',
    'lungmuang': 'free',
    'lungphamawh': 'free',
    'lungsim': 'free',
    'lungtang': 'free',
    'luppih': 'free',
    'lut': 'free',
    'lutang': 'free',
    'luzepna': 'bound',
    'maan': 'free',
    'maangmuh': 'free',
    'mahmah': 'free',
    'mai': 'free',
    'maikun': 'free',
    'mailam': 'free',
    'maimang': 'free',
    'maipuksuk': 'free',
    'maitang': 'free',
    'makaih': 'free',
    'makaipi': 'free',
    'makhelh': 'free',
    'mangbuh': 'free',
    'mangbuhman': 'free',
    'manglian': 'bound',
    'mangzo': 'free',
    'manlan': 'free',
    'manlang': 'free',
    'manna': 'free',
    'mansiang': 'free',
    'masiah': 'free',
    'matutzawh': 'bound',
    'mavansak': 'bound',
    'mawhna': 'free',
    'mawhnei': 'free',
    'mawhzon': 'free',
    'mawklot': 'free',
    'mawkphat': 'free',
    'mawkval': 'free',
    'mawl': 'free',
    'mawlpih': 'free',
    'mehbeel': 'free',
    'mehteh': 'free',
    'meidawi': 'free',
    'meidawilawh': 'free',
    'meikhuam': 'free',
    'meikhuk': 'free',
    'meilah': 'free',
    'meilak': 'bound',
    'meimapi': 'bound',
    'meithau': 'free',
    'meltheih': 'free',
    'metna': 'free',
    'mi': 'free',
    'miaimuai': 'free',
    'mial': 'free',
    'midang': 'free',
    'migilo': 'free',
    'migina': 'free',
    'mihai': 'free',
    'mihing': 'free',
    'mihoih': 'free',
    'mihon': 'free',
    'mihonpi': 'free',
    'milim': 'free',
    'min': 'free',
    'minam': 'free',
    'miniam': 'bound',
    'minthang': 'free',
    'mipa': 'free',
    'mipil': 'free',
    'misi': 'free',
    'mit': 'free',
    'mithuman': 'bound',
    'mitlawt': 'free',
    'mittaw': 'free',
    'mivom': 'bound',
    'mohlawh': 'free',
    'mohneu': 'free',
    'moilai': 'free',
    'moken': 'free',
    'moliah': 'free',
    'mongciik': 'free',
    'monu': 'free',
    'mual': 'free',
    'mualtung': 'free',
    'muanhuai': 'free',
    'mudah': 'free',
    'muh': 'free',
    'mun': 'free',
    'mung': 'bound',
    'musak': 'free',
    'naita': 'free',
    'nak': 'free',
    'nakleh': 'free',
    'nakpi': 'free',
    'nakvang': 'free',
    'nalamdang': 'free',
    'nam': 'free',
    'namkim': 'free',
    'namun': 'free',
    'nasem': 'free',
    'nasempa': 'free',
    'nasepna': 'free',
    'nasia': 'free',
    'natui': 'free',
    'naudom': 'free',
    'naupa': 'free',
    'naupang': 'free',
    'nausuah': 'free',
    'nawi': 'free',
    'nawk': 'free',
    'nawlhui': 'free',
    'nawng': 'free',
    'neel': 'free',
    'neih': 'free',
    'nengkia': 'free',
    'nengneng': 'free',
    'netniamna': 'free',
    'ngaihno': 'free',
    'ngaihsutna': 'free',
    'ngasa': 'free',
    'ngawhdawn': 'free',
    'ngawng': 'free',
    'ngeina': 'free',
    'ngel': 'free',
    'ngentel': 'free',
    'nget': 'free',
    'ngim': 'free',
    'ngunlekham': 'free',
    'nguumkhia': 'free',
    'nhai': 'bound',
    'ni': 'free',
    'nilh': 'free',
    'nin': 'free',
    'ninikikhol': 'ghost',
    'ninkikhol': 'bound',
    'ninsak': 'free',
    'nisuah': 'free',
    'nisuhkung': 'free',
    'nkungno': 'bound',
    'nneng': 'bound',
    'no': 'free',
    'nu': 'free',
    'nuaikiat': 'free',
    'nuak': 'free',
    'nuam': 'free',
    'nuamsa': 'free',
    'numei': 'free',
    'nun': 'free',
    'nungak': 'free',
    'nungdal': 'bound',
    'nungdelh': 'free',
    'nungguh': 'free',
    'nuntakna': 'free',
    'nusia': 'free',
    'olna': 'free',
    'omlai': 'free',
    'omzia': 'free',
    'onikha': 'free',
    'pa': 'free',
    'paikhiato': 'free',
    'paisan': 'free',
    'pal': 'bound',
    'palhngulh': 'free',
    'pangbet': 'bound',
    'panun': 'free',
    'pasal': 'free',
    'pasian': 'free',
    'patkhau': 'bound',
    'pawi': 'free',
    'pawl': 'free',
    'peem': 'free',
    'peengkul': 'free',
    'pei': 'free',
    'peikalh': 'bound',
    'peikual': 'free',
    'pel': 'free',
    'pelhem': 'free',
    'pelhzah': 'free',
    'pente': 'free',
    'petlum': 'free',
    'phaknat': 'bound',
    'phamawh': 'free',
    'phansak': 'free',
    'phattua': 'bound',
    'phawkkik': 'free',
    'phawng': 'free',
    'pheek': 'free',
    'pheeng': 'bound',
    'phehkeu': 'free',
    'pheituam': 'free',
    'phiatkhiat': 'free',
    'phiatmai': 'free',
    'phinna': 'free',
    'phok': 'bound',
    'phottohsakkik': 'bound',
    'phuah': 'free',
    'phualpi': 'free',
    'phuang': 'free',
    'phuhsa': 'free',
    'phuk': 'free',
    'phukhia': 'free',
    'phula': 'free',
    'phung': 'free',
    'phunsan': 'free',
    'pian': 'free',
    'pianzia': 'free',
    'piklup': 'free',
    'piksan': 'bound',
    'pilna': 'free',
    'pistakhio': 'free',
    'pomcip': 'bound',
    'pomlai': 'free',
    'psap': 'free',
    'puan': 'free',
    'puandum': 'bound',
    'puangin': 'free',
    'puankek': 'bound',
    'puantualpi': 'free',
    'puknah': 'free',
    'pul': 'free',
    'pulak': 'free',
    'pusawn': 'free',
    'pute': 'free',
    'sa': 'free',
    'saanin': 'free',
    'sabak': 'bound',
    'sabuai': 'free',
    'sagih': 'free',
    'sakhati': 'bound',
    'sakhital': 'free',
    'sakikh': 'bound',
    'sakol': 'free',
    'samsia': 'free',
    'samuat': 'free',
    'samulpuan': 'free',
    'sanang': 'free',
    'sanen': 'bound',
    'sang': 'free',
    'sanggam': 'free',
    'sanggampa': 'free',
    'sangkil': 'free',
    'sankhit': 'free',
    'sathaukhal': 'free',
    'sattansak': 'free',
    'sau': 'free',
    'sauveipi': 'free',
    'sawkkhawm': 'bound',
    'sawltak': 'free',
    'sawmgiat': 'free',
    'sawtlai': 'free',
    'seel': 'free',
    'seeng': 'free',
    'sehkhen': 'free',
    'sen': 'bound',
    'set': 'bound',
    'si': 'free',
    'sia': 'free',
    'siakkhia': 'free',
    'siakkhiat': 'free',
    'sial': 'free',
    'sialh': 'ghost',  # 'tomorrow' - not attested; Tedim uses 'zing' instead
    'siampi': 'free',
    'siampipa': 'free',
    'siamte': 'free',
    'siang': 'free',
    'siangtho': 'free',
    'sianthosaksa': 'free',
    'siasa': 'free',
    'siatgamtat': 'bound',
    'siatna': 'free',
    'sihna': 'free',
    'sik': 'free',
    'sikkeuka': 'bound',
    'siknazat': 'free',
    'sikzum': 'bound',
    'sila': 'free',
    'silh': 'free',
    'silngo': 'free',
    'sim': 'free',
    'simsakhi': 'free',
    'simzel': 'free',
    'sin': 'free',
    'sing': 'free',
    'singbek': 'bound',
    'singhiangpi': 'bound',
    'singkung': 'free',
    'sisan': 'free',
    'sot': 'free',
    'stak': 'bound',
    'suah': 'free',
    'suahloh': 'free',
    'suakmasa': 'free',
    'suangat': 'bound',
    'suangpak': 'free',
    'suangphahpek': 'free',
    'suangtang': 'free',
    'suangte': 'free',
    'suankhiat': 'free',
    'suanlekhak': 'free',
    'sucim': 'free',
    'sum': 'free',
    'sumkhek': 'bound',
    'sunga': 'free',
    'sungpa': 'free',
    'sungtengun': 'free',
    'sungvan': 'free',
    'sunlet': 'free',
    'sunlezanin': 'free',
    'suntang': 'bound',
    'supna': 'free',
    'susiazaw': 'free',
    'suun': 'free',
    'taak': 'free',
    'taal': 'free',
    'taaubeelin': 'free',
    'takhialsak': 'free',
    'tal': 'free',
    'taltang': 'free',
    'tamngaikop': 'free',
    'tamzawk': 'bound',
    'taneu': 'bound',
    'tangban': 'free',
    'tangngol': 'free',
    'tangteuh': 'free',
    'tangval': 'free',
    'tanu': 'free',
    'tanzum': 'bound',
    'tapa': 'free',
    'tapeeng': 'free',
    'tatolh': 'free',
    'tausangpi': 'free',
    'taute': 'free',
    'tawhtang': 'free',
    'tawiteh': 'free',
    'tawlbawkpi': 'free',
    'tawlnga': 'free',
    'tawmkha': 'free',
    'tawmno': 'free',
    'tawnlang': 'free',
    'tawnpuk': 'free',
    'tawntung': 'free',
    'tecipanna': 'free',
    'teeknu': 'free',
    'teeksia': 'bound',
    'teem': 'free',
    'teembaw': 'free',
    'teemsak': 'free',
    'teep': 'free',
    'teepkang': 'free',
    'tehteh': 'bound',
    'tei': 'free',
    'teibul': 'free',
    'teikhawh': 'free',
    'teipak': 'free',
    'teipi': 'free',
    'teitei': 'free',
    'telkheh': 'free',
    'tennop': 'bound',
    'tenpak': 'bound',
    'tenpih': 'free',
    'tensak': 'free',
    'tentheih': 'free',
    'tep': 'free',
    'thacial': 'free',
    'thacingzaw': 'free',
    'thagol': 'free',
    'thagui': 'free',
    'thah': 'free',
    'thahzawh': 'free',
    'thal': 'free',
    'thalkhau': 'free',
    'thalpuk': 'bound',
    'thaltang': 'free',
    'thau': 'free',
    'thawnkham': 'free',
    'theem': 'free',
    'theimoh': 'free',
    'themlen': 'free',
    'thu': 'free',
    'thuciamna': 'free',
    'thudamin': 'free',
    'thugik': 'free',
    'thuhaksa': 'free',
    'thuhilhna': 'free',
    'thuhoih': 'free',
    'thukan': 'free',
    'thukham': 'free',
    'thukimnasa': 'bound',
    'thuko': 'free',
    'thukzawh': 'free',
    'thumong': 'free',
    'thumvei': 'free',
    'thupeel': 'bound',
    'thupha': 'free',
    'thupiak': 'free',
    'thupiakna': 'free',
    'thupiangsa': 'bound',
    'thupina': 'free',
    'thusim': 'free',
    'thutanna': 'free',
    'thuthak': 'free',
    'thuvaan': 'bound',
    'tlup': 'bound',
    'tol': 'free',
    'tolhkhiat': 'free',
    'tom': 'free',
    'tomkhano': 'free',
    'tomlua': 'bound',
    'topa': 'free',
    'totawm': 'free',
    'tuakpe': 'bound',
    'tual': 'free',
    'tuam': 'free',
    'tuami': 'free',
    'tuankhamin': 'free',
    'tuanthu': 'free',
    'tuat': 'free',
    'tui': 'free',
    'tuikuangpi': 'free',
    'tuipi': 'free',
    'tuipiakna': 'free',
    'tukimin': 'free',
    'tukkilh': 'bound',
    'tulzum': 'free',
    'tumsuak': 'free',
    'tumsuk': 'free',
    'tumtheih': 'free',
    'tunai': 'free',
    'tungnun': 'bound',
    'tunitak': 'free',
    'tunna': 'free',
    'tunsuk': 'free',
    'tunu': 'free',
    'tunzaw': 'free',
    'tupkhiat': 'free',
    'tuuhon': 'free',
    'tuulebawng': 'bound',
    'tuulekeelno': 'free',
    'tuumul': 'free',
    'tuuno': 'free',
    'tuusiah': 'free',
    'tuuvun': 'free',
    'tuzum': 'free',
    'uili': 'free',
    'uisi': 'free',
    'ukna': 'free',
    'ukpi': 'free',
    'umcih': 'free',
    'unau': 'free',
    'upa': 'free',
    'upmawhna': 'free',
    'upna': 'free',
    'utong': 'free',
    'vahui': 'free',
    'vaihawm': 'free',
    'vaikhakna': 'free',
    'vakhu': 'free',
    'val': 'free',
    'valzaw': 'free',
    'van': 'free',
    'vanging': 'free',
    'vanglian': 'free',
    'vangliatna': 'free',
    'vangsung': 'free',
    'vankia': 'free',
    'vantung': 'free',
    'vantungmi': 'free',
    'vanzat': 'bound',
    'vatgawp': 'free',
    'vengvang': 'bound',
    'vu': 'free',
    'vuak': 'free',
    'vuhsak': 'free',
    'vuk': 'free',
    'vun': 'free',
    'vutluahna': 'free',
    'vutvang': 'free',
    'wcikah': 'bound',
    'wivak': 'bound',
    'wmvalh': 'bound',
    'zaguk': 'free',
    'zahko': 'free',
    'zahkoh': 'bound',
    'zakma': 'free',
    'zakphet': 'bound',
    'zalesawmnga': 'free',
    'zalh': 'free',
    'zali': 'free',
    'zan': 'free',
    'zantaamsak': 'free',
    'zaptel': 'free',
    'zathum': 'free',
    'zatna': 'free',
    'zawh': 'free',
    'zawl': 'free',
    'zawsop': 'free',
    'zeizai': 'free',
    'zi': 'free',
    'zial': 'free',
    'zialetong': 'bound',
    'zialin': 'free',
    'zialkhia': 'free',
    'zialkhol': 'free',
    'ziazua': 'free',
    'zimna': 'free',
    'zindo': 'free',
    'zineu': 'free',
    'zing': 'free',
    'zingsang': 'free',
    'zingtung': 'bound',
    'zinzin': 'free',
    'zolua': 'free',
    'zom': 'free',
    'zongpah': 'free',
    'zongsat': 'bound',
    'zosakhi': 'free',
    'zothawh': 'bound',
    'zuak': 'free',
    'zual': 'free',
    'zuaugen': 'free',
    'zuausiam': 'bound',
    'zuauthu': 'free',
    'zuibup': 'free',
    'zuk': 'free',
    'zuksak': 'free',
    'zulhtat': 'bound',
    'zulhzau': 'free',
}

# Transparent proper nouns - show Tedim etymology in glossing
# These are proper nouns in context but have meaningful Tedim morphology
TRANSPARENT_PROPER_NOUNS = {
    # Divine terms with Tedim etymology
    'Pasian': ('Pasian', 'God'),           # pa-sian 'father-holy' → God
    'Topa': ('Topa', 'Lord'),              # to-pa 'master-male' → Lord  
    'Lungdamna': ('lungdam-na', 'good.news-NMLZ'),  # lungdam 'rejoice' + -na → Gospel
    'Khanpugol': ('khan-pu-gol', 'generation-father-origin'),  # ancestor/patriarch
}

# Proper nouns (don't gloss with lowercase - return as-is with uppercase marker)
# Expanded from corpus frequency analysis - 200+ entries
PROPER_NOUNS = {
    # Jesus and titles (foreign names - no Tedim etymology)
    'Jesuh', 'Jesus', 'Khrih', 'Christ', 'Kristu', 'Zeisu', 'Khrih',
    
    # Old Testament figures - Patriarchs
    'Abraham', 'Abram', 'Isaac', 'Jakob', 'Jakobu', 'Israel', 'Srael', 'Josef', 'Joseph',
    'Noah', 'Adam', 'Eve', 'Seth', 'Enoch', 'Methuselah', 'Lamech',
    'Sarah', 'Sarai', 'Rebekah', 'Leah', 'Rachel',  # Matriarchs
    'Issakhar', 'Issachar', 'Reuben', 'Simeon', 'Levi', 'Judah', 'Zebulun',  # Tribes
    'Kohath', 'Gershon', 'Merari', 'Hori', 'Oreb',  # Levite clans and others
    
    # Old Testament - Moses era
    'Moses', 'Aaron', 'Joshua', 'Caleb', 'Miriam', 'Korah', 'Phinehas',
    
    # Old Testament - Judges & Kings
    'David', 'Solomon', 'Saul', 'Samuel', 'Eli', 'Gideon', 'Samson',
    'Jeroboam', 'Rehoboam', 'Ahab', 'Jehoshafat', 'Hezekiah', 'Josiah',
    'Nebukhadnezzar', 'Nebuchadnezzar', 'Belshazzar', 'Darius', 'Cyrus',
    'Abimelek', 'Abimelech', 'Abner', 'Absalom', 'Joab', 'Jonathan',
    
    # Old Testament - Prophets
    'Elijah', 'Elisha', 'Isaiah', 'Jeremiah', 'Ezekiel', 'Daniel',
    'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
    'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
    'Nathan', 'Zadok',
    
    # Old Testament - Other figures
    'Job', 'Esau', 'Levi', 'Reuben', 'Benjamin', 'Judah', 'Manasseh',
    'Efraim', 'Ephraim', 'Gad', 'Simeon', 'Naphtali', 'Naftali', 'Asher',
    'Zebulun', 'Issachar', 'Dan', 'Ishmael', 'Ruth', 'Boaz', 'Rahab',
    'Shuah', 'Giloh', 'Gilopa',  # Added
    
    # Proper nouns that are homophones of common Tedim words
    # These need capitalized forms to disambiguate from common words
    'Sin',   # Wilderness of Sin (common word 'sin' = near/liver)
    'Gilo',  # Place name Giloh (common word 'gilo' = enemy)
    'Giah',  # Place name (common word 'giah' = camp)
    'Zin',   # Wilderness of Zin (common word 'zin' = travel)
    'Zia',   # Person name (common word 'zia' = manner)
    
    # New Testament figures - Apostles
    'Johan', 'John', 'Peter', 'Piter', 'Paul', 'Paulus', 'Simon', 'Andru', 'Andrew',
    'James', 'Zebedi', 'Zebedee', 'Matthew', 'Mark', 'Luke', 'Thomas', 'Philip',
    'Bartholomew', 'Judas', 'Thaddaeus', 'Matthias',
    
    # New Testament - Other figures  
    'Maria', 'Mary', 'Martha', 'Lazarus', 'Nicodemus', 'Stephen', 'Stefanus',
    'Timothy', 'Titus', 'Barnabas', 'Silas', 'Apollos', 'Priscilla', 'Aquila',
    'Pilat', 'Pilate', 'Herod', 'Caiaphas', 'Annas',
    
    # Places - Old Testament
    'Egypt', 'Babylon', 'Jerusalem', 'Judah', 'Samaria', 'Damaskas', 'Damascus',
    'Moab', 'Edom', 'Ammon', 'Syria', 'Assiria', 'Assyria', 'Kanaan', 'Canaan',
    'Gilead', 'Zion', 'Sinai', 'Horeb', 'Bethel', 'Bethlehem', 'Ai',
    'Jordan', 'Filistia', 'Philistia', 'Khaldea', 'Chaldea',
    'Midian', 'Persia', 'Media', 'Sheba',
    'Lebanon', 'Hebron', 'Hiopia', 'Ethiopia', 'Libya', 'Put',  # Added
    'Horonaim', 'Makpelah', 'Efrath', 'Ephrath', 'Kishon', 'Seba',  # Added
    'Rameses', 'Marah', 'Berea',  # Added
    
    # Places - New Testament
    'Galilee', 'Nazareth', 'Nazaret', 'Kapernaum', 'Capernaum',
    'Roma', 'Rome', 'Corinth', 'Ephesus', 'Antioch', 'Athens',
    'Macedonia', 'Galatia', 'Thessalonica', 'Judea', 'Tarsus',
    
    # Groups/Peoples
    'Jew', 'Farisi', 'Pharisee', 'Sadducee', 'Gentail', 'Gentile',
    'Levite', 'Pawi', 'Faro', 'Pharaoh', 'Kherub', 'Cherub', 'Satan',
    'Amor', 'Amorite', 'Hittite', 'Midianite',
    
    # Lowercase forms found in corpus (need to match case-insensitively)
    'israel', 'jesuh', 'jerusalem', 'egypt', 'babylon', 'judah',
    'saul', 'aaron', 'abraham', 'paul', 'kanaan', 'ammon', 'assiria',
    'samuel', 'sabbath', 'isaac', 'absalom', 'zion', 'samaria', 'ahab',
    'nebukhadnezzar', 'abimelek', 'abner', 'abram', 'isaiah', 'ishmael',
    'damaskas', 'zadok', 'pilat', 'satan', 'naftali', 'khaldea',
    'gentail', 'filistia', 'amor', 'kherub',
    # Note: 'ai' removed - conflicts with common word 'ai' (lot for casting)
    # Additional proper nouns from corpus frequency analysis
    'ahaz', 'samson', 'midian', 'amalek', 'asher', 'nathan', 'saihadial',
    'moab', 'edom', 'gilead', 'sheba', 'laban', 'rebekah', 'leah', 'rachel',
    'bethel', 'sodom', 'gomorrah', 'nineveh', 'tyre', 'sidon',
    # Proper names starting with 'ba-' (must not be analyzed as ba + X)
    'baal', 'balaam', 'bashan', 'babylon', 'barnabus', 'barnabas',
    'bathsheba', 'barak', 'barabbas', 'baruch', 'belshazzar', 'benhadad',
    'bethlehem', 'beersheba', 'beelzebub', 'belial',
    # Additional proper names from residual analysis
    'balak', 'zippor', 'mizpah', 'azariah', 'zadok', 'nathan',
    # Round 156: More proper nouns to prevent prefix mis-segmentation
    'kenan', 'amen', 'ur', 'aram', 'hamath', 'anak', 'negeb',
    'amaziah', 'hiv', 'hivite', 'kaleb', 'uriah', 'zikri', 'jessi', 'jehoiada',
    'zif', 'abijah', 'baruk', 'kadesh', 'zedekiah', 'hezekiah',
    # Round 157: More proper nouns from partials
    'heman', 'aner', 'Puah', 'enan', 'adonijah', 'mikaiah', 'on',  # puah→Puah (divine/bet)
    'arnon', 'karmel', 'carmel', 'ahaziah', 'uzziah', 'nebat', 'athaliah',
    'antiok', 'iram', 'arabah', 'abiathar', 'nadab', 'khadet', 'kedar',
    'akhan', 'achan', 'sisera', 'jabin', 'joash', 'joab', 'omri',
    # Round 158: Proper nouns with prefix-like beginnings (a-, na-, mi-, hi-, etc.)
    'haman', 'asa', 'sihon', 'akhish', 'zeruiah', 'baasha', 'mikah',
    'hiram', 'ahasueras', 'ahasuerus', 'sisaria', 'eleazar', 'ashdod',
    'abigail', 'abishai', 'asaf', 'asaph', 'lakhish', 'lachish',
    'anathoth', 'naomi', 'naaman', 'mikhal', 'michal', 'shafan', 'shaphan',
    'nebuzaradan', 'nethaniah', 'aroer', 'ahijah', 'nabal', 'ziba', 'amasa',
    # Round 159: Short proper nouns that conflict with prefixes
    # Note: removed lowercase versions of words with common meanings:
    # - 'ai' (lot), 'en' (look), removed to allow common word analysis
    'uz', 'ar', 'on', 'or', 'ir', 'ed',
    # Round 160: More proper nouns from unknowns
    'elim', 'zeeb', 'doeg', 'harar', 'meunim', 'hagri', 'hananel', 'thebes',
    'oholah', 'derbe', 'husham', 'shimron', 'hushim', 'pihahiroth', 'zered',
    'elath', 'golan', 'gerizim', 'betharabah', 'eshtemoa', 'gaash', 'harod',
    'elimelek', 'peninnah', 'jeshanah', 'merab', 'jehozabad', 'jaazaniah',
    # Round 161: More OT/NT proper nouns to prevent prefix mis-segmentation
    'hilkiah', 'tola', 'nethanel', 'hammon', 'amon', 'ahimelek', 'zibiah',
    'tobiah', 'enok', 'asahel', 'mattaniah', 'abel', 'babel', 'sukkoth',
    'ashhur', 'pashhur', 'ahikam', 'enosh', 'khemosh', 'chemosh', 'nahor',
    'paran', 'naboth', 'kareah', 'amariah', 'ananias', 'uzziel', 'urim',
    'abarim', 'jefunneh', 'agag', 'zimri', 'nebo', 'ahimaaz', 'netofah',
    'bani', 'jehoram', 'remaliah', 'amoz', 'mikhael', 'sairas', 'saipras',
    'saddusi', 'agrippa', 'abihu', 'ashtaroth', 'ashkelon', 'ner',
    'ahithofel', 'ahithophel', 'jehu', 'esther', 'Lot', 'beor', 'amram',
    'izhar', 'ithamar', 'ahira', 'ira',
    # Round 162: Bulk proper noun addition - all remaining names
    'abaddon', 'abagtha', 'abda', 'abdeel', 'abdi', 'abdiel', 'abdon', 'abednego', 'abelbethmaakah', 'abelkeramim',
    'abelmaim', 'abelmeholah', 'abelmizraim', 'abelshittim', 'abi', 'abiah', 'abialbon', 'abiasaf', 'abib', 'abida',
    'abidan', 'abiel', 'abiezer', 'abihail', 'abihud', 'abijam', 'abilene', 'abimael', 'abinadab', 'abinoam',
    'abiram', 'abishag', 'abishua', 'abishur', 'abital', 'abiud', 'adadah', 'adah', 'adaiah', 'adalia',
    'adaminekeb', 'adar', 'adbeel', 'addan', 'addar', 'addi', 'adiel', 'adin', 'adina', 'adithaim',
    'adlai', 'admah', 'admatha', 'admin', 'adna', 'adnah', 'adonibezek', 'adonikam', 'adoniram', 'adonizedek',
    'adoram', 'adramittium', 'adrammelek', 'adriel', 'adullam', 'adummim', 'afek', 'afekah', 'afiah', 'afik',
    'agabas', 'agee', 'agur', 'aharah', 'aharhel', 'ahasbai', 'ahava', 'ahban', 'ahian', 'ahiezer',
    'ahihud', 'ahilud', 'ahiman', 'ahimoth', 'ahinadab', 'ahio', 'ahiram', 'ahisamak', 'ahishar', 'ahitub',
    'ahlab', 'ahlai', 'ahoah', 'ahoh', 'ahumai', 'ahuzzam', 'ahuzzath', 'ahzai', 'aiah', 'aiath',
    'aija', 'aijalon', 'aineas', 'ainon', 'akan', 'akbor', 'akeldama', 'akhaikas', 'akhim', 'akhor',
    'akkad', 'akko', 'akkub', 'aklui', 'akpi', 'akrabbim', 'aksah', 'akshaf', 'akzib', 'alemeth',
    'alexander', 'alexandria', 'alfa', 'alfeas', 'aliah', 'allammelek', 'allon', 'allonbakuth', 'almodad', 'almon',
    'almondiblathaim', 'alush', 'alvah', 'alvan', 'amad', 'amana', 'amasai', 'amashsai', 'amasiah',
    'amaw', 'amfipolis', 'amittai', 'ammah', 'ammiel', 'ammihud', 'amminadab', 'ammishaddai', 'ammizabad', 'amnon',
    'amok', 'ampliatas', 'amrafel', 'amzi', 'anab', 'anah', 'anaharath', 'anammelek', 'anani', 'ananiah',
    'anath', 'andronikas', 'anem', 'angkawmin', 'anim', 'anna', 'antak', 'anthak', 'anthothijah', 'antipas',
    'antipatris', 'anub', 'apelles', 'apfia', 'apis', 'apkikna', 'apollion', 'apollonia', 'appaim', 'ara',
    'arab', 'arabia', 'arad', 'arah', 'arammaakah', 'aran', 'ararat', 'araunah', 'arba', 'arbi',
    'ard', 'ardon', 'areli', 'areopagas', 'aretas', 'argob', 'aridai', 'aridatha', 'ariel', 'arimathea',
    'ariok', 'arisai', 'aristarkhas', 'aristobulas', 'arka', 'arkhelaus', 'arkhi', 'arkhippas', 'arki', 'armageddon',
    'armoni', 'arnan', 'arod', 'arodi', 'arpad', 'arpakshad', 'artakzaksis', 'artemas', 'artemis', 'arubboth',
    'arumah', 'arvad', 'arza', 'asaiah', 'asarel', 'asenath', 'ashan', 'asharelah', 'ashbel', 'asherah',
    'ashima', 'ashimah', 'ashkenaz', 'ashnah', 'ashpenaz', 'ashterath', 'ashteroth', 'ashtoreth', 'ashur', 'ashurbanipal',
    'ashvath', 'asiel', 'asinkritas', 'asnah', 'aspatha', 'asriel', 'asshur', 'asshurim', 'assir', 'assos',
    'atad', 'atarah', 'ataroth', 'atarothaddar', 'ater', 'athaiah', 'athak', 'atharim', 'athlai', 'atrothbethjoab',
    'atrothshofan', 'attai', 'attalia', 'augustas', 'avith', 'avva', 'avvim', 'awle', 'azaniah', 'azarel',
    'azaz', 'azazel', 'azaziah', 'azbuk', 'azekah', 'azel', 'azgad', 'aziel', 'aziza', 'azmaveth',
    'azmon', 'aznothtabor', 'azor', 'azotas', 'azriel', 'azrikam', 'azubah', 'azzah', 'azzan', 'azzur',
    'baaberith', 'baalath', 'baalathbeer', 'baalberith', 'baalejudah', 'baalgad', 'baalhamon', 'baalhanan', 'baalhazor', 'baalhermon',
    'baalis', 'baalmeon', 'baalpeor', 'baalperazim', 'baalshalishah', 'baaltamar', 'baalzebub', 'baalzefon', 'baana', 'baanah',
    'baara', 'baaseiah', 'bahurim', 'bakbakkar', 'bakbuk', 'bakbukiah', 'bala', 'baladan', 'bamoth',
    'bamothbaal', 'bangcia', 'barakhel', 'barakhiah', 'bariah', 'barjesuh', 'barkos', 'barsabbas', 'bartimias', 'barzillai',
    'basemath', 'bathshua', 'bavvai', 'bazlith', 'bazluth', 'bealiah', 'bealoth', 'bebai', 'bedad', 'bedan',
    'bedeiah', 'beeliada', 'beelzebul', 'beer', 'beera', 'beerah', 'beerelim', 'beeri', 'beerlahairoi', 'beeshterah',
    'bekher', 'bekorath', 'bela', 'beltashazzar', 'belteshazzar', 'benabinadab', 'benaiah', 'benammi', 'bendeker', 'beneberak',
    'benejaakan', 'bengeber', 'benhail', 'benhanan', 'benhesed', 'benhur', 'beninu', 'beno', 'benoni', 'benzoheth',
    'beon', 'bera', 'beraiah', 'berakah', 'bered', 'berekhiah', 'beri', 'beriah', 'bernis', 'berothah',
    'berothai', 'besai', 'besan', 'besodeiah', 'besor', 'betah', 'betashazzar', 'beten', 'beteshazzar', 'beth',
    'bethanath', 'bethanoth', 'betharbel', 'bethashbea', 'bethazmaveth', 'bethbaalmeon', 'bethbarah', 'bethbiri', 'bethdagon',
    'bethdiblathaim', 'betheden', 'bethemek', 'bethezel', 'bethfage', 'bethgader', 'bethgamul', 'bethgilgal', 'bethhaggan', 'bethhakkherem',
    'bethharam', 'bethharan', 'bethhoglah', 'bethjeshimoth', 'bethkar', 'bethleafrah', 'bethlebaoth', 'bethmarkaboth', 'bethmeon', 'bethmillo',
    'bethnimrah', 'bethpazzez', 'bethpelet', 'bethpeor', 'bethrafa', 'bethrehob', 'bethshan', 'bethshittah', 'bethtappuah',
    'bethtogarmah', 'bethuel', 'bethul', 'bethzatha', 'bethzur', 'betonim', 'beza', 'bezai', 'bezalel', 'bezek',
    'bezer', 'bidkar', 'bigah', 'bigai', 'bigtha', 'bigthana', 'bigvai', 'bihah', 'bikhri', 'bildad',
    'bileam', 'bilgah', 'bilhah', 'bilhan', 'bilshan', 'bimhal', 'binea', 'binnui', 'birsha', 'birzaith',
    'bithiah', 'bithynia', 'biziothiah', 'biztha', 'blastus', 'boanerges', 'bohan', 'bokheru', 'bokhim', 'borashan',
    'bozez', 'bozkath', 'bukki', 'bukkiah', 'bunah', 'bunni', 'buz', 'buzi',
    'chin', 'ciktuite',
    'daberath', 'dalmanutha', 'dalmatia', 'damaris', 'dan-jaan', 'dannah', 'dara', 'darda', 'datik', 'dedan',
    'deker', 'delaiah', 'demas', 'demetrias', 'derbe', 'deuel', 'diblah', 'diblaim', 'dibon', 'dibongad',
    'dibri', 'diklah', 'dimnah', 'dimon', 'dimonah', 'dinah', 'dinhabbah', 'diotrephes', 'dishan', 'dishon',
    'dizahab', 'dodai', 'dodavahu', 'dodo', 'dophkah', 'dor', 'drusilla', 'dumah',
    'ebal', 'ebed', 'ebedmelek', 'ebenezer', 'eber', 'ebiasaph', 'eden', 'eder', 'edrei', 'efer',
    'efod', 'efraim', 'efron', 'ehi', 'ehud', 'ekron', 'ela', 'elah', 'elamite', 'elasa',
    'elasah', 'elath', 'eldaah', 'eldad', 'elead', 'elealeh', 'eleasa', 'eleasah', 'eleazer', 'elhanan',
    'eli', 'eliab', 'eliada', 'eliakim', 'eliam', 'elias', 'eliasaph', 'eliashib', 'eliathah', 'elidad',
    'eliel', 'elienai', 'eliezer', 'elihoreph', 'elihud', 'elika', 'elim', 'elimelek', 'elioenai', 'eliphaz',
    'eliphelet', 'elipheleth', 'elisha', 'elishama', 'elisheba', 'elishua', 'eliud', 'elizafan', 'elizur', 'elkana',
    'elkanah', 'elkosh', 'ellasar', 'elmadam', 'elnaam', 'elnatan', 'eloi', 'elon', 'elonbethhanan', 'elpaaran',
    'elpaal', 'elpelet', 'elteke', 'eltekeh', 'eltekon', 'eltolad', 'eluzai', 'elymas', 'elzabad', 'elzaphan',
    'emaas', 'emim', 'enam', 'endor', 'engedi', 'engannim', 'enhaddah', 'enhakkore', 'enmishpat', 'enrimmon',
    'enrogel', 'enshemesh', 'entappuah', 'epafras', 'epafroditas', 'epaenetas', 'erastus', 'erech', 'eri', 'esarhaddon',
    'eshban', 'eshek', 'eshkol', 'eshtaol', 'eshtemoa', 'eshtemoh', 'eshton', 'esli', 'esrom', 'etam',
    'ethan', 'ethbaal', 'ether', 'etni', 'eunika', 'eutykas', 'evi', 'ezbai', 'ezbon', 'ezekias',
    'ezem', 'ezer', 'ezion-geber', 'ezra', 'ezri',
    'felix', 'festas', 'filistia-pa', 'foenisia', 'fortunatas', 'frihia',
    'gaal', 'gaash', 'gabbai', 'gabbatha', 'gad-ite', 'gaddi', 'gaddiel', 'gader', 'gaham', 'gahar',
    'gaius', 'galal', 'galatia', 'galeed', 'gallion', 'gamul', 'garmite', 'gatam', 'gathhefer', 'gathrimmon',
    'gaza', 'gazam', 'gazer', 'gazez', 'gazzam', 'geba', 'geber', 'gedaliah', 'geder', 'gederah',
    'gederoth', 'gederothaim', 'gedor', 'gehazi', 'geliloth', 'gemalli', 'gemariah', 'gennesaret', 'genubath', 'gera',
    'gerar', 'gerizim', 'gershom', 'gershon', 'geshan', 'geshem', 'geshur', 'geshuri', 'gether', 'gethsemane',
    'geuel', 'gezer', 'gibbar', 'gibbethon', 'gibea', 'gibeah', 'gibeon', 'giddalti', 'giddel',
    # Note: 'giah' removed - common Tedim word meaning 'camp'
    'gideoni', 'gidom', 'gihon', 'gilalai', 'gilboa', 'gilgal', 'giloh', 'gimzo', 'ginath', 'ginnethon',
    'girgashite', 'gispa', 'gittaim', 'gittite', 'gizonite', 'goah', 'gob', 'goiim', 'golan', 'goliath',
    'gomer', 'gomorrah', 'gophna', 'goshen', 'gozan', 'guni', 'gunite', 'gur', 'gurbaal',
    'haahashtari', 'habaiah', 'habakkuk', 'habazziniah', 'habergeon', 'habor', 'hachaliah', 'hachilah', 'hachmoni', 'hadadezer',
    'hadashah', 'hadattah', 'haddah', 'hadid', 'hadlai', 'hadoram', 'hadrakh', 'hagab', 'hagabah', 'hagar',
    'haggai', 'haggai-te', 'haggedolim', 'haggiah', 'haggith', 'hagri', 'haifa', 'hakkatan', 'hakkoz', 'hakufa',
    'halah', 'halak', 'halhul', 'hali', 'hallohesh', 'Ham', 'haman', 'hamath', 'hamathite', 'hamathzobah',  # ham→Ham (also/full/cover)
    'hammedatha', 'hammiphkad', 'hammon', 'hammuel', 'hamonah', 'hamongog', 'hamor', 'hamuel', 'hamul', 'hamutal',
    'hanamel', 'hanan', 'hananeel', 'hanani', 'hananiah', 'hanes', 'haniel', 'hannah', 'hannathon', 'hanniel',
    'hanun', 'haphraim', 'happizzez', 'hara', 'haradah', 'haralah', 'haran', 'harar', 'hararhiah', 'harbona',
    'hareph', 'hareth', 'harhaiah', 'harhas', 'harhur', 'harim', 'harnefer', 'harod', 'haroeh', 'harosheth-ha-goiim',
    'harsha', 'harum', 'harumaph', 'haruz', 'hasadiah', 'hashabiah', 'hashabneiah', 'hashbaddanah', 'hashem', 'hashmonah',
    'hashubah', 'hashum', 'hasrah', 'hassenah', 'hasshub', 'hassophereth', 'hasupha', 'hatach', 'hathath', 'hatipha',
    'hatita', 'hattil', 'hattush', 'hauran', 'havilah', 'havvothjair', 'hazael', 'hazaiah', 'hazarenan', 'hazargaddah',
    'hazarshual', 'hazarsusah', 'hazarsusim', 'hazelelponi', 'hazerim', 'hazeroth', 'hazezon-tamar', 'haziel', 'hazo', 'hazor',
    'hazzelelponite', 'heber', 'hebron', 'hegai', 'helah', 'helbah', 'helbon', 'heldai', 'heleb', 'heled',
    'helek', 'helem', 'heleph', 'helez', 'heli', 'helkai', 'helkath', 'helkathhazzurim', 'helon', 'hemam',
    'heman', 'hemdan', 'hena', 'henadad', 'henok', 'hepher', 'hephzibah', 'heresh', 'hermas', 'hermes',
    'hermogenes', 'heshbon', 'heshmon', 'heth', 'hethlon', 'hezekiah', 'hezion', 'hezir', 'hezrai', 'hezro',
    'hezron', 'hiddai', 'hiddekel', 'hiel', 'hierapolis', 'higgaion', 'hikiah', 'hilkiah', 'hillel', 'hinnom',
    'hirah', 'hiram', 'hittite', 'hivite', 'hizkiah', 'hizkijah', 'hobab', 'hobah', 'hod', 'hodaiah',
    'hodaviah', 'hodesh', 'hodevah', 'hodiah', 'hodijah', 'hoglah', 'hoham', 'holon', 'homam', 'hophni',
    'hophra', 'hor', 'horam', 'horeb', 'horem', 'horesh', 'horhagidgad', 'hori', 'horite', 'hormah',
    'horonaim', 'horonite', 'hosah', 'hosea', 'hoshaiah', 'hoshama', 'hoshea', 'hotham', 'hothan', 'hothir',
    'hukkok', 'hukok', 'hul', 'huldah', 'humtah', 'hupham', 'huppim', 'hur', 'hurai', 'huram',
    'huri', 'hushai', 'husham', 'hushathite', 'hushim', 'huz', 'huzzab', 'hymeneus',
    'ibhar', 'ibleam', 'ibneiah', 'ibnijah', 'ibri', 'ibsam', 'ibzan', 'ichabod', 'idala', 'idbash',
    'iddo', 'idumeate', 'ijon', 'ikkesh', 'ilai', 'illyricum', 'imlah', 'imla', 'immanuel', 'immer',
    'imna', 'imnah', 'imrah', 'imri', 'innsungah', 'iob', 'iphedeiah', 'ir', 'ira', 'irad',
    'iram', 'iri', 'irijah', 'irnahash', 'irpeel', 'irshemesh', 'isaac', 'isaiah', 'iscah', 'iscariot',
    'ishbah', 'ishbak', 'ishbibenob', 'ishbosheth', 'ishi', 'ishiah', 'ishijah', 'ishma', 'ishmael', 'ishmaiah',
    'ishmerai', 'ishod', 'ishpan', 'ishsechel', 'ishuah', 'ishuai', 'ishui', 'ishvah', 'ishvi', 'iskariot',
    'ismakiah', 'israel-te', 'isshiah', 'isshijah', 'isuah', 'italian', 'italy', 'ithai', 'ithamar', 'ithiel',
    'ithmah', 'ithnan', 'ithra', 'ithran', 'ithream', 'ithri', 'ithrite', 'ittai', 'ittahkazin', 'ituraea',
    'ivvah', 'iye-abarim', 'iyin', 'izhar', 'izliah', 'izrahiah', 'izrahite', 'izri', 'izziah',
    'jaakan', 'jaakobah', 'jaala', 'jaalah', 'jaareshiah', 'jaasau', 'jaasiel', 'jaazaniah', 'jaaziah', 'jaaziel',
    'jabal', 'jabbok', 'jabesh', 'jabez', 'jabin', 'jabneel', 'jabneh', 'jachan', 'jadau', 'jaddua',
    'jadon', 'jael', 'jafia', 'jagur', 'jah', 'jahath', 'jahaz', 'jahazah', 'jahaziah', 'jahaziel',
    'jahdai', 'jahdiel', 'jahdo', 'jahleel', 'jahmai', 'jahzah', 'jahzeel', 'jahzera', 'jahzerah', 'jahziel',
    'jair', 'jairite', 'jairus', 'jakan', 'jakeh', 'jakim', 'jalam', 'jalon', 'jambres', 'jamin',
    'jamlech', 'janai', 'janes', 'janim', 'janna', 'jannai', 'janoah', 'janum', 'japheth', 'japhia',
    'japhlet', 'japho', 'jarah', 'jared', 'jaresiah', 'jarha', 'jarib', 'jarmuth', 'jaroah', 'jashen',
    'jasher', 'jashobeam', 'jashub', 'jashubi-lehem', 'jasiel', 'jason', 'jathniel', 'jattir', 'javan', 'jazer',
    'jaziz', 'jearim', 'jeaterai', 'jeberechiah', 'jebus', 'jebusite', 'jecamiah', 'jecoliah', 'jeconiah', 'jedaiah',
    'jediael', 'jedidah', 'jedidiah', 'jeduthun', 'jeezer', 'jegar-sahadutha', 'jehalelel', 'jehallelel', 'jehdeiah', 'jehezekel',
    'jehiah', 'jehiel', 'jehieli', 'jehizkiah', 'jehoaddah', 'jehoaddan', 'jehoahaz', 'jehoash', 'jehohanan', 'jehoiachin',
    'jehoiakim', 'jehoiarib', 'jehonadab', 'jehonathan', 'jehoram', 'jehoshaphat', 'jehosheba', 'jehoshua', 'jehovah', 'jehovah-jireh',
    'jehovah-nissi', 'jehovah-shalom', 'jehozabad', 'jehozadak', 'jehu', 'jehubbah', 'jehucal', 'jehud', 'jehudi', 'jehush',
    'jeiel', 'jekabzeel', 'jekameam', 'jekamiah', 'jekuthiel', 'jemimah', 'jemuel', 'jephthae', 'jefthah', 'jefunneh',
    'jerah', 'jerahmeel', 'jered', 'jeremai', 'jeremiah', 'jeremoth', 'jeriah', 'jeribai', 'jericho', 'jeriel',
    'jerijah', 'jerimoth', 'jerioth', 'jeruel', 'jerubbaal', 'jerubbesheth', 'jerusha', 'jerushah', 'jesaiah', 'jeshaiah',
    'jeshanah', 'jesharelah', 'jeshebeab', 'jesher', 'jeshimon', 'jeshishai', 'jeshohaiah', 'jeshua', 'jeshurun', 'jesimiel',
    'jesse', 'jether', 'jetheth', 'jethro', 'jetur', 'jeuel', 'jeush', 'jeuz', 'jezaniah', 'jezebel',
    'jezer', 'jeziel', 'jezliah', 'jezoar', 'jezrahiah', 'jezreel', 'jibsam', 'jidlaph', 'jimna', 'jimnah',
    'jiphtah', 'jiphtahel', 'joab', 'joah', 'joahaz', 'joakim', 'joanna', 'joash', 'jobab', 'jochebed',
    'joda', 'joed', 'joel', 'joelah', 'joezer', 'jogbehah', 'jogli', 'joha', 'johanan', 'joiakim',
    'joiarib', 'jokdeam', 'jokim', 'jokmeam', 'jokneam', 'jokshan', 'joktan', 'joktheel', 'jonadab', 'jonam',
    'jonan', 'jorah', 'jorai', 'joram', 'jored', 'jorim', 'jorkoam', 'josech', 'josedech', 'joshaphat',
    'joshaviah', 'joshbekashah', 'josheb-basshebeth', 'joshibiah', 'josiphiah', 'josses', 'jotham', 'jothath', 'jothathah', 'jozabad',
    'jozachar', 'jozadak', 'jubal', 'jucal', 'judith', 'julia', 'junias', 'jushab-hesed', 'justus', 'juttah',
    'kabzeel', 'kadesh', 'kadmiel', 'kadmonite', 'kain', 'kaiafas', 'kainan', 'kallai', 'kamon', 'kanah',
    'kareah', 'karkaa', 'karmi', 'karnaim', 'karshena', 'kartah', 'kartan', 'kattath', 'kedar', 'kedemah',
    'kedemoth', 'kedesh', 'kedorlaomer', 'kehelathah', 'keilah', 'kelaiah', 'kelal', 'kelita', 'kelub', 'keluhi',
    'kemuel', 'kenan', 'kenath', 'kenaz', 'kenezite', 'kenite', 'kenizzite', 'kephirah', 'keran', 'kerenhappuch',
    'kerioth', 'keros', 'keruv', 'kesalon', 'kesed', 'kesil', 'kesulloth', 'keturah', 'kezia', 'keziz',
    'khaldea', 'khenaanah', 'kheran', 'khesalon', 'khesed', 'khesil', 'khesulloth', 'kheturah', 'kheziab', 'khinnereth',
    'khinneroth', 'khios', 'khislev', 'khislon', 'khisloth-tabor', 'khittaim', 'khloe', 'khobar', 'khobi', 'kholon',
    'khozeba', 'khristiante', 'khristianpihte', 'khub', 'khun', 'kibrothhattaavah', 'kibzaim', 'kidron', 'kinah', 'kir',
    'kirhareseth', 'kiriathaim', 'kiriath-arba', 'kiriathhaim', 'kiriathjearim', 'kiriathsannah', 'kiriathsepher', 'kish', 'kishi', 'kishion',
    'kishon', 'kithlish', 'kitron', 'kittim', 'koa', 'kohathite', 'kolaiah', 'kona', 'konaiah', 'korahite',
    'kore', 'korhite', 'koz', 'krete', 'kue', 'kushaiah',
    'laadah', 'laadan', 'laban', 'lael', 'lahad', 'lahai-roi', 'lahmam', 'lahmi', 'laish', 'laishah',
    'lakkum', 'lamek', 'laodikeia', 'lapidoth', 'lasea', 'lasha', 'lasharon', 'lazarus', 'leah', 'lebana',
    'lebanah', 'lebaoth', 'lebbaeus', 'lebonah', 'lekah', 'lechem', 'lehabim', 'lehi', 'lemuel', 'leshem',
    'letushim', 'leummim', 'levi', 'levite', 'libnah', 'libni', 'libyate', 'likhi', 'linus', 'lo-ammi',
    'lo-debar', 'lo-ruhamah', 'lod', 'lois', 'lotan', 'lubim', 'lucius', 'lud', 'ludim', 'luhith',
    'luz', 'lydia', 'lysanias', 'lysias', 'lystra',
    'maadai', 'maadiah', 'maai', 'maakah', 'maakathite', 'maarath', 'maaseiah', 'maasiai', 'maath', 'maaz',
    'maaziah', 'macedonia-te', 'machbenah', 'machi', 'machir', 'machnadebai', 'machpelah', 'madai', 'madian', 'madmannah',
    'madmen', 'madmenah', 'madon', 'magbish', 'magdala', 'magdiel', 'magog', 'magor-missabib', 'magpiash', 'mahalah',
    'mahalal', 'mahalalel', 'mahalath', 'mahanaim', 'mahaneh-dan', 'maharai', 'mahath', 'mahavite', 'mahazioth', 'maher-shalal-hash-baz',
    'mahlah', 'mahli', 'mahlon', 'mahol', 'mahseiah', 'maki', 'makheloth', 'makhir', 'makkedah', 'maktesh',
    'malachi', 'malkam', 'malki-shua', 'malkiel', 'malkijah', 'malkiram', 'malkishua', 'mallothi', 'malluch', 'malluk',
    'malta', 'maluhi', 'mamre', 'manaen', 'manahath', 'manahathite', 'manasseh-te', 'maoch', 'maon', 'mara',
    'marah', 'maralah', 'marcus', 'mareshah', 'mark', 'maroth', 'marsena', 'mash', 'mashal', 'masrekah',
    'massa', 'massah', 'matred', 'matri', 'mattai', 'mattan', 'mattanah', 'mattaniah', 'mattatha', 'mattathah',
    'mattathias', 'mattenai', 'matthai', 'matthat', 'matthew', 'matthias', 'mattithiah', 'mazzaroth', 'meah', 'mearah',
    'mebunnai', 'mecherathite', 'medad', 'medan', 'medeba', 'media', 'megiddo', 'mehetabel', 'mehida', 'mehir',
    'meholathite', 'mehujael', 'mehuman', 'mejarkon', 'mekonah', 'melatiah', 'melchi', 'melchisedek', 'melchizedek', 'melea',
    'melek', 'melita', 'melzar', 'memphis', 'memucan', 'menahem', 'menan', 'mene', 'menna', 'meonothai',
    'mefaath', 'mefibosheth', 'merab', 'meraiah', 'meraioth', 'merari', 'merathaim', 'mered', 'meremoth', 'meres',
    'meribah', 'meribbaal', 'merodach', 'merodachbaladan', 'merom', 'meronothite', 'meroz', 'mesech', 'mesha', 'meshak',
    'meshech', 'meshelemiah', 'meshezabel', 'meshillemith', 'meshillemoth', 'meshullam', 'meshullemeth', 'mesobaite', 'mesopotamia', 'messiah',
    'methegammah', 'methusael', 'methuselah', 'meunim', 'mezahab', 'miamin', 'mibhar', 'mibsam', 'mibzar', 'mica',
    'micaiah', 'mika', 'mikael', 'mikhael', 'mikhaiau', 'mikhaiah', 'mikmash', 'mikneiah', 'mikri', 'miktam',
    'mikthah', 'milalai', 'milcah', 'miletus', 'milkah', 'milkom', 'millo', 'miniamin', 'minni', 'minnith',
    'miriam', 'mirma', 'mishael', 'misham', 'misheal', 'mishma', 'mishmannah', 'mishraite', 'mispar', 'misrephoth-maim',
    'mithkah', 'mithnite', 'mithredath', 'mityene', 'mizar', 'mizpah', 'mizpar', 'mizpeh', 'mizraim', 'mizzah',
    'mnason', 'moab-te', 'moadiah', 'moladah', 'molid', 'moloch', 'morasthite', 'mordekai', 'moreh', 'moresheth',
    'moreshethgath', 'moriah', 'moserah', 'moseroth', 'moza', 'mozah', 'muppim', 'mushi', 'myra', 'mysia',
    'naam', 'naamah', 'naaman', 'naarah', 'naarai', 'naaran', 'naarath', 'naashon', 'naasson', 'nabal',
    'naboth', 'nachon', 'nacon', 'nadab', 'nafat', 'nafathdor', 'nafishite', 'naftali-te', 'nagge', 'nahalal',
    'nahaliel', 'nahalol', 'naham', 'nahamani', 'naharai', 'nahash', 'nahath', 'nahbi', 'nahor', 'nahshon',
    'nahum', 'naioth', 'naomi', 'naphish', 'naphtali', 'naphtuhim', 'narcissus', 'nasi', 'nathan-melek', 'nathanael',
    'nathanmelek', 'naum', 'nazarene', 'nazarite', 'nazir', 'neah', 'neapolis', 'neariah', 'nebai', 'nebaioth',
    'neballat', 'nebat', 'nebo', 'nebushasban', 'nebuzaradan', 'necho', 'nedabiah', 'neginah', 'neginoth', 'nehelamite',
    'nehemiah', 'nehiloth', 'nehum', 'nehushta', 'nehushtan', 'neiel', 'neiel', 'nekeb', 'neko', 'nekoda',
    'nemuel', 'nemuelite', 'nepheg', 'nephilim', 'nephish', 'nephisim', 'nephtoah', 'nephusim', 'ner', 'nereus',
    'nergal', 'nergal-sharezer', 'neri', 'neriah', 'netaim', 'netaneel', 'netanel', 'netaniah', 'nethaneel', 'nethaniah',
    'nethanel', 'nethinim', 'netofah', 'netofathite', 'neziah', 'nezib', 'nibhaz', 'nibshan', 'nikanor', 'nikodemas',
    'nikolaitante', 'nikolas', 'nile', 'nimrah', 'nimrim', 'nimrod', 'nimshi', 'nineva', 'nisan', 'nisroch',
    'No', 'noadiah', 'noah', 'nob', 'nobah', 'nobai', 'nod', 'nodab', 'noe', 'nofah',  # no→No (young/obey)
    'nogah', 'noha', 'non', 'nophah', 'Nun', 'nymphas',
    'obadiah', 'obal', 'obed', 'obededom', 'obil', 'oboth', 'ochran', 'oded', 'og', 'ohad',
    'ohel', 'oholah', 'oholiab', 'oholibah', 'oholibamah', 'okran', 'olive', 'olympas', 'omar', 'omega',
    'omri', 'on', 'onam', 'onan', 'onesiforas', 'onesimus', 'ono', 'ophel', 'ophir', 'ophni',
    'ophrah', 'oreb', 'oren', 'orion', 'ornan', 'orpah', 'ortygometra', 'osaias', 'oseas', 'osee',
    'osnappar', 'othni', 'othniel', 'ozem', 'ozias', 'ozni',
    'paarai', 'padanaram', 'paddanaram', 'padon', 'pagiel', 'pahathmoab', 'palal', 'palestine', 'pallu',
    # Note: 'pai' removed - conflicts with verb 'pai' (go, 2998x). Place name only 1x in 1Ch 1:50.
    'palti', 'paltiel', 'paltite', 'pamfilia', 'pannag', 'paphos', 'parah', 'paran', 'parbar', 'parmashta',
    'parmenas', 'parnach', 'parosh', 'parshandatha', 'partahia', 'parthian', 'paruah', 'parvaim', 'pasach', 'pasdammim',
    'paseah', 'pashhur', 'pathros', 'pathrusim', 'patmos', 'patrobas', 'Pau', 'pedael', 'pedahel', 'pedahzur',  # pau→Pau (speak)
    'pedaiah', 'pekah', 'pekahiah', 'pekod', 'pelaiah', 'pelaliah', 'pelatiah', 'peleg', 'pelet', 'peleth',
    'pelethite', 'pelonite', 'peniel', 'peninnah', 'pentekost', 'penuel', 'peor', 'perazim', 'peresh', 'perez',
    'perezzah', 'perga', 'pergamos', 'perida', 'perizzite', 'persis', 'peruda', 'petahiah', 'pethahiah', 'pethor',
    'pethuel', 'peulthai', 'phanuel', 'pharathoni', 'pharaoh', 'pharez', 'pharisee-te', 'pharosh', 'pharpar', 'phaselis',
    'phebe', 'phenice', 'phichol', 'philadelpheia', 'philemon', 'philetas', 'philippe', 'philippi', 'philippian', 'philip',
    'phinehas', 'phlegon', 'phoenicia', 'phrygia', 'phurah', 'Phut', 'phuvah', 'phygellas', 'pi-beseth', 'pibeset',  # phut→Phut (spray)
    'pihahiroth', 'pilate', 'pildash', 'pileha', 'piltai', 'pinon', 'piraham', 'pirathon', 'pirathonite', 'pisgah',
    'pisidia', 'pison', 'pispah', 'pithom', 'pithon', 'pochereth-hazzebaim', 'pontius', 'pontus', 'poratha', 'potifar',
    'potifera', 'potiphar', 'priscilla', 'priska', 'prochorus', 'ptolomais', 'Puah', 'publius', 'pudens', 'puhite',  # puah→Puah (divine/bet)
    'pul', 'punite', 'punon', 'pur', 'purim', 'put', 'puteoli', 'putiel', 'puvah',
    'quartus',
    'raamah', 'raamses', 'rabbah', 'rabbath', 'rabbi', 'rabbith', 'rabboni', 'rabmag', 'rabsaris', 'rabshakeh',
    'racal', 'rachab', 'rachel', 'raddai', 'ragau', 'raguel', 'rahab', 'raham', 'rakem', 'rakkath',
    'rakkon', 'ramah', 'ramath', 'ramathaim', 'ramathaim-zophim', 'ramathite', 'ramathlehi', 'ramathmizpeh', 'ramath-negeb', 'ramiah',
    'ramoth', 'ramothgilead', 'rapha', 'raphah', 'raphu', 'reaiah', 'reba', 'rebekah', 'recab', 'recah',
    'rechab', 'rechah', 'reelaiah', 'regem', 'regemmelek', 'rehabiah', 'rehob', 'rehoboam', 'rehoboth', 'rehum',
    'rei', 'rekem', 'remaliah', 'remeth', 'remmon', 'remmonmethoar', 'rephael', 'rephah', 'rephaiah', 'rephaim',
    'rephidim', 'resen', 'reshef', 'resheph', 'reu', 'reuben-te', 'reuel', 'reumah', 'rezeph', 'rezia',
    'rezin', 'rezon', 'rhegium', 'rhesa', 'rhoda', 'rhodes', 'ribai', 'riblah', 'rimmon', 'rimmono',
    'rinnah', 'riphath', 'rissah', 'rithmah', 'rizpah', 'rodanim', 'rogel', 'rogelim', 'rohgah', 'romamti-ezer',
    'rompha', 'rosh', 'rufus', 'ruhamah', 'rumah', 'ruth',
    'sabachthani', 'sabaoth', 'sabtah', 'sabta', 'sabteca', 'sabteka', 'sacar', 'sadok', 'sairin', 'sakkuth',
    'salah', 'salamis', 'salathiel', 'salecah', 'salekah', 'salem', 'salim', 'sallai', 'sallu', 'salma',
    'salmon', 'salmone', 'salome', 'salu', 'samaria-te', 'samlah', 'sammus', 'samos', 'samothrace', 'samson',
    'sanballat', 'sansannah', 'saph', 'saphir', 'sapphira', 'sarah', 'sarai', 'saraph', 'sardine', 'sardis',
    'sarepta', 'sargon', 'sarid', 'saron', 'sarsechim', 'saruhen', 'sasai', 'satan', 'saul-te', 'sceva',
    'seah', 'seba', 'sebam', 'secachah', 'sechu', 'secundus', 'segub', 'seir', 'seirah', 'sela',
    'selah', 'selahammahlekoth', 'seled', 'seleucia', 'Sem', 'semachiah', 'semei', 'senaah', 'seneh', 'senir',  # sem→Sem (serve)
    'sennacherib', 'senuah', 'seorim', 'sephar', 'sepharad', 'sepharvaim', 'sepharvite', 'serah', 'seraiah', 'sered',
    'sergius-paulas', 'serug', 'seth', 'sethar', 'shaalabbin', 'shaalbbim', 'shaalbim', 'shaalbonite', 'shaaph', 'shaaraim',
    'shaashgaz', 'shabbethai', 'shachia', 'shaddai', 'shadrach', 'shage', 'shaharaim', 'shahazimah', 'shahazumah', 'shalem',
    'shalim', 'shalisha', 'shallecheth', 'shallum', 'shallun', 'shalmai', 'shalman', 'shalmaneser', 'shama', 'shamariah',
    'shamed', 'shamer', 'shamgar', 'shamhuth', 'shamir', 'shamma', 'shammah', 'shammai', 'shammoth', 'shammua',
    'shammuah', 'shamsherai', 'shafan', 'shafat', 'sharai', 'sharar', 'sharezer', 'sharon', 'sharonite', 'sharuhen',
    'shashai', 'shashak', 'shaul', 'shaulite', 'shaveh', 'shaveh-kiriathaim', 'shavsha', 'sheal', 'shealtiel', 'sheariah',
    'shear-jashub', 'sheba', 'shebah', 'shebam', 'shebaniah', 'shebarim', 'sheber', 'shebna', 'shebnah', 'shebuel',
    'shecaniah', 'shechaniah', 'shechem', 'shedeur', 'shehariah', 'shekel', 'shekhem', 'shelah', 'shelanite', 'shelef',
    'shelemiah', 'sheleph', 'shelesh', 'shelomi', 'shelomith', 'shelomoth', 'shelumiel', 'shem', 'shema', 'shemaah',
    'shemaiah', 'shemariah', 'shemeber', 'shemed', 'shemer', 'shemesh', 'shemida', 'shemidah', 'sheminith', 'shemiramoth',
    'shemuel', 'shenazar', 'shenazzar', 'shenir', 'shepham', 'shephathiah', 'shephatiah', 'shephi', 'shepho', 'shephuphan',
    'sherah', 'sherebiah', 'sheresh', 'sherezer', 'sheshach', 'sheshai', 'sheshan', 'sheshbazzar', 'sheth', 'shethar',
    'shethar-bozenai', 'shetharbozenai', 'sheva', 'shibboleth', 'shibmah', 'shicron', 'shiggaion', 'shiggionoth', 'shihon', 'shihor',
    'shihor-libnath', 'shikkeron', 'shilhi', 'shilhim', 'shillem', 'shiloah', 'shiloh', 'shiloni', 'shilonite', 'shilshah',
    'shimea', 'shimeah', 'shimeam', 'shimeath', 'shimei', 'shimeon', 'shimhi', 'shimi', 'shimite', 'shimma',
    'shimon', 'shimrath', 'shimri', 'shimrith', 'shimrom', 'shimron', 'shimronite', 'shimronmeron', 'shimshai', 'shinab',
    'shinar', 'shiphi', 'shiphmite', 'shiphrah', 'shiphtan', 'shisha', 'shishak', 'shitrai', 'shittim', 'shiza',
    'shoa', 'shobab', 'shobach', 'shobai', 'shobal', 'shobek', 'shobi', 'shocho', 'shochoh', 'shoham',
    'shomer', 'shophach', 'shophan', 'shoshannim', 'shua', 'shuah', 'shual', 'shubael', 'shuham', 'shulamite',
    'shulammite', 'shumathite', 'shunammite', 'shunem', 'shuni', 'shunite', 'shupham', 'shuphamite', 'shuppim', 'shur',
    'shushan', 'shushaneduth', 'shuthelah', 'shuthelahite', 'sia', 'siaha', 'sibbecai', 'sibbekai', 'sibboleth', 'sibmah',
    'sibraim', 'sichem', 'siddim', 'sidon', 'sidonian', 'sihon', 'sihor', 'silas', 'silisia', 'silla',
    'siloah', 'siloam', 'silvanus', 'simeon-te', 'simon', 'simri', 'sina', 'sinai', 'sinim',
    # Note: 'sin' removed - common Tedim word meaning 'near'
    'sinite', 'sion', 'siphmoth', 'sippai', 'sirah', 'sirion', 'sisamai', 'sisar', 'sisera', 'sismai',
    'sithri', 'sitnah', 'sivan', 'smyrna', 'so', 'soco', 'socoh', 'sodi', 'sokoh', 'solomon-te',
    'sopater', 'sopatros', 'sophereth', 'sorek', 'sosipater', 'sosthenes', 'sotai', 'spain', 'stachys', 'stephanas',
    'stephenias', 'stoik', 'Suah', 'succoth', 'succothbenoth', 'sukkoth', 'suph', 'suphah', 'sur', 'susah',  # suah→Suah (birth)
    'susi', 'suthelah', 'sychar', 'syene', 'syntyche', 'syracuse', 'syria-te', 'syrophoenician', 'syrtis',
    'taanach', 'taanath-shiloh', 'tabbaoth', 'tabbath', 'tabeal', 'tabeel', 'taberah', 'tabitha', 'tabor', 'tabrimon',
    'tadmor', 'tahan', 'tahanite', 'tahash', 'tahath', 'tahpanhes', 'tahpenes', 'tahrea', 'tahtim-hodshi', 'talitha',
    'talmai', 'talmon', 'tamah', 'tamar', 'tammuz', 'tanach', 'tanhum', 'tanhumeth', 'tappuah', 'tarah',
    'taralah', 'tarea', 'tarshish', 'tarsos', 'tartak', 'tartan', 'tatami', 'tatnai', 'tattenai', 'tebah',
    'tebaliah', 'tebeth', 'tehaphnehes', 'tehinnah', 'tekel', 'tekoa', 'tekoah', 'tekoite', 'telabib', 'telah',
    'telaim', 'telassar', 'telem', 'telharsha', 'telharsa', 'telmelah', 'tema', 'teman', 'temani', 'temanite',
    'temeni', 'terah', 'teraphim', 'teresh', 'tertius', 'tertullus', 'thaddaeus', 'thahash', 'thamah', 'thamar',
    'thara', 'tharshish', 'thebes', 'thebez', 'thelasar', 'theofilus', 'thessalonians-te', 'thessalonikia', 'theudas', 'thomas',
    'thummim', 'thyatira', 'tiberias', 'tiberius', 'tibhath', 'tibni', 'tidal', 'tiglathpileser', 'tikvah', 'tikvath',
    'tilgath-pilneser', 'tilon', 'timaeus', 'timna', 'timnah', 'timnath', 'timnatheres', 'timnath-heres', 'timnathserah', 'timnite',
    'timon', 'timotheus', 'timothy', 'tiphsah', 'tiras', 'tirathite', 'tirhakah', 'tirhanah', 'tiria', 'tirshatha',
    'tirzah', 'tishbite', 'titus', 'toah', 'tob', 'tobadonijah', 'tobiah', 'tobijah', 'tochen', 'tofeth',
    'togarmah', 'tohu', 'toi', 'tokhath', 'tola', 'tolad', 'tolaite', 'tophel', 'tophet', 'topheth',
    'tou', 'trachonitis', 'troas', 'trogyllium', 'trofimas', 'trophimus', 'tubal', 'tubal-cain', 'tychicus',
    'tyrannus', 'tyre-te', 'tyros', 'tyrus',
    'ucal', 'uel', 'ulai', 'ulam', 'ulla', 'ummah', 'unni', 'unno', 'uphaz', 'uppaz',
    'ur', 'urbane', 'urbanus', 'uri', 'uriah', 'urias', 'uriel', 'urijah', 'urim', 'uthai',
    'uz', 'uzai', 'uzal', 'uzza', 'uzzah', 'uzzen-sheerah', 'uzzi', 'uzzia', 'uzziah', 'uzziel',
    'uzzielite',
    'vajezatha', 'vaniah', 'vashni', 'vashti', 'vofsi',
    'yahweh',
    # Round 163: Additional proper nouns found with partial glosses
    'dabbesheth', 'dalfon', 'danel', 'darias', 'darkon', 'dilean', 'dinhabah', 'dionisias',
    'diotrefes', 'dodanim', 'dofkah', 'dorkas', 'dothan', 'dura',
    'ebez', 'ebiasaf', 'ebron', 'ebronah', 'efai', 'efesdammim', 'eflal', 'eglah', 'eglaim',
    'eglathshelishiah', 'eglon', 'ekbatana', 'eker', 'elam', 'elberith', 'elbethel', 'eliahba',
    'eliasaf', 'eliehoenai', 'elifal', 'elifaz', 'elifelehu', 'elihoref', 'elishafat', 'elishah',
    'elna', 'elnathan', 'eloth', 'elparan', 'elul', 'elzafan', 'emekkeziz', 'emmanuel', 'emmaus',
    'enaim', 'eneglaim', 'enhazor', 'enos', 'epainetas', 'epikuras', 'eran', 'erastas', 'erek',
    'esek', 'eshan', 'eshbaal', 'ethanim', 'ethkazin', 'ethnan', 'ethni', 'eubulas', 'eunis',
    'euodia', 'eutikhas', 'evilmerodak', 'eziongebar', 'ezrah',
    'fanuel', 'farpar', 'figelas', 'fikol', 'filadelfia', 'filemon', 'filetas', 'filip',
    'filologas', 'finehas', 'flegon', 'foebe', 'foenik', 'frigia',
    'gabriel', 'gadara', 'gadi', 'galati', 'gallim', 'gallio', 'gamad', 'gamaliel', 'gareb',
    'garm', 'gebal', 'gebim', 'geharashim', 'ginnethoi', 'girzi', 'gishpa', 'gizon',
    # Note: 'gilo' removed - lowercase is common word 'enemy', uppercase Gilo/Giloh handled by suffix
    'golgotha', 'gudgodah',
    'hadadrimmon', 'hadar', 'hadassah', 'hadrak', 'haelef', 'hafaraim', 'hagaba', 'haggi',
    'hakaliah', 'hakhilah', 'hakkofirim', 'hakmoni', 'halek', 'halohesh', 'hammath', 'hammolekheth',
    'hammothdor', 'hamran', 'haref', 'harheres', 'harif', 'harumaf', 'hashabnah', 'hassenaah',
    'hassenuah', 'hassofereth', 'hasufa', 'hatifa', 'hazaraddar', 'hazarmaveth', 'hazazontamar',
    'hazerhattikon', 'hazorhadattah', 'hazzeleponi', 'hefer', 'hefzibah', 'heglam', 'helam',
    'helef', 'heliopolis', 'heres', 'hereth', 'herodias', 'herodion', 'hilen', 'hizki',
    'hobaiah', 'hofra', 'horhaggidgad', 'hufam', 'huppah', 'hymenaias',
    'idumia', 'iezer', 'ifdeiah', 'iftah', 'iftahel', 'igdaliah', 'ikhabod', 'ikonium',
    'illyrikam', 'india', 'iron', 'iru', 'ishhod', 'ishpah', 'iskah', 'ismakhiah', 'ithlah',
    'iturea', 'iyeabarim', 'iyim', 'izrah',
    'jaar', 'jaareoregim', 'jaasu', 'jada', 'jaddai', 'jafeth', 'jaflet', 'jahzeiah', 'jairas',
    'jamlek', 'jannes', 'jashar', 'jeatherai', 'jeberekhiah', 'jegarsahadutha', 'jehezkel',
    'jehoaddin', 'jehoiakhin', 'jehukal', 'jekhoniah', 'jekoliah', 'jekoniah', 'jeroham',
    'jidlaf', 'joanan', 'joiada', 'jokhebed', 'jorkeam', 'josek', 'joshafat', 'joshah',
    'joshebbasshebeth', 'josifiah', 'jotbah', 'jotbathah', 'jozakar', 'jude', 'julias',
    'jushabhesed', 'justas',
    'kabbon', 'kabul', 'kadeshbarnea', 'kadmon', 'kaftor', 'kaivuan', 'kalkol', 'kalneh',
    'kalno', 'kandeis', 'kanneh', 'kappadosia', 'karka', 'karkas', 'karkhemish', 'karkor',
    'karpas', 'kasifia', 'kasluh', 'kauda', 'kenkhrea', 'keriothhezron', 'keziah',
    'khedorlaomer', 'khefarammoni', 'khefirah', 'khelal', 'khelub', 'khelubai', 'kheluhi',
    'khenani', 'khenaniah', 'kherith', 'khezib', 'khidon', 'khileab', 'khilion', 'khilmad',
    'khimham', 'khislothtabor', 'khitlish', 'kirheres', 'kiriathbaal', 'kiriathhuzoth',
    'kiriathsefer', 'klaudias', 'klement', 'kleopas', 'klopas', 'kolhozeh', 'kolose',
    'konaniah', 'kos', 'kosam', 'kozbi', 'kozeba', 'kresen', 'krispas', 'kuartas', 'kuirinias',
    'kush', 'kushanrishathaim', 'kushi', 'kuth', 'kuthah',
    'ladan', 'laisah', 'lappidoth', 'lasia', 'lazaras', 'lehab', 'lethusim', 'likaonia',
    'linas', 'loammi', 'lodebar', 'loruhamah', 'luka', 'lusias', 'lydda', 'lysia',
    'maasai', 'magadan', 'mahalab', 'mahalaleel', 'mahanehdan', 'mahavah', 'mahershalahashbaz',
    'makaz', 'makbannai', 'makbenah', 'makhi', 'makhijah', 'makhiram', 'makhishua',
    'maknadebai', 'makri', 'malakhi', 'malkhiah', 'malkhiel', 'malkhijah', 'malkhishua',
    'malkhus', 'maluk', 'malukhi', 'manoah', 'maok', 'mareal', 'markaboth', 'mattattah',
    'matthan', 'meholah', 'mekherath', 'melkhi', 'melkhizedek', 'memukan', 'meni', 'menuhoth',
    'meribathkadesh', 'merodak', 'meronoth', 'meshilemith', 'meshobab', 'methushael', 'middin',
    'mifibosheth', 'migdalel', 'migdalgad', 'migdol', 'migron', 'mijamin', 'mikloth',
    'mikmethath', 'miletas', 'mirmah', 'mishal', 'mishrai', 'mispereth', 'misrefothmaim',
    'mithni', 'mitylene', 'molok', 'moresethgath',
    'nafath', 'nafish', 'naftuh', 'naggai', 'nakon', 'narsissas', 'nebushazban', 'nefeg',
    'nefilim', 'nefisim', 'neftoah', 'nefushesim', 'nehelam', 'nereas', 'nergalsharezer',
    'nidas', 'nikopolis', 'nisrok', 'nymfas',
    'ofel', 'ofni', 'ofrah', 'onesimas',
    'paddan', 'pafos', 'paradais', 'parnak', 'parsin', 'parthia', 'patara', 'pathru',
    'pathrus', 'pelon', 'pelusium', 'pentekos', 'perezuzza', 'perezuzzah', 'pergamum',
    'peullethai', 'pibeseth', 'piram', 'pishon', 'pispa', 'pokherethhazzebaim', 'pontas',
    'pontias', 'prisilla', 'prokhoras', 'publias', 'puth',
    'rafa', 'rafah', 'rafu', 'rama', 'ramathaimzofim', 'refael', 'refah', 'refan', 'regium',
    'rekah', 'rekhab', 'resa', 'resef', 'rezef', 'ribnah', 'rifath', 'rimmonperez', 'rizia',
    'roda', 'romamtiezer', 'rufas',
    'saf', 'sakar', 'sakhar', 'samgarnebo', 'samothrasia', 'sanbalat', 'sapfira', 'saraf',
    'sarsekhim', 'sefar', 'seguk', 'sekakah', 'sekundus', 'seleusia', 'semein', 'sennakherib',
    'sergius', 'shaaf', 'shaalbon', 'shaalim', 'shaarim', 'shafam', 'shafir', 'shagee',
    'shallekheth', 'shalma', 'shalum', 'shamai', 'shamlai', 'shavehkiriathaim', 'shearjashub',
    'sheatiel', 'shebat', 'sheerah', 'shefam', 'shefatiah', 'shefer', 'shefi', 'shefo',
    'shefufam', 'shefufan', 'shekaniah', 'shemakhiah', 'sheol', 'shethur', 'shibah', 'shifi',
    'shifmoth', 'shifrah', 'shiftan', 'shihorlibnath', 'shion', 'shitthim', 'shobak', 'shofak',
    'shuhah', 'shulam', 'shullam', 'shumath', 'siene', 'sifas', 'sifmoth', 'silvanas',
    'sintikhe', 'sirakus', 'sitni', 'skeva', 'sofereth', 'soko', 'stakhus', 'stefanas',
    'stefen', 'sukath', 'sukkiim', 'sukkothbenoth', 'susanna',
    'taanathshiloh', 'taber', 'tabrimmon', 'tafath', 'tahkhemon', 'tertias', 'tertullas',
    'thaddeas', 'theofilas', 'thiatira', 'thudas', 'tifsah', 'tigris', 'timias', 'timoti',
    'tirannas', 'tirath', 'tofel', 'tokhen', 'tolemais', 'trakhonitis', 'trifana', 'trifosa',
    'tubalkain', 'ufaz', 'urbanas', 'uzzensheerah', 'vaizatha', 'zafon', 'zakkai', 'zakkhias',
    'zalaf', 'zanaan', 'zarefat', 'zarefath', 'zeba', 'zebidah', 'zefo', 'zefon', 'zekhariah',
    'zekher', 'zela', 'zemari', 'zeus', 'zifion', 'zifron', 'zior', 'ziv', 'zofim', 'zozabad',
    'zaanaim', 'zaanan', 'zaanannim', 'zaavan', 'zabad', 'zabbai', 'zabbud', 'zabdi', 'zabdiel', 'zabud',
    'zaccai', 'zacchaeus', 'zacchur', 'zachariah', 'zacher', 'zadok', 'zaham', 'zair', 'zakkur', 'zalmon',
    'zalmonah', 'zalmunna', 'zamzummim', 'zanoah', 'zaphon', 'zara', 'zarah', 'zareah', 'zared', 'zarephath',
    'zaretan', 'zarethan', 'zarhite', 'zartanah', 'zarthan', 'zatthu', 'zattu', 'zavan', 'zaza', 'zealot',
    'zebadiah', 'zebah', 'zebaim', 'zebedee', 'zebina', 'zeboiim', 'zeboim', 'zebudah', 'zebul', 'zebulonite',
    'zechariah', 'zedad', 'zedekiah', 'zeeb', 'zelah', 'zelek', 'zelofehad', 'zelophehad', 'zelzah', 'zemaraim',
    'zemarite', 'zemira', 'zemirah', 'zenan', 'zenas', 'zephaniah', 'zefaniah', 'zefath', 'zefathah', 'zephi',
    'zepho', 'zephon', 'zer', 'zerah', 'zerahiah', 'zered', 'zereda', 'zeredah', 'zeredathah', 'zererah',
    'zeresh', 'zereth', 'zereth-shahar', 'zeri', 'zeror', 'zeruah', 'zerubbabel', 'zeruiah', 'zetham', 'zethan',
    'zethar', 'ziba', 'zibeon', 'zibia', 'zibiah', 'zichri', 'ziddim', 'zidkijah', 'zidon',
    # Note: 'zia' removed - common word 'manner' in Tedim
    'zidonian', 'zif', 'ziha', 'ziklag', 'zikri', 'zillah', 'zillethai', 'zilpah', 'zilthai', 'zimmah',
    'zimran', 'zimri', 'zina', 'ziph', 'ziphah', 'ziphim', 'ziphion', 'ziphite', 'ziphron',
    # Note: 'zin' removed - common word 'journey/travel' in Tedim
    'zippor', 'zipporah', 'zithri', 'ziz', 'ziza', 'zizah', 'zoan', 'zoar', 'zoba', 'zobah',
    'zobebah', 'zohar', 'zoheleth', 'zoheth', 'zofah', 'zofai', 'zofar', 'zofa', 'zorah', 'zorathite',
    'zoreah', 'zorite', 'zorobabel', 'zuar', 'zuf', 'zuph', 'zur', 'zuriel', 'zurishaddai', 'zuzim',
    # Round 188b: Additional proper nouns
    'athen', 'athens',  # Acts 17:15-21 - city of Athens
    # Round 194: Place names from remaining unknowns
    'harosheth', 'gibeath', 'temelah',  # Judges 4, Josh 5, Ezra 2
    # Round 196: More place names
    'rods',  # Acts 21:1 - Rhodes (Greek island)
    # Round 197: Final proper nouns and loanwords
    'khorazin',      # Chorazin - city cursed by Jesus (Matt 11:21)
    'elohe',         # El-Elohe-Israel (Gen 33:20)
    'zafenath',      # Zaphenath-paneah - Joseph's Egyptian name (Gen 41:45)
    'haaraloth',     # Gibeath-haaraloth - place of circumcision (Josh 5:3)
    'shahar',        # Zereth-shahar - place (Josh 13:19)
    'timnathheres',  # Timnath-heres - Joshua's burial place (Judg 2:9)
    'elohim',        # Gibeath-elohim - place (1Sam 10:5)
    'seku',          # Secu - place near Ramah (1Sam 19:22)
    'aniam',         # Aniam - son of Shemida (1Chr 7:19)
    'labanon',       # Lebanon variant spelling
    'kerenhappuk',   # Keren-happuch - Job's daughter (Job 42:14)
    'korban',        # Korban - Hebrew offering term (Mark 7:11)
    'effatha',       # Ephphatha - Aramaic "be opened" (Mark 7:34)
    'saffron',       # saffron - spice (Song 4:14)
    'ruby',          # ruby - gemstone (Ezek 27:16)
    'terebinth',     # terebinth - tree type (Hos 4:13)
    'githa',         # gittith - musical term (Psa 150:3)
    'khrisoprase',   # chrysoprase - gemstone (Rev 21:20)
    'porsias',       # Porcius Festus (Acts 24:27)
    # Round 198: More place names
    'sufa',          # Sufa region (Num 21:14)
    'suf',           # Suf/Suph - Red Sea area (Deut 1:1)
    # Round 199: More proper nouns
    'reke',          # Rekem - Midianite king (Josh 13:21)
    
    # === Lexicon internalization (2024-03-18) ===
    # Biblical proper nouns from external ctd_lexicon.tsv (lowercase forms)
    'david',         # 1053x - King David
    'moses',         # 866x
    'khrih',         # 643x - Christ
    'jew',           # 346x
    'jakob',         # 339x - Jacob
    'solomon',       # 303x
    'josef',         # 271x - Joseph
    'faro',          # 269x - Pharaoh
    'joshua',        # 224x
    'peter',         # 217x
    'jordan',        # 190x
    'johan',         # 169x - John
    'benjamin',      # 153x
    'manasseh',      # 146x
    'jonathan',      # 120x
    'syria',         # 119x
    'hangun',        # 117x - Christ variant/compound
    'esau',          # 110x
    'jeroboam',      # 104x
    'elijah',        # 96x
    'ezekiel',       # 94x
    'farisi',        # 93x - Pharisee
    'reuben',        # 87x
    'galilee',       # 85x
    'jehoshafat',    # 85x - Jehoshaphat
    'gad',           # 81x
    'job',           # 69x
    'daniel',        # 69x
    'mary',          # 64x
    'lebanon',       # 62x
    'herod',         # 59x
    'jerikho',       # 56x - Jericho
    'josiah',        # 56x
    'eufratis',      # 54x - Euphrates
    'judea',         # 49x
    'simeon',        # 48x
    'gideon',        # 45x
    'rom',           # 44x - Roman
    'zebulun',       # 43x
    'kohath',        # 42x
    'judas',         # 41x
    'james',         # 41x
    'issakhar',      # 37x - Issachar
    'ethiopia',      # 35x
    'korah',         # 34x
    'ginalo',        # 39x - Belial
    'persia',        # 30x
    'boaz',          # 29x
    'jonah',         # 29x
    'grik',          # 26x - Greek
    'masedonia',     # 25x - Macedonia
    'refaim',        # 17x - Rephaim
    'kapernaum',     # 17x - Capernaum
    'zebedi',        # 11x - Zebedee
    'apollos',       # 11x
    'ofir',          # 10x - Ophir
    'molek',         # 10x - Molech
    'shefelah',      # 10x - Shephelah
    'thesalonika',   # 10x - Thessalonica
    'korin',         # 10x - Corinth
    'jakhin',        # 9x - Jachin
    'jabeshgilead',  # 9x - Jabesh-Gilead
    'shadrak',       # 9x - Shadrach
    'kiriatharba',   # 8x - Kiriath-Arba
    'sapfaia',       # 8x - Sapphire (place)
    'maakath',       # 8x - Maachathite
    'khereth',       # 8x - Cherethite
    'meshek',        # 8x - Meshech
    'khebar',        # 8x - Chebar river
    'girgash',       # 7x - Girgashite
    'hanok',         # 7x - Hanoch
    'bethshemesh',   # 7x - Beth-Shemesh
    'ahinoam',       # 7x
    'tishbe',        # 7x - Tishbite
    'sefarvaim',     # 7x - Sepharvaim
    'memfis',        # 7x - Memphis
    'amos',          # 7x
    'filippi',       # 7x - Philippi
    'bethaven',      # 6x - Beth-Aven
    'taanak',        # 6x - Taanach
    'bethshean',     # 6x - Beth-Shean
    'hushah',        # 6x - Hushathite
    'laodisia',      # 6x - Laodicea
    'hofni',         # 5x - Hophni
    'refaiah',       # 5x - Rephaiah
    'ekanah',        # 5x - Elkanah
    'tarsas',        # 5x - Tarsus
    'tikhikas',      # 5x - Tychicus
    'bethhoron',     # 14x - Beth-Horon
    'andru',         # 13x - Andrew
    'martha',        # 13x
    'efesa',         # 21x - Ephesus
    'elizabeth',     # 12x - Elisabeth
    'marka',         # 11x - Mark
    'kornelias',     # 9x - Cornelius
    'elifelet',      # 7x - Eliphelet
    'feliks',        # 7x - Felix
    'eziongeber',    # 3x - Ezion-Geber
    'refidim',       # 2x - Rephidim
    'mediterranean', # 11x
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def clean_word(word: str) -> str:
    """Remove punctuation from word, including quotes at word boundaries.
    Note: Interior and trailing apostrophes (both ' and ') are preserved as they are meaningful in Tedim.
    Examples: keima-a' (1SG.self.GEN), ke'n (1SG.PRO), Topa' (Lord's)
    """
    # Handle curly quotes (", ", ', ') and other Unicode punctuation
    # Leading: remove quotes, brackets including leading apostrophes that are quote marks
    word = re.sub(r'^["\u201c\u201d\u2018\u2019\'\[\(\xab\u201e]+', '', word)
    # Trailing: remove punctuation, double quotes, brackets
    # Also remove apostrophe/curly quote when preceded by comma/punctuation (closing quotes)
    # Pattern: word,'\n or word,"
    word = re.sub(r',["\'\u2018\u2019\u201c\u201d]+$', '', word)  # Remove ,' or ," at end
    word = re.sub(r'\?["\'\u2018\u2019]+$', '?', word)  # Keep ? but remove trailing quote
    word = re.sub(r'!["\'\u2018\u2019]+$', '', word)  # Remove !' or !" at end (exclamation + quote)
    word = re.sub(r'[.,;:!?\u201c\u201d"\)\]\xbb]+$', '', word)  # Remove other trailing punct
    return word


def disambiguate_morpheme(morpheme: str, context: dict) -> str:
    """
    Disambiguate an ambiguous morpheme based on context.
    
    This function implements contextual disambiguation for polysemous morphemes.
    It examines the morphological and syntactic context to select the most
    appropriate meaning from the AMBIGUOUS_MORPHEMES dictionary.
    
    Args:
        morpheme: The morpheme to disambiguate (lowercase)
        context: Dictionary with contextual information. Recognized keys:
            - 'position': Where in word ('standalone', 'prefix', 'suffix', 'stem')
            - 'prev_morpheme': The morpheme before this one (e.g., 'kum' for numbers)
            - 'next_morpheme': The morpheme after this one
            - 'has_prefix': True if word has prefix (ka-, na-, a-, ki-, etc.)
            - 'has_suffix': True if word has suffix (-te, -na, -in, etc.)
            - 'has_ki_prefix': True if word specifically has ki- (reflexive)
            - 'in_compound': True if part of compound word
    
    Returns:
        str: The appropriate gloss for this context, or None if morpheme
        is not in AMBIGUOUS_MORPHEMES.
    
    Examples:
        >>> disambiguate_morpheme('za', {'position': 'standalone'})
        'hear'
        >>> disambiguate_morpheme('za', {'prev_morpheme': 'kum'})
        'hundred'
        >>> disambiguate_morpheme('vei', {'prev_morpheme': 'khat'})
        'time'
        >>> disambiguate_morpheme('kham', {'has_ki_prefix': True})
        'forbid'
    
    Rule Priority:
        1. Specific contextual triggers (prev_morpheme matches known pattern)
        2. Morphological context (has_prefix, has_suffix)
        3. Default meaning (most common in corpus)
    """
    if morpheme not in AMBIGUOUS_MORPHEMES:
        return None
    
    meanings = AMBIGUOUS_MORPHEMES[morpheme]
    
    # Apply disambiguation rules
    if morpheme == 'za':
        # 'hundred' after kum/sawm or in number context
        if context.get('prev_morpheme') in ('kum', 'sawm', 'tul'):
            return 'hundred'
        # 'hear' with verbal morphology
        if context.get('has_prefix') or context.get('has_suffix'):
            return 'hear'
        # Default: check if followed by tul (thousand)
        if context.get('next_morpheme') == 'tul':
            return 'hundred'
        return 'hear'  # Default to verbal meaning
    
    elif morpheme == 'la':
        # 'and.SEQ' after imperative hen
        if context.get('prev_morpheme') == 'hen':
            return 'and.SEQ'
        # 'take' with verbal morphology (la-in, etc.)
        if context.get('has_suffix') or context.get('has_prefix'):
            return 'take'
        return 'take'  # Default to verbal meaning
    
    elif morpheme == 'na':
        # 'NMLZ' when used as suffix
        if context.get('position') == 'suffix':
            return 'NMLZ'
        # '2SG' when standalone or prefix
        return '2SG'
    
    elif morpheme == 'pa':
        # 'NMLZ.AG' when suffix on verb
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'NMLZ.AG'
        return 'father'
    
    elif morpheme == 'man':
        # Check frozen form manin
        if context.get('in_compound') == 'manin':
            return 'reason'
        # 'finish' with khit
        if context.get('next_morpheme') == 'khit':
            return 'finish'
        return 'finish'  # Default
    
    elif morpheme == 'hang':
        # Almost always 'reason' in Biblical text
        return 'reason'
    
    elif morpheme == 'vei':
        # 'time' after numerals
        if context.get('prev_morpheme') in ('khat', 'nih', 'thum', 'li', 'nga', 'guk', 'sagih', 'giat', 'sawmle'):
            return 'time'
        # 'wave' when has verbal suffix (-a piak pattern = wave offering)
        if context.get('has_suffix'):
            return 'wave'
        return 'sick'
    
    elif morpheme == 'pha':
        # 'good' when used as suffix (thu-pha = blessing)
        if context.get('has_prefix') or context.get('position') == 'suffix':
            return 'good'
        # 'branch' as standalone noun
        return 'branch'
    
    elif morpheme == 'kham':
        # 'forbid' with ki- prefix (kikham = refrain)
        if context.get('has_ki_prefix'):
            return 'forbid'
        # 'hold' after pawi (pawi kham = hold feast)
        if context.get('prev_morpheme') == 'pawi':
            return 'hold'
        # 'gold' as standalone noun (default)
        return 'gold'
    
    elif morpheme == 'mang':
        # 'obey' after thu (thu mang = obey word/command)
        if context.get('prev_morpheme') == 'thu':
            return 'obey'
        # 'dream' as standalone noun (default)
        return 'dream'
    
    elif morpheme == 'hi':
        # 'be' (copula) when preceded by subject prefix
        if context.get('has_prefix'):
            return 'be'
        # 'DECL' sentence-finally (standalone)
        return 'DECL'
    
    elif morpheme == 'sa':
        # 'PERF' after verb stems
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'PERF'
        # 'flesh' as noun
        return 'flesh'
    
    elif morpheme == 'ta':
        # 'PFV' after verbs (aspect marker) - when followed by sentence-final
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'PFV'
        # 'PFV' when standalone but followed by sentence-final markers
        if context.get('next_morpheme') in ['hen', 'hi', 'uh', 'un', 'in', 'a']:
            if context.get('prev_is_verb'):
                return 'PFV'
        # 'child' in nominal compounds (ta-pa, ta-nu) or after possessive
        return 'child'
    
    elif morpheme == 'thei':
        # 'ABIL' when follows another verb (mu thei = can see)
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'ABIL'
        # 'know' when main verb (ka thei, na thei, a thei hi)
        if context.get('has_prefix') or context.get('position') == 'root':
            return 'know'
        # Default: 'know' for standalone
        return 'know'
    
    elif morpheme == 'thum':
        # 'three' (numeral) vs 'entreat' (verb) vs 'mourn' (verb)
        prev = context.get('prev_morpheme', '')
        prev_word = context.get('prev_word', '')
        next_m = context.get('next_morpheme', '')
        
        # NUMERAL: after classifiers/time units/numerals
        numeral_triggers = ('ni', 'kum', 'tul', 'sawm', 'za', 'khat', 'nih', 'li', 'nga', 
                            'guk', 'sagih', 'giat', 'kha', 'zan', 'tapa', 'tanu', 'mi',
                            'hiang', 'hai', 'lawh', 'nai')
        if prev in numeral_triggers:
            return 'three'
        # NUMERAL: before -vei (times): thumvei = three times
        if next_m == 'vei':
            return 'three'
        # NUMERAL: in compound numbers (sawmthum le thum = 33)
        if prev in ('le',) and context.get('position') != 'sentence_final':
            return 'three'
        
        # ENTREAT: 1SG/2SG object markers kong/hong clearly indicate entreating
        if prev in ('kong', 'hong', 'nong'):
            return 'entreat'
        # ENTREAT: ka thum (my entreating) in verbal context
        if prev == 'ka' and context.get('is_verbal'):
            return 'entreat'
        
        # MOURN: kapin thum = weep-mourn (clear mourning indicator)
        if prev_word.endswith('kapin') or prev == 'kapin':
            return 'mourn'
        # MOURN: dahin thum = wailing-mourn
        if prev == 'dahin':
            return 'mourn'
        
        # Default by frequency: numeral > entreat > mourn
        # For ambiguous cases, let sentence-level disambiguation handle it
        return 'three'
    
    elif morpheme == 'tung':
        # 'on' when followed by -ah
        if context.get('next_morpheme') == 'ah':
            return 'on'
        # 'arrive' as verb
        if context.get('has_prefix'):
            return 'arrive'
        return 'on'  # Default to relational noun
    
    # === Henderson 1965 Relational Nouns ===
    # These are spatial/relational nouns that take -ah to form postpositions
    
    elif morpheme == 'sung':
        # 'inside' - relational noun (default)
        # sung-ah = inside-LOC, a sungah = in it
        return 'inside'
    
    elif morpheme == 'kiang':
        # 'beside' - relational noun (default)
        # kiang-ah = beside-LOC
        if context.get('has_prefix') and not context.get('next_morpheme') == 'ah':
            return 'separate'  # Verb: be.separate (rare)
        return 'beside'
    
    elif morpheme == 'lak':
        # 'among' - relational noun
        return 'among'
    
    elif morpheme == 'mai':
        # 'face/front' - default to face (body part)
        # mai-ah = front-LOC, a maitung = before him
        if context.get('next_morpheme') == 'ah':
            return 'front'
        return 'face'
    
    elif morpheme == 'nuai':
        # 'below/under' - relational noun
        return 'below'
    
    elif morpheme == 'lam':
        # CRITICAL: Four homophonous roots
        # lam1 'way/road', lam2 'build', lam3 'dance', lam4 'manner'
        # Before -kik: build (lamkik = rebuild)
        if context.get('next_morpheme') == 'kik':
            return 'build'
        # Before -na (without preceding verb): dance (lamna = dancing)
        if context.get('next_morpheme') == 'na' and not context.get('prev_is_verb'):
            return 'dance'
        # After verb: manner nominalizer (zui-lam = way of following)
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'manner'
        # Before -ah: side/direction
        if context.get('next_morpheme') == 'ah':
            return 'side'
        # Default: road/way
        return 'way'
    
    elif morpheme == 'zo':
        # 'COMPL' (completive) vs 'south'
        # After verb: completive (nei-zo = able to have)
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'COMPL'
        return 'south'
    
    elif morpheme == 'hen':
        # 'JUSS' (jussive) vs 'tie' (verb)
        # - 'JUSS' when standalone/sentence-final (~500x): om hen = "let there be"
        # - 'tie' when with verbal morphology (~50x): hong hen = "tie me", kihen = "be bound"
        # Context: standalone defaults to JUSS; prefix context suggests 'tie'
        if context.get('position') == 'standalone':
            return 'JUSS'
        if context.get('has_prefix') or context.get('position') == 'stem':
            return 'tie'
        return 'JUSS'  # Default to jussive
    
    elif morpheme == 'in':
        # 'ERG' (ergative case on nouns) vs 'CVB' (converb on verbs) vs 'QUOT' (quotative)
        # Note: 'house' is spelled 'inn' (double n), not 'in'
        # 
        # Disambiguation:
        # - After ci: QUOT (quotative marker, "ci-in" = saying)
        # - After verb stem: CVB (converb, same-subject sequential)
        # - After noun: ERG (ergative/instrumental case marker)
        #
        # Key insight: -in on verbs is a converb marking same-subject sequencing
        # ("bawl-in a pai" = having made, he went), not ergative case.
        
        # After ci: QUOT
        if context.get('prev_morpheme') == 'ci':
            return 'QUOT'
        
        # After verb stem: CVB (converb)
        if context.get('prev_is_verb'):
            return 'CVB'
        
        # Default: ERG (ergative case on nouns)
        return 'ERG'
    
    elif morpheme == 'ah':
        # 'LOC' (locative) vs 'DAT' (dative)
        # Henderson doesn't strongly distinguish; default LOC
        # Motion verbs may take DAT reading
        if context.get('prev_is_motion_verb'):
            return 'DAT'
        return 'LOC'
    
    elif morpheme == 'te':
        # 'PL' (plural) - nearly always this
        return 'PL'
    
    elif morpheme == 'pi':
        # 'big' (intensifier in compounds) vs 'grandmother'
        # In compounds: big (khua-pi = city, tuipi = sea)
        if context.get('position') == 'suffix':
            return 'big'
        # Standalone: grandmother (or kinship)
        return 'grandmother'
    
    elif morpheme == 'mu':
        # 'see' - Form I (indicative)
        return 'see.I'
    
    elif morpheme == 'ci':
        # 'say' - quotative verb
        return 'say'
    
    # Default: return first meaning
    return meanings[0][0] if meanings else None


def is_proper_noun(word: str) -> bool:
    """Check if word is a proper noun.
    
    Logic:
    1. If the exact word (case-sensitive) is in PROPER_NOUNS → proper noun
    2. If lowercase AND in common word dicts (VERB_STEMS, NOUN_STEMS, FUNCTION_WORDS) → NOT proper noun
    3. If capitalized AND title-case in PROPER_NOUNS → proper noun
    4. If capitalized AND lowercase in common word dicts → NOT proper noun (sentence-initial)
    5. If capitalized AND unknown → treat as proper noun
    
    This allows both:
    - 'sin' → common word (near)
    - 'Sin' → proper noun (if 'Sin' is in PROPER_NOUNS)
    """
    clean = clean_word(word)
    if not clean:
        return False
    clean_lower = clean.lower()
    
    # 1. Explicit proper noun check (case-sensitive)
    # If 'Sin' is in PROPER_NOUNS, 'Sin' matches but 'sin' does not
    if clean in PROPER_NOUNS:
        return True
    
    # 2. Lowercase input that's a common word
    if clean[0].islower():
        return False  # Lowercase words are never proper nouns
    
    # 3. Capitalized input - check if title form is in PROPER_NOUNS
    if clean.title() in PROPER_NOUNS:
        return True
    
    # 4. Capitalized input - check if lowercase is a known common word
    # This handles sentence-initial common words like 'Pai' (go)
    if is_known_word(clean_lower):
        return False
    
    # 5. Unknown capitalized word - treat as proper noun
    return True


# =============================================================================
# PHRASE BOUNDARY DETECTION (Henderson 1965)
# =============================================================================
#
# Henderson identifies three phrase types in Tedim Chin:
# 1. Subjective phrase: Subject NP (pronominal concord with following verb)
# 2. Predicative phrase: Verb phrase (final in conclusive sentences)
# 3. Adjunctive phrase: Non-subject NP, adverbial
#
# NP boundaries are marked by:
# - Case suffixes: -in (ERG), -ah (LOC), -tawh (COM)
# - Postpositions: panin (ABL), sangin (COMP), dong (TERM)
# - Plural marker: -te (often phrase-final in NPs)
# - Topic/focus: pen (TOP), zong (INCL), bek (RESTR)
#
# =============================================================================

# Phrase boundary markers (suffixes and particles that close NPs)
PHRASE_BOUNDARY_SUFFIXES = {
    'in': 'ERG',      # Ergative (transitive subject)
    'ah': 'LOC',      # Locative
    'tawh': 'COM',    # Comitative 'with'
    'pen': 'TOP',     # Topic marker
    'te': 'PL',       # Noun plural (NP-final)
    'uh': '2/3PL',    # 2nd/3rd person plural agreement clitic (VP marker)
}

PHRASE_BOUNDARY_WORDS = {
    # panin: now parsed as pan-in (ABL-ERG) via suffix stripping
    # sangin handled as sang-in = high-ERG (comparative marker)
    'dong': 'TERM',     # Terminative 'until'
    'tungah': 'on-LOC',
    'sungah': 'inside-LOC',
    'kiangah': 'beside-LOC',
    'lakah': 'among-LOC',
    'maitung': 'before',
}


def is_phrase_boundary(word: str, gloss: str) -> bool:
    """
    Check if a word marks a phrase boundary.
    
    Args:
        word: The word form
        gloss: The analyzed gloss
        
    Returns:
        True if this word ends a phrase (NP or VP)
    """
    word_lower = word.lower().rstrip('.,;:!?"\'')
    
    # Check if word itself is a boundary marker
    if word_lower in PHRASE_BOUNDARY_WORDS:
        return True
    
    # Check if gloss ends with a boundary suffix
    for suffix in PHRASE_BOUNDARY_SUFFIXES:
        if gloss.endswith(suffix) or gloss.endswith(PHRASE_BOUNDARY_SUFFIXES[suffix]):
            return True
    
    # Sentence-final particles
    if gloss in ('DECL', 'Q', 'IMP', 'HORT'):
        return True
    
    return False


def analyze_sentence(sentence: str) -> list:
    """
    Analyze a sentence and return word-by-word analysis with phrase boundaries.
    
    Includes sentence-level disambiguation for homophonous words like 'thum'
    (three/entreat/mourn) that require neighboring word context.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of tuples: (word, segmentation, gloss, is_boundary)
    """
    results = []
    words = sentence.split()
    
    for i, word in enumerate(words):
        # First try with original case
        seg, gloss = analyze_word(word)
        
        # If analyzed as a proper noun (ALL CAPS gloss) but it's not in PROPER_NOUNS,
        # try lowercase to see if it parses as a common word
        # This handles cases like "Nungzuite" which should be "life-follow-PL" not "NUNGZUITE"
        clean = word.lower().rstrip('.,;:!?"\'')
        if gloss == word.upper() and word.title() not in PROPER_NOUNS:
            lower_seg, lower_gloss = analyze_word(word.lower())
            if lower_gloss != word.lower().upper():  # If lowercase version parses differently
                seg, gloss = lower_seg, lower_gloss
        
        # Sentence-level disambiguation for 'thum' homophone
        if clean == 'thum' and gloss == 'three':
            prev_word = words[i-1].lower().rstrip('.,;:!?"\'') if i > 0 else ''
            prev2_word = words[i-2].lower().rstrip('.,;:!?"\'') if i > 1 else ''
            next_word = words[i+1].lower().rstrip('.,;:!?"\'') if i < len(words)-1 else ''
            
            # kong/hong/nong thum = entreat (1SG/2SG object marker + verb)
            if prev_word in ('kong', 'hong', 'nong'):
                gloss = 'entreat'
            # ka thum + verbal marker = I entreat
            elif prev_word == 'ka' and next_word in ('hi', 'uh', 'ing', 'ding', 'theih'):
                gloss = 'entreat'
            # kapin [a] thum = weep-ERG [3SG] mourn (look 1-2 words back for kapin)
            elif prev_word == 'kapin' or prev2_word == 'kapin':
                gloss = 'mourn'
            # dahin thum = wail-mourn
            elif prev_word == 'dahin' or prev2_word == 'dahin':
                gloss = 'mourn'
            # a thum hi/uh in mourning context (3SG mourn) - when followed by hi/uh
            # This is ambiguous without KJV - default to numeral
        
        # Sentence-level disambiguation for 'ngen' (pray vs net)
        # Dictionary: ngen = "net, fishing net" AND "pray, petition"
        # Context: fishing vocabulary (nga 'fish', tuili 'lake/river') → net
        #          prayer vocabulary (thu 'word', pasian 'god') → pray (default)
        if clean == 'ngen' or clean.startswith('ngen'):
            # Look for fishing context words
            # ngabeng = fisherman, nusia = abandon (abandoning nets), khuh = cover (casting nets)
            # tuili/tuipi = lake/sea, nga = fish, gunkuang = boat
            fishing_stems = {'nga', 'ngaman', 'ngakim', 'tuili', 'tuipi', 'ngakaih', 'khawl', 
                             'ngabeng', 'nusia', 'khuh', 'gunkuang'}
            # Check if any fishing stem appears in any word
            sentence_words = [w.lower().rstrip('.,;:!?"\'') for w in words]
            has_fishing_context = any(
                stem in word or word.startswith(stem)
                for word in sentence_words 
                for stem in fishing_stems
            )
            if has_fishing_context:
                # Reparse with 'net' base
                if clean == 'ngen':
                    seg = 'ngen'
                    gloss = 'net'
                elif clean == 'ngente':
                    seg = 'ngen-te'
                    gloss = 'net-PL'
                elif clean.startswith('ngen'):
                    # Handle other inflected forms generically
                    suffix = clean[4:]  # After 'ngen'
                    if suffix:
                        seg = f'ngen-{suffix}'
                        gloss = f'net-{suffix.upper()}'
                    else:
                        seg = 'ngen'
                        gloss = 'net'
        
        # Sentence-level disambiguation for 'kei' (NEG vs 1SG.PRO)
        # Dictionary: kei (adv) = "not"; kei (pro) = "I, myself"
        # Context: with sangin/tawh = pronoun "than me/with me"
        #          after verb = negative marker
        if clean == 'kei' and seg == 'kei' and gloss == 'NEG':
            next_kei_word = words[i+1].lower().rstrip('.,;:!?"\'') if i < len(words)-1 else ''
            # Check if followed by comparison/comitative markers → pronoun
            if next_kei_word in ('sangin', 'tawh', 'tawhin', 'tungah', 'panin'):
                seg = 'kei'
                gloss = '1SG.PRO'
            # "kei ka" = "I + 1SG" = emphatic first person
            elif next_kei_word == 'ka':
                seg = 'kei'
                gloss = '1SG.PRO'
        
        # Sentence-level disambiguation for 'hu' (help vs breath)
        # Dictionary: hu (n) = "breath"; hu (v) = "to block" (Bible shows 'help')
        # Context: "nuntakna hu" = breath of life; "hu tawpna/sang" = give up ghost
        #          Otherwise: help (verb)
        if clean == 'hu' and gloss == 'help':
            prev_word = words[i-1].lower().rstrip('.,;:!?"\'') if i > 0 else ''
            next_hu_word = words[i+1].lower().rstrip('.,;:!?"\'') if i < len(words)-1 else ''
            # "nuntakna hu" = breath of life (Gen 2:7)
            if prev_word == 'nuntakna' or prev_word.startswith('nuntak'):
                seg = 'hu'
                gloss = 'breath'
            # "hu tawpna/sang" = give up ghost/breathe last (Gen 25:8)
            elif next_hu_word in ('tawpna', 'sang', 'sang,'):
                seg = 'hu'
                gloss = 'breath'
        
        boundary = is_phrase_boundary(word, gloss)
        results.append((word, seg, gloss, boundary))
    
    return results


def chunk_sentence(sentence: str) -> list:
    """
    Chunk a sentence into phrases based on boundary markers.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of phrases, where each phrase is a list of (word, seg, gloss) tuples
    """
    analysis = analyze_sentence(sentence)
    phrases = []
    current_phrase = []
    
    for word, seg, gloss, is_boundary in analysis:
        current_phrase.append((word, seg, gloss))
        if is_boundary:
            phrases.append(current_phrase)
            current_phrase = []
    
    # Add any remaining words as final phrase
    if current_phrase:
        phrases.append(current_phrase)
    
    return phrases


# =============================================================================
# NP STRUCTURE ANALYSIS
# =============================================================================
# Tedim Chin NP structure (based on corpus analysis):
#
# Basic template:
#   (POSS-GEN) (DEM) HEAD (PROP) (NUM) (QUANT) (-PL) (CASE)
#
# Examples:
#   mi khat = person one = "one person" (N + NUM)
#   hih mite = this people = "these people" (DEM + N.PL)
#   mi khempeuh = person all = "all people" (N + QUANT)
#   mite' tungah = people-GEN on-LOC = "on the people" (N.PL-GEN + REL-LOC)
#   hih mite khempeuh in = this people all ERG = "all these people ERG" (DEM + N.PL + QUANT + CASE)
#
# Key observations:
# - Demonstratives PRECEDE the head noun (prenominal)
# - Numbers, property words, quantifiers FOLLOW the head (post-nominal)
# - No classifiers - nouns directly precede numbers
# - Plural -te attaches to head or to quantifier (khempeuhte)
# - Case markers close the NP
# =============================================================================

def get_word_class(word: str, gloss: str) -> str:
    """
    Determine the word class of a word based on its form and gloss.
    
    Returns one of:
    - DEM: Demonstrative (hih, tua)
    - N: Noun
    - N.PL: Plural noun
    - N.PROP: Proper noun
    - NUM: Numeral
    - QUANT: Quantifier
    - PROP: Property word (adjective-like)
    - COORD: Coordinator (le)
    - CASE: Case marker (in, ah, tawh, etc.)
    - GEN: Genitive marker
    - REL: Relator noun (tung, nuai, lai, etc.)
    - V: Verb (lexical)
    - V.AUX: Auxiliary verb (hi, om as copula)
    - SUBORD: Subordinator (ciangin, hangin, leh, etc.)
    - SFIN: Sentence-final particle (hi, hiam, hen)
    - PRO: Pronoun
    - ADV: Adverb
    - NEG: Negation
    - CONJ: Conjunction/Connective
    - OTHER: Unclassified
    """
    word_lower = word.lower().rstrip('.,;:!?"\'')
    
    # Check demonstratives FIRST (tua, hih, etc.)
    if word_lower in DEMONSTRATIVES:
        return 'DEM'
    
    # Check adverbs
    if word_lower in ADVERBS:
        return 'ADV'
    
    # Check temporal connectives (ciang, tu, tuni, etc.)
    if word_lower in TEMPORAL_CONNECTIVES:
        return 'CONJ'
    
    # Check numerals
    if word_lower in NUMERALS:
        return 'NUM'
    
    # Check quantifiers (both original and extended)
    if word_lower in QUANTIFIERS or word_lower in QUANTIFIERS_EXTENDED:
        return 'QUANT'
    
    # Check property words (bare form only)
    if word_lower in PROPERTY_WORDS:
        return 'PROP'
    
    # Check coordinator
    if word_lower in COORDINATOR:
        return 'COORD'
    
    # Check subordinators
    if word_lower in SUBORDINATORS:
        return 'SUBORD'
    
    # Check negation
    if word_lower in NEGATION or gloss in ('NEG', 'NEG.EMPH'):
        return 'NEG'
    
    # Check agreement markers (standalone subject prefixes)
    if gloss in ('1SG', '2SG', '3SG', '1PL', '2PL', '3PL', '1PL.INCL', '1PL.EXCL'):
        return 'AGR'  # Agreement marker (proclitic to verb)
    
    # Check pronouns
    if word_lower in PRONOUNS or gloss.endswith('.PRO') or gloss.endswith('.POSS'):
        return 'PRO'
    
    # Check case markers in gloss
    case_endings = ('-ERG', '-LOC', '-COM', '-ABL', '-ALL', '-GEN', '-DAT', '-INS')
    case_glosses = ('ERG', 'LOC', 'COM', 'ABL', 'ALL', 'DAT', 'INS', 'BEN')
    if any(gloss.endswith(e) for e in case_endings) or gloss in case_glosses:
        return 'CASE'
    
    # Check for genitive (possessive)
    if gloss.endswith('-GEN') or gloss.endswith('.GEN') or word_lower.endswith("'"):
        return 'GEN'
    
    # Check for relator nouns (spatial)
    if word_lower in RELATOR_NOUNS:
        return 'REL'
    
    # Check sentence-final markers
    if word_lower in SENTENCE_FINAL_MARKERS or gloss in ('DECL', 'Q', 'JUSS', 'HORT'):
        return 'SFIN'
    
    # Check for plural nouns EARLY (before noun_glosses check)
    if '-PL' in gloss and not gloss.startswith('2/3'):
        return 'N.PL'
    
    # Check for nouns by gloss when word is ambiguous
    # Some words appear in both VERB_STEMS and NOUN_STEMS (e.g., lung = feel/heart)
    # Use gloss to disambiguate before checking stem dictionaries
    noun_glosses = {'heart', 'stone', 'altar', 'path', 'road', 'river', 'tree', 'house', 
                    'person', 'hand', 'eye', 'head', 'body', 'land', 'place',
                    'word', 'time', 'day', 'year', 'water', 'fire', 'light', 'name',
                    'king', 'lord', 'son', 'father', 'mother', 'child', 'man', 'woman'}
    gloss_base = gloss.split('-')[0].split('.')[0].lower()
    if gloss_base in noun_glosses:
        return 'N'
    
    # Check for verbs - multiple detection strategies
    # 1. Verb stems in lexicon
    if word_lower in VERB_STEMS:
        return 'V'
    
    # 2. Verb with agreement prefix in gloss
    if gloss.startswith(('1SG-', '2SG-', '3SG-', '1PL-', '2PL-', '3PL-', 'REFL-', '2→1', '3→1', '1→2', '1→3')):
        return 'V'
    
    # 3. Verb stem markers in gloss (Form I/II, TAM, derivational)
    verb_gloss_markers = ('.I', '.II', '-IRR', '-PFV', '-COMPL', '-ITER', '-CONT', '-CAUS', '-APPL', '-ABIL',
                          '-exit', '-enter', '-up', '-down', '-out', '-in')  # directional suffixes
    if any(m in gloss for m in verb_gloss_markers):
        return 'V'
    
    # 4. Common verb glosses (base form before any suffix)
    verb_glosses = {'see', 'hear', 'say', 'go', 'come', 'give', 'take', 'know', 'make', 'do',
                    'exist', 'have', 'want', 'eat', 'drink', 'die', 'live', 'be.born', 'build',
                    'rule', 'follow', 'help', 'love', 'believe', 'finish', 'divide', 'create',
                    'cause', 'call', 'write', 'read', 'send', 'bring', 'carry', 'put', 'sit',
                    'stand', 'lie', 'sleep', 'wake', 'rise', 'fall', 'run', 'walk', 'fly'}
    gloss_base = gloss.split('-')[0].split('.')[0].lower()
    if gloss_base in verb_glosses:
        return 'V'
    
    # 5. Check if first component of compound is a verb stem
    # e.g., khen-khia → divide-exit, where 'khen' is a verb
    if '-' in gloss:
        first_part = gloss.split('-')[0].lower()
        if first_part in verb_glosses:
            return 'V'
        # Also check if first morpheme of segmentation is a verb
        if '-' in word_lower:
            first_morph = word_lower.split('-')[0]
            if first_morph in VERB_STEMS:
                return 'V'
    
    # Check for proper nouns
    # 1. All caps gloss = opaque proper noun (JERUSALEM, GALILI)
    if gloss.isupper() and len(gloss) > 2 and not gloss.startswith(('1', '2', '3')):
        return 'N.PROP'
    # 2. Transparent proper nouns (Pasian→God, Topa→Lord, Lungdamna→good.news-NMLZ)
    word_title = word.title() if word else ''
    if word_title in TRANSPARENT_PROPER_NOUNS:
        return 'N.PROP'
    
    # Default to noun
    return 'N'


def pos_tag_sentence(sentence: str) -> list:
    """
    POS-tag a sentence, returning full analysis for each word.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of tuples: (word, segmentation, gloss, pos_tag)
        
    Example:
        >>> pos_tag_sentence("Pasian in vantung a piangsak hi")
        [('Pasian', 'Pasian', 'PASIAN', 'N.PROP'),
         ('in', 'in', 'ERG', 'CASE'),
         ('vantung', 'van-tung', 'sky-on', 'N'),
         ('a', 'a', '3SG', 'AGR'),
         ('piangsak', 'piangsak', 'cause.birth', 'V'),
         ('hi', 'hi', 'DECL', 'SFIN')]
    """
    result = []
    for word in sentence.split():
        seg, gloss = analyze_word(word)
        pos = get_word_class(word, gloss)
        result.append((word, seg, gloss, pos))
    return result


def format_pos_tagged(sentence: str, format='inline') -> str:
    """
    Format a POS-tagged sentence for display.
    
    Args:
        sentence: A string of space-separated words
        format: 'inline' for word/POS, 'vertical' for aligned columns
        
    Returns:
        Formatted string
        
    Example (inline):
        "Pasian/N.PROP in/CASE vantung/N a/AGR piangsak/V hi/SFIN"
        
    Example (vertical):
        Word       Seg            Gloss               POS
        Pasian     Pasian         PASIAN              N.PROP
        in         in             ERG                 CASE
        ...
    """
    tagged = pos_tag_sentence(sentence)
    
    if format == 'inline':
        return ' '.join(f"{word}/{pos}" for word, seg, gloss, pos in tagged)
    
    elif format == 'vertical':
        lines = [f"{'Word':<12} {'Seg':<15} {'Gloss':<20} {'POS':<8}"]
        lines.append("-" * 60)
        for word, seg, gloss, pos in tagged:
            lines.append(f"{word:<12} {seg:<15} {gloss:<20} {pos:<8}")
        return '\n'.join(lines)
    
    else:
        raise ValueError(f"Unknown format: {format}")


# Subordinators - words that introduce subordinate clauses
SUBORDINATORS = {
    'ciangin': 'when',           # temporal - "when X happened"
    'hangin': 'because',         # causal - "because of X"
    'hanga': 'because.of',       # causal with object
    'bangin': 'like',            # comparative - "like X"
    'dingin': 'in.order.to',     # purpose
    'ahih': 'being',             # "that being so"
    'ahihmanin': 'therefore',    # consequence
    'ahihleh': 'if.so',          # conditional
    'zawkciangin': 'after',      # temporal sequence
    'masaciangin': 'before',     # temporal precedence
    'cianga': 'when',            # temporal variant
}

# Pronouns
PRONOUNS = {
    'kei': '1SG.PRO',            # I
    'nang': '2SG.PRO',           # you (sg)
    'amah': '3SG.PRO',           # he/she/it
    'eite': '1PL.EXCL.PRO',      # we (exclusive)
    'eimah': '1PL.EXCL.PRO',     # we (exclusive, emphatic)
    'note': '2PL.PRO',           # you (pl)
    'amaute': '3PL.PRO',         # they
    'nangmah': '2SG.PRO.EMPH',   # you (emphatic)
    'keimah': '1SG.PRO.EMPH',    # I (emphatic)
}


# =============================================================================
# VERB ARGUMENT FRAMES
# =============================================================================
# Transitivity classification based on corpus analysis of ERG marker frequency:
# - TRANS: >40% ERG marking - canonical transitives (agent acts on patient)
# - AMBI: 20-40% ERG marking - ambitransitive (can be used trans or intrans)
# - INTR: <20% ERG marking - intransitive (single argument)
#
# Case frame notation:
# - ERG: Ergative (transitive subject)
# - ABS: Absolutive (intransitive subject, transitive object)
# - DAT: Dative (recipient, experiencer)
# - LOC: Locative (location, goal)
# - COM: Comitative (accompaniment)
# - ABL: Ablative (source)
# =============================================================================

VERB_FRAMES = {
    # Intransitive verbs (single argument, ABS subject)
    'hi': ('INTR', ['ABS'], 'be/copula'),
    'om': ('INTR', ['ABS', 'LOC'], 'exist/stay'),
    'pai': ('INTR', ['ABS', 'LOC'], 'go'),
    'sih': ('INTR', ['ABS'], 'die'),
    'nungta': ('INTR', ['ABS'], 'live'),
    'hong': ('INTR', ['ABS', 'ABL'], 'come'),  # Can take source
    'suak': ('INTR', ['ABS'], 'become'),
    'ki': ('INTR', ['ABS'], 'flee/run'),
    
    # Transitive verbs (two arguments: ERG agent, ABS patient)
    'ngai': ('TRANS', ['ERG', 'ABS'], 'love/need'),
    'dawt': ('TRANS', ['ERG', 'ABS'], 'love'),
    'en': ('TRANS', ['ERG', 'ABS'], 'look.at'),
    'hawl': ('TRANS', ['ERG', 'ABS'], 'seek'),
    'bei': ('TRANS', ['ERG', 'ABS'], 'finish/complete'),
    
    # Ambitransitive verbs (can be used transitively or intransitively)
    'mu': ('AMBI', ['ERG', 'ABS'], 'see'),
    'muh': ('AMBI', ['ERG', 'ABS'], 'see.II'),
    'za': ('AMBI', ['ERG', 'ABS'], 'hear'),
    'zak': ('AMBI', ['ERG', 'ABS'], 'hear.II'),
    'ci': ('AMBI', ['ERG', 'ABS', 'DAT'], 'say'),
    'gen': ('AMBI', ['ERG', 'ABS', 'DAT'], 'tell'),
    'bawl': ('AMBI', ['ERG', 'ABS'], 'make/do'),
    'nei': ('AMBI', ['ERG', 'ABS'], 'have'),
    'neih': ('AMBI', ['ERG', 'ABS'], 'have.II'),
    'thei': ('AMBI', ['ERG', 'ABS'], 'know'),
    'theih': ('AMBI', ['ERG', 'ABS'], 'know.II'),
    'ne': ('AMBI', ['ERG', 'ABS'], 'eat'),
    'nek': ('AMBI', ['ERG', 'ABS'], 'eat.II'),
    'dawn': ('AMBI', ['ERG', 'ABS'], 'drink'),
    
    # Ditransitive verbs (three arguments: ERG agent, ABS theme, DAT recipient)
    'pia': ('DITRANS', ['ERG', 'ABS', 'DAT'], 'give'),
    'piak': ('DITRANS', ['ERG', 'ABS', 'DAT'], 'give.II'),
    'pia(k)sak': ('DITRANS', ['ERG', 'ABS', 'DAT'], 'give.for'),
    
    # Verbs with oblique arguments
    'zui': ('AMBI', ['ERG', 'ABS'], 'follow'),
    'tom': ('AMBI', ['ERG', 'COM'], 'meet'),  # Takes comitative
    'uk': ('AMBI', ['ERG', 'ABS'], 'rule'),
    'huh': ('AMBI', ['ERG', 'ABS'], 'help'),
    'bia': ('AMBI', ['ERG', 'ABS'], 'worship'),
    'piang': ('AMBI', ['ABS'], 'be.born'),  # Usually intrans for passive
    'piangsak': ('TRANS', ['ERG', 'ABS'], 'create/cause.birth'),  # Causative
    'lak': ('AMBI', ['ERG', 'ABS', 'ABL'], 'take'),  # Takes source
    'pua': ('AMBI', ['ERG', 'ABS'], 'carry'),
    'khen': ('AMBI', ['ERG', 'ABS', 'ABL'], 'divide/separate'),
    'zawh': ('AMBI', ['ERG', 'ABS'], 'finish'),
    'lem': ('AMBI', ['ERG', 'ABS'], 'keep'),
}


def get_verb_frame(verb: str) -> tuple:
    """
    Get the argument frame for a verb.
    
    Args:
        verb: The verb stem (Form I or II)
        
    Returns:
        Tuple of (transitivity, case_list, gloss) or None if not found
        
    Example:
        >>> get_verb_frame('mu')
        ('AMBI', ['ERG', 'ABS'], 'see')
    """
    verb_lower = verb.lower().rstrip('.,;:!?"\'')
    
    # Direct lookup
    if verb_lower in VERB_FRAMES:
        return VERB_FRAMES[verb_lower]
    
    # Try stripping common suffixes
    for suffix in ['ding', 'ta', 'zo', 'kik', 'nawn', 'thei', 'sak', 'pih', 'khawm']:
        if verb_lower.endswith(suffix) and len(verb_lower) > len(suffix):
            base = verb_lower[:-len(suffix)]
            if base in VERB_FRAMES:
                return VERB_FRAMES[base]
    
    # Check VERB_STEMS for transitivity hint
    if verb_lower in VERB_STEMS:
        gloss = VERB_STEMS[verb_lower]
        # Default to AMBI for unknown verbs
        return ('AMBI', ['ERG', 'ABS'], gloss)
    
    return None


def analyze_np_structure(words: list) -> dict:
    """
    Analyze the structure of a noun phrase.
    
    Args:
        words: List of (word, segmentation, gloss) tuples
        
    Returns:
        Dictionary with:
        - pattern: String describing the structure (e.g., "DEM + N.PL + QUANT + CASE")
        - slots: Dict mapping word class to words in that slot
        - head: The head noun (if identifiable)
        - gloss_sequence: The full gloss as a string
    """
    word_classes = []
    slots = {}
    gloss_parts = []
    
    for word, seg, gloss in words:
        wc = get_word_class(word, gloss)
        word_classes.append(wc)
        
        if wc not in slots:
            slots[wc] = []
        slots[wc].append((word, seg, gloss))
        gloss_parts.append(gloss)
    
    pattern = ' + '.join(word_classes)
    
    # Try to identify the head noun
    head = None
    for wc in ('N', 'N.PL'):
        if wc in slots:
            head = slots[wc][0]  # First noun is likely head
            break
    
    return {
        'pattern': pattern,
        'slots': slots,
        'head': head,
        'gloss_sequence': ' '.join(gloss_parts),
        'word_classes': word_classes,
    }


def extract_nps_from_sentence(sentence: str) -> list:
    """
    Extract noun phrases from a sentence.
    
    Uses phrase boundary detection to identify NP chunks, then analyzes
    the structure of each potential NP.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of NP analysis dictionaries
    """
    from analyze_morphemes import analyze_sentence
    
    analysis = analyze_sentence(sentence)
    nps = []
    current_np = []
    
    for word, seg, gloss, is_boundary in analysis:
        wc = get_word_class(word, gloss)
        
        # Start collecting NP when we see DEM, N, or GEN
        if wc in ('DEM', 'N', 'N.PL', 'GEN', 'REL') and not current_np:
            current_np.append((word, seg, gloss))
        elif current_np:
            current_np.append((word, seg, gloss))
            
            # End NP at case marker or coordinator
            if wc in ('CASE', 'COORD', 'V') or is_boundary:
                if len(current_np) >= 1:
                    np_analysis = analyze_np_structure(current_np)
                    if 'N' in np_analysis['slots'] or 'N.PL' in np_analysis['slots']:
                        nps.append({
                            'words': current_np,
                            'analysis': np_analysis,
                        })
                current_np = []
    
    # Handle any remaining NP
    if current_np:
        np_analysis = analyze_np_structure(current_np)
        if 'N' in np_analysis['slots'] or 'N.PL' in np_analysis['slots']:
            nps.append({
                'words': current_np,
                'analysis': np_analysis,
            })
    
    return nps


# =============================================================================
# SENTENCE TYPE DETECTION (Henderson 1965)
# =============================================================================
#
# Henderson identifies two sentence types:
# 1. Conclusive: Ends with 'hi' (DECL) - statement of fact
# 2. Inconclusive: Ends with 'leh' - conditional/hypothetical
#
# Conclusive sentences use Form I verbs in final predicative phrase.
# Inconclusive sentences use Form II verbs in final predicative phrase.
#
# =============================================================================

# Sentence-final markers (Henderson pp. 30-31)
SENTENCE_FINAL_MARKERS = {
    'hi': ('DECL', 'conclusive'),       # Declarative - conclusive sentence
    'leh': ('COND', 'inconclusive'),    # Conditional - inconclusive sentence  
    'hiam': ('Q', 'interrogative'),     # Question marker
    'hen': ('JUSS', 'jussive'),         # Jussive/optative "let/may"
    'ta': ('PFV', 'perfective'),        # Perfective (can be sentence-final)
    'rawh': ('HORT', 'hortative'),      # Hortative/polite imperative
    'in': ('ERG', 'subordinate'),       # Ergative often marks subordinate clause
}


def detect_sentence_type(sentence: str) -> dict:
    """
    Detect the sentence type based on Henderson's analysis.
    
    Args:
        sentence: A sentence string
        
    Returns:
        Dictionary with:
        - type: 'conclusive', 'inconclusive', 'interrogative', 'imperative'
        - final_marker: The sentence-final particle
        - expected_verb_form: 'I' (indicative) or 'II' (subjunctive)
    """
    words = sentence.strip().rstrip('.,;:!?"\'').split()
    if not words:
        return {'type': 'unknown', 'final_marker': None, 'expected_verb_form': None}
    
    # Check last word for sentence-final marker
    last_word = words[-1].lower().rstrip('.,;:!?"\'')
    
    # Direct check
    if last_word in SENTENCE_FINAL_MARKERS:
        marker, sent_type = SENTENCE_FINAL_MARKERS[last_word]
        verb_form = 'II' if sent_type == 'inconclusive' else 'I'
        return {'type': sent_type, 'final_marker': marker, 'expected_verb_form': verb_form}
    
    # Check if ends with common sentence-final patterns
    seg, gloss = analyze_word(last_word)
    
    if gloss.endswith('DECL') or 'hi' in gloss.split('-'):
        return {'type': 'conclusive', 'final_marker': 'DECL', 'expected_verb_form': 'I'}
    
    if 'Q' in gloss or 'hiam' in last_word:
        return {'type': 'interrogative', 'final_marker': 'Q', 'expected_verb_form': 'I'}
    
    # Default to conclusive (most common)
    return {'type': 'conclusive', 'final_marker': None, 'expected_verb_form': 'I'}


def analyze_phrase_type(phrase_words: list) -> str:
    """
    Determine if a phrase is subjective, predicative, or adjunctive.
    
    Henderson 1965:
    - Subjective phrase: Subject NP, has pronominal concord with following verb
    - Predicative phrase: Contains verb, final in sentence
    - Adjunctive phrase: Non-subject NP, adverbial, contains Form II verbs
    
    Args:
        phrase_words: List of (word, seg, gloss) tuples
        
    Returns:
        'subjective', 'predicative', or 'adjunctive'
    """
    if not phrase_words:
        return 'unknown'
    
    # Check if phrase contains a verb
    has_verb = False
    has_form_ii = False
    ends_with_case = False
    
    for word, seg, gloss in phrase_words:
        # Check for verb markers
        if any(v in gloss for v in ['see', 'hear', 'say', 'go', 'come', 'give', 'take', 
                                      'know', 'exist', 'be', 'have', 'want', 'make']):
            has_verb = True
        
        # Check for Form II marker
        if '.II' in gloss or gloss.endswith('.II'):
            has_form_ii = True
    
    # Check final word for case marker
    final_gloss = phrase_words[-1][2]
    if any(case in final_gloss for case in ['ERG', 'LOC', 'COM', 'ABL', 'DAT']):
        ends_with_case = True
    
    # Adjunctive: has Form II verb OR ends with case marker (non-final)
    if has_form_ii:
        return 'adjunctive'
    
    # Predicative: has verb (Form I implied)
    if has_verb:
        return 'predicative'
    
    # Subjective: NP without case marker or with nominative/topic
    if ends_with_case:
        return 'adjunctive'
    
    return 'subjective'


def check_pronominal_concord(subject: str, verb_prefix: str) -> bool:
    """
    Check if a subject noun/pronoun concords with a verbal prefix.
    
    Henderson 1965 (pp. 32-33): Pronominal concord distinguishes
    subjective phrases from adjunctive phrases. Subjective phrases
    have concord with following predicative phrases; adjunctive
    phrases do NOT.
    
    Args:
        subject: The subject noun or pronoun
        verb_prefix: The pronominal prefix on the verb (a, ka, na, i)
        
    Returns:
        True if the subject concords with the prefix
        
    Examples:
        >>> check_pronominal_concord('Dahpa', 'a')
        True  # 3rd person noun → a-
        >>> check_pronominal_concord('kei', 'ka')
        True  # 1SG pronoun → ka-
        >>> check_pronominal_concord('kei', 'a')
        False  # 1SG should have ka-, not a-
    """
    subject_lower = subject.lower().rstrip('.,;:!?"\'-')
    
    # Get expected prefix for this subject
    if subject_lower in PRONOMINAL_CONCORD:
        expected = PRONOMINAL_CONCORD[subject_lower]
    else:
        # Default: all other nouns are 3rd person
        expected = PRONOMINAL_CONCORD['_default']
    
    return verb_prefix.lower() == expected


def extract_verb_prefix(analyzed_gloss: str) -> str:
    """
    Extract the pronominal prefix from an analyzed gloss.
    
    Args:
        analyzed_gloss: A gloss string like "3SG-go" or "1SG-have"
        
    Returns:
        The prefix ('a', 'ka', 'na', 'i') or None
    """
    prefix_map = {
        '1SG': 'ka',
        '2SG': 'na',
        '3SG': 'a',
        '1PL.INCL': 'i',
        '1PL.EXCL': 'ka',
        '2PL': 'na',
        '3PL': 'a',
    }
    
    for prefix_gloss, prefix in prefix_map.items():
        if analyzed_gloss.startswith(prefix_gloss + '-'):
            return prefix
    
    return None


# =============================================================================
# CLAUSE STRUCTURE ANALYSIS
# =============================================================================
#
# Tedim Chin clause structure (Henderson 1965):
# - Main clauses: End with sentence-final particle (hi, hiam, etc.)
# - Subordinate clauses: Marked by subordinators (ciangin, hangin, etc.)
# - Relative clauses: Verb (Form II) + relativizer (te, mi, pa, nu)
# - Conditional clauses: End with leh (if/when)
#
# Form I vs Form II:
# - Form I: Main clause verb, conclusive sentence
# - Form II: Subordinate clause verb, before relativizer
#
# =============================================================================

# Clause boundary markers (morphemes that signal clause edges)
CLAUSE_BOUNDARY_MARKERS = {
    # Subordinators (clause-initial or clause-final)
    'ciangin': 'when',       # Temporal
    'hangin': 'because',     # Causal  
    'bangin': 'like',        # Comparative/manner
    'dingin': 'in.order.to', # Purpose
    'ahih': 'being.that',    # Relative/causal
    # Conditional/conditional
    'leh': 'if/when',        # Conditional (clause-final)
    # Quotative
    'ci': 'say',             # Quotative (introduces reported speech)
    'cih': 'say.II',
    # Sentence-final (main clause)
    'hi': 'DECL',            # Declarative (conclusive)
    'hiam': 'Q',             # Interrogative
    'hen': 'JUSS',           # Jussive
    'rawh': 'HORT',          # Hortative
}

# Relativizers (turn verb into modifier)
RELATIVIZERS = {
    'te': 'PL/REL',          # Plural/relativizer
    'mi': 'person.REL',      # Human relativizer
    'pa': 'male.REL',        # Male relativizer  
    'nu': 'female.REL',      # Female relativizer
}

# Switch reference markers (Henderson 1965)
SWITCH_REFERENCE = {
    'in': 'SS.ERG',          # Same-subject + ergative
    'a': 'DS',               # Different-subject prefix
}


def detect_clause_boundaries(sentence: str) -> list:
    """
    Detect clause boundaries in a sentence.
    
    Clause boundaries are marked by:
    1. Subordinators (ciangin, hangin, etc.) 
    2. Sentence-final markers (hi, hiam, etc.)
    3. Quotative verbs (ci, cih)
    4. Relativizers after Form II verbs
    
    Args:
        sentence: A sentence string
        
    Returns:
        List of clause dictionaries, each with:
        - text: The clause text
        - start: Start word index
        - end: End word index
        - boundary_marker: What marks the boundary (or None)
        - clause_type: 'main', 'temporal', 'causal', 'relative', 'conditional', 'quotative'
    """
    words = sentence.strip().split()
    if not words:
        return []
    
    clauses = []
    current_start = 0
    
    for i, word in enumerate(words):
        word_lower = word.lower().rstrip('.,;:!?"\'')
        
        # Check for subordinators (typically clause-final in Tedim)
        is_boundary = False
        clause_type = 'main'
        marker = None
        
        # Temporal subordinators
        if word_lower == 'ciangin':
            is_boundary = True
            clause_type = 'temporal'
            marker = 'ciangin'
        # Causal subordinators
        elif word_lower == 'hangin':
            is_boundary = True
            clause_type = 'causal'
            marker = 'hangin'
        # Purpose subordinators
        elif word_lower == 'dingin':
            is_boundary = True  
            clause_type = 'purpose'
            marker = 'dingin'
        # Comparative/manner
        elif word_lower == 'bangin':
            is_boundary = True
            clause_type = 'comparative'
            marker = 'bangin'
        # Conditional
        elif word_lower == 'leh' and i < len(words) - 1:
            is_boundary = True
            clause_type = 'conditional'
            marker = 'leh'
        # Quotative
        elif word_lower in ('ci', 'cih', 'cin', 'ciin'):
            is_boundary = True
            clause_type = 'quotative'
            marker = word_lower
        # Sentence-final (main clause boundary)
        elif word_lower == 'hi' and i == len(words) - 1:
            is_boundary = True
            clause_type = 'main'
            marker = 'hi'
        # Relative clause: check for relativizer after verb
        elif word_lower in RELATIVIZERS:
            # Look back for Form II verb
            if i > 0:
                prev_word = words[i-1].lower().rstrip('.,;:!?"\'')
                if prev_word.endswith('h'):  # Form II often ends in -h
                    is_boundary = True
                    clause_type = 'relative'
                    marker = word_lower
        
        if is_boundary:
            clause_text = ' '.join(words[current_start:i+1])
            clauses.append({
                'text': clause_text,
                'start': current_start,
                'end': i,
                'boundary_marker': marker,
                'clause_type': clause_type
            })
            current_start = i + 1
    
    # Handle remaining words as final clause
    if current_start < len(words):
        clause_text = ' '.join(words[current_start:])
        clauses.append({
            'text': clause_text,
            'start': current_start,
            'end': len(words) - 1,
            'boundary_marker': None,
            'clause_type': 'main'
        })
    
    return clauses


def classify_clause(clause_text: str, position: str = 'unknown') -> dict:
    """
    Classify a clause by type and expected verb form.
    
    Args:
        clause_text: Text of the clause
        position: 'initial', 'medial', 'final', or 'unknown'
        
    Returns:
        Dictionary with:
        - type: 'main', 'temporal', 'causal', 'relative', 'conditional', 'purpose'
        - expected_form: 'I' (indicative) or 'II' (subjunctive)
        - subordinator: The subordinating morpheme (if any)
        - has_verb: Whether a verb was detected
    """
    words = clause_text.strip().split()
    if not words:
        return {'type': 'unknown', 'expected_form': None, 'subordinator': None, 'has_verb': False}
    
    clause_type = 'main'
    expected_form = 'I'  # Default to Form I for main clauses
    subordinator = None
    
    # Check for subordinators
    for word in words:
        word_lower = word.lower().rstrip('.,;:!?"\'')
        if word_lower == 'ciangin':
            clause_type = 'temporal'
            subordinator = 'ciangin'
            expected_form = 'II'
        elif word_lower == 'hangin':
            clause_type = 'causal'
            subordinator = 'hangin'
            expected_form = 'II'
        elif word_lower == 'dingin':
            clause_type = 'purpose'
            subordinator = 'dingin'
            expected_form = 'II'
        elif word_lower == 'bangin':
            clause_type = 'comparative'
            subordinator = 'bangin'
            expected_form = 'II'
        elif word_lower == 'leh':
            clause_type = 'conditional'
            subordinator = 'leh'
            expected_form = 'II'
    
    # Check for verb presence
    has_verb = False
    for word in words:
        word_lower = word.lower().rstrip('.,;:!?"\'')
        if word_lower in VERB_STEMS or any(word_lower.startswith(v) for v in list(VERB_STEMS.keys())[:50]):
            has_verb = True
            break
    
    # Position-based refinement
    if position == 'final' and clause_type == 'main':
        expected_form = 'I'  # Final main clause uses Form I
    elif position in ('initial', 'medial'):
        # Non-final clauses typically use Form II
        if subordinator is None:
            expected_form = 'II'
    
    return {
        'type': clause_type,
        'expected_form': expected_form,
        'subordinator': subordinator,
        'has_verb': has_verb
    }


def analyze_clause_structure(sentence: str) -> dict:
    """
    Full clause structure analysis for a sentence.
    
    Args:
        sentence: A sentence string
        
    Returns:
        Dictionary with:
        - clauses: List of clause analyses
        - clause_count: Number of clauses
        - main_clause_position: Index of main clause
        - clause_chain: Description of clause chaining pattern
        - verb_forms: Expected verb forms per clause
    """
    clauses = detect_clause_boundaries(sentence)
    
    if not clauses:
        return {
            'clauses': [],
            'clause_count': 0,
            'main_clause_position': None,
            'clause_chain': 'empty',
            'verb_forms': []
        }
    
    n_clauses = len(clauses)
    
    # Analyze each clause with position info
    analyzed_clauses = []
    verb_forms = []
    main_position = None
    
    for i, clause in enumerate(clauses):
        if i == 0:
            position = 'initial'
        elif i == n_clauses - 1:
            position = 'final'
        else:
            position = 'medial'
        
        analysis = classify_clause(clause['text'], position)
        analysis['position'] = position
        analysis['boundary_marker'] = clause.get('boundary_marker')
        
        if analysis['type'] == 'main' and position == 'final':
            main_position = i
        
        analyzed_clauses.append(analysis)
        verb_forms.append(analysis['expected_form'])
    
    # Determine clause chaining pattern
    if n_clauses == 1:
        chain_type = 'simple'
    elif all(c['type'] == 'main' for c in analyzed_clauses):
        chain_type = 'coordinate'
    else:
        subord_types = [c['type'] for c in analyzed_clauses if c['type'] != 'main']
        if subord_types:
            chain_type = f"subordinate:{'+'.join(set(subord_types))}"
        else:
            chain_type = 'complex'
    
    return {
        'clauses': analyzed_clauses,
        'clause_count': n_clauses,
        'main_clause_position': main_position,
        'clause_chain': chain_type,
        'verb_forms': verb_forms
    }
# 
# Tedim Chin compounds can be nested: singnamtui = sing + (nam + tui)
# where namtui is itself a compound (nam=smell + tui=water → perfume)
#
# This system identifies "compound bases" that can serve as heads of larger
# compounds, and recursively analyzes modifiers.
#
# =============================================================================
# HIERARCHICAL COMPOUND ANALYSIS SYSTEM
# =============================================================================
#
# Tedim Chin has productive compound formation where:
# 1. Simple compounds: N + N → compound (e.g., nam + tui → namtui "perfume")
# 2. Complex compounds: N + (N N) or (N N) + N → nested compound
#    e.g., sing + namtui → singnamtui "spices" = tree + (smell + water)
#
# This system represents BOTH:
# - The lexicalized meaning (holistic gloss): "spices"
# - The compositional structure (morpheme-by-morpheme): "tree-(smell-water)"
#
# The analysis returns:
# - segmentation: "sing-nam-tui" (morpheme boundaries)
# - gloss: "spices" (lexical meaning when known)
# - structure: "sing-(nam-tui)" (bracketed structure showing constituency)
# - compositional: "tree-(smell-water)" (meaning of each morpheme)
# =============================================================================

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple, Union

@dataclass
class CompoundStructure:
    """
    Represents the hierarchical structure of a compound word.
    
    Attributes:
        morphemes: List of morpheme strings in order
        segmentation: Hyphen-separated morphemes (e.g., "sing-nam-tui")
        bracketing: Constituency structure (e.g., "sing-(nam-tui)")
        compositional_gloss: Morpheme-by-morpheme meaning (e.g., "tree-(smell-water)")
        lexical_gloss: Holistic/lexicalized meaning if known (e.g., "spices")
        head_position: 'left' for (N N) N, 'right' for N (N N), or None
    """
    morphemes: List[str]
    segmentation: str
    bracketing: str
    compositional_gloss: str
    lexical_gloss: Optional[str] = None
    head_position: Optional[str] = None
    
    def get_display_gloss(self) -> str:
        """Return the best gloss for display - prefer lexical if available."""
        return self.lexical_gloss if self.lexical_gloss else self.compositional_gloss
    
    def get_full_analysis(self) -> str:
        """Return full analysis showing both lexical and compositional."""
        if self.lexical_gloss:
            return f"{self.lexical_gloss} [{self.compositional_gloss}]"
        return self.compositional_gloss


# =============================================================================
# ATOMIC MORPHEME GLOSSES (for compositional analysis)
# =============================================================================
# These are the building blocks - morphemes with their basic meanings.
# Used to compute compositional glosses for compounds.

ATOMIC_GLOSSES = {
    # Body parts
    'lung': 'heart',
    'lu': 'head',
    'khe': 'foot',
    'khut': 'hand',
    'mit': 'eye',
    'bil': 'ear',
    'lei': 'tongue',
    'ha': 'tooth',
    'sam': 'hair',
    'gu': 'bone',
    'thi': 'blood',
    'sa': 'flesh',
    'nak': 'nose',
    
    # Nature
    'tui': 'water',
    'mei': 'fire',      # Also mei 'female' (TB *mei) - homophonous roots
    'van': 'sky',
    'lei': 'earth',
    'ni': 'sun',
    'kha': 'moon',
    'huih': 'wind',
    'gua': 'rain',
    'khu': 'smoke',
    'khuk': 'pool',  # tuikhuk = pool
    
    # Gender (TB cognates)
    # mei 'female' (TB *mei) - distinct from mei 'fire', used in numei, meigong
    # pa 'male/father' - used in many compounds
    
    # Plants/trees
    'sing': 'tree',
    'kung': 'trunk',
    'gah': 'fruit',
    'nang': 'leaf',
    'gui': 'vine',
    'bu': 'grain',
    'an': 'food',
    
    # Animals
    'nga': 'fish',
    'vak': 'bird',
    'sa': 'animal',
    'tuu': 'sheep',
    'bawng': 'cattle',
    'ui': 'dog',
    'ngal': 'wolf',
    'hon': 'flock',
    
    # Qualities
    'dam': 'well',
    'sat': 'hard',
    'nem': 'soft',
    'tang': 'stand',
    'kham': 'forbid',
    'nop': 'want',
    'za': 'feel',
    'kim': 'complete',
    'muang': 'calm',
    'thim': 'dark',
    'siam': 'skilled',
    'mawh': 'guilty',
    'siat': 'spoil',
    'khialh': 'sin',
    'tak': 'true',           # laitakin = exactly.in.midst
    'liat': 'power',         # vangliatna = glory
    'hing': 'kind',          # mihing = person
    'lim': 'form',            # limtak = truly (sign-true)
    
    # Substances
    'nam': 'smell',      # TB root for smell/fragrance
    'pak': 'wine',
    'leeng': 'grape',
    'zu': 'wine',
    'thei': 'fig',
    'buh': 'rice',
    
    # Positions/locations
    'tung': 'above',
    'nuai': 'below',
    'sung': 'inside',
    'lai': 'middle',
    'ki': 'side',
    'lam': 'direction',
    'inn': 'house',
    'mun': 'place',
    'khua': 'town',
    'gam': 'land',
    'lak': 'midst',          # gamlak = land-midst
    
    # Abstracts
    'na': 'NMLZ',        # nominalizer
    'pa': 'male',     # agent/man
    'nu': 'woman',
    'te': 'PL',          # plural (default; also 'small' in some contexts)
    'ki': 'REFL',        # reflexive/reciprocal
    'sai': 'throw',      # throw (in compounds)
    'vang': 'glory',       # vangliat = glory
    
    # Verbal roots
    'sak': 'CAUS',       # causative
    'kik': 'ITER',       # iterative (do again)
    'khia': 'out',       # directional out
    'let': 'back',       # directional back
    'khin': 'COMPL',     # completive
    'tat': 'strike',     # gamtat = kingdom
    'gen': 'speak',      # thugen = speech
    'sim': 'count',      # lungsim = heart
    'sem': 'serve',      # nasem = servant
    'sep': 'work',       # nasep = work
    'bawl': 'make',      # kibawl = be.made
    'pia': 'give',       # kipia = be.given
    'pan': 'begin',      # kipan = begin
    'pawl': 'group',     # pawlkhat = some
    'khat': 'one',       # numeral
    'khop': 'gather',    # kikhop = REFL-gather
    'zui': 'follow',     # nungzui = back-follow = disciple
    'gal': 'enemy',  # galte = enemies
    # 'kap' removed - conflicts with verb stem 'kap' (weep); use compound for galkap
    'heh': 'anger',# hehpih = grace
    'pih': 'APPL',       # applicative
    'suah': 'birth',     # nisuah = day-birth = birthday
    'ngaih': 'love', # ngaihsut = think
    'sut': 'break',  # ngaihsut = deliberate
    'khiat': 'out', # paikhiat = go.out
    'biak': 'worship',   # biakna = worship (NMLZ)
    'piak': 'offer',     # biakpiak = worship-offer
    
    # Round 173: Additional verbal/adjectival roots
    'tha': 'strength',   # thahat = strong
    'hat': 'firm',       # thahat = strength-firm
    'lem': 'prepare',    # kilem = REFL-prepare
    'hot': 'save',  # hotkhiat = salvation
    'nget': 'pray',      # thunget = word-pray = prayer
    'zawng': 'all',      # mizawng = person-all
    'tam': 'many',       # tampi = many-big
    'khen': 'judge',     # thukhen = word-judge = judgment
    'hilh': 'teach',     # thuhilh = word-teach = teaching
    'neu': 'small',      # khuaneu = village-small
    'tuam': 'various',   # tuamtuam = various-REDUP
    
    # Round 174: Additional atomic morphemes from full audit
    'lo': 'NEG',         # lono = NEG-obey = disobey; ALSO lo 'field' (homophonous) in lopa, lokhawh
    'no': 'obey',        # lono = NEG-obey
    'tum': 'all',        # nitum = day-all = always
    'lang': 'clear',# langkhat = side-one
    'la': 'field',  # gamla = land-field
    'et': 'example', # lamet = way-see = example
    'ciam': 'promise',   # kiciam = REFL-promise = covenant
    'teh': 'cross', # singlamteh = wooden.cross
    'mual': 'mountain',  # mualtung = mountain-top
    'kuan': 'family',    # innkuan = house-family = household
    'pang': 'small',# langpang = side-near = beside
    'zum': 'bow',        # maizum = face-bow = bow.down
    'tal': 'young',      # bawngtal = cow-young = calf
    'zing': 'morning',   # zingsang = morning-high = early
    'sang': 'high',# zingsang = morning-high
    'dang': 'other',     # lamdang = way-other
    'dik': 'straight',   # midik = person-straight = righteous
    'ham': 'cover',      # puanham = cloth-cover = covering
    'zang': 'side',      # laizang = middle-side = midst
    'man': 'true',       # thuman = word-true = truth
    'tual': 'generation',# puantual = cloth-generation = robe
    'phat': 'praise',    # kiphat = REFL-praise
    'cih': 'say',        # cihnop = say-want = meaning
    'mai': 'face',       # maizum = face-bow, kimaisak = appear
    
    # Sizes/degrees
    'pi': 'big',
    # Note: 'te' can also mean 'small/diminutive' but PL is far more common
    'lian': 'great',
    'nau': 'young',
    
    # Round 175: Medium-frequency atomic glosses
    'u': 'elder.sibling',  # ulianpa = elder-great-man = elder
    'pul': 'tremble',      # pulnat = tremble-hurt = terror
    'nat': 'hurt',         # pulnat = tremble-hurt
    'tot': 'circumcise',   # kitot = REFL-circumcise
    'khuam': 'darkness',   # Also khuam 'pillar' in innkhuam, khuampi, suangkhuam (homophonous)
    'muan': 'trust',       # munmuan = place-trust
    'huai': 'terrible',# muhdahhuai = see-hate-terrible = abomination
    'baan': 'lay',         # paubaan = say-lay = blaspheme
    'sal': 'slave',        # salsuah = slave-become = slavery
    'do': 'fight',         # galdo = war-fight = battle
    'koih': 'put',         # vankoih = sky-put = heaven
    'git': 'hate',         # migit = person-hate
    'suan': 'plant',       # kisuan = REFL-plant = succession
    'ho': 'greet',         # hopih = greet-APPL = counsel
    'zep': 'clothe',       # kizep = REFL-clothe = join
    'phum': 'immerse',     # tuiphum = water-immerse = baptism
    'le': 'and',           # nulepa = mother-and-father
    'mang': 'dream',       # dream/obey (polysemous, see AMBIGUOUS_MORPHEMES)
    'zin': 'travel',       # khualzin = village-travel = pilgrimage
    'pei': 'guide',        # leengpei = chariot-guide = chariot.leader
    'thah': 'slay',        # kithah = REFL-slay = murder
    'kal': 'middle',       # lamkal = way-middle = midway
    'lum': 'warm',         # gamlum = land-warm = south
    'gelh': 'write',       # kigelh = REFL-write = scripture
    'tel': 'know',         # theihtel = know-know = wisdom
    'kuang': 'basin',   # tuikuang = water-box = pool
    'theih': 'know',       # thutheih = word-know = knowledge
    'hau': 'rich',         # mihau = person-rich = rich.one
    'khang': 'generation', # khangnote = generation-young-PL = youth
    'thawh': 'rise',       # thawhkik = rise-again = resurrection
    'ai': 'lot',           # ai san = lot-cast = cast.lots (divination)
    'kong': 'side',        # kongcing = side-pure = faithful
    'cing': 'pure',        # kongcing = side-pure
    'cil': 'thresh',       # ancil = rice-thresh = threshing
    'mu': 'see',           # muvan = see-sky = vision
    
    # Round 176: Additional atomic glosses
    'vai': 'plan',         # vaihawm = plan-counsel = counsel
    'hawm': 'counsel',     # vaihawm = plan-counsel
    'nih': 'two',          # nihvei = two-time = second
    'vei': 'time',         # nihvei = two-time
    'hawl': 'drive',       # hawlkhiat = drive-out = persecution
    'hen': 'tie',          # hencip = tie-tightly, kihen = REFL-tie, henna = tie-NMLZ (bond)
    'paih': 'pour',        # thangpaih = rise-pour = flood
    'duai': 'soft',        # lungduai = heart-soft = compassion
    'khum': 'cover',       # kikhum = REFL-cover = covering
    'dan': 'manner',       # kilamdan = REFL-way-manner = pattern
    'gong': 'alone',       # meigong = female-alone = widow (mei 'female' TB *mei)
    
    # Round 177: Additional atomic glosses (5-9x compounds)
    'kiat': 'release',     # thongkiat = prison-release = deliverance
    'nep': 'soft',         # hehnep = angry-soft = patience
    'lat': 'strong',       # kilat = REFL-strong = strengthen
    'kip': 'firm',         # kipsak = firm-CAUS = confirm
    'bah': 'deaf',         # bilbah = ear-deaf = deaf
    'phu': 'carry',        # phulak = carry-take = burden
    'li': 'four',          # livei = four-time = fourth
    'mong': 'hem',         # puanmong = cloth-hem = garment hem
    'teep': 'fringe',      # puanmongteep = garment-hem-fringe
    'net': 'hungry',       # netniam = hungry-low = hunger
    'niam': 'low',         # netniam = hungry-low
    'ngak': 'wait',        # kingak = REFL-wait = expectation
    'sil': 'wash',         # kisil = REFL-wash = washing
    'hhuai': 'abominate',  # kihhuai = REFL-abominate = abomination
    
    # Round 178: Additional atomic glosses (batch 2)
    'thang': 'famous',     # minthang = name-famous = fame
    'sia': 'evil',         # minsia = name-evil = dishonor (also 'bad/old' in siapa)
    'gilo': 'enemy',       # gilote = enemy-PL (distinct from proper noun Gilo/Giloh)
    'kial': 'hunger',      # gilkial = stomach-hunger = bowels
    'sel': 'quarrel',      # kisel = REFL-quarrel = strife
    'phawk': 'remember',   # kiphawk = REFL-remember = remembrance
    'khih': 'bind',        # kikhih = REFL-bind = binding
    'daih': 'wide',        # gamdaih = land-wide = breadth
    'sawm': 'ten',         # sawmnih = ten-two = twelve
    
    # Round 179: Additional atomic glosses (batch 3)
    'dong': 'collect',     # siahdong = tax-collect = tax collector
    'kia': 'fall',         # lungkia = heart-fall = discourage
    'khawh': 'work',       # lokhawh = field-work = farming
    'keu': 'cluster',      # leenggahkeu = grape-dry-cluster = raisin cluster
    'vui': 'bury',         # kivui = REFL-bury = burial
    'sik': 'turn',         # kisik = REFL-turn = turning
    'huh': 'help',         # kihuh = REFL-help = help
    'hal': 'burn',         # kihal = REFL-burn = burning
    'tawng': 'false',      # lungsimtawng = heart-mind-false = hypocrisy
    
    # Round 180: Additional atomic glosses (batch 4)
    # Note: kholh has TWO homophonous morphemes:
    # - kholh₁ 'INTENS' (intensifier) used with gen-, hilh-, theih-, geel-, bawl-
    # - kholh₂ 'accompany' used with ki- (REFL-accompany = be with)
    # The INTENS meaning is in SUFFIXES dict; 'accompany' applies to ki- compounds only
    'gan': 'cattle',       # gancing = cattle-care = shepherd
    'tun': 'arrive',       # zintun = journey-arrive = destination
    'zak': 'hear',         # zaksak = hear-CAUS = testimony
    'tan': 'judge',        # thutan = word-judge = judgment
    'tawl': 'rest',        # tawldam = rest-well = rest
    'tawi': 'weigh',       # tawikhai = weigh-balance = balance
    'khai': 'balance',     # tawikhai = weigh-balance
    'thuk': 'deep',        # thuthuk = word-deep = deep word
    
    # Round 182: Additional atomic glosses (5-9x compounds)
    'hual': 'wave',        # tuihual = water-wave = flood
    'teek': 'master',      # innteek = house-master = landlord
    'lom': 'bundle',       # buhlom = grain-bundle = sheaf
    'kawi': 'fish',        # sikkawi = hook-fish = fishhook
    'dot': 'ask',          # thudot = word-ask = question
    'mul': 'tip',          # keelmul = heel-tip = goat's hair (contextual)
    
    # Round 183: Additional atomic glosses
    'niim': 'shade',       # singniim = tree-shade = green tree
    'hiang': 'branch',     # singhiang = tree-branch
    'phia': 'bright',      # khuaphia = cloud-bright = brightness
    'taang': 'beautiful',  # vangtaang = glory-beautiful
    'tai': 'bright', # maitai = face-bright = radiant
    'kaih': 'betray',      # kamkaih = word-betray = treachery
    'luah': 'inherit',     # innluahza = house-inherit-right = birthright
    
    # Round 184: Final batch atomic glosses
    'nawl': 'place',       # nawlnung = place-back = edge
    'nung': 'back',        # nawlnung = place-back
    'pam': 'all',          # pammaih = all-face = behalf
    'maih': 'face',        # pammaih = all-face
    'dial': 'belt',        # dialkaih = belt-loosen = girdle
    'len': 'net',          # siklen = tie-net = network
    'buah': 'pour',        # tuibuah = water-pour = libation
    
    # Round 185: Low-frequency atomic glosses
    'nai': 'precious',     # singnai = stone-precious = onyx
    'kul': 'tar',          # kultal = tar-coat = pitch
    'mim': 'thread',       # mimkhau = thread-fine
    'khau': 'fine',        # mimkhau = thread-fine
    'khauh': 'hard',       # lungkhauh = heart-hard = stubborn; khauh pau = speak roughly (37x)
    'bek': 'sleep',        # bekbak = sleep-deep
    'bak': 'deep',         # bekbak = sleep-deep
    'dung': 'length',      # gamdung = land-length
    'mel': 'void',         # limlemel = form-NEG-void
    
    # Round 186: Additional atomic glosses
    'vui': 'ear',     # buhvui = grain-dust = ears of corn
    'ging': 'sound',       # kheging = foot-sound = footsteps
    'ka': 'high',          # lamka = way-high = heights
    'zin': 'bright',       # lungzin = heart-bright = clearness
    'bah': 'ring',         # nakbah = ear-ring = earring
    
    # Round 187: Missing atomic glosses (systematic addition)
    # Common verbs
    'dah': 'put',          # used in compounds
    'it': 'love',          # itna = love-NMLZ
    'lau': 'fear',         # milauna = fear-NMLZ
    'muh': 'see',          # muhdahna = see-put-NMLZ = vision
    'neih': 'have',        # neihsa = have-PERF
    'ngah': 'get',         # ngahsa = get-PERF
    'om': 'be',            # omna = being-NMLZ = place
    'pai': 'go',           # paite = those.going
    'pha': 'reach',        # phate = arrived.ones
    'sih': 'die',          # sihna = death
    
    # Body/physical
    'kam': 'mouth',        # kampi = mouth-big = edge/opening
    'keel': 'foot',        # keelmul = heel
    'sul': 'track',        # sulzui = follow.track
    'gil': 'stomach',      # gilkial = famished
    
    # Descriptive
    'gim': 'heavy',        # gimna = weight
    'hoih': 'good',        # hoihpen = best
    'hak': 'difficult',    # haksat = difficult
    
    # Direction/location
    'khual': 'guest',      # khualzin = traveling
    'kulh': 'surround',    # kulhpi = fortress
    'zung': 'root',        # zungkuang = foundation
    
    # Abstract/other
    'bang': 'like',        # bangzat = how.many
    'buk': 'building',     # biakbuk = worship-building = sanctuary
    'khan': 'time',        # khankuang = time-trunk = ancient
    'min': 'name',         # mintha = good.name
    'puan': 'cloth',       # puanbek = cloth-piece
    'san': 'price',        # sanna = price-NMLZ = redemption
    'sap': 'foreign',      # sapthu = foreign.word
    'thu': 'word',         # thupuan = word-cloth = scroll
    
    # Compounds used atomically in larger compounds
    'galkap': 'soldier',   # galkap = war-person
    'gamla': 'elder',      # gamla = old-person
    'kumpi': 'king',       # kumpi = age-big
    'siangtho': 'holy',    # siangtho = deity-pure
    'siansuah': 'save',    # siansuah = deity-rescue
    'thahat': 'strong',    # thahat = strength-firm
    'neihkhem': 'possess', # neihkhem = have-hold
    'maisak': 'despise',   # maisak = face-discard
    'honkhia': 'spare',    # honkhia = flock-out
    
    # Less common but needed
    'hih': 'this',         # demonstrative
    'kai': 'roast',        # meikai = fire-roast
    'khawm': 'together',   # khawmpi = congregation
    'ling': 'awake',       # lingling = watchful
    'luang': 'flow',       # tuiluang = river
    'luat': 'exceed',      # itluat = beloved
    # 'ngei' removed - conflicts with TAM suffix 'ngei' (EXP); use compound for ngeingei
    'paa': 'father',       # pasal-paa = husband-father
    'pat': 'weave',        # patna = weaving
    'pau': 'speak',        # paupui = counsel
    'pen': 'SUPER',        # hoihpen = best
    'pian': 'born',        # pianna = birth
    'pikal': 'side',       # pikala = one.side
    'siah': 'official',    # siahpa = official-father
    'sian': 'deity',       # siangtho = holy
    'suk': 'push',         # sukkhia = push.out
    'suang': 'stone',      # suangtum = stone-round
    'tawm': 'short',       # tawmciang = soon
    'tawp': 'end',         # tawpna = ending
    'thong': 'chain',      # thongkhang = prison
    'zuih': 'follow',      # sulzuih = track-follow
}

# Morphemes with multiple meanings - used for contextual disambiguation
# in compositional gloss generation
AMBIGUOUS_ATOMIC = {
    'te': {
        'default': 'PL',
        'as_suffix': 'PL',           # noun + te → plural
        'as_modifier': 'small',       # te + noun → diminutive
        'standalone': 'small.one',    # rare
    },
    'pi': {
        'default': 'big',
        'as_suffix': 'big',           # noun + pi → augmentative
        'as_modifier': 'big',         # pi + noun → large X
    },
    'na': {
        'default': 'NMLZ',
        'as_suffix': 'NMLZ',          # verb + na → nominalization
        'as_prefix': '2SG',           # na- + verb → 2nd person
    },
    'sa': {
        'default': 'flesh',
        'as_noun': 'flesh',
        'as_suffix': 'PERF',          # verb + sa → perfective
    },
    'in': {
        'default': 'ERG',
        'as_suffix': 'ERG',           # NP + in → ergative
        'as_noun': 'house',           # inn → house
    },
    'nam': {
        'default': 'smell',           # TB root for smell/fragrance
        'in_namtui': 'smell',         # namtui = perfume
        'in_minam': 'kind',     # minam = nation/people
    },
}


# =============================================================================
# BINARY COMPOUNDS (two-morpheme compounds with internal structure)
# =============================================================================
# Format: compound -> (morpheme1, morpheme2, lexical_gloss)
# These are the building blocks for larger hierarchical compounds.

BINARY_COMPOUNDS = {
    # Liquids/substances: N + tui (water)
    'namtui': ('nam', 'tui', 'perfume'),        # smell-water → perfume/fragrant oil
    'guahtui': ('guah', 'tui', 'rainwater'),    # rain-water → rainwater
    'tuipi': ('tui', 'pi', 'sea'),              # water-big → sea/ocean
    'tuibang': ('tui', 'bang', 'flood'),        # water-spread → flood
    'tuikhuk': ('tui', 'khuk', 'pool'),         # water-bend → pool
    
    # Heart compounds: lung + X
    'lungdam': ('lung', 'dam', 'joy'),          # heart-well → joy/gladness
    'lungtang': ('lung', 'tang', 'courage'),    # heart-stand → courage
    'lungkham': ('lung', 'kham', 'sorrow'),     # heart-forbid → sorrow/trouble
    'lungmit': ('lung', 'mit', 'attention'),    # heart-eye → attention
    'lungkim': ('lung', 'kim', 'peace'),        # heart-complete → contentment
    'lungthim': ('lung', 'thim', 'conscience'), # heart-dark → conscience
    'lungmuang': ('lung', 'muang', 'peace'),    # heart-still → peace of mind
    'lungnop': ('lung', 'nop', 'desire'),       # heart-want → desire/wish
    
    # Sky/heaven compounds: van + X
    'vantung': ('van', 'tung', 'heaven'),       # sky-above → heaven
    'vanlei': ('van', 'lei', 'world'),          # sky-earth → world
    'vanmi': ('van', 'mi', 'angel'),            # sky-person → angel/heavenly being
    'vangliat': ('vang', 'liat', 'glory'),      # glory-power → glory/majesty
    
    # Earth compounds: lei + X
    'leitung': ('lei', 'tung', 'earth'),        # earth-on → earth/world (surface)
    'leilak': ('lei', 'lak', 'dust'),           # earth-particle → dust
    'laitak': ('lai', 'tak', 'exact.midst'),    # midst-true → exactly in midst
    
    # Tree/plant compounds: sing + X
    'singkung': ('sing', 'kung', 'tree'),       # tree-trunk → tree
    'singgah': ('sing', 'gah', 'fruit.tree'),   # tree-fruit → fruit tree
    
    # Vine compounds: X + gui
    'leenggui': ('leeng', 'gui', 'grapevine'),  # grape-vine → grapevine
    
    # Food compounds
    'buhkung': ('buh', 'kung', 'provender'),    # rice-trunk → stored grain
    'ankung': ('an', 'kung', 'provision'),      # food-trunk → provisions
    
    # Juice/liquid compounds: X + zu
    'gahzu': ('gah', 'zu', 'sap'),              # fruit-juice → sap/juice
    'paazu': ('paa', 'zu', 'wine'),             # grape?-juice → wine
    
    # Animal compounds
    'tuupi': ('tuu', 'pi', 'ram'),              # sheep-big → ram
    'bawngpi': ('bawng', 'pi', 'bull'),         # cattle-big → bull
    'ngalpi': ('ngal', 'pi', 'great.wolf'),     # wolf-big → great wolf
    
    # Place compounds: X + inn (house)
    'biakinn': ('biak', 'inn', 'temple'),       # worship-house → temple
    'sihinn': ('sih', 'inn', 'prison'),         # bind-house → prison
    
    # Other productive patterns
    'haksat': ('hak', 'sat', 'difficult'),      # hard-hard → difficult
    'mikhual': ('mi', 'khual', 'stranger'),     # person-village → stranger
    'mihing': ('mi', 'hing', 'mankind'),        # person-creature → mankind
    'saili': ('sai', 'li', 'sling'),            # throw-? → sling
    
    # High-frequency compounds from corpus (freq >= 100)
    'kumpipa': ('kumpi', 'pa', 'king'),         # king-man → king (1910x)
    'biakna': ('biak', 'na', 'worship'),        # worship-NMLZ → worship (1518x)
    'khuapi': ('khua', 'pi', 'city'),           # town-big → city (1225x)
    'lungsim': ('lung', 'sim', 'heart'),        # heart-count → heart/mind (989x)
    'numei': ('nu', 'mei', 'woman'),            # mother-female → woman (763x) - mei 'female' (TB *mei)
    'mawhna': ('mawh', 'na', 'sin'),            # guilty-NMLZ → sin/guilt (735x)
    'minam': ('mi', 'nam', 'nation'),           # person-kind → nation/people (711x)
    'thukham': ('thu', 'kham', 'law'),          # word-forbid → law/commandment (447x)
    'thugen': ('thu', 'gen', 'speech'),         # word-speak → speech/saying (381x)
    'siampi': ('siam', 'pi', 'priest'),         # skilled-big → priest (431x)
    'lampi': ('lam', 'pi', 'road'),             # way-big → road/highway (378x)
    'siatna': ('siat', 'na', 'destruction'),    # spoil-NMLZ → destruction (384x)
    'khialhna': ('khialh', 'na', 'sin'),        # sin-NMLZ → sin/transgression (354x)
    'sihna': ('sih', 'na', 'death'),            # die-NMLZ → death (317x)
    'gamtat': ('gam', 'tat', 'kingdom'),        # land-strike → kingdom (398x)
    'pawlkhat': ('pawl', 'khat', 'some'),       # group-one → some (394x)
    # nasem and nasep are OPAQUE - na- is NOT a prefix (na NMLZ is a suffix!)
    'nasem': ('nasem', None, 'servant'),         # opaque: servant (350x)
    'nasep': ('nasep', None, 'work'),            # opaque: work (573x)
    'kibawl': ('ki', 'bawl', 'be.made'),        # REFL-make → be made (345x)
    'kipia': ('ki', 'pia', 'be.given'),         # REFL-give → be given (339x)
    'kipan': ('ki', 'pan', 'begin'),            # REFL-begin → begin (409x)
    'paikhia': ('pai', 'khia', 'go.out'),       # go-exit → go out (464x)
    'honkhia': ('hon', 'khia', 'go.forth'),     # flock-exit → go forth (357x)
    'leitang': ('lei', 'tang', 'earth'),        # earth-stand → earth/ground (514x)
    
    # Round 172: Additional high-frequency compounds
    'kikhop': ('ki', 'khop', 'assemble'),       # REFL-gather → assemble (292x)
    'nungzui': ('nung', 'zui', 'disciple'),     # back-follow → disciple (274x)
    'galkap': ('gal', 'kap', 'soldier'),        # war-throw → soldier (246x)
    'limtak': ('lim', 'tak', 'sign.true'),      # sign-true → truly/form (240x)
    'hehpih': ('heh', 'pih', 'grace'),          # anger/favor-APPL → grace/mercy (240x)
    'nisuah': ('ni', 'suah', 'birthday'),       # day-birth → birthday (213x)
    'ngaihsut': ('ngaih', 'sut', 'think'),      # think-break → think/deliberate (199x)
    'paikhiat': ('pai', 'khiat', 'go.out'),     # go-emerge → go out (185x)
    'gamlak': ('gam', 'lak', 'land.midst'),     # land-midst → among lands (156x)
    'hoihtak': ('hoih', 'tak', 'good.truly'),   # good-true → truly good (145x)
    'biakpiak': ('biak', 'piak', 'offering'),   # worship-offer → offering (145x)
    
    # Round 173: Additional binary compounds
    'thahat': ('tha', 'hat', 'strength'),       # strength-firm → strong (123x)
    'kilem': ('ki', 'lem', 'prepare'),          # REFL-prepare → preparation (123x)
    'hotkhiat': ('hot', 'khiat', 'save'),       # lead-out → salvation (122x)
    'thunget': ('thu', 'nget', 'pray'),         # word-request → prayer (120x)
    'mipih': ('mi', 'pih', 'companion'),        # person-APPL → companion (112x)
    'mizawng': ('mi', 'zawng', 'everyone'),     # person-all → everyone (109x)
    'tampi': ('tam', 'pi', 'many'),             # many-big → multitude (108x)
    'thukhen': ('thu', 'khen', 'judgment'),     # word-judge → judgment (107x)
    'thuhilh': ('thu', 'hilh', 'teach'),        # word-teach → teaching (96x)
    'khuaneu': ('khua', 'neu', 'village'),      # town-small → village (96x)
    'khuami': ('khua', 'mi', 'townsman'),       # town-person → townsperson (90x)
    'milim': ('mi', 'lim', 'idol'),             # person-image → idol (129x)
    'tuamtuam': ('tuam', 'tuam', 'various'),    # various-REDUP → various (82x)
    # Round 174: Additional binary compounds from full audit
    'lono': ('lo', 'no', 'disobey'),            # not-obey → disobey (125x)
    'nitum': ('ni', 'tum', 'always'),           # day-all → always (104x)
    'langkhat': ('lang', 'khat', 'one.side'),   # side-one → one side (88x)
    'omlai': ('om', 'lai', 'present'),          # exist-midst → those present (88x)
    'gamla': ('gam', 'la', 'wilderness'),       # land-field → wilderness (82x)
    'lamet': ('lam', 'et', 'manner'),           # way-see → manner/example (82x)
    'kiciam': ('ki', 'ciam', 'covenant'),       # REFL-promise → covenant (80x)
    'lasak': ('la', 'sak', 'redeem'),           # take-CAUS → redeem (77x)
    'phattuam': ('phat', 'tuam', 'vow'),        # praise-promise → vow (77x)
    'mualtung': ('mual', 'tung', 'mountaintop'),# mountain-top → summit (67x)
    'mawhsak': ('mawh', 'sak', 'cause.sin'),    # sin-CAUS → cause to sin (67x)
    'innkuan': ('inn', 'kuan', 'household'),    # house-family → household (65x)
    'langpang': ('lang', 'pang', 'beside'),     # side-near → beside (63x)
    'maizum': ('mai', 'zum', 'bow.down'),       # face-bow → bow down (62x)
    'bawngtal': ('bawng', 'tal', 'calf'),       # cow-young → calf (59x)
    'naupang': ('nau', 'pang', 'child'),        # child-small → child (59x)
    'zingsang': ('zing', 'sang', 'early'),      # morning-high → early morning (55x)
    'lamdang': ('lam', 'dang', 'other.way'),    # way-other → other way (54x)
    'kimaisak': ('ki', 'maisak', 'appear'),     # REFL-face.CAUS → appear (52x)
    'midik': ('mi', 'dik', 'righteous'),        # person-straight → righteous (52x)
    'puanham': ('puan', 'ham', 'covering'),     # cloth-cover → covering (45x)
    'laizang': ('lai', 'zang', 'midst'),        # middle-side → in midst (41x)
    'thuman': ('thu', 'man', 'truth'),          # word-true → truth (41x)
    'puantual': ('puan', 'tual', 'robe'),       # cloth-generation → robe (40x)
    
    # Round 175: Medium-frequency binary compounds (20-39x)
    'ulian': ('u', 'lian', 'elder'),            # elder-great → elder (39x)
    'pulnat': ('pul', 'nat', 'terror'),         # fear-pain → terror (39x)
    'kipawl': ('ki', 'pawl', 'fellowship'),     # REFL-associate → fellowship (37x)
    'kitot': ('ki', 'tot', 'circumcision'),     # REFL-cut → circumcision (36x)
    'meivak': ('mei', 'vak', 'lamp'),           # fire-light → lamp (36x)
    'neihsa': ('neih', 'sa', 'possession'),     # have-flesh → possession (35x)
    'pawlpi': ('pawl', 'pi', 'elders'),         # group-big → elders (35x)
    'honpi': ('hon', 'pi', 'multitude'),        # many-big → multitude (33x)
    'kisap': ('ki', 'sap', 'calling'),          # REFL-call → calling (33x)
    'ompih': ('om', 'pih', 'presence'),         # exist-APPL → presence (33x)
    'lauhuai': ('lau', 'huai', 'dread'),        # fear-dread → dread (32x)
    'paubaan': ('pau', 'baan', 'blasphemy'),    # speak-slander → blasphemy (32x)
    'salsuah': ('sal', 'suah', 'slavery'),      # servant-become → slavery (31x)
    'galdo': ('gal', 'do', 'campaign'),          # war-go → military campaign (59x)
    'milian': ('mi', 'lian', 'noble'),          # person-great → noble (31x)
    'kipat': ('ki', 'pat', 'beginning'),        # REFL-begin → beginning (30x)
    'muhdah': ('muh', 'dah', 'abomination'),    # smell-bad → abomination (29x)
    'ancil': ('an', 'cil', 'thresh'),           # food-thresh → threshing (29x)
    'kisiansuah': ('ki', 'siansuah', 'sanctify'), # REFL-holy.become → sanctify (28x)
    'vankoih': ('van', 'koih', 'heaven'),       # sky-put → heaven (26x)
    'migit': ('mi', 'git', 'hatred'),           # person-hate → hatred (25x)
    'kisuan': ('ki', 'suan', 'succession'),     # REFL-follow → succession (25x)
    'hopih': ('ho', 'pih', 'counsel'),          # counsel-APPL → counsel (25x)
    'kizep': ('ki', 'zep', 'joining'),          # REFL-join → joining (24x)
    'tuiphum': ('tui', 'phum', 'baptism'),      # water-immerse → baptism (24x)
    'nule': ('nu', 'le', 'parents'),            # mother-and → parents (23x)
    'cihtak': ('cih', 'tak', 'testimony'),      # say-true → testimony (23x)
    'galkapmang': ('galkap', 'mang', 'captain'),# soldier-chief → captain (23x)
    'khualzin': ('khual', 'zin', 'pilgrimage'), # sojourn-travel → pilgrimage (22x)
    'hoihpen': ('hoih', 'pen', 'best'),         # good-SUPER → best (22x)
    'nipikal': ('ni', 'pikal', 'anniversary'),  # day-fold → anniversary (22x)
    'kithah': ('ki', 'thah', 'murder'),         # REFL-kill → murder (22x)
    'kigamla': ('ki', 'gamla', 'territory'),    # REFL-land.field → territory (22x)
    'kineihkhem': ('ki', 'neihkhem', 'possess.all'), # REFL-have.all → possess all (22x)
    'lopa': ('lo', 'pa', 'farmer'),             # field-man → farmer (21x)
    'kigen': ('ki', 'gen', 'conversation'),     # REFL-speak → conversation (21x)
    'lamkal': ('lam', 'kal', 'midway'),         # way-middle → midway (21x)
    'gamlum': ('gam', 'lum', 'south'),          # land-warm → south (21x)
    'kigelh': ('ki', 'gelh', 'scripture'),      # REFL-write → scripture (21x)
    'theihtel': ('theih', 'tel', 'wisdom'),     # know-help → wisdom (21x)
    'thutheih': ('thu', 'theih', 'knowledge'),  # word-know → knowledge (21x)
    'mihau': ('mi', 'hau', 'rich.one'),         # person-rich → rich one (21x)
    'khangno': ('khang', 'no', 'youth'),        # generation-young → youth (20x)
    'thahatsak': ('thahat', 'sak', 'strengthen'), # strong-CAUS → strengthen (20x)
    'kihonkhia': ('ki', 'honkhia', 'escape'),   # REFL-go.forth → escape (20x)
    'thawhkik': ('thawh', 'kik', 'resurrection'), # rise-again → resurrection (20x)
    
    # Round 176: 10-19x frequency binary compounds
    'vaihawm': ('vai', 'hawm', 'counsel'),       # plan-counsel → counsel (19x)
    'lungmuan': ('lung', 'muan', 'confidence'),  # heart-trust → confidence (18x)
    'minphat': ('min', 'phat', 'fame'),          # name-praise → fame (18x)
    'bawnghon': ('bawng', 'hon', 'herd'),        # cattle-flock → herd (18x)
    'hingkik': ('hing', 'kik', 'resurrect'),     # alive-again → resurrect (18x)
    'nihvei': ('nih', 'vei', 'second'),          # two-time → second (17x)
    'khialhsak': ('khialh', 'sak', 'trespass'),  # err-CAUS → trespass (17x)
    'hawlkhiat': ('hawl', 'khiat', 'persecute'), # drive-out → persecution (17x)
    'thukim': ('thu', 'kim', 'covenant'),        # word-keep → covenant (15x)
    'thangpaih': ('thang', 'paih', 'pour.out'),     # rise-pour → pour out (wrath); thangpaihna = fury/indignation
    'lungduai': ('lung', 'duai', 'compassion'),  # heart-soft → compassion (15x)
    'huaiham': ('huai', 'ham', 'terror'),        # dread-full → terror (15x)
    'galsim': ('gal', 'sim', 'number'),          # enemy-count → number (15x)
    'hamphat': ('ham', 'phat', 'glory'),         # full-praise → glory (16x)
    'kikhum': ('ki', 'khum', 'covering'),        # REFL-cover → covering (14x)
    'kulhkong': ('kulh', 'kong', 'gate'),        # wall-road → gate (14x)
    'meigong': ('mei', 'gong', 'widow'),         # female-alone → widow (14x) - mei 'female' (TB *mei)
    
    # Round 177: 5-9x frequency binary compounds
    'siansuah': ('sian', 'suah', 'sanctify'),    # holy-become → sanctify (9x)
    'thongkiat': ('thong', 'kiat', 'deliver'),   # prison-release → deliver (8x)
    'lungdam': ('lung', 'dam', 'joy'),           # heart-heal → joy (inner compounds)
    'hehnep': ('heh', 'nep', 'patience'),        # angry-soft → patience (9x)
    'kilat': ('ki', 'lat', 'strengthen'),        # REFL-strong → strengthen (9x)
    'kipsak': ('kip', 'sak', 'confirm'),         # firm-CAUS → confirm (9x)
    'bilbah': ('bil', 'bah', 'earring'),         # ear-ring → earring (11x, NOT deaf!)
    'suanghawm': ('suang', 'hawm', 'cave'),       # rock-hollow → cave (12x)
    'phulak': ('phu', 'lak', 'burden'),          # carry-take → burden (9x)
    'langpan': ('lang', 'pan', 'advocate'),      # side-plead → advocate (9x)
    'laigelh': ('lai', 'gelh', 'write'),         # paper-write → writing (8x)
    'livei': ('li', 'vei', 'fourth'),            # four-time → fourth (8x)
    'khangsim': ('khang', 'sim', 'genealogy'),   # generation-count → genealogy (8x)
    'thuman': ('thu', 'man', 'true.word'),       # word-true → true word (9x)
    'thutak': ('thu', 'tak', 'truth'),           # word-true → truth (8x)
    'thuciam': ('thu', 'ciam', 'promise'),       # word-promise → promise (8x)
    'gamdang': ('gam', 'dang', 'other.land'),    # land-other → other land (9x)
    'innkhum': ('inn', 'khum', 'tent.cover'),    # house-cover → tent covering (9x)
    'sintuam': ('sin', 'tuam', 'liver.lobe'),    # liver-lobe → liver lobe (8x)
    'puanmong': ('puan', 'mong', 'garment.hem'), # cloth-hem → garment hem (8x)
    'netniam': ('net', 'niam', 'hunger'),        # hunger-lowly → hunger (8x)
    'kingak': ('ki', 'ngak', 'expect'),          # REFL-wait → expectation (8x)
    'kikoih': ('ki', 'koih', 'place'),           # REFL-put → placement (8x)
    'kisil': ('ki', 'sil', 'wash'),              # REFL-wash → washing (8x)
    'kicih': ('ki', 'cih', 'say'),               # REFL-say → saying (8x)
    
    # Round 178: More 5-9x frequency binary compounds (batch 2)
    'minthang': ('min', 'thang', 'fame'),         # name-famous → fame (7x)
    'minsia': ('min', 'sia', 'dishonor'),         # name-evil → dishonor (7x)
    'meivak': ('mei', 'vak', 'lamplight'),        # fire-light → lamplight (7x)
    'maisak': ('mai', 'sak', 'appearance'),       # face-cause → appearance (7x)
    'gilkial': ('gil', 'kial', 'bowels'),         # stomach-turn → bowels (7x)
    'kisel': ('ki', 'sel', 'strife'),             # REFL-quarrel → strife (7x)
    'kiphawk': ('ki', 'phawk', 'remember'),       # REFL-remember → remembrance (7x)
    'kikhih': ('ki', 'khih', 'bind'),             # REFL-bind → binding (7x)
    'kiho': ('ki', 'ho', 'call'),                 # REFL-call → calling (7x)
    'gentheih': ('gen', 'theih', 'eloquence'),    # speak-know → eloquence (7x)
    'gamdaih': ('gam', 'daih', 'breadth'),        # land-wide → breadth (7x)
    'hamsiat': ('ham', 'siat', 'reproach'),       # cover-spoil → reproach (7x)
    'khuakulh': ('khua', 'kulh', 'fortress'),     # town-wall → fortress (7x)
    'innkuan': ('inn', 'kuan', 'household'),      # house-family → household (7x)
    'khangham': ('khang', 'ham', 'ancestor'),     # generation-old → ancestor (7x)
    'sawmnih': ('sawm', 'nih', 'twelve'),         # ten-two → twelve (7x)
    
    # Round 179: More 5-9x frequency binary compounds (batch 3)
    'siahdong': ('siah', 'dong', 'tax.collect'),  # tax-collect → tax collector (6x)
    'lungkia': ('lung', 'kia', 'discourage'),     # heart-fall → discourage (6x)
    'lungsim': ('lung', 'sim', 'mind'),           # heart-think → mind (6x)
    'mulkiat': ('mul', 'kiat', 'shave'),          # hair-cut → shave (6x)
    'lokhawh': ('lo', 'khawh', 'farm'),           # field-work → farm (6x)
    'leenggah': ('leeng', 'gah', 'raisin'),       # grape-dry → raisin (6x)
    'manphat': ('man', 'phat', 'worthy'),         # price-worthy → worthy (6x)
    'kivui': ('ki', 'vui', 'bury'),               # REFL-bury → burial (6x)
    'kisik': ('ki', 'sik', 'turn'),               # REFL-turn → turning (6x)
    'kisat': ('ki', 'sat', 'strike'),             # REFL-strike → striking (6x)
    'kihuh': ('ki', 'huh', 'help'),               # REFL-help → help (6x)
    'kihal': ('ki', 'hal', 'burn'),               # REFL-burn → burning (6x)
    'sawmli': ('sawm', 'li', 'forty'),            # ten-four → forty (6x)
    
    # Round 180: More 5-9x frequency binary compounds (batch 4)
    'genkholh': ('gen', 'kholh', 'prophesy'),      # speak-INTENS → prophesy/declare (6x)
    'gancing': ('gan', 'cing', 'shepherd'),       # cattle-care → shepherd (6x)
    'galdaih': ('gal', 'daih', 'warfare'),        # enemy-able → warfare (6x)
    'zintun': ('zin', 'tun', 'arrive'),           # journey-arrive → destination (5x)
    'zaksak': ('zak', 'sak', 'testify'),          # hear-CAUS → testimony (5x)
    'thumsak': ('thum', 'sak', 'intercede'),      # entreat-CAUS → intercede/pray.for (19x)
    'thutel': ('thu', 'tel', 'fulfill'),          # word-fulfill → fulfillment (5x)
    'thutan': ('thu', 'tan', 'judge'),            # word-judge → judgment (5x)
    'tawldam': ('tawl', 'dam', 'rest'),           # rest-well → rest (5x)
    'tawikhai': ('tawi', 'khai', 'balance'),      # weigh-balance → balance (5x)
    'tatsiat': ('tat', 'siat', 'destroy'),        # strike-spoil → destruction (5x)
    'tatkhialh': ('tat', 'khialh', 'transgress'), # strike-err → transgression (5x)
    'piankhiat': ('pian', 'khiat', 'birthright'), # birth-leave → birthright (5x)
    'tuinak': ('tui', 'nak', 'spring'),           # water-nose → spring (5x)
    'thuthuk': ('thu', 'thuk', 'deep.word'),      # word-deep → deep word (5x)
    
    # Round 182: More 5-9x lexicalized compounds
    'tuihual': ('tui', 'hual', 'flood'),          # water-wave → flood/depths (9x)
    'khuttum': ('khut', 'tum', 'fist'),           # hand-bunch → fist (9x)
    'bukkong': ('buk', 'kong', 'doorway'),        # shelter-road → doorway (9x)
    'zungbuh': ('zung', 'buh', 'ring'),           # root-? → ring/jewelry (9x)
    'innteek': ('inn', 'teek', 'landlord'),       # house-master → household master (9x)
    'buhlom': ('buh', 'lom', 'sheaf'),            # grain-bundle → sheaf (9x)
    'lingkung': ('ling', 'kung', 'thorns'),       # thorn-round → thorns/briers (9x)
    'sikkawi': ('sik', 'kawi', 'fishhook'),       # hook-fish → fishhook (9x)
    'nitawp': ('ni', 'tawp', 'last.day'),         # day-end → last day (9x)
    'limlang': ('lim', 'lang', 'crystal'),        # image-reflect → crystal (8x)
    'thudot': ('thu', 'dot', 'question'),         # word-ask → question/demand (8x)
    'mundang': ('mun', 'dang', 'elsewhere'),      # place-other → another place (8x)
    'cingnu': ('cing', 'nu', 'nurse'),            # care-mother → nurse (8x)
    'mangpha': ('mang', 'pha', 'farewell'),       # chief-good → farewell (8x)
    'tawmvei': ('tawm', 'vei', 'moment'),         # little-time → short time (8x)
    'keelmul': ('keel', 'mul', 'goathair'),       # heel-tip → goat's hair (8x)
    
    # Round 183: More N+N lexicalized compounds (5-9x)
    'kampi': ('kam', 'pi', 'mouth'),              # word-big → mouth (9x)
    'luzang': ('lu', 'zang', 'crown'),            # head-crown → top of head (8x)
    'singniim': ('sing', 'niim', 'green.tree'),   # tree-shade → green tree (8x)
    'singluang': ('sing', 'luang', 'beam'),       # tree-log → wooden beam (8x)
    'singhiang': ('sing', 'hiang', 'branch'),     # tree-branch → branch (8x)
    'khuaphia': ('khua', 'phia', 'brightness'),   # cloud-bright → brightness (8x)
    'puankhai': ('puan', 'khai', 'curtain'),      # cloth-hang → hanging/curtain (9x)
    'vangtaang': ('vang', 'taang', 'glory'),      # glory-beautiful → glory (7x)
    'maitai': ('mai', 'tai', 'radiant'),          # face-bright → radiant/joyful (7x)
    'kamciam': ('kam', 'ciam', 'vow'),            # word-promise → vow (6x)
    'kamkaih': ('kam', 'kaih', 'treachery'),      # word-betray → treachery (6x)
    
    # Round 184: Final batch of 5-9x lexicalized compounds
    'ngahsa': ('ngah', 'sa', 'acquire'),          # get-flesh → acquire/gotten (9x)
    'nawlnung': ('nawl', 'nung', 'edge'),         # place-back → edge/selvedge (9x)
    'pammaih': ('pam', 'maih', 'behalf'),         # all-face → on behalf of (9x)
    'tatsat': ('tat', 'sat', 'continual'),        # cut-regular → continual/daily (9x)
    'diktat': ('dik', 'tat', 'entrance'),         # straight-cut → entrance (9x)
    'itluat': ('it', 'luat', 'beloved'),          # love-exceed → beloved (9x)
    'dialkaih': ('dial', 'kaih', 'girdle'),       # belt-loosen → girdle/loincloth (9x)
    'omngei': ('om', 'ngei', 'know'),             # be-know → recognize (9x)
    'gimnam': ('gim', 'nam', 'savour'),           # suffer-smell → sweet savour (8x)
    'sulzuih': ('sul', 'zuih', 'pursue'),         # track-follow → pursue/overcome (8x)
    'siklen': ('sik', 'len', 'network'),          # tie-net → network/grating (8x)
    'tuibuah': ('tui', 'buah', 'libation'),       # water-pour → drink offering (8x)
    'khutsiam': ('khut', 'siam', 'craft'),        # hand-skill → craftsmanship (8x)
    'tawisuang': ('tawi', 'suang', 'weights'),    # weigh-stone → scale weights (8x)
    
    # Round 185: Low-frequency (1-4x) lexicalized compounds
    'singnai': ('sing', 'nai', 'bdellium'),       # tree-precious → bdellium/tree resin (4x)
    'kultal': ('kul', 'tal', 'pitch'),            # tar-coat → pitch (4x)
    'khansung': ('khan', 'sung', 'lifetime'),     # generation-inside → lifetime/days (4x)
    'mimkhau': ('mim', 'khau', 'thread'),         # thread-fine → thread (4x)
    'bekbak': ('bek', 'bak', 'deep.sleep'),       # sleep-deep → deep sleep (2x)
    'gamdung': ('gam', 'dung', 'length'),         # land-length → length of land (1x)
    'gamvai': ('gam', 'vai', 'breadth'),          # land-breadth → breadth of land (1x)
    
    # Round 186: More low-frequency (1-4x) lexicalized compounds
    'buhvui': ('buh', 'vui', 'ears.of.corn'),     # grain-dust → ears of corn (4x)
    'kamsia': ('kam', 'sia', 'boast'),            # mouth-evil → boastful words (4x)
    'kheging': ('khe', 'ging', 'footsteps'),      # foot-sound → sound of going (4x)
    'khuanawl': ('khua', 'nawl', 'outskirts'),    # town-place → outskirts (4x)
    'lampai': ('lam', 'pai', 'proceed'),          # way-go → proceed/go on (4x)
    'lamka': ('lam', 'ka', 'heights'),            # way-high → high places (4x)
    'lungnem': ('lung', 'nem', 'meek'),           # heart-soft → meekness (4x)
    'lungzin': ('lung', 'zin', 'brightness'),     # heart-bright → clearness/shine (4x)
    'nakbah': ('nak', 'bah', 'earring'),          # ear-ring → earring (4x)
    'namdang': ('nam', 'dang', 'diverse'),        # kind-different → diverse kind (4x)
    'puanbek': ('puan', 'bek', 'piece.of.cloth'), # cloth-piece → piece of cloth (4x)
    
    # Round 188: More 1-4x lexicalized compounds
    'ankuang': ('an', 'kuang', 'bosom'),          # breast-bosom → bosom (Prov 19:24) (4x)
    'saltang': ('sal', 'tang', 'captive'),        # slave-stand → captive (Jer 29:4) (4x)
    'sangpi': ('sang', 'pi', 'high.wall'),        # high-big → high wall (Deut 3:5) (4x)
    'sungnu': ('sung', 'nu', 'mother.in.law'),    # inside-woman → mother-in-law (Deut 27:23) (4x)
    'teekpa': ('teek', 'pa', 'father.in.law'),    # master-man → father-in-law (Gen 38:13) (4x)
    # lungno removed - opaque lexeme meaning 'worm' (5x), not lung+no compound
    'maisiat': ('mai', 'siat', 'oppose'),         # face-spoil → set face against (Lev 17:10) (4x)
    
    # Body part compounds (3x)
    'lukham': ('lu', 'kham', 'pillow'),           # head-cover → pillow/bolster (1Sam 19:13) (3x)
    'lungham': ('lung', 'ham', 'wrath'),          # heart-anger → wrath/indignation (Deut 29:28) (3x)
    'mitkhu': ('mit', 'khu', 'eyebrow'),          # eye-smoke → eyebrow (Lev 14:9) (3x)
    
    # Nature compounds (2-3x)
    'singzung': ('sing', 'zung', 'root'),         # tree-root → root/trunk (Job 30:3) (2x)
    'leipi': ('lei', 'pi', 'earthquake'),         # earth-big → earthquake (Joel 2:10) (3x)
    'khasim': ('kha', 'sim', 'new.moon'),         # moon-sweet → new moon (Num 29:6) (3x)
    
    # Round 193m: Long stems analyzed as binary compounds
    'lamhilh': ('lam', 'hilh', 'guide'),          # way-teach → guide
    'tuikulh': ('tui', 'kulh', 'island'),         # water-surround → island
    'taanggam': ('taang', 'gam', 'suburb'),       # beautiful-land → suburb
    # sanggam removed - opaque lexeme meaning 'brother', not sang+gam
    'innkhuam': ('inn', 'khuam', 'house-pillar'),  # khuam 'pillar', not 'darkness'
    'suangkhuam': ('suang', 'khuam', 'stone-pillar'),  # suang 'stone' + khuam 'pillar'
    'khuampi': ('khuam', 'pi', 'pillar-great'),    # khuam 'pillar' + pi 'great' → great pillar
    
    # Round 193m continued: More long stems as binary compounds
    'banbulh': ('ban', 'bulh', 'bracelet'),       # arm-bind → bracelet
    'galkah': ('gal', 'kah', 'warfare'),          # war-fight → warfare
    'galpan': ('gal', 'pan', 'fortress'),         # war-side → fortress
    'bawngno': ('bawng', 'no', 'calf'),           # cattle-young → calf
}


# =============================================================================
# TERNARY+ COMPOUNDS (three or more morphemes with hierarchical structure)
# =============================================================================
# Format: compound -> {
#     'morphemes': ['m1', 'm2', 'm3'],
#     'structure': 'm1-(m2-m3)' or '(m1-m2)-m3',
#     'lexical': 'holistic meaning',
#     'head': 'right' or 'left'
# }
# 
# head='right' means N (N N): modifier + [head compound]
# head='left' means (N N) N: [head compound] + modifier

TERNARY_COMPOUNDS = {
    # sing + namtui type: tree + (smell-water) = tree-perfume = spices
    'singnamtui': {
        'morphemes': ['sing', 'nam', 'tui'],
        'structure': 'sing-(nam-tui)',
        'lexical': 'spices',
        'head': 'right',
    },
    # pak + namtui type: wine + (smell-water) = wine-perfume
    'paknamtui': {
        'morphemes': ['pak', 'nam', 'tui'],
        'structure': 'pak-(nam-tui)',
        'lexical': 'ointment',
        'head': 'right',
    },
    # leeng + gahzu type: grape + (fruit-juice) = grape juice
    'leenggahzu': {
        'morphemes': ['leeng', 'gah', 'zu'],
        'structure': 'leeng-(gah-zu)',
        'lexical': 'grape.juice',
        'head': 'right',
    },
    # biakinn + lam type: (worship-house) + direction = temple direction
    'biakinnlam': {
        'morphemes': ['biak', 'inn', 'lam'],
        'structure': '(biak-inn)-lam',
        'lexical': 'temple.side',
        'head': 'left',
    },
    # lung + damna type: heart + (well-NMLZ) = gladness
    'lungdamna': {
        'morphemes': ['lung', 'dam', 'na'],
        'structure': 'lung-(dam-na)',
        'lexical': 'gladness',
        'head': 'right',
    },
    # Additional complex compounds from corpus
    # kilungkim: ki + lungkim = REFL + (heart-complete) = peace/contentment
    'kilungkim': {
        'morphemes': ['ki', 'lung', 'kim'],
        'structure': 'ki-(lung-kim)',
        'lexical': 'contentment',
        'head': 'right',
    },
    # sailungtang: saili + lungtang is NOT the structure
    # Actually: sai-lung-tang = sling-stone (lit. throw?-stone-?)
    # From context: slingstone
    'sailungtang': {
        'morphemes': ['sai', 'lung', 'tang'],
        'structure': '(sai-lung)-tang',
        'lexical': 'slingstone',
        'head': 'left',
    },
    # lung-X + te (plural) patterns - very common
    'lungdamte': {
        'morphemes': ['lung', 'dam', 'te'],
        'structure': '(lung-dam)-te',
        'lexical': 'joyful.ones',
        'head': 'left',
    },
    'lungkhamte': {
        'morphemes': ['lung', 'kham', 'te'],
        'structure': '(lung-kham)-te',
        'lexical': 'sorrowful.ones',
        'head': 'left',
    },
    'lungkimte': {
        'morphemes': ['lung', 'kim', 'te'],
        'structure': '(lung-kim)-te',
        'lexical': 'peaceful.ones',
        'head': 'left',
    },
    # lung-X + sak (causative) patterns
    'lungkhamsak': {
        'morphemes': ['lung', 'kham', 'sak'],
        'structure': '(lung-kham)-sak',
        'lexical': 'cause.sorrow',
        'head': 'left',
    },
    'lungmuangsak': {
        'morphemes': ['lung', 'muang', 'sak'],
        'structure': '(lung-muang)-sak',
        'lexical': 'comfort',
        'head': 'left',
    },
    'lungnopsak': {
        'morphemes': ['lung', 'nop', 'sak'],
        'structure': '(lung-nop)-sak',
        'lexical': 'tempt',
        'head': 'left',
    },
    # lung-nop + na (nominalization)
    'lungnopna': {
        'morphemes': ['lung', 'nop', 'na'],
        'structure': '(lung-nop)-na',
        'lexical': 'desire',
        'head': 'left',
    },
    # leeng-gui + pi (augmentative)
    'leengguipi': {
        'morphemes': ['leeng', 'gui', 'pi'],
        'structure': '(leeng-gui)-pi',
        'lexical': 'great.vine',
        'head': 'left',
    },
    # biak-inn + te (plural)
    'biakinnte': {
        'morphemes': ['biak', 'inn', 'te'],
        'structure': '(biak-inn)-te',
        'lexical': 'temples',
        'head': 'left',
    },
    # High-frequency ternary compounds from corpus
    # [compound]-te (plural) patterns
    # nasemte removed - handled in COMPOUND_WORDS as opaque nasem + -te
    'minamte': {
        'morphemes': ['mi', 'nam', 'te'],
        'structure': '(mi-nam)-te',
        'lexical': 'nations',
        'head': 'left',
    },
    'siampite': {
        'morphemes': ['siam', 'pi', 'te'],
        'structure': '(siam-pi)-te',
        'lexical': 'priests',
        'head': 'left',
    },
    'khuapite': {
        'morphemes': ['khua', 'pi', 'te'],
        'structure': '(khua-pi)-te',
        'lexical': 'cities',
        'head': 'left',
    },
    'mihingte': {
        'morphemes': ['mi', 'hing', 'te'],
        'structure': '(mi-hing)-te',
        'lexical': 'mankind',
        'head': 'left',
    },
    'numeite': {
        'morphemes': ['nu', 'mei', 'te'],
        'structure': '(nu-mei)-te',
        'lexical': 'women',
        'head': 'left',
    },
    'thugente': {
        'morphemes': ['thu', 'gen', 'te'],
        'structure': '(thu-gen)-te',
        'lexical': 'sayings',
        'head': 'left',
    },
    'biaknate': {
        'morphemes': ['biak', 'na', 'te'],
        'structure': '(biak-na)-te',
        'lexical': 'worships',
        'head': 'left',
    },
    'pawlkhatte': {
        'morphemes': ['pawl', 'khat', 'te'],
        'structure': '(pawl-khat)-te',
        'lexical': 'some',
        'head': 'left',
    },
    'thukhamte': {
        'morphemes': ['thu', 'kham', 'te'],
        'structure': '(thu-kham)-te',
        'lexical': 'laws',
        'head': 'left',
    },
    'mawhnate': {
        'morphemes': ['mawh', 'na', 'te'],
        'structure': '(mawh-na)-te',
        'lexical': 'sins',
        'head': 'left',
    },
    'khialhnate': {
        'morphemes': ['khialh', 'na', 'te'],
        'structure': '(khialh-na)-te',
        'lexical': 'transgressions',
        'head': 'left',
    },
    'vantungte': {
        'morphemes': ['van', 'tung', 'te'],
        'structure': '(van-tung)-te',
        'lexical': 'heavens',
        'head': 'left',
    },
    'singkungte': {
        'morphemes': ['sing', 'kung', 'te'],
        'structure': '(sing-kung)-te',
        'lexical': 'trees',
        'head': 'left',
    },
    'leengguite': {
        'morphemes': ['leeng', 'gui', 'te'],
        'structure': '(leeng-gui)-te',
        'lexical': 'vineyards',
        'head': 'left',
    },
    'lampite': {
        'morphemes': ['lam', 'pi', 'te'],
        'structure': '(lam-pi)-te',
        'lexical': 'roads',
        'head': 'left',
    },
    # nasepte removed - handled in COMPOUND_WORDS as opaque nasep + -te
    # [compound]-na (nominalization) patterns  
    'gamtatna': {
        'morphemes': ['gam', 'tat', 'na'],
        'structure': '(gam-tat)-na',
        'lexical': 'kingdom',
        'head': 'left',
    },
    # nasepna removed - handled in COMPOUND_WORDS as opaque nasep + -na
    'lungkhamna': {
        'morphemes': ['lung', 'kham', 'na'],
        'structure': '(lung-kham)-na',
        'lexical': 'sorrow',
        'head': 'left',
    },
    'thugenna': {
        'morphemes': ['thu', 'gen', 'na'],
        'structure': '(thu-gen)-na',
        'lexical': 'saying',
        'head': 'left',
    },
    'haksatna': {
        'morphemes': ['hak', 'sat', 'na'],
        'structure': '(hak-sat)-na',
        'lexical': 'difficulty',
        'head': 'left',
    },
    'lungkimna': {
        'morphemes': ['lung', 'kim', 'na'],
        'structure': '(lung-kim)-na',
        'lexical': 'peace',
        'head': 'left',
    },
    'kibawlna': {
        'morphemes': ['ki', 'bawl', 'na'],
        'structure': '(ki-bawl)-na',
        'lexical': 'creation',
        'head': 'left',
    },
    # [compound]-pa (agent) patterns
    'nasempa': {
        'morphemes': ['na', 'sem', 'pa'],
        'structure': '(na-sem)-pa',
        'lexical': 'servant',
        'head': 'left',
    },
    'siampipa': {
        'morphemes': ['siam', 'pi', 'pa'],
        'structure': '(siam-pi)-pa',
        'lexical': 'priest',
        'head': 'left',
    },
    'nasemnu': {
        'morphemes': ['na', 'sem', 'nu'],
        'structure': '(na-sem)-nu',
        'lexical': 'maidservant',
        'head': 'left',
    },
    # [compound]-mi (person) patterns
    'vantungmi': {
        'morphemes': ['van', 'tung', 'mi'],
        'structure': '(van-tung)-mi',
        'lexical': 'angel',
        'head': 'left',
    },
    # [compound]-sak (causative) patterns
    'lungdamsak': {
        'morphemes': ['lung', 'dam', 'sak'],
        'structure': '(lung-dam)-sak',
        'lexical': 'make.glad',
        'head': 'left',
    },
    'lungkimsak': {
        'morphemes': ['lung', 'kim', 'sak'],
        'structure': '(lung-kim)-sak',
        'lexical': 'satisfy',
        'head': 'left',
    },
    'paikhiasak': {
        'morphemes': ['pai', 'khia', 'sak'],
        'structure': '(pai-khia)-sak',
        'lexical': 'send.out',
        'head': 'left',
    },
    # [compound]-in (ergative) patterns
    'kipanin': {
        'morphemes': ['ki', 'pan', 'in'],
        'structure': '(ki-pan)-in',
        'lexical': 'from',
        'head': 'left',
    },
    'lungdamin': {
        'morphemes': ['lung', 'dam', 'in'],
        'structure': '(lung-dam)-in',
        'lexical': 'gladly',
        'head': 'left',
    },
    'lungmuangin': {
        'morphemes': ['lung', 'muang', 'in'],
        'structure': '(lung-muang)-in',
        'lexical': 'peacefully',
        'head': 'left',
    },
    # [compound]-pi (augmentative) patterns
    'biakinnpi': {
        'morphemes': ['biak', 'inn', 'pi'],
        'structure': '(biak-inn)-pi',
        'lexical': 'great.temple',
        'head': 'left',
    },
    # [compound]-sung (inside) patterns
    'biakinnsung': {
        'morphemes': ['biak', 'inn', 'sung'],
        'structure': '(biak-inn)-sung',
        'lexical': 'in.temple',
        'head': 'left',
    },
    # [modifier]-siatna (destruction) patterns - right-headed
    'samsiatna': {
        'morphemes': ['sam', 'siat', 'na'],
        'structure': 'sam-(siat-na)',
        'lexical': 'utter.destruction',
        'head': 'right',
    },
    'bawlsiatna': {
        'morphemes': ['bawl', 'siat', 'na'],
        'structure': 'bawl-(siat-na)',
        'lexical': 'complete.destruction',
        'head': 'right',
    },
    'suksiatna': {
        'morphemes': ['suk', 'siat', 'na'],
        'structure': 'suk-(siat-na)',
        'lexical': 'destruction',
        'head': 'right',
    },
    'simmawhna': {
        'morphemes': ['sim', 'mawh', 'na'],
        'structure': 'sim-(mawh-na)',
        'lexical': 'guilt',
        'head': 'right',
    },
    # Round 172: Additional high-frequency ternary compounds
    'vangliatna': {
        'morphemes': ['vang', 'liat', 'na'],
        'structure': '(vang-liat)-na',
        'lexical': 'glory',
        'head': 'left',
    },
    'kikhopna': {
        'morphemes': ['ki', 'khop', 'na'],
        'structure': '(ki-khop)-na',
        'lexical': 'assembly',
        'head': 'left',
    },
    'nungzuite': {
        'morphemes': ['nung', 'zui', 'te'],
        'structure': '(nung-zui)-te',
        'lexical': 'disciples',
        'head': 'left',
    },
    'galkapte': {
        'morphemes': ['gal', 'kap', 'te'],
        'structure': '(gal-kap)-te',
        'lexical': 'soldiers',
        'head': 'left',
    },
    'hehpihna': {
        'morphemes': ['heh', 'pih', 'na'],
        'structure': '(heh-pih)-na',
        'lexical': 'grace',
        'head': 'left',
    },
    'ngaihsutna': {
        'morphemes': ['ngaih', 'sut', 'na'],
        'structure': '(ngaih-sut)-na',
        'lexical': 'thought',
        'head': 'left',
    },
    'biakpiakna': {
        'morphemes': ['biak', 'piak', 'na'],
        'structure': '(biak-piak)-na',
        'lexical': 'offering',
        'head': 'left',
    },
    'nisuahna': {
        'morphemes': ['ni', 'suah', 'na'],
        'structure': '(ni-suah)-na',
        'lexical': 'birthday',
        'head': 'left',
    },
    # X + tak + in patterns (truly/exactly + ERG)
    'laitakin': {
        'morphemes': ['lai', 'tak', 'in'],
        'structure': '(lai-tak)-in',
        'lexical': 'exactly.in.midst',
        'head': 'left',
    },
    'nakpitakin': {
        'morphemes': ['nak', 'pi', 'tak', 'in'],  # Actually 4 morphemes
        'structure': '((nak-pi)-tak)-in',
        'lexical': 'strongly',
        'head': 'left',
    },
    'limtakin': {
        'morphemes': ['lim', 'tak', 'in'],
        'structure': '(lim-tak)-in',
        'lexical': 'truly',
        'head': 'left',
    },
    'hoihtakin': {
        'morphemes': ['hoih', 'tak', 'in'],
        'structure': '(hoih-tak)-in',
        'lexical': 'well',
        'head': 'left',
    },
    # khatlekhat pattern (one-and-one = each)
    'khatlekhat': {
        'morphemes': ['khat', 'le', 'khat'],
        'structure': 'khat-le-khat',
        'lexical': 'each',
        'head': 'none',  # reduplication pattern
    },
    # paikhiatpih pattern (go-out-APPL)
    'paikhiatpih': {
        'morphemes': ['pai', 'khiat', 'pih'],
        'structure': '(pai-khiat)-pih',
        'lexical': 'send.forth',
        'head': 'left',
    },
    'gamlakah': {
        'morphemes': ['gam', 'lak', 'ah'],
        'structure': '(gam-lak)-ah',
        'lexical': 'among.lands',
        'head': 'left',
    },
    # Round 173: High-frequency ternary compounds (freq >= 80)
    'milimte': {
        'morphemes': ['mi', 'lim', 'te'],
        'structure': '(mi-lim)-te',
        'lexical': 'idols',
        'head': 'left',
    },
    'thahatna': {
        'morphemes': ['tha', 'hat', 'na'],
        'structure': '(tha-hat)-na',
        'lexical': 'strength',
        'head': 'left',
    },
    'kilemna': {
        'morphemes': ['ki', 'lem', 'na'],
        'structure': '(ki-lem)-na',
        'lexical': 'preparation',
        'head': 'left',
    },
    'hotkhiatna': {
        'morphemes': ['hot', 'khiat', 'na'],
        'structure': '(hot-khiat)-na',
        'lexical': 'salvation',
        'head': 'left',
    },
    'thungetna': {
        'morphemes': ['thu', 'nget', 'na'],
        'structure': '(thu-nget)-na',
        'lexical': 'prayer',
        'head': 'left',
    },
    'mipihte': {
        'morphemes': ['mi', 'pih', 'te'],
        'structure': '(mi-pih)-te',
        'lexical': 'companions',
        'head': 'left',
    },
    'mizawngte': {
        'morphemes': ['mi', 'zawng', 'te'],
        'structure': '(mi-zawng)-te',
        'lexical': 'all.people',
        'head': 'left',
    },
    'tampite': {
        'morphemes': ['tam', 'pi', 'te'],
        'structure': '(tam-pi)-te',
        'lexical': 'multitude',
        'head': 'left',
    },
    'thukhenna': {
        'morphemes': ['thu', 'khen', 'na'],
        'structure': '(thu-khen)-na',
        'lexical': 'judgment',
        'head': 'left',
    },
    'thuhilhna': {
        'morphemes': ['thu', 'hilh', 'na'],
        'structure': '(thu-hilh)-na',
        'lexical': 'teaching',
        'head': 'left',
    },
    'khuaneute': {
        'morphemes': ['khua', 'neu', 'te'],
        'structure': '(khua-neu)-te',
        'lexical': 'villages',
        'head': 'left',
    },
    'khuamite': {
        'morphemes': ['khua', 'mi', 'te'],
        'structure': '(khua-mi)-te',
        'lexical': 'townspeople',
        'head': 'left',
    },
    'tuamtuamte': {
        'morphemes': ['tuam', 'tuam', 'te'],
        'structure': '(tuam-tuam)-te',
        'lexical': 'various.ones',
        'head': 'left',
    },
    # Round 174: Additional ternary compounds from full audit
    'lonona': {
        'morphemes': ['lo', 'no', 'na'],
        'structure': '(lo-no)-na',
        'lexical': 'disobedience',
        'head': 'left',
    },
    'nitumna': {
        'morphemes': ['ni', 'tum', 'na'],
        'structure': '(ni-tum)-na',
        'lexical': 'always',
        'head': 'left',
    },
    'thupiaknate': {
        'morphemes': ['thu', 'piak', 'na', 'te'],
        'structure': '((thu-piak)-na)-te',
        'lexical': 'commandments',
        'head': 'left',
    },
    'cihnopna': {
        'morphemes': ['cih', 'nop', 'na'],
        'structure': '(cih-nop)-na',
        'lexical': 'meaning',
        'head': 'left',
    },
    'langkhatah': {
        'morphemes': ['lang', 'khat', 'ah'],
        'structure': '(lang-khat)-ah',
        'lexical': 'on.one.side',
        'head': 'left',
    },
    'omlaite': {
        'morphemes': ['om', 'lai', 'te'],
        'structure': '(om-lai)-te',
        'lexical': 'those.present',
        'head': 'left',
    },
    'gamlapi': {
        'morphemes': ['gam', 'la', 'pi'],
        'structure': '(gam-la)-pi',
        'lexical': 'wilderness',
        'head': 'left',
    },
    'lametna': {
        'morphemes': ['lam', 'et', 'na'],
        'structure': '(lam-et)-na',
        'lexical': 'example',
        'head': 'left',
    },
    'kiciamna': {
        'morphemes': ['ki', 'ciam', 'na'],
        'structure': '(ki-ciam)-na',
        'lexical': 'covenant',
        'head': 'left',
    },
    'singlamteh': {
        'morphemes': ['sing', 'lam', 'teh'],
        'structure': 'sing-(lam-teh)',
        'lexical': 'cross',
        'head': 'right',
    },
    'lasakna': {
        'morphemes': ['la', 'sak', 'na'],
        'structure': '(la-sak)-na',
        'lexical': 'redemption',
        'head': 'left',
    },
    'phattuamna': {
        'morphemes': ['phat', 'tuam', 'na'],
        'structure': '(phat-tuam)-na',
        'lexical': 'vow',
        'head': 'left',
    },
    'mualtungah': {
        'morphemes': ['mual', 'tung', 'ah'],
        'structure': '(mual-tung)-ah',
        'lexical': 'on.mountaintop',
        'head': 'left',
    },
    'mawhsakna': {
        'morphemes': ['mawh', 'sak', 'na'],
        'structure': '(mawh-sak)-na',
        'lexical': 'causing.sin',
        'head': 'left',
    },
    'innkuante': {
        'morphemes': ['inn', 'kuan', 'te'],
        'structure': '(inn-kuan)-te',
        'lexical': 'households',
        'head': 'left',
    },
    'langpangin': {
        'morphemes': ['lang', 'pang', 'in'],
        'structure': '(lang-pang)-in',
        'lexical': 'beside',
        'head': 'left',
    },
    'maizumna': {
        'morphemes': ['mai', 'zum', 'na'],
        'structure': '(mai-zum)-na',
        'lexical': 'obeisance',
        'head': 'left',
    },
    'bawngtalte': {
        'morphemes': ['bawng', 'tal', 'te'],
        'structure': '(bawng-tal)-te',
        'lexical': 'calves',
        'head': 'left',
    },
    'naupangte': {
        'morphemes': ['nau', 'pang', 'te'],
        'structure': '(nau-pang)-te',
        'lexical': 'children',
        'head': 'left',
    },
    'zingsangin': {
        'morphemes': ['zing', 'sang', 'in'],
        'structure': '(zing-sang)-in',
        'lexical': 'early.morning',
        'head': 'left',
    },
    'lamdangte': {
        'morphemes': ['lam', 'dang', 'te'],
        'structure': '(lam-dang)-te',
        'lexical': 'other.ways',
        'head': 'left',
    },
    'thukhente': {
        'morphemes': ['thu', 'khen', 'te'],
        'structure': '(thu-khen)-te',
        'lexical': 'judgments',
        'head': 'left',
    },
    'midikte': {
        'morphemes': ['mi', 'dik', 'te'],
        'structure': '(mi-dik)-te',
        'lexical': 'righteous.ones',
        'head': 'left',
    },
    'biakpiaknate': {
        'morphemes': ['biak', 'piak', 'na', 'te'],
        'structure': '((biak-piak)-na)-te',
        'lexical': 'offerings',
        'head': 'left',
    },
    'kiphatsakna': {
        'morphemes': ['ki', 'phat', 'sak', 'na'],
        'structure': '((ki-phat)-sak)-na',
        'lexical': 'self.glorification',
        'head': 'left',
    },
    'puanhampi': {
        'morphemes': ['puan', 'ham', 'pi'],
        'structure': '(puan-ham)-pi',
        'lexical': 'veil',
        'head': 'left',
    },
    'laizangah': {
        'morphemes': ['lai', 'zang', 'ah'],
        'structure': '(lai-zang)-ah',
        'lexical': 'in.midst',
        'head': 'left',
    },
    'thumanin': {
        'morphemes': ['thu', 'man', 'in'],
        'structure': '(thu-man)-in',
        'lexical': 'truly',
        'head': 'left',
    },
    'puantualpi': {
        'morphemes': ['puan', 'tual', 'pi'],
        'structure': '(puan-tual)-pi',
        'lexical': 'great.robe',
        'head': 'left',
    },
    'lasaknate': {
        'morphemes': ['la', 'sak', 'na', 'te'],
        'structure': '((la-sak)-na)-te',
        'lexical': 'redemptions',
        'head': 'left',
    },
    # Round 175: Medium-frequency ternary compounds (20-39x)
    'ulianpa': {
        'morphemes': ['u', 'lian', 'pa'],
        'structure': '(u-lian)-pa',
        'lexical': 'elder',
        'head': 'left',
    },
    'pulnatna': {
        'morphemes': ['pul', 'nat', 'na'],
        'structure': '(pul-nat)-na',
        'lexical': 'terror',
        'head': 'left',
    },
    'kipawlna': {
        'morphemes': ['ki', 'pawl', 'na'],
        'structure': '(ki-pawl)-na',
        'lexical': 'fellowship',
        'head': 'left',
    },
    'kiciamteh': {
        'morphemes': ['ki', 'ciam', 'teh'],
        'structure': '(ki-ciam)-teh',
        'lexical': 'circumcision',
        'head': 'left',
    },
    'kitotna': {
        'morphemes': ['ki', 'tot', 'na'],
        'structure': '(ki-tot)-na',
        'lexical': 'circumcision',
        'head': 'left',
    },
    'meivakkhuam': {
        'morphemes': ['mei', 'vak', 'khuam'],
        'structure': '(mei-vak)-khuam',
        'lexical': 'lampstand',
        'head': 'left',
    },
    'neihsate': {
        'morphemes': ['neih', 'sa', 'te'],
        'structure': '(neih-sa)-te',
        'lexical': 'possessions',
        'head': 'left',
    },
    'pawlpite': {
        'morphemes': ['pawl', 'pi', 'te'],
        'structure': '(pawl-pi)-te',
        'lexical': 'elders',
        'head': 'left',
    },
    'munmuanhuai': {
        'morphemes': ['mun', 'muan', 'huai'],
        'structure': '(mun-muan)-huai',
        'lexical': 'trustworthy',
        'head': 'left',
    },
    'honpite': {
        'morphemes': ['hon', 'pi', 'te'],
        'structure': '(hon-pi)-te',
        'lexical': 'multitudes',
        'head': 'left',
    },
    'kisapna': {
        'morphemes': ['ki', 'sap', 'na'],
        'structure': '(ki-sap)-na',
        'lexical': 'calling',
        'head': 'left',
    },
    'ompihna': {
        'morphemes': ['om', 'pih', 'na'],
        'structure': '(om-pih)-na',
        'lexical': 'presence',
        'head': 'left',
    },
    'kikaikhawm': {
        'morphemes': ['ki', 'kai', 'khawm'],
        'structure': '(ki-kai)-khawm',
        'lexical': 'assembly',
        'head': 'left',
    },
    'lauhuaina': {
        'morphemes': ['lau', 'huai', 'na'],
        'structure': '(lau-huai)-na',
        'lexical': 'dread',
        'head': 'left',
    },
    'paubaanna': {
        'morphemes': ['pau', 'baan', 'na'],
        'structure': '(pau-baan)-na',
        'lexical': 'blasphemy',
        'head': 'left',
    },
    'paktatna': {
        'morphemes': ['pak', 'tat', 'na'],
        'structure': '(pak-tat)-na',
        'lexical': 'declaration',
        'head': 'left',
    },
    'salsuahna': {
        'morphemes': ['sal', 'suah', 'na'],
        'structure': '(sal-suah)-na',
        'lexical': 'slavery',
        'head': 'left',
    },
    'muvanlai': {
        'morphemes': ['mu', 'van', 'lai'],
        'structure': 'mu-(van-lai)',
        'lexical': 'vision',
        'head': 'right',
    },
    'aisanna': {
        'morphemes': ['ai', 'san', 'na'],
        'structure': '(ai-san)-na',
        'lexical': 'persecution',
        'head': 'left',
    },
    'galdona': {
        'morphemes': ['gal', 'do', 'na'],
        'structure': '(gal-do)-na',
        'lexical': 'victory',
        'head': 'left',
    },
    'miliante': {
        'morphemes': ['mi', 'lian', 'te'],
        'structure': '(mi-lian)-te',
        'lexical': 'nobles',
        'head': 'left',
    },
    'kipatna': {
        'morphemes': ['ki', 'pat', 'na'],
        'structure': '(ki-pat)-na',
        'lexical': 'beginning',
        'head': 'left',
    },
    'muhdahhuai': {
        'morphemes': ['muh', 'dah', 'huai'],
        'structure': '(muh-dah)-huai',
        'lexical': 'abomination',
        'head': 'left',
    },
    'ancilna': {
        'morphemes': ['an', 'cil', 'na'],
        'structure': '(an-cil)-na',
        'lexical': 'threshing',
        'head': 'left',
    },
    'kongcingte': {
        'morphemes': ['kong', 'cing', 'te'],
        'structure': '(kong-cing)-te',
        'lexical': 'faithful.ones',
        'head': 'left',
    },
    'vankoihna': {
        'morphemes': ['van', 'koih', 'na'],
        'structure': '(van-koih)-na',
        'lexical': 'heaven',
        'head': 'left',
    },
    'migitna': {
        'morphemes': ['mi', 'git', 'na'],
        'structure': '(mi-git)-na',
        'lexical': 'hatred',
        'head': 'left',
    },
    'kisuanna': {
        'morphemes': ['ki', 'suan', 'na'],
        'structure': '(ki-suan)-na',
        'lexical': 'succession',
        'head': 'left',
    },
    'hopihna': {
        'morphemes': ['ho', 'pih', 'na'],
        'structure': '(ho-pih)-na',
        'lexical': 'counsel',
        'head': 'left',
    },
    'kizepna': {
        'morphemes': ['ki', 'zep', 'na'],
        'structure': '(ki-zep)-na',
        'lexical': 'joining',
        'head': 'left',
    },
    'tuiphumpa': {
        'morphemes': ['tui', 'phum', 'pa'],
        'structure': '(tui-phum)-pa',
        'lexical': 'baptist',
        'head': 'left',
    },
    'nulepa': {
        'morphemes': ['nu', 'le', 'pa'],
        'structure': 'nu-le-pa',
        'lexical': 'parents',
        'head': 'none',
    },
    'cihtakna': {
        'morphemes': ['cih', 'tak', 'na'],
        'structure': '(cih-tak)-na',
        'lexical': 'testimony',
        'head': 'left',
    },
    'galkapmangte': {
        'morphemes': ['gal', 'kap', 'mang', 'te'],
        'structure': '((gal-kap)-mang)-te',
        'lexical': 'captains',
        'head': 'left',
    },
    'khualzinna': {
        'morphemes': ['khual', 'zin', 'na'],
        'structure': '(khual-zin)-na',
        'lexical': 'pilgrimage',
        'head': 'left',
    },
    'hoihpente': {
        'morphemes': ['hoih', 'pen', 'te'],
        'structure': '(hoih-pen)-te',
        'lexical': 'best.ones',
        'head': 'left',
    },
    'leengpeite': {
        'morphemes': ['leeng', 'pei', 'te'],
        'structure': '(leeng-pei)-te',
        'lexical': 'chariot.leaders',
        'head': 'left',
    },
    'kithahna': {
        'morphemes': ['ki', 'thah', 'na'],
        'structure': '(ki-thah)-na',
        'lexical': 'murder',
        'head': 'left',
    },
    'paktatte': {
        'morphemes': ['pak', 'tat', 'te'],
        'structure': '(pak-tat)-te',
        'lexical': 'portions',
        'head': 'left',
    },
    'lunghihmawhna': {
        'morphemes': ['lung', 'hih', 'mawh', 'na'],
        'structure': '((lung-hih)-mawh)-na',
        'lexical': 'guilt',
        'head': 'left',
    },
    'lopate': {
        'morphemes': ['lo', 'pa', 'te'],
        'structure': '(lo-pa)-te',
        'lexical': 'farmers',
        'head': 'left',
    },
    'kigenna': {
        'morphemes': ['ki', 'gen', 'na'],
        'structure': '(ki-gen)-na',
        'lexical': 'conversation',
        'head': 'left',
    },
    'lamkalah': {
        'morphemes': ['lam', 'kal', 'ah'],
        'structure': '(lam-kal)-ah',
        'lexical': 'midway',
        'head': 'left',
    },
    'gamlumna': {
        'morphemes': ['gam', 'lum', 'na'],
        'structure': '(gam-lum)-na',
        'lexical': 'south',
        'head': 'left',
    },
    'kigelhna': {
        'morphemes': ['ki', 'gelh', 'na'],
        'structure': '(ki-gelh)-na',
        'lexical': 'scripture',
        'head': 'left',
    },
    'theihtelna': {
        'morphemes': ['theih', 'tel', 'na'],
        'structure': '(theih-tel)-na',
        'lexical': 'wisdom',
        'head': 'left',
    },
    'thahatte': {
        'morphemes': ['tha', 'hat', 'te'],
        'structure': '(tha-hat)-te',
        'lexical': 'mighty.ones',
        'head': 'left',
    },
    'tuikuangpi': {
        'morphemes': ['tui', 'kuang', 'pi'],
        'structure': '(tui-kuang)-pi',
        'lexical': 'great.pool',
        'head': 'left',
    },
    'thutheihna': {
        'morphemes': ['thu', 'theih', 'na'],
        'structure': '(thu-theih)-na',
        'lexical': 'knowledge',
        'head': 'left',
    },
    'mihaute': {
        'morphemes': ['mi', 'hau', 'te'],
        'structure': '(mi-hau)-te',
        'lexical': 'rich.ones',
        'head': 'left',
    },
    'khangnote': {
        'morphemes': ['khang', 'no', 'te'],
        'structure': '(khang-no)-te',
        'lexical': 'youth',
        'head': 'left',
    },
    'thawhkikna': {
        'morphemes': ['thawh', 'kik', 'na'],
        'structure': '(thawh-kik)-na',
        'lexical': 'resurrection',
        'head': 'left',
    },
    # Round 176: 10-19x frequency ternary compounds
    'vaihawmna': {
        'morphemes': ['vai', 'hawm', 'na'],
        'structure': '(vai-hawm)-na',
        'lexical': 'counsel',
        'head': 'left',
    },
    'lungmuanna': {
        'morphemes': ['lung', 'muan', 'na'],
        'structure': '(lung-muan)-na',
        'lexical': 'confidence',
        'head': 'left',
    },
    'minphatna': {
        'morphemes': ['min', 'phat', 'na'],
        'structure': '(min-phat)-na',
        'lexical': 'fame',
        'head': 'left',
    },
    'bawnghonte': {
        'morphemes': ['bawng', 'hon', 'te'],
        'structure': '(bawng-hon)-te',
        'lexical': 'herds',
        'head': 'left',
    },
    'hingkiksak': {
        'morphemes': ['hing', 'kik', 'sak'],
        'structure': '(hing-kik)-sak',
        'lexical': 'resurrect',
        'head': 'left',
    },
    'nihveina': {
        'morphemes': ['nih', 'vei', 'na'],
        'structure': '(nih-vei)-na',
        'lexical': 'second',
        'head': 'left',
    },
    'khialhsakna': {
        'morphemes': ['khialh', 'sak', 'na'],
        'structure': '(khialh-sak)-na',
        'lexical': 'trespass',
        'head': 'left',
    },
    'hawlkhiatna': {
        'morphemes': ['hawl', 'khiat', 'na'],
        'structure': '(hawl-khiat)-na',
        'lexical': 'persecution',
        'head': 'left',
    },
    'thukimna': {
        'morphemes': ['thu', 'kim', 'na'],
        'structure': '(thu-kim)-na',
        'lexical': 'covenant',
        'head': 'left',
    },
    'thangpaihna': {
        'morphemes': ['thang', 'paih', 'na'],
        'structure': '(thang-paih)-na',
        'lexical': 'flood',
        'head': 'left',
    },
    'lungduaina': {
        'morphemes': ['lung', 'duai', 'na'],
        'structure': '(lung-duai)-na',
        'lexical': 'compassion',
        'head': 'left',
    },
    'huaihamna': {
        'morphemes': ['huai', 'ham', 'na'],
        'structure': '(huai-ham)-na',
        'lexical': 'terror',
        'head': 'left',
    },
    'galsimna': {
        'morphemes': ['gal', 'sim', 'na'],
        'structure': '(gal-sim)-na',
        'lexical': 'census',
        'head': 'left',
    },
    'hamphatna': {
        'morphemes': ['ham', 'phat', 'na'],
        'structure': '(ham-phat)-na',
        'lexical': 'glory',
        'head': 'left',
    },
    'kikhumna': {
        'morphemes': ['ki', 'khum', 'na'],
        'structure': '(ki-khum)-na',
        'lexical': 'covering',
        'head': 'left',
    },
    'kulhkongpite': {
        'morphemes': ['kulh', 'kong', 'pi', 'te'],
        'structure': '((kulh-kong)-pi)-te',
        'lexical': 'city.gates',
        'head': 'left',
    },
    'meigongnu': {
        'morphemes': ['mei', 'gong', 'nu'],
        'structure': '(mei-gong)-nu',
        'lexical': 'widow',
        'head': 'left',
    },
    'kilamdanna': {
        'morphemes': ['ki', 'lam', 'dan', 'na'],
        'structure': '((ki-lam)-dan)-na',
        'lexical': 'pattern',
        'head': 'left',
    },
    # Round 177: 5-9x frequency ternary compounds
    'siansuahna': {
        'morphemes': ['sian', 'suah', 'na'],
        'structure': '(sian-suah)-na',
        'lexical': 'sanctification',
        'head': 'left',
    },
    'kisiansuahna': {
        'morphemes': ['ki', 'sian', 'suah', 'na'],
        'structure': '(ki-(sian-suah))-na',
        'lexical': 'sanctification',
        'head': 'left',
    },
    'kiciamtehna': {
        'morphemes': ['ki', 'ciam', 'teh', 'na'],
        'structure': '((ki-ciam)-teh)-na',
        'lexical': 'circumcision',
        'head': 'left',
    },
    'kibiakna': {
        'morphemes': ['ki', 'biak', 'na'],
        'structure': '(ki-biak)-na',
        'lexical': 'worship',
        'head': 'left',
    },
    'thongkiatna': {
        'morphemes': ['thong', 'kiat', 'na'],
        'structure': '(thong-kiat)-na',
        'lexical': 'deliverance',
        'head': 'left',
    },
    'lungdamhuai': {
        'morphemes': ['lung', 'dam', 'huai'],
        'structure': '(lung-dam)-huai',
        'lexical': 'great.joy',
        'head': 'left',
    },
    'hehnepna': {
        'morphemes': ['heh', 'nep', 'na'],
        'structure': '(heh-nep)-na',
        'lexical': 'patience',
        'head': 'left',
    },
    'kilatna': {
        'morphemes': ['ki', 'lat', 'na'],
        'structure': '(ki-lat)-na',
        'lexical': 'strength',
        'head': 'left',
    },
    'kipsakna': {
        'morphemes': ['kip', 'sak', 'na'],
        'structure': '(kip-sak)-na',
        'lexical': 'confirmation',
        'head': 'left',
    },
    'kihhuaina': {
        'morphemes': ['ki', 'hhuai', 'na'],
        'structure': '(ki-hhuai)-na',
        'lexical': 'abomination',
        'head': 'left',
    },
    'bilbahte': {
        'morphemes': ['bil', 'bah', 'te'],
        'structure': '(bil-bah)-te',
        'lexical': 'deaf.ones',
        'head': 'left',
    },
    'phulakna': {
        'morphemes': ['phu', 'lak', 'na'],
        'structure': '(phu-lak)-na',
        'lexical': 'burden',
        'head': 'left',
    },
    'kitangsapna': {
        'morphemes': ['ki', 'tang', 'sap', 'na'],
        'structure': '((ki-tang)-sap)-na',
        'lexical': 'compulsion',
        'head': 'left',
    },
    'langpanna': {
        'morphemes': ['lang', 'pan', 'na'],
        'structure': '(lang-pan)-na',
        'lexical': 'advocacy',
        'head': 'left',
    },
    'laigelhna': {
        'morphemes': ['lai', 'gelh', 'na'],
        'structure': '(lai-gelh)-na',
        'lexical': 'writing',
        'head': 'left',
    },
    'liveina': {
        'morphemes': ['li', 'vei', 'na'],
        'structure': '(li-vei)-na',
        'lexical': 'fourth',
        'head': 'left',
    },
    'khangsimna': {
        'morphemes': ['khang', 'sim', 'na'],
        'structure': '(khang-sim)-na',
        'lexical': 'genealogy',
        'head': 'left',
    },
    'thumante': {
        'morphemes': ['thu', 'man', 'te'],
        'structure': '(thu-man)-te',
        'lexical': 'true.words',
        'head': 'left',
    },
    'thutakna': {
        'morphemes': ['thu', 'tak', 'na'],
        'structure': '(thu-tak)-na',
        'lexical': 'truth',
        'head': 'left',
    },
    'thuciamte': {
        'morphemes': ['thu', 'ciam', 'te'],
        'structure': '(thu-ciam)-te',
        'lexical': 'promises',
        'head': 'left',
    },
    'thahatpa': {
        'morphemes': ['tha', 'hat', 'pa'],
        'structure': '(tha-hat)-pa',
        'lexical': 'mighty.man',
        'head': 'left',
    },
    'gamdangte': {
        'morphemes': ['gam', 'dang', 'te'],
        'structure': '(gam-dang)-te',
        'lexical': 'other.lands',
        'head': 'left',
    },
    'innkhumzang': {
        'morphemes': ['inn', 'khum', 'zang'],
        'structure': '(inn-khum)-zang',
        'lexical': 'tent.curtain',
        'head': 'left',
    },
    'sintuamte': {
        'morphemes': ['sin', 'tuam', 'te'],
        'structure': '(sin-tuam)-te',
        'lexical': 'liver.lobes',
        'head': 'left',
    },
    'puanmongteep': {
        'morphemes': ['puan', 'mong', 'teep'],
        'structure': '(puan-mong)-teep',
        'lexical': 'garment.hem',
        'head': 'left',
    },
    'netniamna': {
        'morphemes': ['net', 'niam', 'na'],
        'structure': '(net-niam)-na',
        'lexical': 'hunger',
        'head': 'left',
    },
    'kingakna': {
        'morphemes': ['ki', 'ngak', 'na'],
        'structure': '(ki-ngak)-na',
        'lexical': 'expectation',
        'head': 'left',
    },
    'kikoihna': {
        'morphemes': ['ki', 'koih', 'na'],
        'structure': '(ki-koih)-na',
        'lexical': 'placement',
        'head': 'left',
    },
    'kisilna': {
        'morphemes': ['ki', 'sil', 'na'],
        'structure': '(ki-sil)-na',
        'lexical': 'washing',
        'head': 'left',
    },
    'kicihna': {
        'morphemes': ['ki', 'cih', 'na'],
        'structure': '(ki-cih)-na',
        'lexical': 'saying',
        'head': 'left',
    },
    # Round 178: More 5-9x frequency ternary compounds (batch 2)
    'kithawhkiksak': {
        'morphemes': ['ki', 'thawh', 'kik', 'sak'],
        'structure': '((ki-thawh)-kik)-sak',
        'lexical': 'resurrect',
        'head': 'left',
    },
    'kituiphum': {
        'morphemes': ['ki', 'tui', 'phum'],
        'structure': 'ki-(tui-phum)',
        'lexical': 'baptize',
        'head': 'right',
    },
    'minthangsak': {
        'morphemes': ['min', 'thang', 'sak'],
        'structure': '(min-thang)-sak',
        'lexical': 'glorify',
        'head': 'left',
    },
    'minsiasak': {
        'morphemes': ['min', 'sia', 'sak'],
        'structure': '(min-sia)-sak',
        'lexical': 'blaspheme',
        'head': 'left',
    },
    'meivakna': {
        'morphemes': ['mei', 'vak', 'na'],
        'structure': '(mei-vak)-na',
        'lexical': 'lamplight',
        'head': 'left',
    },
    'maisakna': {
        'morphemes': ['mai', 'sak', 'na'],
        'structure': '(mai-sak)-na',
        'lexical': 'appearance',
        'head': 'left',
    },
    'gilkialte': {
        'morphemes': ['gil', 'kial', 'te'],
        'structure': '(gil-kial)-te',
        'lexical': 'bowels',
        'head': 'left',
    },
    'kiselna': {
        'morphemes': ['ki', 'sel', 'na'],
        'structure': '(ki-sel)-na',
        'lexical': 'strife',
        'head': 'left',
    },
    'kiphawkna': {
        'morphemes': ['ki', 'phawk', 'na'],
        'structure': '(ki-phawk)-na',
        'lexical': 'remembrance',
        'head': 'left',
    },
    'kikhihna': {
        'morphemes': ['ki', 'khih', 'na'],
        'structure': '(ki-khih)-na',
        'lexical': 'binding',
        'head': 'left',
    },
    'kihona': {
        'morphemes': ['ki', 'ho', 'na'],
        'structure': '(ki-ho)-na',
        'lexical': 'calling',
        'head': 'left',
    },
    'gentheihna': {
        'morphemes': ['gen', 'theih', 'na'],
        'structure': '(gen-theih)-na',
        'lexical': 'eloquence',
        'head': 'left',
    },
    'gamdaihna': {
        'morphemes': ['gam', 'daih', 'na'],
        'structure': '(gam-daih)-na',
        'lexical': 'breadth',
        'head': 'left',
    },
    'hamsiatna': {
        'morphemes': ['ham', 'siat', 'na'],
        'structure': '(ham-siat)-na',
        'lexical': 'reproach',
        'head': 'left',
    },
    'khuakulhpi': {
        'morphemes': ['khua', 'kulh', 'pi'],
        'structure': '(khua-kulh)-pi',
        'lexical': 'fortress',
        'head': 'left',
    },
    'innkuansung': {
        'morphemes': ['inn', 'kuan', 'sung'],
        'structure': '(inn-kuan)-sung',
        'lexical': 'household',
        'head': 'left',
    },
    'khanghamte': {
        'morphemes': ['khang', 'ham', 'te'],
        'structure': '(khang-ham)-te',
        'lexical': 'ancestors',
        'head': 'left',
    },
    'sawmnihna': {
        'morphemes': ['sawm', 'nih', 'na'],
        'structure': '(sawm-nih)-na',
        'lexical': 'twelfth',
        'head': 'left',
    },
    # Round 179: More 5-9x frequency ternary compounds (batch 3)
    'siahdongpa': {
        'morphemes': ['siah', 'dong', 'pa'],
        'structure': '(siah-dong)-pa',
        'lexical': 'tax.collector',
        'head': 'left',
    },
    'phulapa': {
        'morphemes': ['phu', 'la', 'pa'],
        'structure': '(phu-la)-pa',
        'lexical': 'avenger',
        'head': 'left',
    },
    'lungkiasak': {
        'morphemes': ['lung', 'kia', 'sak'],
        'structure': '(lung-kia)-sak',
        'lexical': 'discourage',
        'head': 'left',
    },
    'lungsimtawng': {
        'morphemes': ['lung', 'sim', 'tawng'],
        'structure': '(lung-sim)-tawng',
        'lexical': 'hypocrisy',
        'head': 'left',
    },
    'mulkiatna': {
        'morphemes': ['mul', 'kiat', 'na'],
        'structure': '(mul-kiat)-na',
        'lexical': 'shaving',
        'head': 'left',
    },
    'lokhawhna': {
        'morphemes': ['lo', 'khawh', 'na'],
        'structure': '(lo-khawh)-na',
        'lexical': 'farming',
        'head': 'left',
    },
    'leenggahkeu': {
        'morphemes': ['leeng', 'gah', 'keu'],
        'structure': '(leeng-gah)-keu',
        'lexical': 'raisin.cluster',
        'head': 'left',
    },
    'manphatna': {
        'morphemes': ['man', 'phat', 'na'],
        'structure': '(man-phat)-na',
        'lexical': 'worthiness',
        'head': 'left',
    },
    'kivuina': {
        'morphemes': ['ki', 'vui', 'na'],
        'structure': '(ki-vui)-na',
        'lexical': 'burial',
        'head': 'left',
    },
    'kitheihna': {
        'morphemes': ['ki', 'theih', 'na'],
        'structure': '(ki-theih)-na',
        'lexical': 'knowledge',
        'head': 'left',
    },
    'kisikna': {
        'morphemes': ['ki', 'sik', 'na'],
        'structure': '(ki-sik)-na',
        'lexical': 'turning',
        'head': 'left',
    },
    'kisatna': {
        'morphemes': ['ki', 'sat', 'na'],
        'structure': '(ki-sat)-na',
        'lexical': 'striking',
        'head': 'left',
    },
    'kihuhna': {
        'morphemes': ['ki', 'huh', 'na'],
        'structure': '(ki-huh)-na',
        'lexical': 'help',
        'head': 'left',
    },
    'kihalna': {
        'morphemes': ['ki', 'hal', 'na'],
        'structure': '(ki-hal)-na',
        'lexical': 'burning',
        'head': 'left',
    },
    'sawmlinih': {
        'morphemes': ['sawm', 'li', 'nih'],
        'structure': '(sawm-li)-nih',
        'lexical': 'forty.two',
        'head': 'left',
    },
    # Round 180: More 5-9x frequency ternary compounds (batch 4)
    'genkholhna': {
        'morphemes': ['gen', 'kholh', 'na'],
        'structure': '(gen-kholh)-na',
        'lexical': 'prophecy',  # speak-INTENS-NMLZ = prophetic declaration
        'head': 'left',
    },
    'gancingte': {
        'morphemes': ['gan', 'cing', 'te'],
        'structure': '(gan-cing)-te',
        'lexical': 'shepherds',
        'head': 'left',
    },
    'galdaihna': {
        'morphemes': ['gal', 'daih', 'na'],
        'structure': '(gal-daih)-na',
        'lexical': 'warfare',
        'head': 'left',
    },
    'zintunna': {
        'morphemes': ['zin', 'tun', 'na'],
        'structure': '(zin-tun)-na',
        'lexical': 'destination',
        'head': 'left',
    },
    'zaksakna': {
        'morphemes': ['zak', 'sak', 'na'],
        'structure': '(zak-sak)-na',
        'lexical': 'testimony',
        'head': 'left',
    },
    'thutelna': {
        'morphemes': ['thu', 'tel', 'na'],
        'structure': '(thu-tel)-na',
        'lexical': 'fulfillment',
        'head': 'left',
    },
    'thutanna': {
        'morphemes': ['thu', 'tan', 'na'],
        'structure': '(thu-tan)-na',
        'lexical': 'judgment',
        'head': 'left',
    },
    'tawldamna': {
        'morphemes': ['tawl', 'dam', 'na'],
        'structure': '(tawl-dam)-na',
        'lexical': 'rest',
        'head': 'left',
    },
    'tawikhaina': {
        'morphemes': ['tawi', 'khai', 'na'],
        'structure': '(tawi-khai)-na',
        'lexical': 'balance',
        'head': 'left',
    },
    'tatsiatna': {
        'morphemes': ['tat', 'siat', 'na'],
        'structure': '(tat-siat)-na',
        'lexical': 'destruction',
        'head': 'left',
    },
    'tatkhialhna': {
        'morphemes': ['tat', 'khialh', 'na'],
        'structure': '(tat-khialh)-na',
        'lexical': 'transgression',
        'head': 'left',
    },
    'piankhiatna': {
        'morphemes': ['pian', 'khiat', 'na'],
        'structure': '(pian-khiat)-na',
        'lexical': 'birthright',
        'head': 'left',
    },
    'biakinncing': {
        'morphemes': ['biak', 'inn', 'cing'],
        'structure': '(biak-inn)-cing',
        'lexical': 'temple.betrayal',
        'head': 'left',
    },
    'thuciamteh': {
        'morphemes': ['thu', 'ciam', 'teh'],
        'structure': '(thu-ciam)-teh',
        'lexical': 'covenant',
        'head': 'left',
    },
    'siangthosakpa': {
        'morphemes': ['siangtho', 'sak', 'pa'],
        'structure': '(siangtho-sak)-pa',
        'lexical': 'sanctifier',
        'head': 'left',
    },
    'tuinakte': {
        'morphemes': ['tui', 'nak', 'te'],
        'structure': '(tui-nak)-te',
        'lexical': 'springs',
        'head': 'left',
    },
    'thuthukpi': {
        'morphemes': ['thu', 'thuk', 'pi'],
        'structure': '(thu-thuk)-pi',
        'lexical': 'deep.word',
        'head': 'left',
    },
    
    # Round 183: More ternary compounds (5-9x)
    'innluahza': {
        'morphemes': ['inn', 'luah', 'za'],
        'structure': '(inn-luah)-za',
        'lexical': 'birthright',
        'head': 'left',
    },
    'luzangte': {
        'morphemes': ['lu', 'zang', 'te'],
        'structure': '(lu-zang)-te',
        'lexical': 'crowns',
        'head': 'left',
    },
    'singniimte': {
        'morphemes': ['sing', 'niim', 'te'],
        'structure': '(sing-niim)-te',
        'lexical': 'green.trees',
        'head': 'left',
    },
    'kamciamte': {
        'morphemes': ['kam', 'ciam', 'te'],
        'structure': '(kam-ciam)-te',
        'lexical': 'vows',
        'head': 'left',
    },
    
    # Round 185: Low-frequency ternary compounds (1-4x)
    'limlemel': {
        'morphemes': ['lim', 'le', 'mel'],
        'structure': 'lim-(le-mel)',
        'lexical': 'formless.void',    # Genesis 1:2 "without form and void"
        'head': 'right',
    },
}


def get_morpheme_gloss(morpheme: str, position: str = 'default') -> Optional[str]:
    """
    Get the gloss for an atomic morpheme from all available sources.
    
    Args:
        morpheme: The morpheme to look up
        position: Context hint - 'default', 'as_suffix', 'as_modifier', 'as_prefix'
                  Used to disambiguate morphemes with multiple meanings.
    
    Checks AMBIGUOUS_ATOMIC first for position-sensitive lookup,
    then ATOMIC_GLOSSES, then falls back to NOUN_STEMS, VERB_STEMS.
    """
    morpheme_lower = morpheme.lower()
    
    # Priority 0: Check ambiguous morphemes with position-aware lookup
    if morpheme_lower in AMBIGUOUS_ATOMIC:
        meanings = AMBIGUOUS_ATOMIC[morpheme_lower]
        if position in meanings:
            return meanings[position]
        return meanings.get('default', list(meanings.values())[0])
    
    # Priority 1: Atomic glosses (designed for compositional analysis)
    if morpheme_lower in ATOMIC_GLOSSES:
        return ATOMIC_GLOSSES[morpheme_lower]
    
    # Priority 2: Noun stems
    if morpheme_lower in NOUN_STEMS:
        return NOUN_STEMS[morpheme_lower]
    
    # Priority 3: Verb stems
    if morpheme_lower in VERB_STEMS:
        return VERB_STEMS[morpheme_lower]
    
    return None


def is_known_word(word: str) -> bool:
    """
    Check if word exists in any morpheme dictionary.
    
    Used to determine if a word/stem is a known Tedim morpheme,
    regardless of part of speech. Checks VERB_STEMS, NOUN_STEMS,
    ATOMIC_GLOSSES, FUNCTION_WORDS, and VERB_STEM_PAIRS.
    
    Args:
        word: The word to check (case-insensitive)
    
    Returns:
        True if word is found in any dictionary
    """
    w = word.lower()
    return (w in VERB_STEMS or w in NOUN_STEMS or 
            w in ATOMIC_GLOSSES or w in FUNCTION_WORDS or
            w in VERB_STEM_PAIRS)


def is_known_stem(word: str) -> bool:
    """
    Check if word is a known lexical stem (noun or verb).
    
    Unlike is_known_word(), this does NOT include function words,
    which is important for stem-splitting logic where we don't want
    to over-segment based on function word matches.
    
    Args:
        word: The word to check (case-insensitive)
    
    Returns:
        True if word is found in VERB_STEMS, NOUN_STEMS, or VERB_STEM_PAIRS
    """
    w = word.lower()
    return w in VERB_STEMS or w in NOUN_STEMS or w in VERB_STEM_PAIRS


def longest_first(d: dict):
    """
    Iterate dictionary items in longest-key-first order.
    
    Essential for morphological parsing where longer morphemes must match
    before shorter ones (e.g., 'khia' before 'khi', 'sak' before 'sa').
    
    Args:
        d: Dictionary to iterate
    
    Yields:
        (key, value) tuples sorted by descending key length
    
    Example:
        for suffix, gloss in longest_first(SUFFIXES):
            if word.endswith(suffix):
                ...
    """
    return sorted(d.items(), key=lambda x: -len(x[0]))


def longest_keys_first(d: dict):
    """
    Iterate dictionary keys in longest-first order.
    
    Like longest_first() but returns only keys, not (key, value) pairs.
    Useful when you only need to check key matches.
    
    Args:
        d: Dictionary whose keys to iterate
    
    Yields:
        Keys sorted by descending length
    """
    return sorted(d.keys(), key=lambda x: -len(x))


def analyze_binary_compound(word: str) -> Optional[CompoundStructure]:
    """
    Analyze a two-morpheme compound, returning its full structure.
    
    Returns CompoundStructure with:
    - morphemes: [m1, m2]
    - segmentation: "m1-m2"
    - bracketing: "(m1-m2)" 
    - compositional_gloss: "gloss1-gloss2"
    - lexical_gloss: holistic meaning if in BINARY_COMPOUNDS
    """
    word_lower = word.lower()
    
    # Check if it's a known binary compound
    if word_lower in BINARY_COMPOUNDS:
        m1, m2, lexical = BINARY_COMPOUNDS[word_lower]
        g1 = get_morpheme_gloss(m1) or '?'
        g2 = get_morpheme_gloss(m2) or '?'
        
        return CompoundStructure(
            morphemes=[m1, m2],
            segmentation=f"{m1}-{m2}",
            bracketing=f"({m1}-{m2})",
            compositional_gloss=f"({g1}-{g2})",
            lexical_gloss=lexical,
            head_position='right'  # Tedim is generally head-final
        )
    
    return None


def analyze_ternary_compound(word: str) -> Optional[CompoundStructure]:
    """
    Analyze a three-morpheme compound with hierarchical structure.
    
    Returns CompoundStructure with bracketed structure showing
    which morphemes group together (head compound vs modifier).
    
    Uses position-aware glossing for ambiguous morphemes:
    - Final position morphemes use 'as_suffix' 
    - Initial position morphemes use 'as_modifier'
    """
    word_lower = word.lower()
    
    # Check if it's a known ternary compound
    if word_lower in TERNARY_COMPOUNDS:
        info = TERNARY_COMPOUNDS[word_lower]
        morphemes = info['morphemes']
        
        # Position-aware glossing based on structure
        if info['head'] == 'right':
            # N (N N) - modifier + head compound
            # morphemes[0] is modifier, [1] and [2] are head compound
            g0 = get_morpheme_gloss(morphemes[0], 'as_modifier') or '?'
            g1 = get_morpheme_gloss(morphemes[1]) or '?'
            g2 = get_morpheme_gloss(morphemes[2], 'as_suffix') or '?'
            comp_gloss = f"{g0}-({g1}-{g2})"
        else:
            # (N N) N - head compound + modifier/suffix
            # morphemes[0] and [1] are head compound, [2] is suffix
            g0 = get_morpheme_gloss(morphemes[0]) or '?'
            g1 = get_morpheme_gloss(morphemes[1]) or '?'
            g2 = get_morpheme_gloss(morphemes[2], 'as_suffix') or '?'
            comp_gloss = f"({g0}-{g1})-{g2}"
        
        return CompoundStructure(
            morphemes=morphemes,
            segmentation='-'.join(morphemes),
            bracketing=info['structure'],
            compositional_gloss=comp_gloss,
            lexical_gloss=info.get('lexical'),
            head_position=info['head']
        )
    
    return None


def analyze_hierarchical_compound(word: str, depth: int = 0) -> Tuple[Optional[str], Optional[str]]:
    """
    Attempt hierarchical compound analysis using the new compound system.
    
    This function provides both the morpheme-level segmentation AND
    the appropriate gloss (preferring lexical over compositional).
    
    The analysis proceeds in order:
    1. Check for known ternary+ compounds (full structure known)
    2. Check for known binary compounds
    3. Try to decompose as [modifier] + [known binary compound]
    4. Try to decompose as [known binary compound] + [suffix]
    
    Returns:
        Tuple of (segmentation, gloss) or (None, None) if no analysis found
        
    The gloss returned is the LEXICAL gloss if available (e.g., "spices"),
    otherwise the COMPOSITIONAL gloss (e.g., "tree-(smell-water)").
    """
    if depth > 3:
        return (None, None)
    
    word_lower = word.lower()
    
    # Step 1: Check for known ternary compounds
    ternary = analyze_ternary_compound(word_lower)
    if ternary:
        return (ternary.segmentation, ternary.get_display_gloss())
    
    # Step 2: Check for known binary compounds
    binary = analyze_binary_compound(word_lower)
    if binary:
        return (binary.segmentation, binary.get_display_gloss())
    
    # Step 3: Try decomposing as [modifier] + [binary compound base]
    # Pattern: N (N N) - e.g., thei + namtui = fig + perfume
    for base, (m1, m2, base_lexical) in sorted(BINARY_COMPOUNDS.items(), 
                                                key=lambda x: -len(x[0])):
        if word_lower.endswith(base) and len(word_lower) > len(base):
            modifier = word_lower[:-len(base)]
            mod_gloss = get_morpheme_gloss(modifier, 'as_modifier')
            
            if mod_gloss:
                segmentation = f"{modifier}-{m1}-{m2}"
                
                # Check if this specific ternary has a known lexical gloss
                if word_lower in TERNARY_COMPOUNDS:
                    lex_gloss = TERNARY_COMPOUNDS[word_lower].get('lexical')
                    if lex_gloss:
                        return (segmentation, lex_gloss)
                
                # Use lexical gloss of base compound if available (Round 193m fix)
                if base_lexical:
                    comp_gloss = f"{mod_gloss}-{base_lexical}"
                else:
                    g1 = get_morpheme_gloss(m1) or '?'
                    g2 = get_morpheme_gloss(m2, 'as_suffix') or '?'
                    comp_gloss = f"{mod_gloss}-({g1}-{g2})"
                
                return (segmentation, comp_gloss)
            
            # Try recursive analysis of modifier
            if depth < 2:
                mod_result = analyze_hierarchical_compound(modifier, depth + 1)
                if mod_result[0]:
                    segmentation = f"{mod_result[0]}-{m1}-{m2}"
                    # Use lexical gloss of base compound if available
                    if base_lexical:
                        comp_gloss = f"({mod_result[1]})-{base_lexical}"
                    else:
                        g1 = get_morpheme_gloss(m1) or '?'
                        g2 = get_morpheme_gloss(m2, 'as_suffix') or '?'
                        comp_gloss = f"({mod_result[1]})-({g1}-{g2})"
                    return (segmentation, comp_gloss)
    
    # Step 4: Try decomposing as [binary compound] + [suffix/modifier]
    # Pattern: (N N) N - e.g., biakinn + lam = temple + direction
    # This is common for [compound] + grammatical suffix (te, na, pi, etc.)
    for base, (m1, m2, base_lexical) in sorted(BINARY_COMPOUNDS.items(),
                                                key=lambda x: -len(x[0])):
        if word_lower.startswith(base) and len(word_lower) > len(base):
            suffix = word_lower[len(base):]
            # Final position - use 'as_suffix' for position-aware glossing
            suffix_gloss = get_morpheme_gloss(suffix, 'as_suffix')
            
            if suffix_gloss:
                segmentation = f"{m1}-{m2}-{suffix}"
                # Use lexical gloss if available (Round 193m fix)
                # e.g., suanghawm-te = cave-PL, not (stone-counsel)-PL
                if base_lexical:
                    comp_gloss = f"{base_lexical}-{suffix_gloss}"
                else:
                    g1 = get_morpheme_gloss(m1) or '?'
                    g2 = get_morpheme_gloss(m2) or '?'
                    comp_gloss = f"({g1}-{g2})-{suffix_gloss}"
                
                return (segmentation, comp_gloss)
    
    return (None, None)


def get_full_compound_analysis(word: str) -> Optional[CompoundStructure]:
    """
    Get the full hierarchical analysis of a compound word.
    
    This is the main entry point for compound analysis when you need
    the full structure (not just segmentation + gloss).
    
    Returns:
        CompoundStructure with all fields populated, or None if not a compound
    """
    word_lower = word.lower()
    
    # Check ternary first (most specific)
    ternary = analyze_ternary_compound(word_lower)
    if ternary:
        return ternary
    
    # Check binary
    binary = analyze_binary_compound(word_lower)
    if binary:
        return binary
    
    # Try dynamic decomposition
    # Pattern: modifier + binary base (head-final: N + (N N))
    for base, (m1, m2, base_lexical) in sorted(BINARY_COMPOUNDS.items(),
                                                key=lambda x: -len(x[0])):
        if word_lower.endswith(base) and len(word_lower) > len(base):
            modifier = word_lower[:-len(base)]
            mod_gloss = get_morpheme_gloss(modifier, 'as_modifier')
            
            if mod_gloss:
                g1 = get_morpheme_gloss(m1) or '?'
                g2 = get_morpheme_gloss(m2, 'as_suffix') or '?'
                
                return CompoundStructure(
                    morphemes=[modifier, m1, m2],
                    segmentation=f"{modifier}-{m1}-{m2}",
                    bracketing=f"{modifier}-({m1}-{m2})",
                    compositional_gloss=f"{mod_gloss}-({g1}-{g2})",
                    lexical_gloss=None,  # Unknown - not in dictionary
                    head_position='right'
                )
    
    # Pattern: binary base + suffix (head-initial: (N N) + suffix)
    for base, (m1, m2, base_lexical) in sorted(BINARY_COMPOUNDS.items(),
                                                key=lambda x: -len(x[0])):
        if word_lower.startswith(base) and len(word_lower) > len(base):
            suffix = word_lower[len(base):]
            suffix_gloss = get_morpheme_gloss(suffix, 'as_suffix')
            
            if suffix_gloss:
                g1 = get_morpheme_gloss(m1) or '?'
                g2 = get_morpheme_gloss(m2) or '?'
                
                return CompoundStructure(
                    morphemes=[m1, m2, suffix],
                    segmentation=f"{m1}-{m2}-{suffix}",
                    bracketing=f"({m1}-{m2})-{suffix}",
                    compositional_gloss=f"({g1}-{g2})-{suffix_gloss}",
                    lexical_gloss=None,
                    head_position='left'
                )
    
    return None


def analyze_possessive(word: str) -> Optional[Tuple[str, str]]:
    """
    Consolidated handler for all possessive (') patterns.
    
    This function replaces the previous triple possessive handling blocks
    that were scattered through analyze_word(). All possessive logic is
    now in one place, making it easier to maintain and extend.
    
    Args:
        word: The word to analyze (may or may not end in ')
        
    Returns:
        (segmentation, gloss) tuple if word is possessive, None otherwise
        
    Examples:
        >>> analyze_possessive("Pasian'")
        ("Pasian'", 'God.POSS')
        >>> analyze_possessive("gilote'")
        ("gilote'", 'enemy-PL.POSS')
        >>> analyze_possessive("hello")
        None
    """
    # Only handle words ending in possessive marker
    if not (word.endswith("'") or word.endswith("\u2019")):
        return None
    
    base = word.rstrip("'\u2019")
    if not base:
        return None
    
    base_lower = base.lower()
    base_title = base.title()
    
    # 1. Transparent proper nouns (Pasian' → God.POSS, Topa' → Lord.POSS)
    if base and base[0].isupper() and base_title in TRANSPARENT_PROPER_NOUNS:
        seg, gloss = TRANSPARENT_PROPER_NOUNS[base_title]
        return (f"{seg}'", f"{gloss}.POSS")
    
    # 2. Opaque proper nouns (Jerusalem' → JERUSALEM.POSS)
    if base_title in PROPER_NOUNS or base in PROPER_NOUNS:
        return (f"{base}'", f"{base_title.upper()}.POSS")
    
    # 3. Function words (tua' → DIST.POSS)
    if base_lower in FUNCTION_WORDS:
        return (f"{base}'", f"{FUNCTION_WORDS[base_lower]}.POSS")
    
    # 4. Direct noun stems (pa' → father.POSS)
    if base_lower in NOUN_STEMS:
        return (f"{base}'", f"{NOUN_STEMS[base_lower]}.POSS")
    
    # 5. Plural forms ending in -te (gilote' → enemy-PL.POSS)
    if base_lower.endswith('te') and len(base_lower) > 2:
        stem = base_lower[:-2]
        # Check all lexicons for the stem
        if stem in NOUN_STEMS:
            return (f"{base}'", f"{NOUN_STEMS[stem]}-PL.POSS")
        if stem in ATOMIC_GLOSSES:
            return (f"{base}'", f"{ATOMIC_GLOSSES[stem]}-PL.POSS")
        if stem in VERB_STEMS:
            return (f"{base}'", f"{VERB_STEMS[stem]}-PL.POSS")
        # Proper noun plurals (Israelite' → ISRAEL-PL.POSS)
        stem_title = stem.title()
        if stem_title in PROPER_NOUNS:
            return (f"{base}'", f"{stem_title.upper()}-PL.POSS")
    
    # 6. Agent nominalizer forms ending in -pa (veipa' → do-NMLZ.AG.POSS)
    if base_lower.endswith('pa') and len(base_lower) > 2:
        stem = base_lower[:-2]
        if stem in VERB_STEMS:
            return (f"{stem}-pa'", f"{VERB_STEMS[stem]}-NMLZ.AG.POSS")
    
    # 7. Common possessive words (hard-coded for high frequency items)
    # These are kept for efficiency - they're checked before expensive recursion
    poss_map = {
        'amau': '3PL.POSS',
        # Note: mite should be analyzed as mi-te (person-PL), not possessive
        'note': '2PL.POSS',
        'amaute': '3PL.POSS',
        'kumpipa': 'king.POSS',
        'kei': '1SG.POSS',
        'kote': '1PL.POSS',
        'eite': '1PL.EXCL.POSS',
        'khempeuh': 'all.POSS',
        'nang': '2SG.POSS',
        'kan': '1SG.POSS',
    }
    if base_lower in poss_map:
        return (f"{base}'", poss_map[base_lower])
    
    # 8. Try COMPOUND_WORDS for explicit entries
    if base_lower in COMPOUND_WORDS:
        seg, gloss = COMPOUND_WORDS[base_lower]
        return (f"{seg}'", f"{gloss}.POSS")
    
    # 9. Recursive analysis - analyze base and add .POSS
    # Import here to avoid circular dependency issues
    base_seg, base_gloss = _analyze_word_internal(base)
    if base_gloss and '?' not in base_gloss:
        return (f"{base_seg}'", f"{base_gloss}.POSS")
    
    # No possessive analysis found
    return None


# Forward declaration for recursive calls within analyze_possessive
# This will be set to analyze_word after it's defined
_analyze_word_internal = None


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
    
    # Handle pure numbers (years, verse numbers in metadata)
    if word.isdigit():
        return (word, 'NUM')
    
    # Handle URLs and URL fragments (metadata artifacts)
    if word.startswith('http://') or word.startswith('https://') or word.startswith('//www') or word.startswith('com/'):
        return (word, 'URL')
    
    # Normalize curly apostrophes to straight apostrophes for dictionary lookups
    word = word.replace('\u2019', "'").replace('\u2018', "'")
    
    # Normalize hyphens - try without hyphens first for morphological analysis
    # This handles cases like 'ki-ap' vs 'kiap', 'pua-in' vs 'puain'
    word_no_hyphen = word.replace('-', '')
    
    # Check function words FIRST (before proper noun check)
    # This ensures 'Tua' (sentence-initial 'that') isn't treated as proper noun
    word_lower = word.lower()
    word_no_hyphen_lower = word_no_hyphen.lower()
    
    # Check for ambiguous morphemes FIRST - use context-appropriate meaning
    # For standalone words, use default (first) meaning from AMBIGUOUS_MORPHEMES
    if word_lower in AMBIGUOUS_MORPHEMES:
        # Standalone word - use context-based disambiguation
        # For 'za' standalone, prefer 'hear' (more common in Bible)
        # For 'la' standalone, prefer 'take' (most common)
        # For 'na' standalone, prefer '2SG' (suffix handled separately)
        meaning = disambiguate_morpheme(word_lower, {'position': 'standalone'})
        if meaning:
            return (word, meaning)
    
    # Check METADATA_WORDS - English words in file headers (not Tedim text)
    if word_lower in METADATA_WORDS:
        return (word, METADATA_WORDS[word_lower])
    
    # Check OPAQUE LEXEMES early - these are words that LOOK decomposable
    # but have non-compositional meanings (e.g., sanggam = 'brother' NOT 'high-land')
    # This check uses the refactored morphology/opaque.py module
    if is_opaque(word_lower):
        gloss_tuple = get_opaque_gloss(word_lower)
        if gloss_tuple:
            return gloss_tuple
    if is_opaque(word_no_hyphen_lower):
        gloss_tuple = get_opaque_gloss(word_no_hyphen_lower)
        if gloss_tuple:
            return gloss_tuple
    
    # Try both hyphenated and unhyphenated forms (also check original case for sentence-initial words)
    if word in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word])
    if word_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_lower])
    if word_no_hyphen_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_no_hyphen_lower])
    
    # Handle possessive marker ' at end of word BEFORE proper noun check
    # This ensures Pasian' → God.POSS not PASIAN'
    # (Consolidated in analyze_possessive function)
    poss_result = analyze_possessive(word)
    if poss_result:
        return poss_result
    
    # Check for transparent proper nouns (Tedim words used as proper nouns)
    # Only match if word is capitalized - lowercase should use common noun glosses
    # These show Tedim morphology instead of opaque ALL-CAPS
    # Note: Possessive forms (Pasian', Topa') are handled by analyze_possessive above
    if word and word[0].isupper():
        word_title = word.title()
        if word_title in TRANSPARENT_PROPER_NOUNS:
            return TRANSPARENT_PROPER_NOUNS[word_title]
    
    # Check if proper noun (only AFTER function words and possessive check)
    if is_proper_noun(word):
        return (word, word.upper())
    
    # Check for proper noun + suffix patterns (israel-te, jerusalem-ah, etc.)
    # Also handle possessive forms like Israel-te' (Israel's people)
    proper_suffixes = {
        "-te'": 'PL.POSS',  # plural possessive
        "-te'": 'PL.POSS',  # plural possessive (curly quote)
        '-te': 'PL',        # plural
        '-pa': 'man',       # man/person (e.g., Filistia-pa = Philistine man)
        '-ah': 'LOC',       # locative  
        '-a': 'LOC',        # short locative
        '-in': 'ERG',       # ergative
        "te'": 'PL.POSS',   # without hyphen
        "te'": 'PL.POSS',   # without hyphen (curly quote)
        'te': 'PL',         # without hyphen
        'pa': 'man',        # without hyphen
        'ah': 'LOC',        # without hyphen
    }
    for suffix, gloss in longest_first(proper_suffixes):
        if word_lower.endswith(suffix):
            base = word[:-len(suffix)]
            base_clean = base.rstrip('-')  # Remove trailing hyphen if present
            base_lower = base_clean.lower()
            base_title = base_clean.title()
            # Only treat as proper noun if base is in PROPER_NOUNS AND
            # lowercase base is NOT a known common word
            if (base_title in PROPER_NOUNS or base_clean in PROPER_NOUNS):
                # Skip if lowercase form is a known common word (in any lexicon)
                if is_known_word(base_lower):
                    continue  # Let it fall through to COMPOUND_WORDS
                return (f"{base_clean}-{suffix.lstrip('-')}", f"{base_title.upper()}-{gloss}")
    
    # Note: Main possessive handling removed - now handled by analyze_possessive() 
    # called at line 9752 above
    
    # Polysemous reduplication disambiguation - explicit entries for reduplicated forms
    # where the base stem has multiple meanings and we need a specific one
    REDUP_DISAMBIGUATION = {
        'bangbang': ('bang~bang', 'what~REDUP'),      # "whatever" (not god~REDUP)
        'kawikawi': ('kawi~kawi', 'crooked~REDUP'),   # "to and fro" (not kis~REDUP)
        'vanvan': ('van~van', 'old~REDUP'),           # "ancient" (not sky~REDUP)
        'veivei': ('vei~vei', 'time~REDUP'),          # "at one time" (not sick~REDUP)
        'pakpak': ('pak~pak', 'quick~REDUP'),         # "swift" (not flower~REDUP)
        'thuahthuah': ('thuah~thuah', 'break~REDUP'), # "breach upon breach" (not house~REDUP)
        'thumthum': ('thum~thum', 'mourn~REDUP'),     # "mourn sore" (not three~REDUP)
        'sensen': ('sen~sen', 'distinguish~REDUP'),   # "distinction" (not hide~REDUP)
        'lellel': ('lel~lel', 'mere~REDUP'),          # "mere" (not laugh~REDUP)
        'lumlum': ('lum~lum', 'sleep~REDUP'),         # "sleep" (not warm~REDUP)
        'khangkhang': ('khang~khang', 'generation~REDUP'),  # "from generation" (not increase~REDUP)
        'behbeh': ('beh~beh', 'tribe~REDUP'),         # "by tribes" (not count~REDUP)
        'thenthen': ('then~then', 'thousand~REDUP'),  # "thousands" (not multiply~REDUP)
    }
    
    # Check disambiguation first for polysemous reduplicated forms
    word_clean = word.lower().replace('-', '')
    if word_clean in REDUP_DISAMBIGUATION:
        return REDUP_DISAMBIGUATION[word_clean]
    
    # Round 154: Early reduplication check (X-X patterns like hathat, kilhkilh)
    half_len = len(word_clean) // 2
    if len(word_clean) >= 4 and len(word_clean) % 2 == 0:
        first_half = word_clean[:half_len]
        second_half = word_clean[half_len:]
        if first_half == second_half:
            # Check if base is a known stem
            if first_half in VERB_STEMS:
                return (f"{first_half}~{first_half}", f"{VERB_STEMS[first_half]}~REDUP")
            elif first_half in NOUN_STEMS:
                return (f"{first_half}~{first_half}", f"{NOUN_STEMS[first_half]}~REDUP")
            # Try lexicon lookup for base
            lex_gloss = lookup_lexicon(first_half)
            if lex_gloss:
                return (f"{first_half}~{first_half}", f"{lex_gloss}~REDUP")
    

    # COMPOUND_WORDS moved to morphology/compounds.py for maintainability



    # Check compound words FIRST for explicit overrides
    # This allows COMPOUND_WORDS entries to override hierarchical analysis
    # when a specific form needs a different gloss than what hierarchical produces
    if word_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_lower]
    if word_no_hyphen_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_no_hyphen_lower]
    
    # Try hierarchical compound analysis (Round 181 fix, Round 193m improvements)
    # This handles lexicalized compounds with proper semantic glosses:
    # - BINARY_COMPOUNDS: lungdam → 'joy', suanghawm → 'cave'
    # - TERNARY_COMPOUNDS: singnamtui → 'spices'
    # - Step 3/4 now use lexical glosses (e.g., suanghawmte → cave-PL, not stone-counsel-PL)
    hier_result = analyze_hierarchical_compound(word_no_hyphen_lower)
    if hier_result[0]:
        return hier_result
    
    # Handle explicit hyphen before grammatical suffixes (e.g., lauhuai-in, muanhuai-ah)
    # These are written with explicit hyphen before -in (ERG), -ah (LOC), -a (LOC)
    HYPHEN_SUFFIXES = {
        "-a'": 'GEN',      # possessive/genitive with curly quote
        "-a\u2019": 'GEN', # possessive/genitive with curly quote (unicode)
        '-in': 'ERG',
        '-ah': 'LOC', 
        '-un': 'IMP',      # imperative plural
        '-a': 'LOC',
    }
    for hyph_suffix, suffix_gloss in longest_first(HYPHEN_SUFFIXES):
        if word_lower.endswith(hyph_suffix) or word.endswith(hyph_suffix):
            stem = word[:-len(hyph_suffix)]
            stem_result = analyze_word(stem)
            if stem_result and stem_result[1] and '?' not in stem_result[1]:
                # Stem fully analyzed, combine with suffix
                return (f"{stem_result[0]}{hyph_suffix}", f"{stem_result[1]}-{suffix_gloss}")
    
    # Check noun stems (try both forms)
    if word in NOUN_STEMS:
        return (word, NOUN_STEMS[word])
    if word_no_hyphen in NOUN_STEMS:
        return (word, NOUN_STEMS[word_no_hyphen])
    if word_no_hyphen_lower in NOUN_STEMS:
        return (word, NOUN_STEMS[word_no_hyphen_lower])
    
    # Check verb stems (try both forms)
    if word in VERB_STEMS:
        return (word, VERB_STEMS[word])
    if word_no_hyphen in VERB_STEMS:
        return (word, VERB_STEMS[word_no_hyphen])
    if word_no_hyphen_lower in VERB_STEMS:
        return (word, VERB_STEMS[word_no_hyphen_lower])
    
    # Check for Form II verb stems (Henderson 1965: subjunctive forms)
    # Form II is used in inconclusive sentences and adjunctive phrases
    if word_no_hyphen_lower in VERB_STEM_PAIRS:
        form_i, base_gloss = VERB_STEM_PAIRS[word_no_hyphen_lower]
        return (word, base_gloss)  # Return base gloss (form is grammatical, not lexical)
    
    # For morphological decomposition, use the unhyphenated form
    segments = []
    glosses = []
    remaining = word_no_hyphen
    
    # 1. Check for pronominal prefix
    # Round 188 fix: Don't strip single-char prefixes if remaining would start with
    # a consonant cluster that suggests a longer stem (e.g., 'innpiah' starts with 'inn')
    remaining_lower = remaining.lower()
    for prefix, gloss in longest_first(OBJECT_PREFIXES):
        if remaining_lower.startswith(prefix):
            segments.append(prefix)
            glosses.append(gloss)
            remaining = remaining[len(prefix):]
            break
    else:
        for prefix, gloss in longest_first(PRONOMINAL_PREFIXES):
            if remaining_lower.startswith(prefix) and len(remaining) > len(prefix):
                # Check if stripping prefix would leave a phonotactically invalid onset
                # or if a longer stem exists (e.g., 'inn' vs 'i' + 'nn')
                after_prefix = remaining[len(prefix):]
                after_prefix_lower = after_prefix.lower()
                # Skip if remainder starts with doubled consonant (suggests it's part of stem)
                if len(after_prefix) >= 2 and after_prefix[0] == after_prefix[1] and after_prefix[0].isalpha():
                    continue
                # Skip if the full word is a known stem (don't include function words)
                if remaining_lower in NOUN_STEMS or remaining_lower in VERB_STEMS:
                    continue
                # Check for known longer stems starting with the prefix
                longer_stem_found = False
                for stem in list(NOUN_STEMS.keys()) + list(VERB_STEMS.keys()):
                    if remaining_lower.startswith(stem) and len(stem) > len(prefix):
                        longer_stem_found = True
                        break
                if longer_stem_found:
                    continue
                segments.append(prefix)
                glosses.append(gloss)
                remaining = remaining[len(prefix):]
                break
    
    # 1b. Check for reflexive/reciprocal ki- prefix
    if remaining.lower().startswith('ki') and len(remaining) > 2:
        ki_base = remaining[2:]
        # Check if base is a known verb stem
        ki_base_lower = ki_base.lower()
        # First try full compound forms
        full_ki_word = remaining.lower()
        if full_ki_word in VERB_STEMS:
            segments.append(remaining)
            glosses.append(VERB_STEMS[full_ki_word])
            remaining = ''
        elif ki_base_lower in VERB_STEMS:
            segments.append('ki')
            glosses.append('REFL')
            segments.append(ki_base)
            glosses.append(VERB_STEMS[ki_base_lower])
            remaining = ''
        elif ki_base_lower in NOUN_STEMS:
            segments.append('ki')
            glosses.append('REFL')
            segments.append(ki_base)
            glosses.append(NOUN_STEMS[ki_base_lower])
            remaining = ''
        else:
            # Try suffix stripping on ki- base
            for suffix in ['sak', 'pih', 'khiat', 'khia', 'tak', 'kik', 'zo', 'ta']:
                if ki_base_lower.endswith(suffix) and len(ki_base_lower) > len(suffix):
                    base_before_suffix = ki_base_lower[:-len(suffix)]
                    if base_before_suffix in VERB_STEMS:
                        segments.append('ki')
                        glosses.append('REFL')
                        segments.append(base_before_suffix)
                        glosses.append(VERB_STEMS[base_before_suffix])
                        suffix_glosses_map = {
                            'sak': 'CAUS', 'pih': 'APPL', 'khiat': 'AWAY',
                            'khia': 'AWAY', 'tak': 'firmly', 'kik': 'ITER',
                            'zo': 'COMPL', 'ta': 'PFV'
                        }
                        segments.append(suffix)
                        glosses.append(suffix_glosses_map.get(suffix, suffix))
                        remaining = ''
                        break
    
    # 2. Check for verb/noun stem (Round 154: prefer longest match across both dicts)
    # Round 189: Bug 10 fix - Don't accept short stem matches if remainder is unparseable
    stem_found = False
    remaining_lower = remaining.lower()
    
    # Helper function to check if a remainder is parseable
    def is_remainder_parseable(remainder_text):
        """Check if the remainder after stem extraction can be parsed."""
        if not remainder_text:
            return True  # Empty remainder is fine
        rem_lower = remainder_text.lower()
        # Check if remainder is a known suffix/TAM/case marker
        if rem_lower in TAM_SUFFIXES or rem_lower in CASE_MARKERS or rem_lower in NOMINALIZERS:
            return True
        # Check if remainder is a known stem (N+N compound)
        # Use is_known_stem, not is_known_word, to avoid matching function words
        if is_known_stem(rem_lower) or rem_lower in ATOMIC_GLOSSES:
            return True
        # Check if remainder starts with known stem (stem+suffix pattern)
        # This handles cases like "neihna" = neih-na
        for stem in longest_keys_first(VERB_STEMS):
            if rem_lower.startswith(stem) and len(rem_lower) > len(stem):
                suffix_part = rem_lower[len(stem):]
                if suffix_part in TAM_SUFFIXES or suffix_part in NOMINALIZERS or suffix_part in CASE_MARKERS:
                    return True
                # Also check for common grammatical suffixes
                if suffix_part in ['te', 'na', 'in', 'ah', 'ding', 'zo', 'ta', 'sak', 'pih']:
                    return True
        for stem in longest_keys_first(NOUN_STEMS):
            if rem_lower.startswith(stem) and len(rem_lower) > len(stem):
                suffix_part = rem_lower[len(stem):]
                if suffix_part in TAM_SUFFIXES or suffix_part in NOMINALIZERS or suffix_part in CASE_MARKERS:
                    return True
                if suffix_part in ['te', 'na', 'in', 'ah', 'ding']:
                    return True
        # Check if remainder starts with known suffix chain
        for suf in longest_keys_first(TAM_SUFFIXES):
            if rem_lower.startswith(suf):
                return True
        for suf in longest_keys_first(CASE_MARKERS):
            if rem_lower.startswith(suf):
                return True
        # Check for common verb suffixes
        verb_suffixes = ['sak', 'pih', 'khiat', 'khia', 'tak', 'kik', 'zo', 'ta', 'na', 'te']
        for suf in verb_suffixes:
            if rem_lower.startswith(suf):
                return True
        return False
    
    # Find best verb stem match
    best_verb = None
    for stem, gloss in longest_first(VERB_STEMS):
        if remaining_lower.startswith(stem):
            # Round 189: For short stems (<=3 chars), verify remainder is parseable
            if len(stem) <= 3:
                remainder_after = remaining_lower[len(stem):]
                if remainder_after and not is_remainder_parseable(remainder_after):
                    continue  # Skip this short stem, try next
            best_verb = (stem, gloss)
            break
    
    # Find best noun stem match  
    best_noun = None
    for stem, gloss in longest_first(NOUN_STEMS):
        if remaining_lower.startswith(stem):
            # Round 189: For short stems (<=3 chars), verify remainder is parseable
            if len(stem) <= 3:
                remainder_after = remaining_lower[len(stem):]
                if remainder_after and not is_remainder_parseable(remainder_after):
                    continue  # Skip this short stem, try next
            best_noun = (stem, gloss)
            break
    
    # Find best Form II verb stem match (Henderson 1965)
    best_form_ii = None
    for stem, (form_i, gloss) in longest_first(VERB_STEM_PAIRS):
        if remaining_lower.startswith(stem):
            # Check for disambiguation - some Form II stems conflict with stem+suffix patterns
            if stem in FORM_II_DISAMBIGUATION:
                disamb = FORM_II_DISAMBIGUATION[stem]
                base_stem, _ = disamb['conflicts_with']
                suffix_in_word = remaining_lower[len(base_stem):]  # What comes after Form I stem
                # If followed by a suffix that suggests segmented form, skip this Form II match
                if any(suffix_in_word.startswith(suf) for suf in disamb['prefer_segmented_when']):
                    continue  # Don't use this Form II stem, let stem+suffix win
            
            # Check if Form I + known suffix gives a better parse
            # E.g., for "mukik": prefer mu (Form I) + kik (ITER) over muk (Form II) + ik (?)
            suffix_after_form_ii = remaining_lower[len(stem):]
            if suffix_after_form_ii and suffix_after_form_ii not in TAM_SUFFIXES:
                # Check if Form I + suffix would be valid
                suffix_after_form_i = remaining_lower[len(form_i):]
                if suffix_after_form_i in TAM_SUFFIXES:
                    # Form I parse is better - skip this Form II
                    continue
            
            best_form_ii = (stem, gloss)
            break
    
    # Find best ATOMIC_GLOSSES stem match
    # This ensures stems like 'taang' (beautiful) in ATOMIC_GLOSSES
    # are considered alongside stems in VERB_STEMS/NOUN_STEMS,
    # preventing conflicts where shorter stems (e.g., 'taan') intercept
    # longer atomic stems (e.g., 'taang' in 'taangsak')
    best_atomic = None
    for stem, gloss in longest_first(ATOMIC_GLOSSES):
        if remaining_lower.startswith(stem):
            # For short stems (<=3 chars), verify remainder is parseable
            if len(stem) <= 3:
                remainder_after = remaining_lower[len(stem):]
                if remainder_after and not is_remainder_parseable(remainder_after):
                    continue  # Skip this short stem, try next
            best_atomic = (stem, gloss)
            break
    
    # Choose the longest match (prefer Form II > atomic > noun > verb for ties)
    # Priority order ensures longest match wins; for ties, prefer:
    # - Form II (inflected verb forms)
    # - Atomic glosses (bound morphemes that form compounds)
    # - Noun stems
    # - Verb stems
    candidates = [(best_form_ii, 0), (best_atomic, 1), (best_noun, 2), (best_verb, 3)]
    candidates = [(c, p) for c, p in candidates if c is not None]
    if candidates:
        # Sort by length (descending), then priority (ascending)
        candidates.sort(key=lambda x: (-len(x[0][0]), x[1]))
        stem, gloss = candidates[0][0]
        # Track whether we selected a Form II stem
        is_form_ii_stem = (candidates[0][1] == 0)  # Priority 0 = Form II
    else:
        stem, gloss = None, None
        is_form_ii_stem = False
    
    if stem:
        segments.append(stem)
        # Add .II marker for Form II stems (Henderson 1965)
        if is_form_ii_stem:
            glosses.append(f"{gloss}.II")
        else:
            glosses.append(gloss)
        remaining = remaining[len(stem):]
        stem_found = True
    
    # 3. Check for suffixes on remaining
    if remaining:
        # === Round 154: Enhanced suffix chain parsing ===
        # Process suffix chain iteratively (e.g., -kik-in, -na-teng, etc.)
        suffix_processed = True
        while remaining and suffix_processed:
            suffix_processed = False
            remaining_lower = remaining.lower()
            
            # Combine TAM_SUFFIXES and CASE_MARKERS for unified length-sorted iteration
            # This ensures longer suffixes like 'panin' (ABL) are checked before shorter
            # ones like 'nin' (ERG variant), preventing incorrect segmentation like
            # gam-pa-nin instead of gam-panin
            # Use STRIPPABLE_SUFFIXES which combines TAM, derivational, and case suffixes
            # This ensures proper linguistic categorization while allowing unified suffix stripping
            
            # Check combined suffixes (longest first)
            for suffix, gloss in longest_first(STRIPPABLE_SUFFIXES):
                if remaining_lower == suffix:
                    segments.append(suffix)
                    # Round 196: Disambiguate -in: CVB after verb stems, ERG after nouns
                    # When -in directly follows a verb stem (no nominalizer), it marks
                    # same-subject sequential action (converb), not ergative case
                    if suffix == 'in' and segments:
                        prev_seg = segments[-2].lower() if len(segments) >= 2 else ''
                        prev_gloss = glosses[-1] if glosses else ''
                        # Check if previous segment is a verb stem or verb-based
                        is_prev_verb = (prev_seg in VERB_STEMS or 
                                       prev_seg in VERB_STEM_PAIRS or
                                       any(v in prev_gloss for v in ['CAUS', 'ITER', 'ABIL', 'APPL', 'REFL', 'RECP']))
                        if is_prev_verb:
                            glosses.append('CVB')  # Same-subject converb marker
                        else:
                            glosses.append(gloss)
                    # Round 197: Disambiguate -sak: BENF after Form II, CAUS otherwise
                    elif suffix == 'sak' and segments:
                        prev_seg = segments[-2].lower() if len(segments) >= 2 else ''
                        prev_gloss = glosses[-1] if glosses else ''
                        # Check if previous segment is Form II verb stem
                        is_form_ii = prev_seg in VERB_STEM_PAIRS or '.II' in prev_gloss
                        if is_form_ii:
                            glosses.append('BENF')  # Benefactive (Form II + sak)
                        else:
                            glosses.append(gloss)
                    else:
                        glosses.append(gloss)
                    remaining = ''
                    suffix_processed = True
                    break
                elif remaining_lower.endswith(suffix) and len(remaining) > len(suffix):
                    # Strip suffix from end and check if what remains is valid
                    base = remaining[:-len(suffix)]
                    base_lower = base.lower()
                    # Check if base is a known stem, Form II verb, or another strippable suffix
                    if is_known_word(base_lower) or base_lower in STRIPPABLE_SUFFIXES:
                        segments.append(base)
                        is_form_ii = False  # Track if base is Form II
                        if base_lower in CASE_MARKERS:
                            # Prioritize case marker reading for suffix position
                            glosses.append(CASE_MARKERS[base_lower])
                        elif base_lower in VERB_STEMS:
                            glosses.append(VERB_STEMS[base_lower])
                        elif base_lower in NOUN_STEMS:
                            glosses.append(NOUN_STEMS[base_lower])
                        elif base_lower in VERB_STEM_PAIRS:
                            form_i, base_gloss = VERB_STEM_PAIRS[base_lower]
                            glosses.append(f"{base_gloss}.II")  # Mark Form II
                            is_form_ii = True
                        elif base_lower in STRIPPABLE_SUFFIXES:
                            glosses.append(STRIPPABLE_SUFFIXES[base_lower])
                        elif base_lower in ATOMIC_GLOSSES:
                            glosses.append(ATOMIC_GLOSSES[base_lower])
                        elif base_lower in FUNCTION_WORDS:
                            glosses.append(FUNCTION_WORDS[base_lower])
                        else:
                            glosses.append('?')  # Shouldn't happen, but safe fallback
                        segments.append(suffix)
                        # Disambiguate -in: CVB after verb stems, ERG after nouns
                        if suffix == 'in' and (base_lower in VERB_STEMS or base_lower in VERB_STEM_PAIRS):
                            glosses.append('CVB')  # Converb (same-subject sequential)
                        # Disambiguate -sak: BENF after Form II, CAUS after Form I/nouns
                        elif suffix == 'sak' and is_form_ii:
                            glosses.append('BENF')  # Benefactive (Form II + sak)
                        else:
                            glosses.append(gloss)
                        remaining = ''
                        suffix_processed = True
                        break
        
        # Check final particles (only exact match)
        if remaining:
            for particle, gloss in FINAL_PARTICLES.items():
                if remaining.lower() == particle:
                    segments.append(particle)
                    glosses.append(gloss)
                    remaining = ''
                    break
        
        # Check nominalizers
        if remaining:
            for nom, gloss in NOMINALIZERS.items():
                # Case 1: remaining IS exactly the nominalizer (after stem extraction)
                if remaining.lower() == nom:
                    segments.append(nom)
                    glosses.append(gloss)
                    remaining = ''
                    break
                # Case 2: remaining has a base + nominalizer
                if remaining.lower().endswith(nom) and len(remaining) > len(nom):
                    base = remaining[:-len(nom)]
                    base_lower = base.lower()
                    # Check if base is a known stem (including Form II verbs)
                    if base_lower in VERB_STEMS:
                        segments.append(base)
                        glosses.append(VERB_STEMS[base_lower])
                    elif base_lower in NOUN_STEMS:
                        segments.append(base)
                        glosses.append(NOUN_STEMS[base_lower])
                    elif base_lower in VERB_STEM_PAIRS:
                        # Form II verb (Henderson 1965)
                        form_i, base_gloss = VERB_STEM_PAIRS[base_lower]
                        segments.append(base)
                        glosses.append(base_gloss)
                    elif base_lower in TAM_SUFFIXES:
                        segments.append(base)
                        glosses.append(TAM_SUFFIXES[base_lower])
                    else:
                        segments.append(base)
                        glosses.append('?')  # Unknown base
                    segments.append(nom)
                    glosses.append(gloss)
                    remaining = ''
                    break
    
    # Special handling: if no decomposition, try suffix stripping
    if remaining and not segments:
        # First, try reduplication patterns (X-X)
        half_len = len(remaining) // 2
        if len(remaining) >= 4 and len(remaining) % 2 == 0:
            first_half = remaining[:half_len].lower()
            second_half = remaining[half_len:].lower()
            if first_half == second_half:
                # Check if base is a known stem
                if first_half in VERB_STEMS:
                    return (f"{first_half}~{first_half}", f"{VERB_STEMS[first_half]}~REDUP")
                elif first_half in NOUN_STEMS:
                    return (f"{first_half}~{first_half}", f"{NOUN_STEMS[first_half]}~REDUP")
                else:
                    # Try lexicon lookup for base
                    lex_gloss = lookup_lexicon(first_half)
                    if lex_gloss:
                        return (f"{first_half}~{first_half}", f"{lex_gloss}~REDUP")
                    else:
                        return (f"{first_half}~{first_half}", f"?~REDUP")
        
        # === ENHANCED SUFFIX CHAIN PARSING (Round 154) ===
        # Extended suffix list with verbal aspect/ability markers
        suffix_glosses = {
            # Verbal ability/potential suffixes
            'thei': 'ABIL',     # ability/potential (can/able to)
            'theih': 'ABIL',    # variant form
            'zo': 'able',       # abilitative (capable of)
            # Aspect/directional suffixes
            'gawp': 'INTENS',   # intensive (forcefully/thoroughly)
            'khin': 'INTENS',   # intensive variant
            'kik': 'ITER',      # iterative (again)
            'pih': 'APPL',      # applicative (with/for)
            'khawm': 'COM',     # comitative (together)
            'khia': 'EXIT',     # directional (out)
            'lut': 'ENTER',     # directional (into)
            'toh': 'up',        # directional (up)
            'to': 'CONT',       # continuative
            # Other verbal suffixes
            'sak': 'CAUS',      # causative
            'sa': 'PERF',       # perfective
            'ta': 'PERF',       # perfective variant (completed action)
            'mang': 'COMPL',    # completive
            'khol': 'INTENS',   # intensifier
            'san': 'at',        # locative
            'pen': 'TOP',       # topic/superlative
            # Nominal suffixes
            'na': 'NMLZ',       # nominalizer
            'te': 'PL',         # noun plural
            'uh': '2/3PL',      # 2nd/3rd person plural agreement
            'pan': 'ABL',       # ablative "from"
            'in': 'ERG',        # ergative
            'ah': 'LOC',        # locative
        }
        
        # Try suffix stripping with RECURSIVE analysis of base
        for suffix, suf_gloss in longest_first(suffix_glosses):
            if remaining.lower().endswith(suffix) and len(remaining) > len(suffix) + 1:
                base = remaining[:-len(suffix)]
                base_lower = base.lower()
                
                # First check direct stem lookups (fast path)
                # Round 191: ATOMIC_GLOSSES takes priority - curated glosses override lexicon
                # Round 196: Disambiguate -in as CVB (converb) after verb stems, ERG after nouns
                # When -in attaches directly to a verb stem without nominalizer, it marks
                # same-subject sequential action (converb), not ergative case
                def get_suffix_gloss_for_stem(suffix, suf_gloss, is_verb_base, is_form_ii=False):
                    """Disambiguate suffix glosses based on stem type.
                    
                    -in: CVB (converb) after verbs, ERG after nouns
                    -sak: BENF (benefactive) after Form II, CAUS (causative) after Form I/nouns
                    
                    Based on Otsuka (2009): Form I + -sak = causative, Form II + -sak = benefactive
                    """
                    if suffix == 'in' and is_verb_base:
                        return 'CVB'  # Same-subject converb marker
                    if suffix == 'sak' and is_verb_base and is_form_ii:
                        return 'BENF'  # Benefactive (Form II + -sak)
                    return suf_gloss
                
                if base_lower in ATOMIC_GLOSSES:
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, base_lower in VERB_STEMS, base_lower in VERB_STEM_PAIRS)
                    return (f"{base}-{suffix}", f"{ATOMIC_GLOSSES[base_lower]}-{final_suf_gloss}")
                elif base_lower in VERB_STEMS:
                    # Form I verb stem - CAUS for -sak
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, True, False)
                    return (f"{base}-{suffix}", f"{VERB_STEMS[base_lower]}-{final_suf_gloss}")
                elif base_lower in NOUN_STEMS:
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, False, False)
                    return (f"{base}-{suffix}", f"{NOUN_STEMS[base_lower]}-{final_suf_gloss}")
                # Check Form II verb stems (Henderson 1965)
                elif base_lower in VERB_STEM_PAIRS:
                    form_i, base_gloss = VERB_STEM_PAIRS[base_lower]
                    # Form II verb stem - BENF for -sak
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, True, True)
                    return (f"{base}-{suffix}", f"{base_gloss}.II-{final_suf_gloss}")
                
                # Lexicon lookup as fallback (for words not in curated dictionaries)
                lex_gloss = lookup_lexicon(base_lower)
                if lex_gloss:
                    # Check if lexicon entry is a verb (heuristic: look for typical verb glosses)
                    is_verb_lex = any(v_ind in lex_gloss.lower() for v_ind in ['go', 'come', 'make', 'give', 'take', 'say', 'see', 'hear', 'do', 'put', 'get'])
                    # Lexicon doesn't track Form I/II, default to Form I (CAUS)
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, is_verb_lex, False)
                    return (f"{base}-{suffix}", f"{lex_gloss}-{final_suf_gloss}")
                
                # RECURSIVE: Try analyzing the base as a complex form
                # This handles chains like verb-CAUS-ITER, ki-verb-ABIL, etc.
                base_seg, base_gloss = analyze_word(base)
                if '?' not in base_gloss:
                    # Base is fully analyzable - combine with suffix
                    # Check if recursive analysis indicates a verb base (contains verb glosses)
                    is_verb_base = any(v_ind in base_gloss for v_ind in ['CAUS', 'ITER', 'ABIL', 'APPL', 'REFL', 'RECP'])
                    is_verb_base = is_verb_base or base_lower.startswith('ki') or base_lower in VERB_STEMS
                    # Check if Form II by looking for .II marker in gloss
                    is_form_ii = '.II' in base_gloss
                    final_suf_gloss = get_suffix_gloss_for_stem(suffix, suf_gloss, is_verb_base, is_form_ii)
                    return (f"{base_seg}-{suffix}", f"{base_gloss}-{final_suf_gloss}")
        
        # === KI- REFLEXIVE PREFIX HANDLING (Round 154) ===
        # Handle ki- prefix with recursive analysis of remainder
        remaining_lower = remaining.lower()
        if remaining_lower.startswith('ki') and len(remaining_lower) > 3:
            ki_base = remaining[2:]
            ki_base_lower = ki_base.lower()
            
            # Check direct stem lookups first
            if ki_base_lower in VERB_STEMS:
                return (f"ki-{ki_base}", f"REFL-{VERB_STEMS[ki_base_lower]}")
            
            # Try recursive analysis of the base
            base_seg, base_gloss = analyze_word(ki_base)
            if '?' not in base_gloss:
                return (f"ki-{base_seg}", f"REFL-{base_gloss}")
    
    # If we still have remaining, add it as unknown
    # Round 187: Check ATOMIC_GLOSSES, NOUN_STEMS, VERB_STEMS before marking as ?
    if remaining:
        if segments:
            remaining_lower = remaining.lower()
            remaining_gloss = None
            # Try to find a gloss for the remaining morpheme
            if remaining_lower in ATOMIC_GLOSSES:
                remaining_gloss = ATOMIC_GLOSSES[remaining_lower]
            elif remaining_lower in NOUN_STEMS:
                remaining_gloss = NOUN_STEMS[remaining_lower]
            elif remaining_lower in VERB_STEMS:
                remaining_gloss = VERB_STEMS[remaining_lower]
            elif remaining_lower in VERB_STEM_PAIRS:
                _, remaining_gloss = VERB_STEM_PAIRS[remaining_lower]
            
            segments.append(remaining)
            glosses.append(remaining_gloss if remaining_gloss else '?')
        else:
            # No decomposition found - try internal glosses BEFORE lexicon
            # Round 191: Priority order matters - our curated glosses override lexicon
            word_lower = word.lower()
            if word_lower in ATOMIC_GLOSSES:
                return (word, ATOMIC_GLOSSES[word_lower])
            elif word_lower in NOUN_STEMS:
                return (word, NOUN_STEMS[word_lower])
            elif word_lower in VERB_STEMS:
                return (word, VERB_STEMS[word_lower])
            elif word_lower in VERB_STEM_PAIRS:
                _, stem_gloss = VERB_STEM_PAIRS[word_lower]
                return (word, stem_gloss)
            # Lexicon as fallback for words we haven't curated
            lexicon_gloss = lookup_lexicon(word_lower)
            if lexicon_gloss:
                return (word, lexicon_gloss)
            segments = [word]
            glosses = ['?']
    
    # Round 197: Distinguish agreement vs possessive for pronominal prefixes
    # Henderson (1965): ka-/na-/a- on verbs = agreement, on nouns = possessive
    # Post-process to change 1SG/2SG/3SG to POSS variants when followed by noun
    if len(segments) >= 2 and len(glosses) >= 2:
        first_seg = segments[0].lower()
        first_gloss = glosses[0]
        second_seg = segments[1].lower()
        second_gloss = glosses[1]
        
        # Check if first segment is a pronominal prefix
        if first_seg in PRONOMINAL_PREFIXES and first_gloss in ['1SG', '2SG', '3SG', '1PL.INCL']:
            # Check if second segment is a noun (not a verb)
            is_noun_following = (second_seg in NOUN_STEMS or 
                                 second_gloss in NOUN_STEMS.values() or
                                 any(nom in second_gloss for nom in ['NMLZ', 'house', 'father', 'mother', 
                                     'child', 'person', 'man', 'woman', 'place', 'thing', 'name', 'day',
                                     'night', 'hand', 'head', 'heart', 'body', 'land', 'water', 'fire']))
            is_verb_following = (second_seg in VERB_STEMS or 
                                 second_seg in VERB_STEM_PAIRS or
                                 any(v_marker in second_gloss for v_marker in ['.II', 'CAUS', 'BENF', 
                                     'APPL', 'ITER', 'ABIL', 'REFL', 'go', 'come', 'see', 'say', 'do', 
                                     'make', 'give', 'take', 'know', 'hear', 'eat', 'drink']))
            
            # If noun follows (and not verb), use possessive gloss
            if is_noun_following and not is_verb_following:
                glosses[0] = first_gloss + '.POSS'
    
    # Build output
    if len(segments) > 1:
        segmented = '-'.join(segments)
        gloss = '-'.join(glosses)
    else:
        segmented = segments[0] if segments else word
        gloss = glosses[0] if glosses else '?'
    
    # Round 189: Trailing punctuation fallback
    # If result contains '?' and word ends with punctuation (comma, period, etc.),
    # try stripping the punctuation and re-analyzing.
    # CAREFUL: Apostrophe ' has grammatical meaning (possessive), so only strip if:
    # - It's clearly a quotation mark (other punctuation follows, or at sentence end)
    # - The stripped version gives a BETTER parse (no '?')
    if '?' in gloss and len(original) > 1:
        trailing_punct = '.,;:!?"'  # Safe to strip (not apostrophe by default)
        if original[-1] in trailing_punct:
            stripped = original.rstrip(trailing_punct)
            if stripped and stripped != original:
                stripped_seg, stripped_gloss = analyze_word(stripped)
                if '?' not in stripped_gloss:
                    return (stripped_seg, stripped_gloss)
        # For trailing apostrophe, only strip if it improves the parse
        # This handles quotation marks at end of quoted speech
        elif original[-1] in "'\u2019" and not original.endswith("te'") and not original.endswith("te\u2019"):
            # Don't strip if it's a plural possessive pattern
            stripped = original.rstrip("'\u2019")
            if stripped and stripped != original and len(stripped) > 1:
                stripped_seg, stripped_gloss = analyze_word(stripped)
                if '?' not in stripped_gloss:
                    return (stripped_seg, stripped_gloss)
    
    # Phonotactic validation: check that all segments have valid onsets
    # This catches segmentation errors like *hto, *kp, *ns, etc.
    # NOTE: We log but don't reject, because:
    # 1. Foreign proper nouns have non-native phonotactics (Jerusalem, Filistia)
    # 2. Some valid coda+onset sequences look like invalid clusters
    # Use audit_phonotactics() to find and manually fix real errors
    if len(segments) > 1:
        is_valid, error = validate_segmentation(segments)
        # Validation result available but not blocking - for audit purposes
    
    # Suffix ordering validation: check that suffixes appear in valid order
    # This catches impossible sequences like *NMLZ-CAUS (should be CAUS-NMLZ)
    # Uses the refactored morphology/affixes.py module
    if len(segments) > 1:
        # Extract just the suffixes (skip prefixes and root)
        suffix_candidates = []
        for i, seg in enumerate(segments):
            seg_lower = seg.lower()
            if is_suffix(seg_lower):
                suffix_candidates.append(seg_lower)
        
        # Validate suffix ordering if we have multiple suffixes
        if len(suffix_candidates) >= 2:
            if not validate_suffix_sequence(suffix_candidates):
                # Invalid suffix order - this might indicate a parsing error
                # For now, just log for debugging; in future could use alternative parse
                pass  # TODO: Add logging or alternative parse strategy
    
    return (segmented, gloss)


# Set the internal reference for recursive calls in analyze_possessive
_analyze_word_internal = analyze_word


def analyze_word_with_context(word: str, prev_word: str = '', next_word: str = '', 
                              prev2_word: str = '') -> Tuple[str, str]:
    """
    Analyze a word with sentence context for better disambiguation.
    
    This wraps analyze_word() and applies sentence-level disambiguation
    for homophonous words like 'thum' (three/entreat/mourn).
    
    Args:
        word: The word to analyze
        prev_word: Previous word in sentence (for left context)
        next_word: Next word in sentence (for right context)
        prev2_word: Word two positions back (for patterns like "kapin a thum")
        
    Returns:
        Tuple of (segmented_form, gloss)
    """
    seg, gloss = analyze_word(word)
    
    # Apply sentence-level disambiguation
    clean = word.lower().rstrip('.,;:!?"\'')
    prev_clean = prev_word.lower().rstrip('.,;:!?"\'') if prev_word else ''
    prev2_clean = prev2_word.lower().rstrip('.,;:!?"\'') if prev2_word else ''
    next_clean = next_word.lower().rstrip('.,;:!?"\'') if next_word else ''
    
    # thum: three (numeral) vs entreat (verb) vs mourn (verb)
    if clean == 'thum' and gloss == 'three':
        # kong/hong/nong thum = entreat (1SG/2SG object marker + verb)
        if prev_clean in ('kong', 'hong', 'nong'):
            gloss = 'entreat'
        # ka thum + verbal marker = I entreat
        elif prev_clean == 'ka' and next_clean in ('hi', 'uh', 'ing', 'ding', 'theih'):
            gloss = 'entreat'
        # kapin [a] thum = weep-ERG [3SG] mourn (look 1-2 words back)
        elif prev_clean == 'kapin' or prev2_clean == 'kapin':
            gloss = 'mourn'
        # dahin [a] thum = wail-ERG [3SG] mourn
        elif prev_clean == 'dahin' or prev2_clean == 'dahin':
            gloss = 'mourn'
    
    return (seg, gloss)


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


def audit_phonotactics(verbose: bool = False) -> List[Tuple[str, str, str]]:
    """
    Audit all compound entries for phonotactic validity.
    
    This function checks all entries in FUNCTION_WORDS that have tuple values
    (indicating compound words with segmentation) to identify any segmentations
    that produce phonotactically invalid morphemes.
    
    Args:
        verbose: If True, print each invalid entry as found
        
    Returns:
        List of (word, segmentation, invalid_morpheme) tuples for invalid entries
        
    Usage:
        >>> from analyze_morphemes import audit_phonotactics
        >>> invalid = audit_phonotactics(verbose=True)
        >>> print(f"Found {len(invalid)} invalid segmentations")
    """
    invalid_entries = []
    
    # Check FUNCTION_WORDS for compound entries (those with tuple values)
    for word, value in FUNCTION_WORDS.items():
        if isinstance(value, tuple) and len(value) == 2:
            segmentation, gloss = value
            # Split segmentation into morphemes
            segments = segmentation.split('-')
            
            for seg in segments:
                # Skip empty, punctuation-only, or possessive markers
                if not seg or not seg[0].isalpha():
                    continue
                if seg in ["'", "'"]:
                    continue
                    
                if not is_valid_onset(seg):
                    onset = get_onset(seg)
                    invalid_entries.append((word, segmentation, seg))
                    if verbose:
                        print(f"INVALID: '{word}' → '{segmentation}' has invalid morpheme '{seg}' (onset: '{onset}')")
                    break  # Only report first invalid morpheme per entry
    
    return invalid_entries


def gloss_sentence(sentence: str) -> List[Tuple[str, str, str]]:
    """
    Gloss a full sentence with contextual disambiguation.
    
    Returns:
        List of (original, segmented, gloss) tuples
    
    Contextual patterns handled:
    - "min X" (name X): X is treated as proper noun even if homophonous with common word
      e.g., "min Pai" = "name Pai" (place name), not "name go"
    """
    words = sentence.split()
    results = []
    
    for i, word in enumerate(words):
        # Contextual disambiguation: word after "min" (name) is a proper noun
        # This handles cases like "Ama khuapi min Pai hi" where Pai is a place name
        if i > 0 and words[i-1].lower() == 'min' and word[0].isupper():
            # Word follows "min" and is capitalized - treat as proper noun
            results.append((word, word, word.upper()))
        else:
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
# PARADIGM EXTRACTION
# =============================================================================

def extract_word_paradigm(stem: str, corpus_file: str = None, limit: int = 500) -> Dict[str, List[Tuple[str, str, str]]]:
    """
    Extract all attested forms of a word from the corpus.
    
    Returns a dict grouping forms by their morphological category:
    - Bare stem
    - Case-marked (ERG, LOC, ABL, COM)
    - Plural (-te) and Plural + Case
    - Possessed (1SG, 2SG, 3SG, 1PL, 2PL, 3PL)
    - Possessed + Case combinations
    - Possessed + Plural combinations
    - Possessed + Plural + Case combinations
    - Compounds
    """
    if corpus_file is None:
        corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    
    forms = {
        # Basic forms
        'bare': [],
        # Case-marked (singular)
        'case_erg': [],      # Ergative -in
        'case_loc': [],      # Locative -ah
        'case_abl': [],      # Ablative -panin / -pan
        'case_com': [],      # Comitative -tawh
        # Plural
        'number_pl': [],     # Plural -te
        # Plural + Case
        'pl_erg': [],        # N-te-in (PL-ERG)
        'pl_loc': [],        # N-te-ah (PL-LOC)
        'pl_abl': [],        # N-te-panin (PL-ABL)
        'pl_com': [],        # N-te-tawh (PL-COM)
        # Possessed forms
        'poss_1sg': [],      # 1SG possessed (ka-N)
        'poss_2sg': [],      # 2SG possessed (na-N)
        'poss_3sg': [],      # 3SG possessed (a-N)
        'poss_1pl': [],      # 1PL possessed (i-N / kan-N)
        'poss_2pl': [],      # 2PL possessed (nan-N)
        'poss_3pl': [],      # 3PL possessed (an-N)
        # Possessed + Case
        'poss_1sg_case': [], # ka-N-ah, ka-N-in, etc.
        'poss_2sg_case': [], # na-N-ah, etc.
        'poss_3sg_case': [], # a-N-ah, etc.
        'poss_1pl_case': [], # i-N-ah, etc.
        'poss_2pl_case': [], # nan-N-ah, etc.
        'poss_3pl_case': [], # an-N-ah, etc.
        # Possessed + Plural
        'poss_1sg_pl': [],   # ka-N-te
        'poss_2sg_pl': [],   # na-N-te
        'poss_3sg_pl': [],   # a-N-te
        'poss_pl_pl': [],    # i/kan/nan/an-N-te (all plural possessors)
        # Possessed + Plural + Case
        'poss_pl_case': [],  # POSS-N-te-CASE (any combination)
        # Other
        'compounds': [],
        'other': []
    }
    
    seen = set()
    stem_lower = stem.lower()
    
    # Case/number suffixes
    case_suffixes = {'ah': 'LOC', 'in': 'ERG', 'pan': 'ABL', 'panin': 'ABL', 'tawh': 'COM', 'tawhin': 'COM'}
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            verse_id = parts[0]
            text = parts[1]
            
            for word in text.split():
                # Clean punctuation more aggressively
                word_clean = word.strip('.,;:!?"\'()[]{}«»""''').lower()
                # Skip words that still contain punctuation
                if any(c in word_clean for c in '"\'()[]{}«»""'''):
                    continue
                
                if stem_lower not in word_clean:
                    continue
                    
                if word_clean in seen:
                    continue
                seen.add(word_clean)
                
                segmented, gloss = analyze_word(word_clean)
                seg_parts = segmented.split('-') if segmented else [word_clean]
                
                # Verify stem is actually in the segmentation
                # Allow: exact match as morpheme, or word starts with stem (for unsegmented cases)
                stem_found = (
                    any(p == stem_lower for p in seg_parts) or  # exact morpheme match
                    word_clean == stem_lower or                   # bare stem
                    (word_clean.startswith(stem_lower) and len(word_clean) > len(stem_lower))  # stem + suffix
                )
                if not stem_found:
                    continue
                
                entry = (word_clean, segmented, gloss, verse_id)
                gloss_parts = gloss.split('-') if gloss else []
                
                # Detect features from gloss
                # Check for possessor prefixes first (these contain PL in 1PL, 2PL, 3PL)
                poss_markers = ('1SG.POSS', '2SG.POSS', '3SG.POSS', '1PL.POSS', '2PL.POSS', '3PL.POSS',
                                '1SG', '2SG', '3SG', '1PL', '2PL', '3PL', '1PL.INCL', '1PL.EXCL')
                has_poss = any(g in poss_markers for g in gloss_parts)
                
                # PL as suffix (not as part of 1PL, 2PL, etc.)
                has_pl = 'PL' in gloss_parts and not any(g in ('1PL', '2PL', '3PL', '1PL.INCL', '1PL.EXCL', '1PL.POSS', '2PL.POSS', '3PL.POSS') for g in gloss_parts if g == 'PL')
                # Actually simpler: check if '-te' or '-PL' is at end or followed by case
                has_pl = '-te' in segmented or any(g == 'PL' for g in gloss_parts)
                
                has_erg = 'ERG' in gloss_parts
                has_loc = 'LOC' in gloss_parts
                has_abl = 'ABL' in gloss_parts
                has_com = 'COM' in gloss_parts
                has_case = has_erg or has_loc or has_abl or has_com
                
                # Get possessor person if present
                poss_person = None
                for g in gloss_parts:
                    if g in ('1SG.POSS', '1SG'):
                        poss_person = '1sg'
                    elif g in ('2SG.POSS', '2SG'):
                        poss_person = '2sg'
                    elif g in ('3SG.POSS', '3SG'):
                        poss_person = '3sg'
                    elif g in ('1PL.POSS', '1PL', '1PL.INCL', '1PL.EXCL'):
                        poss_person = '1pl'
                    elif g in ('2PL.POSS', '2PL'):
                        poss_person = '2pl'
                    elif g in ('3PL.POSS', '3PL'):
                        poss_person = '3pl'
                    if poss_person:
                        break
                
                # Categorize hierarchically:
                # POSS+PL+CASE > POSS+CASE > POSS+PL > PL+CASE > POSS > PL > CASE > BARE
                
                if word_clean == stem_lower:
                    forms['bare'].append(entry)
                elif has_poss and has_pl and has_case:
                    forms['poss_pl_case'].append(entry)
                elif has_poss and has_case:
                    cat = f'poss_{poss_person}_case' if poss_person else 'poss_1sg_case'
                    if cat in forms:
                        forms[cat].append(entry)
                    else:
                        forms['poss_1sg_case'].append(entry)
                elif has_poss and has_pl:
                    if poss_person in ('1sg', '2sg', '3sg'):
                        forms[f'poss_{poss_person}_pl'].append(entry)
                    else:
                        forms['poss_pl_pl'].append(entry)
                elif has_pl and has_case:
                    if has_erg:
                        forms['pl_erg'].append(entry)
                    elif has_loc:
                        forms['pl_loc'].append(entry)
                    elif has_abl:
                        forms['pl_abl'].append(entry)
                    elif has_com:
                        forms['pl_com'].append(entry)
                elif has_poss:
                    if poss_person:
                        forms[f'poss_{poss_person}'].append(entry)
                    else:
                        forms['poss_1sg'].append(entry)
                elif has_pl:
                    forms['number_pl'].append(entry)
                elif has_case:
                    if has_erg:
                        forms['case_erg'].append(entry)
                    elif has_loc:
                        forms['case_loc'].append(entry)
                    elif has_abl:
                        forms['case_abl'].append(entry)
                    elif has_com:
                        forms['case_com'].append(entry)
                elif '-' in segmented:
                    forms['compounds'].append(entry)
                else:
                    forms['other'].append(entry)
                
                total = sum(len(v) for v in forms.values())
                if total >= limit:
                    break
            
            total = sum(len(v) for v in forms.values())
            if total >= limit:
                break
    
    return forms


def format_paradigm(stem: str, forms: Dict, show_verses: bool = False) -> str:
    """Format paradigm extraction as readable text."""
    lines = [f"# Paradigm for '{stem}'", ""]
    
    category_names = {
        'bare': 'Bare form',
        # Case (singular)
        'case_erg': 'Ergative (-in)',
        'case_loc': 'Locative (-ah)',
        'case_abl': 'Ablative (-panin)',
        'case_com': 'Comitative (-tawh)',
        # Plural
        'number_pl': 'Plural (-te)',
        # Plural + Case
        'pl_erg': 'Plural + Ergative (-te-in)',
        'pl_loc': 'Plural + Locative (-te-ah)',
        'pl_abl': 'Plural + Ablative (-te-panin)',
        'pl_com': 'Plural + Comitative (-te-tawh)',
        # Possessed
        'poss_1sg': 'Possessed 1SG (ka-)',
        'poss_2sg': 'Possessed 2SG (na-)',
        'poss_3sg': 'Possessed 3SG (a-)',
        'poss_1pl': 'Possessed 1PL (i-/kan-)',
        'poss_2pl': 'Possessed 2PL (nan-)',
        'poss_3pl': 'Possessed 3PL (an-)',
        # Possessed + Case
        'poss_1sg_case': 'Possessed 1SG + Case (ka-N-CASE)',
        'poss_2sg_case': 'Possessed 2SG + Case (na-N-CASE)',
        'poss_3sg_case': 'Possessed 3SG + Case (a-N-CASE)',
        'poss_1pl_case': 'Possessed 1PL + Case (i-N-CASE)',
        'poss_2pl_case': 'Possessed 2PL + Case (nan-N-CASE)',
        'poss_3pl_case': 'Possessed 3PL + Case (an-N-CASE)',
        # Possessed + Plural
        'poss_1sg_pl': 'Possessed 1SG + Plural (ka-N-te)',
        'poss_2sg_pl': 'Possessed 2SG + Plural (na-N-te)',
        'poss_3sg_pl': 'Possessed 3SG + Plural (a-N-te)',
        'poss_pl_pl': 'Possessed PL + Plural (i/kan/nan/an-N-te)',
        # Possessed + Plural + Case
        'poss_pl_case': 'Possessed + Plural + Case (POSS-N-te-CASE)',
        # Other
        'compounds': 'In compounds',
        'other': 'Other forms'
    }
    
    # Define display order
    display_order = [
        'bare',
        'case_erg', 'case_loc', 'case_abl', 'case_com',
        'number_pl',
        'pl_erg', 'pl_loc', 'pl_abl', 'pl_com',
        'poss_1sg', 'poss_2sg', 'poss_3sg', 'poss_1pl', 'poss_2pl', 'poss_3pl',
        'poss_1sg_case', 'poss_2sg_case', 'poss_3sg_case', 'poss_1pl_case', 'poss_2pl_case', 'poss_3pl_case',
        'poss_1sg_pl', 'poss_2sg_pl', 'poss_3sg_pl', 'poss_pl_pl',
        'poss_pl_case',
        'compounds', 'other'
    ]
    
    for cat in display_order:
        if cat not in forms or not forms[cat]:
            continue
        entries = forms[cat]
        name = category_names.get(cat, cat)
        lines.append(f"## {name} ({len(entries)} forms)")
        for entry in entries:
            word, seg, gloss, verse_id = entry
            if show_verses:
                lines.append(f"  {word:<20} {seg:<30} '{gloss}' [{verse_id}]")
            else:
                lines.append(f"  {word:<20} {seg:<30} '{gloss}'")
        lines.append("")
    
    return '\n'.join(lines)


def extract_verb_paradigm(stem: str, corpus_file: str = None, limit: int = 100) -> Dict[str, List]:
    """
    Extract all attested forms of a verb from the corpus.
    
    Groups by: bare, prefixed (ki-, pi-, etc.), TAM-marked, nominalized, compounds
    """
    if corpus_file is None:
        corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    
    forms = {
        'bare': [],
        'pronominal': [],  # ka-, na-, a-, kong-, hong-
        'voice': [],  # ki-, pi-
        'tam': [],  # -ta, -zo, -ding, -kik, etc.
        'nominalized': [],  # -na, -pa, -te
        'serial': [],  # compound verbs
        'other': []
    }
    
    seen = set()
    stem_lower = stem.lower()
    
    # Voice/derivational prefixes
    voice_prefixes = {'ki-', 'pi-', 'pua-'}
    # Pronominal prefixes  
    pron_prefixes = {'ka-', 'na-', 'a-', 'i-', 'kong-', 'hong-', 'nong-'}
    # TAM suffixes
    tam_suffixes = {'-ta', '-zo', '-ding', '-kik', '-nawn', '-khin', '-khit', '-thei', '-nuam', '-sak', '-pih'}
    # Nominalizer suffixes
    nmlz_suffixes = {'-na', '-pa', '-te', '-sate'}
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            verse_id = parts[0]
            text = parts[1]
            
            for word in text.split():
                word_clean = word.strip('.,;:!?"\'').lower()
                if stem_lower not in word_clean:
                    continue
                if word_clean in seen:
                    continue
                seen.add(word_clean)
                
                segmented, gloss = analyze_word(word_clean)
                entry = (word_clean, segmented, gloss, verse_id)
                
                # Categorize
                if word_clean == stem_lower:
                    forms['bare'].append(entry)
                elif any(segmented.startswith(p) for p in voice_prefixes):
                    forms['voice'].append(entry)
                elif any(segmented.startswith(p) for p in pron_prefixes):
                    forms['pronominal'].append(entry)
                elif any(s in segmented for s in tam_suffixes):
                    forms['tam'].append(entry)
                elif any(segmented.endswith(s) for s in nmlz_suffixes):
                    forms['nominalized'].append(entry)
                elif '-' in segmented:
                    forms['serial'].append(entry)
                else:
                    forms['other'].append(entry)
                
                total = sum(len(v) for v in forms.values())
                if total >= limit:
                    break
            
            total = sum(len(v) for v in forms.values())
            if total >= limit:
                break
    
    return forms


def format_verb_paradigm(stem: str, forms: Dict, show_verses: bool = False) -> str:
    """Format verb paradigm as readable text."""
    lines = [f"# Verb paradigm for '{stem}'", ""]
    
    category_names = {
        'bare': 'Bare stem',
        'pronominal': 'Pronominal prefixes',
        'voice': 'Voice/derivational',
        'tam': 'TAM-marked',
        'nominalized': 'Nominalized',
        'serial': 'Serial/compound verbs',
        'other': 'Other forms'
    }
    
    for cat, entries in forms.items():
        if not entries:
            continue
        lines.append(f"## {category_names[cat]} ({len(entries)} forms)")
        for word, seg, gloss, verse_id in entries:
            if show_verses:
                lines.append(f"  {word:<20} {seg:<30} '{gloss}' [{verse_id}]")
            else:
                lines.append(f"  {word:<20} {seg:<30} '{gloss}'")
        lines.append("")
    
    return '\n'.join(lines)


# =============================================================================
# COVERAGE CHECKING
# =============================================================================

def check_coverage(corpus_file: str = None, verbose: bool = False) -> dict:
    """
    Check morphological analysis coverage on the Bible corpus.
    
    IMPORTANT: Do NOT lowercase words before analysis - proper noun detection
    requires original case (e.g., 'Nazareth' → NAZARETH, 'nazareth' → 2SG-?).
    
    Returns:
        dict with keys: total, full, partial, unknown, coverage_pct
    """
    if corpus_file is None:
        corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    
    total = 0
    full = 0
    partial = 0
    unknown = 0
    partial_words = []
    unknown_words = []
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            text = parts[1]
            for word in text.split():
                if not word:
                    continue
                total += 1
                # IMPORTANT: preserve original case for proper noun detection
                seg, gloss = analyze_word(word)
                if '?' in gloss:
                    if gloss == '?':
                        unknown += 1
                        if verbose and len(unknown_words) < 50:
                            unknown_words.append(word)
                    else:
                        partial += 1
                        if verbose and len(partial_words) < 50:
                            partial_words.append((word, seg, gloss))
                else:
                    full += 1
    
    coverage_pct = 100 * full / total if total > 0 else 0
    
    result = {
        'total': total,
        'full': full,
        'partial': partial,
        'unknown': unknown,
        'coverage_pct': coverage_pct
    }
    
    if verbose:
        result['partial_words'] = partial_words
        result['unknown_words'] = unknown_words
    
    return result


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_morphemes.py <word>")
        print("       python analyze_morphemes.py --sentence 'Tedim sentence here'")
        print("       python analyze_morphemes.py --paradigm <noun>")
        print("       python analyze_morphemes.py --verb-paradigm <verb>")
        print("       python analyze_morphemes.py --coverage [-v]")
        sys.exit(1)
    
    if sys.argv[1] == '--coverage':
        verbose = '-v' in sys.argv or '--verbose' in sys.argv
        result = check_coverage(verbose=verbose)
        print(f"Total tokens:  {result['total']:,}")
        print(f"Full glosses:  {result['full']:,} ({result['coverage_pct']:.4f}%)")
        print(f"Partial:       {result['partial']:,}")
        print(f"Unknown:       {result['unknown']:,}")
        if verbose and result.get('partial_words'):
            print("\nPartial glosses:")
            for word, seg, gloss in result['partial_words'][:20]:
                print(f"  {word:<20} -> {seg:<25} {gloss}")
        if verbose and result.get('unknown_words'):
            print("\nUnknown words:")
            for word in result['unknown_words'][:20]:
                print(f"  {word}")
        sys.exit(0)
    
    if sys.argv[1] == '--paradigm':
        # Extract noun paradigm
        stem = sys.argv[2]
        forms = extract_word_paradigm(stem, limit=100)
        print(format_paradigm(stem, forms, show_verses=True))
    
    elif sys.argv[1] == '--verb-paradigm':
        # Extract verb paradigm
        stem = sys.argv[2]
        forms = extract_verb_paradigm(stem, limit=100)
        print(format_verb_paradigm(stem, forms, show_verses=True))
    
    elif sys.argv[1] == '--sentence':
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
