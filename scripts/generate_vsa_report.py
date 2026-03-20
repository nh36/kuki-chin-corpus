#!/usr/bin/env python3
"""
Generate VSA (Verb Stem Alternation) Questionnaire Report for Tedim Chin

This script generates a report matching Zakaria Muhammad's VSA questionnaire format,
using corpus attestations instead of elicitation. For each verb, examples are
categorized by syntactic context:

1. Affirmative main clause (Form I, declarative)
2. Negative (contains negation marker)
3. A/S Relative (subject/agent relative clause)
4. P Relative (patient/object relative clause)
5. Subordinate clause (temporal/conditional/causal)

Output format matches the VSA questionnaire structure for cross-linguistic comparison.
"""

import sys
import os
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, gloss_sentence, VERB_STEMS,
    detect_clause_boundaries, classify_clause, analyze_clause_structure
)

# =============================================================================
# PSC to Tedim Cognate Mapping
# =============================================================================
# Maps Proto-South-Central reconstructions to Tedim Chin cognates
# Format: PSC stem -> (Tedim Form I, Tedim Form II, English gloss)

PSC_TO_TEDIM = {
    # From Zakaria's questionnaire - common verbs with known Tedim cognates
    '*muu-I/*muk-II': ('mu', 'muh', 'see'),
    '*zaa-I/*zak-II': ('za', 'zak', 'hear'),
    '*nei-I/*neih-II': ('nei', 'neih', 'have'),
    '*thei-I/*theih-II': ('thei', 'theih', 'know'),
    '*ne-I/*nek-II': ('ne', 'nek', 'eat'),
    '*dawn-I/*dawn-II': ('dawn', 'dawn', 'drink'),
    '*piang-I/*pian-II': ('piang', 'pian', 'be.born'),
    '*sih-I/*sit-II': ('si', 'sit', 'die'),
    '*pai-I/*pai-II': ('pai', 'pai', 'go'),
    '*hong-I/*hong-II': ('hong', 'hong', 'come'),
    '*pia-I/*piak-II': ('pia', 'piak', 'give'),
    '*lian-I/*lian-II': ('lian', 'lian', 'big'),
    '*nuam-I/*nuam-II': ('nuam', 'nuam', 'comfortable/want'),
    '*hoih-I/*hoih-II': ('hoih', 'hoih', 'good'),
    '*sak-I/*sak-II': ('sak', 'sak', 'build/cause'),
    '*lei-I/*lei-II': ('lei', 'lei', 'buy'),
    '*ngai-I/*ngaih-II': ('ngai', 'ngaih', 'love/need'),
    '*om-I/*om-II': ('om', 'om', 'exist/stay'),
    '*ci-I/*ci-II': ('ci', 'ci', 'say'),
    '*hi-I/*hi-II': ('hi', 'hi', 'be'),
    '*bawl-I/*bawl-II': ('bawl', 'bawl', 'make/do'),
    '*theih-I/*thei-II': ('thei', 'theih', 'know'),
    '*zawh-I/*zawh-II': ('zawh', 'zawh', 'finish'),
    '*tom-I/*tom-II': ('tom', 'tom', 'meet'),
    '*uk-I/*uk-II': ('uk', 'uk', 'rule'),
    '*khen-I/*khen-II': ('khen', 'khen', 'divide'),
    '*pua-I/*puak-II': ('pua', 'puak', 'carry.on.back'),
    '*huh-I/*huh-II': ('hu', 'huh', 'help'),
    '*khum-I/*khum-II': ('khum', 'khum', 'cover/lock'),
    '*rin-I/*rin-II': ('rin', 'rin', 'believe/trust'),
    '*khawl-I/*khawl-II': ('khawl', 'khawl', 'rest'),
    '*zui-I/*zui-II': ('zui', 'zui', 'follow'),
}

# Book names for citation formatting
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
    '52': '1 Thessalonians', '53': '2 Thessalonians', '54': '1 Timothy',
    '55': '2 Timothy', '56': 'Titus', '57': 'Philemon', '58': 'Hebrews',
    '59': 'James', '60': '1 Peter', '61': '2 Peter', '62': '1 John',
    '63': '2 John', '64': '3 John', '65': 'Jude', '66': 'Revelation'
}

# Negation markers
NEGATION_MARKERS = {'lo', 'kei', 'nilo', 'ngawllo', 'hilo', 'ahilo'}

# Subordinators (temporal, conditional, causal)
SUBORDINATORS = {
    'leh': 'when/if',
    'ciangin': 'when',
    'hangin': 'because',
    'hanga': 'because.of',
    'bangin': 'like',
    'dingin': 'in.order.to',
    'phawt': 'first',
    'zawkciangin': 'after',
    'masakin': 'before',
}

