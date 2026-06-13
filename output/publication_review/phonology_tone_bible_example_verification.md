# Phonology/tone Bible-example verification

This verification pass checks whether the current Bible-attested phonology/tone rows are genuinely source-resolved and correctly classified for print-facing use.

## Data consulted

- `output/publication_review/grammar_phonology_tone_print_slice.md`
- `output/publication_review/candidates_phonology_tone.tsv`
- `data/ctd_analysis/tokens.tsv`
- `bibles/extracted/ctd/ctd-x-bible.txt`
- `docs/grammar/lit-reviews/02-phon-02-tone-lit.md`
- `docs/grammar/lit-reviews/02-phon-01-phonology-lit.md`

## 1. `ta / -ta`

### Claimed set

Lexical `ta` 'child' versus grammatical `-ta` (PFV), with Bible anchors at Genesis 11:30 and Matthew 4:4.

| Member form | Bible source | Exact Bible form as printed | Free/bound/embedded | Morphological analysis status | Meaning support from verse context | Tone claim source | Evidence type classification | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lexical `ta` | Genesis 11:30 | `ta` (in `ta nei lo hi`) | free lexical form | secure | verse directly means 'had no child' | literature: lexical high-tone `ta` | supporting member | keep |
| grammatical `-ta` candidate | Matthew 4:4 | `nungta` (in `... thute tawh nungta zaw hi`) | embedded in larger word | analyzer-supported with caveat | verse context supports `live` semantics; not a strict isolated suffix token | literature: grammatical low-tone `-ta` | supporting member (not strict minimal) | keep with caveat |

### `nungta` morphology check

- In the current `tokens.tsv` export, surface `nungta` is consistently segmented as `nung-ta` with gloss `life-PFV`.
- Related forms such as `nungta-in` and `nungta-lai` are likewise segmented with `-ta`, supporting productive morphology in the analyzer layer.
- `scripts/analyze_morphemes.py` also contains a lexical `nungta` entry (`variant of nuntak`), so this row should remain caveated and not be treated as a strict minimal pair.

**Decision:** remain promoted as `supporting_bible_attestation`, not as `true_minimal_pair` or strict `near_minimal_pair`.

## 2. `thei / -thei`

### Claimed set

Lexical `thei` 'know' versus abilitative `-thei` in `lutthei`, using Genesis 4:9 and Matthew 7:21.

| Member form | Bible source | Exact Bible form as printed | Free/bound/embedded | Morphological analysis status | Meaning support from verse context | Tone claim source | Evidence type classification | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lexical `thei` | Genesis 4:9 | `thei` (in `Ka thei kei hi`) | free lexical form | secure enough for this slice | verse context supports 'I do not know' | literature: lexical high-tone `thei` | near-minimal member | keep |
| grammatical `-thei` | Matthew 7:21 | `lutthei` | bound suffix in host verb | secure | verse context supports abilitative meaning ('be able to enter') | literature: grammatical low-tone `-thei` | near-minimal member | keep |

**Decision:** remain promoted as `near_minimal_pair` (host-bound grammatical member, so not strict minimal).

## 3. `hi / hi`

### Claimed set

Homographic lexical/grammatical contrast in Genesis 16:13 (`na hi hi`).

| Member form | Bible source | Exact Bible form as printed | Free/bound/embedded | Morphological analysis status | Meaning support from verse context | Tone claim source | Evidence type classification | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| lexical/copular `hi` | Genesis 16:13 | first `hi` in `na hi hi` | free predicate-position form | context-secure with caveat | clause context supports copular reading ('you are') | literature: lexical high-tone `hi` | homographic lexical/grammatical contrast | keep with caveat |
| declarative `hi` | Genesis 16:13 | second `hi` in `na hi hi` | sentence-final grammatical form | secure | sentence-final declarative function is clear in context | literature: declarative low-tone `hi` | homographic lexical/grammatical contrast | keep |

**Decision:** remain promoted as `homographic_lexical_grammatical_contrast`, explicitly caveated.

## 4. Short Bible-example verification

Current short examples are checked against verse text and intended pair membership:

| Example label | Verse | Tedim printed form | Target member illustrated | Verification result |
| --- | --- | --- | --- | --- |
| `@ex:phon-thei-abil-matt7` | Matthew 7:21 | `lutthei ding uh hi` | grammatical `-thei` | text and gloss alignment acceptable |
| `@ex:phon-hi-lex-gram-gen16` | Genesis 16:13 | `na hi hi` | `hi / hi` lexical-vs-grammatical contrast | text and gloss alignment acceptable |

Genesis 11:30 and Matthew 4:4 are retained as table evidence for the `ta / -ta` supporting row; they do not need separate full interlinear blocks to remain source-resolved.

## 5. Tone-marking audit for assembled preview

- Bible examples should be printed in ordinary Bible spelling in the object-language line.
- Tone-marked forms are restricted to literature-facing table columns and prose caveats.
- The prose explicitly states that Bible orthography locates forms in context but does not directly prove tone values.

## 6. Final decision summary

| Claimed set | Final status |
| --- | --- |
| `ta / -ta` | remain promoted only as `supporting_bible_attestation`; not a strict minimal pair |
| `thei / -thei` | remain promoted as `near_minimal_pair` |
| `hi / hi` | remain promoted as `homographic_lexical_grammatical_contrast` |

Unresolved `-a` tone remains blocked, and analyzer-gap material is not promoted as settled grammar fact.
