# Verbal `-pih` and stem alternation diagnostic

## 1. Literature statement

The controlling sources converge on one core claim: verbal comitative `-pih` is a Stem 2 / Form II selecting suffix.

- **Henderson (1965)** (as summarized in `docs/grammar/morphemes/06-derivational.md`) does **not** present verbal `-pih`; she presents nominal `-pih` ('member / group member') as a separate category.
- **Otsuka** (summarized in `docs/grammar/morphemes/06-derivational.md` and `docs/grammar/lit-reviews/05-verb-09-valency-lit.md`) states that comitative `-pih` attaches to **Form II** intransitive and transitive stems.
- **Zam Ngaih Cing** (same sources) states the same Stem 2 restriction and gives explicit grammaticality contrasts (`tut-pih` vs `*tu-pih`; `nuih-pih` vs `*nui-pih`).
- `docs/grammar/reports/05-verb-08-derivational.md` and `docs/grammar/reports/05-verb-09-valency.md` surface many `-pih` forms, but those report rows are discovery-layer evidence and do not by themselves resolve stem diagnostics.

**Literature-level conclusion:** Stem 2 selection is the best-supported analysis for verbal `-pih`.  
**Corpus-level caution:** not every frequent `-pih` form is equally diagnostic for that rule.

## 2. Candidate inventory and stem-diagnostic classification

| Surface `-pih` form | Proposed base | Suspected Form I | Suspected Form II | Stem-II transparency in `-pih` form | Stem-diagnostic class | Morphophonological explanation needed? | Source references | Packet role |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `paipih` | `pai-` | `pai` | `paih` (or zero-alternation `pai`) | compatible, but not transparent | `morphophonological_boundary` | yes (possible `paih + -pih` > `paipih`) | Gen 2:22; Matt 4:1; stem questionnaire GO block | promoted with caveat |
| `nekpih` | `nek-` | `ne` | `nek` | transparent | `diagnostic_form_ii` | no | Prov 7:15; Luke 11:37; stem packet core `ne/nek` | promoted diagnostic |
| `tunpih` | `tun-` | uncertain (`tun` / `tung` overlap) | uncertain | compatible, not independently diagnostic | `compatible_not_diagnostic` | maybe | Gen 8:11; Matt 9:2 | promoted for function, non-diagnostic for stem rule |
| `hopih` | `ho-` / `hop-` (unclear) | unclear | unclear | unclear | `lexicalized_or_unclear` | yes | Gen 27:5; Matt 12:46 | supporting only |
| `hehpih` | `heh-` (lexical grace family) | unclear | unclear | unclear | `lexicalized_or_unclear` | yes | Gen 33:11; Matt 5:7 | boundary |
| `ompih` | `om-` | `om` | likely same-form or non-alternating | compatible only | `compatible_not_diagnostic` | no | Gen 21:20; Matt 17:17 | supporting only |
| `paikhiatpih` | `pai(-h)-khiat-` | `pai` | `paih` in some derived contexts | compatible, stack-dominated | `morphophonological_boundary` | yes | Gen 19:5 (plus high-frequency stack rows) | boundary |
| `innkuanpih` / `mipihte` | nominal `-pih` | n/a | n/a | not verbal evidence | `blocked` | n/a | Gen 7:1; Gen 9:5; Henderson nominal `-pih` | boundary (nominal) |
| `tut-pih` (`*tu-pih`) | `tu/tut` | `tu` | `tut` | transparent in elicited contrast | `literature_backed` | no | ZNC contrast in `morphemes/06-derivational.md` | blocked in corpus, diagnostic in literature |
| `nuih-pih` (`*nui-pih`) | `nui/nuih` | `nui` | `nuih` | transparent in elicited contrast | `literature_backed` | no | ZNC contrast in `morphemes/06-derivational.md` | blocked in corpus, diagnostic in literature |

## 3. Focused treatment of `paipih` (`pai / paih`)

The packet has to choose among five live accounts:

1. `paipih = pai + -pih` (Form I base), which would weaken strict Stem 2 selection.
2. `paipih = paih + -pih` with non-realization of `h` before `p`.
3. `pai / paih` is unstable enough that `paipih` is not a reliable diagnostic row either way.
4. `paipih` is lexicalized/special and cannot be used for stem diagnostics.
5. Literature Stem 2 restriction is still correct even if `paipih` is not the best diagnostic item.

### Evidence considered

- The stem questionnaire GO block currently contains internally mixed evidence: it labels GO as `pai` Form I / `pai` Form II, while the current stem print slice keeps `pai / paih` in its difficult set.
- Analyzer-facing corpus output has abundant `paipih` as `pai-pih`, but it does not provide minimal-pair `paih-pih` rows.
- The same corpus/analyzer layer does attest `paih` in derived forms (for example `paih-khiat`, `paih-sak`) with Stem-II-like behavior in some rows.

### Best-supported decision

`Paipih` is **best treated as morphophonological boundary evidence** for stem diagnostics:

- It remains strong, promoted evidence for the **verbal comitative-applicative function** of `-pih`.
- It is **compatible** with Stem 2 selection.
- It is **not** the primary diagnostic row for proving Stem 2 selection, because the underlying `pai / paih` relation remains unresolved in packet-level corpus evidence.

This preserves the strong literature rule without pretending that `paipih` alone settles the stem alternation question.

## 4. Comparison with clearer forms

`Nekpih` is currently the clearest packet-internal diagnostic because `ne / nek` is independently stabilized in the stem-alternation packet and `nek` is a recognized Form II shape. By contrast:

- `tunpih` supports verbal `-pih` but has weaker independent stem diagnostics in the current packet.
- `hopih`, `hehpih`, and `ompih` are useful distributional/supporting rows, but their stem alternation status is unclear, lexicalized, or same-form.
- ZNC elicited contrasts (`tut-pih` vs `*tu-pih`; `nuih-pih` vs `*nui-pih`) remain important literature-backed diagnostics even though they are blocked from corpus-style print promotion.

## 5. Implications for packet stabilization

### Decision for grammar-facing phrasing

Use this formulation:

1. Verbal `-pih` is best treated as a Stem 2 / Form II selecting comitative applicative in the literature-backed analysis.
2. Packet evidence is split into:
   - **diagnostic_form_ii** rows (`nekpih`);
   - **compatible_not_diagnostic** rows (`tunpih`, `ompih`);
   - **morphophonological_boundary** rows (`paipih`, `paikhiatpih`);
   - **lexicalized_or_unclear** rows (`hopih`, `hehpih`);
   - **literature_backed** elicited diagnostics (`tut-pih`, `nuih-pih`);
   - **blocked** non-verbal rows (nominal `-pih`).
3. `Paipih` should remain promoted for comitative-applicative function, but explicitly caveated for stem diagnostics.

### Candidate layer changes required

- Add explicit stem-diagnostic status coding to each candidate row.
- Keep nominal `-pih` rows blocked for stem diagnostics.
- Preserve elicited ZNC diagnostic pairs as literature-backed blocked rows.

### `dingin` harmonization decision

In this packet, `dingin` should follow the same grammar-facing convention already used in TAM, clause-linkage, and VP sections:

- segmentation: `ding-in`
- gloss: `IRR-ERG`
- prose label: purposive / clause-bound irrealis boundary

It should not be reanalyzed here as a packet-specific nominalization rule.
