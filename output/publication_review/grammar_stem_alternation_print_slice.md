---
title: "Tedim Chin Grammar Review Slice: Verb Stem Alternation"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

# Scope

This review slice now uses the hardened lexical inventory rather than the earlier overinclusive analyzer table. The aim is still to discuss Tedim verb-stem alternation as a real grammar topic, but the relevant inventory must now separate genuine verbal evidence from same-form questionnaire controls, stative or adjectival predicates, nominal analyzer rows, lexicalized families, and analyzer-only uncertainties.

# Form I and Form II

Earlier descriptions agree that Tedim has a two-form verbal system, even though the terminology differs. Henderson describes Form I and Form II, while Zam Ngaih Cing speaks of Stem 1 and Stem 2 [@henderson1965; @zamngaihcing2017]. Henderson emphasizes clause type and the contrast between conclusive and inconclusive predication, while Zam Ngaih Cing makes the connection to nominalization, negation, and other morphosyntactic environments more explicit [@henderson1965; @zamngaihcing2017].

The current packet therefore keeps three distinct layers in view:

1. **Lexical-pair status**: whether the item is supported by secondary literature, the Zakaria/VSA questionnaire, the analyzer inventory, the corpus audit, or some combination of those sources.
2. **Bible attestation profile**: whether Form I and Form II are both attested, one-sided, or mainly visible in derived, nominalized, or lexicalized environments.
3. **Promotion status**: whether the pair should be promoted into the main verbal grammar, kept only in the wider inventory, treated as a questionnaire control, or discussed as a difficult case.

That separation matters. Henderson and Zam Ngaih Cing are witnesses to the system, not automatic authorities over every Bible token. Likewise, the hardened example matrix is a review tool, not itself a set of print-safe quotations. The expanded inventory is welcome, but non-verbal analyzer pairs must not inflate the verb-stem alternation discussion.

The new tracked shortlist in `output/publication_review/stem_alternation_citation_shortlist.tsv` adds one more layer: **promoted for grammar discussion** is not identical to **safe as a printed quotation**. Some pairs are now secure enough to discuss grammatically, while their best Tedim citations still need caveated handling or should remain notes-only.

# Citation shortlist and print layer

The shortlist distinguishes four editorial outcomes:

1. **Promoted for grammar discussion and usable as main quotation**: the core showcase set.
2. **Promoted for grammar discussion, but not all equally good first examples**: the caveated promoted set.
3. **Retained as a difficult case**: real and grammatically important, but better mentioned cautiously than quoted as a clean paradigm.
4. **rejected as non-verbal or analyzer noise**: rows that stay in the audit precisely so they do not drift back into the stem-verb prose.

# Core showcase pairs

The cleanest pedagogical material remains concentrated in three pairs. Those still anchor the prose, while the shortlist keeps the larger promoted inventory separate from the printed-example layer.

| Pair | Shortlist lead evidence | Citation status |
| --- | --- | --- |
| `mu ~ muh` | Gen 1:4 `mu`; Gen 19:1 `muh` | Form I print-ready; Form II usable with caveat |
| `ne ~ nek` | Gen 2:17 `ne`; Gen 2:17 `nek` | print-ready |
| `nei ~ neih` | Gen 11:30 `nei`; 2 Sam 23:8 `neih` | print-ready |

# Promoted verbal inventory

The new manual review sheet in `output/publication_review/stem_alternation_manual_promotion_review.tsv` separates the **current** inventory status from the **recommended** grammar promotion decision. In the prose itself, the main promoted table should stay narrow and should not be expanded just because the analyzer can manufacture more pair families.

| Pair | Why it stays in the main promoted table |
| --- | --- |
| `mu ~ muh` | Strong exact Form I and Form II evidence, with dependent and nominalized support that stays lexically transparent. |
| `ne ~ nek` | The Gen 2:17 contrast remains the cleanest same-verse demonstration of Tedim Form I/Form II. |
| `nei ~ neih` | Both forms remain robust and easy to explain without major lexical-family contamination. |

# Caveated promoted verbs

The manual review supports a broader **caveated promoted** inventory. These pairs belong in the grammar, but their best Form II evidence is usually constructionally restricted, domain-specific, or harder to quote cleanly than the three core showcase pairs.

The shortlist makes that distinction explicit. The caveated promoted verbs are **not all equally good first examples**. Some are promoted because they are real lexical pairs with good Bible evidence, while the final printed quotations still need careful selection or should remain supporting citations rather than headline examples.

