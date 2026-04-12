#!/usr/bin/env python3
"""
Generate TAM Markers Report from Backend

Backend-based grammar report generator for Tedim Chin TAM (tense-aspect-mood) markers.
This demonstrates reading from the shared SQLite backend instead of scattered sources.

Usage:
    python scripts/generate_tam_report_backend.py
    python scripts/generate_tam_report_backend.py --db data/ctd_backend.db
    python scripts/generate_tam_report_backend.py --output output/tam_report.md
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import Backend, GrammaticalMorpheme, Example, Source
from report_utils import format_reference, BOOK_NAMES

# =============================================================================
# TAM Categories
# =============================================================================

TAM_CATEGORIES = {
    'tam_suffix': {
        'title': 'Tense-Aspect-Mood Suffixes',
        'description': 'Core TAM markers that attach to verb stems.',
        'subcategories': {
            'aspect': ['PFV', 'COMPL', 'CONT', 'ITER', 'HAB'],
            'mood': ['IRR', 'PROSP', 'ABIL', 'NEG'],
            'tense': ['PST', 'FUT'],
        }
    },
    'aspect_suffix': {
        'title': 'Aspect Suffixes', 
        'description': 'Suffixes encoding aspectual distinctions.',
    },
    'modal_suffix': {
        'title': 'Modal Suffixes',
        'description': 'Suffixes encoding modality (ability, possibility, obligation).',
    },
    'sentence_final': {
        'title': 'Sentence-Final Particles',
        'description': 'Particles that mark sentence mood and illocutionary force.',
    },
}

# Map glosses to human-readable descriptions
GLOSS_DESCRIPTIONS = {
    'PFV': 'Perfective - completed action',
    'COMPL': 'Completive - action done to completion',
    'CONT': 'Continuous - ongoing action',
    'ITER': 'Iterative - repeated action',
    'HAB': 'Habitual - regular occurrence',
    'IRR': 'Irrealis - non-actual event',
    'PROSP': 'Prospective - about to happen',
    'ABIL': 'Abilitative - ability/possibility',
    'NEG': 'Negative',
    'PST': 'Past tense',
    'FUT': 'Future tense',
    'DECL': 'Declarative - statement',
    'Q': 'Question marker',
    'IMP': 'Imperative - command',
    'HORT': 'Hortative - suggestion',
    'EMPH': 'Emphatic',
    'EXP': 'Experiential - have done before',
}


# =============================================================================
# Report Generation
# =============================================================================

def generate_tam_report(db: Backend, include_examples: bool = True) -> List[str]:
    """Generate TAM markers report from backend data."""
    lines = []
    
    # Header
    lines.append("# Tedim Chin TAM Markers")
    lines.append("")
    lines.append("This report documents the tense-aspect-mood system of Tedim Chin,")
    lines.append("generated from the corpus backend.")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Overview table
    lines.append("## Overview")
    lines.append("")
    lines.append("| Category | Count | Most Frequent |")
    lines.append("|----------|-------|---------------|")
    
    # Get morphemes by category
    categories_found = {}
    all_morphemes = db.get_grammatical_morphemes()
    
    for morph in all_morphemes:
        cat = morph.category
        if cat not in categories_found:
            categories_found[cat] = []
        categories_found[cat].append(morph)
    
    # TAM-related categories
    tam_cats = ['tam_suffix', 'aspect_suffix', 'modal_suffix', 'sentence_final']
    
    for cat in tam_cats:
        if cat in categories_found:
            morphs = categories_found[cat]
            morphs.sort(key=lambda m: -m.frequency)
            top = morphs[0] if morphs else None
            top_str = f"{top.form} ({top.gloss})" if top else "—"
            lines.append(f"| {cat.replace('_', ' ').title()} | {len(morphs)} | {top_str} |")
    
    lines.append("")
    
    # Detailed sections
    for cat in tam_cats:
        if cat not in categories_found:
            continue
            
        morphs = categories_found[cat]
        if not morphs:
            continue
        
        cat_info = TAM_CATEGORIES.get(cat, {})
        title = cat_info.get('title', cat.replace('_', ' ').title())
        desc = cat_info.get('description', '')
        
        lines.append("---")
        lines.append("")
        lines.append(f"## {title}")
        lines.append("")
        if desc:
            lines.append(desc)
            lines.append("")
        
        # Sort by frequency
        morphs.sort(key=lambda m: -m.frequency)
        
        # Table of markers
        lines.append("| Form | Gloss | Function | Frequency | Status |")
        lines.append("|------|-------|----------|-----------|--------|")
        
        for m in morphs[:20]:  # Top 20
            func_desc = GLOSS_DESCRIPTIONS.get(m.gloss, m.function or m.gloss)
            status = '⚠️' if m.is_polysemous else '✓'
            lines.append(f"| **{m.form}** | {m.gloss} | {func_desc[:40]} | {m.frequency:,} | {status} |")
        
        lines.append("")
        
        # Examples for top markers
        if include_examples:
            lines.append("### Examples")
            lines.append("")
            
            for m in morphs[:5]:  # Examples for top 5
                examples = db.get_examples_for_morpheme(m.morpheme_id, limit=2)
                
                if not examples:
                    # Try to find examples via sense
                    # This is a fallback - ideally examples link to morphemes directly
                    continue
                
                lines.append(f"#### {m.form} ({m.gloss})")
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
                        lines.append(f"> KJV: *{ex.kjv_text}*")
                    lines.append("")
    
    # Summary statistics
    lines.append("---")
    lines.append("")
    lines.append("## Statistics")
    lines.append("")
    
    stats = db.get_stats()
    lines.append(f"- Total grammatical morphemes in database: {stats.get('grammatical_morphemes', 0):,}")
    lines.append(f"- Total examples in database: {stats.get('examples', 0):,}")
    lines.append(f"- Review items pending: {stats.get('review_open', 0):,}")
    lines.append("")
    
    # Data source
    lines.append("---")
    lines.append("")
    lines.append("*Generated from `ctd_backend.db` using `generate_tam_report_backend.py`*")
    
    return lines


def generate_verb_slot_report(db: Backend) -> List[str]:
    """Generate verb slot template report from backend."""
    lines = []
    
    lines.append("# Tedim Chin Verb Slots")
    lines.append("")
    lines.append("The Tedim Chin verb has the following slot structure:")
    lines.append("")
    lines.append("```")
    lines.append("(NEG) (OBJ) SUBJ-STEM-(DERIV)-(ASPECT)-(DIR)-(TAM)")
    lines.append("```")
    lines.append("")
    
    # Get morphemes by position
    prefixes = db.get_grammatical_morphemes(position='prefix')
    suffixes = db.get_grammatical_morphemes(position='suffix')
    
    # Slot tables
    slots = [
        ('Prefix Slot', 'prefix', [
            ('pronominal_prefix', 'Subject agreement'),
            ('object_prefix', 'Object agreement'),
            ('negation', 'Negation'),
        ]),
        ('Suffix Slot 1: Derivational', 'suffix', [
            ('derivational', 'Derivational'),
            ('causative', 'Causative'),
            ('applicative', 'Applicative'),
        ]),
        ('Suffix Slot 2: Aspect', 'suffix', [
            ('aspect_suffix', 'Aspect'),
        ]),
        ('Suffix Slot 3: Directional', 'suffix', [
            ('directional', 'Directional'),
        ]),
        ('Suffix Slot 4: TAM', 'suffix', [
            ('tam_suffix', 'TAM'),
            ('modal_suffix', 'Modal'),
        ]),
    ]
    
    for slot_name, position, categories in slots:
        lines.append(f"## {slot_name}")
        lines.append("")
        lines.append("| Form | Gloss | Category | Freq |")
        lines.append("|------|-------|----------|------|")
        
        for cat, cat_name in categories:
            morphs = db.get_grammatical_morphemes(category=cat)
            morphs.sort(key=lambda m: -m.frequency)
            for m in morphs[:5]:
                lines.append(f"| {m.form} | {m.gloss} | {cat_name} | {m.frequency:,} |")
        
        lines.append("")
    
    return lines


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Generate TAM report from backend")
    parser.add_argument("--db", default="data/ctd_backend.db",
                        help="Backend database path")
    parser.add_argument("--output", "-o", default=None,
                        help="Output file (default: stdout)")
    parser.add_argument("--no-examples", action="store_true",
                        help="Exclude examples from report")
    parser.add_argument("--slots", action="store_true",
                        help="Generate verb slots report instead")
    
    args = parser.parse_args()
    
    db_path = Path(args.db)
    if not db_path.exists():
        print(f"Error: Database not found: {db_path}", file=sys.stderr)
        print("Run: python scripts/backend.py migrate", file=sys.stderr)
        sys.exit(1)
    
    db = Backend(str(db_path))
    
    if args.slots:
        lines = generate_verb_slot_report(db)
    else:
        lines = generate_tam_report(db, include_examples=not args.no_examples)
    
    output = "\n".join(lines)
    
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
