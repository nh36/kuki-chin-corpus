# Tedim Chin Morphological Analyzer Regression Tests

This document captures errors that were fixed during development.
**Review before each commit** to ensure no regressions.

## Test Format
Each test shows:
- **Citation**: Bible verse reference
- **Token/Phrase**: The Tedim text being tested
- **KJV**: English translation for context
- **Wrong**: Previous incorrect parse
- **Correct**: Expected correct parse

---

## 1. PROSP → IRR (ding marker)

**Source**: Zam Ngaih Cing (2018) - "irrealis marker"

| Token | Wrong | Correct |
|-------|-------|---------|
| ding | PROSP | IRR |
| dinghi | PROSP-be | IRR-be |
| dingin | PROSP-ERG | IRR-ERG |

**Citation**: Throughout corpus (13,000+ occurrences)

---

## 2. Proper Noun vs Common Word Disambiguation

### 2.1 sin/Sin
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| sin | SIN (proper) | near | lowercase = common word |
| Sin | near | SIN | Wilderness of Sin (EXO 16:1) |

**Citation**: EXO 16:1 "Sin khuazing" (Wilderness of Sin)

### 2.2 lot/Lot
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| lot | arrow | cast (verb) | verbal use (GEN 31:35) |
| Lot | cast | LOT | proper noun (GEN 11:27) |
| lotte | lo-te | lot-te (arrow-PL) | plural of lot 'arrow' |

**Citation**: GEN 11:27 "Lot a tapa" (Lot his son)

---

## 3. Ghost Entries Removed

These meanings were incorrectly in the dictionary but don't appear in corpus:

| Token | Ghost Meaning | Actual Meaning | Evidence |
|-------|---------------|----------------|----------|
| awk | ram | trap/snare | ram = tuutal |
| huh | blow | help | blow = mut/kitum |
| zong | warm | also | warm = lum |
| hang | stallion | reason | horse = sakol |
| ap | span | entrust | span = letmat kua |

---

## 4. Polysemy Disambiguation

### 4.1 kham (gold vs forbid vs hold)
| Context | Parse | Meaning |
|---------|-------|---------|
| kham (default) | gold | precious metal |
| kikham | REFL-forbid | refrain |
| pawi kham | feast hold | hold feast |

**Citation**: GEN 2:11 "kham a omna" (where gold is)

### 4.2 vei (sick vs time)
| Context | Parse | Meaning |
|---------|-------|---------|
| vei (default) | sick | illness |
| khatvei | one-time | once |
| nihvei | two-time | second time |

**Citation**: GEN 27:36 "nihvei hong suankhia" (twice deceived)

---

## 5. Tokenization

Apostrophe-containing words must be kept intact:

| Token | Wrong Split | Correct |
|-------|-------------|---------|
| ke'n | ke + n | ke'n (1SG.PRO) |
| hi'ng | hi + ng | hi'ng (be-EMPH) |

---

## 6. Function Words (Opaque)

These parse as atomic units, not decomposed:

| Token | Wrong | Correct |
|-------|-------|---------|
| ahihleh | a-hih-leh (3SG-be.II-if) | ahihleh (if) |
| bangmah | bang-mah (what-EMPH) | bangmah (nothing) |
| kuamah | kua-mah (who-EMPH) | kuamah (nobody) |

---

## Running Tests

```python
# Quick verification
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

tests = [
    ('ding', 'IRR'),           # not PROSP
    ('sin', 'near'),           # not SIN
    ('Sin', 'SIN'),            # proper noun
    ('lot', 'cast'),           # verb, not arrow
    ('Lot', 'LOT'),            # proper noun
    ('kham', 'gold'),          # default
    ('kikham', 'REFL-forbid'), # with ki-
    ('ahihleh', 'if'),         # opaque
    ("ke'n", '1SG.PRO'),       # apostrophe preserved
]

for token, expected_gloss in tests:
    seg, gloss = analyze_word(token)
    status = '✓' if expected_gloss in gloss else '✗'
    print(f'{status} {token}: {gloss}')
```

---

## 7. Opaque Lexemes (Wrong Decomposition)

These words look like compounds but have idiomatic meanings:

| Token | Wrong | Correct | Meaning |
|-------|-------|---------|---------|
| lupna | lup-na (bow.down-NMLZ) | lupna | bed |
| zatui | za-tui (hear-water) | zatui | medicine |
| golhguk | golh-guk (oppose-six) | golhguk | bribe |
| namsau | nam-sau (hair-long) | namsau | sword |
| sanggam | sang-gam (high-land) | sanggam | brother |
| zungbuh | zung-buh (root-rice) | zungbuh | ring |

