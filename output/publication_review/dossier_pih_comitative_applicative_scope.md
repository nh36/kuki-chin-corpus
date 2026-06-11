---
title: "Scope Dossier: Verbal -pih Comitative Applicative / Comitative Suffix"
---

# Scope Dossier: Verbal `-pih` Comitative Applicative / Comitative Suffix

## Controlling sources

- `docs/grammar/morphemes/06-derivational.md` — primary morpheme-database source for `-pih`, including Otsuka (2011), ZNC (2017/2018), and Henderson (1965) extractions
- `docs/grammar/reports/05-verb-08-derivational.md` — derivational report with `-pih` evidence
- `docs/grammar/reports/05-verb-09-valency.md` — valency report cross-referencing comitative applicative evidence
- `docs/grammar/lit-reviews/05-verb-09-valency-lit.md` — Otsuka (2011) applicative paper treatment
- `docs/grammar/ANALYZER_LITERATURE_GAPS.md` — `-pih` Form II constraint flagged as partly unresolved in analyzer layer
- `output/publication_review/grammar_derivation_valency_print_slice.md` — current boundary treatment of `paipih` within derivation/valency

## What the sources establish

### Verbal -pih as comitative applicative

Otsuka (2011) identifies verbal `-pih` as one of three productive applicative markers in Tedim, alongside `-sak` (benefactive) and `-san` (relinquitive). The core claim is:

> "When the comitative suffix -piʔ³ is attached to Form II intransitive or transitive verbs, the verb valence increases. The newly introduced core argument (i.e., direct object) in the applicative construction represents either a comitative participant or a comitative object." (Otsuka 2011: 56)

ZNC (2017/2018 §5.8.2.7 and §6.6.1.2.2) independently documents verbal `-pih` as a comitative suffix requiring Stem 2, with clear grammaticality pairs:

- ✓ `tut-pih` (sit.II-COM) "sit together"
- ✗ `*tu-pih` (sit.I-COM) [ungrammatical]
- ✓ `nuih-pih` (laugh.II-COM) "laugh together"
- ✗ `*nui-pih` (laugh.I-COM) [ungrammatical]

### Nominal -pih as boundary

Henderson (1965) documents `-pih` only as a nominal member/group suffix (e.g., `a inkuan-pih te` "his family members", `ka kho-pih` "my village-mate"). She does not discuss verbal applicative `-pih`. This nominal sense must remain boundary material and must not be conflated with the verbal comitative applicative sense.

### Co-occurrence restrictions

Otsuka (2011: 56) explicitly states that neither the benefactive `-sak` nor the causative `-sak` co-occur with comitative `-pih`. However, `-pih` can co-occur with relinquitive `-san` (e.g., `pai-pih-san`). Co-occurrence with directionals (e.g., `pai-pih-suk` "walk down with", `pai-khiat-pih` "bring out with") is documented in ZNC but creates VP-stacking contexts that should remain boundary material in this first packet.

## Corpus evidence summary

The corpus (Bible text) contains extensive verbal `-pih` evidence. The dominant forms are:

| Form | Approx. count | Analysis |
|------|--------------|---------|
| `paipih` | ~600 | go.II-COM.APPL — comitative motion (most frequent) |
| `paikhiatpih` | ~185 | go.II-AWAY-COM.APPL — directional stack (boundary) |
| `hopih` | ~161 | meet/greet.II-COM.APPL — comitative encounter |
| `hehpih` | ~144 | favor/grace.II-COM.APPL — benefactive-adjacent (cautious) |
| `ompih` | ~110 | dwell/stay.II-COM.APPL — comitative residence |
| `mipihte` | ~112 | group-member-PL — NOMINAL (boundary) |
| `innkuanpihte` | ~46 | household-member-PL — NOMINAL (boundary) |
| `ciahpih` | ~68 | return.II-COM.APPL — comitative motion return |
| `tunpih` | ~63 | arrive.II-COM.APPL — comitative motion arrival |
| `tenpih` | ~62 | go.toward.II-COM.APPL — comitative motion approach |
| `nekpih` | ~6 | eat.II-COM.APPL — comitative eating (transitive) |
| `tutpih` | ~3 | sit.II-COM.APPL — comitative sitting (low frequency in corpus) |

The Form II requirement documented in Otsuka and ZNC is consistent with the corpus: all identified verbal `-pih` forms have Stem 2 bases.

## Candidate categories

### Promoted core candidates

These are accepted as print-ready for formal interlinear examples in the grammar slice:

- `pih-core-paipih-gen2` (Genesis 2:22) — `paipih` intransitive motion + COM.APPL, clear accompanying participant
- `pih-core-paipih-matt4` (Matthew 4:1) — `paipih` Gospel counterpart, Spirit leads Jesus

### Transitive verb candidates (print-ready)

- `pih-trans-nekpih-prov7` (Proverbs 7:15) — `nekpih` eat.II-COM.APPL, OT purpose context
- `pih-trans-nekpih-luke11` (Luke 11:37) — `nekpih` eat.II-COM.APPL, Gospel invitation context

### Motion/comitative object candidates (print-ready)

- `pih-motion-tunpih-gen8` (Genesis 8:11) — `tunpih` arrive.II-COM.APPL, comitative object (olive leaf)
- `pih-motion-tunpih-matt9` (Matthew 9:2) — `tunpih` arrive.II-COM.APPL, comitative participant (paralytic)

### Nominal -pih boundary rows

These are deferred/boundary-only and must not be promoted as verbal applicative evidence:

- `pih-nominal-innkuanpih-gen7` (Genesis 7:1) — `innkuanpih` household-member (NOMINAL)
- `pih-nominal-mipihte-gen9` (Genesis 9:5) — `mipihte` group-member-PL (NOMINAL)

### Directional/VP stacking boundary rows

- `pih-boundary-paikhiatpih-gen19` (Genesis 19:5) — `paikhiatpih` go.II-AWAY-COM.APPL (directional stack)

### Blocked rows

- `pih-blocked-report-zncexample` — ZNC elicited grammaticality data; not promotable as corpus evidence but motivates the Form II restriction claim from literature

## Scope boundaries: what this packet does not claim

This packet does not claim:
- A complete comitative system including `-khawm` and case-marked comitative strategies
- Resolution of the verbal/nominal homophony as a synchronic or diachronic question
- A full applicative analysis beyond the comitative type
- The status of high-frequency forms such as `hopih`, `hehpih`, `ompih` as applicatives (these are cautious/boundary pending deeper analysis)
- VP-stacking or directional interaction beyond boundary framing
- Co-occurrence patterns between `-pih` and `-sak`, `-san`, or TAM suffixes

## Next steps (for human review and subsequent packets)

- A human reviewer should check whether the Form II restriction claim from Otsuka and ZNC is consistently reflected in the promoted examples and whether any counter-example exists in the corpus.
- The high-frequency forms `hopih` and `ompih` may warrant their own candidate investigation in a later tranche.
- The possible benefactive reading of `-pih` (noted by Otsuka for the `nek-pih` example: "ate food (and gave some) to Aunt Hau") is not promoted in this first packet and should remain an open question.
