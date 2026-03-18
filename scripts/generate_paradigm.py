#!/usr/bin/env python3
"""
Generate textbook-style noun paradigms with corpus attestations.

Usage:
    python generate_paradigm.py gam              # Single noun
    python generate_paradigm.py --all            # Sample nouns (10)
    python generate_paradigm.py --free           # All free noun stems
    python generate_paradigm.py --compounds      # Compound paradigms
    python generate_paradigm.py --proper         # Proper noun paradigms
    python generate_paradigm.py --all-reports    # Generate all three reports
    python generate_paradigm.py --output FILE    # Write to file
"""

import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Optional, Set

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import (
    analyze_word, NOUN_STEMS, NOUN_STEM_TYPES, 
    PROPER_NOUNS, BINARY_COMPOUNDS
)

# Book abbreviations for verse references
BOOK_ABBREVS = {
    '01': 'Gen', '02': 'Exo', '03': 'Lev', '04': 'Num', '05': 'Deu',
    '06': 'Jos', '07': 'Jdg', '08': 'Rut', '09': '1Sa', '10': '2Sa',
    '11': '1Ki', '12': '2Ki', '13': '1Ch', '14': '2Ch', '15': 'Ezr',
    '16': 'Neh', '17': 'Est', '18': 'Job', '19': 'Psa', '20': 'Pro',
    '21': 'Ecc', '22': 'Sol', '23': 'Isa', '24': 'Jer', '25': 'Lam',
    '26': 'Eze', '27': 'Dan', '28': 'Hos', '29': 'Joe', '30': 'Amo',
    '31': 'Oba', '32': 'Jon', '33': 'Mic', '34': 'Nah', '35': 'Hab',
    '36': 'Zep', '37': 'Hag', '38': 'Zec', '39': 'Mal',
    '40': 'Mat', '41': 'Mar', '42': 'Luk', '43': 'Joh', '44': 'Act',
    '45': 'Rom', '46': '1Co', '47': '2Co', '48': 'Gal', '49': 'Eph',
    '50': 'Phi', '51': 'Col', '52': '1Th', '53': '2Th', '54': '1Ti',
    '55': '2Ti', '56': 'Tit', '57': 'Phm', '58': 'Heb', '59': 'Jam',
    '60': '1Pe', '61': '2Pe', '62': '1Jo', '63': '2Jo', '64': '3Jo',
    '65': 'Jud', '66': 'Rev',
}

def format_verse_ref(verse_id: str) -> str:
    """Convert BBCCCVVV format to readable form (e.g., 01002005 -> Gen 2:5)."""
    if len(verse_id) != 8:
        return verse_id
    book = verse_id[:2]
    chapter = str(int(verse_id[2:5]))  # Remove leading zeros
    verse = str(int(verse_id[5:8]))
    book_name = BOOK_ABBREVS.get(book, book)
    return f"{book_name} {chapter}:{verse}"


def get_free_stems() -> Dict[str, str]:
    """Return noun stems that occur independently (free stems)."""
    return {stem: NOUN_STEMS[stem] for stem, stype in NOUN_STEM_TYPES.items() 
            if stype == 'free' and stem in NOUN_STEMS}


def get_bound_stems() -> Dict[str, str]:
    """Return noun stems that only occur in compounds (bound stems)."""
    return {stem: NOUN_STEMS[stem] for stem, stype in NOUN_STEM_TYPES.items() 
            if stype == 'bound' and stem in NOUN_STEMS}


def get_compounds_by_stem() -> Dict[str, List[Tuple[str, str, str]]]:
    """
    Return compounds grouped by their constituent stems.
    Each compound appears under ALL its stems.
    Skips entries with None stems (opaque forms like nasem, nasep).
    
    Returns: {stem: [(compound, components_str, gloss), ...]}
    """
    compounds_by_stem = defaultdict(list)
    
    for compound, (stem1, stem2, gloss) in BINARY_COMPOUNDS.items():
        # Skip opaque entries with None stems
        if stem1 is None or stem2 is None:
            continue
        entry = (compound, f"{stem1}-{stem2}", gloss)
        compounds_by_stem[stem1].append(entry)
        compounds_by_stem[stem2].append(entry)
    
    return dict(compounds_by_stem)


