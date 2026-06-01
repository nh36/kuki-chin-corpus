---
title: "Assembled Tedim Grammar Review Preview"
subtitle: "Not a finished grammar"
date: ""
---

# Review preview status

This is a review preview, not a finished grammar. It is assembled from first-pass publication-review slices and is controlled by `output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md`, `output/publication_review/whole_grammar_coverage_checkpoint_after_reduplication.md`, `output/publication_review/whole_grammar_coverage_audit.md`, `docs/SKELETON_GRAMMAR.md`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `PROGRESS.md`.

`output/publication_review/review_notes_transitivity.md` brought the transitivity packet to review-note maturity, and the post-transitivity checkpoint now treats the packet set as stable enough for a review preview assembled from actual slice prose. This document is not a new grammar slice, not a dictionary slice, and not a human-review packet. It is intended to help human review and direct editing, not to certify completion.

Many sections are deliberately narrow. Missing or blocked domains are marked explicitly. The PDF built from this assembly is a review preview PDF, not a final publication PDF.

# PDF/build status

This preview is reproducible from committed sources with `python3 scripts/assemble_publication_review_preview.py`. The script writes `output/publication_review/assembled_grammar_review_preview.md`, generates `output/publication_review/assembled_grammar_review_preview.tex` through Pandoc plus natbib/BibTeX citation processing, and compiles `output/publication_review/assembled_grammar_review_preview.pdf` with XeLaTeX while routing publication-review example blocks through the shared analyzer and gb4e interlinear machinery.

The assembly reuses current repository conventions where practical: the repository bibliography in `literature/bibliography.bib`, XeLaTeX compilation and the `Times New Roman` / `Helvetica` font pair already used in `scripts/export_interlinear.py`, the shared Bible/analyzer helpers in `scripts/interlinear_latex.py`, and the same 0.75-inch page-margin convention for generated TeX output.

# Known narrow-slice limitations

- VP structure / suffix stacking: currently anchored by `bawlzoding`.
- derivation / valency: currently anchored by `-sak`.
- prefix/agreement: currently anchored by `kanei / kainn`.
- clause linkage: currently anchored by `ciangin`.
- nominalization: currently anchored by `-na / bawlna`.
- NP structure / possession: currently anchored by `hih mite`, `mi khat`, `mi khempeuh`.
- noun domain: currently anchored by `gam` and `aksi / aksi-te`.
- reduplication: currently anchored by `mahmah / taktak`, with `peuhpeuh` secondary.
- transitivity: currently anchored by `sih / suak` versus `hawl / en`.

# Major unresolved domains

- [MAJOR GAP: phonology/tone remains blocked or theory-heavy.]
- [MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]
- [MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]
- [MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]

Second-pass expansions such as `-pih`, `ki-`, hong-/kong-, switch reference, relative clauses, transparent compounds, wider reduplication, and labile or ambitransitive transitivity remain outside this first-pass assembled review preview.

# 1. Phonology and tone

[MAJOR GAP: phonology/tone remains blocked or theory-heavy.]

The controlling checkpoints and audit still treat phonology/tone as blocked or theory-heavy, so no publication-review grammar slice is inlined here yet.

# 2. Deixis, pronouns, and nominal domain

## Demonstratives / deixis

*Source slice: `output/publication_review/grammar_demonstratives_print_slice.md`*

### Scope

This account offers a short treatment of Tedim demonstratives and deixis. It is intentionally narrow. It focuses on a small set of manually checked Bible examples and on the interaction between the core demonstratives `hih` and `tua`, their plural forms, and a few strong constructional extensions. It does not attempt a full treatment of copulas, sentence-final particles, directionals, or broad discourse structure.

### Overview of the demonstrative system

The current Bible corpus and the literature agree on a compact demonstrative core: proximal `hih` and distal `tua` [@henderson1965; @zamngaihcing2017]. In Bible usage, however, `tua` is not merely a spatial "that". It is also a strongly anaphoric and discourse-linking form, especially in narrative and temporal sequencing. The most economical description is therefore a system with `hih` as the core proximal demonstrative and `tua` as the core distal/anaphoric demonstrative.

The plural forms `hihte` and `tuate` behave transparently as DEM + `-te`, and the Bible also gives strong constructional material such as `hih bangin`, `tua bangin`, `tua ciangin`, and `tua ahih ciangin`. One caution remains explicit throughout this slice: Zam Ngaih Cing gives distal `huā`, while the Bible corpus overwhelmingly uses `tua` as the ordinary distal/anaphoric form [@zamngaihcing2017]. The relation is plausible, but it is not resolved here as a settled orthographic identity.

### Core demonstratives: `hih` and `tua`

`Hih` is the clearest proximal form in the present corpus. It works both as an identificational demonstrative and as an adnominal determiner.

(@ex:dem-hih) Genesis 5:1
a. Tedim: Hih pen Adam’ suanlekhakte’ laibu ahi hi.
b. Segmentation: hih pen
c. Gloss: PROX TOP
d. Translation: "This is the book of the generations of Adam."

Genesis 5:1 is especially useful because it shows `hih` as the unmarked proximal form in identificational prose. Genesis 9:12 `Hih pen ... thuciamna lim ahi hi` confirms the same pattern, while Exodus 32:9 `Hih mite ka mu zo hi` shows `hih` before a noun phrase in ordinary adnominal use.

`Tua` belongs to the same system, but its range in the Bible is broader. It clearly marks distal or previously activated referents, and it also extends naturally into anaphoric and discourse-linking uses.

(@ex:dem-tua) Genesis 1:6
a. Tedim: Pasian in, “Tuite’ laizangah van kuumpi om hen la, tua van kuumpi in tui le tui kikhensak hen,” ci hi.
b. Segmentation: tua van kuumpi
c. Gloss: DIST firmament
d. Translation: "And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters."

Genesis 1:6 is a clean adnominal example. Genesis 21:27 `tua mi nihte` is equally good for a more discourse-linked noun phrase. The important descriptive point is that the corpus keeps using `tua` where English may translate "that", "the same", or simply a contextually given referent.

### Plural forms: `hihte` and `tuate`

The plural demonstratives are straightforward. The Bible corpus strongly supports `hihte` and `tuate` as transparent plural extensions of the singular forms.

(@ex:dem-hihte) Genesis 48:8
a. Tedim: Israel in Josef’ tapate a muh ciangin amah in, “Hihte kua ahi hiam?” a ci hi.
b. Segmentation: hihte
c. Gloss: PROX-PL
d. Translation: "And Israel beheld Joseph's sons, and said, Who are these?"

(@ex:dem-tuate) Genesis 7:20
a. Tedim: Mual liante tungah tui omto lai a, tuate tungah pi sawmnih le nih thuk-in tuumcip hi.
b. Segmentation: tuate tungah
c. Gloss: DIST-PL on-LOC
d. Translation: "Fifteen cubits upward did the waters prevail; and the mountains were covered."

Genesis 10:20 `Hihte pen ... Ham’ suanlekhakte ahi hi` shows the proximal plural in topic-like prose, while Genesis 2:19 `mipa in tuate bang a ci hiam` shows the distal plural as an ordinary pronoun. Nothing in the present corpus suggests that these need any more complex treatment than DEM + `-te`.

### Adnominal and pronominal uses

The same forms serve both as adnominal modifiers and as independent pronouns. Adnominal use is easy to see in Exodus 32:9 `Hih mite`, Genesis 1:6 `tua van kuumpi`, and Genesis 21:27 `tua mi nihte`. Pronominal use is equally clear in Genesis 5:1 `Hih pen`, Genesis 48:8 `Hihte kua ahi hiam?`, and Genesis 2:19 `tuate bang a ci hiam`.

The Bible also shows productive matter/topic phrases such as `hih thu` and `tua thu`. In Genesis 24:9 `hih thu tawh kisai-in` points to the present matter under discussion, while Genesis 6:6 `tua thu in ama lungsim dahsak hi` and Exodus 2:15 `Faro in tua thu a zak ciangin` show anaphoric reference to something just reported. These are important for the grammar chapter, even if they do not have to be first-round dictionary headwords.

### Discourse and temporal deixis

This is where `tua` most clearly exceeds a merely spatial description. In Bible narrative, `tua` is a major discourse and temporal linker.

(@ex:dem-tua-ciangin) Genesis 1:3
a. Tedim: Pasian in, “Khuavak om hen,” ci hi; tua ciangin khuavak om pah hi.
b. Segmentation: tua ciangin
c. Gloss: DIST time-CVB
d. Translation: "And God said, Let there be light: and there was light."

`Tua ciangin` works naturally as "then / at that time" in event sequencing. Genesis 5:5 repeats the same pattern in obituary-style narrative: `tua ciangin amah si hi`.

`Tua ahih ciangin` is even more explicitly a discourse bridge, linking a prior state or event to the next clause.

(@ex:dem-tua-ahih-ciangin) Genesis 2:21
a. Tedim: Tua ahih ciangin Topa Pasian in mipa ihmut suak mahmah sak a, ama ihmut kalin a nakguhte khat la-in tua mun pen satak tawh a dimsak hi.
b. Segmentation: tua ahih ciangin
c. Gloss: DIST be.3SG then-CVB
d. Translation: "And the LORD God caused a deep sleep to fall upon Adam, and he slept: and he took one of his ribs, and closed up the flesh instead thereof."

Genesis 1:21 and Genesis 2:19 confirm that `tua ahih ciangin` is one of the strongest discourse-transition frames in the present corpus. It is better understood as a fixed demonstrative-temporal construction than as a purely compositional spatial phrase.

### Manner constructions with `bangin`

The Bible also gives strong manner and discourse constructions built from the demonstratives plus `bangin`.

(@ex:dem-hih-bangin) Genesis 32:4
a. Tedim: amaute hilhin, “Note in ka topa Esau kiangah hih bangin na ci ding uh hi: Na nasempa Jakob in, ‘Laban’ kiangah peemta-in tu ciang dong ka om hi.
b. Segmentation: hih bangin
c. Gloss: PROX like-CVB
d. Translation: "And he commanded them, saying, Thus shall ye speak unto my lord Esau; Thy servant Jacob saith thus, I have sojourned with Laban, and stayed there until now:"

(@ex:dem-tua-bangin) Exodus 14:30
a. Tedim: Topa in tua bangin Egypt mite’ khutsung panin tua ni-in Israel-te honkhia a, tuipi gei-ah Egypt mi a site, Israel mite in mu uh hi.
b. Segmentation: tua bangin
c. Gloss: DIST like-CVB
d. Translation: "Thus the LORD saved Israel that day out of the hand of the Egyptians; and Israel saw the Egyptians dead upon the sea shore."

`Hih bangin` is especially good for direct instruction or quoted manner, as also seen in Genesis 42:18 `hih bangin gamta un`. `Tua bangin` often resumes or summarizes an already described event, as in Genesis 50:21 `Amah in tua bangin ... amaute a hehnem hi`. These patterns belong naturally in a demonstratives slice because the deictic base still contributes to how the construction organizes discourse.

### Deferred forms: `hi` and `hih ciangin`

`Hi` should be deferred. Exact-token `hi` is far too entangled with copular, auxiliary, and sentence-final material to serve as a safe demonstrative headword in this packet. Genesis 48:18 `Hi lo hi, pa aw; hih pen a suak masa ahi hi` shows how quickly the shorter form is absorbed into other clause types. The right place for `hi` is later work on copula or sentence-final particles, not this first demonstratives packet.

`Hih ciangin` should also be deferred. The current dossier showed that many apparent hits involve verbal `hih` "do/be thus" rather than demonstrative `hih`. Genesis 18:10, the old generated-report example, does not contain exact demonstrative `hih ciangin`. For the present slice, `tua ciangin` is strong enough to represent the temporal side of the system on its own.

### Editorial summary

The current evidence supports a compact but stable demonstrative system. `Hih` is the core proximal demonstrative. `Tua` is the core distal/anaphoric demonstrative and should not be reduced to a merely spatial "that". `Hihte` and `tuate` are transparent plural forms, and the constructional extensions `hih bangin`, `tua bangin`, `tua ciangin`, and `tua ahih ciangin` are all well supported by manually checked Bible examples.

Just as important, the chapter has to preserve its cautions. `Hi` is not yet safe as a demonstrative headword, `hih ciangin` is not yet a stable temporal counterpart to `tua ciangin`, and the relation between Bible `tua` and the literature's `huā` is plausible but unresolved. With those limits kept explicit, demonstratives and deixis make a good narrow chapter for the next Tedim packet.

## Pronouns / clusivity

*Source slice: `output/publication_review/grammar_pronouns_print_slice.md`*

### Scope

This account presents a short print-facing chapter on Tedim personal pronouns and closely related pronominal marking. It covers independent personal pronouns, first-person plural forms and clusivity, possessive prefixes, emphatic forms in `-mah`, reflexive and reciprocal marking with `ki-`, and a cautious first treatment of `hong-` and `kong-`. It does not attempt a full account of demonstratives, interrogatives, quantifiers, TAM, or the wider verbal agreement system.

### Personal pronouns

Earlier descriptions agree on a basic personal-pronoun system with distinct first, second, and third persons and with plural forms for at least the first and second persons [@henderson1965, 32-33; @zamngaihcing2017, sec. 3.2.1]. Henderson explicitly lists `kei`, `nang`, `amah`, `ei/eite`, `ko/kote`, and `no/note`, while Zam Ngaih Cing confirms the broader person-and-number system and the absence of gender in the third person [@henderson1965, 32; @zamngaihcing2017, sec. 3.2.1]. For print purposes, the following paradigm is stable enough to use:

| Person | Singular | Plural |
| --- | --- | --- |
| 1 | `kei` | `eite`, `kote` |
| 2 | `nang` | `note` |
| 3 | `amah` | `amaute` |

(@ex:pro-amah) Genesis 3:20
a. Tedim: Mipa in a zi' min pen Eve, ci hi. Bang hang hiam cih leh amah pen mihing khempeuh' nu ahi hi.
b. Segmentation: amah
c. Gloss: 3SG.PRO
d. Translation: 'And Adam called his wife's name Eve; because she was the mother of all living.'

(@ex:pro-note) Genesis 9:9
a. Tedim: En un, note le note' khit a na suanlekhakte uh le,
b. Segmentation: note
c. Gloss: 2PL.PRO
d. Translation: 'And I, behold, I establish my covenant with you, and with your seed after you;'

These examples are ordinary independent pronouns rather than bound agreement markers. `amah` functions as a free third-person form, while `note` shows the equally straightforward second-person plural. The printed chapter can therefore begin from free pronouns and only then move to the more tightly bound prefixal system.

### First-person plural forms and clusivity

The main editorial problem in this slice is not whether Tedim has clusivity, but how far the current evidence supports global labels for the two first-person plural series. Henderson clearly distinguishes `ei/eite` from `ko/kote` through pronominal-concord prefixes, pairing the former with `i-` and the latter with `ka-` [@henderson1965, 32-33]. Zam Ngaih Cing likewise treats clusivity as a real feature of Tedim person marking, even though her presentation of the plural forms is not identical in surface detail [@zamngaihcing2017, sec. 3.2.1; @zamngaihcing2017, sec. 3.2.2]. The separate clusivity dossier for this slice shows that sampled Bible dialogue contexts strongly support `ko/kote` as exclusive, but that `ei/eite` has both clear inclusive uses and less straightforward uses in the current Bible evidence. Comparative Sukte is useful here mainly as a contrast, since Singh does not describe the same inclusive/exclusive opposition for Sukte [@sukte_grammar, sec. 4.6.1].

(@ex:pro-eite) Genesis 13:8
a. Tedim: Tua ciangin Abram in Lot' kiangah, "Nang le kei' kikal, nang' gancingte le kei' gancingte' kikalah kitotna omsak kei ni. Bang hang hiam cih leh eite beh khat ihi hi."
b. Segmentation: eite
c. Gloss: 1PL.PRO
d. Translation: 'And Abram said unto Lot, Let there be no strife, I pray thee, between me and thee, and between my herdmen and thy herdmen; for we be brethren.'

(@ex:pro-kote) Genesis 34:9
a. Tedim: Kote tawh kitenna hong bawl un. Na tanute uh kote' tungah hong pia unla, no a dingin ka tanute uh la un.
b. Segmentation: kote
c. Gloss: 1PL.PRO
d. Translation: 'And make ye marriages with us, and give your daughters unto us, and take our daughters unto you.'

Genesis 13:8 shows a genuinely inclusive use of `eite`, since Abram explicitly includes Lot in the relevant group. It does not prove that every `eite` token is inclusive. Genesis 34:9, by contrast, is a strong diagnostic for exclusive `kote`, since Hamor addresses Jacob's family from a distinct in-group. The present slice therefore treats `kote` as exclusive and leaves the exact global status of `eite` under review.[^clusivity]

### Possessive prefixes

The same person-marking forms that appear in pronominal concord also appear before nouns as possessive prefixes. Henderson treats `ka-`, `na-`, `a-`, and `i-` primarily as pronominal concord prefixes, while Zam Ngaih Cing foregrounds their possessive use in noun phrases [@henderson1965, 32-33; @zamngaihcing2017, sec. 3.2.2; @zamngaihcing2017, sec. 3.3.4.1.1]. For a printed grammar, the safest description is that the forms are shared across possessive and agreement environments, but are easiest to present first in their nominal use.

(@ex:poss-na) Genesis 24:23
a. Tedim: Kua' tanu na hi hiam, hong gen in. Na pa' inn-ah kote' giah nading a awng ding hiam? a ci hi.
b. Segmentation: na pa' inn-ah
c. Gloss: 2SG.POSS father house-LOC
d. Translation: 'Whose daughter art thou? tell me, I pray thee: is there room in thy father's house for us to lodge in?'

(@ex:poss-a) Genesis 3:20
a. Tedim: Mipa in a zi' min pen Eve, ci hi.
b. Segmentation: a zi'
c. Gloss: 3SG.POSS wife
d. Translation: 'And the man called his wife's name Eve.'

The same pattern is visible in `ka pa' inn` 'my father's house' and in the `i-` prefix that Henderson associates with the `ei/eite` series [@henderson1965, 32-33]. Singh's Sukte comparison is also helpful here, since it shows cognate person-marking prefixes in possessive use even though the wider systems are not identical [@sukte_grammar, sec. 4.5.4]. Plural verbal markers such as `-uh` belong to the later agreement chapter rather than to the pronoun inventory itself.

### Emphatic pronouns in `-mah`

Emphatic pronouns are formed by adding `-mah` to a personal-pronoun base [@henderson1965, 32; @zamngaihcing2017, sec. 3.2.6]. In print, it is best to treat these forms neither as an unrelated lexical series nor as mere stylistic variants, but as a productive emphatic pattern built on the ordinary pronoun paradigm.

(@ex:emph-keimah) Genesis 4:13
a. Tedim: Kain in Topa' tungah, Keimah gim hong kipiakna, ka thuak zawh ding hi lo hi.
b. Segmentation: kei-mah
c. Gloss: 1SG-EMPH
d. Translation: 'And Cain said unto the LORD, My punishment is greater than I can bear.'

(@ex:emph-nangmah) Genesis 20:15
a. Tedim: Abimelek in, En in, ka leitang, na mai-ah om hi. Nangmah in hoih na sakna munah teng in, a ci hi.
b. Segmentation: nang-mah
c. Gloss: 2SG-EMPH
d. Translation: 'And Abimelech said, Behold, my land is before thee: dwell where it pleaseth thee.'

The same element also appears in negative-indefinite forms such as `kuamah` 'no one' and `bangmah` 'nothing' [@zamngaihcing2017, sec. 3.2.7]. Those items belong more naturally to a later section on indefinites and interrogative-based forms, but the connection should already be noted here.

### Reflexive and reciprocal marking with `ki-`

Zam Ngaih Cing describes reflexive pronouns as repeated pronouns linked by `leh` [@zamngaihcing2017, sec. 3.2.5]. The biblical corpus nevertheless makes it clear that a print grammar also needs to acknowledge verbal `ki-`, since many reader-facing examples of reflexive or reciprocal meaning are expressed through `ki-` forms rather than through a free reflexive pronoun alone.

