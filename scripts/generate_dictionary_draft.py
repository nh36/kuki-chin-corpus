#!/usr/bin/env python3
"""
Tedim Chin Draft Dictionary Export
==================================

Generates a complete draft dictionary from the backend, suitable for review
and eventual publication.

Usage:
    python scripts/generate_dictionary_draft.py [--db data/ctd_backend.db]

Output:
    output/dictionary/draft_dictionary.md

Features:
- Headwords ordered by frequency (most common first)
- POS tags and grammatical information
- Primary and secondary senses
- Usage type (lexical/grammatical)
- Frequency statistics
- Representative examples
- Review flags where data is incomplete

Publication Readiness Criteria:
- Draft ready = can export a coherent, revisable dictionary with stable structure
- Uncertain items are marked visibly, not silently omitted
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent))
from report_utils import generate_provenance_header, format_reference


def get_connection(db_path: str):
    """Get database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_lemmas_by_frequency(conn, limit=None):
    """Get all lemmas ordered by frequency."""
    query = '''
        SELECT 
            l.lemma_id,
            l.citation_form,
            l.pos,
            l.entry_type,
            l.primary_gloss,
            l.token_count,
            l.form_count,
            l.is_polysemous,
            l.needs_review,
            l.notes
        FROM lemmas l
        ORDER BY l.token_count DESC
    '''
    if limit:
        query += f' LIMIT {limit}'
    return conn.execute(query).fetchall()


def get_senses_for_lemma(conn, lemma_id):
    """Get all senses for a lemma."""
    return conn.execute('''
        SELECT 
            sense_id,
            gloss,
            definition,
            notes,
            usage_type,
            is_primary
        FROM senses
        WHERE lemma_id = ?
        ORDER BY is_primary DESC, sense_id
    ''', (lemma_id,)).fetchall()


def get_examples_for_sense(conn, sense_id, limit=3):
    """Get examples for a sense."""
    return conn.execute('''
        SELECT 
            e.example_id,
            e.source_id,
            e.tedim_text,
            e.kjv_text,
            e.target_form,
            e.segmented,
            e.glossed,
            e.quality
        FROM examples e
        WHERE e.sense_id = ?
        ORDER BY 
            CASE e.quality
                WHEN 'canonical' THEN 1
                WHEN 'excellent' THEN 2
                WHEN 'good' THEN 3
                WHEN 'transparent' THEN 4
                WHEN 'shortest' THEN 5
                WHEN 'acceptable' THEN 6
                ELSE 7
            END
        LIMIT ?
    ''', (sense_id, limit)).fetchall()


def get_wordforms_for_lemma(conn, lemma_id, limit=10):
    """Get attested wordforms for a lemma."""
    return conn.execute('''
        SELECT 
            surface,
            segmentation,
            gloss,
            frequency
        FROM wordforms
        WHERE lemma_id = ?
        ORDER BY frequency DESC
        LIMIT ?
    ''', (lemma_id, limit)).fetchall()


def format_example(example, show_verse=True):
    """Format an example for display."""
    lines = []
    
    # Tedim text with target highlighted
    tedim = example['tedim_text'] or ''
    target = example['target_form'] or ''
    if target and target in tedim:
        tedim = tedim.replace(target, f"**{target}**", 1)
    
    lines.append(f"- {tedim}")
    
    # Gloss if available
    if example['segmented'] and example['glossed']:
        lines.append(f"  - *{example['segmented']}* → '{example['glossed']}'")
    
    # English translation
    if example['kjv_text']:
        lines.append(f"  - '{example['kjv_text']}'")
    
    # Verse reference
    if show_verse and example['source_id']:
        lines.append(f"  - ({format_reference(example['source_id'])})")
    
    return '\n'.join(lines)


def has_incomplete_data(lemma, senses):
    """Check if a lemma entry has incomplete data that needs review."""
    issues = []
    
    # Check primary gloss
    if not lemma['primary_gloss'] or '?' in (lemma['primary_gloss'] or ''):
        issues.append('unclear gloss')
    
    # Check POS
    if not lemma['pos'] or lemma['pos'] == '?':
        issues.append('missing POS')
    
    # Check for any sense definitions
    if not senses:
        issues.append('no senses')
    
    # Check for examples
    # (This would need another query, simplified here)
    
    if lemma['needs_review']:
        issues.append('flagged for review')
    
    return issues