**Citation**: lupna 85x, zatui 13x, namsau 447x

---

## 8. Homophonous Roots (Polysemy)

### 8.1 mei (fire vs female)
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| mei | female | fire | standalone |
| numei | fire-? | mother-female | woman |
| meigong | fire-alone | female-alone | widow |
| meivak | female-light | fire-light | lamplight |

### 8.2 lo (NEG vs field)
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| lono | field-? | NEG-obey | disobey |
| lopa | NEG-? | field-person | farmer |

### 8.3 khuam (darkness vs pillar)
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| khuamial | khua-mial (town-dark) | khuamial (darkness) | 123x: opaque compound like khuavak |
| khuampi | darkness-big | pillar-big | pillar (44x) |
| innkhuam | house-darkness | house-pillar | doorpost |

---

## 9. Reduplication Notation

| Pattern | Wrong | Correct |
|---------|-------|---------|
| bangbang | bang-bang, what-what | bang~bang, what~REDUP |
| vanvan | van~RED | van~REDUP |

Segmentation uses `~` not `-` for reduplication.

---

## 10. ERG Transparency

These conjunctions now parse transparently (not as atoms):

| Token | Wrong (opaque) | Correct (transparent) |
|-------|----------------|----------------------|
| ciangin | therefore | ciang-in (then-ERG) |
| hangin | because | hang-in (reason-ERG) |
| manin | therefore | man-in (reason-ERG) |
| bangin | like | bang-in (what-ERG) |

---

## 11. Compound Fixes

| Token | Wrong | Correct | Evidence |
|-------|-------|---------|----------|
| kikal | REFL-gate | between | 119x all "between" |
| gukte | almond-PL | six-PL | almond is loanword |
| kidona | sword | REFL-war-LOC (battle) | namsau=sword, kidona=battle |
| zuaunate | rebel-NMLZ-PL | lie-NMLZ-PL | 8x all "lies/falsehood" |
| thangpaih | indignation | pour.out | verb (nominalized = indignation) |

---

## 12. Polysemous Reduplication

| Token | Wrong Default | Correct | Meaning |
|-------|---------------|---------|---------|
| bangbang | god~REDUP | what~REDUP | whatever |
| thuahthuah | house~REDUP | break~REDUP | breach upon breach |
| pakpak | flower~REDUP | quick~REDUP | swift |
| veivei | sick~REDUP | time~REDUP | at one time |
| thumthum | three~REDUP | mourn~REDUP | mourn sore |

---

## Extended Test Suite

```python
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

tests = [
    # 1. IRR marker
    ('ding', 'IRR'),
    # 2. Proper nouns
    ('sin', 'near'), ('Sin', 'SIN'),
    ('lot', 'cast'), ('Lot', 'LOT'),
    # 3. Polysemy
    ('kham', 'gold'), ('kikham', 'REFL-forbid'),
    # 4. Opaque
    ('ahihleh', 'if'), ("ke'n", '1SG.PRO'),
    # 7. Opaque lexemes
    ('lupna', 'bed'), ('zatui', 'medicine'), ('namsau', 'sword'),
    # 8. Homophonous roots
    ('numei', 'woman'), ('meigong', 'widow'), ('meivak', 'lamplight'),
    ('lopa', 'farmer'), ('lono', 'disobey'),
    ('khuampi', 'pillar'), ('khuamial', 'darkness'),  # opaque, like khuavak='light'
    # 10. ERG transparency
    ('ciangin', 'then-ERG'), ('hangin', 'reason-ERG'),
    # 11. Compound fixes
    ('kikal', 'between'), ('kidona', 'battle'),
]

for token, expected in tests:
    seg, gloss = analyze_word(token)
    status = '✓' if expected in gloss else '✗'
    print(f'{status} {token}: {gloss} (expected: {expected})')
```

---

## 13. Stem Over-Parsing (Bug 10)

Short stems (≤3 chars) were greedily matching prefixes of longer words:

| Token | Wrong | Correct | Issue |
|-------|-------|---------|-------|
| angtang | an-gtang (food-?) | angtang | boast |
| awlmang | aw-lmang (cloth-?) | awlmang | spirit |

Fix: `is_remainder_parseable()` validates decompositions.

---

