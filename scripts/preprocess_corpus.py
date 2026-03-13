#!/usr/bin/env python3
"""
Corpus Preprocessing Script for Kuki-Chin Bible Texts

This script cleans web-scraped Bible texts by:
1. Extracting metadata into separate JSON files
2. Normalizing Unicode (apostrophes, quotes, etc.)
3. Removing HTML artifacts
4. Validating verse format

Usage:
    python3 scripts/preprocess_corpus.py                    # Process all languages
    python3 scripts/preprocess_corpus.py ctd                # Process single language
    python3 scripts/preprocess_corpus.py --validate-only    # Just check without modifying
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from collections import Counter


def extract_metadata(lines: list[str]) -> tuple[dict, list[str]]:
    """Extract # prefixed metadata lines into a dict, return remaining lines."""
    metadata = {}
    verse_lines = []
    
    for line in lines:
        line = line.rstrip('\n')
        if line.startswith('#'):
            # Parse "# key: value" format
            match = re.match(r'^#\s*([^:]+):\s*(.*)$', line)
            if match:
                key = match.group(1).strip().lower().replace(' ', '_')
                value = match.group(2).strip()
                metadata[key] = value
        elif line.strip():  # Non-empty, non-metadata line
            verse_lines.append(line)
    
    return metadata, verse_lines


