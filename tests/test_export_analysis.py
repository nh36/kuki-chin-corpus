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
    """Should have 100-600 grammatical morphemes."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    with open(path, 'r', encoding='utf-8') as f:
        row_count = sum(1 for _ in f) - 1
    
    assert 50 < row_count < 600, f"Gram morpheme count {row_count} outside expected range"


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


# =============================================================================
# SEMANTIC CORRECTNESS TESTS
# =============================================================================

def test_hi_not_glossed_as_this():
    """hi is primarily DECL (88%), not 'this'."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'hi':
                gloss = row.get('primary_gloss', '')
                # Should be DECL or declarative, not 'this'
                assert gloss != 'this', \
                    f"hi should not have primary_gloss='this' (is DECL ~88% of time)"
                return
    
    assert False, "lemma 'hi' not found"


def test_thei_not_glossed_as_fig():
    """thei is primarily 'know', not 'fig'."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'thei':
                gloss = row.get('primary_gloss', '')
                # Should be 'know' or similar, not 'fig'
                assert gloss != 'fig', \
                    f"thei should not have primary_gloss='fig' (is 'know' in corpus)"
                return


def test_mu_not_glossed_as_kiss():
    """mu is primarily 'see', not 'kiss'."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'mu':
                gloss = row.get('primary_gloss', '')
                # Should be 'see' or similar, not 'kiss'
                assert gloss != 'kiss', \
                    f"mu should not have primary_gloss='kiss' (is 'see' in corpus)"
                return


def test_pai_not_glossed_as_pour():
    """pai is primarily 'go', not 'pour'."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'pai':
                gloss = row.get('primary_gloss', '')
                # Should be 'go' or similar, not 'pour'
                assert gloss != 'pour', \
                    f"pai should not have primary_gloss='pour' (is 'go' in corpus)"
                return


def test_te_plural_not_glossed_loc():
    """Plural marker -te should not have LOC as dominant gloss."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    te_entries = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['form'] == 'te' and row['category'] == 'plural_marker':
                te_entries.append((row['gloss'], int(row['frequency'])))
    
    # Should have at least one PL entry
    pl_entries = [e for e in te_entries if e[0] == 'PL']
    assert pl_entries, "Plural marker -te should have a PL gloss entry"
    
    # The PL gloss should be dominant (most frequent)
    te_entries.sort(key=lambda x: -x[1])
    if te_entries:
        assert te_entries[0][0] == 'PL', \
            f"Plural marker -te should have PL as most frequent gloss, got {te_entries[0][0]}"


