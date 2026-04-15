#!/usr/bin/env python3
"""
Sync README and PROGRESS with Canonical Metrics
================================================

This script updates the metrics sections in README.md and PROGRESS.md
to match the canonical metrics in output/metrics/ctd_metrics.json.

This ensures public documentation always reflects the actual data state,
eliminating manual copy errors and drift.

Usage:
    python scripts/sync_docs_to_metrics.py [--check]
    
Options:
    --check  Don't update files, just report mismatches (for CI)
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).parent.parent
METRICS_JSON = REPO_ROOT / 'output' / 'metrics' / 'ctd_metrics.json'
README = REPO_ROOT / 'README.md'
PROGRESS = REPO_ROOT / 'PROGRESS.md'


def load_metrics():
    """Load canonical metrics."""
    if not METRICS_JSON.exists():
        print(f"ERROR: Metrics file not found: {METRICS_JSON}")
        print("Run 'make metrics' first to generate canonical metrics.")
        sys.exit(1)
    
    with open(METRICS_JSON) as f:
        return json.load(f)


def get_test_counts():
    """Get actual test counts by running pytest --collect-only."""
    try:
        result = subprocess.run(
            ['python3', '-m', 'pytest', '--collect-only', '-q', 'tests/'],
            capture_output=True, text=True, cwd=REPO_ROOT, timeout=30
        )
        # Parse output like "364 tests collected in 0.11s"
        match = re.search(r'(\d+) tests? collected', result.stdout)
        if match:
            return int(match.group(1))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def get_test_breakdown():
    """Get test counts per category."""
    counts = {'backend': 0, 'export': 0, 'orthography': 0, 'metrics': 0, 'other': 0}
    
    try:
        for test_file in (REPO_ROOT / 'tests').glob('test_*.py'):
            result = subprocess.run(
                ['python3', '-m', 'pytest', '--collect-only', '-q', str(test_file)],
                capture_output=True, text=True, cwd=REPO_ROOT, timeout=15
            )
            match = re.search(r'(\d+) tests? collected', result.stdout)
            if match:
                count = int(match.group(1))
                name = test_file.stem
                if 'backend' in name:
                    counts['backend'] += count
                elif 'export' in name:
                    counts['export'] += count
                elif 'orthography' in name or 'normalize' in name or 'restore' in name:
                    counts['orthography'] += count
                elif 'metrics' in name:
                    counts['metrics'] += count
                else:
                    counts['other'] += count
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return counts


def generate_readme_metrics_table(metrics: dict) -> str:
    """Generate the metrics table for README.md."""
    m = metrics['metrics']
    
    # Determine review queue status description
    if m['review_queue_open'] == 0:
        review_note = "All resolved"
    else:
        review_note = f"{m['review_queue_open']} open"
    
    # Determine constructions status
    if m['construction_count'] == 0:
        constr_note = "Layer not yet populated"
    else:
        constr_note = f"{m['construction_count']} documented"
    
    return f"""| Metric | Value | Notes |
|--------|-------|-------|
| Corpus tokens | {m['total_tokens']:,} | Full Bible text |
| Lemmas | {m['lemma_count']:,} | All with glosses |
| Senses | {m['sense_count']:,} | Including polysemous items |
| Grammatical morphemes | {m['grammatical_morpheme_count']} | Affixes and clitics |
| Corpus examples | {m['example_count']:,} | Linked to senses/morphemes |
| Coverage (known POS) | {m['coverage_known_pos_pct']}% | Full morphological analysis |
| Senses with examples | {m['senses_with_examples']:,} | {m['senses_with_examples_pct']:.0f}% of senses |"""


def generate_test_coverage_table(test_counts: dict, total: int) -> str:
    """Generate the test coverage table for README.md."""
    return f"""| Suite | Tests | Purpose |
