# Tedim Chin Possession

This report documents the possession system of Tedim Chin based on analysis
of the Bible corpus (830,741 tokens).

## Overview

Tedim Chin has two primary strategies for marking possession:
1. **Pronominal prefixes**: ka-, na-, a- etc. for pronoun possessors
2. **Apostrophe marking**: NOUN' for full NP possessors

The possessor precedes the possessed noun in both constructions.

---

## Possessive Prefixes

### Paradigm

| Person | Singular | Plural | Approx. Count |
|--------|----------|--------|---------------|
| 1st | ka- "my" | kan- "our" | 3,241 / 358 |
| 2nd | na- "your" | nan- "your.PL" | 13,726 / 4,401 |
| 3rd | a- "his/her" | an- "their" | 64,855 / 856 |

**Structure**: POSS.PREFIX + NOUN

### Examples

| Form | Gloss | Meaning | Count |
|------|-------|---------|-------|
| a pa | 3SG father | his/her father | 5,964 |
| a nu | 3SG mother | his/her mother | 2,262 |
| a ta | 3SG child | his/her child | 5,570 |
| a zi | 3SG wife | his wife | 571 |
| a inn | 3SG house | his/her house | 879 |
| a min | 3SG name | his/her name | 762 |
| a gam | 3SG land | his/her land | 1,993 |

**Genesis 24:7**:
> **Ka pa'** inn le **ka** suahna leitang panin
> *1SG father.POSS house and 1SG birth-NMLZ land ABL-CVB*
> "from **my father's** house and the land of **my** birth"

### Kinship Terms

Kinship nouns are especially common with possessive prefixes:

| Noun | Meaning | a- | ka- | na- |
|------|---------|-----|------|------|
| pa | father | 5,964 | 682 | 1,655 |
| nu | mother | 2,262 | 204 | 279 |
| ta | child | 5,570 | 357 | 2,267 |
| zi | wife | 571 | 48 | 132 |
| tapa | son | 985 | 114 | 126 |
| tanu | daughter | 179 | 39 | 50 |
| sanggam | sibling | 492 | 87 | 147 |

---

## Apostrophe Possessive

For full NP possessors (not pronouns), Tedim Chin uses apostrophe marking:

**Structure**: POSSESSOR' + POSSESSED

| Form | Gloss | Count |
|------|-------|-------|
| topa' | lord.POSS | 2,056 |
| pasian' | god.POSS | 1,693 |
| israel' | israel.POSS | 22 |

**Total apostrophe occurrences**: 20,343

### Examples

**Genesis 4:3**:
> piakna **Topa'** tungah paipih a
> *offering LORD.POSS on-LOC bring and*
> "brought an offering unto **the LORD**"

**Genesis 9:26**:
> Topa **ka Pasian** in Shem thupha pia hen
> *LORD 1SG god ERG SHEM blessing give OPT*
> "Blessed be the LORD, **my God**, of Shem"

### Double Possession

Both strategies can combine:

> **a pa'** inn
> *3SG father.POSS house*
> "his father's house"

Here **a** marks third person, **pa'** marks the possessive on "father".

---

## Alienable vs. Inalienable

### Inalienable Possession

Kinship and body parts typically use simple prefix attachment:

| Type | Example | Structure |
|------|---------|-----------|
| Kinship | a pa "his father" | 3SG + kin |
| Body | a khe "his leg" | 3SG + body |

### Alienable Possession

Non-kinship nouns may use the same structure:

| Type | Example | Structure |
|------|---------|-----------|
| Property | a inn "his house" | 3SG + noun |
| Ownership | a gam "his land" | 3SG + noun |

**Note**: There is no clear grammatical distinction between alienable and
inalienable possession in terms of marking.

---

## Possessor Raising

The possessor can be fronted for topicalization:

> **Amah** a pa Terah ahi hi
> *3SG 3SG father TERAH be.3SG DECL*
> "**His** father was Terah"

---

## Word Order

Basic possessive word order is:

```
[POSSESSOR] + [POSSESSED]
```

| Structure | Example | Meaning |
|-----------|---------|---------|
| PRON.POSS + N | ka pa | my father |
| N' + N | Topa' inn | Lord's house |
| PRON.POSS + N' + N | a pa' inn | his father's house |

### Recursive Possession

Multiple levels of possession chain leftward:

> ka pa' sanggam' ta
> *1SG father.POSS sibling.POSS child*
> "my father's sibling's child" (my cousin)

---

## Distribution Summary

| Person | Prefix | Frequency |
|--------|--------|-----------|
| 3SG | a- | 64,855 (dominant) |
| 2SG | na- | 13,726 |
| 2PL | nan- | 4,401 |
| 1SG | ka- | 3,241 |
| 3PL | an- | 856 |
| 1PL | kan- | 358 |

The overwhelming dominance of **a-** (3SG) reflects the narrative nature
of Biblical text, where third-person reference is most common.

---

## Summary

1. **Pronominal possession**: Prefixes (ka-, na-, a-, kan-, nan-, an-)
2. **NP possession**: Apostrophe marking (NOUN')
3. **Word order**: Possessor precedes possessed
4. **High frequency**: 3SG **a-** most common (64,855x)
5. **Kinship**: Most commonly possessed nouns are kinship terms

**Key patterns**:
- a pa "his father" (5,964x)
- a ta "his child" (5,570x)
- Topa' "Lord's" (2,056x)
- na pa "your father" (1,655x)

**Total possession tokens**: ~90,000+ (10.8% of corpus)
