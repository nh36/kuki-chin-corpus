# Tedim Chin Skeleton Grammar: Development Plan

## Objective

Create a descriptive grammar of Tedim Chin morphology based on the morphological
analyzer, illustrated with example sentences from narrative portions of the Bible.

## Phase 1: Document Analyzer Categories (Current Task)

### 1.1 Inventory from Analyzer

Extract all morphological categories currently in the analyzer:

#### A. Pronominal System
- **Pronominal prefixes**: ka- (1SG), na- (2SG), a- (3SG), i- (1PL.INCL), ei- (1PL.EXCL)
- **Object prefixes**: kong- (3→1), hong- (3→1/2)
- **Independent pronouns**: kei, nang, amah, eite, note, etc.
- **Emphatic pronouns**: keimah, nangmah (with -mah suffix)

#### B. Nominal System
- **Case markers**: -in (ERG), -ah (LOC), -tawh (COM), -pan (ABL)
- **Number**: -te (PL), khat (one), nih (two), etc.
- **Possession**: ka- (1SG.POSS), -' (POSS marker on nouns)
- **Demonstratives**: hih (PROX), tua (DIST), kha (DIST.far)
- **Nominalizers**: -na (NMLZ), -pa (AG.NMLZ), -mi (AG.NMLZ)

#### C. Verbal System

##### C.1 Stem Alternation (Form I / Form II)
47 pairs documented: mu/muh (see), nei/neih (have), za/zak (hear), etc.

##### C.2 Derivational Suffixes
- **Causative**: -sak (CAUS)
- **Applicative**: -pih (APPL)
- **Directional**: -khia (out), -lut (in), -to (up), -khiat (away)
- **Reversive**: -kik (ITER/again)
- **Ability**: -theih (ABIL)
- **Intensive**: -gawp (INTENS)

##### C.3 TAM Suffixes
- **Irrealis**: -ding (IRR)
- **Completive**: -zo (COMPL), -khit (COMPL), -mang (COMPL)
- **Perfective**: -ta (PFV), -sa (PERF)
- **Immediate**: -khin (IMM)
- **Continuative**: -lai (CONT), -to (CONT)

##### C.4 Negation
- **Simple**: lo (NEG)
- **Emphatic**: kei (NEG.EMPH)

#### D. Sentence-Level
- **Declarative**: hi (DECL)
- **Interrogative**: hiam (Q)
- **Topicalizer**: pen (TOP)

### 1.2 Structure of Each Grammar Section

For each morpheme/category:

```
## 3.2.1 The Causative Suffix -sak

### Form
The causative suffix -sak attaches to verb stems to derive causative verbs.

### Distribution
Follows the verb stem and precedes inflectional suffixes:
  V-sak-INFL
  
### Gloss
CAUS (causative)

### Examples

(1) Gen 1:3 - God causes light to exist
    Pasian in "Khuavak a om hen" a ci a, khuavak a om hi.
    pasian  in   khuavak  a-om       hen  a-ci   a   khuavak  a-om    hi
    God     ERG  light    3SG-exist  let  3SG-say and light   3SG-exist DECL
    'God said "Let there be light," and there was light.'

(2) Gen 2:21 - God causes deep sleep
    Topa Pasian in a ihmut nak suak sak a...
    topa  pasian  in   a-ihmut.nak-suak-sak          a
    Lord  God     ERG  3SG-deep.sleep-become-CAUS    and
    'The Lord God caused a deep sleep to fall...'
    
### Frequency
-sak appears X times in corpus.

### Notes
Compare with -pih (applicative) and -huai (another causative).
```

## Phase 2: Organize Into Grammar Chapters

### Proposed Structure

