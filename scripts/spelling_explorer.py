#!/usr/bin/env python3
"""
Spelling Variation Explorer for Tedim Chin.

Analyzes the corpus for orthographic variants to determine:
1. Whether spelling variation is trivial and mechanically manageable
2. Which variants might be distinct forms vs genuine spelling differences
3. What normalization rules (if any) are safe to apply

Approach: Conservative exploration, not aggressive normalization.

Usage:
    python spelling_explorer.py --analyze
    python spelling_explorer.py --report
"""

import sys
import csv
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set
import json

csv.field_size_limit(sys.maxsize)

# =============================================================================
# VARIATION PATTERNS TO INVESTIGATE
# =============================================================================

# Potential orthographic alternations in Tedim
POTENTIAL_ALTERNATIONS = {
    # Final consonant variations
    'h_loss': (r'(.+)h$', r'\1'),        # word-final h loss?
    'k_h': (r'(.+)k$', r'\1h'),          # k ~ h alternation?
    
    # Vowel variations
    'ei_i': (r'ei', r'i'),               # ei ~ i?
    'ai_e': (r'ai', r'e'),               # ai ~ e?
    'ua_aw': (r'ua', r'aw'),             # ua ~ aw?
    
    # Consonant variations
    'ng_n': (r'ng', r'n'),               # ng ~ n?
    'kh_k': (r'kh', r'k'),               # kh ~ k?
    'ph_p': (r'ph', r'p'),               # ph ~ p?
    'th_t': (r'th', r't'),               # th ~ t?
    
    # Gemination
    'geminate': (r'(.)\1', r'\1'),       # double consonant ~ single?
}

# Known systematic alternations (Stem I vs Stem II)
KNOWN_ALTERNATIONS = {
    # Stem I (before vowel-initial suffix) vs Stem II (elsewhere)
    # These are grammatical, not spelling variants
    'mu': 'muh',     # see
    'za': 'zak',     # know
    'thei': 'theih', # be.able
    'pia': 'piak',   # give
    'nei': 'neih',   # have
    # These are NOT spelling variants - they are distinct forms
}


# =============================================================================
# ANALYSIS
# =============================================================================

