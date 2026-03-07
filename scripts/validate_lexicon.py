#!/usr/bin/env python3
"""
Lexicon Validation and Refinement Tool

Identifies and flags problematic lexical mappings:
1. Function words mis-glossed as content words
2. Polysemous English glosses that may conflate distinct meanings
3. Low-confidence mappings that need review
4. Cross-language validation using cognate patterns

Usage:
    python validate_lexicon.py <iso>           # Validate one language
    python validate_lexicon.py --all           # Validate all languages
    python validate_lexicon.py --fix <iso>     # Generate refined lexicon
"""

import argparse
import os
import sys
from collections import defaultdict
import math
import json

# English words with multiple distinct meanings (homographs/polysemes)
POLYSEMOUS_ENGLISH = {
    # Body part vs. other
    'ear': ['body_part', 'grain'],
    'arm': ['body_part', 'weapon'],
    'palm': ['body_part', 'tree'],
    'tongue': ['body_part', 'language'],
    'mouth': ['body_part', 'opening'],
    'temple': ['building', 'body_part'],
    
    # Multiple distinct senses
    'light': ['illumination', 'weight'],
    'bear': ['animal', 'carry'],
    'fast': ['quick', 'abstain'],
    'rest': ['remainder', 'repose'],
    'lie': ['recline', 'falsehood'],
    'watch': ['timepiece', 'observe'],
    'well': ['water_source', 'healthy'],
    'spring': ['season', 'water_source', 'jump'],
    'kind': ['type', 'gentle'],
    'corn': ['grain_general', 'maize'],
    'mean': ['intend', 'unkind'],
    'left': ['direction', 'departed'],
    'still': ['motionless', 'yet'],
    'even': ['level', 'also'],
    'meet': ['encounter', 'fitting'],
    
    # Biblical terms
    'host': ['army', 'entertainer'],
    'issue': ['offspring', 'matter'],
    'vessel': ['container', 'ship'],
    'compass': ['surround', 'instrument'],
}

# High-frequency English words that should NOT appear as glosses for function words
CONTENT_WORD_GLOSSES = {
    'king', 'lord', 'god', 'man', 'woman', 'son', 'father', 'mother',
    'hand', 'heart', 'eye', 'head', 'spirit', 'mouth', 'foot',
    'house', 'land', 'water', 'fire', 'earth', 'heaven',
}

def load_bible(iso, bibles_dir='bibles/extracted'):
    """Load Bible text for a language."""
    bible = {}
    for suffix in ['', '-x-bible', '-mbs']:
        try:
            path = os.path.join(bibles_dir, iso, f'{iso}{suffix}.txt')
            with open(path) as f:
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        bible[parts[0]] = parts[1]
        except FileNotFoundError:
            continue
    return bible

def load_lexicon(iso, lexicons_dir='data/lexicons'):
    """Load lexicon for a language."""
    lexicon = {}
    path = os.path.join(lexicons_dir, f'{iso}_lexicon.tsv')
    if not os.path.exists(path):
        return lexicon
    
    with open(path) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                kc, kc_freq, eng, pmi, pair_ct, conf, rank = parts[:7]
                lexicon[kc] = {
                    'eng': eng,
                    'freq': int(kc_freq),
                    'pmi': float(pmi),
                    'pair_count': int(pair_ct),
                    'conf': float(conf),
                    'rank': int(rank),
                }
    return lexicon

def compute_verse_coverage(bible):
    """Compute what fraction of verses each word appears in."""
    total_verses = len(bible)
    word_verse_count = defaultdict(int)
    
    for vid, text in bible.items():
        seen = set()
        for tok in text.split():
            tok_lower = tok.lower()
            if tok_lower not in seen:
                word_verse_count[tok_lower] += 1
                seen.add(tok_lower)
    
    coverage = {}
    for word, count in word_verse_count.items():
        coverage[word] = count / total_verses
    return coverage

