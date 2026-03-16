# Tedim Chin Morphological Analyzer Regression Tests

This document captures errors that were fixed during development.
**Review before each commit** to ensure no regressions.

## Test Format
Each test shows:
- **Citation**: Bible verse reference
- **Token/Phrase**: The Tedim text being tested
- **KJV**: English translation for context
- **Wrong**: Previous incorrect parse
- **Correct**: Expected correct parse

---

## 1. PROSP → IRR (ding marker)

**Source**: Zam Ngaih Cing (2018) - "irrealis marker"

| Token | Wrong | Correct |
|-------|-------|---------|
| ding | PROSP | IRR |
| dinghi | PROSP-be | IRR-be |
| dingin | PROSP-ERG | IRR-ERG |

**Citation**: Throughout corpus (13,000+ occurrences)

---

## 2. Proper Noun vs Common Word Disambiguation

### 2.1 sin/Sin
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| sin | SIN (proper) | near | lowercase = common word |
| Sin | near | SIN | Wilderness of Sin (EXO 16:1) |

**Citation**: EXO 16:1 "Sin khuazing" (Wilderness of Sin)

### 2.2 lot/Lot
| Token | Wrong | Correct | Context |
|-------|-------|---------|---------|
| lot | arrow | cast (verb) | verbal use (GEN 31:35) |
| Lot | cast | LOT | proper noun (GEN 11:27) |
| lotte | lo-te | lot-te (arrow-PL) | plural of lot 'arrow' |

**Citation**: GEN 11:27 "Lot a tapa" (Lot his son)

---

## 3. Ghost Entries Removed

These meanings were incorrectly in the dictionary but don't appear in corpus:

| Token | Ghost Meaning | Actual Meaning | Evidence |
|-------|---------------|----------------|----------|
| awk | ram | trap/snare | ram = tuutal |
| huh | blow | help | blow = mut/kitum |
| zong | warm | also | warm = lum |
| hang | stallion | reason | horse = sakol |
| ap | span | entrust | span = letmat kua |

---

## 4. Polysemy Disambiguation

### 4.1 kham (gold vs forbid vs hold)
| Context | Parse | Meaning |
|---------|-------|---------|
| kham (default) | gold | precious metal |
| kikham | REFL-forbid | refrain |
| pawi kham | feast hold | hold feast |

**Citation**: GEN 2:11 "kham a omna" (where gold is)

### 4.2 vei (sick vs time)
| Context | Parse | Meaning |
|---------|-------|---------|
| vei (default) | sick | illness |
| khatvei | one-time | once |
| nihvei | two-time | second time |

**Citation**: GEN 27:36 "nihvei hong suankhia" (twice deceived)

---

## 5. Tokenization

Apostrophe-containing words must be kept intact:

| Token | Wrong Split | Correct |
|-------|-------------|---------|
| ke'n | ke + n | ke'n (1SG.PRO) |
| hi'ng | hi + ng | hi'ng (be-EMPH) |

---

## 6. Function Words (Opaque)

These parse as atomic units, not decomposed:

| Token | Wrong | Correct |
|-------|-------|---------|
| ahihleh | a-hih-leh (3SG-be.II-if) | ahihleh (if) |
| bangmah | bang-mah (what-EMPH) | bangmah (nothing) |
| kuamah | kua-mah (who-EMPH) | kuamah (nobody) |

---

## Running Tests

```python
# Quick verification
import sys; sys.path.insert(0, 'scripts')
from analyze_morphemes import analyze_word

tests = [
    ('ding', 'IRR'),           # not PROSP
    ('sin', 'near'),           # not SIN
    ('Sin', 'SIN'),            # proper noun
    ('lot', 'cast'),           # verb, not arrow
    ('Lot', 'LOT'),            # proper noun
    ('kham', 'gold'),          # default
    ('kikham', 'REFL-forbid'), # with ki-
    ('ahihleh', 'if'),         # opaque
    ("ke'n", '1SG.PRO'),       # apostrophe preserved
]

for token, expected_gloss in tests:
    seg, gloss = analyze_word(token)
    status = '✓' if expected_gloss in gloss else '✗'
    print(f'{status} {token}: {gloss}')
```

---
*Last updated: March 2026*
