# Analyzer vs Literature Gaps - Complete Documentation

## Document Organization

This analysis systematically compares the Tedim Chin morphological analyzer's current glossing with what the linguistic literature recognizes as distinct categories. Three complementary documents provide different levels of detail:

### 📋 **START HERE: Quick Reference**
**File**: `ANALYZER_GAPS_QUICK_REFERENCE.md`
- **Audience**: Developers, quick decision-makers
- **Length**: 2-3 pages
- **Content**: 
  - At-a-glance comparison table (12 gaps ranked by severity)
  - Phase 1-3 implementation roadmap
  - Blocked issues checklist
  - Implementation checklist

**Best for**: Understanding what needs to be fixed and in what order

---

### 📊 **Executive Summary**
**File**: `ANALYZER_LITERATURE_SUMMARY.txt`
- **Audience**: Project leads, grammar researchers
- **Length**: 8-10 pages
- **Content**:
  - Overview of gap categories
  - 10 critical/major gaps with detailed descriptions
  - Impact and fix difficulty assessments
  - Recoverability matrix
  - Phase 1-3 roadmap with effort estimates

**Best for**: Understanding scope of work and priorities

---

### 📖 **Complete Technical Analysis**
**File**: `ANALYZER_LITERATURE_GAPS.md`
- **Audience**: Linguists, developers doing implementation
- **Length**: ~15 pages
- **Content**:
  - Detailed gap-by-gap analysis
  - Morpheme categories: Prefixes, Cases, Aspect, Directionals, Modals, Derivational
  - For each gap:
    - What analyzer currently does
    - What literature says
    - Why the distinction matters
    - How to recover it
  - Summary tables by severity and recoverability
  - Priority roadmap with phase details

**Best for**: Deep understanding of each gap; implementation guidance

---

### 💡 **Real Corpus Examples**
**File**: `ANALYZER_GAPS_CORPUS_EXAMPLES.md`
- **Audience**: Anyone wanting concrete examples
- **Length**: ~8 pages
- **Content**:
  - 9 real cases from Bible corpus showing analyzer failures
  - For each gap:
    - Actual analyzed text
    - Current (wrong) gloss
    - What literature says
    - Why it matters
    - How to fix it
  - Summary statistics on gap impact

**Best for**: Understanding gaps through concrete examples; motivation for fixes

---

## Quick Navigation

**Want to understand...** → Read this document:

| Question | Document | Section |
|----------|----------|---------|
| What are the 3 most important fixes? | Quick Ref | Phase 1: Critical Fixes |
| What's blocking us? | Executive Summary | Blocked Issues (❌) |
| Is this gap fixable with current data? | Technical Analysis | Section 9: Recoverability Matrix |
| How would this appear in actual text? | Corpus Examples | All sections |
| How much work is each gap? | Executive Summary | Gaps 1-10 |
| What does the literature say about -sak? | Technical Analysis | 6.1: Causative/Benefactive |

---

## Gap Summary by Category

### CRITICAL GAPS (🔴 Must fix for serious analysis)

