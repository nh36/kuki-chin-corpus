#!/usr/bin/env python3
"""
Tone restoration tool for Tedim Chin Bible text.

Takes Bible text (without tone marking) and adds tone diacritics
where the tone is known with confidence.

Strategy:
1. Morphologically analyze each word
2. Look up each morpheme in tone dictionary
3. If tone is unambiguous, mark it
4. If ambiguous but contextually resolvable, apply disambiguation rules
5. If unknown, leave unmarked

Output formats:
- Toned orthography: uses combining diacritics (á=H, ā=M, à=L)
- IPA tier: phonemic transcription with tone numbers
- Confidence annotation: marks uncertain forms with ?
"""

import sys
import re
from pathlib import Path
from collections import defaultdict

# Add scripts to path for analyzer import
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import analyze_word

# Tone diacritics (combining characters)
TONE_MARK = {
    'H': '\u0301',  # combining acute accent (high/rising)
    'M': '\u0304',  # combining macron (mid/level)
    'L': '\u0300',  # combining grave accent (low/falling)
}

def load_tone_dictionary(path='data/tone_dictionary.tsv'):
    """Load tone dictionary from TSV file."""
    tone_dict = {}
    
    with open(path, 'r', encoding='utf-8') as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 6:
                orth = parts[0].lower()
                tone_pattern = parts[3]
                gloss = parts[4]
                source = parts[5]
                confidence = parts[6] if len(parts) > 6 else 'high'
                
                if orth not in tone_dict:
                    tone_dict[orth] = []
                tone_dict[orth].append({
                    'tone': tone_pattern,
                    'gloss': gloss,
                    'source': source,
                    'confidence': confidence
                })
    
    return tone_dict

def add_tone_diacritics(syllable, tone):
    """Add tone diacritic to a syllable.
    
    The diacritic goes on the nucleus (main vowel).
    For diphthongs, mark the first vowel.
    """
    if tone not in TONE_MARK:
        return syllable
    
    diacritic = TONE_MARK[tone]
    vowels = 'aeiouɔ'
    
    # Find first vowel and add diacritic after it
    for i, char in enumerate(syllable):
        if char.lower() in vowels:
            return syllable[:i+1] + diacritic + syllable[i+1:]
    
    # No vowel found - just return unchanged
    return syllable

def mark_syllable_tones(morpheme, tone_pattern):
    """Mark tones on a multi-syllable morpheme.
    
    E.g., morpheme='amah', tone_pattern='LL' -> 'àmàh'
    """
    # Simple case: single tone
    if len(tone_pattern) == 1:
        return add_tone_diacritics(morpheme, tone_pattern)
    
    # Multi-syllable: split into syllables and apply
    # Tedim Chin syllable structure is (C)V(C)
    # Heuristic: each vowel sequence is a syllable nucleus
    
    syllables = []
    current = ''
    vowels = 'aeiouɔ'
    vowel_count = 0
    
    for char in morpheme:
        current += char
        if char.lower() in vowels:
            vowel_count += 1
    
    # If syllable count matches tone pattern, we can mark directly
    if vowel_count == len(tone_pattern):
        result = ''
        tone_idx = 0
        for char in morpheme:
            result += char
            if char.lower() in vowels and tone_idx < len(tone_pattern):
                result += TONE_MARK.get(tone_pattern[tone_idx], '')
                tone_idx += 1
        return result
    
    # Otherwise, apply first tone to the whole morpheme
    return add_tone_diacritics(morpheme, tone_pattern[0])

def disambiguate_tone(morpheme, entries, context=None):
    """
    Resolve ambiguous tone entries using context.
    
    Rules:
    1. hi: 'be' (H) vs 'DECL' (L) - DECL is sentence-final
    2. na: '2SG' (L) vs 'smell' (H) - 2SG is prefix position
    3. thei: 'know' (H) vs 'ABIL' (L) - ABIL follows verb
    """
    glosses = [e['gloss'] for e in entries]
    
    # Rule 1: hi - if context suggests verb, use H; if sentence-final, use L
    if morpheme == 'hi' and context:
        if context.get('position') == 'final':
            return next((e for e in entries if 'DECL' in e['gloss']), entries[0])
        else:
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    # Rule 2: na - prefix position suggests 2SG (L)
    if morpheme == 'na' and context:
        if context.get('position') == 'prefix':
            return next((e for e in entries if '2SG' in e['gloss']), entries[0])
    
    # Rule 3: thei - after verb stem suggests ABIL (L)
    if morpheme == 'thei' and context:
        if context.get('position') == 'suffix':
            return next((e for e in entries if 'ABIL' in e['gloss']), entries[0])
        else:
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    # Default: return first entry (usually most common)
    return entries[0]

