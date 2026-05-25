---
title: "Tedim Chin Negation Evidence Dossier"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

This dossier is the research layer for a future Tedim negation print slice. It treats the current negation report as a discovery aid, not as final authority, and checks its claims against the aligned Bible corpus before any print-facing grammar or dictionary prose is drafted. Unless otherwise noted, the scan counts below are direct verse-level regex counts over the Tedim column of `data/verses_aligned.tsv`; they are useful for distributional shape, but they are not lemmatized totals, and raw `kei` counts are inflated by homography with the 1SG pronoun.[^method]

# Literature expectations

The secondary literature does **not** support reducing Tedim negation to a single marker `lo`. Henderson's discussion foregrounds `-kei`, treating it as a negative adverb and illustrating it in ordinary verbal negation, in cessative contexts such as `kuan nawn kei`, and in prohibitive uses such as `nui nui kei un` [@henderson1965]. On Henderson's evidence alone, `-kei` is already central enough that a Tedim negation summary cannot be written as if `lo` were the whole system.

Zam Ngaih Cing goes further and explicitly describes a two-negator system: `-kei` and `-lou/-louh` [@zamngaihcing2017]. In her account, `-lou/-louh` is stem-sensitive, with the `-h` shape associated with Stem 2 environments, while `-kei` is available with both stems and is especially prominent in prohibitives and in first-person realis contexts [@zamngaihcing2017]. That makes two predictions worth testing in the Bible corpus: first, that the orthographic contrast `lo` vs `loh` should not be random; second, that `kei` should do more than just add emphasis.

Zam Ngaih Cing also mentions an informal negative `-da'`, but she explicitly treats it as non-standard for written usage [@zamngaihcing2017]. Nothing in the current Bible data makes `-da'` a useful organizing category for a print slice, and raw `dah` searches would be confounded by unrelated lexical material. The dossier therefore keeps `-da'` in the background only.

Comparative Sukte is useful as background, but not as direct Tedim evidence. Singh's Sukte description likewise distinguishes `lo` and `kei`, and it treats `kei`-based material as central to verbal negation and prohibitives [@sukte_grammar]. That comparison makes the Tedim `lo/kei` split more plausible typologically, but the print-facing Tedim account still has to stand on Tedim corpus evidence rather than on Sukte analogy.

# Current report audit

The current report at `docs/grammar/reports/06-func-04-negation.md` is useful as a first pass, but several of its headline claims are too simple or actively misleading.

| Current report claim | Dossier finding | Status |
| --- | --- | --- |
| `lo` is the primary negation marker. | Bare `lo` is very common, but the Bible also uses exact-token `loh`, and negative `kei` is too well attested to be treated as marginal. | too simple |
| Prohibitive = `V lo uh`. | The report's example, Genesis 2:25 `maizum lo uh hi`, is declarative "they were not ashamed", not a prohibition. Real prohibitives are dominated by `kei` patterns such as `lau kei in`, `su kei in`, `kuanto kei un`. | wrong |
| `kei` is only an emphatic side form. | Bible data shows `kei` in ordinary negation, quoted prohibitions, commands, and conditional/irrealis material such as `hi-kei-leh`; it is not just ornamental emphasis. | too simple |
| `loh` can be ignored. | The corpus has many exact `loh` hits, and they cluster in dependent or derived environments such as `muh loh dingin`, `nek loh ding`, `theih loh nadingin`. The sample grammatical dictionary already separates `Loh` from `lo`. | wrong by omission |
| `V lo hi`, `V lo ding`, `om lo`, and `nawn lo` define the main system. | These are all real and important, but they are only part of the system; the report underplays `kei`, ignores `loh`, and does not distinguish clause-level negation from dependent negative morphology. | incomplete |
| `thei lo` / `theih lo` can be treated as a single transparent category. | `thei lo` is common and useful. Exact `theih lo` is extremely rare in the current scan, while `theih loh` and broader `X theih loh nadingin` patterns are much more frequent. | needs correction |
| `kuamah` and `bangmah` require negative context. | Broadly right for the true NPI uses, but raw string counts overgenerate because `kuamah` also appears in non-pronominal strings and `bangmah` also has non-NPI uses such as `tua bangmah ahi hi` "likewise / that same way". | broadly right, but needs filtering |

The generated grammar layer already hints at a broader system by labeling the topic "Negation lo and kei" in `output/grammar/grammar_full.md`, but the currently selected grammar examples are not enough for a print slice. Job 24:10 `silh-lo-in` is useful for a "without X" type construction, and Leviticus 18:28 `hi-kei-leh` is useful for conditional negation, but neither one on its own gives a reader the core Tedim negation system.

# Corpus search

