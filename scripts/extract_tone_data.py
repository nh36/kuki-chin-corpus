#!/usr/bin/env python3
"""
Extract tone data from literature sources for Tedim Chin.

Phase 1: Extract from existing documents (morpheme database, lit reviews)
Phase 2: Extract from Henderson OCR (requires cleanup)
Phase 3: Extract from ZNC grammar (requires OCR or manual entry)

Output: data/tone_dictionary.tsv with columns:
  orthographic, toned, ipa, tone_pattern, gloss, source, confidence
"""

import re
import os
from pathlib import Path
from collections import defaultdict

# Tone diacritic patterns
TONE_HIGH = 'áéíóúɔ́'  # acute accent = high tone (tone 1)
TONE_MID = 'āēīōūɔ̄'   # macron = mid tone (tone 2)  
TONE_LOW = 'àèìòùɔ̀'   # grave accent = low tone (tone 3)

def normalize_to_bible_orth(toned_form):
    """Convert toned/IPA form to Bible orthography."""
    result = toned_form.lower()
    
    # Remove tone diacritics
    for c in TONE_HIGH + TONE_MID + TONE_LOW:
        base = c[0] if len(c) == 1 else c.replace('\u0301', '').replace('\u0304', '').replace('\u0300', '')
        result = result.replace(c, base)
    
    # IPA to orthography
    replacements = [
        ('ʔ', 'h'),      # glottal stop
        ('ŋ', 'ng'),     # velar nasal
        ('ɔ', 'aw'),     # open-o
        ('x', 'kh'),     # voiceless velar fricative
        ('ɁàɁ', 'ah'),   # Henderson notation
        ('Ɂ', 'h'),      # glottal
    ]
    for old, new in replacements:
        result = result.replace(old, new)
    
    # Remove remaining diacritics
    import unicodedata
    result = ''.join(c for c in unicodedata.normalize('NFD', result) 
                     if unicodedata.category(c) != 'Mn')
    
    return result

def extract_tone_pattern(toned_form):
    """Extract tone pattern as sequence of H/M/L."""
    pattern = []
    for char in toned_form:
        if char in TONE_HIGH or '\u0301' in char:  # acute
            pattern.append('H')
        elif char in TONE_MID or '\u0304' in char:  # macron
            pattern.append('M')
        elif char in TONE_LOW or '\u0300' in char:  # grave
            pattern.append('L')
    return ''.join(pattern) if pattern else '?'

def extract_from_morpheme_docs():
    """Extract tone data from docs/grammar/morphemes/*.md"""
    entries = []
    morpheme_dir = Path('docs/grammar/morphemes')
    
    if not morpheme_dir.exists():
        return entries
    
    # Pattern to match toned forms in ZNC notation
    # e.g., -tà, -xín, kík, -ìn
    toned_pattern = re.compile(r'[-]?([a-zɔ][áàāéèēíìīóòōúùūɔ́ɔ̄ɔ̀ŋɁʔx]+)', re.IGNORECASE)
    
    for md_file in morpheme_dir.glob('*.md'):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract morpheme name from filename
        source = md_file.stem
        
        for match in toned_pattern.finditer(content):
            toned = match.group(1)
            orth = normalize_to_bible_orth(toned)
            tone = extract_tone_pattern(toned)
            
            if tone != '?' and len(orth) > 1:
                entries.append({
                    'orthographic': orth,
                    'toned': toned,
                    'ipa': '',  # Will be filled from Henderson
                    'tone_pattern': tone,
                    'gloss': '',  # Context-dependent
                    'source': f'ZNC via {source}',
                    'confidence': 'high'
                })
    
    return entries