def get_proper_nouns_attested(corpus_file: str) -> Set[str]:
    """Return proper nouns that are actually attested in the corpus."""
    attested = set()
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            text = parts[1]
            for word in text.split():
                word_clean = word.strip('.,;:!?"')
                # Check both exact and title case
                if word_clean in PROPER_NOUNS or word_clean.title() in PROPER_NOUNS:
                    attested.add(word_clean)
    
    return attested


# Tedim Chin case system (6 cases)
# Based on corpus analysis: GEN (many), ERG (53,915), LOC (25,569), ABL.ERG (4,343), ABL (32)
# Note: -in marks both ERG (on nouns) and INST (on manner expressions)
# -pan = simple ablative "from"; -panin = ablative+ergative (source as agent)
# Genitive marked with apostrophe (glottal stop): pa' = father's
#
# NOTE: -tawh and -tawhin are NOT case suffixes - they are FREE POSTPOSITIONS
# Tedim uses "pa tawh" (with father) as two words, NOT "*patawh"
# See POSTPOSITIONS dict in analyze_morphemes.py
CASE_SUFFIXES = [
    ('', 'ABS', 'Absolutive'),           # Unmarked
    ("'", 'GEN', 'Genitive'),            # Possessor (glottal stop)
    ('in', 'ERG', 'Ergative'),           # Agent/instrument
    ('ah', 'LOC', 'Locative'),           # Location
    ('pan', 'ABL', 'Ablative'),          # Simple source/from
    ('panin', 'ABL.ERG', 'Ablative-Ergative'),  # Source as agent
]

# Number marking
NUMBER_SUFFIXES = [
    ('', '', 'Singular'),
    ('te', 'PL', 'Plural'),
]

# Postpositions that should not count preceding nouns as absolutive
NOMINAL_POSTPOSITIONS = {'pan', 'tawh', 'panin', 'tawhin'}

def find_attestations(corpus_file: str, forms: List[str], 
                      exclude_prepostpositional: bool = False) -> Dict[str, List[Tuple[str, str]]]:
    """
    Find corpus attestations for a list of word forms.
    
    Args:
        corpus_file: Path to corpus file
        forms: List of word forms to search for
        exclude_prepostpositional: If True, exclude bare stems that are followed
            by postpositions (pan, tawh, panin, tawhin) - these are not true absolutives
    
    Returns dict mapping form -> [(verse_id, context), ...]
    """
    attestations = defaultdict(list)
    forms_lower = {f.lower().replace('-', '') for f in forms}
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            verse_id = parts[0]
            text = parts[1]
            words = text.split()
            
            for i, word in enumerate(words):
                # Strip punctuation but PRESERVE apostrophe (genitive marker)
                word_clean = word.strip('.,;:!?"').lower()
                # Remove trailing apostrophe only if followed by punctuation that was stripped
                # Actually, we want to keep trailing apostrophe for genitive
                if word_clean in forms_lower:
                    # Find the canonical form
                    for form in forms:
                        if form.lower().replace('-', '') == word_clean:
                            # Check if this is a bare stem followed by postposition
                            if exclude_prepostpositional and '-' not in form:
                                # Check next word
                                if i + 1 < len(words):
                                    next_word = words[i + 1].strip('.,;:!?"').lower()
                                    if next_word in NOMINAL_POSTPOSITIONS:
                                        # Skip - this is NP + postposition, not absolutive
                                        break
                            
                            if len(attestations[form]) < 5:  # Limit examples
                                attestations[form].append((verse_id, word))
                            break
    
    return attestations


def generate_paradigm_forms(stem: str) -> List[Tuple[str, str, str, str]]:
    """
    Generate all paradigm forms for a noun stem.
    
    Returns list of (form, segmentation, gloss, category)
    """
    forms = []
    
    for num_suf, num_gloss, num_name in NUMBER_SUFFIXES:
        for case_suf, case_gloss, case_name in CASE_SUFFIXES:
            # Build form
            if num_suf and case_suf:
                form = f"{stem}-{num_suf}-{case_suf}"
                seg = form
                gloss = f"{stem}-{num_gloss}-{case_gloss}"
            elif num_suf:
                form = f"{stem}-{num_suf}"
                seg = form
                gloss = f"{stem}-{num_gloss}"
            elif case_suf:
                form = f"{stem}-{case_suf}"
                seg = form
                gloss = f"{stem}-{case_gloss}"
            else:
                form = stem
                seg = stem
                gloss = stem
            
            category = f"{num_name} {case_name}".strip()
            forms.append((form, seg, gloss, category))
    
    return forms


