---
title: "Tedim Pronoun Clusivity Dossier"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

# Scope

This dossier tests the first-person plural clusivity labels in the Tedim pronoun materials before any change is made to the generated pronoun report. It distinguishes direct source evidence, repository literature-review summaries, generated-report claims, and later editorial inference. It also checks a manually classified sample from the Tedim Bible corpus. The generated pronoun report is **not** changed in this task.

# Source claims

## Direct source evidence

### Henderson 1965

The key direct Henderson passage is the pronominal-concord discussion on printed pp. 32--33, represented in the repository OCR at `literature/tedim-ctd/ocr/henderson_65a_text/page-22.txt` [@henderson1965, 32-33].

> "For all nominal forms except `kei, keimah`, &c., I, `nang, nangmah`, &c., you, `ei, eite`, &c., we, `ko, kote`, &c., we, `no, note`, &c., you, concord obtains with the pronominal prefix `a-`. For the words listed above, the concordant pronominal prefixes are `ka-, na-, i-, ka-, and na-` respectively." [@henderson1965, 32-33]

This direct passage does two things clearly. First, it groups `ei, eite` separately from `ko, kote`. Second, it maps those two groups to different concord prefixes: `i-` for `ei/eite`, `ka-` for `ko/kote`. What it does **not** do in the quoted passage is explicitly gloss one group as *inclusive* and the other as *exclusive*. In the repository OCR for Henderson 1965, the clusivity terminology itself does not appear in the pronoun passage; the inclusive/exclusive reading is therefore an inference drawn from the system, not a quoted Henderson label.

### Zam Ngaih Cing

The directly extracted PDF text for Zam Ngaih Cing's thesis states that Tedim has a first-person plural distinction "in terms of inclusivity and exclusivity" [@zamngaihcing2017, sec. 3.2.1]:

> "The first person plural is further distinguished in terms of inclusivity and exclusivity as shown in Table 21." [@zamngaihcing2017, sec. 3.2.1]

However, the directly extracted table text is internally unstable. In the extracted Table 21, both plural first-person forms are given as inclusive:

> "First: keí 'I'; ì 'us (incl.)'; eí 'us (incl.)'" [@zamngaihcing2017, sec. 3.2.1]

The directly extracted possessive table is also unstable:

> "First: kà 'my'; ì 'our (excl.)'; eí 'us(incl.)'" [@zamngaihcing2017, sec. 3.2.2]

The direct ZNC evidence therefore supports the existence of a clusivity distinction in Tedim, but it does **not** straightforwardly confirm the Henderson-style mapping `ei/eite` versus `ko/kote`. The extracted text available in the repository is internally inconsistent and uses forms (`ì`, `eí`) that do not directly settle the `eite` versus `kote` question.

## Repository literature-review summaries

The repository literature-review layer simplifies the direct-source picture:

| Witness | Type | Claim |
| --- | --- | --- |
| `docs/grammar/lit-reviews/06-func-01-pronouns-lit.md` | literature review | Henderson is summarized as `ei, eite` = inclusive and `ko, kote` = exclusive. |
| `docs/grammar/morphemes/01-prefixes.md` | morpheme literature database | `i-` is treated as `1PL.INCL`; `ka-` is treated as `1SG/1PL.EXCL`, following the Henderson-style mapping. |
| `output/publication_review/grammar_pronouns_print_slice.md` | editorial prose | The print slice provisionally adopts the Henderson-style mapping. |
| `output/publication_review/review_notes_pronouns.md` | editorial memo | The review note currently treats the generated report as conflicting with the literature-based provisional print analysis. |

These are summary-level or editorial claims, not direct quotations from the primary sources.

## Generated report claims

The generated pronoun report states the opposite mapping:

| File | Claim |
| --- | --- |
| `docs/grammar/reports/06-func-01-pronouns.md` | `kote` = inclusive; `eite` = exclusive |

This is the explicit claim under review in the present dossier.

## Editorial inference before this dossier

Before this dossier, the publication-review pronoun slice followed the repository literature-review summaries rather than the generated report. That choice was editorially cautious, but it was still an inference layer rather than an independently tested corpus conclusion.

# Competing hypotheses

## Hypothesis A

- `eite` / `ei` = inclusive
- `kote` / `ko` = exclusive

## Hypothesis B

- `kote` / `ko` = inclusive
- `eite` / `ei` = exclusive

The dossier does **not** assume either hypothesis in advance.

# Corpus method

