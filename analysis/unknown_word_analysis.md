# Tedim Chin Unknown Word Analysis

**Date:** 2026-03-07
**Coverage:** 98.99% (753,675/761,347 tokens)
**Unknown tokens:** 7,672 (1.01%)
**Unknown types:** 3,731

## Summary

The remaining 1% of unanalyzed tokens fall into distinct categories, each requiring different handling strategies.

## Category Breakdown

| Category | Types | Tokens | % of Unknown |
|----------|-------|--------|--------------|
| ki- prefix forms | 1,012 | 2,048 | 26.7% |
| Short stems (≤4 chars) | 256 | 780 | 10.2% |
| Suffix forms (-na, -te, -in, -ah) | 365 | 596 | 7.8% |
| Other compounds/complex | 2,098 | 4,248 | 55.4% |

## Detailed Analysis by Category

### 1. ki- Prefix Forms (26.7% of unknowns)

These are reflexive/reciprocal verb forms where the base is not yet in our verb stem list.

**Top examples with English context:**
- `kitot` (9x) - "rebelled", "contention", "strife" → likely "to quarrel, contend"
- `kiimnai` (9x) - "smote", "plain" → unclear, possibly place-related
- `kisimmawh` (9x) - "despised", "spared" → likely "to despise" or "to spare"
- `kiciang` (9x) - "wall was built", "round about" → likely "to be arranged, set up"
- `kinial` (9x) - "contend", "answer" → likely "to contend, argue"

**Recommendation:** Extract base stems (tot, imnai, simmawh, ciang, nial) and add to VERB_STEMS if they can be independently verified.

### 2. Short Stems (10.2% of unknowns)

Two-to-four character words that are likely basic vocabulary not yet in our lexicon.

**Top examples with English context:**
- `ng` (11x) - Various contexts → may be OCR/tokenization artifact or abbreviation
- `ba` (11x) - "owed", "account" → likely "to owe, debt"
- `lapa` (10x) - "wise", "oppression" → unclear semantic field
- `nolh` (9x) - "rejected", "refused", "abhorred" → likely "to reject, refuse"
- `kunh` (9x) - "intreated", "succoured" → likely "to entreat, plead"
- `siim` (9x) - "feasted" → likely "to feast, celebrate"
- `vul` (9x) - "tree planted", "flourish" → likely "to flourish" (cf. informant Vul Za Thang)

**Recommendation:** These require individual philological verification. Add only those with clear semantic patterns.

### 3. Suffix Forms (7.8% of unknowns)

Words ending in grammatical suffixes where the base is not recognized.

**Top examples:**
- `sungtumin` (9x) - "heart", "mind" → sung-tum-in "inside-think-ERG"?
- `ututin` (9x) - "scorning", "small things" → reduplication of ut?
- `gilvah` (8x) - "Levite" → likely proper noun variant
- `dimtakin` (8x) - "filled", "knowledge" → dim-tak-in "full-truly-ERG"?

**Recommendation:** These may be analyzable with additional suffix stripping or as compounds.

### 4. Complex/Other Forms (55.4% of unknowns)

Longer words that may be compounds, loan words, or rare vocabulary.

**Top examples with semantic inference:**
- `dongun` (14x) - "harvest", "wilderness", "field" → agricultural/geographic term
- `utzaw` (11x) - "death", "sword", "slaughter" → violent/death-related
- `sungtawng` (10x) - "heart", "within", "palace" → interior/inner place
- `zomlai` (9x) - "journeyed", "went", "proceeded" → motion verb
- `zuautat` (9x) - "trespass", "falsehood" → transgression/sin
- `lawnthal` (9x) - "overthrown", "beat down" → destruction verb
- `thakhatthu` (9x) - "suddenly", "terror" → adverb/manner
- `lianlua` (9x) - "too heavy", "too great", "too high" → excessive quantity
- `tuahkhak` (9x) - "travail", "fool", "terror" → difficulty/trouble
- `tuakun` (9x) - "lying with", "meet together" → encounter verb

**Potential loan words identified:**
- Words with unusual phonotactics
- Very low frequency (hapax legomena)

## Philological Notes

### Semantic Field Analysis

From English context analysis:

1. **Agricultural vocabulary** often unknown (harvest, field, vineyard)
2. **Emotional/psychological terms** partially covered (contention, despise, pride)
3. **Architectural/spatial terms** need expansion (palace, oracle, wall)
4. **Intensive/excessive adverbs** (suddenly, greatly, exceedingly)

### Morphological Patterns

1. **Productive ki- prefix** - Most ki- unknowns have analyzable bases if the stem is in lexicon
2. **Compound words** - Many unknowns are noun+noun or verb+noun compounds
3. **Dialectal variants** - Some unknowns may be spelling variants of known words

## Action Items

### Immediate (can add now with confidence):
1. `ba` - "owe, debt" (11x, clear from "owed ten thousand talents")
2. `nolh` - "reject, refuse" (9x, clear from "rejected", "abhorred")
3. `kunh` - "entreat, plead" (9x, clear from "intreated the LORD")
4. `vul` - "flourish" (9x, matches Henderson informant name meaning)

### Investigate further:
1. `ng` - May be tokenization artifact
2. `lapa` - Unclear semantic field
3. Most ki- forms - Require base stem verification

### Henderson cross-reference:
- Only 13 of our unknowns found directly in Henderson
- Henderson vocabulary is limited to text examples, not comprehensive

## Recommendations for Proceeding

1. **Be conservative** - Only add stems with clear semantic evidence
2. **Document sources** - Note verse references for each addition
3. **Cross-validate** - Check if word appears with consistent meaning across books
4. **Flag uncertain** - Mark low-confidence glosses with "?"
