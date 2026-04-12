#!/usr/bin/env python3
"""
Lookup tool for Kuki-Chin dictionaries.

Now supports both:
1. SQLite backend (for languages with full analysis, e.g., Tedim Chin)
2. Bootstrap lexicons (for languages in initial development)

Usage:
    python lookup_word.py <language> <word>
    python lookup_word.py ctd tapa         # Uses backend if available
    python lookup_word.py lus thil          # Falls back to lexicon
    python lookup_word.py --all water       # Search all languages
    python lookup_word.py -r ctd go         # Reverse lookup (English→KC)
"""

import argparse
import os
import sys
from pathlib import Path

# Add scripts directory to path for backend import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# =============================================================================
# Backend Lookup (SQLite)
# =============================================================================

def backend_lookup(db_path: Path, word: str, reverse: bool = False) -> list:
    """Look up a word using the SQLite backend."""
    from backend import Backend
    
    if not db_path.exists():
        return []
    
    db = Backend(str(db_path))
    results = []
    
    if reverse:
        # Search by English gloss
        lemmas = db.search_lemmas(word, limit=20)
        for lemma in lemmas:
            # Check if gloss actually matches
            if word.lower() in lemma.primary_gloss.lower():
                results.append({
                    'type': 'backend',
                    'kc_word': lemma.citation_form,
                    'kc_freq': lemma.token_count,
                    'eng_gloss': lemma.primary_gloss,
                    'pos': lemma.pos,
                    'entry_type': lemma.entry_type,
                    'is_polysemous': lemma.is_polysemous,
                })
    else:
        # Direct lookup
        lemma = db.get_lemma(word.lower())
        if lemma:
            senses = db.get_senses(lemma.lemma_id)
            examples = db.get_examples_for_lemma(lemma.lemma_id, limit=3)
            
            results.append({
                'type': 'backend',
                'kc_word': lemma.citation_form,
                'kc_freq': lemma.token_count,
                'eng_gloss': lemma.primary_gloss,
                'pos': lemma.pos,
                'entry_type': lemma.entry_type,
                'is_polysemous': lemma.is_polysemous,
                'senses': senses,
                'examples': examples,
            })
        else:
            # Try fuzzy search
            matches = db.search_lemmas(word, limit=5)
            for m in matches:
                results.append({
                    'type': 'backend',
                    'kc_word': m.citation_form,
                    'kc_freq': m.token_count,
                    'eng_gloss': m.primary_gloss,
                    'pos': m.pos,
                    'entry_type': m.entry_type,
                    'is_polysemous': m.is_polysemous,
                    'is_fuzzy': True,
                })
    
    return results


def format_backend_result(r: dict, verbose: bool = True) -> list:
    """Format a backend lookup result for display."""
    lines = []
    
    fuzzy_marker = ' (similar)' if r.get('is_fuzzy') else ''
    poly_marker = ' [polysemous]' if r.get('is_polysemous') else ''
    
    lines.append(f"\n{r['kc_word']} ({r['pos']}) - {r['eng_gloss']}{fuzzy_marker}{poly_marker}")
    lines.append(f"  Type: {r['entry_type']}, Freq: {r['kc_freq']:,}")
    
    if verbose and 'senses' in r and r['senses']:
        lines.append(f"\n  Senses ({len(r['senses'])}):")
        for s in r['senses'][:5]:
            primary = '*' if s.is_primary else ' '
            lines.append(f"    {primary}{s.sense_num}. {s.gloss} ({s.usage_type}, n={s.frequency:,})")
    
    if verbose and 'examples' in r and r['examples']:
        lines.append(f"\n  Examples:")
        for e in r['examples'][:2]:
            lines.append(f"    {e.source_id}: {e.tedim_text[:60]}...")
            if e.kjv_text:
                lines.append(f"      KJV: {e.kjv_text[:60]}...")
    
    return lines


# =============================================================================
# Lexicon Lookup (TSV)
# =============================================================================

def lookup_word(lexicon_path: Path, word: str) -> list:
    """Look up a word in a lexicon file."""
    results = []
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        header = f.readline()  # skip header
        
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                kc_word, kc_freq, eng_gloss, pmi, pair_count, confidence, rank = parts
                
                if kc_word.lower() == word.lower():
                    results.append({
                        "type": "lexicon",
                        "kc_word": kc_word,
                        "kc_freq": int(kc_freq),
                        "eng_gloss": eng_gloss,
                        "pmi": float(pmi),
                        "pair_count": int(pair_count),
                        "confidence": float(confidence),
                        "rank": int(rank)
                    })
    
    return results