The corpus check used the Tedim Bible text in `bibles/extracted/ctd/ctd-x-bible.txt`, joined to verse references and KJV English lines from `data/verses_aligned.tsv`.

For token matching, the search stripped edge punctuation and final apostrophes from verse tokens. On that basis, the surface-search hit counts were:

| Form | Token hits |
| --- | ---: |
| `eite` | 495 |
| `kote` | 503 |
| `ei` | 46 |
| `ko` | 215 |

The classification labels below use the following meanings:

- **inclusive**: the speaker's group includes the addressee;
- **exclusive**: the speaker's group excludes the addressee;
- **ambiguous**: the discourse context does not securely decide;
- **unsuitable**: divine deliberative speech, formulaic quotation, or another context that is too unstable for diagnosis.

# Corpus evidence

## `eite`: selected evidence

The selected `eite` sample does **not** point in only one direction. It contains clearly inclusive uses, clearly exclusive uses, and at least one unsuitable diagnostic case.

1. **Genesis 13:8 — inclusive**

   Tedim: `Tua ciangin Abram in Lot' kiangah, "Nang le kei' kikal, nang' gancingte le kei' gancingte' kikalah kitotna omsak kei ni. Bang hang hiam cih leh eite beh khat ihi hi."`

   KJV: "And Abram said unto Lot, Let there be no strife, I pray thee, between me and thee, and between my herdmen and thy herdmen; for we be brethren."

   Speaker/addressee: Abram addresses Lot directly.

   Note: This is a strong inclusive example because the proposition explicitly joins speaker and addressee.

2. **Genesis 19:31 — inclusive**

   Tedim: `A u pen in a nau tungah, "I pa lah teek ta a, leitung ngeina bangin eite hong luppih ding pasal khat zong om lo hi."`

   KJV: "And the firstborn said unto the younger, Our father is old, and there is not a man in the earth to come in unto us after the manner of all the earth:"

   Speaker/addressee: the older daughter speaks to the younger daughter.

   Note: The hearer is part of the relevant group, so this is another strong inclusive case.

3. **Genesis 31:15 — exclusive**

   Tedim: `Amah in eite gamdangmi bangin hong ngaihsun hi lo ahi hiam? Bang hang hiam cih leh amah in eite hong zuak khin a, eite a' ding hong kipia sum amah in zang mang khin hi.`

   KJV: "Are we not counted of him strangers? for he hath sold us, and hath quite devoured also our money."

   Speaker/addressee: Rachel and Leah answer Jacob.

   Note: Jacob is not included in the referent of `eite`; this is a strong exclusive use.

4. **Genesis 31:16 — exclusive**

   Tedim: `I pa' tung panin Pasian in a lakkhiatsa neihsa khempeuh eite le i tate a' ahi hi. Tua ahih ciangin tu-in, nang' tunga Pasian' hong cih peuhpeuh hih in.`

   KJV: "For all the riches which God hath taken from our father, that is our's, and our children's: now then, whatsoever God hath said unto thee, do."

   Speaker/addressee: Rachel and Leah continue speaking to Jacob.

   Note: Again the addressee is outside the `eite` group. This is exclusive.

5. **Genesis 34:21 — inclusive**

   Tedim: `"Hih mite, eite' tungah hong nop mahmah uh hi. I gam sungah tengsakin sum bawlsak ni. ... Eite' tanute zong amau pia ni."`

   KJV: "These men are peaceable with us; therefore let them dwell in the land, and trade therein; ... let us take their daughters to us for wives, and let us give them our daughters."

   Speaker/addressee: Hamor and Shechem address their own townsmen.

   Note: The exhortation includes the hearers as participants in the proposed action. This is inclusive.

6. **Genesis 34:22 — inclusive**

   Tedim: `Hih thu khat bek tawh eite tawh tenkhop ding, mikhat suah ding amau thukim uh hi. Amaute vun a ki-at bangin eite' lakah pasal khempeuh vun ki-at ding ahi hi.`

   KJV: "Only herein will the men consent unto us for to dwell with us, to be one people, if every male among us be circumcised, as they are circumcised."

   Speaker/addressee: Hamor and Shechem continue addressing their townsmen.

   Note: `eite` still refers to a speaker-plus-hearer in-group. Inclusive.

