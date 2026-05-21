#!/usr/bin/env python3
"""
Canonical Tedim Chin Metrics Pipeline
======================================

Generates all headline metrics from a single source of truth (the backend database).
Outputs both machine-readable JSON and human-readable Markdown.

Usage:
    python scripts/generate_metrics.py [--db data/ctd_backend.db]

Outputs:
    - output/ctd_metrics.json  (machine-readable, for CI/tests)
    - output/ctd_metrics.md    (human-readable report)

This script defines all metrics explicitly with their denominators and inclusion
rules, providing a stable, reproducible baseline for publication work.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
import subprocess

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from backend import Backend


# =============================================================================
# METRIC DEFINITIONS
# =============================================================================
# Each metric is defined with:
# - name: canonical identifier
# - description: what it measures
# - denominator: what the percentage is relative to (if applicable)
# - inclusion_rule: what is counted/excluded

METRIC_DEFINITIONS = {
    # Token metrics
    'total_tokens': {
        'description': 'Total tokens in corpus (from tokens.tsv)',
        'denominator': None,
        'inclusion_rule': 'All rows in tokens table, each representing one token occurrence in the Bible text',
    },
    'total_sources': {
        'description': 'Number of verse sources (Bible verses)',
        'denominator': None,
        'inclusion_rule': 'Distinct verse IDs in sources table',
    },
    
    # Coverage metrics
    'tokens_with_known_pos': {
        'description': 'Tokens where analyzer assigned a known POS',
        'denominator': 'total_tokens',
        'inclusion_rule': 'Tokens where pos IS NOT NULL AND pos != "?"',
    },
    'tokens_with_unknown_pos': {
        'description': 'Tokens where POS could not be determined',
        'denominator': 'total_tokens',
        'inclusion_rule': 'Tokens where pos IS NULL OR pos = "?"',
    },
    'tokens_non_ambiguous': {
        'description': 'Tokens with single, clear analysis (no review needed)',
        'denominator': 'total_tokens',
        'inclusion_rule': 'Tokens not flagged for review, single segmentation/lemma/POS',
    },
    'tokens_ambiguous': {
        'description': 'Tokens requiring editorial review',
        'denominator': 'total_tokens',
        'inclusion_rule': 'Tokens with multiple possible analyses or flagged for review',
    },
    
    # Lexicon metrics
    'wordform_count': {
        'description': 'Distinct surface forms in corpus',
        'denominator': None,
        'inclusion_rule': 'Distinct wordforms in wordforms table',
    },
    'lemma_count': {
        'description': 'Dictionary headwords (lexemes)',
        'denominator': None,
        'inclusion_rule': 'All entries in lemmas table',
    },
    'sense_count': {
        'description': 'Distinct word senses (polysemy expansion)',
        'denominator': None,
        'inclusion_rule': 'All entries in senses table',
    },
    'grammatical_morpheme_count': {
        'description': 'Bound morphemes and function words',
        'denominator': None,
        'inclusion_rule': 'All entries in grammatical_morphemes table',
    },
    
    # Example metrics
    'example_count': {
        'description': 'Total usage examples',
        'denominator': None,
        'inclusion_rule': 'All entries in examples table',
    },
    'examples_linked_to_sense': {
        'description': 'Examples with sense assignment',
        'denominator': 'example_count',
        'inclusion_rule': 'Examples where sense_id IS NOT NULL',
    },
    'examples_linked_to_morpheme': {
        'description': 'Examples illustrating grammatical morphemes',
        'denominator': None,
        'inclusion_rule': 'Examples where morpheme_id IS NOT NULL',
    },
    
    # Review queue metrics
    'review_queue_total': {
        'description': 'Total items requiring editorial review',
        'denominator': None,
        'inclusion_rule': 'All entries in review_queue table (resolved and open)',
    },
    'review_queue_open': {
        'description': 'Unresolved review items',
        'denominator': 'review_queue_total',
        'inclusion_rule': 'review_queue entries where resolution IS NULL',
    },
    'review_queue_resolved': {
        'description': 'Resolved review items',
        'denominator': 'review_queue_total',
        'inclusion_rule': 'review_queue entries where resolution IS NOT NULL',
    },
    'review_high_priority': {
        'description': 'High priority review items',
        'denominator': 'review_queue_total',
        'inclusion_rule': 'review_queue entries where priority = "high"',
    },
    
    # Construction/Grammar topic metrics
    'construction_count': {
        'description': 'Grammatical constructions modeled',
        'denominator': None,
        'inclusion_rule': 'All entries in constructions table',
    },
    'grammar_topic_count': {
        'description': 'Grammar topics for chaptered export',
        'denominator': None,
        'inclusion_rule': 'All entries in grammar_topics table',
    },
    
    # Quality metrics
    'senses_with_examples': {
        'description': 'Senses that have at least one example',
        'denominator': 'sense_count',
        'inclusion_rule': 'Senses with at least one linked example',
    },
    'high_freq_lemmas_stable': {
        'description': 'Top-1000 frequency lemmas with stable primary gloss',
        'denominator': None,
        'inclusion_rule': 'Lemmas in top 1000 by frequency where primary sense is unambiguous',
    },
}


def get_git_commit():
    """Get current git commit hash."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True, text=True, cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            return result.stdout.strip()[:8]
    except:
        pass
    return 'unknown'


