#!/usr/bin/env python3
"""
Generate report of nominal postpositions (pan, tawh, panin, tawhin).

Shows nouns occurring with these postpositions, similar to paradigm reports
but focused on postpositional constructions rather than case suffixes.

Usage:
    python generate_postposition_report.py              # Generate full report
    python generate_postposition_report.py --output FILE  # Write to file
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import NOUN_STEMS, NOUN_STEM_TYPES, PROPER_NOUNS

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

# Postpositions to track
POSTPOSITIONS = {
    'pan': ('ABL', 'from'),
    'panin': ('ABL.ERG', 'from (as agent)'),
    'tawh': ('COM', 'with'),
    'tawhin': ('COM.ERG', 'with (as instrument)'),
}

def format_verse_ref(verse_id: str) -> str:
    """Convert BBCCCVVV format to readable form (e.g., 01002005 -> Gen 2:5)."""
    if len(verse_id) != 8:
        return verse_id
    book = verse_id[:2]
    chapter = str(int(verse_id[2:5]))
    verse = str(int(verse_id[5:8]))
    book_name = BOOK_ABBREVS.get(book, book)
    return f"{book_name} {chapter}:{verse}"


def find_postposition_contexts(corpus_file: str) -> Dict[str, List[Tuple[str, str, str, str]]]:
    """
    Find all instances of nouns followed by postpositions.
    
    Returns: {postposition: [(noun, verse_id, context_before, context_after), ...]}
    """
    results = {postp: [] for postp in POSTPOSITIONS}
    
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
                
                if word_clean in POSTPOSITIONS:
                    # Found a postposition - get preceding word
                    if i > 0:
                        prev_word = words[i - 1].strip('.,;:!?"')
                        # Get context (2 words before, 2 words after)
                        start = max(0, i - 2)
                        end = min(len(words), i + 3)
                        context = ' '.join(words[start:end])
                        
                        results[word_clean].append((prev_word, verse_id, context, word_clean))
    
    return results


def analyze_by_noun(contexts: Dict[str, List]) -> Dict[str, Dict[str, List]]:
    """
    Reorganize contexts by the noun that precedes the postposition.
    
    Returns: {noun: {postposition: [(verse_id, context), ...]}}
    """
    by_noun = defaultdict(lambda: defaultdict(list))
    
    for postp, examples in contexts.items():
        for noun, verse_id, context, _ in examples:
            by_noun[noun.lower()][postp].append((verse_id, context))
    
    return dict(by_noun)


def get_top_nouns(by_noun: Dict, min_count: int = 3) -> List[Tuple[str, int, Dict]]:
    """
    Get nouns with most postposition attestations.
    
    Returns: [(noun, total_count, {postp: count, ...}), ...]
    """
    results = []
    for noun, postps in by_noun.items():
        total = sum(len(examples) for examples in postps.values())
        if total >= min_count:
            postp_counts = {p: len(examples) for p, examples in postps.items()}
            results.append((noun, total, postp_counts))
    
    return sorted(results, key=lambda x: -x[1])


def generate_report(corpus_file: str) -> str:
    """Generate the full postposition report."""
    
    print("Finding postposition contexts...", file=sys.stderr)
    contexts = find_postposition_contexts(corpus_file)
    
    print("Analyzing by noun...", file=sys.stderr)
    by_noun = analyze_by_noun(contexts)
    top_nouns = get_top_nouns(by_noun, min_count=2)
    
    lines = [
        '# Tedim Chin Postposition Report',
        '',
        '## Overview',
        '',
        'This report documents nouns occurring with nominal postpositions.',
        'Unlike case suffixes (which attach directly to nouns), postpositions',
        'are separate words that follow the noun phrase.',
        '',
        '**Postpositions covered:**',
        '',
        '| Postposition | Gloss | Meaning | Count |',
        '|--------------|-------|---------|-------|',
    ]
    
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        count = len(contexts[postp])
        lines.append(f'| {postp} | {gloss} | {meaning} | {count:,} |')
    
    total = sum(len(c) for c in contexts.values())
    lines.append(f'| **Total** | | | **{total:,}** |')
    
    lines.extend([
        '',
        '---',
        '',
        '## Summary Statistics',
        '',
        f'- **Total postposition instances**: {total:,}',
        f'- **Unique preceding words**: {len(by_noun):,}',
        f'- **Words with 2+ instances**: {len(top_nouns):,}',
        '',
    ])
    
    # Top nouns by postposition usage
    lines.extend([
        '## Top Nouns by Postposition Usage',
        '',
        '| Rank | Noun | Total | pan | panin | tawh | tawhin |',
        '|------|------|-------|-----|-------|------|--------|',
    ])
    
    for i, (noun, total, postp_counts) in enumerate(top_nouns[:50], 1):
        pan = postp_counts.get('pan', 0)
        panin = postp_counts.get('panin', 0)
        tawh = postp_counts.get('tawh', 0)
        tawhin = postp_counts.get('tawhin', 0)
        lines.append(f'| {i} | [{noun}](#{noun.replace(" ", "-")}) | {total} | {pan} | {panin} | {tawh} | {tawhin} |')
    
    lines.extend(['', '---', ''])
    
    # Detailed sections for each postposition
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        examples = contexts[postp]
        lines.extend([
            f'## {postp.upper()} "{meaning}"',
            '',
            f'**Total occurrences**: {len(examples):,}',
            '',
        ])
        
        # Count by preceding word
        word_counts = defaultdict(int)
        for noun, _, _, _ in examples:
            word_counts[noun.lower()] += 1
        
        top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:30]
        
        lines.extend([
            '### Most frequent preceding words',
            '',
            '| Word | Count | Sample |',
            '|------|-------|--------|',
        ])
        
        # Get sample for each top word
        samples = defaultdict(list)
        for noun, verse_id, context, _ in examples:
            if len(samples[noun.lower()]) < 1:
                samples[noun.lower()].append((verse_id, context))
        
        for word, count in top_words:
            sample_list = samples.get(word, [])
            if sample_list:
                verse_id, context = sample_list[0]
                sample = f'{format_verse_ref(verse_id)}: *{context}*'
            else:
                sample = '—'
            lines.append(f'| {word} | {count} | {sample} |')
        
        lines.extend(['', '---', ''])
    
    # Detailed paradigm-style entries for top nouns
    lines.extend([
        '## Detailed Entries by Noun',
        '',
        'For each noun, showing all attested postposition combinations.',
        '',
    ])
    
    for noun, total, postp_counts in top_nouns[:100]:
        # Get gloss if it's a known noun
        gloss = NOUN_STEMS.get(noun, noun)
        
        lines.extend([
            f'### {noun}',
            f'**Gloss**: {gloss}',
            '',
            '| Postposition | Count | Sample |',
            '|--------------|-------|--------|',
        ])
        
        for postp in ['pan', 'panin', 'tawh', 'tawhin']:
            examples_for_postp = by_noun[noun].get(postp, [])
            count = len(examples_for_postp)
            if count > 0:
                verse_id, context = examples_for_postp[0]
                sample = f'{format_verse_ref(verse_id)}: *{context}*'
            else:
                sample = '—'
            lines.append(f'| {postp} | {count} | {sample} |')
        
        lines.extend(['', '---', ''])
    
    return '\n'.join(lines)


def main():
    corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    
    import argparse
    parser = argparse.ArgumentParser(description='Generate postposition report')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    args = parser.parse_args()
    
    report = generate_report(corpus_file)
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        print(f"Written to {output_path}", file=sys.stderr)
    else:
        # Default output location
        output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / 'postpositions.md'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding='utf-8')
        print(f"Written to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
