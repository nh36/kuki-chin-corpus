#!/usr/bin/env python3
"""
Build a corpus-wide analyzer-based audit for Tedim stem alternation.

Outputs:
    - output/publication_review/stem_alternation_corpus_audit.tsv
    - output/publication_review/stem_alternation_environment_summary.tsv
    - output/publication_review/stem_alternation_pair_summary.tsv
    - output/publication_review/stem_alternation_example_matrix.tsv
    - output/publication_review/stem_alternation_lexical_inventory.tsv

The audit uses the analyzer's stem-pair inventory plus the local Tedim token
export. `data/ctd_analysis/tokens.tsv` remains generated local build output and
is intentionally not tracked in git. The row-level audit is likewise generated
locally, while the smaller summaries and representative example matrix are
intended for git tracking.
"""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = ROOT / "data" / "ctd_analysis" / "tokens.tsv"
VERSES_PATH = ROOT / "data" / "verses_aligned.tsv"
OUTPUT_DIR = ROOT / "output" / "publication_review"
CORPUS_AUDIT_PATH = OUTPUT_DIR / "stem_alternation_corpus_audit.tsv"
ENV_SUMMARY_PATH = OUTPUT_DIR / "stem_alternation_environment_summary.tsv"
PAIR_SUMMARY_PATH = OUTPUT_DIR / "stem_alternation_pair_summary.tsv"
EXAMPLE_MATRIX_PATH = OUTPUT_DIR / "stem_alternation_example_matrix.tsv"
LEXICAL_INVENTORY_PATH = OUTPUT_DIR / "stem_alternation_lexical_inventory.tsv"
CANDIDATES_PATH = OUTPUT_DIR / "candidates_stem_alternation.tsv"
GRAMMAR_PACKET_PATH = OUTPUT_DIR / "grammar_stem_alternation_print_slice.md"
DICTIONARY_PACKET_PATH = OUTPUT_DIR / "dictionary_stem_alternation_print_slice.md"
REVIEW_NOTES_PATH = OUTPUT_DIR / "review_notes_stem_alternation.md"
DOSSIER_PATH = OUTPUT_DIR / "dossier_stem_alternation.md"
STEMS_LIT_REVIEW_PATH = ROOT / "docs" / "grammar" / "lit-reviews" / "05-verb-01-stems-lit.md"

sys.path.insert(0, str(ROOT / "scripts"))
from analyze_morphemes import VERB_STEM_PAIRS  # noqa: E402
from generate_vsa_report import PSC_TO_TEDIM  # noqa: E402


CORPUS_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "attested_form",
    "stem_form",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss",
    "lemma",
    "pos",
    "stem_alternation",
    "prefix_chain",
    "suffix_chain",
    "usage_type",
    "function_type",
    "local_context",
    "kjv",
    "inferred_environment",
    "environment_confidence",
    "print_status",
    "notes",
]

ENV_SUMMARY_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "environment",
    "form_i_count",
    "form_ii_count",
    "total_count",
    "representative_references",
    "notes",
]

PAIR_SUMMARY_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "form_i_total",
    "form_ii_total",
    "total",
    "dominant_form_i_environments",
    "dominant_form_ii_environments",
    "analyzer_status",
    "used_in_print_packet",
    "in_candidate_tsv",
    "candidate_statuses",
    "publication_status",
    "recommendation",
    "notes",
]

EXAMPLE_MATRIX_COLUMNS = [
    "pair_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "stem_side",
    "attested_form",
    "environment",
    "environment_count_for_side",
    "verse_id",
    "reference",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss_span",
    "lemma",
    "pos",
    "local_context",
    "kjv",
    "print_status",
    "selection_reason",
    "notes",
]

LEXICAL_INVENTORY_COLUMNS = [
    "lexeme_id",
    "form_i",
    "form_ii",
    "gloss",
    "alternation_type",
    "source_secondary_literature",
    "source_vsa_questionnaire",
    "source_analyzer_inventory",
    "source_corpus_audit",
    "source_notes",
    "form_i_bible_attested",
    "form_ii_bible_attested",
    "form_i_clean_token_count",
    "form_ii_clean_token_count",
    "form_i_family_count",
    "form_ii_family_count",
    "best_form_i_examples",
    "best_form_ii_examples",
    "nominalized_examples",
    "dependent_temporal_examples",
    "purpose_examples",
    "relative_or_attributive_examples",
    "negative_examples",
    "finite_predicate_examples",
    "derived_or_causative_examples",
    "compound_or_lexicalized_examples",
    "homophone_or_noise_notes",
    "bible_attestation_profile",
    "lexical_pair_status",
    "recommended_grammar_treatment",
    "print_example_status",
    "notes",
]

REVIEW_CITED_SAFE_ENVIRONMENTS = {
    "finite_main_or_matrix",
    "dependent_temporal_ciangin",
    "dependent_temporal_ni_in",
    "clause_linking_kipan",
    "nominalized_na",
    "possessed_or_genitive_attributive",
    "relative_or_attributive_mi",
}

OBVIOUS_NOISY_ROW_FORMS = {
    "luimu",
    "muhdah",
    "mualtung",
    "mukte",
    "ngaihsun",
    "ngaihsut",
    "ngaihsutna",
    "ngaihsutna-in",
    "piangsak",
    "piangkhiasak",
    "piangsakin",
    "honkhia",
    "honkhiat",
    "hu",
    "huh",
}

MANUAL_REVIEW_ROW_ALLOWLIST = {
    ("mu-muh", "01019001", "20"): "print_usable_with_caveat",
    ("za-zak", "01003008", "13"): "print_usable_with_caveat",
    ("pia-piak", "01004005", "5"): "print_usable_with_caveat",
    ("nusia-nusiat", "01002024", "10"): "print_usable_with_caveat",
}

MANUAL_PUBLICATION_STATUS = {
    "mu-muh": "print_ready",
    "ne-nek": "print_ready",
    "nei-neih": "print_ready",
    "za-zak": "print_usable_with_caveat",
    "pia-piak": "print_usable_with_caveat",
    "nusia-nusiat": "print_usable_with_caveat",
    "thei-theih": "dossier_only",
    "piang-pian": "dossier_only",
    "ngai-ngaih": "dossier_only",
    "honkhia-honkhiat": "exclude_for_now",
    "hu-huh": "exclude_for_now",
}

LEXICAL_PAIR_STATUS_OVERRIDES = {
    "mu-muh": "established_pair",
    "ne-nek": "established_pair",
    "nei-neih": "established_pair",
    "za-zak": "established_pair",
    "pia-piak": "established_pair",
    "nusia-nusiat": "likely_pair",
    "thei-theih": "established_pair",
    "piang-pian": "likely_pair",
    "ngai-ngaih": "likely_pair",
    "honkhia-honkhiat": "lexicalized_or_category_mixed",
    "hu-huh": "lexicalized_or_category_mixed",
}

GRAMMAR_TREATMENT_OVERRIDES = {
    "mu-muh": "core_paradigm_example",
    "ne-nek": "core_paradigm_example",
    "nei-neih": "core_paradigm_example",
    "za-zak": "ordinary_inventory_entry",
    "pia-piak": "ordinary_inventory_entry",
    "nusia-nusiat": "ordinary_inventory_entry",
    "thei-theih": "discuss_under_modal_or_constructional_complexity",
    "piang-pian": "discuss_under_nominalization_or_dependent_clauses",
    "ngai-ngaih": "discuss_under_lexicalized_or_excluded_forms",
    "honkhia-honkhiat": "discuss_under_lexicalized_or_excluded_forms",
    "hu-huh": "discuss_under_lexicalized_or_excluded_forms",
}

PRINT_STATUS_RANK = {
    "print_ready": 5,
    "print_usable_with_caveat": 4,
    "dossier_only": 3,
    "needs_analyzer_review": 2,
    "exclude_for_now": 1,
}

