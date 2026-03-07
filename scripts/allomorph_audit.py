#!/usr/bin/env python3
"""
Allomorph Audit System for Tedim Chin Morphological Analyzer

This script checks for potential over-segmentation issues where:
1. Stem material may be incorrectly included in suffix analysis
2. Allomorphs are not properly phonologically conditioned
3. Unknown bases appear before known suffixes

Key suffixes to audit:
- -te (plural)
- -na (nominalizer)
- -in (ergative/instrumental)
- -ah (locative)
- -pa (masculine)
- -nu (feminine)
"""

import sys
sys.path.insert(0, '.')
from analyze_morphemes import analyze_word, NOUN_STEMS, VERB_STEMS, FUNCTION_WORDS
from collections import Counter, defaultdict
import re

def load_corpus(filepath='bibles/extracted/ctd/ctd-x-bible.txt'):
    """Load corpus and yield (verse_id, word) pairs."""
    with open(filepath) as f:
        for line in f:
            if '\t' not in line:
                continue
            verse_id, text = line.strip().split('\t', 1)
            for word in text.split():
                word_clean = re.sub(r'^[^a-zA-Z]+|[^a-zA-Z]+$', '', word)
                if word_clean:
                    yield verse_id, word_clean

def audit_suffix(suffix, gloss_marker, corpus_path='bibles/extracted/ctd/ctd-x-bible.txt'):
    """
    Audit a suffix for potential over-segmentation.
    
    Returns:
    - correctly_analyzed: words where base is a known stem
    - unknown_base: words where base is NOT a known stem
    - possible_allomorph: words where an extended form might be the base
    """
    results = {
        'correct': Counter(),
        'unknown_base': Counter(),
        'possible_allomorph': [],
        'no_gloss_marker': Counter(),
    }
    
    for verse_id, word in load_corpus(corpus_path):
        word_lower = word.lower()
        
        # Only process words ending in this suffix
        if not word_lower.endswith(suffix):
            continue
            
        seg, gloss = analyze_word(word)
        
        # Check if gloss contains the expected marker
        if gloss_marker not in gloss:
            # Word ends in suffix but not glossed as such
            results['no_gloss_marker'][word] += 1
            continue
        
        # Check if there's an unknown element before the suffix
        if '?' in gloss:
            # Extract the base
            base = word_lower[:-len(suffix)]
            
            # Is the base a known stem?
            if base in NOUN_STEMS or base in VERB_STEMS or base in FUNCTION_WORDS:
                results['correct'][word] += 1
            else:
                results['unknown_base'][word] += 1
                
                # Check if this might be an allomorph issue
                # e.g., if word is "vokte" and we're checking -te,
                # maybe "vok" is the stem and -te is the suffix
                if len(base) > 2:
                    # Check various truncations
                    for i in range(1, min(3, len(base))):
                        truncated = base[:-i]
                        if truncated in NOUN_STEMS or truncated in VERB_STEMS:
                            results['possible_allomorph'].append({
                                'word': word,
                                'analyzed_base': base,
                                'truncated_base': truncated,
                                'truncated_meaning': NOUN_STEMS.get(truncated) or VERB_STEMS.get(truncated),
                                'extra_chars': base[-i:],
                            })
                            break
        else:
            results['correct'][word] += 1
    
    return results

def check_phonological_conditioning(corpus_path='bibles/extracted/ctd/ctd-x-bible.txt'):
    """
    Check if suffix allomorphs show phonological conditioning.
    
    For -te plural:
    - Does -te appear after all stem-final segments?
    - Are there patterns like -ite only after certain segments?
    """
    te_contexts = defaultdict(Counter)
    
    for verse_id, word in load_corpus(corpus_path):
        word_lower = word.lower()
        if word_lower.endswith('te') and len(word_lower) > 2:
            # Get the segment before -te
            preceding = word_lower[-3:-2]  # character before 'te'
            te_contexts[preceding][word] += 1
    
    return te_contexts

def main():
    print("=" * 70)
    print("TEDIM CHIN MORPHOLOGICAL ANALYZER - ALLOMORPH AUDIT")
    print("=" * 70)
    
    # Audit -te (plural)
    print("\n## AUDIT: -te (Plural Suffix)")
    print("-" * 50)
    te_results = audit_suffix('te', 'PL')
    
    print(f"\nCorrectly analyzed: {sum(te_results['correct'].values()):,} tokens")
    print(f"Unknown base + -te: {sum(te_results['unknown_base'].values()):,} tokens")
    print(f"Missing PL gloss: {sum(te_results['no_gloss_marker'].values()):,} tokens")
    
    print("\nTop 20 unknown base + -te words:")
    for word, count in te_results['unknown_base'].most_common(20):
        seg, gloss = analyze_word(word)
        base = word.lower()[:-2]
        print(f"  {count:4d}  {word:20s} base=\"{base}\" -> {gloss}")
    
    if te_results['possible_allomorph']:
        print(f"\nPossible allomorph issues ({len(te_results['possible_allomorph'])} cases):")
        seen = set()
        for item in te_results['possible_allomorph'][:15]:
            key = (item['word'], item['truncated_base'])
            if key not in seen:
                seen.add(key)
                print(f"  {item['word']:20s}: analyzed as \"{item['analyzed_base']}-te\"")
                print(f"      but \"{item['truncated_base']}\" ({item['truncated_meaning']}) + \"-{item['extra_chars']}te\" might be wrong")

    # Audit -na (nominalizer)
    print("\n\n## AUDIT: -na (Nominalizer Suffix)")
    print("-" * 50)
    na_results = audit_suffix('na', 'NMLZ')
    
    print(f"\nCorrectly analyzed: {sum(na_results['correct'].values()):,} tokens")
    print(f"Unknown base + -na: {sum(na_results['unknown_base'].values()):,} tokens")
    
    print("\nTop 15 unknown base + -na words:")
    for word, count in na_results['unknown_base'].most_common(15):
        seg, gloss = analyze_word(word)
        base = word.lower()[:-2]
        print(f"  {count:4d}  {word:20s} base=\"{base}\" -> {gloss}")

    # Check phonological conditioning
    print("\n\n## PHONOLOGICAL CONDITIONING CHECK")
    print("-" * 50)
    contexts = check_phonological_conditioning()
    
    print("\nDistribution of segments before -te:")
    total = sum(sum(c.values()) for c in contexts.values())
    for seg in sorted(contexts.keys(), key=lambda x: -sum(contexts[x].values())):
        count = sum(contexts[seg].values())
        pct = 100 * count / total
        print(f"  {seg}: {count:,} ({pct:.1f}%)")

if __name__ == '__main__':
    main()
