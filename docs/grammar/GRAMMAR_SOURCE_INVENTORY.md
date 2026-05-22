# Tedim Grammar Source Inventory

This inventory records the main Tedim grammar sources already in the repository and how they should feed the grammar, dictionary, and chrestomathy workflow.

## How to read this inventory

- **Source type** uses the repository-specific categories requested for integration work.
- **Status** is conservative: anything with open questions, old roadmap language, or unresolved routing into the current backend workflow stays below **current**.
- **Feeds into** explains whether the file is best treated as grammar prose input, corpus evidence, lexicographic support, chrestomathy support, or a routing/checklist document.

## Core overview and architecture files

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/SKELETON_GRAMMAR.md` | Whole-grammar Tedim chapter structure | draft prose | case markers, prefixes, stem alternation, derivation, TAM, negation, sentence-final particles, nominalization | needs review | Main chapter scaffold for the edited grammar; use as chapter/section anchor rather than as canonical evidence |
| `docs/grammar/grammar_source_map.json` | Integration routing across Tedim grammar topics | implementation inventory | topic-level mappings for case, prefix, TAM, derivation, discourse, subordination, dictionary/chrestomathy support | current | Machine-readable routing layer for grammar generation and integration reporting |
| `output/grammar/grammar_constructions.md` | Backend-driven construction summary | generated backend output | agreement, case, aspect, negation, modal, sentence-final, subordination summaries | partially stale | Quick generated overview; useful as a bridge to backend data but not stable enough to cite without cross-checking |
| `output/grammar/grammar_full.md` | Backend-driven full grammar draft | generated backend output | topic and construction sections from backend layer | needs review | Drafting output only; use to spot coverage gaps and formatting issues rather than as a final prose source |
| `output/grammar/draft_grammar.md` | Chaptered Tedim grammar draft | generated backend output | chapter coverage, morpheme-category summaries, provisional/stub section tracking | current | Drafting layer for the publishable grammar |
| `output/grammar_integration_report.md` | Tedim integration dashboard | generated backend output | source-map topic routing, backend examples, analyzer-gap audit | current | Working dashboard for integration and grammar-writing workflow |

## Phonology and tone

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/lit-reviews/02-phon-01-phonology-lit.md` | segment inventory, phonological background | literature review | phoneme inventory, syllable structure | current | Scholarly source layer for phonology chapter drafting |
| `docs/grammar/lit-reviews/02-phon-02-tone-lit.md` | tone and tone-conditioned alternation | literature review | tone contrasts, tone-conditioned morphology | current | Scholarly source layer for tone chapter drafting |
| `docs/grammar/README_ANALYZER_GAPS.md` | analyzer/literature mismatches affecting phonology and morphology | analyzer gap analysis | tone distinction in `-a`, unresolved conditioned variants | partially stale | Use as a caution layer when drafting phonology/tone sections from current analyzer output |

## Nominal morphology, case marking, postpositions, and relators

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/morphemes/02-case-markers.md` | case system overview | morpheme literature database | `-in`, `-ah`, `-a`, `-pan`, `-tawh` | needs review | Scholarly source layer for case sections; also flags unresolved tone/instrumental issues |
| `docs/grammar/reports/03-noun-01-simple.md` | simple nouns | corpus report | nominal stems with case behavior | current | Empirical evidence for noun morphology chapter |
| `docs/grammar/reports/03-noun-02-compounds.md` | compound nouns | corpus report | compound nominal structures | current | Grammar and dictionary support for nominal compounding |
| `docs/grammar/reports/03-noun-03-proper.md` | proper nouns | corpus report | proper-name morphology and syntax | current | Grammar and chrestomathy support for proper names |
| `docs/grammar/reports/03-noun-04-relators.md` | relator nouns | corpus report | `tung`, `sung`, `kiang`, `lak`, `nuai`, `mai` | current | Main evidence layer for relator-noun and spatial-construction sections |
| `docs/grammar/reports/03-noun-05-postpositions.md` | postpositions and case/postposition overlap | corpus report | `-tawh`, `-pan`, free postpositions | current | Main empirical evidence for postposition and oblique-marking discussion |
| `docs/grammar/reports/03-noun-06-np-structure.md` | NP structure | corpus report | noun phrase ordering, modifiers, relational nouns | current | Grammar drafting support for NP chapter |
| `docs/grammar/reports/04-np-07-possession.md` | possession | corpus report | possessive prefixes and possessed NPs | current | Grammar and dictionary support for possessive constructions |
| `docs/grammar/lit-reviews/03-noun-05-postpositions-lit.md` | case/postposition literature | literature review | ergative, locative, ablative, comitative, postpositional patterns | current | Scholarly source layer for case and postposition chapters |
| `docs/grammar/lit-reviews/04-np-07-possession-lit.md` | possession in literature | literature review | possessive marking, possessor-possessed order | current | Scholarly source layer for possession chapter |
| `output/grammar/case_marking_report.md` | backend-driven case summary | generated backend output | ergative, locative, comitative, ablative | current | Quick empirical summary for drafting and consistency checks |

## Pronouns, pronominal prefixes, inverse marking, and reflexives

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/morphemes/01-prefixes.md` | prefixal marking | morpheme literature database | `ka-`, `na-`, `a-`, `i-`, `kong-`, `hong-`, `ki-` | needs review | Scholarly source layer for agreement, possession, inverse, and reflexive sections |
| `docs/grammar/reports/05-verb-03-agreement.md` | subject/object agreement | corpus report | subject prefixes, `kong-`, `hong-`, plural `-uh` | current | Main empirical evidence for pronominal verbal marking |
| `docs/grammar/reports/06-func-01-pronouns.md` | independent and related pronouns | corpus report | pronouns, possessive forms, reflexive forms | current | Grammar and dictionary support for pronominal system |
| `docs/grammar/lit-reviews/06-func-01-pronouns-lit.md` | pronoun literature | literature review | person marking, prefix system, pronouns | current | Scholarly source layer for pronominal chapters |
| `docs/grammar/DISAMBIGUATION.md` | homophony and contextual resolution | disambiguation note | `hong`, `na`, `hi`, `in`, relational nouns | current | Use to keep grammar examples aligned with current analyzer decisions |