7. **Genesis 34:23 — inclusive**

   Tedim: `Amau' bawngte, amaute' neihsate, le amau' ganhingte khempeuh ei a' ding hi lo ahi hiam? Amaute tawh eite thukim hoh ni. Tua hileh amaute, eite tawh hong tengkhawm ding uh hi.`

   KJV: "Shall not their cattle and their substance and every beast of their's be our's? only let us consent unto them, and they will dwell with us."

   Speaker/addressee: same local political speech to the in-group.

   Note: Inclusive.

8. **Genesis 42:2 — inclusive**

   Tedim: `Egypt-ah an om hi, ci-in ka za hi. Eite si loin i nuntak nadingin paisuk unla, ei a' ding an va lei un.`

   KJV: "And he said, Behold, I have heard that there is corn in Egypt: get you down thither, and buy for us from thence; that we may live, and not die."

   Speaker/addressee: Jacob addresses his sons.

   Note: The sons are part of the group that must survive, so this is inclusive.

9. **Genesis 11:4 — inclusive, but weak**

   Tedim: `Tua ciangin amaute in, "Hong pai un, leitung buppi-ah eite i kithehthang gawp loh nadingin ei a dingin khuapi khat bawlin ... eite' minthan nading khat bawl ni," ci uh hi.`

   KJV: "And they said, Go to, let us build us a city and a tower ... and let us make us a name, lest we be scattered abroad..."

   Speaker/addressee: the builders speak to one another.

   Note: The hearers are included, so the form is inclusive in discourse terms, but the verse is a collective exhortation and is therefore weaker than Genesis 13:8.

10. **Genesis 11:7 — unsuitable**

   Tedim: `Hong pai un, amaute khatlekhat' thugen a kitheih loh nadingun eite paisukin amau' kampau va kitukalhsak ni, a ci hi.`

   KJV: "Go to, let us go down, and there confound their language..."

   Speaker/addressee: divine deliberative speech.

   Note: This is not a safe clusivity diagnostic because the addressee relation is not ordinary human dialogue.

Taken together, the `eite` sample is mixed. It contains both inclusive and exclusive uses, and the most famous "let us go down" example is not a good diagnostic at all.

## `kote`: selected evidence

The selected `kote` sample is strikingly different. In the addressed dialogue cases sampled here, `kote` behaves consistently as **exclusive**.

1. **Genesis 24:23 — exclusive**

   Tedim: `"Kua' tanu na hi hiam, hong gen in. Na pa' inn-ah kote' giah nading a awng ding hiam?"`

   KJV: "Whose daughter art thou? tell me, I pray thee: is there room in thy father's house for us to lodge in?"

   Speaker/addressee: Abraham's servant addresses Rebekah.

   Note: Rebekah is not part of the traveling party denoted by `kote`. Exclusive.

2. **Genesis 26:16 — exclusive**

   Tedim: `Abimelek in Isaac kiangah, "Kote' kiang panin paikhia in. Bang hang hiam cih leh kote sangin nang na vanglian zaw hi."`

   KJV: "And Abimelech said unto Isaac, Go from us; for thou art much mightier than we."

   Speaker/addressee: Abimelech addresses Isaac.

   Note: Isaac is outside the `kote` group. Exclusive.

3. **Genesis 34:9 — exclusive**

   Tedim: `Kote tawh kitenna hong bawl un. Na tanute uh kote' tungah hong pia unla, no a dingin ka tanute uh la un.`

   KJV: "And make ye marriages with us, and give your daughters unto us, and take our daughters unto you."

   Speaker/addressee: Hamor addresses Jacob's family.

   Note: The addressees are explicitly opposed to the `kote` group. This is a strong exclusive example.

4. **Genesis 37:8 — exclusive**

   Tedim: `A sanggamte in ama kiangah, "Kote' tungah nang in hong uk ding a, kote' tungah ukna aana nei ding na hi hiam?"`

   KJV: "And his brethren said to him, Shalt thou indeed reign over us? or shalt thou indeed have dominion over us?"

   Speaker/addressee: Joseph's brothers address Joseph.

   Note: Joseph is not included in `kote`. Exclusive.

5. **Genesis 43:8 — exclusive**

   Tedim: `Judah in a pa Israel kiangah, "Tangvalpa hong zuisak in; nang le kote le i tate si loin i nuntak theih nadingin kote ka va pai ding uh hi."`

   KJV: "And Judah said unto Israel his father, Send the lad with me, and we will arise and go; that we may live, and not die, both we, and thou, and also our little ones."

   Speaker/addressee: Judah addresses Israel.

   Note: The verse explicitly contrasts `nang` with `kote`. This is a very strong exclusive example.

