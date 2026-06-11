---
title: "Report-to-Grammar Coverage Reconciliation"
---

# 1. Current coverage status

The current grammar-facing preview is now strong across many packetized domains, but it is still **not yet a complete Tedim grammar** at a uniform maturity level.

This reconciliation is architecture-focused (coverage and next-target decisions), not a prose-polish pass and not a new packet launch.

Controlling sources used in this reconciliation:

- `docs/SKELETON_GRAMMAR.md`
- `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`
- `docs/grammar/grammar_source_map.json`
- `docs/grammar/README_ANALYZER_GAPS.md`
- `docs/grammar/ANALYZER_LITERATURE_GAPS.md`
- `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md`
- `docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md`
- `docs/grammar/reports/` (all current report files)
- `docs/grammar/lit-reviews/` (all current literature-review files)
- `docs/grammar/morphemes/` (all current morpheme files)
- `output/grammar/grammar_full.md`
- `output/publication_review/assembled_grammar_review_preview.md`
- current publication-review packet surfaces (`grammar_*_print_slice.md`, `candidates_*.tsv`, `dossier*.md`, `review_notes_*.md`)

High-level status split:

- **Properly lifted into grammar-facing treatment**: demonstratives/deixis, negation, interrogatives, sentence-final particles, numerals, quantifiers, coordinators, case marking, NP structure, noun domain, relators/postpositions, reduplication.
- **Lifted but still narrow slices**: pronouns/clusivity, prefix/agreement, stem alternation, transitivity, TAM/aspect/modal, directionals, VP structure/stacking, derivation/valency (`-sak`-led), reflexive/reciprocal/middle-like `ki-` (first slice), verbal `-pih` comitative applicative (active first slice), nominalization, clause linkage.
- **Mainly boundary material**: object-prefix/inverse-like `hong-`/`kong-`, switch reference, relative clauses, broad possession architecture.
- **Report-backed but not packetized**: verb paradigms; phonology/tone remains chapter-scale and still outside packetization.
- **Cross-cutting analyzer-gap topics**: tone in `-a`, conditioned variants (`-pah`/`-pak`/`-lawh`), `hong-` constraints, `-sak` split, `-pih` constraints, `-thei/-theih`, habituals.

# 2. Source-to-preview matrix