class SpellingAnalyzer:
    """Analyzes corpus for spelling variation patterns."""
    
    def __init__(self, corpus_path: Path):
        self.corpus_path = corpus_path
        self.word_counts = Counter()
        self.word_contexts = defaultdict(list)  # word -> [verse_ids]
        self.potential_variants = defaultdict(set)  # base -> {variants}
        
    def load_corpus(self):
        """Load Tedim text from aligned corpus."""
        with open(self.corpus_path, 'r') as f:
            reader = csv.reader(f, delimiter='\t')
            header = next(reader)
            ctd_idx = header.index('ctd_Tedim Chin')
            verse_idx = 0  # verse_id column
            
            for row in reader:
                if len(row) > ctd_idx and row[ctd_idx]:
                    verse_id = row[verse_idx]
                    for word in row[ctd_idx].split():
                        # Clean word
                        w = word.strip('.,;:!?"()[]')
                        w = re.sub(r'[\u201c\u201d\u2018\u2019]', '', w)
                        w = w.strip("'")
                        if w and len(w) > 1:
                            self.word_counts[w.lower()] += 1
                            self.word_contexts[w.lower()].append(verse_id)
        
        print(f"Loaded {len(self.word_counts)} unique words, {sum(self.word_counts.values())} total tokens")
    
    def find_near_variants(self, max_edit_distance: int = 1):
        """
        Find pairs of words that differ by small edit distance.
        These might be spelling variants or distinct forms.
        """
        words = sorted(self.word_counts.keys())
        pairs = []
        
        for i, w1 in enumerate(words):
            if self.word_counts[w1] < 10:  # Skip rare words
                continue
            
            for w2 in words[i+1:]:
                if self.word_counts[w2] < 10:
                    continue
                
                # Quick length check
                if abs(len(w1) - len(w2)) > max_edit_distance:
                    continue
                
                # Calculate edit distance
                dist = self._edit_distance(w1, w2)
                if 0 < dist <= max_edit_distance:
                    pairs.append((w1, w2, dist, 
                                  self.word_counts[w1], 
                                  self.word_counts[w2]))
        
        return sorted(pairs, key=lambda x: -(x[3] + x[4]))
    
    def _edit_distance(self, s1: str, s2: str) -> int:
        """Calculate Levenshtein distance."""
        if len(s1) < len(s2):
            return self._edit_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        prev_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            curr_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = prev_row[j + 1] + 1
                deletions = curr_row[j] + 1
                substitutions = prev_row[j] + (c1 != c2)
                curr_row.append(min(insertions, deletions, substitutions))
            prev_row = curr_row
        
        return prev_row[-1]
    
    def analyze_specific_patterns(self) -> Dict[str, List[Tuple]]:
        """
        Analyze specific alternation patterns.
        Returns dict of pattern_name -> [(word1, word2, freq1, freq2), ...]
        """
        results = defaultdict(list)
        words = set(self.word_counts.keys())
        
        # Check each potential alternation
        for name, (pattern, replacement) in POTENTIAL_ALTERNATIONS.items():
            for word in words:
                if self.word_counts[word] < 20:  # Only frequent words
                    continue
                
                # Try applying the pattern
                if name == 'geminate':
                    # Special case: find doubled consonants
                    match = re.search(pattern, word)
                    if match:
                        variant = re.sub(pattern, replacement, word, count=1)
                        if variant != word and variant in words:
                            results[name].append((
                                word, variant,
                                self.word_counts[word],
                                self.word_counts[variant]
                            ))
                else:
                    # Standard pattern check
                    match = re.search(pattern, word)
                    if match:
                        variant = re.sub(pattern, replacement, word)
                        if variant != word and variant in words:
                            results[name].append((
                                word, variant,
                                self.word_counts[word],
                                self.word_counts[variant]
                            ))
        
        return results
    
    def check_h_variation(self) -> List[Tuple]:
        """
        Check word-final h variation specifically.
        This is the most common variation type (Stem I vs Stem II).
        """
        results = []
        words = set(self.word_counts.keys())
        
        for word in words:
            if self.word_counts[word] < 10:
                continue
            
            # Check if word + h exists
            with_h = word + 'h'
            if with_h in words:
                results.append((
                    word, with_h,
                    self.word_counts[word],
                    self.word_counts[with_h],
                    'h-addition'
                ))
            
            # Check if word - h exists
            if word.endswith('h') and len(word) > 2:
                without_h = word[:-1]
                if without_h in words:
                    results.append((
                        word, without_h,
                        self.word_counts[word],
                        self.word_counts[without_h],
                        'h-loss'
                    ))
        
        # Deduplicate
        seen = set()
        unique = []
        for item in results:
            key = tuple(sorted([item[0], item[1]]))
            if key not in seen:
                seen.add(key)
                unique.append(item)
        
        return sorted(unique, key=lambda x: -(x[2] + x[3]))
    
    def generate_report(self) -> str:
        """Generate comprehensive spelling variation report."""
        lines = []
        lines.append("=" * 70)
        lines.append("TEDIM CHIN SPELLING VARIATION ANALYSIS")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Total unique words: {len(self.word_counts)}")
        lines.append(f"Total tokens: {sum(self.word_counts.values())}")
        lines.append("")
        
        # H-variation (most important)
        lines.append("-" * 70)
        lines.append("1. WORD-FINAL H VARIATION (Stem I/II)")
        lines.append("-" * 70)
        lines.append("Note: Most of these are grammatical alternations, NOT spelling variants.")
        lines.append("Stem I (no -h) appears before vowel-initial suffixes.")
        lines.append("Stem II (-h or -k) appears elsewhere.")
        lines.append("")
        
        h_vars = self.check_h_variation()[:30]
        for word1, word2, freq1, freq2, vtype in h_vars:
            total = freq1 + freq2
            pct1 = freq1 / total * 100
            pct2 = freq2 / total * 100
            lines.append(f"  {word1:15s} ({freq1:5d}, {pct1:4.1f}%) ~ {word2:15s} ({freq2:5d}, {pct2:4.1f}%)")
        
        # Near-variants
        lines.append("")
        lines.append("-" * 70)
        lines.append("2. NEAR-VARIANTS (Edit Distance = 1)")
        lines.append("-" * 70)
        lines.append("Pairs differing by one character. May be typos, variants, or distinct words.")
        lines.append("")
        
        near_vars = self.find_near_variants(max_edit_distance=1)[:40]
        for word1, word2, dist, freq1, freq2 in near_vars:
            # Highlight the difference
            diff = self._highlight_diff(word1, word2)
            lines.append(f"  {word1:15s} ({freq1:5d}) ~ {word2:15s} ({freq2:5d})  [{diff}]")
        
        # Specific pattern analysis
        lines.append("")
        lines.append("-" * 70)
        lines.append("3. SPECIFIC ORTHOGRAPHIC PATTERNS")
        lines.append("-" * 70)
        
        patterns = self.analyze_specific_patterns()
        for pattern_name, pairs in patterns.items():
            if pairs:
                lines.append(f"\n  {pattern_name}:")
                for word1, word2, freq1, freq2 in pairs[:10]:
                    lines.append(f"    {word1:15s} ({freq1:5d}) ~ {word2:15s} ({freq2:5d})")
        
        # Summary
        lines.append("")
        lines.append("-" * 70)
        lines.append("4. PRELIMINARY ASSESSMENT")
        lines.append("-" * 70)
        
        h_variation_count = len(h_vars)
        near_variant_count = len(near_vars)
        
        lines.append("")
        lines.append(f"  H-variation pairs found: {h_variation_count}")
        lines.append(f"  Near-variant pairs found: {near_variant_count}")
        lines.append("")
        lines.append("  INTERPRETATION:")
        lines.append("  - Most 'variation' appears to be grammatical (Stem I/II alternation)")
        lines.append("  - True orthographic variants seem limited")
        lines.append("  - Aggressive normalization NOT recommended at this stage")
        lines.append("  - Safe to treat Stem I/II as related but distinct forms")
        
        return '\n'.join(lines)
    
    def _highlight_diff(self, w1: str, w2: str) -> str:
        """Highlight the character difference between two words."""
        # Simple approach: show what's different
        if len(w1) != len(w2):
            if len(w1) < len(w2):
                return f"+{w2[len(w1):]}"
            else:
                return f"-{w1[len(w2):]}"
        
        for i, (c1, c2) in enumerate(zip(w1, w2)):
            if c1 != c2:
                return f"{c1}→{c2} at pos {i}"
        
        return "identical?"