6. **Exodus 2:19 — exclusive**

   Tedim: `Amaute in, "Egypt mi khat in tuucing dangte' khutsung panin kote hong honkhia a, ko a dingin tui nangawn hong tawisakin tuuhonte tui pia hi," ci uh hi.`

   KJV: "And they said, An Egyptian delivered us out of the hand of the shepherds, and also drew water enough for us, and watered the flock."

   Speaker/addressee: the daughters address their father.

   Note: Exclusive.

7. **Exodus 5:3 — exclusive**

   Tedim: `Tua ciangin amaute in, "Hebru-te' Pasian ko kiangah hong kilangzo hi. ... ni thum paina sehnel gamah kote hong paisakin, Topa ka Pasian uh' tungah biakna hong piasak in," a ci uh hi.`

   KJV: "And they said, The God of the Hebrews hath met with us: let us go, we pray thee, three days' journey into the desert, and sacrifice unto the LORD our God..."

   Speaker/addressee: Moses and Aaron address Pharaoh.

   Note: Pharaoh is excluded from the `kote` group. Exclusive.

8. **Exodus 20:19 — exclusive**

   Tedim: `Moses kiangah, "Nangmah in kote kiangah thu hong gen in; kote in ka ngai ding uh hi. Ahi zongin kote si kha ding ka hih uh ciangin ko tungah Pasian hong gensak kei in," a ci uh hi.`

   KJV: "And they said unto Moses, Speak thou with us, and we will hear: but let not God speak with us, lest we die."

   Speaker/addressee: the people address Moses.

   Note: Moses is the addressee and is not included in `kote`. Strong exclusive evidence.

9. **Genesis 42:31 — exclusive**

   Tedim: `Ahih hangin kote in ama kiangah, "Kote thuman mi ka hi uh a, kote thukan ka hi kei uh hi."`

   KJV: "And we said unto him, We are true men; we are no spies:"

   Speaker/addressee: Joseph's brothers recount their speech to Joseph.

   Note: The group excludes Joseph. Exclusive.

10. **Deuteronomy 5:27 — exclusive**

   Tedim: `A nai-ah va pai inla, Topa i Pasian in a gen ding khempeuh va za in. Topa i Pasian in nang tungah hong genteng ko' tungah nang hong gensawn in. Kote in hong mangin ka sem ding uh hi.`

   KJV: "Go thou near, and hear all that the LORD our God shall say: and speak thou unto us ... and we will hear it, and do it."

   Speaker/addressee: the people address Moses.

   Note: Again the addressee is outside the `kote` group. Strong exclusive evidence.

In this selected sample, `kote` repeatedly behaves as exclusive. No comparably clear inclusive `kote` example emerged from the addressed-dialogue cases reviewed here.

## `ei`: smaller comparison set

The smaller `ei` sample is mixed.

1. **Genesis 31:14 — exclusive**

   Tedim: `Tua ciangin Rachel le Leah in amah dawngin, "I pa' inn sungah ei' tanh ding ahi a, ei' luah ding ahi zongin bang om ahi hiam?"`

   KJV: "And Rachel and Leah answered and said unto him, Is there yet any portion or inheritance for us in our father's house?"

   Speaker/addressee: Rachel and Leah address Jacob.

2. **Genesis 42:2 — inclusive**

   Tedim: `... ei a' ding an va lei un.`

   KJV: "... buy for us from thence ..."

   Speaker/addressee: Jacob addresses his sons.

3. **Judges 9:28 — inclusive**

   Tedim: `Abimelek, kua hi a, ama na i sepsak dingin ei Shekhem mite kua ihi hiam?`

   KJV: "Who is Abimelech, and who is Shechem, that we should serve him?"

   Speaker/addressee: Gaal addresses the Shechemites as one political group.

4. **2 Kings 3:10 — inclusive, but weak**

   Tedim: `Topa in ei kumpi thumte hong sam hi.`

   KJV: "the LORD hath called these three kings together"

   Speaker/addressee: the king of Israel speaks in the presence of the allied kings.

5. **Psalms 137:3 — ambiguous**

   Tedim: `ei hong man mite in la i sak ding hong deih a ...`

   KJV: "they that carried us away captive required of us a song"

   Speaker/addressee: communal lament, not a stable face-to-face dialogue.

This smaller sample already shows that `ei` cannot be assumed to be exclusively inclusive or exclusively exclusive on Bible-corpus grounds alone.