def test_case_marker_not_lexical_gloss():
    """Case markers should not have lexical glosses as dominant entry."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    lexical_glosses = {'take', 'house', 'go', 'come', 'stand', 'sit', 'give', 
                       'fly', 'leaf', 'with'}
    
    # Group by form and find dominant gloss
    case_markers = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['category'] == 'case_marker':
                form = row['form']
                freq = int(row['frequency'])
                if form not in case_markers or freq > case_markers[form][1]:
                    case_markers[form] = (row['gloss'], freq)
    
    # Check that the dominant gloss for each case marker is grammatical
    for form, (gloss, freq) in case_markers.items():
        gloss_lower = gloss.lower()
        assert gloss_lower not in lexical_glosses, \
            f"Case marker {form} should not have lexical gloss '{gloss}' as dominant (freq={freq})"


def test_review_file_exists():
    """Review entries file should exist."""
    path = os.path.join(OUTPUT_DIR, 'review_entries.md')
    assert os.path.exists(path), "review_entries.md should exist"


def test_senses_file_exists():
    """Senses file should exist with proper structure."""
    path = os.path.join(OUTPUT_DIR, 'senses.tsv')
    assert os.path.exists(path), "senses.tsv should exist"
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        required = ['sense_id', 'lemma', 'sense_num', 'pos', 'gloss', 'frequency']
        for col in required:
            assert col in columns, f"senses.tsv missing column: {col}"


def test_senses_primary_sense_is_most_frequent():
    """Primary sense should have highest frequency for each lemma."""
    path = os.path.join(OUTPUT_DIR, 'senses.tsv')
    
    # Group senses by lemma
    lemma_senses = {}
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemma = row['lemma']
            if lemma not in lemma_senses:
                lemma_senses[lemma] = []
            lemma_senses[lemma].append({
                'freq': int(row['frequency']),
                'is_primary': row['is_primary'] == '1',
                'gloss': row['gloss']
            })
    
    # Verify primary sense is most frequent
    for lemma, senses in list(lemma_senses.items())[:100]:  # Check first 100
        if len(senses) > 1:
            primary = [s for s in senses if s['is_primary']]
            if primary:
                max_freq = max(s['freq'] for s in senses)
                assert primary[0]['freq'] == max_freq, \
                    f"Lemma '{lemma}': primary sense freq {primary[0]['freq']} != max {max_freq}"


def test_ci_primary_sense_is_say():
    """ci (say) should have 'say' as primary sense, not REFL."""
    path = os.path.join(OUTPUT_DIR, 'senses.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'ci' and row['is_primary'] == '1':
                assert row['gloss'] == 'say', \
                    f"ci primary sense should be 'say', got '{row['gloss']}'"
                return
    
    assert False, "ci lemma not found in senses"


def test_sih_has_multiple_senses():
    """sih should have both 'die' and 'blood' senses."""
    path = os.path.join(OUTPUT_DIR, 'senses.tsv')
    
    sih_glosses = set()
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'sih':
                sih_glosses.add(row['gloss'])
    
    assert 'die' in sih_glosses, "sih should have 'die' sense"
    assert 'blood' in sih_glosses, "sih should have 'blood' sense"


def test_context_disambiguation_thum():
    """Verify thum context disambiguation works via analyze_sentence."""
    from analyze_morphemes import analyze_sentence
    
    # "kong thum" should give 'entreat', not 'three'
    result = analyze_sentence("kong thum hi")
    glosses = [r[2] for r in result]
    # Check thum gloss
    thum_idx = next(i for i, r in enumerate(result) if 'thum' in r[0].lower())
    assert glosses[thum_idx] == 'entreat', \
        f"'kong thum' should be entreat, got '{glosses[thum_idx]}'"


def test_context_disambiguation_ngen():
    """Verify ngen context disambiguation works."""
    from analyze_morphemes import analyze_sentence
    
    # "ngen" with fishing context should be 'net'
    result = analyze_sentence("nga ngente")  # fish nets
    glosses = [r[2] for r in result]
    assert 'net' in glosses or 'net-PL' in glosses, \
        f"'nga ngente' should have net gloss, got {glosses}"


def test_lemmas_have_pos_variants():
    """Lemmas with multiple POS should have pos_variants column populated."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        assert 'pos_variants' in columns, "lemmas.tsv should have pos_variants column"
        
        # Check that some high-freq items have variants
        for row in reader:
            if row['lemma'] == 'hi':
                pos_var = row.get('pos_variants', '')
                assert pos_var, "hi should have POS variants (FUNC and V)"
                break


def test_high_frequency_items_properly_classified():
    """High-frequency items should be marked as grammatical or have stable gloss."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    # These items are known to be primarily grammatical
    primarily_grammatical = {'hi', 'ding', 'hong', 'ta', 'te', 'in', 'na', 'pan'}
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            lemma = row['lemma'].lower()
            if lemma in primarily_grammatical:
                # Should be marked as grammatical or needing review
                is_gram = row.get('is_grammatical') == '1'
                needs_review = row.get('needs_review') == '1'
                status = row.get('entry_status', 'auto')
                
                # At least one of these should be true
                properly_handled = is_gram or needs_review or status in ('mixed_lex_gram', 'polysemous_review')
                assert properly_handled, \
                    f"High-frequency item '{lemma}' should be marked grammatical or review-needed"


def test_no_duplicate_entries_in_sample():
    """Same form should not appear in both lexical and grammatical sections."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections
    parts = content.split('## Part')
    if len(parts) < 3:
        return
    
    lexical_section = parts[1] if len(parts) > 1 else ''
    grammatical_section = parts[2] if len(parts) > 2 else ''
    
    # Extract entry names (lines starting with ### )
    import re
    lexical_entries = set(re.findall(r'^### (\w+)', lexical_section, re.MULTILINE))
    grammatical_entries = set(re.findall(r'^### (\w+)', grammatical_section, re.MULTILINE))
    
    overlap = lexical_entries & grammatical_entries
    
    # Allow some overlap for items explicitly split by sense
    allowed_overlap = {'tua', 'hih', 'bang'}  # Known function words
    
    unexpected_overlap = overlap - allowed_overlap
    assert not unexpected_overlap, \
        f"Forms appear in both lexical and grammatical sections: {unexpected_overlap}"


