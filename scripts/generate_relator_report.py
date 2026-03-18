#!/usr/bin/env python3
"""
Generate report of relator nouns (spatial postpositions).

Relator nouns are spatial terms that function as postpositions:
- They take a genitive-marked possessor: mite' sungah "in the people"
- They can themselves be case-marked: sungah, sungin, sung pan

This report shows:
1. Frequency and distribution of each relator noun
2. What case markers they combine with
3. What types of possessors they take
4. Sample contexts with KJV translations

Usage:
    python generate_relator_report.py              # Generate full report
    python generate_relator_report.py --output FILE  # Write to file
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import RELATOR_NOUNS

# Book abbreviations for verse references
BOOK_ABBREVS = {
    '01': 'Gen', '02': 'Exo', '03': 'Lev', '04': 'Num', '05': 'Deu',
    '06': 'Jos', '07': 'Jdg', '08': 'Rut', '09': '1Sa', '10': '2Sa',
    '11': '1Ki', '12': '2Ki', '13': '1Ch', '14': '2Ch', '15': 'Ezr',
    '16': 'Neh', '17': 'Est', '18': 'Job', '19': 'Psa', '20': 'Pro',
    '21': 'Ecc', '22': 'Sol', '23': 'Isa', '24': 'Jer', '25': 'Lam',
    '26': 'Eze', '27': 'Dan', '28': 'Hos', '29': 'Joe', '30': 'Amo',
    '31': 'Oba', '32': 'Jon', '33': 'Mic', '34': 'Nah', '35': 'Hab',
    '36': 'Zep', '37': 'Hag', '38': 'Zec', '39': 'Mal',
    '40': 'Mat', '41': 'Mar', '42': 'Luk', '43': 'Joh', '44': 'Act',
    '45': 'Rom', '46': '1Co', '47': '2Co', '48': 'Gal', '49': 'Eph',
    '50': 'Phi', '51': 'Col', '52': '1Th', '53': '2Th', '54': '1Ti',
    '55': '2Ti', '56': 'Tit', '57': 'Phm', '58': 'Heb', '59': 'Jam',
    '60': '1Pe', '61': '2Pe', '62': '1Jo', '63': '2Jo', '64': '3Jo',
    '65': 'Jud', '66': 'Rev',
}

# Case forms that relator nouns can take
RELATOR_CASES = [
    ('', 'bare', 'Bare form'),
    ('ah', 'LOC', 'Locative'),
    ('in', 'ERG', 'Ergative'),
    (' pan', 'ABL', 'Ablative (separate)'),
    (' panin', 'ABL.ERG', 'Ablative-Ergative (separate)'),
]

def format_verse_ref(verse_id: str) -> str:
    """Convert BBCCCVVV format to readable form."""
    if len(verse_id) != 8:
        return verse_id
    book = verse_id[:2]
    chapter = str(int(verse_id[2:5]))
    verse = str(int(verse_id[5:8]))
    book_name = BOOK_ABBREVS.get(book, book)
    return f"{book_name} {chapter}:{verse}"


def load_kjv_translations(aligned_file: str) -> Dict[str, str]:
    """Load KJV translations from verses_aligned.tsv."""
    kjv = {}
    with open(aligned_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                verse_id = parts[0]
                kjv_text = parts[2]
                kjv[verse_id] = kjv_text
    return kjv


def find_relator_contexts(corpus_file: str) -> Dict[str, Dict[str, List]]:
    """
    Find all instances of relator nouns in their various case forms.
    
    Returns: {relator: {case_form: [(verse_id, context, preceding_word), ...]}}
    """
    results = {rel: defaultdict(list) for rel in RELATOR_NOUNS}
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            verse_id = parts[0]
            text = parts[1]
            words = text.split()
            
            for i, word in enumerate(words):
                word_clean = word.strip('.,;:!?"').lower()
                
                for relator, gloss in RELATOR_NOUNS.items():
                    # Check for various forms
                    
                    # Bare form
                    if word_clean == relator:
                        # Check if next word is pan or panin
                        next_word = words[i + 1].strip('.,;:!?"').lower() if i + 1 < len(words) else ''
                        if next_word == 'pan':
                            # This will be caught as "relator pan" form
                            continue
                        elif next_word == 'panin':
                            continue
                        else:
                            prev = words[i - 1] if i > 0 else ''
                            context = ' '.join(words[max(0, i-2):min(len(words), i+3)])
                            results[relator]['bare'].append((verse_id, context, prev))
                    
                    # With -ah (locative)
                    elif word_clean == f"{relator}ah":
                        prev = words[i - 1] if i > 0 else ''
                        context = ' '.join(words[max(0, i-2):min(len(words), i+3)])
                        results[relator]['ah'].append((verse_id, context, prev))
                    
                    # With -in (ergative)  
                    elif word_clean == f"{relator}in":
                        prev = words[i - 1] if i > 0 else ''
                        context = ' '.join(words[max(0, i-2):min(len(words), i+3)])
                        results[relator]['in'].append((verse_id, context, prev))
                    
                    # Check for "relator pan" (two words)
                    if word_clean == relator and i + 1 < len(words):
                        next_clean = words[i + 1].strip('.,;:!?"').lower()
                        if next_clean == 'pan':
                            prev = words[i - 1] if i > 0 else ''
                            context = ' '.join(words[max(0, i-2):min(len(words), i+4)])
                            results[relator]['pan'].append((verse_id, context, prev))
                        elif next_clean == 'panin':
                            prev = words[i - 1] if i > 0 else ''
                            context = ' '.join(words[max(0, i-2):min(len(words), i+4)])
                            results[relator]['panin'].append((verse_id, context, prev))
    
    return results


def analyze_possessors(contexts: Dict[str, Dict[str, List]]) -> Dict[str, Dict[str, int]]:
    """
    Analyze what words precede relator nouns (potential possessors).
    
    Returns: {relator: {preceding_word: count}}
    """
    results = {}
    for relator, case_forms in contexts.items():
        word_counts = defaultdict(int)
        for case_form, examples in case_forms.items():
            for verse_id, context, prev_word in examples:
                # Check if preceding word ends in genitive marker
                prev_clean = prev_word.strip('.,;:!?"')
                word_counts[prev_clean.lower()] += 1
        results[relator] = dict(word_counts)
    return results


def generate_report(corpus_file: str, kjv_file: str) -> str:
    """Generate the full relator noun report with KJV translations."""
    
    print("Loading KJV translations...", file=sys.stderr)
    kjv = load_kjv_translations(kjv_file)
    
    print("Finding relator noun contexts...", file=sys.stderr)
    contexts = find_relator_contexts(corpus_file)
    
    print("Analyzing possessors...", file=sys.stderr)
    possessors = analyze_possessors(contexts)
    
    lines = [
        '# Tedim Chin Relator Noun Report',
        '',
        '## Overview',
        '',
        'Relator nouns (also called "spatial postpositions" or "relational nouns")',
        'are a class of nouns with spatial meanings that function like postpositions.',
        '',
        '**Key properties:**',
        '1. They take a **genitive-marked possessor**: *mite\' sungah* "among the people"',
        '2. They can themselves be **case-marked**: *sungah* (LOC), *sungin* (ERG)',
        '3. They combine with **pan/panin** (ablative): *sung pan*, *sung panin*',
        '',
        '**Relator nouns in Tedim Chin:**',
        '',
        '| Relator | Gloss | Meaning |',
        '|---------|-------|---------|',
    ]
    
    for relator, gloss in sorted(RELATOR_NOUNS.items()):
        lines.append(f'| {relator} | {gloss} | spatial "{gloss}" |')
    
    lines.extend(['', '---', ''])
    
    # Summary statistics
    lines.extend([
        '## Summary Statistics',
        '',
        '| Relator | Bare | +ah (LOC) | +in (ERG) | + pan | + panin | **Total** |',
        '|---------|------|-----------|-----------|-------|---------|-----------|',
    ])
    
    grand_total = 0
    relator_totals = {}
    for relator in sorted(RELATOR_NOUNS.keys()):
        case_forms = contexts[relator]
        bare = len(case_forms.get('bare', []))
        ah = len(case_forms.get('ah', []))
        in_ = len(case_forms.get('in', []))
        pan = len(case_forms.get('pan', []))
        panin = len(case_forms.get('panin', []))
        total = bare + ah + in_ + pan + panin
        relator_totals[relator] = total
        grand_total += total
        lines.append(f'| [{relator}](#{relator}) | {bare:,} | {ah:,} | {in_:,} | {pan:,} | {panin:,} | **{total:,}** |')
    
    lines.append(f'| **Total** | | | | | | **{grand_total:,}** |')
    
    lines.extend(['', '---', ''])
    
    # Distribution chart (simple ASCII)
    lines.extend([
        '## Case Distribution',
        '',
        'Which cases do relator nouns most commonly appear in?',
        '',
    ])
    
    # Aggregate case counts
    case_totals = defaultdict(int)
    for relator, case_forms in contexts.items():
        for case_name, examples in case_forms.items():
            case_totals[case_name] += len(examples)
    
    lines.append('| Case | Count | Percentage |')
    lines.append('|------|-------|------------|')
    for case_name, count in sorted(case_totals.items(), key=lambda x: -x[1]):
        pct = 100 * count / grand_total if grand_total > 0 else 0
        bar = '█' * int(pct / 2)
        lines.append(f'| {case_name} | {count:,} | {pct:.1f}% {bar} |')
    
    lines.extend(['', '---', ''])
    
    # Detailed section for each relator noun
    for relator in sorted(RELATOR_NOUNS.keys(), key=lambda r: -relator_totals.get(r, 0)):
        gloss = RELATOR_NOUNS[relator]
        case_forms = contexts[relator]
        total = relator_totals[relator]
        
        lines.extend([
            f'## {relator}',
            '',
            f'**Gloss**: {gloss}',
            f'**Total occurrences**: {total:,}',
            '',
            '### Case Forms',
            '',
            '| Case | Form | Count | Sample 1 | Sample 2 | Sample 3 |',
            '|------|------|-------|----------|----------|----------|',
        ])
        
        case_order = ['bare', 'ah', 'in', 'pan', 'panin']
        case_labels = {
            'bare': ('Bare', relator),
            'ah': ('Locative', f'{relator}ah'),
            'in': ('Ergative', f'{relator}in'),
            'pan': ('Ablative', f'{relator} pan'),
            'panin': ('Abl-Erg', f'{relator} panin'),
        }
        
        for case_name in case_order:
            label, form = case_labels[case_name]
            examples = case_forms.get(case_name, [])
            count = len(examples)
            sample_cols = []
            for j in range(3):
                if j < len(examples):
                    verse_id, context, _ = examples[j]
                    kjv_text = kjv.get(verse_id, '')[:50] + ('...' if len(kjv.get(verse_id, '')) > 50 else '')
                    sample_cols.append(f'{format_verse_ref(verse_id)}: *{context}* — "{kjv_text}"')
                else:
                    sample_cols.append('—')
            lines.append(f'| {label} | {form} | {count:,} | {sample_cols[0]} | {sample_cols[1]} | {sample_cols[2]} |')
        
        # Top possessors (words that precede this relator)
        poss_counts = possessors.get(relator, {})
        top_poss = sorted(poss_counts.items(), key=lambda x: -x[1])[:15]
        
        if top_poss:
            lines.extend([
                '',
                '### Most Common Preceding Words (Possessors)',
                '',
                '| Word | Count | Notes |',
                '|------|-------|-------|',
            ])
            
            for word, count in top_poss:
                # Check if it ends in genitive marker
                notes = ''
                if word.endswith("'"):
                    notes = 'genitive-marked'
                elif word in ('a', 'ka', 'na', 'i', 'ko'):
                    notes = 'possessive prefix'
                lines.append(f'| {word} | {count} | {notes} |')
        
        # Sample sentences with KJV
        lines.extend([
            '',
            '### Sample Contexts with KJV',
            '',
        ])
        
        # Get 3 diverse samples from different case forms
        samples_shown = 0
        for case_name in case_order:
            examples = case_forms.get(case_name, [])
            for ex in examples[:1]:  # Take 1 from each case
                if samples_shown < 5:
                    verse_id, context, prev = ex
                    kjv_text = kjv.get(verse_id, 'N/A')
                    lines.append(f'- **{case_labels[case_name][0]}** ({format_verse_ref(verse_id)}):')
                    lines.append(f'  - Tedim: *{context}*')
                    lines.append(f'  - KJV: "{kjv_text}"')
                    lines.append('')
                    samples_shown += 1
        
        lines.extend(['', '---', ''])
    
    # Possessor patterns section
    lines.extend([
        '## Possessor Patterns',
        '',
        'Relator nouns typically follow a genitive-marked possessor.',
        'The genitive is marked with an apostrophe (glottal stop).',
        '',
        '**Pattern**: [POSSESSOR-GEN] [RELATOR-CASE]',
        '',
        'Examples:',
        "- *mite' sungah* = people-GEN inside-LOC = 'among the people'",
        "- *inn' tungah* = house-GEN on-LOC = 'on the house'",
        "- *amau' kiangah* = they-GEN beside-LOC = 'beside them'",
        '',
        '### Most Common Possessors Across All Relators',
        '',
        '| Word | Total Count | Notes |',
        '|------|-------------|-------|',
    ])
    
    # Aggregate possessor counts
    all_poss = defaultdict(int)
    for relator, poss_dict in possessors.items():
        for word, count in poss_dict.items():
            all_poss[word] += count
    
    top_all_poss = sorted(all_poss.items(), key=lambda x: -x[1])[:25]
    for word, count in top_all_poss:
        notes = ''
        if word.endswith("'"):
            notes = 'genitive-marked'
        elif word in ('a', 'ka', 'na', 'i', 'ko'):
            notes = 'possessive prefix'
        lines.append(f'| {word} | {count:,} | {notes} |')
    
    return '\n'.join(lines)


def main():
    corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    
    import argparse
    parser = argparse.ArgumentParser(description='Generate relator noun report')
    parser.add_argument('--output', '-o', help='Output file (default: docs/paradigms/relator_nouns.md)')
    args = parser.parse_args()
    
    kjv_file = str(Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv')
    report = generate_report(corpus_file, kjv_file)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / 'relator_nouns.md'
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')
    print(f"Written to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
