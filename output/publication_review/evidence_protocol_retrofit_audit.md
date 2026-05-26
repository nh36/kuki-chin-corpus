# Retrospective Evidence-Protocol Audit

## Purpose

This audit checks the existing publication-review packets against the newer analyzer-aware evidence protocol in `docs/publication_review/EVIDENCE_PROTOCOL.md`. The aim is not to reopen already stabilized analysis, but to identify which earlier packets now need explicit candidate files or other narrow retrofit work before the project starts another topic.

## Current protocol baseline

The current publication-review protocol distinguishes four evidence levels:

- **Level 0: raw hit** — a string occurs in the Bible text; this is only a discovery clue.
- **Level 1: analyzer-confirmed token** — the token or morpheme is confirmed in analyzer output with segmentation, gloss, lemma, POS, usage type, or function type.
- **Level 2: construction-confirmed example** — the surrounding context confirms the relevant grammatical construction.
- **Level 3: print-safe example** — the example has been manually checked, verse-referenced, short enough to cite, and directly supports the printed claim.

Under this standard, earlier publication-review packets are analytically usable, but not all of them are yet fully protocol-backed. The main retrofit question is where the project now needs explicit `candidates_<topic>.tsv` files.

## Packet inventory table

| Topic | Dossier | Grammar slice | Dictionary slice | Review notes | Candidate TSV | Related tests | Related generated-report correction | Known ambiguity risks | Current status | Recommended next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| case marking | no dossier located | yes | yes | yes | no | no packet-specific publication-review test located; general integration and export tests touch case markers | no explicit report-level correction located during this audit | homographic `-in`, conservative `-panin`, source vs relator-noun boundaries, raw orthographic overgeneration for `-ah`, `-a`, `-pan`, `-tawh` | editorial model, but predates candidate-first workflow | lower-priority retrofit; add a candidate file later unless a specific extraction problem becomes urgent |
| pronouns | no separate pronoun dossier; clusivity handled in a separate dossier plus an analyzer-quality dossier | yes | yes | yes | yes (`candidates_pronouns.tsv`) | `tests/test_pronoun_candidates.py`, `tests/test_pronoun_clusivity_docs.py`, `tests/test_pronoun_analyzer_quality.py`, and extractor reproducibility coverage | yes: `docs/grammar/reports/06-func-01-pronouns.md` now treats `ko/kote` as exclusive and keeps `ei/eite` under review | unresolved `ei/eite`, possessive vs agreement prefixes, `hong-/kong-`, remaining lexical/pronominal polysemy around short forms | candidate TSV hardened at the publication layer and the upstream analyzer now exports audited pronominal `ko` contexts as `1PL.EXCL.PRO` / `PRON` | keep `ei/eite` unresolved while stem alternation hardening proceeds |
| pronoun clusivity | yes (`dossier_pronoun_clusivity.md`) | no | no | no separate review note | yes, via `candidates_pronouns.tsv` | `tests/test_pronoun_candidates.py`, `tests/test_pronoun_clusivity_docs.py`, `tests/test_pronoun_analyzer_quality.py` | yes, via the partial correction in `docs/grammar/reports/06-func-01-pronouns.md` | mixed `ei/eite`, more stable `ko/kote`, dialogue-context sensitivity | support-layer dossier now paired with a hardened shared pronoun candidate TSV and a completed `ko` analyzer-quality fix | keep `ei/eite` unresolved and treat philologically checked Tedim evidence, not Henderson alone or export labels alone, as the control in later person-marking work |
| stem alternation | yes | yes | yes | yes | yes (`candidates_stem_alternation.tsv`) | `tests/test_stem_alternation_candidates.py`, `tests/test_stem_alternation_corpus_audit.py`, plus extractor reproducibility coverage | no explicit report correction located; review notes instead describe noisy report/questionnaire layers | Form I / Form II distribution, noisy questionnaire output, lexical-family contamination (`ngai/ngaih`), caveated expansions such as `za ~ zak` and `nusia ~ nusiat` | candidate TSV added; broader analyzer-based corpus audit now added so Form I / Form II distribution can be reviewed across environments before the packet is called hardened | review the new corpus audit against the packet prose, then move to case marking |
| negation | yes | yes | yes | yes | yes (`candidates_negation.tsv`) | `tests/test_negation_candidates.py` plus extractor reproducibility coverage | yes: `docs/grammar/reports/06-func-04-negation.md` was minimally corrected so Genesis 2:25 and `V lo uh` no longer mislead the packet | `kei` negator vs pronoun, `lo` vs `loh`, `V lo uh`, `kuamah`, `bangmah`, `thei lo / theih loh` | first retrofit candidate TSV added and hardened, with export caveats now documented in the audit trail | maintain the hardened negation layer while stem alternation candidate hardening becomes the next retrofit task |
| demonstratives/deixis | yes | yes | yes | yes | yes (`candidates_demonstratives.tsv`) | `tests/test_demonstratives_docs.py`, `tests/test_publication_evidence_protocol.py`, `tests/test_publication_candidate_extractor.py` | yes: `docs/grammar/reports/06-func-02-demonstratives.md` now carries explicit correction notes | `hi`, exact `hih ciangin`, `tua` / `hua`, raw-search false friends | current pilot for the protocol-backed workflow | no immediate retrofit needed beyond maintenance and future topic extension |