def generate_paradigm_markdown(stem: str, stem_gloss: str, 
                                attestations: Dict[str, List],
                                show_all: bool = True) -> str:
    """Generate markdown paradigm table with attestations."""
    
    lines = [f'## {stem} "{stem_gloss}"', '']
    
    # Table header
    lines.append('| Case | Singular | Attested | Plural | Attested |')
    lines.append('|------|----------|----------|--------|----------|')
    
    for case_suf, case_gloss, case_name in CASE_SUFFIXES:
        # Singular form
        if case_suf:
            sg_form = f"{stem}-{case_suf}"
            sg_gloss = f"{stem_gloss}-{case_gloss}"
        else:
            sg_form = stem
            sg_gloss = stem_gloss
        
        # Plural form
        if case_suf:
            pl_form = f"{stem}-te-{case_suf}"
            pl_gloss = f"{stem_gloss}-PL-{case_gloss}"
        else:
            pl_form = f"{stem}-te"
            pl_gloss = f"{stem_gloss}-PL"
        
        # Get attestations
        sg_attest = attestations.get(sg_form, [])
        pl_attest = attestations.get(pl_form, [])
        
        # Format attestation citations (use readable verse refs)
        if sg_attest:
            sg_cite = ', '.join([format_verse_ref(v) for v, _ in sg_attest[:3]])
            if len(sg_attest) > 3:
                sg_cite += f" (+{len(sg_attest)-3})"
        else:
            sg_cite = "—"
        
        if pl_attest:
            pl_cite = ', '.join([format_verse_ref(v) for v, _ in pl_attest[:3]])
            if len(pl_attest) > 3:
                pl_cite += f" (+{len(pl_attest)-3})"
        else:
            pl_cite = "—"
        
        lines.append(f'| {case_name} | {sg_form} | {sg_cite} | {pl_form} | {pl_cite} |')
    
    return '\n'.join(lines)


def generate_full_report(nouns: List[Tuple[str, str]], corpus_file: str) -> str:
    """Generate full paradigm report for multiple nouns."""
    
    lines = [
        '# Tedim Chin Noun Paradigms',
        '',
        '## Overview',
        '',
        'Tedim Chin nouns inflect for:',
        '- **Number**: Singular (unmarked), Plural (*-te*)',
        '- **Case**:',
        '  - Absolutive (unmarked)',
        "  - Genitive (*-'*) — possessor (glottal stop)",
        '  - Ergative (*-in*) — marks agent',
        '  - Locative (*-ah*) — location',
        '  - Ablative (*-pan*) — source/from',
        '  - Ablative-Ergative (*-panin*) — source as agent',
        '  - Comitative (*-tawh*) — accompaniment',
        '  - Comitative-Ergative (*-tawhin*) — instrument as agent',
        '',
        'Suffix order: **STEM-PLURAL-CASE** (e.g., *gam-te-ah* = land-PL-LOC)',
        '',
        'Citations show verse references where forms are attested in the Tedim Chin Bible (30,422 verses, 66 books).',
        '"—" indicates the form is grammatically possible but not attested in the corpus.',
        '',
        '---',
        '',
    ]
    
    for stem, gloss in nouns:
        # Generate all forms for this stem
        paradigm_forms = generate_paradigm_forms(stem)
        forms_list = [f[0] for f in paradigm_forms]
        
        # Find attestations - exclude bare stems followed by postpositions
        attestations = find_attestations(corpus_file, forms_list, exclude_prepostpositional=True)
        
        # Generate markdown
        lines.append(generate_paradigm_markdown(stem, gloss, attestations))
        lines.append('')
        lines.append('---')
        lines.append('')
    
    return '\n'.join(lines)


