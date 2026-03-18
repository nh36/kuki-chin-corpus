# Tedim Chin Grammar Development Notes

This document tracks ongoing research questions and development tasks for the Tedim Chin morphological analyzer.

---

## 1. Postpositions vs. Case Suffixes

### Investigation Date: 2026-03-18

### Background

During paradigm report generation, we discovered that the comitative marker *tawh* ("with") shows unusual behavior: 7,806 attestations as a standalone word but only 2 as a suffix. This prompted a deeper investigation into the boundary between postpositions and case suffixes in Tedim Chin.

### The *tawh* Question

**Corpus evidence:**
- Standalone `tawh`: 7,806 occurrences
- Suffixed forms: 2 occurrences (both `kitawh`)

**The two `kitawh` cases:**

1. **1 Samuel 14:20** (09014020):
   - Tedim: *"...kitawhnawina lianpi khat na om hi"*
   - KJV: *"...there was a very great discomfiture"*
   - Analysis: `kitawh` here appears to be a verb meaning "to be together" or "to associate" (reciprocal ki- + tawh). The word `kitawhnawina` is a nominalization: "mutual association/togetherness."

2. **1 Kings 6:7** (11006007):
   - Tedim: *"...a kitawhna mun panin a kibawlsa suangte tawh kilam hi"*
   - KJV: *"...built of stone made ready before it was brought thither"*
   - Analysis: `kitawhna` = "joining place" (where things are joined together). Again, verbal use.

3. **Job 28:1** (18028001):
   - Tedim: *"Ngun a kitawh khiatna a khuk om a"*
   - KJV: *"Surely there is a vein for the silver"*
   - Analysis: `a kitawh` = "where it is found/joined" - verbal construction.

**Conclusion:** The two `kitawh` forms are **verbal** (reciprocal ki- + tawh = "be together/join"), NOT nominal case marking. There are **zero** examples of tawh as a nominal case suffix.

### The *pan* Question

**Corpus evidence:**
- Standalone `pan`: 603 occurrences
- `kipan` ("to begin"): 408 occurrences (verbal: ki- + pan)
- `langpan` ("opposing"): 25 occurrences
- `sungpan`: 3 occurrences (as single word)
- `sung pan`: 118 occurrences (as two words)
- `sung panin`: 689 occurrences (spatial + panin)
- `kiang pan`: 60 occurrences (as two words)
- `kiang panin`: 370 occurrences (spatial + panin)

**Key observation:** Unlike `tawh`, `pan` appears both:
1. As a bound suffix on regular nouns (e.g., *Jerusalempan* "from Jerusalem")
2. As part of spatial postposition phrases (e.g., *sung pan* "from inside")

**Pattern comparison:**

| Form | Suffixed | Separate | Ratio |
|------|----------|----------|-------|
| tawh | 0* | 7,806 | 0:7806 |
| pan | ~600 on nouns | ~1,200 on spatials | ~1:2 |

*The 2 `kitawh` are verbal, not nominal suffixes.

### Spatial Postpositions

The spatial terms in Tedim Chin function like **relational nouns** (also called "adpositions" or "postpositions"). They take a genitive-marked possessor and can themselves be case-marked:

**Core spatial nouns:**

| Tedim | Meaning | +LOC (-ah) | +ERG (-in) | +ABL (pan/panin) |
|-------|---------|------------|------------|------------------|
| tung | on/above | tungah (6,072) | tungin (84) | tung panin (280) |
| sung | inside | sungah (3,205) | sungin (?) | sung panin (689) |
| nuai | below | nuaiah | nuaiin (?) | nuai panin (4) |
| mai | face/front | maiah | maiin (?) | mai panin (29) |
| lak | among/middle | lakah (769) | lakin (8) | lak panin (191) |
| kiang | beside | kiangah (4,208) | kiangin (?) | kiang panin (370) |
| lang | side | langah | langin | langpan (25) |

**Usage pattern:**
```
[Possessor-GEN] [Spatial.noun-CASE]
mite'          sungah          = "in (the midst of) people"  
amau'          kiangah         = "beside them"
inn'           tungah          = "on the house"
```

**Why these are postpositions, not case suffixes:**
1. They are independent words that can stand alone
2. They take their own case marking
3. Their possessor is marked with genitive (glottal stop)
4. They have lexical meaning (spatial orientation)

### Revised Analysis

**True Case Suffixes (6):**
1. Absolutive: ∅ (unmarked)
2. Genitive: -' (glottal stop)
3. Ergative: -in
4. Locative: -ah
5. Ablative: -pan
6. Ablative-Ergative: -panin

**Free Postpositions:**
1. **tawh** "with" (comitative) - ALWAYS separate word
   - Attaches to bare noun: *pa tawh* "with father"
   - Can take ergative: *tawhin* (2 attestations)
   - Isaiah 44:15: *mei tawhin moh a em hi* "he bakes bread with fire"
   - Ezekiel 22:21: *mei tawhin...kong haltui ding* "with fire I will melt"
   - The ergative *-in* marks instrumental use: "by means of (being) with"

2. **ding** "for, in order to" (purposive) - 19,257 occurrences
   - Very high frequency - marks purpose/intention
   - *na nei ding* "for you to have" / "you will have"
   - Functions as both postposition and future/irrealis marker

