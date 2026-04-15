#!/usr/bin/env python3
"""
Generate publication dashboard summarizing all Tedim readiness metrics.

This script consolidates:
- Canonical metrics (from generate_metrics.py output)
- Dictionary readiness status
- Grammar readiness status
- Top editorial blockers
- Changes since last run

Output: output/publication_dashboard.md
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from report_utils import generate_provenance_header, get_git_commit


def load_metrics(metrics_path):
    """Load canonical metrics from JSON file."""
    if not metrics_path.exists():
        return None
    with open(metrics_path) as f:
        return json.load(f)


def get_dictionary_status(output_dir):
    """Check dictionary draft status from manifest or markdown."""
    manifest_path = output_dir / 'dictionary' / 'draft_dictionary_manifest.json'
    
    # Prefer manifest if available (structured, reliable)
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        return {
            'exists': True,
            'entries': manifest.get('glossed_lemmas', 0),
            'total_lemmas': manifest.get('total_lemmas', 0),
            'unglossed': manifest.get('unglossed_lemmas', 0),
            'with_examples': manifest.get('lemmas_with_examples', 0),
            'senses': manifest.get('total_senses', 0),
            'percent_glossed': manifest.get('percent_glossed', 0),
            'percent_with_examples': manifest.get('percent_with_examples', 0),
            'top_unresolved': manifest.get('top_unresolved', []),
            'by_pos': manifest.get('by_pos', {}),
            'by_entry_type': manifest.get('by_entry_type', {}),
            'unresolved_count': manifest.get('unresolved_count', 0),
            'mixed_count': manifest.get('mixed_count', 0),
            'lexical_cleanup_needed': manifest.get('lexical_cleanup_needed', 0),
            'ready_for_draft': manifest.get('ready_for_draft', False),
            'source': 'manifest',
            'path': str(output_dir / 'dictionary' / 'draft_dictionary.md')
        }
    
    # Fall back to parsing markdown
    draft_path = output_dir / 'dictionary' / 'draft_dictionary.md'
    if not draft_path.exists():
        return {'exists': False, 'entries': 0, 'with_review_flags': 0}
    
    content = draft_path.read_text()
    lines = content.split('\n')
    
    # Count entries (## headers)
    entries = sum(1 for line in lines if line.startswith('## ') and not line.startswith('## Document'))
    
    # Count review flags
    review_flags = content.count('⚠️')
    
    return {
        'exists': True,
        'entries': entries,
        'with_review_flags': review_flags,
        'source': 'markdown',
        'path': str(draft_path)
    }


def get_grammar_status(output_dir):
    """Check grammar draft status from manifest or markdown."""
    manifest_path = output_dir / 'grammar' / 'draft_grammar_manifest.json'
    
    # Prefer manifest if available (structured, reliable)
    if manifest_path.exists():
        with open(manifest_path) as f:
            manifest = json.load(f)
        
        status_counts = manifest.get('status_counts', {})
        return {
            'exists': True,
            'sections': manifest.get('total_sections', 0),
            'chapters': manifest.get('total_chapters', 0),
            'stable': status_counts.get('stable', 0),
            'provisional': status_counts.get('provisional', 0),
            'stubs': status_counts.get('stub', 0),
            'stable_pct': manifest.get('percent_stable', 0),
            'complete_pct': manifest.get('percent_complete', 0),
            'grammatical_morphemes': manifest.get('grammatical_morphemes', 0),
            'morphemes_with_examples': manifest.get('morphemes_with_examples', 0),
            'constructions': manifest.get('constructions_documented', 0),
            'topics': manifest.get('grammar_topics_documented', 0),
            'stub_sections': manifest.get('stub_sections', []),
            'ready_for_draft': manifest.get('ready_for_draft', False),
            'source': 'manifest',
            'path': str(output_dir / 'grammar' / 'draft_grammar.md')
        }
    
    # Fall back to parsing markdown
    draft_path = output_dir / 'grammar' / 'draft_grammar.md'
    if not draft_path.exists():
        return {'exists': False, 'sections': 0, 'stable': 0, 'provisional': 0, 'stubs': 0}
    
    content = draft_path.read_text()
    
    # Count status markers
    stable = content.count('[✓]')
    provisional = content.count('[⚠]')
    stubs = content.count('[❌]')
    
    total_sections = stable + provisional + stubs
    
    return {
        'exists': True,
        'sections': total_sections,
        'stable': stable,
        'provisional': provisional,
        'stubs': stubs,
        'stable_pct': round(100 * stable / total_sections, 1) if total_sections > 0 else 0,
        'complete_pct': round(100 * (stable + provisional) / total_sections, 1) if total_sections > 0 else 0,
        'source': 'markdown',
        'path': str(draft_path)
    }


def get_editorial_status(output_dir):
    """Check editorial dashboard status."""
    dashboard_path = output_dir / 'editorial_dashboard.md'
    if not dashboard_path.exists():
        return {'exists': False}
    
    content = dashboard_path.read_text()
    
    # Extract key counts from dashboard
    blockers = {
        'dictionary': content.count('Dictionary blocker'),
        'grammar': content.count('Grammar blocker'),
        'total': content.count('blocker')
    }
    
    return {
        'exists': True,
        'blockers': blockers,
        'path': str(dashboard_path)
    }


def get_top_blockers(conn, limit=10):
    """Get top editorial blockers from backend."""
    # Get high-frequency polysemous lemmas
    polysemous = conn.execute('''
        SELECT l.citation_form, l.pos, l.token_count, COUNT(s.sense_id) as sense_count
        FROM lemmas l
        JOIN senses s ON l.lemma_id = s.lemma_id
        WHERE l.token_count > 100
        GROUP BY l.lemma_id
        HAVING COUNT(s.sense_id) > 1
        ORDER BY l.token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    
    # Get items with unclear glosses
    unclear = conn.execute('''
        SELECT citation_form, pos, primary_gloss, token_count
        FROM lemmas
        WHERE primary_gloss LIKE '%?%' OR primary_gloss = ''
        ORDER BY token_count DESC
        LIMIT ?
    ''', (limit,)).fetchall()
    
    return {
        'polysemous': polysemous,
        'unclear': unclear
    }


def generate_dashboard(conn, output_dir, metrics_path):
    """Generate the publication dashboard."""
    lines = []
    
    # Provenance header
    lines.append(generate_provenance_header(
        script_name='scripts/generate_publication_dashboard.py',
        inputs=['data/ctd_backend.db'],
        command='make publication-dashboard'
    ))
    lines.append('')
    
    # Title
    lines.append('# Tedim Chin Publication Dashboard')
    lines.append('')
    lines.append(f'**Generated:** {datetime.now().isoformat()}')
    lines.append('')
    
    # Load canonical metrics
    metrics = load_metrics(metrics_path)
    if not metrics:
        lines.append('> **Warning:** Canonical metrics not found. Run `make metrics` first.')
        lines.append('')
    
    # Overview section
    lines.append('## Overview')
    lines.append('')
    
    if metrics:
        m = metrics.get('metrics', {})
        lines.append('| Metric | Value |')
        lines.append('|--------|-------|')
        lines.append(f"| Total tokens | {m.get('total_tokens', 'N/A'):,} |")
        lines.append(f"| Coverage | {m.get('coverage_known_pos_pct', 'N/A')}% |")
        lines.append(f"| Lemmas | {m.get('lemma_count', 'N/A'):,} |")
        lines.append(f"| Senses | {m.get('sense_count', 'N/A'):,} |")
        lines.append(f"| Grammatical morphemes | {m.get('grammatical_morpheme_count', 'N/A'):,} |")
        lines.append(f"| Examples | {m.get('example_count', 'N/A'):,} |")
        lines.append(f"| Review queue (open) | {m.get('review_queue_open', 'N/A'):,} |")
        lines.append('')
    
    # Dictionary readiness
    lines.append('## Dictionary Readiness')
    lines.append('')
    
    dict_status = get_dictionary_status(output_dir)
    if dict_status['exists']:
        lines.append(f"✓ Draft dictionary generated: `{dict_status['path']}`")
        lines.append('')
        
        if dict_status.get('source') == 'manifest':
            # Rich data from manifest
            lines.append(f"- **Glossed entries:** {dict_status['entries']:,} / {dict_status['total_lemmas']:,} ({dict_status['percent_glossed']}%)")
            lines.append(f"- **Entries with examples:** {dict_status['with_examples']:,} ({dict_status['percent_with_examples']}%)")
            lines.append(f"- **Total senses:** {dict_status['senses']:,}")
            
            # Entry type breakdown
            by_type = dict_status.get('by_entry_type', {})
            if by_type:
                lines.append('')
                lines.append('**Entry types:**')
                for etype, count in sorted(by_type.items(), key=lambda x: -x[1]):
                    marker = '⚠' if etype in ('unresolved', 'mixed') else ''
                    lines.append(f"  - {etype}: {count:,} {marker}")
            
            # Lexical cleanup needed
            cleanup = dict_status.get('lexical_cleanup_needed', 0)
            if cleanup > 0:
                lines.append('')
                lines.append(f"**⚠ Lexical cleanup needed:** {cleanup} entries (unresolved: {dict_status.get('unresolved_count', 0)}, mixed: {dict_status.get('mixed_count', 0)})")
            
            if dict_status.get('top_unresolved'):
                lines.append('')
                lines.append('**Top items needing attention:**')
                for item in dict_status['top_unresolved'][:5]:
                    etype = item.get('entry_type', '?')
                    lines.append(f"  - {item['form']} ({item['pos'] or '?'}, {etype}) — {item['tokens']:,} tokens")
        else:
            # Fallback markdown parsing
            lines.append(f"- **Entries:** {dict_status['entries']:,}")
            if dict_status.get('with_review_flags', 0) > 0:
                lines.append(f"- **Entries with review flags:** {dict_status['with_review_flags']:,}")
                pct_clean = 100 * (dict_status['entries'] - dict_status['with_review_flags']) / dict_status['entries']
                lines.append(f"- **Clean entries:** {pct_clean:.1f}%")
    else:
        lines.append('❌ Draft dictionary not generated. Run `make dictionary-draft`.')
    lines.append('')
    
    # Grammar readiness
    lines.append('## Grammar Readiness')
    lines.append('')
    
    grammar_status = get_grammar_status(output_dir)
    if grammar_status['exists']:
        lines.append(f"✓ Draft grammar generated: `{grammar_status['path']}`")
        lines.append('')
        
        if grammar_status.get('source') == 'manifest':
            # Rich data from manifest
            lines.append(f"- **Chapters:** {grammar_status.get('chapters', 'N/A')}")
            lines.append(f"- **Sections:** {grammar_status['sections']}")
            lines.append(f"- **Stable (✓):** {grammar_status['stable']} ({grammar_status['stable_pct']}%)")
            lines.append(f"- **Provisional (⚠):** {grammar_status['provisional']}")
            lines.append(f"- **Stubs (❌):** {grammar_status['stubs']}")
            lines.append('')
            lines.append(f"- **Grammatical morphemes:** {grammar_status.get('grammatical_morphemes', 0):,}")
            lines.append(f"- **Morphemes with examples:** {grammar_status.get('morphemes_with_examples', 0):,}")
            lines.append(f"- **Constructions documented:** {grammar_status.get('constructions', 0)}")
            
            if grammar_status.get('stub_sections'):
                lines.append('')
                lines.append('**Sections needing content:**')
                for stub in grammar_status['stub_sections'][:5]:
                    lines.append(f"  - {stub}")
        else:
            # Fallback markdown parsing
            lines.append(f"- **Total sections:** {grammar_status['sections']}")
            lines.append(f"- **Stable (✓):** {grammar_status['stable']} ({grammar_status['stable_pct']}%)")
            lines.append(f"- **Provisional (⚠):** {grammar_status['provisional']}")
            lines.append(f"- **Stubs (❌):** {grammar_status['stubs']}")
        lines.append('')
        
        if grammar_status['stubs'] > 0:
            lines.append(f"> **Gaps:** {grammar_status['stubs']} sections need content before publication.")
    else:
        lines.append('❌ Draft grammar not generated. Run `make grammar-draft`.')
    lines.append('')
    
    # Top blockers
    lines.append('## Top Editorial Blockers')
    lines.append('')
    
    blockers = get_top_blockers(conn)
    
    if blockers['polysemous']:
        lines.append('### High-Frequency Polysemous Lemmas')
        lines.append('')
        lines.append('These lemmas have multiple senses and high frequency—disambiguation impacts many tokens.')
        lines.append('')
        lines.append('| Lemma | POS | Tokens | Senses |')
        lines.append('|-------|-----|--------|--------|')
        for row in blockers['polysemous'][:10]:
            lines.append(f"| {row[0]} | {row[1] or '?'} | {row[2]:,} | {row[3]} |")
        lines.append('')
    
    if blockers['unclear']:
        lines.append('### Items with Unclear Glosses')
        lines.append('')
        lines.append('These lemmas have missing or uncertain glosses.')
        lines.append('')
        lines.append('| Lemma | POS | Current Gloss | Tokens |')
        lines.append('|-------|-----|---------------|--------|')
        for row in blockers['unclear'][:10]:
            gloss = row[2] if row[2] else '(empty)'
            lines.append(f"| {row[0]} | {row[1] or '?'} | {gloss} | {row[3]:,} |")
        lines.append('')
    
    # Publication gates
    lines.append('## Publication Gates')
    lines.append('')
    
    gates = []
    
    # Coverage gate
    if metrics:
        coverage = metrics.get('metrics', {}).get('coverage_known_pos_pct', 0)
        if coverage >= 99:
            gates.append(('✓', 'Coverage ≥ 99%', f'{coverage}%'))
        else:
            gates.append(('❌', 'Coverage ≥ 99%', f'{coverage}%'))
    
    # Review queue gate
    if metrics:
        open_items = metrics.get('metrics', {}).get('review_queue_open', 0)
        if open_items == 0:
            gates.append(('✓', 'Review queue cleared', f'{open_items} items'))
        else:
            gates.append(('⚠', 'Review queue cleared', f'{open_items} open'))
    
    # Dictionary gate - now considers entry_type cleanup
    if dict_status['exists']:
        if dict_status.get('source') == 'manifest':
            # Use manifest: check ready_for_draft (glossed AND no unresolved/mixed)
            if dict_status.get('ready_for_draft', False):
                gates.append(('✓', 'Dictionary ready', f"All clean"))
            else:
                # Report what's blocking
                unglossed = dict_status.get('unglossed', 0)
                cleanup = dict_status.get('lexical_cleanup_needed', 0)
                if unglossed > 0:
                    gates.append(('❌', 'Dictionary ready', f"{unglossed} unglossed"))
                elif cleanup > 0:
                    gates.append(('⚠', 'Dictionary ready', f"{cleanup} unresolved/mixed"))
                else:
                    gates.append(('⚠', 'Dictionary ready', 'Unknown blocker'))
        else:
            # Fallback: use review flags
            review_flags = dict_status.get('with_review_flags', 0)
            if review_flags < dict_status['entries'] * 0.1:
                gates.append(('✓', 'Dictionary <10% review flags', f"{review_flags} flags"))
            else:
                gates.append(('⚠', 'Dictionary <10% review flags', f"{review_flags} flags"))
    else:
        gates.append(('❌', 'Dictionary draft exists', 'Not generated'))
    
    # Grammar gate
    if grammar_status['exists']:
        if grammar_status['stubs'] == 0:
            gates.append(('✓', 'Grammar no stubs', 'Complete'))
        else:
            gates.append(('⚠', 'Grammar no stubs', f"{grammar_status['stubs']} stubs"))
    else:
        gates.append(('❌', 'Grammar draft exists', 'Not generated'))
    
    lines.append('| Status | Gate | Current |')
    lines.append('|--------|------|---------|')
    for status, gate, current in gates:
        lines.append(f'| {status} | {gate} | {current} |')
    lines.append('')
    
    # Overall readiness
    passed = sum(1 for g in gates if g[0] == '✓')
    total = len(gates)
    
    lines.append('## Overall Readiness')
    lines.append('')
    lines.append(f'**Gates passed:** {passed}/{total}')
    lines.append('')
    
    if passed == total:
        lines.append('✓ **Publication ready** — All gates passed.')
    elif passed >= total * 0.75:
        lines.append('⚠ **Nearly ready** — Minor issues remain.')
    else:
        lines.append('❌ **Not ready** — Significant work needed.')
    lines.append('')
    
    # Next steps
    lines.append('## Recommended Next Steps')
    lines.append('')
    
    if not dict_status['exists']:
        lines.append('1. Generate dictionary draft: `make dictionary-draft`')
    if not grammar_status['exists']:
        lines.append('1. Generate grammar draft: `make grammar-draft`')
    if blockers['polysemous']:
        lines.append(f"1. Resolve top polysemous lemma: **{blockers['polysemous'][0][0]}** ({blockers['polysemous'][0][2]:,} tokens)")
    if grammar_status.get('stubs', 0) > 0:
        lines.append('1. Fill grammar stub sections')
    if metrics and metrics.get('metrics', {}).get('review_queue_open', 0) > 0:
        lines.append('1. Process review queue items')
    
    lines.append('')
    lines.append('---')
    lines.append('')
    lines.append('*Generated by `make publication-dashboard`*')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate Tedim publication dashboard')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Backend database path')
    parser.add_argument('--output', default='output/publication_dashboard.md', help='Output path')
    args = parser.parse_args()
    
    db_path = Path(args.db)
    output_path = Path(args.output)
    output_dir = Path('output')
    metrics_path = output_dir / 'metrics' / 'ctd_metrics.json'
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}", file=sys.stderr)
        return 1
    
    print(f"Loading backend from {db_path}...")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    print("Generating publication dashboard...")
    report = generate_dashboard(conn, output_dir, metrics_path)
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_path.write_text(report)
    print(f"  → {output_path}")
    
    conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
