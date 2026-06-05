#!/usr/bin/env python3
"""Assemble the publication-review grammar preview into Markdown, TeX, and PDF.

The Markdown preview remains a readable assembled draft built from the committed
publication-review grammar slices. The TeX/PDF path is richer:

1. Pandoc runs with natbib/BibTeX against `literature/bibliography.bib`, so
   Markdown citation syntax resolves into real author-year citations and a
   References section.
2. Slice example blocks of the form

       (@ex:label) Source
       a. Tedim: ...
       b. Segmentation: ...
       c. Gloss: ...
       d. Translation: ...

   are converted into chapter-numbered gb4e examples using the shared analyzer,
   tone-restoration, Bible-reference, and Leipzig-gloss helpers from
   `scripts/interlinear_latex.py`.

The resulting PDF is still a review preview, not a final publication PDF.
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from restore_tone import load_tone_dictionary

from interlinear_latex import (
    analyze_text,
    build_gll_lines,
    escape_latex,
    format_reference,
    format_inline_tedim,
    generate_abbreviations_section,
    generate_gb4e_setup,
    load_bible,
    normalize_text_for_matching,
    reference_to_verse_id,
)


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_REVIEW_DIR = ROOT / "output" / "publication_review"
MARKDOWN_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.md"
TEX_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.tex"
PDF_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.pdf"
BIBLIOGRAPHY_PATH = ROOT / "literature" / "bibliography.bib"
BIBLIOGRAPHY_RELATIVE = Path("../../literature/bibliography.bib")
BIBLE_PATH = ROOT / "bibles" / "extracted" / "ctd" / "ctd-x-bible.txt"

PANDOC_FALLBACKS = [
    "/opt/homebrew/bin/pandoc",
    "/usr/local/bin/pandoc",
]

XELATEX_FALLBACKS = [
    "/Library/TeX/texbin/xelatex",
    "/usr/local/texlive/2024/bin/universal-darwin/xelatex",
    "/usr/local/texlive/2025/bin/universal-darwin/xelatex",
]

BIBTEX_FALLBACKS = [
    "/Library/TeX/texbin/bibtex",
    "/usr/local/texlive/2024/bin/universal-darwin/bibtex",
    "/usr/local/texlive/2025/bin/universal-darwin/bibtex",
]

FRONTMATTER_SECTION_TITLES = {"Review preview status"}

ASSEMBLY_SPEC = [
    {
        "title": "1. Phonology and tone",
        "items": [
            {
                "type": "gap",
                "text": "[MAJOR GAP: phonology/tone remains blocked or theory-heavy.]",
                "explanation": (
                    "The controlling checkpoints and audit still treat phonology/tone as blocked or theory-heavy, "
                    "so no publication-review grammar slice is inlined here yet."
                ),
            }
        ],
    },
    {
        "title": "2. Deixis, pronouns, and nominal domain",
        "items": [
            {"type": "slice", "title": "Demonstratives / deixis", "path": "output/publication_review/grammar_demonstratives_print_slice.md"},
            {"type": "slice", "title": "Pronouns / clusivity", "path": "output/publication_review/grammar_pronouns_print_slice.md"},
            {"type": "slice", "title": "NP structure / possession", "path": "output/publication_review/grammar_np_possession_print_slice.md"},
            {"type": "slice", "title": "Noun domain", "path": "output/publication_review/grammar_noun_domain_print_slice.md"},
            {"type": "slice", "title": "Case marking", "path": "output/publication_review/grammar_case_marking_print_slice.md"},
            {"type": "slice", "title": "Relators / postpositions", "path": "output/publication_review/grammar_relators_postpositions_print_slice.md"},
            {"type": "slice", "title": "Numerals", "path": "output/publication_review/grammar_numerals_print_slice.md"},
            {"type": "slice", "title": "Quantifiers", "path": "output/publication_review/grammar_quantifiers_print_slice.md"},
        ],
    },
    {
        "title": "3. Predicate structure and verbal morphology",
        "items": [
            {"type": "slice", "title": "Stem alternation", "path": "output/publication_review/grammar_stem_alternation_print_slice.md"},
            {
                "type": "gap",
                "title": "Verb paradigms",
                "text": "[MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]",
                "explanation": (
                    "`docs/grammar/reports/05-verb-00-paradigm-tables.md` remains part of the evidence base, "
                    "but it has not yet been converted into a review-note-stage packet with an assembled grammar slice."
                ),
            },
            {"type": "slice", "title": "Prefix / agreement", "path": "output/publication_review/grammar_prefix_agreement_print_slice.md"},
            {"type": "slice", "title": "Transitivity", "path": "output/publication_review/grammar_transitivity_print_slice.md"},
            {"type": "slice", "title": "VP structure / suffix stacking", "path": "output/publication_review/grammar_vp_structure_stacking_print_slice.md"},
            {"type": "slice", "title": "TAM / aspect / modal", "path": "output/publication_review/grammar_tam_print_slice.md"},
            {"type": "slice", "title": "Directionals", "path": "output/publication_review/grammar_directionals_print_slice.md"},
            {"type": "slice", "title": "Derivation / valency", "path": "output/publication_review/grammar_derivation_valency_print_slice.md"},
            {"type": "slice", "title": "Nominalization", "path": "output/publication_review/grammar_nominalization_print_slice.md"},
            {"type": "slice", "title": "Clause linkage", "path": "output/publication_review/grammar_clause_linkage_print_slice.md"},
        ],
    },
    {
        "title": "4. Clause type, discourse-facing material, and expressive morphology",
        "items": [
            {"type": "slice", "title": "Negation", "path": "output/publication_review/grammar_negation_print_slice.md"},
            {"type": "slice", "title": "Interrogatives", "path": "output/publication_review/grammar_interrogatives_print_slice.md"},
            {"type": "slice", "title": "Sentence-final particles", "path": "output/publication_review/grammar_sentence_final_particles_print_slice.md"},
            {"type": "slice", "title": "Coordinators", "path": "output/publication_review/grammar_coordinators_print_slice.md"},
            {"type": "slice", "title": "Reduplication", "path": "output/publication_review/grammar_reduplication_print_slice.md"},
            {
                "type": "gap",
                "title": "Broader discourse",
                "text": "[MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]",
                "explanation": (
                    "Current packetized material reaches clause type and sentence-final behavior, but a broader "
                    "discourse packet is still only partly surfaced and remains boundary-heavy."
                ),
            },
            {
                "type": "gap",
                "title": "Analyzer-gap caution",
                "text": "[MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]",
                "explanation": (
                    "Analyzer-gap topics still cut across tone in `-a`, conditioned variants, hong-/kong-, `-sak`, "
                    "`-pih`, and related cross-packet boundaries, so they remain visible blockers rather than "
                    "assembled review prose."
                ),
            },
        ],
    },
]

EXAMPLE_HEADER_RE = re.compile(r"^\((@ex:[^)]+)\)(?:\s+(.+?))?\s*$")
EXAMPLE_PART_RE = {
    "tedim": re.compile(r"^a\. Tedim:\s*(.+?)\s*$"),
    "segmentation": re.compile(r"^b\. Segmentation:\s*(.+?)\s*$"),
    "gloss": re.compile(r"^c\. Gloss:\s*(.+?)\s*$"),
    "translation": re.compile(r"^d\. Translation:\s*(.+?)\s*$"),
}

CHAPTER_HEADING_RE = re.compile(r"^#\s+(\d+)\.\s+(.+?)\s*$")
CITATION_KEY_RE = re.compile(r"(?<![`\\])@(?!ex:)([A-Za-z0-9_:+.-]+)")
BIBLIOGRAPHY_KEY_RE = re.compile(r"@\w+\{([^,]+),")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
MARKDOWN_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
INLINE_GLOSS_QUOTE_RE = re.compile(r"(?<![A-Za-z])['‘’]((?:[^'\n]|'[A-Za-z])+?)['’](?![A-Za-z])")
SCRIPTURE_BOOKS = (
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms?",
    "Proverbs",
    "Ecclesiastes",
    "Song of Songs",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
)
SCRIPTURE_REFERENCE_RE = re.compile(
    rf"\b(?:{'|'.join(SCRIPTURE_BOOKS)})\s+\d+:\d+\b"
)

TECHNICAL_PATH_PREFIXES = ("output/", "docs/", "scripts/", "tests/", "data/", "literature/", "bibles/")
TECHNICAL_FILE_SUFFIXES = (".md", ".py", ".tex", ".pdf", ".tsv", ".bib", ".json", ".txt", ".yaml", ".yml")
TECHNICAL_COMMAND_PREFIXES = ("python3", "make", "pytest", "xelatex", "pandoc", "git", "bibtex", "pdftotext")
SOURCE_AUDIT_EXCEPTIONS: set[str] = set()
TARGET_QUALITY_GATE_SECTION_TITLES = {
    "Numerals",
    "Quantifiers",
    "NP structure / possession",
    "Noun domain",
    "Case marking",
    "Relators / postpositions",
    "Derivation / valency",
    "VP structure / suffix stacking",
    "TAM / aspect / modal",
    "Directionals",
}
NO_SOURCE_AVAILABLE_RE = re.compile(r"\b(?:no[- ]source[- ]available|source unavailable)\b", re.IGNORECASE)
NORMALIZATION_SUPPLEMENT_PATHS = (
    PUBLICATION_REVIEW_DIR / "examples_numerals_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_quantifiers_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_np_possession_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_noun_domain_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_case_marking_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_relators_postpositions_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_derivation_valency_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_vp_structure_stacking_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_tam_normalization.tsv",
    PUBLICATION_REVIEW_DIR / "examples_directionals_normalization.tsv",
)
GRAMMAR_FACING_INTERNAL_SECTION_TITLES = {"Scope", "Editorial scope"}
GRAMMAR_FACING_DROP_SENTENCE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"\bif the project later wants\b", re.IGNORECASE),
    re.compile(r"\bthe next (?:editorial )?step\b", re.IGNORECASE),
    re.compile(r"\bready for human review\b", re.IGNORECASE),
    re.compile(r"\breview-note work\b", re.IGNORECASE),
    re.compile(r"\b(?:this|that) commit\b", re.IGNORECASE),
    re.compile(r"\b(?:tests?/|scripts?/|output/|docs/|bibles/)", re.IGNORECASE),
)
GRAMMAR_FACING_SECTION_INTROS = {
    "NP structure / possession": (
        "The current evidence supports demonstrative-before-noun order alongside noun-plus-postnominal numeral "
        "and quantifier patterns, with possession kept as a cautious boundary subsection."
    ),
    "Noun domain": (
        "The noun-domain evidence is strongest for simple stems such as `gam` 'land / country' and `aksi` 'star', "
        "for plural `-te`, and for nouns that remain visible as heads inside larger phrases."
    ),
    "Case marking": (
        "The current case evidence centers on `-ah` 'locative / goal-like' and `-in` 'ergative / agentive', "
        "while `-pan` 'source / ablative', `-panin` 'source / departure', and `-tawh` 'with' remain more cautious oblique extensions."
    ),
    "Relators / postpositions": (
        "The current evidence supports relational nouns such as `sung` 'inside', `tung` 'on / upon', "
        "`kiang` 'beside / near', and `lak` 'among / midst', together with postpositional source patterns that close the larger phrase."
    ),
    "Derivation / valency": (
        "The current derivation and valency evidence is strongest around `-sak` 'causative / benefactive', "
        "especially `paisak` 'cause to go' and `muhsak` 'show / make see', while `-pih` 'with / accompanying', "
        "`ki-` 'reflexive / middle / passive-like', and heavier suffix stacks remain boundary material."
    ),
    "VP structure / suffix stacking": (
        "The current VP-structure evidence is strongest for a small checked set of suffix stacks such as "
        "`bawlzoding` 'make-COMPL-IRR', directional-plus-irrealis sequences, modal-plus-irrealis strings, "
        "and derivational stacks whose ordering can be discussed without forcing a full verb-template chapter."
    ),
    "Numerals": (
        "The current numeral evidence supports a decimal system with basic cardinals, counted noun phrases, "
        "and `-na` ordinals, while larger-number and classifier-like material remain explicit boundary notes."
    ),
    "Quantifiers": (
        "The current quantifier evidence centers on `khempeuh` 'all', `pawlkhat` 'some people', "
        "`kuamah` 'nobody', `bangmah` 'nothing', and noun-plus-quantifier phrases such as `mi tampi` 'many people'."
    ),
    "Directionals": (
        "The current directional evidence is strongest for post-verbal forms such as `-khia` 'outward', "
        "`-khiat` 'away', `-toh` 'upward', `-sawn` 'toward', and `-suk` 'downward', while deictic prefixes remain separate."
    ),
    "TAM / aspect / modal": (
        "The current TAM evidence is strongest for a small checked set of aspectual and modal anchors such as "
        "`-ta` 'completive / change-of-state', `-zo` 'already / completive', `-gige` 'habitually / always', "
        "`-ding` 'prospective / irrealis', `-thei` 'can / be able', and `-kik` 'again / back'."
    ),
}
GRAMMAR_FACING_TECHNICAL_REFERENCE_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"`(?:output/publication_review/)?candidates_[^`]+\.tsv`"), "the checked evidence tables"),
    (re.compile(r"`(?:output/publication_review/)?dossier_[^`]+\.md`"), "background notes"),
    (re.compile(r"`(?:output/publication_review/)?review_notes_[^`]+\.md`"), "background notes"),
    (re.compile(r"`(?:output/publication_review/)?whole_grammar_coverage_audit\.md`"), "the whole-grammar audit"),
    (re.compile(r"`(?:docs/grammar/(?:reports|lit-reviews)/)[^`]+`"), "background review material"),
    (re.compile(r"`(?:tests/test_[^`]+|scripts/[^`]+)`"), "the current workflow"),
    (re.compile(r"`(?:output/publication_review/)?grammar_[^`]+\.md`"), "the present section"),
]
GRAMMAR_FACING_REPLACEMENTS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bcurrent packet\b", re.IGNORECASE), "current evidence"),
    (re.compile(r"\bpacket anchors\b", re.IGNORECASE), "main anchors"),
    (re.compile(r"\bpacket anchor\b", re.IGNORECASE), "main anchor"),
    (re.compile(r"\bpacketized\b", re.IGNORECASE), "assembled"),
    (re.compile(r"\bpacket-status\b", re.IGNORECASE), "section"),
    (re.compile(r"\bpackets\b", re.IGNORECASE), "sections"),
    (re.compile(r"\bpacket\b", re.IGNORECASE), "section"),
    (re.compile(r"\bpublication-review\b", re.IGNORECASE), "review"),
    (re.compile(r"\bnormalized section\b", re.IGNORECASE), "section"),
    (re.compile(r"\bpublication-facing\b", re.IGNORECASE), ""),
    (re.compile(r"\bcandidate TSV\b", re.IGNORECASE), "evidence table"),
    (re.compile(r"\bcandidate-backed\b", re.IGNORECASE), "checked"),
    (re.compile(r"\bcandidate-controlled\b", re.IGNORECASE), "checked"),
    (re.compile(r"\bcandidate discipline\b", re.IGNORECASE), "careful evidence control"),
    (re.compile(r"\bcandidate control\b", re.IGNORECASE), "careful evidence control"),
    (re.compile(r"\bcandidate evidence\b", re.IGNORECASE), "checked evidence"),
    (re.compile(r"\bcandidate layer\b", re.IGNORECASE), "checked evidence"),
    (re.compile(r"\bcandidate rows\b", re.IGNORECASE), "checked examples"),
    (re.compile(r"\bcandidate row\b", re.IGNORECASE), "checked example"),
    (re.compile(r"\bprint slice\b", re.IGNORECASE), "section"),
    (re.compile(r"\bCurrent print status\b"), "Status in this draft"),
    (re.compile(r"\bCurrent print policy\b"), "Current treatment"),
    (re.compile(r"\bprint-ready\b", re.IGNORECASE), "well-supported"),
    (re.compile(r"\bprint-usable with caveat\b", re.IGNORECASE), "supported with caveat"),
    (re.compile(r"\bedge row only\b", re.IGNORECASE), "boundary item"),
    (re.compile(r"\bprint use\b", re.IGNORECASE), "discussion here"),
    (re.compile(r"\bprint purposes\b", re.IGNORECASE), "present purposes"),
    (re.compile(r"\bpublication prose\b", re.IGNORECASE), "the present discussion"),
    (re.compile(r"\bcoverage-normalization\b", re.IGNORECASE), "editorial"),
    (re.compile(r"\bcoverage normalization\b", re.IGNORECASE), "editorial standard"),
    (re.compile(r"\bdossier\b", re.IGNORECASE), "background notes"),
    (re.compile(r"\breview-note\b", re.IGNORECASE), "background"),
    (re.compile(r"\breview notes\b", re.IGNORECASE), "background notes"),
    (re.compile(r"\bthis pass\b", re.IGNORECASE), "here"),
    (re.compile(r"\bcurrent pass\b", re.IGNORECASE), "current stage"),
    (re.compile(r"\bready for human review\b", re.IGNORECASE), "keeps the analysis deliberately narrow"),
    (re.compile(r"\bcontrolling files\b", re.IGNORECASE), "background materials"),
    (re.compile(r"\bsource files\b", re.IGNORECASE), "background materials"),
]


@dataclass(frozen=True)
class ParsedExample:
    label: str
    source: str
    tedim: str
    segmentation: str
    gloss: str
    translation: str


@dataclass(frozen=True)
class SourceAuditRecord:
    label: str
    source: str
    rendered_source: str


@dataclass(frozen=True)
class NormalizationSupplementRow:
    example_id: str
    source_reference: str
    tedim_text: str
    segmentation: str
    translation: str
    path: Path
    row_number: int


@dataclass(frozen=True)
class ExampleSourceResolution:
    resolved_source: str
    header_source: str
    contextual_source: str
    supplement_sources: tuple[str, ...]
    inferred_source: str
    supplement_example_ids: tuple[str, ...]
    explicit_no_source: bool
    require_source: bool
    conflict_message: str


def strip_yaml_front_matter(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return "\n".join(lines[index + 1 :]).lstrip("\n")
    return text


def adjust_heading_levels(text: str, increment: int = 2) -> str:
    adjusted_lines: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})(\s+.*)$", line)
        if match:
            level = min(6, len(match.group(1)) + increment)
            adjusted_lines.append("#" * level + match.group(2))
        else:
            adjusted_lines.append(line)
    return "\n".join(adjusted_lines).rstrip() + "\n"


def strip_markdown_sections(text: str, titles: set[str]) -> str:
    output: list[str] = []
    skip_level: int | None = None

    for line in text.splitlines():
        heading_match = MARKDOWN_HEADING_RE.match(line)
        if skip_level is not None:
            if heading_match and len(heading_match.group(1)) <= skip_level:
                skip_level = None
            else:
                continue

        if heading_match and heading_match.group(2).strip() in titles:
            skip_level = len(heading_match.group(1))
            continue

        output.append(line)

    return "\n".join(output).strip() + "\n"


def rewrite_grammar_facing_line(line: str) -> str:
    rewritten = line
    for pattern, replacement in GRAMMAR_FACING_TECHNICAL_REFERENCE_REPLACEMENTS:
        rewritten = pattern.sub(replacement, rewritten)
    for pattern, replacement in GRAMMAR_FACING_REPLACEMENTS:
        rewritten = pattern.sub(replacement, rewritten)
    if not rewritten.strip():
        return ""
    if any(pattern.search(rewritten) for pattern in GRAMMAR_FACING_DROP_SENTENCE_PATTERNS):
        sentences = re.split(r"(?<=[.?!])\s+", rewritten)
        kept_sentences = [
            sentence
            for sentence in sentences
            if sentence.strip() and not any(pattern.search(sentence) for pattern in GRAMMAR_FACING_DROP_SENTENCE_PATTERNS)
        ]
        rewritten = " ".join(kept_sentences)
    rewritten = re.sub(r"\s{2,}", " ", rewritten)
    rewritten = rewritten.replace(" .", ".").replace(" ,", ",").replace(" ;", ";").replace(" :", ":")
    return rewritten.strip() if rewritten.strip() else ""


def rewrite_grammar_facing_text(text: str) -> str:
    rewritten_lines = [rewrite_grammar_facing_line(line) if line.strip() else "" for line in text.splitlines()]
    return "\n".join(rewritten_lines).strip() + "\n"


def grammar_facing_gap_text(item: dict[str, object]) -> str:
    title = str(item.get("title", "")).strip()
    raw_text = str(item.get("text", "")).lower()

    if "phonology/tone" in raw_text:
        return "A full discussion of phonology and tone is not yet included in this review preview."
    if title == "Verb paradigms":
        return "A full discussion of verbal paradigms is not yet included in this draft."
    if title == "Broader discourse":
        return "A fuller treatment of discourse structure is not yet included in this draft."
    if title == "Analyzer-gap caution":
        return "Several cross-cutting morphological issues remain unresolved and are not yet integrated into this draft."
    return "This topic remains outside the present draft."


def find_executable(name: str, fallbacks: list[str]) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for fallback in fallbacks:
        if os.path.exists(fallback):
            return fallback
    return None


def read_slice(path_text: str, grammar_facing: bool = True) -> str | None:
    path = ROOT / path_text
    if not path.exists():
        return None
    text = adjust_heading_levels(strip_yaml_front_matter(path.read_text(encoding="utf-8")))
    if grammar_facing:
        text = strip_markdown_sections(text, GRAMMAR_FACING_INTERNAL_SECTION_TITLES)
        text = rewrite_grammar_facing_text(text)
    return text


def build_markdown(grammar_facing: bool = True) -> str:
    if grammar_facing:
        lines: list[str] = [
            "---",
            'title: "Assembled Tedim Grammar Review Preview"',
            'subtitle: "Not a finished grammar"',
            'date: ""',
            "---",
            "",
            "# Review preview status",
            "",
            "This is a review preview, not a finished grammar. It is an assembled draft of the current Tedim grammar sections.",
            "",
            "Several domains remain incomplete, and end-of-section caveats remain visible while the draft is still under review.",
            "",
        ]
    else:
        lines = [
            "---",
            'title: "Assembled Tedim Grammar Review Preview"',
            'subtitle: "Not a finished grammar"',
            'date: ""',
            "---",
            "",
            "# Review preview status",
            "",
            "This is a review preview, not a finished grammar.",
            "",
        ]

    for chapter in ASSEMBLY_SPEC:
        lines.extend([f"# {chapter['title']}", ""])
        for item in chapter["items"]:
            if item["type"] == "slice":
                lines.extend([f"## {item['title']}", ""])
                if grammar_facing and item["title"] in GRAMMAR_FACING_SECTION_INTROS:
                    lines.extend([GRAMMAR_FACING_SECTION_INTROS[item["title"]], ""])
                if not grammar_facing:
                    lines.extend([f"*Source slice: `{item['path']}`*", ""])
                content = read_slice(item["path"], grammar_facing=grammar_facing)
                if content is None:
                    if grammar_facing:
                        lines.extend(["This section is not yet available in the assembled draft.", ""])
                    else:
                        lines.extend([f"[REVIEW PREVIEW GAP: expected grammar slice not found: {item['path']}]", ""])
                else:
                    lines.extend([content.rstrip(), ""])
            else:
                if item.get("title"):
                    lines.extend([f"## {item['title']}", ""])
                if grammar_facing:
                    lines.extend([grammar_facing_gap_text(item), ""])
                else:
                    lines.extend([item["text"], "", item["explanation"], ""])

    if not grammar_facing:
        lines.extend(
            [
                "# End state of this preview",
                "",
                "This assembled review preview contains the actual prose of the current first-pass review grammar slices in a single ordered draft. It does not claim that the whole grammar is finished, and the generated PDF is a review preview PDF rather than a final publication PDF.",
                "",
            ]
        )
    return "\n".join(lines)


def load_bibliography_keys(path: Path) -> set[str]:
    return set(BIBLIOGRAPHY_KEY_RE.findall(path.read_text(encoding="utf-8")))


def extract_citation_keys(text: str) -> set[str]:
    return set(CITATION_KEY_RE.findall(text))


def validate_citations(markdown_text: str, bibliography_path: Path) -> None:
    cited = extract_citation_keys(markdown_text)
    if not cited:
        return
    available = load_bibliography_keys(bibliography_path)
    missing = sorted(cited - available)
    if missing:
        raise RuntimeError(f"Missing bibliography keys for assembled preview: {', '.join(missing)}")


def parse_example_at(lines: list[str], start: int) -> tuple[ParsedExample | None, int]:
    match = EXAMPLE_HEADER_RE.match(lines[start])
    if not match:
        return None, start + 1

    if start + 4 >= len(lines):
        warning = ParsedExample(
            label="review-preview-warning",
            source="Malformed example header",
            tedim=f"[REVIEW PREVIEW WARNING: malformed example block near {match.group(1)}]",
            segmentation="",
            gloss="",
            translation="",
        )
        return warning, len(lines)

    tedim_match = EXAMPLE_PART_RE["tedim"].match(lines[start + 1])
    segmentation_match = EXAMPLE_PART_RE["segmentation"].match(lines[start + 2])
    gloss_match = EXAMPLE_PART_RE["gloss"].match(lines[start + 3])
    translation_match = EXAMPLE_PART_RE["translation"].match(lines[start + 4])

    if not all((tedim_match, segmentation_match, gloss_match, translation_match)):
        warning = ParsedExample(
            label="review-preview-warning",
            source="Malformed example block",
            tedim=f"[REVIEW PREVIEW WARNING: malformed example block near {match.group(1)}]",
            segmentation="",
            gloss="",
            translation="",
        )
        return warning, start + 1

    return (
        ParsedExample(
            label=match.group(1).lstrip("@"),
            source=normalize_quote_marks((match.group(2) or "").strip()),
            tedim=normalize_quote_marks(tedim_match.group(1).strip()),
            segmentation=normalize_quote_marks(segmentation_match.group(1).strip()),
            gloss=normalize_quote_marks(gloss_match.group(1).strip()),
            translation=normalize_quote_marks(translation_match.group(1).strip()),
        ),
        start + 5,
    )


def parse_examples(markdown_text: str) -> list[ParsedExample]:
    examples: list[ParsedExample] = []
    lines = markdown_text.splitlines()
    index = 0

    while index < len(lines):
        parsed_example, next_index = parse_example_at(lines, index)
        if parsed_example:
            examples.append(parsed_example)
            index = next_index
            continue
        index += 1

    return examples


def extract_preceding_prose(lines: list[str], start: int) -> str:
    paragraph_lines: list[str] = []
    index = start - 1

    while index >= 0:
        raw_line = lines[index]
        stripped = raw_line.strip()
        if not stripped:
            if paragraph_lines:
                break
            index -= 1
            continue
        if (
            MARKDOWN_HEADING_RE.match(stripped)
            or EXAMPLE_HEADER_RE.match(stripped)
            or stripped.startswith("|")
            or stripped.startswith(">")
            or stripped.startswith("```")
            or stripped.startswith("*Source slice:")
        ):
            break
        paragraph_lines.insert(0, stripped)
        index -= 1

    return " ".join(paragraph_lines).strip()


def find_contextual_example_source(lines: list[str], start: int) -> str:
    preceding_prose = extract_preceding_prose(lines, start)
    if not preceding_prose:
        return ""
    matches = SCRIPTURE_REFERENCE_RE.findall(preceding_prose)
    unique_matches = list(dict.fromkeys(matches))
    if len(unique_matches) == 1:
        return unique_matches[0]
    return ""


def infer_example_source_from_bible(example: ParsedExample, bible: dict[str, str]) -> str:
    tedim_norm = normalize_text_for_matching(example.tedim)
    if not tedim_norm:
        return ""

    matches = [
        verse_id
        for verse_id, verse_text in bible.items()
        if tedim_norm in normalize_text_for_matching(verse_text)
    ]
    if len(matches) == 1:
        return format_reference(matches[0])
    return ""


def strip_outer_quotes(text: str) -> str:
    stripped = text.strip()
    paired_quotes = [
        ("'", "'"),
        ('"', '"'),
        ("‘", "’"),
        ("“", "”"),
    ]
    for left, right in paired_quotes:
        if stripped.startswith(left) and stripped.endswith(right) and len(stripped) >= 2:
            return stripped[1:-1].strip()
    return stripped


def normalize_for_comparison(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def heading_path_requires_example_source(heading_path: tuple[str, ...]) -> bool:
    return any(title in TARGET_QUALITY_GATE_SECTION_TITLES for title in heading_path)


def normalize_example_text_for_match(text: str) -> str:
    normalized = strip_outer_quotes(normalize_quote_marks(text))
    normalized = re.sub(r"\s+", " ", normalized.strip())
    return normalized.casefold()


def load_normalization_supplements() -> tuple[NormalizationSupplementRow, ...]:
    rows: list[NormalizationSupplementRow] = []
    for path in NORMALIZATION_SUPPLEMENT_PATHS:
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter="\t")
            for row_number, row in enumerate(reader, start=2):
                rows.append(
                    NormalizationSupplementRow(
                        example_id=(row.get("example_id") or "").strip(),
                        source_reference=(row.get("source_reference") or "").strip(),
                        tedim_text=(row.get("tedim_text") or "").strip(),
                        segmentation=(row.get("segmentation") or "").strip(),
                        translation=(row.get("translation") or "").strip(),
                        path=path,
                        row_number=row_number,
                    )
                )
    return tuple(rows)


def match_normalization_supplement_rows(
    example: ParsedExample, supplement_rows: tuple[NormalizationSupplementRow, ...]
) -> tuple[NormalizationSupplementRow, ...]:
    tedim_key = normalize_example_text_for_match(example.tedim)
    if not tedim_key:
        return ()

    tedim_matches = [row for row in supplement_rows if normalize_example_text_for_match(row.tedim_text) == tedim_key]
    if not tedim_matches:
        return ()

    translation_key = normalize_example_text_for_match(example.translation)
    translation_matches = [
        row for row in tedim_matches if normalize_example_text_for_match(row.translation) == translation_key
    ]
    if translation_matches:
        return tuple(translation_matches)

    segmentation_key = normalize_example_text_for_match(example.segmentation)
    segmentation_matches = [
        row for row in tedim_matches if normalize_example_text_for_match(row.segmentation) == segmentation_key
    ]
    if segmentation_matches:
        return tuple(segmentation_matches)

    unique_sources = {row.source_reference for row in tedim_matches if row.source_reference}
    if len(unique_sources) == 1:
        return tuple(tedim_matches)

    return ()


def render_example_source(source: str, bible: dict[str, str]) -> str:
    source = source.strip()
    if not source:
        return ""

    verse_id = reference_to_verse_id(source)
    if verse_id and verse_id in bible:
        return format_reference(verse_id)
    return source


def resolve_example_source(example: ParsedExample, bible: dict[str, str]) -> str:
    if example.source:
        return render_example_source(example.source, bible)
    return infer_example_source_from_bible(example, bible)


def resolve_example_source_metadata(
    example: ParsedExample,
    lines: list[str],
    start: int,
    bible: dict[str, str],
    supplement_rows: tuple[NormalizationSupplementRow, ...],
    heading_path: tuple[str, ...],
) -> ExampleSourceResolution:
    preceding_prose = extract_preceding_prose(lines, start)
    explicit_no_source = bool(
        NO_SOURCE_AVAILABLE_RE.search(example.source)
        or NO_SOURCE_AVAILABLE_RE.search(example.translation)
        or NO_SOURCE_AVAILABLE_RE.search(preceding_prose)
    )
    header_source = render_example_source(example.source, bible) if example.source and not explicit_no_source else ""
    contextual_source = render_example_source(find_contextual_example_source(lines, start), bible)
    inferred_source = infer_example_source_from_bible(example, bible)
    matched_rows = match_normalization_supplement_rows(example, supplement_rows)
    supplement_sources = tuple(
        sorted({render_example_source(row.source_reference, bible) for row in matched_rows if row.source_reference})
    )
    require_source = heading_path_requires_example_source(heading_path)

    evidence_pairs = [
        ("header", header_source),
        ("preceding prose", contextual_source),
        ("Bible inference", inferred_source),
    ]
    evidence_pairs.extend((f"supplement {row.example_id}", render_example_source(row.source_reference, bible)) for row in matched_rows)
    nonempty_pairs = [(origin, source) for origin, source in evidence_pairs if source]
    unique_sources = sorted({source for _, source in nonempty_pairs})

    conflict_message = ""
    if len(unique_sources) > 1:
        rendered_pairs = ", ".join(f"{origin}={source}" for origin, source in nonempty_pairs)
        conflict_message = f"Conflicting example sources for {example.label}: {rendered_pairs}"

    resolved_source = unique_sources[0] if len(unique_sources) == 1 else ""
    return ExampleSourceResolution(
        resolved_source=resolved_source,
        header_source=header_source,
        contextual_source=contextual_source,
        supplement_sources=supplement_sources,
        inferred_source=inferred_source,
        supplement_example_ids=tuple(row.example_id for row in matched_rows),
        explicit_no_source=explicit_no_source,
        require_source=require_source,
        conflict_message=conflict_message,
    )


def enrich_example_headers(markdown_text: str, bible: dict[str, str]) -> str:
    lines = markdown_text.splitlines()
    enriched_lines = list(lines)
    supplement_rows = load_normalization_supplements()
    stack: list[tuple[int, str]] = []
    index = 0

    while index < len(lines):
        heading_match = MARKDOWN_HEADING_RE.match(lines[index])
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            index += 1
            continue

        parsed_example, next_index = parse_example_at(lines, index)
        if not parsed_example:
            index += 1
            continue

        if parsed_example.label != "review-preview-warning":
            resolution = resolve_example_source_metadata(
                parsed_example,
                lines,
                index,
                bible,
                supplement_rows,
                tuple(title for _, title in stack),
            )
            if resolution.conflict_message:
                raise RuntimeError(resolution.conflict_message)
            if resolution.require_source and not resolution.resolved_source and not resolution.explicit_no_source:
                raise RuntimeError(
                    f"Missing example source for {parsed_example.label} in {' > '.join(title for _, title in stack)}"
                )
            resolved_source = resolution.resolved_source
            if resolved_source:
                enriched_lines[index] = f"(@{parsed_example.label}) {resolved_source}"

        index = next_index

    return "\n".join(enriched_lines).rstrip() + "\n"


def strip_terminal_source_parenthetical(translation: str, source: str) -> str:
    match = re.search(r"\(([^()]*)\)\s*$", translation)
    if not match:
        return translation

    parenthetical = normalize_for_comparison(match.group(1))
    if parenthetical != normalize_for_comparison(source):
        return translation

    return translation[: match.start()].rstrip()


def normalize_quote_marks(text: str) -> str:
    return text.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')


def latex_glossquote(text: str) -> str:
    return rf"\glossquote{{{escape_latex(text.strip())}}}"


def replace_inline_english_glosses(line: str) -> str:
    def replace(match: re.Match[str]) -> str:
        return latex_glossquote(match.group(1))

    return INLINE_GLOSS_QUOTE_RE.sub(replace, line)


def render_english_text_for_latex(text: str, *, wrap_if_unquoted: bool = False) -> str:
    normalized = normalize_quote_marks(text).strip()
    parts: list[str] = []
    last_end = 0
    found = False

    for match in INLINE_GLOSS_QUOTE_RE.finditer(normalized):
        found = True
        parts.append(escape_latex(normalized[last_end : match.start()]))
        parts.append(latex_glossquote(match.group(1)))
        last_end = match.end()

    parts.append(escape_latex(normalized[last_end:]))
    rendered = "".join(parts).strip()
    if found:
        return rendered

    stripped = strip_outer_quotes(normalized)
    if wrap_if_unquoted:
        return latex_glossquote(stripped)
    return escape_latex(stripped)


def build_translation_line(translation: str, source: str) -> str:
    normalized_translation = normalize_quote_marks(translation)
    if source:
        normalized_translation = strip_terminal_source_parenthetical(normalized_translation, source)

    rendered = render_english_text_for_latex(normalized_translation, wrap_if_unquoted=True)
    if source:
        rendered = f"{rendered} ({escape_latex(source)})"
    return rendered


def analysis_is_usable(analysis: dict[str, list[str]]) -> bool:
    gloss_words = analysis.get("gloss_words", [])
    if not gloss_words:
        return False
    return any(gloss != "??" for gloss in gloss_words)


def fallback_analysis(example: ParsedExample) -> dict[str, list[str]]:
    fallback_surface = example.segmentation.split() or example.tedim.split()
    fallback_gloss = example.gloss.split() or ["??"] * max(len(fallback_surface), 1)
    return {
        "toned_words": fallback_surface,
        "segmentation_words": fallback_surface,
        "gloss_words": fallback_gloss,
    }


def build_example_warning_text(label: str, warnings: list[str]) -> str | None:
    if not warnings:
        return None
    joined = "; ".join(warnings)
    return f"[REVIEW PREVIEW WARNING: {label}: {joined}]"


def analyze_example(
    example: ParsedExample, bible: dict[str, str], tone_dict: dict[str, list[dict[str, str]]]
) -> tuple[dict[str, list[str]], str, str | None]:
    warnings: list[str] = []
    source_display = resolve_example_source(example, bible)

    if example.source:
        verse_id = reference_to_verse_id(example.source)
        if verse_id:
            if verse_id in bible:
                verse_text = bible[verse_id]
                verse_norm = normalize_text_for_matching(verse_text)
                tedim_norm = normalize_text_for_matching(example.tedim)
                if tedim_norm and tedim_norm not in verse_norm:
                    warnings.append("Bible reference mapped, but slice example is not a direct verse span; analyzed slice wording")
            else:
                warnings.append("Bible reference parsed but no matching verse was found in the CTD Bible data")

    analysis = analyze_text(example.tedim, tone_dict)
    if not analysis_is_usable(analysis):
        analysis = fallback_analysis(example)
        warnings.append("analyzer-derived interlinear unavailable; using slice segmentation/gloss fallback")

    return analysis, source_display, build_example_warning_text(example.label, warnings)


def _is_technical_inline_code(span: str) -> bool:
    stripped = span.strip()
    lower = stripped.lower()

    if not stripped:
        return True
    if lower.startswith(TECHNICAL_PATH_PREFIXES):
        return True
    if stripped.startswith(("ex:", "@ex:", "@")):
        return True
    if "::" in stripped:
        return True
    if "\\" in stripped:
        return True
    if "/" in stripped and " / " not in stripped:
        return True
    if any(lower.endswith(suffix) for suffix in TECHNICAL_FILE_SUFFIXES):
        return True
    if lower.startswith(TECHNICAL_COMMAND_PREFIXES):
        return True
    if re.search(r"\s--?[A-Za-z0-9]", stripped):
        return True
    if re.search(r"\b(pytest|python3|pandoc|xelatex|bibtex|git)\b", lower) and " " in stripped:
        return True
    return False


def format_publication_inline_code(line: str) -> str:
    def replace(match: re.Match[str]) -> str:
        content = match.group(1)
        if _is_technical_inline_code(content):
            return match.group(0)
        return format_inline_tedim(content)

    return INLINE_CODE_RE.sub(replace, line)


def collect_source_audit_records(markdown_text: str, bible: dict[str, str]) -> list[SourceAuditRecord]:
    records: list[SourceAuditRecord] = []
    for example in parse_examples(markdown_text):
        if example.label == "review-preview-warning":
            continue
        rendered_source = resolve_example_source(example, bible)
        if not rendered_source:
            continue
        records.append(SourceAuditRecord(label=example.label, source=example.source, rendered_source=rendered_source))
    return records


def audit_example_sources(latex_markdown: str, source_records: list[SourceAuditRecord]) -> None:
    missing: list[str] = []
    for record in source_records:
        if record.label in SOURCE_AUDIT_EXCEPTIONS:
            continue

        match = re.search(
            rf"\\ex \\label\{{{re.escape(record.label)}\}}(?P<block>.*?)\\end\{{exe\}}",
            latex_markdown,
            re.DOTALL,
        )
        if not match:
            missing.append(f"{record.label}: missing gb4e block")
            continue

        glt_match = re.search(r"\\glt (?P<glt>[^\n]+)", match.group("block"))
        if not glt_match or record.rendered_source not in glt_match.group("glt"):
            missing.append(f"{record.label}: missing source after \\glt -> {record.rendered_source}")

    if missing:
        raise RuntimeError("Source audit failed for assembled preview examples:\n" + "\n".join(missing))


def example_to_latex_block(
    example: ParsedExample, bible: dict[str, str], tone_dict: dict[str, list[dict[str, str]]]
) -> str:
    if example.label == "review-preview-warning":
        return "\n".join(
            [
                "```{=latex}",
                rf"\reviewwarning{{{escape_latex(example.tedim)}}}",
                "```",
                "",
            ]
        )

    analysis, source_display, warning = analyze_example(example, bible, tone_dict)
    object_line, gloss_line = build_gll_lines(analysis)
    translation_line = build_translation_line(example.translation, source_display)

    latex_lines = [
        "```{=latex}",
        r"\begin{exe}",
        rf"\ex \label{{{escape_latex(example.label)}}}",
    ]
    if warning:
        latex_lines.append(rf"\reviewwarninginline{{{escape_latex(warning)}}}")
    latex_lines.extend(
        [
            rf"\gll {object_line} \\",
            rf"     {gloss_line} \\",
            rf"\glt {translation_line}",
            r"\end{exe}",
            "```",
            "",
        ]
    )
    return "\n".join(latex_lines)


def transform_markdown_for_latex(markdown_text: str, grammar_facing: bool = True) -> str:
    bible = load_bible(BIBLE_PATH)
    tone_dict = load_tone_dictionary()
    source_audit_records = collect_source_audit_records(markdown_text, bible)
    transformed: list[str] = []
    lines = markdown_text.splitlines()
    index = 0
    abbreviations_inserted = False
    in_publication_slice = False

    while index < len(lines):
        line = normalize_quote_marks(lines[index])

        if line.strip() == "---":
            index += 1
            while index < len(lines) and lines[index].strip() != "---":
                index += 1
            index += 1
            continue

        parsed_example, next_index = parse_example_at(lines, index)
        if parsed_example:
            transformed.append(example_to_latex_block(parsed_example, bible, tone_dict).rstrip("\n"))
            index = next_index
            continue

        chapter_match = CHAPTER_HEADING_RE.match(line)
        if chapter_match:
            if not abbreviations_inserted:
                transformed.extend(
                    [
                        "```{=latex}",
                        generate_abbreviations_section(),
                        "```",
                        "",
                    ]
                )
                abbreviations_inserted = True
            in_publication_slice = False
            transformed.extend(
                [
                    "```{=latex}",
                    r"\reviewchapterbreak",
                    "```",
                    "",
                    f"# {chapter_match.group(2)}",
                ]
            )
            index += 1
            continue

        if line.startswith("## "):
            in_publication_slice = grammar_facing

        if line.startswith("*Source slice: `"):
            in_publication_slice = True
            transformed.append(line)
            index += 1
            continue

        heading_match = re.match(r"^#\s+(.+?)\s*$", line)
        if heading_match:
            title = heading_match.group(1)
            if title in FRONTMATTER_SECTION_TITLES:
                transformed.extend(
                    [
                        "```{=latex}",
                        rf"\frontmattersection{{{escape_latex(title)}}}",
                        "```",
                        "",
                    ]
                )
                index += 1
                continue

        if grammar_facing and line and not line.startswith("[MAJOR GAP:") and not line.startswith("[REVIEW PREVIEW"):
            line = replace_inline_english_glosses(line)

        if in_publication_slice and line and not line.startswith("[MAJOR GAP:") and not line.startswith("[REVIEW PREVIEW"):
            line = format_publication_inline_code(line)

        transformed.append(line)
        index += 1

    latex_markdown = "\n".join(transformed).rstrip() + "\n"
    audit_example_sources(latex_markdown, source_audit_records)
    return latex_markdown


def write_latex_header(path: Path) -> None:
    header = rf"""
