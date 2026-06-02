---
title: "Tedim case marking"
bibliography: "../../docs/grammar/references.bib"
csl: "../../docs/grammar/linguistics.csl"
nocite: |
  @henderson1965
  @zamngaihcing2017
---

# Scope

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

# Overview of case-like marking

The current evidence supports a modest but coherent picture of postnominal case-like marking in Tedim. The clearest publication-facing claims concern locative or goal-like `-ah` 'locative / goal-like' and clause-level agentive or ergative `-in` 'ergative / agentive'. The same section also supports more cautious discussion of source marking with `-pan` 'source / ablative' and `-panin` 'source / departure', plus accompaniment or material-extension uses of `-tawh` 'with', but those markers remain more boundary-heavy because they overlap with relator nouns, postpositions, or broader semantic extension.

The safest current prose therefore treats case marking as an NP-final domain rather than as a fully settled paradigm of discrete suffixes. Plain noun-plus-case rows such as `khua-ah` 'in the town' and clause-level agent rows such as `Kain in` 'Cain as agent' are secure enough to print. Relator-hosted forms such as `lakpan` 'from among' and `David khuapi sungah` 'in the city of David' are also real, but they should not be collapsed into a bare suffix inventory. Apostrophe-marked possession can host the same NP-final marking, yet the apostrophe itself remains a boundary issue rather than a settled genitive case marker in this section.

The Gospel search was productive enough to keep the section from becoming OT-only. The current manually reviewed supplement adds usable Gospel support for `Herod in` 'Herod as agent', `keima inn-ah` 'into my house', `David khuapi sungah` 'in the city of David', and `lakpan` 'from among'. The possessive-boundary example remains OT-led, because no equally compact Gospel row was as clean under the current control standard.

# Current case-marking inventory

| Marker or pattern | Rough function | Example context | Current print status | Main boundary issue |
| --- | --- | --- | --- | --- |
| `-ah` | locative or goal-like NP-final marking | `khua-ah`, `inn-ah` | print-ready | must stay distinct from deferred tone-sensitive `-a` and from relator-hosted spatial phrases |
| `-in` | clause-level ergative or agentive marking | `Kain in`, `Herod in` | print-ready | raw `-in` extraction overgenerates forms such as `ciangin` |
| possessor phrase plus `-ah` | possessed NP closed by case-like marking | `na pa' inn-ah` | print-usable with caveat | does not settle the apostrophe or genitive analysis |
| `-pan` | source marking, often on a relator host | `lakpan` | print-usable with caveat | current clean evidence is relator-hosted rather than a broad bare-suffix paradigm |
| `-panin` | source or departure marking | `inn panin` | print-usable with caveat | internal structure remains under review |
| `-tawh` | accompaniment, with material or instrumental extension | `kei tawh`, `leivui tawh` | print-usable with caveat | accompaniment should not be flattened together with material-extension use |
| relator noun plus case | spatial relational phrase closed by case-like marking | `David khuapi sungah`, `tungah`, `kiangah` | print-usable with caveat | belongs jointly with the relators / postpositions section rather than a suffix-only list |

# Locative and goal marking with -ah

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

# Agentive, ergative, or instrumental marking with -in

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

# Other controlled oblique markers

The section still retains a small set of other controlled case-like markers, but they are best treated more cautiously than `-ah` and `-in`. Source marking with `-pan` and `-panin` is real enough to describe, especially in rows such as `lakpan` 'from among' and `inn panin` 'from the house', yet the cleanest `-pan` example is relator-hosted and the internal structure of `-panin` remains under review. Likewise, `-tawh` remains part of the section because `kei tawh` 'with me' is a clean accompaniment row and `leivui tawh` 'with dust' shows a material or instrument-like extension, but that semantic split needs to stay explicit.

This means the section can already mention `-pan`, `-panin`, and `-tawh` in the current inventory, but it should not yet present them as a fully normalized oblique subsystem. For the present pass, they remain controlled supporting material rather than the center of the case-marking chapter.

