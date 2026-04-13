#!/usr/bin/env python3
"""
Review Queue Workflow Tool

Operationalize the review queue for coordinators to work through flagged items.
Prioritizes high-frequency ambiguous forms where curation pays off fastest.

Usage:
    python scripts/review_queue.py list              # List open items
    python scripts/review_queue.py list --high       # High-priority only
    python scripts/review_queue.py show <id>         # Show item details
    python scripts/review_queue.py resolve <id> <resolution>
    python scripts/review_queue.py stats             # Review queue statistics
    python scripts/review_queue.py export            # Export to TSV for batch review
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import Backend


def cmd_list(db: Backend, args):
    """List open review items."""
    priority = args.priority if hasattr(args, 'priority') else None
    entity_type = args.type if hasattr(args, 'type') else None
    limit = args.limit if hasattr(args, 'limit') else 50
    
    items = db.get_review_items(status='open', priority=priority, 
                                entity_type=entity_type, limit=limit)
    
    if not items:
        print("No open review items found.")
        return
    
    print(f"Open review items ({len(items)} shown):\n")
    print(f"{'ID':>5} {'Type':<10} {'Priority':<8} {'Entity ID':<20} {'Reason'}")
    print("-" * 80)
    
    for item in items:
        reason_short = item.reason[:35] + "..." if len(item.reason) > 35 else item.reason
        print(f"{item.review_id:>5} {item.entity_type:<10} {item.priority:<8} {item.entity_id:<20} {reason_short}")


def cmd_show(db: Backend, args):
    """Show details for a review item."""
    items = db.get_review_items(status='open', limit=1000)
    item = next((i for i in items if i.review_id == args.review_id), None)
    
    if not item:
        print(f"Review item {args.review_id} not found or already resolved.")
        return
    
    print(f"Review Item #{item.review_id}")
    print("=" * 40)
    print(f"Type:     {item.entity_type}")
    print(f"Entity:   {item.entity_id}")
    print(f"Priority: {item.priority}")
    print(f"Status:   {item.status}")
    print(f"Reason:   {item.reason}")
    print(f"Created:  {item.created_at}")
    print()
    
    # Show related data based on entity type
    if item.entity_type == 'wordform':
        wf = db.get_wordform(item.entity_id)
        if wf:
            print("Wordform details:")
            print(f"  Surface:      {wf['surface']}")
            print(f"  Normalized:   {wf['normalized']}")
            print(f"  Lemma:        {wf['lemma_id']}")
            print(f"  POS:          {wf['pos']}")
            print(f"  Segmentation: {wf['segmentation']}")
            print(f"  Gloss:        {wf['gloss']}")
            print(f"  Frequency:    {wf['frequency']:,}")
    
    elif item.entity_type == 'lemma':
        lemma = db.get_lemma(item.entity_id)
        if lemma:
            print("Lemma details:")
            print(f"  Citation:  {lemma.citation_form}")
            print(f"  POS:       {lemma.pos}")
            print(f"  Gloss:     {lemma.primary_gloss}")
            print(f"  Type:      {lemma.entry_type}")
            print(f"  Frequency: {lemma.token_count:,}")
            
            senses = db.get_senses(item.entity_id)
            if senses:
                print(f"\n  Senses ({len(senses)}):")
                for s in senses:
                    print(f"    {s.sense_num}. {s.gloss} (freq: {s.frequency:,})")


def cmd_resolve(db: Backend, args):
    """Resolve a review item."""
    db.resolve_review_item(args.review_id, args.resolution)
    print(f"Resolved review item #{args.review_id}: {args.resolution}")


def cmd_stats(db: Backend, args):
    """Show review queue statistics."""
    stats = db.get_stats()
    
    print("Review Queue Statistics")
    print("=" * 40)
    print(f"Open items:     {stats.get('review_open', 0):,}")
    print(f"Resolved items: {stats.get('review_resolved', 0):,}")
    print()
    
    # Breakdown by type and priority
    with db._connection() as conn:
        print("By entity type:")
        rows = conn.execute('''
            SELECT entity_type, COUNT(*) as cnt 
            FROM review_queue WHERE status = 'open'
            GROUP BY entity_type ORDER BY cnt DESC
        ''').fetchall()
        for row in rows:
            print(f"  {row['entity_type']}: {row['cnt']:,}")
        
        print("\nBy priority:")
        rows = conn.execute('''
            SELECT priority, COUNT(*) as cnt 
            FROM review_queue WHERE status = 'open'
            GROUP BY priority ORDER BY cnt DESC
        ''').fetchall()
        for row in rows:
            print(f"  {row['priority']}: {row['cnt']:,}")
        
        print("\nTop reasons:")
        rows = conn.execute('''
            SELECT reason, COUNT(*) as cnt 
            FROM review_queue WHERE status = 'open'
            GROUP BY reason ORDER BY cnt DESC LIMIT 10
        ''').fetchall()
        for row in rows:
            reason_short = row['reason'][:50] + "..." if len(row['reason']) > 50 else row['reason']
            print(f"  {row['cnt']:>4}: {reason_short}")


def cmd_export(db: Backend, args):
    """Export review queue to TSV for batch review."""
    output = args.output if hasattr(args, 'output') else 'analysis/review/review_queue_export.tsv'
    
    items = db.get_review_items(status='open', limit=5000)
    
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write("review_id\tentity_type\tentity_id\tpriority\treason\tcreated_at\n")
        for item in items:
            f.write(f"{item.review_id}\t{item.entity_type}\t{item.entity_id}\t"
                    f"{item.priority}\t{item.reason}\t{item.created_at}\n")
    
    print(f"Exported {len(items)} review items to {output}")


def main():
    parser = argparse.ArgumentParser(description='Review queue workflow tool')
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List open review items')
    list_parser.add_argument('--priority', '-p', choices=['high', 'medium', 'low'],
                             help='Filter by priority')
    list_parser.add_argument('--type', '-t', choices=['lemma', 'sense', 'wordform', 'example'],
                             help='Filter by entity type')
    list_parser.add_argument('--limit', '-n', type=int, default=50,
                             help='Maximum items to show')
    
    # show command
    show_parser = subparsers.add_parser('show', help='Show review item details')
    show_parser.add_argument('review_id', type=int, help='Review item ID')
    
    # resolve command
    resolve_parser = subparsers.add_parser('resolve', help='Resolve a review item')
    resolve_parser.add_argument('review_id', type=int, help='Review item ID')
    resolve_parser.add_argument('resolution', help='Resolution description')
    
    # stats command
    subparsers.add_parser('stats', help='Show review queue statistics')
    
    # export command
    export_parser = subparsers.add_parser('export', help='Export to TSV')
    export_parser.add_argument('--output', '-o', 
                               default='analysis/review/review_queue_export.tsv',
                               help='Output file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    db = Backend(args.db)
    
    if args.command == 'list':
        cmd_list(db, args)
    elif args.command == 'show':
        cmd_show(db, args)
    elif args.command == 'resolve':
        cmd_resolve(db, args)
    elif args.command == 'stats':
        cmd_stats(db, args)
    elif args.command == 'export':
        cmd_export(db, args)


if __name__ == '__main__':
    main()
