---
title: "Analyzer Quality Dossier: Pronoun and Clusivity Forms"
bibliography:
  - ../../literature/bibliography.bib
link-citations: true
reference-section-title: "References"
---

# 1. Scope

This dossier audits analyzer and export quality for Tedim pronoun-related forms, especially `ko`, after the pronoun candidate retrofit exposed a mismatch between discourse reading and exported analysis. The control in this dossier is **philological discourse evidence**: speaker, addressee, and inclusion or exclusion in actual Tedim dialogue. Henderson, Zam Ngaih Cing, the analyzer's concord tables, and the current export are all important witnesses, but none of them overrides a discourse-clear verse on its own.

The dossier does **not** reopen the whole pronoun packet, does **not** settle `ei/eite`, and does **not** change analyzer logic in this pass. Its job is diagnostic: determine where the `ko` mismatch arises and decide what should happen before more analyzer-backed retrofits continue.

# 2. Triggering problem

The immediate trigger is a mismatch across four layers:

1. `output/publication_review/candidates_pronouns.tsv` accepts Genesis 24:55 `ko tawh` as a strong exclusive first-person plural candidate because the dialogue context is clear.
2. `data/ctd_analysis/tokens.tsv` exports that same `ko` token with gloss `long`, lemma `ko`, POS `ADJ`, and lexical usage.
3. `scripts/analyze_morphemes.py` still contains a `PRONOMINAL_CONCORD` table in which `ko/kote` map to the `ka-` series as first-person plural exclusive.
4. The publication-review protocol now depends on analyzer-backed candidate extraction as a quality-control layer.

The issue therefore is **not** "the export disagrees with Henderson, so the export must be wrong." The issue is that the export disagrees with a discourse-clear philological reading and also disagrees with the analyzer's own concord expectations. The first question is whether the philological reading is secure. The second is where the analyzer/export mismatch comes from.

# 3. Philological evidence as the control

Publication-review work can accept a discourse-clear example even when the automatic export label is wrong or incomplete. That is already what happened for the accepted `ko-exclusive` row in `candidates_pronouns.tsv`, and the broader audit below shows that this was the right editorial decision.

## 3.1 `ko`: discourse-clear exclusive evidence

| Reference | Tedim span | Speaker -> addressee | Addressee included? | Philological reading | Export gloss / POS | Export agrees? |
| --- | --- | --- | --- | --- | --- | --- |
| Genesis 20:9 | `ko tungah` | Abimelech -> Abraham | no | exclusive | `long` / `ADJ` | no |
| Genesis 24:55 | `ko tawh` | Rebekah's family -> Abraham's servant | no | exclusive | `long` / `ADJ` | no |
| Genesis 26:20 | `ko a' hi` | Gerar herdsmen -> Isaac's side | no | exclusive | `long` / `ADJ` | no |
| Genesis 34:14 | `ko a dingin` | Jacob's sons -> Hamor and Shechem | no | exclusive | `long` / `ADJ` | no |
| Exodus 20:19 | `ko tungah` | the people -> Moses | no | exclusive | `long` / `ADJ` | no |

The `ko` sample is therefore not a one-off anomaly. In the audited dialogue set, `ko` behaves as a secure exclusive first-person plural form while the export repeatedly sends it to the lexical property-word analysis `long`.

## 3.2 `kote`: stable exclusive evidence

