# A Skeleton Grammar of Tedim Chin

## Based on Morphological Analysis of the Tedim Bible (ctd-x-bible)

*Working document - extracted from morphological analyzer*

---

## 1. Introduction

### 1.1 The Present Work

This skeleton grammar documents the morphological categories extracted from 
a computational analyzer achieving 100% coverage on the Tedim Chin Bible 
(850,906 tokens). Each morpheme is illustrated with examples from narrative 
portions of the Bible.

### 1.2 Corpus

- **Text**: Tedim Chin Bible (ctd-x-bible)
- **Tokens**: 850,906 (100% analyzed)
- **Books**: 66 (Old and New Testaments)
- **Primary example sources**: Genesis, Exodus, Ruth, 1 Samuel, Mark, Luke, Acts

### 1.3 Methodology

Morphemes were identified through:
1. Leipzig-style segmentation of Bible text
2. KJV cross-reference for semantic verification
3. Comparison with Henderson (1965) and other Tedim literature

---

## 2. Phonology (Summary)

### 2.1 Consonants

| Manner | Labial | Alveolar | Palatal | Velar | Glottal |
|--------|--------|----------|---------|-------|---------|
| Stop (vl) | p | t | c [tʃ] | k | (ʔ) |
| Stop (asp) | ph | th | — | kh | — |
| Fricative | — | s | — | — | h |
| Nasal | m | n | — | ng [ŋ] | — |
| Lateral | — | l | — | — | — |
| Rhotic | — | — | — | — | — |
| Glide | v [w] | — | z [j] | — | — |

### 2.2 Vowels

| | Front | Central | Back |
|---|-------|---------|------|
| High | i | — | u |
| Mid | e | — | o |
| Low | — | a | — |

### 2.3 Syllable Structure

Tedim syllables follow the pattern (C)V(V)(C):
- **V**: a (3SG prefix)
- **CV**: ka (1SG prefix), hi (DECL)
- **CVC**: gen (speak), khum (cover)
- **CVVC**: mual (mountain), suan (thread)

---

## 3. Nominal Morphology

### 3.1 Case Markers

#### 3.1.1 Ergative -in

**Form**: -in  
**Gloss**: ERG (ergative)  
**Function**: Marks agent of transitive verb

**Example 1** (Gen 1:1)
```
Pasian in vantung le leitung a piangsak hi
pasian  in   van-tung    le   lei-tung    a-piang-sak          hi
God     ERG  sky-on      and  land-on     3SG-be.born-CAUS     DECL
'God created the heavens and the earth.'
```

**Example 2** (Gen 3:1)
```
Gul in numei tungah "Pasian in..." a ci hi
gul  in   numei  tung-ah  pasian  in   a-ci      hi
snake ERG woman  to-LOC   God     ERG  3SG-say   DECL
'The serpent said to the woman, "Did God..."'
```

#### 3.1.2 Locative -ah

**Form**: -ah  
**Gloss**: LOC (locative)  
**Function**: Location, direction, beneficiary

**Example** (Gen 1:9)
```
tui in mun khatah a kituak sek hen
tui  in   mun   khat-ah   a-ki-tuak             sek  hen
water ERG place one-LOC   3SG-REFL-gather       all  let
'Let the waters be gathered together into one place.'
```

#### 3.1.3 Comitative -tawh

**Form**: -tawh  
**Gloss**: COM (comitative)  
**Function**: Accompaniment, instrument

**Example** (Gen 3:6)
```
a pasal a tawh om lai zong tungah a pia a
a-pasal     a-tawh  om      lai   zong tung-ah  a-pia     a
3SG.POSS-husband 3SG-COM exist still also on-LOC  3SG-give  and
'...and gave also to her husband with her.'
```

#### 3.1.4 Ablative -pan(in)

**Form**: -pan, -panin  
**Gloss**: ABL (ablative)  
**Function**: Source, origin

**Example** (Gen 2:19)
```
Topa Pasian in leilung panin...
topa  pasian  in   lei-lung  pan-in
Lord  God     ERG  land      ABL
'The Lord God formed out of the ground...'
```

### 3.2 Number

#### 3.2.1 Plural -te

**Form**: -te  
**Gloss**: PL (plural)  
**Function**: Marks nominal plurality

