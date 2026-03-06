#!/usr/bin/env python3
"""
Verse glosser: annotate Kuki-Chin verses with English glosses.

Uses bootstrap lexicons to provide interlinear reading aids.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class GlossEntry:
    """A single gloss entry from the lexicon."""
    eng_gloss: str
    confidence: float
    pmi: float
    pair_count: int


@dataclass
class GlossedWord:
    """A word with its gloss information."""
    kc_word: str
    gloss: Optional[str]
    confidence: float
    tier: str  # 'high', 'medium', 'low', 'unknown'


def load_lexicon(lexicon_path: Path) -> Dict[str, GlossEntry]:
    """Load lexicon as dict mapping KC word -> top gloss entry."""
    lexicon = {}
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        header = f.readline()
        
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                kc_word, kc_freq, eng_gloss, pmi, pair_count, confidence, rank = parts
                
                # Only keep rank 1 (best gloss)
                if rank == "1":
                    lexicon[kc_word.lower()] = GlossEntry(
                        eng_gloss=eng_gloss,
                        confidence=float(confidence),
                        pmi=float(pmi),
                        pair_count=int(pair_count)
                    )
    
    return lexicon


def tokenize(text: str) -> List[str]:
    """Tokenize text into words, preserving order."""
    # Match word characters including extended Latin and special chars
    words = re.findall(r"[A-Za-z\u00C0-\u024F\u1E00-\u1EFF'']+", text)
    return words


def get_confidence_tier(confidence: float) -> str:
    """Classify confidence into tiers."""
    if confidence >= 0.7:
        return "high"
    elif confidence >= 0.4:
        return "medium"
    elif confidence > 0:
        return "low"
    else:
        return "unknown"


def gloss_words(words: List[str], lexicon: Dict[str, GlossEntry]) -> List[GlossedWord]:
    """Look up each word in lexicon and return glossed words."""
    glossed = []
    
    for word in words:
        word_lower = word.lower()
        
        if word_lower in lexicon:
            entry = lexicon[word_lower]
            tier = get_confidence_tier(entry.confidence)
            glossed.append(GlossedWord(
                kc_word=word,
                gloss=entry.eng_gloss,
                confidence=entry.confidence,
                tier=tier
            ))
        else:
            # Check if it might be a proper noun (starts with capital)
            if word[0].isupper() and len(word) > 1:
                # Keep proper nouns as-is
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=word,  # Keep the original
                    confidence=1.0,
                    tier="proper"
                ))
            else:
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=None,
                    confidence=0.0,
                    tier="unknown"
                ))
    
    return glossed


def format_interlinear(glossed_words: List[GlossedWord], show_confidence: bool = False) -> str:
    """Format glossed words as interlinear text."""
    kc_line = []
    gl_line = []
    
    for gw in glossed_words:
        # Determine display width
        kc_width = len(gw.kc_word)
        
        if gw.gloss:
            if gw.tier == "medium":
                gloss_display = f"{gw.gloss}?"
            elif gw.tier == "low":
                gloss_display = f"({gw.gloss})"
            else:
                gloss_display = gw.gloss
        else:
            gloss_display = "???"
        
        gl_width = len(gloss_display)
        width = max(kc_width, gl_width)
        
        kc_line.append(gw.kc_word.ljust(width))
        gl_line.append(gloss_display.ljust(width))
    
    return "  ".join(kc_line) + "\n" + "  ".join(gl_line)


def format_tsv(verse_id: str, glossed_words: List[GlossedWord]) -> str:
    """Format as TSV with metadata."""
    lines = []
    for i, gw in enumerate(glossed_words):
        gloss = gw.gloss if gw.gloss else ""
        lines.append(f"{verse_id}\t{i}\t{gw.kc_word}\t{gloss}\t{gw.confidence:.3f}\t{gw.tier}")
    return "\n".join(lines)


def load_bible(bible_dir: Path) -> Dict[str, str]:
    """Load Bible verses as dict of verse_id -> text."""
    verses = {}
    
    txt_files = list(bible_dir.glob("*-x-bible.txt"))
    if not txt_files:
        return verses
    
    with open(txt_files[0], "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t", 1)
            if len(parts) == 2:
                verses[parts[0]] = parts[1]
    
    return verses


def analyze_coverage(glossed_words: List[GlossedWord]) -> dict:
    """Analyze glossing coverage statistics."""
    total = len(glossed_words)
    if total == 0:
        return {"total": 0, "glossed": 0, "coverage": 0}
    
    tiers = defaultdict(int)
    for gw in glossed_words:
        tiers[gw.tier] += 1
    
    glossed = total - tiers["unknown"]
    
    return {
        "total": total,
        "glossed": glossed,
        "coverage": glossed / total if total > 0 else 0,
        "high": tiers["high"],
        "medium": tiers["medium"],
        "low": tiers["low"],
        "proper": tiers["proper"],
        "unknown": tiers["unknown"]
    }


def gloss_chapter(
    bible_verses: Dict[str, str],
    lexicon: Dict[str, GlossEntry],
    book: int,
    chapter: int
) -> Tuple[List[Tuple[str, str, List[GlossedWord]]], dict]:
    """Gloss all verses in a chapter."""
    
    # Build verse ID prefix
    prefix = f"{book:02d}{chapter:03d}"
    
    results = []
    all_glossed = []
    
    for verse_id in sorted(bible_verses.keys()):
        if verse_id.startswith(prefix):
            text = bible_verses[verse_id]
            words = tokenize(text)
            glossed = gloss_words(words, lexicon)
            results.append((verse_id, text, glossed))
            all_glossed.extend(glossed)
    
    stats = analyze_coverage(all_glossed)
    
    return results, stats


def main():
    parser = argparse.ArgumentParser(description="Gloss Kuki-Chin verses with English")
    parser.add_argument("iso", help="ISO code for the language")
    parser.add_argument("verse_id", nargs="?", help="Verse ID (e.g., 41001001) or 'chapter:41001'")
    parser.add_argument("--bibles-dir", type=Path, default=Path("bibles/extracted"))
    parser.add_argument("--lexicons-dir", type=Path, default=Path("data/lexicons"))
    parser.add_argument("--format", choices=["interlinear", "tsv", "plain"], default="interlinear")
    parser.add_argument("--chapter", help="Chapter prefix (e.g., 41001 for Mark 1)")
    parser.add_argument("--stats-only", action="store_true", help="Only show statistics")
    
    args = parser.parse_args()
    
    # Load lexicon
    lexicon_path = args.lexicons_dir / f"{args.iso}_lexicon.tsv"
    if not lexicon_path.exists():
        print(f"Lexicon not found: {lexicon_path}")
        return
    
    lexicon = load_lexicon(lexicon_path)
    print(f"Loaded lexicon: {len(lexicon)} entries")
    
    # Load Bible
    bible_dir = args.bibles_dir / args.iso
    if not bible_dir.exists():
        print(f"Bible not found: {bible_dir}")
        return
    
    bible_verses = load_bible(bible_dir)
    print(f"Loaded Bible: {len(bible_verses)} verses")
    print()
    
    # Process
    if args.chapter:
        # Parse chapter: "41001" -> book 41, chapter 1
        prefix = args.chapter
        book = int(prefix[:2])
        chapter = int(prefix[2:])
        
        results, stats = gloss_chapter(bible_verses, lexicon, book, chapter)
        
        if args.stats_only:
            print(f"Chapter {book}:{chapter}")
            print(f"  Verses: {len(results)}")
            print(f"  Tokens: {stats['total']}")
            print(f"  Glossed: {stats['glossed']} ({stats['coverage']*100:.1f}%)")
            print(f"    High confidence: {stats['high']}")
            print(f"    Medium: {stats['medium']}")
            print(f"    Low: {stats['low']}")
            print(f"    Proper nouns: {stats['proper']}")
            print(f"    Unknown: {stats['unknown']}")
        else:
            for verse_id, text, glossed in results:
                verse_num = int(verse_id[-3:])
                print(f"--- {book}:{chapter}:{verse_num} ---")
                if args.format == "interlinear":
                    print(format_interlinear(glossed))
                elif args.format == "tsv":
                    print(format_tsv(verse_id, glossed))
                else:
                    print(text)
                    print(" | ".join(gw.gloss or "???" for gw in glossed))
                print()
    
    elif args.verse_id:
        if args.verse_id not in bible_verses:
            print(f"Verse not found: {args.verse_id}")
            return
        
        text = bible_verses[args.verse_id]
        words = tokenize(text)
        glossed = gloss_words(words, lexicon)
        
        print(f"Verse: {args.verse_id}")
        print(f"Text: {text}")
        print()
        
        if args.format == "interlinear":
            print(format_interlinear(glossed))
        elif args.format == "tsv":
            print(format_tsv(args.verse_id, glossed))
        else:
            print(" | ".join(gw.gloss or "???" for gw in glossed))
        
        print()
        stats = analyze_coverage(glossed)
        print(f"Coverage: {stats['glossed']}/{stats['total']} ({stats['coverage']*100:.1f}%)")
    
    else:
        print("Specify --chapter or verse_id")


if __name__ == "__main__":
    main()
