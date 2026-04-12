# Kuki-Chin Shared Backend Specification

This document specifies the normalized intermediate representation (IR) that
both dictionary generation and grammar report generation read from.

## Design Principles

1. **Single source of truth**: One data layer serves dictionary, grammar, and lookup
2. **Explicit uncertainty**: Review status, confidence, and alternative analyses are first-class
3. **Lexical vs grammatical distinction**: Forms with dual functions are modeled explicitly
4. **Sense-level granularity**: Examples and functions link to senses, not just lemmas
5. **Language-agnostic core**: Schema works across Kuki-Chin languages with dialect extensions

## Storage Format

**SQLite** is chosen for the shared backend because:

- Cross-linking (examples → senses → lemmas, tokens → morphemes) is central
- Many queries involve filtering + joining (e.g., "all examples for sense X")
- Atomic updates during iterative refinement are safer than full-file rewrites
- Schema enforcement catches errors early
- Tooling (CLI, Python, visualization) is mature

Location: `data/{lang}_backend.db` (e.g., `data/ctd_backend.db`)

TSV exports remain available as derived products for external tools.

---

## Entity Reference

### 1. `languages`

Language-level metadata.

| Column | Type | Description |
|--------|------|-------------|
| `iso` | TEXT PK | ISO 639-3 code (e.g., 'ctd') |
| `name` | TEXT | Language name |
| `family` | TEXT | 'Kuki-Chin' |
| `source_bible` | TEXT | Path to primary corpus |
| `analyzer_module` | TEXT | Python module name |
| `notes` | TEXT | |

### 2. `sources`

Source texts (Bible books, chapters, verses).

| Column | Type | Description |
|--------|------|-------------|
| `source_id` | TEXT PK | e.g., '01001001' (BBCCCVVV) |
| `iso` | TEXT FK | Language |
| `book_code` | TEXT | '01'-'66' |
| `chapter` | INT | |
| `verse` | INT | |
| `text` | TEXT | Raw verse text |
| `text_normalized` | TEXT | Normalized form |
| `kjv_text` | TEXT | Aligned KJV (if available) |
| `token_count` | INT | Cached count |

### 3. `tokens`

Every token occurrence in the corpus.

| Column | Type | Description |
|--------|------|-------------|
| `token_id` | INTEGER PK | Auto-increment |
| `source_id` | TEXT FK | → sources |
| `position` | INT | 0-indexed position in verse |
| `surface` | TEXT | As-written form |
| `normalized` | TEXT | Lowercased, punctuation stripped |
| `wordform_id` | TEXT FK | → wordforms |
| `is_sentence_final` | INT | Boolean (0/1) |

### 4. `wordforms`

Distinct surface forms (types) with their analysis.

| Column | Type | Description |
|--------|------|-------------|
| `wordform_id` | TEXT PK | Stable ID: `{normalized}` |
| `surface` | TEXT | Representative spelling |
| `normalized` | TEXT | Canonical form |
| `lemma_id` | TEXT FK | → lemmas |
| `segmentation` | TEXT | e.g., 'ka-pai-ding' |
| `gloss` | TEXT | Full gloss string |
| `pos` | TEXT | Part of speech |
| `frequency` | INT | Token count |
| `is_ambiguous` | INT | 0/1 |
| `status` | TEXT | 'auto', 'reviewed', 'needs_review' |

### 5. `lemmas`

Dictionary headwords.

| Column | Type | Description |
|--------|------|-------------|
| `lemma_id` | TEXT PK | Stable ID: `{citation_form}` |
| `citation_form` | TEXT | Dictionary headword |
| `pos` | TEXT | Primary POS |
| `entry_type` | TEXT | 'lexical', 'grammatical', 'mixed' |
| `primary_gloss` | TEXT | Main English gloss |
| `token_count` | INT | Total corpus occurrences |
| `form_count` | INT | Number of distinct wordforms |
| `is_polysemous` | INT | 0/1 |
| `needs_review` | INT | 0/1 |
| `entry_status` | TEXT | 'clean', 'draft', 'unsafe_gloss' |
| `notes` | TEXT | Editorial notes |