## 14. Phonotactic Violations

Invalid consonant clusters in native words:

| Token | Wrong | Correct | Issue |
|-------|-------|---------|-------|
| kipsak | ki-psak (*ps) | kip-sak | firm-CAUS (establish) |
| kimin | ki-min (*m after ki) | kim-in | fully-ERG |
| kinsak | ki-nsak (*ns) | kin-sak | quickly-CAUS |
| paktat | pa-ktat (*kt) | pak-tat | quick-carry |

**Rule**: Tedim has NO true consonant clusters. Valid digraphs: kh, th, ph, ng only.

---

## 15. Proper Noun Mis-Segmentation

Names with prefix-like beginnings:

| Token | Wrong | Correct | Issue |
|-------|-------|---------|-------|
| Hilkiah | Hi-lkiah (be-?) | HILKIAH | hi = verb |
| Heman | He-man (be.II-?) | HEMAN | he = verb |
| Asa | A-sa (3SG-flesh) | ASA | a = prefix |
| Naomi | Na-omi (2SG.POSS-?) | NAOMI | na = prefix |

---

## 16. Form I/II Verb Alternation

Henderson 1965: Form II (subjunctive) adds -h, -k, -t:

| Form I | Form II | Pattern |
|--------|---------|---------|
| mu | muh | +h (see) |
| za | zak | +k (know) |
| nusia | nusiat | +t (abandon) |
| theih | thei | -h (know) |

VERB_STEM_PAIRS is single source of truth.

---

## 17. TAM Suffix Disambiguation

| Morpheme | Context | Meaning |
|----------|---------|---------|
| sa | after verb | PERF (perfective) |
| sa | standalone | flesh (noun) |
| ta | after verb | PFV (perfective) |
| ta | standalone | child (noun) |
| hi | sentence-final | DECL (declarative) |
| hi | with prefix | be (copula) |

---

## 18. Possessive vs Quotation Mark

| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| Topa' | strip apostrophe | Topa' (LORD.POSS) | possessive |
| gulpi' | strip | gul-pi' (serpent-big.POSS) | compound possessive |

Preserve apostrophe for possessives, strip only for quotation marks.

---

## 19. Semantic Corrections (Spot-Check)

| Token | Wrong | Correct | KJV Evidence |
|-------|-------|---------|--------------|
| lauhlauh | fear~REDUP | rattle~REDUP | onomatopoeia |
| tohtoh | up~REDUP | stand~REDUP | continuously |
| ihmusip | ih-mu-sip | ihmu-sip | sleep-deep |
| nakpau | nose-fat | nakpau | vehemently (lexicalized) |
| kamka | word-bitter | kamka | ashamed (lexicalized) |
| leibeel | lazy.person | leibeel | pot (earthen vessel) |

---

## Full Test Suite

```python
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

tests = [
    # 1. IRR marker
    ('ding', 'IRR'),
    # 2. Proper nouns  
    ('sin', 'near'), ('Sin', 'SIN'),
    ('lot', 'cast'), ('Lot', 'LOT'),
    # 3-4. Polysemy & Opaque
    ('kham', 'gold'), ('kikham', 'REFL-forbid'),
    ('ahihleh', 'if'), ("ke'n", '1SG.PRO'),
    # 7. Opaque lexemes
    ('lupna', 'bed'), ('zatui', 'medicine'), ('namsau', 'sword'),
    # 8. Homophonous roots
    ('numei', 'woman'), ('meigong', 'widow'),
    ('lopa', 'farmer'), ('lono', 'disobey'),
    ('khuampi', 'pillar'), ('khuamial', 'darkness'),  # opaque
    # 10-11. ERG transparency & compounds
    ('ciangin', 'then-ERG'), ('hangin', 'reason-ERG'),
    ('kikal', 'between'), ('kidona', 'battle'),
    # 14. Phonotactics
    ('kipsak', 'firm-CAUS'), ('kimin', 'fully-ERG'),
    # 15. Proper nouns (not mis-segmented)
    ('Hilkiah', 'HILKIAH'), ('Heman', 'HEMAN'),
    # 16. Form I/II
    ('muh', 'see'), ('zak', 'know'),
    # 17. TAM disambiguation
    ('sa', 'flesh'),  # standalone = noun
    # 18. Possessive
    ("gulpi'", 'POSS'),  # should have POSS
    # 19. Semantic fixes
    ('nakpau', 'vehement'), ('kamka', 'asham'),
]

for token, expected in tests:
    seg, gloss = analyze_word(token)
    status = '✓' if expected in gloss else '✗'
    print(f'{status} {token}: {gloss} (expected: {expected})')
```

