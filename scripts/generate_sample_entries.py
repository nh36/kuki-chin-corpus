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
    """Select n affixes/clitics."""
    affixes = []
    
    # Case markers
    case_markers = [m for m in morphemes.values() if m['category'] == 'case']
    case_markers.sort(key=lambda x: -int(x['frequency']))
    
    # TAM markers
    tam_markers = [m for m in morphemes.values() if m['category'] == 'tam']
    tam_markers.sort(key=lambda x: -int(x['frequency']))
    
    # Pronominal prefixes
    pronominal = [m for m in morphemes.values() if m['category'] == 'pronominal_prefix']
    pronominal.sort(key=lambda x: -int(x['frequency']))
    
    # Nominalizers
    nominalizers = [m for m in morphemes.values() if m['category'] == 'nominalizer']
    nominalizers.sort(key=lambda x: -int(x['frequency']))
    
    # Select mix
    affixes.extend(case_markers[:3])
    affixes.extend(tam_markers[:2])
    affixes.extend(pronominal[:3])
    affixes.extend(nominalizers[:2])
    
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
            'gloss': '',
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
    lines.append(f"**Gloss:** {lemma.get('english_glosses', '?')}")
    lines.append(f"**Frequency:** {lemma['token_count']} tokens")
    
    # Attested forms
    forms = lemma.get('attested_forms', '').split('; ')[:5]
    if forms and forms[0]:
        lines.append(f"**Attested forms:** {', '.join(forms)}")
    
    # Examples
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            lines.append(f"{i}. [{ex['verse_id']}] {ex.get('tedim', '')} — {ex.get('english', '')}")
    
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
    lines.append(f"**Gloss:** {item.get('english_glosses', item.get('gloss', '?'))}")
    lines.append(f"**Category:** {item.get('category', 'function word')}")
    freq = item.get('token_count', item.get('frequency', '?'))
    lines.append(f"**Frequency:** {freq} tokens")
    
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            lines.append(f"{i}. [{ex['verse_id']}] {ex.get('tedim', '')} — {ex.get('english', '')}")
    
    lines.append("")
    return '\n'.join(lines)


def format_affix_entry(morpheme: dict, examples: List[Dict[str, str]]) -> str:
    """Format an affix entry."""
    lines = []
    form = morpheme['form']
    category = morpheme['category']
    
    # Determine if prefix or suffix
    if category in ('pronominal_prefix', 'object_prefix'):
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
        lines.append(f"**Environments:** {envs[:100]}...")
    
    if examples:
        lines.append("")
        lines.append("**Examples:**")
        for i, ex in enumerate(examples[:3], 1):
            lines.append(f"{i}. [{ex['verse_id']}] {ex.get('tedim', '')} — {ex.get('english', '')}")
    
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
