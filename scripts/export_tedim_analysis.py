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
class LemmaEntry:
    """Lemma-level dictionary entry."""
    lemma: str
    citation_form: str
    pos: str
    glosses: Set[str] = field(default_factory=set)
    inflected_forms: Set[str] = field(default_factory=set)
    token_count: int = 0
    form_count: int = 0
    derivational_family: Set[str] = field(default_factory=set)
    compounds: Set[str] = field(default_factory=set)
    collocates: Dict[str, int] = field(default_factory=dict)
    example_verses: List[Tuple[str, str, str]] = field(default_factory=list)  # (verse_id, tedim, kjv)
    polysemy_notes: str = ''
    grammaticalization_notes: str = ''

@dataclass
class GrammaticalMorpheme:
    """Grammatical morpheme entry."""
    form: str
    gloss: str
    category: str  # case, tam, particle, nominalizer, prefix, etc.
    frequency: int = 0
    environments: Set[str] = field(default_factory=set)  # prefix, suffix, clitic, etc.
    example_verses: List[Tuple[str, str, str]] = field(default_factory=list)
    ambiguity_notes: str = ''
    status: str = 'auto'

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
# MORPHEME CLASSIFICATION
# =============================================================================

# Grammatical morpheme categories
GRAMMATICAL_CATEGORIES = {
    'case': {
        'in': 'ERG', 'ah': 'LOC', 'pan': 'ABL', 'tawh': 'COM',
        'ding': 'PROSP', 'dingin': 'PROSP', 'bang': 'SIM',
    },
    'tam': dict(TAM_SUFFIXES),
    'nominalizer': dict(NOMINALIZERS),
    'pronominal_prefix': dict(PRONOMINAL_PREFIXES),
    'object_prefix': dict(OBJECT_PREFIXES),
    'particle': {
        'ahi': 'COP', 'hi': 'PROX', 'kha': 'DIST', 'le': 'and',
        'leh': 'if/and', 'pen': 'TOP', 'zong': 'also', 'ham': 'also',
        'mah': 'EMPH', 'bek': 'only', 'peuhmah': 'any', 'peuh': 'every',
    },
    'sentence_final': {
        'hi': 'DECL', 'hiam': 'Q', 'hen': 'HORT', 'in': 'IMP',
        'ang': 'FUT', 'ding': 'PROSP', 've': 'EMPH', 'eh': 'EXCL',
    },
    'directional': {
        'khia': 'out', 'lut': 'in', 'tung': 'up', 'tang': 'down',
        'pai': 'go', 'hong': 'come.DIR', 'kik': 'back',
    },
    'auxiliary': {
        'thei': 'ABIL', 'theih': 'ABIL.II', 'nuam': 'want',
        'ding': 'PROSP', 'kik': 'again', 'zel': 'CONT',
        'ngei': 'EXPER', 'gige': 'HAB',
    },
}