(@ex:refl-ki) Genesis 2:24
a. Tedim: Tua thu hangin pasal in a nu le a pa nusia-in a zi tawh kigawm a, amau tegel pum khat a bang uh hi.
b. Segmentation: ki-gawm
c. Gloss: REFL-join
d. Translation: 'Therefore shall a man leave his father and his mother, and shall cleave unto his wife: and they shall be one flesh.'

For print purposes, `ki-` can already be described as a productive reflexive or reciprocal verbal prefix. The remaining caution is lexical rather than structural: some surface `ki-` forms are lexicalized stems, so not every `ki-` word should be taken automatically as transparent reflexive morphology.

### Pronominal prefixes and inverse/directional marking

Henderson's discussion of pronominal concord is still the best starting point for the bound prefix system. She pairs `kei` with `ka-`, `nang` with `na-`, the `ei/eite` series with `i-`, the `ko/kote` series with `ka-`, `no/note` with `na-`, and all other nominals with `a-` [@henderson1965, 32-33]. Zam Ngaih Cing's discussion of nominal prefixes confirms the same basic person-marking inventory in noun phrases [@zamngaihcing2017, sec. 3.3.4.1.1]. A printed chapter on pronouns does not need the whole verbal paradigm yet, but it does need to note that the independent pronouns belong to a wider system of bound person marking.

The harder question concerns `hong-` and `kong-`. The literature treats them as participant-oriented preverbal prefixes with directional or inverse-like behavior, and Otsuka's causative discussion shows that first- and second-person objects are structurally important to their distribution [@zamngaihcing2017, sec. 5.8.1.3; @otsuka_causative]. The current corpus outputs, however, do not yet yield a stable automatic example set for `hong-`, so the present slice uses only narrow, manually checked illustrations.[^hong-kong]

(@ex:hong-prefix) Psalms 18:16
a. Tedim: Amah in a sangna panin a khut tawh zamin kei hong la a, tui thukpi panin keimah hong kaikhia hi.
b. Segmentation: hong la
c. Gloss: 3>1 take
d. Translation: 'He sent from above, he took me, He drew me out of many waters.'

(@ex:kong-prefix) Genesis 41:41
a. Tedim: Faro in Josef' kiangah, Egypt gam khempeuh a uk dingin nang kong koih khinzo hi, a ci hi.
b. Segmentation: kong koih
c. Gloss: 1>2 set
d. Translation: 'And Pharaoh said unto Joseph, See, I have set thee over all the land of Egypt.'

These examples are enough to justify a cautious print description: `hong-` and `kong-` belong with person-sensitive preverbal marking, but the exact boundary between inverse, venitive, benefactive, and wider directional readings still needs fuller chapter-level review. They should therefore appear in the dictionary slice and grammar prose, but under an explicitly provisional analysis rather than as a closed paradigm.

### Editorial summary

This slice now supports a real draft chapter on pronouns and pronominal marking. Independent pronouns, emphatic forms in `-mah`, and possessive prefixes are straightforward enough for print. `ki-` is also clear enough to present as reflexive or reciprocal verbal marking, provided lexicalized forms remain a review checkpoint. The main unresolved issue is not the existence of clusivity or of `hong-/kong-`, but how far the current report layer can be trusted to label those patterns automatically without closer editorial control.

### References

[^clusivity]: The earlier report-level reversal `kote` inclusive versus `eite` exclusive has now been removed. The safer editorial position is narrower: `ko/kote` can already be treated as exclusive, but `ei/eite` still shows mixed Bible-corpus behavior and should remain under review rather than receiving a single global label.

[^hong-kong]: The present editorial problem is not whether these forms exist, but how narrowly they should be defined in a first print chapter. The current wording stays close to cases that can be read directly from the verse context without relying on a fully solved backend analysis.

## NP structure / possession

*Source slice: `output/publication_review/grammar_np_possession_print_slice.md`*

### Scope

This is now a normalized publication-facing NP structure / possession section, following the coverage-normalization standard defined in `coverage_normalization_audit.md` and piloted in the numerals and quantifiers sections. It remains controlled by candidate evidence and explicit caveats rather than by raw generated-report counts or broad analyzer output [@henderson1965; @zamngaihcing2017].

The current section depends on:

- `coverage_normalization_audit.md`
- `candidates_np_possession.tsv`
- `dossier_np_possession.md`
- `review_notes_np_possession.md`
- `docs/grammar/reports/03-noun-06-np-structure.md`
- `docs/grammar/reports/04-np-07-possession.md`
- `examples_np_possession_normalization.tsv`

The numerals and quantifiers sections already carry the fuller analysis of numeral and quantifier systems. This section reuses those checked examples only to support modest noun-phrase structure claims.

### Overview of noun phrase structure

The clearest current evidence supports a small but coherent set of NP-order observations. Demonstrative-related material is safest where a proximal form precedes the noun, as in `hih mite`. Numerals and several quantifier-like forms follow the noun in the cleanest current examples, as seen in `mi khat`, `ni li`, `mi khempeuh`, `mi pawlkhat`, and `mi tampi`. The present section therefore supports a modest contrast between demonstrative-before-noun structure and noun-plus-postnominal numeral or quantifier structure, while leaving broader NP templating for later review.

Possession is now visible enough to include as part of the same publication-facing section, but it remains less normalized than the modifier-order material. The safest checked rows show possessor-before-possessed structure in compact noun phrases such as `na pa' inn-ah` and `a zi' min`, while the analysis of possessive prefixes, apostrophe marking, genitive structure, and relator or case overlap still requires explicit caveats.

Gospel searches produced clean noun-plus-numeral and noun-plus-quantifier examples, which helps keep the section from becoming Genesis-only. Demonstratives and possession remain more OT-led in the current pass because the Gospel comparanda were less clean under present candidate control.

### Current NP pattern inventory

| Pattern | Example form | Rough function | Current print status | Main boundary issue |
| --- | --- | --- | --- | --- |
| demonstrative + noun | `hih mite` | proximal demonstrative before a plural noun | print-ready | Gospel demonstrative comparanda are less clean than the OT anchor |
| noun + numeral / indefinite boundary | `mi khat` | noun followed by `khat` as numeral or indefinite-like modifier | print-usable with caveat | overlaps with the numerals and indefinites boundary |
| noun + numeral | `ni li` | counted noun followed by a simple numeral | print-ready | numeral formation belongs to the numerals section |
| noun + numeral | `kum sawm le nih` | counted noun followed by a compound numeral | print-ready | compound-ten analysis belongs to the numerals section |
| noun + quantifier | `mi khempeuh` | noun followed by a total quantifier | print-ready | full quantifier semantics belong to the quantifiers section |
| noun + quantifier | `mi pawlkhat` | noun followed by an existential or partitive-like quantifier | print-usable with caveat | grouping semantics remain caveated |
| noun + quantifier | `mi tampi` | noun followed by a quantity modifier | print-usable with caveat | borders on broader degree or adjective-like modification |
| possessor + possessed NP | `na pa' inn-ah` | pronominal possessor with possessed noun phrase | print-usable with caveat | overlaps with possessive prefixes, apostrophe analysis, and case closure |
| possessed NP chain | `a zi' min` | possessor-marked noun phrase containing a possessed noun | print-usable with caveat | does not yet justify a full possession paradigm |

### Demonstratives and nouns

The clearest checked demonstrative-related anchor remains `hih mite`, which safely supports a demonstrative-before-noun description for the current packet. That is a narrower and safer claim than a full theory of determiner position. The demonstratives section remains the right place for the broader deictic inventory; the present section only uses the NP row to show that demonstrative-related modification does not pattern like the postnominal numeral and quantifier rows.

(@ex:np-hih-mite) Exodus 5:5
a. Tedim: hih mite
b. Segmentation: hih | mi-te
c. Gloss: PROX | person-PL
d. Translation: 'these people'

Matthew 6:2 gives a Gospel comparandum in `a hih mite`, but that row is embedded in a larger relative-like phrase and is therefore less clean as a simple adnominal demonstrative anchor. For print purposes, the OT phrase above remains the better controlled example.

### Numerals and nouns

The normalized numerals section already carries the fuller description of the numeral system, including compound tens and larger-number expressions. The current NP section uses numeral material only to support noun-plus-numeral order: the cleanest checked rows place the noun before the numeral rather than the numeral before the noun.

(@ex:np-ni-li) John 11:39
a. Tedim: ni li
b. Segmentation: ni | li
c. Gloss: day | four
d. Translation: 'four days'

This pattern is also visible in `kum nih` and `kum sawm le nih`, so the NP claim is not tied to a single lexical head. At the same time, `mi khat` remains an explicit boundary row, since the present section uses it as NP-order evidence without resolving the full numeral versus indefinite analysis that belongs to the numerals and quantifier-adjacent discussion.

### Quantifiers and nouns

The quantifiers section already carries the fuller discussion of total, existential-like, and negative-licensed quantifier material. Here the relevant point is more limited: the cleanest checked quantifier rows also place the noun before the quantifier-like item.

(@ex:np-mi-khempeuh) Luke 2:1
a. Tedim: mi khempeuh
b. Segmentation: mi | khem-peuh
c. Gloss: person | all
d. Translation: 'all people'

`mi pawlkhat` (Matthew 2:1) and `mi tampi` (Mark 6:34) support the same general noun-plus-quantifier profile, although each keeps its own semantic caveats from the normalized quantifiers section. The current section therefore uses them as modest NP-order evidence rather than as a reopened quantifier chapter.

### Possession

Possession is now printable in a cautious way, but it remains less normalized than the modifier-order material above. The safest current claim is that the checked possession rows show possessor-before-possessed order inside the noun phrase. They do not yet justify a full paradigm of possessive prefixes, a settled treatment of apostrophe marking, or a broad theory of alienable versus inalienable possession.

(@ex:np-poss-na-pa-inn) Genesis 24:23
a. Tedim: na pa' inn-ah
b. Segmentation: na pa' inn-ah
c. Gloss: 2SG.POSS father house-LOC
d. Translation: 'in thy father's house'

(@ex:np-poss-a-zi-min) Genesis 3:20
a. Tedim: a zi' min
b. Segmentation: a zi' | min
c. Gloss: 3SG.POSS wife | name
d. Translation: 'his wife's name'

These rows are enough for a cautious description of possessor-before-possessed structure, especially when read together with the packet anchors `ka pa`, `Topa' inn`, and `a pa' inn`. They are not enough for a full possession paradigm, because the current evidence still overlaps with pronouns and possessive prefixes, genitive or apostrophe analysis, relator and postposition structure, and broader questions about head-dependent order.

No equally clean Gospel possession row was found for this pass under current candidate discipline. The possession subsection therefore remains OT-led even though the section as a whole includes Gospel-balanced NP-order examples.

### Deferred and boundary material

Several important possession and NP topics remain explicitly deferred.

- A full possession paradigm is still deferred: the present section does not normalize every possessive prefix or every nominal host.
- Kinship possession remains under-supported beyond a few controlled anchors such as `ka pa`.
- Pronominal possession and agreement overlap remains shared with the pronoun and prefix/agreement material rather than settled here.
- Apostrophe-marked relations such as `Topa' inn` remain promising, but their exact relation to genitive marking and title-like noun combinations still needs fuller normalization.
- `Topa' tungah` remains a relator or case-boundary row rather than a clean possession example.
- `ka suahna leitang` remains a nominalization boundary row rather than a core possession anchor.
- Demonstrative, numeral, and quantifier rows are used here for NP-order support only; their full systems remain in the demonstratives, numerals, and quantifiers sections.
- Analyzer-noisy or report-only material, including isolated prefix surfaces and broad recursive-possession claims, is not promoted into publication prose here.

### Summary

The NP structure / possession section can now support a modest publication-facing description of noun phrase order: the cleanest current evidence points to demonstrative-before-noun structure alongside noun-plus-postnominal numeral and quantifier patterns. Possession is now visible enough to include with formal examples, but it remains a cautious subsection whose broader paradigm, marking analysis, and interface with pronouns, genitive structure, and relators are still explicitly deferred.

## Noun domain

*Source slice: `output/publication_review/grammar_noun_domain_print_slice.md`*

### Scope

This is now a normalized publication-facing noun domain section, following the coverage-normalization standard defined in `coverage_normalization_audit.md` and piloted in the numerals, quantifiers, and NP structure / possession sections. It remains controlled by candidate evidence and explicit caveats rather than by raw generated-report counts or broad analyzer output [@henderson1965; @zamngaihcing2017].

The current section depends on:

- `coverage_normalization_audit.md`
- `candidates_noun_domain.tsv`
- `dossier_noun_domain.md`
- `review_notes_noun_domain.md`
- `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`
- `docs/grammar/reports/03-noun-01-simple.md`
- `docs/grammar/reports/03-noun-02-compounds.md`
- `docs/grammar/reports/03-noun-03-proper.md`
- `docs/grammar/reports/03-noun-04-plural.md`
- `docs/grammar/reports/03-noun-05-nominalization.md`
- `examples_noun_domain_normalization.tsv`

The normalized NP, numerals, and quantifiers sections already carry the fuller discussion of noun phrase order, numeral formation, and quantifier semantics. The present section reuses those checked rows only to show which lexical noun anchors are currently safe to describe in publication-facing prose.

### Overview of the noun domain

The clearest current evidence supports a modest but coherent noun-domain description. Simple lexical nouns such as `gam` and `aksi` are safely attested, and plural marking with `-te` is printable for controlled anchors such as `aksi-te` and `mite`. Human noun `mi` is also a stable lexical head in larger noun phrases, as seen in rows such as `mi khat`, `mi khempeuh`, `mi pawlkhat`, and `mi tampi`, while nonhuman nouns such as `ni` and `kum` behave similarly in counted phrases.

This is enough to describe a small publication-facing noun inventory, to note a cautious `-te` plural pattern, and to show that lexical nouns remain visible as heads inside demonstrative, numeral, and quantifier phrases. It is not yet enough for a full noun-domain chapter, because compounds, proper names, classifier-like nouns, and nominalized nouns still require more boundary control.

Gospel searches produced usable noun-domain evidence for `aksi`, `mi khempeuh`, `ni li`, and proper-name material such as `Abraham' suan David`, which helps keep the section from becoming Genesis-only. The cleanest `gam` and `-te` plural anchors, however, remain OT-led in the current pass.

### Current noun-domain inventory

| Form or pattern | Rough function | Example context | Current print status | Main boundary issue |
| --- | --- | --- | --- | --- |
| `gam` | simple common noun 'land / country' | `gam sung` | print-ready | semantic range varies across geographic and political contexts |
| `aksi` | simple common noun 'star' | `ama aksi` | print-usable with caveat | current Gospel anchor occurs inside a possessed phrase |
| `aksi-te` | noun with `-te` plural marking | `aksi-te` | print-ready | does not yet settle the full behavior of plural / collective marking |
| `mi` | human common noun 'person' | `mi khat`, `mi khempeuh` | print-ready | overlaps with quantified and counted NP structure discussed elsewhere |
| `mi-te` / `mite` | human plural noun | `hih mite` | print-ready | demonstrative and NP-order analysis belongs to other sections |
| `ni` | noun head in counted phrase | `ni li` | print-ready | numeral semantics belong to the numerals section |
| `kum` | noun head in counted phrase | `kum sawm le nih` | print-ready | compound numeral analysis belongs to the numerals section |
| `mi-nam` / `minam` | transparent compound noun | `minam khat` | print-usable with caveat | compound transparency and lexicalization remain under review |
| `Abraham` | proper name used inside a larger noun phrase | `Abraham' suan David` | print-usable with caveat | does not yet justify a full proper-noun system |

### Simple noun stems

The safest simple-stem anchors remain `gam` and `aksi`. `gam` is a robust nonhuman common noun in the noun reports, while `aksi` is visible both in older OT material and in a clean Gospel phrase that keeps the stem separate from plural marking. These rows are enough to show that the noun packet is not limited to derived forms or larger noun phrases: basic lexical stems are directly attested.

At the same time, the current section keeps the claim narrow. It does not attempt to classify all noun semantics or all stem alternations; it only records that ordinary lexical nouns can be cited safely before the analysis moves on to plural marking and larger NP environments.

(@ex:noun-gam) Genesis 2:5
a. Tedim: gam sung
b. Segmentation: gam | sung
c. Gloss: land | inside
d. Translation: in the land

(@ex:noun-aksi) Matthew 2:2
a. Tedim: ama aksi
b. Segmentation: ama | aksi
c. Gloss: 3SG | star
d. Translation: his star

### Plural marking with -te

Plural marking with `-te` is now safe to discuss in a limited way. The clearest noun-domain anchors are nonhuman `aksi-te` and human `mi-te` in the fused form `mite`. Taken together, they support a modest claim that `-te` marks plurality on nouns in publication-facing examples.

The present section does not claim that every plural or collective pattern has been normalized. Broader questions about distributive readings, plurality outside simple noun stems, and the interaction of plural marking with quantification are still deferred.

(@ex:noun-aksi-te) Genesis 1:16
a. Tedim: aksi-te
b. Segmentation: aksi | -te
c. Gloss: star | PL
d. Translation: stars

### Human nouns and common nouns

Human noun `mi` is now one of the clearest lexical noun anchors in the nominal domain. It appears as a simple noun stem and as the head of several already-normalized noun phrases, including `mi khat`, `mi khempeuh`, `mi pawlkhat`, and `mi tampi`. Its plural form `mite` is equally secure in the current packet.

This matters for the noun domain because it shows that the normalized NP, numeral, and quantifier sections are reusing genuine noun heads rather than unanalyzed filler forms. The NP structure section remains the right place for broader ordering claims, but the noun domain can now safely say that `mi` and `mite` are stable human common nouns.

(@ex:noun-hih-mite) Exodus 5:5
a. Tedim: hih mite
b. Segmentation: hih | mi | -te
c. Gloss: PROX | person | PL
d. Translation: these people

### Nouns in larger phrases

The normalized numerals, quantifiers, and NP structure / possession sections already show that nouns remain visible as heads in larger phrases. In the current noun-domain pass, that point can be stated modestly: noun heads such as `mi`, `ni`, and `kum` stay lexically identifiable inside counted and quantified expressions rather than disappearing into unanalyzed templates.

`mi khempeuh` is the clearest quantified anchor for this purpose, while `ni li` and `kum sawm le nih` show the same thing for counted phrases. The noun-domain claim is therefore limited to lexical headedness; it does not reopen the fuller NP-order or numeral/quantifier analyses.

(@ex:noun-mi-khempeuh) Luke 2:1
a. Tedim: mi khempeuh
b. Segmentation: mi | khempeuh
c. Gloss: person | all
d. Translation: all people

### Compounds and proper nouns

Compounds and proper nouns are now visible enough for a cautious note, but they remain less normalized than simple stems and plural-marked nouns. The clearest compound-like anchor is `minam`, which is still transparent enough to support a controlled print comment about noun-noun composition. Proper names such as `Abraham` are also clearly nominal, but the current packet is not yet strong enough to generalize over Bible names, place names, or analyzer-noisy multiword name strings.

The current section therefore treats compounds and proper nouns as boundary material with one safe compound example and a more modest proper-name note. `Abraham' suan David` is a useful comparandum, but it does not yet justify a full proper-name subsection or a complete account of name-internal structure.

(@ex:noun-minam-khat) Genesis 11:6
a. Tedim: minam khat
b. Segmentation: mi-nam | khat
c. Gloss: people.group | one
d. Translation: one nation

### Nominalization boundary

Derived nouns and nominalized forms remain shared with the nominalization section. Items such as `kholhna` and broader `-na` material are important for the nominal domain, but the present section does not absorb them into the lexical noun inventory. It only notes that lexical nouns, plural-marked nouns, and larger noun phrases have now been normalized far enough that nominalized nouns can be kept as an explicit boundary rather than being mixed into the basic noun list.

### Deferred and boundary material

Several noun-domain topics remain explicitly deferred.

