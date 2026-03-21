# TEDIM CHIN MORPHOLOGICAL ANALYZER vs. LITERATURE: GAP ANALYSIS

**Date**: 2025-03-21  
**Sources Compared**:
- Analyzer glossing: `/scripts/analyze_morphemes.py`
- Literature: ZNC (2017/2018), Henderson (1965), Otsuka (2009-2024), Singh (2018)
- Morpheme databases: `/docs/grammar/morphemes/*.md`

---

## 1. PREFIXES

### 1.1 Pronominal Prefixes (ka-, na-, a-, i-)

| Aspect | Analyzer | Literature | GAP | Recoverable? |
|--------|----------|-----------|-----|-------------|
| **ka-** | `1SG` | 1SG + 1PL.EXCL; Agreement vs Possession marker | Ambiguity: Does ka- mark subject agreement OR possessive on nouns? | YES - Syntactic position (verb vs noun) |
| **na-** | `2SG` | 2SG + 2PL; Agreement vs Possession | Same as ka- | YES - Same method |
| **a-** | `3SG` | 3SG + Relativizer; Default nominal prefix | Conflates two functions: agreement marker vs relativizer (relative clause marker) | PARTIALLY - Requires clause structure parsing |
| **i-** | `1PL.INCL` | 1PL.INCL specific; no inclusive/exclusive distinction in other prefixes | Incomplete: Analyzer doesn't mark clusivity distinction for ka- (1SG/EXCL) vs i- (INCL) | YES - Infer from concordant pronoun (kote/eite) |

**KEY MISSING DISTINCTION**: 
- Literature distinguishes AGREEMENT prefixes (on verbs) from POSSESSIVE prefixes (on nouns)
- Analyzer treats them as single morphemes without noting the dual function
- Henderson (1965, pp. 32-33) emphasizes this is a CONCORD system at sentence level

---

### 1.2 Directional/Object Prefixes (kong-, hong-)

| Aspect | Analyzer | Literature | GAP | Recoverable? |
|--------|----------|-----------|-----|-------------|
| **kong-** | `1SG→3` | 1st person acting toward 2nd person; "inverse" marker (Otsuka 2009) | Analyzer glosses as "to 3rd" but literature calls it INVERSE marking for 1→2 directionality | PARTIALLY - Requires analysis of whole clause argument structure |
| **hong-** | `3→1` | VENITIVE ("toward speaker") + INVERSE marker obligatory for 1st/2nd person causees | Analyzer identifies only object relation, misses the OBLIGATORY marking pattern in causatives | YES - Check if -sak present & causee is 1/2 person |

**KEY MISSING DISTINCTIONS**:
1. Inverse marking patterns (Otsuka 2009 shows hong- is obligatory with certain argument combinations)
2. Distinction between DEICTIC function (toward speaker) vs APPLICATIVE function (inverse)
3. Co-occurrence constraints with -sak

---

## 2. CASE MARKERS

### 2.1 Overview

| Marker | Analyzer Gloss | Literature Status | GAP | Notes |
|--------|---|---|---|---|
| **-in** | `ERG` | Ergative; phrase-final particle in Henderson | Single gloss but dual status in literature | Analyzer treats as case; Henderson calls it "particle" |
| **-ah** | `LOC` | Location OR destination | Underdifferentiated | Can't distinguish STATIVE location vs GOAL destination |
| **-a** | `LOC` | High tone = GEN; Low tone = INSTR/LOC (ZNC) | **MAJOR GAP**: Analyzer ignores tonal distinction | YES - Preserve tone marks |
| **-pan** | `ABL` | Ablative (source) | Correctly identified | No gap |
| **-tawh** | `COM` | Comitative + Instrumental (multifunction) | Analyzer marks only as `COM` | NO - Requires semantic context |

**CRITICAL MISSING FEATURE**:
- Analyzer glosses **-a** uniformly as `LOC` but literature documents HIGH tone (-á) = **GEN** vs LOW tone (-à) = **INSTR/LOC**
- This is a fundamental distinction that CANNOT be recovered without tone preservation

**Secondary gap**:
- **-ah** vs **-a** (locative) distinction not clearly marked
- ZNC documents both as locatives but with different productivity/collocations

---

## 3. ASPECT SUFFIXES

### 3.1 Stacking & Interaction Patterns