---

## 20. PAST vs Flesh (-sa suffix)

| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| neihsa | have-flesh | neih-sa (have-PAST) | past tense |
| gensa | tell-flesh | gen-sa (tell-PAST) | past tense |
| bawlsa | do-flesh | bawl-sa (do-PAST) | past tense |
| sa | - | flesh | standalone noun |

---

## 21. Homograph: tuucin (shepherd)

| Token | Wrong | Correct |
|-------|-------|---------|
| tuucin | tuu-cin (throw-rope) | tuucin (shepherd) |
| tuucingte | throw-rope-PL | tuucingte (shepherd-PL) |

**Citation**: Shepherds throughout Gospels.

---

## 22. Prefix Mis-Segmentation

| Token | Wrong | Correct |
|-------|-------|---------|
| innkuan | i-nnkuan (1PL-?) | inn-kuan (house-family) |
| kankhia | ka-nkhia (1SG-?) | kan-khia (we-go.out) |
| angvan | a-ngvan (3SG-?) | ang-van (boast-old) |

---

## 23. Hyphenated Suffix Chains

| Token | Pattern | Analysis |
|-------|---------|----------|
| word-in | explicit hyphen | word-ERG |
| word-ah | explicit hyphen | word-LOC |
| word-a | explicit hyphen | word-LOC |

HYPHEN_SUFFIXES: -in, -ah, -a, -a', -un

---

## 24. in vs inn (ERG vs house)

The standalone word `in` is the ergative case marker (21,383x), NOT 'house'.
The word for 'house' is spelled `inn` with double n (924x).

| Token | Wrong | Correct | Notes |
|-------|-------|---------|-------|
| in | house | ERG | Case marker after nouns |
| inn | ? | house | House (double n) |
| innpi | house | house-big | house-big (= temple) |
| innkuan | ? | house-family | household |

**Citation**: GEN 1:1 "Pasian in" (God ERG = by God)
**Citation**: EXO 12:3 "inn" (house)

---

## 25. TAM Suffix Expansion

These suffixes were added to TAM_SUFFIXES:

| Suffix | Gloss | Category |
|--------|-------|----------|
| thei/theih | ABIL | ability |
| zo | COMPL | completive |
| gawp | INTENS | intensive |
| khin | IMM | immediate |
| kik | ITER | iterative |
| khia/khiat | out/away | directional |
| sak | CAUS | causative |
| zaw | COMPAR | comparative |

---

## 25. Stem Matching Priority

Prefer longer stem match:

| Token | Wrong | Correct | Issue |
|-------|-------|---------|-------|
| mungte | mu-ng-te (see-?-PL) | mung-te (place-PL) | mu=2, mung=4 |
| nungakte | nung-ak-te | nungak-te (girl-PL) | prefer 6-char |

---

## 26. Possessive Plural (-te', -pa')

| Token | Wrong | Correct |
|-------|-------|---------|
| biate' | bia-te-' | bia-te' (worship-PL.POSS) |
| veipa' | vei-pa-' | vei-pa' (sick-AG.POSS) |

---

## 27. Compound Verbs

| Token | Wrong | Correct |
|-------|-------|---------|
| samsiatna | samsia-t-na (destroy-?-NMLZ) | samsiat-na (destroy-NMLZ) |

`samsiat` = compound verb, not samsiat = samsia + t

---

## 28. Punctuation Stripping

| Pattern | Action |
|---------|--------|
| word! | strip ! |
| word!' | strip !' |
| word, | strip , (carefully) |
| word' | preserve (possessive) |

---

## 29. ki- Reflexive Prefix

| Token | Analysis |
|-------|----------|
| kido | ki-do (REFL-fight) |
| kikham | ki-kham (REFL-forbid) |
| kilawm | ki-lawm (REFL-meet) |

---

## Comprehensive Test Suite (50 tests)