def classify_morpheme(morpheme: str, gloss: str, position: str = 'suffix') -> Tuple[str, str]:
    """
    Classify a morpheme as lexical or grammatical.
    
    Returns:
        (category, subcategory) - e.g., ('grammatical', 'case') or ('lexical', 'verb')
    """
    m_lower = morpheme.lower()
    
    # Check grammatical categories
    for cat, morphemes in GRAMMATICAL_CATEGORIES.items():
        if m_lower in morphemes:
            return ('grammatical', cat)
    
    # Check if it's a known stem
    if m_lower in VERB_STEMS:
        return ('lexical', 'verb')
    if m_lower in NOUN_STEMS:
        return ('lexical', 'noun')
    if m_lower in VERB_STEM_PAIRS:
        return ('lexical', 'verb_ii')
    
    # Check function words
    if m_lower in FUNCTION_WORDS:
        return ('grammatical', 'function')
    
    # Check if gloss suggests grammatical function
    gram_glosses = {'ERG', 'LOC', 'ABL', 'COM', 'DAT', 'GEN', 'POSS',
                    'PL', 'SG', 'NMLZ', 'CAUS', 'APPL', 'REFL', 'RECIP',
                    'PST', 'FUT', 'PERF', 'PROG', 'HAB', 'CONT',
                    '1SG', '2SG', '3SG', '1PL', '2PL', '3PL',
                    'Q', 'NEG', 'IMP', 'HORT', 'DECL', 'EXCL'}
    if gloss.upper() in gram_glosses:
        return ('grammatical', 'inflection')
    
    return ('lexical', 'unknown')

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
        
        # Tokenize
        words = tedim_text.split()
        prev_lemma = None
        
        for idx, word in enumerate(words):
            # Clean punctuation for analysis
            clean_word = word.strip('.,;:!?"\'')
            if not clean_word:
                continue
            
            # Analyze
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
            if confidence != 'unknown' and pos not in ('FUNC', 'UNK'):
                if lemma not in lemmas:
                    lemmas[lemma] = LemmaEntry(
                        lemma=lemma,
                        citation_form=lemma,
                        pos=pos
                    )
                lem = lemmas[lemma]
                lem.glosses.add(gloss.split('-')[0] if '-' in gloss else gloss)
                lem.inflected_forms.add(normalized)
                lem.token_count += 1
                if len(lem.example_verses) < 10:
                    lem.example_verses.append((verse_id, tedim_text, kjv_text))
                
                # Track collocations
                if prev_lemma and prev_lemma != lemma:
                    collocations[prev_lemma][lemma] += 1
                    collocations[lemma][prev_lemma] += 1
            
            # Extract grammatical morphemes
            gloss_parts = gloss.split('-')
            seg_parts = segmentation.replace("'", '').split('-')
            
            for i, (seg_part, gloss_part) in enumerate(zip(seg_parts, gloss_parts)):
                cat_type, cat_sub = classify_morpheme(seg_part, gloss_part)
                if cat_type == 'grammatical':
                    gm_key = seg_part.lower()
                    if gm_key not in gram_morphemes:
                        gram_morphemes[gm_key] = GrammaticalMorpheme(
                            form=seg_part.lower(),
                            gloss=gloss_part,
                            category=cat_sub
                        )
                    gm = gram_morphemes[gm_key]
                    gm.frequency += 1
                    env = 'prefix' if i == 0 else ('suffix' if i == len(seg_parts) - 1 else 'infix')
                    gm.environments.add(env)
                    if len(gm.example_verses) < 10:
                        gm.example_verses.append((verse_id, tedim_text, kjv_text))
            
            prev_lemma = lemma if pos not in ('FUNC', 'UNK', 'PROP') else prev_lemma
    
    # Post-process: add collocates to lemmas
    for lemma_key, lem in lemmas.items():
        if lemma_key in collocations:
            lem.collocates = dict(sorted(
                collocations[lemma_key].items(),
                key=lambda x: -x[1]
            )[:20])
        lem.form_count = len(lem.inflected_forms)
    
    return tokens, wordforms, lemmas, gram_morphemes

