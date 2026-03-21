#!/usr/bin/env python3
"""
Generate report of nominal postpositions (pan, tawh, panin, tawhin).

Shows nouns occurring with these postpositions, similar to paradigm reports
but focused on postpositional constructions rather than case suffixes.

Includes both:
- Separate postpositions: "sung pan" (inside from)
- Attached postpositions: "gampan" (land-from)

Usage:
    python generate_postposition_report.py              # Generate full report
    python generate_postposition_report.py --output FILE  # Write to file
"""

import sys
import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import NOUN_STEMS, NOUN_STEM_TYPES, PROPER_NOUNS, RELATOR_NOUNS

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

# Additional glosses for common words not in NOUN_STEMS
EXTRA_GLOSSES = {
    # Pronouns and demonstratives
    'ki': 'REFL',
    'uh': '2/3PL',
    'amah': '3SG.EMPH',
    'amaute': '3PL',
    'kei': '1SG',
    'nang': '2SG',
    'nangma': '2SG.EMPH',
    'note': '2PL',
    'mite': 'people',
    'khempeuh': 'all',
    'khat': 'one',
    'tua': 'that',
    'hih': 'this',
    'an': '3PL.POSS',
    'min': 'name',
    # Common nouns
    'thu': 'word',
    'namsau': 'nation',
    'mei': 'fire',
    'lai': 'time',
    'khua': 'village',
    # gamte removed - should be parsed as gam-te (land-PL)
    'khut': 'hand',
    'mah': 'self',
    'sihna': 'death',
    'mun': 'place',
    'vangliatna': 'power',
    'kham': 'cheek',
    'bek': 'only',
    'beh': 'tribe',
    'suang': 'stone',
    'leitang': 'earth',
    'khuapi': 'city',
    'omna': 'dwelling',
    'siangtho': 'holy',
    'sathau': 'fat',
    'kam': 'mouth',
    'hehna': 'anger',
    'numei': 'woman',
    'khutsung': 'hand.inside',
    'vantung': 'heaven',
    'pasian': 'God',
    'leenggahzu': 'grape.wine',
    'thei': 'fruit',
    'tuipi': 'sea',
    'biakna': 'worship',
    # Proper nouns
    'egypt': 'Egypt',
    'jesuh': 'Jesus',
    'khrih': 'Christ',
    'israel': 'Israel',
    'jerusalem': 'Jerusalem',
    'david': 'David',
    'moses': 'Moses',
}

# Postpositions to track
POSTPOSITIONS = {
    'pan': ('ABL', 'from'),
    'panin': ('ABL.ERG', 'from (as agent)'),
    'tawh': ('COM', 'with'),
    'tawhin': ('COM.ERG', 'with (as instrument)'),
}


def get_gloss(word: str) -> str:
    """Get gloss for a word from multiple sources."""
    word_lower = word.lower()
    # Check in order: EXTRA_GLOSSES, NOUN_STEMS, RELATOR_NOUNS, PROPER_NOUNS
    if word_lower in EXTRA_GLOSSES:
        return EXTRA_GLOSSES[word_lower]
    if word_lower in NOUN_STEMS:
        return NOUN_STEMS[word_lower]
    if word_lower in RELATOR_NOUNS:
        return RELATOR_NOUNS[word_lower]
    if word_lower in PROPER_NOUNS:
        return PROPER_NOUNS[word_lower]
    # Try morphological analysis for compound/derived forms
    from analyze_morphemes import analyze_word
    result = analyze_word(word_lower)
    if result and result[1] and '?' not in result[1]:
        return result[1]  # Use the morphological gloss
    # Return em-dash for truly unknown words
    return '—'


