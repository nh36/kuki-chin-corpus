---
title: "Tedim Chin Grammar Review Slice: Verb Stem Alternation"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

# Scope

This review slice now aims at a broader target than the earlier packet. It still does not attempt a full verb chapter or a full TAM chapter, but it does try to show that Tedim verb-stem alternation can be discussed through a larger lexical inventory rather than through only three or four showcase pairs. The key question is no longer just "which quotations are safe enough to print?" but also "which lexical items belong in the grammatical discussion at all, and what kind of Bible evidence actually supports each one?"

# Form I and Form II

Earlier descriptions agree that Tedim has a two-form verbal system, even though the terminology differs. Henderson describes Form I and Form II, while Zam Ngaih Cing speaks of Stem 1 and Stem 2 [@henderson1965; @zamngaihcing2017]. Henderson emphasizes clause type and the contrast between conclusive and inconclusive predication, while Zam Ngaih Cing makes the connection to nominalization, negation, and other morphosyntactic environments more explicit [@henderson1965; @zamngaihcing2017].

The corpus now supports a stronger editorial distinction than the earlier packet did. The new `output/publication_review/stem_alternation_lexical_inventory.tsv` separates three layers:

1. **Lexical-pair status**: whether the item is supported by secondary literature, the Zakaria/VSA questionnaire, the analyzer inventory, the corpus audit, or some combination of those sources.
2. **Bible attestation profile**: whether Form I and Form II are both attested, one-sided, or mainly visible in derived, nominalized, or lexicalized environments.
3. **Print-example safety**: whether any exact token is currently print-ready, print-usable with caveat, dossier-only, or excluded.

That separation matters. Henderson and Zam Ngaih Cing are witnesses to the system, not automatic authorities over every Bible token. Likewise, the hardened `output/publication_review/stem_alternation_example_matrix.tsv` is a review tool, not itself a set of print-safe quotations. It is useful because it makes the corpus distribution inspectable, but it does **not** mean that every matrix row, or every Form II-looking token, belongs in print prose unchanged.

# Clean showcase pairs

The cleanest pedagogical material remains concentrated in a small set of pairs. Those still anchor the prose, but they no longer define the whole lexical discussion.

| Pair | Showcase evidence | Current print layer |
| --- | --- | --- |
| `mu ~ muh` | Gen 1:4 `mu`; Gen 19:19 `muhna-ah` | print-ready |
| `ne ~ nek` | Gen 2:17 `ne`; Gen 2:17 `nek` | print-ready |
| `nei ~ neih` | Gen 11:30 `nei`; 2 Sam 23:8 `neih` | print-ready |
| `za ~ zak` | Gen 3:8 `za`; Gen 24:52 `zak` | print-usable with caveat |
| `pia ~ piak` | Gen 3:12 `pia`; Gen 3:12 `piak` | print-usable with caveat |
| `nusia ~ nusiat` | Gen 2:24 `nusia-in`; Deut 2:14 `nusiat` | print-usable with caveat |

# Larger lexical inventory

The inventory is deliberately broader than the print-example layer: not every non-print-ready verb is omitted from discussion. Some verbs are securely alternating but still need manual example control; some are one-sided in the Bible but are still worth listing because the literature or questionnaire flags them; and some are included precisely so the difficult cases can be discussed explicitly instead of disappearing into a false "clean examples only" picture.

Sources are abbreviated as **lit** (Henderson/Zam-facing review layer), **VSA** (the in-repo Zakaria questionnaire/report material), **analyzer**, and **Bible** (current corpus audit / exact-form scan).

