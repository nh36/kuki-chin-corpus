#!/usr/bin/env python3
"""
Shared helpers for Tedim grammar integration.

This module loads the Tedim grammar source map, renders related-material
sections, and pulls backend examples conservatively enough for grammar-drafting
workflows. Example selection distinguishes technical safety from drafting
quality so grammar outputs can stay stricter than the audit dashboard.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
from pathlib import Path
from typing import Any, Dict, Iterable, List

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

DRAFT_READY_QUALITIES = {'exemplar', 'usable'}

DEFAULT_EXAMPLE_FILTERS = {
    'pronominal-prefixes': {
        'example_glosses': ['1SG→3', '3→1'],
    },
    'ergative-marking': {
        'example_glosses': ['ERG'],
    },
    'locative-marking': {
        'example_glosses': ['LOC'],
    },
    'ablative-marking': {
        'example_glosses': ['ABL'],
    },
    'comitative-marking': {
        'example_glosses': ['COM'],
    },
    'verb-stem-alternation': {
        'example_search_terms': ['muh', 'theih', 'cih'],
    },
    'perfective-ta': {
        'example_glosses': ['PFV'],
    },
    'completive-zo': {
        'example_glosses': ['COMPL'],
    },
    'irrealis-ding': {
        'example_glosses': ['IRR'],
    },
    'ability-thei-theih': {
        'example_glosses': ['ABIL', 'ABIL.II'],
    },
    'directional-suffixes': {
        'example_search_terms': ['khia', 'khiat', 'lut', 'toh', 'suk', 'phei'],
    },
    'inverse-hong': {
        'example_glosses': ['3→1'],
    },
    'causative-sak': {
        'example_glosses': ['CAUS'],
    },
    'benefactive-sak': {
        'example_search_terms': ['muhsak', 'muh sak', 'cihsak', 'cih sak', 'theihsak', 'theih sak', 'tuahsak', 'tuah sak'],
    },
    'applicative-pih': {
        'example_glosses': ['APPL'],
    },
    'reflexive-ki': {
        'example_glosses': ['REFL'],
    },
    'negation-lo-kei': {
        'example_glosses': ['NEG', 'NEG.EMPH'],
    },
    'nominalization-na': {
        'example_glosses': ['NMLZ'],
    },
    'interrogative-hiam': {
        'example_glosses': ['Q'],
    },
    'declarative-hi': {
        'example_glosses': ['DECL'],
    },
    'topic-marker-pen': {
        'example_glosses': ['TOP'],
    },
    'major-subordination': {
        'example_search_terms': ['ciangin', 'dingin', 'hangin', 'ahih', 'leh'],
    },
}

STRICT_SELECTION_RULES = {
    'pronominal-prefixes': [
        {
            'name': '3SG agreement prefix a-',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 1,
            'morpheme_ids': ['a.3SG.pronominal_prefix'],
            'sense_ids': ['a.3SG.pronominal_prefix'],
            'target_forms': ['a'],
            'segmented_normalized': ['a'],
            'gloss_exact': ['3SG'],
        },
        {
            'name': '3SG possessive a',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 1,
            'morpheme_ids': ['a.3SG.POSS.function_word'],
            'target_forms': ['a'],
            'segmented_normalized': ['a'],
            'gloss_exact': ['3SG.POSS'],
        },
    ],
    'ergative-marking': [
        {
            'name': 'Reject current backend -in rows',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'morpheme_ids': ['in.ERG.case_marker'],
            'target_forms': ['in'],
            'reason_note': 'Current backend-linked -in examples attach ERG to lexical stems or clause-final material, so they are not reliable drafting examples for ergative case marking.',
        },
    ],
    'comitative-marking': [
        {
            'name': 'Plain comitative tawh',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['tawh.COM.case_marker'],
            'target_forms': ['tawh'],
            'segmented_exact': ['tawh'],
            'gloss_exact': ['COM'],
        },
    ],
    'declarative-hi': [
        {
            'name': 'Sentence-final declarative hi',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['hi.DECL.sentence_final'],
            'target_forms': ['hi'],
            'segmented_exact': ['hi'],
            'gloss_exact': ['DECL'],
        },
        {
            'name': 'Reject current hi rows with mismatched glossing',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'morpheme_ids': ['hi.DECL.sentence_final'],
            'target_forms': ['hi'],
            'reason_note': 'Current linked hi examples are still glossed as DECL.POSS or otherwise fail the sentence-final declarative filter.',
        },
    ],
    'directional-suffixes': [
        {
            'name': 'Draft-ready directional examples',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'segmented_query_terms': ['khen-khia', 'khia-suk', 'lawn-khia', 'phul-khia'],
            'segmented_exact': ['khen-khia', 'khia-suk', 'lawn-khia', 'phul-khia'],
            'gloss_tokens': ['out', 'exit', 'down'],
        },
        {
            'name': 'Technically directional but poor drafting examples',
            'status': 'safe',
            'drafting_quality': 'safe_but_poor',
            'max_examples': 4,
            'segmented_query_terms': ['-khia', '-khiat', '-lut', '-toh', '-suk', '-phei'],
            'segmented_contains': ['khia', 'khiat', 'lut', 'toh', 'suk', 'phei'],
            'gloss_tokens': ['out', 'exit', 'away', 'down', 'up', 'horiz', 'in'],
            'exclude_segmented_exact': ['khen-khia', 'khia-suk', 'lawn-khia', 'phul-khia'],
            'exclude_segmented_contains': ['tuni'],
            'exclude_gloss_tokens': ['nmlz'],
            'reason_note': 'The example contains directional morphology, but the lexical content is too opaque or too context-dependent to be a good grammar exemplar.',
        },
        {
            'name': 'Reject false directional Tuni-in examples',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'segmented_query_terms': ['tuni-in'],
            'segmented_exact': ['Tuni-in'],
            'reason_note': 'Tuni-in is a lexical time expression, not a directional suffix example.',
        },
        {
            'name': 'Directional fallback text search',
            'status': 'fallback only',
            'drafting_quality': 'review_only',
            'max_examples': 2,
            'text_search_terms': ['khia', 'khiat', 'lut', 'toh', 'suk', 'phei'],
            'reason_note': 'No additional draft-ready linked directional example was found, so these text-search hits remain review-only.',
        },
    ],
    'causative-sak': [
        {
            'name': 'Causative -sak with explicit CAUS gloss',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['sak.CAUS.tam_suffix'],
            'sense_ids': ['sak.CAUS.tam_suffix'],
            'target_forms': ['sak'],
            'segmented_contains': ['sak'],
            'gloss_tokens': ['caus'],
        },
    ],
    'benefactive-sak': [
        {
            'name': 'Benefactive -sak fallback text search',
            'status': 'fallback only',
            'drafting_quality': 'review_only',
            'max_examples': 2,
            'text_search_terms': ['muhsak', 'muh sak', 'cihsak', 'cih sak', 'theihsak', 'theih sak', 'tuahsak', 'tuah sak'],
            'reason_note': 'No distinct benefactive morpheme ID or sense ID is currently populated in the backend, so only text-search candidates are available.',
        },
    ],
    'ability-thei-theih': [
        {
            'name': 'Transparent abilitative examples',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['thei.ABIL.auxiliary', 'theih.ABIL.II.auxiliary'],
            'segmented_query_terms': ['mu-thei', 'pau-thei'],
            'segmented_exact': ['mu-thei-in', 'pau-thei-in'],
            'gloss_tokens': ['abil'],
        },
        {
            'name': 'Technically abilitative but poor drafting examples',
            'status': 'safe',
            'drafting_quality': 'safe_but_poor',
            'max_examples': 4,
            'morpheme_ids': ['thei.ABIL.auxiliary', 'theih.ABIL.II.auxiliary'],
            'segmented_query_terms': ['thei', 'theih'],
            'segmented_contains': ['thei', 'theih'],
            'gloss_tokens': ['abil'],
            'exclude_segmented_exact': ['mu-thei-in', 'pau-thei-in'],
            'reason_note': 'The example is technically abilitative, but extra derivational or discourse material makes it a poor grammar exemplar.',
        },
        {
            'name': 'Ability fallback text search',
            'status': 'fallback only',
            'drafting_quality': 'review_only',
            'max_examples': 2,
            'text_search_terms': ['thei', 'theih'],
            'reason_note': 'No additional transparent linked abilitative example was found, so these candidates remain review-only.',
        },
    ],
    'nominalization-na': [
        {
            'name': 'Deverbal -na nominalization',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['na.NMLZ.nominalizer'],
            'sense_ids': ['na.NMLZ.nominalizer'],
            'source_ids': ['01002009'],
            'segmented_exact': ['nuntak-na'],
            'gloss_exact': ['live-NMLZ'],
        },
        {
            'name': 'Reject opaque or lexicalized -na examples',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 4,
            'morpheme_ids': ['na.NMLZ.nominalizer'],
            'segmented_exact': ['pa-na', 'ni-suah-na'],
            'reason_note': 'The backend links these rows to NMLZ, but they are too lexicalized or semantically opaque to use as drafting examples for productive nominalization.',
        },
    ],
    'agentive-pa-mi': [
        {
            'name': 'Clear agent nominalization in -pa',
            'status': 'safe',
            'drafting_quality': 'exemplar',
            'max_examples': 1,
            'source_ids': ['42018010'],
            'segmented_exact': ['siah-dong-pa'],
            'gloss_exact': ['tax-collect-AGT'],
        },
        {
            'name': 'Other agentive -pa/-mi candidates',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'segmented_query_terms': ['-pa', '-mi'],
            'segmented_contains': ['pa', 'mi'],
            'gloss_tokens': ['agt', 'nmlz.ag'],
            'exclude_segmented_exact': ['siah-dong-pa'],
        },
        {
            'name': 'Reject lexical -pa/-mi endings',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 4,
            'segmented_query_terms': ['-pa', '-mi'],
            'segmented_contains': ['pa', 'mi'],
            'reason_note': 'The example contains -pa/-mi on the surface, but it is lexical, gender-marking, or otherwise unrelated to productive agent nominalization.',
        },
    ],
    'interrogative-hiam': [
        {
            'name': 'Ordinary interrogative hiam',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['hiam.Q.sentence_final'],
            'target_forms': ['hiam'],
            'segmented_exact': ['Hiam'],
            'gloss_exact': ['Q'],
            'exclude_text_contains': ['Bang hang hiam ci', 'Bang hang hiam cih'],
        },
        {
            'name': 'Reject formulaic Bang hang hiam expressions',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'morpheme_ids': ['hiam.Q.sentence_final'],
            'target_forms': ['hiam'],
            'segmented_exact': ['Hiam'],
            'gloss_exact': ['Q'],
            'text_contains': ['Bang hang hiam ci', 'Bang hang hiam cih'],
            'reason_note': 'This is the formulaic reason expression “Bang hang hiam cih leh/ci leh”, not an ordinary question-particle exemplar.',
        },
        {
            'name': 'Reject formulaic Bang hang hiam source-text hits',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'text_search_terms': ['Bang hang hiam ci', 'Bang hang hiam cih'],
            'reason_note': 'These verse-level hits contain the formulaic reason expression “Bang hang hiam cih leh/ci leh”, so they remain audit-only rejected candidates.',
        },
    ],
    'declarative-hi': [
        {
            'name': 'Sentence-final declarative hi',
            'status': 'safe',
            'drafting_quality': 'usable',
            'max_examples': 2,
            'morpheme_ids': ['hi.DECL.sentence_final'],
            'target_forms': ['hi'],
            'segmented_exact': ['hi'],
            'gloss_exact': ['DECL'],
        },
        {
            'name': 'Reject current hi rows with mismatched glossing',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 2,
            'morpheme_ids': ['hi.DECL.sentence_final'],
            'target_forms': ['hi'],
            'reason_note': 'Current linked hi examples are still glossed as DECL.POSS or otherwise fail the sentence-final declarative filter.',
        },
    ],
    'topic-marker-pen': [
        {
            'name': 'Reject current linked pen rows',
            'status': 'rejected',
            'drafting_quality': 'rejected',
            'max_examples': 3,
            'morpheme_ids': ['pen.TOP.particle'],
            'target_forms': ['pen'],
            'reason_note': 'The backend links these rows to pen.TOP, but their segmented/glossed tiers still read TOP.POSS, so they are not safe topic-marker exemplars yet.',
        },
        {
            'name': 'Topic marker pen fallback text search',
            'status': 'fallback only',
            'drafting_quality': 'review_only',
            'max_examples': 2,
            'text_search_terms': [' pen '],
            'reason_note': 'Fallback text-search hits show likely topic-marking contexts, but no clean backend-linked topic-marker example is available yet.',
        },
    ],
}


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


def merged_entry_filters(entry: Dict) -> Dict:
    """Merge built-in example filters with any source-map overrides."""
    merged = dict(DEFAULT_EXAMPLE_FILTERS.get(entry.get('topic_id', ''), {}))
    for key, value in entry.items():
        if key.startswith('example_'):
            merged[key] = value
    return merged


def markdown_link(from_file: Path, target: str, label: str | None = None) -> str:
    """Build a relative markdown link from one file to another."""
    target_path = repo_path(target).resolve()
    href = os.path.relpath(target_path, start=from_file.resolve().parent)
    return f'[{label or target}]({href})'


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


def render_source_of_truth_lines(source_map: Dict, output_path: Path) -> List[str]:
    """Render canonical-layer links and backend/source-map authority notes."""
    meta = source_map.get('meta', {})
    canonical_path = meta.get('canonical_topic_layer', 'docs/grammar/grammar_source_map.json')
    inventory_path = meta.get('source_inventory', 'docs/grammar/GRAMMAR_SOURCE_INVENTORY.md')
    backend_note = meta.get(
        'backend_topic_tables_note',
        'scripts/backend.py migrate creates the grammar_topics and constructions tables but does not populate them for Tedim.',
    )

    return [
        f"- Canonical topic/construction layer: {markdown_link(output_path, canonical_path)}",
        f"- Source inventory: {markdown_link(output_path, inventory_path)}",
        f"- Backend table status: {backend_note}",
    ]


def _normalize_form(value: str | None) -> str:
    """Normalize a form for conservative matching."""
    return re.sub(r'[^0-9a-z]+', '', (value or '').lower())


def _split_morph_tokens(value: str | None) -> List[str]:
    """Split a segmented or glossed string into morpheme-like pieces."""
    return [token for token in re.split(r'[\s\-]+', value or '') if token]


def _normalized_tokens(value: str | None) -> set[str]:
    """Return normalized morpheme-like pieces for matching."""
    return {_normalize_form(token) for token in _split_morph_tokens(value)}


def _normalized_gloss_tokens(value: str | None) -> set[str]:
    """Return lowercase gloss tokens for robust matching."""
    return {token.lower() for token in _split_morph_tokens(value)}


def _normalize_target_forms(values: Iterable[str]) -> set[str]:
    """Normalize a collection of target forms."""
    return {_normalize_form(value) for value in values if value}


def _selection_rules_for_entry(entry: Dict) -> List[Dict[str, Any]]:
    """Build selection rules for a topic entry."""
    if entry.get('example_selection_rules'):
        return entry['example_selection_rules']

    topic_id = entry.get('topic_id', '')
    if topic_id in STRICT_SELECTION_RULES:
        return STRICT_SELECTION_RULES[topic_id]

    filters = merged_entry_filters(entry)
    rules: List[Dict[str, Any]] = []

    linked_rule: Dict[str, Any] = {
        'name': 'Backend-linked example match',
        'status': 'safe',
        'drafting_quality': 'usable',
        'max_examples': 2,
        'morpheme_ids': filters.get('example_morpheme_ids', []),
        'gm_forms': filters.get('example_forms', []),
        'gm_categories': filters.get('example_categories', []),
        'gm_glosses': filters.get('example_glosses', []),
        'target_forms': filters.get('example_forms', []),
        'segmented_contains': filters.get('example_forms', []),
        'gloss_tokens': [value.lower() for value in filters.get('example_glosses', [])],
    }
    if any(linked_rule.get(key) for key in ('morpheme_ids', 'gm_forms', 'gm_categories', 'gm_glosses')):
        rules.append(linked_rule)

    fallback_terms = filters.get('example_search_terms') or []
    if fallback_terms:
        rules.append(
            {
                'name': 'Fallback text search',
                'status': 'fallback only',
                'drafting_quality': 'review_only',
                'max_examples': 2,
                'text_search_terms': fallback_terms,
                'reason_note': 'No fully safe backend-linked example matched, so only text-search candidates are available for review.',
            }
        )

    return rules


def _append_or_group(
    conditions: List[str],
    params: List[Any],
    column_sql: str,
    values: Iterable[str],
    transform=lambda value: value,
) -> None:
    """Append an OR group of scalar comparisons to SQL conditions."""
    prepared = [transform(value) for value in values if value]
    if not prepared:
        return
    placeholders = ', '.join('?' for _ in prepared)
    conditions.append(f'{column_sql} IN ({placeholders})')
    params.extend(prepared)


def _append_like_group(
    conditions: List[str],
    params: List[Any],
    column_sql: str,
    values: Iterable[str],
) -> None:
    """Append an OR group of LIKE comparisons to SQL conditions."""
    prepared = [value.lower() for value in values if value]
    if not prepared:
        return
    like_parts = [f'{column_sql} LIKE ?' for _ in prepared]
    conditions.append(f"({' OR '.join(like_parts)})")
    params.extend([f'%{value}%' for value in prepared])


def _linked_rule_query(rule: Dict[str, Any]) -> tuple[str, List[Any]] | None:
    """Build the broad SQL query used to seed linked-example candidates."""
    conditions: List[str] = []
    params: List[Any] = []

    id_parts: List[str] = []
    morpheme_ids = rule.get('morpheme_ids', [])
    if morpheme_ids:
        placeholders = ', '.join('?' for _ in morpheme_ids)
        id_parts.append(f'e.morpheme_id IN ({placeholders})')
        params.extend(morpheme_ids)

    sense_ids = rule.get('sense_ids', [])
    if sense_ids:
        placeholders = ', '.join('?' for _ in sense_ids)
        id_parts.append(f'e.sense_id IN ({placeholders})')
        params.extend(sense_ids)

    if id_parts:
        conditions.append(f"({' OR '.join(id_parts)})")

    _append_or_group(conditions, params, 'e.source_id', rule.get('source_ids', []))
    _append_or_group(conditions, params, 'e.target_form', rule.get('target_forms', []))
    _append_or_group(conditions, params, 'gm.form', rule.get('gm_forms', []))
    _append_or_group(conditions, params, 'gm.category', rule.get('gm_categories', []))

    gm_glosses = rule.get('gm_glosses', [])
    if gm_glosses:
        placeholders = ', '.join('?' for _ in gm_glosses)
        conditions.append(f'(gm.gloss IN ({placeholders}) OR gm.function IN ({placeholders}))')
        params.extend(gm_glosses)
        params.extend(gm_glosses)

    _append_or_group(conditions, params, 'e.segmented', rule.get('segmented_exact', []))
    _append_like_group(conditions, params, 'LOWER(COALESCE(e.segmented, \'\'))', rule.get('segmented_query_terms', []))
    _append_or_group(conditions, params, 'e.glossed', rule.get('gloss_exact', []))
    _append_like_group(conditions, params, 'LOWER(COALESCE(e.glossed, \'\'))', rule.get('gloss_query_terms', []))
    _append_like_group(conditions, params, 'LOWER(COALESCE(e.tedim_text, \'\'))', rule.get('text_query_terms', []))

    if not conditions:
        return None

    query = f'''
        SELECT DISTINCT
            e.example_id,
            e.source_id,
            e.sense_id,
            e.morpheme_id,
            e.target_form,
            e.tedim_text,
            e.segmented,
            e.glossed,
            e.kjv_text,
            e.quality,
            gm.form AS gm_form,
            gm.gloss AS gm_gloss,
            gm.function AS gm_function,
            gm.category AS gm_category
        FROM examples e
        LEFT JOIN grammatical_morphemes gm ON e.morpheme_id = gm.morpheme_id
        WHERE {' AND '.join(conditions)}
        ORDER BY {EXAMPLE_QUALITY_ORDER_SQL}, LENGTH(COALESCE(e.tedim_text, '')), e.example_id
        LIMIT ?
    '''
    return query, params


def _text_matches_any(text: str | None, snippets: Iterable[str]) -> bool:
    """Return whether the given text contains any snippet, case-insensitively."""
    haystack = (text or '').lower()
    return any(snippet.lower() in haystack for snippet in snippets if snippet)


def _row_matches_rule(row: sqlite3.Row, rule: Dict[str, Any]) -> List[str]:
    """Return matched fields if a linked example row satisfies a rule."""
    matched_fields: List[str] = []
    segmented_tokens = _normalized_tokens(row['segmented'])
    gloss_tokens = _normalized_gloss_tokens(row['glossed'])
    normalized_segmented = _normalize_form(row['segmented'])
    normalized_target = _normalize_form(row['target_form'])

    source_ids = rule.get('source_ids', [])
    if source_ids:
        if row['source_id'] not in source_ids:
            return []
        matched_fields.append('source_id')

    morpheme_ids = rule.get('morpheme_ids', [])
    if morpheme_ids:
        if row['morpheme_id'] not in morpheme_ids:
            return []
        matched_fields.append('morpheme_id')

    sense_ids = rule.get('sense_ids', [])
    if sense_ids:
        if row['sense_id'] not in sense_ids:
            return []
        matched_fields.append('sense_id')

    target_forms = _normalize_target_forms(rule.get('target_forms', []))
    if target_forms:
        if normalized_target not in target_forms:
            return []
        matched_fields.append('target_form')

    segmented_exact = rule.get('segmented_exact', [])
    if segmented_exact:
        if row['segmented'] not in segmented_exact:
            return []
        matched_fields.append('segmentation')

    exclude_segmented_exact = rule.get('exclude_segmented_exact', [])
    if exclude_segmented_exact and row['segmented'] in exclude_segmented_exact:
        return []

    segmented_normalized = _normalize_target_forms(rule.get('segmented_normalized', []))
    if segmented_normalized:
        if normalized_segmented not in segmented_normalized:
            return []
        matched_fields.append('segmentation')

    segmented_contains = _normalize_target_forms(rule.get('segmented_contains', []))
    if segmented_contains:
        if not any(term in segmented_tokens for term in segmented_contains):
            return []
        matched_fields.append('segmentation')

    gloss_exact = rule.get('gloss_exact', [])
    if gloss_exact:
        if row['glossed'] not in gloss_exact:
            return []
        matched_fields.append('gloss')

    gloss_tokens_required = {token.lower() for token in rule.get('gloss_tokens', []) if token}
    if gloss_tokens_required:
        if not any(token in gloss_tokens for token in gloss_tokens_required):
            return []
        matched_fields.append('gloss')

    excluded_segmented = _normalize_target_forms(rule.get('exclude_segmented_contains', []))
    if excluded_segmented and any(term in segmented_tokens for term in excluded_segmented):
        return []

    excluded_gloss_tokens = {token.lower() for token in rule.get('exclude_gloss_tokens', []) if token}
    if excluded_gloss_tokens and any(token in gloss_tokens for token in excluded_gloss_tokens):
        return []

    if rule.get('text_contains'):
        if not _text_matches_any(row['tedim_text'], rule['text_contains']):
            return []
        matched_fields.append('text')

    if rule.get('exclude_text_contains') and _text_matches_any(row['tedim_text'], rule['exclude_text_contains']):
        return []

    return list(dict.fromkeys(matched_fields))


def _default_drafting_quality(rule: Dict[str, Any], row: sqlite3.Row | None) -> str:
    """Compute the default drafting quality for a rule/candidate pair."""
    if rule.get('drafting_quality'):
        return rule['drafting_quality']

    status = rule.get('status', 'safe')
    if status == 'fallback only':
        return 'review_only'
    if status == 'rejected':
        return 'rejected'

    quality = (row['quality'] if row is not None and row['quality'] else '').lower()
    if quality in {'canonical', 'excellent'}:
        return 'exemplar'
    return 'usable'


def _fetch_linked_examples_for_rule(conn: sqlite3.Connection, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch linked backend examples that satisfy one rule."""
    query_data = _linked_rule_query(rule)
    if not query_data:
        return []

    query, params = query_data
    fetch_limit = max(rule.get('max_examples', 2) * 10, 20)
    rows = conn.execute(query, params + [fetch_limit]).fetchall()
    examples: List[Dict[str, Any]] = []

    for row in rows:
        matched_fields = _row_matches_rule(row, rule)
        if not matched_fields:
            continue
        candidate = dict(row)
        candidate['selection_status'] = rule.get('status', 'safe')
        candidate['drafting_quality'] = _default_drafting_quality(rule, row)
        candidate['selection_reason'] = rule['name']
        candidate['selection_note'] = rule.get('reason_note', '')
        candidate['matched_fields'] = matched_fields
        candidate['selection_method'] = 'linked_example'
        examples.append(candidate)

    return examples