ENVIRONMENT_PRIORITY = {
    "finite_main_or_matrix": 9,
    "imperative_or_directive": 8,
    "dependent_temporal_ciangin": 7,
    "dependent_temporal_ni_in": 7,
    "clause_linking_kipan": 7,
    "nominalized_na": 6,
    "relative_or_attributive_mi": 5,
    "possessed_or_genitive_attributive": 5,
    "purpose_nadingin": 4,
    "negative_clause": 3,
    "modal_or_ability": 2,
    "quotative_or_say_complement": 1,
    "unknown_or_needs_review": 0,
    "causative_or_derivational_sak": -1,
    "compound_or_lexicalized": -2,
}

SECONDARY_LITERATURE_PAIR_IDS = {
    "mu-muh",
    "ne-nek",
    "nei-neih",
    "ngai-ngaih",
    "thei-theih",
    "za-zak",
    "pia-piak",
    "piang-pian",
    "nusia-nusiat",
    "honkhia-honkhiat",
    "hu-huh",
    "pai-pai",
    "si-sit",
}

SUPPLEMENTAL_PACKET_PAIRS = {
    "piang-pian": ("piang", "pian", "be.born"),
    "hu-huh": ("hu", "huh", "help"),
}

CANDIDATE_ALIASES = {
    "pia-piak-report-noise": "pia-piak",
    "ngai-ngaih-family": "ngai-ngaih",
}

NOISY_FORM_OVERRIDES = {
    "piangsak": "piang-pian",
    "piangkhiasak": "piang-pian",
    "piangsakin": "piang-pian",
    "ngaihsun": "ngai-ngaih",
    "ngaihsut": "ngai-ngaih",
    "ngaihsutna": "ngai-ngaih",
    "ngaihsutna-in": "ngai-ngaih",
    "neihsak": "nei-neih",
}

FORM_I_NOTE_PRIORITY = {
    "mu-muh": 10,
    "ne-nek": 10,
    "za-zak": 9,
    "pia-piak": 9,
    "nusia-nusiat": 9,
}


@dataclass(frozen=True)
class PairMeta:
    pair_id: str
    form_i: str
    form_ii: str
    gloss: str
    alternation_type: str
    analyzer_status: str
    used_in_print_packet: bool
    in_candidate_tsv: bool
    candidate_statuses: tuple[str, ...]
    publication_status: str
    notes: str


def require_tokens_export() -> None:
    if TOKENS_PATH.exists():
        return
    raise SystemExit(
        "Missing data/ctd_analysis/tokens.tsv. Run `python3 scripts/export_tedim_analysis.py` "
        "before building the stem alternation corpus audit."
    )


def clean(text: str) -> str:
    return text.lower().strip("“”\"'.,;:!?()[]{}")


def split_chain(text: str) -> list[str]:
    return [part for part in clean(text).split("-") if part]


def alternation_type(form_i: str, form_ii: str) -> str:
    if form_ii == f"{form_i}h":
        return "+h"
    if form_ii == f"{form_i}k":
        return "+k"
    if form_ii == f"{form_i}t":
        return "+t"
    if form_i.endswith("ng") and form_ii == form_i[:-1]:
        return "-ng > -n"
    return "other / irregular / uncertain"


def load_candidate_statuses() -> tuple[
    dict[str, set[str]],
    dict[str, bool],
    dict[str, set[str]],
    dict[str, dict[str, set[str]]],
]:
    statuses: dict[str, set[str]] = defaultdict(set)
    present: dict[str, bool] = defaultdict(bool)
    references: dict[str, set[str]] = defaultdict(set)
    reference_statuses: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    if not CANDIDATES_PATH.exists():
        return statuses, present, references, reference_statuses

    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            construction_id = row["construction_id"]
            pair_id = CANDIDATE_ALIASES.get(construction_id, construction_id)
            if "~" in pair_id:
                pair_id = pair_id.replace(" ~ ", "-").replace("~", "-")
            if pair_id in {"mu-muh", "ne-nek", "nei-neih", "pia-piak", "za-zak", "nusia-nusiat", "thei-theih", "piang-pian", "ngai-ngaih", "honkhia-honkhiat"}:
                present[pair_id] = True
                statuses[pair_id].add(row["candidate_status"])
                references[pair_id].add(row["reference"])
                reference_statuses[pair_id][row["reference"]].add(row["candidate_status"])
    return statuses, present, references, reference_statuses


def load_print_packet_text() -> str:
    text_parts = []
    for path in (GRAMMAR_PACKET_PATH, DICTIONARY_PACKET_PATH, REVIEW_NOTES_PATH):
        text_parts.append(path.read_text(encoding="utf-8") if path.exists() else "")
    return "\n".join(text_parts)


def load_review_bundle_text() -> str:
    text_parts = []
    for path in (DOSSIER_PATH, GRAMMAR_PACKET_PATH, DICTIONARY_PACKET_PATH, REVIEW_NOTES_PATH):
        text_parts.append(path.read_text(encoding="utf-8") if path.exists() else "")
    return "\n".join(text_parts)


def extract_exact_review_references(text: str) -> set[str]:
    references = set()
    with VERSES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            reference = row["reference"]
            if re.search(rf"(?<![0-9A-Za-z]){re.escape(reference)}(?![0-9])", text):
                references.add(reference)
    return references


def build_pair_inventory() -> dict[str, PairMeta]:
    candidate_statuses, in_candidate, _, _ = load_candidate_statuses()
    print_packet_text = load_print_packet_text()

    pairs: dict[str, PairMeta] = {}

    for form_ii, (form_i, gloss) in sorted(VERB_STEM_PAIRS.items()):
        pair_id = f"{form_i}-{form_ii}"
        pair_phrase = f"`{form_i} ~ {form_ii}`"
        publication_status = MANUAL_PUBLICATION_STATUS.get(pair_id, "needs_analyzer_review")
        pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=form_i,
            form_ii=form_ii,
            gloss=gloss,
            alternation_type=alternation_type(form_i, form_ii),
            analyzer_status="known_to_analyzer",
            used_in_print_packet=pair_phrase in print_packet_text,
            in_candidate_tsv=in_candidate.get(pair_id, False),
            candidate_statuses=tuple(sorted(candidate_statuses.get(pair_id, set()))),
            publication_status=publication_status,
            notes="",
        )

    for pair_id, (form_i, form_ii, gloss) in SUPPLEMENTAL_PACKET_PAIRS.items():
        if pair_id in pairs:
            continue
        pair_phrase = f"`{form_i} ~ {form_ii}`"
        pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=form_i,
            form_ii=form_ii,
            gloss=gloss,
            alternation_type=alternation_type(form_i, form_ii),
            analyzer_status="packet_pair_not_in_VERB_STEM_PAIRS",
            used_in_print_packet=pair_phrase in print_packet_text,
            in_candidate_tsv=in_candidate.get(pair_id, False),
            candidate_statuses=tuple(sorted(candidate_statuses.get(pair_id, set()))),
            publication_status=MANUAL_PUBLICATION_STATUS.get(pair_id, "needs_analyzer_review"),
            notes="Present in the stem packet, but absent from VERB_STEM_PAIRS.",
        )

    return pairs


def load_verse_metadata() -> dict[str, dict[str, str]]:
    csv.field_size_limit(10**7)
    verses: dict[str, dict[str, str]] = {}
    with VERSES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            verses[row["verse_id"]] = {
                "reference": row["reference"],
                "tedim": row["ctd_Tedim Chin"],
                "kjv": row["eng_King James Version"],
            }
    return verses


def iter_tokens_by_verse():
    csv.field_size_limit(10**7)
    with TOKENS_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        current_verse = None
        bucket: list[dict[str, str]] = []
        for row in reader:
            verse_id = row["verse_id"]
            if current_verse is None:
                current_verse = verse_id
            if verse_id != current_verse:
                yield current_verse, bucket
                current_verse = verse_id
                bucket = []
            bucket.append(row)
        if current_verse is not None:
            yield current_verse, bucket