def analyze_attestation_patterns(nouns: List[Tuple[str, str]], corpus_file: str) -> Dict:
    """
    Analyze case attestation patterns for nouns.
    
    Returns dict with:
    - 'by_case_count': {count: [stems...]} - stems grouped by how many cases attested
    - 'by_pattern': {pattern_str: [stems...]} - stems grouped by exact case pattern
    - 'case_frequencies': {case: count} - how many stems have this case attested
    - 'top_by_cases': [(stem, gloss, count, pattern)] - stems with most cases attested
    """
    results = {
        'by_case_count': defaultdict(list),
        'by_pattern': defaultdict(list),
        'case_frequencies': defaultdict(int),
        'top_by_cases': [],
        'stem_patterns': {},  # stem -> {cases_attested, pattern_str, attestation_counts}
    }
    
    case_abbrevs = ['ABS', 'GEN', 'ERG', 'LOC', 'ABL', 'ABL.ERG']  # 6 cases (no comitative)
    
    for stem, gloss in nouns:
        paradigm_forms = generate_paradigm_forms(stem)
        forms_list = [f[0] for f in paradigm_forms]
        # Exclude bare stems followed by postpositions from absolutive counts
        attestations = find_attestations(corpus_file, forms_list, exclude_prepostpositional=True)
        
        # Track which cases are attested (singular or plural)
        cases_attested = set()
        attestation_counts = {}
        
        for case_suf, case_gloss, case_name in CASE_SUFFIXES:
            sg_form = f"{stem}-{case_suf}" if case_suf else stem
            pl_form = f"{stem}-te-{case_suf}" if case_suf else f"{stem}-te"
            
            sg_count = len(attestations.get(sg_form, []))
            pl_count = len(attestations.get(pl_form, []))
            total = sg_count + pl_count
            
            if total > 0:
                cases_attested.add(case_gloss)
                attestation_counts[case_gloss] = total
                results['case_frequencies'][case_gloss] += 1
        
        # Create pattern string (sorted by standard case order)
        pattern = '+'.join(c for c in case_abbrevs if c in cases_attested) or 'NONE'
        num_cases = len(cases_attested)
        
        results['by_case_count'][num_cases].append((stem, gloss))
        results['by_pattern'][pattern].append((stem, gloss))
        results['stem_patterns'][stem] = {
            'gloss': gloss,
            'cases_attested': cases_attested,
            'pattern': pattern,
            'num_cases': num_cases,
            'counts': attestation_counts,
        }
        results['top_by_cases'].append((stem, gloss, num_cases, pattern))
    
    # Sort top by cases (descending)
    results['top_by_cases'].sort(key=lambda x: (-x[2], x[0].lower()))
    
    return results


def generate_index_section(analysis: Dict, report_type: str = 'free') -> str:
    """Generate index/summary section for report header."""
    lines = ['## Index and Summary', '']
    
    # 1. Top nouns by case coverage
    lines.append('### Nouns with Most Case Forms Attested')
    lines.append('')
    lines.append('| Rank | Stem | Gloss | Cases | Pattern |')
    lines.append('|------|------|-------|-------|---------|')
    
    for i, (stem, gloss, count, pattern) in enumerate(analysis['top_by_cases'][:30], 1):
        lines.append(f'| {i} | [{stem}](#{stem.lower()}-{gloss.replace(".", "").replace(" ", "-").lower()}) | {gloss} | {count}/6 | {pattern} |')
    
    lines.append('')
    
    # 2. Distribution by case count
    lines.append('### Distribution by Number of Cases Attested')
    lines.append('')
    lines.append('| Cases Attested | Count | Percentage |')
    lines.append('|----------------|-------|------------|')
    
    total = sum(len(stems) for stems in analysis['by_case_count'].values())
    for count in sorted(analysis['by_case_count'].keys(), reverse=True):
        stems = analysis['by_case_count'][count]
        pct = 100 * len(stems) / total if total > 0 else 0
        lines.append(f'| {count}/6 cases | {len(stems)} | {pct:.1f}% |')
    
    lines.append('')
    
    # 3. Case frequency (how many stems have each case)
    lines.append('### Case Attestation Frequency')
    lines.append('')
    lines.append('How many noun stems have each case attested:')
    lines.append('')
    lines.append('| Case | Stems with Attestation | Percentage |')
    lines.append('|------|------------------------|------------|')
    
    case_order = ['ABS', 'GEN', 'ERG', 'LOC', 'ABL', 'ABL.ERG']
    for case in case_order:
        count = analysis['case_frequencies'].get(case, 0)
        pct = 100 * count / total if total > 0 else 0
        lines.append(f'| {case} | {count} | {pct:.1f}% |')
    
    lines.append('')
    
    # 4. Most common patterns
    lines.append('### Most Common Case Patterns')
    lines.append('')
    lines.append('Nouns grouped by which cases they are attested in:')
    lines.append('')
    lines.append('| Pattern | Count | Example Stems |')
    lines.append('|---------|-------|---------------|')
    
    patterns_sorted = sorted(analysis['by_pattern'].items(), key=lambda x: -len(x[1]))
    for pattern, stems in patterns_sorted[:20]:
        examples = ', '.join(f'{s}' for s, g in stems[:5])
        if len(stems) > 5:
            examples += f' (+{len(stems)-5} more)'
        lines.append(f'| {pattern} | {len(stems)} | {examples} |')
    
    lines.append('')
    lines.append('---')
    lines.append('')
    
    return '\n'.join(lines)