**Example** (Gen 1:26)
```
mihingte i bawl ding hi
mi-hing-te       i-bawl     ding  hi
person-life-PL   1PL-make   IRR   DECL
'Let us make mankind...'
```

### 3.3 Demonstratives

#### 3.3.1 Proximal hih

**Form**: hih  
**Gloss**: PROX (proximal demonstrative)

**Example** (Gen 2:23)
```
Hih pen ka guk pan guk ahi hi
hih   pen  ka-guk     pan  guk  a-hi      hi
PROX  TOP  1SG-bone   from bone 3SG-be    DECL
'This is now bone of my bones.'
```

#### 3.3.2 Distal tua

**Form**: tua  
**Gloss**: DIST (distal demonstrative)

**Example** (Gen 2:12)
```
Tua lei ah ngir pha a om hi
tua   lei    ah   ngir.pha  a-om     hi
DIST  land   LOC  gold      3SG-exist DECL
'There is gold in that land.'
```

---

## 4. Pronominal System

### 4.1 Independent Pronouns

| Person | Singular | Plural |
|--------|----------|--------|
| 1 | kei | eite (EXCL), eimite (INCL) |
| 2 | nang | note |
| 3 | amah | amaute |

### 4.2 Pronominal Prefixes

| Person | Form | Gloss |
|--------|------|-------|
| 1SG | ka- | 1SG |
| 2SG | na- | 2SG |
| 3SG | a- | 3SG |
| 1PL.INCL | i- | 1PL.INCL |
| 1PL.EXCL | ei- | 1PL.EXCL |

**Example 1** (Gen 22:2)
```
na tapa a, na it na Abraham Isaac...
na-tapa      a   na-it          na   abraham  isaac
2SG.POSS-son and 2SG-love       2SG  Abraham  Isaac
'your son, whom you love, Abraham... Isaac'
```

### 4.3 Object Prefixes

| Form | Meaning | Function |
|------|---------|----------|
| kong- | 3→1SG | 3rd person acts on 1st singular |
| hong- | 3→1/2 | 3rd person acts on 1st/2nd |

**Example** (Gen 3:13)
```
Gul in hong bum a...
gul  in   hong-bum       a
snake ERG 3→1/2-deceive  and
'The serpent deceived me...'
```

### 4.4 Reflexive Prefix ki-

**Form**: ki-  
**Gloss**: REFL (reflexive/reciprocal)

**Example** (Gen 2:24)
```
a nu le a pa a nusiat a, a zi tawh a kikaih ding hi
a-nu    le  a-pa      a-nusia-t        a   a-zi     tawh a-ki-kaih     ding hi
3SG-mother and 3SG-father 3SG-abandon-II  and 3SG-wife with 3SG-REFL-join IRR DECL
'...shall leave his father and mother and be joined to his wife.'
```

---

## 5. Verbal Morphology

### 5.1 Stem Alternation (Form I / Form II)

Many Tedim verbs have two stem forms. Henderson (1965) terms these "Stem I" and "Stem II."

| Form I | Form II | Gloss | Pattern |
|--------|---------|-------|---------|
| mu | muh | see | V → VC |
| za | zak | hear | V → VC |
| nei | neih | have | VV → VVC |
| gen | genh | speak | VVC → VVCC |
| ci | cih | say | V → VC |
| om | omh | exist | VC → VCC |
| bawl | bawlh | make | VVC → VVCC |

**Form I**: Used in main clauses, with TAM suffixes  
**Form II**: Used in dependent clauses, nominalized forms

**Example** (Gen 1:4)
```
khuavak a muh ciangin...
khuavak  a-muh      ciang-in
light    3SG-see.II when-ERG
'when he saw the light...'
```

### 5.2 Derivational Suffixes

#### 5.2.1 Causative -sak

**Form**: -sak  
**Gloss**: CAUS (causative)  
**Function**: Causative derivation

**Example 1** (Gen 1:1)
```
Pasian in vantung le leitung a piangsak hi
pasian  in   van-tung    le   lei-tung    a-piang-sak          hi
God     ERG  sky-upon    and  land-upon   3SG-be.born-CAUS     DECL
'God created the heavens and the earth.'
```

