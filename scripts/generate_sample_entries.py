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
    """Load grammatical morphemes from TSV file."""
    morphemes = {}
    path = os.path.join(DATA_DIR, 'grammatical_morphemes.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            morphemes[row['form']] = row
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


def select_grammatical_words(lemmas: Dict[str, dict], morphemes: Dict[str, dict], n: int = 20) -> List[dict]:
    """
    Select n grammatical words (function words, particles).
    
    Only includes items that are primarily grammatical in function.
    """
    selected = []
    seen_forms = set()
    
    # Forms that should only appear as grammatical entries
    GRAMMATICAL_ONLY = {'ahi', 'ahih', 'tua', 'hih', 'bang', 'kua', 'khempeuh', 
                        'maw', 'hiam', 'cih', 'hangin', 'ciangin', 'bangin', 
                        'peuh', 'bek', 'khit', 'suan', 'zawh'}
    
    # Get function words from lemmas (explicitly marked FUNC POS)
    func_words = [l for l in lemmas.values() 
                  if l['pos'] == 'FUNC' and int(l['token_count']) > 100]
    func_words.sort(key=lambda x: -int(x['token_count']))
    
    for fw in func_words[:12]:
        if fw['lemma'] not in seen_forms:
            selected.append(fw)
            seen_forms.add(fw['lemma'])
    
    # Add items that are marked as primarily grammatical
    gram_lemmas = [l for l in lemmas.values() 
                   if l.get('is_grammatical') == '1' 
                   and l['lemma'].lower() not in seen_forms
                   and int(l['token_count']) > 500]
    gram_lemmas.sort(key=lambda x: -int(x['token_count']))
    
    for gl in gram_lemmas[:8]:
        if len(selected) >= n:
            break
        selected.append(gl)
        seen_forms.add(gl['lemma'])
    
    # Fill with common grammatical words if needed
    common_grammatical = ['tua', 'hih', 'kua', 'khempeuh', 'taktak', 'mahin', 
                          'zong', 'leh', 'maw', 'hiam', 'cih',
                          'hangin', 'ciangin', 'bangin', 'peuh', 'bek']
    for word in common_grammatical:
        if len(selected) >= n:
            break
        if word in lemmas and word not in seen_forms:
            selected.append(lemmas[word])
            seen_forms.add(word)
    
    return selected[:n]


def select_affixes(morphemes: Dict[str, dict], n: int = 10) -> List[dict]:
    """Select n affixes/clitics from diverse categories."""
    affixes = []
    seen_forms = set()  # Avoid duplicates
    
    # Categories in order of priority
    categories = [
        ('case_marker', 2),
        ('tam_suffix', 2),
        ('irrealis_marker', 1),
        ('pronominal_prefix', 2),
        ('plural_marker', 1),
        ('sentence_final', 1),
        ('nominalizer', 1),
        ('auxiliary', 1),
        ('directional_verb', 1),
    ]
    
    for category, count in categories:
        items = [m for m in morphemes.values() 
                 if m['category'] == category and m['form'] not in seen_forms]
        items.sort(key=lambda x: -int(x['frequency']))
        for m in items[:count]:
            if len(affixes) < n:
                affixes.append(m)
                seen_forms.add(m['form'])
    
    return affixes[:n]


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


def format_grammatical_entry(item: dict, examples: List[Dict[str, str]]) -> str:
    """Format a grammatical word entry."""
    lines = []
    lemma = item.get('lemma', item.get('form', '?'))
    lines.append(f"### {lemma}")
    lines.append("")
    lines.append(f"**Citation form:** {item.get('citation_form', lemma)}")
    lines.append(f"**POS:** {item.get('pos', 'FUNC')}")
    
    # Get gloss from primary_gloss or english_glosses
    gloss = item.get('primary_gloss', '')
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
                    'mu', 'kha', 'ci', 'tawh', 'zo', 'za', 'bang'}
    
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
    
    return review[:n]


def format_review_entry(lemma: dict, examples: List[Dict[str, str]]) -> str:
    """Format a review entry with full uncertainty information."""
    lines = []
    lines.append(f"### {lemma['lemma']}")
    lines.append("")
    lines.append(f"**Citation form:** {lemma.get('citation_form', lemma['lemma'])}")
    lines.append(f"**POS:** {lemma['pos']}")
    lines.append(f"**Entry status:** {lemma.get('entry_status', 'auto')}")
    lines.append(f"**Frequency:** {lemma['token_count']} tokens")
    
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


def generate_review_file(lemmas: Dict[str, dict], all_examples: Dict[str, List[dict]]):
    """Generate review_entries.md with items needing human review."""
    review = select_review_entries(lemmas, 50)
    
    output = []
    output.append("# Tedim Chin: Entries Requiring Review")
    output.append("")
    output.append("These entries were excluded from the polished sample dictionary because")
    output.append("they have unresolved gloss ambiguity, mixed lexical/grammatical status,")
    output.append("or other issues requiring human review.")
    output.append("")
    output.append(f"**Total entries:** {len(review)}")
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
    output.append(f"- Other: {len(other)}")
    output.append("")
    output.append("---")
    output.append("")
    
    # Generate entries
    for item in review:
        examples = get_entry_examples(item['lemma'], all_examples, 5)
        output.append(format_review_entry(item, examples))
    
    # Write output
    output_path = os.path.join(DATA_DIR, 'review_entries.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"Generated {output_path}")
    return len(review)


def main():
    print("Loading export data...")
    lemmas = load_lemmas()
    morphemes = load_grammatical_morphemes()
    all_examples = load_examples()
    
    print(f"Loaded {len(lemmas)} lemmas, {len(morphemes)} morphemes, {len(all_examples)} example sets")
    
    # Select entries
    lexical = select_lexical_stems(lemmas, 70)
    grammatical = select_grammatical_words(lemmas, morphemes, 20)
    affixes = select_affixes(morphemes, 10)
    
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
        examples = get_entry_examples(item['lemma'], all_examples, 3)
        output.append(format_lexical_entry(item, examples))
    
    # Section 2: Grammatical words
    output.append("---")
    output.append("")
    output.append("## Part 2: Grammatical Words")
    output.append("")
    
    for item in grammatical[:20]:
        lemma = item.get('lemma', item.get('form', '?'))
        examples = get_entry_examples(lemma, all_examples, 3)
        output.append(format_grammatical_entry(item, examples))
    
    # Section 3: Affixes
    output.append("---")
    output.append("")
    output.append("## Part 3: Affixes and Clitics")
    output.append("")
    
    for item in affixes[:10]:
        examples = get_entry_examples(item['form'], all_examples, 3)
        output.append(format_affix_entry(item, examples))
    
    # Write output
    output_path = os.path.join(DATA_DIR, 'sample_entries.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output))
    
    print(f"\nGenerated {output_path}")
    print(f"Total entries: {len(lexical[:70]) + len(grammatical[:20]) + len(affixes[:10])}")
    
    # Generate review entries
    review_count = generate_review_file(lemmas, all_examples)
    print(f"Review entries: {review_count}")


if __name__ == '__main__':
    main()