| Reference | Tedim span | Speaker -> addressee | Addressee included? | Philological reading | Export gloss / POS | Export agrees? |
| --- | --- | --- | --- | --- | --- | --- |
| Genesis 24:23 | `kote' giah nading` | Abraham's servant -> Rebekah | no | exclusive | `1PL.PRO.POSS` / `PRON` | yes |
| Genesis 26:16 | `kote' kiang panin` | Abimelech -> Isaac | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Genesis 34:9 | `Kote tawh` | Hamor -> Jacob's family | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Genesis 37:8 | `kote' tungah` | Joseph's brothers -> Joseph | no | exclusive | `1PL.PRO.POSS` / `PRON` | yes |
| Genesis 43:8 | `nang le kote` | Judah -> Israel | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Exodus 2:19 | `kote hong honkhia` | the daughters -> their father | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Exodus 5:3 | `kote hong hihkha` | Moses and Aaron -> Pharaoh | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Exodus 20:19 | `kote kiangah` | the people -> Moses | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Genesis 42:31 | `Kote thuman mi` | Joseph's brothers -> Joseph's steward / Egyptian authority | no | exclusive | `1PL.PRO` / `PRON` | yes |
| Deuteronomy 5:27 | `Kote in hong mangin` | the people -> Moses | no | exclusive | `1PL.PRO` / `PRON` | yes |

The contrast with `ko` is sharp: the longer `kote` series exports stably as pronominal and agrees with the discourse reading across the same kind of addressed-dialogue evidence.

## 3.3 `ei/eite`: mixed philological evidence

| Reference | Tedim span | Speaker -> addressee | Addressee included? | Philological reading | Export gloss / POS | Export agrees? |
| --- | --- | --- | --- | --- | --- | --- |
| Genesis 13:8 | `eite beh khat` | Abram -> Lot | yes | inclusive | `1PL.PRO` / `PRON` | non-decisive |
| Genesis 31:15 | `eite gamdangmi` | Rachel and Leah -> Jacob | no | exclusive | `1PL.PRO` / `PRON` | non-decisive |
| Genesis 31:14 | `ei' tanh ding` | Rachel and Leah -> Jacob | no | exclusive | `1PL.EXCL.POSS` / `PRON` | partial local agreement |
| Genesis 42:2 | `Eite si loin ... ei a' ding` | Jacob -> his sons | yes | inclusive-compatible | `1PL.PRO` / `PRON`; `1PL.EXCL` / `FUNC` | conflicting / non-decisive |

The philological reading here remains mixed. `eite` can be inclusive or exclusive depending on discourse context, and the shorter `ei` series also points in different directions. The export therefore cannot be used to settle the paradigm, especially where it already assigns `1PL.EXCL` labels in verses that still function as inclusive-compatible discourse contexts.

# 4. Henderson and other descriptive witnesses

Henderson's direct discussion groups `ei/eite` separately from `ko/kote` and maps them to different concord prefixes, `i-` versus `ka-` [@henderson1965, 32-33]. That is highly relevant, and it matches the analyzer's current `PRONOMINAL_CONCORD` table. But the quoted passage is still a descriptive witness, not a substitute for checking actual Tedim dialogue.

Zam Ngaih Cing's thesis confirms that Tedim has a first-person plural clusivity distinction, but the extracted table text available in the repository is internally unstable and does not by itself settle the `ei/eite` versus `ko/kote` mapping [@zamngaihcing2017, sec. 3.2.1-3.2.2].

The result is a three-layer hierarchy:

1. **Philological discourse evidence** decides whether a verse is inclusive, exclusive, ambiguous, or unsuitable.
2. **Henderson and other witnesses** help explain why the analyzer encodes the distinctions it does.
3. **Analyzer/export output** is quality-controlled against the first two layers, not treated as final authority.

# 5. Analyzer source expectations

The source audit shows that the analyzer already "knows" some of the right distinctions, but the knowledge is unevenly distributed.

