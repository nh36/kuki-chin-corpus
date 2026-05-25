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
SUPPORTED_TOPICS = ("demonstratives",)

CANDIDATE_COLUMNS = [
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


def accepted(**kwargs: object) -> CandidateSpec:
    return CandidateSpec(candidate_status="accepted", manual_review_status="reviewed", **kwargs)


def excluded(**kwargs: object) -> CandidateSpec:
    return CandidateSpec(candidate_status="excluded", manual_review_status="reviewed", **kwargs)


def deferred(**kwargs: object) -> CandidateSpec:
    return CandidateSpec(candidate_status="deferred", manual_review_status="reviewed", **kwargs)


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
        "verse_id": verse_meta.verse_id,
        "reference": verse_meta.reference,
        "surface_span": " ".join(token.surface_form for token in selected),
        "token_indices": ",".join(str(token.token_index) for token in selected),
        "segmentation_span": " | ".join(token.segmentation for token in selected),
        "gloss_span": " | ".join(token.gloss for token in selected),
        "lemma_span": " | ".join(token.lemma for token in selected),
        "pos_span": " | ".join(token.pos for token in selected),
        "kjv": verse_meta.kjv,
        "candidate_status": spec.candidate_status,
        "confidence": spec.confidence,
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


def build_specs(topic: str) -> list[CandidateSpec]:
    if topic == "demonstratives":
        return build_demonstratives_specs()
    raise SystemExit(f"Unsupported topic: {topic}")


def write_candidates(topic: str, output_path: Path) -> None:
    require_tokens_export()
    verses = load_verse_metadata()
    tokens_by_verse = load_tokens()
    specs = build_specs(topic)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CANDIDATE_COLUMNS, delimiter="\t")
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
