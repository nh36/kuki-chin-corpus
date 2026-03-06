#!/usr/bin/env python3
"""
Scrape Bible texts from bible.com and convert to paralleltext.info format.

Output format matches existing corpus:
- {iso}-x-bible.txt: TSV with verse_id TAB text
- {iso}-x-bible.wordforms: TSV with word TAB frequency
- datapackage.json: Metadata
- README.md: Documentation

Usage:
    python scrape_bible.py --version-id 1 --iso eng --abbrev KJV --name "King James Version"
    python scrape_bible.py --version-id 1958 --iso cnk --abbrev KCL02 --name "Khumi Chin"
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import quote

# We'll use urllib since requests might not be installed
import urllib.request
import urllib.error


# Book codes used by bible.com
BOOKS = [
    ("GEN", "Genesis", 50),
    ("EXO", "Exodus", 40),
    ("LEV", "Leviticus", 27),
    ("NUM", "Numbers", 36),
    ("DEU", "Deuteronomy", 34),
    ("JOS", "Joshua", 24),
    ("JDG", "Judges", 21),
    ("RUT", "Ruth", 4),
    ("1SA", "1 Samuel", 31),
    ("2SA", "2 Samuel", 24),
    ("1KI", "1 Kings", 22),
    ("2KI", "2 Kings", 25),
    ("1CH", "1 Chronicles", 29),
    ("2CH", "2 Chronicles", 36),
    ("EZR", "Ezra", 10),
    ("NEH", "Nehemiah", 13),
    ("EST", "Esther", 10),
    ("JOB", "Job", 42),
    ("PSA", "Psalms", 150),
    ("PRO", "Proverbs", 31),
    ("ECC", "Ecclesiastes", 12),
    ("SNG", "Song of Solomon", 8),
    ("ISA", "Isaiah", 66),
    ("JER", "Jeremiah", 52),
    ("LAM", "Lamentations", 5),
    ("EZK", "Ezekiel", 48),
    ("DAN", "Daniel", 12),
    ("HOS", "Hosea", 14),
    ("JOL", "Joel", 3),
    ("AMO", "Amos", 9),
    ("OBA", "Obadiah", 1),
    ("JON", "Jonah", 4),
    ("MIC", "Micah", 7),
    ("NAM", "Nahum", 3),
    ("HAB", "Habakkuk", 3),
    ("ZEP", "Zephaniah", 3),
    ("HAG", "Haggai", 2),
    ("ZEC", "Zechariah", 14),
    ("MAL", "Malachi", 4),
    # New Testament
    ("MAT", "Matthew", 28),
    ("MRK", "Mark", 16),
    ("LUK", "Luke", 24),
    ("JHN", "John", 21),
    ("ACT", "Acts", 28),
    ("ROM", "Romans", 16),
    ("1CO", "1 Corinthians", 16),
    ("2CO", "2 Corinthians", 13),
    ("GAL", "Galatians", 6),
    ("EPH", "Ephesians", 6),
    ("PHP", "Philippians", 4),
    ("COL", "Colossians", 4),
    ("1TH", "1 Thessalonians", 5),
    ("2TH", "2 Thessalonians", 3),
    ("1TI", "1 Timothy", 6),
    ("2TI", "2 Timothy", 4),
    ("TIT", "Titus", 3),
    ("PHM", "Philemon", 1),
    ("HEB", "Hebrews", 13),
    ("JAS", "James", 5),
    ("1PE", "1 Peter", 5),
    ("2PE", "2 Peter", 3),
    ("1JN", "1 John", 5),
    ("2JN", "2 John", 1),
    ("3JN", "3 John", 1),
    ("JUD", "Jude", 1),
    ("REV", "Revelation", 22),
]

# Map book index (1-66) to book code
BOOK_NUM_TO_CODE = {i + 1: code for i, (code, _, _) in enumerate(BOOKS)}


def fetch_chapter(version_id: int, book_code: str, chapter: int, abbrev: str) -> str:
    """Fetch a chapter from bible.com and return the markdown text."""
    url = f"https://www.bible.com/en-GB/bible/{version_id}/{book_code}.{chapter}.{abbrev}"
    
    # Use a simple text fetcher approach - we'll use curl for reliability
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml",
            }
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            html = response.read().decode("utf-8")
            return html
    except urllib.error.HTTPError as e:
        print(f"  HTTP Error {e.code} for {url}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"  Error fetching {url}: {e}", file=sys.stderr)
        return ""


def extract_verses_from_html(html: str, book_num: int, chapter: int) -> list[tuple[str, str]]:
    """
    Extract verses from bible.com HTML.
    Returns list of (verse_id, text) tuples.
    """
    verses = []
    
    # Look for verse spans with data-usfm attribute
    # Pattern: <span class="verse" data-usfm="GEN.1.1">...<span class="content">text</span>
    
    # Simpler approach: find all verse markers and text
    # The page has patterns like: <span class="label">1</span><span class="content">In the beginning...
    
    # Actually, let's extract from a cleaner source
    # Try to find JSON data embedded in the page
    json_match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html, re.DOTALL)
    
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            # Navigate to the chapter content
            props = data.get("props", {}).get("pageProps", {})
            chapter_info = props.get("chapterInfo")
            if chapter_info is None:
                return []  # Chapter doesn't exist in this translation
            content = chapter_info.get("content", "")
            
            if content:
                return parse_usfm_content(content, book_num, chapter)
        except json.JSONDecodeError:
            pass
    
    # Fallback: parse visible text with verse numbers
    # Remove HTML tags but keep verse number markers
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    
    # Find verse patterns (number followed by text)
    # This is fragile but works as fallback
    verse_pattern = re.compile(r'(\d{1,3})([A-Z][^0-9]{10,}?)(?=\d{1,3}[A-Z]|$)')
    
    for match in verse_pattern.finditer(text):
        verse_num = int(match.group(1))
        verse_text = match.group(2).strip()
        verse_id = f"{book_num:02d}{chapter:03d}{verse_num:03d}"
        verses.append((verse_id, verse_text))
    
    return verses


def parse_usfm_content(content: str, book_num: int, chapter: int) -> list[tuple[str, str]]:
    """Parse HTML/USFM-style content from bible.com JSON."""
    import html as html_module
    from collections import OrderedDict
    
    verse_texts = OrderedDict()  # verse_id -> list of text fragments
    
    # bible.com uses HTML with verse spans. The content can be nested in various ways:
    # - Direct: <span class="content">Text</span>
    # - Words of Jesus: <span class="wj"><span class="content">Text</span></span>
    # - Added words: <span class="add"><span class="content">Text</span></span>
    # Same verse may appear multiple times (poetry), so we merge them
    
    # Strategy: Find each verse span, then extract ALL content spans within it
    verse_span_pattern = re.compile(
        r'<span[^>]*data-usfm="[A-Z0-9]+\.(\d+)\.(\d+)"[^>]*>(.*?)</span>(?=<span[^>]*(?:class="verse|data-usfm)|</div>|$)',
        re.DOTALL
    )
    
    # Find verse boundaries more robustly: look for data-usfm markers
    # and capture until the next verse marker or end of paragraph
    verse_pattern = re.compile(r'data-usfm="[A-Z0-9]+\.(\d+)\.(\d+)"')
    
    # Split content by verse markers and capture verse numbers
    parts = re.split(r'(data-usfm="[A-Z0-9]+\.\d+\.\d+")', content)
    
    current_verse_id = None
    
    for i, part in enumerate(parts):
        match = verse_pattern.match(part)
        if match:
            chap_num = int(match.group(1))
            verse_num = int(match.group(2))
            if chap_num == chapter:
                current_verse_id = f"{book_num:02d}{chapter:03d}{verse_num:03d}"
                if current_verse_id not in verse_texts:
                    verse_texts[current_verse_id] = []
        elif current_verse_id:
            # Extract all content spans from this part
            content_matches = re.findall(r'<span class="content">([^<]*)</span>', part)
            for text in content_matches:
                text = text.strip()
                if text:
                    verse_texts[current_verse_id].append(text)
    
    # Merge fragments for each verse
    verses = []
    for verse_id, fragments in verse_texts.items():
        merged_text = " ".join(fragments)
        # Clean up extra whitespace
        merged_text = re.sub(r'\s+', ' ', merged_text).strip()
        # Decode HTML entities
        merged_text = html_module.unescape(merged_text)
        if merged_text:
            verses.append((verse_id, merged_text))
    
    # Fallback if no verses found
    if not verses:
        plain = re.sub(r'<[^>]+>', ' ', content)
        plain = re.sub(r'\s+', ' ', plain).strip()
        
        for match in re.finditer(r'(?:^|\s)(\d{1,3})\s+([A-Z][^0-9]{5,}?)(?=\s+\d{1,3}\s+[A-Z]|$)', plain):
            verse_num = int(match.group(1))
            text = match.group(2).strip()
            verse_id = f"{book_num:02d}{chapter:03d}{verse_num:03d}"
            verses.append((verse_id, text))
    
    return verses


def scrape_bible(
    version_id: int,
    iso: str,
    abbrev: str,
    name: str,
    output_dir: Path,
    books_to_scrape: list[str] | None = None,
    delay: float = 1.0,
) -> dict:
    """
    Scrape a complete Bible from bible.com.
    
    Args:
        version_id: bible.com version ID
        iso: ISO 639-3 language code
        abbrev: Bible abbreviation (e.g., KJV)
        name: Full name of the Bible
        output_dir: Directory to write output files
        books_to_scrape: Optional list of book codes to scrape (default: all)
        delay: Delay between requests in seconds
    
    Returns:
        Statistics dict
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_verses = []
    wordform_counts = Counter()
    
    books_list = BOOKS
    if books_to_scrape:
        books_list = [(code, name, chapters) for code, name, chapters in BOOKS if code in books_to_scrape]
    
    for book_idx, (book_code, book_name, num_chapters) in enumerate(books_list):
        book_num = list(BOOK_NUM_TO_CODE.keys())[list(BOOK_NUM_TO_CODE.values()).index(book_code)]
        print(f"[{book_idx + 1}/{len(books_list)}] {book_name} ({num_chapters} chapters)", flush=True)
        
        for chapter in range(1, num_chapters + 1):
            html = fetch_chapter(version_id, book_code, chapter, abbrev)
            
            if not html:
                print(f"  Chapter {chapter}: failed to fetch")
                continue
            
            verses = extract_verses_from_html(html, book_num, chapter)
            
            if verses:
                all_verses.extend(verses)
                
                # Count wordforms
                for _, text in verses:
                    words = re.findall(r'\S+', text)
                    wordform_counts.update(words)
                
                print(f"  Chapter {chapter}: {len(verses)} verses")
            else:
                print(f"  Chapter {chapter}: no verses extracted")
            
            time.sleep(delay)
    
    # Write output files
    corpus_id = f"{iso}-x-bible"
    
    # Main text file
    txt_file = output_dir / f"{corpus_id}.txt"
    with open(txt_file, "w", encoding="utf-8") as f:
        f.write(f"# language_name:\t{name}\n")
        f.write(f"# closest ISO 639-3:\t{iso}\n")
        f.write(f"# year_short:\tscraped {datetime.now().year}\n")
        f.write(f"# year_long:\tNot available\n")
        f.write(f"# title:\t{name}\n")
        f.write(f"# URL:\thttps://www.bible.com/bible/{version_id}\n")
        f.write(f"# copyright_short:\tSee bible.com for copyright information\n")
        f.write(f"# copyright_long:\tScraped from bible.com. See original source for copyright.\n")
        
        for verse_id, text in sorted(all_verses, key=lambda x: x[0]):
            f.write(f"{verse_id}\t{text}\n")
    
    # Wordforms file
    wf_file = output_dir / f"{corpus_id}.wordforms"
    with open(wf_file, "w", encoding="utf-8") as f:
        for word, count in sorted(wordform_counts.items()):
            f.write(f"{word}\t{count}\n")
    
    # Datapackage.json
    dp = {
        "title": name,
        "Corpus ID": corpus_id,
        "language_name": name,
        "closest_iso639-3": iso,
        "translation_year": "unknown",
        "source": f"https://www.bible.com/bible/{version_id}",
        "copyright": "See bible.com for copyright information",
        "copyright_long": "Scraped from bible.com. See original source for copyright.",
        "homepage": f"https://www.bible.com/bible/{version_id}",
        "version": abbrev,
        "last_modified": datetime.now().strftime("%Y-%m-%d"),
        "scraped": True,
        "scrape_date": datetime.now().isoformat(),
    }
    
    dp_file = output_dir / "datapackage.json"
    with open(dp_file, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)
    
    # README
    readme_file = output_dir / "README.md"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n\n")
        f.write(f"Scraped from bible.com version {version_id}\n\n")
        f.write(f"- ISO 639-3: {iso}\n")
        f.write(f"- Abbreviation: {abbrev}\n")
        f.write(f"- Total verses: {len(all_verses)}\n")
        f.write(f"- Unique wordforms: {len(wordform_counts)}\n")
        f.write(f"- Scraped: {datetime.now().strftime('%Y-%m-%d')}\n")
    
    stats = {
        "verses": len(all_verses),
        "unique_wordforms": len(wordform_counts),
        "total_tokens": sum(wordform_counts.values()),
    }
    
    print(f"\nDone! {stats['verses']} verses, {stats['unique_wordforms']} unique wordforms")
    return stats


def main():
    parser = argparse.ArgumentParser(description="Scrape Bible from bible.com")
    parser.add_argument("--version-id", type=int, required=True, help="bible.com version ID")
    parser.add_argument("--iso", required=True, help="ISO 639-3 language code")
    parser.add_argument("--abbrev", required=True, help="Bible abbreviation (e.g., KJV)")
    parser.add_argument("--name", required=True, help="Full name of Bible")
    parser.add_argument("--output-dir", type=Path, default=None, help="Output directory")
    parser.add_argument("--books", nargs="+", help="Specific books to scrape (e.g., MAT MRK LUK)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests (seconds)")
    
    args = parser.parse_args()
    
    if args.output_dir is None:
        args.output_dir = Path(__file__).parent.parent / "bibles" / "extracted" / args.iso
    
    scrape_bible(
        version_id=args.version_id,
        iso=args.iso,
        abbrev=args.abbrev,
        name=args.name,
        output_dir=args.output_dir,
        books_to_scrape=args.books,
        delay=args.delay,
    )


if __name__ == "__main__":
    main()
