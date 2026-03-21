#!/usr/bin/env python3
"""
Normalize Tedim Chin orthography from various scholarly notations to Bible orthography.

This script converts examples from:
- ZNC (Zam Ngaih Cing) IPA notation with tone diacritics
- Henderson (1965) notation
- Singh (2018) Sukte notation

To the practical "Bible orthography" used in ctd-x-bible.txt

Usage:
    python normalize_orthography.py "example text"
    python normalize_orthography.py --file input.txt
    python normalize_orthography.py --report docs/grammar/lit-reviews/05-vp-01-verb-stems-lit.md
    
As a module:
    from normalize_orthography import normalize_to_bible, normalize_example_line
"""

import re
import sys
import argparse
from pathlib import Path

# =============================================================================
# Character Mappings
# =============================================================================

# IPA to Bible orthography mappings
IPA_TO_BIBLE = {
    # Consonants
    'ʔ': 'h',      # Glottal stop → h (word-finally)
    'Ɂ': 'h',      # Alternative glottal stop symbol
    'ŋ': 'ng',     # Velar nasal
    'x': 'kh',     # Velar fricative
    'χ': 'kh',     # Uvular fricative (variant)
    'ɣ': 'g',      # Voiced velar fricative (if present)
    
    # Aspirates (IPA superscript h)
    'pʰ': 'ph',
    'tʰ': 'th',
    'kʰ': 'kh',
    
    # Diphthongs with ɔ (must come before single ɔ mapping)
    'ɔi': 'oi',    # ɔi diphthong → oi
    'ɔ̀i': 'oi',   # with low tone
    'ɔ́i': 'oi',   # with high tone
    'ɔ̄i': 'oi',   # with mid tone
    'ͻi': 'oi',    # alternative symbol
    'ͻ̀i': 'oi',
    'ͻ́i': 'oi',
    'ͻ̄i': 'oi',
    'ɔu': 'o',     # ɔu diphthong → o (per Henderson: 'o' [ou])
    
    # Vowels
    'ɔ': 'aw',     # Open-mid back rounded (not in diphthong)
    'ɔ́': 'aw',    # With high tone
    'ɔ̄': 'aw',    # With mid tone  
    'ɔ̀': 'aw',    # With low tone
    'ͻ': 'aw',     # Alternative symbol (Greek small letter omicron with hook)
    'ͻ́': 'aw',
    'ͻ̄': 'aw',
    'ͻ̀': 'aw',
    'ə': 'a',      # Schwa → a (approximation for Sukte)
    'ǝ': 'a',      # Alternative schwa
    'ɛ': 'e',      # Open-mid front (if present)
    'ı': 'i',      # Dotless i (used in some IPA)
    'ı́': 'i',
    'ı̄': 'i',
    'ı̀': 'i',
    
    # Special sequences
    'lʔ': 'lh',    # Lateral + glottal
    'lɁ': 'lh',
    'ɂw': 'w',     # Pre-glottalized w → w
    'ʔw': 'w',
}

# Tone diacritics to remove
TONE_DIACRITICS = [
    '\u0301',  # Combining acute accent (́)
    '\u0304',  # Combining macron (̄)
    '\u0300',  # Combining grave accent (̀)
    '\u0302',  # Combining circumflex (̂)
    '\u030c',  # Combining caron (̌)
    '\u0303',  # Combining tilde (̃)
]

# Standalone tone marks (precomposed)
TONE_CHARS = {
    'á': 'a', 'ā': 'a', 'à': 'a', 'â': 'a',
    'é': 'e', 'ē': 'e', 'è': 'e', 'ê': 'e',
    'í': 'i', 'ī': 'i', 'ì': 'i', 'î': 'i',
    'ó': 'o', 'ō': 'o', 'ò': 'o', 'ô': 'o',
    'ú': 'u', 'ū': 'u', 'ù': 'u', 'û': 'u',
    'ɔ́': 'aw', 'ɔ̄': 'aw', 'ɔ̀': 'aw',
}

# =============================================================================
# Core Normalization Functions
# =============================================================================

def remove_tone_diacritics(text: str) -> str:
    """Remove combining tone diacritics from text."""
    for diacritic in TONE_DIACRITICS:
        text = text.replace(diacritic, '')
    return text

