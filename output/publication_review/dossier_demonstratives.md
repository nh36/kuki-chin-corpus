---
title: "Tedim Chin Demonstratives and Deixis Evidence Dossier"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

This dossier is the research layer for a future Tedim demonstratives/deixis print slice. It treats the current demonstratives report as a discovery aid, not as final authority, and checks its claims against the aligned Bible corpus before any print-facing grammar or dictionary prose is drafted. Unless otherwise noted, scan counts below are case-normalized verse-level regex counts over the Tedim column of `data/verses_aligned.tsv`; they are useful for distributional shape, but they are not lemmatized totals, and forms such as `hi` and apparent `hih ciangin` strings require manual filtering.[^method]

# Scope

This dossier asks whether the Tedim Bible corpus supports a narrow demonstratives/deixis slice built around `hih` and `tua`, their plural forms, and a small number of clearly demonstrative constructions. It does **not** attempt a full treatment of copulas, sentence-final particles, directionals, or broad discourse structure. It also does not assume that every high-frequency string in the generated report is a safe dictionary or grammar entry.

# Literature expectations

The literature points to a basic two-way demonstrative contrast. Henderson does not isolate demonstratives in a large paradigm table, but her Tedim examples use `hih` "this" and `tua` "that" in ways consistent with a proximal/distal opposition [@henderson1965]. At the level of broad expectation, the Bible corpus ought therefore to show a core contrast between a proximal form and a distal or anaphoric form.

Zam Ngaih Cing is more explicit. She gives proximal `híʔ` and distal `huā`, describes demonstratives as pre-head modifiers in the noun phrase, and derives plural demonstratives with `-té` [@zamngaihcing2017]. She also gives locative derivatives built from the demonstrative base plus additional morphology [@zamngaihcing2017]. That creates three questions for Bible data: whether the corpus supports the same two-way contrast, whether plural forms behave transparently as DEM + `-te`, and whether the Bible orthography's frequent distal `tua` should be treated as equivalent to Zam Ngaih Cing's `huā`.

Comparative Sukte supports the same broad typology. Singh likewise gives a proximal/distal pair and plural demonstratives in `-te` [@sukte_grammar]. This is helpful background, but not direct Tedim evidence. The Tedim slice still has to be built from Tedim Bible usage, especially because the Bible's dominant distal form is `tua`, not the exact spelling `hua`.

# Current report audit

The current report at `docs/grammar/reports/06-func-02-demonstratives.md` is useful as a first-pass inventory, but its examples and some of its counts cannot yet be treated as print-safe.

| Current report claim | Dossier finding | Status |
| --- | --- | --- |
| Tedim has a two-way proximal/distal system `hih` / `tua`. | Strongly supported. Both forms are widespread and easy to confirm manually. `tua` is especially frequent in narrative and discourse-anaphoric use. | broadly right |
| Plural forms are `hihte` and `tuate`. | Supported. The Bible corpus clearly uses `hihte` and `tuate`, and the forms behave transparently as DEM + `-te`. | right |
| `hi` is the short proximal demonstrative and can be handled inside the demonstrative system. | Not yet supported as a safe print claim. Exact-token `hi` is overwhelmingly frequent, but its collocations are mostly clause-final, copular, or particle-like. No clean `hi pen` pattern surfaced in the current scan, while `hih pen` is common. | too simple |
| `hih bangin` and `tua bangin` are good demonstrative-manner constructions. | Broadly right, but the report's sample verses cannot simply be trusted. Its Genesis 6:22 example actually has `tua bangmahin`, not `hih bangin`. | needs manual correction |
| `hih ciangin` and `tua ciangin` are parallel temporal demonstrative expressions. | `tua ciangin` is strongly supported. Exact `hih ciangin` is not: many apparent hits are verbal `... na hih ciangin` "when you do", and the report's Genesis 18:10 example does not contain demonstrative `hih ciangin`. | only half right |
| John 1:19 shows a good `hi` demonstrative/copular example. | The aligned verse does not match the report's demonstrative quotation. In the current corpus line, John 1:19 contains `na hi hiam?`, an identity question, not a clear proximal demonstrative entry. | wrong example |

