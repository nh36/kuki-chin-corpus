# Tedim Chin Grammar Review Slice: Case Marking and Postpositions

## 1. Scope and editorial status

This review slice tests whether the current Tedim grammar pipeline can be turned into continuous, print-facing prose for one manageable domain: nominal case marking and closely related postpositions. It draws on the routed grammar materials, the corpus-based case-marking report, the example-selection audit, and the case-marker literature review. The present draft is not a full chapter. It is an editorial slice intended to show what can already be written in prose and where the current backend still fails to supply safe print examples.

The section concentrates on four markers that are central both in the literature and in the corpus reports: ergative **-in**, locative **-ah**, ablative/source **-pan / -panin**, and comitative **-tawh**. A short note on relator nouns is included because the safest locative and ablative examples already pass through relational nouns such as *laizang* ‘middle/inside region’ and *lak* ‘among’. In other words, the material itself shows that Tedim spatial grammar cannot be described cleanly by isolating case markers from relational nominal stems.

## 2. Case marking in outline

Earlier descriptions agree that Tedim marks core and oblique nominal relations post-nominally, but they differ in terminology and granularity. Henderson describes forms such as **-in**, **-ah**, and **-tawh** structurally as post-nominal particles rather than in modern typological terms. Zam Ngaih Cing, by contrast, presents a more explicit seven-case inventory, including ergative, locative, ablative, and comitative. The corpus-facing materials in this repository broadly support that later functional analysis, but they also show that homography and segmentation noise make some markers much easier to print safely than others.

The clearest print lesson from the current pipeline is methodological: case marking can already be discussed confidently when the selected corpus evidence lines up with the literature and with stable segmentation, but the chapter still needs editorial supervision whenever a high-frequency string is also used elsewhere in the verbal system. The problem is sharpest with **-in**, which is frequent enough to dominate the backend counts but currently too ambiguous for automatic inclusion as a clean ergative example.

## 3. Ergative **-in**

The literature is consistent in assigning **-in** to transitive subjects. Zam Ngaih Cing explicitly defines it as an ergative marker, and Otsuka likewise uses **-in** for causers in causative constructions. Henderson does not frame the system in ergative-absolutive terms, but her structural description of phrase-final nominal particles is compatible with the later analysis. For a print grammar, then, the grammatical claim itself is not the problem. The problem is example control.

At present the backend does **not** supply a draft-ready Bible example for ergative **-in**. The audit shows why. Current linked rows are dominated by forms such as *bei-in* ‘finish-CVB/ERG-like segmentation’, *cil-in*, and other clause-final or verbal strings that are not safe nominal ergatives. In other words, the repository can already say that Tedim has ergative **-in**, but it cannot yet print a Bible example automatically without risking confusion between nominal ergative marking and homographic verbal morphology.

For a print-facing chapter, the responsible wording is therefore conservative: **-in** should be described as the ergative marker known from the descriptive literature, but the chapter should carry an explicit editorial note that a manually confirmed Bible example still needs to be chosen before this subsection is camera-ready. This is preferable to printing an automatically selected false example simply to fill the slot.

## 4. Locative **-ah**

The locative marker **-ah** is in much better shape. Henderson already treats it as a post-nominal locative particle, while Zam Ngaih Cing describes it as marking both location and destination. The corpus evidence supports that analysis, but it also shows that many naturally occurring examples involve relational nouns rather than simple bare nouns. That does not weaken the case analysis; instead, it shows that Tedim spatial grammar is built from the interaction of case morphology and a class of relational nominal stems.

One safe example comes from the creation account:

> **Genesis 1:6**  
> Pasian in, “Tuite' **laizangah** van kuumpi om hen la, tua van kuumpi in tui le tui kikhensak hen,” ci hi.  
> *lai-zang-ah*  
> middle-side-LOC  
> ‘And God said, Let there be a firmament in the midst of the waters, and let it divide the waters from the waters.’

This example is especially useful because it shows a structure that is frequent in the corpus reports: the locative is attached not directly to a simple noun but to a relational form (*laizang* ‘middle/interior region’). In prose, that means **-ah** should not be presented only as a simple “at/in” suffix. It is also the case marker that completes larger spatial expressions built on relational nouns.

The second safe example is more straightforward:

> **Genesis 1:15**  
> leitung khua a vaksak dingin **vantungah** khuavak hi uh hen,” ci hi.  
> *vantung-ah*  
> heaven-LOC  
> ‘and let them be for lights in the firmament of the heaven to give light upon the earth: and it was so.’

Taken together, these two examples support a print description along the following lines: **-ah** marks static location, but the noun phrase it attaches to may already encode a relational geometry such as ‘middle’, ‘inside’, or ‘surface’. The boundary between “locative case” and “relator-noun construction” is therefore one of grammatical layering rather than a strict either/or contrast.

## 5. Ablative and source marking: **-pan** and **-panin**

