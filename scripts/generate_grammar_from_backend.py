#!/usr/bin/env python3
"""
Generate Tedim grammar documentation from the backend/source-map integration layer.

When the backend `grammar_topics` and `constructions` tables are empty, this
script falls back to the Tedim grammar source map so the generated grammar can
still route each major topic to the existing grammar materials.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from grammar_integration import (
    backend_counts,
    fetch_examples_for_entry,
    format_example_block,
    grouped_topic_entries,
    load_source_map,
    render_source_of_truth_lines,
    render_related_material,
)
from report_utils import generate_provenance_header


def render_source_map_entry(entry: dict, conn: sqlite3.Connection, output_path: Path, compact: bool = False) -> list[str]:
    """Render a source-map entry as a grammar section."""
    lines = [f"### {entry['title']}", '']

    backend_refs = entry.get('backend_topic_ids', []) + entry.get('construction_ids', [])
    if backend_refs:
        lines.append(f"**Backend topics/constructions:** {', '.join(f'`{item}`' for item in backend_refs)}")
        lines.append('')

    if entry.get('relevant_morphemes'):
        lines.append(f"**Relevant morphemes:** {', '.join(f'`{item}`' for item in entry['relevant_morphemes'])}")
        lines.append('')

    lines.extend(render_related_material(entry, output_path))

    examples = fetch_examples_for_entry(conn, entry, limit=1 if compact else 2)
    if examples:
        lines.append('**Examples**')
        lines.append('')
        for example in examples:
            lines.extend(format_example_block(example))
    else:
        lines.append('**Examples**')
        lines.append('')
        lines.append('- No safe backend example selected.')
        lines.append('')

    lines.append('**Human review**')
    lines.append(f"- {entry.get('notes_human_review', 'No additional note.')}")
    lines.append('')
    return lines


def render_backend_inventory(conn: sqlite3.Connection) -> list[str]:
    """Render current backend construction inventory without duplicating sections."""
    lines = ['## Backend construction inventory', '']
    rows = list(conn.execute('''
        SELECT construction_id, name, category, pattern, frequency
        FROM constructions
        ORDER BY category, frequency DESC, construction_id
    '''))
    if not rows:
        lines.append('_No backend constructions are populated in the current Tedim database._')
        lines.append('')
        return lines

    lines.append('| ID | Name | Category | Pattern | Frequency |')
    lines.append('|----|------|----------|---------|-----------|')
    for row in rows:
        lines.append(f"| `{row['construction_id']}` | {row['name']} | {row['category']} | `{row['pattern']}` | {row['frequency']:,} |")
    lines.append('')
    return lines


def generate_full_grammar(conn: sqlite3.Connection, source_map: dict, output_path: Path) -> str:
    """Generate a full grammar draft driven by the Tedim source map."""
    counts = backend_counts(conn)
    lines = [
        generate_provenance_header(
            'scripts/generate_grammar_from_backend.py',
            inputs=['data/ctd_backend.db', 'docs/grammar/grammar_source_map.json'],
            command='make grammar-reports',
        ).rstrip(),
        '# Tedim Chin Grammar',
        '',
        'Generated from the Tedim backend and grammar source map.',
        '',
        f"- Backend grammar topics: **{counts['grammar_topics']}**",
        f"- Backend constructions: **{counts['constructions']}**",
        *render_source_of_truth_lines(source_map, output_path),
        '',
    ]

    if counts['grammar_topics'] == 0 and counts['constructions'] == 0:
        lines.extend([
            '> **Source of truth:** `docs/grammar/grammar_source_map.json` is the canonical Tedim topic/construction layer. The backend `grammar_topics` and `constructions` tables exist in the Tedim database schema but are not populated by the current migration pipeline.',
            '',
        ])

    for chapter_area, entries in grouped_topic_entries(source_map):
        lines.append(f"## {chapter_area}")
        lines.append('')
        for entry in entries:
            lines.extend(render_source_map_entry(entry, conn, output_path, compact=False))

    lines.extend(render_backend_inventory(conn))
    lines.append('*Generated from the Tedim backend/source-map integration layer*')
    return '\n'.join(lines).rstrip() + '\n'


def generate_constructions_report(conn: sqlite3.Connection, source_map: dict, output_path: Path) -> str:
    """Generate a focused topic/construction routing report."""
    counts = backend_counts(conn)
    lines = [
        generate_provenance_header(
            'scripts/generate_grammar_from_backend.py',
            inputs=['data/ctd_backend.db', 'docs/grammar/grammar_source_map.json'],
            command='make grammar-reports',
        ).rstrip(),
        '# Tedim Chin Constructions',
        '',
        'This report routes Tedim grammar topics and constructions to the legacy materials that support grammar writing.',
        '',
        f"- Backend grammar topics: **{counts['grammar_topics']}**",
        f"- Backend constructions: **{counts['constructions']}**",
        *render_source_of_truth_lines(source_map, output_path),
        '',
    ]

    if counts['grammar_topics'] == 0 and counts['constructions'] == 0:
        lines.extend([
            '> **Source of truth:** `docs/grammar/grammar_source_map.json` is the canonical Tedim topic/construction layer. The backend `grammar_topics` and `constructions` tables exist in the Tedim database schema but are not populated by the current migration pipeline.',
            '',
        ])

    for chapter_area, entries in grouped_topic_entries(source_map):
        lines.append(f"## {chapter_area}")
        lines.append('')
        for entry in entries:
            lines.extend(render_source_map_entry(entry, conn, output_path, compact=True))

    lines.extend(render_backend_inventory(conn))
    return '\n'.join(lines).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='Generate grammar documentation from backend/source map')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Database path')
    parser.add_argument('--source-map', default='docs/grammar/grammar_source_map.json', help='Source map JSON path')
    parser.add_argument('--output', default='output/grammar/grammar_constructions.md', help='Output file')
    parser.add_argument('--full', action='store_true', help='Generate full grammar (vs constructions only)')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    source_map = load_source_map(args.source_map)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.full:
        content = generate_full_grammar(conn, source_map, output_path)
    else:
        content = generate_constructions_report(conn, source_map, output_path)

    output_path.write_text(content, encoding='utf-8')
    print(f"Generated {args.output}")
    print("\nStats:")
    counts = backend_counts(conn)
    print(f"  Constructions: {counts['constructions']}")
    print(f"  Grammar topics: {counts['grammar_topics']}")
    print(f"  Source-map topics: {len(source_map.get('topic_mappings', []))}")
    conn.close()


if __name__ == '__main__':
    main()