The direct scan confirms the broad outline of the literature, but not in the simplified form of the current report. Exact token `lo` appears in 5,026 verses, exact token `loh` in 810 verses, and exact token `kei` in 5,245 verses; the `kei` figure cannot be read as a negation count because many of those hits are simply the 1SG pronoun. Even so, the corpus gives a stable evidence set for the main negation categories.

## Standard declarative negation

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 4:5 | `Kain le ama piakna thusim lo hi.` | "unto Cain and to his offering he had not respect" | clean clause-level `V lo hi` negation | print-ready |
| Genesis 11:30 | `Sarai ... ta nei lo hi.` | "Sarai was barren; she had no child." | ordinary predicate negation with `nei lo hi` | print-ready |
| Genesis 24:50 | `... nang tungah kong gen ding dang uh om lo hi.` | "we cannot speak unto thee bad or good" | negative existence / possibility inside ordinary clause negation | print-ready |
| Job 24:10 | `silh-lo-in` | "without clothing" | negative morphology is real, but this is not the best central example for core sentential negation | usable with caveat |

## Negated irrealis, future, and obligation with `ding`

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 3:1 | `Huan sung singgah ... ne lo ding` | "Ye shall not eat ..." | straightforward `V lo ding` future/prohibitive quotation | print-ready |
| Genesis 2:17 | `na ne kei ding hi` | "thou shalt not eat" | `kei` in a quoted command/future prohibition; central counterexample to "negation = lo" | print-ready |
| Genesis 17:15 | `ama min Sarai na ci nawn kei ding` | "thou shalt not call her name Sarai" | `kei ding` in a divine directive, not first-person realis | print-ready |
| Deuteronomy 17:16 | `na kilehkik ngei kei ding uh hi` | "ye shall henceforth return no more that way" | `kei` plus `ding` in legal-prohibitive style | print-ready |

## Negative existence: `om lo`

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 2:20 | `... amah a huh ding khat zong om lo hi.` | "there was not found an help meet for him" | clean existential negation | print-ready |
| Exodus 8:10 | `Topa ahi kote' Pasian tawh a kibang kuamah om lo hi` | "there is none like unto the LORD our God" | existential negation with NPI subject | print-ready |
| Genesis 37:24 | `a sungah tui om lo hi` | "there was no water in it" | straightforward negative existence | print-ready |
| Genesis 39:9 | `... a kep tuam bangmah om lo hi` | "neither hath he kept back any thing" | combines existential negation with `bangmah` | print-ready |

## Cessative and aspectual `nawn lo`

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 8:12 | `hong ciahkik nawn lo hi` | "returned not again" | clear cessative / "no longer" use | print-ready |
| Genesis 17:5 | `Na min Abram hi nawn lo ding` | "Neither shall thy name any more be called Abram" | negated continuation plus `ding` | print-ready |
| Genesis 26:22 | `kitawng nawn lo uh hi` | "they strove not" | plural negative clause, not a prohibitive | print-ready |
| Genesis 24:56 | `... zekaisak nawn kei un` | "Hinder me not" | cessation plus `kei`; useful but already in imperative discourse | usable with caveat |

## Ability and inability: `thei lo`, `theih lo`, `theih loh`

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 27:23 | `amah in thei lo hi` | "he discerned him not" | clean `thei lo` inability / non-recognition | print-ready |
| Genesis 37:4 | `amah hopih thei lo uh hi` | "could not speak peaceably unto him" | plural clause with modal inability | print-ready |
| Exodus 33:20 | `ka maitang na mu thei kei ding hi` | "Thou canst not see my face" | modal inability with `thei` plus `kei` | print-ready |
| Exodus 10:5 | `leitang a muh theih loh nadingin` | "that one cannot be able to see the earth" | dependent `theih loh` pattern; shows that the report's `theih lo` label is too simple | usable with caveat |
| 1 Corinthians 2:7 | `mite' theih lo dingin` | "hidden wisdom" | exact `theih lo` is rare and not a good core Bible example | ambiguous |

## Negative polarity items

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Exodus 2:12 | `kuamah mu lo ahih manin` | "when he saw that there was no man" | clean `kuamah` plus negative predicate | print-ready |
| Genesis 41:8 | `a gen thei kuamah om lo hi` | "there was none that could interpret" | NPI plus existential negation | print-ready |
| Genesis 22:12 | `Ama tungah bangmah hih kei in.` | "do thou any thing unto him" | `bangmah` under prohibitive `kei` | print-ready |
| Genesis 39:9 | `... bangmah om lo hi` | "neither hath he kept back any thing" | negative predicate licenses `bangmah` | print-ready |
| Exodus 27:11 | `tua bangmah hi-in` | "likewise ..." | non-NPI lexical use; raw searches overcount this string | unsuitable as NPI evidence |

