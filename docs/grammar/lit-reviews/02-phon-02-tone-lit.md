# Literature Review: Tone System

## Overview

This report synthesizes previous scholarship on the Tedim Chin tone system, compares tone assignments across sources, and documents the methods and coverage of our tone restoration tool. Tedim Chin has a three-tone system that is lexically contrastive but not marked in practical orthography.

## 1. Henderson (1965)

### 1.1 Three-Tone System

Henderson's informants recognized three tones, labeled "high," "mid," and "low":

> "My informants, however, recognized three possible tones for monosyllables. These were called by VZT 'high', 'mid', and 'low'." [p. 13]

### 1.2 Phonetic Realization

| Tone | Citation Name | Open/Long Syllables | Closed by Stop |
|------|--------------|---------------------|----------------|
| 1 | High | Rising pitch | High level or short high rising |
| 2 | Mid | Level pitch | Level |
| 3 | Low | Falling pitch | Low level or short low falling |

Henderson notes a key generalization:

> "In the great majority of cases short syllables closed by a stop, i.e. those ending in the spelling with '-h, -lh, -k, -t, -p' or '-wh', are pronounced with a low level pitch" [p. 13]

This implies that **checked syllables (those ending in stops) are typically low tone**.

### 1.3 Tone and Verb Stems

Henderson documents tone alternation between verb stem forms:

| Form I (Stem 1) | Form II (Stem 2) | Pattern |
|-----------------|------------------|---------|
| High tone | Low tone | Regular |
| Mid tone | Low tone | Regular |
| Low tone | Low tone | No change (checked syllables) |

Examples:
- *za* (H) 'hear.I' → *zak* (L) 'hear.II'
- *pai* (M) 'go.I' → *pai* (L) 'go.II' (tone change only)
- *thah* (L) 'kill.I' → *thah* (L) 'kill.II' (no change; already checked)

### 1.4 Notation

Henderson uses tone numbers in her phonemic transcription:
- Superscript 1 = High
- Superscript 2 = Mid  
- Superscript 3 = Low

Example: *pa¹* 'male' vs *pa³* 'father'

---

## 2. Zam Ngaih Cing (2017/2018)

### 2.1 Three-Tone Analysis

ZNC confirms the three-tone system and provides diacritics:

