#!/usr/bin/env python3
"""
Tedim Chin Chaptered Grammar Draft
==================================

Generates a chaptered grammar with explicit gap markers showing:
- Stable sections (well-documented, good examples)
- Provisional sections (documented but needs review)
- Missing sections (placeholder with explicit gap marker)

Usage:
    python scripts/generate_grammar_draft.py [--db data/ctd_backend.db]

Output:
    output/grammar/draft_grammar.md

Publication Readiness Criteria:
- Draft ready = can export chaptered grammar with stable structure
- Provisional sections are marked as such
- Missing sections have explicit gap markers
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


# Grammar chapter structure for Tedim Chin
GRAMMAR_CHAPTERS = [
    {
        'id': '1',
        'title': 'Introduction',
        'sections': [
            {'id': '1.1', 'title': 'Language Background', 'status': 'stub'},
            {'id': '1.2', 'title': 'Genetic Classification', 'status': 'stub'},
            {'id': '1.3', 'title': 'Phoneme Inventory', 'status': 'provisional'},
            {'id': '1.4', 'title': 'Syllable Structure', 'status': 'provisional'},
            {'id': '1.5', 'title': 'Tone System', 'status': 'provisional'},
        ]
    },
    {
        'id': '2',
        'title': 'Morphological Overview',
        'sections': [
            {'id': '2.1', 'title': 'Word Classes', 'status': 'stable'},
            {'id': '2.2', 'title': 'Morphological Processes', 'status': 'stable'},
            {'id': '2.3', 'title': 'Compounding', 'status': 'stable'},
            {'id': '2.4', 'title': 'Reduplication', 'status': 'stable'},
        ]
    },
    {
        'id': '3',
        'title': 'Noun Morphology',
        'sections': [
            {'id': '3.1', 'title': 'Noun Classification', 'status': 'stable'},
            {'id': '3.2', 'title': 'Plural Marking', 'status': 'stable', 'morpheme_category': 'plural_marker'},
            {'id': '3.3', 'title': 'Case Marking', 'status': 'stable', 'morpheme_category': 'case_marker'},
            {'id': '3.4', 'title': 'Possession', 'status': 'provisional'},
            {'id': '3.5', 'title': 'Nominalization', 'status': 'stable', 'morpheme_category': 'nominalizer'},
        ]
    },
    {
        'id': '4',
        'title': 'Pronouns',
        'sections': [
            {'id': '4.1', 'title': 'Personal Pronouns', 'status': 'stable'},
            {'id': '4.2', 'title': 'Pronominal Prefixes', 'status': 'stable', 'morpheme_category': 'pronominal_prefix'},
            {'id': '4.3', 'title': 'Demonstratives', 'status': 'provisional'},
            {'id': '4.4', 'title': 'Interrogatives', 'status': 'provisional'},
        ]
    },
    {
        'id': '5',
        'title': 'Verb Morphology',
        'sections': [
            {'id': '5.1', 'title': 'Verb Classification', 'status': 'stable'},
            {'id': '5.2', 'title': 'Stem Alternations', 'status': 'stable'},
            {'id': '5.3', 'title': 'TAM Suffixes', 'status': 'stable', 'morpheme_category': 'tam_suffix'},
            {'id': '5.4', 'title': 'Irrealis Marking', 'status': 'stable', 'morpheme_category': 'irrealis_marker'},
            {'id': '5.5', 'title': 'Sentence-Final Particles', 'status': 'stable', 'morpheme_category': 'sentence_final'},
            {'id': '5.6', 'title': 'Directional Verbs', 'status': 'provisional', 'morpheme_category': 'directional_verb'},
            {'id': '5.7', 'title': 'Auxiliary Verbs', 'status': 'provisional', 'morpheme_category': 'auxiliary'},
        ]
    },
    {
        'id': '6',
        'title': 'Function Words',
        'sections': [
            {'id': '6.1', 'title': 'Overview', 'status': 'stable'},
            {'id': '6.2', 'title': 'Copula', 'status': 'stable', 'morpheme_category': 'copula'},
            {'id': '6.3', 'title': 'Conjunctions', 'status': 'provisional'},
            {'id': '6.4', 'title': 'Discourse Particles', 'status': 'provisional', 'morpheme_category': 'particle'},
        ]
    },
    {
        'id': '7',
        'title': 'Clause Structure',
        'sections': [
            {'id': '7.1', 'title': 'Basic Clause Types', 'status': 'provisional'},
            {'id': '7.2', 'title': 'Argument Structure', 'status': 'provisional'},
            {'id': '7.3', 'title': 'Word Order', 'status': 'stub'},
            {'id': '7.4', 'title': 'Relative Clauses', 'status': 'stub'},
        ]
    },
    {
        'id': '8',
        'title': 'Complex Sentences',
        'sections': [
            {'id': '8.1', 'title': 'Coordination', 'status': 'provisional'},
            {'id': '8.2', 'title': 'Subordination', 'status': 'stub'},
            {'id': '8.3', 'title': 'Serial Verb Constructions', 'status': 'stub'},
        ]
    },
    {
        'id': '9',
        'title': 'Constructions',
        'sections': [
            {'id': '9.1', 'title': 'Aspect Chains', 'status': 'provisional', 'construction_type': 'aspect'},
            {'id': '9.2', 'title': 'Case Constructions', 'status': 'provisional', 'construction_type': 'case'},
            {'id': '9.3', 'title': 'TAM Constructions', 'status': 'provisional', 'construction_type': 'tam'},
        ]
    },
]


def get_morphemes_by_category(conn, category):
    """Get grammatical morphemes for a category."""
    return conn.execute('''
        SELECT form, gloss, function, frequency, position
        FROM grammatical_morphemes
        WHERE category = ?
        ORDER BY frequency DESC
    ''', (category,)).fetchall()


def get_examples_for_morpheme(conn, form, limit=3):
    """Get examples for a morpheme."""
    return conn.execute('''
        SELECT 
            e.tedim_text,
            e.segmented,
            e.glossed,
            e.kjv_text,
            e.source_id,
            e.quality
        FROM examples e
        JOIN grammatical_morphemes gm ON e.morpheme_id = gm.morpheme_id
        WHERE gm.form = ?
        ORDER BY e.quality
        LIMIT ?
    ''', (form, limit)).fetchall()


def get_constructions_by_type(conn, construction_type):
    """Get constructions of a specific type."""
    return conn.execute('''
        SELECT 
            construction_id,
            name,
            pattern,
            description,
            example_ids
        FROM constructions
        WHERE category = ? OR name LIKE ?
        ORDER BY name
    ''', (construction_type, f'%{construction_type}%')).fetchall()


def generate_morpheme_section(conn, category) -> str:
    """Generate content for a morpheme-based section."""
    morphemes = get_morphemes_by_category(conn, category)
    
    if not morphemes:
        return f"*No data available for {category}.*\n"
    
    lines = []
    lines.append(f"This section documents {len(morphemes)} items in the **{category}** category.\n")
    lines.append('')
    lines.append('| Form | Gloss | Function | Position | Frequency |')
    lines.append('|------|-------|----------|----------|-----------|')
    
    for m in morphemes[:20]:  # Limit to top 20
        lines.append(
            f"| {m['form']} | {m['gloss'] or '—'} | {m['function'] or '—'} | "
            f"{m['position'] or '—'} | {m['frequency']:,} |"
        )
    
    if len(morphemes) > 20:
        lines.append(f"\n*({len(morphemes) - 20} more items not shown)*\n")
    
    # Add example for top morpheme
    if morphemes:
        top = morphemes[0]
        examples = get_examples_for_morpheme(conn, top['form'], limit=2)
        if examples:
            lines.append('')
            lines.append(f"**Example: {top['form']} '{top['gloss']}'**\n")
            for ex in examples:
                lines.append(f"- {ex['tedim_text']}")
                if ex['segmented'] and ex['glossed']:
                    lines.append(f"  - *{ex['segmented']}* → '{ex['glossed']}'")
                if ex['kjv_text']:
                    lines.append(f"  - '{ex['kjv_text']}'")
                if ex['source_id']:
                    lines.append(f"  - ({format_reference(ex['source_id'])})")
                lines.append('')
    
    return '\n'.join(lines)


def generate_construction_section(conn, construction_type) -> str:
    """Generate content for a construction-based section."""
    constructions = get_constructions_by_type(conn, construction_type)
    
    if not constructions:
        return f"*No constructions documented for {construction_type}.*\n"
    
    lines = []
    lines.append(f"This section documents {len(constructions)} constructions.\n")
    
    for c in constructions:
        lines.append(f"**{c['name']}**\n")
        if c['pattern']:
            lines.append(f"Pattern: `{c['pattern']}`\n")
        if c['description']:
            lines.append(f"{c['description']}\n")
        if c['example_ids']:
            lines.append(f"Examples: {c['example_ids']}\n")
        lines.append('')
    
    return '\n'.join(lines)


def generate_section(conn, section) -> str:
    """Generate content for a section based on its type."""
    status = section['status']
    
    # Status markers
    status_markers = {
        'stable': '✓',
        'provisional': '⚠',
        'stub': '❌',
    }
    marker = status_markers.get(status, '?')
    
    lines = []
    lines.append(f"### {section['id']} {section['title']} [{marker}]\n")
    
    # Status note
    if status == 'stub':
        lines.append('> **GAP:** This section is not yet documented. Placeholder only.\n')
        lines.append('')
        return '\n'.join(lines)
    elif status == 'provisional':
        lines.append('> **Provisional:** This section has partial documentation and needs review.\n')
        lines.append('')
    
    # Generate content based on section type
    if 'morpheme_category' in section:
        content = generate_morpheme_section(conn, section['morpheme_category'])
        lines.append(content)
    elif 'construction_type' in section:
        content = generate_construction_section(conn, section['construction_type'])
        lines.append(content)
    else:
        # Generic placeholder
        lines.append('*Content to be developed.*\n')
    
    lines.append('')
    return '\n'.join(lines)


def generate_grammar_draft(conn) -> str:
    """Generate the complete grammar draft."""
    
    provenance = generate_provenance_header(
        'scripts/generate_grammar_draft.py',
        ['data/ctd_backend.db'],
        'make grammar-draft'
    )
    
    # Count status
    status_counts = {'stable': 0, 'provisional': 0, 'stub': 0}
    for chapter in GRAMMAR_CHAPTERS:
        for section in chapter['sections']:
            status_counts[section['status']] = status_counts.get(section['status'], 0) + 1
    
    total_sections = sum(status_counts.values())
    
    lines = [provenance]
    lines.append('# Tedim Chin Grammar Draft')
    lines.append('')
    lines.append(f'**Generated:** {datetime.now().isoformat()}')
    lines.append('')
    
    # Status summary
    lines.append('## Document Status')
    lines.append('')
    lines.append('| Status | Count | Meaning |')
    lines.append('|--------|-------|---------|')
    lines.append(f"| ✓ Stable | {status_counts['stable']} | Well-documented with examples |")
    lines.append(f"| ⚠ Provisional | {status_counts['provisional']} | Documented but needs review |")
    lines.append(f"| ❌ Stub | {status_counts['stub']} | Placeholder - not yet written |")
    lines.append('')
    
    # Readiness
    stable_pct = 100 * status_counts['stable'] / total_sections if total_sections > 0 else 0
    complete_pct = 100 * (status_counts['stable'] + status_counts['provisional']) / total_sections if total_sections > 0 else 0
    
    lines.append('## Publication Readiness')
    lines.append('')
    lines.append(f'- **Stable sections:** {stable_pct:.1f}%')
    lines.append(f'- **Complete (stable + provisional):** {complete_pct:.1f}%')
    lines.append(f'- **Major gaps (stubs):** {status_counts["stub"]} sections')
    lines.append('')
    
    # Table of contents
    lines.append('---')
    lines.append('')
    lines.append('## Table of Contents')
    lines.append('')
    
    for chapter in GRAMMAR_CHAPTERS:
        lines.append(f"**{chapter['id']}. {chapter['title']}**")
        for section in chapter['sections']:
            marker = {'stable': '✓', 'provisional': '⚠', 'stub': '❌'}.get(section['status'], '?')
            lines.append(f"  - {section['id']} {section['title']} [{marker}]")
        lines.append('')
    
    # Chapters
    lines.append('---')
    lines.append('')
    
    for chapter in GRAMMAR_CHAPTERS:
        lines.append(f"## {chapter['id']}. {chapter['title']}")
        lines.append('')
        
        for section in chapter['sections']:
            section_content = generate_section(conn, section)
            lines.append(section_content)
        
        lines.append('---')
        lines.append('')
    
    # Gap summary
    lines.append('## Gap Summary')
    lines.append('')
    lines.append('The following sections need further work before publication:')
    lines.append('')
    
    lines.append('### Stubs (highest priority)')
    for chapter in GRAMMAR_CHAPTERS:
        for section in chapter['sections']:
            if section['status'] == 'stub':
                lines.append(f"- {section['id']} {section['title']}")
    lines.append('')
    
    lines.append('### Provisional (review needed)')
    for chapter in GRAMMAR_CHAPTERS:
        for section in chapter['sections']:
            if section['status'] == 'provisional':
                lines.append(f"- {section['id']} {section['title']}")
    lines.append('')
    
    lines.append('---')
    lines.append('')
    lines.append('*This grammar was generated from the Tedim Chin backend database.')
    lines.append('Sections marked with ❌ are placeholders for future work.*')
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Generate Tedim grammar draft'
    )
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--output', default='output/grammar/draft_grammar.md',
                        help='Output path')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        sys.exit(1)
    
    print(f"Loading backend from {args.db}...")
    conn = get_connection(args.db)
    
    print("Generating grammar draft...")
    report = generate_grammar_draft(conn)
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(report)
    
    print(f"  → {args.output}")
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
