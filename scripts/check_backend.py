#!/usr/bin/env python3
"""
Verify backend integrity - check that counts are within expected ranges.

Usage:
    python scripts/check_backend.py [--db data/ctd_backend.db]
"""

import argparse
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from backend import Backend


# Expected minimum counts (sanity check)
EXPECTED = {
    'sources': 30000,
    'tokens': 830000,
    'lemmas': 7000,
    'senses': 9000,
    'grammatical_morphemes': 400,
    'examples': 20000,
}


def main():
    parser = argparse.ArgumentParser(description='Check backend integrity')
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    args = parser.parse_args()
    
    if not Path(args.db).exists():
        print(f"ERROR: Database not found: {args.db}")
        print("Run 'make backend' to generate it.")
        sys.exit(1)
    
    db = Backend(args.db)
    stats = db.get_stats()
    
    print("Backend statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value:,}")
    
    # Check minimums
    errors = []
    for key, minimum in EXPECTED.items():
        if key in stats and stats[key] < minimum:
            errors.append(f"{key} too low: {stats[key]:,} < {minimum:,}")
    
    if errors:
        print("\nERRORS:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    print("\n✓ All counts within expected range")
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