## Verb stem alternation, paradigms, and VP structure

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/reports/05-verb-00-paradigm-tables.md` | paradigms | corpus report | representative Tedim verb paradigms | current | Empirical evidence and grammar table source |
| `docs/grammar/reports/05-verb-01-stems.md` | stem inventory | corpus report | Stem I / Stem II patterns and lexical domains | current | Main evidence layer for stem-alternation chapter |
| `docs/grammar/reports/05-verb-02-vp-structure.md` | VP structure | corpus report | verbal slot ordering, serial-verb-like patterns | current | Grammar drafting support for VP chapter |
| `docs/grammar/reports/05-verb-11-vsa-questionnaire.md` | verb stem alternation questionnaire | corpus report | stem alternation behavior across verbs | current | Cross-check source for stem-alternation chapter |
| `docs/grammar/reports/05-verb-12-transitivity.md` | transitivity | corpus report | transitive/intransitive classes | current | Grammar and dictionary support for lexical valency |
| `docs/grammar/lit-reviews/05-verb-01-stems-lit.md` | stem alternation literature | literature review | Form I/Form II, alternation contexts | current | Scholarly source layer for stem alternation |

## TAM, aspect, directionals, and modality

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/morphemes/03-aspect.md` | aspect and habitual systems | morpheme literature database | `-ta`, `-zo`, `-kik`, `-khin`, `-lai`, `ngei`, `gige`, `zel` | needs review | Scholarly source layer for aspect and habitual sections |
| `docs/grammar/morphemes/04-directional.md` | directional morphology | morpheme literature database | `-toh`, `-suk`, `-phei`, `-khia`, `-khiat`, `hong-`, `va-`, `ma-` | needs review | Scholarly source layer for directional chapter; also flags unconfirmed items |
| `docs/grammar/morphemes/05-modal.md` | modal morphology | morpheme literature database | `-ding`, `-thei/-theih`, `-nuam`, `-nop`, `-ngei`, conditioned modal variants | needs review | Scholarly source layer for irrealis, ability, and modal sections |
| `docs/grammar/reports/05-verb-04-tam.md` | TAM inventory | corpus report | `-ding`, `-zo`, `-thei`, `-kik`, `-ta`, `-khin`, `-nawn` | current | Main empirical evidence layer for TAM chapter |
| `docs/grammar/reports/05-verb-05-aspect.md` | aspect | corpus report | perfective, completive, iterative, continuative patterns | current | Main evidence layer for aspect sections |
| `docs/grammar/reports/05-verb-06-directional.md` | directionals | corpus report | directional suffixes and motion patterns | current | Main evidence layer for directional chapter |
| `docs/grammar/reports/05-verb-07-modal.md` | modals | corpus report | irrealis, ability, desiderative, necessity-like forms | current | Main evidence layer for modal chapter |
| `docs/grammar/lit-reviews/05-verb-05-aspect-lit.md` | aspect/TAM literature | literature review | PFV, COMPL, TAM stacking, aspect distinctions | current | Scholarly source layer for TAM/aspect chapter |
| `docs/grammar/lit-reviews/05-verb-06-directional-lit.md` | directionals in literature | literature review | elevational/directional system | current | Scholarly source layer for directional chapter |

