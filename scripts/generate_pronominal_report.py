#!/usr/bin/env python3
"""
Generate Pronominal Marking Report for Tedim Chin

Documents subject and object agreement prefixes on verbs.
"""

import sys
import os
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (analyze_word, gloss_sentence,
                               PRONOMINAL_CONCORD, OBJECT_PREFIXES)

# Book names
BOOK_NAMES = {
    '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus', '04': 'Numbers',
    '05': 'Deuteronomy', '06': 'Joshua', '07': 'Judges', '08': 'Ruth',
    '09': '1 Samuel', '10': '2 Samuel', '11': '1 Kings', '12': '2 Kings',
    '13': '1 Chronicles', '14': '2 Chronicles', '15': 'Ezra', '16': 'Nehemiah',
    '17': 'Esther', '18': 'Job', '19': 'Psalms', '20': 'Proverbs',
    '21': 'Ecclesiastes', '22': 'Song of Solomon', '23': 'Isaiah', '24': 'Jeremiah',
    '25': 'Lamentations', '26': 'Ezekiel', '27': 'Daniel', '28': 'Hosea',
    '29': 'Joel', '30': 'Amos', '31': 'Obadiah', '32': 'Jonah',
    '33': 'Micah', '34': 'Nahum', '35': 'Habakkuk', '36': 'Zephaniah',
    '37': 'Haggai', '38': 'Zechariah', '39': 'Malachi',
    '40': 'Matthew', '41': 'Mark', '42': 'Luke', '43': 'John',
    '44': 'Acts', '45': 'Romans', '46': '1 Corinthians', '47': '2 Corinthians',
    '48': 'Galatians', '49': 'Ephesians', '50': 'Philippians', '51': 'Colossians',
    '52': '1 Thessalonians', '53': '2 Thessalonians', '54': '1 Timothy', '55': '2 Timothy',
    '56': 'Titus', '57': 'Philemon', '58': 'Hebrews', '59': 'James',
    '60': '1 Peter', '61': '2 Peter', '62': '1 John', '63': '2 John',
    '64': 'John', '65': 'Jude', '66': 'Revelation',
}

GOSPEL_CODES = {'40', '41', '42', '43'}

def format_reference(ref):
    """Convert 01001001 to Genesis 1:1."""
    if len(ref) != 8 or not ref.isdigit():
        return ref  # Return as-is if not standard format
    book_code = ref[:2]
    chapter = int(ref[2:5])
    verse = int(ref[5:8])
    book_name = BOOK_NAMES.get(book_code, f'Book {book_code}')
    return f"{book_name} {chapter}:{verse}"