The source marker **-pan** is one of the easier cases to synthesize because the literature, the postposition report, and the audit all align well. Zam Ngaih Cing describes **-pan** as an ablative marking source or point of departure, and the corpus report confirms that both separate and attached spellings are common. The current grammar output safely selects an example with the relator noun *lak* ‘among, amid’, giving a form that is semantically transparent even though it is not the simple textbook combination *inn-pan* ‘from the house’.

> **Matthew 5:19**  
> Tua ahih manin hih thukhamte **lakpan** a neupente khat bek nangawn zuikha loin, midangte in zong a zuih loh nadingin a gen mite pen vantung ki-ukna sungah mi neupen hi ding uh hi.  
> *lak-pan*  
> midst-ABL  
> ‘Whosoever therefore shall break one of these least commandments, and shall teach men so, he shall be called the least in the kingdom of heaven …’

This is a good print example because it shows a real Tedim source construction rather than an invented citation form. At the same time, it again demonstrates that the most usable corpus evidence for case marking is often embedded in relational nominal syntax. The relevant print generalization is that **-pan** marks source or point of departure, but many natural instances are built on nouns such as *lak* ‘among’, *sung* ‘inside’, or *kiang* ‘beside’.

The corpus materials also make clear that **-panin** deserves mention as a related source form. In the postposition report it is much commoner than bare **-pan** in many relational environments. For print purposes, the safest wording at this stage is that **-panin** is a source-marking extension that often behaves adverbially and occurs heavily in fused or tightly integrated spellings. The generated reports contain many instances, but they still need editorial triage before the grammar can decide whether to present **-panin** as a straightforward case form, a postposition-plus-particle sequence, or a family of related source-marking constructions.

## 6. Comitative **-tawh**

The comitative marker **-tawh** is already close to printable. Henderson documents it among the post-nominal particles, and Zam Ngaih Cing explicitly glosses it as comitative, ‘with’. The corpus report, however, shows that accompaniment and instrument-like uses overlap. That overlap is visible even in the two safest Bible examples currently selected by the grammar.

In Genesis 2:21, **-tawh** marks the material used to close Adam’s side:

> **Genesis 2:21**  
> Tua ahih ciangin Topa Pasian in mipa ihmut suak mahmah sak a, ama ihmut kalin a nakguhte khat la-in tua mun pen **satak tawh** a dimsak hi.  
> *tawh*  
> COM  
> ‘And the LORD God caused a deep sleep to fall upon Adam, and he slept: and he took one of his ribs, and closed up the flesh instead thereof.’

Genesis 2:7 gives a more instrumental-material reading:

> **Genesis 2:7**  
> Topa Pasian in leilak pana **leivui tawh** mihing bawl a, a nak sungah nuntakna hu sang suk hi.  
> *tawh*  
> COM  
> ‘And the LORD God formed man of the dust of the ground, and breathed into his nostrils the breath of life …’

These two examples suggest that a print grammar should not flatten **-tawh** into a single English gloss. “With” is still the right starting gloss, but the prose should note that the same marker can cover accompaniment, association, and at least some material or instrument-like relations. The chapter should therefore present **-tawh** as a comitative-postpositional marker with a semantic range broader than simple human accompaniment.

## 7. Relator nouns and the shape of the final chapter

Although this slice is organized around case markers, the current evidence repeatedly points beyond simple case suffixes to relational nouns such as *sung* ‘inside’, *kiang* ‘beside’, *lak* ‘among’, and *tung* ‘on’. The relator-noun report shows just how central they are: forms such as *sungah*, *kiangah*, and *tungah* are not marginal embellishments but high-frequency spatial constructions. The locative and ablative sections above already rely on that fact. The safe locative example is built on *laizang-ah*, and the safe ablative example is built on *lak-pan*.

For a final print grammar, this means the chapter should probably be structured in two layers. One layer treats **-ah**, **-pan**, and **-tawh** as general case/postpositional markers. The second layer treats relational nouns as stems that regularly host those markers and create more specific spatial meanings. The current backend cannot yet route relator nouns into draft-ready grammar prose automatically, but the reports already make the editorial necessity clear.

## 8. Editorial summary for this slice

This case-marking slice is a good candidate for the first print-facing review packet because it already shows both strengths and limitations of the current pipeline. Locative, ablative, and comitative material can be turned into genuine prose with Bible evidence. Ergative **-in**, by contrast, is not blocked by lack of linguistic analysis but by lack of a safe automatically selected Bible example. That is exactly the kind of problem a review slice should expose before the project scales up to larger grammar chapters.

In its present state, the section is strong enough for editorial review, but not yet for typesetting. The next improvement should not be more dashboard material; it should be manual confirmation of one or two secure ergative Bible examples and a deliberate editorial decision about how strongly to separate case markers from relator-noun constructions in the printed grammar.