def normalize_to_bible(text: str, preserve_gloss: bool = False) -> str:
    """
    Convert IPA/scholarly notation to Bible orthography.
    
    Args:
        text: Input text in ZNC IPA, Henderson, or Singh notation
        preserve_gloss: If True, don't modify glosses (text in single quotes or after =)
    
    Returns:
        Text normalized to Bible orthography
    """
    if not text:
        return text
    
    result = text
    
    # FIRST: Remove combining tone diacritics (so ɔ̀i becomes ɔi)
    result = remove_tone_diacritics(result)
    
    # SECOND: Handle precomposed tone characters (á → a, etc.)
    for toned, plain in TONE_CHARS.items():
        result = result.replace(toned, plain)
    
    # THIRD: Handle multi-character IPA sequences (diphthongs, aspirates)
    # Sort by length descending so longer sequences match first
    for ipa, bible in sorted(IPA_TO_BIBLE.items(), key=lambda x: -len(x[0])):
        if len(ipa) > 1:
            result = result.replace(ipa, bible)
    
    # FOURTH: Handle remaining single-character IPA
    for ipa, bible in IPA_TO_BIBLE.items():
        if len(ipa) == 1:
            result = result.replace(ipa, bible)
    
    # Clean up any double consonants that might result from conversion
    # (e.g., ngng → ng, khkh → kh)
    result = re.sub(r'(ng)\1+', r'\1', result)
    result = re.sub(r'(kh)\1+', r'\1', result)
    result = re.sub(r'(ph)\1+', r'\1', result)
    result = re.sub(r'(th)\1+', r'\1', result)
    
    # Handle word-medial glottal stop (should often be omitted)
    # Keep h at word boundaries, remove medially in some contexts
    # This is a heuristic - medial ʔ often not written in Bible
    
    return result

def normalize_word(word: str) -> str:
    """Normalize a single word to Bible orthography."""
    return normalize_to_bible(word)

def extract_and_normalize_example(line: str) -> tuple:
    """
    Extract Tedim example from a line and return normalized version.
    
    Handles common formats:
    - (42) pàt 'cotton'
    - /pat/ 'cotton'
    - pàt 'cotton'
    - pàt => normalized
    
    Returns:
        Tuple of (original_tedim, normalized_tedim, gloss)
    """
    # Pattern for numbered examples: (N) word 'gloss'
    numbered = re.match(r"^\s*\(?\d+\)?\s*(.+?)\s+'([^']+)'", line)
    if numbered:
        tedim = numbered.group(1).strip()
        gloss = numbered.group(2)
        return (tedim, normalize_to_bible(tedim), gloss)
    
    # Pattern for IPA in slashes: /word/ 'gloss'
    ipa_pattern = re.match(r"^\s*/([^/]+)/\s+'([^']+)'", line)
    if ipa_pattern:
        tedim = ipa_pattern.group(1).strip()
        gloss = ipa_pattern.group(2)
        return (tedim, normalize_to_bible(tedim), gloss)
    
    # Pattern for word 'gloss' (simple)
    simple = re.match(r"^\s*([a-zA-Zɔŋʔɂəɛɪʊáéíóúàèìòùāēīōū]+(?:[- ][a-zA-Zɔŋʔɂəɛɪʊáéíóúàèìòùāēīōū]+)*)\s+'([^']+)'", line)
    if simple:
        tedim = simple.group(1).strip()
        gloss = simple.group(2)
        return (tedim, normalize_to_bible(tedim), gloss)
    
    return (None, None, None)

def normalize_example_line(line: str) -> str:
    """
    Add Bible orthography annotation to an example line.
    
    Input:  (42) pàt 'cotton'
    Output: (42) pàt [Bible: pat] 'cotton'
    """
    original, normalized, gloss = extract_and_normalize_example(line)
    
    if original and normalized and original != normalized:
        # Insert [Bible: ...] before the gloss
        return line.replace(f"'{gloss}'", f"[Bible: {normalized}] '{gloss}'")
    
    return line

# =============================================================================
# Report Processing Functions
# =============================================================================

def is_example_line(line: str) -> bool:
    """Check if a line appears to be a linguistic example."""
    # Numbered examples
    if re.match(r'^\s*\(\d+\)', line):
        return True
    # IPA in slashes
    if re.search(r'/[^/]+/', line):
        return True
    # Lines with Tedim + gloss pattern
    if re.search(r"[ɔŋʔɂəɛáéíóúàèìòùāēīōūͻɁı].*'[^']+'", line):
        return True
    return False

def process_markdown_report(content: str) -> str:
    """
    Process a markdown literature review report, adding Bible orthography
    annotations to linguistic examples.
    """
    lines = content.split('\n')
    result_lines = []
    
    in_code_block = False
    in_table = False
    
    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            continue
        
        # Track tables
        if '|' in line and not in_code_block:
            in_table = True
        elif in_table and not line.strip().startswith('|') and line.strip():
            in_table = False
        
        # Skip processing in code blocks and tables
        if in_code_block or in_table:
            result_lines.append(line)
            continue
        
        # Process example lines
        if is_example_line(line):
            processed = normalize_example_line(line)
            result_lines.append(processed)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)