### 6. `senses`

Distinct meanings/functions of a lemma.

| Column | Type | Description |
|--------|------|-------------|
| `sense_id` | TEXT PK | `{lemma_id}.{sense_num}` |
| `lemma_id` | TEXT FK | → lemmas |
| `sense_num` | INT | 1, 2, 3... |
| `pos` | TEXT | POS for this sense (may differ from lemma) |
| `gloss` | TEXT | Sense-specific gloss |
| `definition` | TEXT | Longer definition |
| `usage_type` | TEXT | 'lexical', 'grammatical', 'mixed' |
| `frequency` | INT | Token count for this sense |
| `is_primary` | INT | 0/1 |
| `notes` | TEXT | |

### 7. `grammatical_morphemes`

Affixes, clitics, particles, and grammaticalized forms.

| Column | Type | Description |
|--------|------|-------------|
| `morpheme_id` | TEXT PK | `{form}.{function}.{category}` |
| `form` | TEXT | Surface form |
| `gloss` | TEXT | Leipzig-style gloss (e.g., 'ERG', 'CAUS') |
| `function` | TEXT | Same as gloss, or expanded |
| `category` | TEXT | 'pronominal_prefix', 'case_marker', etc. |
| `subcategory` | TEXT | |
| `position` | TEXT | 'prefix', 'suffix', 'clitic', 'particle' |
| `frequency` | INT | |
| `environments` | TEXT | Pipe-separated list |
| `is_polysemous` | INT | 0/1 |
| `lexical_source_id` | TEXT FK | → lemmas (if grammaticalized from lexical item) |
| `status` | TEXT | 'clean', 'contaminated', 'needs_review' |
| `notes` | TEXT | |

### 8. `examples`

Curated example sentences linked to senses or morphemes.

| Column | Type | Description |
|--------|------|-------------|
| `example_id` | INTEGER PK | Auto-increment |
| `source_id` | TEXT FK | → sources |
| `sense_id` | TEXT FK | → senses (may be NULL) |
| `morpheme_id` | TEXT FK | → grammatical_morphemes (may be NULL) |
| `target_form` | TEXT | The word/morpheme being illustrated |
| `tedim_text` | TEXT | Full verse text |
| `segmented` | TEXT | Morpheme-segmented |
| `glossed` | TEXT | Interlinear gloss |
| `kjv_text` | TEXT | English translation |
| `quality` | TEXT | 'excellent', 'good', 'acceptable' |
| `example_type` | TEXT | 'sense', 'morpheme', 'construction' |
| `notes` | TEXT | |

### 9. `constructions`

Grammar patterns and collocations (for grammar chapters).

| Column | Type | Description |
|--------|------|-------------|
| `construction_id` | TEXT PK | e.g., 'serial_verb_motion' |
| `name` | TEXT | Human-readable name |
| `category` | TEXT | 'clause', 'phrase', 'morphological' |
| `pattern` | TEXT | Abstract pattern (e.g., 'V1-V2.DIR') |
| `description` | TEXT | Prose description |
| `morpheme_ids` | TEXT | Pipe-separated FK list |
| `frequency` | INT | |
| `example_ids` | TEXT | Pipe-separated FK list |
| `status` | TEXT | |

### 10. `grammar_topics`

Chapter/section markers for grammar report generation.

| Column | Type | Description |
|--------|------|-------------|
| `topic_id` | TEXT PK | e.g., 'tam_markers' |
| `title` | TEXT | Chapter/section title |
| `parent_id` | TEXT FK | → grammar_topics (for hierarchy) |
| `display_order` | INT | Display order within parent |
| `description` | TEXT | |
| `construction_ids` | TEXT | Related constructions |
| `morpheme_ids` | TEXT | Related morphemes |
| `status` | TEXT | 'draft', 'complete' |

### 11. `review_queue`

