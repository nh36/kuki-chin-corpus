#!/usr/bin/env python3
"""
Generate Nominalization Report for Tedim Chin

Documents deverbal nominalization patterns: -na (action), -pa (agent), etc.
"""

import sys
import os
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word

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


def find_suffix_examples(verses, suffix, limit=3):
    """Find examples with a nominalizing suffix."""
    examples = []
    books_used = set()
    
    for ref, text in sorted(verses.items()):
        if len(ref) != 8 or not ref.isdigit():
            continue
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # Check for suffix at word end
            if clean.endswith(suffix) or clean.endswith(suffix + 'te'):
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


def count_nominalizers(verses):
    """Count nominalizer occurrences."""
    counts = Counter()
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # -na (action nominal)
            if clean.endswith('na') or 'na-' in clean:
                counts['na'] += 1
            # -pa (agent)
            if clean.endswith('pa') or clean.endswith('pate'):
                counts['pa'] += 1
            # -nu (female agent)
            if clean.endswith('nu') or clean.endswith('nute'):
                counts['nu'] += 1
            # mi- (person/agent)
            if clean.startswith('mi'):
                counts['mi'] += 1
    
    return counts


def generate_report():
    """Generate nominalization report."""
    print("Loading corpus...")
    verses = load_bible()
    
    print("Analyzing nominalization patterns...")
    counts = count_nominalizers(verses)
    
    report = []
    report.append("# Tedim Chin Nominalization")
    report.append("")
    report.append("This report documents deverbal nominalization patterns in Tedim Chin.")
    report.append("")
    
    # Overview
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin has several strategies for deriving nouns from verbs:")
    report.append("")
    report.append("| Morpheme | Type | Gloss | Function | Attestations |")
    report.append("|----------|------|-------|----------|--------------|")
    report.append(f"| -na | Suffix | NMLZ | Action/Result nominal | {counts['na']}x |")
    report.append(f"| -pa | Suffix | AGT.M | Male agent | {counts['pa']}x |")
    report.append(f"| -nu | Suffix | AGT.F | Female agent | {counts['nu']}x |")
    report.append(f"| mi- | Prefix | person | Person who... | {counts['mi']}x |")
    report.append("")
    
    # -na (Action/Result Nominal)
    report.append("---")
    report.append("")
    report.append("## -na (Action/Result Nominal)")
    report.append("")
    report.append("The suffix -na derives action nouns and result nouns from verbs.")
    report.append("It attaches to the verb stem (typically Form II).")
    report.append("")
    report.append("### Pattern")
    report.append("```")
    report.append("VERB-na → 'the act of VERBing' / 'thing VERBed'")
    report.append("```")
    report.append("")
    report.append("### Examples")
    report.append("")
    report.append("| -na Form | Base Verb | Meaning |")
    report.append("|----------|-----------|---------|")
    report.append("| paina | pai (go) | going, journey |")
    report.append("| tenna | ten (dwell) | dwelling, residence |")
    report.append("| neihna | neih (have) | having, possession |")
    report.append("| bawlna | bawl (make) | making, creation |")
    report.append("| genkholhna | genkholh (promise) | promising, promise |")
    report.append("| ciamna | ciam (swear) | oath, sworn thing |")
    report.append("| thupiakna | thupiakna | commandment |")
    report.append("| nuntakna | nuntak (live) | living, life |")
    report.append("")
    
    report.append("### Corpus Examples")
    report.append("")
    examples = find_suffix_examples(verses, 'na', limit=5)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -pa (Male Agent)
    report.append("---")
    report.append("")
    report.append("## -pa (Male Agent)")
    report.append("")
    report.append("The suffix -pa derives agent nouns referring to males.")
    report.append("")
    report.append("### Pattern")
    report.append("```")
    report.append("VERB-pa → 'one who VERBs (male)'")
    report.append("```")
    report.append("")
    report.append("### Examples")
    report.append("")
    report.append("| -pa Form | Base | Meaning |")
    report.append("|----------|------|---------|")
    report.append("| bawlpa | bawl (make) | maker (male) |")
    report.append("| ukpa | uk (rule) | ruler (male) |")
    report.append("| genpa | gen (say) | speaker (male) |")
    report.append("| ngenpa | ngen (beg) | beggar (male) |")
    report.append("| kilpa | kil (watch) | watchman |")
    report.append("| neihpa | neih (have) | owner (male) |")
    report.append("")
    
    report.append("### Corpus Examples")
    report.append("")
    examples = find_suffix_examples(verses, 'pa', limit=5)
    for ref, text, word, analysis in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append(f"> *{word}*: {analysis[0]} → {analysis[1]}")
        report.append("")
    
    # -nu (Female Agent)
    report.append("---")
    report.append("")
    report.append("## -nu (Female Agent)")
    report.append("")
    report.append("The suffix -nu derives agent nouns referring to females.")
    report.append("")
    report.append("### Examples")
    report.append("")
    report.append("| -nu Form | Base | Meaning |")
    report.append("|----------|------|---------|")
    report.append("| bawlnu | bawl (make) | maker (female) |")
    report.append("| neihnu | neih (have) | owner (female) |")
    report.append("| zinna | zin (travel) | traveler (female) |")
    report.append("")
    
    # mi- (Person Prefix)
    report.append("---")
    report.append("")
    report.append("## mi- (Person Prefix)")
    report.append("")
    report.append("The prefix mi- (or noun *mi* 'person') can form agent-like compounds.")
    report.append("")
    report.append("### Examples")
    report.append("")
    report.append("| Form | Meaning |")
    report.append("|------|---------|")
    report.append("| mihing | human being |")
    report.append("| mipa | man |")
    report.append("| minu | woman |")
    report.append("| misim | wise person |")
    report.append("| milian | important person |")
    report.append("")
    
    # Nominalized Relative Clauses
    report.append("---")
    report.append("")
    report.append("## Nominalized Relative Clauses")
    report.append("")
    report.append("Tedim Chin uses nominalization to form relative clauses.")
    report.append("The relativized NP is typically marked as the head, with the")
    report.append("verb in Form II + -na or -pa/-nu.")
    report.append("")
    report.append("### Pattern")
    report.append("```")
    report.append("[CLAUSE + VERB-na] N")
    report.append("'the N that was VERBed'")
    report.append("```")
    report.append("")
    report.append("### Example Patterns")
    report.append("")
    report.append("- *Pathian in bawlna thil* 'thing that God made'")
    report.append("- *Jesus' genpa thu* 'word that Jesus spoke'")
    report.append("- *hih genmi thu* 'this spoken word'")
    report.append("")
    
    # Summary
    report.append("---")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append("Tedim Chin nominalization strategies:")
    report.append("")
    report.append("1. **-na** creates action/result nouns from verbs")
    report.append("2. **-pa/-nu** creates gendered agent nouns")
    report.append("3. **mi-** (person) forms generic person compounds")
    report.append("4. **Nominalized clauses** function as relative clauses")
    report.append("")
    report.append("The -na suffix is extremely productive and is the primary")
    report.append("strategy for creating abstract nouns from verbal concepts.")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'nominalization.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