- Transparent compounds remain only partially normalized: `minam` is useful, but broader compound classes still need more evidence.
- Lexicalized compounds remain deferred because current report evidence does not cleanly separate synchronically analyzable forms from frozen lexemes.
- Proper nouns remain boundary-heavy: `Abraham` is usable as a controlled anchor, but Bible person and place names are not yet normalized as a full subsystem.
- Classifier-like nouns and measure-like nominal heads remain shared with numeral and quantifier work rather than settled here.
- Kinship nouns remain partly shared with possession, especially where forms such as `pa`, `inn`, and `min` enter possessor constructions.
- Nominalized nouns in `-na` remain with the nominalization section rather than being promoted as basic noun stems here.
- Plural and number patterns beyond straightforward `-te` marking remain deferred.
- Analyzer-noisy noun labels and multiword proper-name strings are not promoted into publication prose.
- Raw report-only noun lists are not treated as grammar facts without checked candidate control.

### Summary

The noun domain can now support a fuller publication-facing section than the earlier narrow packet allowed. Current evidence safely identifies simple noun stems such as `gam` and `aksi`, a cautious `-te` plural pattern visible in `aksi-te` and `mite`, stable human noun heads such as `mi`, and lexical nouns that remain visible inside counted and quantified noun phrases. Compounds, proper nouns, and nominalized nouns are now better framed as explicit boundary material rather than being mixed into an under-controlled noun list [@henderson1965; @zamngaihcing2017].

## Case marking

*Source slice: `output/publication_review/grammar_case_marking_print_slice.md`*

### Scope

This is now a normalized publication-facing case marking section, following the coverage-normalization standard defined in `coverage_normalization_audit.md` and piloted in the numerals, quantifiers, NP structure / possession, and noun domain sections. It remains controlled by candidate evidence and explicit caveats rather than by raw generated-report counts or broad analyzer output [@henderson1965; @zamngaihcing2017].

The current section depends on:

- `coverage_normalization_audit.md`
- `candidates_case_marking.tsv`
- `dossier_case_marking.md`
- `review_notes_case_marking.md`
- `examples_case_marking_normalization.tsv`
- `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`
- `docs/grammar/morphemes/02-case-markers.md`
- `docs/grammar/lit-reviews/03-noun-05-postpositions-lit.md`
- `docs/grammar/reports/03-noun-04-relators.md`
- `docs/grammar/reports/03-noun-05-postpositions.md`
- `docs/grammar/reports/03-noun-06-np-structure.md`
- `docs/grammar/reports/04-np-07-possession.md`
- `docs/grammar/reports/05-verb-12-transitivity.md`
- `output/grammar/case_marking_report.md`

The normalized NP structure / possession, noun domain, relators / postpositions, and transitivity sections already carry fuller discussion of possessor structure, spatial relators, and clause-level valency. The present section only states the case-like patterns that are now safe to print, marks where those other sections begin to take over, and keeps the unresolved edges explicit.

### Overview of case-like marking

The current evidence supports a modest but coherent picture of postnominal case-like marking in Tedim. The clearest publication-facing claims concern locative or goal-like `-ah` and clause-level agentive or ergative `-in`. The same packet also supports more cautious discussion of source marking with `-pan` and `-panin`, plus accompaniment or material-extension uses of `-tawh`, but those markers remain more boundary-heavy because they overlap with relator nouns, postpositions, or broader semantic extension.

The safest current prose therefore treats case marking as an NP-final domain rather than as a fully settled paradigm of discrete suffixes. Plain noun-plus-case rows such as `khua-ah` and clause-level agent rows such as `Kain in` are secure enough to print. Relator-hosted forms such as `lakpan` and `David khuapi sungah` are also real, but they should not be collapsed into a bare suffix inventory. Apostrophe-marked possession can host the same NP-final marking, yet the apostrophe itself remains a boundary issue rather than a settled genitive case marker in this section.

The Gospel search was productive enough to keep the section from becoming OT-only. The current manually reviewed supplement adds usable Gospel support for `Herod in`, `keima inn-ah`, `David khuapi sungah`, and `lakpan`. The possessive-boundary example remains OT-led, because no equally compact Gospel row was as clean under the current control standard.

### Current case-marking inventory

| Marker or pattern | Rough function | Example context | Current print status | Main boundary issue |
| --- | --- | --- | --- | --- |
| `-ah` | locative or goal-like NP-final marking | `khua-ah`, `inn-ah` | print-ready | must stay distinct from deferred tone-sensitive `-a` and from relator-hosted spatial phrases |
| `-in` | clause-level ergative or agentive marking | `Kain in`, `Herod in` | print-ready | raw `-in` extraction overgenerates forms such as `ciangin` |
| possessor phrase plus `-ah` | possessed NP closed by case-like marking | `na pa' inn-ah` | print-usable with caveat | does not settle the apostrophe or genitive analysis |
| `-pan` | source marking, often on a relator host | `lakpan` | print-usable with caveat | current clean evidence is relator-hosted rather than a broad bare-suffix paradigm |
| `-panin` | source or departure marking | `inn panin` | print-usable with caveat | internal structure remains under review |
| `-tawh` | accompaniment, with material or instrumental extension | `kei tawh`, `leivui tawh` | print-usable with caveat | accompaniment should not be flattened together with material-extension use |
| relator noun plus case | spatial relational phrase closed by case-like marking | `David khuapi sungah`, `tungah`, `kiangah` | print-usable with caveat | belongs jointly with the relators / postpositions section rather than a suffix-only list |

### Locative and goal marking with -ah

The clearest present claim is that `-ah` is a locative or goal-like case marker at the right edge of the noun phrase. The primary candidate-backed control is plain noun-plus-locative `khua-ah`, while the new source-balance supplement adds a compact Gospel goal-like example with `keima inn-ah`. This is enough to describe `-ah` as marking location and destination-like relations without forcing a sharper split among locative, allative, and general oblique labels than the current packet can support.

The section also keeps one important negative control explicit. The current evidence does **not** justify collapsing deferred `-a` material into `-ah`. The source inventory and case dossier both keep tone-sensitive or otherwise ambiguous `-a` questions unresolved, so the publication-facing description remains narrower than a full locative or allative chapter.

(@ex:case-ah-khua) Genesis 11:28
a. Tedim: khua-ah
b. Segmentation: khua | -ah
c. Gloss: town | LOC
d. Translation: in the town

(@ex:case-ah-inn) Matthew 8:8
a. Tedim: keima inn-ah
b. Segmentation: keima | inn | -ah
c. Gloss: 1SG.self | house | LOC
d. Translation: into my house

These two rows together support the safest present wording. `khua-ah` keeps the simple noun-plus-case pattern visible, while `keima inn-ah` shows that the same marker naturally appears in a Gospel clause with motion toward a location. That is enough for cautious publication prose, but not yet enough to decide whether every `-ah` token should be described as specifically locative, allative, or more generally oblique.

### Agentive, ergative, or instrumental marking with -in

The present packet supports an agentive or ergative analysis of `-in` more clearly than it supports any broader instrumental analysis. Genesis 4:3 remains the primary candidate-backed anchor because `Kain in` is the cleanest controlled row. The new supplement adds Matthew 2:4 `Herod in` as a manually reviewed Gospel support example, which helps show that the pattern is not confined to one OT narrative window.

At the same time, this section does not claim a complete ergative system. It also does not promote a general instrumental `-in` category. The most important control here is still the homograph problem: raw searches for `-in` overgenerate forms such as `ciangin`, so only checked clause-level noun phrase rows are promoted into the grammar prose.

(@ex:case-in-kain) Genesis 4:3
a. Tedim: Kain in
b. Segmentation: Kain | in
c. Gloss: Cain | ERG
d. Translation: Cain as transitive subject

(@ex:case-in-herod) Matthew 2:4
a. Tedim: Herod in
b. Segmentation: Herod | in
c. Gloss: Herod | ERG
d. Translation: Herod as transitive subject

These examples are intentionally compact. They are not meant to reopen the full alignment chapter. They only show that a noun phrase can bear checked `-in` marking in a clause with a transitive predicate, and that this is stronger evidence than any uncontrolled `-in` string would be.

### Other controlled oblique markers

The packet still retains a small set of other controlled case-like markers, but they are best treated more cautiously than `-ah` and `-in`. Source marking with `-pan` and `-panin` is real enough to describe, especially in rows such as `lakpan` and `inn panin`, yet the cleanest `-pan` example is relator-hosted and the internal structure of `-panin` remains under review. Likewise, `-tawh` remains part of the packet because `kei tawh` is a clean accompaniment row and `leivui tawh` shows a material or instrument-like extension, but that semantic split needs to stay explicit.

This means the section can already mention `-pan`, `-panin`, and `-tawh` in the current inventory, but it should not yet present them as a fully normalized oblique subsystem. For the present pass, they remain controlled supporting material rather than the center of the case-marking chapter.

### Genitive / possessive boundary

The clearest way to discuss genitive or possessive boundary material at present is to show that an already possessed noun phrase can host case-like marking at its right edge. Genesis 24:23 gives the compact row `na pa' inn-ah`, which is already reused in the normalized NP structure / possession section. Here it serves a narrower purpose: it shows that case-like marking closes the larger noun phrase rather than attaching only to a simple underived noun stem.

(@ex:case-poss-na-pa-inn) Genesis 24:23
a. Tedim: na pa' inn-ah
b. Segmentation: na | pa' | inn | -ah
c. Gloss: 2SG.POSS | father | house | LOC
d. Translation: in thy father's house

This is enough to justify a boundary note, but not enough to settle the apostrophe analysis. The present section therefore does not settle whether the apostrophe material should be treated as a genitive suffix, a possessive linker, or an orthographic boundary convention. It only records that possessed noun phrases can participate in the same case-closing pattern that appears elsewhere in the nominal domain. The fuller discussion of possessive structure remains with the normalized NP structure / possession section.

### Case marking and relators/postpositions

The boundary with relators and postpositions is now one of the main editorial points of the section. Forms such as `sungah`, `tungah`, `kiangah`, and `lakpan` are not noise, but neither are they simple proof that Tedim can be described by a suffix-only case list. The relational host matters: `sung`, `tung`, `kiang`, and `lak` contribute spatial content before locative or source marking is added.

(@ex:case-relator-david-khuapi-sungah) Luke 2:11
a. Tedim: David khuapi sungah
b. Segmentation: David | khuapi | sung | -ah
c. Gloss: David | city | inside | LOC
d. Translation: in the city of David

(@ex:case-relator-lakpan) Matthew 5:19
a. Tedim: lakpan
b. Segmentation: lak | -pan
c. Gloss: among | ABL
d. Translation: from among

These rows belong here because they are case-like and NP-final. They also belong with the relators / postpositions section because the relational noun is part of the grammar, not just a carrier for a suffix. That is why forms such as `tungah` or `lakpan` should not be collapsed into case marking without candidate control. The best current solution is to let the two sections meet at the boundary rather than pretending the boundary does not exist.

### Case marking and argument structure

The normalized case section can now say one modest thing about argument structure: checked `-in` rows such as `Kain in` and `Herod in` show case-marked noun phrases functioning as clause-level agents, while locative or goal-like rows such as `inn-ah` show noun phrases entering the clause as spatial arguments or adjuncts. That is enough to connect the nominal domain to clause structure without reopening the full alignment or valency chapter.

The present section therefore cross-references the transitivity packet rather than replacing it. The transitivity section remains the place for fuller discussion of argument frames, lexical valency, and broader alignment questions. Case marking only contributes the controlled NP-final marking side of that picture here.

### Deferred and boundary material

Several important topics remain explicitly deferred.

- A full case paradigm is still deferred; the present evidence is not yet enough for a full case paradigm.
- The ergative versus instrumental distinction for `-in` is not settled here.
- The finer split among locative, dative, allative, and general oblique functions is still under review.
- Tone-sensitive `-a` material remains blocked rather than being collapsed into `-ah`.
- Apostrophe or genitive analysis remains unresolved and stays shared with the NP structure / possession section.
- Possessive noun phrase overlap remains explicit, especially where possessed NPs then take `-ah`.
- Relator-noun and postposition structure remains shared with the relators / postpositions section.
- Full alignment and argument-structure claims remain shared with the transitivity section.
- `-panin` remains a controlled source-marking row without a fully settled internal analysis.
- `-tawh` remains split between accompaniment and material or instrumental extension.
- Analyzer-noisy or raw report-only marker rows are not promoted into publication prose.
- Raw generated-report counts and broad analyzer output are not treated as grammar facts in this section.

### Summary

The case-marking section can now support a fuller publication-facing description than the earlier narrow packet allowed. Current evidence safely supports clause-level `-in`, locative or goal-like `-ah`, a boundary note on possessed noun phrases such as `na pa' inn-ah`, and a controlled interface with relator-hosted forms such as `David khuapi sungah` and `lakpan`. Source marking with `-pan` and `-panin`, along with `-tawh`, remains usable but secondary and caveated. The result is a real grammar section with explicit limits, not a claim that the full Tedim case system has already been finished [@henderson1965; @zamngaihcing2017].

## Relators / postpositions

*Source slice: `output/publication_review/grammar_relators_postpositions_print_slice.md`*

### Editorial scope

This is the first narrow grammar slice for Tedim relators / postpositions. It is controlled by `candidates_relators_postpositions.tsv` and `dossier_relators_postpositions_scope.md`. The generated reports `docs/grammar/reports/03-noun-04-relators.md` and `docs/grammar/reports/03-noun-05-postpositions.md` remain discovery or background sources only.

The case-marking packet is the boundary control for this slice: `candidates_case_marking.tsv`, `dossier_case_marking.md`, `grammar_case_marking_print_slice.md`, `dictionary_case_markers_print_slice.md`, and `review_notes_case_marking.md` remain the main print-facing treatment of case marking. This slice is therefore not a rewrite of the case-marking packet. The relators/postpositions dictionary slice now exists at `dictionary_relators_postpositions_print_slice.md`, and review notes now exist at `review_notes_relators_postpositions.md`.

### Relator nouns as relational hosts

The first-slice relator-noun anchors are `kiang`, `lak`, `sung`, `tung`, and cautiously `pualam`. These are best treated as relational nouns or relational stems that can host locative or source marking rather than as simple bare case suffixes.

`Kiang` is the clearest 'beside / near / at the side of' anchor. `Lak` is the clearest 'among / amid / between' anchor. `Sung` is the clearest 'inside / within / among' anchor. `Tung` is usable for 'on / above / upon', but it stays slightly closer to case-marking territory than the first three anchors and should therefore keep an explicit caveat. `Pualam` is usable for 'outside / exterior side', but it should remain the most cautious positive relator-noun anchor in the first slice because it still looks somewhat more lexical-nominal than `kiang`, `lak`, `sung`, or `tung`.

The point of this slice is not to deny the role of `-ah` or `-pan`. It is to keep visible that forms such as `kiang`, `lak`, `sung`, `tung`, and `pualam` contribute relational-host structure before locative or source marking is added. They are not simply bare case suffixes in disguise.

### Separate and relator-hosted postpositions

The first-slice postpositional material stays deliberately narrow. `Pan` is usable only as a separate or relator-hosted source postposition, as in `kiang pan` or `lak pan`. `Panin` is usable only as a source form with structural caution. `Tawh` is usable only as a separate accompaniment or associative postposition, and it must keep its case-marking boundary caveat visible.

This slice therefore treats `pan`, `panin`, and `tawh` only where they are clearly separate or clearly relator-hosted. It does **not** replace the existing case-marking treatment of `-ah`, `-in`, `-pan`, `-panin`, or `-tawh`. The goal is to show how relator nouns and separate postpositions meet in the same constructions without reopening the settled case-marking packet.

`Tawhin` remains deferred or boundary-only in the first slice. The current evidence is sparse and strongly instrument-like, so it is not yet a clean postpositional anchor parallel to `pan`, `panin`, or `tawh`.

### Case-marking boundary

Attached or fused-looking rows such as `kiangah`, `sungah`, `tungah`, `lakpan`, and similar forms are shared boundary territory with the case-marking packet. They are useful here because they show the relational-host side of the system, but they are not a reason to reopen the case-marking analysis or to treat every attached-looking form as an independent postposition.

This is the main value of the current grammar slice. The case-marking packet already explains the marker side of the system. The relators/postpositions slice adds value by explaining the relational-host side: why `kiang`, `lak`, `sung`, `tung`, and `pualam` matter, and why separate or relator-hosted `pan`, `panin`, and `tawh` should not be flattened into a broad inventory of suffix-like strings.

### Deferred and boundary material

Several items stay outside the first grammar slice as core claims.

- `nuai` remains lower-confidence boundary material rather than a first-slice relator-noun anchor.
- `mai` remains lower-confidence boundary material because it stays close to lexical noun or body-part uses.
- `tawhin` remains deferred or boundary-only because the current evidence is sparse and instrument-like.
- Raw report counts are not evidence for the slice.
- `kipan` and `kipanin` rows involving `ki` remain boundary material rather than clean independent postpositions.
- Attached or fused-looking forms should not be promoted here as independent postpositions just because they contain `pan`, `panin`, or locative material.

### Recommended next step

With `review_notes_relators_postpositions.md` now added, the packet is ready for human review at the current slice maturity level. Later work should remain narrow and case-boundary-controlled rather than broadening into a new case-marking chapter.

## Numerals

*Source slice: `output/publication_review/grammar_numerals_print_slice.md`*

### Scope

This is now a normalized publication-facing numerals section, not just the first narrow slice. It is controlled by `candidates_numerals.tsv` and `dossier_numerals.md`, and it is additionally checked against `review_notes_numerals.md`, `coverage_normalization_audit.md`, and `examples_numerals_normalization.tsv`.

The section still keeps candidate discipline. Printed claims and formal examples come from candidate evidence in `candidates_numerals.tsv` or from newly checked normalization examples in `examples_numerals_normalization.tsv`, not from raw generated-report counts and not from broad string searches over every numeral-looking form. The separate dictionary print slice still exists, but this section now aims to read like a real grammar section rather than a packet-status note.

### Overview of the numeral system

The current evidence supports a cautious but fuller overview of the Tedim numeral system. Tedim is described in the literature as a decimal system, with `sawm` as the ten base and `za` as the next larger base above the first two-digit range [@zamngaihcing2017; @henderson1965]. The Bible-backed review packet confirms that basic cardinals, compound tens, larger-number expressions, `-na` ordinals, and at least one occurrence-counting expression are all securely part of the current publication-facing section.

This normalized section therefore includes:

- decimal structure and the most useful cardinal bases;
- basic cardinal numerals and noun-plus-numeral counting phrases;
- compound tens and one Gospel teen expression;
- hundreds, thousands, and larger units only where the evidence is safe;
- ordinals with `-na`, anchored by `nihna`;
- counting expressions and classifier-like material, but only cautiously;
- occurrence-counting `sawmvei`;
- explicit ambiguity controls for `kua` and `khat`;
- distributive reduplication only as deferred material.

What it does **not** do is claim that the whole numeral chapter is finished. It does not promote raw generated-report counts as grammar facts, it does not normalize a full classifier system from thin evidence, and it does not import quantifier prose or dubious analyzer output without candidate control.

### Cardinal numerals

The table below gives the core numeral inventory needed for the present section. It is publication-facing orientation rather than a raw frequency table: the point is to show the basic system, while the formal examples below remain restricted to candidate-controlled or newly checked normalization rows.

| Value | Form | Current status in this section |
|---|---|---|
| 1 | `khat` | basic numeral; keep numeral/indefinite overlap explicit |
| 2 | `nih` | clean basic cardinal |
| 3 | `thum` | basic cardinal recognized in the report/literature layer |
| 4 | `li` | basic cardinal recognized in the report/literature layer |
| 5 | `nga` | basic cardinal recognized in the report/literature layer |
| 6 | `guk` | basic cardinal recognized in the report/literature layer |
| 7 | `sagih` | clean basic cardinal in current examples |
| 8 | `giat` | basic cardinal recognized in the report/literature layer |
| 9 | `kua` | numeral `nine` only in constructionally numeral contexts |
| 10 | `sawm` | ten base |
| 100 | `za` | hundred base |
| 1,000 | `sing` | thousand base; not fully normalized in this pass |
| 10,000 | `tul` | larger unit recognized in the report/literature layer; not fully normalized in this pass |

The table does not by itself authorize every form for immediate print-heavy exposition. It gives the normalized section a visible inventory, while the examples below keep the actual printed claims small and checked.

### Decimal composition