| Form(s) | Concord table | Standalone pronoun tables | Other source inventory | Ambiguity handling | Source expectation |
| --- | --- | --- | --- | --- | --- |
| `ko` | `PRONOMINAL_CONCORD` maps `ko -> ka` | absent from the audited standalone pronoun entries in `FUNCTION_WORDS` and `PRONOUNS` | `PROPERTY_WORDS` includes `ko = long` | not present in `AMBIGUOUS_MORPHEMES` | should at least be treated as ambiguous between pronoun and lexical `long`, but current routing prefers the lexical entry |
| `kote` | `kote -> ka` | present in `FUNCTION_WORDS` as `1PL.PRO`; present in `PRONOUNS` as `1PL.EXCL.PRO` | present in possessive handling as `1PL.POSS` | no special ambiguity entry needed in the audited sample | expected to export as a pronoun |
| `ei/eite` | `ei/eite -> i` | `eite` is present in `FUNCTION_WORDS` and `PRONOUNS`; `ei` is not parallel there in the audited standalone tables | `ei` still surfaces in export and in pronominal-prefix classification logic | no explicit clusivity-resolution layer | expected to belong to the first-person plural series, but source encoding alone does not settle clusivity |
| `kei` | `kei -> ka` | present in `FUNCTION_WORDS`, `PRONOUNS`, and possessive handling | also present in `NEGATION` | present in `AMBIGUOUS_MORPHEMES` | expected polysemy: pronoun vs negator |
| `no/note` | `no/note -> na` | `note` is present in `FUNCTION_WORDS`, `PRONOUNS`, and possessive handling; `no` is not parallel there | lexical inventory includes `no = young`, plus other non-pronominal uses | no `no` ambiguity entry found | `note` should export as pronoun; bare `no` needs caution because lexical competitors are strong |
| `nang`, `amah`, `amaute` | mapped in `PRONOMINAL_CONCORD` | present in `FUNCTION_WORDS` and/or `PRONOUNS` | possessive and emphatic handling also present where relevant | no special issue in audited sample | expected stable pronoun export |
| `na`, `a`, `i` | `PRONOMINAL_PREFIXES` encodes `na`, `a`, `i` | `FUNCTION_WORDS` also has standalone `na`, `a`, `i` | `na` also appears as `NMLZ`; `a` also appears as short `LOC`; `a` also occurs in other prefixal roles | `na` has ambiguity handling; `a` is multifunctional in source tables | expected to export as functional person markers in pronominal environments, but `na` and `a` are intrinsically multifunctional |

Two details matter most for the present bug:

1. `ko` is present in the concord table but **absent** from the standalone pronoun tables audited here.
2. `ko` is also present as a lexical property word `long`, and unlike `kei` it is **not** sent through any dedicated ambiguity handler.

# 6. Export-layer behavior

The export pipeline makes the `ko` mismatch visible but does not appear to be the root cause.

1. `scripts/export_tedim_analysis.py` imports `analyze_sentence`, `analyze_word`, and `get_word_class` from the analyzer.
2. `analyze_corpus()` runs `analyze_sentence()` over each verse, then calls `determine_pos()`, which delegates to `get_word_class()`.
3. `get_word_class()` checks `PROPERTY_WORDS` before pronouns. If the analyzer gloss has already settled on lexical `ko = long`, the export maps it to `PROP -> ADJ`.
4. `determine_usage_type()` then treats the token as lexical unless the form is already listed in `MIXED_LEXICAL_GRAMMATICAL` or the gloss is obviously grammatical.

In the audited export tables:

- `ko` is **not** in `POLYSEMOUS_FORMS`;
- `ko` is **not** in `HIGH_FREQUENCY_SEMANTIC_MAP`;
- `ko` is **not** in `MIXED_LEXICAL_GRAMMATICAL`.

So the export does not currently know that `ko` is a form that needs pronoun-aware review. Once the analyzer hands over `long`, the export behaves consistently with that lexical analysis. The export is therefore a **secondary amplifier**, not the clearest root source of the problem.

# 7. Form-by-form audit

## 7.1 Core independent forms