def count_form_ii_hits(pairs: dict[str, PairMeta]) -> Counter:
    counts: Counter = Counter()
    form_ii_index = {meta.form_ii: meta.pair_id for meta in pairs.values()}
    for _, verse_tokens in iter_tokens_by_verse():
        for row in verse_tokens:
            normalized = clean(row["normalized_form"])
            stem = clean(row["stem_form"])
            seg_parts = split_chain(row["segmentation"])
            compact = "".join(seg_parts)
            for candidate in {normalized, stem, compact, *seg_parts}:
                pair_id = form_ii_index.get(candidate)
                if pair_id:
                    counts[pair_id] += 1
                    break
    return counts


def build_indexes(pairs: dict[str, PairMeta], form_ii_counts: Counter):
    form_i_index: dict[str, list[str]] = defaultdict(list)
    form_ii_index: dict[str, str] = {}
    for pair_id, meta in pairs.items():
        form_i_index[meta.form_i].append(pair_id)
        form_ii_index[meta.form_ii] = pair_id

    canonical_by_form_i: dict[str, str] = {}
    for form_i, pair_ids in form_i_index.items():
        if len(pair_ids) == 1:
            canonical_by_form_i[form_i] = pair_ids[0]
            continue
        canonical_by_form_i[form_i] = max(
            pair_ids,
            key=lambda pair_id: (
                form_ii_counts[pair_id],
                FORM_I_NOTE_PRIORITY.get(pair_id, 0),
                pair_id,
            ),
        )
    return form_i_index, form_ii_index, canonical_by_form_i


def pair_override_for_row(row: dict[str, str]) -> str | None:
    normalized = clean(row["normalized_form"])
    if normalized in NOISY_FORM_OVERRIDES:
        return NOISY_FORM_OVERRIDES[normalized]
    if normalized.startswith("ngaihs"):
        return "ngai-ngaih"
    if normalized.startswith("piangsak") or normalized.startswith("piangkhia"):
        return "piang-pian"
    if normalized.startswith("neihsak"):
        return "nei-neih"
    return None


def resolve_pair_id(
    row: dict[str, str],
    form_i_index: dict[str, list[str]],
    form_ii_index: dict[str, str],
    canonical_by_form_i: dict[str, str],
) -> tuple[str | None, str]:
    override = pair_override_for_row(row)
    if override:
        return override, "pair inferred from known noisy or derived family."

    normalized = clean(row["normalized_form"])
    stem = clean(row["stem_form"])
    lemma = clean(row["lemma"])
    seg_parts = split_chain(row["segmentation"])
    compact = "".join(seg_parts)

    for candidate in (stem, normalized, compact, *seg_parts):
        pair_id = form_ii_index.get(candidate)
        if pair_id:
            return pair_id, ""

    for candidate in (stem, normalized, lemma, compact, *seg_parts):
        pair_ids = form_i_index.get(candidate, [])
        if not pair_ids:
            continue
        if len(pair_ids) == 1:
            return pair_ids[0], ""
        canonical = canonical_by_form_i[candidate]
        others = sorted(pair_id for pair_id in pair_ids if pair_id != canonical)
        note = (
            f"Form I stem `{candidate}` participates in multiple analyzer pairs "
            f"({', '.join(pair_ids)}); counted under canonical pair {canonical}."
        )
        if others:
            note += f" Alternate Form II analyses remain visible in pair summary notes: {', '.join(others)}."
        return canonical, note

    return None, ""


def infer_attested_form(row: dict[str, str], pair: PairMeta) -> tuple[str, str, str]:
    normalized = clean(row["normalized_form"])
    stem = clean(row["stem_form"])
    seg_parts = split_chain(row["segmentation"])
    compact = "".join(seg_parts)
    suffix_parts = split_chain(row["suffix_chain"])
    export_alt = row["stem_alternation"].strip()

    if pair.form_ii in {normalized, stem, compact, *seg_parts}:
        return pair.form_ii, export_alt or "II", ""

    if pair.alternation_type in {"+h", "+k", "+t"} and stem == pair.form_i and suffix_parts:
        added = pair.form_ii[len(pair.form_i):]
        if suffix_parts[0] == added and normalized.startswith(pair.form_ii):
            return pair.form_ii, export_alt or "II", "stem alternation inferred from suffix chain."

    if pair.form_i in {normalized, stem, compact, *seg_parts}:
        return pair.form_i, export_alt or "I", ""

    if export_alt == "II":
        return pair.form_ii, "II", "stem alternation inferred from export metadata."
    if export_alt == "I":
        return pair.form_i, "I", "stem alternation inferred from export metadata."

    return normalized or stem, export_alt, "token belongs to the pair family but is not a simple Form I/II token."


def local_context(tokens: list[dict[str, str]], index: int, width: int = 3) -> str:
    start = max(0, index - width)
    end = min(len(tokens), index + width + 1)
    parts = []
    for offset, row in enumerate(tokens[start:end], start=start):
        token = row["surface_form"]
        if offset == index:
            parts.append(f"[{token}]")
        else:
            parts.append(token)
    return " ".join(parts)


def token_normalized(tokens: list[dict[str, str]], index: int) -> str:
    if 0 <= index < len(tokens):
        return clean(tokens[index]["normalized_form"])
    return ""


def token_pos(tokens: list[dict[str, str]], index: int) -> str:
    if 0 <= index < len(tokens):
        return tokens[index]["pos"]
    return ""


def infer_environment(
    tokens: list[dict[str, str]],
    index: int,
    pair: PairMeta,
    row: dict[str, str],
) -> tuple[str, str, str]:
    normalized = clean(row["normalized_form"])
    segmentation = row["segmentation"].lower()
    suffix_parts = split_chain(row["suffix_chain"])
    prev2 = token_normalized(tokens, index - 2)
    prev1 = token_normalized(tokens, index - 1)
    next1 = token_normalized(tokens, index + 1)
    next2 = token_normalized(tokens, index + 2)

    if normalized in {"ngaihsun", "ngaihsut", "ngaihsutna", "ngaihsutna-in"} or normalized.startswith("ngaihs"):
        return "compound_or_lexicalized", "high", "The dossier treats the `ngaihsun/ngaihsut` family as lexical-family contamination rather than clean `ngaih` evidence."

    if pair.pair_id in {"honkhia-honkhiat", "hu-huh"}:
        return "compound_or_lexicalized", "high", "This pair is currently treated as lexicalized or category-mixed rather than as simple stem evidence."

    if "sak" in suffix_parts or normalized.endswith("sak") or normalized.endswith("sakin") or "-sak" in segmentation:
        return "causative_or_derivational_sak", "high", "Causative or derivational `sak` blocks promotion as simple stem-alternation evidence."

    if next1 in {"ciangin", "ciang-in"}:
        return "dependent_temporal_ciangin", "high", "Immediate following `ciangin` provides a conservative dependent-temporal cue."

    if next1 in {"ni-in", "niin"} or (next1 == "ni" and next2 == "in"):
        return "dependent_temporal_ni_in", "high", "Immediate following `ni-in` provides a conservative dependent-temporal cue."

    if next1 == "kipan" or (next1 == "a" and next2 == "kipan"):
        return "clause_linking_kipan", "high", "Local `a kipan` sequence marks a clause-linking or source/beginning environment."

    if normalized in {"nadingin", "dinga", "dingin"} or next1 in {"nadingin", "dinga", "dingin"} or next2 == "nadingin":
        return "purpose_nadingin", "medium", "Local `ding` or `nadingin` material suggests a purpose or irrealis-heavy environment."

    if "na" in suffix_parts or segmentation.endswith("-na") or "-na-" in segmentation:
        return "nominalized_na", "high", "Suffixal `-na` in the analyzer segmentation supports a nominalized environment."

    if next1 == "mi" and token_pos(tokens, index - 1) in {"PROP", "PRON", "N"}:
        return "possessed_or_genitive_attributive", "medium", "A following `mi` plus a preceding possessor-like token suggests an attributive or possessed nominal environment."

    if next1 == "mi":
        return "relative_or_attributive_mi", "medium", "A following `mi` suggests a relative-like or attributive nominal environment."

    if any(token in {"lo", "loh", "kei"} for token in (prev2, prev1, next1, next2)):
        return "negative_clause", "medium", "Nearby negative material marks a negative or irrealis-heavy clause."

    if pair.pair_id == "thei-theih" and (next1 in {"ding", "lo", "mi"} or next2 in {"ding", "nadingin"}):
        return "modal_or_ability", "medium", "The `thei/theih` pair often surfaces in modal or ability-heavy contexts."

    if any(token in {"ci", "ci-in", "cih", "leh"} for token in (prev1, next1, next2)):
        return "quotative_or_say_complement", "low", "Nearby quotative material suggests embedded or reported-speech structure."

    if next1 in {"un", "in"}:
        return "imperative_or_directive", "low", "A following imperative-like particle may indicate directive force."

    if row["pos"] in {"V", "FUNC"} or next1 in {"hi", "uh", "ding"}:
        return "finite_main_or_matrix", "medium", "No stronger local cue was found, so the token is kept in a conservative finite or matrix bucket."

    return "unknown_or_needs_review", "low", "No conservative local environment rule fired for this token."