def validate_lexicon(iso, bibles_dir='bibles/extracted', lexicons_dir='data/lexicons'):
    """
    Validate a lexicon and return issues found.
    """
    issues = {
        'function_word_misgloss': [],  # High-coverage words glossed as content words
        'polysemous_gloss': [],        # Words with ambiguous English glosses
        'low_confidence': [],          # Low confidence entries
        'cross_lang_mismatch': [],     # Cognates with different glosses (future)
    }
    
    bible = load_bible(iso, bibles_dir)
    lexicon = load_lexicon(iso, lexicons_dir)
    
    if not bible or not lexicon:
        return issues
    
    coverage = compute_verse_coverage(bible)
    
    # Check for function words mis-glossed as content words
    for kc_word, data in lexicon.items():
        eng_gloss = data['eng'].rstrip('?').lower()
        word_coverage = coverage.get(kc_word.lower(), 0)
        
        # Flag: high coverage + content word gloss + low confidence
        if word_coverage > 0.30 and eng_gloss in CONTENT_WORD_GLOSSES and data['conf'] < 0.1:
            issues['function_word_misgloss'].append({
                'kc_word': kc_word,
                'gloss': data['eng'],
                'coverage': word_coverage,
                'conf': data['conf'],
                'freq': data['freq'],
            })
        
        # Flag: polysemous English gloss
        if eng_gloss in POLYSEMOUS_ENGLISH:
            issues['polysemous_gloss'].append({
                'kc_word': kc_word,
                'gloss': data['eng'],
                'senses': POLYSEMOUS_ENGLISH[eng_gloss],
                'conf': data['conf'],
                'freq': data['freq'],
            })
        
        # Flag: low confidence content words
        if data['conf'] < 0.1 and data['freq'] >= 50 and eng_gloss in CONTENT_WORD_GLOSSES:
            issues['low_confidence'].append({
                'kc_word': kc_word,
                'gloss': data['eng'],
                'conf': data['conf'],
                'freq': data['freq'],
            })
    
    return issues

def print_validation_report(iso, issues):
    """Print a validation report."""
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT: {iso.upper()}")
    print(f"{'='*60}")
    
    # Function word mis-glosses
    if issues['function_word_misgloss']:
        print(f"\n⚠️  FUNCTION WORDS MIS-GLOSSED AS CONTENT WORDS ({len(issues['function_word_misgloss'])})")
        print(f"   These high-frequency words are likely grammatical particles:\n")
        print(f"   {'KC Word':<15} {'Gloss':<12} {'Verse %':<10} {'Conf':<8}")
        print(f"   {'-'*45}")
        for item in sorted(issues['function_word_misgloss'], key=lambda x: x['coverage'], reverse=True)[:15]:
            print(f"   {item['kc_word']:<15} {item['gloss']:<12} {item['coverage']*100:.1f}%      {item['conf']:.4f}")
    
    # Polysemous glosses
    poly_high_freq = [p for p in issues['polysemous_gloss'] if p['freq'] >= 100]
    if poly_high_freq:
        print(f"\n⚠️  POLYSEMOUS ENGLISH GLOSSES ({len(poly_high_freq)} high-freq)")
        print(f"   These English words have multiple distinct meanings:\n")
        for item in sorted(poly_high_freq, key=lambda x: x['freq'], reverse=True)[:10]:
            senses = ', '.join(item['senses'])
            print(f"   {item['kc_word']:<15} → {item['gloss']:<10} (senses: {senses})")
    
    # Low confidence
    if issues['low_confidence']:
        print(f"\n⚠️  LOW CONFIDENCE MAPPINGS ({len(issues['low_confidence'])})")
        print(f"   These content words have low confidence scores:\n")
        print(f"   {'KC Word':<15} {'Gloss':<12} {'Freq':<8} {'Conf':<8}")
        print(f"   {'-'*43}")
        for item in sorted(issues['low_confidence'], key=lambda x: x['freq'], reverse=True)[:15]:
            print(f"   {item['kc_word']:<15} {item['gloss']:<12} {item['freq']:<8} {item['conf']:.4f}")
    
    # Summary
    total_issues = sum(len(v) for v in issues.values())
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_issues} total issues found")
    print(f"{'='*60}")

def main():
    parser = argparse.ArgumentParser(description='Validate and refine lexicons')
    parser.add_argument('iso', nargs='?', help='Language ISO code')
    parser.add_argument('--all', action='store_true', help='Validate all languages')
    parser.add_argument('--bibles-dir', default='bibles/extracted')
    parser.add_argument('--lexicons-dir', default='data/lexicons')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    if args.all:
        # Get all languages from lexicons
        languages = []
        for fn in os.listdir(args.lexicons_dir):
            if fn.endswith('_lexicon.tsv'):
                languages.append(fn.replace('_lexicon.tsv', ''))
        languages.sort()
    elif args.iso:
        languages = [args.iso]
    else:
        parser.print_help()
        sys.exit(1)
    
    all_issues = {}
    for iso in languages:
        issues = validate_lexicon(iso, args.bibles_dir, args.lexicons_dir)
        all_issues[iso] = issues
        
        if not args.json:
            print_validation_report(iso, issues)
    
    if args.json:
        print(json.dumps(all_issues, indent=2))

if __name__ == '__main__':
    main()