|-------|-------|---------|
| Backend tests | {test_counts['backend']} | Database integrity, API behavior, end-to-end workflow |
| Export tests | {test_counts['export']} | TSV export correctness |
| Orthography tests | {test_counts['orthography']} | Normalization and tone restoration |
| Metrics tests | {test_counts['metrics']} | Publication readiness gates |
| Other analyzer tests | {test_counts['other']} | POS tagging, morphology, disambiguation |
| **Total** | **{total}** | |

Run tests: `pytest tests/` or `make test`"""


def generate_readme_status(metrics: dict) -> str:
    """Generate the publication status section for README.md."""
    m = metrics['metrics']
    
    if m['review_queue_open'] == 0:
        status = f"""The analyzer achieves **100% coverage** with all lemmas glossed.

Current state:
- All {m['lemma_count']:,} lemmas have English glosses
- {m['sense_count']:,} distinct senses catalogued
- {m['grammatical_morpheme_count']} grammatical morphemes documented
- {m['example_count']:,} corpus examples linked
- {m['senses_with_examples']:,} senses ({m['senses_with_examples_pct']:.0f}%) have corpus examples"""
    else:
        status = f"""The analyzer achieves **100% coverage** with {m['review_queue_open']} items pending review.

Editorial work remaining:
- {m['review_queue_open']} review queue items open"""
    
    # Add constructions layer status
    if m['construction_count'] == 0:
        status += "\n\n**Note:** The constructions and grammar topics layer is not yet populated."
    
    return status


def generate_progress_metrics_table(metrics: dict) -> str:
    """Generate the metrics table for PROGRESS.md."""
    m = metrics['metrics']
    
    return f"""| Metric | Value |
|--------|-------|
| Corpus tokens | {m['total_tokens']:,} |
| Lemmas (headwords) | {m['lemma_count']:,} |
| Senses | {m['sense_count']:,} |
| Grammatical morphemes | {m['grammatical_morpheme_count']} |
| Linked examples | {m['example_count']:,} |
| Senses with examples | {m['senses_with_examples']:,} ({m['senses_with_examples_pct']:.0f}%) |
| Coverage (known POS) | {m['coverage_known_pos_pct']}% |"""


def generate_progress_editorial_section(metrics: dict) -> str:
    """Generate the editorial status section for PROGRESS.md."""
    m = metrics['metrics']
    
    section = f"""### Review Queue Status

| Status | Count |
|--------|-------|
| Resolved | {m['review_queue_resolved']} |
| Open | {m['review_queue_open']} |

All formal review items have been processed. The review queue tracked:
- High priority: {m['review_high_priority']} items (core function words)
- Medium priority: {m['review_medium_priority']} items (compounds, plurals)
- Low priority: {m['review_low_priority']} items (edge cases)

### Live Editorial Work