def extract_known_verb_tones():
    """
    Extract tone patterns from known verb Form I/II alternations.
    
    Henderson's rules:
    - Tone 1 (rising) or Tone 2 (level) in Form I → Tone 3 (falling) in Form II
    - This is absolutely regular for long syllables
    """
    entries = []
    
    # From Henderson and analyzer's VERB_STEM_PAIRS
    # Format: (form_i, form_ii, gloss, form_i_tone, form_ii_tone)
    known_pairs = [
        # +h alternation
        ('mu', 'muh', 'see', 'H', 'L'),      # tone 1 → tone 3
        ('thei', 'theih', 'know', 'H', 'L'),
        ('nei', 'neih', 'have', 'H', 'L'),
        ('ci', 'cih', 'say', 'H', 'L'),
        ('zui', 'zuih', 'follow', 'H', 'L'),
        ('ngai', 'ngaih', 'think', 'H', 'L'),
        ('ne', 'neh', 'eat', 'H', 'L'),
        ('sia', 'siah', 'decay', 'H', 'L'),
        ('lua', 'luah', 'exceed', 'H', 'L'),
        ('pua', 'puah', 'bet', 'H', 'L'),
        ('gen', 'genh', 'speak', 'M', 'L'),
        ('bawl', 'bawlh', 'make', 'M', 'L'),
        ('om', 'omh', 'exist', 'M', 'L'),
        ('pai', 'paih', 'go', 'H', 'L'),
        ('hi', 'hih', 'be', 'H', 'L'),
        ('tu', 'tuh', 'sit', 'H', 'L'),
        
        # +k alternation
        ('za', 'zak', 'hear', 'H', 'L'),
        ('pia', 'piak', 'give', 'H', 'L'),
        ('ne', 'nek', 'eat', 'H', 'L'),
        ('bia', 'biak', 'worship', 'H', 'L'),
        ('pua', 'puak', 'spill', 'H', 'L'),
        ('tua', 'tuak', 'meet', 'H', 'L'),
        ('kia', 'kiak', 'fear', 'H', 'L'),
        
        # From Henderson irregular verbs
        ('nuam', 'nop', 'want', 'H', 'L'),
        ('nui', 'nuih', 'laugh', 'H', 'L'),
        ('si', 'sih', 'die', 'H', 'L'),
        ('it', 'ih', 'love', 'H', 'L'),
        ('en', 'et', 'look', 'M', 'L'),
        ('khin', 'khit', 'finish', 'M', 'L'),
        ('kou', 'koh', 'cultivate', 'H', 'L'),
        ('zou', 'zoh', 'finish', 'H', 'L'),
        ('thou', 'thoh', 'spring.up', 'H', 'L'),
        
        # Henderson regular verbs pp. 73-76 (Tone 1→3, Tone 2→3)
        # Tone 1 in Form I, long syllables
        ('kuan', 'kuanh', 'go.to.work', 'H', 'L'),
        ('aim', 'aimh', 'jealous', 'H', 'L'),
        ('dai', 'daih', 'cut', 'H', 'L'),
        ('dail', 'dailh', 'protect', 'H', 'L'),
        ('gem', 'gemh', 'tell', 'H', 'L'),
        ('chai', 'chaih', 'burn', 'H', 'L'),
        ('kam', 'kamh', 'jump.over', 'H', 'L'),
        ('mail', 'mailh', 'blunt', 'H', 'L'),
        ('sip', 'siph', 'watch', 'H', 'L'),
        ('vak', 'vakh', 'walk', 'H', 'L'),
        ('zaip', 'zaiph', 'fan', 'H', 'L'),
        ('zaim', 'zaimh', 'fall.down', 'H', 'L'),
        ('cham', 'chamh', 'utter.cries', 'H', 'L'),
        ('kap', 'kaph', 'shoot', 'H', 'L'),
        ('kai', 'kaih', 'bend.head', 'H', 'L'),
        ('kim', 'kimh', 'move', 'H', 'L'),
        ('kum', 'kumh', 'bow', 'H', 'L'),
        ('kuk', 'kukh', 'reverse', 'H', 'L'),
        ('kaim', 'kaimh', 'forbid', 'H', 'L'),
        ('kaik', 'kaikh', 'close', 'H', 'L'),
        ('keim', 'keimh', 'deceive', 'H', 'L'),
        ('sain', 'sainh', 'accelerate', 'H', 'L'),
        ('tai', 'taih', 'scold', 'H', 'L'),
        ('vai', 'vaih', 'beat.down', 'H', 'L'),
        ('zual', 'zualh', 'lie', 'H', 'L'),
        ('lut', 'luth', 'enter', 'H', 'L'),
        ('lai', 'laih', 'wrestle', 'H', 'L'),
        ('lam', 'lamh', 'fear', 'H', 'L'),
        ('muat', 'muath', 'decay', 'H', 'L'),
        ('nai', 'naih', 'near', 'H', 'L'),
        ('neu', 'neuh', 'small', 'H', 'L'),
        ('nuak', 'nuakh', 'sulk', 'H', 'L'),
        ('nak', 'nakh', 'wait', 'H', 'L'),
        ('yai', 'yaih', 'strict', 'H', 'L'),
        ('pai', 'paih', 'pregnant', 'H', 'L'),
        ('saun', 'saunh', 'long', 'H', 'L'),
        ('tau', 'tauh', 'groan', 'H', 'L'),
        ('zam', 'zamh', 'break', 'H', 'L'),
        
        # Tone 2 in Form I, long syllables  
        ('on', 'onh', 'agree', 'M', 'L'),
        ('sain', 'sainh', 'foretell', 'M', 'L'),
        ('bai', 'baih', 'lame', 'M', 'L'),
        ('bual', 'bualh', 'swim', 'M', 'L'),
        ('tam', 'tamh', 'spend.night', 'M', 'L'),
        ('top', 'toph', 'stop', 'M', 'L'),
        ('vak', 'vakh', 'feed', 'M', 'L'),
        ('zam', 'zamh', 'grow', 'M', 'L'),
        ('pan', 'panh', 'speak', 'M', 'L'),
        ('phual', 'phualh', 'scratch', 'M', 'L'),
        ('zaik', 'zaikh', 'spread', 'M', 'L'),
        ('dik', 'dikh', 'inhale', 'M', 'L'),
        ('gai', 'gaih', 'conceive', 'M', 'L'),
        ('ham', 'hamh', 'old', 'M', 'L'),
        ('hup', 'huph', 'attract', 'M', 'L'),
        ('hiam', 'hiamh', 'sharp', 'M', 'L'),
        ('kak', 'kakh', 'dilate', 'M', 'L'),
        ('kai', 'kaih', 'hang', 'M', 'L'),
        ('seip', 'seiph', 'winnow', 'M', 'L'),
        ('lam', 'lamh', 'dance', 'M', 'L'),
        ('luk', 'lukh', 'collapse', 'M', 'L'),
        ('lak', 'lakh', 'expose', 'M', 'L'),
        ('liau', 'liauh', 'pay.fine', 'M', 'L'),
        ('lup', 'luph', 'prepare.beer', 'M', 'L'),
        ('lui', 'luih', 'old', 'M', 'L'),
        ('mam', 'mamh', 'straight', 'M', 'L'),
        ('man', 'manh', 'true', 'M', 'L'),
        ('maui', 'mauih', 'null', 'M', 'L'),
        ('mol', 'molh', 'play', 'M', 'L'),
        ('nak', 'nakh', 'breathe', 'M', 'L'),
        ('nim', 'nimh', 'aim', 'M', 'L'),
        ('tam', 'tamh', 'deprived', 'M', 'L'),
        
        # Short syllables tone 1/2 → tone 3
        ('bal', 'balh', 'tear', 'H', 'L'),
        ('dai', 'daih', 'shallow', 'H', 'L'),
        ('gam', 'gamh', 'dry', 'H', 'L'),
        ('ham', 'hamh', 'coarse', 'H', 'L'),
        ('chai', 'chaih', 'foolish', 'H', 'L'),
        ('heu', 'heuh', 'wither', 'H', 'L'),
        ('mai', 'maih', 'grope', 'H', 'L'),
        ('kam', 'kamh', 'replete', 'H', 'L'),
        ('zin', 'zinh', 'travel', 'H', 'L'),
        ('dei', 'deih', 'separate', 'H', 'L'),
        ('lal', 'lalh', 'migrate', 'H', 'L'),
        ('lam', 'lamh', 'build', 'H', 'L'),
        ('lei', 'leih', 'buy', 'H', 'L'),
        ('man', 'manh', 'finish', 'H', 'L'),
        ('mang', 'mangh', 'lost', 'H', 'L'),
        ('tung', 'tungh', 'arrive', 'H', 'L'),
        ('vang', 'vangh', 'sparse', 'H', 'L'),
        ('om', 'omh', 'present', 'H', 'L'),
        ('gan', 'ganh', 'profuse', 'H', 'L'),
        ('kang', 'kangh', 'dry.up', 'H', 'L'),
        ('pal', 'palh', 'stumble', 'H', 'L'),
        ('pan', 'panh', 'thin', 'H', 'L'),
        ('phou', 'phouh', 'dry', 'H', 'L'),
        ('tam', 'tamh', 'many', 'H', 'L'),
        ('tan', 'tanh', 'cut', 'H', 'L'),
        ('tum', 'tumh', 'beat', 'H', 'L'),
        ('vau', 'vauh', 'strike', 'H', 'L'),
        ('zai', 'zaih', 'wide', 'H', 'L'),
        ('dan', 'danh', 'different', 'H', 'L'),
        
        # Short syllables tone 2 → 3
        ('san', 'sanh', 'red', 'M', 'L'),
        ('sam', 'samh', 'incant', 'M', 'L'),
        ('sai', 'saih', 'charge', 'M', 'L'),
        ('tam', 'tamh', 'level', 'M', 'L'),
        ('tang', 'tangh', 'straight', 'M', 'L'),
        ('vang', 'vangh', 'hole', 'M', 'L'),
        ('veng', 'vengh', 'over', 'M', 'L'),
        ('vom', 'vomh', 'black', 'M', 'L'),
        ('zan', 'zanh', 'stretch', 'M', 'L'),
        ('zang', 'zangh', 'reach.far', 'M', 'L'),
        ('zol', 'zolh', 'greasy', 'M', 'L'),
        ('ban', 'banh', 'slash', 'M', 'L'),
        ('dam', 'damh', 'well', 'M', 'L'),
        ('dau', 'dauh', 'insipid', 'M', 'L'),
        ('dou', 'douh', 'fight', 'M', 'L'),
        ('hai', 'haih', 'greedy', 'M', 'L'),
        ('kan', 'kanh', 'inquire', 'M', 'L'),
        ('keu', 'keuh', 'dry', 'M', 'L'),
        ('kam', 'kamh', 'lay.crosswise', 'M', 'L'),
        ('kal', 'kalh', 'control', 'M', 'L'),
        ('pou', 'pouh', 'grow', 'M', 'L'),
        ('koi', 'koih', 'suckle', 'M', 'L'),
        ('man', 'manh', 'sticky', 'M', 'L'),
        ('mal', 'malh', 'tear', 'M', 'L'),
        ('min', 'minh', 'cooked', 'M', 'L'),
        ('nam', 'namh', 'smelly', 'M', 'L'),
        
        # From Weera 1998 tone paper (checked syllables)
        # Tone 4 (low, short checked) 
        ('kap', 'kaph', 'weep', 'L', 'L'),
        ('nap', 'naph', 'snot', 'L', 'L'),
        ('gip', 'giph', 'lac', 'L', 'L'),
        ('mit', 'mith', 'eye', 'L', 'L'),
        ('that', 'thath', 'kill', 'L', 'L'),
        ('guk', 'gukh', 'six', 'L', 'L'),
        ('vok', 'vokh', 'pig', 'L', 'L'),
        ('thak', 'thakh', 'pungent', 'L', 'L'),
        ('bak', 'bakh', 'full', 'L', 'L'),
        ('hak', 'hakh', 'awake', 'L', 'L'),
        ('lap', 'laph', 'wing', 'L', 'L'),
        ('dat', 'dath', 'appear', 'L', 'L'),
        ('phat', 'phath', 'good', 'L', 'L'),
        ('cik', 'cikh', 'tight', 'L', 'L'),
        
        # Tone 1 (high, long checked)
        ('zap', 'zaph', 'fan', 'H', 'L'),
        ('tep', 'teph', 'suck', 'H', 'L'),
        ('tuap', 'tuaph', 'lungs', 'H', 'L'),
        ('hut', 'huth', 'shave', 'H', 'L'),
        ('met', 'meth', 'eight', 'H', 'L'),
        ('giat', 'giath', 'rib', 'H', 'L'),
        ('nak', 'nakh', 'walk', 'H', 'L'),
        ('vak', 'vakh', 'walk', 'H', 'L'),
        ('liak', 'liakh', 'lick', 'H', 'L'),
        ('kek', 'kekh', 'thunderbolt', 'H', 'L'),
        ('at', 'ath', 'cut', 'H', 'L'),
        ('pat', 'path', 'thin', 'H', 'L'),
        ('mul', 'mulh', 'fur', 'H', 'L'),
        ('nay', 'nayh', 'near', 'H', 'L'),
        ('sin', 'sinh', 'new', 'H', 'L'),
        
        # Tone 2/3 from *-r (Weera Table 3)
        ('ak', 'akh', 'fowl', 'M', 'L'),
        ('dak', 'dakh', 'bell', 'M', 'L'),
        ('pak', 'pakh', 'flower', 'M', 'L'),
        ('phak', 'phakh', 'leprosy', 'M', 'L'),
        ('tak', 'takh', 'pine', 'M', 'L'),
        ('zak', 'zakh', 'spread', 'M', 'L'),
        ('zuak', 'zuakh', 'sell', 'M', 'L'),
        
        # Weera smooth syllables with tone 1 (from *-?)
        ('va', 'vah', 'bird', 'H', 'L'),
        ('ta', 'tah', 'cold', 'H', 'L'),
        ('tui', 'tuih', 'water', 'H', 'L'),
        ('sa', 'sah', 'meat/animal', 'H', 'L'),
        ('si', 'sih', 'die', 'H', 'L'),
        ('pa', 'pah', 'father', 'H', 'L'),
        ('mei', 'meih', 'fire', 'H', 'L'),
        ('lei', 'leih', 'buy', 'H', 'L'),
        ('gu', 'guh', 'nine', 'H', 'L'),
        ('ya', 'yah', 'eight', 'H', 'L'),
        ('vei', 'veih', 'carry', 'H', 'L'),
        ('xa', 'xah', 'bitter', 'H', 'L'),
        ('kha', 'khah', 'bitter', 'H', 'L'),
        ('wi', 'wih', 'dog', 'H', 'L'),
        
        # Henderson irregular verbs (abrupt closure)
        ('nop', 'noph', 'want', 'L', 'L'),
        ('nuih', 'nuih', 'laugh.II', 'L', 'L'),
        ('sih', 'sih', 'die.II', 'L', 'L'),
        ('ih', 'ih', 'love.II', 'L', 'L'),
        ('et', 'eth', 'look.II', 'L', 'L'),
        ('khit', 'khith', 'finish.II', 'L', 'L'),
        ('koh', 'koh', 'cultivate.II', 'L', 'L'),
        ('zoh', 'zoh', 'finish.II', 'L', 'L'),
        ('thoh', 'thoh', 'spring.II', 'L', 'L'),
        
        # Henderson CVc verbs with irregular Form II
        ('phet', 'pheth', 'tremble.II', 'L', 'L'),
        ('sik', 'sikh', 'fight.II', 'L', 'L'),
        ('phat', 'phath', 'good.II', 'L', 'L'),
        ('nak', 'nakh', 'lay.II', 'L', 'L'),
        ('sak', 'sakh', 'sing.II', 'L', 'L'),
        ('det', 'deth', 'appear.II', 'L', 'L'),
        ('bat', 'bath', 'owe.II', 'L', 'L'),
        ('zat', 'zath', 'broad.II', 'L', 'L'),
        ('tek', 'tekh', 'glitter.II', 'L', 'L'),
        ('gok', 'gokh', 'dry.II', 'L', 'L'),
        ('puak', 'puakh', 'carry.II', 'L', 'L'),
        ('biak', 'biakh', 'worship.II', 'L', 'L'),
        ('nek', 'nekh', 'eat.II', 'L', 'L'),
        ('lak', 'lakh', 'take.II', 'L', 'L'),
        ('guk', 'gukh', 'steal.II', 'L', 'L'),
        ('phak', 'phakh', 'overtake.II', 'L', 'L'),
        ('zak', 'zakh', 'hear.II', 'L', 'L'),
        ('hat', 'hath', 'solid.II', 'L', 'L'),
        ('hazat', 'hazath', 'covet.II', 'L', 'L'),
        ('kat', 'kath', 'forked.II', 'L', 'L'),
        ('pat', 'path', 'thin.II', 'L', 'L'),
        ('siat', 'siath', 'spoil.II', 'L', 'L'),
        ('kiat', 'kiath', 'fall.II', 'L', 'L'),
        ('nusiat', 'nusiath', 'leave.II', 'L', 'L'),
        
        # Henderson glottal stop Form II
        ('bah', 'bah', 'feed.II', 'L', 'L'),
        ('suah', 'suah', 'born.II', 'L', 'L'),
        ('hah', 'hah', 'awake.II', 'L', 'L'),
        ('lah', 'lah', 'show.II', 'L', 'L'),
        ('pah', 'pah', 'loose.II', 'L', 'L'),
        ('sah', 'sah', 'hard.II', 'L', 'L'),
        ('kah', 'kah', 'cry.II', 'L', 'L'),
        ('pah', 'pah', 'immerse.II', 'L', 'L'),
        ('sah', 'sah', 'jerk.II', 'L', 'L'),
        ('suh', 'suh', 'snatch.II', 'L', 'L'),
        ('tah', 'tah', 'strike.II', 'L', 'L'),
        ('thah', 'thah', 'kill.II', 'L', 'L'),
    ]
    
    for form_i, form_ii, gloss, tone_i, tone_ii in known_pairs:
        entries.append({
            'orthographic': form_i,
            'toned': form_i,  # Would need diacritics added
            'ipa': '',
            'tone_pattern': tone_i,
            'gloss': f'{gloss}.I',
            'source': 'Henderson 1965',
            'confidence': 'high'
        })
        entries.append({
            'orthographic': form_ii,
            'toned': form_ii,
            'ipa': '',
            'tone_pattern': tone_ii,
            'gloss': f'{gloss}.II',
            'source': 'Henderson 1965',
            'confidence': 'high'
        })
    
    return entries

