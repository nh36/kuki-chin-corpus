#!/usr/bin/env python3
"""
Generate reports for each VP slot category with attested examples.

VP Template: VERB-(DERIV)-(ASPECT)-(DIR)-(MODAL)

Creates separate reports for:
1. Derivational suffixes (valency/semantic changes)
2. Aspect suffixes (viewpoint/completion)
3. Directional suffixes (path/direction)
4. Modal suffixes (modality)
5. Attested combinations (which slots co-occur)
"""

import os
import sys
from collections import Counter, defaultdict
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_morphemes import (
    analyze_word, ASPECT_SUFFIXES, DIRECTIONAL_SUFFIXES, 
    MODAL_SUFFIXES, DERIVATIONAL_SUFFIXES, VERB_STEMS, gloss_sentence
)
from report_utils import (
    load_bible, load_kjv, format_reference, BOOK_NAMES, GOSPEL_CODES
)


def single_pass_analysis(verses):
    """
    Analyze all verses in a single pass, collecting data for all reports.
    Much faster than multiple passes.
    """
    # Collections for each slot category
    slot_counts = {
        'ASPECT': Counter(),
        'DIRECTIONAL': Counter(),
        'MODAL': Counter(),
        'DERIVATIONAL': Counter(),
    }
    slot_examples = {
        'ASPECT': defaultdict(list),
        'DIRECTIONAL': defaultdict(list),
        'MODAL': defaultdict(list),
        'DERIVATIONAL': defaultdict(list),
    }
    
    # For combinations
    combo_counts = Counter()
    combo_examples = defaultdict(list)
    
    # Slot mappings
    all_slots = {
        'ASPECT': ASPECT_SUFFIXES,
        'DIRECTIONAL': DIRECTIONAL_SUFFIXES,
        'MODAL': MODAL_SUFFIXES,
        'DERIVATIONAL': DERIVATIONAL_SUFFIXES,
    }
    
    # Reverse mapping: gloss -> (slot_name, suffix)
    gloss_to_slot = {}
    for slot_name, suffix_dict in all_slots.items():
        for suffix, gloss in suffix_dict.items():
            if gloss not in gloss_to_slot:
                gloss_to_slot[gloss] = []
            gloss_to_slot[gloss].append((slot_name, suffix))
    
    print("Analyzing verses...")
    verse_count = 0
    
    for ref, text in verses.items():
        if len(ref) != 8 or not ref.isdigit():
            continue
        
        verse_count += 1
        if verse_count % 5000 == 0:
            print(f"  Processed {verse_count:,} verses...")
        
        words = text.split()
        for word in words:
            clean = word.lower().rstrip('.,;:!?"\'')
            seg, gloss = analyze_word(clean)
            if not gloss or '?' in gloss:
                continue
            
            # Track which slots are filled for this word
            slots_found = set()
            
            # Check each slot type
            for slot_name, suffix_dict in all_slots.items():
                for suffix, expected_gloss in suffix_dict.items():
                    # Check if this suffix appears with correct gloss
                    if (f'-{suffix}' in seg or seg.endswith(suffix)) and expected_gloss in gloss:
                        slot_counts[slot_name][suffix] += 1
                        slots_found.add(slot_name)
                        # Store example (limit to 10 per suffix for memory)
                        if len(slot_examples[slot_name][suffix]) < 10:
                            slot_examples[slot_name][suffix].append((ref, text, word, (seg, gloss)))
                        break  # Only count each suffix once per word
            
            # Track combinations
            if len(slots_found) >= 2:
                combo = '+'.join(sorted(slots_found))
                combo_counts[combo] += 1
                if len(combo_examples[combo]) < 10:
                    combo_examples[combo].append((ref, text, word, (seg, gloss)))
    
    print(f"  Completed {verse_count:,} verses")
    return slot_counts, slot_examples, combo_counts, combo_examples


