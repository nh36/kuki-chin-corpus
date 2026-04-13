#!/usr/bin/env python3
"""
Link examples to senses based on target_form and gloss matching.

This script populates the sense_id field in examples table by:
1. Direct match: target_form matches lemma_id for single-sense lemmas
2. Gloss match: For multi-sense lemmas, match example gloss to sense gloss
3. Heuristic: Apply rules for common patterns (e.g., DECL for hi)
"""

import sqlite3
import re
from pathlib import Path

def normalize_gloss(gloss: str) -> str:
    """Normalize gloss for matching."""
    if not gloss:
        return ""
    # Remove quotes
    gloss = gloss.strip('"\'')
    # Take first part before hyphen for compound glosses
    if '-' in gloss:
        parts = gloss.split('-')
        # Return first substantial part
        for p in parts:
            if p and len(p) > 1:
                return p.upper()
    return gloss.upper()

def link_examples_to_senses(db_path: str, dry_run: bool = False):
    """Link unlinked examples to their senses."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    stats = {
        'direct_single': 0,
        'gloss_match': 0,
        'heuristic': 0,
        'skipped': 0,
        'total_unlinked': 0
    }
    
    # Get all senses indexed by lemma
    senses_by_lemma = {}
    for row in conn.execute('SELECT sense_id, lemma_id, gloss FROM senses'):
        lemma = row['lemma_id']
        if lemma not in senses_by_lemma:
            senses_by_lemma[lemma] = []
        senses_by_lemma[lemma].append({
            'sense_id': row['sense_id'],
            'gloss': row['gloss']
        })
    
    # Get unlinked examples
    unlinked = list(conn.execute('''
        SELECT example_id, target_form, glossed 
        FROM examples 
        WHERE sense_id IS NULL OR sense_id = ""
    '''))
    
    stats['total_unlinked'] = len(unlinked)
    
    updates = []
    
    for row in unlinked:
        example_id = row['example_id']
        target = row['target_form'].lower() if row['target_form'] else None
        glossed = row['glossed']
        
        if not target:
            stats['skipped'] += 1
            continue
            
        # Check if target matches a lemma
        if target not in senses_by_lemma:
            # Try without quotes/punctuation
            target_clean = re.sub(r'^["\']|["\']$', '', target)
            if target_clean not in senses_by_lemma:
                stats['skipped'] += 1
                continue
            target = target_clean
        
        senses = senses_by_lemma[target]
        
        # Case 1: Single sense - direct link
        if len(senses) == 1:
            updates.append((senses[0]['sense_id'], example_id))
            stats['direct_single'] += 1
            continue
        
        # Case 2: Multi-sense - try gloss matching
        norm_glossed = normalize_gloss(glossed)
        matched = None
        
        for sense in senses:
            norm_sense = normalize_gloss(sense['gloss'])
            if norm_sense == norm_glossed:
                matched = sense['sense_id']
                break
            # Partial match
            if norm_sense in norm_glossed or norm_glossed in norm_sense:
                matched = sense['sense_id']
                break
        
        if matched:
            updates.append((matched, example_id))
            stats['gloss_match'] += 1
            continue
        
        # Case 3: Heuristics for common patterns
        # For 'hi', default to DECL (most common)
        if target == 'hi':
            for sense in senses:
                if sense['gloss'] == 'DECL':
                    updates.append((sense['sense_id'], example_id))
                    stats['heuristic'] += 1
                    matched = True
                    break
        
        if not matched:
            # Default to first sense for multi-sense
            updates.append((senses[0]['sense_id'], example_id))
            stats['heuristic'] += 1
    
    # Apply updates
    if not dry_run and updates:
        conn.executemany(
            'UPDATE examples SET sense_id = ? WHERE example_id = ?',
            updates
        )
        conn.commit()
    
    conn.close()
    return stats, len(updates)

def generate_corpus_examples(db_path: str, limit_per_sense: int = 5, max_senses: int = 500, dry_run: bool = False):
    """Generate examples from corpus for senses lacking examples."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    
    # Find senses without examples, prioritized by lemma frequency
    senses_needing = list(conn.execute('''
        SELECT s.sense_id, s.lemma_id, s.gloss, l.token_count
        FROM senses s
        JOIN lemmas l ON s.lemma_id = l.lemma_id
        LEFT JOIN examples e ON s.sense_id = e.sense_id
        WHERE e.example_id IS NULL
        ORDER BY l.token_count DESC
    '''))
    
    print(f"Found {len(senses_needing)} senses without examples")
    
    new_examples = []
    
    for sense in senses_needing[:max_senses]:
        lemma_id = sense['lemma_id']
        sense_id = sense['sense_id']
        
        # Find corpus occurrences via tokens/wordforms
        verses = list(conn.execute('''
            SELECT DISTINCT s.source_id, s.text, s.kjv_text, t.surface
            FROM sources s
            JOIN tokens t ON s.source_id = t.source_id
            JOIN wordforms w ON t.wordform_id = w.wordform_id
            WHERE w.lemma_id = ?
            ORDER BY LENGTH(s.text)
            LIMIT ?
        ''', (lemma_id, limit_per_sense)))
        
        for v in verses:
            new_examples.append({
                'source_id': v['source_id'],
                'sense_id': sense_id,
                'target_form': v['surface'],
                'tedim_text': v['text'],
                'kjv_text': v['kjv_text'],
                'quality': 'auto',
                'example_type': 'corpus'
            })
    
    # Insert new examples
    if not dry_run and new_examples:
        conn.executemany('''
            INSERT INTO examples (source_id, sense_id, target_form, tedim_text, 
                                  kjv_text, quality, example_type)
            VALUES (:source_id, :sense_id, :target_form, :tedim_text, 
                    :kjv_text, :quality, :example_type)
        ''', new_examples)
        conn.commit()
    
    conn.close()
    return len(new_examples)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Link examples to senses')
    parser.add_argument('--db', default='data/ctd_backend.db', help='Database path')
    parser.add_argument('--dry-run', action='store_true', help='Dry run without updates')
    parser.add_argument('--generate', action='store_true', help='Also generate corpus examples')
    parser.add_argument('--max-senses', type=int, default=500, help='Max senses for corpus generation')
    args = parser.parse_args()
    
    print("=== Linking existing examples to senses ===")
    stats, updated = link_examples_to_senses(args.db, args.dry_run)
    
    print(f"\nResults:")
    print(f"  Total unlinked: {stats['total_unlinked']}")
    print(f"  Direct (single-sense): {stats['direct_single']}")
    print(f"  Gloss match: {stats['gloss_match']}")
    print(f"  Heuristic: {stats['heuristic']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Updated: {updated}")
    
    if args.generate:
        print("\n=== Generating corpus examples for senses without ===")
        generated = generate_corpus_examples(args.db, max_senses=args.max_senses, dry_run=args.dry_run)
        print(f"  Generated: {generated} new examples")
    
    if args.dry_run:
        print("\n[DRY RUN - no changes made]")
