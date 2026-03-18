#!/usr/bin/env python3
"""
Generate report of nominal postpositions (pan, tawh, panin, tawhin).

Shows nouns occurring with these postpositions, similar to paradigm reports
but focused on postpositional constructions rather than case suffixes.

Includes both:
- Separate postpositions: "sung pan" (inside from)
- Attached postpositions: "gampan" (land-from)

Usage:
    python generate_postposition_report.py              # Generate full report
    python generate_postposition_report.py --output FILE  # Write to file
"""

import sys
import re
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


# Gospel book codes (Matthew=40, Mark=41, Luke=42, John=43)
GOSPEL_BOOKS = {'40', '41', '42', '43'}


def select_diverse_samples(examples: List[Tuple], n: int = 3, verse_idx: int = 1) -> List[Tuple]:
    """
    Select up to n samples from different books, prioritizing gospels.
    
    Args:
        examples: List of tuples where verse_id is at position verse_idx
        n: Number of samples to select
        verse_idx: Index of verse_id in the tuple (default 1)
        
    Returns:
        List of up to n examples from different books, with gospel priority
    """
    if not examples:
        return []
    
    # Group by book
    by_book = defaultdict(list)
    for ex in examples:
        verse_id = ex[verse_idx] if len(ex) > verse_idx else ex[0]
        book = verse_id[:2] if len(verse_id) >= 2 else '00'
        by_book[book].append(ex)
    
    selected = []
    used_books = set()
    
    # First, try to get one from gospels
    for gospel in GOSPEL_BOOKS:
        if gospel in by_book and len(selected) < n:
            selected.append(by_book[gospel][0])
            used_books.add(gospel)
            break
    
    # Then fill with samples from different books
    for book in sorted(by_book.keys()):
        if book not in used_books and len(selected) < n:
            selected.append(by_book[book][0])
            used_books.add(book)
    
    # If still need more, take from any book not yet fully used
    if len(selected) < n:
        for book, exs in by_book.items():
            for ex in exs[1:]:  # Skip first (already used if this book was picked)
                if len(selected) >= n:
                    break
                if ex not in selected:
                    selected.append(ex)
    
    return selected[:n]