The report is therefore best treated as a discovery layer. It identifies the right domain, but it still needs verse-by-verse checking before any print slice is drafted.

# Corpus search notes

The case-normalized verse scan gives the following broad profile:

| Form or pattern | Verse hits | Dossier note |
| --- | --- | --- |
| `hih` | 4,478 | common proximal form |
| `tua` | 10,002 | very common distal/anaphoric form |
| `hihte` | 295 | transparent proximal plural |
| `tuate` | 556 | transparent distal plural |
| `hih bangin` | 668 | productive manner/discourse construction |
| `tua bangin` | 390 | productive manner/discourse construction |
| `tua ciangin` | 3,853 | very common temporal/discourse linker |
| `tua ahih ciangin` | 1,412 | very common discourse-temporal linker |
| `hih ciangin` | 19 | many hits are false friends with verbal `hih` "do" |
| `hih thu` | 491 | productive proximal matter/topic phrase |
| `tua thu` | 156 | productive anaphoric "that matter / it" phrase |
| `hi` | 26,090 | far too ambiguous to treat as a safe demonstrative entry without further filtering |
| `hua` | 38 | real, but mostly spatial "that side / yonder" material rather than the corpus-default distal determiner |

These counts already show two important asymmetries. First, `tua` is much commoner than `hih`, which makes sense in narrative discourse where anaphoric "that/then" expressions dominate. Second, `hi` is so frequent and so collocationally diffuse that it cannot simply be folded into the demonstratives dossier as if it were the short form of `hih`.

# Core demonstratives: `hih` and `tua`

The Bible corpus strongly supports a two-way core system built around `hih` and `tua`. `Hih` is the clearest proximal form in equative or deictic identification:

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 5:1 | `Hih pen Adam’ suanlekhakte’ laibu ahi hi.` | "This is the book of the generations of Adam." | clean proximal pronominal/topic use with `hih pen` | print-ready |
| Genesis 9:12 | `Hih pen ... thuciamna lim ahi hi.` | "This is the token of the covenant ..." | clear proximal identificational use | print-ready |
| Exodus 32:9 | `Hih mite ka mu zo hi.` | "I have seen this people ..." | clean adnominal proximal determiner | print-ready |

`Tua` is also a core demonstrative, but its Bible profile is broader than simple spatial "that". It is frequent in adnominal reference, discourse anaphora, and temporal linkage:

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 1:6 | `tua van kuumpi` | "that firmament / the firmament" | clean adnominal distal/anaphoric determiner | print-ready |
| Genesis 21:27 | `tua mi nihte` | "both of them" | determiner with numeral/classifier-like noun phrase | print-ready |
| Genesis 1:3 | `tua ciangin khuavak om pah hi` | "and there was light" | discourse-temporal linker built from `tua` | print-ready |

The safest descriptive label is therefore not just "distal", but "distal/anaphoric". The narrative corpus uses `tua` constantly to resume events, chain clauses, and refer back to already activated discourse material.

# Plural demonstratives: `hihte` and `tuate`

The plural forms behave exactly as the literature predicts: demonstrative base plus `-te` [@zamngaihcing2017; @sukte_grammar].

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 10:20 | `Hihte pen ... Ham’ suanlekhakte ahi hi.` | "These are the sons of Ham ..." | clear proximal plural topic/pronominal use | print-ready |
| Genesis 48:8 | `Hihte kua ahi hiam?` | "Who are these?" | standalone proximal plural pronoun | print-ready |
| Genesis 2:19 | `mipa in tuate bang a ci hiam` | "what he would call them" | clear distal plural pronoun | print-ready |
| Genesis 7:20 | `tuate tungah` | "upon them / upon those" | pronominal distal plural inside postpositional phrase | print-ready |

Nothing in the current Bible evidence suggests that `hihte` or `tuate` need special treatment beyond DEM + `-te`. They are good candidates for direct dictionary treatment if a later print slice is drafted.

# Adnominal vs pronominal use

The core forms participate in both adnominal and pronominal constructions.