```
1. Introduction
   1.1 The Tedim Chin Language
   1.2 Previous Studies
   1.3 The Present Work
   1.4 Corpus and Methodology

2. Phonology (brief)
   2.1 Phoneme Inventory
   2.2 Syllable Structure
   2.3 Tone (limited)

3. Nominal Morphology
   3.1 Noun Stems
   3.2 Case Markers
       3.2.1 Ergative -in
       3.2.2 Locative -ah
       3.2.3 Comitative -tawh
       3.2.4 Ablative -pan(in)
   3.3 Number
       3.3.1 Plural -te
       3.3.2 Numerals
   3.4 Possession
       3.4.1 Pronominal Possessive Prefixes
       3.4.2 Possessive Suffix -'
   3.5 Demonstratives and Determiners

4. Pronominal System
   4.1 Independent Pronouns
   4.2 Pronominal Prefixes
   4.3 Object Prefixes
   4.4 Reflexive Prefix ki-
   4.5 Emphatic Forms

5. Verbal Morphology
   5.1 Verb Stems
       5.1.1 Form I and Form II
       5.1.2 Distribution of Forms
   5.2 Pronominal Prefixes on Verbs
   5.3 Derivational Morphology
       5.3.1 Causative -sak
       5.3.2 Applicative -pih
       5.3.3 Directional Suffixes
       5.3.4 Reversive/Iterative -kik
       5.3.5 Ability -theih
       5.3.6 Intensive -gawp
   5.4 TAM Morphology
       5.4.1 Irrealis -ding
       5.4.2 Completive: -zo, -khit, -mang
       5.4.3 Perfective -ta, -sa
       5.4.4 Continuative -lai, -to
       5.4.5 Immediate -khin
   5.5 Negation

6. Other Categories
   6.1 Sentence-Final Particles
   6.2 Conjunctions
   6.3 Question Words
   6.4 Adverbs

7. Compounds
   7.1 Noun-Noun Compounds
   7.2 Verb-Verb Compounds
   7.3 Reduplication

8. Appendices
   A. Complete Morpheme Inventory
   B. Verb Stem Pairs (Form I/II)
   C. Sample Glossed Texts
```

## Phase 3: Example Collection

### Source Texts (Narrative)
- Genesis 1-3 (creation, fall)
- Genesis 12, 22 (Abraham narratives)
- Exodus 1-3 (Moses birth and call)
- Ruth 1-4 (complete book)
- Mark 1-5 (Jesus' ministry)
- Luke 15 (parables)
- Acts 2-4 (early church)

### Example Format
```
(verse_ref)
Original Tedim text
morpheme-by-morpheme segmentation
morpheme-by-morpheme gloss
Free English translation (from KJV)
```

### Examples per Morpheme
- High-frequency morphemes (>1000x): 5-10 examples
- Medium-frequency (100-1000x): 3-5 examples
- Low-frequency (<100x): 2-3 examples

## Phase 4: Comparison with Literature

After skeleton is complete, compare against:

### Primary Sources (Tedim-specific)
1. **Henderson 1965a/b** - Phonology and basic grammar
2. **Henderson 1965 Two Texts** - Text analysis
3. **Weera 1998** - Tone
4. **Zam Ngaih Cing 2018** - Modern grammar (2 parts)

### Secondary Sources (Otsuka papers)
5. **Otsuka - Applicative** - -pih suffix
6. **Otsuka - Causative/Benefactive** - -sak suffix
7. **Otsuka - Directional Affixes** - -khia, -lut, -to, -khiat
8. **Otsuka - Voice** - Passive, middle, etc.
9. **Otsuka - Burmese Loanwords** - Loan vocabulary

### Comparative Sources
10. **VanBik 2009** - Proto-Kuki-Chin reconstructions
11. **Button 2011** - Proto-Northern-Chin

## Phase 5: Analyzer Refinements

Based on literature review, potentially:
- Add new morpheme distinctions (e.g., -sak₁ vs -sak₂)
- Refine glosses based on scholarly consensus
- Add tone marking if relevant
- Document grammaticalization paths

---

## Immediate Next Steps

1. **Create grammar skeleton file** (`docs/SKELETON_GRAMMAR.md`)
   - Outline all chapters/sections
   - For each morpheme: form, gloss, 1 example

2. **Collect examples** for each morpheme
   - Use analyzer to find verses containing morpheme
   - Select diverse narrative contexts
   - Full Leipzig-style glossing

3. **Generate frequency counts** for each morpheme
   - Total occurrences in corpus
   - Helps prioritize documentation effort

---

*Plan created: 2026-03-17*