\usepackage{{fontspec}}
\usepackage{{geometry}}
\usepackage{{fancyhdr}}
\usepackage{{xcolor}}
\usepackage{{natbib}}
{generate_gb4e_setup()}
\geometry{{margin=0.75in}}
\setmainfont{{Times New Roman}}
\setsansfont{{Helvetica}}
\pagestyle{{fancy}}
\fancyhf{{}}
\fancyfoot[C]{{\thepage}}
\setcitestyle{{authoryear,round,semicolon}}
\setcounter{{secnumdepth}}{{3}}
\setcounter{{tocdepth}}{{2}}
\newcommand{{\frontmattersection}}[1]{{\section*{{#1}}\addcontentsline{{toc}}{{section}}{{#1}}}}
\newcommand{{\glossquote}}[1]{{`#1'}}
\newcommand{{\reviewwarning}}[1]{{\par\medskip\noindent\textbf{{#1}}\par\medskip}}
\newcommand{{\reviewwarninginline}}[1]{{\textbf{{#1}}\par\smallskip}}
\newcounter{{reviewchapter}}
\newcommand{{\reviewchapterbreak}}{{\stepcounter{{reviewchapter}}\setcounter{{xnumi}}{{0}}}}
\renewcommand{{\thexnumi}}{{\arabic{{reviewchapter}}.\arabic{{xnumi}}}}
\exewidth{{(4.99)}}
"""
    path.write_text(header.lstrip(), encoding="utf-8")


def generate_tex(markdown_text: str, markdown_path: Path, tex_path: Path, grammar_facing: bool = True) -> None:
    pandoc_cmd = find_executable("pandoc", PANDOC_FALLBACKS)
    if not pandoc_cmd:
        raise RuntimeError("pandoc not found; cannot generate LaTeX preview source")

    validate_citations(markdown_text, BIBLIOGRAPHY_PATH)
    latex_markdown = transform_markdown_for_latex(markdown_text, grammar_facing=grammar_facing)

    with tempfile.TemporaryDirectory() as tmpdir:
        temp_dir = Path(tmpdir)
        latex_markdown_path = temp_dir / "assembled_preview_for_latex.md"
        header_path = temp_dir / "assembled_preview_header.tex"
        latex_markdown_path.write_text(latex_markdown, encoding="utf-8")
        write_latex_header(header_path)

        command = [
            pandoc_cmd,
            str(latex_markdown_path),
            "--from=markdown+raw_tex",
            "--to=latex",
            "--standalone",
            "--toc",
            "--number-sections",
            "--natbib",
            "--bibliography",
            str(BIBLIOGRAPHY_RELATIVE),
            "-M",
            "reference-section-title=References",
            "-V",
            "fontsize=11pt",
            "-V",
            "papersize=a4",
            "-V",
            "geometry:margin=0.75in",
            "-V",
            "mainfont=Times New Roman",
            "-V",
            "sansfont=Helvetica",
            "-V",
            "colorlinks=true",
            "-V",
            "biblio-style=plainnat",
            "--include-in-header",
            str(header_path),
            "-o",
            str(tex_path),
        ]
        subprocess.run(command, check=True, cwd=markdown_path.parent)


def compile_pdf(tex_path: Path, pdf_path: Path) -> None:
    xelatex_cmd = find_executable("xelatex", XELATEX_FALLBACKS)
    if not xelatex_cmd:
        raise RuntimeError("xelatex not found; cannot compile review preview PDF")
    bibtex_cmd = find_executable("bibtex", BIBTEX_FALLBACKS)
    if not bibtex_cmd:
        raise RuntimeError("bibtex not found; cannot compile bibliography for review preview PDF")

    tex_dir = tex_path.parent
    stem = tex_path.stem

    def run(command: list[str]) -> None:
        result = subprocess.run(command, cwd=tex_dir, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(
                "Command failed while compiling assembled review preview PDF:\n"
                f"{' '.join(command)}\n\nSTDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
            )

    run([xelatex_cmd, "-interaction=nonstopmode", "-halt-on-error", tex_path.name])
    run([bibtex_cmd, stem])
    run([xelatex_cmd, "-interaction=nonstopmode", "-halt-on-error", tex_path.name])
    run([xelatex_cmd, "-interaction=nonstopmode", "-halt-on-error", tex_path.name])

    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        raise RuntimeError(f"expected non-empty PDF at {pdf_path}")


def run_quality_gate(tex_path: Path) -> None:
    gate_script = ROOT / "scripts" / "grammar_pdf_quality_gate.py"
    result = subprocess.run([sys.executable, str(gate_script), str(tex_path)], cwd=ROOT, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--grammar-facing",
        dest="grammar_facing",
        action="store_true",
        default=True,
        help="build the grammar-facing review preview (default)",
    )
    parser.add_argument(
        "--internal-review-apparatus",
        dest="grammar_facing",
        action="store_false",
        help="retain internal workflow apparatus in the assembled output",
    )
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="write Markdown and TeX only, without compiling the PDF",
    )
    args = parser.parse_args()

    PUBLICATION_REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    bible = load_bible(BIBLE_PATH)
    markdown = enrich_example_headers(build_markdown(grammar_facing=args.grammar_facing), bible)
    MARKDOWN_OUTPUT.write_text(markdown, encoding="utf-8")
    print(f"Wrote Markdown preview: {MARKDOWN_OUTPUT}")

    generate_tex(markdown, MARKDOWN_OUTPUT, TEX_OUTPUT, grammar_facing=args.grammar_facing)
    print(f"Wrote LaTeX preview: {TEX_OUTPUT}")

    if not args.skip_pdf:
        compile_pdf(TEX_OUTPUT, PDF_OUTPUT)
        print(f"Wrote PDF preview: {PDF_OUTPUT}")

    if args.grammar_facing:
        run_quality_gate(TEX_OUTPUT)


if __name__ == "__main__":
    main()
