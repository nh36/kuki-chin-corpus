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
| case marking | yes (`dossier_case_marking.md`) | yes (`grammar_case_marking_print_slice.md`) | yes (`dictionary_case_markers_print_slice.md`) | yes (`review_notes_case_marking.md`) | yes (`candidates_case_marking.tsv`) | `tests/test_case_marking_candidates.py`, plus general integration and export tests touching case markers | no explicit report-level correction located during this audit | homographic `-in`, `-ah` / `-a` overgeneration, source `-pan` with conservative `-panin`, source vs relator-noun boundaries, `-tawh` accompaniment vs material/instrumental extension | candidate layer and dossier now in place for an older slice family; extractor route still absent | keep the packet conservative and use the dossier plus candidate TSV as the control for any later narrow clarifications |
| pronouns | no separate pronoun dossier; clusivity handled in a separate dossier plus an analyzer-quality dossier | yes | yes | yes | yes (`candidates_pronouns.tsv`) | `tests/test_pronoun_candidates.py`, `tests/test_pronoun_clusivity_docs.py`, `tests/test_pronoun_analyzer_quality.py`, and extractor reproducibility coverage | yes: `docs/grammar/reports/06-func-01-pronouns.md` now treats `ko/kote` as exclusive and keeps `ei/eite` under review | unresolved `ei/eite`, possessive vs agreement prefixes, `hong-/kong-`, remaining lexical/pronominal polysemy around short forms | candidate TSV hardened at the publication layer and the upstream analyzer now exports audited pronominal `ko` contexts as `1PL.EXCL.PRO` / `PRON` | keep `ei/eite` unresolved while stem alternation hardening proceeds |
| pronoun clusivity | yes (`dossier_pronoun_clusivity.md`) | no | no | no separate review note | yes, via `candidates_pronouns.tsv` | `tests/test_pronoun_candidates.py`, `tests/test_pronoun_clusivity_docs.py`, `tests/test_pronoun_analyzer_quality.py` | yes, via the partial correction in `docs/grammar/reports/06-func-01-pronouns.md` | mixed `ei/eite`, more stable `ko/kote`, dialogue-context sensitivity | support-layer dossier now paired with a hardened shared pronoun candidate TSV and a completed `ko` analyzer-quality fix | keep `ei/eite` unresolved and treat philologically checked Tedim evidence, not Henderson alone or export labels alone, as the control in later person-marking work |
| stem alternation | yes (`dossier_stem_alternation.md`) | yes (`grammar_stem_alternation_print_slice.md`; planning file) plus working prose draft (`grammar_stem_alternation_section_draft.md`) | yes (`dictionary_stem_alternation_print_slice.md`) | yes (`review_notes_stem_alternation.md`) | yes (`candidates_stem_alternation.tsv`) | `tests/test_stem_alternation_candidates.py`, `tests/test_stem_alternation_corpus_audit.py`, `tests/test_stem_alternation_lexical_inventory.py`, plus extractor reproducibility coverage | no explicit report correction located; review notes instead describe noisy report/questionnaire layers | Form I / Form II distribution, noisy questionnaire output, lexical-family contamination (`ngai/ngaih`), caveated expansions such as `za ~ zak` and `nusia ~ nusiat` | review-ready evidence architecture now in place: candidate TSV, broader corpus audit, tracked summaries, lexical inventory, citation shortlist, syntactic-context matrix, pair-discussion plan, and first working prose draft | hold stable for maintenance and human review while case marking becomes the next retrofit |
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

Stem alternation now has a fuller review-ready evidence stack. In addition to `candidates_stem_alternation.tsv`, the packet now has `stem_alternation_corpus_audit.tsv`, `stem_alternation_environment_summary.tsv`, `stem_alternation_pair_summary.tsv`, `stem_alternation_example_matrix.tsv`, `stem_alternation_lexical_inventory.tsv`, `stem_alternation_promotable_examples.tsv`, `stem_alternation_manual_promotion_review.tsv`, `stem_alternation_citation_shortlist.tsv`, `stem_alternation_syntactic_context_matrix.tsv`, `stem_alternation_pair_discussion_plan.tsv`, and a first working prose draft in `grammar_stem_alternation_section_draft.md`. That stack is rich enough for the current publication-review maturity target. The topic should now be held stable for human review rather than polished further before other slices catch up.

### Case marking

Case marking has now entered the candidate-first workflow without yet gaining an extractor route. The packet still has `grammar_case_marking_print_slice.md`, `review_notes_case_marking.md`, and a dictionary slice under the older filename `dictionary_case_markers_print_slice.md`, and it now also has `candidates_case_marking.tsv` plus `dossier_case_marking.md`. The packet should now stay conservative: the new dossier interprets which claims are directly supported, which ones remain caveated, and why homographic `-in`, raw `-ah` / `-a` overgeneration, source `-pan` with conservative `-panin`, source-vs-relator-noun boundaries, and `-tawh` accompaniment vs material/instrumental extension still need explicit guardrails.

## Recommended retrofit order

With demonstratives, negation, pronouns / clusivity, stem alternation, and now the first case-marking candidate layer all present under the current protocol, the remaining practical order should be:

1. **Case marking packet review next** — use the new analyzer-aware candidate TSV to revisit the existing grammar and dictionary slices conservatively.
2. **Then decide between another retrofit or a genuinely new topic** — after case marking has been checked against the new candidate layer, reassess whether another existing slice needs the same treatment.
3. **Demonstratives, negation, pronouns / clusivity, and stem alternation remain maintenance/human-review topics for now**.

## Conclusion

The retrofit audit now supports a clearer roadmap. Demonstratives remains the protocol pilot, negation is the first hardened retrofit, pronouns / clusivity is the second hardened retrofit with its `ko` analyzer issue addressed upstream, stem alternation is the third completed retrospective retrofit at the publication-review evidence-architecture level, and case marking now has its first analyzer-aware candidate layer even though extractor support is still pending.
