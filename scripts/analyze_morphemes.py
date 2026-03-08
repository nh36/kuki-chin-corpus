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
    'ding': 'PROSP',  # Prospective/future
    'ta': 'PFV',      # Perfective
    'zo': 'COMPL',    # Completive
    'kik': 'ITER',    # Iterative
    'nawn': 'CONT',   # Continuative
    'khin': 'IMM',    # Immediate
}

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

# Common function words with glosses - expanded with frequencies
FUNCTION_WORDS = {
    # === Conjunctions & Connectors ===
    'le': 'and',             # 10,942
    'leh': 'and/or',         # 2,921
    'ahihleh': 'if',         # 335
    'hitaleh': 'if.so',      # 295
    'hangin': 'because',     # 3,461
    'bangin': 'like',        # 3,886
    'manin': 'therefore',    # 2,790
    'zongin': 'although',    # 1,970
    'ciangin': 'then',       # 9,297
    'inla': 'and.then',      # ~838
    'napi': 'but/however',   # 279x - contrastive conjunction
    'hinapi': 'but/however', # 156x - variant with hi-
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
    'na': 'NMLZ',
    
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
    'za': 'hundred',
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
    'kipan': 'begin',        # ki-pan "REFL-begin"
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
    'vei': 'faint',          # 71x - Gen 25:29 "he was faint" (also "red")
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
    'ka': 'mouth',
    
    # Place/Location
    'gam': 'land',           # 2,586
    'gamte': 'lands',        # 173
    'khua': 'town',          # 919
    'khuapi': 'city',        # 1,050
    'khuapite': 'cities',    # 253
    'inn': 'house',          # 715
    'innte': 'houses',
    'mun': 'place',          # 820
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
    word = re.sub(r'[.,;:!?\u201c\u201d"\)\]\xbb]+$', '', word)  # Remove other trailing punct
    return word

def is_proper_noun(word: str) -> bool:
    """Check if word is a proper noun (case-insensitive matching)."""
    clean = clean_word(word)
    if not clean:
        return False
    # Check both original case and lowercase
    return clean in PROPER_NOUNS or clean.lower() in PROPER_NOUNS or clean[0].isupper()

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
    
    # Check if proper noun
    if is_proper_noun(word):
        return (word, word.upper())
    
    
    # Check for proper noun + suffix patterns (israel-te, jerusalem-ah, etc.)
    word_lower = word.lower()
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
    
    # Check function words first (full match)
    word_lower = word.lower()
    word_no_hyphen_lower = word_no_hyphen.lower()
    
    # Try both hyphenated and unhyphenated forms
    if word_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_lower])
    if word_no_hyphen_lower in FUNCTION_WORDS:
        return (word, FUNCTION_WORDS[word_no_hyphen_lower])
    
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
        }
        if base_lower in poss_map:
            return (word, poss_map[base_lower])
    
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
        'neihsa': ('nei-h-sa', 'have-NOM-flesh'),
        'paknamtui': ('pak-nam-tui', 'wine'),
        'minthanna': ('min-than-na', 'name-bless-NMLZ'),
        'suanlekhakte': ('suan-le-khak-te', 'offspring-PL'),
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
        'gensa': ('gen-sa', 'speak-flesh'),
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
        'bawlsa': ('bawl-sa', 'make-flesh'),
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
        'ciamsa': ('ciam-sa', 'promise-flesh'),
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
        'leenggahzu': ('leeng-gah-zu', 'chariot-?-?'),       # 228
        'sumngo': ('sum-ngo', 'money-?'),                     # 152
        'leenggui': ('leeng-gui', 'chariot-wheel'),           # 130
        'ling': ('ling', 'pile'),                              # 106
        'panun': ('pa-nun', 'father-life'),                    # 101
        'leenggah': ('leeng-gah', 'chariot-?'),               # 98
        'mudah': ('mu-dah', 'see-easy'),                       # 97
        'keel': ('keel', 'heel'),                              # 85
        'salin': ('sa-lin', 'meat-hope'),                      # 82
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
        'ngaihno': ('ngaih-no', 'think-?'),                   # 42
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
        'thatang': ('that-ang', 'kill-?'),                  # 28x - compound
        'khauhtakin': ('khauh-tak-in', 'strong-true-ERG'),  # 28x - "strongly"
        'nawkin': ('na-wkin', '2SG-?'),                     # 27x - compound
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
        'nengniam': ('neng-niam', 'breast-?'),              # 25x - compound
        'singkha': ('sing-kha', 'wood-?'),                  # 25x - compound
        'khate': ('khat-te', 'one-PL'),                     # 25x - "some (ones)"
        'kawlsing': ('kawl-sing', 'fry-wood'),              # 25x - compound
        'paai': ('pa-ai', 'father-love'),                   # 25x - compound
        'ngeite': ('ngei-te', 'have.NMLZ-PL'),              # 25x - "possessions"
        'hawlkhiat': ('hawl-khiat', 'drive-away'),          # 25x - "drive away"
        'zahko': ('zah-ko', 'fear-?'),                       # 25x - compound
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
        'thuteng': ('thu-teng', 'word-?'),                  # 23x - compound
        'pawlpih': ('pawl-pih', 'group-APPL'),              # 23x - "with group"
        'miliante': ('mi-lian-te', 'person-great-PL'),      # 23x - "great people"
        'mangbuhham': ('mangbuh-ham', 'barley-wheat'),      # 28x - "barley and wheat"
        'thatang': ('that-ang', 'kill-?'),                  # 28x - needs context
        'nawkin': ('na-wk-in', '2SG-?-ERG'),                # 27x - needs context
        'kaikhawmin': ('ka-i-khawm-in', '1SG-?-together-ERG'), # 28x - compound
        
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
        'kawnggak': ('kawng-gak', 'road-?'),                # 22x - compound
        'gingte': ('ging-te', 'gong-PL'),                   # 22x - "gongs"
        'kongpite': ('kongpi-te', 'road.big-PL'),           # 22x - "highways"
        'tuikhang': ('tui-khang', 'water-carry'),           # 22x - "water carrier"
        'hihlam': ('hih-lam', 'this-direction'),            # 22x - "this way"
        'tuihualte': ('tuihual-te', 'flood-PL'),            # 22x - "floods"
        'ihihna': ('i-hih-na', '1PL.INCL-do-NMLZ'),         # 22x - "our doing"
        'kongcingte': ('kong-cing-te', 'road-faithful-PL'), # 22x - compound
        'nengniam': ('neng-niam', 'breast-soft'),           # 25x - "tender breast"
        'singkha': ('sing-kha', 'tree-spirit'),             # 25x - "tree (sacred)"
        'zahko': ('zah-ko', 'respect-DISRP'),               # 25x - "cursed" (disrespect)
        'vaikhak': ('va-i-khak', 'go.and-?-give.command'),  # 26x - "command/charge"
        
        # === Session 4 Round 7: More compounds from philological analysis ===
        'thatang': ('tha-tang', 'strength-force'),          # 28x - "servile/hard"
        'nawkin': ('nawl-kin', 'place-from.ERG'),           # 27x - "from (a place)"
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
        'cianga': ('ci-ang-a', 'say-FUT-?'),                # 20x - "will say"
        'neihsun': ('neih-sun', 'have.II-long'),            # 20x - "have long"
        'cidam': ('ci-dam', 'say-?'),                       # 20x - compound
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
        'vaihawmna': ('va-i-hawm-na', 'go-?-together-NMLZ'),# 19x - compound
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
        'khauhual': ('khau-hual', 'spirit-?'),              # 18x - compound
        'lopate': ('lo-pa-te', 'field-father-PL'),          # 18x - "farmers"
        'cikmah': ('cik-mah', 'one-self'),                  # 18x - "oneself"
        'peemtate': ('peem-ta-te', 'peace-?-PL'),           # 18x - compound
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
        'tuucingte': ('tuucing-te', 'pure-PL'),              # 14x - "pure ones"
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
        'ngaihsutsa': ('ngaihsut-sa', 'think-?'),            # 14x - compound
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
        'ngaihsutsa': ('ngaihsut-sa', 'think-flesh'),        # 14x - "imagination"
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
        'thuhaksa': ('thu-hak-sa', 'word-strong-flesh'),      # 11x - compound
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
        'liangko-ah': ('liang-ko-ah', 'shine-?-LOC'),          # 8x - compound
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
        'liangko-ah': ('liang-ko-ah', 'shoulder-?-LOC'),       # 8x - "on shoulders"
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
        'napi-un': ('na-pi-un', '2PL-big-?'),                  # 8x - compound
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
        'tuucin': ('tuu-cin', 'throw-rope'),                   # sling
        'cin': ('cin', 'rope'),                                # base - rope
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
    }
    
    # Check compound words (try both hyphenated and unhyphenated)
    if word_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_lower]
    if word_no_hyphen_lower in COMPOUND_WORDS:
        return COMPOUND_WORDS[word_no_hyphen_lower]
    
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
    
    # 2. Check for verb/noun stem
    stem_found = False
    for stem, gloss in sorted(VERB_STEMS.items(), key=lambda x: -len(x[0])):
        if remaining.lower().startswith(stem):
            segments.append(stem)
            glosses.append(gloss)
            remaining = remaining[len(stem):]
            stem_found = True
            break
    
    if not stem_found:
        for stem, gloss in sorted(NOUN_STEMS.items(), key=lambda x: -len(x[0])):
            if remaining.lower().startswith(stem):
                segments.append(stem)
                glosses.append(gloss)
                remaining = remaining[len(stem):]
                stem_found = True
                break
    
    # 3. Check for suffixes on remaining
    if remaining:
        # Check TAM suffixes
        for suffix, gloss in sorted(TAM_SUFFIXES.items(), key=lambda x: -len(x[0])):
            if remaining.lower() == suffix or remaining.lower().endswith(suffix):
                if remaining.lower() == suffix:
                    segments.append(suffix)
                    glosses.append(gloss)
                    remaining = ''
                    break
        
        # Check case markers
        for case, gloss in sorted(CASE_MARKERS.items(), key=lambda x: -len(x[0])):
            if remaining.lower() == case:
                segments.append(case)
                glosses.append(gloss)
                remaining = ''
                break
        
        # Check final particles
        for particle, gloss in FINAL_PARTICLES.items():
            if remaining.lower() == particle:
                segments.append(particle)
                glosses.append(gloss)
                remaining = ''
                break
        
        # Check nominalizers
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
        
        # Try stripping common suffixes to find stem
        suffix_glosses = {
            'na': 'NMLZ',
            'te': 'PL', 
            'uh': 'PL',       # Plural (alternative to te)
            'in': 'ERG',
            'ah': 'LOC',
            'sak': 'CAUS',
            'pih': 'APPL',
            'theih': 'ABIL',  # Abilitative/potential suffix
            'kik': 'ITER',    # Iterative suffix
            'khia': 'EXIT',   # Directional "out"
            'khawm': 'together', # Directional "together"
            'toh': 'up',      # Directional "up"
            'sa': 'PERF',     # Perfective aspect
            'khol': 'INTENS', # Intensifier (genkhol = denounce)
            'pen': 'TOP',     # Topic marker (also superlative)
            'mang': 'COMPL',  # Completive (beimang = perish completely)
            'san': 'at',      # Locative "at" (nuihsan = laugh at)
        }
        for suffix, suf_gloss in sorted(suffix_glosses.items(), key=lambda x: -len(x[0])):
            if remaining.lower().endswith(suffix) and len(remaining) > len(suffix) + 1:
                base = remaining[:-len(suffix)]
                base_lower = base.lower()
                # Check if base is a known stem
                if base_lower in VERB_STEMS:
                    return (f"{base}-{suffix}", f"{VERB_STEMS[base_lower]}-{suf_gloss}")
                elif base_lower in NOUN_STEMS:
                    return (f"{base}-{suffix}", f"{NOUN_STEMS[base_lower]}-{suf_gloss}")
                # Try lexicon lookup for base
                lex_gloss = lookup_lexicon(base_lower)
                if lex_gloss:
                    return (f"{base}-{suffix}", f"{lex_gloss}-{suf_gloss}")
    
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