The safest current descriptive claim is that Tedim builds higher numerals through decimal composition, but the publication-facing section should phrase that conservatively. The report and literature support a decimal structure [@zamngaihcing2017; @henderson1965], while the current packet gives two especially useful checked examples: one Old Testament compound-ten anchor and one Gospel counted-noun expression with a compound numeral.

Genesis 5:9 remains the best controlled compound-ten anchor:

(@ex:num-sawmkua) Genesis 5:9
a. Tedim: kum sawmkua
b. Segmentation: kum | sawm-kua
c. Gloss: year | ten-nine
d. Translation: 'ninety years'

Matthew 9:20 gives a good Gospel counted-noun expression with a compound numeral:

(@ex:num-kum-sawm-le-nih) Matthew 9:20
a. Tedim: kum sawm le nih
b. Segmentation: kum | sawm | le | nih
c. Gloss: year | ten | and | two
d. Translation: 'twelve years'

These two rows are enough to support a modest decimal-composition claim. `Sawmkua` shows a clean compound-ten pattern and keeps numeral-side `kua = nine` visible in a securely numeral context. `Kum sawm le nih` shows that a counted noun can also host a larger compound numeral in Gospel material, which helps the section avoid becoming a grammar of Genesis.

The section should still stop short of a full typology of every higher numeral pattern. The report mentions wider two-digit and larger-number combinations, but the present normalized section only promotes the best checked examples.

Hundreds, thousands, and larger-number expressions are real parts of the system, but they need more caution than the simple and compound-ten rows. The current large-number anchor remains useful because it shows real biblical number style, not because every detail of the analyzer export is already polished:

(@ex:num-large) Genesis 5:27
a. Tedim: kum zakua le kum sawmguk le kua
b. Segmentation: kum | za-kua | le | kum | sawm-guk | le | kua
c. Gloss: year | hundred-nine | and | year | ten-six | and | nine [export: who]
d. Translation: 'nine hundred sixty and nine years'

This is still a print-usable-with-caveat example. The wider construction is clearly numeral, but the export compresses `za-kua`, and the final `kua` is glossed as `who` in the current export layer. The normalized section therefore keeps the row with its analyzer caveat visible instead of pretending that the export is already perfect.

### Ordinals

The safest current ordinal claim is that Tedim has `-na` ordinal formation, with `nihna` as the best controlled anchor. This is consistent with the report and literature [@zamngaihcing2017].

(@ex:num-nihna) Genesis 7:11
a. Tedim: nihna
b. Segmentation: nih-na
c. Gloss: two-NMLZ
d. Translation: 'second'

`Nihna` is the current print-ready ordinal row. The dossier already notes that `pos_span = N` in the export; that is a label caveat, not a reason to reject the ordinal analysis.

`Masa` remains visible but deferred. Gospel material such as Matthew 10:2 confirms that `masa` is a live background form for 'first', but the present section does not yet promote it as the normalized ordinal anchor because the current candidate-controlled packet is still built around `nihna`, not around a full ordinal paradigm or a full contrast between `masa` and `khatna`-type forms.

### Counting phrases and word order

The clearest current word-order claim is still modest: noun-plus-numeral patterns are securely attested. The normalized section now keeps both Old Testament and Gospel evidence visible for that pattern.

(@ex:num-kum-nih) Genesis 11:10
a. Tedim: kum nih
b. Segmentation: kum | nih
c. Gloss: year | two
d. Translation: 'two years'

(@ex:num-ni-sagih) Genesis 7:10
a. Tedim: ni sagih
b. Segmentation: ni | sagih
c. Gloss: day | seven
d. Translation: 'seven days'

(@ex:num-ni-li) John 11:39
a. Tedim: ni li
b. Segmentation: ni | li
c. Gloss: day | four
d. Translation: 'four days'

These are clean counted-noun examples, and they justify a real publication-facing statement that noun-plus-numeral order is well supported. The normalized section should still avoid overclaiming a complete typology of numeral placement. The broader report layer contains more patterns, and the literature discusses wider numeral syntax, but the checked publication-facing section should stop at what the current examples support directly.

The Gospel search for this pilot found good counted-noun examples such as `ni li` and `kum sawm le nih`. That is enough to improve source balance. It does **not** mean that every numeral construction in the section now has an equally good Gospel counterpart.

### Classifier-like and counting expressions

The report and literature mention classifier-like material and counting expressions, but the current normalized section should stay selective. Only the rows that are candidate-controlled or newly checked for this pilot should be promoted.

The safest current occurrence-counting row is still `sawmvei`:

(@ex:num-sawmvei) Genesis 31:7
a. Tedim: sawmvei
b. Segmentation: sawm-vei
c. Gloss: ten-times
d. Translation: 'ten times'

The generated report paraphrases this as `vei sawm`, but the current analyzer export preserves the fused form `sawmvei`. That export-backed `sawmvei` form means the fused form should control the present slice.

`Mi khat` remains valuable boundary evidence:

(@ex:num-mi-khat) Genesis 32:24
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: 'a man' / 'one person'

This is why the section discusses `mi khat` here but does not treat it as an uncomplicated bare numeral `one` example. It should not be treated as an uncomplicated bare numeral `one` example. It sits exactly on the numeral/indefinite boundary.

The classifier-like material can therefore be summarized cautiously:

| Expression or form | Current treatment | Reason |
|---|---|---|
| `mi khat` | print-usable with caveat | numeral/indefinite boundary, not a simple classifier row |
| `sawmvei` | print-usable with caveat | clear occurrence-counting expression |
| `pa`, `nu`, `zat`, `tei` | deferred | promising report/literature material, but not normalized in this pass |

This means the section can talk about classifier-like and counting expressions without pretending that the full classifier system has already been normalized. It also means the section does not start a quantifiers retrofit here.

### Distributive numerals

Distributive numerals remain deferred in this pilot. The previous generated-report claim for distributive `sagih sagih` is not print-ready because the current analyzer/candidate layer still does not support the repeated span in the key Genesis 7:2 row. The generated report is useful background orientation, but it should not outrun the current checked evidence.

This is exactly the kind of place where normalization must stay disciplined. The normalized section can say that distributive reduplication is a promising area in the report and literature, but it should still defer `sagih sagih` until the analyzer-backed evidence is clean enough to promote.

### Ambiguity controls

Two ambiguity controls remain central to the section:

| Form | Numeral-side use | Competing use | Current print policy |
|---|---|---|---|
| `kua` | `sawmkua`; Genesis 5:27 large-number phrase | interrogative `who` | print only in constructionally numeral contexts |
| `khat` | basic cardinal 'one' | indefinite-like readings such as `mi khat` | keep explicit boundary notes; do not overgeneralize article-like use |

The blocked `kua` control remains Genesis 48:8:

> Hihte kua ahi hiam?

That row belongs to the interrogatives packet, not to numerals. Future numerals prose must therefore not use raw `kua` hits as numeral evidence.

The `khat` side of the control is different. `Khat` is unquestionably part of the numeral inventory, but not every `khat` example is equally good as a bare numeral illustration. The best currently controlled boundary row is still `mi khat`, and no cleaner Gospel `khat` boundary example was strong enough to replace it in this pilot.

### Summary

The normalized numerals section now supports a genuine publication-facing description. Tedim has a decimal numeral system with basic cardinals, compound tens, larger bases such as `za`, `sing`, and `tul`, `-na` ordinals, noun-plus-numeral counting phrases, and at least one compact occurrence-counting expression. The section now includes multiple formal examples, a visible inventory table, and both Old Testament and Gospel evidence where the checked material allows it.

At the same time, the section keeps the important boundaries explicit. `Sawmvei` remains tied to its fused-export caveat; the Genesis 5:27 large-number phrase remains usable only with analyzer caveats; `mi khat` remains boundary evidence; `kua` must stay constructionally controlled; and distributive `sagih sagih` remains deferred until the repeated span is genuinely analyzer-backed.

## Quantifiers

*Source slice: `output/publication_review/grammar_quantifiers_print_slice.md`*

### Scope

This is now a normalized publication-facing quantifiers section, following the coverage-normalization standard defined in `coverage_normalization_audit.md` and piloted in `grammar_numerals_print_slice.md`.

The section remains controlled by `candidates_quantifiers.tsv`, `dossier_quantifiers.md`, `review_notes_quantifiers.md`, `docs/grammar/reports/06-func-05-quantifiers.md`, and the checked normalization supplement `examples_quantifiers_normalization.tsv`. Example selection follows the audit standard: example quality comes first, source balance comes second.

The present section therefore keeps candidate evidence and explicit caveats central. It does not claim that the whole quantifier system is finished, and it does not promote raw generated-report counts as grammar facts.

### Overview of quantification in Tedim

The current packet supports a modest but real publication-facing account of quantification in Tedim. The safest core anchor is universal or total `khempeuh`. Existential or indefinite-like quantification is visible through `pawlkhat`, but that material still carries a partitive or alternative-grouping caveat. `Khat` remains boundary evidence shared with numerals rather than an uncomplicated quantifier anchor. Negative-quantifier work is currently safest with `kuamah` and `bangmah` only where clear clause-level negation licenses them. Quantity-related material is also visible through `tampi tak` and noun-phrase `mi tampi`, but those rows still border on broader degree or modification work rather than constituting a full independent quantifier subsystem.

This is also where the current evidence meets broader descriptive literature most clearly: quantification in Tedim overlaps with noun-phrase structure, indefiniteness, and negation rather than forming a neatly isolated paradigm [@henderson1965; @zamngaihcing2017].

The present section therefore keeps five safe publication-facing claims in view. First, `khempeuh` supports a modest universal or total-quantifier generalization. Second, `pawlkhat` supports existential or indefinite-like readings with an explicit grouping caveat. Third, `kuamah` and `bangmah` remain usable only in negative-licensed clauses. Fourth, noun phrases such as `mi khempeuh`, `mi pawlkhat`, and `mi tampi` support only a modest noun-plus-quantifier discussion. Fifth, `peuhpeuh`, `tawm`, `zaw`, and `mahmah` remain visible as boundary material without broadening the section into a full free-choice, low-quantity, comparative, or intensifier chapter.

### Quantifier inventory

The table below summarizes the forms that are currently safe enough to discuss in the normalized section.

| Form | Rough function | Constructional status | Current print status | Main boundary issue |
| --- | --- | --- | --- | --- |
| `khempeuh` | universal / total quantifier | safe in checked noun phrases and scoped nominal expressions | print-ready | does not yet justify a full universal/distributive system |
| `pawlkhat` | existential / indefinite-like quantifier | usable in partitive or group-indefinite contexts | print-usable with caveat | grouping / alternative-set nuance remains explicit |
| `khat` in `mi khat` | numeral / indefinite boundary material | usable only as boundary evidence | print-usable with caveat | overlaps directly with numerals and indefinites |
| `kuamah` | negative-licensed human quantifier | safe in checked negative clauses | print-usable with caveat | depends on explicit negation |
| `bangmah` | negative-licensed nonhuman quantifier | safe in checked negative clauses | print-usable with caveat | overlaps with broader bang-family material outside negation |
| `tampi tak` | quantity / degree expression | compact quantity-related anchor | print-usable with caveat | borders on broader degree-modification work |
| `tampi` in `mi tampi` | quantity in noun phrase structure | usable as noun-plus-quantity row | print-usable with caveat | must not be widened into a full adjective/adverb chapter |
| `peuhpeuh` | free-choice / distributive-looking material | visible but not stabilized as core quantifier evidence | deferred | current rows lean toward free-choice or discourse readings |
| `tawm` | low-quantity edge material | report-visible but export-noisy | deferred | current analyzer gloss is too noisy for print use |
| `zaw` | comparative edge row | visible only as boundary material | edge row only | comparison is not normalized as part of the core quantifier chapter |
| `mahmah` | intensifier edge row | visible only as boundary material | edge row only | intensification belongs to broader modification work, not the core quantifier chapter |

### Universal / total quantifiers

`Khempeuh` remains the clearest current universal or total-quantifier anchor. The original packet anchor is still Genesis 2:1, which gives a well-scoped nominal expression and keeps the printed claim conservative.

(@ex:quant-khempeuh) Genesis 2:1
a. Tedim: vantung leitung le a sunga omte khempeuh
b. Segmentation: van-tung | lei-tung | le | a | sung-a | om-te | khempeuh
c. Gloss: sky-on | land-on | and | 3SG | inside-3SG | exist-PL | all
d. Translation: 'the heavens and the earth, and all that was in them'

The normalized section also adds a clean Gospel counterpart so that the section does not become another Genesis-heavy chapter.

(@ex:quant-mi-khempeuh) Luke 2:1
a. Tedim: mi khempeuh
b. Segmentation: mi | khempeuh
c. Gloss: person | all
d. Translation: 'all people' / 'everyone'

Together these rows support a modest claim: total quantification is safely visible in noun-phrase-like structures, and `khempeuh` is currently the best publication-facing anchor. Matthew 2:3 `Jerusalem khuami khempeuh` points in the same direction and supports the same noun-plus-quantifier pattern, but the printed section does not need to turn that into a broad universal/distributive system or a report-driven frequency claim.

### Existential / indefinite-like quantifiers

Existential or indefinite-like quantification is currently safest around `pawlkhat`, but the packet's original Genesis 32:8 control still has to be read as partitive or alternative-grouping evidence rather than as an uncomplicated bare `some`.

For the normalized section, a checked Gospel noun-phrase example helps show the construction more clearly in print:

(@ex:quant-mi-pawlkhat) Matthew 2:1
a. Tedim: mi pawlkhat
b. Segmentation: mi | pawl-khat
c. Gloss: person | group-one
d. Translation: 'some people'

This Gospel row is useful because it makes the noun-phrase behavior clearer, but the Genesis 32:8 packet anchor still controls the interpretation. `Pawlkhat` therefore remains grouped, partitive, or alternative-set material rather than a fully normalized article-like determiner.

The existential or indefinite-like subsection also has to keep `khat` on the boundary with numerals.

(@ex:quant-mi-khat) Genesis 32:24
a. Tedim: mi khat
b. Segmentation: mi | khat
c. Gloss: person | one
d. Translation: 'a man' / 'one person'

`Mi khat` is reused from the numerals packet as boundary evidence. The present section does not treat `khat` as an uncomplicated quantifier anchor. Instead, it keeps the numeral/indefinite overlap explicit and lets the numerals section carry the fuller discussion of `one`.

### Quantifiers and negation

The packet still handles negative quantifier material conservatively. `Kuamah` and `bangmah` are safe only in clearly negative-licensed clauses, so the section should cross-reference, not reopen, the stabilized negation packet.

(@ex:quant-kuamah) Exodus 2:12
a. Tedim: kuamah mu lo
b. Segmentation: kuamah | mu | lo
c. Gloss: nobody | see.I | NEG
d. Translation: 'he saw nobody' / 'he saw no man'

(@ex:quant-kuamah-bangmah) John 3:27
a. Tedim: kuamah in bangmah hih thei lo hi
b. Segmentation: kuamah | in | bangmah | hih | thei | lo | hi
c. Gloss: nobody | ERG | anything | do | can | NEG | DECL
d. Translation: 'nobody can do anything'

These two rows show the safest current pattern. Human-domain `kuamah` and nonhuman-domain `bangmah` are usable in print only where the negative licensing is explicit. The original Genesis 39:9 row `bangmah om lo hi` remains the compact candidate-backed nonhuman anchor behind this subsection, but John 3:27 gives the normalized section a good Gospel example without loosening the negation caveat.

The section must also keep blocked bang-family material visible. `Tua bangmah hi-in` from Exodus 27:11 remains a blocked control rather than ordinary negative-quantifier evidence. That control prevents the quantifiers packet from absorbing every `bangmah` token outside clear negative licensing.

### Quantifiers and noun phrase structure

The safest noun-phrase claim is still modest. The checked examples support noun-plus-quantifier combinations such as `mi khempeuh`, `mi pawlkhat`, and `mi tampi`, but they do not yet justify a full noun-phrase ordering chapter covering demonstratives, numerals, and all quantifier types.

(@ex:quant-mi-tampi) Mark 6:34
a. Tedim: mi tampi
b. Segmentation: mi | tampi
c. Gloss: person | many
d. Translation: 'many people'

This is where the section can integrate quantity material without broadening uncontrollably. The original packet's `tampi tak` row is still the main quantity/degree anchor, but `mi tampi` gives the normalized section a cleaner noun-phrase example. The printed claim should therefore stay narrow: Tedim clearly allows noun-plus-quantifier or noun-plus-quantity combinations in at least some checked rows, but the present packet does not yet settle a full NP-ordering typology.

### Deferred and boundary material

Several quantifier-looking domains still need to stay visibly non-normalized.

| Topic | Current treatment | Reason for caution |
| --- | --- | --- |
| numeral overlap with `khat` | print-usable with caveat | `mi khat` is shared boundary evidence and should not be detached from the numerals discussion |
| negative quantifier overlap | print-usable with caveat | `kuamah` and `bangmah` are safe only with explicit negation |
| pronoun / determiner overlap | deferred beyond modest NP discussion | current examples support only local noun-phrase claims, not a full determiner system |
| discourse / scope readings with `peuhpeuh` | deferred | current rows lean toward free-choice or broad-indefinite readings rather than settled universal quantification |
| low-quantity `tawm` | deferred | current export gloss remains too noisy for print promotion |
| `tampi tak` versus broader degree work | print-usable with caveat | useful quantity evidence, but not the start of a broad adjective/adverb chapter |
| `zaw` and `mahmah` | edge rows only | keep comparison and intensification visible without widening the section into a full comparison or intensifier chapter |
| bang-family false friends such as `tua bangmah hi-in` | blocked control | prevents overgeneration from raw bang-family report material |

This is also the right place to keep the source-balance search honest. Gospel searches produced useful rows for `khempeuh`, `pawlkhat`, `tampi`, and negative-licensed `kuamah` / `bangmah`, so the normalized section now has genuine Old Testament and Gospel coverage. The same search did not yield a cleaner Gospel replacement for the classic `mi khat` boundary row, and Gospel `peuhpeuh` material remained too free-choice or discourse-heavy to promote as settled core quantifier evidence.

### Summary

The quantifiers section now reads as a real publication-facing grammar section rather than a narrow packet note. `Khempeuh` remains the clearest universal anchor; `pawlkhat` remains useful existential or indefinite-like evidence with a grouping caveat; `khat` remains explicit numeral/indefinite boundary material; `kuamah` and `bangmah` remain tied to clear negative licensing; and `tampi` material now supports a modest noun-phrase discussion without widening into a broad modification chapter.

What remains deferred is equally important. The section still does not claim a full universal/distributive system, a full determiner system, a full negative-quantifier chapter, or a full degree/intensifier/comparative chapter. It keeps candidate evidence and explicit caveats in front of the reader, uses Gospel examples where they genuinely help, and leaves `peuhpeuh`, `tawm`, and other boundary-heavy material clearly marked for later review.

# 3. Predicate structure and verbal morphology

## Stem alternation

*Source slice: `output/publication_review/grammar_stem_alternation_print_slice.md`*

### Verb-stem alternation

This file is now a **draft argument plan**, not the final polished grammar section. The eventual prose should not be organized only by print status. It should discuss **both syntactic contexts and individual verb pairs**, in that order:

1. system-wide Form I / Form II distribution by syntactic context;
2. the strongest illustrative pairs;
3. pair-by-pair caveated and difficult evidence;
4. one-sided, control, and rejected material.

Earlier descriptions agree that Tedim has a two-form verbal system, even though the terminology differs. Henderson describes Form I and Form II, while Zam Ngaih Cing speaks of Stem 1 and Stem 2 [@henderson1965; @zamngaihcing2017]. The present review packet keeps those descriptive traditions in view, but it now separates coverage, promotion, and quotation safety much more explicitly than the earlier broad analyzer table did.

#### The Form I / Form II contrast

The opening section of the eventual grammar should introduce the system with the strongest lexical pairs, not with the widest possible inventory.

- **Core starting point**: `mu ~ muh`, `ne ~ nek`, `nei ~ neih`.
- **Basic descriptive claim**: Form I is especially clear in ordinary finite predication and many main-clause uses. Form II is especially visible in dependent, temporal, purposive, attributive, nominalized, and other constructionally bound environments.
- **Immediate caution**: do not reduce the system to slogans such as *Form II = subordinate*, *Form II = negative*, *Form I = finite*, or *Form II = nominalized only*.

