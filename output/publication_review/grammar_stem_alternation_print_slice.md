---
title: "Tedim Chin Grammar Review Slice: Verb Stem Alternation"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

# Scope

This review slice tests whether the project can now produce a short print-facing treatment of Tedim verb stem alternation. It focuses on the opposition traditionally called Form I and Form II, on a small set of manually checked Bible examples, and on how paired stems should be represented in print dictionary entries. It does not attempt a full verb chapter, a TAM chapter, or an inventory of every alternating verb in the corpus.

# Form I and Form II

Earlier descriptions agree that Tedim has a two-form verbal system, even though the terminology differs. Henderson describes Form I and Form II, while Zam Ngaih Cing speaks of Stem 1 and Stem 2 [@henderson1965; @zamngaihcing2017]. Henderson's account emphasizes clause type, especially the contrast between conclusive and inconclusive verbal phrases, whereas Zam Ngaih Cing gives a more explicitly morphosyntactic account in which Stem 2 is associated with negatives, nominalizations, and certain derived environments [@henderson1965; @zamngaihcing2017].

The project's generated stem inventory and paradigm tables confirm that the alternation is lexically widespread. Pairs such as `mu ~ muh`, `ne ~ nek`, `nei ~ neih`, `thei ~ theih`, `pia ~ piak`, and `piang ~ pian` are all visible in the current report layer. What is not yet safe enough is automatic editorial packaging. The current `output/grammar/grammar_full.md` and `output/grammar/example_selection_audit.md` still leave stem alternation without a draft-ready backend example, so the present slice uses manually selected Bible verses rather than inheriting auto-selected quotations.[^reports]

# Main environments for stem alternation

For print purposes, the safest generalization is narrower than any one-line formula such as "Form II is subordinate" or "Form II is negative." The Bible corpus does support a real distributional contrast, but it shows that the opposition is expressed especially clearly when one compares ordinary finite predication with dependent, derived, or nominalized environments. That is the level at which the current material is strongest enough for print.

(@ex:stem-mu)
a. Tedim: Pasian in tua khuavak hoih hi, ci-in a mu hi. Pasian in khuamial panin khuavak khenkhia hi.
b. Segmentation: mu
c. Gloss: see.I
d. Translation: "And God saw the light, that it was good: and God divided the light from the darkness."

(@ex:stem-muh)
a. Tedim: en un, note' muhna-ah na nasempa in maipha muzo a, ka nuntakna nong hutna uhah migitna lianpi kei tungah nong lak khin uh hi.
b. Segmentation: muh-na
c. Gloss: see.II-NMLZ
d. Translation: "behold now, thy servant hath found grace in thy sight, and thou hast magnified thy mercy, which thou hast shewed unto me in saving my life"

Genesis 1:4 is a straightforward finite predicate and gives a good Form I example of `mu`. Genesis 19:19, by contrast, does not merely repeat the same verb in a different translation. The relevant form is `muhna-ah` "in your sight", a nominalized dependent phrase. That contrast is stronger print evidence than a loose appeal to English "see" alone, because it shows Form II surfacing inside a derived nominal expression rather than in the final predicate of the clause.

(@ex:stem-ne-nek)
a. Tedim: Ahih hangin a pha le a sia theihna singkung gah pen na ne kei ding hi. Bang hang hiam cih leh tua na nek ni-in na si ding hi, a ci hi.
b. Segmentation: ne ... nek
c. Gloss: eat.I ... eat.II
d. Translation: "but of the tree of the knowledge of good and evil, thou shalt not eat of it: for in the day that thou eatest thereof thou shalt surely die"

Genesis 2:17 is especially valuable because it places both forms in one verse. The finite prohibition has `na ne kei ding hi`, while the temporal dependent clause has `na nek ni-in`. The same verse also contains `theihna`, which confirms that Stem II is at home in nominalized material as well as in clause-linking environments. This is the kind of evidence a printed chapter should foreground: one verse can show the alternation structurally, not just lexically.

# Stem alternation and clause/sentence structure

The alternation matters not only inside verbal paradigms, but also in how Tedim builds noun phrases and clause chains. Many of the clearest corpus examples of Form II are not bare finite verbs at all. They appear in nominalizations, relative-like expressions, and other dependent constructions that are structurally central to Tedim prose.

(@ex:stem-nei-neih)
a. Tedim: Tu-in Sarai ciing a, ta nei lo hi.
b. Segmentation: nei
c. Gloss: have.I
d. Translation: "But Sarai was barren; she had no child."

