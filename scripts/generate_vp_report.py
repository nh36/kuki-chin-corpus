#!/usr/bin/env python3
"""
Generate VP Structure Report for Tedim Chin

Documents verb phrase template, serial verbs, auxiliaries, and sentence-final particles.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word, gloss_sentence
from report_utils import (format_reference, load_bible, load_kjv,
                          find_diverse_examples, format_example)


def generate_report():
    """Generate VP structure report."""
    print("Loading corpus...")
    verses = load_bible()
    kjv = load_kjv()
    
    print("Analyzing VP patterns...")
    
    report = []
    report.append("# Tedim Chin Verb Phrase Structure")
    report.append("")
    report.append("This report documents the structure of verb phrases in Tedim Chin,")
    report.append("including the verb template, serial verbs, auxiliaries, and particles.")
    report.append("")
    
    # VP Template
    report.append("## Verb Phrase Template")
    report.append("")
    report.append("The Tedim Chin VP has the following general structure:")
    report.append("")
    report.append("```")
    report.append("(NEG) + (OBJ.AGR) + SUBJ.AGR + VERB-STEM + (DERIV) + (ASPECT) + (DIR) + (TAM) + (SFP)")
    report.append("```")
    report.append("")
    report.append("### Slot Descriptions")
    report.append("")
    report.append("| Slot | Content | Examples |")
    report.append("|------|---------|----------|")
    report.append("| NEG | Negation | kei (NEG) |")
    report.append("| OBJ.AGR | Object agreement | hong- (3>1/2), kong- (1>3) |")
    report.append("| SUBJ.AGR | Subject agreement | ka-, na-, a-, i- |")
    report.append("| VERB-STEM | Lexical verb | pai, bawl, mu, gen |")
    report.append("| DERIV | Derivational | -sak (CAUS), -pih (APPL), ki- (REFL) |")
    report.append("| ASPECT | Aspect markers | -zo (COMPL), -kik (ITER) |")
    report.append("| DIR | Directional | -khia (out), -lut (in), -toh (up) |")
    report.append("| TAM | Tense-Aspect-Mood | -ding (IRR), -ta (PFV), -lai (PROSP) |")
    report.append("| SFP | Sentence-final particle | hi, hiam, hen, aw |")
    report.append("")
    
    # Form I vs Form II
    report.append("---")
    report.append("")
    report.append("## Form I vs Form II")
    report.append("")
    report.append("Tedim Chin verbs have two stems that alternate based on clause type:")
    report.append("")
    report.append("| Feature | Form I (Indicative) | Form II (Subjunctive) |")
    report.append("|---------|---------------------|----------------------|")
    report.append("| Clause type | Main, conclusive | Subordinate, inconclusive |")
    report.append("| Shape | Open syllable | Closed syllable |")
    report.append("| Example | mu 'see' | muh 'see.II' |")
    report.append("| Example | nei 'have' | neih 'have.II' |")
    report.append("")
    
    # Serial verbs
    report.append("---")
    report.append("")
    report.append("## Serial Verb Constructions")
    report.append("")
    report.append("Tedim Chin uses serial verb constructions where multiple verbs")
    report.append("share a subject and describe aspects of a single event.")
    report.append("")
    report.append("### Common Patterns")
    report.append("")
    report.append("| Pattern | Example | Meaning |")
    report.append("|---------|---------|---------|")
    report.append("| V1 + V2(motion) | lak-khia | take-go.out 'take out' |")
    report.append("| V1 + V2(direction) | pai-lut | go-enter 'go in' |")
    report.append("| V1 + V2(result) | bawl-zo | make-complete 'finish making' |")
    report.append("| V1 + V2(manner) | pai-zawm | go-continue 'keep going' |")
    report.append("")
    
    # Corpus examples - serial verbs
    report.append("### Illustrated Examples")
    report.append("")
    examples = find_diverse_examples(verses, kjv, lambda w: 'khia' in w, limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
    # Auxiliaries
    report.append("---")
    report.append("")
    report.append("## Auxiliary Verbs")
    report.append("")
    report.append("Several verbs function as auxiliaries in VP structure:")
    report.append("")
    report.append("| Auxiliary | Meaning | Function |")
    report.append("|-----------|---------|----------|")
    report.append("| om | be, exist | Existential, progressive |")
    report.append("| hi | be (copula) | Equational, identificational |")
    report.append("| thei | can, able | Modal (ability) |")
    report.append("| nuam | want | Modal (volition) |")
    report.append("| ding | will | Modal (future/intention) |")
    report.append("| kul | must | Modal (obligation) |")
    report.append("")
    
    # Sentence-final particles
    report.append("---")
    report.append("")
    report.append("## Sentence-Final Particles")
    report.append("")
    report.append("Tedim Chin uses sentence-final particles for illocutionary force:")
    report.append("")
    report.append("| Particle | Function | Gloss |")
    report.append("|----------|----------|-------|")
    report.append("| hi | Assertive | SFP |")
    report.append("| hiam | Interrogative (yes/no) | Q |")
    report.append("| hen | Imperative (polite) | IMP |")
    report.append("| ta | Imperative | IMP |")
    report.append("| aw | Exclamative | EXCL |")
    report.append("| lo | Imperative (hortative) | HORT |")
    report.append("| leh | Conditional consequence | then |")
    report.append("")
    
    # Negation
    report.append("---")
    report.append("")
    report.append("## Negation")
    report.append("")
    report.append("Negation in Tedim Chin uses *kei* (or variant forms) before the verb:")
    report.append("")
    report.append("```")
    report.append("ka-pai kei → I don't go")
    report.append("NEG position: before verb complex or at end")
    report.append("```")
    report.append("")
    report.append("### Negative patterns")
    report.append("")
    report.append("| Pattern | Example | Meaning |")
    report.append("|---------|---------|---------|")
    report.append("| V kei | pai kei | not go |")
    report.append("| V lo | pai lo | not go (milder) |")
    report.append("| om kei | om kei | not exist |")
    report.append("| thei kei | thei kei | cannot |")
    report.append("")
    
    # Summary
    report.append("---")
    report.append("")
    report.append("## Summary of VP Structure Types")
    report.append("")
    report.append("### Type 1: Simple VP")
    report.append("```")
    report.append("SUBJ.AGR + VERB + (TAM) + (SFP)")
    report.append("a-pai-hi 'he goes'")
    report.append("```")
    report.append("")
    report.append("### Type 2: Transitive VP with Object Agreement")
    report.append("```")
    report.append("OBJ.AGR + SUBJ.AGR + VERB + (TAM) + (SFP)")
    report.append("kong-mu-hi 'I see him'")
    report.append("```")
    report.append("")
    report.append("### Type 3: Derived VP")
    report.append("```")
    report.append("SUBJ.AGR + VERB + DERIV + (TAM) + (SFP)")
    report.append("ka-pai-sak-hi 'I make go (send)'")
    report.append("```")
    report.append("")
    report.append("### Type 4: Negated VP")
    report.append("```")
    report.append("SUBJ.AGR + VERB + NEG + (SFP)")
    report.append("ka-pai-kei-hi 'I don't go'")
    report.append("```")
    report.append("")
    
    # Illustrated examples for each type
    report.append("---")
    report.append("")
    report.append("## Illustrated Examples by Type")
    report.append("")
    
    # Transitive with agreement
    report.append("### Transitive VP (Object Agreement)")
    report.append("")
    examples = find_diverse_examples(verses, kjv, lambda w: w.startswith('hong') or w.startswith('kong'), limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
    # Negated
    report.append("### Negated VP")
    report.append("")
    examples = find_diverse_examples(verses, kjv, lambda w: w == 'kei' or w.endswith('kei'), limit=3)
    for ref, text, word, analysis, kjv_text in examples:
        report.extend(format_example(ref, text, word, analysis, kjv_text))
    
    report.append("---")
    report.append("")
    report.append("*Generated from Tedim Chin Bible corpus analysis*")
    
    return '\n'.join(report)


if __name__ == '__main__':
    report = generate_report()
    
    output_path = os.path.join(os.path.dirname(__file__), 
                               '..', 'docs', 'paradigms', 'vp_structure.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {output_path}")