def generate_free_noun_report(corpus_file: str) -> str:
    """Generate paradigm report for free (independently attested) noun stems."""
    free_stems = get_free_stems()
    nouns = sorted(free_stems.items(), key=lambda x: x[0].lower())
    
    # First pass: analyze attestation patterns for index
    print("  Analyzing attestation patterns...", file=sys.stderr)
    analysis = analyze_attestation_patterns(nouns, corpus_file)
    
    lines = [
        '# Tedim Chin Noun Paradigms (Free Stems)',
        '',
        '## Overview',
        '',
        'Free stems are nouns that can occur independently in the corpus.',
        f'Total: {len(nouns)} free noun stems',
        '',
        'Tedim Chin nouns inflect for:',
        '- **Number**: Singular (unmarked), Plural (*-te*)',
        '- **Case** (6 cases):',
        '  - Absolutive (unmarked)',
        "  - Genitive (*-'*) — possessor (glottal stop)",
        '  - Ergative (*-in*) — marks agent',
        '  - Locative (*-ah*) — location',
        '  - Ablative (*-pan*) — source/from',
        '  - Ablative-Ergative (*-panin*) — source as agent',
        '',
        '**Note on comitative:** The comitative marker *tawh* ("with") is a free postposition,',
        'not a case suffix. Tedim uses "pa tawh" (with father) as two words, not "*patawh".',
        '',
        'Suffix order: **STEM-PLURAL-CASE** (e.g., *gam-te-ah* = land-PL-LOC)',
        '',
        'Citations show verse references where forms are attested in the Tedim Chin Bible.',
        '"—" indicates the form is grammatically possible but not attested in the corpus.',
        '',
        '---',
        '',
    ]
    
    # Add index section
    lines.append(generate_index_section(analysis, 'free'))
    lines.append('## Paradigms')
    lines.append('')
    
    # Use pre-computed attestations from analysis
    for stem, gloss in nouns:
        stem_info = analysis['stem_patterns'].get(stem)
        paradigm_forms = generate_paradigm_forms(stem)
        forms_list = [f[0] for f in paradigm_forms]
        # Exclude bare stems followed by postpositions
        attestations = find_attestations(corpus_file, forms_list, exclude_prepostpositional=True)
        lines.append(generate_paradigm_markdown(stem, gloss, attestations))
        lines.append('')
        lines.append('---')
        lines.append('')
    
    return '\n'.join(lines)