The argument here should stay structural and distributional before it becomes lexical and pair-specific.

The eventual section will likely need five editorial surfaces:

- a **small core showcase table**;
- a **larger promoted-pair inventory table**;
- a **pair-by-pair discussion section**;
- a **one-sided / same-form / functional coverage table**;
- a **blocked or analyzer-noise table / appendix paragraph**.

#### Distribution by syntactic context

The main organizing file for this part of the write-up is `output/publication_review/stem_alternation_syntactic_context_matrix.tsv`. The matrix is for organizing claims and subsection order; the citation shortlist remains the source of quotation candidates. The prose should work through the following contexts in order, using the matrix rather than treating all environments as equivalent evidence.

##### Finite and main-clause uses

Start with ordinary finite predication. This is where Form I is clearest, even though some lexical pairs still show real Form II matrix tokens.

##### Imperatives and directives

Use imperatives and directives to reinforce the ordinary clause-force profile of Form I, while noting that some lexical pairs still show marked Form II directive material.

##### Negative clauses

Negative clauses belong in the argument, but they are **not** a single diagnostic. The prose should say that negative environments matter, not that Form II simply equals negation.

##### Dependent temporal clauses with `ciangin`

This is one of the strongest places to show Form II in clearly dependent syntax. It should be one of the central distributional subsections.

##### Temporal and nominal `ni-in` contexts

Use `ni-in` as a second temporal construction so the grammar does not make `ciangin` carry the whole dependent-clause argument.

##### Clause-linking with `kipan`

This subsection is especially important for pairs such as `nusia ~ nusiat`, where the best Form II evidence is constructionally bound and source-linking rather than a neat finite contrast.

##### Purposive `nadingin`

Purposive or irrealis-heavy `ding / nadingin` clauses are one of the clearest places where Form II becomes prominent across several promoted pairs.

##### Nominalized `-na`

Nominalized material should be discussed directly, but with an explicit filter against lexicalized nouns and compounds.

##### Attributive and relative `mi` contexts

These contexts belong with the broader non-final distribution. They matter, but they should not be turned into a mechanical rule.

##### Possessed and genitive attributive contexts

This section should stay compact and should probably center on `nei ~ neih`, since that pair gives the clearest evidence here.

##### Modal and ability uses

This subsection should explicitly center on `thei ~ theih`, since the pair is real but constructionally special.

##### Quotative and say-complement contexts

Discuss this environment mainly to explain why functional material such as `ci ~ cih` should not be merged blindly into the lexical-verb showcase table.

##### Derived, causative, compound, and lexicalized material

This should be an explicit filter section, not a positive-evidence section. The grammar needs to show why `-sak` material, compounds, lexicalized families, and review-bucket rows cannot simply be counted as ordinary stem evidence.

#### Core showcase pairs

The core pair subsection should remain narrow and should illustrate the system with the strongest three pairs:

- `mu ~ muh`
- `ne ~ nek`
- `nei ~ neih`

These pairs should do the main pedagogical work for the Form I / Form II contrast.

This should become the **small core showcase table**, not the full promoted inventory.

#### Promoted caveated pairs

The next section should move to the broader but still promoted inventory:

- `za ~ zak`
- `pia ~ piak`
- `nusia ~ nusiat`
- `bia ~ biak`
- `thei ~ theih`
- `piang ~ pian`
- `zui ~ zuih`
- `khial ~ khialh`
- `kia ~ kiak`
- `sawlkhia ~ sawlkhiat`

Each pair should get a short paragraph or table note answering two questions:

1. **What does the evidence positively show?**
2. **What is the specific caveat?**

The point is not to collapse them into one generic “caveated examples” bucket, but to say what kind of Form II evidence each pair contributes.

This should likely become the **larger promoted-pair inventory table**, with short editorial notes rather than long prose for every row.

#### Difficult but grammatically important pairs

This section should keep the difficult cases in the argument rather than silently dropping them:

- `ngai ~ ngaih`
- `pua ~ puak`
- `pai ~ paih`
- `tua ~ tuah`
- `tua ~ tuak`

These are not simply rejected. They matter because they show lexical-family contamination, shared-base problems, one-sided evidence, and analyzer overgeneration.

#### One-sided Bible attestations and questionnaire controls

This section should separate two things that were too easily blurred in earlier drafts:

1. **One-sided or constructionally skewed lexical verbs** such as `bawl ~ bawlh`, `dipkua ~ dipkuat`, `gen ~ genh`, `hawlkhia ~ hawlkhiat`, `husia ~ husiat`, `kho ~ khoh`, `kido ~ kidot`, `lua ~ luah`, `tu ~ tuh`, `tuahpha ~ tuahphat`, and `vial ~ vialh`.
2. **Same-form questionnaire controls** such as `dawn ~ dawn`, `hong ~ hong`, `om ~ om`, `ci ~ ci`, `hi ~ hi`, `bawl ~ bawl`, `zui ~ zui`, `pai ~ pai`, and the other same-form rows now tracked in the lexical inventory.

The prose should say clearly that same-form questionnaire rows are useful controls, but they are not overt alternating pairs in the Bible layer.

These rows are **not** discarded. They should stay visible in a coverage table because the grammar needs to account for verbs flagged by the literature, questionnaire, analyzer inventory, and Bible audit even when only one side is cleanly attested in the current Bible layer.

#### Rejected/non-verbal/analyzer-noise cases

This section should explain why some apparent pairs stay blocked:

- nouns and nominal compounds;
- lexicalized or compound families;
- derivational `-sak` material;
- homophones and shared-base contamination;
- category mismatches;
- analyzer overgeneration.

Representative blocked rows should include:

- `keu ~ keuh`
- `khai ~ khaih`
- `sia ~ siah`
- `tan ~ tanh`
- `mual ~ mualh`
- `sum ~ sumh`
- `thu ~ thuh`
- `lampi ~ lampih`
- `khua ~ khuat`
- `gamla ~ gamlat`

#### How the evidence files should be used

The final prose should keep the current evidence layers distinct:

- `output/publication_review/stem_alternation_citation_shortlist.tsv` = the **only quotation-safe layer** for printed examples.
- `output/publication_review/stem_alternation_syntactic_context_matrix.tsv` = the basis for the **context-by-context distributional argument** and for organizing claims by subsection.
- `output/publication_review/stem_alternation_pair_discussion_plan.tsv` = the basis for the **pair-by-pair discussion order and claims**.
- `output/publication_review/stem_alternation_lexical_inventory.tsv` = the coverage layer for lexical category, promotion status, blockers, and source basis.
- `output/publication_review/stem_alternation_promotable_examples.tsv` and `output/publication_review/stem_alternation_manual_promotion_review.tsv` = editorial support files for promotion and example triage.
- `output/publication_review/stem_alternation_corpus_audit.tsv` = generated local background evidence; useful for checking rows, but not a quotation-safe layer and not a tracked argument table.

#### Writing order for the eventual section

The actual grammar section should be drafted in this order:

1. **System-wide syntactic distribution**
2. **Best-attested showcase pairs**
3. **Promoted and difficult pair-by-pair discussion**
4. **One-sided / same-form / functional coverage table**
5. **Blocked or analyzer-noise appendix paragraph**

That is the architecture this packet should now support.

#### Next prose draft

The next commit should create a separate prose draft file rather than overwrite this planning file, probably at `output/publication_review/grammar_stem_alternation_section_draft.md`.

That draft should be organized as:

1. **System-wide syntactic distribution**
2. **Core showcase examples**
3. **Promoted-pair inventory**
4. **Pair-by-pair notes for promoted and difficult pairs**
5. **One-sided / same-form / functional coverage table**
6. **Blocked/noise appendix paragraph**

## Verb paradigms

[MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]

`docs/grammar/reports/05-verb-00-paradigm-tables.md` remains part of the evidence base, but it has not yet been converted into a review-note-stage packet with an assembled grammar slice.

## Prefix / agreement

*Source slice: `output/publication_review/grammar_prefix_agreement_print_slice.md`*

### Editorial scope

This is the first narrow prefix/agreement grammar slice for Tedim. It is controlled by `output/publication_review/candidates_prefix_agreement.tsv` and `output/publication_review/dossier_prefix_agreement_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-03-agreement.md`, `docs/grammar/reports/04-np-07-possession.md`, `docs/grammar/morphemes/01-prefixes.md`, `docs/grammar/lit-reviews/04-np-07-possession-lit.md`, `docs/grammar/DISAMBIGUATION.md`, and the regression evidence in `tests/test_prefix_agr_poss.py`.

This is not a full agreement chapter, not a full possession chapter, not a full object-prefix or inverse chapter, and not a rewrite of the completed pronouns/clusivity packet. It also stays narrow against `output/publication_review/review_notes_pronouns.md`, `output/publication_review/review_notes_derivation_valency.md`, and `output/publication_review/review_notes_vp_structure_stacking.md`.

The present slice therefore covers only the agreement-versus-possession routing contrast, with `kanei` as the clearest agreement anchor and `kainn` as the clearest possessive-routing anchor. No dictionary slice exists yet for prefix/agreement, because this packet is still establishing a controlled routing claim rather than a lexical headword layer. The packet now proceeds through review notes rather than through a lexical headword layer.

### Agreement versus possession routing

The first safe prefix/agreement claim is a routing contrast. Before verbs, the shared pronominal prefix family may be routed as agreement; before nouns, the same family may be routed as possession.

`Kanei` and `kainn` are the core pair for that contrast. `Kanei` keeps the prefix family on a verbal host, while `kainn` keeps it on a nominal host. `tests/test_prefix_agr_poss.py` is the key regression control here, because it explicitly requires verb-side AGR glossing to stay distinct from noun-side POSS glossing.

That is enough for the first print-facing claim. The slice does not need to resolve every larger prefix question before stating that host type already controls a safe agreement-versus-possession routing contrast in the current candidate layer.

### Agreement anchor: kanei

`Kanei` is the clearest verbal agreement anchor in the packet. The candidate TSV marks it as the main AGR-side row, and `tests/test_prefix_agr_poss.py` protects the glossing as `ka-nei` / `1SG-have`.

The grammar claim here is deliberately limited. At the current slice maturity level, `kanei` supports only the routing statement that the shared prefix family can surface as verbal agreement before a verb host. This is strong enough for a narrow print slice, but still smaller than a full agreement chapter or a full prefix paradigm.

### Possessive anchor: kainn

`Kainn` is the clearest possessive-routing anchor in the packet. The candidate TSV marks it as the nominal counterpart to `kanei`, and `tests/test_prefix_agr_poss.py` protects the glossing as `ka-inn` / `1SG.POSS-house`.

The grammar claim again stays small. At the current slice maturity level, `kainn` supports the routing statement that the same prefix family can be analyzed as possessive before a noun host. This is enough to justify a first print-facing contrast without pretending that the project already has a full possession chapter or a full possessor-syntax account.

### Why this is not just pronouns again

The completed pronouns/clusivity packet already handles independent pronouns, clusivity, and the broader pronoun paradigm through `output/publication_review/review_notes_pronouns.md`.

This slice is doing something narrower. It is about prefix routing across verbal and nominal hosts, not about reopening the independent-pronoun paradigm. That is why `kanei` and `kainn` are better first anchors here than `ipai`, `ko`, `ei`, or any broader person-paradigm table.

### Boundary material

The rest of the candidate packet stays outside the first grammar slice because each row is still dominated by another unresolved boundary.

`ainn` stays outside because the broader `a-` family overlaps with verbal agreement, relativizer-like material, and other domains. It is useful boundary evidence, but not the first clean routing anchor.

`ipai` stays outside because inclusive/exclusive `i-` material belongs first to the completed pronouns/clusivity packet rather than to this first routing slice.

`hongmu` and `kongmu` stay outside because object-prefix or inverse-like material still needs a later dedicated sub-scope with tighter directional and inverse controls.

`kipan` stays outside because `ki-` reflexive or middle material remains boundary-only between prefix/agreement and derivation/valency.

Apostrophe possession and broader possessor syntax also stay outside because this is not a full possession chapter.

### Safe first-slice claim

At the current slice maturity level, the safest prefix/agreement claim is that Tedim has candidate-controlled evidence for routing a shared pronominal prefix family differently by host type: `kanei` supports verbal agreement routing, while `kainn` supports nominal possessive routing.

That claim is deliberately smaller than a full agreement chapter, smaller than a full possession chapter, smaller than a full object-prefix or inverse chapter, and smaller than a rewritten pronoun packet.

### Recommended next step

This packet now properly proceeds to prefix/agreement review notes rather than to a dictionary slice, because it is a routing/analysis packet rather than a lexical headword packet.

If the project later wants one more prefix step after review notes and human review, the next sub-scope should be a separate hong-/kong- object-prefix or inverse candidate expansion rather than a dictionary layer.

## Transitivity

*Source slice: `output/publication_review/grammar_transitivity_print_slice.md`*

### Editorial scope

This is the first narrow transitivity grammar slice. It is controlled by `output/publication_review/candidates_transitivity.tsv` and `output/publication_review/dossier_transitivity_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-12-transitivity.md`.

Boundary control comes from `output/publication_review/review_notes_derivation_valency.md`, `output/publication_review/review_notes_stem_alternation.md`, `output/publication_review/review_notes_prefix_agreement.md`, `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, and `output/publication_review/review_notes_case_marking.md`.

This is not a full valency chapter, not a full verb-class chapter, not a dictionary slice, and not a full argument-structure account.

### Clean intransitive anchor: sih

`sih` is the clean intransitive anchor for the first slice. The controlled form and gloss/function are `sih / die`.

The claim stays narrow. `output/publication_review/candidates_transitivity.tsv` and `output/publication_review/dossier_transitivity_scope.md` treat `sih` as the safest current intransitive anchor because it is a simple ABS-led event row that does not immediately force derivation/valency, prefix/agreement, or case-marking analysis into the first print-facing claim.

### Supporting intransitive row: suak

`suak` is supporting intransitive evidence rather than the sole anchor. The controlled form and gloss/function are `suak / become`.

That makes `suak` useful as a second row for the intransitive side of the contrast. It supports a narrow change-of-state intransitive reading without forcing the slice to generalize over the whole report-level intransitive inventory.

### Clean transitive anchor: hawl

`hawl` is the clean transitive anchor for the first slice. The controlled form and gloss/function are `hawl / seek`.

The claim here also stays narrow. `hawl` is the safest current transitive anchor because it gives the packet a simple transitive event row without leaning on derivation-heavy material such as `piangsak` or stem-family material such as `ngai / ngaih`. The report percentages in `docs/grammar/reports/05-verb-12-transitivity.md` are useful discovery evidence, but they are not treated here as categorical proof.

### Supporting transitive row: en

`en` is supporting transitive evidence rather than the leading transitive claim. The controlled form and gloss/function are `en / look.at`.

That makes `en` useful as secondary support for the transitive side of the slice. It helps confirm the narrow contrast, but lower counts and perception-verb semantics make it weaker than `hawl` as a chapter-leading anchor.

### Why ambitransitive/labile material is not yet the first slice

`mu / muh` remains visible boundary evidence for alternation or labile-looking behavior. It matters because it shows that the transitivity report is not exhausted by a clean binary class split.

It stays outside the first print-facing claim, however, because `mu / muh` overlaps directly with Form I / Form II stem alternation. The same caution applies to `za / zak`, `nei / neih`, and `ngai / ngaih`, which remain candidate-layer or boundary material rather than anchors for this commit.

### Boundary material

The following stay outside the first grammar slice:

- `mu / muh`
- `za / zak`
- `nei / neih`
- `ngai / ngaih`
- `piangsak`
- `pia`
- `gen`
- `tom`
- `hong`
- `ki`
- `dawt`
- `bei`
- `pia(k)sak`
- case-dominated rows
- derivation-heavy rows
- prefix/agreement-heavy rows
- analyzer-noisy, lexicalized, report-only, or whole-system verb-class claims

`piangsak` remains outside because it is derivation/valency-heavy and lexicalized-looking. `pia`, `gen`, and `tom` remain outside because they are dominated by broader case-marking and argument-structure interpretation. `hong` and `ki` remain outside because their report behavior is too mixed for the first clean intransitive claim. `dawt`, `bei`, and `pia(k)sak` remain outside because they are too thin, too noisy, or too report-bound for the first print-facing contrast.

### Safe first-slice claim

At the current slice maturity level, the safest transitivity claim is that Tedim has candidate-controlled evidence for a narrow intransitive/transitive contrast, with `sih` and `suak` supporting the intransitive side and `hawl`, with secondary support from `en`, supporting the transitive side.

Alternation, labile behavior, stem alternation, derivation/valency, prefix/agreement, case-marking, and whole-system verb-class claims remain candidate-layer or boundary material.

### Recommended next step

After this grammar slice, the next step should be transitivity review notes rather than a dictionary slice, because this packet is grammar-facing and argument-structure-oriented rather than lexical.

If more transitivity work is chosen before review notes, the next sub-scope should be `mu / muh` as a labile or stem-alternation boundary packet, but not in this commit.

## VP structure / suffix stacking

*Source slice: `output/publication_review/grammar_vp_structure_stacking_print_slice.md`*

### Editorial scope

This is the first narrow VP structure / suffix stacking grammar slice for Tedim. It is controlled by `output/publication_review/candidates_vp_structure_stacking.tsv` and `output/publication_review/dossier_vp_structure_stacking_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-02-vp-structure.md`, `docs/grammar/reports/05-verb-10-combinations.md`, and the regression evidence in `tests/test_vp_slots.py`.

This is not a full VP chapter. It is not a rewrite of TAM, directionals, negation, sentence-final particles, or relators/postpositions. Those packet boundaries remain explicit through `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, `output/publication_review/review_notes_negation.md`, `output/publication_review/review_notes_sentence_final_particles.md`, and `output/publication_review/review_notes_relators_postpositions.md`.

The present slice therefore covers only the first safe suffix-stacking claim: `bawlzoding` as the central print-usable-with-caveat anchor for aspect plus irrealis stacking. No ordinary dictionary slice exists for this packet because it is constructional rather than lexical.

### Baseline: completed single-suffix packets

The packet starts from two completed single-suffix baselines that are already owned elsewhere.

`bawlzo` remains the compact V+ASPECT baseline already owned by the TAM packet. It shows that the repository already has a stable completive anchor, but it should be used here only as baseline evidence rather than reopened as new VP-structure prose.

`pokhia` remains the compact V+DIR baseline already owned by the directionals packet. It shows that the repository already has a stable post-stem directional anchor, but it should be used here only as baseline evidence rather than widened into a new VP-slot claim.

These baseline rows matter because the first VP slice should not redescribe already-completed packets. Their role here is only to show that compact single-suffix material is already controlled before a multi-suffix claim is added.

### First stacking anchor: aspect plus irrealis

`bawlzoding` is the central first-slice stack. The candidate layer marks it as `print_usable_with_caveat`, and `tests/test_vp_slots.py` already keeps it visible as aspect-plus-modal regression evidence.

The safe print claim is deliberately narrow. `bawlzoding` supports the ordering observation:

> verb stem + completive/aspectual material + irrealis/modal material

In other words, the current slice supports a small VP-structure claim that aspectual material can precede irrealis/modal material inside a multi-suffix verbal complex.

For the present packet, that means reading `bawlzoding` as a constructional stack rather than over-trusting every analyzer label on the row. The current analyzer gloss is noisy (`make-south-IRR`), so the slice should not pretend that the middle gloss is already a perfect semantic label. The point of the row is its suffix-stacking evidence: the repository already has a regression-backed form in which a verbal stem is followed by completive/aspectual material and then by irrealis/modal material.

This is enough for a first grammar slice, but not enough for a full VP slot template. The present packet therefore treats `bawlzoding` as the clearest current anchor for aspect plus irrealis stacking and stops there.

### Boundary and deferred stacks

The rest of the visible stacks remain outside the first core slice because each one is dominated by another packet boundary.

`khia-ta` is useful boundary evidence because it shows real TAM/directional overlap, but it is not the first-slice core. The completed TAM and directionals packets already keep this row visible as overlap evidence, and this slice should not reopen either packet through that row.

