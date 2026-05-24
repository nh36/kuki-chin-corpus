---
title: "Review Notes: Tedim Pronouns and Pronominal Marking"
---

# What works

This slice now reads like a draft grammar chapter rather than a backend memo. The grammar prose starts from the independent pronouns, moves through clusivity, possession, emphatics, and reflexive marking, and then only at the end turns to the harder `hong-/kong-` material. That order keeps the printed chapter readable while still acknowledging the parts of the system that are not fully settled.

The dictionary slice is also in good shape as a print-facing companion. The core pronouns (`kei`, `nang`, `amah`, `note`, `amaute`) are straightforward, the possessive prefixes are explained without pretending that possession and agreement are entirely separate morphologies, and `-mah` has been normalized as an emphatic suffix rather than reproduced from noisy backend labels. `ki-` is similarly strong because the chosen example is semantically transparent and does not depend on speculative parsing.

The treatment of `hong-` and `kong-` is cautious in the right way. They are included because they clearly matter to the person-marking system, but the slice does not overclaim that the current corpus outputs already support a polished closed paradigm.

# What does not yet work

The main unresolved issue is the inclusive/exclusive labeling conflict. The current generated pronoun report labels `kote` as inclusive and `eite` as exclusive, while Henderson's paradigm and the associated prefix evidence point the other way. The print slice handles this honestly by following the literature provisionally and naming the conflict explicitly, but the upstream report remains out of alignment.

The boundary between possessive prefixes and verbal agreement prefixes is also only partly normalized in the project documentation. In the print slice this is manageable, because noun-attached examples are usually easy to interpret. In the wider project, however, some older analyzer-gap notes still describe the contrast as unresolved even though the current outputs are more stable than that wording suggests.

`hong-` and `kong-` are usable in a narrow editorial sense, but they are not yet safe enough for a broad paradigm table without stronger manual review. `kong-` has a clean biblical illustration, while `hong-` still requires more contextual judgment than the rest of the slice.

# Citation and source audit

The grammar slice cites only bibliography keys that already exist in `literature/bibliography.bib`: `@henderson1965`, `@zamngaihcing2017`, `@sukte_grammar`, and `@otsuka_causative`. No provisional citation keys were introduced.

Henderson is the anchor source for the independent-pronoun paradigm, the clusivity contrast, and the concord-prefix mapping. Zam Ngaih Cing provides the strongest support for the pronoun subclasses, possessive pronouns, emphatic `-mah`, and the broader presence of clusivity in Tedim. Singh is used only as a comparative check, mainly to show that Sukte does not straightforwardly reproduce the same clusivity pattern. Otsuka is used narrowly for the person-sensitive `hong-/kong-` domain, not as a general citation for the whole pronoun chapter.

# Clusivity dossier note

A separate dossier now exists at `output/publication_review/dossier_pronoun_clusivity.md`. The generated pronoun report should not be corrected until that dossier conclusion has been reviewed.

# Decision for next slice

This slice is close to being reusable as the next model, but one issue should be reviewed before expanding the same workflow much further into person-marking material: the new clusivity dossier shows that the `eite/ei` versus `kote/ko` problem is not yet settled well enough for an automatic report correction. The present slice can remain provisional, but later person-marking slices should wait for an editorial decision on that dossier.
