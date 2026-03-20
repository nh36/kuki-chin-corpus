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
from analyze_morphemes import analyze_word
from report_utils import (format_reference, load_bible, load_kjv, 
                          find_diverse_examples, format_example)


def count_patterns(verses):
    """Count derivational pattern occurrences."""
    counts = Counter()
    
    for ref, text in verses.items():
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            if clean.startswith('ki'):
                counts['ki'] += 1
            if 'sak' in clean:
                counts['sak'] += 1
            if 'pih' in clean:
                counts['pih'] += 1
            if 'khawm' in clean:
                counts['khawm'] += 1
            if 'gawp' in clean:
                counts['gawp'] += 1
            if 'thei' in clean:
                counts['thei'] += 1
    
    return counts


def generate_report():
    """Generate valency/voice report."""
    print("Loading corpus...")
    verses = load_bible()
    kjv = load_kjv()
    
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
    examples = find_diverse_examples(verses, kjv, lambda w: w.startswith('ki'), limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
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
    examples = find_diverse_examples(verses, kjv, lambda w: 'sak' in w, limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
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
    examples = find_diverse_examples(verses, kjv, lambda w: 'pih' in w, limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
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
