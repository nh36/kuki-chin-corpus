#!/usr/bin/env python3
"""
Test metrics consistency.

These tests ensure that:
1. The metrics pipeline generates valid output
2. README/PROGRESS don't drift from canonical metrics
3. Publication readiness gates are met
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest


# Paths
REPO_ROOT = Path(__file__).parent.parent
METRICS_JSON = REPO_ROOT / 'output' / 'metrics' / 'ctd_metrics.json'
METRICS_SCRIPT = REPO_ROOT / 'scripts' / 'generate_metrics.py'
CHECK_SCRIPT = REPO_ROOT / 'scripts' / 'check_metrics.py'
DB_PATH = REPO_ROOT / 'data' / 'ctd_backend.db'


class TestMetricsGeneration:
    """Test that metrics can be generated."""
    
    def test_metrics_json_exists(self):
        """Metrics JSON should exist (run 'make metrics' if not)."""
        assert METRICS_JSON.exists(), \
            f"Metrics JSON not found at {METRICS_JSON}. Run 'make metrics' to generate."
    
    def test_metrics_json_valid(self):
        """Metrics JSON should be valid JSON."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        assert 'meta' in data
        assert 'metrics' in data
        assert 'definitions' in data
    
    def test_metrics_has_required_keys(self):
        """Metrics should include all required fields."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        required_metrics = [
            'total_tokens',
            'total_sources',
            'tokens_with_known_pos',
            'lemma_count',
            'sense_count',
            'grammatical_morpheme_count',
            'example_count',
            'review_queue_open',
            'coverage_known_pos_pct',
        ]
        
        for key in required_metrics:
            assert key in data['metrics'], f"Missing required metric: {key}"


class TestMetricsConsistency:
    """Test that documentation matches canonical metrics."""
    
    def test_no_metric_drift(self):
        """README and PROGRESS should match canonical metrics."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        if not CHECK_SCRIPT.exists():
            pytest.skip("Check script not found")
        
        result = subprocess.run(
            [sys.executable, str(CHECK_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT
        )
        
        assert result.returncode == 0, \
            f"Metric drift detected:\n{result.stdout}\n{result.stderr}"


class TestPublicationReadinessGates:
    """Test publication readiness criteria."""
    
    def test_coverage_above_threshold(self):
        """Coverage should be at least 99%."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        coverage = data['metrics'].get('coverage_known_pos_pct', 0)
        assert coverage >= 99.0, f"Coverage {coverage}% is below 99% threshold"
    
    def test_review_queue_manageable(self):
        """Review queue should be manageable - high-priority items tracked."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        high_priority = data['metrics'].get('review_high_priority', 0)
        total_open = data['metrics'].get('review_queue_open', 0)
        
        # Gate: high-priority items should be under control (< 100)
        # This is a soft gate - allows work in progress
        assert high_priority < 100, \
            f"{high_priority} high-priority review items (target: < 100)"
    
    def test_examples_linked(self):
        """At least 80% of examples should be linked to senses."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        linked_pct = data['metrics'].get('examples_linked_pct', 0)
        assert linked_pct >= 80.0, \
            f"Only {linked_pct}% of examples are linked to senses"
    
    def test_minimum_lemma_count(self):
        """Should have at least 5000 lemmas."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        lemma_count = data['metrics'].get('lemma_count', 0)
        assert lemma_count >= 5000, \
            f"Only {lemma_count} lemmas (minimum 5000 for publication)"
    
    def test_minimum_examples(self):
        """Should have at least 10000 examples."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        example_count = data['metrics'].get('example_count', 0)
        assert example_count >= 10000, \
            f"Only {example_count} examples (minimum 10000 for publication)"
    
    def test_metrics_not_stale(self):
        """Metrics should be from current git commit."""
        if not METRICS_JSON.exists():
            pytest.skip("Metrics JSON not found")
        
        with open(METRICS_JSON) as f:
            data = json.load(f)
        
        # Get current git commit
        result = subprocess.run(
            ['git', 'rev-parse', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT
        )
        current_commit = result.stdout.strip()[:8]
        
        metrics_commit = data['meta'].get('git_commit', 'unknown')
        
        # Warning only - don't fail if metrics are a few commits behind
        if metrics_commit != current_commit:
            pytest.skip(
                f"Metrics from commit {metrics_commit}, current is {current_commit}. "
                "Run 'make metrics' to update."
            )


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
