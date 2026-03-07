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
    'alang': 'vine',         # 73
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
    """Remove punctuation from word, including quotes and apostrophes at word boundaries."""
    # Handle curly quotes (", ", ', ') and other Unicode punctuation
    # Leading: remove quotes, brackets
    word = re.sub(r'^["\'\u201c\u201d\u2018\u2019\[\(\xab\u201e]+', '', word)
    # Trailing: remove punctuation, quotes, brackets
    word = re.sub(r'[.,;:!?\u201c\u201d\u2018\u2019"\'\)\]\xbb]+$', '', word)
    # Remove trailing straight apostrophes
    word = re.sub(r"'+$", '', word)
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
        
        # === Household/Family Compounds ===
        'innkuanpihte': ('innkuanpih-te', 'household-PL'),  # 46x
        'kiphatsakna': ('ki-phatsak-na', 'REFL-glorify-NMLZ'),  # 45x - pride/selfwill
        
        # === Causative Compounds ===
        'paisak': ('pai-sak', 'go-CAUS'),
        'damsak': ('dam-sak', 'well-CAUS'),
        'suaksak': ('suak-sak', 'become-CAUS'),
        'maisak': ('mai-sak', 'face-CAUS'),
        'kumsuk': ('kum-suk', 'bow-CAUS'),
        
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
        'cing': ('cing', 'know'),
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
        'alang': ('a-lang', '3SG-?'),
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
        'sap': ('sap', 'European'),
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
        'alang': ('a-lang', '3SG-vine'),                       # 73
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
        'puantualpi': ('puan-tual-pi', 'cloth-?-big'),        # 39
        'thutak': ('thu-tak', 'word-true'),                   # 39
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
            'in': 'ERG',
            'ah': 'LOC',
            'sak': 'CAUS',
            'pih': 'APPL',
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