def recommendation_for_pair(
    pair: PairMeta,
    form_i_total: int,
    form_ii_total: int,
    dominant_form_ii_envs: list[str],
) -> str:
    if pair.publication_status in {"print_ready", "print_usable_with_caveat", "dossier_only", "exclude_for_now"}:
        if pair.publication_status == "dossier_only":
            return "interpretive_revision_of_slice"
        if pair.publication_status == "exclude_for_now":
            return "keep_excluded"
        return "interpretive_revision_of_slice"
    if pair.analyzer_status == "packet_pair_not_in_VERB_STEM_PAIRS":
        return "needs_analyzer_review"
    if form_ii_total == 0:
        return "needs_analyzer_review"
    if dominant_form_ii_envs and all(env in {"compound_or_lexicalized", "causative_or_derivational_sak"} for env in dominant_form_ii_envs):
        return "exclude_for_now"
    if form_i_total > 0 and form_ii_total > 0:
        return "candidate_for_expansion"
    return "needs_analyzer_review"


def join_top(counter: Counter, limit: int = 3) -> str:
    if not counter:
        return ""
    return "; ".join(f"{name}:{count}" for name, count in counter.most_common(limit))


def analysis_clarity_score(row: dict[str, str]) -> int:
    score = 0
    if row["segmentation"].strip() and row["segmentation"] not in {"?", "-"}:
        score += 1
    if row["lemma"].strip() and row["lemma"] not in {"?", "-"}:
        score += 1
    if row["pos"].strip() and row["pos"] not in {"UNK", "X", "?"}:
        score += 1
    if "inferred from export metadata" not in row["notes"] and "token belongs to the pair family" not in row["notes"]:
        score += 1
    return score


def selection_priority(
    row: dict[str, str],
    accepted_candidate_row_keys: set[tuple[str, str, str]],
    review_references: set[str],
    order_index: int,
) -> tuple[int, int, int, int, int]:
    row_key = (row["pair_id"], row["verse_id"], row["token_index"])
    return (
        1 if row["environment"] != "unknown_or_needs_review" else 0,
        analysis_clarity_score(row),
        2 if row_key in accepted_candidate_row_keys else 1 if row_key in MANUAL_REVIEW_ROW_ALLOWLIST or row["reference"] in review_references else 0,
        -len(row["local_context"].split()),
        -order_index,
    )


def build_selection_reason(
    row: dict[str, str],
    candidate_row_keys: set[tuple[str, str, str]],
    review_references: set[str],
) -> str:
    reasons = []
    row_key = (row["pair_id"], row["verse_id"], row["token_index"])
    if row_key in candidate_row_keys:
        reasons.append("preferred because this exact token is already part of an accepted candidate TSV row")
    elif row_key in MANUAL_REVIEW_ROW_ALLOWLIST:
        reasons.append("preferred because this exact row is manually retained as caveated evidence in the packet")
    elif row["reference"] in review_references:
        reasons.append("preferred because this verse is already cited in the dossier or packet")

    if row["environment"] == "unknown_or_needs_review":
        reasons.append("retained as the clearest available review-bucket example for this pair and stem side")
    else:
        reasons.append("kept as the clearest analyzed example for this pair, stem side, and environment")

    if analysis_clarity_score(row) >= 3:
        reasons.append("analyzer segmentation and POS are explicit enough for write-up use")

    return "; ".join(reasons)


def row_has_obvious_contamination(pair: PairMeta, row: dict[str, str]) -> tuple[bool, str]:
    normalized = clean(row["normalized_form"])
    surface = clean(row["surface_form"])
    segmentation = clean(row["segmentation"])
    if normalized in OBVIOUS_NOISY_ROW_FORMS or surface in OBVIOUS_NOISY_ROW_FORMS:
        return True, "Surface form belongs to a noisy lexicalized or compound family rather than to a clean print-safe stem token."
    if normalized.startswith("ngaihs") or normalized.startswith("piangsak") or normalized.startswith("piangkhia"):
        return True, "Surface form belongs to a derived or lexical-family cluster rather than to a clean stem alternation example."
    if pair.pair_id == "mu-muh" and ("muh-dah" in segmentation or "lui-mu" in segmentation):
        return True, "This `mu/muh` family row is lexicalized or compounded rather than a clean print-safe stem token."
    if "pair inferred from known noisy or derived family." in row["notes"]:
        return True, "Row was attached to the pair through a known noisy or derived-family override."
    if "token belongs to the pair family but is not a simple Form I/II token." in row["notes"]:
        return True, "Row belongs to the stem family, but not as a simple Form I or Form II token."
    return False, ""


def load_accepted_candidate_row_keys(pairs: dict[str, PairMeta]) -> set[tuple[str, str, str]]:
    accepted_keys: set[tuple[str, str, str]] = set()
    if not CANDIDATES_PATH.exists():
        return accepted_keys

    token_lookup: dict[tuple[str, str], dict[str, str]] = {}
    for _, verse_tokens in iter_tokens_by_verse():
        for token_row in verse_tokens:
            token_lookup[(token_row["verse_id"], token_row["token_index"])] = token_row

    with CANDIDATES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            if row["candidate_status"] != "accepted":
                continue
            pair_id = CANDIDATE_ALIASES.get(row["construction_id"], row["construction_id"])
            if "~" in pair_id:
                pair_id = pair_id.replace(" ~ ", "-").replace("~", "-")
            pair = pairs.get(pair_id)
            if pair is None:
                continue
            for token_index in [part.strip() for part in row["token_indices"].split(",") if part.strip()]:
                token_row = token_lookup.get((row["verse_id"], token_index))
                if token_row is None:
                    continue
                attested_form, stem_alt, attested_note = infer_attested_form(token_row, pair)
                if stem_alt in {"I", "II"} and attested_form in {pair.form_i, pair.form_ii} and not attested_note:
                    accepted_keys.add((pair_id, row["verse_id"], token_index))
    return accepted_keys


def merge_notes(*parts: str) -> str:
    merged = []
    seen = set()
    for part in parts:
        text = part.strip()
        if not text or text in seen:
            continue
        seen.add(text)
        merged.append(text)
    return " ".join(merged)


def load_tsv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def load_questionnaire_inventory() -> dict[str, dict[str, str]]:
    inventory: dict[str, dict[str, str]] = {}
    for psc_label, (form_i, form_ii, gloss) in sorted(PSC_TO_TEDIM.items()):
        pair_id = f"{form_i}-{form_ii}"
        inventory[pair_id] = {
            "pair_id": pair_id,
            "psc_label": psc_label,
            "form_i": form_i,
            "form_ii": form_ii,
            "gloss": gloss,
        }
    return inventory


def exact_match_candidates(row: dict[str, str]) -> set[str]:
    segmentation_compact = "".join(split_chain(row.get("segmentation", "")))
    return {
        clean(row.get("normalized_form", "")),
        segmentation_compact,
    } - {""}


