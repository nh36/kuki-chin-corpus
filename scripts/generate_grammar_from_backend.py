#!/usr/bin/env python3
"""
Generate grammar documentation from the backend constructions layer.

This script generates markdown grammar reports organized by grammar topics,
with constructions and examples pulled from the backend database.
"""

import sqlite3
import json
import argparse
from pathlib import Path


def format_example(example: dict) -> str:
    """Format an example for display."""
    lines = []
    if example.get('tedim_text'):
        lines.append(f"> {example['tedim_text']}")
    if example.get('segmented'):
        lines.append(f"> *{example['segmented']}*")
    if example.get('glossed'):
        lines.append(f"> {example['glossed']}")
    if example.get('kjv_text'):
        lines.append(f"> '{example['kjv_text']}'")
    return '\n'.join(lines)


def generate_construction_section(conn, construction_id: str) -> str:
    """Generate markdown section for a construction."""
    row = conn.execute('''
        SELECT name, category, pattern, description, morpheme_ids, frequency, example_ids
        FROM constructions WHERE construction_id = ?
    ''', (construction_id,)).fetchone()
    
    if not row:
        return ""
    
    name, category, pattern, description, morpheme_ids_json, frequency, example_ids_json = row
    
    lines = [
        f"### {name}",
        "",
        f"**Pattern:** `{pattern}`",
        "",
        description,
        "",
        f"**Frequency:** ~{frequency:,}",
        "",
    ]
    
    # Add morphemes involved
    if morpheme_ids_json and morpheme_ids_json != '[]':
        morpheme_ids = json.loads(morpheme_ids_json)
        morphemes = []
        for mid in morpheme_ids:
            mrow = conn.execute('''
                SELECT form, gloss FROM grammatical_morphemes WHERE morpheme_id = ?
            ''', (mid,)).fetchone()
            if mrow:
                morphemes.append(f"-{mrow[0]} ({mrow[1]})")
        if morphemes:
            lines.append(f"**Morphemes:** {', '.join(morphemes)}")
            lines.append("")
    
    # Add examples
    if example_ids_json and example_ids_json != '[]':
        example_ids = json.loads(example_ids_json)
        lines.append("**Examples:**")
        lines.append("")
        
        for eid in example_ids[:3]:
            ex = conn.execute('''
                SELECT source_id, tedim_text, segmented, glossed, kjv_text
                FROM examples WHERE example_id = ?
            ''', (eid,)).fetchone()
            if ex:
                src_row = conn.execute('''
                    SELECT book_code, chapter, verse FROM sources WHERE source_id = ?
                ''', (ex[0],)).fetchone()
                if src_row:
                    ref = f"({src_row[0]} {src_row[1]}:{src_row[2]})"
                else:
                    ref = ""
                
                lines.append(f"**{ref}**")
                if ex[1]:
                    lines.append(f"> {ex[1][:100]}{'...' if len(ex[1]) > 100 else ''}")
                if ex[4]:
                    lines.append(f"> *'{ex[4][:80]}...'*" if len(ex[4]) > 80 else f"> *'{ex[4]}'*")
                lines.append("")
    
    return '\n'.join(lines)


def generate_topic_section(conn, topic_id: str, level: int = 2) -> str:
    """Generate markdown section for a grammar topic."""
    row = conn.execute('''
        SELECT title, description, construction_ids, morpheme_ids
        FROM grammar_topics WHERE topic_id = ?
    ''', (topic_id,)).fetchone()
    
    if not row:
        return ""
    
    title, description, construction_ids_json, morpheme_ids_json = row
    
    heading = '#' * level
    lines = [
        f"{heading} {title}",
        "",
        description,
        "",
    ]
    
    # Add constructions
    if construction_ids_json and construction_ids_json != '[]':
        construction_ids = json.loads(construction_ids_json)
        for cid in construction_ids:
            section = generate_construction_section(conn, cid)
            if section:
                lines.append(section)
                lines.append("")
    
    # Add child topics
    children = list(conn.execute('''
        SELECT topic_id FROM grammar_topics 
        WHERE parent_id = ? ORDER BY display_order
    ''', (topic_id,)))
    
    for child in children:
        child_section = generate_topic_section(conn, child[0], level + 1)
        if child_section:
            lines.append(child_section)
    
    return '\n'.join(lines)


def generate_full_grammar(conn) -> str:
    """Generate full grammar documentation."""
    lines = [
        "# Tedim Chin Grammar",
        "",
        "Generated from corpus backend with constructions and examples.",
        "",
        "---",
        "",
    ]
    
    # Get top-level topics
    topics = list(conn.execute('''
        SELECT topic_id FROM grammar_topics 
        WHERE parent_id IS NULL ORDER BY display_order
    '''))
    
    for topic in topics:
        section = generate_topic_section(conn, topic[0])
        if section:
            lines.append(section)
            lines.append("---")
            lines.append("")
    
    # Add construction inventory
    lines.append("## Construction Inventory")
    lines.append("")
    lines.append("| ID | Name | Category | Pattern | Frequency |")
    lines.append("|---|---|---|---|---|")
    
    for row in conn.execute('''
        SELECT construction_id, name, category, pattern, frequency
        FROM constructions ORDER BY category, frequency DESC
    '''):
        lines.append(f"| {row[0]} | {row[1]} | {row[2]} | `{row[3]}` | {row[4]:,} |")
    
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated from backend database*")
    
    return '\n'.join(lines)


def generate_constructions_report(conn) -> str:
    """Generate a focused constructions report."""
    lines = [
        "# Tedim Chin Constructions",
        "",
        "This report documents grammatical constructions in Tedim Chin,",
        "organized by category with pattern descriptions and corpus examples.",
        "",
        "---",
        "",
    ]
    
    # Get categories
    categories = list(conn.execute('''
        SELECT DISTINCT category FROM constructions ORDER BY category
    '''))
    
    for cat in categories:
        cat_name = cat[0].replace('_', ' ').title()
        lines.append(f"## {cat_name}")
        lines.append("")
        
        constructions = list(conn.execute('''
            SELECT construction_id FROM constructions 
            WHERE category = ? ORDER BY frequency DESC
        ''', (cat[0],)))
        
        for c in constructions:
            section = generate_construction_section(conn, c[0])
            if section:
                lines.append(section)
                lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate grammar documentation from backend')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Database path')
    parser.add_argument('--output', default='output/grammar_constructions.md', help='Output file')
    parser.add_argument('--full', action='store_true', help='Generate full grammar (vs constructions only)')
    args = parser.parse_args()
    
    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    
    if args.full:
        content = generate_full_grammar(conn)
    else:
        content = generate_constructions_report(conn)
    
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content)
    
    print(f"Generated {args.output}")
    
    # Print stats
    print(f"\nStats:")
    print(f"  Constructions: {conn.execute('SELECT COUNT(*) FROM constructions').fetchone()[0]}")
    print(f"  Grammar topics: {conn.execute('SELECT COUNT(*) FROM grammar_topics').fetchone()[0]}")
    print(f"  With examples: {conn.execute('SELECT COUNT(*) FROM constructions WHERE example_ids IS NOT NULL').fetchone()[0]}")
    
    conn.close()


if __name__ == '__main__':
    main()