def normalize_unicode(text: str) -> str:
    """Normalize Unicode characters to their ASCII equivalents."""
    replacements = {
        '\u2019': "'",   # RIGHT SINGLE QUOTATION MARK → apostrophe
        '\u2018': "'",   # LEFT SINGLE QUOTATION MARK → apostrophe
        '\u201c': '"',   # LEFT DOUBLE QUOTATION MARK
        '\u201d': '"',   # RIGHT DOUBLE QUOTATION MARK
        '\u00a0': ' ',   # NO-BREAK SPACE → regular space
        '\u2013': '-',   # EN DASH
        '\u2014': '-',   # EM DASH
        '\ufeff': '',    # BOM
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def remove_html_artifacts(text: str) -> str:
    """Remove HTML entities and stray tags."""
    # HTML entities
    entities = {
        '&amp;': '&',
        '&nbsp;': ' ',
        '&lt;': '<',
        '&gt;': '>',
        '&quot;': '"',
        '&apos;': "'",
    }
    for entity, char in entities.items():
        text = text.replace(entity, char)
    
    # Remove stray HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    return text


def validate_verse_format(line: str) -> bool:
    """Check if line matches expected VERSE_ID\ttext format."""
    # VERSE_ID is 8 digits: BBCCCVVV (book, chapter, verse)
    return bool(re.match(r'^[0-9]{8}\t.+$', line))


def compute_statistics(verse_lines: list[str]) -> dict:
    """Compute corpus statistics."""
    word_counter = Counter()
    total_tokens = 0
    
    for line in verse_lines:
        if '\t' in line:
            text = line.split('\t', 1)[1]
            words = re.findall(r'\b[A-Za-z]+\b', text)
            word_counter.update(w.lower() for w in words)
            total_tokens += len(words)
    
    return {
        'total_verses': len(verse_lines),
        'total_tokens': total_tokens,
        'unique_tokens': len(word_counter),
        'top_10_words': dict(word_counter.most_common(10))
    }


def process_language(lang_dir: Path, validate_only: bool = False) -> dict:
    """Process a single language directory."""
    results = {
        'language': lang_dir.name,
        'status': 'ok',
        'issues': [],
        'changes': []
    }
    
    # Find the Bible text file
    txt_files = list(lang_dir.glob('*.txt'))
    if not txt_files:
        results['status'] = 'error'
        results['issues'].append('No .txt file found')
        return results
    
    txt_file = txt_files[0]
    
    # Check for existing metadata.json
    metadata_file = lang_dir / 'metadata.json'
    
    # Read the file
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract metadata
    metadata, verse_lines = extract_metadata(lines)
    
    if metadata:
        results['changes'].append(f"Extracted {len(metadata)} metadata fields")
    
    # Process verse lines
    cleaned_lines = []
    for i, line in enumerate(verse_lines):
        original = line
        
        # Normalize Unicode
        line = normalize_unicode(line)
        
        # Remove HTML artifacts
        line = remove_html_artifacts(line)
        
        # Validate format
        if not validate_verse_format(line):
            results['issues'].append(f"Line {i+1} invalid format: {line[:50]}...")
        
        if line != original:
            results['changes'].append(f"Normalized line {i+1}")
        
        cleaned_lines.append(line)
    
    # Build full metadata
    full_metadata = {
        'language_name': metadata.get('language_name', lang_dir.name),
        'iso_639_3': metadata.get('closest_iso_639-3', lang_dir.name),
        'source': {
            'url': metadata.get('url', ''),
            'scrape_date': metadata.get('year_short', '').replace('scraped ', ''),
            'scrape_tool': 'bible_scraper.py'
        },
        'copyright': {
            'short': metadata.get('copyright_short', ''),
            'long': metadata.get('copyright_long', '')
        },
        'preprocessing': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'script_version': '1.0',
            'steps': ['extracted_metadata', 'normalized_unicode', 'removed_html_artifacts']
        },
        'statistics': compute_statistics(cleaned_lines)
    }
    
    if validate_only:
        print(f"  Would create metadata.json with {len(full_metadata)} fields")
        print(f"  Would clean {len(results['changes'])} lines")
        return results
    
    # Archive original if changes made
    if results['changes'] or metadata:
        raw_file = txt_file.with_suffix('.raw.txt')
        if not raw_file.exists():
            with open(txt_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(raw_file, 'w', encoding='utf-8') as f:
                f.write(original_content)
            results['changes'].append(f"Archived original as {raw_file.name}")
    
    # Write cleaned text file (verse lines only)
    with open(txt_file, 'w', encoding='utf-8') as f:
        for line in cleaned_lines:
            f.write(line + '\n' if not line.endswith('\n') else line)
    
    # Write metadata.json
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(full_metadata, f, indent=2, ensure_ascii=False)
    results['changes'].append('Created metadata.json')
    
    results['status'] = 'ok' if not results['issues'] else 'warning'
    return results


def main():
    base_dir = Path(__file__).parent.parent / 'bibles' / 'extracted'
    
    validate_only = '--validate-only' in sys.argv
    specific_lang = None
    
    for arg in sys.argv[1:]:
        if not arg.startswith('--'):
            specific_lang = arg
    
    if specific_lang:
        lang_dirs = [base_dir / specific_lang]
    else:
        lang_dirs = sorted(base_dir.iterdir())
    
    print(f"Preprocessing Kuki-Chin Bible Corpora")
    print(f"{'Validation mode' if validate_only else 'Processing'}: {len(lang_dirs)} languages")
    print("=" * 60)
    
    all_results = []
    for lang_dir in lang_dirs:
        if not lang_dir.is_dir():
            continue
        
        print(f"\n{lang_dir.name}:")
        results = process_language(lang_dir, validate_only)
        all_results.append(results)
        
        if results['issues']:
            for issue in results['issues'][:5]:
                print(f"  ⚠ {issue}")
        if results['changes']:
            for change in results['changes'][:5]:
                print(f"  ✓ {change}")
        if not results['issues'] and not results['changes']:
            print(f"  ✓ Already clean")
    
    print("\n" + "=" * 60)
    ok = sum(1 for r in all_results if r['status'] == 'ok')
    warn = sum(1 for r in all_results if r['status'] == 'warning')
    err = sum(1 for r in all_results if r['status'] == 'error')
    print(f"Summary: {ok} ok, {warn} warnings, {err} errors")


if __name__ == '__main__':
    main()
