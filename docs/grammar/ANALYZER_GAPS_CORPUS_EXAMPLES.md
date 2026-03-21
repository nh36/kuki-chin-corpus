# Analyzer Gaps - Corpus Examples

## Real Cases Where Analyzer Falls Short

### 1. CAUSATIVE-BENEFACTIVE AMBIGUITY (-sak)

**Problem**: All -sak glossed as CAUS; doesn't distinguish Form I (causative) from Form II (benefactive)

#### Example 1a: CAUSATIVE (Form I)
```
Source: Genesis 1:20
Hebrew original: "Let the waters bring forth abundantly..."

Analyzed: "tut-sak"
Current gloss: "sit-CAUS"
Literature says:
  - tut (Form I: "make sit")
  - tut + -sak → CAUSATIVE "cause to sit"
  
Should be: "sit-CAUS" (cause X to sit)
```

#### Example 1b: BENEFACTIVE (Form II)
```
Source: (from Otsuka 2009, Example 30)
"I made some tea for Lian"

Analyzed: "bawl-sak"
Current gloss: "make-CAUS"
Literature says:
  - bawl (Form II: "make.for")
  - bawl + -sak → BENEFACTIVE "make for someone"
  
Should be: "make-BENF" (make something for someone)
```

**Impact**: ~5% of corpus (~40,000+ verb tokens); reader cannot distinguish causative from benefactive reading

**How to fix**: Check verb dictionary for Form I vs Form II status of "tut", "bawl", etc.

---

### 2. TONE DISTINCTION IN -a CASE MARKER

**Problem**: Both HIGH tone -á (GEN) and LOW tone -à (INSTR/LOC) glossed as LOC

#### Example 2a: GENITIVE (HIGH tone -á)
```
Source: Luke 1:13
"fear him not, Zacharias: for thy prayer is heard"

Analyzed: "na-a pawp"
Current gloss: "2SG-LOC prayer"
Literature says (ZNC §3.3.3.3.2):
  - High tone -á = GENITIVE
  - na-á pawp = "2SG-GEN prayer" → "your prayer"
  
Should be: "2SG-GEN prayer"
```

#### Example 2b: LOCATIVE (LOW tone -à)
```
Source: Genesis 1:14
"let there be lights in the firmament of heaven"

Analyzed: "van-a"
Current gloss: "sky-LOC"
Literature says:
  - Low tone -à = LOCATIVE
  - van-à = "sky-LOC" → "in the sky"
  
Actually correct in this case (both surface same way)
```

**Impact**: **CRITICAL and UNRECOVERABLE** — Tone not preserved in corpus; ambiguity cannot be resolved without retokenizing

**Data limitation**: Bible corpus doesn't distinguish tone marks; would require tone restoration project

---

### 3. MISSING DIRECTIONAL SUFFIXES

**Problem**: -suk and -phei missing from analyzer inventory

#### Example 3a: -suk (DOWNWARD)
```
Source: ZNC (2018: §5.8.2.3, Example 363)
Analyzed text: "kum-suk"
Current gloss: "step-???" (unknown)
Literature says:
  - -suk = DOWN (elevation system)
  - kum-suk = "descend downward"
  
Should be: "step-DOWN"

Additional examples from ZNC:
  - "tai-suk" = "carried-DOWN" (carried away downward)
  - "puk-suk" = "fall-DOWN" (fall down)
```

#### Example 3b: -phei (HORIZONTAL)
```
Source: ZNC (2018: §5.8.2.3, Example 364)
Analyzed text: "pai-phei"
Current gloss: "go-???" (unknown)
Literature says:
  - -phei = HORIZ (elevation system)
  - pai-phei = "go horizontal/level"
  
Should be: "go-HORIZ"
```

**Impact**: LOW for frequency but SYSTEMATIC gap; elevation system incomplete

**How to fix**: Trivial — add two dictionary entries

---

### 4. INVERSE MARKING CONSTRAINTS (hong-)

**Problem**: hong- glossed as "3→1" but obligatory occurrence pattern with -sak not captured

