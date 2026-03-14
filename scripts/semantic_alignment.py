#!/usr/bin/env python3
"""
Semantic Alignment Validation Tool

Compares Tedim Chin morphological glosses against KJV translations
to identify potential analysis errors.

Usage:
    python3 scripts/semantic_alignment.py --sample 100
    python3 scripts/semantic_alignment.py --verse 01001002
    python3 scripts/semantic_alignment.py --full --output alignment_report.tsv
"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))
from analyze_morphemes import analyze_word

# === CONFIGURATION ===

# Grammatical morphemes to filter (not content words)
GRAMMATICAL = {
    # Case markers
    'loc', 'erg', 'gen', 'dat', 'nom', 'abl', 'ins', 'com',
    # TAM markers
    'pfv', 'ipfv', 'cont', 'perf', 'pst', 'fut', 'prog', 'compl',
    'prosp', 'prosp.erg',  # prospective (ding)
    'purp', 'purp.erg',    # purposive
    # Derivational
    'nmlz', 'caus', 'appl', 'refl', 'recp', 'pass',
    'neg.nom',  # negative nominalizer
    # Plurals/Number
    'pl', 'sg', 'du', 'pl.imp', 'pl.poss',
    # Person/pronouns
    '1sg', '2sg', '3sg', '1pl', '2pl', '3pl', '3→1', '1sg→3',
    '3sg.pro', '3pl.pro', '1sg.pro', '2sg.pro', '2pl.pro', '1pl.pro',
    '3pl.pro.poss', '1pl.incl',
    # Discourse
    'top', 'foc', 'emph', 'q', 'decl', 'imp', 'opt',
    'neg.emph', 'neg.erg',  # negation variants
    'quot',  # quotative
    # Connectives
    'and', 'or', 'but', 'rel', 'conj', 'comp', 'and/or',
    # Copula/existential
    'cop', 'exist', 'be.3sg', 'be.3sg.rel',
    # Aspect/Direction
    'iter', 'away', 'enter', 'exit', 'intens', 'abil',
    # Other grammatical
    'aux', 'det', 'dem', 'poss', 'neg', 'part', 'red',
    # Common functional glosses to filter
    'house', 'on', 'too', 'also', 'that', 'then', 'amen',
    # Adverbs/discourse  
    'therefore', 'because', 'although', 'beside', 'very',
    'this', 'all', 'one', 'like', 'inside', 'now',
    'what/like', 'each', 'only', 'among', 'exp',
    # Unanalyzed Tedim words (proper handling needed)
    'ama',  # 3sg pronoun
}

# Semantic equivalences: Tedim gloss -> KJV word stems
# IMPORTANT: Only add mappings where the Tedim gloss is VERIFIED to mean the KJV concept
SEMANTIC_MAP = {
    # Divine terms
    'pasian': {'god', 'lord', 'gods'},
    'topa': {'lord', 'god'},
    'kha': {'spirit', 'ghost'},
    'khrih': {'christ'},
    'khrist': {'christ'},
    
    # Creation/existence
    'cause.birth': {'create', 'created', 'make', 'made', 'birth', 'bear', 'bore'},
    'be.born': {'create', 'created', 'come', 'born'},
    'birth': {'bear', 'born', 'birth', 'create'},
    'exist': {'be', 'was', 'were', 'is', 'exist'},
    
    # Nature
    'heaven': {'heaven', 'heavens', 'sky', 'firmament'},
    'earth': {'earth', 'land', 'ground', 'world'},
    'leitung': {'earth', 'land', 'world'},  
    'land': {'land', 'earth', 'country', 'ground', 'place'},
    'sky': {'heaven', 'sky', 'firmament'},
    'water': {'water', 'waters', 'sea', 'seas', 'deep'},
    'sea': {'sea', 'seas', 'water', 'waters', 'deep'},
    'light': {'light', 'lights', 'sun'},
    'dark': {'dark', 'darkness', 'night'},
    'fire': {'fire', 'flame'},
    'road': {'way', 'road', 'path'},
    'midst': {'midst', 'among', 'middle'},
    'town': {'city', 'town', 'place'},
    
    # Body/emotion - VERIFIED: lung="feel" is Tedim for heart/emotion center
    'feel': {'heart', 'hearts', 'mind', 'soul'},  # lung -> feel
    'joy': {'joy', 'glad', 'gladness', 'rejoice', 'rejoiced'},  # lungdam -> joy
    'sorrow': {'sorrow', 'grief', 'sad', 'mourn', 'mourning'},  # lungkham -> sorrow
    'heart-pleased': {'peace', 'content', 'pleased'},  # lungnuam -> heart-pleased
    
    # Communication
    'say': {'say', 'said', 'speak', 'spoke', 'tell', 'told', 'call', 'called', 'spake'},
    'say.nom': {'saying', 'word', 'words'},
    'speak': {'say', 'said', 'speak', 'spoke', 'tell', 'told', 'spake'},
    'word': {'word', 'words', 'speak', 'saying', 'thing', 'things', 'matter'},
    'name': {'name', 'named', 'call', 'called'},
    'voice': {'voice', 'cry', 'sound'},
    
    # Perception
    'see': {'see', 'saw', 'seen', 'look', 'looked', 'behold', 'perceive'},
    'hear': {'hear', 'heard', 'listen'},
    'know': {'know', 'knew', 'known', 'understand'},
    'know.i': {'know', 'knew', 'known', 'understand'},
    'know.ii': {'know', 'knew', 'known', 'understand'},
    
    # Quality
    'good': {'good', 'well', 'right', 'righteous'},
    'great': {'great', 'big', 'large', 'mighty'},
    'big': {'great', 'big', 'large', 'mighty'},
    'holy': {'holy', 'sacred', 'sanctify'},
    'old': {'old', 'elder', 'ancient'},
    
    # People - VERIFIED: mi="person/REL", mipa="man", mite="people"
    'man': {'man', 'men', 'person', 'people', 'adam'},
    'person': {'man', 'men', 'person', 'people', 'one'},
    'person/rel': {'man', 'men', 'person', 'people', 'one', 'who', 'which'},  # mi often = REL marker
    'people': {'people', 'man', 'men', 'nation', 'nations'},
    'woman': {'woman', 'women', 'wife', 'wives'},
    'son': {'son', 'sons', 'child', 'children'},
    'child': {'child', 'children', 'son', 'sons'},
    'father': {'father', 'fathers'},
    'mother': {'mother', 'mothers'},
    'brother': {'brother', 'brothers', 'brethren'},
    'king': {'king', 'kings', 'reign', 'royal'},
    'household': {'house', 'household', 'family'},  # innkuan -> household
    
    # Actions
    'come': {'come', 'came', 'coming'},
    'go': {'go', 'went', 'gone', 'going', 'depart'},
    'pai': {'go', 'went', 'gone', 'walk', 'walked'},  # Tedim verb (currently unanalyzed)
    'give': {'give', 'gave', 'given'},
    'take': {'take', 'took', 'taken'},
    'make': {'make', 'made', 'making'},
    'bring': {'bring', 'brought'},
    'arrive': {'come', 'came', 'arrive', 'arrived', 'reach'},
    'die': {'die', 'died', 'dead', 'death'},
    'want': {'desire', 'want', 'seek'},
    
    # Mental/cognitive
    'reason': {'reason', 'cause', 'because', 'why'},
    
    # Direct matches that need explicit mapping for plurals/forms
    'have': {'have', 'had', 'hath', 'having'},
    'time': {'time', 'times', 'season', 'seasons'},
    'face': {'face', 'faces', 'countenance'},
    'sin': {'sin', 'sins', 'sinned', 'transgression', 'iniquity'},
    'day': {'day', 'days'},
    'eye': {'eye', 'eyes'},
    'hand': {'hand', 'hands'},
    'foot': {'foot', 'feet'},
    
    # Life/living
    'live': {'live', 'lived', 'life', 'living', 'alive'},
    'evil': {'evil', 'wicked', 'wickedness'},
    
    # More verbs
    'send': {'send', 'sent'},
    'send.away': {'send', 'sent', 'away'},
    'get': {'get', 'got', 'receive', 'received', 'obtain'},
    'finish': {'finish', 'finished', 'end', 'ended', 'complete'},
    'cut': {'cut', 'cutting'},
    'put': {'put', 'set', 'place', 'placed'},
    'deliver': {'deliver', 'delivered', 'save', 'saved'},
    'see.i': {'see', 'saw', 'seen', 'behold'},
    
    # Additional verb tenses (Round 192c)
    'answer': {'answer', 'answered'},
    'call': {'call', 'called', 'calling'},
    'cast': {'cast', 'casting'},
    'do': {'do', 'did', 'done', 'doing'},
    'eat': {'eat', 'ate', 'eaten', 'eating'},
    'fall': {'fall', 'fell', 'fallen'},
    'fear': {'fear', 'feared', 'afraid'},
    'find': {'find', 'found'},
    'keep': {'keep', 'kept', 'keeping'},
    'kill': {'kill', 'killed', 'slay', 'slew', 'slain'},
    'open': {'open', 'opened', 'opening'},
    'return': {'return', 'returned'},
    'rise': {'rise', 'rose', 'risen'},
    'sit': {'sit', 'sat'},
    'stand': {'stand', 'stood', 'standing'},
    'turn': {'turn', 'turned'},
    'walk': {'walk', 'walked', 'walking'},
    'write': {'write', 'wrote', 'written'},
    
    # Nouns needing plural forms
    'house': {'house', 'houses', 'household'},
    'inn': {'house', 'houses', 'household'},  # Tedim 'inn' = house
    'servant': {'servant', 'servants'},
    'field': {'field', 'fields'},
    'gate': {'gate', 'gates'},
    'offering': {'offering', 'offerings', 'sacrifice', 'sacrifices'},
    'power': {'power', 'powers', 'might', 'strength'},
    'iniquity': {'iniquity', 'iniquities', 'sin', 'sins'},
    'righteousness': {'righteousness', 'righteous', 'just'},
    'flesh': {'flesh', 'body'},
    'mouth': {'mouth', 'lips'},
}

# KJV stopwords (function words to ignore)
KJV_STOPWORDS = {
    # Articles/determiners
    'the', 'a', 'an', 'this', 'that', 'these', 'those',
    # Pronouns
    'i', 'me', 'my', 'mine', 'we', 'us', 'our', 'ours',
    'you', 'your', 'yours', 'ye', 'thee', 'thou', 'thy', 'thine',
    'he', 'him', 'his', 'she', 'her', 'hers', 'it', 'its',
    'they', 'them', 'their', 'theirs', 'who', 'whom', 'whose',
    'which', 'what', 'where', 'when', 'how', 'why',
    # Prepositions
    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from',
    'into', 'onto', 'upon', 'unto', 'over', 'under', 'through',
    'before', 'after', 'between', 'among', 'within', 'without',
    # Conjunctions
    'and', 'or', 'but', 'nor', 'so', 'yet', 'for', 'because',
    'if', 'then', 'than', 'as', 'while', 'when', 'where',
    # Auxiliaries
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'done',
    'will', 'would', 'shall', 'should', 'can', 'could',
    'may', 'might', 'must', 'ought',
    # Archaic
    'hath', 'doth', 'art', 'wast', 'hast', 'shalt', 'wilt',
    'saith', 'sayeth', 'cometh', 'goeth',
    # Discourse markers
    'lo', 'behold', 'thus', 'therefore', 'wherefore', 'yea', 'nay',
    'verily', 'indeed', 'amen', 'selah',
    # Other function words
    'not', 'no', 'all', 'every', 'each', 'any', 'some', 'none',
    'let', 'now', 'even', 'also', 'only', 'just', 'still',
    'very', 'much', 'more', 'most', 'less', 'least',
    'again', 'here', 'there', 'away', 'out', 'off', 'up', 'down',
    # Archaic reference words (Round 192c)
    'thereof', 'therein', 'thereon', 'thereto', 'thereby', 'therefrom',
    'whereof', 'wherein', 'whereon', 'whereto', 'whereby', 'wherefrom',
    'henceforth', 'hitherto', 'thenceforth',
    'whence', 'thence', 'hence',
    'whatsoever', 'whosoever', 'wheresoever', 'whithersoever',
    'likewise', 'nevertheless', 'notwithstanding',
    'forthwith', 'straightway',
    # More particles
    'both', 'neither', 'either', 'same', 'such', 'other', 'another',
}


def extract_tedim_content(verse_text: str) -> dict:
    """
    Extract content glosses from Tedim verse.
    
    Returns dict mapping glosses to source words for debugging.
    """
    content = {}
    for word in verse_text.replace(',', ' ').replace('.', ' ').replace(';', ' ').split():
        if not word.strip():
            continue
        seg, gloss = analyze_word(word)
        
        # Handle compound glosses with dots (e.g., 'cause.birth')
        # Also handle parentheses in glosses like '(heart-count)'
        for g in re.split(r'[-~]', gloss):
            g_clean = g.strip('?').lower()
            # Remove trailing apostrophes and parentheses
            g_clean = g_clean.strip("'()")
            
            # Skip unknowns, grammatical, single chars
            if (g_clean and 
                g_clean != '?' and 
                g_clean not in GRAMMATICAL and
                len(g_clean) > 1 and
                not g_clean.isupper()):  # Skip unanalyzed uppercase words
                content[g_clean] = word
    
    return content


def extract_kjv_content(verse_text: str) -> set:
    """Extract content words from KJV verse."""
    content = set()
    for word in re.findall(r'\b\w+\b', verse_text.lower()):
        if word not in KJV_STOPWORDS and len(word) > 2:
            content.add(word)
    return content


def compute_alignment(tedim_content: dict, kjv_content: set) -> dict:
    """
    Compute semantic alignment between Tedim glosses and KJV words.
    
    Returns dict with alignment statistics.
    """
    tedim_glosses = set(tedim_content.keys())
    
    matched_tedim = set()
    matched_kjv = set()
    mappings = []  # (tedim, kjv, method)
    
    # Check semantic mappings
    for t in tedim_glosses:
        if t in SEMANTIC_MAP:
            for k in kjv_content:
                if k in SEMANTIC_MAP[t]:
                    matched_tedim.add(t)
                    matched_kjv.add(k)
                    mappings.append((t, k, 'semantic'))
    
    # Check direct matches (same word)
    direct = tedim_glosses & kjv_content
    for word in direct:
        if word not in matched_tedim:
            matched_tedim.add(word)
            matched_kjv.add(word)
            mappings.append((word, word, 'direct'))
    
    # Check partial stem matches (e.g., 'create' matches 'created')
    for t in tedim_glosses - matched_tedim:
        for k in kjv_content - matched_kjv:
            if len(t) >= 4 and len(k) >= 4:
                if t.startswith(k[:4]) or k.startswith(t[:4]):
                    matched_tedim.add(t)
                    matched_kjv.add(k)
                    mappings.append((t, k, 'stem'))
    
    unmatched_tedim = tedim_glosses - matched_tedim
    unmatched_kjv = kjv_content - matched_kjv
    
    # Alignment score: proportion of content matched
    total = len(tedim_glosses) + len(kjv_content)
    matched = len(matched_tedim) + len(matched_kjv)
    score = matched / total if total > 0 else 1.0
    
    return {
        'tedim_glosses': tedim_glosses,
        'kjv_content': kjv_content,
        'matched_tedim': matched_tedim,
        'matched_kjv': matched_kjv,
        'unmatched_tedim': unmatched_tedim,
        'unmatched_kjv': unmatched_kjv,
        'mappings': mappings,
        'score': score,
        'tedim_content': tedim_content,  # For debugging - maps gloss to source word
    }


def load_verses() -> dict:
    """Load aligned verses from both corpora."""
    base_path = Path(__file__).parent.parent
    
    # Load Tedim verses
    tedim_file = base_path / 'bibles' / 'extracted' / 'ctd' / 'ctd-x-bible.txt'
    tedim_verses = {}
    with open(tedim_file) as f:
        for line in f:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                tedim_verses[parts[0]] = parts[1]
    
    # Load KJV verses from alignment file
    align_file = base_path / 'data' / 'verses_aligned.tsv'
    kjv_verses = {}
    with open(align_file) as f:
        next(f)  # skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                kjv_verses[parts[0]] = parts[2]
    
    return tedim_verses, kjv_verses


def analyze_verse(verse_id: str, tedim_text: str, kjv_text: str, verbose: bool = False) -> dict:
    """Analyze alignment for a single verse."""
    tedim_content = extract_tedim_content(tedim_text)
    kjv_content = extract_kjv_content(kjv_text)
    alignment = compute_alignment(tedim_content, kjv_content)
    
    alignment['verse_id'] = verse_id
    alignment['tedim_text'] = tedim_text
    alignment['kjv_text'] = kjv_text
    
    if verbose:
        print(f"\n=== {verse_id} ===")
        print(f"Tedim: {tedim_text[:80]}...")
        print(f"KJV: {kjv_text[:80]}...")
        print(f"Score: {alignment['score']:.2%}")
        if alignment['unmatched_tedim']:
            print(f"Unmatched Tedim: {sorted(alignment['unmatched_tedim'])}")
            for g in alignment['unmatched_tedim']:
                print(f"  {g} <- {alignment['tedim_content'].get(g, '?')}")
        if alignment['unmatched_kjv']:
            print(f"Unmatched KJV: {sorted(alignment['unmatched_kjv'])}")
    
    return alignment


def find_problematic_verses(tedim_verses: dict, kjv_verses: dict, 
                            threshold: float = 0.3,
                            sample_size: int = None) -> list:
    """Find verses with low alignment scores."""
    problems = []
    
    verse_ids = list(set(tedim_verses.keys()) & set(kjv_verses.keys()))
    
    if sample_size:
        import random
        random.seed(42)
        verse_ids = random.sample(verse_ids, min(sample_size, len(verse_ids)))
    
    for verse_id in sorted(verse_ids):
        tedim_text = tedim_verses[verse_id]
        kjv_text = kjv_verses[verse_id]
        
        alignment = analyze_verse(verse_id, tedim_text, kjv_text)
        
        if alignment['score'] < threshold:
            problems.append(alignment)
    
    return problems


def aggregate_unmatched(problems: list) -> dict:
    """Aggregate unmatched glosses across problematic verses."""
    tedim_counts = defaultdict(list)  # gloss -> list of (verse_id, source_word)
    kjv_counts = defaultdict(int)     # word -> count
    
    for p in problems:
        for g in p['unmatched_tedim']:
            source_word = p['tedim_content'].get(g, '?')
            tedim_counts[g].append((p['verse_id'], source_word))
        for k in p['unmatched_kjv']:
            kjv_counts[k] += 1
    
    return tedim_counts, kjv_counts


def main():
    parser = argparse.ArgumentParser(description='Semantic alignment validation')
    parser.add_argument('--verse', help='Analyze specific verse (e.g., 01001002)')
    parser.add_argument('--sample', type=int, help='Sample N random verses')
    parser.add_argument('--threshold', type=float, default=0.3, 
                        help='Alignment score threshold (default: 0.3)')
    parser.add_argument('--full', action='store_true', help='Run on full corpus')
    parser.add_argument('--output', help='Output file for report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print("Loading verses...")
    tedim_verses, kjv_verses = load_verses()
    print(f"Loaded {len(tedim_verses)} Tedim verses, {len(kjv_verses)} KJV verses")
    
    if args.verse:
        # Analyze single verse
        if args.verse in tedim_verses and args.verse in kjv_verses:
            analyze_verse(args.verse, tedim_verses[args.verse], 
                         kjv_verses[args.verse], verbose=True)
        else:
            print(f"Verse {args.verse} not found")
    
    elif args.sample or args.full:
        # Find problematic verses
        sample_size = args.sample if args.sample else None
        problems = find_problematic_verses(tedim_verses, kjv_verses,
                                          threshold=args.threshold,
                                          sample_size=sample_size)
        
        print(f"\nFound {len(problems)} verses with alignment < {args.threshold:.0%}")
        
        # Aggregate unmatched glosses
        tedim_counts, kjv_counts = aggregate_unmatched(problems)
        
        print(f"\n=== TOP UNMATCHED TEDIM GLOSSES ===")
        for gloss, occurrences in sorted(tedim_counts.items(), 
                                         key=lambda x: -len(x[1]))[:30]:
            print(f"  {gloss:20} ({len(occurrences):3}x)")
            if args.verbose:
                for verse_id, source in occurrences[:3]:
                    print(f"    {verse_id}: {source}")
        
        print(f"\n=== TOP UNMATCHED KJV WORDS ===")
        for word, count in sorted(kjv_counts.items(), 
                                  key=lambda x: -x[1])[:30]:
            print(f"  {word:20} ({count:3}x)")
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write("verse_id\tscore\tunmatched_tedim\tunmatched_kjv\n")
                for p in sorted(problems, key=lambda x: x['score']):
                    f.write(f"{p['verse_id']}\t{p['score']:.3f}\t")
                    f.write(f"{','.join(sorted(p['unmatched_tedim']))}\t")
                    f.write(f"{','.join(sorted(p['unmatched_kjv']))}\n")
            print(f"\nReport written to {args.output}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