1. **Causative-Benefactive ambiguity (-sak)**
   - Analyzer: Glosses all as CAUS
   - Literature: Form I = CAUS, Form II = BENF
   - Impact: ~5% of corpus
   - Recoverable: YES (check verb form)
   - Docs: Quick Ref (✦#1), Executive Summary (Gap 1), Technical Analysis (6.1), Examples (1)

2. **Tone distinction in -a case marker**
   - Analyzer: Glosses all as LOC
   - Literature: -á = GEN, -à = INSTR/LOC
   - Impact: Unknown (tone not preserved)
   - Recoverable: NO (blocked on tone restoration)
   - Docs: Quick Ref (❌), Executive Summary (Gap 2), Technical Analysis (2.1), Examples (2)

3. **Missing -suk, -phei directionals**
   - Analyzer: Absent
   - Literature: Core elevation system (-toh, -suk, -phei)
   - Impact: ~200-300 tokens (0.02%)
   - Recoverable: YES (trivial inventory addition)
   - Docs: Quick Ref (✦#3), Technical Analysis (4.1), Examples (3)

4. **Inverse marking constraints (hong-)**
   - Analyzer: Unmarked co-occurrence pattern
   - Literature: hong- obligatory with 1/2 person causees
   - Impact: ~0.5% of corpus
   - Recoverable: YES (add constraint rules)
   - Docs: Quick Ref (✦#4), Executive Summary (Gap 4), Technical Analysis (1.2), Examples (4)

5. **Agreement vs Possession (ka-, na-, a-)**
   - Analyzer: Undifferentiated
   - Literature: Context-dependent (verb = agreement; noun = possessive)
   - Impact: ~12% of corpus
   - Recoverable: YES (check POS of following word)
   - Docs: Quick Ref (✦#5), Executive Summary (Gap 5), Technical Analysis (1.1), Examples (5)

### MAJOR GAPS (🟠 Should improve for complete analysis)

6. **Habitual system incompleteness**
   - Missing: ngei, gige, zel
   - Docs: Technical Analysis (3.1), Examples (6)

7. **Form-dependent allomorphy (-thei/-theih)**
   - Missing: Form I/II distinction
   - Docs: Technical Analysis (5), Examples (7)

8. **-pih Form II requirement**
   - Missing: Constraint documentation
   - Docs: Technical Analysis (6.2), Examples (8)

### MINOR GAPS (🟡 Nice-to-have)

9. **Undifferentiated desideratives** (-nuam vs -nop)
10. **NEG.ABIL variants** (-pah, -pak, -lawh)
11. **Questionable directional classifications**
12. **Non-standard glosses** (terminology)

---

## Phase-Based Implementation Guide

### PHASE 1: CRITICAL FIXES (Do first - enables ~95% accuracy)
**Effort**: ~2-3 days per item for experienced developer
**Impact**: ~5-15% improvement in output accuracy

1. ✦ Implement -sak dual-glossing (CAUS vs BENF)
2. ✦ Add -suk, -phei to inventory
3. ✦ Document inverse marking rules
4. ✦ Mark prefix agreement vs possession contexts

**See**: Quick Reference "Phase 1: Critical Fixes" for code-level guidance

### PHASE 2: MAJOR IMPROVEMENTS (Next - adds ~97% accuracy)
**Effort**: ~1-2 days per item
**Impact**: Additional 2-3% improvement

1. ⚡ Add habitual system (ngei, gige, zel)
2. ⚡ Implement -thei/-theih Form-dependent glossing
3. ⚡ Document -pih Form II requirement
4. ⚡ Add co-occurrence constraint checking

**See**: Quick Reference "Phase 2: Major Improvements" for guidance

### PHASE 3: POLISH (Later - refinement)
**Effort**: ~1 day per item
**Impact**: Additional 1-2% improvement

1. 🔧 Verify directional stem status
2. 🔧 Clarify aspect/modal boundary cases
3. 🔧 Standardize terminology
4. 🔧 Complete literature extraction

### BLOCKED ITEMS (Require additional resources)
- Tone distinction in -a (needs corpus with tone marks)
- Complete -nuam/-nop distinction (needs research)
- Complete -pah/-pak/-lawh distinction (needs research)

---

## Literature Sources

All gaps are grounded in published linguistic literature:

| Source | Content | Citations |
|--------|---------|-----------|
| ZNC (2017/2018) | Most comprehensive modern grammar | 50+ citations throughout |
| Henderson (1965) | Foundational descriptive study | 15+ citations |
| Otsuka (2009) | Specialized study of -sak | Multiple technical gaps |
| Otsuka (2024) | Applicative constructions | Constraints documentation |
| Singh (2018) | Comparative cognate data (Sukte) | ~5 citations |

---

## How to Use These Documents

**If you have 5 minutes**: Read "Quick Reference" → understand priority list

**If you have 15 minutes**: Read "Executive Summary" → understand scope and effort

**If you need to implement**: Read "Technical Analysis" → get implementation guidance

**If you need examples**: Read "Corpus Examples" → see real failures and solutions

**If doing literature review**: Use "Complete Analysis" as reference document

---

## Key Statistics

| Metric | Value |
|--------|-------|
| Total gaps identified | 12 major categories |
| Critical (must fix) | 5 gaps |
| Major (should fix) | 4 gaps |
| Minor (nice-to-have) | 3 gaps |
| Blocked (need external resources) | 2 gaps |
| Gaps recoverable with current data | ~10 (83%) |
| Gaps unrecoverable | ~1 (tone) |
| Gaps requiring research | ~2 (desiderative, NEG.ABIL) |
| Estimated impact of critical gaps | 15-20% of corpus |
| Estimated impact after Phase 1 fixes | Reduces to 5-10% |
| Estimated impact after Phase 2 fixes | Reduces to 1-3% |

---

## Related Documents

Also in `/docs/grammar/`:
- `morphemes/01-prefixes.md` - Literature on prefix system
- `morphemes/02-case-markers.md` - Literature on cases
- `morphemes/03-aspect.md` - Literature on aspect/TAM
- `morphemes/04-directional.md` - Literature on directionals
- `morphemes/05-modal.md` - Literature on modals
- `morphemes/06-derivational.md` - Literature on derivational affixes

In `/scripts/`:
- `analyze_morphemes.py` - Analyzer implementation (lines 165-390: gloss dictionaries)

In `/docs/grammar/reports/`:
- Sample corpus analysis showing current glossing

---

## Feedback & Updates

These documents represent analysis as of 2025-03-21. They should be updated as:
1. Implementation proceeds
2. New literature becomes available
3. Corpus statistics are refined
4. Linguistics research clarifies remaining gaps

*Last updated: 2025-03-21*