def find_diverse_slot_examples(examples, kjv, limit=3):
    """Select diverse examples from collected examples."""
    results = []
    books_used = set()
    gospel_found = False
    
    # Sort by ref to get consistent ordering
    sorted_examples = sorted(examples, key=lambda x: x[0])
    
    # First pass: Gospel
    for ref, text, word, analysis in sorted_examples:
        if gospel_found:
            break
        book_code = ref[:2]
        if book_code not in GOSPEL_CODES:
            continue
        kjv_text = kjv.get(ref, '')
        results.append((ref, text, word, analysis, kjv_text))
        books_used.add(book_code)
        gospel_found = True
    
    # Second pass: diverse books
    for ref, text, word, analysis in sorted_examples:
        if len(results) >= limit:
            break
        book_code = ref[:2]
        if book_code in books_used:
            continue
        kjv_text = kjv.get(ref, '')
        results.append((ref, text, word, analysis, kjv_text))
        books_used.add(book_code)
    
    return results


def format_example_with_gloss(ref, text, word, analysis, kjv_text):
    """Format an example with full interlinear glossing."""
    lines = []
    lines.append(f"**{format_reference(ref)}**")
    lines.append(f"> {text}")
    
    # Add interlinear gloss tier
    glossed = gloss_sentence(text)
    seg_parts = [g[1] for g in glossed]
    gloss_parts = [g[2] for g in glossed]
    lines.append(f"> *{' '.join(seg_parts)}*")
    lines.append(f"> {' '.join(gloss_parts)}")
    
    if kjv_text:
        lines.append(f"> KJV: *{kjv_text}*")
    lines.append(f"> Target: *{word}* → {analysis[0]} → {analysis[1]}")
    lines.append("")
    return lines


# Suffix descriptions
SUFFIX_DESCRIPTIONS = {
    # Aspect
    'ta': 'Perfective - completed action',
    'zo': 'Completive - successfully done',
    'kik': 'Iterative - again, repetition',
    'nawn': 'Continuative - still, ongoing',
    'khin': 'Immediate - already, just now',
    'mang': 'Completive - completely',
    'kim': 'Fully - thoroughly',
    'zawh': 'Finish - done V-ing',
    'khit': 'Sequential - and then',
    'to': 'Continuative - ongoing',
    # Directional
    'khia': 'Outward - motion out of',
    'khiat': 'Away - motion away from',
    'lut': 'Inward - motion into',
    'toh': 'Upward - motion up',
    'cip': 'Downward - motion down',
    'tang': 'Arrive - reach endpoint',
    'sawn': 'Toward - motion toward',
    'lam': 'Direction - toward, manner',
    # Modal
    'ding': 'Irrealis - future, potential',
    'thei': 'Abilitative - can, able to',
    'theih': 'Abilitative - Form II',
    'nuam': 'Desiderative - want to',
    'nop': 'Desiderative - desire',
    'pah': 'Negative ability - cannot',
    'pak': 'Unable - cannot',
    'lawh': 'Unable - cannot',
    'kul': 'Deontic - must, should',
    'lai': 'Prospective - about to',
    'mawk': 'Dubitative - perhaps',
    'ngei': 'Experiential - have done',
    # Derivational
    'sak': 'Causative - make/cause',
    'suk': 'Causative - make become',
    'pih': 'Applicative - for/with',
    'khawm': 'Comitative - together',
    'gawp': 'Intensive - forcefully',
    'nasa': 'Intensive - strongly',
    'zah': 'Fear - fear/respect',
    'hak': 'Intensive - hard, firmly',
    'tawm': 'Diminutive - a little',
    'khak': 'Resultative - result state',
    'zaw': 'Comparative - more',
    'lua': 'Excessive - too much',
    'tel': 'Distributive - each/every',
    'khop': 'Collective - together',
    'loh': 'Negative - negative result',
    'suak': 'Inchoative - become',
}