def generate_dictionary_entry(conn, lemma, include_examples=True):
    """Generate a complete dictionary entry for one lemma."""
    lines = []
    
    senses = get_senses_for_lemma(conn, lemma['lemma_id'])
    wordforms = get_wordforms_for_lemma(conn, lemma['lemma_id'])
    issues = has_incomplete_data(lemma, senses)
    
    # Entry header
    pos_tag = lemma['pos'] or '?'
    entry_type = lemma['entry_type'] or 'lexical'
    
    # Review flag if needed
    review_flag = ' ⚠️' if issues else ''
    
    lines.append(f"### {lemma['citation_form']}{review_flag}")
    lines.append('')
    lines.append(f"**{pos_tag}** | {entry_type} | freq: {lemma['token_count']:,}")
    
    if issues:
        lines.append('')
        lines.append(f"*Review needed: {', '.join(issues)}*")
    
    lines.append('')
    
    # Primary gloss
    primary = lemma['primary_gloss'] or '?'
    lines.append(f"**Primary gloss:** {primary}")
    lines.append('')
    
    # All senses
    if senses:
        lines.append('**Senses:**')
        for i, sense in enumerate(senses, 1):
            primary_marker = ' (primary)' if sense['is_primary'] else ''
            gloss = sense['gloss'] or '?'
            lines.append(f"{i}. {gloss}{primary_marker}")
            
            if sense['definition']:
                lines.append(f"   - {sense['definition']}")
            
            if sense['notes']:
                lines.append(f"   - *{sense['notes']}*")
            
            # Examples for this sense
            if include_examples:
                examples = get_examples_for_sense(conn, sense['sense_id'], limit=2)
                if examples:
                    lines.append('')
                    for ex in examples:
                        lines.append(format_example(ex, show_verse=True))
        lines.append('')
    
    # Attested forms
    if wordforms:
        lines.append('**Attested forms:**')
        forms_str = ', '.join(
            f"{w['surface']} ({w['frequency']})" 
            for w in wordforms[:5]
        )
        lines.append(forms_str)
        lines.append('')
    
    lines.append('---')
    lines.append('')
    
    return '\n'.join(lines)


def generate_dictionary_draft(conn, limit=None) -> str:
    """Generate the complete dictionary draft."""
    
    provenance = generate_provenance_header(
        'scripts/generate_dictionary_draft.py',
        ['data/ctd_backend.db'],
        'make dictionary-draft'
    )
    
    # Get statistics
    total_lemmas = conn.execute('SELECT COUNT(*) FROM lemmas').fetchone()[0]
    total_senses = conn.execute('SELECT COUNT(*) FROM senses').fetchone()[0]
    lemmas_with_examples = conn.execute('''
        SELECT COUNT(DISTINCT s.lemma_id) FROM senses s
        JOIN examples e ON s.sense_id = e.sense_id
    ''').fetchone()[0]
    
    # Count entries with issues
    unclear_count = conn.execute('''
        SELECT COUNT(*) FROM lemmas
        WHERE primary_gloss LIKE '%?%' OR primary_gloss IS NULL OR primary_gloss = ''
    ''').fetchone()[0]
    
    lines = [provenance]
    lines.append('# Tedim Chin Draft Dictionary')
    lines.append('')
    lines.append(f'**Generated:** {datetime.now().isoformat()}')
    lines.append('')
    
    # Statistics section
    lines.append('## Dictionary Statistics')
    lines.append('')
    lines.append(f'- **Total headwords:** {total_lemmas:,}')
    lines.append(f'- **Total senses:** {total_senses:,}')
    lines.append(f'- **Headwords with examples:** {lemmas_with_examples:,}')
    lines.append(f'- **Entries needing review:** {unclear_count:,}')
    lines.append('')
    
    # Publication readiness
    readiness_pct = 100 * (total_lemmas - unclear_count) / total_lemmas if total_lemmas > 0 else 0
    lines.append('## Publication Readiness')
    lines.append('')
    lines.append(f'- **Entries with complete data:** {readiness_pct:.1f}%')
    lines.append(f'- **Entries marked ⚠️:** need review before publication')
    lines.append('')
    
    # Legend
    lines.append('## Legend')
    lines.append('')
    lines.append('- **⚠️** = Entry needs editorial review')
    lines.append('- **freq:** = Token count in corpus')
    lines.append('- **POS tags:** N=noun, V=verb, ADJ=adjective, ADV=adverb, PRON=pronoun,')
    lines.append('  DET=determiner, CONJ=conjunction, FUNC=function word, PROP=proper noun')
    lines.append('')
    lines.append('---')
    lines.append('')
    
    # Dictionary entries
    lines.append('## Entries')
    lines.append('')
    
    lemmas = get_lemmas_by_frequency(conn, limit=limit)
    
    # Group by first letter
    current_letter = None
    for lemma in lemmas:
        first_letter = (lemma['citation_form'] or 'A')[0].upper()
        
        if first_letter != current_letter:
            current_letter = first_letter
            lines.append(f'## {current_letter}')
            lines.append('')
        
        entry = generate_dictionary_entry(conn, lemma, include_examples=True)
        lines.append(entry)
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Tedim dictionary draft'
    )
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--output', default='output/dictionary/draft_dictionary.md',
                        help='Output path')
    parser.add_argument('--limit', type=int, default=None,
                        help='Limit number of entries (for testing)')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        sys.exit(1)
    
    print(f"Loading backend from {args.db}...")
    conn = get_connection(args.db)
    
    print("Generating dictionary draft...")
    report = generate_dictionary_draft(conn, limit=args.limit)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"  → {args.output}")
    
    # Print summary
    total_lines = len(report.split('\n'))
    print(f"  → {total_lines:,} lines generated")
    
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
