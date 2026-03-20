#!/usr/bin/env python3
"""
Generate Verb Stem Report for Tedim Chin

This script analyzes verb stems in the Bible corpus and generates
a comprehensive report organized by semantic domain.
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word, VERB_STEMS, TAM_SUFFIXES, VERBAL_DERIVATIONAL_SUFFIXES

# Book code to name mapping
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
    """Convert 01001001 to Genesis 1:1 format."""
    book_code = ref[:2]
    chapter = int(ref[2:5])
    verse = int(ref[5:8])
    book_name = BOOK_NAMES.get(book_code, f'Book {book_code}')
    return f"{book_name} {chapter}:{verse}"


def load_bible_text():
    """Load the Tedim Chin Bible text."""
    bible_path = os.path.join(os.path.dirname(__file__), 
                              '..', 'bibles', 'extracted', 'ctd', 'ctd-x-bible.txt')
    verses = {}
    with open(bible_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                ref, text = line.strip().split('\t', 1)
                verses[ref] = text
    return verses


def count_verb_occurrences(verses):
    """Count occurrences of each verb stem in the corpus."""
    counts = defaultdict(int)
    first_ref = {}
    
    # Sort stems by length (longest first) so longer stems match before shorter ones
    # This ensures 'nungta' matches before 'nung', 'piangsak' before 'piang', etc.
    sorted_stems = sorted(VERB_STEMS.keys(), key=len, reverse=True)
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            # Check if it starts with a verb stem (longest match first)
            for stem in sorted_stems:
                if clean == stem or clean.startswith(stem):
                    counts[stem] += 1
                    if stem not in first_ref:
                        first_ref[stem] = ref
                    break
    
    return counts, first_ref


# Semantic domains for verb classification
SEMANTIC_DOMAINS = {
    'existence': ['om', 'hi', 'ahi', 'ahih', 'suak', 'teng', 'dam', 'hoih', 'sih', 'nung', 'piang', 'nuntak', 'nungta'],
    'motion': ['pai', 'va', 'lut', 'khia', 'tung', 'zui', 'ciah', 'ciahpai', 'liahpai', 'zuan', 'ciahkik', 'hong', 'vak', 'leen', 'let', 'puakkik'],
    'perception': ['mu', 'muh', 'za', 'zak', 'ngai', 'ngaih', 'en'],
    'cognition': ['thei', 'theih', 'um', 'ngaihsun', 'ngaihsut', 'lung', 'deih', 'nuam', 'duh', 'muan'],
    'speech': ['ci', 'cih', 'gen', 'hilh', 'thugen', 'sam', 'sampah', 'kiko', 'pau', 'dei'],
    'transfer': ['pia', 'piak', 'lak', 'nei', 'neih', 'koih', 'sawl', 'ngah'],
    'creation': ['bawl', 'piangsak', 'limbawl'],
    'destruction': ['that', 'tat', 'sat', 'susia'],
    'physical': ['ne', 'nek', 'tut', 'ding', 'to', 'ton', 'kap', 'lup', 'phum', 'gelh'],
    'social': ['sem', 'sep', 'uk', 'zol', 'it', 'zahtak', 'hehpih'],
    'emotion': ['lungdam', 'zah', 'huai', 'hite'],
    'reflexive': ['kipat', 'kipan', 'kizom', 'kisai', 'kisik', 'kikhia', 'kibawl', 'kibang', 'kikhel', 'kituah', 'kikhen', 'kilem'],
    'causative': ['sak', 'paisak', 'damsak', 'paipih', 'honkhia', 'tungsak', 'paikhiat', 'siansak', 'hisak'],
}


def classify_verb(stem):
    """Classify a verb stem by semantic domain."""
    for domain, verbs in SEMANTIC_DOMAINS.items():
        if stem in verbs:
            return domain
    # Check for ki- prefix (reflexive/middle)
    if stem.startswith('ki'):
        return 'reflexive'
    # Check for -sak suffix (causative)
    if stem.endswith('sak'):
        return 'causative'
    return 'other'


def generate_report():
    """Generate the verb stems report."""
    print("Loading corpus...")
    verses = load_bible_text()
    
    print("Counting verb occurrences...")
    counts, first_refs = count_verb_occurrences(verses)
    
    report = []
    report.append("# Tedim Chin Verb Stems")
    report.append("")
    report.append("This report documents verb stems in Tedim Chin, organized by semantic domain.")
    report.append(f"Total verb stems in lexicon: **{len(VERB_STEMS)}**")
    report.append("")
    
    # Overview
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin verbs are characterized by:")
    report.append("")
    report.append("1. **Stem alternation** (Form I / Form II)")
    report.append("   - Form I: Indicative, used in conclusive sentences")
    report.append("   - Form II: Subjunctive, used in subordinate/inconclusive clauses")
    report.append("   - Changes: add -h/-k, tone change, -ng → -n")
    report.append("")
    report.append("2. **Pronominal prefixes** for subject agreement")
    report.append("   - ka- (1SG), na- (2SG), a- (3SG), i- (1PL.INCL)")
    report.append("")
    report.append("3. **TAM suffixes** for tense-aspect-mood")
    report.append("   - -ding (IRR), -ta (PFV), -zo (COMPL), -kik (ITER)")
    report.append("")
    report.append("4. **Derivational morphology**")
    report.append("   - ki- (reflexive/middle), -sak (causative), -pih (applicative)")
    report.append("")
    
    # Form I / Form II pairs
    report.append("---")
    report.append("")
    report.append("## Form I / Form II Alternation")
    report.append("")
    report.append("Many verbs have two stems that alternate based on clause type:")
    report.append("")
    report.append("| Form I | Form II | Gloss | Pattern |")
    report.append("|--------|---------|-------|---------|")
    
    form_pairs = [
        ('mu', 'muh', 'see', 'add -h'),
        ('za', 'zak', 'hear', 'add -k'),
        ('ngai', 'ngaih', 'listen', 'add -h'),
        ('thei', 'theih', 'know', 'add -h'),
        ('ne', 'nek', 'eat', 'add -k'),
        ('nei', 'neih', 'have', 'add -h'),
        ('nusia', 'nusiat', 'abandon', 'add -t'),
        ('honkhia', 'honkhiat', 'bring.out', 'add -t'),
    ]
    
    for f1, f2, gloss, pattern in form_pairs:
        report.append(f"| {f1} | {f2} | {gloss} | {pattern} |")
    report.append("")
    
    # Semantic domains
    report.append("---")
    report.append("")
    report.append("## Verb Stems by Semantic Domain")
    report.append("")
    
    domain_names = {
        'existence': 'Existence and State',
        'motion': 'Motion',
        'perception': 'Perception',
        'cognition': 'Cognition',
        'speech': 'Speech',
        'transfer': 'Transfer and Possession',
        'creation': 'Creation and Making',
        'destruction': 'Destruction',
        'physical': 'Physical Actions',
        'social': 'Social Actions',
        'emotion': 'Emotion',
        'reflexive': 'Reflexive/Middle (ki-)',
        'causative': 'Causative (-sak)',
    }
    
    for domain, domain_title in domain_names.items():
        if domain not in SEMANTIC_DOMAINS:
            continue
            
        report.append(f"### {domain_title}")
        report.append("")
        report.append("| Stem | Gloss | Attestations | First Citation |")
        report.append("|------|-------|--------------|----------------|")
        
        domain_verbs = SEMANTIC_DOMAINS[domain]
        # Sort by frequency
        sorted_verbs = sorted(domain_verbs, key=lambda v: -counts.get(v, 0))
        
        for stem in sorted_verbs:
            if stem in VERB_STEMS:
                gloss = VERB_STEMS[stem]
                count = counts.get(stem, 0)
                ref = first_refs.get(stem, '')
                citation = format_reference(ref) if ref else '—'
                report.append(f"| {stem} | {gloss} | {count}x | {citation} |")
        
        report.append("")
    
    # High-frequency verbs (top 50)
    report.append("---")
    report.append("")
    report.append("## High-Frequency Verbs (Top 50)")
    report.append("")
    report.append("| Rank | Stem | Gloss | Count | First Citation |")
    report.append("|------|------|-------|-------|----------------|")
    
    sorted_by_freq = sorted(counts.items(), key=lambda x: -x[1])
    for rank, (stem, count) in enumerate(sorted_by_freq[:50], 1):
        if stem in VERB_STEMS:
            gloss = VERB_STEMS[stem]
            ref = first_refs.get(stem, '')
            citation = format_reference(ref) if ref else '—'
            report.append(f"| {rank} | {stem} | {gloss} | {count}x | {citation} |")
    
    report.append("")
    
    # Full alphabetical list
    report.append("---")
    report.append("")
    report.append("## Complete Verb Stem List (Alphabetical)")
    report.append("")
    report.append("| Stem | Gloss | Domain | Attestations |")
    report.append("|------|-------|--------|--------------|")
    
    for stem in sorted(VERB_STEMS.keys()):
        gloss = VERB_STEMS[stem]
        domain = classify_verb(stem)
        count = counts.get(stem, 0)
        report.append(f"| {stem} | {gloss} | {domain} | {count}x |")
    
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', '5-verb-01-stems.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")