def gloss_context(context: str) -> str:
    """
    Add interlinear glossing to a Tedim context phrase.
    Returns: "word1 word2 word3" → "(gloss1 gloss2 gloss3)"
    
    Uses postposition-aware glossing where pan/panin/tawh/tawhin
    get their grammatical function glosses in this report context.
    """
    from analyze_morphemes import analyze_word
    
    # Postposition-specific overrides for this report context
    POSTP_GLOSSES = {
        # Note: pan/panin/tawh/tawhin now handled correctly by analyzer
        # Only kha needs context-aware override (month when followed by number)
        'kha': 'month',         # Override NEG.PERF when likely 'month'
    }
    
    # Clean context and split into words
    words = context.split()
    glosses = []
    
    for i, word in enumerate(words):
        # Remove punctuation for analysis
        clean = word.strip('.,;:!?"*')
        if not clean:
            continue
        
        clean_lower = clean.lower()
        
        # Check for postposition overrides
        if clean_lower in POSTP_GLOSSES:
            glosses.append(POSTP_GLOSSES[clean_lower])
            continue
        
        # Check for 'kha' as month (when followed by number or 'khat')
        if clean_lower == 'kha':
            # Look ahead for number context
            if i + 1 < len(words):
                next_word = words[i + 1].strip('.,;:!?"*').lower()
                if next_word in ('khat', 'nih', 'thum', 'li', 'nga', 'guk', 'sagih', 'giat', 'kua', 'sawm'):
                    glosses.append('month')
                    continue
        
        result = analyze_word(clean_lower)
        if result and result[1] and '?' not in result[1]:
            glosses.append(result[1])
        else:
            # Unknown word - use the word itself in brackets
            glosses.append(f'[{clean}]')
    
    if glosses:
        return f"({' '.join(glosses)})"
    return ''


def categorize_word(word: str) -> str:
    """
    Categorize a word into grammatical type.
    Returns: 'grammatical', 'proper', 'common', or 'unknown'
    """
    word_lower = word.lower()
    
    # Grammatical items (pronouns, demonstratives, particles, relators)
    grammatical_markers = {
        'ki', 'uh', 'un', 'amah', 'amaute', 'kei', 'nang', 'nangma', 'note',
        'khempeuh', 'khat', 'tua', 'tuate', 'hih', 'an', 'eite', 'kote', 'dangte',
        'ding', 'nading', 'lo', 'bek', 'mah', 'mahmah',
    }
    if word_lower in grammatical_markers:
        return 'grammatical'
    if word_lower in RELATOR_NOUNS:
        return 'grammatical'
    
    # Proper nouns
    if word_lower in PROPER_NOUNS:
        return 'proper'
    # Check for capitalized biblical names
    proper_markers = ['egypt', 'israel', 'jerusalem', 'jesuh', 'khrih', 'moses', 
                      'david', 'faro', 'abraham', 'jacob', 'esau', 'joseph',
                      'judah', 'levite', 'babylon', 'assyria', 'sodom', 'gomorrah']
    if word_lower in proper_markers:
        return 'proper'
    
    # Common nouns (everything else that's in our dictionaries)
    if word_lower in NOUN_STEMS:
        return 'common'
    if word_lower in EXTRA_GLOSSES:
        # Check if it's a noun gloss vs grammatical
        gloss = EXTRA_GLOSSES[word_lower]
        if any(x in gloss for x in ['SG', 'PL', 'POSS', 'REFL', 'RECIP', 'IRR', 'NEG', 'PURP']):
            return 'grammatical'
        return 'common'
    
    # Try morphological analysis
    from analyze_morphemes import analyze_word
    result = analyze_word(word_lower)
    if result and result[1]:
        gloss = result[1]
        # Nominalizations and compounds are common nouns
        if '-NMLZ' in gloss or '-' in gloss:
            return 'common'
    
    return 'unknown'


def format_verse_ref(verse_id: str) -> str:
    """Convert BBCCCVVV format to readable form (e.g., 01002005 -> Gen 2:5)."""
    if len(verse_id) != 8:
        return verse_id
    book = verse_id[:2]
    chapter = str(int(verse_id[2:5]))
    verse = str(int(verse_id[5:8]))
    book_name = BOOK_ABBREVS.get(book, book)
    return f"{book_name} {chapter}:{verse}"


