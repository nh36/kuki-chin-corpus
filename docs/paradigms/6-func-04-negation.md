# Tedim Chin Negation

This report documents the negation system of Tedim Chin based on analysis
of the Bible corpus (830,741 tokens).

## Overview

Tedim Chin uses post-verbal negation with the primary negative marker **lo**
appearing after the verb. The system includes:
- Standard negation: lo (6,408x)
- Negative polarity items: kuamah "nobody", bangmah "nothing"
- Aspectual negation: nawn lo "no longer"

---

## Negation Markers

### Primary Marker: lo

| Form | Position | Function | Count |
|------|----------|----------|-------|
| lo | post-verbal | standard negation | 6,408 |

**Structure**: VERB + lo + (copula/auxiliary)

**Genesis 4:5**:
> Kain le ama piakna thusim **lo** hi
> *KAIN and 3SG offering accept NEG PROX.COP*
> "to Cain and his offering he had **not** respect"

### Negative Constructions

| Pattern | Structure | Meaning | Count |
|---------|-----------|---------|-------|
| V lo hi | V NEG COP | "is not V" | 1,695 |
| V lo ding | V NEG IRR | "will not V" | 1,202 |
| V lo ding hi | V NEG IRR COP | "should not V" | 658 |
| V lo uh | V NEG 2/3PL | "don't V (pl.)" | 749 |
| om lo | exist NEG | "doesn't exist" | 684 |

---

## Prohibitive (Negative Imperative)

Prohibitive commands use **lo** with plural marker **-uh**:

| Pattern | Meaning | Count |
|---------|---------|-------|
| V lo uh | "don't V!" (plural) | 749 |
| V lo ding hi | "must not V" | 658 |
| ding hi lo | "must not" | 84 |
| pih lo | "don't" (specific) | 65 |

**Genesis 2:25**:
> maizum **lo uh** hi
> *shame NEG 2/3PL PROX.COP*
> "they were **not** ashamed"

---

## Negative Polarity Items

Tedim Chin has negative indefinite pronouns formed with **-mah** (emphatic):

| Form | Structure | Meaning | Count |
|------|-----------|---------|-------|
| kuamah | kua-mah | who-EMPH = nobody | 664 |
| bangmah | bang-mah | what-EMPH = nothing | 525 |

These require a negative context (unlike English "anyone/anything"):

**Exodus 2:12**:
> **kuamah** mu lo ahih manin
> *nobody see NEG be.3SG because-CVB*
> "when he saw that there was **no man**"

**Structure**: [NPI] ... V lo ("nobody/nothing ... V-NEG")

---

## Ability/Potential Negation

Inability is expressed with **thei lo** or specific ability verbs + lo:

| Pattern | Meaning | Count |
|---------|---------|-------|
| thei lo | cannot (know/able) | 668 |
| theih lo | cannot (nominalized) | 151 |
| ngah lo | cannot get | 43 |

**1 Kings 1:18**:
> na **theih lo** hangin
> *2SG know.NMLZ NEG because-CVB*
> "thou **knowest** it **not**"

---

## Aspectual Negation: nawn lo

The auxiliary **nawn** "still, anymore" combines with **lo** for cessative aspect:

| Pattern | Meaning | Count |
|---------|---------|-------|
| nawn lo | no more, no longer | 687 |
| om nawn lo | no longer exists | 152 |

**Genesis 40:23**:
> Josef phawk **nawn lo** a, amah mangngilh ta hi
> *JOSEF remember anymore NEG and 3SG forget PFV PROX.COP*
> "yet did not...remember Joseph, but **forgot** him"

---

## Negative Scope

Negation takes scope over the immediately preceding verb:

### Subject Scope
> **kuamah** om **lo** "nobody exists" (NPI + V + NEG)

### Verb Scope
> a om **lo** "it doesn't exist" (SUBJ + V + NEG)

### Examples by Verb

| Pattern | Gloss | Count |
|---------|-------|-------|
| a om lo | 3SG exist NEG | 179 |
| gen lo | say NEG | 83 |
| pai lo | go NEG | 53 |
| bawl lo | do NEG | 51 |
| hong pai lo | 3→1 come NEG | 27 |

---

## Negative + Modal Combinations

| Pattern | Structure | Meaning | Count |
|---------|-----------|---------|-------|
| lo ding | NEG IRR | will not | 1,202 |
| lo hi | NEG COP | is not | 1,695 |
| lo ding hi | NEG IRR COP | should/must not | 658 |
| lo zaw | NEG COMPAR | not rather | 17 |

**Deontic negation** (obligation):
> bawl **lo ding hi**
> *do NEG IRR COP*
> "should **not** do"

**Epistemic negation** (certainty):
> tua mipa **lo hi**
> *DIST man NEG COP*
> "that is **not** the man"

---

## Word Order Summary

Basic negative clause structure:

```
(SUBJ) + (OBJ) + VERB + lo + (AUX/COP)
```

| Slot | Content | Example |
|------|---------|---------|
| 1 | Subject | amah "he" |
| 2 | Object | tua "that" |
| 3 | Verb | bawl "do" |
| 4 | NEG | lo |
| 5 | Aux/Cop | hi / ding / uh |

**Full example**:
> Amah in tua bawl **lo ding** hi
> *3SG ERG DIST do NEG IRR COP*
> "He will **not** do that"

---

## Summary

1. **Post-verbal negation**: lo follows verb
2. **Prohibitive**: V lo uh (plural imperative)
3. **NPIs**: kuamah "nobody", bangmah "nothing" (require negative)
4. **Cessative**: nawn lo "no longer"
5. **Inability**: thei(h) lo "cannot"
6. **Modal combinations**: lo ding "won't", lo ding hi "shouldn't"

**Total negative tokens**: ~10,000+ (1.2% of corpus)

**Key patterns**:
- lo hi "is not" (1,695x)
- lo ding "will not" (1,202x)
- nawn lo "no longer" (687x)
- kuamah/bangmah "nobody/nothing" (1,189x combined)