def extract_grammatical_morpheme_tones():
    """
    Extract tones for grammatical morphemes from ZNC and Henderson.
    These are high-confidence since they're well-documented.
    """
    entries = []
    
    # Format: (orthographic, toned, tone_pattern, gloss, source)
    morphemes = [
        # Case markers (from ZNC)
        ('in', 'ìn', 'L', 'ERG/CVB', 'ZNC 2018'),
        ('ah', 'àɁ', 'L', 'LOC', 'ZNC 2018'),
        ('pan', 'pàn', 'L', 'ABL', 'ZNC 2018'),
        ('tawh', 'tɔ̀Ɂ', 'L', 'COM', 'ZNC 2018'),
        
        # Aspect markers
        ('ta', 'tà', 'L', 'PFV', 'ZNC 2018'),
        ('zo', 'zò', 'L', 'COMPL', 'ZNC 2018'),
        ('khin', 'xín', 'H', 'SEQ', 'ZNC 2018'),
        ('kik', 'kík', 'H', 'ITER', 'ZNC 2018'),
        ('nawn', 'nàwn', 'L', 'CONT', 'ZNC 2018'),
        
        # Modal markers
        ('ding', 'dìng', 'L', 'IRR', 'ZNC 2018'),
        ('thei', 'thèi', 'L', 'ABIL', 'ZNC 2018'),
        ('nuam', 'nuàm', 'L', 'DESID', 'ZNC 2018'),
        
        # Derivational
        ('sak', 'sàk', 'L', 'CAUS', 'ZNC 2018'),
        ('pih', 'pìh', 'L', 'APPL', 'ZNC 2018'),
        
        # Pronominal prefixes (from Henderson)
        ('ka', 'kà', 'L', '1SG', 'Henderson 1965'),
        ('na', 'nà', 'L', '2SG', 'Henderson 1965'),
        ('a', 'à', 'L', '3SG', 'Henderson 1965'),
        ('i', 'ì', 'L', '1PL.INCL', 'Henderson 1965'),
        ('kan', 'kàn', 'L', '1PL.EXCL', 'Henderson 1965'),
        ('nan', 'nàn', 'L', '2PL', 'Henderson 1965'),
        ('an', 'àn', 'L', '3PL', 'Henderson 1965'),
        
        # Sentence-final particles
        ('hi', 'hì', 'L', 'DECL', 'Henderson 1965'),
        ('e', 'è', 'L', 'INCONCL', 'Henderson 1965'),
        ('hen', 'hèn', 'L', 'JUSS', 'Henderson 1965'),
        ('maw', 'màw', 'L', 'Q', 'Henderson 1965'),
        
        # Common words with known tones
        ('pa', 'pà', 'L', 'father/male', 'Henderson 1965'),
        ('nu', 'nù', 'L', 'mother/female', 'Henderson 1965'),
        ('nau', 'nàu', 'L', 'child', 'Henderson 1965'),
        ('inn', 'ín', 'H', 'house', 'Henderson 1965'),
        ('gam', 'gàm', 'L', 'land', 'Henderson 1965'),
        ('thu', 'thù', 'L', 'word', 'Henderson 1965'),
        ('ni', 'nì', 'L', 'day/sun', 'Henderson 1965'),
        ('khua', 'khùa', 'L', 'village', 'Henderson 1965'),
        ('mi', 'mì', 'L', 'person', 'Henderson 1965'),
        ('mun', 'mùn', 'L', 'place', 'Henderson 1965'),
        
        # High-frequency words in Bible (from corpus analysis)
        ('uh', 'ùh', 'L', 'PL', 'ZNC 2018'),
        ('le', 'lè', 'L', 'and', 'ZNC 2018'),
        ('ciang', 'ciàng', 'L', 'when/if', 'ZNC 2018'),
        ('bang', 'bàng', 'L', 'like/what', 'ZNC 2018'),
        ('lo', 'lò', 'L', 'NEG', 'Henderson 1965'),
        ('kei', 'kèi', 'L', 'NEG.EMPH', 'Henderson 1965'),
        ('sung', 'sùng', 'L', 'inside', 'ZNC 2018'),
        ('khat', 'khàt', 'L', 'one', 'ZNC 2018'),
        ('amah', 'àmàh', 'LL', '3SG.EMPH', 'Henderson 1965'),
        ('amaute', 'àmàutè', 'LLL', '3PL.EMPH', 'Henderson 1965'),
        ('hang', 'hàng', 'L', 'because', 'ZNC 2018'),
        ('zong', 'zòng', 'L', 'also', 'ZNC 2018'),
        ('un', 'ùn', 'L', 'IMP.PL', 'Henderson 1965'),
        ('hiam', 'hiàm', 'L', 'Q.ALT', 'Henderson 1965'),
        ('pen', 'pèn', 'L', 'TOP', 'ZNC 2018'),
        ('kiang', 'kiàng', 'L', 'near', 'ZNC 2018'),
        ('man', 'màn', 'L', 'reason', 'ZNC 2018'),
        ('ama', 'àmà', 'LL', '3SG.POSS', 'Henderson 1965'),
        ('note', 'nòtè', 'LL', '2PL.EMPH', 'Henderson 1965'),
        ('lai', 'làì', 'L', 'FUT.CONT', 'ZNC 2018'),
        ('leh', 'lèh', 'L', 'then', 'ZNC 2018'),
        ('tak', 'tàk', 'L', 'very/true', 'ZNC 2018'),
        ('tua', 'tùa', 'H', 'that', 'Henderson 1965'),
        ('hong', 'hòng', 'L', 'INV', 'ZNC 2018'),
        ('kong', 'kòng', 'L', '1.OBJ', 'ZNC 2018'),
        
        # More common nouns (from ZNC/Henderson)
        # Note: topa/pasian would need proper sourcing from ZNC grammar
        ('kumpi', 'kùmpì', 'LL', 'king', 'ZNC 2018'),
        
        # Additional Weera 1998 entries (checked syllables)
        # Tone 4 (low, short checked) - Weera Table 1
        ('bak', 'bak', 'L', 'full', 'Weera 1998'),
        ('cik', 'cik', 'L', 'tight', 'Weera 1998'),
        ('dat', 'dat', 'L', 'appear', 'Weera 1998'),
        ('hak', 'hak', 'L', 'awake', 'Weera 1998'),
        ('lap', 'lap', 'L', 'wing', 'Weera 1998'),
        ('nap', 'nap', 'L', 'snot', 'Weera 1998'),
        # Tone 2/3 entries from Weera (mid/falling)
        ('vom', 'vom', 'M', 'black', 'Weera 1998'),
        ('lun', 'lun', 'M', 'warm', 'Weera 1998'),
        ('thau', 'thau', 'M', 'fat', 'Weera 1998'),
        ('kal', 'kal', 'M', 'go', 'Weera 1998'),
        ('nam', 'nam', 'M', 'tribe', 'Weera 1998'),
        ('tuan', 'tuan', 'M', 'perch', 'Weera 1998'),
        
        # More high-frequency morphemes from corpus
        ('ahi', 'àhì', 'LL', '3SG.be', 'Henderson 1965'),
        ('ahih', 'àhìh', 'LL', '3SG.be.II', 'Henderson 1965'),
        ('pi', 'pì', 'L', 'INTENS', 'ZNC 2018'),
        ('khempeuh', 'khèmpeùh', 'LL', 'all', 'ZNC 2018'),
        ('lung', 'lùng', 'L', 'heart/mind', 'ZNC 2018'),
        ('aw', 'àw', 'L', 'EXCL', 'Henderson 1965'),
        ('khia', 'khìa', 'L', 'DIR.out', 'ZNC 2018'),
        ('mah', 'màh', 'L', 'EMPH', 'Henderson 1965'),
        ('nang', 'nàng', 'L', '2SG.EMPH', 'Henderson 1965'),
        ('tui', 'tùì', 'L', 'water', 'Henderson 1965'),
        ('sim', 'sìm', 'L', 'whole/all', 'ZNC 2018'),
        ('sawm', 'sàwm', 'L', 'ten', 'ZNC 2018'),
        ('amau', 'àmàu', 'LL', '3SG.POSS.EMPH', 'Henderson 1965'),
        ('hun', 'hùn', 'L', 'time', 'ZNC 2018'),
        ('gal', 'gàl', 'L', 'enemy/outside', 'ZNC 2018'),
        ('dang', 'dàng', 'L', 'other', 'ZNC 2018'),
        ('mahmah', 'màhmàh', 'LL', 'INTENS.EMPH', 'Henderson 1965'),
        ('kote', 'kòtè', 'LL', '1PL.EXCL.EMPH', 'Henderson 1965'),
        ('zawh', 'zàwh', 'L', 'COMPL', 'ZNC 2018'),
        ('peuh', 'peùh', 'L', 'any/each', 'ZNC 2018'),
        ('teng', 'tèng', 'L', 'all/every', 'ZNC 2018'),
        ('te', 'tè', 'L', 'PL', 'Henderson 1965'),
        ('lian', 'liàn', 'L', 'big', 'ZNC 2018'),
        ('suak', 'suàk', 'L', 'become', 'ZNC 2018'),
        ('nuai', 'nuài', 'L', 'under', 'ZNC 2018'),
        ('tungah', 'tùngàh', 'LL', 'on.LOC', 'ZNC 2018'),
        ('sam', 'sàm', 'L', 'call/invite', 'Henderson 1965'),
        ('loh', 'lòh', 'L', 'NEG.NOM', 'Henderson 1965'),
        ('vek', 'vèk', 'L', 'together', 'ZNC 2018'),
        ('nih', 'nìh', 'L', 'two', 'ZNC 2018'),
        ('khit', 'khìt', 'L', 'SEQ.II', 'Henderson 1965'),
        ('thum', 'thùm', 'L', 'three', 'ZNC 2018'),
        ('kei', 'kèi', 'L', '1SG.EMPH', 'Henderson 1965'),
        ('keimah', 'kèimàh', 'LL', '1SG.EMPH.full', 'Henderson 1965'),
        ('ngeina', 'ngèinà', 'LL', 'law', 'ZNC 2018'),
        ('tunga', 'tùngà', 'LL', 'on.LOC', 'ZNC 2018'),
        ('bulh', 'bùlh', 'L', 'sprinkle', 'Henderson 1965'),
        ('va', 'và', 'L', 'go.and', 'Henderson 1965'),
        
        # Common nouns and morphemes (from ZNC and Henderson)
        ('hoih', 'hòih', 'L', 'good', 'Henderson 1965'),
        ('van', 'vàn', 'L', 'sky/heaven', 'ZNC 2018'),
        ('pha', 'phà', 'L', 'cloth/good', 'Henderson 1965'),
        ('mawh', 'màwh', 'L', 'sin/wrong', 'ZNC 2018'),
        ('siam', 'siàm', 'L', 'able/skilled', 'ZNC 2018'),
        ('khut', 'khùt', 'L', 'hand', 'Henderson 1965'),
        ('nung', 'nùng', 'L', 'back/behind', 'ZNC 2018'),
        ('sang', 'sàng', 'L', 'high/building', 'ZNC 2018'),
        ('ngah', 'ngàh', 'L', 'receive/get', 'Henderson 1965'),
        ('dong', 'dòng', 'L', 'until', 'ZNC 2018'),
        ('ngei', 'ngèi', 'L', 'HAB.CONT', 'ZNC 2018'),
        ('uk', 'ùk', 'L', 'rule/govern', 'ZNC 2018'),
        ('sem', 'sèm', 'L', 'serve/work', 'ZNC 2018'),
        ('puan', 'puàn', 'L', 'blanket/cloth', 'Henderson 1965'),
        ('siangtho', 'siàngtho', 'LL', 'holy', 'ZNC 2018'),
        ('pawl', 'pàwl', 'L', 'group/some', 'ZNC 2018'),
        ('khiat', 'khìat', 'L', 'remove/DIR.away', 'ZNC 2018'),
        ('bek', 'bèk', 'L', 'only', 'ZNC 2018'),
        ('keima', 'kèimà', 'LL', '1SG.EMPH', 'Henderson 1965'),
        ('khawm', 'khàwm', 'L', 'collect/gather', 'ZNC 2018'),
        ('nangma', 'nàngmà', 'LL', '2SG.EMPH', 'Henderson 1965'),
        ('lim', 'lìm', 'L', 'look/empty', 'Henderson 1965'),
        ('hing', 'hìng', 'L', 'INV.IMP', 'ZNC 2018'),
        ('hilh', 'hìlh', 'L', 'teach/tell', 'ZNC 2018'),
        ('tawn', 'tàwn', 'L', 'experience/meet', 'ZNC 2018'),
        ('gim', 'gìm', 'L', 'tired/difficult', 'ZNC 2018'),
        ('thuak', 'thuàk', 'L', 'endure/suffer', 'ZNC 2018'),
        ('kham', 'khàm', 'L', 'prohibit/forbid', 'Henderson 1965'),
        ('nadingin', 'nàdìngìn', 'LLL', 'for.2SG.purpose', 'ZNC compound'),
        ('nading', 'nàdìng', 'LL', 'for.2SG.purpose', 'ZNC compound'),
        ('nasem', 'nàsèm', 'LL', '2SG.work', 'ZNC compound'),
        ('inla', 'ìnlà', 'LL', 'if/when', 'ZNC 2018'),
        
        # More verbs from Henderson
        ('koi', 'kòi', 'L', 'call', 'Henderson 1965'),
        ('gel', 'gèl', 'L', 'each/every', 'ZNC 2018'),
        ('zel', 'zèl', 'L', 'HAB.CONT', 'ZNC 2018'),
        ('pek', 'pèk', 'L', 'give', 'Henderson 1965'),
        ('tom', 'tòm', 'L', 'gather', 'Henderson 1965'),
        ('phut', 'phùt', 'L', 'COMPL.away', 'ZNC 2018'),
        ('bei', 'bèi', 'L', 'finish', 'Henderson 1965'),
        ('bul', 'bùl', 'L', 'root/base', 'ZNC 2018'),
        ('zang', 'zàng', 'L', 'use', 'ZNC 2018'),
        ('ngak', 'ngàk', 'L', 'wait', 'Henderson 1965'),
        ('cing', 'cìng', 'L', 'know', 'Henderson 1965'),
        ('zin', 'zìn', 'L', 'travel', 'Henderson 1965'),
        ('kem', 'kèm', 'L', 'touch', 'Henderson 1965'),
        ('gawh', 'gàwh', 'L', 'desire', 'Henderson 1965'),
        ('suk', 'sùk', 'L', 'DOWN', 'ZNC 2018'),
        ('phei', 'phèi', 'L', 'UP', 'ZNC 2018'),
    ]
    
    for orth, toned, tone, gloss, source in morphemes:
        entries.append({
            'orthographic': orth,
            'toned': toned,
            'ipa': '',
            'tone_pattern': tone,
            'gloss': gloss,
            'source': source,
            'confidence': 'high'
        })
    
    return entries

