#!/usr/bin/env python3
"""
Extract analyzer-aware publication-review candidate files.

This script establishes a reusable scaffold for publication-review evidence
work. The current pilot topic is demonstratives/deixis, using the exported
Tedim token analysis in data/ctd_analysis/tokens.tsv.

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
    python3 scripts/publication_review/extract_candidates.py interrogatives
    python3 scripts/publication_review/extract_candidates.py negation
    python3 scripts/publication_review/extract_candidates.py pronouns
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
    "interrogatives",
    "negation",
    "pronouns",
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


def build_specs(topic: str) -> list[CandidateSpec]:
    if topic == "demonstratives":
        return build_demonstratives_specs()
    if topic == "case_marking":
        return build_case_marking_specs()
    if topic == "interrogatives":
        return build_interrogatives_specs()
    if topic == "negation":
        return build_negation_specs()
    if topic == "pronouns":
        return build_pronouns_specs()
    if topic == "stem_alternation":
        return build_stem_alternation_specs()
    raise SystemExit(f"Unsupported topic: {topic}")


def candidate_columns(topic: str) -> list[str]:
    if topic == "case_marking":
        return CASE_MARKING_CANDIDATE_COLUMNS
    if topic == "interrogatives":
        return INTERROGATIVES_CANDIDATE_COLUMNS
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
