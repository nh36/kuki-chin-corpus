# Chapter 3: Nominal Morphology

*Part of the Tedim Chin Skeleton Grammar*

This chapter documents nominal morphology in Tedim Chin, based on
computational analysis of the Tedim Bible (850,906 tokens, 100% coverage).

---

## 3.1 Overview of the Nominal Domain

Tedim Chin nouns can take the following affixes:

| Position | Affixes | Function |
|----------|---------|----------|
| Prefix | a-, ka-, na-, i-, ei- | Possession |
| Suffix | -te, -uh | Plural |
| Suffix | -in, -ah, -tawh, -pan(in) | Case |
| Suffix | -na, -pa, -mi | Nominalization |

The maximal noun template:
```
POSS.PREFIX + NOUN.STEM + PLURAL + CASE
```

Example: `a-sanggam-te-in` (3SG.POSS-brother-PL-ERG) 'by his brothers'

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

### 3.3.2 Plural -uh

**Form**: -uh  
**Gloss**: PL  
**Function**: Alternative plural marker

#### Example: Ruth 1:8

**Tedim**: Ahih hangin Naomi in a mo nihte kiangah, “Pai un, na inn tuak uhah ciahkik unla, na nute uh tawh om un. A sisate hitaleh kei hitaleh nong limbawl uh mah bangin Topa in note hong limbawl tahen.
**KJV**: And Naomi said unto her two daughters in law, Go, return each to her mother's house: the LORD deal kindly with you, as ye have dealt with the dead, and with me.

| Token | Segmentation | Gloss |
|-------|--------------|-------|
| Ahih | Ahih | be.3SG.REL |
| hangin | hang-in | because-ERG |
| Naomi | Naomi | NAOMI |
| in | in | ERG |
| a | a | 3SG |
| mo | mo | bride |
| nihte | nih-te | two-PL |
| kiangah | kiang-ah | beside-LOC |
| “Pai | Pai | go |
| un | un | PL.IMP |
| na | na | 2SG |
| inn | inn | house |
| tuak | tuak | receive |
| uhah | uhah | PL.LOC |
| ciahkik | ciah-kik | return-ITER |
| unla | un-la | PL.IMP-and |
| na | na | 2SG |
| nute | nu-te | female-PL |
| uh | uh | PL |
| tawh | tawh | COM |
| om | om | exist |
| un | un | PL.IMP |
| A | A | 3SG |
| sisate | si-sa-te | blood-PAST-PL |
| hitaleh | hitaleh | if.so |
| kei | kei | NEG.EMPH |
| hitaleh | hitaleh | if.so |
| nong | nong | 2→1 |
| limbawl | limbawl | prepare |
| uh | uh | PL |
| mah | mah | EMPH |
| bangin | bang-in | like-ERG |
| Topa | Topa | Lord |
| in | in | ERG |
| note | note | 2PL.PRO |
| hong | hong | 3→1 |
| limbawl | limbawl | prepare |
| tahen | tahen | amen |

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
| Plural | -te | PL | ~25,000 |
| Plural | -uh | PL | ~5,000 |
| Proximal dem | hih | PROX | ~2,000 |
| Distal dem | tua | DIST | ~3,500 |

---

*Chapter 3 generated from analyze_morphemes.py*
*Last updated: March 2026*