## Prohibitives and negative imperatives

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 15:1 | `Lau kei in.` | "Fear not" | singular prohibitive with `kei in` | print-ready |
| Genesis 19:17 | `Nunghei kei unla, ... khawl kei un.` | "look not ... neither stay" | plural prohibitives with `kei un` | print-ready |
| Genesis 22:12 | `Tangvalpa su kei in. Ama tungah bangmah hih kei in.` | "Lay not thine hand ... do not any thing" | especially strong paired prohibitive example | print-ready |
| Leviticus 10:9 | `leenggahzu ... ne kei un` | "Do not drink wine nor strong drink" | legal prohibitive with `kei un` | print-ready |
| Numbers 14:42 | `kuanto kei un ... do kei un` | "Go not up, neither fight" | double imperative negation with `kei un` | print-ready |
| Genesis 2:25 | `maizum lo uh hi` | "they were not ashamed" | declarative plural negative, not a command | unsuitable |

## Analyzer-aware candidate audit

The original negation dossier relied on raw verse-level scans as distributional clues. Those counts remain useful for orientation, but they are not the preferred evidence layer for future publication-review work because raw `kei`, `bangmah`, and `V lo uh` searches overgenerate.

Negation now has an analyzer-aware candidate file at `output/publication_review/candidates_negation.tsv`. That file records accepted, excluded, and deferred negation candidates with analyzer-backed token spans, verse references, and manual review notes. The existing packet should now be read through the sequence `candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`, so the dossier interprets filtered candidate evidence rather than doing the first major cleanup of raw-string noise.

## Negative clauses relevant to stem alternation

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 2:17 | `na ne kei ding hi` | "thou shalt not eat" | negative command with Form I `ne` | print-ready |
| Genesis 3:11 | `na nek loh dinga kong thupiak` | "I commanded thee that thou shouldest not eat" | Stem II `nek` plus dependent `loh`; strong overlap with literature expectations | print-ready |
| Isaiah 6:10 | `a muh loh nading ... a zak loh nading ... a theihtel loh nading` | "lest they see ... hear ... understand" | repeated dependent `loh` in clause-linking negative material | print-ready |
| Exodus 10:5 | `muh theih loh nadingin` | "that one cannot be able to see" | layered negative plus ability morphology; good for caution, not for a first pedagogical example | usable with caveat |

# `lo`, `loh`, and `kei`

The Bible corpus clearly uses both `lo` and `kei`, and it also uses orthographic `loh`. The question is not whether these forms exist, but how distinctively they behave.

Bare `lo` is the easiest clause-level negator to document. It is abundant in `V lo hi`, `V lo ding`, `om lo`, `nawn lo`, and in many ordinary negative predicates such as `thusim lo hi`, `nei lo hi`, and `om lo hi`. If the future print slice needs one core "simple negation" marker, `lo` is the safest place to begin.

`Loh` is not just a random spelling variant of `lo`. In the direct scan it patterns heavily with dependent and derived environments: the most frequent following strings are `nadingin`, `nadingun`, `nading`, and `ding`. Corpus examples such as Genesis 3:8 `muh loh dingin`, Genesis 3:11 `nek loh dinga`, Exodus 23:11 `nek loh teng`, Exodus 10:5 `muh theih loh nadingin`, and Isaiah 6:10 `muh loh nading / zak loh nading / theihtel loh nading` all show `loh` in clause-linking, purposive, or otherwise non-finite material. The Bible orthography therefore does distinguish `lo` and `loh`, and the distribution matches the literature better than the current report allows.

`Kei` is harder because the same exact form also spells the 1SG pronoun. Raw string counts therefore overstate its negative frequency. Even so, the negative use of `kei` is secure and central. It appears in ordinary negation (`ka thei kei hi`, Exodus 5:2 `ka paisak kei ding hi`), in quoted future or irrealis prohibitions (`na ne kei ding hi`), in conditional material (`hi-kei-leh`), and especially in negative imperatives (`lau kei in`, `su kei in`, `kuanto kei un`). Bible data therefore supports treating `kei` as an ordinary negator in at least some constructions, not merely as an emphatic afterthought.

Does the Bible support Zam Ngaih Cing's two-negator distinction? Partly. The corpus strongly supports a three-way editorial distinction between clause-level `lo`, dependent/derived `loh`, and `kei`-based prohibitive or irrealis-heavy negation. It does **not** yet support a fully rigid rule set of the kind "first-person realis always takes `kei` and `lo` never does X". First-person contexts are not the only place where negative `kei` occurs; many of the clearest Bible examples are second-person commands, legal directives, or quoted warnings. The safest conclusion is therefore: the Bible corpus broadly supports Zam Ngaih Cing's contrast, but it does not confirm every stated distributional restriction cleanly enough to print as a rigid rule.

# Prohibitives and negative imperatives

