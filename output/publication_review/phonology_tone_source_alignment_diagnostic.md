# Phonology and tone source-alignment diagnostic

The safe conclusion remains hybrid and narrow: literature-backed tables are the right format for general segmental and tonal orientation, while a small number of source-resolved Bible-attested examples can be promoted where morphology and meaning are secure enough in context.

## 1. Segmental orientation

The literature supports conservative orientation claims for consonants, vowels, and syllable shape [@henderson1965, pp. 9-13; @zamngaihcing2017, pp. 25-26, 37]. These remain literature-backed table claims rather than a full phoneme reconstruction.

| Area | Safe conclusion | Status |
| --- | --- | --- |
| Consonants | Conservative consonant inventory summary is safe to print. | safe |
| Vowels | Conservative vowel inventory summary is safe to print. | safe |
| Syllable shape | Mostly simple CV/CVC orientation is safe to print. | safe |
| Orthography | Practical spelling is useful for locating forms and segmental orientation only. | safe with caveat |

## 2. Tone orientation and Bible attestation

Tedim tone claims remain literature-backed: three tones are reported in the phonological literature, while ordinary Bible spelling does not mark tone [@henderson1965, p. 13; @zamngaihcing2017, pp. 57-60].

A small number of Bible-attested examples are now appropriate where forms are source-resolved:

- `thei / -thei` (Genesis 4:9; Matthew 7:21) remains promoted as a near-minimal lexical/grammatical contrast.
- `hi / hi` (Genesis 16:13) remains promoted as a homographic lexical/grammatical contrast.
- `ta / -ta` (`ta` in Genesis 11:30; `nungta` in Matthew 4:4) remains promoted only as supporting Bible attestation, not as a strict minimal pair.

For `ta / -ta`, the corpus analyzer currently supports a real `nung-ta` segmentation rather than a purely opaque lexical item: in `data/ctd_analysis/tokens.tsv`, surface `nungta` is consistently segmented `nung-ta` in the current export, and related forms such as `nungta-in` and `nungta-lai` are likewise segmented with `-ta`. This supports keeping the row with a caveat rather than dropping it outright.

These Bible examples support form existence and contextual use. The tone analysis attached to them remains literature-backed when orthography is unmarked.

## 3. The blocked `-a` issue

The analyzer-gap notes (`docs/grammar/README_ANALYZER_GAPS.md`, `docs/grammar/ANALYZER_LITERATURE_GAPS.md`, `docs/grammar/ANALYZER_GAPS_CORPUS_EXAMPLES.md`, `docs/grammar/ANALYZER_GAPS_QUICK_REFERENCE.md`) continue to block the high/low `-a` contrast. The literature distinguishes these values, but current corpus spelling does not recover them safely.

Best-supported conclusion: keep `-a` blocked and unresolved.

## 4. Relationship to other grammar sections

- **Stem alternation:** open/checked and Form I/II tone interactions stay anchored there.
- **TAM / aspect / modal:** suffixal tone-sensitive material stays anchored there.
- **`-pih`:** comitative/applicative material stays anchored there.
- **Verb paradigms:** finite predicate structure remains separate.
- **Analyzer-gap material:** unresolved tone-sensitive rows remain blocked rather than promoted.

## 5. Print decision

### Safe to print now

- cautious segmental orientation tables
- orthography caveat
- literature-backed three-tone summary
- a small number of Bible-attested near-minimal, homographic, or supporting lexical/grammatical examples with explicit caveats
- blocked `-a` warning

### Literature-only wording

- tone is contrastive
- ordinary spelling does not mark tone
- tone values for Bible-attested forms come from literature unless tone marking is explicit in source transcription

### Blocked

- high/low `-a` distinction
- full tone sandhi rules
- any claim of a complete resolved tone system

### Belongs elsewhere

- stem alternation
- TAM / aspect / modal
- `-pih`
- verb paradigms

### Human review tasks

- verify promoted Bible-attested contrasts are genuinely minimal/near-minimal, homographic lexical/grammatical, or supporting-only as labeled
- verify verse context supports assigned meanings
- verify literature-backed tone assignments
- verify `ta / -ta` remains caveated unless stronger independent morphology evidence is preferred
- verify `-a` remains blocked