`ciahsakkik`, `bawlsakthei`, and `paikhiatsak` are real multi-suffix complexes, but they are derivation/valency-heavy stacks. Once `-sak` and other valency-changing material become central, the next packet boundary is derivation/valency rather than narrow VP stacking. These rows therefore stay deferred until the derivation/valency packet is explicitly selected.

`khiathei ding om lo` is also real overlap evidence, but it is TAM-negation overlap rather than a clean first VP-stack anchor. The completed negation and TAM packets already control that territory, so it should not be promoted as the model for core VP-stacking prose.

`dingin` remains clause-bound irrealis or subordination material. It is important because it shows how quickly visible verbal stacking can turn into clause-linkage evidence, but it should wait for a subordination packet rather than being promoted here as simple VP suffix stacking.

### Safe first-slice claim

At the current slice maturity level, the safest VP-structure claim is that Tedim permits at least some multi-suffix verbal complexes in which aspectual material precedes irrealis/modal material, with `bawlzoding` as the clearest current anchor.

That claim stays deliberately smaller than a full slot template. It does not claim that every visible stack in the reports belongs to one solved VP order, and it does not reopen completed TAM, directional, negation, sentence-final, or relator/postposition packets.

### Recommended next step

After this grammar slice, the packet can move to review notes without forcing an ordinary dictionary slice, because the safe first-slice claim is constructional rather than lexical.

The next substantive packet after this narrow constructional slice should therefore be derivation/valency candidate scoping rather than a broader VP rewrite.

## TAM / aspect / modal

*Source slice: `output/publication_review/grammar_tam_print_slice.md`*

### Editorial scope

This is the first narrow TAM / aspect / modal grammar slice for Tedim Chin, controlled by `candidates_tam.tsv` and `dossier_tam_scope.md`. It is not a full TAM chapter.

The first-slice TAM anchors are limited to `-ngei`, `-gige`, `-zel`, `-ta`, `-zo`, `-kik`, `-ding`, and `-thei`, represented here by `paingei`, `neigige`, `paizel`, `kilawmta`, `bawlzo`, `hongpaikik`, `omding`, and `bawlthei`. This slice therefore stays with compact suffixal anchors already marked print-ready or print-usable in the candidate TSV instead of widening into broad clause-structure, sentence-final, directional, or VP-slot prose. The dictionary slice now exists, but review-note work has not yet begun.

### Experiential and habitual anchors

`Paingei` (`pai-ngei` -> `go-EXP`) is the current experiential anchor. It supports the narrow claim that `-ngei` can mark experiential meaning such as 'have V-ed before' when it stays tied to a compact verbal host.

`Neigige` (`nei-gige` -> `have-HAB`) is the current habitual anchor. It supports a modest print claim that `-gige` can mark habitual or regularly repeated action.

`Paizel` (`pai-zel` -> `go-HAB.CONT`) is the current habitual-continuative anchor. It is usable, but it borders broader continuative aspect and should stay construction-controlled. The first TAM slice should therefore keep `-zel` tied to compact anchors such as `paizel` rather than turning every continuative-looking or lexicalized `zel` sequence into TAM evidence.

### Compact aspectual anchors

`Kilawmta` (`ki-lawm-ta` -> `REFL-worthy-PFV`) is the current compact perfective anchor. It supports a modest completed-event reading for `-ta`, but only with sentence-final overlap caveat. The slice relies on compact suffixed verbs, not bare `ta`, and it keeps sentence-final overlap material such as `mangngilh ta hi` outside the core TAM evidence.

`Bawlzo` (`bawl-zo` -> `make-COMPL`) is the current compact completive anchor. It supports a modest 'finish V-ing' or completive reading for `-zo`, but only with the bare-`zo` and sentence-final overlap caveat kept explicit. The slice therefore treats `bawlzo` as usable compact evidence while refusing to turn bare `zo` into default TAM proof.

`Hongpaikik` (`hong-pai-kik` -> `3→1-go-ITER`) is the current iterative anchor. It is usable as iterative or 'again' evidence, but it should not become a motion/return chapter. The first slice keeps `-kik` narrow and construction-backed rather than expanding it into every return- or motion-flavored verbal sequence.

### Compact modal anchors

`Omding` (`om-ding` -> `exist-IRR`) is the current compact `-ding` anchor. It supports a narrow irrealis / future / modal claim, but only with the explicit dingin and clause-bound caveat. `Dingin` and other clause-bound `-ding` material stay outside the starting print slice, so `omding` remains the safer anchor than report-style purposive or clause-linking material.

`Bawlthei` (`bawl-thei` -> `make-ABIL`) is the current compact abilitative anchor. It supports a narrow 'can / be able' reading for `-thei`, but only with the negation/irrealis-stack caveat kept explicit. Negative-modal strings such as `khiathei ding om lo` remain overlap controls rather than core evidence for this first slice.

### Deferred and overlap material

The following items remain out of this first grammar slice:

- `pailai`, because `-lai` still overlaps lexical `lai` / `go-midst` material and is not yet a clean prospective anchor;
- `dingin` and other clause-bound `-ding` material;
- negative modal stacks such as `khiathei ding om lo`;
- sentence-final overlap such as `mangngilh ta hi`;
- directional/TAM stacking such as `khia-ta`;
- broader VP-slot stacks such as `bawlzoding` and `bawlsakthei`;
- report-summary items such as `-nawn` and `-khin` until cleaner anchors are selected.

These forms stay visible as overlap or deferred controls, but they do not belong to the first compact TAM grammar slice.

### Recommended next step

After this grammar slice, the next step is the TAM dictionary print slice drafted against the same `candidates_tam.tsv` and `dossier_tam_scope.md`; that slice now exists, and review-note work has not yet begun. Broad TAM rewrite work remains out of scope.

## Directionals

*Source slice: `output/publication_review/grammar_directionals_print_slice.md`*

### Scope

This is a short print-facing draft section on directionals in Tedim Chin, controlled by `candidates_directionals.tsv` and `dossier_directionals.md`.

It covers only a small candidate-backed set: outward `-khia`, anchored by `pokhia`; away `-khiat`, anchored by `nawhkhiat`; nominalized `-khiat-na` boundary material, represented by `hotkhiatna`; upward `-toh`, anchored by `kilaktoh`; nominalized `-toh-na` boundary material, represented by `kahtohna`; blocked comitative/accompany `-toh` overlap, represented by `paitoh`; direction/side/manner `-lam` boundary material, represented by `tawplam`; cautious toward `-sawn` evidence, represented by `piasawn`; downward `-suk` evidence, represented by `paisuk`; and deferred `-lut`, `-phei`, `-cip`, plus `-tang`.

It does not yet attempt a full VP-slot chapter, a full TAM or aspect account, a full inventory from raw suffix counts, or a treatment of all lexicalized directional-looking forms. Dictionary and review-note slices have not yet begun.

### Directionals in outline

The current candidate-backed packet supports a narrow generalization. Directionals are visible here as suffixed verbal or verbal-derived forms in the candidate layer. The clearest first anchors are `pokhia`, `nawhkhiat`, `kilaktoh`, `piasawn`, and `paisuk`. Nominalized forms such as `hotkhiatna` and `kahtohna` are useful boundary evidence but are not identical to finite directional verbs. `-toh` requires an explicit comitative/accompany warning because `paitoh` is blocked as lexicalized `go-accompany`. `-lam` remains direction/side/manner boundary material rather than a clean simple verbal suffix in the current packet. `-lut`, `-phei`, `-cip`, and `-tang` remain deferred or not print-ready.

### Outward `-khia`

Genesis 2:5 supplies the cleanest current outward anchor:

(@ex:dir-khia-pokhia)
a. Tedim: pokhia
b. Segmentation: po-khia
c. Gloss: grow-out
d. Translation: 'grew'

`Pokhia` is the cleanest current outward `-khia` anchor. It supports a modest print claim that `-khia` can mark outward motion or direction.

That claim must stay narrow. The row does **not** license raw `khia` harvesting or a claim that every orthographic `khia` sequence is directional evidence.

### Away `-khiat` and nominalized `-khiat-na`

Deuteronomy 9:4 supplies the current away anchor:

(@ex:dir-khiat-nawhkhiat)
a. Tedim: nawhkhiat
b. Segmentation: nawh-khiat
c. Gloss: hurry-away
d. Translation: 'cast them out'

`Nawhkhiat` is the current compact away `-khiat` anchor. It is accepted with caveat because the export still labels the selected lemma/POS as `nawh` / `N`. The example is therefore usable as construction-backed away evidence with an analyzer label caution, not as an uncomplicated finite-verb showcase.

Future prose should keep `-khiat` construction-controlled rather than treating every `...khiat` token as the same directional claim.

Exodus 14:13 then keeps nominalized boundary material visible:

(@ex:dir-khiatna-hotkhiatna)
a. Tedim: hotkhiatna
b. Segmentation: hot-khiat-na
c. Gloss: save-away-NMLZ
d. Translation: 'salvation'

`Hotkhiatna` keeps `-khiat-na` visible in the packet. It is nominalized boundary material and should not be treated as identical to a finite directional predicate.

### Upward `-toh` and comitative/accompany overlap

Numbers 9:17 supplies the current upward anchor:

(@ex:dir-toh-kilaktoh)
a. Tedim: kilaktoh
b. Segmentation: ki-lak-toh
c. Gloss: REFL-take-UP
d. Translation: 'was taken up'

`Kilaktoh` is the current upward `-toh` anchor. It is usable only with the packet's polysemy caveat: this row supports upward `-toh`, but it does not license a raw equation of `-toh = UP`.

Blocked control:

> `paitoh`

`Paitoh` is blocked as comitative/accompany material. The analyzer tests treat it as lexicalized `go-accompany`, so the present grammar slice must not imply that every `-toh` token is upward-directional evidence. Upward `-toh` examples should therefore be paired with this explicit caveat.

Deuteronomy 32:50 also keeps nominalized `-toh-na` material visible:

(@ex:dir-tohna-kahtohna)
a. Tedim: kahtohna
b. Segmentation: kah-toh-na
c. Gloss: climb-up-NMLZ
d. Translation: 'the mount whither thou goest up' / 'going up'

`Kahtohna` keeps `-toh-na` visible, but it is nominalized boundary material rather than a simple finite directional predicate.

### Direction/side/manner `-lam`

Genesis 30:9 keeps `-lam` visible:

(@ex:dir-lam-tawplam) Genesis 30:9
a. Tedim: tawplam
b. Segmentation: tawp-lam
c. Gloss: end-TOWARD
d. Translation: 'left off' / 'at the end'

`Tawplam` keeps `-lam` visible, but the export profile remains nominal (`tawp` / `N`). The safest present analysis is therefore direction/side/manner boundary material rather than a clean verbal directional suffix.

This row should not be used to turn every `-lam` form into a simple verbal directional.

### Toward `-sawn`

Ezra 9:9 supplies the current cautious toward row:

(@ex:dir-sawn-piasawn)
a. Tedim: piasawn
b. Segmentation: pia-sawn
c. Gloss: give-toward
d. Translation: 'give us' / 'extend to us'

`Piasawn` is the current cautious toward `-sawn` row. It is more useful than kinship-heavy or nominal-looking rows for this packet, but it still should stay construction-controlled. The current slice should not generalize from lexicalized, continuative-looking, or kinship-heavy `-sawn` material.

### Downward `-suk`

Genesis 11:5 supplies the first corpus-backed downward row:

(@ex:dir-suk-paisuk)
a. Tedim: paisuk
b. Segmentation: pai-suk
c. Gloss: go-DOWN
d. Translation: 'came down'

`Paisuk` gives the packet a corpus-backed downward `-suk` row. Analyzer tests also support `-suk`, but print prose should rely on corpus-backed candidate rows rather than analyzer inventory alone.

### Deferred forms: `-lut`, `-phei`, `-cip`, `-tang`

Several forms remain visible only as deferred or not print-ready controls in this first slice:

- `uilut` keeps `-lut` visible but is not yet a clean print-safe inward anchor;
- `paiphei` keeps `-phei` visible, but the current export gloss `go-enter` does not justify a clean horizontal claim;
- `cip` remains lexical or analyzer-noise material rather than directional down evidence;
- `tang` remains lexical or analyzer-noise material rather than endpoint-directional evidence.

These forms remain deferred or not print-ready in this slice. They should not be promoted without cleaner analyzer-backed corpus rows.

### Editorial summary

This slice safely supports seven modest claims: `-khia` is usable as outward evidence, anchored by `pokhia`; `-khiat` is usable as away evidence, anchored by `nawhkhiat`, with `-khiat-na` boundary material from `hotkhiatna`; `-toh` is usable as upward evidence, anchored by `kilaktoh`, but only with the `paitoh` comitative/accompany caveat; `-toh-na` remains visible through `kahtohna` as nominalized boundary material; `-lam` remains direction/side/manner boundary material; `-sawn` remains cautious toward evidence through `piasawn`; and `-suk` is now corpus-backed downward evidence through `paisuk`.

What remains deferred is equally important: raw generated-report counts, raw suffix harvesting, `paitoh` as upward `-toh`, nominalized `-na` forms as equivalent to finite directional verbs, `-lut`, `-phei`, `-cip`, and `-tang` as print-ready directionals, and broad TAM or VP-slot prose. Broad TAM, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.

The next step after this grammar slice is the dictionary print slice at `output/publication_review/dictionary_directionals_print_slice.md`. Dictionary and review-note work have not yet begun.

## Derivation / valency

*Source slice: `output/publication_review/grammar_derivation_valency_print_slice.md`*

### Editorial scope

This is the first narrow derivation / valency grammar slice for Tedim. It is controlled by `output/publication_review/candidates_derivation_valency.tsv` and `output/publication_review/dossier_derivation_valency_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/05-verb-08-derivational.md`, `docs/grammar/reports/05-verb-09-valency.md`, `docs/grammar/morphemes/06-derivational.md`, `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`, and the regression evidence in `tests/test_sak_caus_benf.py`.

