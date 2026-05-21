#!/usr/bin/env python3
"""
Generate a Tedim backend example-selection audit.

This audit shows which examples were allowed into grammar-drafting outputs,
which ones were kept only as fallback/review candidates, and why.
"""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

from grammar_integration import (
    backend_counts,
    format_example_block,
    grouped_topic_entries,
    load_source_map,
    render_source_of_truth_lines,
    select_examples_for_entry,
)
from report_utils import generate_provenance_header


def render_topic_audit(entry: dict, conn: sqlite3.Connection) -> list[str]:
    """Render audit details for one mapped topic."""
    selections = select_examples_for_entry(conn, entry, limit=3, include_non_safe=True)
    safe_count = sum(1 for item in selections if item['selection_status'] == 'safe')

    lines = [f"### {entry['title']}", '']
    lines.append(f"**Topic ID:** `{entry['topic_id']}`")
    lines.append('')
    if safe_count:
        lines.append(f"**Drafting status:** {safe_count} safe example(s) selected for grammar output.")
    else:
        lines.append('**Drafting status:** No safe backend example selected.')
    lines.append('')

    if not selections:
        lines.append('- No example candidate matched the current selection rules.')
        lines.append('')
        return lines

    for selection in selections:
        lines.append(f"**Status:** {selection['selection_status']}")
        lines.append(f"**Why selected:** {selection['selection_reason']}")
        lines.append(f"**Matched fields:** {', '.join(selection['matched_fields'])}")
        if selection.get('selection_note'):
            lines.append(f"**Note:** {selection['selection_note']}")
        lines.append('')
        lines.extend(format_example_block(selection))

    return lines


def generate_audit(db_path: str, source_map_path: str, output_path: Path) -> str:
    """Generate the example-selection audit markdown."""
    source_map = load_source_map(source_map_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    counts = backend_counts(conn)

    lines = [
        generate_provenance_header(
            'scripts/generate_example_selection_audit.py',
            inputs=[db_path, source_map_path],
            command='make grammar-reports',
        ).rstrip(),
        '# Tedim Example Selection Audit',
        '',
        'This audit records how the grammar integration layer selected backend examples for each mapped Tedim grammar topic.',
        '',
        '## Backend layer status',
        '',
        f"- Grammar topics in backend: **{counts['grammar_topics']}**",
        f"- Constructions in backend: **{counts['constructions']}**",
        *render_source_of_truth_lines(source_map, output_path),
        '- Drafting policy: grammar outputs include only examples marked **safe** here; fallback-only candidates remain in this audit and are not used in drafting output.',
        '',
    ]

    for chapter_area, entries in grouped_topic_entries(source_map):
        lines.append(f"## {chapter_area}")
        lines.append('')
        for entry in entries:
            lines.extend(render_topic_audit(entry, conn))

    conn.close()
    return '\n'.join(lines).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='Generate Tedim example-selection audit')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Database path')
    parser.add_argument('--source-map', default='docs/grammar/grammar_source_map.json', help='Source map JSON path')
    parser.add_argument('--output', default='output/grammar/example_selection_audit.md', help='Output file')
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = generate_audit(args.db, args.source_map, output_path)
    output_path.write_text(content, encoding='utf-8')
    print(f"Generated {args.output}")


if __name__ == '__main__':
    main()
