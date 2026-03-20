# Chapter 3: Nominal Morphology

*Part of the Tedim Chin Skeleton Grammar*

This chapter documents nominal morphology in Tedim Chin, based on
computational analysis of the Tedim Bible (850,906 tokens, 100% coverage).

---

## 3.1 Noun Phrase Structure

Before examining individual morphemes, we present the overall structure of
the Tedim Chin noun phrase (NP).

### 3.1.1 Basic NP Template

The maximal noun phrase follows this template:

```
(DEM) + (POSS) + NOUN + (NUM) + (PL) + (CASE)
```

Where:
- **DEM**: Demonstrative (tua, hih, etc.)
- **POSS**: Possessive prefix (a-, ka-, na-, i-)
- **NOUN**: The noun stem
- **NUM**: Numeral (khat, nih, thum...)
- **PL**: Plural suffix -te
- **CASE**: Case marker (-in, -ah, -tawh, -panin)

Note: The 2nd/3rd person plural agreement clitic `uh` is NOT a noun plural
marker. It appears VP-finally to mark plural agreement with 2nd/3rd person
subjects/possessors (see Chapter 5).

### 3.1.2 Paradigm: "father" (pa)

| Form | Segmentation | Gloss | English |
|------|--------------|-------|---------|
| pa | pa | father | 'father' |
| pa-in | pa-in | father-ERG | 'by (the) father' |
| a pa | a pa | 3SG father | 'his/her father' |
| ka pa | ka pa | 1SG father | 'my father' |
| na pa | na pa | 2SG father | 'your father' |
| a pa-in | a pa-in | 3SG father-ERG | 'by his father' |
| pate | pa-te | father-PL | 'fathers' |
| a pate | a pa-te | 3SG father-PL | 'their fathers' |

#### Example: Gen 2:24

**Tedim**: Tua thu hangin pasal in a nu le a pa nusia-in a zi tawh kigawm

**KJV**: Therefore shall a man leave his father and his mother, and cleave unto his wife

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Tua | Tua | that |
| thu | thu | word |
| hangin | hang-in | because-ERG |
| pasal | pasal | husband |
| in | in | ERG |
| a | a | 3SG |
| nu | nu | mother |
| le | le | and |
| a | a | 3SG |
| pa | pa | father |
| nusia-in | nusia-in | abandon-ERG |
| a | a | 3SG |
| zi | zi | wife |
| tawh | tawh | COM |
| kigawm | ki-gawm | REFL-seize |

Note: `a nu le a pa` = "his mother and his father" - possessive `a-` precedes each noun

### 3.1.3 Paradigm: "house" (inn)

| Form | Segmentation | Gloss | English |
|------|--------------|-------|---------|
| inn | inn | house | 'house' |
| inn-ah | inn-ah | house-LOC | 'in/at the house' |
| inn-in | inn-in | house-ERG | 'by the house' |
| a inn | a inn | 3SG house | 'his/her house' |
| ka inn | ka inn | 1SG house | 'my house' |
| innte | inn-te | house-PL | 'houses' |
| innsung | inn-sung | house-inside | 'inside the house' |
| innsungah | inn-sung-ah | house-inside-LOC | 'in the interior of the house' |
| biakinn | biak-inn | worship-house | 'temple' |

#### Example: Gen 19:2

**Tedim**: ... tua ni zanin no' pa inn-ah na hawh ding uh hi

**KJV**: ... tarry all night ... in your servant's house

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| no' | no' | 2PL.POSS |
| pa | pa | male |
| inn-ah | inn-ah | house-LOC |
| na | na | 2SG |
| hawh | hawh | stay |
| ding | ding | PROSP |
| uh | uh | 2/3PL |
| hi | hi | DECL |

### 3.1.4 Paradigm: "person" (mi)

| Form | Segmentation | Gloss | English |
|------|--------------|-------|---------|
| mi | mi | person | 'person' |
| mite | mi-te | person-PL | 'people' |
| mi-in | mi-in | person-ERG | 'by a person' |
| mipa | mi-pa | person-male | 'man (male person)' |
| numei | nu-mei | female-? | 'woman' |

### 3.1.5 Complex NPs

Tedim allows stacking of modifiers and embedding of possessive NPs:

#### Example: Gen 17:16 - Multiple embedded possessors

**Tedim**: Mihingte' kumpite ama sung pan hong piangkhia ding hi

**KJV**: kings of people shall be of her

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Mihingte' | mihing-te' | human-PL.POSS |
| kumpite | kumpi-te | king-PL |
| ama | ama | 3SG.POSS |
| sung | sung | inside |
| pan | pan | from |
| hong | hong | 3→1 |
| piangkhia | piang-khia | be.born-EXIT |
| ding | ding | PROSP |
| hi | hi | DECL |

