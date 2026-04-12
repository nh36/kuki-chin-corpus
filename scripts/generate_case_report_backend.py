#!/usr/bin/env python3
"""
Generate Case Marking Report from Backend

Backend-based grammar report generator for Tedim Chin case markers and argument marking.
This demonstrates the backend architecture for syntactic grammar domains.

Usage:
    python scripts/generate_case_report_backend.py
    python scripts/generate_case_report_backend.py --db data/ctd_backend.db
    python scripts/generate_case_report_backend.py --output output/case_marking_report.md
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import Backend, GrammaticalMorpheme, Example
from report_utils import format_reference, BOOK_NAMES


# =============================================================================
# Case Marker Descriptions
# =============================================================================

CASE_DESCRIPTIONS = {
    'ERG': {
        'name': 'Ergative',
        'description': 'Marks the agent (A) of transitive verbs. Tedim Chin exhibits split ergativity with ergative-absolutive alignment in certain contexts.',
        'syntax': 'Attaches to NPs functioning as transitive agents.',
    },
    'LOC': {
        'name': 'Locative',
        'description': 'Marks location in space. Used for static location ("at, in") and sometimes goals of motion.',
        'syntax': 'Attaches to NPs denoting places or spatial reference points.',
    },
    'COM': {
        'name': 'Comitative',
        'description': 'Marks accompaniment ("with, together with"). Can extend to instrumental uses.',
        'syntax': 'Attaches to NPs denoting companions or instruments.',
    },
    'ABL': {
        'name': 'Ablative',
        'description': 'Marks source or origin ("from"). Used for spatial, temporal, and abstract origins.',
        'syntax': 'Attaches to NPs denoting sources or starting points.',
    },
    'CVB': {
        'name': 'Converb',
        'description': 'Marks adverbial subordination. The verb plus this marker functions as a non-finite clause modifying the main predicate.',
        'syntax': 'Attaches to verbs, creating adverbial clauses.',
    },
    'QUOT': {
        'name': 'Quotative',
        'description': 'Marks reported speech or thought. Introduces direct or indirect quotations.',
        'syntax': 'Follows quoted material, introducing the quote frame.',
    },
    'INST': {
        'name': 'Instrumental',
        'description': 'Marks instruments or means ("by means of, using"). Derived from comitative.',
        'syntax': 'Attaches to NPs denoting instruments.',
    },
    'IN': {
        'name': 'Inessive',
        'description': 'Marks containment or interior location ("inside, within").',
        'syntax': 'Attaches to NPs denoting containers or bounded regions.',
    },
}


# =============================================================================
# Report Generation
# =============================================================================

def generate_case_report(db: Backend, include_examples: bool = True) -> List[str]:
    """Generate case marking report from backend data."""
    lines = []
    
    # Header
    lines.append("# Tedim Chin Case Marking")
    lines.append("")
    lines.append("This report documents the case marking system of Tedim Chin,")
    lines.append("generated from the corpus backend. Case markers in Tedim Chin")
    lines.append("are postpositions or enclitics that attach to noun phrases.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Get case markers from backend
    case_markers = db.get_grammatical_morphemes(category='case_marker')
    case_markers.sort(key=lambda m: -m.frequency)
    
    # Filter out noise (very low frequency items that may be errors)
    primary_markers = [m for m in case_markers if m.frequency >= 100]
    secondary_markers = [m for m in case_markers if 10 <= m.frequency < 100]
    
    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"The corpus contains **{len(case_markers)}** distinct case marking forms,")
    lines.append(f"with **{len(primary_markers)}** high-frequency markers (≥100 occurrences).")
    lines.append("")
    
    # Summary table
    lines.append("### Primary Case Markers")
    lines.append("")
    lines.append("| Form | Gloss | Function | Frequency |")
    lines.append("|------|-------|----------|-----------|")
    
    for m in primary_markers:
        desc = CASE_DESCRIPTIONS.get(m.gloss, {})
        func = desc.get('name', m.gloss)
        lines.append(f"| **{m.form}** | {m.gloss} | {func} | {m.frequency:,} |")
    
    lines.append("")
    
    # Ergative-Absolutive alignment section
    lines.append("---")
    lines.append("")
    lines.append("## Ergative-Absolutive Alignment")
    lines.append("")
    lines.append("Tedim Chin shows ergative marking on transitive agents. The ergative")
    lines.append("marker **-in** is the most frequent case marker in the corpus.")
    lines.append("")
    
    erg_marker = next((m for m in case_markers if m.gloss == 'ERG'), None)
    if erg_marker and include_examples:
        lines.append("### Ergative Examples")
        lines.append("")
        examples = db.get_examples_for_morpheme(erg_marker.morpheme_id, limit=5)
        for ex in examples:
            ref = format_reference(ex.source_id)
            lines.append(f"**{ref}**")
            lines.append(f"> {ex.tedim_text}")
            if ex.segmented:
                lines.append(f"> *{ex.segmented}*")
            if ex.glossed:
                lines.append(f"> {ex.glossed}")
            if ex.kjv_text:
                lines.append(f"> '{ex.kjv_text}'")
            lines.append("")
    
    # Detailed sections for each case
    for m in primary_markers:
        if m.gloss not in CASE_DESCRIPTIONS:
            continue
            
        desc = CASE_DESCRIPTIONS[m.gloss]
        
        lines.append("---")
        lines.append("")
        lines.append(f"## {desc['name']} ({m.gloss})")
        lines.append("")
        lines.append(f"**Form:** *-{m.form}*")
        lines.append("")
        lines.append(desc['description'])
        lines.append("")
        lines.append(f"**Syntax:** {desc['syntax']}")
        lines.append("")
        lines.append(f"**Corpus frequency:** {m.frequency:,} occurrences")
        lines.append("")
        
        if include_examples:
            examples = db.get_examples_for_morpheme(m.morpheme_id, limit=3)
            if examples:
                lines.append("### Examples")
                lines.append("")
                for ex in examples:
                    ref = format_reference(ex.source_id)
                    lines.append(f"**{ref}**")
                    lines.append(f"> {ex.tedim_text}")
                    if ex.segmented:
                        lines.append(f"> *{ex.segmented}*")
                    if ex.glossed:
                        lines.append(f"> {ex.glossed}")
                    if ex.kjv_text:
                        lines.append(f"> '{ex.kjv_text}'")
                    lines.append("")
    
    # Polysemy section
    lines.append("---")
    lines.append("")
    lines.append("## Polysemy and Form Overlap")
    lines.append("")
    lines.append("The form **-in** is highly polysemous, serving multiple grammatical")
    lines.append("functions beyond case marking:")
    lines.append("")
    
    # Get all 'in' morphemes
    in_morphemes = db.get_morpheme_by_form('in')
    in_morphemes.sort(key=lambda m: -m.frequency)
    
    lines.append("| Function | Category | Frequency |")
    lines.append("|----------|----------|-----------|")
    for m in in_morphemes[:8]:
        lines.append(f"| {m.gloss} | {m.category} | {m.frequency:,} |")
    
    lines.append("")
    lines.append("Disambiguation depends on syntactic context: -in following an NP is typically")
    lines.append("ergative, while -in following a verb is typically a converb marker.")
    lines.append("")
    
    # Secondary markers
    if secondary_markers:
        lines.append("---")
        lines.append("")
        lines.append("## Secondary and Low-Frequency Forms")
        lines.append("")
        lines.append("| Form | Gloss | Category | Frequency |")
        lines.append("|------|-------|----------|-----------|")
        for m in secondary_markers:
            lines.append(f"| {m.form} | {m.gloss} | {m.category} | {m.frequency:,} |")
        lines.append("")
    
    # Footer
    lines.append("---")
    lines.append("")
    lines.append("*Report generated from backend database.*")
    
    return lines


def main():
    parser = argparse.ArgumentParser(description='Generate case marking report')
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--output', default='output/case_marking_report.md',
                        help='Output file path')
    parser.add_argument('--no-examples', action='store_true',
                        help='Omit example sentences')
    args = parser.parse_args()
    
    # Ensure output directory exists
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # Generate report
    db = Backend(args.db)
    lines = generate_case_report(db, include_examples=not args.no_examples)
    
    # Write output
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Case marking report written to {args.output}")
    print(f"  {len(lines)} lines")


if __name__ == '__main__':
    main()
