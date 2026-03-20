#!/usr/bin/env python3
"""
Generate TAM Markers Report for Tedim Chin

Documents the tense-aspect-mood suffix system.
"""

import sys
import os
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (analyze_word, gloss_sentence, 
                               TAM_SUFFIXES, VERBAL_DERIVATIONAL_SUFFIXES)

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
    '64': '3 John', '65': 'Jude', '66': 'Revelation',
}

GOSPEL_CODES = {'40', '41', '42', '43'}

def format_reference(ref):
    """Convert 01001001 to Genesis 1:1."""
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


def find_tam_examples(verses, suffix_pattern, limit=5, require_gospel=True):
    """Find diverse examples of a TAM suffix."""
    examples = []
    books_used = set()
    gospel_found = False
    
    for ref, text in sorted(verses.items()):
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if suffix_pattern in clean:
                book_code = ref[:2]
                
                # Skip if we already have this book
                if book_code in books_used:
                    continue
                
                # Track gospel status
                is_gospel = book_code in GOSPEL_CODES
                if is_gospel:
                    gospel_found = True
                
                analysis = analyze_word(clean)
                if analysis[1]:  # Has valid gloss
                    examples.append((ref, text, word, analysis))
                    books_used.add(book_code)
                    
                    if len(examples) >= limit:
                        if require_gospel and not gospel_found:
                            continue  # Keep looking for gospel
                        return examples
    
    return examples


def count_suffix_occurrences(verses):
    """Count TAM suffix occurrences."""
    counts = Counter()
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # Check for TAM suffixes
            for suffix in TAM_SUFFIXES:
                if clean.endswith(suffix) or suffix in clean:
                    counts[suffix] += 1
    
    return counts


def generate_report():
    """Generate TAM markers report."""
    print("Loading corpus...")
    verses = load_bible()
    
    print("Analyzing TAM markers...")
    counts = count_suffix_occurrences(verses)
    
    report = []
    report.append("# Tedim Chin TAM Markers")
    report.append("")
    report.append("This report documents the Tense-Aspect-Mood (TAM) suffix system in Tedim Chin.")
    report.append("")
    
    # Overview
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin expresses tense, aspect, and mood through verbal suffixes")
    report.append("attached after the verb stem. Multiple TAM markers can stack.")
    report.append("")
    report.append("### TAM Suffix Template")
    report.append("")
    report.append("```")
    report.append("VERB-STEM-(DERIV)-(ASPECT)-(DIRECTIONAL)-(MODAL)")
    report.append("```")
    report.append("")
    
    # Main TAM suffixes
    report.append("---")
    report.append("")
    report.append("## Core TAM Suffixes")
    report.append("")
    report.append("| Suffix | Gloss | Function | Attestations |")
    report.append("|--------|-------|----------|--------------|")
    
    core_tam = {
        'ding': ('IRR', 'Irrealis/Future'),
        'ta': ('PFV', 'Perfective'),
        'zo': ('COMPL', 'Completive'),
        'kik': ('ITER', 'Iterative/Again'),
        'nawn': ('CONT', 'Continuative'),
        'khin': ('IMM', 'Immediate'),
        'in': ('PROG', 'Progressive/Adverbial'),
        'lai': ('PROSP', 'Prospective'),
        'ning': ('DUB', 'Dubitative'),
        'thei': ('ABIL', 'Abilitative'),
    }
    
    for suffix, (gloss, func) in sorted(core_tam.items(), key=lambda x: -counts.get(x[0], 0)):
        count = counts.get(suffix, 0)
        report.append(f"| -{suffix} | {gloss} | {func} | {count}x |")
    
    report.append("")
    
    # Detailed sections for each TAM
    report.append("---")
    report.append("")
    report.append("## Detailed TAM Analysis")
    report.append("")
    
    # -ding (Irrealis)
    report.append("### -ding (Irrealis/Future)")
    report.append("")
    report.append("The irrealis marker expresses future, potential, or hypothetical events.")
    report.append("")
    examples = find_tam_examples(verses, 'ding', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -ta (Perfective)
    report.append("### -ta (Perfective)")
    report.append("")
    report.append("Marks completed actions, often with past time reference.")
    report.append("")
    examples = find_tam_examples(verses, 'ta', limit=3)
    for ref, text, word, analysis in examples:
        if 'PFV' in analysis[1] or '-ta' in analysis[0]:
            report.append(f"**{format_reference(ref)}**")
            report.append(f"> {text}")
            report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
            report.append("")
    
    # -zo (Completive)
    report.append("### -zo (Completive)")
    report.append("")
    report.append("Indicates action completed to its endpoint.")
    report.append("")
    examples = find_tam_examples(verses, 'zo', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -kik (Iterative)
    report.append("### -kik (Iterative/Repetitive)")
    report.append("")
    report.append("Marks repeated or returned action ('again').")
    report.append("")
    examples = find_tam_examples(verses, 'kik', limit=3)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # Directional suffixes
    report.append("---")
    report.append("")
    report.append("## Directional Suffixes")
    report.append("")
    report.append("Directional markers indicate the path of motion or orientation of action.")
    report.append("")
    report.append("| Suffix | Gloss | Meaning | Attestations |")
    report.append("|--------|-------|---------|--------------|")
    
    directionals = {
        'khia': ('out', 'Outward motion'),
        'lut': ('in', 'Inward motion'),
        'toh': ('up', 'Upward motion'),
        'khiat': ('away', 'Away from'),
        'cip': ('down', 'Downward motion'),
        'kik': ('back', 'Return motion'),
        'tang': ('arrive', 'Motion with arrival'),
    }
    
    for suffix, (gloss, meaning) in directionals.items():
        count = counts.get(suffix, 0)
        report.append(f"| -{suffix} | {gloss} | {meaning} | {count}x |")
    
    report.append("")
    
    # TAM stacking
    report.append("---")
    report.append("")
    report.append("## TAM Suffix Stacking")
    report.append("")
    report.append("Multiple TAM markers can combine on a single verb:")
    report.append("")
    report.append("| Pattern | Example | Gloss |")
    report.append("|---------|---------|-------|")
    report.append("| VERB-ITER-PFV | pai-kik-ta | go-ITER-PFV 'went again' |")
    report.append("| VERB-COMPL-IRR | bawl-zo-ding | make-COMPL-IRR 'will finish making' |")
    report.append("| VERB-out-PFV | khia-ta | go.out-PFV 'went out' |")
    report.append("| VERB-ABIL-IRR | bawl-thei-ding | make-ABIL-IRR 'will be able to make' |")
    report.append("")
    
    # Summary
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append("Tedim Chin TAM system features:")
    report.append("")
    report.append("1. **Core aspectual markers**: -ta (PFV), -zo (COMPL), -kik (ITER)")
    report.append("2. **Modal markers**: -ding (IRR), -thei (ABIL), -ning (DUB)")
    report.append("3. **Directional markers**: -khia, -lut, -toh, -cip")
    report.append("4. **Stacking**: Multiple markers can combine in fixed order")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'tam_markers.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