Items requiring manual attention.

| Column | Type | Description |
|--------|------|-------------|
| `review_id` | INTEGER PK | |
| `entity_type` | TEXT | 'lemma', 'sense', 'morpheme', 'wordform' |
| `entity_id` | TEXT | FK to relevant table |
| `reason` | TEXT | Why review is needed |
| `priority` | TEXT | 'high', 'medium', 'low' |
| `assigned_to` | TEXT | |
| `status` | TEXT | 'open', 'resolved', 'wontfix' |
| `resolution` | TEXT | What was done |
| `created_at` | TEXT | ISO timestamp |
| `resolved_at` | TEXT | |

### 12. `provenance`

Track where data came from and confidence levels.

| Column | Type | Description |
|--------|------|-------------|
| `provenance_id` | INTEGER PK | |
| `entity_type` | TEXT | |
| `entity_id` | TEXT | |
| `source` | TEXT | 'analyzer', 'manual', 'bootstrap_lexicon', 'kjv_alignment' |
| `confidence` | REAL | 0.0 - 1.0 |
| `evidence` | TEXT | Supporting evidence |
| `created_at` | TEXT | |
| `updated_at` | TEXT | |

---

## ID Conventions

Stable IDs are essential for cross-referencing and external tools.

| Entity | ID Format | Example |
|--------|-----------|---------|
| Source | `{BBCCCVVV}` | `01001001` |
| Wordform | `{normalized}` | `kapaiding` |
| Lemma | `{citation_form}` | `pai` |
| Sense | `{lemma_id}.{n}` | `pai.1` |
| Morpheme | `{form}.{gloss}.{cat}` | `in.ERG.case_marker` |
| Construction | `{name_snake_case}` | `serial_verb_motion` |
| Topic | `{name_snake_case}` | `tam_markers` |

---

## Relationships

```
sources ──1:N──▶ tokens ──N:1──▶ wordforms ──N:1──▶ lemmas
                                     │                  │
                                     │                  ├──1:N──▶ senses
                                     │                  │
                                     └──────────────────┴──1:N──▶ examples
                                                                    │
grammatical_morphemes ◀──N:1─────────────────────────────────────────┘
        │
        └──1:N──▶ constructions ──N:N──▶ grammar_topics
```

---

## Usage Type Classification

The `usage_type` field distinguishes how a form is used:

| Value | Description | Example |
|-------|-------------|---------|
| `lexical` | Content word (noun, verb, adj) | `pa` = 'male' |
| `grammatical` | Function word / affix | `in` = ERG |
| `mixed` | Both uses attested | `hi` = 'be' (V) + DECL (particle) |

For `mixed` forms, the sense table captures each usage separately:

```
lemmas: hi (entry_type='mixed')
  └── senses:
       ├── hi.1 (usage_type='grammatical', gloss='DECL')
       └── hi.2 (usage_type='lexical', gloss='be')
```

---

## Status Values

### Entry/Item Status

| Value | Meaning |
|-------|---------|
| `auto` | Machine-generated, not reviewed |
| `reviewed` | Manually checked, confirmed correct |
| `needs_review` | Flagged for manual attention |
| `clean` | Production-ready |
| `draft` | Work in progress |
| `unsafe_gloss` | Gloss uncertain or incomplete |

### Review Priority

| Value | Meaning |
|-------|---------|
| `high` | Frequent form, blocking other work |
| `medium` | Important but not urgent |
| `low` | Can defer |

---

## Migration Path

### From Current TSV Exports

The existing `data/ctd_analysis/*.tsv` files map to backend tables:

| Current File | Backend Table(s) | Notes |
|--------------|------------------|-------|
| `verses.tsv` | `sources` | Full migration |
| `tokens.tsv` | `tokens` | Full migration (~831K rows) |
| `wordforms.tsv` | `wordforms` | Full migration (~22K rows) |
| `lemmas.tsv` | `lemmas` | Full migration |
| `senses.tsv` | `senses` | Full migration |
| `grammatical_morphemes.tsv` | `grammatical_morphemes` | Full migration |
| `examples.tsv` | `examples` | With morpheme_id derivation |
| `ambiguities.tsv` | `review_queue` | Filtered to needs_review |

