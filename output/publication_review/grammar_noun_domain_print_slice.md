---
title: "Tedim noun domain"
bibliography: "../../docs/grammar/references.bib"
csl: "../../docs/grammar/linguistics.csl"
nocite: |
  @henderson1965
  @zamngaihcing2017
---

# Scope

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

# Overview of the noun domain

The clearest current evidence supports a modest but coherent noun-domain description. Simple lexical nouns such as `gam` and `aksi` are safely attested, and plural marking with `-te` is printable for controlled anchors such as `aksi-te` and `mite`. Human noun `mi` is also a stable lexical head in larger noun phrases, as seen in rows such as `mi khat`, `mi khempeuh`, `mi pawlkhat`, and `mi tampi`, while nonhuman nouns such as `ni` and `kum` behave similarly in counted phrases.

This is enough to describe a small publication-facing noun inventory, to note a cautious `-te` plural pattern, and to show that lexical nouns remain visible as heads inside demonstrative, numeral, and quantifier phrases. It is not yet enough for a full noun-domain chapter, because compounds, proper names, classifier-like nouns, and nominalized nouns still require more boundary control.

Gospel searches produced usable noun-domain evidence for `aksi`, `mi khempeuh`, `ni li`, and proper-name material such as `Abraham' suan David`, which helps keep the section from becoming Genesis-only. The cleanest `gam` and `-te` plural anchors, however, remain OT-led in the current pass.

# Current noun-domain inventory

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

# Simple noun stems

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

# Plural marking with -te

Plural marking with `-te` is now safe to discuss in a limited way. The clearest noun-domain anchors are nonhuman `aksi-te` and human `mi-te` in the fused form `mite`. Taken together, they support a modest claim that `-te` marks plurality on nouns in publication-facing examples.

The present section does not claim that every plural or collective pattern has been normalized. Broader questions about distributive readings, plurality outside simple noun stems, and the interaction of plural marking with quantification are still deferred.

(@ex:noun-aksi-te) Genesis 1:16
a. Tedim: aksi-te
b. Segmentation: aksi | -te
c. Gloss: star | PL
d. Translation: stars

# Human nouns and common nouns

Human noun `mi` is now one of the clearest lexical noun anchors in the nominal domain. It appears as a simple noun stem and as the head of several already-normalized noun phrases, including `mi khat`, `mi khempeuh`, `mi pawlkhat`, and `mi tampi`. Its plural form `mite` is equally secure in the current packet.

This matters for the noun domain because it shows that the normalized NP, numeral, and quantifier sections are reusing genuine noun heads rather than unanalyzed filler forms. The NP structure section remains the right place for broader ordering claims, but the noun domain can now safely say that `mi` and `mite` are stable human common nouns.

(@ex:noun-hih-mite) Exodus 5:5
a. Tedim: hih mite
b. Segmentation: hih | mi | -te
c. Gloss: PROX | person | PL
d. Translation: these people

# Nouns in larger phrases

The normalized numerals, quantifiers, and NP structure / possession sections already show that nouns remain visible as heads in larger phrases. In the current noun-domain pass, that point can be stated modestly: noun heads such as `mi`, `ni`, and `kum` stay lexically identifiable inside counted and quantified expressions rather than disappearing into unanalyzed templates.

`mi khempeuh` is the clearest quantified anchor for this purpose, while `ni li` and `kum sawm le nih` show the same thing for counted phrases. The noun-domain claim is therefore limited to lexical headedness; it does not reopen the fuller NP-order or numeral/quantifier analyses.

(@ex:noun-mi-khempeuh) Luke 2:1
a. Tedim: mi khempeuh
b. Segmentation: mi | khempeuh
c. Gloss: person | all
d. Translation: all people

# Compounds and proper nouns

Compounds and proper nouns are now visible enough for a cautious note, but they remain less normalized than simple stems and plural-marked nouns. The clearest compound-like anchor is `minam`, which is still transparent enough to support a controlled print comment about noun-noun composition. Proper names such as `Abraham` are also clearly nominal, but the current packet is not yet strong enough to generalize over Bible names, place names, or analyzer-noisy multiword name strings.

The current section therefore treats compounds and proper nouns as boundary material with one safe compound example and a more modest proper-name note. `Abraham' suan David` is a useful comparandum, but it does not yet justify a full proper-name subsection or a complete account of name-internal structure.

(@ex:noun-minam-khat) Genesis 11:6
a. Tedim: minam khat
b. Segmentation: mi-nam | khat
c. Gloss: people.group | one
d. Translation: one nation

# Nominalization boundary

Derived nouns and nominalized forms remain shared with the nominalization section. Items such as `kholhna` and broader `-na` material are important for the nominal domain, but the present section does not absorb them into the lexical noun inventory. It only notes that lexical nouns, plural-marked nouns, and larger noun phrases have now been normalized far enough that nominalized nouns can be kept as an explicit boundary rather than being mixed into the basic noun list.

# Deferred and boundary material

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

# Summary

The noun domain can now support a fuller publication-facing section than the earlier narrow packet allowed. Current evidence safely identifies simple noun stems such as `gam` and `aksi`, a cautious `-te` plural pattern visible in `aksi-te` and `mite`, stable human noun heads such as `mi`, and lexical nouns that remain visible inside counted and quantified noun phrases. Compounds, proper nouns, and nominalized nouns are now better framed as explicit boundary material rather than being mixed into an under-controlled noun list [@henderson1965; @zamngaihcing2017].