| Tone | Diacritic | Example | Gloss |
|------|-----------|---------|-------|
| High | Acute (´) | zá | 'hear' |
| Mid | Macron (¯) | zā | 'medicine' |
| Low | Grave (\`) | zà | 'hundred' |

### 2.2 Tonal Constraints

ZNC documents a constraint on tone sequences:

> "Tedim Chin does not permit the combination of Mid + Low tone. So in places where the Low tone is expected to occur, it is usually replaced by a High tone" [p. 57]

Example: Expected *lisàk → Actual *lisák* 'cause to be tasty'

### 2.3 Stem 1/Stem 2 Tonal Restriction

> "The Stem 1 verbs can carry either High, Mid or Low tones but Stem 2 can have only the High and Low tones" [p. 59]

This matches Henderson's observation that Form II verbs are typically low tone.

### 2.4 Grammatical Tone

ZNC notes tone change marks possession on proper nouns:
- *thāŋpū* 'Thangpu (name)' → *thāŋpú* 'Thangpu's' [p. 60]

---

## 3. Weera (1998)

Weera's paper "Tedim Chin Checked Syllables" focuses on the phonetics and phonology of checked syllables (those ending in glottal stop or voiceless stops).

### 3.1 Four-Way Distinction (including Checked Syllables)

Weera proposes treating checked syllables as a separate category:

| Tone | Label | Phonetic Description |
|------|-------|---------------------|
| 1 | High | Rising, often glottalized |
| 2 | Mid | Level |
| 3 | Low | Falling |
| 4 | Checked (Low) | Short, low level, glottalized final |

Weera argues that "Tone 4" checked syllables are phonetically distinct but may be analyzed as allotones of Tone 3 (Low).

### 3.2 Notation in OCR

Weera uses special markers:
- `word!` = Tone 1 (High)
- `word?` = Tone 2/3 (Mid/Low)
- `word*` = Tone 4 (Checked/Low)

### 3.3 Checked Syllable Examples

From Weera 1998 (extracted via OCR):

| Form | Tone | Gloss |
|------|------|-------|
| kap* | 4/L | 'shoot' |
| gip* | 4/L | 'strong' |
| mit* | 4/L | 'eye' |
| bak* | 4/L | 'full' |
| hak* | 4/L | 'awake' |
| lap* | 4/L | 'wing' |

---

## 4. Singh (2018) - Sukte/Salhte

Singh's grammar of Sukte (closely related to Tedim Chin) provides comparative data.

### 4.1 Three Tones Confirmed

Singh documents the same three-tone system:
- **High** (T¹): "high rising"
- **Mid** (T²): "mid level"
- **Low** (T³): "low falling"

### 4.2 Minimal Pairs

Singh provides clear minimal triplets:
- *za¹* 'hear' / *za²* 'medicine' / *za³* 'hundred'
- *pa¹* 'male' / *pa²* — / *pa³* 'father'

---

## 5. Cross-Source Comparison: Points of Disagreement

Analysis of our tone dictionary reveals systematic disagreements between Henderson (1965) and ZNC (2017/2018) for certain morphemes.

### 5.1 Grammatical Morphemes with Disagreement

| Morpheme | Henderson | ZNC | Analysis |
|----------|-----------|-----|----------|
| *ta* (PFV) | H | L | May reflect Form I/II distinction |
| *thei* (ABIL) | H | L | May reflect Form I/II distinction |
| *sa* (PAST) | H | L | Unclear |
| *lai* (PROSP) | H | L | Unclear |
| *nuam* (DESID) | H | L | Unclear |
| *khin* (IMM) | M | H | Possible transcription difference |
| *pan* (ABL) | M/H | L | Multiple meanings conflated? |
| *tak* (truly) | M | L | Possible dialectal variation |
| *zang* (use) | M | L | Possible dialectal variation |

### 5.2 Analysis of Disagreements

Several patterns emerge:

**1. Form I/II Confusion**

Henderson documents both verb forms explicitly. If ZNC cites only the Form II (low tone) while Henderson cites Form I, this creates apparent disagreement. Examples:
- *ta* 'finish/complete': Henderson H (Form I), ZNC L (Form II?)
- *thei* 'know/able': Henderson H (Form I), ZNC L (Form II?)

**2. Dialectal Variation**

Henderson worked with speakers from Tiddim, Burma. ZNC's data may reflect different dialect communities or more recent pronunciation. Examples where both record the same meaning but different tones suggest genuine dialect differences.

**3. Notation Conventions**

Henderson uses tone numbers while ZNC uses diacritics. Transcription practices may differ:
- Henderson's "mid" may correspond to ZNC's "high" in some cases
- Phonetic realization vs. phonemic analysis

### 5.3 High-Confidence Agreements

Where sources agree, we can be confident about tone:

| Morpheme | Tone | Gloss | Sources |
|----------|------|-------|---------|
| *lo* | L | NEG | Henderson, ZNC |
| *in* | L | ERG | Henderson, ZNC |
| *ah* | L | LOC | Henderson, ZNC |
| *ding* | L | IRR | Henderson, ZNC |
| *khia* | L | DIR.out | Henderson, ZNC |
| *ka* | L | 1SG | Henderson, ZNC |
| *na* | L | 2SG | Henderson, ZNC |
| *a* | L | 3SG | Henderson, ZNC |
| *i* | M | 1PL.INCL | Henderson, ZNC |
| *hong* | L | INV | Henderson, ZNC |
| *kong* | L | 1.OBJ | Henderson, ZNC |

---

## 6. Tone Restoration Tool

### 6.1 Architecture

Our tone restoration system (`scripts/restore_tone.py`) operates in three layers:

1. **Dictionary lookup**: Check `data/tone_dictionary.tsv` for documented tones
2. **Gloss-based disambiguation**: Use morphological analyzer's gloss to resolve ambiguity
3. **Context rules**: Apply positional/syntactic rules for remaining cases

### 6.2 Dictionary Sources

| Source | Entries | Description |
|--------|---------|-------------|
| Henderson 1965 | 529 | Verb Form I/II pairs, grammatical morphemes |
| ZNC 2018 | 79 | Aspect, case, modal markers |
| ZNC via morpheme docs | 45+ | From literature database |
| Weera 1998 | 12 | Checked syllable examples |

**Total: 561 unique morphemes**

### 6.3 Gloss-Based Disambiguation

When multiple tone entries exist for a morpheme, we use the morphological analyzer's gloss to select the correct entry with high confidence:

```
Input: "hi" in sentence-final position
Analyzer: parses as DECL (declarative particle)
Lookup: "hi" has L (DECL) and H (be.I)
Match: DECL → L tone
Result: HIGH confidence
```

This approach leverages the work already done by the morphological analyzer to resolve tone ambiguity.

### 6.4 Confidence Levels

| Level | Meaning | Current Coverage |
|-------|---------|------------------|
| High | Unambiguous OR gloss matched | 75.4% |
| Medium | Multiple entries, no gloss match | 3.5% |
| Low | Morpheme not in dictionary | 21.1% |

### 6.5 Known Limitations

1. **Proper nouns**: Names like *Israel*, *Jerusalem* lack documented tones
2. **Recent loanwords**: Not covered in Henderson or ZNC
3. **Source conflicts**: Where Henderson and ZNC disagree, we typically follow ZNC (more recent)
4. **Sandhi effects**: Tone changes in connected speech not modeled

---

## 7. Open Questions

1. **Dialectal variation**: How much tone variation exists across Tedim Chin speech communities?

2. **Tone sandhi rules**: ZNC documents some; systematic investigation needed.

3. **Historical change**: Do Henderson-ZNC disagreements reflect change over 50 years?

4. **Checked syllable status**: Is Weera's "Tone 4" a separate toneme or allotone of Low?

5. **Grammatical tone**: Beyond possession marking, what other grammatical functions involve tone?

6. **Form I/II correlation**: Is the Form II = Low tone pattern truly exceptionless?

---

## 8. Recommendations

### For the Grammar

1. Present the three-tone system as established fact
2. Note disagreements between sources with specific examples
3. Document the Form I (H/M) → Form II (L) pattern
4. Include a section on tone-orthography mismatch

### For the Dictionary

1. Mark tone on all headwords using diacritics
2. Indicate source of tone information
3. Note when sources disagree

### For the Reader/Interlinear

1. Generate toned text only where confident
2. Leave ambiguous items unmarked rather than guess
3. Indicate confidence level in metadata

---

## References

Henderson, Eugénie J. A. 1965. *Tiddim Chin: A Descriptive Analysis of Two Texts*. London: Oxford University Press.

Weera, [First Name]. 1998. "Tedim Chin Checked Syllables." [Unpublished manuscript or conference paper - need full citation]

Zam Ngaih Cing. 2017. *A Descriptive Grammar of Chin (Tedim): Part 1*. Delhi: Jawaharlal Nehru University PhD dissertation.

Zam Ngaih Cing. 2018. *A Descriptive Grammar of Chin (Tedim): Part 2*. Delhi: Jawaharlal Nehru University PhD dissertation.

Singh, N. Pramodini. 2018. *A Grammar of Sukte*. Delhi: Akansha Publishing House.