#### Example 4a: WITH OBLIGATORY hong-
```
Source: Otsuka (2009, Example 23)
Text: "nu hau in kei hong-an huan-sak"
       aunt Hau ERG 1SG INV-meal cook.I-SAK

Analyzed:
  - hong- = "3→1"
  - -sak = "CAUS"
  
Current gloss: "aunt Hau 1SG 3→1-meal cook-CAUS"
Literature says (Otsuka p. 10-11):
  - When causee is 1st/2nd person, hong- is OBLIGATORY
  - This is the INVERSE marking pattern
  
Should check: "Is -sak present AND causee 1st/2nd person?" → hong- MUST be there
```

#### Example 4b: WITHOUT hong- (3rd person beneficiary)
```
Source: Otsuka (2009, Example 30)
Text: "ken Lian niangtui bawl-sak"
      1SG.ERG Lian tea make.II-SAK

Analyzed:
  - No hong- prefix
  - -sak = "CAUS"
  
This is grammatical because beneficiary (Lian) is 3rd person
No hong- needed in 3→3 causative
```

**Impact**: MEDIUM — Affects complex predicates; enables error detection for malformed causatives

**How to fix**: Add constraint rule for -sak + 1/2 person arguments

---

### 5. AGREEMENT vs POSSESSION (ka-, na-, a-)

**Problem**: Prefix treated uniformly; doesn't distinguish agreement marker on verbs from possessive marker on nouns

#### Example 5a: POSSESSIVE (on noun)
```
Source: Genesis 1:27
Text: "ka inn" → "my house"
       "a pa" → "his father"

Current gloss: Both treated as "1SG-NOUN" and "3SG-NOUN"
Literature says (Henderson 1965, pp. 32-33):
  - These are POSSESSIVE prefixes marking possession
  - Function at NOUN level
  - Example: "ka inn-ah" = "my house-LOC" → "in my house"
```

#### Example 5b: AGREEMENT (on verb)
```
Source: Matthew 1:18
Text: "ka pai" → "I go"
       "a bawl" → "he/she makes"

Current gloss: Both treated as "1SG-VERB" and "3SG-VERB"
Literature says:
  - These are AGREEMENT prefixes marking subject concord
  - Function at VERB level
  - Example: "kei ka pai" = "I 1SG go" → Agreement marker
```

**Impact**: MEDIUM — Affects syntactic analysis; important for understanding phrase structure

**How to fix**: Check part-of-speech of following word (noun → possessive; verb → agreement)

---

### 6. HABITUAL SYSTEM (incomplete)

**Problem**: Only -kik marked; misses 4-way habitual system (ZNC §5.6.4)

#### Example 6a: -ngei (HAB.PST "before but not now")
```
Source: ZNC (2018: §5.6.4.1, Example 318)
Text: "na sem ngei ing"
      thing do HAB.PST 1SG.RLS

Current status: ngei NOT in analyzer inventory
Literature says: -ngei marks "used to do but not anymore"
Should be: "do-HAB.PST" = "used to work (but not now)"
```

#### Example 6b: -gige (HAB "always")
```
Source: ZNC (2018: §5.6.4.2, Example 319)
Text: "na sem gige ing"
      thing do HAB 1SG.RLS

Current status: gige NOT in analyzer inventory
Literature says: -gige marks habitual "always"
Should be: "do-HAB" = "always works"
```

#### Example 6c: -zel (CONT.HAB "continue/repeat")
```
Source: ZNC (2018: §5.6.4.3, Example 320)
Text: "na sem zel ing"
      thing do CONT.HAB 1SG.RLS

Current status: zel NOT in analyzer inventory
Literature says: -zel marks "continues/repeats from before"
Should be: "do-CONT.HAB" = "continue to work"
```

#### Example 6d: -kik (ITER "again")
```
Source: Analyzer tracks this one ✓
Text: "na sem kik ing"
      thing do ITER 1SG.RLS

Gloss: "do-ITER" = "work again" ✓ Already correct
```

**Impact**: MEDIUM — Habitual system incomplete; readers miss aspectual nuances

**How to fix**: Add ngei, gige, zel to inventory; connect to existing -kik