The current report's prohibitive section needs correction before it can feed a print slice. Genesis 2:25 `maizum lo uh hi` is simply a declarative plural negative predicate, "they were not ashamed". It is not an imperative, not a warning, and not evidence for a prohibitive construction.

Real prohibitives are easy to find once the search is centered on `kei` rather than on `lo uh`. The cleanest evidence is:

| Reference | Tedim form | Marker | Imperative/plural marking | Comment | Status |
| --- | --- | --- | --- | --- | --- |
| Genesis 15:1 | `Lau kei in` | `kei` | singular | classic "fear not" prohibitive | print-ready |
| Genesis 19:17 | `Nunghei kei un`, `khawl kei un` | `kei` | plural | strong paired command context | print-ready |
| Genesis 22:12 | `su kei in`, `bangmah hih kei in` | `kei` | singular | strongest single prohibitive verse in current dossier | print-ready |
| Leviticus 10:9 | `ne kei un` | `kei` | plural | legal / ritual prohibition | print-ready |
| Numbers 14:42 | `kuanto kei un`, `do kei un` | `kei` | plural | explicit military prohibition | print-ready |
| Exodus 20:20 | `Lau kei un` | `kei` | plural | direct admonition to the people | print-ready |

The report's broader surface claim about `V lo uh` also needs revision. The string `lo uh` is certainly common, but many of its occurrences are ordinary plural negatives rather than commands: Genesis 2:25 `maizum lo uh hi`, Genesis 32:32 `ne lo uh hi`, Genesis 35:5 `delh lo uh hi`, and Genesis 37:4 `hopih thei lo uh hi` are all declarative. A future print slice may still mention that plural negatives often end in `... lo uh hi`, but it should not identify that surface string as the prohibitive construction.

# Negative polarity items

The current report is broadly right that true NPI uses of `kuamah` and `bangmah` occur under negation, but raw search results have to be filtered carefully.

For `kuamah`, the cleanest pattern is NPI plus negative predicate or existential negation: Exodus 2:12 `kuamah mu lo`, Genesis 41:8 `a gen thei kuamah om lo hi`, Leviticus 16:17 `kuamah om lo ding hi`, and Deuteronomy 32:39 `... kuamah om lo hi` all support the report's core claim. But raw `kuamah` string counts also pull in non-pronominal strings involving valley names or other lexical material, so the exact frequency is not identical to the number of true "nobody / no one" uses.

For `bangmah`, the negative dependency is also strong in the real NPI cases: Genesis 22:12 `bangmah hih kei in`, Genesis 39:9 `bangmah om lo hi`, and Genesis 19:22 `bangmah ka hih thei kei hi` are all clean. But `bangmah` also has non-NPI uses such as Exodus 27:11 `tua bangmah hi-in` "likewise / in the same way", so a print slice should not cite raw counts without manual filtering.

The print-facing implication is simple: `kuamah` and `bangmah` are good negation-slice material, but they need manually checked examples and a note that exact-string search overgenerates.

# Recommendation for print slice

**B. Negation is ready, but only if certain report claims are corrected first.**

The next task can be a negation print-facing grammar/dictionary slice, but only after the following corrections are made explicit:

1. The slice must not flatten the system to `lo` alone. It should treat `lo`, `loh`, and `kei` together, with `lo` as the safest clause-level starting point, `kei` as central to prohibitives and many irrealis-heavy negatives, and `loh` as a dependent/derived negative form visible in `... loh ding(in)` and `... loh nading(in)` environments.
2. The current report's prohibitive section must be corrected. Genesis 2:25 must be removed as a prohibitive example, and the slice should instead foreground real `kei` prohibitives such as Genesis 15:1, Genesis 19:17, Genesis 22:12, Leviticus 10:9, and Numbers 14:42.
3. The slice should not present `V lo uh` as the prohibitive pattern. It is better analyzed as an ordinary plural-negative surface string that sometimes appears in non-imperative clauses.
4. The ability subsection must distinguish common `thei lo` from much rarer exact `theih lo`; many of the report's apparent `theih lo` examples are better described as `theih loh` or broader dependent negative constructions.
5. The NPI subsection should keep `kuamah` and `bangmah`, but only with manually checked examples and with a warning that raw string counts include non-NPI material.

With those corrections in place, negation looks like the right next narrow print-facing slice. It is broad enough to be interesting, but still focused enough to avoid collapsing into a full TAM chapter or into directionals.

[^method]: Direct scan notes from this dossier pass: exact-token verse counts include `lo` in 5,026 verses and `loh` in 810 verses. Exact-token `kei` appears in 5,245 verses, but that number is not a negation count because it also includes the 1SG pronoun. Pattern searches used exact-space strings such as `thei lo`, `theih lo`, `nawn lo`, `om lo`, `V lo ding`, and context windows around `kei`; these are reproducible from `data/verses_aligned.tsv` without changing repository code.