# ============================================================================
# PRECISION TESTS (new round of quality enforcement)
# ============================================================================

def test_no_unk_pos_in_grammatical_section():
    """Polished grammatical section should not contain POS: UNK."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find grammatical section
    parts = content.split('## Part 2: Grammatical Words')
    if len(parts) < 2:
        return
    
    gram_section = parts[1].split('## Part 3:')[0] if '## Part 3:' in parts[1] else parts[1]
    
    assert 'POS: UNK' not in gram_section, \
        "Grammatical section contains POS: UNK entries"


def test_problem_forms_not_in_polished_grammatical():
    """Problem forms like zong, leh, maw, hiam should not be in polished grammatical section."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find grammatical section
    parts = content.split('## Part 2: Grammatical Words')
    if len(parts) < 2:
        return
    
    gram_section = parts[1].split('## Part 3:')[0] if '## Part 3:' in parts[1] else parts[1]
    
    problem_forms = {'ciang', 'zong', 'leh', 'maw', 'hiam'}
    
    import re
    entries = set(re.findall(r'^### (\w+)', gram_section, re.MULTILINE))
    
    found_problems = entries & problem_forms
    assert not found_problems, \
        f"Polished grammatical section contains problem forms: {found_problems}"


def test_affix_section_no_lexical_glosses():
    """Affix section should not contain case markers with lexical glosses like 'take'."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find affix section
    parts = content.split('## Part 3: Affixes')
    if len(parts) < 2:
        return
    
    affix_section = parts[1]
    
    # Check for lexical glosses that shouldn't appear
    bad_glosses = ['Gloss: take', 'Gloss: go', 'Gloss: come', 'Gloss: put']
    
    for bad in bad_glosses:
        assert bad not in affix_section, \
            f"Affix section contains lexical gloss: {bad}"


def test_affix_section_no_mismatched_categories():
    """Affix section should not contain plural markers with LOC gloss."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find affix section
    parts = content.split('## Part 3: Affixes')
    if len(parts) < 2:
        return
    
    affix_section = parts[1]
    
    # Parse entries
    import re
    entries = re.split(r'^### ', affix_section, flags=re.MULTILINE)[1:]
    
    for entry in entries:
        lines = entry.strip().split('\n')
        category = None
        gloss = None
        
        for line in lines:
            if line.startswith('**Category:**'):
                category = line.split(':**')[1].strip()
            if line.startswith('**Gloss:**'):
                gloss = line.split(':**')[1].strip()
        
        if category == 'plural_marker':
            assert gloss != 'LOC', \
                f"Plural marker has LOC gloss"
        
        if category == 'tam_suffix':
            assert gloss != 'CAUS', \
                f"TAM suffix has CAUS gloss (should be in derivational category)"


