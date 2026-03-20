#!/usr/bin/env python3
"""
Generate TAM Markers Report for Tedim Chin

Documents the tense-aspect-mood suffix system.
"""

import sys
import os
import re
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word, gloss_sentence, TAM_SUFFIXES

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
    if len(ref) != 8 or not ref.isdigit():
        return ref
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


def load_kjv():
    """Load KJV translations from aligned verses."""
    kjv = {}
    aligned_path = os.path.join(os.path.dirname(__file__), 
                                '..', 'data', 'verses_aligned.tsv')
    with open(aligned_path, 'r', encoding='utf-8') as f:
        header = f.readline().strip().split('\t')
        kjv_idx = header.index('eng_King James Version') if 'eng_King James Version' in header else 2
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) > kjv_idx:
                ref = parts[0]
                kjv[ref] = parts[kjv_idx]
    return kjv


def find_tam_examples(verses, kjv, suffix_pattern, gloss_pattern, limit=3, require_gospel=True):
    """Find diverse examples of a TAM suffix with KJV translations.
    
    Uses gloss_pattern to verify the word actually contains the TAM marker.
    """
    examples = []
    books_used = set()
    gospel_found = False
    
    # First pass: try to include a Gospel example
    if require_gospel:
        for ref, text in sorted(verses.items()):
            if len(ref) != 8 or not ref.isdigit():
                continue
            book_code = ref[:2]
            if book_code not in GOSPEL_CODES:
                continue
            words = text.split()
            for word in words:
                clean = word.lower().rstrip('.,;:!?"\'')
                if suffix_pattern in clean:
                    analysis = analyze_word(clean)
                    # Check if gloss contains the TAM marker
                    if analysis[1] and gloss_pattern in analysis[1]:
                        kjv_text = kjv.get(ref, '')
                        examples.append((ref, text, word, analysis, kjv_text))
                        books_used.add(book_code)
                        gospel_found = True
                        break
            if gospel_found:
                break
    
    # Second pass: fill remaining slots from diverse books
    for ref, text in sorted(verses.items()):
        if len(examples) >= limit:
            break
        if len(ref) != 8 or not ref.isdigit():
            continue
        book_code = ref[:2]
        if book_code in books_used:
            continue
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if suffix_pattern in clean:
                analysis = analyze_word(clean)
                # Check if gloss contains the TAM marker
                if analysis[1] and gloss_pattern in analysis[1]:
                    kjv_text = kjv.get(ref, '')
                    examples.append((ref, text, word, analysis, kjv_text))
                    books_used.add(book_code)
                    break
        if len(examples) >= limit:
            break
    
    return examples


def count_suffix_occurrences(verses):
    """Count TAM suffix occurrences by simple pattern matching."""
    counts = Counter()
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # Count by suffix presence in word
            if clean.endswith('ding') or 'ding' in clean:
                counts['ding'] += 1
            elif clean.endswith('ta') or 'ta ' in clean:
                counts['ta'] += 1
            elif 'zo' in clean:
                counts['zo'] += 1
            elif 'kik' in clean:
                counts['kik'] += 1
            elif clean.endswith('nawn') or 'nawn' in clean:
                counts['nawn'] += 1
            elif 'khin' in clean:
                counts['khin'] += 1
            elif clean.endswith('lai'):
                counts['lai'] += 1
            elif 'thei' in clean:
                counts['thei'] += 1
    
    return counts


def generate_report():
    """Generate TAM markers report."""
    print("Loading corpus...")
    verses = load_bible()
    kjv = load_kjv()
    
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
    
    # Main TAM suffixes - only true TAM markers
    report.append("---")
    report.append("")
    report.append("## Core TAM Suffixes")
    report.append("")
    report.append("| Suffix | Gloss | Function | Attestations |")
    report.append("|--------|-------|----------|--------------|")
    
    core_tam = [
        ('ding', 'IRR', 'Irrealis/Future'),
        ('ta', 'PFV', 'Perfective'),
        ('zo', 'COMPL', 'Completive'),
        ('kik', 'ITER', 'Iterative/Again'),
        ('nawn', 'CONT', 'Continuative'),
        ('khin', 'IMM', 'Immediate'),
        ('lai', 'PROSP', 'Prospective'),
        ('thei', 'ABIL', 'Abilitative'),
    ]
    
    for suffix, gloss, func in sorted(core_tam, key=lambda x: -counts.get(x[0], 0)):
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
    examples = find_tam_examples(verses, kjv, 'ding', 'IRR', limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        # Add interlinear gloss tier
        glossed = gloss_sentence(text)
        seg_parts = [g[1] for g in glossed]
        gloss_parts = [g[2] for g in glossed]
        report.append(f"> *{' '.join(seg_parts)}*")
        report.append(f"> {' '.join(gloss_parts)}")
        report.append(f"> KJV: *{kjv_text}*")
        report.append(f"> Target: *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -ta (Perfective)
    report.append("### -ta (Perfective)")
    report.append("")
    report.append("Marks completed actions, often with past time reference.")
    report.append("")
    examples = find_tam_examples(verses, kjv, 'ta', 'PFV', limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        glossed = gloss_sentence(text)
        seg_parts = [g[1] for g in glossed]
        gloss_parts = [g[2] for g in glossed]
        report.append(f"> *{' '.join(seg_parts)}*")
        report.append(f"> {' '.join(gloss_parts)}")
        report.append(f"> KJV: *{kjv_text}*")
        report.append(f"> Target: *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -zo (Completive)
    report.append("### -zo (Completive)")
    report.append("")
    report.append("Indicates action completed to its endpoint.")
    report.append("")
    examples = find_tam_examples(verses, kjv, 'zo', 'COMPL', limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        glossed = gloss_sentence(text)
        seg_parts = [g[1] for g in glossed]
        gloss_parts = [g[2] for g in glossed]
        report.append(f"> *{' '.join(seg_parts)}*")
        report.append(f"> {' '.join(gloss_parts)}")
        report.append(f"> KJV: *{kjv_text}*")
        report.append(f"> Target: *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -kik (Iterative)
    report.append("### -kik (Iterative/Repetitive)")
    report.append("")
    report.append("Marks repeated or returned action ('again').")
    report.append("")
    examples = find_tam_examples(verses, kjv, 'kik', 'ITER', limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        glossed = gloss_sentence(text)
        seg_parts = [g[1] for g in glossed]
        gloss_parts = [g[2] for g in glossed]
        report.append(f"> *{' '.join(seg_parts)}*")
        report.append(f"> {' '.join(gloss_parts)}")
        report.append(f"> KJV: *{kjv_text}*")
        report.append(f"> Target: *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -thei (Abilitative)
    report.append("### -thei (Abilitative)")
    report.append("")
    report.append("Marks ability or possibility to perform an action.")
    report.append("")
    examples = find_tam_examples(verses, kjv, 'thei', 'ABIL', limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        glossed = gloss_sentence(text)
        seg_parts = [g[1] for g in glossed]
        gloss_parts = [g[2] for g in glossed]
        report.append(f"> *{' '.join(seg_parts)}*")
        report.append(f"> {' '.join(gloss_parts)}")
        report.append(f"> KJV: *{kjv_text}*")
        report.append(f"> Target: *{word}*: {analysis[0]} → {analysis[1]}")
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
    report.append("2. **Modal markers**: -ding (IRR), -thei (ABIL)")
    report.append("3. **Continuative/Prospective**: -nawn (CONT), -lai (PROSP)")
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