```python
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

tests = [
    # 1. IRR marker
    ('ding', 'IRR'),
    ('dingin', 'IRR-ERG'),
    # 2-3. Proper nouns  
    ('sin', 'near'), ('Sin', 'SIN'),
    ('lot', 'cast'), ('Lot', 'LOT'),
    ('Hilkiah', 'HILKIAH'), ('Heman', 'HEMAN'),
    # 4-6. Polysemy, Opaque, Function
    ('kham', 'gold'), ('kikham', 'REFL-forbid'),
    ('ahihleh', 'if'), ("ke'n", '1SG.PRO'),
    ('lupna', 'bed'), ('zatui', 'medicine'),
    # 7-8. Homophonous roots
    ('numei', 'woman'), ('meigong', 'widow'),
    ('lopa', 'farmer'), ('lono', 'disobey'),
    ('khuampi', 'pillar'), ('khuamial', 'darkness'),  # opaque (like khuavak='light')
    # 9-11. ERG, compounds
    ('ciangin', 'then-ERG'), ('hangin', 'because'),  # semantic gloss
    ('kikal', 'middle'),  # transparent: REFL-middle (semantic = between)
    ('kidona', 'fight'),  # transparent: REFL-fight-NMLZ (semantic = battle)
    ('namsau', 'sword'),
    # 12-14. Phonotactics, Form I/II
    ('kipsak', 'firm-CAUS'), ('kimin', 'fully-ERG'),
    ('muh', 'see'), ('zak', 'proclaim'),  # Form II of za
    # 15-16. TAM disambiguation
    ('sa', 'flesh'),
    ("gulpi'", 'POSS'),
    # 17-19. Semantic fixes
    ('nakpau', 'vehement'), ('kamka', 'asham'),
    ('tuucin', 'shepherd'),
    # 20. PAST suffix
    ('neihsa', 'PAST'), ('gensa', 'PAST'),
    # 21-22. Prefix fixes
    ('innkuan', 'house'), ('kankhia', 'exit'),  # kan-khia = firmly-exit
    # 23-24. TAM suffixes
    ('mutheih', 'ABIL'), ('bawlzo', 'COMPL'),
    ('neihgawp', 'INTENS'),
    # 25. Stem priority
    ('mungte', 'place-PL'),
    # 26. Possessive plural
    ("biate'", 'PL.POSS'),
    # 27. Compound verbs
    ('samsiatna', 'destruction'),  # opaque: utter.destruction
    # 28-29. ki- reflexives
    ('kilawm', 'REFL-worthy'),  # worthy/suitable (semantic = meet)
    ('kido', 'fight'),  # can appear without REFL in output
    # 30-35. Reduplication
    ('bangbang', 'REDUP'), ('vanvan', 'REDUP'),
    ('hathat', 'REDUP'),
    # 36-40. More compounds
    ('sanggam', 'brother'), ('zungbuh', 'ring'),
    ('thukham', 'law'), ('lungdam', 'heart'),  # transparent: heart-well
    ('innpi', 'house'),  # transparent: house-big (semantic = temple)
    # 41-45. More suffixes
    ('neihtheih', 'have'),  # have.II-able.II (contains ability concept)
    ('bawlkhin', 'IMM'),
    ('paihkhia', 'go'),  # go-out (both valid)
    ('lutkhiat', 'enter'),
    ('sawlsak', 'CAUS'),
    # 46-50. Final tests
    ('veivei', 'REDUP'), ('thuahthuah', 'REDUP'),
    ('khuavak', 'light'), ('ganhing', 'animal'),  # general term for livestock
    ('suangkhuam', 'pillar'),  # stone-pillar (KJV = "heap and pillar")
    # in vs inn disambiguation (fixed 2026-03-17)
    ('in', 'ERG'),  # 21,383x - ergative case marker, NOT 'house'
    ('inn', 'house'),  # 924x - 'house' has double n
    # hen: JUSS (jussive) vs 'tie' (verb) - polysemous (fixed 2026-03-17)
    ('hen', 'JUSS'),  # 512x standalone - "let/may" (om hen = "let there be")
    ('kihen', 'REFL-tie'),  # ~7x - be bound (Judges 16)
    ('henna', 'tie-NMLZ'),  # ~5x - bond, binding (Ps 2:3)
    ('hente', 'tie-PL'),    # 1x Ruth 2:16 - bundles/handfuls
    ('hi', 'DECL'),   # 35,961x - declarative sentence-final
    ('hiam', 'Q'),    # question marker
]

passed = 0
for token, expected in tests:
    seg, gloss = analyze_word(token)
    ok = expected in gloss
    passed += ok
    status = '✓' if ok else '✗'
    print(f'{status} {token}: {gloss} (expected: {expected})')

print(f'\n{passed}/{len(tests)} tests passed')
```

---
*Last updated: March 2026*