Adnominal use is straightforward: `hih` and `tua` precede the noun phrase they modify. Good examples include Exodus 32:9 `Hih mite`, Genesis 1:6 `tua van kuumpi`, Genesis 21:27 `tua mi nihte`, and the productive matter/topic phrases `hih thu` and `tua thu`.

Pronominal use is equally clear. `Hih pen` in Genesis 5:1 and Genesis 9:12 identifies something already pointed out in discourse, while `Hihte kua ahi hiam?` in Genesis 48:8 shows the plural proximal form as an independent pronoun. `Tuate` in Genesis 2:19 and Genesis 7:20 behaves the same way on the distal side.

The dossier therefore supports a single lexical treatment in which the same forms can be used adnominally and pronominally, rather than separate headwords for determiner and pronoun uses.

# Discourse and temporal deixis

This is the part of the system where `tua` clearly outruns `hih`.

`Tua ciangin` is one of the strongest discourse-temporal linkers in the Bible corpus:

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 1:3 | `tua ciangin khuavak om pah hi` | "and there was light" | clean clause-chaining "then" | print-ready |
| Genesis 5:5 | `tua ciangin amah si hi` | "and he died" | repeated narrative/temporal linker | print-ready |
| Genesis 19:22 | `Tua ahih ciangin tua khuapi min Zoar kici hi.` | "Therefore the name of the city was called Zoar." | discourse-sequencing plus explanation | print-ready |

`Tua ahih ciangin` is also firmly established as a discourse bridge:

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 2:19 | `Tua ahih ciangin Topa Pasian in ...` | "And out of the ground the LORD God formed ..." | event-linking discourse transition | print-ready |
| Genesis 2:21 | `Tua ahih ciangin Topa Pasian in ...` | "And the LORD God caused ..." | another clean transition frame | print-ready |
| Genesis 1:21 | `Tua ahih ciangin Pasian in ...` | "So God created ..." | narrative consequence / continuation | print-ready |

By contrast, exact `hih ciangin` is **not** yet a safe demonstrative construction. Most apparent hits are strings like `na hih ciangin` or `ka hih ciangin`, where `hih` is the verb "do/be thus", not the proximal demonstrative. The report's Genesis 18:10 example does not contain demonstrative `hih ciangin`, and the current exact-space search yields only a handful of noisy hits. A future slice should therefore treat `tua ciangin` and `tua ahih ciangin` as strong candidates, but defer `hih ciangin`.

The matter/topic phrases `hih thu` and `tua thu` also belong here. `Hih thu` often points to the present matter, oath, or instruction (Genesis 24:9; Exodus 3:14), while `tua thu` is frequently anaphoric "that matter / it" after hearing or reporting (Genesis 6:6; Genesis 34:7; Exodus 2:15). These are real discourse-deictic patterns, but they look more like productive NP combinations than mandatory standalone dictionary headwords.

# Manner and comparative demonstrative constructions

Both `hih bangin` and `tua bangin` are real, but they should be built from manually checked examples rather than from the report's auto-selected verses.

| Reference | Tedim | KJV | Grammatical note | Status |
| --- | --- | --- | --- | --- |
| Genesis 32:4 | `hih bangin na ci ding uh hi` | "Thus shall ye speak ..." | clean proximal manner/discourse instruction | print-ready |
| Genesis 42:18 | `hih bangin gamta un` | "This do, and live" | instructional proximal manner | print-ready |
| Exodus 14:30 | `Topa in tua bangin ... honkhia` | "Thus the LORD saved Israel ..." | clear distal/anaphoric manner/result expression | print-ready |
| Genesis 50:21 | `Amah in tua bangin ... amaute a hehnem hi.` | "And he comforted them ..." | manner/discourse resumption with `tua bangin` | print-ready |

This is also a point where the current report needs caution. Its Genesis 6:22 sample does **not** give plain `hih bangin`; the aligned verse has `tua bangmahin`. The manner constructions themselves are solid, but the dossier should not promote the report's sample lines without checking them.

# The special problem of `hi`

`Hi` is the hardest item in this dossier, and the safest conclusion is that it should be deferred.

