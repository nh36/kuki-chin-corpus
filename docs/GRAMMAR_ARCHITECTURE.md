# Tedim Chin Grammar Architecture

Organizing morphological analyzer output into a coherent grammatical description.

## Overview

The analyzer data can be structured into the following grammatical domains:

```
1. Phonology
   1.1 Phoneme inventory
   1.2 Syllable structure
   1.3 Tone (limited evidence)

2. Morphology
   2.1 Nominal domain
       - Noun stems
       - Case markers
       - Number (plural)
       - Possession
       - Determiners/demonstratives
   
   2.2 Verbal domain
       - Verb stems (Form I/II)
       - Pronominal prefixes
       - Derivational suffixes
       - TAM suffixes
       - Directional suffixes
   
   2.3 Other categories
       - Function words
       - Particles
       - Conjunctions
       - Question words

3. Syntax (requires parsed sentences - future work)
```

---

## 1. Phonology

### 1.1 Phoneme Inventory (from orthography)

**Consonants:**

| Manner | Labial | Alveolar | Palatal | Velar | Glottal |
|--------|--------|----------|---------|-------|---------|
| Stop (vl) | p | t | c | k | ' |
| Stop (asp) | ph | th | - | kh | - |
| Nasal | m | n | - | ng | - |
| Fricative | - | s | - | - | h |
| Affricate | - | z | - | - | - |
| Lateral | - | l | - | - | - |
| Rhotic | - | - | - | - | - |
| Glide | w | - | y | - | - |

**Vowels:**

| Height | Front | Central | Back |
|--------|-------|---------|------|
| High | i | - | u |
| Mid | e | - | o |
| Low | - | a | - |

**Diphthongs:** ai, au, ei, ia, ua, etc.

### 1.2 Syllable Structure

Basic template: (C)(C)V(V)(C)

- Onset: Single C or CC clusters (limited: kh, ph, th, etc.)
- Nucleus: V or VV (diphthong)
- Coda: Single C (p, t, k, m, n, ng, l, h)

---

## 2. Morphology

### 2.1 Nominal Domain

#### Noun Stems (992 in analyzer)

Categories:
- Body parts: lung 'heart', khe 'foot', lu 'head'
- Kinship: pa 'father', nu 'mother', tapa 'son'
- Nature: tui 'water', mei 'fire', khua 'village'
- Abstract: thu 'word', na 'illness', lam 'way'

#### Case Markers

| Marker | Function | Example |
|--------|----------|---------|
| -in | ERG/INSTR | mi-in 'person-ERG' |
| -ah | LOC | inn-ah 'house-LOC' |
| -tawh | COM | amah-tawh '3SG-COM' |
| -pan | ABL | Jerusalem-pan 'from Jerusalem' |

#### Number

| Marker | Function | Example |
|--------|----------|---------|
| -te | PL | mi-te 'people' |
| khat | one | mi khat 'one person' |
| nih | two | ni-nih 'two days' |

#### Possession

| Marker | Function | Example |
|--------|----------|---------|
| ka- | 1SG.POSS | ka-inn 'my house' |
| na- | 2SG.POSS | na-inn 'your house' |
| a- | 3SG.POSS | a-inn 'his/her house' |
| -' | POSS marker | Topa' 'Lord's' |

#### Determiners

| Word | Gloss | Example |
|------|-------|---------|
| hih | this (PROX) | hih mi 'this person' |
| tua | that (MED) | tua mi 'that person' |
| kha | that (DIST) | kha mi 'that person (far)' |

### 2.2 Verbal Domain

#### Verb Stems (650 in analyzer)

**Form I vs Form II:**

| Meaning | Form I | Form II | Context |
|---------|--------|---------|---------|
| see | mu | muh | I before V, II before C |
| have | nei | neih | |
| know | thei | theih | |
| hear | za | zak | |

#### Pronominal Prefixes

| Prefix | Subject | Example |
|--------|---------|---------|
| ka- | 1SG | ka-mu 'I see' |
| na- | 2SG | na-mu 'you see' |
| a- | 3SG | a-mu 'he/she sees' |
| i- | 1PL.INCL | i-mu 'we (incl.) see' |
| ei- | 1PL.EXCL | ei-mu 'we (excl.) see' |