def generate_compound_report(corpus_file: str) -> str:
    """Generate paradigm report for compounds, grouped by constituent stems."""
    compounds_by_stem = get_compounds_by_stem()
    bound_stems = get_bound_stems()
    
    # Build list of all compounds for analysis
    all_compounds = []
    for compound, (stem1, stem2, gloss) in BINARY_COMPOUNDS.items():
        if stem1 is not None and stem2 is not None:
            all_compounds.append((compound, gloss))
    
    # Analyze attestation patterns
    print("  Analyzing compound attestation patterns...", file=sys.stderr)
    analysis = analyze_attestation_patterns(all_compounds, corpus_file)
    
    lines = [
        '# Tedim Chin Compound Paradigms',
        '',
        '## Overview',
        '',
        'Compounds are formed from two or more stems. This report groups compounds',
        'by their constituent stems. Each compound appears under ALL its stems.',
        '',
        f'Total: {len(BINARY_COMPOUNDS)} compounds from {len(compounds_by_stem)} unique stems',
        f'Bound stems (only occur in compounds): {len(bound_stems)}',
        '',
        '**Note on attestation:** Some compounds only appear inside larger compounds',
        '(e.g., *gahzu* "sap" only appears in *leenggahzu* "wine"). These show 0/6 cases',
        'because the bare compound is not attested as a standalone word.',
        '',
        'Case marking follows the same pattern as simple nouns (6 cases: ABS, GEN, ERG, LOC, ABL, ABL.ERG).',
        '',
        '**Note on comitative:** The comitative marker *tawh* is a free postposition',
        '(written separately: *mi tawh* "with person"), not a case suffix.',
        '',
        '"—" indicates the form is grammatically possible but not attested.',
        '',
        '---',
        '',
    ]
    
    # Add index section
    lines.append(generate_index_section(analysis, 'compounds'))
    lines.append('## Paradigms by Stem')
    lines.append('')
    
    # Process stems alphabetically
    for stem in sorted(compounds_by_stem.keys(), key=str.lower):
        compounds = compounds_by_stem[stem]
        stem_gloss = NOUN_STEMS.get(stem, '?')
        stem_type = NOUN_STEM_TYPES.get(stem, 'unknown')
        
        lines.append(f'## Compounds with "{stem}" ({stem_gloss})')
        lines.append('')
        if stem_type == 'bound':
            lines.append('*This is a bound stem (only occurs in compounds)*')
        else:
            lines.append('*This stem also occurs independently*')
        lines.append('')
        
        for compound, structure, gloss in sorted(compounds):
            # Generate paradigm for this compound
            paradigm_forms = generate_paradigm_forms(compound)
            forms_list = [f[0] for f in paradigm_forms]
            # Exclude bare compounds followed by postpositions
            attestations = find_attestations(corpus_file, forms_list, exclude_prepostpositional=True)
            
            lines.append(f'### {compound} "{gloss}" ({structure})')
            lines.append('')
            lines.append(generate_paradigm_table(compound, gloss, attestations))
            lines.append('')
        
        lines.append('---')
        lines.append('')
    
    return '\n'.join(lines)


def generate_paradigm_table(stem: str, stem_gloss: str, attestations: Dict[str, List]) -> str:
    """Generate just the paradigm table (no heading)."""
    table_lines = []
    table_lines.append('| Case | Singular | Attested | Plural | Attested |')
    table_lines.append('|------|----------|----------|--------|----------|')
    
    for case_suf, case_gloss, case_name in CASE_SUFFIXES:
        if case_suf:
            sg_form = f"{stem}-{case_suf}"
        else:
            sg_form = stem
        
        if case_suf:
            pl_form = f"{stem}-te-{case_suf}"
        else:
            pl_form = f"{stem}-te"
        
        sg_attest = attestations.get(sg_form, [])
        pl_attest = attestations.get(pl_form, [])
        
        if sg_attest:
            sg_cite = ', '.join([format_verse_ref(v) for v, _ in sg_attest[:3]])
            if len(sg_attest) > 3:
                sg_cite += f" (+{len(sg_attest)-3})"
        else:
            sg_cite = "—"
        
        if pl_attest:
            pl_cite = ', '.join([format_verse_ref(v) for v, _ in pl_attest[:3]])
            if len(pl_attest) > 3:
                pl_cite += f" (+{len(pl_attest)-3})"
        else:
            pl_cite = "—"
        
        table_lines.append(f'| {case_name} | {sg_form} | {sg_cite} | {pl_form} | {pl_cite} |')
    
    return '\n'.join(table_lines)