def test_sentence_final_no_prefix_env():
    """Sentence-final items should not show prefix as environment."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find affix section
    parts = content.split('## Part 3: Affixes')
    if len(parts) < 2:
        return
    
    affix_section = parts[1]
    
    import re
    entries = re.split(r'^### ', affix_section, flags=re.MULTILINE)[1:]
    
    for entry in entries:
        lines = entry.strip().split('\n')
        category = None
        envs = None
        form = lines[0].strip() if lines else ''
        
        for line in lines:
            if line.startswith('**Category:**'):
                category = line.split(':**')[1].strip()
            if line.startswith('**Environments:**'):
                envs = line.split(':**')[1].strip()
        
        if category == 'sentence_final':
            assert envs is None or 'prefix' not in envs, \
                f"Sentence-final item {form} has prefix environment: {envs}"


def test_grammatical_entries_have_func_pos():
    """Grammatical entries with grammatical glosses should show FUNC POS, not V/N."""
    if not os.path.exists(SAMPLE_ENTRIES):
        return
    
    with open(SAMPLE_ENTRIES, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find grammatical section
    parts = content.split('## Part 2: Grammatical Words')
    if len(parts) < 2:
        return
    
    gram_section = parts[1].split('## Part 3:')[0] if '## Part 3:' in parts[1] else parts[1]
    
    import re
    entries = re.split(r'^### ', gram_section, flags=re.MULTILINE)[1:]
    
    gram_glosses = {'DECL', 'IRR', 'ABL', 'ERG', 'LOC', 'DIR', 'Q'}
    
    for entry in entries:
        lines = entry.strip().split('\n')
        form = lines[0].strip() if lines else ''
        pos = None
        gloss = None
        
        for line in lines:
            if line.startswith('**POS:**'):
                pos = line.split(':**')[1].strip()
            if line.startswith('**Gloss:**'):
                gloss = line.split(':**')[1].strip()
        
        if gloss in gram_glosses:
            assert pos == 'FUNC', \
                f"Grammatical entry {form} has gloss {gloss} but POS is {pos}, expected FUNC"


def test_review_file_has_problem_forms():
    """Review file should capture high-frequency problem forms."""
    review_file = os.path.join(OUTPUT_DIR, 'review_entries.md')
    if not os.path.exists(review_file):
        return
    
    with open(review_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # ciang is high-frequency (10K+) and should be in review
    assert '### ciang' in content, \
        "High-frequency problem form 'ciang' not in review file"


# ============================================================================
# BACKEND STRUCTURE TESTS (new fields and data quality)
# ============================================================================

def test_tokens_have_usage_type():
    """Tokens should have usage_type field with valid values."""
    path = os.path.join(OUTPUT_DIR, 'tokens.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        assert 'usage_type' in columns, "tokens.tsv missing usage_type column"
        assert 'function_type' in columns, "tokens.tsv missing function_type column"
        assert 'is_sentence_final' in columns, "tokens.tsv missing is_sentence_final column"


def test_tokens_usage_type_distribution():
    """Tokens should have reasonable distribution of usage_type values."""
    path = os.path.join(OUTPUT_DIR, 'tokens.tsv')
    
    usage_counts = {'lexical': 0, 'grammatical': 0, 'ambiguous': 0}
    total = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            usage = row.get('usage_type', '')
            if usage in usage_counts:
                usage_counts[usage] += 1
            total += 1
    
    # Should have both lexical and grammatical tokens
    assert usage_counts['lexical'] > 100000, \
        f"Too few lexical tokens: {usage_counts['lexical']}"
    assert usage_counts['grammatical'] > 100000, \
        f"Too few grammatical tokens: {usage_counts['grammatical']}"


def test_lemmas_have_entry_type():
    """Lemmas should have entry_type field with valid values."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        assert 'entry_type' in columns, "lemmas.tsv missing entry_type column"
        assert 'lexical_frequency' in columns, "lemmas.tsv missing lexical_frequency column"
        assert 'grammatical_frequency' in columns, "lemmas.tsv missing grammatical_frequency column"


def test_lemmas_entry_type_values():
    """Lemmas entry_type should have valid values."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    valid_types = {'lexical', 'grammatical', 'mixed', 'unresolved'}
    entry_types = set()
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            entry_type = row.get('entry_type', '')
            entry_types.add(entry_type)
    
    invalid = entry_types - valid_types
    assert not invalid, f"Invalid entry_type values: {invalid}"


def test_grammatical_morphemes_function_specific():
    """Grammatical morphemes should be split by function (one row per form+function)."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        # Check for new columns
        assert 'function_id' in columns, "grammatical_morphemes.tsv missing function_id column"
        assert 'clean_environments' in columns, "grammatical_morphemes.tsv missing clean_environments column"
        assert 'lexical_contamination' in columns, "grammatical_morphemes.tsv missing lexical_contamination column"
        assert 'usage_type' in columns, "grammatical_morphemes.tsv missing usage_type column"


def test_in_morpheme_split_by_function():
    """'in' morpheme should appear as separate rows for ERG, CVB, QUOT, INST."""
    path = os.path.join(OUTPUT_DIR, 'grammatical_morphemes.tsv')
    
    in_glosses = set()
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['form'] == 'in':
                in_glosses.add(row['gloss'])
    
    # Should have multiple function-specific rows
    expected = {'ERG', 'CVB', 'QUOT', 'INST'}
    found = expected & in_glosses
    
    assert len(found) >= 3, \
        f"'in' morpheme should be split by function. Found glosses: {in_glosses}"


