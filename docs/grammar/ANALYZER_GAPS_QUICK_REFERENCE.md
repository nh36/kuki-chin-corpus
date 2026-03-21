# Analyzer vs Literature Gaps - Quick Reference

## At-a-Glance Comparison

| # | Gap | Category | Severity | Analyzer Gloss | Literature Distinction | Recoverable? | Fix Effort |
|---|---|---|---|---|---|---|---|
| 1 | Causative-Benefactive | Derivational (-sak) | 🔴 CRITICAL | `CAUS` (all) | Form I=CAUS, Form II=BENF | ✓ YES | 🟡 EASY |
| 2 | Tone in -a case marker | Case | 🔴 CRITICAL | `LOC` (all) | -á=GEN, -à=INSTR/LOC | ✗ NO | ⚠️ BLOCKED |
| 3 | Missing -suk, -phei | Directionals | 🔴 CRITICAL | absent | 3-way elevation system | ✓ YES | 🟢 TRIVIAL |
| 4 | Inverse marking constraints | Prefix (hong-) | 🔴 CRITICAL | `3→1` (unmarked) | Obligatory w/ 1/2 person causee | ✓ YES | 🟡 EASY |
| 5 | Agreement vs Possession | Prefix (ka-, na-, a-) | 🟠 MAJOR | unmarked | Context-dependent function | ✓ YES | 🟢 EASY |
| 6 | Habitual system incompleteness | Aspect | 🟠 MAJOR | -kik only | 4-way (ngei, gige, zel, kik) | ✓ YES | 🟡 MEDIUM |
| 7 | Form-dependent allomorphy | Modal (-thei/-theih) | 🟠 MAJOR | -thei=`ABIL`, -theih=`ABIL` | Form I→-thei, Form II→-theih | ✓ YES | 🟢 EASY |
| 8 | -pih Form II requirement | Derivational | 🟠 MAJOR | unmarked | Strict Form II only | ✓ YES | 🟢 EASY |
| 9 | Undifferentiated desideratives | Modal (-nuam, -nop) | 🟡 MINOR | both `want` | Different frequency + patterns | ~ PARTIAL | 🟡 RESEARCH |
| 10 | NEG.ABIL variants | Modal (-pah, -pak, -lawh) | 🟡 MINOR | all `NEG.ABIL` | Conditioning unknown | ✗ NO | ⚠️ RESEARCH |
| 11 | Directional classifications | Post-verbal | 🟡 MINOR | some questionable | -khia, -cip, -tang, -sawn status | ~ VERIFY | 🟡 VERIFY |
| 12 | Non-standard glosses | Terminology | 🟡 MINOR | `IMM`, `perhaps`, `must` | Should be `COMPL`, `DUB`, `DEON` | ✓ YES | 🟢 COSMETIC |

---

## Phase 1: Critical Fixes (Do First)

✦ **#1: -sak dual-glossing**
```
RULE: If verb form is Form I → gloss as CAUS
      If verb form is Form II → gloss as BENF
EXAMPLE: puk-sak 
  → Check verb dictionary for "puk"
  → If Form I: "fall-CAUS" (make fall)
  → If Form II: "fall-BENF" (fall for someone)
```

✦ **#3: Add -suk, -phei**
```
ADDITIONS:
'suk': 'DOWN'  (downward motion)
'phei': 'HORIZ'  (horizontal/level motion)
SYSTEM: -toh (UP), -suk (DOWN), -phei (HORIZ) = elevation system
```

✦ **#4: Inverse marking with -sak**
```
RULE: When -sak present AND causee/beneficiary is 1st or 2nd person,
      hong- MUST appear
EXAMPLES:
  ✓ "nu hau in kei hong-an huan-sak" (aunt Hau made me cook)
    → hong- REQUIRED because causee is 1SG (kei)
  ✓ "ken Lian niangtui bawl-sak" (I made tea for Lian)
    → no hong- because beneficiary is 3rd person
```

✦ **#5: Agreement vs Possession**
```
RULE: ka-, na-, a- function differently:
  If following word is NOUN → POSSESSIVE ("my", "your", "his")
  If following word is VERB → AGREEMENT (subject concord)
EXAMPLES:
  "ka inn" (1SG-house) → Possessive: "my house"
  "ka pai" (1SG-go) → Agreement: "I go"
```

---

## Phase 2: Major Improvements

⚡ **#6: Habitual system (4-way)**
```
Literature: ZNC §5.6.4 documents four-way distinction
- ngei "before but not now" (HAB.PST)
- gige "always" (HAB)
- zel "continue from before" (CONT.HAB)
- kik "again" (ITER)

ACTION: Add inventory entries; connect to existing -kik
```

⚡ **#7: Form-dependent -thei/-theih**
```
RULE: Form I verb → -thei
      Form II verb → -theih (with allomorphic vowel change)
EXAMPLES:
  tu-thei "sit-ABIL" (Form I: ability to sit)
  tut-theih "sit-ABIL" (Form II: ready to sit)
```

⚡ **#8: -pih Form II strict requirement**
```
RULE: -pih ONLY attaches to Stem II (Form II) verbs
      Form I attachment is UNGRAMMATICAL
EXAMPLES:
  ✓ tut-pih (sit.II-COM) "sit together"
  ✗ *tu-pih (sit.I-COM) [ungrammatical]
ACTION: Add constraint; check for violations in corpus
```

---

## Phase 3: Polish (Nice-to-have)

🔧 **#11: Verify directional classifications**
- -khia: Listed as "out" but ZNC shows as verb "drop"
- -cip: Listed as "down" but ZNC shows as adjective "hard"
- -tang: Listed as "arrive" but unclear status
- -sawn: Listed as "toward" but unclear status

ACTION: Need corpus examples or literature confirmation

---

## Blocked Issues (Cannot Fix)

❌ **#2: Tone distinction in -a**
```
ISSUE: -á (HIGH) = GENITIVE vs -à (LOW) = INSTR/LOC
PROBLEM: Analyzer doesn't preserve tone in Bible corpus
PREREQUISITE: Corpus retokenization with tone marks
STATUS: Blocked until tone restoration available
```

❌ **#10: -pah/-pak/-lawh conditioning**
```
ISSUE: Three NEG.ABIL forms; conditioning unknown
PROBLEM: Literature doesn't explain distinction
STATUS: Requires linguistic investigation
```

---

## Key Source References

| Source | Topic | Key Pages |
|---|---|---|
| ZNC (2018) Part 1 §3.3 | Prefixes + case system | 108-114 |
| ZNC (2018) Part 2 §5.6-5.8 | Aspect + modal + derivational | 147-164 |
| Otsuka (2009) | Causative-benefactive | 9-20 |
| Otsuka (2024) | Applicative constraints | 43-63 |
| Henderson (1965) | Concord system | 32-33 |

---

## Implementation Checklist

- [ ] Implement -sak dual-glossing (CAUS/BENF)
- [ ] Add missing -suk, -phei to inventory
- [ ] Document inverse marking rules for hong-
- [ ] Mark prefix agreement vs possession contexts
- [ ] Add ngei, gige, zel to habitual system
- [ ] Implement -thei/-theih Form-dependent glossing
- [ ] Add -pih Form II requirement constraint
- [ ] Verify/correct directional classifications
- [ ] Standardize non-standard glosses
- [ ] Extract remaining literature (Henderson directionals, etc.)