**Example 2** (Gen 2:7)
```
a nak sung a huisak a, mihing a hinkho hi
a-nak        sung  a-hui-sak        a   mi-hing    a-hin-kho      hi
3SG-nose    into  3SG-blow-CAUS    and person     3SG-live       DECL
'breathed into his nostrils the breath of life'
```

#### 5.2.2 Applicative -pih

**Form**: -pih  
**Gloss**: APPL (applicative)  
**Function**: Introduces applied argument (benefactive, associative)

**Example** (Gen 21:22)
```
Pasian in na bawl khempeuh ah na om pih hi
pasian  in   na-bawl       khempeuh  ah   na-om-pih            hi
God     ERG  2SG-make      all       LOC  2SG-exist-APPL       DECL
'God is with you in all that you do.'
```

#### 5.2.3 Directional Suffixes

##### -khia (out)
**Form**: -khia  
**Gloss**: out

**Example** (Gen 8:18)
```
Noah a suakkhia a...
noah  a-suak-khia        a
Noah  3SG-go.out-out     and
'Noah went out...'
```

##### -lut (in)
**Form**: -lut  
**Gloss**: in

**Example** (Gen 7:1)
```
cimui sungah na lut in
cimui   sung-ah  na-lut       in
ark     in-LOC   2SG-enter    IMP
'Enter into the ark.'
```

##### -to (up/continue)
**Form**: -to  
**Gloss**: up / CONT

**Example** (Gen 2:6)
```
tui a puakto a...
tui   a-puak-to        a
water 3SG-rise-up      and
'A mist went up...'
```

##### -khiat (away)
**Form**: -khiat  
**Gloss**: away

**Example** (Gen 3:24)
```
mihing a hawlkhiat hi
mi-hing    a-hawl-khiat       hi
person     3SG-drive-away     DECL
'He drove out the man.'
```

#### 5.2.4 Iterative/Reversive -kik

**Form**: -kik  
**Gloss**: ITER (iterative/again)

**Example** (Gen 8:21)
```
lei ka supsiat kik nawn ding kei hi
lei   ka-sup-siat-kik      nawn  ding  kei  hi
land  1SG-curse-destroy-ITER CONT  IRR   NEG  DECL
'I will not again curse the ground.'
```

#### 5.2.5 Ability -theih

**Form**: -theih  
**Gloss**: ABIL (ability)

**Example** (Gen 13:16)
```
tawl theih nai lo ahi ciangin
tawl-theih           nai   lo   a-hi     ciang-in
count-ABIL           near  NEG  3SG-be   when-ERG
'...so that it cannot be numbered.'
```

### 5.3 TAM Suffixes

#### 5.3.1 Irrealis -ding

**Form**: -ding  
**Gloss**: IRR (irrealis)  
**Function**: Future, intention, obligation

**Example** (Gen 1:26)
```
mihingte i bawl ding hi
mi-hing-te       i-bawl     ding  hi
person-life-PL   1PL-make   IRR   DECL
'Let us make mankind.'
```

#### 5.3.2 Completive -zo

**Form**: -zo  
**Gloss**: COMPL (completive)

**Example** (Gen 2:2)
```
a nasepna a bawlzo hi
a-na-sep-na            a-bawl-zo        hi
3SG-NMLZ-work-NMLZ     3SG-make-COMPL   DECL
'He completed his work.'
```

#### 5.3.3 Perfective -ta

**Form**: -ta  
**Gloss**: PFV (perfective)

**Example** (Gen 3:7)
```
anni niksuah a nihlai uh hi ti a he ta uh hi
anni  nik-suah    a-ni-lai       uh  hi   ti   a-he-ta             uh  hi
they  eye-open    3SG-be-still   PL  be   COMP 3SG-know-PFV        PL  DECL
'They knew that they were naked.'
```

#### 5.3.4 Continuative -lai

**Form**: -lai  
**Gloss**: still / CONT (continuative)

**Example** (Gen 8:22)
```
lei a om lai sungin...
lei   a-om       lai   sung-in
earth 3SG-exist still while-ERG
'While the earth remains...'
```

### 5.4 Negation

#### 5.4.1 Simple Negation lo

**Form**: lo  
**Gloss**: NEG (negation)