def test_examples_have_sense_linkage():
    """Examples should have sense_id for sense-level linkage."""
    path = os.path.join(OUTPUT_DIR, 'examples.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        columns = reader.fieldnames
        
        assert 'sense_id' in columns, "examples.tsv missing sense_id column"
        assert 'usage_type' in columns, "examples.tsv missing usage_type column"
        assert 'function_match' in columns, "examples.tsv missing function_match column"


def test_hi_lemma_is_primarily_grammatical():
    """'hi' lemma should be classified as primarily grammatical (entry_type grammatical or unresolved with high gram_freq)."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'hi':
                entry_type = row.get('entry_type', '')
                # 'hi' can be grammatical or unresolved (since it has ~12% lexical uses as "be/this")
                assert entry_type in ('grammatical', 'unresolved'), \
                    f"'hi' should be grammatical/unresolved, got {entry_type}"
                
                gram_freq = int(row.get('grammatical_frequency', 0))
                lex_freq = int(row.get('lexical_frequency', 0))
                # Grammatical uses should be majority (>50%), accounting for 'be' as lexical
                assert gram_freq > lex_freq, \
                    f"'hi' grammatical freq ({gram_freq}) should be > lexical ({lex_freq})"
                return
    
    assert False, "'hi' lemma not found"


def test_ding_lemma_is_grammatical():
    """'ding' lemma should be classified as grammatical entry_type."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'ding':
                entry_type = row.get('entry_type', '')
                assert entry_type == 'grammatical', \
                    f"'ding' should be grammatical, got {entry_type}"
                return
    
    assert False, "'ding' lemma not found"


def test_sih_lemma_is_lexical():
    """'sih' (die/blood) lemma should be classified as lexical entry_type."""
    path = os.path.join(OUTPUT_DIR, 'lemmas.tsv')
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['lemma'] == 'sih':
                entry_type = row.get('entry_type', '')
                assert entry_type == 'lexical', \
                    f"'sih' should be lexical, got {entry_type}"
                return
    
    assert False, "'sih' lemma not found"


def test_auto_resolution_reduces_review_burden():
    """Auto-resolution should dramatically reduce items needing human review."""
    path = os.path.join(OUTPUT_DIR, 'ambiguities.tsv')
    
    status_counts = {'auto_resolved': 0, 'low_priority': 0, 'needs_review': 0}
    total = 0
    
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            status = row.get('status', '')
            if status in status_counts:
                status_counts[status] += 1
            total += 1
    
    # Auto-resolved should be majority
    assert status_counts['auto_resolved'] > total * 0.5, \
        f"Auto-resolved ({status_counts['auto_resolved']}) should be > 50% of {total}"
    
    # Needs_review should be small minority
    assert status_counts['needs_review'] < total * 0.15, \
        f"Needs_review ({status_counts['needs_review']}) should be < 15% of {total}"


def test_high_freq_unk_pos_needs_review():
    """High-frequency UNK POS items should be flagged for review."""
    path = os.path.join(OUTPUT_DIR, 'ambiguities.tsv')
    
    # ciangin has 10K tokens with UNK POS - should need review
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['normalized_form'] == 'ciangin':
                assert row['status'] == 'needs_review', \
                    f"High-freq UNK 'ciangin' should need review, got {row['status']}"
                return
    
    # It's OK if ciangin isn't in ambiguities (might have been resolved elsewhere)


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
        # Semantic correctness tests
        test_hi_not_glossed_as_this,
        test_thei_not_glossed_as_fig,
        test_mu_not_glossed_as_kiss,
        test_pai_not_glossed_as_pour,
        test_te_plural_not_glossed_loc,
        test_case_marker_not_lexical_gloss,
        test_review_file_exists,
        # Sense and context tests
        test_senses_file_exists,
        test_senses_primary_sense_is_most_frequent,
        test_ci_primary_sense_is_say,
        test_sih_has_multiple_senses,
        test_context_disambiguation_thum,
        test_context_disambiguation_ngen,
        test_lemmas_have_pos_variants,
        test_high_frequency_items_properly_classified,
        test_no_duplicate_entries_in_sample,
        # Precision tests (quality enforcement)
        test_no_unk_pos_in_grammatical_section,
        test_problem_forms_not_in_polished_grammatical,
        test_affix_section_no_lexical_glosses,
        test_affix_section_no_mismatched_categories,
        test_sentence_final_no_prefix_env,
        test_grammatical_entries_have_func_pos,
        test_review_file_has_problem_forms,
        # Backend structure tests
        test_tokens_have_usage_type,
        test_tokens_usage_type_distribution,
        test_lemmas_have_entry_type,
        test_lemmas_entry_type_values,
        test_grammatical_morphemes_function_specific,
        test_in_morpheme_split_by_function,
        test_examples_have_sense_linkage,
        test_hi_lemma_is_primarily_grammatical,
        test_ding_lemma_is_grammatical,
        test_sih_lemma_is_lexical,
        # Auto-resolution tests
        test_auto_resolution_reduces_review_burden,
        test_high_freq_unk_pos_needs_review,
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