# Relativizers / relative clause markers
RELATIVE_MARKERS = {'te', 'mi', 'pa', 'nu', 'na', 'thu', 'mun'}


def load_corpus():
    """Load Tedim Chin Bible corpus."""
    verses = {}
    corpus_path = Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt'
    with open(corpus_path, 'r', encoding='utf-8') as f:
        for line in f:
            if '\t' in line:
                ref, text = line.strip().split('\t', 1)
                verses[ref] = text
    return verses


def load_kjv():
    """Load KJV translations for glossing."""
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


def format_ref(ref):
    """Convert verse reference to human-readable format."""
    book_code = ref[:2]
    chapter = int(ref[2:5])
    verse = int(ref[5:8])
    book_name = BOOK_NAMES.get(book_code, book_code)
    return f"{book_name} {chapter}:{verse}"


def format_interlinear(text, max_words=15):
    """Format text as interlinear gloss (truncated)."""
    words = text.split()[:max_words]
    truncated = ' '.join(words)
    if len(text.split()) > max_words:
        truncated += '...'
    
    result = gloss_sentence(truncated.rstrip('.'))
    originals = [t[0] for t in result]
    segmented = [t[1] for t in result]
    glosses = [t[2] for t in result]
    
    return ' '.join(originals), ' '.join(segmented), ' '.join(glosses)


def find_verb_position(words, stem):
    """Find the position of a verb stem in a word list."""
    for i, w in enumerate(words):
        clean = w.lower().rstrip('.,;:!?"\'')
        if clean == stem or clean.startswith(stem):
            return i
    return -1


def classify_clause_type(text, stem):
    """
    Classify the syntactic context of a verb occurrence using enhanced clause detection.
    
    Returns one of:
    - 'affirmative': Affirmative main clause
    - 'negative': Negative clause
    - 'relative_as': A/S (subject/agent) relative clause
    - 'relative_p': P (patient/object) relative clause
    - 'subordinate': Subordinate clause (temporal/conditional/causal)
    
    Also returns verb form information.
    """
    words = text.split()
    words_lower = [w.lower().rstrip('.,;:!?"\'') for w in words]
    
    verb_idx = find_verb_position(words, stem)
    if verb_idx == -1:
        return 'unknown', None
    
    verb_word = words_lower[verb_idx]
    
    # Determine verb form based on ending
    # Form II often ends in -h, -k, -t (muh, zak, sit vs mu, za, si)
    form = 'I'
    if verb_word.endswith(('h', 'k', 't')) and verb_word != stem:
        form = 'II'
    
    # Check for negation (within ±3 words of verb)
    for i in range(max(0, verb_idx - 3), min(len(words_lower), verb_idx + 4)):
        if words_lower[i] in NEGATION_MARKERS:
            return 'negative', form
    
    # Use enhanced clause detection
    clause_analysis = analyze_clause_structure(text)
    
    # Find which clause contains our verb
    for clause in clause_analysis['clauses']:
        clause_start = clause.get('start', 0)
        clause_end = clause.get('end', len(words) - 1)
        
        if clause_start <= verb_idx <= clause_end:
            clause_type = clause['type']
            
            # Map clause types to VSA categories
            if clause_type == 'temporal':
                return 'subordinate', form
            elif clause_type == 'causal':
                return 'subordinate', form
            elif clause_type == 'conditional':
                return 'subordinate', form
            elif clause_type == 'purpose':
                return 'subordinate', form
            elif clause_type == 'comparative':
                return 'subordinate', form
            elif clause_type == 'relative':
                # Determine if A/S or P relative based on position
                if verb_idx > 0:
                    return 'relative_p', form
                return 'relative_as', form
    
    # Check for relative clause patterns (verb + relativizer)
    if verb_idx < len(words_lower) - 1:
        next_word = words_lower[verb_idx + 1]
        if next_word in RELATIVE_MARKERS:
            # Form II before relativizer suggests P relative
            if form == 'II':
                return 'relative_p', form
            return 'relative_as', form
    
    # Check for subordinators anywhere in clause
    for sub in SUBORDINATORS:
        if sub in words_lower:
            return 'subordinate', form
    
    return 'affirmative', form