def find_postposition_contexts(corpus_file: str) -> Dict[str, List[Tuple[str, str, str, str, str]]]:
    """
    Find all instances of nouns with postpositions (both separate and attached).
    
    Returns: {postposition: [(noun, verse_id, context, form_type, full_word), ...]}
    where form_type is 'separate' or 'attached'
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
                
                # Check for SEPARATE postpositions (e.g., "sung pan")
                if word_clean in POSTPOSITIONS:
                    if i > 0:
                        prev_word = words[i - 1].strip('.,;:!?"')
                        start = max(0, i - 2)
                        end = min(len(words), i + 3)
                        context = ' '.join(words[start:end])
                        results[word_clean].append((prev_word, verse_id, context, 'separate', word_clean))
                
                # Check for ATTACHED postpositions (e.g., "gampan", "gampanin")
                # Must check panin before pan to avoid double-counting
                for postp in ['panin', 'pan', 'tawhin', 'tawh']:
                    if word_clean.endswith(postp) and len(word_clean) > len(postp):
                        stem = word_clean[:-len(postp)]
                        # Avoid matching words that just happen to end in these letters
                        # Require stem to be at least 2 chars
                        if len(stem) >= 2:
                            start = max(0, i - 2)
                            end = min(len(words), i + 3)
                            context = ' '.join(words[start:end])
                            results[postp].append((stem, verse_id, context, 'attached', word_clean))
                            break  # Don't double-count panin as pan
    
    return results


def analyze_by_noun(contexts: Dict[str, List]) -> Dict[str, Dict[str, List]]:
    """
    Reorganize contexts by the noun that precedes the postposition.
    
    Returns: {noun: {postposition: [(verse_id, context, form_type, full_word), ...]}}
    """
    by_noun = defaultdict(lambda: defaultdict(list))
    
    for postp, examples in contexts.items():
        for noun, verse_id, context, form_type, full_word in examples:
            by_noun[noun.lower()][postp].append((verse_id, context, form_type, full_word))
    
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


def generate_report(corpus_file: str, kjv_file: str) -> str:
    """Generate the full postposition report with KJV translations."""
    
    print("Loading KJV translations...", file=sys.stderr)
    kjv = load_kjv_translations(kjv_file)
    
    print("Finding postposition contexts...", file=sys.stderr)
    contexts = find_postposition_contexts(corpus_file)
    
    print("Analyzing by noun...", file=sys.stderr)
    by_noun = analyze_by_noun(contexts)
    top_nouns = get_top_nouns(by_noun, min_count=2)
    
    # Count separate vs attached forms
    sep_count = sum(1 for postp in contexts.values() for ex in postp if ex[3] == 'separate')
    att_count = sum(1 for postp in contexts.values() for ex in postp if ex[3] == 'attached')
    
    lines = [
        '# Tedim Chin Postposition Report',
        '',
        '## Overview',
        '',
        'This report documents nouns occurring with nominal postpositions.',
        'Includes both separate postpositions (*sung pan*) and attached forms (*gampan*).',
        '',
        '**Postpositions covered:**',
        '',
        '| Postposition | Gloss | Meaning | Separate | Attached | Total |',
        '|--------------|-------|---------|----------|----------|-------|',
    ]
    
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        examples = contexts[postp]
        sep = sum(1 for ex in examples if ex[3] == 'separate')
        att = sum(1 for ex in examples if ex[3] == 'attached')
        total_p = len(examples)
        lines.append(f'| {postp} | {gloss} | {meaning} | {sep:,} | {att:,} | {total_p:,} |')
    
    total = sum(len(c) for c in contexts.values())
    lines.append(f'| **Total** | | | {sep_count:,} | {att_count:,} | **{total:,}** |')
    
    lines.extend([
        '',
        '---',
        '',
        '## Summary Statistics',
        '',
        f'- **Total postposition instances**: {total:,}',
        f'- **Separate forms** (e.g., *sung pan*): {sep_count:,}',
        f'- **Attached forms** (e.g., *gampan*): {att_count:,}',
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
    
    for i, (noun, total_n, postp_counts) in enumerate(top_nouns[:50], 1):
        pan = postp_counts.get('pan', 0)
        panin = postp_counts.get('panin', 0)
        tawh = postp_counts.get('tawh', 0)
        tawhin = postp_counts.get('tawhin', 0)
        lines.append(f'| {i} | [{noun}](#{noun.replace(" ", "-")}) | {total_n} | {pan} | {panin} | {tawh} | {tawhin} |')
    
    lines.extend(['', '---', ''])
    
    # Detailed sections for each postposition with 3 diverse samples
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        examples = contexts[postp]
        lines.extend([
            f'## {postp.upper()} "{meaning}"',
            '',
            f'**Total occurrences**: {len(examples):,}',
            '',
        ])
        
        # Count by preceding word and collect samples
        word_samples = defaultdict(list)
        for noun, verse_id, context, form_type, full_word in examples:
            word_samples[noun.lower()].append((noun, verse_id, context, form_type, full_word))
        
        word_counts = {w: len(s) for w, s in word_samples.items()}
        top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:30]
        
        lines.extend([
            '### Most frequent preceding words',
            '',
            '| Word | Count | Sample 1 | Sample 2 | Sample 3 |',
            '|------|-------|----------|----------|----------|',
        ])
        
        for word, count in top_words:
            samples = word_samples.get(word, [])
            # Select diverse samples from different books
            diverse = select_diverse_samples(samples, 3, verse_idx=1)
            sample_cols = []
            for j in range(3):
                if j < len(diverse):
                    _, verse_id, context, _, _ = diverse[j]
                    kjv_text = kjv.get(verse_id, '')[:60] + ('...' if len(kjv.get(verse_id, '')) > 60 else '')
                    sample_cols.append(f'{format_verse_ref(verse_id)}: *{context}* — "{kjv_text}"')
                else:
                    sample_cols.append('—')
            lines.append(f'| {word} | {count} | {sample_cols[0]} | {sample_cols[1]} | {sample_cols[2]} |')
        
        lines.extend(['', '---', ''])
    
    # Detailed paradigm-style entries for top nouns
    lines.extend([
        '## Detailed Entries by Noun',
        '',
        'For each noun, showing all attested postposition combinations with 3 diverse samples each.',
        '',
    ])
    
    for noun, total_n, postp_counts in top_nouns[:100]:
        # Get gloss if it's a known noun
        gloss = NOUN_STEMS.get(noun, noun)
        
        lines.extend([
            f'### {noun}',
            f'**Gloss**: {gloss}',
            '',
            '| Postposition | Count | Sample 1 | Sample 2 | Sample 3 |',
            '|--------------|-------|----------|----------|----------|',
        ])
        
        for postp in ['pan', 'panin', 'tawh', 'tawhin']:
            examples_for_postp = by_noun[noun].get(postp, [])
            count = len(examples_for_postp)
            # Convert to tuple format for select_diverse_samples (verse_id is at index 0)
            examples_tuple = [(verse_id, context, form_type, full_word) for verse_id, context, form_type, full_word in examples_for_postp]
            diverse = select_diverse_samples(examples_tuple, 3, verse_idx=0)
            sample_cols = []
            for j in range(3):
                if j < len(diverse):
                    verse_id, context, form_type, full_word = diverse[j]
                    kjv_text = kjv.get(verse_id, '')[:50] + ('...' if len(kjv.get(verse_id, '')) > 50 else '')
                    sample_cols.append(f'{format_verse_ref(verse_id)}: *{context}* — "{kjv_text}"')
                else:
                    sample_cols.append('—')
            lines.append(f'| {postp} | {count} | {sample_cols[0]} | {sample_cols[1]} | {sample_cols[2]} |')
        
        lines.extend(['', '---', ''])
    
    return '\n'.join(lines)


def main():
    corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    kjv_file = str(Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv')
    
    import argparse
    parser = argparse.ArgumentParser(description='Generate postposition report')
    parser.add_argument('--output', '-o', help='Output file (default: docs/paradigms/postpositions.md)')
    args = parser.parse_args()
    
    report = generate_report(corpus_file, kjv_file)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / 'postpositions.md'
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')
    print(f"Written to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
