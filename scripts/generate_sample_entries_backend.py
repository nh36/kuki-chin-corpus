#!/usr/bin/env python3
"""
Generate Sample Dictionary Entries from Backend

Backend-based dictionary output generator for Tedim Chin.
Produces structured dictionary entries with senses, wordforms, frequencies, and ranked examples.

Usage:
    python scripts/generate_sample_entries_backend.py
    python scripts/generate_sample_entries_backend.py --lemma pai
    python scripts/generate_sample_entries_backend.py --pos V --limit 20
    python scripts/generate_sample_entries_backend.py --output output/sample_entries.md
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import Backend, Lemma, Sense, Example
from report_utils import format_reference


def format_entry(db: Backend, lemma: Lemma, 
                 include_wordforms: bool = True,
                 include_examples: bool = True,
                 max_examples: int = 3) -> List[str]:
    """Format a single dictionary entry from backend data."""
    lines = []
    
    # Headword
    lines.append(f"## {lemma.citation_form}")
    lines.append("")
    
    # Basic info line
    pos_str = lemma.pos or "?"
    type_badge = ""
    if lemma.entry_type == 'grammatical':
        type_badge = " [GRAM]"
    elif lemma.entry_type == 'mixed':
        type_badge = " [MIXED]"
    
    lines.append(f"**{pos_str}**{type_badge} | freq: {lemma.token_count:,} | forms: {lemma.form_count}")
    lines.append("")
    
    # Primary gloss
    lines.append(f"'{lemma.primary_gloss}'")
    lines.append("")
    
    # Senses
    senses = db.get_senses(lemma.lemma_id)
    if len(senses) > 1:
        lines.append("### Senses")
        lines.append("")
        for sense in senses:
            primary_marker = " ★" if sense.is_primary else ""
            type_marker = f" [{sense.usage_type}]" if sense.usage_type != 'lexical' else ""
            lines.append(f"**{sense.sense_num}.** {sense.gloss}{type_marker}{primary_marker}")
            if sense.definition:
                lines.append(f"   {sense.definition}")
            lines.append(f"   *freq: {sense.frequency:,}*")
            lines.append("")
    
    # Wordforms
    if include_wordforms:
        wordforms = db.get_wordforms_for_lemma(lemma.lemma_id)
        if wordforms:
            lines.append("### Forms")
            lines.append("")
            # Show top forms by frequency
            top_forms = sorted(wordforms, key=lambda w: -w['frequency'])[:10]
            forms_str = ", ".join(f"{w['surface']} ({w['frequency']:,})" for w in top_forms)
            lines.append(forms_str)
            if len(wordforms) > 10:
                lines.append(f"*... and {len(wordforms) - 10} more forms*")
            lines.append("")
    
    # Examples
    if include_examples:
        examples = db.get_examples_for_lemma(lemma.lemma_id, limit=max_examples)
        if examples:
            lines.append("### Examples")
            lines.append("")
            for ex in examples:
                ref = format_reference(ex.source_id)
                quality_badge = f" [{ex.quality}]" if ex.quality != 'good' else ""
                lines.append(f"**{ref}**{quality_badge}")
                lines.append(f"> {ex.tedim_text}")
                if ex.segmented:
                    lines.append(f"> *{ex.segmented}*")
                if ex.glossed:
                    lines.append(f"> {ex.glossed}")
                if ex.kjv_text:
                    lines.append(f"> '{ex.kjv_text}'")
                lines.append("")
    
    # Notes
    if lemma.notes:
        lines.append(f"*Note: {lemma.notes}*")
        lines.append("")
    
    # Review flag
    if lemma.needs_review:
        lines.append("⚠️ *Needs review*")
        lines.append("")
    
    lines.append("---")
    lines.append("")
    
    return lines


def generate_sample_entries(db: Backend, 
                            pos: Optional[str] = None,
                            entry_type: Optional[str] = None,
                            lemmas: Optional[List[str]] = None,
                            limit: int = 20,
                            include_wordforms: bool = True,
                            include_examples: bool = True) -> List[str]:
    """Generate sample dictionary entries from backend."""
    lines = []
    
    # Header
    lines.append("# Tedim Chin Sample Dictionary Entries")
    lines.append("")
    lines.append("Generated from the corpus backend. Each entry includes senses,")
    lines.append("wordforms, frequencies, and ranked example sentences.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Get lemmas
    if lemmas:
        # Specific lemmas requested
        entries = []
        for lemma_id in lemmas:
            lemma = db.get_lemma(lemma_id)
            if lemma:
                entries.append(lemma)
    else:
        # Filter by POS/type
        entries = db.get_lemmas_by_pos(pos or 'V', entry_type=entry_type, limit=limit)
    
    # Statistics
    lines.append(f"## Statistics")
    lines.append("")
    lines.append(f"- **Entries shown:** {len(entries)}")
    if pos:
        lines.append(f"- **POS filter:** {pos}")
    if entry_type:
        lines.append(f"- **Type filter:** {entry_type}")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Generate entries
    for lemma in entries:
        entry_lines = format_entry(db, lemma, 
                                   include_wordforms=include_wordforms,
                                   include_examples=include_examples)
        lines.extend(entry_lines)
    
    # Footer
    lines.append("*Generated from backend database.*")
    
    return lines


def main():
    parser = argparse.ArgumentParser(description='Generate sample dictionary entries')
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--output', default='output/sample_entries.md',
                        help='Output file path')
    parser.add_argument('--lemma', action='append', dest='lemmas',
                        help='Specific lemma(s) to generate (can repeat)')
    parser.add_argument('--pos', default=None,
                        help='Filter by POS (e.g., V, N, ADJ)')
    parser.add_argument('--type', dest='entry_type', default=None,
                        help='Filter by entry type (lexical, grammatical, mixed)')
    parser.add_argument('--limit', type=int, default=20,
                        help='Maximum entries to generate')
    parser.add_argument('--no-wordforms', action='store_true',
                        help='Omit wordform lists')
    parser.add_argument('--no-examples', action='store_true',
                        help='Omit example sentences')
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate entries
    db = Backend(args.db)
    lines = generate_sample_entries(
        db,
        pos=args.pos,
        entry_type=args.entry_type,
        lemmas=args.lemmas,
        limit=args.limit,
        include_wordforms=not args.no_wordforms,
        include_examples=not args.no_examples
    )
    
    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Sample entries written to {args.output}")
    print(f"  {len(lines)} lines")


if __name__ == '__main__':
    main()