def get_canonical_glosses():
    """Get canonical glosses from morphological analyzer for alignment."""
    import sys
    sys.path.insert(0, 'scripts')
    try:
        from analyze_morphemes import (
            PRONOMINAL_PREFIXES, OBJECT_PREFIXES,
            ASPECT_SUFFIXES, DIRECTIONAL_SUFFIXES, MODAL_SUFFIXES,
            DERIVATIONAL_SUFFIXES, TAM_SUFFIXES, ADDITIONAL_VERBAL_SUFFIXES,
            CASE_MARKERS
        )
        
        canonical = {}
        
        # Prefixes
        for d in [PRONOMINAL_PREFIXES, OBJECT_PREFIXES]:
            for k, v in d.items():
                canonical[k.rstrip('-')] = v
        
        # Suffixes
        for d in [ASPECT_SUFFIXES, DIRECTIONAL_SUFFIXES, MODAL_SUFFIXES, 
                  DERIVATIONAL_SUFFIXES, TAM_SUFFIXES, ADDITIONAL_VERBAL_SUFFIXES,
                  CASE_MARKERS]:
            for k, v in d.items():
                canonical[k.lstrip('-')] = v
        
        return canonical
    except ImportError:
        return {}


def normalize_gloss(gloss):
    """Normalize gloss for comparison (strip .I/.II, lowercase)."""
    return gloss.split('.')[0].split('/')[0].lower()


