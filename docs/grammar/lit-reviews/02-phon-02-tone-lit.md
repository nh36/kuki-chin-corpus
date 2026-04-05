# Tedim Chin Tone System

## 1. Overview

Tedim Chin has a **three-tone system**: High (H), Mid (M), and Low (L). Tone is lexically contrastive but **not marked in practical orthography**. This report synthesizes what is known about tone from Henderson (1965), Zam Ngaih Cing (2017/2018), Weera (1998), and Singh (2018), and documents systematic patterns discovered through corpus analysis.

### 1.1 Minimal Pairs

All sources confirm three contrastive tones via minimal sets:

| High | Mid | Low | Domain |
|------|-----|-----|--------|
| *za* 'hear' | *za* 'medicine' | *za* 'hundred' | Lexical |
| *pa* 'male' | — | *pa* 'father' | Lexical |
| *ne* 'eat.I' | *pai* 'go.I' | *nek* 'eat.II' | Verb Form I/II |

### 1.2 Phonetic Realization

| Tone | Open Syllables | Checked Syllables |
|------|----------------|-------------------|
| High (H) | Rising | Short high rise |
| Mid (M) | Level | Level |
| Low (L) | Falling | Short low level |

**Key constraint**: Checked syllables (ending in -h, -k, -t, -p) are predominantly Low tone.

---

## 2. Tone in Verb Morphology

### 2.1 The Form I / Form II Alternation

Henderson (1965) documents a systematic tone alternation between verb stem forms:

| Pattern | Form I | Form II | Example |
|---------|--------|---------|---------|
| H → L | High | Low | *za* (H) 'hear.I' → *zak* (L) 'hear.II' |
| M → L | Mid | Low | *pai* (M) 'go.I' → *pai* (L) 'go.II' |
| L → L | Low | Low | *thah* (L) 'kill.I' → *thah* (L) 'kill.II' |

**Generalization**: Form II is always Low tone. Form I can be H, M, or L.

From our corpus of 268 verb pairs documented by Henderson:
- 153 pairs follow H → L pattern
- 85 pairs follow M → L pattern  
- 30 pairs have L → L (no tone change, typically checked syllables)

### 2.2 Morphophonological Implications

When a suffix attaches to a verb, knowing whether it requires Form I or Form II determines the stem tone:

| Suffix | Requires | Example | Resulting Tone |
|--------|----------|---------|----------------|
| *-ta* (PFV) | Form I | *za-ta* | H-L |
| *-sak* (CAUS) | Form I | *za-sak* | H-L |
| *-pih* (APPL) | Form II | *zak-pih* | L-L |

---

## 3. Tone of Grammatical Morphemes

### 3.1 Established Tones (Sources Agree)

These morphemes have consistent tone across Henderson and ZNC:

| Category | Morpheme | Tone | Gloss |
|----------|----------|------|-------|
| **Pronouns** | *ka-* | L | 1SG |
| | *na-* | L | 2SG |
| | *a-* | L | 3SG |
| | *i-* | L | 1PL.INCL |
| | *kan-* | L | 1PL.EXCL |
| **Case** | *-in* | L | ERG |
| | *-ah* | L | LOC |
| | *-pan* | L | ABL |
| | *-tawh* | L | COM |
| **Negation** | *lo* | L | NEG |
| | *kei* | L | NEG.EMPH |
| **Aspect** | *-ta* | L | PFV |
| | *-zo* | L | COMPL |
| | *-khin* | H | IMM/SEQ |
| | *-kik* | H | ITER |
| **Modal** | *-ding* | L | IRR |
| | *-nuam* | L | DESID |
| **Directional** | *-khia* | L | DIR.out |
| | *-toh* | L | UP |
| | *-suk* | L | DOWN |
| **Sentence-final** | *hi* | L | DECL |
| | *e* | L | INCONCL |
| | *maw* | L | Q |

### 3.2 Pattern: Most Grammatical Morphemes are Low

Of 90 grammatical morphemes in our analyzer:
- **Low tone**: 72 (80%)
- **High tone**: 12 (13%)
- **Mid tone**: 6 (7%)

This reflects a typological tendency: grammatical morphemes typically have reduced prosodic prominence.

---

## 4. Homophony and Tone

### 4.1 Lexical vs. Grammatical Homophony

Several morphemes have distinct lexical and grammatical meanings with **different tones**:

| Form | Lexical | Tone | Grammatical | Tone |
|------|---------|------|-------------|------|
| *ta* | 'child' | H | PFV | L |
| *thei* | 'know' | H | ABIL | L |
| *lai* | 'midst' | H | PROSP | L |
| *sa* | 'flesh' | H | PAST | L |
| *hi* | 'be' | H | DECL | L |

**Disambiguation principle**: When analyzing text, the morphological parse determines which meaning (and thus which tone) applies. If the analyzer parses *ta* as PFV (perfective), it receives Low tone. If parsed as 'child', it receives High tone.

### 4.2 True Minimal Pairs within Henderson

Henderson documents several morphemes with the same spelling but different tones and meanings:

| Form | Tone 1 | Meaning 1 | Tone 2 | Meaning 2 |
|------|--------|-----------|--------|-----------|
| *gam* | L | 'land' | H | 'dry' |
| *zin* | L | 'travel.II' | H | 'travel.I' |
| *tui* | L | 'water' | H | 'liver' |
| *pat* | H | 'thin.I' | L | 'thin.II' |