def generate_slot_report(slot_name, suffix_dict, description, counts, examples, kjv, output_path):
    """Generate a report for one VP slot category."""
    lines = []
    lines.append(f"# {slot_name} Suffixes in Tedim Chin\n")
    lines.append(f"{description}\n")
    lines.append("## Inventory\n")
    lines.append("| Suffix | Gloss | Description | Attestations |")
    lines.append("|--------|-------|-------------|--------------|")
    
    for suffix, gloss in sorted(suffix_dict.items(), key=lambda x: -counts.get(x[0], 0)):
        desc = SUFFIX_DESCRIPTIONS.get(suffix, '')
        count = counts.get(suffix, 0)
        lines.append(f"| -{suffix} | {gloss} | {desc} | {count:,} |")
    
    lines.append("")
    lines.append("## Examples by Suffix\n")
    
    # Generate examples for each suffix
    for suffix, gloss in sorted(suffix_dict.items(), key=lambda x: -counts.get(x[0], 0)):
        if counts.get(suffix, 0) == 0:
            continue
        
        lines.append(f"### -{suffix} ({gloss})\n")
        diverse = find_diverse_slot_examples(examples.get(suffix, []), kjv, limit=3)
        
        for ref, text, word, analysis, kjv_text in diverse:
            lines.extend(format_example_with_gloss(ref, text, word, analysis, kjv_text))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return len(lines)


def generate_combinations_report(combo_counts, combo_examples, kjv, output_path):
    """Generate report on attested VP slot combinations."""
    lines = []
    lines.append("# VP Slot Combinations in Tedim Chin\n")
    lines.append("This report documents which combinations of VP slots actually occur.\n")
    lines.append("## VP Template\n")
    lines.append("```")
    lines.append("VERB-(DERIV)-(ASPECT)-(DIR)-(MODAL)")
    lines.append("```\n")
    lines.append("Not all combinations are equally common. This report shows attested patterns.\n")
    
    lines.append("## Attested Combinations\n")
    lines.append("| Slots Combined | Attestations | Example |")
    lines.append("|---------------|--------------|---------|")
    
    for combo, count in combo_counts.most_common(30):
        if count < 10:
            continue
        ex_list = combo_examples[combo]
        if ex_list:
            ex = ex_list[0]
            lines.append(f"| {combo} | {count:,} | {ex[2]} → {ex[3][1]} |")
    
    lines.append("")
    lines.append("## Detailed Examples\n")
    
    for combo, count in combo_counts.most_common(15):
        if count < 50:
            continue
        
        lines.append(f"### {combo} ({count:,} attestations)\n")
        
        diverse = find_diverse_slot_examples(combo_examples[combo], kjv, limit=3)
        for ref, text, word, analysis, kjv_text in diverse:
            lines.extend(format_example_with_gloss(ref, text, word, analysis, kjv_text))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return len(lines)


def main():
    print("Loading Bible text...")
    verses = load_bible()
    kjv = load_kjv()
    print(f"Loaded {len(verses):,} verses")
    
    # Single pass analysis
    slot_counts, slot_examples, combo_counts, combo_examples = single_pass_analysis(verses)
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              '..', 'docs', 'paradigms')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate slot reports
    reports = [
        ('Aspect', ASPECT_SUFFIXES, 
         "Aspect suffixes mark the internal temporal structure of events: whether complete, ongoing, repeated, etc.",
         '5-verb-05-aspect.md'),
        ('Directional', DIRECTIONAL_SUFFIXES,
         "Directional suffixes indicate the path or direction of motion associated with the verbal action.",
         '5-verb-06-directional.md'),
        ('Modal', MODAL_SUFFIXES,
         "Modal suffixes express modality: possibility, ability, necessity, desire, or epistemic stance.",
         '5-verb-07-modal.md'),
        ('Derivational', DERIVATIONAL_SUFFIXES,
         "Derivational suffixes change verb valency or add semantic content (causative, applicative, etc.).",
         '5-verb-08-derivational.md'),
    ]
    
    print("\nGenerating reports...")
    for name, suffix_dict, desc, filename in reports:
        output_path = os.path.join(output_dir, filename)
        lines = generate_slot_report(name, suffix_dict, desc, 
                                     slot_counts[name.upper()], 
                                     slot_examples[name.upper()], 
                                     kjv, output_path)
        print(f"  {filename}: {lines} lines")
    
    # Generate combinations report
    output_path = os.path.join(output_dir, '5-verb-10-combinations.md')
    lines = generate_combinations_report(combo_counts, combo_examples, kjv, output_path)
    print(f"  5-verb-10-combinations.md: {lines} lines")
    
    print("\nDone!")


if __name__ == '__main__':
    main()
