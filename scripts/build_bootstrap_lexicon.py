#!/usr/bin/env python3
"""
Build bootstrap lexicons via co-occurrence statistics.

For each Kuki-Chin language, pairs words with English (KJV) equivalents
based on recurrent co-occurrence across aligned Bible verses.

Method:
1. For each verse pair (English, Kuki-Chin), treat as bag of words
2. Take cross-product of all word pairs
3. Track co-occurrence counts across entire corpus
4. Rank pairs by frequency and stability metrics

Output: TSV lexicon with KC_word → English candidates ranked by score
"""

import argparse
import re
import math
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Set
import json

# Simple English lemmatization rules
# We'll use a basic approach - could enhance with NLTK/spaCy later
ENGLISH_IRREGULAR = {
    # Be
    "am": "be", "is": "be", "are": "be", "was": "be", "were": "be", "been": "be", "being": "be",
    # Have
    "has": "have", "had": "have", "having": "have",
    # Do
    "does": "do", "did": "do", "doing": "do", "done": "do",
    # Say
    "says": "say", "said": "say", "saying": "say",
    # Go
    "goes": "go", "went": "go", "gone": "go", "going": "go",
    # Get
    "gets": "get", "got": "get", "gotten": "get", "getting": "get",
    # Make
    "makes": "make", "made": "make", "making": "make",
    # Come
    "comes": "come", "came": "come", "coming": "come",
    # Know
    "knows": "know", "knew": "know", "known": "know", "knowing": "know",
    # Take
    "takes": "take", "took": "take", "taken": "take", "taking": "take",
    # See
    "sees": "see", "saw": "see", "seen": "see", "seeing": "see",
    # Give
    "gives": "give", "gave": "give", "given": "give", "giving": "give",
    # Find
    "finds": "find", "found": "find", "finding": "find",
    # Think
    "thinks": "think", "thought": "think", "thinking": "think",
    # Tell
    "tells": "tell", "told": "tell", "telling": "tell",
    # Become
    "becomes": "become", "became": "become", "becoming": "become",
    # Leave
    "leaves": "leave", "left": "leave", "leaving": "leave",
    # Put
    "puts": "put", "putting": "put",
    # Bring
    "brings": "bring", "brought": "bring", "bringing": "bring",
    # Begin
    "begins": "begin", "began": "begin", "begun": "begin", "beginning": "begin",
    # Write
    "writes": "write", "wrote": "write", "written": "write", "writing": "write",
    # Speak
    "speaks": "speak", "spoke": "speak", "spoken": "speak", "speaking": "speak",
    # Hear
    "hears": "hear", "heard": "hear", "hearing": "hear",
    # Send
    "sends": "send", "sent": "send", "sending": "send",
    # Sit
    "sits": "sit", "sat": "sit", "sitting": "sit",
    # Stand
    "stands": "stand", "stood": "stand", "standing": "stand",
    # Eat
    "eats": "eat", "ate": "eat", "eaten": "eat", "eating": "eat",
    # Drink
    "drinks": "drink", "drank": "drink", "drunk": "drink", "drinking": "drink",
    # Pronouns (keep as-is but normalize case)
    "i": "I", "me": "I", "my": "I", "mine": "I", "myself": "I",
    "he": "he", "him": "he", "his": "he", "himself": "he",
    "she": "she", "her": "she", "hers": "she", "herself": "she",
    "they": "they", "them": "they", "their": "they", "theirs": "they", "themselves": "they",
    "we": "we", "us": "we", "our": "we", "ours": "we", "ourselves": "we",
    "you": "you", "your": "you", "yours": "you", "yourself": "you", "yourselves": "you",
    # Common KJV forms
    "ye": "you", "thee": "you", "thou": "you", "thy": "you", "thine": "you",
    "hath": "have", "doth": "do", "doeth": "do", "saith": "say", "sayeth": "say",
    "shalt": "shall", "wilt": "will", "wouldst": "would", "shouldst": "should",
    "art": "be", "wast": "be", "wert": "be",
    "goeth": "go", "cometh": "come", "maketh": "make", "taketh": "take",
    "giveth": "give", "knoweth": "know", "seeth": "see", "heareth": "hear",
    "speaketh": "speak", "walketh": "walk", "liveth": "live", "loveth": "love",
    "believeth": "believe", "receiveth": "receive", "bringeth": "bring",
    # Plurals of common nouns (sample)
    "men": "man", "women": "woman", "children": "child", "brethren": "brother",
    "oxen": "ox", "feet": "foot", "teeth": "tooth", "geese": "goose",
    # Past participles
    "blessed": "bless", "cursed": "curse",
}


