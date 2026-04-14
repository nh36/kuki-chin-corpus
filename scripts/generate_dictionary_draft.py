#!/usr/bin/env python3
"""
Tedim Chin Draft Dictionary Export
==================================

Generates a clean draft dictionary from the backend, suitable for editorial
revision and eventual publication.

Usage:
    python scripts/generate_dictionary_draft.py [--db data/ctd_backend.db]

Output:
    output/dictionary/draft_dictionary.md

Key principles:
- One clear example per sense (not duplicated)
- Empty glosses are clearly marked as UNGLOSSED
- Clean layout that can be revised chapter by chapter
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from backend import QUALITY_ORDER_SQL
from report_utils import generate_provenance_header, format_reference


def get_connection(db_path: str):
    """Get database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_lemmas_by_letter(conn, letter):
    """Get lemmas starting with a specific letter, ordered by frequency."""
    return conn.execute('''
        SELECT 
            l.lemma_id,
            l.citation_form,
            l.pos,
            l.entry_type,
            l.primary_gloss,
            l.token_count,
            l.needs_review
        FROM lemmas l
        WHERE UPPER(SUBSTR(l.citation_form, 1, 1)) = ?
          AND l.citation_form NOT LIKE '"%'
          AND l.citation_form NOT LIKE "'%"
        ORDER BY l.token_count DESC
    ''', (letter,)).fetchall()


def get_senses_for_lemma(conn, lemma_id):
    """Get senses for a lemma, primary first."""
    return conn.execute('''
        SELECT sense_id, gloss, definition, is_primary
        FROM senses
        WHERE lemma_id = ?
        ORDER BY is_primary DESC, gloss
    ''', (lemma_id,)).fetchall()


def get_best_example(conn, sense_id):
    """Get one high-quality example for a sense using canonical quality ordering."""
    return conn.execute(f'''
        SELECT tedim_text, kjv_text, source_id
        FROM examples
        WHERE sense_id = ?
        ORDER BY {QUALITY_ORDER_SQL}
        LIMIT 1
    ''', (sense_id,)).fetchone()


def format_entry(conn, lemma):
    """Format a single dictionary entry."""
    lines = []
    
    citation = lemma['citation_form']
    pos = lemma['pos'] or '?'
    freq = lemma['token_count']
    primary_gloss = lemma['primary_gloss']
    
    # Determine status
    needs_gloss = not primary_gloss or primary_gloss == '?' or primary_gloss == ''
    
    # Entry header
    if needs_gloss:
        lines.append(f"**{citation}** *{pos}* — **UNGLOSSED** (freq: {freq:,})")
    else:
        lines.append(f"**{citation}** *{pos}* — {primary_gloss} (freq: {freq:,})")
    
    # Get senses
    senses = get_senses_for_lemma(conn, lemma['lemma_id'])
    
    if len(senses) > 1:
        # Multiple senses - list them
        lines.append('')
        for i, sense in enumerate(senses, 1):
            gloss = sense['gloss'] or '?'
            marker = '●' if sense['is_primary'] else '○'
            lines.append(f"  {marker} {i}. {gloss}")
            
            # One example per sense
            ex = get_best_example(conn, sense['sense_id'])
            if ex and ex['tedim_text']:
                tedim = ex['tedim_text'][:80] + '...' if len(ex['tedim_text']) > 80 else ex['tedim_text']
                lines.append(f"    — *{tedim}*")
    elif senses:
        # Single sense - just show one example
        ex = get_best_example(conn, senses[0]['sense_id'])
        if ex and ex['tedim_text']:
            tedim = ex['tedim_text'][:80] + '...' if len(ex['tedim_text']) > 80 else ex['tedim_text']
            lines.append(f"  — *{tedim}*")
    
    lines.append('')
    return '\n'.join(lines)


def get_glossed_lemmas_by_letter(conn, letter):
    """Get glossed lemmas starting with a specific letter."""
    return conn.execute('''
        SELECT 
            l.lemma_id, l.citation_form, l.pos, l.entry_type,
            l.primary_gloss, l.token_count, l.needs_review
        FROM lemmas l
        WHERE UPPER(SUBSTR(l.citation_form, 1, 1)) = ?
          AND l.citation_form NOT LIKE '"%'
          AND l.citation_form NOT LIKE "'%"
          AND l.primary_gloss IS NOT NULL
          AND l.primary_gloss != ''
          AND l.primary_gloss NOT LIKE '%?%'
        ORDER BY l.token_count DESC
    ''', (letter,)).fetchall()


def get_unglossed_lemmas(conn, limit=100):
    """Get unglossed lemmas ordered by frequency."""
    return conn.execute('''
        SELECT 
            l.lemma_id, l.citation_form, l.pos, l.entry_type,
            l.primary_gloss, l.token_count, l.needs_review
        FROM lemmas l
        WHERE l.primary_gloss IS NULL
           OR l.primary_gloss = ''
           OR l.primary_gloss LIKE '%?%'
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def generate_dictionary_draft(conn) -> str:
    """Generate the complete dictionary draft."""
    
    provenance = generate_provenance_header(
        'scripts/generate_dictionary_draft.py',
        ['data/ctd_backend.db'],
        'make dictionary-draft'
    )
    
    # Get statistics
    total_lemmas = conn.execute('SELECT COUNT(*) FROM lemmas').fetchone()[0]
    glossed_count = conn.execute('''
        SELECT COUNT(*) FROM lemmas
        WHERE primary_gloss IS NOT NULL 
          AND primary_gloss != '' 
          AND primary_gloss NOT LIKE '%?%'
    ''').fetchone()[0]
    unclear_count = total_lemmas - glossed_count
    
    lines = [provenance, '']
    lines.append('# Tedim Chin Dictionary Draft')
    lines.append('')
    lines.append(f'Generated: {datetime.now().strftime("%Y-%m-%d")}')
    lines.append('')
    lines.append(f'**{glossed_count:,} glossed entries** | {unclear_count:,} unresolved (see end)')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # Part 1: Glossed entries by letter
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    for letter in letters:
        lemmas = get_glossed_lemmas_by_letter(conn, letter)
        
        if not lemmas:
            continue
        
        lines.append(f'## {letter}')
        lines.append('')
        
        for lemma in lemmas:
            entry = format_entry(conn, lemma)
            lines.append(entry)
        
        lines.append('---')
        lines.append('')
    
    # Part 2: Unresolved entries (separate section)
    lines.append('# UNRESOLVED ENTRIES')
    lines.append('')
    lines.append('The following entries need glosses assigned before publication.')
    lines.append('Sorted by corpus frequency (highest first).')
    lines.append('')
    
    unglossed = get_unglossed_lemmas(conn, limit=200)
    
    lines.append('| Rank | Form | POS | Tokens | Current |')
    lines.append('|------|------|-----|--------|---------|')
    for i, lemma in enumerate(unglossed, 1):
        current = lemma['primary_gloss'] or '(empty)'
        lines.append(f"| {i} | **{lemma['citation_form']}** | {lemma['pos'] or '?'} | {lemma['token_count']:,} | {current} |")
    
    if unclear_count > 200:
        lines.append(f"\n*({unclear_count - 200} more unresolved entries not shown)*")
    
    lines.append('')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate Tedim dictionary draft')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Path to backend database')
    parser.add_argument('--output', default='output/dictionary/draft_dictionary.md', help='Output path')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        sys.exit(1)
    
    print(f"Loading backend from {args.db}...")
    conn = get_connection(args.db)
    
    print("Generating dictionary draft...")
    report = generate_dictionary_draft(conn)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"  → {args.output}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
