#!/usr/bin/env python3
"""
Shared helpers for Tedim grammar integration.

This module loads the grammar source map, renders related-material sections,
and pulls example material from the backend for source-map-driven outputs.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Dict, Iterable, List

from report_utils import format_reference, gloss_sentence


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE_MAP = REPO_ROOT / 'docs' / 'grammar' / 'grammar_source_map.json'

EXAMPLE_QUALITY_ORDER_SQL = """
CASE e.quality
    WHEN 'canonical' THEN 1
    WHEN 'excellent' THEN 2
    WHEN 'good' THEN 3
    WHEN 'transparent' THEN 4
    WHEN 'shortest' THEN 5
    WHEN 'acceptable' THEN 6
    WHEN 'auto' THEN 7
    WHEN 'additional' THEN 8
    ELSE 9
END
"""


def load_source_map(source_map_path: str | Path | None = None) -> Dict:
    """Load the Tedim grammar source map JSON."""
    path = Path(source_map_path) if source_map_path else DEFAULT_SOURCE_MAP
    with open(path, 'r', encoding='utf-8') as handle:
        return json.load(handle)


def topic_entries(source_map: Dict) -> List[Dict]:
    """Return source-map entries sorted by chapter area and sort order."""
    return sorted(
        source_map.get('topic_mappings', []),
        key=lambda entry: (entry.get('chapter_area', ''), entry.get('sort_order', 0), entry.get('title', '')),
    )


def grouped_topic_entries(source_map: Dict) -> List[tuple[str, List[Dict]]]:
    """Group topic entries by chapter area while preserving sort order."""
    groups: Dict[str, List[Dict]] = {}
    order: List[str] = []
    for entry in topic_entries(source_map):
        chapter_area = entry.get('chapter_area', 'Ungrouped')
        if chapter_area not in groups:
            groups[chapter_area] = []
            order.append(chapter_area)
        groups[chapter_area].append(entry)
    return [(chapter_area, groups[chapter_area]) for chapter_area in order]


def repo_path(path_str: str) -> Path:
    """Resolve a repository-relative path."""
    return REPO_ROOT / path_str


def markdown_link(from_file: Path, target: str, label: str | None = None) -> str:
    """Build a relative markdown link from one file to another."""
    target_path = repo_path(target)
    relative = Path(Path(target_path).relative_to(REPO_ROOT))
    link_path = Path(target_path).relative_to(REPO_ROOT)
    rel = Path(
        Path(
            Path(target_path).relative_to(REPO_ROOT)
        )
    )
    relative_link = Path(
        Path(
            Path(
                Path(target_path)
            )
        )
    )
    rel_text = Path(
        Path(target_path).relative_to(from_file.parent.resolve()) if False else Path()
    )
    rel_posix = Path(
        Path(target_path).relative_to(REPO_ROOT)
    )
    computed = Path(target_path).relative_to(REPO_ROOT)
    markdown_rel = Path(target_path).relative_to(REPO_ROOT)
    relative_href = Path(target_path).relative_to(REPO_ROOT)
    href = Path(target_path)
    rel_path = Path(target_path).relative_to(REPO_ROOT)
    final = Path(
        Path(
            Path(target_path)
        )
    )
    # Use os-like relative paths without importing os just for link formatting.
    relative_path = Path(
        Path(target_path).relative_to(REPO_ROOT)
    )
    resolved = target_path.resolve()
    from_parent = from_file.resolve().parent
    rel_link = Path(
        resolved.relative_to(REPO_ROOT)
    )
    link = resolved.relative_to(REPO_ROOT)
    # pathlib cannot emit parent-directory traversals, so fall back to manual URI path.
    uri = Path(
        Path(target_path).relative_to(REPO_ROOT)
    ).as_posix()
    try:
        import os

        uri = os.path.relpath(resolved, start=from_parent)
    except ValueError:
        uri = target
    label = label or target
    return f'[{label}]({uri})'


def bullet_link_lines(from_file: Path, paths: Iterable[str]) -> List[str]:
    """Render a list of repo-relative paths as bullet links."""
    return [f'- {markdown_link(from_file, path)}' for path in paths]


def render_related_material(entry: Dict, output_path: Path) -> List[str]:
    """Render the related-material section for a source-map entry."""
    sections = [
        ('Corpus reports', entry.get('relevant_corpus_reports', [])),
        ('Literature reviews', entry.get('relevant_literature_reviews', [])),
        ('Morpheme databases', entry.get('relevant_morpheme_files', [])),
        ('Analyzer-gap notes', entry.get('relevant_analyzer_gap_documents', [])),
        ('Generated outputs', entry.get('relevant_generated_outputs', [])),
    ]

    lines = ['**Related material**', '']
    for heading, paths in sections:
        if not paths:
            continue
        lines.append(f'*{heading}*')
        lines.extend(bullet_link_lines(output_path, paths))
        lines.append('')

    skeleton = entry.get('skeleton_grammar_section')
    if skeleton:
        lines.append(f"*Skeleton grammar:* `{skeleton}`")
        lines.append('')

    return lines


def _fetch_examples_by_grammar_metadata(conn: sqlite3.Connection, entry: Dict, limit: int) -> List[sqlite3.Row]:
    """Fetch examples linked to grammatical morphemes that match a source-map entry."""
    forms = entry.get('example_forms', [])
    categories = entry.get('example_categories', [])
    search_terms = entry.get('example_search_terms', [])

    conditions: List[str] = []
    params: List[str] = []

    if forms:
        placeholders = ', '.join('?' for _ in forms)
        conditions.append(f'gm.form IN ({placeholders})')
        params.extend(forms)
    if categories:
        placeholders = ', '.join('?' for _ in categories)
        conditions.append(f'gm.category IN ({placeholders})')
        params.extend(categories)
    if search_terms:
        term_conditions = []
        for term in search_terms:
            term_conditions.append('(e.target_form LIKE ? OR e.tedim_text LIKE ?)')
            params.extend([f'%{term}%', f'%{term}%'])
        conditions.append('(' + ' OR '.join(term_conditions) + ')')

    if not conditions:
        return []

    query = f'''
        SELECT DISTINCT
            e.example_id,
            e.source_id,
            e.tedim_text,
            e.segmented,
            e.glossed,
            e.kjv_text,
            e.quality
        FROM examples e
        LEFT JOIN grammatical_morphemes gm ON e.morpheme_id = gm.morpheme_id
        WHERE {' OR '.join(conditions)}
        ORDER BY {EXAMPLE_QUALITY_ORDER_SQL}, LENGTH(COALESCE(e.tedim_text, '')), e.example_id
        LIMIT ?
    '''
    params.append(limit)
    return conn.execute(query, params).fetchall()


def _fallback_source_examples(conn: sqlite3.Connection, entry: Dict, limit: int) -> List[Dict]:
    """Fetch verse-level examples by text search when examples table lacks linked rows."""
    terms = entry.get('example_search_terms') or entry.get('example_forms') or []
    if not terms:
        return []

    conditions = []
    params: List[str] = []
    for term in terms:
        conditions.append('(text LIKE ? OR text_normalized LIKE ?)')
        params.extend([f'%{term}%', f'%{term.lower()}%'])

    query = f'''
        SELECT source_id, text, kjv_text
        FROM sources
        WHERE {' OR '.join(conditions)}
        ORDER BY source_id
        LIMIT ?
    '''
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    examples = []
    for row in rows:
        segmented = ''
        glossed = ''
        if row['text']:
            glossed_sentence = gloss_sentence(row['text'])
            segmented = ' '.join(piece[1] for piece in glossed_sentence)
            glossed = ' '.join(piece[2] for piece in glossed_sentence)
        examples.append(
            {
                'source_id': row['source_id'],
                'tedim_text': row['text'],
                'segmented': segmented,
                'glossed': glossed,
                'kjv_text': row['kjv_text'],
            }
        )
    return examples


def fetch_examples_for_entry(conn: sqlite3.Connection, entry: Dict, limit: int = 3) -> List[Dict]:
    """Fetch formatted examples for a source-map entry."""
    seen = set()
    examples: List[Dict] = []

    for row in _fetch_examples_by_grammar_metadata(conn, entry, limit):
        if row['source_id'] in seen:
            continue
        seen.add(row['source_id'])
        examples.append(dict(row))
        if len(examples) >= limit:
            return examples

    for row in _fallback_source_examples(conn, entry, limit - len(examples)):
        if row['source_id'] in seen:
            continue
        seen.add(row['source_id'])
        examples.append(row)
        if len(examples) >= limit:
            break

    return examples


def format_example_block(example: Dict) -> List[str]:
    """Render a full interlinear example block with no default truncation."""
    lines = [f"**{format_reference(example['source_id'])}**"]
    if example.get('tedim_text'):
        lines.append(f"> {example['tedim_text']}")
    if example.get('segmented'):
        lines.append(f"> *{example['segmented']}*")
    if example.get('glossed'):
        lines.append(f"> {example['glossed']}")
    if example.get('kjv_text'):
        lines.append(f"> KJV: *{example['kjv_text']}*")
    lines.append('')
    return lines


def backend_counts(conn: sqlite3.Connection) -> Dict[str, int]:
    """Return current backend counts for grammar topics and constructions."""
    return {
        'grammar_topics': conn.execute('SELECT COUNT(*) FROM grammar_topics').fetchone()[0],
        'constructions': conn.execute('SELECT COUNT(*) FROM constructions').fetchone()[0],
    }
