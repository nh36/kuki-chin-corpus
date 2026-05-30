#!/usr/bin/env python3
"""
Extract analyzer-aware publication-review candidate files.

This script establishes a reusable scaffold for publication-review evidence
work. The supported topics use curated analyzer-backed verse windows from the
exported Tedim token analysis in data/ctd_analysis/tokens.tsv.

Extension pattern:
    - build_<topic>_specs() defines curated CandidateSpec rows for one topic.
    - build_specs(topic) routes the topic name to its spec builder.
    - Future topics should follow the same pattern: add a topic-specific spec
      builder, add it to the router, and commit the resulting candidate TSV.
    - Automatic discovery may be added later, but current publication-review
      candidates are intentionally curated and analyzer-validated.

Usage:
    python3 scripts/publication_review/extract_candidates.py --list-topics
    python3 scripts/publication_review/extract_candidates.py demonstratives
    python3 scripts/publication_review/extract_candidates.py case_marking
    python3 scripts/publication_review/extract_candidates.py coordinators
    python3 scripts/publication_review/extract_candidates.py interrogatives
    python3 scripts/publication_review/extract_candidates.py numerals
    python3 scripts/publication_review/extract_candidates.py negation
    python3 scripts/publication_review/extract_candidates.py pronouns
    python3 scripts/publication_review/extract_candidates.py quantifiers
    python3 scripts/publication_review/extract_candidates.py sentence_final_particles
    python3 scripts/publication_review/extract_candidates.py stem_alternation
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOKENS_PATH = ROOT / "data" / "ctd_analysis" / "tokens.tsv"
VERSES_PATH = ROOT / "data" / "verses_aligned.tsv"
OUTPUT_DIR = ROOT / "output" / "publication_review"
SUPPORTED_TOPICS = (
    "demonstratives",
    "case_marking",
    "coordinators",
    "interrogatives",
    "numerals",
    "negation",
    "pronouns",
    "quantifiers",
    "sentence_final_particles",
    "stem_alternation",
)

DEFAULT_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

CASE_MARKING_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "marker",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

INTERROGATIVES_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "interrogative_type",
    "question_word",
    "particle",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

NUMERALS_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "numeral_type",
    "numeral_value",
    "numeral_form",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

QUANTIFIERS_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "quantifier_type",
    "quantifier_form",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

COORDINATORS_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "coordinator_type",
    "coordinator_form",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

SENTENCE_FINAL_PARTICLES_CANDIDATE_COLUMNS = [
    "candidate_id",
    "topic",
    "construction_id",
    "particle_type",
    "particle_form",
    "construction_type",
    "verse_id",
    "reference",
    "surface_span",
    "token_indices",
    "segmentation_span",
    "gloss_span",
    "lemma_span",
    "pos_span",
    "kjv",
    "candidate_status",
    "confidence",
    "print_status",
    "why_selected",
    "why_excluded",
    "manual_review_status",
    "notes",
]

REQUIRED_TOKEN_COLUMNS = {
    "verse_id",
    "token_index",
    "surface_form",
    "normalized_form",
    "segmentation",
    "gloss",
    "lemma",
    "pos",
    "confidence",
    "kjv_text",
    "usage_type",
    "function_type",
}


@dataclass(frozen=True)
class VerseMeta:
    verse_id: str
    reference: str
    tedim: str
    kjv: str


@dataclass(frozen=True)
class TokenRecord:
    verse_id: str
    token_index: int
    surface_form: str
    normalized_form: str
    segmentation: str
    gloss: str
    lemma: str
    pos: str
    confidence: str
    kjv_text: str
    usage_type: str
    function_type: str


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    topic: str
    construction_id: str
    reference: str
    token_indices: tuple[int, ...]
    candidate_status: str
    confidence: str
    why_selected: str = ""
    why_excluded: str = ""
    manual_review_status: str = "reviewed"
    notes: str = ""
    expected_normalized: tuple[str, ...] = ()
    marker: str = ""
    interrogative_type: str = ""
    question_word: str = ""
    particle: str = ""
    numeral_type: str = ""
    numeral_value: str = ""
    numeral_form: str = ""
    quantifier_type: str = ""
    quantifier_form: str = ""
    coordinator_type: str = ""
    coordinator_form: str = ""
    particle_type: str = ""
    particle_form: str = ""
    construction_type: str = ""
    print_status: str = ""
    token_indices_style: str = "comma"


def build_candidate(candidate_status: str, **kwargs: object) -> CandidateSpec:
    kwargs.setdefault("manual_review_status", "reviewed")
    return CandidateSpec(candidate_status=candidate_status, **kwargs)


def accepted(**kwargs: object) -> CandidateSpec:
    return build_candidate("accepted", **kwargs)


def accepted_with_caveat(**kwargs: object) -> CandidateSpec:
    return build_candidate("accepted_with_caveat", **kwargs)


def excluded(**kwargs: object) -> CandidateSpec:
    return build_candidate("excluded", **kwargs)


def deferred(**kwargs: object) -> CandidateSpec:
    return build_candidate("deferred", **kwargs)


def needs_review(**kwargs: object) -> CandidateSpec:
    return build_candidate("needs_review", **kwargs)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "topic",
        nargs="?",
        choices=SUPPORTED_TOPICS,
        help="Publication-review topic to extract.",
    )
    parser.add_argument(
        "--list-topics",
        action="store_true",
        help="List supported topics and exit.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional explicit output path. Defaults to output/publication_review/candidates_<topic>.tsv.",
    )
    args = parser.parse_args()
    if not args.list_topics and not args.topic:
        parser.error("topic is required unless --list-topics is used")
    return args


def list_topics() -> None:
    for topic in SUPPORTED_TOPICS:
        print(topic)


def require_tokens_export() -> None:
    if TOKENS_PATH.exists():
        return

    raise SystemExit(
        "Missing data/ctd_analysis/tokens.tsv. Run `python3 scripts/export_tedim_analysis.py` "
        "before extracting publication-review candidates."
    )


def load_verse_metadata() -> dict[str, VerseMeta]:
    csv.field_size_limit(10**7)
    verses: dict[str, VerseMeta] = {}

    with VERSES_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            verse_id = row["verse_id"]
            verses[row["reference"]] = VerseMeta(
                verse_id=verse_id,
                reference=row["reference"],
                tedim=row["ctd_Tedim Chin"],
                kjv=row["eng_King James Version"],
            )

    return verses


def load_tokens() -> dict[str, list[TokenRecord]]:
    with TOKENS_PATH.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        missing = REQUIRED_TOKEN_COLUMNS - set(reader.fieldnames or [])
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise SystemExit(
                f"Token export is missing required columns: {missing_list}. "
                "Regenerate it with `python3 scripts/export_tedim_analysis.py`."
            )

        by_verse: dict[str, list[TokenRecord]] = {}
        for row in reader:
            if row["verse_id"].startswith("#"):
                continue

            record = TokenRecord(
                verse_id=row["verse_id"],
                token_index=int(row["token_index"]),
                surface_form=row["surface_form"],
                normalized_form=row["normalized_form"],
                segmentation=row["segmentation"],
                gloss=row["gloss"],
                lemma=row["lemma"],
                pos=row["pos"],
                confidence=row["confidence"],
                kjv_text=row["kjv_text"],
                usage_type=row["usage_type"],
                function_type=row["function_type"],
            )
            by_verse.setdefault(record.verse_id, []).append(record)

    return by_verse


def format_token_indices(token_indices: tuple[int, ...], style: str) -> str:
    if style == "range":
        if len(token_indices) == 1:
            return str(token_indices[0])
        if tuple(range(token_indices[0], token_indices[-1] + 1)) == token_indices:
            return f"{token_indices[0]}-{token_indices[-1]}"
    return ",".join(str(token_index) for token_index in token_indices)


def candidate_row(
    spec: CandidateSpec,
    verse_meta: VerseMeta,
    tokens_by_verse: dict[str, list[TokenRecord]],
) -> dict[str, str]:
    verse_tokens = tokens_by_verse.get(verse_meta.verse_id, [])
    index_map = {token.token_index: token for token in verse_tokens}

    try:
        selected = [index_map[token_index] for token_index in spec.token_indices]
    except KeyError as exc:
        missing = exc.args[0]
        raise SystemExit(
            f"{spec.reference} is missing token index {missing} in data/ctd_analysis/tokens.tsv."
        ) from exc

    if spec.expected_normalized:
        actual = tuple(
            token.normalized_form.lower().strip("“”\"'.,;:!?")
            for token in selected
        )
        if actual != spec.expected_normalized:
            raise SystemExit(
                f"{spec.reference} token window {spec.token_indices} normalized as {actual}, "
                f"expected {spec.expected_normalized}."
            )

    return {
        "candidate_id": spec.candidate_id,
        "topic": spec.topic,
        "construction_id": spec.construction_id,
        "marker": spec.marker,
        "interrogative_type": spec.interrogative_type,
        "question_word": spec.question_word,
        "particle": spec.particle,
        "numeral_type": spec.numeral_type,
        "numeral_value": spec.numeral_value,
        "numeral_form": spec.numeral_form,
        "quantifier_type": spec.quantifier_type,
        "quantifier_form": spec.quantifier_form,
        "coordinator_type": spec.coordinator_type,
        "coordinator_form": spec.coordinator_form,
        "particle_type": spec.particle_type,
        "particle_form": spec.particle_form,
        "construction_type": spec.construction_type,
        "verse_id": verse_meta.verse_id,
        "reference": verse_meta.reference,
        "surface_span": " ".join(token.surface_form for token in selected),
        "token_indices": format_token_indices(spec.token_indices, spec.token_indices_style),
        "segmentation_span": " | ".join(token.segmentation for token in selected),
        "gloss_span": " | ".join(token.gloss for token in selected),
        "lemma_span": " | ".join(token.lemma for token in selected),
        "pos_span": " | ".join(token.pos for token in selected),
        "kjv": verse_meta.kjv,
        "candidate_status": spec.candidate_status,
        "confidence": spec.confidence,
        "print_status": spec.print_status,
        "why_selected": spec.why_selected,
        "why_excluded": spec.why_excluded,
        "manual_review_status": spec.manual_review_status,
        "notes": spec.notes,
    }


def build_demonstratives_specs() -> list[CandidateSpec]:
    topic = "demonstratives"
    return [
        accepted(
            candidate_id="dem-hih-gen-5-1",
            topic=topic,
            construction_id="hih",
            reference="Genesis 5:1",
            token_indices=(0,),
            confidence="high",
            why_selected="Analyzer confirms `hih` as a demonstrative token in a clean proximal identificational clause.",
            expected_normalized=("hih",),
        ),
        accepted(
            candidate_id="dem-tua-gen-1-6",
            topic=topic,
            construction_id="tua",
            reference="Genesis 1:6",
            token_indices=(9,),
            confidence="high",
            why_selected="Analyzer confirms `tua` as a distal/anaphoric determiner in an ordinary noun phrase.",
            expected_normalized=("tua",),
        ),
        accepted(
            candidate_id="dem-hihte-gen-10-20",
            topic=topic,
            construction_id="hihte",
            reference="Genesis 10:20",
            token_indices=(0,),
            confidence="high",
            why_selected="Analyzer export preserves the plural demonstrative span and supports the dossier's DEM + `-te` analysis.",
            expected_normalized=("hihte",),
        ),
        accepted(
            candidate_id="dem-tuate-gen-2-19",
            topic=topic,
            construction_id="tuate",
            reference="Genesis 2:19",
            token_indices=(21,),
            confidence="high",
            why_selected="Analyzer export confirms `tuate` as the distal plural form in pronominal use.",
            expected_normalized=("tuate",),
        ),
        accepted(
            candidate_id="dem-hih-bangin-gen-32-4",
            topic=topic,
            construction_id="hih-bangin",
            reference="Genesis 32:4",
            token_indices=(8, 9),
            confidence="high",
            why_selected="Analyzer-confirmed `hih` plus `bangin` supports a manually checked manner/discourse construction.",
            expected_normalized=("hih", "bangin"),
        ),
        accepted(
            candidate_id="dem-tua-bangin-exod-14-30",
            topic=topic,
            construction_id="tua-bangin",
            reference="Exodus 14:30",
            token_indices=(2, 3),
            confidence="high",
            why_selected="Analyzer-confirmed `tua bangin` supports the distal/anaphoric manner/discourse construction after manual review.",
            expected_normalized=("tua", "bangin"),
        ),
        accepted(
            candidate_id="dem-tua-ciangin-gen-1-3",
            topic=topic,
            construction_id="tua-ciangin",
            reference="Genesis 1:3",
            token_indices=(7, 8),
            confidence="high",
            why_selected="Analyzer-confirmed `tua ciangin` supports a discourse-temporal linker, not a raw two-word adjacency only.",
            expected_normalized=("tua", "ciangin"),
        ),
        accepted(
            candidate_id="dem-tua-ahih-ciangin-gen-2-21",
            topic=topic,
            construction_id="tua-ahih-ciangin",
            reference="Genesis 2:21",
            token_indices=(0, 1, 2),
            confidence="high",
            why_selected="Analyzer-confirmed token sequence supports the discourse-temporal transition construction.",
            expected_normalized=("tua", "ahih", "ciangin"),
        ),
        deferred(
            candidate_id="dem-hi-john-1-19",
            topic=topic,
            construction_id="hi",
            reference="John 1:19",
            token_indices=(17, 18, 19),
            confidence="medium",
            why_selected="Keep one analyzer-confirmed `hi` context in the candidate layer to document why raw `hi` hits cannot be promoted directly.",
            why_excluded="Defer `hi` as a demonstrative headword: this verse shows an identity question (`na hi hiam`), not a clean demonstrative citation.",
            notes="Analyzer marks `hi` as DECL in this span; the dossier therefore defers `hi` to later copular or sentence-final work.",
            expected_normalized=("na", "hi", "hiam"),
        ),
        excluded(
            candidate_id="dem-hih-ciangin-gen-18-10",
            topic=topic,
            construction_id="hih-ciangin",
            reference="Genesis 18:10",
            token_indices=(3, 4, 5, 6, 7),
            confidence="high",
            why_selected="Retain a documented exclusion so future work can see why raw report discovery overgenerated here.",
            why_excluded="The old report's Genesis 18:10 example does not contain demonstrative `hih ciangin`; the analyzer-confirmed span contains no demonstrative `hih` before `ciangin`.",
            notes="Raw discovery and analyzer-aware review disagree here; the discrepancy is preserved rather than silently corrected.",
            expected_normalized=("tuzawh", "kha", "kua", "khit", "ciangin"),
        ),
        excluded(
            candidate_id="dem-hih-bangin-gen-6-22",
            topic=topic,
            construction_id="hih-bangin",
            reference="Genesis 6:22",
            token_indices=(2, 3),
            confidence="high",
            why_selected="Retain the report-level pitfall as an exclusion row so later dossiers do not reuse it.",
            why_excluded="Genesis 6:22 has `tua bangmahin`, not plain `hih bangin`, so it cannot be accepted as a proximal demonstrative manner example.",
            notes="This row records a raw-report misread and the analyzer-confirmed surface span that replaced it.",
            expected_normalized=("tua", "bangmahin"),
        ),
    ]


def build_case_marking_specs() -> list[CandidateSpec]:
    topic = "case_marking"
    return [
        accepted(
            candidate_id="case_in_gen4_3_kain_in",
            topic=topic,
            construction_id="case_in_ergative",
            marker="in",
            construction_type="ergative_agent",
            reference="Genesis 4:3",
            token_indices=(3, 4),
            token_indices_style="range",
            confidence="high",
            print_status="print_ready",
            why_selected="Current grammar slice anchor for ergative -in; analyzer export preserves a clean proper-noun-plus-ERG window.",
            notes="Use as the main accepted ergative candidate.",
            expected_normalized=("kain", "in"),
        ),
        needs_review(
            candidate_id="case_in_gen1_3_ciangin_review",
            topic=topic,
            construction_id="case_in_ambiguity",
            marker="in",
            construction_type="ambiguous_homograph",
            reference="Genesis 1:3",
            token_indices=(8,),
            token_indices_style="range",
            confidence="low",
            print_status="blocked",
            why_selected="Retained to show why automatic -in extraction is risky.",
            why_excluded="String matching on -in would overgenerate conjunctional or non-case material such as ciangin.",
            manual_review_status="needs_followup",
            notes="This row is an ambiguity control, not a case example.",
            expected_normalized=("ciangin",),
        ),
        accepted(
            candidate_id="case_ah_gen11_28_khuaah",
            topic=topic,
            construction_id="case_ah_locative",
            marker="ah",
            construction_type="locative_place",
            reference="Genesis 11:28",
            token_indices=(13,),
            token_indices_style="range",
            confidence="high",
            print_status="print_ready",
            why_selected="Clean noun-plus-locative example from the analyzer export; use as the ordinary -ah locative control.",
            notes="Plain locative row, kept separate from relator-noun constructions.",
            expected_normalized=("khua-ah",),
        ),
        accepted_with_caveat(
            candidate_id="case_relator_gen1_6_laizangah",
            topic=topic,
            construction_id="case_relator_spatial",
            marker="relator_noun_plus_case",
            construction_type="relator_noun_spatial",
            reference="Genesis 1:6",
            token_indices=(3,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Existing slice example; analyzer export preserves the spatial construction cleanly enough for candidate review.",
            notes="Keep as relator-noun-plus-case evidence rather than flattening it into a bare -ah example.",
            expected_normalized=("laizangah",),
        ),
        accepted_with_caveat(
            candidate_id="case_relator_gen1_14_vantungah",
            topic=topic,
            construction_id="case_relator_spatial",
            marker="relator_noun_plus_case",
            construction_type="relator_noun_spatial",
            reference="Genesis 1:14",
            token_indices=(8,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Second existing slice example showing spatial-stem plus locative marking in the analyzer export.",
            notes="Keep as relator-noun-plus-case evidence rather than as a bare place-noun locative.",
            expected_normalized=("vantungah",),
        ),
        accepted(
            candidate_id="case_relator_gen2_19_kiangah",
            topic=topic,
            construction_id="case_relator_spatial",
            marker="relator_noun_plus_case",
            construction_type="relator_noun_spatial",
            reference="Genesis 2:19",
            token_indices=(31,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Representative relator-noun-plus-case row from the token export.",
            notes="Supports the claim that relator-noun spatial grammar cannot be reduced to a suffix list.",
            expected_normalized=("kiangah",),
        ),
        accepted(
            candidate_id="case_relator_gen1_11_sungah",
            topic=topic,
            construction_id="case_relator_spatial",
            marker="relator_noun_plus_case",
            construction_type="relator_noun_spatial",
            reference="Genesis 1:11",
            token_indices=(15,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Representative internal-space relator construction from the analyzer export.",
            notes="Relator-noun evidence, not a plain -ah control.",
            expected_normalized=("sungah",),
        ),
        accepted(
            candidate_id="case_relator_gen1_2_tungah",
            topic=topic,
            construction_id="case_relator_spatial",
            marker="relator_noun_plus_case",
            construction_type="relator_noun_spatial",
            reference="Genesis 1:2",
            token_indices=(18,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Representative surface or vertical relator construction from the analyzer export.",
            notes="Keep with relator-noun-plus-case rows.",
            expected_normalized=("tungah",),
        ),
        deferred(
            candidate_id="case_a_gen2_7_a_review",
            topic=topic,
            construction_id="case_a_review",
            marker="a",
            construction_type="review_needed",
            reference="Genesis 2:7",
            token_indices=(9, 10),
            token_indices_style="range",
            confidence="low",
            print_status="blocked",
            why_selected="Retained as a control because the current export does not cleanly separate allative -a from pronominal or other functional tokens.",
            why_excluded="The current export does not cleanly separate allative -a from other ambiguous exported a tokens, so do not force them into a candidate layer until the analyzer route is sharper.",
            manual_review_status="needs_followup",
            notes="This row documents why -a remains deferred instead of being collapsed into -ah.",
            expected_normalized=("a", "a"),
        ),
        accepted_with_caveat(
            candidate_id="case_pan_matt5_19_lakpan",
            topic=topic,
            construction_id="case_pan_source",
            marker="pan",
            construction_type="source_relator",
            reference="Matthew 5:19",
            token_indices=(5,),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Matches the current case slice's source example and is analyzer-supported as a relator-noun source construction.",
            notes="Keep as source marking on a relator noun, not as a bare suffix token.",
            expected_normalized=("lakpan",),
        ),
        accepted_with_caveat(
            candidate_id="case_panin_gen12_1_inn_panin",
            topic=topic,
            construction_id="case_panin_source",
            marker="panin",
            construction_type="source_ablative",
            reference="Genesis 12:1",
            token_indices=(11, 12),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer export preserves the `inn panin` span and supports conservative source-marking treatment.",
            notes="Treat -panin conservatively as source-marking evidence without forcing a fully settled compositional `pan + in` analysis.",
            expected_normalized=("inn", "panin"),
        ),
        accepted(
            candidate_id="case_tawh_gen14_24_kei_tawh",
            topic=topic,
            construction_id="case_tawh_comitative",
            marker="tawh",
            construction_type="comitative_accompaniment",
            reference="Genesis 14:24",
            token_indices=(3, 4),
            token_indices_style="range",
            confidence="high",
            print_status="print_ready",
            why_selected="Current slice example for accompaniment; analyzer export preserves the pronoun-plus-COM window cleanly.",
            notes="Use as the main comitative/accompaniment candidate.",
            expected_normalized=("kei", "tawh"),
        ),
        accepted_with_caveat(
            candidate_id="case_tawh_gen2_7_leivui_tawh",
            topic=topic,
            construction_id="case_tawh_material",
            marker="tawh",
            construction_type="material_or_instrumental_extension",
            reference="Genesis 2:7",
            token_indices=(5, 6),
            token_indices_style="range",
            confidence="high",
            print_status="print_usable_with_caveat",
            why_selected="Current slice and review notes treat this as material or means extension rather than ordinary accompaniment.",
            notes="Keep distinct from accompaniment so tawh is not flattened into a single undifferentiated with-category.",
            expected_normalized=("leivui", "tawh"),
        ),
    ]


def build_coordinators_specs() -> list[CandidateSpec]:
    topic = "coordinators"
    return [
        accepted(
            candidate_id="coord_le_gen1_1_vantung_le_leitung",
            topic=topic,
            construction_id="coordinator-le-np",
            coordinator_type="np_conjunction",
            coordinator_form="le",
            construction_type="np_le",
            reference="Genesis 1:1",
            token_indices=(5, 6, 7),
            token_indices_style="range",
            confidence="high",
            print_status="print_ready",
            why_selected="Core NP-coordination anchor: the analyzer cleanly preserves `vantung le leitung` as a noun-plus-conjunction-plus-noun span.",
            notes="This first pass controls le-overgeneration mainly through curated selection rather than a broad raw le harvest or a separate blocked le row.",
            expected_normalized=("vantung", "le", "leitung"),
        ),
        needs_review(
            candidate_id="coord_leh_gen13_9_conditional_boundary",
            topic=topic,
            construction_id="coordinator-leh-boundary",
            coordinator_type="clause_conjunction",
            coordinator_form="leh",
            construction_type="conditional_leh",
            reference="Genesis 13:9",
            token_indices=(18, 19, 20, 21, 22, 23, 24, 25, 26, 27),
            token_indices_style="range",
            confidence="medium",
            print_status="not_print_ready",
            why_selected="Keeps `leh` visible in the candidate layer through a clean analyzer-backed conditional window instead of pretending every `leh` is a plain clause coordinator.",
            why_excluded="This row is a boundary control: the verse reads conditionally (`... na lak leh ...`) rather than as uncomplicated clause conjunction, so it should not license generic `leh = and` prose yet.",
            manual_review_status="needs_followup",
            notes="Useful overlap control for the coordinator packet because many easy `leh` hits in the export are conditional or otherwise subordinate rather than simple clause conjunctions.",
            expected_normalized=("veilam", "na", "lak", "leh", "kei", "taklamah", "ka", "pai", "ding", "hi"),
        ),
        accepted_with_caveat(
            candidate_id="coord_a_gen2_10_sequential_linker",
            topic=topic,
            construction_id="coordinator-a-sequential",
            coordinator_type="sequential_clause_linker",
            coordinator_form="a",
            construction_type="sequential_a",
            reference="Genesis 2:10",
            token_indices=(10, 11, 12, 13, 14, 15, 16, 17),
            token_indices_style="range",
            confidence="low",
            print_status="not_print_ready",
            why_selected="Representative sequential linkage window: after `gun khat hong luang`, the following `a ... gun hong kikhenin` clause shows why `a` cannot be ignored completely in coordinator review.",
            why_excluded="The analyzer still exports the relevant `a` as `3SG` / `FUNC`, so this stays caveated boundary evidence rather than an uncomplicated coordinator anchor.",
            notes="Treat as possible sequential clause linkage only in this specific constructional window; do not broaden to raw `a` hits.",
            expected_normalized=("luang", "a", "tua", "mun", "panin", "gun", "hong", "kikhenin"),
        ),
        excluded(
            candidate_id="coord_a_gen1_1_agreement_false_friend",
            topic=topic,
            construction_id="coordinator-a-false-friend",
            coordinator_type="false_friend",
            coordinator_form="a",
            construction_type="agreement_a_false_friend",
            reference="Genesis 1:1",
            token_indices=(8, 9),
            token_indices_style="range",
            confidence="high",
            print_status="blocked",
            why_selected="High-risk control row showing why raw `a` harvesting would flood the coordinator packet with agreement or other functional material.",
            why_excluded="Here `a` is the ordinary exported `3SG` / `FUNC` element before `piangsak`, not a coordinator or sequential linker.",
            notes="Use this row to keep the packet from treating every exported `a` as coordinator evidence.",
            expected_normalized=("a", "piangsak"),
        ),
        deferred(
            candidate_id="coord_mawh_gen6_3_lexical_control",
            topic=topic,
            construction_id="coordinator-mawh-review",
            coordinator_type="deferred",
            coordinator_form="mawh",
            construction_type="analyzer_noise",
            reference="Genesis 6:3",
            token_indices=(21,),
            token_indices_style="range",
            confidence="low",
            print_status="not_print_ready",
            why_selected="The generated coordinator report makes `mawh` worth checking, so the candidate layer should document what the current analyzer export actually supplies.",
            why_excluded="The current export surfaces `mawh` overwhelmingly as lexical `sin` / `V` material rather than a clean disjunction or alternative-question coordinator example.",
            manual_review_status="needs_followup",
            notes="Keep `mawh` deferred until a clean analyzer-backed disjunction or alternative-question row is located; do not replace this with report-only schematic examples.",
            expected_normalized=("mawh",),
        ),
        accepted_with_caveat(
            candidate_id="coord_ahih_hangin_gen3_4_adversative",
            topic=topic,
            construction_id="coordinator-ahih-hangin",
            coordinator_type="adversative",
            coordinator_form="ahih hangin",
            construction_type="adversative_ahih_hangin",
            reference="Genesis 3:4",
            token_indices=(0, 1),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer-backed adversative connector from the existing coordinators report.",
            why_excluded="The form remains internally analyzable as `ahih` plus `hangin`, so it should stay an adversative connector with caveat rather than a fully generalized causal/subordinator analysis.",
            notes="Keep this packet-level row narrow: it supports adversative connector prose without opening a separate `hangin` chapter.",
            expected_normalized=("ahih", "hangin"),
        ),
        accepted_with_caveat(
            candidate_id="coord_ahih_kei_leh_exod12_3_boundary",
            topic=topic,
            construction_id="coordinator-ahih-kei-leh",
            coordinator_type="conditional_adversative",
            coordinator_form="ahih kei leh",
            construction_type="conditional_adversative_ahih_kei_leh",
            reference="Exodus 12:3",
            token_indices=(16, 17, 18),
            token_indices_style="range",
            confidence="medium",
            print_status="not_print_ready",
            why_selected="Clean analyzer-backed boundary row for the `ahih kei leh` family, which the generated report places near coordination but which overlaps conditionals and negation.",
            why_excluded="This is not a simple coordinator: it bundles conditional/adversative structure with negation-overlap, so it should remain caveated boundary material.",
            notes="Retain as controlled overlap evidence only; do not reopen the negation packet or flatten `ahih kei leh` into plain conjunction.",
            expected_normalized=("ahih", "kei", "leh"),
        ),
    ]


def build_interrogatives_specs() -> list[CandidateSpec]:
    topic = "interrogatives"
    return [
        accepted_with_caveat(
            candidate_id="int_hiam_gen24_23_awng_ding_hiam",
            topic=topic,
            construction_id="interrogative-hiam-yes-no",
            reference="Genesis 24:23",
            token_indices=(8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="yes_no_question",
            particle="hiam",
            construction_type="clause_final_hiam",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer-backed clause-final hiam yes/no question from the existing interrogatives report.",
            notes="Use the attested yes/no clause `Na pa inn-ah kote giah nading a awng ding hiam`; do not silently back-project the report paraphrase `Inn-ah hong tum theih na hiam` onto the export.",
            expected_normalized=("na", "pa", "inn-ah", "kote", "giah", "nading", "a", "awng", "ding", "hiam"),
        ),
        accepted_with_caveat(
            candidate_id="int_kua_gen48_8_hihte_kua_ahi_hiam",
            topic=topic,
            construction_id="interrogative-kua",
            reference="Genesis 48:8",
            token_indices=(9, 10, 11, 12),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="content_question",
            question_word="kua",
            particle="hiam",
            construction_type="wh_plus_hiam",
            print_status="print_usable_with_caveat",
            why_selected="Canonical who-question with clause-final hiam from the existing report.",
            notes="The analyzer exports `kua` as NUM; treat that as an export caveat rather than rejecting the interrogative window.",
            expected_normalized=("hihte", "kua", "ahi", "hiam"),
        ),
        accepted_with_caveat(
            candidate_id="int_bang_exod16_15_bang_ahi_hiam",
            topic=topic,
            construction_id="interrogative-bang",
            reference="Exodus 16:15",
            token_indices=(10, 11, 12),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="content_question",
            question_word="bang",
            particle="hiam",
            construction_type="wh_plus_hiam",
            print_status="print_usable_with_caveat",
            why_selected="Compact analyzer-backed what-question with clause-final hiam.",
            notes="The analyzer glosses `bang` as `like`; the clause is still the report's core `Bang ahi hiam?` evidence.",
            expected_normalized=("bang", "ahi", "hiam"),
        ),
        accepted(
            candidate_id="int_bangci_gen3_13_bangci_hici_gamtat_na_hi_hiam",
            topic=topic,
            construction_id="interrogative-bangci",
            reference="Genesis 3:13",
            token_indices=(7, 8, 9, 10, 11, 12, 13),
            token_indices_style="range",
            confidence="high",
            interrogative_type="content_question",
            question_word="bangci",
            particle="hiam",
            construction_type="wh_plus_hiam",
            print_status="print_ready",
            why_selected="Clean how-question with bangci plus clause-final hiam.",
            notes="Keep the analyzer-backed bangci window visible rather than flattening it into a generic bang example.",
            expected_normalized=("bangci", "a", "hici", "gamtat", "na", "hi", "hiam"),
        ),
        accepted_with_caveat(
            candidate_id="int_banghangin_gen4_6_mai_sia_ahi_hiam",
            topic=topic,
            construction_id="interrogative-banghangin",
            reference="Genesis 4:6",
            token_indices=(9, 10, 11, 12, 13, 14, 15),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="content_question",
            question_word="banghangin",
            particle="hiam",
            construction_type="wh_plus_hiam",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer-backed why-question showing the banghangin reason-question family with clause-final hiam.",
            notes="The export splits `banghangin` as `bang` + `hangin`; keep it as curated reason-question evidence rather than trusting every raw bang hit.",
            expected_normalized=("bang", "hangin", "na", "mai", "sia", "ahi", "hiam"),
        ),
        accepted_with_caveat(
            candidate_id="int_kua_2sam22_32_topa_longal_pasian_kua_hiam",
            topic=topic,
            construction_id="interrogative-kua",
            reference="2 Samuel 22:32",
            token_indices=(0, 1, 2, 3, 4),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="content_question",
            question_word="kua",
            particle="hiam",
            construction_type="wh_plus_hiam",
            print_status="print_usable_with_caveat",
            why_selected="Report-backed who-question with explicit clause-final hiam.",
            notes="As in Genesis 48:8, the analyzer tags `kua` as NUM; the interrogative reading is still clear in the full clause.",
            expected_normalized=("topa", "longal", "pasian", "kua", "hiam"),
        ),
        needs_review(
            candidate_id="int_embedded_exod16_15_bang_hiam_cih_thei_lo_uh_hi",
            topic=topic,
            construction_id="interrogative-embedded-bang-hiam-cih",
            reference="Exodus 16:15",
            token_indices=(25, 26, 27, 28, 29, 30, 31),
            token_indices_style="range",
            confidence="medium",
            interrogative_type="embedded_question",
            question_word="bang",
            particle="hiam",
            construction_type="embedded_bang_hiam_cih",
            print_status="not_print_ready",
            why_selected="Keeps embedded question material visible in the first-pass candidate layer.",
            why_excluded="Indirect question complements need separate editorial treatment before they can be reused as ordinary clause-final hiam evidence.",
            manual_review_status="needs_followup",
            notes="This is useful embedded-question evidence, but it should not yet drive the first print-facing interrogatives slice.",
            expected_normalized=("bang", "hiam", "cih", "thei", "lo", "uh", "hi"),
        ),
        excluded(
            candidate_id="int_formulaic_gen3_20_bang_hang_hiam_cih_leh",
            topic=topic,
            construction_id="interrogative-formulaic-bang-hang-hiam-cih",
            reference="Genesis 3:20",
            token_indices=(9, 10, 11, 12, 13),
            token_indices_style="range",
            confidence="high",
            interrogative_type="rhetorical_or_formulaic",
            question_word="banghangin",
            particle="hiam",
            construction_type="formulaic_reason_expression",
            print_status="blocked",
            why_selected="Records the formulaic reason-expression guard already enforced in grammar integration tests.",
            why_excluded="`Bang hang hiam cih leh` is a formulaic explanatory frame, not an ordinary clause-final hiam question for print promotion.",
            notes="Keep this blocked so formulaic reason expressions do not leak into core interrogative examples.",
            expected_normalized=("bang", "hang", "hiam", "cih", "leh"),
        ),
        excluded(
            candidate_id="int_falsefriend_2kings11_11_a_hiam_ciat_uh",
            topic=topic,
            construction_id="interrogative-hiam-lexical-false-friend",
            reference="2 Kings 11:11",
            token_indices=(15, 16, 17, 18),
            token_indices_style="range",
            confidence="high",
            interrogative_type="false_friend",
            particle="hiam",
            construction_type="lexical_or_noninterrogative_hiam",
            print_status="blocked",
            why_selected="Makes the lexical `a hiam ciat uh` blocker explicit in the publication-review workflow.",
            why_excluded="This lexical sequence is not clause-final interrogative hiam evidence and should stay blocked.",
            notes="Use as an explicit hiam false-friend control instead of relying only on integration-test exclusions.",
            expected_normalized=("a", "hiam", "ciat", "uh"),
        ),
        excluded(
            candidate_id="int_falsefriend_rev1_16_langnih_a_hiam_namsau",
            topic=topic,
            construction_id="interrogative-hiam-lexical-false-friend",
            reference="Revelation 1:16",
            token_indices=(10, 11, 12, 13),
            token_indices_style="range",
            confidence="high",
            interrogative_type="false_friend",
            particle="hiam",
            construction_type="lexical_or_noninterrogative_hiam",
            print_status="blocked",
            why_selected="Captures the Revelation 1:16 sharp/two-edged-sword false friend already guarded by integration tests.",
            why_excluded="The `a hiam` sequence here belongs to lexical sword description, not to interrogative particle hiam.",
            notes="Do not treat sharp/two-edged sword contexts as interrogative evidence just because the export surfaces `hiam`.",
            expected_normalized=("langnih", "a", "hiam", "namsau"),
        ),
        excluded(
            candidate_id="int_falsefriend_gen9_21_bangmah",
            topic=topic,
            construction_id="interrogative-bang-false-friend",
            reference="Genesis 9:21",
            token_indices=(9,),
            confidence="high",
            interrogative_type="false_friend",
            question_word="bang",
            construction_type="analyzer_noise",
            print_status="blocked",
            why_selected="Keeps bang-family lexical noise visible in the candidate layer.",
            why_excluded="`bangmah` is lexical/negative-polarity material, not ordinary bang interrogative evidence.",
            notes="Blocked control row so raw bang matching does not silently treat bangmah as a what-question.",
            expected_normalized=("bangmah",),
        ),
        excluded(
            candidate_id="int_falsefriend_gen1_7_bangin",
            topic=topic,
            construction_id="interrogative-bang-false-friend",
            reference="Genesis 1:7",
            token_indices=(22,),
            confidence="high",
            interrogative_type="false_friend",
            question_word="bang",
            construction_type="analyzer_noise",
            print_status="blocked",
            why_selected="Keeps bang-family comparative/non-interrogative material out of the core interrogatives set.",
            why_excluded="`bangin` is comparison-like material, not ordinary bang interrogative evidence.",
            notes="Comparison particles `maw`, `ham`, and `em` remain deferred; this first pass stabilizes core hiam and WH evidence first.",
            expected_normalized=("bangin",),
        ),
    ]


def build_numerals_specs() -> list[CandidateSpec]:
    topic = "numerals"
    return [
        accepted(
            candidate_id="num_card_gen11_10_kum_nih",
            topic=topic,
            construction_id="numeral-nih",
            reference="Genesis 11:10",
            token_indices=(14, 15),
            token_indices_style="range",
            confidence="high",
            numeral_type="cardinal",
            numeral_value="2",
            numeral_form="nih",
            construction_type="simple_cardinal",
            print_status="print_ready",
            why_selected="Analyzer confirms a clean post-nominal year-counting phrase for basic cardinal `nih`.",
            notes="Keep as plain `kum nih` evidence; this route is curated rather than a broad search for every numeral-looking token.",
            expected_normalized=("kum", "nih"),
        ),
        accepted(
            candidate_id="num_card_gen7_10_ni_sagih",
            topic=topic,
            construction_id="numeral-sagih",
            reference="Genesis 7:10",
            token_indices=(1, 2),
            token_indices_style="range",
            confidence="high",
            numeral_type="cardinal",
            numeral_value="7",
            numeral_form="sagih",
            construction_type="noun_plus_numeral",
            print_status="print_ready",
            why_selected="Analyzer confirms a short time-unit counting phrase for basic cardinal `sagih`.",
            notes="Useful plain noun-plus-numeral evidence without broadening into a full numeral chapter.",
            expected_normalized=("ni", "sagih"),
        ),
        accepted(
            candidate_id="num_compound_gen5_9_kum_sawmkua",
            topic=topic,
            construction_id="numeral-sawmkua",
            reference="Genesis 5:9",
            token_indices=(1, 2),
            token_indices_style="range",
            confidence="high",
            numeral_type="compound_cardinal",
            numeral_value="90",
            numeral_form="sawmkua",
            construction_type="compound_tens",
            print_status="print_ready",
            why_selected="Analyzer confirms `sawmkua` as a clean compound-ten row and keeps numeral `kua = nine` visible on the numeral side of the ambiguity.",
            notes="Use as the primary accepted numeral control showing `kua` inside a numeral compound rather than as interrogative `who`.",
            expected_normalized=("kum", "sawmkua"),
        ),
        accepted_with_caveat(
            candidate_id="num_boundary_gen32_24_mi_khat",
            topic=topic,
            construction_id="numeral-khat-boundary",
            reference="Genesis 32:24",
            token_indices=(9, 10),
            token_indices_style="range",
            confidence="medium",
            numeral_type="indefinite_or_quantifier_overlap",
            numeral_value="1",
            numeral_form="khat",
            construction_type="khat_indefinite_boundary",
            print_status="print_usable_with_caveat",
            why_selected="`mi khat` is the clearest familiar analyzer-backed `khat` row, but it sits exactly on the numeral versus indefinite boundary that the packet needs to keep explicit.",
            notes="Treat as boundary evidence (`one person` / `a man`), not as an uncomplicated print anchor for bare numeral `one`.",
            expected_normalized=("mi", "khat"),
        ),
        accepted(
            candidate_id="num_ordinal_gen7_11_nihna",
            topic=topic,
            construction_id="numeral-nihna",
            reference="Genesis 7:11",
            token_indices=(7,),
            confidence="high",
            numeral_type="ordinal",
            numeral_value="2",
            numeral_form="nihna",
            construction_type="ordinal_na",
            print_status="print_ready",
            why_selected="Analyzer confirms a clean `-na` ordinal token for the basic ordinal layer.",
            notes="Keep the tight ordinal token instead of promoting the noisier surrounding month-day expression in this first pass.",
            expected_normalized=("nihna",),
        ),
        accepted_with_caveat(
            candidate_id="num_mult_gen31_7_sawmvei",
            topic=topic,
            construction_id="numeral-sawmvei",
            reference="Genesis 31:7",
            token_indices=(10,),
            confidence="medium",
            numeral_type="multiplicative",
            numeral_value="10",
            numeral_form="sawmvei",
            construction_type="classifier_vei_sawm",
            print_status="print_usable_with_caveat",
            why_selected="Keeps a compact occurrence-counting expression in the candidate layer without trying to build the full classifier system yet.",
            notes="The generated report paraphrases this as `vei sawm`, but the current analyzer export preserves fused `sawmvei`; keep the export-backed form as the control.",
            expected_normalized=("sawmvei",),
        ),
        accepted_with_caveat(
            candidate_id="num_large_gen5_27_kum_zakua_kum_sawmguk_kua",
            topic=topic,
            construction_id="numeral-large-number",
            reference="Genesis 5:27",
            token_indices=(7, 8, 9, 10, 11, 12, 13),
            token_indices_style="range",
            confidence="medium",
            numeral_type="large_number",
            numeral_value="969",
            numeral_form="zakua ... sawmguk ... kua",
            construction_type="large_number_phrase",
            print_status="print_usable_with_caveat",
            why_selected="Keeps biblical large-number style visible in the candidate layer and preserves a second numeral-side `kua` context without turning the first pass into a full numerals chapter.",
            notes="The export compresses the hundred-plus-nine material into `zakua` and leaves final `kua` as a standalone token, so keep this as candidate-level large-number evidence with a visible analyzer caveat.",
            expected_normalized=("kum", "zakua", "le", "kum", "sawmguk", "le", "kua"),
        ),
        excluded(
            candidate_id="num_falsefriend_gen48_8_hihte_kua_ahi_hiam",
            topic=topic,
            construction_id="numeral-kua-false-friend",
            reference="Genesis 48:8",
            token_indices=(9, 10, 11, 12),
            token_indices_style="range",
            confidence="high",
            numeral_type="false_friend",
            numeral_form="kua",
            construction_type="kua_who_false_friend",
            print_status="blocked",
            why_selected="Explicit ambiguity control so raw `kua` matching cannot pull interrogative `who` rows into the numeral packet as `nine`.",
            why_excluded="This is the familiar interrogative `who` clause `Hihte kua ahi hiam?`, not numeral `kua = nine` evidence.",
            notes="Reuse the already-audited interrogative window as a blocked numeral false friend instead of rediscovering it later via raw search.",
            expected_normalized=("hihte", "kua", "ahi", "hiam"),
        ),
        deferred(
            candidate_id="num_dist_gen7_2_sagih_sagih",
            topic=topic,
            construction_id="numeral-distributive-sagih",
            reference="Genesis 7:2",
            token_indices=(4,),
            confidence="low",
            numeral_type="distributive",
            numeral_value="7",
            numeral_form="sagih sagih",
            construction_type="numeral_reduplication",
            print_status="not_print_ready",
            why_selected="The generated numerals report treats Genesis 7:2 as distributive `sagih sagih`, so the candidate layer needs one explicit placeholder for that tempting pattern.",
            why_excluded="The current analyzer export preserves only a single `sagih` token in this counting span, so the expected reduplicated distributive form is not yet analyzer-backed here.",
            manual_review_status="needs_followup",
            notes="Keep deferred rather than importing the report's distributive wording into the candidate layer without an analyzer-confirmed repeated numeral span.",
            expected_normalized=("sagih",),
        ),
    ]


def build_quantifiers_specs() -> list[CandidateSpec]:
    topic = "quantifiers"
    return [
        accepted(
            candidate_id="quant_univ_gen2_1_khempeuh",
            topic=topic,
            construction_id="quantifier-khempeuh",
            reference="Genesis 2:1",
            token_indices=(3, 4, 5, 6, 7, 8, 9),
            token_indices_style="range",
            confidence="high",
            quantifier_type="universal",
            quantifier_form="khempeuh",
            construction_type="noun_plus_khempeuh",
            print_status="print_ready",
            why_selected="Analyzer confirms `khempeuh` in a clean scoped noun phrase, giving the packet a conservative universal anchor.",
            notes="Keep this as the core universal row rather than importing generated-report frequency counts or broad raw `khempeuh` searches.",
            expected_normalized=("vantung", "leitung", "le", "a", "sunga", "omte", "khempeuh"),
        ),
        accepted_with_caveat(
            candidate_id="quant_exist_gen32_8_pawlkhat",
            topic=topic,
            construction_id="quantifier-pawlkhat",
            reference="Genesis 32:8",
            token_indices=(7,),
            confidence="medium",
            quantifier_type="existential",
            quantifier_form="pawlkhat",
            construction_type="pawlkhat_partitive",
            print_status="print_usable_with_caveat",
            why_selected="The generated-report Esau contingency verse still yields a clean analyzer-backed `pawlkhat` token and preserves the partitive or alternative-grouping reading the packet needs.",
            notes="Treat as partitive or alternative-grouping evidence (`one company ... the other company`), not as an uncomplicated bare `some` entry. The opening `Pawlkhatah` token in this verse remains noisy in the current export, so the clean control token is the later `pawlkhat`.",
            expected_normalized=("pawlkhat",),
        ),
        accepted_with_caveat(
            candidate_id="quant_boundary_gen32_24_mi_khat",
            topic=topic,
            construction_id="quantifier-khat-boundary",
            reference="Genesis 32:24",
            token_indices=(9, 10),
            token_indices_style="range",
            confidence="medium",
            quantifier_type="numeral_indefinite_boundary",
            quantifier_form="khat",
            construction_type="khat_indefinite_boundary",
            print_status="print_usable_with_caveat",
            why_selected="`mi khat` is the clearest familiar analyzer-backed `khat` row, but it sits on the numeral-versus-indefinite boundary that quantifier work must keep explicit.",
            notes="Boundary evidence only: reuse the already-audited numerals row so quantifiers does not silently absorb numeral `one` as an uncomplicated article-like quantifier.",
            expected_normalized=("mi", "khat"),
        ),
        accepted_with_caveat(
            candidate_id="quant_neg_exod2_12_kuamah",
            topic=topic,
            construction_id="quantifier-kuamah",
            reference="Exodus 2:12",
            token_indices=(4, 5, 6),
            token_indices_style="range",
            confidence="high",
            quantifier_type="negative_quantifier",
            quantifier_form="kuamah",
            construction_type="negative_quantifier_kuamah",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer confirms `kuamah mu lo` in a true negative clause, giving the packet a controlled negative-quantifier row without reopening the negation slice.",
            notes="Negation-overlap caveat: keep this as quantifier evidence only in the licensed negative clause; cross-reference the stabilized negation packet instead of re-arguing `lo` here.",
            expected_normalized=("kuamah", "mu", "lo"),
        ),
        accepted_with_caveat(
            candidate_id="quant_neg_gen39_9_bangmah",
            topic=topic,
            construction_id="quantifier-bangmah",
            reference="Genesis 39:9",
            token_indices=(25, 26, 27, 28),
            token_indices_style="range",
            confidence="high",
            quantifier_type="negative_quantifier",
            quantifier_form="bangmah",
            construction_type="negative_quantifier_bangmah",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer confirms `bangmah om lo hi` as a negative-existential or negative-quantifier clause with a compact analyzer-backed span.",
            notes="Keep both cautions explicit: this row depends on clear negative licensing, and it must not override interrogative-packet controls on other bang-family material.",
            expected_normalized=("bangmah", "om", "lo", "hi"),
        ),
        accepted_with_caveat(
            candidate_id="quant_degree_gen17_2_tampi_tak",
            topic=topic,
            construction_id="quantifier-tampi",
            reference="Genesis 17:2",
            token_indices=(8, 9),
            token_indices_style="range",
            confidence="high",
            quantifier_type="degree",
            quantifier_form="tampi",
            construction_type="degree_tampi",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer confirms `tampi tak` as a compact quantity or degree row for the first quantifiers pass.",
            notes="Keep as quantity or degree evidence only; do not let this first pass broaden into a general adjective or adverb chapter.",
            expected_normalized=("tampi", "tak"),
        ),
        accepted_with_caveat(
            candidate_id="quant_comp_gen26_16_zaw",
            topic=topic,
            construction_id="quantifier-zaw",
            reference="Genesis 26:16",
            token_indices=(18, 19),
            token_indices_style="range",
            confidence="medium",
            quantifier_type="comparative",
            quantifier_form="zaw",
            construction_type="comparative_zaw",
            print_status="print_usable_with_caveat",
            why_selected="A short analyzer-backed `vanglian zaw` span keeps one comparative boundary row visible without overextending the packet.",
            notes="Comparative caveat: retain only as a compact edge case; do not expand quantifiers into a general comparison chapter.",
            expected_normalized=("vanglian", "zaw"),
        ),
        accepted_with_caveat(
            candidate_id="quant_int_gen13_2_hau_mahmah",
            topic=topic,
            construction_id="quantifier-mahmah",
            reference="Genesis 13:2",
            token_indices=(6, 7),
            token_indices_style="range",
            confidence="medium",
            quantifier_type="intensifier",
            quantifier_form="mahmah",
            construction_type="intensifier_mahmah",
            print_status="print_usable_with_caveat",
            why_selected="A compact `hau mahmah` span keeps intensifier material explicit without pretending this packet now covers full intensifier syntax.",
            notes="Intensifier caveat: useful as a boundary row, not as the start of a broad degree-modification chapter.",
            expected_normalized=("hau", "mahmah"),
        ),
        deferred(
            candidate_id="quant_dist_gen31_32_mi_peuhpeuh",
            topic=topic,
            construction_id="quantifier-peuhpeuh",
            reference="Genesis 31:32",
            token_indices=(4, 5),
            token_indices_style="range",
            confidence="medium",
            quantifier_type="distributive_universal",
            quantifier_form="peuhpeuh",
            construction_type="peuhpeuh_distributive",
            print_status="not_print_ready",
            why_selected="The report mentions `peuhpeuh`, so the candidate layer keeps one clean analyzer-backed span visible instead of losing track of the form entirely.",
            why_excluded="The current clean window `mi peuhpeuh` behaves more like free-choice or `whoever / any person` material than a settled distributive-universal anchor, so it is deferred.",
            manual_review_status="needs_followup",
            notes="Defer rather than manufacturing a cleaner distributive example from the report alone.",
            expected_normalized=("mi", "peuhpeuh"),
        ),
        deferred(
            candidate_id="quant_degree_exod16_17_tawm",
            topic=topic,
            construction_id="quantifier-tawm",
            reference="Exodus 16:17",
            token_indices=(18,),
            confidence="low",
            quantifier_type="degree",
            quantifier_form="tawm",
            construction_type="degree_tawm",
            print_status="not_print_ready",
            why_selected="The quantity-contrast verse behind report-visible `tampi ... tawm` is worth keeping in view for later quantifier work.",
            why_excluded="The current export glosses `tawm` as `produce` and leaves the low-quantity reading too noisy for print promotion in this first pass.",
            manual_review_status="needs_followup",
            notes="Keep deferred until a cleaner analyzer-backed low-quantity row is available; do not infer a settled `tawm` quantifier entry from this contrast alone.",
            expected_normalized=("tawm",),
        ),
        excluded(
            candidate_id="quant_falsefriend_exod27_11_tua_bangmah_hiin",
            topic=topic,
            construction_id="quantifier-bangmah-false-friend",
            reference="Exodus 27:11",
            token_indices=(7, 8, 9),
            token_indices_style="range",
            confidence="high",
            quantifier_type="false_friend",
            quantifier_form="bangmah",
            construction_type="interrogative_overlap_control",
            print_status="blocked",
            why_selected="Bang-family material already caused overgeneration in the interrogatives and negation packets, so the quantifiers layer needs one explicit blocked control.",
            why_excluded="In `tua bangmah hi-in`, `bangmah` is not an ordinary negative quantifier; this lexicalized bang-family span cannot be promoted as quantifier evidence.",
            notes="Interrogative-overlap control: keep this blocked so quantifiers does not absorb every `bangmah` hit that surfaces outside clear negative licensing.",
            expected_normalized=("tua", "bangmah", "hi-in"),
        ),
    ]


def build_negation_specs() -> list[CandidateSpec]:
    topic = "negation"
    return [
        accepted(
            candidate_id="neg-lo-gen-4-5",
            topic=topic,
            construction_id="lo",
            reference="Genesis 4:5",
            token_indices=(6, 7, 8),
            confidence="high",
            why_selected="Analyzer-confirmed `thusim lo hi` gives a clean clause-level negative predicate for the core `lo` entry.",
            expected_normalized=("thusim", "lo", "hi"),
        ),
        accepted(
            candidate_id="neg-loh-gen-3-11",
            topic=topic,
            construction_id="loh",
            reference="Genesis 3:11",
            token_indices=(13, 14, 15),
            confidence="high",
            why_selected="Analyzer-confirmed `nek loh dinga` supports dependent or derived negation rather than a random spelling variant of `lo`.",
            notes="Export caveat: the token window is correct, but the export currently lemmatizes `loh` as `Loh` and tags it `PROP`; accepted status rests on the confirmed surface window plus manual constructional review.",
            expected_normalized=("nek", "loh", "dinga"),
        ),
        accepted(
            candidate_id="neg-kei-prohibitive-gen-15-1",
            topic=topic,
            construction_id="kei-prohibitive",
            reference="Genesis 15:1",
            token_indices=(15, 16, 17),
            confidence="high",
            why_selected="Analyzer-confirmed `lau kei in` is a compact prohibitive and supports `kei` as the strongest current prohibitive marker.",
            expected_normalized=("lau", "kei", "in"),
        ),
        accepted(
            candidate_id="neg-nawn-lo-gen-8-12",
            topic=topic,
            construction_id="nawn-lo",
            reference="Genesis 8:12",
            token_indices=(18, 19, 20),
            confidence="high",
            why_selected="Analyzer-confirmed `nawn lo hi` gives a clean cessative or no-longer construction.",
            notes="Export caveat: the token window is correct, but `nawn` currently surfaces with lemma `Nawn` and POS `PROP`; the row is accepted because the surface span and verse context are unambiguous.",
            expected_normalized=("nawn", "lo", "hi"),
        ),
        accepted(
            candidate_id="neg-thei-lo-gen-27-23",
            topic=topic,
            construction_id="thei-lo",
            reference="Genesis 27:23",
            token_indices=(14, 15, 16),
            confidence="high",
            why_selected="Analyzer-confirmed `thei lo hi` gives a print-safe inability or non-recognition pattern for ordinary ability negation.",
            expected_normalized=("thei", "lo", "hi"),
        ),
        accepted(
            candidate_id="neg-theih-loh-exod-10-5",
            topic=topic,
            construction_id="theih-loh",
            reference="Exodus 10:5",
            token_indices=(5, 6, 7),
            confidence="high",
            why_selected="Analyzer-confirmed `theih loh nadingin` preserves the dependent ability-negation pattern that the packet treats separately from simple `thei lo`.",
            notes="Export caveat: the token window is correct, but the export currently shows `loh` and `nadingin` with `PROP`-like lemma/POS values (`Loh`, `Nadingin`); accepted status depends on the analyzer-backed span plus manual verse review.",
            expected_normalized=("theih", "loh", "nadingin"),
        ),
        accepted(
            candidate_id="neg-kuamah-exod-2-12",
            topic=topic,
            construction_id="kuamah",
            reference="Exodus 2:12",
            token_indices=(4, 5, 6),
            confidence="high",
            why_selected="Analyzer-confirmed `kuamah mu lo` gives a manually checked negative-polarity environment rather than a raw string hit only.",
            expected_normalized=("kuamah", "mu", "lo"),
        ),
        accepted(
            candidate_id="neg-bangmah-gen-39-9",
            topic=topic,
            construction_id="bangmah",
            reference="Genesis 39:9",
            token_indices=(25, 26, 27, 28),
            confidence="high",
            why_selected="Analyzer-confirmed `bangmah om lo hi` gives a clean negative-polarity or negative-existential environment for `bangmah`.",
            expected_normalized=("bangmah", "om", "lo", "hi"),
        ),
        excluded(
            candidate_id="neg-lo-uh-prohibitive-gen-2-25",
            topic=topic,
            construction_id="lo-uh-prohibitive",
            reference="Genesis 2:25",
            token_indices=(9, 10, 11, 12),
            confidence="high",
            why_selected="Retain the old report-level pitfall so future work does not reclassify raw `V lo uh` as prohibitive evidence.",
            why_excluded="Genesis 2:25 is an ordinary declarative plural negative clause (`maizum lo uh hi`), not a prohibitive or directive.",
            notes="Problem type: raw-string overgeneration plus constructional ambiguity. Export caveat: the surface window is correct, but `uh` currently appears as POS `N`; this row remains excluded because `V lo uh` cannot be accepted as prohibitive evidence without an independently directive context.",
            expected_normalized=("maizum", "lo", "uh", "hi"),
        ),
        excluded(
            candidate_id="neg-kei-pronoun-gen-39-9",
            topic=topic,
            construction_id="kei-pronoun",
            reference="Genesis 39:9",
            token_indices=(3, 4),
            confidence="high",
            why_selected="Raw `kei` searches are tempting because negative `kei` is central to the packet, so the candidate layer needs one explicit pronoun false friend.",
            why_excluded="In `kei sangin`, the analyzer marks `kei` as 1SG pronoun, not as a negator, so this row cannot support negation prose.",
            notes="Problem type: analyzer-backed ambiguity handling. Export caveat: `kei` is correctly interpreted as `1SG.PRO` and now exports with pronoun POS in this row, but exact `kei` counts still need function-level checking so pronominal and negative uses do not get conflated.",
            expected_normalized=("kei", "sangin"),
        ),
        excluded(
            candidate_id="neg-bangmah-npi-exod-27-11",
            topic=topic,
            construction_id="bangmah-npi",
            reference="Exodus 27:11",
            token_indices=(7, 8, 9),
            confidence="high",
            why_selected="The dossier already flags non-NPI `bangmah` uses, so one explicit exclusion row helps keep raw `bangmah` searches from overcounting negation evidence.",
            why_excluded="`tua bangmah hi-in` is a non-NPI lexical expression ('likewise / in the same way'), not negative-polarity evidence.",
            notes="Problem type: raw-string overgeneration. Export caveat: `bangmah` still glosses as `nothing`, but the broader span lacks negative licensing; `bangmah` requires polarity-context checking before it can support negation prose.",
            expected_normalized=("tua", "bangmah", "hi-in"),
        ),
    ]


def build_pronouns_specs() -> list[CandidateSpec]:
    topic = "pronouns"
    return [
        accepted(
            candidate_id="pro-kei-gen-24-7",
            topic=topic,
            construction_id="kei-pronoun",
            reference="Genesis 24:7",
            token_indices=(16,),
            confidence="high",
            why_selected="Analyzer-confirmed `kei` gives a manually checked free 1SG pronoun in ordinary argument position without relying on the negation packet.",
            notes="Analyzer fix side effect: the same POS-routing correction that repaired pronominal `ko` now also preserves this `kei` row as `PRON` rather than collapsing it into the generic function-word class.",
            expected_normalized=("kei",),
        ),
        accepted(
            candidate_id="pro-nang-gen-4-11",
            topic=topic,
            construction_id="nang-pronoun",
            reference="Genesis 4:11",
            token_indices=(13,),
            confidence="high",
            why_selected="Analyzer-confirmed `nang` provides a straightforward free 2SG pronoun example.",
            expected_normalized=("nang",),
        ),
        accepted(
            candidate_id="pro-amah-gen-3-20",
            topic=topic,
            construction_id="amah-pronoun",
            reference="Genesis 3:20",
            token_indices=(14,),
            confidence="high",
            why_selected="Analyzer-confirmed `amah` is a clean free 3SG pronoun in a stable discourse example already used by the packet.",
            expected_normalized=("amah",),
        ),
        accepted(
            candidate_id="pro-amaute-gen-3-21",
            topic=topic,
            construction_id="amaute-pronoun",
            reference="Genesis 3:21",
            token_indices=(13,),
            confidence="high",
            why_selected="Analyzer-confirmed `amaute` supplies a print-safe 3PL independent pronoun row for the packet's paradigm.",
            expected_normalized=("amaute",),
        ),
        accepted(
            candidate_id="pro-note-gen-9-9",
            topic=topic,
            construction_id="note-pronoun",
            reference="Genesis 9:9",
            token_indices=(2,),
            confidence="high",
            why_selected="Analyzer-confirmed `note` gives a clear 2PL independent pronoun distinct from the following possessive-looking `note'` token in the same verse.",
            expected_normalized=("note",),
        ),
        accepted(
            candidate_id="pro-kote-gen-34-9",
            topic=topic,
            construction_id="kote-exclusive",
            reference="Genesis 34:9",
            token_indices=(0,),
            confidence="high",
            why_selected="The analyzer confirms `kote`, and the addressed-dialogue context already documented in the clusivity dossier makes this a strong exclusive 1PL example.",
            expected_normalized=("kote",),
        ),
        accepted(
            candidate_id="pro-ko-gen-24-55",
            topic=topic,
            construction_id="ko-exclusive",
            reference="Genesis 24:55",
            token_indices=(14, 15),
            confidence="high",
            why_selected="The token window is analyzer-confirmed, and the dossier already treats this addressed-dialogue context as strong exclusive evidence for the shorter `ko` series.",
            notes="Analyzer fix: `ko` now exports as `1PL.EXCL.PRO` in this addressed-dialogue window, while lexical `ko = long` remains available outside the clear pronoun contexts audited in the dossier.",
            expected_normalized=("ko", "tawh"),
        ),
        needs_review(
            candidate_id="pro-eite-gen-13-8",
            topic=topic,
            construction_id="eite-inclusive-context",
            reference="Genesis 13:8",
            token_indices=(25,),
            confidence="high",
            why_selected="Genesis 13:8 is a strong inclusive discourse context and therefore belongs in the candidate layer as explicit evidence for why `eite` is tempting to treat as globally inclusive.",
            why_excluded="This verse supports an inclusive reading in context, but the clusivity dossier also contains clear exclusive `eite` uses, so the form cannot yet support a final global print claim.",
            notes="Analyzer caveat: the nearby predicate `ihi` is glossed `1PL.INCL`, but the candidate row remains unresolved because the broader `eite/ei` series is still mixed in the Bible dossier.",
            expected_normalized=("eite",),
        ),
        needs_review(
            candidate_id="pro-eite-gen-31-15",
            topic=topic,
            construction_id="eite-exclusive-context",
            reference="Genesis 31:15",
            token_indices=(2,),
            confidence="high",
            why_selected="This row preserves the strongest dossier-level counterexample to a simple inclusive label for `eite`.",
            why_excluded="Rachel and Leah address Jacob while excluding him from the `eite` group, so this verse blocks any automatic promotion of `eite` to a settled inclusive headword.",
            notes="The candidate layer keeps this verse precisely because it conflicts with Genesis 13:8; the mixed discourse evidence is the reason `eite` remains unresolved.",
            expected_normalized=("eite",),
        ),
        deferred(
            candidate_id="pro-ei-gen-31-14",
            topic=topic,
            construction_id="ei-exclusive-context",
            reference="Genesis 31:14",
            token_indices=(12,),
            confidence="medium",
            why_selected="This row preserves a strong local counterexample to any simple globally inclusive reading of the shorter `ei` series.",
            why_excluded="Rachel and Leah address Jacob while excluding him from `ei`, so this verse cannot be promoted into a settled paradigm label for the shorter series.",
            notes="Export caveat: the token is glossed `1PL.EXCL.POSS` and tagged `PRON`, but the candidate layer still defers the series because other `ei` contexts point in different directions.",
            expected_normalized=("ei",),
        ),
        deferred(
            candidate_id="pro-ei-gen-42-2",
            topic=topic,
            construction_id="ei-inclusive-context",
            reference="Genesis 42:2",
            token_indices=(16,),
            confidence="medium",
            why_selected="Keep one shorter-form `ei` token in the candidate file so the unresolved clusivity question is not reduced to `eite` alone.",
            why_excluded="Genesis 42:2 is compatible with an inclusive reading, but the smaller `ei` sample is mixed and the export itself currently assigns clusivity-like labels that the dossier does not yet treat as decisive.",
            notes="Export caveat: this token is glossed `1PL.EXCL` and tagged `FUNC`, while nearby `i` is glossed `1PL.INCL`; the candidate file records the conflict instead of normalizing it away.",
            expected_normalized=("ei",),
        ),
        excluded(
            candidate_id="pro-kei-negator-gen-15-1",
            topic=topic,
            construction_id="kei-negator",
            reference="Genesis 15:1",
            token_indices=(15, 16, 17),
            confidence="high",
            why_selected="Raw `kei` discovery overlaps directly with the negation packet, so the pronoun candidate layer needs one explicit negator false friend.",
            why_excluded="`lau kei in` is prohibitive negation, not 1SG pronoun evidence, and therefore cannot support pronoun prose.",
            notes="Cross-topic caveat: the analyzer export correctly treats this `kei` as NEG/FUNC, matching the negation candidate layer rather than the pronoun layer.",
            expected_normalized=("lau", "kei", "in"),
        ),
    ]


def build_stem_alternation_specs() -> list[CandidateSpec]:
    topic = "stem_alternation"
    return [
        accepted(
            candidate_id="stem-mu-form-i-gen-1-4",
            topic=topic,
            construction_id="mu-muh",
            reference="Genesis 1:4",
            token_indices=(8,),
            confidence="high",
            why_selected="`a mu hi` is the packet's clearest finite Form I example for `mu ~ muh` and remains analyzer-confirmed in a straightforward clause-final predicate.",
            expected_normalized=("mu",),
        ),
        accepted(
            candidate_id="stem-muh-derived-gen-19-19",
            topic=topic,
            construction_id="mu-muh",
            reference="Genesis 19:19",
            token_indices=(3,),
            confidence="high",
            why_selected="`muhna-ah` is the dossier's clean nominalized Form II example and makes the derived-vs-finite contrast explicit for `mu ~ muh`.",
            expected_normalized=("muhna-ah",),
        ),
        accepted(
            candidate_id="stem-ne-nek-gen-2-17",
            topic=topic,
            construction_id="ne-nek",
            reference="Genesis 2:17",
            token_indices=(12, 23),
            confidence="high",
            why_selected="Genesis 2:17 remains the strongest same-verse contrast in the packet: finite `ne` in the prohibition and Form II `nek` in the dependent temporal clause.",
            expected_normalized=("ne", "nek"),
        ),
        accepted(
            candidate_id="stem-nei-form-i-gen-11-30",
            topic=topic,
            construction_id="nei-neih",
            reference="Genesis 11:30",
            token_indices=(5,),
            confidence="high",
            why_selected="Finite `nei` in Genesis 11:30 is one of the packet's stable Form I possession examples.",
            expected_normalized=("nei",),
        ),
        accepted(
            candidate_id="stem-neih-derived-2sam-23-8",
            topic=topic,
            construction_id="nei-neih",
            reference="2 Samuel 23:8",
            token_indices=(1,),
            confidence="high",
            why_selected="`neih` in `David' neih mi` gives the print-facing derived/attributive Form II side of `nei ~ neih` that the packet already uses.",
            expected_normalized=("neih",),
        ),
        accepted(
            candidate_id="stem-pia-piak-gen-3-12",
            topic=topic,
            construction_id="pia-piak",
            reference="Genesis 3:12",
            token_indices=(8, 13),
            confidence="high",
            why_selected="Genesis 3:12 is the manually checked same-turn contrast for `pia ~ piak`; it is safe packet evidence even though the broader questionnaire is noisy.",
            notes="Report-layer caveat: this accepted row is manual packet evidence, not a license to trust questionnaire hits contaminated by `piangsak` and related derivations.",
            expected_normalized=("piak", "pia"),
        ),
        accepted(
            candidate_id="stem-zak-dependent-gen-24-52",
            topic=topic,
            construction_id="za-zak",
            reference="Genesis 24:52",
            token_indices=(6, 7),
            confidence="high",
            why_selected="`a zak ciangin` is the packet's best analyzer-backed dependent-clause example for the caveated `za ~ zak` expansion.",
            notes="Packet caveat: `zak` is safe here as a hearing example, but the dossier warns that not every surface `zak` token should be promoted without manual review.",
            expected_normalized=("zak", "ciangin"),
        ),
        accepted(
            candidate_id="stem-nusiat-dependent-deut-2-14",
            topic=topic,
            construction_id="nusia-nusiat",
            reference="Deuteronomy 2:14",
            token_indices=(22, 23, 24),
            confidence="high",
            why_selected="`i nusiat a kipan` preserves the dossier's strongest dependent/clause-linking Form II evidence for the caveated `nusia ~ nusiat` pair.",
            notes="Export caveat: the analyzer currently surfaces `nusiat` with noun-like POS here, so accepted status depends on the analyzer-backed span plus manual packet review rather than POS alone.",
            expected_normalized=("nusiat", "a", "kipan"),
        ),
        needs_review(
            candidate_id="stem-theihna-gen-2-17",
            topic=topic,
            construction_id="thei-theih",
            reference="Genesis 2:17",
            token_indices=(7,),
            confidence="high",
            why_selected="`theihna` keeps the real `thei ~ theih` pair visible in the candidate layer because the packet and dossier both treat it as genuine but constructionally mixed evidence.",
            why_excluded="This row shows Form II through a nominalized derivative, not through a reader-friendly bare contrast, so it should not by itself settle print prose for the whole pair.",
            notes="The packet keeps `thei ~ theih` caveated because the Form I side overlaps with modal/ability uses and the Form II side is overrepresented in nominalized or purposive material.",
            expected_normalized=("theihna",),
        ),
        needs_review(
            candidate_id="stem-pianna-gen-10-29",
            topic=topic,
            construction_id="piang-pian",
            reference="Genesis 10:29",
            token_indices=(4,),
            confidence="medium",
            why_selected="`pianna` records the dossier's main reason for keeping `piang ~ pian` visible even though the pair is still more derived than pedagogically neat.",
            why_excluded="The Form II side is mostly visible through derived forms such as `pianna`, so this row cannot yet carry a simple print-safe bare-stem contrast on its own.",
            notes="The packet keeps `piang ~ pian` provisional rather than excluded: the pair is real, but the evidence is still dominated by nominalized and purposive environments.",
            expected_normalized=("pianna",),
        ),
        excluded(
            candidate_id="stem-piangsak-noise-gen-1-1",
            topic=topic,
            construction_id="pia-piak-report-noise",
            reference="Genesis 1:1",
            token_indices=(9,),
            confidence="high",
            why_selected="The questionnaire/report layer repeatedly tempts `pia ~ piak` work with creation verses, so the candidate file needs one explicit derivational false friend.",
            why_excluded="`piangsak` is a causative/derived verb and cannot count as direct `piak` evidence for the simple Form I / Form II pair.",
            notes="Problem type: report noise plus derivational contamination. This row preserves the packet's warning that `piak` examples must be insulated from `piangsak`.",
            expected_normalized=("piangsak",),
        ),
        excluded(
            candidate_id="stem-ngaihsutna-noise-gen-6-5",
            topic=topic,
            construction_id="ngai-ngaih-family",
            reference="Genesis 6:5",
            token_indices=(9,),
            confidence="high",
            why_selected="The packet explicitly says `ngai/ngaih` remains dossier-only because raw `ngaih` discovery is swamped by the `ngaihsun/ngaihsut` lexical family.",
            why_excluded="`ngaihsutna` is a lexical-family derivative, not clean `ngaih` stem evidence, so this row cannot support print-safe stem-alternation prose.",
            notes="Problem type: lexical-family contamination rather than simple analyzer failure. The candidate layer keeps this row so `ngai/ngaih` cannot be silently promoted from noisy family material.",
            expected_normalized=("ngaihsutna",),
        ),
        excluded(
            candidate_id="stem-honkhiat-rev-6-1",
            topic=topic,
            construction_id="honkhia-honkhiat",
            reference="Revelation 6:1",
            token_indices=(11,),
            confidence="high",
            why_selected="The dossier treats `honkhia ~ honkhiat` as a tempting report-visible pair because exact `honkhiat` does occur once.",
            why_excluded="The solitary `honkhiat` hit and the overwhelmingly lexicalized/compound-like `honkhia` family make this unsafe as simple stem-pair evidence.",
            notes="Problem type: insufficient evidence plus likely lexicalization. The candidate layer keeps the one exact Form II-looking hit visible while blocking it from print promotion.",
            expected_normalized=("honkhiat",),
        ),
    ]


def build_sentence_final_particles_specs() -> list[CandidateSpec]:
    topic = "sentence_final_particles"
    return [
        accepted_with_caveat(
            candidate_id="sfp_hi_gen1_13_ahi_hi",
            topic=topic,
            construction_id="particle-hi-ahi-hi",
            particle_type="declarative",
            particle_form="hi",
            construction_type="copula_plus_declarative_ahi_hi",
            reference="Genesis 1:13",
            token_indices=(10, 11),
            token_indices_style="range",
            confidence="high",
            print_status="print_usable_with_caveat",
            why_selected="Analyzer preserves `ahi hi` in a compact clause-final span, so the first sentence-final packet can keep declarative `hi` visible without pretending the evidence is a bare standalone particle.",
            why_excluded="This is not a bare declarative `hi` row: it bundles copular `ahi` plus final `hi`, so it cannot license raw `hi` harvesting or a claim that every `hi` token is sentence-final declarative.",
            notes="Copula-versus-sentence-final overlap is explicit here; keep `hi` narrow and construction-controlled.",
            expected_normalized=("ahi", "hi"),
        ),
        accepted_with_caveat(
            candidate_id="sfp_hi_gen4_5_lo_hi",
            topic=topic,
            construction_id="particle-hi-lo-hi",
            particle_type="negation_overlap",
            particle_form="hi",
            construction_type="neg_plus_declarative_lo_hi",
            reference="Genesis 4:5",
            token_indices=(6, 7, 8),
            token_indices_style="range",
            confidence="high",
            print_status="print_usable_with_caveat",
            why_selected="`thusim lo hi` keeps one compact negative-plus-declarative row visible in the candidate layer so sentence-final review can register how `hi` clusters with stabilized negation material.",
            why_excluded="This row overlaps the negation packet and should not reopen `lo` analysis or broaden `hi` into every clause-final negative sequence.",
            notes="Negation-overlap control only; cross-reference the stabilized negation packet rather than rebuilding it here.",
            expected_normalized=("thusim", "lo", "hi"),
        ),
        deferred(
            candidate_id="sfp_hiam_gen48_8_overlap_control",
            topic=topic,
            construction_id="particle-hiam-overlap-control",
            particle_type="interrogative_overlap",
            particle_form="hiam",
            construction_type="interrogative_hiam_overlap_control",
            reference="Genesis 48:8",
            token_indices=(9, 10, 11, 12),
            token_indices_style="range",
            confidence="high",
            print_status="not_print_ready",
            why_selected="Sentence-final particle work borders the already stabilized interrogatives packet, so one clause-final `hiam` row is kept as a cross-reference control.",
            why_excluded="`Hiam` already belongs to the interrogatives packet, so this row is overlap control only and must not reopen or duplicate interrogatives analysis.",
            notes="Cross-reference the existing interrogatives packet instead of absorbing `hiam` into a new sentence-final chapter.",
            manual_review_status="needs_followup",
            expected_normalized=("hihte", "kua", "ahi", "hiam"),
        ),
        deferred(
            candidate_id="sfp_tahen_gen9_25_hi_tahen",
            topic=topic,
            construction_id="particle-tahen-jussive",
            particle_type="jussive",
            particle_form="tahen",
            construction_type="jussive_tahen",
            reference="Genesis 9:25",
            token_indices=(12, 13),
            token_indices_style="range",
            confidence="low",
            print_status="not_print_ready",
            why_selected="The generated sentence-final report makes `tahen` worth checking, so the candidate layer keeps one compact `hi tahen` window in view instead of relying on report paraphrase alone.",
            why_excluded="In the current export, `tahen` here is lexical `army` / `N` rather than a clean jussive particle, so the row cannot yet serve as settled sentence-final evidence.",
            notes="The same verse also contains split `ta hen` material earlier in the clause; keep fused-versus-split `tahen`/`ta hen` noise explicit and do not turn this into a broad mood chapter.",
            manual_review_status="needs_followup",
            expected_normalized=("hi", "tahen"),
        ),
        accepted_with_caveat(
            candidate_id="sfp_hen_gen1_3_khuavak_om_hen",
            topic=topic,
            construction_id="particle-hen-optative",
            particle_type="optative",
            particle_form="hen",
            construction_type="optative_hen",
            reference="Genesis 1:3",
            token_indices=(2, 3, 4),
            token_indices_style="range",
            confidence="high",
            print_status="print_usable_with_caveat",
            why_selected="Genesis 1:3 gives a compact analyzer-backed clause-final `hen` row, which is enough to keep optative material visible in a first sentence-final packet.",
            why_excluded="Use this as optative evidence only: do not let the row expand into a broad mood or TAM account, and note that report-style `ta hen` wording is not what the current export preserves in this verse.",
            notes="Optative evidence with a report-versus-export caveat; broad TAM remains deferred.",
            expected_normalized=("khuavak", "om", "hen"),
        ),
        accepted_with_caveat(
            candidate_id="sfp_in_gen6_14_teembaw_khat_bawl_in",
            topic=topic,
            construction_id="particle-in-imperative",
            particle_type="imperative_singular",
            particle_form="in",
            construction_type="imperative_in",
            reference="Genesis 6:14",
            token_indices=(6, 7, 8, 9),
            token_indices_style="range",
            confidence="medium",
            print_status="print_usable_with_caveat",
            why_selected="Verse-final `... bawl in` keeps singular imperative `in` visible in a compact analyzer-backed window for the first sentence-final pass.",
            why_excluded="The current export still glosses this `in` as `ERG` / `FUNC`, and `in` has substantial case-marker overlap elsewhere, so this row must not license raw `in` harvesting.",
            notes="Imperative-versus-case overlap control. The analyzer exports `teembaw` rather than report-style `lawng`, so later prose should stay aligned to the actual candidate span.",
            expected_normalized=("teembaw", "khat", "bawl", "in"),
        ),
        accepted(
            candidate_id="sfp_un_ps100_1_gingsak_un",
            topic=topic,
            construction_id="particle-un-imperative",
            particle_type="imperative_plural",
            particle_form="un",
            construction_type="imperative_un",
            reference="Psalms 100:1",
            token_indices=(7, 8),
            token_indices_style="range",
            confidence="high",
            print_status="print_ready",
            why_selected="`gingsak un` is a compact analyzer-backed imperative plural window and gives the packet one clean `un` anchor.",
            notes="The selected span stays tight so the nearby `aw` material does not get flattened into the same candidate row.",
            expected_normalized=("gingsak", "un"),
        ),
        accepted_with_caveat(
            candidate_id="sfp_aw_ps100_1_gam_khempeuh_aw",
            topic=topic,
            construction_id="particle-aw-vocative",
            particle_type="exclamative_vocative",
            particle_form="aw",
            construction_type="vocative_aw",
            reference="Psalms 100:1",
            token_indices=(0, 1, 2),
            token_indices_style="range",
            confidence="medium",
            print_status="not_print_ready",
            why_selected="`Gam khempeuh aw` keeps report-visible `aw` in the candidate layer as vocative or exclamative boundary evidence rather than letting it disappear from the first pass.",
            why_excluded="The current export glosses `aw` lexically as `voice`, and this verse also contains a second `aw` in `lungdamna aw`, so the row should stay vocative/exclamative boundary material rather than a generalized sentence-final particle entry.",
            notes="Do not treat every `aw` token as sentence-final mood marking without constructional review.",
            expected_normalized=("gam", "khempeuh", "aw"),
        ),
        needs_review(
            candidate_id="sfp_ta_gen40_23_mangngilh_ta_hi",
            topic=topic,
            construction_id="particle-ta-boundary",
            particle_type="tam_overlap",
            particle_form="ta",
            construction_type="aspect_plus_decl_ta_hi",
            reference="Genesis 40:23",
            token_indices=(12, 13, 14),
            token_indices_style="range",
            confidence="low",
            print_status="not_print_ready",
            why_selected="`mangngilh ta hi` keeps report-visible `ta hi` boundary material explicit without starting a broad TAM chapter.",
            why_excluded="The current export glosses `ta` here as ambiguous `child` / `FUNC` rather than a clean perfective particle, so this row remains boundary evidence only.",
            notes="TAM-overlap control only; broad aspectual prose remains deferred.",
            manual_review_status="needs_followup",
            expected_normalized=("mangngilh", "ta", "hi"),
        ),
        deferred(
            candidate_id="sfp_zo_gen1_28_zo_boundary",
            topic=topic,
            construction_id="particle-zo-boundary",
            particle_type="tam_overlap",
            particle_form="zo",
            construction_type="completive_zo_boundary",
            reference="Genesis 1:28",
            token_indices=(17,),
            confidence="low",
            print_status="not_print_ready",
            why_selected="The generated sentence-final report points toward completive `zo`, so the first candidate layer keeps one analyzer-backed `zo` token visible rather than relying on report counts or schematic examples.",
            why_excluded="The current export glosses this `zo` as ambiguous lexical `south` / `N` rather than as a clean completive particle, so `zo` remains deferred in the sentence-final packet.",
            notes="Keep `zo` as TAM-overlap boundary material only until a cleaner analyzer-backed completive row is found.",
            manual_review_status="needs_followup",
            expected_normalized=("zo",),
        ),
    ]


def build_specs(topic: str) -> list[CandidateSpec]:
    if topic == "demonstratives":
        return build_demonstratives_specs()
    if topic == "case_marking":
        return build_case_marking_specs()
    if topic == "coordinators":
        return build_coordinators_specs()
    if topic == "interrogatives":
        return build_interrogatives_specs()
    if topic == "numerals":
        return build_numerals_specs()
    if topic == "negation":
        return build_negation_specs()
    if topic == "pronouns":
        return build_pronouns_specs()
    if topic == "quantifiers":
        return build_quantifiers_specs()
    if topic == "sentence_final_particles":
        return build_sentence_final_particles_specs()
    if topic == "stem_alternation":
        return build_stem_alternation_specs()
    raise SystemExit(f"Unsupported topic: {topic}")


def candidate_columns(topic: str) -> list[str]:
    if topic == "case_marking":
        return CASE_MARKING_CANDIDATE_COLUMNS
    if topic == "coordinators":
        return COORDINATORS_CANDIDATE_COLUMNS
    if topic == "interrogatives":
        return INTERROGATIVES_CANDIDATE_COLUMNS
    if topic == "numerals":
        return NUMERALS_CANDIDATE_COLUMNS
    if topic == "quantifiers":
        return QUANTIFIERS_CANDIDATE_COLUMNS
    if topic == "sentence_final_particles":
        return SENTENCE_FINAL_PARTICLES_CANDIDATE_COLUMNS
    return DEFAULT_CANDIDATE_COLUMNS


def write_candidates(topic: str, output_path: Path) -> None:
    require_tokens_export()
    verses = load_verse_metadata()
    tokens_by_verse = load_tokens()
    specs = build_specs(topic)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=candidate_columns(topic),
            delimiter="\t",
            extrasaction="ignore",
            lineterminator="\n",
        )
        writer.writeheader()
        for spec in specs:
            verse_meta = verses.get(spec.reference)
            if verse_meta is None:
                raise SystemExit(f"Reference not found in data/verses_aligned.tsv: {spec.reference}")
            writer.writerow(candidate_row(spec, verse_meta, tokens_by_verse))

    try:
        display_path = output_path.relative_to(ROOT)
    except ValueError:
        display_path = output_path

    print(f"Wrote {display_path} using data/ctd_analysis/tokens.tsv")


def main() -> None:
    args = parse_args()
    if args.list_topics:
        list_topics()
        return

    output_path = args.output or OUTPUT_DIR / f"candidates_{args.topic}.tsv"
    write_candidates(args.topic, output_path)


if __name__ == "__main__":
    main()
