#!/usr/bin/env python3
"""
Generate editorial blockers report for Tedim Chin publication.

This script identifies the highest-value issues to resolve before publication:
1. High-frequency items with empty or unclear glosses
2. Polysemous lemmas needing sense disambiguation
3. Mixed lexical/grammatical items
4. Senses without examples

Output: output/editorial_blockers.md
"""

import argparse
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
from report_utils import generate_provenance_header


def get_empty_gloss_blockers(conn, limit=30):
    """Get high-frequency items with empty or unclear glosses."""
    return conn.execute('''
        SELECT citation_form, pos, primary_gloss, token_count
        FROM lemmas
        WHERE (primary_gloss = '' OR primary_gloss LIKE '%?%')
          AND token_count > 50
        ORDER BY token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_polysemous_blockers(conn, limit=20):
    """Get high-frequency polysemous lemmas."""
    return conn.execute('''
        SELECT l.citation_form, l.pos, l.token_count, 
               COUNT(s.sense_id) as sense_count,
               GROUP_CONCAT(s.gloss, ' | ') as glosses
        FROM lemmas l
        JOIN senses s ON l.lemma_id = s.lemma_id
        WHERE l.token_count > 500
        GROUP BY l.lemma_id
        HAVING COUNT(s.sense_id) > 1
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_mixed_pos_blockers(conn, limit=20):
    """Get items with mixed lexical/grammatical POS assignments."""
    # Find lemmas where wordforms have conflicting POS
    return conn.execute('''
        SELECT l.citation_form, l.pos as lemma_pos, l.token_count,
               GROUP_CONCAT(DISTINCT w.pos) as wordform_pos_set
        FROM lemmas l
        JOIN wordforms w ON l.lemma_id = w.lemma_id
        WHERE l.token_count > 100
        GROUP BY l.lemma_id
        HAVING COUNT(DISTINCT w.pos) > 1
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_senses_without_examples(conn, limit=30):
    """Get high-frequency senses without examples."""
    return conn.execute('''
        SELECT l.citation_form, s.gloss, l.token_count
        FROM senses s
        JOIN lemmas l ON s.lemma_id = l.lemma_id
        LEFT JOIN examples e ON s.sense_id = e.sense_id
        WHERE e.example_id IS NULL
          AND l.token_count > 100
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()


def get_summary_stats(conn):
    """Get summary statistics for blockers."""
    stats = {}
    
    # Total with empty/unclear gloss
    stats['empty_gloss_count'] = conn.execute('''
        SELECT COUNT(*) FROM lemmas 
        WHERE primary_gloss = '' OR primary_gloss LIKE '%?%'
    ''').fetchone()[0]
    
    # Token mass affected by empty glosses
    stats['empty_gloss_tokens'] = conn.execute('''
        SELECT COALESCE(SUM(token_count), 0) FROM lemmas 
        WHERE primary_gloss = '' OR primary_gloss LIKE '%?%'
    ''').fetchone()[0]
    
    # Total polysemous lemmas
    stats['polysemous_count'] = conn.execute('''
        SELECT COUNT(*) FROM (
            SELECT lemma_id FROM senses GROUP BY lemma_id HAVING COUNT(*) > 1
        )
    ''').fetchone()[0]
    
    # Total tokens
    stats['total_tokens'] = conn.execute('SELECT COUNT(*) FROM tokens').fetchone()[0]
    
    # Senses without examples
    stats['senses_no_examples'] = conn.execute('''
        SELECT COUNT(*) FROM senses s
        LEFT JOIN examples e ON s.sense_id = e.sense_id
        WHERE e.example_id IS NULL
    ''').fetchone()[0]
    
    return stats


def generate_blockers_report(conn):
    """Generate the editorial blockers report."""
    lines = []
    
    lines.append(generate_provenance_header(
        script_name='scripts/generate_editorial_blockers.py',
        inputs=['data/ctd_backend.db'],
        command='make editorial-blockers'
    ))
    lines.append('')
    
    lines.append('# Tedim Chin Editorial Blockers')
    lines.append('')
    lines.append(f'**Generated:** {datetime.now().isoformat()}')
    lines.append('')
    lines.append('This report identifies the highest-priority items to resolve before publication.')
    lines.append('')
    
    # Summary
    stats = get_summary_stats(conn)
    lines.append('## Summary')
    lines.append('')
    lines.append('| Issue | Count | Impact |')
    lines.append('|-------|-------|--------|')
    lines.append(f"| Empty/unclear glosses | {stats['empty_gloss_count']:,} | {stats['empty_gloss_tokens']:,} tokens |")
    lines.append(f"| Polysemous lemmas | {stats['polysemous_count']:,} | Need disambiguation |")
    lines.append(f"| Senses without examples | {stats['senses_no_examples']:,} | No corpus evidence |")
    lines.append('')
    
    # Empty/unclear glosses (dictionary blockers)
    lines.append('## Dictionary Blockers: Empty or Unclear Glosses')
    lines.append('')
    lines.append('These items have high frequency but empty or uncertain glosses.')
    lines.append('**Action:** Assign clear English glosses based on KJV alignment.')
    lines.append('')
    
    empty_glosses = get_empty_gloss_blockers(conn)
    if empty_glosses:
        lines.append('| Rank | Lemma | POS | Current Gloss | Tokens |')
        lines.append('|------|-------|-----|---------------|--------|')
        for i, row in enumerate(empty_glosses, 1):
            gloss = row['primary_gloss'] if row['primary_gloss'] else '(empty)'
            lines.append(f"| {i} | **{row['citation_form']}** | {row['pos'] or '?'} | {gloss} | {row['token_count']:,} |")
        lines.append('')
    
    # Polysemous lemmas (disambiguation blockers)
    lines.append('## Disambiguation Blockers: Polysemous Lemmas')
    lines.append('')
    lines.append('These frequent lemmas have multiple senses. Disambiguation affects many tokens.')
    lines.append('**Action:** Review sense boundaries and add context-sensitive rules.')
    lines.append('')
    
    polysemous = get_polysemous_blockers(conn)
    if polysemous:
        lines.append('| Rank | Lemma | POS | Tokens | Senses | Glosses |')
        lines.append('|------|-------|-----|--------|--------|---------|')
        for i, row in enumerate(polysemous, 1):
            glosses = row['glosses'][:60] + '...' if len(row['glosses']) > 60 else row['glosses']
            lines.append(f"| {i} | **{row['citation_form']}** | {row['pos'] or '?'} | {row['token_count']:,} | {row['sense_count']} | {glosses} |")
        lines.append('')
    
    # Mixed POS items
    lines.append('## POS Cleanup: Mixed Lexical/Grammatical Items')
    lines.append('')
    lines.append('These items have wordforms with conflicting POS assignments.')
    lines.append('**Action:** Determine primary POS or split into separate lemmas.')
    lines.append('')
    
    mixed_pos = get_mixed_pos_blockers(conn)
    if mixed_pos:
        lines.append('| Lemma | Lemma POS | Tokens | Wordform POS |')
        lines.append('|-------|-----------|--------|--------------|')
        for row in mixed_pos:
            lines.append(f"| **{row['citation_form']}** | {row['lemma_pos'] or '?'} | {row['token_count']:,} | {row['wordform_pos_set']} |")
        lines.append('')
    
    # Senses without examples
    lines.append('## Example Gaps: Senses Without Corpus Examples')
    lines.append('')
    lines.append('These senses exist but have no linked examples.')
    lines.append('**Action:** Link examples from corpus or mark as unattested.')
    lines.append('')
    
    no_examples = get_senses_without_examples(conn)
    if no_examples:
        lines.append('| Lemma | Sense | Tokens |')
        lines.append('|-------|-------|--------|')
        for row in no_examples[:20]:
            lines.append(f"| **{row['citation_form']}** | {row['gloss']} | {row['token_count']:,} |")
        if len(no_examples) > 20:
            lines.append(f"| ... | ({len(no_examples) - 20} more) | |")
        lines.append('')
    
    # Next steps
    lines.append('## Recommended Workflow')
    lines.append('')
    lines.append('1. **Start with dictionary blockers** — resolve empty glosses for the top 10 items')
    lines.append('2. **Then disambiguation** — review polysemous lemmas starting with highest frequency')
    lines.append('3. **Clean up POS** — decide on primary category for mixed items')
    lines.append('4. **Fill example gaps** — link corpus examples to unattested senses')
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('*Regenerate with `make editorial-blockers`*')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate Tedim editorial blockers report')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Backend database path')
    parser.add_argument('--output', default='output/editorial_blockers.md', help='Output path')
    args = parser.parse_args()
    
    db_path = Path(args.db)
    output_path = Path(args.output)
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        return 1
    
    print(f"Loading backend from {db_path}...")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    print("Generating editorial blockers report...")
    report = generate_blockers_report(conn)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report)
    print(f"  → {output_path}")
    
    conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