| Pair | Sources | Bible attestation profile | Recommended grammar treatment | Print-example layer |
| --- | --- | --- | --- | --- |
| `mu ~ muh` | lit+VSA+analyzer+Bible | both forms attested cleanly | core paradigm example | print ready |
| `ne ~ nek` | lit+VSA+analyzer+Bible | both forms attested cleanly | core paradigm example | print ready |
| `nei ~ neih` | lit+VSA+analyzer+Bible | both forms attested cleanly | core paradigm example | print ready |
| `gamla ~ gamlat` | analyzer+Bible | both forms attested cleanly | ordinary inventory entry | needs analyzer review |
| `mu ~ muk` | analyzer+Bible | both forms attested, but constructionally complex | ordinary inventory entry | needs analyzer review |
| `nusia ~ nusiat` | lit+analyzer+Bible | both forms attested cleanly | ordinary inventory entry | print usable with caveat |
| `pia ~ piak` | lit+VSA+analyzer+Bible | both forms attested cleanly | ordinary inventory entry | print usable with caveat |
| `za ~ zak` | lit+VSA+analyzer+Bible | both forms attested cleanly | ordinary inventory entry | print usable with caveat |
| `bia ~ biak` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `ci ~ cih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `dipkua ~ dipkuat` | analyzer+Bible | both forms attested, but constructionally complex | discuss under nominalized/dependent evidence | needs analyzer review |
| `hawlkhia ~ hawlkhiat` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `hi ~ hih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `keu ~ keuh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `khai ~ khaih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `khial ~ khialh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `kho ~ khoh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `khua ~ khuat` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `kia ~ kiak` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `kido ~ kidot` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `lampi ~ lampih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `lua ~ luah` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `mual ~ mualh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `no ~ noh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `pai ~ paih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `piang ~ pian` | lit+VSA+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | dossier only |
| `pua ~ puak` | VSA+analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `sawlkhia ~ sawlkhiat` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `si ~ sit` | lit+VSA+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `sia ~ siah` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `sum ~ sumh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `tan ~ tanh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `thu ~ thuh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `tu ~ tuh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `tua ~ tuak` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `tuahpha ~ tuahphat` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `vial ~ vialh` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `zui ~ zuih` | analyzer+Bible | both forms attested cleanly | discuss under nominalized/dependent evidence | needs analyzer review |
| `thei ~ theih` | lit+VSA+analyzer+Bible | both forms attested cleanly | discuss under modal/constructional complexity | dossier only |
| `honkhia ~ honkhiat` | lit+analyzer+Bible | noisy or lexicalized evidence only | discuss under lexicalized/excluded cases | exclude for now |
| `hu ~ huh` | lit+VSA+Bible | noisy or lexicalized evidence only | discuss under lexicalized/excluded cases | exclude for now |
| `kho ~ khot` | analyzer+Bible | noisy or lexicalized evidence only | discuss under lexicalized/excluded cases | needs analyzer review |
| `ngai ~ ngaih` | lit+VSA+analyzer+Bible | both forms attested cleanly | discuss under lexicalized/excluded cases | dossier only |
| `sak ~ sak` | VSA+Bible | noisy or lexicalized evidence only | discuss under lexicalized/excluded cases | needs analyzer review |
| `bawl ~ bawl` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `ci ~ ci` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `dawn ~ dawn` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `hi ~ hi` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `hoih ~ hoih` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `hong ~ hong` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `khawl ~ khawl` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `khen ~ khen` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `khum ~ khum` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `lei ~ lei` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `lian ~ lian` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `nuam ~ nuam` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `om ~ om` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `pai ~ pai` | lit+VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `rin ~ rin` | VSA | not attested in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `tom ~ tom` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `uk ~ uk` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `zawh ~ zawh` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `zui ~ zui` | VSA+Bible | Form I only in Bible | mention as literature/questionnaire one-sided item | needs analyzer review |
| `bawl ~ bawlh` | analyzer+Bible | Form I only in Bible | omit pending stronger evidence | needs analyzer review |
| `gen ~ genh` | analyzer+Bible | Form I only in Bible | omit pending stronger evidence | needs analyzer review |
| `husia ~ husiat` | analyzer+Bible | Form I only in Bible | omit pending stronger evidence | needs analyzer review |
| `ne ~ neh` | analyzer+Bible | Form II only in Bible | omit pending stronger evidence | needs analyzer review |
| `om ~ omh` | analyzer+Bible | Form I only in Bible | omit pending stronger evidence | needs analyzer review |
| `pua ~ puah` | analyzer+Bible | Form II only in Bible | omit pending stronger evidence | needs analyzer review |
| `tua ~ tuah` | analyzer+Bible | Form II only in Bible | omit pending stronger evidence | needs analyzer review |

# One-sided Bible attestations

