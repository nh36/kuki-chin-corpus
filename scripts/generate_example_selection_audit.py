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
    audit_examples_for_entry,
    backend_counts,
    format_example_block,
    grouped_topic_entries,
    load_source_map,
    render_source_of_truth_lines,
)
from report_utils import generate_provenance_header


def render_candidate_block(candidate: dict) -> list[str]:
    """Render one audited candidate with status metadata."""
    lines = [f"**Status:** {candidate['selection_status']}"]
    lines.append(f"**Drafting quality:** {candidate['drafting_quality']}")
    lines.append(f"**Reason:** {candidate['selection_reason']}")
    if candidate.get('matched_fields'):
        lines.append(f"**Matched fields:** {', '.join(candidate['matched_fields'])}")
    if candidate.get('selection_note'):
        lines.append(f"**Note:** {candidate['selection_note']}")
    if candidate.get('used_in_grammar'):
        lines.append('**Used in grammar output:** yes')
    lines.append('')
    lines.extend(format_example_block(candidate))
    return lines


def render_topic_audit(entry: dict, conn: sqlite3.Connection) -> list[str]:
    """Render audit details for one mapped topic."""
    candidates = audit_examples_for_entry(conn, entry, limit=3)
    selected_safe = [item for item in candidates if item.get('used_in_grammar')]
    safe_but_unused = [
        item for item in candidates
        if item['selection_status'] == 'safe' and not item.get('used_in_grammar')
    ]
    fallback_only = [item for item in candidates if item['selection_status'] == 'fallback only']
    rejected = [item for item in candidates if item['selection_status'] == 'rejected']

    lines = [f"### {entry['title']}", '']
    lines.append(f"**Topic ID:** `{entry['topic_id']}`")
    lines.append('')
    if selected_safe:
        lines.append(f"**Drafting status:** {len(selected_safe)} draft-ready example(s) selected for grammar output.")
    else:
        lines.append('**Drafting status:** No draft-ready backend example selected.')
    lines.append('')

    if not candidates:
        lines.append('- No example candidate matched the current selection rules.')
        lines.append('')
        return lines

    sections = [
        ('Selected safe examples', selected_safe),
        ('Other safe candidates not used in grammar', safe_but_unused),
        ('Fallback-only candidates', fallback_only),
        ('Rejected candidates', rejected),
    ]

    for heading, items in sections:
        lines.append(f"**{heading}:**")
        if not items:
            lines.append('- None.')
            lines.append('')
            continue
        lines.append('')
        for item in items:
            lines.extend(render_candidate_block(item))

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
        '- Drafting policy: grammar outputs include only examples with `selection_status = safe` and `drafting_quality = exemplar` or `usable`.',
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