def load_bible():
    """Load Bible text."""
    bible_path = os.path.join(os.path.dirname(__file__), 
                              '..', 'bibles', 'extracted', 'ctd', 'ctd-x-bible.txt')
    verses = {}
    with open(bible_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                ref, text = line.strip().split('\t', 1)
                verses[ref] = text
    return verses


def find_prefix_examples(verses, prefix, limit=3):
    """Find examples of a pronominal prefix."""
    examples = []
    books_used = set()
    
    for ref, text in sorted(verses.items()):
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if clean.startswith(prefix):
                book_code = ref[:2]
                if book_code in books_used:
                    continue
                
                analysis = analyze_word(clean)
                if analysis[1] and prefix.upper() in analysis[1].upper():
                    examples.append((ref, text, word, analysis))
                    books_used.add(book_code)
                    
                    if len(examples) >= limit:
                        return examples
    
    return examples


def count_prefixes(verses):
    """Count prefix occurrences."""
    counts = Counter()
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # Check subject prefixes
            for prefix in PRONOMINAL_CONCORD:
                if clean.startswith(prefix):
                    counts[prefix] += 1
                    break
            # Check object prefixes
            for prefix in OBJECT_PREFIXES:
                if clean.startswith(prefix):
                    counts[prefix] += 1
    
    return counts


def generate_report():
    """Generate pronominal marking report."""
    print("Loading corpus...")
    verses = load_bible()
    
    print("Analyzing pronominal markers...")
    counts = count_prefixes(verses)
    
    report = []
    report.append("# Tedim Chin Pronominal Marking")
    report.append("")
    report.append("This report documents the verbal agreement system in Tedim Chin.")
    report.append("")
    
    # Overview
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin verbs agree with their subjects through prefixes.")
    report.append("The system distinguishes person and number, with a special")
    report.append("inclusive/exclusive distinction in first person plural.")
    report.append("")
    
    # Subject agreement
    report.append("---")
    report.append("")
    report.append("## Subject Agreement Prefixes")
    report.append("")
    report.append("| Person | Prefix | Gloss | Example | Attestations |")
    report.append("|--------|--------|-------|---------|--------------|")
    
    subject_prefixes = [
        ('1SG', 'ka-', '1SG', 'ka-pai (I go)'),
        ('2SG', 'na-', '2SG', 'na-pai (you go)'),
        ('3SG', 'a-', '3SG', 'a-pai (he/she goes)'),
        ('1PL.INCL', 'i-', '1PL.INCL', 'i-pai (we all go)'),
        ('1PL.EXCL', 'ka-', '1PL.EXCL', 'ka-pai-uh (we [excl] go)'),
        ('2PL', 'na-', '2PL', 'na-pai-uh (you all go)'),
        ('3PL', 'a-', '3PL', 'a-pai-uh (they go)'),
    ]
    
    for person, prefix, gloss, example in subject_prefixes:
        prefix_key = prefix.rstrip('-')
        count = counts.get(prefix_key, 0)
        report.append(f"| {person} | {prefix} | {gloss} | {example} | {count}x |")
    
    report.append("")
    
    # Paradigm table
    report.append("### Full Paradigm with 'pai' (go)")
    report.append("")
    report.append("| | Singular | Plural |")
    report.append("|---|----------|--------|")
    report.append("| 1 | ka-pai | ka-pai-uh (excl) / i-pai (incl) |")
    report.append("| 2 | na-pai | na-pai-uh |")
    report.append("| 3 | a-pai | a-pai-uh |")
    report.append("")
    
    # Object/Inverse prefixes
    report.append("---")
    report.append("")
    report.append("## Object/Inverse Prefixes")
    report.append("")
    report.append("Tedim Chin uses portmanteau prefixes to mark both subject and object.")
    report.append("")
    report.append("| Prefix | Function | Gloss | Example | Attestations |")
    report.append("|--------|----------|-------|---------|--------------|")
    
    object_prefixes = [
        ('kong-', '1SG→3', '1SG>3', 'kong-mu (I see him/her)'),
        ('hong-', '3→1/2', '3>1/2', 'hong-mu (he sees me)'),
        ('ni-', '2→1', '2>1', 'ni-mu (you see me)'),
    ]
    
    for prefix, func, gloss, example in object_prefixes:
        prefix_key = prefix.rstrip('-')
        count = counts.get(prefix_key, 0)
        report.append(f"| {prefix} | {func} | {gloss} | {example} | {count}x |")
    
    report.append("")
    
    # Direction/Inverse system
    report.append("### Direction System")
    report.append("")
    report.append("The object prefixes encode a hierarchy: 1 > 2 > 3")
    report.append("")
    report.append("- **Direct** (higher acts on lower): kong- 'I→him'")
    report.append("- **Inverse** (lower acts on higher): hong- 'he→me'")
    report.append("")
    
    # Examples with glosses
    report.append("---")
    report.append("")
    report.append("## Illustrated Examples")
    report.append("")
    
    # ka- examples
    report.append("### ka- (1SG)")
    report.append("")
    examples = find_prefix_examples(verses, 'ka', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # a- examples
    report.append("### a- (3SG)")
    report.append("")
    examples = find_prefix_examples(verses, 'a', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # hong- examples
    report.append("### hong- (3→1/2 Inverse)")
    report.append("")
    examples = find_prefix_examples(verses, 'hong', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # Summary
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append("The Tedim Chin pronominal system features:")
    report.append("")
    report.append("1. **Obligatory subject agreement** via prefixes (ka-, na-, a-, i-)")
    report.append("2. **Inclusive/exclusive distinction** in 1PL (i- vs ka-...-uh)")
    report.append("3. **Plural suffix -uh** combines with prefixes for plural subjects")
    report.append("4. **Inverse marking** with hong- for SAP objects of 3rd person subjects")
    report.append("5. **Direct marking** with kong- for 1SG acting on 3rd person")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'pronominal_marking.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