def compute_metrics(db: Backend) -> dict:
    """Compute all canonical metrics from the backend database."""
    
    metrics = {}
    
    # Get a connection for raw queries
    import sqlite3
    conn = sqlite3.connect(str(db.db_path))
    conn.row_factory = sqlite3.Row
    
    # Basic counts from get_stats()
    stats = db.get_stats()
    
    # Token metrics
    metrics['total_tokens'] = conn.execute('SELECT COUNT(*) FROM tokens').fetchone()[0]
    metrics['total_sources'] = stats.get('sources', 0)
    
    # Coverage - tokens with known POS (POS is on wordforms, join via wordform_id)
    known_pos = conn.execute('''
        SELECT COUNT(*) FROM tokens t
        JOIN wordforms w ON t.wordform_id = w.wordform_id
        WHERE w.pos IS NOT NULL AND w.pos != '?' AND w.pos != ''
    ''').fetchone()[0]
    metrics['tokens_with_known_pos'] = known_pos
    metrics['tokens_with_unknown_pos'] = metrics['total_tokens'] - known_pos
    
    # Ambiguity analysis - ambiguous wordforms
    ambiguous_wordforms = conn.execute('''
        SELECT COUNT(*) FROM wordforms WHERE is_ambiguous = 1
    ''').fetchone()[0]
    
    # Count ambiguous tokens based on ambiguous wordforms
    ambiguous_tokens = conn.execute('''
        SELECT COUNT(*) FROM tokens t
        JOIN wordforms w ON t.wordform_id = w.wordform_id
        WHERE w.is_ambiguous = 1
    ''').fetchone()[0]
    
    metrics['tokens_ambiguous'] = ambiguous_tokens
    metrics['tokens_non_ambiguous'] = metrics['total_tokens'] - ambiguous_tokens
    
    # Lexicon counts
    metrics['wordform_count'] = conn.execute('SELECT COUNT(*) FROM wordforms').fetchone()[0]
    metrics['lemma_count'] = stats.get('lemmas', 0)
    metrics['sense_count'] = stats.get('senses', 0)
    metrics['grammatical_morpheme_count'] = stats.get('grammatical_morphemes', 0)
    
    # Example metrics
    metrics['example_count'] = stats.get('examples', 0)
    metrics['examples_linked_to_sense'] = conn.execute('''
        SELECT COUNT(*) FROM examples WHERE sense_id IS NOT NULL
    ''').fetchone()[0]
    metrics['examples_linked_to_morpheme'] = conn.execute('''
        SELECT COUNT(*) FROM examples WHERE morpheme_id IS NOT NULL
    ''').fetchone()[0]
    
    # Review queue metrics
    metrics['review_queue_total'] = conn.execute('SELECT COUNT(*) FROM review_queue').fetchone()[0]
    metrics['review_queue_open'] = stats.get('review_open', 0)
    metrics['review_queue_resolved'] = stats.get('review_resolved', 0)
    metrics['review_high_priority'] = conn.execute('''
        SELECT COUNT(*) FROM review_queue WHERE priority = 'high'
    ''').fetchone()[0]
    metrics['review_medium_priority'] = conn.execute('''
        SELECT COUNT(*) FROM review_queue WHERE priority = 'medium'
    ''').fetchone()[0]
    metrics['review_low_priority'] = conn.execute('''
        SELECT COUNT(*) FROM review_queue WHERE priority = 'low'
    ''').fetchone()[0]
    
    # Construction/Grammar metrics
    try:
        metrics['construction_count'] = conn.execute('SELECT COUNT(*) FROM constructions').fetchone()[0]
    except:
        metrics['construction_count'] = 0
    try:
        metrics['grammar_topic_count'] = conn.execute('SELECT COUNT(*) FROM grammar_topics').fetchone()[0]
    except:
        metrics['grammar_topic_count'] = 0
    
    # Quality metrics
    metrics['senses_with_examples'] = conn.execute('''
        SELECT COUNT(DISTINCT sense_id) FROM examples WHERE sense_id IS NOT NULL
    ''').fetchone()[0]
    
    # High-frequency lemmas with stable gloss
    # Definition: lemmas in top 1000 by token_count that have only one sense
    top_lemmas = conn.execute('''
        SELECT l.lemma_id, COUNT(DISTINCT s.sense_id) as sense_count
        FROM lemmas l
        LEFT JOIN senses s ON l.lemma_id = s.lemma_id
        GROUP BY l.lemma_id
        ORDER BY l.token_count DESC
        LIMIT 1000
    ''').fetchall()
    
    stable_count = sum(1 for _, sense_count in top_lemmas if sense_count <= 1)
    metrics['high_freq_lemmas_stable'] = stable_count
    metrics['high_freq_lemmas_total'] = len(top_lemmas)
    
    # Compute derived percentages
    if metrics['total_tokens'] > 0:
        metrics['coverage_known_pos_pct'] = round(
            100 * metrics['tokens_with_known_pos'] / metrics['total_tokens'], 2
        )
        metrics['coverage_non_ambiguous_pct'] = round(
            100 * metrics['tokens_non_ambiguous'] / metrics['total_tokens'], 2
        )
    else:
        metrics['coverage_known_pos_pct'] = 0
        metrics['coverage_non_ambiguous_pct'] = 0
    
    if metrics['example_count'] > 0:
        metrics['examples_linked_pct'] = round(
            100 * metrics['examples_linked_to_sense'] / metrics['example_count'], 2
        )
    else:
        metrics['examples_linked_pct'] = 0
    
    if metrics['sense_count'] > 0:
        metrics['senses_with_examples_pct'] = round(
            100 * metrics['senses_with_examples'] / metrics['sense_count'], 2
        )
    else:
        metrics['senses_with_examples_pct'] = 0
    
    conn.close()
    return metrics


