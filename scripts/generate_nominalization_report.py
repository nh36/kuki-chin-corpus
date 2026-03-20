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
from report_utils import (format_reference, load_bible, load_kjv,
                          find_diverse_examples, format_example)


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
    kjv = load_kjv()
    
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
    report.append("| nuntakna | nuntak (live) | living, life |")
    report.append("")
    
    report.append("### Corpus Examples")
    report.append("")
    examples = find_diverse_examples(verses, kjv, lambda w: w.endswith('na'), limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
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
    examples = find_diverse_examples(verses, kjv, lambda w: w.endswith('pa'), limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
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
    report.append("| zinu | zi (wife) | wife |")
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