## Valency, derivation, causative/benefactive/applicative, and reduplication

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/morphemes/06-derivational.md` | derivational and valency-changing morphology | morpheme literature database | `-sak`, `-pih`, `-khawm`, `-gawp`, `-suk`, `-zaw`, `-loh` | needs review | Scholarly source layer for derivation and valency chapters |
| `docs/grammar/morphemes/07-comparative-augmentative.md` | comparative/augmentative material | draft prose | `-zaw`, `-pi`, lexicalized comparative/augmentative patterns | partially stale | Candidate prose for grammar and dictionary notes; needs routing into current chapter structure |
| `docs/grammar/reports/05-verb-08-derivational.md` | derivational suffixes | corpus report | `-sak`, `-pih`, `-suak`, `-loh`, `-gawp`, `-khawm`, `-zaw` | current | Main empirical evidence for derivational morphology |
| `docs/grammar/reports/05-verb-09-valency.md` | valency and voice | corpus report | `ki-`, `-sak`, `-pih`, argument-structure patterns | current | Main evidence layer for valency/voice chapter |
| `docs/grammar/reports/05-verb-10-combinations.md` | suffix stacking | corpus report | multi-suffix combinations across derivation/TAM/direction | current | Evidence layer for constructional interactions |
| `docs/grammar/reports/07-deriv-02-reduplication.md` | reduplication | corpus report | reduplicative patterns | current | Grammar and dictionary support for derivation chapter |
| `docs/grammar/lit-reviews/05-verb-09-valency-lit.md` | valency and derivation literature | literature review | causative vs benefactive `-sak`, applicative `-pih`, reflexive/reciprocal `ki-` | current | Scholarly source layer for valency and derivation chapters |

## Function words, demonstratives, numerals, quantifiers, and coordinators

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/reports/06-func-02-demonstratives.md` | demonstratives | corpus report | proximal/distal demonstratives | current | Grammar and chrestomathy support for deictic system |
| `docs/grammar/reports/06-func-03-numerals.md` | numerals | corpus report | numeral forms and use | current | Grammar and dictionary support for numeral system |
| `docs/grammar/reports/06-func-05-quantifiers.md` | quantifiers | corpus report | universal/existential quantifiers | current | Grammar drafting support for quantifier section |
| `docs/grammar/reports/06-func-06-coordinators.md` | coordination | corpus report | coordinators/disjunction | current | Grammar drafting support for coordination section |
| `docs/grammar/lit-reviews/06-func-02-demonstratives-lit.md` | demonstrative literature | literature review | proximal/distal system | current | Scholarly source layer for demonstrative section |
| `docs/grammar/lit-reviews/06-func-03-numerals-lit.md` | numeral literature | literature review | numeral system | current | Scholarly source layer for numeral section |

## Negation, sentence-final markers, interrogatives, and discourse particles

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/reports/06-func-04-negation.md` | negation | corpus report | `lo`, `kei`, negative patterns | current | Main empirical evidence for negation chapter |
| `docs/grammar/reports/09-sent-01-interrogatives.md` | interrogatives | corpus report | `hiam`, question constructions | current | Main evidence layer for interrogative section |
| `docs/grammar/reports/10-disc-01-sentence-final.md` | sentence-final markers and discourse | corpus report | `hi`, `hiam`, `pen`, clause-final particles | current | Main empirical evidence for sentence-final/discourse chapter |
| `docs/grammar/lit-reviews/06-func-04-negation-lit.md` | negation literature | literature review | simple negation, emphatic negation, double-negation questions | current | Scholarly source layer for negation section |
| `docs/grammar/lit-reviews/09-sent-01-interrogatives-lit.md` | interrogative literature | literature review | interrogative particles and constructions | current | Scholarly source layer for question chapter |
| `docs/grammar/lit-reviews/10-disc-01-sentence-final-lit.md` | sentence-final/discourse literature | literature review | declarative, interrogative, topic/focus markers | current | Scholarly source layer for discourse chapter |

## Nominalization, subordination, switch reference, and relative clauses

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/reports/07-nmlz-01-deverbal.md` | deverbal nominalization | corpus report | `-na`, `-pa`, `-nu` and related deverbal forms | current | Main empirical evidence for nominalization chapter |
| `docs/grammar/reports/08-clause-01-subordination.md` | subordination | corpus report | `ciangin`, `dingin`, `hangin`, `leh`, clause chaining | current | Main evidence layer for subordination chapter |
| `docs/grammar/reports/08-clause-02-switch-reference.md` | switch reference | corpus report | same/different-subject chaining patterns | current | Evidence layer for clause linkage chapter |
| `docs/grammar/reports/08-clause-03-relatives.md` | relatives | corpus report | relative-clause formation | current | Grammar drafting support for relative-clause section |
| `docs/grammar/lit-reviews/08-clause-03-subordination-lit.md` | subordination literature | literature review | subordination, clause chaining, serial-verb boundary questions | current | Scholarly source layer for complex-sentence chapter |

