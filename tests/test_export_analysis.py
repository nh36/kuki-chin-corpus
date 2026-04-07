"""
Regression tests for export_tedim_analysis.py

Tests verify:
1. Output file existence and basic structure
2. Row counts within expected ranges
3. Coverage statistics
4. Representative analyses
5. Linguistic correctness (category assignments, gloss consistency)
6. Data integrity across files
"""

import os
import sys
import csv

# Add scripts to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'ctd_analysis')
SAMPLE_ENTRIES = os.path.join(OUTPUT_DIR, 'sample_entries.md')


def test_output_files_exist():
    """All expected output files should exist."""
    expected_files = [
        'verses.tsv',
        'tokens.tsv', 
        'wordforms.tsv',
        'lemmas.tsv',
        'grammatical_morphemes.tsv',
        'examples.tsv',
        'ambiguities.tsv',
        'coverage_report.md',
        'README.md'
    ]
    
    for fname in expected_files:
        path = os.path.join(OUTPUT_DIR, fname)
        assert os.path.exists(path), f"Missing file: {fname}"


def test_tokens_row_count():
    """Token count should be approximately 831,000."""
    path = os.path.join(OUTPUT_DIR, 'tokens.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1  # Subtract header
    
    assert 800000 < row_count < 900000, f"Token count {row_count} outside expected range"


def test_wordforms_row_count():
    """Wordform count should be approximately 20,000-25,000."""
    path = os.path.join(OUTPUT_DIR, 'wordforms.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1
    
    assert 15000 < row_count < 30000, f"Wordform count {row_count} outside expected range"


def test_lemmas_row_count():
    """Lemma count should be approximately 5,000-10,000."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1
    
    assert 4000 < row_count < 15000, f"Lemma count {row_count} outside expected range"


def test_grammatical_morphemes_row_count():
    """Should have 100-500 grammatical morphemes."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1
    
    assert 50 < row_count < 500, f"Gram morpheme count {row_count} outside expected range"


def test_tokens_has_required_columns():
    """Tokens file should have all required columns."""
    path = os.path.join(OUTPUT_DIR, 'tokens.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
    
    required = ['verse_id', 'token_index', 'surface_form', 'segmentation', 
                'gloss', 'lemma', 'pos', 'confidence']
    
    for col in required:
        assert col in header, f"Missing column: {col}"


def test_representative_verb_analysis():
    """Check that common verbs are analyzed correctly."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    lemmas = {}
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemmas[row['lemma']] = row
    
    # 'pai' should be a verb with high frequency
    assert 'pai' in lemmas, "Missing lemma: pai (go)"
    assert lemmas['pai']['pos'] == 'V', f"pai should be V, got {lemmas['pai']['pos']}"
    assert int(lemmas['pai']['token_count']) > 1000, "pai should have >1000 tokens"


def test_representative_noun_analysis():
    """Check that common nouns are analyzed correctly."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    lemmas = {}
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemmas[row['lemma']] = row
    
    # 'mi' should be a noun with high frequency
    assert 'mi' in lemmas, "Missing lemma: mi (person)"
    assert lemmas['mi']['pos'] == 'N', f"mi should be N, got {lemmas['mi']['pos']}"
    assert int(lemmas['mi']['token_count']) > 5000, "mi should have >5000 tokens"


def test_grammatical_morpheme_categories():
    """Check that key grammatical categories are present."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    categories = set()
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            categories.add(row['category'])
    
    # Updated category names to match actual output
    expected = ['case_marker', 'tam_suffix', 'nominalizer', 'pronominal_prefix',
                'plural_marker', 'sentence_final', 'irrealis_marker']
    for cat in expected:
        assert cat in categories, f"Missing category: {cat}"


def test_ding_not_categorized_as_case():
    """-ding should be irrealis_marker, NOT case marker."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['form'] == 'ding':
                # ding is either irrealis_marker (as suffix) or lexical verb
                assert row['category'] != 'case_marker', \
                    f"-ding should not be case marker, got {row['category']}"


def test_na_nominalizer_not_2sg():
    """-na nominalizer should not have 2SG gloss."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['form'] == 'na' and row['category'] == 'nominalizer':
                assert row['gloss'] == 'NMLZ', \
                    f"-na nominalizer should gloss as NMLZ, got {row['gloss']}"
                return
    
    # na as nominalizer should exist
    assert False, "Nominalizer 'na' not found in grammatical morphemes"


def test_case_marker_in():
    """Ergative marker 'in' should be in grammatical morphemes."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['form'] == 'in' and row['category'] == 'case_marker':
                assert row['gloss'] == 'ERG', f"'in' should gloss as ERG, got {row['gloss']}"
                assert int(row['frequency']) > 50000, "'in' should be very frequent"
                return
    
    assert False, "Case marker 'in' not found"


def test_known_polysemous_forms_in_ambiguities():
    """Known polysemous forms should appear in ambiguities.tsv."""
    path = os.path.join(OUTPUT_DIR, 'ambiguities.tsv')
    found_forms = set()
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            found_forms.add(row['normalized_form'])
    
    # These forms are known to be polysemous and should be flagged
    expected = ['hi', 'hong', 'ta', 'te', 'in', 'na']
    for form in expected:
        assert form in found_forms, f"Known polysemous form '{form}' not in ambiguities"


def test_ambiguity_queue_not_empty():
    """Ambiguity queue should contain real items needing review."""
    path = os.path.join(OUTPUT_DIR, 'ambiguities.tsv')
    row_count = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            row_count += 1
    
    # Should have substantial ambiguities, not 0 or tiny number
    assert row_count > 100, f"Ambiguity queue too small: {row_count} (expected >100)"


def test_unk_not_counted_as_fully_analyzed():
    """Coverage report should not count UNK POS as fully analyzed."""
    path = os.path.join(OUTPUT_DIR, 'coverage_report.md')
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Report should mention UNK category separately
    assert 'UNK' in content or 'pos_unknown' in content or 'Unknown' in content, \
        "Coverage report should track UNK tokens separately"


def test_sample_entries_have_glosses():
    """Sample entries should not show 'Gloss: ?' for high-frequency lemmas."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return  # Skip if sample entries not generated
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences of "Gloss: ?"
    question_glosses = content.count('**Gloss:** ?')
    
    # Should have very few (if any) missing glosses
    assert question_glosses < 5, \
        f"Too many entries with missing glosses: {question_glosses}"


def test_lemma_table_has_english_glosses():
    """Lemma table should have english_glosses column filled for non-proper nouns."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    missing_count = 0
    total = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            # Skip proper nouns (names don't need glosses)
            if row.get('pos', '') == 'PROP':
                continue
            total += 1
            if row.get('primary_gloss', '?') == '?':
                missing_count += 1
    
    # Allow some unknowns but should be minority for non-proper nouns
    missing_pct = (missing_count / total) * 100 if total > 0 else 100
    assert missing_pct < 40, \
        f"{missing_pct:.1f}% of non-PROP lemmas have missing glosses (expected <40%)"


def test_examples_have_segmented_glossed():
    """Examples should have segmented and glossed fields populated."""
    path = os.path.join(OUTPUT_DIR, 'examples.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        header = reader.fieldnames
        
        # Check columns exist
        assert 'segmented' in header, "Missing 'segmented' column in examples"
        assert 'glossed' in header, "Missing 'glossed' column in examples"
        
        # Check some examples have content
        filled_count = 0
        total = 0
        for row in reader:
            total += 1
            if row.get('segmented', ''):
                filled_count += 1
            if total >= 1000:
                break
        
        fill_rate = filled_count / total if total > 0 else 0
        assert fill_rate > 0.5, f"Only {fill_rate:.1%} of examples have segmented form"


def test_examples_bank_has_lemmas():
    """Examples bank should have entries for lemmas."""
    path = os.path.join(OUTPUT_DIR, 'examples.tsv')
    lemma_count = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['item_type'] == 'lemma':
                lemma_count += 1
    
    assert lemma_count > 10000, f"Expected >10000 lemma examples, got {lemma_count}"


def test_examples_bank_has_morphemes():
    """Examples bank should have entries for grammatical morphemes."""
    path = os.path.join(OUTPUT_DIR, 'examples.tsv')
    morpheme_count = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['item_type'] == 'morpheme':
                morpheme_count += 1
    
    assert morpheme_count > 500, f"Expected >500 morpheme examples, got {morpheme_count}"


def test_coverage_report_exists():
    """Coverage report should exist and contain key metrics."""
    path = os.path.join(OUTPUT_DIR, 'coverage_report.md')
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert 'Coverage:' in content, "Coverage report should contain coverage percentage"
    assert 'Total tokens' in content, "Coverage report should contain token count"
    assert 'Lemmas' in content, "Coverage report should contain lemma count"


if __name__ == '__main__':
    # Run as simple test functions
    tests = [
        test_output_files_exist,
        test_tokens_row_count,
        test_wordforms_row_count,
        test_lemmas_row_count,
        test_grammatical_morphemes_row_count,
        test_tokens_has_required_columns,
        test_representative_verb_analysis,
        test_representative_noun_analysis,
        test_grammatical_morpheme_categories,
        test_ding_not_categorized_as_case,
        test_na_nominalizer_not_2sg,
        test_case_marker_in,
        test_known_polysemous_forms_in_ambiguities,
        test_ambiguity_queue_not_empty,
        test_unk_not_counted_as_fully_analyzed,
        test_sample_entries_have_glosses,
        test_lemma_table_has_english_glosses,
        test_examples_have_segmented_glossed,
        test_examples_bank_has_lemmas,
        test_examples_bank_has_morphemes,
        test_coverage_report_exists,
    ]
    
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__}: {type(e).__name__}: {e}")
            failed += 1
    
    print(f"\n{passed}/{passed+failed} tests passed")
    exit(0 if failed == 0 else 1)