def analyze_proper_noun_patterns(names: List[str], corpus_file: str) -> Dict:
    """Analyze case attestation patterns for proper nouns (no plural forms)."""
    results = {
        'by_case_count': defaultdict(list),
        'by_pattern': defaultdict(list),
        'case_frequencies': defaultdict(int),
        'top_by_cases': [],
        'stem_patterns': {},
    }
    
    case_abbrevs = ['ABS', 'GEN', 'ERG', 'LOC', 'ABL', 'ABL.ERG']  # 6 cases (no comitative)
    
    for name in names:
        forms = [name]
        for case_suf, case_gloss, case_name in CASE_SUFFIXES:
            if case_suf:
                forms.append(f"{name}{case_suf}")
        
        # Exclude bare proper nouns followed by postpositions
        attestations = find_attestations(corpus_file, forms, exclude_prepostpositional=True)
        
        cases_attested = set()
        attestation_counts = {}
        
        for case_suf, case_gloss, case_name in CASE_SUFFIXES:
            form = f"{name}{case_suf}" if case_suf else name
            count = len(attestations.get(form, []))
            if count > 0:
                cases_attested.add(case_gloss)
                attestation_counts[case_gloss] = count
                results['case_frequencies'][case_gloss] += 1
        
        pattern = '+'.join(c for c in case_abbrevs if c in cases_attested) or 'NONE'
        num_cases = len(cases_attested)
        
        results['by_case_count'][num_cases].append((name, name))
        results['by_pattern'][pattern].append((name, name))
        results['stem_patterns'][name] = {
            'gloss': name,
            'cases_attested': cases_attested,
            'pattern': pattern,
            'num_cases': num_cases,
            'counts': attestation_counts,
        }
        results['top_by_cases'].append((name, name, num_cases, pattern))
    
    results['top_by_cases'].sort(key=lambda x: (-x[2], x[0].lower()))
    
    return results


def generate_proper_noun_report(corpus_file: str) -> str:
    """Generate paradigm report for proper nouns (biblical names)."""
    # Get attested proper nouns
    attested = get_proper_nouns_attested(corpus_file)
    attested_list = sorted(attested, key=str.lower)
    
    # Analyze patterns
    print("  Analyzing proper noun attestation patterns...", file=sys.stderr)
    analysis = analyze_proper_noun_patterns(attested_list, corpus_file)
    
    lines = [
        '# Tedim Chin Proper Noun Paradigms',
        '',
        '## Overview',
        '',
        'Proper nouns (biblical names) inflect for case like common nouns (6 cases).',
        f'Total proper nouns in system: {len(PROPER_NOUNS)}',
        f'Attested in corpus: {len(attested)}',
        '',
        'This report shows paradigms for proper nouns actually found in the Tedim Chin Bible.',
        'Proper nouns do not typically take plural marking.',
        '',
        '**Note on comitative:** The comitative marker *tawh* is a free postposition,',
        'not a case suffix. Tedim uses "David tawh" (with David) as two words.',
        '',
        '---',
        '',
    ]
    
    # Add index section
    lines.append(generate_index_section(analysis, 'proper'))
    lines.append('## Paradigms')
    lines.append('')
    
    # Generate paradigms for attested proper nouns (sorted)
    for name in attested_list:
        # Generate forms (no plural for proper nouns)
        forms = [name]
        for case_suf, case_gloss, case_name in CASE_SUFFIXES:
            if case_suf:
                forms.append(f"{name}{case_suf}")  # No hyphen for proper nouns
        
        # Exclude bare proper nouns followed by postpositions
        attestations = find_attestations(corpus_file, forms, exclude_prepostpositional=True)
        
        # Only include if we found any attestations
        if any(attestations.values()):
            lines.append(f'## {name}')
            lines.append('')
            lines.append('| Case | Form | Attested |')
            lines.append('|------|------|----------|')
            
            for case_suf, case_gloss, case_name in CASE_SUFFIXES:
                if case_suf:
                    form = f"{name}{case_suf}"
                else:
                    form = name
                
                attest = attestations.get(form, [])
                if attest:
                    cite = ', '.join([format_verse_ref(v) for v, _ in attest[:3]])
                    if len(attest) > 3:
                        cite += f" (+{len(attest)-3})"
                else:
                    cite = "—"
                
                lines.append(f'| {case_name} | {form} | {cite} |')
            
            lines.append('')
            lines.append('---')
            lines.append('')
    
    return '\n'.join(lines)


