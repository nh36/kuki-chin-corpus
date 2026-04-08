#!/usr/bin/env python3
"""
Generate 100 sample dictionary entries from the export pipeline data.

Produces:
- 70 lexical stems (nouns and verbs)
- 20 grammatical words (function words, particles)
- 10 affixes/clitics

Each entry includes:
- lemma
- citation form
- POS
- gloss
- morphology notes
- attested forms (sample)
- frequency
- 2-3 curated examples

Output: data/ctd_analysis/sample_entries.md
"""

import os
import csv
import random
from dataclasses import dataclass
from typing import List, Dict, Optional


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'ctd_analysis')


@dataclass
class DictEntry:
    lemma: str
    citation_form: str
    pos: str
    gloss: str
    morphology: str
    attested_forms: List[str]
    frequency: int
    examples: List[Dict[str, str]]


def load_lemmas() -> Dict[str, dict]:
    """Load lemmas from TSV file."""
    lemmas = {}
    path = os.path.join(DATA_DIR, 'lemmas.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemmas[row['lemma']] = row
    return lemmas


def load_grammatical_morphemes() -> Dict[str, dict]:
    """
    Load grammatical morphemes from TSV file.
    
    Since the same form can have multiple rows (different glosses/functions),
    we aggregate by form and keep the highest-frequency row as primary,
    while tracking all glosses.
    """
    morphemes = {}
    path = os.path.join(DATA_DIR, 'grammatical_morphemes.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            form = row['form']
            freq = int(row.get('frequency', 0) or 0)
            
            if form not in morphemes:
                morphemes[form] = {
                    'form': form,
                    'gloss': row['gloss'],
                    'dominant_gloss': row['gloss'],
                    'category': row['category'],
                    'frequency': freq,
                    'environments': row.get('environments', ''),
                    'example_verses': row.get('example_verses', ''),
                    'all_glosses': [(row['gloss'], freq)],
                    'is_polysemous': row.get('is_polysemous', '0'),
                    '_max_freq': freq  # Track the current max
                }
            else:
                # Aggregate: keep highest frequency row as primary
                existing = morphemes[form]
                existing['all_glosses'].append((row['gloss'], freq))
                existing['frequency'] = max(int(existing['frequency']), freq)
                
                # Update gloss if this row has higher frequency
                if freq > existing.get('_max_freq', 0):
                    existing['gloss'] = row['gloss']
                    existing['dominant_gloss'] = row['gloss']
                    existing['category'] = row['category']  # Also update category
                    existing['_max_freq'] = freq
                
                # Merge environments
                existing_envs = set(existing['environments'].split('|')) if existing['environments'] else set()
                new_envs = set(row.get('environments', '').split('|')) if row.get('environments') else set()
                existing['environments'] = '|'.join(sorted(existing_envs | new_envs - {''}))
                
                # Mark as polysemous if multiple glosses
                existing['is_polysemous'] = '1'
    
    # Clean up temporary fields
    for m in morphemes.values():
        m.pop('_max_freq', None)
    
    return morphemes


def load_examples() -> Dict[str, List[dict]]:
    """Load examples, indexed by item_id."""
    examples = {}
    path = os.path.join(DATA_DIR, 'examples.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            item = row['item_id']
            if item not in examples:
                examples[item] = []
            examples[item].append(row)
    return examples


def select_lexical_stems(lemmas: Dict[str, dict], n: int = 70) -> List[dict]:
    """
    Select n lexical stems, balanced between nouns and verbs.
    
    Excludes:
    - Items marked as primarily grammatical (is_grammatical=1)
    - Items with unsafe_gloss or mixed_lex_gram entry_status
    - Known problematic polysemous forms
    """
    # Forms to exclude from polished lexical entries
    EXCLUDE_FORMS = {'hi', 'ding', 'ahih', 'ahi', 'hong', 'khat', 'lai', 'mahmah', 
                     'thei', 'pan', 'ta', 'te', 'in', 'na'}
    
    def is_clean_lexical(l: dict) -> bool:
        """Check if a lemma is suitable for polished lexical entry."""
        # Must be V or N
        if l['pos'] not in ('V', 'N'):
            return False
        # Must have reasonable frequency
        if int(l['token_count']) < 50:
            return False
        # Exclude primarily grammatical items
        if l.get('is_grammatical') == '1':
            return False
        # Exclude unsafe or mixed entries
        status = l.get('entry_status', 'auto')
        if status in ('unsafe_gloss', 'mixed_lex_gram'):
            return False
        # Exclude known problematic forms
        if l['lemma'].lower() in EXCLUDE_FORMS:
            return False
        # Must have a real gloss (not just ?)
        gloss = l.get('primary_gloss', '?')
        if not gloss or gloss == '?':
            return False
        return True
    
    verbs = [l for l in lemmas.values() if l['pos'] == 'V' and is_clean_lexical(l)]
    nouns = [l for l in lemmas.values() if l['pos'] == 'N' and is_clean_lexical(l)]
    
    # Sort by frequency
    verbs.sort(key=lambda x: -int(x['token_count']))
    nouns.sort(key=lambda x: -int(x['token_count']))
    
    # Take top items, balanced
    n_verbs = n // 2
    n_nouns = n - n_verbs
    
    # Mix high and mid frequency
    selected_verbs = verbs[:n_verbs//2] + verbs[n_verbs//2:n_verbs]
    selected_nouns = nouns[:n_nouns//2] + nouns[n_nouns//2:n_nouns]
    
    return selected_verbs + selected_nouns


def load_senses() -> Dict[str, List[dict]]:
    """Load senses from TSV file, indexed by lemma."""
    senses = {}
    path = os.path.join(DATA_DIR, 'senses.tsv')
    if not os.path.exists(path):
        return senses
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemma = row['lemma']
            if lemma not in senses:
                senses[lemma] = []
            senses[lemma].append(row)
    return senses


def is_clean_grammatical(l: dict, senses: Dict[str, List[dict]]) -> bool:
    """
    Check if a lemma is suitable for polished grammatical entry.
    
    Requires:
    - Stable grammatical gloss (not lexical residue)
    - Entry status is clean or at least coherent
    - POS is FUNC or clearly grammaticalized
    - Examples support the grammatical function
    """
    lemma = l['lemma'].lower()
    
    # Exclude items with UNK POS
    if l['pos'] == 'UNK':
        return False
    
    # Must have decent frequency
    if int(l['token_count']) < 100:
        return False
    
    # Check entry status - only clean or polysemous_review (not mixed/unsafe)
    status = l.get('entry_status', 'auto')
    if status in ('unsafe_gloss', 'mixed_lex_gram'):
        return False
    
    # Must have a real gloss
    gloss = l.get('primary_gloss', '')
    if not gloss or gloss == '?':
        return False
    
    # Gloss should look grammatical (all caps or known gram pattern)
    gram_glosses = {'DECL', 'IRR', 'ERG', 'LOC', 'ABL', 'ALL', 'GEN', 'DAT', 
                    '1SG', '2SG', '3SG', '1PL', '2PL', '3PL', 'REFL', 'RECIP',
                    'NMLZ', 'CAUS', 'NEG', 'Q', 'QUOT', 'REL', 'PL', 'POSS',
                    'say', 'be', 'go', 'come', 'and', 'or', 'but', 'if', 'then',
                    'that', 'this', 'what', 'who', 'where', 'when', 'how',
                    'all', 'every', 'some', 'any', 'no', 'not', 'also', 'too',
                    'DIR', '3→1', '1SG→3', 'be.3SG'}
    
    gloss_base = gloss.split('.')[0].split('-')[0]
    if gloss_base not in gram_glosses and not gloss.isupper():
        # Check if it looks like a content word gloss
        content_glosses = {'see', 'sharpen', 'return', 'measure', 'clear', 'become'}
        if gloss_base.lower() in content_glosses:
            return False
    
    # If we have senses, verify the primary sense is grammatical
    if lemma in senses:
        primary = [s for s in senses[lemma] if s.get('is_primary') == '1']
        if primary:
            if primary[0].get('is_grammatical') != '1':
                # Primary sense is lexical, not grammatical
                return False
    
    return True


# Forms that are known to be clean grammatical words
VERIFIED_GRAMMATICAL = {
    'hi', 'ding', 'hong', 'ci', 'ahi', 'ahih', 'tua', 'hih', 'bang',
    'le', 'in', 'a', 'ka', 'na', 'i', 'nu', 'te', 'ta',
    'khempeuh', 'peuh', 'bek', 'mahmah', 'taktak', 'khat', 'khit'
}

# Forms that need review (mixed/unclear) - exclude from polished
GRAMMATICAL_REVIEW_NEEDED = {
    'ciang', 'zong', 'leh', 'maw', 'hiam', 'zawh', 'suan', 'kua',
    'hangin', 'ciangin', 'bangin', 'mahin'
}


def select_grammatical_words(lemmas: Dict[str, dict], morphemes: Dict[str, dict], 
                             senses: Dict[str, List[dict]], max_n: int = 20) -> List[dict]:
    """
    Select grammatical words (function words, particles) for polished sample.
    
    Prioritizes clean, high-confidence items over reaching arbitrary count.
    Returns fewer items if clean entries are not available.
    """
    selected = []
    seen_forms = set()
    
    # First pass: verified grammatical forms that pass clean check
    for lemma_name in VERIFIED_GRAMMATICAL:
        if lemma_name in lemmas:
            l = lemmas[lemma_name]
            # Accept any POS that's marked as grammatical
            if l.get('is_grammatical') == '1' and is_clean_grammatical(l, senses):
                if lemma_name not in seen_forms:
                    selected.append(l)
                    seen_forms.add(lemma_name)
    
    # Second pass: high-frequency items marked is_grammatical=1
    gram_lemmas = [l for l in lemmas.values() 
                   if l.get('is_grammatical') == '1'
                   and l['lemma'].lower() not in seen_forms
                   and l['lemma'].lower() not in GRAMMATICAL_REVIEW_NEEDED
                   and is_clean_grammatical(l, senses)
                   and int(l['token_count']) > 500]
    gram_lemmas.sort(key=lambda x: -int(x['token_count']))
    
    for gl in gram_lemmas:
        if len(selected) >= max_n:
            break
        selected.append(gl)
        seen_forms.add(gl['lemma'])
    
    # Do NOT pad with unverified items - prefer fewer clean entries
    return selected


def is_clean_affix(m: dict) -> bool:
    """
    Check if a grammatical morpheme is suitable for polished affix entry.
    
    Requires:
    - Stable category
    - Dominant gloss matches category
    - Environments compatible with category
    - No mixed lexical/grammatical evidence
    """
    form = m['form']
    category = m.get('category', '')
    gloss = m.get('dominant_gloss', m.get('gloss', ''))
    envs = set(m.get('environments', '').split('|')) if m.get('environments') else set()
    freq = int(m.get('frequency', 0) or 0)
    
    # Must have reasonable frequency
    if freq < 50:
        return False
    
    # Must have a real gloss
    if not gloss or gloss == '?':
        return False
    
    # Only include actual affixes/clitics, not function words masquerading as affixes
    affix_categories = {'pronominal_prefix', 'case_marker', 'plural_marker', 
                        'tam_suffix', 'sentence_final', 'derivational', 'inflection'}
    if category not in affix_categories:
        return False
    
    # Category-specific validation
    if category == 'case_marker':
        # Case markers should be suffixes, not prefixes
        if 'prefix' in envs and 'suffix' not in envs:
            return False
        # Gloss should be case-like (ERG, LOC, ABL, ALL, etc.)
        if gloss.lower() in ('take', 'go', 'come', 'put', 'leaf', 'fly', 'with'):
            return False
        # Must be grammatical gloss, not lexical
        valid_case_glosses = {'ERG', 'ABS', 'LOC', 'ABL', 'ALL', 'DAT', 'GEN', 'COM', 
                              'INST', 'CVB', 'QUOT', 'IN'}
        if gloss not in valid_case_glosses:
            return False
    
    if category == 'plural_marker':
        # Should have PL-related gloss
        valid_pl_glosses = {'PL', 'plural', 'te', 'TE', 'PL.POSS', 'TE.POSS'}
        if gloss not in valid_pl_glosses:
            return False
    
    if category == 'tam_suffix':
        # TAM markers should be suffixes
        if 'prefix' in envs and 'suffix' not in envs:
            return False
        # Gloss should be TAM-like, not causative (that's a separate category)
        if gloss in ('CAUS', 'causative'):
            return False
    
    if category == 'sentence_final':
        # Should not show prefix environment
        if 'prefix' in envs:
            return False
    
    if category == 'pronominal_prefix':
        # Should be prefix, not suffix
        if 'suffix' in envs and 'prefix' not in envs:
            return False
        # Valid pronominal glosses
        valid_pron = {'1SG', '2SG', '3SG', '1PL', '2PL', '3PL', 'POSS', 'AGR'}
        if gloss not in valid_pron:
            return False
    
    # Reject items with suspiciously mixed environments (usually indicates contaminated data)
    if envs == {'prefix', 'suffix'}:
        return False
    if envs == {'prefix', 'stem', 'suffix'}:
        return False
    
    return True


def select_affixes(morphemes: Dict[str, dict], max_n: int = 10) -> List[dict]:
    """
    Select affixes/clitics for polished sample.
    
    Prioritizes clean, function-specific rows over filling a quota.
    Returns fewer items if clean entries are not available.
    """
    affixes = []
    seen_forms = set()
    
    # Categories in order of priority, with target counts (flexible)
    category_targets = [
        ('pronominal_prefix', 2),  # a-, ka-, na-, i-
        ('case_marker', 2),        # -ah, -in (ERG)
        ('inflection', 2),         # ki-, su-, suk-
        ('tam_suffix', 1),         # -ta, -khin, -lai
        ('nominalizer', 1),        # -na
        ('plural_marker', 1),      # -te (PL only)
        ('sentence_final', 1),     # -hi (if clean)
        ('derivational', 1),       # -sak (CAUS), etc.
        ('quotative', 1),          # -ci
    ]
    
    for category, target in category_targets:
        items = [m for m in morphemes.values() 
                 if m['category'] == category 
                 and m['form'] not in seen_forms
                 and is_clean_affix(m)]
        items.sort(key=lambda x: -int(x['frequency']))
        
        added = 0
        for m in items:
            if added >= target or len(affixes) >= max_n:
                break
            affixes.append(m)
            seen_forms.add(m['form'])
            added += 1
    
    return affixes


def get_entry_examples(item: str, all_examples: Dict[str, List[dict]], n: int = 3) -> List[Dict[str, str]]:
    """Get curated examples for an entry."""
    if item not in all_examples:
        return []
    
    examples = all_examples[item][:n]
    result = []
    for ex in examples:
        result.append({
            'verse_id': ex['verse_id'],
            'tedim': ex.get('tedim_text', ''),
            'segmented': ex.get('segmented', ''),
            'glossed': ex.get('glossed', ''),
            'english': ex.get('kjv_text', '')
        })
    return result


def get_sense_examples(lemma: str, target_gloss: str, senses: Dict[str, List[dict]], 
                       all_examples: Dict[str, List[dict]], n: int = 3) -> List[Dict[str, str]]:
    """
    Get examples that match a specific sense/gloss for a lemma.
    
    This ensures examples support the entry's chosen gloss, not a conflicting sense.
    """
    result = []
    
    # First try to get sense-specific examples from senses data
    if lemma in senses:
        for sense in senses[lemma]:
            sense_gloss = sense.get('gloss', '')
            if sense_gloss == target_gloss or sense_gloss.upper() == target_gloss.upper():
                # Found matching sense - get its examples
                ex_verses = sense.get('example_verses', '').split('|')
                for verse_id in ex_verses[:n]:
                    if verse_id and lemma in all_examples:
                        # Find the example with this verse_id
                        for ex in all_examples[lemma]:
                            if ex.get('verse_id') == verse_id:
                                result.append({
                                    'verse_id': ex['verse_id'],
                                    'tedim': ex.get('tedim_text', ''),
                                    'segmented': ex.get('segmented', ''),
                                    'glossed': ex.get('glossed', ''),
                                    'english': ex.get('kjv_text', '')
                                })
                                break
                    if len(result) >= n:
                        break
                break  # Found matching sense
    
    # Fallback to regular examples if sense-specific not available
    if len(result) < n:
        fallback = get_entry_examples(lemma, all_examples, n - len(result))
        result.extend(fallback)
    
    return result[:n]


def format_lexical_entry(lemma: dict, examples: List[Dict[str, str]]) -> str:
    """Format a lexical stem entry."""
    lines = []
    lines.append(f"### {lemma['lemma']}")
    lines.append("")
    lines.append(f"**Citation form:** {lemma.get('citation_form', lemma['lemma'])}")
    lines.append(f"**POS:** {lemma['pos']}")
    
    # Handle gloss display based on entry status
    entry_status = lemma.get('entry_status', 'auto')
    gloss = lemma.get('primary_gloss', '')
    review_summary = lemma.get('review_gloss_summary', '')
    
    if entry_status in ('polysemous_review', 'mixed_lex_gram', 'unsafe_gloss'):
        # Show uncertainty explicitly
        if review_summary:
            lines.append(f"**Gloss candidates:** {review_summary}")
        elif gloss and gloss != '?':
            lines.append(f"**Primary gloss:** {gloss} (needs review)")
        else:
            lines.append(f"**Gloss:** ? (needs review)")
    else:
        # Clean entry - show confident gloss
        if gloss and gloss != '?':
            lines.append(f"**Gloss:** {gloss}")
        else:
            eng_glosses = lemma.get('english_glosses', '')
            if eng_glosses:
                gloss = eng_glosses.split('|')[0] if '|' in eng_glosses else eng_glosses
                lines.append(f"**Gloss:** {gloss}")
            else:
                lines.append(f"**Gloss:** ?")
    
    # Show gloss frequency distribution for polysemous items
    gloss_counts = lemma.get('gloss_counts', '')
    if lemma.get('is_polysemous') == '1' and gloss_counts:
        top_glosses = gloss_counts.split('|')[:3]
        lines.append(f"**Gloss distribution:** {', '.join(top_glosses)}")
    
    lines.append(f"**Frequency:** {lemma['token_count']} tokens")
    
    # Attested forms
    forms_str = lemma.get('inflected_forms', '')
    if forms_str:
        forms = forms_str.split('|')[:5]
        if forms and forms[0]:
            lines.append(f"**Attested forms:** {', '.join(forms)}")
    
    # Entry status note
    if entry_status == 'polysemous_review':
        lines.append(f"**Note:** Polysemous - gloss may vary by context")
    elif entry_status == 'mixed_lex_gram':
        lines.append(f"**Note:** Mixed lexical/grammatical - needs sense separation")
    
    # Grammaticalization notes
    gram_notes = lemma.get('grammaticalization_notes', '')
    if gram_notes:
        lines.append(f"**Usage:** {gram_notes}")
    
    # Examples
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            tedim = ex.get('tedim', '')
            english = ex.get('english', '')
            segmented = ex.get('segmented', '')
            glossed = ex.get('glossed', '')
            lines.append(f"{i}. [{ex['verse_id']}] {tedim}")
            if segmented and glossed:
                lines.append(f"   *{segmented}* / {glossed}")
            if english:
                lines.append(f"   — {english}")
    
    lines.append("")
    return '\n'.join(lines)


def format_grammatical_entry(item: dict, examples: List[Dict[str, str]], senses: Dict[str, List[dict]] = None) -> str:
    """Format a grammatical word entry with proper POS labeling."""
    lines = []
    lemma = item.get('lemma', item.get('form', '?'))
    lines.append(f"### {lemma}")
    lines.append("")
    lines.append(f"**Citation form:** {item.get('citation_form', lemma)}")
    
    # For grammatical entries, show FUNC as POS, not the raw lemma POS
    raw_pos = item.get('pos', 'FUNC')
    gloss = item.get('primary_gloss', '')
    
    # Determine display POS - grammatical items should show FUNC or particle type
    if raw_pos in ('V', 'N', 'UNK'):
        # Check if gloss indicates grammatical function
        if gloss and (gloss.isupper() or gloss in ('say', 'be', 'and', 'or', 'that', 'this')):
            display_pos = 'FUNC'  # Grammaticalized
        else:
            display_pos = raw_pos
    else:
        display_pos = raw_pos
    
    lines.append(f"**POS:** {display_pos}")
    
    # Get gloss from primary_gloss or english_glosses
    if not gloss or gloss == '?':
        eng_glosses = item.get('english_glosses', item.get('gloss', ''))
        if eng_glosses:
            gloss = eng_glosses.split('|')[0] if '|' in eng_glosses else eng_glosses
    lines.append(f"**Gloss:** {gloss if gloss else '?'}")
    
    lines.append(f"**Category:** {item.get('category', 'function word')}")
    freq = item.get('token_count', item.get('frequency', '?'))
    lines.append(f"**Frequency:** {freq} tokens")
    
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            tedim = ex.get('tedim', '')
            english = ex.get('english', '')
            lines.append(f"{i}. [{ex['verse_id']}] {tedim}")
            if english:
                lines.append(f"   — {english}")
    
    lines.append("")
    return '\n'.join(lines)


def format_affix_entry(morpheme: dict, examples: List[Dict[str, str]]) -> str:
    """Format an affix entry."""
    lines = []
    form = morpheme['form']
    category = morpheme['category']
    
    # Determine if prefix or suffix based on category
    if category in ('pronominal_prefix', 'object_prefix', 'object_marker'):
        display = f"{form}-"
    else:
        display = f"-{form}"
    
    lines.append(f"### {display}")
    lines.append("")
    lines.append(f"**Form:** {display}")
    lines.append(f"**Gloss:** {morpheme.get('gloss', '?')}")
    lines.append(f"**Category:** {category}")
    lines.append(f"**Frequency:** {morpheme['frequency']} tokens")
    
    # Environments
    envs = morpheme.get('environments', '')
    if envs:
        lines.append(f"**Environments:** {envs}")
    
    # Polysemy note
    if morpheme.get('is_polysemous') == '1':
        lines.append(f"**Note:** Polysemous form")
    
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            tedim = ex.get('tedim', '')
            english = ex.get('english', '')
            lines.append(f"{i}. [{ex['verse_id']}] {tedim}")
            if english:
                lines.append(f"   — {english}")
    
    lines.append("")
    return '\n'.join(lines)


def select_review_entries(lemmas: Dict[str, dict], n: int = 50) -> List[dict]:
    """
    Select entries that need review (polysemous, mixed, unsafe).
    
    These are high-frequency items that were excluded from polished output
    but are important for dictionary work.
    """
    # Known problematic forms that need review
    REVIEW_FORMS = {'hi', 'ding', 'ahih', 'ahi', 'hong', 'khat', 'lai', 'mahmah', 
                    'thei', 'pan', 'ta', 'te', 'in', 'na', 'tung', 'om', 'thu',
                    'mu', 'kha', 'ci', 'tawh', 'zo', 'za', 'bang',
                    # User-identified problem forms
                    'ciang', 'zong', 'leh', 'maw', 'hiam', 'zawh', 'suan', 'kua',
                    'hangin', 'ciangin', 'bangin', 'mahin'}
    
    review = []
    
    # Add explicitly flagged items
    for l in lemmas.values():
        status = l.get('entry_status', 'auto')
        if status in ('polysemous_review', 'mixed_lex_gram', 'unsafe_gloss'):
            if int(l['token_count']) > 100:
                review.append(l)
        elif l['lemma'].lower() in REVIEW_FORMS:
            review.append(l)
    
    # Sort by frequency (most important first)
    review.sort(key=lambda x: -int(x['token_count']))
    
    # Increase limit to include more problem forms
    return review[:max(n, 100)]


def format_review_entry(lemma: dict, examples: List[Dict[str, str]]) -> str:
    """Format a review entry with full uncertainty information."""
    lines = []
    lines.append(f"### {lemma['lemma']}")
    lines.append("")
    lines.append(f"**Citation form:** {lemma.get('citation_form', lemma['lemma'])}")
    lines.append(f"**POS:** {lemma.get('pos', 'UNK')}")
    lines.append(f"**Entry status:** {lemma.get('entry_status', 'auto')}")
    # Handle both lemma (token_count) and morpheme (frequency) formats
    freq = lemma.get('token_count', lemma.get('frequency', 0))
    lines.append(f"**Frequency:** {freq} tokens")
    
    # Show all gloss information
    review_summary = lemma.get('review_gloss_summary', '')
    primary_gloss = lemma.get('primary_gloss', '')
    gloss_counts = lemma.get('gloss_counts', '')
    
    if review_summary:
        lines.append(f"**Gloss candidates:** {review_summary}")
    if primary_gloss and primary_gloss != '?':
        lines.append(f"**Tentative primary:** {primary_gloss}")
    if gloss_counts:
        top_glosses = gloss_counts.split('|')[:5]
        lines.append(f"**Corpus distribution:** {', '.join(top_glosses)}")
    
    # Status flags
    flags = []
    if lemma.get('is_polysemous') == '1':
        flags.append('polysemous')
    if lemma.get('is_grammatical') == '1':
        flags.append('primarily_grammatical')
    if lemma.get('needs_review') == '1':
        flags.append('needs_review')
    if flags:
        lines.append(f"**Flags:** {', '.join(flags)}")
    
    # Grammaticalization notes
    gram_notes = lemma.get('grammaticalization_notes', '')
    if gram_notes:
        lines.append(f"**Notes:** {gram_notes}")
    
    # Review questions
    status = lemma.get('entry_status', '')
    if status == 'mixed_lex_gram':
        lines.append("**Review question:** Should this be split into lexical and grammatical senses?")
    elif status == 'polysemous_review':
        lines.append("**Review question:** Which is the primary sense?")
    elif status == 'unsafe_gloss':
        lines.append("**Review question:** What is the correct gloss?")
    
    # Examples
    if examples:
        lines.append("")
        lines.append("**Examples (for review):**")
        for i, ex in enumerate(examples[:5], 1):
            tedim = ex.get('tedim', '')
            english = ex.get('english', '')
            segmented = ex.get('segmented', '')
            glossed = ex.get('glossed', '')
            lines.append(f"{i}. [{ex['verse_id']}] {tedim}")
            if segmented and glossed:
                lines.append(f"   *{segmented}* / {glossed}")
            if english:
                lines.append(f"   — {english}")
    
    lines.append("")
    return '\n'.join(lines)


def generate_review_file(lemmas: Dict[str, dict], morphemes: Dict[str, dict],
                         senses: Dict[str, List[dict]], all_examples: Dict[str, List[dict]]):
    """Generate review_entries.md with items needing human review.
    
    This now includes:
    - High-frequency lemmas that failed clean checks
    - Grammatical words not clean enough for polished sample
    - Affixes with mixed/problematic categorization
    """
    review = select_review_entries(lemmas, 50)
    
    # Add grammatical words that didn't make the polished cut
    gram_review = []
    for lemma, l in lemmas.items():
        freq = l.get('frequency', 0)
        # High-frequency items that failed clean grammatical check
        if freq >= 100 and lemma in GRAMMATICAL_REVIEW_NEEDED:
            gram_review.append({
                'lemma': lemma,
                'frequency': freq,
                'primary_gloss': l.get('primary_gloss', '?'),
                'pos': l.get('pos', 'UNK'),
                'entry_status': 'grammatical_review_needed',
                'gloss_distribution': l.get('gloss_distribution', {})
            })
    
    # Add mixed-category affixes that didn't make polished cut
    affix_review = []
    for form, m in morphemes.items():
        category = m.get('category', '')
        if m.get('dominant_gloss') and not is_clean_affix(m):
            affix_review.append({
                'form': form,
                'lemma': form,  # for formatting
                'frequency': m.get('frequency', 0),
                'primary_gloss': m.get('dominant_gloss', '?'),
                'pos': f"AFFIX ({category})",
                'entry_status': 'affix_review_needed',
                'environments': m.get('environments', ''),
                'gloss_distribution': {}
            })
    
    output = []
    output.append("# Tedim Chin: Entries Requiring Review")
    output.append("")
    output.append("These entries were excluded from the polished sample dictionary because")
    output.append("they have unresolved gloss ambiguity, mixed lexical/grammatical status,")
    output.append("or other issues requiring human review.")
    output.append("")
    output.append(f"**Total entries:** {len(review) + len(gram_review) + len(affix_review)}")
    output.append("")
    output.append("## Review Categories")
    output.append("")
    
    # Categorize
    mixed = [l for l in review if l.get('entry_status') == 'mixed_lex_gram']
    polysemous = [l for l in review if l.get('entry_status') == 'polysemous_review']
    unsafe = [l for l in review if l.get('entry_status') == 'unsafe_gloss']
    other = [l for l in review if l.get('entry_status') not in ('mixed_lex_gram', 'polysemous_review', 'unsafe_gloss')]
    
    output.append(f"- Mixed lexical/grammatical: {len(mixed)}")
    output.append(f"- Polysemous (needs sense separation): {len(polysemous)}")
    output.append(f"- Unsafe gloss: {len(unsafe)}")
    output.append(f"- Grammatical words needing review: {len(gram_review)}")
    output.append(f"- Affixes needing review: {len(affix_review)}")
    output.append(f"- Other: {len(other)}")
    output.append("")
    output.append("---")
    output.append("")
    
    # Generate standard review entries
    for item in review:
        examples = get_entry_examples(item['lemma'], all_examples, 5)
        output.append(format_review_entry(item, examples))
    
    # Add grammatical review section
    if gram_review:
        output.append("---")
        output.append("")
        output.append("## Grammatical Words Needing Review")
        output.append("")
        output.append("These high-frequency grammatical items were excluded from the polished")
        output.append("sample due to mixed analysis, unclear function, or unresolved glosses.")
        output.append("")
        for item in sorted(gram_review, key=lambda x: -x['frequency']):
            examples = get_entry_examples(item['lemma'], all_examples, 5)
            output.append(format_review_entry(item, examples))
    
    # Add affix review section
    if affix_review:
        output.append("---")
        output.append("")
        output.append("## Affixes Needing Review")
        output.append("")
        output.append("These affixes have mixed categories, contradictory glosses, or")
        output.append("environment labels inconsistent with their function.")
        output.append("")
        for item in sorted(affix_review, key=lambda x: -x['frequency']):
            examples = get_entry_examples(item.get('form', item['lemma']), all_examples, 5)
            output.append(format_review_entry(item, examples))
    
    # Write output
    output_path = os.path.join(DATA_DIR, 'review_entries.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Generated {output_path}")
    return len(review) + len(gram_review) + len(affix_review)


def main():
    print("Loading export data...")
    lemmas = load_lemmas()
    morphemes = load_grammatical_morphemes()
    all_examples = load_examples()
    senses = load_senses()
    
    print(f"Loaded {len(lemmas)} lemmas, {len(morphemes)} morphemes, {len(all_examples)} example sets")
    
    # Select entries - now with quality over quantity
    lexical = select_lexical_stems(lemmas, 70)
    grammatical = select_grammatical_words(lemmas, morphemes, senses, max_n=20)
    affixes = select_affixes(morphemes, max_n=10)
    
    print(f"Selected: {len(lexical)} lexical, {len(grammatical)} grammatical, {len(affixes)} affixes")
    
    # Generate markdown
    output = []
    output.append("# Sample Dictionary Entries: Tedim Chin")
    output.append("")
    output.append("This file contains sample dictionary entries generated from the")
    output.append("full-Bible morphological analysis export.")
    output.append("")
    output.append("**Note:** These are 'clean' entries with reliable glosses. For polysemous")
    output.append("and ambiguous items requiring human review, see `review_entries.md`.")
    output.append("")
    output.append("**Quality policy:** Entries are included only if they pass strict quality")
    output.append("checks. The count is intentionally limited to maintain precision.")
    output.append("")
    output.append("**Contents:**")
    output.append(f"- {len(lexical)} lexical stems (nouns and verbs)")
    output.append(f"- {len(grammatical)} grammatical words (function words, particles)")
    output.append(f"- {len(affixes)} affixes and clitics")
    output.append("")
    output.append("---")
    output.append("")
    
    # Section 1: Lexical stems
    output.append("## Part 1: Lexical Stems")
    output.append("")
    
    for item in lexical[:70]:
        gloss = item.get('primary_gloss', '')
        examples = get_sense_examples(item['lemma'], gloss, senses, all_examples, 3)
        output.append(format_lexical_entry(item, examples))
    
    # Section 2: Grammatical words
    output.append("---")
    output.append("")
    output.append("## Part 2: Grammatical Words")
    output.append("")
    
    for item in grammatical:
        lemma = item.get('lemma', item.get('form', '?'))
        gloss = item.get('primary_gloss', '')
        examples = get_sense_examples(lemma, gloss, senses, all_examples, 3)
        output.append(format_grammatical_entry(item, examples, senses))
    
    # Section 3: Affixes
    output.append("---")
    output.append("")
    output.append("## Part 3: Affixes and Clitics")
    output.append("")
    
    for item in affixes:
        examples = get_entry_examples(item['form'], all_examples, 3)
        output.append(format_affix_entry(item, examples))
    
    # Write output
    output_path = os.path.join(DATA_DIR, 'sample_entries.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"\nGenerated {output_path}")
    print(f"Total entries: {len(lexical) + len(grammatical) + len(affixes)}")
    
    # Generate review entries - expanded to include items not in polished sample
    review_count = generate_review_file(lemmas, morphemes, senses, all_examples)
    print(f"Review entries: {review_count}")


if __name__ == '__main__':
    main()