Exact-token `hi` appears in 26,090 verses, far more often than any core demonstrative. Its top preceding tokens are clause-final or auxiliary-like items such as `uh`, `ding`, `ci`, `ahi`, and `lo`, while its common following tokens include `a`, `ci`, `hiam`, `ding`, `lo`, `ahi`, `hih`, and `tua`. That collocational profile is not what a simple adnominal demonstrative looks like.

The current manual examples point in the same direction. Genesis 48:18 has `Hi lo hi, pa aw; hih pen a suak masa ahi hi`, where `hi` is part of an identity correction, not a clean standalone demonstrative entry. Genesis 17:1 `Kei, Vanglian Pasian ka hi hi` and Genesis 20:6 `Hi hi ... kei mahmah ka hi hi` show `hi` in copular or sentence-final environments. Just as important, a quick scan found no clean `hi pen` pattern, while `hih pen` is common and stable.

The literature still matters here. Zam Ngaih Cing's proximal `híʔ` certainly suggests a formal relationship between `hih` and shorter hi-like material [@zamngaihcing2017]. But the current Bible dossier cannot safely convert that relationship into a print dictionary entry for `hi` without collapsing copular, sentence-final, and deictic functions into one bucket. The right editorial move is to flag `hi` for later work under copula or sentence-final particles, not to treat it as settled demonstrative material now.

# Dictionary implications

The strongest future dictionary candidates are:

| Candidate | Dossier assessment | Note |
| --- | --- | --- |
| `hih` | strong candidate | core proximal demonstrative |
| `tua` | strong candidate | core distal/anaphoric demonstrative |
| `hihte` | strong candidate | transparent proximal plural |
| `tuate` | strong candidate | transparent distal plural |
| `hih bangin` | promising constructional entry | real manner/discourse construction |
| `tua bangin` | promising constructional entry | real manner/discourse construction |
| `tua ciangin` | strong constructional candidate | common temporal/discourse linker |
| `tua ahih ciangin` | strong constructional candidate | common discourse transition |
| `hih ciangin` | defer | raw hits are mostly not demonstrative |
| `hi` | defer | too entangled with copular/sentence-final material |

`Hih thu` and `tua thu` are also real and productive, but they look more like useful subsection material than obligatory headwords. A future print slice should mention them as discourse-deictic NP patterns rather than rush them into the first dictionary shortlist.

The `tua` / `hua` issue needs an explicit editorial warning. The literature's `huā` is clearly related to distal deixis [@zamngaihcing2017], but the Bible corpus overwhelmingly uses `tua` for the core distal/anaphoric determiner. Exact `hua` does occur in the Bible, but the checked examples are mostly spatial forms like `hua lamah`, `hua lampang`, or "on that side / yonder" material rather than the high-frequency distal determiner. A future slice should therefore note the relation as plausible but unresolved, not silently flatten everything into a single orthographic equation.

# Recommendation for print slice

Demonstratives/deixis looks like a good next narrow print-facing topic, but only if the slice follows this dossier rather than the current generated report.

The safest next-step profile is:

1. Build the slice around `hih` and `tua` as the core demonstratives, with `tua` explicitly treated as distal/anaphoric rather than merely spatial.
2. Include `hihte` and `tuate` as transparent plural extensions.
3. Treat `hih bangin`, `tua bangin`, `tua ciangin`, and `tua ahih ciangin` as the strongest constructional extensions.
4. Do **not** promote `hih ciangin` as a core entry yet.
5. Defer `hi` to later work on copula or sentence-final particles.
6. Keep the `tua` / `hua` relation as an editorial caution rather than a solved identity claim.

With those limits, demonstratives are ready for a narrow print slice after review. The main thing still missing is not more raw searching, but disciplined selection: the first slice must correct the generated report's shaky examples and keep `hi` out of the core demonstrative inventory until its non-deictic uses are handled separately.

[^method]: Case-normalized verse-level regex counts in this dossier were run directly over the Tedim column of `data/verses_aligned.tsv`. They are meant only as distributional clues. Exact `hi` overgenerates because it includes copular and sentence-final uses, and exact `hih ciangin` overgenerates because many hits involve verbal `hih` rather than the proximal demonstrative.