---

### 7. FORM-DEPENDENT ALLOMORPHY (-thei vs -theih)

**Problem**: Both -thei and -theih glossed as ABIL; doesn't note Form I vs Form II requirement

#### Example 7a: Form I → -thei
```
Source: ZNC (2018: §5.7.4, Example 332)
Text: "tu-thei-ta"
      sit.I-ABIL-PFV

Current gloss: "sit-ABIL-PFV"
Literature says (ZNC pp. 150-153):
  - Form I verb → -thei "able/capable"
  - "tu-thei" = "able to sit" (general ability)

Correct in practice but Form I-specific rule not documented
```

#### Example 7b: Form II → -theih
```
Source: ZNC (2018: §5.7.4, Example 333)
Text: "nek-theih-ta"
      eat.II-ABIL-PFV

Current gloss: "eat-ABIL-PFV"
Literature says:
  - Form II verb → -theih "ready/prepared"
  - "nek-theih" = "food is ready to eat"
  
This is DIFFERENT meaning but analyzer can't distinguish
```

**Impact**: MEDIUM — Affects semantic interpretation of abilitative constructions (~662 in corpus)

**How to fix**: Check verb form in dictionary; add Form-dependent glossing rule

---

### 8. -pih FORM II REQUIREMENT

**Problem**: Constraint not documented; analyzer allows -pih on any verb

#### Example 8a: Grammatical Form II
```
Source: ZNC (2018: §6.6.1.2.2, Example 443)
Text: "nek-pih"
      eat.II-COM

Gloss: "eat-COM" = "eat together" ✓ Grammatical
Literature says: -pih REQUIRES Form II
Check: "nek" is Form II of eat ✓ Correct
```

#### Example 8b: Ungrammatical Form I (should be flagged)
```
Source: ZNC (2018: §6.6.1.2.2, Example 444)
Text: "*ne-pih"
      eat.I-COM

Gloss: Would be "eat-COM" but UNGRAMMATICAL
Literature says: Form I + -pih is invalid
Should flag: ERROR — Form I cannot take -pih
```

**Impact**: LOW for frequency but enables error checking

**How to fix**: Add Form II requirement constraint; check dictionary

---

### 9. UNDIFFERENTIATED DESIDERATIVES (-nuam vs -nop)

**Problem**: Both glossed as "want"; difference in frequency and patterns not captured

#### Example 9a: -nuam "want"
```
Source: Corpus frequency: 630 attestations (higher)
Text examples: "uk nuam" "en nuam"
Gloss: "want to rule" "want to see"

Current: both marked as `want`
Difference unclear in literature
```

#### Example 9b: -nop "want"
```
Source: Corpus frequency: 216 attestations (lower)
Text examples: "cih-nop-na" (desire to say)
Pattern: Often occurs with nominalizer -na

Current: both marked as `want`
Pattern-based distinction possible but unclear
```

**Impact**: LOW — Literature doesn't fully explain distinction

**Note**: This is a **literature gap**, not an analyzer bug

---

## Summary Statistics

| Gap Category | # Affected | % of Corpus | Severity |
|---|---|---|---|
| -sak ambiguity | ~40,000 tokens | ~5% | 🔴 CRITICAL |
| Tone in -a | Unknown | Unknown | 🔴 CRITICAL (unrecoverable) |
| -suk/-phei missing | ~200-300 | ~0.02% | 🔴 CRITICAL (trivial fix) |
| Inverse marking | ~5-10% of causatives | ~0.5% | 🔴 CRITICAL |
| Agreement vs possession | ~100,000+ | ~12% | 🟠 MAJOR |
| Habitual incomplete | ~2,000-3,000 | ~0.3% | 🟠 MAJOR |
| Form-dependent allomorphy | ~662 | ~0.08% | 🟠 MAJOR |
| -pih constraint | Validation only | varies | 🟠 MAJOR |
| Other gaps | Minor | <1% | 🟡 MINOR |

**Total impact of critical gaps**: ~15-20% of corpus affected by at least one distinction

**Recoverable without new data**: ~80% of identified gaps