| Domain | Source files / source category | Evidence layers present (R/L/M/A) | Current publication-review packet | Appears in assembled preview? | Coverage type | Main remaining gap | Recommended next action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| phonology and tone | `SKELETON_GRAMMAR.md`; `GRAMMAR_SOURCE_INVENTORY.md`; `lit-reviews/02-phon-*`; analyzer-gap docs | R: no, L: yes, M: no, A: yes | none | yes (gap placeholder section) | blocked | no packet; tone-sensitive distinctions blocked in corpus layer | keep explicit as blocked chapter-scale gap |
| simple nouns | `reports/03-noun-01-simple.md`; noun-domain packet files | R: yes, L: partial, M: no, A: no | noun-domain packet | yes (`Noun domain`) | core section | broader noun architecture still incomplete | hold stable unless human review finds defects |
| compound nouns | `reports/03-noun-02-compounds.md`; noun-domain dossier/slice | R: yes, L: partial, M: no, A: no | noun-domain packet | yes (boundary prose inside noun domain) | boundary-only | transparent vs opaque routing still incomplete | keep boundary-controlled inside noun-domain scope |
| proper nouns | `reports/03-noun-03-proper.md`; noun-domain dossier/slice | R: yes, L: partial, M: no, A: no | noun-domain packet | yes (boundary prose inside noun domain) | boundary-only | no stabilized proper-name subsystem | keep as boundary material |
| noun domain generally | `reports/03-noun-01..03`; noun-domain packet | R: yes, L: partial, M: no, A: no | noun-domain packet | yes | core section | compounds/proper/nominalized noun boundaries remain | hold stable for now |
| NP structure | `reports/03-noun-06-np-structure.md`; `reports/04-np-07-possession.md`; NP packet | R: yes, L: yes, M: no, A: no | NP structure / possession packet | yes | core section | interface with possession still uneven | hold stable for now |
| possession | `reports/04-np-07-possession.md`; `lit-reviews/04-np-07-possession-lit.md`; NP packet | R: yes, L: yes, M: partial, A: no | NP structure / possession packet | yes | narrow slice | full possession paradigm and marking analysis remain open | keep cautious possession scope; no broad expansion yet |
| case marking | `morphemes/02-case-markers.md`; `reports/03-noun-05-postpositions.md`; case packet | R: yes, L: yes, M: yes, A: yes | case-marking packet | yes | core section | tone in `-a` remains unresolved | hold stable; keep analyzer caution explicit |
| relators / postpositions | `reports/03-noun-04-relators.md`; `reports/03-noun-05-postpositions.md`; relator packet | R: yes, L: yes, M: partial, A: no | relators/postpositions packet | yes | core section | overlap with case and possession still bounded | hold stable for now |
| demonstratives / deixis | `reports/06-func-02-demonstratives.md`; `lit-reviews/06-func-02-demonstratives-lit.md`; demonstratives packet | R: yes, L: yes, M: no, A: no | demonstratives packet | yes | core section | discourse/deixis extension stays bounded | hold stable |
| pronouns / clusivity | `reports/06-func-01-pronouns.md`; pronoun packet | R: yes, L: yes, M: partial, A: no | pronouns packet | yes | narrow slice | clusivity and prefix interfaces still partially unresolved | hold stable; avoid broad rewrite |
| pronominal prefixes / agreement | `reports/05-verb-03-agreement.md`; `morphemes/01-prefixes.md`; prefix packet | R: yes, L: yes, M: yes, A: yes | prefix/agreement packet | yes | narrow slice | full paradigm and object/inverse selection not yet synthesized | hold stable; keep boundary cautions |
| object-prefix or inverse-like `hong-` / `kong-` | `reports/05-verb-03-agreement.md`; `morphemes/01-prefixes.md`; analyzer-gap docs | R: yes, L: partial, M: yes, A: yes | present as boundary rows in prefix/agreement packet | yes | boundary-only | selection constraints and interaction with valency remain unresolved | keep boundary-only until dedicated synthesis |
| reflexive / reciprocal / middle-like `ki-` | `reports/05-verb-09-valency.md`; `reports/06-func-01-pronouns.md`; `lit-reviews/05-verb-09-valency-lit.md`; `morphemes/01-prefixes.md` | R: yes, L: yes, M: yes, A: no | dedicated `ki-` reflexive/reciprocal/middle packet | yes | narrow slice | first slice is intentionally narrow and still boundary-heavy around lexicalized and passive-like rows | hold stable at first-slice maturity; deepen only if review/testing exposes defects |
| verb paradigms | `reports/05-verb-00-paradigm-tables.md`; skeleton verb chapter | R: yes, L: partial, M: no, A: no | none | yes (`Verb paradigms` placeholder) | unpacketized | report-backed but not lifted into packet workflow | schedule as major packet after next manageable packet |
| stem alternation | `reports/05-verb-01-stems.md`; `reports/05-verb-11-vsa-questionnaire.md`; stem packet | R: yes, L: yes, M: no, A: no | stem-alternation packet | yes | narrow slice | difficult/one-sided pairs remain explicitly controlled | hold stable |
| transitivity | `reports/05-verb-12-transitivity.md`; transitivity packet | R: yes, L: partial, M: no, A: no | transitivity packet | yes | narrow slice | lexical vs derivational and prefix-heavy overlap remains open | hold stable |
| TAM / aspect / modal | `reports/05-verb-04/05/07`; `morphemes/03-aspect.md`; `morphemes/05-modal.md`; TAM packet | R: yes, L: yes, M: yes, A: yes | TAM packet | yes | narrow slice | full system and stacking interactions remain open | hold stable |
| directionals | `reports/05-verb-06-directional.md`; `lit-reviews/05-verb-06-directional-lit.md`; `morphemes/04-directional.md`; directional packet | R: yes, L: yes, M: yes, A: yes | directionals packet | yes | narrow slice | broader directional classifications and VP interaction remain open | hold stable |
| VP structure | `reports/05-verb-02-vp-structure.md`; VP packet | R: yes, L: partial, M: no, A: no | VP structure / stacking packet | yes | narrow slice | no full slot architecture synthesis yet | hold stable |
| suffix combinations / stacking | `reports/05-verb-10-combinations.md`; VP packet | R: yes, L: partial, M: no, A: no | VP structure / stacking packet | yes | narrow slice | cross-domain stacking remains partly unresolved | keep narrow scope |
| derivation / valency | `reports/05-verb-08-derivational.md`; `reports/05-verb-09-valency.md`; `lit-reviews/05-verb-09-valency-lit.md`; derivation packet | R: yes, L: yes, M: yes, A: yes | derivation/valency packet | yes | narrow slice | still centered on `-sak`; broader system deferred | hold stable |
| `-sak` | derivation/valency reports + lit + morpheme db + analyzer-gap docs | R: yes, L: yes, M: yes, A: yes | derivation/valency packet | yes | core section | CAUS/BENF split still not globally reconciled with analyzer docs | keep current controlled anchors; avoid broadening |
| `-pih` | derivation/valency reports + lit + morpheme db + analyzer-gap docs | R: yes, L: yes, M: yes, A: yes | dedicated `-pih` comitative applicative packet (active) | yes | narrow slice | verbal-vs-nominal homophony and VP/directional stacking boundaries remain unresolved | keep the packet narrow while stabilizing first-slice verbal evidence |
| nominalization | `reports/07-nmlz-01-deverbal.md`; nominalization packet | R: yes, L: partial, M: yes, A: no | nominalization packet | yes | narrow slice | agentive and clause-boundary interactions remain open | hold stable |
| reduplication | `reports/07-deriv-02-reduplication.md`; reduplication packet | R: yes, L: partial, M: no, A: no | reduplication packet | yes | core section | broader expressive/lexicalized domain deferred | hold stable |
| interrogatives | `reports/09-sent-01-interrogatives.md`; `lit-reviews/09-sent-01-interrogatives-lit.md`; interrogatives packet | R: yes, L: yes, M: no, A: no | interrogatives packet | yes | core section | broader discourse/question architecture deferred | hold stable |
| negation | `reports/06-func-04-negation.md`; `lit-reviews/06-func-04-negation-lit.md`; negation packet | R: yes, L: yes, M: no, A: no | negation packet | yes | core section | cross-domain interfaces remain bounded | hold stable |
| quantifiers | `reports/06-func-05-quantifiers.md`; quantifier packet | R: yes, L: partial, M: no, A: no | quantifiers packet | yes | core section | quantifier/negation/numeral interfaces remain bounded | hold stable |
| numerals | `reports/06-func-03-numerals.md`; `lit-reviews/06-func-03-numerals-lit.md`; numeral packet | R: yes, L: yes, M: no, A: no | numerals packet | yes | core section | classifier/indefinite boundary remains open | hold stable |
| coordinators | `reports/06-func-06-coordinators.md`; coordinators packet | R: yes, L: partial, M: no, A: no | coordinators packet | yes | core section | clause-linkage overlap remains bounded | hold stable |
| sentence-final particles | `reports/10-disc-01-sentence-final.md`; `lit-reviews/10-disc-01-sentence-final-lit.md`; SFP packet | R: yes, L: yes, M: no, A: no | sentence-final particles packet | yes | core section | broader discourse still outside this slice | hold stable |
| subordination | `reports/08-clause-01-subordination.md`; `lit-reviews/08-clause-03-subordination-lit.md`; clause-linkage packet | R: yes, L: yes, M: no, A: no | clause-linkage packet | yes | narrow slice | currently centered on safest temporal anchors | hold stable |
| switch reference | `reports/08-clause-02-switch-reference.md`; subordination lit review | R: yes, L: yes, M: no, A: no | only boundary rows in clause-linkage packet | yes | boundary-only | still theory-heavy and not fully synthesized | keep boundary-only |
| relative clauses | `reports/08-clause-03-relatives.md`; subordination lit review | R: yes, L: yes, M: no, A: no | only boundary rows in clause-linkage packet | yes | boundary-only | unresolved interface with prefix/agreement + nominalization | keep boundary-only |
| broader discourse beyond sentence-final particles | discourse report/lit + skeleton discourse architecture | R: yes, L: yes, M: no, A: no | none (beyond current SFP packet) | yes (`Broader discourse` placeholder) | deferred | no dedicated discourse packet yet | keep deferred but visible |
| analyzer-gap caution (cross-cutting roll-up) | all analyzer-gap docs + inventory audit rows | R: n/a, L: n/a, M: n/a, A: yes | none | yes (`Analyzer-gap caution`) | mentioned only | unresolved items are listed but not synthesized in grammar-facing packets | keep as cross-cutting blocker layer |
| tone in `-a` case marker | analyzer-gap docs; case-marker literature | R: partial, L: yes, M: yes, A: yes | none | no (only indirect caution) | blocked | corpus layer lacks tone preservation | leave blocked until tone-restored corpus path exists |
| conditioned variants (`-pah` / `-pak` / `-lawh`) | analyzer-gap docs; modal morpheme notes | R: partial, L: partial, M: yes, A: yes | none | no | blocked | conditioning still unresolved in sources | keep blocked/open as research issue |
| `hong-` inverse constraints (analyzer topic) | agreement report; prefix morpheme db; analyzer-gap docs | R: yes, L: partial, M: yes, A: yes | prefix/agreement packet (boundary rows) | yes | boundary-only | constraints not yet captured as stable grammar-facing rules | keep boundary-only until dedicated synthesis |
| `-sak` CAUS/BENF split (analyzer topic) | derivation/valency reports; lit review; analyzer-gap docs | R: yes, L: yes, M: yes, A: yes | derivation/valency packet | yes | narrow slice | split is only partly reconciled across layers | keep controlled `-sak` slice; avoid overgeneralization |
| `-pih` Form II constraints (analyzer topic) | derivation/valency reports; lit review; morpheme db; analyzer-gap docs | R: yes, L: yes, M: yes, A: yes | derivation/valency packet (boundary only) | yes | boundary-only | still not lifted into core packet claim | keep boundary-only |
| `-thei/-theih` allomorphy (analyzer topic) | TAM reports; modal morpheme db; analyzer-gap docs | R: yes, L: partial, M: yes, A: yes | TAM packet | yes | narrow slice | form-conditioned allomorphy remains under-specified in review prose | keep narrow and controlled |
| habituals (`ngei` / `gige` / `zel`) (analyzer topic) | aspect/TAM reports; aspect morpheme db; analyzer-gap docs | R: yes, L: yes, M: yes, A: yes | TAM packet | yes | narrow slice | four-way habitual/exponential distinctions still not fully harmonized | keep narrow and controlled |

