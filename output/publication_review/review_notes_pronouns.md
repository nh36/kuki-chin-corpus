---
title: "Review Notes: Tedim Pronouns and Pronominal Marking"
---

# What works

This slice now reads like a draft grammar chapter rather than a backend memo. The grammar prose starts from the independent pronouns, moves through clusivity, possession, emphatics, and reflexive marking, and then only at the end turns to the harder `hong-/kong-` material. That order keeps the printed chapter readable while still acknowledging the parts of the system that are not fully settled.

The dictionary slice is also in good shape as a print-facing companion. The core pronouns (`kei`, `nang`, `amah`, `note`, `amaute`) are straightforward, the possessive prefixes are explained without pretending that possession and agreement are entirely separate morphologies, and `-mah` has been normalized as an emphatic suffix rather than reproduced from noisy backend labels. `ki-` is similarly strong because the chosen example is semantically transparent and does not depend on speculative parsing.

The treatment of `hong-` and `kong-` is cautious in the right way. They are included because they clearly matter to the person-marking system, but the slice does not overclaim that the current corpus outputs already support a polished closed paradigm.

# What does not yet work

The main unresolved issue is now narrower than it was in the first draft. The clusivity dossier supports a safe partial correction: sampled dialogue contexts consistently support `ko/kote` as exclusive, so the old `kote`-inclusive report wording should not return. The harder problem is `ei/eite`, which still shows mixed Bible-corpus behavior and therefore remains under review rather than receiving a simple global inclusive label.

The boundary between possessive prefixes and verbal agreement prefixes is also only partly normalized in the project documentation. In the print slice this is manageable, because noun-attached examples are usually easy to interpret. In the wider project, however, some older analyzer-gap notes still describe the contrast as unresolved even though the current outputs are more stable than that wording suggests.

`hong-` and `kong-` are usable in a narrow editorial sense, but they are not yet safe enough for a broad paradigm table without stronger manual review. `kong-` has a clean biblical illustration, while `hong-` still requires more contextual judgment than the rest of the slice.

# Citation and source audit

The grammar slice cites only bibliography keys that already exist in `literature/bibliography.bib`: `@henderson1965`, `@zamngaihcing2017`, `@sukte_grammar`, and `@otsuka_causative`. No provisional citation keys were introduced.

Henderson is the anchor source for the independent-pronoun paradigm, the clusivity contrast, and the concord-prefix mapping. Zam Ngaih Cing provides the strongest support for the pronoun subclasses, possessive pronouns, emphatic `-mah`, and the broader presence of clusivity in Tedim. Singh is used only as a comparative check, mainly to show that Sukte does not straightforwardly reproduce the same clusivity pattern. Otsuka is used narrowly for the person-sensitive `hong-/kong-` domain, not as a general citation for the whole pronoun chapter.

# Clusivity dossier note

A separate dossier now exists at `output/publication_review/dossier_pronoun_clusivity.md`. That dossier now supports a safe partial correction: remove the old report wording that treated `kote` as inclusive, treat `ko/kote` as exclusive, and keep `ei/eite` under review rather than forcing a full global label swap.

# Candidate-layer note

Pronouns and clusivity now also have an analyzer-aware candidate file at `output/publication_review/candidates_pronouns.tsv`. That layer records stable accepted pronoun rows, unresolved `ei/eite` evidence, and at least one explicit false friend where `kei` is negative rather than pronominal.

The packet should now be read in the order `candidate file -> dossier -> grammar slice -> dictionary slice -> review notes`. That keeps the clusivity discussion anchored to explicit analyzer-backed candidate rows instead of to raw counts or report-level labels alone.

# Analyzer/export caveats in the candidate layer

The pronoun candidate file uses analyzer-export spans, but some of the exported labels remain imperfect. The clearest accepted `kei` row is glossed `1SG.PRO` and functioned as first person, yet its POS field still reads `FUNC` rather than `PRON`. In the shorter `ei` series, some rows already export as `1PL.EXCL` or `1PL.EXCL.POSS`, even though the clusivity dossier still treats `ei/eite` as mixed and unresolved at the publication level.

These caveats do not invalidate the candidate layer, but they do mean the layer is analyzer-backed rather than analyzer-infallible. Accepted status depends on the combination of confirmed token windows, manual verse review, and the constructional interpretation already established in the dossier and packet prose.

# Decision for next slice

This slice is now supported by an explicit candidate layer as well as by the clusivity dossier. The partial correction still stands: `ko/kote` should remain treated as exclusive, while `ei/eite` should remain flagged as under review rather than treated as globally solved. The next step should therefore be to review and harden the pronoun candidate layer before moving on to stem alternation or any new topic.