# =============================================================================
# MAIN
# =============================================================================

def main():
    base_dir = Path(__file__).parent.parent
    corpus_path = base_dir / 'data' / 'verses_aligned.tsv'
    output_dir = base_dir / 'analysis'
    output_dir.mkdir(exist_ok=True)
    
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    analyzer = SpellingAnalyzer(corpus_path)
    analyzer.load_corpus()
    
    if command == '--analyze':
        # Run analysis and show summary
        print("\n=== H-VARIATION (Stem I/II) ===")
        h_vars = analyzer.check_h_variation()[:20]
        for word1, word2, freq1, freq2, vtype in h_vars:
            print(f"  {word1:15s} ({freq1:5d}) ~ {word2:15s} ({freq2:5d})")
        
        print("\n=== NEAR-VARIANTS ===")
        near_vars = analyzer.find_near_variants()[:20]
        for word1, word2, dist, freq1, freq2 in near_vars:
            print(f"  {word1:15s} ({freq1:5d}) ~ {word2:15s} ({freq2:5d})")
        
        # Save full analysis
        with open(output_dir / 'spelling_analysis.json', 'w') as f:
            json.dump({
                'h_variations': [(w1, w2, f1, f2, t) for w1, w2, f1, f2, t in h_vars],
                'near_variants': [(w1, w2, d, f1, f2) for w1, w2, d, f1, f2 in near_vars[:100]],
                'specific_patterns': {k: v[:20] for k, v in analyzer.analyze_specific_patterns().items()},
            }, f, indent=2)
        
        print(f"\nFull analysis saved to {output_dir / 'spelling_analysis.json'}")
    
    elif command == '--report':
        report = analyzer.generate_report()
        print(report)
        
        # Save report
        report_path = output_dir / 'spelling_variation_report.txt'
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nReport saved to {report_path}")
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()