def deduplicate_entries(entries):
    """
    Deduplicate entries by (orthographic, tone_pattern).
    
    Rules:
    1. Merge entries with same orth + tone + similar glosses (e.g., 'full' vs 'full.I')
    2. Keep distinct homophonous words (e.g., 'burn.I' vs 'foolish.I' for 'chai')
    3. Align glosses with analyzer's canonical glosses where possible
    """
    canonical = get_canonical_glosses()
    
    # Group by orthographic form
    by_orth = defaultdict(list)
    for entry in entries:
        by_orth[entry['orthographic']].append(entry)
    
    result = []
    
    for orth, elist in by_orth.items():
        # Group by tone pattern
        by_tone = defaultdict(list)
        for e in elist:
            by_tone[e['tone_pattern']].append(e)
        
        for tone, telist in by_tone.items():
            if len(telist) == 1:
                # Single entry - check if gloss should be aligned
                entry = telist[0]
                if orth in canonical and entry['gloss']:
                    # Update gloss to canonical if it's a grammatical morpheme
                    entry = dict(entry)  # Copy
                    entry['gloss'] = canonical[orth]
                result.append(entry)
            else:
                # Multiple entries with same tone - check if they can be merged
                glosses = [e['gloss'] for e in telist]
                base_glosses = set(normalize_gloss(g) for g in glosses if g)
                
                if len(base_glosses) <= 1:
                    # Same base meaning - merge, use canonical or first gloss
                    merged = dict(telist[0])
                    if orth in canonical:
                        merged['gloss'] = canonical[orth]
                    elif glosses[0]:
                        # Use shortest/cleanest gloss
                        merged['gloss'] = min((g for g in glosses if g), key=len)
                    result.append(merged)
                else:
                    # Different meanings - keep separate (true homophony)
                    for e in telist:
                        result.append(e)
    
    return result