def select_examples(lemmas: Dict[str, LemmaEntry], 
                    gram_morphemes: Dict[str, GrammaticalMorpheme],
                    target_per_item: int = 5) -> List[ExampleEntry]:
    """
    Select high-quality examples for each lemma and grammatical morpheme.
    
    Selection criteria:
    - shortest: Shortest verse containing the item
    - canonical: Most frequent/typical usage
    - transparent: Clear morphological structure
    - marked: Secondary or less prototypical function
    """
    examples = []
    
    # Process lemmas
    for lemma, entry in lemmas.items():
        if not entry.example_verses:
            continue
        
        # Sort by verse length to find shortest
        sorted_by_len = sorted(entry.example_verses, key=lambda x: len(x[1]))
        
        selected = set()
        
        # 1. Shortest clear example
        if sorted_by_len:
            ex = sorted_by_len[0]
            if ex[0] not in selected:
                examples.append(ExampleEntry(
                    item_type='lemma',
                    item_id=lemma,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented='',  # Will be filled by caller if needed
                    glossed='',
                    kjv_text=ex[2],
                    example_quality='shortest',
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
        
        # 2-4. Additional diverse examples
        for ex in entry.example_verses:
            if len(selected) >= target_per_item:
                break
            if ex[0] not in selected:
                quality = 'canonical' if len(selected) == 1 else 'additional'
                examples.append(ExampleEntry(
                    item_type='lemma',
                    item_id=lemma,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented='',
                    glossed='',
                    kjv_text=ex[2],
                    example_quality=quality,
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
    
    # Process grammatical morphemes
    for form, entry in gram_morphemes.items():
        if not entry.example_verses:
            continue
        
        sorted_by_len = sorted(entry.example_verses, key=lambda x: len(x[1]))
        selected = set()
        
        for i, ex in enumerate(sorted_by_len[:target_per_item]):
            if ex[0] not in selected:
                quality = 'shortest' if i == 0 else ('canonical' if i == 1 else 'additional')
                examples.append(ExampleEntry(
                    item_type='morpheme',
                    item_id=form,
                    verse_id=ex[0],
                    tedim_text=ex[1],
                    segmented='',
                    glossed='',
                    kjv_text=ex[2],
                    example_quality=quality,
                    word_count=len(ex[1].split())
                ))
                selected.add(ex[0])
    
    return examples

def collect_ambiguities(tokens: List[TokenAnalysis], 
                        wordforms: Dict) -> List[Dict]:
    """Collect ambiguous analyses into review queue."""
    ambiguities = []
    seen = set()
    
    for token in tokens:
        if token.is_ambiguous:
            key = (token.normalized_form, token.segmentation)
            if key not in seen:
                seen.add(key)
                ambiguities.append({
                    'surface_form': token.surface_form,
                    'normalized_form': token.normalized_form,
                    'segmentation': token.segmentation,
                    'gloss': token.gloss,
                    'confidence': token.confidence,
                    'pos': token.pos,
                    'first_verse': token.verse_id,
                    'frequency': sum(1 for t in tokens 
                                    if t.normalized_form == token.normalized_form),
                    'issue': 'unknown' if token.confidence == 'unknown' else 'partial_gloss',
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
            'lemma', 'citation_form', 'pos', 'glosses', 'inflected_forms',
            'token_count', 'form_count', 'compounds', 'top_collocates',
            'example_verses', 'polysemy_notes', 'grammaticalization_notes'
        ])
        
        for lem in lem_list:
            # Format collocates as "word:count" pairs
            colloc_str = '|'.join(f"{k}:{v}" for k, v in list(lem.collocates.items())[:10])
            # Format examples as verse IDs
            ex_str = '|'.join(ex[0] for ex in lem.example_verses[:5])
            
            writer.writerow([
                lem.lemma, lem.citation_form, lem.pos,
                '|'.join(sorted(lem.glosses)),
                '|'.join(sorted(lem.inflected_forms)[:20]),
                lem.token_count, lem.form_count,
                '|'.join(sorted(lem.compounds)),
                colloc_str, ex_str,
                lem.polysemy_notes, lem.grammaticalization_notes
            ])

def write_grammatical_morphemes_tsv(gram_morphemes: Dict[str, GrammaticalMorpheme], 
                                     output_path: str):
    """Write grammatical morphemes table."""
    # Sort by frequency
    gm_list = sorted(gram_morphemes.values(), key=lambda x: -x.frequency)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'form', 'gloss', 'category', 'frequency', 'environments',
            'example_verses', 'ambiguity_notes', 'status'
        ])
        
        for gm in gm_list:
            ex_str = '|'.join(ex[0] for ex in gm.example_verses[:5])
            
            writer.writerow([
                gm.form, gm.gloss, gm.category, gm.frequency,
                '|'.join(sorted(gm.environments)), ex_str,
                gm.ambiguity_notes, gm.status
            ])

def write_examples_tsv(examples: List[ExampleEntry], output_path: str):
    """Write curated examples bank."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'item_type', 'item_id', 'verse_id', 'tedim_text',
            'kjv_text', 'example_quality', 'word_count'
        ])
        
        for ex in examples:
            writer.writerow([
                ex.item_type, ex.item_id, ex.verse_id, ex.tedim_text,
                ex.kjv_text, ex.example_quality, ex.word_count
            ])

def write_ambiguities_tsv(ambiguities: List[Dict], output_path: str):
    """Write ambiguity review queue."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'surface_form', 'normalized_form', 'segmentation', 'gloss',
            'confidence', 'pos', 'first_verse', 'frequency', 'issue', 'status'
        ])
        
        for amb in ambiguities:
            writer.writerow([
                amb['surface_form'], amb['normalized_form'],
                amb['segmentation'], amb['gloss'], amb['confidence'],
                amb['pos'], amb['first_verse'], amb['frequency'],
                amb['issue'], amb['status']
            ])

