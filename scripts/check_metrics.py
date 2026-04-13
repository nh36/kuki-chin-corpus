#!/usr/bin/env python3
"""
Check for metric drift between canonical metrics and documentation.

This script compares the canonical metrics from the backend with claims in
README.md and PROGRESS.md to catch metric drift.

Usage:
    python scripts/check_metrics.py [--db data/ctd_backend.db]

Returns exit code 1 if any drift is detected.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))


def load_canonical_metrics(metrics_path: str = 'output/metrics/ctd_metrics.json') -> dict:
    """Load the canonical metrics from JSON."""
    if not Path(metrics_path).exists():
        print(f"ERROR: Canonical metrics not found: {metrics_path}")
        print("Run 'make metrics' to generate them first.")
        sys.exit(1)
    
    with open(metrics_path) as f:
        return json.load(f)


def extract_numbers_from_text(text: str) -> dict:
    """Extract all numeric claims from markdown text."""
    findings = {}
    
    # Pattern: coverage percentages like "100% coverage" or "100.00%"
    for match in re.finditer(r'(\d+(?:\.\d+)?)\s*%\s*(?:coverage|analyzed|fully)', text, re.I):
        key = f"coverage_claim_{match.start()}"
        findings[key] = float(match.group(1))
    
    # Pattern: token counts like "831,152 tokens" or "771,190 tokens"
    for match in re.finditer(r'([\d,]+)\s*tokens?', text, re.I):
        num = int(match.group(1).replace(',', ''))
        key = f"token_count_{match.start()}"
        findings[key] = num
    
    # Pattern: lemma/entry counts like "7,000+ entries" or "7,339 lemmas"
    for match in re.finditer(r'([\d,]+)\+?\s*(?:entries|lemmas|dictionary entries|headwords)', text, re.I):
        num = int(match.group(1).replace(',', ''))
        key = f"lemma_count_{match.start()}"
        findings[key] = num
    
    # Pattern: wordform counts
    for match in re.finditer(r'([\d,]+)\s*(?:wordforms?|distinct forms)', text, re.I):
        num = int(match.group(1).replace(',', ''))
        key = f"wordform_count_{match.start()}"
        findings[key] = num
    
    # Pattern: test counts
    for match in re.finditer(r'(\d+)\s*(?:regression )tests?', text, re.I):
        key = f"test_count_{match.start()}"
        findings[key] = int(match.group(1))
    
    return findings


def check_consistency(canonical: dict, doc_path: str) -> list:
    """Check a document for consistency with canonical metrics."""
    issues = []
    
    if not Path(doc_path).exists():
        return issues
    
    with open(doc_path) as f:
        content = f.read()
    
    metrics = canonical['metrics']
    
    # Check for specific claim patterns and compare to canonical
    
    # Coverage claims
    coverage_patterns = [
        (r'(\d+(?:\.\d+)?)\s*%\s*coverage', 'coverage_known_pos_pct'),
        (r'(\d+(?:\.\d+)?)\s*%\s*\(.*fully analyzed', 'coverage_known_pos_pct'),
    ]
    
    for pattern, metric_key in coverage_patterns:
        for match in re.finditer(pattern, content, re.I):
            claimed = float(match.group(1))
            actual = metrics.get(metric_key, 100.0)
            if abs(claimed - actual) > 0.5:  # Allow 0.5% tolerance
                issues.append({
                    'file': doc_path,
                    'claimed': f"{claimed}%",
                    'actual': f"{actual}%",
                    'context': content[max(0, match.start()-20):match.end()+20].strip(),
                    'metric': metric_key,
                })
    
    # Token count claims - look for specific format patterns
    token_patterns = [
        (r'([\d,]+)\s*/\s*([\d,]+)\s*tokens', 'total_tokens'),  # fraction form
        (r'([\d,]+)\s*tokens?\s+fully', 'total_tokens'),
    ]
    
    for pattern, metric_key in token_patterns:
        for match in re.finditer(pattern, content, re.I):
            if '/' in match.group(0):
                # Fraction form like "771,190/771,201 tokens"
                claimed = int(match.group(2).replace(',', ''))
            else:
                claimed = int(match.group(1).replace(',', ''))
            
            actual = metrics.get(metric_key)
            if actual and abs(claimed - actual) > 10000:  # Allow 10k tolerance for old numbers
                issues.append({
                    'file': doc_path,
                    'claimed': f"{claimed:,}",
                    'actual': f"{actual:,}",
                    'context': content[max(0, match.start()-20):match.end()+40].strip(),
                    'metric': metric_key,
                })
    
    # Lemma/entry count claims - be careful to distinguish from lexicons
    for match in re.finditer(r'([\d,]+)\+?\s*(?:dictionary )?entries', content, re.I):
        claimed = int(match.group(1).replace(',', ''))
        actual = metrics.get('lemma_count', 0)
        
        # Skip if this is clearly about lexicon entries, not lemmas
        context_before = content[max(0, match.start()-100):match.start()].lower()
        if 'lexicon' in context_before or 'bootstrap' in context_before:
            continue
        if 'work queue' in context_before or 'work_queue' in context_before:
            continue
        if 'wordform' in context_before or 'inventory' in context_before:
            continue
        if 'per language' in context_before:  # "~4,000 entries per language"
            continue
        if 'initial analyzer' in context_before:  # "~5,000 entries from bootstrap"
            continue
        
        # If claim is significantly different (and not just "7,000+" approximate)
        if '+' not in match.group(0) and abs(claimed - actual) > 500:
            issues.append({
                'file': doc_path,
                'claimed': f"{claimed:,}",
                'actual': f"{actual:,}",
                'context': content[max(0, match.start()-20):match.end()+20].strip(),
                'metric': 'lemma_count',
            })
    
    return issues


def main():
    parser = argparse.ArgumentParser(description='Check for metric drift')
    parser.add_argument('--db', default='data/ctd_backend.db',
                        help='Path to backend database')
    parser.add_argument('--metrics', default='output/metrics/ctd_metrics.json',
                        help='Path to canonical metrics JSON')
    args = parser.parse_args()
    
    # Load canonical metrics
    canonical = load_canonical_metrics(args.metrics)
    
    # Check documents
    docs_to_check = ['README.md', 'PROGRESS.md']
    all_issues = []
    
    for doc in docs_to_check:
        issues = check_consistency(canonical, doc)
        all_issues.extend(issues)
    
    if all_issues:
        print("⚠️  METRIC DRIFT DETECTED")
        print("=" * 60)
        for issue in all_issues:
            print(f"\nFile: {issue['file']}")
            print(f"  Claimed: {issue['claimed']}")
            print(f"  Actual:  {issue['actual']}")
            print(f"  Metric:  {issue['metric']}")
            print(f"  Context: ...{issue['context']}...")
        print()
        print(f"Found {len(all_issues)} potential drift issue(s).")
        print("Run 'make metrics' and update documentation to match.")
        sys.exit(1)
    else:
        print("✓ No metric drift detected")
        print(f"  Checked: {', '.join(docs_to_check)}")
        print(f"  Against: {args.metrics}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main() or 0)