def reverse_lookup(lexicon_path: Path, eng_word: str) -> list:
    """Look up English word to find KC equivalents."""
    results = []
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        header = f.readline()
        
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                kc_word, kc_freq, eng_gloss, pmi, pair_count, confidence, rank = parts
                
                if eng_gloss.lower() == eng_word.lower() and rank == "1":  # Only top candidate
                    results.append({
                        "type": "lexicon",
                        "kc_word": kc_word,
                        "kc_freq": int(kc_freq),
                        "eng_gloss": eng_gloss,
                        "pmi": float(pmi),
                        "pair_count": int(pair_count),
                        "confidence": float(confidence)
                    })
    
    # Sort by confidence
    results.sort(key=lambda x: -x["confidence"])
    return results


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Look up words in Kuki-Chin dictionaries")
    parser.add_argument("language", nargs="?", help="ISO code (e.g., ctd) or --all")
    parser.add_argument("word", nargs="?", help="Word to look up")
    parser.add_argument("--all", action="store_true", help="Search all languages")
    parser.add_argument("--reverse", "-r", action="store_true", 
                        help="Reverse lookup: find KC words for English gloss")
    parser.add_argument("--lexicons-dir", type=Path, default=Path("data/lexicons"),
                        help="Directory containing lexicons")
    parser.add_argument("--backends-dir", type=Path, default=Path("data"),
                        help="Directory containing SQLite backends")
    parser.add_argument("--brief", "-b", action="store_true",
                        help="Brief output (no examples)")
    
    args = parser.parse_args()
    
    if args.all:
        word = args.language  # word is first positional arg when using --all
        if not word:
            print("Usage: python lookup_word.py --all <word>")
            sys.exit(1)
        
        # Search backends first
        backend_files = sorted(args.backends_dir.glob("*_backend.db"))
        for backend_path in backend_files:
            lang = backend_path.stem.replace("_backend", "")
            results = backend_lookup(backend_path, word, args.reverse)
            if results:
                print(f"\n=== {lang} (backend) ===")
                for r in results[:5]:
                    if r.get('is_fuzzy'):
                        continue
                    print(f"  {r['kc_word']:20} {r['eng_gloss']:20} freq={r['kc_freq']:5}")
        
        # Then search lexicons
        lexicon_files = sorted(args.lexicons_dir.glob("*_lexicon.tsv"))
        for lexicon_path in lexicon_files:
            lang = lexicon_path.stem.replace("_lexicon", "")
            # Skip if backend exists
            if (args.backends_dir / f"{lang}_backend.db").exists():
                continue
            
            if args.reverse:
                results = reverse_lookup(lexicon_path, word)
                if results:
                    print(f"\n=== {lang} (lexicon) ===")
                    for r in results[:10]:
                        print(f"  {r['kc_word']:20} freq={r['kc_freq']:5} conf={r['confidence']:.3f}")
            else:
                results = lookup_word(lexicon_path, word)
                if results:
                    print(f"\n=== {lang} (lexicon) ===")
                    for r in results:
                        print(f"  {r['rank']}. {r['eng_gloss']:15} conf={r['confidence']:.3f} (count={r['pair_count']})")
    else:
        if not args.language or not args.word:
            print("Usage: python lookup_word.py <language> <word>")
            print("       python lookup_word.py --all <word>")
            print("       python lookup_word.py -r <language> <english_word>")
            sys.exit(1)
        
        # Try backend first
        backend_path = args.backends_dir / f"{args.language}_backend.db"
        if backend_path.exists():
            results = backend_lookup(backend_path, args.word, args.reverse)
            if results:
                print(f"\n{args.language} (from backend):")
                for r in results:
                    for line in format_backend_result(r, verbose=not args.brief):
                        print(line)
                return
            else:
                print(f"No entry found for '{args.word}' in {args.language} backend")
                return
        
        # Fall back to lexicon
        lexicon_path = args.lexicons_dir / f"{args.language}_lexicon.tsv"
        
        if not lexicon_path.exists():
            print(f"No backend or lexicon found for {args.language}")
            sys.exit(1)
        
        if args.reverse:
            results = reverse_lookup(lexicon_path, args.word)
            if results:
                print(f"English '{args.word}' in {args.language}:")
                for r in results[:20]:
                    print(f"  {r['kc_word']:20} freq={r['kc_freq']:5} conf={r['confidence']:.3f}")
            else:
                print(f"No entries found for '{args.word}'")
        else:
            results = lookup_word(lexicon_path, args.word)
            if results:
                print(f"{args.language} '{args.word}' (freq={results[0]['kc_freq']}):")
                for r in results:
                    print(f"  {r['rank']}. {r['eng_gloss']:15} conf={r['confidence']:.3f} PMI={r['pmi']:.2f} (count={r['pair_count']})")
            else:
                print(f"No entry found for '{args.word}'")


if __name__ == "__main__":
    main()
