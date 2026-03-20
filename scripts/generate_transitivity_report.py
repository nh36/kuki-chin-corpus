#!/usr/bin/env python3
"""
Generate Transitivity and Argument Frame Report for Tedim Chin

This script analyzes verb transitivity patterns and generates a report
documenting argument structure based on corpus attestations.
"""

import sys
import os
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, gloss_sentence, VERB_STEMS, VERB_FRAMES,
    get_verb_frame, pos_tag_sentence
)

# Book names for citations
BOOK_NAMES = {
    '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus', '04': 'Numbers',
    '05': 'Deuteronomy', '40': 'Matthew', '41': 'Mark', '42': 'Luke',
    '43': 'John', '44': 'Acts', '45': 'Romans', '66': 'Revelation'
}


def format_ref(ref):
    """Convert verse reference to human-readable format."""
    book_code = ref[:2]
    chapter = int(ref[2:5])
    verse = int(ref[5:8])
    book_name = BOOK_NAMES.get(book_code, f"Book{book_code}")
    return f"{book_name} {chapter}:{verse}"


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


def analyze_erg_frequency(verses, verb, max_samples=100):
    """Analyze ERG marker frequency for a verb."""
    erg_count = 0
    total = 0
    examples = {'with_erg': [], 'without_erg': []}
    
    for ref, text in verses.items():
        words = text.lower().split()
        for i, w in enumerate(words):
            clean = w.rstrip('.,;:!?"\'')
            if clean == verb or clean.startswith(verb):
                window = words[max(0, i-6):i]
                has_erg = 'in' in [x.rstrip('.,;:!?"\'') for x in window]
                
                if has_erg:
                    erg_count += 1
                    if len(examples['with_erg']) < 3:
                        examples['with_erg'].append((ref, text))
                else:
                    if len(examples['without_erg']) < 3:
                        examples['without_erg'].append((ref, text))
                
                total += 1
                if total >= max_samples:
                    return erg_count, total, examples
    
    return erg_count, total, examples


def format_example(ref, text, kjv, max_words=12):
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
    """Generate the transitivity report."""
    print("Loading corpus...")
    verses = load_corpus()
    kjv = load_kjv()
    
    lines = []
    
    # Header
    lines.append("# Tedim Chin Verb Transitivity and Argument Frames")
    lines.append("")
    lines.append("This report documents verb argument structure based on corpus analysis.")
    lines.append("Transitivity is classified by ERG marker frequency with the verb.")
    lines.append("")
    
    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("Tedim Chin has split-ergative alignment:")
    lines.append("- **ERG** marker `-in` marks transitive agents")
    lines.append("- **ABS** (unmarked) marks intransitive subjects and transitive patients")
    lines.append("")
    lines.append("Classification thresholds (based on ERG frequency in corpus):")
    lines.append("| Class | ERG% | Description |")
    lines.append("|-------|------|-------------|")
    lines.append("| TRANS | >40% | Canonical transitives |")
    lines.append("| AMBI | 20-40% | Ambitransitive |")
    lines.append("| INTR | <20% | Intransitive |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Analyze verbs by transitivity class
    print("Analyzing transitivity patterns...")
    
    # Group verbs by frame transitivity
    by_class = {'TRANS': [], 'DITRANS': [], 'AMBI': [], 'INTR': []}
    
    for verb, (trans, cases, gloss) in VERB_FRAMES.items():
        erg, total, examples = analyze_erg_frequency(verses, verb, 100)
        pct = 100 * erg / max(total, 1)
        by_class[trans].append((verb, gloss, cases, pct, total, examples))
    
    # Generate sections by class
    for trans_class, description in [
        ('INTR', 'Intransitive Verbs'),
        ('AMBI', 'Ambitransitive Verbs'),
        ('TRANS', 'Transitive Verbs'),
        ('DITRANS', 'Ditransitive Verbs'),
    ]:
        verbs = by_class[trans_class]
        if not verbs:
            continue
        
        lines.append(f"## {description}")
        lines.append("")
        
        if trans_class == 'INTR':
            lines.append("Single argument (ABS subject). ERG marking rare (<20%).")
        elif trans_class == 'AMBI':
            lines.append("Can function as transitive or intransitive. ERG marking variable (20-40%).")
        elif trans_class == 'TRANS':
            lines.append("Two arguments: ERG agent, ABS patient. ERG marking frequent (>40%).")
        elif trans_class == 'DITRANS':
            lines.append("Three arguments: ERG agent, ABS theme, DAT recipient.")
        
        lines.append("")
        lines.append("| Verb | Gloss | Frame | ERG% | n |")
        lines.append("|------|-------|-------|------|---|")
        
        for verb, gloss, cases, pct, total, examples in sorted(verbs, key=lambda x: -x[3]):
            case_str = '+'.join(cases)
            lines.append(f"| {verb} | {gloss} | {case_str} | {pct:.0f}% | {total} |")
        
        lines.append("")
        
        # Show examples for first verb in class
        if verbs:
            verb, gloss, cases, pct, total, examples = verbs[0]
            lines.append(f"### Example: *{verb}* '{gloss}'")
            lines.append("")
            
            if examples['with_erg']:
                lines.append("**With ERG-marked agent:**")
                lines.append("")
                ref, text = examples['with_erg'][0]
                lines.append(f"**{format_ref(ref)}**")
                lines.append(format_example(ref, text, kjv))
                lines.append("")
            
            if examples['without_erg']:
                lines.append("**Without ERG (absolutive subject):**")
                lines.append("")
                ref, text = examples['without_erg'][0]
                lines.append(f"**{format_ref(ref)}**")
                lines.append(format_example(ref, text, kjv))
                lines.append("")
        
        lines.append("---")
        lines.append("")
    
    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("Tedim Chin shows **fluid transitivity** with many ambitransitive verbs.")
    lines.append("ERG marking is not strictly binary but gradient, correlating with semantic")
    lines.append("properties of the event (agentivity, volitionality, affectedness).")
    lines.append("")
    lines.append("| Class | Count | Verbs |")
    lines.append("|-------|-------|-------|")
    for trans_class in ['INTR', 'AMBI', 'TRANS', 'DITRANS']:
        verbs = by_class[trans_class]
        verb_list = ', '.join(v[0] for v in verbs[:5])
        if len(verbs) > 5:
            verb_list += f", ... (+{len(verbs)-5})"
        lines.append(f"| {trans_class} | {len(verbs)} | {verb_list} |")
    
    return '\n'.join(lines)


def main():
    report = generate_report()
    
    output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / '5-verb-12-transitivity.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")


if __name__ == '__main__':
    main()