def row_matches_exact_form(row: dict[str, str], form: str) -> bool:
    return form in exact_match_candidates(row)


def is_clean_bare_stem_row(row: dict[str, str], form: str) -> bool:
    if clean(row.get("attested_form", "")) != form:
        return False
    if row.get("stem_alternation", "") not in {"I", "II"}:
        return False
    if row.get("inferred_environment", "") in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return False
    notes = row.get("notes", "")
    if "pair inferred from known noisy or derived family." in notes:
        return False
    if "token belongs to the pair family but is not a simple Form I/II token." in notes:
        return False
    return row_matches_exact_form(row, form)


def inventory_row_priority(row: dict[str, str], form: str) -> tuple[int, int, int, int, str, int]:
    return (
        PRINT_STATUS_RANK.get(row.get("print_status", ""), 0),
        1 if is_clean_bare_stem_row(row, form) else 0,
        ENVIRONMENT_PRIORITY.get(row.get("inferred_environment", ""), -3),
        analysis_clarity_score(row),
        row.get("reference", ""),
        -int(row.get("token_index", "0") or 0),
    )


def format_inventory_example(row: dict[str, str]) -> str:
    form = row.get("surface_form") or row.get("attested_form") or row.get("normalized_form")
    environment = row.get("inferred_environment", "")
    status = row.get("print_status", "")
    return f"{row.get('reference', '')} `{form}` [{environment}; {status}]"


def choose_inventory_examples(
    rows: list[dict[str, str]],
    form: str,
    *,
    stem_alts: set[str] | None = None,
    environments: set[str] | None = None,
    limit: int = 3,
) -> str:
    filtered = []
    for row in rows:
        if stem_alts and row.get("stem_alternation", "") not in stem_alts:
            continue
        if environments and row.get("inferred_environment", "") not in environments:
            continue
        if form and clean(row.get("attested_form", "")) not in {form, ""} and not row_matches_exact_form(row, form):
            continue
        filtered.append(row)

    ordered = sorted(filtered, key=lambda item: inventory_row_priority(item, form), reverse=True)
    seen = set()
    chosen = []
    for row in ordered:
        key = (row.get("reference", ""), row.get("token_index", ""))
        if key in seen:
            continue
        seen.add(key)
        chosen.append(format_inventory_example(row))
        if len(chosen) >= limit:
            break
    return "; ".join(chosen)