def _fallback_source_examples(conn: sqlite3.Connection, rule: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Fetch verse-level review candidates by text search when linked examples are absent."""
    terms = rule.get('text_search_terms', [])
    if not terms:
        return []

    conditions = []
    params: List[str] = []
    for term in terms:
        conditions.append('(LOWER(text) LIKE ? OR LOWER(text_normalized) LIKE ?)')
        params.extend([f'%{term.lower()}%', f'%{term.lower()}%'])

    query = f'''
        SELECT source_id, text, kjv_text
        FROM sources
        WHERE {' OR '.join(conditions)}
        ORDER BY source_id
        LIMIT ?
    '''
    fetch_limit = max(rule.get('max_examples', 2) * 6, 12)
    rows = conn.execute(query, params + [fetch_limit]).fetchall()

    examples: List[Dict[str, Any]] = []
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
                'selection_status': rule.get('status', 'fallback only'),
                'drafting_quality': _default_drafting_quality(rule, None),
                'selection_reason': rule['name'],
                'selection_note': rule.get('reason_note', ''),
                'matched_fields': ['fallback text search'],
                'selection_method': 'fallback_text_search',
            }
        )

    return examples


def _is_draft_ready(candidate: Dict[str, Any]) -> bool:
    """Return whether a candidate can be used in grammar-drafting output."""
    return candidate['selection_status'] == 'safe' and candidate['drafting_quality'] in DRAFT_READY_QUALITIES


def _annotate_grammar_usage(candidates: List[Dict[str, Any]], limit: int) -> List[Dict[str, Any]]:
    """Mark which candidates are actually used in grammar-drafting outputs."""
    used = 0
    for candidate in candidates:
        candidate['used_in_grammar'] = False
        if used >= limit:
            continue
        if _is_draft_ready(candidate):
            candidate['used_in_grammar'] = True
            used += 1
    return candidates


def select_examples_for_entry(
    conn: sqlite3.Connection,
    entry: Dict,
    limit: int = 3,
    include_non_safe: bool = False,
) -> List[Dict[str, Any]]:
    """Select example candidates for one source-map entry."""
    candidates: List[Dict[str, Any]] = []
    seen_source_ids: set[str] = set()

    for rule in _selection_rules_for_entry(entry):
        per_rule_count = 0
        rule_candidates = (
            _fallback_source_examples(conn, rule)
            if rule.get('text_search_terms')
            else _fetch_linked_examples_for_rule(conn, rule)
        )
        for candidate in rule_candidates:
            if candidate['source_id'] in seen_source_ids:
                continue
            seen_source_ids.add(candidate['source_id'])
            candidates.append(candidate)
            per_rule_count += 1
            if per_rule_count >= rule.get('max_examples', limit):
                break

    candidates = _annotate_grammar_usage(candidates, limit)
    if include_non_safe:
        return candidates
    return [candidate for candidate in candidates if candidate['used_in_grammar']]


def audit_examples_for_entry(conn: sqlite3.Connection, entry: Dict, limit: int = 3) -> List[Dict[str, Any]]:
    """Return all audit-visible candidates for one source-map entry."""
    return select_examples_for_entry(conn, entry, limit=limit, include_non_safe=True)


def fetch_examples_for_entry(conn: sqlite3.Connection, entry: Dict, limit: int = 3) -> List[Dict]:
    """Fetch only draft-ready examples for a source-map entry."""
    return select_examples_for_entry(conn, entry, limit=limit, include_non_safe=False)


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
