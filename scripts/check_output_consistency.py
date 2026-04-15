#!/usr/bin/env python3
"""
Check Output Consistency
========================

Ensures all generated outputs in output/ have consistent commit stamps.
This prevents the repo from containing mutually inconsistent "official" outputs.

Usage:
    python scripts/check_output_consistency.py [--fix]

Options:
    --fix    Regenerate stale outputs to match current HEAD
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = REPO_ROOT / 'output'

# Files that should have commit stamps
STAMPED_FILES = [
    'metrics/ctd_metrics.json',
    'metrics/ctd_metrics.md',
    'dictionary/draft_dictionary.md',
    'dictionary/draft_dictionary_manifest.json',
    'grammar/draft_grammar.md',
    'grammar/draft_grammar_manifest.json',
    'publication_dashboard.md',
    'editorial_blockers.md',
    'editorial_dashboard.md',
]

# Commands to regenerate each output
REGENERATE_COMMANDS = {
    'metrics/ctd_metrics.json': 'make metrics',
    'metrics/ctd_metrics.md': 'make metrics',
    'dictionary/draft_dictionary.md': 'make dictionary-draft',
    'dictionary/draft_dictionary_manifest.json': 'make dictionary-draft',
    'grammar/draft_grammar.md': 'make grammar-draft',
    'grammar/draft_grammar_manifest.json': 'make grammar-draft',
    'publication_dashboard.md': 'python3 scripts/generate_publication_dashboard.py',
    'editorial_blockers.md': 'python3 scripts/generate_editorial_blockers.py',
    'editorial_dashboard.md': 'python3 scripts/generate_editorial_dashboard.py',
}


def get_current_head():
    """Get current git HEAD short SHA."""
    result = subprocess.run(
        ['git', 'rev-parse', '--short', 'HEAD'],
        capture_output=True, text=True, cwd=REPO_ROOT
    )
    return result.stdout.strip()


def extract_commit_stamp(filepath: Path) -> str:
    """Extract commit stamp from a file."""
    if not filepath.exists():
        return None
    
    content = filepath.read_text()
    
    # Try JSON format
    if filepath.suffix == '.json':
        try:
            data = json.loads(content)
            # Try meta.git_commit first (ctd_metrics.json format)
            stamp = data.get('meta', {}).get('git_commit', None)
            if stamp:
                return stamp
            # Try top-level git_commit (manifest format)
            stamp = data.get('git_commit', None)
            if stamp:
                return stamp
        except json.JSONDecodeError:
            pass
    
    # Try markdown comment format: <!-- Commit: abc123 -->
    match = re.search(r'<!--\s*Commit:\s*([a-f0-9]+)\s*-->', content)
    if match:
        return match.group(1)
    
    # Try "git_commit": "abc123" format (fallback regex)
    match = re.search(r'"git_commit":\s*"([a-f0-9]+)"', content)
    if match:
        return match.group(1)
    
    return None


def stamps_match(stamp1: str, stamp2: str) -> bool:
    """Check if two commit stamps match (handles different lengths)."""
    if not stamp1 or not stamp2:
        return False
    min_len = min(len(stamp1), len(stamp2))
    return stamp1[:min_len] == stamp2[:min_len]


def check_consistency(fix: bool = False) -> bool:
    """Check all outputs have consistent commit stamps. Returns True if consistent."""
    current_head = get_current_head()
    print(f"Current HEAD: {current_head}")
    print()
    
    stamps = {}
    missing = []
    
    for rel_path in STAMPED_FILES:
        filepath = OUTPUT_DIR / rel_path
        if not filepath.exists():
            missing.append(rel_path)
            continue
        
        stamp = extract_commit_stamp(filepath)
        stamps[rel_path] = stamp
    
    # Report findings
    if missing:
        print("Missing files:")
        for f in missing:
            print(f"  ❌ {f}")
        print()
    
    # Group by stamp (normalize to 7 chars for grouping)
    by_stamp = {}
    for path, stamp in stamps.items():
        norm_stamp = stamp[:7] if stamp else None
        if norm_stamp not in by_stamp:
            by_stamp[norm_stamp] = []
        by_stamp[norm_stamp].append(path)
    
    print("Commit stamps found:")
    for stamp, files in sorted(by_stamp.items(), key=lambda x: -len(x[1])):
        status = "✓" if stamps_match(stamp, current_head) else "⚠️ STALE"
        print(f"  {stamp or 'NONE'}: {len(files)} files {status}")
        for f in files:
            print(f"    - {f}")
    print()
    
    # Check for inconsistency
    stale_files = [f for f, s in stamps.items() if not stamps_match(s, current_head)]
    
    if not stale_files and not missing:
        print("✓ All outputs are consistent with current HEAD")
        return True
    
    if stale_files:
        print(f"❌ {len(stale_files)} files have stale commit stamps")
        
        if fix:
            print("\nRegenerating stale outputs...")
            commands_needed = set()
            for f in stale_files:
                if f in REGENERATE_COMMANDS:
                    commands_needed.add(REGENERATE_COMMANDS[f])
            
            for cmd in sorted(commands_needed):
                print(f"  Running: {cmd}")
                result = subprocess.run(
                    cmd, shell=True, cwd=REPO_ROOT,
                    capture_output=True, text=True
                )
                if result.returncode != 0:
                    print(f"    ERROR: {result.stderr}")
                else:
                    print(f"    OK")
            
            print("\nRe-checking...")
            return check_consistency(fix=False)
        else:
            print("Run with --fix to regenerate stale outputs")
    
    return False


def main():
    parser = argparse.ArgumentParser(description='Check output commit consistency')
    parser.add_argument('--fix', action='store_true',
                       help='Regenerate stale outputs to match current HEAD')
    args = parser.parse_args()
    
    consistent = check_consistency(fix=args.fix)
    sys.exit(0 if consistent else 1)


if __name__ == '__main__':
    main()