def add_bible_tier_to_examples(content: str) -> str:
    """
    Add Bible orthography tier to examples in literature reviews.
    
    Instead of inline annotations, this adds a separate line below each
    line containing IPA/toned Tedim content with the normalized version.
    
    Format:
        Original: mànnɔú-ín à naú-nú-tɔ̀Ɂ tuí tɔī
        [≈Bible: manno-in a nau-nu-tawh tui toi]
    """
    lines = content.split('\n')
    result_lines = []
    
    # Words/patterns to skip (proper names, common English/French words)
    skip_words = {
        'Eugénie', 'Eugenie', 'café', 'naïve', 'résumé', 'exposé',
        'Déclaration', 'première', 'Zürich', 'Müller', 'über', 'für',
    }
    
    # Lines to skip entirely
    skip_line_patterns = [
        r'^\*\*Source:\*\*',
        r'^[-–] Henderson',
        r'^[-–] Zam Ngaih', 
        r'^[-–] Singh',
        r'^[-–] Otsuka',
        r'^#{1,6}\s',  # Headers
        r'^\s*$',  # Empty lines
        r'^\[≈Bible:',  # Already normalized
    ]
    skip_line_re = re.compile('|'.join(skip_line_patterns))
    
    # Characters that indicate Tedim/IPA content
    IPA_CHARS = 'ɔŋʔɂəɛͻɁıʰ'
    TONED_VOWELS = 'áéíóúàèìòùāēīōūâêîôûǎěǐǒǔ'
    COMBINING = '\u0300\u0301\u0302\u0304\u0306\u030c\u0303'
    MODIFIERS = '\u02b0\u02b1\u02b2\u02b7\u02bc'
    TEDIM_MARKERS = IPA_CHARS + TONED_VOWELS + COMBINING + MODIFIERS
    
    def has_tedim_content(text: str) -> bool:
        """Check if text contains IPA/toned characters."""
        for char in text:
            if char in TEDIM_MARKERS:
                return True
        return False
    
    def normalize_line_content(text: str) -> str:
        """Normalize all Tedim words in a line."""
        # Pattern to find words (including hyphenated)
        word_pattern = re.compile(r'[a-zA-Z' + re.escape(TEDIM_MARKERS) + r']+(?:-[a-zA-Z' + re.escape(TEDIM_MARKERS) + r']+)*', re.UNICODE)
        
        def replace_word(match):
            word = match.group(0)
            if word in skip_words:
                return word
            normalized = normalize_to_bible(word)
            return normalized
        
        return word_pattern.sub(replace_word, text)
    
    def extract_tedim_content(line: str) -> list:
        """Extract Tedim phrases from a line (in backticks, quotes, or standalone)."""
        tedim_phrases = []
        
        # Extract content in backticks - these are always Tedim examples
        backtick_matches = re.findall(r'`([^`]+)`', line)
        for match in backtick_matches:
            if has_tedim_content(match):
                tedim_phrases.append(match)
        
        # If we found backtick content, that's the primary source - return it
        if tedim_phrases:
            return tedim_phrases
        
        # Extract content in single quotes (linguistic examples)
        # Be careful not to grab English glosses
        quote_matches = re.findall(r"'([^']+)'", line)
        for match in quote_matches:
            if has_tedim_content(match) and not match.startswith(('the ', 'a ', 'to ')):
                tedim_phrases.append(match)
        
        if tedim_phrases:
            return tedim_phrases
        
        # For lines without quotes/backticks, extract only the Tedim words
        # (not the surrounding English)
        word_pattern = re.compile(
            r'-?[a-zA-Z' + re.escape(TEDIM_MARKERS) + r']+(?:-[a-zA-Z' + re.escape(TEDIM_MARKERS) + r']+)*',
            re.UNICODE
        )
        
        tedim_words = []
        for match in word_pattern.finditer(line):
            word = match.group(0)
            # Include words with 2+ chars if they have Tedim markers
            if has_tedim_content(word) and len(word) >= 2:
                tedim_words.append(word)
        
        if tedim_words:
            # Return as a single phrase of just the Tedim words
            tedim_phrases.append(' '.join(tedim_words))
        
        return tedim_phrases
    
    def get_indent(line: str) -> str:
        """Get the indentation of a line."""
        match = re.match(r'^(\s*)', line)
        return match.group(1) if match else ''
    
    in_code_block = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Track fenced code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result_lines.append(line)
            i += 1
            continue
        
        # Skip inside fenced code blocks
        if in_code_block:
            result_lines.append(line)
            i += 1
            continue
        
        # Skip lines that shouldn't be processed
        if skip_line_re.search(line):
            result_lines.append(line)
            i += 1
            continue
        
        # Skip if next line is already a normalization
        if i + 1 < len(lines) and lines[i + 1].strip().startswith('[≈Bible:'):
            result_lines.append(line)
            i += 1
            continue
        
        # Check for Tedim content
        if has_tedim_content(line):
            result_lines.append(line)
            
            # Extract and normalize Tedim phrases
            phrases = extract_tedim_content(line)
            if phrases:
                # Create normalized versions
                normalized_phrases = []
                for phrase in phrases:
                    norm = normalize_line_content(phrase)
                    if norm != phrase:  # Only add if different
                        normalized_phrases.append(norm)
                
                if normalized_phrases:
                    # Add normalization line with appropriate indent
                    indent = get_indent(line)
                    # For table rows, add inline comment at end
                    if '|' in line:
                        # Add normalization as comment after the row
                        norm_text = ' '.join(normalized_phrases)
                        result_lines[-1] = result_lines[-1] + f' <!-- ≈Bible: {norm_text} -->'
                    else:
                        norm_line = indent + '[≈Bible: ' + ' | '.join(normalized_phrases) + ']'
                        result_lines.append(norm_line)
        else:
            result_lines.append(line)
        
        i += 1
    
    return '\n'.join(result_lines)

