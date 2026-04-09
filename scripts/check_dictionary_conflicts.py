#!/usr/bin/env python3
"""
Dictionary Conflict Detection for Tedim Chin Morphological Analyzer.

This script detects when entries in different dictionaries conflict,
which can cause regression bugs when the lookup order changes.

Run this after any dictionary modification to catch conflicts early.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_morphemes import (
    ATOMIC_GLOSSES, VERB_STEMS, NOUN_STEMS, TAM_SUFFIXES,
    CASE_MARKERS, ASPECT_SUFFIXES, MODAL_SUFFIXES, DIRECTIONAL_SUFFIXES,
    FUNCTION_WORDS, DERIVATIONAL_SUFFIXES
)
from morphology.compounds import COMPOUND_WORDS

# Define which dictionary overlaps are EXPECTED (not bugs)
# Format: (dict1, dict2, form, reason)
KNOWN_OVERLAPS = {
    # These are intentional - the form has both lexical and grammatical uses
    ('VERB_STEMS', 'MODAL_SUFFIXES', 'thei'): 'thei is both verb (know) and suffix (ABIL)',
    ('VERB_STEMS', 'MODAL_SUFFIXES', 'nop'): 'nop is both verb (want) and suffix (want)',
    ('VERB_STEMS', 'TAM_SUFFIXES', 'khia'): 'khia is both verb (exit) and directional suffix',
    ('NOUN_STEMS', 'MODAL_SUFFIXES', 'lai'): 'lai is both noun (middle) and modal (PROSP)',
    ('VERB_STEMS', 'CASE_MARKERS', 'pan'): 'pan is both verb (plead) and ablative marker',
    # Add more as we discover them
}

def get_all_dictionaries():
    """Return all dictionaries with their names."""
    return {
        'FUNCTION_WORDS': FUNCTION_WORDS,
        'ATOMIC_GLOSSES': ATOMIC_GLOSSES,
        'VERB_STEMS': VERB_STEMS,
        'NOUN_STEMS': NOUN_STEMS,
        'TAM_SUFFIXES': TAM_SUFFIXES,
        'CASE_MARKERS': CASE_MARKERS,
        'ASPECT_SUFFIXES': ASPECT_SUFFIXES,
        'MODAL_SUFFIXES': MODAL_SUFFIXES,
        'DIRECTIONAL_SUFFIXES': DIRECTIONAL_SUFFIXES,
        'DERIVATIONAL_SUFFIXES': DERIVATIONAL_SUFFIXES,
    }

def find_conflicts():
    """Find all forms that appear in multiple dictionaries with different glosses."""
    dicts = get_all_dictionaries()
    
    # Build index of all forms
    all_forms = {}
    for name, d in dicts.items():
        for form, gloss in d.items():
            if form not in all_forms:
                all_forms[form] = []
            all_forms[form].append((name, gloss))
    
    # Find conflicts (same form, different glosses)
    conflicts = []
    for form, entries in all_forms.items():
        if len(entries) > 1:
            glosses = set(g for _, g in entries)
            if len(glosses) > 1:  # Different glosses = real conflict
                conflicts.append((form, entries))
    
    return conflicts

def classify_conflict(form, entries):
    """Classify a conflict as known/expected or unexpected."""
    dict_names = sorted([e[0] for e in entries])
    for i, (d1, g1) in enumerate(entries):
        for d2, g2 in entries[i+1:]:
            key = (d1, d2, form) if d1 < d2 else (d2, d1, form)
            if key in KNOWN_OVERLAPS:
                return 'known', KNOWN_OVERLAPS[key]
    return 'unexpected', None

def check_dangerous_overlaps():
    """Check for overlaps that are likely to cause bugs.
    
    Dangerous overlaps are where:
    1. ATOMIC_GLOSSES shadows a VERB_STEMS entry (breaks stem+suffix parsing)
    2. ATOMIC_GLOSSES shadows a TAM_SUFFIXES entry (breaks suffix recognition)
    """
    dangerous = []
    
    # ATOMIC_GLOSSES vs VERB_STEMS
    for form in ATOMIC_GLOSSES:
        if form in VERB_STEMS and ATOMIC_GLOSSES[form] != VERB_STEMS[form]:
            dangerous.append((
                form, 
                f"ATOMIC_GLOSSES:{ATOMIC_GLOSSES[form]}", 
                f"VERB_STEMS:{VERB_STEMS[form]}",
                "ATOMIC shadows VERB (will break stem+suffix parsing)"
            ))
    
    # ATOMIC_GLOSSES vs TAM_SUFFIXES
    for form in ATOMIC_GLOSSES:
        if form in TAM_SUFFIXES and ATOMIC_GLOSSES[form] != TAM_SUFFIXES[form]:
            dangerous.append((
                form,
                f"ATOMIC_GLOSSES:{ATOMIC_GLOSSES[form]}",
                f"TAM_SUFFIXES:{TAM_SUFFIXES[form]}",
                "ATOMIC shadows TAM (will break suffix recognition)"
            ))
    
    return dangerous

def main():
    """Run conflict detection and report."""
    print("=" * 60)
    print("DICTIONARY CONFLICT DETECTION")
    print("=" * 60)
    print()
    
    # Check for dangerous overlaps first
    dangerous = check_dangerous_overlaps()
    if dangerous:
        print(f"⚠️  DANGEROUS OVERLAPS FOUND: {len(dangerous)}")
        print("These will likely cause parsing bugs!\n")
        for form, entry1, entry2, reason in dangerous:
            print(f"  {form:15} {entry1:30} vs {entry2}")
            print(f"                 └── {reason}")
        print()
    else:
        print("✓ No dangerous overlaps found\n")
    
    # Find all conflicts
    conflicts = find_conflicts()
    unexpected = []
    known = []
    
    for form, entries in conflicts:
        status, reason = classify_conflict(form, entries)
        if status == 'known':
            known.append((form, entries, reason))
        else:
            unexpected.append((form, entries))
    
    print(f"Total multi-dictionary forms: {len(conflicts)}")
    print(f"  Known/expected overlaps: {len(known)}")
    print(f"  Unexpected overlaps: {len(unexpected)}")
    print()
    
    if unexpected:
        print("UNEXPECTED OVERLAPS (review these):")
        for form, entries in sorted(unexpected)[:20]:
            glosses = ', '.join([f'{n}:{g}' for n, g in entries])
            print(f"  {form:15} -> {glosses}")
        if len(unexpected) > 20:
            print(f"  ... and {len(unexpected) - 20} more")
    
    return len(dangerous)

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
