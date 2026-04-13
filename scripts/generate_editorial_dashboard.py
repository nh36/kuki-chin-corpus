#!/usr/bin/env python3
"""
Tedim Chin Editorial Dashboard
==============================

Generates a ranked report of editorial priorities for dictionary and grammar work.
This is the key tool for focusing editorial effort where it matters most.

Usage:
    python scripts/generate_editorial_dashboard.py [--db data/ctd_backend.db]

Output:
    output/editorial_dashboard.md

The dashboard includes:
1. High-frequency unresolved lemmas
2. Mixed lexical/grammatical items
3. Unstable gloss assignments
4. Weak example linkages
5. Publication blockers vs cosmetic issues
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from report_utils import generate_provenance_header, format_reference


def get_connection(db_path: str):
    """Get database connection."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def get_high_freq_polysemous(conn, limit=50):
    """Get high-frequency lemmas with multiple senses (need disambiguation)."""
    return conn.execute('''
        SELECT 
            l.lemma_id,
            l.citation_form,
            l.pos,
            l.primary_gloss,
            l.token_count,
            COUNT(DISTINCT s.sense_id) as sense_count,
            GROUP_CONCAT(DISTINCT s.gloss) as all_glosses
        FROM lemmas l
        JOIN senses s ON l.lemma_id = s.lemma_id
        GROUP BY l.lemma_id
        HAVING sense_count > 1
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_mixed_lex_gram(conn, limit=30):
    """Get items that appear both as lexical and grammatical."""
    return conn.execute('''
        SELECT 
            l.lemma_id,
            l.citation_form,
            l.pos,
            l.primary_gloss,
            l.token_count,
            gm.category as gram_category,
            gm.gloss as gram_gloss,
            gm.frequency as gram_freq
        FROM lemmas l
        JOIN grammatical_morphemes gm ON LOWER(l.citation_form) = LOWER(gm.form)
        WHERE l.entry_type = 'lexical' OR l.entry_type IS NULL
        ORDER BY l.token_count + gm.frequency DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_senses_without_examples(conn, min_freq=100, limit=50):
    """Get high-frequency senses that lack examples."""
    return conn.execute('''
        SELECT 
            s.sense_id,
            s.lemma_id,
            s.gloss,
            l.token_count,
            l.citation_form,
            l.pos
        FROM senses s
        JOIN lemmas l ON s.lemma_id = l.lemma_id
        LEFT JOIN examples e ON s.sense_id = e.sense_id
        WHERE e.example_id IS NULL
          AND l.token_count >= ?
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (min_freq, limit)).fetchall()


def get_ambiguous_wordforms(conn, limit=50):
    """Get wordforms with is_ambiguous flag that have high frequency."""
    return conn.execute('''
        SELECT 
            w.wordform_id,
            w.surface,
            w.lemma_id,
            w.pos,
            w.gloss,
            w.frequency,
            w.is_ambiguous
        FROM wordforms w
        WHERE w.is_ambiguous = 1
        ORDER BY w.frequency DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_unstable_glosses(conn, limit=30):
    """
    Get lemmas where the same form has different glosses across wordforms.
    This indicates potentially inconsistent analysis.
    """
    return conn.execute('''
        SELECT 
            l.lemma_id,
            l.citation_form,
            l.pos,
            l.token_count,
            COUNT(DISTINCT w.gloss) as gloss_variants,
            GROUP_CONCAT(DISTINCT w.gloss) as glosses
        FROM lemmas l
        JOIN wordforms w ON l.lemma_id = w.lemma_id
        WHERE w.gloss IS NOT NULL AND w.gloss != ''
        GROUP BY l.lemma_id
        HAVING gloss_variants > 2
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_review_queue_by_priority(conn):
    """Get review queue items grouped by priority."""
    high = conn.execute('''
        SELECT entity_type, entity_id, reason, resolution
        FROM review_queue
        WHERE priority = 'high' AND resolution IS NULL
        ORDER BY entity_type, entity_id
    ''').fetchall()
    
    medium = conn.execute('''
        SELECT entity_type, entity_id, reason, resolution
        FROM review_queue
        WHERE priority = 'medium' AND resolution IS NULL
        ORDER BY entity_type, entity_id
        LIMIT 50
    ''').fetchall()
    
    return high, medium


def categorize_blockers(conn):
    """
    Categorize issues into dictionary blockers, grammar blockers, and cosmetic.
    
    Dictionary blocker: would materially damage a printed dictionary
    Grammar blocker: would materially damage a grammar description
    Cosmetic: low-priority cleanup
    """
    blockers = {
        'dictionary': [],
        'grammar': [],
        'cosmetic': []
    }
    
    # Dictionary blockers: high-freq lemmas with unclear primary gloss
    unclear_glosses = conn.execute('''
        SELECT lemma_id, citation_form, primary_gloss, token_count
        FROM lemmas
        WHERE (primary_gloss LIKE '%?%' OR primary_gloss IS NULL OR primary_gloss = '')
          AND token_count > 100
        ORDER BY token_count DESC
        LIMIT 20
    ''').fetchall()
    
    for row in unclear_glosses:
        blockers['dictionary'].append({
            'type': 'unclear_gloss',
            'lemma': row['lemma_id'],
            'citation': row['citation_form'],
            'gloss': row['primary_gloss'],
            'freq': row['token_count'],
        })
    
    # Grammar blockers: grammatical morphemes without clear analysis
    unclear_morphemes = conn.execute('''
        SELECT form, gloss, category, frequency
        FROM grammatical_morphemes
        WHERE gloss LIKE '%?%' OR category IS NULL OR category = ''
        ORDER BY frequency DESC
        LIMIT 20
    ''').fetchall()
    
    for row in unclear_morphemes:
        blockers['grammar'].append({
            'type': 'unclear_morpheme',
            'morpheme': row['form'],
            'gloss': row['gloss'],
            'category': row['category'],
            'freq': row['frequency'],
        })
    
    return blockers


def generate_dashboard(conn) -> str:
    """Generate the complete editorial dashboard."""
    
    provenance = generate_provenance_header(
        'scripts/generate_editorial_dashboard.py',
        ['data/ctd_backend.db'],
        'make editorial-dashboard'
    )
    
    lines = [provenance]
    lines.append('# Tedim Chin Editorial Dashboard')
    lines.append('')
    lines.append(f'**Generated:** {datetime.now().isoformat()}')
    lines.append('')
    lines.append('This dashboard highlights editorial priorities for dictionary and grammar work.')
    lines.append('Focus on items at the top of each section first.')
    lines.append('')
    
    # Summary statistics
    stats = {}
    stats['total_lemmas'] = conn.execute('SELECT COUNT(*) FROM lemmas').fetchone()[0]
    stats['polysemous_lemmas'] = conn.execute('''
        SELECT COUNT(DISTINCT lemma_id) FROM senses 
        GROUP BY lemma_id HAVING COUNT(*) > 1
    ''').fetchone()
    stats['polysemous_lemmas'] = stats['polysemous_lemmas'][0] if stats['polysemous_lemmas'] else 0
    
    lines.append('## Summary')
    lines.append('')
    lines.append(f'- Total lemmas: {stats["total_lemmas"]:,}')
    lines.append(f'- Polysemous lemmas: {stats["polysemous_lemmas"]:,}')
    lines.append('')
    
    # High-frequency polysemous lemmas
    lines.append('---')
    lines.append('')
    lines.append('## 1. High-Frequency Polysemous Lemmas')
    lines.append('')
    lines.append('These lemmas have multiple senses and high frequency. Focus disambiguation here first.')
    lines.append('')
    lines.append('| Lemma | POS | Frequency | Senses | Glosses |')
    lines.append('|-------|-----|-----------|--------|---------|')
    
    for row in get_high_freq_polysemous(conn, 30):
        glosses = row['all_glosses'][:60] + '...' if len(row['all_glosses'] or '') > 60 else row['all_glosses']
        lines.append(
            f"| {row['citation_form']} | {row['pos']} | {row['token_count']:,} | "
            f"{row['sense_count']} | {glosses} |"
        )
    
    # Mixed lexical/grammatical
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 2. Mixed Lexical/Grammatical Items')
    lines.append('')
    lines.append('These items appear both as lexemes and as grammatical morphemes.')
    lines.append('Clarify whether they are fundamentally lexical (with grammaticalized uses)')
    lines.append('or fundamentally grammatical (with lexical origins).')
    lines.append('')
    
    mixed = get_mixed_lex_gram(conn, 20)
    if mixed:
        lines.append('| Form | Lexical POS | Lexical Gloss | Freq | Gram Category | Gram Gloss | Gram Freq |')
        lines.append('|------|-------------|---------------|------|---------------|------------|-----------|')
        for row in mixed:
            lines.append(
                f"| {row['citation_form']} | {row['pos']} | {row['primary_gloss']} | "
                f"{row['token_count']:,} | {row['gram_category']} | {row['gram_gloss']} | "
                f"{row['gram_freq']:,} |"
            )
    else:
        lines.append('*No mixed items found.*')
    
    # Senses without examples
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 3. High-Frequency Senses Without Examples')
    lines.append('')
    lines.append('These senses have no linked examples but high token frequency.')
    lines.append('Adding examples improves both dictionary and grammar quality.')
    lines.append('')
    
    no_examples = get_senses_without_examples(conn, 100, 30)
    if no_examples:
        lines.append('| Sense ID | Lemma | POS | Gloss | Frequency |')
        lines.append('|----------|-------|-----|-------|-----------|')
        for row in no_examples:
            lines.append(
                f"| {row['sense_id']} | {row['citation_form']} | {row['pos']} | "
                f"{row['gloss']} | {row['token_count']:,} |"
            )
    else:
        lines.append('*All high-frequency senses have examples. ✓*')
    
    # Unstable glosses
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 4. Lemmas with Unstable Glosses')
    lines.append('')
    lines.append('These lemmas have inconsistent glosses across wordforms.')
    lines.append('Consolidate to a consistent primary gloss.')
    lines.append('')
    
    unstable = get_unstable_glosses(conn, 20)
    if unstable:
        lines.append('| Lemma | POS | Frequency | # Variants | Glosses |')
        lines.append('|-------|-----|-----------|------------|---------|')
        for row in unstable:
            glosses = row['glosses'][:80] + '...' if len(row['glosses'] or '') > 80 else row['glosses']
            lines.append(
                f"| {row['citation_form']} | {row['pos']} | {row['token_count']:,} | "
                f"{row['gloss_variants']} | {glosses} |"
            )
    else:
        lines.append('*No unstable glosses found. ✓*')
    
    # Publication blockers
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 5. Publication Blockers')
    lines.append('')
    lines.append('These issues would materially damage a printed dictionary or grammar.')
    lines.append('')
    
    blockers = categorize_blockers(conn)
    
    lines.append('### Dictionary Blockers')
    lines.append('')
    if blockers['dictionary']:
        lines.append('| Type | Lemma | Citation | Current Gloss | Frequency |')
        lines.append('|------|-------|----------|---------------|-----------|')
        for item in blockers['dictionary'][:15]:
            lines.append(
                f"| {item['type']} | {item['lemma']} | {item['citation']} | "
                f"{item['gloss']} | {item['freq']:,} |"
            )
    else:
        lines.append('*No dictionary blockers. ✓*')
    
    lines.append('')
    lines.append('### Grammar Blockers')
    lines.append('')
    if blockers['grammar']:
        lines.append('| Type | Morpheme | Gloss | Category | Frequency |')
        lines.append('|------|----------|-------|----------|-----------|')
        for item in blockers['grammar'][:15]:
            lines.append(
                f"| {item['type']} | {item['morpheme']} | {item['gloss']} | "
                f"{item['category']} | {item['freq']:,} |"
            )
    else:
        lines.append('*No grammar blockers. ✓*')
    
    # Review queue summary
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('## 6. Review Queue Summary')
    lines.append('')
    
    high_priority, medium_priority = get_review_queue_by_priority(conn)
    
    lines.append(f'**Open high-priority items:** {len(high_priority)}')
    lines.append(f'**Open medium-priority items (showing first 50):** {len(medium_priority)}')
    lines.append('')
    
    if high_priority:
        lines.append('### High Priority (Resolve First)')
        lines.append('')
        lines.append('| Type | ID | Issue | Notes |')
        lines.append('|------|-------|-------|-------|')
        for row in high_priority[:20]:
            reason = (row['reason'] or '')[:40] + '...' if len(row['reason'] or '') > 40 else (row['reason'] or '')
            lines.append(
                f"| {row['entity_type']} | {row['entity_id']} | "
                f"{reason} | - |"
            )
    
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('*Focus editorial effort on the top of each section for maximum impact.*')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Tedim editorial dashboard'
    )
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--output', default='output/editorial_dashboard.md',
                        help='Output path')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        sys.exit(1)
    
    print(f"Loading backend from {args.db}...")
    conn = get_connection(args.db)
    
    print("Generating editorial dashboard...")
    report = generate_dashboard(conn)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"  → {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
