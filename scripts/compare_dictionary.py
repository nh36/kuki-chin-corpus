#!/usr/bin/env python3
"""
Compare Tedim-English dictionary entries with analyzer glosses.

Identifies:
1. Words where dictionary shows multiple meanings but analyzer has one
2. Words where analyzer gloss doesn't match any dictionary meaning
3. Potential disambiguation opportunities

Usage: python3 scripts/compare_dictionary.py
"""

import re
import sys
sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

def parse_dictionary():
    """Parse tedim_dictionary.txt into word->meanings mapping."""
    dictionary = {}
    
    with open('data/tedim_dictionary.txt', 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Pattern for dictionary entries: word, part of speech. definition
    # Examples:
    #   aai, (sa' aai), v. to celebrate...
    #   aalu, n. potato, murphy, spud,
    #   kei, adv. not in no manner
    #   kei, pro. I, myself
    
    # Simple pattern to capture headwords
    pattern = r'^([a-z][a-z\-\']+),\s*(?:\([^)]*\),\s*)?(n\.|v\.|adj\.|adv\.|pro\.|prep\.|conj\.|int\.)\s*(.+?)(?=\n[a-z]|\Z)'
    
    for match in re.finditer(pattern, text, re.MULTILINE | re.DOTALL):
        word = match.group(1).lower().strip()
        pos = match.group(2).strip()
        definition = match.group(3).strip()
        # Clean up definition
        definition = re.sub(r'\s+', ' ', definition)
        definition = definition[:100]  # Truncate
        
        if word not in dictionary:
            dictionary[word] = []
        dictionary[word].append({'pos': pos, 'def': definition})
    
    return dictionary

def get_bible_vocabulary():
    """Get vocabulary from Bible text."""
    vocab = {}
    with open('bibles/extracted/ctd/ctd-x-bible.txt', 'r') as f:
        for line in f:
            if '\t' not in line:
                continue
            parts = line.split('\t')
            if len(parts) < 2:
                continue
            verse_text = parts[1]
            for word in verse_text.split():
                word_clean = re.sub(r'[.,;:!?\"\'\(\)]+', '', word.lower())
                if word_clean and len(word_clean) > 1:
                    vocab[word_clean] = vocab.get(word_clean, 0) + 1
    return vocab

def main():
    print("Parsing dictionary...")
    dictionary = parse_dictionary()
    print(f"Found {len(dictionary)} dictionary entries")
    
    print("\nGetting Bible vocabulary...")
    bible_vocab = get_bible_vocabulary()
    print(f"Found {len(bible_vocab)} unique word forms in Bible")
    
    # Find words with multiple dictionary meanings
    print("\n" + "="*70)
    print("WORDS WITH MULTIPLE DICTIONARY MEANINGS (potential disambiguation)")
    print("="*70)
    
    multi_meaning = []
    for word, meanings in dictionary.items():
        if len(meanings) > 1 and word in bible_vocab:
            multi_meaning.append((word, bible_vocab[word], meanings))
    
    # Sort by frequency
    multi_meaning.sort(key=lambda x: -x[1])
    
    print(f"\nFound {len(multi_meaning)} Bible words with multiple dictionary meanings:\n")
    
    for word, freq, meanings in multi_meaning[:50]:  # Top 50
        seg, gloss = analyze_word(word)
        print(f"\n{word} ({freq}x) → analyzer: {gloss}")
        for m in meanings:
            print(f"  • {m['pos']} {m['def']}")
        
    # Find analyzer glosses that don't match dictionary
    print("\n" + "="*70)
    print("HIGH-FREQUENCY WORDS: Analyzer vs Dictionary")
    print("="*70)
    
    comparisons = []
    for word in sorted(bible_vocab.keys(), key=lambda w: -bible_vocab[w])[:200]:
        if word in dictionary:
            seg, gloss = analyze_word(word)
            meanings = dictionary[word]
            comparisons.append((word, bible_vocab[word], gloss, meanings))
    
    print(f"\nChecking top 200 frequent words that have dictionary entries:\n")
    for word, freq, gloss, meanings in comparisons[:30]:
        meanings_str = "; ".join(f"{m['pos']} {m['def'][:50]}" for m in meanings)
        print(f"{word} ({freq}x)")
        print(f"  Analyzer: {gloss}")
        print(f"  Dict: {meanings_str}\n")

if __name__ == "__main__":
    main()
