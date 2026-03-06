#!/usr/bin/env python3
"""
Build a unified verse alignment table across all Kuki-Chin Bible translations.

Creates a TSV with one row per verse_id, and columns for each language.
This enables parallel comparison of translations.

Output:
  - data/verses_aligned.tsv: All verses aligned by verse_id
  - data/alignment_stats.tsv: Coverage statistics per language
"""

import json
import re
from collections import defaultdict
from pathlib import Path

EXTRACTED_DIR = Path(__file__).parent.parent / "bibles" / "extracted"
DATA_DIR = Path(__file__).parent.parent / "data"

# Book names for readable output
BOOK_NAMES = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles",
    15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms",
    20: "Proverbs", 21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
    28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
    33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah", 37: "Haggai",
    38: "Zechariah", 39: "Malachi", 40: "Matthew", 41: "Mark", 42: "Luke",
    43: "John", 44: "Acts", 45: "Romans", 46: "1 Corinthians",
    47: "2 Corinthians", 48: "Galatians", 49: "Ephesians", 50: "Philippians",
    51: "Colossians", 52: "1 Thessalonians", 53: "2 Thessalonians",
    54: "1 Timothy", 55: "2 Timothy", 56: "Titus", 57: "Philemon",
    58: "Hebrews", 59: "James", 60: "1 Peter", 61: "2 Peter", 62: "1 John",
    63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation",
}


def parse_verse_id(verse_id: str) -> tuple[int, int, int]:
    """Parse BBCCCVVV format to (book, chapter, verse)."""
    verse_id = verse_id.zfill(8)
    book = int(verse_id[:2])
    chapter = int(verse_id[2:5])
    verse = int(verse_id[5:8])
    return book, chapter, verse


def format_verse_ref(verse_id: str) -> str:
    """Format verse_id as readable reference (e.g., 'Genesis 1:1')."""
    book, chapter, verse = parse_verse_id(verse_id)
    book_name = BOOK_NAMES.get(book, f"Book{book}")
    return f"{book_name} {chapter}:{verse}"


def load_metadata(iso_dir: Path) -> dict:
    """Load language metadata from datapackage.json."""
    dp_file = iso_dir / "datapackage.json"
    if dp_file.exists():
        with open(dp_file, encoding="utf-8") as f:
            return json.load(f)
    return {}


def load_verses(iso_dir: Path, iso: str) -> dict[str, str]:
    """Load verses from text file. Returns dict of verse_id -> text."""
    # Find the text file (may have different naming patterns)
    txt_files = list(iso_dir.glob(f"{iso}-x-bible*.txt"))
    if not txt_files:
        return {}
    
    txt_file = txt_files[0]
    verses = {}
    
    with open(txt_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            parts = line.split("\t", 1)
            if len(parts) == 2:
                verse_id, text = parts
                # Normalize verse_id to 8 digits
                if verse_id.isdigit():
                    verse_id = verse_id.zfill(8)
                    if text.strip():
                        verses[verse_id] = text.strip()
    
    return verses


def main():
    DATA_DIR.mkdir(exist_ok=True)
    
    # Collect all verses by language
    all_verses = {}  # iso -> {verse_id -> text}
    language_names = {}  # iso -> name
    
    for iso_dir in sorted(EXTRACTED_DIR.iterdir()):
        if not iso_dir.is_dir():
            continue
        
        iso = iso_dir.name
        metadata = load_metadata(iso_dir)
        lang_name = metadata.get("language_name", iso)
        # Clean up HTML in names
        lang_name = re.sub(r'<[^>]+>', ' ', lang_name).strip()
        
        verses = load_verses(iso_dir, iso)
        if verses:
            all_verses[iso] = verses
            language_names[iso] = lang_name
            print(f"Loaded {iso} ({lang_name}): {len(verses)} verses")
    
    # Get all unique verse IDs
    all_verse_ids = set()
    for verses in all_verses.values():
        all_verse_ids.update(verses.keys())
    
    # Sort verse IDs numerically
    sorted_verse_ids = sorted(all_verse_ids, key=lambda x: int(x))
    
    # Sort languages (put English first for reference)
    sorted_isos = sorted(all_verses.keys(), key=lambda x: (x != "eng", x))
    
    print(f"\nTotal unique verse IDs: {len(sorted_verse_ids)}")
    print(f"Languages: {', '.join(sorted_isos)}")
    
    # Write aligned verses
    aligned_file = DATA_DIR / "verses_aligned.tsv"
    with open(aligned_file, "w", encoding="utf-8") as f:
        # Header
        header = ["verse_id", "reference"] + [f"{iso}_{language_names[iso]}" for iso in sorted_isos]
        f.write("\t".join(header) + "\n")
        
        # Data rows
        for verse_id in sorted_verse_ids:
            ref = format_verse_ref(verse_id)
            row = [verse_id, ref]
            for iso in sorted_isos:
                text = all_verses[iso].get(verse_id, "")
                # Escape tabs and newlines in text
                text = text.replace("\t", " ").replace("\n", " ")
                row.append(text)
            f.write("\t".join(row) + "\n")
    
    print(f"\nWrote {len(sorted_verse_ids)} aligned verses to {aligned_file}")
    
    # Calculate coverage statistics
    stats = []
    for iso in sorted_isos:
        verses = all_verses[iso]
        coverage = len(verses) / len(sorted_verse_ids) * 100 if sorted_verse_ids else 0
        
        # Calculate book coverage
        books_present = set()
        for verse_id in verses.keys():
            book, _, _ = parse_verse_id(verse_id)
            books_present.add(book)
        
        stats.append({
            "iso": iso,
            "language_name": language_names[iso],
            "verses": len(verses),
            "total_possible": len(sorted_verse_ids),
            "coverage_pct": round(coverage, 2),
            "books_count": len(books_present),
        })
    
    # Write stats
    stats_file = DATA_DIR / "alignment_stats.tsv"
    with open(stats_file, "w", encoding="utf-8") as f:
        f.write("iso\tlanguage_name\tverses\ttotal_possible\tcoverage_pct\tbooks_count\n")
        for s in stats:
            f.write(f"{s['iso']}\t{s['language_name']}\t{s['verses']}\t{s['total_possible']}\t{s['coverage_pct']}\t{s['books_count']}\n")
    
    print(f"Wrote coverage stats to {stats_file}")
    
    # Print summary
    print("\nCoverage Summary:")
    for s in stats:
        print(f"  {s['iso']:4} {s['language_name']:25} {s['verses']:6} verses ({s['coverage_pct']:5.1f}%) - {s['books_count']} books")


if __name__ == "__main__":
    main()