## `ko`: smaller comparison set

The smaller `ko` sample patterns with `kote` rather than against it.

1. **Genesis 20:9 — exclusive**

   Tedim: `Bang hangin ko tungah hong hici gamtat na hi hiam?`

   KJV: "What hast thou done unto us?"

   Speaker/addressee: Abimelech addresses Abraham.

2. **Genesis 24:55 — exclusive**

   Tedim: `ko tawh numei hong omsak lai in`

   KJV: "Let the damsel abide with us a few days"

   Speaker/addressee: Rebekah's family addresses the servant.

3. **Genesis 26:20 — exclusive**

   Tedim: `"Tui, ko a' hi," ci uh hi.`

   KJV: "The water is our's"

   Speaker/addressee: Gerar herdsmen address Isaac's side.

4. **Genesis 34:14 — exclusive**

   Tedim: `Tua bangin pia le ung ko a dingin mindaina hi ding hi.`

   KJV: "for that were a reproach unto us"

   Speaker/addressee: Jacob's sons address Hamor and Shechem.

5. **Exodus 20:19 — exclusive**

   Tedim: `ko tungah Pasian hong gensak kei in`

   KJV: "let not God speak with us"

   Speaker/addressee: the people address Moses.

The sampled `ko` evidence is consistently exclusive.

# Evaluation of the current print-slice examples

## `eite` example in `grammar_pronouns_print_slice.md`

The current print slice uses Genesis 11:7: "let us go down, and there confound their language."

This is **unsuitable** as a clusivity diagnostic. The verse is divine deliberative speech, not ordinary human dialogue, and the addressee relation is not secure in the way required for a clusivity test.

A better corpus example exists: **Genesis 13:8**, where Abram addresses Lot and explicitly includes him in `eite beh khat ihi hi` "we are brethren." That is a much stronger diagnostic if the chapter continues to print `eite` as provisionally inclusive.

## `kote` example in `grammar_pronouns_print_slice.md`

The current print slice uses Genesis 34:9: "make marriages with us."

This is a **good diagnostic example** for an **exclusive** reading. Hamor addresses Jacob's family from a clearly distinct in-group. The addressees are not part of the `kote` referent. The example is therefore useful evidence against an inclusive reading of `kote`.

# Conclusion

## C. The Bible corpus is inconclusive

The Bible corpus does **not** support the generated report as it currently stands. In the sampled addressed-dialogue evidence, `kote` and `ko` behave consistently as **exclusive**, not inclusive.

At the same time, the Bible corpus does **not** cleanly support a full Henderson-style correction either. The sampled `eite` and `ei` material is mixed: some examples are clearly inclusive, some are clearly exclusive, and some of the most frequently cited verses are weak or unsuitable diagnostics.

The safest conclusion for the project at this stage is therefore:

1. **Do not correct `docs/grammar/reports/06-func-01-pronouns.md` yet.**
2. Keep the pronoun print slice provisional until this dossier is reviewed.
3. Treat any future correction as at least a two-part problem:
   - `kote/ko` look strongly exclusive in the Bible sample;
   - `eite/ei` require further investigation before a global label swap is made.

The most important missing evidence is not another generated summary, but a broader set of non-formulaic, non-deliberative Tedim discourse contexts. The next review step should therefore prioritize:

- more manually checked dialogue contexts for `eite/ei`;
- a fresh check of the thesis tables behind ZNC's `ì/eí` forms;
- if available later, non-Bible narrative or conversational Tedim material that is less translation-driven.

## Analyzer-aware candidate layer

This dossier now also has an analyzer-aware candidate file at `output/publication_review/candidates_pronouns.tsv`.

That file records stable accepted pronoun rows, strong `ko/kote` evidence that remains treated as exclusive, and explicit unresolved `ei/eite` rows rather than silently flattening them into a solved paradigm. It also keeps at least one false-friend row where `kei` is negative rather than pronominal.

The packet should now be read in the order `candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`. Later pronoun prose should therefore treat the candidate file as the first explicit evidence layer, not as a back-formed appendix after the print packet.

# Optional regression planning

No regression should be implemented yet.

If later editorial review accepts at least a partial correction, the first safe regression should target the **exclusive** behavior of `kote/ko`, because that is the strongest signal in the present dossier. Candidate guardrail verses would be Genesis 34:9, Exodus 20:19, and Deuteronomy 5:27. A second regression for `eite/ei` should wait until the mixed corpus behavior is resolved.
