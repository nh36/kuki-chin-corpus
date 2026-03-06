#!/usr/bin/env python3
"""
Build a unified wordform inventory across all Kuki-Chin Bible translations.
Outputs:
  - data/wordforms_by_language.tsv (all wordforms with language and frequency)
  - data/language_stats.tsv (summary statistics per language)
"""

import os
import json
from pathlib import Path
from collections import defaultdict

EXTRACTED_DIR = Path(__file__).parent.parent / "bibles" / "extracted"
DATA_DIR = Path(__file__).parent.parent / "data"


def load_metadata(iso_dir: Path) -> dict:
    """Load language metadata from datapackage.json."""
    dp_file = iso_dir / "datapackage.json"
    if dp_file.exists():
        with open(dp_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_wordforms(iso_dir: Path, iso: str) -> list[tuple[str, str, int]]:
    """Load wordforms from .wordforms file. Returns list of (iso, word, count)."""
    wf_file = iso_dir / f"{iso}-x-bible.wordforms"
    if not wf_file.exists():
        # Try alternate naming patterns (e.g., lus-x-bible-1959.wordforms)
        candidates = list(iso_dir.glob(f"{iso}-x-bible*.wordforms"))
        if candidates:
            wf_file = candidates[0]
        else:
            print(f"  Warning: {wf_file} not found")
            return []
    
    results = []
    with open(wf_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                word = parts[0]
                try:
                    count = int(parts[1])
                except ValueError:
                    count = 1
                results.append((iso, word, count))
    return results


def count_verses(iso_dir: Path, iso: str) -> int:
    """Count verses in the Bible text file."""
    txt_file = iso_dir / f"{iso}-x-bible.txt"
    if not txt_file.exists():
        # Try alternate naming patterns
        candidates = list(iso_dir.glob(f"{iso}-x-bible*.txt"))
        if candidates:
            txt_file = candidates[0]
        else:
            return 0
    
    count = 0
    with open(txt_file, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if "\t" in line and line.split("\t")[1].strip():
                count += 1
    return count


def main():
    DATA_DIR.mkdir(exist_ok=True)
    
    all_wordforms = []
    stats = []
    
    for iso_dir in sorted(EXTRACTED_DIR.iterdir()):
        if not iso_dir.is_dir():
            continue
        
        iso = iso_dir.name
        print(f"Processing {iso}...")
        
        metadata = load_metadata(iso_dir)
        lang_name = metadata.get("language_name", iso)
        
        wordforms = load_wordforms(iso_dir, iso)
        all_wordforms.extend(wordforms)
        
        verse_count = count_verses(iso_dir, iso)
        unique_words = len(set(w for _, w, _ in wordforms))
        total_tokens = sum(c for _, _, c in wordforms)
        
        stats.append({
            "iso": iso,
            "language_name": lang_name,
            "verses": verse_count,
            "unique_wordforms": unique_words,
            "total_tokens": total_tokens,
        })
        
        print(f"  {lang_name}: {verse_count} verses, {unique_words} unique words, {total_tokens} tokens")
    
    # Write wordforms
    wf_out = DATA_DIR / "wordforms_by_language.tsv"
    with open(wf_out, "w", encoding="utf-8") as f:
        f.write("iso\twordform\tfrequency\n")
        for iso, word, count in sorted(all_wordforms):
            f.write(f"{iso}\t{word}\t{count}\n")
    print(f"\nWrote {len(all_wordforms)} wordforms to {wf_out}")
    
    # Write stats
    stats_out = DATA_DIR / "language_stats.tsv"
    with open(stats_out, "w", encoding="utf-8") as f:
        f.write("iso\tlanguage_name\tverses\tunique_wordforms\ttotal_tokens\n")
        for s in stats:
            f.write(f"{s['iso']}\t{s['language_name']}\t{s['verses']}\t{s['unique_wordforms']}\t{s['total_tokens']}\n")
    print(f"Wrote language stats to {stats_out}")


if __name__ == "__main__":
    main()