# 3. Coverage classes

## A. Already lifted enough for now

Hold stable unless human review finds defects:

- demonstratives / deixis
- negation
- interrogatives
- sentence-final particles
- numerals
- quantifiers
- coordinators
- case marking
- NP structure
- noun domain (as currently scoped)
- relators / postpositions
- reduplication

## B. Lifted as narrow slices but acceptable for current preview

- pronouns / clusivity
- pronominal prefixes / agreement
- stem alternation
- transitivity
- TAM / aspect / modal
- directionals
- VP structure
- suffix combinations / stacking
- derivation / valency (`-sak`-led)
- reflexive / reciprocal / middle-like `ki-` (first slice)
- verbal `-pih` comitative applicative (first slice)
- nominalization
- subordination (inside clause linkage)

## C. Boundary-only domains still needing synthesis for a fuller grammar

- object-prefix or inverse-like `hong-` / `kong-`
- switch reference
- relative clauses
- broader possession architecture
- full VP slot architecture beyond current narrow stacks

## D. Report-backed but not yet packetized domains

- phonology and tone
- verb paradigms

## E. Cross-cutting blockers / analyzer-gap topics

- tone in `-a` case marker (blocked)
- conditioned variants (`-pah` / `-pak` / `-lawh`) (open/blocked)
- `hong-` constraints (partly reconciled)
- `-sak` split (partly reconciled)
- `-pih` constraints (partly reconciled)
- `-thei/-theih` allomorphy (partly reconciled)
- habituals (`ngei` / `gige` / `zel`) (partly reconciled)

