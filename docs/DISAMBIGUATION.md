# Tedim Chin Morphological Disambiguation

This document inventories all homophonous/polysemous morphemes in the analyzer
and describes the contextual rules used for disambiguation.

## Overview

The analyzer handles **37 polysemous morphemes** through the `AMBIGUOUS_MORPHEMES`
system in `scripts/analyze_morphemes.py`. Each entry specifies:
1. All attested meanings
2. The context that triggers each meaning
3. A default when context is ambiguous

## Homophonous Roots Inventory

### High-Frequency Polysemous Morphemes

| Root | Meanings | Disambiguation Rule |
|------|----------|---------------------|
| **za** | hear (verb), hundred (number) | 'hundred' after numerals (kum za, sawm za); 'hear' with verbal morphology |
| **na** | 2SG (pronoun), NMLZ (suffix) | '2SG' standalone; 'NMLZ' as suffix on verbs |
| **pa** | male/father (noun), NMLZ.AG (suffix) | 'male' standalone; 'NMLZ.AG' after verbs |
| **sa** | flesh (noun), PERF (aspect) | 'flesh' standalone; 'PERF' after verbs |
| **ta** | child (noun), PFV (aspect) | 'child' in compounds; 'PFV' after verbs |
| **in** | ERG (case), house (noun), QUOT (particle) | 'ERG' as suffix; 'house' in compounds; 'QUOT' after ci |
| **hi** | be (copula), DECL (particle) | 'be' with prefixes (a-hi); 'DECL' sentence-finally |

### Relational Nouns (Location/Position)

| Root | Primary | Secondary | Context |
|------|---------|-----------|---------|
| **tung** | on/upon | arrive (verb) | 'on' with -ah; 'arrive' with verbal morphology |
| **sung** | inside | high (adj) | 'inside' with -ah; 'high' rare |
| **kiang** | beside | separate (verb) | 'beside' with -ah; 'separate' with ki- |
| **lak** | among | take (verb) | 'among' relational; 'take' verbal |
| **nuai** | below | - | Always relational |
| **mai** | face | front | 'face' as noun; 'front' relational |

### Verbs with Multiple Meanings

| Root | Meanings | Context Rules |
|------|----------|---------------|
| **lam** | way, build, dance, manner | 'way' nominal; 'build' before -kik; 'dance' before -na; 'manner' after verbs |
| **man** | finish, catch, reason, price | 'finish' with khit; 'catch' verbal; 'reason' in manin; 'price' nominal |
| **mang** | dream, obey, fly | 'dream' standalone; 'obey' with thu; 'fly' in compounds |
| **kah** | climb, fight | 'climb' motion context; 'fight' conflict context |
| **hong** | 3→1 (prefix), open, come | '3→1' as prefix; 'open' verbal; 'come' standalone |

### TAM Markers with Nominal Homophones

| Root | TAM Meaning | Nominal Meaning |
|------|-------------|-----------------|
| **ding** | IRR (irrealis) | stand (verb) |
| **zo** | COMPL (completive) | south (direction) |
| **khin** | IMM (immediate) | move (verb) |
| **vei** | time (with numerals) | sick/wave |

## Context-Dependent Analysis

### Multi-Word Patterns

Some analyses require looking at surrounding words:

1. **ahih manin** → "therefore" (frozen expression)
   - Not: "be.3SG.REL" + "catch-ERG"

2. **bang hang hiam** → "why" (question formula)
   - hang = "reason" here, not "stallion"

3. **hih bangin** → "like this" / "in this manner"
   - hih = demonstrative, not copula

4. **kum za** → "hundred years"
   - za = "hundred" after numeral context

### Prefix-Triggered Disambiguation

| Prefix | Triggers | Example |
|--------|----------|---------|
| ki- | Reflexive/reciprocal verb | ki-kham → REFL-forbid (not REFL-gold) |
| ka-/na-/a- | Pronominal, expects verb | ka-za → 1SG-hear (not 1SG-hundred) |

### Suffix-Triggered Disambiguation

| Suffix | Triggers | Example |
|--------|----------|---------|
| -na | Nominalizer (expects verb base) | gen-na → speak-NMLZ |
| -pa | Agentive (expects verb base) | gen-pa → speaker |
| -in | ERG case (expects noun phrase) | mi-in → person-ERG |
| -ah | LOC case (expects noun/relational) | sung-ah → inside-LOC |

## Implementation

The disambiguation is implemented in `analyze_morphemes.py`:

```python
AMBIGUOUS_MORPHEMES = {
    'za': [
        ('hear', 'verbal'),      # Primary: with verbal morphology
        ('hundred', 'numeral'),  # After kum/sawm, before tul
    ],
    # ... 37 entries total
}

def get_morpheme_gloss(morpheme, position, context):
    """Return appropriate gloss based on context."""
    if morpheme not in AMBIGUOUS_MORPHEMES:
        return default_lookup(morpheme)
    meanings = AMBIGUOUS_MORPHEMES[morpheme]
    # Context-based selection logic
    ...
```

## Adding New Disambiguation Rules

When discovering a new homophone:

1. Verify both meanings exist in corpus (≥3 examples each)
2. Identify distinguishing context
3. Add to `AMBIGUOUS_MORPHEMES` with context tags
4. Add regression test in `tests/regression_tests.md`
5. Document here

---

*Last updated: 2026-03-17*
*Part of Phase 3: Disambiguation Documentation*