One-sided Bible attestations are not a reason to drop a verb from the grammar. They are a reason to label it honestly. The inventory therefore keeps same-form questionnaire items such as `dawn ~ dawn`, `pai ~ pai`, `hong ~ hong`, `om ~ om`, `ci ~ ci`, `hi ~ hi`, `bawl ~ bawl`, and `zui ~ zui`, but it treats them as one-sided Bible attestations because the current corpus does not independently show a distinct written Form II for them. Where the analyzer proposes a distinct partner such as `paih`, `cih`, `hih`, `omh`, `bawlh`, or `zuih`, that analyzer row is kept separately rather than being collapsed into the same-form questionnaire row.

No separate Karius, Kariuss, or Karias questionnaire file is present in the repository. The questionnaire layer used here is the in-repo Zakaria/VSA material in `scripts/generate_vsa_report.py`, `docs/paradigms/5-verb-11-vsa-questionnaire.md`, and `docs/grammar/reports/05-verb-11-vsa-questionnaire.md`.

# Nominalized and dependent evidence

The main descriptive generalization is still structural, not mechanical. Form I is clearest in ordinary finite predication. Form II is especially clear in nominalized, dependent, purposive, relative/attributive, and other non-final environments. The strongest examples remain:

- `mu ~ muh`: Gen 1:4 `mu` versus Gen 19:19 `muhna-ah`
- `ne ~ nek`: Gen 2:17 `na ne kei ding hi` versus `na nek ni-in`
- `nei ~ neih`: Gen 11:30 `nei` versus 2 Sam 23:8 `neih`
- `za ~ zak`: Gen 3:8 `za` versus Gen 24:52 `a zak ciangin`
- `pia ~ piak`: Gen 3:12 `pia` and `piak` in one speech turn
- `nusia ~ nusiat`: Gen 2:24 `nusia-in` versus Deut 2:14 `nusiat a kipan`

This is also why `thei ~ theih` and `piang ~ pian` remain provisional in the print layer even though they clearly belong in the lexical inventory. `theihna`, `pianna`, purpose constructions, and other dependent material are genuine evidence for the alternation, but they are not the same thing as a neat paired finite paradigm. Negative clauses are relevant here, but they are not a simple diagnostic: the corpus still shows many negatives with Form I, so the grammar should not flatten the system into "Form II = negative."

# Difficult and excluded cases

Several rows remain discussable only because the inventory is broader than the quotation layer. `ngai ~ ngaih` still belongs in the dossier and in the lexical inventory, but the `ngaihsun/ngaihsut/ngaihsutna` family keeps it out of straightforward pedagogical prose. `honkhia ~ honkhiat` and `hu ~ huh` remain excluded from simple stem-alternation treatment because the current evidence behaves as lexicalized, compound-like, or category-mixed material rather than as clean stem alternation. Questionnaire/report noise also has to stay visible: `piangsak`, `neihsak`, `luimu`, `mualtung`, and similar strings belong in the audit discussion precisely because they show where automatic discovery still overreaches.

The wider analyzer inventory raises a second kind of difficulty. Pairs such as `mu ~ muk`, `ne ~ neh`, `pua ~ puak` / `pua ~ puah`, and `tua ~ tuak` / `tua ~ tuah` share a Form I base but not a single clean interpretation. The grammar should therefore inventory them, not suppress them, while making it explicit that some members of that larger field still need philological review before they can support printed examples.

# Editorial summary

The result is a more usable print-facing model. Tedim verb-stem alternation is lexically widespread. The Bible corpus gives clean paradigm evidence for some verbs, partial or constructionally restricted evidence for many others, and one-sided or same-form questionnaire evidence for still others. That is enough for a larger lexical inventory, even when the exact print-safe quotation layer remains narrow.

The larger lexical inventory is stronger than the older automatic report layer because it does not collapse lexical-pair status, Bible attestation, and print-example safety into a single confidence word. The matrix remains a review aid, not itself a set of print-safe quotations; the accepted candidate rows remain the strongest anchors for actual printed examples; and the grammar can now say more than "only the cleanest three pairs matter." It can also say which additional verbs are real, which are one-sided in the Bible, which are best discussed under nominalization or dependent structure, and which still belong under lexicalized or excluded cases.