def lemmatize_english(word: str) -> str:
    """Simple English lemmatization for KJV text."""
    word_lower = word.lower()
    
    # Check irregular forms first
    if word_lower in ENGLISH_IRREGULAR:
        return ENGLISH_IRREGULAR[word_lower]
    
    # Basic suffix rules
    if word_lower.endswith("ies") and len(word_lower) > 4:
        return word_lower[:-3] + "y"  # carries -> carry
    if word_lower.endswith("ied") and len(word_lower) > 4:
        return word_lower[:-3] + "y"  # carried -> carry
    if word_lower.endswith("es") and len(word_lower) > 3:
        if word_lower.endswith("shes") or word_lower.endswith("ches") or word_lower.endswith("xes") or word_lower.endswith("sses") or word_lower.endswith("zzes"):
            return word_lower[:-2]  # watches -> watch
        return word_lower[:-1]  # makes -> make (imperfect but ok)
    if word_lower.endswith("s") and len(word_lower) > 2 and not word_lower.endswith("ss"):
        return word_lower[:-1]  # words -> word
    if word_lower.endswith("ed") and len(word_lower) > 3:
        if word_lower.endswith("ied"):
            return word_lower[:-3] + "y"
        if word_lower[-3] == word_lower[-4] and word_lower[-3] in "bdgklmnprst":
            return word_lower[:-3]  # stopped -> stop
        return word_lower[:-2]  # walked -> walk
    if word_lower.endswith("ing") and len(word_lower) > 4:
        if word_lower[-4] == word_lower[-5] and word_lower[-4] in "bdgklmnprst":
            return word_lower[:-4]  # stopping -> stop
        return word_lower[:-3]  # walking -> walk
    
    return word_lower


def tokenize(text: str, lemmatize: bool = False) -> List[str]:
    """Tokenize text into words."""
    # Remove punctuation, split on whitespace
    words = re.findall(r"[A-Za-z\u00C0-\u024F\u1E00-\u1EFF']+", text)
    
    if lemmatize:
        return [lemmatize_english(w) for w in words if len(w) > 0]
    else:
        return [w for w in words if len(w) > 0]


