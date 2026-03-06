#!/usr/bin/env python3
"""
Verse glosser: annotate Kuki-Chin verses with English glosses.

Uses bootstrap lexicons to provide interlinear reading aids.
Includes context disambiguation to select better glosses.
"""

import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class GlossCandidate:
    """A single gloss candidate from the lexicon."""
    eng_gloss: str
    confidence: float
    pmi: float
    pair_count: int
    rank: int


@dataclass 
class GlossEntry:
    """All gloss candidates for a KC word."""
    candidates: List[GlossCandidate] = field(default_factory=list)
    
    @property
    def top(self) -> Optional[GlossCandidate]:
        return self.candidates[0] if self.candidates else None


@dataclass
class GlossedWord:
    """A word with its gloss information."""
    kc_word: str
    gloss: Optional[str]
    confidence: float
    tier: str  # 'high', 'medium', 'low', 'unknown', 'proper'
    context_boosted: bool = False  # Was this gloss selected via context?


def load_lexicon_full(lexicon_path: Path) -> Dict[str, GlossEntry]:
    """Load lexicon with ALL candidates (not just rank 1)."""
    lexicon = defaultdict(lambda: GlossEntry())
    
    with open(lexicon_path, "r", encoding="utf-8") as f:
        header = f.readline()
        
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) >= 7:
                kc_word, kc_freq, eng_gloss, pmi, pair_count, confidence, rank = parts
                
                lexicon[kc_word.lower()].candidates.append(GlossCandidate(
                    eng_gloss=eng_gloss,
                    confidence=float(confidence),
                    pmi=float(pmi),
                    pair_count=int(pair_count),
                    rank=int(rank)
                ))
    
    # Sort candidates by rank
    for entry in lexicon.values():
        entry.candidates.sort(key=lambda c: c.rank)
    
    return dict(lexicon)


def load_lexicon(lexicon_path: Path) -> Dict[str, GlossEntry]:
    """Alias for load_lexicon_full."""
    return load_lexicon_full(lexicon_path)


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
    """Look up each word in lexicon and return glossed words (no context)."""
    glossed = []
    
    for word in words:
        word_lower = word.lower()
        
        if word_lower in lexicon:
            entry = lexicon[word_lower]
            if entry.top:
                tier = get_confidence_tier(entry.top.confidence)
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=entry.top.eng_gloss,
                    confidence=entry.top.confidence,
                    tier=tier
                ))
            else:
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=None,
                    confidence=0.0,
                    tier="unknown"
                ))
        else:
            # Check if it might be a proper noun (starts with capital)
            if word[0].isupper() and len(word) > 1:
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=word,
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


