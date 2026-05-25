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
| pronouns | no separate pronoun dossier; clusivity handled in a separate dossier | yes | yes | yes | no | `tests/test_pronoun_clusivity_docs.py` | yes: `docs/grammar/reports/06-func-01-pronouns.md` now treats `ko/kote` as exclusive and keeps `ei/eite` under review | unresolved `ei/eite`, `ko/kote`, possessive vs agreement prefixes, `hong-/kong-` | usable packet with a partial report correction, but not yet candidate-backed | retrofit after negation; likely share work with the clusivity dossier rather than force a full pronoun rewrite |
| pronoun clusivity | yes (`dossier_pronoun_clusivity.md`) | no | no | no separate review note | no | `tests/test_pronoun_clusivity_docs.py` | yes, via the partial correction in `docs/grammar/reports/06-func-01-pronouns.md` | mixed `ei/eite`, more stable `ko/kote`, dialogue-context sensitivity | dossier-only support layer that still feeds the pronoun packet | treat as part of the pronoun retrofit rather than as a stand-alone print packet |
| stem alternation | yes | yes | yes | yes | no | no packet-specific publication-review test located | no explicit report correction located; review notes instead describe noisy report/questionnaire layers | Form I / Form II distribution, noisy questionnaire output, lexical-family contamination (`ngai/ngaih`), caveated expansions such as `za ~ zak` and `nusia ~ nusiat` | strong packet, but still depends on manual filtering rather than explicit candidate rows | third retrofit candidate; add a candidate file for core pairs and explicitly excluded pairs |
| negation | yes | yes | yes | yes | yes (`candidates_negation.tsv`) | `tests/test_negation_candidates.py` plus extractor reproducibility coverage | yes: `docs/grammar/reports/06-func-04-negation.md` was minimally corrected so Genesis 2:25 and `V lo uh` no longer mislead the packet | `kei` negator vs pronoun, `lo` vs `loh`, `V lo uh`, `kuamah`, `bangmah`, `thei lo / theih loh` | first retrofit now completed under the candidate-first workflow | review and harden the new negation candidate file before moving to pronouns |
| demonstratives/deixis | yes | yes | yes | yes | yes (`candidates_demonstratives.tsv`) | `tests/test_demonstratives_docs.py`, `tests/test_publication_evidence_protocol.py`, `tests/test_publication_candidate_extractor.py` | yes: `docs/grammar/reports/06-func-02-demonstratives.md` now carries explicit correction notes | `hi`, exact `hih ciangin`, `tua` / `hua`, raw-search false friends | current pilot for the protocol-backed workflow | no immediate retrofit needed beyond maintenance and future topic extension |

## Topic-by-topic audit notes

### Demonstratives/deixis

Demonstratives is already protocol-backed. It has a dossier, synchronized print packet, review notes, a candidate TSV, a protocol test, and a reproducibility test for the extractor. It should be treated as the working model for future candidate-first packet work. No immediate retrofit is needed beyond normal maintenance.

### Negation

Negation was the highest-priority retrofit, and it now has an analyzer-aware candidate file. That retrofit was warranted because the packet has an unusually high ambiguity profile: `kei` is homographic with the first-person singular pronoun, `lo` and `loh` need constructional rather than string-based handling, `V lo uh` has already proved easy to misread, and `kuamah` / `bangmah` overgenerate under raw search. The new `candidates_negation.tsv` now makes the packet substantially closer to the newer protocol standard.

### Pronouns

The pronoun packet itself is usable, but it is only partly protocol-hardened. A separate clusivity dossier exists, and the generated pronoun report has already been partially corrected so that `ko/kote` stays exclusive while `ei/eite` remains under review. That means the packet should not be reopened broadly, but it does need a future candidate layer that can separate stable person-marking evidence from the still unresolved clusivity material.

### Pronoun clusivity

Pronoun clusivity should be treated as a support-layer retrofit rather than as its own print packet. The dossier remains valuable because it established the current partial correction, but it does not yet have a candidate TSV or a packet-specific review-note layer. Any later candidate extraction here should be designed to preserve the mixed `ei/eite` evidence instead of forcing a premature resolution.

### Stem alternation

Stem alternation is a strong packet, but it still depends on manual curation layered over noisy reports and questionnaire output. The review notes already admit that the report layer is too uneven to auto-generate the chapter safely. A future candidate file should therefore focus on a controlled set of analyzer-backed Form I / Form II pairs, plus explicit exclusions for lexical-family traps and non-simple alternations. This looks important, but less urgent than negation or pronouns.

### Case marking

Case marking remains the editorial model, but it predates the candidate-first protocol and still exposes extraction risk. The review notes explicitly mention that automatic example selection is weak for ergative `-in`, and that `-panin` is being handled conservatively. A future candidate file would help with `-in`, `-ah`, `-a`, `-pan`, and `-tawh`, especially where raw orthography and homography overgenerate. Still, the current audit does not reveal a packet-level contradiction urgent enough to move case marking ahead of negation or pronouns.

## Recommended retrofit order

With negation now retrofitted, the remaining practical order should be:

1. **Pronouns / clusivity next** — unresolved `ei/eite` makes candidate-level evidence especially useful.
2. **Stem alternation after that** — needs explicit candidate rows for core pairs and exclusions.
3. **Case marking after stem alternation** — worthwhile, but lower urgency unless a specific extraction problem becomes pressing.
4. **Demonstratives maintenance only** — already protocol-backed.

## Conclusion

The retrofit audit now supports a clear updated next step: review and harden `output/publication_review/candidates_negation.tsv`, then move to the pronoun / clusivity retrofit rather than opening a brand-new grammar topic. Demonstratives remains the protocol pilot, negation is now the first retrofit, and the remaining backlog should move toward the same candidate-first architecture in the order above.
