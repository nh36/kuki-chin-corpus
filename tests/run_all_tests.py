#!/usr/bin/env python3
"""
Run all Tedim Chin morphological analyzer tests.

Usage: python3 tests/run_all_tests.py [-v]
"""

import sys
import os
import unittest
import importlib.util

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

def load_simple_test_module(filepath):
    """Load a test module that uses simple function-based tests (not unittest)."""
    spec = importlib.util.spec_from_file_location("test_module", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_simple_tests(module, name):
    """Run function-based tests and return (passed, failed)."""
    passed = 0
    failed = 0
    for attr in dir(module):
        if attr.startswith('test_'):
            func = getattr(module, attr)
            if callable(func):
                try:
                    func()
                    passed += 1
                    print(f"  ✓ {attr}")
                except AssertionError as e:
                    failed += 1
                    print(f"  ✗ {attr}: {e}")
                except Exception as e:
                    failed += 1
                    print(f"  ✗ {attr}: {type(e).__name__}: {e}")
    return passed, failed

def main():
    verbose = '-v' in sys.argv
    
    # Test files - unittest-based
    unittest_tests = [
        'test_pos_tagging.py',
        'test_vp_slots.py',
        'test_sak_caus_benf.py',
        'test_directional_suffixes.py',
        'test_prefix_agr_poss.py',
        'test_normalize_orthography.py',
        'test_restore_tone.py',
        'test_thum_disambiguation.py',
    ]
    
    # Test files - simple function-based
    simple_tests = [
        'test_habitual_markers.py',
        'test_thei_theih_allomorphy.py',
    ]
    
    test_dir = os.path.dirname(__file__)
    total_passed = 0
    total_failed = 0
    
    print("=" * 60)
    print("Tedim Chin Morphological Analyzer Test Suite")
    print("=" * 60)
    
    # Run unittest-based tests
    print("\n--- unittest-based tests ---\n")
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for test_file in unittest_tests:
        filepath = os.path.join(test_dir, test_file)
        if os.path.exists(filepath):
            # Skip slow coverage test by default
            if test_file == 'test_coverage_reporting.py' and '-a' not in sys.argv:
                print(f"Skipping {test_file} (slow - use -a to include)")
                continue
            spec = importlib.util.spec_from_file_location(test_file[:-3], filepath)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
                tests = loader.loadTestsFromModule(module)
                suite.addTests(tests)
            except Exception as e:
                print(f"Error loading {test_file}: {e}")
    
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)
    total_passed += result.testsRun - len(result.failures) - len(result.errors)
    total_failed += len(result.failures) + len(result.errors)
    
    # Run simple function-based tests
    print("\n--- function-based tests ---\n")
    for test_file in simple_tests:
        filepath = os.path.join(test_dir, test_file)
        if os.path.exists(filepath):
            print(f"\n{test_file}:")
            try:
                module = load_simple_test_module(filepath)
                passed, failed = run_simple_tests(module, test_file)
                total_passed += passed
                total_failed += failed
            except Exception as e:
                print(f"  Error loading: {e}")
                total_failed += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    print("=" * 60)
    
    return 0 if total_failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