| Form | Example reference | Surface span | Exported gloss | Exported lemma | Exported POS | Usage type | Function type | Philological reading | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `kei` | Genesis 24:7 | `kei` | `1SG.PRO` | `kei` | `FUNC` | grammatical | `1SG` | free 1SG pronoun | export caveat |
| `nang` | Genesis 4:11 | `nang` | `2SG.PRO` | `nang` | `PRON` | grammatical | `2SG` | free 2SG pronoun | OK |
| `amah` | Genesis 3:20 | `amah` | `3SG.PRO` | `amah` | `PRON` | grammatical | `3SG` | free 3SG pronoun | OK |
| `amaute` | Genesis 3:21 | `amaute` | `3PL.PRO` | `amaute` | `PRON` | grammatical | `3PL` | free 3PL pronoun | OK |
| `note` | Genesis 9:9 | `note` | `2PL.PRO` | `note` | `PRON` | grammatical | `2PL` | free 2PL pronoun | OK |
| `ko` | Genesis 24:55 | `ko tawh` | `long` | `ko` | `ADJ` | lexical |  | 1PL exclusive in addressed dialogue | likely analyzer/export bug |
| `kote` | Genesis 34:9 | `Kote` | `1PL.PRO` | `kote` | `PRON` | grammatical | `1PL` | 1PL exclusive in addressed dialogue | OK |
| `eite` | Genesis 13:8 / 31:15 | `eite` | `1PL.PRO` | `eite` | `PRON` | grammatical | `1PL` | mixed inclusive and exclusive contexts | unresolved / needs more review |
| `ei` | Genesis 31:14 / 42:2 | `ei` / `ei'` | `1PL.EXCL` / `1PL.EXCL.POSS` | `ei` | `FUNC` / `PRON` | grammatical | `1PL` | mixed discourse evidence | unresolved / needs more review |

## 7.2 Adjacent pronominal and bound forms

| Form | Example reference | Surface span | Exported gloss | Exported lemma | Exported POS | Usage type | Function type | Philological reading | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ka` | Genesis 1:30 | `ka` | `1SG` | `ka` | `FUNC` | grammatical | `1SG` | stable first-person marker | OK |
| `na` | Genesis 1:2 | `na` | `2SG` | `na` | `FUNC` | grammatical | `2SG` | stable second-person marker in sampled pronominal use | OK |
| `a` | Genesis 1:1 | `A` | `3SG` | `a` | `FUNC` | grammatical | `3SG` | stable third-person marker in sampled pronominal use | OK |
| `i` | Genesis 3:22 | `i` | `1PL.INCL` | `i` | `FUNC` | grammatical | `1PL` | stable first-person plural inclusive marker | OK |
| `no` | Genesis 34:9 | `no` | `young` | `no` | `N` | lexical |  | lexical "young" in the sampled row; no clean independent 2PL token surfaced in this export audit | export caveat |

This form-by-form audit reinforces the central diagnosis. Most pronoun-related forms export reasonably well. The two main trouble spots are:

- `ko`, where philology and source expectations both point to pronoun use while the export stays lexical;
- `ei/eite`, where the export looks superficially neat but the discourse evidence is still too mixed to license a paradigm decision.

# 8. Candidate-layer implications

The candidate-layer consequences are straightforward.

1. The accepted `ko-exclusive` row in `candidates_pronouns.tsv` should remain accepted. Its acceptance already rests on a discourse-clear window, not on blind trust in the export gloss.
2. The accepted `kote-exclusive` row is independently supported by both philology and stable export output.
3. `eite-inclusive-context`, `eite-exclusive-context`, `ei-inclusive-context`, and `ei-exclusive-context` should remain unresolved. Export labels alone do not settle clusivity.
4. `kei-negator` should remain excluded from pronoun evidence even though `kei` is also a pronoun elsewhere.

So the publication-review layer is currently doing the right thing: it is analyzer-backed, but not analyzer-submissive.

# 9. Recommended fixes or follow-up tests

The evidence points most strongly to an analyzer-side **lexical-priority / missing ambiguity-handling** problem for `ko`, with export classification acting downstream of that choice.

Recommended follow-up:

1. **Add explicit ambiguity handling for `ko`.** At minimum, `ko` should be treated as a form with both lexical and pronominal possibilities, not as a property word only.
2. **Align standalone-pronoun inventory with concord knowledge.** If `ko/kote` belong to the `ka-` concord series, the standalone short form should not be absent from the pronoun tables while the long form is present.
3. **Add export-side review handling for `ko` until the analyzer is fixed.** A temporary `POLYSEMOUS_FORMS` or `MIXED_LEXICAL_GRAMMATICAL` entry would at least stop the pipeline from presenting `ko` as clean lexical `ADJ` in all contexts.
4. **Add targeted regression coverage.** Genesis 24:55 and Exodus 20:19 are especially good tests because the dialogue contrast is clear and already part of the publication-review evidence base.
5. **Keep `ei/eite` warnings in place.** Even after a `ko` fix, analyzer/export labels should not be used to settle the shorter series without renewed philological review.

# 10. Decision before continuing retrofits

The publication-review pronoun packet does **not** need to be rolled back. Its hardened candidate layer was already doing the right thing: it preserved `ko/kote` as exclusive on philological grounds and kept `ei/eite` unresolved.

The diagnosis above also identified the core source of the problem correctly. The issue was **systematic**, not isolated to Genesis 24:55, and it was best described as:

- primarily an **analyzer inventory / lexical-priority problem** for standalone `ko`,
- compounded by **missing ambiguity handling**,
- and secondarily an **export classification** problem when pronominal glosses were still allowed to fall through to lexical POS routing.

# 11. Follow-up fix

The sections above document the pre-fix diagnosis. A narrow upstream fix has now been applied and the downstream export regenerated.

## 11.1 Upstream analyzer change

The fix landed in `scripts/analyze_morphemes.py` and did four things:

1. Added `ko` to `AMBIGUOUS_MORPHEMES` as a contrast between lexical `long` and pronominal `1PL.EXCL.PRO`.
2. Added `ko` to the `PRONOUNS` inventory so a pronominal `ko` gloss has an explicit home parallel to `kote`.
3. Extended sentence-level context disambiguation so `ko` is promoted to `1PL.EXCL.PRO` in the attested discourse-clear frames audited in this dossier: `ko tawh`, `ko tungah`, `ko kiangah`, `ko a' hi`, and `ko a dingin`.
4. Corrected `get_word_class()` so a pronominal gloss is classified as `PRO` before lexical property-word fallback. This matters for `ko`, and it also corrects the long-standing `kei` pronoun-vs-`FUNC` POS mismatch in the accepted pronoun row.