| Marker | Analyzer | Literature Pattern | GAP | Recoverable? |
|--------|----------|---|---|---|
| **-khin** | `IMM` | COMPL; CAN STACK with -ta | Analyzer gloss `IMM` is non-standard; literature calls it "already/just completed" | YES - Rename to `COMPL` |
| **-ta** | `PFV` | Perfective; aspect suffix at specific position | Analyzer treats as TAM but position constraints unclear | PARTIALLY |
| **-zo** | `COMPL` | Completive "successfully done" | -zo glossed identically to -khin but literature distinguishes them | YES - They mark different completion types |
| **-kik** | `ITER` | Iterative "again"; also part of 4-way habitual system | Missing: -kik, -nawn, -to all glossed as aspect but literature shows them as part of a HABITUAL SYSTEM that includes ngei, gige, zel | Need reclassification |
| **-nawn** | `CONT` | Continuative "still"; implies continuation from prior point | More frequent than -to (1,023 vs 145 attestations) | YES - Mark frequency difference |
| **-to** | `CONT` | "general ongoing" but much rarer than -nawn | Same gloss as -nawn | YES - Distinguish or add frequency notes |
| **-lai** | `PROSP` in analyzer; also `PROG` in grammar | ZNC lists as both PROGRESSIVE (§5.6.3) AND MODAL (§5.7) | **DUAL CLASSIFICATION**: Analyzer treats as modal but literature shows it functions as aspect | Requires context |
| **-mang** | `COMPL` | Strong completive "completely"; appears with destruction/revealing verbs | Glossed as COMPL; indistinguishable from -zo/-khin in analyzer | Possibly lexically motivated |
| **-zawh** | `finish` | Resultative "done V-ing"; result state emphasis | Glossed as `finish` (non-standard); position-specific | YES - More analysis needed |
| **-kim** | `fully` | Intensive "thoroughly"; rare (15 occurrences) | Not clearly marked as aspect vs modifier | Probably intensive adverbializer, not aspect |

**MAJOR GAPS**:
1. **Habitual system**: ZNC documents 4-way habitual (ngei, gige, zel, kik) - analyzer only marks kik
2. **Missing particles**: ngei, gige, zel, -den, -lai(prog) not fully cataloged
3. **Stacking rules**: Only khin-ta documented; others underdocumented
4. **Position uncertainty**: Analyzer doesn't enforce position slots clearly

---

## 4. DIRECTIONAL SUFFIXES (post-verbal)

| Marker | Analyzer | Literature | GAP | Recoverable? |
|--------|----------|-----------|-----|-------------|
| **-toh** | `up` | UP; elevational (northward) | Analyzer uses English "up" not standard gloss | YES - Use `UP` |
| **-suk** | NOT in analyzer | DOWN; elevational (southward) | **MAJOR GAP**: -suk is documented in ZNC §5.8.2.3 but missing from analyzer | Yes - Add it |
| **-phei** | NOT in analyzer | HORIZ; horizontal/level motion | **MAJOR GAP**: Documented in ZNC but missing from analyzer | Yes - Add it |
| **-lam** | `DIR` | TOWARD; goal-oriented (may be postposition) | Vague gloss; literature suggests postposition status | Possibly |
| **-khia** | `out` | Status unclear - appears as lexical "drop" in ZNC vocabulary | Unconfirmed - may be lexicalized | Needs review |
| **-khiat** | `away` | Not clearly documented; analyzer lists it | Unconfirmed | Needs verification |
| **-lut** | `in` | IN; inward motion (from Sukte cognate) | Analyzer marks but needs verification for Tedim productivity | Check for examples |
| **-cip** | `down` | Not clearly directional; ZNC lists as adjective "hard/unbreakable" | **MAJOR ERROR**: Analyzer may have wrong classification | Needs reclassification |
| **-tang** | `arrive` | Appears as verb "move" and adjective "bright"; unclear if productive suffix | Questionable suffix status | Needs verification |
| **-sawn** | `toward` | Appears as verb "passed on"; unclear if productive suffix | Questionable suffix status | Needs verification |

**CRITICAL ISSUES**:
1. **Missing core items**: -suk, -phei are documented in ZNC §5.8.2.3 but absent from analyzer
2. **Questionable classifications**: -khia, -cip, -tang, -sawn may be misclassified lexical verbs
3. **Incomplete inventory**: No elevation-based organization despite literature showing 3-way elevation system (UP/DOWN/HORIZ)

---

## 5. MODAL SUFFIXES