#### Object Prefixes

| Prefix | Object | Example |
|--------|--------|---------|
| kong- | 3→1 | kong-mu 'he sees me' |
| hong- | 3→1/2 | hong-mu 'he sees me/you' |

#### Derivational Suffixes

| Suffix | Function | Example | Gloss |
|--------|----------|---------|-------|
| -sak | CAUS | mu-sak | see-CAUS = 'show' |
| -pih | APPL | pai-pih | go-APPL = 'go.with' |
| -kik | REVERT | lam-kik | build-REVERT = 'rebuild' |
| -na | NMLZ | gen-na | speak-NMLZ = 'speech' |
| -pa | AG.NMLZ | gen-pa | speak-AG = 'speaker' |

#### TAM Suffixes

| Suffix | Function | Example | Gloss |
|--------|----------|---------|-------|
| -ding | IRR | pai-ding | go-IRR = 'will go' |
| -zo | COMPL | bawl-zo | do-COMPL = 'finished doing' |
| -ta | PFV | pai-ta | go-PFV = 'already went' |
| -khin | IMM | pai-khin | go-IMM = 'go right now' |
| -lai | CONT | pai-lai | go-CONT = 'going' |
| -sa | PERF | muh-sa | see-PERF = 'has seen' |

#### Directional Suffixes

| Suffix | Direction | Example | Gloss |
|--------|-----------|---------|-------|
| -khia | out | pai-khia | go-out = 'go out' |
| -lut | in | pai-lut | go-in = 'enter' |
| -to | up | kah-to | climb-up = 'ascend' |
| -khiat | away | pai-khiat | go-away = 'depart' |

### 2.3 Other Categories

#### Function Words (131 in analyzer)

| Category | Examples |
|----------|----------|
| Pronouns | ka, na, a, i, ei, keimah, nangmah |
| Demonstratives | hih, tua, kha |
| Question words | bang, koi, kuamah |
| Negation | lo, kei |
| Conjunctions | le, leh, ahih |

#### Particles

| Particle | Function | Example |
|----------|----------|---------|
| hi | DECL | ... hi = declarative |
| hiam | Q | ... hiam? = question |
| dah | EMPH | ... dah = emphasis |

---

## 3. Morphological Templates

### Noun Phrase

```
(DET) (POSS-) NOUN (-PL) (-CASE)

Examples:
- hih ka-inn-te-ah = this 1SG.POSS-house-PL-LOC = "in these my houses"
- mi-te-in = person-PL-ERG = "the people (as subject)"
```

### Verb Complex

```
(OBJ.PREFIX-) (SUBJ.PREFIX-) STEM (-DERIV)* (-TAM)* (-CASE)

Examples:
- hong-gen-sak-ding = 3→1-speak-CAUS-IRR = "will tell me"
- ka-pai-khia-zo = 1SG-go-out-COMPL = "I have gone out"
- ki-bawl-pih-na = REFL-do-APPL-NMLZ = "mutual cooperation"
```

### Suffix Ordering

```
ROOT + DERIV + INFL

DERIV order: -sak/-pih/-kik + -khia/-lut/-to + -theih/-gawp
INFL order:  -na/-pa + -te + -in/-ah

Example: gen-sak-na-te-in = speak-CAUS-NMLZ-PL-ERG
```

---

## 4. Implementation Status

| Domain | Analyzer Coverage | Notes |
|--------|-------------------|-------|
| Noun stems | ✓ 992 entries | |
| Verb stems | ✓ 650 entries | Form I/II pairs |
| Case markers | ✓ Productive | -in, -ah, -tawh, -pan |
| TAM | ✓ Productive | -ding, -zo, -ta, -khin |
| Derivation | ✓ Productive | -sak, -pih, -na, -pa |
| Compounds | ✓ 581 entries | BINARY + TERNARY |
| Proper nouns | ✓ 3747 entries | Biblical names |
| Polysemy | ✓ 37 entries | AMBIGUOUS_MORPHEMES |

---

*Last updated: 2026-03-17*
*Source: scripts/analyze_morphemes.py*
