# Tedim Chin Reduplication

This report documents reduplication patterns in Tedim Chin based on analysis
of the Bible corpus (830,741 tokens).

## Overview

Tedim Chin uses reduplication for:
- **Intensification**: mahmah "very" (< mah "emphatic")
- **Distribution**: peuhpeuh "each" (< peuh "every")
- **Iteration**: ni ni "day by day"
- **Expressiveness**: kawikawi "all around"

---

## Types of Reduplication

### 1. Full Reduplication (ABAB)

Complete doubling of a morpheme within a single word:

| Form | Base | Gloss | Meaning | Count |
|------|------|-------|---------|-------|
| mahmah | mah | EMPH~EMPH | very, really | 1,351 |
| peuhpeuh | peuh | each~each | every, each | 455 |
| taktak | tak | true~true | truly, really | 314 |
| leuleu | leu | ITER~ITER | continually | 193 |
| semsem | sem | INTENS~INTENS | intensifier | 159 |
| veve | ve | go~go | again and again | 142 |
| kawikawi | kawi | side~side | everywhere, all around | 135 |

### 2. Syntactic Reduplication (X X)

Word repeated as separate tokens:

| Pattern | Meaning | Count |
|---------|---------|-------|
| hi hi | emphasis | 578 |
| ni ni | day by day | 9 |
| khat khat | one by one | 7 |
| kum kum | year by year | 7 |

---

## Semantic Functions

### Intensification (mahmah, taktak)

Reduplication intensifies the base meaning:

| Form | Base | Meaning | Intensified |
|------|------|---------|-------------|
| mahmah | mah | emphatic | very, truly | 
| taktak | tak | true | truly, certainly |
| semsem | sem | ? | very much |

**Genesis 17:2**:
> nang tampi tak kong phasak ding hi
> *2SG much true 1→2 multiply IRR DECL*
> "multiply thee exceedingly" (tak intensifies tampi)

### Distribution (peuhpeuh, khat khat)

Marks distributive meaning:

| Form | Base | Meaning |
|------|------|---------|
| peuhpeuh | peuh | every, each (distributive) |
| khat khat | khat | one by one |

**Proverbs 17:10**:
> mipil **khat khat**vei tai-na
> *wise one one-time rebuke-NMLZ*
> "a rebuke entereth more... **one by one**"

### Iteration/Continuation (leuleu, veve)

Marks repeated or continuous action:

| Form | Base | Meaning |
|------|------|---------|
| leuleu | leu | continually |
| veve | ve | again and again |
| gengen | gen | saying repeatedly |

### Location (kawikawi)

Marks totality of location:

| Form | Base | Meaning | Count |
|------|------|---------|-------|
| kawikawi | kawi | everywhere, all around | 135 |

---

## Morphological Analysis

### Base + Reduplication

| Reduplicated | Base | Analysis |
|--------------|------|----------|
| mahmah | mah | EMPH~EMPH → "very" |
| peuhpeuh | peuh | EVERY~EVERY → "each" |
| taktak | tak | TRUE~TRUE → "truly" |
| tuamtuam | tuam | SEPARATE~SEPARATE → "various" |
| bekbek | bek | ONLY~ONLY → "merely" |
| zenzen | zen | SILENT~SILENT → "silently" |
| bangbang | bang | WHAT~WHAT → "whatever" |
| theithei | thei | KNOW~KNOW → "knowingly" |

### Reduplication in Analyzer

The analyzer recognizes these patterns:

| Pattern | Gloss |
|---------|-------|
| mahmah | EMPH.INTENS |
| peuhpeuh | DISTR |
| taktak | INTENS |
| leuleu | ITER |

---

## Distribution by Category

### Intensifiers (1,824 tokens)
- mahmah (1,351)
- taktak (314)
- semsem (159)

### Distributives (462 tokens)
- peuhpeuh (455)
- khat khat (7)

### Iteratives (335 tokens)
- leuleu (193)
- veve (142)

### Expressive (135+ tokens)
- kawikawi (135)

---

## Syntactic vs. Morphological

| Type | Form | Position | Example |
|------|------|----------|---------|
| Morphological | mahmah | single word | pha mahmah "very good" |
| Syntactic | ni ni | two words | ni ni-in "day by day" |

### Morphological (compound word)

> pha **mahmah** hi
> *good very DECL*
> "is **very** good"

### Syntactic (separate words)

> **ni ni**-in a bawl hi
> *day day-CVB 3SG do DECL*
> "**day by day** he did (it)"

---

## Word Class of Reduplicated Forms

| Word Class | Examples | Function |
|------------|----------|----------|
| Adverb | mahmah, taktak | modifies verb/adj |
| Quantifier | peuhpeuh | modifies noun |
| Manner | kawikawi, zenzen | adverbial |
| Temporal | leuleu | aspectual |

---

## Summary

1. **Full reduplication**: ABAB pattern within single words
2. **Syntactic reduplication**: X X pattern as separate tokens
3. **Functions**: Intensification, distribution, iteration
4. **Productivity**: Semi-productive (certain bases only)

**High-frequency patterns**:
- mahmah "very" (1,351x)
- peuhpeuh "each/every" (455x)
- taktak "truly" (314x)
- leuleu "continually" (193x)

**Total reduplicated tokens**: ~3,500+ (0.4% of corpus)

**Semantic categories**:
- Intensification: mahmah, taktak, semsem
- Distribution: peuhpeuh, khat khat
- Iteration: leuleu, veve
- Spatial totality: kawikawi