# 4. Recommendation for the next substantive packet

**Synchronization update:** the recommended `ki-` target has now been actioned as a first grammar-facing slice and should be held stable at first-slice maturity.

**Current active substantive target: verbal `-pih` comitative applicative / comitative suffix.**

Why this is the best active target from the same source architecture:

1. **Completeness value:** `-pih` is repeatedly visible in derivation/valency, VP, and analyzer-gap boundaries, but has lacked a dedicated packetized treatment.
2. **Evidence readiness:** it is report-backed, lit-backed, and morpheme-backed (`05-verb-08-derivational`, `05-verb-09-valency`, `05-verb-09-valency-lit`, `morphemes/06-derivational.md`).
3. **Candidate-first fit:** a narrow verbal-comitative slice is manageable without opening a full applicative/valency/VP chapter.
4. **Boundary value:** it directly resolves a recurring ambiguity with nominal `-pih` and keeps directional/stacking overlaps explicit.

Why not the other major gaps immediately:

- **Phonology/tone** remains high-priority but blocked by unresolved tone-sensitive corpus constraints.
- **Verb paradigms** remain report-backed but chapter-scale and too large for the next ordinary narrow packet.

# 5. Implementation sketch for the active `-pih` target

Likely controlling evidence:

- `docs/grammar/morphemes/06-derivational.md`
- `docs/grammar/reports/05-verb-08-derivational.md`
- `docs/grammar/reports/05-verb-09-valency.md`
- `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`
- `docs/grammar/ANALYZER_LITERATURE_GAPS.md`
- `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md`

Likely boundary surfaces to keep visible:

- `output/publication_review/grammar_derivation_valency_print_slice.md` (`-pih` currently boundary-only there)
- `output/publication_review/grammar_vp_structure_stacking_print_slice.md` (directional and suffix-stack overlap)
- `output/publication_review/grammar_directionals_print_slice.md` (`-pih` with directional material)

Proposed packet surfaces (now active):

- `output/publication_review/candidates_pih_comitative_applicative.tsv`
- `output/publication_review/dossier_pih_comitative_applicative_scope.md`
- `output/publication_review/grammar_pih_comitative_applicative_print_slice.md`
- `output/publication_review/review_notes_pih_comitative_applicative.md`

Likely anchors and controlled boundaries:

- Core verbal anchors: `paipih`, `nekpih`, `tunpih`
- Nominal boundary anchors: `innkuanpihte`, `mipihte`
- VP/directional boundary anchors: `paikhiatpih`, `pai-pih-suk`-type stacking
- Keep `-khawm`, full applicatives, and full VP template analysis out of first-slice scope