def main():
    corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    output_dir = Path(__file__).parent.parent / 'docs' / 'paradigms'
    output_file = None
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage: python generate_paradigm.py <noun> [<gloss>]")
        print("       python generate_paradigm.py --all         # Sample nouns (10)")
        print("       python generate_paradigm.py --full        # All noun stems")
        print("       python generate_paradigm.py --free        # Free noun stems only")
        print("       python generate_paradigm.py --compounds   # Compound paradigms")
        print("       python generate_paradigm.py --proper      # Proper noun paradigms")
        print("       python generate_paradigm.py --all-reports # Generate all three reports")
        print("       python generate_paradigm.py --output FILE")
        sys.exit(1)
    
    args = sys.argv[1:]
    
    # Check for --output flag
    if '--output' in args:
        idx = args.index('--output')
        output_file = args[idx + 1]
        args = args[:idx] + args[idx+2:]
    
    # Handle different report types
    if '--all-reports' in args:
        # Generate all three reports
        print("Generating free noun report...", file=sys.stderr)
        free_report = generate_free_noun_report(corpus_file)
        with open(output_dir / 'nouns_free.md', 'w', encoding='utf-8') as f:
            f.write(free_report)
        print(f"  Written to {output_dir / 'nouns_free.md'}", file=sys.stderr)
        
        print("Generating compound report...", file=sys.stderr)
        compound_report = generate_compound_report(corpus_file)
        with open(output_dir / 'nouns_compounds.md', 'w', encoding='utf-8') as f:
            f.write(compound_report)
        print(f"  Written to {output_dir / 'nouns_compounds.md'}", file=sys.stderr)
        
        print("Generating proper noun report...", file=sys.stderr)
        proper_report = generate_proper_noun_report(corpus_file)
        with open(output_dir / 'nouns_proper.md', 'w', encoding='utf-8') as f:
            f.write(proper_report)
        print(f"  Written to {output_dir / 'nouns_proper.md'}", file=sys.stderr)
        
        print("Done!", file=sys.stderr)
        return
    
    if '--free' in args:
        print("Generating free noun report...", file=sys.stderr)
        report = generate_free_noun_report(corpus_file)
        out = output_file or str(output_dir / 'nouns_free.md')
    elif '--compounds' in args:
        print("Generating compound report...", file=sys.stderr)
        report = generate_compound_report(corpus_file)
        out = output_file or str(output_dir / 'nouns_compounds.md')
    elif '--proper' in args:
        print("Generating proper noun report...", file=sys.stderr)
        report = generate_proper_noun_report(corpus_file)
        out = output_file or str(output_dir / 'nouns_proper.md')
    elif '--full' in args or (args and args[0] == '--full'):
        # Generate for ALL noun stems from the analyzer
        nouns = [(stem, gloss) for stem, gloss in NOUN_STEMS.items()]
        nouns.sort(key=lambda x: x[0].lower())
        print(f"Generating paradigms for {len(nouns)} noun stems...", file=sys.stderr)
        report = generate_full_report(nouns, corpus_file)
        out = output_file
    elif '--all' in args or (args and args[0] == '--all'):
        # Generate for common nouns (sample)
        nouns = [
            ('gam', 'land'),
            ('khut', 'hand'),
            ('inn', 'house'),
            ('mi', 'person'),
            ('thu', 'word'),
            ('lam', 'way'),
            ('pa', 'father'),
            ('nu', 'mother'),
            ('ta', 'child'),
            ('min', 'name'),
        ]
        report = generate_full_report(nouns, corpus_file)
        out = output_file
    else:
        stem = args[0]
        gloss = args[1] if len(args) > 1 else NOUN_STEMS.get(stem, stem)
        nouns = [(stem, gloss)]
        report = generate_full_report(nouns, corpus_file)
        out = output_file
    
    if out:
        with open(out, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Written to {out}")
    else:
        print(report)


if __name__ == '__main__':
    main()