def gloss_words_with_context(
    words: List[str], 
    lexicon: Dict[str, GlossEntry],
    context_window: int = 3
) -> List[GlossedWord]:
    """
    Look up each word with context disambiguation.
    
    For each word, consider glosses of neighboring words and boost
    candidates that semantically relate to the context.
    
    Context heuristic: if a KC neighbor has a high-confidence gloss,
    prefer gloss candidates that share semantic domain (same POS prefix,
    or known collocations).
    """
    glossed = []
    n = len(words)
    
    # First pass: get all candidates for all words
    word_candidates = []
    for word in words:
        word_lower = word.lower()
        if word_lower in lexicon:
            word_candidates.append((word, lexicon[word_lower]))
        elif word[0].isupper() and len(word) > 1:
            # Proper noun
            word_candidates.append((word, None))  # Will be handled specially
        else:
            word_candidates.append((word, None))
    
    # Second pass: select best gloss using context
    for i, (word, entry) in enumerate(word_candidates):
        if entry is None:
            # Proper noun or unknown
            if word[0].isupper() and len(word) > 1:
                glossed.append(GlossedWord(
                    kc_word=word,
                    gloss=word,
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
            continue
        
        if not entry.candidates:
            glossed.append(GlossedWord(
                kc_word=word,
                gloss=None,
                confidence=0.0,
                tier="unknown"
            ))
            continue
        
        # Get context glosses (high-confidence neighbors)
        context_glosses = set()
        for j in range(max(0, i - context_window), min(n, i + context_window + 1)):
            if j == i:
                continue
            neighbor_word, neighbor_entry = word_candidates[j]
            if neighbor_entry and neighbor_entry.top and neighbor_entry.top.confidence >= 0.5:
                context_glosses.add(neighbor_entry.top.eng_gloss)
        
        # Score candidates: boost if they relate to context
        best_candidate = entry.candidates[0]
        best_score = entry.candidates[0].confidence
        context_boosted = False
        
        # Check if any non-top candidate gets boosted by context
        for candidate in entry.candidates[:5]:  # Only check top 5
            score = candidate.confidence
            
            # Context boost: if this gloss shares semantic domain with neighbors
            # Simple heuristic: check if first 3 chars match (e.g., "prophe-" family)
            for ctx_gloss in context_glosses:
                if len(candidate.eng_gloss) >= 3 and len(ctx_gloss) >= 3:
                    if candidate.eng_gloss[:3] == ctx_gloss[:3]:
                        score *= 1.5  # 50% boost for same-prefix words
                    # Also check for known semantic pairs
                    if is_semantic_pair(candidate.eng_gloss, ctx_gloss):
                        score *= 1.3
            
            if score > best_score:
                best_score = score
                best_candidate = candidate
                context_boosted = True
        
        tier = get_confidence_tier(best_candidate.confidence)
        glossed.append(GlossedWord(
            kc_word=word,
            gloss=best_candidate.eng_gloss,
            confidence=best_candidate.confidence,
            tier=tier,
            context_boosted=context_boosted
        ))
    
    return glossed


# Semantic pairs: words that often co-occur
SEMANTIC_PAIRS = {
    # Religious terms
    ("god", "lord"), ("god", "spirit"), ("god", "holy"), ("god", "heaven"),
    ("lord", "servant"), ("lord", "king"), ("lord", "master"),
    ("spirit", "holy"), ("spirit", "soul"), ("spirit", "ghost"),
    ("sin", "forgive"), ("sin", "repent"), ("sin", "iniquity"),
    ("baptiz", "water"), ("baptiz", "wash"), ("baptiz", "spirit"),
    ("prophet", "speak"), ("prophet", "word"), ("prophet", "preach"),
    ("preach", "gospel"), ("preach", "word"), ("preach", "hear"),
    ("pray", "god"), ("pray", "father"), ("pray", "heaven"),
    # Family
    ("son", "father"), ("son", "daughter"), ("son", "mother"),
    ("father", "son"), ("father", "mother"), ("father", "child"),
    ("brother", "sister"), ("brother", "brethren"),
    # Body
    ("hand", "foot"), ("hand", "finger"), ("hand", "arm"),
    ("eye", "see"), ("ear", "hear"), ("mouth", "speak"),
    # Actions
    ("speak", "word"), ("speak", "hear"), ("speak", "voice"),
    ("write", "book"), ("write", "read"), ("write", "letter"),
    # Nature
    ("water", "sea"), ("water", "river"), ("water", "drink"),
    ("fire", "burn"), ("fire", "flame"),
    # Time
    ("day", "night"), ("day", "morning"), ("day", "year"),
    ("year", "day"), ("year", "month"),
    # Places
    ("city", "gate"), ("city", "wall"), ("city", "house"),
    ("temple", "priest"), ("temple", "altar"), ("temple", "sacrifice"),
}


def is_semantic_pair(gloss1: str, gloss2: str) -> bool:
    """Check if two glosses are semantically related."""
    g1 = gloss1.lower().rstrip("?")
    g2 = gloss2.lower().rstrip("?")
    return (g1, g2) in SEMANTIC_PAIRS or (g2, g1) in SEMANTIC_PAIRS


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
    chapter: int,
    use_context: bool = True
) -> Tuple[List[Tuple[str, str, List[GlossedWord]]], dict]:
    """Gloss all verses in a chapter."""
    
    # Build verse ID prefix
    prefix = f"{book:02d}{chapter:03d}"
    
    results = []
    all_glossed = []
    context_boost_count = 0
    
    for verse_id in sorted(bible_verses.keys()):
        if verse_id.startswith(prefix):
            text = bible_verses[verse_id]
            words = tokenize(text)
            
            if use_context:
                glossed = gloss_words_with_context(words, lexicon)
            else:
                glossed = gloss_words(words, lexicon)
            
            results.append((verse_id, text, glossed))
            all_glossed.extend(glossed)
            context_boost_count += sum(1 for gw in glossed if gw.context_boosted)
    
    stats = analyze_coverage(all_glossed)
    stats["context_boosted"] = context_boost_count
    
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
    parser.add_argument("--no-context", action="store_true", help="Disable context disambiguation")
    
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
    
    use_context = not args.no_context
    
    # Process
    if args.chapter:
        # Parse chapter: "41001" -> book 41, chapter 1
        prefix = args.chapter
        book = int(prefix[:2])
        chapter = int(prefix[2:])
        
        results, stats = gloss_chapter(bible_verses, lexicon, book, chapter, use_context=use_context)
        
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
            if use_context:
                print(f"    Context-boosted: {stats.get('context_boosted', 0)}")
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
