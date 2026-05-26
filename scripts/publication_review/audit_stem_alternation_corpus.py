#!/usr/bin/env python3
"""
Build a corpus-wide analyzer-based audit for Tedim stem alternation.

Outputs:
    - output/publication_review/stem_alternation_corpus_audit.tsv
    - output/publication_review/stem_alternation_environment_summary.tsv
    - output/publication_review/stem_alternation_pair_summary.tsv

The audit uses the analyzer's stem-pair inventory plus the local Tedim token
export. `data/ctd_analysis/tokens.tsv` remains generated local build output and
is intentionally not tracked in git.
"""

from __future__ import annotations

import csv
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
CANDIDATES_PATH = OUTPUT_DIR / "candidates_stem_alternation.tsv"
GRAMMAR_PACKET_PATH = OUTPUT_DIR / "grammar_stem_alternation_print_slice.md"
DICTIONARY_PACKET_PATH = OUTPUT_DIR / "dictionary_stem_alternation_print_slice.md"
REVIEW_NOTES_PATH = OUTPUT_DIR / "review_notes_stem_alternation.md"

sys.path.insert(0, str(ROOT / "scripts"))
from analyze_morphemes import VERB_STEM_PAIRS  # noqa: E402


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


def load_candidate_statuses() -> tuple[dict[str, set[str]], dict[str, bool]]:
    statuses: dict[str, set[str]] = defaultdict(set)
    present: dict[str, bool] = defaultdict(bool)
    if not CANDIDATES_PATH.exists():
        return statuses, present

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
    return statuses, present


def load_print_packet_text() -> str:
    text_parts = []
    for path in (GRAMMAR_PACKET_PATH, DICTIONARY_PACKET_PATH, REVIEW_NOTES_PATH):
        text_parts.append(path.read_text(encoding="utf-8") if path.exists() else "")
    return "\n".join(text_parts)


def build_pair_inventory() -> dict[str, PairMeta]:
    candidate_statuses, in_candidate = load_candidate_statuses()
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


def row_print_status(pair: PairMeta, environment: str) -> str:
    if environment in {"causative_or_derivational_sak", "compound_or_lexicalized"}:
        return "exclude_for_now"
    return pair.publication_status


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


def write_corpus_audit() -> None:
    require_tokens_export()

    pairs = build_pair_inventory()
    verses = load_verse_metadata()
    form_ii_counts = count_form_ii_hits(pairs)
    form_i_index, form_ii_index, canonical_by_form_i = build_indexes(pairs, form_ii_counts)

    pair_counts: dict[str, Counter] = defaultdict(Counter)
    pair_form_env_counts: dict[str, dict[str, Counter]] = defaultdict(lambda: {"I": Counter(), "II": Counter(), "": Counter()})
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
                notes = " ".join(note for note in (pair.notes, pair_note, attested_note, env_note) if note)
                print_status = row_print_status(pair, environment)

                writer.writerow(
                    {
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
                        "local_context": local_context(verse_tokens, index),
                        "kjv": verse_meta["kjv"],
                        "inferred_environment": environment,
                        "environment_confidence": env_confidence,
                        "print_status": print_status,
                        "notes": notes,
                    }
                )

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

    print(f"Wrote {CORPUS_AUDIT_PATH.relative_to(ROOT)}")
    print(f"Wrote {ENV_SUMMARY_PATH.relative_to(ROOT)}")
    print(f"Wrote {PAIR_SUMMARY_PATH.relative_to(ROOT)}")


def main() -> None:
    write_corpus_audit()


if __name__ == "__main__":
    main()