| Marker | Analyzer | Literature | GAP | Recoverable? |
|--------|----------|-----------|-----|-------------|
| **-ding** | `IRR` | Irrealis/future; **most frequent modal** (19,963 attestations) | Correctly identified but analyzer doesn't note it stacks with other modals | Note stacking patterns |
| **-thei/-theih** | `ABIL` / `ABIL` | Abilitative; Form I = -thei, Form II = -theih (allomorph) | Analyzer marks both as `ABIL` but doesn't note the STEM-DEPENDENT allomorphy | **Recoverable** - Check verb stem form (Form I vs II) |
| **-nuam** | `want` | Desiderative (want to); **630 attestations** | Marked as `want` not standard gloss `WANT` or `DESID` | Minor - standardize gloss |
| **-nop** | `want` | Desiderative variant; **216 attestations** | Same gloss as -nuam, no distinction | PARTIALLY - May have register/nominalization differences |
| **-mawk** | `perhaps` | Dubitative (uncertainty) | Marked as `perhaps` rather than `DUB` | Minor - standardize |
| **-pah/-pak/-lawh** | `NEG.ABIL` / `NEG.ABIL` / `NEG.ABIL` | Negative ability (three variants) | All grouped under single gloss; **literature doesn't explain distinction** between -pah, -pak, -lawh | NO - Unknown conditioning factors |
| **-kul** | `must` | Deontic necessity; **rare** | Non-standard gloss; should be `DEON` | Minor |
| **-ngei** | `EXP` | Experiential; **748 attestations**; also habitual aspect | Correctly marked but position ambiguous (aspect vs modal) | PARTIALLY - Check co-occurrence patterns |
| **-lai** | `PROSP` | Can be PROGRESSIVE (aspect) OR PROSPECTIVE (modal) | **Analyzer lists as modal only** but ZNC documents as aspect in §5.6.3 | YES - Check context |

**KEY GAPS**:
1. **Stem-dependent allomorphy** (-thei/-theih): Not captured
2. **Conflicting classifications**: -ngei, -lai span aspect/modal boundary
3. **Unexplained variants**: -pah/-pak/-lawh lack conditioning explanation (phonological? lexical? register?)

---

## 6. DERIVATIONAL SUFFIXES

### 6.1 Causative/Benefactive: -sak

| Feature | Analyzer | Literature | GAP | Recoverable? |
|---|---|---|---|---|
| **Function** | `CAUS` | Dual: Form I stem + -sak = CAUSATIVE; Form II stem + -sak = BENEFACTIVE | **CRITICAL**: Analyzer marks only as `CAUS`; doesn't distinguish causative from benefactive | **YES** - Check verb stem form (Form I vs II) |
| **Morphological status** | Suffix | **DISPUTED**: Henderson treats as verb; Otsuka as bound suffix; ZNC as suffix (consensus) | Not an issue for analyzer | — |
| **Allomorphy** | Single form | Tone varies: -sàk (Low) normally, -sák (High) after Mid tone (ZNC) | Analyzer doesn't mark tone behavior | **RECOVERABLE** but requires tone data |
| **Distribution** | Single inventory | Cannot co-occur with -pih or -san (Otsuka 2024) | No co-occurrence constraints marked | **Potentially recoverable** - check suffix sequences |
| **Double causative** | Single -sak | Can reduplicate for 3-argument causation (rare; Otsuka p. 19) | Not documented in analyzer | Rare in corpus |
| **Related prefix** | Not documented | su- prefix also marks volitional causative (ZNC §5.8.2.1) | **MAJOR GAP**: Analyzer doesn't document su- as causative | Separate lexical entry |

**CRITICAL MISSING DISTINCTION**:
- **Analyzer glosses all -sak as `CAUS` but literature requires distinguishing CAUSATIVE (Form I + -sak) from BENEFACTIVE (Form II + -sak)**
- This is fully recoverable if verb stem form is tracked

---

### 6.2 Applicatives: -pih vs -khawm

| Feature | Analyzer | Literature | GAP | Recoverable? |
|---|---|---|---|---|
| **-pih** | `APPL` | Comitative applicative; **Form II only** (strict requirement) | Analyzer doesn't mark Form II requirement | **YES** - Check stem form |
| **Constraint** | No marking | Cannot co-occur with -sak (Otsuka 2024: "Neither benefactive nor causative -sak co-occurs with comitative -pih") | No constraints documented | **YES** - Check suffix sequences |
| **Interpretation** | Single gloss | Three reading types: (a) comitative participant, (b) comitative object, (c) benefactive sense (Otsuka 41b) | Single-valued | PARTIALLY - Requires sentence structure analysis |
| **Homonymy** | Not noted | Homophonous with nominal -pih "group member" (Henderson 1965) | Analyzer may conflate instances | **YES** - Distinguish by syntactic context |
| **-khawm** | `COM` | Comitative "together with someone" | Same gloss as -pih in some cases | Needs separate analysis; literature incomplete on -khawm |

**GAPS**:
1. -pih form requirement (Stem II only) not captured
2. -pih/-sak co-occurrence constraints not marked
3. Homonymy with nominal -pih not noted
4. -khawm poorly documented in literature; analyzer can't improve

---

### 6.3 Other Derivational Suffixes