def load_bible(bible_dir: Path) -> Dict[str, str]:
    """Load Bible text as dict of verse_id -> text."""
    verses = {}
    
    # Find the main text file
    txt_files = list(bible_dir.glob("*-x-bible.txt"))
    if not txt_files:
        return verses
    
    txt_file = txt_files[0]
    
    with open(txt_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t", 1)
            if len(parts) == 2:
                verse_id, text = parts
                verses[verse_id] = text
    
    return verses


def compute_cooccurrence(
    eng_verses: Dict[str, str],
    kc_verses: Dict[str, str],
    min_verse_overlap: int = 100
) -> Tuple[Dict[Tuple[str, str], int], Dict[str, int], Dict[str, int]]:
    """
    Compute co-occurrence statistics between English and Kuki-Chin words.
    
    Returns:
        pair_counts: Dict of (kc_word, eng_lemma) -> count
        kc_counts: Dict of kc_word -> total count
        eng_counts: Dict of eng_lemma -> total count
    """
    pair_counts = Counter()
    kc_counts = Counter()
    eng_counts = Counter()
    
    # Find common verses
    common_verses = set(eng_verses.keys()) & set(kc_verses.keys())
    
    if len(common_verses) < min_verse_overlap:
        print(f"  Warning: Only {len(common_verses)} common verses (min: {min_verse_overlap})")
        if len(common_verses) == 0:
            return pair_counts, kc_counts, eng_counts
    
    for verse_id in common_verses:
        eng_text = eng_verses[verse_id]
        kc_text = kc_verses[verse_id]
        
        # Tokenize (lemmatize English, keep KC as-is)
        eng_words = set(tokenize(eng_text, lemmatize=True))
        kc_words = set(tokenize(kc_text, lemmatize=False))
        
        # Update individual counts
        for kc_word in kc_words:
            kc_counts[kc_word] += 1
        for eng_word in eng_words:
            eng_counts[eng_word] += 1
        
        # Update pair counts (cross-product)
        for kc_word in kc_words:
            for eng_word in eng_words:
                pair_counts[(kc_word, eng_word)] += 1
    
    return pair_counts, kc_counts, eng_counts


def compute_association_scores(
    pair_counts: Dict[Tuple[str, str], int],
    kc_counts: Dict[str, int],
    eng_counts: Dict[str, int],
    total_verses: int,
    min_pair_count: int = 3,
    min_eng_freq: int = 5
) -> Dict[str, List[Tuple[str, float, int, float]]]:
    """
    Compute association scores for word pairs.
    
    Uses Positive PMI (PPMI) combined with a confidence weight:
    - PMI(kc, eng) = log2(P(kc, eng) / (P(kc) * P(eng)))
    - Confidence = min(pair_count, kc_freq) / kc_freq (how often the KC word co-occurs with this English word)
    - Final score combines PMI with frequency evidence
    
    Filters out:
    - Pairs occurring less than min_pair_count times
    - English words appearing less than min_eng_freq times (reduces noise from rare words)
    
    Returns:
        Dict of kc_word -> [(eng_word, pmi_score, raw_count, confidence), ...]
    """
    lexicon = defaultdict(list)
    
    for (kc_word, eng_word), count in pair_counts.items():
        # Skip low-frequency pairs
        if count < min_pair_count:
            continue
        
        # Skip rare English words (proper nouns, hapaxes)
        if eng_counts[eng_word] < min_eng_freq:
            continue
        
        # Skip single-letter words on both sides
        if len(kc_word) <= 1 or len(eng_word) <= 1:
            continue
        
        # Compute PMI
        p_pair = count / total_verses
        p_kc = kc_counts[kc_word] / total_verses
        p_eng = eng_counts[eng_word] / total_verses
        
        if p_kc > 0 and p_eng > 0:
            pmi = math.log2(p_pair / (p_kc * p_eng))
            
            # Only keep positive associations
            if pmi > 0:
                # Confidence: what fraction of KC word occurrences co-occur with this ENG word
                confidence = count / kc_counts[kc_word]
                lexicon[kc_word].append((eng_word, pmi, count, confidence))
    
    # Sort by confidence (stability) first, then PMI
    # This prioritizes consistent translations over rare high-PMI pairs
    for kc_word in lexicon:
        lexicon[kc_word].sort(key=lambda x: (-x[3], -x[1], -x[2]))
    
    return lexicon


def build_bootstrap_lexicon(
    eng_dir: Path,
    kc_dir: Path,
    output_path: Path,
    top_n: int = 5
) -> Dict[str, List[Tuple[str, float, int]]]:
    """
    Build bootstrap lexicon for one language pair.
    
    Args:
        eng_dir: Path to English Bible directory
        kc_dir: Path to Kuki-Chin Bible directory
        output_path: Where to write TSV output
        top_n: Number of top candidates to keep per KC word
    
    Returns:
        Lexicon dict
    """
    # Load Bibles
    eng_verses = load_bible(eng_dir)
    kc_verses = load_bible(kc_dir)
    
    print(f"  English verses: {len(eng_verses)}")
    print(f"  KC verses: {len(kc_verses)}")
    
    # Compute co-occurrence
    pair_counts, kc_counts, eng_counts = compute_cooccurrence(eng_verses, kc_verses)
    
    print(f"  Unique KC words: {len(kc_counts)}")
    print(f"  Unique ENG lemmas: {len(eng_counts)}")
    print(f"  Word pairs: {len(pair_counts)}")
    
    # Compute association scores
    total_verses = len(set(eng_verses.keys()) & set(kc_verses.keys()))
    lexicon = compute_association_scores(pair_counts, kc_counts, eng_counts, total_verses)
    
    print(f"  Lexicon entries: {len(lexicon)}")
    
    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("kc_word\tkc_freq\teng_gloss\tpmi_score\tpair_count\tconfidence\trank\n")
        
        for kc_word in sorted(lexicon.keys()):
            kc_freq = kc_counts[kc_word]
            candidates = lexicon[kc_word][:top_n]
            
            for rank, (eng_word, pmi, count, confidence) in enumerate(candidates, 1):
                f.write(f"{kc_word}\t{kc_freq}\t{eng_word}\t{pmi:.4f}\t{count}\t{confidence:.4f}\t{rank}\n")
    
    return lexicon


def main():
    parser = argparse.ArgumentParser(description="Build bootstrap lexicons via co-occurrence")
    parser.add_argument("--bibles-dir", type=Path, default=Path("bibles/extracted"),
                        help="Directory containing Bible subdirectories")
    parser.add_argument("--output-dir", type=Path, default=Path("data/lexicons"),
                        help="Output directory for lexicons")
    parser.add_argument("--english", type=str, default="eng",
                        help="ISO code for English Bible (default: eng)")
    parser.add_argument("--languages", type=str, nargs="*",
                        help="Specific languages to process (default: all)")
    parser.add_argument("--top-n", type=int, default=5,
                        help="Number of top candidates per word (default: 5)")
    
    args = parser.parse_args()
    
    # Find English Bible
    eng_dir = args.bibles_dir / args.english
    if not eng_dir.exists():
        print(f"Error: English Bible not found at {eng_dir}")
        return
    
    # Find all other language directories
    if args.languages:
        lang_dirs = [args.bibles_dir / lang for lang in args.languages]
    else:
        lang_dirs = [d for d in args.bibles_dir.iterdir() 
                     if d.is_dir() and d.name != args.english]
    
    print(f"Building bootstrap lexicons for {len(lang_dirs)} languages")
    print(f"English reference: {eng_dir}")
    print()
    
    # Process each language
    stats = []
    
    for kc_dir in sorted(lang_dirs):
        iso = kc_dir.name
        print(f"Processing {iso}...")
        
        output_path = args.output_dir / f"{iso}_lexicon.tsv"
        
        try:
            lexicon = build_bootstrap_lexicon(
                eng_dir, kc_dir, output_path, 
                top_n=args.top_n
            )
            stats.append({
                "iso": iso,
                "entries": len(lexicon),
                "output": str(output_path)
            })
            print(f"  -> Wrote {output_path}")
        except Exception as e:
            print(f"  Error: {e}")
            stats.append({
                "iso": iso,
                "entries": 0,
                "error": str(e)
            })
        
        print()
    
    # Write summary
    summary_path = args.output_dir / "lexicon_stats.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
    
    print(f"Summary written to {summary_path}")
    print(f"Total languages processed: {len(stats)}")
    print(f"Successful: {sum(1 for s in stats if s.get('entries', 0) > 0)}")


if __name__ == "__main__":
    main()