| Pair | Why it is promoted with caveat |
| --- | --- |
| `za ~ zak` | A genuine alternating pair, but `zak` ranges widely enough that the grammar should keep the example choice conservative. |
| `pia ~ piak` | Strong evidence on both sides, but exact examples still need filtering away from nearby derivational material. |
| `nusia ~ nusiat` | Form II is clearest in dependent and clause-linking contexts rather than in a neat finite pedagogical contrast. |
| `bia ~ biak` | Clean exact verbal rows survive on both sides, but Form II is still concentrated in worship and offering contexts. |
| `thei ~ theih` | Both forms are abundant and real, but Form II is especially strong in modal, ability, purposive, and nominalized environments. |
| `piang ~ pian` | Exact `piang` and `pian` rows survive after filtering, but the pair is easiest to explain under eventive and dependent usage rather than as a simple finite paradigm. |
| `zui ~ zuih` | Both forms are cleanly attested, but a final citation set still needs to avoid `zuihsak`-family noise. |
| `khial ~ khialh` | Both forms are usable, but the `khialsak` family still creates derivational crowding around otherwise good examples. |
| `kia ~ kiak` | The Form II side is thinner than for the best pairs, but the surviving exact rows are still strong enough for grammar discussion. |
| `sawlkhia ~ sawlkhiat` | Both forms are attested, but the Form II side is sparse enough that the pair should stay explicitly caveated. |

The row-level shortlist now prefers:

1. exact verbal tokens when they exist;
2. Form II rows whose Tedim clause clearly shows dependent, purposive, modal, attributive, or clause-linking syntax;
3. notes-only treatment when a pair is real but the surviving citation is still too thin or constructionally awkward for print.

# One-sided Bible attestations and questionnaire controls

One-sided Bible attestations are not a reason to drop a verb from the lexical discussion. They are a reason to label it honestly and keep it out of the promoted alternating-verb tables until both sides are philologically secure.

| Row type | Examples | Editorial treatment |
| --- | --- | --- |
| Same-form questionnaire controls | `dawn ~ dawn`, `hong ~ hong`, `om ~ om`, `ci ~ ci`, `hi ~ hi`, `bawl ~ bawl`, `zui ~ zui`, `pai ~ pai` | Keep as controls; do **not** treat them as overt alternating pairs in the promoted verbal inventory. |
| One-sided or constructionally skewed lexical verbs | `dipkua ~ dipkuat`, `gen ~ genh`, `hawlkhia ~ hawlkhiat`, `husia ~ husiat`, `kho ~ khoh`, `kido ~ kidot`, `lua ~ luah`, `tu ~ tuh`, `tuahpha ~ tuahphat`, `vial ~ vialh`, `bawl ~ bawlh` | Keep in the wider inventory and manual review sheet, but do not promote them until a clean verbal row survives on the missing or unstable side. |
| One-sided analyzer or questionnaire items | `om ~ omh`, `pai ~ paih` | Keep visible with clear blocking notes, but do not promote them into the verbal tables yet. |

No separate Karius, Kariuss, or Karias questionnaire file is present in the repository. The questionnaire layer used here is the in-repo Zakaria/VSA material in `scripts/generate_vsa_report.py`, `docs/paradigms/5-verb-11-vsa-questionnaire.md`, and `docs/grammar/reports/05-verb-11-vsa-questionnaire.md`.

# Stative/adjectival and functional predicates

The widened inventory also contains categories that are grammatically relevant but should not inflate the main lexical-verb table.

| Category | Examples | Editorial treatment |
| --- | --- | --- |
| Stative/adjectival predicate | `no ~ noh` | Mention only as a possible predicative alternation, not as a promoted lexical verb. |
| Auxiliary or functional verb | `ci ~ cih`, `hi ~ hih`, `om ~ omh` | Discuss separately from lexical verbs. `ci ~ cih` is real and important, but it behaves primarily as quotative or functional verbal material. `hi ~ hih` and `om ~ omh` still suffer from category mismatch or one-sided evidence in the current Bible layer. |

# Analyzer-only uncertain rows

Some rows are worth retaining precisely because they show where the analyzer inventory outruns the current philological control.

| Row type | Examples | Why they stay out of the main promoted table |
| --- | --- | --- |
| Analyzer-only uncertain | `mu ~ muk`, `pai ~ paih`, `pua ~ puah`, `tua ~ tuak`, `tua ~ tuah` | The analyzer proposes a pair, but the Bible evidence is still mixed, shared-base, or category-uncertain. |

