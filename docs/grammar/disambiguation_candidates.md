# Disambiguation Candidates from Dictionary Analysis

## Confirmed New Case: hu (breath vs help)

**Dictionary entries:**
- hu, n. breath; a kind of fruit bearing
- hu, v. to block; to close a hole

**Bible attestations:**
1. **breath (noun)** ~15x
   - "nuntakna hu" = breath of life (Gen 2:7)
   - "a hu tawpna" = gave up the ghost (Gen 25:8)
   - "a hu sang" = gave up the ghost

2. **help (verb)** ~50x
   - "hong hu" = help (Gen 49:25 "who shall help thee")
   - "ka hong hu" = I will help you
   - "hu kei" = do not help

**Current analyzer gloss:** help (verb only)
**Action needed:** Add disambiguation based on context:
- If preceded by "nuntakna" → breath
- If followed by "tawpna/sang" → breath (idiom: give up ghost)
- Otherwise → help

## Verified NOT Needing Disambiguation

### vom (black vs bear)
- Bible: Always "black" when standalone (Gen 30:32-35 - black animals)
- Bear animal uses compound "vompi" (big-black = bear) in 2 Ki 2:24
- Status: ✅ Correct

### zawng (poor/all vs monkey)
- Bible: "poor" in "mizawng" (poor person), "all" in quantifier use
- "monkey" meaning not attested in Bible
- Status: ✅ Correct

### hiam (question vs sharp/weapon)
- Bible: Question particle 4357x
- "sharp/weapon" meaning not attested
- Status: ✅ Correct (Q particle)

### hai (cup vs mango/postpone)
- Bible: "cup" - Pharaoh's cup, silver cup, bowls
- "mango" and "postpone" not clearly attested
- Status: ✅ Correct (cup)

## Lower Priority Candidates

These need more investigation:

### tang (168x)
- Current: embed
- Dictionary: straight (adj) / millet (n)
- Need to verify if "embed" is correct

### mai (309x)
- Current: face
- Dictionary: pumpkin (n) / tear (v)
- "face" seems correct for most uses

### sang (218x)
- Current: high
- Dictionary: high (adj) / younger sibling (n)
- Need to check if sibling meaning attested

## Summary

| Word | Freq | Status | Action |
|------|------|--------|--------|
| hu | 117x | NEEDS WORK | Add breath/help disambiguation |
| vom | 22x | OK | black (bear=vompi) |
| zawng | 47x | OK | poor/all (monkey not attested) |
| hiam | 4357x | OK | Q particle |
| hai | 167x | OK | cup |
| tang | 168x | INVESTIGATE | verify 'embed' |
| mai | 309x | INVESTIGATE | verify 'face' |
| sang | 218x | INVESTIGATE | verify 'high' vs 'sibling' |