def restore_word_tone(word, tone_dict, context=None):
    """
    Restore tone for a single word.
    
    Returns tuple: (toned_word, confidence, analysis)
    - toned_word: word with tone diacritics
    - confidence: 'high', 'medium', 'low', or 'unknown'
    - analysis: list of (morpheme, tone, gloss) tuples
    """
    # First, try the whole word
    word_lower = word.lower().strip('.,;:!?"\'')
    
    if word_lower in tone_dict:
        entries = tone_dict[word_lower]
        if len(entries) == 1:
            entry = entries[0]
            toned = mark_syllable_tones(word_lower, entry['tone'])
            return (toned, 'high', [(word_lower, entry['tone'], entry['gloss'])])
        else:
            # Ambiguous - try to disambiguate
            entry = disambiguate_tone(word_lower, entries, context)
            toned = mark_syllable_tones(word_lower, entry['tone'])
            return (toned, 'medium', [(word_lower, entry['tone'], entry['gloss'])])
    
    # Try morphological analysis
    result = analyze_word(word_lower)
    if not result:
        return (word, 'unknown', [])
    
    segmentation, gloss = result
    morphemes = segmentation.replace('~', '-').split('-')
    
    toned_parts = []
    analysis = []
    overall_confidence = 'high'
    
    for morph in morphemes:
        morph_lower = morph.lower()
        if morph_lower in tone_dict:
            entries = tone_dict[morph_lower]
            if len(entries) == 1:
                entry = entries[0]
                toned_parts.append(mark_syllable_tones(morph, entry['tone']))
                analysis.append((morph_lower, entry['tone'], entry['gloss']))
            else:
                # Ambiguous
                entry = disambiguate_tone(morph_lower, entries)
                toned_parts.append(mark_syllable_tones(morph, entry['tone']))
                analysis.append((morph_lower, entry['tone'] + '?', entry['gloss']))
                overall_confidence = 'medium'
        else:
            # Unknown tone
            toned_parts.append(morph)
            analysis.append((morph_lower, '?', ''))
            overall_confidence = 'low' if overall_confidence != 'unknown' else overall_confidence
    
    return ('-'.join(toned_parts), overall_confidence, analysis)

def restore_verse_tone(verse_text, tone_dict):
    """
    Restore tones for an entire verse.
    
    Returns: (toned_text, stats)
    """
    words = verse_text.split()
    toned_words = []
    stats = {'high': 0, 'medium': 0, 'low': 0, 'unknown': 0}
    
    for i, word in enumerate(words):
        # Build context
        context = {
            'position': 'final' if i == len(words) - 1 else 'medial',
            'prev_word': words[i-1] if i > 0 else None,
            'next_word': words[i+1] if i < len(words) - 1 else None,
        }
        
        toned, confidence, analysis = restore_word_tone(word, tone_dict, context)
        toned_words.append(toned)
        stats[confidence] += 1
    
    return (' '.join(toned_words), stats)

def format_interlinear(verse_ref, original, toned, gloss):
    """Format verse as interlinear gloss with multiple tiers."""
    return f"""{verse_ref}
  Original: {original}
  Toned:    {toned}
  Gloss:    {gloss}
"""

def main():
    """Demo: restore tones on sample verses."""
    print("Tedim Chin Tone Restoration Tool")
    print("=" * 50)
    
    # Load dictionary
    tone_dict = load_tone_dictionary()
    print(f"Loaded {len(tone_dict)} entries from tone dictionary\n")
    
    # Sample verses from Genesis 1:1-3
    sample_verses = [
        ("Gen.1.1", "A masapen in Pasian in van le lei a bawl hi"),
        ("Gen.1.2", "Lei in a lim a piangsak lo a nuntakna om nai lo hi"),
        ("Gen.1.3", "Pasian in Khua a vak hen ci hi Khua a vak hi"),
        ("Jhn.3.16", "Pasian in leitung a it lua ahih manin a Tapa khatbek pia hi"),
    ]
    
    total_stats = {'high': 0, 'medium': 0, 'low': 0, 'unknown': 0}
    
    for ref, verse in sample_verses:
        toned, stats = restore_verse_tone(verse, tone_dict)
        
        print(f"\n{ref}")
        print(f"  Original: {verse}")
        print(f"  Toned:    {toned}")
        print(f"  Stats:    H:{stats['high']} M:{stats['medium']} L:{stats['low']} ?:{stats['unknown']}")
        
        for k in total_stats:
            total_stats[k] += stats[k]
    
    # Summary
    total_words = sum(total_stats.values())
    print("\n" + "=" * 50)
    print("Summary:")
    print(f"  Total words: {total_words}")
    print(f"  High confidence: {total_stats['high']} ({100*total_stats['high']/total_words:.1f}%)")
    print(f"  Medium confidence: {total_stats['medium']} ({100*total_stats['medium']/total_words:.1f}%)")
    print(f"  Low confidence: {total_stats['low']} ({100*total_stats['low']/total_words:.1f}%)")
    print(f"  Unknown: {total_stats['unknown']} ({100*total_stats['unknown']/total_words:.1f}%)")

if __name__ == '__main__':
    main()
