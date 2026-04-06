#!/usr/bin/env python3
"""
Validate analyzer data integrity.

Checks for:
1. Duplicate keys in COMPOUND_WORDS
2. Missing imports
3. Python syntax errors

Usage:
    python scripts/validate_analyzer.py
"""

import re
import sys

def check_duplicates_in_file(filepath, dict_name='COMPOUND_WORDS'):
    """Check for duplicate keys in a Python dictionary file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Pattern for dict entries
    key_pattern = re.compile(r"^\s+'([a-z][a-z\-\']*)':\s*[\(\'\"\[]")
    keys_found = {}
    
    for i, line in enumerate(lines, 1):
        match = key_pattern.match(line)
        if match:
            key = match.group(1)
            if key not in keys_found:
                keys_found[key] = []
            keys_found[key].append(i)
    
    duplicates = {k: v for k, v in keys_found.items() if len(v) > 1}
    return duplicates


def validate_import():
    """Verify the analyzer can be imported."""
    try:
        sys.path.insert(0, 'scripts')
        import analyze_morphemes
        return True, None
    except Exception as e:
        return False, str(e)


def validate_compounds():
    """Check COMPOUND_WORDS for duplicates."""
    dups = check_duplicates_in_file('scripts/morphology/compounds.py')
    return dups


def main():
    errors = 0
    
    print("Validating Tedim Chin Morphological Analyzer...")
    print("=" * 60)
    
    # Check import
    print("\n1. Checking import...")
    ok, err = validate_import()
    if ok:
        print("   ✓ analyze_morphemes imports successfully")
    else:
        print(f"   ✗ Import failed: {err}")
        errors += 1
    
    # Check compounds
    print("\n2. Checking COMPOUND_WORDS for duplicates...")
    dups = validate_compounds()
    if not dups:
        print("   ✓ No duplicate keys found")
    else:
        print(f"   ✗ Found {len(dups)} duplicate keys:")
        for key, lines in list(dups.items())[:10]:
            print(f"      '{key}': lines {lines}")
        if len(dups) > 10:
            print(f"      ... and {len(dups) - 10} more")
        errors += 1
    
    # Summary
    print("\n" + "=" * 60)
    if errors == 0:
        print("✓ All validation checks passed")
        return 0
    else:
        print(f"✗ {errors} validation error(s) found")
        return 1


if __name__ == '__main__':
    sys.exit(main())
