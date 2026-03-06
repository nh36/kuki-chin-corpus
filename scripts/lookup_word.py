#!/usr/bin/env python3
"""
Lookup tool for bootstrap lexicons.

Usage:
    python lookup_word.py <language> <word>
    python lookup_word.py ctd tapa
    python lookup_word.py --all water
"""

import argparse
import sys
from pathlib import Path


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


def main():
    parser = argparse.ArgumentParser(description="Look up words in bootstrap lexicons")
    parser.add_argument("language", nargs="?", help="ISO code (e.g., ctd) or --all")
    parser.add_argument("word", nargs="?", help="Word to look up")
    parser.add_argument("--all", action="store_true", help="Search all languages")
    parser.add_argument("--reverse", "-r", action="store_true", 
                        help="Reverse lookup: find KC words for English gloss")
    parser.add_argument("--lexicons-dir", type=Path, default=Path("data/lexicons"),
                        help="Directory containing lexicons")
    
    args = parser.parse_args()
    
    if args.all:
        word = args.language  # word is first positional arg when using --all
        if not word:
            print("Usage: python lookup_word.py --all <word>")
            sys.exit(1)
        
        lexicon_files = sorted(args.lexicons_dir.glob("*_lexicon.tsv"))
        
        for lexicon_path in lexicon_files:
            lang = lexicon_path.stem.replace("_lexicon", "")
            
            if args.reverse:
                results = reverse_lookup(lexicon_path, word)
                if results:
                    print(f"\n=== {lang} ===")
                    for r in results[:10]:
                        print(f"  {r['kc_word']:20} freq={r['kc_freq']:5} conf={r['confidence']:.3f}")
            else:
                results = lookup_word(lexicon_path, word)
                if results:
                    print(f"\n=== {lang} ===")
                    for r in results:
                        print(f"  {r['rank']}. {r['eng_gloss']:15} conf={r['confidence']:.3f} (count={r['pair_count']})")
    else:
        if not args.language or not args.word:
            print("Usage: python lookup_word.py <language> <word>")
            print("       python lookup_word.py --all <word>")
            print("       python lookup_word.py -r <language> <english_word>")
            sys.exit(1)
        
        lexicon_path = args.lexicons_dir / f"{args.language}_lexicon.tsv"
        
        if not lexicon_path.exists():
            print(f"Lexicon not found: {lexicon_path}")
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
