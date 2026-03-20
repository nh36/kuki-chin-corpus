#!/usr/bin/env python3
"""
Generate Clause Structure Report for Tedim Chin

This script analyzes clause structure patterns in the corpus and generates
a report documenting subordination, clause chaining, and verb form distribution.
"""

import sys
import os
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, gloss_sentence,
    detect_clause_boundaries, classify_clause, analyze_clause_structure,
    CLAUSE_BOUNDARY_MARKERS, SUBORDINATORS
)

# Book names for citations
BOOK_NAMES = {
    '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus', '04': 'Numbers',
    '05': 'Deuteronomy', '06': 'Joshua', '07': 'Judges', '08': 'Ruth',
    '09': '1 Samuel', '10': '2 Samuel', '11': '1 Kings', '12': '2 Kings',
    '19': 'Psalms', '20': 'Proverbs', '23': 'Isaiah',
    '40': 'Matthew', '41': 'Mark', '42': 'Luke', '43': 'John',
    '44': 'Acts', '45': 'Romans', '46': '1 Corinthians', 
    '58': 'Hebrews', '66': 'Revelation'
}


def format_ref(ref):
    """Convert verse reference to human-readable format."""
    if len(ref) < 8 or not ref[:2].isdigit():
        return ref  # Return as-is if malformed
    try:
        book_code = ref[:2]
        chapter = int(ref[2:5])
        verse = int(ref[5:8])
        book_name = BOOK_NAMES.get(book_code, f"Book{book_code}")
        return f"{book_name} {chapter}:{verse}"
    except (ValueError, IndexError):
        return ref


def load_corpus():
    """Load Bible corpus."""
    verses = {}
    corpus_path = Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt'
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                ref, text = line.strip().split('\t', 1)
                verses[ref] = text
    return verses


