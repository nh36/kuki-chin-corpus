#!/usr/bin/env python3
"""
Generate Valency and Voice Report for Tedim Chin

Documents ki- reflexive/middle, -sak causative, -pih applicative,
and other valency-changing morphology.
"""

import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word, VERBAL_DERIVATIONAL_SUFFIXES

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


def find_pattern_examples(verses, pattern, limit=3):
    """Find examples matching a pattern."""
    examples = []
    books_used = set()
    
    for ref, text in sorted(verses.items()):
        if len(ref) != 8 or not ref.isdigit():
            continue
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if pattern in clean:
                book_code = ref[:2]
                if book_code in books_used:
                    continue
                
                analysis = analyze_word(clean)
                if analysis[1]:
                    examples.append((ref, text, word, analysis))
                    books_used.add(book_code)
                    
                    if len(examples) >= limit:
                        return examples
    
    return examples


def count_patterns(verses):
    """Count derivational pattern occurrences."""
    ki_count = 0
    sak_count = 0
    pih_count = 0
    khawm_count = 0
    gawp_count = 0
    thei_count = 0
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if clean.startswith('ki'):
                ki_count += 1
            if 'sak' in clean:
                sak_count += 1
            if 'pih' in clean:
                pih_count += 1
            if 'khawm' in clean:
                khawm_count += 1
            if 'gawp' in clean:
                gawp_count += 1
            if 'thei' in clean:
                thei_count += 1
    
    return {
        'ki': ki_count,
        'sak': sak_count,
        'pih': pih_count,
        'khawm': khawm_count,
        'gawp': gawp_count,
        'thei': thei_count,
    }


def generate_report():
    """Generate valency/voice report."""
    print("Loading corpus...")
    verses = load_bible()
    
    print("Analyzing valency patterns...")
    counts = count_patterns(verses)
    
    report = []
    report.append("# Tedim Chin Valency and Voice")
    report.append("")
    report.append("This report documents valency-changing and voice morphology.")
    report.append("")
    
    # Overview
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin has productive derivational morphology for changing verb valency:")
    report.append("")
    report.append("| Morpheme | Function | Gloss | Attestations |")
    report.append("|----------|----------|-------|--------------|")
    report.append(f"| ki- | Reflexive/Middle/Passive | REFL | {counts['ki']}x |")
    report.append(f"| -sak | Causative | CAUS | {counts['sak']}x |")
    report.append(f"| -pih | Applicative | APPL | {counts['pih']}x |")
    report.append(f"| -khawm | Comitative | COM | {counts['khawm']}x |")
    report.append(f"| -gawp | Intensive | INTENS | {counts['gawp']}x |")
    report.append(f"| -thei | Abilitative | ABIL | {counts['thei']}x |")
    report.append("")
    
    # ki- (Reflexive/Middle/Passive)
    report.append("---")
    report.append("")
    report.append("## ki- (Reflexive/Middle/Passive)")
    report.append("")
    report.append("The prefix ki- has multiple related functions:")
    report.append("")
    report.append("### Reflexive")
    report.append("Subject acts on self: *kibawl* 'make oneself'")
    report.append("")
    report.append("### Reciprocal")
    report.append("Plural subjects act on each other: *kiten* 'hit each other'")
    report.append("")
    report.append("### Middle")
    report.append("Subject is affected by action: *kilak* 'be taken' (from *lak* 'take')")
    report.append("")
    report.append("### Passive-like")
    report.append("Agent defocused: *kigen* 'be said, it is said'")
    report.append("")
    
    # ki- examples
    report.append("### Examples")
    report.append("")
    examples = find_pattern_examples(verses, 'ki', limit=5)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # Common ki- verbs
    report.append("### Common ki- Forms")
    report.append("")
    report.append("| Form | Base | Meaning |")
    report.append("|------|------|---------|")
    report.append("| kipat | pat (begin) | begin from |")
    report.append("| kipan | pan (from) | originate from |")
    report.append("| kigen | gen (say) | be said |")
    report.append("| kibawl | bawl (make) | be made |")
    report.append("| kilak | lak (take) | be taken |")
    report.append("| kisik | sik (pour) | be poured |")
    report.append("| kizom | zom (follow) | follow after |")
    report.append("| kikhel | khel (change) | be changed |")
    report.append("| kikhen | khen (separate) | be separated |")
    report.append("| kilem | lem (keep) | be kept |")
    report.append("")
    
    # -sak (Causative)
    report.append("---")
    report.append("")
    report.append("## -sak (Causative)")
    report.append("")
    report.append("The suffix -sak adds a causer argument, making intransitives transitive")
    report.append("and transitives ditransitive.")
    report.append("")
    report.append("### Pattern")
    report.append("```")
    report.append("CAUSER + CAUSEE + VERB-sak")
    report.append("```")
    report.append("")
    
    # -sak examples
    report.append("### Examples")
    report.append("")
    examples = find_pattern_examples(verses, 'sak', limit=5)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # Common -sak verbs
    report.append("### Common -sak Forms")
    report.append("")
    report.append("| Form | Base | Meaning |")
    report.append("|------|------|---------|")
    report.append("| damsak | dam (be.well) | heal, make well |")
    report.append("| paisak | pai (go) | send |")
    report.append("| tungsak | tung (arrive) | bring to |")
    report.append("| siansak | sian (holy) | sanctify |")
    report.append("| hisak | hi (be) | make known |")
    report.append("| nungsak | nung (live) | revive |")
    report.append("")
    
    # -pih (Applicative)
    report.append("---")
    report.append("")
    report.append("## -pih (Applicative)")
    report.append("")
    report.append("The suffix -pih adds a benefactive or comitative argument.")
    report.append("")
    report.append("### Examples")
    report.append("")
    examples = find_pattern_examples(verses, 'pih', limit=5)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # Other derivational suffixes
    report.append("---")
    report.append("")
    report.append("## Other Derivational Suffixes")
    report.append("")
    report.append("### -khawm (Comitative)")
    report.append("Action done together: *omkhawm* 'be together' (from *om* 'be')")
    report.append("")
    report.append("### -gawp (Intensive)")
    report.append("Intensified action: *maitamgawp* 'burn intensely'")
    report.append("")
    report.append("### -thei (Abilitative)")
    report.append("Ability to perform action: *bawlthei* 'able to make'")
    report.append("")
    
    # Summary
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append("Tedim Chin valency-changing morphology:")
    report.append("")
    report.append("1. **ki-** reduces valency (reflexive, middle, passive)")
    report.append("2. **-sak** increases valency (causative)")
    report.append("3. **-pih** adds benefactive/comitative argument (applicative)")
    report.append("4. **-khawm** adds comitative meaning")
    report.append("5. **-thei** adds modal meaning (ability)")
    report.append("")
    report.append("The prefix ki- is highly productive and combines with many verbs.")
    report.append("The causative -sak can combine with already derived forms.")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'valency_voice.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
