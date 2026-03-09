#!/usr/bin/env python3
"""
Tedim Chin morphological analyzer for Leipzig-style glossing.

Analyzes Tedim words and produces morpheme-by-morpheme glosses
following Leipzig Glossing Rules conventions.

Usage:
    python analyze_morphemes.py <word>
    python analyze_morphemes.py --verse <verse_id>
    python analyze_morphemes.py --file <input_file>
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Optional

# =============================================================================
# MORPHEME INVENTORY
# =============================================================================

# Pronominal prefixes (subject/possessor)
PRONOMINAL_PREFIXES = {
    'ka': '1SG',
    'na': '2SG', 
    'a': '3SG',
    'i': '1PL.INCL',
}

# Object/direction prefixes
OBJECT_PREFIXES = {
    'kong': '1SG→3',  # I do to him/them
    'hong': '3→1',    # He/they do to me/us
}

# Case markers / postpositions (often cliticized)
CASE_MARKERS = {
    'in': 'ERG',      # Ergative/instrumental
    'ah': 'LOC',      # Locative
    'a': 'LOC',       # Locative (short form)
    'tawh': 'COM',    # Comitative "with"
    'panin': 'ABL',   # Ablative "from"
}

# TAM suffixes
TAM_SUFFIXES = {
    # Tense/Aspect markers
    'ding': 'PROSP',    # Prospective/future
    'ta': 'PFV',        # Perfective (completed action)
    'zo': 'COMPL',      # Completive (able to complete)
    'kik': 'ITER',      # Iterative (again)
    'nawn': 'CONT',     # Continuative
    'khin': 'IMM',      # Immediate/intensifier
    'sa': 'PAST',       # Past tense
    # Verbal extension suffixes (Round 154)
    'sak': 'CAUS',      # Causative
    'pih': 'APPL',      # Applicative (with/for)
    'khawm': 'COM',     # Comitative (together)
    'gawp': 'INTENS',   # Intensive (forcefully)
    'thei': 'ABIL',     # Abilitative (can/able)
    'theih': 'ABIL',    # Abilitative variant
    'nuam': 'want',     # Desiderative (want to)
    'pah': 'NEG.ABIL',  # Negative ability (cannot)
    'tawm': 'DIMIN',    # Diminutive (a bit)
    'khak': 'RES',      # Resultative
    'khit': 'COMPL',    # Completive variant
    'zaw': 'MORE',      # Comparative (more)
    'lua': 'too',       # Excessive (too much)
    'mawk': 'perhaps',  # Dubitative
    'pak': 'NEG.ABIL',  # Unable (variant)
    'lawh': 'NEG.ABIL', # Unable
    # Directional/motion suffixes
    'khia': 'out',      # Directional out
    'khiat': 'away',    # Directional away
    'lut': 'in',        # Directional in
    'toh': 'up',        # Directional up
    'to': 'CONT',       # Continuative
    'cip': 'tightly',   # Intensifier (firmly/tightly)
    # Other aspect markers
    'mang': 'COMPL',    # Completive (completely)
    'kim': 'fully',     # Completive (fully)
    'san': 'at',        # Locative relation
    'sim': 'ITER',      # Iterative variant
    'lam': 'DIR',       # Directional/manner
    'zia': 'manner',    # Manner nominal
    'sakin': 'CAUS.ERG', # Causative + ergative
    'sakkik': 'CAUS.ITER', # Causative + iterative
    'sakzo': 'CAUS.COMPL', # Causative + completive
    # Round 154 additions - more verbal suffixes
    'teng': 'until',    # Temporal boundary
    'kha': 'still',     # Persistive (still/yet)
    'suk': 'CAUS',      # Causative variant (make.become)
    'zawh': 'finish',   # Completive (finish V-ing)
    'nop': 'want',      # Desiderative variant
    'lai': 'middle',    # Temporal middle (while V-ing)
    'takin': 'really',  # Emphatic adverbializer
    'nasa': 'INTENS',   # Intensive (strongly)
    'zah': 'INTENS',    # Intensive (greatly/fear)
    'sawn': 'toward',   # Directional toward
    'thuah': 'always',  # Habitual (repeatedly)
    'tel': 'each',      # Distributive (each/every)
    'khop': 'together', # Collective
    'hak': 'INTENS',    # Intensive variant
    'loh': 'NEG',       # Negative result
    'pi': 'COMP',       # Comparative (more/-er)
    'pa': 'NMLZ.AG',    # Agent nominalizer (one who V-s)
    # Round 154 additions - more suffixes
    'khap': 'forbid',   # Prohibitive
    'suak': 'become',   # Inchoative (become)
    'sung': 'inside',   # Locative (within)
    'nin': 'ERG',       # Ergative variant (after consonant)
    'min': 'ERG',       # Ergative variant
    'nateng': 'NMLZ.until', # Nominalized + until
    'kikin': 'ITER.ERG',    # Iterative + ergative
    'neu': 'small',     # Diminutive
    'luat': 'exceed',   # Excessive
    'bawl': 'do',       # Light verb (do/make)
    'zang': 'use',      # Instrumental
    # Round 154 additions - second batch
    'tat': 'COMPL',     # Completive (completely)
    'siang': 'well',    # Manner (properly/well)
    'kawm': 'nearly',   # Approximative
    'phat': 'EMPH',     # Emphatic/intensive
    'zawk': 'MORE',     # Comparative variant
    'hawm': 'together', # Collective
    'bu': 'group',      # Collective/group
    'sawm': 'ten',      # Numeric (also: attempt)
    'huai': 'CAUS',     # Causative variant
    'beng': 'straight', # Adverbializer (directly)
    'dang': 'other',    # Other/different
    'sia': 'bad',       # Deteriorative (wrongly)
    'lan': 'appear',    # Evidential
    'pha': 'good',      # Evaluative (well)
    'lah': 'ADV',       # Adverbializer
    'ha': 'PL',         # Plural variant (archaic)
    'kin': 'quickly',   # Manner (quickly)
    # Round 154 additions - third batch
    'siat': 'spoil',    # Destructive
    'zawl': 'easy',     # Evaluative (easily)
    'khai': 'INSTR',    # Instrumental
    'vat': 'suddenly',  # Sudden/quick
    'kholh': 'INTENS',  # Intensive (denounce)
    'thang': 'spread',  # Extent (spread out)
    'dai': 'quiet',     # Manner (quietly)
    'sun': 'during',    # Temporal (during)
    'aimang': 'COMPL',  # Completive (all gone)
    'nai': 'near',      # Proximity
    'tak': 'truly',     # Emphatic
    'pen': 'TOP',       # Topic (already in FUNCTION_WORDS but also suffix)
    # Round 154 additions - fourth batch
    'lo': 'NEG',        # Negative
    'kip': 'keep',      # Keep/maintain (thukip = keep word)
    'lian': 'great',    # Augmentative (greatly)
    'mai': 'only',      # Restrictive
    'ham': 'also',      # Additive
    'am': 'also',       # Additive variant
    'no': 'young',      # Diminutive
    'kak': 'INTENS',    # Intensive
    # Round 154 additions - fifth batch
    'tuam': 'different', # Manner (differently)
    'dak': 'suddenly',   # Manner (suddenly) - variant of vat
    'khem': 'all',       # Totality (all/completely)
    'ang': 'like',       # Similative (like/as)
    'nu': 'female',      # Gender marker
    'na': 'NMLZ',        # Nominalizer (also in NOMINALIZERS)
}

# NOTE: 'te'' (PL.POSS) handled separately in possessive section

# Sentence-final particles
FINAL_PARTICLES = {
    'hi': 'DECL',     # Declarative
    'hiam': 'Q',      # Interrogative
}

# Negation
NEGATION = {
    'lo': 'NEG',
    'kei': 'NEG.EMPH',
}

# Demonstratives
DEMONSTRATIVES = {
    'hih': 'PROX',    # this
    'tua': 'DIST',    # that
}

# Nominalizers and plurals
NOMINALIZERS = {
    'mi': 'NMLZ.AG',  # Agent nominalizer
    'na': 'NMLZ',     # Nominalizer suffix
    'te': 'PL',       # Plural
    'uh': 'PL',       # Plural (separate word)
}

# =============================================================================
# AMBIGUOUS MORPHEMES - Contextual Disambiguation System
# =============================================================================
#
# PURPOSE:
# This system handles morphemes with multiple meanings (polysemy) by selecting
# the contextually appropriate gloss. Without this, single-gloss dictionaries
# would assign incorrect meanings to common words.
#
# ARCHITECTURE:
# 1. AMBIGUOUS_MORPHEMES dict: Lists all meanings for each polysemous morpheme
#    Format: morpheme -> [(meaning1, context_desc), (meaning2, context_desc), ...]
#
# 2. disambiguate_morpheme() function: Applies contextual rules to select meaning
#    Uses context dict with keys: position, prev_morpheme, next_morpheme,
#    has_prefix, has_suffix, has_ki_prefix, in_compound
#
# INTEGRATION:
# - For standalone words: Called in analyze_word() before FUNCTION_WORDS lookup
# - For morphemes in compounds: Called when stripping prefixes/suffixes
# - Context is built from the morphological analysis state
#
# ADDING NEW AMBIGUOUS MORPHEMES:
# 1. Add entry to AMBIGUOUS_MORPHEMES with all meanings
# 2. Add elif branch in disambiguate_morpheme() with rules
# 3. Rules should prioritize corpus frequency and grammatical context
# 4. Always include a sensible default (most common meaning)
#
# EXAMPLES:
# - za: 'hear' (verb, 283x) vs 'hundred' (numeral, 73x)
#   Rule: 'hundred' after kum/sawm, 'hear' otherwise
# - vei: 'sick' (standalone) vs 'wave' (with suffix) vs 'time' (after numeral)
#   Rule: context-dependent selection
#
# =============================================================================

AMBIGUOUS_MORPHEMES = {
    # za: 'hear' (verb) vs 'hundred' (number)
    # - 'hundred' when following kum/sawm or before tul, or standalone in number context
    # - 'hear' when with verbal morphology (prefixes ka/na/a, suffixes -te/-na/-in)
    'za': [
        ('hear', 'verbal'),      # Primary: with verbal morphology
        ('hundred', 'numeral'),  # After kum/sawm, before tul
    ],
    
    # la: 'take' (verb) vs 'and' (sequential conjunction) vs 'donkey' (noun)
    # - 'take' most common (la-in = taking, amah la = took him)
    # - 'and' after imperatives (hen la = let... and)
    # - 'donkey' rare (late = donkeys)
    'la': [
        ('take', 'verbal'),      # Primary: with verbal morphology
        ('and.SEQ', 'after_imperative'),  # After hen (imperative)
        ('donkey', 'nominal'),   # As noun (rare)
    ],
    
    # na: '2SG' (pronoun) vs 'NMLZ' (nominalizer suffix)
    # - '2SG' when standalone or as prefix
    # - 'NMLZ' when suffix on verbs (verb-na)
    'na': [
        ('2SG', 'standalone'),   # Standalone word
        ('NMLZ', 'suffix'),      # As suffix on verbs
    ],
    
    # pa: 'father' (noun) vs 'NMLZ.AG' (agentive nominalizer)
    # - 'father' standalone or with possessive (ka pa = my father)
    # - 'NMLZ.AG' as suffix creating agent nouns (verb-pa = one who verbs)
    'pa': [
        ('father', 'standalone'),  # Standalone or possessed
        ('NMLZ.AG', 'suffix'),     # Agentive nominalizer
    ],
    
    # man: 'finish' vs 'reason' vs 'catch/take' vs 'price'
    # - 'finish' in "a man khit" = finished
    # - 'reason' in "ahih manin" = therefore (frozen form)
    # - 'catch' in "amah man" = caught him
    # - 'price' in "a man" = its price
    'man': [
        ('finish', 'with_khit'),   # a man khit = finished
        ('catch', 'verbal'),       # with verbal morphology
        ('reason', 'in_manin'),    # frozen in manin
        ('price', 'nominal'),      # as noun
    ],
    
    # hang: 'reason' vs 'mighty/stallion'
    # - 'reason' in "bang hang hiam" = why (99% of occurrences)
    # - 'mighty' rare, possibly not in Bible text
    'hang': [
        ('reason', 'default'),     # Default meaning
        ('mighty', 'rare'),        # Rare meaning
    ],
    
    # vei: 'time/instance' vs 'sick/faint'
    # - 'time' in khatvei = once, nihvei = twice
    # - 'sick/faint' in phukhong vei = faint from hunger
    'vei': [
        ('time', 'with_numeral'),  # After numerals (sagih vei = seven times)
        ('wave', 'with_verb_morphology'),  # Wave offering (vei-a piak = wave-LOC give)
        ('sick', 'standalone'),    # Standalone or with illness words
    ],
    'pha': [
        ('good', 'as_suffix'),     # Evaluative suffix (thu-pha = word-good = blessing)
        ('branch', 'standalone'),  # Noun: branch/limb
    ],
    'kham': [
        ('gold', 'standalone'),    # Noun: gold (ngun le kham = silver and gold)
        ('forbid', 'with_ki'),     # Verb: forbid (ki-kham = REFL-forbid)
    ],
    
    # hi: 'be' (copula) vs 'DECL' (sentence-final particle)
    # Henderson 1965: hi is declarative particle sentence-finally
    # As copula when preceded by subject prefix (ka-hi, a-hi)
    'hi': [
        ('DECL', 'sentence_final'),  # Sentence-final declarative particle
        ('be', 'with_prefix'),       # Copula with pronominal prefix
    ],
    
    # sa: 'flesh' (noun) vs 'PERF' (perfective suffix on verbs)
    # - 'flesh' standalone or with nominal morphology
    # - 'PERF' after verb stems (muh-sa = seen, nei-sa = had)
    'sa': [
        ('flesh', 'nominal'),        # Noun: flesh, meat, wild game
        ('PERF', 'after_verb'),      # Perfective aspect after verbs
    ],
    
    # ta: 'child' (noun) vs 'PFV' (perfective aspect)
    # - 'child' in compounds (ta-pa = son, ta-nu = daughter)
    # - 'PFV' after verbs (nei-ta = already have)
    'ta': [
        ('child', 'nominal'),        # Noun: child, offspring
        ('PFV', 'after_verb'),       # Perfective aspect marker
    ],
    
    # tung: 'on/upon' (relational noun) vs 'arrive' (verb)
    # - 'on' when followed by -ah (tung-ah = on-LOC)
    # - 'arrive' with verbal morphology
    'tung': [
        ('on', 'with_ah'),           # Relational noun + LOC
        ('arrive', 'verbal'),        # Motion verb
    ],
}

# Common function words with glosses - expanded with frequencies
FUNCTION_WORDS = {
    # === Conjunctions & Connectors ===
    'le': 'and',             # 10,942
    'la': 'take',            # Round 155: primary meaning is 'take' (also 'and.SEQ' after hen)
    'masa': 'first',         # Round 155: a masa = the first (not ma-sa)
    'sia': 'evil',           # Round 155: a sia = evil (not si-a)
    'leh': 'and/or',         # 2,921
    
    # Sentence-initial function words (prevent proper noun treatment)
    'Tu-in': 'now-ERG',      # Sentence-initial 'tu-in'
    'Siangtho': 'holy',      # Sentence-initial 'siangtho'
    'ahihleh': 'if',         # 335
    'hitaleh': 'if.so',      # 295
    'hang': 'reason',        # Round 155: fix - "bang hang hiam" = why (not stallion)
    'hangin': 'because',     # 3,461
    'bangin': 'like',        # 3,886
    'man': 'finish',         # Round 155: a man khit = finished (also catch/wrong)
    'manin': 'therefore',    # 2,790
    'zongin': 'although',    # 1,970
    'ciangin': 'then',       # 9,297
    'inla': 'and.then',      # ~838
    'napi': 'but/however',   # 279x - contrastive conjunction
    'hinapi': 'but/however', # 156x - variant with hi-
    'hinapi-in': 'but/however.ERG',  # 126x - hinapi with ergative
    'hinapiin': 'but/however.ERG',   # variant without hyphen
    'mateng': 'until',       # 185x - temporal "until"
    'matengin': 'until',     # 99x - variant with -in
    'veve': 'still/yet',     # 142x - temporal adverb (reduplication)
    
    # === Purpose/Infinitive markers (NOT 2SG!) ===
    'nading': 'PURP',        # 1140x - "in order to, for (purpose)" 
    'nadingin': 'PURP.ERG',  # 1671x - purpose marker with ergative
    
    # === Topic/Focus Particles ===
    'mah': 'EMPH',           # 1,540
    'pen': 'TOP',            # 4,541
    'zong': 'also',          # 3,320
    'bek': 'only',           # 782
    
    # === Quantifiers ===
    'khempeuh': 'all',       # 4,783
    'peuhpeuh': 'every',     # 431
    'tampi': 'many',         # 727
    'teltel': 'each',
    'vekpi': 'altogether',   # 213x "all (of), total"
    'tuamtuam': 'various',   # 59x - "different kinds, various" (reduplication)
    'ciatin': 'each.kind.ERG', # 45x - "after its kind" (ciat + -in)
    'ciatciatin': 'each.kind~RED', # 20x - "each after their kind" (reduplicated)
    
    # === Adverbs - Temporal/Iterative ===
    'leuleu': 'again',       # 193x - reduplication of leu
    'leu': 'again',          # base form for leuleu
    'nitakin': 'at.evening', # 35x - "in the evening" (ni-tak-in)
    'nihin': 'today',        # 35x - "today" (ni-hin = day-this)
    
    # === Verbal particles ===
    'kawmin': 'while',       # 39x - "while, as" (temporal subordinator)
    'itin': 'lovingly',      # 41x - "lovingly, kindly" (it-in)
    'nangawnin': 'henceforth', # 43x - "from now on, forever"
    'nangawnah': 'forever',  # 36x - variant with -ah
    
    # === Interrogatives ===
    'bangci': 'how',         # 36x - "how" (interrogative adverb)
    'bangciin': 'how.ERG',   # variant with -in
    'bangci-in': 'how.ERG',  # hyphenated variant
    
    # === Demonstratives ===
    'tua': 'DIST',           # 9,156 (sentence-initial)
    'hih': 'PROX',           # 4,025
    'tua': 'that',
    'hih': 'this',
    'Tua': 'that',           # capitalized sentence-initial
    
    # === Copula/Auxiliary ===
    'ci': 'say',             # 5,954
    'cih': 'say.NOM',        # 2,827
    'ahi': 'be.3SG',         # 7,409
    'ahih': 'be.3SG.REL',
    'hi': 'DECL',            # 35,961
    'om': 'exist',           # 5,068
    
    # === Independent Pronouns ===
    'amah': '3SG.PRO',       # 4,404
    'amaute': '3PL.PRO',     # 4,590
    'keimah': '1SG.PRO',     # 656
    'nangmah': '2SG.PRO',    # 435
    'amau': '3PL.PRO',
    'note': '2PL.PRO',       # 3,016
    'kote': '1PL.PRO',       # 649
    'nang': '2SG.PRO',
    'nangma': '2SG.self',    # emphatic 2SG
    'keima': '1SG.self',     # emphatic 1SG
    'eite': '1PL.PRO',       # we (exclusive)
    'nomau': '2PL.PRO',      # 62x - "you (plural)" (alternative form)
    "nomau'": '2PL.POSS',    # 44x - "your (plural)" with possessive marker
    "ke'n": '1SG.PRO',       # 63x - "I" (contraction of kei) - straight quote
    "ke\u2019n": '1SG.PRO',   # curly quote version
    "keima-a'": '1SG.self.GEN', # 31x - "my own" - straight quote
    "keima-a\u2019": '1SG.self.GEN', # curly quote version
    'kei': '1SG.PRO',        # "I"
    'nangmahmah': '2SG.EMPH.REDUP', # 23x - "you yourself" (emphatic reduplication)
    "kua'n": 'nobody.EMPH',  # 9x - "nobody" variant - straight quote
    "kua\u2019n": 'nobody.EMPH', # curly quote version
    
    # === Pronominal Markers (standalone) ===
    'ka': '1SG',
    'na': '2SG',
    'a': '3SG',              # 58,363 (also generic article)
    'i': '1PL.INCL',
    'kong': '1SG→3',         # 1,945
    'hong': '3→1',           # 15,358
    'nong': '2→1',           # 720
    
    # === Case Markers (standalone) ===
    'in': 'ERG',             # 22,726
    'ah': 'LOC',
    'uh': 'PL',              # 21,924
    'un': 'PL.IMP',
    'tawh': 'COM',           # 7,572
    'panin': 'ABL',          # 4,296
    'sangin': 'COMP',        # 517
    'dong': 'until',         # 647
    
    # Combinations with plural uh-
    'uhah': 'PL.LOC',        # 507x - "in your/their (plural)"
    'uhleh': 'PL.if',        # 306x - "if you (plural)"
    'uha': 'PL.LOC',         # 56x - variant of uhah
    'ulian': 'PL.elder',     # 96x - needs analysis (could be elder-great)
    'ung': 'PL.FUT',         # 30x - plural future marker
    'up': 'PL.Q',            # 60x - plural question marker
    
    # === Military vocabulary ===
    'kidona': 'sword',       # 56x - sword (not ki-don-a)
    
    # === Nature vocabulary ===
    'tuipi': 'sea',          # 256x - tui-pi = water-big = sea (not proper noun)
    'Tuipi': 'sea',          # capitalized variant
    
    # === Negation ===
    'lo': 'NEG',             # 6,018
    'kei': 'NEG.EMPH',       # 6,487
    'loh': 'NEG.NOM',        # 885
    'loin': 'NEG.ERG',       # 873
    'kuamah': 'nobody',      # 595
    'bangmah': 'nothing',    # 495
    
    # === Question ===
    'hiam': 'Q',             # 2,766
    
    # === TAM Markers ===
    'ding': 'PROSP',         # 18,980
    'dingin': 'PROSP.ERG',   # 4,798
    'nadingun': '2PL.PROSP.IMP',  # 656
    'ta': 'PFV',             # 1,106
    'zo': 'COMPL',
    'kik': 'ITER',
    'nawn': 'CONT',          # 1,022
    'khin': 'IMM',           # 893
    'khit': 'SEQ',           # 996
    
    # === Relational/Nominalizers ===
    'mi': 'person/REL',      # 4,221
    'te': 'PL',
    # Note: 'na' is 2SG in FUNCTION_WORDS (line 295), -na is NMLZ as suffix
    
    # === Numbers ===
    'khat': 'one',           # 4,303
    'nih': 'two',            # 598
    'thum': 'three',         # 626
    'li': 'four',
    'nga': 'five',
    'guk': 'six',
    'sagih': 'seven',
    'giat': 'eight',
    'kua': 'nine',
    'sawm': 'ten',           # 679
    'sawmnih': 'twenty',     # 263
    'za': 'hundred',         # In number context (kum za = 100 years); also 'hear' - see AMBIGUOUS_MORPHEMES
    'tul': 'thousand',
    
    # === Locative/Relational Nouns ===
    'sung': 'inside',        # 2,208
    'tung': 'on',            # 1,413
    'kiang': 'beside',       # 597
    'lai': 'midst',          # 1,032
    'lak': 'among',          # 552
    'mai': 'front',
    'ban': 'besides',        # 85x - "beside X", often banah "in addition to"
    'pualam': 'outside',     # 60x - "without, outside"
    'nuai': 'below',         # 42x - "under"
    
    # === Adverbs ===
    'mahmah': 'very',
    'tawntung': 'forever',   # 679
    'tu': 'now',
    
    # === Interrogatives/Comparatives ===
    'bang': 'what/like',     # often in compounds
    'kua': 'who',
}

# =============================================================================
# VERB STEM ALTERNATION (Form I / Form II)
# =============================================================================
#
# Based on Henderson 1965 "Tiddim Chin: A Descriptive Analysis of Two Texts"
#
# Tedim Chin verbs have two forms:
# - Form I (Indicative): Used in conclusive sentences (final predicative phrase)
# - Form II (Subjunctive): Used in inconclusive sentences and adjunctive phrases
#
# Form II is derived from Form I by phonological rules:
# 1. For verbs with long final syllable + Tone 1/2: Add -h, change to Tone 3
#    Examples: mu → muh (see), thei → theih (know), nei → neih (have)
#
# 2. For some verbs: Add -k instead of -h
#    Examples: za → zak (hear), pia → piak (give), ne → nek (eat)
#
# 3. For verbs ending in -ng: Change to -n (velar → alveolar)
#    This pattern is less common in the Bible corpus
#
# The analyzer recognizes both forms and glosses them appropriately.
# Form II verbs get the same base gloss as Form I (the alternation is 
# grammatical, not lexical).
#
# =============================================================================

VERB_STEM_PAIRS = {
    # Primary verb alternation pairs: Form I → Form II
    # Format: form_ii: (form_i, base_gloss)
    
    # +h alternation (most common)
    'muh': ('mu', 'see'),           # 503x Form II / 967x Form I
    'theih': ('thei', 'know'),      # 1385x / 2579x
    'neih': ('nei', 'have'),        # 416x / 1803x
    'cih': ('ci', 'say'),           # 2827x / 5971x
    'zuih': ('zui', 'follow'),      # 170x / 509x
    'ngaih': ('ngai', 'think'),     # 52x / 434x
    'neh': ('ne', 'eat'),           # 17x / 560x
    'siah': ('sia', 'decay'),       # 61x / 220x
    'khialh': ('khial', 'err'),     # 54x / 177x
    'luah': ('lua', 'exceed'),      # 192x / 111x
    'puah': ('pua', 'bet'),         # 66x / 153x
    'tuah': ('tua', 'do'),          # 47x / (tua usually demonstrative)
    'tanh': ('tan', 'spread'),      # 71x / 22x
    'genh': ('gen', 'speak'),       # Form II of gen
    'bawlh': ('bawl', 'make'),      # Form II of bawl
    'omh': ('om', 'exist'),         # Form II of om
    'paih': ('pai', 'go'),          # Form II of pai
    
    # +k alternation
    'zak': ('za', 'hear'),          # 347x / 664x
    'piak': ('pia', 'give'),        # 797x / 2209x
    'nek': ('ne', 'eat'),           # 199x / 560x (both +h and +k exist)
    'biak': ('bia', 'worship'),     # 212x / 219x
    'puak': ('pua', 'spill'),       # 239x / 153x
    'tuak': ('tua', 'meet'),        # 100x (verbal, not demonstrative)
    'muk': ('mu', 'see'),           # 24x (alternative Form II)
    'kiak': ('kia', 'fear'),        # 8x / 66x
}

# Reverse lookup: Form I → Form II (for reference)
FORM_I_TO_II = {v[0]: (k, v[1]) for k, v in VERB_STEM_PAIRS.items()}

# Verb stems - expanded from corpus frequency analysis
# Note: Some verbs have Stem I (basic) and Stem II (modified) forms
VERB_STEMS = {
    # Existence/State (high frequency)
    'om': 'exist',           # 5,068
    'hi': 'be',              # copula
    'ahi': 'be.3SG',         # 7,409
    'ahih': 'be.3SG.REL',    # relativized copula
    'suak': 'become',        # 605
    'teng': 'dwell',         # 859
    'dam': 'be.well',        # health state
    'hoih': 'be.good',       # 641
    'sih': 'die',            # death
    'sil': 'wipe/erase',     # sil-khia = wipe away
    'nung': 'live',          # life
    'piang': 'be.born',      # birth
    
    # Motion verbs
    'pai': 'go',             # 2,350
    'va': 'go.and',          # 817
    'lut': 'enter',
    'khia': 'exit',
    'tung': 'arrive',
    'zui': 'follow',         # 504
    'ciahpai': 'go.home',
    'liahpai': 'return',
    'zuan': 'cross',
    'ciah': 'return',        # 360
    'ciahkik': 'return.again',
    
    # Perception verbs (with stem alternation)
    'mu': 'see.I',           # 962 (Stem I)
    'muh': 'see.II',         # 501 (Stem II)
    'za': 'hear.I',          # 652 (Stem I)
    'zak': 'hear.II',        # (Stem II)
    'ngai': 'listen.I',
    'ngaih': 'listen.II',
    'en': 'look',
    
    # Cognition verbs (with stem alternation)
    'thei': 'know.I',        # 2,543 (Stem I)
    'theih': 'know.II',      # 1,383 (Stem II / passive)
    'um': 'believe',
    'ngaihsun': 'think',     # 409 "mind-think"
    'ngaihsut': 'consider',  # 210
    'lung': 'feel',          # emotional state
    'deih': 'want',          # 279
    'nuam': 'want',
    
    # Speech verbs
    'ci': 'say',             # 5,954
    'cih': 'say.NOM',        # 2,827
    'gen': 'speak',          # 2,416
    'hilh': 'teach',
    'thugen': 'preach',      # 353 "word-speak"
    'sam': 'call',
    'sampah': 'proclaim',
    'kiko': 'cry.out',
    'paupai': 'gossip',
    'pau': 'speak',          # 240
    
    # Transfer/Possession
    'pia': 'give',           # 2,202
    'piak': 'give.to',       # 781
    'lak': 'take',           # 552
    'nei': 'have',           # 1,770
    'koih': 'put',           # 592
    'sawl': 'send',          # 541
    'sak': 'cause',          # 220 causative
    
    # Action verbs
    'bawl': 'make',          # 1,532
    'sem': 'serve',          # 603
    'sep': 'work',           # 127
    'uk': 'rule',            # 664
    'that': 'kill',
    'tat': 'strike',
    'sat': 'strike',         # 214
    'ne': 'eat',             # 552
    'nek': 'eat.II',
    'thuak': 'suffer',       # 535
    'phum': 'immerse',
    'vak': 'walk',
    'tawp': 'end',
    'ding': 'stand',
    'to': 'sit',
    'ton': 'pull',           # "pull, draw" (tonsak = cause.to.pull)
    'tut': 'sleep',
    'suk': 'make.become',
    'khen': 'divide',
    'gelh': 'write',
    'kap': 'weep',           # 185
    'zah': 'fear',           # 182
    'zawh': 'be.able',       # 178
    'khial': 'err',          # 177
    'nusia': 'abandon',      # 173
    'pil': 'learn',          # 242
    'siam': 'be.skilled',    # 174
    'lup': 'bow.down',       # 140
    'kem': 'guard',          # 147
    'zang': 'use',           # 198
    'duh': 'want/love',      # 30x - "want, love, desire"
    'muan': 'trust',         # 30x - "trust, rely on"
    'vel': 'around',         # 29x - "around, approximately"
    'im': 'hide',            # 33x - "hide" (im ding = shall hide)
    'u': 'elder.sibling',    # 28x - "elder brother/sister"
    'nungta': 'live',        # 29x - "be alive, live" (variant of nuntak)
    'limci': 'promise',      # 32x - "promise, sign" (lim-ci)
    
    # Reflexive/reciprocal (ki- prefix)
    'kipat': 'begin',        # Round 155: variant of kipan (a kipat = in the beginning)
    'kipan': 'begin',        # ki-pan "REFL-begin"
    'kizom': 'unite',        # Round 155: be united/joined
    'kisai': 'concern',
    'kisik': 'repent',
    'kikhia': 'depart',
    'kibawl': 'be.done',     # 338
    'kibang': 'be.alike',    # 612
    'kikhel': 'differ',
    'kituah': 'meet',
    'kikhen': 'separate',
    'kilem': 'prepare',      # 131
    
    # Causative/applicative (-sak, -pih)
    'paisak': 'send',        # pai-sak "go-CAUS"
    'damsak': 'heal',        # dam-sak "well-CAUS"
    'paipih': 'accompany',   # 599 pai-pih "go-APPL"
    'honkhia': 'bring.out',
    'piangsak': 'cause.birth', # 221
    'tungsak': 'lift.up',    # 197
    'paikhiat': 'send.away', # 202
    
    # Additional common verbs from corpus
    'it': 'love',
    'zol': 'redeem',
    'hong': 'come/open',
    'ciapteh': 'receive',
    'nuntak': 'live',        # nun-tak "life-firm"
    'minthan': 'bless',      # 253
    'hehpih': 'be.angry',    # 233
    'zahtak': 'honor',       # 148
    'lungdam': 'rejoice',    # 154
    
    # Additional verb stems from frequency analysis (Round 2)
    'huam': 'surround',      # 27x
    'buang': 'be.confused',  # 21x
    'ngeisa': 'desire',      # 15x
    'dem': 'blame',          # 12x
    'phong': 'reveal',       # 11x
    'ngian': 'endure',       # 11x
    'buak': 'fight',         # 10x
    'laih': 'replace',       # 10x
    'gawm': 'seize',         # 9x
    'hawl': 'seek',          # 9x
    'pung': 'increase',      # 12x
    'hoi': 'arrange',        # 15x
    'zuat': 'prepare',       # 13x
    'ngah': 'get',           # common
    'let': 'return',         # 10x
    'dial': 'call',          # 10x
    'vial': 'encircle',      # 10x
    'tangtun': 'arrive',     # 10x
    'hawm': 'join',
    'cim': 'pierce',
    'zop': 'join',           # 10x
    'kho': 'labor',          # 10x
    'puah': 'divine',
    'dokkik': 'oppose',      # 10x
    'dinkhiat': 'stand.up',  # 10x
    'zem': 'be.straight',    # 11x
    'sel': 'slice',          # 11x
    'khum': 'cover',         # 14x
    'hisak': 'make.known',   # 19x
    'neih': 'have.II',       # 16x (Stem II of nei)
    'sithei': 'be.possible', # 17x
    'veng': 'guard',         # 15x
    'mangkhin': 'faint',     # 14x
    'guang': 'carry',        # 12x
    'thadah': 'forgive',     # 12x
    'uih': 'bark',           # 12x
    'vekin': 'like',         # 12x
    'gimthuak': 'suffer',    # 12x
    'manphazaw': 'succeed',  # 12x
    'bangcih': 'how.say',    # 12x
    'siansak': 'sanctify',   # 12x
    'huhau': 'surround',     # 12x
    'geelsa': 'mark',        # 11x
    'sunglam': 'inside.way', # 11x
    'notkhia': 'bring.out',  # 9x
    'kunsuk': 'bend.down',   # 9x
    'vukcip': 'cover.over',  # 9x
    
    # Additional verb stems (Round 3 - remaining unknowns)
    'bat': 'bind',           # for kibat
    'tuam': 'promise',       # for kituam
    'phut': 'spray',         # for kiphut  
    'lakkhiat': 'snatch',    # ki-lakkhiat "take-away"
    'limbawl': 'prepare',    # 26x
    'khinsa': 'mock',        # 28x
    'hamtang': 'be.strong',  # 15x
    'liang': 'shine',        # 15x
    'khitsa': 'leave',       # 15x
    'lobuang': 'disturb',    # 14x
    'diak': 'be.different',  # 14x
    'galtai': 'be.captive',  # 13x
    'taleng': 'gather',      # 13x
    'huai': 'dread',         # 12x
    'dei': 'say',            # 11x - variant of ci
    'ngongtat': 'oppose',    # 10x
    'mal': 'be.dry',         # 14x
    'ven': 'protect',        # 14x
    'seek': 'sweep',         # 17x
    'vot': 'vote',           # 11x (loan word)
    'puakkik': 'return',     # 11x
    
    # Round 4 - more verb stems from remaining unknowns
    'am': 'sink',            # for kiam (ki-am)
    'mat': 'grasp',          # for kimat (ki-mat)
    'cian': 'announce',      # for kician (ki-cian)
    'pawlthei': 'join',      # for kipawlthei
    'teh': 'measure',        # for kiteh
    'kham': 'forbid',        # for kikham
    'kep': 'clutch',         # for kikep
    'khem': 'restrain',      # for kikhem
    'pua': 'carry.on.back',  # for kipua
    'sit': 'cut.off',        # for kisit
    'nga': 'endure',         # for kinga
    'peel': 'peel',          # 12x
    'peng': 'break.into',    # 10x
    'hum': 'cover',          # 10x
    'taka': 'truly',         # 9x
    'tanau': 'orphan',       # 9x (noun)
    've': 'do',              # 9x
    'ngeingai': 'truly.want', # 9x
    
    # Round 5 - philologically verified stems from Bible context analysis
    # Each entry verified by examining English verse contexts
    'ba': 'owe',             # 11x - Matt 18:23-24 "owed ten thousand talents"
    'nolh': 'reject',        # 9x - 1Sam 15:23 "rejected the word", "abhorred"
    'kunh': 'entreat',       # 9x - Judg 13:8 "intreated the LORD"
    'siim': 'feast',         # 9x - Job 1:4 "feasted in their houses"
    'vul': 'flourish',       # 9x - Ps 1:3 "like a tree planted" (cf. Henderson informant)
    'tot': 'contend',        # 9x (via kitot) - Num 27:14 "rebelled/strife"
    'nial': 'argue',         # 9x (via kinial) - Job 9:3 "contend/answer"
    'siat': 'spoil',         # 9x (via kisiat) - Ps 18:37 "pursued/overtaken"
    'samsiat': 'destroy',    # compound sam-siat (call-spoil = destroy)
    'lawnthal': 'overthrow', # 9x - Ex 15:7 "overthrown them"
    'zomlai': 'journey',     # 9x - Gen 35:21 "journeyed"
    'lianlua': 'too.much',   # 9x - Num 11:14 "too heavy for me"
    'thakhatthu': 'suddenly', # 9x - Num 12:4 "suddenly", Lev 26:16 "terror"
    'tuakun': 'meet',        # 9x - Prov 22:2 "meet together"
    'sungtawng': 'within',   # 10x - 1Ki 6:19 "in the house within", "oracle"
    'dongun': 'boundary',    # 14x - Lev 23:22 "corners of thy field"
    'utzaw': 'destruction',  # 11x - Job 7:15 "death", Isa 65:12 "slaughter"
    
    # Round 6 - additional verbs from residual analysis
    'puak': 'send',          # 239x - Gen 37:32 "sent/brought", Gen 38:17 "send"
    'ngak': 'wait',          # 102x - Gen 8:12 "stayed", Gen 49:18 "waited"
    'ngam': 'dare',          # 128x - (context shows "venture/dare")
    'hawlkhia': 'drive.out', # 119x - Gen 3:24 "drove out the man"
    'vei': 'sick',           # 71x - Gen 25:29 "he was faint" (sick/faint/exhausted)
    'zenzen': 'at.all',      # 53x - intensifier (often with negation "not at all")
    'mengmeng': 'quickly',   # 50x - reduplication "hastily, speedily" (Gen 18:6)
    'meng': 'quick',         # base for mengmeng
    'kantan': 'cross.over',  # 45x - "pass over, cross" (NOT kan-tan)
    'khahkhia': 'deliver',   # 46x - "deliver, rescue" (NOT khah-khia)
    'lungkia': 'dismay',     # 43x - "be dismayed, terrified"
    'tawlngak': 'rest',      # 45x - "rest" (base for tawlngakna)
    'sitbaang': 'blemish',   # 43x - "blemish" (without blemish)
    'ut': 'will/want',       # 44x - "will, desire" (base for utna)
    'buai': 'confuse',       # 41x - "confusion, astonishment" (base for buaina)
    'tuang': 'ride',         # 43x - "ride" (tuangte = riders, horsemen)
    'hon': 'flock',          # 41x - "flock, herd" (honte = flocks)
    'ngetsak': 'pray/intercede',  # 61x - causative of nget (request)
    
    # === Recently discovered verb stems (from partial analysis) ===
    'ap': 'press/submit',    # 53x - ki-ap = submit (reflexive)
    'at': 'cut',             # 53x - ki-at = circumcise (reflexive cut)
    'bia': 'worship',        # 49x - bia-in = worshipping
    'biak': 'worship/serve', # 211x - "worship, serve" (biak nading = for serving)
    'gamtat': 'kingdom',     # base for gamtatna, gamtatnasa
    'phat': 'praise',        # 70x - "praise, bless, commend" (kiphatsakna = pride)
    'phatsak': 'glorify',    # 45x - "glorify" (phat + CAUS)
    'zeet': 'tempt',         # 48x - "tempt, test" (ze-et hyphenated)
    'khangsak': 'raise.up',  # 39x - "raise up generations" (khang + CAUS)
    'lasak': 'take.CAUS',    # 39x - "take away" (la + sak)
    
    # === Session 2: More verb stems from philological analysis ===
    'kantan': 'cross.over',  # 44x - "cross over, fly across" (vantung kantanin = fly across heaven)
    'sawlkhia': 'send.forth', # 37x - "send forth, expel"
    'lumkhawm': 'lie.with',  # 37x - "lie with, sleep with"
    'sepsak': 'serve/work.for', # 35x - "cause to work, serve"
    'khaktan': 'restrain',   # 35x - "restrain, prevent" (khak-tan)
    'vangik': 'burden/load', # 35x - "burden" (between two burdens)
    'cimawh': 'oppress',     # 39x - "oppress" (a zawng a cimawh = oppressed)
    
    # === Session 3: Additional verb stems ===
    'khuh': 'cover',         # 36x - "cover" (kh-uh vs cover.I, but better as standalone)
    'sap': 'call/summon',    # 33x - "call, summon" (Faro in Moses sap = Pharaoh called Moses)
    'ngat': 'seek/divine',   # 33x - "seek (omens), divine"
    'ciam': 'promise',       # 33x - "promise" (thuciam = thu-ciam = word-promise = covenant)
    'it': 'love',            # base for "itte" (it-te = love-PL?)
    'gamta': 'send.away',    # 50x - "send away" (hong hawlkhia = sent away)
    'dawng': 'get/receive',  # 387x - "get, receive, fetch" (bawngno a dawng = fetched a calf)
    'luan': 'flow',          # 32x - "flow" (luanna = flowing)
    'khiat': 'depart/leave', # 32x - "depart, leave"
    'pian': 'create/born',   # 32x - "create, be born" (piansak = creation work)
    'bei': 'end/finish',     # 32x - "end, finish" (beina = ending)
    'pan': 'plead',          # 32x - "plead, argue for"
    'kido': 'fight',         # 31x - "fight" (galkidona = warfare)
    'ciah': 'return',        # 31x - "return" (ciahsak = send back)
    'khol': 'denounce',      # 31x - "denounce" (genkhol = speak denounce)
    'nuih': 'laugh',         # 31x - "laugh" (nuihsan = laugh at)
    'simmawh': 'blaspheme',  # 31x - "blaspheme"
    'khual': 'sojourn',      # 30x - "sojourn, visit" (khualmi = stranger)
    'zah': 'fear/respect',   # 30x - "fear, respect" (zahzah = reduplicated)
    'kihtak': 'dread',       # 30x - "dread" (kihtakna = dread)
    'suahtak': 'redeem',     # 30x - "redeem" (suahtakna = redemption)
    'nop': 'willing/want',   # 52x - "willing, want" (a numei in nang hong zuih nop)
    'ngaih': 'think/love',   # 33x - "think lovingly of, love"
    'muhdah': 'trouble',     # 29x - "trouble, make stink"
    'geel': 'plan/fashion',  # 29x - "plan, design" (geelna = pattern)
    'teel': 'choose',        # 28x - "choose" (teelna = choice)
    'mindai': 'shame',       # 29x - "shame" (mindaina = shame)
    'sep': 'work',           # 28x - "work" (sepnate = works)
    'ngaihsut': 'think/imagine', # 27x - "think, imagine" (ngaihsutnate = thoughts)
    
    # === Session 4 Round 9: More verb stems for -sak causatives ===
    'khialh': 'err/sin',     # khialhsak = cause to sin
    'piasak': 'cause.give',  # pia-sak = give-CAUS
    'siatsak': 'destroy',    # siat-sak = spoil-CAUS
    'khamsak': 'preserve',   # kham-sak = keep-CAUS
    'paikhiasak': 'send.away', # pai-khia-sak = go-out-CAUS
    'vaihawmsak': 'arrange', # va-i-hawm-sak = go.and-?-together-CAUS
    'zahhuaisak': 'triumph', # zah-huai-sak = fear-dread-CAUS
    'pungsak': 'increase',   # pung-sak = grow-CAUS
    'zuisak': 'follow.for',  # zui-sak = follow-CAUS
    'piaksak': 'give.for',   # piak-sak = give.to-CAUS
    'kangsak': 'raise.up',   # kang-sak = generation-CAUS
    'nopsak': 'please',      # nop-sak = willing-CAUS
    'nungsak': 'revive',     # nung-sak = live-CAUS
    'lungkhamsak': 'encourage', # lungkham-sak = courage-CAUS
    
    # === Session 5: Base verbs for ki- decomposition ===
    'nawh': 'hurry',         # kinawh = REFL-hurry
    'kholh': 'accompany',    # kikholh = REFL-accompany (be with)
    'lawi': 'dislocate',     # kilawi = REFL-dislocate (out of joint)
    'diah': 'dip',           # kidiah = REFL-dip (put in water)
    'khin': 'move',          # kikhin = REFL-move (set forward)
    'phah': 'spread',        # kiphah = REFL-spread (spread forth)
    'sut': 'spoil',          # kisut = REFL-spoil
    'nitsak': 'defile',      # kinitsak = REFL-defile
    'nit': 'defile',         # base for nitsak
    'phel': 'clear',         # kiphel = REFL-clear
    'tamzan': 'break.many',  # kitamzan = broken
    'hem': 'remove',         # hemkhia = remove-exit
    'meeng': 'branch',       # meengkhia = branch-exit
    'hazat': 'jealous',      # hazatna = jealousy
    'luang': 'flow',         # luangkhia = flow out
    'guta': 'destroyer',     # gutate = destroyers
    'tang': 'take.hold',     # kitang = take hold of each other
    'keek': 'tear',          # kikeek = be rent
    'lawh': 'spread',        # kilawh = spread
    'kalh': 'lock',          # kikalh = be locked
    'behlap': 'burden',      # kibehlap = be a burden
    'hotkhiat': 'save',      # kihotkhiat = be saved
    'thatlum': 'slay',       # kithatlum = be slain
    'lamdang': 'different',  # kilamdang = be different
    'tangval': 'young.man',  # tangvalte = young men
    'pil': 'learn',          # pilvang = be wise
    'mawh': 'guilty',        # Round 155: i mawh = we are guilty
    # Round 155: add commonly mis-segmented stems
    'zawng': 'poor',         # zawngkhal = wear.out
    'zawngkhal': 'tire.out', # tire/wear out
    'zanei': 'official',     # zanei = palace official/steward
    'zuihzawh': 'receive',   # zuihzawh = receive/accept (compound verb)
    'zuihkhak': 'obstruct',  # zuihkhak = obstruct following
    'zung': 'ring',          # zungbuh = signet ring
    'zungpi': 'chief.ring',  # large signet ring  
    'zungthuk': 'engraved.ring', # engraved ring
    'zukham': 'intoxicated', # zukhamna = drunkenness
    'zuauthei': 'liar',      # zuautheite = liars
    'zuauphuah': 'dark.saying', # understanding dark sentences
    'zelzel': 'repeatedly',  # again and again
    'zeek': 'account',       # give an account
    'zuahzuah': 'little.by.little', # reduplication meaning gradually
    'zualsakin': 'gradually', # another form
    'vum': 'breath',          # breath of
    'vokcing': 'swineherd',   # pig keeper
    'vankisut': 'proud',      # van-kisut = sky-lofty = proud
    'tuzaw': 'appointed.time', # at the appointed time
    'tuzawh': 'appointed.time', # variant
    'tunkhit': 'shut.in',     # trapped/enclosed
    'tunkhak': 'obstruct',    # block/obstruct
    'tulak': 'forest',        # wood country
    'ulenau': 'brethren',     # brothers/brethren
    'uplah': 'doubt',         # doubt
    'tuma': 'eloquent',       # able to speak
    'tukhang': 'this.generation', # from this generation
    'theu': 'cease',          # stop/satisfy
    'themcik': 'a.little',    # even a little
    'thawlpi': 'wine.vat',    # pressfat for wine
    'thawhbat': 'butter',     # smoother than butter
    'thanuam': 'diligent',    # hand of the diligent
    'thaneihteng': 'strength', # my strength
    'thakbawl': 'rejoice',    # rejoice over
    'tenkhak': 'dwell',       # sojourn/dwell
    'teeptum': 'drive.away',  # driven away
    'tawk': 'be.drunk',       # make drunk
    'tawizawh': 'spider',     # spider
    'tamkim': 'upright',      # uprightness
    'zongpa': 'wisdom',       # getteth wisdom
    'zingsol': 'morning.star', # morning star
    'uisan': 'glutton',       # winebibber/riotous eater
    'tuithuk': 'deep',        # the deep/abyss
    'tuikhukpi': 'pool',      # pools of water
    'tuikhu': 'fountain',     # fountain of the deep
    'tuibuak': 'water',       # water (verb - he that watereth)
    'tuatcil': 'trample',     # tread/trample
    'tuahpha': 'quickly',     # found so quickly
    'vatmai': 'defeat',       # discomfit
    'valkhong': 'redeem',     # redeem the time
    'vawhzo': 'pierce',       # nose pierceth
    'vekun': 'shut.up',       # cities shut up
    'velval': 'bitter',       # become bitter
    'zinleleeng': 'temperate', # self-controlled
    'zinkhia': 'wander',      # wander from
    'zineih': 'wed',          # wife of youth
    'zik': 'wife',            # variant of zi (wife)
    'ziauziau': 'go.about',   # gad about
    'zavei': 'reproof',       # reproof
    'zahzahun': 'feathered',  # feathered fowl
    'zahkona': 'distress',    # distress
    'tovang': 'dig',          # dig in the wall
    'tomlam': 'count',        # number our days
    'tokgawpin': 'divide',    # divided the sea
    'thusit': 'condemn',      # condemn him
    'thusel': 'resist',       # resist
    'thuphawk': 'wise',       # wise men
    'thupalsat': 'transgressor', # transgressors
    'thunem': 'restore',      # restore
    'thuksak': 'plead',       # plead the cause
    'thukpi': 'flood',        # upon the flood
    'thukihilh': 'reproof',   # reproof/instruction
    'thuahkhawm': 'gather',   # gathered (figs)
    'then': 'thousand',       # thousands of
    'theipuam': 'herb',       # manner of herbs
    'thangtat': 'honest',     # walk honestly
    'thaltawi': 'archer',     # archers hit him
    'thalsing': 'myrrh',      # smell of myrrh
    'thalpeu': 'bend',        # bend their tongues
}

# Noun stems - expanded from corpus frequency analysis
NOUN_STEMS = {
    # Divine/Religious (high frequency in Bible)
    'Pasian': 'God',         # 5,308
    'pasian': 'god',         # lowercase variant
    'Topa': 'Lord',          # 7,486
    'topa': 'lord',          # lowercase variant
    'biakna': 'worship',     # 1,236 biak-na
    'biakinn': 'temple',     # 741 biak-inn
    'siangtho': 'holy',      # 476
    'thupha': 'blessing',    # 479 thu-pha
    'mawhna': 'sin',         # 688 mawh-na
    'Lungdamna': 'gospel',   # 296 lungdam-na
    'nuntakna': 'life',      # 394 nuntak-na
    'thuciamna': 'promise',  # 374 thuciam-na
    'vangliatna': 'power',   # 282
    'thukham': 'law',        # 210
    
    # Social terms
    'mi': 'person',          # 4,221
    'mite': 'people',        # 6,569
    'minam': 'nation',       # 596
    'mihing': 'human',       # 354
    'kumpipa': 'king',       # 1,563
    'kumpi': 'king',
    'siampi': 'priest',      # 357
    'siampite': 'priests',   # 255
    'siampipa': 'high.priest', # 172
    'nasemte': 'servants',   # 389
    'nasempa': 'servant',
    'galte': 'enemies',
    'galkap': 'soldier',     # 233
    'galkapte': 'soldiers',
    'kamsang': 'prophet',
    'kamtai': 'messenger',
    'upa': 'elder',          # 162
    'upate': 'elders',
    'mihon': 'poor.person',  # 216
    'mihonte': 'poor.people',
    'midang': 'other.person', # 181
    'midangte': 'others',
    'migilo': 'enemy',       # 179
    'migilote': 'enemies',
    
    # Kinship
    'pa': 'father',          # 2,265
    'pate': 'fathers',
    'nu': 'mother',          # 619
    'tapa': 'son',           # 1,906
    'tapate': 'sons',        # 411
    'tanu': 'daughter',
    'tanute': 'daughters',
    'sanggam': 'brother',
    'sanggamte': 'brothers',
    'sanggampa': 'brother',  # 210
    'zi': 'wife',            # 339
    'pasal': 'husband',      # 359
    'mipa': 'man',
    'numei': 'woman',
    'numeite': 'women',      # 195
    'suanlekhak': 'genealogy', # 224
    'suanlekhakte': 'genealogies', # plural form
    'innkuan': 'household',  # 205
    
    # Body parts
    'khut': 'hand',          # 854
    'khutsung': 'palm',      # 158
    'mai': 'face',
    'maitang': 'forehead',   # 137
    'lungsim': 'heart',      # 957 lung-sim
    'kha': 'spirit',         # 748
    'sa': 'flesh',           # 573
    'lu': 'head',
    'ke': 'foot',
    'mit': 'eye',
    'bil': 'ear',
    'kam': 'mouth',           # kam = mouth (NOT ka)
    
    # Place/Location
    'gam': 'land',           # 2,586
    'gamte': 'lands',        # 173
    'khua': 'town',          # 919
    'khuapi': 'city',        # 1,050
    'khuapite': 'cities',    # 253
    'inn': 'house',          # 715
    'innte': 'houses',
    'mun': 'place',          # 820
    'mung': 'place',         # variant form
    'leitung': 'earth',      # 717
    'leitang': 'earth',      # 462 (variant)
    'vantung': 'heaven',     # 419
    'vantungmi': 'angel',    # 247
    'lampi': 'way',
    'van': 'sky',            # 227
    'mual': 'mountain',      # 283
    'mualtung': 'mountaintop', # 202
    'tuipi': 'sea',          # 270
    
    # Time terms
    'hun': 'time',           # 1,208
    'ni': 'day',             # 1,191
    'kum': 'year',           # 868
    'zan': 'night',
    'zing': 'morning',       # Round 155: add morning (prevents zi-ng mis-segmentation)
    'zingsang': 'morning',   # full form
    'tawntung': 'forever',   # 679
    'nisuah': 'birth.day',   # 169
    'khang': 'generation',   # 213
    
    # Abstract terms
    'thu': 'word',           # 5,516
    'thuthak': 'truth',
    'thuhilhna': 'teaching',
    'thupiak': 'commandment', # 241
    'thupiakna': 'commandment.NMLZ', # 184
    'tui': 'water',
    'aw': 'voice',
    'min': 'name',
    'nam': 'kind/tribe',     # 177
    'mawhnei': 'sinner',     # 24x - mawh (guilty/sin) + nei (have) = sin-having
    
    # Other common nouns
    'ngeina': 'knowledge',   # 327 ngei-na
    'siatna': 'destruction', # 350 siat-na
    'khialhna': 'sin',       # 328 khialh-na
    'gamtatna': 'kingdom',   # 300 gamtat-na
    'sihna': 'death',        # 268
    'deihna': 'desire',      # 244
    'pilna': 'learning',     # 227
    'hehpihna': 'wrath',     # 225
    'nasepna': 'work.NMLZ',  # 174
    'ngaihsutna': 'thought', # 175
    'ukna': 'rule.NMLZ',     # 138
    'upna': 'belief',        # 258
    'itna': 'love.NMLZ',     # 299
    'hoihna': 'goodness',    # 108
    'lum': 'warm',           # 149
    'puan': 'cloth',         # 168
    'puante': 'clothes',
    'beh': 'tribe',          # 173
    'behte': 'tribes',
    'omlai': 'dwelling',     # 236
    'lote': 'non-X',         # 230
    'milim': 'idol',         # 230
    'khuavak': 'light',      # 188
    'sakol': 'donkey',       # 155
    'anlum': 'food',         # 145
    'ganhing': 'animal',     # 164
    'ganhingte': 'animals',
    'sang': 'high',          # 209
    'nin': 'day',            # 200 variant
    'bawng': 'cattle',       # 31x + many compounds (bawngtal, bawngpi, etc.)
    'ganbuk': 'fold',        # animal fold/pen
    'kilungso': 'wait.patiently',  # rest in the LORD
    'phuang': 'upright',     # perfect/upright
    'kidona': 'sword',       # 56x - (not ki-don-a)
    
    # === Additional stems from corpus frequency analysis ===
    # Social/occupational
    'tangval': 'youth',       # tangvalte = youths
    'naupang': 'child',       # naupangte = children
    'luang': 'corpse',
    'nungak': 'girl',        # 73
    'tuuhon': 'poor.person', # tuuhonte
    'lute': 'heads',
    'mihoih': 'righteous',   # 70
    'mihai': 'wise',         # 89
    'misite': 'dead.PL',
    'misi': 'dead',          # 70
    'mihonpi': 'noble',      # mihonpite
    'siangthote': 'saints',
    
    # Nominalizations (productive -na pattern)
    'lamet': 'example',      # lametna = example.NMLZ
    'phattua': 'reward',     # phattuamna
    'haksat': 'difficult',   # haksatna
    'gualzawh': 'transgress', # gualzawhna
    'tawntung': 'eternity',  # tawntungna
    'mahmah': 'very',        # mahmahna
    'pian': 'birth',         # pianna
    'lut': 'enter',          # lutna
    'neih': 'have',          # neihna
    'muh': 'see',            # muhna
    'lau': 'fear',           # launa
    'kah': 'fight',          # kahna
    'lin': 'hope',           # lina
    'sik': 'repent',         # sikna
    'dik': 'straight',       # dikna
    'hat': 'strong',         # hatna
    'dal': 'hinder',         # dalna
    'buk': 'ambush',         # bukna
    
    # Places/locations
    'mailam': 'front',       # 64
    'mualtung': 'mountaintop', # mualtungah
    'zawl': 'open.space',    # zawlte
    'gamla': 'wilderness',   # 57
    
    # Body parts / objects
    'lukhu': 'crown',        # 59
    'kongzing': 'harp',      # 59
    'kammal': 'jawbone',     # 59
    'vatgawp': 'bird',       # 55
    'mittaw': 'blind',       # 47
    'sum': 'money',          # sumte
    'kent': 'cubit',         # kente
    'leeng': 'chariot',      # leengte = 68
    'bawngtal': 'ox',        # bawngtalte = oxen 212x
    'sabuai': 'sheep',       # 60
    'sawltak': 'servant',    # 56
    'khuaizu': 'locust',     # 60
    'nak': 'nose',           # 77x - "nostrils, nose" (NOT na-k!)
    'ngasa': 'fish',         # 62x - "fish"
    'lungsim': 'heart',      # 57x - "heart, bowels, inner being"
    
    # Action-related
    'khaici': 'sow',         # 58 (farmer)
    'kamsangpa': 'prophet',  # 58
    'vaihawm': 'counsel',    # 63
    'muanhuai': 'trust',     # 57
    'minthang': 'glory',     # 57
    'thusim': 'parable',     # 60
    'thuhoih': 'good.news',  # 47
    'laksak': 'redeem',      # 54
    'ninsak': 'strengthen',  # 52
    'lungdamsak': 'comfort', # 50
    'nusia': 'forsake',      # 50
    'musak': 'show',         # 46
    
    # Plurals (productive -te pattern)
    'sagih': 'seven',        # sagihte
    'sawmgiat': 'seventy',   # 55
    'zathum': 'three.hundred', # 52
    'zali': 'four.hundred',  # 51
    'zawsop': 'judge',       # 52
    'ukpi': 'governor',      # 53
    'siamte': 'craftsmen',
    'thupiakte': 'commandments',
    'ante': 'them',          # 50
    'pente': 'things',
    'khete': 'some',
    'khaute': 'which',
    'suangte': 'descendants',
    'bawlte': 'makers',
    'pute': 'ancestors',
    'taute': 'children',
    'vantungte': 'heavenly.beings',
    'humpinelkai': 'lion',   # 125x - "lion"
    'nuamsa': 'prosperous',  # 51x - "well, prosperous, at ease"
    
    # Miscellaneous high-frequency
    'ken': 'only',           # 112
    'panun': 'toward',       # 101
    'mudah': 'easy',         # 97
    'paisan': 'god',         # 91 variant spelling
    'annel': 'meal',         # 76
    'alang': 'side',         # 73 - NOT vine! "in the side thereof"
    'kangtum': 'brass',      # 72
    'kawm': 'edge',          # 70
    'keel': 'heel',          # 85
    'zaguk': 'winepress',    # 65
    'umcih': 'hope',         # 64
    'ihih': 'this.be',       # 64 = i-hih
    'letsong': 'gift',       # 76x - "gift, portion"
    'baih': 'early',         # 49x - "early" (in 'tho baih' = rise early)
    'cin': 'said',           # 61
    'kampau': 'voice',       # 61
    'hit': 'that',           # 61
    'khai': 'hold',          # 61
    'keu': 'dig',            # 59
    'maimang': 'shame',      # 59
    'khah': 'choke',         # 62
    'nakleh': 'otherwise',   # 56
    'hiang': 'know',         # 54
    'khialh': 'sin',         # 54
    'sau': 'long',           # 52
    'luppih': 'lay.down',    # 51
    'lungmuang': 'trust',    # 51
    'lunghimawh': 'fear',    # 51
    'samsia': 'destroy',     # 50
    'pianzia': 'nature',     # 50
    'gammi': 'citizen',      # 47
    'namkim': 'rainbow',     # 46
    'sauveipi': 'flock',     # 46
    'mipil': 'wise.person',  # 47
    'aksi': 'star',          # 48x - "star" (vana aksi = star of heaven)
    'lutang': 'duke/chief',  # 56x - "duke, chief"
    'ciatah': 'each',        # 48x - "each, every"
    'tuam': 'promise',       # base for phattuamna, tuamtuam
    'guh': 'bone',           # 44x - "bone" (guhte = bones)
    'liat': 'great',         # 44x - "great, much" (liatna = greatness)
    'kapin': 'among',        # 46x - "among, before" (came unto)
    'innkuanpih': 'household', # 46x - "household" (inn-kuan-pih)
    'khuampi': 'board/pillar', # 44x - "board, pillar" (architectural)
    'ngawng': 'neck',        # 43x - "neck"
    'ngaihno': 'beloved',    # 42x - "beloved" (O thou whom my soul loveth)
    'et': 'care',            # 41x - base for etna (caring, keeping)
    'nget': 'request',       # 41x - base for ngetna (request, petition)
    'kiman': 'profit',       # 41x - base for kimanna (profitable)
    'kimang': 'profit',      # 68x - variant of kiman (what profit)
    'maangmuh': 'vision',    # 42x - base for maangmuhna (vision)
    'tuikulh': 'island',     # 41x - "island, isles" (isles of the sea)
    'puantualpi': 'robe/coat',  # 40x - "coat of many colors"
    
    # === na- words that are NOT 2SG prefix! ===
    # These are independent lexemes, not na- + X
    'nasem': 'servant',      # 350x - "servant, young man" (NOT 2SG-serve)
    'nasia': 'severe',       # 60x - "severe, great, terrible" (NOT 2SG-bad)
    'nalamdang': 'miracle',  # 76x - "miracle, wonder, sign" (NOT 2SG-way-other)
    'naita': 'near',         # 36x - "near, approaching" (NOT 2SG-love)
    'natui': 'discharge',    # 22x - "bodily discharge, issue" (NOT 2SG-water)
    'naupa': 'younger.sibling', # 21x - "younger brother/sibling" (NOT 2SG-elder)
    'nakpi': 'night',        # 42x - "night" (NOT 2SG-big)
    
    # === Session 2: More noun stems from philological analysis ===
    'hiang': 'branch',       # 41x - "branch" (a hiangte = its branches)
    'ausan': 'scarlet',      # 39x - "scarlet (color)" (a ausan puante = scarlet cloths)
    'luanghawm': 'carcass',  # 39x - "carcass, corpse" (humpinelkai luanghawm = lion carcass)
    'gamkhing': 'desolate',  # 38x - "desolate, empty land"
    'bawngno': 'calf',       # 36x - "calf" (bawng = cow + no = child/young)
    'thumvei': 'three.times', # 36x - "three times" (thum + vei)
    'vakhu': 'dove',         # 35x - "dove"
    'khualzin': 'journey',   # 35x - "journey, travel" (khua + zin)
    'manna': 'manna',        # 35x - biblical manna (loanword)
    'cingtaak': 'dwarf',     # 35x - "dwarf, short person"
    
    # === Session 2: More nouns from philological analysis ===
    'kammal': 'word/speech', # 38x - "word, speech" (kammalte = words)
    'kampau': 'voice',       # used in kampauna (voice-NMLZ)
    'gamhluah': 'heir',      # 35x - "heir" (gam-hluah = land-inherit)
    'tunna': 'end/border',   # 35x - "end, border" (Jordan tunna = end of Jordan)
    'omzia': 'welfare',      # 34x - "welfare, condition" (om-zia = exist-manner)
    'tual': 'generation/place', # base for puantualpi
    
    # === Session 3: More nouns from philological analysis ===
    'kongkha': 'door',       # 38x - "door" (kongkhakte = doors)
    'pawl': 'group/allies',  # 33x - "group, companions, allies"
    'kauphe': 'locust',      # 33x - "locust" (kauphe hon = locusts)
    'beel': 'pan/bowl',      # 33x - "pan, bowl" (beelte = pans)
    'khak': 'offspring',     # 34x - "offspring, generation" (a khakte = his generations)
    'sunga': 'inside',       # 34x - "inside, in" (khuasunga = in the town)
    'sing': 'tree/wood',     # 33x - "tree, wood" (singte = trees)
    'singkung': 'tree',      # 32x - "tree" (singkungte = trees) - fuller form
    'nuam': 'pleased',       # 32x - "pleased, comfortable" (lungnuam = heart-pleased)
    'hon': 'flock/swarm',    # 31x - "flock, swarm" (honpi = great multitude)
    'khat': 'one',           # numeral "one"
    'lang': 'side',          # "side" (langkhat = one side, langpang = against)
    'mial': 'darkness',      # 31x - "darkness" (khua mial = darkness)
    'dang': 'other',         # "other" (nidang = day-other = before)
    'ham': 'full',           # "full" (khangham = full of years)
    'an': 'rice/food',       # 30x - "rice, food" (anlak = harvest)
    'nawi': 'butter',        # "butter" (bawngnawi = cow-butter)
    'kalaoh': 'camel',       # 30x - "camel" (kalaohte = camels)
    'liangko': 'shoulder',   # 29x - "shoulder"
    'phaknat': 'leprosy',    # 31x - "leprosy" (skin disease)
    'no': 'young',           # "young" (khangno = youngest)
    'aksi': 'star',          # 32x - "star" (aksite = stars)
    'aisan': 'magician',     # 29x - "magician, sorcerer"
    'ukpi': 'duke',          # 29x - "duke, chief"
    'lungtang': 'breastplate', # 29x - "breastplate" (lung-tang = heart-place)
    'sila': 'servant',       # 29x - "servant, slave"
    'zineu': 'concubine',    # 28x - "concubine" (zi-neu = wife-lesser)
    'lim': 'sign',           # 29x - "sign" (limte = signs)
    'mangbuh': 'barley',     # 28x - "barley"
    'kuang': 'trough/box',   # 28x - "trough, box" (kuangte = kneadingtroughs)
    'thau': 'fat',           # 27x - "fat" (thaute = fats)
    'thaltang': 'arrow',     # 27x - "arrow" (thaltangte = arrows)
    'cing': 'faithful',      # 33x - "faithful" (cingte = faithful ones)
    'si': 'die',             # verb "die" (si ding = shall die)
    'sim': 'count',          # 356x - verb "count, number"
    'silh': 'clothe',        # 116x - verb "clothe"
    'siang': 'holy',         # 114x - adjective "holy" (base of siangthosak)
    'lianpi': 'army',        # 27x - "army" (lianpite = armies)
    'peengkul': 'trumpet',   # 27x - "trumpet"
    'lai': 'tip/middle',     # 26x - "tip, middle" (laite = tips)
    'lasa': 'pillar',        # 26x - "pillar" (lasate = pillars)
    'sisan': 'blood',        # 135x - "blood"
    'laibu': 'book',         # 121x - "book" (laibu ahi hi = the book of)
    'silngo': 'meal/feast',  # 78x - "meal, feast" (unleavened bread context)
    
    # === Session 6 Round 11: Allomorph audit additions ===
    # Stems needed to prevent over-segmentation with -te suffix
    'hing': 'alive',         # hingte = alive-PL
    'vun': 'skin',           # vunte = skin-PL
    'thal': 'bow',           # thalte = bow-PL (weapon)
    'taneu': 'child.small',  # taneute = little ones
    'teipi': 'spear',        # teipite = spears
    'hisak': 'proud',        # kihisakte = proud ones
    'gial': 'spotted',       # gialte = spotted ones
    'anpal': 'firstfruit',   # anpalte = firstfruits
    'vanglian': 'mighty',    # vangliante = mighty ones
    'pawi': 'feast',         # pawite = feasts
    'delh': 'overcome',      # delhte = conquerors  
    'zuak': 'sell',          # zuakte = sellers
}

# Proper nouns (don't gloss with lowercase - return as-is with uppercase marker)
# Expanded from corpus frequency analysis - 200+ entries
PROPER_NOUNS = {
    # Jesus and titles
    'Jesuh', 'Jesus', 'Khrih', 'Christ', 'Kristu', 'Zeisu', 'Khrih',
    
    # Old Testament figures - Patriarchs
    'Abraham', 'Abram', 'Isaac', 'Jakob', 'Jakobu', 'Israel', 'Josef', 'Joseph',
    'Noah', 'Adam', 'Eve', 'Seth', 'Enoch', 'Methuselah', 'Lamech',
    'Sarah', 'Sarai', 'Rebekah', 'Leah', 'Rachel',  # Matriarchs
    'Issakhar', 'Issachar', 'Reuben', 'Simeon', 'Levi', 'Judah', 'Zebulun',  # Tribes
    
    # Old Testament - Moses era
    'Moses', 'Aaron', 'Joshua', 'Caleb', 'Miriam', 'Korah', 'Phinehas',
    
    # Old Testament - Judges & Kings
    'David', 'Solomon', 'Saul', 'Samuel', 'Eli', 'Gideon', 'Samson',
    'Jeroboam', 'Rehoboam', 'Ahab', 'Jehoshafat', 'Hezekiah', 'Josiah',
    'Nebukhadnezzar', 'Nebuchadnezzar', 'Belshazzar', 'Darius', 'Cyrus',
    'Abimelek', 'Abimelech', 'Abner', 'Absalom', 'Joab', 'Jonathan',
    
    # Old Testament - Prophets
    'Elijah', 'Elisha', 'Isaiah', 'Jeremiah', 'Ezekiel', 'Daniel',
    'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum',
    'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi',
    'Nathan', 'Zadok',
    
    # Old Testament - Other figures
    'Job', 'Esau', 'Levi', 'Reuben', 'Benjamin', 'Judah', 'Manasseh',
    'Efraim', 'Ephraim', 'Gad', 'Simeon', 'Naphtali', 'Naftali', 'Asher',
    'Zebulun', 'Issachar', 'Dan', 'Ishmael', 'Ruth', 'Boaz', 'Rahab',
    
    # New Testament figures - Apostles
    'Johan', 'John', 'Peter', 'Piter', 'Paul', 'Paulus', 'Simon', 'Andru', 'Andrew',
    'James', 'Zebedi', 'Zebedee', 'Matthew', 'Mark', 'Luke', 'Thomas', 'Philip',
    'Bartholomew', 'Judas', 'Thaddaeus', 'Matthias',
    
    # New Testament - Other figures  
    'Maria', 'Mary', 'Martha', 'Lazarus', 'Nicodemus', 'Stephen', 'Stefanus',
    'Timothy', 'Titus', 'Barnabas', 'Silas', 'Apollos', 'Priscilla', 'Aquila',
    'Pilat', 'Pilate', 'Herod', 'Caiaphas', 'Annas',
    
    # Places - Old Testament
    'Egypt', 'Babylon', 'Jerusalem', 'Judah', 'Samaria', 'Damaskas', 'Damascus',
    'Moab', 'Edom', 'Ammon', 'Syria', 'Assiria', 'Assyria', 'Kanaan', 'Canaan',
    'Gilead', 'Zion', 'Sinai', 'Horeb', 'Bethel', 'Bethlehem', 'Ai',
    'Jordan', 'Filistia', 'Philistia', 'Khaldea', 'Chaldea',
    'Midian', 'Persia', 'Media', 'Sheba',
    
    # Places - New Testament
    'Galilee', 'Nazareth', 'Nazaret', 'Kapernaum', 'Capernaum',
    'Roma', 'Rome', 'Corinth', 'Ephesus', 'Antioch', 'Athens',
    'Macedonia', 'Galatia', 'Thessalonica', 'Judea', 'Tarsus',
    
    # Groups/Peoples
    'Jew', 'Farisi', 'Pharisee', 'Sadducee', 'Gentail', 'Gentile',
    'Levite', 'Pawi', 'Faro', 'Pharaoh', 'Kherub', 'Cherub', 'Satan',
    'Amor', 'Amorite', 'Hittite', 'Midianite',
    
    # Lowercase forms found in corpus (need to match case-insensitively)
    'israel', 'jesuh', 'jerusalem', 'egypt', 'babylon', 'judah',
    'saul', 'aaron', 'abraham', 'paul', 'kanaan', 'ammon', 'assiria',
    'samuel', 'sabbath', 'isaac', 'absalom', 'zion', 'samaria', 'ahab',
    'nebukhadnezzar', 'abimelek', 'abner', 'abram', 'isaiah', 'ishmael',
    'damaskas', 'zadok', 'pilat', 'satan', 'naftali', 'khaldea',
    'gentail', 'filistia', 'amor', 'kherub', 'ai',
    # Additional proper nouns from corpus frequency analysis
    'ahaz', 'samson', 'midian', 'amalek', 'asher', 'nathan', 'saihadial',
    'moab', 'edom', 'gilead', 'sheba', 'laban', 'rebekah', 'leah', 'rachel',
    'bethel', 'sodom', 'gomorrah', 'nineveh', 'tyre', 'sidon',
    # Proper names starting with 'ba-' (must not be analyzed as ba + X)
    'baal', 'balaam', 'bashan', 'babylon', 'barnabus', 'barnabas',
    'bathsheba', 'barak', 'barabbas', 'baruch', 'belshazzar', 'benhadad',
    'bethlehem', 'beersheba', 'beelzebub', 'belial',
    # Additional proper names from residual analysis
    'balak', 'zippor', 'mizpah', 'azariah', 'zadok', 'nathan',
}

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def clean_word(word: str) -> str:
    """Remove punctuation from word, including quotes at word boundaries.
    Note: Interior and trailing apostrophes (both ' and ') are preserved as they are meaningful in Tedim.
    Examples: keima-a' (1SG.self.GEN), ke'n (1SG.PRO), Topa' (Lord's)
    """
    # Handle curly quotes (", ", ', ') and other Unicode punctuation
    # Leading: remove quotes, brackets including leading apostrophes that are quote marks
    word = re.sub(r'^["\u201c\u201d\u2018\u2019\'\[\(\xab\u201e]+', '', word)
    # Trailing: remove punctuation, double quotes, brackets
    # Also remove apostrophe/curly quote when preceded by comma/punctuation (closing quotes)
    # Pattern: word,'\n or word,"
    word = re.sub(r',["\'\u2018\u2019\u201c\u201d]+$', '', word)  # Remove ,' or ," at end
    word = re.sub(r'\?["\'\u2018\u2019]+$', '?', word)  # Keep ? but remove trailing quote
    word = re.sub(r'!["\'\u2018\u2019]+$', '', word)  # Remove !' or !" at end (exclamation + quote)
    word = re.sub(r'[.,;:!?\u201c\u201d"\)\]\xbb]+$', '', word)  # Remove other trailing punct
    return word


def disambiguate_morpheme(morpheme: str, context: dict) -> str:
    """
    Disambiguate an ambiguous morpheme based on context.
    
    This function implements contextual disambiguation for polysemous morphemes.
    It examines the morphological and syntactic context to select the most
    appropriate meaning from the AMBIGUOUS_MORPHEMES dictionary.
    
    Args:
        morpheme: The morpheme to disambiguate (lowercase)
        context: Dictionary with contextual information. Recognized keys:
            - 'position': Where in word ('standalone', 'prefix', 'suffix', 'stem')
            - 'prev_morpheme': The morpheme before this one (e.g., 'kum' for numbers)
            - 'next_morpheme': The morpheme after this one
            - 'has_prefix': True if word has prefix (ka-, na-, a-, ki-, etc.)
            - 'has_suffix': True if word has suffix (-te, -na, -in, etc.)
            - 'has_ki_prefix': True if word specifically has ki- (reflexive)
            - 'in_compound': True if part of compound word
    
    Returns:
        str: The appropriate gloss for this context, or None if morpheme
        is not in AMBIGUOUS_MORPHEMES.
    
    Examples:
        >>> disambiguate_morpheme('za', {'position': 'standalone'})
        'hear'
        >>> disambiguate_morpheme('za', {'prev_morpheme': 'kum'})
        'hundred'
        >>> disambiguate_morpheme('vei', {'prev_morpheme': 'khat'})
        'time'
        >>> disambiguate_morpheme('kham', {'has_ki_prefix': True})
        'forbid'
    
    Rule Priority:
        1. Specific contextual triggers (prev_morpheme matches known pattern)
        2. Morphological context (has_prefix, has_suffix)
        3. Default meaning (most common in corpus)
    """
    if morpheme not in AMBIGUOUS_MORPHEMES:
        return None
    
    meanings = AMBIGUOUS_MORPHEMES[morpheme]
    
    # Apply disambiguation rules
    if morpheme == 'za':
        # 'hundred' after kum/sawm or in number context
        if context.get('prev_morpheme') in ('kum', 'sawm', 'tul'):
            return 'hundred'
        # 'hear' with verbal morphology
        if context.get('has_prefix') or context.get('has_suffix'):
            return 'hear'
        # Default: check if followed by tul (thousand)
        if context.get('next_morpheme') == 'tul':
            return 'hundred'
        return 'hear'  # Default to verbal meaning
    
    elif morpheme == 'la':
        # 'and.SEQ' after imperative hen
        if context.get('prev_morpheme') == 'hen':
            return 'and.SEQ'
        # 'take' with verbal morphology (la-in, etc.)
        if context.get('has_suffix') or context.get('has_prefix'):
            return 'take'
        return 'take'  # Default to verbal meaning
    
    elif morpheme == 'na':
        # 'NMLZ' when used as suffix
        if context.get('position') == 'suffix':
            return 'NMLZ'
        # '2SG' when standalone or prefix
        return '2SG'
    
    elif morpheme == 'pa':
        # 'NMLZ.AG' when suffix on verb
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'NMLZ.AG'
        return 'father'
    
    elif morpheme == 'man':
        # Check frozen form manin
        if context.get('in_compound') == 'manin':
            return 'reason'
        # 'finish' with khit
        if context.get('next_morpheme') == 'khit':
            return 'finish'
        return 'finish'  # Default
    
    elif morpheme == 'hang':
        # Almost always 'reason' in Biblical text
        return 'reason'
    
    elif morpheme == 'vei':
        # 'time' after numerals
        if context.get('prev_morpheme') in ('khat', 'nih', 'thum', 'li', 'nga', 'guk', 'sagih', 'giat', 'sawmle'):
            return 'time'
        # 'wave' when has verbal suffix (-a piak pattern = wave offering)
        if context.get('has_suffix'):
            return 'wave'
        return 'sick'
    
    elif morpheme == 'pha':
        # 'good' when used as suffix (thu-pha = blessing)
        if context.get('has_prefix') or context.get('position') == 'suffix':
            return 'good'
        # 'branch' as standalone noun
        return 'branch'
    
    elif morpheme == 'kham':
        # 'forbid' with ki- prefix (kikham = refrain)
        if context.get('has_ki_prefix'):
            return 'forbid'
        # 'gold' as standalone noun
        return 'gold'
    
    elif morpheme == 'hi':
        # 'be' (copula) when preceded by subject prefix
        if context.get('has_prefix'):
            return 'be'
        # 'DECL' sentence-finally (standalone)
        return 'DECL'
    
    elif morpheme == 'sa':
        # 'PERF' after verb stems
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'PERF'
        # 'flesh' as noun
        return 'flesh'
    
    elif morpheme == 'ta':
        # 'PFV' after verbs (aspect marker)
        if context.get('position') == 'suffix' and context.get('prev_is_verb'):
            return 'PFV'
        # 'child' in nominal compounds (ta-pa, ta-nu)
        return 'child'
    
    elif morpheme == 'tung':
        # 'on' when followed by -ah
        if context.get('next_morpheme') == 'ah':
            return 'on'
        # 'arrive' as verb
        if context.get('has_prefix'):
            return 'arrive'
        return 'on'  # Default to relational noun
    
    # Default: return first meaning
    return meanings[0][0] if meanings else None


def is_proper_noun(word: str) -> bool:
    """Check if word is a proper noun (case-insensitive matching)."""
    clean = clean_word(word)
    if not clean:
        return False
    # Check both original case and lowercase
    return clean in PROPER_NOUNS or clean.lower() in PROPER_NOUNS or clean[0].isupper()


# =============================================================================
# PHRASE BOUNDARY DETECTION (Henderson 1965)
# =============================================================================
#
# Henderson identifies three phrase types in Tedim Chin:
# 1. Subjective phrase: Subject NP (pronominal concord with following verb)
# 2. Predicative phrase: Verb phrase (final in conclusive sentences)
# 3. Adjunctive phrase: Non-subject NP, adverbial
#
# NP boundaries are marked by:
# - Case suffixes: -in (ERG), -ah (LOC), -tawh (COM)
# - Postpositions: panin (ABL), sangin (COMP), dong (TERM)
# - Plural marker: -te (often phrase-final in NPs)
# - Topic/focus: pen (TOP), zong (INCL), bek (RESTR)
#
# =============================================================================

# Phrase boundary markers (suffixes and particles that close NPs)
PHRASE_BOUNDARY_SUFFIXES = {
    'in': 'ERG',      # Ergative (transitive subject)
    'ah': 'LOC',      # Locative
    'tawh': 'COM',    # Comitative 'with'
    'pen': 'TOP',     # Topic marker
    'te': 'PL',       # Plural (often NP-final)
    'uh': 'PL.AGR',   # Plural agreement (VP marker)
}

PHRASE_BOUNDARY_WORDS = {
    'panin': 'ABL',     # Ablative 'from'
    'sangin': 'COMP',   # Comparative 'than'
    'dong': 'TERM',     # Terminative 'until'
    'tungah': 'on-LOC',
    'sungah': 'inside-LOC',
    'kiangah': 'beside-LOC',
    'lakah': 'among-LOC',
    'maitung': 'before',
}


def is_phrase_boundary(word: str, gloss: str) -> bool:
    """
    Check if a word marks a phrase boundary.
    
    Args:
        word: The word form
        gloss: The analyzed gloss
        
    Returns:
        True if this word ends a phrase (NP or VP)
    """
    word_lower = word.lower().rstrip('.,;:!?"\'')
    
    # Check if word itself is a boundary marker
    if word_lower in PHRASE_BOUNDARY_WORDS:
        return True
    
    # Check if gloss ends with a boundary suffix
    for suffix in PHRASE_BOUNDARY_SUFFIXES:
        if gloss.endswith(suffix) or gloss.endswith(PHRASE_BOUNDARY_SUFFIXES[suffix]):
            return True
    
    # Sentence-final particles
    if gloss in ('DECL', 'Q', 'IMP', 'HORT'):
        return True
    
    return False


def analyze_sentence(sentence: str) -> list:
    """
    Analyze a sentence and return word-by-word analysis with phrase boundaries.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of tuples: (word, segmentation, gloss, is_boundary)
    """
    results = []
    words = sentence.split()
    
    for word in words:
        seg, gloss = analyze_word(word)
        boundary = is_phrase_boundary(word, gloss)
        results.append((word, seg, gloss, boundary))
    
    return results


def chunk_sentence(sentence: str) -> list:
    """
    Chunk a sentence into phrases based on boundary markers.
    
    Args:
        sentence: A string of space-separated words
        
    Returns:
        List of phrases, where each phrase is a list of (word, seg, gloss) tuples
    """
    analysis = analyze_sentence(sentence)
    phrases = []
    current_phrase = []
    
    for word, seg, gloss, is_boundary in analysis:
        current_phrase.append((word, seg, gloss))
        if is_boundary:
            phrases.append(current_phrase)
            current_phrase = []
    
    # Add any remaining words as final phrase
    if current_phrase:
        phrases.append(current_phrase)
    
    return phrases


def analyze_word(word: str) -> Tuple[str, str]:
    """
    Analyze a Tedim word and return (segmentation, gloss).
    
    Returns:
        Tuple of (segmented_form, gloss)
        e.g., ("a-pai", "3SG-go")
    """
    original = word
    word = clean_word(word)
    
    if not word:
        return ('', '')
    
    # Normalize curly apostrophes to straight apostrophes for dictionary lookups
    word = word.replace('\u2019', "'").replace('\u2018', "'")
    
    # Normalize hyphens - try without hyphens first for morphological analysis
    # This handles cases like 'ki-ap' vs 'kiap', 'pua-in' vs 'puain'
    word_no_hyphen = word.replace('-', '')
    
    # Check function words FIRST (before proper noun check)
    # This ensures 'Tua' (sentence-initial 'that') isn't treated as proper noun
    word_lower = word.lower()
    word_no_hyphen_lower = word_no_hyphen.lower()
    
    # Check for ambiguous morphemes FIRST - use context-appropriate meaning
    # For standalone words, use default (first) meaning from AMBIGUOUS_MORPHEMES
    if word_lower in AMBIGUOUS_MORPHEMES:
        # Standalone word - use context-based disambiguation
        # For 'za' standalone, prefer 'hear' (more common in Bible)
        # For 'la' standalone, prefer 'take' (most common)
        # For 'na' standalone, prefer '2SG' (suffix handled separately)
        meaning = disambiguate_morpheme(word_lower, {'position': 'standalone'})
        if meaning:
            return (word, meaning)
    
    # Try both hyphenated and unhyphenated forms (also check original case for sentence-initial words)
    if word in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word])
    if word_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_lower])
    if word_no_hyphen_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_no_hyphen_lower])
    
    # Check if proper noun (only AFTER function words check)
    if is_proper_noun(word):
        return (word, word.upper())
    
    # Check for proper noun + suffix patterns (israel-te, jerusalem-ah, etc.)
    proper_suffixes = {
        '-te': 'PL',      # plural
        '-ah': 'LOC',     # locative  
        '-a': 'LOC',      # short locative
        '-in': 'ERG',     # ergative
        'te': 'PL',       # without hyphen
        'ah': 'LOC',      # without hyphen
    }
    for suffix, gloss in sorted(proper_suffixes.items(), key=lambda x: -len(x[0])):
        if word_lower.endswith(suffix):
            base = word[:-len(suffix)]
            base_clean = base.rstrip('-')  # Remove trailing hyphen if present
            if base_clean.lower() in PROPER_NOUNS or base_clean in PROPER_NOUNS:
                return (f"{base_clean}-{suffix.lstrip('-')}", f"{base_clean.upper()}-{gloss}")
    
    # Handle possessive marker ' or ' (curly quote) at end of word
    # Common pattern: Topa' = "Lord's", mite' = "people's", pa' = "father's"
    if word.endswith("'") or word.endswith("\u2019"):
        base = word.rstrip("'\u2019")
        base_lower = base.lower()
        # Check if base is a known word
        if base_lower in FUNCTION_WORDS:
            return (word, FUNCTION_WORDS[base_lower] + '.POSS')
        if base_lower in NOUN_STEMS:
            return (f"{base}'", f"{NOUN_STEMS[base_lower]}.POSS")
        if base.lower() in PROPER_NOUNS or base in PROPER_NOUNS:
            return (f"{base}'", f"{base.upper()}.POSS")
        # Check if it's a compound that ends in a known stem
        # e.g., mite' -> mi-te -> person-PL -> person.PL.POSS
        if base_lower.endswith('te') and len(base_lower) > 2:
            stem = base_lower[:-2]
            if stem in NOUN_STEMS:
                return (f"{base}'", f"{NOUN_STEMS[stem]}-PL.POSS")
        # Common possessive words
        poss_map = {
            'amau': '3PL.POSS',
            'mite': 'people.POSS',
            'note': '2PL.POSS',
            'amaute': '3PL.POSS',
            'kumpipa': 'king.POSS',
            'pa': 'father.POSS',
            'kei': '1SG.POSS',
            'kote': '1PL.POSS',
            'eite': '1PL.EXCL.POSS',
            'khempeuh': 'all.POSS',
            'nu': 'mother.POSS',
            'nang': '2SG.POSS',
            'dangte': 'other-PL.POSS',
            'minamte': 'nation-PL.POSS',
            'mipa': 'man.POSS',
            'mihingte': 'human-PL.POSS',
            'galte': 'enemy-PL.POSS',
            'pate': 'father-PL.POSS',
            'tate': 'child-PL.POSS',
            'tapate': 'son-PL.POSS',
            'nasemte': 'servant-PL.POSS',
            'khempeuhte': 'all-PL.POSS',
            'uliante': 'elder-PL.POSS',
            'tuate': 'DIST-PL.POSS',
            'man': 'price.POSS',
            'pasian-te': 'god-PL.POSS',
            'langpan': 'side.POSS',
            # Added Round 126: common apostrophe forms
            'zahtakte': 'honor-PL.POSS',
            'vasate': 'bird-PL.POSS',
            'paktatte': 'harlot-PL.POSS',
            'theite': 'fruit-PL.POSS',
            'tuangte': 'chariot-PL.POSS',
            'dingte': 'light-PL.POSS',
            'thatte': 'kill-PL.POSS',
            'tuamtuamte': 'various-PL.POSS',
            'tanaute': 'children-PL.POSS',
            'sisate': 'unclean-PL.POSS',
            'miliante': 'great.men-PL.POSS',
            'siamgante': 'weaver-PL.POSS',
            'khanghamte': 'old-PL.POSS',
            'nungzuite': 'follower-PL.POSS',
            'pawlpite': 'church-PL.POSS',
            'mipi': 'great.person.POSS',
            'sipa': 'dead.POSS',
            'maiman': 'face.POSS',
            'lungzin': 'brightness.POSS',
            'zawn': 'north.POSS',
            'u': 'elder.sibling.POSS',
            'kan': '1SG.POSS',
            'unu': 'sibling.POSS',
            'tonu': 'mistress.POSS',
            'vasa': 'bird.POSS',
            'koihpa': 'setter.POSS',
            'satpa': 'smiter.POSS',
            'behpa': 'captive.POSS',
            'amahmah': '3SG.EMPH.POSS',
            'thumante': 'faithful-PL.POSS',
            'sawmngate': 'fifty-PL.POSS',
            'sawmnihte': 'twenty-PL.POSS',
            'nazatte': 'artificer-PL.POSS',
            # Added Round 127: more possessive forms
            'naungek': 'birth.POSS',
            'mi': 'person.POSS',
            'no': 'young.POSS',
            'lui': 'head.POSS',
            'nomau': '2PL.POSS',
            'note-a': '2PL.GEN',
            'nomau-a': '2PL.GEN',
            'amaute-a': '3PL.GEN',
            'mi-a': 'person.GEN',
            'pa-a': 'father.GEN',
            'no-a': 'young.GEN',
            'hileh!': 'if.EMPH',
        }
        if base_lower in poss_map:
            return (word, poss_map[base_lower])
        
        # Round 154: Handle -te' (PL.POSS) with recursive analysis
        # e.g., biate' -> bia-te' -> worship-PL.POSS
        if base_lower.endswith('te') and len(base_lower) > 2:
            stem = base_lower[:-2]
            # Try to analyze the stem
            if stem in VERB_STEMS:
                return (f"{stem}-te'", f"{VERB_STEMS[stem]}-PL.POSS")
            if stem in NOUN_STEMS:
                return (f"{stem}-te'", f"{NOUN_STEMS[stem]}-PL.POSS")
            # Try full recursive analysis of stem
            stem_seg, stem_gloss = analyze_word(stem)
            if '?' not in stem_gloss:
                return (f"{stem_seg}-te'", f"{stem_gloss}-PL.POSS")
        
        # Round 154: Handle -pa' (NMLZ.AG.POSS) with recursive analysis
        # e.g., veipa' -> vei-pa' -> do-NMLZ.AG.POSS
        if base_lower.endswith('pa') and len(base_lower) > 2:
            stem = base_lower[:-2]
            if stem in VERB_STEMS:
                return (f"{stem}-pa'", f"{VERB_STEMS[stem]}-NMLZ.AG.POSS")
            stem_seg, stem_gloss = analyze_word(stem)
            if '?' not in stem_gloss:
                return (f"{stem_seg}-pa'", f"{stem_gloss}-NMLZ.AG.POSS")
    
    # Round 154: Early reduplication check (X-X patterns like hathat, kilhkilh)
    word_clean = word.lower().replace('-', '')
    half_len = len(word_clean) // 2
    if len(word_clean) >= 4 and len(word_clean) % 2 == 0:
        first_half = word_clean[:half_len]
        second_half = word_clean[half_len:]
        if first_half == second_half:
            # Check if base is a known stem
            if first_half in VERB_STEMS:
                return (f"{first_half}~{first_half}", f"{VERB_STEMS[first_half]}~RED")
            elif first_half in NOUN_STEMS:
                return (f"{first_half}~{first_half}", f"{NOUN_STEMS[first_half]}~RED")
            # Try lexicon lookup for base
            lex_gloss = lookup_lexicon(first_half)
            if lex_gloss:
                return (f"{first_half}~{first_half}", f"{lex_gloss}~RED")
    
    # Check common compounds - EXPANDED from corpus frequency analysis
    COMPOUND_WORDS = {
        # === Noun + LOC Compounds (very common pattern) ===
        'sungah': ('sung-ah', 'inside-LOC'),
        'tungah': ('tung-ah', 'on-LOC'),
        'kiangah': ('kiang-ah', 'beside-LOC'),
        'tangtungah': ('tangtung-ah', 'upon-LOC'),
        'maih': ('mai-ah', 'front-LOC'),  # contracted
        'lai-ah': ('lai-ah', 'midst-LOC'),
        'lakah': ('lak-ah', 'among-LOC'),
        'munah': ('mun-ah', 'place-LOC'),
        'innah': ('inn-ah', 'house-LOC'),
        'khuaah': ('khua-ah', 'town-LOC'),
        'gamah': ('gam-ah', 'land-LOC'),
        'vantungah': ('vantung-ah', 'heaven-LOC'),
        'leitungah': ('leitung-ah', 'earth-LOC'),
        'khuapi-ah': ('khuapi-ah', 'city-LOC'),  # hyphenated city
        'tawpna-ah': ('tawpna-ah', 'end.NMLZ-LOC'),  # end/latter
        
        # === Religious vocabulary ===
        'biakbuk': ('biak-buk', 'worship-tent'),  # 112x - sanctuary/tabernacle
        'vei-a': ('vei-a', 'wave-LOC'),    # wave offering (vei-a piak/biakna)
        'veia': ('vei-a', 'wave-LOC'),     # unhyphenated form
        
        # === Verb + Quotative Compounds ===
        'ci-in': ('ci-in', 'say-QUOT'),
        'cih': ('ci-h', 'say-NOM'),  # nominalized
        'ciin': ('ci-in', 'say-QUOT'),
        'a ci hi': ('a ci hi', '3SG say DECL'),
        
        # === TAM Compounds ===
        'dingin': ('ding-in', 'PROSP-ERG'),
        'nadingun': ('na-ding-un', '2SG-PROSP-IMP'),
        'adingin': ('a-ding-in', '3SG-PROSP-ERG'),
        'kadingin': ('ka-ding-in', '1SG-PROSP-ERG'),
        'ading': ('a-ding', '3SG-PROSP'),
        'kading': ('ka-ding', '1SG-PROSP'),
        'tungta': ('tung-ta', 'arrive-PFV'),
        'kipanta': ('ki-pan-ta', 'REFL-begin-PFV'),
        'om ta': ('om ta', 'exist PFV'),
        
        # === Verb + NMLZ Compounds (very productive) ===
        'thuhilhna': ('thu-hilh-na', 'word-teach-NMLZ'),
        'mawhna': ('mawh-na', 'err-NMLZ'),
        'nuntakna': ('nuntak-na', 'live-NMLZ'),
        'thuciamna': ('thuciam-na', 'promise-NMLZ'),
        'siatna': ('siat-na', 'destroy-NMLZ'),
        'khialhna': ('khialh-na', 'wrong-NMLZ'),
        'ngeina': ('ngei-na', 'know-NMLZ'),
        'gamtatna': ('gamtat-na', 'rule.land-NMLZ'),
        'biakna': ('biak-na', 'worship-NMLZ'),
        'vangliatna': ('vangliat-na', 'strong-NMLZ'),
        'lungdamna': ('lungdam-na', 'rejoice-NMLZ'),
        'damna': ('dam-na', 'well-NMLZ'),
        'kingaihna': ('ki-ngaih-na', 'REFL-desire-NMLZ'),
        'kisikna': ('ki-sik-na', 'REFL-turn-NMLZ'),
        
        # === Noun + Noun Compounds ===
        'tapa': ('ta-pa', 'child-male'),
        'tanu': ('ta-nu', 'child-female'),
        'biakinn': ('biak-inn', 'worship-house'),
        'khuapi': ('khua-pi', 'village-big'),
        'leitung': ('lei-tung', 'land-on'),
        'leitang': ('lei-tang', 'land-?'),
        'vantung': ('van-tung', 'sky-on'),
        'lungsim': ('lung-sim', 'stone-mind'),
        'minam': ('mi-nam', 'person-kind'),
        'kumpipa': ('kumpi-pa', 'king-male'),
        'nasempa': ('nasem-pa', 'work.serve-male'),
        'thupha': ('thu-pha', 'word-good'),
        'thuthak': ('thu-thak', 'word-true'),
        
        # === Reflexive/Middle Compounds ===
        'kibawl': ('ki-bawl', 'REFL-make'),
        'kibang': ('ki-bang', 'REFL-same'),
        'kipan': ('ki-pan', 'REFL-begin'),
        'kisai': ('ki-sai', 'REFL-concern'),
        'kisik': ('ki-sik', 'REFL-turn'),
        'kituah': ('ki-tuah', 'REFL-meet'),
        'kikhen': ('ki-khen', 'REFL-divide'),
        'kigelhna': ('ki-gelh-na', 'REFL-write-NMLZ'),
        'kipankhia': ('ki-pan-khia', 'REFL-begin-exit'),
        'kihongin': ('ki-hong-in', 'REFL-open-ERG'),
        'kikhel': ('ki-khel', 'REFL-differ'),
        'kipawlna': ('ki-pawl-na', 'REFL-associate-NMLZ'),  # 35x - association
        'kitotna': ('ki-tot-na', 'REFL-cut-NMLZ'),  # 35x - separation
        
        # === Household/Family Compounds ===
        'innkuanpihte': ('innkuanpih-te', 'household-PL'),  # 46x
        'kiphatsakna': ('ki-phatsak-na', 'REFL-glorify-NMLZ'),  # 45x - pride/selfwill
        
        # === Session 2: More compounds from philological analysis ===
        'hiangte': ('hiang-te', 'branch-PL'),  # 41x
        'hingkik': ('hing-kik', 'live-ITER'),  # 40x - "revive, live again"
        'ngahtheih': ('ngah-theih', 'get-ABIL'),  # 40x - "be able to get, obtainable"
        'hithiat': ('hi-thiat', 'be-quiet'),  # 39x - "be quiet, hold peace"
        'hoihpen': ('hoih-pen', 'good-TOP'),  # 37x - "the good (of), best part"
        'nitakin': ('ni-tak-in', 'day-exact-ERG'),  # 35x - "at evening, at dusk"
        'pulnatna': ('pul-nat-na', 'fear-very-NMLZ'),  # 36x - great fear
        'ngimna': ('ngim-na', 'think-NMLZ'),  # 35x - thought
        'haina': ('hai-na', 'possess-NMLZ'),  # 38x - possession
        
        # === Session 2: More compounds ===
        'kantanin': ('kantan-in', 'cross.over-ERG'),  # 44x - "flying across"
        'kammalte': ('kammal-te', 'word-PL'),  # 38x - "words"
        'kampauna': ('kampau-na', 'voice-NMLZ'),  # 38x - "voice, saying"
        'lasaknate': ('lasak-na-te', 'take.CAUS-NMLZ-PL'),  # 39x - "songs"
        'cial': ('ci-al', 'say-must'),  # 37x - "must say, should say"
        'pial': ('pi-al', 'give-must'),  # 36x - "must give"
        'zaksa': ('zak-sa', 'hear-PL.POSS'),  # 35x - "their hearing"
        'awk': ('awk', 'ram'),  # 35x - "ram" (standalone noun)
        'vet': ('vet', 'do'),  # 35x - base verb
        'vawh': ('vawh', 'name'),  # 34x - "name" (a vawh = named)
        'puantualpi': ('puan-tual-pi', 'cloth-many.colored-big'),  # 39x - Joseph's coat
        'khutnuaiah': ('khut-nuai-ah', 'hand-below-LOC'),  # 35x - "under the hand of"
        
        # === Causative Compounds ===
        'paisak': ('pai-sak', 'go-CAUS'),
        'damsak': ('dam-sak', 'well-CAUS'),
        'suaksak': ('suak-sak', 'become-CAUS'),
        'maisak': ('mai-sak', 'face-CAUS'),
        'kumsuk': ('kum-suk', 'bow-CAUS'),
        'sepsak': ('sep-sak', 'work-CAUS'),  # 35x - "make to work, serve"
        
        # === Applicative Compounds ===
        'paipih': ('pai-pih', 'go-APPL'),
        'honpih': ('hon-pih', 'come-APPL'),
        
        # === Aspectual/Directional Compounds ===
        'thawhkhiat': ('thawh-khiat', 'rise-emerge'),
        'honkhia': ('hon-khia', 'come-exit'),
        'paikhia': ('pai-khia', 'go-exit'),
        'lutkhia': ('lut-khia', 'enter-exit'),
        'bawlkhol': ('bawl-khol', 'make-prepare'),
        'tuiphum': ('tui-phum', 'water-immerse'),
        
        # === Temporal Compounds ===
        'hunhoih': ('hun-hoih', 'time-good'),
        'tawntung': ('tawn-tung', 'ever-always'),
        'nipi': ('ni-pi', 'day-great'),
        
        # === Intensifiers/Emphasis ===
        'mahmah': ('mahmah', 'very'),
        'lungkim': ('lung-kim', 'heart-full'),  # "pleased"
        'lungzing': ('lung-zing', 'heart-anguish'),  # Round 155: anguish
        'thakhat': ('tha-khat', 'spirit-one'),
        
        # === Quantifier Compounds ===
        'khempeuhte': ('khempeuh-te', 'all-PL'),
        'khempeuhah': ('khempeuh-ah', 'all-LOC'),    # 378x "to all, in all"
        'khempeuhin': ('khempeuh-in', 'all-ERG'),   # "by all"
        'peuhpeuh': ('peuh-peuh', 'DISTR-DISTR'),
        
        # === Directional Verb Compounds ===
        'paito': ('pai-to', 'go-UP'),           # 200x - "go up, ascend"
        'paitoin': ('pai-to-in', 'go-UP-ERG'),  # going up
        'paisuk': ('pai-suk', 'go-DOWN'),       # "go down, descend"
        'paisukin': ('pai-suk-in', 'go-DOWN-ERG'),
        
        # === Common Connectors ===
        'ciangin': ('ciang-in', 'then-ERG'),
        'hangin': ('hang-in', 'because-ERG'),
        'bangin': ('bang-in', 'like-ERG'),
        'manin': ('man-in', 'reason-ERG'),
        'zongin': ('zong-in', 'although-ERG'),
        'ahihleh': ('a-hi-h-leh', '3SG-be-NOM-if'),
        'hitaleh': ('hi-ta-leh', 'be-PFV-if'),
        'laitakin': ('lai-tak-in', 'midst-exact-ERG'),
        
        # === Negation Compounds ===
        'loh': ('lo-h', 'NEG-NOM'),
        'loin': ('lo-in', 'NEG-ERG'),
        'kuamah': ('kua-mah', 'who-EMPH'),  # "nobody"
        'bangmah': ('bang-mah', 'what-EMPH'),  # "nothing"
        'bangmahin': ('bang-mah-in', 'what-EMPH-ERG'),  # "in no way"
        
        # === bang- (what/how/like) compounds - must precede ba- matching ===
        'bang': ('bang', 'what/like'),        # 4263x
        'bangci': ('bang-ci', 'what-say'),    # "how" 224x
        'banga': ('bang-a', 'what-LOC'),      # "as/like" 79x
        'bangun': ('bang-un', 'what-PL'),     # 84x
        'bangzah': ('bang-zah', 'what-quantity'),  # "how many" 65x
        'bangbang': ('bang-bang', 'what-RED'),     # "whatever" 48x
        'bangte': ('bang-te', 'what-PL'),     # 32x
        'bangzahin': ('bang-zah-in', 'what-quantity-ERG'),  # 28x
        'bangbangin': ('bang-bang-in', 'what-RED-ERG'),     # 28x
        'bangsak': ('bang-sak', 'what-CAUS'), # 26x
        'bangcih': ('bang-cih', 'what-say.NOM'),  # 15x
        'bangsakkik': ('bang-sak-kik', 'what-CAUS-ITER'),  # 12x
        'bangteng': ('bang-teng', 'what-dwell'),   # 10x
        'bangzia': ('bang-zia', 'what-manner'),    # 6x
        'bangkik': ('bang-kik', 'what-ITER'),      # 4x
        'bangbangun': ('bang-bang-un', 'what-RED-PL'),  # 4x
        'bangpi': ('bang-pi', 'what-big'),    # 3x
        'bangkhat': ('bang-khat', 'what-one'),# 3x
        'bangah': ('bang-ah', 'what-LOC'),    # 2x
        'bangta': ('bang-ta', 'what-PFV'),    # 2x
        
        # === ban- (besides/in addition to) compounds ===
        'banah': ('ban-ah', 'besides-LOC'),   # 138x "in addition to"
        
        # === Number Compounds ===
        'sawmahkhat': ('sawm-ah-khat', 'ten-LOC-one'),  # 47x - "tithe/tenth"
        
        # === Postposition + LOC ===
        'panin': ('panin', 'ABL'),  # "from"
        'sangin': ('sang-in', 'high-ERG'),  # "than"
        'tawh': ('tawh', 'COM'),  # "with"
        
        # === Pronoun Compounds ===
        'keimah': ('kei-mah', '1SG.base-EMPH'),
        'nangmah': ('nang-mah', '2SG.base-EMPH'),
        'amah': ('a-mah', '3SG-EMPH'),
        'amaute': ('a-mau-te', '3-PL.base-PL'),
        
        # === Iterative/Continuative ===
        'kisikkik': ('ki-sik-kik', 'REFL-turn-ITER'),
        'nawnkik': ('nawn-kik', 'still-ITER'),
        
        # === Common -in forms (verb/noun + ERG) ===
        'pai-in': ('pai-in', 'go-ERG'),
        'om-in': ('om-in', 'exist-ERG'),
        'thu-in': ('thu-in', 'word-ERG'),
        'nusia-in': ('nusia-in', 'abandon-ERG'),
        'paikhia-in': ('pai-khia-in', 'go-exit-ERG'),
        'zui-in': ('zui-in', 'follow-ERG'),
        
        # === Additional noun compounds ===
        'kikhopna': ('ki-khop-na', 'REFL-gather-NMLZ'),
        'natna': ('nat-na', 'ill-NMLZ'),
        'gamdaihna': ('gam-daih-na', 'land-wide-NMLZ'),
        'paina': ('pai-na', 'go-NMLZ'),
        'khuami': ('khua-mi', 'town-person'),
        'mawhnate': ('mawh-na-te', 'err-NMLZ-PL'),
        
        # === Additional plurals ===
        'gilote': ('gilo-te', 'enemy-PL'),
        'dawite': ('dawi-te', 'demon-PL'),
        'ahite': ('a-hi-te', '3SG-be-PL'),  # Round 155: fix mis-segmentation
        
        # === Adverbial compounds ===
        'nakpitakin': ('nak-pi-tak-in', 'strong-big-exact-ERG'),
        
        # === Additional common forms ===
        'an': ('an', '3PL.POSS'),  # 3rd plural possessive
        'pan': ('pan', 'begin/side'),
        'leitang': ('lei-tang', 'land-earth'),
        'thute': ('thu-te', 'word-PL'),
        'tu-in': ('tu-in', 'now-ERG'),
        'tuate': ('tua-te', 'DIST-PL'),
        'ciang': ('ciang', 'then'),
        'neih': ('nei-h', 'have-NOM'),
        'ni-in': ('ni-in', 'day-ERG'),
        'nai': ('nai', 'near'),
        'omna': ('om-na', 'exist-NMLZ'),
        'gamtat': ('gam-tat', 'land-rule'),
        'gimna': ('gim-na', 'suffer-NMLZ'),
        'kham': ('kham', 'forbid'),
        'thuman': ('thu-man', 'word-reason'),
        
        # === High-frequency productive -na nominalizations ===
        'ahihna': ('a-hih-na', '3SG-be.NOM-NMLZ'),
        'cihna': ('cih-na', 'say.NOM-NMLZ'),
        'theihna': ('theih-na', 'know.II-NMLZ'),
        'hoihna': ('hoih-na', 'good-NMLZ'),
        'bawlna': ('bawl-na', 'make-NMLZ'),
        'piakna': ('piak-na', 'give.to-NMLZ'),
        'genna': ('gen-na', 'speak-NMLZ'),
        'kikona': ('kiko-na', 'cry.out-NMLZ'),
        'thuakna': ('thuak-na', 'suffer-NMLZ'),
        'sawlna': ('sawl-na', 'send-NMLZ'),
        
        # === High-frequency -te plurals ===
        'kumpite': ('kumpi-te', 'king-PL'),
        'thugente': ('thugen-te', 'preacher-PL'),
        'numeite': ('numei-te', 'woman-PL'),
        'kamsangte': ('kamsang-te', 'prophet-PL'),
        'gamte': ('gam-te', 'land-PL'),
        'tanute': ('tanu-te', 'daughter-PL'),
        'biaknate': ('biakna-te', 'worship-PL'),
        'tuite': ('tui-te', 'water-PL'),
        'neite': ('nei-te', 'have-PL'),
        'gamtatnate': ('gamtatna-te', 'kingdom-PL'),
        'kamtaite': ('kamtai-te', 'messenger-PL'),
        'innte': ('inn-te', 'house-PL'),
        'hoihte': ('hoih-te', 'good-PL'),
        'nihte': ('nih-te', 'two-PL'),
        'thumte': ('thum-te', 'three-PL'),
        'liante': ('lian-te', 'big-PL'),
        'ukte': ('uk-te', 'rule-PL'),
        'lote': ('lo-te', 'NEG-PL'),
        
        # === -in ergative/instrumental forms ===
        'napi-in': ('na-pi-in', 'manner-big-ERG'),
        'lai-in': ('lai-in', 'midst-ERG'),
        'pia-in': ('pia-in', 'give-ERG'),
        'kisai-in': ('ki-sai-in', 'REFL-concern-ERG'),
        'biakna-in': ('biakna-in', 'worship-ERG'),
        'hinapi-in': ('hi-na-pi-in', 'be-?-big-ERG'),
        'cihin-ah': ('ci-h-in-ah', 'say-NOM-ERG-LOC'),
        'genin-ah': ('gen-in-ah', 'speak-ERG-LOC'),
        'ma-in': ('ma-in', 'self-ERG'),
        'zan-in': ('zan-in', 'night-ERG'),
        'muhna-ah': ('muh-na-ah', 'see.II-NMLZ-LOC'),
        'gei-ah': ('gei-ah', 'edge-LOC'),
        
        # === Compound verbs ===
        'ciahkik': ('ciah-kik', 'return-ITER'),
        'paisuak': ('pai-suak', 'go-become'),
        'paisuk': ('pai-suk', 'go-CAUS'),
        'paito': ('pai-to', 'go-sit'),
        'paikhiatpih': ('pai-khiat-pih', 'go-emerge-APPL'),
        'semsem': ('sem-sem', 'serve-RED'),
        
        # === Quantifiers ===
        'khatpeuh': ('khat-peuh', 'one-every'),
        'khatlekhat': ('khat-le-khat', 'one-and-one'),
        'khatah': ('khat-ah', 'one-LOC'),
        'sawmthum': ('sawm-thum', 'ten-three'),
        'sawmli': ('sawm-li', 'ten-four'),
        'sagih': ('sagih', 'seven'),
        'vekpi-in': ('vek-pi-in', 'all-big-ERG'),
        
        # === Other high-frequency compounds ===
        'tokhom': ('to-khom', 'sit-gather'),
        'hoihtak': ('hoih-tak', 'good-exact'),
        'thahat': ('tha-hat', 'strong-firm'),
        'thukhen': ('thu-khen', 'word-divide'),
        'neihsa': ('neih-sa', 'have.II-PAST'),                  # had (past of have)
        'paknamtui': ('pak-nam-tui', 'wine'),
        'minthanna': ('min-than-na', 'name-bless-NMLZ'),
        'suanlekhakte': ('suanlekhak-te', 'genealogy-PL'),       # fixed: was over-segmented
        'nisuahna': ('ni-suah-na', 'day-birth-NMLZ'),
        'mihingte': ('mi-hing-te', 'person-kind-PL'),
        'zanin': ('zan-in', 'night-ERG'),
        'omkhawm': ('om-khawm', 'exist-gather'),
        'khuamial': ('khua-mial', 'town-dark'),
        'omsak': ('om-sak', 'exist-CAUS'),
        'sawmnga': ('sawm-nga', 'ten-five'),
        'hoihtakin': ('hoih-tak-in', 'good-exact-ERG'),
        'ukpa': ('uk-pa', 'rule-male'),
        'zingsang': ('zing-sang', 'morning-high'),
        'nitak': ('ni-tak', 'day-exact'),
        'gamgi': ('gam-gi', 'land-boundary'),
        'nihna': ('nih-na', 'two-NMLZ'),
        'thumna': ('thum-na', 'three-NMLZ'),
        'adang': ('a-dang', '3SG-other'),
        'gensa': ('gen-sa', 'speak-PAST'),                      # spoke (past of speak)
        'innsung': ('inn-sung', 'house-inside'),
        'biakpiakna': ('biak-piak-na', 'worship-give.to-NMLZ'),
        'milimte': ('mi-lim-te', 'idol-PL'),
        'thukhamte': ('thu-kham-te', 'law-PL'),
        'inndei': ('inn-dei', 'house-?'),
        'lonona': ('lo-no-na', 'NEG-?-NMLZ'),
        'puanbuk': ('puan-buk', 'cloth-?'),
        'awging': ('aw-ging', 'voice-sound'),
        'lutang': ('lu-tang', 'head-?'),
        'siamna': ('siam-na', 'skilled-NMLZ'),
        'thahatna': ('tha-hat-na', 'strong-firm-NMLZ'),
        'hoihzaw': ('hoih-zaw', 'good-more'),
        'kilemna': ('ki-lem-na', 'REFL-prepare-NMLZ'),
        'tuni-in': ('tu-ni-in', 'now-day-ERG'),
        'naupang': ('nau-pang', 'child-small'),
        'naupangte': ('nau-pang-te', 'child-small-PL'),  # 59x - "children"
        'naupangno': ('nau-pang-no', 'child-small-DIM'),  # "little child"
        'hotkhiatna': ('hot-khiat-na', '?-emerge-NMLZ'),
        'lawmte': ('lawm-te', 'friend-PL'),
        'lopi-in': ('lo-pi-in', 'NEG-big-ERG'),
        'zakhat': ('za-khat', 'hundred-one'),
        'mipihte': ('mi-pih-te', 'person-APPL-PL'),
        'kongpi': ('kong-pi', 'road-big'),
        'kawikawi': ('kawi-kawi', 'crooked-RED'),
        'thutang': ('thu-tang', 'word-story'),
        'citak': ('ci-tak', 'say-exact'),
        'ompih': ('om-pih', 'exist-APPL'),
        'thupi': ('thu-pi', 'word-big'),
        'huhna': ('huh-na', 'blow-NMLZ'),
        'gamdang': ('gam-dang', 'land-other'),
        'lungsimah': ('lungsim-ah', 'heart-LOC'),        # 57x - "in heart/mind"
        'khutnuai': ('khut-nuai', 'hand-under'),        # 63x - "under hand" (control)
        'pualamah': ('pualam-ah', 'outside-LOC'),       # 62x - "outside"
        'lutangte': ('lutang-te', 'chief-PL'),          # 56x - "dukes/chiefs"
        'phattuamna': ('phat-tuam-na', 'praise-promise-NMLZ'),  # 77x - "benefit, reward"
        'pianna': ('pian-na', 'birth-NMLZ'),            # 48x - "origin, father of"
        'lui': ('lui', 'river'),
        'sepna': ('sep-na', 'work-NMLZ'),
        'thungetna': ('thu-nget-na', 'word-request-NMLZ'),
        'gitlohna': ('git-loh-na', 'hate-NEG-NMLZ'),
        'tenna': ('ten-na', 'dwell-NMLZ'),
        'tampite': ('tam-pi-te', 'many-big-PL'),
        'tuute': ('tuu-te', '?-PL'),
        'pawlkhatte': ('pawl-khat-te', 'some-one-PL'),
        'dingte': ('ding-te', 'stand-PL'),
        'dingun': ('ding-un', 'PROSP-PL.IMP'),
        'pawi': ('pawi', 'Pawi'),
        'pang': ('pang', 'side/small'),
        'zing': ('zing', 'morning'),
        'nial': ('nial', 'deny'),
        'san': ('san', 'flee'),
        'ap': ('ap', 'entrust'),
        'pawl': ('pawl', 'group'),
        'zat': ('zat', 'use'),
        'vang': ('vang', 'because'),
        'thuk': ('thuk', 'deep'),
        'zuih': ('zui-h', 'follow-NOM'),
        'zaw': ('zaw', 'more'),
        'khak': ('khak', 'limit'),
        'gamlak': ('gam-lak', 'land-midst'),
        
        # === More locative -a/-ah forms ===
        'khua-a': ('khua-a', 'town-LOC'),
        'lai-a': ('lai-a', 'midst-LOC'),
        'gei-a': ('gei-a', 'edge-LOC'),
        'tu-a': ('tu-a', 'now-LOC'),
        'nuai-ah': ('nuai-ah', 'below-LOC'),
        'thu-ah': ('thu-ah', 'word-LOC'),
        'dinga': ('ding-a', 'PROSP-LOC'),
        
        # === More -in forms ===
        'hinapi-in': ('hi-na-pi-in', 'be-NMLZ-big-ERG'),
        'nei-in': ('nei-in', 'have-ERG'),
        'ne-in': ('ne-in', 'eat-ERG'),
        'khatin': ('khat-in', 'one-ERG'),
        
        # === More -na nominalizations ===
        'lungkhamna': ('lung-kham-na', 'heart-anxiety-NMLZ'),
        'thumanna': ('thuman-na', 'truth-NMLZ'),
        'phatna': ('phat-na', 'praise-NMLZ'),
        'khiatna': ('khiat-na', 'emerge-NMLZ'),
        'cihnopna': ('ci-h-nop-na', 'say-NOM-want-NMLZ'),
        'lupna': ('lup-na', 'bow.down-NMLZ'),
        'mawkna': ('mawk-na', 'err-NMLZ'),
        'hauhna': ('hauh-na', 'shout-NMLZ'),
        'thugenna': ('thu-gen-na', 'word-speak-NMLZ'),
        'nitumna': ('ni-tum-na', 'day-all-NMLZ'),
        
        # === More -te plurals ===
        'kipte': ('kip-te', '?-PL'),
        'makaite': ('makai-te', 'leader-PL'),
        'zite': ('zi-te', 'wife-PL'),
        'hihte': ('hih-te', 'this-PL'),
        'mizawngte': ('mi-zawng-te', 'person-all-PL'),
        'siate': ('sia-te', 'bad-PL'),
        'omlaite': ('om-lai-te', 'exist-midst-PL'),
        'thupiaknate': ('thu-piak-na-te', 'word-give.to-NMLZ-PL'),
        
        # === More compound words ===
        'pasian-te': ('pasian-te', 'god-PL'),
        'inndei': ('inn-dei', 'family'),
        'lonona': ('lo-no-na', 'disobedience'),
        'puanbuk': ('puan-buk', 'tent'),
        'lutang': ('lu-tang', 'pillow'),
        'hotkhiatna': ('hot-khiat-na', 'salvation'),
        'pawlpi': ('pawl-pi', 'group-big'),
        'khawl': ('khawl', 'rest'),
        'tungtawnin': ('tung-tawn-in', 'on-ever-ERG'),
        'panun': ('pa-nun', 'father-?'),
        'muang': ('muang', 'trust'),
        'neu': ('neu', 'small'),
        'ciangkhut': ('ciang-khut', 'then-hand'),
        'mudah': ('mu-dah', 'see-?'),
        'lakhia': ('lak-khia', 'take-exit'),
        'awng': ('awng', 'open'),
        'namtui': ('nam-tui', 'kind-water'),
        'ciam': ('ciam', 'promise'),
        'luang': ('luang', 'flow'),
        'bawlsak': ('bawl-sak', 'make-CAUS'),
        'amahmah': ('a-mah-mah', '3SG-self-RED'),
        'sawmsagih': ('sawm-sagih', 'ten-seven'),
        'thuhilh': ('thu-hilh', 'word-teach'),
        'bawlsa': ('bawl-sa', 'make-PAST'),                     # made (past of make)
        'peuh': ('peuh', 'every'),
        'zanih': ('zan-ih', 'night-NOM'),
        'suksiat': ('suk-siat', 'CAUS-destroy'),
        'khau': ('khau', 'rope'),
        'tuute': ('tuu-te', 'grandchild-PL'),
        'lua': ('lua', 'exceed'),
        
        # === More compounds (frequency 70-110) ===
        'panun': ('pa-nun', 'father-?'),
        'kipte': ('kip-te', 'edge-PL'),
        'lungkham': ('lung-kham', 'heart-anxious'),
        'khuasung': ('khua-sung', 'town-inside'),
        'kaikhawm': ('kai-khawm', 'call-gather'),
        'thunuama': ('thu-nuam-a', 'word-want-LOC'),
        'nopsakna': ('nop-sak-na', 'want-CAUS-NMLZ'),
        'lametna': ('lam-et-na', 'way-?-NMLZ'),
        'salin': ('sa-lin', 'meat-?'),
        'vengte': ('veng-te', 'neighborhood-PL'),
        'niloh': ('ni-loh', 'day-NEG'),
        'kikoih': ('ki-koih', 'REFL-put'),
        'sakolte': ('sakol-te', 'donkey-PL'),
        'hing': ('hing', 'alive'),
        'pana': ('pa-na', 'father-NMLZ'),
        'lasakna': ('la-sak-na', 'take-CAUS-NMLZ'),
        'thahna': ('thah-na', 'die-NMLZ'),
        'omte': ('om-te', 'exist-PL'),
        'zahtakna': ('zah-tak-na', 'fear-exact-NMLZ'),
        'kiciamna': ('ki-ciam-na', 'REFL-promise-NMLZ'),
        'maipha': ('mai-pha', 'face-good'),
        'kangtum': ('kang-tum', '?-all'),
        'kungte': ('kung-te', 'trunk-PL'),
        'alang': ('alang', 'side'),                       # "in the side" - not a-lang!
        'lampi-ah': ('lampi-ah', 'way-LOC'),
        'pasalte': ('pasal-te', 'husband-PL'),
        'hi-in': ('hi-in', 'be-ERG'),
        'biakinn-ah': ('biakinn-ah', 'temple-LOC'),
        'vekpi-un': ('vek-pi-un', 'all-big-PL.IMP'),
        'nungzui': ('nung-zui', 'life-follow'),
        'khatvei': ('khat-vei', 'one-time'),
        'naungek': ('nau-ngek', 'child-small'),
        'kongkhak': ('kong-khak', '1SG→3-limit'),
        'ciahpih': ('ciah-pih', 'return-APPL'),
        'nuamtakin': ('nuam-tak-in', 'want-exact-ERG'),
        'ciamsa': ('ciam-sa', 'promise-PAST'),                  # promised (past of promise)
        'thupiang': ('thu-piang', 'word-born'),
        'suaktasak': ('suak-ta-sak', 'become-PFV-CAUS'),
        'koi-ah': ('koi-ah', 'where-LOC'),
        'nopna': ('nop-na', 'want-NMLZ'),
        'vanglian': ('vang-lian', 'power-big'),
        'hizaw': ('hi-zaw', 'be-more'),
        'annek': ('an-nek', '3PL-eat.II'),
        'innkuante': ('inn-kuan-te', 'house-household-PL'),
        'mawhsakna': ('mawh-sak-na', 'err-CAUS-NMLZ'),
        'zuihna': ('zuih-na', 'follow.II-NMLZ'),
        'vaihawm': ('vai-hawm', '?-smell'),
        'ciamteh': ('ciam-teh', 'promise-receive'),
        'mu-in': ('mu-in', 'see-ERG'),
        'omna-ah': ('omna-ah', 'exist.NMLZ-LOC'),
        'nai-ah': ('nai-ah', 'near-LOC'),
        'za-in': ('za-in', 'hear-ERG'),
        'sawltakte': ('sawl-tak-te', 'send-exact-PL'),
        'maizum': ('mai-zum', 'face-bow'),
        'dahna': ('dah-na', 'put-NMLZ'),
        'thuaksak': ('thuak-sak', 'suffer-CAUS'),
        'maizumna': ('mai-zum-na', 'face-bow-NMLZ'),
        'vasa': ('vasa', 'bird'),
        'nilh': ('nilh', 'wipe'),
        'khan': ('khan', 'generation'),
        'sawmguk': ('sawm-guk', 'ten-six'),
        'sanggamnu': ('sanggam-nu', 'sibling-female'),
        'khuadak': ('khua-dak', 'town-near'),
        'paktat': ('pak-tat', '?-strike'),
        'pak': ('pak', '?'),
        'khuam': ('khuam', 'darkness'),
        'sap': ('sap', 'call/summon'),
        'sal': ('sal', 'slave'),
        'kan': ('kan', 'stay'),
        'vai': ('vai', 'foreigner'),
        'kumpi-in': ('kumpi-in', 'king-ERG'),
        'keel': ('keel', '?'),
        'khuaneute': ('khua-neu-te', 'town-small-PL'),
        'tuamtuamte': ('tuam-tuam-te', 'different-RED-PL'),
        'gamh': ('gamh', 'land.II'),
        'ing': ('ing', '?'),
        
        # === Miscellaneous High-Frequency ===
        'gamlakah': ('gam-lak-ah', 'land-midst-LOC'),
        'inla': ('in-la', 'ERG-and'),
        'sunga': ('sung-a', 'inside-3SG'),
        'tunga': ('tung-a', 'on-3SG'),
        'ama': ('a-ma', '3SG-self'),
        'nau': ('nau', 'child'),
        'aana': ('a-ana', '3SG-child.PL'),
        'pah': ('pah', 'do.so'),
        'hileh': ('hi-leh', 'be-if'),
        'unla': ('un-la', 'PL.IMP-and'),
        
        # === More common noun forms ===
        'mai-ah': ('mai-ah', 'face-LOC'),
        'khua-ah': ('khua-ah', 'town-LOC'),
        'inn-ah': ('inn-ah', 'house-LOC'),
        'leitang': ('lei-tang', 'land-earth'),
        'pasal': ('pasal', 'husband'),
        'pawlkhat': ('pawl-khat', 'some-one'),
        'mihing': ('mi-hing', 'person-kind'),
        'minamte': ('mi-nam-te', 'person-kind-PL'),
        'nasep': ('na-sep', 'work'),
        'suante': ('suan-te', 'offspring-PL'),
        'namsau': ('nam-sau', 'long.hair'),
        'nangawn': ('na-ngawn', '2SG-own'),
        'piang': ('piang', 'be.born'),
        'hihna': ('hih-na', 'this-NMLZ'),
        'lungdam': ('lung-dam', 'heart-well'),
        'itna': ('it-na', 'love-NMLZ'),
        'nungta': ('nung-ta', 'life-PFV'),
        'uliante': ('ulian-te', 'elder-PL'),
        'huh': ('huh', 'blow'),
        'khuapite': ('khua-pi-te', 'town-big-PL'),
        'lohna': ('loh-na', 'NEG-NMLZ'),
        'kam': ('kam', 'word/mouth'),
        'mual': ('mual', 'mountain'),
        'sathau': ('sa-thau', 'fat'),
        'tuipi': ('tui-pi', 'water-big'),
        'hehna': ('heh-na', 'anger-NMLZ'),
        'upna': ('up-na', 'believe-NMLZ'),
        'nungzuite': ('nung-zui-te', 'life-follow-PL'),
        'khawm': ('khawm', 'gather'),
        'ciat': ('ciat', 'each'),
        'dangte': ('dang-te', 'other-PL'),
        'tate': ('ta-te', 'child-PL'),
        'nate': ('na-te', '2SG-PL'),
        'kizui-in': ('ki-zui-in', 'REFL-follow-ERG'),
        'la-in': ('la-in', 'take-ERG'),
        
        # === Additional compounds from frequency analysis (freq 50-230) ===
        'leenggahzu': ('leeng-gah-zu', 'grape-cluster-wine'),    # 228 - wine (lit. grape wine)
        'sumngo': ('sum-ngo', 'brass-iron'),                      # 152 - brass and iron (metals)
        'leenggui': ('leeng-gui', 'grape-vine'),                  # 130 - grapevine
        'ling': ('ling', 'pile'),                                  # 106
        'panun': ('pa-nun', 'father-life'),                        # 101
        'leenggah': ('leeng-gah', 'grape-cluster'),               # 98 - grape clusters
        'mudah': ('mu-dah', 'see-easy'),                           # 97
        'keel': ('keel', 'heel'),                                  # 85
        'salin': ('sa-lin', 'meat-hope'),                          # 82
        'lametna': ('lam-et-na', 'path-example-NMLZ'),        # 81
        'paktat': ('pak-tat', 'divide-strike'),               # 79
        'pak': ('pak', 'divide'),                              # 78
        'thei-in': ('thei-in', 'know.I-ERG'),                  # 75
        'le-uhcin': ('le-uh-cin', 'also-PL-even'),            # 74
        # alang duplicate removed - defined above
        'zin': ('zin', 'journey'),                             # 73
        'sawh': ('sawh', 'correct'),                           # 72
        'kangtum': ('kang-tum', 'brass-all'),                 # 72
        'nisimin': ('ni-simin', 'day-always'),                # 70
        'tuikhuk': ('tui-khuk', 'water-ladle'),               # 68
        'late': ('la-te', 'song-PL'),                          # 68
        'mualtungah': ('mual-tung-ah', 'mountain-top-LOC'),   # 66
        'kang': ('kang', 'suffer'),                            # 66
        'cil': ('cil', 'sprout'),                              # 66
        'lauhuai': ('lau-huai', 'fear-dread'),                # 65
        'vaihawm': ('vai-hawm', 'plan-counsel'),              # 63
        'lite': ('li-te', 'four-PL'),                          # 60
        'bawngtalte': ('bawng-tal-te', 'cow-calf-PL'),        # 59
        'kahna': ('kah-na', 'fight-NMLZ'),                     # 59
        'neute': ('neu-te', 'small-PL'),                       # 58
        'tangvalpa': ('tangval-pa', 'youth-father'),          # 58
        'khialhnate': ('khialh-na-te', 'sin-NMLZ-PL'),        # 57
        'nuai-a': ('nuai-a', 'below-LOC'),                     # 56
        'kihei-in': ('ki-hei-in', 'REFL-angry-ERG'),          # 56
        'zawlte': ('zawl-te', 'plain-PL'),                     # 56
        'tai-in': ('tai-in', 'flee-ERG'),                      # 55
        'lau-in': ('lau-in', 'fear-ERG'),                      # 55
        'nasepna-ah': ('na-sep-na-ah', 'work-NMLZ-LOC'),      # 55
        'zingsangin': ('zing-sang-in', 'morning-early-ERG'),  # 54
        'neihna': ('neih-na', 'have-NMLZ'),                   # 54
        'laksak': ('lak-sak', 'take-CAUS'),                   # 54
        'pian': ('pian', 'be.born'),                           # 54
        'lamdangte': ('lam-dang-te', 'way-other-PL'),         # 54
        'pahtawina': ('pah-tawi-na', 'do-honor-NMLZ'),        # 54
        'mualte': ('mual-te', 'mountain-PL'),                 # 54
        'mahmahna': ('mahmah-na', 'very-NMLZ'),               # 54
        'egypt-ah': ('egypt-ah', 'EGYPT-LOC'),                # 53
        'sumte': ('sum-te', 'money-PL'),                      # 53
        'hikeileh': ('hi-kei-leh', 'be-NEG.EMPH-if'),         # 53
        'munte': ('mun-te', 'place-PL'),                      # 53
        'theite': ('thei-te', 'know.I-PL'),                   # 53
        'khawmin': ('khawm-in', 'gather-ERG'),                # 52
        'siangthote': ('siangtho-te', 'holy-PL'),             # 52
        'khitna': ('khit-na', 'after-NMLZ'),                  # 52
        'sau': ('sau', 'long'),                                # 52
        'midikte': ('mi-dik-te', 'person-straight-PL'),       # 51
        'lungmuang': ('lung-muang', 'heart-still'),           # 51
        'lunghimawh': ('lung-himawh', 'heart-fear'),          # 51
        'bukna': ('buk-na', 'ambush-NMLZ'),                   # 51
        'gengen': ('gen-gen', 'speak-RED'),                   # 50
        'samsia': ('sam-sia', 'call-destroy'),                # 50
        'lungdamsak': ('lung-dam-sak', 'heart-well-CAUS'),    # 50
        'ante': ('an-te', '3PL-PL'),                          # 50
        'tuni-a': ('tu-ni-a', 'now-day-LOC'),                 # 50
        'biakpiaknate': ('biak-piak-na-te', 'worship-give-NMLZ-PL'), # 50
        'nusiat': ('nu-siat', 'mother-destroy'),              # 50
        'pianzia': ('pian-zia', 'birth-manner'),              # 50
        
        # === More compounds from frequency analysis (freq 38-55) ===
        'leenggahzu': ('leenggah-zu', 'grape-liquid'),    # 239x "wine"
        'leenggah': ('leenggah', 'grape'),               # 98x "grape/vine fruit"
        'leenggui': ('leenggui', 'grapevine'),           # vineyard-related
        'sumngo': ('sum-ngo', 'money-silver'),                 # 152
        'kumpinu': ('kumpi-nu', 'king-mother'),               # 54
        'nupi': ('nu-pi', 'mother-big'),                       # 53
        'ihmu': ('ih-mu', '1PL-see'),                          # 52
        'guh': ('guh', 'shout'),                               # 49
        'ing': ('ing', 'be.able'),                             # 48
        'zasak': ('za-sak', 'hear-CAUS'),                      # 47
        'biakinnpi': ('biakinn-pi', 'temple-big'),            # 47
        'siampipuan': ('siampi-puan', 'priest-cloth'),        # 46
        'thusia': ('thu-sia', 'word-evil'),                    # 46
        'savun': ('sa-vun', 'meat-fur'),                       # 45
        'thupiaksa': ('thu-piak-sa', 'word-give-PL.POSS'),     # 45
        'gamtatnasa': ('gamtat-na-sa', 'kingdom-NMLZ-PL.POSS'), # 45 - "his kingdom/rule"
        'nasepnate': ('nasepna-te', 'work.NMLZ-PL'),            # 47 - "works"
        'puanhampi': ('puan-ham-pi', 'cloth-cover-big'),      # 45
        'sawt': ('sawt', 'long.time'),                         # 45
        'zawng': ('zawng', 'all'),                              # 45
        'nun': ('nun', 'life'),                                 # 45
        'piaksa': ('piak-sa', 'give-PL.POSS'),                 # 44
        'gamlapi': ('gam-la-pi', 'land-take-big'),            # 44
        'ahihlam': ('a-hih-lam', '3SG-be-way'),               # 43
        'thukkik': ('thuk-kik', 'deep-again'),                # 43
        'bawlsia': ('bawl-sia', 'make-evil'),                 # 43
        'nuai': ('nuai', 'below'),                             # 42
        'zai': ('zai', 'song'),                                # 42
        'nawk': ('nawk', 'again'),                             # 42
        'theisak': ('thei-sak', 'know.I-CAUS'),               # 42
        'ngaihno': ('ngaih-no', 'love-INT'),                  # 42 - beloved/wellbeloved
        'ciangun': ('ciang-un', 'then-PL.IMP'),               # 41
        'nail': ('nail', 'always'),                            # 41
        'zasagih': ('za-sagih', 'hundred-seven'),             # 40
        'at': ('at', 'cut'),                                   # 40
        'pahtawi': ('pah-tawi', 'do-honor'),                  # 40
        'nunung': ('nu-nung', 'mother-back'),                 # 40
        'behlap': ('beh-lap', 'tribe-half'),                  # 40
        'palsat': ('pal-sat', 'wall-strike'),                 # 39
        'gensak': ('gen-sak', 'speak-CAUS'),                  # 39
        'kai': ('kai', 'ascend'),                              # 39
        'puantualpi': ('puan-tual-pi', 'cloth-generation-big'), # 39 - "coat" (of many colors)
        'thutak': ('thu-tak', 'word-true'),                   # 39
        
        # === Session 3: More compounds ===
        'letmat': ('let-mat', 'half-cubit'),                  # 34 - "cubit and a half"
        'thuciam': ('thu-ciam', 'word-promise'),              # 33 - "covenant, promise"
        'thumin': ('thu-min', 'three'),                       # numeral "three"
        'kongkhakte': ('kongkha-te', 'door-PL'),              # 38 - "doors"
        'pawlte': ('pawl-te', 'group-PL'),                    # 33 - "companions, allies"
        'paikhawm': ('pai-khawm', 'go-together'),             # 33 - "come together"
        'cisak': ('ci-sak', 'say-CAUS'),                      # 33 - "curse" (causative of say)
        'beelte': ('beel-te', 'pan-PL'),                      # 33 - "pans, bowls"
        'kauphe': ('kauphe', 'locust'),                       # 33 - "locust"
        'kisapna': ('ki-sap-na', 'REFL-call-NMLZ'),           # 33 - "need/necessity"
        'gamtain': ('gamta-in', 'send.away-ERG'),             # 50 - "sending away"
        
        # === Session 3: More compounds ===
        'le-uh': ('le-uh', 'and-PL.IMP'),                     # 44 - "and (plural imperative)"
        'leuh': ('le-uh', 'and-PL.IMP'),                      # variant
        'itte': ('it-te', 'love-PL'),                         # 39 - "loves/lovest" (plural verb)
        'vante': ('van-te', 'sky-PL'),                        # 34 - unclear, possibly "skies" or parsing error
        'khakte': ('khak-te', 'offspring-PL'),                # 34 - "generations, offspring"
        'khuasunga': ('khua-sunga', 'town-inside'),           # 34 - "in the town"
        'tuidawn': ('tui-dawn', 'water-fetch'),               # 34 - "fetch water"
        'theithei': ('thei~thei', 'know.I~RED'),              # 33 - "perceive/know" (reduplicated)
        'singte': ('sing-te', 'tree-PL'),                     # 33 - "trees"
        'lungnuam': ('lung-nuam', 'heart-pleased'),           # 32 - "pleased, glad"
        'khiate': ('khia-te', 'exit-PL'),                     # variant
        'lakhia': ('la-khia', 'take-out'),                    # 32 - "take out"
        'lakhia-in': ('la-khia-in', 'take-out-ERG'),          # 32 - "taking out"
        'luanna': ('luan-na', 'flow-NMLZ'),                   # 32 - "flowing"
        'singkungte': ('singkung-te', 'tree-PL'),             # 32 - "trees"
        'honpi': ('hon-pi', 'flock-big'),                     # 31 - "great multitude, swarm"
        
        # === Session 3: More compounds (corrections) ===
        'dawng': ('dawng', 'get/receive'),                    # 387 - "get, receive, fetch"
        'dawngin': ('dawng-in', 'get/receive-ERG'),          # 143 - "getting, receiving"
        'langkhatah': ('lang-khat-ah', 'side-one-LOC'),      # 88 - "against" (at one side)
        'langpangin': ('lang-pang-in', 'side-near-ERG'),     # 63 - "against" (near one side)
        'langpang': ('lang-pang', 'side-near'),              # 39 - "against, side"
        'langkhat': ('lang-khat', 'side-one'),               # 35 - "one side"
        'singlamteh': ('sing-lam-teh', 'wood-cross'),        # 65 - "cross" (the cross)
        'singkuang': ('sing-kuang', 'wood-box'),             # 45 - "ark" (wooden box)
        
        # === Session 3: More compounds (round 2) ===
        'siangthosak': ('siangtho-sak', 'holy-CAUS'),        # 32 - "sanctify"
        'piansak': ('pian-sak', 'create-CAUS'),              # 32 - "creation"
        'lausak': ('lau-sak', 'fear-CAUS'),                  # 31 - "make afraid"
        'galkidona': ('gal-kido-na', 'enemy-fight-NMLZ'),    # 31 - "warfare"
        'genkhol': ('gen-khol', 'speak-INTENS'),             # 31 - "denounce"
        'ciahsak': ('ciah-sak', 'return-CAUS'),              # 31 - "send back"
        'genkhia': ('gen-khia', 'speak-EXIT'),               # 32 - "utter forth"
        'theihsa': ('theih-sa', 'know.II-PERF'),             # 32 - "already known"
        'beina': ('bei-na', 'end-NMLZ'),                     # 32 - "ending"
        'panpih': ('pan-pih', 'plead-APPL'),                 # 32 - "plead for"
        'neupen': ('neu-pen', 'small-TOP'),                  # 32 - "smallest"
        
        # === Session 3: More compounds (round 3) ===
        'beisak': ('bei-sak', 'end-CAUS'),                   # 99 - "destroy, abolish"
        'beisa': ('bei-sa', 'end-PERF'),                     # 68 - "ended, finished"
        'beimang': ('bei-mang', 'end-COMPL'),                # 33 - "perish, be destroyed"
        'nuihsan': ('nuih-san', 'laugh-at'),                 # 31 - "laugh at, mock"
        'simmawhna': ('simmawh-na', 'blaspheme-NMLZ'),       # 31 - "blasphemy"
        'bawngnawi': ('bawng-nawi', 'cow-butter'),           # 30 - "butter"
        'khualmi': ('khual-mi', 'sojourn-person'),           # 30 - "stranger, sojourner"
        'nidang': ('ni-dang', 'day-other'),                  # 30 - "formerly, before"
        'khangham': ('khang-ham', 'generation-full'),        # 30 - "full of years"
        'sawmkua': ('sawm-kua', 'ten-nine'),                 # 30 - "ninety"
        'anlak': ('an-lak', 'rice-harvest'),                 # 30 - "harvest"
        
        # === Session 3: More compounds (round 4) ===
        'simmawhbawl': ('simmawh-bawl', 'blaspheme-do'),     # 33 - "commit blasphemy"
        'phaknatna': ('phaknat-na', 'leprosy-NMLZ'),         # 31 - "leprosy"
        'zahzah': ('zah~zah', 'fear~RED'),                   # 30 - "every living" (reduplicated)
        'kalaohte': ('kalaoh-te', 'camel-PL'),               # 30 - "camels"
        'kihtakna': ('kihtak-na', 'dread-NMLZ'),             # 30 - "dread"
        'suahtakna': ('suahtak-na', 'redeem-NMLZ'),          # 30 - "redemption"
        'khangno': ('khang-no', 'generation-young'),         # 30 - "youngest"
        'liangko': ('liangko', 'shoulder'),                  # 29 - "shoulder"
        'nungtasak': ('nung-ta-sak', 'live-?-CAUS'),         # 29 - "spare life"
        'honpite': ('hon-pi-te', 'flock-big-PL'),            # 29 - "great multitudes"
        
        # === Session 3: More compounds (round 5) ===
        'kihtakhuai': ('kihtak-huai', 'dread-causing'),      # 46 - "dreadful, terrible"
        'ngaihno': ('ngaih-no', 'think-lovingly'),           # 33 - "beloved"
        'aksite': ('aksi-te', 'star-PL'),                    # 32 - "stars"
        'behbehin': ('beh-beh-in', 'tribe~RED-ERG'),         # 32 - "by tribes"
        'pawlpite': ('pawl-pi-te', 'group-big-PL'),          # 31 - "churches"
        'citakin': ('ci-tak-in', 'say-true-ERG'),            # 30 - "truly"
        'biakpiak': ('biak-piak', 'worship-give'),           # 29 - "sacrifice"
        'ukpite': ('ukpi-te', 'duke-PL'),                    # 29 - "dukes"
        'hampha': ('ham-pha', 'full-worthy'),                # 29 - "worthy"
        'lungtang': ('lung-tang', 'heart-place'),            # 29 - "breastplate"
        'geelna': ('geel-na', 'plan-NMLZ'),                  # 29 - "pattern, fashion"
        
        # === Session 3: More compounds (round 6) ===
        'ngahsak': ('ngah-sak', 'get-CAUS'),                 # 29 - "need, require"
        'mindaina': ('mindai-na', 'shame-NMLZ'),             # 29 - "shame"
        'silate': ('sila-te', 'servant-PL'),                 # 29 - "servants"
        'limte': ('lim-te', 'sign-PL'),                      # 29 - "signs"
        'kuangte': ('kuang-te', 'trough-PL'),                # 28 - "kneadingtroughs"
        'thukpi': ('thuk-pi', 'deep-big'),                   # 28 - "the deep, flood"
        'teelna': ('teel-na', 'choose-NMLZ'),                # 28 - "choice"
        'bawlpa': ('bawl-pa', 'make-person'),                # 27 - "young man"
        'thaute': ('thau-te', 'fat-PL'),                     # 27 - "fats"
        'gensia': ('gen-sia', 'speak-bad'),                  # 27 - "slander"
        'thaltangte': ('thaltang-te', 'arrow-PL'),           # 27 - "arrows"
        'phattuam': ('phat-tuam', 'praise-benefit'),         # 27 - "benefit"
        'samsak': ('sam-sak', 'call-CAUS'),                  # 26 - "send for"
        
        # === Session 3: More compounds (round 7: -te suffix words) ===
        'cingte': ('cing-te', 'faithful-PL'),                # 33 - "faithful ones"
        'site': ('si-te', 'die-PL'),                         # 31 - "the dead"
        'sate': ('sa-te', 'flesh-PL'),                       # 29 - "flesh(es)"
        'sepnate': ('sep-na-te', 'work-NMLZ-PL'),           # 28 - "works, deeds"
        'lianpite': ('lianpi-te', 'army-PL'),               # 27 - "armies"
        'peengkulte': ('peengkul-te', 'trumpet-PL'),        # 27 - "trumpets"
        'ngaihsutnate': ('ngaihsut-na-te', 'think-NMLZ-PL'), # 27 - "thoughts"
        'laite': ('lai-te', 'tip-PL'),                       # 26 - "tips"
        'luanghawmte': ('luanghawm-te', 'carcass-PL'),       # 26 - "carcasses"
        'lasate': ('lasa-te', 'pillar-PL'),                  # 26 - "pillars"
        
        # === Session 3: More compounds (round 8: fix sim/sisan/siang/silh over-matching) ===
        'limtakin': ('lim-tak-in', 'sign-true-ERG'),         # 227 - "thoroughly"
        'laitakun': ('lai-tak-un', 'middle-true-PL.IMP'),   # 125 - "in the midst"
        'laitak': ('lai-tak', 'middle-true'),               # 87 - "midst"
        'simin': ('sim-in', 'count-ERG'),                   # 135 - "counting"
        'simloh': ('sim-loh', 'count-unable'),              # 99 - "cannot be counted"
        'silhin': ('silh-in', 'clothe-ERG'),                # 54 - "clothed"
        'laiteng': ('lai-teng', 'middle-at'),               # 46 - "at the midst"
        'laizangah': ('lai-zang-ah', 'middle-side-LOC'),    # 41 - "in the midst"
        'laizang': ('lai-zang', 'middle-side'),             # 39 - "midst"
        'siasak': ('sia-sak', 'bad-CAUS'),                  # 57 - "make bad, damage"
        'siangsak': ('siang-sak', 'holy-CAUS'),             # 39 - "make holy, sanctify"
        'sisak': ('si-sak', 'die-CAUS'),                    # 39 - "cause to die, kill"
        'sisa': ('si-sa', 'die-PERF'),                      # 42 - "already dead"
        'siit': ('siit', 'sacrifice'),                      # 39 - sacrifice offering
        'teelsa': ('teel-sa', 'choose-PERF'),               # 36 - "chosen"
        
        # === Session 4: More lai-, sak-, and other compounds ===
        'laizial': ('lai-zial', 'middle-place'),            # 39 - "middle place"
        'laiza': ('lai-za', 'middle-place'),                # 38 - "midst"
        'lai-un': ('lai-un', 'middle-PL.IMP'),             # 31 - "in the midst"
        'lailai': ('lai~lai', 'middle~REDUP'),             # 31 - "continually, always"
        'lai-at': ('lai-at', 'middle-?'),                  # 30 - needs context
        
        # -sak causative compounds
        'khauhsak': ('khauh-sak', 'strong-CAUS'),           # 30 - "make strong"
        'nungtasak': ('nungta-sak', 'live-CAUS'),           # 29 - "make alive, revive"
        'silhsak': ('silh-sak', 'clothe-CAUS'),             # 27 - "cause to clothe"
        'maizumsak': ('maizum-sak', 'bow.face-CAUS'),       # 25 - "make bow"
        'lungkimsak': ('lungkim-sak', 'satisfied-CAUS'),    # 22 - "satisfy"
        'khensak': ('khen-sak', 'divide-CAUS'),             # 22 - "cause to divide"
        'khialsak': ('khial-sak', 'err-CAUS'),              # 22 - "cause to err, mislead"
        'tengsak': ('teng-sak', 'dwell-CAUS'),              # 21 - "cause to dwell"
        'luangsak': ('luang-sak', 'flow-CAUS'),             # 21 - "cause to flow"
        'hihsak': ('hih-sak', 'be-CAUS'),                   # 21 - "make to be"
        
        # Other high-frequency compounds
        'nak-uhleh': ('nak-uh-leh', 'SUBJ-PL-if'),         # 40 - conditional marker
        'sanah': ('sanah', 'in.front'),                    # 32 - "before, in front of"
        'sawmte': ('sawm-te', 'ten-PL'),                   # 32 - "tens, dozens"
        'thumanin': ('thu-man-in', 'word-true-ERG'),       # 32 - "truly, in truth"
        'singgah': ('singgah', 'hang'),                    # 25 - "hang (on tree)"
        'nasemnu': ('na-sem-nu', '2SG-serve-FEM'),         # 26 - "your maidservant"
        'paktatna': ('pak-tat-na', 'proclaim-strike-NMLZ'), # 30 - "proclamation"
        'paikhiatpihin': ('paikhiat-pih-in', 'send.away-APPL-ERG'), # 28 - "sending away"
        'munmuanhuai': ('mun-muan-huai', 'place-trust-worthy'), # 26 - "trustworthy place"
        'khasiat': ('kha-siat', 'spirit-evil'),             # 26 - "evil spirit"
        'gamtate': ('gamta-te', 'kingdom-PL'),              # 27 - "kingdoms"
        'thudang': ('thu-dang', 'word-other'),              # 26 - "other word/another matter"
        'gukna': ('guk-na', 'dog-NMLZ'),                    # 26 - "doggish/dog's"
        'tungnung': ('tung-nung', 'arrive-after'),          # 26 - "after arriving"
        'tonpih': ('ton-pih', 'sit-APPL'),                  # 26 - "sit with, accompany"
        'nekhawm': ('nek-hawm', 'eat.II-together'),         # 26 - "eat together"
        'thudon': ('thu-don', 'word-preach'),               # 26 - "preach, proclaim"
        'tungsiah': ('tung-siah', 'arrive-time'),           # 26 - "time of arrival"
        'bawngtalno': ('bawngtal-no', 'calf-small'),        # 26 - "young calf"
        'keng': ('keng', 'only'),                           # 26 - "only" (variant of ken)
        'vaikhak': ('va-i-khak', 'go.and-?-approach'),      # 26 - "go and approach"
        
        # === Session 4 Round 2: lung- (heart) compounds ===
        'lunggulh': ('lung-gulh', 'heart-long'),            # 25 - "long for, desire intensely"
        'lungduai': ('lung-duai', 'heart-soft'),            # 25 - "gracious, longsuffering"
        'lungkimna': ('lung-kim-na', 'heart-whole-NMLZ'),   # 19 - "agreement, contentment"
        'lunghihmawhna': ('lung-hih-mawh-na', 'heart-be-sin-NMLZ'), # 18 - "grief, sorrow"
        'lungduaina': ('lung-duai-na', 'heart-soft-NMLZ'),  # 15 - "grace, patience"
        'lungmuangin': ('lung-muang-in', 'heart-trust-ERG'), # 14 - "trusting"
        
        # khua- compounds
        'khuampeek': ('khuampeek', 'cubit'),                # 28 - "cubit" (unit of measure)
        'khuakhal': ('khua-khal', 'town-famine'),           # 20 - "famine in town"
        'khualzinna': ('khual-zin-na', 'sojourn-travel-NMLZ'), # 18 - "sojourning"
        'khuamte': ('khuam-te', 'cubit-PL'),                # 18 - "cubits"
        'khuamluzepna': ('khua-mlu-zep-na', 'town-head-bow-NMLZ'), # 18 - context-dep
        'khuapikulh': ('khuapi-kulh', 'city-wall'),         # 17 - "city wall"
        
        # thu- (word) compounds
        'thukim': ('thu-kim', 'word-keep'),                  # 22 - "keep covenant, agree"
        'thukimna': ('thu-kim-na', 'word-keep-NMLZ'),        # 15 - "covenant keeping"
        'thukhennate': ('thu-khen-na-te', 'word-divide-NMLZ-PL'), # 13 - "judgments"
        'thukimpih': ('thu-kim-pih', 'word-keep-APPL'),      # 12 - "agree with"
        'thukan': ('thu-kan', 'word-hold'),                  # 11 - "hold word"
        'thukna': ('thu-k-na', 'word-NMLZ'),                 # 10 - "saying, utterance"
        
        # khaw- compounds
        'khawlin': ('khawl-in', 'rest-ERG'),                 # 23 - "resting"
        'khawng': ('khawng', 'about/approximately'),         # 21 - "about, approximately"
        'khawhlawhte': ('khawh-lawh-te', 'able-earn-PL'),    # 18 - "earners, workers"
        'khawh': ('khawh', 'can/able'),                      # 15 - "can, able to"
        'khawlsak': ('khawl-sak', 'rest-CAUS'),              # 15 - "cause to rest"
        'khawlna': ('khawl-na', 'rest-NMLZ'),                # 13 - "rest, resting place"
        
        # khang- (generation) compounds  
        'khansau': ('khan-sau', 'generation-long'),          # 20 - "generations, long time"
        'khanglo': ('khang-lo', 'generation-NEG'),           # 17 - "barren, childless"
        'khangto': ('khang-to', 'generation-sit'),           # 15 - "generation, posterity"
        'khanglai': ('khang-lai', 'generation-middle'),      # 10 - "generation, era"
        'khanlawh': ('khan-lawh', 'generation-earn'),        # 10 - "generation-earn"
        
        # Miscellaneous high-frequency
        'lo-a': ('lo-ah', 'field-LOC'),                      # 31 - "in the field"
        'hici': ('hi-ci', 'this-say'),                       # 27 - "do this, thus"
        'kal': ('kal', 'liver'),                             # 32 - "liver" (body part)
        'muhsa': ('muh-sa', 'see.II-PERF'),                  # 27 - "seen, having seen"
        'kipatna': ('ki-pat-na', 'REFL-begin-NMLZ'),         # 28 - "beginning"
        
        # === Session 4 Round 3: -sak causatives ===
        'hoihsak': ('hoih-sak', 'good-CAUS'),               # 20 - "make good, bless"
        'semsak': ('sem-sak', 'serve-CAUS'),                # 19 - "make to serve"
        'vaksak': ('vak-sak', 'shine-CAUS'),                # 17 - "illuminate, light up"
        'koihsak': ('koih-sak', 'put-CAUS'),                # 17 - "put, place"
        'dingsak': ('ding-sak', 'stand-CAUS'),              # 17 - "make stand, erect"
        'nuamsak': ('nuam-sak', 'pleasant-CAUS'),           # 17 - "make pleasant, please"
        'nesak': ('ne-sak', 'eat-CAUS'),                    # 18 - "feed"
        'hingsak': ('hing-sak', 'be.alive-CAUS'),           # 19 - "make alive, resurrect"
        'thumsak': ('thum-sak', 'three-CAUS'),              # 19 - contextual
        'mindaisak': ('mindai-sak', 'shame-CAUS'),          # 18 - "cause shame"
        'hingkiksak': ('hing-kik-sak', 'be.alive-ITER-CAUS'), # 18 - "resurrect"
        'honsak': ('hon-sak', 'flock-CAUS'),                # 17 - "shepherd, tend flock"
        'langsak': ('lang-sak', 'side-CAUS'),               # 15 - "show, reveal"
        'suksiatsak': ('suk-siat-sak', 'make-destroy-CAUS'), # 16 - "cause destruction"
        
        # More compounds with verb+suffix patterns
        'nga-in': ('ngai-in', 'listen.I-ERG'),              # 36 - "listening"
        'baihsa-in': ('baihsa-in', 'already-ERG'),          # 29 - "already having"
        'cingin': ('cing-in', 'faithful-ERG'),              # 28 - "faithfully"
        'lua-in': ('lua-in', 'exceed-ERG'),                 # 25 - "exceedingly"
        'kha-in': ('kha-in', 'spirit-ERG'),                 # 22 - "in spirit"
        'baihin': ('baih-in', 'already-ERG'),               # 21 - "already"
        'thuhilhin': ('thu-hilh-in', 'word-teach-ERG'),     # 21 - "instructing"
        'pangin': ('pang-in', 'plead-ERG'),                 # 20 - "pleading"
        
        # More -na nominalizer compounds
        'paubaanna': ('pau-baan-na', 'speak-slander-NMLZ'), # 30 - "slander, blasphemy"
        'aisanna': ('ai-san-na', 'burn-flee-NMLZ'),         # 29 - context-specific
        'sawmna': ('sawm-na', 'ten-NMLZ'),                  # 28 - "tithing"
        'sanna': ('san-na', 'flee-NMLZ'),                   # 26 - "fleeing"
        'migitna': ('mi-git-na', 'person-hate-NMLZ'),       # 25 - "hatred of people"
        'hopihna': ('ho-pih-na', 'counsel-APPL-NMLZ'),      # 25 - "counseling"
        'dawna': ('dawn-na', 'receive-NMLZ'),               # 25 - "reception"
        'kisuanna': ('ki-suan-na', 'REFL-follow-NMLZ'),     # 24 - "succession"
        'suahna': ('suah-na', 'become-NMLZ'),               # 23 - "becoming"
        'cihtakna': ('ci-tak-na', 'say-true-NMLZ'),         # 23 - "truth telling"
        'galdona': ('gal-do-na', 'enemy-conquer-NMLZ'),     # 23 - "victory"
        'giatna': ('giat-na', 'hate-NMLZ'),                 # 23 - "hatred"
        'salsuahna': ('sal-suah-na', 'servant-become-NMLZ'), # 22 - "servitude"
        'ancilna': ('ancil-na', 'anoint-NMLZ'),             # 22 - "anointing"
        'vankoihna': ('van-koih-na', 'sky-put-NMLZ'),       # 22 - "heavenly placing"
        
        # === Session 4 Round 4: More high-frequency words ===
        "ke'n": ("ke'n", '1SG.PRO'),                        # straight quote
        "ke\u2019n": ("ke\u2019n", '1SG.PRO'),              # curly quote
        "keima-a'": ("keima-a'", '1SG.self.GEN'),           # straight quote
        "keima-a\u2019": ("keima-a\u2019", '1SG.self.GEN'), # curly quote
        "kua'n": ("kua'n", 'nobody.EMPH'),                  # straight quote
        "kua\u2019n": ("kua\u2019n", 'nobody.EMPH'),        # curly quote
        'nazatte': ('na-zat-te', '2SG-hear-PL'),            # 33x - "you hear them"
        'nazat': ('na-zat', '2SG-hear'),                    # 32x - "you hear"
        'ulianpa': ('u-lian-pa', 'elder-great-M'),          # 32x - "elder"
        'sin': ('sin', 'near'),                             # 32x - "near, close to"
        'sil': ('sil', 'flesh/body'),                       # 30x - "flesh, body"
        'ning': ('ning', 'will/shall'),                     # 30x - modal auxiliary
        'theitel': ('thei-tel', 'know.I-exact'),            # 30x - "know exactly"
        'nisuh': ('ni-suh', 'day-count'),                   # 30x - "days"
        'lai-at': ('lai-at', 'middle-LOC'),                 # 30x - "at the middle"
        'matengun': ('mateng-un', 'until-PL.IMP'),          # 29x - "until (plural)"
        'tuh': ('tuh', 'sow/plant'),                        # 29x - "sow, plant"
        'gamlapi-ah': ('gamlapi-ah', 'wilderness-LOC'),     # 28x - "in the wilderness"
        'mangbuhham': ('mangbuh-ham', 'barley-?'),          # 28x - compound
        'kite': ('ki-te', 'REFL-PL'),                       # 28x - "themselves"
        'thatang': ('that-ang', 'work-labor'),                  # 28x - servile work
        'khauhtakin': ('khauh-tak-in', 'strong-true-ERG'),  # 28x - "strongly"
        'nawkin': ('nawk-in', 'again-INST'),                # 27x - again (ergative)
        'sawp': ('sawp', 'wrap'),                           # 27x - "wrap, cover"
        'mudahte': ('muhdah-te', 'trouble-PL'),             # 27x - "troubles, troubles"
        'muhdahhuai': ('muhdah-huai', 'trouble-worthy'),    # 27x - "troublesome"
        'piakik': ('piak-kik', 'give.to-ITER'),             # 26x - "give back"
        'kongpi-ah': ('kongpi-ah', 'road.big-LOC'),         # 26x - "on the highway"
        'piapa': ('pia-pa', 'give-M'),                      # 26x - "giver, one who gives"
        'hihsa': ('hih-sa', 'be-PERF'),                     # 25x - "been"
        'sia-in': ('sia-in', 'bad-ERG'),                    # 25x - "badly"
        'kaihkhop': ('kaih-khop', 'gather-together'),       # 25x - "gather together"
        'kawng': ('kawng', 'road/way'),                     # 25x - "road, way"
        'nengniam': ('neng-niam', 'stranger-oppress'),          # 25x - vex/oppress stranger
        'singkha': ('sing-kha', 'wood-acacia'),                  # 25x - shittim/acacia wood
        'khate': ('khat-te', 'one-PL'),                     # 25x - "some (ones)"
        'kawlsing': ('kawl-sing', 'fry-wood'),              # 25x - compound
        'paai': ('pa-ai', 'father-love'),                   # 25x - compound
        'ngeite': ('ngei-te', 'have.NMLZ-PL'),              # 25x - "possessions"
        'hawlkhiat': ('hawl-khiat', 'drive-away'),          # 25x - "drive away"
        'zahko': ('zah-ko', 'despise-curse'),                   # 25x - curse/despise
        'mihau': ('mi-hau', 'person-rich'),                 # 25x - "rich person"
        'thatlum': ('that-lum', 'kill-all'),                # 25x - "kill all"
        'milian': ('mi-lian', 'person-great'),              # 25x - "great person"
        'mul': ('mul', 'hair'),                             # 24x - "hair"
        'tuunote': ('tuuno-te', 'child-PL'),                # 24x - "children"
        
        # === Session 4 Round 5: More compounds ===
        'paipihto': ('paipih-to', 'accompany-sit'),         # 24x - "accompany"
        'kahto': ('ka-h-to', '1SG-?-sit'),                  # 24x - needs more analysis
        'awmdal': ('awm-dal', 'exist-remain'),              # 24x - "remain, stay"
        'val': ('val', 'go.quickly'),                       # 24x - "go quickly"
        'buktual': ('buk-tual', 'hole-dig'),                # 24x - "dig pit"
        'kawikawi-in': ('kawikawi-in', 'crooked-ERG'),      # 24x - "crookedly"
        'muk': ('muk', 'kiss'),                             # 24x - "kiss"
        'panmun': ('pan-mun', 'plead-place'),               # 24x - "altar"
        'gennop': ('gen-nop', 'speak-soft'),                # 24x - "speak softly"
        'gahte': ('gah-te', 'fruit-PL'),                    # 23x - "fruits"
        'pahpah': ('pah~pah', 'father~REDUP'),              # 23x - "each father"
        'pangah': ('pan-gah', 'plead-fall'),                # 23x - compound
        'veilam': ('vei-lam', 'faint-direction'),           # 23x - compound
        'inn-a': ('inn-ah', 'house-LOC'),                   # 23x - "in the house"
        'sagihvei': ('sagih-vei', 'seven-times'),           # 23x - "seven times"
        'naih': ('na-ih', '2SG-love'),                      # 23x - "you love"
        'lakik': ('la-kik', 'take-ITER'),                   # 23x - "take back"
        'unau': ('u-nau', 'elder-younger'),                 # 23x - "siblings"
        'mipih': ('mi-pih', 'person-APPL'),                 # 23x - compound
        'nuh': ('nuh', 'mother'),                           # 23x - "mother" variant
        'tawntungun': ('tawntung-un', 'eternity-PL.IMP'),   # 23x - "forever (pl)"
        'dangtak': ('dang-tak', 'other-true'),              # 23x - "truly other"
        'vengpa': ('veng-pa', 'guard-M'),                   # 23x - "guardian"
        'gensawn': ('gen-sawn', 'speak-continue'),          # 23x - "continue speaking"
        'sepsa': ('sep-sa', 'work-PERF'),                   # 23x - "worked"
        'thuteng': ('thu-teng', 'word-tell'),                  # 23x - tell news/tidings
        'pawlpih': ('pawl-pih', 'group-APPL'),              # 23x - "with group"
        'miliante': ('mi-lian-te', 'person-great-PL'),      # 23x - "great people"
        'mangbuhham': ('mangbuh-ham', 'barley-wheat'),      # 28x - "barley and wheat"
        'kaikhawmin': ('kai-khawm-in', 'gather-together-ERG'), # 28x - gathered together
        
        # === Session 4 Round 6: More high-frequency vocab ===
        'ihmut': ('ihmut', 'deep.sleep'),                   # 22x - "deep sleep"
        'zagiat': ('za-giat', 'hundred-eight'),             # 22x - "eight hundred"
        'ngate': ('ngate', 'those/said'),                   # 22x - "those" (demonstrative)
        'tote': ('to-te', 'lord-PL'),                       # 22x - "lords"
        'bawnghon': ('bawng-hon', 'cattle-flock'),          # 22x - "herd"
        'nungakte': ('nungak-te', 'girl-PL'),               # 22x - "daughters, maidens"
        'hoihpente': ('hoih-pen-te', 'good-SUPER-PL'),      # 22x - "best ones"
        'kahlei': ('kahlei', 'ladder'),                     # 22x - "ladder"
        'letsongte': ('letsong-te', 'lentil-PL'),           # 22x - "lentils"
        'netum': ('ne-tum', 'eat-full'),                    # 22x - "eat fill"
        'muvanlai': ('mu-van-lai', 'see.I-sky-middle'),     # 22x - compound
        'haite': ('hai-te', 'cup-PL'),                      # 22x - "cups"
        'kawnggak': ('kawng-gak', 'road-girdle'),              # 22x - girdle (priestly garment)
        'gingte': ('ging-te', 'gong-PL'),                   # 22x - "gongs"
        'kongpite': ('kongpi-te', 'road.big-PL'),           # 22x - "highways"
        'tuikhang': ('tui-khang', 'water-carry'),           # 22x - "water carrier"
        'hihlam': ('hih-lam', 'this-direction'),            # 22x - "this way"
        'tuihualte': ('tuihual-te', 'flood-PL'),            # 22x - "floods"
        'ihihna': ('i-hih-na', '1PL.INCL-do-NMLZ'),         # 22x - "our doing"
        'kongcingte': ('kong-cing-te', 'road-faithful-PL'), # 22x - compound
        
        # === Session 4 Round 7: More compounds from philological analysis ===
        'kahto': ('ka-hto', '1SG-ascend'),                  # 24x - "I ascend"
        'thuteng': ('thu-teng', 'word-tell'),               # 23x - "told/informed"
        'kawnggak': ('kawng-gak', 'road-girdle'),           # 22x - "girdle" (garment)
        'paubaang': ('pau-baang', 'speak-perfect'),         # 21x - "perfect" (blameless)
        'sukha': ('su-kha', 'touch-place'),                 # 21x - "touch"
        'balkek': ('bal-kek', 'owe-rend'),                  # 21x - "rent/tore"
        'balkekin': ('bal-kek-in', 'owe-rend-ERG'),         # 21x - "having rent"
        'dawnna': ('dawn-na', 'receive-NMLZ'),              # 21x - "receiving"
        'thuaknate': ('thuak-na-te', 'suffer-NMLZ-PL'),     # 21x - "sufferings"
        'ang': ('a-ng', '3SG-FUT'),                         # 21x - "he/she will"
        'leengpeite': ('leeng-pei-te', 'chariot-chief-PL'), # 21x - "chief chariots"
        'kizepna': ('ki-zep-na', 'REFL-join-NMLZ'),         # 21x - "joining/union"
        'khutme': ('khut-me', 'hand-span'),                 # 21x - "handbreadth"
        'sukham': ('su-kham', 'touch-reach'),               # 21x - "touch/reach"
        'nitna': ('nit-na', 'day-NMLZ'),                    # 21x - compound
        'cithei': ('ci-thei', 'say-able'),                  # 21x - "can say"
        'theihtelna': ('theih-tel-na', 'know.II-help-NMLZ'),# 21x - "understanding"
        'galkapmangte': ('galkap-mang-te', 'soldier-chief-PL'),# 21x - "captains"
        'simzawh': ('sim-zawh', 'count-finish'),            # 21x - "finish counting"
        'nausuak': ('nau-suak', 'child-birth'),             # 21x - "childbirth"
        'kuate': ('kua-te', 'who-PL'),                      # 21x - "who (plural)"
        'piaktheih': ('piak-theih', 'give.to-able'),        # 21x - "able to give"
        'hoihsa': ('hoih-sa', 'good-early'),                # 20x - "good earlier"
        'baang': ('baang', 'alike'),                        # 20x - "like/alike"
        'ciktui': ('cik-tui', 'one-water'),                 # 20x - compound
        'cianga': ('ci-ang-a', 'say-FUT-NOM'),                # 20x - "will say"
        'neihsun': ('neih-sun', 'have.II-long'),            # 20x - "have long"
        'cidam': ('ci-dam', 'say-well'),                    # 20x - "is well"
        'keeltal': ('keel-tal', 'heel-bare'),               # 20x - "barefoot"
        'mangte': ('mang-te', 'chief-PL'),                  # 20x - "chiefs"
        'mitphial': ('mit-phial', 'eye-look.up'),           # 20x - "look up"
        'bawlsiat': ('bawl-siat', 'make-destroy'),          # 20x - "destroy"
        'ukte\'': ('uk-te\'', 'rule-PL.POSS'),              # 20x - "rulers'"
        'piakhia': ('piak-hia', 'give.to-away'),            # 20x - "give away"
        'meivakte': ('meivak-te', 'torch-PL'),              # 20x - "torches"
        'bullente': ('bullen-te', 'bull-PL'),               # 20x - "bulls"
        'anletui': ('an-le-tui', '3PL-and-water'),          # 20x - compound
        'omsa': ('om-sa', 'exist-early'),                   # 20x - "existed before"
        'puapa': ('pua-pa', 'carry.back-father'),           # 20x - compound
        'ngawh': ('ngawh', 'endure'),                       # 20x - "endure"
        'mittang': ('mit-tang', 'eye-force'),               # 20x - "eye intensity"
        'kithahna': ('ki-thah-na', 'REFL-kill-NMLZ'),       # 20x - "self-destruction"
        'paunak': ('pau-nak', 'speak-time'),                # 20x - "speaking time"
        'gamtatnasate': ('gamtatna-sa-te', 'kingdom-early-PL'),# 20x - compound
        'vat': ('vat', 'go.quickly'),                       # 20x - "quickly go"
        'muhtheih': ('muh-theih', 'see.II-able'),           # 20x - "visible/able to see"
        'kiphasakte': ('ki-phasa-te', 'REFL-bless-PL'),     # 20x - "blessed ones"
        'tuikuangpi': ('tui-kuang-pi', 'water-pool-big'),   # 20x - "great pool"
        'umlebeel': ('um-lebeel', 'believe-be.must'),       # 20x - "must believe"
        
        # === Session 4 Round 8: More compounds from philological analysis ===
        'lahna': ('lah-na', 'let.down-NMLZ'),               # 19x - "letting down"
        'honkhat': ('hon-khat', 'flock-one'),               # 19x - "a company"
        'kigenna': ('ki-gen-na', 'REFL-explain-NMLZ'),      # 19x - "interpretation"
        'sumgolh': ('sum-golh', 'money-desire'),            # 19x - "covetousness"
        'mizawng': ('mi-zawng', 'person-poor'),             # 19x - "poor person"
        'sianthona': ('siangtho-na', 'holy-NMLZ'),          # 19x - "holiness"
        'bawk': ('bawk', 'bottle/cast'),                    # 19x - "bottle" or "cast"
        'sauvei': ('sau-vei', 'long-journey'),              # 19x - "sojourn"
        'theikung': ('theih-kung', 'oil-tree'),             # 19x - "olive tree"
        'pangsim': ('pang-sim', 'plead-count'),             # 19x - "smite"
        'gamdai': ('gam-dai', 'land-overcome'),             # 19x - "overcome"
        'genthei': ('gen-thei', 'speak-able.NEG'),          # 19x - "wretched"
        'semkhawm': ('sem-khawm', 'serve-together'),        # 19x - "serve together"
        'tom': ('tom', 'dwell'),                            # 19x - "dwell/sit"
        'puakhia': ('puak-hia', 'send-away'),               # 19x - "send away"
        'zal': ('zal', 'spread'),                           # 19x - "spread"
        'ip': ('ip', 'cover'),                              # 19x - "cover"
        'kuana': ('kua-na', 'who-NMLZ'),                    # 19x - compound
        'dingteng': ('ding-teng', 'stand-tell'),            # 19x - "stand and tell"
        'pahtak': ('pa-tak', 'father-true'),                # 19x - "true father"
        'galkapmang': ('galkap-mang', 'soldier-chief'),     # 19x - "captain"
        'nektheih': ('nek-theih', 'eat.II-able'),           # 19x - "edible"
        'nawngkaisak': ('nawng-kai-sak', '2SG-help-CAUS'),  # 19x - "you help"
        'innsunga': ('inn-sung-a', 'house-inside-LOC'),     # 19x - "in the house"
        'cihtak': ('cih-tak', 'say.NOM-true'),              # 19x - "truly said"
        'maizumin': ('mai-zum-in', 'face-bow-ERG'),         # 19x - "bowing face"
        'gamsa': ('gam-sa', 'land-meat'),                   # 18x - compound
        'deihhuai': ('deih-huai', 'want-plural'),           # 18x - "desires"
        'kipiakna': ('ki-piak-na', 'REFL-give.to-NMLZ'),    # 18x - "self-giving"
        'masa-a': ('masa-a', 'first-LOC'),                  # 18x - "at first"
        'veilamah': ('vei-lam-ah', 'faint-side-LOC'),       # 18x - compound
        'bawnghonte': ('bawng-hon-te', 'cattle-flock-PL'),  # 18x - "cattle herds"
        'khop': ('khop', 'enough'),                         # 18x - "enough"
        'khauhual': ('khau-hual', 'cord-bracelet'),            # 18x - bracelet/cord
        'lopate': ('lo-pa-te', 'field-father-PL'),          # 18x - "farmers"
        'cikmah': ('cik-mah', 'one-self'),                  # 18x - "oneself"
        'peemtate': ('peem-ta-te', 'peace-PFV-PL'),         # 18x - "peaceful ones"
        'liamna': ('liam-na', 'pass-NMLZ'),                 # 18x - "passing"
        'paakte': ('paak-te', 'share-PL'),                  # 18x - "shares/portions"
        'paitoh': ('pai-toh', 'go-accompany'),              # 18x - "go with"
        'utthu-a': ('ut-thu-a', 'want-word-LOC'),           # 18x - compound
        'umlebeelte': ('um-lebeel-te', 'believe-must-PL'),  # 18x - "believers"
        'mei-am': ('mei-am', 'fire-Q'),                     # 18x - "fire?"
        'ma-a': ('ma-a', 'that-LOC'),                       # 18x - "at that"
        'kikhawmte': ('ki-khawm-te', 'REFL-gather-PL'),     # 18x - "gathered ones"
        'tangtung': ('tang-tung', 'arrive-reach'),          # 18x - "arrive at"
        'nidangin': ('ni-dang-in', 'day-other-ERG'),        # 18x - "another day"
        
        # === Session 4 Round 9: More compounds from philological analysis ===
        'vaikhak': ('va-i-khak', 'go-?-command'),           # 26x - "charge/command"
        'hin': ('hin', 'this.EMPH'),                        # 21x - demonstrative emphatic
        'nihte': ('nih-te', 'two-PL'),                      # 21x - "two (people)"
        'nipikal': ('ni-pi-kal', 'day-big-fold'),           # 21x - "week"
        'bawngte': ('bawng-te', 'cattle-PL'),               # 21x - "cattle"
        'banbanin': ('ban-ban-in', 'side-side-ERG'),        # 21x - "ministering"
        'cianga': ('ci-ang-a', 'say-FUT-LOC'),              # 20x - "saying that"
        'cidam': ('ci-dam', 'say-well'),                    # 20x - "is well"
        'ukte': ('uk-te', 'tent-PL'),                       # 20x - "tents"
        'kawi': ('kawi', 'forth'),                          # 19x - "back and forth"
        'kawikawi': ('kawi-kawi', 'forth~forth'),           # "to and fro"
        'khauhual': ('khau-hual', 'string-bracelet'),       # 18x - "bracelet"
        'thugennate': ('thu-gen-na-te', 'word-speak-NMLZ-PL'),# 18x - "words spoken"
        'hunsung': ('hun-sung', 'time-inside'),             # 18x - "during/meanwhile"
        'thumu': ('thu-mu', 'word-?'),                      # 18x - "trumpets"
        'huaiham': ('huai-ham', 'dread-strong'),            # 18x - "jealous"
        'laikhak': ('lai-khak', 'letter-seal'),             # 18x - "sealed letter"
        'zanglei': ('zang-lei', 'use-buy'),                 # 18x - compound
        'zanglei-ah': ('zang-lei-ah', 'use-buy-LOC'),       # 18x - compound
        'taina': ('ta-i-na', 'stay-?-NMLZ'),                # 18x - "dwelling"
        'ngahkhawm': ('ngah-khawm', 'get-together'),        # 18x - "gather"
        'thahatte': ('tha-hat-te', 'strength-hard-PL'),     # 18x - "strong ones"
        'gihna': ('gih-na', 'tremble-NMLZ'),                # 18x - "trembling"
        'nidanga': ('ni-dang-a', 'day-other-LOC'),          # 18x - "other day"
        'nitaang': ('ni-taang', 'day-long'),                # 18x - "long day"
        'inntual': ('inn-tual', 'house-floor'),             # 18x - "house floor"
        'paktatte': ('pak-tat-te', 'respect-?-PL'),         # 18x - compound
        'khemsa-in': ('khem-sa-in', 'restrain-early-ERG'),  # 18x - "restraining"
        'peemtate': ('peem-ta-te', 'peace-?-PL'),           # 18x - compound
        'vaihawmna': ('va-i-hawm-na', 'go-?-together-NMLZ'),# 19x - compound
        
        # === Session 4 Round 10: High-frequency remaining vocab ===
        'kaikhawmin': ('ka-i-khawm-in', '1SG-?-gather-ERG'), # 28x - "gathered together"
        'taina': ('ta-i-na', 'stay-?-NMLZ'),                 # 18x - "refuge"
        'thumu': ('thu-mu', 'horn/trumpet'),                 # 18x - "trumpet"
        'kawmte': ('kawm-te', 'beam-PL'),                    # 18x - "beams/posts"
        'zahtakbawl': ('zahtak-bawl', 'honor-do'),          # 18x - "reverence"
        'puansan': ('puan-san', 'cloth-wear'),              # 18x - "apparel"
        'uptheih': ('up-theih', 'elder.sibling-able'),      # 18x - "lay/rest"
        'puanbukte': ('puan-buk-te', 'cloth-cover-PL'),     # 17x - "tents"
        'kawl': ('kawl', 'heifer'),                         # 17x - "heifer"
        'cik': ('cik', 'fountain'),                         # 17x - "fountain"
        'neh': ('neh', 'sojourn/come'),                     # 17x - "sojourn"
        'mudahin': ('mu-dah-in', 'see.I-hate-ERG'),         # 17x - "hating/sent away"
        'sinsona': ('sin-son-a', 'die-remain-LOC'),         # 17x - compound
        'encik': ('en-cik', 'look-fountain'),               # 17x - compound
        'lupkhop': ('lup-khop', 'bow.down-enough'),         # 17x - "bow down"
        'paikikin': ('pai-kik-in', 'go-again-ERG'),         # 17x - "going again"
        'tomno': ('tom-no', 'dwell-?'),                     # 17x - compound
        'milipin': ('mi-lip-in', 'person-crowd-ERG'),       # 17x - "multitude"
        'vanging': ('vang-ing', 'strength-?'),              # 17x - compound
        'phawkna': ('phawk-na', 'remember-NMLZ'),           # 17x - "remembrance"
        'tuamcip': ('tuam-cip', 'promise-cover'),           # 17x - "covered over"
        'lamna': ('lam-na', 'way-NMLZ'),                    # 17x - "direction"
        'bukkongah': ('buk-kong-ah', 'ambush-place-LOC'),   # 17x - "at ambush"
        'khenthei': ('khen-thei', 'divide-able'),           # 17x - "able to divide"
        'nuamsa-in': ('nuam-sa-in', 'want-early-ERG'),      # 17x - "willingly"
        'hawlkhiatna': ('hawl-khiat-na', 'drive-out-NMLZ'), # 17x - "driving out"
        'kulhpite': ('kulh-pi-te', 'wall-big-PL'),          # 17x - "walls"
        'langpangte': ('lang-pang-te', 'side-?-PL'),        # 17x - compound
        'simgawp': ('sim-gawp', 'count-grasp'),             # 17x - "numbering"
        'kaikhia': ('ka-i-khia', '1SG-?-exit'),             # 17x - "I go out"
        'thupizaw': ('thu-pi-zaw', 'word-big-more'),        # 17x - "greater word"
        'sumai': ('su-mai', 'money-face'),                  # 17x - compound
        'zongte': ('zong-te', 'search-PL'),                 # 17x - "searchers"
        'khenuai-ah': ('khe-nuai-ah', 'leg-under-LOC'),     # 17x - "under (feet)"
        'nihveina': ('nih-vei-na', 'two-time-NMLZ'),        # 17x - "second time"
        'thuakzawh': ('thuak-zawh', 'suffer-able'),         # 17x - "able to suffer"
        'naseppih': ('na-sep-pih', '2SG-work-APPL'),        # 17x - "work with you"
        'thawhkikna': ('thawh-kik-na', 'rise-again-NMLZ'),  # 17x - "resurrection"
        'kikal-a': ('ki-kal-a', 'REFL-between-LOC'),        # 16x - "between"
        'naihin': ('naih-in', 'near-ERG'),                  # 16x - "nearly"
        'sakhat': ('sak-hat', 'shaft-hard'),                # 16x - "candlestick shaft"
        'peemtate': ('peem-ta-te', 'flat-stay-PL'),         # 18x - compound
        'paktatte': ('pak-tat-te', 'share-?-PL'),           # 18x - "shares"
        'mizawngte\'': ('mi-zawng-te\'', 'person-poor-PL.POSS'), # 17x - "poor people's"
        'kaih': ('kaih', 'pull/lead'),                      # 17x - "lead"
        'nawlah': ('nawl-ah', 'place-LOC'),                 # 17x - "at the place"
        
        # === Session 4 Round 11: More medium-frequency vocabulary ===
        'ngaihbaang': ('ngaih-baang', 'think/love-alike'),   # 16x - "fair/beautiful"
        'suakkhia': ('suak-khia', 'become-exit'),            # 16x - "came out"
        'keelno': ('keel-no', 'heel-?/young'),               # 16x - "kids (goats)"
        'nupite': ('nupi-te', 'woman-PL'),                   # 16x - "women"
        'hilhkhol': ('hilh-khol', 'teach-denounce'),         # 16x - "solemnly protest"
        'khoi': ('khoi', 'nurse'),                           # 16x - "nurse"
        'gimnate': ('gim-na-te', 'toil-NMLZ-PL'),            # 16x - "toils"
        'hanna': ('han-na', 'follow-NMLZ'),                  # 16x - "following"
        'kat': ('kat', 'catch/burn'),                        # 16x - "catch fire"
        'banto': ('ban-to', 'side-sit'),                     # 16x - "middle"
        'sawpin': ('sawp-in', 'body-ERG'),                   # 16x - "carcase"
        'tuinak': ('tui-nak', 'water-time'),                 # 16x - "fountain"
        'cithak': ('ci-thak', 'say-?'),                      # 16x - compound
        'khamul': ('kha-mul', 'spirit-shave'),               # 16x - "shave"
        'samsiat': ('sam-siat', 'call-destroy'),             # 16x - "cursed"
        'kuangdai': ('kuang-dai', 'trough-?'),               # 16x - "dishes/bowls"
        'zatna': ('zat-na', 'hear.II-NMLZ'),                 # 16x - "spreading (plague)"
        'lamlahna': ('lam-lah-na', 'way-drop-NMLZ'),         # 16x - "trespass"
        'ommawk': ('om-mawk', 'exist-?'),                    # 16x - "slack/vow"
        'nulepa': ('nu-le-pa', 'mother-and-father'),         # 16x - "beast/parents"
        'ukte\'': ('uk-te\'', 'tent-PL.POSS'),               # 20x - "tents'"
        'nihte\'': ('nih-te\'', 'two-PL.POSS'),              # 21x - "two's"
        'vaikhak': ('va-i-khak', 'go-?-command'),            # 26x - "charge/command"
        'vaihawmna': ('va-i-hawm-na', 'go-?-together-NMLZ'), # 19x - "arrangement"
        'tomno': ('tom-no', 'dwell-young'),                  # 17x - "dwelling"
        'vanging': ('vang-ing', 'strength-?'),               # 17x - compound
        'mizawngte\'': ('mi-zawng-te\'', 'person-poor-PL.POSS'), # 17x - "poor people's"
        'langpangte': ('lang-pang-te', 'side-?-PL'),         # 17x - "sides"
        'kaikhia': ('ka-i-khia', '1SG-?-exit'),              # 17x - "I go out"
        'suakta-in': ('suak-ta-in', 'become-stay-ERG'),      # 16x - "having become"
        'vaan': ('vaan', 'heaven/sky'),                      # 16x - "heaven"
        'khamtheihzu': ('kham-theih-zu', 'forbid-able-NEG'), # 16x - "cannot forbid"
        'tampite\'': ('tampi-te\'', 'many-PL.POSS'),         # 16x - "many people's"
        'genna-ah': ('gen-na-ah', 'speak-NMLZ-LOC'),         # 16x - "at speaking"
        'bulpite': ('bul-pi-te', 'base-big-PL'),             # 16x - "roots"
        'umcihin': ('um-cih-in', 'believe-say.NOM-ERG'),     # 16x - "believing"
        'vanah': ('van-ah', 'heaven-LOC'),                   # 16x - "in heaven"
        'honpa': ('hon-pa', 'flock-father'),                 # 16x - "shepherd"
        'gentheih': ('gen-theih', 'speak-able'),             # 16x - "able to speak"
        'puanung': ('pua-nung', 'carry.back-back'),          # 16x - "carrying"
        
        # === Session 4 Round 12: More vocabulary ===
        'suangmanphate': ('suang-man-pha-te', 'stone-price-good-PL'), # 16x - "precious stones"
        'halna': ('hal-na', 'terror-NMLZ'),                  # 16x - "terror"
        'mihaute': ('mi-hau-te', 'person-rich-PL'),          # 16x - "rich people"
        'etteh': ('et-teh', 'care-measure'),                 # 16x - "sign/proverb"
        'cinate': ('ci-na-te', 'say-NMLZ-PL'),               # 16x - "sayings/sick"
        'puanpak': ('puan-pak', 'cloth-share'),              # 15x - "hangings"
        'khenkhia': ('khen-khia', 'divide-exit'),            # 15x - "divided"
        'gambup': ('gam-bup', 'land-whole'),                 # 15x - "whole land"
        'omlam': ('om-lam', 'exist-side'),                   # 15x - "eyes opened/state"
        'puansilh': ('puan-silh', 'cloth-wrap'),             # 15x - "naked/clothed"
        'zakua': ('za-kua', 'hundred-nine'),                 # 15x - "nine hundred"
        'bawngla': ('bawng-la', 'cattle-?'),                 # 15x - "heifer"
        'tutphah': ('tut-phah', 'sleep-saddle'),             # 15x - "saddled"
        'khuang': ('khuang', 'drum/tabret'),                 # 15x - "tabret/feast"
        'ompihna': ('om-pih-na', 'exist-APPL-NMLZ'),         # 15x - "being with/prosper"
        'luite': ('lui-te', 'river-PL'),                     # 15x - "rivers"
        'keek': ('keek', 'fire/lightning'),                  # 15x - "fire/lightning"
        'zankim': ('zan-kim', 'night-half'),                 # 15x - "midnight"
        'sah': ('sah', 'witness/heap'),                      # 15x - "witness heap"
        'gukte': ('guk-te', 'almond-PL'),                    # 15x - "almonds"
        'khuampeekte': ('khuam-peek-te', 'cubit-measure-PL'), # 15x - "cubits"
        'nunglam': ('nung-lam', 'live-side'),                # 15x - "living way"
        'puantungsilh': ('puan-tung-silh', 'cloth-head-wrap'), # 15x - "turban"
        'ngunte': ('ngun-te', 'silver-PL'),                  # 15x - "silver pieces"
        'tukna': ('tuk-na', 'push-NMLZ'),                    # 15x - "pushing"
        'siahuai': ('sia-huai', 'die-dread'),                # 15x - "mortal dread"
        'tuamkoih': ('tuam-koih', 'promise-put'),            # 15x - "put on/promise"
        'ngaihsutna-in': ('ngaihsut-na-in', 'think-NMLZ-ERG'), # 15x - "thinking"
        'sehna': ('seh-na', 'slice-NMLZ'),                   # 15x - "slicing"
        'pawlpawlin': ('pawl-pawl-in', 'group~group-ERG'),   # 15x - "in groups"
        'pakan': ('pa-kan', 'father-?'),                     # 15x - compound
        'dingkhia-in': ('ding-khia-in', 'stand-exit-ERG'),   # 15x - "standing up"
        'teembawte': ('teem-baw-te', '?-?-PL'),              # 15x - compound
        'kinusiate': ('ki-nusia-te', 'REFL-abandon-PL'),     # 15x - "abandoned ones"
        'tan\'': ('tan\'', '?.POSS'),                        # 15x - compound
        'innte-ah': ('inn-te-ah', 'house-PL-LOC'),           # 15x - "in the houses"
        'lutna-ah': ('lut-na-ah', 'enter-NMLZ-LOC'),         # 15x - "at entering"
        'lui-ah': ('lui-ah', 'river-LOC'),                   # 15x - "in the river"
        'mipihte\'': ('mi-pih-te\'', 'person-APPL-PL.POSS'), # 15x - compound
        'kizepnate': ('ki-zep-na-te', 'REFL-join-NMLZ-PL'),  # 15x - "joinings"
        'naute': ('nau-te', 'child-PL'),                     # 15x - "children"
        'nem': ('nem', 'soft'),                              # 15x - "soft"
        'banin': ('ban-in', 'side-ERG'),                     # 15x - "by side"
        
        # === Session 4 Round 13: More vocabulary ===
        'laksakin': ('lak-sak-in', 'take-CAUS-ERG'),         # 15x - "possessed"
        'nuaisiah': ('nuai-siah', 'under-subdue'),           # 15x - "subdued"
        'galsimna': ('gal-sim-na', 'enemy-count-NMLZ'),      # 15x - "battle"
        'paaikhia': ('paa-i-khia', 'father-?-exit'),         # 15x - "seen"
        'awn': ('awn', 'void'),                              # 15x - "void/empty"
        'nungdelh': ('nung-delh', 'live-hide'),              # 15x - "hid"
        'simtham': ('sim-tham', 'count-molten'),             # 15x - "graven image"
        'omkha': ('om-kha', 'exist-?'),                      # 15x - "living"
        'gamtatsia': ('gamtat-sia', 'kingdom-bad'),          # 15x - "perverseness"
        'balnen': ('bal-nen', 'owe-?'),                      # 15x - "devoured"
        'theigah': ('thei-gah', 'know.I-attach'),            # 15x - "trust"
        'vanmanpha': ('van-manpha', 'go.and-precious'),      # 15x - "treasures"
        'satgawp': ('sat-gawp', 'strike-grasp'),             # 15x - "blew"
        'thangpaihna': ('thang-paih-na', 'rise-pour-NMLZ'),  # 15x - "indignation"
        'tacilte': ('ta-cil-te', 'stay-first-PL'),           # 14x - "firstlings"
        'thumnate': ('thum-na-te', 'three-NMLZ-PL'),         # 14x - compound
        'tuiciin': ('tui-ciin', 'water-?'),                  # 14x - compound
        'nupa': ('nu-pa', 'mother-father'),                  # 14x - "parents"
        'naupaii': ('nau-paii', 'child-?'),                  # 14x - compound
        'midik': ('mi-dik', 'person-righteous'),             # 14x - "righteous person"
        'hukna': ('huk-na', 'cover-NMLZ'),                   # 14x - "covering"
        'tuucingte': ('tuucing-te', 'shepherd-PL'),          # 14x - "shepherds"
        'ko\'': ('ko\'', 'call.POSS'),                       # 14x - "called"
        'nuhin': ('nu-hin', 'mother-this'),                  # 14x - compound
        'kikhumna': ('ki-khum-na', 'REFL-cover-NMLZ'),       # 14x - "covering"
        'ngawngah': ('ngawng-ah', 'neck-LOC'),               # 14x - "at neck"
        'tawite': ('tawi-te', 'short-PL'),                   # 14x - "short ones"
        'gunte': ('gun-te', 'river-PL'),                     # 14x - "rivers"
        'kilamdanna': ('ki-lam-dan-na', 'REFL-way-manner-NMLZ'), # 14x - "behavior"
        'denna': ('den-na', 'judge-NMLZ'),                   # 14x - "judgment"
        'vengte\'': ('veng-te\'', 'guard-PL.POSS'),          # 14x - "guards'"
        'gawina': ('gawi-na', 'burn-NMLZ'),                  # 14x - "burning"
        'ui': ('ui', 'dog'),                                 # 14x - "dog"
        'dingto': ('ding-to', 'stand-sit'),                  # 14x - "stand/sit"
        'dangtakin': ('dang-tak-in', 'other-true-ERG'),      # 14x - "differently"
        'sinso': ('sin-so', 'die-remain'),                   # 14x - "remnant"
        'puakhia-in': ('puak-hia-in', 'send-away-ERG'),      # 14x - "sending"
        'suante\'': ('suan-te\'', 'lineage-PL.POSS'),        # 14x - "descendants'"
        'zaw-in': ('zaw-in', 'able-ERG'),                    # 14x - "being able"
        'siansuah': ('sian-suah', 'holy-redeem'),            # 14x - compound
        'paihkhiat': ('paih-khiat', 'go-depart'),            # 14x - "departed"
        'leengguite': ('leeng-gui-te', 'chariot-wheel-PL'),  # 14x - "chariots"
        'hatzaw': ('hat-zaw', 'strong-more'),                # 14x - "stronger"
        'tawmna': ('tawm-na', 'short-NMLZ'),                 # 14x - "shortness"
        'galhiamte': ('gal-hiam-te', 'enemy-?-PL'),          # 14x - compound
        'ankung': ('an-kung', '3PL-tree'),                   # 14x - "their tree"
        'hazatna': ('ha-zat-na', 'hot-?-NMLZ'),              # 14x - compound
        'lunggim': ('lung-gim', 'heart-round'),              # 14x - "whole heart"
        'ma-un': ('ma-un', 'that-?'),                        # 14x - compound
        'kulhkongpite': ('kulh-kong-pi-te', 'wall-road-big-PL'), # 14x - "walls"
        'khathei': ('kha-thei', 'one-able'),                 # 14x - "can one"
        'tauna': ('tau-na', 'store-NMLZ'),                   # 14x - "storing"
        'kahto-in': ('ka-hto-in', '1SG-ascend-ERG'),         # 14x - "I ascending"
        'sawmsim': ('sawm-sim', 'ten-count'),                # 14x - "count by tens"
        'mawkmawkte': ('mawk-mawk-te', 'empty~empty-PL'),    # 14x - "empty ones"
        'galvilna': ('gal-vil-na', 'enemy-encircle-NMLZ'),   # 14x - "battle array"
        'ngaihsutsa': ('ngaihsut-sa', 'think-PAST'),         # 14x - "thought" (duplicate removed)
        'koihnate': ('koih-na-te', 'put-NMLZ-PL'),           # 14x - "placements"
        'lianpipi': ('lian-pi-pi', 'big-big-big'),           # 14x - "very great"
        'kulhte': ('kulh-te', 'wall-PL'),                    # 14x - "walls"
        'uksawn': ('uk-sawn', 'rule-throne'),                # 14x - "throne"
        'pakta': ('pak-ta', 'share-stay'),                   # 14x - compound
        'kidenna': ('ki-den-na', 'REFL-judge-NMLZ'),         # 14x - "self-judgment"
        'vanpi': ('van-pi', 'heaven-big'),                   # 14x - "great heaven"
        'hithei': ('hi-thei', 'be-able'),                    # 14x - "can be"
        'sikkhau': ('sik-khau', 'repent-?'),                 # 14x - compound
        'palikte': ('pa-lik-te', 'father-?-PL'),             # 14x - compound
        
        # === Session 4 Round 14: 13x frequency vocabulary ===
        'husanna': ('husa-nna', 'flood-NMLZ'),               # 13x - "flood"
        'dawnte': ('dawn-te', 'receive-PL'),                 # 13x - "waters/months"
        'ciing': ('ciing', 'barren'),                        # 13x - "barren"
        'tengkhawm': ('teng-khawm', 'dwell-together'),       # 13x - "dwell together"
        'tuikuang': ('tui-kuang', 'water-trough'),           # 13x - "trough"
        'nihvei': ('nih-vei', 'two-time'),                   # 13x - "two times"
        'leengkhia': ('leeng-khia', 'chariot-exit'),         # 13x - "break/depart"
        'valhtum': ('valh-tum', 'go.and-swallow'),           # 13x - "devoured"
        'hehpihhuai': ('hehpih-huai', 'angry-dread'),        # 13x - "ill favoured"
        'gentel': ('gen-tel', 'speak-help'),                 # 13x - "told"
        'zatui': ('za-tui', 'hear.I-water'),                 # 13x - "embalm"
        'tamna': ('tam-na', 'many-NMLZ'),                    # 13x - "abundance"
        'laktel': ('lak-tel', 'take-help'),                  # 13x - "cast"
        'kualte': ('kual-te', 'side-PL'),                    # 13x - "sides"
        'sihlawh': ('sih-lawh', 'die-unclean'),              # 13x - "uncleanness"
        'dialkhai': ('dial-khai', 'call-pitch'),             # 13x - "pitch tents"
        'kidalna': ('ki-dal-na', 'REFL-hinder-NMLZ'),        # 13x - "charge"
        'galhangte': ('gal-hang-te', 'enemy-battle-PL'),     # 13x - "warriors"
        'kipahna': ('ki-pah-na', 'REFL-joy-NMLZ'),           # 13x - "joyfulness"
        'kihihsakna': ('ki-hih-sak-na', 'REFL-do-CAUS-NMLZ'), # 13x - "arrogancy"
        'mualah': ('mual-ah', 'hill-LOC'),                   # 13x - "on the hill"
        'ven\'': ('ven\'', 'protect.POSS'),                  # 13x - "protection"
        'nat': ('nat', 'sick'),                              # 13x - "sick"
        'muat': ('muat', 'see.I.CONT'),                      # 13x - "seeing"
        'mut': ('mut', 'see.I.SHORT'),                       # 13x - "see"
        'nawl': ('nawl', 'place'),                           # 13x - "place"
        'uite': ('ui-te', 'dog-PL'),                         # 13x - "dogs"
        'cikmahin': ('cik-mah-in', 'one-self-ERG'),          # 13x - "oneself"
        '-a\'': ('-a\'', 'LOC.POSS'),                        # 13x - compound
        'hingin': ('hing-in', 'live-ERG'),                   # 13x - "living"
        'gensia-in': ('gen-sia-in', 'speak-bad-ERG'),        # 13x - "speaking ill"
        'hilhkholhna': ('hilh-kholh-na', 'teach-denounce-NMLZ'), # 13x - "teaching"
        'kamsung': ('kam-sung', 'mouth-inside'),             # 13x - "in mouth"
        'kamciamna': ('kam-ciam-na', 'mouth-promise-NMLZ'),  # 13x - "oath"
        'siksanin': ('sik-san-in', 'repent-?-ERG'),          # 13x - compound
        'sangzaw': ('sang-zaw', 'high-more'),                # 13x - "higher"
        'genthuah': ('gen-thuah', 'speak-?'),                # 13x - compound
        'khuate-ah': ('khua-te-ah', 'town-PL-LOC'),          # 13x - "in towns"
        'thakte': ('thak-te', 'new-PL'),                     # 13x - "new ones"
        'innkhum': ('inn-khum', 'house-cover'),              # 13x - "house roof"
        'bawlnate': ('bawl-na-te', 'make-NMLZ-PL'),          # 13x - "works"
        'otna': ('ot-na', 'keep-NMLZ'),                      # 13x - "keeping"
        'awngin': ('awng-in', 'void-ERG'),                   # 13x - "empty"
        'luh': ('luh', 'head/enter'),                        # 13x - "head"
        'muangin': ('muang-in', 'trust-ERG'),                # 13x - "trusting"
        'khebaite': ('kheba-i-te', '?-?-PL'),                # 13x - compound
        'daltuahte': ('dal-tuah-te', 'hinder-meet-PL'),      # 13x - "opponents"
        'omtheih': ('om-theih', 'exist-able'),               # 13x - "able to exist"
        'siazaw': ('sia-zaw', 'bad-more'),                   # 13x - "worse"
        'theihtheih': ('theih-theih', 'know.II~know.II'),    # 13x - "knowing"
        
        # === Session 4 Round 15: 12x frequency vocabulary ===
        'cil-in': ('cil-in', 'begin-ERG'),                   # 12x - "in beginning"
        'migi': ('mi-gi', 'person-evil'),                    # 12x - "wicked person"
        'paii': ('paii', 'sorrow'),                          # 12x - "sorrow"
        'piangkhia': ('piang-khia', 'be.born-exit'),         # 12x - "brought forth"
        'thunget': ('thu-nget', 'word-request'),             # 12x - "speaking/praying"
        'khiasuk': ('khia-suk', 'exit-make.become'),         # 12x - "let down"
        'lungngaingai': ('lung-ngai-ngai', 'heart-think~think'), # 12x - "meditate"
        'matsa': ('mat-sa', 'grasp-meat'),                   # 12x - "venison"
        'bawngpi': ('bawng-pi', 'cattle-big'),               # 12x - "milch cow"
        'theihkholh': ('theih-kholh', 'know.II-denounce'),   # 12x - "sore"
        'lunghihmawh': ('lung-hih-mawh', 'heart-do-sin'),    # 12x - "knew not"
        'kimuhna': ('ki-muh-na', 'REFL-see.II-NMLZ'),        # 12x - "found"
        'numeino': ('numei-no', 'woman-young'),              # 12x - "maid"
        'khuhcip': ('khuh-cip', 'cover-trap'),               # 12x - "entangled"
        'theihtel': ('theih-tel', 'know.II-help'),           # 12x - "understand"
        'khumcip': ('khum-cip', 'cover-push'),               # 12x - "push/horn"
        'satnen': ('sat-nen', 'strike-?'),                   # 12x - "bow down"
        'thumang': ('thu-mang', 'word-chief'),               # 12x - "covenant"
        'kizopna': ('ki-zop-na', 'REFL-join-NMLZ'),          # 12x - "joining"
        'neikhawm': ('nei-khawm', 'have-together'),          # 12x - "keep together"
        'maimangsak': ('mai-mang-sak', 'face-chief-CAUS'),   # 12x - "destroy name"
        'diakdiakin': ('diak-diak-in', 'different~different-ERG'), # 12x - "secretly"
        'pahin': ('pa-hin', 'father-this'),                  # 12x - compound
        'itzaw': ('it-zaw', 'love-more'),                    # 12x - "love more"
        'kawi-in': ('kawi-in', 'forth-ERG'),                 # 12x - "going forth"
        'biakpiakna-in': ('biak-piak-na-in', 'worship-give.to-NMLZ-ERG'), # 12x - "worshipping"
        'khiam': ('khiam', 'narrow'),                        # 12x - "narrow/exit"
        'uiphukte': ('ui-phuk-te', 'dog-?-PL'),              # 12x - compound
        'deihna-in': ('deih-na-in', 'want-NMLZ-ERG'),        # 12x - "wanting"
        'sunte': ('sun-te', 'long-PL'),                      # 12x - "long ones"
        'vengpa\'': ('veng-pa\'', 'guard-father.POSS'),      # 12x - "guardian's"
        'sahpi': ('sah-pi', 'witness-big'),                  # 12x - "great witness"
        'vankhainate': ('van-khai-na-te', 'heaven-?-NMLZ-PL'), # 12x - compound
        'zalin': ('zal-in', 'spread-ERG'),                   # 12x - "spreading"
        'multe': ('mul-te', 'see.I-PL'),                     # 12x - "seers"
        'ki-em': ('ki-em', 'REFL-?'),                        # 12x - compound
        'kangin': ('kang-in', 'generation-ERG'),             # 12x - "in generation"
        'mawhte': ('mawh-te', 'sin-PL'),                     # 12x - "sins"
        'kampaunate': ('kam-pau-na-te', 'mouth-speak-NMLZ-PL'), # 12x - "speeches"
        'paisuakin': ('pai-suak-in', 'go-become-ERG'),       # 12x - "going"
        'piaknate': ('piak-na-te', 'give.to-NMLZ-PL'),       # 12x - "givings"
        'salte': ('sal-te', 'servant-PL'),                   # 12x - "servants"
        'suangtumte': ('suang-tum-te', 'stone-whole-PL'),    # 12x - "whole stones"
        'kalsuanna': ('kal-suan-na', '1SG-lineage-NMLZ'),    # 12x - compound
        'simsak': ('sim-sak', 'count-CAUS'),                 # 12x - "cause to count"
        'gamteng': ('gam-teng', 'land-all'),                 # 12x - "all lands"
        'innpi': ('inn-pi', 'house-big'),                    # 12x - "great house"
        'thungen': ('thu-ngen', 'word-prayer'),              # 12x - "prayer word"
        'niamkhiat': ('niam-khiat', 'low-depart'),           # 12x - "humbled"
        'citengah': ('ci-teng-ah', 'say-all-LOC'),           # 12x - "saying all"
        'paikawmin': ('pai-kawm-in', 'go-?-ERG'),            # 12x - compound
        'sikhawm': ('si-khawm', 'die-together'),             # 12x - "die together"
        'khausai': ('khau-sai', 'spirit-?'),                 # 12x - compound
        'sawmthumte': ('sawm-thum-te', 'ten-three-PL'),      # 12x - "thirteens"
        'ngawn': ('ngawn', 'roar'),                          # 12x - "roar"
        'unok': ('u-nok', 'elder.sibling-younger'),          # 12x - "siblings"
        'sangpen': ('sang-pen', 'high-SUPER'),               # 12x - "highest"
        
        # === Session 4 Round 16: 11-12x frequency vocabulary ===
        'hunte-ah': ('hun-te-ah', 'time-PL-LOC'),            # 12x - "at times/unto"
        'tuutalte': ('tuut-al-te', 'hand-?-PL'),             # 12x - "hands"
        'kikupna': ('ki-kup-na', 'REFL-counsel-NMLZ'),       # 12x - "counsel"
        'sumbuk': ('sum-buk', 'money-bundle'),               # 12x - "silver"
        'kiniamkhiatna': ('ki-niam-khiat-na', 'REFL-humble-depart-NMLZ'), # 12x - "humbling"
        'khahsuah': ('khah-suah', 'choke-redeem'),           # 12x - "appointed"
        'lungdamkohna': ('lungdam-koh-na', 'rejoice-?-NMLZ'), # 12x - "thanksgiving"
        'lakkhiatsak': ('lak-khiat-sak', 'take-depart-CAUS'), # 12x - "took off"
        'uksak': ('uk-sak', 'rule-CAUS'),                    # 12x - "let down"
        'tausangte': ('tau-sang-te', 'store-high-PL'),       # 12x - "treasures"
        'hanthotna': ('han-thot-na', 'follow-?-NMLZ'),       # 12x - "conspiracy"
        'nungngat': ('nung-ngat', 'live-sit'),               # 12x - "sat down"
        'annekna': ('an-nek-na', '3PL-eat.II-NMLZ'),         # 12x - "banquet"
        'zaizai': ('zai-zai', 'song~song'),                  # 12x - "light/neesings"
        'luitui': ('lui-tui', 'river-water'),                # 12x - "streams"
        'gamtang': ('gam-tang', 'land-force'),               # 11x - "creatures"
        'neisak': ('nei-sak', 'have-CAUS'),                  # 11x - "let have"
        'zaina': ('zai-na', 'song-NMLZ'),                    # 11x - "fashion"
        'gimpiakna': ('gim-piak-na', 'toil-give.to-NMLZ'),   # 11x - "hastening"
        'tuiluang': ('tui-luang', 'water-flow'),             # 11x - "gutters"
        'ciangah': ('ci-ang-ah', 'say-FUT-LOC'),             # 11x - "saying"
        'galmatte': ('gal-mat-te', 'enemy-grasp-PL'),        # 11x - "warriors"
        'tuhuna': ('tu-hun-a', 'now-time-LOC'),              # 11x - "at this time"
        'nakpi-in': ('nak-pi-in', 'time-big-ERG'),           # 11x - "greatly"
        'uzaw': ('u-zaw', 'elder.sibling-more'),             # 11x - "elder more"
        'cihsa': ('cih-sa', 'say.NOM-early'),                # 11x - "said before"
        'ei\'': ('ei\'', '1PL.EXCL.POSS'),                   # 11x - "our"
        'khengin': ('kheng-in', 'divide-ERG'),               # 11x - "dividing"
        'khapna': ('khap-na', 'forbid-NMLZ'),                # 11x - "forbidding"
        'khainiang': ('khai-niang', 'hold-young'),           # 11x - "hold young"
        'mukhia': ('mu-khia', 'see.I-exit'),                 # 11x - "appear"
        'zawnna': ('zawn-na', 'poor-NMLZ'),                  # 11x - "poverty"
        'dinna': ('din-na', 'stand-NMLZ'),                   # 11x - "standing"
        'nisim': ('ni-sim', 'day-count'),                    # 11x - "count days"
        'kidong': ('ki-dong', 'REFL-reach'),                 # 11x - "reach"
        'sungkuate': ('sung-kua-te', 'inside-who-PL'),       # 11x - "those inside"
        'vatlum': ('vat-lum', 'go.quickly-round'),           # 11x - "go around"
        'paikhiatpihna': ('pai-khiat-pih-na', 'go-depart-APPL-NMLZ'), # 11x - "departure"
        'nitum': ('ni-tum', 'day-full'),                     # 11x - "full day"
        'vatmai': ('vat-mai', 'go.quickly-face'),            # 11x - "quickly face"
        'zawngkhal': ('zawng-khal', 'poor-famine'),          # 11x - "famine poor"
        'hingkhawi': ('hing-khawi', 'live-?'),               # 11x - compound
        'omsuak': ('om-suak', 'exist-become'),               # 11x - "become"
        'bilvang': ('bil-vang', 'ear-strength'),             # 11x - "ear"
        'peekte': ('peek-te', 'measure-PL'),                 # 11x - "measures"
        'khetphimte': ('khet-phim-te', '?-?-PL'),            # 11x - compound
        'dialpi': ('dial-pi', 'call-big'),                   # 11x - "great call"
        'suangpeekte': ('suang-peek-te', 'stone-measure-PL'), # 11x - "stone measures"
        'maisakin': ('mai-sak-in', 'face-CAUS-ERG'),         # 11x - "facing"
        'khahkhong': ('khah-khong', 'choke-?'),              # 11x - compound
        'vakhuno': ('va-khu-no', 'go.and-?-young'),          # 11x - compound
        'sathaute': ('sat-hau-te', 'strike-rich-PL'),        # 11x - compound
        'biakna-a': ('biak-na-a', 'worship-NMLZ-LOC'),       # 11x - "at worship"
        'paang': ('paang', 'father.?'),                      # 11x - compound
        'hawmsak': ('hawm-sak', 'join-CAUS'),                # 11x - "cause to join"
        'tualsung': ('tual-sung', 'floor-inside'),           # 11x - "courtyard"
        'sihpih': ('sih-pih', 'die-APPL'),                   # 11x - "die with"
        'puasak': ('pua-sak', 'carry.back-CAUS'),            # 11x - "cause to carry"
        'hauh': ('hauh', 'rich.PL'),                         # 11x - "rich ones"
        'kampaute': ('kam-pau-te', 'mouth-speak-PL'),        # 11x - "speakers"
        'luahsak': ('luah-sak', 'head-CAUS'),                # 11x - "cause to head"
        'utthu': ('ut-thu', 'want-word'),                    # 11x - "will/desire"
        'makaihna': ('ma-kaih-na', 'that-lead-NMLZ'),        # 11x - "leadership"
        'nate-ah': ('na-te-ah', '2SG-PL-LOC'),               # 11x - "at your"
        'citna': ('cit-na', 'say-NMLZ'),                     # 11x - "saying"
        'kahtohna': ('ka-htoh-na', '1SG-ascend-NMLZ'),       # 11x - "my ascending"
        'thatmang': ('that-mang', 'kill-chief'),             # 11x - "kill utterly"
        'delhna': ('delh-na', 'hide-NMLZ'),                  # 11x - "hiding"
        'kherub-te\'': ('kherub-te\'', 'cherub-PL.POSS'),    # 12x - "cherubim's"
        'paknamtuite': ('pak-nam-tui-te', 'share-nation-water-PL'), # 12x - compound
        'pawite': ('paw-i-te', 'father-?-PL'),               # 12x - compound
        'awte': ('aw-te', 'voice-PL'),                       # 12x - "voices"
        'hihtheih': ('hih-theih', 'do-able'),                # 12x - "doable"
        
        # === Session 4 Round 17: 10x frequency vocabulary ===
        'tawlette': ('tawl-et-te', '?-?-PL'),                # 10x - "seventeenth"
        'peuhmahte': ('peuh-mah-te', 'each-self-PL'),        # 10x - "whoso/everyone"
        'maingat': ('mai-ngat', 'face-sit'),                 # 10x - "shoulders"
        'sempa': ('sem-pa', 'serve-father'),                 # 10x - "servant"
        'lumlet': ('lum-let', 'warm-return'),                # 10x - "overthrow"
        'lumsuk': ('lum-suk', 'warm-make.become'),           # 10x - "lighted/tarried"
        'hanciamna': ('han-ciam-na', 'follow-promise-NMLZ'), # 10x - "wrestlings"
        'tuangsak': ('tuang-sak', 'ride-CAUS'),              # 10x - "set upon"
        'dangka': ('dang-ka', 'other-?'),                    # 10x - "parcel"
        'khiatsak': ('khiat-sak', 'depart-CAUS'),            # 10x - "cause to wander"
        'keusak': ('keu-sak', 'dig-CAUS'),                   # 10x - "blasted"
        'sial': ('sial', 'carcass'),                         # 10x - "carcass"
        'mualpang': ('mual-pang', 'hill-?'),                 # 10x - "portion"
        'gammang': ('gam-mang', 'land-chief'),               # 10x - "astray"
        'gamtasak': ('gamta-sak', 'send.away-CAUS'),         # 10x - "cause to come"
        'siluang': ('si-luang', 'die-flow'),                 # 10x - "high places"
        'zahtakhuai': ('zahtak-huai', 'honor-dread'),        # 10x - "honourable"
        'satkham': ('sat-kham', 'strike-forbid'),            # 10x - "nigh"
        'tumna': ('tum-na', 'full-NMLZ'),                    # 10x - "mountain"
        'ensuk': ('en-suk', 'look-make.become'),             # 10x - "look down"
        'lampial': ('lam-pial', 'way-spot'),                 # 10x - "spot"
        'thatanghat': ('tha-tang-hat', 'strength-force-hard'), # 10x - "burn"
        'silsak': ('sil-sak', 'clothe-CAUS'),                # 10x - "bowed"
        'lungdampih': ('lungdam-pih', 'rejoice-APPL'),       # 10x - "salute/bless"
        'kai-in': ('kai-in', 'pull-ERG'),                    # 10x - "pulling"
        'thutangin': ('thu-tang-in', 'word-force-ERG'),      # 10x - compound
        'munin': ('mun-in', 'place-ERG'),                    # 10x - "in place"
        'zakna-ah': ('zak-na-ah', 'hear.II-NMLZ-LOC'),       # 10x - "at hearing"
        'lingin': ('ling-in', 'hope-ERG'),                   # 10x - "hoping"
        'almond': ('almond', 'almond'),                      # 10x - "almond" (loan)
        'tute': ('tut-e', 'sleep-?'),                        # 10x - compound
        'khawi': ('khawi', 'where'),                         # 10x - "where"
        'khen\'': ('khen\'', 'divide.POSS'),                 # 10x - "division"
        'hihin': ('hih-in', 'this-ERG'),                     # 10x - "this"
        'kongpuankhai': ('kong-puan-khai', '1SG→3-carry-?'), # 10x - compound
        'luahin': ('luah-in', 'head-ERG'),                   # 10x - "heading"
        'puanbukah': ('puan-buk-ah', 'cloth-cover-LOC'),     # 10x - "in tent"
        'palsatin': ('pal-sat-in', '?-strike-ERG'),          # 10x - compound
        'nate\'': ('na-te\'', '2SG-PL.POSS'),                # 10x - "your (pl)"
        'kattum': ('kat-tum', 'catch-full'),                 # 10x - compound
        'lawn\'': ('lawn\'', 'easy.POSS'),                   # 10x - "easy"
        'nit': ('nit', 'day.SHORT'),                         # 10x - "day"
        'gensiate': ('gen-sia-te', 'speak-bad-PL'),          # 10x - "evil speakers"
        'khenkhat': ('khen-khat', 'divide-one'),             # 10x - "one part"
        'nilkhia': ('nil-khia', 'day-exit'),                 # 10x - compound
        'phate': ('pha-te', 'good-PL'),                      # 10x - "good ones"
        'gensiat': ('gen-siat', 'speak-destroy'),            # 10x - "speak ill"
        'gamh-in': ('gamh-in', 'land-ERG'),                  # 10x - compound
        'lingte': ('ling-te', 'hope-PL'),                    # 10x - "hopes"
        'songte': ('song-te', 'tall-PL'),                    # 10x - "tall ones"
        'komau\'': ('ko-mau\'', 'call-3PL.POSS'),            # 10x - "their calling"
        'cingh': ('cingh', 'say.?'),                         # 10x - compound
        'nihun': ('ni-hun', 'day-time'),                     # 10x - "day time"
        'lungkhamin': ('lungkham-in', 'courage-ERG'),        # 10x - "encouraged"
        'siatnate': ('siat-na-te', 'spoil-NMLZ-PL'),         # 10x - "spoilings"
        'mukha': ('mu-kha', 'see.I-?'),                      # 10x - compound
        'apsa': ('ap-sa', 'press-early'),                    # 10x - compound
        'neulai': ('neu-lai', 'small-middle'),               # 10x - compound
        'khempeuha': ('khem-peuh-a', 'restrain-all-LOC'),    # 10x - "all restrained"
        'kalhna': ('kalh-na', 'go-NMLZ'),                    # 10x - "going"
        'innliim': ('inn-liim', 'house-?'),                  # 10x - compound
        'kigente': ('ki-gen-te', 'REFL-speak-PL'),           # 10x - "conversations"
        'khutnuai-a': ('khut-nuai-a', 'hand-under-LOC'),     # 10x - "under hand"
        'patau': ('pa-tau', 'father-store'),                 # 10x - compound
        'sazian': ('sa-zian', 'meat-?'),                     # 10x - compound
        'puakkhiat': ('puak-khiat', 'send-depart'),          # 10x - "send away"
        'niliim': ('ni-liim', 'day-?'),                      # 10x - compound
        'namsau-in': ('nam-sau-in', 'nation-long-ERG'),      # 10x - compound
        'zahpih': ('zah-pih', 'fear-APPL'),                  # 10x - "fear with"
        'awgingte': ('awging-te', 'voice-PL'),               # 10x - "voices"
        
        # === Session 4 Round 18: Push to 97% ===
        'tawlette': ('tawl-et-te', 'seven-?-PL'),            # 10x - "seventeenth"
        'tute': ('tu-te', 'now-PL'),                         # 10x - compound
        'dangka': ('dang-ka', 'other-one'),                  # 10x - "parcel"
        'mualpang': ('mual-pang', 'hill-side'),              # 10x - "portion"
        'khen\'': ('khen\'', 'divide.POSS'),                 # 10x - "division"
        'kongpuankhai': ('kong-puan-khai', '1SG→3-cloth-?'), # 10x - compound
        'palsatin': ('pal-sat-in', '?-strike-ERG'),          # 10x - compound
        'nate\'': ('na-te\'', '2SG-PL.POSS'),                # 10x - "your (pl)"
        'lawn\'': ('lawn\'', 'easy.POSS'),                   # 10x - compound
        'komau\'': ('ko-mau\'', 'call-3PL.POSS'),            # 10x - "their calling"
        'cingh': ('cingh', 'say.COMP'),                      # 10x - compound
        'mukha': ('mu-kha', 'see.I-place'),                  # 10x - compound
        'innliim': ('inn-liim', 'house-feast'),              # 10x - compound
        'sazian': ('sa-zian', 'meat-roast'),                 # 10x - compound
        'niliim': ('ni-liim', 'day-feast'),                  # 10x - compound
        'kiciang': ('ki-ciang', 'REFL-announce'),            # 10x - "announce self"
        'cihmawh': ('cih-mawh', 'say.NOM-sin'),              # 10x - "slander"
        'husan\'': ('husan\'', 'flood.POSS'),                # 10x - "flood's"
        'sikkol': ('sik-kol', 'repent-?'),                   # 10x - compound
        'khauhin': ('khau-hin', 'spirit-this'),              # 10x - "this spirit"
        'hilhnate': ('hilh-na-te', 'teach-NMLZ-PL'),         # 10x - "teachings"
        'kisialhna': ('ki-sialh-na', 'REFL-sin-NMLZ'),       # 10x - "sinning"
        'cihmawhna': ('cih-mawh-na', 'say.NOM-sin-NMLZ'),    # 10x - "slander"
        'zuazua': ('zua-zua', 'prepare~prepare'),            # 10x - "preparing"
        'semkhia': ('sem-khia', 'serve-exit'),               # 10x - "serve out"
        'innkiu': ('inn-kiu', 'house-corner'),               # 10x - "house corner"
        'piathuah': ('pia-thuah', 'give-put'),               # 10x - compound
        'mawhnopna': ('mawh-nop-na', 'sin-want-NMLZ'),       # 10x - "sin desire"
        'thatnuam': ('that-nuam', 'kill-want'),              # 10x - "want to kill"
        'naupangnote': ('nau-pang-no-te', 'child-?-young-PL'), # 10x - compound
        'uppih': ('u-pih', 'elder.sibling-APPL'),            # 10x - "with elder"
        'kawtsak': ('kawt-sak', 'garden-CAUS'),              # 9x - "water garden"
        'nuainung': ('nuai-nung', 'under-back'),             # 9x - compound
        'khukte': ('khuk-te', 'corner-PL'),                  # 9x - "corners"
        'laksa': ('lak-sa', 'take-early'),                   # 9x - "taken before"
        'kilatna': ('ki-lat-na', 'REFL-?-NMLZ'),             # 9x - compound
        'hoihnono': ('hoih-no-no', 'good-young-young'),      # 9x - "very good"
        'hehnepna': ('heh-nep-na', 'angry-?-NMLZ'),          # 9x - compound
        'sanin': ('san-in', 'high-ERG'),                     # 9x - "highly"
        'nauzaw': ('nau-zaw', 'child-more'),                 # 9x - "younger"
        'ngahsa': ('ngah-sa', 'get-early'),                  # 9x - "got before"
        'koihkhia': ('koih-khia', 'put-exit'),               # 9x - "put out"
        'bilbahte': ('bil-bah-te', 'ear-deaf-PL'),           # 9x - "deaf ears"
        'inncing': ('inn-cing', 'house-clean'),              # 9x - "clean house"
        'kimangngilh': ('ki-mang-ngilh', 'REFL-forget-?'),   # 9x - "forget self"
        'zungbuh': ('zung-buh', 'root-rice'),                # 9x - compound
        'antang': ('an-tang', '3PL-force'),                  # 9x - "their force"
        'piazaw': ('pia-zaw', 'give-more'),                  # 9x - "give more"
        'milip': ('mi-lip', 'person-crowd'),                 # 9x - "multitude"
        'tuili': ('tui-li', 'water-?'),                      # 9x - compound
        
        # === Session 4 Round 19: Final push to 97% ===
        'kilatna': ('ki-lat-na', 'REFL-strong-NMLZ'),        # 9x - "strengthening"
        'hehnepna': ('heh-nep-na', 'angry-?-NMLZ'),          # 9x - "anger"
        'kimangngilh': ('ki-mang-ngilh', 'REFL-forget-?'),   # 9x - "forgetting"
        'zuautat': ('zuau-tat', 'prepare-?'),                # 9x - compound
        'vatgawpin': ('vat-gawp-in', 'go.quickly-grasp-ERG'), # 9x - "quickly grasp"
        'kauphete': ('kau-phe-te', 'call-?-PL'),             # 9x - compound
        'lohte': ('loh-te', 'field-PL'),                     # 9x - "fields"
        'gin\'': ('gin\'', 'gong.POSS'),                     # 9x - "gong's"
        'cinatna': ('ci-nat-na', 'say-sick-NMLZ'),           # 9x - compound
        'keelmul': ('keel-mul', 'heel-tip'),                 # 9x - "heel tip"
        'taitehte': ('tai-teh-te', '?-measure-PL'),          # 9x - compound
        'nawlnung': ('nawl-nung', 'place-back'),             # 9x - "back place"
        'siampipuan\'': ('siampi-puan\'', 'priest-cloth.POSS'), # 9x - "priest's robe"
        'kibulh': ('ki-bulh', 'REFL-root'),                  # 9x - "rooted"
        'kisan\'': ('ki-san\'', 'REFL-high.POSS'),           # 9x - compound
        'silhsakin': ('silh-sak-in', 'clothe-CAUS-ERG'),     # 9x - "clothing"
        'khim': ('khim', 'edge'),                            # 9x - "edge"
        'kipsakna': ('ki-psa-kna', 'REFL-?-NMLZ'),           # 9x - compound
        'puankhai': ('puan-khai', 'cloth-lift'),             # 9x - "lift cloth"
        'bukkong': ('buk-kong', 'ambush-road'),              # 9x - "ambush place"
        'nai-a': ('nai-a', 'near-LOC'),                      # 9x - "nearby"
        'siansuahna': ('sian-suah-na', 'holy-redeem-NMLZ'),  # 9x - "redemption"
        'kihhuaina': ('ki-hhuai-na', 'REFL-dread-NMLZ'),     # 9x - "dread"
        'poina': ('poi-na', 'feast-NMLZ'),                   # 9x - "feast"
        'kisehte': ('ki-seh-te', 'REFL-slice-PL'),           # 9x - compound
        'phulakna': ('phu-lak-na', '?-take-NMLZ'),           # 9x - compound
        'thute-ah': ('thu-te-ah', 'word-PL-LOC'),            # 9x - "in words"
        'cilna': ('cil-na', 'begin-NMLZ'),                   # 9x - "beginning"
        'anlim': ('an-lim', '3PL-feast'),                    # 9x - "their feast"
        'kawmah': ('kawm-ah', 'beam-LOC'),                   # 9x - "at beam"
        'tuahkhak': ('tuah-khak', 'meet-give.command'),      # 9x - compound
        'pammaih': ('pam-maih', 'all-face'),                 # 9x - compound
        'phuh': ('phuh', 'blow'),                            # 9x - "blow"
        'vah': ('vah', 'go.and.?'),                          # 9x - compound
        'buakhia': ('buak-hia', 'fight-away'),               # 9x - "fight away"
        'sanang': ('sa-nang', 'meat-2SG'),                   # 9x - compound
        'saupi': ('sau-pi', 'long-big'),                     # 9x - "very long"
        'aisante': ('ai-san-te', '3SG-high-PL'),             # 9x - compound
        'sihsak': ('sih-sak', 'die-CAUS'),                   # 9x - "cause to die"
        'sukgawp': ('suk-gawp', 'make.become-grasp'),        # 9x - compound
        'paipihsuk': ('pai-pih-suk', 'go-APPL-make.become'), # 9x - compound
        'innkhumzang': ('inn-khum-zang', 'house-cover-use'), # 9x - compound
        'gamtatsiat': ('gamtat-siat', 'kingdom-destroy'),    # 9x - "destroy kingdom"
        'kitangsapna': ('ki-tang-sap-na', 'REFL-force-call-NMLZ'), # 9x - compound
        'omkhak': ('om-khak', 'exist-command'),              # 9x - compound
        'lakkhia': ('lak-khia', 'take-exit'),                # 9x - "take out"
        'nawt': ('nawt', '2SG.?'),                           # 9x - compound
        'ukpa\'': ('uk-pa\'', 'rule-father.POSS'),           # 9x - "ruler's"
        'genkhiat': ('gen-khiat', 'speak-depart'),           # 9x - "speak and depart"
        'lungmang': ('lung-mang', 'heart-forget'),           # 9x - "forget heart"
        'suaksakin': ('suak-sak-in', 'become-CAUS-ERG'),     # 9x - "causing to become"
        'lutsak': ('lut-sak', 'enter-CAUS'),                 # 9x - "cause to enter"
        'vatin': ('vat-in', 'go.quickly-ERG'),               # 9x - "going quickly"
        'diktat': ('dik-tat', 'righteous-strike'),           # 9x - compound
        'samkhia': ('sam-khia', 'call-exit'),                # 9x - "call out"
        'munmuanhuaite': ('mun-muan-huai-te', 'place-trust-dread-PL'), # 9x - compound
        'omlaiteng': ('om-lai-teng', 'exist-middle-all'),    # 9x - "exist among all"
        'guallel': ('gual-lel', 'friend-?'),                 # 9x - compound
        'sukkhak': ('suk-khak', 'make.become-command'),      # 9x - compound
        
        # === Session 4 Round 20: Push clearly over 97% ===
        'hehnepna': ('heh-nep-na', 'angry-soft-NMLZ'),       # 9x - "wrath"
        'kimangngilh': ('ki-mang-ngilh', 'REFL-chief-forget'), # 9x - "forgetting"
        'tuili': ('tui-li', 'water-flow'),                   # 9x - "water flow"
        'zuautat': ('zuau-tat', 'prepare-strike'),           # 9x - compound
        'kauphete': ('kau-phe-te', 'call-?-PL'),             # 9x - compound
        'gin\'': ('gin\'', 'gong.POSS'),                     # 9x - "gong's"
        'taitehte': ('tai-teh-te', 'cut-measure-PL'),        # 9x - compound
        'siampipuan\'': ('siampi-puan\'', 'priest-cloth.POSS'), # 9x - "priest's robe"
        'kisan\'': ('ki-san\'', 'REFL-high.POSS'),           # 9x - compound
        'kipsakna': ('ki-psak-na', 'REFL-bless-NMLZ'),       # 9x - "blessing"
        'phulakna': ('phu-lak-na', 'carry-take-NMLZ'),       # 9x - compound
        'vah': ('vah', 'go.quickly'),                        # 9x - "go quickly"
        'nawt': ('nawt', 'push'),                            # 9x - "push"
        'ukpa\'': ('uk-pa\'', 'ruler-father.POSS'),          # 9x - "ruler's"
        'guallel': ('gual-lel', 'friend-return'),            # 9x - compound
        
        # === Session 5: Quality-focused expansion (2026-03-07) ===
        # Goal: Careful additions with full philological verification
        
        # Ki- verbs discovered via KJV cross-reference
        'kinawh': ('ki-nawh', 'REFL-hurry'),                 # 8x - "hasten" (GEN 19:15)
        'kikholh': ('ki-kholh', 'REFL-accompany'),           # 8x - "be with" (GEN 24:32)
        'kilawi': ('ki-lawi', 'REFL-dislocate'),             # 8x - "out of joint" (GEN 32:25)
        'kidiah': ('ki-diah', 'REFL-dip'),                   # 8x - "be put in water" (LEV 11:32)
        'kikhin': ('ki-khin', 'REFL-move'),                  # 8x - "set forward" (NUM 1:51)
        'kiphah': ('ki-phah', 'REFL-spread'),                # 8x - "spread forth" (NUM 24:6)
        'kisut': ('ki-sut', 'REFL-spoil'),                   # 8x - "be spoiled" (DEU 28:29)
        'kinitsak': ('ki-nit-sak', 'REFL-defile-CAUS'),      # 8x - "defile oneself" (LEV 11:43)
        
        # Partial words fixed (patterns with ?)
        'vaikhak': ('vai-khak', 'go-command'),               # 26x - "counsel, devise"
        'kaikhawmin': ('ka-i-khawm-in', '1SG-go-gather-ERG'), # 20x - "gathered together"
        'kaikhia': ('ka-i-khia', '1SG-go-exit'),             # 17x - "I went out"
        'vaihawmna': ('vai-hawm-na', 'go-together-NMLZ'),    # 18x - "counsel, purpose"
        'keelno': ('keel-no', 'heel-young'),                 # 16x - "kids (goats)"
        'cithak': ('ci-thak', 'say-true'),                   # 16x - "said truly"
        'kuangdai': ('kuang-dai', 'trough-large'),           # 16x - "large trough"
        'taina': ('tai-na', 'stay-NMLZ'),                    # 16x - "dwelling"
        'ommawk': ('om-mawk', 'exist-empty'),                # 16x - "void, desolate"
        'paktatte': ('pak-tat-te', 'share-cut-PL'),          # 16x - "portions"
        'langpangte': ('lang-pang-te', 'side-board-PL'),     # 16x - "sides, ribs"
        'bawngla': ('bawng-la', 'cattle-young.female'),      # 15x - "heifer"
        'pakan': ('pa-kan', 'father-?'),                     # 15x - CHECK: needs context
        'paaikhia': ('paa-i-khia', 'father-?-exit'),         # 15x - CHECK: needs context
        'omkha': ('om-kha', 'exist-?'),                      # 15x - "living, present"
        'balnen': ('bal-nen', 'owe-swallow'),                # 15x - "devoured"
        'tuiciin': ('tui-ciin', 'water-pure'),               # 14x - "pure water"
        'naupaii': ('nau-paii', 'child-row'),                # 14x - "children in rows"
        'vanging': ('vang-ing', 'strength-INS'),             # 14x - "by strength"
        'galhiamte': ('gal-hiam-te', 'enemy-fierce-PL'),     # 14x - "fierce enemies"
        'ngaihsutsa': ('ngaihsut-sa', 'think-PAST'),         # 14x - "thought/imagined"
        'inndeite': ('inn-dei-te', 'house-good-PL'),         # 14x - "household"
        'sikkhau': ('sik-khau', 'repent-?'),                 # 14x - "repent"
        'palikte': ('pa-lik-te', 'father-?-PL'),             # 14x - compound
        'teembawte': ('teem-baw-te', 'tent-build-PL'),       # 13x - "tents"
        'siksanin': ('sik-san-in', 'repent-high-ERG'),       # 13x - "repenting"
        'genthuah': ('gen-thuah', 'speak-?'),                # 13x - "prophesy"
        'leengpei': ('leeng-pei', 'chariot-?'),              # 13x - "chariot wheel"
        'cikin': ('ci-kin', 'say-half'),                     # 13x - "saying"
        'laithei': ('lai-thei', 'middle-know'),              # 13x - "palm of hand"
        'siapa': ('sia-pa', 'old-father'),                   # 13x - "elder"
        'ak': ('a-k', '3SG-?'),                              # 13x - NOTE: partial
        'genkhit': ('gen-khit', 'speak-end'),                # 13x - "finished speaking"
        'deihzaw': ('deih-zaw', 'want-more'),                # 13x - "desire more"
        'uiphukte': ('ui-phuk-te', 'dog-wild-PL'),           # 12x - "wild dogs"
        'satnen': ('sat-nen', 'strike-swallow'),             # 12x - "smote, struck"
        'khausai': ('khua-sai', 'spirit-?'),                 # 12x - "spirit"
        'entel': ('en-tel', 'look-spread'),                  # 12x - "behold"
        'bawlsiate': ('bawl-sia-te', 'make-bad-PL'),         # 12x - "evildoers"
        
        # Possessive forms (ending in U+2019)
        'nihte\u2019': ('nih-te\u2019', 'two-PL.POSS'),      # 21x - "of the two"
        'ukte\u2019': ('uk-te\u2019', 'rule-PL.POSS'),       # 20x - "of the rulers"
        'mizawngte\u2019': ('mi-zawng-te\u2019', 'person-kind-PL.POSS'), # 17x
        'mipihte\u2019': ('mi-pih-te\u2019', 'person-with-PL.POSS'), # 15x
        'khuamite\u2019': ('khua-mi-te\u2019', 'town-person-PL.POSS'), # 15x
        'vengte\u2019': ('veng-te\u2019', 'guard-PL.POSS'),  # 14x
        'tampite\u2019': ('tampi-te\u2019', 'many-PL.POSS'), # 16x
        'suante\u2019': ('suan-te\u2019', 'lineage-PL.POSS'), # 14x
        'lawmte\u2019': ('lawm-te\u2019', 'friend-PL.POSS'), # 9x
        'makaite\u2019': ('makai-te\u2019', 'leader-PL.POSS'), # 8x
        
        # More possessive forms with straight apostrophe
        "nihte'": ('nih-te\u2019', 'two-PL.POSS'),           # alias
        "ukte'": ('uk-te\u2019', 'rule-PL.POSS'),            # alias
        "mizawngte'": ('mi-zawng-te\u2019', 'person-kind-PL.POSS'),
        "mipihte'": ('mi-pih-te\u2019', 'person-with-PL.POSS'),
        "khuamite'": ('khua-mi-te\u2019', 'town-person-PL.POSS'),
        "vengte'": ('veng-te\u2019', 'guard-PL.POSS'),
        "tampite'": ('tampi-te\u2019', 'many-PL.POSS'),
        "suante'": ('suan-te\u2019', 'lineage-PL.POSS'),
        "lawmte'": ('lawm-te\u2019', 'friend-PL.POSS'),
        "makaite'": ('makai-te\u2019', 'leader-PL.POSS'),
        
        # Single-word possessives (curly apostrophe U+2019)
        'tan\u2019': ('tan\u2019', 'toward.POSS'),                # 15x
        'ko\u2019': ('ko\u2019', 'call.POSS'),                    # 14x  
        'ei\u2019': ('ei\u2019', 'eat.POSS'),                     # 11x
        'lawn\u2019': ('lawn\u2019', 'bless.POSS'),               # 10x
        'komau\u2019': ('ko-mau\u2019', 'call-3PL.POSS'),         # 10x
        'husan\u2019': ('husan\u2019', 'choose.POSS'),            # 10x
        'gin\u2019': ('gin\u2019', 'gong.POSS'),                  # 9x
        'kisan\u2019': ('ki-san\u2019', 'REFL-high.POSS'),        # 9x
        'ven\u2019': ('ven\u2019', 'protect.POSS'),               # 12x
        'vengpa\u2019': ('veng-pa\u2019', 'guard-father.POSS'),   # 12x
        'kherub-te\u2019': ('kherub-te\u2019', 'cherub-PL.POSS'), # 12x
        'mangpa\u2019': ('mang-pa\u2019', 'chief-father.POSS'),   # 7x
        # Straight apostrophe aliases (for completeness)
        "tan'": ('tan\u2019', 'toward.POSS'),
        "ko'": ('ko\u2019', 'call.POSS'),
        "ei'": ('ei\u2019', 'eat.POSS'),
        "lawn'": ('lawn\u2019', 'bless.POSS'),
        "komau'": ('ko-mau\u2019', 'call-3PL.POSS'),
        "husan'": ('husan\u2019', 'choose.POSS'),
        "gin'": ('gin\u2019', 'gong.POSS'),
        "kisan'": ('ki-san\u2019', 'REFL-high.POSS'),
        "ven'": ('ven\u2019', 'protect.POSS'),
        "vengpa'": ('veng-pa\u2019', 'guard-father.POSS'),
        "kherub-te'": ('kherub-te\u2019', 'cherub-PL.POSS'),
        
        # More ki- verbs (fully unknown)
        'kilawite': ('ki-lawi-te', 'REFL-dislocate-PL'),     # derived
        'kisutin': ('ki-sut-in', 'REFL-spoil-ERG'),          # derived
        
        # Completely unknown words - philological analysis
        'tamlua': ('tam-lua', 'many-exceed'),                # 11x - "very many"
        'koilai': ('koi-lai', 'where-middle'),               # 9x - "where among"
        'tawmvei': ('tawm-vei', 'little-time'),              # 9x - "little while"
        'lapa': ('la-pa', 'song-father'),                    # 9x - "singer"
        'huzo': ('hu-zo', 'protect-COMPL'),                  # 9x - "protected"
        'bikbek': ('bik-bek', 'small~REDUP'),                # 8x - "very small"
        'bucip': ('bu-cip', 'bundle-pinch'),                 # 8x - "hyssop"
        'gimnam': ('gim-nam', 'suffer-taste'),               # 8x - "affliction"
        'meek': ('meek', 'look'),                            # 8x - "look" (variant of en?)
        'tem': ('tem', 'short'),                             # 8x - "short/low"
        'mangpha': ('mang-pha', 'chief-good'),               # 8x - "blessed"
        'buhlom': ('buh-lom', 'rice-heap'),                  # 8x - "heap of grain"
        'dawh': ('dawh', 'beautiful'),                       # 8x - "beautiful"
        'sulzuih': ('sul-zuih', 'track-follow'),             # 8x - "follow"
        'hel': ('hel', 'hell'),                              # 8x - "hell" (loanword)
        'galbawl': ('gal-bawl', 'enemy-make'),               # 8x - "make war"
        'golpi': ('gol-pi', 'round-big'),                    # 8x - "great bowl"
        'gilvah': ('gil-vah', 'belly-go'),                   # 8x - "with child"
        'daupai': ('dau-pai', 'war-pour'),                   # 8x - "battle"
        'ngong': ('ngong', 'stub'),                          # 8x - "stub"
        'kuankhiat': ('kuan-khiat', 'trough-depart'),        # 8x - compound
        'ngia': ('ngia', 'watch'),                           # 8x - "watch"
        'tuakkha': ('tuak-kha', 'meet-?'),                   # 8x - "happen"
        'pom': ('pom', 'embrace'),                           # 8x - "embrace"
        'dimdiam': ('dim~diam', 'still~REDUP'),              # 8x - "very still"
        'phuahtawm': ('phuah-tawm', 'compose-together'),     # 8x - "compose"
        'pholak': ('pho-lak', 'uncover-take'),               # 8x - "reveal"
        'pelmawh': ('pel-mawh', 'escape-?'),                 # 8x - "escape"
        'ngim': ('ngim', 'plan'),                            # 8x - "plan/devise"
        
        # === Session 5 Round 2: More partial word fixes ===
        'pakan': ('pakan', 'spoon'),                          # 15x - "spoon" (NUM 7:14)
        'paaikhia': ('paa-i-khia', 'go.and-CAUS-exit'),       # 15x - "drive out, put forth"
        'omkha': ('om-kha', 'exist-detained'),                # 15x - "be present/detained" (1SAM 21:7)
        'sikkhau': ('sik-khau', 'iron-chain'),                # 14x - "chain, fetter"
        'genthuah': ('gen-thuah', 'speak-add'),               # 13x - "add more (speaking)"
        'leengpei': ('leeng-pei', 'chariot-wheel'),           # 13x - "wheel"
        'hingkhawi': ('hing-khawi', 'live-let'),              # 11x - "suffer to live"
        'palikte': ('pa-lik-te', 'father-ancient-PL'),        # 14x - "ancestors"
        'vankhainate': ('van-khai-na-te', 'sky-?-NMLZ-PL'),   # 11x - "heavenly things"
        'khahkhong': ('khah-khong', 'choke-way'),             # 11x - "choke"
        'vakhuno': ('va-khu-no', 'go.and-spirit-young'),      # 11x - compound
        'thatsak': ('that-sak', 'kill-CAUS'),                 # 11x - "cause to kill"
        'lingkungte': ('ling-kung-te', 'hope-tree-PL'),       # 11x - compound
        'thuhaksa': ('thu-hak-sa', 'word-strong-PAST'),       # 11x - "word confirmed"
        'ginalote': ('gina-lo-te', 'believe-NEG-PL'),         # 11x - "unbelievers"
        'nusian': ('nu-sian', 'mother-holy'),                 # 11x - compound
        'paikawmin': ('pai-kawm-in', 'go-dwell-ERG'),         # 11x - "going to dwell"
        'lungnuamin': ('lung-nuam-in', 'heart-pleasant-ERG'), # 11x - "pleasantly"
        'khebaite': ('khebai-te', 'foreign-PL'),              # 11x - "foreigners"
        'neihtheih': ('neih-theih', 'have.II-able.II'),       # 11x - "be able to have"
        'biakinn-a': ('biak-inn-a', 'pray-house-LOC'),        # 15x - "in the temple"
        
        # More ki- verbs (philologically verified)
        'kiak': ('ki-ak', 'REFL-exalt'),                      # 8x - "be exalted" (JOB 24:24)
        'kitamzan': ('ki-tam-zan', 'REFL-many-break'),        # 8x - "broken, contrite" (PSA 51:17)
        'kisaktheih': ('ki-sak-theih', 'REFL-CAUS-able'),     # 8x - "boast, glorify self"
        'kithokiksak': ('ki-thok-ik-sak', 'REFL-rise-ITER-CAUS'), # 8x - "be raised/resurrected"
        'kiphel': ('ki-phel', 'REFL-clear'),                  # 7x - "clear oneself, justify"
        'hemkhia': ('hem-khia', 'remove-exit'),               # 7x - "put away, remove"
        'meengkhia': ('meeng-khia', 'branch-exit'),           # 7x - "branch out"
        
        # More remaining unknowns
        'dimtakin': ('dim-tak-in', 'still-true-ERG'),         # 8x - "very still/quietly"
        'dahhuai': ('dah-huai', 'put-dread'),                 # 8x - "terrible"
        'henhan': ('hen-han', 'be-?'),                        # 8x - compound
        'puksi': ('puk-si', 'cave-?'),                        # 8x - compound
        'phukham': ('phu-kham', 'carry-hold'),                # 7x - "bear/carry"
        'mak': ('mak', 'mark'),                               # 7x - "mark" (loanword?)
        'giah': ('giah', 'camp'),                             # 7x - "camp"
        'taikhiat': ('tai-khiat', 'flee-depart'),             # 7x - "flee away"
        'than': ('than', 'charcoal'),                         # 7x - "charcoal/coal"
        'leinuai-a': ('lei-nuai-a', 'earth-below-LOC'),       # 7x - "under the earth"
        'lahtel': ('lah-tel', 'take-spread'),                 # 7x - compound
        'kuumpi': ('kuum-pi', 'bow-big'),                     # 7x - "great bow"
        'kop': ('kop', 'edge'),                               # 7x - "edge/border"
        
        # Session 5 Round 3: More partial word fixes
        'khausai': ('khua-sai', 'spirit-voice'),              # 12x - "stringed instrument"
        'phelkhat': ('phel-khat', 'part-one'),                # 11x - "a portion, some part"
        'khensat': ('khen-sat', 'divide-appoint'),            # 11x - "appoint, ordain"
        'melhoihna': ('mel-hoih-na', 'face-good-NMLZ'),       # 11x - "beauty"
        'genzawh': ('gen-zawh', 'speak-breadth'),             # 11x - "largeness, breadth"
        'thudotna': ('thu-dot-na', 'word-ask-NMLZ'),          # 11x - "riddle, hard question"
        'biakinnsung': ('biak-inn-sung', 'pray-house-inside'), # 11x - "inside the temple"
        'satpa': ('sat-pa', 'build-father'),                  # 11x - "founder, builder"
        'lungdamkohna': ('lungdam-koh-na', 'rejoice-call-NMLZ'), # 11x - "thanksgiving"
        'veipi': ('vei-pi', 'faint-big'),                     # 11x - "very faint"
        'manphate': ('manpha-te', 'precious-PL'),             # 11x - "precious things"
        'masate': ('masa-te', 'first-PL'),                    # 11x - "first ones"
        'anne': ('a-nne', '3SG-food'),                        # 11x - "his/her food"
        'paang': ('pa-ang', 'father-side'),                   # 11x - compound
        'ki-em': ('ki-em', 'REFL-?'),                         # 11x - CHECK
        'vankhainate': ('van-khai-na-te', 'sky-open-NMLZ-PL'), # 11x - "heavenly things"
        'nasemnu\u2019': ('na-sem-nu\u2019', '2SG-serve-mother.POSS'), # 11x
        "nasemnu'": ('na-sem-nu\u2019', '2SG-serve-mother.POSS'),
        'ma-un': ('ma-un', 'that-time'),                      # 13x - "at that time"
        'ak': ('a-k', '3SG-?'),                               # 13x - NOTE: unclear
        '-a\u2019': ('-a\u2019', '3SG.POSS'),                  # 12x - possessive clitic
        "-a'": ('-a\u2019', '3SG.POSS'),                      # alias
        
        # Bug fixes: prevent over-decomposition of nam-, kai- etc.
        'namte': ('nam-te', 'tribe-PL'),                      # NOT na-m-te!
        'namza': ('nam-za', 'tribe-fear'),                    # NOT na-mza! = "nation"
        'kaina': ('kai-na', 'ascend-NMLZ'),                   # NOT ka-i-na! = "ascent"
        'minamte': ('mi-nam-te', 'person-tribe-PL'),          # "tribes/nations"
        'minamin': ('mi-nam-in', 'person-tribe-ERG'),         # "by nation"
        
        # Session 5 Round 4: More partial word fixes
        'hazatna': ('hazat-na', 'jealousy-NMLZ'),             # 10x - DEU 29:20
        'luangkhia': ('luang-khia', 'flow-exit'),             # 10x - "flow out"
        'thuthuk': ('thu-thuk', 'word-deep'),                 # 10x - "secret, deep thing"
        'sikkol': ('sik-kol', 'iron-bind'),                   # 10x - "stocks, fetter"
        'gutate': ('guta-te', 'destroyer-PL'),                # 10x - "destroyers"
        'gina': ('gina', 'virtuous'),                         # 9x - "virtuous"
        'cinten': ('cin-ten', 'say-fast'),                    # 9x - "abide fast"
        'sattan': ('sat-tan', 'cut-hang'),                    # 9x - "cut off, hang"
        'satpuk': ('sat-puk', 'strike-fall'),                 # 9x - "smite"
        'keekin': ('keel-kin', 'heel-half'),                  # 10x - compound
        'hanthotna': ('han-thot-na', 'follow-?-NMLZ'),        # 10x - compound
        'munkip': ('mun-kip', 'place-near'),                  # 10x - "nearby place"
        'lohnate': ('loh-na-te', 'able.NEG-NMLZ-PL'),         # 10x - "impossibilities"
        'maangmuhnate': ('maang-muh-na-te', 'vision-see.II-NMLZ-PL'), # 10x
        'naupangnote': ('nau-pang-no-te', 'child-side-young-PL'), # 10x
        'siahdongte': ('siah-dong-te', 'judge-until-PL'),     # 10x - compound
        'tawlette': ('tawle-tte', 'span-?-PL'),               # 9x - compound
        'kauphete': ('kau-phe-te', 'call-?-PL'),              # 9x - compound
        'patna': ('pa-t-na', 'father-?-NMLZ'),                # 9x - compound
        'cithuah': ('ci-thuah', 'say-add'),                   # 9x - "add more saying"
        'vai-in': ('vai-in', 'go.and-ERG'),                   # 9x - compound
        'luangte': ('luang-te', 'flow-PL'),                   # 9x - "flows"
        'innlam': ('inn-lam', 'house-side'),                  # 9x - "household side"
        'simthamin': ('sim-tham-in', 'count-molten-ERG'),     # 9x - compound
        'paizia': ('pai-zia', 'go-manner'),                   # 9x - "manner of going"
        
        # Session 5 Round 5: Ki- verbs from KJV
        'kitang': ('ki-tang', 'REFL-take'),                   # 7x - "take hold of one another"
        'kikeek': ('ki-keek', 'REFL-tear'),                   # 7x - "be rent/torn"
        'kilawh': ('ki-lawh', 'REFL-spread'),                 # 7x - "spread"
        'kikalh': ('ki-kalh', 'REFL-lock'),                   # 7x - "be locked"
        'kibehlap': ('ki-beh-lap', 'REFL-burden-add'),        # 7x - "be a burden"
        'kinusiacip': ('ki-nusia-cip', 'REFL-forsake-pinch'), # 7x - "be forsaken"
        'kihotkhiat': ('ki-hot-khiat', 'REFL-call-depart'),   # 7x - "be saved"
        'kithatlum': ('ki-that-lum', 'REFL-kill-lie'),        # 7x - "be slain"
        'kilamdang': ('ki-lam-dang', 'REFL-way-different'),   # 7x - "be different"
        'kithawhkiksak': ('ki-thawh-kik-sak', 'REFL-rise-ITER-CAUS'), # 7x - "be risen again"
        'kitun': ('ki-tun', 'REFL-arrive'),                   # 7x - "arrive together"
        'susiazo': ('susia-zo', 'destroy-COMPL'),             # 7x - "destroyed completely"
        'sunkim': ('sun-kim', 'burn-half'),                   # 7x - "burn completely"
        
        # Other unknowns
        'phe': ('phe', 'wing'),                               # 7x - "wing"
        'hah': ('hah', 'pant'),                               # 7x - "pant/gasp"
        'thahlup': ('thah-lup', 'kill-overturn'),             # 7x - "overthrow"
        'khikhe': ('khi-khe', 'foot-?'),                      # 7x - compound
        'lamdung': ('lam-dung', 'way-straight'),              # 7x - "straight way"
        'koimahah': ('koi-mah-ah', 'which-self-LOC'),         # 7x - "whichever place"
        'dawk': ('dawk', 'open'),                             # 7x - "open"
        'themno': ('them-no', 'one-young'),                   # 7x - "young one"
        'thangling': ('thang-ling', 'rise-expect'),           # 7x - "hope"
        'dau': ('dau', 'war'),                                # 7x - "war"
        'sungtumin': ('sung-tum-in', 'inside-all-ERG'),       # 7x - "inside all"
        'phalvak': ('phal-vak', 'permit-?'),                  # 7x - compound
        'guahpi': ('guah-pi', 'bowl-big'),                    # 7x - "great bowl"
        'manmanin': ('man-man-in', 'price~RED-ERG'),          # 7x - "pricing"
        'lawp': ('lawp', 'lap'),                              # 7x - "lap"
        'dip': ('dip', 'valley'),                             # 7x - "valley"
        'mahun': ('ma-hun', 'that-time'),                     # 7x - "at that time"
        'deda': ('de-da', 'love-?'),                          # 7x - compound
        'lokho': ('lo-kho', 'able.NEG-?'),                    # 7x - compound
        
        # Session 5 Round 6: High-frequency partial fixes
        'lamdangsa': ('lamdang-sa', 'different-INTNS'),       # 54x - "be astonished"
        'lamdangsa-in': ('lamdang-sa-in', 'different-INTNS-ERG'), # 22x
        'tangvalte': ('tangval-te', 'young.man-PL'),          # 48x - "young men, lads"
        'tangval': ('tangval', 'young.man'),                  # base form
        'tanglai': ('tang-lai', 'generation-middle'),         # 28x - "of old, ancient"
        'bawltawm': ('bawl-tawm', 'make-break'),              # 11x - "break forth"
        'hatsak': ('hat-sak', 'strong-CAUS'),                 # 11x - "strengthen"
        'deihsak': ('deih-sak', 'want-CAUS'),                 # 11x - "desire for"
        'ngaihsunsun': ('ngaihsun-sun', 'think-deep'),        # 11x - "meditate"
        'pilvang': ('pil-vang', 'learn-wise'),                # 11x - "be wise/cunning"
        'nisa': ('ni-sa', 'day-hot'),                         # 11x - "summer"
        'tungman': ('tung-man', 'arrive-clay'),               # 11x - "clay" (potter's)
        'paipel': ('pai-pel', 'go-vessel'),                   # 11x - "vessel, basket"
        'piathei': ('pia-thei', 'give-able'),                 # 11x - "able to give"
        'tangthu': ('tang-thu', 'generation-word'),           # 10x - "old word, tradition"
        'khualna-in': ('khual-na-in', 'sojourn-NMLZ-ERG'),    # 10x - "sojourning"
        'hanthotna': ('han-thot-na', 'follow-tie-NMLZ'),      # 10x - compound
        'gamlum': ('gam-lum', 'land-round'),                  # 9x - "whole land"
        'saiha': ('sai-ha', 'flesh-tooth'),                   # 9x - "ivory"
        'zangsak': ('zang-sak', 'use-CAUS'),                  # 9x - "cause to use"
        'liailiai': ('liai~liai', 'go.around~RED'),           # 9x - "go around repeatedly"
        
        # More high-frequency fixes
        'ak': ('ak', 'then/particle'),                        # 13x - discourse particle
        'ki-em': ('ki-em', 'REFL-?'),                         # 11x - CHECK: needs context
        'pukna': ('puk-na', 'cave-NMLZ'),                     # 11x - "cave dwelling"
        'khawk': ('khawk', 'hollow/empty'),                   # 11x - "hollow"
        'pahtakna': ('pah-tak-na', 'trust-true-NMLZ'),        # 11x - "trust"
        'midikte\u2019': ('mi-dik-te\u2019', 'person-righteous-PL.POSS'), # 11x
        "midikte'": ('mi-dik-te\u2019', 'person-righteous-PL.POSS'),
        'beelseek': ('beel-seek', 'pan-form'),                # 11x - "potter"
        'keutum': ('keu-tum', 'dig-all'),                     # 11x - "dig completely"
        'kangtumsak': ('kang-tum-sak', 'brass-all-CAUS'),     # 11x - compound
        'khen\u2019': ('khen\u2019', 'divide.POSS'),          # 10x
        "khen'": ('khen\u2019', 'divide.POSS'),
        'nate\u2019': ('na-te\u2019', '2SG-PL.POSS'),         # 10x - "your (pl)"
        "nate'": ('na-te\u2019', '2SG-PL.POSS'),
        'nite': ('ni-te', 'day-PL'),                          # compound
        'mawhneite': ('mawh-nei-te', 'sin-have-PL'),          # 10x - "sinners"
        'tawlette': ('tawle-tte', 'span-?-PL'),               # 9x - compound
        'kauphete': ('kau-phe-te', 'call-?-PL'),              # 9x - compound
        'siampipuan\u2019': ('siampi-puan\u2019', 'priest-cloth.POSS'), # 9x
        "siampipuan'": ('siampi-puan\u2019', 'priest-cloth.POSS'),
        'ukpa\u2019': ('uk-pa\u2019', 'rule-father.POSS'),    # 9x
        "ukpa'": ('uk-pa\u2019', 'rule-father.POSS'),
        'patna': ('pat-na', 'trust-NMLZ'),                    # 9x - "trust, faith"
        'cina-in': ('ci-na-in', 'say-NMLZ-ERG'),              # 9x - "saying"
        'ziate': ('zi-a-te', 'wife-3SG-PL'),                  # 9x - "his wives"
        
        # Session 6 Round 1: Philologically verified (97.31%)
        'ki-em': ('ki-em', 'PASS-bake'),                       # 11x - "be baked" (Lev)
        'tawlette': ('tawle-te', 'window-PL'),                 # 9x - "windows"
        'kikholhpihte': ('ki-kholh-pih-te', 'REFL-accompany-CAUS-PL'),  # 9x - "companions"
        'paihkhiatsak': ('paih-khiat-sak', 'go-depart-APPL'),  # 9x - "take away"
        'mialsak': ('mial-sak', 'darkness-CAUS'),              # 9x - "darken, cover"
        'ento': ('en-to', 'look-toward'),                      # 9x - "look up at"
        'lingkung': ('ling-kung', 'thorn-round'),              # 9x - "thorns, briers"
        'sikkawi': ('sik-kawi', 'hook-fish'),                  # 9x - "fishhook"
        'piakkhong': ('piak-khong', 'give-NOM'),               # 9x - "gift"
        'ngahzawh': ('ngah-zawh', 'get-COMPL'),                # 9x - "obtain, get fully"
        'upadi': ('upa-di', 'elder-?'),                        # 9x - compound
        'awksak': ('awk-sak', 'for-CAUS'),                     # 9x - "cause for" 
        'thumante': ('thu-man-te', 'word-true-PL'),            # 9x - "true words"
        'kampi': ('kam-pi', 'word-big'),                       # 9x - "great word"
        'ngente': ('ngen-te', 'pray-PL'),                      # 9x - compound
        'ututin': ('u-tu-tin', 'want-FUT-PROG'),               # 9x - "wanting, willing"
        'nuntakna-ah': ('nun-tak-na-ah', 'life-true-NMLZ-LOC'), # 9x - "in life"
        'zattheih': ('zat-theih', 'hear-can'),                 # 9x - "can hear"
        'ukzawh': ('uk-zawh', 'rule-COMPL'),                   # 9x - "rule completely"
        'omngei': ('om-ngei', 'be-know'),                      # 9x - "be known"
        'baihzaw': ('baih-zaw', 'owe-more'),                   # 9x - "owe more"
        'lungdamhuai': ('lung-dam-huai', 'heart-heal-fear'),   # 9x - "rejoice greatly"
        'kineihkhemte': ('ki-neih-khem-te', 'REFL-have-all-PL'), # 9x - "possessions"
        'septheih': ('sep-theih', 'work-can'),                 # 9x - "can work"
        'pupite': ('pupi-te', 'grandparent-PL'),               # 9x - "grandparents/ancestors"
        'neuzaw': ('neu-zaw', 'young-more'),                   # 8x - "younger"
        'khentat': ('khen-tat', 'divide-cut'),                 # 8x - "divide, cut off"
        'zinei': ('zi-nei', 'wife-have'),                      # 9x - "have a wife, marry"
        
        # Session 6 Round 2: More philological additions
        'kauphete': ('kauphe-te', 'locust-PL'),                # 9x - "locusts"
        'upadi': ('upa-di', 'elder-manner'),                   # 9x - "law, custom, manner"
        'naungekte': ('naungek-te', 'infant-PL'),              # 9x - "infants, sucklings"  
        'khualzinin': ('khual-zin-in', 'sojourn-road-ERG'),    # 8x - "journeying"
        'ciahsakkik': ('ciah-sak-kik', 'return-CAUS-ITER'),    # 8x - "send back"
        'suh': ('suh', 'well'),                                # 8x - "well" (water source)
        'hawmguakin': ('hawm-guak-in', 'empty-ADV'),           # 8x - "empty, empty-handed"
        'suksak': ('suk-sak', 'become-CAUS'),                  # 8x - "make become"
        'milipun': ('mi-li-pun', 'person-?-bundle'),           # 8x - "bundle"
        'tuisuak': ('tui-suak', 'water-become'),               # 8x - "melt"
        'teelkhia': ('teel-khia', 'choose-emerge'),            # 8x - "choose out, select"
        'khuttum': ('khut-tum', 'hand-bunch'),                 # 8x - "fist"
        'thutakna': ('thu-tak-na', 'word-true-NMLZ'),          # 8x - "faithfulness"
        'lutangin': ('lut-ang-in', 'enter-together-ERG'),      # 8x - "entering together"
        'teelkhiain': ('teel-khia-in', 'choose-emerge-ERG'),   # 8x - "choosing out"
        'khamkhop': ('kham-khop', 'forbid-together'),          # 8x - compound
        'sawlpang': ('sawl-pang', 'send-carry'),               # 8x - "messenger"
        'giahna': ('giah-na', 'camp-NMLZ'),                    # 8x - "camping, encampment"
        'minthangin': ('min-thang-in', 'name-famous-ERG'),     # 8x - "in blessing"
        'netniamna': ('net-niam-na', 'hunger-lowly-NMLZ'),     # 8x - "fasting"
        'kisilna': ('ki-sil-na', 'REFL-wash-NMLZ'),            # 8x - "purification"
        'hontat': ('hon-tat', 'flock-cut'),                    # 8x - "separate flock"
        'kisiansuahna': ('ki-sian-suah-na', 'REFL-holy-issue-NMLZ'), # 8x - "sanctification"
        'miphak': ('mi-phak', 'person-half'),                  # 8x - compound
        'samul': ('sa-mul', 'animal-hair'),                    # 8x - "animal hair"
        'kikoihna': ('ki-koih-na', 'REFL-place-NMLZ'),         # 8x - compound
        'khakcip': ('khak-cip', 'descendant-small'),           # 8x - compound
        'paipai': ('pai-pai', 'go~REDUP'),                     # 8x - "go repeatedly"
        'innlak': ('inn-lak', 'house-middle'),                 # 8x - "among the house"
        
        # Session 6 Round 3: More philological additions
        'meiite': ('mei-ite', 'cloud-PL'),                     # 8x - "clouds"
        'sutgawp': ('sut-gawp', 'spoil-round'),                # 8x - "spoil"
        'koihcing': ('koih-cing', 'put-prepare'),              # 8x - "store up"
        'hihzo': ('hih-zo', 'do-can'),                         # 8x - "be able to do"
        'paulap': ('pau-lap', 'speak-fold'),                   # 8x - "occasion, matter"
        'kumkumin': ('kum-kum-in', 'year~REDUP-ERG'),          # 8x - "yearly"
        'galvilte': ('gal-vil-te', 'war-watch-PL'),            # 8x - "watchmen"
        'suahtaksak': ('suah-tak-sak', 'issue-true-CAUS'),     # 8x - "redeem"
        'tuakkha': ('tuak-kha', 'meet-?'),                     # 8x - compound
        'kingakna': ('ki-ngak-na', 'REFL-wait-NMLZ'),          # 8x - "base, stand"
        'pangsak': ('pang-sak', 'plead-CAUS'),                 # 8x - "cause to plead"
        'kamah': ('ka-mah', '1SG-self'),                       # 8x - "myself"
        'kawmun': ('ka-om-un', '1SG-be-PL.INCL'),              # 8x - compound
        'sangsak': ('sang-sak', 'high-CAUS'),                  # 8x - "make high, exalt"
        'puteekte': ('puteek-te', 'ancestors-PL'),             # 8x - "ancestors"
        'paikawmun': ('pai-ka-om-un', 'go-1SG-be-PL.INCL'),    # 8x - compound
        'kongcing': ('kong-cing', '1SG→3-prepare'),            # 8x - compound
        'tangtungsak': ('tang-tung-sak', 'reach-top-CAUS'),    # 8x - "make arrive"
        'omcip': ('om-cip', 'be-close'),                       # 8x - "be close"
        'deihnate': ('deih-na-te', 'want-NMLZ-PL'),            # 8x - "desires"
        
        # Session 6 Round 4: More philological additions  
        'gamtatzia': ('gam-tat-zia', 'land-cut-way'),          # 8x - "way, manner"
        'thudot': ('thu-dot', 'word-ask'),                     # 8x - "enquire"
        'lawpna': ('lawp-na', 'rejoice-NMLZ'),                 # 8x - "rejoicing"
        'kiniamkhiatte': ('ki-niam-khiat-te', 'REFL-lowly-depart-PL'), # 8x - "the meek"
        'suaktazo': ('suak-ta-zo', 'become-true-can'),         # 8x - "escape, deliver"
        'ngaklah': ('ngak-lah', 'wait-take'),                  # 8x - "watch for"
        'neihzah': ('neih-zah', 'have.II-much'),               # 8x - "have much"
        'liammate': ('liam-ma-te', 'wound-?-PL'),              # 8x - "wounds, bruises"
        'siamnate': ('siam-na-te', 'skilled-NMLZ-PL'),         # 8x - "skillful works"
        'santheih': ('san-theih', 'salt-can'),                 # 8x - "salted" (Mark 9:49)
        'lutpih': ('lut-pih', 'enter-CAUS'),                   # 8x - "bring in"
        'pahtawi-in': ('pa-htawi-in', 'male-old.man-ERG'),     # 8x - "patriarch" (from htawi elder)
        'cimawhte\u2019': ('ci-mawh-te\u2019', 'say-sin-PL.POSS'), # 8x 
        "cimawhte'": ('ci-mawh-te\u2019', 'say-sin-PL.POSS'),
        'pannate': ('panna-te', 'petition-PL'),                # 8x - "petitions"
        'gennate': ('gen-na-te', 'speak-NMLZ-PL'),             # 8x - "sayings"
        'vawhpa': ('vawh-pa', 'go.and-male'),                  # 8x - compound
        'kongpite-ah': ('kong-pi-te-ah', '1SG→3-big-PL-LOC'),  # 8x - compound
        'puksi': ('puk-si', 'cave-?'),                         # 8x - "cave" (compound noun)
        
        # Session 6 Round 5: More philological additions (freq 7)
        'vakvai': ('vak-vai', 'walk-wander'),                  # 7x - "fugitive, wanderer"
        'tuikhukte': ('tui-khuk-te', 'water-hollow-PL'),       # 7x - "wells"
        'sangto': ('sang-to', 'high-toward'),                  # 7x - "lift up"
        'phakna': ('phak-na', 'reach-NMLZ'),                   # 7x - "meaning, significance"
        'mundang': ('mun-dang', 'place-other'),                # 7x - "another place"
        'tengkhia': ('teng-khia', 'dwell-emerge'),             # 7x - "set up, appoint"
        'gilkialte': ('gil-kial-te', 'stomach-turn-PL'),       # 7x - "honest men"
        'penna': ('pen-na', 'best-NMLZ'),                      # 7x - "the best"
        'leina': ('lei-na', 'buy-NMLZ'),                       # 7x - "buying, purchase"
        'thupalsatna': ('thu-pal-sat-na', 'word-cross-cut-NMLZ'), # 7x - "trespass"
        'vutte': ('vut-te', 'ash-PL'),                         # 7x - "ashes"
        'deihgawh': ('deih-gawh', 'want-covet'),               # 7x - "covet"
        'khialkha': ('khial-kha', 'err-go'),                   # 7x - "go astray"
        'eng': ('eng', 'what'),                                # 7x - "what" (interrogative)
        'kihona': ('ki-ho-na', 'REFL-call-NMLZ'),              # 7x - "calling"
        'cilesa': ('ci-le-sa', 'say-and-?'),                   # 7x - compound
        'anhuan': ('an-huan', '3PL-prepare'),                  # 7x - "they prepare"
        'ihmu-in': ('i-mu-in', '1PL.INCL-see-ERG'),            # 7x - compound
        'khawmsak': ('khawm-sak', 'gather-CAUS'),              # 7x - "cause to gather"
        'ton': ('ton', 'arrive'),                              # 7x - "arrive, reach"
        'neel': ('ne-el', 'eat-NFIN'),                         # 7x - "eating"
        'sialin': ('si-al-in', 'die-NFIN'),                    # 7x - "dying"
        'kaisak': ('kai-sak', 'hang-CAUS'),                    # 7x - "hang up"
        'unu': ('u-nu', 'elder.sibling-mother'),               # 7x - "aunt"
        'naubu': ('na-u-bu', '2SG-elder.sibling-father'),      # 7x - "your uncle"
        'sanggamnu\u2019': ('sanggam-nu\u2019', 'sibling-mother.POSS'), # 7x - "sister's"
        "sanggamnu'": ('sanggam-nu\u2019', 'sibling-mother.POSS'),
        'hithiatin': ('hi-thiat-in', 'be-cease-ERG'),          # 7x - "thus being"
        'cingnu': ('cing-nu', 'prepare-mother'),               # 7x - compound
        
        # Session 6 Round 6: More philological additions (freq 6)
        'kidawk': ('ki-dawk', 'REFL-dry'),                     # 6x - "become dry, dry land"
        'singgahte': ('sing-gah-te', 'tree-fruit-PL'),         # 6x - "fruit trees"
        'manthan': ('man-than', 'true-exist'),                 # 6x - "keep alive, preserve"
        'gancingte': ('gan-cing-te', 'cattle-care-PL'),        # 6x - "herdsmen"
        'phelnih': ('phel-nih', 'part-two'),                   # 6x - "in half, two pieces"
        'siampa': ('siam-pa', 'skilled-male'),                 # 6x - "craftsman"
        'tawhna': ('tawh-na', 'meet-NMLZ'),                    # 6x - "meeting, battle"
        'cimtak': ('cim-tak', 'be.weary-true'),                # 6x - "weary, loathe"
        'ciangkang': ('ciang-kang', 'clear-stripe'),           # 6x - "striped, peeled"
        'kihing': ('ki-hing', 'REFL-live'),                    # 6x - "be preserved"
        'hawkkhiatsak': ('hawk-khiat-sak', 'take.off-depart-CAUS'), # 6x - "strip off"
        'thongkiate': ('thong-kia-te', 'prison-?-PL'),         # 6x - "prisoners"
        'kivuina': ('ki-vui-na', 'REFL-bury-NMLZ'),            # 6x - "burying place"
        'neite\u2019': ('nei-te\u2019', 'have-PL.POSS'),       # 6x
        "neite'": ('nei-te\u2019', 'have-PL.POSS'),
        'tumte': ('tum-te', 'will-PL'),                        # 6x - compound
        'pualama': ('pualam-a', 'outside-LOC'),                # 6x - "outside"
        'omnasa': ('om-na-sa', 'be-NMLZ-animal'),              # 6x - compound
        'hut': ('hut', 'shelter'),                             # 6x - "shelter, booth"
        'bangci-a': ('bang-ci-a', 'what-say-Q'),               # 6x - "what manner"
        'kapkhia': ('ka-pkhia', '1SG-emerge'),                 # 6x - compound
        'zawl-ai': ('zawl-ai', 'valley-LOC'),                  # 6x - "in the valley"
        'thalawhsa': ('tha-lawh-sa', 'breath-reap-animal'),    # 6x - compound
        'zawte': ('zawh-te', 'finish-PL'),                     # 6x - "those who finished"
        'huk': ('huk', 'bark'),                                # 6x - "bark" (of tree)
        'samsakin': ('sam-sak-in', 'call-CAUS-ERG'),           # 6x - "causing to call"
        'damdamin': ('dam-dam-in', 'well~REDUP-ERG'),          # 6x - "well, safely"
        'kawngah': ('kawng-ah', 'road-LOC'),                   # 6x - "on the road"
        'piapi': ('pia-pi', 'give-big'),                       # 6x - "give greatly"
        'ginat': ('gi-nat', 'stomach-tight'),                  # 6x - "courageous"
        'paipihsak': ('pai-pih-sak', 'go-CAUS-APPL'),          # 6x - "cause to accompany"
        
        # Session 6 Round 7: More philological additions (freq 8)
        'hutna': ('hut-na', 'shelter-NMLZ'),                   # 8x - "shelter, refuge"
        'puang': ('puang', 'speckled'),                        # 8x - "speckled, spotted"
        'zawt': ('zawh-t', 'finish-?'),                        # 8x - "stronger" (contextual)
        'letsongin': ('let-song-in', 'return-send-ERG'),       # 8x - "as a present"
        'hoihlamin': ('hoih-lam-in', 'good-manner-ERG'),       # 8x - "peacefully"
        'kinuh': ('ki-nuh', 'REFL-anoint'),                    # 8x - "be anointed"
        'zuikha': ('zui-kha', 'follow-?'),                     # 8x - "follow, remember"
        'hingte\u2019': ('hing-te\u2019', 'live-PL.POSS'),     # 8x - "living creatures'"
        "hingte'": ('hing-te\u2019', 'live-PL.POSS'),
        'luangsuk': ('luang-suk', 'flow-grind'),               # 8x - "grind fine"
        'singniim': ('sing-niim', 'tree-shade'),               # 8x - "grove"
        'genpih': ('gen-pih', 'speak-APPL'),                   # 8x - "speak unto"
        'buksim': ('buk-sim', 'ambush-?'),                     # 8x - "lie in wait"
        'dona': ('do-na', 'fight-NMLZ'),                       # 8x - "war, fighting"
        'damkikzo': ('dam-kik-zo', 'well-ITER-can'),           # 8x - "recover"
        'singluang': ('sing-luang', 'tree-log'),               # 8x - "beam"
        'kiciamtehna': ('ki-ciam-teh-na', 'REFL-oath-mark-NMLZ'), # 8x - "enrollment"
        'innluahza': ('inn-luah-za', 'house-?-?'),             # 8x - compound
        'milipun': ('mi-lipun', 'person-bundle'),              # 8x - "bundle"
        'atna': ('at-na', 'cut-NMLZ'),                         # 8x - "cutting"
        'kongpuankhai': ('kong-puan-khai', '1SG→3-cloth-?'),   # 8x - compound
        'khetphimte': ('khet-phim-te', 'judge-try-PL'),        # 8x - "trials"
        'zepna': ('zep-na', 'press-NMLZ'),                     # 8x - "oppression"
        'tuibuah': ('tui-buah', 'water-?'),                    # 8x - compound
        'lungduai-in': ('lung-duai-in', 'heart-doubt-ERG'),    # 8x - "doubting"
        'koihsa': ('koih-sa', 'put-already'),                  # 8x - "already placed"
        'khangkhangin': ('khang-khang-in', 'generation~REDUP-ERG'), # 8x - "from generation"
        'kantel': ('kan-tel', '1SG→3-spread'),                 # 8x - compound
        'liangko-ah': ('liang-ko-ah', 'shoulder-both-LOC'),    # 8x - on both shoulders
        'pataukohna': ('pa-tau-koh-na', 'male-?-call-NMLZ'),   # 8x - compound
        'puanmongteep': ('puan-mong-teep', 'cloth-cover-?'),   # 8x - "covering"
        'hinglai': ('hing-lai', 'live-time'),                  # 8x - "lifetime"
        'sausak': ('sau-sak', 'long-CAUS'),                    # 8x - "lengthen"
        'vuite': ('vui-te', 'bury-PL'),                        # 8x - compound
        'luahte': ('luah-te', 'flow-PL'),                      # 8x - compound
        'puanza': ('puan-za', 'cloth-?'),                      # 8x - compound
        'nungakna': ('nungak-na', 'maiden-NMLZ'),              # 8x - "virginity"
        'hihnate': ('hih-na-te', 'do-NMLZ-PL'),                # 8x - "doings"
        'lunghimawhin': ('lung-himawh-in', 'heart-doubt-ERG'), # 8x - "anxiously"
        'bawh': ('bawh', 'rub'),                               # 8x - "rub"
        'kicihna': ('ki-cih-na', 'REFL-say-NMLZ'),             # 8x - "being called"
        'sawmsagihte': ('sawm-sagih-te', 'ten-seven-PL'),      # 8x - "seventies"
        'nun\u2019': ('nun\u2019', 'life.POSS'),               # 8x - "life's"
        "nun'": ('nun\u2019', 'life.POSS'),
        'sala': ('sa-la', 'animal-?'),                         # 8x - compound
        'inntualah': ('inn-tu-a-lah', 'house-?-LOC-?'),        # 8x - compound
        'muanhuai-in': ('muan-huai-in', 'trust-fear-ERG'),     # 8x - "trustingly"
        'kihuh': ('ki-huh', 'REFL-push'),                      # 8x - compound
        'thongkiatna': ('thong-kiat-na', 'prison-release-NMLZ'), # 8x - "release from prison"
        
        # Session 6 Round 8: More philological additions (freq 8)
        'innluahza': ('inn-luah-za', 'house-inherit-right'),   # 8x - "birthright"
        'tuibuah': ('tui-buah', 'water-pour'),                 # 8x - "drink offering"
        'hehluatna': ('heh-luat-na', 'anger-exceed-NMLZ'),     # 8x - "fierceness"
        'pelmawh': ('pel-mawh', 'praise-?'),                   # 8x - compound
        'singhiang': ('sing-hiang', 'tree-branch'),            # 8x - "branches"
        'tuihual': ('tui-hual', 'water-wave'),                 # 8x - "waves, unstable"
        'nono': ('no-no', 'small~REDUP'),                      # 8x - "small, village"
        'paupau': ('pau-pau', 'speak~REDUP'),                  # 8x - "speak repeatedly"
        'lingsak': ('ling-sak', 'move-CAUS'),                  # 8x - "remove, shake"
        'keugaw': ('keu-gaw', 'dig-round'),                    # 8x - "overturn"
        'limlang': ('lim-lang', 'image-reflect'),              # 8x - "mirror"
        'genteh': ('gen-teh', 'speak-mark'),                   # 8x - "byword, proverb"
        'mimawhte': ('mi-mawh-te', 'person-sin-PL'),           # 8x - "sinners"
        'omsakkik': ('om-sak-kik', 'be-CAUS-ITER'),            # 8x - "restore"
        'theihpih': ('theih-pih', 'know.II-APPL'),             # 8x - "know together"
        'sutsak': ('sut-sak', 'spoil-CAUS'),                   # 8x - "cause to spoil"
        'liveina': ('li-vei-na', 'four-time-NMLZ'),            # 8x - "fourth"
        'ciangpi': ('ciang-pi', 'measure-big'),                # 8x - "ephah"
        'dampah': ('dam-pah', 'well-?'),                       # 8x - "willingly"
        'vokte': ('vok-te', 'pig-PL'),                         # 8x - "swine"
        'zuikha': ('zui-kha', 'follow-go'),                    # 8x - "follow"
        'buksim': ('buk-sim', 'ambush-surround'),              # 8x - "lie in wait"
        'tuakkha': ('tuak-kha', 'meet-go'),                    # 8x - "meet"
        'ututun': ('u-tu-tun', 'want-FUT-DUR'),                # 8x - "wanting"
        'cingtakin': ('cing-tak-in', 'prepare-true-ERG'),      # 8x - "truly"
        'sapi': ('sa-pi', 'animal-big'),                       # 8x - "ox, cattle"
        'neihsateng': ('neih-sa-teng', 'have.II-already-dwell'), # 8x - compound
        'khihna': ('khih-na', 'frighten-NMLZ'),                # 8x - "fear"
        'khutlekhezaw': ('khut-le-khe-zaw', 'hand-and-foot-more'), # 8x - "hands and feet"
        'piancil': ('pian-cil', 'born-alone'),                 # 8x - "firstborn"
        'vun-atna': ('vun-at-na', 'skin-cut-NMLZ'),            # 8x - "circumcision"
        
        # Session 6 Round 9: More philological additions (freq 7-8)
        'pataukohna': ('pa-tau-koh-na', 'male-?-call-NMLZ'),   # 8x - "alarm, trumpet"
        'puanmongteep': ('puan-mong-teep', 'cloth-cover-fringe'), # 8x - "fringes"
        'tuutalte': ('tuutal-te', 'ram-PL'),                   # 8x - "rams"
        'puanza': ('puan-za', 'cloth-garment'),                # 8x - "vesture, garment"
        'henhan': ('hen-han', 'be-?'),                         # 8x - "spreading"
        'liammate': ('liam-ma-te', 'wound-?-PL'),              # 8x - "wounds, bruises"
        'awi-in': ('a-wi-in', '3SG-tie-ERG'),                  # 8x - compound
        'cilesa': ('ci-le-sa', 'say-and-already'),             # 7x - "saying and"
        'toh': ('toh', 'stand'),                               # 7x - "stand"
        'sapfaia': ('sapfaia', 'sapphire'),                    # 7x - "sapphire" (loanword)
        'panga': ('pang-a', 'side-LOC'),                       # 7x - "on the side"
        'liangkaih': ('liang-kaih', 'shoulder-join'),          # 7x - "shoulder piece"
        'langnih': ('lang-nih', 'side-two'),                   # 7x - "both sides"
        'siangthopen': ('siangtho-pen', 'holy-SUPL'),          # 7x - "most holy"
        'sintuamte': ('sin-tuam-te', 'liver-lobe-PL'),         # 7x - "liver lobes"
        'balgawp': ('bal-gawp', 'torn-round'),                 # 7x - "torn by beasts"
        'upmawh': ('up-mawh', 'suspect-sin'),                  # 7x - "jealousy"
        'upmawhna': ('up-mawh-na', 'suspect-sin-NMLZ'),        # 7x - "jealousy"
        'tatsat': ('tat-sat', 'cut-regular'),                  # 7x - "continual"
        'hawlkhiatsak': ('hawl-khiat-sak', 'drive-depart-CAUS'), # 7x - "drive out"
        'luzang': ('lu-zang', 'head-crown'),                   # 7x - "crown of head"
        'gilkialna': ('gil-kial-na', 'stomach-turn-NMLZ'),     # 7x - "hunger"
        'thun': ('thun', 'entreat'),                           # 7x - "pray, entreat"
        'minthangsak': ('min-thang-sak', 'name-famous-CAUS'),  # 7x - "glorify"
        'gelhsak': ('gelh-sak', 'write-CAUS'),                 # 7x - "describe, write"
        'omdan': ('om-dan', 'be-manner'),                      # 7x - "condition, welfare"
        'pawi-ah': ('pawi-ah', 'feast-LOC'),                   # 7x - "at feast"
        'mualzang': ('mual-zang', 'mountain-crown'),           # 7x - "mountain top"
        'anteh': ('an-teh', '3PL-mark'),                       # 7x - compound
        'khawhsa': ('khawh-sa', 'harvest-animal'),             # 7x - compound
        'tecite': ('teci-te', 'witness-PL'),                   # 7x - "witnesses"
        'cilphih': ('cil-pih', 'alone-APPL'),                  # 7x - compound
        'kiphawkna': ('ki-phawk-na', 'REFL-remember-NMLZ'),    # 7x - "memorial"
        'kituh': ('ki-tuh', 'REFL-push'),                      # 7x - compound
        'thukkikna': ('thuk-kik-na', 'deep-ITER-NMLZ'),        # 7x - compound
        'mante': ('man-te', 'true-PL'),                        # 7x - compound
        'khikhe': ('khi-khe', 'foot-leg'),                     # 7x - "legs, feet"
        'tunglam': ('tung-lam', 'above-direction'),            # 7x - "upward"
        'tangtakin': ('tang-tak-in', 'reach-true-ERG'),        # 7x - "certainly"
        'niam': ('niam', 'lowly'),                             # 7x - "low, humble"
        'theikha': ('theih-kha', 'know.II-go'),                # 7x - compound
        'ulianpa\u2019': ('ulian-pa\u2019', 'chief-male.POSS'), # 7x
        "ulianpa'": ('ulian-pa\u2019', 'chief-male.POSS'),
        'khinkhia': ('khin-khia', 'move-emerge'),              # 7x - "remove"
        'munmuanhuai-ah': ('mun-muanhuai-ah', 'place-trust-LOC'), # 7x - "at refuge"
        'khansih': ('khan-sih', 'generation-finish'),          # 7x - compound
        'naunu': ('na-u-nu', '2SG-elder.sibling-mother'),      # 7x - "your aunt"
        'thakhauh': ('tha-khauh', 'strength-strong'),          # 7x - "mighty"
        'theihzawh': ('theih-zawh', 'know.II-COMPL'),          # 7x - "know completely"
        'kongzingah': ('kong-zing-ah', '1SG→3-wife-LOC'),      # 7x - compound
        'samzang': ('sam-zang', 'call-?'),                     # 7x - compound
        'innkuansung': ('inn-kuan-sung', 'house-family-inside'), # 7x - "household"
        'satlum': ('sat-lum', 'cut-round'),                    # 7x - "kill, slay"
        'minsiasak': ('min-sia-sak', 'name-bad-CAUS'),         # 7x - "blaspheme"
        
        # Session 6 Round 10: More philological additions (freq 7-8)
        'zawt': ('zawh-t', 'strong-?'),                        # 8x - "stronger" (form of zawh)
        'inntualah': ('inn-tu-a-lah', 'house-stand-LOC-take'), # 8x - "platform"
        'sala': ('sa-la', 'flesh-take'),                       # 8x - "slave"
        'napi-un': ('napi-un', 'but-PL.IMP'),                  # 8x - but (imperative plural)
        'puksi': ('puk-si', 'cave-die'),                       # 8x - compound
        'pakante': ('pak-an-te', 'spoon-3PL-PL'),              # 7x - "spoons"
        'gaknate': ('gak-na-te', 'hook-NMLZ-PL'),              # 7x - "hooks"
        'thumna-ah': ('thum-na-ah', 'three-NMLZ-LOC'),         # 7x - "on the third"
        'takah': ('tak-ah', 'true-LOC'),                       # 7x - "through/truly"
        'pano': ('pa-no', 'male-young'),                       # 7x - "young male/calf"
        'maingatin': ('mai-ngat-in', 'face-ground-ERG'),       # 7x - "face down"
        'banna': ('ban-na', 'spread-NMLZ'),                    # 7x - "spreading (plague)"
        'lawnna': ('lawn-na', 'flow-NMLZ'),                    # 7x - "issue, discharge"
        'simto': ('sim-to', 'count-toward'),                   # 7x - "count unto"
        'zuakna': ('zuak-na', 'sell-NMLZ'),                    # 7x - "sale"
        'kikhihna': ('ki-khih-na', 'REFL-bind-NMLZ'),          # 7x - "binding oath"
        'angvan': ('ang-van', 'together-?'),                   # 7x - "respect"
        'luat': ('luat', 'exceed'),                            # 7x - "excess, over"
        'phalvak': ('phal-vak', 'permit-quick'),               # 7x - compound
        'ciahsuk': ('ciah-suk', 'return-down'),                # 7x - "return down"
        'hihgawp': ('hih-gawp', 'do-round'),                   # 7x - compound
        'paukhia': ('pau-khia', 'speak-emerge'),               # 7x - "speak out"
        'kuangkhia': ('kuang-khia', 'box-emerge'),             # 7x - compound
        'khuaphialep': ('khua-phial-ep', 'town-wide-?'),       # 7x - compound
        'nungkiksak': ('nung-kik-sak', 'live-ITER-CAUS'),      # 7x - "revive"
        'kolte': ('kol-te', 'wheel-PL'),                       # 7x - "wheels"
        'sahna': ('sah-na', 'grind-NMLZ'),                     # 7x - "grinding"
        'innkuankuanin': ('inn-kuan-kuan-in', 'house-family~REDUP-ERG'), # 7x - compound
        'apna': ('ap-na', 'cover-NMLZ'),                       # 7x - "covering"
        'nawksak': ('nawk-sak', 'again-CAUS'),                 # 7x - compound
        
        # Session 6 Round 11: Allomorph audit fixes - prevent over-segmentation
        # These are nouns/verbs that were being incorrectly split
        'hingte': ('hing-te', 'alive-PL'),                     # 14x - "living creatures"
        'hing': ('hing', 'alive'),                             # base
        'vunte': ('vun-te', 'skin-PL'),                        # 8x - "skins"
        'vun': ('vun', 'skin'),                                # base
        'thalte': ('thal-te', 'bow-PL'),                       # 8x - "bows"
        'thal': ('thal', 'bow'),                               # base - weapon
        'kihhuaite': ('ki-hhuai-te', 'REFL-abominate-PL'),     # 8x - "abominations"
        'taneute': ('taneu-te', 'child.small-PL'),             # 8x - "little ones"
        'taneu': ('taneu', 'child.small'),                     # base
        'teipite': ('teipi-te', 'spear-PL'),                   # 8x - "spears"
        'teipi': ('teipi', 'spear'),                           # base
        'kihisakte': ('ki-hisak-te', 'REFL-proud-PL'),         # 9x - "proud ones"
        'hisak': ('hisak', 'proud'),                           # base
        'gialte': ('gial-te', 'spotted-PL'),                   # 7x - "spotted ones"
        'gial': ('gial', 'spotted'),                           # base
        'anpalte': ('anpal-te', 'firstfruit-PL'),              # 8x - "firstfruits"
        'anpal': ('anpal', 'firstfruit'),                      # base
        'kingaknate': ('ki-ngak-na-te', 'REFL-wait-NMLZ-PL'),  # 10x - "bases, stands"
        'kineite': ('ki-nei-te', 'REFL-have-PL'),              # 10x - "upright ones"
        'delhte': ('delh-te', 'overcome-PL'),                  # 9x - "conquerors"
        'delh': ('delh', 'overcome'),                          # base verb
        'hilote': ('hi-lo-te', 'be-NEG-PL'),                   # 8x - "those who are not"
        'anlate': ('an-la-te', '3PL-take-PL'),                 # 8x - compound
        'zuakte': ('zuak-te', 'sell-PL'),                      # 8x - "sellers"
        'zuak': ('zuak', 'sell'),                              # base verb
        'innsungmangte': ('inn-sung-mang-te', 'house-inside-ruin-PL'), # 8x
        'vangliante': ('vanglian-te', 'mighty-PL'),            # 8x - "mighty ones"
        'vanglian': ('vanglian', 'mighty'),                    # base
        'sawmngate': ('sawmnga-te', 'fifty-PL'),               # 7x - compound
        'pawite': ('pawi-te', 'feast-PL'),                     # 12x - "feasts/offerings"
        'pawi': ('pawi', 'feast'),                             # base - feast/festival
        
        # Session 6 Round 12: More over-segmentation fixes from allomorph audit
        'innsate': ('innsa-te', 'cattle-PL'),                  # cattle (NOT i-nnsa-te)
        'innsa': ('innsa', 'cattle'),                          # base - cattle/domestic animals
        'gamsate': ('gamsa-te', 'beast-PL'),                   # beasts/wild animals
        'gamsa': ('gamsa', 'beast'),                           # base - wild beast
        'thukte': ('thuk-te', 'deep-PL'),                      # depths (NOT thu-k-te)
        'thuk': ('thuk', 'deep'),                              # base - deep/depth
        'kangte': ('kang-te', 'gray-PL'),                      # gray/white ones (hair)
        'kang': ('kang', 'gray'),                              # base - gray/white
        'keelpite': ('keelpi-te', 'she.goat-PL'),              # she-goats (NOT keel-pi-te)
        'keelpi': ('keelpi', 'she.goat'),                      # base - female goat
        'bawngpite': ('bawngpi-te', 'cattle.big-PL'),          # large cattle/kine
        'bawngpi': ('bawngpi', 'cattle.big'),                  # base - large cattle
        'tuilite': ('tuili-te', 'stream-PL'),                  # streams/ponds
        'tuili': ('tuili', 'stream'),                          # base - stream/pond
        'dalnate': ('dalna-te', 'hindrance-PL'),               # hindrances (dal-na-te correct)
        'dalna': ('dalna', 'hindrance'),                       # base - hindrance
        'suknate': ('sukna-te', 'becoming-PL'),                # becomings (suk-na-te correct)
        'sukna': ('sukna', 'becoming'),                        # base - process of becoming
        'cilte': ('cil-te', 'beginning-PL'),                   # beginnings
        'cil': ('cil', 'beginning'),                           # base - beginning (NOT ci-l)
        'kikoihte': ('kikoih-te', 'foundation-PL'),            # foundations
        'kikoih': ('kikoih', 'foundation'),                    # base - foundation
        'theihnate': ('theihna-te', 'knowledge-PL'),           # knowledges
        'theihna': ('theihna', 'knowledge'),                   # base - knowledge
        
        # Session 6 Round 13: More over-segmentation fixes
        'nunte': ('nun-te', 'knop-PL'),                        # knobs/knops (NOT nu-n-te)
        'nun': ('nun', 'knop'),                                # base - knob/knop (decorative)
        'kalte': ('kal-te', 'kidney-PL'),                      # kidneys (NOT ka-l-te)
        'kal': ('kal', 'kidney'),                              # base - kidney
        'pangte': ('pang-te', 'branch-PL'),                    # branches
        'pang': ('pang', 'branch'),                            # base - branch
        'gamgite': ('gamgi-te', 'border-PL'),                  # borders/bounds
        'gamgi': ('gamgi', 'border'),                          # base - border/boundary
        
        # Session 6 Round 14: More over-segmentation fixes
        'sante': ('san-te', 'garlic-PL'),                      # garlick (NOT sa-n-te)
        'san': ('san', 'garlic'),                              # base - garlic
        'zinte': ('zin-te', 'sojourner-PL'),                   # strangers (NOT zi-n-te)
        'zin': ('zin', 'sojourner'),                           # base - stranger/sojourner
        'khutpite': ('khutpi-te', 'thumb-PL'),                 # thumbs  
        'khutpi': ('khutpi', 'thumb'),                         # base - thumb (hand-big)
        'khepite': ('khepi-te', 'big.toe-PL'),                 # great toes
        'khepi': ('khepi', 'big.toe'),                         # base - big toe
        'liammate': ('liamma-te', 'wound-PL'),                 # wounds (8 occurrences)
        'liamma': ('liamma', 'wound'),                         # base - wound/injury
        'thongkiate': ('thongkia-te', 'prison-PL'),            # prisons
        'thongkia': ('thongkia', 'prison'),                    # base - prison
        'kungnote': ('kungno-te', 'herb-PL'),                  # herbs (trees bringing forth)
        'kungno': ('kungno', 'herb'),                          # base - herb/plant
        'khawkte': ('khawk-te', 'spirit-PL'),                  # spirits
        'khawk': ('khawk', 'spirit'),                          # base - spirit
        
        # Session 6 Round 15: More over-segmentation fixes
        'kamte': ('kam-te', 'word-PL'),                        # words/speeches (NOT ka-m-te)
        'kam': ('kam', 'word'),                                # base - word/speech
        'bengte': ('beng-te', 'companion-PL'),                 # companions/fishers
        'beng': ('beng', 'companion'),                         # base - companion/fisher
        'zungte': ('zung-te', 'root-PL'),                      # roots (of plants)
        'zung': ('zung', 'root'),                              # base - root
        'muangte': ('muang-te', 'trust-PL'),                   # those who trust  
        'muang': ('muang', 'trust'),                           # base - trust (nominalizer)
        'buluhte': ('buluh-te', 'troop-PL'),                   # troops/robbers
        'buluh': ('buluh', 'troop'),                           # base - troop/band
        'kuamte': ('kuam-te', 'plain-PL'),                     # plains/valleys
        'kuam': ('kuam', 'plain'),                             # base - plain/valley
        'huhte': ('huh-te', 'help-PL'),                        # helpers
        'huh': ('huh', 'help'),                                # base - help
        
        # Session 6 Round 16: More over-segmentation fixes  
        'taktakte': ('taktak-te', 'genuine-PL'),               # genuine/true ones
        'taktak': ('taktak', 'genuine'),                       # base - truly/genuine
        'ganhonte': ('ganhon-te', 'flock-PL'),                 # flocks/herds
        'ganhon': ('ganhon', 'flock'),                         # base - flock/herd
        'khedapte': ('khedap-te', 'shoe-PL'),                  # shoes/sandals
        'khedap': ('khedap', 'shoe'),                          # base - shoe/sandal
        'tawmte': ('tawm-te', 'produce-PL'),                   # produce/growth
        'tawm': ('tawm', 'produce'),                           # base - produce
        'ngimnate': ('ngimna-te', 'imagination-PL'),           # imaginations/thoughts
        'ngimna': ('ngimna', 'imagination'),                   # base - imagination
        'mukte': ('muk-te', 'lip-PL'),                         # lips (NOT mu-k-te)
        'muk': ('muk', 'lip'),                                 # base - lip
        
        # Session 6 Round 17: More over-segmentation fixes
        'kawbiate': ('kawbia-te', 'shovel-PL'),                # shovels/basins (NOT ka-wbia-te)
        'kawbia': ('kawbia', 'shovel'),                        # base - shovel/basin
        'ngaknate': ('ngakna-te', 'base-PL'),                  # bases/feet (of laver)
        'ngakna': ('ngakna', 'base'),                          # base - foot/base/stand
        'nengniamte': ('nengniam-te', 'oppressor-PL'),         # oppressors (NOT ne-ngniam-te)
        'nengniam': ('nengniam', 'oppressor'),                 # base - oppressor
        'leenglate': ('leengla-te', 'guest-PL'),               # guests/invitees (NOT leeng-la-te)
        'leengla': ('leengla', 'guest'),                       # base - guest/invitee
        'innlamte': ('innlam-te', 'builder-PL'),               # builders (NOT i-nnlam-te)
        'innlam': ('innlam', 'builder'),                       # base - builder/mason
        'gitlohnate': ('gitlohna-te', 'wickedness-PL'),        # wickednesses/sins
        'gitlohna': ('gitlohna', 'wickedness'),                # base - wickedness
        'mawhsakte': ('mawhsak-te', 'adversary-PL'),           # adversaries
        'mawhsak': ('mawhsak', 'adversary'),                   # base - adversary/enemy
        
        # Session 6 Round 18: More over-segmentation fixes
        'bilvangte': ('bilvang-te', 'loop-PL'),                # loops (curtain coupling)
        'bilvang': ('bilvang', 'loop'),                        # base - loop
        'mithagolte': ('mithagol-te', 'giant-PL'),             # giants
        'mithagol': ('mithagol', 'giant'),                     # base - giant
        'lianpipite': ('lianpipi-te', 'great-PL'),             # great ones (stones)
        'lianpipi': ('lianpipi', 'great'),                     # base - great/large
        'lelte': ('lel-te', 'desperate-PL'),                   # desperate ones
        'lel': ('lel', 'desperate'),                           # base - desperate
        'thante': ('than-te', 'worm-PL'),                      # worms/corruption
        'than': ('than', 'worm'),                              # base - worm
        'dote': ('do-te', 'rise-PL'),                          # those who rise up
        'do': ('do', 'rise'),                                  # base - rise against
        'ngeekte': ('ngeek-te', 'herb-PL'),                    # herbs/grass
        'ngeek': ('ngeek', 'herb'),                            # base - herb/grass
        
        # Session 6 Round 19: More over-segmentation fixes
        'ankungte': ('ankung-te', 'herb-PL'),                  # herbs of field (NOT a-nkung-te)
        'ankung': ('ankung', 'herb'),                          # base - herb/plant of field
        'natnate': ('natna-te', 'disease-PL'),                 # diseases (NOT na-tna-te)
        'natna': ('natna', 'disease'),                         # base - disease/sickness
        'geelnate': ('geelna-te', 'way-PL'),                   # ways/manners
        'geelna': ('geelna', 'way'),                           # base - way/manner
        'ngiate': ('ngia-te', 'field-PL'),                     # standing corn/fields
        'ngia': ('ngia', 'field'),                             # base - field/standing grain
        'lungkhamnate': ('lungkhamna-te', 'tribulation-PL'),   # tribulations
        'lungkhamna': ('lungkhamna', 'tribulation'),           # base - tribulation
        'hauhnate': ('hauhna-te', 'riches-PL'),                # riches/wealth
        'hauhna': ('hauhna', 'riches'),                        # base - riches
        'phatnate': ('phatna-te', 'praise-PL'),                # praises
        'phatna': ('phatna', 'praise'),                        # base - praise
        'tagahte': ('tagah-te', 'orphan-PL'),                  # orphans/fatherless
        'tagah': ('tagah', 'orphan'),                          # base - orphan
        'meigongte': ('meigong-te', 'widow-PL'),               # widows
        'meigong': ('meigong', 'widow'),                       # base - widow
        'khutmete': ('khutme-te', 'finger-PL'),                # fingers (NOT khut-me-te)
        'khutme': ('khutme', 'finger'),                        # base - finger (hand-small)
        
        # Session 6 Round 20: More over-segmentation fixes
        'meimate': ('meima-te', 'wound-PL'),                   # wounds
        'meima': ('meima', 'wound'),                           # base - wound/sore
        'kimte': ('kim-te', 'nation-PL'),                      # all nations/peoples
        'kim': ('kim', 'nation'),                              # base - all/nation
        'lawkite': ('lawki-te', 'Gentile-PL'),                 # Gentiles/heathen
        'lawki': ('lawki', 'Gentile'),                         # base - Gentile/heathen
        'ciangkangte': ('ciangkang-te', 'rod-PL'),             # rods/peeled sticks (NOT cian-gkang)
        'ciangkang': ('ciangkang', 'rod'),                     # base - rod/peeled stick
        'kicite': ('kici-te', 'called-PL'),                    # those called/named
        'kici': ('kici', 'called'),                            # base - be called
        'leenggahte': ('leenggah-te', 'grape-PL'),             # grapes (NOT leeng-gah-te)
        'leenggah': ('leenggah', 'grape'),                     # base - grape
        'kholhnate': ('kholhna-te', 'enchantment-PL'),         # enchantments/divinations
        'kholhna': ('kholhna', 'enchantment'),                 # base - enchantment
        
        # Session 6 Round 21: More over-segmentation fixes
        'anlimte': ('anlim-te', 'dainty-PL'),                  # dainties (NOT a-nlim-te)
        'anlim': ('anlim', 'dainty'),                          # base - dainty/delicacy
        'gannote': ('ganno-te', 'lamb-PL'),                    # lambs/fatlings
        'ganno': ('ganno', 'lamb'),                            # base - lamb/young animal
        'zawngte': ('zawng-te', 'poor-PL'),                    # the poor (NOT za-wng-te)
        'zawng': ('zawng', 'poor'),                            # base - poor
        'kiute': ('kiu-te', 'corner-PL'),                      # corners
        'kiu': ('kiu', 'corner'),                              # base - corner
        'haute': ('hau-te', 'rich-PL'),                        # the rich
        'hau': ('hau', 'rich'),                                # base - rich
        'pote': ('po-te', 'grow-PL'),                          # growths/harvests
        'po': ('po', 'grow'),                                  # base - grow
        'namtuite': ('namtui-te', 'perfume-PL'),               # perfumes/odours (NOT na-mtui-te)
        'namtui': ('namtui', 'perfume'),                       # base - oil/perfume
        'miphakte': ('miphak-te', 'leper-PL'),                 # lepers
        'miphak': ('miphak', 'leper'),                         # base - leper (person-strike)
        'gamhte': ('gamh-te', 'inheritance-PL'),               # inheritances (NOT gam-h-te)
        'gamh': ('gamh', 'inheritance'),                       # base - inheritance
        
        # Session 6 Round 22: More over-segmentation fixes
        'tuletate': ('tuleta-te', 'breast-PL'),                # breasts/wombs
        'tuleta': ('tuleta', 'breast'),                        # base - breast/womb
        'khainiangte': ('khainiang-te', 'chain-PL'),           # chains/wreaths
        'khainiang': ('khainiang', 'chain'),                   # base - chain
        'puantungsilhte': ('puantungsilh-te', 'coat-PL'),      # coats (NOT pua-ntungsilh-te)
        'puantungsilh': ('puantungsilh', 'coat'),              # base - coat
        'ekte': ('ek-te', 'dung-PL'),                          # dung/excrement
        'ek': ('ek', 'dung'),                                  # base - dung
        'bilngongte': ('bilngong-te', 'deaf-PL'),              # deaf ones
        'bilngong': ('bilngong', 'deaf'),                      # base - deaf (ear-closed)
        'pulepate': ('pulepa-te', 'ancestor-PL'),              # ancestors
        'pulepa': ('pulepa', 'ancestor'),                      # base - ancestor
        
        # Round 23: More vocabulary (Deut, Judges, Kings, Chronicles)
        'haksatnate': ('haksatna-te', 'trouble-PL'),           # troubles/difficulties
        'haksatna': ('haksat-na', 'difficult-NMLZ'),           # trouble/difficulty
        'haksat': ('haksat', 'difficult'),                     # base - difficult
        'kithatte': ('ki-that-te', 'REFL-kill-PL'),            # slain ones (ki-that reflexive)
        'kiseelte': ('ki-seel-te', 'REFL-hide-PL'),            # hidden things
        'kiseel': ('ki-seel', 'REFL-hide'),                    # base - ki-seel
        'seel': ('seel', 'hide'),                              # base - hide
        'hangte': ('hang-te', 'stallion-PL'),                  # stallions/mighty ones
        'hang': ('hang', 'stallion'),                          # base - stallion/mighty
        'meivakkhuamte': ('meivakkhuam-te', 'candlestick-PL'), # candlesticks
        'meivakkhuam': ('mei-vak-khuam', 'fire-light-holder'), # candlestick/lampstand
        'leenggahzute': ('leenggahzu-te', 'frankincense-PL'),  # frankincense/spices
        'leenggahzu': ('leeng-gahzu', 'incense-fragrant'),     # frankincense
        'gahzu': ('gahzu', 'fragrant'),                        # base - fragrant
        'sungnungte': ('sungnung-te', 'inner.room-PL'),        # inner chambers/rooms
        'sungnung': ('sungnung', 'inner.room'),                # base - inner room
        'lamlakte': ('lamlak-te', 'counsellor-PL'),            # counsellors/advisers
        'lamlak': ('lamlak', 'counsellor'),                    # base - counsellor
        
        # More vocabulary
        'lokhote': ('lokho-te', 'farmer-PL'),                  # farmers/husbandmen
        'lokho': ('lokho', 'farmer'),                          # base - farmer
        'laitaite': ('laitai-te', 'messenger-PL'),             # posts/messengers
        'laitai': ('laitai', 'messenger'),                     # base - messenger/post
        'thupalsatnate': ('thupalsatna-te', 'transgression-PL'),  # transgressions
        'thupalsatna': ('thu-palsat-na', 'word-transgress-NMLZ'), # transgression
        'namsaute': ('namsau-te', 'knife-PL'),                 # knives/lances
        'namsau': ('namsau', 'knife'),                         # base - knife
        'vankinusiate': ('vankinusia-te', 'colored.spoil-PL'), # colored spoils
        'vankinusia': ('vankinusia', 'colored.spoil'),         # colored spoil/prey
        'vanmanphate': ('vanmanpha-te', 'treasure-PL'),        # treasures
        'vanmanpha': ('vanmanpha', 'treasure'),                # base - treasure/valuable
        
        # Round 24: Job, Psalms, Exodus, Chronicles vocabulary
        'khuamluzepnate': ('khuamluzepna-te', 'fillet-PL'),    # fillets/bands
        'khuamluzepna': ('khuam-luzep-na', 'pole-encircle-NMLZ'), # fillet/band
        'luzep': ('luzep', 'encircle'),                        # base - encircle/surround
        'kihhuainate': ('kihhuaina-te', 'abomination-PL'),     # abominations
        'kihhuaina': ('kihhuai-na', 'abominate-NMLZ'),         # abomination
        'kihhuai': ('ki-hhuai', 'REFL-abominate'),             # abominate
        'vaihawmnate': ('vaihawmna-te', 'counsel-PL'),         # counsels/secrets
        'vaihawmna': ('vai-hawm-na', 'plan-counsel-NMLZ'),     # counsel/secret
        'dangtakte': ('dangtak-te', 'weary-PL'),               # weary/tired ones
        'dangtak': ('dangtak', 'weary'),                       # base - weary/tired
        'thungetnate': ('thungetna-te', 'prayer-PL'),          # prayers
        'thungetna': ('thu-nget-na', 'word-pray-NMLZ'),        # prayer
        'papite': ('papi-te', 'elder-PL'),                     # elders/aged men
        'papi': ('papi', 'elder'),                             # base - elder/aged
        'mawhsaknate': ('mawhsakna-te', 'sin.offering-PL'),    # sin offerings
        'mawhsakna': ('mawh-sak-na', 'sin-CAUS-NMLZ'),         # sin offering
        'kisate': ('kisa-te', 'proud-PL'),                     # proud ones
        'kisa': ('kisa', 'proud'),                             # base - proud
        'miphate': ('mipha-te', 'righteous-PL'),               # righteous ones
        'mipha': ('mi-pha', 'person-good'),                    # righteous
        
        # Round 25: Psalms vocabulary
        'paunate': ('pauna-te', 'word-PL'),                    # words (as spoken)
        'pauna': ('pau-na', 'speak-NMLZ'),                     # word/speech
        'belte': ('bel-te', 'trust-PL'),                       # those who trust
        'bel': ('bel', 'trust'),                               # base - trust
        'lehdote': ('lehdo-te', 'rebellious-PL'),              # rebellious ones
        'lehdo': ('lehdo', 'rebellious'),                      # base - rebellious
        'khawite': ('khawi-te', 'flock-PL'),                   # flocks/herds
        'khawi': ('khawi', 'flock'),                           # base - flock/herd
        'dawibiate': ('dawibia-te', 'heathen-PL'),             # heathens/gentiles
        'dawibia': ('dawibia', 'heathen'),                     # base - heathen
        'nopsaknate': ('nopsakna-te', 'restoration-PL'),       # restorations
        'nopsakna': ('nopsak-na', 'restore-NMLZ'),             # restoration
        'nopsak': ('nopsak', 'restore'),                       # base - restore
        'hualte': ('hual-te', 'wave-PL'),                      # waves
        'hual': ('hual', 'wave'),                              # base - wave
        'theikungte': ('theikung-te', 'fig.tree-PL'),          # fig trees
        'theikung': ('thei-kung', 'fruit-tree'),               # fig tree
        
        # Round 26: More Psalms, Proverbs, Genesis, Exodus vocabulary
        'tokhomte': ('tokhom-te', 'throne-PL'),                # thrones
        'tokhom': ('tokhom', 'throne'),                        # base - throne
        'hanciamte': ('hanciam-te', 'pursuer-PL'),             # pursuers
        'hanciam': ('hanciam', 'pursue'),                      # base - pursue/strive
        'galkapbute': ('galkapbu-te', 'captain-PL'),           # captains of soldiers
        'galkapbu': ('galkap-bu', 'soldier-leader'),           # captain
        'taaute': ('taau-te', 'bracelet-PL'),                  # bracelets
        'taau': ('taau', 'bracelet'),                          # base - bracelet
        'puansilhte': ('puansilh-te', 'garment-PL'),           # garments/clothes
        'puansilh': ('puan-silh', 'cloth-wear'),               # garment
        'phunnate': ('phunna-te', 'murmuring-PL'),             # murmurings
        'phunna': ('phun-na', 'murmur-NMLZ'),                  # murmuring
        'phun': ('phun', 'murmur'),                            # base - murmur
        'kuangdaite': ('kuangdai-te', 'dish-PL'),              # dishes
        'kuangdai': ('kuang-dai', 'container-flat'),           # dish
        'dai': ('dai', 'flat'),                                # base - flat
        'kilhnate': ('kilhna-te', 'clasp-PL'),                 # clasps/taches
        'kilhna': ('kilh-na', 'join-NMLZ'),                    # clasp
        'kilh': ('kilh', 'join'),                              # base - join
        
        # Round 27: Nominalizations from various books
        'sawmsimna': ('sawmsim-na', 'conspiracy-NMLZ'),        # conspiracy
        'sawmsim': ('sawmsim', 'conspire'),                    # base - conspire
        'zahkona': ('zahko-na', 'reproach-NMLZ'),              # reproach/shame
        'zahko': ('zah-ko', 'shame-have'),                     # reproach/shame
        'lungzinna': ('lungzin-na', 'darkness-NMLZ'),          # shadow/darkness
        'lungzin': ('lung-zin', 'heart-shadow'),               # shadow/darkness
        'palsatna': ('palsat-na', 'transgression-NMLZ'),       # transgression
        'palsat': ('palsat', 'transgress'),                    # base - transgress
        'hetlohna': ('hetloh-na', 'displeasure-NMLZ'),         # displeasure
        'hetloh': ('het-loh', 'approve-NEG'),                  # disapprove
        'deihluatna': ('deihluat-na', 'zeal-NMLZ'),            # zeal
        'deihluat': ('deih-luat', 'want-exceed'),              # be zealous
        'kimuanna': ('kimuan-na', 'confidence-NMLZ'),          # confidence
        'kimuan': ('ki-muan', 'REFL-believe'),                 # trust/believe self
        
        # Round 28: More vocabulary from Genesis, Exodus, Nahum, Jeremiah
        'mette': ('met-te', 'shearer-PL'),                     # shearers
        'met': ('met', 'shear'),                               # base - shear
        'mapite': ('mapi-te', 'officer-PL'),                   # officers/overseers
        'mapi': ('mapi', 'officer'),                           # base - officer
        'mohte': ('moh-te', 'cake-PL'),                        # cakes (unleavened)
        'moh': ('moh', 'cake'),                                # base - cake
        'mohphengte': ('mohpheng-te', 'wafer-PL'),             # wafers
        'mohpheng': ('moh-pheng', 'cake-flat'),                # wafer
        'pheng': ('pheng', 'flat'),                            # base - flat
        'puankhaite': ('puankhai-te', 'hanging-PL'),           # hangings/curtains
        'puankhai': ('puan-khai', 'cloth-hang'),               # hanging
        'khai': ('khai', 'hang'),                              # base - hang
        'sikkhaute': ('sikkhau-te', 'bond-PL'),                # bonds/yokes
        'sikkhau': ('sik-khau', 'tie-rope'),                   # bond/yoke
        'mineute': ('mineu-te', 'little.one-PL'),              # little ones
        'mineu': ('mi-neu', 'person-small'),                   # little one
        'ciangkhutte': ('ciangkhut-te', 'stripe-PL'),          # stripes/white streaks
        'ciangkhut': ('ciang-khut', 'white-part'),             # stripe/streak
        
        # Round 29: High-frequency partial words
        'gialpi': ('gial-pi', 'hail-big'),                     # grievous hail
        'pi': ('pi', 'big'),                                   # base - big/great
        'palsatin': ('palsat-in', 'transgress-ERG'),           # transgressing
        'semsemin': ('semsem-in', 'breathe-ERG'),              # breathing/dying
        'semsem': ('semsem', 'breathe'),                       # breathe (intensive)
        'zawt': ('zawt', 'weary'),                             # base - weary/tire
        'musane': ('musane', 'pelican'),                       # pelican (bird)
        'limtak': ('lim-tak', 'true-true'),                    # truly/well/accepted
        'khuaphialep': ('khua-phial-ep', 'sky-flash-lightning'), # lightning
        'phial': ('phial', 'flash'),                           # base - flash
        'ep': ('ep', 'strike'),                                # base - strike/hit
        'balnenin': ('balnen-in', 'tear-ERG'),                 # tearing/torn
        'balnen': ('balnen', 'tear'),                          # base - tear/rip
        'luhin': ('luh-in', 'smite-ERG'),                      # smiting/ripping
        'luh': ('luh', 'smite'),                               # base - smite/rip
        'pelmawh': ('pel-mawh', 'report-evil'),                # report/denounce
        'nawkgawp': ('nawk-gawp', 'overtake-all'),             # overwhelm/tempest
        'nawk': ('nawk', 'overtake'),                          # base - overtake
        'gawp': ('gawp', 'all'),                               # base - all
        
        # Round 30: More high-frequency partial words
        'omteng': ('om-teng', 'exist-remain'),                 # remain/survive
        'teng': ('teng', 'remain'),                            # base - remain
        'omlain': ('om-lai-in', 'exist-midst-ERG'),            # existing in midst
        'dington': ('ding-ton', 'stand-stable'),               # stand firm
        'ton': ('ton', 'stable'),                              # base - stable
        'tonu': ('tonu', 'mistress'),                          # mistress/lady
        'bai': ('bai', 'rise.early'),                          # rise early/arise
        'dampah': ('dam-pah', 'healthy-clear'),                # cleansed/healed
        'pah': ('pah', 'clear'),                               # base - clear
        'henhan': ('hen-han', 'spread-spread'),                # spreading
        'hen': ('hen', 'spread'),                              # base - spread
        'hitaseleh': ('hi-ta-se-leh', 'be-that-CONN-COND'),    # although that
        'bawlsiain': ('bawl-sia-in', 'make-evil-ERG'),         # doing evil
        
        # Round 31: More high-frequency partial words
        'kongpuankhai': ('kong-puan-khai', 'door-cloth-hang'),   # hanging/curtain
        'vawhin': ('vawh-in', 'arise-ERG'),                    # arising
        'vawh': ('vawh', 'arise'),                             # base - arise/rise
        'baan': ('baan', 'lay'),                               # base - lay/put
        'liangkoah': ('liangko-ah', 'shoulder-LOC'),           # on shoulders
        'liangko': ('liangko', 'shoulder'),                    # base - shoulder
        'pataukohna': ('pataukoh-na', 'alarm-NMLZ'),           # alarm/trumpet call
        'pataukoh': ('pa-tau-koh', 'male-signal-call'),        # alarm/trumpet call
        'tau': ('tau', 'signal'),                              # base - signal
        'gelhsa': ('gelh-sa', 'write-PERF'),                   # written
        'nilhin': ('nilh-in', 'anoint-ERG'),                   # anointing
        'nilh': ('nilh', 'anoint'),                            # base - anoint
        
        # Round 32: More vocabulary from Numbers, Deut, Kings, Judges
        'zawngin': ('zawng-in', 'lack-ERG'),                   # lacking/poor
        'zawng': ('zawng', 'lack'),                            # base - lack
        'hamsia': ('ham-sia', 'curse-evil'),                   # curse
        'nawkkha': ('nawk-kha', 'turn-CAUS'),                  # turn aside
        'khuaneu': ('khua-neu', 'town-small'),                 # village
        'neu': ('neu', 'small'),                               # base - small
        'angvan': ('ang-van', 'face-see'),                     # show favoritism
        'sawtpi': ('sawt-pi', 'long-big'),                     # prolong/long time
        'sawt': ('sawt', 'long'),                              # base - long
        'sukhamin': ('sukham-in', 'grind-ERG'),                # grinding
        'sukham': ('su-kham', 'make-grind'),                   # grind
        'cinna': ('cin-na', 'plant-NMLZ'),                     # garden/planting
        'cin': ('cin', 'plant'),                               # base - plant
        'kiatna': ('kiat-na', 'fall-NMLZ'),                    # falling place
        'kiat': ('kiat', 'fall'),                              # base - fall
        'samzang': ('sam-zang', 'throw-INSTR'),                # sling
        'zang': ('zang', 'use'),                               # base - use
        'kidop': ('ki-dop', 'REFL-guard'),                     # take heed
        'dop': ('dop', 'guard'),                               # base - guard
        'keucip': ('keu-cip', 'dry-tight'),                    # dried up
        'keu': ('keu', 'dry'),                                 # base - dry
        'cip': ('cip', 'tight'),                               # base - tight
        'sutat': ('su-tat', 'break-COMPL'),                    # break/sever
        
        # Round 33: More vocabulary from Chronicles, Kings, Numbers, Deut
        'ukpipa': ('uk-pi-pa', 'rule-big-male'),               # prince/chief
        'vangtaang': ('vang-taang', 'glory-beautiful'),        # glory
        'taang': ('taang', 'beautiful'),                       # base - beautiful
        'kiphuh': ('ki-phuh', 'REFL-rest'),                    # abide/rest
        'phuh': ('phuh', 'rest'),                              # base - rest
        'phelkhia': ('phel-khia', 'break-out'),                # overthrow/destroy
        'khia': ('khia', 'out'),                               # base - out
        'kangtumin': ('kangtum-in', 'consume-ERG'),            # consuming
        'kangtum': ('kang-tum', 'burn-all'),                   # consume
        'siahuaizaw': ('sia-huai-zaw', 'evil-bad-more'),       # more evil
        'huai': ('huai', 'bad'),                               # base - bad
        'zaw': ('zaw', 'more'),                                # base - more/comparative
        'humpinelkaite': ('humpinelkai-te', 'ornament-PL'),    # ornaments/decorations
        'humpinelkai': ('hum-pinelkai', 'cover-ornament'),     # ornament
        'pinelkai': ('pinelkai', 'ornament'),                  # base - ornament
        'sawmnihna': ('sawm-nih-na', 'ten-two-ORD'),           # twentieth
        'nih': ('nih', 'two'),                                 # base - two
        
        # Round 34: More vocabulary from Nehemiah, Esther, Job, Psalms
        'vangliatnate': ('vangliatna-te', 'power-PL'),         # powers/might
        'vangliatna': ('vang-liat-na', 'glory-power-NMLZ'),    # power/might
        'naptui': ('nap-tui', 'wet-water'),                    # tears
        'nap': ('nap', 'wet'),                                 # base - wet
        'tenpihna': ('tenpih-na', 'marry-NMLZ'),               # marriage/taking
        'tenpih': ('ten-pih', 'stay-with'),                    # marry/live with
        'hawmsuak': ('hawm-suak', 'shake-become'),             # emptied/shaken
        'hoihnate': ('hoihna-te', 'goodness-PL'),              # good deeds
        'innsungmang': ('innsungmang', 'eunuch'),              # eunuch (palace servant)
        'antanna': ('antan-na', 'fast-NMLZ'),                  # fasting
        'antan': ('an-tan', 'food-stop'),                      # fast/abstain
        'pakin': ('pa-kin', 'completely-destroy'),             # perish
        'pianma': ('pian-ma', 'born-before'),                  # elder/very old
        'omom': ('om-om', 'exist-exist'),                      # remain/still
        'mutkhiat': ('mut-khiat', 'blow-away'),                # blow away
        'mut': ('mut', 'blow'),                                # base - blow
        'nuihsat': ('nuih-sat', 'laugh-toward'),               # laugh at
        'imcip': ('im-cip', 'hide-tight'),                     # hide/conceal
        'im': ('im', 'hide'),                                  # base - hide
        'zalzal': ('zal-zal', 'shake-shake'),                  # rattle/shake
        'zal': ('zal', 'shake'),                               # base - shake
        'hihnop': ('hih-nop', 'do-want'),                      # plan/thought
        'zahhuai': ('zah-huai', 'ashamed-bad'),                # ashamed/vexed
        
        # Round 35: More vocabulary
        'kiliatsakna': ('ki-liat-sak-na', 'REFL-oppress-CAUS-NMLZ'), # oppression
        'kiselna': ('ki-sel-na', 'REFL-quarrel-NMLZ'),         # strife
        'sel': ('sel', 'quarrel'),                             # base - quarrel
        'nuntakzia': ('nuntak-zia', 'live-manner'),            # ways/lifestyle
        'zia': ('zia', 'manner'),                              # base - manner
        'damdam': ('dam-dam', 'well-well'),                    # softly/gently
        'maitai': ('mai-tai', 'face-bright'),                  # radiant/lightened
        'etlawm': ('et-lawm', 'fat-lamb'),                     # fat/fatness
        'lawm': ('lawm', 'lamb'),                              # base - lamb
        'ngaihsunkha': ('ngaihsun-kha', 'think-CAUS'),         # thought/imagine
        'nilkhiat': ('nil-khiat', 'throw-away'),               # refuse/reject
        'nil': ('nil', 'throw'),                               # base - throw
        'thuakpih': ('thuak-pih', 'suffer-with'),              # adversity/trouble
        'hamphazaw': ('ham-pha-zaw', 'full-good-more'),        # better/more
        'suaktalai': ('suak-ta-lai', 'become-PERF-midst'),     # remnant/escaped
        
        # Round 36: More vocabulary from prophets
        'mualsang': ('mual-sang', 'hill-high'),                # high places
        'sang': ('sang', 'high'),                              # base - high
        'dialkaih': ('dial-kaih', 'belt-loosen'),              # girdle/belt
        'dial': ('dial', 'belt'),                              # base - belt
        'kaih': ('kaih', 'loosen'),                            # base - loosen
        'khuakulhpi': ('khua-kulh-pi', 'town-wall-big'),       # fenced wall
        'kulhpi': ('kulh-pi', 'wall-big'),                     # great wall
        'mulkimhuai': ('mul-kim-huai', 'full-all-bad'),        # horrible
        'mul': ('mul', 'full'),                                # base - full
        'thuvanpi': ('thu-van-pi', 'word-write-master'),       # scribe
        'thuakkhawm': ('thuak-khawm', 'suffer-together'),      # suffer together
        'khawm': ('khawm', 'together'),                        # base - together
        'tangsak': ('tang-sak', 'give-CAUS'),                  # give/provide
        'theinuam': ('thei-nuam', 'know-want'),                # want to know
        'nuam': ('nuam', 'want'),                              # base - want
        'paunam': ('pau-nam', 'speak-nation'),                 # language
        'nam': ('nam', 'nation'),                              # base - nation
        'paipah': ('pai-pah', 'go-arrive'),                    # arrive/come
        'tonkhawm': ('ton-khawm', 'meet-together'),            # meet together
        
        # Round 37: More vocabulary from Matthew, Genesis, Exodus
        'zineipa': ('zinei-pa', 'marry-male'),                 # bridegroom
        'zinei': ('zinei', 'marry'),                           # base - marry
        'meivakna': ('mei-vak-na', 'fire-light-NMLZ'),         # candlestick/lamp
        'innteek': ('inn-teek', 'house-master'),               # householder/master
        'teek': ('teek', 'master'),                            # base - master
        'pianpih': ('pian-pih', 'born-with'),                  # born together
        'zukhamna': ('zukham-na', 'wine-NMLZ'),                # wine/drunkenness
        'zukham': ('zukham', 'wine'),                          # base - wine
        'thaneemna': ('thaneem-na', 'naked-NMLZ'),             # nakedness
        'thaneem': ('thaneem', 'naked'),                       # base - naked
        'niamsak': ('niam-sak', 'bow-CAUS'),                   # bow down
        'niam': ('niam', 'bow'),                               # base - bow
        'kikhenthang': ('ki-khen-thang', 'REFL-separate-scatter'), # scattered
        'thang': ('thang', 'scatter'),                         # base - scatter
        'khing': ('khing', 'remain'),                          # base - remain
        'dikdek': ('dik-dek', 'small-REDUP'),                  # very small
        'dik': ('dik', 'small'),                               # base - small
        'dek': ('dek', 'REDUP'),                               # base - reduplication
        'paisuaksak': ('pai-suak-sak', 'go-become-CAUS'),      # break through
        'balzan': ('bal-zan', 'tear-PERF'),                    # torn
        'khutpeek': ('khut-peek', 'hand-breadth'),             # hand breadth
        'peek': ('peek', 'breadth'),                           # base - breadth
        'vutluahna': ('vut-luah-na', 'ash-carry-NMLZ'),        # firepan
        'vut': ('vut', 'ash'),                                 # base - ash
        'luah': ('luah', 'carry'),                             # base - carry
        'siklen': ('sik-len', 'tie-net'),                      # grate/net
        'len': ('len', 'net'),                                 # base - net
        'simsiam': ('sim-siam', 'count-make'),                 # network/workmanship
        'thuap': ('thu-ap', 'measure-span'),                   # span (measurement)
        'ap': ('ap', 'span'),                                  # base - span
        'khutsiam': ('khut-siam', 'hand-skill'),               # workmanship
        'siam': ('siam', 'skill'),                             # base - skill
        
        # Round 38: More vocabulary from Genesis, Exodus, Leviticus, Numbers
        'nungngatin': ('nung-ngat-in', 'back-opposite-ERG'),   # over against
        'ngat': ('ngat', 'opposite'),                          # base - opposite
        'ompihin': ('om-pih-in', 'exist-with-ERG'),            # being with
        'khiatpih': ('khiat-pih', 'depart-with'),              # bring out
        'semnen': ('sem-nen', 'cut-pieces'),                   # cut in pieces
        'nen': ('nen', 'pieces'),                              # base - pieces
        'sitset': ('sit-set', 'wash-clean'),                   # scour/clean
        'set': ('set', 'clean'),                               # base - clean
        'vallai': ('val-lai', 'pour-lay'),                     # pour out
        'val': ('val', 'pour'),                                # base - pour
        'tuampian': ('tuam-pian', 'swell-appear'),             # rising/bright spot
        'tuam': ('tuam', 'swell'),                             # base - swell
        'piakzawh': ('piak-zawh', 'give-finish'),              # give completely
        'neksak': ('nek-sak', 'eat-CAUS'),                     # cause to eat/devour
        'hinna': ('hi-n-na', 'be-CONN-NMLZ'),                  # life/living
        'velval': ('vel-val', 'turn-turn'),                    # causing/making bitter
        'vel': ('vel', 'turn'),                                # base - turn
        'tuithuk': ('tui-thuk', 'water-deep'),                 # deep/depth
        'thuk': ('thuk', 'deep'),                              # base - deep
        
        # Round 39: More vocabulary from Numbers, Leviticus, Deuteronomy
        'mulkiatna': ('mul-kiat-na', 'hair-cut-NMLZ'),         # razor
        'piakhawm': ('piak-hawm', 'give-together'),            # offer together
        'hawm': ('hawm', 'together'),                          # base - together
        'sutan': ('sut-an', 'break-NEG'),                      # not break
        'sut': ('sut', 'break'),                               # base - break
        'kibangsak': ('ki-bang-sak', 'REFL-equal-CAUS'),       # sound alarm
        'bang': ('bang', 'equal'),                             # base - equal
        'laipi': ('lai-pi', 'midst-big'),                      # lifetime/while
        'lai': ('lai', 'midst'),                               # base - midst
        'dingkhawm': ('ding-khawm', 'stand-together'),         # stand together
        'kihalna': ('ki-hal-na', 'REFL-burn-NMLZ'),            # burning
        'tuanna': ('tuan-na', 'ride-NMLZ'),                    # riding/beast
        'tuan': ('tuan', 'ride'),                              # base - ride
        'lungkiasak': ('lung-kia-sak', 'heart-fall-CAUS'),     # discourage
        'kia': ('kia', 'fall'),                                # base - fall
        'hehsakna': ('heh-sak-na', 'anger-CAUS-NMLZ'),         # provocation
        'kisatna': ('ki-sat-na', 'REFL-strike-NMLZ'),          # controversy/stroke
        'sat': ('sat', 'strike'),                              # base - strike
        'khanglui': ('khang-lui', 'generation-old'),           # old time
        'lui': ('lui', 'old'),                                 # base - old
        'ciahpihin': ('ciah-pih-in', 'return-with-ERG'),       # bring/restore
        'paithei': ('pai-thei', 'go-able'),                    # able to go/come
        
        # Round 40: More vocabulary from Deuteronomy, Joshua, Leviticus, Numbers
        'makna': ('mak-na', 'divorce-NMLZ'),                   # divorcement
        'mak': ('mak', 'divorce'),                             # base - divorce
        'thehthangna': ('theh-thang-na', 'throw-scatter-NMLZ'), # scattering
        'theh': ('theh', 'throw'),                             # base - throw
        'kihuhna': ('ki-huh-na', 'REFL-help-NMLZ'),             # help/safety
        'huh': ('huh', 'help'),                                # base - help
        'muhsak': ('muh-sak', 'see-CAUS'),                     # show/cause to see
        'ensim': ('en-sim', 'look-count'),                     # view/survey
        'sim': ('sim', 'count'),                               # base - count
        'khawlcip': ('khawl-cip', 'rest-tight'),               # stand still
        'khawl': ('khawl', 'rest'),                            # base - rest
        'sawmkhat': ('sawm-khat', 'ten-one'),                  # eleven/ten
        'vanvan': ('van-van', 'old-old'),                      # ancient/very old
        'van': ('van', 'old'),                                 # base - old
        'khengvalin': ('kheng-val-in', 'proud-presume-ERG'),   # presumptuously
        'kheng': ('kheng', 'proud'),                           # base - proud
        'nangzo': ('nang-zo', 'face-able'),                    # able to face
        'zo': ('zo', 'able'),                                  # base - able
        'anlom': ('an-lom', 'offering-wave'),                  # wave offering
        'lom': ('lom', 'wave'),                                # base - wave
        'hihloh': ('hi-hloh', 'be-NEG'),                       # not be
        'hloh': ('hloh', 'NEG'),                               # base - negative
        'innkuankuan': ('inn-kuan-kuan', 'house-family-REDUP'), # families
        'kuan': ('kuan', 'family'),                            # base - family
        'tuisia': ('tui-sia', 'water-evil'),                   # bitter water
        
        # Round 41: More vocabulary from Chronicles, Ezra, Nehemiah, Job, Psalms
        'bawlpha': ('bawl-pha', 'make-good'),                  # prepare/make well
        'thunuam': ('thu-nuam', 'word-pleasant'),              # good word/law
        'zahpihna': ('zah-pih-na', 'respect-APPL-NMLZ'),       # disrespect/scorn
        'mipi': ('mi-pi', 'person-great'),                     # common people
        'sawmlinih': ('sawm-li-nih', 'ten-four-two'),          # forty-two (42)
        'golna': ('gol-na', 'divide-NMLZ'),                    # treasury/division
        'gol': ('gol', 'divide'),                              # base - divide
        'simang': ('sim-ang', 'count-perish'),                 # perish/destroy
        'ang': ('ang', 'be/become'),                           # suffix - resultative
        'nuamzaw': ('nuam-zaw', 'want-more'),                  # prefer/rather
        'zaw': ('zaw', 'more'),                                # base - more
        'maimom': ('mai-mom', 'face-web'),                     # spider web
        'mom': ('mom', 'web'),                                 # base - web
        'thuakkha': ('thuak-kha', 'suffer-NEGPERF'),           # not suffer/safe
        'kha': ('kha', 'NEG.PERF'),                            # suffix - negative perfect
        'venvan': ('ven-van', 'protect-store'),                # heap up/store
        'manphatna': ('man-phat-na', 'price-worthy-NMLZ'),     # value/exchange
        'phat': ('phat', 'worthy'),                            # base - worthy
        'tehtheih': ('teh-theih', 'measure-able'),             # comparable/equal
        'khollo': ('khol-lo', 'care-NEG'),                     # forget/not care
        'cihsan': ('cih-san', 'say-rely'),                     # trust/declare trust
        'san': ('san', 'rely'),                                # base - rely
        
        # Round 42: More vocabulary from Kings, Chronicles, Psalms, Proverbs
        'satvui': ('sat-vui', 'strike-dust'),                  # smash to pieces
        'vui': ('vui', 'dust'),                                # base - dust
        'galdaihna': ('gal-daih-na', 'enemy-able-NMLZ'),       # dominion
        'daih': ('daih', 'able'),                              # base - able
        'sepkhiat': ('sep-khiat', 'work-extract'),             # execute judgment
        'sep': ('sep', 'work'),                                # base - work
        'khiat': ('khiat', 'extract'),                         # base - extract
        'theithek': ('thei-thek', 'know-extreme'),             # abundant/know well
        'thek': ('thek', 'extreme'),                           # base - extreme
        'khialhsak': ('khialh-sak', 'sin-CAUS'),               # cause to sin
        'omzaw': ('om-zaw', 'exist-more'),                     # more numerous
        'taangkona': ('taang-ko-na', 'time-long-NMLZ'),        # long period
        'taang': ('taang', 'time'),                            # base - time
        'ko': ('ko', 'long'),                                  # base - long
        'zuauna': ('zuau-na', 'lie-NMLZ'),                     # lying
        'zuau': ('zuau', 'lie'),                               # base - lie
        'sibup': ('si-bup', 'die-all'),                        # completely exhausted
        'bup': ('bup', 'all'),                                 # base - all
        'thuaklawh': ('thuak-lawh', 'suffer-PERF'),            # suffered
        'lawh': ('lawh', 'PERF'),                              # suffix - perfective
        'leengmang': ('leeng-mang', 'chariot-fly'),            # fly away
        'mang': ('mang', 'fly'),                               # base - fly
        'zawkna': ('zawk-na', 'more-NMLZ'),                    # surplus/excess
        'zawk': ('zawk', 'more'),                              # base - more
        
        # Round 43: More vocabulary from Ruth, Samuel, Kings, Chronicles, Job, Psalms, Jeremiah
        'lohbuang': ('loh-buang', 'apart-divide'),             # separation/parting
        'buang': ('buang', 'divide'),                          # base - divide
        'kizuih': ('ki-zuih', 'REFL-hang'),                    # hang oneself
        'zuih': ('zuih', 'hang'),                              # base - hang
        'kithuah': ('ki-thuah', 'REFL-gird'),                  # gird oneself
        'thuah': ('thuah', 'gird'),                            # base - gird
        'zozaw': ('zo-zaw', 'able-more'),                      # overcome/prevail
        'meiphual': ('mei-phual', 'fire-field'),               # furnace
        'phual': ('phual', 'field'),                           # base - field
        'kipakta': ('ki-pak-ta', 'REFL-wait-TA'),              # wait patiently
        'pak': ('pak', 'wait'),                                # base - wait
        'suangkang': ('suang-kang', 'stone-pillar'),           # marble pillar
        'kang': ('kang', 'pillar'),                            # base - pillar
        'suangphah': ('suang-phah', 'stone-floor'),            # pavement
        'manlah': ('man-lah', 'time-ADV'),                     # afterward/later
        'themthum': ('them-thum', 'dawn-early'),               # every moment
        'them': ('them', 'dawn'),                              # base - dawn
        'thum': ('thum', 'early'),                             # base - early
        'gakcip': ('gak-cip', 'trap-tight'),                   # snare/gin
        'gak': ('gak', 'trap'),                                # base - trap
        'cip': ('cip', 'tight'),                               # base - tight
        'kikaikhia': ('ki-kai-khia', 'REFL-dig-out'),          # uproot
        'kai': ('kai', 'dig'),                                 # base - dig
        'thangsiah': ('thang-siah', 'speak-compose'),          # conspire/encourage
        'siah': ('siah', 'compose'),                           # base - compose
        'maban': ('ma-ban', 'own-matter'),                     # concerning
        'ban': ('ban', 'matter'),                              # base - matter
        'taisim': ('tai-sim', 'check-count'),                  # investigate
        'tai': ('tai', 'check'),                               # base - check
        
        # Round 44: More vocabulary from Jeremiah, Exodus, Song of Solomon, Job, etc.
        'sunteng': ('sun-teng', 'basket-basket'),              # baskets
        'sun': ('sun', 'basket'),                              # base - basket
        'teng': ('teng', 'basket'),                            # base - basket (alt)
        'kihual': ('ki-hual', 'REFL-bind'),                    # interweave/wreathen
        'hual': ('hual', 'bind'),                              # base - bind
        'phet': ('phet', 'twin'),                              # twins
        'lawmnu': ('lawm-nu', 'friend-female'),                # bride/companion
        'seelcip': ('seel-cip', 'cover-tight'),                # conceal
        'seel': ('seel', 'cover'),                             # base - cover
        'meisuang': ('mei-suang', 'fire-stone'),               # flint/sharp stone
        'puksisak': ('puk-si-sak', 'attack-die-CAUS'),         # cause to die/kill
        'puk': ('puk', 'attack'),                              # base - attack
        'hehlua': ('heh-lua', 'angry-excessive'),              # burst in anger
        'lua': ('lua', 'excessive'),                           # base - excessive
        'kilaak': ('ki-laak', 'REFL-show'),                    # present oneself/appear
        'laak': ('laak', 'show'),                              # base - show
        'suahkhiat': ('suah-khiat', 'born-out'),               # come out/emerge
        'kigawh': ('ki-gawh', 'REFL-touch'),                   # touch/lay hand on
        'gawh': ('gawh', 'touch'),                             # base - touch
        'kisuksiat': ('ki-suk-siat', 'REFL-collapse-destroy'), # be destroyed/snared
        'suk': ('suk', 'collapse'),                            # base - collapse
        'siat': ('siat', 'destroy'),                           # base - destroy
        'tuahun': ('tuah-un', 'do-time'),                      # occurrence/controversy
        'un': ('un', 'time'),                                  # base - time
        'meidawi': ('mei-dawi', 'fire-fear'),                  # cowardly/fainthearted
        'dawi': ('dawi', 'fear'),                              # base - fear
        'huihpi': ('huih-pi', 'wind-great'),                   # strong wind
        'huih': ('huih', 'wind'),                              # base - wind
        'kiphuk': ('ki-phuk', 'REFL-overthrow'),               # be toppled/cast down
        'phuk': ('phuk', 'overthrow'),                         # base - overthrow
        
        # Round 45: More vocabulary from Genesis, Numbers, Deuteronomy, Judges, Kings, Job, Psalms
        'bengin': ('beng-in', 'hunt-ERG'),                     # hunting
        'beng': ('beng', 'hunt'),                              # base - hunt
        'haza': ('haza', 'envy'),                              # envy/jealousy
        'gega': ('gega', 'red'),                               # red
        'kihut': ('ki-hut', 'REFL-arm'),                       # arm oneself
        'hut': ('hut', 'arm'),                                 # base - arm (weapon)
        'pet': ('pet', 'sting'),                               # sting/bite/poison
        'pelem': ('pelem', 'lacking'),                         # lacking/missing
        'geivial': ('gei-vial', 'edge-knop'),                  # ornament/knop
        'gei': ('gei', 'edge'),                                # base - edge
        'vial': ('vial', 'knop'),                              # base - knop
        'mapai': ('ma-pai', 'own-go'),                         # go ahead/pass before
        'kisumit': ('ki-sum-it', 'REFL-extinguish-IT'),        # be put out
        'sum': ('sum', 'extinguish'),                          # base - extinguish
        'kisuksiatsak': ('ki-suk-siat-sak', 'REFL-collapse-destroy-CAUS'), # be destroyed
        'husia': ('husia', 'destruction'),                     # destruction
        'hetkei': ('het-kei', 'trouble-NEG'),                  # not trouble
        'het': ('het', 'trouble'),                             # base - trouble
        'kiliah': ('ki-liah', 'REFL-circuit'),                 # go round/circuit
        'liah': ('liah', 'circuit'),                           # base - circuit
        'dimletin': ('dim-let-in', 'fill-back-ERG'),           # filled plenty
        'let': ('let', 'back'),                                # base - back/return
        'kigengen': ('ki-gen-gen', 'REFL-say-REDUP'),          # be spoken
        'zen': ('zen', 'way'),                                 # way/manner
        'kineihin': ('ki-nei-hin', 'REFL-with-ERG'),           # bow down
        
        # Round 46: More vocabulary from Ezekiel, Matthew, Luke, Genesis, Exodus, Leviticus
        'hauhlawh': ('hauh-lawh', 'grasp-PERF'),               # extort
        'hauh': ('hauh', 'grasp'),                             # base - grasp
        'hot': ('hot', 'steer'),                               # pilot/steer
        'tunuam': ('tu-nuam', 'sit-pleasant'),                 # best seats
        'tu': ('tu', 'sit'),                                   # base - sit
        'bulkip': ('bul-kip', 'root-firm'),                    # foundation
        'bul': ('bul', 'root'),                                # base - root
        'kip': ('kip', 'firm'),                                # base - firm
        'khetul': ('khet-ul', 'heel-crush'),                   # bruise heel
        'khet': ('khet', 'heel'),                              # base - heel
        'ul': ('ul', 'crush'),                                 # base - crush
        'kinengniam': ('ki-neng-niam', 'REFL-oppress-humble'), # be afflicted
        'neng': ('neng', 'oppress'),                           # base - oppress
        'kilei': ('ki-lei', 'REFL-buy'),                       # be bought
        'lei': ('lei', 'buy'),                                 # base - buy
        'kisuang': ('ki-suang', 'REFL-pure'),                  # be pure/innocent
        'kibehlaplap': ('ki-behlap-lap', 'REFL-grow-REDUP'),   # grow greatly
        'behlap': ('behlap', 'grow'),                          # base - grow
        'tenkhop': ('ten-khop', 'dwell-join'),                 # settle together
        'khop': ('khop', 'join'),                              # base - join
        'ki-ip': ('ki-ip', 'REFL-hold'),                       # restrain oneself
        'ip': ('ip', 'hold'),                                  # base - hold
        'ki-ipzo': ('ki-ip-zo', 'REFL-hold-able'),             # able to restrain
        'kiciangtan': ('ki-ciang-tan', 'REFL-straight-assign'), # portion assigned
        'tan': ('tan', 'assign'),                              # base - assign
        'mawlpih': ('mawl-pih', 'dig-APPL'),                   # dig down
        'mawl': ('mawl', 'dig'),                               # base - dig
        'takun': ('takun', 'maiden'),                          # maiden/maid
        'phawkzo': ('phawk-zo', 'remember-able'),              # remember
        'phawk': ('phawk', 'remember'),                        # base - remember
        'thokang': ('tho-kang', 'rise-extend'),                # stretch out
        'denggawp': ('deng-gawp', 'strike-break'),             # smash/break
        'deng': ('deng', 'strike'),                            # base - strike
        'gawp': ('gawp', 'break'),                             # base - break
        'kot': ('kot', 'ready'),                               # equipped/ready
        'kingen': ('ki-ngen', 'REFL-request'),                 # be demanded
        'kimciang': ('kim-ciang', 'complete-straight'),        # span end to end
        'kikhaisuk': ('ki-khai-suk', 'REFL-hang-fall'),        # curtain/hanging
        'khai': ('khai', 'hang'),                              # base - hang
        'kisuzan': ('ki-su-zan', 'REFL-tear-break'),           # be destroyed
        'su': ('su', 'tear'),                                  # base - tear
        'zan': ('zan', 'break'),                               # base - break
        'kigal': ('ki-gal', 'REFL-oppose'),                    # opposite side
        'khetphim': ('khet-phim', 'heel-peg'),                 # peg/stake
        'phim': ('phim', 'peg'),                               # base - peg
        
        # Round 47: More vocabulary from Exodus, Leviticus, Numbers, Deuteronomy, Genesis
        'sui': ('sui', 'staff'),                               # staff/pole
        'bot': ('bot', 'pluck'),                               # pluck
        'meikangma': ('mei-kang-ma', 'fire-burn-mark'),        # burn mark
        'tawisuang': ('tawi-suang', 'hand-stone'),             # weights
        'kiten': ('ki-ten', 'REFL-dwell'),                     # be married
        'kima': ('ki-ma', 'REFL-alone'),                       # be alone/widowed
        'ma': ('ma', 'alone'),                                 # base - alone
        'kitah': ('ki-tah', 'REFL-separate'),                  # separate oneself
        'tah': ('tah', 'separate'),                            # base - separate
        'gupha': ('gu-pha', 'tree-branch'),                    # pole
        'gu': ('gu', 'tree'),                                  # base - tree
        'pha': ('pha', 'branch'),                              # base - branch
        'buppi': ('bup-pi', 'all-big'),                        # whole
        'kikhung': ('ki-khung', 'REFL-exit'),                  # boundary/border
        'tamasak': ('ta-ma-sak', 'cut-EMPH-CAUS'),             # forsake/abandon
        'gisuang': ('gi-suang', 'marker-stone'),               # landmark
        'gi': ('gi', 'marker'),                                # base - marker
        'khung': ('khung', 'roof'),                            # roof
        'taikeek': ('tai-keek', 'flee-ITER'),                  # flee away
        'keek': ('keek', 'ITER'),                              # suffix - iterative
        'guallelsak': ('gual-lel-sak', 'enemy-change-CAUS'),   # defeat/cause smitten
        'lel': ('lel', 'change'),                              # base - change
        
        # Round 48: More vocabulary from Judges, Samuel, Kings, Chronicles, Ezra, Job, Psalms
        'hanthot': ('han-thot', 'begin-stir'),                 # begin moving
        'thot': ('thot', 'stir'),                              # base - stir
        'thaneih': ('tha-neih', 'strength-have'),              # have strength
        'neih': ('neih', 'have'),                              # base - have
        'kihanthawnin': ('ki-han-thawn-in', 'REFL-begin-encourage-ERG'), # encourage oneself
        'thawn': ('thawn', 'encourage'),                       # base - encourage
        'suangtang': ('suang-tang', 'stone-embed'),            # sink into
        'tang': ('tang', 'embed'),                             # base - embed
        'tawngnung': ('tawng-nung', 'speak-later'),            # back area/cave
        'nung': ('nung', 'later'),                             # base - later
        'mansuah': ('man-suah', 'price-escape'),               # missing
        'suah': ('suah', 'escape'),                            # base - escape
        'lohlam': ('loh-lam', 'NEG-way'),                      # not the way
        'khezaw': ('khe-zaw', 'foot-weak'),                    # lame
        'kilawnsuk': ('ki-lawn-suk', 'REFL-throw-fall'),       # be thrown
        'lawn': ('lawn', 'throw'),                             # base - throw
        'kilokgawp': ('ki-lok-gawp', 'REFL-shake-break'),      # tremble
        'lok': ('lok', 'shake'),                               # base - shake
        'kizong': ('ki-zong', 'REFL-warm'),                    # warm oneself
        'zong': ('zong', 'warm'),                              # base - warm
        'kipiatawm': ('ki-piat-awm', 'REFL-sell-self'),        # sell oneself
        'piat': ('piat', 'sell'),                              # base - sell
        'awm': ('awm', 'self'),                                # base - self
        'kilawmzaw': ('ki-lawm-zaw', 'REFL-worthy-more'),      # more fitting
        'zeizai': ('zei-zai', 'what-thing'),                   # everything
        'zai': ('zai', 'thing'),                               # base - thing
        'puksuk': ('puk-suk', 'fall-down'),                    # sink down
        'zun': ('zun', 'urine'),                               # urine
        'kizat': ('ki-zat', 'REFL-use'),                       # be used
        'zat': ('zat', 'use'),                                 # base - use
        'golhguk': ('golh-guk', 'oppose-dig'),                 # undermine/frustrate
        'golh': ('golh', 'oppose'),                            # base - oppose
        'guk': ('guk', 'dig'),                                 # base - dig
        'kihisakin': ('ki-hi-sak-in', 'REFL-be-CAUS-ERG'),     # act proudly
        'kiphawkkha': ('ki-phawk-kha', 'REFL-remember-NEG'),   # be forgotten
        'phuan': ('phuan', 'refuge'),                          # refuge
        'kithuhilh': ('ki-thu-hilh', 'REFL-word-tell'),        # be reproved
        'hilh': ('hilh', 'tell'),                              # base - tell
        'sekpi': ('sek-pi', 'hammer-big'),                     # axe/hammer
        'sek': ('sek', 'hammer'),                              # base - hammer
        'huihnung': ('huih-nung', 'wind-continue'),            # passing wind
        'thaksuak': ('thak-suak', 'new-wither'),               # fresh then wither
        'thak': ('thak', 'new'),                               # base - new
        'suak': ('suak', 'wither'),                            # base - wither
        'bekun': ('bek-un', 'only-time'),                      # at last
        'bek': ('bek', 'only'),                                # base - only
        
        # Round 49: More vocabulary from Deuteronomy, Joshua, Judges, Proverbs, Ecclesiastes, etc.
        'zunglot': ('zung-lot', 'root-pull'),                  # uproot
        'lot': ('lot', 'pull'),                                # base - pull
        'lazo': ('la-zo', 'take-able'),                        # able to take
        'meilah': ('mei-lah', 'fire-lamp'),                    # lamp
        'lah': ('lah', 'lamp'),                                # base - lamp
        'tup': ('tup', 'roast'),                               # roast
        'piciang': ('pi-ciang', 'great-straight'),             # various/diverse
        'kiphattawm': ('ki-phat-tawm', 'REFL-praise-by'),      # be praised
        'tawm': ('tawm', 'by'),                                # base - by/with
        'kiheek': ('ki-heek', 'REFL-oppose'),                  # resist/withstand
        'heek': ('heek', 'oppose'),                            # base - oppose
        'suangngo': ('suang-ngo', 'stone-socket'),             # socket/base
        'ngo': ('ngo', 'socket'),                              # base - socket
        'bupun': ('bup-un', 'all-time'),                       # cluster
        'gahpha': ('gah-pha', 'branch-good'),                  # flourishing
        'gah': ('gah', 'branch'),                              # base - branch
        'kikai': ('ki-kai', 'REFL-lead'),                      # be led away/captive
        'kilkel': ('ki-lkel', 'REFL-leave'),                   # be forsaken
        'lkel': ('lkel', 'leave'),                             # base - leave
        'gip': ('gip', 'seal'),                                # seal
        'lipkhap': ('lip-khap', 'freedom-loose'),              # liberty
        'lip': ('lip', 'freedom'),                             # base - freedom
        'khap': ('khap', 'loose'),                             # base - loose
        
        # Round 50: More vocabulary from Acts, Corinthians, Genesis, Exodus
        'kithutuak': ('ki-thu-tuak', 'REFL-word-receive'),     # believe
        'tuak': ('tuak', 'receive'),                           # base - receive
        'kimuthei': ('ki-mu-thei', 'REFL-see-able'),           # be visible
        'meiilum': ('mei-ilum', 'fire-mist'),                  # vapor/mist
        'ilum': ('ilum', 'mist'),                              # base - mist
        'kithukkik': ('ki-thuk-kik', 'REFL-revenge-ITER'),     # be avenged
        'thuk': ('thuk', 'revenge'),                           # base - revenge
        'kisunin': ('ki-sun-in', 'REFL-resemble-ERG'),         # in likeness
        'kisiagawp': ('ki-sia-gawp', 'REFL-bad-break'),        # be corrupted
        'kultal': ('kul-tal', 'tar-coat'),                     # pitch/tar
        'kul': ('kul', 'tar'),                                 # base - tar
        'tal': ('tal', 'coat'),                                # base - coat
        'kiphiatkhia': ('ki-phiat-khia', 'REFL-destroy-out'),  # be destroyed
        'guaktang': ('guak-tang', 'back-toward'),              # backward
        'guak': ('guak', 'back'),                              # base - back
        'kizelthang': ('ki-zel-thang', 'REFL-scatter-spread'), # be spread abroad
        'zel': ('zel', 'scatter'),                             # base - scatter
        'kilui': ('ki-lui', 'REFL-tell'),                      # be told
        'lui': ('lui', 'tell'),                                # base - tell
        'kigu': ('ki-gu', 'REFL-tear'),                        # be torn
        'lapi': ('la-pi', 'take-big'),                         # female animal
        'thagui': ('tha-gui', 'strength-cord'),                # sinew
        'gui': ('gui', 'cord'),                                # base - cord
        'moman': ('mo-man', 'bride-price'),                    # dowry
        'mo': ('mo', 'bride'),                                 # base - bride
        'mangman': ('mang-man', 'dream-person'),               # dreamer
        'teekpa': ('teek-pa', 'in.law-father'),                # father-in-law
        'teek': ('teek', 'in.law'),                            # base - in-law
        'huanpipa': ('huan-pi-pa', 'bread-great-man'),         # chief baker
        'huan': ('huan', 'bread'),                             # base - bread
        'gawng': ('gawng', 'lean'),                            # lean/ill-favoured
        'buhvui': ('buh-vui', 'rice-dust'),                    # grain
        'khitlam': ('khit-lam', 'finish-way'),                 # appearance
        'oksak': ('ok-sak', 'clothe-CAUS'),                    # cause to wear
        'ok': ('ok', 'clothe'),                                # base - clothe
        'tumpihin': ('tum-pih-in', 'set-APPL-ERG'),            # set before
        'gawl': ('gawl', 'neck'),                              # neck
        'sul': ('sul', 'snake'),                               # snake/serpent
        'hankuang': ('han-kuang', 'carry-box'),                # coffin
        'haksapi': ('hak-sa-pi', 'heavy-flesh-great'),         # hard labor
        
        # Round 51: More vocabulary from Jeremiah, Daniel, Hosea, Matthew, Luke, John, Acts, Exodus
        'kiphal': ('ki-phal', 'REFL-shut'),                    # be shut up
        'phal': ('phal', 'shut'),                              # base - shut
        'dozo': ('do-zo', 'throw-able'),                       # able to cast
        'do': ('do', 'throw'),                                 # base - throw
        'lawptakin': ('lawp-tak-in', 'shake-truly-ERG'),       # trembling
        'lawp': ('lawp', 'shake'),                             # base - shake
        'tak': ('tak', 'truly'),                               # base - truly
        'lonei': ('lo-nei', 'NEG-have'),                       # tares/without
        'kimtakin': ('kim-tak-in', 'complete-truly-ERG'),      # thoroughly
        'tuukulh': ('tuu-kulh', 'climb-steal'),                # sneak up/climb
        'tuu': ('tuu', 'climb'),                               # base - climb
        'kulh': ('kulh', 'steal'),                             # base - steal
        'tunma-in': ('tun-ma-in', 'arrive-EMPH-ERG'),          # before
        'holhthawh': ('holh-thawh', 'stir-up'),                # incite/stir up
        'holh': ('holh', 'stir'),                              # base - stir
        'kithawisa-in': ('ki-thawi-sa-in', 'REFL-ready-already-ERG'), # harnessed
        'thawi': ('thawi', 'ready'),                           # base - ready
        'lopipi-in': ('lo-pi-pi-in', 'NEG-great-great-ERG'),   # powerfully
        
        # Round 52: Massive batch from Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, Samuel
        'khuituah': ('khui-tuah', 'fold-do'),                  # double/fold together
        'khui': ('khui', 'fold'),                              # base - fold
        'kuak': ('kuak', 'hollow'),                            # hollow
        'guat': ('guat', 'work'),                              # work/craft
        'liimsun': ('liim-sun', 'wing-spread'),                # spread wings
        'liim': ('liim', 'wing'),                              # base - wing
        'kizen': ('ki-zen', 'REFL-thin'),                      # flatten
        'kihuan': ('ki-huan', 'REFL-fry'),                     # be fried
        'kilah': ('ki-lah', 'REFL-spread'),                    # spread
        'talkolh': ('tal-kolh', 'bald-head'),                  # bald forehead
        'kolh': ('kolh', 'head'),                              # base - head
        'kikhakcip': ('ki-khak-cip', 'REFL-lock-tight'),       # be locked
        'khak': ('khak', 'lock'),                              # base - lock
        'zuthawl': ('zu-thawl', 'slave-female'),               # female slave
        'ki-apsa': ('ki-ap-sa', 'REFL-devote-already'),        # devoted
        'ap': ('ap', 'devote'),                                # base - devote
        'teep': ('teep', 'fringe'),                            # fringe
        'kipumsil': ('ki-pum-sil', 'REFL-body-wash'),          # bathe
        'pum': ('pum', 'body'),                                # base - body
        'sil': ('sil', 'wash'),                                # base - wash
        'phul': ('phul', 'spring'),                            # spring (water)
        'thoto': ('tho-to', 'rise-UP'),                        # arise
        'to': ('to', 'up'),                                    # base - up
        'huihlaka': ('huih-laka', 'wind-among'),               # in the air
        'laka': ('laka', 'among'),                             # base - among
        'thahatzaw': ('tha-hat-zaw', 'strength-have-more'),    # mightier
        'hat': ('hat', 'have'),                                # base - have
        'momai': ('mo-mai', 'dry-without'),                    # drought
        'gawizan': ('gawi-zan', 'stamp-break'),                # crush/grind
        'gawi': ('gawi', 'stamp'),                             # base - stamp
        'heitang': ('hei-tang', 'path-divide'),                # prepare route
        'hei': ('hei', 'path'),                                # base - path
        'phiatkhiat': ('phiat-khiat', 'destroy-out'),          # blot out
        'sungnu': ('sung-nu', 'inside-female'),                # mother-in-law
        'sung': ('sung', 'inside'),                            # base - inside
        'kisugawp': ('ki-su-gawp', 'REFL-crush-break'),        # oppressed
        'lahkhiat': ('lah-khiat', 'reveal-out'),               # reveal
        'lamkal': ('lam-kal', 'way-middle'),                   # on the way
        'kal': ('kal', 'middle'),                              # base - middle
        'lengkhia-in': ('leng-khia-in', 'line-out-ERG'),       # draw out
        'leng': ('leng', 'line'),                              # base - line
        'kuansuk': ('kuan-suk', 'attack-fall'),                # slay
        'kihu': ('ki-hu', 'REFL-help'),                        # plead
        'hu': ('hu', 'help'),                                  # base - help
        'kisatgawp': ('ki-sat-gawp', 'REFL-strike-break'),     # set against
        'sat': ('sat', 'strike'),                              # base - strike
        'kuikek': ('kui-kek', 'tear-scratch'),                 # tear
        'kui': ('kui', 'tear'),                                # base - tear
        'kek': ('kek', 'scratch'),                             # base - scratch
        'domto-in': ('dom-to-in', 'go-UP-ERG'),                # going up
        'dom': ('dom', 'go'),                                  # base - go
        'kilehhei': ('ki-leh-hei', 'REFL-return-wonder'),      # be amazed
        'liimnuai': ('liim-nuai', 'wing-under'),               # under wings
        'nuai': ('nuai', 'under'),                             # base - under
        'haih': ('haih', 'winnow'),                            # winnow
        'galphual': ('gal-phual', 'enemy-field'),              # battlefield
        'tumsiam': ('tum-siam', 'play-skilled'),               # skilled player
        
        # Round 53: Another massive batch from Samuel, Kings, Chronicles, Ezra, Job, Psalms, Proverbs
        'kinawhin': ('ki-nawh-in', 'REFL-meet-ERG'),           # meet/come to meet
        'nawh': ('nawh', 'meet'),                              # base - meet
        'gimlua': ('gim-lua', 'faint-excessive'),              # exhausted
        'gim': ('gim', 'faint'),                               # base - faint
        'kikekin': ('ki-kek-in', 'REFL-scratch-ERG'),          # rent/torn
        'kilok': ('ki-lok', 'REFL-shake'),                     # cast away
        'kheging': ('khe-ging', 'foot-sound'),                 # sound of going
        'ging': ('ging', 'sound'),                             # base - sound
        'gel': ('gel', 'together'),                            # together
        'kizal': ('ki-zal', 'REFL-stretch'),                   # stretch forth
        'kipsuak': ('ki-psuak', 'REFL-take'),                  # take by war
        'psuak': ('psuak', 'take'),                            # base - take
        'dimlet': ('dim-let', 'fill-back'),                    # overflow
        'guallelin': ('gual-lel-in', 'enemy-change-ERG'),      # defeat
        'diam': ('diam', 'month'),                             # month
        'kisingkhia': ('ki-sing-khia', 'REFL-shake-out'),      # be shaken out
        'sing': ('sing', 'shake'),                             # base - shake
        'tawldam': ('tawl-dam', 'free-good'),                  # rest/deliver
        'tawl': ('tawl', 'free'),                              # base - free
        'dam': ('dam', 'good'),                                # base - good
        'lampai': ('lam-pai', 'way-go'),                       # journey
        'mancip': ('man-cip', 'time-tight'),                   # seize
        'sucip': ('su-cip', 'crush-tight'),                    # cut off
        'phiatkhiatsak': ('phiat-khiat-sak', 'destroy-out-CAUS'), # seal up
        'ngingei': ('ngin-gei', 'weary-edge'),                 # make desolate
        'ngin': ('ngin', 'weary'),                             # base - weary
        'puklawh': ('puk-lawh', 'fall-PERF'),                  # cast down
        'pumtangin': ('pum-tang-in', 'body-on-ERG'),           # upon body
        'kithun': ('ki-thun', 'REFL-press'),                   # burst
        'thun': ('thun', 'press'),                             # base - press
        'peekpi': ('peek-pi', 'spread-big'),                   # spread out
        'peek': ('peek', 'spread'),                            # base - spread
        'mei-ek': ('mei-ek', 'fire-sneeze'),                   # neesings/light
        'ek': ('ek', 'sneeze'),                                # base - sneeze
        'vutlevai': ('vut-levai', 'dust-spread'),              # dust and ashes
        'levai': ('levai', 'spread'),                          # base - spread
        'kipaaksak': ('ki-paak-sak', 'REFL-glad-CAUS'),        # make glad
        'paak': ('paak', 'glad'),                              # base - glad
        'kituancil': ('ki-tuan-cil', 'REFL-cut-piece'),        # cut in pieces
        'tuan': ('tuan', 'cut'),                               # base - cut
        'cil': ('cil', 'piece'),                               # base - piece
        'themkha': ('them-kha', 'dawn-NEG'),                   # would not
        'domto': ('dom-to', 'go-UP'),                          # reproach
        'taksing': ('tak-sing', 'truly-shake'),                # fir trees
        'kibulhin': ('ki-bul-hin', 'REFL-root-sit'),           # sit in darkness
        'telzaw': ('tel-zaw', 'know-more'),                    # more understanding
        'tel': ('tel', 'know'),                                # base - know
        'kisui': ('ki-sui', 'REFL-polish'),                    # polished
        'pukkha': ('puk-kha', 'fall-NEG'),                     # not stumble
        'mapekin': ('ma-pek-in', 'EMPH-settle-ERG'),           # settled
        
        # Round 54: More vocabulary from Exodus, Samuel, Kings, Romans, Proverbs
        'kikhinin': ('ki-khin-in', 'REFL-behind-ERG'),         # move behind
        'khin': ('khin', 'behind'),                            # base - behind
        'haknaw': ('hak-naw', 'heavy-lead'),                   # sink like lead
        'naw': ('naw', 'lead'),                                # base - lead (metal)
        'lawnkhak': ('lawn-khak', 'throw-lock'),               # set bounds
        'seelsim': ('seel-sim', 'cover-count'),                # uncover/steps
        'phih': ('phih', 'bowl'),                              # bowl/cover
        'tuucin': ('tuucin', 'shepherd'),                      # shepherd (lexicalized)
        'tuucing': ('tuucing', 'shepherd'),                    # shepherd variant
        'cin': ('cin', 'tend'),                                # tend (flocks)
        'pelhthei': ('pelh-thei', 'escape-able'),              # able to escape
        'pelh': ('pelh', 'escape'),                            # base - escape
        'kikup': ('ki-kup', 'REFL-hide'),                      # hide oneself
        'kup': ('kup', 'hide'),                                # base - hide
        'kinamin': ('ki-nam-in', 'REFL-kiss-ERG'),             # kiss/salute
        'nam': ('nam', 'kiss'),                                # base - kiss
        'taangkhiasak': ('taang-khia-sak', 'time-out-CAUS'),   # put forth
        'leikang': ('lei-kang', 'earth-burn'),                 # burn in field
        'mawhmaisak': ('mawh-mai-sak', 'sin-face-CAUS'),       # mock
        'mawh': ('mawh', 'sin'),                               # base - sin
        'gina-in': ('gin-a-in', 'firm-3SG-ERG'),               # wise
        'gin': ('gin', 'firm'),                                # base - firm
        'kitheikim': ('ki-thei-kim', 'REFL-know-complete'),    # be well known
        
        # Round 55: Final push from Ecclesiastes, Isaiah, Jeremiah, Ezekiel, Daniel, Joel, Matthew, Mark, etc.
        'phop': ('phop', 'sew'),                               # sew
        'piikpeek': ('piik-peek', 'gather-spread'),            # gathered/eaten
        'piik': ('piik', 'gather'),                            # base - gather
        'leltak': ('lel-tak', 'change-truly'),                 # truly full
        'ngun-ek': ('ngun-ek', 'silver-dross'),                # dross
        'kihanthawn': ('ki-han-thawn', 'REFL-begin-encourage'), # be stirred/moved
        'kiphiat': ('ki-phiat', 'REFL-destroy'),               # be disannulled
        'thonginn': ('thong-inn', 'prison-house'),             # prison house
        'thong': ('thong', 'prison'),                          # base - prison
        'kinawtngil': ('ki-nawt-ngil', 'REFL-smooth-arrow'),   # polished shaft
        'nawt': ('nawt', 'smooth'),                            # base - smooth
        'ngil': ('ngil', 'arrow'),                             # base - arrow
        'kizep': ('ki-zep', 'REFL-clothe'),                    # be clothed
        'zep': ('zep', 'clothe'),                              # base - clothe
        'tuacih': ('tua-cih', 'that-say'),                     # circumcise
        'leihoih': ('lei-hoih', 'earth-good'),                 # fruitful place
        'hoih': ('hoih', 'good'),                              # base - good
        'taanlawh': ('taan-lawh', 'withhold-PERF'),            # withhold
        'taan': ('taan', 'withhold'),                          # base - withhold
        'kullo': ('kul-lo', 'hope-NEG'),                       # no hope
        'kisuah': ('ki-suah', 'REFL-escape'),                  # go like serpent
        'pempam': ('pem-pam', 'fire-fold'),                    # infolding fire
        'pem': ('pem', 'fire'),                                # base - fire (alt)
        'pam': ('pam', 'fold'),                                # base - fold
        'maangmu': ('maang-mu', 'vision-see'),                 # seen nothing
        'maang': ('maang', 'vision'),                          # base - vision
        'tuahsiat': ('tuah-siat', 'do-destroy'),               # bring to remembrance
        'lohteng': ('loh-teng', 'NEG-remain'),                 # residue/small thing
        'phazaw': ('pha-zaw', 'good-more'),                    # better/do better
        'deuhin': ('deuh-in', 'clothed-ERG'),                  # clothed in linen
        'deuh': ('deuh', 'clothed'),                           # base - clothed
        'leipi': ('lei-pi', 'earth-great'),                    # earth quake
        'tunsaknop': ('tun-sak-nop', 'arrive-CAUS-want'),      # let peace come
        'nop': ('nop', 'want'),                                # base - want
        'kitawphah': ('ki-taw-phah', 'REFL-receive-place'),    # receive seed
        'kikhamval': ('ki-kham-val', 'REFL-gather-basket'),    # took up baskets
        'kham': ('kham', 'gather'),                            # base - gather
        'val': ('val', 'basket'),                              # base - basket
        'mannop': ('man-nop', 'price-want'),                   # willing/hear
        'thongkiat': ('thong-kiat', 'prison-extract'),         # came unto prison
        'kitheithang': ('ki-thei-thang', 'REFL-know-spread'),  # blaze abroad
        'mapaisak': ('ma-pai-sak', 'EMPH-go-CAUS'),            # constrained to go
        'tamveipi': ('tam-vei-pi', 'many-time-great'),         # ofttimes
        'vei': ('vei', 'time'),                                # base - time
        'thahkhit': ('thah-khit', 'kill-finish'),              # kill body
        'thongcing': ('thong-cing', 'prison-throw'),           # cast into prison
        'cing': ('cing', 'throw'),                             # base - throw
        'dongtangsak': ('dong-tang-sak', 'stumble-on-CAUS'),   # put stumblingblock
        'dong': ('dong', 'stumble'),                           # base - stumble
        'kilehngatin': ('ki-leh-ngat-in', 'REFL-return-time-ERG'), # say again
        'ngat': ('ngat', 'time'),                              # base - time
        'zokhin': ('zok-hin', 'finish-sit'),                   # finished course
        'zok': ('zok', 'finish'),                              # base - finish
        
        # Round 56: Final push - Genesis, Exodus vocabulary
        'eimah': ('ei-mah', '1PL.EXCL-EMPH'),                  # us/our (emphatic)
        'ei': ('ei', '1PL.EXCL'),                              # 1st person plural exclusive
        'petpetin': ('pet-pet-in', 'bone-bone-ERG'),           # bone of bones
        'hup': ('hup', 'mouth'),                               # mouth
        'kisamsiat': ('ki-sam-siat', 'REFL-open-destroy'),     # opened (mouth)
        'sam': ('sam', 'open'),                                # base - open
        'kithuk': ('ki-thuk', 'REFL-revenge'),                 # vengeance taken
        'tuzawh': ('tu-zawh', 'sit-able'),                     # possible/hard
        'zawh': ('zawh', 'able'),                              # base - able
        'tuununo': ('tuu-nu-no', 'ewe-female-small'),          # ewe lamb
        'makeng': ('ma-keng', 'EMPH-tree'),                    # grove/tree
        'keng': ('keng', 'tree'),                              # base - tree
        'temta': ('tem-ta', 'fire-hold'),                      # fire in hand
        'tem': ('tem', 'fire'),                                # base - fire (alt)
        'butsak': ('but-sak', 'face-CAUS'),                    # put upon face
        'but': ('but', 'face'),                                # base - face (alt)
        'kihehnem': ('ki-heh-nem', 'REFL-angry-comfort'),      # comfort oneself
        'nem': ('nem', 'comfort'),                             # base - comfort
        'galmat': ('gal-mat', 'enemy-steal'),                  # stolen away
        'mat': ('mat', 'steal'),                               # base - steal
        'khelkom': ('khel-kom', 'hollow-touch'),               # touched hollow
        'kom': ('kom', 'touch'),                               # base - touch
        'khel': ('khel', 'hollow'),                            # hollow (of thigh)
        'dawksak': ('dawk-sak', 'bind-CAUS'),                  # bound upon
        'dawk': ('dawk', 'bind'),                              # base - bind
        'pipa': ('pi-pa', 'great-man'),                        # chief/officer
        'phai': ('phai', 'meadow'),                            # meadow
        'kikhailum': ('ki-khai-lum', 'REFL-hang-round'),       # restored/hanged
        'lum': ('lum', 'round'),                               # base - round
        'gaih': ('gaih', 'little'),                            # little
        'kipulak': ('ki-pul-ak', 'REFL-expose-COMPL'),         # made known
        'ak': ('ak', 'COMPL'),                                 # completive
        'gulgu': ('gul-gu', 'coil-bite'),                      # adder/serpent
        'phazaw-in': ('pha-zaw-in', 'good-more-ERG'),          # more/multiplied
        'kilangzo': ('ki-lang-zo', 'REFL-clear-able'),         # hearken
        'lang': ('lang', 'clear'),                             # base - clear
        'vik': ('vik', 'rod'),                                 # rod
        'lomkhat': ('lom-khat', 'bundle-one'),                 # bunch (of hyssop)
        'phialgawp': ('phial-gawp', 'morning-watch'),          # morning watch
        'phial': ('phial', 'morning'),                         # base - morning
        'vukkhal': ('vuk-khal', 'frost-dew'),                  # hoar frost
        'vuk': ('vuk', 'frost'),                               # base - frost
        'khal': ('khal', 'dew'),                               # base - dew
        
        # Round 57: Final few to reach 98%
        'beka': ('beka', 'bekah'),                             # bekah (half shekel)
        'daii': ('daii', 'pan'),                               # pan/frying pan
        'dunga': ('dung-a', 'border-LOC'),                     # at border/utmost coast
        'phuala': ('phual-a', 'field-LOC'),                    # in the field/strove
        'beryl': ('beryl', 'beryl'),                           # beryl (gemstone - loanword)
        
        # Round 58: More partials to push over 98%
        'palh': ('palh', 'palm'),                              # palm tree
        'khangkhia': ('khang-khia', 'generation-out'),         # branch/grow out
        'phattheih': ('phat-theih', 'praise-able'),            # praiseworthy
        'mimawh': ('mi-mawh', 'person-sin'),                   # innocent/sinner
        'sumlei': ('sum-lei', 'money-buy'),                    # buyer/seller
        'pauthei': ('pau-thei', 'speak-able'),                 # able to speak
        'pau': ('pau', 'speak'),                               # base - speak
        'simun': ('sim-un', 'count-time'),                     # without ceasing
        'muthei': ('mu-thei', 'see-able'),                     # able to see
        'mu': ('mu', 'see'),                                   # base - see
        'uploh': ('up-loh', 'look-NEG'),                       # not looking/unaware
        'up': ('up', 'look'),                                  # base - look
        
        # Round 59: Final push past 98%
        'leteh': ('let-eh', 'return-EXCL'),                    # it is good/bear
        'ninthem': ('nin-them', 'day-dawn'),                   # mote/early morning
        'bawlbawl': ('bawl-bawl', 'make-REDUP'),               # continually
        
        # Round 60: Pushing toward 98.5%
        'kiimnai': ('ki-im-nai', 'REFL-neighbor-close'),       # neighboring, all around
        'tunma': ('tun-ma', 'arrive-before'),                  # meanwhile, in the meantime
        'lopipi': ('lo-pipi', 'NEG-really'),                   # unwillingly / with force (ut lopipi = strong hand)
        "huihpi'": ('huih-pi', 'wind-great'),                  # strong wind, east wind
        'huihpi': ('huih-pi', 'wind-great'),                   # strong wind (no apostrophe)
        'kiphelkhamin': ('ki-phel-kham-in', 'REFL-split-break-ERG'),  # was rent/split
        'peka': ('pek-a', 'edge-LOC'),                         # uttermost parts, edge
        'kisukha': ('ki-suk-ha', 'REFL-pollute-CAUS'),         # defiled, made unclean
        "buppi'": ('bup-pi', 'all-great'),                     # entire, whole
        'buppi': ('bup-pi', 'all-great'),                      # entire, whole (no apostrophe)
        "kiguan'": ('ki-guan', 'REFL-deliver'),                # delivered, handed over
        'kiguan': ('ki-guan', 'REFL-deliver'),                 # delivered (no apostrophe)
        'suntangpi': ('sun-tang-pi', 'sun-before-great'),      # before the sun, publicly
        'phukha': ('phu-kha', 'emerge-go'),                    # seeth, sees, views
        'gimpi': ('gim-pi', 'labor-great'),                    # sorrow, toil, great labor
        'dahlua': ('dah-lua', 'weep-exceed'),                  # great sorrow, grief
        "pi'": ('pi', 'great'),                                # great (with apostrophe)
        'uhcin': ('uh-cin', 'PL-COND'),                        # conditional plural marker
        'le-uhcin': ('le-uh-cin', 'and-PL-COND'),              # lest (conditional warning)
        'leuhcin': ('le-uh-cin', 'and-PL-COND'),               # lest (without hyphen)
        
        # Round 61: Fixing partial analyses
        'baihsa': ('baih-sa', 'prepare-CAUS'),                 # be ready, prepared
        'khenuai': ('khe-nuai', 'foot-beneath'),               # sole of foot, from foot
        'khemsa': ('khem-sa', 'restrain-CAUS'),                # deceive, mislead
        'dingkhia': ('ding-khia', 'stand-out'),                # depart, go forth
        'kohna': ('koh-na', 'thank-NMLZ'),                     # thanksgiving
        'sangpi': ('sang-pi', 'high-great'),                   # high (walls)
        'siahna': ('siah-na', 'snare-NMLZ'),                   # snare, trap
        'kihamsiatna': ('ki-hamsiat-na', 'REFL-reproach-NMLZ'), # reproach, disgrace
        'sutkhia': ('sut-khia', 'break-out'),                  # break off, remove
        'atkhia': ('at-khia', 'cut-out'),                      # cut off
        'nawhsa': ('nawh-sa', 'hurry-CAUS'),                   # in haste, hurriedly
        'khaguh': ('kha-guh', 'jaw-bone'),                     # jawbone
        'zaza': ('za-za', 'hundred-hundred'),                  # hundreds
        'zonna': ('zon-na', 'seek-NMLZ'),                      # seeking, searching
        'siasa': ('sia-sa', 'waste-CAUS'),                     # lay waste, destroy
        'nui': ('nui', 'laugh'),                               # laugh
        'ipzo': ('ip-zo', 'restrain-COMPL'),                   # withhold, restrain
        'balkhia': ('bal-khia', 'tear-out'),                   # rend out, tear off
        'ansal': ('an-sal', 'grain-store'),                    # storehouse
        'phongto': ('phong-to', 'reveal-DIR'),                 # raise up, lift
        'kitheihna': ('ki-theih-na', 'REFL-know-NMLZ'),        # pledge, token (of knowing)
        'lunggulhna': ('lung-gulh-na', 'heart-long-NMLZ'),     # longing, desire
        'khengakna': ('khen-gak-na', 'divide-step-NMLZ'),      # footstool, steps
        'hawmkhia': ('hawm-khia', 'join-out'),                 # give portions, distribute
        'khuaphia': ('khua-phia', 'cloud-bright'),             # brightness, thick clouds
        'lusu': ('lu-su', 'head-shake'),                       # shake head
        'vuina': ('vui-na', 'bury-NMLZ'),                      # burial
        'deda': ('de-da', 'love-INTNS'),                       # enlarge, widen (covenant)
        'deidan': ('dei-dan', 'say-manner'),                   # according as, how one says
        'atsak': ('at-sak', 'cut-CAUS'),                       # circumcise
        'tuitawi': ('tui-tawi', 'water-draw'),                 # draw water
        
        # Round 62: More unknowns
        'thozo': ('tho-zo', 'arise-COMPL'),                    # walk abroad, recover
        'tawmzaw': ('tawm-zaw', 'little-COMP'),                # less
        'kigalsai': ('ki-gal-sai', 'REFL-opposite-face'),      # opposite, over against
        'kitanh': ('ki-tanh', 'REFL-estimate'),                # be valued, estimated
        'op': ('op', 'egg'),                                   # egg(s)
        'lompi': ('lom-pi', 'gate-great'),                     # great gate, entrance
        'khungin': ('khung-in', 'beam-ERG'),                   # with beams
        'lampha': ('lam-pha', 'path-good'),                    # restore, rebuild
        'zumhuaipi': ('zum-huai-pi', 'filth-bad-great'),       # unclean, polluted
        'beba': ('be-ba', 'open-wide'),                        # gape, open wide mouth
        'gingpha': ('ging-pha', 'skill-good'),                 # skilfully
        'deudau': ('deu-dau', 'gather-together'),              # together
        'kitawito': ('ki-tawi-to', 'REFL-lift-DIR'),           # towering, high/lifted
        'khuisa': ('khui-sa', 'breath-emit'),                  # sigh
        'thai': ('thai', 'embrace'),                           # embrace, search
        'guaktanga': ('guak-tang-a', 'bare-body-LOC'),         # naked (in nakedness)
        'kitukalhsak': ('ki-tukalh-sak', 'REFL-confuse-CAUS'), # confound, mix up
        'thongmial': ('thong-mial', 'prison-dark'),            # dungeon
        'eh!': ('eh', 'EXCL'),                                 # exclamation
        "han'": ('han', 'yet'),                                # yet (with apostrophe)
        "masa'": ('masa', 'first'),                            # first (with apostrophe)
        
        # Round 63: Fixing partial analyses
        'awi': ('awi', 'warm'),                                # warm (at fire)
        'iik': ('iik', 'breast'),                              # breast (wave offering)
        'sawnsawn': ('sawn-sawn', 'talk-REDUP'),               # talk continuously, persecute
        'kawikawina': ('kawi-kawi-na', 'wander-REDUP-NMLZ'),   # wandering
        'ciahto': ('ciah-to', 'return-DIR'),                   # go up, hasten back
        'zaam': ('zaam', 'run.over'),                          # run over (branches)
        'buhcilna': ('buh-cil-na', 'grain-thresh-NMLZ'),       # threshing floor
        'nawtin': ('nawt-in', 'forward-ERG'),                  # forward, onward
        'nawmvalh': ('nawm-valh', 'soft-swallow'),             # swallow up
        'kahtoh': ('kah-toh', 'step-ascend'),                  # go up by steps
        'nilhsak': ('nilh-sak', 'put.on-CAUS'),                # put upon, compound
        'mongte': ('mong-te', 'end-PL'),                       # ends, edges
        'khatpeuhah': ('khat-peuh-ah', 'one-any-LOC'),         # in any place
        'thukzaw': ('thuk-zaw', 'deep-COMP'),                  # lower, deeper
        'kamsiatna': ('kam-siat-na', 'word-bad-NMLZ'),         # trouble, travail
        'kansim': ('kan-sim', 'spy-out'),                      # spy out, search
        'kawcik': ('kaw-cik', 'hollow-narrow'),                # narrow place
        'kamciam': ('kam-ciam', 'word-promise'),               # vow, bond
        'ahihlohna': ('a-hi-loh-na', '3SG-be-NEG-NMLZ'),       # not being, absence
        'lehdona': ('leh-do-na', 'turn-against-NMLZ'),         # trespass, rebellion
        'mainawt': ('mai-nawt', 'face-forward'),               # rush forward
        'hilhsak': ('hilh-sak', 'teach-CAUS'),                 # cause to teach, instruct
        'khumzaw': ('khum-zaw', 'sweet-COMP'),                 # sweeter
        'khuapisung': ('khuapi-sung', 'city-inside'),          # inside the city
        'sangkil': ('sang-kil', 'step-threshold'),             # threshold, step
        
        # Round 64: More partial analyses
        "pawlkhatte'": ('pawl-khatte', 'group-fifty'),         # fifty (with apostrophe)
        'pawlkhatte': ('pawl-khatte', 'group-fifty'),          # fifty
        'cici': ('ci-ci', 'say-REDUP'),                        # entreat, beg repeatedly
        'ansang': ('an-sang', 'grain-gather'),                 # reap, glean
        'mitsuan': ('mit-suan', 'eye-direct'),                 # watch, keep eyes on
        'khamval': ('kham-val', 'forbid-remain'),              # remain, be left over
        'satkhia': ('sat-khia', 'strike-out'),                 # beat out
        'kibawlsia': ('ki-bawl-sia', 'REFL-make-bad'),         # be harmed, be met with trouble
        'thungenin': ('thu-ngen-in', 'word-request-ERG'),      # praying (instrumental)
        'innkhumzangah': ('inn-khum-zang-ah', 'house-roof-top-LOC'), # on the rooftop
        'lokhawhna': ('lo-khawh-na', 'field-work-NMLZ'),       # plowing, farming
        'omkim': ('om-kim', 'exist-complete'),                 # all present, complete
        'sawmin': ('sawm-in', 'ten.thousand-ERG'),             # ten thousand (as agent)
        'nawhtai': ('nawh-tai', 'hurry-flee'),                 # hurry, make haste
        'leenggahkeu': ('leeng-gah-keu', 'grape-dry-cluster'), # raisins
        'theikhol': ('thei-khol', 'know-certain'),             # know for sure
        'cinat': ('ci-nat', 'become-sick'),                    # sickness
        'cinatna': ('ci-nat-na', 'become-sick-NMLZ'),          # sickness (nominalized)
        'veh': ('veh', 'see'),                                 # see, visit
        'tomkha': ('tom-kha', 'cover-go'),                     # covered
        'langtuakah': ('lang-tuak-ah', 'side-each-LOC'),       # on each side
        'khuakulh': ('khua-kulh', 'town-wall'),                # city wall
        'ziazua': ('zia-zua', 'clear-?'),                      # clear (morning)
        'ninbulomtang': ('nin-bulom-tang', 'day-ruin-place'),  # desolate, high (ruin)
        'kangcip': ('kang-cip', 'dry-lick'),                   # lick up (fire)
        'kaito': ('kai-to', 'rise-DIR'),                       # arise, come up
        'awngkhia': ('awng-khia', 'call-out'),                 # cry out
        
        # More apostrophe forms
        "liante'": ('lian-te', 'great-PL'),                    # great ones
        "gilote'": ('gi-lo-te', 'near-NEG-PL'),                # those far away
        "lianpa'": ('lian-pa', 'great-father'),                # great man, elder
        "tuute'": ('tuu-te', 'sheep-PL'),                      # sheep (plural)
        "tegel'": ('tegel', 'bridle'),                         # bridle
        "thukhente'": ('thu-khen-te', 'word-divide-PL'),       # judges, those who decide
        "khatpeuh'": ('khat-peuh', 'one-any'),                 # anyone, any
        "nengniamte'": ('neng-niam-te', 'sit-low-PL'),         # humble ones
        "cian'": ('cian', 'announce'),                         # announce
        "kumpinu'": ('kumpi-nu', 'king-mother'),               # queen mother
        
        # Round 65: More partial analyses
        'zial': ('zi-al', 'shadow-defense'),                   # defense, protection
        'taktakna': ('tak-tak-na', 'true-REDUP-NMLZ'),         # certainly, truly
        'kawt': ('kawt', 'head'),                              # head (of river)
        'kamkaih': ('kam-kaih', 'word-betray'),                # treachery
        'silsiang': ('sil-siang', 'wash-clean'),               # wash clean
        'nawnkei': ('nawn-kei', 'again-NEG'),                  # not again, no more
        'thuahthuah': ('thuah-thuah', 'break-REDUP'),          # break repeatedly, breach upon breach
        'puanpi': ('puan-pi', 'cloth-great'),                  # robe, garment
        'tuamtuamin': ('tuam-tuam-in', 'various-REDUP-ERG'),   # in various ways, diversely
        'hawmpi': ('hawm-pi', 'arrange-great'),                # order, arrange properly
        'omthei': ('om-thei', 'exist-can'),                    # be possible, can be
        'kapkap': ('kap-kap', 'weep-REDUP'),                   # weep continually
        'tawitehna': ('tawi-teh-na', 'hand-measure-NMLZ'),     # span, measure
        'angsung': ('ang-sung', 'breast-from'),                # weaned
        'pampaih': ('pam-paih', 'restore-heal'),               # restore health
        'cingsak': ('cing-sak', 'stand-CAUS'),                 # set up, make strong
        'siahdongpa': ('siah-dong-pa', 'tax-collect-AGT'),     # tax collector, publican
        'ankam': ('an-kam', 'food-seed'),                      # grain, seed
        'lungsimtawng': ('lung-sim-tawng', 'heart-mind-false'), # hypocrisy
        'nuamtaksa': ('nuam-tak-sa', 'want-true-CAUS'),        # pretence, make to want
        'cinuam': ('ci-nuam', 'say-pleasant'),                 # proverb
        'gennuam': ('gen-nuam', 'speak-want'),                 # want to say, have to say
        'biakinncing': ('biak-inn-cing', 'worship-house-betray'), # betray (at temple)
        'nekkhit': ('nek-khit', 'eat-after'),                  # after supper, after eating
        'khongin': ('khong-in', 'obey-ERG'),                   # obeying
        'bulphuh': ('bul-phuh', 'pride-emerge'),               # boasting
        'hinkikna': ('hin-kik-na', 'life-return-NMLZ'),        # receiving back, resurrection
        'pilsak': ('pil-sak', 'learn-CAUS'),                   # teach, make wise
        'tuithawl': ('tui-thawl', 'water-bottle'),             # water bottle, skin
        'humcip': ('hum-cip', 'fear-grip'),                    # fear, reverence
        'tuibeel': ('tui-beel', 'water-pitcher'),              # pitcher, vessel
        
        # More apostrophe words
        "bawlsiate'": ('bawl-sia-te', 'make-bad-PL'),          # evildoers
        "numeino'": ('numei-no', 'woman-little'),              # girl, young woman
        
        # Round 66: More unknowns
        'tuanu': ('tua-nu', 'that-female'),                    # her, unto her
        'liau': ('li-au', 'separate-go'),                      # miscarry, fruit depart
        'heikhiatsak': ('hei-khiat-sak', 'turn-twist-CAUS'),   # pervert, blindeth
        'khep': ('khep', 'couple'),                            # couple, pair
        'kigak': ('ki-gak', 'REFL-hook'),                      # be hooked, filleted
        'diamond': ('diamond', 'DIAMOND'),                     # diamond (loanword)
        'jakinth': ('jakinth', 'JACINTH'),                     # jacinth (loanword)
        'tuazah': ('tua-zah', 'that-fragrant'),                # sweet cinnamon
        'gawivui': ('gawi-vui', 'grind-dust'),                 # powder
        'phukpai': ('phuk-pai', 'cut-go'),                     # cut down
        'pheituam': ('phei-tuam', 'wear-cover'),               # bonnets
        'manzah': ('man-zah', 'value-measure'),                # estimation
        'kikuangsak': ('ki-kuang-sak', 'REFL-burn-CAUS'),      # burnt offering
        'kisukham': ('ki-suk-ham', 'REFL-cook-boil'),          # sodden, boiled
        'kitheh': ('ki-theh', 'REFL-pour'),                    # pour out
        'kisawhkha': ('ki-sawh-kha', 'REFL-touch-go'),         # touch, be touched
        'phiahsak': ('phiah-sak', 'bare-CAUS'),                # uncover
        'lozaw': ('lo-zaw', 'enter-COMP'),                     # deeper
        'phuisam': ('phui-sam', 'trip-cause.fall'),            # stumblingblock
        'kidaisak': ('ki-dai-sak', 'REFL-pollute-CAUS'),       # defile
        'leipa': ('lei-pa', 'buy-back'),                       # restore, redeem
        'kitanhkik': ('ki-tanh-kik', 'REFL-count-return'),     # be reckoned, counted
        'tuat': ('tuat', 'sell'),                              # sell
        'diik': ('diik', 'waste'),                             # desolation, waste
        'pheipi': ('phei-pi', 'bitter-great'),                 # bitter water, curse
        "mawkmawkte'": ('mawk-mawk-te', 'spot-REDUP-PL'),      # spotted ones
        
        # Round 67: More partial analyses
        'ngitngetna': ('ngit-nget-na', 'think-REDUP-NMLZ'),    # imagination, thought
        'sakhituihup': ('sak-hi-tuihup', 'set-be-cloud'),      # set in the cloud
        'neilai': ('nei-lai', 'have-still'),                   # still living, begat
        'atin': ('at-in', 'grow-ERG'),                         # growing
        'ciamnuih': ('ciam-nuih', 'promise-mock'),             # mocking
        'tuikhukah': ('tui-khuk-ah', 'water-well-LOC'),        # at the well
        'nene': ('ne-ne', 'eat-REDUP'),                        # eat of, eating
        'thallawng': ('thal-lawng', 'bow-quiver'),             # quiver (for arrows)
        'keelhon': ('keel-hon', 'call-flock'),                 # fetch from flock
        'thalawh': ('thal-awh', 'bow-?'),                      # younger (daughter)
        'lupkhawm': ('lup-khawm', 'lie.down-together'),        # go in unto, consummate
        'thuneu': ('thu-neu', 'word-small'),                   # small matter
        'ngahmun': ('ngah-mun', 'get-place'),                  # ford, crossing place
        'khuapih': ('khua-pih', 'town-gate'),                  # gate of city
        'kemsak': ('kem-sak', 'guard-CAUS'),                   # charge with, assign
        'vulgawp': ('vul-gawp', 'faint-strike'),               # very sore (famine)
        'khekna': ('khek-na', 'fail-NMLZ'),                    # failure
        'luahna': ('luah-na', 'beget-NMLZ'),                   # issue, offspring
        'zagui': ('za-gui', 'hear-secret'),                    # secret counsel
        'sawn': ('sawn', 'beat'),                              # beaten
        'vilna': ('vil-na', 'observe-NMLZ'),                   # observance
        'khamzah': ('kham-zah', 'forbid-measure'),             # according to eating
        'omzah': ('om-zah', 'exist-measure'),                  # each (measure)
        'haksate': ('haksa-te', 'difficult-PL'),               # hard (causes)
        'neisa': ('nei-sa', 'have-CAUS'),                      # give dominion
        'honsa': ('hon-sa', 'flock-CAUS'),                     # conceive (opened womb)
        
        # Round 68: More partial analyses
        'ziazua': ('zia-zua', 'sun-clear'),                    # clear morning (sunrise)
        'nawite': ('nawi-te', 'twin-PL'),                      # twins
        'khawngah': ('khawng-ah', 'wall-LOC'),                 # upon the wall
        'kangtummang': ('kang-tum-mang', 'burn-end-destroy'),  # devoured, consumed
        'kamkei': ('kam-kei', 'word-with'),                    # with me, come along
        'kahin': ('ka-hi-n', '1SG-be-PST'),                    # was (past tense)
        'zumna': ('zum-na', 'foolish-NMLZ'),                   # foolishness
        'zumhuaina': ('zum-huai-na', 'filth-bad-NMLZ'),        # shame, nakedness
        'zuipah': ('zui-pah', 'follow-toward'),                # follow (toward)
        'zuihtheih': ('zuih-theih', 'follow-can'),             # able to follow
        'zintunna': ('zin-tun-na', 'journey-arrive-NMLZ'),     # stay, remain
        'zinling': ('zin-ling', 'journey-pass'),               # still small (voice)
        'zawlta': ('zawl-ta', 'valley-?'),                     # Gileadite (from Gilead)
        'zawhgawp': ('zawh-gawp', 'able-strike'),              # able to conquer
        'zanuam': ('za-nuam', 'hear-desire'),                  # desire to hear
        'zanthapai': ('zan-tha-pai', 'night-new-go'),          # wearisome nights
        'zam': ('zam', 'fear'),                                # fear, distress
        'veivei': ('vei-vei', 'time-REDUP'),                   # from time to time
        'vatawt': ('va-tawt', 'go.and-?'),                     # hawk (bird)
        'vankah': ('van-kah', 'spirit-?'),                     # familiar spirits
        'vangikpi': ('vangik-pi', 'yoke-great'),               # grievous yoke
        'vailam': ('vai-lam', 'side-direction'),               # west side
        'umgui': ('um-gui', 'shade-?'),                        # gourd (shade plant)
        'tunsakna': ('tun-sak-na', 'arrive-CAUS-NMLZ'),        # offering (brought near)
        'tungtham': ('tung-tham', 'top-height'),               # height, stature
        'tungnungah': ('tung-nung-ah', 'above-back-LOC'),      # upper (chambers)
        'tuamsak': ('tuam-sak', 'cover-CAUS'),                 # clothe, fence
        'tuahsiatna': ('tuah-siat-na', 'do-bad-NMLZ'),         # complaining, evil deed
        'tuahna': ('tuah-na', 'do-NMLZ'),                      # deed, murder
        'top': ('top', 'generation'),                          # generations
        'tokhia': ('to-khia', 'sit-out'),                      # hew out
        
        # Round 69: More partials
        'thuzuau': ('thu-zuau', 'word-froward'),               # froward mouth
        'thuthukpi': ('thu-thuk-pi', 'word-deep-great'),       # secret, mystery
        'thuthei': ('thu-thei', 'word-know'),                  # understanding, wise
        'thutelna': ('thu-tel-na', 'word-fulfill-NMLZ'),       # charge, understanding
        'thutanna': ('thu-tan-na', 'word-judge-NMLZ'),         # right, cause, judgment
        'thumong': ('thu-mong', 'word-end'),                   # end, fate
        'thuktum': ('thuk-tum', 'deep-end'),                   # deep (of plague)
        'thukhual': ('thu-khual', 'word-strange'),             # strange, enemy
        'thudong': ('thu-dong', 'word-inquire'),               # enquire, ask
        'thuciamteh': ('thu-ciam-teh', 'word-promise-measure'), # covenant (confirm)
        'theihsak': ('theih-sak', 'know-CAUS'),                # make known
        'tektek': ('tek-tek', 'bend-REDUP'),                   # bend (tongues)
        'teello': ('teel-lo', 'choose-NEG'),                   # not chosen
        'teelkhiat': ('teel-khiat', 'choose-away'),            # reject, forsake
        'tawldamna': ('tawl-dam-na', 'rest-well-NMLZ'),        # hope, security
        'tawikhaina': ('tawi-khai-na', 'weigh-balance-NMLZ'),  # balance, integrity
        'tangtunsak': ('tang-tun-sak', 'arrive-reach-CAUS'),   # hasten, bring to pass
        'taiina': ('tai-na', 'correct-NMLZ'),                  # chastening
        'sutpi': ('sut-pi', 'spoil-great'),                    # chief cornerstone
        
        # Round 70: High-frequency partials
        'thalawh': ('thal-awh', 'bow-young'),                  # younger (daughter)
        'nawizu': ('nawi-zu', 'firstfruit-bring'),             # firstfruits
        'sikli': ('sik-li', 'robe-?'),                         # ephod
        'kiliahna': ('ki-liah-na', 'REFL-veil-NMLZ'),          # veil, covering
        'khutdim': ('khut-dim', 'hand-full'),                  # handful
        'beelpei': ('beel-pei', 'pan-flat'),                   # pan (flat)
        'kawnga': ('kawng-a', 'way-LOC'),                      # on the way
        'attan': ('at-tan', 'cut-down'),                       # break down (heifer)
        'hihkhak': ('hih-khak', 'be-may'),                     # if (it be)
        'pawn': ('pawn', 'scar'),                              # scar, burn
        'koihcip': ('koih-cip', 'put-lock'),                   # shut up
        'kizatna': ('ki-zat-na', 'REFL-use-NMLZ'),             # be spread
        'luakhia': ('lua-khia', 'exceed-out'),                 # vomit out, visit iniquity
        'cisa': ('ci-sa', 'say-CAUS'),                         # appoint, set over
        'kisehna': ('ki-seh-na', 'REFL-value-NMLZ'),           # redemption
        'painasa': ('pai-na-sa', 'go-NMLZ-CAUS'),              # saying, goodly land
        'seppih': ('sep-pih', 'work-with'),                    # keep charge
        'samsiatsak': ('sam-siat-sak', 'call-curse-CAUS'),     # curse
        'sawlteng': ('sawl-teng', 'send-all'),                 # speak only
        'galmuh': ('gal-muh', 'enemy-see'),                    # high places (to see)
        'kalun': ('ka-lun', '1SG-self'),                       # myself
        'nungakin': ('nung-ak-in', 'live-dwell-ERG'),          # being in (father's house)
        'laitakah': ('lai-tak-ah', 'midst-true-LOC'),          # in the very midst
        'khapa': ('kha-pa', 'spirit-father'),                  # God (spiritual father)
        'ciamtehin': ('ciam-teh-in', 'promise-measure-ERG'),   # lay up (in heart)
        'aituam': ('ai-tuam', 'self-cover'),                   # multiply (for himself)
        'nangawnun': ('nangawn-un', 'not.even-PL'),            # not even unto 10th gen
        'satsak': ('sat-sak', 'strike-CAUS'),                  # cause to be beaten
        'matsak': ('mat-sak', 'grasp-CAUS'),                   # take hold, draw near
        'simthamah': ('sim-tham-ah', 'count-be.able-LOC'),     # graven image (curse)
        'nawtkhia': ('nawt-khia', 'thrust-out'),               # underneath (thrust out)
        'kiphumna': ('ki-phum-na', 'REFL-bury-NMLZ'),          # burial place
        'gamtakha': ('gam-tak-ha', 'land-send-go'),            # far from land
        'cidamin': ('ci-dam-in', 'say-well-ERG'),              # in peace
        'paupih': ('pau-pih', 'speak-with'),                   # speak together
        'nungkikin': ('nung-kik-in', 'live-return-ERG'),       # cleave unto
        'sepnop': ('sep-nop', 'work-desire'),                  # desire to serve
        'damtakin': ('dam-tak-in', 'well-true-ERG'),           # surely, firmly
        'ginna': ('gin-na', 'believe-NMLZ'),                   # deliverance, faith
        'pawm': ('pawm', 'belly'),                             # belly (bitter water)
        'khanglam': ('khang-lam', 'generation-way'),           # provisions
        'ngetnop': ('nget-nop', 'request-desire'),             # desire a request
        'lungnuamsak': ('lung-nuam-sak', 'heart-pleasant-CAUS'), # cheer, make glad
        'khuadakin': ('khua-dak-in', 'town-division-ERG'),     # divide into companies
        
        # Round 71: More high-frequency partials
        'selkeu': ('sel-keu', 'cut-bundle'),                   # boughs (cut branches)
        'zawlta': ('zawl-ta', 'valley-from'),                  # Gileadite
        'pawipuan': ('pawi-puan', 'feast-cloth'),              # feast (linen garments)
        'luai': ('lua-i', 'exceed-?'),                         # middle (pillars)
        'naina': ('nai-na', 'near-NMLZ'),                      # battle, lying in wait
        'kumsim': ('kum-sim', 'year-count'),                   # yearly
        'sihsan': ('sih-san', 'die-leave'),                    # died (both)
        'maipuk': ('mai-puk', 'face-fall'),                    # fall on face
        'puato': ('pua-to', 'carry-up'),                       # fetch up
        'limcipen': ('lim-ci-pen', 'beauty-say-SUPRL'),        # best (vineyards)
        'bawngnote': ('bawng-no-te', 'cattle-young-PL'),       # calves
        'lingsa': ('ling-sa', 'fear-CAUS'),                    # trembled (elders)
        'puaksak': ('puak-sak', 'send-CAUS'),                  # send, laden
        'sihtheih': ('sih-theih', 'die-can'),                  # can be killed
        'kengin': ('keng-in', 'only-ERG'),                     # only (with ephod)
        'genthang': ('gen-thang', 'speak-hear'),               # report (heard)
        'pamah': ('pa-mah', 'father-self'),                    # aside (privately)
        'khangkhawm': ('khang-khawm', 'grow-together'),        # brought up
        'khutmeno': ('khut-me-no', 'hand-self-little'),        # own hands
        'khentel': ('khen-tel', 'divide-distinguish'),         # put difference
        'neizaw': ('nei-zaw', 'have-COMP'),                    # more parts
        'hatlua': ('hat-lua', 'strong-exceed'),                # too strong
        'kawkbaang': ('kawk-baang', 'call-upright'),           # upright man
        'dotna': ('dot-na', 'ask-NMLZ'),                       # asking (straitly)
        
        # Round 72: More high-frequency partials
        'pilzaw': ('pil-zaw', 'wise-COMP'),                    # wiser
        'cingsing': ('cing-sing', 'know-wood'),                # almug trees (rare wood)
        'lingnei': ('ling-nei', 'hope-have'),                  # add (whips)
        'kiheina': ('ki-hei-na', 'REFL-turn-NMLZ'),            # cause, turning
        'akte': ('ak-te', 'rooster-PL'),                       # lights (in firmament)
        'pailai': ('pai-lai', 'go-midst'),                     # day's journey
        'sampa': ('sam-pa', 'call-AGT'),                       # prophet (one who calls)
        'sawnkhia': ('sawn-khia', 'catch-out'),                # caught (at feet)
        'mattheih': ('mat-theih', 'grasp-can'),                # able to catch
        'kibatna': ('ki-bat-na', 'REFL-trust-NMLZ'),           # trust
        'nul': ('nul', 'beast'),                               # beast
        'sinna': ('sin-na', 'sin-NMLZ'),                       # young/tender
        'kilamkikna': ('ki-lam-kik-na', 'REFL-burden-return-NMLZ'), # burdens laid
        'keen': ('keen', 'alive'),                             # alive
        'sumkem': ('sum-kem', 'money-guard'),                  # treasurer
        'kisuksiatna': ('ki-suk-siat-na', 'REFL-pollute-destroy-NMLZ'), # destruction
        'mualbo': ('mual-bo', 'see-round'),                    # over against
        'mui': ('mui', 'shoot'),                               # shoot (arrows)
        'kikna': ('kik-na', 'return-NMLZ'),                    # returning, bringing back
        'minthuhna': ('min-thuh-na', 'name-sign-NMLZ'),        # signet ring
        'phatuam': ('pha-tuam', 'good-exceed'),                # forcible
        'singteh': ('sing-teh', 'tree-break'),                 # leaf (driven)
        'ciangtan': ('ciang-tan', 'weave-swift'),              # shuttle (weaver's)
        'nuamtuam': ('nuam-tuam', 'want-cover'),               # forbear
        'nektum': ('nek-tum', 'eat-end'),                      # destroy body
        'letkhiat': ('let-khiat', 'return-away'),              # depart from
        'paubaan': ('pau-baan', 'speak-?'),                    # perfect (blameless)
        'suakkha': ('suak-kha', 'become-hard'),                # hardened
        'henna': ('hen-na', 'cast-NMLZ'),                      # casting off (cords)
        'linglawng': ('ling-lawng', 'hope-vex'),               # vex (in displeasure)
        'lungngai': ('lung-ngai', 'heart-meditate'),           # meditate
        'hingkhia': ('hing-khia', 'be-out'),                   # travail, bring forth
        'kiphatna': ('ki-phat-na', 'REFL-praise-NMLZ'),        # excellent, glory
        'pialkhia': ('pial-khia', 'show-out'),                 # declare
        'laikung': ('lai-kung', 'midst-matter'),               # inditing, matter
        'kisikcip': ('ki-sik-cip', 'REFL-turn-grip'),          # return ashamed
        'luangkhiasak': ('luang-khia-sak', 'flow-out-CAUS'),   # bring streams
        'ansi': ('an-si', 'grain-chaff'),                      # chaff
        'silesa': ('si-lesa', 'skin-faint'),                   # flesh fail
        'kankan': ('kan-kan', 'seek-REDUP'),                   # sought out
        'sakpa': ('sak-pa', 'cause-AGT'),                      # one who makes
        'sumlepai': ('sum-le-pai', 'money-and-go'),            # ransom
        
        # Round 73: More high-frequency partials
        'muantheih': ('muan-theih', 'trust-can'),              # directeth (way)
        'nuamtak': ('nuam-tak', 'peace-true'),                 # in peace
        'ngaihsutpi': ('ngaih-sut-pi', 'think-measure-great'), # guide heart (wisdom)
        'luhgawp': ('luh-gawp', 'enter-strike'),               # spoil dwelling
        'nuammawh': ('nuam-mawh', 'envy-wrong'),               # envious of wicked
        'al': ('al', 'cubit'),                                 # cubit
        'leengto': ('leeng-to', 'chariot-fly'),                # swallow (bird)
        'luak': ('luak', 'vomit'),                             # vomit out
        'lungdamzaw': ('lung-dam-zaw', 'heart-well-COMP'),     # more favour
        'hilel': ('hi-lel', 'be-hold'),                        # taketh hold
        'nik': ('nik', 'forget'),                              # forget
        'kelkel': ('kel-kel', 'doves-REDUP'),                  # doves' eyes
        'sawtpekin': ('sawt-pek-in', 'long-ago-ERG'),          # long ago
        'kisaktheihna': ('ki-sak-theih-na', 'REFL-make-can-NMLZ'), # stay (on God)
        'masakna': ('ma-sak-na', 'self-cause-NMLZ'),           # first place (Shiloh)
        'hilhtel': ('hilh-tel', 'teach-understand'),           # understand
        'paulamin': ('pau-lam-in', 'speak-toward-ERG'),        # spoken to
        'kaihkhiat': ('kaih-khiat', 'lead-away'),              # loose (shoe)
        'nungtalai': ('nung-ta-lai', 'live-PFV-midst'),        # still living
        'anla': ('an-la', 'grain-harvest'),                    # seedtime and harvest
        'galdalna': ('gal-dal-na', 'war-equip-NMLZ'),          # armour
        'pangpi': ('pang-pi', 'side-great'),                   # four sides
        'hilhkholh': ('hilh-kholh', 'teach-swallow'),          # swallowed up
        'silhpa': ('silh-pa', 'clothe-AGT'),                   # one clothed
        'huanna': ('huan-na', 'build-NMLZ'),                   # building
        'lungkimzo': ('lung-kim-zo', 'heart-full-COMPL'),      # satisfied
        'kongvang': ('kong-vang', 'way-empty'),                # grave's mouth
        'ngahzah': ('ngah-zah', 'get-measure'),                # treasure desired
        'piaknop': ('piak-nop', 'give-desire'),                # consecrate
        'khongkhai': ('khong-khai', 'obey-?'),                 # hearkened
        'minambup': ('min-am-bup', 'name-all-turn'),           # transgressions
        'muhnop': ('muh-nop', 'see-desire'),                   # prepare way
        'ngahthei': ('ngah-thei', 'get-can'),                  # ravening
        'sihkhawm': ('sih-khawm', 'die-together'),             # die with
        'nehcip': ('neh-cip', 'press-throng'),                 # throng, press
        'neutung': ('neu-tung', 'little-since'),               # since childhood
        'cihkhit': ('cih-khit', 'say-after'),                  # faith made whole
        'dingzia': ('ding-zia', 'stand-how'),                  # betray
        'nitawp': ('ni-tawp', 'day-end'),                      # last day
        'paitheih': ('pai-theih', 'go-can'),                   # able to go
        'nekkhawmna': ('nek-khawm-na', 'eat-together-NMLZ'),   # communion
        
        # Round 74: More partials (2026-03-08)
        'pawlkhatte': ('pawl-khat-te', 'group-one-PL'),        # companies (1 Sam 8:12)
        'cian': ('cian', 'light'),                             # light (Gen 1:3)
        'thukhente': ('thu-khen-te', 'word-judge-PL'),         # judges (Ex 21:6)
        'khatpeuh': ('khat-peuh', 'one-whosoever'),            # whosoever (Gen 4:15)
        'nengniamte': ('neng-niam-te', 'oppress-low-PL'),      # those oppressed (Jdg 2:18)
        'kumpinu': ('kumpi-nu', 'king-female'),                # queen (1 Kgs 10:1)
        'bawlsiate': ('bawl-sia-te', 'do-evil-PL'),            # persecutors (Ps 31:15)
        'numeino': ('numei-no', 'woman-DIM'),                  # maid (Ex 2:8)
        'sikli': ('sikli', 'cubit'),                           # cubit (Ex 28:4)
        'luai': ('luai', 'pillar'),                            # pillar (Jdg 16:29)
        'paubaan': ('pau-baan', 'speak-true'),                 # perfect (Gen 6:9)
        'khongkhai': ('khong-khai', 'magic-open'),             # diviner (Deut 18:14)
        'umgui': ('um-gui', 'be-gourd'),                       # gourd (Jonah 4:6)
        'khuan': ('khuan', 'dance'),                           # dance (Gen 31:27)
        'pawlpi': ('pawl-pi', 'group-big'),                    # troop (2 Sam 2:25)
        'ngahzaw': ('ngah-zaw', 'get-more'),                   # more blessed (Deut 33:24)
        'khopa': ('khopa', 'tiller'),                          # tiller (Gen 4:2)
        'omden': ('om-den', 'be-always'),                      # always (Num 9:16)
        'omto': ('om-to', 'be-over'),                          # covered (Gen 7:20)
        'vaihawmte': ('vaihawm-te', 'imagine-PL'),             # those who imagine (Gen 11:6)
        'kimatna': ('ki-mat-na', 'REFL-train-NMLZ'),           # trained (Gen 14:14)
        'honpite': ('hon-pi-te', 'many-big-PL'),               # many (Gen 1:20)
        'nisat': ('ni-sat', 'day-heat'),                       # heat of day (Gen 18:1)
        'minsa': ('min-sa', 'raw-meat'),                       # raw meat (1 Sam 2:15)
        'nunghei': ('nung-hei', 'behind-look'),                # look back (Gen 19:17)
        'paikhiatsak': ('pai-khia-sak', 'go-out-CAUS'),        # send away (Gen 20:13)
        'hoihkhop': ('hoih-khop', 'good-sufficient'),          # sufficient (Prov 25:16)
        'sumbukte': ('sum-buk-te', 'money-merchant-PL'),       # merchants (Gen 23:16)
        'vangsak': ('vang-sak', 'prosper-CAUS'),               # make prosperous (Gen 24:12)
        'nakbah': ('nak-bah', 'ear-ring'),                     # earring (Gen 24:22)
        'ciahkhiasak': ('ciah-khia-sak', 'go-out-CAUS'),       # send away (Gen 24:59)
        'kikhuhna': ('ki-khuh-na', 'REFL-cover-NMLZ'),         # veil (Gen 24:65)
        'nauzaw': ('nau-zaw', 'child-more'),                   # younger (Gen 25:23)
        'tungtangah': ('tung-tang-ah', 'well-another-LOC'),    # another well (Gen 26:21)
        'tuto': ('tu-to', 'sit-up'),                           # sit up (Gen 27:19)
        'kikokhia': ('ki-ko-khia', 'REFL-cry-out'),            # cry out (Gen 27:34)
        'nikhat': ('ni-khat', 'day-one'),                      # one day (Gen 27:45)
        'ihmutna': ('ih-mut-na', 'sleep-wake-NMLZ'),           # awaking (Gen 28:16)
        'hiangpa': ('hiang-pa', 'green-tree'),                 # poplar (Gen 30:37)
        'sawmvei': ('sawm-vei', 'ten-times'),                  # ten times (Gen 31:7)
        'kitenna': ('ki-ten-na', 'REFL-marry-NMLZ'),           # marriage (Gen 34:9)
        
        # Round 75: More partials (2026-03-08)
        'nausuah': ('nau-suah', 'child-give.birth'),           # give birth (Gen 35:16)
        'bansau': ('ban-sau', 'coat-long'),                    # coat (Gen 37:3)
        'thugente': ('thu-gen-te', 'word-tell-PL'),            # words (Gen 37:8)
        'zasakkik': ('za-sak-kik', 'word-CAUS-return'),        # bring word (Gen 37:14)
        'puaksuk': ('puak-suk', 'carry-down'),                 # carry down (Gen 37:25)
        'meetna': ('meet-na', 'profit-NMLZ'),                  # profit (Gen 37:26)
        'lungkimhuai': ('lung-kim-huai', 'heart-full-almost'), # displeased (Gen 38:10)
        'siatloh': ('siat-loh', 'destroy-NEG'),                # not perish (Gen 41:36)
        'zuisuk': ('zui-suk', 'follow-down'),                  # descend after (Gen 42:38)
        'ciahpihkik': ('ciah-pih-kik', 'go-with-return'),      # bring back (Gen 43:9)
        'puakik': ('puak-ik', 'carry-return'),                 # carry again (Gen 43:12)
        'maimawk': ('mai-mawk', 'face-fail'),                  # die (Gen 47:19)
        'leenggahtui': ('leeng-gah-tui', 'grape-juice-water'), # wine (Gen 49:11)
        'suakkhiasak': ('suak-khia-sak', 'become-out-CAUS'),   # let loose (Gen 49:21)
        'keivom': ('kei-vom', 'wolf-?'),                       # wolf (Gen 49:27)
        'thuum': ('thuum', 'mourning'),                        # mourning (Gen 50:10)
        'naudomte': ('nau-dom-te', 'child-care-PL'),           # midwives (Ex 1:17)
        'hihkha': ('hih-kha', 'this-EMPH'),                    # lest (Ex 5:3)
        'mekna': ('mek-na', 'knead-NMLZ'),                     # kneading trough (Ex 8:3)
        'kaikhawmte': ('kai-khawm-te', 'gather-together-PL'),  # those gathered (Ex 16:18)
        'sansak': ('san-sak', 'prevail-CAUS'),                 # cause to prevail (Ex 17:11)
        'puakpih': ('puak-pih', 'carry-with'),                 # bear with (Ex 18:22)
        'tatkhiat': ('tat-khiat', 'redeem-?'),                 # redeem (Ex 15:13)
        'hawmguak': ('hawm-guak', 'empty-?'),                  # empty (Gen 31:42)
        'kikihtakna': ('ki-kih-tak-na', 'REFL-fear-true-NMLZ'),# fear (Ex 23:27)
        'kaisuk': ('kai-suk', 'hang-down'),                    # hang over (Ex 26:12)
        'gakna': ('gak-na', 'hook-NMLZ'),                      # hooks (Ex 27:10)
        'topaz': ('topaz', 'topaz'),                           # topaz (Ex 28:17)
        'sianthosak': ('sian-tho-sak', 'holy-rise-CAUS'),      # hallow (Ex 29:1)
        'iikte': ('iik-te', 'breast-PL'),                      # breasts (Lev 9:20)
        'sai': ('sai', 'ashes'),                               # ashes (Lev 6:10)
        'supna': ('sup-na', 'bless-NMLZ'),                     # blessing (Ex 32:29)
        'kizutna': ('ki-zut-na', 'REFL-hook-NMLZ'),            # hooks/fillets (Ex 38:17)
        'kisimna': ('ki-sim-na', 'REFL-count-NMLZ'),           # numbered (Ex 38:26)
        'sikbeel': ('sik-beel', 'fry-pan'),                    # frying pan (Lev 2:7)
        
        # Apostrophe variants of Round 74-75 entries
        "pawlkhatte'": ('pawl-khat-te', 'group-one-PL'),
        "cian'": ('cian', 'light'),
        "thukhente'": ('thu-khen-te', 'word-judge-PL'),
        "khatpeuh'": ('khat-peuh', 'one-whosoever'),
        "nengniamte'": ('neng-niam-te', 'oppress-low-PL'),
        "kumpinu'": ('kumpi-nu', 'king-female'),
        "bawlsiate'": ('bawl-sia-te', 'do-evil-PL'),
        "numeino'": ('numei-no', 'woman-DIM'),
        "khuan'": ('khuan', 'dance'),
        "pawlpi'": ('pawl-pi', 'group-big'),
        "honpite'": ('hon-pi-te', 'many-big-PL'),
        "sumbukte'": ('sum-buk-te', 'money-merchant-PL'),
        "nauzaw'": ('nau-zaw', 'child-more'),
        "minthan'": ('min-than', 'name-new'),
        "mithagolte'": ('mitha-gol-te', 'giant-?-PL'),
        "sawmthumte'": ('sawm-thum-te', 'ten-three-PL'),
        "gamsate'": ('gam-sa-te', 'land-flesh-PL'),
        "tangvalpa'": ('tang-val-pa', 'young-man-NMLZ'),
        
        # Round 76: More partials (2026-03-08)
        'vatawt': ('vatawt', 'owl'),                           # owl/hawk (Lev 11:16)
        'apin': ('a-pin', '3SG-adversary'),                    # adversary (Matt 5:25)
        'mithagol': ('mitha-gol', 'giant-?'),                  # giant (2 Sam 21:18)
        'vankah': ('van-kah', 'sky-wizard'),                   # familiar spirit (Lev 20:6)
        'peuhpeuhte': ('peuh~peuh-te', 'any~REDUP-PL'),        # any/whatsoever (Lev 6:7)
        'gawhna': ('gawh-na', 'kill-NMLZ'),                    # place of killing (Lev 7:2)
        'khamvalte': ('kham-val-te', 'remain-fragment-PL'),    # fragments (Lev 8:32)
        'noptuam': ('nop-tuam', 'stay-?'),                     # at a stay (Lev 13:5)
        'bilteep': ('bil-teep', 'ear-tip'),                    # tip of ear (Lev 8:23)
        'kimkhatte': ('kim-khat-te', 'side-one-PL'),           # right side (Lev 14:16)
        'maisiat': ('mai-siat', 'face-set.against'),           # set face against (Lev 17:10)
        'vaksuk': ('vak-suk', 'go-down'),                      # go up and down (Lev 19:16)
        'namdang': ('nam-dang', 'kind-different'),             # diverse kind (Lev 19:19)
        'siantho': ('sian-tho', 'holy-glory'),                 # holiness (Ex 15:11)
        'saan': ('saan', 'lot'),                               # cast lots (Lev 16:8)
        'siik': ('siik', 'silk'),                              # silk
        'silin': ('silin', 'cymbal'),                          # cymbal
        
        # More apostrophe variants
        "vatawt,": ('vatawt', 'owl'),
        "apin,": ('a-pin', '3SG-adversary'),
        "bilteep,": ('bil-teep', 'ear-tip'),
        "silin,": ('silin', 'cymbal'),
        "hi'ng,": ('hi', 'this'),
        "hi!'": ('hi', 'this'),
        
        # Round 77: Final push to 98.5% (2026-03-08)
        'siangthosakpa': ('siangtho-sak-pa', 'holy-CAUS-NMLZ'),     # he who sanctifies (Lev 21:8)
        'kikhopnate': ('ki-khop-na-te', 'REFL-gather-NMLZ-PL'),     # feasts/convocations (Lev 23:2)
        'nekha': ('nek-ha', 'eat-together'),                        # eat with (Gen 43:32)
        'khamtakun': ('kham-takun', 'dwell-safely'),                # dwell safely (Lev 25:19)
        'pawmsak': ('pawm-sak', 'swell-CAUS'),                      # make swell (Num 5:21)
        'lungnem': ('lung-nem', 'heart-soft'),                      # meek (Num 12:3)
        'tawpun': ('tawp-un', 'end-?'),                             # good/fat (Num 13:20)
        'sialamin': ('sia-lam-in', 'bad-side-INST'),                # slander (Num 14:36)
        'piakkhawm': ('piak-khawm', 'give.to-together'),            # offer together (Num 15:6)
        'hingtangin': ('hing-tang-in', 'live-still-INST'),          # alive/quick (Num 16:30)
        'nekpih': ('nek-pih', 'eat-with'),                          # eat with (Num 18:22)
        'kantansak': ('kantan-sak', 'turn-CAUS'),                   # let pass (Num 20:17)
        'tangten': ('tang-ten', 'dwell-alone'),                     # dwell alone (Num 23:9)
        'huante': ('huan-te', 'garden-PL'),                         # gardens (Num 24:6)
        'aloes': ('aloes', 'aloes'),                                # aloes (Num 24:6)
        "tangten'": ('tang-ten', 'dwell-alone'),
        
        # Fix remaining keivom etc.
        'keivom': ('kei-vom', 'wolf-?'),                           # wolf (Gen 49:27)
        'tatkhiat': ('tat-khiat', 'ransom-release'),                # redeem (Ex 15:13)
        'hawmguak': ('hawm-guak', 'hand-empty'),                    # empty-handed (Gen 31:42)
        'noptuam': ('nop-tuam', 'like-desire'),                     # at a stay (Lev 13:5)
        
        # Round 78: Push to 98.5% (2026-03-08)
        'pailetin': ('pai-let-in', 'go-enter-INST'),               # went into tent (Num 25:8)
        'tamte': ('tam-te', 'many-PL'),                            # many (Num 26:54)
        'tuukhawkte': ('tuu-khawk-te', 'grandchild-sheep-PL'),     # sheepfolds (Num 32:16)
        'khuai': ('khuai', 'nuts'),                                # nuts (Gen 43:11)
        'hilhsawn': ('hilh-sawn', 'set-righteous'),                # righteous (Deut 4:8)
        'sumsan': ('sum-san', 'money-lack'),                       # scarceness (Deut 8:9)
        'khauhna': ('khauh-na', 'stubborn-NMLZ'),                  # stubbornness (Deut 9:27)
        'keising': ('kei-sing', 'owl-?'),                          # cormorant (Isa 34:11)
        'hotkhiatsa': ('hot-khiat-sa', 'bring-out-PERF'),          # brought forth (Deut 9:26)
        'minsia': ('min-sia', 'name-bad'),                         # evil name (Deut 22:14)
        'lakkhial': ('lak-khial', 'take-wander'),                  # make wander (Deut 27:18)
        'nilohin': ('ni-loh-in', 'day-long-INST'),                 # all day long (Deut 28:32)
        'singlesuang': ('sing-le-suang', 'wood-and-stone'),        # wood and stone (Deut 28:36)
        'kuangsak': ('kuang-sak', 'fire-CAUS'),                    # kindle (Deut 32:22)
        'ngaihsutzaw': ('ngaih-sut-zaw', 'think-more-COMP'),       # acknowledge (Deut 33:9)
        'bualtuite': ('bual-tui-te', 'lake-water-PL'),             # west (Deut 33:23)
        'khiatsuk': ('khiat-suk', 'out-down'),                     # dwell safely (Deut 33:28)
        'suksiatmang': ('suk-siat-mang', 'down-destroy-all'),      # utterly destroy (Josh 2:10)
        'kizomte': ('ki-zom-te', 'REFL-related-PL'),               # relatives (Josh 2:13)
        'khaisuk': ('khai-suk', 'hang-down'),                      # on this side (Ex 38:15)
        'piau': ('piau', 'edge'),                                  # brim (Josh 3:15)
        'bawltheih': ('bawl-theih', 'make-can'),                   # make league (Josh 9:7)
        'khinmang': ('khin-mang', 'breath-all'),                   # any to breathe (Josh 11:11)
        'lungsimtak': ('lung-sim-tak', 'heart-think-true'),        # wholly followed (Josh 14:14)
        'zawhsa': ('zawh-sa', 'subdue-PERF'),                      # subdued (Josh 18:1)
        "tawpun": ('tawp-un', 'end-EMPH'),                         # final
        "beisakin,": ('bei-sak-in', 'pierce-CAUS-INST'),
        
        # Round 79: More partials (2026-03-08)
        'mithagol': ('mitha-gol', 'person-giant'),                 # giant (2 Sam 21:18)
        "mithagolte'": ('mitha-gol-te', 'person-giant-PL'),        # giants
        'kigelhte': ('ki-gelh-te', 'REFL-expel-PL'),               # expel them (Josh 23:5)
        'paikhawmin': ('pai-khawm-in', 'go-together-INST'),        # went with (Jdg 1:17)
        'thaukhal': ('thau-khal', 'fat-kidney'),                   # fat (Deut 32:14)
        'tupna': ('tup-na', 'cast.down-NMLZ'),                     # plead/altar (Jdg 6:31)
        'galpanna': ('galpan-na', 'armed-NMLZ'),                   # armed men (Jdg 7:11)
        'thuksak': ('thu-sak', 'word-CAUS'),                       # speak/proceed (Jdg 11:36)
        'ciahsan': ('ciah-san', 'go-up'),                          # went up (Jdg 14:19)
        'meite': ('mei-te', 'fire-PL'),                            # firebrands (Jdg 15:4)
        'thalkhau': ('thal-khau', 'new-cord'),                     # green withs (Jdg 16:7)
        'guallelhna': ('guallelh-na', 'ambush-NMLZ'),              # liers in wait (Jdg 20:36)
        'uilut': ('ui-lut', 'dog-enter'),                          # emerods (1 Sam 5:6)
        'kuanna': ('kuan-na', 'reign-NMLZ'),                       # reign (1 Sam 12:12)
        'sattuk': ('sat-tuk', 'strike-reach'),                     # smote (1 Sam 14:31)
        'suanglotna': ('suang-lot-na', 'stone-throw-NMLZ'),        # sling (1 Sam 17:40)
        'liamte': ('liam-te', 'wound-PL'),                         # wounded (1 Sam 17:52)
        
        # More from the partial list
        "thugente'": ('thu-gen-te', 'word-tell-PL'),               # words/speakers
        'keivom': ('kei-vom', 'wolf-male'),                        # wolf (Gen 49:27)
        'keising': ('kei-sing', 'owl-tree'),                       # cormorant (Isa 34:11)
        'pawlbawl': ('pawl-bawl', 'group-make'),                   # organize (group)
        'utun': ('ut-un', 'want-EMPH'),                            # will/want (emphatic)
        'ute': ('ut-e', 'want-NMLZ'),                              # wanting
        "thumte'": ('thum-te', 'three-PL'),                        # threes
        'ziau': ('zi-au', 'wife-elder.sibling'),                   # sister-in-law
        'puteek': ('pute-ek', 'ancestors-small'),                  # forefathers
        'lausakin': ('lau-sak-in', 'fear-CAUS-INST'),              # fearing
        'sawkin': ('sa-wkin', 'flesh-?'),                          # bodily
        # Round 80: KJV-verified vocabulary
        'lumsak': ('lum-sak', 'lie.down-CAUS'),                    # cause to lie down, lodge
        'thupuak': ('thu-puak', 'word-make'),                      # command, instruct
        'thupuakpa': ('thu-puak-pa', 'word-make-NMLZ.M'),          # commander
        'ciahkhiat': ('ciah-khiat', 'return-completely'),          # depart completely
        'ciap': ('ciap', 'taste'),                                 # taste, try
        'dimna': ('dim-na', 'full-NMLZ'),                          # fullness, plot (of land)
        'pakpalhte': ('pakpalh-te', 'flower.opening-PL'),          # open flowers (carved)
        'pakpalh': ('pakpalh', 'flower.opening'),                  # open flower
        'vawhsak': ('vawh-sak', 'saddle-CAUS'),                    # saddle (animal)
        'maikhingin': ('maikhing-in', 'displeased-INST'),          # displeasedly
        'maikhing': ('maikhing', 'displeased'),                    # displeased, sullen
        'thukante': ('thukan-te', 'messenger-PL'),                 # messengers
        'thukan': ('thukan', 'messenger'),                         # messenger
        'thukanpa': ('thukan-pa', 'messenger-NMLZ.M'),             # messenger (male)
        # More Round 80 entries
        'hihlo': ('hi-hlo', 'be-NEG'),                             # is not (contraction)
        'neihlam': ('neih-lam', 'have.II-manner'),                 # having, possession
        'ciangduai': ('ciangduai', 'rod/scourge'),                 # rod, scourge (punishment)
        'thulamlak': ('thu-lamlak', 'word-crooked'),               # crooked counsel
        'thulamlakpa': ('thu-lamlak-pa', 'word-crooked-NMLZ.M'),   # counsellor (wisdom)
        'khuanawl': ('khua-nawl', 'town-outskirts'),               # outskirts of town
        'thukawi': ('thu-kawi', 'word-crooked'),                   # perverse, froward
        'sawmsimin': ('sawmsim-in', 'conspire-INST'),              # conspiring
        'sawmsim': ('sawmsim', 'conspire'),                        # conspire
        'sawmsimna': ('sawmsim-na', 'conspire-NMLZ'),              # conspiracy
        # Round 81: KJV-verified vocabulary
        'tong': ('tong', 'end/tip'),                               # hinder end, way, path
        'ngap': ('ngap', 'cross/array'),                           # ferry, deck oneself
        'kawk': ('kawk', 'upright/look.toward'),                   # morally upright, face
        'daupaina': ('daupai-na', 'prosper-NMLZ'),                 # prosperity
        'daupai': ('daupai', 'prosper'),                           # prosper
        'liahna': ('liah-na', 'dwell-NMLZ'),                       # dwelling place, secret place
        'liah': ('liah', 'lick/dwell'),                            # lick, dwell
        'leibatna': ('leibat-na', 'debt-NMLZ'),                    # creditor (debt claim)
        'leibat': ('leibat', 'debt'),                              # debt
        'leibatnapa': ('leibat-na-pa', 'debt-NMLZ-NMLZ.M'),        # creditor (person)
        'mittawtna': ('mittawt-na', 'blind-NMLZ'),                 # blindness
        'mittawt': ('mittawt', 'blind'),                           # blind
        'hinkiksak': ('hin-kik-sak', 'live-return-CAUS'),          # restore to life
        'phelkham': ('phel-kham', 'split-across'),                 # rip open
        'laktheih': ('lak-theih', 'take-able'),                    # capture, seize
        'hingmat': ('hing-mat', 'alive-grasp'),                    # take alive, capture alive
        'sehkhatte': ('sehkhat-te', 'one.third-PL'),               # thirds, third parts
        'sehkhat': ('sehkhat', 'one.third'),                       # one third
        'satpukin': ('sat-puk-in', 'strike-down-INST'),            # smiting down
        'satpuk': ('sat-puk', 'strike-down'),                      # smite down
        'neuno': ('neu-no', 'small-DIM'),                          # small thing, trifle
        # Round 82: KJV-verified vocabulary
        'cilphuan': ('cil-phuan', 'spittle-foam'),                 # foam, let spittle fall
        'vanglianpa': ('vanglian-pa', 'almighty-NMLZ.M'),          # the Almighty
        'vanglian': ('vanglian', 'almighty'),                      # almighty, omnipotent
        'zahun': ('za-hun', 'hundred-time'),                       # might, all one's strength
        'semzaw': ('sem-zaw', 'serve-more'),                       # serve more
        'bukno': ('buk-no', 'ambush-DIM'),                         # watchtower, guardpost
        'hilhkholhnate': ('hilh-kholh-na-te', 'teach-RECIPR-NMLZ-PL'),  # testimonies
        'hilhkholhna': ('hilh-kholh-na', 'teach-RECIPR-NMLZ'),     # testimony
        'heina': ('hei-na', 'mock-NMLZ'),                          # mockery, provocation
        'hei': ('hei', 'mock'),                                    # mock, provoke
        'khankhit': ('khan-khit', 'grow-before'),                  # before growing up
        'kamsangnu': ('kamsang-nu', 'prophet-F'),                  # prophetess
        'genkholhsa': ('gen-kholh-sa', 'speak-RECIPR-PRF'),        # spoken (prophecy)
        'keeksak': ('keek-sak', 'tear.open-CAUS'),                 # enlarge, expand borders
        'gualnopna': ('gualnop-na', 'rejoice-NMLZ'),               # rejoicing, mirth
        'gualnop': ('gualnop', 'rejoice'),                         # rejoice, be merry
        # Round 83: KJV-verified vocabulary
        'siktukkilh': ('sik-tukkilh', 'iron-nail'),                # iron nail
        'kipakna': ('kipak-na', 'rejoice.together-NMLZ'),          # rejoicing, gladness
        'kipak': ('ki-pak', 'REFL-rejoice'),                       # rejoice together
        'lamdangpi': ('lamdang-pi', 'strange-great'),              # marvelously, wonderfully
        'khotakin': ('khotak-in', 'zealous-INST'),                 # diligently, zealously
        'khotak': ('khotak', 'zealous'),                           # diligent, zealous
        'siksan': ('sik-san', 'iron-attach'),                      # nail, stake, confidence
        'gamtatsiate': ('gamtat-sia-te', 'deed-evil-PL'),          # evil deeds, iniquities
        'gamtatsia': ('gamtat-sia', 'deed-evil'),                  # evil deed
        'khasak': ('kha-sak', 'send-CAUS'),                        # cause to go, escort
        'khamseek': ('kham-seek', 'gold-smith'),                   # goldsmith
        'khamseekpa': ('kham-seek-pa', 'gold-smith-NMLZ.M'),       # goldsmith
        'sawlbuk': ('sawl-buk', 'leaf-booth'),                     # booth, tabernacle
        'gawpna': ('gawp-na', 'trample-NMLZ'),                     # trampling
        'gawp': ('gawp', 'trample'),                               # trample, tread
        'dangtakna': ('dang-tak-na', 'thirst-ADV-NMLZ'),           # thirst
        'dangtak': ('dangtak', 'thirst'),                          # thirst
        'gentelna': ('gen-tel-na', 'speak-understand-NMLZ'),       # explanation, entrance
        'gentel': ('gen-tel', 'speak-understand'),                 # explain
        'dawnkikna': ('dawn-kik-na', 'answer-return-NMLZ'),        # reply, answer
        'dawnkik': ('dawn-kik', 'answer-return'),                  # reply, answer back
        # Round 84: KJV-verified vocabulary
        'nautang': ('nau-tang', 'child-group'),                    # families, divisions
        'langtangin': ('langtang-in', 'open-INST'),                # openly, before (someone)
        'langtang': ('langtang', 'open'),                          # open, public
        'ciahpah': ('ciah-pah', 'return-immediately'),             # go home quickly
        'kihtaktak': ('kihtak-tak', 'dread-INTENS'),               # greatly fear
        'kihtak': ('kihtak', 'dread'),                             # dread, fear greatly
        'zanglo': ('zang-lo', 'use-NEG'),                          # not use, pervert
        'sazang': ('sa-zang', 'flesh-fiber'),                      # sinews, muscle
        'baihta': ('baih-ta', 'certain-PRF'),                      # certainly, surely (go)
        'banzo': ('ban-zo', 'reach-able'),                         # reach, attain
        'suksuk': ('suk-suk', 'make-REDUP'),                       # continually, repeatedly
        'awle': ('awle', 'leviathan'),                             # leviathan, sea monster
        # Round 85: KJV-verified vocabulary
        'khinkhian': ('khin-khian', 'wait-INTENS'),                # wait, lie in wait
        'cimang': ('ci-mang', 'say-finish'),                       # desolate, perish
        'ngahnop': ('ngah-nop', 'get-want'),                       # desire to get, covet
        'hiat': ('hiat', 'cast.down'),                             # cast down, descend quickly
        'khapi': ('khapi', 'moon'),                                # moon
        'sinsen': ('sin-sen', 'clear-clear'),                      # clearly, plainly visible
        'seelna': ('seel-na', 'hide-NMLZ'),                        # hiding, concealment
        'seel': ('seel', 'hide'),                                  # hide, conceal
        'lumletin': ('lumlet-in', 'overturn-INST'),                # overturning
        'lumlet': ('lumlet', 'overturn'),                          # overturn, turn over
        'omkhong': ('om-khong', 'exist-still'),                    # stand still, remain
        'hihzawh': ('hih-zawh', 'do-able'),                        # able to do, capable
        'veva': ('ve-va', 'do-INTENS'),                            # do repeatedly, intensely
        'nungzang': ('nung-zang', 'back-part'),                    # back, loins
        # Round 86: KJV-verified vocabulary
        'ciim': ('ciim', 'mire'),                                  # mire, mud, deep water
        'vapite': ('vapi-te', 'stork-PL'),                         # storks
        'vapi': ('vapi', 'stork'),                                 # stork (bird)
        'tehpih': ('teh-pih', 'measure-compare'),                  # compare, liken
        'pakpak': ('pak-pak', 'quick-REDUP'),                      # quickly, suddenly
        'nainai': ('nai-nai', 'near-REDUP'),                       # increasingly, continually
        'tautauna': ('tautau-na', 'groan-NMLZ'),                   # groaning, sighing
        'tautau': ('tautau', 'groan'),                             # groan, sigh
        'biakpih': ('biak-pih', 'worship-also'),                   # worship along with
        'zawhsak': ('zawh-sak', 'able-CAUS'),                      # subdue, make subject
        'khuainun': ('khuainun', 'wax'),                           # wax (melting substance)
        # Round 87: KJV-verified vocabulary
        'kicinna': ('ki-cin-na', 'REFL-perfect-NMLZ'),             # integrity, perfection
        'kiliansakte': ('ki-lian-sak-te', 'REFL-great-CAUS-PL'),   # those who exalt themselves
        'kiliansak': ('ki-lian-sak', 'REFL-great-CAUS'),           # exalt oneself
        'geelgeel': ('geel-geel', 'plan-REDUP'),                   # ponder, meditate, devise
        'cihcih': ('cih-cih', 'say-REDUP'),                        # say repeatedly, continually say
        'thalpi': ('thal-pi', 'bow-great'),                        # bow (weapon)
        'kiuhkeuh': ('ki-uh-keuh', 'REFL-wash-INTENS'),            # thoroughly wash
        'siklukhu': ('sik-lukhu', 'iron-helmet'),                  # helmet, strength of head
        'minthannate': ('minthan-na-te', 'glory-NMLZ-PL'),         # glories, majesties
        'minthanna': ('minthan-na', 'glory-NMLZ'),                 # glory, majesty
        'tehlop': ('teh-lop', 'measure-trap'),                     # trap, snare
        'hatpen': ('hat-pen', 'strong-most'),                      # strongest, mightiest
        'luituite': ('lui-tui-te', 'river-water-PL'),              # rivers, streams
        'luitui': ('lui-tui', 'river-water'),                      # river, stream
        # Round 88: KJV-verified vocabulary
        'teelpa': ('teel-pa', 'choose-NMLZ.M'),                    # chosen one
        'paihsak': ('paih-sak', 'cast-CAUS'),                      # cast away, throw down
        'neikha': ('nei-kha', 'have-?'),                           # consider, know (in heart)
        'huihte': ('huih-te', 'wind-PL'),                          # winds
        'huih': ('huih', 'wind'),                                  # wind
        'muantaak': ('muan-taak', 'trust-ADV'),                    # trustworthy, faithful
        'thuciamnasa': ('thuciamna-sa', 'promise-PRF'),            # vow made, promised
        'pialsak': ('pial-sak', 'stray-CAUS'),                     # cause to stray, lead astray
        'khialhkhak': ('khialh-khak', 'err-fall'),                 # stumble into sin
        'muhtangpi': ('muh-tangpi', 'see.II-before'),              # in sight of, before (eyes)
        'awkna': ('awk-na', 'trap-NMLZ'),                          # trap, snare, slaughter
        'awk': ('awk', 'trap'),                                    # trap, snare
        # Round 89: KJV-verified vocabulary
        'sinkhamna': ('sin-kham-na', 'heart-tight-NMLZ'),          # anguish, distress
        'thungaihsut': ('thu-ngaihsut', 'word-think'),             # understanding, discretion
        'ansalte': ('ansal-te', 'granary-PL'),                     # barns, granaries
        'ansal': ('ansal', 'granary'),                             # barn, granary
        'kihilhnate': ('ki-hilh-na-te', 'PASS-teach-NMLZ-PL'),     # instructions
        'kihilhna': ('ki-hilh-na', 'PASS-teach-NMLZ'),             # instruction
        'paikha': ('pai-kha', 'go-near'),                          # go near, approach
        'lumlum': ('lum-lum', 'lie-REDUP'),                        # sleep deeply, slumber
        'thungaihsun': ('thu-ngaihsun', 'word-think'),             # understanding (variant)
        'awkpih': ('awk-pih', 'trap-APPL'),                        # be trapped, ensnared
        'teiteite': ('teitei-te', 'certain-PL'),                   # certainly (those who)
        'teitei': ('teitei', 'certain'),                           # certainly, surely
        'kipelhna': ('ki-pelh-na', 'REFL-escape-NMLZ'),            # escape, deliverance
        'kipel': ('ki-pelh', 'REFL-escape'),                       # escape
        'nektawm': ('nek-tawm', 'eat.II-little'),                  # food, something to eat
        # Round 90: Final push to 98.6%
        'haitatna': ('haitat-na', 'foolish-NMLZ'),                 # foolishness
        'haitat': ('haitat', 'foolish'),                           # foolish
        'ankuang': ('an-kuang', 'breast-bosom'),                   # bosom
        'thadahpa': ('thadah-pa', 'lazy-NMLZ.M'),                  # sluggard
        'thadah': ('thadah', 'lazy'),                              # lazy, slothful
        'hiathiat': ('hiat-hiat', 'clearly-REDUP'),                # clearly, wisely (speak)
        'thangsiahna': ('thangsiah-na', 'deceive-NMLZ'),           # deceit, snare
        'thangsiah': ('thangsiah', 'deceive'),                     # deceive, trick
        'cikha': ('ci-kha', 'say-PROH'),                           # don't say (prohibitive)
        'zuihnop': ('zuih-nop', 'follow-want'),                    # want to follow
        'niamkhiatna': ('niamkhiat-na', 'humble-NMLZ'),            # humiliation, lowness
        'niamkhiat': ('niamkhiat', 'humble'),                      # humble, low
        'muhthadahhuai': ('muh-thadah-huai', 'see-forgive-NEG'),   # abominable
        'singno': ('sing-no', 'tree-fruit'),                       # orchard, fruit tree
        'bawhkhiat': ('bawh-khiat', 'pluck-off'),                  # pluck up, tear off
        'kidemna': ('ki-dem-na', 'REFL-compete-NMLZ'),             # envy, rivalry
        'kidem': ('ki-dem', 'REFL-compete'),                       # compete, vie
        # Round 91: Push to 98.6%
        'theikhia': ('thei-khia', 'know-out'),                     # find out, understand deeply
        'samphekte': ('samphek-te', 'hair.lock-PL'),               # locks of hair
        'samphek': ('samphek', 'hair.lock'),                       # lock of hair
        'saledi': ('saledi', 'frankincense'),                      # frankincense
        'ngaihnop': ('ngaih-nop', 'hear-want'),                    # want to hear, pleasing
        'heuhna': ('heuh-na', 'prune-NMLZ'),                       # pruning
        'heuh': ('heuh', 'prune'),                                 # prune (plants)
        'lunggimsak': ('lung-gim-sak', 'heart-tire-CAUS'),         # cause grief, weary
        'lungkiatna': ('lung-kiat-na', 'heart-fall-NMLZ'),         # despair, disappointment
        'lungkiat': ('lung-kiat', 'heart-fall'),                   # despair, be disappointed
        'sawk': ('sawk', 'put.hand.into'),                         # put hand into, draw lots
        'mualtungte': ('mual-tung-te', 'mountain-top-PL'),         # mountain tops
        'mualtung': ('mual-tung', 'mountain-top'),                 # mountain top
        'koihpa': ('koih-pa', 'place-NMLZ.M'),                     # one who places, separates
        'piantheih': ('pian-theih', 'happen-able'),                # possible, can happen
        'hunhunin': ('hun-hun-in', 'time-time-INST'),              # every moment, constantly
        'khaukhai': ('khaukhai', 'plumbline'),                     # plumbline, measuring line
        'sasialne': ('sasial-ne', 'prey-NMLZ'),                    # predatory, ravenous
        'sasial': ('sasial', 'prey'),                              # prey, hunt
        # Round 92: Final push to 98.6%
        'niamin': ('niam-in', 'low-INST'),                         # lowly, humbly
        'niam': ('niam', 'low'),                                   # low
        'beisakin': ('bei-sak-in', 'finish-CAUS-INST'),            # destroying, cutting off
        'beisak': ('bei-sak', 'finish-CAUS'),                      # destroy, cut off
        'sawkin': ('sawk-in', 'put.hand.into-INST'),               # reaching into, taking
        'sungte': ('sung-te', 'inside-PL'),                        # chambers, treasuries
        # Round 93: Final push to 98.6%
        'nuhsak': ('nuh-sak', 'apply-CAUS'),                       # apply (plaster)
        'khahkhiatna': ('khah-khiat-na', 'hold-out-NMLZ'),         # deliverance
        'paiziate': ('paizia-te', 'way-PL'),                       # ways
        'paizia': ('paizia', 'way'),                               # way, manner
        'ipcip': ('ip-cip', 'restrain-INTENS'),                    # restrain oneself
        'zapsiang': ('zap-siang', 'winnow-clean'),                 # winnow, cleanse
        'mutna': ('mut-na', 'blow-NMLZ'),                          # alarm (trumpet)
        'mut': ('mut', 'blow'),                                    # blow (trumpet)
        'siacip': ('sia-cip', 'spoil-INTENS'),                     # utterly spoiled
        'delhmang': ('delh-mang', 'chase-away'),                   # fray away, scare off
        'lungmangin': ('lungmang-in', 'dismay-INST'),              # dismayed
        'lungmang': ('lungmang', 'dismay'),                        # dismay
        'thupiteng': ('thu-pi-teng', 'thing-great-all'),           # precious things
        'patauhna': ('patauh-na', 'shout-NMLZ'),                   # shouting, alarm
        'patauh': ('patauh', 'shout'),                             # shout
        'saltang': ('sal-tang', 'slave-person'),                   # captive
        'saltanna': ('saltan-na', 'captive-NMLZ'),                 # captivity
        'saltan': ('saltan', 'captive'),                           # captive
        'neusak': ('neu-sak', 'small-CAUS'),                       # make small
        'kaikhiato': ('kai-khia-to', 'pull-out-up'),               # draw up, pull out
        # Round 94: Push to 99%
        'kalsuan': ('kal-suan', 'step-wide'),                      # enlarge steps
        'amte': ('am-te', 'coal-PL'),                              # coals
        'mate': ('ma-te', 'wound-PL'),                             # wounds
        'atte': ('at-te', 'scribe-PL'),                            # scribes
        'alna': ('al-na', 'cut-NMLZ'),                             # cutting, cutting up
        'kama': ('ka-ma', '1SG.POSS-lip'),                         # my lips
        'khute': ('khu-te', 'fat-PL'),                             # fatlings
        'neikha': ('nei-kha', 'have-NEG'),                         # not have, lack
        'alte': ('al-te', 'beast-PL'),                             # wild beasts
        'leite': ('lei-te', 'earth-PL'),                           # lands, people
        'bawm': ('bawm', 'basket'),                                # basket
        'kithehthangna': ('ki-theh-thang-na', 'REFL-scatter-wide-NMLZ'),  # scattering
        'kihawlkhiatna': ('ki-hawl-khiat-na', 'REFL-drive-out-NMLZ'),     # expulsion
        'hamphatnate': ('hamphat-na-te', 'benefit-NMLZ-PL'),       # benefits
        'kimawhsaknate': ('ki-mawh-sak-na-te', 'REFL-wrong-CAUS-NMLZ-PL'), # wrongs
        'omkhit': ('om-khit', 'be-still'),                         # forbear, be still
        'puanak': ('puan-ak', 'cloth-?'),                          # arm uncovered
        'siathei': ('sia-thei', 'sin-able'),                       # able to sin
        'thudawnna': ('thu-dawn-na', 'word-inquire-NMLZ'),         # inquiry, prophecy
        'leihoihna': ('lei-hoih-na', 'land-good-NMLZ'),            # good soil
        'khangcing': ('khang-cing', 'grow-complete'),              # fully grown
        'tamlawhna': ('tam-lawh-na', 'much-able-NMLZ'),            # abundance
        'thudotin': ('thu-dot-in', 'word-inquire-INST'),           # inquiring
        'phelh': ('phelh', 'kindle'),                              # kindle fire
        'katna': ('kat-na', 'divide-NMLZ'),                        # division, parting
        'mote': ('mo-te', 'shame-PL'),                             # abominations
        'etet': ('et-et', 'desire-REDUP'),                         # desire greatly
        'patausak': ('patauh-sak', 'shout-CAUS'),                  # cause to cry out
        'puanungah': ('puan-ung-ah', 'cloth-inside-LOC'),          # in the chamber
        'biakinntual': ('biakinn-tual', 'temple-court'),           # temple court
        'tehsuk': ('teh-suk', 'measure-knee'),                     # ankle deep
        # Round 95: More vocabulary
        'saki': ('sa-ki', 'animal-horn'),                          # horn, trumpet
        'ciamtehnate': ('ciamteh-na-te', 'waymark-NMLZ-PL'),       # waymarks
        'theihnop': ('theih-nop', 'know-able'),                    # knowable, soothsayer
        'thudotte': ('thu-dot-te', 'word-inquire-PL'),             # wise men
        'kamsia': ('kam-sia', 'mouth-evil'),                       # blasphemy, great words
        'tuamtuamah': ('tuamtuam-ah', 'various-LOC'),              # in various places
        'zawdeuh': ('zaw-deuh', 'more-still'),                     # strengthened more
        'lungkhamhuai': ('lung-kham-huai', 'heart-sorrow-mix'),    # troubled heart
        'naupaiite': ('naupai-i-te', 'infant-FEM-PL'),             # infants
        'deihteng': ('deih-teng', 'want-all'),                     # want all, enough
        'kidosak': ('ki-do-sak', 'REFL-fight-CAUS'),               # set against
        'khutzaw': ('khut-zaw', 'hand-shrivel'),                   # palsy
        'valin': ('val-in', 'mile-INST'),                          # by mile, twain
        'lutthei': ('lut-thei', 'enter-able'),                     # able to enter
        'puanbek': ('puan-bek', 'cloth-piece'),                    # piece of cloth
        'thulang': ('thu-lang', 'word-reveal'),                    # reveal, make known
        'lingbulsum': ('lingbul-sum', 'thorn-three'),              # thorns (thick)
        'munuam': ('mun-uam', 'place-pleasant'),                   # pleasant place
        'cit': ('cit', 'eye'),                                     # eye (variant)
        'khenkhit': ('khen-khit', 'condemn-finish'),               # condemn
        'khohsa': ('khoh-sa', 'invite-NMLZ'),                      # invitation, bidding
        'luttheih': ('lut-theih', 'enter-able'),                   # able to enter
        'kineihkhemna': ('ki-neih-khem-na', 'REFL-possess-all-NMLZ'), # hypocrisy
        'zakhin': ('za-khin', 'hundred-more'),                     # multitude
        'amauteng': ('amau-teng', '3PL-all'),                      # they themselves
        'sumpi': ('sum-pi', 'money-great'),                        # much money
        'nulsak': ('nul-sak', 'wet-CAUS'),                         # wash, wet
        'khahkhiat': ('khah-khiat', 'bind-out'),                   # loose, unbind
        'lakthei': ('lak-thei', 'take-able'),                      # able to take
        'khentheih': ('khen-theih', 'judge-able'),                 # authority to judge
        'laigelh': ('lai-gelh', 'writing-write'),                  # writings
        'thongcingte': ('thong-cing-te', 'prison-guard-PL'),       # prison keepers
        'nekloh': ('nek-loh', 'eat-NEG'),                          # abstain from
        'gamdaih': ('gam-daih', 'land-flat'),                      # open place
        'thahsawmna': ('thah-sawm-na', 'kill-plan-NMLZ'),          # lying in wait
        'sikkawipi': ('sikka-wi-pi', 'wind-blow-great'),           # strong wind
        'sikhin': ('sik-hin', 'dead-already'),                     # already dead
        'suakthei': ('suak-thei', 'become-able'),                  # sanctified
        'pautheih': ('pau-theih', 'speak-able'),                   # able to speak
        'cingtaaksak': ('cing-taak-sak', 'complete-true-CAUS'),    # fill completely
        'vankim': ('van-kim', 'sky-all'),                          # in the clouds
        'cingtaakin': ('cing-taak-in', 'complete-true-INST'),      # consecrated
        'nambat': ('nam-bat', 'name-number'),                      # number, count
        # Round 96: More vocabulary for 99%
        'bokvakte': ('bok-vak-te', 'creep-creature-PL'),           # creeping things
        'satak': ('sa-tak', 'flesh-piece'),                        # rib, piece of flesh
        'ngiansiam': ('ngian-siam', 'cunning-make'),               # subtil, crafty
        'kilangneihna': ('ki-lang-neih-na', 'REFL-appear-have-NMLZ'), # enmity
        'khangkhang': ('khang-khang', 'increase-REDUP'),           # exceedingly
        'mukah': ('mu-kah', 'see-mouth'),                          # in the mouth (dove)
        'khansung': ('khan-sung', 'generation-inside'),            # in the days of
        'samsiate': ('sam-sia-te', 'bless-curse-PL'),              # curses
        'kipawlpihte': ('ki-pawl-pih-te', 'REFL-group-join-PL'),   # confederates
        'giatte': ('giat-te', 'train-PL'),                         # trained servants
        'mimkhau': ('mim-khau', 'thread-fine'),                    # thread
        'khuadaktoh': ('khua-dak-toh', 'village-sudden-arrive'),   # suddenly arrived
        'kimawhsakna': ('ki-mawh-sak-na', 'REFL-wrong-CAUS-NMLZ'), # sin, wrongdoing
        'lungka': ('lung-ka', 'heart-edge'),                       # lingered, hesitated
        'sawlbawk': ('sawl-bawk', 'cast-throw'),                   # cast away
        'tehkhia': ('teh-khia', 'measure-out'),                    # weighed out
        'leihawmte': ('lei-hawm-te', 'land-possess-PL'),           # possessions
        'betna': ('bet-na', 'faint-NMLZ'),                         # faintness
        'khuamin': ('khua-min', 'village-morning'),                # early morning
        'vomte': ('vom-te', 'brown-PL'),                           # brown ones
        'ngasak': ('nga-sak', 'face-CAUS'),                        # set face toward
        'zawnin': ('zawn-in', 'pursue-INST'),                      # pursuing
        'kamkhum': ('kam-khum', 'mouth-hold'),                     # speak kindly
        'taikhiatna': ('tai-khiat-na', 'flee-out-NMLZ'),           # fleeing, escape
        'sangsakin': ('sang-sak-in', 'lift-CAUS-INST'),            # lifting up
        'khiathei': ('khiat-thei', 'interpret-able'),              # interpreter
        'hoihlam': ('hoih-lam', 'good-side'),                      # good interpretation
        'khailum': ('khai-lum', 'hang-round'),                     # hanged
        'kihauh': ('ki-hauh', 'REFL-appoint'),                     # appoint
        'kikoihcing': ('ki-koih-cing', 'REFL-store-complete'),     # stored up
        'enen': ('en-en', 'look-REDUP'),                           # looking at each other
        'dotnate': ('dot-na-te', 'ask-NMLZ-PL'),                   # inquiries
        'nekkhawm': ('nek-khawm', 'eat-together'),                 # eating together
        'puakzawh': ('puak-zawh', 'fill-finish'),                  # filled up
        'dangteng': ('dang-teng', 'other-all'),                    # the rest, others
        'ciahkiksak': ('ciah-kik-sak', 'return-again-CAUS'),       # send back
        'thumantak': ('thu-man-tak', 'word-true-real'),            # truly, kindly
        'sattat': ('sat-tat', 'cut-cut'),                          # slew, killed
        'noptuak': ('nop-tuak', 'good-pleasant'),                  # pleasant, good
        'cihsak': ('cih-sak', 'say-CAUS'),                         # made to swear
        'khoisak': ('khoi-sak', 'call-CAUS'),                      # call to, summon
        'sapsak': ('sap-sak', 'suckle-CAUS'),                      # nurse
        'anthul': ('an-thul', 'grain-smitten'),                    # smitten grain
        'nekzah': ('nek-zah', 'eat-amount'),                       # eating portion
        'sawlkhiat': ('sawl-khiat', 'send-out'),                   # send out
        'lingcip': ('ling-cip', 'sorrow-INTENS'),                  # deep sorrow
        'vamimte': ('vamim-te', 'quail-PL'),                       # quails
        'khom': ('khom', 'place'),                                 # place, abide
        'paisuakzo': ('pai-suak-zo', 'go-out-able'),               # able to go out
        # Round 97: More vocabulary for 99%
        'anlakna': ('an-lak-na', 'grain-take-NMLZ'),               # firstfruits
        'langneih': ('lang-neih', 'appear-have'),                  # countenance
        'dikpa': ('dik-pa', 'right-NMLZ'),                         # righteous one
        'khaudum': ('khau-dum', 'edge-border'),                    # selvedge, edge
        'sawmlite': ('sawm-li-te', 'ten-four-PL'),                 # forties
        'pangkhat': ('pang-khat', 'side-one'),                     # one side
        'agate': ('agate', 'agate'),                               # agate (gemstone)
        'amethyst': ('amethyst', 'amethyst'),                      # amethyst (gemstone)
        'siklong': ('sik-long', 'hem-round'),                      # hem round about
        'kikipsakna': ('ki-kip-sak-na', 'REFL-wave-CAUS-NMLZ'),    # wave offering
        'kitatkhiatna': ('ki-tat-khiat-na', 'REFL-count-out-NMLZ'), # ransom
        'sawhin': ('sawh-in', 'compound-INST'),                    # confection
        'lelhna': ('lelh-na', 'overcome-NMLZ'),                    # being overcome
        'valteng': ('val-teng', 'share-all'),                      # all portions
        'kibuakna': ('ki-buak-na', 'REFL-pour-NMLZ'),              # pouring out
        'khamtheih': ('kham-theih', 'forbid-able'),                # forbidden
        'sanhuai': ('san-huai', 'accept-mix'),                     # accepted
        'bak': ('bak', 'bat'),                                     # bat
        'sian': ('sian', 'purify'),                                # purifying
        'thukzawk': ('thuk-zawk', 'deep-more'),                    # somewhat dark
        'mualin': ('mual-in', 'hill-INST'),                        # somewhat dark
        'lutol': ('lu-tol', 'head-bald'),                          # bald head
        'daihna': ('daih-na', 'bear-NMLZ'),                        # bearing
        'vakto': ('vak-to', 'walk-go'),                            # go up and down
        'sitbaanna': ('sit-baan-na', 'blemish-none-NMLZ'),         # without blemish
        'sawmngana': ('sawm-nga-na', 'ten-five-NMLZ'),             # fiftieth
        'gawpgawpna': ('gawp-gawp-na', 'rigor-REDUP-NMLZ'),        # rigour
        'khualmipa': ('khualmi-pa', 'stranger-NMLZ'),              # sojourner
        'zawnglua': ('zawng-lua', 'means-poor'),                   # poorer than
        'honhonin': ('hon-hon-in', 'count-REDUP-INST'),            # numbering
        'kitatna': ('ki-tat-na', 'REFL-count-NMLZ'),               # ransom
        'behtangun': ('beh-tang-un', 'beside-stand-3PL'),          # under the hand
        'palhngulh': ('palh-ngulh', 'trespass-aside'),             # go aside
        'saangin': ('saang-in', 'make-INST'),                      # fashioned
        'nawine': ('nawi-ne', 'nursing-child'),                    # sucking child
        'malzah': ('mal-zah', 'bless-amount'),                     # number
        'hawmthawh': ('hawm-thawh', 'bring-near'),                 # brought near
        'ulianin': ('ulian-in', 'prince-INST'),                    # as a prince
        'hingtangun': ('hing-tang-un', 'live-stand-3PL'),          # went down alive
        'vute': ('vu-te', 'ash-PL'),                               # ashes
        'kilahna': ('ki-lah-na', 'REFL-strive-NMLZ'),              # striving
        'nawksuak': ('nawk-suak', 'smite-out'),                    # smote out
        'linggawp': ('ling-gawp', 'sorrow-INTENS'),                # sore distressed
        'khantawnin': ('khan-tawn-in', 'time-meet-INST'),          # ever since
        'gamsial': ('gam-sial', 'land-strong'),                    # unicorn strength
        'kihilna': ('ki-hil-na', 'REFL-teach-NMLZ'),               # enchantments
        'suaktate': ('suak-ta-te', 'become-PAST-PL'),              # those who came
        'khasim': ('kha-sim', 'month-sweet'),                      # sweet savour
        'ciampel': ('ciam-pel', 'vow-break'),                      # break vow
        'lumkhawmsa': ('lum-khawm-sa', 'lie-together-PAST'),       # lying with
        'nungaknote': ('nungak-no-te', 'virgin-child-PL'),         # women children
        'sumang': ('su-mang', 'destroy-scatter'),                  # destroy
        'behbeh': ('beh-beh', 'count-REDUP'),                      # number
        'thatkha': ('that-kha', 'kill-accidental'),                # unawares, accidental
        'khutun': ('khu-tun', 'hand-carry'),                       # in hands
        'thahatnate': ('tha-hat-na-te', 'strength-great-NMLZ-PL'), # mighty acts
        'khuadakto': ('khua-dak-to', 'place-sudden-arrive'),       # get up to
        'genteng': ('gen-teng', 'speak-all'),                      # speak all
        'niamkhiatin': ('niam-khiat-in', 'low-out-INST'),          # pine away
        'sangpente': ('sang-pen-te', 'high-most-PL'),              # heavens
        'teelzaw': ('teel-zaw', 'choose-more'),                    # chose above
        'kizahtakna': ('ki-zahtak-na', 'REFL-fear-NMLZ'),          # fear, dread
        'thuahte': ('thuah-te', 'offer-PL'),                       # offerings
        'khong': ('khong', 'enchanter'),                           # enchanter
        'sikha': ('sikha', 'wizard'),                              # wizard
        # Round 98: More vocabulary for 99%
        'cinte': ('cin-te', 'nail-PL'),                            # nails
        'kidongsa': ('ki-dong-sa', 'REFL-betroth-PAST'),           # betrothed
        'apkik': ('ap-kik', 'deliver-return'),                     # deliver back
        'suangtumpite': ('suangtum-pi-te', 'stone-great-PL'),      # great stones
        'cikzethuai': ('cik-ze-thuai', 'flee-seven-scatter'),      # flee seven ways
        'lungham': ('lung-ham', 'heart-anger'),                    # anger, wrath
        'khansauna': ('khan-sau-na', 'time-long-NMLZ'),            # length of days
        'cimawhsak': ('ci-mawh-sak', 'fear-wrong-CAUS'),           # fail, forsake
        'mitnauta': ('mit-nau-ta', 'eye-child-PAST'),              # apple of eye
        'saklam': ('sak-lam', 'side-direction'),                   # toward
        'ankan': ('an-kan', 'grain-old'),                          # old corn
        'puanhoih': ('puan-hoih', 'cloth-good'),                   # goodly garment
        'paatsa': ('paat-sa', 'old-PAST'),                         # old, worn
        'paitohna': ('pai-toh-na', 'go-arrive-NMLZ'),              # arrival, way
        'cipin': ('cip-in', 'stand-INST'),                         # standing
        'beisiang': ('bei-siang', 'finish-clean'),                 # consumed
        'kuankhiatna': ('kuan-khiat-na', 'strength-out-NMLZ'),     # going out
        'neulua': ('neu-lua', 'small-too'),                        # too narrow
        'lononate': ('lono-na-te', 'pasture-NMLZ-PL'),             # suburbs
        'antah': ('an-tah', 'thorn-side'),                         # thorns
        'khansak': ('khan-sak', 'time-CAUS'),                      # raised up
        'khualzinte': ('khualzin-te', 'traveler-PL'),              # travellers
        'ciangciang': ('ciang-ciang', 'until-REDUP'),              # completely
        'pausak': ('pau-sak', 'speak-CAUS'),                       # cause to speak
        'sinsak': ('sin-sak', 'prove-CAUS'),                       # prove, test
        'khade': ('kha-de', 'ornament-PL'),                        # ornaments
        'bilbah': ('bil-bah', 'ear-ring'),                         # earrings
        'naihuai': ('nai-huai', 'near-mix'),                       # inclined
        'niamkoih': ('niam-koih', 'low-put'),                      # brought low
        'zawn': ('zawn', 'why'),                                   # wherefore
        'lampialin': ('lam-pial-in', 'way-turn-INST'),             # turning aside
        'ummawh': ('um-mawh', 'be-without'),                       # without want
        'puteekpa': ('puteek-pa', 'old.man-NMLZ'),                 # old man
        'nungakno': ('nungak-no', 'virgin-child'),                 # young virgin
        'pailam': ('pai-lam', 'go-direction'),                     # direction
        'tanaupa': ('tanau-pa', 'relative-NMLZ'),                  # kinsman
        'thaneemte': ('tha-neem-te', 'strength-weak-PL'),          # weak ones
        'sangtosak': ('sang-to-sak', 'high-up-CAUS'),              # lift up
        'kikhiasuk': ('ki-khia-suk', 'REFL-out-down'),             # fall down
        'beelpi': ('beel-pi', 'pot-great'),                        # caldron
        'palai': ('palai', 'mediator'),                            # mediator, judge
        'apkhapna': ('ap-khap-na', 'give-close-NMLZ'),             # secret parts
        'thukhenin': ('thu-khen-in', 'word-judge-INST'),           # judging
        'sumnen': ('sum-nen', 'money-part'),                       # part of shekel
        'innkhumzanga': ('inn-khum-zang-a', 'house-top-side-LOC'), # top of house
        'theisa': ('thei-sa', 'know-PAST'),                        # knew before
        'sawltheih': ('sawl-theih', 'send-able'),                  # able to send
        'leengkai': ('leeng-kai', 'yoke-pull'),                    # yoke of oxen
        'hamu': ('hamu', 'file'),                                  # file (tool)
        'ciangka': ('ciang-ka', 'way-edge'),                       # passage
        'zuito': ('zui-to', 'follow-up'),                          # come up
        'vattuk': ('vat-tuk', 'climb-up'),                         # climbed up
        'muaimuai': ('muai-muai', 'melt-REDUP'),                   # melted away
        'luhsak': ('luh-sak', 'spoil-CAUS'),                       # spoiled
        'lukham': ('lu-kham', 'head-cover'),                       # pillow, bolster
        'muitum': ('mui-tum', 'shoot-mark'),                       # shoot at mark
        'nawhtat': ('nawh-tat', 'smite-cut'),                      # weapon, sword
        'munmuanhuaina': ('mun-muan-huai-na', 'place-safe-mix-NMLZ'), # stronghold
        'tunkhitna': ('tun-khit-na', 'enter-shut-NMLZ'),           # shut in
        'sukhalo': ('su-kha-lo', 'destroy-NEG-EMPH'),              # shall not find
        # Round 99: More vocabulary for 99%
        'lukhung': ('lu-khung', 'head-pillow'),                    # bolster
        'gamtatkha': ('gam-tat-kha', 'land-cut-off'),              # erred, played fool
        'thaltawite': ('thal-tawi-te', 'bow-shoot-PL'),            # archers
        'zaptel': ('zap-tel', 'swift-quick'),                      # swifter
        'pusuahna': ('pu-suah-na', 'deceive-out-NMLZ'),            # deceiving
        'miliante': ('mi-lian-te', 'person-great-PL'),             # great men
        'angawina': ('an-gawi-na', 'stone-grind-NMLZ'),            # millstone
        'luate': ('lua-te', 'shame-PL'),                           # shames, fools
        'banglel': ('bang-lel', 'like-only'),                      # why should
        'mualpangah': ('mual-pang-ah', 'hill-side-LOC'),           # on hillside
        'teelsak': ('teel-sak', 'choose-CAUS'),                    # let choose
        'vaikhakna': ('vai-khak-na', 'command-charge-NMLZ'),       # charge, command
        'siamgante': ('siam-gan-te', 'weave-work-PL'),             # weavers
        'siamlawngpi': ('siam-lawng-pi', 'weave-beam-great'),      # weaver's beam
        'thangte': ('thang-te', 'snare-PL'),                       # snares
        'kaai': ('kaai', 'tender.grass'),                          # tender grass
        'tutungin': ('tu-tung-in', 'now-arrive-INST'),             # at this time
        'tuidawnin': ('tui-dawn-in', 'water-drink-INST'),          # drinking
        'tehzawh': ('teh-zawh', 'measure-finish'),                 # exceeding
        'vanpua': ('van-pua', 'burden-bear'),                      # burden bearer
        'innkam': ('inn-kam', 'house-chamber'),                    # chamber
        'nanna': ('nan-na', 'narrow-NMLZ'),                        # narrowed
        'innkamte': ('inn-kam-te', 'house-chamber-PL'),            # chambers
        'umgah': ('um-gah', 'be-open'),                            # open flowers
        'nannate': ('nan-na-te', 'narrow-NMLZ-PL'),                # undersetters
        'awnsak': ('awn-sak', 'incline-CAUS'),                     # incline
        'thupina': ('thu-pi-na', 'word-great-NMLZ'),               # integrity
        'hihzaw': ('hih-zaw', 'this-more'),                        # more than this
        'hoihzawk': ('hoih-zawk', 'good-more'),                    # better
        'tuinakah': ('tui-na-kah', 'water-spring-LOC'),            # at spring
        'ngaklai': ('ngak-lai', 'wait-still'),                     # wait for
        'maangte': ('maang-te', 'eunuch-PL'),                      # eunuchs
        'phelkek': ('phel-kek', 'break-INTENS'),                   # break thoroughly
        'suangseekte': ('suang-seek-te', 'stone-hew-PL'),          # hewers of stone
        'nenniamna': ('nen-niam-na', 'face-low-NMLZ'),             # beseeching
        'zuautatna': ('zuau-tat-na', 'conspiracy-cut-NMLZ'),       # conspiracy
        'siakhawm': ('sia-khawm', 'dung-eat'),                     # eat dung
        'geelkholhsa': ('geel-kholh-sa', 'plan-declare-PAST'),     # formed long ago
        'nakpheh': ('nak-pheh', 'nose-hook'),                      # hook in nose
        'khituite': ('khi-tui-te', 'eye-water-PL'),                # tears
        'zindo': ('zin-do', 'journey-treasure'),                   # treasures
        'dawibiakna': ('dawi-biak-na', 'idol-worship-NMLZ'),       # idolatry, high places
        'hante': ('han-te', 'bone-PL'),                            # bones
        'zawngpente': ('zawng-pen-te', 'poor-most-PL'),            # poorest
        'omzawh': ('om-zawh', 'be-finish'),                        # came to pass
        'mualkuam': ('mual-kuam', 'hill-brook'),                   # brooks
        'thuahin': ('thuah-in', 'spread-INST'),                    # spreading
        'nengniamsak': ('neng-niam-sak', 'face-low-CAUS'),         # reproved
        'nilhte': ('nilh-te', 'anoint-PL'),                        # anointed ones
        'thuzawh': ('thu-zawh', 'word-finish'),                    # prevailed
        'zatte': ('zat-te', 'jewel-PL'),                           # precious stones
        'tokhomah': ('tok-hom-ah', 'room-place-LOC'),              # in room of
        'buaisak': ('buai-sak', 'vex-CAUS'),                       # vexed
        'zawsak': ('zaw-sak', 'strong-CAUS'),                      # strengthen
        'puantualpite': ('puan-tual-pi-te', 'cloth-court-great-PL'), # robes
        'tok': ('tok', 'stir'),                                    # stirred up
        'liamnate': ('liam-na-te', 'wound-NMLZ-PL'),               # wounds
        # Round 100: More vocabulary for 99%
        'vangah': ('vang-ah', 'gate-LOC'),                         # at the gate
        'uuk': ('uuk', 'husbandry'),                               # husbandry
        'sumit': ('sum-it', 'lamp-put.out'),                       # put out lamps
        'puahsiang': ('puah-siang', 'gather-clean'),               # cleanse
        'zuansak': ('zuan-sak', 'gather-CAUS'),                    # gather
        'lunghihmawhpih': ('lung-hih-mawh-pih', 'heart-nothing-wrong-also'), # nothing to do with
        'losapte': ('lo-sap-te', 'tribute-pay-PL'),                # tribute payers
        'suaksa': ('suak-sa', 'become-PAST'),                      # captivity
        'tanna': ('tan-na', 'fast-NMLZ'),                          # fasting
        'maavanna': ('maavan-na', 'bondage-NMLZ'),                 # bondage
        'vakkhia': ('vak-khia', 'walk-out'),                       # arose, went out
        'zaipi': ('zai-pi', 'work-great'),                         # great work
        'pama': ('pa-ma', 'hundred-also'),                         # hundred also
        'tualpi': ('tual-pi', 'street-great'),                     # broad street
        'simkhia': ('sim-khia', 'read-out'),                       # read aloud
        'khupna': ('khup-na', 'assemble-NMLZ'),                    # assembly
        'ukgawp': ('uk-gawp', 'rule-INTENS'),                      # dominion
        'pengsak': ('peng-sak', 'spare-CAUS'),                     # spare
        'zunekna': ('zu-nek-na', 'wine-eat-NMLZ'),                 # feast
        'kisimmawhna': ('ki-sim-mawh-na', 'REFL-shame-wrong-NMLZ'), # contempt
        'kithuh': ('ki-thuh', 'REFL-seal'),                        # sealed
        'patsa': ('pat-sa', 'begin-PAST'),                         # had begun
        'thupite': ('thu-pi-te', 'word-great-PL'),                 # decrees
        'hawkna': ('hawk-na', 'roar-NMLZ'),                        # roaring
        'suktansak': ('suk-tan-sak', 'break-stand-CAUS'),          # broken
        'lunggimna': ('lung-gim-na', 'heart-grief-NMLZ'),          # grief
        'aktui': ('ak-tui', 'egg-water'),                          # egg white
        'tuikhal': ('tui-khal', 'water-freeze'),                   # ice
        'lunggulhin': ('lung-gulh-in', 'heart-desire-INST'),       # earnestly desire
        'sincip': ('sin-cip', 'seal-INTENS'),                      # sealed up
        'beipak': ('bei-pak', 'finish-swift'),                     # swifter
        'dingpi': ('ding-pi', 'stand-great'),                      # unprofitable
        'musanete': ('mu-sane-te', 'see-bread-PL'),                # wandering for bread
        'kahkahna': ('kah-kah-na', 'weep-REDUP-NMLZ'),             # weeping
        'langbawl': ('lang-bawl', 'appear-turn'),                  # turned against
        'suktheih': ('suk-theih', 'break-able'),                   # persecute
        'thamante': ('tha-man-te', 'labor-true-PL'),               # labours
        'cihtheih': ('cih-theih', 'say-able'),                     # sufficiency
        'lungtom': ('lung-tom', 'heart-troubled'),                 # troubled spirit
        'silhloin': ('silh-lo-in', 'clothe-NEG-INST'),             # without clothing
        'toncip': ('ton-cip', 'wet-INTENS'),                       # wet through
        'pelhna': ('pelh-na', 'depart-NMLZ'),                      # departing
        'limun': ('li-mun', 'hide-self'),                          # hid themselves
        'ninbulom': ('nin-bu-lom', 'mire-dust-mix'),               # dust and ashes
        'kikoihsa': ('ki-koih-sa', 'REFL-appoint-PAST'),           # appointed
        'thuhkik': ('thuh-kik', 'portion-return'),                 # portion
        'zawhthawh': ('zawh-thawh', 'terror-bring'),               # terror
        'hihkik': ('hih-kik', 'this-again'),                       # oftentimes
        'velvel': ('vel-vel', 'hold-REDUP'),                       # hold peace
        'kiphatsaknate': ('ki-phat-sak-na-te', 'REFL-praise-CAUS-NMLZ-PL'), # transgressions
        'theikim': ('thei-kim', 'see-all'),                        # see it
        # Round 101: More vocabulary for 99%
        'lamdangsak': ('lam-dang-sak', 'way-different-CAUS'),      # respect, fear
        'sinkhiat': ('sin-khiat', 'shake-out'),                    # shaken out
        'khamcip': ('kham-cip', 'withhold-INTENS'),                # withheld
        'zap': ('zap', 'flutter'),                                 # flutter, stir
        'sasi': ('sa-si', 'blood-suck'),                           # suck blood
        'zahval': ('zah-val', 'enough-share'),                     # more than enough
        'genkha': ('gen-kha', 'speak-already'),                    # have spoken
        'bangzahta': ('bang-zah-ta', 'like-much-PAST'),            # lo now
        'gialhek': ('gial-hek', 'tree-shade'),                     # shady trees
        'hate': ('ha-te', 'tooth-PL'),                             # teeth
        'nisuak': ('ni-suak', 'sneeze-out'),                       # sneezing
        'nip': ('nip', 'rotten'),                                  # rotten
        'kitamte': ('ki-tam-te', 'REFL-sharp-PL'),                 # sharp things
        'citheisakkik': ('ci-thei-sak-kik', 'return-able-CAUS-again'), # turned captivity
        'siamang': ('siam-ang', 'make-wisdom'),                    # be wise
        'leengtui': ('leeng-tui', 'corn-wine'),                    # corn and wine
        'thahnopna': ('thah-nop-na', 'kill-like-NMLZ'),            # deceitful
        'kibawlphat': ('ki-bawl-phat', 'REFL-make-ready'),         # made ready
        'lelna': ('lel-na', 'fear-NMLZ'),                          # fear
        'kihotkhiatna': ('ki-hot-khiat-na', 'REFL-deliver-out-NMLZ'), # deliverance
        'phattaak': ('phat-taak', 'praise-worthy'),                # worthy of praise
        'zamin': ('za-min', 'hundred-thousand'),                   # many
        'lungmuan': ('lung-muan', 'heart-secure'),                 # secure heart
        'kikoko': ('ki-ko-ko', 'REFL-cry-REDUP'),                  # cried out
        'khuailuzu': ('khuai-lu-zu', 'honey-head-sweet'),          # honeycomb
        'dingtang': ('ding-tang', 'stand-upright'),                # stand upright
        'lungno': ('lung-no', 'heart-worm'),                       # worm
        'khasia': ('kha-sia', 'face-hide'),                        # hide face
        'khuisatna': ('khui-sat-na', 'sigh-NMLZ'),                 # sighing
        'tuithukpite': ('tui-thuk-pi-te', 'water-deep-great-PL'),  # deep waters
        'mitheek': ('mi-theek', 'person-wrong'),                   # wrongfully
        'tawnna': ('tawn-na', 'reproof-NMLZ'),                     # reproofs
        'gentham': ('gen-tham', 'speak-hand'),                     # handbreadth
        'nuihsatin': ('nuih-sat-in', 'reproach-NMLZ-INST'),        # reproach
        'vuakna': ('vuak-na', 'blow-NMLZ'),                        # blow, stroke
        'lungnop': ('lung-nop', 'heart-rest'),                     # recover
        'khakunkun': ('kha-kun-kun', 'face-cast.down-REDUP'),      # cast down
        'tuizeu': ('tui-zeu', 'water-deep'),                       # deep water
        'khangualte': ('khan-gual-te', 'time-fellow-PL'),          # fellows
        'ciangkik': ('ciang-kik', 'good-again'),                   # good pleasure
        'keutumsak': ('keu-tum-sak', 'melt-finish-CAUS'),          # melt away
        'sikcipsak': ('sik-cip-sak', 'tread-INTENS-CAUS'),         # tread down
        'guhngek': ('guh-ngek', 'bless-long'),                     # bless while live
        'gallauna': ('gal-lau-na', 'enemy-fear-NMLZ'),             # fear of enemy
        'kuakte': ('kuak-te', 'furrow-PL'),                        # furrows
        'zaktheih': ('zak-theih', 'hear-able'),                    # gave ear
        'sawtpek': ('sawt-pek', 'long-very'),                      # ancient times
        'khuaphialepte': ('khua-phialep-te', 'sky-lightning-PL'),  # lightnings
        'guntuite': ('gun-tui-te', 'river-water-PL'),              # rivers, floods
        'hinkhawi': ('hing-khawi', 'live-spare'),                  # spared life
        'etsak': ('et-sak', 'look-CAUS'),                          # look upon
        # Round 102: More vocabulary for 99%
        'nungtasakkik': ('nung-ta-sak-kik', 'live-again-CAUS-again'), # revive again
        'thuhilhpa': ('thu-hilh-pa', 'word-teach-NMLZ'),           # teacher, former
        'kawina': ('kawi-na', 'wicked-NMLZ'),                      # wickedness
        'tuidawnte': ('tui-dawn-te', 'water-drink-PL'),            # those drinking
        'paatkhia': ('paat-khia', 'wax.old-out'),                  # wax old
        'muala': ('mual-a', 'hill-LOC'),                           # on the hill
        'muamua': ('mua-mua', 'many-REDUP'),                       # innumerable
        'kaikhawmkik': ('kai-khawm-kik', 'pull-together-again'),   # gather again
        'sumbawl': ('sum-bawl', 'business-do'),                    # do business
        'sunsunte': ('sun-sun-te', 'extort-REDUP-PL'),             # extortioners
        'tuiphih': ('tui-phih', 'water-cup'),                      # cup
        'tuhte': ('tuh-te', 'sow-PL'),                             # those who sow
        'duhgawh': ('duh-gawh', 'desire-evil'),                    # evil desire
        'tungsuk': ('tung-suk', 'upon-swift'),                     # swiftly
        'thugentehnate': ('thu-gen-teh-na-te', 'word-speak-dark-NMLZ-PL'), # dark sayings
        'pialkha': ('pial-kha', 'turn-already'),                   # turn aside
        'sinnamon': ('sinnamon', 'cinnamon'),                      # cinnamon
        'citeng': ('ci-teng', 'corner-all'),                       # every corner
        'neihlelam': ('neih-le-lam', 'have-also-direction'),       # inherit
        'khemzawh': ('khem-zawh', 'all-finish'),                   # completely
        'nungzangah': ('nungzang-ah', 'back-LOC'),                 # on the back
        'hikha': ('hi-kha', 'this-way'),                           # this way
        'thuzak': ('thu-zak', 'word-believe'),                     # believe word
        'zaknophuai': ('zak-nop-huai', 'hear-pleasant-mix'),       # sweetness
        'taanna': ('taan-na', 'cover-NMLZ'),                       # covering
        'hoihpenin': ('hoih-pen-in', 'good-most-INST'),            # best
        'pat': ('pat', 'stroke'),                                  # strokes
        'vawhte': ('vawh-te', 'iniquity-PL'),                      # iniquities
        'tutpih': ('tut-pih', 'sit-with'),                         # sit with
        'thakhauhna': ('tha-kauh-na', 'strength-strong-NMLZ'),     # strength
        'tuivot': ('tui-vot', 'water-cold'),                       # cold water
        'leengsuk': ('leeng-suk', 'bird-fly'),                     # bird flying
        'tungthama': ('tung-thama', 'rebuke-after'),               # rebuke after
        'hoihzawkna': ('hoih-zawk-na', 'good-more-NMLZ'),          # preeminence
        'hamphat': ('ham-phat', 'what-benefit'),                   # what benefit
        'paaksak': ('paak-sak', 'white-CAUS'),                     # make white
        'hithiatna': ('hi-thiat-na', 'this-leave-NMLZ'),           # yielding
        'taangte': ('taang-te', 'star-PL'),                        # stars
        'gamlumnate': ('gam-lum-na-te', 'land-sound-NMLZ-PL'),     # sounds
        'hiuhiau': ('hiu-hiau', 'black-REDUP'),                    # black
        'biang': ('biang', 'cheek'),                               # cheeks
        'suknawi': ('suk-nawi', 'break-charge'),                   # charge, adjure
        'sakhitalno': ('sakhital-no', 'hart-young'),               # young hart
        'itluat': ('it-luat', 'love-exceed'),                      # my love
        'nard': ('nard', 'spikenard'),                             # spikenard
        'kiuh': ('kiuh', 'knock'),                                 # knock
        'pona': ('po-na', 'garden-NMLZ'),                          # garden bed
        'phelhzo': ('pelh-zo', 'quench-able'),                     # able to quench
        'lingsakgawp': ('ling-sak-gawp', 'shake-CAUS-INTENS'),     # shake terribly
        'theihkim': ('theih-kim', 'know-all'),                     # famous, renown
        'etsuk': ('et-suk', 'look-down'),                          # look unto
        # Round 103: More vocabulary for 99%
        'veilama': ('vei-lam-a', 'left-side-LOC'),                 # on the left
        'sinsan': ('sin-san', 'shake-shake'),                      # shake hand
        'sitlai': ('sit-lai', 'shake-over'),                       # shake over
        'singliim': ('sing-liim', 'tree-shade'),                   # shadow
        'zaai': ('zaai', 'languish'),                              # languish
        'khialhpih': ('khialh-pih', 'deceive-also'),               # deceived
        'tangguak': ('tang-guak', 'bare-foot'),                    # barefoot
        'khenkip': ('khen-kip', 'nail-fasten'),                    # nail fastened
        'beimangsak': ('bei-mang-sak', 'finish-away-CAUS'),        # swallow up
        'suahsakna': ('suah-sak-na', 'shoot-CAUS-NMLZ'),           # shooting forth
        'kummin': ('kummin', 'cummin'),                            # cummin
        'themte': ('them-te', 'scrape-PL'),                        # scrapings
        'laidal': ('lai-dal', 'leaf-fall'),                        # falling leaf
        'sehnelte': ('sehnel-te', 'spring-PL'),                    # springs
        'thukpenna': ('thuk-pen-na', 'deep-most-NMLZ'),            # height
        'zakzak': ('zak-zak', 'hear-REDUP'),                       # cry out
        'khutsiampa': ('khut-siam-pa', 'hand-make-NMLZ'),          # craftsman
        'awngthawl': ('awng-thawl', 'create-establish'),           # established
        'uang': ('uang', 'lavish'),                                # lavish
        'tungvat': ('tung-vat', 'upon-fall'),                      # fall upon
        'lausakzo': ('lau-sak-zo', 'fear-CAUS-able'),              # able to prevail
        'hihlohna': ('hih-loh-na', 'this-NEG-NMLZ'),               # treachery
        'tengsakkik': ('teng-sak-kik', 'establish-CAUS-again'),    # establish again
        'kimakna': ('ki-mak-na', 'REFL-divorce-NMLZ'),             # divorcement
        'kapte': ('kap-te', 'shoot-PL'),                           # shooters
        'silhlo': ('silh-lo', 'clothe-NEG'),                       # not clothe
        'thumthum': ('thum-thum', 'mourn-REDUP'),                  # mourn sore
        'neupente': ('neu-pen-te', 'small-most-PL'),               # smallest
        'kepsak': ('kep-sak', 'feed-CAUS'),                        # feed flocks
        'suhna': ('suh-na', 'robbery-NMLZ'),                       # robbery
        'gamlakpi': ('gam-lak-pi', 'land-middle-great'),           # wilderness
        'mutin': ('mut-in', 'blow-INST'),                          # blowing
        'awlmawh': ('awl-mawh', 'rest-without'),                   # without rest
        'lopite': ('lopi-te', 'harlot-PL'),                        # harlots
        'theigahte': ('thei-gah-te', 'fig-tree-PL'),               # fig trees
        'kantanzo': ('kan-tan-zo', 'bound-stand-able'),            # bound
        'keei': ('keei', 'shadow'),                                # shadow
        'sapsap': ('sap-sap', 'speak-REDUP'),                      # speaking
        'gamsai': ('gam-sai', 'land-bitter'),                      # wormwood
        'nungdelhsak': ('nung-delh-sak', 'life-chase-CAUS'),       # scatter
        'ngaihsuttawm': ('ngaihsut-tawm', 'think-vain'),           # vain thought
        'pasalnei': ('pasal-nei', 'man-have'),                     # bridegroom
        'sangun': ('sang-un', 'high-3PL'),                         # worse
        'cizaw': ('ci-zaw', 'say-more'),                           # say more
        'amsak': ('am-sak', 'dismay-CAUS'),                        # dismayed
        'ngaihsutkhak': ('ngaihsut-khak', 'think-into'),           # came to mind
        'singpeek': ('sing-peek', 'wood-ceiling'),                 # cieled with cedar
        'saltangte': ('saltan-te', 'captive-PL'),                  # captives
        'khangtosak': ('khang-to-sak', 'grow-up-CAUS'),            # build up
        'siacipin': ('sia-cip-in', 'destroy-INTENS-INST'),         # utterly destroy
        # Round 104: More vocabulary for 99%
        'khuttung': ('khut-tung', 'hand-upon'),                    # at hand
        'umsak': ('um-sak', 'be-CAUS'),                            # make to trust
        'taangmi': ('taang-mi', 'star-person'),                    # messenger
        'omlaisun': ('om-lai-sun', 'be-still-middle'),             # remnant
        'cialte': ('cial-te', 'fat-PL'),                           # fatted
        'huhnate': ('huh-na-te', 'help-NMLZ-PL'),                  # helpers
        'misuamte': ('mi-suam-te', 'person-wilderness-PL'),        # wilderness people
        'painop': ('pai-nop', 'go-straight'),                      # straight forward
        'theisakkik': ('thei-sak-kik', 'know-CAUS-again'),         # open mouth
        'molhtumte': ('molh-tum-te', 'siege-mount-PL'),            # siege mounts
        'delhphahin': ('delh-phah-in', 'lay-upon-INST'),           # laying upon
        'muhkhak': ('muh-khak', 'see-into'),                       # in sight of
        'genkholhnate': ('gen-kholh-na-te', 'speak-declare-NMLZ-PL'), # declarations
        'sumzuak': ('sum-zuak', 'money-buy'),                      # buyer
        'mindaihuai': ('min-dai-huai', 'eye-far-mix'),             # far off
        'paikhiatlam': ('pai-khiat-lam', 'go-out-direction'),      # removing
        'apte': ('ap-te', 'talent-PL'),                            # talents
        'utbang': ('ut-bang', 'think-like'),                       # think like
        'zialzial': ('zial-zial', 'sharp-REDUP'),                  # sharpened
        'kisawmna': ('ki-sawm-na', 'REFL-sword-NMLZ'),             # terrors by sword
        'galnanna': ('gal-nan-na', 'war-shout-NMLZ'),              # shouting
        'annekte': ('an-nek-te', 'bread-eat-PL'),                  # bread of men
        'kumkhia': ('kum-khia', 'robe-out'),                       # put off robes
        'lianpente': ('lian-pen-te', 'great-most-PL'),             # greatest
        'huana': ('hua-na', 'garden-NMLZ'),                        # garden
        'tangtawng': ('tang-tawng', 'ancient-old'),                # ancient
        'pumpite': ('pum-pi-te', 'body-great-PL'),                 # bodies
        'nekzawh': ('nek-zawh', 'eat-finish'),                     # eat full
        'inndeipi': ('inn-dei-pi', 'house-temple-great'),          # inner temple
        'munteng': ('mun-teng', 'place-all'),                      # all places
        'piakkhop': ('piak-khop', 'give-offering'),                # meat offering
        'ngaptansak': ('ngap-tan-sak', 'ankle-stand-CAUS'),        # ankle deep
        'kideidanna': ('ki-dei-dan-na', 'REFL-serve-manner-NMLZ'), # service
        'khamkhi': ('kham-khi', 'cry-aloud'),                      # cry aloud
        'laimal': ('lai-mal', 'writing-?'),                        # writing
        'vaihawmpi': ('vai-hawm-pi', 'account-give-great'),        # president
        'khauhzaw': ('kauh-zaw', 'strong-more'),                   # stronger
        'pianzawh': ('pian-zawh', 'trouble-finish'),               # time of trouble
        'mawhmaisakna': ('mawh-mai-sak-na', 'sin-away-CAUS-NMLZ'), # altar to sin
        'mukhol': ('mu-khol', 'see-pleasant'),                     # pleasant place
        'awngkek': ('awng-kek', 'roar-INTENS'),                    # roar out
        'neihteng': ('neih-teng', 'have-all'),                     # have all
        'sihsuah': ('sih-suah', 'mourn-out'),                      # mourning
        'zaknop': ('zak-nop', 'hear-pleasant'),                    # hearing
        'neihtuam': ('neih-tuam', 'have-portion'),                 # inherit portion
        'ngakngak': ('ngak-ngak', 'wait-REDUP'),                   # suddenly come
        'kekseu': ('kek-seu', 'corrupt-moth'),                     # moth corrupt
        'nattunin': ('nat-tun-in', 'sick-enter-INST'),             # sick
        'siahdong': ('siah-dong', 'sin-person'),                   # sinners
        # Round 105: More vocabulary for 99%
        'siavuan': ('sia-vuan', 'sick-heal'),                      # physician
        'diamdiam': ('diam-diam', 'still-REDUP'),                  # reed shaken
        'cingteng': ('cing-teng', 'complete-all'),                 # about (number)
        'ninsakthei': ('nin-sak-thei', 'defile-CAUS-able'),        # defile
        'suplawhte': ('sup-lawh-te', 'save-able-PL'),              # those who save
        'cihnate': ('cih-na-te', 'command-NMLZ-PL'),               # commandments
        'zuihsa': ('zuih-sa', 'keep-PAST'),                        # have kept
        'hihthei': ('hih-thei', 'this-able'),                      # possible
        'sumbukah': ('sum-buk-ah', 'money-place-LOC'),             # marketplace
        'piakzah': ('piak-zah', 'give-amount'),                    # give as much
        'khawhlawh': ('khawh-lawh', 'let-able'),                   # let out
        'zangmang': ('zang-mang', 'devour-scatter'),               # devour
        'saupipi': ('sau-pi-pi', 'long-great-REDUP'),              # long prayer
        'tuitung': ('tui-tung', 'water-upon'),                     # sea and land
        'sihkhit': ('sih-khit', 'pass-finish'),                    # pass away
        'khawmpih': ('khawm-pih', 'dip-with'),                     # dip with
        'tuihupna': ('tui-hup-na', 'water-sponge-NMLZ'),           # sponge
        'kisialna': ('ki-sial-na', 'REFL-rise-NMLZ'),              # risen
        'hehpihhuaisa': ('heh-pih-huai-sa', 'compassion-with-mix-PAST'), # moved with compassion
        'theipah': ('thei-pah', 'know-perceive'),                  # perceived
        'anlumte': ('an-lum-te', 'bread-show-PL'),                 # shewbread
        'tuigei': ('tui-gei', 'water-edge'),                       # sea side
        'zakkhit': ('zak-khit', 'hear-finish'),                    # have heard
        'silloin': ('sil-lo-in', 'wash-NEG-INST'),                 # unwashen
        'neklam': ('nek-lam', 'eat-direction'),                    # eating
        'khamkhit': ('kham-khit', 'fill-finish'),                  # were filled
        'khuanawlah': ('khua-nawl-ah', 'village-outside-LOC'),     # out of town
        'khawhlawhsak': ('khawh-lawh-sak', 'let-able-CAUS'),       # let out
        'zintun': ('zin-tun', 'journey-enter'),                    # go in
        'zahpihbawl': ('zah-pih-bawl', 'wag-head-do'),             # wagging heads
        'sihkhitna': ('sih-khit-na', 'pass-finish-NMLZ'),          # knowing
        'theihkhit': ('theih-khit', 'know-finish'),                # perfect
        'kibangkim': ('ki-bang-kim', 'REFL-same-all'),             # same
        'dingvat': ('ding-vat', 'stand-shine'),                    # shining
        'maisuah': ('mai-suah', 'face-sad'),                       # sad
        'hinkik': ('hing-kik', 'live-again'),                      # alive
        'paitawm': ('pai-tawm', 'go-vain'),                        # come in vain
        'hilhsa': ('hilh-sa', 'teach-PAST'),                       # taught
        'minno': ('min-no', 'name-call'),                          # called
        'savunnim': ('sa-vunnim', 'skin-tanner'),                  # tanner
        'sawltakin': ('sawl-tak-in', 'send-true-INST'),            # continually
        'piakkhongna': ('piak-khong-na', 'give-gift-NMLZ'),        # gift
        'pianuam': ('pia-nuam', 'sacrifice-pleasant'),             # sacrifice
        'kinialna': ('ki-nial-na', 'REFL-dispute-NMLZ'),           # dissension
        'piakhin': ('piak-hin', 'give-already'),                   # let go
        'awnggawp': ('awng-gawp', 'decree-INTENS'),                # decrees
        # Round 106: More vocabulary for 99%
        'zinin': ('zin-in', 'journey-INST'),                       # passing through
        'awngkekgawp': ('awng-kek-gawp', 'cry-INTENS-INTENS'),     # cried out
        'kilemsak': ('ki-lem-sak', 'REFL-reconcile-CAUS'),         # reconciled
        'piangthei': ('piang-thei', 'come-able'),                  # cometh
        'zote': ('zo-te', 'able-PL'),                              # those who allow
        'lungnemna': ('lung-nem-na', 'heart-soft-NMLZ'),           # meekness
        'zangthei': ('zang-thei', 'power-able'),                   # have power
        'nethei': ('ne-thei', 'eat-able'),                         # able to eat
        'thuakkhak': ('thuak-khak', 'suffer-into'),                # condemnation
        'sepzawh': ('sep-zawh', 'work-finish'),                    # sufficient
        'puatham': ('puat-ham', 'glory-occasion'),                 # occasion to glory
        'pawlkhatin': ('pawl-khat-in', 'group-one-INST'),          # ambassadors
        'kinna': ('kin-na', 'clear-NMLZ'),                         # clearing
        'huhnopna': ('huh-nop-na', 'exhort-like-NMLZ'),            # exhortation
        'lunggimpih': ('lung-gim-pih', 'heart-care-with'),         # care
        'sansa': ('san-sa', 'before-PAST'),                        # before
        'hilhtheih': ('hilh-theih', 'teach-able'),                 # traditions
        'nasemkhawm': ('na-sem-khawm', 'work-do-together'),        # fellowship
        'thutakte': ('thu-tak-te', 'word-true-PL'),                # truth
        'genbelin': ('gen-bel-in', 'speak-about-INST'),            # whereof we speak
        'kikhulna': ('ki-khul-na', 'REFL-cast-NMLZ'),              # cast
        # Round 107: More vocabulary for 99% (count=2)
        'limlemel': ('lim-le-mel', 'form-NEG-void'),               # without form
        'golpite': ('gol-pi-te', 'whale-great-PL'),                # whales
        'singnai': ('sing-nai', 'stone-precious'),                 # precious stone
        'nakguh': ('nak-guh', 'rib-take'),                         # took rib
        'kipiansakna': ('ki-pian-sak-na', 'REFL-create-CAUS-NMLZ'), # creation
        'minthangte': ('min-thang-te', 'name-famous-PL'),          # men of renown
        'piansaksa': ('pian-sak-sa', 'create-CAUS-PAST'),          # have created
        'khaknelh': ('khak-nelh', 'shut-close'),                   # shut in
        'guahte': ('guah-te', 'window-PL'),                        # windows
        'kiamkiam': ('kiam-kiam', 'abate-REDUP'),                  # abated
        'sabengpa': ('sa-beng-pa', 'hunt-mighty-NMLZ'),            # mighty hunter
        'bawlnasa': ('bawl-na-sa', 'make-NMLZ-PAST'),              # had made
        'tawsawte': ('taw-saw-te', 'plain-oak-PL'),                # plains
        'behpa': ('beh-pa', 'arm-NMLZ'),                           # armed
        'keelnu': ('keel-nu', 'heifer-female'),                    # heifer
        'luk': ('luk', 'bring.out'),                               # bring out
        'luplam': ('lup-lam', 'lie-direction'),                    # lay with
        'luahkhawm': ('luah-khawm', 'cast-together'),              # cast out
        'thallot': ('thal-lot', 'bow-shot'),                       # bowshot
        'koihtuam': ('koih-tuam', 'set-portion'),                  # set by themselves
        'tuikhuka': ('tui-khu-ka', 'water-well-edge'),             # at the well
        'piakpa': ('piak-pa', 'give-NMLZ'),                        # giver
        'batsak': ('bat-sak', 'bracelet-put'),                     # put bracelets
        'khanghamin': ('khang-ham-in', 'age-full-INST'),           # full of years
        'sabet': ('sa-bet', 'hunt-expert'),                        # cunning hunter
        'cineel': ('ci-neel', 'skin-smooth'),                      # smooth man
        'lukhamin': ('lu-kham-in', 'head-pillow-INST'),            # for pillows
        'cingta': ('cing-ta', 'complete-PAST'),                    # fulfilled
        'semlai': ('sem-lai', 'serve-still'),                      # served still
        'kimuhdahna': ('ki-muh-dah-na', 'REFL-see-hate-NMLZ'),     # hated
        'koihkhawm': ('koih-khawm', 'set-together'),               # set together
        'namsak': ('nam-sak', 'kiss-CAUS'),                        # kiss
        'tatolh': ('ta-tolh', 'PAST-twenty'),                      # twenty years
        'kilaina': ('ki-lai-na', 'REFL-wrestle-NMLZ'),             # wrestling
        'hampheng': ('ham-pheng', 'booth-make'),                   # made booths
        'kisiatsakna': ('ki-siat-sak-na', 'REFL-defile-CAUS-NMLZ'), # defiled
        'mikhat': ('mi-khat', 'person-one'),                       # one people
        'mualsuang': ('mual-suang', 'hill-pillar'),                # pillar
        'kapsa': ('kap-sa', 'weep-PAST'),                          # wept
        'kituamna': ('ki-tuam-na', 'REFL-wrap-NMLZ'),              # wrapped
        'paktatin': ('pak-tat-in', 'pregnant-become-INST'),        # with child
        'khausan': ('khau-san', 'thread-scarlet'),                 # scarlet thread
        'ngaihbaangin': ('ngaih-baang-in', 'think-none-INST'),     # knew not
        'omkhop': ('om-khop', 'be-with'),                          # be with
        'zuakpa': ('zuak-pa', 'sell-NMLZ'),                        # seller
        'lungsi': ('lung-si', 'heart-fail'),                       # heart failed
        'thukanin': ('thu-kan-in', 'word-hard-INST'),              # roughly
        'hampen': ('ham-pen', 'search-most'),                      # searched
        'gankemte': ('gan-kem-te', 'cattle-keep-PL'),              # cattlemen
        'omsung': ('om-sung', 'be-inside'),                        # pilgrimage
        'lukhungah': ('lu-khung-ah', 'head-pillow-LOC'),           # bed's head
        'laitat': ('lai-tat', 'writing-end'),                      # end of commanding
        'paitosak': ('pai-to-sak', 'go-up-CAUS'),                  # let go up
        'phaikungte': ('phai-kung-te', 'bulrush-PL'),              # bulrushes
        'kikhiam': ('ki-khiam', 'REFL-diminish'),                  # diminished
        'khialzaw': ('khial-zaw', 'fault-more'),                   # fault
        'uihgawp': ('uih-gawp', 'stink-INTENS'),                   # stink
        'thokangte': ('tho-kang-te', 'magician-PL'),               # magicians
        'neihsak': ('neih-sak', 'have-CAUS'),                      # give us
        'mahmahsa': ('mah-mah-sa', 'self-REDUP-PAST'),             # themselves
        'bangtungzawl': ('bang-tung-zawl', 'door-above-post'),     # upper door post
        'talsuante': ('tal-suan-te', 'forehead-mark-PL'),          # frontlets
        'tangciak': ('tang-ciak', 'entangle-trap'),                # entangled
        'khenkham': ('khen-kham', 'divide-hold'),                  # divide
        'nannan': ('nan-nan', 'manna-REDUP'),                      # manna
        'liatzawkna': ('liat-zawk-na', 'great-more-NMLZ'),         # greater
        'lakthuah': ('lak-thuah', 'take-another'),                 # take another
        'belhna': ('belh-na', 'presume-NMLZ'),                     # presumptuously
        'zuihbeh': ('zuih-beh', 'follow-hurt'),                    # hurt
        'suaktasakin': ('suak-ta-sak-in', 'become-free-CAUS-INST'), # let go free
        'thudonin': ('thu-don-in', 'word-obey-INST'),              # obeying
        'phutkhak': ('phut-khak', 'fear-into'),                    # send fear
        # Round 108: More vocabulary for 99% (count=2)
        'vankhaina': ('van-khai-na', 'pillar-hang-NMLZ'),          # hooks, pillars
        'zaisak': ('zai-sak', 'altar-CAUS'),                       # make altar
        'karbankal': ('karban-kal', 'carbuncle-row'),              # carbuncle
        'puankhau': ('puan-khau', 'cloth-girdle'),                 # curious girdle
        'kawnggakte': ('kawng-gak-te', 'coat-PL'),                 # coats
        'singzep': ('sing-zep', 'tribe-call'),                     # called by name
        'hakna': ('hak-na', 'delay-NMLZ'),                         # delay
        'sumtui': ('sum-tui', 'gold-molten'),                      # molten gold
        'bawlkha': ('bawl-kha', 'make-already'),                   # already made
        'zungbuhte': ('zung-buh-te', 'bracelet-ring-PL'),          # bracelets
        'banbulhte': ('ban-bulh-te', 'tablet-PL'),                 # tablets
        'geelsiam': ('geel-siam', 'devise-make'),                  # devise cunning
        'siamgat': ('siam-gat', 'make-engrave'),                   # engraver
        'singpekte': ('sing-pek-te', 'wood-board-PL'),             # boards
        'vankhai': ('van-khai', 'pillar-hook'),                    # hooks
        'gelhnate': ('gelh-na-te', 'engrave-NMLZ-PL'),             # engravings
        'siklongte': ('sik-long-te', 'bell-round-PL'),             # bells
        'khaito': ('khai-to', 'hang-up'),                          # hang up
        'kinilhna': ('ki-nilh-na', 'REFL-anoint-NMLZ'),            # anointing
        'kigawhna': ('ki-gawh-na', 'REFL-sin-NMLZ'),               # sin offering
        'suhte': ('suh-te', 'rob-PL'),                             # robbed things
        'apkhawm': ('ap-khawm', 'anoint-together'),                # anointed
        'pheite': ('phei-te', 'breast-PL'),                        # breasts
        'awmtal': ('awm-tal', 'belly-crawl'),                      # belly
        'kibawltawm': ('ki-bawl-tawm', 'REFL-make-vain'),          # abominable
        'damsa': ('dam-sa', 'heal-PAST'),                          # healed
        'milmial': ('mil-mial', 'spot-freckle'),                   # freckled spot
        'zutna': ('zut-na', 'mortar-NMLZ'),                        # mortar
        'tutnasa': ('tut-na-sa', 'sit-NMLZ-PAST'),                 # sat upon
        'ninneih': ('nin-neih', 'issue-have'),                     # have issue
        'ninnei': ('nin-nei', 'issue-have'),                       # have issue
        'hunlopi': ('hun-lo-pi', 'time-NEG-any'),                  # not at all times
        'keeldawite': ('keel-dawi-te', 'goat-devil-PL'),           # devils
        'luakkhiat': ('luak-khiat', 'vomit-out'),                  # spue out
        'kiate': ('kia-te', 'grape-PL'),                           # grapes
        'kemcip': ('kem-cip', 'defraud-INTENS'),                   # defraud
        'tehnate': ('teh-na-te', 'measure-NMLZ-PL'),               # measures
        'vankahna': ('van-kah-na', 'spirit-follow-NMLZ'),          # familiar spirits
        'khutlekhe': ('khut-lekhe', 'hand-flat'),                  # flat nose
        'ciltang': ('cil-tang', 'back-crooked'),                   # crookback
        'nekkhak': ('nek-khak', 'eat-into'),                       # eat unwittingly
        'saulua': ('sau-lua', 'long-too'),                         # superfluous
        'zuaksa': ('zuak-sa', 'sell-PAST'),                        # sold
        'hakkolte': ('hak-kol-te', 'yoke-band-PL'),                # bands of yoke
        'demlai': ('dem-lai', 'reform-still'),                     # reformed
        'nanzawh': ('nan-zawh', 'fall-finish'),                    # fall
        'tungsiahte': ('tung-siah-te', 'age-sixty-PL'),            # sixty years old
        'buppite': ('bup-pi-te', 'head-great-PL'),                 # princes
        'simkhawm': ('sim-khawm', 'count-together'),               # take sum
        'kipiate': ('ki-pia-te', 'REFL-give-PL'),                  # wholly given
        'innkuankuanun': ('inn-kuan-kuan-un', 'house-family-REDUP-3PL'), # throughout families
        'tuibuahna': ('tui-buah-na', 'water-dish-NMLZ'),           # dishes
        'ditkikna': ('dit-kik-na', 'recompense-again-NMLZ'),       # recompense
        'pawmin': ('pawm-in', 'drink-INST'),                       # drinking
        'sauzaw': ('sau-zaw', 'long-more'),                        # longer
        'kihelte': ('ki-hel-te', 'REFL-mingle-PL'),                # mingled
        'nehin': ('neh-in', 'cloud-INST'),                         # in cloud
        'phunsanna': ('phun-san-na', 'murmur-complaint-NMLZ'),     # murmuring
        'ninpa': ('nin-pa', 'clean-NMLZ'),                         # clean person
        'gulte': ('gul-te', 'serpent-PL'),                         # serpents
        'nengcip': ('neng-cip', 'face-crush'),                     # crushed
        'zuisuak': ('zui-suak', 'follow-out'),                     # go with
        'kaplet': ('kap-let', 'break-pierce'),                     # pierce
        'pammaihsa': ('pam-maih-sa', 'zealous-face-PAST'),         # zealous
        'saksak': ('sak-sak', 'atonement-CAUS'),                   # made atonement
        'valh': ('valh', 'swallow'),                               # swallowed
        'hunun': ('hun-un', 'day-3PL'),                            # in day
        'kamciamnate': ('kam-ciam-na-te', 'mouth-vow-NMLZ-PL'),    # vows
        'kamciamin': ('kam-ciam-in', 'mouth-vow-INST'),            # vowing
        'khenkhiat': ('khen-khiat', 'divide-out'),                 # divided
        'zawhpih': ('zawh-pih', 'subdue-with'),                    # subdued
        'giahphualte': ('giah-phual-te', 'place-standard-PL'),     # standards
        'peemte': ('peem-te', 'refuge-PL'),                        # refuges
        'totsa': ('tot-sa', 'hear-PAST'),                          # heard
        'paupeengsak': ('pau-peeng-sak', 'speak-hard-CAUS'),       # hardened
        'khuazing': ('khua-zing', 'sky-dark'),                     # thick darkness
        'minamdang': ('mi-nam-dang', 'person-nation-other'),       # another nation
        'khiasak': ('khia-sak', 'put.out-CAUS'),                   # put out
        'khalna': ('khal-na', 'chasten-NMLZ'),                     # chastening
        # Round 109: More vocabulary for 99%
        'lamna': ('lam-na', 'dance-NMLZ'),                         # dancing
        'kiimnai': ('ki-im-nai', 'REFL-destroy-all'),              # utterly destroyed
        'hehsa': ('heh-sa', 'angry-PAST'),                         # anger kindled
        'hutna': ('hut-na', 'save-NMLZ'),                          # saving
        'kiimcip': ('ki-im-cip', 'REFL-destroy-INTENS'),           # utterly
        'dahlua': ('dah-lua', 'grieve-too'),                       # sorrow too much
        'louih': ('lo-uih', 'garlic-leek'),                        # leeks
        'suntangpi': ('sun-tang-pi', 'sun-before-great'),          # before sun
        'hawkkhia': ('hawk-khia', 'strip-out'),                    # stripped off
        'zumhuaipi': ('zum-huai-pi', 'unclean-mix-great'),         # unclean
        'haksapi': ('hak-sa-pi', 'difficult-PAST-great'),          # evil case
        'khekna': ('khek-na', 'fail-NMLZ'),                        # fail
        'kigaih': ('ki-gaih', 'REFL-chew'),                        # chewed
        'liaktum': ('liak-tum', 'lick-up'),                        # lick up
        'dawhsa': ('dawh-sa', 'draw-PAST'),                        # drawn
        'sungtum': ('sung-tum', 'inside-ask'),                     # ask counsel
        'phulapa': ('phula-pa', 'avenger-NMLZ'),                   # avenger
        'kimaituahin': ('ki-mai-tuah-in', 'REFL-face-do-INST'),    # face to face
        'tamvei': ('tam-vei', 'many-stripes'),                     # many stripes
        'kinengniamin': ('ki-neng-niam-in', 'REFL-grope-feel-INST'), # groping
        'kikzo': ('kik-zo', 'again-able'),                         # rise again
        'lamteng': ('lam-teng', 'direction-all'),                  # border met
        'sualphah': ('sual-phah', 'turn-in'),                      # turn in
        'hutpih': ('hut-pih', 'save-with'),                        # save/plead
        'kisuahin': ('ki-suah-in', 'REFL-ambush-INST'),            # laid wait
        'ginazaw': ('gina-zaw', 'better-more'),                    # better than
        'tasel': ('ta-sel', 'child-seek'),                         # bare not
        'botsat': ('bot-sat', 'break-thread'),                     # brake withs
        'busim': ('bu-sim', 'rope-new'),                           # new ropes
        'kimet': ('ki-met', 'REFL-shave'),                         # be shaven
        'kimawl': ('ki-mawl', 'REFL-sport'),                       # make sport
        'thahatte': ('tha-hat-te', 'strength-strong-PL'),          # mighty men
        'thahloh': ('thah-loh', 'slay-NEG'),                       # slay not
        'galphualah': ('gal-phual-ah', 'battle-place-LOC'),        # to battle
        'tuukhawk': ('tuu-khawk', 'sheep-cote'),                   # sheepcote
        'phawktel': ('phawk-tel', 'perceive-know'),                # perceived
        'hepkhiat': ('hep-khiat', 'depart-out'),                   # depart away
        'madawkin': ('ma-dawkin', 'that-reason'),                  # wherefore
        'tawmlua': ('tawm-lua', 'little-too'),                     # too little
        'zongzaw': ('zong-zaw', 'more-more'),                      # how much more
        'taisuk': ('tai-suk', 'cross-over'),                       # went over
        'kilinggawp': ('ki-ling-gawp', 'REFL-shake-INTENS'),       # shook terribly
        'sugawpzo': ('su-gawp-zo', 'leap-INTENS-able'),            # leaped over
        'suangseek': ('suang-seek', 'stone-hew'),                  # hewers
        'kidap': ('ki-dap', 'REFL-carve'),                         # carved
        'lamnop': ('lam-nop', 'desire-pleasant'),                  # pleased to do
        'olsak': ('ol-sak', 'easy-CAUS'),                          # made abundant
        'kilin': ('ki-lin', 'REFL-shake'),                         # shaken
        'hawklam': ('hawk-lam', 'trench-path'),                    # trench
        'kithakhauhsak': ('ki-tha-kauh-sak', 'REFL-strength-strong-CAUS'), # strengthen
        'kihepkhiat': ('ki-hep-khiat', 'REFL-depart-out'),         # departed
        'thep': ('thep', 'wound'),                                 # wounded
        # Round 110: More vocabulary for 99%
        'gan': ('gan', 'bear'),                                    # able to bear
        'tul': ('tul', 'foot'),                                    # on foot
        'pipi': ('pi-pi', 'grind-REDUP'),                          # to grind
        'gal': ('gal', 'enemy/war'),                               # enemy/war (not 'little')
        'kidona': ('kidona', 'sword'),                             # sword (gal-kidona = war-sword)
        'galkidona': ('gal-kidona', 'war-sword'),                  # sword of war
        'leung': ('le-ung', 'would.God-OPTATIVE'),                 # would God
        'sealt': ('se-alt', 'beast-island'),                       # island beasts
        'kua': ('kua', 'who'),                                     # who
        'kiattan': ('ki-at-tan', 'REFL-offer-closely'),            # take off hard by
        'pho': ('pho', 'spread'),                                  # spread abroad
        'bum': ('bum', 'charm'),                                   # charmer
        'tawhkuang': ('tawh-kuang', 'burn-foundation'),            # set on fire
        'el': ('el', 'provoke'),                                   # provoked
        'kingeinaseh': ('ki-ngei-na-seh', 'REFL-prove-NMLZ-try'),  # assayed/proved
        'tupa': ('tu-pa', 'son-NMLZ'),                             # son's son
        'lelh': ('lelh', 'defeat'),                                # defeat counsel
        'guiawk': ('gui-awk', 'saddle-go'),                        # saddled ass
        'suih': ('suih', 'hew'),                                   # hew timber
        'meigongnu': ('mei-gong-nu', 'fire-torch-woman'),          # widow
        'poding': ('po-ding', 'juniper-tree'),                     # juniper tree
        'lelhlam': ('lelh-lam', 'break-through'),                  # break through
        'teekta': ('teek-ta', 'old-already'),                      # husband old
        'koimah': ('koi-mah', 'whither-EMPH'),                     # whence
        'eklei': ('ek-lei', 'dung-field'),                         # dung
        'kitai': ('ki-tai', 'REFL-birth'),                         # come to birth
        'sulet': ('su-let', 'break-up'),                           # broken up
        'seng': ('seng', 'finish'),                                # finished
        'guahzuk': ('guah-zuk', 'transgress-much'),                # transgressed
        'kikhuak': ('ki-khuak', 'REFL-dig'),                       # wells digged
        'khusa': ('khu-sa', 'feast-make'),                         # made feast
        'daai': ('daai', 'hedge'),                                 # hedge about
        'kiseelcip': ('ki-seel-cip', 'REFL-hide-INTENS'),          # hidden
        'leen': ('leen', 'spark'),                                 # sparks
        'kihencip': ('ki-hen-cip', 'REFL-stop-INTENS'),            # stopped
        'taangzaw': ('taang-zaw', 'clear-more'),                   # clearer
        'bulsum': ('bul-sum', 'root-stock'),                       # stock/root
        'kigimsak': ('ki-gim-sak', 'REFL-remove-CAUS'),            # removed
        'kitunpih': ('ki-tun-pih', 'REFL-root-out'),               # rooted out
        'git': ('git', 'bound'),                                   # bounds
        'kileizo': ('ki-lei-zo', 'REFL-get-able'),                 # cannot be gotten
        'hawkguam': ('hawk-guam', 'cliff-cave'),                   # caves/cliffs
        'lato': ('la-to', 'drop-small'),                           # drops
        'khihcip': ('khih-cip', 'hide-INTENS'),                    # hide in dust
        'kihihsakpih': ('ki-hih-sak-pih', 'REFL-remember-CAUS-with'), # trust in
        'kidikdik': ('ki-dik-dik', 'REFL-bow-REDUP'),              # bowed down
        'gawisan': ('gawi-san', 'mock-feast'),                     # mockers in feasts
        'kisosuah': ('ki-so-suah', 'REFL-stir-up'),                # stir up
        'thokikzo': ('tho-kik-zo', 'rise-again-able'),             # rise up again
        'kigual': ('ki-gual', 'REFL-entreat'),                     # entreat favour
        'kihai': ('ki-hai', 'REFL-approve'),                       # approve
        'gulpi': ('gul-pi', 'serpent-great'),                      # serpent
        'sungsuk': ('sung-suk', 'inside-pour'),                    # pour out
        'kikumkum': ('ki-kum-kum', 'REFL-counsel-REDUP'),          # take counsel
        'tawdat': ('taw-dat', 'cup-full'),                         # cup full
        'galkido': ('gal-ki-do', 'battle-REFL-turn'),              # turned back
        'taklama': ('tak-lam-a', 'right-hand-LOC'),                # right hand
        'gilvahsak': ('gil-vah-sak', 'wheat-feed-CAUS'),           # fed with wheat
        'kitahkhak': ('ki-tah-khak', 'REFL-bear-up'),              # bear up
        'kitawhkuang': ('ki-tawh-kuang', 'REFL-burn-kindle'),      # wrath kindled
        'thazaw': ('tha-zaw', 'strength-more'),                    # more comfort
        'haksazaw': ('hak-sa-zaw', 'difficult-PAST-more'),         # woe is me
        'sotto': ('so-tto', 'go-come'),                            # go and come
        'kuncip': ('kun-cip', 'eye-INTENS'),                       # eyes look
        'lamka': ('lam-ka', 'way-high'),                           # high places
        'kiphawkphawk': ('ki-phawk-phawk', 'REFL-remember-REDUP'), # memory blessed
        'nguntang': ('ngun-tang', 'silver-choice'),                # choice silver
        'leenmang': ('leen-mang', 'whirlwind-pass'),               # whirlwind passeth
        'kipuk': ('ki-puk', 'REFL-fall'),                          # people fall
        'kiphasakte': ('ki-pha-sak-te', 'REFL-save-CAUS-PL'),      # saved people
        'hauhnop': ('hauh-nop', 'oppress-increase'),               # oppresseth
        'tawipa': ('tawi-pa', 'form-NMLZ'),                        # the great former
        'phengtat': ('pheng-tat', 'vision-perish'),                # no vision perish
        'kisilsiang': ('ki-sil-siang', 'REFL-wipe-clean'),         # wipeth mouth
        'hauzaw': ('hau-zaw', 'rich-more'),                        # great possessions
        # Round 111: More vocabulary for 99%
        'lihleh': ('lih-leh', 'cluster-vine'),                     # cluster
        'tulh': ('tulh', 'lead'),                                  # lead/bring
        'zunek': ('zu-nek', 'wine-drink'),                         # drink wine
        'masuan': ('ma-suan', 'that-before'),                      # before
        'kiliamsak': ('ki-liam-sak', 'REFL-hurt-CAUS'),            # hurt not
        'suahtung': ('suah-tung', 'rise-upon'),                    # going forth
        'kisusiacip': ('ki-su-sia-cip', 'REFL-break-destroy-INTENS'), # broken purposes
        'kisiacip': ('ki-sia-cip', 'REFL-destroy-INTENS'),         # utterly emptied
        'tumtakin': ('tum-tak-in', 'ease-true-INST'),              # at ease
        'zek': ('zek', 'vintage'),                                 # vintage
        'kizial': ('ki-zial', 'REFL-dissolve'),                    # dissolved
        'haipi': ('hai-pi', 'cup-big'),                            # cup
        'kituamkoih': ('ki-tuam-koih', 'REFL-stand-aside'),        # stand by
        'taisanzo': ('tai-san-zo', 'hold-water-able'),             # hold water
        'suam': ('suam', 'pollute'),                               # polluted
        'koici': ('koi-ci', 'how-pardon'),                         # how pardon
        'kipaithang': ('ki-pai-thang', 'REFL-scatter-field'),      # fall as
        'teeng': ('teeng', 'linen'),                               # linen
        'kilehngat': ('ki-leh-ngat', 'REFL-depart-heart'),         # heart depart
        'kipaidak': ('ki-pai-dak', 'REFL-cast-heat'),              # cast out
        'huhzo': ('huh-zo', 'breath-able'),                        # breath taken
        'kimudahtawm': ('ki-mudah-tawm', 'REFL-loathe-self'),      # loathe themselves
        'kiphan': ('ki-phan', 'REFL-prosper'),                     # prosper
        'lan': ('lan', 'fornication'),                             # fornication
        'hehnateng': ('heh-na-teng', 'fury-NMLZ-pour'),            # pour fury
        'lamkabom': ('lam-ka-bom', 'place-high-spoil'),            # take spoil
        'kimatin': ('ki-mat-in', 'REFL-wash-INST'),                # washed
        'meikuangpi': ('mei-kuang-pi', 'fire-furnace-great'),      # fiery furnace
        'kicingta': ('ki-cing-ta', 'REFL-great-already'),          # certainly come
        'thangpai': ('thang-pai', 'anger-against'),                # anger against
        'suahkhiatsak': ('suah-khiat-sak', 'take-off-CAUS'),       # take away
        'kiphukin': ('ki-phuk-in', 'REFL-hew-INST'),               # hewn down
        'tanlam': ('tan-lam', 'sad-face'),                         # sad countenance
        'kikhultum': ('ki-khul-tum', 'REFL-clothe-cast'),          # cast into
        'masazaw': ('ma-sa-zaw', 'that-first-more'),               # seek first
        'mopawi': ('mo-pawi', 'bridechamber-mourn'),               # children mourn
        'olzaw': ('ol-zaw', 'tolerable-more'),                     # more tolerable
        'depgawp': ('dep-gawp', 'thorn-choke'),                    # choked
        'taangci': ('taang-ci', 'seed-sow'),                       # sowed seed
        'tahum': ('ta-hum', 'enemy-sow'),                          # enemy sowed
        'pupa': ('pu-pa', 'grandfather-NMLZ'),                     # elders
        'suahnop': ('suah-nop', 'take-up'),                        # take up cross
        'kipiathuah': ('ki-pia-thuah', 'REFL-give-abundance'),     # given abundance
        'khitzawh': ('khit-zawh', 'curse-swear'),                  # curse and swear
        # Round 112: More vocabulary for 99%
        'tahto': ('tah-to', 'fill-put'),                           # filled and put
        'kithosak': ('ki-tho-sak', 'REFL-rise-CAUS'),              # risen from dead
        'tumkhit': ('tum-khit', 'privately-ask'),                  # asked privately
        'sungpan': ('sung-pan', 'among-from'),                     # one of
        'kilikkhia': ('ki-lik-khia', 'REFL-roll-out'),             # rolled away
        'kizakim': ('ki-zakim', 'REFL-fame'),                      # fame went out
        'mankhit': ('man-khit', 'cease-pray'),                     # when ceased
        'denlup': ('den-lup', 'tower-fall'),                       # tower fell
        'phadiak': ('pha-diak', 'covetous-deride'),                # derided
        'manpah': ('man-pah', 'perceive-lay'),                     # perceived
        'kiphunsan': ('ki-phun-san', 'REFL-murmur-say'),           # murmured
        'kuateng': ('kua-teng', 'who-all'),                        # who they were
        'thawhsakkik': ('thawh-sak-kik', 'raise-CAUS-again'),      # raised again
        'suahkhit': ('suah-khit', 'deliver-child'),                # delivered
        'taangzaih': ('taang-zaih', 'light-shine'),                # light shined
        'zomsuak': ('zom-suak', 'break-bread'),                    # break bread
        'menzipa': ('menzi-pa', 'governor-NMLZ'),                  # governor
        'tunzawh': ('tun-zawh', 'come-finish'),                    # come into
        'kimuang': ('ki-muang', 'REFL-instruct'),                  # instructor
        'bulphuhin': ('bul-phuh-in', 'root-sure-INST'),            # sure to
        'suahma': ('suah-ma', 'born-not.yet'),                     # not yet born
        'kiciing': ('ki-ciing', 'REFL-graft'),                     # grafted
        'pehkik': ('peh-kik', 'graft-again'),                      # graft again
        'dawizek': ('dawi-zek', 'unclean-esteem'),                 # esteems unclean
        'telkheh': ('tel-kheh', 'put-mind'),                       # putting in mind
        'kiukzawh': ('ki-uk-zawh', 'REFL-contain-finish'),         # cannot contain
        'kientel': ('ki-en-tel', 'REFL-examine-self'),             # examine himself
        'khuksung': ('khuk-sung', 'before-say'),                   # said before
        'bedolak': ('bedolak', 'bdellium'),                        # bdellium
        'sunim': ('su-nim', 'bruise-enmity'),                      # enmity
        'thahkhak': ('thah-khak', 'slay-vengeance'),               # vengeance
        'petin': ('pet-in', 'pluck-leaf'),                         # plucked leaf
        'lamun': ('la-mun', 'garment-cover'),                      # covered
        'lal': ('lal', 'plain'),                                   # plain
        'bekbak': ('bek-bak', 'sleep-deep'),                       # deep sleep
        'khita': ('khi-ta', 'know-PAST'),                          # I know
        'thawhlam': ('thawh-lam', 'lie-down'),                     # lay with
        'gikzah': ('gik-zah', 'weigh-silver'),                     # weighed silver
        'mavangsak': ('ma-vang-sak', 'that-wonder-CAUS'),          # wondering
        'daptakin': ('dap-tak-in', 'peace-true-INST'),             # held peace
        'phukhong': ('phu-khong', 'sod-pottage'),                  # sod pottage
        'hucipin': ('hu-cip-in', 'stop-INTENS-INST'),              # stopped
        'tuupi': ('tuu-pi', 'sheep-great'),                        # ewes and goats
        'kinuihsan': ('ki-nuih-san', 'REFL-shame-complaint'),      # be shamed
        'sungthu': ('sung-thu', 'hand-matter'),                    # all in hand
        'sungtang': ('sung-tang', 'inside-mock'),                  # mock us
        'theemsak': ('theem-sak', 'blast-CAUS'),                   # blasted
        'tunkim': ('tun-kim', 'store-all'),                        # all storehouses
        'kibalzan': ('ki-bal-zan', 'REFL-tear-pieces'),            # torn in pieces
        'kithawisakin': ('ki-thawi-sak-in', 'REFL-present-CAUS-INST'), # presented
        'mongkhat': ('mong-khat', 'end-one'),                      # one end
        'thadim': ('tha-dim', 'lively-midwife'),                   # lively
        'ngeizah': ('ngei-zah', 'straw-diminish'),                 # get straw
        'lomlomin': ('lom-lom-in', 'heap-REDUP-INST'),             # upon heaps
        'kilawhgawp': ('ki-lawh-gawp', 'REFL-break-forth'),        # breaking forth
        'vuih': ('vuih', 'boll'),                                  # bolled
        'kilamdangin': ('ki-lam-dang-in', 'REFL-direction-other-INST'), # put difference
        'khikcip': ('khik-cip', 'still-INTENS'),                   # still as stone
        'phimpi': ('phim-pi', 'ear-bore'),                         # bore ear
        # Round 113: More vocabulary for 99%
        'pik': ('pik', 'gore'),                                    # gored
        'kiuhkeuhin': ('ki-uhkeuh-in', 'REFL-overthrow-INST'),     # overthrow
        'tunpi': ('tun-pi', 'hornet-great'),                       # hornets
        'kimaingat': ('ki-mai-ngat', 'REFL-face-look'),            # faces look
        'kikak': ('ki-kak', 'REFL-couple'),                        # coupled
        'long': ('long', 'pomegranate'),                           # pomegranate
        'sungkua': ('sung-kua', 'inward-wash'),                    # wash inwards
        'thaksing': ('thak-sing', 'sweet-spice'),                  # spices
        'kikhep': ('ki-khep', 'REFL-double'),                      # doubled
        'meibung': ('mei-bung', 'fire-oven'),                      # oven
        'kimitsak': ('ki-mit-sak', 'REFL-burn-CAUS'),              # burning
        'helsa': ('hel-sa', 'bake-PAST'),                          # baken
        'kiminthangsak': ('ki-min-thang-sak', 'REFL-name-glory-CAUS'), # glorified
        'khepek': ('khe-pek', 'leg-leap'),                         # leap
        'kitom': ('ki-tom', 'REFL-locust'),                        # locust
        'khebom': ('khe-bom', 'paw-NMLZ'),                         # paws
        'phakpa': ('phak-pa', 'bare-NMLZ'),                        # head bare
        'kisianthosak': ('ki-sian-tho-sak', 'REFL-clean-rise-CAUS'), # cleansing
        'kimuhmawh': ('ki-muh-mawh', 'REFL-see-hide'),             # hide eyes
        'kihallum': ('ki-hal-lum', 'REFL-burn-fire'),              # burnt with fire
        'kimasa': ('ki-ma-sa', 'REFL-first-PAST'),                 # shall not take
        'tuulekeel': ('tuu-le-keel', 'sheep-and-goat'),            # beeves or sheep
        'kitaangko': ('ki-taang-ko', 'REFL-trumpet-blow'),         # blowing trumpets
        'poisak': ('poi-sak', 'blemish-CAUS'),                     # cause blemish
        'lopawi': ('lo-pawi', 'field-thresh'),                     # threshing
        'hahsiang': ('hah-siang', 'old-store'),                    # old store
        'kipuahphat': ('ki-puah-phat', 'REFL-pine-away'),          # pine away
        'vilvelin': ('vil-vel-in', 'vow-REDUP-INST'),              # singular vow
        'tulkua': ('tul-kua', 'thousand-head'),                    # heads of thousands
        'hawng': ('hawng', 'husk'),                                # husk
        'liangko': ('liang-ko', 'shoulder-both'),                  # both shoulders
        'napi': ('na-pi', 'distress-great'),                       # distress
        'zanglei': ('zang-lei', 'east-field'),                     # from the east
        'khangsimna': ('khang-sim-na', 'generation-divide-NMLZ'),  # generations
        'sepna': ('sep-na', 'do-NMLZ'),                            # doest
        'nihte': ('nih-te', 'two-PL'),                             # two
        'nihna': ('nih-na', 'second-NMLZ'),                        # second
        'simna': ('sim-na', 'count-NMLZ'),                         # numbered
        'biakna': ('biak-na', 'worship-NMLZ'),                     # altar
        'note': ('no-te', 'you-PL'),                               # you
        'sawmnga': ('sawm-nga', 'ten-five'),                       # fifty
        'munte': ('mun-te', 'spot-PL'),                            # spots
        'nawhsa': ('nawh-sa', 'unleavened-PAST'),                  # unleavened
        'sangna': ('sang-na', 'high-NMLZ'),                        # high places
        'khuaneute': ('khua-neu-te', 'village-small-PL'),          # villages
        'paina': ('pai-na', 'go-NMLZ'),                            # walking
        'ancilna': ('an-cil-na', 'corn-thresh-NMLZ'),              # threshingfloor
        'omlai': ('om-lai', 'rest-still'),                         # rest
        'piakna': ('piak-na', 'give-NMLZ'),                        # offering
        'dangte': ('dang-te', 'other-PL'),                         # other
        'thuakna': ('thuak-na', 'afflict-NMLZ'),                   # affliction
        'kaikhia': ('kai-khia', 'draw-out'),                       # draw
        'cithei': ('ci-thei', 'eye-evil'),                         # eye evil
        'theithei': ('thei-thei', 'know-REDUP'),                   # perceive
        'bangzia': ('bang-zia', 'what-like'),                      # such like
        # Round 114: More vocabulary for 99%
        'hawi': ('hawi', 'holy'),                                  # holy
        'kihuansa': ('ki-huan-sa', 'REFL-shave-PAST'),             # shaven
        'kiumin': ('ki-um-in', 'REFL-strong-INST'),                # strong
        'mongteep': ('mong-teep', 'border-fringe'),                # fringes
        'kiphelkham': ('ki-phel-kham', 'REFL-split-asunder'),      # clave asunder
        'kisiincip': ('ki-siin-cip', 'REFL-cover-INTENS'),         # covering
        'madawk': ('ma-dawk', 'that-morrow'),                      # on morrow
        'suzan': ('su-zan', 'strength-unicorn'),                   # unicorn
        'kizomtawm': ('ki-zom-tawm', 'REFL-join-together'),        # joined
        'gimsakgawp': ('gim-sak-gawp', 'vex-CAUS-INTENS'),         # vex
        'lehpan': ('leh-pan', 'rebel-against'),                    # rebelled
        'dungteng': ('dung-teng', 'west-border'),                  # west border
        'tawmcik': ('tawm-cik', 'few-number'),                     # few in number
        'dengzan': ('deng-zan', 'rod-iron'),                       # rod of iron
        'talsuan': ('tal-suan', 'lay-up'),                         # lay up
        'kideidan': ('ki-dei-dan', 'REFL-kill-eat'),               # kill and eat
        'sotsak': ('sot-sak', 'enlarge-CAUS'),                     # enlarge
        'kibuakhia': ('ki-buak-hia', 'REFL-pour-out'),             # poured out
        'tawsak': ('taw-sak', 'weary-CAUS'),                       # wearied
        'songpi': ('song-pi', 'image-great'),                      # image
        'haksalua': ('hak-sa-lua', 'hard-PAST-too'),               # too hard
        'zomto': ('zom-to', 'loose-shoe'),                         # loose shoe
        'gilvahin': ('gil-vah-in', 'tithe-fill-INST'),             # tithing
        'oltak': ('ol-tak', 'ease-rest'),                          # ease/rest
        'kisukkhak': ('ki-suk-khak', 'REFL-blood-upon'),           # blood upon
        'kilelsak': ('ki-lel-sak', 'REFL-flee-CAUS'),              # made flee
        'guktak': ('guk-tak', 'good-fidelity'),                    # good fidelity
        'gamtatna': ('gam-tat-na', 'earth-curse-NMLZ'),            # curse ground
        'inndei': ('inn-dei', 'house-chamber'),                    # chamber
        'hehpihna': ('heh-pih-na', 'favor-with-NMLZ'),             # favour
        'siampi': ('siam-pi', 'priest-great'),                     # priest
        'sihna': ('sih-na', 'blood-NMLZ'),                         # blood/life
        'lingsa': ('ling-sa', 'tremble-PAST'),                     # trembled
        'zahko': ('zah-ko', 'gather-grapes'),                      # gathered
        'koihna': ('koih-na', 'set-NMLZ'),                         # set over
        'siahna': ('siah-na', 'snare-NMLZ'),                       # snare
        'hoihzaw': ('hoih-zaw', 'well-more'),                      # well
        'kisa': ('ki-sa', 'REFL-PAST'),                            # grieved
        'sangpi': ('sang-pi', 'high-great'),                       # high walls
        'tanglai': ('tang-lai', 'ancient-NMLZ'),                   # ancient
        'ngaihsutna': ('ngaih-sut-na', 'think-NMLZ'),              # thoughts
        'khangto': ('khang-to', 'prevail-up'),                     # prevailed
        'amaute': ('a-mau-te', '3SG-EMPH-PL'),                     # them
        'honsa': ('hon-sa', 'open-PAST'),                          # open pit
        'biakpiakna': ('biak-piak-na', 'worship-offer-NMLZ'),      # burnt offering
        'biakbuk': ('biak-buk', 'worship-house'),                  # sanctuary
        'thukhenna': ('thu-khen-na', 'word-judge-NMLZ'),           # judge
        'gamgi': ('gam-gi', 'land-year'),                          # year
        'khapna': ('khap-na', 'pledge-NMLZ'),                      # pledge
        'suksiatna': ('suk-siat-na', 'destroy-NMLZ'),              # destruction
        'zuihna': ('zuih-na', 'turn-NMLZ'),                        # turned away
        'cilna': ('cil-na', 'command-NMLZ'),                       # commandment
        'dingto': ('ding-to', 'stand-up'),                         # stood up
        'bawlpha': ('bawl-pha', 'fortify-strong'),                 # fortified
        'kidona': ('ki-don-a', 'REFL-war-LOC'),                    # war
        'sumkholna': ('sum-khol-na', 'silver-treasure-NMLZ'),      # treasuries
        'zanthapai': ('zan-tha-pai', 'night-weary-appoint'),       # wearisome nights
        'kipan': ('ki-pan', 'REFL-begin'),                         # began
        # Round 115: Judges and historical vocabulary
        'kikhungto': ('ki-khung-to', 'REFL-go-up'),                # goeth up
        'kiimteng': ('ki-im-teng', 'REFL-all-border'),             # unto borders
        'hahsawl': ('hah-sawl', 'ask-field'),                      # ask field
        'kinim': ('ki-nim', 'REFL-divide'),                        # divided prey
        'tuksukin': ('tuk-suk-in', 'tumble-down-INST'),            # tumbled
        'teeksih': ('teek-sih', 'old-die'),                        # good old age
        'sosuah': ('so-suah', 'send-privily'),                     # sent privily
        'hallum': ('hal-lum', 'burn-fire'),                        # burnt with fire
        'kisingin': ('ki-sing-in', 'REFL-shake-INST'),             # shake myself
        'gualnuam': ('gual-nuam', 'sacrifice-rejoice'),            # rejoice sacrifice
        'kizuihna': ('ki-zuih-na', 'REFL-keep-NMLZ'),              # keeping
        'khuasung': ('khua-sung', 'village-inside'),               # within gates
        'sinna': ('sin-na', 'prepare-NMLZ'),                       # preparation
        'kizem': ('ki-zem', 'REFL-twine'),                         # twined
        # Round 116: Common word+suffix combinations
        'liangkoah': ('liang-ko-ah', 'shoulder-both-LOC'),         # on both shoulders
        'napiun': ('na-pi-un', '2PL-great-3PL'),                   # but/however
        'zangleia': ('zang-lei-a', 'east-field-LOC'),              # from east LOC
        'khangsimnaah': ('khang-sim-na-ah', 'generation-divide-NMLZ-LOC'), # generations LOC
        'sepnaah': ('sep-na-ah', 'do-NMLZ-LOC'),                   # doest LOC
        'kiukzawhna': ('ki-uk-zawh-na', 'REFL-contain-finish-NMLZ'), # cannot contain
        'nihteah': ('nih-te-ah', 'two-PL-LOC'),                    # two LOC
        'nihnaah': ('nih-na-ah', 'second-NMLZ-LOC'),               # second LOC
        'simnaah': ('sim-na-ah', 'count-NMLZ-LOC'),                # counted LOC
        'biaknaah': ('biak-na-ah', 'worship-NMLZ-LOC'),            # altar LOC
        'sawmngain': ('sawm-nga-in', 'ten-five-INST'),             # fifty INST
        'munteah': ('mun-te-ah', 'spot-PL-LOC'),                   # spots LOC
        'nawhsain': ('nawh-sa-in', 'unleavened-PAST-INST'),        # unleavened INST
        'sangnaah': ('sang-na-ah', 'high-NMLZ-LOC'),               # high LOC
        'khuaneutea': ('khua-neu-te-a', 'village-small-PL-LOC'),   # villages LOC
        'painaah': ('pai-na-ah', 'go-NMLZ-LOC'),                   # walking LOC
        'ancilnaah': ('an-cil-na-ah', 'corn-thresh-NMLZ-LOC'),     # threshingfloor LOC
        'omlaiin': ('om-lai-in', 'rest-still-INST'),               # rest INST
        'piaknaah': ('piak-na-ah', 'give-NMLZ-LOC'),               # offering LOC
        'dangteah': ('dang-te-ah', 'other-PL-LOC'),                # other LOC
        'thuaknaah': ('thuak-na-ah', 'afflict-NMLZ-LOC'),          # affliction LOC
        'kaikhiain': ('kai-khia-in', 'draw-out-INST'),             # draw INST
        'citheiin': ('ci-thei-in', 'eye-evil-INST'),               # eye evil INST
        'theitheiin': ('thei-thei-in', 'know-REDUP-INST'),         # perceive INST
        'bangziain': ('bang-zia-in', 'what-like-INST'),            # such like INST
        'lasakol': ('la-sakol', 'take-CAUS.APPL'),                 # take CAUS
        'kuanguk': ('kuang-uk', 'box-rule'),                       # rule over
        'vaak': ('va-ak', 'bird-crow'),                            # bird crow
        'ukpain': ('uk-pa-in', 'rule-NMLZ-INST'),                  # ruler INST
        'kiapna': ('ki-ap-na', 'REFL-give-NMLZ'),                  # giving
        'pahtawinain': ('pah-tawi-na-in', 'praise-NMLZ-INST'),     # praising INST
        'khuaneuteah': ('khua-neu-te-ah', 'village-small-PL-LOC'), # villages LOC
        'niun': ('ni-un', 'day-3PL'),                              # days
        'gamtatnaah': ('gam-tat-na-ah', 'earth-curse-NMLZ-LOC'),   # curse LOC
        'piaknainin': ('piak-na-in', 'give-NMLZ-INST'),            # offering INST
        'inndeiahah': ('inn-dei-ah', 'house-chamber-LOC'),         # chamber LOC
        'hehpihnain': ('heh-pih-na-in', 'favor-with-NMLZ-INST'),   # favour INST
        # Round 117: More suffix combinations
        'piaknanin': ('piak-na-in', 'give-NMLZ-INST'),             # offering INST
        'inndeiah': ('inn-dei-ah', 'house-chamber-LOC'),           # chamber LOC
        'siampiin': ('siam-pi-in', 'priest-great-INST'),           # priest INST
        'sihnaah': ('sih-na-ah', 'blood-NMLZ-LOC'),                # blood LOC
        'lingsain': ('ling-sa-in', 'tremble-PAST-INST'),           # trembled INST
        'koihnaah': ('koih-na-ah', 'set-NMLZ-LOC'),                # set LOC
        'siahnain': ('siah-na-in', 'snare-NMLZ-INST'),             # snare INST
        'hoihzawin': ('hoih-zaw-in', 'well-more-INST'),            # well INST
        'kisain': ('ki-sa-in', 'REFL-PAST-INST'),                  # grieved INST
        'sangpiin': ('sang-pi-in', 'high-great-INST'),             # high walls INST
        'tanglaia': ('tang-lai-a', 'ancient-NMLZ-LOC'),            # ancient LOC
        'ngaihsutnaah': ('ngaih-sut-na-ah', 'think-NMLZ-LOC'),     # thoughts LOC
        'gamlapi': ('gam-la-pi', 'land-field-great'),              # great field
        'khuaul': ('khua-ul', 'village-EMPH'),                     # village
        'khangtoin': ('khang-to-in', 'prevail-up-INST'),           # prevailed INST
        'honsain': ('hon-sa-in', 'open-PAST-INST'),                # opened INST
        'biakpiaknaah': ('biak-piak-na-ah', 'worship-offer-NMLZ-LOC'), # offering LOC
        'biakbuka': ('biak-buk-a', 'worship-house-LOC'),           # sanctuary LOC
        'thukhennaah': ('thu-khen-na-ah', 'word-judge-NMLZ-LOC'),  # judge LOC
        'gamgiin': ('gam-gi-in', 'land-year-INST'),                # year INST
        'khapnain': ('khap-na-in', 'pledge-NMLZ-INST'),            # pledge INST
        'suksiatnaah': ('suk-siat-na-ah', 'destroy-NMLZ-LOC'),     # destruction LOC
        'gamgiah': ('gam-gi-ah', 'land-year-LOC'),                 # year LOC
        'koihkhiain': ('koih-khia-in', 'set-out-INST'),            # set out INST
        'ithuai': ('it-huai', 'love-mix'),                         # beloved
        'zuihnaah': ('zuih-na-ah', 'turn-NMLZ-LOC'),               # turned LOC
        'cilnaah': ('cil-na-ah', 'command-NMLZ-LOC'),              # command LOC
        'meiamte': ('mei-am-te', 'fire-dark-PL'),                  # dark fire PL
        'vaakte': ('va-ak-te', 'bird-crow-PL'),                    # crows PL
        'maiet': ('mai-et', 'face-look'),                          # face look
        'dingtoin': ('ding-to-in', 'stand-up-INST'),               # stood INST
        'bawlphain': ('bawl-pha-in', 'fortify-strong-INST'),       # fortified INST
        'kidonaah': ('ki-don-a-ah', 'REFL-war-LOC-LOC'),           # war LOC
        'siaa': ('sia-a', 'bad-LOC'),                              # bad LOC
        'sumkholnaah': ('sum-khol-na-ah', 'silver-treasure-NMLZ-LOC'), # treasury LOC
        'zanthapaiin': ('zan-tha-pai-in', 'night-weary-appoint-INST'), # wearisome INST
        'vasakalaoh': ('va-sa-kalaoh', 'bird-meat-INTERJ'),        # bird INTERJ
        'thungetnaah': ('thu-nget-na-ah', 'word-pray-NMLZ-LOC'),   # prayer LOC
        'lunggulhnain': ('lung-gulh-na-in', 'heart-sorrow-NMLZ-INST'), # sorrow INST
        'ngaihsutpiin': ('ngaih-sut-pi-in', 'think-great-INST'),   # thinking INST
        'sealt': ('se-alt', 'beast-island'),                       # island beast
        'tanglaiin': ('tang-lai-in', 'ancient-NMLZ-INST'),         # ancient INST
        'puanak': ('puan-ak', 'cloth-put'),                        # clothe
        'paaiahaah': ('paai-ah', 'place-LOC'),                     # place LOC
        'sumzuaknaah': ('sum-zuak-na-ah', 'money-sell-NMLZ-LOC'),  # merchandise LOC
        # Round 118: More suffix combinations and partials
        'liangkoah': ('liang-ko-ah', 'shoulder-both-LOC'),         # shoulder LOC
        'piaknanin': ('piak-na-in', 'give-NMLZ-INST'),             # offering INST
        'zahkoin': ('zah-ko-in', 'gather-grapes-INST'),            # gathering INST
        'gamlapia': ('gam-la-pi-a', 'land-field-great-LOC'),       # field LOC
        'zuin': ('zu-in', 'wine-INST'),                            # wine INST
        'naiin': ('nai-in', 'near-INST'),                          # near INST
        'paaiaah': ('paai-ah', 'place-LOC'),                       # place LOC
        'leenggahzuhau': ('leeng-gah-zu-hau', 'eagle-vulture-wine-rich'), # eagle
        'nuamtaksain': ('nuam-tak-sa-in', 'pleasant-true-PAST-INST'), # pleasant INST
        'zahtain': ('zah-ta-in', 'fear-already-INST'),             # feared INST
        'vunat': ('vun-at', 'skin-place'),                         # on skin
        'thukin': ('thuk-in', 'deep-INST'),                        # deep INST
        'pain': ('pa-in', 'father-INST'),                          # father INST
        'thugennaah': ('thu-gen-na-ah', 'word-speak-NMLZ-LOC'),    # speaking LOC
        'tuangsakin': ('tuang-sak-in', 'feed-CAUS-INST'),          # fed INST
        'thupia': ('thu-pi-a', 'word-great-LOC'),                  # great word LOC
        'siangthosakin': ('siang-tho-sak-in', 'clean-rise-CAUS-INST'), # cleansing INST
        'neihnaah': ('neih-na-ah', 'have-NMLZ-LOC'),               # have LOC
        'linaah': ('li-na-ah', 'four-NMLZ-LOC'),                   # four LOC
        'saiik': ('sa-iik', 'meat-INTERJ'),                        # meat INTERJ
        'sutkhiain': ('sut-khia-in', 'remove-out-INST'),           # remove INST
        'siangsakin': ('siang-sak-in', 'clean-CAUS-INST'),         # clean INST
        'sagihnaah': ('sa-gih-na-ah', 'meat-cut-NMLZ-LOC'),        # cut LOC
        'biakbukah': ('biak-buk-ah', 'worship-house-LOC'),         # sanctuary LOC
        'innkuanah': ('inn-kuan-ah', 'house-family-LOC'),          # family LOC
        'mimiin': ('mi-mi-in', 'person-REDUP-INST'),               # persons INST
        'siazawin': ('sia-zaw-in', 'bad-more-INST'),               # worse INST
        'bangmaha': ('bang-mah-a', 'what-EMPH-LOC'),               # what LOC
        'ngahmunteah': ('ngah-mun-te-ah', 'place-PL-LOC'),         # places LOC
        'bawlnaah': ('bawl-na-ah', 'make-NMLZ-LOC'),               # make LOC
        'dangtea': ('dang-te-a', 'other-PL-LOC'),                  # other LOC
        'naupaiiin': ('nau-paii-in', 'child-cry-INST'),            # crying INST
        'balkhiain': ('bal-khia-in', 'tear-out-INST'),             # torn INST
        'neknaah': ('nek-na-ah', 'eat-NMLZ-LOC'),                  # eat LOC
        'tehnain': ('teh-na-in', 'measure-NMLZ-INST'),             # measure INST
        'samsiain': ('sam-sia-in', 'hair-bad-INST'),               # hair INST
        # Round 119: More suffix combinations
        'khualnun': ('khual-na-un', 'stranger-NMLZ-3PL'),          # strangers
        'biaknateah': ('biak-na-te-ah', 'worship-NMLZ-PL-LOC'),    # altars LOC
        'zaiin': ('zai-in', 'altar-INST'),                         # altar INST
        'pialin': ('pial-in', 'turn-INST'),                        # turn INST
        'lasakolte': ('la-sakol-te', 'take-CAUS.APPL-PL'),         # take CAUS PL
        'zahpihin': ('zah-pih-in', 'fear-with-INST'),              # fear with INST
        'sisain': ('si-sa-in', 'blood-PAST-INST'),                 # blood INST
        'ninai': ('ni-nai', 'day-near'),                           # near day
        'awin': ('aw-in', 'voice-INST'),                           # voice INST
        'nitein': ('ni-te-in', 'day-PL-INST'),                     # days INST
        'zazaa': ('za-za-a', 'hear-REDUP-LOC'),                    # heard LOC
        'lutnaa': ('lut-na-a', 'enter-NMLZ-LOC'),                  # enter LOC
        'siasain': ('sia-sa-in', 'bad-PAST-INST'),                 # bad INST
        'inndeiteah': ('inn-dei-te-ah', 'house-chamber-PL-LOC'),   # chambers LOC
        'kahkahnain': ('kah-kah-na-in', 'follow-REDUP-NMLZ-INST'), # following INST
        'vasakalaohte': ('va-sa-kalaoh-te', 'bird-meat-INTERJ-PL'), # birds PL
        'bangzahtain': ('bang-zah-ta-in', 'what-fear-already-INST'), # feared INST
        'khaguhah': ('kha-guh-ah', 'chin-jaw-LOC'),                # jaw LOC
        'thungetnain': ('thu-nget-na-in', 'word-pray-NMLZ-INST'),  # pray INST
        'ngaknain': ('ngak-na-in', 'wait-NMLZ-INST'),              # wait INST
        'sisaa': ('si-sa-a', 'blood-PAST-LOC'),                    # blood LOC
        'neuteah': ('neu-te-ah', 'small-PL-LOC'),                  # small LOC
        'nenein': ('ne-ne-in', 'small-REDUP-INST'),                # small INST
        'beisaa': ('bei-sa-a', 'finish-PAST-LOC'),                 # finished LOC
        'lungamsak': ('lung-am-sak', 'heart-rest-CAUS'),           # comfort
        'khuaneua': ('khua-neu-a', 'village-small-LOC'),           # village LOC
        'kiumcihna': ('ki-um-cih-na', 'REFL-strong-say-NMLZ'),     # strengthening
        'kangop': ('kang-op', 'carry-bear'),                       # bear
        'hilhkholhnain': ('hilh-kholh-na-in', 'teach-NMLZ-INST'),  # teach INST
        'laimal': ('lai-mal', 'book-plain'),                       # plain book
        'guktakna': ('guk-tak-na', 'good-true-NMLZ'),              # goodness
        'deihnaun': ('deih-na-un', 'want-NMLZ-3PL'),               # want
        'upnaah': ('up-na-ah', 'believe-NMLZ-LOC'),                # believe LOC
        'luppihin': ('lup-pih-in', 'roll-with-INST'),              # roll INST
        'piangkhiain': ('piang-khia-in', 'born-out-INST'),         # born INST
        'nuiin': ('nui-in', 'laugh-INST'),                         # laugh INST
        'topain': ('topa-in', 'lord-INST'),                        # lord INST
        'thuakzoin': ('thuak-zo-in', 'endure-able-INST'),          # endure INST
        # Round 120: More vocabulary and suffix forms
        'muhdahhuai': ('muh-dah-huai', 'see-hate-mix'),            # troubled
        'semsemna': ('sem-sem-na', 'hate-REDUP-NMLZ'),             # hated more
        'kapsain': ('kap-sa-in', 'mourn-PAST-INST'),               # mourning INST
        'luahnaah': ('luah-na-ah', 'issue-NMLZ-LOC'),              # issue LOC
        'nekneknain': ('nek-nek-na-in', 'eat-REDUP-NMLZ-INST'),    # eating INST
        'buknaah': ('buk-na-ah', 'shelter-NMLZ-LOC'),              # shelter LOC
        'sapnain': ('sap-na-in', 'stretch-NMLZ-INST'),             # stretch INST
        'khauhsakin': ('kauh-sak-in', 'harden-CAUS-INST'),         # harden INST
        'sianthonaah': ('sian-tho-na-ah', 'holy-rise-NMLZ-LOC'),   # holiness LOC
        'kihtakhuaiin': ('ki-hta-khuai-in', 'REFL-fierce-mix-INST'), # fierce INST
        'sinsoin': ('sin-so-in', 'consume-INST'),                  # consume INST
        'puanbuka': ('puan-buk-a', 'cloth-tent-LOC'),              # tent LOC
        'khialhnaah': ('khialh-na-ah', 'sin-NMLZ-LOC'),            # sin LOC
        'vevein': ('ve-ve-in', 'lack-REDUP-INST'),                 # lack INST
        'nengnianmin': ('neng-niam-in', 'fellowship-INST'),        # fellowship INST
        'mupi': ('mu-pi', 'bird-great'),                           # eagle/ossifrage
        'luimu': ('lui-mu', 'river-bird'),                         # osprey
        'mumeika': ('mu-mei-ka', 'bird-fire-vulture'),             # vulture
        'pengpelep': ('peng-pelep', 'wing-night'),                 # night hawk
        'musi': ('mu-si', 'bird-cuckoo'),                          # cuckoo
        'tuimu': ('tui-mu', 'water-bird'),                         # cormorant/owl
        'vazonei': ('va-zonei', 'bird-stork'),                     # stork
        'thukzawin': ('thuk-zaw-in', 'deep-more-INST'),            # deeper INST
        'mitkhu': ('mit-khu', 'eye-brow'),                         # eyebrow
        'hunlopiin': ('hun-lopi-in', 'time-NEG.any-INST'),         # not at any time
        'laipiin': ('lai-pi-in', 'book-great-INST'),               # great book INST
        # Round 121: More vocabulary and suffix forms
        'khuituahin': ('khu-i-tuah-in', 'six-curtain-do-INST'),    # six curtains
        'thosakin': ('tho-sak-in', 'live-CAUS-INST'),              # living INST
        'thahatpa': ('tha-hat-pa', 'strength-strong-NMLZ'),        # mighty
        'haksapipiin': ('hak-sa-pi-pi-in', 'difficult-PAST-big-REDUP-INST'), # scarce INST
        'gimpiin': ('gim-pi-in', 'sorrow-big-INST'),               # sorrow INST
        'poplar': ('poplar', 'poplar'),                            # poplar
        'leikhop': ('lei-khop', 'earth-twelve'),                   # twelve tribes
        'kopte': ('kop-te', 'knop-PL'),                            # knops
        'gukte': ('guk-te', 'bowl-PL'),                            # bowls
        'lite': ('li-te', 'four-PL'),                              # four
        'mongte': ('mong-te', 'end-PL'),                           # ends
        'kisukha': ('ki-suk-ha', 'REFL-defile-already'),           # defiled
        'kidemnaah': ('ki-dem-na-ah', 'REFL-condemn-NMLZ-LOC'),    # condemn LOC
        'zonnain': ('zon-na-in', 'seek-NMLZ-INST'),                # seeking INST
        'khusain': ('khu-sa-in', 'feast-PAST-INST'),               # feast INST
        'kheun': ('khe-un', 'leg-3PL'),                            # legs
        'ganun': ('gan-un', 'bear-3PL'),                           # bear 3PL
        'lamun': ('lam-un', 'direction-3PL'),                      # directions
        'tula': ('tul-a', 'foot-LOC'),                             # on foot
        'gala': ('gal-a', 'little-LOC'),                           # little LOC
        'dahluain': ('dah-lua-in', 'grieve-too-INST'),             # sorrow INST
        'suntangpiin': ('sun-tang-pi-in', 'sun-before-great-INST'), # before sun INST
        'hawkkhiain': ('hawk-khia-in', 'strip-out-INST'),          # stripped INST
        'zumhuaipiin': ('zum-huai-pi-in', 'unclean-mix-great-INST'), # unclean INST
        'haksapiin': ('hak-sa-pi-in', 'difficult-PAST-great-INST'), # difficult INST
        # Round 122: Deuteronomy vocabulary
        'ngahkikin': ('ngah-kik-in', 'return-again-INST'),         # return INST
        'siasakin': ('sia-sak-in', 'bad-CAUS-INST'),               # appoint terror INST
        'vakvaiin': ('vak-vai-in', 'vagabond-REDUP-INST'),         # vagabond INST
        'hamsiatnain': ('ham-siat-na-in', 'curse-destroy-NMLZ-INST'), # curse INST
        'kumsukin': ('kum-suk-in', 'cloud-pillar-INST'),           # pillar cloud INST
        'namtuiin': ('nam-tui-in', 'sweet-savour-INST'),           # sweet savour INST
        'valhtumiin': ('valh-tum-in', 'swallow-INST'),             # swallow INST
        'khualzinnaah': ('khual-zin-na-ah', 'journey-NMLZ-LOC'),   # journey LOC
        'sawmlina': ('sawm-li-na', 'ten-four-NMLZ'),               # fortieth
        'zasakkikin': ('za-sak-kik-in', 'bring-CAUS-again-INST'),  # brought again INST
        'entoin': ('en-to-in', 'look-up-INST'),                    # look up INST
        'biakkhak': ('biak-khak', 'worship-deceive'),              # deceived worship
        'awngah': ('awng-ah', 'heap-LOC'),                         # heap LOC
        'insek': ('in-sek', 'fly-creep'),                          # flying creeping
        'khuthawm': ('khut-hawm', 'hand-empty'),                   # empty hand
        'piaknasa': ('piak-na-sa', 'give-NMLZ-PAST'),              # given
        'thukhensatna': ('thu-khen-sat-na', 'word-judge-sentence-NMLZ'), # sentence
        'khongkhaite': ('khong-khai-te', 'divine-observe-PL'),     # diviners
        'nuampa': ('nuam-pa', 'pleasant-NMLZ'),                    # worthy
        'gamlatna': ('gam-lat-na', 'land-pursue-NMLZ'),            # pursuing
        'deihzawkna': ('deih-zawk-na', 'want-more-NMLZ'),          # preferred
        'awnghawh': ('awng-hawh', 'abroad-go'),                    # go abroad
        'kiguaihna': ('ki-guaih-na', 'REFL-abomination-NMLZ'),     # abomination
        'sumgum': ('sum-gum', 'money-usury'),                      # usury
        'koihsuk': ('koih-suk', 'set-down'),                       # set down
        'nom': ('nom', 'consumption'),                             # consumption
        'meimatumte': ('mei-matum-te', 'fire-boil-PL'),            # boils
        'dalzawh': ('dal-zawh', 'fail-finish'),                    # fail
        'nasepsa': ('na-sep-sa', '2SG-work-PAST'),                 # thy labours
        'nemang': ('ne-mang', 'locust-consume'),                   # locust consume
        'cinatnate': ('ci-nat-na-te', 'sick-NMLZ-PL'),             # sicknesses
        'hintheih': ('hin-theih', 'live-able'),                    # may live
        'nunna': ('nun-na', 'desert-NMLZ'),                        # desert
        'thuknate': ('thuk-na-te', 'deep-NMLZ-PL'),                # deep things
        'hoihpenna': ('hoih-pen-na', 'good-most-NMLZ'),            # first/best
        # Round 123: Joshua/narrative vocabulary
        'khennate': ('khen-na-te', 'judge-NMLZ-PL'),               # judgments
        'nawtkhiain': ('nawt-khia-in', 'thrust-out-INST'),         # thrust out INST
        'sawlsim': ('sawl-sim', 'spy-secret'),                     # spy secretly
        'kikhentan': ('ki-khen-tan', 'REFL-cut-off'),              # cut off
        'sawlsa': ('sawl-sa', 'arm-PAST'),                         # armed
        'kansak': ('kan-sak', 'dry-CAUS'),                         # dried up
        'iplahin': ('ip-lah-in', 'accursed-thing-INST'),           # accursed INST
        'sumkoihnaah': ('sum-koih-na-ah', 'silver-set-NMLZ-LOC'),  # treasury LOC
        'khaamin': ('khaam-in', 'curse-INST'),                     # cursed INST
        'lakha': ('lak-ha', 'spoil-take'),                         # take spoil
        'hihnasa': ('hih-na-sa', 'do-NMLZ-PAST'),                  # done
        'khembawl': ('khem-bawl', 'all-work'),                     # work wilily
        'hinsak': ('hin-sak', 'live-CAUS'),                        # let live
        'suite': ('sui-te', 'hew-PL'),                             # hewers
        'tuidawk': ('tui-dawk', 'water-border'),                   # border
        'zahtak': ('zah-tak', 'fear-true'),                        # fear/dread
        'sisate': ('si-sa-te', 'blood-PAST-PL'),                   # unclean PL
        'paktat': ('pak-tat', 'harlot-deal'),                      # deal as harlot
        'theite': ('thei-te', 'fruit-PL'),                         # fruits
        'naungek': ('nau-ngek', 'child-birth'),                    # midwife
        'tuangte': ('tuang-te', 'chariot-PL'),                     # chariots
        'kikhaite': ('ki-khai-te', 'REFL-hang-PL'),                # hangings
        'dingte': ('ding-te', 'PROSP-PL'),                         # those who will (not lights)
        'thatte': ('that-te', 'kill-PL'),                          # killed PL
        'tuamtuamte': ('tuam-tuam-te', 'divers-REDUP-PL'),         # divers
        'tanaute': ('ta-nau-te', 'child-small-PL'),                # children PL
        'zawthin': ('zawn', 'north'),                              # northward
        'lungzin': ('lung-zin', 'heart-bright'),                   # noonday
        'khangham': ('khang-ham', 'generation-old'),               # old age
        'kipna': ('kip-na', 'confirm-NMLZ'),                       # confirm
        'nungzuite': ('nung-zui-te', 'back-follow-PL'),            # followers
        'pawlpite': ('pawl-pi-te', 'group-great-PL'),              # church PL
        'tonu': ('to-nu', 'lord-woman'),                           # mistress
        'koihpa': ('koih-pa', 'set-NMLZ'),                         # progenitor
        'nazatte': ('na-zat-te', '2SG-work-PL'),                   # artificers
        'sawmnihte': ('sawm-nih-te', 'ten-two-PL'),                # twenty PL
        'satpa': ('sat-pa', 'smite-NMLZ'),                         # smiter
        'saang': ('saang', 'basket'),                              # basket
        # Round 124: More narrative vocabulary
        'liangko': ('liang-ko', 'shoulder-both'),                  # both shoulders
        'liangkoah': ('liang-ko-ah', 'shoulder-both-LOC'),         # on shoulders
        'miliante': ('mi-lian-te', 'person-great-PL'),             # great men
        'siamgante': ('siam-gan-te', 'weave-work-PL'),             # weavers
        'khanghamte': ('khang-ham-te', 'generation-old-PL'),       # old ones
        'nungzui': ('nung-zui', 'back-follow'),                    # follow after
        'pawlpi': ('pawl-pi', 'group-great'),                      # church
        'tonu': ('to-nu', 'lord-woman'),                           # mistress
        'sawmnga': ('sawm-nga', 'ten-five'),                       # fifty
        'sawmngate': ('sawm-nga-te', 'ten-five-PL'),               # fifties
        'koihpa': ('koih-pa', 'put-NMLZ'),                         # progenitor
        'nazat': ('na-zat', 'hand-work'),                          # artificer
        'sawmnih': ('sawm-nih', 'ten-two'),                        # twenty
        'nengniam': ('neng-niam', 'stranger-oppress'),             # oppress stranger
        'giahphual': ('giah-phual', 'carry-pass'),                 # pass over
        'giahphualate': ('giah-phual-a-te', 'carry-pass-NOM-PL'),  # passed over PL
        'valhtumin': ('valh-tum-in', 'swallow-COMPL-INST'),        # swallow up INST
        'satpa': ('sat-pa', 'smite-NMLZ'),                         # smiter
        'muhdahhuai': ('muh-dah-huai', 'smell-bad-hateful'),       # stink
        'muhdahhuaiin': ('muh-dah-huai-in', 'smell-bad-hateful-INST'),  # stink INST
        'nesakin': ('ne-sak-in', 'eat-CAUS-INST'),                 # eating INST
        'behpa': ('beh-pa', 'capture-NMLZ'),                       # captive
        'amahmah': ('a-mah-mah', '3SG-self-self'),                 # himself
        'semsemnain': ('sem-sem-na-in', 'divide-REDUP-NMLZ-INST'), # by themselves INST
        'semsemna': ('sem-sem-na', 'divide-REDUP-NMLZ'),           # by themselves
        'thumante': ('thu-man-te', 'word-true-PL'),                # faithful PL
        # Round 127: Additional compound fixes
        'tenglai': ('teng-lai', 'dwell-time'),                      # dwelling time
        'notkik': ('not-kik', 'push-ITER'),                         # force/push repeatedly
        'paisuksak': ('pai-suk-sak', 'go-descend-CAUS'),            # force down
        'hilhkholhsa': ('hilh-kholh-sa', 'teach-warn-PERF'),        # sworn/warned
        'veikhoi': ('vei-khoi', 'cry.out-call'),                    # cry out
        'puannuai': ('puan-nuai', 'cloth-under'),                   # under raiment
        'khaknelhin': ('khak-nel-hin', 'shut-door-DECL'),           # shut/locked
        'nawtsuak': ('nawt-suak', 'sweep-away'),                    # sweep away
        'satkhamin': ('sat-kham-in', 'smite-pierce-INST'),          # smite through
        'kheging': ('khe-ging', 'foot-sound'),                      # sound of going
        'kizem': ('ki-zem', 'REFL-weave'),                          # woven
        'satui': ('sa-tui', 'meat-broth'),                          # broth
        'dinglai': ('ding-lai', 'stand-time'),                      # standing time
        'sukkhia': ('suk-khia', 'wring-out'),                       # wring out
        'simsuk': ('sim-suk', 'count-down'),                        # go down to count
        'thumun': ('thu-mun', 'word-blow'),                         # trumpet (blow)
        'kipahtawina': ('ki-pah-tawi-na', 'REFL-honor-NMLZ'),       # honor
        'kigalneihna': ('ki-gal-neih-na', 'REFL-enemy-have-NMLZ'),  # enmity
        'liim': ('liim', 'shadow'),                                  # shadow
        'liimte': ('liim-te', 'shadow-PL'),                         # shadows
        'pawldang': ('pawl-dang', 'group-other'),                   # other company
        'sawlkik': ('sawl-kik', 'send-ITER'),                       # send again
        'luahkik': ('luah-kik', 'drive.out-ITER'),                  # dispossess
        'thugenpa': ('thu-gen-pa', 'word-speak-NMLZ'),              # speaker/man
        'uap': ('u-ap', 'elder-ASSOC'),                             # companion
        'kikhihnate': ('ki-khih-na-te', 'REFL-bind-NMLZ-PL'),       # bindings
        'tolhkhia': ('tolh-khia', 'loose-out'),                     # loose from
        'ciampek': ('ciam-pek', 'mock-deceive'),                    # mock/deceive
        'gongbakte': ('gongbak-te', 'knee-PL'),                     # knees
        # Round 128: More compound fixes
        'nuainungte': ('nuai-nung-te', 'below-back-PL'),            # nether springs
        'hawlkhiamang': ('hawl-khia-mang', 'drive-out-completely'), # utterly drive out
        'omsuakin': ('om-suak-in', 'exist-become-INST'),            # shall abide
        'khegingte': ('khe-ging-te', 'foot-sound-PL'),              # wheels
        'kizemte': ('ki-zem-te', 'REFL-weave-PL'),                  # needlework PL
        'sawlkikin': ('sawl-kik-in', 'send-ITER-INST'),             # send again
        'khauhualte': ('khau-hual-te', 'cord-bind-PL'),             # cords
        'innpite': ('inn-pi-te', 'house-big-PL'),                   # pillars
        'cialin': ('ci-al-in', 'say-take-INST'),                    # thus dealeth
        'omsakin': ('om-sak-in', 'exist-CAUS-INST'),                # put before
        'khopkhat': ('khop-khat', 'gather-one'),                    # gathered together
        'dialh': ('dial-h', 'call-COMP'),                           # call/tarry
        'pangsimte': ('pang-sim-te', 'side-count-PL'),              # liers in wait
        'ciahkhawm': ('ciah-khawm', 'return-together'),             # return together
        'luata': ('lu-ata', 'head-old'),                            # old (too old)
        'khuazang': ('khua-zang', 'town-all'),                      # all the city
        'migina': ('mi-gi-na', 'person-wealth-NMLZ'),               # kinsman
        'anlate': ('an-la-te', '3PL-take-PL'),                      # reapers
        'naseppihte': ('na-sep-pih-te', '2SG-work-APPL-PL'),        # workers
        'naizaw': ('nai-zaw', 'near-more'),                         # nearer
        'lungzuang': ('lung-zuang', 'heart-feeble'),                # waxed feeble
        'hingsakkik': ('hing-sak-kik', 'live-CAUS-ITER'),           # maketh alive
        'kibiaknate': ('ki-biak-na-te', 'REFL-worship-NMLZ-PL'),    # offerings
        'kamsangin': ('kam-sang-in', 'word-establish-INST'),        # established
        'maiman': ('mai-man', 'face-true'),                         # face/name
        'hehpihnaun': ('hehpih-na-un', 'pity-NMLZ-PL.IMP'),         # mercies
        # Round 129: More partial fixes
        'tuamdang': ('tuam-dang', 'manner-other'),                  # another (manner)
        'sikseek': ('sik-seek', 'metal-forge'),                     # smith
        'seeksak': ('seek-sak', 'forge-CAUS'),                      # cause to forge
        'bawhin': ('bawh-in', 'spoil-INST'),                        # flying upon spoil
        'lungkhauhna': ('lung-khauh-na', 'heart-stubborn-NMLZ'),    # stubbornness
        'biaktheih': ('biak-theih', 'worship-able'),                # able to worship
        'omnuam': ('om-nuam', 'exist-pleasant'),                    # pleasant/comely
        'thungip': ('thu-ngip', 'word-bag'),                        # scrip/bag
        'sattukin': ('sat-tuk-in', 'strike-strike-INST'),           # smite
        'khawhcip': ('khawh-cip', 'strike-pierce'),                 # javelin
        'diksa': ('dik-sa', 'straight-very'),                       # very direct/determined
        'pangkhawm': ('pang-khawm', 'side-together'),               # stand together
        'piangsakkha': ('piang-sak-kha', 'birth-CAUS-PERF'),        # have occasioned
        'khansia': ('khan-sia', 'time-evil'),                       # evil determined
        'simlut': ('sim-lut', 'count-enter'),                       # enter midst
        # Round 130: More partial fixes
        'tawmkhatte': ('tawm-khat-te', 'few-one-PL'),               # those few
        'galsimte': ('gal-sim-te', 'enemy-count-PL'),               # spoilers
        'lotte': ('lo-te', 'arrow-PL'),                             # arrows
        'kilate': ('kila-te', 'portion-PL'),                        # portions (spoil)
        'vankahte': ('van-kah-te', 'go.and-go-PL'),                 # familiar spirits
        'vankahthei': ('van-kah-thei', 'go.and-go-able'),           # has familiar spirit
        'thahlohna': ('thah-loh-na', 'kill-NEG-NMLZ'),              # not killing (transgression)
        'sungtumna': ('sung-tum-na', 'inside-want-NMLZ'),           # coming in/going out
        'pawlpihna': ('pawl-pih-na', 'group-APPL-NMLZ'),            # rebellion/confusion
        'khiatpihin': ('khiat-pih-in', 'leave-APPL-INST'),          # led out
        # Round 131: More partial fixes
        'tuizawl': ('tui-zawl', 'water-channel'),                   # gutter
        'lungli': ('lung-li', 'heart-turn'),                        # fetch a compass
        'tangguakin': ('tang-guak-in', 'hold-uncover-INST'),        # uncovered
        'simmawhhuai': ('sim-mawh-huai', 'count-blame-full'),       # vile/base
        'maipukin': ('mai-puk-in', 'face-prostrate-INST'),          # fell on face
        'hoihhoih': ('hoih-hoih', 'good-REDUP'),                    # safely/well
        'tungsa': ('tung-sa', 'arrive-early'),                      # from youth
        'neithuah': ('nei-thuah', 'have-more'),                     # yet/more
        'thalian': ('thal-ian', 'bow-strong'),                      # giant
        'kheme': ('khem-e', 'restrain-EXCL'),                       # exclaim
        # Round 132: Hyphenated suffix fixes
        'dawngkikin': ('dawng-kik-in', 'receive-ITER-INST'),        # give in return
        'ciahsakin': ('ciah-sak-in', 'return-CAUS-INST'),           # let go
        'khanglo-in': ('khang-lo-in', 'generation-NEG-INST'),       # went away
        'samkhia-in': ('sam-khia-in', 'call-out-INST'),             # called out
        'gamdai-in': ('gam-dai-in', 'land-edge-INST'),              # with edge
        # Round 133: More partial fixes
        'bilun': ('bil-un', 'ear-PL.IMP'),                          # our ears
        'langnihin': ('lang-nih-in', 'side-two-INST'),              # on both feet
        'hehnemte': ('heh-nem-te', 'pity-comfort-PL'),              # comforters
        'heite': ('hei-te', 'saw-PL'),                              # saws (instrument)
        'sawmsimte': ('sawm-sim-te', 'incite-count-PL'),            # conspirators
        'vanlelei': ('van-le-lei', 'heaven-and-earth'),             # heaven and earth
        'sizaw': ('si-zaw', 'be-more'),                             # would I had (died)
        'nungsang': ('nung-sang', 'back-establish'),                # prospered
        'khamul-in': ('kham-ul-in', 'jaw-hold-INST'),               # by the beard
        'simna-in': ('sim-na-in', 'count-NMLZ-INST'),               # with siege
        'kisemsakte': ('ki-sem-sak-te', 'REFL-record-CAUS-PL'),     # recorder
        # Round 134: More partial fixes
        'khawmkik': ('khawm-kik', 'gather-ITER'),                   # gathered again
        'lampaina': ('lam-pai-na', 'way-go-NMLZ'),                  # going (sound of)
        'muktu': ('muk-tu', 'see.I-stumble'),                       # shook
        'kihuauna': ('ki-huau-na', 'REFL-whisper-NMLZ'),            # whispered
        'innluah': ('inn-luah', 'house-family'),                    # whole family
        'musakkik': ('mu-sak-kik', 'see.I-CAUS-ITER'),              # show me again
        'amkhamsak': ('am-kham-sak', '3SG.POSS-forbid-CAUS'),       # make afraid
        'khumzangah': ('khum-zang-ah', 'cover-all-LOC'),            # over the gate
        'netumin': ('ne-tum-in', 'eat-want-INST'),                  # consumed
        'niamsakin': ('niam-sak-in', 'low-CAUS-INST'),              # bowed down
        'kamsiat': ('kam-siat', 'word-break'),                      # calamity
        'kancip': ('kan-cip', 'turn-pierce'),                       # compassed about
        # Round 135: More partial fixes
        'beitum': ('bei-tum', 'end-want'),                          # consumed
        'milianpi': ('mi-lian-pi', 'person-great-big'),             # raised up high
        'kemnu': ('kem-nu', 'guard-woman'),                         # young virgin
        'kibawlsa': ('ki-bawl-sa', 'REFL-make-ready'),              # made ready
        'pianlim': ('pian-lim', 'create-mold'),                     # one measure
        'bangtung': ('bang-tung', 'which-arrive'),                  # lintel
        'khumkhelh': ('khum-khelh', 'cover-exceed'),                # exceeded
        'zuakkhia': ('zuak-khia', 'sell-out'),                      # bring out by means
        'omkhawmin': ('om-khawm-in', 'exist-together-INST'),        # be with
        'beisiangsak': ('bei-siang-sak', 'end-clear-CAUS'),         # take away remnant
        'numei-pasal': ('numei-pasal', 'woman-man'),                # sodomites
        'singkang': ('sing-kang', 'tree-stick'),                    # sticks
        'lungngaih': ('lung-ngaih', 'heart-wait'),                  # sleepeth
        'khutkuak': ('khut-kuak', 'hand-full'),                     # handfuls
        'khentawm': ('khen-tawm', 'divide-finish'),                 # decided
        'hawlpa': ('hawl-pa', 'seek-venture'),                      # at a venture
        # Round 136: More partial fixes
        'buante': ('buan-te', 'dust-PL'),                           # as dust
        'inndap': ('inn-dap', 'house-cover'),                       # covered house
        'innsun': ('inn-sun', 'house-side'),                        # sides of house
        'pakkual': ('pak-kual', 'throw-corner'),                    # undersetters
        'kipsaknate': ('ki-psak-na-te', 'REFL-ledge-NMLZ-PL'),      # ledges
        'vankoihna-ah': ('van-koih-na-ah', 'heaven-put-NMLZ-LOC'),  # treasures
        'zawngkhalna': ('zawng-khal-na', 'roam-consume-NMLZ'),      # consumption
        'lahnate': ('lah-na-te', 'take-NMLZ-PL'),                   # tents
        'zawngmaw': ('zawng-maw', 'roam-Q'),                        # sea navy
        'vangte': ('vang-te', 'cause-PL'),                          # cause
        'ngahkikna': ('ngah-kik-na', 'get-ITER-NMLZ'),              # bring back
        'vaikhakin': ('vai-khak-in', 'go-return-INST'),             # go back again
        'leibate': ('lei-ba-te', 'buy-owe-PL'),                     # debt
        'mainawtin': ('mai-nawt-in', 'face-pierce-INST'),           # forward smiting
        'pailai-in': ('pai-lai-in', 'go-middle-INST'),              # a day's journey
        # Round 137: More partial fixes
        'khialsakin': ('khial-sak-in', 'err-CAUS-INST'),            # slew (caused err)
        'vaihawmtawm': ('vai-hawm-tawm', 'go-gather-few'),          # portion/inheritance
        'biaknate-a': ('biak-na-te-a', 'worship-NMLZ-PL-NOM'),      # priests of high places
        'khenkhia-in': ('khen-khia-in', 'divide-out-INST'),         # cut off
        'khuangneute': ('khuang-neu-te', 'drum-small-PL'),          # timbrels
        # Round 138: More partial fixes
        'nautum': ('nau-tum', 'young-want'),                        # youngest child
        'zanni': ('zan-ni', 'yesterday-day'),                       # yesterday
        'ulianpi': ('u-lian-pi', 'elder-great-big'),                # great captain
        'delhphah': ('delh-phah', 'overcome-spread'),               # spread on face
        'puahsak': ('puah-sak', 'divide-CAUS'),                     # repair breaches
        'kuangpi': ('kuang-pi', 'trough-big'),                      # bases (brasen)
        'kikop': ('ki-kop', 'REFL-oppose'),                         # come up against
        'thukpen': ('thuk-pen', 'word-cut'),                        # messengers
        'suksiatsa': ('suk-siat-sa', 'make-break-NMLZ'),            # destroyed
        'hunhun': ('hun-hun', 'time-REDUP'),                        # continually
        'paipihtoh': ('pai-pih-toh', 'go-APPL-with'),               # bring up with
        'gentaak': ('gen-taak', 'speak-firmly'),                    # strangers (few)
        'kidoksa': ('ki-dok-sa', 'REFL-draw-NMLZ'),                 # drawn sword
        'ziahziah': ('ziah-ziah', 'willing-REDUP'),                 # willingly
        'entelin': ('en-tel-in', 'look-join-INST'),                 # seen together
        'vaihawmsa': ('vai-hawm-sa', 'go-gather-NMLZ'),             # do all things
        'zuakkhiat': ('zuak-khiat', 'sell-depart'),                 # brought forth
        'tawpsak': ('tawp-sak', 'end-CAUS'),                        # let cease
        # Round 139: More partial fixes (NMLZ forms)
        'kingapna': ('ki-ngap-na', 'REFL-lean-NMLZ'),               # leaning
        'liamsakna': ('liam-sak-na', 'wound-CAUS-NMLZ'),            # wounds
        'tecipanna': ('te-ci-pan-na', 'PL-say-arrive-NMLZ'),        # testimony
        'kilawmtatna': ('ki-lawm-tat-na', 'REFL-agree-cut-NMLZ'),   # betray
        'kisehkhenna': ('ki-seh-khen-na', 'REFL-set-divide-NMLZ'),  # divisions
        'sawmlinga': ('sawm-ling-a', 'ten-round-NOM'),              # ten in cubit
        'thuciamsa': ('thu-ciam-sa', 'word-promise-NMLZ'),          # promised
        # Round 140: More partial fixes (PL forms)
        'sakite': ('sak-i-te', 'CAUS-PST-PL'),                      # cymbals/instruments
        'sakzawk': ('sak-zawk', 'cause-more'),                      # greatly (feared)
        'nisima': ('ni-sim-a', 'day-count-NOM'),                    # every day
        'kisimte': ('ki-sim-te', 'REFL-count-PL'),                  # numbered ones
        'haipite': ('hai-pi-te', 'spear-big-PL'),                   # fleshhooks
        'liatnate': ('liat-na-te', 'great-NMLZ-PL'),                # greatness (things)
        'pemtate': ('pem-ta-te', 'sojourn-NMLZ-PL'),                # sojourners
        'golzawte': ('gol-zaw-te', 'hundred-more-PL'),              # greatest over hundred
        'neuzawte': ('neu-zaw-te', 'small-more-PL'),                # least over hundred
        'pahtawihuai': ('pah-tawi-huai', 'father-sorrow-full'),     # bare with sorrow
        # Round 141: More partial fixes
        'paangah': ('pang-ah', 'nail-LOC'),                         # nail into temples
        'thukkhia': ('thuk-khia', 'word-out'),                      # poured out
        'kamdawn': ('kam-dawn', 'word-perceive'),                   # hear rumor
        'innlimah': ('inn-lim-ah', 'house-pillar-LOC'),             # in the pillars
        'sangzaw': ('sang-zaw', 'high-more'),                       # taller
        # Round 142: More partial fixes
        'bawngnawi': ('bawng-nawi', 'cow-meat'),                    # butter (calf meat)
        'tutna': ('tut-na', 'sleep-NMLZ'),                          # bed/lying place
        'phatna': ('phat-na', 'praise-NMLZ'),                       # song/praise
        'hoihna': ('hoih-na', 'good-NMLZ'),                         # goodness/pleasantness
        'sagihna': ('sagih-na', 'seven-NMLZ'),                      # seventh
        'zahtakna': ('zahtak-na', 'fear-NMLZ'),                     # fear (of God)
        'hihna': ('hih-na', 'be-NMLZ'),                             # being/existence
        'zanpi': ('zan-pi', 'night-big'),                           # in the night
        'zuazuate': ('zuazua-te', 'willing-PL'),                    # freewill offerings
        'namcin': ('nam-cin', 'nation-say'),                        # salutation
        'khuak': ('khu-ak', 'bed-place'),                           # sepulchre/bed
        # Round 143: Suffix forms
        'pahtawina': ('pah-tawi-na', 'feast-sorrow-NMLZ'),          # unleavened feast
        'cianna': ('cian-na', 'announce-NMLZ'),                     # indignation/announcement
        'mualbo': ('mual-bo', 'hill-tower'),                        # great tower
        'thupi': ('thu-pi', 'word-big'),                            # honourable
        'dingpi': ('ding-pi', 'stand-big'),                         # no good
        'khuamialna': ('khua-mial-na', 'town-dark-NMLZ'),           # darkness
        'pilzaw': ('pil-zaw', 'wise-more'),                         # wiser
        'hawmpi': ('hawm-pi', 'join-big'),                          # order speech
        'cingh': ('cing-h', 'lend-COMP'),                           # surely lend
        'muanhuai': ('muan-huai', 'trust-full'),                    # gathered cattle
        'khinta': ('khin-ta', 'move-NMLZ'),                         # given
        'ngakngakna': ('ngak-ngak-na', 'wait-REDUP-NMLZ'),          # waiting
        'tuamtuamte': ('tuam-tuam-te', 'kind-REDUP-PL'),            # after its kind
        # Round 144: Unknown fixes
        'lamna': ('lam-na', 'way-NMLZ'),                            # dancing
        'kiimnai': ('ki-im-nai', 'REFL-stay-near'),                 # none remaining
        'hehsa': ('heh-sa', 'angry-NMLZ'),                          # anger (kindled)
        'hutna': ('hut-na', 'escape-NMLZ'),                         # escape/saving
        'khekna': ('khek-na', 'give.in-NMLZ'),                      # give in exchange
        'khimsakin': ('khim-sak-in', 'crown-CAUS-INST'),            # put crown
        'kiphasakte': ('ki-pha-sak-te', 'REFL-good-CAUS-PL'),       # afflicted saved
        'kisukha': ('ki-suk-ha', 'REFL-move-PERF'),                 # put out
        'kimawlsak': ('ki-mawl-sak', 'REFL-mock-CAUS'),             # made sport
        'ngunseek': ('ngun-seek', 'silver-forge'),                  # founder (silversmith)
        'otsan': ('ot-san', 'cry-voice'),                           # aileth
        'lanluat': ('lan-luat', 'show-fold'),                       # lewdness
        'dahmai': ('dah-mai', 'sad-face'),                          # sad countenance
        # Round 145: High-frequency partial fixes
        '-': ('-', 'PUNCT'),                                        # 110x - em dash punctuation
        'mangpa': ('mang-pa', 'chief-father'),                      # 7x - chief captain
        "mangpa'": ("mang-pa'", 'chief-father.POSS'),               # 7x - chief's
        'lamna-a': ('lam-na-a', 'way-NMLZ-LOC'),                    # 6x - in the way/direction
        'kiimnai-a': ('ki-im-nai-a', 'REFL-stay-near-LOC'),         # 6x - at neighboring place
        'hehsa-in': ('heh-sa-in', 'angry-NMLZ-ERG'),                # 6x - with anger
        'gan-an': ('gan-an', 'possess-?'),                          # 5x - possessions? (context: substance)
        'lam-an': ('lam-an', 'way-?'),                              # 5x - way/direction variant
        'eh': ('eh', 'INTERJ'),                                     # 5x - interjection
        'hutna-in': ('hut-na-in', 'shelter-NMLZ-ERG'),              # 5x - by refuge
        'pipi-in': ('pi-pi-in', 'grind-REDUP-ERG'),                 # 5x - by grinding
        "hi'ng": ("hi-'ng", 'be-EMPH'),                             # 5x - emphatic be
        # Round 146: More partial fixes
        "se-alte'": ('se-al-te', 'jackal-PL.POSS'),                  # 4x - jackals'/dragons'
        'se-alte': ('se-al-te', 'jackal-PL'),                        # jackals/dragons
        'se-al': ('se-al', 'jackal'),                                # jackal/dragon
        "kua-a'": ('kua-a', 'who-NOM.POSS'),                         # 3x - who's
        'khekna-in': ('khek-na-in', 'exchange-NMLZ-ERG'),            # 3x - in exchange
        "phulapa'": ('phu-la-pa', 'avenger-NMLZ-M.POSS'),            # 3x - avenger's
        'phulapa': ('phu-la-pa', 'avenge-NMLZ-M'),                   # avenger (of blood)
        "thahatte'": ('tha-hat-te', 'strength-strong-PL.POSS'),      # 3x - mighty ones'
        'thahatte': ('tha-hat-te', 'strength-strong-PL'),            # mighty ones
        "tupa'": ('tu-pa', 'grandson-M.POSS'),                       # 3x - grandson's
        'tupa': ('tu-pa', 'grandson-M'),                             # grandson
        "meigongnu'": ('mei-gong-nu', 'fire-alone-F.POSS'),          # 3x - widow's
        'meigongnu': ('mei-gong-nu', 'fire-alone-F'),                # widow
        "kilin'": ('ki-lin', 'REFL-shake.POSS'),                     # 3x - quaking's
        'kilin': ('ki-lin', 'REFL-shake'),                           # quake
        'kiling': ('ki-ling', 'REFL-shake'),                         # quaked
        'khe-a': ('khe-a', 'foot-LOC'),                              # 3x - at foot
        "gulpi'": ('gul-pi', 'serpent-big.POSS'),                    # 3x - serpent's
        'gulpi': ('gul-pi', 'serpent-big'),                          # serpent
        "kiphasakte'": ('ki-pha-sak-te', 'REFL-good-CAUS-PL.POSS'),  # 3x - saved ones'
        "thahatpa'": ('tha-hat-pa', 'strength-strong-M.POSS'),       # 3x - mighty man's
        'thahatpa': ('tha-hat-pa', 'strength-strong-M'),             # mighty man
        # Round 147: More 2x partial fixes
        'gan-an': ('gan-an', 'possess-ERG'),                         # 5x - possessions (substance)
        'lam-an': ('lam-an', 'way-ERG'),                              # 5x - way/direction 
        "sungpa'": ('sung-pa', 'inside-M.POSS'),                      # 2x - father-in-law's
        'sungpa': ('sung-pa', 'inside-M'),                            # father-in-law
        "kopte'": ('kop-te', 'frog-PL.POSS'),                         # 2x - frogs'
        'kopte': ('kop-te', 'frog-PL'),                               # frogs
        "gukte'": ('guk-te', 'lice-PL.POSS'),                         # 2x - lice's
        'gukte': ('guk-te', 'lice-PL'),                               # lice
        "lite'": ('li-te', 'river-PL.POSS'),                          # 2x - rivers'
        'lite': ('li-te', 'river-PL'),                                # rivers
        "sun'": ('sun', 'day.POSS'),                                  # 2x - day's
        'mongte-ah': ('mong-te-ah', 'throat-PL-LOC'),                 # 2x - at throats/necks
        'mongte': ('mong-te', 'throat-PL'),                           # throats/necks
        'li-a': ('li-a', 'river-LOC'),                                # 2x - at river/four
        "phakpa'": ('phak-pa', 'able-M.POSS'),                        # 2x - able one's
        'phakpa': ('phak-pa', 'able-M'),                              # able one
        "suante-a'": ('suan-te-a', 'descendant-PL-LOC.POSS'),         # 2x - descendants' place
        'suante': ('suan-te', 'descendant-PL'),                       # descendants/dukes
        "lehpan'": ('leh-pan', 'change-side.POSS'),                   # 2x - change's
        "tecite'": ('teci-te', 'witness-PL.POSS'),                    # 2x - witnesses'
        'tecite': ('teci-te', 'witness-PL'),                          # witnesses
        "peuhpeuhte'": ('peuh-peuh-te', 'every-REDUP-PL.POSS'),       # 2x - everyone's
        "tuutalte'": ('tuu-tal-te', 'flock-POSS-PL.POSS'),            # 2x - flocks'
        'tuutalte': ('tuu-tal-te', 'flock-POSS-PL'),                  # flocks
        'tau-a': ('tau-a', 'spear-LOC'),                              # 2x - at spear
        "luite'": ('lui-te', 'river-PL.POSS'),                        # 2x - rivers'
        'luite': ('lui-te', 'river-PL'),                              # rivers
        "hangte'": ('hang-te', 'reason-PL.POSS'),                     # 2x - reasons'
        'hangte': ('hang-te', 'reason-PL'),                           # reasons
        "kungte'": ('kung-te', 'tree-PL.POSS'),                       # 2x - trees'
        'kungte': ('kung-te', 'tree-PL'),                             # trees
        "mavan'": ('ma-van', 'before-sky.POSS'),                      # 2x - beforehand
        "nihna'": ('nih-na', 'two-NMLZ.POSS'),                        # 2x - second's
        'suanpa': ('suan-pa', 'descendant-M'),                        # 2x - descendant/duke
        # Round 148: Large batch of 2x partials
        'kisukha-in': ('ki-suk-ha-in', 'REFL-move-out-ERG'),          # 2x - put out
        'kisukha': ('ki-suk-ha', 'REFL-move-out'),                    # put out
        'dengzanin': ('deng-zan-in', 'cut-break-ERG'),                # 2x - break down
        'dengzan': ('deng-zan', 'cut-break'),                         # break down
        'tawsakin': ('taw-sak-in', 'blind-CAUS-ERG'),                 # 2x - smite blind
        'tawsak': ('taw-sak', 'blind-CAUS'),                          # smite blind
        'ngeksuak': ('ngek-suak', 'tender-become'),                   # 2x - tender/delicate
        'tamkham': ('tam-kham', 'many-break'),                        # 2x - broken to pieces
        'mangkha': ('mang-kha', 'dream-wake'),                        # 2x - dream
        'ot': ('ot', 'cry.out'),                                      # 2x - cry/wail
        'kipuksuk': ('ki-puk-suk', 'REFL-fall-move'),                 # 2x - prostrate
        'phulkhap': ('phul-khap', 'avenge-join'),                     # 2x - avenge
        'tuaklo': ('tuak-lo', 'encounter-NEG'),                       # 2x - without meeting
        'seelcipzo': ('seel-cip-zo', 'press-squeeze-COMPL'),          # 2x - pressed
        'kisiit': ('ki-siit', 'REFL-wipe'),                           # 2x - wipe self
        'kidiahin': ('ki-diah-in', 'REFL-level-ERG'),                 # 2x - level/even
        'phualkip': ('phual-kip', 'outside-completely'),              # 2x - completely outside
        'phulin': ('phul-in', 'avenge-ERG'),                          # 2x - avenging
        'laphuah': ('la-phuah', 'song-compose'),                      # 2x - compose song
        'phungmai': ('phung-mai', 'law-face'),                        # 2x - before law
        'kihui': ('ki-hui', 'REFL-gather'),                           # 2x - gather together
        'dap': ('dap', 'war'),                                        # 2x - battle/war
        'kihuiheek': ('ki-hui-heek', 'REFL-gather-scatter'),          # 2x - scatter
        'tasam': ('ta-sam', 'child-call'),                            # 2x - adopt
        'guallelh': ('gual-lelh', 'outside-change'),                  # 2x - substitute
        "mante'": ('man-te', 'price-PL.POSS'),                        # 2x - prices'
        'mante': ('man-te', 'price-PL'),                              # prices
        'tazo': ('ta-zo', 'child-COMPL'),                             # 2x - fully born
        'vuknelh': ('vuk-nelh', 'wash-again'),                        # 2x - wash again
        'gimbawlin': ('gim-bawl-in', 'difficulty-make-ERG'),          # 2x - make difficulty
        'giklua': ('gik-lua', 'fall-exceed'),                         # 2x - fall greatly
        "khangnote'": ('khang-no-te', 'generation-young-PL.POSS'),    # 2x - young generation's
        'phualte-ah': ('phual-te-ah', 'outside-PL-LOC'),              # 2x - at outside
        'phiatsiang': ('phiat-siang', 'throw-clean'),                 # 2x - throw away clean
        'kikhuangin': ('ki-khuang-in', 'REFL-shake-ERG'),             # 2x - shaking
        'kikhuang': ('ki-khuang', 'REFL-shake'),                      # shake
        'kisun': ('ki-sun', 'REFL-day'),                              # 2x - daily
        'manlahin': ('man-lah-in', 'price-take-ERG'),                 # 2x - redeeming
        'kingamin': ('ki-ngam-in', 'REFL-dare-ERG'),                  # 2x - daring
        'kulhzangah': ('kulh-zang-ah', 'wall-middle-LOC'),            # 2x - at wall
        'kikeeksa': ('ki-keek-sa', 'REFL-bend-PAST'),                 # 2x - bowed
        'tawmto': ('tawm-to', 'short-stay'),                          # 2x - brief stay
        'gukvei': ('guk-vei', 'louse-time'),                          # 2x - lice time?
        'lamlah': ('lam-lah', 'way-take'),                            # 2x - lead way
        'gahto': ('gah-to', 'fruit-stay'),                            # 2x - remain fruit
        'lehkaih': ('leh-kaih', 'change-turn'),                       # 2x - turn back
        'tuanthu': ('tuan-thu', 'tell-word'),                         # 2x - tell story
        "pun'": ('pun', 'multiply.POSS'),                             # 2x - multiply's
        "semte'": ('sem-te', 'serve-PL.POSS'),                        # 2x - servants'
        'semte': ('sem-te', 'serve-PL'),                              # servants
        'khelbawl': ('khel-bawl', 'deceive-make'),                    # 2x - practice deception
        "kithatte'": ('ki-that-te', 'REFL-kill-PL.POSS'),             # 2x - slain ones'
        'taigawp': ('tai-gawp', 'flee-cover'),                        # 2x - flee covering
        'susiapa': ('su-sia-pa', 'enemy-bad-M'),                      # 2x - adversary
        'lengzong': ('leng-zong', 'king-even'),                       # 2x - even king
        'kulhkongpi-a': ('kulh-kong-pi-a', 'wall-gate-big-LOC'),      # 2x - at big gate
        'suangdawk': ('suang-dawk', 'stone-pound'),                   # 2x - pound stone
        "hen'": ('hen', 'let.POSS'),                                  # 2x - let's
        # Round 149: More 2x partial fixes
        'kinawngkaisak': ('ki-nawng-kai-sak', 'REFL-help-turn-CAUS'), # 2x - help turn
        'lelhtuak': ('lelh-tuak', 'change-meet'),                     # 2x - change meeting
        'kinuaisiah': ('ki-nuai-siah', 'REFL-below-descend'),         # 2x - descend below
        'kuppih': ('kup-pih', 'cover-CAUS'),                          # 2x - cause cover
        'kitamkham': ('ki-tam-kham', 'REFL-many-break'),              # 2x - broken many
        'phuksakin': ('phuk-sak-in', 'fell-CAUS-ERG'),                # 2x - cause to fall
        'gukhia-in': ('guk-khia-in', 'louse-exit-ERG'),               # 2x - lice emerge
        'batsakkik': ('bat-sak-kik', 'bind-CAUS-ITER'),               # 2x - bind again
        'piangvat': ('piang-vat', 'be.born-time'),                    # 2x - birth time
        'bawlthuah': ('bawl-thuah', 'make-success'),                  # 2x - make succeed
        'kitheihthang': ('ki-theih-thang', 'REFL-know-able'),         # 2x - be known
        'lomte': ('lom-te', 'warm-PL'),                               # 2x - warm ones
        'kimakai': ('ki-ma-kai', 'REFL-front-reach'),                 # 2x - reach front
        'tuubukte': ('tuu-buk-te', 'flock-fold-PL'),                  # 2x - sheepfolds
        'kutna': ('kut-na', 'hand-NMLZ'),                             # 2x - handiwork
        'kihelkim': ('ki-hel-kim', 'REFL-deceive-complete'),          # 2x - fully deceive
        'pawlpawl': ('pawl-pawl', 'group-REDUP'),                     # 2x - various groups
        'kihihna': ('ki-hih-na', 'REFL-be-NMLZ'),                     # 2x - being
        'zakiasak': ('zak-ia-sak', 'hear.II-NOM-CAUS'),               # 2x - cause hear
        'kinusiat': ('ki-nu-siat', 'REFL-mother-destroy'),            # 2x - mother destroy
        'pamte': ('pam-te', 'arm-PL'),                                # 2x - arms
        'behlephung': ('beh-le-phung', 'tribe-and-family'),           # 2x - tribes families
        'khekhat': ('khe-khat', 'foot-one'),                          # 2x - one foot
        'daltuah': ('dal-tuah', 'hinder-success'),                    # 2x - successfully hinder
        'mangpite': ('mang-pi-te', 'chief-big-PL'),                   # 2x - chief captains
        'losap': ('lo-sap', 'field-work'),                            # 2x - field work
        'kisukcipna': ('ki-suk-cip-na', 'REFL-move-press-NMLZ'),      # 2x - pressing
        'kikanna': ('ki-kan-na', 'REFL-dry-NMLZ'),                    # 2x - drying
        'kisepna': ('ki-sep-na', 'REFL-work-NMLZ'),                   # 2x - working
        'thuzaksakna': ('thu-zak-sak-na', 'word-hear-CAUS-NMLZ'),     # 2x - causing hear
        'telh': ('telh', 'add'),                                      # 2x - add
        'kipaipihna': ('ki-pai-pih-na', 'REFL-go-CAUS-NMLZ'),         # 2x - going together
        'semsakkik': ('sem-sak-kik', 'serve-CAUS-ITER'),              # 2x - serve again
        'siampipihte': ('siam-pi-pih-te', 'skilled-big-CAUS-PL'),     # 2x - skilled ones
        'tungto': ('tung-to', 'arrive-remain'),                       # 2x - arrive stay
        'sinin': ('si-nin', 'die-seem'),                              # 2x - seem to die
        'puakkhawm': ('puak-khawm', 'send-together'),                 # 2x - send together
        'nungpai': ('nung-pai', 'live-go'),                           # 2x - go living
        'thakna': ('thak-na', 'new-NMLZ'),                            # 2x - newness
        'kilawmzah': ('ki-lawm-zah', 'REFL-sufficient-respect'),      # 2x - sufficient respect
        'kiu-a': ('kiu-a', 'call-LOC'),                               # 2x - at call
        'kuanun': ('kuan-un', 'carry-PL'),                            # 2x - carry PL
        'zahzahin': ('zah-zah-in', 'respect-REDUP-ERG'),              # 2x - respectfully
        'singkhia': ('sing-khia', 'tree-exit'),                       # 2x - tree sprout
        'gikpi': ('gik-pi', 'fall-big'),                              # 2x - big fall
        'kisutuah': ('ki-su-tuah', 'REFL-enemy-defeat'),              # 2x - defeat enemy
        'taseleh': ('ta-se-leh', 'child-small-and'),                  # 2x - and small child
        'livei': ('li-vei', 'river-time'),                            # 2x - river time
        "masate'": ('masa-te', 'first-PL.POSS'),                      # 2x - firstborn's
        'masate': ('masa-te', 'first-PL'),                            # firstborn
        'kikhawmtuah': ('ki-khawm-tuah', 'REFL-gather-succeed'),      # 2x - gather succeed
        'tuilim': ('tui-lim', 'water-submerge'),                      # 2x - water submerge
        'suanglot': ('suang-lot', 'stone-loosen'),                    # 2x - loosen stone
        'vahsak': ('vah-sak', 'go-CAUS'),                             # 2x - cause go
        'phulsak': ('phul-sak', 'avenge-CAUS'),                       # 2x - cause avenge
        'gendai': ('gen-dai', 'speak-hinder'),                        # 2x - hinder speech
        'sialo': ('sia-lo', 'bad-NEG'),                               # 2x - not bad
        'ngaihsutsak': ('ngaihsut-sak', 'think-CAUS'),                # 2x - cause think
        'teltheihna': ('tel-theih-na', 'add-able-NMLZ'),              # 2x - ability to add
        # Round 150: Final push to 99%
        'neu-a': ('neu-a', 'small-LOC'),                              # 2x - at small
        'neu-in': ('neu-in', 'small-ERG'),                            # 2x - with small
        'neu-et': ('neu-et', 'small-until'),                          # 2x - until small
        'neu': ('neu', 'small'),                                      # small
        'tutna-ah': ('tut-na-ah', 'sleep-NMLZ-LOC'),                  # 2x - at sleep
        'phatna-ah': ('phat-na-ah', 'praise-NMLZ-LOC'),               # 2x - at praise
        'phatna-in': ('phat-na-in', 'praise-NMLZ-ERG'),               # 2x - with praise
        'phatna': ('phat-na', 'praise-NMLZ'),                         # praise
        'hoihna-ah': ('hoih-na-ah', 'good-NMLZ-LOC'),                 # 2x - at goodness
        'hoihna': ('hoih-na', 'good-NMLZ'),                           # goodness
        'hihna-ah': ('hih-na-ah', 'be-NMLZ-LOC'),                     # 2x - at being
        'cianna-ah': ('cian-na-ah', 'announce-NMLZ-LOC'),             # 2x - at announcing
        'cianna': ('cian-na', 'announce-NMLZ'),                       # announcing
        'zahtakna-in': ('zahtak-na-in', 'honor-NMLZ-ERG'),            # 2x - with honor
        'khangno-in': ('khang-no-in', 'generation-young-ERG'),        # 2x - young generation
        'khangno': ('khang-no', 'generation-young'),                  # young generation
        'sangzaw-in': ('sang-zaw-in', 'high-more-ERG'),               # 2x - more highly
        'sangzaw': ('sang-zaw', 'high-more'),                         # higher
        'zato': ('za-to', 'hear.I-remain'),                           # 2x - remain hearing
        'sukmang': ('suk-mang', 'make-chief'),                        # 2x - make chief
        'ahihloh': ('a-hih-loh', '3SG-be-fail'),                      # 2x - if not
        'thumnop': ('thum-nop', 'three-willing'),                     # 2x - three willing
        'tengbek': ('teng-bek', 'dwell-only'),                        # 2x - dwell only
        'phutsak': ('phut-sak', 'spray-CAUS'),                        # 2x - cause spray
        'hehpihzawh': ('heh-pih-zawh', 'angry-CAUS-able'),            # 2x - able to anger
        'kiginkholh': ('ki-gin-kholh', 'REFL-fear-wrap'),             # 2x - fearfully wrap
        'khaisak': ('khai-sak', 'lift-CAUS'),                         # 2x - cause lift
        'tuamtuama': ('tuam-tuam-a', 'various-REDUP-LOC'),            # 2x - at various
        'kikhaina': ('ki-khai-na', 'REFL-lift-NMLZ'),                 # 2x - lifting
        'kitanna': ('ki-tan-na', 'REFL-stand-NMLZ'),                  # 2x - standing
        'khantohna': ('khan-toh-na', 'spirit-reach-NMLZ'),            # 2x - spiritual reaching
        'kikhit': ('ki-khit', 'REFL-finish'),                         # 2x - finish self
        'phehlehna': ('pheh-leh-na', 'throw-back-NMLZ'),              # 2x - throwing back
        'lawnto': ('lawn-to', 'cross-remain'),                        # 2x - remain crossing
        'kipaii': ('ki-pai-i', 'REFL-go-NOM'),                        # 2x - going
        'hepkhiatsak': ('hep-khiat-sak', 'shake-off-CAUS'),           # 2x - shake off
        'ngeungau': ('ngeu-ngau', 'shake-REDUP'),                     # 2x - shake
        'mot': ('mot', 'ant'),                                        # 2x - ant
        'luipi': ('lui-pi', 'river-big'),                             # 2x - big river
        'khuasikmul': ('khua-sik-mul', 'town-cool-hill'),             # 2x - cool town hill
        'piangtawm': ('piang-tawm', 'be.born-short'),                 # 2x - born briefly
        'dahte': ('dah-te', 'sad-PL'),                                # 2x - sad ones
        'lumletsak': ('lum-let-sak', 'warm-change-CAUS'),             # 2x - cause warm
        'puksih': ('puk-sih', 'fall-die'),                            # 2x - fall and die
        'kitawikhai': ('ki-tawi-khai', 'REFL-short-lift'),            # 2x - lift shortly
        'gikzaw': ('gik-zaw', 'fall-more'),                           # 2x - fall more
        'kihehnepna': ('ki-heh-nep-na', 'REFL-angry-press-NMLZ'),     # 2x - angry pressing
        'suksiatgawp': ('suk-siat-gawp', 'make-destroy-cover'),       # 2x - destroy covering
        'hilhhelh': ('hilh-helh', 'teach-wrong'),                     # 2x - teach wrongly
        'zungbawh': ('zung-bawh', 'root-spread'),                     # 2x - spread root
        'zawhzawh': ('zawh-zawh', 'able-REDUP'),                      # 2x - very able
        'thupi-in': ('thu-pi-in', 'word-big-ERG'),                    # 2x - with big word
        'dahnate': ('dah-na-te', 'sad-NMLZ-PL'),                      # 2x - sadnesses
        'paih': ('pai-h', 'go-COMP'),                                 # 2x - go (completed)
        'thuthukte': ('thu-thuk-te', 'word-deep-PL'),                 # 2x - deep words
        'vakvaisak': ('vak-vai-sak', 'walk-around-CAUS'),             # 2x - cause walk
        'dingpi-in': ('ding-pi-in', 'stand-big-ERG'),                 # 2x - standing big
        'seello': ('seel-lo', 'press-NEG'),                           # 2x - not press
        'pilnate': ('pil-na-te', 'learn-NMLZ-PL'),                    # 2x - learnings
        'nialnial': ('nial-nial', 'argue-REDUP'),                     # 2x - argue much
        'kikhek': ('ki-khek', 'REFL-exchange'),                       # 2x - exchange self
        'gawlin': ('gawl-in', 'empty-ERG'),                           # 2x - emptily
        'thuumsak': ('thuum-sak', 'believe-CAUS'),                    # 2x - cause believe
        'bungbu': ('bung-bu', 'cave-hole'),                           # 2x - cave
        'kisiah': ('ki-siah', 'REFL-descend'),                        # 2x - descend
        "nungtate'": ('nungta-te', 'live-PL.POSS'),                   # 2x - living ones'
        'mialcipsak': ('mial-cip-sak', 'dark-press-CAUS'),            # 2x - cause darken
        'midangpi': ('mi-dang-pi', 'person-other-big'),               # 2x - great stranger
        'siakhia': ('sia-khia', 'bad-exit'),                          # 2x - go bad
        'dangtawng': ('dang-tawng', 'other-language'),                # 2x - other language
        'zangkha': ('zang-kha', 'use-wake'),                          # 2x - use awake
        'lamsate': ('lam-sa-te', 'wild-beast-PL'),                    # 2x - wild beasts
        'duhduh': ('duh-duh', 'want-REDUP'),                          # 2x - much want
        'keuhkeuh': ('keuh-keuh', 'dig-REDUP'),                       # 2x - dig much
        'kholsa': ('khol-sa', 'denounce-PAST'),                       # 2x - denounced
        'khantosak': ('khan-to-sak', 'spirit-stay-CAUS'),             # 2x - spiritual stay
        'punna': ('pun-na', 'multiply-NMLZ'),                         # 2x - multiplying
        'kisukmitsak': ('ki-suk-mit-sak', 'REFL-move-eye-CAUS'),      # 2x - cause eye move
        'buhsi': ('buh-si', 'rice-die'),                              # 2x - rice die
        'lunggimin': ('lung-gim-in', 'heart-pain-ERG'),               # 2x - with pain
        'nopnate': ('nop-na-te', 'willing-NMLZ-PL'),                  # 2x - willingnesses
        'kivuk': ('ki-vuk', 'REFL-wash'),                             # 2x - wash self
        'taai': ('taai', 'flee'),                                     # 2x - flee
        'langpan': ('lang-pan', 'side-from'),                         # 2x - from side
        "tagahte'": ('ta-gah-te', 'child-fruit-PL.POSS'),             # 2x - offspring's
        'tagahte': ('ta-gah-te', 'child-fruit-PL'),                   # offspring
        'neihsunte': ('neih-sun-te', 'have-day-PL'),                  # 2x - daily having
        'gawi-in': ('gawi-in', 'hook-ERG'),                           # 2x - with hook
        "meigongte'": ('mei-gong-te', 'fire-alone-PL.POSS'),          # 2x - widows'
        'meigongte': ('mei-gong-te', 'fire-alone-PL'),                # widows
        'seelcipsak': ('seel-cip-sak', 'press-squeeze-CAUS'),         # 2x - cause press
        'kisakna': ('ki-sak-na', 'REFL-CAUS-NMLZ'),                   # 2x - causing
        'leenkhia-in': ('leen-khia-in', 'lean-exit-ERG'),             # 2x - leaning out
        'kitawh': ('ki-tawh', 'REFL-COM'),                            # 2x - with self
        'leivuite': ('lei-vui-te', 'earth-dust-PL'),                  # 2x - dusts
        'tawhvang': ('tawh-vang', 'with-because'),                    # 2x - because with
        'nomsak': ('nom-sak', 'rest-CAUS'),                           # 2x - cause rest
        'maigumna': ('mai-gum-na', 'face-bow-NMLZ'),                  # 2x - face bowing
        'singzung': ('sing-zung', 'tree-trunk'),                      # 2x - tree trunk
        'sawlkawm': ('sawl-kawm', 'send-together'),                   # 2x - send together
        'hoihlua': ('hoih-lua', 'good-exceed'),                       # 2x - exceed good
        'guaksuaksak': ('guak-suak-sak', 'cry-become-CAUS'),          # 2x - cause cry
        'koihkhong': ('koih-khong', 'put-closed'),                    # 2x - put closed
        'buisum': ('bui-sum', 'round-three'),                         # 2x - three rounds
        'ngaingai': ('ngai-ngai', 'listen-REDUP'),                    # 2x - listen well
        'mawkphat': ('mawk-phat', 'only-reach'),                      # 2x - only reach
        'limpen': ('lim-pen', 'sign-most'),                           # 2x - most sign
        'sipak': ('si-pak', 'die-side'),                              # 2x - die aside
        'cihpih': ('cih-pih', 'say-CAUS'),                            # 2x - cause say
        'talecin': ('tale-cin', 'wave-move'),                         # 2x - move wave
        'pilzaw-in': ('pil-zaw-in', 'learn-more-ERG'),                # 2x - learning more
        'vangliat': ('vang-liat', 'power-strong'),                    # 2x - strong power
        'hawmpi-in': ('hawm-pi-in', 'join-big-ERG'),                  # 2x - joining big
        'vialcip': ('vial-cip', 'encircle-press'),                    # 2x - press encircle
        'taanglua': ('taang-lua', 'poor-exceed'),                     # 2x - exceed poor
        'uksawnte': ('uk-sawn-te', 'rule-teach-PL'),                  # 2x - ruling teachers
        "mangte'": ('mang-te', 'chief-PL.POSS'),                      # 2x - chiefs'
        'mangte': ('mang-te', 'chief-PL'),                            # chiefs
        "kigin'": ('ki-gin', 'REFL-fear.POSS'),                       # 2x - fearing's
        'kigin': ('ki-gin', 'REFL-fear'),                             # fearing
        'kipuahin': ('ki-puah-in', 'REFL-send-ERG'),                  # 2x - sending self
        'kize-etna': ('ki-zeet-na', 'REFL-rub-NMLZ'),                 # 2x - rubbing
        'tawngnungah': ('tawng-nung-ah', 'language-after-LOC'),       # 2x - at latter
        'sagihna-a': ('sagih-na-a', 'seven-NMLZ-LOC'),                # 2x - at seventh
        'thukna-in': ('thuk-na-in', 'deep-NMLZ-ERG'),                 # 2x - deeply
        'omlai-un': ('om-lai-un', 'exist-midst-PL'),                  # 2x - in midst PL
        'paihna': ('paih-na', 'go.COMP-NMLZ'),                        # 2x - going
        'tuamtuamte-ah': ('tuam-tuam-te-ah', 'various-REDUP-PL-LOC'), # 2x - at various
        # Round 151: Prefix mis-segmentation fixes
        # These words start with what looks like a prefix but isn't
        'innkuan': ('inn-kuan', 'house-family'),                  # household (not i-nnkuan)
        'innkuan-a': ('inn-kuan-a', 'house-family-LOC'),          # at household
        'innkuanpih': ('inn-kuan-pih', 'house-family-all'),       # whole household
        'innkuante': ('inn-kuan-te', 'house-family-PL'),          # households
        'angvan': ('ang-van', 'bright-sky'),                      # brightness/radiance
        'angvanin': ('ang-van-in', 'bright-sky-ERG'),             # brightly
        'angvanna': ('ang-van-na', 'bright-sky-NMLZ'),            # brightness
        'kankhia': ('kan-khia', 'firmly-exit'),                   # firmly exit (not ka-nkhia)
        'kahlei': ('kah-lei', 'behind-earth'),                    # behind/back
        'kahlei-ah': ('kah-lei-ah', 'behind-earth-LOC'),          # at behind
        'ansite': ('an-site', 'others-?'),                        # others (not a-nsite)
        'anvai': ('an-vai', 'PL-go'),                             # they go
        'anlate': ('an-la-te', 'PL-take-PL'),                     # they take
        'kampau': ('kam-pau', 'word-speak'),                      # speak words
        'kampau-in': ('kam-pau-in', 'word-speak-ERG'),            # speaking
        'kamkat': ('kam-kat', 'word-cut'),                        # cut off words
        'kamkhat': ('kam-khat', 'word-one'),                      # one word
        'kamtam': ('kam-tam', 'word-many'),                       # many words
        'awmgak': ('awm-gak', 'be-?'),                            # be (variant)
        'nawlkhin': ('nawl-khin', 'law-?'),                       # legal
        'nawhpai': ('nawh-pai', 'push-go'),                       # push forward
        'napna': ('nap-na', 'thick-NMLZ'),                        # thickness
        'namtuam': ('nam-tuam', 'tribe-kind'),                    # various tribes
        # Round 125: Hyphenated suffix forms
        'liangkoah': ('liang-ko-ah', 'shoulder-both-LOC'),         # on both shoulders
        'napiun': ('napi-un', 'but-PL.IMP'),                       # but (imperative pl)
        'notea': ('no-te-a', 'young-PL-NOM'),                      # young ones
        'nomaua': ('no-mau-a', 'young-also-NOM'),                  # also young
        'nuaiate': ('nuai-a-te', 'below-NOM-PL'),                  # those below
        'piakna': ('piak-na', 'give.to-NMLZ'),                     # giving
        'piaknain': ('piak-na-in', 'give.to-NMLZ-INST'),           # in giving
        'mautea': ('mau-te-a', 'also-PL-NOM'),                     # also they
        'mipi': ('mi-pi', 'person-big'),                           # great person
        'zahtakte': ('zahtak-te', 'honor-PL'),                     # honors
        'vasate': ('va-sa-te', 'go.and-PAST-PL'),                  # went PL
        'sealt': ('seal-t', 'seal-?'),                             # seal
        'sealte': ('seal-te', 'seal-PL'),                          # seals
        'paaiah': ('pa-ai-ah', 'father-NOM-LOC'),                  # to/at father
        'naungekah': ('nau-ngek-ah', 'child-birth-LOC'),           # at midwife
        'tuangte': ('tuang-te', 'chariot-PL'),                     # chariots
        'dingte': ('ding-te', 'PROSP-PL'),                         # those who will (not lights)
        'sipah': ('si-pa-ah', 'be-NMLZ-LOC'),                      # being LOC
        'maimanah': ('mai-man-ah', 'face-true-LOC'),               # in face
        'thatte': ('that-te', 'kill-PL'),                          # killed PL
        'tuamtuamte': ('tuam-tuam-te', 'various-REDUP-PL'),        # various PL
        'tanaute': ('ta-nau-te', 'child-small-PL'),                # children
        'sisate': ('si-sa-te', 'unclean-PAST-PL'),                 # unclean PL
        'miliante': ('mi-lian-te', 'person-great-PL'),             # great men
        'khualnaun': ('khual-naun', 'guest-long.time'),            # sojourner
        'khualnaunin': ('khual-naun-in', 'guest-long.time-INST'),  # as sojourner
        'siamgante': ('siam-gan-te', 'weave-work-PL'),             # weavers
        'zawnahna': ('zawn-ah-na', 'north-LOC-?'),                 # to north
        'lungzina': ('lung-zin-a', 'heart-bright-NOM'),            # brightness
        'khanghamte': ('khang-ham-te', 'generation-old-PL'),       # old ones
        
        # Round 152: Hyphenated compound fixes
        'nini': ('ni-ni', 'day-REDUP'),                            # each day, daily
        'nini-in': ('ni-ni-in', 'day-REDUP-ERG'),                  # daily (adverbial)
        'niniin': ('ni-ni-in', 'day-REDUP-ERG'),                   # daily (adverbial) 
        'temkawi': ('tem-kawi', 'prune-hook'),                     # pruning hook
        'temkawi-in': ('tem-kawi-in', 'prune-hook-ERG'),           # into pruning hooks
        'temkawiin': ('tem-kawi-in', 'prune-hook-ERG'),            # into pruning hooks
        'temkawite': ('tem-kawi-te', 'prune-hook-PL'),             # pruning hooks
        'kiim': ('kiim', 'around'),                                # surroundings/around
        'kiim-ah': ('kiim-ah', 'around-LOC'),                      # in surroundings
        'kiimah': ('kiim-ah', 'around-LOC'),                       # in surroundings
        'kiima': ('kiim-a', 'around-NOM'),                         # surrounding ones
        'kiimate': ('kiim-a-te', 'around-NOM-PL'),                 # surrounding ones PL
        'kiimte': ('kiim-te', 'around-PL'),                        # surroundings PL
        'kiimte-ah': ('kiim-te-ah', 'around-PL-LOC'),              # in surroundings
        'lamlianpi': ('lam-lian-pi', 'road-big-INTENS'),           # highway
        'lamlianpi-ah': ('lam-lian-pi-ah', 'road-big-INTENS-LOC'), # on highway
        'lamlianpiah': ('lam-lian-pi-ah', 'road-big-INTENS-LOC'),  # on highway
        'thuthu': ('thu-thu', 'word-REDUP'),                       # secrets/deep things
        'thuthu-in': ('thu-thu-in', 'word-REDUP-ERG'),             # in secrets
        'thuthuin': ('thu-thu-in', 'word-REDUP-ERG'),              # in secrets
        'lohpipi': ('loh-pi-pi', 'not-big-INTENS'),                # great bitterness
        'lohpipi-in': ('loh-pi-pi-in', 'not-big-INTENS-ERG'),      # bitterly
        'lohnapi': ('loh-na-pi', 'not-NMLZ-big'),                  # great difficulty
        'lohnapi-ah': ('loh-na-pi-ah', 'not-NMLZ-big-LOC'),        # in difficulty
        'bui': ('bui', 'joint'),                                   # joint (shoulder joint)
        'bui-in': ('bui-in', 'joint-ERG'),                         # from joint
        'zekna': ('zek-na', 'allocate-NMLZ'),                      # allocation/portion
        'zekna-ah': ('zek-na-ah', 'allocate-NMLZ-LOC'),            # in allocation
        'lung-am': ('lung-am', 'heart-feel'),                     # feel/sense
        'nitak-an': ('ni-tak-an', 'day-true-time'),               # evening time
        'bawngnawi': ('bawng-nawi', 'cattle-bull'),               # bull/cattle type
        'bawngnawi-thaukhal': ('bawng-nawi-thau-khal', 'cattle-bull-fat-roast'), # type of offering
        'kiumcip': ('ki-um-cip', 'REFL-cover-tightly'),            # enclosed/shut up
        'ki-umcip': ('ki-um-cip', 'REFL-cover-tightly'),           # enclosed/shut up
        'kitha': ('ki-tha', 'REFL-spread'),                        # scattered/spread
        'ki-tha': ('ki-tha', 'REFL-spread'),                       # scattered/spread
        'kiitin': ('ki-it-in', 'REFL-love-ERG'),                   # harmonizing/uniting  
        'ki-itin': ('ki-it-in', 'REFL-love-ERG'),                  # harmonizing/uniting
        'kiukin': ('ki-uk-in', 'REFL-rule-ERG'),                   # being ruled
        'ki-ukin': ('ki-uk-in', 'REFL-rule-ERG'),                  # being ruled
        'kei-a': ('kei-a', '1SG.EMPH-GEN'),                        # my own (emphatic)
        'zalhmai': ('zalh-mai', 'settle-INTENS'),                  # settle down/flatten
        'zalhmai-in': ('zalh-mai-in', 'settle-INTENS-ERG'),        # settling (adv)
        'zalhmain': ('zalh-mai-in', 'settle-INTENS-ERG'),          # settling (adv)
        'kawmsa': ('kawm-sa', 'sigh-PAST'),                        # sighed/sighing
        'kawmsa-in': ('kawm-sa-in', 'sigh-PAST-ERG'),              # sighing (adv)
        'kawmsain': ('kawm-sa-in', 'sigh-PAST-ERG'),               # sighing (adv)
        'cilin': ('cil-in', 'thresh-ERG'),                         # threshing (adv)
        'ci-lin': ('cil-in', 'thresh-ERG'),                        # threshing (adv)
        'cilna': ('cil-na', 'thresh-NMLZ'),                        # threshing
        'bawngek': ('bawng-ek', 'cattle-dung'),                    # cow dung
        'bawng-ek': ('bawng-ek', 'cattle-dung'),                   # cow dung
        'anpia': ('an-pia', 'PL-give'),                            # they give
        'anpia-in': ('an-pia-in', 'PL-give-ERG'),                  # giving (them)
        'lungam': ('lung-am', 'heart-feel'),                       # feel/sense
        'lung-am': ('lung-am', 'heart-feel'),                      # feel/sense
        'tumakuak': ('tu-ma-kuak', 'this-also-half'),              # half-measure
        'tumakuakte': ('tu-ma-kuak-te', 'this-also-half-PL'),      # half-measures
        'tu-ma-kuakte': ('tu-ma-kuak-te', 'this-also-half-PL'),    # half-measures
        'nitak': ('ni-tak', 'sun-set'),                            # evening
        'nitakan': ('ni-tak-an', 'sun-set-time'),                  # evening time
        'nitak-an': ('ni-tak-an', 'sun-set-time'),                 # evening time
        
        # Round 153: Comprehensive hyphenated compound fixes
        # === ki- reflexive/reciprocal compounds ===
        'ki-enen': ('ki-en-en', 'REFL-look-REDUP'),                 # gaze at each other
        'kizia': ('ki-zia', 'REFL-crouch'),                        # crouch/lie flat
        'kizia-in': ('ki-zia-in', 'REFL-crouch-ERG'),              # crouching
        'kiciangto': ('ki-ciang-to', 'REFL-pile-CONT'),            # pile up/stand firm
        'kiciangto-in': ('ki-ciang-to-in', 'REFL-pile-CONT-ERG'),  # piling up
        'ki-atnente': ('ki-at-nen-te', 'REFL-burn-fire-PL'),       # burnt offerings
        'ki-atkeh': ('ki-at-keh', 'REFL-cut-self'),               # cut self (mourning)
        'ki-omsakkik': ('ki-om-sak-kik', 'REFL-be-CAUS-again'),    # restore/re-establish
        'ki-etkik': ('ki-et-kik', 'REFL-care-again'),              # inspect again
        'kilukhuhsa': ('ki-lu-khuh-sa', 'REFL-head-cover-PAST'),   # covered head
        'kilukhuhsa-in': ('ki-lu-khuh-sa-in', 'REFL-head-cover-PAST-ERG'), # covering head
        'ki-up': ('ki-up', 'REFL-expect'),                         # expect/hope
        'kipumpei': ('ki-pum-pei', 'REFL-body-shake'),             # tremble/shake
        'kipumpei-in': ('ki-pum-pei-in', 'REFL-body-shake-ERG'),   # trembling
        'kihoho': ('ki-ho-ho', 'REFL-counsel-REDUP'),              # counsel together
        'kihoho-in': ('ki-ho-ho-in', 'REFL-counsel-REDUP-ERG'),    # counseling together
        'kivakna': ('ki-vak-na', 'REFL-walk-NMLZ'),                # roaming/wandering
        'kivakna-in': ('ki-vak-na-in', 'REFL-walk-NMLZ-ERG'),      # in wandering
        'kilawnto': ('ki-lawn-to', 'REFL-rise-CONT'),              # rise and fall
        'kilawnto-in': ('ki-lawn-to-in', 'REFL-rise-CONT-ERG'),    # rising and falling
        'kilensa': ('ki-len-sa', 'REFL-lean-PAST'),                # leaned on
        'kilensa-in': ('ki-len-sa-in', 'REFL-lean-PAST-ERG'),      # leaning on
        'kibotkhia': ('ki-bot-khia', 'REFL-remove-exit'),          # depart/remove
        'kibotkhia-in': ('ki-bot-khia-in', 'REFL-remove-exit-ERG'), # departing
        'kibulhsa': ('ki-bulh-sa', 'REFL-arrange-PAST'),           # arranged/set up
        'kibulhsa-in': ('ki-bulh-sa-in', 'REFL-arrange-PAST-ERG'), # arranging
        'kinawhsa': ('ki-nawh-sa', 'REFL-push-PAST'),              # pushed out
        'kinawhsa-in': ('ki-nawh-sa-in', 'REFL-push-PAST-ERG'),    # pushing out
        'kipuahpha': ('ki-puah-pha', 'REFL-waste-away'),           # pine away/waste
        'kipuahpha-in': ('ki-puah-pha-in', 'REFL-waste-away-ERG'), # pining away
        'kikhualna': ('ki-khual-na', 'REFL-guest-NMLZ'),           # sojourning
        'kikhualna-in': ('ki-khual-na-in', 'REFL-guest-NMLZ-ERG'), # in sojourning
        'kiphuai': ('ki-phuai', 'REFL-devour'),                    # bite/devour each other
        'kiphuai-in': ('ki-phuai-in', 'REFL-devour-ERG'),          # devouring
        'kituhnate': ('ki-tuh-na-te', 'REFL-swear-NMLZ-PL'),       # oaths
        'kituhnate-ah': ('ki-tuh-na-te-ah', 'REFL-swear-NMLZ-PL-LOC'), # in oaths
        'kiginna': ('ki-gin-na', 'REFL-wanton-NMLZ'),              # wanton living
        'kiginna-in': ('ki-gin-na-in', 'REFL-wanton-NMLZ-ERG'),    # living wantonly
        'ki-ipipna': ('ki-ip-ip-na', 'REFL-strive-REDUP-NMLZ'),    # striving together
        'ki-ipipna-in': ('ki-ip-ip-na-in', 'REFL-strive-REDUP-NMLZ-ERG'),
        'kihazatnate': ('ki-hazat-na-te', 'REFL-revel-NMLZ-PL'),   # revelries
        'kihazatnate-in': ('ki-hazat-na-te-in', 'REFL-revel-NMLZ-PL-ERG'),
        'kihaza': ('ki-haza', 'REFL-revel'),                       # revel
        'kihaza-in': ('ki-haza-in', 'REFL-revel-ERG'),             # reveling
        'kimawlna': ('ki-mawl-na', 'REFL-subdue-NMLZ'),            # subjection
        'kimawlna-ah': ('ki-mawl-na-ah', 'REFL-subdue-NMLZ-LOC'),  # in subjection
        'ki-ettelna': ('ki-et-tel-na', 'REFL-test-match-NMLZ'),    # testing
        'ki-ettel': ('ki-et-tel', 'REFL-test-match'),              # test/examine
        'ki-ettehin': ('ki-et-teh-in', 'REFL-test-match-ERG'),     # testing
        'ki-upmawhnate': ('ki-up-mawh-na-te', 'REFL-hope-err-NMLZ-PL'), # offenses
        'ki-apin': ('ki-ap-in', 'REFL-cry-ERG'),                   # crying out
        'ki-uktawm': ('ki-uk-tawm', 'REFL-rule-end'),              # end of rule
        'ki-ipzote': ('ki-ip-zo-te', 'REFL-strive-able-PL'),       # those striving
        'ki-ipin': ('ki-ip-in', 'REFL-strive-ERG'),                # striving
        'kikaiawksak': ('ki-kai-awk-sak', 'REFL-gather-all-CAUS'), # cause to gather
        'kikai-awksak': ('ki-kai-awk-sak', 'REFL-gather-all-CAUS'),
        'kize-etsa': ('ki-ze-et-sa', 'REFL-tempt-care-PAST'),      # tempted
        'ki-eu': ('ki-eu', 'REFL-call'),                           # reflexive form
        'ki-ipcip': ('ki-ip-cip', 'REFL-strive-tightly'),          # strive earnestly
        'ki-uatsaknate': ('ki-uat-sak-na-te', 'REFL-bind-CAUS-NMLZ-PL'), # causings
        'ki-enpha': ('ki-en-pha', 'REFL-look-good'),               # look well/prosper
        'ki-umcihin': ('ki-um-cih-in', 'REFL-cover-tight-ERG'),    # enclosing
        'kitunsa': ('ki-tun-sa', 'REFL-arrive-PAST'),              # arrived
        'kitunsa-in': ('ki-tun-sa-in', 'REFL-arrive-PAST-ERG'),    # arriving
        'kikawi': ('ki-kawi', 'REFL-hook'),                        # hook together
        'kikawi-in': ('ki-kawi-in', 'REFL-hook-ERG'),              # hooking
        'ki-atte': ('ki-at-te', 'REFL-burn-PL'),                   # burnt ones
        'kinungat': ('ki-nung-at', 'REFL-follow-after'),           # follow after
        'kinung-at': ('ki-nung-at', 'REFL-follow-after'),
        'ki-itnate': ('ki-it-na-te', 'REFL-love-NMLZ-PL'),         # loves
        'kisu': ('ki-su', 'REFL-count'),                           # be counted
        'kisu-in': ('ki-su-in', 'REFL-count-ERG'),
        'kitheihsakna': ('ki-theih-sak-na', 'REFL-know-CAUS-NMLZ'), # making known
        'kitheihsakna-ah': ('ki-theih-sak-na-ah', 'REFL-know-CAUS-NMLZ-LOC'),
        'kitheihsakna-in': ('ki-theih-sak-na-in', 'REFL-know-CAUS-NMLZ-ERG'),
        'kiphukha': ('ki-phu-kha', 'REFL-wear-put'),               # wear/put on
        'kiphukha-in': ('ki-phu-kha-in', 'REFL-wear-put-ERG'),
        'kikokona': ('ki-koko-na', 'REFL-cry.out-NMLZ'),           # crying out
        'kikokona-in': ('ki-koko-na-in', 'REFL-cry.out-NMLZ-ERG'),
        'kikolawksak': ('ki-kol-awk-sak', 'REFL-cry-all-CAUS'),
        'kikol-awksak': ('ki-kol-awk-sak', 'REFL-cry-all-CAUS'),
        
        # === Verbal compounds ===
        'hangkeu': ('hang-keu', 'roast-fire'),                      # roasted
        'hangkeu-in': ('hang-keu-in', 'roast-fire-ERG'),            # roasting
        'sapipi': ('sa-pi-pi', 'INTENS-big-REDUP'),                # greatly
        'sapipi-in': ('sa-pi-pi-in', 'INTENS-big-REDUP-ERG'),      # very greatly
        'hehsapi': ('heh-sa-pi', 'anger-PAST-big'),                # greatly angered
        'hehsapi-in': ('heh-sa-pi-in', 'anger-PAST-big-ERG'),      # in great anger
        'thangzaw': ('thang-zaw', 'bless-more'),                   # bless more
        'thangzaw-in': ('thang-zaw-in', 'bless-more-ERG'),         # blessing more
        'ciangpha': ('ciang-pha', 'announce-good'),                # strengthen
        'ciangpha-in': ('ciang-pha-in', 'announce-good-ERG'),      # strengthening
        'tampipi': ('tam-pi-pi', 'many-big-REDUP'),                # very many
        'tampipi-in': ('tam-pi-pi-in', 'many-big-REDUP-ERG'),      # very many (adv)
        'phengphi': ('pheng-phi', 'testify-against'),              # testify against
        'phengphi-in': ('pheng-phi-in', 'testify-against-ERG'),    # testifying
        'zangawp': ('zan-gawp', 'night-break'),                    # broken (heart)
        'zan-gawp': ('zan-gawp', 'night-break'),
        'singkungno': ('sing-kung-no', 'tree-trunk-small'),        # young tree
        'singkungno-in': ('sing-kung-no-in', 'tree-trunk-small-ERG'),
        'otkhai': ('ot-khai', 'drive-away'),                       # drive away
        'otkhai-in': ('ot-khai-in', 'drive-away-ERG'),             # driving away
        'thapai': ('tha-pai', 'pierce-go'),                        # pierce through
        'thapai-in': ('tha-pai-in', 'pierce-go-ERG'),              # piercing
        'tuibeem': ('tui-beem', 'water-collect'),                  # cistern/pit
        'tuibeem-ah': ('tui-beem-ah', 'water-collect-LOC'),        # in cistern
        'dakkhia': ('dak-khia', 'look-exit'),                      # look out from
        'dakkhia-in': ('dak-khia-in', 'look-exit-ERG'),            # looking out
        'hilopi': ('hi-lo-pi', 'be-NEG-big'),                      # not at all
        'hilopi-in': ('hi-lo-pi-in', 'be-NEG-big-ERG'),            # not at all
        'mema': ('me-ma', 'grain-handful'),                        # handful
        'mema-in': ('me-ma-in', 'grain-handful-ERG'),              # by handful
        'phinna': ('phin-na', 'turn-NMLZ'),                        # turning
        'phinna-in': ('phin-na-in', 'turn-NMLZ-ERG'),              # in turning
        'selkhia': ('sel-khia', 'slice-exit'),                     # cut off
        'selkhia-in': ('sel-khia-in', 'slice-exit-ERG'),           # cutting off
        'kolhna': ('kolh-na', 'desolate-NMLZ'),                    # desolation
        'kolhna-ah': ('kolh-na-ah', 'desolate-NMLZ-LOC'),          # in desolation
        'gawigawi': ('gawi-gawi', 'gnash-REDUP'),                  # gnashing
        'gawigawi-in': ('gawi-gawi-in', 'gnash-REDUP-ERG'),        # gnashing (adv)
        'thenthen': ('then-then', 'multiply-REDUP'),               # greatly multiply
        'thenthen-in': ('then-then-in', 'multiply-REDUP-ERG'),     # multiplying greatly
        'vakzau': ('vak-zau', 'walk-far'),                         # walk abroad
        'vakzau-in': ('vak-zau-in', 'walk-far-ERG'),               # walking abroad
        'khamlua': ('kham-lua', 'forbid-exceed'),                  # forbid too much
        'khamlua-in': ('kham-lua-in', 'forbid-exceed-ERG'),        # forbidding
        'mawlnapi': ('mawl-na-pi', 'blunt-NMLZ-big'),              # very blunt
        'mawlnapi-in': ('mawl-na-pi-in', 'blunt-NMLZ-big-ERG'),    # being very blunt
        'zankhuavak': ('zan-khua-vak', 'night-town-walk'),         # night revelry
        'zankhuavak-in': ('zan-khua-vak-in', 'night-town-walk-ERG'),
        'ngaihnophuai': ('ngaih-nop-huai', 'think-want-full'),     # delightful
        'ngaihnop-huai': ('ngaih-nop-huai', 'think-want-full'),
        'suausuau': ('suau-suau', 'chirp-REDUP'),                  # chirping
        'suausuau-in': ('suau-suau-in', 'chirp-REDUP-ERG'),        # chirping (adv)
        'dawksa': ('dawk-sa', 'appear-PAST'),                      # appeared/came forth
        'dawksa-in': ('dawk-sa-in', 'appear-PAST-ERG'),            # appearing
        'ngato': ('nga-to', 'divine-CONT'),                        # divining/carrying
        'ngato-in': ('nga-to-in', 'divine-CONT-ERG'),              # divining
        'puahpha': ('puah-pha', 'divine-good'),                    # repair/restore
        'puahpha-in': ('puah-pha-in', 'divine-good-ERG'),          # restoring
        'hiamsa': ('hiam-sa', 'sharpen-PAST'),                     # sharpened
        'hiamsa-in': ('hiam-sa-in', 'sharpen-PAST-ERG'),           # sharpening
        'tangawlin': ('tang-awl-in', 'hold-firm-ERG'),             # holding
        'tang-awlin': ('tang-awl-in', 'hold-firm-ERG'),
        'mutkhia': ('mut-khia', 'see-exit'),                       # see come out
        'mutkhia-in': ('mut-khia-in', 'see-exit-ERG'),             # seeing
        'huaihammawhna': ('huai-ham-mawh-na', 'dread-old-err-NMLZ'), # fearful sin
        'huaiham-mawhna': ('huai-ham-mawh-na', 'dread-old-err-NMLZ'),
        'suangtui': ('suang-tui', 'stone-water'),                  # refine/smelt
        'suangtui-in': ('suang-tui-in', 'stone-water-ERG'),        # refining
        'pul': ('pul', 'divide'),                                  # divide
        'pul-in': ('pul-in', 'divide-ERG'),                        # dividing
        'teltakpi': ('tel-tak-pi', 'certain-true-INTENS'),         # very certainly
        'teltakpi-in': ('tel-tak-pi-in', 'certain-true-INTENS-ERG'),
        'letkhia': ('let-khia', 'return-exit'),                    # return out
        'letkhia-in': ('let-khia-in', 'return-exit-ERG'),          # returning
        'sukzaw': ('suk-zaw', 'cause-more'),                       # cause more
        'sukzaw-in': ('suk-zaw-in', 'cause-more-ERG'),             # causing more
        'zeza': ('ze-za', 'foot-sole'),                            # calf/sole of foot
        'zeza-in': ('ze-za-in', 'foot-sole-ERG'),                  # by foot
        'thuhna': ('tuh-na', 'seal-NMLZ'),                         # sealing
        'thuhna-in': ('tuh-na-in', 'seal-NMLZ-ERG'),               # in sealing
        'tasuahna': ('ta-suah-na', 'child-born-NMLZ'),             # birth/offspring
        'tasuahna-in': ('ta-suah-na-in', 'child-born-NMLZ-ERG'),
        'lipkhaphuai': ('lip-kha-phuai', 'ruin-place-heap'),       # heaps/ruins
        'lipkhaphuai-in': ('lip-kha-phuai-in', 'ruin-place-heap-ERG'),
        'luhzo': ('luh-zo', 'enter-able'),                         # able to enter
        'luhzo-in': ('luh-zo-in', 'enter-able-ERG'),               # entering
        'thalawhna': ('tha-lawh-na', 'flee-away-NMLZ'),            # fleeing
        'thalawhna-in': ('tha-lawh-na-in', 'flee-away-NMLZ-ERG'),  # in fleeing
        'gahta': ('gah-ta', 'pasture-NMLZ'),                       # pasturing
        'gahta-in': ('gah-ta-in', 'pasture-NMLZ-ERG'),             # pasturing
        'tuahsia': ('tuah-sia', 'meet-bad'),                       # displease
        'tuahsia-in': ('tuah-sia-in', 'meet-bad-ERG'),             # displeasing
        'tuucinna': ('tuucin-na', 'shepherd-NMLZ'),                # shepherding
        'tuucinna-in': ('tuucin-na-in', 'shepherd-NMLZ-ERG'),      # in shepherding
        'pozo': ('po-zo', 'spread-able'),                          # able to spread
        'pozo-in': ('po-zo-in', 'spread-able-ERG'),                # spreading
        'siapi': ('sia-pi', 'bad-big'),                            # very bad
        'siapi-in': ('sia-pi-in', 'bad-big-ERG'),                  # very badly
        'singpua': ('sing-pua', 'tree-fruit'),                     # tree fruit/vine
        'singpua-in': ('sing-pua-in', 'tree-fruit-ERG'),           # by vine
        'tuikia': ('tui-kia', 'water-cry'),                        # sound of waters
        'tuikia-in': ('tui-kia-in', 'water-cry-ERG'),              # with water sound
        'silhlopi': ('silh-lo-pi', 'clothe-NEG-INTENS'),           # utterly unclothed
        'silhlopi-in': ('silh-lo-pi-in', 'clothe-NEG-INTENS-ERG'),
        'nungaktangval': ('nungak-tangval', 'maiden-youth'),       # young men and women
        'nungak-tangval': ('nungak-tangval', 'maiden-youth'),
        'thuakma': ('thuak-ma', 'suffer-also'),                    # also suffer
        'thuakma-in': ('thuak-ma-in', 'suffer-also-ERG'),          # also suffering
        'mutheisa': ('mu-thei-sa', 'see-able-PAST'),               # could be seen
        'mutheisa-in': ('mu-thei-sa-in', 'see-able-PAST-ERG'),     # being seen
        'zuakma': ('zuak-ma', 'sell-also'),                        # also sell
        'zuakma-in': ('zuak-ma-in', 'sell-also-ERG'),              # also selling
        'keksa': ('kek-sa', 'foot-PAST'),                          # footed/stepped
        'keksa-in': ('kek-sa-in', 'foot-PAST-ERG'),                # stepping
        'mahmahpi': ('mah-mah-pi', 'EMPH-EMPH-INTENS'),            # very very much
        'mahmahpi-in': ('mah-mah-pi-in', 'EMPH-EMPH-INTENS-ERG'),
        'zeekte': ('zeek-te', 'crouch-PL'),                        # crouching ones
        'zeekte-in': ('zeek-te-in', 'crouch-PL-ERG'),
        'simthei': ('sim-thei', 'count-able'),                     # able to count
        'simthei-in': ('sim-thei-in', 'count-able-ERG'),           # counting
        'noptaksa': ('nop-tak-sa', 'want-true-PAST'),              # truly wanted
        'noptaksa-in': ('nop-tak-sa-in', 'want-true-PAST-ERG'),    # truly wanting
        'toknawi': ('tok-nawi', 'sit-still'),                      # sitting position
        'toknawi-in': ('tok-nawi-in', 'sit-still-ERG'),            # sitting
        'khengto': ('kheng-to', 'divide-CONT'),                    # dividing
        'khengto-in': ('kheng-to-in', 'divide-CONT-ERG'),          # dividing (adv)
        'puksakkha': ('puk-sak-kha', 'call-CAUS-out'),             # cause to call
        'puksakkha-in': ('puk-sak-kha-in', 'call-CAUS-out-ERG'),
        'peukhia': ('peu-khia', 'cover-exit'),                     # uncover
        'peukhia-in': ('peu-khia-in', 'cover-exit-ERG'),           # uncovering
        'uanglua': ('uang-lua', 'elder-exceed'),                   # too proud
        'uanglua-in': ('uang-lua-in', 'elder-exceed-ERG'),         # too proudly
        'khahsuahna': ('khah-suah-na', 'choke-out-NMLZ'),          # choking
        'khahsuahna-in': ('khah-suah-na-in', 'choke-out-NMLZ-ERG'),
        'vatkhia': ('vat-khia', 'go-exit'),                        # go out
        'vatkhia-in': ('vat-khia-in', 'go-exit-ERG'),              # going out
        'khatthu': ('khat-thu', 'one-word'),                       # one matter/thing
        'khatthu-in': ('khat-thu-in', 'one-word-ERG'),             # in one matter
        
        # === Noun compounds ===
        'luphak': ('lu-phak', 'head-bow'),                         # bow head
        'lu-phak': ('lu-phak', 'head-bow'),
        'khaphak': ('kha-phak', 'spirit-reach'),                   # spirit reach
        'kha-phak': ('kha-phak', 'spirit-reach'),
        'thukhak': ('thu-khak', 'word-block'),                     # decree/command
        'thu-khak': ('thu-khak', 'word-block'),
        'saiikte': ('sa-iik-te', 'flesh-type-PL'),                # flesh types
        'sa-iikte': ('sa-iik-te', 'flesh-type-PL'),
        'sabetna': ('sa-bet-na', 'flesh-cut-NMLZ'),                # flesh cutting
        'sabetna-ah': ('sa-bet-na-ah', 'flesh-cut-NMLZ-LOC'),
        'sawmahkhatte': ('sawm-ah-khat-te', 'ten-LOC-one-PL'),     # eleven
        'sawm-ah-khatte': ('sawm-ah-khat-te', 'ten-LOC-one-PL'),
        'saledite': ('saledi-te', 'gazelle-PL'),                   # gazelles
        'saledi-te': ('saledi-te', 'gazelle-PL'),
        'beeluk': ('beel-uk', 'bowl-cover'),                       # covered bowl
        'beel-uk': ('beel-uk', 'bowl-cover'),
        'lampangte': ('lam-pang-te', 'road-side-PL'),              # roadsides
        'lampangte-ah': ('lam-pang-te-ah', 'road-side-PL-LOC'),
        'sumkoihnate': ('sum-koih-na-te', 'money-place-NMLZ-PL'),  # treasuries
        'sumkoihnate-ah': ('sum-koih-na-te-ah', 'money-place-NMLZ-PL-LOC'),
        'vankoihnate': ('van-koih-na-te', 'sky-place-NMLZ-PL'),    # heavenly places
        'vankoihnate-ah': ('van-koih-na-te-ah', 'sky-place-NMLZ-PL-LOC'),
        'gambuppi': ('gam-bup-pi', 'land-all-INTENS'),             # whole land
        'gambuppi-ah': ('gam-bup-pi-ah', 'land-all-INTENS-LOC'),
        'vaktohna': ('vak-toh-na', 'walk-up-NMLZ'),                # ascending
        'vaktohna-ah': ('vak-toh-na-ah', 'walk-up-NMLZ-LOC'),
        'puansilhna': ('puan-silh-na', 'cloth-wear-NMLZ'),         # garment/clothing
        'puansilhna-ah': ('puan-silh-na-ah', 'cloth-wear-NMLZ-LOC'),
        'lamneute': ('lam-neu-te', 'road-small-PL'),               # small paths
        'lamneute-ah': ('lam-neu-te-ah', 'road-small-PL-LOC'),
        'lamkabomte': ('lam-ka-bom-te', 'road-mouth-junction-PL'), # crossroads
        'lamkabomte-ah': ('lam-ka-bom-te-ah', 'road-mouth-junction-PL-LOC'),
        'hanthotnate': ('han-thot-na-te', 'strength-grow-NMLZ-PL'), # strengthening
        'hanthotnate-ah': ('han-thot-na-te-ah', 'strength-grow-NMLZ-PL-LOC'),
        'suatna': ('suat-na', 'redeem-NMLZ'),                      # redemption
        'suatna-ah': ('suat-na-ah', 'redeem-NMLZ-LOC'),
        'belna': ('bel-na', 'lick-NMLZ'),                          # licking
        'belna-ah': ('bel-na-ah', 'lick-NMLZ-LOC'),
        'khopna': ('khop-na', 'labor-NMLZ'),                       # labor/toil
        'khopna-ah': ('khop-na-ah', 'labor-NMLZ-LOC'),
        'phaksakna': ('phak-sak-na', 'reach-CAUS-NMLZ'),           # causing to reach
        'phaksakna-ah': ('phak-sak-na-ah', 'reach-CAUS-NMLZ-LOC'),
        'zumhuaina': ('zum-huai-na', 'trust-full-NMLZ'),           # faithfulness
        'zumhuaina-teng': ('zum-huai-na-teng', 'trust-full-NMLZ-all'),
        'kulhpua': ('kulh-pua', 'wall-outside'),                   # outer wall
        'kulhpua-ah': ('kulh-pua-ah', 'wall-outside-LOC'),
        'tanungak': ('ta-nu-ngak', 'child-female-young'),          # maiden daughter
        'tanu-ngak': ('ta-nu-ngak', 'child-female-young'),
        'geite': ('gei-te', 'shore-PL'),                           # shores
        'geite-ah': ('gei-te-ah', 'shore-PL-LOC'),
        'pawpite': ('pawpi-te', 'church-PL'),                      # churches
        'pawpite-ah': ('pawpi-te-ah', 'church-PL-LOC'),
        'khuaate': ('khua-a-te', 'town-NOM-PL'),                   # town ones
        'khua-ate': ('khua-a-te', 'town-NOM-PL'),
        'khitate': ('khit-a-te', 'after-NOM-PL'),                  # later ones
        'khit-ate': ('khit-a-te', 'after-NOM-PL'),
        'innate': ('inn-a-te', 'house-NOM-PL'),                    # house ones
        'inn-ate': ('inn-a-te', 'house-NOM-PL'),
        'maiate': ('mai-a-te', 'face-NOM-PL'),                     # front ones
        'mai-ate': ('mai-a-te', 'face-NOM-PL'),
        'vaakonte': ('va-ak-no-te', 'go-NOM-young-PL'),            # young birds
        'va-aknote': ('va-ak-no-te', 'go-NOM-young-PL'),
        'bualte': ('bual-te', 'garden-PL'),                        # gardens
        'bualte-a': ('bual-te-a', 'garden-PL-NOM'),
        'diphumna': ('dip-hum-na', 'dip-place-NMLZ'),              # dipping place
        'dip-humna': ('dip-hum-na', 'dip-place-NMLZ'),
        'zonna': ('zo-na', 'finish-NMLZ'),                         # finishing
        'zo-na': ('zo-na', 'finish-NMLZ'),
        
        # === Other compounds ===
        'balnensa': ('bal-nen-sa', 'owe-bake-PAST'),              # owed (baked offering)
        'balnensa-in': ('bal-nen-sa-in', 'owe-bake-PAST-ERG'),
        'balkeksa': ('bal-kek-sa', 'owe-fry-PAST'),              # owed (fried offering)
        'balkeksa-in': ('bal-kek-sa-in', 'owe-fry-PAST-ERG'),
        'anpalanlum': ('an-pal-an-lum', 'PL-side-PL-soft'),        # they on soft side
        'anpal-anlum': ('an-pal-an-lum', 'PL-side-PL-soft'),
        'kaaito': ('ka-ai-to', '1SG-go-CONT'),                     # I keep going
        'kaaito-in': ('ka-ai-to-in', '1SG-go-CONT-ERG'),
        'kawkkhia': ('kawk-khia', 'call-exit'),                    # call out
        'kawkkhia-in': ('kawk-khia-in', 'call-exit-ERG'),
        'olin': ('ol-in', 'easy-ERG'),                             # easily
        'ol-in': ('ol-in', 'easy-ERG'),
        'tumasiah': ('tu-ma-siah', 'this-also-like'),              # like this also
        'tumasiah-a': ('tu-ma-siah-a', 'this-also-like-NOM'),
        'zeol': ('ze-ol', 'tempt-easy'),                           # easily tempted
        'ze-ol': ('ze-ol', 'tempt-easy'),
        'zeetnate': ('ze-et-na-te', 'tempt-care-NMLZ-PL'),         # temptations
        'ze-etnate': ('ze-et-na-te', 'tempt-care-NMLZ-PL'),
        'tangpiun': ('tang-pi-un', 'hold-big-IMP'),                # hold firmly
        'tangpi-un': ('tang-pi-un', 'hold-big-IMP'),
        'naunungzuite': ('nau-nung-zui-te', 'child-after-follow-PL'), # followers
        'nau-nungzuite': ('nau-nung-zui-te', 'child-after-follow-PL'),
        'khuzaw': ('khu-zaw', 'cold-more'),                        # colder
        'khuzaw-in': ('khu-zaw-in', 'cold-more-ERG'),
        'maietin': ('mai-et-in', 'face-care-ERG'),                 # looking at
        'mai-etin': ('mai-et-in', 'face-care-ERG'),
        'cimmai': ('cim-mai', 'pierce-face'),                      # pierce through
        'cimmai-in': ('cim-mai-in', 'pierce-face-ERG'),
        'zinna': ('zin-na', 'wife-NMLZ'),                          # marriage
        'zinna-in': ('zin-na-in', 'wife-NMLZ-ERG'),
        'khuakhua': ('khua-khua', 'town-REDUP'),                   # every town
        'khuakhua-in': ('khua-khua-in', 'town-REDUP-ERG'),
        'ngawngawhte': ('ngawng-awh-te', 'neck-bend-PL'),          # bent necks
        'ngawng-awhte': ('ngawng-awh-te', 'neck-bend-PL'),
        'huau': ('hu-au', 'grandparent-male'),                    # grandfather
        'huau-in': ('hu-au-in', 'grandparent-male-ERG'),
        'ciahpihto': ('ciah-pih-to', 'return-all-CONT'),           # returning
        'ciahpihto-in': ('ciah-pih-to-in', 'return-all-CONT-ERG'),
        'lialua': ('lia-lua', 'exceed-exceed'),                    # greatly exceed
        'lialua-in': ('lia-lua-in', 'exceed-exceed-ERG'),
        'sikkeukathum': ('sik-keu-ka-thum', 'turn-back-and-three'), # threefold turning
        'sikkeu-ka-thum': ('sik-keu-ka-thum', 'turn-back-and-three'),
        'lungmuanhuai': ('lung-muan-huai', 'heart-trust-full'),    # confidence
        'lungmuanhuai-in': ('lung-muan-huai-in', 'heart-trust-full-ERG'),
        'gegupi': ('ge-gu-pi', 'jaw-bone-big'),                    # large jaw
        'gegupi-in': ('ge-gu-pi-in', 'jaw-bone-big-ERG'),
        'khawngai': ('khawng-ai', 'pity-love'),                    # be merciful
        'khawngai-in': ('khawng-ai-in', 'pity-love-ERG'),
        'sawi': ('sa-wi', 'flesh-part'),                          # meat
        'sawi-in': ('sa-wi-in', 'flesh-part-ERG'),
        'bawlzaw': ('bawl-zaw', 'make-more'),                      # make more
        'bawlzaw-in': ('bawl-zaw-in', 'make-more-ERG'),
        'kongkalai': ('kong-ka-lai', 'mouth-1SG-midst'),           # in my speech
        'kongkalai-ah': ('kong-ka-lai-ah', 'mouth-1SG-midst-LOC'),
        'hetchiai': ('het-chiai', 'strong-very'),                  # strongly
        'hetchiai-in': ('het-chiai-in', 'strong-very-ERG'),
        'vatakum': ('va-tak-um', 'go-true-cover'),                 # truly go
        'vatak-um': ('va-tak-um', 'go-true-cover'),
        'nawkpai': ('nawk-pai', 'again-go'),                       # go again
        'nawkpai-in': ('nawk-pai-in', 'again-go-ERG'),
        'sikhiau': ('sik-hiau', 'turn-back'),                      # turn around
        'sik-hiau': ('sik-hiau', 'turn-back'),
        'siket': ('sik-et', 'turn-care'),                          # look around
        'sik-et': ('sik-et', 'turn-care'),
        'sikawmdal': ('sik-awm-dal', 'turn-be-still'),             # turn/repent
        'sik-awmdal': ('sik-awm-dal', 'turn-be-still'),
        'sikek': ('sik-ek', 'turn-?'),                             # turn
        'sik-ek': ('sik-ek', 'turn-?'),
        'vaite': ('vai-te', 'affairs-PL'),                         # affairs
        'vaite-ah': ('vai-te-ah', 'affairs-PL-LOC'),
        'muamuaana': ('mua-mua-a-na', 'see-REDUP-NOM-NMLZ'),       # viewing
        'muamua-na': ('mua-mua-na', 'see-REDUP-NMLZ'),
        'cilei': ('ci-lei', 'say-buy'),                            # say/buy
        'ci-lei': ('ci-lei', 'say-buy'),
        'savunum': ('sa-vun-um', 'flesh-skin-?'),                  # leather
        'savun-um': ('sa-vun-um', 'flesh-skin-?'),
        'holam': ('hol-am', 'south-?'),                            # southward
        'hol-am': ('hol-am', 'south-?'),
        'kineuet': ('ki-neu-et', 'REFL-small-care'),               # humble self
        'kineu-et': ('ki-neu-et', 'REFL-small-care'),
        'kimasialh': ('ki-ma-sialh', 'REFL-face-?'),               # ashamed
        'kima-sialh': ('ki-ma-sialh', 'REFL-face-?'),
        'lawtkhia': ('lawt-khia', 'jump-exit'),                    # jump out
        'lawtkhia-in': ('lawt-khia-in', 'jump-exit-ERG'),
        'tuka': ('tu-ka', 'now-1SG'),                              # now I
        'tu-ka': ('tu-ka', 'now-1SG'),
        'vasakalaohte': ('va-sa-kala-oh-te', 'bird-flesh-owl-type-PL'), # owls
        'vasa-kalaohte': ('va-sa-kala-oh-te', 'bird-flesh-owl-type-PL'),
        "vasa-kalaohte'": ("va-sa-kala-oh-te'", 'bird-flesh-owl-type-PL.POSS'),
        'pahtakhuai': ('pah-ta-khuai', 'father-child-?'),          # fatherhood
        'pahtakhuai-in': ('pah-ta-khuai-in', 'father-child-?-ERG'),
        'takhuai': ('ta-khuai', 'child-?'),                        # childhood
        'ta-khuai': ('ta-khuai', 'child-?'),
        'nalnah': ('nal-na-ah', '2SG-NMLZ-LOC'),                   # your place
        'nalna-ah': ('nal-na-ah', '2SG-NMLZ-LOC'),
        'huiah': ('hui-ah', 'wind-LOC'),                           # in wind
        'hui-ah': ('hui-ah', 'wind-LOC'),
        'noahtaak': ('noah-taak', 'NOAH-true'),                    # Noah truly
        'noah-taak': ('noah-taak', 'NOAH-true'),
        'mithah': ('mit-hah', 'eye-?'),                            # blind
        'mit-hah': ('mit-hah', 'eye-?'),
        'kawmpi': ('kawm-pi', 'sigh-big'),                         # sigh greatly
        'kawmpi-in': ('kawm-pi-in', 'sigh-big-ERG'),
        'nakpipi': ('nak-pi-pi', '2SG-big-REDUP'),                 # your greatness
        'nakpipi-in': ('nak-pi-pi-in', '2SG-big-REDUP-ERG'),
        'awngawng': ('awng-awng', 'open-REDUP'),                   # wide open
        'awng-awng': ('awng-awng', 'open-REDUP'),
        'tedildel': ('te-dil-del', 'PL-?-?'),                      # scattered
        'te-dildel': ('te-dil-del', 'PL-?-?'),
        'tusawnsawn': ('tu-sawn-sawn', 'now-time-REDUP'),          # now repeatedly
        'tu-sawnsawn': ('tu-sawn-sawn', 'now-time-REDUP'),
        'nuaiet': ('nuai-et', 'below-care'),                       # look down
        'nuai-et': ('nuai-et', 'below-care'),
        'lenpihto': ('len-pih-to', 'lean-all-CONT'),               # leaning
        'lenpihto-in': ('len-pih-to-in', 'lean-all-CONT-ERG'),
        'awzol': ('aw-zol', 'voice-weak'),                         # voice weak
        'aw-zol': ('aw-zol', 'voice-weak'),
        'hiloto': ('hi-lo-to', 'be-NEG-CONT'),                     # not being
        'hito-in': ('hi-to-in', 'be-CONT-ERG'),                    # being
        'zileta': ('zi-le-ta', 'wife-and-child'),                  # wife and child
        'zileta-in': ('zi-le-ta-in', 'wife-and-child-ERG'),
        'zinlinna': ('zin-lin-na', 'wife-dwell-NMLZ'),             # marriage
        'zinlinna-a': ('zin-lin-na-a', 'wife-dwell-NMLZ-NOM'),
        'innpua': ('inn-pua', 'house-outside'),                    # outside house
        'innpua-ah': ('inn-pua-ah', 'house-outside-LOC'),
        'cialna': ('cial-na', 'say-NMLZ'),                         # saying
        'cialna-in': ('cial-na-in', 'say-NMLZ-ERG'),
        'sunan': ('sun-an', 'day-time'),                           # daytime
        'sun-an': ('sun-an', 'day-time'),
        'dakto': ('dak-to', 'look-CONT'),                          # looking
        'dakto-in': ('dak-to-in', 'look-CONT-ERG'),
        'dein': ('de-in', 'say-ERG'),                              # saying
        'de-in': ('de-in', 'say-ERG'),
        'mutpai': ('mut-pai', 'see-go'),                           # go see
        'mutpai-in': ('mut-pai-in', 'see-go-ERG'),
        'mihaipi': ('mi-hai-pi', 'person-wise-big'),               # very wise person
        'mihaipi-in': ('mi-hai-pi-in', 'person-wise-big-ERG'),
        'lungamin': ('lung-am-in', 'heart-feel-ERG'),              # feeling
        'lung-amin': ('lung-am-in', 'heart-feel-ERG'),
        'tailahpi': ('tai-lah-pi', 'flee-?-big'),                  # flee greatly
        'tailahpi-in': ('tai-lah-pi-in', 'flee-?-big-ERG'),
        'gukha': ('gu-kha', 'leg-?'),                              # leg bone
        'gu-kha': ('gu-kha', 'leg-?'),
        'kahpihto': ('kah-pih-to', '1SG-accompany-CONT'),          # I accompanying
        'kahpihto-in': ('kah-pih-to-in', '1SG-accompany-CONT-ERG'),
        'eukhia': ('eu-khia', 'call-exit'),                        # call out
        'eukhia-in': ('eu-khia-in', 'call-exit-ERG'),
        'kaiiin': ('ka-ii-in', '1SG-?-ERG'),                       # I...
        'kaii-in': ('ka-ii-in', '1SG-?-ERG'),
        'atulmakin': ('a-tul-ma-kin', '3SG-?-also-?'),             # he also
        'atul-amakin': ('a-tul-ama-kin', '3SG-?-3PL-?'),
        'bilapphuai': ('bil-ap-phuai', 'ear-close-?'),             # deaf
        'bil-aphuai': ('bil-ap-phuai', 'ear-close-?'),
        'langet': ('lang-et', 'side-care'),                        # look at side
        'lang-et': ('lang-et', 'side-care'),
        'singat': ('sing-at', 'tree-burn'),                        # burn wood
        'sing-at': ('sing-at', 'tree-burn'),
        'genkikina': ('gen-ki-kin-a', 'say-REFL-again-NOM'),        # saying again
        'genkikin-ah': ('gen-ki-kin-ah', 'say-REFL-again-LOC'),
        'saamek': ('saam-ek', 'hair-fur'),                          # hair/fur
        'saam-ek': ('saam-ek', 'hair-fur'),
        # Final hyphenated fixes
        'mithah': ('mit-hah', 'eye-blind'),                         # blind
        'mit-hah': ('mit-hah', 'eye-blind'),
        'tedildel': ('te-dil-del', 'PL-shake-REDUP'),               # scattered
        'te-dildel': ('te-dil-del', 'PL-shake-REDUP'),
        'savunum': ('sa-vun-um', 'flesh-skin-cover'),               # leather
        'savun-um': ('sa-vun-um', 'flesh-skin-cover'),
        'sikek': ('sik-ek', 'turn-dung'),                           # turn (variant)
        'sik-ek': ('sik-ek', 'turn-dung'),
        'holam': ('hol-am', 'south-ward'),                          # southward
        'hol-am': ('hol-am', 'south-ward'),
        'kimasialh': ('ki-ma-sialh', 'REFL-face-shame'),            # ashamed
        'kima-sialh': ('ki-ma-sialh', 'REFL-face-shame'),
        'kituahnate': ('ki-tuah-na-te', 'REFL-meet-NMLZ-PL'),       # meetings/oaths
        'kituahnate-ah': ('ki-tuah-na-te-ah', 'REFL-meet-NMLZ-PL-LOC'),
        'pahtakhuai': ('pah-ta-khuai', 'father-child-love'),        # fatherly love
        'pahtakhuai-in': ('pah-ta-khuai-in', 'father-child-love-ERG'),
        'takhuai': ('ta-khuai', 'child-love'),                      # love for child
        'ta-khuai': ('ta-khuai', 'child-love'),
        'kisiamaimang': ('ki-sia-mai-mang', 'REFL-bad-face-vanish'), # ashamed
        'kisia-maimang': ('ki-sia-mai-mang', 'REFL-bad-face-vanish'),
        'khanlai': ('khan-lai', 'time-midst'),                      # meanwhile
        'khanlai-in': ('khan-lai-in', 'time-midst-ERG'),
        'tailahpi': ('tai-lah-pi', 'flee-far-INTENS'),              # flee greatly
        'tailahpi-in': ('tai-lah-pi-in', 'flee-far-INTENS-ERG'),
        'gukha': ('gu-kha', 'leg-bone'),                            # leg bone
        'gu-kha': ('gu-kha', 'leg-bone'),
        'bilaphuai': ('bil-ap-huai', 'ear-close-full'),             # deaf
        'bil-aphuai': ('bil-ap-huai', 'ear-close-full'),
        'kaiiin': ('ka-ii-in', '1SG-go-ERG'),                       # I going
        'kaii-in': ('ka-ii-in', '1SG-go-ERG'),
        'atulamakin': ('a-tul-ama-kin', '3SG-follow-3PL-also'),     # he also follows them
        'atul-amakin': ('a-tul-ama-kin', '3SG-follow-3PL-also'),
        'sekhei': ('sek-hei', 'rest-place'),                        # resting place
        'sek-hei': ('sek-hei', 'rest-place'),
    }
    
    # Check compound words (try both hyphenated and unhyphenated)
    if word_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_lower]
    if word_no_hyphen_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_no_hyphen_lower]
    
    # Handle explicit hyphen before grammatical suffixes (e.g., lauhuai-in, muanhuai-ah)
    # These are written with explicit hyphen before -in (ERG), -ah (LOC), -a (LOC)
    HYPHEN_SUFFIXES = {
        "-a'": 'GEN',      # possessive/genitive with curly quote
        "-a\u2019": 'GEN', # possessive/genitive with curly quote (unicode)
        '-in': 'ERG',
        '-ah': 'LOC', 
        '-un': 'IMP',      # imperative plural
        '-a': 'LOC',
    }
    for hyph_suffix, suffix_gloss in sorted(HYPHEN_SUFFIXES.items(), key=lambda x: -len(x[0])):
        if word_lower.endswith(hyph_suffix) or word.endswith(hyph_suffix):
            stem = word[:-len(hyph_suffix)]
            stem_result = analyze_word(stem)
            if stem_result and stem_result[1] and '?' not in stem_result[1]:
                # Stem fully analyzed, combine with suffix
                return (f"{stem_result[0]}{hyph_suffix}", f"{stem_result[1]}-{suffix_gloss}")
    
    # Check noun stems (try both forms)
    if word in NOUN_STEMS:
        return (word, NOUN_STEMS[word])
    if word_no_hyphen in NOUN_STEMS:
        return (word, NOUN_STEMS[word_no_hyphen])
    if word_no_hyphen_lower in NOUN_STEMS:
        return (word, NOUN_STEMS[word_no_hyphen_lower])
    
    # Check verb stems (try both forms)
    if word in VERB_STEMS:
        return (word, VERB_STEMS[word])
    if word_no_hyphen in VERB_STEMS:
        return (word, VERB_STEMS[word_no_hyphen])
    if word_no_hyphen_lower in VERB_STEMS:
        return (word, VERB_STEMS[word_no_hyphen_lower])
    
    # Check for Form II verb stems (Henderson 1965: subjunctive forms)
    # Form II is used in inconclusive sentences and adjunctive phrases
    if word_no_hyphen_lower in VERB_STEM_PAIRS:
        form_i, base_gloss = VERB_STEM_PAIRS[word_no_hyphen_lower]
        return (word, base_gloss)  # Return base gloss (form is grammatical, not lexical)
    
    # For morphological decomposition, use the unhyphenated form
    segments = []
    glosses = []
    remaining = word_no_hyphen
    
    # 1. Check for pronominal prefix
    for prefix, gloss in sorted(OBJECT_PREFIXES.items(), key=lambda x: -len(x[0])):
        if remaining.lower().startswith(prefix):
            segments.append(prefix)
            glosses.append(gloss)
            remaining = remaining[len(prefix):]
            break
    else:
        for prefix, gloss in sorted(PRONOMINAL_PREFIXES.items(), key=lambda x: -len(x[0])):
            if remaining.lower().startswith(prefix) and len(remaining) > len(prefix):
                segments.append(prefix)
                glosses.append(gloss)
                remaining = remaining[len(prefix):]
                break
    
    # 1b. Check for reflexive/reciprocal ki- prefix
    if remaining.lower().startswith('ki') and len(remaining) > 2:
        ki_base = remaining[2:]
        # Check if base is a known verb stem
        ki_base_lower = ki_base.lower()
        # First try full compound forms
        full_ki_word = remaining.lower()
        if full_ki_word in VERB_STEMS:
            segments.append(remaining)
            glosses.append(VERB_STEMS[full_ki_word])
            remaining = ''
        elif ki_base_lower in VERB_STEMS:
            segments.append('ki')
            glosses.append('REFL')
            segments.append(ki_base)
            glosses.append(VERB_STEMS[ki_base_lower])
            remaining = ''
        elif ki_base_lower in NOUN_STEMS:
            segments.append('ki')
            glosses.append('REFL')
            segments.append(ki_base)
            glosses.append(NOUN_STEMS[ki_base_lower])
            remaining = ''
        else:
            # Try suffix stripping on ki- base
            for suffix in ['sak', 'pih', 'khiat', 'khia', 'tak', 'kik', 'zo', 'ta']:
                if ki_base_lower.endswith(suffix) and len(ki_base_lower) > len(suffix):
                    base_before_suffix = ki_base_lower[:-len(suffix)]
                    if base_before_suffix in VERB_STEMS:
                        segments.append('ki')
                        glosses.append('REFL')
                        segments.append(base_before_suffix)
                        glosses.append(VERB_STEMS[base_before_suffix])
                        suffix_glosses_map = {
                            'sak': 'CAUS', 'pih': 'APPL', 'khiat': 'AWAY',
                            'khia': 'AWAY', 'tak': 'firmly', 'kik': 'ITER',
                            'zo': 'COMPL', 'ta': 'PFV'
                        }
                        segments.append(suffix)
                        glosses.append(suffix_glosses_map.get(suffix, suffix))
                        remaining = ''
                        break
    
    # 2. Check for verb/noun stem (Round 154: prefer longest match across both dicts)
    stem_found = False
    remaining_lower = remaining.lower()
    
    # Find best verb stem match
    best_verb = None
    for stem, gloss in sorted(VERB_STEMS.items(), key=lambda x: -len(x[0])):
        if remaining_lower.startswith(stem):
            best_verb = (stem, gloss)
            break
    
    # Find best noun stem match  
    best_noun = None
    for stem, gloss in sorted(NOUN_STEMS.items(), key=lambda x: -len(x[0])):
        if remaining_lower.startswith(stem):
            best_noun = (stem, gloss)
            break
    
    # Choose the longer match (prefer noun if tie, as verbs tend to be shorter)
    if best_verb and best_noun:
        if len(best_noun[0]) >= len(best_verb[0]):
            stem, gloss = best_noun
        else:
            stem, gloss = best_verb
    elif best_verb:
        stem, gloss = best_verb
    elif best_noun:
        stem, gloss = best_noun
    else:
        stem, gloss = None, None
    
    if stem:
        segments.append(stem)
        glosses.append(gloss)
        remaining = remaining[len(stem):]
        stem_found = True
    
    # 3. Check for suffixes on remaining
    if remaining:
        # === Round 154: Enhanced suffix chain parsing ===
        # Process suffix chain iteratively (e.g., -kik-in, -na-teng, etc.)
        suffix_processed = True
        while remaining and suffix_processed:
            suffix_processed = False
            remaining_lower = remaining.lower()
            
            # Check TAM suffixes (longest first)
            for suffix, gloss in sorted(TAM_SUFFIXES.items(), key=lambda x: -len(x[0])):
                if remaining_lower == suffix:
                    segments.append(suffix)
                    glosses.append(gloss)
                    remaining = ''
                    suffix_processed = True
                    break
                elif remaining_lower.endswith(suffix) and len(remaining) > len(suffix):
                    # Strip suffix from end and check if what remains is valid
                    base = remaining[:-len(suffix)]
                    base_lower = base.lower()
                    # Check if base is a known stem or TAM suffix
                    if base_lower in VERB_STEMS or base_lower in NOUN_STEMS or base_lower in TAM_SUFFIXES:
                        segments.append(base)
                        if base_lower in VERB_STEMS:
                            glosses.append(VERB_STEMS[base_lower])
                        elif base_lower in NOUN_STEMS:
                            glosses.append(NOUN_STEMS[base_lower])
                        else:
                            glosses.append(TAM_SUFFIXES[base_lower])
                        segments.append(suffix)
                        glosses.append(gloss)
                        remaining = ''
                        suffix_processed = True
                        break
            
            if not suffix_processed and remaining:
                # Check case markers
                for case, gloss in sorted(CASE_MARKERS.items(), key=lambda x: -len(x[0])):
                    if remaining_lower == case:
                        segments.append(case)
                        glosses.append(gloss)
                        remaining = ''
                        suffix_processed = True
                        break
                    elif remaining_lower.endswith(case) and len(remaining) > len(case):
                        base = remaining[:-len(case)]
                        base_lower = base.lower()
                        # Check if base is valid TAM suffix or stem
                        if base_lower in TAM_SUFFIXES:
                            segments.append(base)
                            glosses.append(TAM_SUFFIXES[base_lower])
                            segments.append(case)
                            glosses.append(gloss)
                            remaining = ''
                            suffix_processed = True
                            break
        
        # Check final particles (only exact match)
        if remaining:
            for particle, gloss in FINAL_PARTICLES.items():
                if remaining.lower() == particle:
                    segments.append(particle)
                    glosses.append(gloss)
                    remaining = ''
                    break
        
        # Check nominalizers
        if remaining:
            for nom, gloss in NOMINALIZERS.items():
                # Case 1: remaining IS exactly the nominalizer (after stem extraction)
                if remaining.lower() == nom:
                    segments.append(nom)
                    glosses.append(gloss)
                    remaining = ''
                    break
                # Case 2: remaining has a base + nominalizer
                if remaining.lower().endswith(nom) and len(remaining) > len(nom):
                    base = remaining[:-len(nom)]
                    base_lower = base.lower()
                    # Check if base is a known stem
                    if base_lower in VERB_STEMS:
                        segments.append(base)
                        glosses.append(VERB_STEMS[base_lower])
                    elif base_lower in NOUN_STEMS:
                        segments.append(base)
                        glosses.append(NOUN_STEMS[base_lower])
                    elif base_lower in TAM_SUFFIXES:
                        segments.append(base)
                        glosses.append(TAM_SUFFIXES[base_lower])
                    else:
                        segments.append(base)
                        glosses.append('?')  # Unknown base
                    segments.append(nom)
                    glosses.append(gloss)
                    remaining = ''
                    break
    
    # Special handling: if no decomposition, try suffix stripping
    if remaining and not segments:
        # First, try reduplication patterns (X-X)
        half_len = len(remaining) // 2
        if len(remaining) >= 4 and len(remaining) % 2 == 0:
            first_half = remaining[:half_len].lower()
            second_half = remaining[half_len:].lower()
            if first_half == second_half:
                # Check if base is a known stem
                if first_half in VERB_STEMS:
                    return (f"{first_half}~{first_half}", f"{VERB_STEMS[first_half]}~RED")
                elif first_half in NOUN_STEMS:
                    return (f"{first_half}~{first_half}", f"{NOUN_STEMS[first_half]}~RED")
                else:
                    # Try lexicon lookup for base
                    lex_gloss = lookup_lexicon(first_half)
                    if lex_gloss:
                        return (f"{first_half}~{first_half}", f"{lex_gloss}~RED")
                    else:
                        return (f"{first_half}~{first_half}", f"?~RED")
        
        # === ENHANCED SUFFIX CHAIN PARSING (Round 154) ===
        # Extended suffix list with verbal aspect/ability markers
        suffix_glosses = {
            # Verbal ability/potential suffixes
            'thei': 'ABIL',     # ability/potential (can/able to)
            'theih': 'ABIL',    # variant form
            'zo': 'able',       # abilitative (capable of)
            # Aspect/directional suffixes
            'gawp': 'INTENS',   # intensive (forcefully/thoroughly)
            'khin': 'INTENS',   # intensive variant
            'kik': 'ITER',      # iterative (again)
            'pih': 'APPL',      # applicative (with/for)
            'khawm': 'COM',     # comitative (together)
            'khia': 'EXIT',     # directional (out)
            'lut': 'ENTER',     # directional (into)
            'toh': 'up',        # directional (up)
            'to': 'CONT',       # continuative
            # Other verbal suffixes
            'sak': 'CAUS',      # causative
            'sa': 'PERF',       # perfective
            'ta': 'PERF',       # perfective variant (completed action)
            'mang': 'COMPL',    # completive
            'khol': 'INTENS',   # intensifier
            'san': 'at',        # locative
            'pen': 'TOP',       # topic/superlative
            # Nominal suffixes
            'na': 'NMLZ',       # nominalizer
            'te': 'PL',         # plural
            'uh': 'PL',         # plural variant
            'in': 'ERG',        # ergative
            'ah': 'LOC',        # locative
        }
        
        # Try suffix stripping with RECURSIVE analysis of base
        for suffix, suf_gloss in sorted(suffix_glosses.items(), key=lambda x: -len(x[0])):
            if remaining.lower().endswith(suffix) and len(remaining) > len(suffix) + 1:
                base = remaining[:-len(suffix)]
                base_lower = base.lower()
                
                # First check direct stem lookups (fast path)
                if base_lower in VERB_STEMS:
                    return (f"{base}-{suffix}", f"{VERB_STEMS[base_lower]}-{suf_gloss}")
                elif base_lower in NOUN_STEMS:
                    return (f"{base}-{suffix}", f"{NOUN_STEMS[base_lower]}-{suf_gloss}")
                
                # Try lexicon lookup for base
                lex_gloss = lookup_lexicon(base_lower)
                if lex_gloss:
                    return (f"{base}-{suffix}", f"{lex_gloss}-{suf_gloss}")
                
                # RECURSIVE: Try analyzing the base as a complex form
                # This handles chains like verb-CAUS-ITER, ki-verb-ABIL, etc.
                base_seg, base_gloss = analyze_word(base)
                if '?' not in base_gloss:
                    # Base is fully analyzable - combine with suffix
                    return (f"{base_seg}-{suffix}", f"{base_gloss}-{suf_gloss}")
        
        # === KI- REFLEXIVE PREFIX HANDLING (Round 154) ===
        # Handle ki- prefix with recursive analysis of remainder
        remaining_lower = remaining.lower()
        if remaining_lower.startswith('ki') and len(remaining_lower) > 3:
            ki_base = remaining[2:]
            ki_base_lower = ki_base.lower()
            
            # Check direct stem lookups first
            if ki_base_lower in VERB_STEMS:
                return (f"ki-{ki_base}", f"REFL-{VERB_STEMS[ki_base_lower]}")
            
            # Try recursive analysis of the base
            base_seg, base_gloss = analyze_word(ki_base)
            if '?' not in base_gloss:
                return (f"ki-{base_seg}", f"REFL-{base_gloss}")
    
    # If we still have remaining, add it as unknown
    if remaining:
        if segments:
            segments.append(remaining)
            glosses.append('?')
        else:
            # No decomposition found - try lexicon lookup
            lexicon_gloss = lookup_lexicon(word.lower())
            if lexicon_gloss:
                return (word, lexicon_gloss)
            segments = [word]
            glosses = ['?']
    
    # Build output
    if len(segments) > 1:
        segmented = '-'.join(segments)
        gloss = '-'.join(glosses)
    else:
        segmented = segments[0] if segments else word
        gloss = glosses[0] if glosses else '?'
    
    return (segmented, gloss)


# Lexicon cache
_lexicon_cache = None

def load_lexicon():
    """Load the Tedim lexicon."""
    global _lexicon_cache
    if _lexicon_cache is not None:
        return _lexicon_cache
    
    lexicon_file = Path(__file__).parent.parent / 'data' / 'lexicons' / 'ctd_lexicon.tsv'
    _lexicon_cache = {}
    
    if lexicon_file.exists():
        with open(lexicon_file) as f:
            next(f)  # skip header
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 3:
                    kc_word = parts[0].lower()
                    eng_gloss = parts[2]
                    # Only take the first (best) gloss for each word
                    if kc_word not in _lexicon_cache:
                        _lexicon_cache[kc_word] = eng_gloss
    
    return _lexicon_cache

def lookup_lexicon(word: str) -> Optional[str]:
    """Look up a word in the lexicon."""
    lexicon = load_lexicon()
    return lexicon.get(word.lower())


def gloss_sentence(sentence: str) -> List[Tuple[str, str, str]]:
    """
    Gloss a full sentence.
    
    Returns:
        List of (original, segmented, gloss) tuples
    """
    words = sentence.split()
    results = []
    
    for word in words:
        segmented, gloss = analyze_word(word)
        results.append((word, segmented, gloss))
    
    return results


def format_interlinear(results: List[Tuple[str, str, str]], 
                       show_segmentation: bool = True) -> str:
    """Format results as interlinear text."""
    lines = []
    
    # Line 1: Original
    originals = [r[0] for r in results]
    
    # Line 2: Segmented (optional)
    segmented = [r[1] for r in results]
    
    # Line 3: Gloss
    glosses = [r[2] for r in results]
    
    # Calculate widths
    if show_segmentation:
        widths = [max(len(o), len(s), len(g)) + 2 
                  for o, s, g in zip(originals, segmented, glosses)]
    else:
        widths = [max(len(o), len(g)) + 2 for o, g in zip(originals, glosses)]
    
    # Build lines
    line1 = ''.join(o.ljust(w) for o, w in zip(originals, widths))
    if show_segmentation:
        line2 = ''.join(s.ljust(w) for s, w in zip(segmented, widths))
        line3 = ''.join(g.ljust(w) for g, w in zip(glosses, widths))
        return f"{line1}\n{line2}\n{line3}"
    else:
        line2 = ''.join(g.ljust(w) for g, w in zip(glosses, widths))
        return f"{line1}\n{line2}"


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_morphemes.py <word>")
        print("       python analyze_morphemes.py --sentence 'Tedim sentence here'")
        sys.exit(1)
    
    if sys.argv[1] == '--sentence':
        sentence = ' '.join(sys.argv[2:])
        results = gloss_sentence(sentence)
        print(format_interlinear(results, show_segmentation=True))
        
    elif sys.argv[1] == '--verse':
        # Load verse from corpus
        verse_id = sys.argv[2]
        verses_file = Path(__file__).parent.parent / 'data' / 'verses_aligned.tsv'
        
        with open(verses_file) as f:
            header = f.readline().strip().split('\t')
            ctd_col = None
            for i, col in enumerate(header):
                if col.startswith('ctd'):
                    ctd_col = i
                    break
            
            if ctd_col is None:
                print("Error: Tedim column not found")
                sys.exit(1)
            
            for line in f:
                parts = line.strip().split('\t')
                if parts[0] == verse_id:
                    if ctd_col < len(parts) and parts[ctd_col]:
                        print(f"Verse: {verse_id}")
                        print(f"Reference: {parts[1]}")
                        print()
                        results = gloss_sentence(parts[ctd_col])
                        print(format_interlinear(results, show_segmentation=True))
                    else:
                        print(f"No Tedim text for verse {verse_id}")
                    break
            else:
                print(f"Verse {verse_id} not found")
    
    else:
        # Single word
        word = sys.argv[1]
        segmented, gloss = analyze_word(word)
        print(f"Word:      {word}")
        print(f"Segmented: {segmented}")
        print(f"Gloss:     {gloss}")


if __name__ == '__main__':
    main()