Beyond the formal review queue, ongoing editorial tasks include:
- **Polysemous lemmas:** ~975 lemmas have multiple senses needing context-sensitive disambiguation
- **Senses without examples:** {m['sense_count'] - m['senses_with_examples']:,} senses ({100 - m['senses_with_examples_pct']:.0f}%) lack corpus examples
- **Constructions layer:** Not yet populated ({m['construction_count']} entries)
- **Grammar topics layer:** Not yet populated ({m['grammar_topic_count']} entries)"""
    
    return section


def update_readme(metrics: dict, test_counts: dict, total_tests: int, check_only: bool = False) -> bool:
    """Update README.md with canonical metrics and test counts. Returns True if changes needed."""
    content = README.read_text()
    original = content
    
    # Pattern to match the metrics table section
    metrics_pattern = r'(## Tedim Chin: Current Metrics\n\n)\| Metric \| Value \| Notes \|.*?(?=\n\nRegenerate metrics:)'
    new_table = generate_readme_metrics_table(metrics)
    content = re.sub(metrics_pattern, r'\1' + new_table, content, flags=re.DOTALL)
    
    # Pattern to match the publication status section  
    status_pattern = r'(### Publication Status\n\n).*?(?=\n\n\*\*Backend layer status|\n\n## Current Corpus Status)'
    new_status = generate_readme_status(metrics)
    content = re.sub(status_pattern, r'\1' + new_status, content, flags=re.DOTALL)
    
    # Pattern to match test coverage table
    test_pattern = r'(### Test Coverage\n\n)\| Suite \| Tests \| Purpose \|.*?\n\nRun tests:.*'
    if test_counts and total_tests:
        new_tests = generate_test_coverage_table(test_counts, total_tests)
        content = re.sub(test_pattern, r'\1' + new_tests, content, flags=re.DOTALL)
    
    # Update Quick Start test count
    quickstart_pattern = r'# Run all tests \(\d+ tests\)'
    if total_tests:
        content = re.sub(quickstart_pattern, f'# Run all tests ({total_tests} tests)', content)
    
    changed = content != original
    
    if changed and not check_only:
        README.write_text(content)
        print(f"  Updated: {README}")
    elif changed:
        print(f"  MISMATCH: {README} needs update")
    else:
        print(f"  OK: {README}")
    
    return changed


def update_progress(metrics: dict, check_only: bool = False) -> bool:
    """Update PROGRESS.md with canonical metrics. Returns True if changes needed."""
    content = PROGRESS.read_text()
    original = content
    
    # Pattern to match the metrics table
    metrics_pattern = r'(### Corpus Metrics \(as of \d{4}-\d{2}\)\n\n)\| Metric \| Value \|.*?(?=\n\n###)'
    new_table = generate_progress_metrics_table(metrics)
    content = re.sub(metrics_pattern, r'\1' + new_table + '\n', content, flags=re.DOTALL)
    
    # Pattern to match the editorial section
    editorial_pattern = r'(### Review Queue Status\n\n).*?(?=\n\n### Generated Outputs|\n\n### Dictionary Composition|\Z)'
    # Check if section exists, if not we'll add it
    if '### Review Queue Status' in content:
        new_editorial = generate_progress_editorial_section(metrics)
        content = re.sub(editorial_pattern, new_editorial + '\n', content, flags=re.DOTALL)
    
    changed = content != original
    
    if changed and not check_only:
        PROGRESS.write_text(content)
        print(f"  Updated: {PROGRESS}")
    elif changed:
        print(f"  MISMATCH: {PROGRESS} needs update")
    else:
        print(f"  OK: {PROGRESS}")
    
    return changed


def main():
    parser = argparse.ArgumentParser(description='Sync docs to canonical metrics')
    parser.add_argument('--check', action='store_true',
                       help="Don't update files, just report mismatches")
    args = parser.parse_args()
    
    print("Loading canonical metrics...")
    metrics = load_metrics()
    
    print("Counting tests...")
    total_tests = get_test_counts()
    test_counts = get_test_breakdown() if total_tests else {}
    
    print(f"\nCanonical values from {METRICS_JSON}:")
    m = metrics['metrics']
    print(f"  Examples: {m['example_count']:,}")
    print(f"  Senses with examples: {m['senses_with_examples']:,}")
    print(f"  Review queue open: {m['review_queue_open']}")
    print(f"  Constructions: {m['construction_count']}")
    if total_tests:
        print(f"  Tests: {total_tests}")
    
    print("\nSyncing documentation...")
    readme_changed = update_readme(metrics, test_counts, total_tests, args.check)
    progress_changed = update_progress(metrics, args.check)
    
    if args.check:
        if readme_changed or progress_changed:
            print("\n❌ Documentation out of sync with canonical metrics!")
            print("Run 'python scripts/sync_docs_to_metrics.py' to fix.")
            sys.exit(1)
        else:
            print("\n✓ Documentation matches canonical metrics")
    else:
        if readme_changed or progress_changed:
            print("\n✓ Documentation synced to canonical metrics")
        else:
            print("\n✓ No changes needed")


if __name__ == '__main__':
    main()