def load_kjv_translations(aligned_file: str) -> Dict[str, str]:
    """Load KJV translations from verses_aligned.tsv."""
    kjv = {}
    with open(aligned_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                verse_id = parts[0]
                kjv_text = parts[2]
                kjv[verse_id] = kjv_text
    return kjv


# Gospel book codes (Matthew=40, Mark=41, Luke=42, John=43)
GOSPEL_BOOKS = {'40', '41', '42', '43'}


def select_diverse_samples(examples: List[Tuple], n: int = 3, verse_idx: int = 1) -> List[Tuple]:
    """
    Select up to n samples from different books, prioritizing gospels.
    
    Args:
        examples: List of tuples where verse_id is at position verse_idx
        n: Number of samples to select
        verse_idx: Index of verse_id in the tuple (default 1)
        
    Returns:
        List of up to n examples from different books, with gospel priority
    """
    if not examples:
        return []
    
    # Group by book
    by_book = defaultdict(list)
    for ex in examples:
        verse_id = ex[verse_idx] if len(ex) > verse_idx else ex[0]
        book = verse_id[:2] if len(verse_id) >= 2 else '00'
        by_book[book].append(ex)
    
    selected = []
    used_books = set()
    
    # First, try to get one from gospels
    for gospel in GOSPEL_BOOKS:
        if gospel in by_book and len(selected) < n:
            selected.append(by_book[gospel][0])
            used_books.add(gospel)
            break
    
    # Then fill with samples from different books
    for book in sorted(by_book.keys()):
        if book not in used_books and len(selected) < n:
            selected.append(by_book[book][0])
            used_books.add(book)
    
    # If still need more, take from any book not yet fully used
    if len(selected) < n:
        for book, exs in by_book.items():
            for ex in exs[1:]:  # Skip first (already used if this book was picked)
                if len(selected) >= n:
                    break
                if ex not in selected:
                    selected.append(ex)
    
    return selected[:n]


def find_postposition_contexts(corpus_file: str) -> Dict[str, List[Tuple[str, str, str, str, str]]]:
    """
    Find all instances of nouns with postpositions (both separate and attached).
    
    Returns: {postposition: [(noun, verse_id, context, form_type, full_word), ...]}
    where form_type is 'separate' or 'attached'
    """
    results = {postp: [] for postp in POSTPOSITIONS}
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            verse_id = parts[0]
            text = parts[1]
            words = text.split()
            
            for i, word in enumerate(words):
                word_clean = word.strip('.,;:!?"').lower()
                
                # Check for SEPARATE postpositions (e.g., "sung pan")
                if word_clean in POSTPOSITIONS:
                    if i > 0:
                        prev_word = words[i - 1].strip('.,;:!?"')
                        start = max(0, i - 2)
                        end = min(len(words), i + 3)
                        context = ' '.join(words[start:end])
                        results[word_clean].append((prev_word, verse_id, context, 'separate', word_clean))
                
                # Check for ATTACHED postpositions (e.g., "gampan", "gampanin")
                # Must check panin before pan to avoid double-counting
                for postp in ['panin', 'pan', 'tawhin', 'tawh']:
                    if word_clean.endswith(postp) and len(word_clean) > len(postp):
                        stem = word_clean[:-len(postp)]
                        # Avoid matching words that just happen to end in these letters
                        # Require stem to be at least 2 chars
                        if len(stem) >= 2:
                            start = max(0, i - 2)
                            end = min(len(words), i + 3)
                            context = ' '.join(words[start:end])
                            results[postp].append((stem, verse_id, context, 'attached', word_clean))
                            break  # Don't double-count panin as pan
    
    return results


def get_lemma(word: str) -> str:
    """
    Get the lemma (base form) of a word.
    Strips plural -te suffix and returns stem.
    """
    word_lower = word.lower()
    
    # Check if it's a plural form ending in -te
    if word_lower.endswith('te') and len(word_lower) > 3:
        stem = word_lower[:-2]
        # Verify the stem exists in NOUN_STEMS or can be analyzed
        if stem in NOUN_STEMS:
            return stem
        # Check for plurals like 'mite' -> 'mi', 'tate' -> 'ta'
        from analyze_morphemes import analyze_word
        result = analyze_word(word_lower)
        if result and result[1] and '-PL' in result[1]:
            # Extract stem from segmentation
            seg = result[0]
            if '-te' in seg:
                return seg.split('-te')[0].replace('-', '')
    
    return word_lower


def analyze_by_noun(contexts: Dict[str, List]) -> Dict[str, Dict[str, List]]:
    """
    Reorganize contexts by the noun that precedes the postposition.
    Lemmatizes plurals to group them with their singular forms.
    
    Returns: {noun_lemma: {postposition: [(verse_id, context, form_type, full_word, surface_form), ...]}}
    """
    by_noun = defaultdict(lambda: defaultdict(list))
    
    for postp, examples in contexts.items():
        for noun, verse_id, context, form_type, full_word in examples:
            lemma = get_lemma(noun)
            surface_form = noun.lower()
            by_noun[lemma][postp].append((verse_id, context, form_type, full_word, surface_form))
    
    return dict(by_noun)


def get_top_nouns(by_noun: Dict, min_count: int = 3) -> List[Tuple[str, int, Dict]]:
    """
    Get nouns with most postposition attestations.
    
    Returns: [(noun, total_count, {postp: count, ...}), ...]
    """
    results = []
    for noun, postps in by_noun.items():
        total = sum(len(examples) for examples in postps.values())
        if total >= min_count:
            postp_counts = {p: len(examples) for p, examples in postps.items()}
            results.append((noun, total, postp_counts))
    
    return sorted(results, key=lambda x: -x[1])


def generate_report(corpus_file: str, kjv_file: str) -> str:
    """Generate the full postposition report with KJV translations."""
    
    print("Loading KJV translations...", file=sys.stderr)
    kjv = load_kjv_translations(kjv_file)
    
    print("Finding postposition contexts...", file=sys.stderr)
    contexts = find_postposition_contexts(corpus_file)
    
    print("Analyzing by noun...", file=sys.stderr)
    by_noun = analyze_by_noun(contexts)
    top_nouns = get_top_nouns(by_noun, min_count=2)
    
    # Count separate vs attached forms
    sep_count = sum(1 for postp in contexts.values() for ex in postp if ex[3] == 'separate')
    att_count = sum(1 for postp in contexts.values() for ex in postp if ex[3] == 'attached')
    
    lines = [
        '# Tedim Chin Postposition Report',
        '',
        '## Overview',
        '',
        'This report documents nouns occurring with nominal postpositions.',
        'Includes both separate postpositions (*sung pan*) and attached forms (*gampan*).',
        '',
        '**Postpositions covered:**',
        '',
        '| Postposition | Gloss | Meaning | Separate | Attached | Total |',
        '|--------------|-------|---------|----------|----------|-------|',
    ]
    
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        examples = contexts[postp]
        sep = sum(1 for ex in examples if ex[3] == 'separate')
        att = sum(1 for ex in examples if ex[3] == 'attached')
        total_p = len(examples)
        lines.append(f'| {postp} | {gloss} | {meaning} | {sep:,} | {att:,} | {total_p:,} |')
    
    total = sum(len(c) for c in contexts.values())
    lines.append(f'| **Total** | | | {sep_count:,} | {att_count:,} | **{total:,}** |')
    
    lines.extend([
        '',
        '---',
        '',
        '## Summary Statistics',
        '',
        f'- **Total postposition instances**: {total:,}',
        f'- **Separate forms** (e.g., *sung pan*): {sep_count:,}',
        f'- **Attached forms** (e.g., *gampan*): {att_count:,}',
        f'- **Unique preceding words**: {len(by_noun):,}',
        f'- **Words with 2+ instances**: {len(top_nouns):,}',
        '',
    ])
    
    # Top nouns by postposition usage
    lines.extend([
        '## Top Nouns by Postposition Usage',
        '',
        '| Rank | Noun | Total | pan | panin | tawh | tawhin |',
        '|------|------|-------|-----|-------|------|--------|',
    ])
    
    for i, (noun, total_n, postp_counts) in enumerate(top_nouns[:50], 1):
        pan = postp_counts.get('pan', 0)
        panin = postp_counts.get('panin', 0)
        tawh = postp_counts.get('tawh', 0)
        tawhin = postp_counts.get('tawhin', 0)
        lines.append(f'| {i} | [{noun}](#{noun.replace(" ", "-")}) | {total_n} | {pan} | {panin} | {tawh} | {tawhin} |')
    
    lines.extend(['', '---', ''])
    
    # Detailed sections for each postposition with 3 diverse samples
    for postp, (gloss, meaning) in POSTPOSITIONS.items():
        examples = contexts[postp]
        lines.extend([
            f'## {postp.upper()} "{meaning}"',
            '',
            f'**Total occurrences**: {len(examples):,}',
            '',
        ])
        
        # Count by preceding word and collect samples
        word_samples = defaultdict(list)
        for noun, verse_id, context, form_type, full_word in examples:
            word_samples[noun.lower()].append((noun, verse_id, context, form_type, full_word))
        
        word_counts = {w: len(s) for w, s in word_samples.items()}
        top_words = sorted(word_counts.items(), key=lambda x: -x[1])[:30]
        
        lines.extend([
            '### Most frequent preceding words',
            '',
            '| Word | Count | Sample 1 | Sample 2 | Sample 3 |',
            '|------|-------|----------|----------|----------|',
        ])
        
        for word, count in top_words:
            samples = word_samples.get(word, [])
            # Select diverse samples from different books
            diverse = select_diverse_samples(samples, 3, verse_idx=1)
            sample_cols = []
            for j in range(3):
                if j < len(diverse):
                    _, verse_id, context, _, _ = diverse[j]
                    kjv_text = kjv.get(verse_id, '')[:50] + ('...' if len(kjv.get(verse_id, '')) > 50 else '')
                    gloss_str = gloss_context(context)
                    sample_cols.append(f'{format_verse_ref(verse_id)}: *{context}* {gloss_str} — "{kjv_text}"')
                else:
                    sample_cols.append('—')
            lines.append(f'| {word} | {count} | {sample_cols[0]} | {sample_cols[1]} | {sample_cols[2]} |')
        
        lines.extend(['', '---', ''])
    
    # Categorize all top nouns
    categories = {'grammatical': [], 'common': [], 'proper': [], 'unknown': []}
    for noun, total_n, postp_counts in top_nouns[:100]:
        cat = categorize_word(noun)
        categories[cat].append((noun, total_n, postp_counts))
    
    # Helper function to generate entries for a category
    def generate_category_entries(items, category_name):
        cat_lines = []
        if not items:
            return cat_lines
        
        # Calculate category statistics
        total_instances = sum(t for _, t, _ in items)
        pan_total = sum(pc.get('pan', 0) for _, _, pc in items)
        panin_total = sum(pc.get('panin', 0) for _, _, pc in items)
        tawh_total = sum(pc.get('tawh', 0) for _, _, pc in items)
        tawhin_total = sum(pc.get('tawhin', 0) for _, _, pc in items)
        
        # Category header with statistics
        cat_lines.extend([
            f'### {category_name} ({len(items)} items)',
            '',
            f'**Total postposition instances**: {total_instances:,}',
            '',
            '| Postposition | Count | % of category |',
            '|--------------|-------|---------------|',
            f'| pan | {pan_total:,} | {100*pan_total/total_instances:.1f}% |' if total_instances else '| pan | 0 | 0% |',
            f'| panin | {panin_total:,} | {100*panin_total/total_instances:.1f}% |' if total_instances else '| panin | 0 | 0% |',
            f'| tawh | {tawh_total:,} | {100*tawh_total/total_instances:.1f}% |' if total_instances else '| tawh | 0 | 0% |',
            f'| tawhin | {tawhin_total:,} | {100*tawhin_total/total_instances:.1f}% |' if total_instances else '| tawhin | 0 | 0% |',
            '',
        ])
        
        # Observations based on the data
        if total_instances > 0:
            dominant = max([('pan', pan_total), ('panin', panin_total), ('tawh', tawh_total), ('tawhin', tawhin_total)], key=lambda x: x[1])
            cat_lines.append(f'**Observation**: {category_name} most frequently occur with *{dominant[0]}* ({100*dominant[1]/total_instances:.1f}%).')
            if tawh_total > pan_total + panin_total:
                cat_lines.append(f'Comitative (*tawh*) dominates over ablative (*pan/panin*), suggesting these items commonly express accompaniment.')
            elif pan_total + panin_total > tawh_total:
                cat_lines.append(f'Ablative (*pan/panin*) dominates over comitative (*tawh*), suggesting these items commonly express source/origin.')
            cat_lines.append('')
        
        # Individual entries
        for noun, total_n, postp_counts in items:
            gloss = get_gloss(noun)
            
            cat_lines.extend([
                f'#### {noun}',
                f'**Gloss**: {gloss}',
                '',
                '| Postposition | Count | Sample 1 | Sample 2 | Sample 3 |',
                '|--------------|-------|----------|----------|----------|',
            ])
            
            for postp in ['pan', 'panin', 'tawh', 'tawhin']:
                examples_for_postp = by_noun[noun].get(postp, [])
                count = len(examples_for_postp)
                # Handle both old (4-tuple) and new (5-tuple) formats
                examples_tuple = []
                for ex in examples_for_postp:
                    if len(ex) == 5:
                        verse_id, context, form_type, full_word, surface_form = ex
                    else:
                        verse_id, context, form_type, full_word = ex
                    examples_tuple.append((verse_id, context, form_type, full_word))
                diverse = select_diverse_samples(examples_tuple, 3, verse_idx=0)
                sample_cols = []
                for j in range(3):
                    if j < len(diverse):
                        verse_id, context, form_type, full_word = diverse[j]
                        kjv_text = kjv.get(verse_id, '')[:50] + ('...' if len(kjv.get(verse_id, '')) > 50 else '')
                        gloss_str = gloss_context(context)
                        sample_cols.append(f'{format_verse_ref(verse_id)}: *{context}* {gloss_str} — "{kjv_text}"')
                    else:
                        sample_cols.append('—')
                cat_lines.append(f'| {postp} | {count} | {sample_cols[0]} | {sample_cols[1]} | {sample_cols[2]} |')
            
            cat_lines.extend(['', '---', ''])
        
        return cat_lines
    
    # Generate detailed entries section with categories
    lines.extend([
        '## Detailed Entries by Noun',
        '',
        'Entries organized by grammatical category to reveal different postposition patterns.',
        '',
    ])
    
    # Grammatical items first
    lines.append('## Grammatical Items (Pronouns, Demonstratives, Relators)')
    lines.append('')
    lines.append('These are function words: pronouns, demonstratives, quantifiers, and relator nouns.')
    lines.append('Their postposition patterns reveal grammatical constructions.')
    lines.append('')
    lines.extend(generate_category_entries(categories['grammatical'], 'Grammatical Items'))
    
    # Common nouns
    lines.append('## Common Nouns')
    lines.append('')
    lines.append('Lexical nouns including simple stems, compounds, and nominalizations.')
    lines.append('')
    lines.extend(generate_category_entries(categories['common'], 'Common Nouns'))
    
    # Proper nouns
    lines.append('## Proper Nouns')
    lines.append('')
    lines.append('Names of people, places, and other entities.')
    lines.append('')
    lines.extend(generate_category_entries(categories['proper'], 'Proper Nouns'))
    
    # Unknown (if any)
    if categories['unknown']:
        lines.append('## Uncategorized')
        lines.append('')
        lines.append('Words not yet classified (may need dictionary additions).')
        lines.append('')
        lines.extend(generate_category_entries(categories['unknown'], 'Uncategorized'))
    
    return '\n'.join(lines)


def main():
    corpus_file = str(Path(__file__).parent.parent / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt')
    kjv_file = str(Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv')
    
    import argparse
    parser = argparse.ArgumentParser(description='Generate postposition report')
    parser.add_argument('--output', '-o', help='Output file (default: docs/grammar/reports/03-noun-05-postpositions.md)')
    args = parser.parse_args()
    
    report = generate_report(corpus_file, kjv_file)
    
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(__file__).parent.parent / 'docs' / 'paradigms' / '3-noun-05-postpositions.md'
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding='utf-8')
    print(f"Written to {output_path}", file=sys.stderr)


if __name__ == '__main__':
    main()