# Blocked nominal and non-verbal analyzer rows

The manual review also keeps clearly non-verbal analyzer pairs visible as blocked rows rather than letting them drift back into the stem-verb prose.

| Row type | Examples | Why they stay blocked |
| --- | --- | --- |
| Nominal or compound-like analyzer rows | `mual ~ mualh`, `sum ~ sumh`, `thu ~ thuh`, `lampi ~ lampih`, `khua ~ khuat`, `gamla ~ gamlat`, `keu ~ keuh` | Current Bible hits are nominal, locative, or compound-like rather than clean verbal evidence. |
| Weakly verbal or category-mismatched rows | `khai ~ khaih`, `sia ~ siah`, `tan ~ tanh` | The best Bible hits are still non-verbal, category-mixed, or too noisy to justify promotion. |

# Nominalized and dependent evidence

The main descriptive generalization remains structural, not mechanical. Form I is clearest in ordinary finite predication. Form II is especially clear in nominalized, dependent, purposive, relative/attributive, and other non-final environments. That is why `mu ~ muh`, `ne ~ nek`, and `nei ~ neih` remain so strong, and it is also why several real verbs remain caveated rather than disappearing from the discussion.

Negative clauses remain relevant but not diagnostic on their own. The grammar should still avoid slogans like "Form II = negative" or "Form II = subordinate." The more accurate generalization is that Form II is especially visible in dependent, nominalized, purposive, and other non-final environments.

# Difficult but grammatically important cases

Several rows remain central to the grammar precisely because the manual review shows both why they matter and why they should **not** be promoted mechanically.

1. `ngai ~ ngaih` now has to be described more carefully: clean exact verbal `ngai` and `ngaih` rows do survive, but the `ngaihsun/ngaihsut/ngaihsutna` family still creates too much lexical-family contamination for ordinary promotion.
2. `pua ~ puak` also keeps real verbal evidence on both sides, but the shared Form I base, gloss mismatch, and competition with `pua ~ puah` still make it a difficult-case item rather than a promoted pair.
3. `pua ~ puah` remains analyzer-only uncertain because the Form II side is cleaner than the Form I side.
4. `tua ~ tuak` and `tua ~ tuah` remain analyzer overgeneration problems: the base `tua` is too often determiner-like or otherwise category-mixed to support lexical promotion.
5. `honkhia ~ honkhiat` and `hu ~ huh` remain excluded from simple stem-alternation prose because the current evidence is lexicalized, category-mixed, or both.

# Retained difficult and rejected citation candidates

The shortlist now keeps difficult and rejected items visible under separate labels instead of letting them blur together.

| Shortlist group | Examples | Editorial use |
| --- | --- | --- |
| Difficult but still grammatically relevant | `ngai ~ ngaih`, `pua ~ puak` | Mention without overpromoting them as clean citation pairs. |
| Inventory-only or analyzer-only uncertain | `pai ~ paih`, `tua ~ tuak`, `tua ~ tuah` | Keep in notes until the lexical and category problems are resolved. |
| Rejected as non-verbal or analyzer noise | `keu ~ keuh`, `khai ~ khaih`, `sia ~ siah`, `tan ~ tanh` | Keep blocked; do not recycle these into the promoted citation set. |

# Editorial summary

The hardened lexical inventory is better than the earlier broad table because it now asks the right question: **is this a genuine verbal stem-alternation item, and if so, what kind of evidence supports promoting it?** The new manual review layer pushes that one step further by separating the inherited inventory status from the editorial promotion decision, and the citation shortlist separates promotion from quotation.

The result is a broader but still controlled packet. The three main showcase pairs remain stable. The caveated promoted inventory is now larger: in addition to `za ~ zak`, `pia ~ piak`, `nusia ~ nusiat`, and `bia ~ biak`, the grammar can now discuss `thei ~ theih`, `piang ~ pian`, `zui ~ zuih`, `khial ~ khialh`, `kia ~ kiak`, and `sawlkhia ~ sawlkhiat` as genuine lexical verbs with caveated evidence. At the same time, same-form questionnaire controls, functional or stative predicates, analyzer-only uncertainties, difficult-case lexical families, and blocked nominal rows stay visible without inflating the promoted verbal inventory or the printed citation set.