3. **dong** "until" (terminative) - 712 occurrences
   - Marks temporal/spatial endpoint
   - *Gaza ciang dong* "until Gaza"
   - *nitak dong* "until evening"

**Spatial/Relational Nouns (take GEN possessor):**
1. **tung** "on, above" - inn' tungah "on the house"
2. **sung** "inside" - inn' sungah "in the house"
3. **nuai** "below" - inn' nuaiah "below the house"
4. **mai** "face, front" - pa' maiah "in front of father"
5. **lak** "among, middle" - mite' lakah "among the people"
6. **kiang** "beside" - pa' kiangah "beside father"
7. **lang** "side" - langkhat "one side"
8. **pualam** "outside" - pualamah "outside" (62x)

### The *-in* on Postpositions

Both `tawh` and `pan` can take `-in` (ergative):
- `tawhin`: tawh + in (2 attestations - both instrumental "by means of")
- `panin`: pan + in (very common, ~1,500+ with spatials)

This suggests `-in` is a general adverbializer/ergative that can attach to postpositional phrases, not evidence that these are case suffixes.

### Other Postposition Candidates

High-frequency particles that may be postpositions:

| Form | Frequency | Meaning | Notes |
|------|-----------|---------|-------|
| dingin | 4,832 | for (purpose) | ding + in |
| bangin | 4,080 | like (manner) | bang + in |
| hangin | 3,548 | because of | hang + in |
| manin | 3,103 | because | man + in |

These all end in `-in` (ergative/adverbializer), suggesting a pattern:
- Base postposition: ding, bang, hang, man
- Adverbialized form: dingin, bangin, hangin, manin

### Open Questions

1. **Is `pan` a true case suffix or a postposition?**
   - Evidence FOR case suffix: Attaches directly to proper nouns (*Jerusalempan*)
   - Evidence FOR postposition: Often written separately with spatials
   - **Resolution:** `pan` is a **hybrid** - it functions as a bound ablative case on nouns but as a postposition with spatial nouns.

2. **What is the status of `tawhin`?**
   - ✅ RESOLVED: 2 attestations found
   - Both are instrumental: *mei tawhin* "with/by fire"
   - This is `tawh` + `-in` (comitative + ergative = instrumental)

3. **Are there other postpositions?**
   - ✅ Confirmed: `ding` "for/purpose" (19,257x)
   - ✅ Confirmed: `dong` "until" (712x)
   - Likely: `bang` "like", `hang` "because", `man` "reason"

### Recommendations

1. **Keep 6-case system** for nominal paradigms
2. **Add POSTPOSITIONS section** to analyzer documenting:
   - `tawh` as comitative postposition
   - `ding` as purposive postposition
   - `dong` as terminative postposition
   - Spatial nouns as relational postpositions
3. **Document the spatial nouns** as a separate word class that:
   - Takes genitive possessor
   - Can be case-marked itself
4. **Investigate** bang/hang/man as potential postpositions

---

## 2. TODO: Ghost Word Audit

### Status: Not yet started

### Known Ghost Words

Words in the dictionary with zero attestations in the corpus:

**From noun stems:**
- `ke` - "foot" (only appears as `ke'n` = 1SG-ERG "I")
- `sialh` - "tomorrow" (Tedim uses `zing` instead)
- `kent` - unknown (no attestations)
- `lute` - unknown (no attestations)
- `ninikikhol` - unknown (no attestations)
- `dawtna` - "beloved" (potentially a ghost - needs verification)

**From compound nouns (unattested as standalone):**
- lungmit, lungthim, mikhual, ngalpi, paazu, sihinn, tuibang, vanmi

### Tasks

1. Run systematic search for all dictionary entries with zero corpus hits
2. Determine if ghosts are:
   - Errors (never existed)
   - Dialectal variants (exist in other Kuki-Chin varieties)
   - Archaic forms (no longer in use)
   - Orthographic variants (spelled differently in corpus)
3. Flag confirmed ghosts in dictionary rather than deleting
4. Document findings in this file

---

## 3. TODO: Compound Attestation Deep Dive

### Status: Not yet started

### Issue

The compound paradigm report shows 17 compounds that only appear inside larger compounds (not as standalone words). For example:
- `gahzu` (sap) only appears in `leenggahzu` (wine = grape-sap)

### Questions

1. Should these be listed as compounds at all, or as bound morphemes?
2. Are there other cases where a "compound" is really a bound stem?
3. How should the paradigm extraction handle nested compounds?

### Known Cases

Compounds only found inside larger compounds:
- `gahzu` in `leenggahzu`
- (need to extract complete list from report)

### Tasks

1. Extract complete list of compounds with 0 standalone attestations
2. For each, determine what larger compound(s) contain it
3. Decide on classification: true compound vs. bound stem
4. Update NOUN_STEM_TYPES accordingly

---

## 4. Research Log

### 2026-03-18
- Discovered comitative `-tawh` is a free postposition, not a case suffix
- Reduced case system from 8 to 6 cases
- Created POSTPOSITIONS dict in analyzer
- Marked `ke` and `sialh` as ghost words
- Identified spatial nouns as relational postpositions
- Created this document

---

## References

- Bible corpus: bibles/extracted/ctd/ctd-x-bible.txt (831,431 tokens)
- Analyzer: scripts/analyze_morphemes.py
- Paradigm generator: scripts/generate_paradigm.py
- Paradigm reports: docs/paradigms/