def write_coverage_report(tokens: List[TokenAnalysis], wordforms: Dict,
                          lemmas: Dict, gram_morphemes: Dict,
                          ambiguities: List[Dict], output_path: str):
    """Write coverage statistics report."""
    total_tokens = len(tokens)
    analyzed = sum(1 for t in tokens if t.confidence in ('high', 'medium'))
    partial = sum(1 for t in tokens if t.confidence == 'low')
    unknown = sum(1 for t in tokens if t.confidence == 'unknown')
    
    coverage = 100 * analyzed / total_tokens if total_tokens else 0
    
    # POS distribution
    pos_counts = defaultdict(int)
    for t in tokens:
        pos_counts[t.pos] += 1
    
    report = f"""# Tedim Chin Bible Analysis Coverage Report

Generated: {__import__('datetime').datetime.now().isoformat()}

## Overall Statistics

| Metric | Count | Percentage |
|--------|-------|------------|
| Total tokens | {total_tokens:,} | 100% |
| Fully analyzed | {analyzed:,} | {100*analyzed/total_tokens:.2f}% |
| Partial analysis | {partial:,} | {100*partial/total_tokens:.2f}% |
| Unknown | {unknown:,} | {100*unknown/total_tokens:.4f}% |

**Coverage: {coverage:.4f}%**

## Inventory Counts

| Category | Count |
|----------|-------|
| Distinct wordforms | {len(wordforms):,} |
| Lemmas | {len(lemmas):,} |
| Grammatical morphemes | {len(gram_morphemes):,} |
| Items needing review | {len(ambiguities):,} |

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

| Lemma | POS | Token Count | Form Count |
|-------|-----|-------------|------------|
"""
    top_lemmas = sorted(lemmas.values(), key=lambda x: -x.token_count)[:20]
    for lem in top_lemmas:
        report += f"| {lem.lemma} | {lem.pos} | {lem.token_count:,} | {lem.form_count} |\n"
    
    report += f"""
## Ambiguity Summary

- Total ambiguous wordforms: {len(ambiguities)}
- Unknown tokens: {sum(1 for a in ambiguities if a['issue'] == 'unknown')}
- Partial glosses: {sum(1 for a in ambiguities if a['issue'] == 'partial_gloss')}

### Top 10 Most Frequent Ambiguous Forms

| Form | Frequency | Issue |
|------|-----------|-------|
"""
    for amb in ambiguities[:10]:
        report += f"| {amb['surface_form']} | {amb['frequency']} | {amb['issue']} |\n"
    
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
    ambiguities = collect_ambiguities(tokens, wordforms)
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