# =============================================================================
# Batch Processing
# =============================================================================

def process_all_lit_reviews(lit_review_dir: Path, dry_run: bool = False) -> dict:
    """
    Process all literature review files in a directory.
    
    Args:
        lit_review_dir: Path to lit-reviews directory
        dry_run: If True, don't write changes
    
    Returns:
        Dict of {filename: num_changes}
    """
    results = {}
    
    for md_file in sorted(lit_review_dir.glob('*-lit.md')):
        print(f"Processing {md_file.name}...")
        
        original = md_file.read_text(encoding='utf-8')
        processed = add_bible_tier_to_examples(original)
        
        # Count changes
        orig_lines = original.split('\n')
        proc_lines = processed.split('\n')
        changes = sum(1 for o, p in zip(orig_lines, proc_lines) if o != p)
        
        results[md_file.name] = changes
        
        if changes > 0 and not dry_run:
            md_file.write_text(processed, encoding='utf-8')
            print(f"  → {changes} lines modified")
        elif changes > 0:
            print(f"  → {changes} lines would be modified (dry run)")
        else:
            print(f"  → No changes needed")
    
    return results

# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Normalize Tedim Chin orthography to Bible style'
    )
    parser.add_argument(
        'text', nargs='?',
        help='Text to normalize (if not using --file or --report)'
    )
    parser.add_argument(
        '--file', '-f',
        help='Input file to normalize'
    )
    parser.add_argument(
        '--report', '-r',
        help='Literature review markdown file to process'
    )
    parser.add_argument(
        '--all-reports', '-a',
        help='Process all lit reviews in directory'
    )
    parser.add_argument(
        '--dry-run', '-n', action='store_true',
        help='Show what would change without modifying files'
    )
    parser.add_argument(
        '--output', '-o',
        help='Output file (default: stdout or in-place for reports)'
    )
    
    args = parser.parse_args()
    
    if args.all_reports:
        lit_dir = Path(args.all_reports)
        if not lit_dir.exists():
            print(f"Error: Directory not found: {lit_dir}", file=sys.stderr)
            sys.exit(1)
        results = process_all_lit_reviews(lit_dir, args.dry_run)
        total = sum(results.values())
        print(f"\nTotal: {total} lines modified across {len(results)} files")
        
    elif args.report:
        report_path = Path(args.report)
        if not report_path.exists():
            print(f"Error: File not found: {report_path}", file=sys.stderr)
            sys.exit(1)
        
        content = report_path.read_text(encoding='utf-8')
        processed = add_bible_tier_to_examples(content)
        
        if args.output:
            Path(args.output).write_text(processed, encoding='utf-8')
        elif args.dry_run:
            # Show diff
            orig_lines = content.split('\n')
            proc_lines = processed.split('\n')
            for i, (o, p) in enumerate(zip(orig_lines, proc_lines), 1):
                if o != p:
                    print(f"Line {i}:")
                    print(f"  - {o}")
                    print(f"  + {p}")
        else:
            report_path.write_text(processed, encoding='utf-8')
            print(f"Updated {report_path}")
            
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        
        content = file_path.read_text(encoding='utf-8')
        normalized = normalize_to_bible(content)
        
        if args.output:
            Path(args.output).write_text(normalized, encoding='utf-8')
        else:
            print(normalized)
            
    elif args.text:
        print(normalize_to_bible(args.text))
        
    else:
        # Interactive mode: read from stdin
        for line in sys.stdin:
            print(normalize_to_bible(line.rstrip()))

if __name__ == '__main__':
    main()