| Marker | Analyzer | Literature | GAP | Recoverable? |
|---|---|---|---|---|
| **-gawp** | `INTENS` | Intensive "forcefully" | Marked but needs verification | — |
| **-nasa** | `INTENS` | Intensive "strongly" | Marked but needs verification | — |
| **-tawm** | `DIMIN` | Diminutive "a little" | Marked but needs verification | — |
| **-zaw** | `MORE` | Comparative | Marked but literature incomplete | — |
| **-lua** | `too` | Excessive "too much" | Marked but literature incomplete | — |
| **-suak** | `become` | Inchoative "change of state" | Marked but literature incomplete | — |
| **-loh** | `NEG` | Negative result | Marked but literature incomplete | — |
| **Other: -tel, -khop, -hak, -zah, -khak** | Various | Many NOT clearly documented in literature | Multiple gaps | Needs verification |

---

## 7. SUMMARY TABLE: GAPS BY SEVERITY

### CRITICAL GAPS (Must Fix)

| Gap | Category | Issue | Solution |
|-----|----------|-------|----------|
| **Causative-Benefactive ambiguity** | Derivational | -sak glossed uniformly as `CAUS`; doesn't distinguish Form I (CAUS) from Form II (BENEF) | Check stem form; dual-gloss as `CAUS/BENF` |
| **-a tone distinction** | Case markers | LOW tone -à (INSTR/LOC) vs HIGH tone -á (GEN) | **Requires tone preservation** |
| **Missing -suk, -phei** | Directionals | Core post-verbal directionals absent from analyzer | Add to inventory |
| **Inverse marking** | Prefixes | kong-, hong- functions in applicatives not captured | Document co-occurrence constraints with -sak |
| **Agreement vs Possession** | Prefixes | ka-, na-, a- function differently on nouns vs verbs | Note syntactic context |

### MAJOR GAPS (Should Improve)

| Gap | Category | Issue | Solution |
|-----|----------|-------|----------|
| **Habitual system** | Aspect | 4-way habitual (ngei, gige, zel, kik) incompletely marked | Catalog ngei, gige, zel; connect to kik |
| **Stem-dependent allomorphy** | Modals | -thei/-theih not distinguished | Mark Form I vs II requirement |
| **-pih constraints** | Derivational | Form II requirement, -sak co-occurrence not marked | Document constraints |
| **Aspect/Modal boundary** | Aspect/Modal | -lai, -ngei straddle categories | Clarify classification |
| **Directional stem status** | Directionals | -khia, -cip, -tang, -sawn may be misclassified | Verify productivity |

### MINOR GAPS (Nice to Have)

| Gap | Category | Issue | Solution |
|-----|----------|-------|----------|
| Non-standard glosses | Multiple | `IMM` instead of `COMPL`; `DIR` instead of specific directions | Standardize to Leipzig glossing conventions |
| Rare morphemes | Various | -kul (deontic), -mawk (dubitative), reduced-attestation items | Document but lower priority |
| Literature incomplete | Various | Henderson's treatment of -khawm, -gawp not yet extracted | Continue literature review |

---

## 8. RECOVERABILITY MATRIX

Can distinctions be recovered WITHOUT additional input data?

| Distinction | Recoverable? | Method |
|---|---|---|
| Causative vs Benefactive (-sak) | YES | Check verb stem form (Form I vs II) |
| -á (GEN) vs -à (INSTR/LOC) | NO | Requires original tone preservation in corpus |
| Agreement vs Possession (prefixes) | YES | Check syntactic category (N vs V) |
| -thei vs -theih | YES | Check verb stem form |
| -pih Form II requirement | YES | Check stem form |
| Relativizer vs 3SG (a-) | PARTIALLY | Requires clause-boundary detection |
| Inverse marking (hong- obligatory) | PARTIALLY | Requires full argument structure analysis |
| Habitual distinctions | PARTIALLY | Requires aspectual/habitual system training |
| -nawn vs -to distinction | PARTIAL | Frequency-based heuristics possible |
| -suk vs -phei addition | YES | Add to static inventory |

---

## 9. PRIORITY ROADMAP

**Phase 1 (Critical - blocks many analyses):**
1. Add -sak dual-glossing (CAUS vs BENF based on stem form)
2. Document tone preservation requirement for -a marker
3. Add missing -suk, -phei to directional inventory
4. Clarify prefix agreement vs possession distinction

**Phase 2 (High-value - improves ~10-15% of outputs):**
1. Add -thei/-theih Form-dependent glossing
2. Catalog habitual system (ngei, gige, zel, kik)
3. Document -pih Form II requirement
4. Add inverse marking constraints for hong-, kong-

**Phase 3 (Polish - refinements):**
1. Verify directional stem status (-khia, -cip, -tang, -sawn)
2. Clarify -lai/-ngei aspect vs modal distinction
3. Add co-occurrence constraint checking
4. Standardize non-standard glosses

