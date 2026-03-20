#!/usr/bin/env python3
"""
Generate Noun Phrase Structure Report for Tedim Chin

This script analyzes NP patterns in the Bible corpus and generates
a comprehensive report with attested examples and interlinear glosses.
"""

import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, DEMONSTRATIVES, NUMERALS, QUANTIFIERS, 
    PROPERTY_WORDS, COORDINATOR, RELATOR_NOUNS, CASE_MARKERS
)


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


def load_kjv_glosses():
    """Load KJV translations for verse references."""
    kjv_path = os.path.join(os.path.dirname(__file__), 
                            '..', 'data', 'verses_aligned.tsv')
    kjv = {}
    if os.path.exists(kjv_path):
        with open(kjv_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    kjv[parts[0]] = parts[2]
    return kjv


def gloss_phrase(phrase):
    """Generate interlinear gloss for a phrase."""
    words = phrase.split()
    tedim_line = []
    seg_line = []
    gloss_line = []
    
    for word in words:
        clean_word = word.rstrip('.,;:!?"\'')
        seg, gloss = analyze_word(clean_word)
        tedim_line.append(clean_word)
        seg_line.append(seg)
        gloss_line.append(gloss)
    
    return {
        'tedim': ' '.join(tedim_line),
        'segmentation': ' '.join(seg_line),
        'gloss': ' '.join(gloss_line),
    }


def find_examples(verses, pattern, limit=3):
    """Find verses containing a pattern and return with context."""
    examples = []
    for ref, text in verses.items():
        if pattern in text:
            # Find the pattern in context
            idx = text.find(pattern)
            # Get surrounding context (up to 50 chars each side)
            start = max(0, idx - 50)
            end = min(len(text), idx + len(pattern) + 50)
            context = text[start:end]
            if start > 0:
                context = '...' + context
            if end < len(text):
                context = context + '...'
            
            examples.append({
                'ref': ref,
                'context': context,
                'full_verse': text,
            })
            if len(examples) >= limit:
                break
    return examples


def count_pattern(text, pattern):
    """Count occurrences of a pattern in text."""
    return text.count(pattern)


def generate_report():
    """Generate the NP structure report."""
    print("Loading corpus...")
    verses = load_bible_text()
    kjv = load_kjv_glosses()
    full_text = '\n'.join(verses.values())
    
    report = []
    report.append("# Tedim Chin Noun Phrase Structure")
    report.append("")
    report.append("This report documents the structural patterns of noun phrases (NPs) in Tedim Chin,")
    report.append("based on analysis of the Bible corpus.")
    report.append("")
    report.append("## Overview")
    report.append("")
    report.append("Tedim Chin noun phrase structure follows a general template:")
    report.append("")
    report.append("```")
    report.append("(POSS-GEN) (DEM) HEAD (PROP) (NUM) (QUANT) (-PL) (CASE)")
    report.append("```")
    report.append("")
    report.append("Key characteristics:")
    report.append("- **Head-initial for modifiers**: Adjectives, numerals, and quantifiers FOLLOW the head noun")
    report.append("- **Demonstratives are prenominal**: Demonstratives PRECEDE the head noun")
    report.append("- **No numeral classifiers**: Nouns directly precede numerals")
    report.append("- **Plural -te**: Attaches to head noun or quantifier")
    report.append("- **Case markers close the NP**: ERG, LOC, COM, ABL, etc.")
    report.append("")
    
    # Section 1: Demonstratives
    report.append("---")
    report.append("")
    report.append("## 1. Demonstrative + Noun")
    report.append("")
    report.append("Demonstratives precede the noun (prenominal position).")
    report.append("")
    report.append("### Demonstrative Inventory")
    report.append("")
    report.append("| Form | Gloss | Translation |")
    report.append("|------|-------|-------------|")
    for form, gloss in DEMONSTRATIVES.items():
        report.append(f"| {form} | {gloss} | {'this' if 'PROX' in gloss else 'that'}{'/these' if '.PL' in gloss else ''} |")
    report.append("")
    
    dem_patterns = [
        ('hih mi', 'this person'),
        ('hih mite', 'these people'),
        ('hih thu', 'this word'),
        ('hih gam', 'this land'),
        ('tua mi', 'that person'),
        ('tua gam', 'that land'),
        ('tua nu', 'that woman'),
        ('tua lai', 'that place'),
    ]
    
    report.append("### DEM + N Patterns")
    report.append("")
    report.append("| Pattern | Count | Gloss | Translation |")
    report.append("|---------|-------|-------|-------------|")
    for pat, trans in dem_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            glossed = gloss_phrase(pat)
            report.append(f"| {pat} | {count}x | {glossed['gloss']} | '{trans}' |")
    report.append("")
    
    # Example with full context
    report.append("### Examples")
    report.append("")
    examples = find_examples(verses, 'hih mite', limit=2)
    for ex in examples:
        report.append(f"**{ex['ref']}**")
        report.append("```")
        glossed = gloss_phrase(ex['context'].replace('...', '').strip())
        report.append(f"Tedim:  {glossed['tedim']}")
        report.append(f"Gloss:  {glossed['gloss']}")
        if ex['ref'] in kjv:
            report.append(f"KJV:    {kjv[ex['ref']][:100]}...")
        report.append("```")
        report.append("")
    
    # Section 2: Noun + Numeral
    report.append("---")
    report.append("")
    report.append("## 2. Noun + Numeral")
    report.append("")
    report.append("Numerals follow the noun directly. There are **no numeral classifiers** in Tedim Chin.")
    report.append("")
    report.append("### Numeral Inventory")
    report.append("")
    report.append("| Form | Gloss |")
    report.append("|------|-------|")
    for form, gloss in list(NUMERALS.items())[:12]:
        report.append(f"| {form} | {gloss} |")
    report.append("")
    
    num_patterns = [
        ('mi khat', 'one person'),
        ('mi nih', 'two people'),
        ('mi thum', 'three people'),
        ('ni khat', 'one day'),
        ('ni sagih', 'seven days'),
        ('kum khat', 'one year'),
        ('kum za', 'hundred years'),
        ('tapa khat', 'one son'),
    ]
    
    report.append("### N + NUM Patterns")
    report.append("")
    report.append("| Pattern | Count | Gloss | Translation |")
    report.append("|---------|-------|-------|-------------|")
    for pat, trans in num_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            glossed = gloss_phrase(pat)
            report.append(f"| {pat} | {count}x | {glossed['gloss']} | '{trans}' |")
    report.append("")
    
    # Examples
    report.append("### Examples")
    report.append("")
    examples = find_examples(verses, 'mi khat', limit=2)
    for ex in examples:
        report.append(f"**{ex['ref']}**")
        report.append("```")
        glossed = gloss_phrase(ex['context'].replace('...', '').strip())
        report.append(f"Tedim:  {glossed['tedim']}")
        report.append(f"Gloss:  {glossed['gloss']}")
        if ex['ref'] in kjv:
            report.append(f"KJV:    {kjv[ex['ref']][:100]}...")
        report.append("```")
        report.append("")
    
    # Section 3: Noun + Quantifier
    report.append("---")
    report.append("")
    report.append("## 3. Noun + Quantifier")
    report.append("")
    report.append("Quantifiers follow the noun phrase.")
    report.append("")
    report.append("### Quantifier Inventory")
    report.append("")
    report.append("| Form | Gloss | Translation |")
    report.append("|------|-------|-------------|")
    for form, gloss in QUANTIFIERS.items():
        report.append(f"| {form} | {gloss} | {gloss} |")
    report.append("")
    
    quant_patterns = [
        ('mi khempeuh', 'all people'),
        ('mite khempeuh', 'all the people'),
        ('thu khempeuh', 'all words'),
        ('mi tampi', 'many people'),
        ('mi khatpeuh', 'anyone'),
        ('mi peuhpeuh', 'everyone'),
    ]
    
    report.append("### N + QUANT Patterns")
    report.append("")
    report.append("| Pattern | Count | Gloss | Translation |")
    report.append("|---------|-------|-------|-------------|")
    for pat, trans in quant_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            glossed = gloss_phrase(pat)
            report.append(f"| {pat} | {count}x | {glossed['gloss']} | '{trans}' |")
    report.append("")
    
    # Section 4: Noun + Property Word
    report.append("---")
    report.append("")
    report.append("## 4. Noun + Property Word (Attributive Adjective)")
    report.append("")
    report.append("Property words (stative verbs) follow the noun in attributive position.")
    report.append("Compare predicative use: `a hoih` '3SG good' = 'it is good'")
    report.append("")
    report.append("### Property Word Sample")
    report.append("")
    report.append("| Form | Gloss |")
    report.append("|------|-------|")
    sample_props = list(PROPERTY_WORDS.items())[:10]
    for form, gloss in sample_props:
        report.append(f"| {form} | {gloss} |")
    report.append("")
    
    prop_patterns = [
        ('mi hoih', 'good person'),
        ('mi sia', 'evil person'),
        ('mi siangtho', 'holy person'),
        ('thu hoih', 'good word'),
        ('gam hoih', 'good land'),
        ('inn lian', 'big house'),
    ]
    
    report.append("### N + PROP Patterns")
    report.append("")
    report.append("| Pattern | Count | Gloss | Translation |")
    report.append("|---------|-------|-------|-------------|")
    for pat, trans in prop_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            glossed = gloss_phrase(pat)
            report.append(f"| {pat} | {count}x | {glossed['gloss']} | '{trans}' |")
    report.append("")
    
    # Section 5: Complex NPs
    report.append("---")
    report.append("")
    report.append("## 5. Complex Noun Phrases")
    report.append("")
    report.append("Longer NPs combine multiple modifiers following the template.")
    report.append("")
    
    complex_patterns = [
        ('hih mite khempeuh', 'DEM + N.PL + QUANT', 'all these people'),
        ('mi khempeuh tungah', 'N + QUANT + REL-LOC', 'on all people'),
        ('mi khempeuh in', 'N + QUANT + CASE', 'all people (ERG)'),
        ('mite khempeuh in', 'N.PL + QUANT + CASE', 'all the people (ERG)'),
        ('mi khat in', 'N + NUM + CASE', 'one person (ERG)'),
    ]
    
    report.append("### Complex Pattern Examples")
    report.append("")
    report.append("| Pattern | Structure | Count | Translation |")
    report.append("|---------|-----------|-------|-------------|")
    for pat, struct, trans in complex_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            report.append(f"| {pat} | {struct} | {count}x | '{trans}' |")
    report.append("")
    
    # Section 6: Coordination
    report.append("---")
    report.append("")
    report.append("## 6. Noun Coordination")
    report.append("")
    report.append("Nouns are coordinated with `le` 'and'.")
    report.append("")
    
    # Use explicit glosses for coordination (polysemy issues)
    coord_patterns = [
        ('numei le pasal', 'woman and husband', 'woman and man'),
        ('ngun le kham', 'silver and gold', 'silver and gold'),
        ('sun le zan', 'day and night', 'day and night'),  
        ('van le lei', 'sky and earth', 'heaven and earth'),
        ('nu le pa', 'mother and father', 'mother and father'),
        ('pute le pate', 'grandmother.PL and grandfather.PL', 'ancestors'),
    ]
    
    report.append("### N le N (N and N)")
    report.append("")
    report.append("| Pattern | Count | Gloss | Translation |")
    report.append("|---------|-------|-------|-------------|")
    for pat, gloss, trans in coord_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            report.append(f"| {pat} | {count}x | {gloss} | '{trans}' |")
    report.append("")
    
    # Section 7: Possessive constructions
    report.append("---")
    report.append("")
    report.append("## 7. Possessive Constructions")
    report.append("")
    report.append("Possessors precede the head noun and are marked with genitive `'` (apostrophe).")
    report.append("")
    
    poss_patterns = [
        ("mite' tungah", 'on the people'),
        ("kei' tungah", 'on me'),
        ("note' tungah", 'on you (PL)'),
        ("amau' gam", 'their land'),
    ]
    
    report.append("### POSS-GEN + N Patterns")
    report.append("")
    report.append("| Pattern | Count | Translation |")
    report.append("|---------|-------|-------------|")
    for pat, trans in poss_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            report.append(f"| {pat} | {count}x | '{trans}' |")
    report.append("")
    
    # Section 8: NP + Case
    report.append("---")
    report.append("")
    report.append("## 8. NP + Case Marking")
    report.append("")
    report.append("Case markers close the NP. See the Postpositions report for full details.")
    report.append("")
    report.append("### Common NP + CASE patterns")
    report.append("")
    
    case_patterns = [
        ('mite in', 'N.PL + ERG', 'the people (ERG)'),
        ('mite ah', 'N.PL + LOC', 'among the people'),
        ('mite tawh', 'N.PL + COM', 'with the people'),
        ('mite kiangah', 'N.PL + REL-LOC', 'beside the people'),
        ('mite tungah', 'N.PL + REL-LOC', 'on the people'),
        ('mite lakah', 'N.PL + REL-LOC', 'among the people'),
    ]
    
    report.append("| Pattern | Structure | Count | Translation |")
    report.append("|---------|-----------|-------|-------------|")
    for pat, struct, trans in case_patterns:
        count = count_pattern(full_text, pat)
        if count > 0:
            report.append(f"| {pat} | {struct} | {count}x | '{trans}' |")
    report.append("")
    
    # Summary section
    report.append("---")
    report.append("")
    report.append("## Summary: NP Structure Template")
    report.append("")
    report.append("```")
    report.append("Full NP template:")
    report.append("")
    report.append("(POSS-GEN) (DEM) HEAD-N (-PL) (PROP) (NUM) (QUANT) (CASE)")
    report.append("")
    report.append("Examples filling different slots:")
    report.append("")
    report.append("                          mi                                  = person")
    report.append("                          mi-te                               = people")
    report.append("              hih         mi-te                               = these people")
    report.append("              hih         mi-te          khempeuh             = all these people")
    report.append("              hih         mi-te          khempeuh      in     = all these people (ERG)")
    report.append("mite'                     tung                          -ah   = on the people")
    report.append("              tua         pa                    khat          = that one man")
    report.append("```")
    report.append("")
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    # Write to file
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'np_structure.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")