(@ex:case-panin-inn) Genesis 12:1
a. Tedim: inn panin
b. Segmentation: inn | panin
c. Gloss: house | from
d. Translation: from the house

(@ex:case-tawh-kei) Genesis 14:24
a. Tedim: kei tawh
b. Segmentation: kei | tawh
c. Gloss: 1SG.PRO | COM
d. Translation: with me

(@ex:case-tawh-leivui) Genesis 2:7
a. Tedim: leivui tawh
b. Segmentation: leivui | tawh
c. Gloss: dust | COM
d. Translation: with dust

These rows keep the oblique material concrete. `Inn panin` 'from the house' shows source marking without a relator host, while `kei tawh` 'with me' and `leivui tawh` 'with dust' show that `-tawh` covers both accompaniment and material-extension uses.

No equally clean Gospel source or accompaniment row is currently used here, so the subsection stays OT-led while the broader oblique inventory remains cautiously delimited.

# Genitive / possessive boundary

The clearest way to discuss genitive or possessive boundary material at present is to show that an already possessed noun phrase can host case-like marking at its right edge. Genesis 24:23 gives the compact row `na pa' inn-ah` 'in your father's house', which is already reused in the normalized NP structure / possession section. Here it serves a narrower purpose: it shows that case-like marking closes the larger noun phrase rather than attaching only to a simple underived noun stem.

(@ex:case-poss-na-pa-inn) Genesis 24:23
a. Tedim: na pa' inn-ah
b. Segmentation: na | pa' | inn | -ah
c. Gloss: 2SG.POSS | father | house | LOC
d. Translation: in thy father's house

This is enough to justify a boundary note, but not enough to settle the apostrophe analysis. The present section therefore does not settle whether the apostrophe material should be treated as a genitive suffix, a possessive linker, or an orthographic boundary convention. It only records that possessed noun phrases can participate in the same case-closing pattern that appears elsewhere in the nominal domain. The fuller discussion of possessive structure remains with the normalized NP structure / possession section.

No equally good Gospel possessed NP with case-like closure is currently used here, so the subsection stays with the compact OT example while the wider possession discussion remains elsewhere.

# Case marking and relators/postpositions

The boundary with relators and postpositions is now one of the main editorial points of the section. Forms such as `sungah` 'inside / in', `tungah` 'on / upon', `kiangah` 'beside / near', and `lakpan` 'from among' are not noise, but neither are they simple proof that Tedim can be described by a suffix-only case list. The relational host matters: `sung` 'inside', `tung` 'on top', `kiang` 'side / vicinity', and `lak` 'among' contribute spatial content before locative or source marking is added.

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

# Case marking and argument structure

The normalized case section can now say one modest thing about argument structure: checked `-in` rows such as `Kain in` 'Cain as agent' and `Herod in` 'Herod as agent' show case-marked noun phrases functioning as clause-level agents, while locative or goal-like rows such as `inn-ah` 'in / into the house' show noun phrases entering the clause as spatial arguments or adjuncts. That is enough to connect the nominal domain to clause structure without reopening the full alignment or valency chapter.

The present section therefore cross-references the transitivity packet rather than replacing it. The transitivity section remains the place for fuller discussion of argument frames, lexical valency, and broader alignment questions. Case marking only contributes the controlled NP-final marking side of that picture here.

# Deferred and boundary material

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

# Summary

The case-marking section can now support a fuller publication-facing description than the earlier narrow packet allowed. Current evidence safely supports clause-level `-in`, locative or goal-like `-ah`, a boundary note on possessed noun phrases such as `na pa' inn-ah`, and a controlled interface with relator-hosted forms such as `David khuapi sungah` and `lakpan`. Source marking with `-pan` and `-panin`, along with `-tawh`, remains usable but secondary and caveated. The result is a real grammar section with explicit limits, not a claim that the full Tedim case system has already been finished [@henderson1965; @zamngaihcing2017].