This is justified by philological evidence first. The fix does **not** simply force Henderson's concord table onto the export. It teaches the analyzer to recognize the pronominal reading only in the discourse environments already shown by manually checked Tedim examples to be exclusive first-person plural contexts.

## 11.2 Updated audited contexts

After regenerating `data/ctd_analysis/tokens.tsv`, the audited `ko` contexts now export as follows:

| Reference | Tedim span | Updated export gloss / POS | Export agrees now? |
| --- | --- | --- | --- |
| Genesis 20:9 | `ko tungah` | `1PL.EXCL.PRO` / `PRON` | yes |
| Genesis 24:55 | `ko tawh` | `1PL.EXCL.PRO` / `PRON` | yes |
| Genesis 26:20 | `ko a' hi` | `1PL.EXCL.PRO` / `PRON` | yes |
| Genesis 34:14 | `ko a dingin` | `1PL.EXCL.PRO` / `PRON` | yes |
| Exodus 20:19 | `ko tungah` | `1PL.EXCL.PRO` / `PRON` | yes |

So the specific publication-review problem has been repaired upstream: the audited pronominal `ko` rows no longer export as lexical `long` / `ADJ`.

## 11.3 Lexical `ko = long` remains available

The fix is disambiguation, not erasure. Bare `analyze_word("ko")` still returns lexical `long`, and the lexical long reading remains represented in the analyzer's property-word and compound inventories. The change therefore preserves a genuine lexical `ko = long` analysis while blocking that lexical reading from automatically overriding the audited pronoun environments.

## 11.4 Other pronoun behavior after the fix

- `kote` remains stable and unchanged as a pronoun in the audited exclusive contexts.
- `ei/eite` remain unresolved at the publication level. No new analyzer change was introduced to force a global clusivity decision there.
- `kei` negator behavior remains unchanged in the negation row.
- Free pronominal `kei` now exports more cleanly as `PRON` rather than being collapsed into the generic function-word POS bucket.

## 11.5 Updated decision

The `ko` analyzer issue has now been addressed upstream far enough for the publication-review workflow to trust the audited exclusive examples again. The next step can therefore return to the planned **stem alternation retrofit**, while still keeping `ei/eite` explicitly unresolved in later person-marking work.