def load_kjv():
    """Load KJV translations."""
    kjv = {}
    kjv_path = Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv'
    try:
        with open(kjv_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    kjv[parts[0]] = parts[2]
    except FileNotFoundError:
        pass
    return kjv


def format_example(ref, text, kjv, max_words=15):
    """Format an example with interlinear gloss."""
    words = text.split()[:max_words]
    truncated = ' '.join(words)
    if len(text.split()) > max_words:
        truncated += '...'
    
    result = gloss_sentence(truncated.rstrip('.'))
    seg_line = ' '.join(t[1] for t in result)
    gloss_line = ' '.join(t[2] for t in result)
    
    lines = []
    lines.append(f"> {truncated}")
    lines.append(f"> *{seg_line}*")
    lines.append(f"> {gloss_line}")
    if ref in kjv:
        kjv_text = kjv[ref][:100]
        if len(kjv.get(ref, '')) > 100:
            kjv_text += '...'
        lines.append(f"> KJV: *{kjv_text}*")
    
    return '\n'.join(lines)


def generate_report():
    """Generate the clause structure report."""
    print("Loading corpus...")
    verses = load_corpus()
    kjv = load_kjv()
    
    lines = []
    
    # Header
    lines.append("# Tedim Chin Clause Structure")
    lines.append("")
    lines.append("This report documents clause structure patterns in the Tedim Chin Bible,")
    lines.append("including subordination types, clause chaining, and verb form distribution.")
    lines.append("")
    
    # Analyze clause patterns
    print("Analyzing clause structure patterns...")
    
    # Stats
    clause_type_counts = Counter()
    chain_type_counts = Counter()
    marker_counts = Counter()
    subordinator_examples = defaultdict(list)
    chain_examples = defaultdict(list)
    
    total_verses = 0
    total_clauses = 0
    
    for ref, text in verses.items():
        result = analyze_clause_structure(text)
        total_verses += 1
        total_clauses += result['clause_count']
        
        # Count clause types
        for clause in result['clauses']:
            clause_type_counts[clause['type']] += 1
            if clause.get('boundary_marker'):
                marker_counts[clause['boundary_marker']] += 1
                
                # Store examples
                marker = clause['boundary_marker']
                if len(subordinator_examples[marker]) < 10:
                    subordinator_examples[marker].append((ref, text))
        
        # Count chain types
        chain_type_counts[result['clause_chain']] += 1
        
        # Store chain examples
        chain = result['clause_chain']
        if len(chain_examples[chain]) < 10:
            chain_examples[chain].append((ref, text))
    
    # Overview section
    lines.append("## Overview")
    lines.append("")
    lines.append(f"- Total verses analyzed: {total_verses:,}")
    lines.append(f"- Total clauses detected: {total_clauses:,}")
    lines.append(f"- Average clauses per verse: {total_clauses/total_verses:.1f}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Subordinator inventory
    lines.append("## Subordinator Inventory")
    lines.append("")
    lines.append("Tedim Chin subordinators typically appear clause-finally, marking the")
    lines.append("preceding clause as subordinate to the following main clause.")
    lines.append("")
    lines.append("| Subordinator | Gloss | Clause Type | Frequency |")
    lines.append("|--------------|-------|-------------|-----------|")
    
    for marker, gloss in sorted(SUBORDINATORS.items(), key=lambda x: -marker_counts.get(x[0], 0)):
        count = marker_counts.get(marker, 0)
        ctype = {
            'ciangin': 'temporal',
            'hangin': 'causal',
            'dingin': 'purpose',
            'bangin': 'comparative',
            'leh': 'conditional',
            'ahih': 'relative'
        }.get(marker, 'subordinate')
        lines.append(f"| {marker} | {gloss} | {ctype} | {count:,} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Clause type distribution
    lines.append("## Clause Type Distribution")
    lines.append("")
    lines.append("| Clause Type | Count | Percentage |")
    lines.append("|-------------|-------|------------|")
    
    for ctype, count in clause_type_counts.most_common():
        pct = 100 * count / total_clauses
        lines.append(f"| {ctype} | {count:,} | {pct:.1f}% |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Clause chaining patterns
    lines.append("## Clause Chaining Patterns")
    lines.append("")
    lines.append("Clause chain types based on the sequence of clause types within a verse:")
    lines.append("")
    lines.append("| Chain Pattern | Count | Percentage |")
    lines.append("|---------------|-------|------------|")
    
    for chain, count in chain_type_counts.most_common(15):
        pct = 100 * count / total_verses
        lines.append(f"| {chain} | {count:,} | {pct:.1f}% |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Examples by subordinator type
    lines.append("## Subordinate Clause Examples")
    lines.append("")
    
    # Select diverse examples for each subordinator
    gospel_books = {'40', '41', '42', '43'}
    ot_books = {'01', '02', '03', '04', '05', '19', '23'}
    
    for marker in ['ciangin', 'hangin', 'leh', 'dingin', 'bangin']:
        gloss = SUBORDINATORS.get(marker, marker)
        ctype = {
            'ciangin': 'Temporal',
            'hangin': 'Causal',
            'dingin': 'Purpose',
            'bangin': 'Comparative',
            'leh': 'Conditional'
        }.get(marker, 'Subordinate')
        
        lines.append(f"### {ctype}: *{marker}* '{gloss}'")
        lines.append("")
        
        examples = subordinator_examples.get(marker, [])
        if not examples:
            lines.append("*No examples found*")
            lines.append("")
            continue
        
        # Get one from OT, one from Gospels, one other
        selected = []
        for ref, text in examples:
            book = ref[:2]
            if book in gospel_books and not any(r[:2] in gospel_books for r, t in selected):
                selected.append((ref, text))
            elif book in ot_books and not any(r[:2] in ot_books for r, t in selected):
                selected.append((ref, text))
            elif len(selected) < 3:
                selected.append((ref, text))
            if len(selected) >= 3:
                break
        
        for ref, text in selected[:3]:
            lines.append(f"**{format_ref(ref)}**")
            lines.append(format_example(ref, text, kjv))
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Clause chain examples
    lines.append("## Clause Chain Examples")
    lines.append("")
    
    for chain in ['simple', 'subordinate:temporal', 'subordinate:causal', 'subordinate:conditional']:
        examples = chain_examples.get(chain, [])
        if not examples:
            continue
        
        lines.append(f"### {chain.replace('subordinate:', 'Subordinate: ').title()}")
        lines.append("")
        
        # Select diverse examples
        selected = []
        for ref, text in examples:
            book = ref[:2]
            if book in gospel_books and not any(r[:2] in gospel_books for r, t in selected):
                selected.append((ref, text))
            elif book in ot_books and not any(r[:2] in ot_books for r, t in selected):
                selected.append((ref, text))
            elif len(selected) < 2:
                selected.append((ref, text))
            if len(selected) >= 2:
                break
        
        for ref, text in selected[:2]:
            lines.append(f"**{format_ref(ref)}**")
            lines.append(format_example(ref, text, kjv))
            lines.append("")
        
        lines.append("")
    
    # Verb form distribution
    lines.append("## Verb Form Distribution by Clause Type")
    lines.append("")
    lines.append("Henderson (1965) describes two verb stem forms:")
    lines.append("- **Form I** (indicative): Main clause, conclusive sentence")
    lines.append("- **Form II** (subjunctive): Subordinate clause, before relativizer")
    lines.append("")
    lines.append("| Clause Type | Expected Form |")
    lines.append("|-------------|---------------|")
    lines.append("| main (final) | Form I |")
    lines.append("| main (non-final) | Form II |")
    lines.append("| temporal | Form II |")
    lines.append("| causal | Form II |")
    lines.append("| conditional | Form II |")
    lines.append("| purpose | Form II |")
    lines.append("| relative | Form II |")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("Tedim Chin clause structure shows typical SOV/verb-final patterns with:")
    lines.append("")
    lines.append("1. **Subordinators appear clause-finally** - e.g., *ciangin* 'when' marks")
    lines.append("   the end of a temporal clause")
    lines.append("")
    lines.append("2. **Rich subordination system** - temporal (*ciangin*), causal (*hangin*),")
    lines.append("   conditional (*leh*), purpose (*dingin*), comparative (*bangin*)")
    lines.append("")
    lines.append("3. **Verb form alternation** - Form II in subordinate clauses,")
    lines.append("   Form I in final main clauses")
    lines.append("")
    lines.append("4. **Clause chaining** - Multiple subordinate clauses can chain before")
    lines.append("   the main clause, creating complex sentences")
    lines.append("")
    
    return '\n'.join(lines)


def main():
    report = generate_report()
    
    output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / '8-clause-01-subordination.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")


if __name__ == '__main__':
    main()