def get_pos_distribution(db: Backend) -> dict:
    """Get token count by POS (via wordforms table)."""
    import sqlite3
    conn = sqlite3.connect(str(db.db_path))
    rows = conn.execute('''
        SELECT w.pos, COUNT(*) as count
        FROM tokens t
        JOIN wordforms w ON t.wordform_id = w.wordform_id
        WHERE w.pos IS NOT NULL AND w.pos != ''
        GROUP BY w.pos
        ORDER BY count DESC
    ''').fetchall()
    conn.close()
    return {row[0]: row[1] for row in rows}


def get_morpheme_categories(db: Backend) -> dict:
    """Get grammatical morpheme counts by category."""
    import sqlite3
    conn = sqlite3.connect(str(db.db_path))
    rows = conn.execute('''
        SELECT category, COUNT(*) as count, SUM(frequency) as total_freq
        FROM grammatical_morphemes
        GROUP BY category
        ORDER BY total_freq DESC
    ''').fetchall()
    conn.close()
    return {row[0]: {'count': row[1], 'frequency': row[2]} for row in rows}


def generate_json_output(metrics: dict, pos_dist: dict, morph_cats: dict) -> dict:
    """Generate the complete JSON output structure."""
    return {
        'meta': {
            'generated': datetime.now().isoformat(),
            'generator': 'scripts/generate_metrics.py',
            'git_commit': get_git_commit(),
            'source': 'data/ctd_backend.db',
            'language': 'ctd',
            'language_name': 'Tedim Chin',
        },
        'metrics': metrics,
        'pos_distribution': pos_dist,
        'morpheme_categories': morph_cats,
        'definitions': METRIC_DEFINITIONS,
    }


