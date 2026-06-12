# Phonology and tone source-alignment diagnostic

The safe conclusion is narrow: print a cautious segmental orientation, an orthography caveat, a three-tone summary, a tiny formal tone contrast, and a blocked `-a` warning. Do not print a solved tone system.

## 1. Segmental phonology

The literature supports a conservative segmental summary rather than a full phoneme table. Henderson and ZNC both support a small consonant inventory, a five-vowel summary, and simple syllable-shape claims that are good enough for grammar-facing orientation prose [@henderson1965, pp. 9-13; @zamngaihcing2017, pp. 25-26, 37].

| Area | Safe conclusion | Status |
| --- | --- | --- |
| Consonants | Conservative consonant inventory summary is safe to print. | safe |
| Vowels | Conservative vowel inventory summary is safe to print. | safe |
| Syllable shape | Mostly simple CV/CVC orientation is safe to print. | safe |
| Orthography | Practical spelling is useful but indirect. | safe with caveat |

## 2. Tone

Tedim is described as a three-tone language in the literature, and the ordinary spelling system does not mark tone. That means the section can state the three-tone summary, but it should not pretend that spelling alone recovers tone or that every tonal alternation is already settled [@henderson1965, p. 13; @zamngaihcing2017, pp. 57-60].

The current boundary is simple:

- lexical tone can be stated cautiously;
- grammatical tone can be mentioned cautiously;
- tone in verbal or suffixal material stays boundary-level;
- full tone sandhi remains unresolved.

## 3. The blocked `-a` issue

The analyzer-gap notes (`docs/grammar/README_ANALYZER_GAPS.md`, `docs/grammar/ANALYZER_LITERATURE_GAPS.md`, `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md`, `docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md`) preserve the blocked high/low `-a` contrast. The literature distinguishes the high-tone and low-tone values, but the current corpus spelling does not preserve tone, so the distinction cannot be recovered safely.

Best-supported conclusion: `-a` stays blocked and unresolved, not normalized into a single grammar fact.

## 4. Relationship to other grammar sections

- **Stem alternation:** tone interacts with Form I / Form II material, but that analysis belongs there.
- **TAM / aspect / modal:** tone-bearing suffixes and suffixal alternations belong there.
- **`-pih`:** comitative/applicative material belongs there.
- **Verb paradigms:** finite predicate work stays separate.
- **Analyzer-gap material:** keep the blocked `-a` contrast and other unresolved tone-sensitive material out of this section.

## 5. Print decision

### Safe to print now

- cautious segmental orientation
- orthography caveat
- three-tone status summary
- a tiny formal tone contrast from the literature
- blocked `-a` warning

### Literature-only wording

- tone is contrastive
- ordinary spelling does not mark tone
- tone is described in the literature

### Blocked

- the exact high/low `-a` distinction
- full tone sandhi rules
- any claim of a complete tone system

### Belongs elsewhere

- stem alternation
- TAM / aspect / modal
- `-pih`
- verb paradigms

### Human review tasks

- verify consonant and vowel claims against the literature
- check that orthography is not mistaken for phonology
- confirm tone is not overclaimed
- confirm the `-a` issue stays blocked
- decide whether this section should remain an orientation section or later expand into a fuller chapter