## Analyzer-gap and status-tracking documents

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/README_ANALYZER_GAPS.md` | high-level analyzer/literature gap audit | analyzer gap analysis | `-sak`, `hong-`, pronominal prefixes, `-suk/-phei`, `-thei/-theih`, habituals, tone in `-a` | partially stale | Keep as a caution and prioritization layer; do not treat it as solved-state documentation |
| `docs/grammar/ANALYZER_LITERATURE_GAPS.md` | full technical gap analysis | analyzer gap analysis | prefix system, cases, aspect, directionals, modals, derivation | partially stale | Technical background for unresolved issues and review notes |
| `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md` | gap examples from corpus | analyzer gap analysis | real corpus cases for `-sak`, `hong-`, directionals, prefix ambiguity, habituals | partially stale | Evidence file for unresolved or only-partly-verified issues |
| `docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md` | implementation priorities | analyzer gap analysis | ranked unresolved distinctions | partially stale | Quick status check for current integration work |
| `docs/grammar/ANALYZER_LITERATURE_GAPS_INDEX.md` | navigation to gap set | analyzer gap analysis | analyzer-gap document map | partially stale | Navigation layer only |
| `docs/grammar/ANALYZER_LITERATURE_SUMMARY.txt` | executive summary of gaps | analyzer gap analysis | high-level scope and effort estimates | partially stale | Scope note for planning, not current-state evidence |

## Disambiguation, inventories, lexical notes, and chrestomathy support

| File path | Topic(s) covered | Source type | Main morphemes/constructions covered | Current status | Feeds into |
|-----------|------------------|-------------|--------------------------------------|----------------|------------|
| `docs/grammar/MORPHEME_INVENTORY.md` | whole-analyzer inventory | implementation inventory | prefixes, suffixes, function words, verb stems, noun stems, polysemy list | current | Quick inventory layer for grammar, dictionary, and chrestomathy routing |
| `docs/grammar/RARE_WORDS.md` | rare lexical material | analyzer gap analysis | rare lexical items and verse references | needs review | Dictionary/chrestomathy support rather than direct grammar prose |
| `docs/grammar/lexical_notes.md` | lexical problem notes | draft prose | item-specific lexical observations | needs review | Dictionary and chrestomathy support |
| `docs/grammar/compound_transparency_audit.md` | compound transparency | analyzer gap analysis | transparent vs opaque compounds | current | Dictionary and chrestomathy support; helps keep grammar examples interpretable |
| `docs/grammar/opaque_lexemes.md` | opaque lexical items | draft prose | opaque compounds and lexicalized forms | current | Dictionary and chrestomathy support |

## Analyzer-gap status audit

These statuses are conservative and only count an issue as more than **open** when there is current test coverage, current analyzer behavior, or current generated evidence pointing that way.

| Major gap | Status | Evidence used for status |
|-----------|--------|--------------------------|
| `-sak` causative vs benefactive | partly addressed | `tests/test_sak_caus_benf.py` exists, but older gap docs still flag the split and generated derivational summaries still flatten much of `-sak` |
| Agreement vs possession in `ka-/na-/a-` | probably addressed, needs verification | `tests/test_prefix_agr_poss.py` exists, but legacy gap docs still describe the distinction as unfinished |
| `hong-` inverse constraints | partly addressed | current reports/disambiguation cover `hong-`, but analyzer-gap docs still mark co-occurrence constraints as unresolved |
| Missing `-suk` / `-phei` directional coverage | probably addressed, needs verification | `tests/test_directional_suffixes.py` exists, but legacy docs still treat the gap as active and not all generated summaries are reconciled |
| `-thei / -theih` abilitative allomorphy | probably addressed, needs verification | `tests/test_thei_theih_allomorphy.py` exists, but analyzer-gap docs have not been updated to a resolved state |
| Habitual / experiential markers (`ngei`, `gige`, `zel`) | probably addressed, needs verification | `tests/test_habitual_markers.py` exists, but gap docs predate that coverage |
| Applicative `-pih` argument-structure constraints | partly addressed | current reports and tests show `-pih`, but the literature-level constraint system has not been routed into backend-aware drafting |
| Tone distinction in `-a` case marker | blocked | legacy gap docs explicitly mark this as blocked because the corpus layer does not preserve tone |
| Conditioned variants `-pah / -pak / -lawh` | open | gap docs still mark full conditioning as unfinished, and no current regression target closes it |
