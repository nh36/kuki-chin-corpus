"""
Tedim Chin Compound Words Dictionary

Extracted from analyze_morphemes.py for maintainability.
Contains ~9,700 compound word entries with segmentations and glosses.
"""

COMPOUND_WORDS = {
    # === Opaque Lexemes (no transparent morphological analysis) ===
    'paktat': ('paktat', 'fornication'),  # 122x KJV: harlot/whore/fornication
    '144': ('144', '144'),  # Revelation 7:4 "144,000"
    '000': ('000', '000'),  # Revelation 7:4 "144,000" (comma-split)
    'zawt': ('zawt', 'search'),  # KJV: search, grope
    'lokho': ('lokho', 'husbandman'),  # KJV: husbandman, plowman
    'lokho-in': ('lokho-in', 'farmer-ERG'),
    
    # === Quality audit fixes: 22 partials ===
    'leizang': ('lei-zang', 'land-even'),         # Psalm 26:12 KJV "even place"
    'kuamkeu': ('kuam-keu', 'valley-Baca'),       # Psalm 84:6 place name "valley of Baca"
    'misusia': ('mi-su-sia', 'person-enemy-evil'), # Psalm 137:8 KJV "daughter of Babylon...destroyed"
    "saphulipte'": ("sa-phulip-te'", 'animal-bittern-PL.POSS'), # Isaiah 14:23 KJV "bittern"
    'hui': ('hui', 'fitches'),                    # Isaiah 28:25 KJV "fitches" (plant)
    'eu': ('eu', 'dig'),                          # Isaiah 51:1 KJV "digged"
    'maugua': ('mau-gua', 'bulrush-droop'),       # Isaiah 58:5 KJV "bulrush"
    'zubeel': ('zubeel', 'bottle'),               # Jeremiah 13:12 KJV "bottle" (loanword?)
    'gangawh': ('gan-gawh', 'week-half'),         # Daniel 9:27 KJV "midst of the week"
    'tawlno': ('tawl-no', 'tax-raiser'),          # Daniel 11:20 KJV "raiser of taxes"
    'sbawl': ('s-bawl', 'NMLZ-make'),             # Hosea 7:5 KJV "made...sick" (nominalized?)
    'tuubuk': ('tuu-buk', 'flock-fold'),          # Micah 2:12 KJV "flock in...fold"
    'gunva': ('gun-va', 'owl-night'),             # Zephaniah 2:14 KJV "cormorant" (bird)
    "gunvapite": ("gun-va-pi-te", 'owl-night-big-PL'), # bittern (larger owl)
    "'zuhai": ("'zuhai", 'glutton'),              # Matt 11:19, Luke 7:34 KJV "gluttonous"
    'zuhai': ('zuhai', 'glutton'),                # glutton (without initial apostrophe)
    "khuza'": ("khuza'", 'Chuza'),                # Luke 8:3 proper name
    "tu'n": ("tu'n", 'now.EMPH'),                 # Luke 16:4 contraction "tu + in"
    'saikhar': ('saikhar', 'Sychar'),             # John 4:5 proper name
    'de': ('de', 'torch'),                        # John 18:3 KJV "torches"
    "pirras'": ("pirras'", 'Pyrrhus'),            # Acts 20:4 proper name
    'kaii': ('ka-ii', '1SG-vapor'),               # James 4:14 KJV "vapour"
    'atul': ('a-tul', '3SG-ten.thousand'),        # Rev 5:11 KJV "ten thousand"
    
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
    'meikhukah': ('meikhuk-ah', 'furnace-LOC'),  # 9x - "furnace, smelting pot"
    
    # === Relator Noun + ERG (parallel to +LOC forms) ===
    'sungin': ('sung-in', 'inside-ERG'),
    'tungin': ('tung-in', 'on-ERG'),
    'kiangin': ('kiang-in', 'beside-ERG'),
    'lakin': ('lak-in', 'among-ERG'),
    
    # === Disambiguation compounds (stem + -ah where stem ends in vowel) ===
    'kimkotah': ('kimkot-ah', 'round-LOC'),      # 119x - not kimkota + h
    'dongah': ('dong-ah', 'until-LOC'),          # 52x - not donga + h  
    'bupah': ('bupa-ah', 'centurion-LOC'),       # 4x
    'kimkota': ('kimkot-a', 'round-LOC'),        # variant without -h
    'donga': ('dong-a', 'until-LOC'),            # variant
    
    # === Disambiguation: tuni (today) + suffixes ===
    'tunin': ('tuni-in', 'today-ERG'),           # 8x - not tuni + n
    
    # === Disambiguation: ki-h... compounds (not kih 'abhor' + ...) ===
    # These are ki- (REFL) + verb starting with h
    'kihingkiksak': ('ki-hing-kik-sak', 'REFL-live-return-CAUS'),  # 12x resurrection
    'kihangsak': ('ki-hang-sak', 'REFL-oppose-CAUS'),    # 2x - cause to oppose
    'kihangkeu': ('ki-hang-keu', 'REFL-oppose-refuse'),  # 1x
    'kihawmin': ('ki-hawm-in', 'REFL-share-CVB'),        # 1x
    'kihausak': ('ki-hau-sak', 'REFL-rich-CAUS'),        # 1x
    'kihauhlawh': ('ki-hauh-lawh', 'REFL-desire-able'),  # 1x
    'kihawmsuak': ('ki-hawm-suak', 'REFL-share-become'), # 1x
    'kihawmkeek': ('ki-hawm-keek', 'REFL-share-return'), # 1x
    'kihaih': ('ki-haih', 'REFL-join'),                  # 1x
    'kihingsakkik': ('ki-hing-sak-kik', 'REFL-live-CAUS-return'), # 1x
    'kihaibawl': ('ki-hai-bawl', 'REFL-join-make'),      # 1x
    
    # === Disambiguation: ki-n... compounds (not kin 'god' + ...) ===
    # These are ki- (REFL) + verb starting with n
    'kinaipih': ('ki-nai-pih', 'REFL-near-APPL'),        # 4x - approach closely
    'kininsaksa': ('ki-nin-sak-sa', 'REFL-pity-CAUS-PASS'), # 2x - be divorced
    'kininsaktawm': ('ki-nin-sak-tawm', 'REFL-pity-CAUS-finish'), # 2x
    'kinaih': ('ki-nai-h', 'REFL-near-NOM'),             # 1x
    'kinawtkhia': ('ki-nawt-khia', 'REFL-scratch-out'),  # 1x
    'kinawmvalhin': ('ki-nawm-val-hin', 'REFL-enjoy-good-QUOT'), # 1x - swallowed up pleasurably
    
    # === More disambiguations (remaining partials) ===
    'phakik': ('pha-kik', 'year-return'),           # 2x - renew, anew
    'thukip': ('thuk-ip', 'deep-INTENS'),           # 2x - very deep
    'thukipin': ('thuk-ip-in', 'deep-INTENS-ERG'),  # variant
    'kisilhsak': ('ki-silh-sak', 'REFL-clothe-CAUS'), # 2x - clothe oneself
    'lianpenin': ('lian-pen-in', 'great-COMPAR-ERG'), # 3x - most greatly
    'sukkhapte': ('suk-khap-te', 'push-close-PL'),        # 1x - push shut
    'siahsun': ('siah-sun', 'decay-think'),         # 1x - consider decay
    'thukhupna': ('thuk-hup-na', 'deep-cover-NMLZ'), # 1x - covering depth
    'guallelhsak': ('gual-lelh-sak', 'row-arrange-CAUS'), # 1x
    'thamang': ('tha-mang', 'strength-dream'),      # 1x - (compound)
    'tawnggawp': ('tawng-gawp', 'contend-INTENS'),  # 1x
    
    # === Intensifiers/Adverbs ===
    'dipkuathuai': ('dipkua-thuai', 'terrifying-INTENS'),  # 6x - "very terrible"
    'lamethuai': ('lamet-huai', 'vanity'),                 # 2x - "vanity, emptiness"
    
    # === Religious vocabulary ===
    'biakbuk': ('biak-buk', 'worship-tent'),  # 112x - sanctuary/tabernacle
    'vei-a': ('vei-a', 'wave-LOC'),    # wave offering (vei-a piak/biakna)
    'veia': ('vei-a', 'wave-LOC'),     # unhyphenated form
    
    # === Verb + Quotative Compounds ===
    'ci-in': ('ci-in', 'say-QUOT'),
    'cih': ('cih', 'say.NOM'),  # nominalized
    'ciin': ('ci-in', 'say-QUOT'),
    'a ci hi': ('a ci hi', '3SG say DECL'),
    
    # === TAM Compounds ===
    'dingin': ('ding-in', 'IRR-ERG'),
    'nadingun': ('na-ding-un', '2SG-IRR-IMP'),
    'adingin': ('a-ding-in', '3SG-IRR-ERG'),
    'kadingin': ('ka-ding-in', '1SG-IRR-ERG'),
    'ading': ('a-ding', '3SG-IRR'),
    'kading': ('ka-ding', '1SG-IRR'),
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
    'vantung': ('van-tung', 'sky-on'),
    'lungsim': ('lung-sim', 'stone-mind'),
    'minam': ('mi-nam', 'person-kind'),
    'kumpipa': ('kumpi-pa', 'king-male'),
    'nasempa': ('nasem-pa', 'servant-male'),
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
    'kihongin': ('ki-hong-in', 'REFL-open-CVB'),
    'kikhel': ('ki-khel', 'REFL-differ'),
    'kipawlna': ('ki-pawl-na', 'REFL-associate-NMLZ'),  # 35x - association
    'kitotna': ('ki-tot-na', 'REFL-cut-NMLZ'),  # 35x - separation
    'kilawmna': ('ki-lawm-na', 'REFL-worthy-NMLZ'),  # 3x - worthiness/suitability
    'kihutna': ('ki-hut-na', 'REFL-shelter-NMLZ'),  # 3x - refuge
    'kilakna': ('ki-lak-na', 'REFL-appear-NMLZ'),  # 2x - appearing
    
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
    'awk': ('awk', 'trap'),  # 35x - "ram" (standalone noun)
    'vet': ('vet', 'do'),  # 35x - base verb
    'vawh': ('vawh', 'name'),  # 34x - "name" (a vawh = named)
    'puantualpi': ('puan-tual-pi', 'cloth-many.colored-big'),  # 39x - Joseph's coat
    'khutnuaiah': ('khut-nuai-ah', 'hand-below-LOC'),  # 35x - "under the hand of"
    
    # === Causative Compounds ===
    'paisak': ('pai-sak', 'go-CAUS'),
    'damsak': ('dam-sak', 'well-CAUS'),
    'suaksak': ('suak-sak', 'become-CAUS'),
    'maisak': ('mai-sak', 'face-CAUS'),
    'kumsuk': ('kum-suk', 'bow-DOWN'),  # bow down (directional)
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
    'peuhpeuh': ('peuhpeuh', 'every'),
    
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
    'ahihleh': ('ahihleh', 'if'),  # hih is Form II of hi
    'hitaleh': ('hitaleh', 'if.so'),
    'laitakin': ('lai-tak-in', 'midst-exact-ERG'),
    
    # === Negation Compounds ===
    'loh': ('lo-h', 'NEG-NOM'),
    'loin': ('lo-in', 'NEG-ERG'),
    'kuamah': ('kuamah', 'nobody'),  # "nobody"
    'bangmah': ('bangmah', 'nothing'),  # "nothing"
    'bangmahin': ('bang-mah-in', 'what-EMPH-ERG'),  # "in no way"
    
    # === bang- (what/how/like) compounds - must precede ba- matching ===
    'bang': ('bang', 'like'),        # 4263x
    'bangci': ('bangci', 'how'),    # "how" 224x
    'banga': ('bang-a', 'what-LOC'),      # "as/like" 79x
    'bangun': ('bang-un', 'what-PL'),     # 84x
    'bangzah': ('bang-zah', 'what-quantity'),  # "how many" 65x
    'bangbang': ('bang~bang', 'what~REDUP'),     # "whatever" 48x
    'bangte': ('bang-te', 'what-PL'),     # 32x
    'bangzahin': ('bang-zah-in', 'what-quantity-ERG'),  # 28x
    'bangbangin': ('bang-bang-in', 'what-REDUP-ERG'),     # 28x
    'bangsak': ('bang-sak', 'what-CAUS'), # 26x
    'bangcih': ('bang-cih', 'what-say.NOM'),  # 15x
    'bangsakkik': ('bang-sak-kik', 'what-CAUS-ITER'),  # 12x
    'bangteng': ('bang-teng', 'what-dwell'),   # 10x
    'bangzia': ('bang-zia', 'what-manner'),    # 6x
    'bangkik': ('bang-kik', 'what-ITER'),      # 4x
    'bangbangun': ('bang-bang-un', 'what-REDUP-PL'),  # 4x
    'bangpi': ('bang-pi', 'what-big'),    # 3x
    'bangkhat': ('bang-khat', 'what-one'),# 3x
    'bangah': ('bang-ah', 'what-LOC'),    # 2x
    'bangta': ('bang-ta', 'what-PFV'),    # 2x
    
    # === ban- (besides/in addition to) compounds ===
    'banah': ('ban-ah', 'besides-LOC'),   # 138x "in addition to"
    
    # === Number Compounds ===
    'sawmahkhat': ('sawm-ah-khat', 'ten-LOC-one'),  # 47x - "tithe/tenth"
    
    # === Case Markers ===
    'pan': ('pan', 'ABL'),            # ablative "from" - 603x standalone
                                      # Note: pan as verb "plead" only in compounds (langpan, panna)
    'panin': ('pan-in', 'ABL-ERG'),   # "from" (double case marking)
    'sangin': ('sang-in', 'high-ERG'),  # "than"
    'tawh': ('tawh', 'COM'),  # "with"
    
    # === Pronoun Compounds ===
    'keimah': ('keimah', '1SG.PRO'),
    'nangmah': ('nangmah', '2SG.PRO'),
    'amah': ('amah', '3SG.PRO'),
    'amaute': ('amaute', '3PL.PRO'),
    
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
    # pan removed - ABL postposition (not 'begin'); verb only in kipan (REFL-begin)
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
    'kham': ('kham', 'gold'),
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
    'kisai-in': ('ki-sai-in', 'REFL-concern-CVB'),
    'biakna-in': ('biakna-in', 'worship-ERG'),
    'cihin-ah': ('cih-in-ah', 'say.II-ERG-LOC'),  # cih is Form II of ci
    'genin-ah': ('gen-in-ah', 'speak-ERG-LOC'),
    'ma-in': ('ma-in', 'self-ERG'),
    'zan-in': ('zan-in', 'night-ERG'),
    'muhna-ah': ('muh-na-ah', 'see.II-NMLZ-LOC'),
    'gei-ah': ('gei-ah', 'edge-LOC'),
    
    # === Compound verbs ===
    'ciahkik': ('ciah-kik', 'return-ITER'),
    'paisuak': ('pai-suak', 'go-become'),
    'paikhiatpih': ('pai-khiat-pih', 'go-emerge-APPL'),
    'semsem': ('sem~sem', 'serve~REDUP'),
    
    # === Quantifiers ===
    'khatpeuh': ('khat-peuh', 'one-every'),
    'khatlekhat': ('khat-le-khat', 'one-and-one'),
    'khatah': ('khat-ah', 'one-LOC'),
    'sawmthum': ('sawm-thum', 'ten-three'),
    'sawmli': ('sawm-li', 'ten-four'),
    'sagih': ('sagih', 'seven'),
    'vekpi-in': ('vek-pi-in', 'all-big-ERG'),
    
    # === Other high-frequency compounds ===
    'hoihtak': ('hoih-tak', 'good-exact'),
    'thahat': ('tha-hat', 'strong-firm'),
    'thukhen': ('thu-khen', 'word-divide'),
    'neihsa': ('neih-sa', 'have.II-PAST'),                  # had (past of have)
    # paknamtui now handled by hierarchical system → 'ointment'
    'minthanna': ('min-than-na', 'name-bless-NMLZ'),
    'suanlekhakte': ('suanlekhak-te', 'genealogy-PL'),       # fixed: was over-segmented
    'nisuahna': ('ni-suah-na', 'day-birth-NMLZ'),
    'mihingte': ('mi-hing-te', 'person-kind-PL'),
    'zanin': ('zan-in', 'night-ERG'),
    'omkhawm': ('om-khawm', 'exist-gather'),
    'khuamial': ('khuamial', 'darkness'),  # opaque: khua=atmosphere + mial=dark (cf. khuavak=light)
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
    'thumuhnate': ('thu-muhna-te', 'word-vision-PL'),  # 3x - visions/understandings
    'awging': ('aw-ging', 'voice-sound'),
    'siamna': ('siam-na', 'skilled-NMLZ'),
    'thahatna': ('tha-hat-na', 'strong-firm-NMLZ'),
    'hoihzaw': ('hoih-zaw', 'good-more'),
    'kilemna': ('ki-lem-na', 'REFL-prepare-NMLZ'),
    'tuni-in': ('tu-ni-in', 'now-day-ERG'),
    'naupang': ('nau-pang', 'child-small'),
    'naupangte': ('nau-pang-te', 'child-small-PL'),  # 59x - "children"
    'naupangno': ('nau-pang-no', 'child-small-DIM'),  # "little child"
    'lawmte': ('lawm-te', 'friend-PL'),
    'lopi-in': ('lo-pi-in', 'NEG-big-ERG'),
    'zakhat': ('za-khat', 'hundred-one'),
    'mipihte': ('mi-pih-te', 'person-APPL-PL'),
    'kongpi': ('kong-pi', 'road-big'),
    'kawikawi': ('kawi~kawi', 'crooked~REDUP'),
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
    'misia': ('mi-sia', 'person-evil'),              # 13x - "evil person/wicked"
    'misiate': ('mi-sia-te', 'person-evil-PL'),      # 3x - "evil people"
    'lui': ('lui', 'river'),
    'sepna': ('sep-na', 'work-NMLZ'),
    'thungetna': ('thu-nget-na', 'word-request-NMLZ'),
    'gitlohna': ('git-loh-na', 'hate-NEG-NMLZ'),
    'phawksakna': ('phawk-sak-na', 'remember-CAUS-NMLZ'), # 2x - "memorial, reminder"
    'thakhauhsakna': ('tha-khauh-sak-na', 'strength-strong-CAUS-NMLZ'), # 2x - "strengthening"
    'awkin': ('awk-in', 'snare-ERG'),              # 3x - "being snared" (not a-wkin)
    'kituhna': ('ki-tuh-na', 'REFL-dispute-NMLZ'),  # 2x - "controversy, dispute"
    'tenna': ('ten-na', 'dwell-NMLZ'),
    'tampite': ('tam-pi-te', 'many-big-PL'),
    'pawlkhatte': ('pawl-khat-te', 'some-one-PL'),
    'dingte': ('ding-te', 'stand-PL'),
    'dingun': ('ding-un', 'IRR-PL.IMP'),
    'pawi': ('pawi', 'Pawi'),
    'pang': ('pang', 'side'),
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
    'dinga': ('ding-a', 'IRR-LOC'),
    
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
    'cihnopna': ('cih-nop-na', 'say.II-want-NMLZ'),  # cih is Form II of ci
    'lupna': ('lupna', 'bed'),                # opaque - bed/couch
    'lupnate': ('lupna-te', 'bed-PL'),        # beds
    'mawkna': ('mawk-na', 'err-NMLZ'),
    'hauhna': ('hauh-na', 'shout-NMLZ'),
    'thugenna': ('thu-gen-na', 'word-speak-NMLZ'),
    'nitumna': ('ni-tum-na', 'day-all-NMLZ'),
    
    # === More -te plurals ===
    'makaite': ('makai-te', 'leader-PL'),
    'zite': ('zi-te', 'wife-PL'),
    'hihte': ('hih-te', 'this-PL'),
    'mizawngte': ('mi-zawng-te', 'person-all-PL'),
    'siate': ('sia-te', 'evil-PL'),
    'omlaite': ('om-lai-te', 'exist-midst-PL'),
    'thupiaknate': ('thu-piak-na-te', 'word-give.to-NMLZ-PL'),
    
    # === More compound words ===
    'pasian-te': ('pasian-te', 'god-PL'),
    'lonona': ('lo-no-na', 'NEG-obey-NMLZ'),                 # disobedience (transparent)
    'puanbuk': ('puan-buk', 'cloth-shelter'),                # tent (transparent)
    'lutang': ('lu-tang', 'head-leader'),                    # chief/head (NOT pillow - see Gen 36:21)
    'hotkhiatna': ('hot-khiat-na', 'save-away-NMLZ'),        # salvation (transparent)
    'pawlpi': ('pawl-pi', 'group-big'),
    'khawl': ('khawl', 'rest'),
    'tungtawnin': ('tung-tawn-in', 'on-ever-ERG'),
    'muang': ('muang', 'trust'),
    'neu': ('neu', 'small'),
    'ciangkhut': ('ciang-khut', 'then-hand'),
    'lakhia': ('lak-khia', 'take-exit'),
    'awng': ('awng', 'open'),
    'namtui': ('nam-tui', 'kind-water'),
    'ciam': ('ciam', 'promise'),
    'luang': ('luang', 'flow'),
    'bawlsak': ('bawl-sak', 'make-CAUS'),
    'amahmah': ('a-mah-mah', '3SG-self~REDUP'),
    'sawmsagih': ('sawm-sagih', 'ten-seven'),
    'thuhilh': ('thu-hilh', 'word-teach'),
    'thuhilhte': ('thu-hilh-te', 'word-teach-PL'),   # ordinances/customs (19x)
    'bawlsa': ('bawl-sa', 'make-PAST'),                     # made (past of make)
    'peuh': ('peuh', 'every'),
    'zanih': ('zan-ih', 'night-NOM'),
    'suksiat': ('suk-siat', 'CAUS-destroy'),
    'khau': ('khau', 'rope'),
    'tuute': ('tuu-te', 'grandchild-PL'),
    'lua': ('lua', 'exceed'),
    
    # === More compounds (frequency 70-110) ===
    'kipte': ('kip-te', 'edge-PL'),
    'lungkham': ('lung-kham', 'heart-anxious'),
    'khuasung': ('khua-sung', 'town-inside'),
    'kaikhawm': ('kai-khawm', 'call-gather'),
    'thunuama': ('thu-nuam-a', 'word-want-LOC'),
    'nopsakna': ('nop-sak-na', 'want-CAUS-NMLZ'),
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
    'kungte': ('kung-te', 'trunk-PL'),
    'alang': ('alang', 'side'),                       # "in the side" - not a-lang!
    'lampi-ah': ('lampi-ah', 'way-LOC'),
    'pasalte': ('pasal-te', 'husband-PL'),
    'hi-in': ('hi-in', 'be-ERG'),
    'biakinn-ah': ('biakinn-ah', 'temple-LOC'),
    'vekpi-un': ('vek-pi-un', 'all-big-PL.IMP'),
    'nungzui': ('nungzui', 'disciple'),         # back-follow → disciple (per dictionary)
    'nungzuite': ('nungzui-te', 'disciple-PL'), # disciples
    'cina': ('cina', 'sick'),                   # ill, sick (adj) - dictionary: "cina (damlo), adj. ill; sick"
    'cinate': ('cina-te', 'sick.person-PL'),    # patients, sick persons - dictionary: "cinate, n. patients; sick person"
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
    'khuam': ('khuam', 'darkness'),
    'sap': ('sap', 'call'),
    'sal': ('sal', 'slave'),
    'kan': ('kan', 'stay'),
    'vai': ('vai', 'foreigner'),
    'kumpi-in': ('kumpi-in', 'king-ERG'),
    'khuaneute': ('khua-neu-te', 'town-small-PL'),
    'tuamtuamte': ('tuam-tuam-te', 'different-REDUP-PL'),
    'gamh': ('gamh', 'land.II'),
    
    # === Miscellaneous High-Frequency ===
    'gamlakah': ('gam-lak-ah', 'land-midst-LOC'),
    'inla': ('inla', 'and.then'),
    'sunga': ('sung-a', 'inside-3SG'),
    'tunga': ('tung-a', 'on-3SG'),
    'ama': ('ama', '3SG.POSS'),                          # his/her/its possessive
    'nau': ('nau', 'child'),
    'aana': ('a-ana', '3SG-child.PL'),
    'pah': ('pah', 'do.so'),
    'hileh': ('hi-leh', 'be-if'),
    'unla': ('un-la', 'PL.IMP-and'),
    
    # === More common noun forms ===
    'mai-ah': ('mai-ah', 'face-LOC'),
    'khua-ah': ('khua-ah', 'town-LOC'),
    'inn-ah': ('inn-ah', 'house-LOC'),
    'pasal': ('pasal', 'husband'),
    'pawlkhat': ('pawl-khat', 'some-one'),
    'mihing': ('mi-hing', 'person-kind'),
    'minamte': ('mi-nam-te', 'person-kind-PL'),
    'nasep': ('nasep', 'work'),                                # OPAQUE: not na-sep (na NMLZ is suffix!)
    'nasem': ('nasem', 'servant'),                             # OPAQUE: not na-sem
    'suante': ('suan-te', 'offspring-PL'),
    'namsau': ('namsau', 'sword'),                             # OPAQUE: 234x - sword (not nam-sau)
    'nangawn': ('na-ngawn', '2SG-own'),
    'piang': ('piang', 'be.born'),
    'hihna': ('hih-na', 'this-NMLZ'),
    'lungdam': ('lung-dam', 'heart-well'),
    'itna': ('it-na', 'love-NMLZ'),
    'nungta': ('nung-ta', 'life-PFV'),
    'uliante': ('ulian-te', 'elder-PL'),
    'huh': ('huh', 'help'),
    'khuapite': ('khua-pi-te', 'town-big-PL'),
    'lohna': ('loh-na', 'NEG-NMLZ'),
    'kam': ('kam', 'mouth'),                                 # mouth (body part), not 'word'
    'mual': ('mual', 'mountain'),
    'sathau': ('sa-thau', 'flesh-fat'),                      # fat (transparent)
    'tuipi': ('tui-pi', 'water-big'),
    'hehna': ('heh-na', 'anger-NMLZ'),
    'upna': ('up-na', 'believe-NMLZ'),
    'nungzuite': ('nungzui-te', 'disciple-PL'),              # disciples (not life-follow-PL)
    'khawm': ('khawm', 'gather'),
    'ciat': ('ciat', 'each'),
    'dangte': ('dang-te', 'other-PL'),
    'tate': ('ta-te', 'child-PL'),
    'nate': ('na-te', '2SG-PL'),
    'kizui-in': ('ki-zui-in', 'REFL-follow-CVB'),
    'la-in': ('la-in', 'take-ERG'),
    
    # === Additional compounds from frequency analysis (freq 50-230) ===
    # leenggahzu now handled by hierarchical system → 'grape.juice'
    'sumngo': ('sum-ngo', 'brass-iron'),                      # 152 - brass and iron (metals)
    'leenggui': ('leeng-gui', 'grape-vine'),                  # 130 - grapevine
    'ling': ('ling', 'pile'),                                  # 106
    'panun': ('pa-nun', 'father-life'),                        # 101
    'leenggah': ('leeng-gah', 'grape-cluster'),               # 98 - grape clusters
    'mudah': ('mu-dah', 'see-easy'),                           # 97
    'keel': ('keel', 'heel'),                                  # 85
    'salin': ('sa-lin', 'meat-hope'),                          # 82
    'lametna': ('lam-et-na', 'path-example-NMLZ'),        # 81
    'pak': ('pak', 'divide'),                              # 78
    'thei-in': ('thei-in', 'know.I-ERG'),                  # 75
    'le-uhcin': ('le-uh-cin', 'also-PL-even'),            # 74
    # alang duplicate removed - defined above
    'zin': ('zin', 'travel'),                             # 73
    'sawh': ('sawh', 'correct'),                           # 72
    'nisimin': ('ni-simin', 'day-always'),                # 70
    'tuikhuk': ('tui-khuk', 'water-ladle'),               # 68
    'late': ('la-te', 'song-PL'),                          # 68
    'mualtungah': ('mual-tung-ah', 'mountain-top-LOC'),   # 66
    'kang': ('kang', 'suffer'),                            # 66
    'lauhuai': ('lau-huai', 'fear-dread'),                # 65
    'vaihawm': ('vai-hawm', 'plan-counsel'),              # 63
    'lite': ('li-te', 'four-PL'),                          # 60
    'bawngtalte': ('bawng-tal-te', 'cow-calf-PL'),        # 59
    'kahna': ('kah-na', 'fight-NMLZ'),                     # 59
    'neute': ('neu-te', 'small-PL'),                       # 58
    'tangvalpa': ('tangval-pa', 'youth-father'),          # 58
    'khialhnate': ('khialh-na-te', 'sin-NMLZ-PL'),        # 57
    'nuai-a': ('nuai-a', 'below-LOC'),                     # 56
    'kihei-in': ('ki-hei-in', 'REFL-angry-CVB'),          # 56
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
    'gengen': ('gen~gen', 'speak~REDUP'),                   # 50
    'gengenin': ('gen-gen-in', 'speak-REDUP-ERG'),           # 3x - "speaking intensively"
    'samsia': ('sam-sia', 'call-destroy'),                # 50
    'lungdamsak': ('lung-dam-sak', 'heart-well-CAUS'),    # 50
    'ante': ('an-te', '3PL-PL'),                          # 50
    'tuni-a': ('tu-ni-a', 'now-day-LOC'),                 # 50
    'biakpiaknate': ('biak-piak-na-te', 'worship-give-NMLZ-PL'), # 50
    # Note: nusiat is Form II of nusia, handled in VERB_STEM_PAIRS
    'pianzia': ('pian-zia', 'birth-manner'),              # 50
    
    # === More compounds from frequency analysis (freq 38-55) ===
    # leenggahzu now handled by hierarchical system
    # leenggui already defined above
    # sumngo already defined above
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
    'nasepnate': ('nasep-na-te', 'work-NMLZ-PL'),            # 47 - "works"
    'puanhampi': ('puan-ham-pi', 'cloth-cover-big'),      # 45
    'sawt': ('sawt', 'long.time'),                         # 45
    'zawng': ('zawng', 'all'),                              # 45
    'nun': ('nun', 'knop'),                                # 45 - decorative bud on lampstand (KJV "knop")
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
    'thutak': ('thu-tak', 'word-true'),                   # 39
    
    # === Session 3: More compounds ===
    'letmat': ('let-mat', 'half-cubit'),                  # 34 - "cubit and a half"
    'thuciam': ('thu-ciam', 'word-promise'),              # 33 - "covenant, promise"
    'thumin': ('thum-in', 'three-ERG'),                   # transparent: three + ERG
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
    'theithei': ('thei~thei', 'know.I~REDUP'),              # 33 - "perceive/know" (reduplicated)
    'singte': ('sing-te', 'tree-PL'),                     # 33 - "trees"
    'lungnuam': ('lung-nuam', 'heart-pleased'),           # 32 - "pleased, glad"
    'khiate': ('khia-te', 'exit-PL'),                     # variant
    'lakhia-in': ('la-khia-in', 'take-out-ERG'),          # 32 - "taking out"
    'luanna': ('luan-na', 'flow-NMLZ'),                   # 32 - "flowing"
    'singkungte': ('singkung-te', 'tree-PL'),             # 32 - "trees"
    'honpi': ('hon-pi', 'flock-big'),                     # 31 - "great multitude, swarm"
    
    # === Session 3: More compounds (corrections) ===
    'dawng': ('dawng', 'receive'),                    # 387 - "get, receive, fetch"
    'dawngin': ('dawng-in', 'receive-ERG'),          # 143 - "getting, receiving"
    'langkhatah': ('lang-khat-ah', 'side-one-LOC'),      # 88 - "against" (at one side)
    'langpangin': ('langpang-in', 'against-ERG'),     # 63 - "against"
    'langpang': ('langpang', 'against'),              # 39 - "against, oppose"
    'langkhat': ('lang-khat', 'side-one'),               # 35 - "one side"
    'singlamteh': ('sing-lam-teh', 'wood-cross'),        # 65 - "cross" (the cross)
    'singkuang': ('sing-kuang', 'wood-box'),             # 45 - "ark" (wooden box)
    
    # === Session 3: More compounds (round 2) ===
    'siangthosak': ('siangtho-sak', 'holy-CAUS'),        # 32 - "sanctify"
    'piansak': ('pian-sak', 'create-CAUS'),              # 32 - "creation"
    'lausak': ('lau-sak', 'fear-CAUS'),                  # 31 - "make afraid"
    'galkidona': ('gal-kido-na', 'enemy-fight-NMLZ'),    # 31 - "warfare"
    'galkidonate': ('gal-ki-do-na-te', 'enemy-REFL-fight-NMLZ-PL'),  # 1x - "wars"
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
    'bawngnawi': ('bawng-nawi', 'cow-milk'),             # 30 - KJV "milk" (not butter)
    'khualmi': ('khual-mi', 'sojourn-person'),           # 30 - "stranger, sojourner"
    'nidang': ('ni-dang', 'day-other'),                  # 30 - "formerly, before"
    'khangham': ('khang-ham', 'generation-full'),        # 30 - "full of years"
    'sawmkua': ('sawm-kua', 'ten-nine'),                 # 30 - "ninety"
    'anlak': ('an-lak', 'rice-harvest'),                 # 30 - "harvest"
    
    # === Session 3: More compounds (round 4) ===
    'simmawhbawl': ('simmawh-bawl', 'blaspheme-do'),     # 33 - "commit blasphemy"
    'phaknatna': ('phaknat-na', 'leprosy-NMLZ'),         # 31 - "leprosy"
    'zahzah': ('zah~zah', 'fear~REDUP'),                   # 30 - "every living" (reduplicated)
    'kalaohte': ('kalaoh-te', 'camel-PL'),               # 30 - "camels"
    'kihtakna': ('kihtak-na', 'dread-NMLZ'),             # 30 - "dread"
    'suahtakna': ('suahtak-na', 'redeem-NMLZ'),          # 30 - "redemption"
    'khangno': ('khang-no', 'generation-young'),         # 30 - "youngest"
    'honpite': ('hon-pi-te', 'flock-big-PL'),            # 29 - "great multitudes"
    
    # === Session 3: More compounds (round 5) ===
    'kihtakhuai': ('kihtak-huai', 'dread-causing'),      # 46 - "dreadful, terrible"
    'aksite': ('aksi-te', 'star-PL'),                    # 32 - "stars"
    'behbehin': ('beh-beh-in', 'tribe~REDUP-ERG'),         # 32 - "by tribes"
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
    'nasemnu': ('nasem-nu', 'servant-female'),         # 26 - "your maidservant"
    'paktatna': ('pak-tat-na', 'proclaim-strike-NMLZ'), # 30 - "proclamation"
    'paikhiatpihin': ('paikhiat-pih-in', 'send.away-APPL-CVB'), # 28 - "sending away"
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
    'khawng': ('khawng', 'about'),         # 21 - "about, approximately"
    'khawhlawhte': ('khawh-lawh-te', 'able-earn-PL'),    # 18 - "earners, workers"
    'khawh': ('khawh', 'able'),                      # 15 - "can, able to"
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
    'kal': ('kal', 'kidney'),                            # 32 - "kidney" (body part) - KJV "the two kidneys"
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
    'thumsak': ('thum-sak', 'entreat-CAUS'),             # 19 - "intercede, pray for"
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
    'sil': ('sil', 'flesh'),                       # 30x - "flesh, body"
    'ning': ('ning', 'will'),                     # 30x - modal auxiliary
    'theitel': ('thei-tel', 'know.I-exact'),            # 30x - "know exactly"
    'nisuh': ('ni-suh', 'day-count'),                   # 30x - "days"
    'lai-at': ('lai-at', 'middle-LOC'),                 # 30x - "at the middle"
    'matengun': ('mateng-un', 'until-PL.IMP'),          # 29x - "until (plural)"
    'tuh': ('tuh', 'sow'),                        # 29x - "sow, plant"
    'gamlapi-ah': ('gamlapi-ah', 'wilderness-LOC'),     # 28x - "in the wilderness"
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
    'kawng': ('kawng', 'road'),                     # 25x - "road, way"
    'nengniam': ('neng-niam', 'stranger-oppress'),          # 25x - vex/oppress stranger
    'singkha': ('sing-kha', 'wood-acacia'),                  # 25x - shittim/acacia wood
    'khate': ('khat-te', 'one-PL'),                     # 25x - "some (ones)"
    'kawlsing': ('kawl-sing', 'fry-wood'),              # 25x - compound
    'paai': ('pa-ai', 'father-love'),                   # 25x - compound
    'ngeite': ('ngei-te', 'have.NMLZ-PL'),              # 25x - "possessions"
    # Note: hawlkhiat is Form II of hawlkhia, handled in VERB_STEM_PAIRS
    'zahko': ('zah-ko', 'despise-curse'),                   # 25x - curse/despise
    'mihau': ('mi-hau', 'person-rich'),                 # 25x - "rich person"
    'thatlum': ('that-lum', 'kill-all'),                # 25x - "kill all"
    'milian': ('mi-lian', 'person-great'),              # 25x - "great person"
    'mul': ('mul', 'hair'),                             # 24x - "hair"
    'tuunote': ('tuuno-te', 'lamb-PL'),                 # 24x - "lambs"
    
    # === Session 4 Round 5: More compounds ===
    'paipihto': ('paipih-to', 'accompany-sit'),         # 24x - "accompany"
    # kahto entry moved to later section with correct analysis
    'awmdal': ('awm-dal', 'exist-remain'),              # 24x - "remain, stay"
    'val': ('val', 'go.quickly'),                       # 24x - "go quickly"
    'buktual': ('buk-tual', 'hole-dig'),                # 24x - "dig pit"
    'kawikawi-in': ('kawikawi-in', 'crooked-ERG'),      # 24x - "crookedly"
    'muk': ('muk', 'kiss'),                             # 24x - "kiss"
    'panmun': ('pan-mun', 'plead-place'),               # 24x - "altar"
    'gennop': ('gen-nop', 'speak-soft'),                # 24x - "speak softly"
    'gahte': ('gah-te', 'fruit-PL'),                    # 23x - "fruits"
    'pahpah': ('pah~pah', 'immediately~REDUP'),              # 23x - "each father"
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
    'ngate': ('ngate', 'those'),                   # 22x - "those" (demonstrative)
    'tote': ('to-te', 'lord-PL'),                       # 22x - "lords"
    'bawnghon': ('bawng-hon', 'cattle-flock'),          # 22x - "herd"
    'nungakte': ('nungak-te', 'girl-PL'),               # 22x - "daughters, maidens"
    'hoihpente': ('hoih-pen-te', 'good-SUPER-PL'),      # 22x - "best ones"
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
    'kahto': ('kah-to', 'climb-up'),                    # 37x - "ascend" (kah=climb, to=up)
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
    'cithei': ('ci-thei', 'say-ABIL'),                  # 21x - "can say"
    'theihtelna': ('theih-tel-na', 'know.II-help-NMLZ'),# 21x - "understanding"
    'galkapmangte': ('galkap-mang-te', 'soldier-chief-PL'),# 21x - "captains"
    'simzawh': ('sim-zawh', 'count-finish'),            # 21x - "finish counting"
    'nausuak': ('nau-suak', 'child-birth'),             # 21x - "childbirth"
    'kuate': ('kua-te', 'who-PL'),                      # 21x - "who (plural)"
    'piaktheih': ('piak-theih', 'give.to-ABIL'),        # 21x - "able to give"
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
    'muhtheih': ('muh-theih', 'see.II-ABIL'),           # 20x - "visible/able to see"
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
    'bawk': ('bawk', 'bottle'),                    # 19x - "bottle" or "cast"
    'sauvei': ('sau-vei', 'long-journey'),              # 19x - "sojourn"
    'theikung': ('theih-kung', 'oil-tree'),             # 19x - "olive tree"
    'pangsim': ('pang-sim', 'plead-count'),             # 19x - "smite"
    'gamdai': ('gam-dai', 'land-overcome'),             # 19x - "overcome"
    'genthei': ('gen-thei', 'speak-ABIL.NEG'),          # 19x - "wretched"
    'semkhawm': ('sem-khawm', 'serve-together'),        # 19x - "serve together"
    'tom': ('tom', 'dwell'),                            # 19x - "dwell/sit"
    'puakhia': ('puak-hia', 'send-away'),               # 19x - "send away"
    'zal': ('zal', 'spread'),                           # 19x - "spread"
    'ip': ('ip', 'cover'),                              # 19x - "cover"
    'kuana': ('kua-na', 'who-NMLZ'),                    # 19x - compound
    'dingteng': ('ding-teng', 'stand-tell'),            # 19x - "stand and tell"
    'pahtak': ('pa-tak', 'father-true'),                # 19x - "true father"
    'galkapmang': ('galkap-mang', 'soldier-chief'),     # 19x - "captain"
    'nektheih': ('nek-theih', 'eat.II-ABIL'),           # 19x - "edible"
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
    'hin': ('hin', 'this.EMPH'),                        # 21x - demonstrative emphatic
    'nipikal': ('ni-pi-kal', 'day-big-fold'),           # 21x - "week"
    'bawngte': ('bawng-te', 'cattle-PL'),               # 21x - "cattle"
    'banbanin': ('ban-ban-in', 'side-side-ERG'),        # 21x - "ministering"
    'kawi': ('kawi', 'forth'),                          # 19x - "back and forth"
    'thugennate': ('thu-gen-na-te', 'word-speak-NMLZ-PL'),# 18x - "words spoken"
    'hunsung': ('hun-sung', 'time-inside'),             # 18x - "during/meanwhile"
    'huaiham': ('huai-ham', 'dread-strong'),            # 18x - "jealous"
    'laikhak': ('lai-khak', 'letter-seal'),             # 18x - "sealed letter"
    'zanglei': ('zang-lei', 'use-buy'),                 # 18x - compound
    'zanglei-ah': ('zang-lei-ah', 'use-buy-LOC'),       # 18x - compound
    'ngahkhawm': ('ngah-khawm', 'get-together'),        # 18x - "gather"
    'thahatte': ('tha-hat-te', 'strength-hard-PL'),     # 18x - "strong ones"
    'gihna': ('gihna', 'tremble'),                       # 18x - DISAMBIGUATION: separate root, not gih-na
    'nidanga': ('ni-dang-a', 'day-other-LOC'),          # 18x - "other day"
    'nitaang': ('ni-taang', 'day-long'),                # 18x - "long day"
    'inntual': ('inn-tual', 'house-floor'),             # 18x - "house floor"
    'khemsa-in': ('khem-sa-in', 'restrain-early-ERG'),  # 18x - "restraining"
    
    # === Session 4 Round 10: High-frequency remaining vocab ===
    'thumu': ('thumu', 'trumpet'),                   # 28x - "trumpet" (opaque lexeme)
    'kawmte': ('kawm-te', 'beam-PL'),                    # 18x - "beams/posts"
    'zahtakbawl': ('zahtak-bawl', 'honor-do'),          # 18x - "reverence"
    'puansan': ('puan-san', 'cloth-wear'),              # 18x - "apparel"
    'uptheih': ('up-theih', 'elder.sibling-ABIL'),      # 18x - "lay/rest"
    'puanbukte': ('puan-buk-te', 'cloth-cover-PL'),     # 17x - "tents"
    'kawl': ('kawl', 'heifer'),                         # 17x - "heifer"
    'cik': ('cik', 'fountain'),                         # 17x - "fountain"
    'neh': ('neh', 'sojourn'),                     # 17x - "sojourn"
    'mudahin': ('mu-dah-in', 'see.I-hate-ERG'),         # 17x - "hating/sent away"
    # sinsona: see line ~15277 (wrath - opaque lexeme, not sin-son-a)
    'encik': ('en-cik', 'look-fountain'),               # 17x - compound
    'lupkhop': ('lup-khop', 'bow.down-enough'),         # 17x - "bow down"
    'paikikin': ('pai-kik-in', 'go-again-ERG'),         # 17x - "going again"
    'milipin': ('mi-lip-in', 'person-crowd-ERG'),       # 17x - "multitude"
    'phawkna': ('phawk-na', 'remember-NMLZ'),           # 17x - "remembrance"
    'tuamcip': ('tuam-cip', 'promise-cover'),           # 17x - "covered over"
    # lamna: default to build-NMLZ (more common); dance contexts handled via compounds below
    'lamna': ('lam-na', 'build-NMLZ'),                  # 17x - "building" (default; dance: see explicit entries)
    # Explicit lamna disambiguation entries:
    # Dance contexts (Ex 32:19, Ps 30:11, Ps 150:4, Lk 15:25):
    'le lamna': ('le lam-na', 'and dance-NMLZ'),        # "and the dancing" (Ex 32:19, Ps 150:4)
    'taunate lamna': ('tauna-te lam-na', 'mourn-PL dance-NMLZ'),  # mourning → dancing (Ps 30:11)
    'lamna le lasakna': ('lam-na le lasak-na', 'dance-NMLZ and sing-NMLZ'),  # dancing and music (Lk 15:25)
    # Build contexts are the default - no need for explicit entries
    'bukkongah': ('buk-kong-ah', 'ambush-place-LOC'),   # 17x - "at ambush"
    'khenthei': ('khen-thei', 'divide-ABIL'),           # 17x - "able to divide"
    'nuamsa-in': ('nuam-sa-in', 'want-early-ERG'),      # 17x - "willingly"
    'hawlkhiatna': ('hawl-khiat-na', 'drive-out-NMLZ'), # 17x - "driving out"
    'kulhpite': ('kulh-pi-te', 'wall-big-PL'),          # 17x - "walls"
    'simgawp': ('sim-gawp', 'count-grasp'),             # 17x - "numbering"
    'thupizaw': ('thu-pi-zaw', 'word-big-more'),        # 17x - "greater word"
    'sumai': ('su-mai', 'money-face'),                  # 17x - compound
    'zongte': ('zong-te', 'search-PL'),                 # 17x - "searchers"
    'khenuai-ah': ('khe-nuai-ah', 'leg-under-LOC'),     # 17x - "under (feet)"
    'nihveina': ('nih-vei-na', 'two-time-NMLZ'),        # 17x - "second time"
    'thuakzawh': ('thuak-zawh', 'suffer-ABIL'),         # 17x - "able to suffer"
    'naseppih': ('nasep-pih', 'work-APPL'),        # 17x - "work with you"
    'thawhkikna': ('thawh-kik-na', 'rise-again-NMLZ'),  # 17x - "resurrection"
    # kikal: transparent analysis (overrides incorrect lexicon entry "gate")
    'kikal': ('ki-kal', 'REFL-middle'),                 # 70x - "between"
    'kikalah': ('ki-kal-ah', 'REFL-middle-LOC'),        # 119x - "between-LOC"
    'naihin': ('naih-in', 'near-ERG'),                  # 16x - "nearly"
    'sakhat': ('sak-hat', 'shaft-hard'),                # 16x - "candlestick shaft"
    'mizawngte\'': ('mi-zawng-te\'', 'person-poor-PL.POSS'), # 17x - "poor people's"
    'kaih': ('kaih', 'lead'),                      # 17x - "lead"
    'nawlah': ('nawl-ah', 'place-LOC'),                 # 17x - "at the place"
    
    # === Session 4 Round 11: More medium-frequency vocabulary ===
    'ngaihbaang': ('ngaih-baang', 'think-alike'),   # 16x - "fair/beautiful"
    'suakkhia': ('suak-khia', 'become-exit'),            # 16x - "came out"
    'nupite': ('nupi-te', 'woman-PL'),                   # 16x - "women"
    'hilhkhol': ('hilh-khol', 'teach-denounce'),         # 16x - "solemnly protest"
    'khoi': ('khoi', 'nurse'),                           # 16x - "nurse"
    'gimnate': ('gim-na-te', 'toil-NMLZ-PL'),            # 16x - "toils"
    'hanna': ('han-na', 'follow-NMLZ'),                  # 16x - "following"
    'kat': ('kat', 'catch'),                        # 16x - "catch fire"
    'banto': ('ban-to', 'side-sit'),                     # 16x - "middle"
    'sawpin': ('sawp-in', 'body-ERG'),                   # 16x - "carcase"
    'tuinak': ('tui-nak', 'water-time'),                 # 16x - "fountain"
    'khamul': ('kha-mul', 'spirit-shave'),               # 16x - "shave"
    'samsiat': ('sam-siat', 'call-destroy'),             # 16x - "cursed"
    'zatna': ('zat-na', 'hear.II-NMLZ'),                 # 16x - "spreading (plague)"
    'lamlahna': ('lam-lah-na', 'way-drop-NMLZ'),         # 16x - "trespass"
    'nulepa': ('nu-le-pa', 'mother-and-father'),         # 16x - "beast/parents"
    'ukte\'': ('uk-te\'', 'tent-PL.POSS'),               # 20x - "tents'"
    'nihte\'': ('nih-te\'', 'two-PL.POSS'),              # 21x - "two's"
    'tomno': ('tom-no', 'dwell-young'),                  # 17x - "dwelling"
    'mizawngte\'': ('mi-zawng-te\'', 'person-poor-PL.POSS'), # 17x - "poor people's"
    'suakta-in': ('suak-ta-in', 'become-stay-ERG'),      # 16x - "having become"
    'vaan': ('vaan', 'heaven'),                      # 16x - "heaven"
    'khamtheihzu': ('kham-theih-zu', 'forbid-ABIL-NEG'), # 16x - "cannot forbid"
    'tampite\'': ('tampi-te\'', 'many-PL.POSS'),         # 16x - "many people's"
    'genna-ah': ('gen-na-ah', 'speak-NMLZ-LOC'),         # 16x - "at speaking"
    'bulpite': ('bul-pi-te', 'base-big-PL'),             # 16x - "roots"
    'umcihin': ('um-cih-in', 'believe-say.NOM-ERG'),     # 16x - "believing"
    'vanah': ('van-ah', 'heaven-LOC'),                   # 16x - "in heaven"
    'honpa': ('hon-pa', 'flock-father'),                 # 16x - "shepherd"
    'gentheih': ('gen-theih', 'speak-ABIL'),             # 16x - "able to speak"
    'puanung': ('pua-nung', 'carry.back-back'),          # 16x - "carrying"
    
    # === Session 4 Round 12: More vocabulary ===
    'suangmanphate': ('suang-man-pha-te', 'stone-price-good-PL'), # 16x - "precious stones"
    'halna': ('hal-na', 'terror-NMLZ'),                  # 16x - "terror"
    'mihaute': ('mi-hau-te', 'person-rich-PL'),          # 16x - "rich people"
    'etteh': ('et-teh', 'care-measure'),                 # 16x - "sign/proverb"
    'cinate': ('cina-te', 'sick.person-PL'),             # 16x - patients (per dictionary)
    'puanpak': ('puan-pak', 'cloth-share'),              # 15x - "hangings"
    'khenkhia': ('khen-khia', 'divide-exit'),            # 15x - "divided"
    'gambup': ('gam-bup', 'land-whole'),                 # 15x - "whole land"
    'omlam': ('om-lam', 'exist-side'),                   # 15x - "eyes opened/state"
    'puansilh': ('puan-silh', 'cloth-wrap'),             # 15x - "naked/clothed"
    'zakua': ('za-kua', 'hundred-nine'),                 # 15x - "nine hundred"
    'tutphah': ('tut-phah', 'sleep-saddle'),             # 15x - "saddled"
    'khuang': ('khuang', 'drum'),                 # 15x - "tabret/feast"
    'ompihna': ('om-pih-na', 'exist-APPL-NMLZ'),         # 15x - "being with/prosper"
    'luite': ('lui-te', 'river-PL'),                     # 15x - "rivers"
    'keek': ('keek', 'fire'),                  # 15x - "fire/lightning"
    'zankim': ('zan-kim', 'night-half'),                 # 15x - "midnight"
    'sah': ('sah', 'witness'),                      # 15x - "witness heap"
    'gukte': ('guk-te', 'six-PL'),                       # 15x - "six"
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
    'dingkhia-in': ('ding-khia-in', 'stand-exit-ERG'),   # 15x - "standing up"
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
    'laksakin': ('lak-sak-in', 'take-CAUS-CVB'),         # 15x - "possessed"
    'nuaisiah': ('nuai-siah', 'under-subdue'),           # 15x - "subdued"
    'galsimna': ('gal-sim-na', 'enemy-count-NMLZ'),      # 15x - "battle"
    'awn': ('awn', 'void'),                              # 15x - "void/empty"
    'nungdelh': ('nung-delh', 'live-hide'),              # 15x - "hid"
    'simtham': ('sim-tham', 'count-molten'),             # 15x - "graven image"
    'gamtatsia': ('gamtat-sia', 'kingdom-bad'),          # 15x - "perverseness"
    'theigah': ('thei-gah', 'know.I-attach'),            # 15x - "trust"
    'vanmanpha': ('van-manpha', 'go.and-precious'),      # 15x - "treasures"
    'satgawp': ('sat-gawp', 'strike-grasp'),             # 15x - "blew"
    'thangpaihna': ('thang-paih-na', 'rise-pour-NMLZ'),  # 15x - "indignation"
    'tacilte': ('ta-cil-te', 'stay-first-PL'),           # 14x - "firstlings"
    'thumnate': ('thum-na-te', 'three-NMLZ-PL'),         # 14x - compound
    'nupa': ('nu-pa', 'female-male'),                     # 14x - "male and female pair" (Gen 7:2, Acts 5:1)
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
    'sinso': ('sinso', 'be.angry'),                      # 16x - "be angry/wrathful"
    'puakhia-in': ('puak-hia-in', 'send-away-ERG'),      # 14x - "sending"
    'suante\'': ('suan-te\'', 'lineage-PL.POSS'),        # 14x - "descendants'"
    'zaw-in': ('zaw-in', 'able-ERG'),                    # 14x - "being able"
    'siansuah': ('sian-suah', 'holy-redeem'),            # 14x - compound
    'paihkhiat': ('paih-khiat', 'go-depart'),            # 14x - "departed"
    'leengguite': ('leeng-gui-te', 'chariot-wheel-PL'),  # 14x - "chariots"
    'hatzaw': ('hat-zaw', 'strong-more'),                # 14x - "stronger"
    'tawmna': ('tawm-na', 'short-NMLZ'),                 # 14x - "shortness"
    'ankung': ('an-kung', '3PL-tree'),                   # 14x - "their tree"
    'lunggim': ('lung-gim', 'heart-round'),              # 14x - "whole heart"
    'kulhkongpite': ('kulh-kong-pi-te', 'wall-road-big-PL'), # 14x - "walls"
    'khathei': ('kha-thei', 'one-ABIL'),                 # 14x - "can one"
    'tauna': ('tau-na', 'store-NMLZ'),                   # 14x - "storing"
    'kahto-in': ('kah-to-in', 'climb-up-ERG'),           # 14x - phonotactic fix (no ht cluster)
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
    'hithei': ('hi-thei', 'be-ABIL'),                    # 14x - "can be"
    
    # === Session 4 Round 14: 13x frequency vocabulary ===
    'dawnte': ('dawn-te', 'receive-PL'),                 # 13x - "waters/months"
    'ciing': ('ciing', 'barren'),                        # 13x - "barren"
    'tengkhawm': ('teng-khawm', 'dwell-together'),       # 13x - "dwell together"
    'tuikuang': ('tui-kuang', 'water-trough'),           # 13x - "trough"
    'nihvei': ('nih-vei', 'two-time'),                   # 13x - "two times"
    'leengkhia': ('leeng-khia', 'chariot-exit'),         # 13x - "break/depart"
    'valhtum': ('valh-tum', 'go.and-swallow'),           # 13x - "devoured"
    'hehpihhuai': ('hehpih-huai', 'angry-dread'),        # 13x - "ill favoured"
    'gentel': ('gen-tel', 'speak-help'),                 # 13x - "told"
    'zatui': ('zatui', 'medicine'),                    # 13x - balm/medicine/healing substance
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
    'hilhkholhna': ('hilh-kholh-na', 'teach-INTENS-NMLZ'),  # 13x - "testimony"
    'kamsung': ('kam-sung', 'mouth-inside'),             # 13x - "in mouth"
    'kamciamna': ('kam-ciam-na', 'mouth-promise-NMLZ'),  # 13x - "oath"
    'sangzaw': ('sang-zaw', 'high-more'),                # 13x - "higher"
    'khuate-ah': ('khua-te-ah', 'town-PL-LOC'),          # 13x - "in towns"
    'thakte': ('thak-te', 'new-PL'),                     # 13x - "new ones"
    'innkhum': ('inn-khum', 'house-cover'),              # 13x - "house roof"
    'bawlnate': ('bawl-na-te', 'make-NMLZ-PL'),          # 13x - "works"
    'otna': ('ot-na', 'keep-NMLZ'),                      # 13x - "keeping"
    'awngin': ('awng-in', 'void-ERG'),                   # 13x - "empty"
    'luh': ('luh', 'enter'),                        # 13x - "head"
    'muangin': ('muang-in', 'trust-ERG'),                # 13x - "trusting"
    'daltuahte': ('dal-tuah-te', 'hinder-meet-PL'),      # 13x - "opponents"
    'omtheih': ('om-theih', 'exist-ABIL'),               # 13x - "able to exist"
    'siazaw': ('sia-zaw', 'bad-more'),                   # 13x - "worse"
    'theihtheih': ('theih~theih', 'know.II~REDUP'),    # 13x - "knowing"
    
    # === Session 4 Round 15: 12x frequency vocabulary ===
    'cil-in': ('cil-in', 'begin-ERG'),                   # 12x - "in beginning"
    'migi': ('mi-gi', 'person-evil'),                    # 12x - "wicked person"
    'paii': ('paii', 'sorrow'),                          # 12x - "sorrow"
    'piangkhia': ('piang-khia', 'be.born-exit'),         # 12x - "brought forth"
    'thunget': ('thu-nget', 'word-request'),             # 12x - "speaking/praying"
    'khiasuk': ('khia-suk', 'exit-DOWN'),                # 12x - "let down" (directional)
    'lungngaingai': ('lung-ngai-ngai', 'heart-think~think'), # 12x - "meditate"
    'matsa': ('mat-sa', 'grasp-meat'),                   # 12x - "venison"
    'bawngpi': ('bawng-pi', 'cattle-big'),               # 12x - "milch cow"
    'theihkholh': ('theih-kholh', 'know.II-INTENS'),       # 12x - "certainly/sore"
    'lunghihmawh': ('lung-hih-mawh', 'heart-do-sin'),    # 12x - "knew not"
    'kimuhna': ('ki-muh-na', 'REFL-see.II-NMLZ'),        # 12x - "found"
    'numeino': ('numei-no', 'woman-young'),              # 12x - "maid"
    'khuhcip': ('khuh-cip', 'cover-trap'),               # 12x - "entangled"
    'theihtel': ('theih-tel', 'know.II-help'),           # 12x - "understand"
    'khumcip': ('khum-cip', 'cover-push'),               # 12x - "push/horn"
    'thumang': ('thu-mang', 'word-obey'),                # 12x - "obey word/command" (KJV "hearkened")
    'kizopna': ('ki-zop-na', 'REFL-join-NMLZ'),          # 12x - "joining"
    'neikhawm': ('nei-khawm', 'have-together'),          # 12x - "keep together"
    'maimangsak': ('mai-mang-sak', 'face-chief-CAUS'),   # 12x - "destroy name"
    'diakdiakin': ('diak-diak-in', 'different~different-ERG'), # 12x - "secretly"
    'pahin': ('pa-hin', 'father-this'),                  # 12x - compound
    'itzaw': ('it-zaw', 'love-more'),                    # 12x - "love more"
    'kawi-in': ('kawi-in', 'forth-ERG'),                 # 12x - "going forth"
    'biakpiakna-in': ('biak-piak-na-in', 'worship-give.to-NMLZ-ERG'), # 12x - "worshipping"
    'khiam': ('khiam', 'narrow'),                        # 12x - "narrow/exit"
    'deihna-in': ('deih-na-in', 'want-NMLZ-ERG'),        # 12x - "wanting"
    'sunte': ('sun-te', 'long-PL'),                      # 12x - "long ones"
    'vengpa\'': ('veng-pa\'', 'guard-father.POSS'),      # 12x - "guardian's"
    'sahpi': ('sah-pi', 'witness-big'),                  # 12x - "great witness"
    'zalin': ('zal-in', 'spread-ERG'),                   # 12x - "spreading"
    'multe': ('mul-te', 'see.I-PL'),                     # 12x - "seers"
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
    'sikhawm': ('si-khawm', 'die-together'),             # 12x - "die together"
    'sawmthumte': ('sawm-thum-te', 'ten-three-PL'),      # 12x - "thirteens"
    'ngawn': ('ngawn', 'roar'),                          # 12x - "roar"
    'unok': ('u-nok', 'elder.sibling-younger'),          # 12x - "siblings"
    'sangpen': ('sang-pen', 'high-SUPER'),               # 12x - "highest"
    
    # === Session 4 Round 16: 11-12x frequency vocabulary ===
    'hunte-ah': ('hun-te-ah', 'time-PL-LOC'),            # 12x - "at times/unto"
    'kikupna': ('ki-kup-na', 'REFL-counsel-NMLZ'),       # 12x - "counsel"
    'sumbuk': ('sum-buk', 'money-bundle'),               # 12x - "silver"
    'kiniamkhiatna': ('ki-niam-khiat-na', 'REFL-humble-depart-NMLZ'), # 12x - "humbling"
    'khahsuah': ('khah-suah', 'choke-redeem'),           # 12x - "appointed"
    'lakkhiatsak': ('lak-khiat-sak', 'take-depart-CAUS'), # 12x - "took off"
    'uksak': ('uk-sak', 'rule-CAUS'),                    # 12x - "let down"
    'tausangte': ('tau-sang-te', 'store-high-PL'),       # 12x - "treasures"
    'nungngat': ('nung-ngat', 'live-sit'),               # 12x - "sat down"
    'annekna': ('an-nek-na', '3PL-eat.II-NMLZ'),         # 12x - "banquet"
    'zaizai': ('zai~zai', 'breadth~REDUP'),                  # 12x - "light/neesings"
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
    'omsuak': ('om-suak', 'exist-become'),               # 11x - "become"
    'bilvang': ('bil-vang', 'ear-strength'),             # 11x - "ear"
    'peekte': ('peek-te', 'measure-PL'),                 # 11x - "measures"
    'dialpi': ('dial-pi', 'call-big'),                   # 11x - "great call"
    'suangpeekte': ('suang-peek-te', 'stone-measure-PL'), # 11x - "stone measures"
    'maisakin': ('mai-sak-in', 'face-CAUS-CVB'),         # 11x - "facing"
    'sathaute': ('sat-hau-te', 'strike-rich-PL'),        # 11x - compound
    'biakna-a': ('biak-na-a', 'worship-NMLZ-LOC'),       # 11x - "at worship"
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
    'kahtohna': ('kah-toh-na', 'climb-up-NMLZ'),         # 11x - phonotactic fix (no ht cluster)
    'thatmang': ('that-mang', 'kill-chief'),             # 11x - "kill utterly"
    'delhna': ('delh-na', 'hide-NMLZ'),                  # 11x - "hiding"
    'kherub-te\'': ('kherub-te\'', 'cherub-PL.POSS'),    # 12x - "cherubim's"
    'paknamtuite': ('pak-nam-tui-te', 'share-nation-water-PL'), # 12x - compound
    'awte': ('aw-te', 'voice-PL'),                       # 12x - "voices"
    'hihtheih': ('hih-theih', 'do-ABIL'),                # 12x - "doable"
    
    # === Session 4 Round 17: 10x frequency vocabulary ===
    # 'tawlette': see line ~9286 (window-PL)
    'peuhmahte': ('peuh-mah-te', 'each-self-PL'),        # 10x - "whoso/everyone"
    'maingat': ('mai-ngat', 'face-sit'),                 # 10x - "shoulders"
    'sempa': ('sem-pa', 'serve-father'),                 # 10x - "servant"
    'lumlet': ('lum-let', 'warm-return'),                # 10x - "overthrow"
    'lumsuk': ('lum-suk', 'rest-DOWN'),                  # 10x - "lighted/tarried" (directional)
    'hanciamna': ('han-ciam-na', 'follow-promise-NMLZ'), # 10x - "wrestlings"
    'tuangsak': ('tuang-sak', 'ride-CAUS'),              # 10x - "set upon"
    'khiatsak': ('khiat-sak', 'depart-CAUS'),            # 10x - "cause to wander"
    'keusak': ('keu-sak', 'dig-CAUS'),                   # 10x - "blasted"
    'sial': ('sial', 'carcass'),                         # 10x - "carcass"
    'gammang': ('gam-mang', 'land-chief'),               # 10x - "astray"
    'gamtasak': ('gamta-sak', 'send.away-CAUS'),         # 10x - "cause to come"
    'siluang': ('si-luang', 'die-flow'),                 # 10x - "high places"
    'zahtakhuai': ('zahtak-huai', 'honor-dread'),        # 10x - "honourable"
    'satkham': ('sat-kham', 'strike-forbid'),            # 10x - "nigh"
    'tumna': ('tum-na', 'full-NMLZ'),                    # 10x - "mountain"
    'ensuk': ('en-suk', 'look-DOWN'),                    # 10x - "look down" (directional)
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
    'khawi': ('khawi', 'where'),                         # 10x - "where"
    'khen\'': ('khen\'', 'divide.POSS'),                 # 10x - "division"
    'hihin': ('hih-in', 'this-ERG'),                     # 10x - "this"
    'luahin': ('luah-in', 'head-ERG'),                   # 10x - "heading"
    'puanbukah': ('puan-buk-ah', 'cloth-cover-LOC'),     # 10x - "in tent"
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
    'nihun': ('ni-hun', 'day-time'),                     # 10x - "day time"
    'lungkhamin': ('lungkham-in', 'courage-ERG'),        # 10x - "encouraged"
    'siatnate': ('siat-na-te', 'spoil-NMLZ-PL'),         # 10x - "spoilings"
    'apsa': ('ap-sa', 'press-early'),                    # 10x - compound
    'neulai': ('neu-lai', 'small-middle'),               # 10x - compound
    'khempeuha': ('khem-peuh-a', 'restrain-all-LOC'),    # 10x - "all restrained"
    'kalhna': ('kalh-na', 'go-NMLZ'),                    # 10x - "going"
    'kigente': ('ki-gen-te', 'REFL-speak-PL'),           # 10x - "conversations"
    'khutnuai-a': ('khut-nuai-a', 'hand-under-LOC'),     # 10x - "under hand"
    'patau': ('pa-tau', 'father-store'),                 # 10x - compound
    'puakkhiat': ('puak-khiat', 'send-depart'),          # 10x - "send away"
    'namsau-in': ('nam-sau-in', 'nation-long-ERG'),      # 10x - compound
    'zahpih': ('zah-pih', 'fear-APPL'),                  # 10x - "fear with"
    'awgingte': ('awging-te', 'voice-PL'),               # 10x - "voices"
    
    # === Session 4 Round 18: Push to 97% ===
    # 'tawlette': see line ~9286
    'tute': ('tu-te', 'now-PL'),                         # 10x - compound
    'dangka': ('dang-ka', 'other-one'),                  # 10x - "parcel"
    'mualpang': ('mual-pang', 'hill-side'),              # 10x - "portion"
    'khen\'': ('khen\'', 'divide.POSS'),                 # 10x - "division"
    'nate\'': ('na-te\'', '2SG-PL.POSS'),                # 10x - "your (pl)"
    'lawn\'': ('lawn\'', 'easy.POSS'),                   # 10x - compound
    'komau\'': ('ko-mau\'', 'call-3PL.POSS'),            # 10x - "their calling"
    'mukha': ('mu-kha', 'see.I-place'),                  # 10x - compound
    'innliim': ('inn-liim', 'house-feast'),              # 10x - compound
    'sazian': ('sa-zian', 'meat-roast'),                 # 10x - compound
    'niliim': ('ni-liim', 'day-feast'),                  # 10x - compound
    'kiciang': ('ki-ciang', 'REFL-announce'),            # 10x - "announce self"
    'cihmawh': ('cih-mawh', 'say.NOM-sin'),              # 10x - "slander"
    'husan\'': ('husan\'', 'flood.POSS'),                # 10x - "flood's"
    'khauhin': ('khau-hin', 'spirit-this'),              # 10x - "this spirit"
    'hilhnate': ('hilh-na-te', 'teach-NMLZ-PL'),         # 10x - "teachings"
    'kisialhna': ('ki-sialh-na', 'REFL-sin-NMLZ'),       # 10x - "sinning"
    'cihmawhna': ('cih-mawh-na', 'say.NOM-sin-NMLZ'),    # 10x - "slander"
    'zuazua': ('zua~zua', 'prepare~REDUP'),            # 10x - "preparing"
    'semkhia': ('sem-khia', 'serve-exit'),               # 10x - "serve out"
    'innkiu': ('inn-kiu', 'house-corner'),               # 10x - "house corner"
    'piathuah': ('pia-thuah', 'give-put'),               # 10x - compound
    'mawhnopna': ('mawh-nop-na', 'sin-want-NMLZ'),       # 10x - "sin desire"
    'thatnuam': ('that-nuam', 'kill-want'),              # 10x - "want to kill"
    'uppih': ('u-pih', 'elder.sibling-APPL'),            # 10x - "with elder"
    'kawtsak': ('kawt-sak', 'garden-CAUS'),              # 9x - "water garden"
    'nuainung': ('nuai-nung', 'under-back'),             # 9x - compound
    'khukte': ('khuk-te', 'corner-PL'),                  # 9x - "corners"
    'laksa': ('lak-sa', 'take-early'),                   # 9x - "taken before"
    'hoihnono': ('hoih-no-no', 'good-young-young'),      # 9x - "very good"
    'sanin': ('san-in', 'high-ERG'),                     # 9x - "highly"
    'nauzaw': ('nau-zaw', 'child-more'),                 # 9x - "younger"
    'ngahsa': ('ngah-sa', 'get-early'),                  # 9x - "got before"
    'koihkhia': ('koih-khia', 'put-exit'),               # 9x - "put out"
    'bilbahte': ('bil-bah-te', 'earring-PL'),            # 9x - "earrings" (NOT deaf!)
    'inncing': ('inn-cing', 'house-clean'),              # 9x - "clean house"
    'zungbuh': ('zungbuh', 'ring'),                      # 9x - signet ring (opaque lexeme)
    'antang': ('an-tang', '3PL-force'),                  # 9x - "their force"
    'piazaw': ('pia-zaw', 'give-more'),                  # 9x - "give more"
    'milip': ('mi-lip', 'person-crowd'),                 # 9x - "multitude"
    
    # === Session 4 Round 19: Final push to 97% ===
    'kilatna': ('ki-lat-na', 'REFL-strong-NMLZ'),        # 9x - "strengthening"
    'vatgawpin': ('vat-gawp-in', 'go.quickly-grasp-ERG'), # 9x - "quickly grasp"
    'lohte': ('loh-te', 'field-PL'),                     # 9x - "fields"
    'gin\'': ('gin\'', 'gong.POSS'),                     # 9x - "gong's"
    'cinatna': ('ci-nat-na', 'say-sick-NMLZ'),           # 9x - compound
    'keelmul': ('keelmul', 'goathair'),                  # 9x - goat's hair (opaque lexeme)
    'nawlnung': ('nawl-nung', 'place-back'),             # 9x - "back place"
    'siampipuan\'': ('siampi-puan\'', 'priest-cloth.POSS'), # 9x - "priest's robe"
    'kibulh': ('ki-bulh', 'REFL-root'),                  # 9x - "rooted"
    'kisan\'': ('ki-san\'', 'REFL-high.POSS'),           # 9x - compound
    'silhsakin': ('silh-sak-in', 'clothe-CAUS-CVB'),     # 9x - "clothing"
    'khim': ('khim', 'edge'),                            # 9x - "edge"
    'puankhai': ('puan-khai', 'cloth-lift'),             # 9x - "lift cloth"
    'bukkong': ('buk-kong', 'ambush-road'),              # 9x - "ambush place"
    'nai-a': ('nai-a', 'near-LOC'),                      # 9x - "nearby"
    'siansuahna': ('sian-suah-na', 'holy-redeem-NMLZ'),  # 9x - "redemption"
    'kihhuaina': ('ki-hhuai-na', 'REFL-dread-NMLZ'),     # 9x - "dread"
    'poina': ('poi-na', 'feast-NMLZ'),                   # 9x - "feast"
    'kisehte': ('ki-seh-te', 'REFL-slice-PL'),           # 9x - compound
    'thute-ah': ('thu-te-ah', 'word-PL-LOC'),            # 9x - "in words"
    'cilna': ('cil-na', 'begin-NMLZ'),                   # 9x - "beginning"
    'anlim': ('an-lim', '3PL-feast'),                    # 9x - "their feast"
    'kawmah': ('kawm-ah', 'beam-LOC'),                   # 9x - "at beam"
    'tuahkhak': ('tuah-khak', 'meet-give.command'),      # 9x - compound
    'pammaih': ('pam-maih', 'all-face'),                 # 9x - compound
    'phuh': ('phuh', 'blow'),                            # 9x - "blow"
    'buakhia': ('buak-hia', 'fight-away'),               # 9x - "fight away"
    'sanang': ('sa-nang', 'meat-2SG'),                   # 9x - compound
    'saupi': ('sau-pi', 'long-big'),                     # 9x - "very long"
    'aisante': ('ai-san-te', '3SG-high-PL'),             # 9x - compound
    'sihsak': ('sih-sak', 'die-CAUS'),                   # 9x - "cause to die"
    'sukgawp': ('suk-gawp', 'DOWN-grasp'),               # 9x - "push down and grasp"
    'paipihsuk': ('pai-pih-suk', 'go-APPL-DOWN'),       # 9x - "go down (for someone)"
    'innkhumzang': ('inn-khum-zang', 'house-cover-use'), # 9x - compound
    'gamtatsiat': ('gamtat-siat', 'kingdom-destroy'),    # 9x - "destroy kingdom"
    'kitangsapna': ('ki-tang-sap-na', 'REFL-force-call-NMLZ'), # 9x - compound
    'omkhak': ('om-khak', 'exist-command'),              # 9x - compound
    'lakkhia': ('lak-khia', 'take-exit'),                # 9x - "take out"
    'ukpa\'': ('uk-pa\'', 'rule-father.POSS'),           # 9x - "ruler's"
    'genkhiat': ('gen-khiat', 'speak-depart'),           # 9x - "speak and depart"
    'lungmang': ('lung-mang', 'heart-forget'),           # 9x - "forget heart"
    'suaksakin': ('suak-sak-in', 'become-CAUS-CVB'),     # 9x - "causing to become"
    'lutsak': ('lut-sak', 'enter-CAUS'),                 # 9x - "cause to enter"
    'vatin': ('vat-in', 'go.quickly-ERG'),               # 9x - "going quickly"
    'diktat': ('dik-tat', 'righteous-strike'),           # 9x - compound
    'samkhia': ('sam-khia', 'call-exit'),                # 9x - "call out"
    'munmuanhuaite': ('mun-muan-huai-te', 'place-trust-dread-PL'), # 9x - compound
    'omlaiteng': ('om-lai-teng', 'exist-middle-all'),    # 9x - "exist among all"
    'sukkhak': ('suk-khak', 'DOWN-restrain'),            # 9x - "push down"
    
    # === Session 4 Round 20: Push clearly over 97% ===
    'hehnepna': ('heh-nep-na', 'angry-soft-NMLZ'),       # 9x - "wrath"
    'kimangngilh': ('ki-mang-ngilh', 'REFL-chief-forget'), # 9x - "forgetting"
    'tuili': ('tui-li', 'water-flow'),                   # 9x - "water flow"
    'zuautat': ('zuau-tat', 'prepare-strike'),           # 9x - compound
    'gin\'': ('gin\'', 'gong.POSS'),                     # 9x - "gong's"
    'taitehte': ('tai-teh-te', 'cut-measure-PL'),        # 9x - compound
    'siampipuan\'': ('siampi-puan\'', 'priest-cloth.POSS'), # 9x - "priest's robe"
    'kisan\'': ('ki-san\'', 'REFL-high.POSS'),           # 9x - compound
    'kipsakna': ('kip-sak-na', 'firm-CAUS-NMLZ'),        # 9x - "confirmation" (phonotactic: no ps cluster)
    'phulakna': ('phu-lak-na', 'carry-take-NMLZ'),       # 9x - compound
    'vah': ('vah', 'go.quickly'),                        # 9x - "go quickly"
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
    'tuiciin': ('tui-ciin', 'water-pure'),               # 14x - "pure water"
    'naupaii': ('nau-paii', 'child-row'),                # 14x - "children in rows"
    'vanging': ('vang-ing', 'strength-INS'),             # 14x - "by strength"
    'galhiamte': ('gal-hiam-te', 'enemy-fierce-PL'),     # 14x - "fierce enemies"
    'inndeite': ('inn-dei-te', 'house-good-PL'),         # 14x - "household"
    'teembawte': ('teem-baw-te', 'tent-build-PL'),       # 13x - "tents"
    'siksanin': ('sik-san-in', 'repent-high-ERG'),       # 13x - "repenting"
    'cikin': ('ci-kin', 'say-half'),                     # 13x - "saying"
    'laithei': ('lai-thei', 'middle-know'),              # 13x - "palm of hand"
    'siapa': ('sia-pa', 'evil-man'),                   # 13x - "elder"
    'genkhit': ('gen-khit', 'speak-end'),                # 13x - "finished speaking"
    'deihzaw': ('deih-zaw', 'want-more'),                # 13x - "desire more"
    'uiphukte': ('ui-phuk-te', 'dog-wild-PL'),           # 12x - "wild dogs"
    'satnen': ('sat-nen', 'strike-swallow'),             # 12x - "smote, struck"
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
    'kisutin': ('ki-sut-in', 'REFL-spoil-CVB'),          # derived
    
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
    'dawh': ('dawh', 'beautiful'),                       # 8x - "beautiful"
    'sulzuih': ('sul-zuih', 'track-follow'),             # 8x - "follow"
    'hel': ('hel', 'hell'),                              # 8x - "hell" (loanword)
    'galbawl': ('gal-bawl', 'enemy-make'),               # 8x - "make war"
    'golpi': ('gol-pi', 'creature-great'),                    # 8x - "great bowl"
    'gilvah': ('gil-vah', 'belly-go'),                   # 8x - "with child"
    'daupai': ('dau-pai', 'war-pour'),                   # 8x - "battle"
    'ngong': ('ngong', 'stub'),                          # 8x - "stub"
    'kuankhiat': ('kuan-khiat', 'trough-depart'),        # 8x - compound
    'ngia': ('ngia', 'watch'),                           # 8x - "watch"
    'pom': ('pom', 'embrace'),                           # 8x - "embrace"
    'dimdiam': ('dim~diam', 'still~REDUP'),              # 8x - "very still"
    'phuahtawm': ('phuah-tawm', 'compose-together'),     # 8x - "compose"
    'pholak': ('pho-lak', 'uncover-take'),               # 8x - "reveal"
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
    'neihtheih': ('neih-theih', 'have.II-ABIL.II'),       # 11x - "be able to have"
    'biakinn-a': ('biak-inn-a', 'pray-house-LOC'),        # 15x - "in the temple"
    
    # More ki- verbs (philologically verified)
    'kiak': ('ki-ak', 'REFL-exalt'),                      # 8x - "be exalted" (JOB 24:24)
    'kitamzan': ('ki-tam-zan', 'REFL-many-break'),        # 8x - "broken, contrite" (PSA 51:17)
    'kisaktheih': ('ki-sak-theih', 'REFL-CAUS-ABIL'),     # 8x - "boast, glorify self"
    'kithokiksak': ('ki-thok-ik-sak', 'REFL-rise-ITER-CAUS'), # 8x - "be raised/resurrected"
    'kiphel': ('ki-phel', 'REFL-clear'),                  # 7x - "clear oneself, justify"
    'hemkhia': ('hem-khia', 'remove-exit'),               # 7x - "put away, remove"
    'meengkhia': ('meeng-khia', 'branch-exit'),           # 7x - "branch out"
    
    # More remaining unknowns
    'dimtakin': ('dim-tak-in', 'still-true-ERG'),         # 8x - "very still/quietly"
    'dahhuai': ('dah-huai', 'put-dread'),                 # 8x - "terrible"
    'phukham': ('phu-kham', 'carry-hold'),                # 7x - "bear/carry"
    'mak': ('mak', 'mark'),                               # 7x - "mark" (loanword?)
    'giah': ('giah', 'camp'),                             # 7x - "camp"
    'taikhiat': ('tai-khiat', 'flee-depart'),             # 7x - "flee away"
    'than': ('than', 'charcoal'),                         # 7x - "charcoal/coal"
    'leinuai-a': ('lei-nuai-a', 'earth-below-LOC'),       # 7x - "under the earth"
    'lahtel': ('lah-tel', 'take-spread'),                 # 7x - compound
    'kuumpi': ('kuum-pi', 'bow-big'),                     # 7x - "great bow"
    'kop': ('kop', 'pair'),                               # 7x - classifier for pairs (Gen 7:2 "seven pairs")
    'kialo': ('ki-alo', 'REFL-fall'),                     # 5x - "fall" (1 Sam 14:45 "shall not fall")
    'tungnungte': ('tung-nung-te', 'upper-back-PL'),      # 5x - "upper springs/chambers" (Josh 15:19)
    'ate': ('a-te', 'NOM-PL'),                            # 3x - "those" (nominalizer + plural)
    'nasiat': ('nasiat', 'severe.II'),                    # 2x - "severe/great" (Stem II of nasia)
    'huate': ('hua-te', 'these-PL'),                      # 2x - "these/them" (Ezek 8:17, Mark 14:70)
    'tunpihsuk': ('tun-pih-suk', 'arrive-APPL-DOWN'),     # 1x - "bring down" (Deut 1:25)
    'tunpite': ('tunpi-te', 'hornet-PL'),                 # 1x - "hornets" (Josh 24:12)
    'meette': ('meet-te', 'shearer-PL'),                  # 1x - "shearers" (1 Sam 25:11)
    'halte': ('hal-te', 'burn-PL'),                       # 1x - "those who burned" (2 Ki 23:5)
    
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
    'vankhainate': ('van-khai-na-te', 'sky-open-NMLZ-PL'), # 11x - "heavenly things"
    'nasemnu\u2019': ('na-sem-nu\u2019', '2SG-serve-mother.POSS'), # 11x
    "nasemnu'": ('na-sem-nu\u2019', '2SG-serve-mother.POSS'),
    'ma-un': ('ma-un', 'that-time'),                      # 13x - "at that time"
    '-a\u2019': ('-a\u2019', '3SG.POSS'),                  # 12x - possessive clitic
    "-a'": ('-a\u2019', '3SG.POSS'),                      # alias
    
    # Bug fixes: prevent over-decomposition of nam-, kai- etc.
    'namte': ('nam-te', 'tribe-PL'),                      # NOT na-m-te!
    'namza': ('nam-za', 'tribe-fear'),                    # NOT na-mza! = "nation"
    'kaina': ('kai-na', 'ascend-NMLZ'),                   # NOT ka-i-na! = "ascent"
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
    'munkip': ('mun-kip', 'place-near'),                  # 10x - "nearby place"
    'lohnate': ('loh-na-te', 'able.NEG-NMLZ-PL'),         # 10x - "impossibilities"
    'maangmuhnate': ('maang-muh-na-te', 'vision-see.II-NMLZ-PL'), # 10x
    'naupangnote': ('nau-pang-no-te', 'child-side-young-PL'), # 10x
    'siahdongte': ('siah-dong-te', 'judge-until-PL'),     # 10x - compound
    # 'tawlette': see line ~9286
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
    'lamdung': ('lam-dung', 'way-straight'),              # 7x - "straight way"
    'koimahah': ('koi-mah-ah', 'which-self-LOC'),         # 7x - "whichever place"
    'dawk': ('dawk', 'open'),                             # 7x - "open"
    'themno': ('them-no', 'one-young'),                   # 7x - "young one"
    'thangling': ('thang-ling', 'rise-expect'),           # 7x - "hope"
    'dau': ('dau', 'war'),                                # 7x - "war"
    'sungtumin': ('sung-tum-in', 'inside-all-ERG'),       # 7x - "inside all"
    'guahpi': ('guah-pi', 'bowl-big'),                    # 7x - "great bowl"
    'manmanin': ('man-man-in', 'price~REDUP-ERG'),          # 7x - "pricing"
    'lawp': ('lawp', 'lap'),                              # 7x - "lap"
    'dip': ('dip', 'valley'),                             # 7x - "valley"
    'mahun': ('ma-hun', 'that-time'),                     # 7x - "at that time"
    
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
    'piathei': ('pia-thei', 'give-ABIL'),                 # 11x - "able to give"
    'tangthu': ('tang-thu', 'generation-word'),           # 10x - "old word, tradition"
    'khualna-in': ('khual-na-in', 'sojourn-NMLZ-ERG'),    # 10x - "sojourning"
    'hanthotna': ('han-thot-na', 'follow-tie-NMLZ'),      # 10x - compound
    'gamlum': ('gam-lum', 'land-round'),                  # 9x - "whole land"
    'saiha': ('sai-ha', 'flesh-tooth'),                   # 9x - "ivory"
    'zangsak': ('zang-sak', 'use-CAUS'),                  # 9x - "cause to use"
    'liailiai': ('liai~liai', 'go.around~REDUP'),           # 9x - "go around repeatedly"
    
    # More high-frequency fixes
    'ak': ('ak', 'then'),                        # 13x - discourse particle
    'pukna': ('puk-na', 'cave-NMLZ'),                     # 11x - "cave dwelling"
    'khawk': ('khawk', 'hollow'),                   # 11x - "hollow"
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
    # 'tawlette': see line ~9286
    'siampipuan\u2019': ('siampi-puan\u2019', 'priest-cloth.POSS'), # 9x
    "siampipuan'": ('siampi-puan\u2019', 'priest-cloth.POSS'),
    'ukpa\u2019': ('uk-pa\u2019', 'rule-father.POSS'),    # 9x
    "ukpa'": ('uk-pa\u2019', 'rule-father.POSS'),
    'patna': ('pat-na', 'begin-NMLZ'),                    # 9x - "beginning, first (deed)"
    'cina-in': ('ci-na-in', 'say-NMLZ-ERG'),              # 9x - "saying"
    'ziate': ('zia-te', 'manner-PL'),                  # 9x - "his wives"
    
    # Session 6 Round 1: Philologically verified (97.31%)
    'ki-em': ('ki-em', 'PASS-bake'),                       # 11x - "be baked" (Lev)
    'tawlette': ('tawle-te', 'window-PL'),                 # 9x - "windows"
    'kikholhpihte': ('ki-kholh-pih-te', 'REFL-accompany-CAUS-PL'),  # 9x - "companions"
    'paihkhiatsak': ('paih-khiat-sak', 'go-depart-APPL'),  # 9x - "take away"
    'mialsak': ('mial-sak', 'darkness-CAUS'),              # 9x - "darken, cover"
    'ento': ('en-to', 'look-toward'),                      # 9x - "look up at"
    'lingkung': ('lingkung', 'thorns'),                    # 9x - thorns/briers (opaque lexeme)
    'sikkawi': ('sik-kawi', 'hook-fish'),                  # 9x - "fishhook"
    'piakkhong': ('piak-khong', 'give-NOM'),               # 9x - "gift"
    'ngahzawh': ('ngah-zawh', 'get-COMPL'),                # 9x - "obtain, get fully"
    'awksak': ('awk-sak', 'for-CAUS'),                     # 9x - "cause for" 
    'thumante': ('thu-man-te', 'word-true-PL'),            # 9x - "true words"
    'kampi': ('kam-pi', 'word-big'),                       # 9x - "great word"
    'ngente': ('ngen-te', 'pray-PL'),                      # 9x - compound
    'ututin': ('u-tu-tin', 'want-FUT-PROG'),               # 9x - "wanting, willing"
    'nuntakna-ah': ('nun-tak-na-ah', 'life-true-NMLZ-LOC'), # 9x - "in life"
    'zattheih': ('zat-theih', 'hear-ABIL'),                 # 9x - "can hear"
    'ukzawh': ('uk-zawh', 'rule-COMPL'),                   # 9x - "rule completely"
    'omngei': ('om-ngei', 'be-know'),                      # 9x - "be known"
    'baihzaw': ('baih-zaw', 'owe-more'),                   # 9x - "owe more"
    'lungdamhuai': ('lung-dam-huai', 'heart-heal-fear'),   # 9x - "rejoice greatly"
    'kineihkhemte': ('ki-neih-khem-te', 'REFL-have-all-PL'), # 9x - "possessions"
    'septheih': ('sep-theih', 'work-ABIL'),                 # 9x - "can work"
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
    'suksak': ('suk-sak', 'push.down-CAUS'),               # 8x - "push down and cause"
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
    'paipai': ('pai~pai', 'go~REDUP'),                     # 8x - "go repeatedly"
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
    'siamnate': ('siam-na-te', 'skilled-NMLZ-PL'),         # 8x - "skillful works"
    'santheih': ('san-theih', 'salt-ABIL'),                 # 8x - "salted" (Mark 9:49)
    'lutpih': ('lut-pih', 'enter-CAUS'),                   # 8x - "bring in"
    'pahtawi-in': ('pah-tawi-in', 'honor-carry-ERG'),     # 8x - "patriarch" (from htawi elder)
    'cimawhte\u2019': ('ci-mawh-te\u2019', 'say-sin-PL.POSS'), # 8x 
    "cimawhte'": ('ci-mawh-te\u2019', 'say-sin-PL.POSS'),
    'pannate': ('panna-te', 'petition-PL'),                # 8x - "petitions"
    'gennate': ('gen-na-te', 'speak-NMLZ-PL'),             # 8x - "sayings"
    'vawhpa': ('vawh-pa', 'go.and-male'),                  # 8x - compound
    'kongpite-ah': ('kong-pi-te-ah', '1SG→3-big-PL-LOC'),  # 8x - compound
    
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
    'kivuina': ('ki-vui-na', 'REFL-bury-NMLZ'),            # 6x - "burying place"
    'neite\u2019': ('nei-te\u2019', 'have-PL.POSS'),       # 6x
    "neite'": ('nei-te\u2019', 'have-PL.POSS'),
    'tumte': ('tum-te', 'will-PL'),                        # 6x - compound
    'pualama': ('pualam-a', 'outside-LOC'),                # 6x - "outside"
    'omnasa': ('om-na-sa', 'be-NMLZ-animal'),              # 6x - compound
    'hut': ('hut', 'shelter'),                             # 6x - "shelter, booth"
    'bangci-a': ('bang-ci-a', 'what-say-Q'),               # 6x - "what manner"
    'kapkhia': ('kap-khia', 'weep-out'),                   # 6x - phonotactic fix (no pk cluster)
    'zawl-ai': ('zawl-ai', 'valley-LOC'),                  # 6x - "in the valley"
    'thalawhsa': ('tha-lawh-sa', 'breath-reap-animal'),    # 6x - compound
    'zawte': ('zawh-te', 'finish-PL'),                     # 6x - "those who finished"
    'huk': ('huk', 'bark'),                                # 6x - "bark" (of tree)
    'samsakin': ('sam-sak-in', 'call-CAUS-CVB'),           # 6x - "causing to call"
    'damdamin': ('dam-dam-in', 'well~REDUP-ERG'),          # 6x - "well, safely"
    'kawngah': ('kawng-ah', 'road-LOC'),                   # 6x - "on the road"
    'piapi': ('pia-pi', 'give-big'),                       # 6x - "give greatly"
    'ginat': ('gi-nat', 'stomach-tight'),                  # 6x - "courageous"
    'paipihsak': ('pai-pih-sak', 'go-CAUS-APPL'),          # 6x - "cause to accompany"
    
    # Session 6 Round 7: More philological additions (freq 8)
    'hutna': ('hut-na', 'shelter-NMLZ'),                   # 8x - "shelter, refuge"
    'puang': ('puang', 'speckled'),                        # 8x - "speckled, spotted"
    'letsongin': ('let-song-in', 'return-send-ERG'),       # 8x - "as a present"
    'hoihlamin': ('hoih-lam-in', 'good-manner-ERG'),       # 8x - "peacefully"
    'kinuh': ('ki-nuh', 'REFL-anoint'),                    # 8x - "be anointed"
    'hingte\u2019': ('hing-te\u2019', 'live-PL.POSS'),     # 8x - "living creatures'"
    "hingte'": ('hing-te\u2019', 'live-PL.POSS'),
    'luangsuk': ('luang-suk', 'flow-grind'),               # 8x - "grind fine"
    'singniim': ('sing-niim', 'tree-shade'),               # 8x - "grove"
    'genpih': ('gen-pih', 'speak-APPL'),                   # 8x - "speak unto"
    'dona': ('do-na', 'fight-NMLZ'),                       # 8x - "war, fighting"
    'damkikzo': ('dam-kik-zo', 'well-ITER-can'),           # 8x - "recover"
    'singluang': ('singluang', 'beam'),                    # 8x - wooden beam (partial opacity)
    'kiciamtehna': ('ki-ciam-teh-na', 'REFL-oath-mark-NMLZ'), # 8x - "enrollment"
    'milipun': ('mi-lipun', 'person-bundle'),              # 8x - "bundle"
    'atna': ('at-na', 'cut-NMLZ'),                         # 8x - "cutting"
    'khetphimte': ('khet-phim-te', 'judge-try-PL'),        # 8x - "trials"
    'zepna': ('zep-na', 'press-NMLZ'),                     # 8x - "oppression"
    'lungduai-in': ('lung-duai-in', 'heart-doubt-ERG'),    # 8x - "doubting"
    'koihsa': ('koih-sa', 'put-already'),                  # 8x - "already placed"
    'khangkhangin': ('khang-khang-in', 'generation~REDUP-ERG'), # 8x - "from generation"
    'kantel': ('kan-tel', '1SG→3-spread'),                 # 8x - compound
    'liangko-ah': ('liang-ko-ah', 'shoulder-both-LOC'),    # 8x - on both shoulders
    'hinglai': ('hing-lai', 'live-time'),                  # 8x - "lifetime"
    'sausak': ('sau-sak', 'long-CAUS'),                    # 8x - "lengthen"
    'vuite': ('vui-te', 'bury-PL'),                        # 8x - compound
    'luahte': ('luah-te', 'flow-PL'),                      # 8x - compound
    'nungakna': ('nungak-na', 'maiden-NMLZ'),              # 8x - "virginity"
    'hihnate': ('hih-na-te', 'do-NMLZ-PL'),                # 8x - "doings"
    'lunghimawhin': ('lung-himawh-in', 'heart-doubt-ERG'), # 8x - "anxiously"
    'bawh': ('bawh', 'rub'),                               # 8x - "rub"
    'kicihna': ('ki-cih-na', 'REFL-say-NMLZ'),             # 8x - "being called"
    'sawmsagihte': ('sawm-sagih-te', 'ten-seven-PL'),      # 8x - "seventies"
    'nun\u2019': ('nun\u2019', 'life.POSS'),               # 8x - "life's"
    "nun'": ('nun\u2019', 'life.POSS'),
    'muanhuai-in': ('muan-huai-in', 'trust-fear-ERG'),     # 8x - "trustingly"
    'kihuh': ('ki-huh', 'REFL-push'),                      # 8x - compound
    'thongkiatna': ('thong-kiat-na', 'prison-release-NMLZ'), # 8x - "release from prison"
    
    # Session 6 Round 8: More philological additions (freq 8)
    'innluahza': ('inn-luah-za', 'house-inherit-right'),   # 8x - "birthright"
    'tuibuah': ('tui-buah', 'water-pour'),                 # 8x - "drink offering"
    'hehluatna': ('heh-luat-na', 'anger-exceed-NMLZ'),     # 8x - "fierceness"
    'singhiang': ('sing-hiang', 'tree-branch'),            # 8x - "branches"
    'tuihual': ('tui-hual', 'water-wave'),                 # 8x - "waves, unstable"
    'nono': ('no~no', 'young~REDUP'),                      # 8x - "small, village"
    'paupau': ('pau~pau', 'speak~REDUP'),                  # 8x - "speak repeatedly"
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
    'puanmongteep': ('puan-mong-teep', 'cloth-cover-fringe'), # 8x - "fringes"
    'tuutalte': ('tuutal-te', 'ram-PL'),                   # 8x - "rams"
    'puanza': ('puan-za', 'cloth-garment'),                # 8x - "vesture, garment"
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
    'innkuansung': ('inn-kuan-sung', 'house-family-inside'), # 7x - "household"
    'satlum': ('sat-lum', 'cut-round'),                    # 7x - "kill, slay"
    'minsiasak': ('min-sia-sak', 'name-bad-CAUS'),         # 7x - "blaspheme"
    
    # Session 6 Round 10: More philological additions (freq 7-8)
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
    'luat': ('luat', 'exceed'),                            # 7x - "excess, over"
    'phalvak': ('phal-vak', 'permit-quick'),               # 7x - compound
    'ciahsuk': ('ciah-suk', 'return-down'),                # 7x - "return down"
    'hihgawp': ('hih-gawp', 'do-round'),                   # 7x - compound
    'paukhia': ('pau-khia', 'speak-emerge'),               # 7x - "speak out"
    'kuangkhia': ('kuang-khia', 'box-emerge'),             # 7x - compound
    'nungkiksak': ('nung-kik-sak', 'live-ITER-CAUS'),      # 7x - "revive"
    'kolte': ('kol-te', 'wheel-PL'),                       # 7x - "wheels"
    'sahna': ('sah-na', 'grind-NMLZ'),                     # 7x - "grinding"
    'innkuankuanin': ('inn-kuan-kuan-in', 'house-family~REDUP-ERG'), # 7x - compound
    'apna': ('ap-na', 'cover-NMLZ'),                       # 7x - "covering"
    'nawksak': ('nawk-sak', 'again-CAUS'),                 # 7x - compound
    
    # Session 6 Round 11: Allomorph audit fixes - prevent over-segmentation
    # These are nouns/verbs that were being incorrectly split
    'hingte': ('hing-te', 'alive-PL'),                     # 14x - "living creatures"
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
    'sawmngate': ('sawmnga-te', 'fifty-PL'),               # 7x - compound
    'pawite': ('pawi-te', 'feast-PL'),                     # 12x - "feasts/offerings"
    
    # Session 6 Round 12: More over-segmentation fixes from allomorph audit
    'innsate': ('innsa-te', 'cattle-PL'),                  # cattle (NOT i-nnsa-te)
    'innsa': ('innsa', 'cattle'),                          # base - cattle/domestic animals
    'gamsate': ('gamsa-te', 'beast-PL'),                   # beasts/wild animals
    'thukte': ('thuk-te', 'deep-PL'),                      # depths (NOT thu-k-te)
    'kangte': ('kang-te', 'gray-PL'),                      # gray/white ones (hair)
    'keelpite': ('keelpi-te', 'she.goat-PL'),              # she-goats (NOT keel-pi-te)
    'keelpi': ('keelpi', 'she.goat'),                      # base - female goat
    'bawngpite': ('bawngpi-te', 'cattle.big-PL'),          # large cattle/kine
    'tuilite': ('tuili-te', 'stream-PL'),                  # streams/ponds
    'dalnate': ('dalna-te', 'hindrance-PL'),               # hindrances (dal-na-te correct)
    'dalna': ('dalna', 'hindrance'),                       # base - hindrance
    'suknate': ('sukna-te', 'becoming-PL'),                # becomings (suk-na-te correct)
    'sukna': ('sukna', 'becoming'),                        # base - process of becoming
    'cilte': ('cil-te', 'beginning-PL'),                   # beginnings
    'cil': ('cil', 'beginning'),                           # base - beginning (NOT ci-l)
    'kikoihte': ('kikoih-te', 'foundation-PL'),            # foundations
    'theihnate': ('theihna-te', 'knowledge-PL'),           # knowledges
    
    # Session 6 Round 13: More over-segmentation fixes
    'nunte': ('nun-te', 'knop-PL'),                        # knobs/knops (NOT nu-n-te)
    'kalte': ('kal-te', 'kidney-PL'),                      # kidneys (NOT ka-l-te)
    'pangte': ('pang-te', 'branch-PL'),                    # branches
    'gamgite': ('gamgi-te', 'border-PL'),                  # borders/bounds
    
    # Session 6 Round 14: More over-segmentation fixes
    'sante': ('san-te', 'garlic-PL'),                      # garlick (NOT sa-n-te)
    'zinte': ('zin-te', 'travel-PL'),                   # strangers (NOT zi-n-te)
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
    
    # Session 6 Round 15: More over-segmentation fixes
    'kamte': ('kam-te', 'word-PL'),                        # words/speeches (NOT ka-m-te)
    'bengte': ('beng-te', 'companion-PL'),                 # companions/fishers
    'beng': ('beng', 'companion'),                         # base - companion/fisher
    'zungte': ('zung-te', 'root-PL'),                      # roots (of plants)
    'zung': ('zung', 'root'),                              # base - root
    'muangte': ('muang-te', 'trust-PL'),                   # those who trust  
    'buluhte': ('buluh-te', 'troop-PL'),                   # troops/robbers
    'buluh': ('buluh', 'troop'),                           # base - troop/band
    'kuamte': ('kuam-te', 'plain-PL'),                     # plains/valleys
    'kuam': ('kuam', 'plain'),                             # base - plain/valley
    'huhte': ('huh-te', 'help-PL'),                        # helpers
    'huh': ('huh', 'help'),                                # base - help
    
    # Session 6 Round 16: More over-segmentation fixes  
    'taktakte': ('taktak-te', 'genuine-PL'),               # genuine/true ones
    'taktak': ('tak~tak', 'great~REDUP'),                       # base - truly/genuine
    'ganhonte': ('ganhon-te', 'flock-PL'),                 # flocks/herds
    'ganhon': ('ganhon', 'flock'),                         # base - flock/herd
    'khedapte': ('khedap-te', 'shoe-PL'),                  # shoes/sandals
    'khedap': ('khedap', 'shoe'),                          # base - shoe/sandal
    'tawmte': ('tawm-te', 'produce-PL'),                   # produce/growth
    'tawm': ('tawm', 'produce'),                           # base - produce
    'ngimnate': ('ngimna-te', 'imagination-PL'),           # imaginations/thoughts
    'mukte': ('muk-te', 'lip-PL'),                         # lips (NOT mu-k-te)
    
    # Session 6 Round 17: More over-segmentation fixes
    'kawbiate': ('kawbia-te', 'shovel-PL'),                # shovels/basins (NOT ka-wbia-te)
    'kawbia': ('kawbia', 'shovel'),                        # base - shovel/basin
    'ngaknate': ('ngakna-te', 'base-PL'),                  # bases/feet (of laver)
    'ngakna': ('ngakna', 'base'),                          # base - foot/base/stand
    'nengniamte': ('nengniam-te', 'oppressor-PL'),         # oppressors (NOT ne-ngniam-te)
    'leenglate': ('leengla-te', 'guest-PL'),               # guests/invitees (NOT leeng-la-te)
    'leengla': ('leengla', 'guest'),                       # base - guest/invitee
    'innlamte': ('innlam-te', 'builder-PL'),               # builders (NOT i-nnlam-te)
    'gitlohnate': ('gitlohna-te', 'wickedness-PL'),        # wickednesses/sins
    'mawhsakte': ('mawhsak-te', 'adversary-PL'),           # adversaries
    'mawhsak': ('mawhsak', 'adversary'),                   # base - adversary/enemy
    
    # Session 6 Round 18: More over-segmentation fixes
    'bilvangte': ('bilvang-te', 'loop-PL'),                # loops (curtain coupling)
    'mithagolte': ('mithagol-te', 'giant-PL'),             # giants
    'lianpipite': ('lianpipi-te', 'great-PL'),             # great ones (stones)
    'lelte': ('lel-te', 'desperate-PL'),                   # desperate ones
    'lel': ('lel', 'desperate'),                           # base - desperate
    'thante': ('than-te', 'worm-PL'),                      # worms/corruption
    'dote': ('do-te', 'rise-PL'),                          # those who rise up
    'do': ('do', 'rise'),                                  # base - rise against
    'ngeekte': ('ngeek-te', 'herb-PL'),                    # herbs/grass
    'ngeek': ('ngeek', 'herb'),                            # base - herb/grass
    
    # Session 6 Round 19: More over-segmentation fixes
    'ankungte': ('ankung-te', 'herb-PL'),                  # herbs of field (NOT a-nkung-te)
    'natnate': ('natna-te', 'disease-PL'),                 # diseases (NOT na-tna-te)
    'geelnate': ('geelna-te', 'way-PL'),                   # ways/manners
    'ngiate': ('ngia-te', 'field-PL'),                     # standing corn/fields
    'lungkhamnate': ('lungkhamna-te', 'tribulation-PL'),   # tribulations
    'hauhnate': ('hauhna-te', 'riches-PL'),                # riches/wealth
    'phatnate': ('phatna-te', 'praise-PL'),                # praises
    'tagahte': ('tagah-te', 'orphan-PL'),                  # orphans/fatherless
    'tagah': ('tagah', 'orphan'),                          # base - orphan
    'meigongte': ('meigong-te', 'widow-PL'),               # widows
    'meigong': ('meigong', 'widow'),                       # base - widow
    'khutmete': ('khutme-te', 'finger-PL'),                # fingers (NOT khut-me-te)
    
    # Session 6 Round 20: More over-segmentation fixes
    'meimate': ('meima-te', 'wound-PL'),                   # wounds
    'meima': ('meima', 'wound'),                           # base - wound/sore
    'kimte': ('kim-te', 'nation-PL'),                      # all nations/peoples
    'kim': ('kim', 'nation'),                              # base - all/nation
    'lawkite': ('lawki-te', 'Gentile-PL'),                 # Gentiles/heathen
    'lawki': ('lawki', 'Gentile'),                         # base - Gentile/heathen
    'ciangkangte': ('ciangkang-te', 'rod-PL'),             # rods/peeled sticks (NOT cian-gkang)
    'kicite': ('kici-te', 'called-PL'),                    # those called/named
    'kici': ('kici', 'called'),                            # base - be called
    'leenggahte': ('leenggah-te', 'grape-PL'),             # grapes (NOT leeng-gah-te)
    'kholhnate': ('kholhna-te', 'divination-PL'),           # divinations (opaque lexeme)
    'kholhna': ('kholhna', 'divination'),                  # base - divination (opaque)
    
    # Session 6 Round 21: More over-segmentation fixes
    'anlimte': ('anlim-te', 'dainty-PL'),                  # dainties (NOT a-nlim-te)
    'gannote': ('ganno-te', 'lamb-PL'),                    # lambs/fatlings
    'ganno': ('ganno', 'lamb'),                            # base - lamb/young animal
    'zawngte': ('zawng-te', 'poor-PL'),                    # the poor (NOT za-wng-te)
    'kiute': ('kiu-te', 'corner-PL'),                      # corners
    'kiu': ('kiu', 'corner'),                              # base - corner
    'haute': ('hau-te', 'rich-PL'),                        # the rich
    'hau': ('hau', 'rich'),                                # base - rich
    'pote': ('po-te', 'grow-PL'),                          # growths/harvests
    'po': ('po', 'grow'),                                  # base - grow
    'namtuite': ('namtui-te', 'perfume-PL'),               # perfumes/odours (NOT na-mtui-te)
    'miphakte': ('miphak-te', 'leper-PL'),                 # lepers
    'gamhte': ('gamh-te', 'inheritance-PL'),               # inheritances (NOT gam-h-te)
    
    # Session 6 Round 22: More over-segmentation fixes
    'tuletate': ('tuleta-te', 'breast-PL'),                # breasts/wombs
    'tuleta': ('tuleta', 'breast'),                        # base - breast/womb
    'khainiangte': ('khainiang-te', 'chain-PL'),           # chains/wreaths
    'puantungsilhte': ('puantungsilh-te', 'coat-PL'),      # coats (NOT pua-ntungsilh-te)
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
    'hang': ('hang', 'reason'),                          # base - stallion/mighty
    'meivakkhuamte': ('mei-vak-khuam-te', 'fire-light-pillar-PL'), # candlesticks
    'meivakkhuam': ('mei-vak-khuam', 'fire-light-pillar'), # candlestick/lampstand
    'leenggahzute': ('leeng-gah-zu-te', 'grape.juice-PL'),  # wine (plural)
    # leenggahzu now handled by hierarchical system → 'grape.juice'
    'gahzu': ('gah-zu', 'fruit-juice'),                     # base - fruit juice
    'sungnungte': ('sungnung-te', 'inner.room-PL'),        # inner chambers/rooms
    'sungnung': ('sungnung', 'inner.room'),                # base - inner room
    'lamlakte': ('lamlak-te', 'counsellor-PL'),            # counsellors/advisers
    'lamlak': ('lamlak', 'counsellor'),                    # base - counsellor
    
    # More vocabulary
    'lokhote': ('lokho-te', 'farmer-PL'),                  # farmers/husbandmen
    'laitaite': ('laitai-te', 'messenger-PL'),             # posts/messengers
    'laitai': ('laitai', 'messenger'),                     # base - messenger/post
    'thupalsatnate': ('thupalsatna-te', 'transgression-PL'),  # transgressions
    'namsaute': ('namsau-te', 'knife-PL'),                 # knives/lances
    'vankinusiate': ('vankinusia-te', 'colored.spoil-PL'), # colored spoils
    'vankinusia': ('vankinusia', 'colored.spoil'),         # colored spoil/prey
    'vanmanphate': ('vanmanpha-te', 'treasure-PL'),        # treasures
    
    # Round 24: Job, Psalms, Exodus, Chronicles vocabulary
    'khuamluzepnate': ('khuamluzepna-te', 'fillet-PL'),    # fillets/bands
    'luzep': ('luzep', 'encircle'),                        # base - encircle/surround
    'kihhuainate': ('kihhuaina-te', 'abomination-PL'),     # abominations
    'kihhuai': ('ki-hhuai', 'REFL-abominate'),             # abominate
    'vaihawmnate': ('vaihawmna-te', 'counsel-PL'),         # counsels/secrets
    'dangtakte': ('dangtak-te', 'weary-PL'),               # weary/tired ones
    'thungetnate': ('thungetna-te', 'prayer-PL'),          # prayers
    'papite': ('papi-te', 'elder-PL'),                     # elders/aged men
    'papi': ('papi', 'elder'),                             # base - elder/aged
    'mawhsaknate': ('mawhsakna-te', 'sin.offering-PL'),    # sin offerings
    'kisate': ('kisa-te', 'proud-PL'),                     # proud ones
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
    'dawibiate': ('dawibia-te', 'heathen-PL'),             # heathens/gentiles
    'dawibia': ('dawibia', 'heathen'),                     # base - heathen
    'nopsaknate': ('nopsakna-te', 'restoration-PL'),       # restorations
    'nopsak': ('nopsak', 'restore'),                       # base - restore
    'hualte': ('hual-te', 'wave-PL'),                      # waves
    'hual': ('hual', 'wave'),                              # base - wave
    'theikungte': ('theikung-te', 'fig.tree-PL'),          # fig trees
    
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
    'phunnate': ('phunna-te', 'murmuring-PL'),             # murmurings
    'phunna': ('phun-na', 'murmur-NMLZ'),                  # murmuring
    'phun': ('phun', 'murmur'),                            # base - murmur
    'kuangdaite': ('kuangdai-te', 'dish-PL'),              # dishes
    'dai': ('dai', 'flat'),                                # base - flat
    'kilhnate': ('kilhna-te', 'clasp-PL'),                 # clasps/taches
    'kilhna': ('kilh-na', 'join-NMLZ'),                    # clasp
    'kilh': ('kilh', 'join'),                              # base - join
    
    # Round 27: Nominalizations from various books
    'sawmsimna': ('sawmsim-na', 'conspiracy-NMLZ'),        # conspiracy
    'zahkona': ('zahko-na', 'reproach-NMLZ'),              # reproach/shame
    'lungzinna': ('lungzin-na', 'darkness-NMLZ'),          # shadow/darkness
    'lungzin': ('lung-zin', 'heart-shadow'),               # shadow/darkness
    'palsatna': ('palsat-na', 'transgression-NMLZ'),       # transgression
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
    'khai': ('khai', 'hang'),                              # base - hang
    'sikkhaute': ('sikkhau-te', 'bond-PL'),                # bonds/yokes
    'mineute': ('mineu-te', 'little.one-PL'),              # little ones
    'mineu': ('mi-neu', 'person-small'),                   # little one
    'ciangkhutte': ('ciangkhut-te', 'stripe-PL'),          # stripes/white streaks
    
    # Round 29: High-frequency partial words
    'gialpi': ('gial-pi', 'hail-big'),                     # grievous hail
    'pi': ('pi', 'grandmother'),                                   # base - big/great
    'palsatin': ('palsat-in', 'transgress-ERG'),           # transgressing
    'semsemin': ('semsem-in', 'breathe-ERG'),              # breathing/dying
    'musane': ('musane', 'pelican'),                       # pelican (bird)
    'limtak': ('lim-tak', 'true~REDUP'),                    # truly/well/accepted
    'khuaphialep': ('khua-phial-ep', 'sky-flash-lightning'), # lightning
    'phial': ('phial', 'flash'),                           # base - flash
    'ep': ('ep', 'strike'),                                # base - strike/hit
    'balnenin': ('balnen-in', 'tear-ERG'),                 # tearing/torn
    'balnen': ('balnen', 'tear'),                          # base - tear/rip
    'luhin': ('luh-in', 'smite-ERG'),                      # smiting/ripping
    'pelmawh': ('pel-mawh', 'report-evil'),                # report/denounce
    'nawkgawp': ('nawk-gawp', 'overtake-all'),             # overwhelm/tempest
    'gawp': ('gawp', 'all'),                               # base - all
    
    # Round 30: More high-frequency partial words
    'omteng': ('om-teng', 'exist-remain'),                 # remain/survive
    'teng': ('teng', 'remain'),                            # base - remain
    'omlain': ('om-lai-in', 'exist-midst-ERG'),            # existing in midst
    'dington': ('ding-ton', 'stand-stable'),               # stand firm
    'tonu': ('tonu', 'mistress'),                          # mistress/lady
    'bai': ('bai', 'rise.early'),                          # rise early/arise
    'dampah': ('dam-pah', 'healthy-clear'),                # cleansed/healed
    'henhan': ('henhan', 'like'),                          # like/as in similes (9x)
    'henhanin': ('henhan-in', 'like-ERG'),                 # by/as like (Acts 17:5)
    # hen removed from ATOMIC - it's in FUNCTION_WORDS as JUSS and VERB_STEMS as 'tie'
    'hitaseleh': ('hi-ta-se-leh', 'be-that-CONN-COND'),    # although that
    'bawlsiain': ('bawl-sia-in', 'make-evil-ERG'),         # doing evil
    'puannin': ('puannin', 'rag'),                         # filthy rag (Isa 64:6)
    
    # Round 31: More high-frequency partial words
    'kongpuankhai': ('kong-puan-khai', 'door-cloth-hang'),   # hanging/curtain
    'vawhin': ('vawh-in', 'arise-ERG'),                    # arising
    'baan': ('baan', 'lay'),                               # base - lay/put
    'liangkoah': ('liangko-ah', 'shoulder-LOC'),           # on shoulders
    'pataukoh': ('pa-tau-koh', 'male-signal-call'),        # alarm/trumpet call
    'tau': ('tau', 'signal'),                              # base - signal
    'gelhsa': ('gelh-sa', 'write-PERF'),                   # written
    'nilhin': ('nilh-in', 'anoint-ERG'),                   # anointing
    
    # Round 32: More vocabulary from Numbers, Deut, Kings, Judges
    'zawngin': ('zawng-in', 'lack-ERG'),                   # lacking/poor
    'hamsia': ('ham-sia', 'curse-evil'),                   # curse
    'nawkkha': ('nawk-kha', 'turn-CAUS'),                  # turn aside
    'khuaneu': ('khua-neu', 'town-small'),                 # village
    'angvan': ('ang-van', 'face-see'),                     # show favoritism
    'angvanin': ('ang-van-in', 'face-see-ERG'),            # showing partiality
    'angvanna': ('ang-van-na', 'face-see-NMLZ'),           # partiality
    'sawtpi': ('sawt-pi', 'long-big'),                     # prolong/long time
    'sukhamin': ('sukham-in', 'grind-ERG'),                # grinding
    'cinna': ('cin-na', 'plant-NMLZ'),                     # garden/planting
    'cin': ('cin', 'plant'),                               # base - plant
    'kiatna': ('kiat-na', 'fall-NMLZ'),                    # falling place
    'kiat': ('kiat', 'fall'),                              # base - fall
    'samzang': ('samzang', 'hair'),                         # hair (of head)
    'samzangte': ('samzang-te', 'hair-PL'),                  # hairs
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
    'phelkhia': ('phel-khia', 'break-out'),                # overthrow/destroy
    'khia': ('khia', 'out'),                               # base - out
    'kangtumin': ('kangtum-in', 'consume-ERG'),            # consuming
    'kangtum': ('kang-tum', 'burn-all'),                   # consume
    'siahuaizaw': ('sia-huai-zaw', 'evil-bad-more'),       # more evil
    'huai': ('huai', 'bad'),                               # base - bad
    'humpinelkaite': ('humpinelkai-te', 'ornament-PL'),    # ornaments/decorations
    'humpinelkai': ('hum-pinelkai', 'cover-ornament'),     # ornament
    'pinelkai': ('pinelkai', 'ornament'),                  # base - ornament
    'sawmnihna': ('sawm-nih-na', 'ten-two-ORD'),           # twentieth
    'nih': ('nih', 'two'),                                 # base - two
    
    # Round 34: More vocabulary from Nehemiah, Esther, Job, Psalms
    'vangliatnate': ('vangliatna-te', 'power-PL'),         # powers/might
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
    'omom': ('om~om', 'exist~REDUP'),                      # remain/still
    'mutkhiat': ('mut-khiat', 'blow-away'),                # blow away
    'nuihsat': ('nuih-sat', 'laugh-toward'),               # laugh at
    'imcip': ('im-cip', 'hide-tight'),                     # hide/conceal
    'im': ('im', 'hide'),                                  # base - hide
    'zalzal': ('zal~zal', 'stretch~REDUP'),                  # rattle/shake
    'hihnop': ('hih-nop', 'do-want'),                      # plan/thought
    'zahhuai': ('zah-huai', 'ashamed-bad'),                # ashamed/vexed
    
    # Round 35: More vocabulary
    'kiliatsakna': ('ki-liat-sak-na', 'REFL-oppress-CAUS-NMLZ'), # oppression
    'kiselna': ('ki-sel-na', 'REFL-quarrel-NMLZ'),         # strife
    'sel': ('sel', 'quarrel'),                             # base - quarrel
    'nuntakzia': ('nuntak-zia', 'live-manner'),            # ways/lifestyle
    'zia': ('zia', 'manner'),                              # base - manner
    'damdam': ('dam~dam', 'be.well~REDUP'),                    # softly/gently
    'maitai': ('mai-tai', 'face-bright'),                  # radiant/lightened
    'etlawm': ('et-lawm', 'fat-lamb'),                     # fat/fatness
    'lawm': ('lawm', 'worthy'),                              # base - lamb
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
    'khuakulhpi': ('khua-kulh-pi', 'town-wall-big'),       # fenced wall
    'kulhpi': ('kulh-pi', 'wall-big'),                     # great wall
    'mulkimhuai': ('mul-kim-huai', 'full-all-bad'),        # horrible
    'thuvanpi': ('thu-van-pi', 'word-write-master'),       # scribe
    'thuakkhawm': ('thuak-khawm', 'suffer-together'),      # suffer together
    'tangsak': ('tang-sak', 'give-CAUS'),                  # give/provide
    'theinuam': ('thei-nuam', 'know-want'),                # want to know
    'nuam': ('nuam', 'want'),                              # base - want
    'paunam': ('pau-nam', 'speak-nation'),                 # language
    'nam': ('nam', 'nation'),                              # base - nation
    'paipah': ('pai-pah', 'go-arrive'),                    # arrive/come
    'tonkhawm': ('ton-khawm', 'meet-together'),            # meet together
    
    # Round 37: More vocabulary from Matthew, Genesis, Exodus
    'zineipa': ('zinei-pa', 'marry-male'),                 # bridegroom
    'meivakna': ('mei-vak-na', 'fire-light-NMLZ'),         # candlestick/lamp
    'innteek': ('inn-teek', 'house-master'),               # householder/master
    'teek': ('teek', 'master'),                            # base - master
    'pianpih': ('pian-pih', 'born-with'),                  # born together
    'zukhamna': ('zukham-na', 'wine-NMLZ'),                # wine/drunkenness
    'zukham': ('zukham', 'wine'),                          # base - wine
    'thaneemna': ('thaneem-na', 'naked-NMLZ'),             # nakedness
    'thaneem': ('thaneem', 'naked'),                       # base - naked
    'niamsak': ('niam-sak', 'bow-CAUS'),                   # bow down
    'kikhenthang': ('ki-khen-thang', 'REFL-separate-scatter'), # scattered
    'thang': ('thang', 'scatter'),                         # base - scatter
    'khing': ('khing', 'remain'),                          # base - remain
    'dikdek': ('dik-dek', 'small~REDUP'),                  # very small
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
    'ap': ('ap', 'entrust'),                                  # base - span
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
    'tuampian': ('tuam-pian', 'swell-appear'),             # rising/bright spot
    'tuam': ('tuam', 'swell'),                             # base - swell
    'piakzawh': ('piak-zawh', 'give-finish'),              # give completely
    'neksak': ('nek-sak', 'eat-CAUS'),                     # cause to eat/devour
    'hinna': ('hi-n-na', 'be-CONN-NMLZ'),                  # life/living
    'velval': ('vel-val', 'turn~REDUP'),                    # causing/making bitter
    'vel': ('vel', 'turn'),                                # base - turn
    'tuithuk': ('tui-thuk', 'water-deep'),                 # deep/depth
    
    # Round 39: More vocabulary from Numbers, Leviticus, Deuteronomy
    'mulkiatna': ('mul-kiat-na', 'hair-cut-NMLZ'),         # razor
    'piakhawm': ('piak-hawm', 'give-together'),            # offer together
    'hawm': ('hawm', 'together'),                          # base - together
    'sutan': ('sut-an', 'break-NEG'),                      # not break
    'sut': ('sut', 'break'),                               # base - break
    'kibangsak': ('ki-bang-sak', 'REFL-equal-CAUS'),       # sound alarm
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
    'ciahpihin': ('ciah-pih-in', 'return-with-ERG'),       # bring/restore
    'paithei': ('pai-thei', 'go-ABIL'),                    # able to go/come
    
    # Round 40: More vocabulary from Deuteronomy, Joshua, Leviticus, Numbers
    'makna': ('mak-na', 'divorce-NMLZ'),                   # divorcement
    'thehthangna': ('theh-thang-na', 'throw-scatter-NMLZ'), # scattering
    'theh': ('theh', 'throw'),                             # base - throw
    'kihuhna': ('ki-huh-na', 'REFL-help-NMLZ'),             # help/safety
    'muhsak': ('muh-sak', 'see.II-BENF'),                  # show (for someone) - Form II + sak
    'ensim': ('en-sim', 'look-count'),                     # view/survey
    'sim': ('sim', 'count'),                               # base - count
    'khawlcip': ('khawl-cip', 'rest-tight'),               # stand still
    'sawmkhat': ('sawm-khat', 'ten-one'),                  # eleven/ten
    'vanvan': ('van~van', 'old~REDUP'),                      # ancient/very old (old sense)
    # Note: standalone 'van' = 'sky' (NOUN_STEMS), reduplication 'vanvan' = 'old~REDUP' (ancient)
    'khengvalin': ('kheng-val-in', 'proud-presume-ERG'),   # presumptuously
    'kheng': ('kheng', 'proud'),                           # base - proud
    'nangzo': ('nang-zo', 'face-ABIL'),                    # able to face
    'zo': ('zo', 'south'),                                  # base - able
    'anlom': ('an-lom', 'offering-wave'),                  # wave offering
    'lom': ('lom', 'wave'),                                # base - wave
    'hihloh': ('hi-hloh', 'be-NEG'),                       # not be
    'hloh': ('hloh', 'NEG'),                               # base - negative
    'innkuankuan': ('inn-kuan-kuan', 'house-family~REDUP'), # families
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
    'nuamzaw': ('nuam-zaw', 'want-more'),                  # prefer/rather
    'maimom': ('mai-mom', 'face-web'),                     # spider web
    'mom': ('mom', 'web'),                                 # base - web
    'thuakkha': ('thuak-kha', 'suffer-NEGPERF'),           # not suffer/safe
    'kha': ('kha', 'NEG.PERF'),                            # suffix - negative perfect
    'venvan': ('ven-van', 'protect-store'),                # heap up/store
    'manphatna': ('man-phat-na', 'price-worthy-NMLZ'),     # value/exchange
    'phat': ('phat', 'worthy'),                            # base - worthy
    'tehtheih': ('teh-theih', 'measure-ABIL'),             # comparable/equal
    'khollo': ('khol-lo', 'care-NEG'),                     # forget/not care
    'cihsan': ('cih-san', 'say-rely'),                     # trust/declare trust
    
    # Round 42: More vocabulary from Kings, Chronicles, Psalms, Proverbs
    'satvui': ('sat-vui', 'strike-dust'),                  # smash to pieces
    'vui': ('vui', 'dust'),                                # base - dust
    'galdaihna': ('gal-daih-na', 'enemy-ABIL-NMLZ'),       # dominion
    'daih': ('daih', 'able'),                              # base - able
    'sepkhiat': ('sep-khiat', 'work-extract'),             # execute judgment
    'sep': ('sep', 'work'),                                # base - work
    'khiat': ('khiat', 'extract'),                         # base - extract
    'theithek': ('thei-thek', 'know-extreme'),             # abundant/know well
    'thek': ('thek', 'extreme'),                           # base - extreme
    'khialhsak': ('khialh-sak', 'sin-CAUS'),               # cause to sin
    'omzaw': ('om-zaw', 'exist-more'),                     # more numerous
    'taangkona': ('taang-ko-na', 'time-long-NMLZ'),        # long period
    'ko': ('ko', 'long'),                                  # base - long
    'zuauna': ('zuau-na', 'lie-NMLZ'),                     # lying
    'zuau': ('zuau', 'lie'),                               # base - lie
    'sibup': ('si-bup', 'die-all'),                        # completely exhausted
    'bup': ('bup', 'all'),                                 # base - all
    'thuaklawh': ('thuak-lawh', 'suffer-PERF'),            # suffered
    'lawh': ('lawh', 'PERF'),                              # suffix - perfective
    'leengmang': ('leeng-mang', 'chariot-fly'),            # fly away
    'mang': ('mang', 'dream'),                               # base - fly
    'zawkna': ('zawk-na', 'more-NMLZ'),                    # surplus/excess
    'zawk': ('zawk', 'more'),                              # base - more
    
    # Round 43: More vocabulary from Ruth, Samuel, Kings, Chronicles, Job, Psalms, Jeremiah
    'lohbuang': ('loh-buang', 'apart-divide'),             # separation/parting
    'buang': ('buang', 'divide'),                          # base - divide
    'kizuih': ('ki-zuih', 'REFL-hang'),                    # hang oneself
    'kithuah': ('ki-thuah', 'REFL-gird'),                  # gird oneself
    'thuah': ('thuah', 'gird'),                            # base - gird
    'zozaw': ('zo-zaw', 'able-more'),                      # overcome/prevail
    'meiphual': ('mei-phual', 'fire-field'),               # furnace
    'phual': ('phual', 'field'),                           # base - field
    'kipakta': ('ki-pak-ta', 'REFL-wait-TA'),              # wait patiently
    'suangkang': ('suang-kang', 'stone-pillar'),           # marble pillar
    'suangphah': ('suang-phah', 'stone-floor'),            # pavement
    'manlah': ('man-lah', 'time-ADV'),                     # afterward/later
    'themthum': ('them-thum', 'dawn-early'),               # every moment
    'them': ('them', 'dawn'),                              # base - dawn
    'thum': ('thum', 'three'),                             # base - early
    'gakcip': ('gak-cip', 'trap-tight'),                   # snare/gin
    'gak': ('gak', 'trap'),                                # base - trap
    'kikaikhia': ('ki-kai-khia', 'REFL-dig-out'),          # uproot
    'thangsiah': ('thang-siah', 'speak-compose'),          # conspire/encourage
    'siah': ('siah', 'compose'),                           # base - compose
    'maban': ('ma-ban', 'own-matter'),                     # concerning
    'ban': ('ban', 'besides'),                              # base - matter
    'taisim': ('tai-sim', 'check-count'),                  # investigate
    'tai': ('tai', 'check'),                               # base - check
    
    # Round 44: More vocabulary from Jeremiah, Exodus, Song of Solomon, Job, etc.
    'sunteng': ('sun-teng', 'basket~REDUP'),              # baskets
    'sun': ('sun', 'basket'),                              # base - basket
    'kihual': ('ki-hual', 'REFL-bind'),                    # interweave/wreathen
    'phet': ('phet', 'twin'),                              # twins
    'lawmnu': ('lawm-nu', 'friend-female'),                # bride/companion
    'seelcip': ('seel-cip', 'cover-tight'),                # conceal
    'meisuang': ('mei-suang', 'fire-stone'),               # flint/sharp stone
    'puksisak': ('puk-si-sak', 'attack-die-CAUS'),         # cause to die/kill
    'puk': ('puk', 'attack'),                              # base - attack
    'hehlua': ('heh-lua', 'angry-excessive'),              # burst in anger
    'kilaak': ('ki-laak', 'REFL-show'),                    # present oneself/appear
    'laak': ('laak', 'show'),                              # base - show
    'suahkhiat': ('suah-khiat', 'born-out'),               # come out/emerge
    'kigawh': ('ki-gawh', 'REFL-touch'),                   # touch/lay hand on
    'gawh': ('gawh', 'touch'),                             # base - touch
    'kisuksiat': ('ki-suk-siat', 'REFL-collapse-destroy'), # be destroyed/snared
    'suk': ('suk', 'collapse'),                            # base - collapse
    'siat': ('siat', 'destroy'),                           # base - destroy
    'tuahun': ('tuah-un', 'do-time'),                      # occurrence/controversy
    'un': ('un', 'PL.IMP'),                                  # base - time
    'meidawi': ('mei-dawi', 'fire-fear'),                  # cowardly/fainthearted
    'dawi': ('dawi', 'fear'),                              # base - fear
    'huihpi': ('huih-pi', 'wind-great'),                   # strong wind
    'huih': ('huih', 'wind'),                              # base - wind
    'kiphuk': ('ki-phuk', 'REFL-overthrow'),               # be toppled/cast down
    'phuk': ('phuk', 'overthrow'),                         # base - overthrow
    
    # Round 45: More vocabulary from Genesis, Numbers, Deuteronomy, Judges, Kings, Job, Psalms
    'bengin': ('beng-in', 'hunt-ERG'),                     # hunting
    'haza': ('haza', 'envy'),                              # envy/jealousy
    'gega': ('gega', 'red'),                               # red
    'kihut': ('ki-hut', 'REFL-arm'),                       # arm oneself
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
    'kigengen': ('ki-gen-gen', 'REFL-say~REDUP'),          # be spoken
    'zen': ('zen', 'way'),                                 # way/manner
    'kineihin': ('ki-nei-hin', 'REFL-with-CVB'),           # bow down
    
    # Round 46: More vocabulary from Ezekiel, Matthew, Luke, Genesis, Exodus, Leviticus
    'hauhlawh': ('hauh-lawh', 'grasp-PERF'),               # extort
    'hot': ('hot', 'steer'),                               # pilot/steer
    'tunuam': ('tu-nuam', 'sit-pleasant'),                 # best seats
    'tu': ('tu', 'now'),                                   # base - sit
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
    'kibehlaplap': ('ki-behlap-lap', 'REFL-grow~REDUP'),   # grow greatly
    'tenkhop': ('ten-khop', 'dwell-join'),                 # settle together
    'ki-ip': ('ki-ip', 'REFL-hold'),                       # restrain oneself
    'ki-ipzo': ('ki-ip-zo', 'REFL-hold-ABIL'),             # able to restrain
    'kiciangtan': ('ki-ciang-tan', 'REFL-straight-assign'), # portion assigned
    'tan': ('tan', 'assign'),                              # base - assign
    'mawlpih': ('mawl-pih', 'dig-APPL'),                   # dig down
    'mawl': ('mawl', 'dig'),                               # base - dig
    'takun': ('takun', 'maiden'),                          # maiden/maid
    'phawkzo': ('phawk-zo', 'remember-ABIL'),              # remember
    'phawk': ('phawk', 'remember'),                        # base - remember
    'thokang': ('tho-kang', 'rise-extend'),                # stretch out
    'denggawp': ('deng-gawp', 'strike-break'),             # smash/break
    'deng': ('deng', 'strike'),                            # base - strike
    'kot': ('kot', 'ready'),                               # equipped/ready
    'kingen': ('ki-ngen', 'REFL-request'),                 # be demanded
    'kimciang': ('kim-ciang', 'complete-straight'),        # span end to end
    'kikhaisuk': ('ki-khai-suk', 'REFL-hang-fall'),        # curtain/hanging
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
    'guallelsak': ('gual-lel-sak', 'enemy-change-CAUS'),   # defeat/cause smitten
    
    # Round 48: More vocabulary from Judges, Samuel, Kings, Chronicles, Ezra, Job, Psalms
    'hanthot': ('han-thot', 'begin-stir'),                 # begin moving
    'thot': ('thot', 'stir'),                              # base - stir
    'thaneih': ('tha-neih', 'strength-have'),              # have strength
    'kihanthawnin': ('ki-han-thawn-in', 'REFL-begin-encourage-CVB'), # encourage oneself
    'thawn': ('thawn', 'encourage'),                       # base - encourage
    'suangtang': ('suang-tang', 'stone-embed'),            # sink into
    'tang': ('tang', 'embed'),                             # base - embed
    'tawngnung': ('tawng-nung', 'speak-later'),            # back area/cave
    'nung': ('nung', 'later'),                             # base - later
    'mansuah': ('man-suah', 'price-escape'),               # missing
    'suah': ('suah', 'SUAH'),                            # base - escape
    'lohlam': ('loh-lam', 'NEG-way'),                      # not the way
    'khezaw': ('khe-zaw', 'foot-weak'),                    # lame
    'kilawnsuk': ('ki-lawn-suk', 'REFL-throw-fall'),       # be thrown
    'lawn': ('lawn', 'throw'),                             # base - throw
    'kilokgawp': ('ki-lok-gawp', 'REFL-shake-break'),      # tremble
    'lok': ('lok', 'shake'),                               # base - shake
    'kizong': ('ki-zong', 'REFL-warm'),                    # warm oneself
    'zong': ('zong', 'also'),                              # base - also
    'kipiatawm': ('ki-piat-awm', 'REFL-sell-self'),        # sell oneself
    'piat': ('piat', 'sell'),                              # base - sell
    'awm': ('awm', 'self'),                                # base - self
    'kilawmzaw': ('ki-lawm-zaw', 'REFL-worthy-more'),      # more fitting
    'zeizai': ('zei-zai', 'what-thing'),                   # everything
    'puksuk': ('puk-suk', 'fall-down'),                    # sink down
    'zun': ('zun', 'urine'),                               # urine
    'kizat': ('ki-zat', 'REFL-use'),                       # be used
    'golhguk': ('golhguk', 'bribe'),                       # opaque: bribe/undermine
    'golh': ('golh', 'oppose'),                            # base - oppose
    'kihisakin': ('ki-hi-sak-in', 'REFL-be-CAUS-CVB'),     # act proudly
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
    'zunglot': ('zung-lot', 'root-cast'),                  # uproot
    'lot': ('lot', 'cast'),                                # base - cast/throw/shoot (KJV "cast", "shot")
    'lazo': ('la-zo', 'take-ABIL'),                        # able to take
    'meilah': ('mei-lah', 'fire-lamp'),                    # lamp
    'lah': ('lah', 'lamp'),                                # base - lamp
    'tup': ('tup', 'roast'),                               # roast
    'piciang': ('pi-ciang', 'great-straight'),             # various/diverse
    'kiphattawm': ('ki-phat-tawm', 'REFL-praise-by'),      # be praised
    'kiheek': ('ki-heek', 'REFL-fold'),                    # twine/braid/betray (fold together/fold in cards)
    'heek': ('heek', 'fold'),                              # base - fold (wink=eye-fold, cord=folded, betray=fold)
    'suangngo': ('suang-ngo', 'stone-socket'),             # socket/base
    'ngo': ('ngo', 'socket'),                              # base - socket
    'bupun': ('bup-un', 'all-time'),                       # cluster
    'gahpha': ('gah-pha', 'branch-good'),                  # flourishing
    'gah': ('gah', 'branch'),                              # base - branch
    'kikai': ('ki-kai', 'REFL-lead'),                      # be led away/captive
    'kilkel': ('kil-kel', 'clear-pure'),                   # phonotactic fix (no lk cluster)
    'lkel': ('lkel', 'leave'),                             # leave - probably typo in Bible; opaque
    'gip': ('gip', 'seal'),                                # seal
    'lipkhap': ('lip-khap', 'freedom-loose'),              # liberty
    'lip': ('lip', 'freedom'),                             # base - freedom
    'khap': ('khap', 'loose'),                             # base - loose
    
    # Round 50: More vocabulary from Acts, Corinthians, Genesis, Exodus
    'kithutuak': ('ki-thu-tuak', 'REFL-word-receive'),     # believe
    'tuak': ('tuak', 'receive'),                           # base - receive
    'kimuthei': ('ki-mu-thei', 'REFL-see-ABIL'),           # be visible
    'meiilum': ('mei-ilum', 'fire-mist'),                  # vapor/mist
    'ilum': ('ilum', 'mist'),                              # base - mist
    'kithukkik': ('ki-thuk-kik', 'REFL-revenge-ITER'),     # be avenged
    'kisunin': ('ki-sun-in', 'REFL-resemble-CVB'),         # in likeness
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
    'kigu': ('ki-gu', 'REFL-tear'),                        # be torn
    'lapi': ('la-pi', 'take-big'),                         # female animal
    'thagui': ('tha-gui', 'strength-cord'),                # sinew
    'gui': ('gui', 'cord'),                                # base - cord
    'moman': ('mo-man', 'bride-price'),                    # dowry
    'mo': ('mo', 'bride'),                                 # base - bride
    'mangman': ('mang-man', 'dream-person'),               # dreamer
    'teekpa': ('teek-pa', 'in.law-father'),                # father-in-law
    'huanpipa': ('huan-pi-pa', 'bread-great-man'),         # chief baker
    'huan': ('huan', 'bread'),                             # base - bread
    'gawng': ('gawng', 'lean'),                            # lean/ill-favoured
    'buhvui': ('buh-vui', 'rice-dust'),                    # grain
    'khitlam': ('khit-lam', 'finish-way'),                 # appearance
    'oksak': ('ok-sak', 'clothe-CAUS'),                    # cause to wear
    'ok': ('ok', 'clothe'),                                # base - clothe
    'tumpihin': ('tum-pih-in', 'set-APPL-CVB'),            # set before
    'gawl': ('gawl', 'neck'),                              # neck
    'sul': ('sul', 'snake'),                               # snake/serpent
    'hankuang': ('han-kuang', 'carry-box'),                # coffin
    'haksapi': ('hak-sa-pi', 'heavy-flesh-great'),         # hard labor
    
    # Round 51: More vocabulary from Jeremiah, Daniel, Hosea, Matthew, Luke, John, Acts, Exodus
    'kiphal': ('ki-phal', 'REFL-shut'),                    # be shut up
    'phal': ('phal', 'shut'),                              # base - shut
    'dozo': ('do-zo', 'throw-ABIL'),                       # able to cast
    'lawptakin': ('lawp-tak-in', 'shake-truly-ERG'),       # trembling
    'tak': ('tak', 'truly'),                               # base - truly
    'lonei': ('lo-nei', 'NEG-have'),                       # tares/without
    'kimtakin': ('kim-tak-in', 'complete-truly-ERG'),      # thoroughly
    'tuukulh': ('tuu-kulh', 'climb-steal'),                # sneak up/climb
    'tuu': ('tuu', 'climb'),                               # base - climb
    'kulh': ('kulh', 'steal'),                             # base - steal
    'tunma-in': ('tun-ma-in', 'arrive-EMPH-ERG'),          # before
    'holhthawh': ('holh-thawh', 'stir-up'),                # incite/stir up
    'holh': ('holh', 'stir'),                              # base - stir
    'kithawisa-in': ('ki-thawi-sa-in', 'REFL-ready-already-CVB'), # harnessed
    'thawi': ('thawi', 'ready'),                           # base - ready
    'lopipi-in': ('lo-pi-pi-in', 'NEG-great-great-ERG'),   # powerfully
    
    # Round 52: Massive batch from Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, Samuel
    'khuituah': ('khui-tuah', 'sew-do'),                   # sew together (curtains, etc.)
    'khui': ('khui', 'sew'),                               # sew, stitch, mend (not 'fold')
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
    'zuthawl': ('zu-thawl', 'slave-female'),               # female slave
    'ki-apsa': ('ki-ap-sa', 'REFL-devote-already'),        # devoted
    'teep': ('teep', 'fringe'),                            # fringe
    'kipumsil': ('ki-pum-sil', 'REFL-body-wash'),          # bathe
    'pum': ('pum', 'body'),                                # base - body
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
    'lengkhia-in': ('leng-khia-in', 'line-out-ERG'),       # draw out
    'leng': ('leng', 'line'),                              # base - line
    'kuansuk': ('kuan-suk', 'attack-fall'),                # slay
    'kihu': ('ki-hu', 'REFL-help'),                        # plead
    'hu': ('hu', 'help'),                                  # base - help
    'kisatgawp': ('ki-sat-gawp', 'REFL-strike-break'),     # set against
    'kuikek': ('kui-kek', 'tear-scratch'),                 # tear
    'kui': ('kui', 'tear'),                                # base - tear
    'kek': ('kek', 'scratch'),                             # base - scratch
    'domto-in': ('dom-to-in', 'go-UP-ERG'),                # going up
    'dom': ('dom', 'go'),                                  # base - go
    'kilehhei': ('ki-leh-hei', 'REFL-return-wonder'),      # be amazed
    'liimnuai': ('liim-nuai', 'wing-under'),               # under wings
    'haih': ('haih', 'winnow'),                            # winnow
    'galphual': ('gal-phual', 'enemy-field'),              # battlefield
    'tumsiam': ('tum-siam', 'play-skilled'),               # skilled player
    
    # Round 53: Another massive batch from Samuel, Kings, Chronicles, Ezra, Job, Psalms, Proverbs
    'kinawhin': ('ki-nawh-in', 'REFL-meet-CVB'),           # meet/come to meet
    'nawh': ('nawh', 'meet'),                              # base - meet
    'gimlua': ('gim-lua', 'faint-excessive'),              # exhausted
    'gim': ('gim', 'faint'),                               # base - faint
    'kikekin': ('ki-kek-in', 'REFL-scratch-CVB'),          # rent/torn
    'kilok': ('ki-lok', 'REFL-shake'),                     # cast away
    'kheging': ('khe-ging', 'foot-sound'),                 # sound of going
    'ging': ('ging', 'sound'),                             # base - sound
    'gel': ('gel', 'together'),                            # together
    'kizal': ('ki-zal', 'REFL-stretch'),                   # stretch forth
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
    'peekpi': ('peek-pi', 'spread-big'),                   # spread out
    'mei-ek': ('mei-ek', 'fire-sneeze'),                   # neesings/light
    'vutlevai': ('vut-levai', 'dust-spread'),              # dust and ashes
    'levai': ('levai', 'spread'),                          # base - spread
    'kipaaksak': ('ki-paak-sak', 'REFL-glad-CAUS'),        # make glad
    'paak': ('paak', 'glad'),                              # base - glad
    'kituancil': ('ki-tuan-cil', 'REFL-cut-piece'),        # cut in pieces
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
    'kikhinin': ('ki-khin-in', 'REFL-behind-CVB'),         # move behind
    'khin': ('khin', 'IMM'),                            # base - behind
    'haknaw': ('hak-naw', 'heavy-lead'),                   # sink like lead
    'naw': ('naw', 'lead'),                                # base - lead (metal)
    'lawnkhak': ('lawn-khak', 'throw-lock'),               # set bounds
    'seelsim': ('seel-sim', 'cover-count'),                # uncover/steps
    'phih': ('phih', 'bowl'),                              # bowl/cover
    'tuucin': ('tuucin', 'shepherd'),                      # shepherd (lexicalized)
    'tuucing': ('tuucing', 'shepherd'),                    # shepherd variant
    'pelhthei': ('pelh-thei', 'escape-ABIL'),              # able to escape
    'pelh': ('pelh', 'escape'),                            # base - escape
    'kikup': ('ki-kup', 'REFL-hide'),                      # hide oneself
    'kup': ('kup', 'hide'),                                # base - hide
    'kinamin': ('ki-nam-in', 'REFL-kiss-CVB'),             # kiss/salute
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
    'mannop': ('man-nop', 'price-want'),                   # willing/hear
    'thongkiat': ('thong-kiat', 'prison-extract'),         # came unto prison
    'kitheithang': ('ki-thei-thang', 'REFL-know-spread'),  # blaze abroad
    'mapaisak': ('ma-pai-sak', 'EMPH-go-CAUS'),            # constrained to go
    'tamveipi': ('tam-vei-pi', 'many-time-great'),         # ofttimes
    'vei': ('vei', 'sick'),                                # base - time
    'thahkhit': ('thah-khit', 'kill-finish'),              # kill body
    'thongcing': ('thong-cing', 'prison-throw'),           # cast into prison
    'cing': ('cing', 'throw'),                             # base - throw
    'dongtangsak': ('dong-tang-sak', 'stumble-on-CAUS'),   # put stumblingblock
    'dong': ('dong', 'until'),                           # base - stumble
    'kilehngatin': ('ki-leh-ngat-in', 'REFL-return-time-CVB'), # say again
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
    'tuzawh': ('tu-zawh', 'sit-ABIL'),                     # possible/hard
    'zawh': ('zawh', 'able'),                              # base - able
    'tuununo': ('tuu-nu-no', 'ewe-female-small'),          # ewe lamb
    'makeng': ('ma-keng', 'EMPH-tree'),                    # grove/tree
    'temta': ('tem-ta', 'fire-hold'),                      # fire in hand
    'butsak': ('but-sak', 'face-CAUS'),                    # put upon face
    'but': ('but', 'face'),                                # base - face (alt)
    'kihehnem': ('ki-heh-nem', 'REFL-angry-comfort'),      # comfort oneself
    'galmat': ('gal-mat', 'enemy-steal'),                  # stolen away
    'mat': ('mat', 'steal'),                               # base - steal
    'khelkom': ('khel-kom', 'hollow-touch'),               # touched hollow
    'kom': ('kom', 'touch'),                               # base - touch
    'khel': ('khel', 'hollow'),                            # hollow (of thigh)
    'dawksak': ('dawk-sak', 'bind-CAUS'),                  # bound upon
    'pipa': ('pi-pa', 'great-man'),                        # chief/officer
    'phai': ('phai', 'meadow'),                            # meadow
    'kikhailum': ('ki-khai-lum', 'REFL-hang-round'),       # restored/hanged
    'lum': ('lum', 'round'),                               # base - round
    'gaih': ('gaih', 'little'),                            # little
    'kipulak': ('ki-pul-ak', 'REFL-expose-COMPL'),         # made known
    'gulgu': ('gul-gu', 'coil-bite'),                      # adder/serpent
    'phazaw-in': ('pha-zaw-in', 'good-more-ERG'),          # more/multiplied
    'kilangzo': ('ki-lang-zo', 'REFL-clear-ABIL'),         # hearken
    'lang': ('lang', 'clear'),                             # base - clear
    'vik': ('vik', 'rod'),                                 # rod
    'lomkhat': ('lom-khat', 'bundle-one'),                 # bunch (of hyssop)
    'phialgawp': ('phial-gawp', 'morning-watch'),          # morning watch
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
    'phattheih': ('phat-theih', 'praise-ABIL'),            # praiseworthy
    'mimawh': ('mi-mawh', 'person-sin'),                   # innocent/sinner
    'sumlei': ('sum-lei', 'money-buy'),                    # buyer/seller
    'pauthei': ('pau-thei', 'speak-ABIL'),                 # able to speak
    'pau': ('pau', 'PAU'),                               # base - speak
    'simun': ('sim-un', 'count-time'),                     # without ceasing
    'muthei': ('mu-thei', 'see-ABIL'),                     # able to see
    'mu': ('mu', 'see.I'),                                   # base - see
    'uploh': ('up-loh', 'look-NEG'),                       # not looking/unaware
    'up': ('up', 'PL.Q'),                                  # base - look
    
    # Round 59: Final push past 98%
    'leteh': ('let-eh', 'return-EXCL'),                    # it is good/bear
    'ninthem': ('nin-them', 'day-dawn'),                   # mote/early morning
    'bawlbawl': ('bawl~bawl', 'make~REDUP'),               # continually
    
    # Round 60: Pushing toward 98.5%
    'kiimnai': ('ki-im-nai', 'REFL-around-near'),            # neighboring, surrounding
    'tunma': ('tun-ma', 'arrive-before'),                  # meanwhile, in the meantime
    'lopipi': ('lo-pipi', 'NEG-really'),                   # unwillingly / with force (ut lopipi = strong hand)
    "huihpi'": ('huih-pi', 'wind-great'),                  # strong wind, east wind
    'kiphelkhamin': ('ki-phel-kham-in', 'REFL-split-break-CVB'),  # was rent/split
    'peka': ('pek-a', 'edge-LOC'),                         # uttermost parts, edge
    'kisukha': ('ki-suk-ha', 'REFL-pollute-CAUS'),         # defiled, made unclean
    "buppi'": ('bup-pi', 'all-great'),                     # entire, whole
    "kiguan'": ('ki-guan', 'REFL-deliver'),                # delivered, handed over
    'kiguan': ('ki-guan', 'REFL-deliver'),                 # delivered (no apostrophe)
    'suntangpi': ('sun-tang-pi', 'sun-before-great'),      # before the sun, publicly
    'phukha': ('phu-kha', 'emerge-go'),                    # seeth, sees, views
    'gimpi': ('gim-pi', 'labor-great'),                    # sorrow, toil, great labor
    'dahlua': ('dah-lua', 'weep-exceed'),                  # great sorrow, grief
    "pi'": ('pi', 'great'),                                # great (with apostrophe)
    'uhcin': ('uh-cin', 'PL-COND'),                        # conditional plural marker
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
    'zaza': ('zaza', 'ZAZA'),                  # hundreds
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
    'sawnsawn': ('sawn~sawn', 'talk~REDUP'),               # talk continuously, persecute
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
    'cici': ('ci~ci', 'say~REDUP'),                        # entreat, beg repeatedly
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
    'veh': ('veh', 'see'),                                 # see, visit
    'tomkha': ('tom-kha', 'cover-go'),                     # covered
    'langtuakah': ('lang-tuak-ah', 'side-each-LOC'),       # on each side
    'khuakulh': ('khua-kulh', 'town-wall'),                # city wall
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
    'thuahthuah': ('thuah~thuah', 'break~REDUP'),          # break repeatedly, breach upon breach
    'puanpi': ('puan-pi', 'cloth-great'),                  # robe, garment
    'tuamtuamin': ('tuam-tuam-in', 'various-REDUP-ERG'),   # in various ways, diversely
    'hawmpi': ('hawm-pi', 'arrange-great'),                # order, arrange properly
    'omthei': ('om-thei', 'exist-can'),                    # be possible, can be
    'kapkap': ('kap~kap', 'weep~REDUP'),                   # weep continually
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
    'nene': ('ne~ne', 'eat~REDUP'),                        # eat of, eating
    'thallawng': ('thal-lawng', 'bow-quiver'),             # quiver (for arrows)
    'keelhon': ('keel-hon', 'call-flock'),                 # fetch from flock
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
    'zuihtheih': ('zuih-theih', 'follow-ABIL'),             # able to follow
    'zintunna': ('zin-tun-na', 'journey-arrive-NMLZ'),     # stay, remain
    'zinling': ('zin-ling', 'journey-pass'),               # still small (voice)
    'zawhgawp': ('zawh-gawp', 'able-strike'),              # able to conquer
    'zanuam': ('za-nuam', 'hear-desire'),                  # desire to hear
    'zanthapai': ('zan-tha-pai', 'night-new-go'),          # wearisome nights
    'zam': ('zam', 'fear'),                                # fear, distress
    'veivei': ('vei~vei', 'time~REDUP'),                   # from time to time
    'vangikpi': ('vangik-pi', 'yoke-great'),               # grievous yoke
    'vailam': ('vai-lam', 'side-direction'),               # west side
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
    'theihsak': ('theih-sak', 'know.II-BENF'),             # know for (someone) - Form II + sak
    'tektek': ('tek~tek', 'bend~REDUP'),                   # bend (tongues)
    'teello': ('teel-lo', 'choose-NEG'),                   # not chosen
    'teelkhiat': ('teel-khiat', 'choose-away'),            # reject, forsake
    'tawldamna': ('tawl-dam-na', 'rest-well-NMLZ'),        # hope, security
    'tawikhaina': ('tawi-khai-na', 'weigh-balance-NMLZ'),  # balance, integrity
    'tangtunsak': ('tang-tun-sak', 'arrive-reach-CAUS'),   # hasten, bring to pass
    'taiina': ('tai-na', 'correct-NMLZ'),                  # chastening
    'sutpi': ('sut-pi', 'spoil-great'),                    # chief cornerstone
    
    # Round 70: High-frequency partials
    'nawizu': ('nawi-zu', 'firstfruit-bring'),             # firstfruits
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
    'naina': ('nai-na', 'near-NMLZ'),                      # battle, lying in wait
    'kumsim': ('kum-sim', 'year-count'),                   # yearly
    'sihsan': ('sih-san', 'die-leave'),                    # died (both)
    'maipuk': ('mai-puk', 'face-fall'),                    # fall on face
    'puato': ('pua-to', 'carry-up'),                       # fetch up
    'limcipen': ('lim-ci-pen', 'beauty-say-SUPRL'),        # best (vineyards)
    'bawngnote': ('bawng-no-te', 'cattle-young-PL'),       # calves
    'lingsa': ('ling-sa', 'fear-CAUS'),                    # trembled (elders)
    'puaksak': ('puak-sak', 'send-CAUS'),                  # send, laden
    'sihtheih': ('sih-theih', 'die-ABIL'),                  # can be killed
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
    'mattheih': ('mat-theih', 'grasp-ABIL'),                # able to catch
    'kibatna': ('ki-bat-na', 'REFL-trust-NMLZ'),           # trust
    'nul': ('nul', 'beast'),                               # beast
    'sinna': ('sin-na', 'sin-NMLZ'),                       # young/tender
    'kilamkikna': ('ki-lam-kik-na', 'REFL-build-ITER-NMLZ'), # rebuilding
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
    'suakkha': ('suak-kha', 'become-hard'),                # hardened
    'henna': ('hen-na', 'tie-NMLZ'),                       # bond, binding (Ps 2:3)
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
    'kankan': ('kan~kan', 'enquire~REDUP'),                   # sought out
    'sakpa': ('sak-pa', 'cause-AGT'),                      # one who makes
    'sumlepai': ('sum-le-pai', 'money-and-go'),            # ransom
    
    # Round 73: More high-frequency partials
    'muantheih': ('muan-theih', 'trust-ABIL'),              # directeth (way)
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
    'kelkel': ('kel~kel', 'doves~REDUP'),                  # doves' eyes
    'sawtpekin': ('sawt-pek-in', 'long-ago-ERG'),          # long ago
    'kisaktheihna': ('ki-sak-theih-na', 'REFL-make-ABIL-NMLZ'), # stay (on God)
    'masakna': ('ma-sak-na', 'self-cause-NMLZ'),           # first place (Shiloh)
    'hilhtel': ('hilh-tel', 'teach-understand'),           # understand
    'paulamin': ('pau-lam-in', 'speak-toward-ERG'),        # spoken to
    'kaihkhiat': ('kaih-khiat', 'lead-away'),              # loose (shoe)
    'nungtalai': ('nung-ta-lai', 'live-PFV-midst'),        # still living
    'anla': ('an-la', 'grain-harvest'),                    # seedtime and harvest
    'galdalna': ('gal-dal-na', 'war-equip-NMLZ'),          # armour
    'pangpi': ('pang-pi', 'side-great'),                   # four sides
    'hilhkholh': ('hilh-kholh', 'teach-INTENS'),            # testify/warn
    'silhpa': ('silh-pa', 'clothe-AGT'),                   # one clothed
    'huanna': ('huan-na', 'build-NMLZ'),                   # building
    'lungkimzo': ('lung-kim-zo', 'heart-full-COMPL'),      # satisfied
    'kongvang': ('kong-vang', 'way-empty'),                # grave's mouth
    'ngahzah': ('ngah-zah', 'get-measure'),                # treasure desired
    'piaknop': ('piak-nop', 'give-desire'),                # consecrate
    'minambup': ('min-am-bup', 'name-all-turn'),           # transgressions
    'muhnop': ('muh-nop', 'see-desire'),                   # prepare way
    'ngahthei': ('ngah-thei', 'get-can'),                  # ravening
    'sihkhawm': ('sih-khawm', 'die-together'),             # die with
    'nehcip': ('neh-cip', 'press-throng'),                 # throng, press
    'neutung': ('neu-tung', 'little-since'),               # since childhood
    'cihkhit': ('cih-khit', 'say-after'),                  # faith made whole
    'dingzia': ('ding-zia', 'stand-how'),                  # betray
    'nitawp': ('ni-tawp', 'day-end'),                      # last day
    'paitheih': ('pai-theih', 'go-ABIL'),                   # able to go
    'nekkhawmna': ('nek-khawm-na', 'eat-together-NMLZ'),   # communion
    
    # Round 74: More partials (2026-03-08)
    'cian': ('cian', 'light'),                             # light (Gen 1:3)
    'thukhente': ('thu-khen-te', 'word-judge-PL'),         # judges (Ex 21:6)
    'paubaan': ('pau-baan', 'speak-true'),                 # perfect (Gen 6:9)
    'khongkhai': ('khong-khai', 'magic-open'),             # diviner (Deut 18:14)
    'umgui': ('um-gui', 'be-gourd'),                       # gourd (Jonah 4:6)
    'khuan': ('khuan', 'dance'),                           # dance (Gen 31:27)
    'ngahzaw': ('ngah-zaw', 'get-more'),                   # more blessed (Deut 33:24)
    'khopa': ('khopa', 'tiller'),                          # tiller (Gen 4:2)
    'omden': ('om-den', 'be-always'),                      # always (Num 9:16)
    'omto': ('om-to', 'be-over'),                          # covered (Gen 7:20)
    'vaihawmte': ('vaihawm-te', 'imagine-PL'),             # those who imagine (Gen 11:6)
    'kimatna': ('ki-mat-na', 'REFL-train-NMLZ'),           # trained (Gen 14:14)
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
    'thuum': ('thuum', 'mourning'),                        # mourning (Gen 50:10)
    'naudomte': ('nau-dom-te', 'child-care-PL'),           # midwives (Ex 1:17)
    'hihkha': ('hih-kha', 'this-EMPH'),                    # lest (Ex 5:3)
    'mekna': ('mek-na', 'knead-NMLZ'),                     # kneading trough (Ex 8:3)
    'kaikhawmte': ('kai-khawm-te', 'gather-together-PL'),  # those gathered (Ex 16:18)
    'sansak': ('san-sak', 'prevail-CAUS'),                 # cause to prevail (Ex 17:11)
    'puakpih': ('puak-pih', 'carry-with'),                 # bear with (Ex 18:22)
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
    'apin': ('a-pin', '3SG-adversary'),                    # adversary (Matt 5:25)
    'mithagol': ('mitha-gol', 'giant-?'),                  # giant (2 Sam 21:18)
    'vankah': ('van-kah', 'sky-wizard'),                   # familiar spirit (Lev 20:6)
    'peuhpeuhte': ('peuh~peuh-te', 'any~REDUP-PL'),        # any/whatsoever (Lev 6:7)
    'gawhna': ('gawh-na', 'kill-NMLZ'),                    # place of killing (Lev 7:2)
    'khamvalte': ('kham-val-te', 'remain-fragment-PL'),    # fragments (Lev 8:32)
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
    'tawpun': ('tawp-un', 'end-EMPH'),                             # good/fat (Num 13:20)
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
    'bawltheih': ('bawl-theih', 'make-ABIL'),                   # make league (Josh 9:7)
    'khinmang': ('khin-mang', 'breath-all'),                   # any to breathe (Josh 11:11)
    'lungsimtak': ('lung-sim-tak', 'heart-think-true'),        # wholly followed (Josh 14:14)
    'zawhsa': ('zawh-sa', 'subdue-PERF'),                      # subdued (Josh 18:1)
    "tawpun": ('tawp-un', 'end-EMPH'),                         # final
    "beisakin,": ('bei-sak-in', 'pierce-CAUS-INST'),
    
    # Round 79: More partials (2026-03-08)
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
    'thukanpa': ('thukan-pa', 'messenger-NMLZ.M'),             # messenger (male)
    # More Round 80 entries
    'hihlo': ('hi-hlo', 'be-NEG'),                             # is not (contraction)
    'neihlam': ('neih-lam', 'have.II-manner'),                 # having, possession
    'ciangduai': ('ciangduai', 'rod'),                 # rod, scourge (punishment)
    'thulamlak': ('thu-lamlak', 'word-crooked'),               # crooked counsel
    'thulamlakpa': ('thu-lamlak-pa', 'word-crooked-NMLZ.M'),   # counsellor (wisdom)
    'khuanawl': ('khua-nawl', 'town-outskirts'),               # outskirts of town
    'thukawi': ('thu-kawi', 'word-crooked'),                   # perverse, froward
    'sawmsimin': ('sawmsim-in', 'conspire-INST'),              # conspiring
    # Round 81: KJV-verified vocabulary
    'tong': ('tong', 'tip'),                               # hinder end, way, path
    'ngap': ('ngap', 'cross'),                           # ferry, deck oneself
    'kawk': ('kawk', 'upright'),                   # morally upright, face
    'daupaina': ('daupai-na', 'prosper-NMLZ'),                 # prosperity
    'liahna': ('liah-na', 'dwell-NMLZ'),                       # dwelling place, secret place
    'leibatna': ('leibat-na', 'debt-NMLZ'),                    # creditor (debt claim)
    'leibatnapa': ('leibat-na-pa', 'debt-NMLZ-NMLZ.M'),        # creditor (person)
    'mittawtna': ('mittawt-na', 'blind-NMLZ'),                 # blindness
    'mittawt': ('mittawt', 'blind'),                           # blind
    'hinkiksak': ('hin-kik-sak', 'live-return-CAUS'),          # restore to life
    'phelkham': ('phel-kham', 'split-across'),                 # rip open
    'laktheih': ('lak-theih', 'take-ABIL'),                    # capture, seize
    'hingmat': ('hing-mat', 'alive-grasp'),                    # take alive, capture alive
    'sehkhatte': ('sehkhat-te', 'one.third-PL'),               # thirds, third parts
    'sehkhat': ('sehkhat', 'one.third'),                       # one third
    'satpukin': ('sat-puk-in', 'strike-down-INST'),            # smiting down
    'neuno': ('neu-no', 'small-DIM'),                          # small thing, trifle
    # Round 82: KJV-verified vocabulary
    'cilphuan': ('cil-phuan', 'spittle-foam'),                 # foam, let spittle fall
    'vanglianpa': ('vanglian-pa', 'almighty-NMLZ.M'),          # the Almighty
    'zahun': ('za-hun', 'hundred-time'),                       # might, all one's strength
    'semzaw': ('sem-zaw', 'serve-more'),                       # serve more
    'bukno': ('buk-no', 'ambush-DIM'),                         # watchtower, guardpost
    'hilhkholhnate': ('hilh-kholh-na-te', 'teach-INTENS-NMLZ-PL'),   # testimonies
    'heina': ('hei-na', 'mock-NMLZ'),                          # mockery, provocation
    'khankhit': ('khan-khit', 'grow-before'),                  # before growing up
    'kamsangnu': ('kamsang-nu', 'prophet-F'),                  # prophetess
    'genkholhsa': ('gen-kholh-sa', 'speak-INTENS-PRF'),          # prophesied
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
    'khasak': ('kha-sak', 'send-CAUS'),                        # cause to go, escort
    'khamseek': ('kham-seek', 'gold-smith'),                   # goldsmith
    'khamseekpa': ('kham-seek-pa', 'gold-smith-NMLZ.M'),       # goldsmith
    'sawlbuk': ('sawl-buk', 'leaf-booth'),                     # booth, tabernacle
    'gawpna': ('gawp-na', 'trample-NMLZ'),                     # trampling
    'dangtakna': ('dang-tak-na', 'thirst-ADV-NMLZ'),           # thirst
    'gentelna': ('gen-tel-na', 'speak-understand-NMLZ'),       # explanation, entrance
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
    'banzo': ('ban-zo', 'reach-ABIL'),                         # reach, attain
    'suksuk': ('suk~suk', 'DOWN~REDUP'),                          # continually push down
    'awle': ('awle', 'AWLE'),                             # leviathan, sea monster
    # Round 85: KJV-verified vocabulary
    'khinkhian': ('khin-khian', 'wait-INTENS'),                # wait, lie in wait
    'cimang': ('ci-mang', 'say-finish'),                       # desolate, perish
    'ngahnop': ('ngah-nop', 'get-want'),                       # desire to get, covet
    'hiat': ('hiat', 'cast.down'),                             # cast down, descend quickly
    'khapi': ('khapi', 'moon'),                                # moon
    'sinsen': ('sin-sen', 'clear~REDUP'),                      # clearly, plainly visible
    'seelna': ('seel-na', 'hide-NMLZ'),                        # hiding, concealment
    'lumletin': ('lumlet-in', 'overturn-INST'),                # overturning
    'omkhong': ('om-khong', 'exist-still'),                    # stand still, remain
    'hihzawh': ('hih-zawh', 'do-ABIL'),                        # able to do, capable
    'veva': ('ve-va', 'do-INTENS'),                            # do repeatedly, intensely
    'nungzang': ('nung-zang', 'back-part'),                    # back, loins
    # Round 86: KJV-verified vocabulary
    'ciim': ('ciim', 'mire'),                                  # mire, mud, deep water
    'vapite': ('vapi-te', 'stork-PL'),                         # storks
    'vapi': ('vapi', 'stork'),                                 # stork (bird)
    'tehpih': ('teh-pih', 'measure-compare'),                  # compare, liken
    'pakpak': ('pak~pak', 'quick~REDUP'),                      # quickly, suddenly
    'nainai': ('nai~nai', 'hour~REDUP'),                       # increasingly, continually
    'tautauna': ('tautau-na', 'groan-NMLZ'),                   # groaning, sighing
    'tautau': ('tau~tau', 'altar~REDUP'),                             # groan, sigh
    'biakpih': ('biak-pih', 'worship-also'),                   # worship along with
    'zawhsak': ('zawh-sak', 'able-CAUS'),                      # subdue, make subject
    'khuainun': ('khuainun', 'wax'),                           # wax (melting substance)
    # Round 87: KJV-verified vocabulary
    'kicinna': ('ki-cin-na', 'REFL-perfect-NMLZ'),             # integrity, perfection
    'kiliansakte': ('ki-lian-sak-te', 'REFL-great-CAUS-PL'),   # those who exalt themselves
    'kiliansak': ('ki-lian-sak', 'REFL-great-CAUS'),           # exalt oneself
    'geelgeel': ('geel~geel', 'plan~REDUP'),                   # ponder, meditate, devise
    'cihcih': ('cih~cih', 'say.NOM~REDUP'),                        # say repeatedly, continually say
    'thalpi': ('thal-pi', 'bow-great'),                        # bow (weapon)
    'kiuhkeuh': ('ki-uh-keuh', 'REFL-wash-INTENS'),            # thoroughly wash
    'siklukhu': ('sik-lukhu', 'iron-helmet'),                  # helmet, strength of head
    'minthannate': ('minthan-na-te', 'glory-NMLZ-PL'),         # glories, majesties
    'tehlop': ('teh-lop', 'measure-trap'),                     # trap, snare
    'hatpen': ('hat-pen', 'strong-most'),                      # strongest, mightiest
    'luituite': ('lui-tui-te', 'river-water-PL'),              # rivers, streams
    # Round 88: KJV-verified vocabulary
    'teelpa': ('teel-pa', 'choose-NMLZ.M'),                    # chosen one
    'paihsak': ('paih-sak', 'cast-CAUS'),                      # cast away, throw down
    'huihte': ('huih-te', 'wind-PL'),                          # winds
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
    'kihilhnate': ('ki-hilh-na-te', 'PASS-teach-NMLZ-PL'),     # instructions
    'kihilhna': ('ki-hilh-na', 'PASS-teach-NMLZ'),             # instruction
    'paikha': ('pai-kha', 'go-near'),                          # go near, approach
    'lumlum': ('lum~lum', 'sleep~REDUP'),                        # sleep deeply, slumber
    'thungaihsun': ('thu-ngaihsun', 'word-think'),             # understanding (variant)
    'awkpih': ('awk-pih', 'trap-APPL'),                        # be trapped, ensnared
    'teiteite': ('teitei-te', 'certain-PL'),                   # certainly (those who)
    'teitei': ('tei~tei', 'prudent~REDUP'),                           # certainly, surely
    'kipelhna': ('ki-pelh-na', 'REFL-escape-NMLZ'),            # escape, deliverance
    'kipel': ('ki-pelh', 'REFL-escape'),                       # escape
    'nektawm': ('nek-tawm', 'eat.II-little'),                  # food, something to eat
    # Round 90: Final push to 98.6%
    'haitatna': ('haitat-na', 'foolish-NMLZ'),                 # foolishness
    'haitat': ('haitat', 'foolish'),                           # foolish
    'ankuang': ('an-kuang', 'breast-bosom'),                   # bosom
    'thadahpa': ('thadah-pa', 'lazy-NMLZ.M'),                  # sluggard
    'thadah': ('thadah', 'lazy'),                              # lazy, slothful
    'hiathiat': ('hiat~hiat', 'clearly~REDUP'),                # clearly, wisely (speak)
    'thangsiahna': ('thangsiah-na', 'deceive-NMLZ'),           # deceit, snare
    'cikha': ('ci-kha', 'say-PROH'),                           # don't say (prohibitive)
    'zuihnop': ('zuih-nop', 'follow-want'),                    # want to follow
    'niamkhiatna': ('niamkhiat-na', 'humble-NMLZ'),            # humiliation, lowness
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
    'piantheih': ('pian-theih', 'happen-ABIL'),                # possible, can happen
    'hunhunin': ('hun-hun-in', 'time-time-INST'),              # every moment, constantly
    'khaukhai': ('khaukhai', 'plumbline'),                     # plumbline, measuring line
    'sasialne': ('sasial-ne', 'prey-NMLZ'),                    # predatory, ravenous
    'sasial': ('sasial', 'prey'),                              # prey, hunt
    # Round 92: Final push to 98.6%
    'niamin': ('niam-in', 'low-INST'),                         # lowly, humbly
    'beisakin': ('bei-sak-in', 'finish-CAUS-INST'),            # destroying, cutting off
    'sawkin': ('sawk-in', 'put.hand.into-INST'),               # reaching into, taking
    'sungte': ('sung-te', 'inside-PL'),                        # chambers, treasuries
    # Round 93: Final push to 98.6%
    'nuhsak': ('nuh-sak', 'apply-CAUS'),                       # apply (plaster)
    'khahkhiatna': ('khah-khiat-na', 'hold-out-NMLZ'),         # deliverance
    'paiziate': ('paizia-te', 'way-PL'),                       # ways
    'ipcip': ('ip-cip', 'restrain-INTENS'),                    # restrain oneself
    'zapsiang': ('zap-siang', 'winnow-clean'),                 # winnow, cleanse
    'mutna': ('mut-na', 'blow-NMLZ'),                          # alarm (trumpet)
    'siacip': ('sia-cip', 'spoil-INTENS'),                     # utterly spoiled
    'delhmang': ('delh-mang', 'chase-away'),                   # fray away, scare off
    'lungmangin': ('lungmang-in', 'dismay-INST'),              # dismayed
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
    'siathei': ('sia-thei', 'sin-ABIL'),                       # able to sin
    'thudawnna': ('thu-dawn-na', 'word-inquire-NMLZ'),         # inquiry, prophecy
    'leihoihna': ('lei-hoih-na', 'land-good-NMLZ'),            # good soil
    'khangcing': ('khang-cing', 'grow-complete'),              # fully grown
    'tamlawhna': ('tam-lawh-na', 'much-ABIL-NMLZ'),            # abundance
    'thudotin': ('thu-dot-in', 'word-inquire-INST'),           # inquiring
    'phelh': ('phelh', 'kindle'),                              # kindle fire
    'katna': ('kat-na', 'divide-NMLZ'),                        # division, parting
    'mote': ('mo-te', 'shame-PL'),                             # abominations
    'etet': ('et~et', 'care~REDUP'),                         # desire greatly
    'patausak': ('patauh-sak', 'shout-CAUS'),                  # cause to cry out
    'puanungah': ('puan-ung-ah', 'cloth-inside-LOC'),          # in the chamber
    'biakinntual': ('biakinn-tual', 'temple-court'),           # temple court
    'tehsuk': ('teh-suk', 'measure-knee'),                     # ankle deep
    # Round 95: More vocabulary
    'saki': ('sa-ki', 'animal-horn'),                          # horn, trumpet
    'ciamtehnate': ('ciamteh-na-te', 'waymark-NMLZ-PL'),       # waymarks
    'theihnop': ('theih-nop', 'know-ABIL'),                    # knowable, soothsayer
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
    'lutthei': ('lut-thei', 'enter-ABIL'),                     # able to enter
    'puanbek': ('puan-bek', 'cloth-piece'),                    # piece of cloth
    'thulang': ('thu-lang', 'word-reveal'),                    # reveal, make known
    'lingbulsum': ('lingbul-sum', 'thorn-three'),              # thorns (thick)
    'munuam': ('mun-uam', 'place-pleasant'),                   # pleasant place
    'cit': ('cit', 'eye'),                                     # eye (variant)
    'khenkhit': ('khen-khit', 'condemn-finish'),               # condemn
    'khohsa': ('khoh-sa', 'invite-NMLZ'),                      # invitation, bidding
    'luttheih': ('lut-theih', 'enter-ABIL'),                   # able to enter
    'kineihkhemna': ('ki-neih-khem-na', 'REFL-possess-all-NMLZ'), # hypocrisy
    'zakhin': ('za-khin', 'hundred-more'),                     # multitude
    'amauteng': ('amau-teng', '3PL-all'),                      # they themselves
    'sumpi': ('sum-pi', 'money-great'),                        # much money
    'nulsak': ('nul-sak', 'wet-CAUS'),                         # wash, wet
    'khahkhiat': ('khah-khiat', 'bind-out'),                   # loose, unbind
    'lakthei': ('lak-thei', 'take-ABIL'),                      # able to take
    'khentheih': ('khen-theih', 'judge-ABIL'),                 # authority to judge
    'laigelh': ('lai-gelh', 'writing-write'),                  # writings
    'thongcingte': ('thong-cing-te', 'prison-guard-PL'),       # prison keepers
    'nekloh': ('nek-loh', 'eat-NEG'),                          # abstain from
    'gamdaih': ('gam-daih', 'land-flat'),                      # open place
    'thahsawmna': ('thah-sawm-na', 'kill-plan-NMLZ'),          # lying in wait
    'sikkawipi': ('sikka-wi-pi', 'wind-blow-great'),           # strong wind
    'sikhin': ('sik-hin', 'dead-already'),                     # already dead
    'suakthei': ('suak-thei', 'become-ABIL'),                  # sanctified
    'pautheih': ('pau-theih', 'speak-ABIL'),                   # able to speak
    'cingtaaksak': ('cing-taak-sak', 'complete-true-CAUS'),    # fill completely
    'vankim': ('van-kim', 'sky-all'),                          # in the clouds
    'cingtaakin': ('cing-taak-in', 'complete-true-INST'),      # consecrated
    'nambat': ('nam-bat', 'name-number'),                      # number, count
    # Round 96: More vocabulary for 99%
    'bokvakte': ('bok-vak-te', 'creep-creature-PL'),           # creeping things
    'satak': ('sa-tak', 'flesh-piece'),                        # rib, piece of flesh
    'ngiansiam': ('ngian-siam', 'cunning-make'),               # subtil, crafty
    'kilangneihna': ('ki-lang-neih-na', 'REFL-appear-have-NMLZ'), # enmity
    'khangkhang': ('khang~khang', 'generation~REDUP'),           # exceedingly
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
    'khiathei': ('khiat-thei', 'interpret-ABIL'),              # interpreter
    'hoihlam': ('hoih-lam', 'good-side'),                      # good interpretation
    'khailum': ('khai-lum', 'hang-round'),                     # hanged
    'kihauh': ('ki-hauh', 'REFL-appoint'),                     # appoint
    'kikoihcing': ('ki-koih-cing', 'REFL-store-complete'),     # stored up
    'enen': ('en~en', 'look~REDUP'),                           # looking at each other
    'dotnate': ('dot-na-te', 'ask-NMLZ-PL'),                   # inquiries
    'nekkhawm': ('nek-khawm', 'eat-together'),                 # eating together
    'puakzawh': ('puak-zawh', 'fill-finish'),                  # filled up
    'dangteng': ('dang-teng', 'other-all'),                    # the rest, others
    'ciahkiksak': ('ciah-kik-sak', 'return-again-CAUS'),       # send back
    'thumantak': ('thu-man-tak', 'word-true-real'),            # truly, kindly
    'sattat': ('sat-tat', 'cut~REDUP'),                          # slew, killed
    'noptuak': ('nop-tuak', 'good-pleasant'),                  # pleasant, good
    'cihsak': ('cih-sak', 'say.II-BENF'),                      # say for (someone) - Form II + sak
    'khoisak': ('khoi-sak', 'call-CAUS'),                      # call to, summon
    'sapsak': ('sap-sak', 'suckle-CAUS'),                      # nurse
    'anthul': ('an-thul', 'grain-smitten'),                    # smitten grain
    'nekzah': ('nek-zah', 'eat-amount'),                       # eating portion
    # Note: sawlkhiat is Form II of sawlkhia, handled in VERB_STEM_PAIRS
    'lingcip': ('ling-cip', 'sorrow-INTENS'),                  # deep sorrow
    'vamimte': ('vamim-te', 'quail-PL'),                       # quails
    'khom': ('khom', 'place'),                                 # place, abide
    'paisuakzo': ('pai-suak-zo', 'go-out-ABIL'),               # able to go out
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
    'khamtheih': ('kham-theih', 'forbid-ABIL'),                # forbidden
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
    'behbeh': ('beh~beh', 'tribe~REDUP'),                      # number
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
    'ciangciang': ('ciang~ciang', 'morrow~REDUP'),              # completely
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
    'sawltheih': ('sawl-theih', 'send-ABIL'),                  # able to send
    'leengkai': ('leeng-kai', 'yoke-pull'),                    # yoke of oxen
    'hamu': ('hamu', 'file'),                                  # file (tool)
    'ciangka': ('ciang-ka', 'way-edge'),                       # passage
    'zuito': ('zui-to', 'follow-up'),                          # come up
    'vattuk': ('vat-tuk', 'climb-up'),                         # climbed up
    'muaimuai': ('muai~muai', 'melt~REDUP'),                   # melted away
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
    'geelkholhsa': ('geel-kholh-sa', 'plan-INTENS-PRF'),        # prepared/formed
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
    'suktheih': ('suk-theih', 'break-ABIL'),                   # persecute
    'thamante': ('tha-man-te', 'labor-true-PL'),               # labours
    'cihtheih': ('cih-theih', 'say-ABIL'),                     # sufficiency
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
    'velvel': ('vel~vel', 'around~REDUP'),                       # hold peace
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
    'citheisakkik': ('ci-thei-sak-kik', 'return-ABIL-CAUS-again'), # turned captivity
    'siamang': ('siam-ang', 'make-wisdom'),                    # be wise
    'leengtui': ('leeng-tui', 'corn-wine'),                    # corn and wine
    'thahnopna': ('thah-nop-na', 'kill-like-NMLZ'),            # deceitful
    'kibawlphat': ('ki-bawl-phat', 'REFL-make-ready'),         # made ready
    'lelna': ('lel-na', 'fear-NMLZ'),                          # fear
    'kihotkhiatna': ('ki-hot-khiat-na', 'REFL-deliver-out-NMLZ'), # deliverance
    'phattaak': ('phat-taak', 'praise-worthy'),                # worthy of praise
    'zamin': ('za-min', 'hundred-thousand'),                   # many
    'lungmuan': ('lung-muan', 'heart-secure'),                 # secure heart
    'kikoko': ('ki-ko-ko', 'REFL-cry~REDUP'),                  # cried out
    'khuailuzu': ('khuai-lu-zu', 'honey-head-sweet'),          # honeycomb
    'dingtang': ('ding-tang', 'stand-upright'),                # stand upright
    'lungno': ('lungno', 'worm'),                              # opaque lexeme, not lung+no
    'khasia': ('kha-sia', 'face-hide'),                        # hide face
    'khuisatna': ('khui-sat-na', 'sigh-NMLZ'),                 # sighing
    'tuithukpite': ('tui-thuk-pi-te', 'water-deep-great-PL'),  # deep waters
    'mitheek': ('mik-heek', 'eye-fold'),                        # wink/beckon (fold eyelid)
    'tawnna': ('tawn-na', 'reproof-NMLZ'),                     # reproofs
    'gentham': ('gen-tham', 'speak-hand'),                     # handbreadth
    'nuihsatin': ('nuih-sat-in', 'reproach-NMLZ-INST'),        # reproach
    'vuakna': ('vuak-na', 'blow-NMLZ'),                        # blow, stroke
    'lungnop': ('lung-nop', 'heart-rest'),                     # recover
    'khakunkun': ('kha-kun-kun', 'face-cast.down~REDUP'),      # cast down
    'tuizeu': ('tui-zeu', 'water-deep'),                       # deep water
    'khangualte': ('khan-gual-te', 'time-fellow-PL'),          # fellows
    'ciangkik': ('ciang-kik', 'good-again'),                   # good pleasure
    'keutumsak': ('keu-tum-sak', 'melt-finish-CAUS'),          # melt away
    'sikcipsak': ('sik-cip-sak', 'tread-INTENS-CAUS'),         # tread down
    'guhngek': ('guh-ngek', 'bless-long'),                     # bless while live
    'gallauna': ('gal-lau-na', 'enemy-fear-NMLZ'),             # fear of enemy
    'kuakte': ('kuak-te', 'furrow-PL'),                        # furrows
    'zaktheih': ('zak-theih', 'hear-ABIL'),                    # gave ear
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
    'muamua': ('mua~mua', 'many~REDUP'),                       # innumerable
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
    'hiuhiau': ('hiu-hiau', 'black~REDUP'),                    # black
    'biang': ('biang', 'cheek'),                               # cheeks
    'suknawi': ('suk-nawi', 'break-charge'),                   # charge, adjure
    'sakhitalno': ('sakhital-no', 'hart-young'),               # young hart
    'itluat': ('it-luat', 'love-exceed'),                      # my love
    'nard': ('nard', 'spikenard'),                             # spikenard
    'kiuh': ('kiuh', 'knock'),                                 # knock
    'pona': ('po-na', 'garden-NMLZ'),                          # garden bed
    'phelhzo': ('pelh-zo', 'quench-ABIL'),                     # able to quench
    'lingsakgawp': ('ling-sak-gawp', 'shake-CAUS-INTENS'),     # shake terribly
    'theihkim': ('theih-kim', 'know-all'),                     # famous, renown
    'etsuk': ('et-suk', 'look-down'),                          # look unto
    # Round 103: More vocabulary for 99%
    'veilama': ('vei-lam-a', 'left-side-LOC'),                 # on the left
    'sinsan': ('sin-san', 'shake~REDUP'),                      # shake hand
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
    'zakzak': ('zak~zak', 'proclaim~REDUP'),                       # cry out
    'khutsiampa': ('khut-siam-pa', 'hand-make-NMLZ'),          # craftsman
    'awngthawl': ('awng-thawl', 'create-establish'),           # established
    'uang': ('uang', 'lavish'),                                # lavish
    'tungvat': ('tung-vat', 'upon-fall'),                      # fall upon
    'lausakzo': ('lau-sak-zo', 'fear-CAUS-ABIL'),              # able to prevail
    'hihlohna': ('hih-loh-na', 'this-NEG-NMLZ'),               # treachery
    'tengsakkik': ('teng-sak-kik', 'establish-CAUS-again'),    # establish again
    'kimakna': ('ki-mak-na', 'REFL-divorce-NMLZ'),             # divorcement
    'kapte': ('kap-te', 'shoot-PL'),                           # shooters
    'silhlo': ('silh-lo', 'clothe-NEG'),                       # not clothe
    'thumthum': ('thum~thum', 'mourn~REDUP'),                  # mourn sore
    'neupente': ('neu-pen-te', 'small-most-PL'),               # smallest
    'kepsak': ('kep-sak', 'feed-CAUS'),                        # feed flocks
    'suhna': ('suh-na', 'robbery-NMLZ'),                       # robbery
    'gamlakpi': ('gam-lak-pi', 'land-middle-great'),           # wilderness
    'mutin': ('mut-in', 'blow-INST'),                          # blowing
    'awlmawh': ('awl-mawh', 'rest-without'),                   # without rest
    'lopite': ('lopi-te', 'harlot-PL'),                        # harlots
    'theigahte': ('thei-gah-te', 'fig-tree-PL'),               # fig trees
    'kantanzo': ('kan-tan-zo', 'bound-stand-ABIL'),            # bound
    'keei': ('keei', 'shadow'),                                # shadow
    'sapsap': ('sap~sap', 'call~REDUP'),                      # speaking
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
    'genkholhnate': ('gen-kholh-na-te', 'speak-INTENS-NMLZ-PL'),  # prophecies
    'sumzuak': ('sum-zuak', 'money-buy'),                      # buyer
    'mindaihuai': ('min-dai-huai', 'eye-far-mix'),             # far off
    'paikhiatlam': ('pai-khiat-lam', 'go-out-direction'),      # removing
    'apte': ('ap-te', 'talent-PL'),                            # talents
    'utbang': ('ut-bang', 'think-like'),                       # think like
    'zialzial': ('zial~zial', 'uncover~REDUP'),                  # sharpened
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
    'ngakngak': ('ngak~ngak', 'wait~REDUP'),                   # suddenly come
    'kekseu': ('kek-seu', 'corrupt-moth'),                     # moth corrupt
    'nattunin': ('nat-tun-in', 'sick-enter-INST'),             # sick
    'siahdong': ('siah-dong', 'sin-person'),                   # sinners
    # Round 105: More vocabulary for 99%
    'siavuan': ('sia-vuan', 'sick-heal'),                      # physician
    'diamdiam': ('diam~diam', 'still~REDUP'),                  # reed shaken
    'cingteng': ('cing-teng', 'complete-all'),                 # about (number)
    'ninsakthei': ('nin-sak-thei', 'defile-CAUS-ABIL'),        # defile
    'suplawhte': ('sup-lawh-te', 'save-ABIL-PL'),              # those who save
    'cihnate': ('cih-na-te', 'command-NMLZ-PL'),               # commandments
    'zuihsa': ('zuih-sa', 'keep-PAST'),                        # have kept
    'hihthei': ('hih-thei', 'this-ABIL'),                      # possible
    'sumbukah': ('sum-buk-ah', 'money-place-LOC'),             # marketplace
    'piakzah': ('piak-zah', 'give-amount'),                    # give as much
    'khawhlawh': ('khawh-lawh', 'let-ABIL'),                   # let out
    'zangmang': ('zang-mang', 'devour-scatter'),               # devour
    'saupipi': ('sau-pi-pi', 'long-great~REDUP'),              # long prayer
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
    'khawhlawhsak': ('khawh-lawh-sak', 'let-ABIL-CAUS'),       # let out
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
    'piangthei': ('piang-thei', 'come-ABIL'),                  # cometh
    'zote': ('zo-te', 'able-PL'),                              # those who allow
    'lungnemna': ('lung-nem-na', 'heart-soft-NMLZ'),           # meekness
    'zangthei': ('zang-thei', 'power-ABIL'),                   # have power
    'nethei': ('ne-thei', 'eat-ABIL'),                         # able to eat
    'thuakkhak': ('thuak-khak', 'suffer-into'),                # condemnation
    'sepzawh': ('sep-zawh', 'work-finish'),                    # sufficient
    'puatham': ('puat-ham', 'glory-occasion'),                 # occasion to glory
    'pawlkhatin': ('pawl-khat-in', 'group-one-INST'),          # ambassadors
    'kinna': ('kin-na', 'clear-NMLZ'),                         # clearing
    'huhnopna': ('huh-nop-na', 'exhort-like-NMLZ'),            # exhortation
    'lunggimpih': ('lung-gim-pih', 'heart-care-with'),         # care
    'sansa': ('san-sa', 'before-PAST'),                        # before
    'hilhtheih': ('hilh-theih', 'teach-ABIL'),                 # traditions
    'nasemkhawm': ('nasem-khawm', 'servant-together'),        # fellowship
    'thutakte': ('thu-tak-te', 'word-true-PL'),                # truth
    'genbelin': ('gen-bel-in', 'speak-about-INST'),            # whereof we speak
    'kikhulna': ('ki-khul-na', 'REFL-cast-NMLZ'),              # cast
    # Round 107: More vocabulary for 99% (count=2)
    'limlemel': ('lim-le-mel', 'form-NEG-void'),               # without form
    'singnai': ('sing-nai', 'tree-precious'),                  # tree resin = bdellium (transparent)
    'nakguh': ('nak-guh', 'rib-take'),                         # took rib
    'kipiansakna': ('ki-pian-sak-na', 'REFL-create-CAUS-NMLZ'), # creation
    'minthangte': ('min-thang-te', 'name-famous-PL'),          # men of renown
    'piansaksa': ('pian-sak-sa', 'create-CAUS-PAST'),          # have created
    'khaknelh': ('khak-nelh', 'shut-close'),                   # shut in
    'guahte': ('guah-te', 'window-PL'),                        # windows
    'kiamkiam': ('kiam~kiam', 'abate~REDUP'),                  # abated
    'sabengpa': ('sa-beng-pa', 'hunt-mighty-NMLZ'),            # mighty hunter
    'bawlnasa': ('bawl-na-sa', 'make-NMLZ-PAST'),              # had made
    'tawsawte': ('taw-saw-te', 'plain-oak-PL'),                # plains
    'behpa': ('beh-pa', 'clan-male'),                          # kinsman/brother (KJV verified)
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
    'neihsak': ('neih-sak', 'have.II-BENF'),                   # have for (someone) - Form II + sak
    'mahmahsa': ('mah-mah-sa', 'self-REDUP-PAST'),             # themselves
    'bangtungzawl': ('bang-tung-zawl', 'door-above-post'),     # upper door post
    'talsuante': ('tal-suan-te', 'forehead-mark-PL'),          # frontlets
    'tangciak': ('tang-ciak', 'entangle-trap'),                # entangled
    'khenkham': ('khen-kham', 'divide-hold'),                  # divide
    'nannan': ('nan~nan', 'manna~REDUP'),                      # manna
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
    # banbulhte now handled by BINARY_COMPOUNDS as ban-bulh (arm-bind = bracelet)
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
    'saksak': ('sak~sak', 'cause~REDUP'),                   # made atonement
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
    # 'kiimnai': see line ~10850 (neighboring/surrounding)
    'hehsa': ('heh-sa', 'angry-PRF'),                            # anger kindled
    # 'hutna': see line ~9453
    'kiimcip': ('ki-im-cip', 'REFL-destroy-INTENS'),           # utterly
    'louih': ('lo-uih', 'garlic-leek'),                        # leeks
    'hawkkhia': ('hawk-khia', 'strip-out'),                    # stripped off
    'kigaih': ('ki-gaih', 'REFL-chew'),                        # chewed
    'liaktum': ('liak-tum', 'lick-up'),                        # lick up
    'dawhsa': ('dawh-sa', 'draw-PAST'),                        # drawn
    'sungtum': ('sung-tum', 'inside-ask'),                     # ask counsel
    'phulapa': ('phula-pa', 'avenger-NMLZ'),                   # avenger
    'kimaituahin': ('ki-mai-tuah-in', 'REFL-face-do-INST'),    # face to face
    'tamvei': ('tam-vei', 'many-stripes'),                     # many stripes
    'kinengniamin': ('ki-neng-niam-in', 'REFL-grope-feel-INST'), # groping
    'kikzo': ('kik-zo', 'again-ABIL'),                         # rise again
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
    'thahloh': ('thah-loh', 'slay-NEG'),                       # slay not
    'galphualah': ('gal-phual-ah', 'battle-place-LOC'),        # to battle
    'tuukhawk': ('tuu-khawk', 'sheep-cote'),                   # sheepcote
    'phawktel': ('phawk-tel', 'perceive-know'),                # perceived
    'hepkhiat': ('hep-khiat', 'depart-out'),                   # depart away
    'madawkin': ('ma-dawkin', 'that-reason'),                  # wherefore
    'tawmlua': ('tawm-lua', 'little-too'),                     # too little
    'zongzaw': ('zong-zaw', 'more~REDUP'),                      # how much more
    'taisuk': ('tai-suk', 'cross-over'),                       # went over
    'kilinggawp': ('ki-ling-gawp', 'REFL-shake-INTENS'),       # shook terribly
    'sugawpzo': ('su-gawp-zo', 'leap-INTENS-ABIL'),            # leaped over
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
    'tul': ('tul', 'thousand'),                                    # on foot
    'pipi': ('pi~pi', 'cubit~REDUP'),                          # to grind
    'gal': ('gal', 'enemy'),                               # enemy/war (not 'little')
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
    'meigongnu': ('meigong-nu', 'widow-F'),                    # widow (mei 'female' TB *mei)
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
    'leen': ('leen', 'fly'),                                   # fly (Job 5:7 sparks fly upward)
    'kihencip': ('ki-hen-cip', 'REFL-tie-INTENS'),             # bound tightly
    'kihencipna': ('ki-hen-cip-na', 'REFL-tie-INTENS-NMLZ'),   # bondage
    'kihenna': ('ki-hen-na', 'REFL-tie-NMLZ'),                 # bands/bonds (Isa 52:2, Jer 2:20)
    'kihente': ('ki-hen-te', 'REFL-tie-PL'),                   # bonds (plural)
    'kihennate': ('ki-hen-na-te', 'REFL-tie-NMLZ-PL'),         # bonds (plural)
    'taangzaw': ('taang-zaw', 'clear-more'),                   # clearer
    'bulsum': ('bul-sum', 'root-stock'),                       # stock/root
    'kigimsak': ('ki-gim-sak', 'REFL-remove-CAUS'),            # removed
    'kitunpih': ('ki-tun-pih', 'REFL-root-out'),               # rooted out
    'git': ('git', 'bound'),                                   # bounds
    'kileizo': ('ki-lei-zo', 'REFL-get-ABIL'),                 # cannot be gotten
    'hawkguam': ('hawk-guam', 'cliff-cave'),                   # caves/cliffs
    'lato': ('la-to', 'drop-small'),                           # drops
    'khihcip': ('khih-cip', 'hide-INTENS'),                    # hide in dust
    'kihihsakpih': ('ki-hih-sak-pih', 'REFL-remember-CAUS-with'), # trust in
    'kidikdik': ('ki-dik-dik', 'REFL-bow~REDUP'),              # bowed down
    'gawisan': ('gawi-san', 'mock-feast'),                     # mockers in feasts
    'kisosuah': ('ki-so-suah', 'REFL-stir-up'),                # stir up
    'thokikzo': ('tho-kik-zo', 'rise-again-ABIL'),             # rise up again
    'kigual': ('ki-gual', 'REFL-entreat'),                     # entreat favour
    'kihai': ('ki-hai', 'REFL-approve'),                       # approve
    'gulpi': ('gul-pi', 'serpent-great'),                      # serpent
    'sungsuk': ('sung-suk', 'inside-pour'),                    # pour out
    'kikumkum': ('ki-kum-kum', 'REFL-counsel~REDUP'),          # take counsel
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
    'kiphawkphawk': ('ki-phawk-phawk', 'REFL-remember~REDUP'), # memory blessed
    'nguntang': ('ngun-tang', 'silver-choice'),                # choice silver
    'leenmang': ('leen-mang', 'whirlwind-pass'),               # whirlwind passeth
    'kipuk': ('ki-puk', 'REFL-fall'),                          # people fall
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
    'taisanzo': ('tai-san-zo', 'hold-water-ABIL'),             # hold water
    'suam': ('suam', 'pollute'),                               # polluted
    'koici': ('koi-ci', 'how-pardon'),                         # how pardon
    'kipaithang': ('ki-pai-thang', 'REFL-scatter-field'),      # fall as
    'teeng': ('teeng', 'linen'),                               # linen
    'kilehngat': ('ki-leh-ngat', 'REFL-depart-heart'),         # heart depart
    'kipaidak': ('ki-pai-dak', 'REFL-cast-heat'),              # cast out
    'huhzo': ('huh-zo', 'breath-ABIL'),                        # breath taken
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
    'napi': ('napi', 'but'),                       # distress
    'khangsimna': ('khang-sim-na', 'generation-divide-NMLZ'),  # generations
    'simna': ('sim-na', 'count-NMLZ'),                         # numbered
    'note': ('note', '2PL.PRO'),                               # you
    'sangna': ('sang-na', 'high-NMLZ'),                        # high places
    'ancilna': ('an-cil-na', 'corn-thresh-NMLZ'),              # threshingfloor
    'omlai': ('om-lai', 'rest-still'),                         # rest
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
    'inndei': ('inn-dei', 'house-chamber'),                    # chamber
    'hehpihna': ('heh-pih-na', 'favor-with-NMLZ'),             # favour
    'siampi': ('siam-pi', 'priest-great'),                     # priest
    'sihna': ('sih-na', 'blood-NMLZ'),                         # blood/life
    'koihna': ('koih-na', 'set-NMLZ'),                         # set over
    'kisa': ('ki-sa', 'REFL-PAST'),                            # grieved
    'ngaihsutna': ('ngaih-sut-na', 'think-NMLZ'),              # thoughts
    'thukhenna': ('thu-khen-na', 'word-judge-NMLZ'),           # judge
    'suksiatna': ('suk-siat-na', 'destroy-NMLZ'),              # destruction
    'kidona': ('ki-do-na', 'REFL-fight-NMLZ'),                    # battle/warfare
    'sumkholna': ('sum-khol-na', 'silver-treasure-NMLZ'),      # treasuries
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
    'kizem': ('ki-zem', 'REFL-twine'),                         # twined
    # Round 116: Common word+suffix combinations
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
    'tanglaiin': ('tang-lai-in', 'ancient-NMLZ-INST'),         # ancient INST
    'puanak': ('puan-ak', 'cloth-put'),                        # clothe
    'paaiahaah': ('paai-ah', 'place-LOC'),                     # place LOC
    'sumzuaknaah': ('sum-zuak-na-ah', 'money-sell-NMLZ-LOC'),  # merchandise LOC
    # Round 118: More suffix combinations and partials
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
    'hilhkholhnain': ('hilh-kholh-na-in', 'teach-INTENS-NMLZ-ERG'),  # testimony ERG
    'laimal': ('lai-mal', 'book-plain'),                       # plain book
    'guktakna': ('guk-tak-na', 'good-true-NMLZ'),              # goodness
    'deihnaun': ('deih-na-un', 'want-NMLZ-3PL'),               # want
    'upnaah': ('up-na-ah', 'believe-NMLZ-LOC'),                # believe LOC
    'luppihin': ('lup-pih-in', 'roll-with-INST'),              # roll INST
    'piangkhiain': ('piang-khia-in', 'born-out-INST'),         # born INST
    'nuiin': ('nui-in', 'laugh-INST'),                         # laugh INST
    'topain': ('topa-in', 'lord-INST'),                        # lord INST
    'thuakzoin': ('thuak-zo-in', 'endure-ABIL-INST'),          # endure INST
    # Round 120: More vocabulary and suffix forms
    'semsemna': ('sem-sem-na', 'hate-REDUP-NMLZ'),             # hated more
    'kapsain': ('kap-sa-in', 'mourn-PAST-INST'),               # mourning INST
    'luahnaah': ('luah-na-ah', 'issue-NMLZ-LOC'),              # issue LOC
    'nekneknain': ('nek-nek-na-in', 'eat-REDUP-NMLZ-INST'),    # eating INST
    'buknaah': ('buk-na-ah', 'shelter-NMLZ-LOC'),              # shelter LOC
    'sapnain': ('sap-na-in', 'stretch-NMLZ-INST'),             # stretch INST
    'khauhsakin': ('kauh-sak-in', 'harden-CAUS-INST'),         # harden INST
    'sianthonaah': ('sian-tho-na-ah', 'holy-rise-NMLZ-LOC'),   # holiness LOC
    'kihtakhuaiin': ('kih-takhuai-in', 'fierce-mix-INST'),     # phonotactic fix (no ht cluster)
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
    'kidemnaah': ('ki-dem-na-ah', 'REFL-condemn-NMLZ-LOC'),    # condemn LOC
    'zonnain': ('zon-na-in', 'seek-NMLZ-INST'),                # seeking INST
    'khusain': ('khu-sa-in', 'feast-PAST-INST'),               # feast INST
    'kheun': ('khe-un', 'leg-3PL'),                            # legs
    'ganun': ('gan-un', 'bear-3PL'),                           # bear 3PL
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
    'nasepsa': ('nasep-sa', 'work-PAST'),                 # thy labours
    'nemang': ('ne-mang', 'locust-consume'),                   # locust consume
    'cinatnate': ('ci-nat-na-te', 'sick-NMLZ-PL'),             # sicknesses
    'hintheih': ('hin-theih', 'live-ABIL'),                    # may live
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
    'tuangte': ('tuang-te', 'chariot-PL'),                     # chariots
    'kikhaite': ('ki-khai-te', 'REFL-hang-PL'),                # hangings
    'thatte': ('that-te', 'kill-PL'),                          # killed PL
    'tanaute': ('ta-nau-te', 'child-small-PL'),                # children PL
    'zawthin': ('zawn', 'north'),                              # northward
    'kipna': ('kip-na', 'confirm-NMLZ'),                       # confirm
    'sawmnihte': ('sawm-nih-te', 'ten-two-PL'),                # twenty PL
    'saang': ('saang', 'basket'),                              # basket
    # Round 124: More narrative vocabulary
    'khanghamte': ('khang-ham-te', 'generation-old-PL'),       # old ones
    'sawmnih': ('sawm-nih', 'ten-two'),                        # twenty
    'giahphual': ('giah-phual', 'carry-pass'),                 # pass over
    'giahphualate': ('giah-phual-a-te', 'carry-pass-NOM-PL'),  # passed over PL
    'valhtumin': ('valh-tum-in', 'swallow-COMPL-INST'),        # swallow up INST
    'muhdahhuaiin': ('muh-dah-huai-in', 'smell-bad-hateful-INST'),  # stink INST
    'nesakin': ('ne-sak-in', 'eat-CAUS-INST'),                 # eating INST
    'semsemnain': ('sem-sem-na-in', 'divide-REDUP-NMLZ-INST'), # by themselves INST
    # Round 127: Additional compound fixes
    'tenglai': ('teng-lai', 'dwell-time'),                      # dwelling time
    'notkik': ('not-kik', 'push-ITER'),                         # force/push repeatedly
    'paisuksak': ('pai-suk-sak', 'go-descend-CAUS'),            # force down
    'hilhkholhsa': ('hilh-kholh-sa', 'teach-INTENS-PRF'),         # testified/warned
    'veikhoi': ('vei-khoi', 'cry.out-call'),                    # cry out
    'puannuai': ('puan-nuai', 'cloth-under'),                   # under raiment
    'khaknelhin': ('khak-nel-hin', 'shut-door-DECL'),           # shut/locked
    'nawtsuak': ('nawt-suak', 'sweep-away'),                    # sweep away
    'satkhamin': ('sat-kham-in', 'smite-pierce-INST'),          # smite through
    'satui': ('sa-tui', 'meat-broth'),                          # broth
    'dinglai': ('ding-lai', 'stand-time'),                      # standing time
    'sukkhia': ('suk-khia', 'wring-out'),                       # wring out
    'simsuk': ('sim-suk', 'count-down'),                        # go down to count
    'thumun': ('thu-mun', 'word-blow'),                         # trumpet (blow)
    'kipahtawina': ('ki-pah-tawi-na', 'REFL-honor-NMLZ'),       # honor
    'kigalneihna': ('ki-gal-neih-na', 'REFL-enemy-have-NMLZ'),  # enmity
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
    'naseppihte': ('nasep-pih-te', 'work-APPL-PL'),        # workers
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
    'biaktheih': ('biak-theih', 'worship-ABIL'),                # able to worship
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
    'lotte': ('lot-te', 'cast-PL'),                             # (things) cast/shot - in "thaltang lotte" = arrows shot
    'kilate': ('kila-te', 'portion-PL'),                        # portions (spoil)
    'vankahte': ('van-kah-te', 'go.and-go-PL'),                 # familiar spirits
    'vankahthei': ('van-kah-thei', 'go.and-go-ABIL'),           # has familiar spirit
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
    'hoihhoih': ('hoih~hoih', 'be.good~REDUP'),                    # safely/well
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
    'hunhun': ('hun~hun', 'time~REDUP'),                        # continually
    'paipihtoh': ('pai-pih-toh', 'go-APPL-with'),               # bring up with
    'gentaak': ('gen-taak', 'speak-firmly'),                    # strangers (few)
    'kidoksa': ('ki-dok-sa', 'REFL-draw-NMLZ'),                 # drawn sword
    'ziahziah': ('ziah~ziah', 'willing~REDUP'),                 # willingly
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
    # Round 142: More partial fixes
    'tutna': ('tut-na', 'sleep-NMLZ'),                          # bed/lying place
    'sagihna': ('sagih-na', 'seven-NMLZ'),                      # seventh
    'zanpi': ('zan-pi', 'night-big'),                           # in the night
    'zuazuate': ('zuazua-te', 'willing-PL'),                    # freewill offerings
    'namcin': ('nam-cin', 'nation-say'),                        # salutation
    'khuak': ('khu-ak', 'bed-place'),                           # sepulchre/bed
    # Round 143: Suffix forms
    'cianna': ('cian-na', 'announce-NMLZ'),                     # indignation/announcement
    'khuamialna': ('khua-mial-na', 'town-dark-NMLZ'),           # darkness
    'cingh': ('cing-h', 'lend-COMP'),                           # surely lend
    'muanhuai': ('muan-huai', 'trust-full'),                    # gathered cattle
    'khinta': ('khin-ta', 'move-NMLZ'),                         # given
    'ngakngakna': ('ngak-ngak-na', 'wait-REDUP-NMLZ'),          # waiting
    # Round 144: Unknown fixes (duplicates removed - see earlier entries)
    # 'lamna': see line ~8361
    # 'kiimnai': see line ~10850
    # 'hehsa': see line ~12541
    # 'hutna': see line ~9453
    'khimsakin': ('khim-sak-in', 'crown-CAUS-INST'),            # put crown
    'kimawlsak': ('ki-mawl-sak', 'REFL-mock-CAUS'),             # made sport
    'ngunseek': ('ngun-seek', 'silver-forge'),                  # founder (silversmith)
    'otsan': ('ot-san', 'cry-voice'),                           # aileth
    'lanluat': ('lan-luat', 'show-fold'),                       # lewdness
    'dahmai': ('dah-mai', 'sad-face'),                          # sad countenance
    # Round 145: High-frequency partial fixes
    '-': ('~', 'PUNCT'),                                        # 110x - em dash punctuation
    'mangpa': ('mang-pa', 'chief-father'),                      # 7x - chief captain
    "mangpa'": ("mang-pa'", 'chief-father.POSS'),               # 7x - chief's
    'lamna-a': ('lam-na-a', 'build-NMLZ-LOC'),               # 6x - "in the building" (all contexts are building)
    'kiimnai-a': ('ki-im-nai-a', 'REFL-stay-near-LOC'),         # 6x - at neighboring place
    'hehsa-in': ('heh-sa-in', 'angry-NMLZ-ERG'),                # 6x - with anger
    'eh': ('eh', 'INTERJ'),                                     # 5x - interjection
    'oh': ('oh', 'INTERJ'),                                     # 2x - interjection (Exo 4:10,13)
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
    "thahatte'": ('tha-hat-te', 'strength-strong-PL.POSS'),      # 3x - mighty ones'
    "tupa'": ('tu-pa', 'grandson-M.POSS'),                       # 3x - grandson's
    "meigongnu'": ('meigong-nu', 'widow-F.POSS'),                # 3x - widow's (mei 'female' TB *mei)
    "kilin'": ('ki-lin', 'REFL-shake.POSS'),                     # 3x - quaking's
    'kiling': ('ki-ling', 'REFL-shake'),                         # quaked
    'khe-a': ('khe-a', 'foot-LOC'),                              # 3x - at foot
    "gulpi'": ('gul-pi', 'serpent-big.POSS'),                    # 3x - serpent's
    "kiphasakte'": ('ki-pha-sak-te', 'REFL-good-CAUS-PL.POSS'),  # 3x - saved ones'
    "thahatpa'": ('tha-hat-pa', 'strength-strong-M.POSS'),       # 3x - mighty man's
    # Round 147: More 2x partial fixes
    'gan-an': ('gan-an', 'possess-ERG'),                         # 5x - possessions (substance)
    'lam-an': ('lam-an', 'way-ERG'),                              # 5x - way/direction 
    "sungpa'": ('sung-pa', 'inside-M.POSS'),                      # 2x - father-in-law's
    'sungpa': ('sung-pa', 'inside-M'),                            # father-in-law
    "kopte'": ('kop-te', 'frog-PL.POSS'),                         # 2x - frogs'
    "gukte'": ('guk-te', 'lice-PL.POSS'),                         # 2x - lice's
    "lite'": ('li-te', 'river-PL.POSS'),                          # 2x - rivers'
    "sun'": ('sun', 'day.POSS'),                                  # 2x - day's
    'mongte-ah': ('mong-te-ah', 'throat-PL-LOC'),                 # 2x - at throats/necks
    'li-a': ('li-a', 'river-LOC'),                                # 2x - at river/four
    "phakpa'": ('phak-pa', 'able-M.POSS'),                        # 2x - able one's
    "suante-a'": ('suan-te-a', 'descendant-PL-LOC.POSS'),         # 2x - descendants' place
    "lehpan'": ('leh-pan', 'change-side.POSS'),                   # 2x - change's
    "tecite'": ('teci-te', 'witness-PL.POSS'),                    # 2x - witnesses'
    "peuhpeuhte'": ('peuh-peuh-te', 'every-REDUP-PL.POSS'),       # 2x - everyone's
    "tuutalte'": ('tuu-tal-te', 'flock-POSS-PL.POSS'),            # 2x - flocks'
    'tau-a': ('tau-a', 'spear-LOC'),                              # 2x - at spear
    "luite'": ('lui-te', 'river-PL.POSS'),                        # 2x - rivers'
    "hangte'": ('hang-te', 'reason-PL.POSS'),                     # 2x - reasons'
    "kungte'": ('kung-te', 'tree-PL.POSS'),                       # 2x - trees'
    "mavan'": ('ma-van', 'before-sky.POSS'),                      # 2x - beforehand
    "nihna'": ('nih-na', 'two-NMLZ.POSS'),                        # 2x - second's
    'suanpa': ('suan-pa', 'descendant-M'),                        # 2x - descendant/duke
    # Round 148: Large batch of 2x partials
    'kisukha-in': ('ki-suk-ha-in', 'REFL-move-out-CVB'),          # 2x - put out
    'dengzanin': ('deng-zan-in', 'cut-break-ERG'),                # 2x - break down
    'tawsakin': ('taw-sak-in', 'blind-CAUS-CVB'),                 # 2x - smite blind
    'ngeksuak': ('ngek-suak', 'tender-become'),                   # 2x - tender/delicate
    'tamkham': ('tam-kham', 'many-break'),                        # 2x - broken to pieces
    'mangkha': ('mang-kha', 'dream-wake'),                        # 2x - dream
    'ot': ('ot', 'cry.out'),                                      # 2x - cry/wail
    'kipuksuk': ('ki-puk-suk', 'REFL-fall-move'),                 # 2x - prostrate
    'phulkhap': ('phul-khap', 'avenge-join'),                     # 2x - avenge
    'tuaklo': ('tuak-lo', 'encounter-NEG'),                       # 2x - without meeting
    'seelcipzo': ('seel-cip-zo', 'press-squeeze-COMPL'),          # 2x - pressed
    'kisiit': ('ki-siit', 'REFL-wipe'),                           # 2x - wipe self
    'kidiahin': ('ki-diah-in', 'REFL-level-CVB'),                 # 2x - level/even
    'phualkip': ('phual-kip', 'outside-completely'),              # 2x - completely outside
    'phulin': ('phul-in', 'avenge-ERG'),                          # 2x - avenging
    'laphuah': ('la-phuah', 'song-compose'),                      # 2x - compose song
    'phungmai': ('phung-mai', 'law-face'),                        # 2x - before law
    'kihui': ('ki-hui', 'REFL-gather'),                           # 2x - gather together
    'dap': ('dap', 'war'),                                        # 2x - battle/war
    'kihuiheek': ('ki-hui-heek', 'REFL-wind-fold'),              # 2x - wreath/intertwine (1 Kgs 7:17)
    'tasam': ('ta-sam', 'child-call'),                            # 2x - adopt
    'guallelh': ('gual-lelh', 'outside-change'),                  # 2x - substitute
    "mante'": ('man-te', 'price-PL.POSS'),                        # 2x - prices'
    'tazo': ('ta-zo', 'child-COMPL'),                             # 2x - fully born
    'vuknelh': ('vuk-nelh', 'wash-again'),                        # 2x - wash again
    'gimbawlin': ('gim-bawl-in', 'difficulty-make-CVB'),          # 2x - make difficulty
    'giklua': ('gik-lua', 'fall-exceed'),                         # 2x - fall greatly
    "khangnote'": ('khang-no-te', 'generation-young-PL.POSS'),    # 2x - young generation's
    'phualte-ah': ('phual-te-ah', 'outside-PL-LOC'),              # 2x - at outside
    'phiatsiang': ('phiat-siang', 'throw-clean'),                 # 2x - throw away clean
    'kikhuangin': ('ki-khuang-in', 'REFL-shake-CVB'),             # 2x - shaking
    'kikhuang': ('ki-khuang', 'REFL-shake'),                      # shake
    'kisun': ('ki-sun', 'REFL-day'),                              # 2x - daily
    'manlahin': ('man-lah-in', 'price-take-ERG'),                 # 2x - redeeming
    'kingamin': ('ki-ngam-in', 'REFL-dare-CVB'),                  # 2x - daring
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
    'phuksakin': ('phuk-sak-in', 'fell-CAUS-CVB'),                # 2x - cause to fall
    'gukhia-in': ('guk-khia-in', 'louse-exit-ERG'),               # 2x - lice emerge
    'batsakkik': ('bat-sak-kik', 'bind-CAUS-ITER'),               # 2x - bind again
    'piangvat': ('piang-vat', 'be.born-time'),                    # 2x - birth time
    'bawlthuah': ('bawl-thuah', 'make-success'),                  # 2x - make succeed
    'kitheihthang': ('ki-theih-thang', 'REFL-know-ABIL'),         # 2x - be known
    'lomte': ('lom-te', 'warm-PL'),                               # 2x - warm ones
    'kimakai': ('ki-ma-kai', 'REFL-front-reach'),                 # 2x - reach front
    'tuubukte': ('tuu-buk-te', 'flock-fold-PL'),                  # 2x - sheepfolds
    'kutna': ('kut-na', 'hand-NMLZ'),                             # 2x - handiwork
    'kihelkim': ('ki-hel-kim', 'REFL-deceive-complete'),          # 2x - fully deceive
    'pawlpawl': ('pawl~pawl', 'group~REDUP'),                     # 2x - various groups
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
    'kikhawmtuah': ('ki-khawm-tuah', 'REFL-gather-succeed'),      # 2x - gather succeed
    'tuilim': ('tui-lim', 'water-submerge'),                      # 2x - water submerge
    'suanglot': ('suang-lot', 'stone-loosen'),                    # 2x - loosen stone
    'vahsak': ('vah-sak', 'go-CAUS'),                             # 2x - cause go
    'phulsak': ('phul-sak', 'avenge-CAUS'),                       # 2x - cause avenge
    'gendai': ('gen-dai', 'speak-hinder'),                        # 2x - hinder speech
    'sialo': ('sia-lo', 'bad-NEG'),                               # 2x - not bad
    'ngaihsutsak': ('ngaihsut-sak', 'think-CAUS'),                # 2x - cause think
    'teltheihna': ('tel-theih-na', 'add-ABIL-NMLZ'),              # 2x - ability to add
    # Round 150: Final push to 99%
    'neu-a': ('neu-a', 'small-LOC'),                              # 2x - at small
    'neu-in': ('neu-in', 'small-ERG'),                            # 2x - with small
    'neu-et': ('neu-et', 'small-until'),                          # 2x - until small
    'tutna-ah': ('tut-na-ah', 'sleep-NMLZ-LOC'),                  # 2x - at sleep
    'phatna-ah': ('phat-na-ah', 'praise-NMLZ-LOC'),               # 2x - at praise
    'phatna-in': ('phat-na-in', 'praise-NMLZ-ERG'),               # 2x - with praise
    'hoihna-ah': ('hoih-na-ah', 'good-NMLZ-LOC'),                 # 2x - at goodness
    'hihna-ah': ('hih-na-ah', 'be-NMLZ-LOC'),                     # 2x - at being
    'cianna-ah': ('cian-na-ah', 'announce-NMLZ-LOC'),             # 2x - at announcing
    'zahtakna-in': ('zahtak-na-in', 'honor-NMLZ-ERG'),            # 2x - with honor
    'khangno-in': ('khang-no-in', 'generation-young-ERG'),        # 2x - young generation
    'sangzaw-in': ('sang-zaw-in', 'high-more-ERG'),               # 2x - more highly
    'zato': ('za-to', 'hear.I-remain'),                           # 2x - remain hearing
    'sukmang': ('suk-mang', 'make-chief'),                        # 2x - make chief
    'ahihloh': ('a-hih-loh', '3SG-be-fail'),                      # 2x - if not
    'thumnop': ('thum-nop', 'three-willing'),                     # 2x - three willing
    'tengbek': ('teng-bek', 'dwell-only'),                        # 2x - dwell only
    'phutsak': ('phut-sak', 'spray-CAUS'),                        # 2x - cause spray
    'hehpihzawh': ('heh-pih-zawh', 'angry-CAUS-ABIL'),            # 2x - able to anger
    'kiginkholh': ('ki-gin-kholh', 'REFL-fear-INTENS'),           # 2x - fearfully made
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
    'ngeungau': ('ngeu-ngau', 'shake~REDUP'),                     # 2x - shake
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
    'zawhzawh': ('zawh~zawh', 'be.able~REDUP'),                      # 2x - very able
    'thupi-in': ('thu-pi-in', 'word-big-ERG'),                    # 2x - with big word
    'dahnate': ('dah-na-te', 'sad-NMLZ-PL'),                      # 2x - sadnesses
    'paih': ('pai-h', 'go-COMP'),                                 # 2x - go (completed)
    'thuthukte': ('thu-thuk-te', 'word-deep-PL'),                 # 2x - deep words
    'vakvaisak': ('vak-vai-sak', 'walk-around-CAUS'),             # 2x - cause walk
    'dingpi-in': ('ding-pi-in', 'stand-big-ERG'),                 # 2x - standing big
    'seello': ('seel-lo', 'press-NEG'),                           # 2x - not press
    'pilnate': ('pil-na-te', 'learn-NMLZ-PL'),                    # 2x - learnings
    'nialnial': ('nial~nial', 'argue~REDUP'),                     # 2x - argue much
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
    'duhduh': ('duh~duh', 'want~REDUP'),                          # 2x - much want
    'keuhkeuh': ('keuh~keuh', 'dig~REDUP'),                       # 2x - dig much
    'kholsa': ('khol-sa', 'denounce-PAST'),                       # 2x - denounced
    'khantosak': ('khan-to-sak', 'spirit-stay-CAUS'),             # 2x - spiritual stay
    'punna': ('pun-na', 'multiply-NMLZ'),                         # 2x - multiplying
    'kisukmitsak': ('ki-suk-mit-sak', 'REFL-move-eye-CAUS'),      # 2x - cause eye move
    'buhsi': ('buh-si', 'rice-die'),                              # 2x - rice die
    'lunggimin': ('lung-gim-in', 'heart-pain-ERG'),               # 2x - with pain
    'nopnate': ('nop-na-te', 'willing-NMLZ-PL'),                  # 2x - willingnesses
    'kivuk': ('ki-vuk', 'REFL-wash'),                             # 2x - wash self
    'taai': ('taai', 'flee'),                                     # 2x - flee
    'langpan': ('lang-pan', 'advocate'),                         # 88x - plead.for, support
    # Etymology: lang 'side' + pan 'plead' → 'plead on behalf of, advocate'
    "tagahte'": ('ta-gah-te', 'child-fruit-PL.POSS'),             # 2x - offspring's
    'neihsunte': ('neih-sun-te', 'have-day-PL'),                  # 2x - daily having
    'gawi-in': ('gawi-in', 'hook-ERG'),                           # 2x - with hook
    "meigongte'": ('meigong-te', 'widow-PL.POSS'),                # 2x - widows' (mei 'female' TB *mei)
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
    'ngaingai': ('ngai~ngai', 'listen.I~REDUP'),                    # 2x - listen well
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
    "kigin'": ('ki-gin', 'REFL-fear.POSS'),                       # 2x - fearing's
    'kigin': ('ki-gin', 'REFL-fear'),                             # fearing
    'kipuahin': ('ki-puah-in', 'REFL-send-CVB'),                  # 2x - sending self
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
    'kankhia': ('kan-khia', 'firmly-exit'),                   # firmly exit (not ka-nkhia)
    'kahlei': ('kah-lei', 'behind-earth'),                    # behind/back
    'kahlei-ah': ('kah-lei-ah', 'behind-earth-LOC'),          # at behind
    'anvai': ('an-vai', 'PL-go'),                             # they go
    'kampau': ('kam-pau', 'word-speak'),                      # speak words
    'kampau-in': ('kam-pau-in', 'word-speak-ERG'),            # speaking
    'kamkat': ('kam-kat', 'word-cut'),                        # cut off words
    'kamkhat': ('kam-khat', 'word-one'),                      # one word
    'kamtam': ('kam-tam', 'word-many'),                       # many words
    'nawhpai': ('nawh-pai', 'push-go'),                       # push forward
    'napna': ('nap-na', 'thick-NMLZ'),                        # thickness
    'namtuam': ('nam-tuam', 'tribe-kind'),                    # various tribes
    # Round 125: Hyphenated suffix forms
    'notea': ('no-te-a', 'young-PL-NOM'),                      # young ones
    'nomaua': ('no-mau-a', 'young-also-NOM'),                  # also young
    'nuaiate': ('nuai-a-te', 'below-NOM-PL'),                  # those below
    'piaknain': ('piak-na-in', 'give.to-NMLZ-INST'),           # in giving
    'mautea': ('mau-te-a', 'also-PL-NOM'),                     # also they
    'zahtakte': ('zahtak-te', 'honor-PL'),                     # honors
    'vasate': ('va-sa-te', 'go.and-PAST-PL'),                  # went PL
    'sealte': ('seal-te', 'seal-PL'),                          # seals
    'paaiah': ('pa-ai-ah', 'father-NOM-LOC'),                  # to/at father
    'naungekah': ('nau-ngek-ah', 'child-birth-LOC'),           # at midwife
    'sipah': ('si-pa-ah', 'be-NMLZ-LOC'),                      # being LOC
    'maimanah': ('mai-man-ah', 'face-true-LOC'),               # in face
    'khualnaun': ('khual-naun', 'guest-long.time'),            # sojourner
    'khualnaunin': ('khual-naun-in', 'guest-long.time-INST'),  # as sojourner
    'zawnahna': ('zawn-ah-na', 'north-LOC-?'),                 # to north
    'lungzina': ('lung-zin-a', 'heart-bright-NOM'),            # brightness
    
    # Round 152: Hyphenated compound fixes
    'nini': ('ni~ni', 'day~REDUP'),                            # each day, daily
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
    'thuthu': ('thu~thu', 'word~REDUP'),                       # secrets/deep things
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
    'kiumcip': ('ki-um-cip', 'REFL-cover-tightly'),            # enclosed/shut up
    'ki-umcip': ('ki-um-cip', 'REFL-cover-tightly'),           # enclosed/shut up
    'kitha': ('ki-tha', 'REFL-spread'),                        # scattered/spread
    'ki-tha': ('ki-tha', 'REFL-spread'),                       # scattered/spread
    'kiitin': ('ki-it-in', 'REFL-love-CVB'),                   # harmonizing/uniting  
    'ki-itin': ('ki-it-in', 'REFL-love-CVB'),                  # harmonizing/uniting
    'kiukin': ('ki-uk-in', 'REFL-rule-CVB'),                   # being ruled
    'ki-ukin': ('ki-uk-in', 'REFL-rule-CVB'),                  # being ruled
    'kei-a': ('kei-a', '1SG.EMPH-GEN'),                        # my own (emphatic)
    'zalhmai': ('zalh-mai', 'settle-INTENS'),                  # settle down/flatten
    'zalhmai-in': ('zalh-mai-in', 'settle-INTENS-ERG'),        # settling (adv)
    'zalhmain': ('zalh-mai-in', 'settle-INTENS-ERG'),          # settling (adv)
    'kawmsa': ('kawm-sa', 'sigh-PAST'),                        # sighed/sighing
    'kawmsa-in': ('kawm-sa-in', 'sigh-PAST-ERG'),              # sighing (adv)
    'kawmsain': ('kawm-sa-in', 'sigh-PAST-ERG'),               # sighing (adv)
    'cilin': ('cil-in', 'thresh-ERG'),                         # threshing (adv)
    'ci-lin': ('cil-in', 'thresh-ERG'),                        # threshing (adv)
    'bawngek': ('bawng-ek', 'cattle-dung'),                    # cow dung
    'bawng-ek': ('bawng-ek', 'cattle-dung'),                   # cow dung
    'anpia': ('an-pia', 'PL-give'),                            # they give
    'anpia-in': ('an-pia-in', 'PL-give-ERG'),                  # giving (them)
    'lungam': ('lung-am', 'heart-feel'),                       # feel/sense
    'tumakuak': ('tu-ma-kuak', 'this-also-half'),              # half-measure
    'tumakuakte': ('tu-ma-kuak-te', 'this-also-half-PL'),      # half-measures
    'tu-ma-kuakte': ('tu-ma-kuak-te', 'this-also-half-PL'),    # half-measures
    'nitakan': ('ni-tak-an', 'sun-set-time'),                  # evening time
    
    # Round 153: Comprehensive hyphenated compound fixes
    # === ki- reflexive/reciprocal compounds ===
    'ki-enen': ('ki-en-en', 'REFL-look~REDUP'),                 # gaze at each other
    'kizia': ('ki-zia', 'REFL-crouch'),                        # crouch/lie flat
    'kizia-in': ('ki-zia-in', 'REFL-crouch-CVB'),              # crouching
    'kiciangto': ('ki-ciang-to', 'REFL-pile-CONT'),            # pile up/stand firm
    'kiciangto-in': ('ki-ciang-to-in', 'REFL-pile-CONT-CVB'),  # piling up
    'ki-atnente': ('ki-at-nen-te', 'REFL-burn-fire-PL'),       # burnt offerings
    'ki-atkeh': ('ki-at-keh', 'REFL-cut-self'),               # cut self (mourning)
    'ki-omsakkik': ('ki-om-sak-kik', 'REFL-be-CAUS-again'),    # restore/re-establish
    'ki-etkik': ('ki-et-kik', 'REFL-care-again'),              # inspect again
    'kilukhuhsa': ('ki-lu-khuh-sa', 'REFL-head-cover-PAST'),   # covered head
    'kilukhuhsa-in': ('ki-lu-khuh-sa-in', 'REFL-head-cover-PAST-CVB'), # covering head
    'ki-up': ('ki-up', 'REFL-expect'),                         # expect/hope
    'kipumpei': ('ki-pum-pei', 'REFL-body-shake'),             # tremble/shake
    'kipumpei-in': ('ki-pum-pei-in', 'REFL-body-shake-CVB'),   # trembling
    'kihoho': ('ki-ho-ho', 'REFL-counsel~REDUP'),              # counsel together
    'kihoho-in': ('ki-ho-ho-in', 'REFL-counsel-REDUP-CVB'),    # counseling together
    'kivakna': ('ki-vak-na', 'REFL-walk-NMLZ'),                # roaming/wandering
    'kivakna-in': ('ki-vak-na-in', 'REFL-walk-NMLZ-CVB'),      # in wandering
    'kilawnto': ('ki-lawn-to', 'REFL-rise-CONT'),              # rise and fall
    'kilawnto-in': ('ki-lawn-to-in', 'REFL-rise-CONT-CVB'),    # rising and falling
    'kilensa': ('ki-len-sa', 'REFL-lean-PAST'),                # leaned on
    'kilensa-in': ('ki-len-sa-in', 'REFL-lean-PAST-CVB'),      # leaning on
    'kibotkhia': ('ki-bot-khia', 'REFL-remove-exit'),          # depart/remove
    'kibotkhia-in': ('ki-bot-khia-in', 'REFL-remove-exit-CVB'), # departing
    'kibulhsa': ('ki-bulh-sa', 'REFL-arrange-PAST'),           # arranged/set up
    'kibulhsa-in': ('ki-bulh-sa-in', 'REFL-arrange-PAST-CVB'), # arranging
    'kinawhsa': ('ki-nawh-sa', 'REFL-push-PAST'),              # pushed out
    'kinawhsa-in': ('ki-nawh-sa-in', 'REFL-push-PAST-CVB'),    # pushing out
    'kipuahpha': ('ki-puah-pha', 'REFL-waste-away'),           # pine away/waste
    'kipuahpha-in': ('ki-puah-pha-in', 'REFL-waste-away-CVB'), # pining away
    'kikhualna': ('ki-khual-na', 'REFL-guest-NMLZ'),           # sojourning
    'kikhualna-in': ('ki-khual-na-in', 'REFL-guest-NMLZ-CVB'), # in sojourning
    'kiphuai': ('ki-phuai', 'REFL-devour'),                    # bite/devour each other
    'kiphuai-in': ('ki-phuai-in', 'REFL-devour-CVB'),          # devouring
    'kituhnate': ('ki-tuh-na-te', 'REFL-swear-NMLZ-PL'),       # oaths
    'kituhnate-ah': ('ki-tuh-na-te-ah', 'REFL-swear-NMLZ-PL-LOC'), # in oaths
    'kiginna': ('ki-gin-na', 'REFL-wanton-NMLZ'),              # wanton living
    'kiginna-in': ('ki-gin-na-in', 'REFL-wanton-NMLZ-CVB'),    # living wantonly
    'ki-ipipna': ('ki-ip-ip-na', 'REFL-strive-REDUP-NMLZ'),    # striving together
    'ki-ipipna-in': ('ki-ip-ip-na-in', 'REFL-strive-REDUP-NMLZ-CVB'),
    'kihazatnate': ('ki-hazat-na-te', 'REFL-revel-NMLZ-PL'),   # revelries
    'kihazatnate-in': ('ki-hazat-na-te-in', 'REFL-revel-NMLZ-PL-CVB'),
    'kihaza': ('ki-haza', 'REFL-revel'),                       # revel
    'kihaza-in': ('ki-haza-in', 'REFL-revel-CVB'),             # reveling
    'kimawlna': ('ki-mawl-na', 'REFL-subdue-NMLZ'),            # subjection
    'kimawlna-ah': ('ki-mawl-na-ah', 'REFL-subdue-NMLZ-LOC'),  # in subjection
    'ki-ettelna': ('ki-et-tel-na', 'REFL-test-match-NMLZ'),    # testing
    'ki-ettel': ('ki-et-tel', 'REFL-test-match'),              # test/examine
    'ki-ettehin': ('ki-et-teh-in', 'REFL-test-match-CVB'),     # testing
    'ki-upmawhnate': ('ki-up-mawh-na-te', 'REFL-hope-err-NMLZ-PL'), # offenses
    'ki-apin': ('ki-ap-in', 'REFL-cry-CVB'),                   # crying out
    'ki-uktawm': ('ki-uk-tawm', 'REFL-rule-end'),              # end of rule
    'ki-ipzote': ('ki-ip-zo-te', 'REFL-strive-ABIL-PL'),       # those striving
    'ki-ipin': ('ki-ip-in', 'REFL-strive-CVB'),                # striving
    'kikaiawksak': ('ki-kai-awk-sak', 'REFL-gather-all-CAUS'), # cause to gather
    'kikai-awksak': ('ki-kai-awk-sak', 'REFL-gather-all-CAUS'),
    'kize-etsa': ('ki-ze-et-sa', 'REFL-tempt-care-PAST'),      # tempted
    'ki-eu': ('ki-eu', 'REFL-call'),                           # reflexive form
    'ki-ipcip': ('ki-ip-cip', 'REFL-strive-tightly'),          # strive earnestly
    'ki-uatsaknate': ('ki-uat-sak-na-te', 'REFL-bind-CAUS-NMLZ-PL'), # causings
    'ki-enpha': ('ki-en-pha', 'REFL-look-good'),               # look well/prosper
    'ki-umcihin': ('ki-um-cih-in', 'REFL-cover-tight-CVB'),    # enclosing
    'kitunsa': ('ki-tun-sa', 'REFL-arrive-PAST'),              # arrived
    'kitunsa-in': ('ki-tun-sa-in', 'REFL-arrive-PAST-CVB'),    # arriving
    'kikawi': ('ki-kawi', 'REFL-hook'),                        # hook together
    'kikawi-in': ('ki-kawi-in', 'REFL-hook-CVB'),              # hooking
    'ki-atte': ('ki-at-te', 'REFL-burn-PL'),                   # burnt ones
    'kinungat': ('ki-nung-at', 'REFL-follow-after'),           # follow after
    'kinung-at': ('ki-nung-at', 'REFL-follow-after'),
    'ki-itnate': ('ki-it-na-te', 'REFL-love-NMLZ-PL'),         # loves
    'kisu': ('ki-su', 'REFL-count'),                           # be counted
    'kisu-in': ('ki-su-in', 'REFL-count-CVB'),
    'kitheihsakna': ('ki-theih-sak-na', 'REFL-know-CAUS-NMLZ'), # making known
    'kitheihsakna-ah': ('ki-theih-sak-na-ah', 'REFL-know-CAUS-NMLZ-LOC'),
    'kitheihsakna-in': ('ki-theih-sak-na-in', 'REFL-know-CAUS-NMLZ-CVB'),
    'kiphukha': ('ki-phu-kha', 'REFL-wear-put'),               # wear/put on
    'kiphukha-in': ('ki-phu-kha-in', 'REFL-wear-put-CVB'),
    'kikokona': ('ki-koko-na', 'REFL-cry.out-NMLZ'),           # crying out
    'kikokona-in': ('ki-koko-na-in', 'REFL-cry.out-NMLZ-CVB'),
    'kikolawksak': ('ki-kol-awk-sak', 'REFL-cry-all-CAUS'),
    'kikol-awksak': ('ki-kol-awk-sak', 'REFL-cry-all-CAUS'),
    
    # === Verbal compounds ===
    'hangkeu': ('hang-keu', 'roast-fire'),                      # roasted
    'hangkeu-in': ('hang-keu-in', 'roast-fire-ERG'),            # roasting
    'sapipi': ('sa-pi-pi', 'INTENS-big~REDUP'),                # greatly
    'sapipi-in': ('sa-pi-pi-in', 'INTENS-big-REDUP-ERG'),      # very greatly
    'hehsapi': ('heh-sa-pi', 'anger-PAST-big'),                # greatly angered
    'hehsapi-in': ('heh-sa-pi-in', 'anger-PAST-big-ERG'),      # in great anger
    'thangzaw': ('thang-zaw', 'bless-more'),                   # bless more
    'thangzaw-in': ('thang-zaw-in', 'bless-more-ERG'),         # blessing more
    'ciangpha': ('ciang-pha', 'announce-good'),                # strengthen
    'ciangpha-in': ('ciang-pha-in', 'announce-good-ERG'),      # strengthening
    'tampipi': ('tam-pi-pi', 'many-big~REDUP'),                # very many
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
    'gawigawi': ('gawi~gawi', 'gnash~REDUP'),                  # gnashing
    'gawigawi-in': ('gawi-gawi-in', 'gnash-REDUP-ERG'),        # gnashing (adv)
    'thenthen': ('then~then', 'thousand~REDUP'),               # greatly multiply
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
    'suausuau': ('suau~suau', 'chirp~REDUP'),                  # chirping
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
    'pul': ('pul', 'PUL'),                                  # divide
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
    'luhzo': ('luh-zo', 'enter-ABIL'),                         # able to enter
    'luhzo-in': ('luh-zo-in', 'enter-ABIL-CVB'),               # entering
    'thalawhna': ('tha-lawh-na', 'flee-away-NMLZ'),            # fleeing
    'thalawhna-in': ('tha-lawh-na-in', 'flee-away-NMLZ-ERG'),  # in fleeing
    'gahta': ('gah-ta', 'pasture-NMLZ'),                       # pasturing
    'gahta-in': ('gah-ta-in', 'pasture-NMLZ-ERG'),             # pasturing
    'tuahsia': ('tuah-sia', 'meet-bad'),                       # displease
    'tuahsia-in': ('tuah-sia-in', 'meet-bad-ERG'),             # displeasing
    'tuucinna': ('tuucin-na', 'shepherd-NMLZ'),                # shepherding
    'tuucinna-in': ('tuucin-na-in', 'shepherd-NMLZ-ERG'),      # in shepherding
    'pozo': ('po-zo', 'spread-ABIL'),                          # able to spread
    'pozo-in': ('po-zo-in', 'spread-ABIL-CVB'),                # spreading
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
    'mutheisa': ('mu-thei-sa', 'see-ABIL-PAST'),               # could be seen
    'mutheisa-in': ('mu-thei-sa-in', 'see-ABIL-PAST-ERG'),     # being seen
    'zuakma': ('zuak-ma', 'sell-also'),                        # also sell
    'zuakma-in': ('zuak-ma-in', 'sell-also-ERG'),              # also selling
    'keksa': ('kek-sa', 'foot-PAST'),                          # footed/stepped
    'keksa-in': ('kek-sa-in', 'foot-PAST-ERG'),                # stepping
    'mahmahpi': ('mah-mah-pi', 'EMPH-EMPH-INTENS'),            # very very much
    'mahmahpi-in': ('mah-mah-pi-in', 'EMPH-EMPH-INTENS-ERG'),
    'zeekte': ('zeek-te', 'crouch-PL'),                        # crouching ones
    'zeekte-in': ('zeek-te-in', 'crouch-PL-ERG'),
    'simthei': ('sim-thei', 'count-ABIL'),                     # able to count
    'simthei-in': ('sim-thei-in', 'count-ABIL-CVB'),           # counting
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
    'khuakhua': ('khua~khua', 'town~REDUP'),                   # every town
    'khuakhua-in': ('khua-khua-in', 'town-REDUP-ERG'),
    'ngawngawhte': ('ngawng-awh-te', 'neck-bend-PL'),          # bent necks
    'ngawng-awhte': ('ngawng-awh-te', 'neck-bend-PL'),
    'huau': ('hu-au', 'grandparent-male'),                    # grandfather
    'huau-in': ('hu-au-in', 'grandparent-male-ERG'),
    'ciahpihto': ('ciah-pih-to', 'return-all-CONT'),           # returning
    'ciahpihto-in': ('ciah-pih-to-in', 'return-all-CONT-ERG'),
    'lialua': ('lia-lua', 'exceed~REDUP'),                    # greatly exceed
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
    'vaite': ('vai-te', 'affairs-PL'),                         # affairs
    'vaite-ah': ('vai-te-ah', 'affairs-PL-LOC'),
    'muamuaana': ('mua-mua-a-na', 'see-REDUP-NOM-NMLZ'),       # viewing
    'muamua-na': ('mua-mua-na', 'see-REDUP-NMLZ'),
    'cilei': ('ci-lei', 'say-buy'),                            # say/buy
    'ci-lei': ('ci-lei', 'say-buy'),
    'kineuet': ('ki-neu-et', 'REFL-small-care'),               # humble self
    'kineu-et': ('ki-neu-et', 'REFL-small-care'),
    'lawtkhia': ('lawt-khia', 'jump-exit'),                    # jump out
    'lawtkhia-in': ('lawt-khia-in', 'jump-exit-ERG'),
    'tuka': ('tu-ka', 'now-1SG'),                              # now I
    'tu-ka': ('tu-ka', 'now-1SG'),
    'vasa-kalaohte': ('va-sa-kala-oh-te', 'bird-flesh-owl-type-PL'),
    "vasa-kalaohte'": ("va-sa-kala-oh-te'", 'bird-flesh-owl-type-PL.POSS'),
    'nalnah': ('nal-na-ah', '2SG-NMLZ-LOC'),                   # your place
    'nalna-ah': ('nal-na-ah', '2SG-NMLZ-LOC'),
    'huiah': ('hui-ah', 'wind-LOC'),                           # in wind
    'hui-ah': ('hui-ah', 'wind-LOC'),
    'noahtaak': ('noah-taak', 'NOAH-true'),                    # Noah truly
    'noah-taak': ('noah-taak', 'NOAH-true'),
    'kawmpi': ('kawm-pi', 'sigh-big'),                         # sigh greatly
    'kawmpi-in': ('kawm-pi-in', 'sigh-big-ERG'),
    'nakpipi': ('nak-pi-pi', '2SG-big~REDUP'),                 # your greatness
    'nakpipi-in': ('nak-pi-pi-in', '2SG-big-REDUP-ERG'),
    'awngawng': ('awng~awng', 'young~REDUP'),                   # wide open
    'awng-awng': ('awng~awng', 'young~REDUP'),
    'tusawnsawn': ('tu-sawn-sawn', 'now-time~REDUP'),          # now repeatedly
    'tu-sawnsawn': ('tu-sawn-sawn', 'now-time~REDUP'),
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
    'kahpihto': ('kah-pih-to', '1SG-accompany-CONT'),          # I accompanying
    'kahpihto-in': ('kah-pih-to-in', '1SG-accompany-CONT-ERG'),
    'eukhia': ('eu-khia', 'call-exit'),                        # call out
    'eukhia-in': ('eu-khia-in', 'call-exit-ERG'),
    'atulmakin': ('a-tul-ma-kin', '3SG-?-also-?'),             # he also
    'bilapphuai': ('bil-ap-phuai', 'ear-close-?'),             # deaf
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
    'tedildel': ('te-dil-del', 'PL-shake~REDUP'),               # scattered
    'te-dildel': ('te-dil-del', 'PL-shake~REDUP'),
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
    
    # Form II stems with emphatic -e suffix (5x, 2x)
    'nusiate': ('nusia-te', 'forsake-PL'),                      # those who forsake (5x)
    'husiate': ('husia-te', 'tempest-PL'),                      # tempests (2x)
    
    # Low-frequency compounds (2x each)
    'nawlkhin': ('nawl-khin', 'way-knowledge'),                  # knowledge of ways (2x)
    'sikkate': ('sikka-te', 'basin-PL'),                        # basins/basons (2x)
    'sikka': ('sikka', 'basin'),                                # basin/vessel
    
    # Form II + unknown suffix compounds
    'theihzel': ('theih-zel', 'know-accustomed'),               # accustomed/habitual (2x)
    'cihmel': ('cih-mel', 'say-understand'),                    # understand (2x)
    
    # Contracted locative forms (lak-ah → laka)
    'leilaka': ('lei-lak-ah', 'earth-among-LOC'),               # on the earth (2x)
    
    # Short stems that were removed to prevent mis-segmentation
    # Adding as compounds instead
    'ku': ('ku', 'howl'),                                       # make noise like dog (2x)
    'khi': ('khi', 'chain'),                                    # chain/necklace (2x)
    
    # Round 164: Short-stem reduplication compounds (prevent over-segmentation)
    'helhel': ('hel~hel', 'feed~REDUP'),                          # feeding/grazing repeatedly
    'didi': ('di~di', 'soft~REDUP'),                              # softly
    'hoho': ('ho~ho', 'crowd~REDUP'),                             # greeting repeatedly  
    'themthem': ('them~them', 'matter~REDUP'),                    # matters/things
    'sensen': ('sen~sen', 'distinguish~REDUP'),                   # distinguishing
    'tuptup': ('tup~tup', 'swallow~REDUP'),                       # swallowing
    'cippi': ('ci-pi', 'say-COMP'),                             # saying greatly
    'cipna': ('cip-na', 'besiege-NMLZ'),                        # siege
    'cipte': ('cip-te', 'besiege-PL'),                          # sieges (?)
    'kicipna': ('ki-cip-na', 'REFL-besiege-NMLZ'),              # breach/gap
    
    # Round 164 batch 5: Problematic stems moved to compounds
    'zuauthu': ('zuau-thu', 'vain-word'),                       # lie/dissemble (92x)
    'zuaugen': ('zuau-gen', 'vain-speak'),                      # speak vainly (14x)
    'zuaute': ('zuau-te', 'vain-PL'),                           # vain ones (2x)
    'tainapa': ('tai-na-pa', 'flee-NMLZ-father'),               # refugee (not taina-pa)
    'kituhte': ('ki-tuh-te', 'REFL-dispute-PL'),                # disputes (2x)
    'kituhteh': ('ki-tuh-teh', 'REFL-dispute-EMP'),             # disputed indeed (2x)
    
    # Round 167: V1+V2 serial verb compounds from hapax analysis
    # These need explicit entries because suffix parsing only triggers with grammatical suffixes
    'bawlthak': ('bawl-thak', 'make-new'),                      # renew (Psalm 104:30)
    'khangthak': ('khang-thak', 'generation-new'),              # new generation (Judges 2:10)
    'nongek': ('no-ngek', 'young-tender'),                      # tender young ones (Gen 33:13)
    'dawnngek': ('dawn-ngek', 'top-tender'),                    # tip/branch (Ezek 17:22)
    'dawnngekte': ('dawn-ngek-te', 'top-tender-PL'),            # tips/branches (Psalm 80:11)
    'sidek': ('si-dek', 'die-low'),                             # low/pit (Psalm 88:4)
    'sumdek': ('sum-dek', 'money-low'),                         # cheap (Prov 20:14)
    'dekna': ('dek-na', 'low-NMLZ'),                            # lowness (Song 5:8)
    'genmun': ('gen-mun', 'speak-rare'),                        # rare word (1 Sam 3:1)
    'ommun': ('om-mun', 'exist-rare'),                          # rarely exist (1 Sam 3:1)
    'bukmun': ('buk-mun', 'ambush-place'),                      # place of ambush (Isaiah 54:2)
    
    # Round 167b: Disambiguation - ho-pih (greet-APPL) vs hop-X (snare-X)
    # 'hopih' = ho-pih (speak to) appears 161x, must override 'hop' stem parsing
    'hopih': ('ho-pih', 'greet-APPL'),                          # speak to/address (161x)
    'hopihin': ('ho-pih-in', 'greet-APPL-CVB'),                 # speaking to (10x)
    'hopihsak': ('ho-pih-sak', 'greet-APPL-CAUS'),              # cause to speak to (6x)
    'hopihpah': ('ho-pih-pah', 'greet-APPL-NEG.ABIL'),          # unable to speak to (2x)
    
    # Round 167b: thak-hauh-sak = "strengthen" (KJV: strengthen, strengthened)
    # 'hauh' = strong/vigor, thakhauhsak = make-strong = strengthen
    'thakhatin': ('thak-hat-in', 'new-strong-ERG'),             # freshly/recently (56x)
    'thakhauhsak': ('thak-hauh-sak', 'new-strong-CAUS'),        # strengthen (9x) 
    'kithakhauhsakin': ('ki-thak-hauh-sak-in', 'REFL-new-strong-CAUS-CVB'),
    'thakhauhsakzaw': ('thak-hauh-sak-zaw', 'new-strong-CAUS-MORE'), # strengthen more
    
    # Round 167c: kaih-khop = gather-together (KJV: gathered)
    'kaihkhopsa': ('kaih-khop-sa', 'gather-together-PAST'),     # gathered (Gen 12:5)
    'kaihkhoppih': ('kaih-khop-pih', 'gather-together-APPL'),   # gather with (Matt 12:30)
    'kaihkhopna': ('kaih-khop-na', 'gather-together-NMLZ'),     # gathering (Exod 23:16)
    'kikaihkhopna': ('ki-kaih-khop-na', 'REFL-gather-together-NMLZ'), # gathering (Num 16:11)
    
    # Round 167c: dialkhip = diadem/hood/veil (KJV: hoods, vails, diadem)
    'dialkhip': ('dial-khip', 'call-veil'),                     # hood/veil (Isaiah 3:23)
    'dialkhipte': ('dial-khip-te', 'call-veil-PL'),             # hoods/veils (pl)
    
    # Round 167d: More hapax compounds from KJV cross-reference
    'buhlomte': ('buh-lom-te', 'rice-bundle-PL'),               # sheaves (Psalm 126:6)
    'kawikawite': ('kawikawi-te', 'to.and.fro-PL'),             # talebearers (Prov 20:19)
    'kikhamna': ('ki-kham-na', 'REFL-forbid-NMLZ'),             # vow/oath (Ezek 18:6)
    'gahteng': ('gah-teng', 'fruit-whole'),                     # strong rods/branches (Ezek 19:12)
    'phawktheihna': ('phawk-theih-na', 'remember-ABIL-NMLZ'),   # remembrance (Ezek 21:23)
    'khuaphawk': ('khua-phawk', 'town-remember'),               # care/anxiety (Ezek 30:9)
    'hauhnateng': ('hauhna-teng', 'riches-whole'),              # multitude (Ezek 30:10)
    
    # Round 167d: More verb compounds
    'tawnnate': ('tawn-na-te', 'meet-NMLZ-PL'),                 # meetings
    'kigennate': ('ki-gen-na-te', 'REFL-speak-NMLZ-PL'),        # speakings
    
    # Round 167e: More suffix patterns from hapax analysis
    'hute': ('hu-te', 'protect-PL'),                            # protectors/shields (Gen 15:1)
    'nengniamin': ('nengniami-n', 'deceive-ERG'),               # deceiving (Lev 6:2)
    'galkapteng': ('gal-kap-teng', 'war-throw-ALL'),            # all soldiers (Ezek 30:6)
    'ganhingteng': ('gan-hing-teng', 'animal-alive-ALL'),       # all living animals (Dan 2:38)
    'galkapte': ('gal-kap-te', 'war-throw-PL'),                 # soldiers
    'ganhingteteng': ('gan-hing-te-teng', 'animal-alive-PL-ALL'), # all animals
    
    # Round 167e: -teng suffix (all/whole) compounds
    'leitungteng': ('lei-tung-teng', 'earth-surface-ALL'),      # all the earth surface
    'hihthuteng': ('hih-thu-teng', 'this-word-ALL'),            # all these words
    'lampangteng': ('lam-pang-teng', 'way-carry-ALL'),          # all directions (Ezek 47:18)
    
    # Round 167f: Unknown words from hapax KJV cross-reference
    'daang': ('daang', 'forsake'),                              # forsake (Prov 27:10)
    'daanggawp': ('daang-gawp', 'forsake-grasp'),               # troubled/distressed (Dan 7:28)
    'khungnung': ('khung-nung', 'border-back'),                 # far end/border (Ezek 48:1)
    'phiangsiah': ('phiang-siah', 'collect-tribute'),           # tax collector (Dan 11:20)
    'leenlak': ('leen-lak', 'swoop-among'),                     # swoop down (Hosea 8:1)
    'pettan': ('pettan', 'palmerworm'),                         # palmerworm insect (Joel 1:4)
    'hawksuk': ('hawk-suk', 'roar-down'),                       # roar out (Joel 3:16)
    'kiteenkhia': ('ki-teen-khia', 'REFL-snatch-out'),          # plucked out (Amos 4:11)
    'kiamsuk': ('kiam-suk', 'flood-down'),                      # rise as flood (Amos 8:8)
    'gimlawh': ('gim-lawh', 'pain-exceed'),                     # very sorrowful (Zech 9:5)
    
    # Round 167g: More unknown words from Gospel hapax
    'guai': ('guai', 'hire'),                                   # hire/wage (Deut 23:18)
    # kiguaihna already defined earlier with simpler analysis
    'kipeksat': ('ki-pek-sat', 'REFL-break-strike'),            # break covenant (Isa 33:8)
    'kipeksatin': ('ki-pek-sat-in', 'REFL-break-strike-CVB'),   # breaking
    'likkhiat': ('lik-khiat', 'burden-away'),                   # burden/cut (Zech 12:3)
    'bulphuk': ('bul-phuk', 'root-uproot'),                     # root/uproot (Matt 3:10)
    'lawngsim': ('lawng-sim', 'back-touch'),                    # touch (Matt 9:20)
    'taiibawl': ('taii-bawl', 'rebuke-make'),                   # upbraid (Matt 11:20)
    'popah': ('po-pah', 'spring-up'),                           # spring up (Matt 13:5)
    'lehmut': ('leh-mut', 'turn-contrary'),                     # contrary/toss (Matt 14:24)
    'henkhit': ('hen-khit', 'condemn-away'),                    # condemn variant
    'lehtai': ('leh-tai', 'turn-rebuke'),                       # rebuke (Mark 8:33)
    'kinakko': ('ki-nak-ko', 'REFL-cry-loud'),                  # cry out (Mark 15:14)
    'lamnawl': ('lam-nawl', 'way-other'),                       # other side (Luke 10:31)
    'phengzat': ('pheng-zat', 'waste-use'),                     # waste/squander (Luke 15:13)
    'kilhcip': ('ki-lh-cip', 'REFL-hang-tight'),                # crucify (Luke 23:33)
    # Round 167h: More NT hapax from KJV cross-reference
    'lehpei': ('leh-pei', 'turn-betray'),                        # betray (John 6:64)
    'buannawi': ('buan-nawi', 'dirt-soft'),                      # clay (John 9:6)
    'dengnuam': ('deng-nuam', 'stone-want'),                     # want.to.stone (John 10:33)
    'likkhia': ('lik-khia', 'roll-away'),                        # take.away (John 11:39)
    'mantaktak': ('man-tak-tak', 'true-real~REDUP'),             # truly (John 19:35)
    'manzawk': ('man-zawk', 'true-more'),                        # more.right (Acts 4:19)
    'ngongbawl': ('ngong-bawl', 'force-do'),                     # violence (Acts 5:26)
    'kigawlmek': ('ki-gawl-mek', 'REFL-strangle-tight'),         # strangled (Acts 15:20)
    'buppiak': ('bu-piak', 'body-give'),                         # yield (Romans 6:19)
    'tavai': ('ta-vai', 'child-shame'),                          # ashamed (Romans 9:33)
    'kipeh': ('ki-peh', 'REFL-join'),                            # grafted.in (Romans 11:17)
    'gimsakkhak': ('gim-sak-khak', 'suffer-CAUS-suddenly'),      # persecute (Romans 15:31)
    # Round 167h more: OT hapax compounds
    'singkhuah': ('sing-khuah', 'wood-burn'),                    # firebrand (Amos 4:11)
    'lunggulhgulh': ('lung-gulh-gulh', 'heart-desire~REDUP'),    # desired (Micah 7:1)
    'genzak': ('gen-zak', 'speak-proclaim'),                     # publish (Isaiah 52:7)
    'cikhuk': ('ci-khuk', 'salt-preserve'),                      # to.salt (Ezekiel 47:11)
    'atkhiat': ('at-khiat', '3SG.cut-away'),                     # cut off (1 Sam 24:5) - phonotactic fix
    'kanzaw': ('ka-n-zaw', '1SG-DIR-leap'),                      # leap (1 Sam 20:19)
    'kanzo': ('ka-n-zo', '1SG-DIR-COMPL'),                       # leaped (2 Sam 22:30) - probably kanzo = 'ka-n-zo'
    # Round 167h more: OT partial-gloss fixes
    'siahil': ('siah-il', 'wonder-INTNS'),                       # wonder (Psalm 71:7)
    'kongvangah': ('kong-vang-ah', 'mouth-open-LOC'),            # grave's.mouth (Psalm 141:7)
    'tainate': ('tai-na-te', 'rebuke-NMLZ-PL'),                  # reproof (Proverbs 1:25)
    'mana': ('ma-na', 'envy-NMLZ'),                              # envy (Ecclesiastes 4:4)
    'pialsakin': ('pial-sak-in', 'stray-CAUS-CVB'),              # err (Isaiah 63:17)
    'kaihnelh': ('kaih-nelh', 'thorn-tangle'),                   # briers (Ezekiel 2:6)
    'naisan': ('na-isan', '2SG-own'),                            # own (blood) (Ezekiel 16:6)
    'leengguino': ('leeng-guin-o', 'vine-seed-DIM'),             # seed (Ezekiel 17:5)
    'pantah': ('pan-tah', 'young-lion'),                         # whelp/cub (Ezekiel 19:5)
    'lettamate': ('let-tama-te', 'return-repair-PL'),            # calkers (Ezekiel 27:9)
    # Round 167h more: Daniel/Minor prophets partials
    'hintheihna': ('hin-theih-na', 'life-know-NMLZ'),            # breath (Ezekiel 37:8)
    'puanunga': ('puan-unga', 'outer-court'),                    # outer.court (Ezekiel 42:3)
    'khuapihuam': ('khuapi-huam', 'city-possession'),            # city.possession (Ezekiel 48:20)
    'khemete': ('kheme-te', 'toe-PL'),                           # toes (Daniel 2:41)
    'tamngaite': ('tamngai-te', 'flute-PL'),                     # flutes (Daniel 3:5)
    'khuatheihna': ('khua-theih-na', 'mind-know-NMLZ'),          # understanding (Daniel 4:34)
    'khantoh': ('khan-toh', 'generation-tax'),                   # taxes/glory (Daniel 11:20)
    'sianthosakna': ('siangtho-sak-na', 'holy-CAUS-NMLZ'),       # purge (Daniel 11:35)
    'ommah': ('om-mah', 'exist-EMPH'),                           # born (Hosea 2:3)
    'balthanggawp': ('bal-thang-gawp', 'bite-rend-together'),    # tear (Hosea 13:8)
    # Round 167i: Minor prophets partials
    'ciingte': ('ciing-te', 'vine.dresser-PL'),                  # vinedressers (Joel 1:11)
    'kiluansakna': ('ki-luan-sak-na', 'REFL-pour-CAUS-NMLZ'),    # pouring (Joel 2:30)
    'meikatna': ('mei-kat-na', 'fire-burn-NMLZ'),                # fire (Joel 2:30)
    'duhduhin': ('duh-duh-in', 'want-REDUP-ERG'),                # at.will (Amos 6:4)
    'ngapi': ('nga-pi', 'fish-big'),                             # great.fish (Jonah 1:17)
    'gunpite': ('gun-pi-te', 'river-big-PL'),                    # rivers (Nahum 1:4)
    'itluatna': ('it-luat-na', 'love-exceed-NMLZ'),              # jealousy (Zechariah 8:2)
    'summeet': ('sum-meet', 'money-poor'),                       # poor (Zechariah 11:7)
    # Round 167i: High-frequency partials
    'taii': ('taii', 'rebuke'),                                  # rebuke (32x in corpus)
    'emerald': ('emerald', 'emerald'),                           # English loan word (5x)
    'mangthangte': ('mangthang-te', 'glory-PL'),                 # glory.ones (2x)
    'puansungsilh': ('puan-sung-silh', 'cloth-inside-wipe'),     # inner.garment (2x)
    # Round 167i more: Job/Psalms/Prophets partials
    'kaite': ('kait-e', 'consume-DECL'),                         # consumed (Job 7:9) - kait = consume
    'nikten': ('nikten', 'dust'),                                # dust (Job 27:16)
    'khawhletzo': ('khawh-let-zo', 'pierce-return-COMPL'),       # fill.with (Job 41:7)
    'ansite': ('ansi-te', 'chaff-PL'),                           # chaff (Psalm 35:5)
    'kaisakin': ('ka-isak-in', '1SG-rise.CAUS-ERG'),             # rise (Psalm 135:7)
    'kongkhuam': ('kong-khuam', '1SG→3-threshold'),              # threshold (Ezekiel 43:8)
    'kamciamsa': ('ka-mciam-sa', '1SG-vow-NOM'),                  # vowed (Malachi 1:14)
    'santak': ('san-tak', 'stand-remain'),                       # stood (Matthew 2:9)
    'kahtohpih': ('kah-toh-pih', 'climb-up-with'),               # set (Matthew 4:5) - phonotactic fix
    # Round 167j: More Gospel partials
    'dangate': ('dang-a-te', 'other-REL-PL'),                    # others (Ezekiel 40:28)
    'bate': ('ba-te', 'pledge-PL'),                              # pledges (Habakkuk 2:6)
    'tungthamah': ('tung-thamah', 'on-outside'),                 # outwardly (Matthew 7:15)
    'sialtalling': ('sial-tal-ling', 'thorn-grow-wild'),         # thistles (Matthew 7:16)
    'naksiat': ('nak-siat', '2SG.great-spoil'),                  # fall/ruin (Matthew 7:27) - phonotactic fix
    'kengthuah': ('keng-thuah', 'carry-extra'),                  # extra (Matthew 10:10)
    'sammal': ('sam-mal', 'hair-all'),                           # hairs.all (Matthew 10:30)
    'itzawte': ('it-zaw-te', 'love-more-PL'),                    # love.more (Matthew 10:37)
    'kimawlte': ('ki-mawl-te', 'REFL-play-PL'),                  # playing (Matthew 11:16)
    # Round 167j more: Matthew partials
    'mangbuhvuite': ('mangbuh-vui-te', 'grain-ear-PL'),          # ears.of.corn (Matthew 12:1)
    'lametet': ('lamet-et', 'example-indeed'),                   # indeed (Matthew 12:23)
    'kitawphahna': ('ki-taw-phah-na', 'REFL-cover-rock-NMLZ'),   # stony.places (Matthew 13:5)
    'hihtakpi': ('hih-tak-pi', 'be.II-real-EMPH'),              # truly.be (Matthew 14:28) - hih is Form II
    'kaikhawmsak': ('ka-i-khawm-sak', '1SG-DIR-gather-CAUS'),    # gather (Matthew 24:31)
    'bangcite': ('bang-ci-te', 'what-say-PL'),                   # which.ones (Matthew 24:45)
    'simmatin': ('sim-mat-in', 'deceive-snare-ERG'),             # by.subtilty (Matthew 26:4)
    'limnap': ('lim-nap', 'sign-deep'),                          # kissed (Matthew 26:49)
    'kipatthakna': ('ki-pat-thak-na', 'REFL-begin-new-NMLZ'),    # renewal (Isaiah 6:13)
    # Round 167j more: Mark/Luke partials
    'hihpak': ('hih-pak', 'be.II-ABIL'),                         # can.be (Matthew 26:50) - hih is Form II
    'galzuih': ('gal-zuih', 'far-follow'),                       # follow.afar (Matthew 26:58)
    'hualin': ('hual-in', 'roll-ERG'),                           # roll (Matthew 27:60)
    'nungzuih': ('nung-zuih', 'behind-follow'),                  # follow.after (Mark 1:36)
    'khawlpah': ('khawl-pah', 'dry-COMPL'),                      # dried.up (Mark 5:29)
    'lingkawmin': ('ling-kawm-in', 'tremble-together-ERG'),      # trembling (Mark 5:33)
    'pawlkhatah': ('pawl-khat-ah', 'group-one-LOC'),             # in.groups (Mark 6:40)
    'khuakiim': ('khua-kiim', 'town-border'),                    # borders (Mark 7:24)
    'sawnpaih': ('sawn-paih', 'table-push'),                     # overthrew (Mark 11:15)
    'hihnu': ('hih-nu', 'this-after'),                           # after.this (Mark 12:23) - hih as demonstrative here
    'pilvangin': ('pil-vang-in', 'learn-guard-ERG'),             # watch (Mark 14:38)
    'minnei': ('min-nei', 'name-have'),                          # named (Luke 1:5)
    # Round 167k: Luke/Acts partials
    'hihtheihna': ('hih-theih-na', 'be.II-ABIL-NMLZ'),           # ability (Luke 4:13) - hih is Form II
    'gunkuangte': ('gunkuang-te', 'boat-PL'),                    # ships (Luke 5:3)
    'pahtakbawl': ('pah-tak-bawl', 'praise-real-do'),            # speak.well.of (Luke 6:26)
    # Round 167k more: Luke/John partials
    'taanlawhte': ('taan-lawh-te', 'lose-away-PL'),              # those.who.lose (Matthew 10:39)
    'nakgen': ('nak-gen', 'much-speak'),                         # tell.much (Mark 1:45)
    'kongkawcipsak': ('kong-kaw-cip-sak', '1SG→3-convulse-tight-CAUS'), # tear (Luke 9:39)
    'mawhzon': ('mawh-zon', 'guilty-seek'),                      # accuse (Luke 11:53)
    'anvakna': ('an-vak-na', '3PL-repay-NMLZ'),                  # recompense (Luke 14:12)
    'aptheih': ('a-p-theih', '3SG-give-ABIL'),                   # deliver (Luke 20:20)
    'kipiaknate': ('ki-piak-na-te', 'REFL-give-NMLZ-PL'),        # offerings (Luke 21:5)
    'ahihkhak': ('a-hih-khak', '3SG-be.II-if'),                  # if.it.be (Luke 22:42) - hih is Form II
    'kipawlte': ('ki-pawl-te', 'REFL-ally-PL'),                  # companions (Luke 22:59)
    'talapte': ('talap-te', 'porch-PL'),                         # porches (John 5:3)
    # Round 167l: John/Acts/Romans partials
    'kihukna': ('ki-huk-na', 'REFL-dig-NMLZ'),                   # cave (John 11:38)
    'mainulpi': ('mai-nul-pi', 'face-wipe-cloth'),               # towel (John 13:4)
    'sawpsiangsak': ('sawp-siang-sak', 'wipe-clean-CAUS'),       # blot.out (Acts 3:18)
    'pawlmat': ('pawl-mat', 'ally-friend'),                      # befriend (Acts 12:20)
    'pakkualte': ('pak-kual-te', 'flower-wreath-PL'),            # garlands (Acts 14:13)
    'sawtna': ('sawt-na', 'long-NMLZ'),                          # long.time (Acts 16:18)
    'palikbute': ('palik-bu-te', 'police-group-PL'),             # sergeants (Acts 16:35)
    'tangtut': ('tang-tut', 'hold-complete'),                    # finish (Acts 20:24)
    'kiphelna': ('ki-phel-na', 'REFL-defend-NMLZ'),              # defense (Acts 26:2)
    'ihihlam': ('i-hih-lam', '1PL.INCL-be.II-manner'),           # "as we being" (Romans 6:3) - hih is Form II of hi
    # Round 167l more: Epistles/OT partials
    'tangdinzo': ('tang-din-zo', 'hold-stand-COMPL'),            # complete.without (1 Corinthians 11:11)
    'samsau': ('sam-sau', 'hair-long'),                          # long.hair (1 Corinthians 11:15)
    'daihsakna': ('daih-sak-na', 'silence-CAUS-NMLZ'),           # silencing (Psalm 8:2)
    'lukhu': ('lu-khu', 'head-crown'),                           # crown (Exodus 29:6)
    # Round 167m: Epistles partials
    'namdangpi': ('nam-dang-pi', 'nation-other-big'),            # foreigner (1 Corinthians 14:11)
    'kisialhpihna': ('ki-sialh-pih-na', 'REFL-boast-APPL-NMLZ'), # boasting (2 Corinthians 8:24)
    'patun': ('pa-tun', 'father-arrive'),                        # by.birth (Galatians 2:15)
    'kilunggulhna': ('ki-lung-gulh-na', 'REFL-heart-desire-NMLZ'), # lust (1 Thessalonians 4:3)
    'phuahtawmte': ('phuah-tawm-te', 'make-false-PL'),           # fables (1 Timothy 4:7)
    'kisinna': ('ki-sin-na', 'REFL-train-NMLZ'),                 # exercise (1 Timothy 4:8)
    'nangzote': ('nang-zo-te', 'endure-COMPL-PL'),               # endure (James 1:12)
    # Round 167m more: Genesis/OT partials
    'zawtzawt': ('zawt~zawt', 'grope~REDUP'),                    # groped (Genesis 19:11)
    'ciamnui': ('ciam-nui', 'promise-laugh'),                    # joke (Genesis 19:14)
    'nuihzak': ('nuih-zak', 'laugh-spread'),                     # laugh (Genesis 21:6)
    'gamdung': ('gam-dung', 'land-length'),                      # length (Genesis 13:17)
    'gamvai': ('gam-vai', 'land-breadth'),                       # breadth (Genesis 13:17)
    'buangun': ('buan-gun', 'pass-by'),                          # pass.by (Genesis 18:3)
    'khakhia': ('kha-khia', 'drive-away'),                       # sent.away (Genesis 12:20)
    'awngthawlpi': ('awng-thawl-pi', 'open-waste-big'),          # void (Genesis 1:2)
    # Round 167n: More OT/Revelation partials
    'kipatcil': ('ki-pat-cil', 'REFL-begin-old'),                # from.beginning (3 John 1:5)
    'awmgak': ('awm-gak', 'waist-bind'),                         # girded (Revelation 1:13)
    'gualzote': ('gual-zo-te', 'win-COMPL-PL'),                  # overcomers (Revelation 3:12)
    'kalkakin': ('kal-kak-in', 'step-stand-ERG'),                # standing.on (Revelation 10:5)
    'kanggawp': ('kang-gawp', 'burn-together'),                  # scorched (Revelation 16:8)
    'suangtawphahte': ('suang-taw-phah-te', 'stone-floor-spread-PL'), # foundations (Revelation 21:14)
    'kicinsakna': ('ki-cin-sak-na', 'REFL-complete-CAUS-NMLZ'),  # perfected (James 2:22)
    
    # Round 169: Phonotactic fixes - compounds with invalid *ht, *ps, *hh onsets
    # kipsak (98x) - establish covenant - kip + sak = firm + CAUS = "make firm"
    # NOT ki-piak-sak (REFL-give-CAUS) - kipiaksak only appears 1x
    'kipsak': ('kip-sak', 'firm-CAUS'),                          # establish (Genesis 6:18)
    'kipsakin': ('kip-sak-in', 'firm-CAUS-CVB'),                 # establishing (7x)
    'kipsaksa': ('kip-sak-sa', 'firm-CAUS-PERF'),                # established (3x)
    'kipsaknate': ('kip-sak-na-te', 'firm-CAUS-NMLZ-PL'),        # covenants (2x)
    # kihhuai (66x) - abomination - ki + huai (not ki + hhuai)
    'kihhuaisa': ('ki-huai-sa', 'REFL-abominate-PERF'),          # abominated (1x)
    # kahto compounds - should be kah-to (climb-up), not ka-hto
    'kahtoin': ('kah-to-in', 'climb-up-ERG'),                    # ascending
    # pahtawi (8x) - dwell with / honor - pah + tawi
    'pahtawiin': ('pah-tawi-in', 'honor-carry-ERG'),             # dwelling.with
    # husanna - foreign word, leave unsegmented
    'husanna': ('husanna', 'hosanna'),                           # hosanna (13x)
    # anne - proper noun Anna
    # Round 169c: Fix kiC compounds being misanalyzed as ki-C
    # kim (66x standalone) = "fully/all" - compounds should be kim-X not ki-mX
    'kimin': ('kim-in', 'fully-ERG'),                            # completely (9x)
    # kin (28x standalone) = "quickly/clearly" - compounds should be kin-X not ki-nX
    'kinsak': ('kin-sak', 'quickly-CAUS'),                       # quicken/revive (2x)
    'kinin': ('kin-in', 'quickly-ERG'),                          # quickly (7x)
    # Round 169d: More phonotactic fixes for invalid onsets
    # kilkel (5x) - 'clear/pure' (crystal, glass) - reduplication kil~kel
    # kansak/kansakna - 'dry up' - lexicalized compound (kan here = dry, not ask)
    'kansakna': ('kansak-na', 'dry.up-NMLZ'),                    # drying up (Josh 2:10)
    # Words with geminate nn - should not be segmented as a-nn...
    'annengte': ('Anneng-te', 'ANNENG-PL'),                      # proper name plural (2x)
    'annelte': ('annel-te', 'meal-PL'),                          # meals (2x)
    'annel': ('annel', 'meal'),                                  # meal (unsegmented)
    'anneng': ('anneng', 'crumb'),                               # crumb (unsegmented)
    # Round 169e: More phonotactic fixes
    # hihlo/hihloh - 'nothing' - hih (this) + lo/loh (NEG)
    # kipsuak - 'remain/continue' - kip (firm) + suak (become)
    'kipsuak': ('kip-suak', 'firm-become'),                      # continue/remain (4x)
    # sotto - 'each other' (reduplication) - not so-tto
    # pahpah - reduplication for emphasis
    'pahpahte': ('pah~pah-te', 'honor~REDUP-PL'),                  # honorable ones (2x)
    'pahpahin': ('pah~pah-in', 'honor~REDUP-ERG'),                 # honorably (1x)
    # kihtakhuai - kih (abhor) + takhuai (despise)
    'kihtakhuai-in': ('kih-takhuai-in', 'abhor-despise-ERG'),    # abhorring
    # naksiat - lexicalized 'ruin/destruction' (historically nak+siat)
    # alsakkik - al (salt) + sak (CAUS) + kik (ITER) = 'salt again'
    'alsakkik': ('al-sak-kik', 'salt-CAUS-ITER'),                # salt again (2x)
    # antan - an (eat/food) + tan (endure) - lexicalized
    "antan'": ("antan'", 'endure.GEN'),                          # genitive form
    'antangte': ('antan-te', 'endure-PL'),                       # plural
    # Round 169f: More phonotactic fixes
    # kahtohpih - kah (climb) + toh (up) + pih (with) - not ka-htoh-pih
    # kamciamsa - kam (word) + ciam (promise) + sa (PERF) - not ka-mciam
    'kamciamnasa': ('kam-ciam-na-sa', 'word-promise-NMLZ-PERF'), # vow (1x)
    # ankungnote - an (food) + kungno (desire) + te (PL) - not a-nkungno
    'ankungnote': ('an-kungno-te', 'food-desire-PL'),            # gluttons (2x)
    # pahtawi variants - pah (honor) + tawi (carry) - not pa-htawi  
    'pahtawite': ('pah-tawi-te', 'honor-carry-PL'),              # honored (1x)
    'pahtaklam': ('pah-taklam', 'honor-way'),                    # honored way (1x)
    # nihta - ni (day) + hta -> should be nih-ta or just lexicalized
    'nihta': ('nihta', 'certainly'),                             # certainly/indeed (1x)
    # thukpa - thu (word) + kpa -> thuk-pa (deep-person)?
    'thukpa': ('thuk-pa', 'deep-person'),                        # deep one (1x)
    'thukpah': ('thuk-pah', 'deep-honor'),                       # deep respect (1x)
    # ciltel - cil (answer) + tel -> cil-tel (answer-?) or lexicalized
    'ciltel': ('ciltel', 'response'),                            # response (1x)
    'ciltangte': ('cil-tang-te', 'answer-all-PL'),               # all answers (1x)
    # Round 169g: More phonotactic fixes (hapax and low-frequency)
    # mulnei - mul (full) + nei (have) - not mu-lnei
    'mulnei': ('mul-nei', 'full-have'),                          # have fully (1x)
    # ippi - unsegmented word for 'sack/bag'
    'ippi': ('ippi', 'sack'),                                    # sack (1x)
    # ipsung - ip (basket) + sung (inside) - not i-psung
    'ipsung': ('ip-sung', 'basket-inside'),                      # in basket (1x)
    # ihmucipin, ihmusak - ih (sleep) + mu (see) compounds - not i-hmu
    'ihmucipin': ('ih-mu-cip-in', 'sleep-see-tight-ERG'),        # sleeping tight (1x)
    'ihmusak': ('ih-mu-sak', 'sleep-see-CAUS'),                  # put to sleep (1x)
    # anpalin, anpiang, anpiakna - an (food/eat) + pial/piak - not a-np...
    'anpalin': ('an-pal-in', 'food-stray-ERG'),                  # going astray for food (1x)
    'anpiang': ('an-piang', 'food-fruit'),                       # food/fruit (1x)
    'anpiakna': ('an-piak-na', 'food-give-NMLZ'),                # food offering (1x)
    # ansangte - an (food) + sang (high) + te (PL) - not a-nsang
    'ansangte': ('an-sang-te', 'food-high-PL'),                  # high foods (1x)
    # ankante - an (food) + kan (stay) + te (PL) - not a-nkan
    'ankante': ('an-kan-te', 'food-stay-PL'),                    # remaining food (1x)
    # ancilnate - an (food) + cil (answer) + na + te - not a-ncil
    'ancilnate': ('an-cil-na-te', 'food-answer-NMLZ-PL'),        # food responses (1x)
    # kansimte - kan (stay) + sim (count) + te - not ka-nsim
    'kansimte': ('kan-sim-te', 'stay-count-PL'),                 # counting (1x)
    # tomsakin - tom (heap) + sak (CAUS) + in - not to-msak
    'tomsakin': ('tom-sak-in', 'heap-CAUS-CVB'),                 # heaping (1x)
    # khantawnun - khan (age) + tawn (along) + un - not kha-ntawn
    'khantawnun': ('khan-tawn-un', 'age-along-2PL'),             # throughout your age (1x)
    # khopsakin - khop (whole) + sak (CAUS) + in - not kho-psak
    'khopsakin': ('khop-sak-in', 'whole-CAUS-CVB'),              # making whole (1x)
    # cilbawl - cil (answer) + bawl (make) - not ci-lbawl
    'cilbawl': ('cil-bawl', 'answer-make'),                      # give answer (1x)
    # Round 169h: More hapax phonotactic fixes
    # pak- compounds (pak = wait)
    'paktatsak': ('pak-tat-sak', 'wait-strike-CAUS'),            # (1x)
    'paktatnate': ('pak-tat-na-te', 'wait-strike-NMLZ-PL'),      # (1x)
    # bal- compounds (bal = owe/bear)
    'baltat': ('bal-tat', 'bear-strike'),                        # (1x)
    'balkekna': ('bal-kek-na', 'bear-break-NMLZ'),               # (1x)
    # sal- compounds (sal = slave)
    'salsuaksa': ('sal-suak-sa', 'slave-become-PERF'),           # became slave (1x)
    'salsuakte': ('sal-suak-te', 'slave-become-PL'),             # became slaves (1x)
    # khal- compounds (khal = dew/cool)
    'khalsak': ('khal-sak', 'cool-CAUS'),                        # cool down (1x)
    'khalcip': ('khal-cip', 'cool-tight'),                       # cool tight (1x)
    'khalcipin': ('khal-cip-in', 'cool-tight-ERG'),              # (1x)
    # zap/zat- compounds
    'zattawm': ('zat-tawm', 'use-join'),                         # use together (1x)
    # kat- compounds (should be kat-tum, not ka-ttum)
    'kattumna': ('kat-tum-na', 'strike-end-NMLZ'),               # (1x)
    'kattumsa': ('kat-tum-sa', 'strike-end-PERF'),               # (1x)
    'kattumsak': ('kat-tum-sak', 'strike-end-CAUS'),             # (1x)
    # at- compounds (at = tie/bind)
    'attatsak': ('at-tat-sak', 'tie-strike-CAUS'),               # (1x)
    'atsat': ('at-sat', 'tie-attach'),                           # (1x)
    # Other hapax
    'natsak': ('nat-sak', 'pain-CAUS'),                          # cause pain (1x)
    'topsa': ('top-sa', 'gather-PERF'),                          # gathered (1x)
    'toksuah': ('tok-suah', 'sit-happen'),                       # (1x)
    "namsau'": ("nam-sau'", 'sword-long.GEN'),                   # (1x)
    'kahtosak': ('kah-to-sak', 'climb-up-CAUS'),                 # cause to ascend (1x)
    'khiamsak': ('khiam-sak', 'reduce-CAUS'),                    # reduce (1x)
    'khankik': ('khan-kik', 'age-ITER'),                         # age again (1x)
    'apsate': ('ap-sa-te', 'press-PERF-PL'),                     # pressed (1x)
    'apsak': ('ap-sak', 'press-CAUS'),                           # press (1x)
    'kapsak': ('kap-sak', 'cry-CAUS'),                           # cause to cry (1x)
    'anpiate': ('an-pia-te', 'food-give-PL'),                    # food givers (1x)
    'anpiangte': ('an-piang-te', 'food-fruit-PL'),               # fruits (1x)
    'zinsuk': ('zin-suk', 'journey-rest'),                       # rest from journey (1x)
    'zintohna': ('zin-toh-na', 'journey-up-NMLZ'),               # journey up (1x)
    'kalteng': ('kal-teng', 'go-upright'),                       # go upright (1x)
    'vekpite': ('vek-pi-te', 'all-big-PL'),                      # all big ones (1x)
    'khansakna': ('khan-sak-na', 'age-CAUS-NMLZ'),               # aging (1x)
    'ihsip': ('ih-sip', 'sleep-seep'),                           # (1x)
    'kamka': ('kamka', 'ashamed'),                                # ashamed/confounded (Job 6:20)
    'kahzo': ('kah-zo', 'climb-reach'),                          # climb reach (1x)
    'thuktawng': ('thuk-tawng', 'deep-speak'),                   # speak deeply (1x)
    'mutsiang': ('mut-siang', 'face-bright'),                    # bright face (1x)
    'annektawm': ('an-nek-tawm', 'food-eat-join'),               # eat together (1x)
    # Round 169i: More hapax phonotactic fixes
    # nam- compounds (nam = sword/tribe)
    'nampi': ('nam-pi', 'tribe-big'),                            # big tribe (1x)
    'namkimte': ('nam-kim-te', 'tribe-all-PL'),                  # all tribes (1x)
    'namkimin': ('nam-kim-in', 'tribe-all-ERG'),                 # (1x)
    'namtuisak': ('nam-tui-sak', 'sword-water-CAUS'),            # (1x)
    # kal- compounds (kal = go)
    'kaltangnate': ('kal-tang-na-te', 'go-upright-NMLZ-PL'),     # (1x)
    'kalkawm': ('kal-kawm', 'go-meet'),                          # go meet (1x)
    # nal/pal- compounds
    'nalsak': ('nal-sak', 'straighten-CAUS'),                    # straighten (1x)
    'palsatnate': ('pal-sat-na-te', 'stray-attach-NMLZ-PL'),     # (1x)
    # ban- compounds (ban = arm/owe)
    'bansak': ('ban-sak', 'arm-CAUS'),                           # (1x)
    # tok- compounds (tok = peck/sit)
    'toktok': ('tok~tok', 'peck~REDUP'),                           # pecking (reduplication)
    # Note: sinsona = 'wrath' (opaque lexeme, see line ~15277)
    # NOT sin-sona (sin = 'near', doesn't yield 'wrath')
    'sinsanna': ('sin-san-na', 'near-hang-NMLZ'),               # shaking/wavering (Isa 19:16)
    "sinsin'": ("sin~sin'", 'near~REDUP.POSS'),                   # skipping (Jer 48:27)
    # ih- compounds (ih = sleep)
    'ihmucip': ('ih-mu-cip', 'sleep-see-tight'),                 # deep sleep (1x)
    # khia- compounds
    'khiapsak': ('khiap-sak', 'squeeze-CAUS'),                   # (1x)
    'khiamsuk': ('khiam-suk', 'reduce-rest'),                    # (1x)
    # khan- compounds (khan = age/era)
    'khantom': ('khan-tom', 'age-end'),                          # end of age (1x)
    'khansihin': ('khan-sih-in', 'age-know-ERG'),                # (1x)
    # nak- compounds
    'naksuk': ('nak-suk', 'nose-rest'),                          # (1x)
    'naktoh': ('nak-toh', 'nose-up'),                            # (1x)
    'naksiatzaw': ('nak-siat-zaw', 'nose-destroy-more'),         # (1x)
    # nat- compounds (nat = pain)
    'natsia': ('nat-sia', 'pain-bad'),                           # (1x)
    'nattun': ('nat-tun', 'pain-endure'),                        # (1x)
    # mik- compounds (mik = eye)
    # keh- compounds
    # kam- compounds (kam = word)
    'kamsiam': ('kam-siam', 'word-skilled'),                     # skilled in words (1x)
    'kamsak': ('kam-sak', 'word-CAUS'),                          # (1x)
    # bah- compounds (bah = owe)
    'bahtoh': ('bah-toh', 'owe-up'),                             # (1x)
    # an- compounds
    'ansukna': ('an-suk-na', 'food-rest-NMLZ'),                  # (1x)
    # pat/vat- compounds
    'vattansak': ('vat-tan-sak', 'hold-endure-CAUS'),            # (1x)
    # pam- compounds
    'pampamin': ('pam~pam-in', 'spread~REDUP-ERG'),                # (reduplication)
    # tui- compounds
    'tuihtuihin': ('tuih~tuih-in', 'hang~REDUP-ERG'),              # (reduplication)
    # pua- compounds
    'puamcin': ('puam-cin', 'belly-small'),                      # (1x)
    # mil/mul- compounds
    'milmel': ('mil-mel', 'smooth-soft'),                        # (1x)
    'mulmette': ('mul-met-te', 'full-soft-PL'),                  # (1x)
    # khal- compounds
    'khalguah': ('khal-guah', 'cool-pour'),                      # (1x)
    # at- compounds
    'atsa': ('at-sa', 'tie-PERF'),                               # (1x)
    'atkik': ('at-kik', 'tie-ITER'),                             # (1x)
    # kap- compounds
    'kapsim': ('kap-sim', 'cry-think'),                          # (1x)
    # tom- compounds
    'tommet': ('tom-met', 'heap-soft'),                          # (1x)
    # kan- compounds
    'kankik': ('kan-kik', 'stay-ITER'),                          # (1x)
    # kah- compounds
    'kahnate': ('kah-na-te', 'climb-NMLZ-PL'),                   # (1x)
    'kahzaw': ('kah-zaw', 'climb-more'),                         # (1x)
    # an- compounds
    'ancil': ('ancil', 'food.offering'),                         # lexicalized (1x)
    # nah- compounds
    'nahteh': ('nah-teh', 'near-cut'),                           # (1x)
    # sal- compounds
    'salpihte': ('sal-pih-te', 'slave-with-PL'),                 # (1x)
    # cit- compounds
    'citpiak': ('cit-piak', 'go-give'),                          # (1x)
    # Round 169j: Final batch of phonotactic fixes
    # kel- compounds
    'kelkelna': ('kel~kel-na', 'leave~REDUP-NMLZ'),                # (reduplication)
    # am- compounds
    'amsakin': ('am-sak-in', 'cover-CAUS-CVB'),                  # (1x)
    # mut- compounds
    'mutsia': ('mut-sia', 'face-bad'),                           # (1x)
    # an- compounds  
    'ansing': ('an-sing', 'food-true'),                          # (1x)
    'antehna': ('an-teh-na', 'food-cut-NMLZ'),                   # (1x)
    'antannate': ('an-tan-na-te', 'food-endure-NMLZ-PL'),        # (1x)
    # san- compounds
    'santeng': ('san-teng', 'hang-upright'),                     # (1x)
    'sansanah': ('san~san-ah', 'hang~REDUP-LOC'),                  # (reduplication)
    # nen- compounds
    'nenniamnate': ('nen-niam-na-te', 'soft-humble-NMLZ-PL'),    # (1x)
    # kido- compounds (kidom = catch)
    'kidomto': ('kidom-to', 'catch-sit'),                        # (1x)
    # kal- compounds
    'kallakah': ('kal-lak-ah', 'go-back-LOC'),                   # (1x)
    # kap- compounds
    'kapsuk': ('kap-suk', 'cry-rest'),                           # (1x)
    # nil- compounds
    'nilsuk': ('nil-suk', 'light-rest'),                         # (1x)
    # tol- compounds
    'tolsak': ('tol-sak', 'follow-CAUS'),                        # (1x)
    # cil- compounds
    'cilgawp': ('cil-gawp', 'answer-strike'),                    # (1x)
    'cilsate': ('cil-sa-te', 'answer-PERF-PL'),                  # (1x)
    # bal- compounds
    'balnensak': ('bal-nen-sak', 'bear-soft-CAUS'),              # (1x)
    'balkeksak': ('bal-kek-sak', 'bear-break-CAUS'),             # (1x)
    # lauh- compounds (reduplication)
    'lauhlauh': ('lauh~lauh', 'rattle~REDUP'),                       # onomatopoeia for rattling (Nahum 3:2)
    # ban- compounds
    'bantan': ('ban-tan', 'arm-endure'),                         # (1x)
    # pal- compounds
    'palsatte': ('pal-sat-te', 'stray-attach-PL'),               # (1x)
    # khuan- compounds
    'khuankuan': ('khuan-kuan', 'village~REDUP'),              # (1x)
    # nat- compounds
    'nattutna': ('nat-tut-na', 'pain-endure-NMLZ'),              # (1x)
    # nul- compounds
    'nulsaknu': ('nul-sak-nu', 'push-CAUS-mother'),              # (1x)
    # nak- compounds
    'nakpau': ('nakpau', 'vehemently'),                            # vehemently/fiercely (Luke 23:5)
    # val- compounds
    'valsak': ('val-sak', 'hold-CAUS'),                          # (1x)
    # nuh/kah- compounds
    'nuhkawmin': ('nuh-kawm-in', 'press-meet-ERG'),              # (1x)
    'kahkawmin': ('kah-kawm-in', 'climb-meet-ERG'),              # (1x)
    'kahkawmun': ('kah-kawm-un', 'climb-meet-2PL'),              # (1x)
    'kahtohpihin': ('kah-toh-pih-in', 'climb-up-with-ERG'),      # (1x)
    # it- compounds
    'itteng': ('it-teng', 'love-upright'),                       # (1x)
    'itkik': ('it-kik', 'love-ITER'),                            # (1x)
    # sin- compounds
    'sinsanin': ('sin-san-in', 'trust-hang-ERG'),                # (1x)
    'sinnateng': ('sin-na-teng', 'trust-NMLZ-upright'),          # (1x)
    'sinsenin': ('sin-sen-in', 'trust-hang-ERG'),                # (1x)
    'sinsa': ('sin-sa', 'trust-PERF'),                           # (1x)
    # ih- compounds
    'ihmusip': ('ihmu-sip', 'sleep-deep'),                        # deep sleep (Acts 20:9)
    # toh- compounds (reduplication)
    'tohtoh': ('toh~toh', 'stand~REDUP'),                            # continuously/persistently (Acts 24:25)
    # zat- compounds
    'zatsak': ('zat-sak', 'use-CAUS'),                           # (1x)
    'zatsiamte': ('zat-siam-te', 'use-skilled-PL'),              # (1x)
    # nak- compounds
    'nakkin': ('nak-kin', 'nose-quickly'),                       # (1x)
    # up- compounds
    'upsa': ('up-sa', 'blow-PERF'),                              # (1x)
    # pah- compounds
    'pahtawizawk': ('pah-tawi-zawk', 'honor-carry-more'),        # (1x)
    # kek- compounds
    # zawn- compounds
    'zawnnate': ('zawn-na-te', 'seek-NMLZ-PL'),                  # (1x)
    # tai- compounds
    'taihsak': ('taih-sak', 'rebuke-CAUS'),                      # (1x)
    
    # Round 170: Resolve remaining 2x partials via KJV cross-reference
    # Animal care/agriculture
    'buhkung': ('buhkung', 'provender'),                         # (2x) animal feed - Gen 24:32
    'buhkungte': ('buhkung-te', 'provender-PL'),
    # Siege warfare  
    'dum': ('dum', 'siege.mound'),                               # (2x) siege works - Ezek 4:2
    'dumte': ('dum-te', 'siege.mound-PL'),
    # Geography
    'guam': ('guam', 'valley'),                                  # (2x) valleys - Ezek 36:4
    'guamte': ('guam-te', 'valley-PL'),
    'guamteng': ('guam-teng', 'valley-all'),
    # Sea creatures
    'gulpite': ('gulpi-te', 'dragon-PL'),
    # Snakes/vipers
    'gunei': ('gunei', 'viper'),                                 # (2x) viper/asp - Job 20:16
    'guneite': ('gunei-te', 'viper-PL'),
    # Mixed peoples
    'khawmte': ('khawm-te', 'mingled-PL'),
    # Mental/emotional states
    'meidawite': ('meidawi-te', 'feeble.minded-PL'),
    # Wedding terms
    'mothak': ('mothak', 'bride'),                               # (2x) bride - Jer 7:34
    'mothakte': ('mothak-te', 'bride-PL'),
    # Emotional/mental states
    'lungnemte': ('lung-nem-te', 'heart-soft-PL'),
    'lungzinhuai': ('lung-zinhuai', 'heart-dread'),              # (2x) anxiety - Job 15:23
    # Marriage/family
    # Creatures
    'momaite': ('momai-te', 'scorpion-PL'),
    # Verbs
    'susia': ('su-sia', 'CAUS-bad'),                             # (2x) destroy - Gen 6:13
    'susiate': ('su-sia-te', 'CAUS-bad-PL'),
    # Reflexive compounds
    'kisehtawm': ('ki-seh-tawm', 'REFL-appoint-COMPL'),          # (2x) called/appointed - Heb 5:4
    'kilangbawl': ('ki-lang-bawl', 'REFL-visible-make'),         # (2x) witchcraft - Gal 5:20
    'kilangbawlna': ('ki-lang-bawl-na', 'REFL-visible-make-NMLZ'),
    'kithuahpih': ('ki-thuah-pih', 'REFL-associate-APPL'),       # (2x) kinsmen - Ps 38:11
    'kithuahpihte': ('ki-thuah-pih-te', 'REFL-associate-APPL-PL'),
    # Materials
    'suangkhi': ('suangkhi', 'coral'),                           # (2x) coral/pearls - Job 28:18
    'sumbawm': ('sum-bawm', 'money-bag'),                        # (2x) purse - Luke 22:35
    # Water/wells
    'tuibem': ('tui-bem', 'water-well'),                         # (2x) cistern - Neh 9:25
    'tuibemte': ('tui-bem-te', 'water-well-PL'),
    # Religious/abstract
    'zehphit': ('zehphit', 'desolation'),                        # (2x) abomination - Matt 24:15
    'zehphitna': ('zehphit-na', 'desolation-NMLZ'),
    # Food/materials
    'mangbuhnel': ('mangbuh-nel', 'wheat-flour'),                # (2x) wheat flour - Exod 29:2
    # Fire/burning
    'meikang': ('mei-kang', 'fire-burn'),                        # (2x) burning - Exod 21:25
    # Appearance
    'melhoihzaw': ('mel-hoih-zaw', 'face-good-COMP'),            # (2x) more handsome - 1Sam 9:2
    # Close relations
    'ulianpih': ('u-lianpih', 'elder-close'),                    # (2x) close associates - 2Ki 9:15
    'ulianpihte': ('u-lianpih-te', 'elder-close-PL'),
    # Weather/time
    'khuadam': ('khua-dam', 'weather-cold'),                     # (2x) cold - Job 24:7
    'khuamui': ('khua-mui', 'time-evening'),                     # (2x) evening/twilight - Exod 12:6
    # Places/edges
    'madawkte': ('madawk-te', 'edge-PL'),
    # Family/social
    'meigon': ('mei-gon', 'fire-extinguished'),                  # (2x) widow - Gen 38:11
    'meigonna': ('mei-gon-na', 'fire-extinguished-NMLZ'),        # widowhood
    # Birds
    'huihtun': ('huihtun', 'heron'),                             # (2x) heron - Lev 11:19
    # Vehicles/military
    'hupipa': ('hupipa', 'chariot'),                             # (2x) chariot - 2Ki 2:12
    # Abstract
    'haivai': ('haivai', 'vanity'),                              # (2x) vanity - Eccl 8:14
    # Sequential
    'henla': ('hen-la', 'that-and.SEQ'),                         # (2x) and.then - Gal 6:4
    # Verbs - causatives
    'gimsakkha': ('gim-sak-kha', 'suffer-CAUS-COMPL'),           # (2x) persecute - Rom 15:31
    # Reflexive self-states
    'kisathei': ('ki-sa-thei', 'REFL-proud-ABIL'),               # (2x) boast - 2Chr 25:19
    'kisatheite': ('ki-sa-thei-te', 'REFL-proud-ABIL-PL'),
    # Physical states
    'thakiam': ('thak-iam', 'thin-QST'),                         # (2x) lean - 2Sam 13:4
    # Animals
    'latal': ('latal', 'he.ass'),                                # (2x) male donkey - Gen 12:16
    # Reduplication - humans
    'lellel': ('lel~lel', 'mere~REDUP'),                           # (2x) mere mortal - Ps 56:11
    'lellelte': ('lel~lel-te', 'mere~REDUP-PL'),
    # Spices/herbs
    'lengmasel': ('lengmasel', 'mint'),                          # (2x) mint - Matt 23:23
    'lingsi': ('lingsi', 'balm'),                                # (2x) balm - Gen 37:25
    # Dowry
    'thalawh': ('thalawh', 'bride.price'),                       # (2x) dowry - Gen 29:18
    # Directions/positions
    'dunglam': ('dung-lam', 'back-direction'),                   # (2x) side - Exod 26:13
    # Compounds - informing
    'thukimpihin': ('thu-kim-pih-in', 'word-complete-APPL-CVB'),
    # Social roles
    'thulamlakte': ('thu-lamlak-te', 'word-advisor-PL'),
    'laihilh': ('lai-hilh', 'writing-teach'),                    # (2x) teacher - 1Cor 12:28
    'laihilhte': ('lai-hilh-te', 'writing-teach-PL'),
    # Actions
    'peksat': ('pek-sat', 'break-cut'),                          # (2x) break - Luke 8:29
    # Geography
    'luihawm': ('lui-hawm', 'river-valley'),                     # (2x) valley - Josh 8:11
    # Containers
    'kuanglekeu': ('kuang-lekeu', 'trough-wooden'),              # (2x) wooden vessel - Lev 15:12
    'kuanglekeute': ('kuang-lekeu-te', 'trough-wooden-PL'),
    # Position
    'minautang': ('mi-nau-tang', 'person-young-stand'),          # (2x) lowest - Luke 14:9
    'minautangte': ('mi-nau-tang-te', 'person-young-stand-PL'),
    # Military
    'palikmang': ('palikmang', 'captain'),                       # (2x) captain - Luke 22:4
    'palikmangte': ('palikmang-te', 'captain-PL'),
    # Age/hair
    'samkang': ('sam-kang', 'hair-gray'),                        # (2x) gray.haired - Deut 32:25
    'samkangte': ('sam-kang-te', 'hair-gray-PL'),
    # Trade goods - now handled by hierarchical compound system
    # singnamtui → 'spices' via TERNARY_COMPOUNDS
    'singnamtuite': ('sing-nam-tui-te', 'spices-PL'),
    # Numbers
    'sawmgukte': ('sawm-guk-te', 'ten-six-PL'),
    # Reduplication - looking
    'enenin': ('en~en-in', 'look~REDUP-ERG'),
    # Reduplication - oppression
    'thopthopin': ('thop~thop-in', 'oppress~REDUP-ERG'),           # (2x) reproach - Ezek 22:4
    # Tools
    'singatna': ('sing-at-na', 'wood-cut-NMLZ'),                 # (2x) saw - 2Sam 12:31
    'singatnate': ('sing-at-na-te', 'wood-cut-NMLZ-PL'),
    # Fading
    'theipal': ('thei-pal', 'know-fade'),                        # (2x) fading - Isa 28:4
    
    # Round 170b: More 2x partial resolutions
    # Restore/return
    'bangkikin': ('bang-ki-kin', 'like-REFL-ITER'),              # (2x) restore - 2Ki 5:10
    'bangsakkikin': ('bang-sak-ki-kin', 'like-CAUS-REFL-ITER'),  # (2x) cause.return - Deut 30:3
    # Agricultural/materials
    'buh': ('buh', 'straw'),                                     # (2x) straw - Gen 24:32
    # Protest/teach
    'hilhkholin': ('hilh-khol-in', 'teach-alone-ERG'),           # (2x) protest.solemnly - 1Sam 8:9
    # Fruits/plants
    'kawlsingte': ('kawlsing-te', 'pomegranate-PL'),
    # Body/appearance
    'khauhualpi': ('khau-hualpi', 'shave-big'),                  # (2x) baldness - Isa 3:24
    # Causative rest
    'khawlsakin': ('khawl-sak-in', 'rest-CAUS-CVB'),             # (2x) resting - 2Sam 6:13
    # Evil workers
    'miginalo': ('mi-gina-lo', 'person-true-NEG'),               # (2x) evil.worker - Phil 3:2
    # House parts
    'innsunte': ('inn-sun-te', 'house-shade-PL'),
    # Portions
    'pawkhat': ('paw-khat', 'portion-one'),                      # (2x) portion - Josh 19:1
    # Measurements
    'sehsawmsuah': ('seh-sawm-suah', 'appoint-ten-produce'),     # (2x) tenth.part - Rev 11:13
    'sehzah': ('seh-zah', 'appoint-measure'),                    # (2x) estimation - Lev 6:6
    # Body parts
    'utok': ('utok', 'caul'),                                    # (2x) caul (liver) - Exod 29:13
    # Partiality
    'deidanna': ('dei-dan-na', 'say-manner-NMLZ'),               # (2x) respect.of.persons - 2Chr 19:7
    # Understanding
    'mitei': ('mi-tei', 'person-understand'),                    # (2x) prudent - 1Cor 1:19
    'miteite': ('mi-tei-te', 'person-understand-PL'),
    # Sea creatures - gol = grow, pi = big (NOT go-lpi which violates phonotactics)
    # Containers
    'ipte': ('ip-te', 'sack-PL'),
    # Rising
    'tho': ('tho', 'rise'),                                      # (2x) rise/arise - Gen 19:2
    'thote': ('tho-te', 'rise-PL'),
    # Going and doing
    'taw': ('taw', 'with'),                                      # (2x) with - but tawte context needed
    'tawte': ('taw-te', 'with-PL'),
    
    # Round 170c: Foreign words and remaining 2x partials
    # Food
    'bet': ('bet', 'pottage'),                                   # (2x) pottage - Gen 25:29
    # Letters/epistles
    'koleko': ('koleko', 'epistle'),                             # (2x) letter - 2Cor 3:1
    # Spices
    'masala': ('masala', 'cummin'),                              # (2x) cummin - Isa 28:25
    # Success
    'mavan': ('ma-van', 'NEG-empty'),                            # (2x) prosperous - Gen 24:21
    # Mourning
    'mau': ('mau', 'mourn'),                                     # (2x) mourn - Neh 8:9
    # Sound instruments
    'peeng': ('peeng', 'trumpet'),                               # (2x) trumpet - Exod 19:16
    # Breeding
    'pun': ('pun', 'breed'),                                     # (2x) breed - Gen 8:17
    # Aramaic (untranslated)
    'sabakthani': ('sabakthani', 'forsaken.me[Aramaic]'),        # (2x) - Matt 27:46
    # Measurements  
    'sahin': ('sa-hin', 'six-span'),                             # (2x) six cubits - Ezek 40:5
    # Physical states
    'sanim': ('sanim', 'bruised'),                               # (2x) bruised - Lev 22:24
    # Clothing actions
    'teen': ('teen', 'gird'),                                    # (2x) girdle/gird - Lev 16:4
    # Young animals
    'tuunawi': ('tuu-nawi', 'sheep-young'),                      # (2x) lamb - Deut 32:14
    # Dowry-related
    'thalawhin': ('thalawh-in', 'bride.price-ERG'),              # (2x) for wife - Hos 12:12
    # Service
    'vaanin': ('va-an-in', 'go.and-care-ERG'),                   # (2x) keeping charge - Num 18:4
    # Gemstones
    'khrisolait': ('khrisolait', 'chrysolite'),                  # (2x) chrysolite - Ezek 28:13
    # Enmity context
    'nan': ('nan', '2PL'),                                       # (2x) - Gen 3:15 context = na+n (2SG+?)
    # ciante form
    'ciangte': ('ciang-te', 'time-PL'),                          # (2x) times - contextual
    # Watering
    'kawtsakin': ('kawt-sak-in', 'water-CAUS-CVB'),              # (2x) watereth - Isa 55:10
    # English/URL artifacts (mark as foreign)
    'bi': ('bi', 'FGN'),                                         # URL artifact
    'bible.com': ('bible.com', 'FGN'),                           # URL
    'copyright': ('copyright', 'FGN'),                           # English
    'for': ('for', 'FGN'),                                       # English
    
    # Round 171: High-frequency remaining partials
    'tuhun': ('tu-hun', 'now-time'),                             # 56x - "at this time/season"
    'tuhunin': ('tuhun-in', 'now.time-ERG'),                     # 9x - "this day" (by/at this time)
    'sinsona': ('sinso-na', 'be.angry-NMLZ'),                     # 19x - wrath (from sinso 'be angry')
    'sinsonain': ('sinso-na-in', 'be.angry-NMLZ-ERG'),
    "sinsona'": ("sinso-na'", 'be.angry-NMLZ.POSS'),               # 1x - possessive form
    'bible': ('bible', 'bible'),                                   # 4x - foreign word
    'tedim': ('tedim', 'Tedim'),                                 # 2x - language/place name
    'kristal': ('kristal', 'FGN'),                               # 2x - crystal (foreign)
    
    # Round 193: Systematic hapax compound forms
    'sakhatin': ('sakhati-n', 'cause-ERG'),                      # 1x Exo 37:8 - out of/by means of
    'lahkimna': ('lahkim-na', 'pattern-NMLZ'),                   # 1x 2Kgs 16:10 - "the pattern"
    'kikhapna': ('kikhap-na', 'pledge-NMLZ'),                    # 1x 2Kgs 18:23 - "give pledges"
    'zawdeuhte': ('zawdeuh-te', 'elder-PL'),                     # 1x 2Kgs 19:2 - "the elders"
    'vankiate': ('vankia-te', 'prey-PL'),                        # 1x 2Kgs 21:14 - "prey and spoil"
    'gatna': ('gat-na', 'weave-NMLZ'),                           # 1x 2Kgs 23:7 - "weaving place"
    'ngahthuap': ('ngah-thuap', 'get-allowance'),                # 1x 2Kgs 25:30 - "his allowance"
    'ngahthuapna': ('ngah-thuap-na', 'get-allowance-NMLZ'),      # 1x 2Kgs 25:30 - "allowance"
    'pheengte': ('pheeng-te', 'pan-PL'),                         # 1x 1Chr 9:31 - "things in pans"
    'satpukte': ('satpuk-te', 'smite-PL'),                       # 1x 2Kgs 12:21 - "those who smote"
    'zaptelte': ('zaptel-te', 'swift-PL'),                       # 1x 1Kgs 4:28 - "dromedaries"
    
    # Contracted forms with curly apostrophe (U+2019)
    "ve\u2019n": ("ve\u2019n", 'EMPH'),                          # 3x - emphatic/assertive particle
    "ve'n": ("ve'n", 'EMPH'),                                    # ASCII variant
    "nu\u2019ng": ("nu\u2019ng", 'COHORT'),                      # 2x - "let us" cohortative
    "nu'ng": ("nu'ng", 'COHORT'),                                # ASCII variant  
    "uh\u2019n": ("uh\u2019n", 'PL.EMPH'),                        # 1x - plural emphatic
    "uh'n": ("uh'n", 'PL.EMPH'),                                 # ASCII variant
    
    # More Round 193 hapax compounds
    'khennihte': ('khen-nih-te', 'divide-two-PL'),               # 1x 2Kgs 11:7 - "two parts"
    'thukuppihte': ('thu-kup-pih-te', 'word-place-APPL-PL'),     # 1x 2Kgs 25:19 - counselors
    'phinnate': ('phinna-te', 'provoke-PL'),                     # 1x 2Kgs 23:26 - "provocations"
    'ninbulomtangin': ('nin-bulom-tang-in', 'day-ruin-hang-ERG'), # 1x 2Kgs 19:25 - ruinous heaps
    'phualte': ('phual-te', 'camp-PL'),                          # 4x - camps/journeys (Num 33)
    'ipipna': ('ipip-na', 'endure-NMLZ'),                        # 2x - forbearing/patience
    'hiau': ('hiau', 'directly'),                                # 1x - went directly (Luke 4:30)
    'hiauhiau': ('hiau~hiau', 'gently~REDUP'),                   # 1x - softly (Acts 27:13)
    
    # Round 193b: More hapax
    'anphalte': ('an-phal-te', 'grain-bound-PL'),                # 1x Micah 4:12 - "sheaves"
    'awngte': ('awng-te', 'young-PL'),                           # 1x Gen 33:13 - "herds with young"
    'bakte': ('bak-te', 'cave-PL'),                              # 1x Isa 2:19 - "caves"
    'buite': ('bui-te', 'hole-PL'),                              # 1x Isa 2:19 - "holes"
    'bawlung': ('bawlung', 'ball'),                              # 1x Isa 22:18 - "like a ball"
    'bengbengte': ('bengbeng-te', 'slap-PL'),                    # 1x 2Cor 11:20 - "smite on face"
    'bungte': ('bung-te', 'tablet-PL'),                          # 1x Isa 3:20 - "tablets" (ornaments)
    'bulhna': ('bulh-na', 'bind-NMLZ'),                          # 1x Jer 20:2 - "stocks" (restraint)
    'bumna': ('bum-na', 'deceive-NMLZ'),                         # 1x Isa 47:12 - "sorceries"
    'ciampelin': ('ciam-pel-in', 'promise-break-ERG'),           # 1x 2Tim 3:4 - "traitors"
    'ciampelna': ('ciam-pel-na', 'promise-break-NMLZ'),          # 1x Rom 1:31 - "covenantbreakers"
    'ciamtehteh': ('ciam-tehteh', 'promise-beseech'),            # 1x Isa 64:9 - "we beseech"
    'zingtho': ('zing-tho', 'morning-early'),                    # 1x Prov 31:15 - "riseth early"
    'zingciangin': ('zing-ciang-in', 'morning-time-ERG'),        # 1x Esth 5:14 - "in the morning"
    
    # Round 193c: More hapax
    'dapphahte': ('dapphah-te', 'precious.cloth-PL'),            # 1x Ezek 27:20 - "precious clothes"
    'dawhna': ('dawh-na', 'cut-NMLZ'),                           # 1x Joel 3:13 - "sickle"
    'deldel': ('del~del', 'tremble~REDUP'),                      # 1x James 2:19 - "tremble"
    'deuhte': ('deuh-te', 'more-PL'),                            # 1x 2Kgs 19:2 - "elders"
    'dimsakte': ('dimsak-te', 'fill-PL'),                        # 1x Zeph 1:9 - "those who fill"
    'dongte': ('dong-te', 'end-PL'),                             # 1x Psa 73:17 - "their end"
    'dopna': ('dop-na', 'guard-NMLZ'),                           # 1x 2Cor 1:23 - "witness/record"
    'gaisakna': ('gaisak-na', 'birth-NMLZ'),                     # 1x Matt 1:18 - "birth"
    'galmuhin': ('gal-muh-in', 'far-see-ERG'),                   # 1x Heb 11:13 - "afar off"
    'galpanmun': ('gal-pan-mun', 'enemy-protect-place'),         # 1x Psa 89:40 - "strongholds"
    'ehna': ('eh-na', 'cleave-NMLZ'),                            # 1x Eccl 10:9 - "cleaveth wood"
    
    # Round 193d: Compound words with common patterns
    'kaihkhopte': ('kaih-khop-te', 'gather-PL'),                 # 1x Isa 57:13 - "companies"
    'khuakongpi': ('khua-kong-pi', 'town-gate-big'),             # 1x Jer 51:30 - "holds/strongholds"
    'lungdamkoh': ('lungdam-koh', 'rejoice-call'),               # 1x 2Cor 9:12 - "thanksgiving"
    'lungmuannate': ('lung-muanna-te', 'heart-peace-PL'),        # 1x Ezek 7:11 - "multitude"
    'hehnate': ('hehna-te', 'anger-PL'),                         # 1x - "angers/wraths"
    'khawlmunte': ('khawl-mun-te', 'rest-place-PL'),             # 1x - "resting places"
    
    # Round 193e: More hapax m-z
    'makaihte': ('makaih-te', 'leader-PL'),                      # 1x Isa 9:16 - "leaders"
    'mangzote': ('mangzo-te', 'profit-PL'),                      # 1x Heb 12:11 - "profitable ones"
    'mawlna': ('mawl-na', 'mad-NMLZ'),                           # 1x Eccl 1:17 - "madness"
    'meidawina': ('meidawi-na', 'sober.mind-NMLZ'),              # 1x 2Tim 1:7 - "sound mind"
    # suanghawmte now handled by hierarchical via BINARY_COMPOUNDS
    'suangpite': ('suangpi-te', 'stone.big-PL'),                 # 1x Psa 78:15 - "great rocks"
    'valte': ('val-te', 'young.man-PL'),                         # 1x 1Cor 15:6 - "brethren"
    'vukte': ('vuk-te', 'ice-PL'),                               # 1x Job 38:29 - "ice"
    'piksante': ('piksan-te', 'stubborn-PL'),                    # 1x Prov 16:30 - "froward"
    'phuahte': ('phuah-te', 'thunder-PL'),                       # 1x Mark 3:17 - "thunder"
    'thaguite': ('thagui-te', 'sinew-PL'),                       # 1x Job 10:11 - "sinews"
    'taksate': ('taksa-te', 'wheat-PL'),                          # 1x Matt 3:12 - "wheat" (grain)
    'talte': ('tal-te', 'buffalo-PL'),                           # 1x Isa 34:7 - "unicorns/bulls"
    'taakte': ('taak-te', 'comb-PL'),                            # 1x Psa 19:10 - "honeycomb"
    'ngimte': ('ngim-te', 'bitter-PL'),                          # 1x Psa 64:3 - "bitter words"
    'taltangah': ('taltang-ah', 'forehead-LOC'),                 # 7x Exod/1Sam - "on forehead"
    'zulhzauna': ('zulhzau-na', 'backslide-NMLZ'),              # 1x Jer 3:22 - "backslidings"
    'zulhtatna': ('zulhtat-na', 'shame-NMLZ'),                  # 1x Isa 54:4 - "shame"
    'zuausiamna': ('zuausiam-na', 'deceive-NMLZ'),              # 1x Dan 11:21 - "flatteries"
    'zuaugenna': ('zuaugen-na', 'transgress.speak-NMLZ'),       # 1x Prov 12:13 - "transgression"
    'zuaugente': ('zuaugen-te', 'transgress.speak-PL'),         # 1x - "transgressors"
    'zuauthute': ('zuauthu-te', 'transgression-PL'),            # 1x Josh 7:11 - "transgressions"
    'zukna': ('zuk-na', 'lightning-NMLZ'),                      # 1x Job 28:26 - "lightning"
    'zuksakna': ('zuksak-na', 'diminish-NMLZ'),                 # 1x 1Kgs 17:14 - "waste"
    'zomna': ('zom-na', 'continue-NMLZ'),                       # 1x Ezra 5:5 - "cease"
    'zinzinna': ('zinzin-na', 'journey-NMLZ'),                  # 1x 2Cor 11:26 - "journeyings"
    'zindona': ('zindo-na', 'affection-NMLZ'),                  # 1x 2Cor 7:15 - "affection"
    'zeizaina': ('zeizai-na', 'armory-NMLZ'),                   # 1x SoS 4:4 - "armoury"
    'vutluahnate': ('vutluahna-te', 'snuffer-PL'),              # 1x Jer 52:18 - "snuffers"
    'ziazuana': ('ziazua-na', 'excellent-NMLZ'),                # 1x Esth 1:4 - "excellent majesty"
    'zialto': ('zial-to', 'uncover-also'),                      # 1x Ezek 4:7 - "uncovered"
    'zialkhol': ('zialkhol', 'prepare.to.go'),                  # 1x Jer 46:19 - "furnish/prepare"
    'zialin': ('zialin', 'stand'),                              # 1x SoS 2:9 - "standeth"
    'zialetongte': ('zialetong-te', 'way-PL'),                  # 1x Isa 2:3 - "his ways"
    'zawhthawhna': ('zawh-thawh-na', 'able-INCH-NMLZ'),         # 1x Isa 30:12 - "perverseness"
    'zawhleh': ('zawh-leh', 'able-if'),                         # 1x Mark 13:22 - "if possible"
    'zatnate': ('zatna-te', 'scarcity-PL'),                     # 1x Mic 6:10 - "scant measure"
    'zahkote': ('zahko-te', 'trust-PL'),                        # 1x Psa 119:42 - "trust"
    'vukkhalte': ('vuk-khal-te', 'ice-freeze-PL'),              # 1x Job 24:19 - "snow waters"
    'vanzatte': ('vanzat-te', 'rigging-PL'),                    # 1x Acts 27:19 - "tackling"
    'unaute': ('unau-te', 'sibling-PL'),                        # 1x Mark 3:17 - "brothers"
    'tunpihna': ('tunpih-na', 'kneel.down-NMLZ'),               # 1x 1Chr 17:16 - "hitherto"
    'tungun': ('tung-un', 'arrive-then'),                       # 1x Job 2:12 - "lifted up"
    'upmawhnate': ('upmawhna-te', 'suspicion-PL'),              # 1x 1Tim 6:4 - "evil surmisings"
    'vaikhaknate': ('vaikhakna-te', 'bone-PL'),                 # 1x Heb 11:22 - "bones"
    'vahuite': ('vahui-te', 'fitly.set-PL'),                    # 1x SoS 5:12 - "fitly set"
    'tuulebawngte': ('tuulebawng-te', 'flock-PL'),              # 1x Jer 3:24 - "flocks"
    
    # Round 193f: More hapax
    'zungbawhin': ('zung-bawhin', 'root-pull'),                 # 1x Ezek 17:9 - "pull up roots"
    'zongsatna': ('zongsat-na', 'enslave-NMLZ'),                # 1x 2Pet 2:19 - "bondage"
    'zongpah': ('zongpah', 'opportunity'),                      # 1x Matt 26:16 - "opportunity"
    'zolua': ('zolua', 'wounded'),                              # 1x Jer 37:10 - "wounded"
    'zakma': ('zakma', 'hear.before'),                          # 1x Col 1:5 - "heard before"
    'vuak': ('vuak', 'beat'),                                   # 1x Prov 23:35 - "beaten"
    'vengvangna': ('vengvang-na', 'slaughter-NMLZ'),            # 1x Ezek 26:15 - "slaughter"
    'tuikuangpite': ('tuikuangpi-te', 'basin.big-PL'),          # 1x Jer 27:18 - "vessels"
    'tuikhalte': ('tui-khal-te', 'water-freeze-PL'),            # 1x Psa 147:17 - "ice"
    'tuanthute': ('tuanthu-te', 'fable-PL'),                    # 1x 2Pet 1:16 - "fables"
    'thuvaante': ('thuvaan-te', 'companion-PL'),                # 1x Ezra 4:9 - "companions"
    'tumtheihte': ('tumtheih-te', 'kind-PL'),                   # 1x Dan 3:10 - "all kinds"
    'tumsukte': ('tumsuk-te', 'draught-PL'),                    # 1x Matt 15:17 - "draught"
    'totawm': ('totawm', 'cistern'),                            # 1x Jer 2:13 - "cisterns"
    'thukimpihna': ('thu-kimpih-na', 'word-confirm-NMLZ'),      # 1x Luke 11:16 - "sign"
    'thupinate': ('thu-pina-te', 'pleasant.thing-PL'),          # 1x Lam 1:7 - "pleasant things"
    'thupiangsate': ('thupiangsa-te', 'clearing-PL'),           # 1x 2Cor 7:11 - "clearing"
    'thumongte': ('thumong-te', 'end-PL'),                      # 1x Isa 47:7 - "latter end"
    'thutannate': ('thu-tanna-te', 'judgment-PL'),              # 1x Psa 97:2 - "judgment"
    'thukimnasate': ('thu-kimnasa-te', 'covenant-PL'),          # 1x Isa 33:8 - "covenant"
    
    # Round 193f continued: si- over-segmentation fixes
    'siacimit': ('sia-cimit', 'spoil-completely'),              # 1x Mal 3:6 - "consumed"
    'siacimitsak': ('sia-cimit-sak', 'spoil-completely-CAUS'),  # - "cause to consume"
    'siagawp': ('sia-gawp', 'spoil-all'),                       # 1x Neh 2:3 - "waste"
    'siagawppah': ('sia-gawp-pah', 'spoil-all-also'),           # - "also waste"
    'siakmit': ('siak-mit', 'measure-eye'),                     # 1x Ezek 47:3 - "cubit"
    'siakmitte': ('siak-mit-te', 'measure-eye-PL'),             # - "cubits"
    'sialam': ('sia-lam', 'evil-way'),                          # 1x Rom 1:29 - "maliciousness"
    'sialh': ('sialh', 'tomorrow'),                             # 1x Prov 27:1 - "tomorrow"
    'sialpai': ('sial-pai', 'chase-go'),                        # 1x Psa 7:5 - "persecute"
    'sialsak': ('sial-sak', 'channel-CAUS'),                    # 1x Job 38:25 - "watercourse"
    'siasakmang': ('sia-sak-mang', 'spoil-CAUS-very'),          # - "destroy utterly"
    'siasakte': ('sia-sak-te', 'spoil-CAUS-PL'),                # - "destroyers"
    'siasate': ('siasa-te', 'evil.thing-PL'),                   # - "evils"
    'siakhin': ('siak-hin', 'measure-with'),                    # - "measuring"
    'sawkkhawmna': ('sawkkhawm-na', 'betray-NMLZ'),             # 1x Luke 22:21 - "betrayeth"
    'sawkkhawmte': ('sawkkhawm-te', 'betray-PL'),               # - "betrayers"
    'sawpkhiatna': ('sawp-khiat-na', 'wash-remove-NMLZ'),       # 1x 1Pet 3:21 - "putting away"
    'sawpsiangna': ('sawp-siang-na', 'wash-clean-NMLZ'),        # 1x Titus 3:5 - "washing"
    'sankhitna': ('sankhit-na', 'receive-NMLZ'),                # 1x Acts 8:14 - "received"
    'sangaipi': ('sang-aipi', 'high-big'),                      # 1x Psa 18:33 - "high places"
    'sattantawm': ('sat-tantawm', 'cut-damage'),                # 1x Prov 26:6 - "damage"
    
    # Round 193g: More t-z hapax
    'taalna': ('taal-na', 'fall-NMLZ'),                         # 1x Psa 56:13 - "falling"
    'taalte': ('taal-te', 'fall-PL'),                           # - "fallings"
    'tanggawl': ('tang-gawl', 'single-alone'),                  # 1x 1Cor 7:8 - "unmarried"
    'tanghial': ('tang-hial', 'span-measure'),                  # 1x Lam 2:20 - "span long"
    'tanzumte': ('tanzum-te', 'joint-PL'),                      # 1x SoS 7:1 - "joints"
    'tawhtangte': ('tawhtang-te', 'key-PL'),                    # 1x Matt 16:19 - "keys"
    'tawlngate': ('tawlnga-te', 'work-PL'),                     # 1x Heb 4:10 - "works"
    'teeknute': ('teeknu-te', 'mother.in.law-PL'),              # 1x Ruth 1:14 - "mother in law"
    'teeksiate': ('teeksia-te', 'father.in.law-PL'),            # - "fathers in law"
    'tawmkhate': ('tawmkha-te', 'few-PL'),                      # 1x Jer 44:28 - "remnant"
    'tawmnate': ('tawmna-te', 'humble-PL'),                     # 1x Isa 58:5 - "afflict"
    'tawmnote': ('tawmno-te', 'small-PL'),                      # 1x Luke 12:32 - "little"
    'tenpakna': ('tenpak-na', 'dwell.tent-NMLZ'),               # 1x Jer 35:7 - "dwell in tents"
    'tenpihte': ('tenpih-te', 'marry-PL'),                      # 1x Matt 5:32 - "marry"
    'telkhehna': ('telkheh-na', 'remind-NMLZ'),                 # 1x Rom 15:15 - "putting in mind"
    'tennopna': ('tennop-na', 'desire-NMLZ'),                   # 1x Jer 42:22 - "desire"
    'tentheihna': ('tentheih-na', 'dwell-NMLZ'),                # 1x Jer 33:12 - "habitation"
    'teepkang': ('teepkang', 'medicine'),                       # 1x Prov 17:22 - "medicine"
    'teina': ('tei-na', 'prudent-NMLZ'),                        # 1x 1Cor 1:19 - "prudent"
    'teiteina': ('teitei-na', 'persistent-NMLZ'),               # 1x Luke 11:8 - "importunity"
    'tangngolte': ('tangngol-te', 'caterpillar-PL'),            # 1x Psa 105:34 - "caterpillars"
    'tahtah': ('tah~tah', 'press~REDUP'),                         # 1x Luke 6:38 - "pressed down"
    
    # Round 193h: muan- compounds
    'muanglah': ('muan-lah', 'trust-waver'),                    # 1x Jas 1:6 - "wavering"
    'muangngam': ('muan-ngam', 'trust-firm'),                   # 1x Heb 10:23 - "without wavering"
    'muangsak': ('muan-sak', 'trust-CAUS'),                     # 1x Jer 49:11 - "trust"
    'muangzo': ('muan-zo', 'trust-ABIL'),                       # 1x Job 4:18 - "put trust in"
    'maanna': ('maan-na', 'shadow-NMLZ'),                       # 1x Jer 48:45 - "shadow"
    'mainul': ('mai-nul', 'face-cloth'),                        # 1x Acts 19:12 - "handkerchiefs"
    'mangliante': ('manglian-te', 'governor-PL'),               # 1x Dan 3:3 - "governors"
    'mawkphatna': ('mawkphat-na', 'flatter-NMLZ'),              # 1x Prov 29:5 - "flattereth"
    'meilakna': ('meilak-na', 'break-NMLZ'),                    # 1x Isa 30:14 - "breaking"
    'meimapite': ('meimapi-te', 'sore-PL'),                     # 1x Isa 1:6 - "sores"
    'miaimuai': ('miaimuai', 'myriad'),                         # 1x Rev 5:11 - "ten thousand"
    'mialzawt': ('mial-zawt', 'dark-grope'),                    # 1x Job 12:25 - "grope in dark"
    'mibuppite': ('mi-buppi-te', 'person-great-PL'),            # 1x Ezek 45:17 - "princes"
    'miginate': ('migina-te', 'upright-PL'),                    # 1x Prov 2:21 - "upright"
    'miniamte': ('miniam-te', 'meek-PL'),                       # 1x Psa 149:4 - "meek"
    'mithumante': ('mithuman-te', 'righteous-PL'),              # 1x Prov 28:1 - "righteous"
    'mivomte': ('mivom-te', 'leopard-PL'),                      # 1x Jer 13:23 - "leopard"
    'monute': ('monu-te', 'daughter.in.law-PL'),                # 1x Matt 10:35 - "daughter in law"
    
    # Round 193i: a-l hapax
    'bante': ('ban-te', 'arm-PL'),                              # 1x Dan 2:32 - "arms"
    'bawkte': ('bawk-te', 'mule-PL'),                           # 1x 1Chr 12:40 - "mules"
    'biangte': ('biang-te', 'spice-PL'),                        # 1x SoS 5:13 - "spices"
    'ciimsate': ('ciimsa-te', 'counsel-PL'),                    # 1x Prov 1:5 - "counsels"
    'anvaite': ('anvai-te', 'dry-PL'),                          # 1x Jer 4:11 - "dry wind"
    'anzapna': ('anzap-na', 'winnow-NMLZ'),                     # 1x Matt 3:12 - "fan"
    'dawilutna': ('dawilut-na', 'overcome-NMLZ'),               # 1x Acts 19:16 - "overcame"
    'cilphihna': ('cilphih-na', 'spit-NMLZ'),                   # 1x Isa 50:6 - "spitting"
    'cinghte': ('cingh-te', 'poor-PL'),                         # 1x Prov 14:21 - "poor"
    'beimangsakna': ('bei-mangsak-na', 'finish-destroy-NMLZ'),  # 1x Ezek 25:16 - "destroy"
    'beisakmangna': ('bei-sakmang-na', 'finish-destroy-NMLZ'),  # 1x Esth 3:13 - "destroy"
    'atkhiatsakna': ('at-khiatsak-na', 'cut-off-NMLZ'),         # 1x 1Chr 19:4 - "cut off"
    
    # Round 193j: na- over-segmentation fixes
    'nawngkai': ('nawng-kai', 'wrong-do'),                      # 1x Acts 4:2 - "grieved"
    'nawngkaina': ('nawng-kai-na', 'wrong-do-NMLZ'),            # - "wrongdoing"
    'nawngkaisa': ('nawng-kai-sa', 'wrong-do-already'),         # - "wronged"
    'nawngkaisakin': ('nawng-kai-sak-in', 'wrong-do-CAUS-with'), # - "causing wrong"
    'nawngkaisakte': ('nawng-kai-sak-te', 'wrong-do-CAUS-PL'),  # - "wrongdoers"
    'nawngkaisakzo': ('nawng-kai-sak-zo', 'wrong-do-CAUS-ABIL'), # - "able to wrong"
    'nawnglakte': ('nawng-lak-te', 'wrong-PL'),                 # - "wrongs"
    'nawngpi': ('nawng-pi', 'wrong-big'),                       # - "great wrong"
    'nawkna': ('nawk-na', 'convert-NMLZ'),                      # 1x Acts 15:3 - "conversion"
    'nawkzawh': ('nawk-zawh', 'do.again-ABIL'),                 # 1x Phil 4:13 - "can do"
    'nawkgawpin': ('nawk-gawp-in', 'again-all-with'),           # - "all again"
    'nailung': ('nai-lung', 'fig-heart'),                       # 1x Luke 17:6 - "sycamine"
    'nehphei': ('neh-phei', 'lean-on'),                         # 1x John 13:25 - "lying on breast"
    'neihse': ('neih-se', 'have-more'),                         # 1x 1Cor 7:40 - "happier"
    'nekledawn': ('nek-ledawn', 'eat-drink'),                   # 1x Rom 14:17 - "meat and drink"
    'nektumsak': ('nek-tum-sak', 'eat-all-CAUS'),                 # 1x Psa 105:35 - "devoured"
    'nakbuhte': ('nak-buh-te', 'nose-hang-PL'),                 # 1x Isa 3:21 - "nose jewels"
    'nakvangte': ('nakvang-te', 'nostril-PL'),                  # 1x Psa 18:8 - "nostrils"
    
    # Round 193k: p-r hapax
    'palhngulhna': ('palhngulh-na', 'stray-NMLZ'),              # 1x Psa 106:39 - "whoring"
    'pangbetna': ('pangbet-na', 'correct-NMLZ'),                # 1x Prov 22:15 - "correction"
    'phalna': ('phal-na', 'permit-NMLZ'),                       # 1x Dan 2:16 - "time/permission"
    'phamawhte': ('phamawh-te', 'necessary-PL'),                # 1x Titus 3:14 - "necessary"
    'phokna': ('phok-na', 'turn-NMLZ'),                         # 1x Isa 42:16 - "paths"
    'phualpite': ('phualpi-te', 'merchant.city-PL'),            # 1x Isa 23:11 - "merchant cities"
    'puanakte': ('puan-ak-te', 'cloth-wear-PL'),                # 1x Acts 9:39 - "coats"
    'pheekte': ('pheek-te', 'bed-PL'),                          # 1x Acts 5:15 - "beds"
    'phelthum': ('phel-thum', 'part-three'),                    # 1x Rev 16:19 - "three parts"
    'phuhna': ('phuh-na', 'sit-NMLZ'),                          # 1x Rev 2:13 - "seat"
    'phuhsate': ('phuhsa-te', 'planted-PL'),                    # 1x Jer 45:4 - "planted"
    'piakhol': ('piak-hol', 'give-return'),                     # 1x Isa 36:21 - "answer"
    'puankang': ('puan-kang', 'cloth-pure'),                    # 1x Luke 23:53 - "linen"
    
    # Round 193l: g-l hapax
    'gaite': ('gai-te', 'lame-PL'),                             # 1x Jer 31:8 - "lame"
    'galkisimna': ('galkisim-na', 'war.signal-NMLZ'),           # 1x Jer 4:21 - "standard/trumpet"
    'gambulak': ('gam-bulak', 'land-waste'),                    # 1x Isa 33:8 - "waste"
    'gawhnate': ('gawhna-te', 'understanding-PL'),              # 1x Mark 12:33 - "understanding"
    'gawngte': ('gawng-te', 'lean-PL'),                         # 1x Ezek 34:20 - "lean cattle"
    'gehsate': ('gehsa-te', 'bull-PL'),                         # 1x Isa 34:7 - "bullocks"
    'gialbem': ('gialbem', 'leopard'),                          # 1x Isa 11:6 - "leopard"
    'gimpiakte': ('gimpiak-te', 'afflict-PL'),                  # 1x Psa 88:15 - "afflicted"
    'gimsakte': ('gimsak-te', 'judge-PL'),                      # 1x Isa 59:9 - "judgment"
    'ginalopite': ('ginalopi-te', 'polluted-PL'),               # 1x Mal 1:7 - "polluted"
    'gisuangte': ('gisuang-te', 'boundary-PL'),                 # 1x Job 24:2 - "landmarks"
    'gittate': ('gitta-te', 'sparrow-PL'),                      # 1x Matt 10:29 - "sparrows"
    'guahtuite': ('guah-tui-te', 'rain-water-PL'),                # 1x Heb 6:7 - "rain"
    
    # Round 194: More hapax vocabulary
    'ngiahon': ('ngiahon', 'ravening'),                           # 1x Ezek 22:27 - "ravening prey"
    'haksapipi': ('haksa-pi~pi', 'difficult-INT~REDUP'),            # 3x Acts 27 - "hardly/with difficulty"
    'khawlmun': ('khawl-mun', 'rest-place'),                      # 1x Acts 27:8 - "havens" (Fair Havens)
    'tuani': ('tua-ni', 'that-day'),                              # 1x Josh 6:15 - "on that day"
    'tulai': ('tu-lai', 'now-time'),                              # 1x 1Sam 25:10 - "nowadays"
    'menzipipa': ('men-zipi-pa', 'office-great-person'),          # 4x Ezra 4 - "chancellor"
    'leihawmpi': ('lei-hawm-pi', 'earth-depth-big'),              # 3x Psalms - "hell/corruption" (Sheol)
    
    # Round 195: More hapax vocabulary
    'kulhzang': ('kulh-zang', 'wall-edge'),                       # 2x 2Kgs 6:26 - "upon the wall"
    'khawlei': ('khawlei', 'Arcturus'),                           # 2x Job 9:9, 38:32 - constellation
    'uikai': ('uikai', 'Orion'),                                  # 2x Job 9:9, 38:31 - constellation
    'vuttui': ('vut-tui', 'snow-water'),                          # 2x Job 9:30, 24:19 - "snow water"
    'thangkhau': ('thang-khau', 'trap-rope'),                     # 2x Job 18:9-10 - "gin/snare"
    'dildel': ('dil~del', 'glitter~REDUP'),                         # 2x Job 20:25 - "glittering"
    'suangheeng': ('suang-heeng', 'stone-crag'),                  # 2x Job 39:28 - "rock crag"
    'hol': ('hol', 'coals'),                                      # 2x Gen 6:21, John 18:18 - "coals"
    'husang': ('hu-sang', 'live-up'),                             # 2x 1Thes 3:8 - "we live"
    'olno': ('ol-no', 'vine-tender'),                             # 2x Gen 49:11 - "choice vine"
    'meihol': ('mei-hol', 'fire-coals'),                          # 2x John 18:18, 21:9 - "fire of coals"
    
    # Round 196: More hapax vocabulary
    'haulua': ('hau-lua', 'rich-too'),                            # 2x Prov 30:8 - "riches" (too rich)
    'tuipeek': ('tui-peek', 'water-swim'),                        # 2x Acts 27:43 - "swim"
    'tankhiapa': ('tan-khia-pa', 'redeem-out-M'),                 # 2x Isa 49:26, 60:16 - "Redeemer"
    'citciat': ('cit~ciat', 'go~REDUP'),                            # 2x John 5:9 - exactness marker
    # suangkeen: Job 14:18 "rock is removed", Amos 6:12 "upon the rock"
    # keen appears to mean 'crag/cliff' (cf. keenhawm=cave, keen sang=rock top)
    'suangkeen': ('suang-keen', 'stone-crag'),                    # 2x - rocky crag/cliff
    'thuklua': ('thuk-lua', 'deep-too'),                          # 2x Ezek 47:5 - "too deep"
    'lingvom': ('ling-vom', 'thorn-bush'),                        # 2x Luke 6:44 - "bramble bush"
    
    # Round 198: More hapax vocabulary
    'geh': ('geh', 'bull'),                                       # 2x Isa 34:7 - "bullocks"
    'meitui': ('mei-tui', 'fire-water'),                          # 2x Matt 25:8 - "oil" (lamp oil)
    'zuphung': ('zu-phung', 'wine-master'),                       # 2x John 2:8 - "governor of feast"
    'menzi': ('men-zi', 'office-hold'),                           # 2x Acts 23:33 - "governor"
    'atkeh': ('at-keh', 'cut-REFL'),                              # 1x Deut 14:1 - "cut yourselves"
    'pheklek': ('pheklek', 'spy.out'),                            # 1x 1Chr 19:3 - "spy out"
    'hehsakkha': ('heh-sak-kha', 'anger-CAUS-PAST'),              # 1x Ezra 5:12 - "provoked to wrath"
    'kidawhkhiat': ('ki-dawh-khiat', 'REFL-set-out'),             # 2x Ezra 6:11 - "pulled down"
    'zehsiang': ('zeh-siang', 'pure-clean'),                      # 1x Ezra 6:20 - "purified"
    
    # Round 198b: More hapax from Nehemiah/Esther
    'tukawmin': ('tu-kawm-in', 'sit-beside-ERG'),                 # 1x Neh 2:6 - "sitting by"
    'zumcingte': ('zum-cing-te', 'prison-guard-PL'),              # 1x Neh 3:25 - "court of prison"  
    'lehtuksak': ('leh-tuk-sak', 'turn-back-CAUS'),               # 1x Neh 4:4 - "turn back"
    'gamzai': ('gam-zai', 'land-fat'),                            # 1x Neh 9:35 - "fat land"
    'patkhiat': ('pat-khiat', 'begin-out'),                       # 1x Neh 11:17 - "principal to begin"
    'namlephung': ('nam-le-phung', 'people-and-family'),          # 1x Esth 2:10 - "people nor kindred"
    'ngenthuah': ('ngen-thuah', 'request-extra'),                 # 1x Esth 2:15 - "required"
    'vingveng': ('ving~veng', 'hurry~REDUP'),                       # 1x Esth 6:12 - "hasted"
    'lelhtak': ('lelh-tak', 'fall-begin'),                        # 1x Esth 6:13 - "begun to fall"
    
    # Round 198c: Job/Revelation hapax
    'ngeikei': ('ngei-kei', 'have-NEG'),                          # 1x Job 3:9 - "have none"
    'zonzaw': ('zon-zaw', 'dig-more'),                            # 1x Job 3:21 - "dig for it more"
    'khukzaw': ('khuk-zaw', 'knee-weak'),                         # 1x Job 4:4 - "feeble knees"
    'ginghiau': ('ging-hiau', 'whisper-small'),                   # 1x Job 4:12 - "secretly/a little"
    'liahtumsak': ('liah-tum-sak', 'take-all-CAUS'),              # 1x Job 5:5 - "taketh up"
    'pokhiatawm': ('pok-khiat-awm', 'spring-out-PART'),           # 1x Job 5:6 - "spring out"
    'khalhnelh': ('khalh-nelh', 'freeze-black'),                  # 1x Job 6:16 - "blackish by ice"
    'suangtawphah': ('suang-tawphah', 'stone-foundation'),        # 3x Job 8:17, Rev 21 - "foundations"
    'tuncipsak': ('tun-cip-sak', 'cover-tight-CAUS'),             # 1x Job 9:24 - "covereth"
    
    # Round 199: Job/Luke hapax vocabulary
    'ol': ('ol', 'slow'),                                         # 3x Exod 4:10, 12:39 - "slow of speech" 
    'melh': ('melh', 'forge'),                                    # 1x Job 13:4 - "forgers of lies"
    'dengvui': ('deng-vui', 'pound-dust'),                        # 2x Job 10:9, Luke 20:18 - "dust/powder"
    'vutkhu': ('vut-khu', 'faded-ash'),                           # 1x Job 13:12 - "ashes"
    'zaizaw': ('zai-zaw', 'extent-more'),                         # 2x Job 11:9, 2Cor 10:15 - "broader"
    'lehzuih': ('leh-zuih', 'return-CONT'),                       # 2x Job 16:22, 1Sam 15:25 - "return"
    'lehsuksiat': ('leh-suk-siat', 'return-pull-destroy'),        # 1x Job 10:8 - "destroy"
    
    # Round 199b: Genesis/Job hapax vocabulary
    "khimzin'": ("khim-zin'", "dark-GEN"),                        # 1x Job 3:4 - "that day be darkness"
    'da': ('da', 'dry'),                                          # 1x Gen 1:9 - "dry land"
    'khauzak': ('khau-zak', 'rope-trap'),                         # 1x Job 18:10 - "snare/trap"
    'melmawl': ('mel-mawl', 'face-young'),                        # 1x Job 19:18 - "young children"
    'dihdiahin': ('dih-diah-in', 'bare-only-ERG'),                # 1x Job 19:20 - "barely/just"
    'mumaang': ('mu-maang', 'dream-vision'),                      # 1x Job 20:8 - "vision of night"
    'zongtawm': ('zong-tawm', 'seek-again'),                      # 1x Job 24:5 - "seek/search"
    'thazawngkhal': ('tha-zawng-khal', 'strength-arm-lacking'),   # 1x Job 26:2 - "without strength"
    'lingleng': ('ling-leng', 'hang-IDEO'),                       # 1x Job 26:7 - "hangeth upon nothing"
    'meiilom': ('meii-lom', 'cloud-thick'),                       # 1x Job 26:8 - "thick clouds"
    'dinden': ('din-den', 'stand-border'),                        # 1x Job 26:10 - "boundary/bounds"
    'leizawh': ('lei-zawh', 'buy-exchange'),                      # 1x Job 28:17 - "exchange"
    'dimdem': ('dim-dem', 'quiet-IDEO'),                          # 1x Job 29:21 - "silently/waited"
    "taciingte'": ("taciing-te'", "barren-PL.GEN"),               # 1x Job 24:21 - "barren women" (taciing=lexicalized)
    
    # Round 200: Job/Psalms/Numbers hapax vocabulary
    'lopi': ('lo-pi', 'NEG-EMPH'),                                # 1x Gen 21:23 - "falsely" (not falsely)
    'sucipsuk': ('su-cip-suk', 'push-tight-sink'),                # 1x Job 30:14 - "rolled upon me"
    'heekcip': ('heek-cip', 'fold-tight'),                         # 1x Job 30:18 - "bindeth me about"
    'sehkholhin': ('seh-kholh-in', 'appoint-INTENS-ERG'),          # 1x Job 30:23 - "appointed"
    'sinkhamin': ('sin-kham-in', 'dark-mourn-ERG'),               # 1x Job 30:28 - "mourning"
    'dulhkhia': ('dulh-khia', 'peel-out'),                        # 1x Job 30:30 - "skin peeling off"
    'henkop': ('hen-kop', 'bind-together'),                       # 1x Job 38:31 - "bind influences"
    'bawhsuk': ('bawh-suk', 'bow-sink'),                          # 1x Job 39:3 - "bow down to birth"
    'phitsak': ('phit-sak', 'frighten-CAUS'),                     # 1x Job 39:20 - "make afraid"
    'deek': ('deek', 'bargain'),                                  # 1x Job 41:6 - "make a banquet"
    'phensak': ('phen-sak', 'open-CAUS'),                         # 1x Job 41:14 - "open doors"
    'tuiso': ('tui-so', 'water-bubble'),                          # 1x Job 41:31 - "boil like pot"
    'pheuphau': ('pheu-phau', 'foam-white'),                      # 1x Job 41:32 - "hoary/white"
    'hehluat': ('heh-luat', 'anger-excessive'),                   # 1x Num 32:14 - "fierce anger"
    'gawlgui': ('gawl-gui', 'throat-neck'),                       # 1x Psa 5:9 - "throat"
    'thasaan': ('tha-saan', 'strength-lift'),                     # 1x Psa 7:6 - "lift up thyself"
    'meiivom': ('meii-vom', 'cloud-dark'),                        # 1x Psa 18:9 - "darkness"
    'kinawmsawmin': ('ki-nawm-sawm-in', 'REFL-fall-together-CVB'), # 1x Psa 20:8 - "brought down"
    'guaksuak': ('guak-suak', 'confound-become'),                 # 1x Psa 22:5 - "were not confounded" (suak=become, not CAUS)
    'sabawh': ('sa-bawh', 'roar-open'),                           # 1x Psa 22:13 - "ravening lion"
    
    # Round 200b: Psalms hapax vocabulary
    'kihbawl': ('kih-bawl', 'hide-make'),                         # 1x Psa 22:24 - "hid his face" (kih=hide stem)
    'kigimtawm': ('ki-gim-tawm', 'REFL-afflict-again'),           # 1x Psa 35:13 - "humbled my soul" (with -sak separate)
    'enkhong': ('en-khong', 'look-how.long'),                     # 1x Psa 35:17 - "how long wilt thou look on"
    'lokung': ('lo-kung', 'field-herb'),                          # 1x Psa 37:2 - "green herb"
    'suniam': ('su-niam', 'push-down'),                           # 1x Psa 37:14 - "cast down"
    'kipden': ('kip-den', 'endure-forever'),                      # 1x Psa 37:18 - "for ever"
    'kibokcipsak': ('ki-bok-cip-sak', 'REFL-bow-tight-CAUS'),     # 1x Psa 38:6 - "bowed down greatly"
    'ngiungeu': ('ngiu-ngeu', 'wait-IDEO'),                       # 1x Psa 40:1 - "waited patiently"
    'kihuauhuau': ('ki-huau-huau', 'REFL-whisper~REDUP'),         # 1x Psa 41:7 - "whisper together"
    'sawnpai': ('sawn-pai', 'push-go'),                           # 1x Psa 44:5 - "push down"
    
    # Round 201: Psalms/Leviticus/Numbers hapax vocabulary
    'lop': ('lop', 'false'),                                      # 1x Gen 21:23 - appears in "lopi-in" = falsely
    'angtang': ('ang-tang', 'forehead-part'),                     # 1x 1Sam 17:49 - "forehead"
    'maivil': ('mai-vil', 'face-entreat'),                        # 1x Psa 45:12 - "entreat thy favour"
    'taktakpa': ('tak-tak-pa', 'true-REDUP-NMZ'),                 # 1x Psa 48:3 - "refuge"
    'phuhkip': ('phuh-kip', 'establish-forever'),                 # 1x Psa 48:8 - "establish forever"
    'zelh': ('zelh', 'spread'),                                   # 1x Lev 13:53 - "be not spread"
    'ngozaw': ('ngo-zaw', 'white-more'),                          # 1x Psa 51:7 - "whiter than snow"
    'vakthap': ('vak-thap', 'wander-far'),                        # 1x Psa 55:7 - "wander far off"
    'nelzaw': ('nel-zaw', 'smooth-more'),                         # 1x Psa 55:21 - "smoother than butter"
    'nipzaw': ('nip-zaw', 'soft-more'),                           # 1x Psa 55:21 - "softer than oil"
    'lawnkhiasuk': ('lawn-khia-suk', 'cast-out-sink'),            # 1x Psa 56:7 - "cast down"
    'tawnun': ('tawn-un', 'prosper-PROG'),                        # 1x Deut 23:6 - "prosperity"
    'leek': ('leek', 'weigh'),                                    # 1x Psa 62:9 - "laid in balance"
    'kihubing': ('ki-hu-bing', 'REFL-mouth-stop'),                # 1x Psa 63:11 - "shall be stopped"
    'pumtuam': ('pum-tuam', 'body-cover'),                        # 1x Psa 69:7 - "covered my face"
    'lehsuak': ('leh-suak', 'return-out'),                        # 1x Psa 69:10 - "reproach"
    'kuavang': ('kua-vang', 'pit-mouth'),                         # 1x Psa 69:15 - "pit mouth"
    'kisuipuk': ('ki-sui-puk', 'REFL-slip-sink'),                 # 1x Psa 73:2 - "feet slipped"
    'heipi': ('hei-pi', 'thigh-big'),                             # 1x Num 5:21 - "thy thigh"
    'daigawl': ('dai-gawl', 'fence-break'),                       # 1x Psa 80:12 - "broken hedges"
    'suvang': ('su-vang', 'break-through'),                       # 1x Psa 80:12 - "broken down"
    'ninnen': ('nin-nen', 'dust-blow'),                           # 1x Psa 83:13 - "like a wheel/stubble"
    'helhawt': ('hel-hawt', 'violent-rush'),                      # 1x Psa 86:14 - "violent men"
    'thohonpi': ('tho-hon-pi', 'fly-swarm-big'),                  # 1x Psa 105:31 - "divers flies"
    'tuiphualah': ('tui-phual-ah', 'water-place-LOC'),            # 1x Psa 106:32 - "at the waters"
    'ninphual': ('nin-phual', 'dust-place'),                      # 1x Psa 113:7 - "dunghill"
    'hileng': ('hi-leng', 'be-if.not'),                           # 1x Psa 119:92 - "unless"
    'kibottat': ('ki-bot-tat', 'REFL-break-apart'),               # 1x Psa 124:7 - "snare broken"
    'kuih': ('kuih', 'plow'),                                     # 1x Psa 129:3 - "plowed"
    "luiliante'": ("lui-lian-te'", "river-big-PL.GEN"),           # 1x Psa 77:19 - "great waters"
    
    # Round 202: Proverbs/Job hapax vocabulary
    'liuliau': ('liu-liau', 'straight-IDEO'),                     # 1x Prov 4:25 - "look straight"
    'guhguak': ('guh-guak', 'moan-groan'),                        # 1x Prov 5:11 - "consumed/mourn"
    'keikha': ('kei-kha', 'NEG-PERF'),                            # 1x Prov 5:13 - "have not done"
    'khoih': ('khoih', 'point'),                                  # 1x Prov 6:13 - "teacheth with fingers"
    'kisusiatawm': ('ki-su-siat-awm', 'REFL-push-destroy-PART'),  # 1x Prov 6:32 - "destroyeth own soul"
    'hehzawk': ('heh-zawk', 'angry-most'),                        # 1x Prov 6:34 - "jealousy/rage"
    'petmah': ('pet-mah', 'find-exactly'),                        # 1x Prov 7:15 - "have found thee"
    'siipsak': ('siip-sak', 'sting-CAUS'),                        # 1x Prov 10:26 - "irritate eyes"
    'vokpi': ('vok-pi', 'pig-big'),                               # 1x Prov 11:22 - "swine"
    'leinop': ('lei-nop', 'buy-good'),                            # 1x Prov 11:26 - "good harvest"
    'leikhal': ('lei-khal', 'earth-dry'),                         # 1x Prov 12:12 - "net/snare"
    'pholaklak': ('pho-lak-lak', 'proclaim~REDUP'),               # 1x Prov 12:23 - "proclaimeth"
    'maigumsak': ('mai-gum-sak', 'face-dark-CAUS'),               # 1x Prov 15:13 - "spirit broken"
    'bangbek': ('bang-bek', 'what-only'),                         # 1x Prov 16:33 - "entirely/whole"
    'mohkeu': ('moh-keu', 'bread-dry'),                           # 1x Prov 17:1 - "dry morsel"
    'bunzaw': ('bun-zaw', 'deep-more'),                           # 1x Prov 17:10 - "entereth deeply"
    'lipi': ('li-pi', 'each-EMPH'),                               # 1x Gen 44:11 - "every man"
    'khawlpak': ('khawl-pak', 'cease-quickly'),                   # 1x Prov 17:14 - "leave off" (pak=quickly, not CAUS)
    'maigum': ('mai-gum', 'face-dark'),                           # 1x Job 29:24 - "countenance dark"
    'kihupsuk': ('ki-hup-suk', 'REFL-pierce-sink'),               # 1x Prov 18:8 - "go down into"
    'sawksukin': ('sawk-suk-in', 'dip-hold-ERG'),                 # 1x Prov 19:24 - "hideth hand"
    'haikhak': ('hai-khak', 'gravel-hard'),                       # 1x Prov 20:17 - "filled with gravel"
    'lopthop': ('lop-thop', 'hurry-quickly'),                     # 1x Prov 21:5 - "hasty"
    'lehthuak': ('leh-thuak', 'suffer-instead'),                  # 1x Prov 21:18 - "ransom"
    'kizawnlawh': ('ki-zawn-lawh', 'REFL-poor-RESULT'),           # 1x Prov 22:16 - "come to want"
    'hehbaih': ('heh-baih', 'angry-easily'),                      # 1x Prov 22:24 - "furious man"
    'duhgawhkha': ('duh-gawh-kha', 'desire-dainty-PERF'),         # 1x Prov 23:6 - "desire dainties"
    'kithuahkha': ('ki-thuah-kha', 'REFL-associate-PERF'),        # 1x Prov 23:20 - "be among"
    "dian'": ("dian'", "Midian.GEN"),                             # 1x Gen 25:4 - proper noun
    "kha'n": ("kha'n", "might-COND"),                             # 1x Prov 22:13 - "might"
    
    # Round 203: Proverbs/Judges/Ecclesiastes hapax vocabulary
    'tukha': ('tu-kha', 'sit-PERF'),                              # 1x Judg 19:6 - "sat down together"
    'khei': ('khei', 'pierce'),                                   # 1x Prov 26:9 - "thorn goeth up"
    'sawksuk': ('sawk-suk', 'dip-hold'),                          # 1x Prov 19:24 - "hideth hand"
    'lehkiat': ('leh-kiat', 'return-fall'),                       # 1x Prov 26:27 - "fall therein"
    'dengkha': ('deng-kha', 'strike-PERF'),                       # 1x Judg 9:53 - "brake skull"
    'lehden': ('leh-den', 'return-upon'),                         # 1x Prov 26:27 - "return upon him"
    'daangkoih': ('daang-koih', 'distant-forsake'),               # 1x Prov 27:10 - "forsake not"
    'halungvei': ('ha-lung-vei', 'roar-heart-fierce'),            # 1x Prov 28:15 - "ranging bear"
    'neucik': ('neu-cik', 'small-bit'),                           # 1x Prov 28:21 - "piece of bread"
    'lomcip': ('lom-cip', 'gather-tight'),                        # 1x Prov 30:4 - "gathered in fists"
    'tuncip': ('tun-cip', 'cover-tight'),                         # 1x Job 9:24 - "covereth faces"
    'khazel': ('kha-zel', 'fear-might'),                          # 1x Prov 30:9 - "lest I"
    'taciing': ('taciing', 'barren'),                             # 1x Prov 30:16 - "barren womb" (lexicalized)
    'khelkhiat': ('khel-khiat', 'pick-out'),                      # 1x Prov 30:17 - "pick it out"
    'kheekin': ('kheek-in', 'spin-ERG'),                          # 1x Prov 31:19 - "layeth to spindle"
    'gantawm': ('gan-tawm', 'hold-again'),                        # 1x Prov 31:19 - "hold distaff"
    'khuitawm': ('khui-tawm', 'weave-again'),                     # 1x Prov 31:22 - "maketh coverings"
    'lasiam': ('la-siam', 'song-skilled'),                        # 1x Eccl 2:8 - "singers"
    'bawhsat': ('bawh-sat', 'break-snap'),                        # 1x Eccl 4:12 - "quickly broken"
    'phawkkhiat': ('phawk-khiat', 'perceive-out'),                # 1x Eccl 5:18 - "have seen"
    
    # Round 203b: Ecclesiastes/Song/Exodus hapax vocabulary
    'mamsakkik': ('mam-sak-kik', 'straight-CAUS-again'),          # 1x Eccl 7:13 - "make straight"
    'bangtumlo': ('bang-tum-lo', 'what-all-NEG'),                 # 1x Eccl 10:13 - "foolishness"
    'keh': ('keh', 'cut'),                                        # 1x Deut 14:1 - "cut yourselves"
    'tamluat': ('tam-luat', 'full-excessive'),                    # 1x Eccl 11:3 - "full of rain"
    'zusuk': ('zu-suk', 'pour-sink'),                             # 1x Eccl 11:3 - "empty themselves"
    'phawnzawh': ('phawn-zawh', 'awaken-exchange'),               # 1x Eccl 12:4 - "rise up at voice"
    'gawtbawl': ('gawt-bawl', 'angry-make'),                      # 1x Song 1:6 - "were angry"
    'duangvul': ('duang-vul', 'love-sick'),                       # 1x Song 2:5 - "sick of love"
    'kisawpsiang': ('ki-sawp-siang', 'REFL-wash-clean'),          # 1x Song 4:2 - "from washing"
    'kuai': ('kuai', 'break'),                                    # 1x Exod 12:46 - "break a bone"
    
    # Round 204: Loanwords and proper nouns (high-frequency unknowns)
    'manna': ('manna', 'manna'),                      # 36x - Hebrew loanword
    'gath': ('Gath', 'Gath'),                         # 32x - Philistine city
    'harp': ('harp', 'harp'),                         # 32x - English loanword
    'hell': ('hell', 'hell'),                         # 23x - English loanword (Sheol)
    'myrrh': ('myrrh', 'myrrh'),                      # 19x - fragrant resin
    'joppa': ('Joppa', 'Joppa'),                      # 17x - coastal city
    'hermon': ('Hermon', 'Hermon'),                   # 14x - mountain
    'debir': ('Debir', 'Debir'),                      # 14x - Canaanite city
    'hadad': ('Hadad', 'Hadad'),                      # 13x - personal name
    'dagon': ('Dagon', 'Dagon'),                      # 13x - Philistine god
    'bethany': ('Bethany', 'Bethany'),                # 13x - village near Jerusalem
    'peel': ('peel', 'peel'),                         # 12x - skin/rind
    'beeroth': ('Beeroth', 'Beeroth'),                # 12x - city name
    'gog': ('Gog', 'Gog'),                            # 12x - Ezekiel prophecy figure
    'er': ('Er', 'Er'),                               # 11x - personal name (Judah's son)
    'dathan': ('Dathan', 'Dathan'),                   # 10x - rebel against Moses
    'elihu': ('Elihu', 'Elihu'),                      # 10x - Job's friend
    'deborah': ('Deborah', 'Deborah'),                # 9x - judge/prophetess
    'bozrah': ('Bozrah', 'Bozrah'),                   # 8x - Edomite city
    'jasper': ('jasper', 'jasper'),                   # 7x - precious stone
    'ram': ('Ram', 'Ram'),                            # 7x - personal name
    'bethsaida': ('Bethsaida', 'Bethsaida'),          # 7x - town in Galilee
    'delilah': ('Delilah', 'Delilah'),                # 6x - Samson's betrayer
    'gerah': ('gerah', 'gerah'),                      # 5x - unit of weight
    
    # Round 205: Partial gloss fixes
    'tawmkhat': ('tawm-khat', 'few-one'),             # 55x - "a little"
    'gaias': ('Gaias', 'Gaius'),                      # 8x - personal name
    'maangin': ('maang-in', 'dim-ERG'),               # 6x - "eyes dim"
    'tahumte': ('tahum-te', 'tares-PL'),              # 4x - "tares"
    "puansawppa'": ("puan-sawppa'", "cloth-fuller.POSS"),  # 3x - "fuller's" (cloth washer)
    'sawppa': ('sawppa', 'fuller'),                   # base form
    'karnelian': ('karnelian', 'carnelian'),          # 3x - precious stone
    'carnelian': ('carnelian', 'carnelian'),          # alternate spelling
    "hebru-te'": ("Hebru-te'", "Hebrew-PL.POSS"),     # 2x - "Hebrews'"
    'hebru': ('Hebru', 'Hebrew'),                     # base form
    'leenggahsukna': ('leenggah-suk-na', 'grape-press-NMLZ'),  # 2x - winepress
    'miksite': ('miksi-te', 'ant-PL'),                # 2x - ants
    'miksi': ('miksi', 'ant'),                        # base form
    'diktanna': ('dik-tan-na', 'right-stand-NMLZ'),   # 2x - righteousness
    'thuciamtehna': ('thu-ciam-teh-na', 'word-promise-establish-NMLZ'),  # 2x - covenant record
    'thakhauhin': ('tha-khauh-in', 'strength-strong-ERG'),  # 2x - strengthened
    'galbanum': ('galbanum', 'galbanum'),             # 1x - aromatic resin
    
    # Round 206: More partial fixes
    'nahthel': ('nahthel', 'leaf'),                   # 2x - leaf (Lev 26:36)
    'masalate': ('masala-te', 'fitches-PL'),          # 2x - fitches (grain)
    'tuateng': ('tua-teng', 'that-only'),             # 2x - "not only that"
    'thopi': ('thopi', 'bird'),                       # 2x - bird (Eccl 10:20)
    'limlangah': ('limlang-ah', 'mirror-LOC'),        # 2x - in a glass/mirror
    'kipangsak': ('ki-pang-sak', 'REFL-side-CAUS'),   # 1x - set in array
    'o': ('o', 'INTERJ'),                             # 2x - interjection "O"
    'merodak-baladan': ('Merodak-Baladan', 'Merodach-Baladan'),  # 2x - Babylonian king
    'anaiah': ('Anaiah', 'Anaiah'),                   # 2x - personal name
    'khawlei-uikai': ('khawlei-uikai', 'world-guide'),  # 2x - world guides
    "'zuhai": ('zuhai', 'INTERJ'),                    # 2x - exclamation
    'rehoboth-ir': ('Rehoboth-Ir', 'Rehoboth-Ir'),    # 1x - city name
    'el-elohe-israel': ('El-Elohe-Israel', 'El-Elohe-Israel'),  # 1x - altar name
    'zafenath-paneah': ('Zaphenath-Paneah', 'Zaphenath-Paneah'),  # 1x - Joseph's Egyptian name
    'gibeath-haaraloth': ('Gibeath-Haaraloth', 'Gibeath-Haaraloth'),  # 1x - place name
    'gibeath-elohim': ('Gibeath-Elohim', 'Gibeath-Elohim'),  # 1x - place name
    
    # Round 207: ki- nominalizations and hapax fixes
    'kizawhna': ('ki-zawh-na', 'REFL-cross-NMLZ'),    # 1x - crossing (Ezra 4:10)
    'kikholhna': ('ki-kholh-na', 'REFL-accompany-NMLZ'),  # 1x - sending portions (Esth 9:19)
    'kipuahna': ('ki-puah-na', 'REFL-purify-NMLZ'),   # 1x - purifying (Esth 2:12)
    'kisenna': ('ki-sen-na', 'REFL-red-NMLZ'),        # 1x - reddening
    'kisuhna': ('ki-suh-na', 'REFL-push-NMLZ'),       # 1x - pushing
    'kimematna': ('ki-memat-na', 'REFL-grip-NMLZ'),   # 1x - gripping
    'kikhakna': ('ki-khak-na', 'REFL-shut-NMLZ'),     # 1x - shutting
    'kinaina': ('ki-nai-na', 'REFL-near-NMLZ'),       # 1x - drawing near
    'kipelhsakna': ('ki-pelh-sak-na', 'REFL-cross-CAUS-NMLZ'),  # 1x - causing to cross
    'kipaiina': ('ki-paii-na', 'REFL-sorrow-NMLZ'),   # 1x - sorrowing
    'kiginkholhna': ('ki-gin-kholh-na', 'REFL-fear-INTENS-NMLZ'),  # 1x - fearfully made
    'niangnuangte': ('niangnuang-te', 'feeble-PL'),   # 1x - feeble ones
    'niangnuang': ('niangnuang', 'feeble'),           # base form
    'phazahte': ('phazah-te', 'number-PL'),           # 1x - numbers/census
    'phazah': ('phazah', 'number'),                   # base form
    'makte': ('mak-te', 'strange-PL'),                # 1x - strangers
    'lehtukna': ('leh-tuk-na', 'return-meet-NMLZ'),   # 1x - returning
    'phuisamna': ('phui-sam-na', 'shave-hair-NMLZ'),  # 1x - shaving
    'minphatnate': ('min-phat-na-te', 'name-praise-NMLZ-PL'),  # 1x - praises
    'vuahep': ('vu-ahep', 'bee-swarm'),               # 1x - bee swarm
    'sialun': ('sial-un', 'mithun-3PL'),              # 1x - their mithuns
    'deihdeihin': ('deih-deih-in', 'want-REDUP-ERG'), # 1x - desiring greatly
    'tungtangin': ('tung-tang-in', 'above-long-ERG'), # 1x - from above
    'phuhsak': ('phuh-sak', 'plant-CAUS'),            # 1x - cause to plant
    'phatuamsak': ('phat-tuam-sak', 'praise-all-CAUS'),  # 1x - cause all praise
    'ciangtang': ('ciang-tang', 'clear-long'),        # 1x - clearly long
    'laiphai': ('lai-phai', 'book-flat'),             # 1x - flat book/tablet
    
    # Round 208: More hapax fixes
    'savokphual': ('savokphual', 'weasel'),           # 1x Lev 11:29 - animal
    'singmuat': ('sing-muat', 'wood-rot'),            # 1x Job 13:28 - rotten thing
    'hotna': ('hot-na', 'save-NMLZ'),                 # 1x Job 26:2 - saving
    'suangseeksate': ('suang-seek-sa-te', 'stone-hew-PRF-PL'),  # 1x - masons/stonecutters
    'suangseeksa': ('suang-seeksa', 'stone-carve.PRF'),  # base - mason
    'khialhkhaknate': ('khialh-khak-na-te', 'err-shut-NMLZ-PL'),  # 1x - iniquities
    'suangkeente': ('suang-keen-te', 'stone-crag-PL'),   # 1x Job 14:18 - rocks/crags
    # suangkeen: see line ~15584 (consolidated)
    'teharsha': ('Teharsha', 'Tel-Harsha'),           # 1x - place name
    'tiz': ('tiz', 'scatter'),                        # 1x - scatter
    'ami': ('ami', 'who'),                            # 1x - interrogative
    'kar': ('kar', 'generation'),                     # 1x - generation/age
    '"ciknawng': ('ciknawng', 'alone'),               # 1x - alone/by oneself
    'ciknawng': ('ciknawng', 'alone'),                # base form
    'lapna': ('lap-na', 'wrap-NMLZ'),                 # 1x - wrapping
    'lap': ('lap', 'wrap'),                           # base form
    'nipna': ('nip-na', 'pinch-NMLZ'),                # 1x - pinching
    'kaptuk': ('kap-tuk', 'cry-meet'),                # 1x - crying together
    'mavanna': ('mavan-na', 'wonder-NMLZ'),           # 1x - wondering
    'ngongbawlna': ('ngong-bawl-na', 'self-make-NMLZ'),  # 1x - self-making
    'suahkhiatna': ('suah-khiat-na', 'emerge-exit-NMLZ'),  # 1x - emergence
    'kisiansakna': ('ki-sian-sak-na', 'REFL-holy-CAUS-NMLZ'),  # 1x - sanctification
    'thudotnate': ('thu-dot-na-te', 'word-confirm-NMLZ-PL'),  # 1x - confirmations
    'suhsakte': ('suh-sak-te', 'push-CAUS-PL'),       # 1x - pushers
    'lahtelnate': ('lahtel-na-te', 'accompany-NMLZ-PL'),  # 1x - accompaniments
    
    # Round 209: More hapax compounds
    'lamkhial': ('lam-khial', 'way-err'),             # 1x Jer 50:6 - go astray
    'khekhapte': ('khe-khap-te', 'foot-step-PL'),     # 2x - footsteps
    'khekhap': ('khe-khap', 'foot-step'),             # base - footstep
    'dinkipna': ('din-kip-na', 'stand-together-NMLZ'),  # 1x - standing together
    'kithukkikna': ('ki-thuk-kik-na', 'REFL-deep-ITER-NMLZ'),  # 1x - deepening
    'kigakna': ('ki-gak-na', 'REFL-stop-NMLZ'),       # 1x - stopping
    'dianna': ('dian-na', 'still-NMLZ'),              # 1x - stillness
    'kizuakna': ('ki-zuak-na', 'REFL-sell-NMLZ'),     # 1x - selling self
    'hailuatna': ('hai-luat-na', 'be.anxious-exceed-NMLZ'),  # 1x - excessive anxiety
    'hauhtohna': ('hauh-toh-na', 'call-reach-NMLZ'),  # 1x - calling/reaching
    'lawpluatna': ('lawp-luat-na', 'rejoice-exceed-NMLZ'),  # 1x - exceeding joy
    'khahkhongna': ('khah-khong-na', 'choke-tight-NMLZ'),  # 1x - choking
    'khiukheuna': ('khiu-kheu-na', 'crooked-REDUP-NMLZ'),  # 1x - crookedness
    'laptohna': ('lap-toh-na', 'wrap-reach-NMLZ'),    # 1x - wrapping
    'guhnatna': ('guh-nat-na', 'labor-pain-NMLZ'),    # 1x - labor pains
    'hehsaknate': ('heh-sak-na-te', 'anger-CAUS-NMLZ-PL'),  # 1x - provocations
    'kihilhte': ('ki-hilh-te', 'REFL-teach-PL'),      # 1x - taught ones
    'zuaunate': ('zuau-na-te', 'lie-NMLZ-PL'),        # lies/falsehoods
    'zadahin': ('zadah-in', 'utterly-ERG'),           # 1x - "utterly" intensifier
    'sawmnate': ('sawm-na-te', 'tempt-NMLZ-PL'),      # 1x - temptations
    'lahsate': ('lah-sa-te', 'take-PRF-PL'),          # 1x - taken ones
    'theithekte': ('thei-thek-te', 'know.I-cut-PL'),  # 1x - acquainted ones
    'tatkhiatsate': ('tat-khiat-sa-te', 'strike-out-PRF-PL'),  # 1x - struck out
    'geelgeelin': ('geel-geel-in', 'plan-REDUP-ERG'), # 1x - planning carefully
    'khiankhian': ('khia-khia-in', 'exit-REDUP-ERG'), # 1x - going out repeatedly
    
    # Round 210: More hapax (Song of Songs, Isaiah, etc.)
    'lungtup': ('lung-tup', 'heart-knock'),           # 1x Song 5:2 - beloved knocks
    'singseng': ('sing-seng', 'tree-shear'),          # 1x Song 4:2 - shorn
    'singsengte': ('sing-seng-te', 'tree-shear-PL'),  # 1x - shorn (teeth)
    'duang': ('duang', 'love'),                       # 1x - base for duangvul
    'daingo': ('daingo', 'dew'),                      # 1x Song 5:2 - dew
    'suanghawmpite': ('suang-hawm-pi-te', 'stone-hollow-big-PL'), # 1x Isa 2:19 - caves
    'puktheihna': ('puk-theih-na', 'fall-ABIL-NMLZ'), # 1x - ability to fall
    'ciakciak': ('ciak~ciak', 'chirp~REDUP'),         # 1x - chirping
    'tungdap': ('tung-dap', 'upon-close'),            # 1x - close upon
    'kil': ('kil', 'corner'),                         # 1x - corner
    'eka': ('eka', 'alone'),                          # 1x - alone
    'tupeek': ('tupeek', 'cubit'),                    # 1x - measure
    'lingliang': ('ling-liang', 'shine-bright'),      # 1x - shining bright
    'tumbang': ('tumbang', 'alike'),                  # 1x - like/alike
    'khauzen': ('khauzen', 'yarn'),                   # 1x - thread/yarn
    'bumek': ('bumek', 'fine.flour'),                 # 1x - fine flour
    'bangkeek': ('bang-keek', 'like-tear'),           # 1x - torn like
    'lehmat': ('lehmat', 'exchange'),                 # 1x - exchange
    'dedu': ('dedu', 'suddenly'),                     # 1x - suddenly
    'pialpual': ('pial-pual', 'wander~REDUP'),        # 1x - wandering about
    'tucip': ('tucip', 'squeeze'),                    # 1x - squeeze/press
    'heengte': ('heeng-te', 'bare-PL'),               # 1x - bare ones
    'netumte': ('netum-te', 'young.woman-PL'),        # 1x - young women
    'gawpnate': ('gawp-na-te', 'weep-NMLZ-PL'),       # 1x - weepings
    'patlom': ('pat-lom', 'touch-bundle'),            # 1x - handle/bunch
    'khemul': ('khe-mul', 'foot-tip'),                # 1x - toe
    'thiuhtheuh': ('thiuh-theuh', 'sprinkle~REDUP'),  # 1x - sprinkling
    'lomtangin': ('lom-tang-in', 'bundle-long-ERG'),  # 1x - bundled long
    'kisangsakte': ('ki-sang-sak-te', 'REFL-high-CAUS-PL'),  # 1x - exalted ones
    'kihawlkhiate': ('ki-hawl-khia-te', 'REFL-rest-exit-PL'),  # 1x - those who rest
    'kidengawpna': ('ki-deng-awp-na', 'REFL-stand-meet-NMLZ'),  # 1x - standing together
    'kisepsakna': ('ki-sep-sak-na', 'REFL-destroy-CAUS-NMLZ'),  # 1x - destruction
    'luhinna': ('luh-in-na', 'plunder-take-NMLZ'),    # 1x - plundering
    
    # Round 211: Isaiah hapax vocabulary
    'lamzin': ('lam-zin', 'way-journey'),             # 1x Isa 30:11 - path
    'suanghum': ('suang-hum', 'stone-rough'),         # 1x Isa 40:4 - rough places
    'thangko': ('thang-ko', 'spread-call'),           # 1x Isa 44:7 - declare
    'lamkaih': ('lam-kaih', 'way-lead'),              # 1x Isa 49:10 - guide/lead
    'leibatnate': ('lei-bat-na-te', 'debt-bind-NMLZ-PL'),  # 1x Isa 50:1 - creditors
    'leibat': ('lei-bat', 'debt-bind'),               # base - owe
    'eimau': ('ei-mau', '1PL.EXCL-self'),             # 1x Isa 53:6 - ourselves
    'lungzingin': ('lung-zing-in', 'heart-tremble-ERG'),  # 1x - trembling heart
    'dipna': ('dip-na', 'dip-NMLZ'),                  # 1x - dipping
    'taangzah': ('taang-zah', 'grain-measure'),       # 1x - grain measure
    'kolhsiang': ('kolh-siang', 'wrap-clean'),        # 1x - wrapped clean
    'thawhtohna': ('thawh-toh-na', 'rise-reach-NMLZ'),  # 1x - arising
    'lohun': ('lo-hun', 'NEG-time'),                  # 1x - untimely
    'kidokkhia': ('ki-dok-khia', 'REFL-fight-exit'),  # 1x - fight out
    'laho': ('laho', 'bamboo'),                       # 1x - bamboo
    'sangak': ('sang-ak', 'high-over'),               # 1x - high above
    'keeldawi': ('keel-dawi', 'heel-kick'),           # 1x - kick with heel
    'lauthawng': ('lau-thawng', 'fear-wide'),         # 1x - widespread fear
    'notzo': ('not-zo', 'push-ABIL'),                 # 1x - pushable
    'hial': ('hial', 'EMPH'),                         # 1x - emphatic particle
    'kihial': ('ki-hial', 'REFL-EMPH'),               # 1x - emphatic
    'pongkhaina': ('pong-khai-na', 'open-lift-NMLZ'), # 1x - opening
    'nengbaang': ('neng-baang', 'face-flat'),         # 1x - flat face
    'lenkhiatpih': ('len-khiat-pih', 'change-out-with'),  # 1x - exchange
    'kikoihkhong': ('ki-koih-khong', 'REFL-put-tight'),  # 1x - placed firmly
    'suvui': ('suvui', 'sand'),                       # 1x - sand
    'ngongte': ('ngong-te', 'self-PL'),               # 1x - selves
    'singnawtna': ('sing-nawt-na', 'tree-sweep-NMLZ'),  # 1x - sweeping trees
    'simthama': ('sim-thama', 'examine-fully'),       # 1x - examine fully
    'buasuk': ('bua-suk', 'fruit-descend'),           # 1x - fruit fall
    'pokhiat': ('po-khiat', 'burst-out'),             # 1x - burst out
    'mamsak': ('mam-sak', 'soft-CAUS'),               # 1x - soften
    'zauvak': ('zau-vak', 'carry-lift'),              # 1x - carry away
    'paupeengin': ('pau-peeng-in', 'bag-flat-ERG'),   # 1x - in flat bag
    'kiminthansakna': ('ki-min-than-sak-na', 'REFL-name-spread-CAUS-NMLZ'),  # 1x - making famous
    'pehtum': ('peh-tum', 'join-together'),           # 1x - joined together
    'kithehthangte': ('ki-theh-thang-te', 'REFL-change-spread-PL'),  # 1x - changed ones
    'maimanna': ('mai-man-na', 'face-true-NMLZ'),     # 1x - true face
    'gote': ('go-te', 'round-PL'),                    # 1x - rounds
    'suangvui': ('suang-vui', 'stone-sand'),          # 1x - gravel
    'kikemte': ('ki-kem-te', 'REFL-gather-PL'),       # 1x - gathered ones
    'lususu': ('lu-su-su', 'head-push~REDUP'),        # 1x - pushing head
    
    # Round 212: Jeremiah hapax vocabulary
    'buhvai': ('buh-vai', 'rice-chaff'),              # 1x Jer 13:24 - stubble
    'damlenat': ('dam-le-nat', 'well-or-pain'),       # 1x Jer 15:5 - welfare
    'gimhun': ('gim-hun', 'trouble-time'),            # 1x Jer 30:7 - time of trouble
    'kilamna': ('ki-lam-na', 'REFL-build-NMLZ'),      # 1x Jer 31:28 - building
    'vangpi': ('vang-pi', 'power-great'),             # 1x Jer 32:17 - great power
    'zongsang': ('zong-sang', 'accustom-high'),       # 1x Jer 13:23 - accustomed
    'puksite': ('puk-si-te', 'fall-die-PL'),          # 1x - fallen dead
    'keizan': ('kei-zan', '1SG-EMPH'),                # 1x - I myself
    'lambaangin': ('lam-baang-in', 'way-turn-ERG'),   # 1x - turning aside
    'tamsakzaw': ('tam-sak-zaw', 'many-CAUS-more'),   # 1x - made more
    'sunkimlai': ('sun-kim-lai', 'day-full-time'),    # 1x - midday
    'kuiliam': ('kui-liam', 'ring-joint'),            # 1x - ankle
    'tutung': ('tu-tung', 'now-upon'),                # 1x - upon now
    'opsim': ('op-sim', 'embrace-think'),             # 1x - consider
    'lehngatsan': ('leh-ngat-san', 'return-think-price'),  # 1x - recompense
    'sidar': ('sidar', 'cedar'),                      # 1x - cedar (tree)
    'lamnal': ('lam-nal', 'way-smooth'),              # 1x - smooth way
    'buhtang': ('buh-tang', 'rice-long'),             # 1x - tall grain
    'kidongzaw': ('ki-dong-zaw', 'REFL-beat-more'),   # 1x - beaten more
    'dongzaw': ('dong-zaw', 'beat-more'),             # 1x - beaten more
    'pulnatnate': ('pul-nat-na-te', 'fear-pain-NMLZ-PL'),  # 1x - terrors
    'khelkikzaw': ('khel-kik-zaw', 'err-ITER-more'),  # 1x - erred more
    'lehneih': ('leh-neih', 'return-take'),           # 1x - take back
    'tapeuh': ('ta-peuh', 'child-each'),              # 1x - each child
    'e': ('e', 'INTERJ'),                             # 1x - interjection
    'ngutngutna': ('ngut-ngut-na', 'groan-REDUP-NMLZ'),  # 1x - groaning
    'lamlahnate': ('lam-lah-na-te', 'way-take-NMLZ-PL'),  # 1x - way-takings
    'thazawm': ('tha-zawm', 'strength-continue'),     # 1x - continue strong
    'kibetkhiatna': ('ki-bet-khiat-na', 'REFL-pluck-out-NMLZ'),  # 1x - plucking up
    'kisuankhiatna': ('ki-suan-khiat-na', 'REFL-throw-out-NMLZ'),  # 1x - throwing down
    'kithukimna': ('ki-thu-kim-na', 'REFL-word-full-NMLZ'),  # 1x - fulfillment
    'koltanna': ('kol-tan-na', 'roll-stand-NMLZ'),    # 1x - rolling
    'tusawn': ('tu-sawn', 'now-again'),               # 1x - now again
    "vukngo'": ("vuk-ngo'", 'blanket-warm.POSS'),     # 1x - warm blanket
    'tawna': ('taw-na', 'with-NMLZ'),                 # 1x - companion
    'khaphial': ('kha-phial', 'spirit-wander'),       # 1x - wandering spirit
    'kikhiatlam': ('ki-khiat-lam', 'REFL-exit-direction'),  # 1x - departing direction
    'lenuai': ('le-nuai', 'and-under'),               # 1x - and under
    'haltumna': ('hal-tum-na', 'burn-join-NMLZ'),     # 1x - burning
    'tensuak': ('ten-suak', 'dwell-become'),          # 1x - become dwelling
    'hallam': ('hal-lam', 'burn-direction'),          # 1x - burning direction
    'kilehhawl': ('ki-leh-hawl', 'REFL-return-rest'), # 1x - returning rest
    'taikekmang': ('tai-kek-mang', 'flee-reverse-chief'),  # 1x - fleeing chief
    'kinungleh': ('ki-nung-leh', 'REFL-back-return'), # 1x - turning back
    
    # Round 213: Ezekiel hapax vocabulary
    'tumpihzaw': ('tum-pih-zaw', 'stumble-with-more'),      # 1x Ezek 7:19 - stumblingblock
    'biaibuai': ('biai-buai', 'smoke-disperse'),            # 1x Ezek 8:11 - cloud of incense
    'pulpi': ('pul-pi', 'fear-great'),                      # 1x Ezek 14:19 - pestilence
    'kisanna': ('ki-san-na', 'REFL-separate-NMLZ'),         # 1x Ezek 21:23 - divination
    'piancilna': ('pian-cil-na', 'birth-turn-NMLZ'),        # 1x Ezek 29:14 - habitation
    'kisaktheihpihna': ('ki-sak-theih-pih-na', 'REFL-CAUS-know-with-NMLZ'),  # 1x Ezek 30:18 - pomp
    'kizutnelh': ('ki-zut-nelh', 'REFL-ugly-press'),        # 1x Ezek 16:25 - abhorred
    'semsemah': ('sem-sem-ah', 'give-REDUP-LOC'),           # 1x - giving repeatedly
    'nawhkhiatnate': ('nawh-khiat-na-te', 'destroy-out-NMLZ-PL'),  # 1x - destructions
    'sungnungteng': ('sung-nung-teng', 'inside-back-all'),  # 1x - all back inside
    'dinsih': ('din-sih', 'stand-firm'),                    # 1x - stand firm
    'kicimte': ('ki-cim-te', 'REFL-kiss-PL'),               # 1x - kissing ones
    'phuaktawm': ('phuak-tawm', 'compose-short'),           # 1x - short composition
    'lehhanthot': ('leh-han-thot', 'return-CAUS-bring'),    # 1x - bring back
    'zulkatteng': ('zul-kat-teng', 'follow-cut-all'),       # 1x - all following
    'sawpkhiatsak': ('sawp-khiat-sak', 'sweep-out-CAUS'),   # 1x - cause to sweep out
    'guaizaw': ('guai-zaw', 'crooked-more'),                # 1x - more crooked
    'siateng': ('sia-teng', 'evil-all'),                    # 1x - all evil
    'zonkhiatsak': ('zon-khiat-sak', 'flee-out-CAUS'),      # 1x - cause to flee
    'kaihkhopkik': ('kaih-khop-kik', 'lead-gather-ITER'),   # 1x - gather again
    'seuhseuhin': ('seuh-seuh-in', 'search-REDUP-ERG'),     # 1x - searching repeatedly
    'sumaigawp': ('sumai-gawp', 'face-cover'),              # 1x - cover face
    'kimlaipi': ('kim-lai-pi', 'full-time-great'),          # 1x - great fullness
    'ngunteng': ('ngun-teng', 'silver-all'),                # 1x - all silver
    'bal': ('bal', 'tired'),                                # 1x - tired/weary
    'ciangzo': ('ciang-zo', 'become-ABIL'),                 # 1x - become able
    'kawngten': ('kawng-ten', 'gate-above'),                # 1x - above gate
    'kihzah': ('kih-zah', 'hide-fear'),                     # 1x - hiding in fear
    'huknate': ('huk-na-te', 'shelter-NMLZ-PL'),            # 1x - shelters
    'khekhapteng': ('khek-hap-teng', 'mark-all'),           # 1x - all marks (variant)
    'petkham': ('pet-kham', 'block-prevent'),               # 1x - blocking
    'kuikham': ('kui-kham', 'leg-prevent'),                 # 1x - leg chains
    'vuh': ('vuh', 'blow'),                                 # 1x - blow (wind)
    'taubeel': ('tau-beel', 'gourd-wild'),                  # 1x - wild gourd
    'bun': ('bun', 'portion'),                              # 1x - portion
    'kihongkek': ('ki-hong-kek', 'REFL-open-reverse'),      # 1x - opened
    'hoihpipite': ('hoih-pi-pi-te', 'good-great-REDUP-PL'), # 1x - very good ones
    'tungkhuh': ('tung-khuh', 'upon-nest'),                 # 1x - nest upon
    'haknawte': ('hak-naw-te', 'difficult-small-PL'),       # 1x - small difficulties
    'ningsing': ('ning-sing', 'remember-tree'),             # 1x - memorial tree
    'hotte': ('hot-te', 'save-PL'),                         # 1x - saved ones
    'tuikiate': ('tui-kia-te', 'water-boil-PL'),            # 1x - boiling waters
    'geiteng': ('gei-teng', 'edge-all'),                    # 1x - all edges
    'daicipsuak': ('dai-cip-suak', 'quiet-deep-become'),    # 1x - become deeply quiet
    'karbankel': ('karbankel', 'carbuncle'),                # 1x - carbuncle (gem)
    'puakhiamang': ('puak-hia-mang', 'create-there-chief'), # 1x - created there
    'kitante': ('ki-tan-te', 'REFL-stand-PL'),              # 1x - standing ones
    'gunsung': ('gun-sung', 'heart-inside'),                # 1x - inside heart
    'kamun': ('ka-mun', '1SG.GEN-place'),                   # 1x - my place
    'khiang': ('khiang', 'quick'),                          # 1x - quickly
    
    # Round 214: Daniel/Hosea/Amos/Joel hapax vocabulary
    'kipawlkhawmna': ('ki-pawl-khawm-na', 'REFL-group-join-NMLZ'),  # 1x Dan 11:6 - alliance
    'mangthangpak': ('mang-thang-pak', 'vanish-quick-INTENS'),  # 1x Hos 6:4 - quickly vanishing
    'kitumna': ('ki-tum-na', 'REFL-stumble-NMLZ'),          # 1x Amos 2:2 - tumult
    'leitawina': ('lei-tawi-na', 'borrow-take-NMLZ'),       # 1x Amos 2:8 - pledge
    'lamkik': ('lam-kik', 'build-ITER'),                    # 46x - build/rebuild
    'lamkikna': ('lam-kik-na', 'build-ITER-NMLZ'),          # 6x - repairing/rebuilding
    'lawkgawpna': ('lawkgawp-na', 'spoil-NMLZ'),            # 1x Dan 11:33 - spoil
    'hauhsakna': ('hauh-sak-na', 'rich-CAUS-NMLZ'),         # 3x - enrichment
    'zutsiang': ('zut-siang', 'ugly-handsome'),             # 1x - ugly-handsome
    'dosuakzo': ('do-suak-zo', 'fight-become-finish'),      # 1x - finished fighting
    'tangtungzo': ('tang-tung-zo', 'rise-upon-finish'),     # 1x - risen up
    'lehbawlin': ('leh-bawl-in', 'return-make-CVB'),        # 1x - making return
    'manphateng': ('man-pha-teng', 'price-good-all'),       # 1x - all valuable
    'kenkante': ('ken-kan-te', 'carry-REDUP-PL'),           # 1x - carriers
    'behlaplap': ('beh-lap-lap', 'tribe-lap~REDUP'),        # 1x - tribes
    'phawknuam': ('phawk-nuam', 'remember-pleasant'),       # 1x - pleasant memory
    'singthem': ('sing-them', 'tree-spit'),                 # 1x - tree sap
    'thengpak': ('theng-pak', 'clear-INTENS'),              # 1x Hos 6:4 - quickly clear
    'zuaupiteng': ('zuau-pi-teng', 'lie-great-all'),        # 1x - all great lies
    'mohbawl': ('moh-bawl', 'mock-make'),                   # 1x - mocking
    'seem': ('seem', 'give'),                               # 1x - give (variant)
    'kanlam': ('kan-lam', 'turn-direction'),                # 1x - turning direction
    'lehgen': ('leh-gen', 'return-say'),                    # 1x - say again
    'lehsawm': ('leh-sawm', 'return-call'),                 # 1x - call back
    'tuiphuan': ('tui-phuan', 'water-blanket'),             # 1x - water covering
    'dengcip': ('deng-cip', 'strike-deep'),                 # 1x - strike deep
    'thuapthuapin': ('thuap-thuap-in', 'boast-REDUP-ERG'),  # 1x - boasting
    'kalkham': ('kal-kham', 'walk-prevent'),                # 1x - prevent walking
    'phualnek': ('phual-nek', 'nest-press'),                # 1x - press nest
    'ngawhpiak': ('ngawh-piak', 'bite-give'),               # 1x - give bite
    'hailuat': ('hai-luat', 'pluck-pull'),                  # 1x - pluck out
    'theikungteng': ('thei-kung-teng', 'fruit-tree-all'),   # 1x - all fruit trees
    'sengsang': ('seng-sang', 'rise-high'),                 # 1x - rise high
    'nisuhte': ('ni-suh-te', 'day-count-PL'),               # 1x - counted days
    'alh': ('alh', 'wing'),                                 # 1x - wing (variant)
    'heempai': ('heem-pai', 'scatter-go'),                  # 1x - scatter away
    'hoihbekzah': ('hoih-bek-zah', 'good-only-EMPH'),       # 1x - only good
    'zinlin': ('zin-lin', 'journey-walk'),                  # 1x - journey walk
    'khauhtuak': ('khauh-tuak', 'strict-very'),             # 1x - very strict
    'netcipsuk': ('net-cip-suk', 'twist-deep-push'),        # 1x - twist deep
    'nengcipsuk': ('neng-cip-suk', 'lean-deep-push'),       # 1x - lean deep
    'kimawksai': ('ki-mawk-sai', 'REFL-wet-leave'),         # 1x - left wet
    'kulhvang': ('kulh-vang', 'wall-power'),                # 1x - wall power
    'dikdekin': ('dik-dek-in', 'straight-REDUP-ERG'),       # 1x - straightening
    'nuaigawp': ('nuai-gawp', 'under-cover'),               # 1x - cover under
    'zumkhak': ('zum-khak', 'bow-hard'),                    # 1x - hard bow
    'neuseekin': ('neu-seek-in', 'small-search-ERG'),       # 1x - searching small
    'anhaihna': ('an-haih-na', 'food-want-NMLZ'),           # 1x - food wanting
    'naizo': ('nai-zo', 'near-finish'),                     # 1x - nearly finished
    'hehhak': ('heh-hak', 'angry-difficult'),               # 1x - difficult anger
    'sileng': ('si-leng', 'die-if'),                        # 1x - if die
    
    # Round 215: Matthew/Malachi hapax vocabulary
    'genkholhsakna': ('gen-kholh-sak-na', 'say-INTENS-CAUS-NMLZ'),  # 1x Matt 13:35 - utterance
    'kiphasakteng': ('ki-pha-sak-teng', 'REFL-good-CAUS-all'),  # 1x Mal 3:15 - proud ones
    'kiciamnate': ('ki-ciam-na-te', 'REFL-promise-NMLZ-PL'),  # 1x Matt 5:33 - oaths
    'leidaina': ('lei-dai-na', 'earth-quiet-NMLZ'),         # 1x Matt 13:5 - stony places
    'kilawnkeek': ('ki-lawn-keek', 'REFL-throw-reverse'),   # 1x Matt 24:2 - thrown down
    'kibulphuh': ('ki-bul-phuh', 'REFL-begin-plant'),       # 1x Matt 12:37 - condemned
    'mualsuangte': ('mual-suang-te', 'grave-stone-PL'),     # 1x Matt 23:29 - sepulchres
    'sehnih': ('seh-nih', 'appoint-two'),                   # 1x - appoint two
    'mitkua': ('mit-kua', 'eye-hole'),                      # 1x - eye socket
    'muatin': ('muat-in', 'rot-ERG'),                       # 1x - rotting
    'khilongte': ('khi-long-te', 'climb-round-PL'),         # 1x - climbers
    'hoihmahin': ('hoih-mah-in', 'good-self-ERG'),          # 1x - very well
    'hoihmah': ('hoih-mah', 'good-self'),                   # 1x - very good
    'palsatkhak': ('pal-sat-khak', 'separate-hard-firm'),   # 1x - firmly separated
    'citheibek': ('ci-theih-bek', 'say-know-only'),         # 1x Mal 3:15 - just say
    'nuaisiahin': ('nuai-siah-in', 'under-throw-ERG'),      # 1x - throwing under
    'lemtuahin': ('lem-tuah-in', 'image-do-ERG'),           # 1x - doing image
    'maksim': ('mak-sim', 'Mark-SIM'),                      # 1x - like Mark
    'kihilkik': ('ki-hil-kik', 'REFL-turn-ITER'),           # 1x - turn back
    'khulna': ('khul-na', 'bow-NMLZ'),                      # 1x - bowing
    'kangsa': ('kang-sa', 'burn-leave'),                    # 1x - left burning
    'guktheihna': ('guk-theih-na', 'bow-know-NMLZ'),        # 1x - knowing bow
    'kheek': ('kheek', 'mark'),                             # 1x - mark (variant)
    'guatzaw': ('guat-zaw', 'crooked-more'),                # 1x - more crooked
    'kawcikin': ('kaw-cik-in', 'call-quick-ERG'),           # 1x - calling quickly
    'gamtateng': ('gam-ta-teng', 'land-child-all'),         # 1x - all land children
    'nangpipi': ('nang-pi-pi', '2SG-great~REDUP'),          # 1x - you very great
    'kaigawmin': ('kai-gawm-in', 'lead-around-ERG'),        # 1x - leading around
    'tawmbek': ('tawm-bek', 'short-only'),                  # 1x - only short
    'kozaw': ('ko-zaw', 'cry-more'),                        # 1x - cry more
    'kihtazaw': ('kih-ta-zaw', 'hide-child-more'),          # 1x - hide more
    'mawkkiat': ('mawk-kiat', 'wet-break'),                 # 1x - wet break
    'lopakungte': ('lo-pa-kung-te', 'field-male-tree-PL'),  # 1x - field workers
    'upnop': ('up-nop', 'believe-soft'),                    # 1x - soft belief
    'dopbawl': ('dop-bawl', 'attack-make'),                 # 1x - make attack
    'lingbulsumte': ('ling-bul-sum-te', 'bell-ball-money-PL'),  # 1x - money bells
    'bingsak': ('bing-sak', 'flat-CAUS'),                   # 1x - flatten
    'lomhen': ('lom-hen', 'friend-appear'),                 # 1x - appear friend
    'tungthamun': ('tung-tha-mun', 'upon-new-place'),       # 1x - new place upon
    'pusuakte': ('pu-suak-te', 'grandpa-become-PL'),        # 1x - ancestors
    'suangneu': ('suang-neu', 'stone-small'),               # 1x - small stone
    'phawkkhial': ('phawk-khial', 'remember-err'),          # 1x - misremember
    'meiingo': ('meii-ngo', 'fire-warm'),                   # 1x - warm fire
    'sihbup': ('sih-bup', 'die-fall'),                      # 1x - fall dead
    'dongtak': ('dong-tak', 'beat-true'),                   # 1x - truly beat
    'ciangbek': ('ciang-bek', 'become-only'),               # 1x - only become
    'sehte': ('seh-te', 'appoint-PL'),                      # 1x - appointed ones
    'khingin': ('khing-in', 'lean-ERG'),                    # 1x - leaning
    'dongkhakin': ('dong-khak-in', 'beat-firm-ERG'),        # 1x - beating firmly
    'thovai': ('tho-vai', 'awake-chaff'),                   # 1x - chaff awake
    
    # Round 216: Luke hapax vocabulary
    'kivukdim': ('ki-vuk-dim', 'REFL-fill-full'),           # 1x Luke 3:5 - be filled
    'kiniamkhiatsuk': ('ki-niam-khiat-suk', 'REFL-low-out-push'),  # 1x Luke 18:14 - be abased
    'thuambuak': ('thuam-buak', 'vegetable-scatter'),       # 1x Luke 11:42 - rue (herb)
    'lamliante': ('lam-lian-te', 'way-great-PL'),           # 1x Luke 14:23 - highways
    'kisamte': ('ki-sam-te', 'REFL-invite-PL'),             # 1x Luke 14:8 - invited ones
    'kisuampa': ('ki-suam-pa', 'REFL-throw-NMLZ.M'),        # 1x Luke 10:36 - fallen one
    'lammat': ('lam-mat', 'way-forget'),                    # 1x - forget way
    'laitah': ('lai-tah', 'time-exact'),                    # 1x - exact time
    'ngeizel': ('ngei-zel', 'possess-separate'),            # 1x - separate possession
    'sunkham': ('sun-kham', 'day-prevent'),                 # 1x - prevent day
    'omomin': ('om-om-in', 'be-REDUP-ERG'),                 # 1x - being
    'kawite': ('kawi-te', 'crooked-PL'),                    # 1x Luke 3:5 - crooked
    'leihumte': ('lei-hum-te', 'earth-rough-PL'),           # 1x Luke 3:5 - rough ways
    'mawkcih': ('mawk-cih', 'wet-say'),                     # 1x - say wet
    'khanna': ('khan-na', 'grow-NMLZ'),                     # 1x - growing
    'keenah': ('keen-ah', 'straight-LOC'),                  # 1x - at straight
    'eukhiat': ('eu-khiat', 'shake-out'),                   # 1x - shake out
    'phuisamte': ('phui-sam-te', 'clothe-invite-PL'),       # 1x - clothed ones
    'dawhlai': ('dawh-lai', 'beautiful-time'),              # 1x - beautiful time
    'khuamkua': ('khuam-kua', 'village-hole'),              # 1x - village pit
    'suangsung': ('suang-sung', 'stone-inside'),            # 1x - inside stone
    'madiakin': ('ma-diak-in', 'EMPH-exact-ERG'),           # 1x - exactly
    'nulkeusak': ('nul-keu-sak', 'female-unmarried-CAUS'),  # 1x - cause unmarried
    'deplum': ('dep-lum', 'press-heap'),                    # 1x - pressed heap
    'siavuante': ('sia-vuan-te', 'evil-spirit-PL'),         # 1x - evil spirits
    'kangpah': ('kang-pah', 'burn-fire'),                   # 1x - fire burn
    'sawngteng': ('sawng-teng', 'vessel-all'),              # 1x - all vessels
    'lenkawmin': ('len-kawm-in', 'play-around-ERG'),        # 1x - playing around
    'taangkim': ('taang-kim', 'rise-complete'),             # 1x - rise complete
    'donkha': ('don-kha', 'receive-mouth'),                 # 1x - receive word
    'khiathuah': ('khiat-huah', 'out-throw'),               # 1x - throw out
    'inntuan': ('inn-tuan', 'house-bear'),                  # 1x - bear house
    'guanzaw': ('guan-zaw', 'gaze-more'),                   # 1x - gaze more
    'leikha': ('lei-kha', 'earth-dry'),                     # 1x - dry earth
    'zuma': ('zum-a', 'bow-NMLZ'),                          # 1x - bowing
    'kaigawpin': ('kai-gawp-in', 'lead-cover-ERG'),         # 1x - leading cover
    'liausum': ('liau-sum', 'wander-money'),                # 1x - wander money
    'nawtsuakin': ('nawt-suak-in', 'drive-become-ERG'),     # 1x - driving out
    'tusakzaw': ('tu-sak-zaw', 'now-CAUS-more'),            # 1x - cause more now
    'angtanhuai': ('ang-tan-huai', 'smell-stand-ABIL'),     # 1x - able to smell
    'phuhkhit': ('phuh-khit', 'plant-finish'),              # 1x - finished planting
    'begap': ('be-gap', 'give-close'),                      # 1x - give close
    'vaiciah': ('vai-ciah', 'chaff-eat'),                   # 1x - eat chaff
    'tavuanteng': ('ta-vuan-teng', 'child-spirit-all'),     # 1x - all spirit children
    'taanzaih': ('taan-zaih', 'rise-build'),                # 1x - rise build
    'donnop': ('don-nop', 'receive-want'),                  # 1x - want to receive
    'khutdawh': ('khut-dawh', 'hand-beautiful'),            # 1x - beautiful hand
    'geinai': ('gei-nai', 'edge-near'),                     # 1x - near edge
    'tuntom': ('tun-tom', 'arrive-hurry'),                  # 1x - hurry arrive
    'ginalopa': ('gina-lo-pa', 'believe-NEG-NMLZ.M'),       # 1x - unbeliever
    
    # Round 217: Acts/Romans hapax vocabulary
    'hinkiksakna': ('hin-kik-sak-na', 'live-ITER-CAUS-NMLZ'),  # 1x Acts 13:34 - raising up
    'kituiphumna': ('ki-tui-phum-na', 'REFL-water-immerse-NMLZ'),  # 1x Acts 19:3 - baptism
    'thawhsakkikna': ('thawh-sak-kik-na', 'arise-CAUS-ITER-NMLZ'),  # 1x Rom 1:4 - resurrection
    'khihsakna': ('khih-sak-na', 'bind-CAUS-NMLZ'),          # 1x Acts 22:30 - bands
    'khawlsakna': ('khawl-sak-na', 'rest-CAUS-NMLZ'),        # 1x Acts 27:29 - anchors
    'mawhnopnate': ('mawh-nop-na-te', 'sin-want-NMLZ-PL'),   # 1x Rom 7:5 - motions of sins
    'tamlai': ('tam-lai', 'many-time'),                     # 1x - many times
    'kenkon': ('ken-kon', 'carry-move'),                    # 1x - carry move
    'nawla': ('naw-la', 'drive-take'),                      # 1x - drive take
    'honsaknate': ('hon-sak-na-te', 'open-CAUS-NMLZ-PL'),    # 1x - openings
    'masakun': ('ma-sak-un', 'EMPH-CAUS-IMP'),               # 1x - make surely
    'tunni': ('tun-ni', 'arrive-day'),                      # 1x - arrival day
    'singkol': ('sing-kol', 'tree-roll'),                   # 1x - rolling tree
    'piansakma': ('pian-sak-ma', 'birth-CAUS-EMPH'),         # 1x - truly begotten
    'zatzia': ('zat-zia', 'use-manner'),                    # 1x - manner of use
    'upzawh': ('up-zawh', 'believe-finish'),                # 1x - believe finish
    'aitawi': ('ai-tawi', 'price-take'),                    # 1x - take price
    'maimankhak': ('mai-man-khak', 'face-price-firm'),      # 1x - firm face price
    'lapnuam': ('lap-nuam', 'lap-pleasant'),                # 1x - pleasant lap
    'phawkkawmin': ('phawk-kawm-in', 'remember-around-ERG'),  # 1x - remembering
    'tapkhap': ('tap-khap', 'weep-cry'),                    # 1x - weeping
    'khihcipna': ('khih-cip-na', 'bind-deep-NMLZ'),          # 1x - deep binding
    'gawlmek': ('gawl-mek', 'pond-mud'),                    # 1x - pond mud
    'khensatin': ('khen-sat-in', 'separate-hard-ERG'),      # 1x - separating hard
    'kitawngpah': ('ki-tawng-pah', 'REFL-word-strike'),     # 1x - dispute
    'hupha': ('hu-pha', 'follow-good'),                     # 1x - follow good
    'kikoh': ('ki-koh', 'REFL-call'),                       # 1x - be called
    'hialbawl': ('hial-bawl', 'visit-make'),                # 1x - make visit
    'ciangzum': ('ciang-zum', 'become-bow'),                # 1x - become bowing
    'munsimtham': ('mun-sim-tham', 'place-think-new'),      # 1x - new thinking place
    'leidawk': ('lei-dawk', 'earth-dig'),                   # 1x - dig earth
    'cintenin': ('cin-ten-in', 'ripen-above-ERG'),          # 1x - ripening above
    'khengkhin': ('kheng-khin', 'lean-finish'),             # 1x - finished leaning
    'hailua': ('hai-lua', 'pluck-exceed'),                  # 1x - pluck much
    'piakkhongin': ('piak-khong-in', 'give-hole-ERG'),      # 1x - giving hole
    'ciinna': ('cii-na', 'sting-NMLZ'),                     # 1x - sting
    'luiteng': ('lui-teng', 'river-all'),                   # 1x - all rivers
    'maleep': ('ma-leep', 'EMPH-quick'),                    # 1x - very quick
    'lungduaitakin': ('lung-duai-tak-in', 'heart-soft-true-ERG'),  # 1x - truly soft heart
    'hitalehang': ('hi-ta-leh-ang', 'this-child-and-FUT'),  # 1x - this child then
    'huhnuam': ('huh-nuam', 'blow-pleasant'),               # 1x - pleasant blowing
    'theihma': ('theih-ma', 'know-before'),                 # 1x - foreknow
    'zatnop': ('zat-nop', 'use-want'),                      # 1x - want to use
    'paupeensak': ('pau-peen-sak', 'word-open-CAUS'),       # 1x - cause open word
    'muktuk': ('muk-tuk', 'suck~REDUP'),                     # 1x - sucking
    'lasuk': ('la-suk', 'song-push'),                       # 1x - push song
    'gitnat': ('git-nat', 'squeeze-pain'),                  # 1x - painful squeeze
    'hoihkan': ('hoih-kan', 'good-grow'),                   # 1x - grow good
    'pukding': ('puk-ding', 'fall-FUT'),                    # 1x - will fall
    
    # Round 218: Galatians/Ephesians/Philippians/1 Timothy hapax
    'lunghihmawhsak': ('lung-hih-mawh-sak', 'heart-fear-sin-CAUS'),  # 1x Gal 4:11 - afraid
    'dokhawmna': ('do-khawm-na', 'fight-join-NMLZ'),        # 1x Phil 1:27 - striving together
    'kinopmawhna': ('ki-nop-mawh-na', 'REFL-want-sin-NMLZ'),  # 1x 1Tim 2:8 - doubting
    'suahtheihna': ('suah-theih-na', 'become-know-NMLZ'),   # 1x Gal 3:26 - becoming
    'thanopna': ('tha-nop-na', 'strength-want-NMLZ'),       # 1x Eph 6:7 - good will
    'lahnopna': ('lah-nop-na', 'represent-want-NMLZ'),      # 1x Gal 4:24 - allegory
    'haisapi': ('hai-sa-pi', 'pluck-flesh-great'),          # 1x - great flesh pluck
    'lungkhampihin': ('lung-kham-pih-in', 'heart-prevent-with-ERG'),  # 1x - with heart
    'phattuamnapi': ('phat-tuam-na-pi', 'praise-much-NMLZ-great'),  # 1x - great praise
    'bangmahpi': ('bang-mah-pi', 'what-self-great'),        # 1x - nothing great
    'sumlepaite': ('sum-le-pai-te', 'money-and-go-PL'),     # 1x - money goers
    'lannate': ('lan-na-te', 'appear-NMLZ-PL'),             # 1x - appearances
    'zatkhak': ('zat-khak', 'use-firm'),                    # 1x - firm use
    'kiletna': ('ki-let-na', 'REFL-cut-NMLZ'),              # 1x - circumcision
    'patkhit': ('pat-khit', 'attach-finish'),               # 1x - finished attaching
    'kimemat': ('ki-mem-at', 'REFL-soft-very'),             # 1x - very soft
    'nungphiat': ('nung-phiat', 'back-abandon'),            # 1x - abandon back
    'piakma': ('piak-ma', 'give-before'),                   # 1x - give before
    'vangneite': ('vang-nei-te', 'power-have-PL'),          # 1x - powerful ones
    'pianuamte': ('pian-uam-te', 'birth-pleasant-PL'),      # 1x - pleasant births
    'kipetkha': ('ki-pet-kha', 'REFL-block-dry'),           # 1x - be blocked
    'hahbawl': ('hah-bawl', 'tired-make'),                  # 1x - make tired
    'meimapawn': ('mei-ma-pawn', 'fire-EMPH-even'),         # 1x - even fire
    'sehkholhsa': ('seh-kholh-sa', 'appoint-INTENS-already'),  # 1x - already appointed
    'pianlui': ('pian-lui', 'birth-old'),                   # 1x - old birth
    'gawpgawpnate': ('gawp-gawp-na-te', 'cover-REDUP-NMLZ-PL'),  # 1x - coverings
    'nawtsakzaw': ('nawt-sak-zaw', 'drive-CAUS-more'),      # 1x - drive more
    'huhkim': ('huh-kim', 'blow-complete'),                 # 1x - blow complete
    'hahkatlua': ('hah-kat-lua', 'tired-cut-exceed'),       # 1x - exceed tired
    'supngam': ('sup-ngam', 'suck-dare'),                   # 1x - dare suck
    'piakkhiatnate': ('piak-khiat-na-te', 'give-out-NMLZ-PL'),  # 1x - givings out
    'theihtelnate': ('theih-tel-na-te', 'know-join-NMLZ-PL'),  # 1x - knowledge
    'sepbel': ('sep-bel', 'work-leave'),                    # 1x - leave work
    'khangcingin': ('khang-cing-in', 'generation-still-ERG'),  # 1x - in generation
    'tungthamin': ('tung-tham-in', 'upon-new-ERG'),         # 1x - upon new
    'siavuanpa': ('sia-vuan-pa', 'evil-spirit-NMLZ.M'),     # 1x - evil spirit (person)
    'silbawlnate': ('sil-bawl-na-te', 'clothe-make-NMLZ-PL'),  # 1x - clothings
    'gimlawhkhak': ('gim-lawh-khak', 'trouble-earn-firm'),  # 1x - firmly earn trouble
    'dahluat': ('dah-luat', 'dry-pull'),                    # 1x - pull dry
    'tunvat': ('tun-vat', 'arrive-quick'),                  # 1x - arrive quick
    'mutlum': ('mut-lum', 'suck-heap'),                     # 1x - heap suck
    'suplawhkhak': ('sup-lawh-khak', 'suck-earn-firm'),     # 1x - firmly earn suck
    'hiathiatin': ('hiat-hiat-in', 'there-REDUP-ERG'),      # 1x - there repeatedly
    'khangsimnate': ('khang-sim-na-te', 'generation-think-NMLZ-PL'),  # 1x - generation thoughts
    'palepa': ('pale-pa', 'separate-NMLZ.M'),               # 1x - separated one
    'gute': ('gu-te', 'bow-PL'),                            # 1x - bows
    'kilehbulhin': ('ki-leh-bul-in', 'REFL-return-begin-CVB'),  # 1x - returning begin
    'uphuai': ('up-huai', 'believe-ABIL'),                  # 1x - able to believe
    'dozawh': ('do-zawh', 'fight-finish'),                  # 1x - finish fighting
    'phalkei': ('phal-kei', 'allow-1SG'),                   # 1x - allow me
    
    # Round 219: Exodus/Job/Psalms hapax vocabulary
    'kiphutte': ('ki-phut-te', 'REFL-fasten-PL'),           # 1x Exod 28:14 - ouches
    'piansaksate': ('pian-sak-sa-te', 'birth-CAUS-already-PL'),  # 1x Job 12:10 - created ones
    'khasiatpihnate': ('kha-siat-pih-na-te', 'spirit-evil-with-NMLZ-PL'),  # 1x Job 42:11 - condolences
    'kisukcipnate': ('ki-suk-cip-na-te', 'REFL-push-deep-NMLZ-PL'),  # 1x Ps 44:24 - oppressions
    'lauhuainate': ('lau-huai-na-te', 'fear-ABIL-NMLZ-PL'),  # 1x Ps 66:12 - terrors
    'kikhemnate': ('ki-khem-na-te', 'REFL-limit-NMLZ-PL'),  # 1x Ps 55:11 - guile
    'gimte': ('gim-te', 'trouble-PL'),                      # 1x - troubles
    'sakhipite': ('sa-khi-pi-te', 'flesh-leg-great-PL'),    # 1x - great legs
    'kaihte': ('kaih-te', 'lead-PL'),                       # 1x - led ones
    'nawnkhia': ('nawn-khia', 'remain-out'),                # 1x - remain out
    'khimzin': ('khim-zin', 'dark-journey'),                # 1x - dark journey
    'khian': ('khian', 'grow'),                             # 1x - grow (variant)
    'luaksuahhuai': ('luak-suah-huai', 'vomit-become-ABIL'),  # 1x - able to vomit
    'kalkhia': ('kal-khia', 'walk-out'),                    # 1x - walk out
    'nawtkhiat': ('nawt-khiat', 'drive-out'),               # 1x - drive out
    'muatsakmang': ('muat-sak-mang', 'rot-CAUS-chief'),     # 1x - cause to rot
    'lainatna': ('lai-nat-na', 'time-pain-NMLZ'),           # 1x - time of pain
    'muammuam': ('muam~muam', 'dark~REDUP'),                # 1x - very dark
    'kawtciimsak': ('kawt-ciim-sak', 'gate-shut-CAUS'),     # 1x - cause shut gate
    'kuante': ('kuan-te', 'authority-PL'),                  # 1x - authorities
    'taciingte': ('ta-ciing-te', 'child-NEG-PL'),           # 1x - barren ones
    'khangnozawte': ('khang-no-zaw-te', 'generation-young-more-PL'),  # 1x - younger generations
    'thengta': ('theng-ta', 'clear-child'),                 # 1x - clear child
    'zawlmitin': ('zawl-mit-in', 'prophet-eye-ERG'),        # 1x - prophet eye
    "galte'n": ("gal-te-'n", 'enemy-PL-ERG'),               # 1x - by enemies
    'cinatsakna': ('ci-nat-sak-na', 'say-pain-CAUS-NMLZ'),  # 1x - rebuke
    'henhanna': ('hen-han-na', 'appear-CAUS-NMLZ'),         # 1x - revelation
    'mualleguamte': ('mual-le-guam-te', 'grave-and-hole-PL'),  # 1x - graves and pits
    'kaisakzo': ('kai-sak-zo', 'lead-CAUS-finish'),         # 1x - finished leading
    'zaangmul': ('zaang-mul', 'arm-round'),                 # 1x - round arm
    "na'n": ("na-'n", '2SG.GEN-ERG'),                       # 1x - by your
    'cingvalin': ('cing-val-in', 'still-INTENS-ERG'),       # 1x - very still
    'luatnate': ('luat-na-te', 'pull-NMLZ-PL'),             # 1x - pullings
    'kisiahna': ('ki-siah-na', 'REFL-throw-NMLZ'),          # 1x - casting
    'zangawpte': ('zan-gawp-te', 'night-cover-PL'),         # 1x - night covers
    'khesikna': ('khe-sik-na', 'foot-step-NMLZ'),           # 1x - footsteps
    'ngangngang': ('ngang~ngang', 'steady~REDUP'),          # 1x - very steady
    'buluah': ('bu-luah', 'group-scatter'),                 # 1x - scatter group
    'deudaute': ('deu-dau-te', 'little-little-PL'),         # 1x - little ones
    'kiimvelin': ('ki-im-vel-in', 'REFL-house-around-CVB'),  # 1x - around house
    'helhhawtte': ('helh-hawt-te', 'advise-hard-PL'),       # 1x - hard advisers
    'sumleina': ('sum-lei-na', 'money-borrow-NMLZ'),        # 1x - usury
    'tuancilte': ('tuan-cil-te', 'ride-turn-PL'),           # 1x - riders
    'toktol': ('tok-tol', 'peck-hit'),                      # 1x - pecking
    'suhgawpnate': ('suh-gawp-na-te', 'count-cover-NMLZ-PL'),  # 1x - accountings
    'thuciamsate': ('thu-ciam-sa-te', 'word-promise-already-PL'),  # 1x - promised ones
    'leivumte': ('lei-vum-te', 'earth-heap-PL'),            # 1x - earth heaps
    'nunungin': ('nu-nung-in', 'mother-back-ERG'),          # 1x - after mother
    
    # Round 220: Isaiah hapax vocabulary
    'kitawhzauna': ('ki-tawh-zau-na', 'REFL-with-perplexity-NMLZ'),  # 1x Isa 22:5 - perplexity
    'kitamvuisak': ('ki-tam-vui-sak', 'REFL-many-dust-CAUS'),  # 1x Isa 28:28 - bruise
    'kisialhnate': ('ki-sialh-na-te', 'REFL-boast-NMLZ-PL'),  # 1x Isa 16:6 - lies/boasts
    'puansungsilhte': ('puan-sung-silh-te', 'cloth-inside-clothe-PL'),  # 1x Isa 3:23 - vails
    'kipahtawite': ('ki-pah-tawi-te', 'REFL-good-take-PL'),  # 1x Isa 23:8 - honourable ones
    'thakhauhsakin': ('tha-khauh-sak-in', 'strength-strong-CAUS-CVB'),  # 2x Isa - strengthening
    'kamkeite': ('kam-kei-te', 'word-1SG-PL'),               # 1x - my words
    'bangzahtakin': ('bang-zah-tak-in', 'what-much-true-ERG'),  # 1x - how much truly
    'etlawmin': ('et-lawm-in', 'look-together-ERG'),         # 1x - looking together
    'pattahsa': ('pat-tah-sa', 'attach-exact-already'),      # 1x - exactly attached
    'sialomtangte': ('sia-lom-tang-te', 'evil-friend-rise-PL'),  # 1x - evil friends rising
    'khebuh': ('khe-buh', 'foot-rice'),                      # 1x - foot of rice
    'kawngtente': ('kawng-ten-te', 'gate-above-PL'),         # 1x - above gates
    'siseihte': ('si-seih-te', 'die-lean-PL'),               # 1x - dying lean ones
    'naisakin': ('nai-sak-in', 'near-CAUS-CVB'),             # 1x - making near
    'nawtsuk': ('nawt-suk', 'drive-push'),                   # 1x - drive push
    'tonbucipin': ('ton-bu-cip-in', 'meet-group-deep-ERG'),  # 1x - meeting deeply
    'ciangkhutin': ('ciang-khut-in', 'become-hand-ERG'),     # 1x - becoming hand
    'munphiah': ('mun-phiah', 'place-flat'),                 # 1x - flat place
    'kaiton': ('kai-ton', 'lead-meet'),                      # 1x - lead meet
    'kimetmai': ('ki-met-mai', 'REFL-squeeze-face'),         # 1x - squeeze face
    'ngahmunah': ('ngah-mun-ah', 'receive-place-LOC'),       # 1x - at receiving place
    'phawkkhak': ('phawk-khak', 'remember-firm'),            # 1x - remember firmly
    'lolaite': ('lo-lai-te', 'field-time-PL'),               # 1x - field times
    'pehin': ('peh-in', 'give-ERG'),                         # 1x - giving
    'kimut': ('ki-mut', 'REFL-suck'),                        # 1x - suck self
    'kangcipin': ('kang-cip-in', 'burn-deep-ERG'),           # 1x - burning deep
    'gante': ('gan-te', 'carry-PL'),                         # 1x - carriers
    'sidaangsak': ('si-daang-sak', 'die-tall-CAUS'),         # 1x - cause tall die
    'sualpuante': ('sual-puan-te', 'sin-cloth-PL'),          # 1x - sin cloths
    'kiseepsa': ('ki-seep-sa', 'REFL-burn-already'),         # 1x - already burned
    'tuibempi': ('tui-bem-pi', 'water-edge-great'),          # 1x - great water edge
    'mettolna': ('met-tol-na', 'squeeze-hit-NMLZ'),          # 1x - squeezing
    'huiheek': ('hui-heek', 'wind-fold'),                    # 1x - wreath (KJV: "wreaths of chain work")
    'thangzakte': ('thang-zak-te', 'news-hear-PL'),          # 1x - news hearers
    'bengtumsuk': ('beng-tum-suk', 'side-stumble-push'),     # 1x - push stumble side
    'kiheekheek': ('ki-heek-heek', 'REFL-fold~REDUP'),         # 1x - writhe (repeated folding, Isa 26:18)
    'kikualvial': ('ki-kual-vial', 'REFL-hold-round'),       # 1x - holding round
    'kithukkim': ('ki-thuk-kim', 'REFL-word-complete'),      # 1x - complete word
    'dengawpna': ('den-gawp-na', 'strike-cover-NMLZ'),       # 1x - striking
    'kalkhamin': ('kal-kham-in', 'walk-prevent-ERG'),        # 1x - preventing walk
    'cilvui': ('cil-vui', 'chaff-dust'),                     # 1x Isa 28:28 - chaff
    'leithuk': ('lei-thuk', 'earth-deep'),                   # 1x - deep earth
    'leivuineel': ('lei-vui-neel', 'earth-dust-smooth'),     # 1x - smooth dust earth
    'tumdang': ('tum-dang', 'stumble-different'),            # 1x - different stumble
    'nopnehte': ('nop-neh-te', 'want-weak-PL'),              # 1x - weak wanters
    'kuankhiate': ('kuan-khia-te', 'authority-out-PL'),      # 1x - authorities out
    'minun': ('min-un', 'name-IMP'),                         # 1x - name it!
    
    # Round 221: Jeremiah/Ezekiel hapax vocabulary
    'kaihkhiatna': ('kaih-khiat-na', 'lead-out-NMLZ'),       # 1x Jer 38:11 - letting down
    'kihonthahna': ('ki-hon-thah-na', 'REFL-open-new-NMLZ'),  # 1x Ezek 6:8 - escape
    'kikalhna': ('ki-kalh-na', 'REFL-bar-NMLZ'),             # 1x Jer 51:30 - bars
    'khuaphiatna': ('khua-phiat-na', 'cloud-clear-NMLZ'),    # 1x Ezek 1:4 - brightness
    'khuakongpite': ('khua-kong-pi-te', 'village-gate-great-PL'),  # 1x Jer 51:58 - high gates
    'kisuliam': ('ki-su-liam', 'REFL-cut-joint'),            # 1x Jer 47:5 - cut oneself
    'vukngo': ('vuk-ngo', 'blanket-warm'),                   # 1x - warm blanket
    'anduh': ('an-duh', 'food-soup'),                        # 1x - soup food
    'puanlomte': ('puan-lom-te', 'cloth-friend-PL'),         # 1x - cloth friends
    'zutkhat': ('zut-khat', 'ugly-one'),                     # 1x - one ugly
    'kigawite': ('ki-gawi-te', 'REFL-crooked-PL'),           # 1x - crooked ones
    'zangleite': ('zang-lei-te', 'arm-borrow-PL'),           # 1x - arm borrowers
    'sukhamzan': ('suk-ham-zan', 'push-desire-night'),       # 1x - night desire
    'suktap': ('suk-tap', 'push-weep'),                      # 1x - push weep
    'lakhiasuk': ('la-khia-suk', 'take-out-push'),           # 1x - push take out
    'kisuh': ('ki-suh', 'REFL-count'),                       # 1x - be counted
    'saal': ('saal', 'Saul'),                                # 1x - Saul (variant)
    'nuaiphahin': ('nuai-phah-in', 'under-throw-ERG'),       # 1x - throwing under
    'siktawnte': ('sik-tawn-te', 'bar-stand-PL'),            # 1x Jer 51:30 - bar stands
    'ciak': ('ciak', 'eat'),                                 # 1x - eat (variant)
    'zumlai': ('zum-lai', 'bow-time'),                       # 1x - bow time
    'ngelhngalh': ('ngelh-ngalh', 'smooth~REDUP'),           # 1x - very smooth
    'husamin': ('hu-sam-in', 'follow-call-ERG'),             # 1x - following call
    'tahtansak': ('tah-tan-sak', 'exact-stand-CAUS'),        # 1x - cause stand exact
    'giugiau': ('giu-giau', 'shake~REDUP'),                  # 1x - shaking
    'kenkanzo': ('ken-kan-zo', 'carry-REDUP-finish'),        # 1x - finish carrying
    'lehdokha': ('leh-do-kha', 'return-fight-dry'),          # 1x - return fight
    'delhkek': ('delh-kek', 'throw-reverse'),                # 1x - throw reverse
    'kiciangte': ('ki-ciang-te', 'REFL-become-PL'),          # 1x - become ones
    'dup': ('dup', 'heap'),                                  # 1x - heap
    'silenai': ('si-le-nai', 'die-and-near'),                # 1x - die and near
    'ngenngenkha': ('ngen-ngen-kha', 'beg-REDUP-dry'),        # 1x - begging dry
    'vilsim': ('vil-sim', 'round-think'),                    # 1x - think round
    'nuinui': ('nui~nui', 'laugh~REDUP'),                    # 1x - laughing
    'mam': ('mam', 'mother'),                                # 1x - mother (variant)
    'tatkhatin': ('tat-khat-in', 'each-one-ERG'),            # 1x - each one
    'kangto': ('kang-to', 'burn-reach'),                     # 1x - reach burn
    'kiukiau': ('kiu-kiau', 'cry~REDUP'),                    # 1x - crying
    'leenna': ('leen-na', 'wine-NMLZ'),                      # 1x - wine place
    'paupeeng': ('pau-peeng', 'word-open'),                  # 1x - open word
    'thumletau': ('thum-le-tau', 'three-and-gourd'),         # 1x - three gourds
    'sikpeek': ('sik-peek', 'bar-split'),                    # 1x - split bar
    'ekkeu': ('ek-keu', 'excrement-unmarried'),              # 1x - dung
    'tunsate': ('tun-sa-te', 'arrive-already-PL'),           # 1x - arrived ones
    'tawmcikkhat': ('tawm-cik-khat', 'short-quick-one'),     # 1x - one quick short
    'cikze': ('cik-ze', 'quick-manner'),                     # 1x - quick manner
    'lawnthang': ('lawn-thang', 'throw-rise'),               # 1x - throw rise
    
    # Round 222: Minor Prophets/Daniel hapax vocabulary
    'kisukgawpna': ('ki-suk-gawp-na', 'REFL-push-cover-NMLZ'),  # 1x Hab 1:3 - violence
    'gimtuahna': ('gim-tuah-na', 'trouble-do-NMLZ'),         # 1x Zech 9:1 - burden
    'hehnepnate': ('heh-nep-na-te', 'angry-soft-NMLZ-PL'),   # 1x Zech 10:2 - comforts
    'kidomkaang': ('ki-dom-kaang', 'REFL-stand-straight'),   # 1x Dan 7:4 - stand upright
    'lamnopna': ('lam-nop-na', 'build-want-NMLZ'),           # 1x Hag 1:14 - work
    'leiseekna': ('lei-seek-na', 'earth-seek-NMLZ'),         # 1x Nah 3:14 - brickkiln
    'bakkhat': ('bak-khat', 'bind-one'),                     # 1x - bind one
    'kiphen': ('ki-phen', 'REFL-open'),                      # 1x - be opened
    'sibupin': ('si-bup-in', 'die-fall-ERG'),                # 1x - falling dead
    'daplan': ('da-plan', 'dry-flat'),                       # 1x - flat dry
    'tamzawte': ('tam-zaw-te', 'many-more-PL'),              # 1x - more many
    'gankhawk': ('gan-khawk', 'carry-shake'),                # 1x - shake carry
    'kipaihna': ('ki-paih-na', 'REFL-go-NMLZ'),              # 1x - going
    'heu': ('heu', 'blow'),                                  # 1x - blow (variant)
    'upin': ('up-in', 'believe-ERG'),                        # 1x - believing
    'haibawl': ('hai-bawl', 'pluck-make'),                   # 1x - make pluck
    'sawpkhiat': ('sawp-khiat', 'sweep-out'),                # 1x - sweep out
    'kangcipsak': ('kang-cip-sak', 'burn-deep-CAUS'),        # 1x - cause burn deep
    'linglom': ('ling-lom', 'bell-friend'),                  # 1x - bell friend
    'zulesa': ('zule-sa', 'obey-already'),                   # 1x - already obey
    'koplen': ('kop-len', 'call-play'),                      # 1x - call play
    'kilehsuk': ('ki-leh-suk', 'REFL-return-push'),          # 1x - push return
    'koplenna': ('kop-len-na', 'call-play-NMLZ'),            # 1x - playing
    'miamua': ('mia-mua', 'face-wet'),                       # 1x - wet face
    'sungvumin': ('sung-vum-in', 'inside-heap-ERG'),         # 1x - heaping inside
    'ngenpi': ('ngen-pi', 'beg-great'),                      # 1x - great beg
    'keikai': ('kei-kai', '1SG-lead'),                       # 1x - lead me
    'kimetcip': ('ki-met-cip', 'REFL-squeeze-deep'),         # 1x - squeeze deep
    'suthang': ('su-thang', 'push-rise'),                    # 1x - push rise
    'pumlin': ('pum-lin', 'body-walk'),                      # 1x - walk body
    'pukcipsuk': ('puk-cip-suk', 'fall-deep-push'),          # 1x - push fall deep
    'zaptelsak': ('zap-tel-sak', 'pinch-join-CAUS'),         # 1x - cause join pinch
    'banglai': ('bang-lai', 'what-time'),                    # 1x - what time
    'sinkham': ('sin-kham', 'tree-prevent'),                 # 1x - prevent tree
    'kizapkhiat': ('ki-zap-khiat', 'REFL-pinch-out'),        # 1x - pinch out
    'gunvapite': ('gun-va-pi-te', 'heart-bird-great-PL'),    # 1x - great heart birds
    'khuangin': ('khuang-in', 'drum-ERG'),                   # 1x - drumming
    'saguh': ('sa-guh', 'flesh-basket'),                     # 1x - flesh basket
    'upmawhzah': ('up-mawh-zah', 'believe-sin-EMPH'),        # 1x - truly sin believe
    'kulhhuam': ('kulh-huam', 'wall-guard'),                 # 1x - guard wall
    'meikulh': ('mei-kulh', 'fire-wall'),                    # 1x - fire wall
    'lehsuh': ('leh-suh', 'return-count'),                   # 1x - count return
    'kisiakmang': ('ki-siak-mang', 'REFL-throw-chief'),      # 1x - thrown chief
    'siinkik': ('siin-kik', 'alive-ITER'),                   # 1x - alive again
    'huihleeng': ('huih-leeng', 'wind-wing'),                # 1x - wind wing
    'teeklua': ('teek-lua', 'sink-exceed'),                  # 1x - exceed sink
    'phezaizai': ('phe-zai-zai', 'spread-REDUP~REDUP'),      # 1x - spreading
    'kigizawng': ('ki-gi-zawng', 'REFL-squeeze-search'),     # 1x - search squeeze
    'zulim': ('zul-im', 'follow-house'),                     # 1x - follow house
    'tupi': ('tu-pi', 'now-great'),                          # 1x - great now
    
    # Round 223: John/Mark/NT hapax vocabulary
    'kithuapna': ('ki-thuap-na', 'REFL-stack-NMLZ'),         # 1x Mark 13:2 - stacking
    'lungnopnate': ('lung-nop-na-te', 'heart-want-NMLZ-PL'),  # 1x John 14:27 - peace
    'nungzuihpihte': ('nung-zuih-pih-te', 'back-follow-with-PL'),  # 1x John 11:16 - fellowdisciples
    'kikilhna': ('ki-kilh-na', 'REFL-nail-NMLZ'),            # 1x John 20:25 - print of nails
    'kikalhnelh': ('ki-kalh-nelh', 'REFL-bar-press'),        # 1x John 20:19 - shut
    'huhnop': ('huh-nop', 'blow-want'),                      # 1x - want blow
    'peuhpeuhun': ('peuh-peuh-un', 'each-REDUP-IMP'),        # 1x - each each!
    'nangnuam': ('nang-nuam', '2SG-pleasant'),               # 1x - you pleasant
    'masawlin': ('ma-sawl-in', 'EMPH-send-ERG'),             # 1x - truly sending
    'tunkuan': ('tun-kuan', 'arrive-authority'),             # 1x - authority arrive
    'lunghihmawhin': ('lung-hih-mawh-in', 'heart-fear-sin-ERG'),  # 1x - fearing heart
    'buhhum': ('buh-hum', 'rice-cover'),                     # 1x - cover rice
    'phawkvat': ('phawk-vat', 'remember-quick'),             # 1x - remember quick
    'thonga': ('thong-a', 'prison-LOC'),                     # 1x - in prison
    'hanphual': ('han-phual', 'CAUS-nest'),                  # 1x - cause nest
    'tumpah': ('tum-pah', 'stumble-strike'),                 # 1x - strike stumble
    'dinkhawl': ('din-khawl', 'stand-rest'),                 # 1x - rest stand
    'tusawng': ('tu-sawng', 'now-vessel'),                   # 1x - now vessel
    'haankeu': ('haan-keu', 'goose-unmarried'),              # 1x - young goose
    'khuagei': ('khua-gei', 'village-edge'),                 # 1x - village edge
    'tuipihte': ('tui-pih-te', 'water-with-PL'),             # 1x - water ones
    'ipbawl': ('ip-bawl', 'blow-make'),                      # 1x - make blow
    'thambelpi': ('tham-bel-pi', 'new-leave-great'),         # 1x - great new leave
    'thambelpite': ('tham-bel-pi-te', 'new-leave-great-PL'),  # 1x - great new leaves
    'sitsetin': ('sit-set-in', 'wipe-REDUP-ERG'),            # 1x - wiping
    'khauteep': ('khau-teep', 'rope-tie'),                   # 1x - tie rope
    'khuapihte': ('khua-pih-te', 'village-with-PL'),         # 1x - village ones
    'phengphang': ('pheng-phang', 'plank~REDUP'),            # 1x - planks
    'tuitungah': ('tui-tung-ah', 'water-upon-LOC'),          # 1x - upon water
    'nuailam': ('nuai-lam', 'under-direction'),              # 1x - under direction
    'kobawlin': ('ko-bawl-in', 'cry-make-CVB'),              # 1x - making cry
    'tuukong': ('tuu-kong', 'gourd-hole'),                   # 1x - gourd hole
    'kicialtawm': ('ki-cial-tawm', 'REFL-scatter-short'),    # 1x - scatter short
    'mankim': ('man-kim', 'price-complete'),                 # 1x - complete price
    'kipatma': ('ki-pat-ma', 'REFL-attach-before'),          # 1x - attach before
    'nuhkhit': ('nuh-khit', 'push-finish'),                  # 1x - finish push
    'mawkgen': ('mawk-gen', 'wet-say'),                      # 1x - say wet
    'suahhun': ('suah-hun', 'become-time'),                  # 1x - time become
    'ngenpah': ('ngen-pah', 'beg-strike'),                   # 1x - strike beg
    'lalcin': ('lal-cin', 'king-still'),                     # 1x - still king
    'khukawm': ('khu-kawm', 'knee-around'),                  # 1x - around knee
    'vaikhakte': ('vai-khak-te', 'chaff-firm-PL'),           # 1x - firm chaff
    'kaizo': ('kai-zo', 'lead-finish'),                      # 1x - finish lead
    'buatbuatin': ('buat-buat-in', 'prepare-REDUP-ERG'),     # 1x - preparing
    'kithehkek': ('ki-theh-kek', 'REFL-place-reverse'),      # 1x - reverse place
    'khauhpah': ('khauh-pah', 'strong-strike'),              # 1x - strike strong
    'diangkawmin': ('diang-kawm-in', 'throne-around-ERG'),   # 1x - around throne
    'manzaw': ('man-zaw', 'price-more'),                     # 1x - more price
    
    # Round 224: Epistles hapax vocabulary
    'kigensiatnate': ('ki-gen-siat-na-te', 'REFL-say-evil-NMLZ-PL'),  # 1x 1Pet 2:1 - evil speakings
    'kitotlawhna': ('ki-tot-lawh-na', 'REFL-contend-earn-NMLZ'),  # 1x Titus 3:9 - strivings
    'kiselnate': ('ki-sel-na-te', 'REFL-dispute-NMLZ-PL'),  # 1x 2Tim 2:16 - babblings
    'deihluatnate': ('deih-luat-na-te', 'want-exceed-NMLZ-PL'),  # 1x 2Pet 1:4 - lusts
    'kinialnate': ('ki-nial-na-te', 'REFL-argue-NMLZ-PL'),  # 1x 2Tim 2:23 - questions
    'lahkholhna': ('lah-kholh-na', 'represent-INTENS-NMLZ'),  # 1x Heb 10:1 - shadow
    'thangsakte': ('thang-sak-te', 'news-CAUS-PL'),          # 1x - news makers
    'tapkual': ('tap-kual', 'weep-embrace'),                 # 1x - weep embrace
    'hangsankhak': ('hang-san-khak', 'CAUS-separate-firm'),  # 1x - firmly separate
    'khauhte': ('khauh-te', 'strong-PL'),                    # 1x - strong ones
    'nakzat': ('nak-zat', 'heavy-use'),                      # 1x - use heavy
    'tangzaizaw': ('tang-zai-zaw', 'rise-stand-more'),       # 1x - rise more
    'lehngaihsut': ('leh-ngaih-sut', 'return-think-pull'),   # 1x - think return
    'kitheite': ('ki-thei-te', 'REFL-know-PL'),              # 1x - known ones
    'guptuam': ('gup-tuam', 'war-weapon'),                   # 1x - war weapon
    'haunuam': ('hau-nuam', 'rich-pleasant'),                # 1x - pleasant rich
    'puathamteng': ('pua-tham-teng', 'carry-new-all'),       # 1x - all new carry
    'khiankhianin': ('khian-khian-in', 'grow-REDUP-ERG'),    # 1x - growing
    'kilehbulh': ('ki-leh-bulh', 'REFL-return-begin'),       # 1x - begin return
    'khuahek': ('khua-hek', 'cloud-blow'),                   # 1x - cloud blow
    'kiphamawhte': ('ki-pha-mawh-te', 'REFL-good-sin-PL'),   # 1x - prideful ones
    'kipumpiak': ('ki-pum-piak', 'REFL-body-give'),          # 1x - give body
    'thangba': ('thang-ba', 'news-want'),                    # 1x - want news
    'luisuak': ('lui-suak', 'river-become'),                 # 1x - become river
    'kikhelkhel': ('ki-khel-khel', 'REFL-err~REDUP'),        # 1x - erring repeatedly
    'khahsuahkhak': ('khah-suah-khak', 'carry-become-firm'),  # 1x - firmly carry
    'khauhsakkhak': ('khauh-sak-khak', 'strong-CAUS-firm'),  # 1x - firmly strengthen
    'thanop': ('tha-nop', 'strength-want'),                  # 1x - want strength
    'lianzawte': ('lian-zaw-te', 'great-more-PL'),           # 1x - greater ones
    'kideina': ('ki-dei-na', 'REFL-want-NMLZ'),              # 1x - self-desire
    'khawmnate': ('khawm-na-te', 'join-NMLZ-PL'),            # 1x - joinings
    'hehsakte': ('heh-sak-te', 'angry-CAUS-PL'),             # 1x - anger causers
    'kimvel': ('kim-vel', 'complete-around'),                # 1x - around complete
    'hucip': ('hu-cip', 'follow-deep'),                      # 1x - follow deep
    'phing': ('phing', 'fart'),                              # 1x - fart/flatulence
    'nuangnuang': ('nuang~nuang', 'soft~REDUP'),             # 1x - very soft
    'luangluangin': ('luang-luang-in', 'flow-REDUP-ERG'),    # 1x - flowing
    'thuakngap': ('thuak-ngap', 'suffer-endure'),            # 1x - endure suffering
    'kithehna': ('ki-theh-na', 'REFL-place-NMLZ'),           # 1x - placing
    'kidopzawh': ('ki-dop-zawh', 'REFL-attack-finish'),      # 1x - finish attack
    'gukhal': ('guk-hal', 'bow-burn'),                       # 1x - burn bow
    'theipum': ('thei-pum', 'fruit-body'),                   # 1x - fruit body
    'dawivai': ('dawi-vai', 'medicine-chaff'),               # 1x - medicine chaff
    'pumsung': ('pum-sung', 'body-inside'),                  # 1x - inside body
    'muattumta': ('muat-tum-ta', 'rot-stumble-child'),       # 1x - rotten child
    'kekseuna': ('kek-seu-na', 'reverse-search-NMLZ'),       # 1x - reverse search
    'phitphet': ('phit-phet', 'split~REDUP'),                # 1x - splitting
    'suakcilte': ('suak-cil-te', 'become-turn-PL'),          # 1x - becoming ones
    'uangtatna': ('uang-tat-na', 'pour-each-NMLZ'),          # 1x - pouring each
    'kosia': ('ko-sia', 'cry-evil'),                         # 1x - evil cry
    
    # Round 225: Proverbs/Ecclesiastes/Song hapax vocabulary
    'kigamtatnate': ('ki-gam-tat-na-te', 'REFL-land-each-NMLZ-PL'),  # 1x Eccl 4:1 - oppressions
    'kisamsiatna': ('ki-sam-siat-na', 'REFL-call-evil-NMLZ'),  # 1x Prov 26:2 - curse
    'haihuaina': ('hai-huai-na', 'confuse-ABIL-NMLZ'),       # 1x Eccl 7:25 - madness
    'kaihzawhna': ('kaih-zawh-na', 'lead-finish-NMLZ'),      # 1x Prov 16:7 - peace
    'kawkbaanna': ('kawk-baan-na', 'touch-scratch-NMLZ'),    # 1x Song 4:7 - spot
    'lehbawlna': ('leh-bawl-na', 'return-make-NMLZ'),        # 2x - deceit
    'khuangtumte': ('khuang-tum-te', 'drum-stumble-PL'),     # 1x - drummers
    'khaknelhsak': ('khak-nelh-sak', 'firm-press-CAUS'),     # 1x - cause press firm
    'kawngte': ('kawng-te', 'gate-PL'),                      # 1x - gates
    'luiliante': ('lui-lian-te', 'river-great-PL'),          # 1x - great rivers
    'muanlesuan': ('muan-le-suan', 'trust-and-plant'),       # 1x - trust and plant
    'kanglum': ('kang-lum', 'burn-heap'),                    # 1x - heap burn
    'khuangno': ('khuang-no', 'drum-young'),                 # 1x - young drum
    'kawlgit': ('kawl-git', 'call-squeeze'),                 # 1x - squeeze call
    'luakha': ('luak-ha', 'vomit-dry'),                      # 1x - dry vomit
    'vuasak': ('vua-sak', 'bear.fruit-CAUS'),                # 1x - cause fruit
    'saalte': ('saal-te', 'Saul-PL'),                        # 1x - Sauls
    'ciimsak': ('ciim-sak', 'shut-CAUS'),                    # 1x - cause shut
    'muansuam': ('muan-suam', 'trust-throw'),                # 1x - throw trust
    'suihkhakte': ('suih-khak-te', 'adorn-firm-PL'),         # 1x - firmly adorned
    'khenglahkha': ('kheng-lah-kha', 'lean-take-dry'),       # 1x - lean take
    'dian': ('dian', 'throne'),                              # 1x - throne (variant)
    'iptheite': ('ip-thei-te', 'blow-know-PL'),              # 1x - knowing blowers
    'hoihbekin': ('hoih-bek-in', 'good-only-ERG'),           # 1x - only good
    'gensiasiate': ('gen-sia-sia-te', 'say-evil-REDUP-PL'),  # 1x - evil speakers
    'kimudahsak': ('ki-mu-dah-sak', 'REFL-see-find-CAUS'),   # 1x - cause find
    'teekte': ('teek-te', 'sink-PL'),                        # 1x - sinking ones
    'kehsakkhak': ('keh-sak-khak', 'kick-CAUS-firm'),        # 1x - firmly kick
    'khahsuahsuah': ('khah-suah-suah', 'carry-become~REDUP'),  # 1x - carrying
    'kituakte': ('ki-tuak-te', 'REFL-meet-PL'),              # 1x - met ones
    'nawtgawpin': ('nawt-gawp-in', 'drive-cover-ERG'),       # 1x - driving cover
    "humpi'n": ("hum-pi-'n", 'cover-great-ERG'),             # 1x - greatly covering
    'kiattheihna': ('kiat-theih-na', 'break-know-NMLZ'),     # 1x - breaking know
    'seuhseuh': ('seuh~seuh', 'search~REDUP'),               # 1x - searching
    'khutzepin': ('khut-zep-in', 'hand-pinch-ERG'),          # 1x - pinching hand
    'kawmhek': ('kawm-hek', 'around-blow'),                  # 1x - blow around
    'kaihsak': ('kaih-sak', 'lead-CAUS'),                    # 1x - cause lead
    'lualiang': ('lua-liang', 'exceed-bright'),              # 1x - exceed bright
    'siahuaite': ('sia-huai-te', 'evil-ABIL-PL'),            # 1x - evil ones
    'zakiat': ('za-kiat', 'hundred-break'),                  # 1x - hundred break
    'zakiatna': ('za-kiat-na', 'hundred-break-NMLZ'),        # 1x - hundred breaking
    'penpente': ('pen-pen-te', 'each-REDUP-PL'),             # 1x - each ones
    'singtenin': ('sing-ten-in', 'tree-above-ERG'),          # 1x - above tree
    'thalawp': ('tha-lawp', 'strength-wrap'),                # 1x - wrap strength
    'kawisate': ('kawi-sa-te', 'crooked-already-PL'),        # 1x - crooked ones
    'hahkatna': ('hah-kat-na', 'tired-cut-NMLZ'),            # 1x - cutting tiredness
    
    # Round 226: Mixed hapax vocabulary
    'baina': ('bai-na', 'owe-NMLZ'),                         # 1x 2Cor 4:9 - persecuted (debt)
    'bangsakkikte': ('bang-sak-kik-te', 'like-CAUS-again-PL'),  # 1x Isa 58:12 - restorer
    'bawhhuan': ('bawh-huan', 'cry-garden'),                 # 1x Acts 7:57 - cried out
    'belawi': ('bel-awi', 'leave-winnow'),                   # 1x Ezek 4:9 - fitches (grain)
    'betkhiatsak': ('bet-khiat-sak', 'shoot-out-CAUS'),      # 1x Ezek 39:3 - cause arrows fall
    'betkhiatsakin': ('bet-khiat-sak-in', 'shoot-out-CAUS-CVB'),  # 1x Ezek 39:3 - causing arrows fall
    'bing': ('bing', 'uncircumcised'),                       # 1x Jer 6:10 - uncircumcised ear
    'buhphual': ('buh-phual', 'rice-torch'),                 # 1x Zech 12:6 - torch in sheaf
    'dahlekah': ('dah-le-kah', 'dry-and-lamentations'),      # 1x Ezek 2:10 - lamentations
    'daihawh': ('dai-hawh', 'dawn-sabbath'),                 # 1x Matt 28:1 - end of sabbath
    'dawhkhiat': ('dawh-khiat', 'snatch-out'),               # 1x Jude 1:23 - pulling out of fire
    'deh': ('deh', 'scorpion.sting'),                        # 1x Rev 9:5 - scorpion striketh
    'dehthei': ('deh-thei', 'sting-can'),                    # 1x Rev 9:10 - stings in tails
    'denpaih': ('den-paih', 'stand-beside'),                 # 1x Dan 2:45 - hereafter
    'dongkhak': ('dong-khak', 'way-block'),                  # 1x Isa 57:14 - stumblingblock
    'dongnuam': ('dong-nuam', 'way-pleasant'),               # 1x Jer 12:1 - way prosper
    'dongtelin': ('dong-tel-in', 'way-patient-ERG'),         # 1x Rev 2:2 - patience
    'engdup': ('eng-dup', 'light-cover'),                    # 1x Jer 10:9 - blue and purple
    'gahkhak': ('gah-khak', 'fruit-block'),                  # 1x Mark 11:13 - time of figs
    'gahphat': ('gah-phat', 'fruit-destroy'),                # 1x Jer 11:19 - destroy tree with fruit
    'gamlelei': ('gam-lelei', 'land-tremble'),               # 1x Jer 8:16 - land trembled
    'gawsem': ('gaw-sem', 'sound-dulcimer'),                 # 1x Dan 3:15 - dulcimer (instrument)
    'gawsemte': ('gaw-sem-te', 'sound-dulcimer-PL'),         # 1x Dan 3:5 - dulcimers
    'geihualte': ('gei-hual-te', 'settle-corners-PL'),       # 1x Ezek 43:20 - corners of settle
    'guaktangun': ('guak-tang-un', 'naked-rise-IMP'),        # 1x Lam 4:21 - make thyself naked
    'gualnuamte': ('gual-nuam-te', 'dance-pleasant-PL'),     # 1x Jer 31:4 - dances of merry
    'gualtut': ('gual-tut', 'group-fifty'),                  # 1x Mark 6:40 - by fifties
    'guipi': ('gui-pi', 'bone-big'),                         # 1x Ezek 37:11 - these bones
    'guktaknate': ('guk-tak-na-te', 'steal-true-NMLZ-PL'),   # 1x Rev 9:21 - thefts
    'gumthuak': ('gum-thuak', 'slave-endure'),               # 1x 1Cor 4:12 - we suffer it
    'gutui': ('gu-tui', 'gall-water'),                       # 1x Jer 9:15 - water of gall
    'haitatnasate': ('hai-tat-na-sa-te', 'whore-cut-NMLZ-already-PL'),  # 1x Ezek 6:9 - whorish heart
    'hallupna': ('hal-lup-na', 'burn-bury-NMLZ'),            # 1x Jer 7:31 - burn in fire
    'harpte': ('harp-te', 'harp-PL'),                        # 1x Rev 15:2 - harps (loanword)
    'hauhnopna': ('hauh-nop-na', 'desire-deceive-NMLZ'),     # 1x Mark 4:19 - deceitfulness
    'hehhuai': ('heh-huai', 'anger-stumble'),                # 1x 1Cor 1:23 - stumblingblock
    'hehnemzaw': ('heh-nem-zaw', 'anger-comfort-more'),      # 1x 2Cor 2:7 - comfort more
    'heksim': ('hek-sim', 'accuse-slander'),                 # 1x Dan 3:8 - accused the Jews
    'hekteng': ('hek-teng', 'accuse-fix'),                   # 1x Dan 6:24 - had accused
    'heuhkhiatsak': ('heuh-khiat-sak', 'scatter-out-CAUS'),  # 1x Jer 5:10 - take away battlements
    'heuhsiang': ('heuh-siang', 'scatter-shake'),            # 1x Dan 4:14 - shake off leaves
    'hilhel': ('hilh-el', 'teach-COMPL'),                    # 1x Ezek 42:6 - straitened
    'hilhial': ('hilh-ial', 'teach-spread'),                 # 1x Ps 73:4 - no bands in death
    'hoihzawknate': ('hoih-zawk-na-te', 'good-more-NMLZ-PL'),  # 1x Rev 2:19 - last more than first
    'hotnop': ('hot-nop', 'trust-want'),                     # 1x Matt 27:43 - he trusted
    'huhsawn': ('huh-sawn', 'comfort-console'),              # 1x 2Cor 1:4 - comforteth us
    
    # Round 227: Mixed hapax vocabulary
    'gamtangsakkik': ('gam-tang-sak-kik', 'land-rise-CAUS-again'),  # 1x Ezek 36:12 - inherit again
    'henhante': ('hen-han-te', 'handful-do-PL'),             # 1x Isa 60:8 - fly as doves
    'huhtheite': ('huh-thei-te', 'help-can-PL'),             # 1x 1Cor 12:28 - helps (gifts)
    'hukte': ('huk-te', 'snuff-PL'),                         # 1x Jer 2:24 - snuffeth up wind
    'hullum': ('hul-lum', 'fire-flame'),                     # 1x Dan 3:22 - flame of fire
    'hupkang': ('hup-kang', 'swallow-mouth'),                # 1x Rev 12:16 - swallowed up flood
    'husam': ('hu-sam', 'guard-murderer'),                   # 1x Jer 4:31 - murderers
    'inngualte': ('in-ngual-te', 'house-story-PL'),          # 1x Ezek 42:6 - three stories
    'keutumpah': ('keu-tum-pah', 'scratch-sun-strike'),      # 1x Mark 4:6 - sun scorched
    'khantheihna': ('khan-theih-na', 'grow-ABIL-NMLZ'),       # 1x Mark 4:27 - grow he knoweth not
    'khatkhatin': ('khat-khat-in', 'one-one-ERG'),           # 1x 1Cor 14:31 - one by one
    'khatpeuhin': ('khat-peuh-in', 'one-any-ERG'),           # 1x Matt 24:50 - in hour not aware
    'khauhtat': ('khauh-tat', 'grief-cut'),                  # 1x 2Cor 2:5 - caused grief
    'khausante': ('khau-san-te', 'cloth-silk-PL'),           # 1x Rev 18:12 - silk and scarlet
    'khawngte': ('khawng-te', 'cup-PL'),                     # 1x Mark 7:4 - washing of cups
    'khengsuak': ('kheng-suak', 'row-emerge'),               # 1x Mark 6:48 - toiling in rowing
    'khengta': ('kheng-ta', 'spring-already'),               # 1x Isa 42:9 - spring forth
    'khephung': ('khe-phung', 'foot-group'),                 # 1x Rev 3:9 - worship at feet
    'khephungah': ('khe-phung-ah', 'foot-group-LOC'),        # 1x Mark 5:33 - fell at feet
    'khipkhep': ('khip-khep', 'wind-calm'),                  # 1x Mark 4:39 - be still calm
    'khuakehte': ('khua-keh-te', 'town-cross-PL'),           # 1x Mark 6:56 - villages cities
    'khuangta': ('khuang-ta', 'cock-already'),               # 1x Matt 26:74 - cock crew
    'khuangte': ('khuang-te', 'tabret-PL'),                  # 1x Jer 31:4 - tabrets
    'khuaphawkin': ('khua-phawk-in', 'town-naked-ERG'),      # 1x Rev 16:15 - walk naked
    'khulte': ('khul-te', 'take.up-PL'),                     # 1x Dan 3:22 - took up
    'khutdawhin': ('khut-dawh-in', 'hand-beg-ERG'),          # 1x Mark 10:46 - begging
    'kidimna': ('ki-dim-na', 'REFL-fill-NMLZ'),              # 1x Ezek 43:5 - filled house
    'kigeelna': ('ki-geel-na', 'REFL-go.in-NMLZ'),           # 1x Ezek 43:11 - comings in
    'kigelnate': ('ki-gel-na-te', 'REFL-go.in-NMLZ-PL'),     # 1x Ezek 43:11 - goings
    'kigengenna': ('ki-gen-gen-na', 'REFL-say-REDUP-NMLZ'),  # 1x Mark 6:14 - name spread
    'kihaltumna': ('ki-hal-tum-na', 'REFL-burn-all-NMLZ'),   # 1x 1Cor 13:3 - be burned
    'kihtalua': ('kih-tal-ua', 'abhor-INTNS-very'),          # 1x Matt 28:4 - did shake (phonotactic fix)
    'kihutawm': ('ki-hu-tawm', 'REFL-guard-finish'),         # 1x Ezek 38:11 - at rest
    'kikhamvalte': ('ki-kham-val-te', 'REFL-prevent-left-PL'),  # 1x John 6:12 - fragments remain
    'kikopin': ('ki-kop-in', 'REFL-gather-CVB'),             # 1x Rom 15:17 - glory in
    'kilamdan': ('ki-lam-dan', 'REFL-way-different'),        # 1x 2Pet 3:8 - thousand years
    'kimangngilhkha': ('ki-mang-ngilh-kha', 'REFL-profit-forget-still'),  # 1x Ezek 39:14 - continual
    'kimudahin': ('ki-mu-dah-in', 'REFL-see-offend-CVB'),    # 1x Matt 24:10 - be offended
    'kimuhnop': ('ki-muh-nop', 'REFL-see-want'),             # 1x Rom 15:23 - desire to come
    'kinapna': ('ki-nap-na', 'REFL-kiss-NMLZ'),              # 1x 1Cor 16:20 - holy kiss
    
    # Round 228: Final hapax vocabulary push
    'ipcipte': ('ip-cip-te', 'hide-squeeze-PL'),             # 1x 1Cor 14:25 - secrets made manifest
    'kanghul': ('ka-nghul', '1SG-smell.of.fire'),            # 1x Dan 3:27 - smell of fire
    'kangkha': ('ka-ngkha', '1SG-heat'),                     # 1x Rev 7:16 - nor any heat
    'kawihei': ('ka-wih-ei', '1SG-difficult-EXCL'),          # 1x 2Pet 3:16 - hard to be understood
    'kinotsuk': ('ki-not-suk', 'REFL-push-push'),            # 1x 1Cor 4:11 - buffeted
    'kinotto': ('ki-not-to', 'REFL-push-also'),              # 1x 1Cor 4:11 - have no dwellingplace
    'kipelhzaw': ('ki-pelh-zaw', 'REFL-spare-more'),         # 1x 1Cor 7:28 - I spare you
    'kiphunsanna': ('ki-phun-san-na', 'REFL-kind-stand-NMLZ'),  # 1x Acts 6:1 - murmuring
    'kipiakhiate': ('ki-piak-hia-te', 'REFL-give-all-PL'),   # 1x Ezek 44:29 - dedicated things
    'kisehsate': ('ki-seh-sa-te', 'REFL-write-already-PL'),  # 1x Rev 13:8 - written in book
    'kisiamaisate': ('ki-siam-aisa-te', 'REFL-repair-already-PL'),  # 1x Isa 61:4 - repair waste cities
    'kitamnen': ('ki-tam-nen', 'REFL-many-become'),          # 1x Dan 2:35 - became great mountain
    'kiteelte': ('ki-teel-te', 'REFL-choose-PL'),            # 1x Dan 1:6 - among these were
    'kithahlupna': ('ki-thah-lup-na', 'REFL-tear-flow-NMLZ'),  # 1x Jer 9:1 - fountain of tears
    'kithehzak': ('ki-theh-zak', 'REFL-throw-scatter'),      # 1x 1Cor 10:5 - overthrown
    'kizapzap': ('ki-zap-zap', 'REFL-burn~REDUP'),           # 1x Jer 6:29 - bellows burned
    'kobawlna': ('ko-bawl-na', '1PL.EXCL-make-NMLZ'),        # 1x Ezek 36:15 - cause to fall
    'kongkaw': ('kong-kaw', '1SG→3-tear'),                   # 1x Mark 1:26 - torn him
    'kongkawcip': ('kong-kaw-cip', '1SG→3-tear-squeeze'),    # 1x Mark 9:18 - teareth and foameth
    'kongkawsak': ('kong-kaw-sak', '1SG→3-tear-CAUS'),       # 1x Mark 9:20 - spirit tare him
    'kongkawtsak': ('kong-kawt-sak', '1SG→3-tear-CAUS'),     # 1x Mark 9:26 - rent him sore (kawt variant)
    'kongkhuamte': ('kong-khuam-te', '1SG→3-corner-PL'),     # 1x Ezek 45:19 - corners of settle
    'konglekong': ('kong-le-kong', '1SG→3-and-1SG→3'),       # 1x Ezek 40:27 - gate to gate
    'kongvangneute': ('kong-vang-neu-te', '1SG→3-space-small-PL'),  # 1x Ezek 41:16 - narrow windows
    'kuanlamin': ('kuan-lam-in', 'enter-way-ERG'),           # 1x Ezek 46:8 - go in by way
    'kulzaw': ('kul-zaw', 'lack-more'),                      # 1x 1Cor 12:24 - part which lacked
    'kumi': ('kumi', 'arise'),                               # 1x Mark 5:41 - Talitha cumi (Aramaic)
    'laigelhnate': ('lai-gelh-na-te', 'writing-carve-NMLZ-PL'),  # 1x Rom 16:26 - scriptures
    'laipek': ('lai-pek', 'writing-wash'),                   # 1x Mark 7:5 - unwashen hands
    'lamval': ('lam-val', 'way-left.over'),                  # 1x Mark 12:44 - her want
    'lawngte': ('lawng-te', 'look-PL'),                      # 1x Mark 5:32 - looked round
    'lawnkhit': ('lawn-khit', 'look-recover'),               # 1x Mark 5:29 - healed of plague
    'leenkawmin': ('leen-kawm-in', 'fly-middle-ERG'),        # 1x Rev 8:13 - flying through midst
    'lehbawlnate': ('leh-bawl-na-te', 'again-make-NMLZ-PL'), # 1x Ezek 39:26 - trespasses
    'lehheknate': ('leh-hek-na-te', 'again-accuse-NMLZ-PL'), # 1x Ezek 37:23 - transgressions
    'lehpiak': ('leh-piak', 'again-give'),                   # 1x 1Cor 4:12 - being reviled we bless
    'lehtatte': ('leh-tat-te', 'again-cut-PL'),              # 1x Rev 21:8 - liars
    'leitawm': ('lei-tawm', 'buy-enough'),                   # 1x Matt 25:9 - enough for us
    'leivuithem': ('lei-vui-them', 'buy-dust-dirt'),         # 1x 1Cor 4:13 - filth of world
    'letmatthuhna': ('let-mat-thuh-na', 'turn-eye-point-NMLZ'),  # 1x Jer 22:24 - signet ring
    'liahkhak': ('liah-khak', 'shadow-block'),               # 1x Acts 5:15 - shadow overshadow
    'lialuanate': ('lia-lua-na-te', 'hope-too.much-NMLZ-PL'),  # 1x Jer 3:23 - vain salvation
    'liamlawh': ('liam-lawh', 'burden-self'),                # 1x Zech 12:3 - burden themselves
    'lohongte': ('lo-hong-te', 'field-keep-PL'),             # 1x Jer 4:17 - keepers of field
    'luguh': ('lu-guh', 'head-crown'),                       # 1x Jer 2:16 - crown of head
    'luisate': ('lui-sa-te', 'tear-already-PL'),             # 1x Rev 21:4 - wipe away tears
    'lungduaizo': ('lung-duai-zo', 'heart-loathe-finish'),   # 1x Zech 11:8 - soul lothed
    'lungso': ('lung-so', 'heart-hot'),                      # 1x Ps 6:1 - hot displeasure
    'lungsosa': ('lung-so-sa', 'heart-hot-already'),         # 1x Ps 38:1 - hot displeasure
    
    # Round 229: Remaining hapax vocabulary
    'mapiak': ('ma-piak', 'that-give'),                      # 1x 2Cor 1:22 - given earnest
    'mawkkheel': ('mawk-kheel', 'vain-yea'),                 # 1x 2Cor 1:17 - yea yea nay nay
    'mawkpau': ('mawk-pau', 'vain-say'),                     # 1x Ezek 6:10 - not said in vain
    'mawktai': ('mawk-tai', 'vain-run'),                     # 1x 1Cor 9:26 - run not uncertainly
    'mawktuptup': ('mawk-tup-tup', 'vain-beat~REDUP'),       # 1x 1Cor 9:26 - beateth the air
    'mehtui': ('meh-tui', 'broth-water'),                    # 1x Isa 65:4 - broth of abominations
    'meikat': ('mei-kat', 'fire-burn'),                      # 1x 1Cor 3:15 - work burned
    'melsia': ('mel-sia', 'form-decay'),                     # 1x 1Cor 15:43 - sown in dishonour
    'mengme': ('meng-me', 'dream-slumber'),                  # 1x Prov 6:10 - a little slumber
    'mih': ('mih', 'maimed'),                                # 1x Mark 9:43 - enter life maimed
    'misuam': ('mi-suam', 'person-robber'),                  # 1x Jer 7:11 - den of robbers
    'motpau': ('mot-pau', 'self-speak'),                     # 1x Isa 58:13 - speaking own words
    'muak': ('mu-ak', 'see.I-return'),                       # 1x Dan 4:36 - reason returned
    'muhkhiatnate': ('muh-khiat-na-te', 'see-out-NMLZ-PL'),  # 1x Rev 2:2 - tried them
    'mutkhak': ('mut-khak', 'wind-hold'),                    # 1x Rev 7:1 - holding the winds
    'nektawmzon': ('nek-tawm-zon', 'eat-finish-area'),       # 1x 1Cor 9:6 - forbear working
    'neuneute': ('neu-neu-te', 'small-REDUP-PL'),            # 1x 1Cor 6:3 - things of this life
    'ngakkawmun': ('ngak-kawm-un', 'wait-with-IMP'),         # 1x Jude 1:21 - looking for mercy
    'ngeingeite': ('ngei-ngei-te', 'true-REDUP-PL'),         # 1x 1Cor 10:13 - God is faithful
    'ngentang': ('ngen-tang', 'knowledge-rise'),             # 1x Dan 1:4 - understanding science
    'ngotgawp': ('ngot-gawp', 'dig~REDUP'),                    # 1x Jer 13:7 - digged and took
    'nopcitna': ('nop-cit-na', 'want-desire-NMLZ'),          # 1x Rev 18:14 - soul lusted after
    'nuaisiahna': ('nuai-siah-na', 'oppress-decay-NMLZ'),    # 1x Jer 22:17 - oppression
    'paiphei': ('pai-phei', 'go-enter'),                     # 1x Ezek 41:6 - entered into wall
    'pangtatte': ('pang-tat-te', 'help-cut-PL'),             # 1x Isa 57:3 - sons of sorceress
    'patauhhuai': ('pa-tauh-huai', 'father-wonder-stumble'), # 1x Jer 5:30 - wonderful horrible
    'pataulua': ('pa-tau-lua', 'father-dream-too.much'),     # 1x Dan 2:1 - dreamed dreams
    'pawnlak': ('pawn-lak', 'vineyard-portion'),             # 1x Jer 12:10 - destroyed vineyard
    'penteng': ('pen-teng', 'thing-fixed'),                  # 1x Ezek 44:30 - every oblation
    'phalvaktung': ('phal-vak-tung', 'allow-bright-tall'),   # 1x Isa 58:8 - light break forth
    'phawkpah': ('phawk-pah', 'touch-exactly'),              # 1x Mark 5:30 - who touched
    'phen': ('phen', 'seed'),                                # 1x Isa 57:3 - seed of adulterer
    'phialun': ('phia-lun', 'gather-together'),              # 1x Acts 13:44 - city came together
    'phokeu': ('pho-keu', 'spread-net'),                     # 1x Ezek 47:10 - spread forth nets
    'phunkhak': ('phun-khak', 'kind-blame'),                 # 1x 2Cor 8:20 - no man blame us
    'pikhau': ('pi-khau', 'big-brass'),                      # 1x Ezek 40:3 - appearance of brass
    'piteek': ('pi-teek', 'big-pour'),                       # 1x Jer 6:11 - pour it out
    'puansawpte': ('puan-sawp-te', 'cloth-white-PL'),        # 1x Mark 9:3 - white as snow
    'puanvom': ('puan-vom', 'cloth-black'),                  # 1x Rev 6:12 - black as sackcloth
    'pukpah': ('puk-pah', 'root-exactly'),                   # 1x Mark 4:17 - no root
    'puksukpah': ('puk-suk-pah', 'fall-down-exactly'),       # 1x Acts 5:5 - fell down
    'pumbukah': ('pum-buk-ah', 'body-furnace-LOC'),          # 1x Rev 1:15 - burned in furnace
    'pumguakin': ('pum-guak-in', 'body-naked-ERG'),          # 1x Rev 17:16 - make her naked
    'sabit': ('sabit', 'pearl.gate'),                        # 1x Rev 21:21 - gate of one pearl
    'sagawh': ('sa-gawh', 'flesh-odour'),                    # 1x Dan 2:46 - sweet odours
    'sahang': ('sa-hang', 'flesh-beast'),                    # 1x 1Cor 15:32 - fought with beasts
    'saihate': ('sai-ha-te', 'ivory-vessel-PL'),             # 1x Rev 18:12 - vessels of ivory
    'sandup': ('san-dup', 'gold-cover'),                     # 1x Jer 10:9 - gold from Uphaz
    'sawlpangte': ('sawl-pang-te', 'send-branch-PL'),        # 1x Mark 11:8 - cut down branches
    'sawpsiangin': ('sawp-siang-in', 'wash-clean-ERG'),      # 1x Rev 7:14 - washed their robes
    
    # Round 230: Final hapax vocabulary (approaching 100%)
    'sehlisuah': ('seh-li-suah', 'four-part-become'),        # 1x Rev 6:8 - fourth part
    'sehthum': ('seh-thum', 'four-three'),                   # 1x Zech 13:8 - third shall be left
    'siahdonna': ('siah-don-na', 'sit-stand-NMLZ'),          # 1x Mark 2:14 - receipt of custom
    'sosuk': ('so-suk', 'north-push'),                       # 1x Jer 1:14 - out of north
    'suahsakkhak': ('suah-sak-khak', 'become-CAUS-block'),   # 1x 2Cor 6:1 - receive not in vain
    'suangkangte': ('suang-kang-te', 'stone-marble-PL'),     # 1x Rev 18:12 - marble
    'suktapsak': ('suk-tap-sak', 'push-break-CAUS'),         # 1x Jer 2:16 - have broken
    'sulum': ('su-lum', 'destroy-finish'),                   # 1x 1Cor 10:10 - destroyed of destroyer
    'sumkhotte': ('sum-khot-te', 'money-lack-PL'),           # 1x Mark 10:21 - one thing thou lackest
    'sutatin': ('sut-at-in', 'spoil-hang-ERG'),              # 1x Jer 2:20 - playing the harlot
    'suum': ('suum', 'emerald'),                             # 1x Rev 4:3 - like unto emerald
    'taangmite': ('taang-mi-te', 'messenger-person-PL'),     # 1x Jer 27:3 - by the messengers
    'taankha': ('taan-kha', 'lose-still'),                   # 1x 2John 1:8 - lose not
    'taanlua': ('taan-lua', 'lose-too.much'),                # 1x 2Cor 3:7 - to be done away
    'taanzausak': ('taan-zau-sak', 'lose-wide-CAUS'),        # 1x 2Cor 6:13 - be enlarged
    'tadihin': ('ta-dih-in', 'child-proper-ERG'),            # 1x 1Cor 16:12 - convenient time
    'tangguakun': ('tang-guak-un', 'rise-naked-IMP'),        # 1x Isa 32:11 - strip you bare
    'tankhiat': ('tan-khiat', 'cut-out'),                    # 1x Mark 6:16 - I beheaded
    'tawbo': ('taw-bo', 'with-buttock'),                     # 1x Isa 20:4 - buttocks uncovered
    'tawcip': ('taw-cip', 'arm-squeeze'),                    # 1x Zech 11:17 - arm dried up
    'tawllua': ('tawl-lua', 'tongue-too.much'),              # 1x Jer 9:5 - taught tongue lies
    'tawphah': ('tawp-hah', 'end-foundation'),               # 1x Rev 21:14 - twelve foundations
    'tenma': ('ten-ma', 'before-that'),                      # 1x Acts 7:2 - before he dwelt
    'thakhauhsakkik': ('tha-khauh-sak-kik', 'spirit-revive-CAUS-again'),  # 1x Isa 57:15 - revive
    'thasanpha': ('tha-san-pha', 'spirit-stand-good'),       # 1x Rev 3:2 - strengthen things
    'thehna': ('theh-na', 'sprinkle-NMLZ'),                  # 1x Ezek 43:18 - sprinkle blood
    'themthumte': ('them-thum-te', 'purpose-three-PL'),      # 1x 2Cor 1:17 - things I purpose
    'thuahpah': ('thuah-pah', 'miracle-exactly'),            # 1x Mark 9:39 - do a miracle
    'thugennna': ('thu-gen-na', 'word-say-NMLZ'),            # 1x Jer 23:17 - LORD hath said
    'thukidotna': ('thu-ki-dot-na', 'word-REFL-argue-NMLZ'), # 1x Mark 12:28 - reasoning together
    'thunthuah': ('thun-thuah', 'oil-use'),                  # 1x Matt 25:3 - took no oil
    'tuanlam': ('tuan-lam', 'stand-way'),                    # 1x Dan 1:19 - stood before king
    'tuiphul': ('tui-phul', 'water-cast'),                   # 1x Jer 6:7 - casteth out waters
    'tukguah': ('tuk-guah', 'rain-separate'),                # 1x Jer 5:24 - former and latter rain
    'tuksuk': ('tuk-suk', 'mountain-push'),                  # 1x Dan 2:45 - cut out of mountain
    'tulum': ('tu-lum', 'serpent-coil'),                     # 1x 1Cor 10:9 - destroyed of serpents
    'tunbaih': ('tun-baih', 'present-melt'),                 # 1x 2Pet 3:12 - elements shall melt
    'tunlam': ('tun-lam', 'present-way'),                    # 1x Rev 3:3 - what hour I come
    'tunphetin': ('tun-phet-in', 'now-tell-ERG'),            # 1x Mark 1:30 - anon they tell
    'tupcip': ('tup-cip', 'flood-squeeze'),                  # 1x Matt 24:39 - flood came
    'tuulak': ('tuu-lak', 'howl-voice'),                     # 1x Zech 11:3 - voice of howling
    'uiphuk': ('ui-phuk', 'frog-out'),                       # 1x Rev 16:13 - like frogs
    'valhcip': ('valh-cip', 'bitter-squeeze'),               # 1x Acts 8:23 - gall of bitterness
    'vanzuakin': ('van-zuak-in', 'heaven-sell-ERG'),         # 1x Rev 13:17 - buy or sell
    'vung': ('vung', 'cistern'),                             # 1x Jer 2:13 - broken cisterns
    'zailam': ('zai-lam', 'measure-way'),                    # 1x Ezek 45:3 - of this measure
    'zapin': ('za-pin', 'hear.I-blow'),                      # 1x Isa 54:16 - bloweth the coals
    'zasakkhol': ('za-sak-khol', 'hear.I-CAUS-show'),        # 1x Isa 48:5 - I shewed it thee
    'zatval': ('zat-val', 'use-left.over'),                  # 1x Luke 21:4 - of her penury
    'zehphi': ('zeh-phi', 'conscience-weak'),                # 1x 1Cor 8:7 - conscience weak
    'zelpak': ('zel-pak', 'fame-spread'),                    # 1x Mark 1:28 - fame spread abroad
    'zelzul': ('zel-zul', 'prophesy-follow'),                # 1x 1Cor 14:31 - all prophesy
    'zilepasal': ('zile-pa-sal', 'adultery-father-man'),     # 1x Mark 7:21 - adulteries
    # Numbers stay as partials (expected)
    '144,000': ('144,000', 'NUM'),                           # Rev 7:4 - number
    '666': ('666', 'NUM'),                                   # Rev 13:18 - number of beast
    # Remaining complex forms with unknown intermediate morphemes
    'kaikikpah': ('ka-i-kik-pah', '1SG-need-again-exactly'), # 1x Mark 11:3 - Lord hath need
    'khuaisuahna': ('khua-i-suah-na', 'town-lack-become-NMLZ'),  # 1x Isa 47:9 - loss of children
    'khuaisuahte': ('khua-i-suah-te', 'town-lack-become-PL'),  # 1x Zech 12:10 - mourn
    'kihanthawntawm': ('ki-han-thawn-tawm', 'REFL-do-continue-end'),  # 1x Ezek 38:14 - dwell safely
    
    # Round 227: Final spot-check fixes
    'nawt': ('nawt', 'push'),                                # 9x - push/gore (Deut 33:17)
    'pataukohna': ('pa-tau-koh-na', 'male-signal-call-NMLZ'), # 8x - trumpet alarm (Num 10:9)
    'vatawt': ('vatawt', 'cuckoo'),                          # 6x - cuckoo bird (Lev 11:16)
    'golpi': ('gol-pi', 'creature-great'),                   # 2x - great creature/whale
    'golpite': ('gol-pi-te', 'creature-great-PL'),           # 2x - whales/great creatures (Gen 1:21)
    'paneah': ('paneah', 'PANEAH'),                          # 1x - proper name (Zaphnath-paneah)
    'kikol': ('ki-kol', 'REFL-prevent'),                     # 1x - prevent/hinder
    'nalna': ('nal-na', 'slippery-NMLZ'),                    # 1x - slippery place
    'aknote': ('ak-no-te', 'raven-young-PL'),                # 1x - young ravens
    'ipzote': ('ip-zo-te', 'close-join-PL'),                 # 1x - troubles
    'ipin': ('ip-in', 'restrain-ERG'),                       # 1x - restraining
    'uatsaknate': ('uatsak-na-te', 'pride-NMLZ-PL'),         # 1x - pride/arrogance
    'ettehin': ('et-teh-in', 'care-hold-ERG'),               # 1x - comparing
    
    # Round 230: Fix remaining partials
    'bawngnawithaukhal': ('bawngnawi-thaukhal', 'butter-cream'),  # 2x - dairy products (Gen 18:8, 2Sam 17:29)
    
    # Round 229: Opaque stems with suffixes (nasep, nasem are opaque)
    'nasepna': ('nasep-na', 'work-NMLZ'),                    # 231x - working/work (opaque nasep)
    'nasepte': ('nasep-te', 'work-PL'),                      # 12x - works (opaque nasep)
    'nasemte': ('nasem-te', 'servant-PL'),                   # 389x - servants (opaque nasem)
    'nasemin': ('nasem-in', 'servant-ERG'),                  # as servant
    'naseppih': ('nasep-pih', 'work-APPL'),                  # 17x - work for/with
    'naseppihte': ('nasep-pih-te', 'work-APPL-PL'),          # work for (plural)
    'nasepah': ('nasep-ah', 'work-LOC'),                     # 1x - at work
    'nasepin': ('nasep-in', 'work-ERG'),                     # 3x - work (ERG)
    'nasepsa': ('nasep-sa', 'work-PAST'),                    # 3x - worked
    'nasepsak': ('nasep-sak', 'work-CAUS'),                  # 1x - cause to work
    'nasepteng': ('nasep-teng', 'work-dwell'),               # 1x - work continuously
    'nasepnate': ('nasep-na-te', 'work-NMLZ-PL'),            # 48x - works (nominalized)
    'nasepnasa': ('nasep-na-sa', 'work-NMLZ-PAST'),          # 1x - worked (past nom)
    'nasempa': ('nasem-pa', 'servant-male'),                 # 328x - male servant
    'nasemnu': ('nasem-nu', 'servant-female'),               # 39x - female servant
    'nasemnute': ('nasem-nu-te', 'servant-female-PL'),       # 2x - female servants
    'nasempate': ('nasem-pa-te', 'servant-male-PL'),         # 2x - male servants
    'nasemkhawm': ('nasem-khawm', 'servant-together'),       # 3x - fellow servant
    
    # Round 155: Fix remaining partials for 100% coverage
    # mawhbaang: guilty-alike (10x)
    'mawhbaang': ('mawh-baang', 'guilty-alike'),              # 10x - guilty alike/also guilty
    'mawhbaangte': ('mawh-baang-te', 'guilty-alike-PL'),      # guilty alike (pl)
    # samsiat: destroy (10x) - sam-siat = call-destroy → destroy
    'samsiatnate': ('samsiat-na-te', 'destroy-NMLZ-PL'),      # 10x - destructions
    'samsiatna': ('samsiat-na', 'destroy-NMLZ'),              # destruction
    'samsiat': ('samsiat', 'destroy'),                        # destroy (compound verb)
    # sikkhap: sikkhap = repent-loose (2x) 
    'sikkhap': ('sik-khap', 'turn-loose'),                    # 2x - turn loose/release
    # daina: dai-na (2x) - dai = be.still
    'daina': ('dai-na', 'still-NMLZ'),                        # 2x - stillness/quietness
    'dai': ('dai', 'still'),                                  # be still
    # pillote: pil-lo-te (2x) - lo = NEG
    'pillote': ('pil-lo-te', 'learn-NEG-PL'),                 # 2x - unlearned
    'pillo': ('pil-lo', 'learn-NEG'),                         # unlearned
    # lante: lan-te (2x) - lan = side/form
    'lante': ('lan-te', 'side-PL'),                           # 2x - sides/forms
    # sukgawpna: suk-gawp-na (2x)
    'sukgawpna': ('suk-gawp-na', 'make-grasp-NMLZ'),          # 2x - destruction
    # citakte: ci-tak-te (2x) - citak = say truly
    'citakte': ('ci-tak-te', 'say-true-PL'),                  # 2x - truly said
    'citak': ('ci-tak', 'say-true'),                          # say truly
    # ngongtatnate: ngongtat-na-te (2x)
    'ngongtatnate': ('ngongtat-na-te', 'oppose-NMLZ-PL'),     # 2x - oppositions
    'ngongtatna': ('ngongtat-na', 'oppose-NMLZ'),             # opposition
    # mualliante: mual-lian-te (2x)
    'mualliante': ('mual-lian-te', 'hill-great-PL'),          # 2x - great hills
    'muallian': ('mual-lian', 'hill-great'),                  # great hill
    'muallianah': ('mual-lian-ah', 'hill-great-LOC'),         # at great hill
    # simnate: sim-na-te (2x)
    'simnate': ('sim-na-te', 'read-NMLZ-PL'),                 # 2x - readings
    'simna': ('sim-na', 'read-NMLZ'),                         # reading
    # paidak: pai-dak (2x)
    'paidak': ('pai-dak', 'go-look'),                         # 2x - go look
    # simmawhnate: simmawh-na-te (2x)
    'simmawhnate': ('simmawh-na-te', 'blaspheme-NMLZ-PL'),    # 2x - blasphemies
    'simmawh': ('simmawh', 'blaspheme'),                      # blaspheme
    'simmawhin': ('simmawh-in', 'blaspheme-ERG'),             # blaspheming
    # kikonate: kiko-na-te (2x)
    'kikonate': ('ki-ko-na-te', 'REFL-cry-NMLZ-PL'),          # 2x - cries
    'kikona': ('ki-ko-na', 'REFL-cry-NMLZ'),                  # cry
    # vanpite: vanpi-te (2x)
    'vanpite': ('vanpi-te', 'sky.big-PL'),                    # 2x - heavens
    'vanpi': ('vanpi', 'heaven'),                             # heaven (sky-big)
    # dakdak: dak~dak (2x)
    'dakdak': ('dak~dak', 'strong~REDUP'),                    # 2x - very strong
    # satgawpna: satgawp-na (2x) 
    'satgawpna': ('sat-gawp-na', 'strike-grasp-NMLZ'),        # 2x - striking
    'satgawp': ('sat-gawp', 'strike-grasp'),                  # strike
    # kipzaw: kipzaw (2x)
    'kipzaw': ('kip-zaw', 'diligent-more'),                   # 2x - more diligent
    # ommawkna: ommawk-na (2x)
    'ommawkna': ('om-mawk-na', 'exist-wonder-NMLZ'),          # 2x - wonderfulness
    'ommawk': ('om-mawk', 'exist-wonder'),                    # exist wonderfully
    # sikseekpa: siksek-pa (2x)
    'sikseekpa': ('sik-sek-pa', 'turn-turn-male'),            # 2x - changer/turncoat
    'siksek': ('sik-sek', 'turn-turn'),                       # turnabout
    
    # Round 156: More partial fixes
    'dak': ('dak', 'look'),                                   # 2x - look/gaze
    'kikhenthangte': ('ki-khen-thang-te', 'REFL-separate-ABIL-PL'), # 2x - dispersed ones
    'kikhenthang': ('ki-khen-thang', 'REFL-separate-ABIL'),   # disperse/scatter
    'neihnate': ('neih-na-te', 'have-NMLZ-PL'),               # 2x - possessions
    'neihna': ('neih-na', 'have-NMLZ'),                       # possession
    'luhgawpte': ('luh-gawp-te', 'enter-grasp-PL'),           # 2x - robbers/spoilers
    'luhgawp': ('luh-gawp', 'enter-grasp'),                   # rob/spoil
    'tehkak': ('teh-kak', 'measure-compare'),                 # 2x - compare/liken
    'sumaimang': ('sum-aimang', 'money-empty'),               # 2x - utterly empty (of money)
    'aimang': ('aimang', 'empty'),                            # empty/void
    'ngabeng': ('ngabeng', 'fisherman'),                      # 2x - fisherman
    'ngabengte': ('ngabeng-te', 'fisherman-PL'),              # 2x - fishermen
    'ngetnate': ('nget-na-te', 'request-NMLZ-PL'),            # 2x - requests
    'ngetna': ('nget-na', 'request-NMLZ'),                    # request
    'thupisim': ('thu-pi-sim', 'word-big-count'),             # 2x - important word
    'nuaimang': ('nu-aimang', 'female-empty'),                # 2x - empty/barren woman
    'hanciamnate': ('han-ciam-na-te', 'test-wrestle-NMLZ-PL'), # 2x - labors/struggles
    'hanciamna': ('han-ciam-na', 'test-wrestle-NMLZ'),        # labor/struggle
    'lanna': ('lan-na', 'appear-NMLZ'),                       # 2x - lewdness/appearance
    'bute': ('bu-te', 'heap-PL'),                             # 2x - heaps/wastes
    'bu': ('bu', 'heap'),                                     # heap/pile
    'ciamnuihbawl': ('ciam-nuih-bawl', 'deceive-mock-make'),  # 2x - mockery
    'pena': ('pe-na', 'give-NMLZ'),                           # 2x - giving/portion
    'thanghuaisak': ('thang-huai-sak', 'scatter-defile-CAUS'), # 2x - defile
    'daicip': ('dai-cip', 'still-press'),                     # 2x - hold tongue
    'muanlah': ('muan-lah', 'trust-weak'),                    # 2x - weak faith/doubt
    'omvat': ('om-vat', 'exist-appear'),                      # 2x - appear/be present
    
    # Round 157: More partial fixes
    'khasiathuai': ('kha-siat-huai', 'spirit-evil-full'),     # 2x - compassion/moved
    'paisuakpah': ('pai-suak-pah', 'go-become-unable'),       # 2x - forthwith
    'mipite': ('mi-pi-te', 'person-great-PL'),                # 2x - multitude/nobles
    'mipi': ('mi-pi', 'person-great'),                        # noble/great person
    'semsemzaw': ('sem~sem-zaw', 'serve~REDUP-more'),         # 2x - grow worse
    'gawpte': ('gawp-te', 'all-PL'),                          # 2x - gatherers
    'nauzawpa': ('nau-zaw-pa', 'child-more-male'),            # 2x - younger son
    'nauzaw': ('nau-zaw', 'child-more'),                      # younger child
    'seppihna': ('sep-pih-na', 'work-APPL-NMLZ'),             # 2x - working together
    'khollohte': ('khol-loh-te', 'denounce-fail-PL'),         # 2x - uncomely/less honorable
    'kholloh': ('khol-loh', 'denounce-fail'),                 # less honorable
    'uttawmna': ('ut-tawm-na', 'will-produce-NMLZ'),          # 2x - willingness
    'kiptak': ('kip-tak', 'diligent-true'),                   # 2x - truth/righteousness
    
    # Round 158: Remaining hapax partials - batch 1
    'itzawkna': ('it-zawk-na', 'love-surpass-NMLZ'),          # 1x - beloved/loved more
    'sakhipi': ('sa-khi-pi', 'flesh-deer-big'),               # 1x - hind (deer)
    'sakhino': ('sa-khi-no', 'flesh-deer-young'),             # 1x - young deer
    'tawmluat': ('tawm-luat', 'produce-exceed'),              # 1x - too little
    'sihlohna': ('sih-loh-na', 'die-NEG-NMLZ'),               # 1x - not dead
    'thuneute': ('thu-neu-te', 'word-small-PL'),              # 1x - small matters
    'thuneu': ('thu-neu', 'word-small'),                      # small matter
    'zingciang': ('zing-ciang', 'morning-then'),              # 1x - tomorrow
    'suksiatkhak': ('suk-siat-khak', 'make-destroy-stop'),    # 1x - perish/destroy
    'lahte': ('lah-te', 'lamp-PL'),                           # 1x - lamps/instruments
    'sunna': ('sun-na', 'mold-NMLZ'),                         # 1x - molding/fashioning
    'paikhopna': ('pai-khop-na', 'go-together-NMLZ'),         # 1x - going together
    'sukkhap': ('suk-khap', 'make-loosen'),                   # 1x - hew/cut
    "sukkhapte'": ("suk-khap-te'", 'make-loosen-PL.POSS'),    # 1x - hewn (poss)
    'mawhpihna': ('mawh-pih-na', 'guilt-APPL-NMLZ'),          # 1x - nakedness/shame
    'kisungtawm': ('ki-sung-tawm', 'REFL-inside-produce'),    # 1x - molten/idols
    'khentelna': ('khen-tel-na', 'separate-know-NMLZ'),       # 1x - difference/separation
    
    # Round 158: Remaining hapax partials - batch 2
    'utluatna': ('ut-luat-na', 'will-exceed-NMLZ'),           # 1x - going whoring
    'kaangto': ('ka-ang-to', '1SG-rise-CONT'),                # 1x - I rise up
    'siamaimang': ('siam-aimang', 'create-destroy'),          # 1x - utterly perish
    'siamangsak': ('siam-ang-sak', 'create-face-CAUS'),       # 1x - destroy quickly
    'kineubawl': ('ki-neu-bawl', 'REFL-small-make'),          # 1x - seem vile
    "daite,": ('dai-te', 'itch-PL'),                          # 1x - scab/itch (pl)
    'daite': ('dai-te', 'itch-PL'),                           # itch (pl)
    'citheizaw': ('ci-thei-zaw', 'say-ABIL-more'),            # 1x - multiply more
    'zuihlah': ('zuih-lah', 'follow-far'),                    # 1x - far off
    'omkhawmte': ('om-khawm-te', 'exist-gather-PL'),          # 1x - those with
    'lungkhauhnate': ('lung-khauh-na-te', 'heart-strong-NMLZ-PL'), # 1x - stubborn ways
    'lungkhauhna': ('lung-khauh-na', 'heart-strong-NMLZ'),    # stubborn way
    'pilpennu': ('pil-pen-nu', 'learn-SUPER-female'),         # 1x - wise lady
    'pilpen': ('pil-pen', 'learn-SUPER'),                     # wisest
    "kileinapa,": ('ki-lei-na-pa', 'REFL-buy-NMLZ-male'),     # 1x - buyer (jubilee)
    'kileinapa': ('ki-lei-na-pa', 'REFL-buy-NMLZ-male'),      # buyer
    
    # Round 159: More hapax fixes - batch 3
    "vakang,": ('vak-ang', 'walk-face'),                      # 1x - go/walk
    "siahsun'": ("siah-sun'", 'decay-time'),                  # 1x - decay time
    'zoppihte': ('zop-pih-te', 'join-APPL-PL'),               # 1x - brothers joined
    'thaunate': ('thau-na-te', 'fat-NMLZ-PL'),                # 1x - fatness
    'thaunna': ('thau-na', 'fat-NMLZ'),                       # fatness
    'nuamsakin': ('nuam-sak-in', 'happy-CAUS-CVB'),           # 1x - making merry
    'kitapkhapna': ('ki-tap-khap-na', 'REFL-anguish-loose-NMLZ'), # 1x - breach/repentance
    'sunsuk': ('sun-suk', 'pot-dip'),                         # 1x - pan/pot
    'lupkhopna': ('lup-khop-na', 'lie-together-NMLZ'),        # 1x - lying together
    'genthangna': ('gen-thang-na', 'speak-hear-NMLZ'),        # 1x - report/hearing
    'niampen': ('niam-pen', 'low-SUPER'),                     # 1x - smallest/least
    "khawmna,": ('khawm-na', 'gather-NMLZ'),                  # 1x - gathering
    'khawmna': ('khawm-na', 'gather-NMLZ'),                   # gathering
    'omkhopna': ('om-khop-na', 'exist-together-NMLZ'),        # 1x - together
    'nolhkhitna': ('nolh-khit-na', 'reject-SEQ-NMLZ'),        # 1x - rejection
    'kiteltak': ('ki-tel-tak', 'REFL-know-true'),             # 1x - certainty
    'taksuak': ('tak-suak', 'true-become'),                   # 1x - truly (will do)
    'khauzang': ('khauzang', 'measure.line'),                 # 1x - measuring line
    'vannusiatte': ('van-nu-siat-te', 'sky-mother-destroy-PL'), # 1x - silver vessels
    'vannusiat': ('van-nu-siat', 'sky-mother-destroy'),       # silver vessel
    
    # Round 160: More hapax fixes - batch 4
    'sikbeeldai': ('sik-beel-dai', 'turn-bowl-flat'),         # 1x - pan (cooking)
    'khuadaksuk': ('khua-dak-suk', 'town-look-approach'),     # 1x - look toward
    'phelvat': ('phel-vat', 'clear-quick'),                   # 1x - hastily/discern
    'inndeineu': ('inn-dei-neu', 'house-small-small'),        # 1x - little chamber
    'khiakin': ('khia-kin', 'exit-stick'),                    # 1x - stick/rod
    'apnate': ('ap-na-te', 'entrust-NMLZ-PL'),                # 1x - bestowed
    'apna': ('ap-na', 'entrust-NMLZ'),                        # entrusting
    "nautangte,": ('nau-tang-te', 'child-hold-PL'),           # 1x - children
    'nautangte': ('nau-tang-te', 'child-hold-PL'),            # children
    'siangpente': ('siang-pen-te', 'holy-SUPER-PL'),          # 1x - most holy
    'siangpen': ('siang-pen', 'holy-SUPER'),                  # most holy
    'beinate': ('bei-na-te', 'stone-NMLZ-PL'),                # 1x - great stones
    'beina': ('bei-na', 'stone-NMLZ'),                        # stones
    'nilohna': ('ni-loh-na', 'day-fail-NMLZ'),                # 1x - day and night
    "citakzaw,": ('ci-tak-zaw', 'say-true-more'),             # 1x - more faithful
    'citakzaw': ('ci-tak-zaw', 'say-true-more'),              # more faithful
    'kinloin': ('kin-lo-in', 'together-NEG-ERG'),             # 1x - not forsake
    'puanpakte': ('puan-pak-te', 'cloth-divide-PL'),          # 1x - hangings
    'puanpak': ('puan-pak', 'cloth-divide'),                  # hanging
    'nopzawk': ('nop-zawk', 'like-more'),                     # 1x - delight more
    'neisun': ('nei-sun', 'have-time'),                       # 1x - increase
    'laisun': ('lai-sun', 'midst-time'),                      # 1x - a little while
    'theihzawk': ('theih-zawk', 'know-more'),                 # 1x - understand also
    
    # Round 161: More hapax fixes - batch 5
    'thusiapi': ('thu-sia-pi', 'word-evil-big'),              # 1x - bitter things
    'deidai': ('dei-dai', 'sweet-flat'),                      # 1x - meat/gall
    'bawlgawpna': ('bawl-gawp-na', 'make-all-NMLZ'),          # 1x - terror/making
    'thumawkna': ('thu-mawk-na', 'word-wonder-NMLZ'),         # 1x - vanity/leasing
    'panmunkip': ('pan-mun-kip', 'begin-place-diligent'),     # 1x - ordained strength
    'gamsialno': ('gam-sial-no', 'land-ride-young'),          # 1x - young unicorn
    'gamsial': ('gam-sial', 'land-ride'),                     # unicorn
    'teitangzang': ('tei-tang-zang', 'wise-hold-measure'),    # 1x - spear
    'hatluate': ('hat-lua-te', 'strong-exceed-PL'),           # 1x - too strong
    'hatlua': ('hat-lua', 'strong-exceed'),                   # too strong
    'kisuncip': ('ki-sun-cip', 'REFL-in-press'),              # 1x - cast down
    'kitelsiang': ('ki-tel-siang', 'REFL-know-clear'),        # 1x - understanding
    'tuaksuksuak': ('tuak-suk-suak', 'meet-move-become'),     # 1x - consume
    'thubulpi': ('thu-bul-pi', 'word-origin-big'),            # 1x - true from beginning
    'mukhate': ('mu-kha-te', 'see-out-PL'),                   # 1x - turned back
    'phatnophuai': ('phat-nop-huai', 'praise-like-full'),     # 1x - pleasant
    
    # Suffix patterns for remaining partials
    "vakang,": ('vak-ang', 'walk-toward'),                    # 1x
    'naang': ('na-ang', '2SG-toward'),                        # 1x
    "khopte:": ('khop-te', 'together-PL'),                    # 1x
    'takte': ('tak-te', 'true-PL'),                           # 1x
    "kikhennate,": ('ki-khen-na-te', 'REFL-separate-NMLZ-PL'), # 1x
    'kikhennate': ('ki-khen-na-te', 'REFL-separate-NMLZ-PL'), # separations
    'sawlnate': ('sawl-na-te', 'send-NMLZ-PL'),               # 1x - sendings
    'sawlna': ('sawl-na', 'send-NMLZ'),                       # sending
    'laknate': ('lak-na-te', 'take-NMLZ-PL'),                 # 1x - takings
    'lakna': ('lak-na', 'take-NMLZ'),                         # taking
    "hihnasate,": ('hih-nasa-te', 'be-much-PL'),              # 1x
    'hihnasate': ('hih-nasa-te', 'be-much-PL'),               # many beings
    'laisunte': ('lai-sun-te', 'midst-time-PL'),              # 1x - while (pl)
    'sakpente': ('sak-pen-te', 'make-SUPER-PL'),              # 1x - greatest
    'sakpen': ('sak-pen', 'make-SUPER'),                      # greatest
    'paunasate': ('pau-nasa-te', 'speak-much-PL'),            # 1x - many speakers
    'tawntungnate': ('tawn-tung-na-te', 'eternal-arrive-NMLZ-PL'), # 1x
    'launate': ('lau-na-te', 'fear-NMLZ-PL'),                 # 1x - fears
    'launa': ('lau-na', 'fear-NMLZ'),                         # fear
    'linnate': ('lin-na-te', 'hope-NMLZ-PL'),                 # 1x - hopes
    'linna': ('lin-na', 'hope-NMLZ'),                         # hope
    "ngaihsunsunin,": ('ngaih-sun~sun-in', 'think-time~REDUP-ERG'), # 1x
    'kikoihdak': ('ki-koih-dak', 'REFL-place-look'),          # 1x - restore
    'hektohnate': ('hek-toh-na-te', 'show-up-NMLZ-PL'),       # 1x - shewings
    "panpihna,": ('pan-pih-na', 'begin-APPL-NMLZ'),           # 1x - pleading
    'panpihna': ('pan-pih-na', 'begin-APPL-NMLZ'),            # pleading
    'saknate': ('sak-na-te', 'cause-NMLZ-PL'),                # 1x - causings
    'sakna': ('sak-na', 'cause-NMLZ'),                        # causing
    'zuakpahte': ('zuak-pah-te', 'sell-unable-PL'),           # 1x - cannot sell
    'tutmawkna': ('tut-mawk-na', 'sleep-wonder-NMLZ'),        # 1x - deep sleep
    'paupakna': ('pau-pak-na', 'speak-divide-NMLZ'),          # 1x - division
    'ettelna': ('et-tel-na', 'care-know-NMLZ'),               # 1x - consideration
    "hana,": ('ha-na', 'tooth-NMLZ'),                         # 1x
    'cimbeng': ('cim-beng', 'pierce-flat'),                   # 1x - young
    'zakthadahhuai': ('zak-tha-dah-huai', 'hear-new-put-full'), # 1x
    "lanlan.": ('lan~lan', 'appear~REDUP'),                   # 1x - appearing
    'hatang': ('hat-ang', 'strong-toward'),                   # 1x
    'sakolpite': ('sa-kol-pi-te', 'flesh-colt-big-PL'),       # 1x - donkeys
    'lungzuanhuai': ('lung-zuan-huai', 'heart-turn-full'),    # 1x - feel
    'sangpenin': ('sang-pen-in', 'high-SUPER-ERG'),           # 1x - most high
    "sitnate;": ('sit-na-te', 'cut-NMLZ-PL'),                 # 1x - cuttings
    'sitnate': ('sit-na-te', 'cut-NMLZ-PL'),                  # cuttings
    'puanpite': ('puan-pi-te', 'cloth-big-PL'),               # 1x - cloths
    'vandak': ('van-dak', 'sky-look'),                        # 1x - look up
    'mualciang': ('mual-ciang', 'hill-top'),                  # 1x - hilltop
    'lokha': ('lo-kha', 'field-out'),                         # 1x - out of field
    "phelkhap,": ('phel-khap', 'clear-loose'),                # 1x - cleared
    'phelkhap': ('phel-khap', 'clear-loose'),                 # cleared
    'ngasiahna': ('nga-siah-na', 'fish-descend-NMLZ'),        # 1x
    'suaktasun': ('suak-ta-sun', 'become-child-time'),        # 1x
    'limlahna': ('lim-lah-na', 'image-far-NMLZ'),             # 1x
    'seppihte': ('sep-pih-te', 'work-APPL-PL'),               # 1x - workers
    "siahkhawmte,": ('siah-khawm-te', 'decay-gather-PL'),     # 1x
    'siahkhawmte': ('siah-khawm-te', 'decay-gather-PL'),      # decayed
    'etsathuai': ('et-sat-huai', 'care-strike-full'),         # 1x
    'sutgawppa': ('sut-gawp-pa', 'wipe-all-male'),            # 1x - spoiler
    'paihdak': ('paih-dak', 'drive-look'),                    # 1x
    
    # Round 162: Final batch of hapax fixes
    "vakang,": ('vak-ang', 'walk-face'),                      # walk toward
    "khopte:": ('khop-te', 'together-PL'),                    # together ones
    "ngaihsunsunin,": ('ngaih-sun~sun-in', 'think-time~REDUP-ERG'),
    "hana,": ('ha-na', 'breath-NMLZ'),                        # breathing
    "lanlan.": ('lan~lan', 'side~REDUP'),                     # sides
    'semkhawmte': ('sem-khawm-te', 'serve-together-PL'),      # fellow servants
    'baangte': ('baang-te', 'alike-PL'),                      # alike ones
    "sunpa,": ('sun-pa', 'basket-male'),                      # basket maker
    'sunpa': ('sun-pa', 'basket-male'),                       # basket maker
    'kinlo': ('kin-lo', 'together-NEG'),                      # not together
    'sanzawk': ('san-zawk', 'lean-more'),                     # leaner
    'dektakta': ('dek-tak-ta', 'low-true-PAST'),              # truly lowered
    'nungkin': ('nung-kin', 'live-together'),                 # live together
    'bawltawmte': ('bawl-tawm-te', 'make-produce-PL'),        # makers
    'kamkhapte': ('kam-khap-te', 'mouth-loose-PL'),           # open-mouthed
    'liatluatna': ('liat-luat-na', 'great-exceed-NMLZ'),      # greatness
    'kawikawinate': ('kawikawi-na-te', 'to.and.fro-NMLZ-PL'), # tales
    'sabeng': ('sa-beng', 'flesh-flat'),                      # flat flesh
    'khuakin': ('khua-kin', 'town-together'),                 # fellow townsman
    'kikhenthangsak': ('ki-khen-thang-sak', 'REFL-separate-ABIL-CAUS'), # scatter
    'mundai': ('mun-dai', 'place-flat'),                      # level place
    'kialpite': ('ki-al-pi-te', 'REFL-hunger-big-PL'),        # very hungry
    'paikhiatpihte': ('pai-khiat-pih-te', 'go-away-APPL-PL'), # sent away
    'hatnate': ('hat-na-te', 'strong-NMLZ-PL'),               # strengths
    'hatna': ('hat-na', 'strong-NMLZ'),                       # strength
    'siatgawpna': ('siat-gawp-na', 'destroy-all-NMLZ'),       # destruction
    'thalpite': ('thal-pi-te', 'bow-big-PL'),                 # bows
    'thalpi': ('thal-pi', 'bow-big'),                         # bow
    'limnono': ('lim-no-no', 'image-young-young'),            # very young image
    'losia': ('lo-sia', 'field-bad'),                         # bad field
    'sawnte': ('sawn-te', 'enemy-PL'),                        # enemies
    "keuneute,": ('keu-neu-te', 'back-small-PL'),             # small backs
    'keuneute': ('keu-neu-te', 'back-small-PL'),              # small backs
    'sabengte': ('sa-beng-te', 'flesh-flat-PL'),              # flat flesh (pl)
    'khuadakdak': ('khua-dak~dak', 'town-look~REDUP'),        # look all around
    'khuadakzo': ('khua-dak-zo', 'town-look-COMPL'),          # looked at town
    'zahpihhuai': ('zah-pih-huai', 'respect-APPL-full'),      # respectful
    'sukkhapna': ('suk-khap-na', 'make-loose-NMLZ'),          # loosening
    'kikapnate': ('ki-kap-na-te', 'REFL-fight-NMLZ-PL'),      # fights
    'kikapna': ('ki-kap-na', 'REFL-fight-NMLZ'),              # fight
    'gialpite': ('gial-pi-te', 'spotted-big-PL'),             # spotted ones
    'gialpi': ('gial-pi', 'spotted-big'),                     # spotted
    'siaksiang': ('siak-siang', 'die-clear'),                 # clearly dead
    'baangteng': ('baang-teng', 'alike-all'),                 # all alike
    'nopsaknateng': ('nop-sak-na-teng', 'like-CAUS-NMLZ-all'), # pleasing
    'etkak': ('et-kak', 'care-compare'),                      # compare care
    'mindainateng': ('min-dai-na-teng', 'name-still-NMLZ-all'), # shame
    'ciahpihna': ('ciah-pih-na', 'return-APPL-NMLZ'),         # returning
    'lametnateng': ('lamet-na-teng', 'example-NMLZ-all'),     # all examples
    'ompakna': ('om-pak-na', 'exist-divide-NMLZ'),            # division
    'daikhak': ('dai-khak', 'still-stop'),                    # still
    'satkhapna': ('sat-khap-na', 'strike-loose-NMLZ'),        # striking
    'cimtakta': ('cim-tak-ta', 'pierce-true-PAST'),           # truly pierced
    "ulianpipi,": ('u-lian-pi-pi', 'elder-great-big-INTENS'), # very great
    'ngaihzawk': ('ngaih-zawk', 'think-more'),                # think more
    'mindainate': ('min-dai-na-te', 'name-still-NMLZ-PL'),    # shames
    'mawkte': ('mawk-te', 'wonder-PL'),                       # wonders
    'etkakna': ('et-kak-na', 'care-compare-NMLZ'),            # comparison
    'enkak': ('en-kak', 'see-compare'),                       # compare seeing
    'cidamzaw': ('ci-dam-zaw', 'say-well-more'),              # speak better
    'siamzawklam': ('siam-zawk-lam', 'skilled-more-way'),     # more skilled way
    'pilzawk': ('pil-zawk', 'learn-more'),                    # learn more
    "vaihawmpite,": ('vaihawm-pi-te', 'counsel-big-PL'),      # counselors
    'vaihawmpite': ('vaihawm-pi-te', 'counsel-big-PL'),       # counselors
    'hilhtelna': ('hilh-tel-na', 'teach-know-NMLZ'),          # teaching
    'telna': ('tel-na', 'know-NMLZ'),                         # knowledge
    'suakvat': ('suak-vat', 'become-quick'),                  # quickly become
    'nipisim': ('ni-pi-sim', 'day-big-count'),                # great day
    'sungzah': ('sung-zah', 'inside-respect'),                # inner respect
    'uuklua': ('uuk-lua', 'bend-exceed'),                     # greatly bent
    'khemnateng': ('khem-na-teng', 'restrain-NMLZ-all'),      # all restraints
    'thahatnateng': ('tha-hat-na-teng', 'slay-strong-NMLZ-all'), # slayings
    'kalhkhapna': ('kalh-khap-na', 'lock-loose-NMLZ'),        # unlocking
    'khangsawnte': ('khang-sawn-te', 'generation-enemy-PL'),  # enemy generations
    'kinenniamnate': ('ki-nen-niam-na-te', 'REFL-afflict-low-NMLZ-PL'), # afflictions
    'umpihte': ('um-pih-te', 'believe-APPL-PL'),              # believers
    'khuadakna': ('khua-dak-na', 'town-look-NMLZ'),           # looking at town
    'neubawl': ('neu-bawl', 'small-make'),                    # make small
    'koihdakna': ('koih-dak-na', 'put-look-NMLZ'),            # restoring
    'lungdampihna': ('lungdam-pih-na', 'rejoice-APPL-NMLZ'),  # rejoicing together
    'khanglosak': ('khang-lo-sak', 'generation-NEG-CAUS'),    # not continue
    'nitnateng': ('nit-na-teng', 'defile-NMLZ-all'),          # defilements
    'mittawpite': ('mit-tawp-i-te', 'eye-end-?-PL'),          # blind ones
    'ngamlah': ('ngam-lah', 'dare-far'),                      # far away
    'mawkmai': ('mawk-mai', 'wonder-face'),                   # wonder face
    'cihtakzawk': ('cih-tak-zawk', 'say-true-more'),          # speak more truly
    'damkhitna': ('dam-khit-na', 'well-SEQ-NMLZ'),            # wellness after
    'sapnateng': ('sap-na-teng', 'call-NMLZ-all'),            # all callings
    'sangpahte': ('sang-pah-te', 'high-unable-PL'),           # cannot reach high
    'sumbawlpa': ('sum-bawl-pa', 'money-make-male'),          # money maker
    'sangpena': ('sang-pen-a', 'high-SUPER-NOM'),             # most high
    'tutnate': ('tut-na-te', 'sleep-NMLZ-PL'),                # sleeps
    'tutna': ('tut-na', 'sleep-NMLZ'),                        # sleep
    'nuampente': ('nuam-pen-te', 'pleased-SUPER-PL'),         # most pleased
    'nuampen': ('nuam-pen', 'pleased-SUPER'),                 # most pleased
    'ngahsunte': ('ngah-sun-te', 'get-time-PL'),              # getting times
    'genhak': ('gen-hak', 'speak-hard'),                      # speak harshly
    'nekkhopna': ('nek-khop-na', 'eat-together-NMLZ'),        # eating together
    'noptuamzaw': ('nop-tuam-zaw', 'like-also-more'),         # like more also
    'daipah': ('dai-pah', 'still-unable'),                    # cannot be still
    'takteng': ('tak-teng', 'true-all'),                      # all true
    'sangpenna': ('sang-pen-na', 'high-SUPER-NMLZ'),          # highness
    'damnazia': ('dam-na-zia', 'well-NMLZ-manner'),           # wellness manner
    'dampahna': ('dam-pah-na', 'well-unable-NMLZ'),           # unable wellness
    "dektaksa-in": ('dek-tak-sa-in', 'low-true-PAST-ERG'),    # truly lowered
    'uklah': ('uk-lah', 'cover-far'),                         # far cover
    'kiamvat': ('kiam-vat', 'diminish-quick'),                # quickly diminish
    'lupkhitna': ('lup-khit-na', 'lie-SEQ-NMLZ'),             # lying after
    'theihkhitna': ('theih-khit-na', 'know-SEQ-NMLZ'),        # knowing after
    
    # Round 163: Final 60 hapax - push to 100%
    "vakang,": ('vak-ang', 'walk-toward'),                    # walking
    "khopte:": ('khop-te', 'together-PL'),                    # together ones
    "ngaihsunsunin,": ('ngaih-sun~sun-in', 'think-time~REDUP-ERG'),
    "hana,": ('ha-na', 'tooth-NMLZ'),                         # teeth
    "lanlan.": ('lan~lan', 'appear~REDUP'),                   # appearing
    "ulianpipi,": ('u-lian-pi-pi', 'elder-great-big-INTENS'), # greatest elder
    'mittawpite': ('mit-tawp-te', 'eye-end-PL'),              # blind ones
    'nungkinin': ('nung-kin-in', 'live-together-ERG'),        # living together
    'lutsukpah': ('lut-suk-pah', 'enter-move-unable'),        # cannot enter
    'enluatna': ('en-luat-na', 'see-exceed-NMLZ'),            # exceeding sight
    'gelhzawk': ('gelh-zawk', 'write-more'),                  # write more
    'gamdaizaw': ('gam-dai-zaw', 'land-flat-more'),           # flatter land
    'tonpihte': ('ton-pih-te', 'pull-APPL-PL'),               # pullers
    'omkhitna': ('om-khit-na', 'exist-SEQ-NMLZ'),             # existing after
    'mawhzonnate': ('mawh-zon-na-te', 'guilt-strive-NMLZ-PL'), # quarrels
    'paisuaknop': ('pai-suak-nop', 'go-become-like'),         # willing to go
    'khualzinpihte': ('khualzin-pih-te', 'journey-APPL-PL'),  # fellow travelers
    'numeipihte': ('numei-pih-te', 'woman-APPL-PL'),          # women together
    'kiphellah': ('ki-phel-lah', 'REFL-clear-far'),           # far cleared
    'neihnateng': ('neih-na-teng', 'have-NMLZ-all'),          # all possessions
    'theihtawmna': ('theih-tawm-na', 'know-produce-NMLZ'),    # knowledge
    'pihte': ('pih-te', 'APPL-PL'),                           # applied ones
    'kithuneihnate': ('ki-thu-neih-na-te', 'REFL-word-have-NMLZ-PL'), # ministries
    'hihlamtak': ('hih-lam-tak', 'be-way-true'),              # truly this way
    'kikhelvat': ('ki-khel-vat', 'REFL-differ-quick'),        # quickly differ
    'ngetsaknate': ('nget-sak-na-te', 'pray-CAUS-NMLZ-PL'),   # prayers
    'tatnate': ('tat-na-te', 'strike-NMLZ-PL'),               # strikes
    'ngaklahin': ('ngak-lah-in', 'wait-far-ERG'),             # waiting long
    'kakin': ('ka-kin', '1SG-together'),                      # I together
    'dektakna': ('dek-tak-na', 'low-true-NMLZ'),              # true lowness
    'zuihlahna': ('zuih-lah-na', 'follow-far-NMLZ'),          # far following
    'suknateng': ('suk-na-teng', 'make-NMLZ-all'),            # all makings
    'cimtakhuai': ('cim-tak-huai', 'pierce-true-full'),       # truly pierced
    'omkhawmna': ('om-khawm-na', 'exist-gather-NMLZ'),        # gathering
    'omnate': ('om-na-te', 'exist-NMLZ-PL'),                  # existences
    'thanghuai': ('thang-huai', 'scatter-full'),              # scattered
    'pite': ('pi-te', 'big-PL'),                              # big ones
    'selnate': ('sel-na-te', 'slice-NMLZ-PL'),                # slices
    'luannate': ('luan-na-te', 'flow-NMLZ-PL'),               # flows
    "lungkipna,": ('lung-kip-na', 'heart-diligent-NMLZ'),     # heartfelt
    'lungkipna': ('lung-kip-na', 'heart-diligent-NMLZ'),      # heartfelt
    'kinzaw': ('kin-zaw', 'together-more'),                   # more together
    'lungkipin': ('lung-kip-in', 'heart-diligent-ERG'),       # heartfelt
    'gensiatkhak': ('gen-siat-khak', 'speak-destroy-stop'),   # stop speaking
    "seelloin,": ('seel-lo-in', 'basket-NEG-ERG'),            # without basket
    "thuaklahin,": ('thuak-lah-in', 'suffer-far-ERG'),        # suffer long
    'liatzawk': ('liat-zawk', 'great-more'),                  # greater
    'minthanzawk': ('min-than-zawk', 'name-bless-more'),      # more blessed
    'lutlah': ('lut-lah', 'enter-far'),                       # far enter
    'kitelpha': ('ki-tel-pha', 'REFL-know-reach'),            # know self
    'ngahlah': ('ngah-lah', 'get-far'),                       # get far
    'nuihnate': ('nuih-na-te', 'laugh-NMLZ-PL'),              # laughs
    'nuihna': ('nuih-na', 'laugh-NMLZ'),                      # laugh
    'lungdamnate': ('lungdam-na-te', 'rejoice-NMLZ-PL'),      # rejoicings
    'lungdamna': ('lungdam-na', 'rejoice-NMLZ'),              # rejoicing
    'silhnate': ('silh-na-te', 'clothe-NMLZ-PL'),             # clothings
    'silhna': ('silh-na', 'clothe-NMLZ'),                     # clothing
    'duhluatna': ('duh-luat-na', 'want-exceed-NMLZ'),         # excessive want
    'deihluatin': ('deih-luat-in', 'want-exceed-ERG'),        # excessively wanting
    'kicinzawk': ('ki-cin-zawk', 'REFL-pierce-more'),         # pierce more
    'ngamnate': ('ngam-na-te', 'dare-NMLZ-PL'),               # darings
    'ngamna': ('ngam-na', 'dare-NMLZ'),                       # daring
    'satkhap': ('sat-khap', 'strike-loose'),                  # strike loose
    'dekdak': ('dek-dak', 'low-look'),                        # look down
    'liatnateng': ('liat-na-teng', 'great-NMLZ-all'),         # all greatness
    
    # Round 164: Final 8 for 100% - base forms + punctuation variants
    'vakang': ('vak-ang', 'walk-toward'),                     # walking toward
    'khopte': ('khop-te', 'enough-PL'),                       # enough ones
    'ngaihsunsunin': ('ngaih-sun~sun-in', 'think-time~REDUP-ERG'), # thinking repeatedly
    'hana': ('ha-na', 'tooth-NMLZ'),                          # teeth
    'lanlan': ('lan~lan', 'appear~REDUP'),                    # appearing repeatedly
    'ulianpipi': ('u-lian-pi~pi', 'elder-great-big~INTENS'),  # greatest elder
    'seelloin': ('seel-lo-in', 'basket-NEG-ERG'),             # without basket
    'thuaklahin': ('thuak-lah-in', 'suffer-far-ERG'),         # suffering long
    
    # Round 165: suk- prefix compounds (causative/factitive "make/cause to become")
    # Note: suk- as prefix = causative; -suk as suffix = DOWN (directional)
    'suksakna': ('suk-sak-na', 'cause.become-CAUS-NMLZ'),     # humiliation (make low)
    'suktaak': ('suk-taak', 'cause.become-comb'),             # make combed/groomed
    'sukkhakna': ('suk-khak-na', 'cause.become-restrain-NMLZ'), # restraining
    'kisuktat': ('ki-suk-tat', 'REFL-cause.become-cut'),      # be cut down
    'sukcipna': ('suk-cip-na', 'cause.become-tight-NMLZ'),    # tightening
    'sukniam': ('suk-niam', 'cause.become-low'),              # abase/humble
    'suksiatnate': ('suk-siat-na-te', 'cause.become-destroy-NMLZ-PL'), # destructions
    'suktat': ('suk-tat', 'cause.become-cut'),                # cut down
    'sukpaih': ('suk-paih', 'cause.become-pour'),             # pour out
    'suktan': ('suk-tan', 'cause.become-broken'),             # break
    'suktai': ('suk-tai', 'cause.become-bright'),             # illuminate/brighten
    'sukmai': ('suk-mai', 'cause.become-face'),               # turn face toward
    'suksiatzawh': ('suk-siat-zawh', 'cause.become-destroy-COMPL'), # completely destroy
    'suktuah': ('suk-tuah', 'cause.become-do'),               # cause to do
    'sukpai': ('suk-pai', 'cause.become-go'),                 # cause to go/send
    'sukmit': ('suk-mit', 'cause.become-eye'),                # open eyes
}
