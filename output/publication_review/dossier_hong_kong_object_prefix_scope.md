---
title: "Tedim Hong / kong Object-Prefix Scoping Dossier"
---

# Scope and status

This is the first candidate/scoping pass for the Tedim `hong` / `kong` object-prefix or inverse-like domain. The controlling candidate layer now exists at `output/publication_review/candidates_hong_kong_object_prefix.tsv`. This dossier is not a grammar print slice and not a full agreement chapter.

The packet is intentionally small. Its job is to separate the clearest participant-oriented rows from deictic/venitive motion, speech-formula rows, and lexicalized or unclear material while keeping the prefix/agreement and pronoun packets bounded.

# Evidence protocol

The main discovery and evidence sources for this packet are:

- `docs/grammar/reports/05-verb-03-agreement.md`
- `docs/grammar/morphemes/01-prefixes.md`
- `docs/grammar/reports/06-func-01-pronouns.md`
- `docs/grammar/reports/05-verb-08-derivational.md`
- `docs/grammar/reports/05-verb-09-valency.md`
- `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`
- `docs/grammar/ANALYZER_LITERATURE_GAPS.md`
- `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md`
- `docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md`

The reports and morpheme file keep the key split visible: `hong` is both venitive/deictic and inverse-like in different contexts, while `kong` is the cleaner direct-like / 1→2 side. The pronoun and valency reports keep the person-sensitive overlap visible, and the analyzer-gap docs preserve the stronger literature-backed constraints around causative rows.

# Literature statement

Henderson and the report literature treat `hong-` and `kong-` as part of a participant-oriented preverbal system, but they do not give a single uniform analysis. Henderson and the agreement report present `hong-` as inverse-like / toward-speaker material and `kong-` as the direct-like 1→2 side; the morpheme file keeps `hong-` as directional/venitive while also noting the obligatory inverse-like use with first/second-person causees.

Otsuka's discussion and the analyzer-gap documents sharpen the same point: `hong-` matters when the causee or beneficiary is first or second person, and `kong-` is the clearer 1→2 side. The important methodological point is that these claims are real but not exhaustive. They do not mean every `hong` token is object-prefixal, and they do not justify collapsing motion, speech formula, or lexicalized rows into the same analysis.

# Candidate groups

## Promoted core rows

- `hongbia` is the clearest `hong`-side diagnostic in the current packet.
- `kongpia` and `kongkoih` are the clearest `kong`-side diagnostics.

## Supporting but non-diagnostic rows

- `hongmu`, `kongmu`, and `hongzui` keep the participant-oriented domain visible but do not by themselves settle the selection rule.

## Boundary rows

- `hongpai`, `hongbei`, and `hongsawl` are deictic / venitive boundary rows.
- `hongsuahna`, `kongci`, and `konggenkik` are lexicalized or unclear rows.
- `hong-an-huan-sak` and `kong-bawl-sak` are blocked analyzer-gap rows from the literature.

# Person-configuration diagnostic summary

## Matthew 4:9 (paired Gospel diagnostic)

`Kei hong bia` versus `nangma tungah kong pia` remains the cleanest paired row.

- `hongbia` is retained as inverse-like `2→1` diagnostic evidence.
- `kongpia` is retained as direct-like `1→2` diagnostic evidence.
- Explicit independent pronouns (`kei`, `nangma`) make this pairing unusually clear.

## Genesis 41:41 (OT kong anchor)

`Nang kong koih` remains a strong direct-like `1→2` kong diagnostic and stays promoted.

## Matthew 25:37 (resolved supportive row)

The quoted clause is 1PL→2SG at the clause level (“when did we see you hungry and give you food?”), but the two `hong` tokens are not treated as clean object-prefix diagnostics here.

The row is therefore kept as supporting evidence and glossed consistently as SAP-oriented/venitive (`SAP.ORIENT`) in both the hong/kong slice and the older prefix/agreement boundary slice.

## Candidate-layer implementation

The candidate TSV now records row-level person decisions in `person_configuration_decision` so the evidence layer distinguishes:

- promoted inverse-like `hong` diagnostics;
- promoted direct-like `kong` diagnostics;
- SAP-oriented support rows;
- deictic/venitive boundary rows;
- speech-formula boundary rows;
- blocked literature/analyzer-gap rows.

# Decision

The safest grammar-facing conclusion is a narrow participant-oriented prefix pocket. `kong` is the cleaner direct-like / 1→2 side. `hong` is real but mixed: it can be inverse-like, but it also overlaps with venitive and deictic motion, so it must stay construction-controlled.

`hongmu`, `kongmu`, and `hongzui` stay useful as supporting rows, but they should not be promoted as the cleanest diagnostics. The dossier now explicitly demotes `hongsawl` to deictic/venitive boundary material and keeps speech-formula `kong` rows separate from direct-like diagnostics.

# Recommended print-facing phrasing

The slice should say that Tedim has a narrow participant-oriented prefix domain, not a full agreement chapter or a full inverse-system chapter. The clearest `hong` evidence should be treated as inverse-like but not universal, the clearest `kong` evidence should be treated as direct-like / 1→2, and deictic or lexicalized rows should remain boundary material.