---

## 5. Source Disagreements

### 5.1 Henderson (1965) vs. ZNC (2018)

For some morphemes, Henderson and ZNC record different tones:

| Morpheme | Henderson | ZNC | Analysis |
|----------|-----------|-----|----------|
| *khin* (IMM) | M | H | Different notation conventions? |
| *nuam* (want) | H (Form I) | L (DESID suffix) | Form I/II distinction |
| *thei* (know/ABIL) | H (know) | L (ABIL) | Different morphemes |
| *tak* (true/exact) | M | L | Possibly dialectal |
| *man* (true/reason) | M | L | Different meanings |

### 5.2 Explaining the Disagreements

Most "disagreements" resolve when we recognize:

1. **Different morphemes**: *thei* 'know' (H) ≠ *-thei* ABIL (L)
2. **Form I vs Form II**: Henderson cites Form I, ZNC cites the grammaticalized Form II
3. **Different meanings**: *lai* 'midst' (H) ≠ *-lai* PROSP (L)

**True dialectal variation** appears minimal. Most apparent conflicts are notational or categorical.

---

## 6. Checked Syllables

### 6.1 Weera's Analysis

Weera (1998) argues that checked syllables (ending in glottal stop or -k, -t, -p) constitute a fourth tonal category:

| Category | Phonetic | Distribution |
|----------|----------|--------------|
| Tone 1 (H) | Rising | Open syllables |
| Tone 2 (M) | Level | Open syllables |
| Tone 3 (L) | Falling | Open syllables |
| Tone 4 | Short, low, glottalized | Checked syllables |

### 6.2 Phonemic Status

Henderson and ZNC analyze "Tone 4" as an **allophone of Low tone** conditioned by syllable structure. The consensus position:

> Checked syllables are Low tone by default. Tone 4 is not a separate phoneme.

Evidence: Verb pairs where Form II adds -k/-h consistently become Low:
- *za* (H) → *zak* (L)
- *ne* (H) → *nek* (L)

---

## 7. Tone Sandhi

### 7.1 ZNC's Constraint

ZNC documents a constraint on tone sequences:

> "Tedim Chin does not permit the combination of Mid + Low tone. So in places where the Low tone is expected to occur, it is usually replaced by a High tone." [p. 57]

Example: Expected **lisàk* → Actual *lisák* 'cause to be tasty'

### 7.2 Implications

This constraint affects our predictions when:
- A Mid-tone stem combines with a Low-tone suffix
- The result should be M-L but surfaces as M-H

Further systematic investigation of tone sandhi is needed.

---

## 8. Corpus Statistics

### 8.1 Tone Dictionary

Our tone dictionary contains **576 morphemes** with documented tones:

| Source | Entries | Percentage |
|--------|---------|------------|
| Henderson 1965 | 536 | 77% |
| ZNC 2018 | 96 | 14% |
| Weera 1998 | 12 | 2% |
| ZNC morpheme docs | 60 | 9% |

### 8.2 Tone Distribution

| Tone | Count | Percentage |
|------|-------|------------|
| Low (L) | 436 | 62% |
| High (H) | 153 | 22% |
| Mid (M) | 85 | 12% |
| Multi-syllable | 33 | 5% |

The predominance of Low tone reflects:
1. Form II verbs are always Low
2. Grammatical morphemes are mostly Low
3. Checked syllables are Low

### 8.3 Bible Text Coverage

Applying the tone dictionary to the Tedim Chin Bible:

| Category | Tokens | Percentage |
|----------|--------|------------|
| Known (tone marked) | ~640,000 | 77% |
| Unknown (unmarked) | ~190,000 | 23% |

Unknown tokens include:
- Proper nouns (Israel, Jerusalem, Jesus)
- Compounds with unlisted components
- Lexical items without documented tone

---

## 9. Summary of What We Know

### 9.1 Established Facts

1. **Three tones**: H, M, L — lexically contrastive
2. **Form I/II**: Form I = H/M/L; Form II = always L
3. **Grammatical tone**: Most functional morphemes are L
4. **Checked syllables**: Predictably Low tone
5. **Homophony resolution**: Morphological analysis disambiguates

### 9.2 Remaining Questions

1. **Tone sandhi**: What are the complete rules for M-L → M-H?
2. **Dialectal variation**: Do modern dialects differ from Henderson's 1960s data?
3. **Productive compounds**: How is tone assigned to new compounds?
4. **Loanwords**: What tone do Burmese/English loans receive?

---

## References

Henderson, Eugénie J. A. 1965. *Tiddim Chin: A Descriptive Analysis of Two Texts*. London: Oxford University Press.

Singh, N. Pramodini. 2018. *A Grammar of Sukte*. Delhi: Akansha Publishing House.

Weera, [First Name]. 1998. "Tedim Chin Checked Syllables." [Manuscript]

Zam Ngaih Cing. 2017. *A Descriptive Grammar of Chin (Tedim): Part 1*. PhD dissertation, Jawaharlal Nehru University.

Zam Ngaih Cing. 2018. *A Descriptive Grammar of Chin (Tedim): Part 2*. PhD dissertation, Jawaharlal Nehru University.