Analysis: `Mihingte' kumpite` = "kings of people" (genitive with ')

---

## 3.2 Case Markers

Tedim has a split-ergative case system. Agents of transitive verbs take
the ergative marker `-in`, while patients and intransitive subjects are unmarked.

### 3.2.1 Ergative -in

**Form**: -in (also spelled -'n after vowels)  
**Gloss**: ERG  
**Frequency**: ~22,000 occurrences  
**Function**: Marks agent of transitive verb, instrument, cause

#### Example 1: Gen 1:1

**Tedim**: A kipat cil-in Pasian in vantung le leitung a piangsak hi.
**KJV**: In the beginning God created the heaven and the earth.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| A | A | 3SG |
| kipat | ki-pat | beginning |
| cil-in | cil-in | begin-ERG |
| Pasian | Pasian | God |
| in | in | ERG |
| vantung | van-tung | sky-on |
| le | le | and |
| leitung | lei-tung | land-on |
| a | a | 3SG |
| piangsak | piangsak | cause.birth |
| hi | hi | DECL |

In this example, `Pasian in` shows the agent 'God' marked with ERG.

#### Example 2: Gen 1:3

**Tedim**: Pasian in, “Khuavak om hen,” ci hi; tua ciangin khuavak om pah hi.
**KJV**: And God said, Let there be light: and there was light.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Pasian | Pasian | God |
| in | in | ERG |
| “Khuavak | Khuavak | light |
| om | om | exist |
| hen” | hen | JUSS |
| ci | ci | say |
| hi; | hi | DECL |
| tua | tua | that |
| ciangin | ciang-in | then-ERG |
| khuavak | khuavak | light |
| om | om | exist |
| pah | pah | do.so |
| hi | hi | DECL |

Here `Pasian in` again marks God as the agent of the speech act.
Note also `hen` (JUSS) marking jussive mood: "let there be light."

#### Example 3: Gen 3:1

**Tedim**: Tu-in gulpi pen, Topa Pasian' bawlsa gamlak ganhing dangte khempeuh sangin ngiansiam zaw hi. Amah in numei kiangah, “Pasian in, 'Huan sung singgah khat peuhpeuh ne lo ding,' hong ci ahi hiam?” ci hi.
**KJV**: Now the serpent was more subtil than any beast of the field which the LORD God had made. And he said unto the woman, Yea, hath God said, Ye shall not eat of every tree of the garden?

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Tu-in | Tu-in | now-ERG |
| gulpi | gul-pi | serpent-great |
| pen | pen | TOP |
| Topa | Topa | Lord |
| Pasian | Pasian | God |
| bawlsa | bawl-sa | make-PAST |
| gamlak | gam-lak | land-midst |
| ganhing | ganhing | animal |
| dangte | dang-te | other-PL |
| khempeuh | khempeuh | all |
| sangin | sang-in | high-ERG |
| ngiansiam | ngian-siam | cunning-make |
| zaw | zaw | more |
| hi | hi | DECL |
| Amah | Amah | 3SG.PRO |
| in | in | ERG |
| numei | nu-mei | woman |
| kiangah | kiang-ah | beside-LOC |
| “Pasian | Pasian | God |
| in | in | ERG |
| Huan | huan | bread |
| sung | sung | inside |
| singgah | singgah | hang |
| khat | khat | one |
| peuhpeuh | peuhpeuh | every |
| ne | ne | eat |
| lo | lo | NEG |
| ding | ding | IRR |
| hong | hong | 3→1 |
| ci | ci | say |
| ahi | ahi | be.3SG |
| hiam?” | hiam | Q |
| ci | ci | say |
| hi | hi | DECL |

### 3.2.2 Locative -ah

**Form**: -ah  
**Gloss**: LOC  
**Frequency**: ~15,000 occurrences  
**Function**: Location, goal of motion, temporal setting

#### Example 1: Gen 1:9

**Tedim**: Pasian in, “Vantungte nuai-a om tuite mun khatah kikhawm hen la, lei keu kidawk hen,” ci hi. Tua mah bangin a piang pah hi.
**KJV**: And God said, Let the waters under the heaven be gathered together unto one place, and let the dry land appear: and it was so.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Pasian | Pasian | God |
| in | in | ERG |
| “Vantungte | van-tung-te | heavens |
| nuai-a | nuai-a | below-LOC |
| om | om | exist |
| tuite | tui-te | water-PL |
| mun | mun | place |
| khatah | khat-ah | one-LOC |
| kikhawm | kik-hawm | ITER-together |
| hen | hen | JUSS |
| la | la | take |
| lei | lei | buy |
| keu | keu | dry |
| kidawk | ki-dawk | REFL-dry |
| hen” | hen | JUSS |
| ci | ci | say |
| hi | hi | DECL |
| Tua | Tua | that |
| mah | mah | EMPH |
| bangin | bang-in | like-ERG |
| a | a | 3SG |
| piang | piang | be.born |
| pah | pah | do.so |
| hi | hi | DECL |

#### Example 2: Gen 2:8

**Tedim**: Topa Pasian in nisuahna lamah Eden huan khat bawl hi. Tua lai munah ama bawlsa mipa koih hi.
**KJV**: And the LORD God planted a garden eastward in Eden; and there he put the man whom he had formed.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Topa | Topa | Lord |
| Pasian | Pasian | God |
| in | in | ERG |
| nisuahna | ni-suah-na | day-birth-NMLZ |
| lamah | lam-ah | DIR-LOC |
| Eden | Eden | EDEN |
| huan | huan | bread |
| khat | khat | one |
| bawl | bawl | make |
| hi | hi | DECL |
| Tua | Tua | that |
| lai | lai | midst |
| munah | mun-ah | place-LOC |
| ama | ama | 3SG.POSS |
| bawlsa | bawl-sa | make-PAST |
| mipa | mipa | man |
| koih | koih | put |
| hi | hi | DECL |

### 3.2.3 Comitative -tawh

**Form**: -tawh  
**Gloss**: COM  
**Frequency**: ~3,000 occurrences  
**Function**: Accompaniment, instrument

#### Example: Gen 3:6

**Tedim**: Tua ahih ciangin singkung a hoihna, mi a pilsak dingin tua a gah a deihhuaina a muh ciangin, a singgah loin a ne hi. Amah in singgah kimkhat a pasal pia a, a pasal in zong a ne hi.
**KJV**: And when the woman saw that the tree was good for food, and that it was pleasant to the eyes, and a tree to be desired to make one wise, she took of the fruit thereof, and did eat, and gave also unto her husband with her; and he did eat.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Tua | Tua | that |
| ahih | ahih | be.3SG.REL |
| ciangin | ciang-in | then-ERG |
| singkung | sing-kung | tree |
| a | a | 3SG |
| hoihna | hoih-na | good-NMLZ |
| mi | mi | person |
| a | a | 3SG |
| pilsak | pil-sak | learn-CAUS |
| dingin | ding-in | IRR-ERG |
| tua | tua | that |
| a | a | 3SG |
| gah | gah | branch |
| a | a | 3SG |
| deihhuaina | deih-huai-na | want-dread-NMLZ |
| a | a | 3SG |
| muh | muh | see |
| ciangin | ciang-in | then-ERG |
| a | a | 3SG |
| singgah | singgah | hang |
| loin | lo-in | NEG-ERG |
| a | a | 3SG |
| ne | ne | eat |
| hi | hi | DECL |
| Amah | Amah | 3SG.PRO |
| in | in | ERG |
| singgah | singgah | hang |
| kimkhat | kimkhat | half |
| a | a | 3SG |
| pasal | pasal | husband |
| pia | pia | give |
| a | a | 3SG |
| a | a | 3SG |
| pasal | pasal | husband |
| in | in | ERG |
| zong | zong | also |
| a | a | 3SG |
| ne | ne | eat |
| hi | hi | DECL |

### 3.2.4 Ablative -pan / -panin

**Form**: -pan, -panin  
**Gloss**: ABL  
**Frequency**: ~2,500 occurrences  
**Function**: Source, origin, starting point

#### Example: Gen 2:7

**Tedim**: Topa Pasian in leilak pana leivui tawh mihing bawl a, a nak sungah nuntakna hu sang suk hi. Tua mi pen leitung nuntakna a nei mihing hong suak pah hi.
**KJV**: And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life; and man became a living soul.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Topa | Topa | Lord |
| Pasian | Pasian | God |
| in | in | ERG |
| leilak | lei-lak | dust |
| pana | pa-na | father-NMLZ |
| leivui | leivui | dust |
| tawh | tawh | COM |
| mihing | mi-hing | person-kind |
| bawl | bawl | make |
| a | a | 3SG |
| a | a | 3SG |
| nak | nak | nose |
| sungah | sung-ah | inside-LOC |
| nuntakna | nuntak-na | live-NMLZ |
| hu | hu | help |
| sang | sang | high |
| suk | suk | collapse |
| hi | hi | DECL |
| Tua | Tua | that |
| mi | mi | person |
| pen | pen | TOP |
| leitung | lei-tung | land-on |
| nuntakna | nuntak-na | live-NMLZ |
| a | a | 3SG |
| nei | nei | have |
| mihing | mi-hing | person-kind |
| hong | hong | 3→1 |
| suak | suak | wither |
| pah | pah | do.so |
| hi | hi | DECL |

---

## 3.3 Number

### 3.3.1 Plural -te

**Form**: -te  
**Gloss**: PL  
**Frequency**: ~25,000 occurrences  
**Function**: Marks plural nouns

#### Example: Gen 1:26

**Tedim**: Tua ciangin Pasian in, “Eima lim, eimah hong sunin mihing bawl ni. Tuipi ngasate tung, huihlak vasate tung, ganhingte tung, le leitung a a bokvakte khempeuh tungah ukna neisak ni,” a ci hi.
**KJV**: And God said, Let us make man in our image, after our likeness: and let them have dominion over the fish of the sea, and over the fowl of the air, and over the cattle, and over all the earth, and over every creeping thing that creepeth upon the earth.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Tua | Tua | that |
| ciangin | ciang-in | then-ERG |
| Pasian | Pasian | God |
| in | in | ERG |
| “Eima | Eima | EIMA |
| lim | lim | sign |
| eimah | ei-mah | 1PL.EXCL-EMPH |
| hong | hong | 3→1 |
| sunin | sun-in | during-ERG |
| mihing | mi-hing | person-kind |
| bawl | bawl | make |
| ni | ni | day |
| Tuipi | tui-pi | water-big |
| ngasate | ngasa-te | fish-PL |
| tung | tung | on |
| huihlak | huihlak | air |
| vasate | va-sa-te | go.and-PAST-PL |
| tung | tung | on |
| ganhingte | ganhingte | animals |
| tung | tung | on |
| le | le | and |
| leitung | lei-tung | land-on |
| a | a | 3SG |
| a | a | 3SG |
| bokvakte | bok-vak-te | creep-creature-PL |
| khempeuh | khempeuh | all |
| tungah | tung-ah | on-LOC |
| ukna | ukna | rule.NMLZ |
| neisak | nei-sak | have-CAUS |
| ni” | ni | day |
| a | a | 3SG |
| ci | ci | say |
| hi | hi | DECL |

### 3.3.2 Agreement Clitic -uh (NOT a noun plural)

**IMPORTANT**: The clitic `uh` is NOT a noun plural marker. It is a **2nd/3rd
person plural agreement marker** that appears at the VP boundary.

**Form**: uh (standalone word or clitic)  
**Gloss**: 2/3PL (2nd/3rd person plural agreement)  
**Function**: Marks plural agreement with 2nd or 3rd person subject/possessor

The distribution of `uh` is as follows:
- It appears after verbs to agree with a plural subject
- It appears in possessive NPs like `na X uh` to mark "your (PL) X"
- It is DISTINCT from noun plural `-te`

#### Example: Ruth 1:8

**Tedim**: "Pai un, na inn tuak uhah ciahkik unla, na nute uh tawh om un."

**KJV**: "Go, return each to her mother's house... with your mothers..."

| Token | Segmentation | Gloss | Note |
|-------|--------------|-------|------|
| Pai | Pai | go | verb |
| un | un | IMP.PL | 2PL imperative |
| na | na | 2SG | possessive (but with uh = 2PL) |
| inn | inn | house | noun |
| tuak | tuak | each | modifier |
| uhah | uh-ah | 2/3PL-LOC | **agreement**, not plural |
| ciahkik | ciah-kik | return-ITER | verb |
| unla | un-la | IMP.PL-and | 2PL imperative |
| na | na | 2SG | possessive |
| nute | nu-te | mother-**PL** | **noun plural with -te** |
| uh | uh | 2/3PL | **agreement clitic** |
| tawh | tawh | COM | comitative |
| om | om | exist | verb |
| un | un | IMP.PL | 2PL imperative |

**Analysis**: Notice how `nute` is the noun plural (mothers) marked with `-te`,
while `uh` is the agreement marker agreeing with the 2PL possessor `na`. The
pattern `na nute uh` means "your (plural) mothers" where:
- `na` = 2SG possessive prefix (singular form)
- `nute` = mother-PL (noun plural)
- `uh` = 2/3PL agreement (marks that "your" is actually plural)

This discontinuous pattern `na...uh` is the standard way to express 2PL possession.

---

## 3.4 Possession

### 3.4.1 Possessive Prefixes

| Person | Prefix | Example |
|--------|--------|---------|
| 1SG | ka- | ka-tapa 'my son' |
| 2SG | na- | na-zi 'your wife' |
| 3SG | a- | a-pa 'his father' |
| 1PL.INCL | i- | i-Pasian 'our God' |
| 1PL.EXCL | ei- | ei-gam 'our land' |

#### Example: Gen 22:2

**Tedim**: Amah in, “Na it, na tapa neihsun Isaac, la inla Moriah gamah pai in. Tua lai mun a nang kiangah kong gen ding mual khat tungah meihal biakpiakna-in amah hong pia in,” a ci hi.
**KJV**: And he said, Take now thy son, thine only son Isaac, whom thou lovest, and get thee into the land of Moriah; and offer him there for a burnt offering upon one of the mountains which I will tell thee of.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Amah | Amah | 3SG.PRO |
| in | in | ERG |
| “Na | Na | 2SG |
| it | it | love |
| na | na | 2SG |
| tapa | ta-pa | child-male |
| neihsun | neih-sun | have.II-long |
| Isaac | Isaac | ISAAC |
| la | la | take |
| inla | inla | and.then |
| Moriah | Moriah | MORIAH |
| gamah | gam-ah | land-LOC |
| pai | pai | go |
| in | in | ERG |
| Tua | Tua | that |
| lai | lai | midst |
| mun | mun | place |
| a | a | 3SG |
| nang | nang | 2SG.PRO |
| kiangah | kiang-ah | beside-LOC |
| kong | kong | 1SG→3 |
| gen | gen | speak |
| ding | ding | IRR |
| mual | mual | mountain |
| khat | khat | one |
| tungah | tung-ah | on-LOC |
| meihal | meihal | burnt.offering |
| biakpiakna-in | biak-piak-na-in | worship-give.to-NMLZ-ERG |
| amah | amah | 3SG.PRO |
| hong | hong | 3→1 |
| pia | pia | give |
| in” | in | ERG |
| a | a | 3SG |
| ci | ci | say |
| hi | hi | DECL |

---

## 3.5 Demonstratives

### 3.5.1 Proximal hih

**Form**: hih  
**Gloss**: PROX  
**Function**: 'this' (near speaker)

### 3.5.2 Distal tua

**Form**: tua  
**Gloss**: DIST  
**Function**: 'that' (away from speaker)

#### Example: Gen 2:23

**Tedim**: Tua ciangin mipa in, “Tu petpetin hih pen keima guhte le keima sate ahi hi. Amah pen mipa sung panin a kilakhia ahih manin 'Numei' kici ding hi,” a ci hi.
**KJV**: And Adam said, This is now bone of my bones, and flesh of my flesh: she shall be called Woman, because she was taken out of Man.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Tua | Tua | that |
| ciangin | ciang-in | then-ERG |
| mipa | mipa | man |
| in | in | ERG |
| “Tu | Tu | now |
| petpetin | pet-pet-in | bone-bone-ERG |
| hih | hih | this |
| pen | pen | TOP |
| keima | keima | 1SG.self |
| guhte | guh-te | bone-PL |
| le | le | and |
| keima | keima | 1SG.self |
| sate | sa-te | flesh-PL |
| ahi | ahi | be.3SG |
| hi | hi | DECL |
| Amah | Amah | 3SG.PRO |
| pen | pen | TOP |
| mipa | mipa | man |
| sung | sung | inside |
| panin | panin | ABL |
| a | a | 3SG |
| kilakhia | kila-khia | woman-EXIT |
| ahih | ahih | be.3SG.REL |
| manin | man-in | reason-ERG |
| Numei | nu-mei | woman |
| kici | kici | called |
| ding | ding | IRR |
| hi” | hi | DECL |
| a | a | 3SG |
| ci | ci | say |
| hi | hi | DECL |

---

## 3.6 Summary Table

| Category | Form | Gloss | Frequency |
|----------|------|-------|-----------|
| ERG case | -in | ERG | ~22,000 |
| LOC case | -ah | LOC | ~15,000 |
| COM case | -tawh | COM | ~3,000 |
| ABL case | -pan(in) | ABL | ~2,500 |
| Noun plural | -te | PL | ~25,000 |
| 2/3PL agreement | uh | 2/3PL | ~22,000 |
| Proximal dem | hih | PROX | ~2,000 |
| Distal dem | tua | DIST | ~3,500 |

---

*Chapter 3 generated from analyze_morphemes.py*
*Last updated: March 2026*