def scan_questionnaire_only_rows(
    entries: dict[str, dict[str, str]],
    verses: dict[str, dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    if not entries:
        return {}

    form_index: dict[str, list[tuple[str, str]]] = defaultdict(list)
    pseudo_pairs: dict[str, PairMeta] = {}
    for pair_id, entry in entries.items():
        pseudo_pairs[pair_id] = PairMeta(
            pair_id=pair_id,
            form_i=entry["form_i"],
            form_ii=entry["form_ii"],
            gloss=entry["gloss"],
            alternation_type=alternation_type(entry["form_i"], entry["form_ii"]),
            analyzer_status="questionnaire_only",
            used_in_print_packet=False,
            in_candidate_tsv=False,
            candidate_statuses=(),
            publication_status="needs_analyzer_review",
            notes="Questionnaire-only exact-form scan; not part of the analyzer pair inventory.",
        )
        form_index[entry["form_i"]].append((pair_id, "I"))
        if entry["form_ii"] != entry["form_i"]:
            form_index[entry["form_ii"]].append((pair_id, "II"))

    rows_by_pair: dict[str, list[dict[str, str]]] = defaultdict(list)
    for verse_id, verse_tokens in iter_tokens_by_verse():
        verse_meta = verses.get(verse_id)
        if verse_meta is None:
            continue

        for index, row in enumerate(verse_tokens):
            candidates = exact_match_candidates(row)
            if not candidates:
                continue

            hits: dict[str, str] = {}
            for candidate in candidates:
                for pair_id, stem_alt in form_index.get(candidate, []):
                    if stem_alt == "II" or pair_id not in hits:
                        hits[pair_id] = stem_alt

            for pair_id, stem_alt in hits.items():
                pair = pseudo_pairs[pair_id]
                environment, env_confidence, env_note = infer_environment(verse_tokens, index, pair, row)
                print_status = "exclude_for_now" if environment in {"causative_or_derivational_sak", "compound_or_lexicalized"} else "needs_analyzer_review"
                rows_by_pair[pair_id].append(
                    {
                        "pair_id": pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "attested_form": pair.form_i if stem_alt == "I" else pair.form_ii,
                        "stem_form": row["stem_form"],
                        "verse_id": verse_id,
                        "reference": verse_meta["reference"],
                        "token_index": row["token_index"],
                        "surface_form": row["surface_form"],
                        "normalized_form": row["normalized_form"],
                        "segmentation": row["segmentation"],
                        "gloss": row["gloss"],
                        "lemma": row["lemma"],
                        "pos": row["pos"],
                        "stem_alternation": stem_alt,
                        "prefix_chain": row["prefix_chain"],
                        "suffix_chain": row["suffix_chain"],
                        "usage_type": row["usage_type"],
                        "function_type": row["function_type"],
                        "local_context": local_context(verse_tokens, index),
                        "kjv": verse_meta["kjv"],
                        "inferred_environment": environment,
                        "environment_confidence": env_confidence,
                        "print_status": print_status,
                        "notes": merge_notes(
                            pair.notes,
                            env_note,
                            "Questionnaire maps the same surface form to both slots." if pair.form_i == pair.form_ii else "",
                        ),
                    }
                )
    return rows_by_pair


def source_notes_for_inventory_entry(
    pair_id: str,
    form_i: str,
    form_ii: str,
    questionnaire_entry: dict[str, str] | None,
    pair: PairMeta | None,
    form_i_index: dict[str, list[str]],
) -> str:
    notes = []
    if questionnaire_entry is not None:
        notes.append(
            "Questionnaire evidence comes from the in-repo Zakaria/VSA materials; no separate Karius/Kariuss/Karias questionnaire file is present."
        )
        notes.append(f"{questionnaire_entry['psc_label']} -> {form_i}/{form_ii}.")
        if form_i == form_ii:
            notes.append("The questionnaire uses the same written form in both slots.")
        sibling_pairs = sorted(other for other in form_i_index.get(form_i, []) if other != pair_id)
        if sibling_pairs:
            notes.append(f"Analyzer inventory also maps the same Form I base to {', '.join(sibling_pairs)}.")
    if pair is not None and pair.analyzer_status == "packet_pair_not_in_VERB_STEM_PAIRS":
        notes.append("Present in the publication-review packet, but absent from VERB_STEM_PAIRS.")
    if pair_id in SECONDARY_LITERATURE_PAIR_IDS:
        notes.append("Current Henderson/Zam-facing review materials discuss this pair family directly.")
    if questionnaire_entry is not None and pair is not None and questionnaire_entry["gloss"] != pair.gloss:
        notes.append(f"Questionnaire gloss `{questionnaire_entry['gloss']}` and analyzer gloss `{pair.gloss}` differ.")
    return merge_notes(*notes)


def infer_bible_attestation_profile(
    form_i_attested: bool,
    form_ii_attested: bool,
    form_i_clean: int,
    form_ii_clean: int,
    rows: list[dict[str, str]],
) -> str:
    environments = {row.get("inferred_environment", "") for row in rows}
    if not form_i_attested and not form_ii_attested:
        return "not_attested_in_bible"
    if form_i_attested and form_ii_attested:
        if form_i_clean > 0 and form_ii_clean > 0:
            return "both_forms_cleanly_attested"
        if environments <= {"causative_or_derivational_sak", "compound_or_lexicalized"}:
            return "only_noisy_or_lexicalized_attested"
        if environments & {
            "nominalized_na",
            "dependent_temporal_ciangin",
            "dependent_temporal_ni_in",
            "clause_linking_kipan",
            "purpose_nadingin",
            "relative_or_attributive_mi",
            "possessed_or_genitive_attributive",
            "modal_or_ability",
        }:
            return "both_forms_attested_but_complex"
        return "both_forms_attested_but_complex"
    if form_i_attested:
        if form_i_clean > 0:
            return "form_i_only_attested"
        if environments & {"nominalized_na", "purpose_nadingin", "relative_or_attributive_mi", "possessed_or_genitive_attributive"}:
            return "only_derived_or_nominalized_attested"
        return "only_noisy_or_lexicalized_attested"
    if form_ii_clean > 0:
        return "form_ii_only_attested"
    if environments & {
        "nominalized_na",
        "dependent_temporal_ciangin",
        "dependent_temporal_ni_in",
        "clause_linking_kipan",
        "purpose_nadingin",
        "relative_or_attributive_mi",
        "possessed_or_genitive_attributive",
        "modal_or_ability",
    }:
        return "only_derived_or_nominalized_attested"
    return "only_noisy_or_lexicalized_attested"


def infer_lexical_pair_status(
    pair_id: str,
    *,
    source_secondary: bool,
    source_vsa: bool,
    source_analyzer: bool,
    form_i_attested: bool,
    form_ii_attested: bool,
    bible_profile: str,
    form_i: str,
    form_ii: str,
) -> str:
    if pair_id in LEXICAL_PAIR_STATUS_OVERRIDES:
        return LEXICAL_PAIR_STATUS_OVERRIDES[pair_id]
    if bible_profile == "only_noisy_or_lexicalized_attested":
        return "homophone_or_noise_only"
    if form_i == form_ii and source_vsa:
        return "questionnaire_pair_bible_one_sided" if (form_i_attested or form_ii_attested) else "analyzer_pair_needs_review"
    if source_vsa and form_i_attested != form_ii_attested:
        return "questionnaire_pair_bible_one_sided"
    if source_secondary and form_i_attested != form_ii_attested:
        return "literature_pair_bible_one_sided"
    if source_secondary or source_vsa:
        if bible_profile in {"both_forms_cleanly_attested", "both_forms_attested_but_complex"}:
            return "established_pair"
        return "likely_pair"
    if source_analyzer and bible_profile in {"both_forms_cleanly_attested", "both_forms_attested_but_complex"}:
        return "likely_pair"
    if source_analyzer:
        return "analyzer_pair_needs_review"
    return "likely_pair"


def infer_grammar_treatment(
    pair_id: str,
    *,
    lexical_pair_status: str,
    bible_profile: str,
    source_secondary: bool,
    source_vsa: bool,
    rows: list[dict[str, str]],
) -> str:
    if pair_id in GRAMMAR_TREATMENT_OVERRIDES:
        return GRAMMAR_TREATMENT_OVERRIDES[pair_id]
    if lexical_pair_status in {"lexicalized_or_category_mixed", "homophone_or_noise_only"} or bible_profile == "only_noisy_or_lexicalized_attested":
        return "discuss_under_lexicalized_or_excluded_forms"
    if bible_profile == "not_attested_in_bible":
        return "mention_as_literature_or_questionnaire_only" if (source_secondary or source_vsa) else "omit_pending_evidence"
    if bible_profile in {"form_i_only_attested", "form_ii_only_attested"}:
        return "mention_as_literature_or_questionnaire_only" if (source_secondary or source_vsa) else "omit_pending_evidence"
    if any(row.get("inferred_environment", "") == "modal_or_ability" for row in rows):
        return "discuss_under_modal_or_constructional_complexity"
    if any(
        row.get("inferred_environment", "") in {
            "nominalized_na",
            "dependent_temporal_ciangin",
            "dependent_temporal_ni_in",
            "clause_linking_kipan",
            "purpose_nadingin",
            "relative_or_attributive_mi",
            "possessed_or_genitive_attributive",
        }
        for row in rows
    ):
        return "discuss_under_nominalization_or_dependent_clauses"
    return "ordinary_inventory_entry"


def best_available_print_status(pair: PairMeta | None, rows: list[dict[str, str]]) -> str:
    if pair is not None:
        return pair.publication_status
    best = "needs_analyzer_review"
    for row in rows:
        if PRINT_STATUS_RANK.get(row.get("print_status", ""), 0) > PRINT_STATUS_RANK.get(best, 0):
            best = row["print_status"]
    return best


def homophone_or_noise_notes(
    pair_id: str,
    rows: list[dict[str, str]],
    questionnaire_entry: dict[str, str] | None,
    pair: PairMeta | None,
) -> str:
    notes = []
    if pair_id == "ngai-ngaih":
        notes.append("`ngaihsun/ngaihsut/ngaihsutna` remain lexical-family contamination unless a row can be justified independently.")
    if pair_id == "piang-pian":
        notes.append("`piangsak` and related derived rows must not be counted as clean bare Form II evidence.")
    if pair_id in {"honkhia-honkhiat", "hu-huh"}:
        notes.append("Current evidence behaves as lexicalized or category-mixed rather than as a clean pedagogical stem pair.")
    if questionnaire_entry is not None and questionnaire_entry["form_i"] == questionnaire_entry["form_ii"]:
        notes.append("Questionnaire uses a same-form mapping, so Bible tokens do not independently prove a distinct written Form II.")
    blocked_forms = Counter(
        clean(row.get("normalized_form", ""))
        for row in rows
        if row.get("inferred_environment", "") in {"causative_or_derivational_sak", "compound_or_lexicalized"}
    )
    if blocked_forms:
        notes.append(f"Blocked noisy material includes {', '.join(name for name, _ in blocked_forms.most_common(4))}.")
    if pair is not None and pair.form_i == "pua" and pair.form_ii == "puak":
        notes.append("Questionnaire glosses this base as 'carry.on.back', while the analyzer gloss is 'spill'.")
    return merge_notes(*notes)


def write_lexical_inventory(
    pairs: dict[str, PairMeta],
    form_i_index: dict[str, list[str]],
    verses: dict[str, dict[str, str]],
) -> None:
    questionnaire_inventory = load_questionnaire_inventory()
    audit_rows = load_tsv_rows(CORPUS_AUDIT_PATH)
    rows_by_pair: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in audit_rows:
        rows_by_pair[row["pair_id"]].append(row)

    questionnaire_only = {
        pair_id: entry
        for pair_id, entry in questionnaire_inventory.items()
        if pair_id not in pairs
    }
    for pair_id, extra_rows in scan_questionnaire_only_rows(questionnaire_only, verses).items():
        rows_by_pair[pair_id].extend(extra_rows)

    inventory_rows = []
    all_pair_ids = sorted(set(pairs) | set(questionnaire_inventory))
    for pair_id in all_pair_ids:
        pair = pairs.get(pair_id)
        questionnaire_entry = questionnaire_inventory.get(pair_id)
        form_i = pair.form_i if pair is not None else questionnaire_entry["form_i"]
        form_ii = pair.form_ii if pair is not None else questionnaire_entry["form_ii"]
        gloss_parts = []
        if pair is not None and pair.gloss:
            gloss_parts.append(pair.gloss)
        if questionnaire_entry is not None and questionnaire_entry["gloss"] and questionnaire_entry["gloss"] not in gloss_parts:
            gloss_parts.append(questionnaire_entry["gloss"])
        gloss = " / ".join(gloss_parts)

        pair_rows = rows_by_pair.get(pair_id, [])
        form_i_rows = [row for row in pair_rows if row.get("stem_alternation", "") == "I"]
        form_ii_rows = [row for row in pair_rows if row.get("stem_alternation", "") == "II"]
        form_i_clean = sum(1 for row in form_i_rows if is_clean_bare_stem_row(row, form_i))
        form_ii_clean = sum(1 for row in form_ii_rows if is_clean_bare_stem_row(row, form_ii))
        form_i_family = len(form_i_rows)
        form_ii_family = len(form_ii_rows)
        form_i_attested = form_i_family > 0
        form_ii_attested = form_ii_family > 0 and not (questionnaire_entry is not None and form_i == form_ii and pair is None)

        bible_profile = infer_bible_attestation_profile(
            form_i_attested,
            form_ii_attested,
            form_i_clean,
            form_ii_clean,
            pair_rows,
        )
        source_secondary = pair_id in SECONDARY_LITERATURE_PAIR_IDS
        source_vsa = questionnaire_entry is not None
        source_analyzer = pair is not None and pair.analyzer_status == "known_to_analyzer"
        source_corpus = bool(pair_rows)
        lexical_status = infer_lexical_pair_status(
            pair_id,
            source_secondary=source_secondary,
            source_vsa=source_vsa,
            source_analyzer=source_analyzer,
            form_i_attested=form_i_attested,
            form_ii_attested=form_ii_attested,
            bible_profile=bible_profile,
            form_i=form_i,
            form_ii=form_ii,
        )
        grammar_treatment = infer_grammar_treatment(
            pair_id,
            lexical_pair_status=lexical_status,
            bible_profile=bible_profile,
            source_secondary=source_secondary,
            source_vsa=source_vsa,
            rows=pair_rows,
        )
        print_status = best_available_print_status(pair, pair_rows)
        notes = []
        siblings = sorted(other for other in form_i_index.get(form_i, []) if other != pair_id)
        if siblings:
            notes.append(f"Shared Form I base with {', '.join(siblings)}.")
        if source_vsa and questionnaire_entry is not None and questionnaire_entry["form_i"] == questionnaire_entry["form_ii"] and pair is None:
            notes.append("Questionnaire keeps the same written form in both slots, so this row is treated as Form I only for Bible-attestation purposes.")
        if bible_profile == "both_forms_attested_but_complex":
            notes.append("Both forms are attested, but at least one side is clearest in dependent, nominalized, or otherwise non-bare environments.")
        if bible_profile in {"form_i_only_attested", "form_ii_only_attested"}:
            notes.append("Only one stem side is currently attested cleanly in the Bible corpus.")
        if bible_profile == "only_noisy_or_lexicalized_attested":
            notes.append("Current Bible evidence is limited to noisy, lexicalized, or heavily derived material.")

        inventory_rows.append(
            {
                "lexeme_id": pair_id,
                "form_i": form_i,
                "form_ii": form_ii,
                "gloss": gloss,
                "alternation_type": alternation_type(form_i, form_ii),
                "source_secondary_literature": "yes" if source_secondary else "no",
                "source_vsa_questionnaire": "yes" if source_vsa else "no",
                "source_analyzer_inventory": "yes" if source_analyzer else "no",
                "source_corpus_audit": "yes" if source_corpus else "no",
                "source_notes": source_notes_for_inventory_entry(pair_id, form_i, form_ii, questionnaire_entry, pair, form_i_index),
                "form_i_bible_attested": "yes" if form_i_attested else "no",
                "form_ii_bible_attested": "yes" if form_ii_attested else "no",
                "form_i_clean_token_count": str(form_i_clean),
                "form_ii_clean_token_count": str(form_ii_clean),
                "form_i_family_count": str(form_i_family),
                "form_ii_family_count": str(form_ii_family),
                "best_form_i_examples": choose_inventory_examples(pair_rows, form_i, stem_alts={"I"}),
                "best_form_ii_examples": choose_inventory_examples(pair_rows, form_ii, stem_alts={"II"}),
                "nominalized_examples": choose_inventory_examples(pair_rows, "", environments={"nominalized_na"}, limit=2),
                "dependent_temporal_examples": choose_inventory_examples(pair_rows, "", environments={"dependent_temporal_ciangin", "dependent_temporal_ni_in", "clause_linking_kipan"}, limit=2),
                "purpose_examples": choose_inventory_examples(pair_rows, "", environments={"purpose_nadingin"}, limit=2),
                "relative_or_attributive_examples": choose_inventory_examples(pair_rows, "", environments={"relative_or_attributive_mi", "possessed_or_genitive_attributive"}, limit=2),
                "negative_examples": choose_inventory_examples(pair_rows, "", environments={"negative_clause"}, limit=2),
                "finite_predicate_examples": choose_inventory_examples(pair_rows, "", environments={"finite_main_or_matrix", "imperative_or_directive"}, limit=2),
                "derived_or_causative_examples": choose_inventory_examples(pair_rows, "", environments={"causative_or_derivational_sak"}, limit=2),
                "compound_or_lexicalized_examples": choose_inventory_examples(pair_rows, "", environments={"compound_or_lexicalized"}, limit=2),
                "homophone_or_noise_notes": homophone_or_noise_notes(pair_id, pair_rows, questionnaire_entry, pair),
                "bible_attestation_profile": bible_profile,
                "lexical_pair_status": lexical_status,
                "recommended_grammar_treatment": grammar_treatment,
                "print_example_status": print_status,
                "notes": merge_notes(*notes),
            }
        )

    with LEXICAL_INVENTORY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LEXICAL_INVENTORY_COLUMNS, delimiter="\t")
        writer.writeheader()
        writer.writerows(inventory_rows)


def display_path(path: Path) -> Path:
    try:
        return path.relative_to(ROOT)
    except ValueError:
        return path


def row_print_status(
    pair: PairMeta,
    row: dict[str, str],
    environment: str,
    accepted_candidate_row_keys: set[tuple[str, str, str]],
) -> tuple[str, str]:
    if environment in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return "exclude_for_now", "Derived or lexicalized environments stay excluded at the row level even when the pair is retained for review."
    if environment == "unknown_or_needs_review":
        return "needs_analyzer_review", "Review-bucket rows never count as print-ready evidence."

    contaminated, contamination_note = row_has_obvious_contamination(pair, row)
    if contaminated:
        if pair.publication_status in {"exclude_for_now", "dossier_only"}:
            return pair.publication_status, contamination_note
        return "needs_analyzer_review", contamination_note

    if pair.publication_status in {"exclude_for_now", "dossier_only", "needs_analyzer_review"}:
        return pair.publication_status, "Row status is capped by the pair-level publication status."

    row_key = (pair.pair_id, row["verse_id"], row["token_index"])
    if row_key in accepted_candidate_row_keys:
        return pair.publication_status, "Accepted candidate TSV evidence can inherit the pair's editorial status."

    if (
        row_key in MANUAL_REVIEW_ROW_ALLOWLIST
        and analysis_clarity_score(row) >= 3
        and environment in REVIEW_CITED_SAFE_ENVIRONMENTS
    ):
        return MANUAL_REVIEW_ROW_ALLOWLIST[row_key], "This exact row is a manually checked review example kept as caveated evidence in the packet."

    return "needs_analyzer_review", "Row is useful for matrix review, but it is not strong enough to inherit the pair's print-facing status."


def write_corpus_audit() -> None:
    require_tokens_export()

    pairs = build_pair_inventory()
    verses = load_verse_metadata()
    accepted_candidate_row_keys = load_accepted_candidate_row_keys(pairs)
    review_bundle_text = load_review_bundle_text()
    review_references = extract_exact_review_references(review_bundle_text)
    form_ii_counts = count_form_ii_hits(pairs)
    form_i_index, form_ii_index, canonical_by_form_i = build_indexes(pairs, form_ii_counts)

    pair_counts: dict[str, Counter] = defaultdict(Counter)
    pair_form_env_counts: dict[str, dict[str, Counter]] = defaultdict(lambda: {"I": Counter(), "II": Counter(), "": Counter()})
    example_counts: Counter = Counter()
    best_examples: dict[tuple[str, str, str], dict[str, object]] = {}
    env_summary: dict[tuple[str, str], dict[str, object]] = defaultdict(
        lambda: {
            "form_i_count": 0,
            "form_ii_count": 0,
            "total_count": 0,
            "references": [],
            "notes": Counter(),
        }
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    row_order = 0
    with CORPUS_AUDIT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CORPUS_COLUMNS, delimiter="\t")
        writer.writeheader()

        for verse_id, verse_tokens in iter_tokens_by_verse():
            verse_meta = verses.get(verse_id)
            if verse_meta is None:
                continue

            for index, row in enumerate(verse_tokens):
                pair_id, pair_note = resolve_pair_id(row, form_i_index, form_ii_index, canonical_by_form_i)
                if not pair_id:
                    continue

                pair = pairs[pair_id]
                attested_form, stem_alt, attested_note = infer_attested_form(row, pair)
                environment, env_confidence, env_note = infer_environment(verse_tokens, index, pair, row)
                context = local_context(verse_tokens, index)
                row_for_status = {
                    "pair_id": pair.pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "attested_form": attested_form,
                    "verse_id": verse_id,
                    "reference": verse_meta["reference"],
                    "token_index": row["token_index"],
                    "surface_form": row["surface_form"],
                    "normalized_form": row["normalized_form"],
                    "segmentation": row["segmentation"],
                    "gloss": row["gloss"],
                    "lemma": row["lemma"],
                    "pos": row["pos"],
                    "local_context": context,
                    "environment": environment,
                    "notes": " ".join(note for note in (pair.notes, pair_note, attested_note, env_note) if note),
                }
                print_status, status_note = row_print_status(
                    pair,
                    row_for_status,
                    environment,
                    accepted_candidate_row_keys,
                )
                notes = merge_notes(row_for_status["notes"], status_note)
                audit_row = {
                    "pair_id": pair.pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "attested_form": attested_form,
                    "stem_form": row["stem_form"],
                    "verse_id": verse_id,
                    "reference": verse_meta["reference"],
                    "token_index": row["token_index"],
                    "surface_form": row["surface_form"],
                    "normalized_form": row["normalized_form"],
                    "segmentation": row["segmentation"],
                    "gloss": row["gloss"],
                    "lemma": row["lemma"],
                    "pos": row["pos"],
                    "stem_alternation": stem_alt,
                    "prefix_chain": row["prefix_chain"],
                    "suffix_chain": row["suffix_chain"],
                    "usage_type": row["usage_type"],
                    "function_type": row["function_type"],
                    "local_context": context,
                    "kjv": verse_meta["kjv"],
                    "inferred_environment": environment,
                    "environment_confidence": env_confidence,
                    "print_status": print_status,
                    "notes": notes,
                }

                writer.writerow(audit_row)

                pair_counts[pair.pair_id]["total"] += 1
                if stem_alt == "I":
                    pair_counts[pair.pair_id]["form_i_total"] += 1
                if stem_alt == "II":
                    pair_counts[pair.pair_id]["form_ii_total"] += 1
                pair_form_env_counts[pair.pair_id][stem_alt][environment] += 1

                env_key = (pair.pair_id, environment)
                env_bucket = env_summary[env_key]
                env_bucket["total_count"] += 1
                if stem_alt == "I":
                    env_bucket["form_i_count"] += 1
                if stem_alt == "II":
                    env_bucket["form_ii_count"] += 1
                if verse_meta["reference"] not in env_bucket["references"] and len(env_bucket["references"]) < 5:
                    env_bucket["references"].append(verse_meta["reference"])
                env_bucket["notes"][env_note] += 1

                if stem_alt in {"I", "II"}:
                    key = (pair.pair_id, stem_alt, environment)
                    example_counts[key] += 1
                    example_row = {
                        "pair_id": pair.pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "gloss": pair.gloss,
                        "alternation_type": pair.alternation_type,
                        "stem_side": "form_i" if stem_alt == "I" else "form_ii",
                        "attested_form": attested_form,
                        "environment": environment,
                        "verse_id": verse_id,
                        "reference": verse_meta["reference"],
                        "token_index": row["token_index"],
                        "surface_form": row["surface_form"],
                        "normalized_form": row["normalized_form"],
                        "segmentation": row["segmentation"],
                        "gloss_span": row["gloss"],
                        "lemma": row["lemma"],
                        "pos": row["pos"],
                        "local_context": context,
                        "kjv": verse_meta["kjv"],
                        "print_status": print_status,
                        "notes": merge_notes(
                            notes,
                            "Review bucket only; not a clean syntactic construction." if environment == "unknown_or_needs_review" else "",
                            "Candidate for print." if print_status in {"print_ready", "print_usable_with_caveat"} else "",
                            "Needs review before print use." if print_status in {"dossier_only", "needs_analyzer_review"} else "",
                        ),
                    }
                    priority = selection_priority(
                        example_row,
                        accepted_candidate_row_keys,
                        review_references,
                        row_order,
                    )
                    current = best_examples.get(key)
                    if current is None or priority > current["priority"]:
                        best_examples[key] = {"priority": priority, "row": example_row}
                row_order += 1

    with ENV_SUMMARY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ENV_SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()
        for pair_id, pair in sorted(pairs.items()):
            pair_environments = sorted(
                key for key in env_summary
                if key[0] == pair_id
            )
            for _, environment in pair_environments:
                bucket = env_summary[(pair_id, environment)]
                writer.writerow(
                    {
                        "pair_id": pair_id,
                        "form_i": pair.form_i,
                        "form_ii": pair.form_ii,
                        "environment": environment,
                        "form_i_count": bucket["form_i_count"],
                        "form_ii_count": bucket["form_ii_count"],
                        "total_count": bucket["total_count"],
                        "representative_references": "; ".join(bucket["references"]),
                        "notes": join_top(bucket["notes"], limit=1),
                    }
                )

    with PAIR_SUMMARY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=PAIR_SUMMARY_COLUMNS, delimiter="\t")
        writer.writeheader()
        for pair_id, pair in sorted(pairs.items()):
            counts = pair_counts[pair_id]
            dominant_i = pair_form_env_counts[pair_id]["I"]
            dominant_ii = pair_form_env_counts[pair_id]["II"]
            recommendation = recommendation_for_pair(pair, counts["form_i_total"], counts["form_ii_total"], list(dominant_ii))
            note_parts = []
            siblings = sorted(other for other in form_i_index[pair.form_i] if other != pair_id)
            if siblings:
                note_parts.append(f"Shared Form I base with {', '.join(siblings)}.")
            if pair.notes:
                note_parts.append(pair.notes)
            writer.writerow(
                {
                    "pair_id": pair_id,
                    "form_i": pair.form_i,
                    "form_ii": pair.form_ii,
                    "gloss": pair.gloss,
                    "alternation_type": pair.alternation_type,
                    "form_i_total": counts["form_i_total"],
                    "form_ii_total": counts["form_ii_total"],
                    "total": counts["total"],
                    "dominant_form_i_environments": join_top(dominant_i),
                    "dominant_form_ii_environments": join_top(dominant_ii),
                    "analyzer_status": pair.analyzer_status,
                    "used_in_print_packet": "yes" if pair.used_in_print_packet else "no",
                    "in_candidate_tsv": "yes" if pair.in_candidate_tsv else "no",
                    "candidate_statuses": ", ".join(pair.candidate_statuses),
                    "publication_status": pair.publication_status,
                    "recommendation": recommendation,
                    "notes": " ".join(note_parts),
                }
            )

    with EXAMPLE_MATRIX_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=EXAMPLE_MATRIX_COLUMNS, delimiter="\t")
        writer.writeheader()
        for key in sorted(best_examples, key=lambda item: (item[0], item[1] != "I", item[2])):
            pair_id, stem_alt, environment = key
            example = dict(best_examples[key]["row"])
            example["environment_count_for_side"] = str(example_counts[key])
            example["selection_reason"] = build_selection_reason(
                example,
                accepted_candidate_row_keys,
                review_references,
            )
            writer.writerow(example)

    write_lexical_inventory(pairs, form_i_index, verses)

    print(f"Wrote {display_path(CORPUS_AUDIT_PATH)}")
    print(f"Wrote {display_path(ENV_SUMMARY_PATH)}")
    print(f"Wrote {display_path(PAIR_SUMMARY_PATH)}")
    print(f"Wrote {display_path(EXAMPLE_MATRIX_PATH)}")
    print(f"Wrote {display_path(LEXICAL_INVENTORY_PATH)}")


def main() -> None:
    write_corpus_audit()


if __name__ == "__main__":
    main()