**Example** (Gen 2:5)
```
Topa Pasian in guah lei tungah a guahsak hih lo a
topa pasian in guah lei tung-ah a-guah-sak hih lo a
Lord God ERG rain land on-LOC 3SG-rain-CAUS yet NEG and
'For the Lord God had not caused it to rain.'
```

#### 5.4.2 Emphatic Negation kei

**Form**: kei  
**Gloss**: NEG.EMPH

**Example** (Gen 3:4)
```
Nangma na thi kei ding hi
nangma  na-thi     kei      ding  hi
you     2SG-die    NEG.EMPH IRR   DECL
'You shall surely not die.'
```

---

## 6. Sentence-Final Markers

### 6.1 Declarative hi

**Form**: hi  
**Gloss**: DECL (declarative)

Used at the end of declarative sentences.

### 6.2 Interrogative hiam

**Form**: hiam  
**Gloss**: Q (question)

**Example** (Gen 3:11)
```
na nihlai hi ci kong hilh ka ahi hiam
na-ni-lai       hi   ci    kong-hilh       ka   a-hi    hiam
2SG-naked-still DECL say   3→1-tell        1SG  3SG-be  Q
'Who told you that you were naked?'
```

### 6.3 Topicalizer pen

**Form**: pen  
**Gloss**: TOP (topic marker)

**Example** (Gen 2:23)
```
Hih pen ka guk pan guk ahi hi
hih   pen  ka-guk     pan  guk  a-hi      hi
PROX  TOP  1SG-bone   from bone 3SG-be    DECL
'This is now bone of my bones.'
```

---

## 7. Nominalizers

### 7.1 -na (Nominalization)

**Form**: -na  
**Gloss**: NMLZ (nominalizer)  
**Function**: Creates abstract nouns from verbs

**Example** (Gen 1:1)
```
a kipat cil-in
a-ki-pat              cil-in
3SG-REFL-begin        beginning-ERG
'In the beginning'

(kipat → kipatna 'beginning')
```

### 7.2 -pa / -mi (Agentive)

**Form**: -pa, -mi  
**Gloss**: AG.NMLZ (agentive nominalizer)  
**Function**: Creates agent nouns

**Example**
```
zalsak pa → 'redeemer' (redeem-CAUS + AG)
hong pai mi → 'one who comes' (come + AG)
```

---

## 8. Compounds

### 8.1 Noun-Noun Compounds

| Compound | Analysis | Meaning |
|----------|----------|---------|
| vantung | van-tung (sky-on) | 'heaven' |
| leitung | lei-tung (land-on) | 'earth' |
| lungdam | lung-dam (heart-well) | 'happy' |
| nilam | ni-lam (sun-way) | 'direction of sunrise' |

### 8.2 Semantic Opaque Compounds

Some compounds have meanings not predictable from parts:

| Form | Literal | Actual Meaning |
|------|---------|----------------|
| khuavak | atmosphere-light | 'light' |
| khuamial | atmosphere-dark | 'darkness' |
| zatui | hear.I-water | 'medicine' |
| golhguk | oppose-dig | 'bribe' |

---

## 9. Frequency Summary

| Category | Entries | Top Example | Frequency |
|----------|---------|-------------|-----------|
| Pronominal Prefixes | 5 | a- (3SG) | ~200,000 |
| Case Markers | 5 | -in (ERG) | ~40,000 |
| TAM Suffixes | 50+ | -ding (IRR) | ~25,000 |
| Verb Stems | 650 | hi (be) | ~45,000 |
| Noun Stems | 992 | mi (person) | ~15,000 |
| Proper Nouns | 3,747 | Pasian (God) | ~20,000 |
| Compounds | 581 | leitung (earth) | ~5,000 |

---

## 10. References

Henderson, Eugénie J.A. 1965a. "Tiddim Chin: A descriptive analysis of two texts." 
*London: Oxford University Press*.

Henderson, Eugénie J.A. 1965b. "Tiddim Chin." In *Lingua* 15.

Otsuka, Kosei. Various papers on Tedim verbal morphology.

VanBik, Kenneth. 2009. *Proto-Kuki-Chin*. STEDT Monograph 8.

Zam Ngaih Cing. 2018. *A Grammar of Tedim Chin*. (2 volumes).

---

*Draft generated from analyze_morphemes.py*
*Last updated: 2026-03-17*