def generate_markdown_report(data: dict) -> str:
    """Generate human-readable markdown report."""
    m = data['metrics']
    pos = data['pos_distribution']
    morph = data['morpheme_categories']
    meta = data['meta']
    
    lines = [
        '<!-- GENERATED FILE - DO NOT EDIT MANUALLY -->',
        f'<!-- Generated by: scripts/generate_metrics.py -->',
        f'<!-- From: {meta["source"]} -->',
        f'<!-- At: {meta["generated"]} -->',
        f'<!-- Commit: {meta["git_commit"]} -->',
        '<!-- Regenerate with: make metrics -->',
        '',
        '# Tedim Chin Canonical Metrics Report',
        '',
        f'**Generated:** {meta["generated"]}',
        f'**Git commit:** {meta["git_commit"]}',
        f'**Source:** `{meta["source"]}`',
        '',
        '---',
        '',
        '## Headline Metrics',
        '',
        '### Token Coverage',
        '',
        '| Metric | Value | Percentage |',
        '|--------|-------|------------|',
        f'| Total tokens | {m["total_tokens"]:,} | 100% |',
        f'| Tokens with known POS | {m["tokens_with_known_pos"]:,} | {m["coverage_known_pos_pct"]}% |',
        f'| Tokens non-ambiguous | {m["tokens_non_ambiguous"]:,} | {m["coverage_non_ambiguous_pct"]}% |',
        f'| Tokens ambiguous | {m["tokens_ambiguous"]:,} | {100 - m["coverage_non_ambiguous_pct"]:.2f}% |',
        f'| Tokens with unknown POS | {m["tokens_with_unknown_pos"]:,} | {100 - m["coverage_known_pos_pct"]:.2f}% |',
        '',
        '### Lexicon Size',
        '',
        '| Category | Count |',
        '|----------|-------|',
        f'| Distinct wordforms | {m["wordform_count"]:,} |',
        f'| Lemmas (headwords) | {m["lemma_count"]:,} |',
        f'| Senses | {m["sense_count"]:,} |',
        f'| Grammatical morphemes | {m["grammatical_morpheme_count"]:,} |',
        '',
        '### Examples',
        '',
        '| Metric | Count | Percentage |',
        '|--------|-------|------------|',
        f'| Total examples | {m["example_count"]:,} | 100% |',
        f'| Linked to sense | {m["examples_linked_to_sense"]:,} | {m["examples_linked_pct"]}% |',
        f'| Linked to morpheme | {m["examples_linked_to_morpheme"]:,} | - |',
        f'| Senses with examples | {m["senses_with_examples"]:,} | {m["senses_with_examples_pct"]}% of senses |',
        '',
        '### Review Queue',
        '',
        '| Priority | Count |',
        '|----------|-------|',
        f'| Total items | {m["review_queue_total"]:,} |',
        f'| Open | {m["review_queue_open"]:,} |',
        f'| Resolved | {m["review_queue_resolved"]:,} |',
        f'| High priority | {m["review_high_priority"]:,} |',
        f'| Medium priority | {m.get("review_medium_priority", 0):,} |',
        f'| Low priority | {m.get("review_low_priority", 0):,} |',
        '',
        '### Grammar Infrastructure',
        '',
        '| Layer | Count |',
        '|-------|-------|',
        f'| Constructions | {m["construction_count"]:,} |',
        f'| Grammar topics | {m["grammar_topic_count"]:,} |',
        '',
        '### Publication Readiness',
        '',
        '| Metric | Value |',
        '|--------|-------|',
        f'| High-freq lemmas (top 1000) | {m["high_freq_lemmas_total"]:,} |',
        f'| With stable primary gloss | {m["high_freq_lemmas_stable"]:,} ({100*m["high_freq_lemmas_stable"]/max(1,m["high_freq_lemmas_total"]):.1f}%) |',
        '',
        '---',
        '',
        '## Part of Speech Distribution',
        '',
        '| POS | Token Count | Percentage |',
        '|-----|-------------|------------|',
    ]
    
    total = sum(pos.values())
    for tag, count in sorted(pos.items(), key=lambda x: -x[1]):
        pct = 100 * count / total if total > 0 else 0
        lines.append(f'| {tag} | {count:,} | {pct:.2f}% |')
    
    lines.extend([
        '',
        '---',
        '',
        '## Grammatical Morpheme Categories',
        '',
        '| Category | Count | Total Frequency |',
        '|----------|-------|-----------------|',
    ])
    
    for cat, data in sorted(morph.items(), key=lambda x: -(x[1]['frequency'] or 0)):
        lines.append(f'| {cat} | {data["count"]} | {data["frequency"] or 0:,} |')
    
    lines.extend([
        '',
        '---',
        '',
        '## Metric Definitions',
        '',
        'This section documents exactly what each metric measures.',
        '',
    ])
    
    for metric_name, defn in METRIC_DEFINITIONS.items():
        lines.extend([
            f'### `{metric_name}`',
            '',
            f'**Description:** {defn["description"]}',
            '',
            f'**Denominator:** {defn["denominator"] or "N/A (absolute count)"}',
            '',
            f'**Inclusion rule:** {defn["inclusion_rule"]}',
            '',
        ])
    
    lines.extend([
        '---',
        '',
        '*This report was generated automatically by `scripts/generate_metrics.py`.',
        'Do not edit manually—regenerate from the backend database.*',
    ])
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate canonical Tedim Chin metrics'
    )
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--json-output', default='output/metrics/ctd_metrics.json',
                        help='JSON output path')
    parser.add_argument('--md-output', default='output/metrics/ctd_metrics.md',
                        help='Markdown output path')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        print("Run 'make backend' to generate it.")
        sys.exit(1)
    
    print(f"Loading backend from {args.db}...")
    db = Backend(args.db)
    
    print("Computing metrics...")
    metrics = compute_metrics(db)
    pos_dist = get_pos_distribution(db)
    morph_cats = get_morpheme_categories(db)
    
    print("Generating outputs...")
    json_data = generate_json_output(metrics, pos_dist, morph_cats)
    md_report = generate_markdown_report(json_data)
    
    # Ensure output directory exists
    Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.md_output).parent.mkdir(parents=True, exist_ok=True)
    
    # Write JSON
    with open(args.json_output, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"  → {args.json_output}")
    
    # Write Markdown
    with open(args.md_output, 'w') as f:
        f.write(md_report)
    print(f"  → {args.md_output}")
    
    # Print summary
    print()
    print("=== Headline Metrics ===")
    print(f"  Total tokens:        {metrics['total_tokens']:,}")
    print(f"  Coverage (known POS): {metrics['coverage_known_pos_pct']}%")
    print(f"  Non-ambiguous:       {metrics['coverage_non_ambiguous_pct']}%")
    print(f"  Lemmas:              {metrics['lemma_count']:,}")
    print(f"  Senses:              {metrics['sense_count']:,}")
    print(f"  Examples:            {metrics['example_count']:,}")
    print(f"  Review queue (open): {metrics['review_queue_open']:,}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
