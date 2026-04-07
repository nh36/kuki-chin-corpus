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
    """Select n lexical stems, balanced between nouns and verbs."""
    verbs = [l for l in lemmas.values() if l['pos'] == 'V' and int(l['token_count']) > 50]
    nouns = [l for l in lemmas.values() if l['pos'] == 'N' and int(l['token_count']) > 50]
    
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
    """Select n grammatical words (function words, particles)."""
    selected = []
    
    # Get function words from lemmas
    func_words = [l for l in lemmas.values() if l['pos'] == 'FUNC' and int(l['token_count']) > 100]
    func_words.sort(key=lambda x: -int(x['token_count']))
    selected.extend(func_words[:10])
    
    # Also include high-frequency particles from morphemes
    particles = []
    for m in morphemes.values():
        if m['category'] in ('particle', 'sentence_final', 'auxiliary') and int(m['frequency']) > 500:
            particles.append({
                'lemma': m['form'],
                'pos': 'PTCL',
                'citation_form': m['form'],
                'english_glosses': m['gloss'],
                'attested_forms': m['form'],
                'token_count': m['frequency'],
                'category': m['category']
            })
    particles.sort(key=lambda x: -int(x['token_count']))
    selected.extend(particles[:10])
    
    # If still not enough, add some common words that function grammatically
    # (demonstratives, question words, conjunctions, etc.)
    common_grammatical = ['tua', 'hih', 'bang', 'kua', 'khempeuh', 'taktak', 'mahin', 
                          'zong', 'khat', 'leh', 'tawh', 'maw', 'hiam', 'cih', 'ahih',
                          'hangin', 'ciangin', 'bangin', 'peuh', 'bek', 'khit', 'suan',
                          'zawh', 'ding', 'lai', 'mahmah']
    for word in common_grammatical:
        if len(selected) >= n:
            break
        if word in lemmas and word not in [s.get('lemma', s.get('form')) for s in selected]:
            selected.append(lemmas[word])
    
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
    
    # Use primary_gloss first, fall back to english_glosses
    gloss = lemma.get('primary_gloss', '')
    if not gloss or gloss == '?':
        eng_glosses = lemma.get('english_glosses', '')
        if eng_glosses:
            gloss = eng_glosses.split('|')[0] if '|' in eng_glosses else eng_glosses
    lines.append(f"**Gloss:** {gloss if gloss else '?'}")
    
    # Show all English glosses if multiple
    all_eng = lemma.get('english_glosses', '')
    if all_eng and '|' in all_eng:
        lines.append(f"**All glosses:** {all_eng.replace('|', ', ')}")
    
    lines.append(f"**Frequency:** {lemma['token_count']} tokens")
    
    # Attested forms - field is now 'inflected_forms' with pipe delimiter
    forms_str = lemma.get('inflected_forms', '')
    if forms_str:
        forms = forms_str.split('|')[:5]
        if forms and forms[0]:
            lines.append(f"**Attested forms:** {', '.join(forms)}")
    
    # Polysemy flag
    if lemma.get('is_polysemous') == '1':
        lines.append(f"**Note:** Polysemous - needs review")
    
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
    output.append("This file contains 100 sample dictionary entries generated from the")
    output.append("full-Bible morphological analysis export.")
    output.append("")
    output.append("**Contents:**")
    output.append(f"- 70 lexical stems (nouns and verbs)")
    output.append(f"- 20 grammatical words (function words, particles)")
    output.append(f"- 10 affixes and clitics")
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


if __name__ == '__main__':
    main()
