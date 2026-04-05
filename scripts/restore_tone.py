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
    
    Disambiguation rules based on Henderson 1965 and ZNC 2018:
    
    1. hi: be.I (H) vs DECL particle (L)
       - Sentence-final → DECL (L)
       - After a- prefix → be.I (H)
       
    2. na: 2SG (L) vs smell.I (H) 
       - Word-initial (prefix) → 2SG (L)
       - After verb → smell (H)
       
    3. thei: know.I (H) vs ABIL suffix (L)
       - After verb stem → ABIL (L)
       - Standalone/initial → know (H)
       
    4. hih: this (H) vs be.II (L)
       - Before noun → this (H)
       - Sentence-final/after verb → be.II (L)
       
    5. pa: father (L) vs NMLZ.AGT (H)
       - After verb → NMLZ.AGT (H)
       - After noun/initial → father (L)
       
    6. Form I vs Form II verbs:
       - Before -in (converb) → Form II (L)
       - Before TAM markers → Form I (H/M)
    """
    if not context:
        context = {}
    
    glosses = [e['gloss'] for e in entries]
    tones = [e['tone'] for e in entries]
    
    # Rule 1: hi - DECL is sentence-final
    if morpheme == 'hi':
        if context.get('position') == 'final':
            return next((e for e in entries if 'DECL' in e['gloss']), entries[0])
        elif context.get('prev_morph') == 'a':
            # a hi = 3SG + be
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
        else:
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    # Rule 2: na - 2SG is prefix/initial
    if morpheme == 'na':
        if context.get('morph_position') == 0:  # First morpheme
            return next((e for e in entries if '2SG' in e['gloss']), entries[0])
        else:
            # After something - likely verb 'smell'
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    # Rule 3: thei - ABIL is suffix
    if morpheme == 'thei':
        if context.get('morph_position', 0) > 0:  # Not first morpheme
            return next((e for e in entries if 'ABIL' in e['gloss']), entries[0])
        else:
            return next((e for e in entries if 'know' in e['gloss'].lower()), entries[0])
    
    # Rule 4: hih - proximal demonstrative vs be.II
    if morpheme == 'hih':
        if context.get('position') == 'final':
            return next((e for e in entries if 'be.II' in e['gloss'] or e['tone'] == 'L'), entries[0])
        elif context.get('next_is_noun'):
            return next((e for e in entries if e['tone'] == 'H'), entries[0])
        else:
            return entries[0]
    
    # Rule 5: pa - after verb = NMLZ.AGT
    if morpheme == 'pa':
        if context.get('prev_is_verb'):
            return next((e for e in entries if 'AGT' in e['gloss'] or 'male' in e['gloss']), entries[0])
        else:
            return next((e for e in entries if 'father' in e['gloss'].lower() or e['tone'] == 'L'), entries[0])
    
    # Rule 6: Form I/II verb detection
    # If morpheme ends in -h and has L tone, likely Form II
    # The preceding morpheme being a verb stem suggests this is Form II
    if morpheme.endswith('h') and any(e['tone'] == 'L' for e in entries):
        if context.get('next_morph') == 'in':  # converb marker
            return next((e for e in entries if e['tone'] == 'L'), entries[0])
    
    # Rule 7: tua - demonstrative 'that' (H tone, very common)
    if morpheme == 'tua':
        return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    # Rule 8: a- prefix is always L (3SG/AGR)
    if morpheme == 'a' and context.get('morph_position') == 0:
        return next((e for e in entries if e['tone'] == 'L'), entries[0])
    
    # Default: prefer most common usage (usually first entry)
    # For verbs, prefer Form I (H/M) over Form II (L) in isolation
    if 'H' in tones:
        return next((e for e in entries if e['tone'] == 'H'), entries[0])
    
    return entries[0]


def disambiguate_tone_with_gloss(morpheme, entries, context):
    """
    Resolve ambiguous tone using analyzer's gloss for high-confidence matches.
    
    Returns: (entry, confidence) where confidence is 'high' if gloss matched,
             'medium' if context-based disambiguation was used.
    """
    analyzer_gloss = context.get('gloss', '')
    
    # First, try to match by gloss - this gives HIGH confidence
    if analyzer_gloss:
        # Normalize for comparison
        gloss_lower = analyzer_gloss.lower()
        
        for entry in entries:
            entry_gloss = entry['gloss'].lower()
            # Check for exact or partial match
            if gloss_lower == entry_gloss or gloss_lower in entry_gloss or entry_gloss in gloss_lower:
                return (entry, 'high')
            
            # Handle Form I/II markers in gloss
            if '.I' in analyzer_gloss or '.II' in analyzer_gloss:
                base_gloss = analyzer_gloss.replace('.I', '').replace('.II', '').lower()
                if base_gloss in entry_gloss:
                    # Match Form based on tone: Form II typically L, Form I typically H/M
                    if '.II' in analyzer_gloss and entry['tone'] == 'L':
                        return (entry, 'high')
                    elif '.I' in analyzer_gloss and entry['tone'] in ('H', 'M'):
                        return (entry, 'high')
        
        # Check for grammatical markers
        gloss_to_tone = {
            'DECL': 'L', 'AGR': 'L', '3SG': 'L', '2SG': 'L', '1SG': 'L',
            'ABIL': 'L', 'IRR': 'L', 'FUT': 'L', 'NEG': 'L',
            'NMLZ': 'H', 'AGT': 'H', 'CAUS': 'L', 'REFL': 'L', 'RECIP': 'L',
        }
        for marker, expected_tone in gloss_to_tone.items():
            if marker in analyzer_gloss:
                match = next((e for e in entries if e['tone'] == expected_tone), None)
                if match:
                    return (match, 'high')
    
    # Fall back to context-based disambiguation - this is MEDIUM confidence
    entry = disambiguate_tone(morpheme, entries, context)
    return (entry, 'medium')


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
            # Ambiguous whole word - try morphological analysis first for gloss info
            result = analyze_word(word_lower)
            if result:
                _, gloss_str = result
                # Use gloss to disambiguate
                whole_context = dict(context or {})
                whole_context['gloss'] = gloss_str
                entry, conf = disambiguate_tone_with_gloss(word_lower, entries, whole_context)
                toned = mark_syllable_tones(word_lower, entry['tone'])
                return (toned, conf, [(word_lower, entry['tone'], entry['gloss'])])
            else:
                # No analysis available - fall back to context-only disambiguation
                entry = disambiguate_tone(word_lower, entries, context)
                toned = mark_syllable_tones(word_lower, entry['tone'])
                return (toned, 'medium', [(word_lower, entry['tone'], entry['gloss'])])
    
    # Try morphological analysis
    result = analyze_word(word_lower)
    if not result:
        return (word, 'unknown', [])
    
    segmentation, gloss_str = result
    morphemes = segmentation.replace('~', '-').split('-')
    glosses = gloss_str.replace('~', '-').split('-')
    
    # Align morphemes with glosses
    if len(glosses) != len(morphemes):
        glosses = [''] * len(morphemes)  # Fallback if misaligned
    
    toned_parts = []
    analysis = []
    overall_confidence = 'high'
    
    for i, morph in enumerate(morphemes):
        morph_lower = morph.lower()
        morph_gloss = glosses[i] if i < len(glosses) else ''
        
        # Build morpheme-level context with gloss info
        morph_context = {
            'morph_position': i,
            'prev_morph': morphemes[i-1].lower() if i > 0 else None,
            'next_morph': morphemes[i+1].lower() if i < len(morphemes) - 1 else None,
            'total_morphemes': len(morphemes),
            'gloss': morph_gloss,  # Pass analyzer's gloss for disambiguation
        }
        # Merge with word-level context
        if context:
            morph_context.update(context)
        
        if morph_lower in tone_dict:
            entries = tone_dict[morph_lower]
            if len(entries) == 1:
                entry = entries[0]
                toned_parts.append(mark_syllable_tones(morph, entry['tone']))
                analysis.append((morph_lower, entry['tone'], entry['gloss']))
            else:
                # Ambiguous - try to disambiguate with context AND gloss
                entry, conf = disambiguate_tone_with_gloss(morph_lower, entries, morph_context)
                toned_parts.append(mark_syllable_tones(morph, entry['tone']))
                if conf == 'high':
                    analysis.append((morph_lower, entry['tone'], entry['gloss']))
                else:
                    analysis.append((morph_lower, entry['tone'] + '?', entry['gloss']))
                    if overall_confidence == 'high':
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
