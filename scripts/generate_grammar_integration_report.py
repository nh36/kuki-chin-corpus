#!/usr/bin/env python3
"""
Generate the Tedim grammar integration report.

This report bridges the current backend layer and the older Tedim grammar
materials so grammar writing can route each topic to the right legacy sources.
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
    markdown_link,
)
from report_utils import generate_provenance_header


ANALYZER_GAP_AUDIT = [
    {
        'gap': '-sak causative vs benefactive',
        'status': 'partly addressed',
        'evidence': 'Regression coverage exists in tests/test_sak_caus_benf.py, but older gap docs still flag the distinction and generated derivational summaries still collapse many -sak uses.',
        'sources': [
            'tests/test_sak_caus_benf.py',
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/reports/05-verb-08-derivational.md',
        ],
    },
    {
        'gap': 'Agreement vs possession in ka-/na-/a-',
        'status': 'probably addressed, needs verification',
        'evidence': 'Regression coverage exists in tests/test_prefix_agr_poss.py, but legacy analyzer-gap notes still treat the split as unfinished and the grammar workflow has not yet surfaced that verification automatically.',
        'sources': [
            'tests/test_prefix_agr_poss.py',
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/01-prefixes.md',
        ],
    },
    {
        'gap': 'hong- inverse constraints',
        'status': 'partly addressed',
        'evidence': 'hong- is documented in reports and disambiguation notes, but the older gap analysis still calls out co-occurrence constraints that are not yet surfaced as a dedicated backend construction or explicit grammar-routing check.',
        'sources': [
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md',
            'docs/grammar/reports/05-verb-03-agreement.md',
        ],
    },
    {
        'gap': 'Missing -suk / -phei directional coverage',
        'status': 'probably addressed, needs verification',
        'evidence': 'Directional regression coverage exists in tests/test_directional_suffixes.py, but the older gap docs and some generated summaries still need reconciliation with the current analyzer output.',
        'sources': [
            'tests/test_directional_suffixes.py',
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/04-directional.md',
        ],
    },
    {
        'gap': '-thei / -theih abilitative allomorphy',
        'status': 'probably addressed, needs verification',
        'evidence': 'Regression coverage exists in tests/test_thei_theih_allomorphy.py, but legacy analyzer-gap materials still describe abilitative distinctions as unfinished.',
        'sources': [
            'tests/test_thei_theih_allomorphy.py',
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/05-modal.md',
        ],
    },
    {
        'gap': 'Habitual and experiential markers',
        'status': 'probably addressed, needs verification',
        'evidence': 'Regression coverage exists in tests/test_habitual_markers.py, but the gap documents predate that verification and have not been retired or updated.',
        'sources': [
            'tests/test_habitual_markers.py',
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/03-aspect.md',
        ],
    },
    {
        'gap': 'Applicative -pih constraints',
        'status': 'partly addressed',
        'evidence': 'Applicative morphology is present in reports and tests, but the literature-specific argument-structure constraints remain mostly in legacy docs rather than a current backend topic model.',
        'sources': [
            'docs/grammar/morphemes/06-derivational.md',
            'docs/grammar/lit-reviews/05-verb-09-valency-lit.md',
            'tests/test_vp_slots.py',
        ],
    },
    {
        'gap': 'Tone distinction in -a case marker',
        'status': 'blocked',
        'evidence': 'The gap documents explicitly mark this as blocked because tone is not preserved in the corpus export layer.',
        'sources': [
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/02-case-markers.md',
        ],
    },
    {
        'gap': '-pah / -pak / -lawh conditioning',
        'status': 'open',
        'evidence': 'The analyzer-gap summary still lists complete conditioning for these variants as unfinished, and no current regression target in the Tedim test suite closes that gap.',
        'sources': [
            'docs/grammar/README_ANALYZER_GAPS.md',
            'docs/grammar/morphemes/05-modal.md',
        ],
    },
]


def render_gap_audit(output_path: Path) -> list[str]:
    """Render analyzer-gap audit table and evidence list."""
    lines = [
        '## Analyzer-gap audit',
        '',
        '| Gap | Status | Evidence |',
        '|-----|--------|----------|',
    ]
    for item in ANALYZER_GAP_AUDIT:
        lines.append(f"| {item['gap']} | {item['status']} | {item['evidence']} |")
    lines.append('')

    for item in ANALYZER_GAP_AUDIT:
        lines.append(f"### {item['gap']}")
        lines.append(f"**Status:** {item['status']}")
        lines.append('')
        lines.append(item['evidence'])
        lines.append('')
        lines.append('**Supporting files**')
        for source in item['sources']:
            lines.append(f"- {markdown_link(output_path, source)}")
        lines.append('')
    return lines


def render_entry(entry: dict, conn: sqlite3.Connection, output_path: Path) -> list[str]:
    """Render one source-map topic entry."""
    lines = [f"### {entry['title']}", '']

    backend_refs = entry.get('backend_topic_ids', []) + entry.get('construction_ids', [])
    if backend_refs:
        lines.append(f"**Backend topics/constructions:** {', '.join(f'`{ref}`' for ref in backend_refs)}")
    else:
        lines.append('**Backend topics/constructions:** _No backend topic IDs or construction IDs are populated yet._')
    lines.append('')

    if entry.get('relevant_morphemes'):
        lines.append(f"**Relevant morphemes:** {', '.join(f'`{item}`' for item in entry['relevant_morphemes'])}")
        lines.append('')

    lines.append('**Mapped legacy source files**')
    for source in entry.get('relevant_source_files', []):
        lines.append(f"- {markdown_link(output_path, source)}")
    lines.append('')

    section_map = [
        ('Corpus report evidence', entry.get('relevant_corpus_reports', [])),
        ('Literature-review files', entry.get('relevant_literature_reviews', [])),
        ('Morpheme database files', entry.get('relevant_morpheme_files', [])),
        ('Analyzer-gap files', entry.get('relevant_analyzer_gap_documents', [])),
    ]

    for heading, paths in section_map:
        lines.append(f"**{heading}:**")
        if paths:
            for path in paths:
                lines.append(f"- {markdown_link(output_path, path)}")
        else:
            lines.append('- _No dedicated file mapped._')
        lines.append('')

    lines.append(f"**Skeleton grammar coverage:** `{entry.get('skeleton_grammar_section', 'No direct section mapped')}`")
    lines.append('')

    examples = fetch_examples_for_entry(conn, entry, limit=2)
    lines.append('**Sample backend-linked examples:**')
    if examples:
        lines.append('')
        for example in examples:
            lines.extend(format_example_block(example))
    else:
        lines.append('- _No linked backend examples were found for this topic yet._')
        lines.append('')

    missing = []
    if not backend_refs:
        missing.append('No backend topic/construction IDs are populated for this topic yet.')
    if not entry.get('relevant_literature_reviews'):
        missing.append('No dedicated literature-review file is mapped.')
    if not entry.get('relevant_morpheme_files'):
        missing.append('No dedicated morpheme database file is mapped.')
    if not entry.get('relevant_analyzer_gap_documents'):
        missing.append('No analyzer-gap document is mapped.')

    lines.append('**Missing links:**')
    if missing:
        for item in missing:
            lines.append(f'- {item}')
    else:
        lines.append('- _No immediate routing gap identified._')
    lines.append('')

    lines.append('**Stale or uncertain material needing review:**')
    lines.append(f"- {entry.get('notes_human_review', 'No additional note.')}")
    lines.append('')
    return lines


def generate_report(db_path: str, source_map_path: str, output_path: Path) -> str:
    """Generate the full grammar integration report."""
    source_map = load_source_map(source_map_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    counts = backend_counts(conn)

    lines = [
        generate_provenance_header(
            'scripts/generate_grammar_integration_report.py',
            inputs=[db_path, source_map_path],
            command='make grammar-integration-report',
        ).rstrip(),
        '# Tedim Grammar Integration Report',
        '',
        'This dashboard maps current Tedim grammar topics to legacy source files so the existing grammar, dictionary, and chrestomathy materials can feed a unified drafting workflow.',
        '',
        '## Backend layer status',
        '',
        f"- Grammar topics in backend: **{counts['grammar_topics']}**",
        f"- Constructions in backend: **{counts['constructions']}**",
        '- Integration model: source-map-driven routing from legacy Tedim materials into backend-aware drafting outputs.',
        '',
    ]

    if counts['grammar_topics'] == 0 and counts['constructions'] == 0:
        lines.extend([
            '> **Current limitation:** the `grammar_topics` and `constructions` tables are still empty in the Tedim backend, so this report maps legacy sources to topic IDs conceptually and records the missing backend links explicitly.',
            '',
        ])

    for chapter_area, entries in grouped_topic_entries(source_map):
        lines.append(f"## {chapter_area}")
        lines.append('')
        for entry in entries:
            lines.extend(render_entry(entry, conn, output_path))

    lines.extend(render_gap_audit(output_path))
    conn.close()
    return '\n'.join(lines).rstrip() + '\n'


def main():
    parser = argparse.ArgumentParser(description='Generate Tedim grammar integration report')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Database path')
    parser.add_argument('--source-map', default='docs/grammar/grammar_source_map.json', help='Source map JSON path')
    parser.add_argument('--output', default='output/grammar_integration_report.md', help='Output markdown path')
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate_report(args.db, args.source_map, output_path), encoding='utf-8')
    print(f'Generated {args.output}')


if __name__ == '__main__':
    main()