### Morpheme-Example Linking

During migration, `examples.morpheme_id` is derived from the `glossed` field:
1. Parse the gloss string for grammatical morpheme patterns
2. Match against known morphemes in `grammatical_morphemes`
3. Unmatched morpheme examples are flagged for review
4. Additional examples are auto-generated from corpus for under-represented morphemes

### Build Process

```
analyze_morphemes.py (analyzer)
        │
        ▼
export_tedim_analysis.py
        │
        └──▶ data/ctd_analysis/*.tsv (intermediate exports)
                │
                ▼
        backend.py migrate
                │
                └──▶ data/ctd_backend.db (generated, not committed)
                        │
                        ├──▶ lookup_word.py (dictionary lookup)
                        ├──▶ generate_sample_entries.py (dictionary)
                        └──▶ generate_*_report_backend.py (grammar)
```

### Regenerating the Backend

The database is a generated artifact. To rebuild:

```bash
# Remove old database
rm -f data/ctd_backend.db

# Regenerate from TSV exports
python scripts/backend.py migrate --tsv-dir data/ctd_analysis --db data/ctd_backend.db

# Verify
python scripts/backend.py stats
```
```

---

## Query Examples

### Dictionary: Get lemma with all senses and examples

```sql
SELECT l.*, s.sense_id, s.gloss, s.usage_type, s.frequency
FROM lemmas l
LEFT JOIN senses s ON l.lemma_id = s.lemma_id
WHERE l.lemma_id = 'pai'
ORDER BY s.frequency DESC;

SELECT e.* FROM examples e
WHERE e.sense_id LIKE 'pai.%'
ORDER BY e.quality DESC
LIMIT 5;
```

### Grammar: Get all case markers with examples

```sql
SELECT gm.*, e.source_id, e.tedim_text, e.glossed, e.kjv_text
FROM grammatical_morphemes gm
LEFT JOIN examples e ON gm.morpheme_id = e.morpheme_id
WHERE gm.category = 'case_marker'
ORDER BY gm.frequency DESC, e.quality DESC;
```

### Review: High-priority items

```sql
SELECT rq.*, 
       CASE rq.entity_type 
         WHEN 'lemma' THEN l.primary_gloss
         WHEN 'sense' THEN s.gloss
       END as gloss
FROM review_queue rq
LEFT JOIN lemmas l ON rq.entity_type = 'lemma' AND rq.entity_id = l.lemma_id
LEFT JOIN senses s ON rq.entity_type = 'sense' AND rq.entity_id = s.sense_id
WHERE rq.status = 'open' AND rq.priority = 'high'
ORDER BY rq.created_at;
```

---

## API Surface

The backend will be accessed via a Python module: `scripts/backend.py`

```python
from backend import Backend

db = Backend('data/ctd_backend.db')

# Dictionary lookup
entry = db.get_lemma('pai')
senses = db.get_senses('pai')
examples = db.get_examples_for_sense('pai.1', limit=3)

# Grammar access
markers = db.get_grammatical_morphemes(category='tam_suffix')
examples = db.get_examples_for_morpheme('ding.IRR.tam_suffix')

# Corpus access
verse = db.get_source('41001001')
tokens = db.get_tokens_for_source('41001001')

# Review queue
items = db.get_review_items(priority='high', status='open')
db.resolve_review_item(item_id, resolution='Fixed gloss')
```

---

## Next Steps

1. **Implement `scripts/backend.py`** - SQLite wrapper with query methods
2. **Migrate Tedim data** - Convert TSV exports to SQLite
3. **Refactor `lookup_word.py`** - Read from backend instead of lexicons
4. **Refactor one grammar report** - Read from backend
5. **Document Tedim-specific assumptions** - `docs/GENERALIZATION_NOTES.md`