def get_verb_examples(verses, kjv, form1, form2, max_per_category=5):
    """
    Extract examples for a verb, categorized by syntactic context.
    
    Searches for both Form I and Form II stems.
    Now also tracks detected verb form (I vs II) from morphology.
    """
    examples = {
        'affirmative': [],
        'negative': [],
        'relative_as': [],
        'relative_p': [],
        'subordinate': [],
    }
    
    # Track form distribution for analysis
    form_stats = {'I': 0, 'II': 0}
    
    stems = [form1]
    if form2 and form2 != form1:
        stems.append(form2)
    
    # Sort stems by length (longest first) to match compounds before components
    stems_sorted = sorted(stems, key=len, reverse=True)
    
    for ref, text in verses.items():
        words_lower = [w.lower().rstrip('.,;:!?"\'') for w in text.split()]
        
        for stem in stems_sorted:
            matched = False
            for word in words_lower:
                if word == stem or word.startswith(stem):
                    clause_type, detected_form = classify_clause_type(text, stem)
                    
                    if detected_form:
                        form_stats[detected_form] += 1
                    
                    if clause_type in examples and len(examples[clause_type]) < max_per_category:
                        examples[clause_type].append({
                            'ref': ref,
                            'tedim': text,
                            'kjv': kjv.get(ref, ''),
                            'stem': stem,
                            'form': detected_form or ('I' if stem == form1 else 'II'),
                            'clause_type': clause_type
                        })
                    matched = True
                    break
            if matched:
                break
    
    return examples


def generate_verb_section(psc, form1, form2, gloss, examples, kjv):
    """Generate a report section for one verb."""
    lines = []
    
    # Header
    lines.append(f"## {gloss.upper()}")
    lines.append(f"**PSC:** {psc}")
    lines.append(f"**Tedim:** {form1} (Form I), {form2} (Form II)")
    lines.append("")
    
    # Clause type sections matching questionnaire order
    section_names = {
        'affirmative': 'Affirmative',
        'negative': 'Negative',
        'relative_as': 'A/S Relative',
        'relative_p': 'P Relative',
        'subordinate': 'Subordinate Clause',
    }
    
    for clause_type, section_name in section_names.items():
        exs = examples.get(clause_type, [])
        lines.append(f"### {section_name}")
        lines.append("")
        
        if not exs:
            lines.append("*No examples found in corpus.*")
            lines.append("")
            continue
        
        for ex in exs[:3]:  # Max 3 examples per context
            orig, seg, glosses = format_interlinear(ex['tedim'])
            lines.append(f"**{format_ref(ex['ref'])}** (Form {ex['form']})")
            lines.append(f"> {orig}")
            lines.append(f"> *{seg}*")
            lines.append(f"> {glosses}")
            if ex['kjv']:
                kjv_text = ex['kjv'][:150]
                if len(ex['kjv']) > 150:
                    kjv_text += '...'
                lines.append(f"> KJV: *{kjv_text}*")
            lines.append("")
    
    lines.append("---")
    lines.append("")
    
    return '\n'.join(lines)


def generate_report():
    """Generate the full VSA questionnaire report."""
    print("Loading corpus...")
    verses = load_corpus()
    kjv = load_kjv()
    
    lines = []
    
    # Header
    lines.append("# Verb Stem Alternation Report: Tedim Chin")
    lines.append("")
    lines.append("This report provides corpus attestations matching the VSA questionnaire format")
    lines.append("(Zakaria Muhammad). Examples are drawn from the Tedim Chin Bible and categorized")
    lines.append("by syntactic context.")
    lines.append("")
    lines.append("## Syntactic Contexts")
    lines.append("")
    lines.append("| Context | Description | Typical Stem Form |")
    lines.append("|---------|-------------|-------------------|")
    lines.append("| Affirmative | Main clause, positive polarity | Form I |")
    lines.append("| Negative | Contains negation marker (lo, kei) | Form I |")
    lines.append("| A/S Relative | Subject/agent relative clause | Form II |")
    lines.append("| P Relative | Patient/object relative clause | Form II |")
    lines.append("| Subordinate | Temporal, conditional, causal | Form II |")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Generate section for each verb
    print("Extracting examples...")
    for psc, (form1, form2, gloss) in sorted(PSC_TO_TEDIM.items(), key=lambda x: x[1][2]):
        print(f"  {gloss} ({form1}/{form2})...")
        examples = get_verb_examples(verses, kjv, form1, form2, max_per_category=5)
        section = generate_verb_section(psc, form1, form2, gloss, examples, kjv)
        lines.append(section)
    
    return '\n'.join(lines)


def main():
    report = generate_report()
    
    output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / '5-verb-11-vsa-questionnaire.md'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nReport written to {output_path}")
    print(f"Total lines: {len(report.split(chr(10)))}")


if __name__ == '__main__':
    main()
