#!/usr/bin/env python3
"""
Generate Switch Reference and Clause Chaining Report for Tedim Chin

This script analyzes switch reference patterns (same-subject vs different-subject)
and clause chaining in the Tedim Chin corpus.
"""

import sys
import os
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, gloss_sentence, VERB_STEMS
)

# Book names for citations
BOOK_NAMES = {
    '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus', '04': 'Numbers',
    '05': 'Deuteronomy', '19': 'Psalms', '20': 'Proverbs', '23': 'Isaiah',
    '40': 'Matthew', '41': 'Mark', '42': 'Luke', '43': 'John',
    '44': 'Acts', '45': 'Romans', '66': 'Revelation'
}


def format_ref(ref):
    """Convert verse reference to human-readable format."""
    if len(ref) < 8 or not ref[:2].isdigit():
        return ref
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
            if '\t' in line and not line.startswith('#'):
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
    """Generate the switch reference report."""
    print("Loading corpus...")
    verses = load_corpus()
    kjv = load_kjv()
    
    lines = []
    
    # Header
    lines.append("# Tedim Chin Switch Reference and Clause Chaining")
    lines.append("")
    lines.append("This report documents switch reference patterns (same-subject vs different-subject)")
    lines.append("and clause chaining constructions in the Tedim Chin Bible corpus.")
    lines.append("")
    
    # Introduction
    lines.append("## Background")
    lines.append("")
    lines.append("Switch reference is a grammatical system found in many Tibeto-Burman languages")
    lines.append("that tracks whether the subject of a subordinate clause is the same as (SS)")
    lines.append("or different from (DS) the subject of the main clause.")
    lines.append("")
    lines.append("In Tedim Chin:")
    lines.append("- **Same-subject (SS)**: Marked by converb suffix `-in` on the first verb")
    lines.append("- **Different-subject (DS)**: No `-in` suffix; different agreement markers")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Analyze converb patterns
    print("Analyzing switch reference patterns...")
    
    # SS converb counts
    ss_verb_counts = Counter()
    ss_examples = defaultdict(list)
    
    # Chain length stats
    chain_lengths = Counter()
    chain_examples = defaultdict(list)
    
    # DS pattern stats
    ds_patterns = Counter()
    ds_examples = []
    
    # Gospel and OT book codes for diverse examples
    gospel_books = {'40', '41', '42', '43'}
    ot_books = {'01', '02', '19', '23'}
    
    for ref, text in verses.items():
        words = text.split()
        chain_count = 0
        
        for i in range(len(words)):
            word = words[i].lower().rstrip('.,;:!?"\'')
            
            # Check for VERB-in converb (SS marker)
            if word.endswith('in') and len(word) > 3:
                base = word[:-2]
                if base in VERB_STEMS:
                    ss_verb_counts[base] += 1
                    chain_count += 1
                    
                    if len(ss_examples[base]) < 5:
                        ss_examples[base].append((ref, text))
            
            # End of sentence - record chain length
            if word in ['hi', 'hi.', 'hiam', 'hiam.']:
                if chain_count > 0:
                    chain_lengths[chain_count] += 1
                    if len(chain_examples[chain_count]) < 5:
                        chain_examples[chain_count].append((ref, text))
                chain_count = 0
        
        # Check for DS patterns (ahih ciangin)
        if 'ahih ciangin' in text.lower():
            ds_patterns['ahih_ciangin'] += 1
            if len(ds_examples) < 15:
                ds_examples.append((ref, text))
    
    # Same-Subject Section
    lines.append("## Same-Subject (SS) Converb Construction")
    lines.append("")
    lines.append("The SS converb is formed with `-in` suffix on the verb stem.")
    lines.append("It indicates that the subject of the converb clause is identical to")
    lines.append("the subject of the following main clause.")
    lines.append("")
    lines.append("### Pattern")
    lines.append("")
    lines.append("```")
    lines.append("SUBJ  [VERB-in]  [VERB]  hi")
    lines.append("      (converb)  (main)")
    lines.append("```")
    lines.append("")
    lines.append("### Most Common SS Converb Verbs")
    lines.append("")
    lines.append("| Verb Stem | -in Form | Gloss | Count |")
    lines.append("|-----------|----------|-------|-------|")
    
    for verb, count in ss_verb_counts.most_common(20):
        gloss = VERB_STEMS.get(verb, '?')
        lines.append(f"| {verb} | {verb}in | {gloss} | {count:,} |")
    
    lines.append("")
    lines.append(f"**Total SS converb instances:** {sum(ss_verb_counts.values()):,}")
    lines.append("")
    
    # SS Examples
    lines.append("### SS Converb Examples")
    lines.append("")
    
    # Select diverse examples for top converb verbs
    example_verbs = ['pan', 'bawl', 'zah', 'ngen', 'lungdam']
    for verb in example_verbs:
        if verb in ss_examples:
            gloss = VERB_STEMS.get(verb, '?')
            lines.append(f"**{verb}in** '{gloss}':")
            lines.append("")
            
            # Find one from gospels, one from OT
            selected = []
            for ref, text in ss_examples[verb]:
                book = ref[:2]
                if book in gospel_books and not any(r[:2] in gospel_books for r, t in selected):
                    selected.append((ref, text))
                elif book in ot_books and not any(r[:2] in ot_books for r, t in selected):
                    selected.append((ref, text))
                if len(selected) >= 2:
                    break
            
            if not selected:
                selected = ss_examples[verb][:1]
            
            for ref, text in selected[:2]:
                lines.append(f"**{format_ref(ref)}**")
                lines.append(format_example(ref, text, kjv))
                lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Clause Chaining Section
    lines.append("## Clause Chaining")
    lines.append("")
    lines.append("Tedim Chin allows multiple converb clauses to chain before the main clause.")
    lines.append("Each converb clause maintains same-subject reference with the final main clause.")
    lines.append("")
    lines.append("### Chain Length Distribution")
    lines.append("")
    lines.append("| Chain Length | Sentences | Percentage |")
    lines.append("|--------------|-----------|------------|")
    
    total_chains = sum(chain_lengths.values())
    for length in sorted(chain_lengths.keys()):
        count = chain_lengths[length]
        if count > 10:
            pct = 100 * count / total_chains
            lines.append(f"| {length} converb(s) | {count:,} | {pct:.1f}% |")
    
    lines.append("")
    lines.append(f"**Total sentences with converb chains:** {total_chains:,}")
    lines.append("")
    
    # Chain Examples
    lines.append("### Clause Chain Examples")
    lines.append("")
    
    for length in [2, 3]:
        if length in chain_examples:
            lines.append(f"**{length}-clause chain:**")
            lines.append("")
            ref, text = chain_examples[length][0]
            lines.append(f"**{format_ref(ref)}**")
            lines.append(format_example(ref, text, kjv))
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Different-Subject Section
    lines.append("## Different-Subject (DS) Patterns")
    lines.append("")
    lines.append("When the subordinate clause has a different subject from the main clause,")
    lines.append("the converb suffix `-in` is not used. Instead:")
    lines.append("")
    lines.append("1. **Explicit subject NPs** appear in each clause")
    lines.append("2. **Agreement markers** differ between clauses")
    lines.append("3. **Subordinators** like *ciangin* 'when' mark clause boundaries")
    lines.append("")
    lines.append("### Common DS Pattern: *ahih ciangin*")
    lines.append("")
    lines.append("The construction *ahih ciangin* (be.3SG.REL when) is a common DS marker.")
    lines.append("It introduces a temporal clause with a different subject from the main clause.")
    lines.append("")
    lines.append(f"**Occurrences:** {ds_patterns['ahih_ciangin']:,}")
    lines.append("")
    
    # DS Examples
    lines.append("### DS Examples")
    lines.append("")
    
    # Select diverse DS examples
    selected_ds = []
    for ref, text in ds_examples:
        book = ref[:2]
        if book in gospel_books and not any(r[:2] in gospel_books for r, t in selected_ds):
            selected_ds.append((ref, text))
        elif book in ot_books and not any(r[:2] in ot_books for r, t in selected_ds):
            selected_ds.append((ref, text))
        if len(selected_ds) >= 3:
            break
    
    for ref, text in selected_ds[:3]:
        lines.append(f"**{format_ref(ref)}**")
        lines.append(format_example(ref, text, kjv))
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("Tedim Chin exhibits a **converb-based switch reference system**:")
    lines.append("")
    lines.append("| Feature | Same-Subject (SS) | Different-Subject (DS) |")
    lines.append("|---------|-------------------|------------------------|")
    lines.append("| Verb form | VERB**-in** | VERB (no -in) |")
    lines.append("| Subject marking | Once (on main verb) | Explicit in each clause |")
    lines.append("| Agreement | Shared | Different per clause |")
    lines.append("| Subordinator | Optional | Often *ciangin*, *hangin* |")
    lines.append("")
    lines.append("### Key Findings")
    lines.append("")
    lines.append(f"1. **SS converbs are frequent**: {sum(ss_verb_counts.values()):,} instances")
    lines.append(f"2. **Clause chains common**: Most chains are 1-2 converbs ({chain_lengths.get(1, 0) + chain_lengths.get(2, 0):,} sentences)")
    lines.append(f"3. **DS marked structurally**: Through subordinators and explicit subjects, not a dedicated morpheme")
    lines.append("")
    lines.append("This system allows Tedim Chin to efficiently express complex multi-clause")
    lines.append("sentences while clearly tracking referential coherence across clauses.")
    
    return '\n'.join(lines)


def main():
    report = generate_report()
    
    output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / '8-clause-02-switch-reference.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")


if __name__ == '__main__':
    main()