## Topic-by-topic audit notes

### Demonstratives/deixis

Demonstratives is already protocol-backed. It has a dossier, synchronized print packet, review notes, a candidate TSV, a protocol test, and a reproducibility test for the extractor. It should be treated as the working model for future candidate-first packet work. No immediate retrofit is needed beyond normal maintenance.

### Negation

Negation was the highest-priority retrofit, and it now has an analyzer-aware candidate file plus a hardening pass for export caveats. That retrofit was warranted because the packet has an unusually high ambiguity profile: `kei` is homographic with the first-person singular pronoun, `lo` and `loh` need constructional rather than string-based handling, `V lo uh` has already proved easy to misread, and `kuamah` / `bangmah` overgenerate under raw search. The hardened `candidates_negation.tsv` now makes the packet substantially closer to the newer protocol standard while keeping noisy export fields explicitly documented.

### Pronouns

The pronoun packet itself is usable, and it now has a hardened analyzer-aware candidate file. A separate clusivity dossier still carries the hardest interpretive work, and the generated pronoun report remains only partially corrected: `ko/kote` stays exclusive while `ei/eite` remains under review. The hardened candidate layer therefore does not reopen the whole packet; it makes the stable rows, unresolved clusivity rows, and false friends explicit, including both `ko` and `kote` as explicit exclusive evidence.

The pronoun retrofit did expose a real analyzer-quality issue, but that issue has now been addressed upstream. The accepted `ko` candidate row is philologically secure in several addressed-dialogue contexts, and the regenerated export now emits `1PL.EXCL.PRO` / `PRON` rather than lexical `long` / `ADJ` in those audited windows. The analyzer-quality dossier still matters because it records why the fix was needed and why the philological evidence, not Henderson alone, controlled the repair.

### Pronoun clusivity

Pronoun clusivity should still be treated as a support-layer retrofit rather than as its own print packet. The dossier remains valuable because it established the current partial correction, and the hardened shared pronoun candidate TSV now gives that dossier an analyzer-aware evidence layer with both `ko` and `kote` represented. Any later work should continue to preserve the mixed `ei/eite` evidence instead of forcing a premature resolution.

The analyzer-quality dossier adds one methodological clarification that remains important even after the fix. Henderson's concord table is relevant, but it is not decisive on its own. The immediate control for pronoun-quality review is the manually checked Tedim discourse evidence, especially where speaker and addressee relations make the `ko/kote` exclusive reading secure.

### Stem alternation

Stem alternation is a strong packet, and it now has both an analyzer-aware candidate file and a broader corpus audit. The candidate TSV preserves the packet's strongest core pairs and explicitly blocks report/questionnaire traps such as `piangsak`, `ngaihsutna`, and solitary `honkhiat`. The new audit layer now keeps the full row-level audit local and generated-only in `output/publication_review/stem_alternation_corpus_audit.tsv`, while tracking the reviewable compact outputs in `output/publication_review/stem_alternation_environment_summary.tsv`, `output/publication_review/stem_alternation_pair_summary.tsv`, and `output/publication_review/stem_alternation_example_matrix.tsv`. That is the right next step for a distributional topic like Form I / Form II alternation. The review notes are still right that the report layer is too uneven to auto-generate the chapter safely, so the next task is interpretive review of this broader audit rather than a rush to declare the packet hardened.

### Case marking

Case marking remains the editorial model, but it predates the candidate-first protocol and still exposes extraction risk. The review notes explicitly mention that automatic example selection is weak for ergative `-in`, and that `-panin` is being handled conservatively. A future candidate file would help with `-in`, `-ah`, `-a`, `-pan`, and `-tawh`, especially where raw orthography and homography overgenerate. Still, the current audit does not reveal a packet-level contradiction urgent enough to move case marking ahead of negation or pronouns.

## Recommended retrofit order

With negation now retrofitted, pronouns / clusivity now hardened at the publication layer and repaired upstream for `ko`, and stem alternation now given both an explicit candidate TSV and a broader corpus audit with tracked summaries and an example matrix, the remaining practical order should be:

1. **Stem alternation interpretation next** — review the new corpus audit and use it to revise or confirm the packet's claims about Form I / Form II distribution before calling the topic hardened.
2. **Case marking after stem alternation** — worthwhile, but lower urgency unless a specific extraction problem becomes pressing.
3. **Demonstratives maintenance only** — already protocol-backed.

## Conclusion

The retrofit audit now supports a more distribution-aware next step. Demonstratives remains the protocol pilot, negation is the first hardened retrofit, pronouns / clusivity is the second hardened retrofit with its `ko` analyzer issue addressed upstream, and stem alternation now has both a curated candidate TSV and a broader corpus audit whose large row-level file stays local while tracked summaries and a tracked example matrix support review. The immediate next step is to interpret that audit against the current packet before moving on to case marking.