This is not a full derivation chapter, not a full valency chapter, and not a full verbal morphology chapter. It also does not reopen adjacent packet domains already controlled through `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, `output/publication_review/review_notes_pronouns.md`, `tests/test_vp_slots.py`, and `tests/test_prefix_agr_poss.py`.

The present slice therefore covers only the first safe `-sak` claim: `paisak` as the clearest causative anchor and `muhsak` as the clearest benefactive or applicative-like split row. No dictionary slice exists yet for derivation/valency, because the packet still leaves the `-sak` lexical split open for later editorial review.

### Causative `-sak`

`paisak` is the safest causative anchor for the first print-facing derivation / valency claim. The candidate layer marks it as the main future `-sak` causative anchor, and `docs/grammar/reports/05-verb-09-valency.md` already lists it among the common `-sak` forms.

The safe grammar claim is deliberately narrow. The current evidence supports a productive Form I plus `-sak` causative pattern, with `paisak` as the candidate-controlled row that shows the pattern most cleanly. `tests/test_sak_caus_benf.py` protects that contrast explicitly by requiring `paisak` to gloss as `go-CAUS` rather than as a benefactive or lexicalized exception.

That is enough for the first core claim. The slice does not need to generalize over every `-sak` form in the reports before saying that a productive causative use is visible.

### Benefactive / applicative-like `-sak`

`muhsak` is the safest benefactive or applicative-like split row in the current packet. The candidate layer keeps it distinct from the plain causative line, and `tests/test_sak_caus_benf.py` protects that distinction by requiring Form II plus `-sak` rows to keep the `.II` marker and a `BENF` gloss.

The print claim here also stays narrow. The current evidence supports keeping Form II plus `-sak` distinct from the plain causative line in the candidate layer, with `muhsak` as the clearest first-row anchor. The literature and morpheme files justify describing this as benefactive or applicative-like material, but the slice should not pretend that every higher-level label choice is already settled.

This is why `muhsak` belongs in the first slice even though it is more caveated than `paisak`. It is the clearest compact row showing that the `-sak` domain is not exhausted by a simple causative paraphrase.

### Editorial treatment of the `-sak` split

The grammar can therefore treat the `paisak` versus `muhsak` contrast as a controlled split in the first print slice. The evidence is strong enough to keep Form I plus `-sak` and Form II plus `-sak` apart in the editorial layer.

At the same time, the slice should keep open the higher-level question of whether this contrast is best described as two readings of one suffix or two editorial subsections of the same suffixal domain. `docs/grammar/lit-reviews/05-verb-09-valency-lit.md` and `docs/grammar/morphemes/06-derivational.md` both support cautious wording here: the split is real enough for candidate control, but the final theoretical framing should stay smaller than a full chapter claim.

This first slice therefore adopts a practical editorial solution rather than a maximal theoretical one. It prints the causative and benefactive/applicative-like uses as separate controlled subsections while leaving open whether a later chapter should collapse them back into one suffix with two readings.

### Boundary material

The rest of the candidate packet remains outside the first grammar slice because each row is still dominated by another unresolved boundary.

`paipih` stays outside the first grammar slice because `-pih` still carries applicative, comitative, associative, and benefactive uncertainty. `mipihte` stays outside because it is nominal or lexicalized `pih` boundary material rather than a clean verbal anchor.

`kisep` and `kigen` stay outside because `ki-` still needs a separate reflexive, middle, and passive-like treatment, and because the packet must keep prefix/agreement boundary control explicit through `output/publication_review/review_notes_pronouns.md` and `tests/test_prefix_agr_poss.py`.

`ciahsakkik`, `bawlsakthei`, and `paikhiatsak` stay outside because they are derivation-heavy stacks interacting respectively with aspect, modal, and directional material. Those rows remain visible through `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_directionals.md`, and `tests/test_vp_slots.py`, but they are not the first core derivation anchor.

`piangsak` stays outside because it is lexicalized or transitivity-adjacent rather than a clean productive `-sak` anchor.

### Safe first-slice claim

At the current slice maturity level, the safest derivation / valency claim is that Tedim has candidate-controlled evidence for a productive `-sak` domain, with `paisak` supporting a causative use and `muhsak` supporting a distinct benefactive or applicative-like use.

That claim is deliberately smaller than a full derivation chapter, smaller than a full valency chapter, and smaller than a full verbal morphology chapter. It does not settle the whole `-pih` system, the whole `ki-` system, derivation-heavy stacking, or transitivity as a separate domain.

### Recommended next step

After this grammar slice, the next step should be review notes rather than a dictionary layer, because a dictionary layer would risk overclaiming beyond the current candidate-controlled evidence before the `-sak` lexical split is reviewed.

## Nominalization

*Source slice: `output/publication_review/grammar_nominalization_print_slice.md`*

### Editorial scope

This is the first narrow nominalization grammar slice. It is controlled by `output/publication_review/candidates_nominalization.tsv` and `output/publication_review/dossier_nominalization_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/07-nmlz-01-deverbal.md`, `docs/grammar/morphemes/06-derivational.md`, `docs/grammar/grammar_source_map.json`, and `docs/SKELETON_GRAMMAR.md`.

This is not a full nominalization chapter, not a full derivation chapter, not a full relative-clause chapter, and not a full case-routing chapter. It also stays narrow against `output/publication_review/candidates_clause_linkage.tsv`, `output/publication_review/review_notes_clause_linkage.md`, `output/publication_review/review_notes_case_marking.md`, `output/publication_review/review_notes_derivation_valency.md`, `output/publication_review/review_notes_prefix_agreement.md`, and `output/publication_review/review_notes_pronouns.md`.

The present slice therefore covers only the first safe nominalization claim. `-na` is the clearest productive deverbal nominalizer, with `bawlna` as the controlled anchor form, `bawl-na` as the segmentation, and `make-NMLZ / making, creation` as the controlled gloss and function. No dictionary slice exists yet for nominalization, because this packet is still establishing a controlled constructional or morphological claim rather than a settled lexical layer. The packet now properly proceeds through nominalization review notes rather than a dictionary slice.

### Deverbal nominalization with `-na`

`-na` is the safest current nominalization anchor in the packet. The candidate TSV marks it as the main future print-facing row, and the report, source map, and skeleton all converge on it as the primary productive deverbal nominalizer.

The grammar claim here is deliberately limited. At the current slice maturity level, the safe print-facing row is `bawlna`, with the segmentation `bawl-na` and the controlled gloss `make-NMLZ / making, creation`. That is enough to support a narrow claim for productive deverbal action or result nominalization without broadening into a full nominalization chapter.

### Why `-pa` and `-mi` are not yet the first slice

Agentive or person-head nominalization evidence also exists in the candidate layer, especially through `bawlpa` and `hong pai mi`.

Those rows stay outside the first print-facing claim because `-pa` has lexicalized or title-like boundary rows such as `kumpipa` and `Topa`, while `-mi` still overlaps with person-head and relative-clause analysis. The packet is stronger if it keeps `-pa` and `-mi` visible but secondary rather than forcing them into the first nominalization slice before those lexical and clausal boundaries are better settled.

### Why nominalized relatives are not yet the first slice

Nominalized relative or clause-derived nominal evidence also exists in the candidate layer, especially through `omna`.

That row stays outside the first print-facing claim because it still belongs partly to clause linkage and relative-clause analysis. The current packet can safely preserve `omna` as candidate-layer evidence without pretending that the first nominalization slice should already resolve the nominalization versus relative-clause boundary.

### Why nominalization plus case is not yet the first slice

Nominalization-plus-case evidence also exists in the boundary layer, especially through `muhna-ah`.

That row stays outside the first print-facing claim because it belongs partly to case marking and clause-linkage boundaries. It is important evidence for later packet coordination, but it should not lead the first nominalization slice.

### Boundary material

The rest of the nominalization packet stays outside the first grammar slice because each row is still dominated by another unresolved boundary.

`bawlpa` stays outside because agentive `-pa` still has to be separated from lexicalized and title-like rows.

`hong pai mi` stays outside because person-head `-mi` still overlaps with relative-clause analysis.

`omna` stays outside because nominalized relatives remain shared with clause linkage.

`muhna-ah` stays outside because nominalization plus case routing remains shared with case marking.

`kumpipa` and `Topa` stay outside because lexicalized or title-like `-pa` rows should not be mistaken for the cleanest productive anchor.

`a bawl mi` and similar human-head relative rows stay outside because they still sit between nominalization, relative clauses, and prefix/agreement questions.

bare `na` stays outside because it is an analyzer-noisy surface form.

report-only counts stay outside because attestation by itself does not make a row safe for the first print-facing claim.

Any broad nominalization chapter claim stays outside because this packet is not yet ready to generalize from one safe deverbal nominalizer to the whole nominalization system.

### Safe first-slice claim

At the current slice maturity level, the safest nominalization claim is that Tedim has candidate-controlled evidence for productive deverbal nominalization with `-na`, with `bawlna` / `bawl-na` as the clearest current anchor. Agentive `-pa`, person-head `-mi`, nominalized relatives, and nominalization-plus-case rows remain candidate-layer or boundary material.

That claim is deliberately smaller than a full nominalization chapter, smaller than a full derivation chapter, smaller than a full relative-clause chapter, and smaller than a full case-routing chapter.

### Recommended next step

This packet now properly proceeds to nominalization review notes rather than to a dictionary slice, because this is a constructional or morphological packet and the lexical treatment of `-pa`, `-mi`, and lexicalized forms remains unsettled.

If the project later wants more nominalization work after review notes, the next sub-scope should be a separate `-pa` or `-mi` agentive candidate expansion rather than a dictionary layer, but not in this commit.

## Clause linkage

*Source slice: `output/publication_review/grammar_clause_linkage_print_slice.md`*

### Editorial scope

This is the first narrow clause-linkage grammar slice for Tedim. It is controlled by `output/publication_review/candidates_clause_linkage.tsv` and `output/publication_review/dossier_clause_linkage_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/08-clause-01-subordination.md`, `docs/grammar/reports/08-clause-02-switch-reference.md`, `docs/grammar/reports/08-clause-03-relatives.md`, and `docs/grammar/lit-reviews/08-clause-03-subordination-lit.md`.

This is not a full complex-sentence chapter, not a full switch-reference chapter, and not a full relative-clause chapter. It also stays narrow against `output/publication_review/review_notes_sentence_final_particles.md`, `output/publication_review/review_notes_tam.md`, `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_prefix_agreement.md`, and `output/publication_review/review_notes_pronouns.md`.

The present slice therefore covers only the first safe subordination claim. `Ciangin` is the clearest temporal subordination anchor, while `dingin` remains visible only as a caveated purposive or clause-bound irrealis overlap row. No dictionary slice exists yet for clause linkage, because this packet is still establishing a controlled clausal claim rather than a lexical headword layer. The packet now properly proceeds through clause-linkage review notes rather than a dictionary slice.

### Temporal subordination: ciangin

`Ciangin` is the safest current subordination anchor in the packet. The candidate TSV marks it as the main future print-facing row, and the reports plus literature review converge on it as the clearest temporal subordinator.

The grammar claim here is deliberately limited. At the current slice maturity level, the safe print-facing row is `tua ciangin`, with the segmentation `ciang-in` kept visible where useful. That is enough to support a narrow temporal subordination claim without broadening into a full complex-sentence chapter or a full inventory of all clause-linkage constructions.

### Clause-bound purposive / irrealis overlap: dingin

`Dingin` is relevant to clause linkage because the reports support purposive or clause-bound irrealis use, but it remains partly shared with TAM. The candidate layer is therefore right to keep it explicit while refusing to let it lead the first slice.

The grammar claim stays cautious on purpose. At the current slice maturity level, `dingin` is visible only as a caveated overlap row: it helps show that clause linkage interacts with purposive or irrealis marking, but it does not yet justify a broader clause-linkage or TAM rewrite.

### Why switch reference is not yet the first slice

Switch-reference evidence exists in the candidate layer, especially through `VERB-in` with `ngenin` as the anchor example and through `ahih ciangin` as the clearest different-subject construction.

Those rows stay outside the first print-facing claim because the converb, subordinator, and switch-reference analysis remains theoretically unsettled. The current packet can safely preserve them as candidate-layer evidence without pretending that the first clause-linkage slice should already be a switch-reference chapter.

### Why relative clauses are not yet the first slice

Relative-clause evidence also exists in the candidate layer, especially through `a bawl mi` and `omna`.

Those rows stay outside the first print-facing claim because relative clauses still interact with prefix/agreement, nominalization, and case-routing questions. The packet is stronger if it keeps relative clauses visible but secondary rather than forcing them into the first clause-linkage slice before those boundaries are better settled.

### Boundary material

The rest of the clause-linkage packet stays outside the first grammar slice because each row is still dominated by another unresolved boundary.

`VERB-in` and `ngenin` stay outside because same-subject chaining still sits on the boundary between converbial chaining, subordination, and switch-reference analysis.

`ahih ciangin` stays outside because different-subject linkage still overlaps with temporal subordination and pronominal boundary questions.

`a bawl mi` and `omna` stay outside because relative clauses still interact with prefix/agreement and nominalization.

`muhna-ah` stays outside because nominalized relative-plus-case material belongs to a later nominalization and case-routing treatment.

`leh` stays outside because sentence-final-particle, coordinator, and subordinator analyses still overlap there.

`hangin` and `bangin` stay outside because they remain broader report-inventory rows rather than the first safe print anchor.

report-only relative-clause counts involving `a-` also stay outside because they do not yet separate relativizer behavior cleanly from broader prefix/agreement material.

Any broad complex-sentence chapter claim stays outside because this packet is not yet ready to generalize from one safe subordination anchor to the whole clause-linkage system.

### Safe first-slice claim

At the current slice maturity level, the safest clause-linkage claim is that Tedim has candidate-controlled evidence for temporal subordination, with `ciangin` as the clearest current anchor. `Dingin` is visible as a caveated purposive or clause-bound irrealis overlap row, but switch reference and relative clauses remain candidate-layer material.

That claim is deliberately smaller than a full complex-sentence chapter, smaller than a full switch-reference chapter, and smaller than a full relative-clause chapter.

### Recommended next step

This packet now properly proceeds to clause-linkage review notes rather than to a dictionary slice, because it is a constructional or clausal packet rather than a lexical-headword packet.

If the project later wants one more clause-linkage step before review notes and human review, the next sub-scope should be a separate switch-reference or relative-clause candidate expansion rather than a dictionary layer, but not in this commit.

# 4. Clause type, discourse-facing material, and expressive morphology

## Negation

*Source slice: `output/publication_review/grammar_negation_print_slice.md`*

### Scope

This account offers a short treatment of Tedim negation. It is intentionally narrow. It focuses on a small set of manually checked Bible examples and on the interaction between `lo`, `loh`, and `kei`. It does not attempt a full TAM chapter, a treatment of directionals, or a complete account of every negative construction in the corpus.

### Overview of the negation system

The literature and the Bible corpus agree on one central point: Tedim negation cannot be reduced to `lo` alone. Henderson foregrounds `-kei`, including prohibitive uses, while Zam Ngaih Cing explicitly describes a contrast between `-kei` and `-lou/-louh` and links the latter to stem-sensitive or dependent environments [@henderson1965; @zamngaihcing2017]. The safest summary is therefore not "Tedim negation = `lo`", but rather that the present corpus supports a three-part treatment: ordinary clause-level negation with `lo`, dependent or derived negation with `loh`, and `kei` as a central negator in prohibitives and many irrealis-heavy or directive contexts.

### Clause-level negation with `lo`

`Lo` is the safest place to start because it is the clearest ordinary clause-level negator in the Bible corpus. It appears in straightforward negative predicates such as `thusim lo hi`, `nei lo hi`, `om lo hi`, and in many future or modal combinations such as `V lo ding`. That does not make it the whole negation system, but it does make it the most transparent starting point.

(@ex:neg-lo) Genesis 4:5
a. Tedim: ahih hangin Kain le ama piakna thusim lo hi. Tua ahih ciangin Kain heh mahmah a, a mai sia hi.
b. Segmentation: thusim lo hi
c. Gloss: accept NEG DECL
d. Translation: "but unto Cain and to his offering he had not respect. And Cain was very wroth, and his countenance fell."

Genesis 4:5 is a good central example because it shows exactly the clause type a reader expects from a first negation section: a verbal predicate followed by `lo` and the clause-final declarative material. Genesis 11:30 `ta nei lo hi` is equally useful in a more compact predicative clause, and existential patterns such as `om lo hi` belong in the same zone.

`V lo uh` is a real and common surface string, but it is not automatically prohibitive. Genesis 2:25 `maizum lo uh hi` means "they were not ashamed" and is simply an ordinary plural negative predicate. Similar plural negatives occur elsewhere with no imperative force. It is better treated as an ordinary clausal negative pattern than as the defining prohibitive construction.

### Dependent and derived negation with `loh`

`Loh` should not be treated as a random spelling variant of `lo`. In the current Bible corpus it clusters in dependent, purposive, and derived environments such as `... loh dinga`, `... loh dingin`, and `... loh nadingin`. The safest label is therefore something like "dependent or derived negative form", not just "another way to spell `lo`".

(@ex:neg-loh) Genesis 3:11
a. Tedim: Amah in, “Na guaktanga na omna kua in hong gen ahi hiam? Na nek loh dinga kong thupiak singgah ne kha na hi hiam?” ci hi.
b. Segmentation: nek loh ding-a
c. Gloss: eat.II NEG.DEP IRR-ERG
d. Translation: "And he said, Who told thee that thou wast naked? Hast thou eaten of the tree, whereof I commanded thee that thou shouldest not eat?"

Genesis 3:11 is especially useful because `loh` is not just attached to a bare verb in isolation. It appears inside a dependent complex, `na nek loh dinga kong thupiak`, where the whole point is the commanded non-occurrence of the event. Isaiah 6:10 strengthens the same pattern by repeating `muh loh nading`, `zak loh nading`, and `theihtel loh nading` inside clearly purposive or clause-linking material. This is exactly the distribution seen again and again in the corpus: `loh` is where the Bible orthography most visibly tracks non-finite, dependent, and derived negation.

### `kei` in prohibitives and irrealis-heavy negation

`Kei` is central to real prohibitives in the Bible corpus, and those prohibitives are among the cleanest manually checked negative examples available. This alone is enough to show why the negation system cannot be flattened to `lo`.

(@ex:neg-kei) Genesis 22:12
a. Tedim: Amah in, “Tangvalpa su kei in. Ama tungah bangmah hih kei in. Bang hang hiam cih leh nang in Pasian na zahtakna tu-in ka thei a, na tapa khat neihsun keima a dingin na humcip lohna ka mu hi,” a ci hi.
b. Segmentation: su kei in ... hih kei in
c. Gloss: strike NEG IMP ... do NEG IMP
d. Translation: "And he said, Lay not thine hand upon the lad, neither do thou any thing unto him: for now I know that thou fearest God, seeing thou hast not withheld thy son, thine only son from me."

Genesis 22:12 gives two clear negative imperatives in the same speech turn. Genesis 15:1 `Lau kei in`, Genesis 19:17 `Nunghei kei unla, ... khawl kei un`, Leviticus 10:9 `ne kei un`, and Numbers 14:42 `kuanto kei un ... do kei un` all point in the same direction: `kei` is the core prohibitive negator in the current Bible data.

The corpus also shows that `kei` is not limited to prohibitives or to first-person realis. Exodus 5:2 has both `ka thei kei hi` and `ka paisak kei ding hi`, which shows `kei` in ordinary negation and in irrealis-heavy future material. The safest print summary is therefore that `kei` is central in prohibitives and common in directive, quoted, or otherwise irrealis-heavy negation, without forcing the whole system into a rigid person-based rule.

### Negative existence and cessative negation

Negative existence belongs with ordinary `lo`-based negation, but it deserves its own short section because it is extremely common and very readable in Bible prose. Clauses such as Genesis 11:30 `ta nei lo hi`, Genesis 37:24 `a sungah tui om lo hi`, and Genesis 39:9 `a kep tuam bangmah om lo hi` show the ordinary Tedim way of saying that something is absent, unavailable, or not possessed.

The corpus also supports a neat constructional entry for `nawn lo` "no longer, not again". Genesis 8:12 `hong ciahkik nawn lo hi` is a clean cessative example, and Genesis 17:5 `Na min Abram hi nawn lo ding a` shows the same construction in a renamed-future environment. This material is better treated as a construction than as a new basic negator.

### Ability and inability

The clearest treatment here is not a bare negator but the constructional pair `thei lo / theih loh`. The Bible shows common clause-level inability with `thei lo`, while dependent or derived negative ability is better represented by `theih loh` patterns than by the much rarer exact string `theih lo`.

(@ex:neg-thei-lo) Genesis 27:23
a. Tedim: A khutte in a sanggampa Esau’ khut bangin mul nei ahih manin amah in thei lo hi. Tua ahih ciangin amah in thupha pia dingin kithawi a,
b. Segmentation: thei lo hi
c. Gloss: know NEG DECL
d. Translation: "And he discerned him not, because his hands were hairy, as his brother Esau's hands: so he blessed him."

Genesis 27:23 is a compact ordinary example: `thei lo hi` means that recognition or knowledge failed to occur. Genesis 37:4 `amah hopih thei lo uh hi` shows the same pattern with an ability reading, while Exodus 33:20 `na mu thei kei ding hi` shows inability under `kei`. On the dependent side, Exodus 10:5 `muh theih loh nadingin` and Isaiah 6:10 `theihtel loh nading` show why `theih loh` must be represented directly rather than treating exact `theih lo` as the dominant form in the current corpus.

### Negative polarity items

The Bible corpus gives clean negative-polarity material, but only after filtering. Raw exact-string counts overgenerate because `kuamah` can occur in non-pronominal strings and `bangmah` has non-NPI uses such as `tua bangmah hi-in` "likewise". The discussion here therefore uses only manually checked examples.

(@ex:neg-kuamah) Exodus 2:12
a. Tedim: Amah khuadak kawikawi a, kuamah mu lo ahih manin Egypt mipa thatin sehnel sungah a seel hi.
b. Segmentation: kuamah mu lo
c. Gloss: nobody see NEG
d. Translation: "And he looked this way and that way, and when he saw that there was no man, he slew the Egyptian, and hid him in the sand."

Exodus 2:12 is a good `kuamah` example because the NPI is clearly licensed by the negative predicate. `Bangmah` behaves similarly in real NPI contexts such as Genesis 22:12 `Ama tungah bangmah hih kei in` and Genesis 39:9 `bangmah om lo hi`. Those are the kinds of examples the dictionary can safely quote. What should stay out of the main prose is any claim based on raw counts alone.

### Summary

The current evidence is strong enough for a stable negation chapter, but only if it keeps the system narrow and honest. `Lo` is the safest starting point for ordinary clause-level negation. `Loh` is a real dependent or derived negative form and should not be collapsed into accidental spelling variation. `Kei` is central in prohibitives and in many irrealis-heavy negatives, so the chapter must represent it directly rather than relegating it to a footnote.

Just as important, the description must avoid false simplicity. `V lo uh` is not the prohibitive construction, Genesis 2:25 is not a prohibitive example, and the NPI section must use filtered examples rather than raw exact-string totals. The result is a compact but linguistically honest account of the current Bible evidence.

## Interrogatives

*Source slice: `output/publication_review/grammar_interrogatives_print_slice.md`*

### Scope

This short print-facing draft section on interrogatives in Tedim Chin is controlled by `candidates_interrogatives.tsv` and `dossier_interrogatives.md`. It covers clause-final `hiam` and selected WH + `hiam` content questions. It does not yet attempt a full treatment of the sentence-final particle system, and it leaves comparison particles such as `maw`, `ham`, and `em` for later review.

### Interrogatives in outline

The current candidate-backed packet supports a narrow generalization. Yes/no questions can be marked by clause-final `hiam`, and content questions use a WH element plus `hiam`. The present WH inventory represented in the packet is `bang`, `kua`, `bangci`, and `banghangin`. Embedded question complements are visible in the dossier, but they are not yet ready for the first printed analysis.

Because this slice is controlled by the candidate-first packet rather than by raw report counts, it should stay narrow. The point here is not to describe every sentence-final question marker or every surface occurrence of `hiam`, but to print only the examples that the current candidate and dossier layer already support.

### Clause-final `hiam`

The current candidate-backed examples support clause-final `hiam` as the core yes/no pattern represented in this packet. The best print anchor is Genesis 24:23, using the attested analyzer-backed clause rather than the older generated-report paraphrase.

(@ex:hiam-yes-no)
a. Tedim: Na pa inn-ah kote giah nading a awng ding hiam
b. Segmentation: Na | pa' | inn-ah | kote' | giah | nading | a | awng | ding | hiam
c. Gloss: 2SG | male.POSS | house-LOC | 1PL.PRO.POSS | camp | PURP | 3SG | open | IRR | Q
d. Translation: 'Is there room in thy father's house for us to lodge?'

This printed example should replace the older report paraphrase `Inn-ah hong tum theih na hiam`. The dossier is explicit that the exported window for Genesis 24:23 is `Na pa inn-ah kote giah nading a awng ding hiam`, and that attested clause is what the print slice should use. The candidate TSV also records one export caveat: punctuation is attached to the final token in the raw analyzer window, but that punctuation artifact should not be printed as if it were part of `hiam` itself.

### WH + `hiam` content questions

The content-question pattern in the current packet is WH + `hiam`. The safest print-facing claim is therefore not that every WH form behaves identically, but that the present candidate-backed examples show `bang`, `kua`, `bangci`, and `banghangin` in this construction.

(@ex:hiam-bang)
a. Tedim: Bang ahi hiam?
b. Segmentation: Bang | ahi | hiam
c. Gloss: what | be.3SG | Q
d. Translation: 'What is it?'

Exodus 16:15 is the current print anchor for `bang`. The dossier keeps one export caveat explicit: the analyzer glosses `bang` here as `like`. The clause-level evidence and KJV alignment still support the ordinary what-question reading, so the example remains usable in print with that caveat recorded in the packet rather than foregrounded in the example line.

(@ex:hiam-kua)
a. Tedim: Hihte kua ahi hiam?
b. Segmentation: Hihte | kua | ahi | hiam
c. Gloss: these | who | be.3SG | Q
d. Translation: 'Who are these?'

Genesis 48:8 is the current print anchor for `kua ... hiam`, and 2 Samuel 22:32 gives additional support for the same pattern (`Topa longal Pasian kua hiam`). The dossier again keeps the relevant export caveat explicit: `kua` is tagged as `NUM` in the analyzer output. That label should be treated as an export limitation rather than as evidence against the interrogative reading.

(@ex:hiam-bangci) Genesis 3:13
a. Tedim: Bangci a hici gamtat na hi hiam?
b. Segmentation: Bangci | a | hi-ci | gam-tat | na | hi | hiam
c. Gloss: how | 3SG | this-say | conduct-do | 2SG | DECL | Q
d. Translation: 'How have you acted thus?'

Genesis 3:13 is the cleanest current `bangci` row, and it matters methodologically because it should remain visible as `bangci`, not be flattened into a generic `bang` example.

The present packet also keeps Genesis 4:6 as reason-question evidence:

> bang hangin na mai sia ahi hiam

This row is important because it keeps `banghangin` in the slice while also recording the segmentation caveat from the dossier. The analyzer exports the sequence as `bang | hang-in | na | mai | sia | ahi | hiam`, but the current packet still treats the clause as curated reason-question evidence rather than as a raw `bang` hit.

### Embedded questions

The dossier keeps Exodus 16:15 `bang hiam cih thei lo uh hi` visible as embedded-question material, but it is not promoted here as a core independent-clause `hiam` example. It should remain deferred for a later treatment of embedded questions or interrogative complementation, not folded into the first printed outline as if it were interchangeable with the main clause-final examples above.

### Blocked false friends

The packet also shows why raw `hiam` and `bang` matching would overgenerate. `Bang hang hiam cih leh` in Genesis 3:20 is a formulaic explanatory frame, not an ordinary question example. Revelation 1:16 `langnih a hiam namsau` and 2 Kings 11:11 `a hiam ciat uh` are lexical or non-interrogative `hiam` controls rather than question-particle evidence. Likewise, `bangmah` and `bangin` are bang-family false friends and should not be treated as ordinary `bang` interrogatives.

These blocked rows matter because they keep the printed claim small and accurate: the slice prints candidate-backed interrogative examples, not every surface string that happens to contain `hiam` or `bang`.

### Deferred particles

Existing generated reports mention `maw`, `ham`, and `em`, but they remain deferred in this first print slice. They are not part of the core `hiam` evidence printed here, and this section does not yet build a comparison-particle analysis.

### Editorial summary

This slice can now safely support four modest claims. First, `hiam` is the candidate-backed question marker in the current print packet, with clause-final `hiam` as the core pattern represented in the accepted examples. Second, WH + `hiam` is the current content-question pattern. Third, `bang`, `kua`, `bangci`, and `banghangin` are the current candidate-backed WH forms. Fourth, embedded questions and deferred comparison particles remain outside the scope of this first printed analysis.

## Sentence-final particles

*Source slice: `output/publication_review/grammar_sentence_final_particles_print_slice.md`*

### Scope

This is a short print-facing draft section on sentence-final particles in Tedim Chin, controlled by `candidates_sentence_final_particles.tsv` and `dossier_sentence_final_particles.md`.

It covers only a small candidate-backed set: caveated declarative evidence with `ahi hi`; caveated negative-plus-declarative evidence with `thusim lo hi`; optative `hen` in `Khuavak om hen`; singular imperative `in` in `teembaw khat bawl in`, with case-marker overlap caveat; and plural imperative `un` in `gingsak un`, currently the cleanest imperative anchor.

It does not yet attempt a full sentence-final particle system, a full mood or aspect chapter, a full TAM account, a new treatment of `hiam`, a settled analysis of `tahen`, `aw`, `ta`, or `zo`, or generated-report frequency tables. Dictionary and review-note slices have not yet begun.

### Sentence-final particles in outline

The current candidate-backed packet supports a narrow generalization. `Hi` is visible only through constructionally controlled `ahi hi` and `lo hi` rows. `Hiam` is visible only as overlap control because interrogatives are already stabilized. `Hen` has one usable optative row. `In` and `un` represent imperative material, but `in` has case-marker overlap while `un` is cleaner. `Aw` is only vocative or exclamative boundary material and is not print-ready. `Tahen`, `ta`, and `zo` remain deferred or needs-review because the export is noisy. Broad TAM remains deferred.

### Declarative `hi` with copula overlap

Genesis 1:13 supplies the current declarative anchor:

(@ex:sfp-ahi-hi)
a. Tedim: ahi hi
b. Segmentation: ahi | hi
c. Gloss: be.3SG | DECL
d. Translation: 'it was'

This is the current copula-plus-declarative evidence, but only with caveat. It is not a bare `hi` example. The row bundles copular `ahi` with final `hi`, so it does not license raw `hi` harvesting or a claim that every `hi` token is sentence-final declarative.

### Negative-plus-declarative `lo hi`

Genesis 4:5 keeps one negative-plus-declarative environment visible:

(@ex:sfp-lo-hi) Genesis 4:5
a. Tedim: thusim lo hi
b. Segmentation: thusim | lo | hi
c. Gloss: parable | NEG | DECL
d. Translation: 'he had not respect' / 'it was not accepted'

This row keeps `lo hi` visible as a sentence-final environment, but it overlaps the stabilized negation packet. The present slice should not reopen `lo` or build a new negation section here. It is treated as negation-overlap evidence only.

### `Hiam` as interrogatives overlap

Deferred / overlap control:

> `Hihte kua ahi hiam?`

Genesis 48:8 is mentioned here only as cross-reference material. `Hiam` belongs to the stabilized interrogatives packet, so this sentence-final particle slice should not reopen or duplicate `hiam` analysis. The row is not a print anchor for this slice, and the quotation or punctuation noise plus the `kua = NUM` export caveat should remain visible rather than normalized away.

### Optative `hen`

Genesis 1:3 supplies the current usable optative row:

(@ex:sfp-hen) Genesis 1:3
a. Tedim: Khuavak om hen
b. Segmentation: Khuavak | om | hen
c. Gloss: light | exist | JUSS
d. Translation: 'Let there be light'

This is the current usable optative evidence with caveat. The candidate is analyzer-backed as `om hen`, so the slice should not replace it with report-style `ta hen` wording. It also should not turn this narrow row into a broad mood chapter.

### Imperative `in` and `un`

Genesis 6:14 keeps one singular imperative row visible:

(@ex:sfp-in) Genesis 6:14
a. Tedim: teembaw khat bawl in
b. Segmentation: teembaw | khat | bawl | in
c. Gloss: ark | one | make | ERG [export caveat]
d. Translation: 'Make thee an ark'

This keeps singular imperative `in` visible, but only with a serious case-marker and export caveat: `in` is exported as `ERG` / `FUNC`. The candidate also has `teembaw`, not report-style `lawng`. The slice should not harvest raw `in` hits and should not reopen case marking.

Psalms 100:1 supplies the cleanest current imperative anchor:

(@ex:sfp-un)
a. Tedim: gingsak un
b. Segmentation: ging-sak | un
c. Gloss: sound-CAUS | IMP.PL
d. Translation: 'Make a joyful noise'

This is the clean plural-imperative anchor. The span should stay tight so nearby `aw` material in the same verse is not absorbed, and the row should not be used to launch a full imperative paradigm.

### `Aw` as vocative/exclamative boundary material

Boundary material:

> `Gam khempeuh aw`

Psalms 100:1 keeps `aw` visible, but only as vocative or exclamative boundary material. The analyzer glosses `aw` as `voice` and gives `N` in `pos_span`, and the same verse also has another `aw` in `lungdamna aw`. This is therefore not settled sentence-final mood evidence, and raw `aw` hits should not be treated as sentence-final particles.

### `Tahen`, `ta`, and `zo` deferred

Several report-visible rows remain too noisy to promote:

- `hi tahen`: deferred because `tahen` is exported as `army` / `N`; the slice should not normalize fused `tahen` or split `ta hen` into a clean jussive example.
- `mangngilh ta hi`: needs-review TAM-overlap material because `ta` is exported as `child` / `FUNC`.
- `zo`: deferred because the export glosses `zo` as `south` / `N` rather than as clean completive evidence.

These rows keep report-visible material in view, but they are not print-ready as jussive, perfective, or completive evidence. Broad TAM remains deferred.

### Editorial summary

This slice safely supports five modest claims: `ahi hi` is usable as copula-plus-declarative evidence with caveat; `thusim lo hi` is usable as negation-plus-declarative evidence with caveat; `Khuavak om hen` is usable as optative evidence with caveat; `teembaw khat bawl in` is usable as singular imperative evidence only with a case-overlap caveat; and `gingsak un` is the clean plural-imperative anchor.

What remains deferred is equally important: bare `hi` as a general declarative particle, `hiam` as new sentence-final evidence, `tahen` as a settled jussive, `aw` as a settled exclamative or mood particle, `ta` and `zo` as settled aspectual particles, broad TAM and full mood or aspect chapters, and raw generated-report counts. Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work remain deferred.

The next step after this grammar slice is the dictionary print slice at `output/publication_review/dictionary_sentence_final_particles_print_slice.md`. Dictionary and review-note slices have not yet begun.

## Coordinators

*Source slice: `output/publication_review/grammar_coordinators_print_slice.md`*

### Scope

This is a short print-facing draft section on coordinators in Tedim Chin, controlled by `candidates_coordinators.tsv` and `dossier_coordinators.md`.

It covers only a small candidate-backed set: NP coordination with `le`, anchored by Genesis 1:1 `vantung le leitung`; conditional or boundary `leh`, not clean clause-conjunction `leh`; sequential `a` only as caveated boundary material, paired with a blocked agreement-`a` false friend; `mawh` only as deferred lexical or analyzer-noise material; `Ahih hangin` as a caveated adversative connector; and `ahih kei leh` as conditional-adversative boundary material.

It does not yet attempt a full coordination system, a full clause-linking or converb system, a full temporal or causal subordinator treatment, a full sentence-final particle treatment, or generated-report frequency tables. Dictionary and review-note slices have not yet begun.

### Coordinators in outline

The current candidate-backed packet supports a narrow generalization. `Le` currently provides the safe NP-conjunction anchor. `Leh` is visible, but only as conditional or boundary evidence rather than as print-ready simple clause conjunction. `A` is visible only as caveated sequential-linkage boundary evidence and must not be harvested raw. `Mawh` remains deferred until a clean disjunction or alternative-question example is located. `Ahih hangin` is the current adversative connector anchor, with an internal-analysis caveat. `Ahih kei leh` is conditional-adversative boundary material, not a simple coordinator.

### NP coordination with `le`

Genesis 1:1 supplies the clean print-ready anchor:

(@ex:coord-le-np)
a. Tedim: vantung le leitung
b. Segmentation: van-tung | le | lei-tung
c. Gloss: sky-on | and | land-on
d. Translation: 'heaven and earth'

This is the current safe NP-conjunction anchor. It supports a modest print claim that `le` joins noun phrases.

That claim must remain narrow. The row does **not** license broad raw `le` harvesting, and the current packet does not treat every `le` token as coordinator evidence. A separate blocked `le` row was not created in the first pass; overgeneration is controlled here by curated selection rather than by a broad token sweep.

### `Leh` as conditional or boundary material

Genesis 13:9 keeps `leh` visible only as warning or boundary evidence:

(@ex:coord-leh-boundary) Genesis 13:9
a. Tedim: veilam na lak leh kei taklamah ka pai ding hi
b. Segmentation: vei-lam | na | lak | leh | kei | taklam-ah | ka | pai | ding | hi
c. Gloss: faint-direction | 2SG | among | and/if | NEG [export caveat] | right-LOC | 1SG | go | IRR | DECL
d. Translation: 'if thou wilt take the left hand, then I will go to the right'

This row keeps `leh` visible, but not as a clean simple clause-conjunction anchor. The wider English context is conditional, so future coordinator prose must not flatten conditional `leh` into a simple printed "`and`" analysis.

The row also carries an analyzer or export caveat: `kei` is glossed as `NEG` in the selected window even though the wider English context is "I will go." That should be recorded as an export caveat, not used to reopen the pronouns or negation packets.

### Sequential `a` and agreement-`a` false friends

Genesis 2:10 keeps one possible sequential-linkage window visible:

(@ex:coord-a-sequential-boundary) Genesis 2:10
a. Tedim: luang a tua mun panin gun hong kikhenin
b. Segmentation: luang | a | tua | mun | pan-in | gun | hong | kikhen-in
c. Gloss: flow | 3SG | that | place | ABL-ERG | river | 3→1 | separate-CVB
d. Translation: 'and from thence it was parted'

This row keeps possible sequential linkage visible, but it is not print-ready as a core coordinator example. The analyzer still exports the relevant `a` as `3SG` / `FUNC`, so the present slice treats it as warning or boundary evidence only.

Blocked control:

> `a piangsak`

Genesis 1:1 `a piangsak` is blocked agreement or function material, not coordinator evidence. This false-friend control prevents raw `a` harvesting from flooding the coordinator packet.

### `Mawh` deferred

The present slice does not print a positive `mawh` example.

Deferred control:

> `mawh`

The generated report mentions `mawh` as disjunction or alternative-question material, but the current candidate layer only has Genesis 6:3, where `mawh` is lexical or analyzer-noise material glossed as `sin` / `V` rather than as disjunction. `Mawh` therefore remains not print-ready in this slice.

Report-only schematic examples such as `mi mawh ganhing mawh` or `pai ding mawh om ding mawh` should not be printed unless a later analyzer-backed row is actually located.

### Adversative `Ahih hangin`

Genesis 3:4 supplies the current adversative connector anchor:

(@ex:coord-ahih-hangin)
a. Tedim: Ahih hangin
b. Segmentation: Ahih | hang-in
c. Gloss: be.3SG.REL | because-ERG
d. Translation: 'but'

This row is usable with caveat as the current adversative connector. It remains internally analyzable as `ahih` + `hang-in`, so the present slice should not open a full causal or subordinator analysis from this row.

### Conditional-adversative `ahih kei leh`

Exodus 12:3 keeps one compact boundary row visible:

(@ex:coord-ahih-kei-leh)
a. Tedim: ahih kei leh
b. Segmentation: ahih | kei | leh
c. Gloss: be.3SG.REL | NEG | and/if
d. Translation: 'otherwise' / 'if not'

This row is useful as conditional-adversative boundary material, but it is not a simple coordinator. It overlaps with negation and conditional `leh`, yet the slice should not reopen the stabilized negation packet.

### Deferred material

Several limits remain important at this stage:

- clean simple clause-conjunction `leh` remains deferred;
- clean `mawh` disjunction or alternative-question evidence remains deferred;
- full sequential-`a` analysis remains deferred;
- `ciangin` and broader `hangin` temporal or causal subordinator material remain deferred;
- full clause-chaining or converb coordination remains deferred;
- sentence-final particles remain outside the scope of this slice;
- generated-report raw counts remain excluded.

Broad TAM, directionals, chrestomathy, Mizo/lus, and other Kuki-Chin language work likewise remain deferred.

### Editorial summary

This slice now safely supports four modest claims: `le` is the current NP conjunction anchor, anchored by `vantung le leitung`; `Ahih hangin` is usable as an adversative connector with caveat; `ahih kei leh` is useful as conditional-adversative boundary evidence with caveat; and `leh`, `a`, plus `mawh` remain visible only as warning, deferred, or boundary material.

What remains deferred is equally important: raw frequency counts, treating every `le`, `leh`, or `a` token as coordinator evidence, simple clause-conjunction `leh`, `mawh` as accepted disjunction, a full sequential-`a` analysis, a fuller temporal or causal subordinator treatment, and sentence-final particles. The next step after this grammar slice is the dictionary print slice, while dictionary and review-note work have not yet begun.

## Reduplication

*Source slice: `output/publication_review/grammar_reduplication_print_slice.md`*

### Editorial scope

This is the first narrow reduplication grammar slice. It is controlled by `output/publication_review/candidates_reduplication.tsv` and `output/publication_review/dossier_reduplication_scope.md`. Supporting/background evidence comes from `docs/grammar/reports/07-deriv-02-reduplication.md`.

This is not a full derivation chapter, not a full reduplication chapter, not a dictionary slice, and not a TAM/aspect or VP-structure slice. It also stays narrow against `output/publication_review/review_notes_derivation_valency.md`, `output/publication_review/review_notes_nominalization.md`, `output/publication_review/review_notes_vp_structure_stacking.md`, `output/publication_review/review_notes_noun_domain.md`, and `output/publication_review/review_notes_tam.md`.

The present slice therefore covers only the first safe full-reduplication claim. No dictionary slice exists for reduplication, because this packet is grammar-facing and constructional rather than lexical.

### Full reduplication as intensification

`mahmah` is the main full-reduplication intensifier anchor.

The controlled segmentation and gloss/function are `mah~mah` and `EMPH~EMPH / very, truly`.

The report also supports the worked example `pha mahmah hi`, glossed there as `good very DECL`.

`taktak` is the closest support row for the same small intensifying pattern.

Its controlled segmentation and gloss/function are `tak~tak` and `TRUE~TRUE / truly, certainly`.

Taken together, `mahmah` and `taktak` support a narrow full-reduplication intensifier pattern, not the whole reduplication system.

### Secondary distributive evidence

`peuhpeuh` remains visible as secondary distributive evidence for full reduplication.

Its controlled segmentation and gloss/function are `peuh~peuh` and `each~each / every, each`.

It stays outside the leading claim because it is more quantifier-like or noun-modifying than the clean intensifier anchors.

### Boundary material

`ni ni` stays outside the first grammar slice because syntactic X X repetition overlaps with temporal/adverbial and VP-structure interpretation.

`leuleu` stays outside because iterative or continuative reduplication overlaps with TAM/aspect and VP structure.

`gengen` stays outside because the verbal reduplication evidence is too thin for the first print-facing claim.

`kawikawi` stays outside because it is expressive, spatial-totality, or lexicalized-looking material.

`theithei` stays outside because it is report-only and overlaps adverbial, modal, or ability-related territory.

`bangbang`, `bekbek`, `zenzen`, `tuamtuam`, or similar report-only analysis-table rows stay outside because they are not yet controlled enough for the first slice.

analyzer-noisy, count-only, or theory-heavy whole-system claims stay outside because they do not yet produce a safe first print-facing pattern.

Any broad derivation chapter claim stays outside because this packet is not yet ready to widen one narrow full-reduplication slice into a full derivational account.

Any dictionary-entry claim stays outside because this packet is constructional rather than lexical.

### Safe first-slice claim

At the current slice maturity level, the safest reduplication claim is that Tedim has candidate-controlled evidence for full reduplication used in intensification, with `mahmah` / `mah~mah` as the main anchor and `taktak` / `tak~tak` as the closest support row. Distributive `peuhpeuh` remains visible as secondary evidence, while syntactic, aspectual, verbal, lexicalized-looking, and report-only reduplication rows remain candidate-layer or boundary material.

That claim is deliberately smaller than a full derivation chapter, smaller than a full reduplication chapter, smaller than a TAM/aspect or VP-structure slice, and smaller than a dictionary slice.

### Recommended next step

This grammar slice is now paired with `output/publication_review/review_notes_reduplication.md`, so the packet is ready for human review at its current full-reduplication-intensifier slice maturity level.

The next editorial step should be a whole-grammar coverage checkpoint rather than starting another new packet immediately. If more reduplication work is chosen after that checkpoint, the next sub-scope should be distributive `peuhpeuh` or syntactic `ni ni`, not lexicalized-looking or aspect-heavy rows.

## Broader discourse

[MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]

Current packetized material reaches clause type and sentence-final behavior, but a broader discourse packet is still only partly surfaced and remains boundary-heavy.

## Analyzer-gap caution

[MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]

Analyzer-gap topics still cut across tone in `-a`, conditioned variants, hong-/kong-, `-sak`, `-pih`, and related cross-packet boundaries, so they remain visible blockers rather than assembled review prose.

# End state of this preview

This assembled review preview contains the actual prose of the current first-pass publication-review grammar slices in a single ordered draft. It does not claim that the whole grammar is finished, and the generated PDF is a review preview PDF rather than a final publication PDF.
