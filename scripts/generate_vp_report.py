#!/usr/bin/env python3
"""
Generate VP Structure Report for Tedim Chin

Documents verb phrase template, serial verbs, auxiliaries, and sentence-final particles.
"""

import sys
import os
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import analyze_word, gloss_sentence

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


def is_gospel(ref):
    """Check if reference is from a Gospel."""
    return ref[:2] in GOSPEL_CODES


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


def find_diverse_examples(verses, pattern_check, limit=3, require_gospel=True):
    """Find examples from diverse books."""
    examples = []
    books_used = set()
    gospel_found = False
    
    for ref, text in sorted(verses.items()):
        if len(ref) != 8 or not ref.isdigit():
            continue
        
        if pattern_check(text):
            book_code = ref[:2]
            if book_code in books_used:
                continue
            
            is_gsp = book_code in GOSPEL_CODES
            if is_gsp:
                gospel_found = True
            
            glossed = gloss_sentence(text)
            examples.append((ref, text, glossed))
            books_used.add(book_code)
            
            if len(examples) >= limit:
                if require_gospel and not gospel_found:
                    continue
                return examples
    
    return examples


def generate_report():
    """Generate VP structure report."""
    print("Loading corpus...")
    verses = load_bible()
    
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
    
    # Illustrative paradigm
    report.append("### Example Expansion")
    report.append("")
    report.append("```")
    report.append("kong-hong-pai-sak-zo-khia-ding-hi")
    report.append("1>3-INV-go-CAUS-COMPL-out-IRR-SFP")
    report.append("'I will have completely made him go out'")
    report.append("```")
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
    report.append("| Example | pai 'go' | pai 'go' (no change) |")
    report.append("| Example | nei 'have' | neih 'have.II' |")
    report.append("")
    report.append("### Distribution")
    report.append("")
    report.append("**Form I** appears in:")
    report.append("- Main clauses")
    report.append("- Declarative sentences")
    report.append("- With sentence-final particle *hi*")
    report.append("")
    report.append("**Form II** appears in:")
    report.append("- Subordinate clauses")
    report.append("- Before nominalization")
    report.append("- Before certain TAM markers")
    report.append("- In relative clauses")
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
    
    def has_serial_pattern(text):
        patterns = ['khia ', 'lut ', 'toh ', 'cip ', 'kik ']
        return any(p in text.lower() for p in patterns)
    
    examples = find_diverse_examples(verses, has_serial_pattern, limit=3)
    for ref, text, glossed in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        # Show first few glossed words
        gloss_str = ' '.join([f"{w[0]}={w[2]}" for w in glossed[:6]])
        report.append(f"> {gloss_str}...")
        report.append("")
    
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
    report.append("### om (existential/progressive)")
    report.append("")
    report.append("*om* 'exist, be' is used for existential statements and progressive aspect:")
    report.append("")
    
    def has_om(text):
        words = text.lower().split()
        return 'om' in words or any(w.startswith('om') for w in words)
    
    examples = find_diverse_examples(verses, has_om, limit=2)
    for ref, text, glossed in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append("")
    
    report.append("### hi (copula)")
    report.append("")
    report.append("*hi* 'be' functions as a copula and sentence-final particle:")
    report.append("")
    
    def has_hi(text):
        return text.rstrip('.,;:!?"\'').endswith(' hi')
    
    examples = find_diverse_examples(verses, has_hi, limit=2)
    for ref, text, glossed in examples:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
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
    report.append("### hi (Assertive)")
    report.append("Marks declarative statements:")
    report.append("")
    
    examples = find_diverse_examples(verses, has_hi, limit=2)
    for ref, text, glossed in examples:
        report.append(f"> {text} — {format_reference(ref)}")
        report.append("")
    
    report.append("### hiam (Interrogative)")
    report.append("Marks yes/no questions:")
    report.append("")
    
    def has_hiam(text):
        return 'hiam' in text.lower()
    
    examples = find_diverse_examples(verses, has_hiam, limit=2)
    for ref, text, glossed in examples:
        report.append(f"> {text} — {format_reference(ref)}")
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
    report.append("### Type 4: Complex VP (Serial)")
    report.append("```")
    report.append("SUBJ.AGR + V1 + V2 + (TAM) + (SFP)")
    report.append("a-lak-khia-hi 'he takes out'")
    report.append("```")
    report.append("")
    report.append("### Type 5: Negated VP")
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
    
    # Simple VP
    report.append("### Simple VP")
    report.append("")
    def is_simple_vp(text):
        words = text.split()
        return len(words) < 10 and any(w.startswith('a') for w in words)
    
    examples = find_diverse_examples(verses, is_simple_vp, limit=3)
    for ref, text, glossed in examples[:3]:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append("")
    
    # Transitive with agreement
    report.append("### Transitive VP (Object Agreement)")
    report.append("")
    def has_object_agr(text):
        return 'hong' in text.lower() or 'kong' in text.lower()
    
    examples = find_diverse_examples(verses, has_object_agr, limit=3)
    for ref, text, glossed in examples[:3]:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append("")
    
    # Negated
    report.append("### Negated VP")
    report.append("")
    def has_neg(text):
        return ' kei' in text.lower() or text.lower().endswith('kei')
    
    examples = find_diverse_examples(verses, has_neg, limit=3)
    for ref, text, glossed in examples[:3]:
        report.append(f"**{format_reference(ref)}**")
        report.append(f"> {text}")
        report.append("")
    
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