(@ex:stem-neih)
a. Tedim: David' neih mi thahatte' minte: Tahkhemon mi Joshebbasshebeth hi a, amah pen mi thumte a ukpa ahi hi.
b. Segmentation: nei-h
c. Gloss: have.II-NOM
d. Translation: "These be the names of the mighty men whom David had: the Tachmonite that sat in the seat, chief among the captains"

The pair `nei ~ neih` makes the point clearly. Genesis 11:30 has ordinary finite `nei`, while 2 Samuel 23:8 uses `neih` in a derived nominal expression meaning roughly "the men David had". The difference is not a separate dictionary sense. It is the same lexical stem participating in a clause-structure contrast that the printed dictionary should represent explicitly.

(@ex:stem-piang-pianna)
a. Tedim: Ofir, Havilah, le Jobab' pianna pa ahi hi. Hihte khempeuh Joktan' tapate ahi hi.
b. Segmentation: pian-na
c. Gloss: be.born.II-NMLZ
d. Translation: "and Ophir, and Havilah, and Jobab: all these were the sons of Joktan."

The `piang ~ pian` pair is slightly less tidy in surface distribution than `mu ~ muh` or `ne ~ nek`, because the Bible corpus often shows the Form II side through derived forms such as `pianna` or `a pian nadingin` rather than through a simple isolated bare `pian`. Even so, Genesis 10:29 is good print evidence that the pair should be represented in the dictionary. The important editorial move is to record the pair while also telling the reader that the corpus most readily displays Form II in derived environments.

# Stem alternation and transitivity

The current transitivity report is useful here mainly because it shows what stem alternation is not. Many alternating pairs fall into the report's ambitransitive middle band rather than forming a neat transitive versus intransitive split. `mu/muh`, `ne/nek`, `nei/neih`, and `thei/theih` all cluster outside a simple lexical-valency opposition. That is a warning against turning Form II into a transitivity label. The more plausible editorial summary is that stem choice tracks clause type and derivational environment more strongly than lexical transitivity alone.

At the same time, valency still matters for how alternating verbs are presented in a print dictionary. Ditransitives such as `pia ~ piak` need examples that preserve argument structure rather than isolated citation forms.

(@ex:stem-pia-piak)
a. Tedim: Mipa in, "Kei tawh a om dinga nong piak numei in singgah hong pia a, ke'n ka ne hi," ci hi.
b. Segmentation: piak ... pia
c. Gloss: give.II ... give.I
d. Translation: "And the man said, The woman whom thou gavest to be with me, she gave me of the tree, and I did eat."

Genesis 3:12 is a good manual example because it puts `nong piak` and `hong pia` in one speech turn. That is enough to justify a paired dictionary entry for `pia ~ piak`. It is not enough to claim that the current autogenerated questionnaire already handles the whole distribution cleanly, so this pair should remain manually curated in print-facing work.

# Paradigm examples

The following mini-paradigm is narrow by design. It records only pairs for which the current packet has manually checked Bible support.

| Pair | Representative corpus evidence | Editorial note |
| --- | --- | --- |
| `mu ~ muh` | Gen 1:4 `mu`; Gen 19:19 `muhna-ah` | Strong finite vs nominalized contrast; draft-ready. |
| `ne ~ nek` | Gen 2:17 `ne` ... `nek` | One-verse contrast; draft-ready. |
| `nei ~ neih` | Gen 11:30 `nei`; 2 Sam 23:8 `neih` | Strong finite vs derived nominal contrast; draft-ready. |
| `thei ~ theih` | Gen 3:2 `thei`; Gen 2:17 `theihna` | Real pair, but Form II is mostly surfaced through derived forms here and the Form I side overlaps with modal use; needs review. |
| `piang ~ pian` | Gen 1:9 `a piang pah hi`; Gen 10:29 `pianna` | Pair is supported, but Form II is most visible through derived forms; needs review. |
| `pia ~ piak` | Gen 3:12 `nong piak` ... `hong pia` | Good manual contrast, but current autogenerated report examples remain noisy; needs review. |

# Editorial summary

This slice now supports a genuine print-facing treatment of Tedim verb stem alternation. The literature and the manually checked Bible evidence agree that a Form I and Form II contrast is real and central. The safest prose, however, is still cautious prose. Form I is straightforward in ordinary finite predication, while Form II is clearest in dependent and derived environments, especially nominalizations and certain clause-linking contexts. The current backend is good enough to inventory pairs, but not yet good enough to choose print examples automatically or to flatten the whole system into a single rule about subordination, negation, or transitivity.

[^reports]: The main current weakness is not the existence of stem alternation, but the reliability of automatic example selection. Some verb sections in `05-verb-11-vsa-questionnaire.md` are visibly noisier than others, and the generated grammar layer still marks the topic as review-only. That is why this slice keeps the evidence set small and manually checked.