def main():
    print("Extracting tone data from local resources...")
    
    all_entries = []
    
    # Phase 1: Known grammatical morphemes
    print("\n1. Extracting grammatical morpheme tones...")
    gram_entries = extract_grammatical_morpheme_tones()
    print(f"   Found {len(gram_entries)} entries")
    all_entries.extend(gram_entries)
    
    # Phase 2: Verb Form I/II pairs
    print("\n2. Extracting verb tone alternations...")
    verb_entries = extract_known_verb_tones()
    print(f"   Found {len(verb_entries)} entries")
    all_entries.extend(verb_entries)
    
    # Phase 3: Morpheme documentation
    print("\n3. Extracting from morpheme docs...")
    doc_entries = extract_from_morpheme_docs()
    print(f"   Found {len(doc_entries)} entries")
    all_entries.extend(doc_entries)
    
    # Deduplicate
    unique_entries = deduplicate_entries(all_entries)
    print(f"\nTotal unique entries: {len(unique_entries)}")
    
    # Save to TSV
    os.makedirs('data', exist_ok=True)
    output_path = 'data/tone_dictionary.tsv'
    
    with open(output_path, 'w', encoding='utf-8') as f:
        headers = ['orthographic', 'toned', 'ipa', 'tone_pattern', 'gloss', 'source', 'confidence']
        f.write('\t'.join(headers) + '\n')
        
        for entry in sorted(unique_entries, key=lambda x: x['orthographic']):
            row = [entry.get(h, '') for h in headers]
            f.write('\t'.join(row) + '\n')
    
    print(f"\nSaved to {output_path}")
    
    # Summary by tone pattern
    by_pattern = defaultdict(int)
    for e in unique_entries:
        by_pattern[e['tone_pattern']] += 1
    
    print("\nTone pattern distribution:")
    for pattern, count in sorted(by_pattern.items()):
        print(f"  {pattern}: {count}")
    
    # Summary by source
    by_source = defaultdict(int)
    for e in unique_entries:
        by_source[e['source']] += 1
    
    print("\nSource distribution:")
    for source, count in sorted(by_source.items(), key=lambda x: -x[1]):
        print(f"  {source}: {count}")

if __name__ == '__main__':
    main()
