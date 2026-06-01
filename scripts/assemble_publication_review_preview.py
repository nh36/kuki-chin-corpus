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
import os
import re
import shutil
import subprocess
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

FRONTMATTER_SECTION_TITLES = {
    "Review preview status",
    "PDF/build status",
    "Known narrow-slice limitations",
    "Major unresolved domains",
    "End state of this preview",
}

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

TECHNICAL_PATH_PREFIXES = ("output/", "docs/", "scripts/", "tests/", "data/", "literature/", "bibles/")
TECHNICAL_FILE_SUFFIXES = (".md", ".py", ".tex", ".pdf", ".tsv", ".bib", ".json", ".txt", ".yaml", ".yml")
TECHNICAL_COMMAND_PREFIXES = ("python3", "make", "pytest", "xelatex", "pandoc", "git", "bibtex", "pdftotext")
SOURCE_AUDIT_EXCEPTIONS: set[str] = set()


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


def find_executable(name: str, fallbacks: list[str]) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    for fallback in fallbacks:
        if os.path.exists(fallback):
            return fallback
    return None


def read_slice(path_text: str) -> str | None:
    path = ROOT / path_text
    if not path.exists():
        return None
    return adjust_heading_levels(strip_yaml_front_matter(path.read_text(encoding="utf-8")))


def build_markdown() -> str:
    lines: list[str] = [
        "---",
        'title: "Assembled Tedim Grammar Review Preview"',
        'subtitle: "Not a finished grammar"',
        'date: ""',
        "---",
        "",
        "# Review preview status",
        "",
        "This is a review preview, not a finished grammar. It is assembled from first-pass publication-review slices and is controlled by `output/publication_review/whole_grammar_coverage_checkpoint_after_transitivity.md`, `output/publication_review/whole_grammar_coverage_checkpoint_after_reduplication.md`, `output/publication_review/whole_grammar_coverage_audit.md`, `docs/SKELETON_GRAMMAR.md`, `docs/grammar/GRAMMAR_SOURCE_INVENTORY.md`, and `PROGRESS.md`.",
        "",
        "`output/publication_review/review_notes_transitivity.md` brought the transitivity packet to review-note maturity, and the post-transitivity checkpoint now treats the packet set as stable enough for a review preview assembled from actual slice prose. This document is not a new grammar slice, not a dictionary slice, and not a human-review packet. It is intended to help human review and direct editing, not to certify completion.",
        "",
        "Many sections are deliberately narrow. Missing or blocked domains are marked explicitly. The PDF built from this assembly is a review preview PDF, not a final publication PDF.",
        "",
        "# PDF/build status",
        "",
        "This preview is reproducible from committed sources with `python3 scripts/assemble_publication_review_preview.py`. The script writes `output/publication_review/assembled_grammar_review_preview.md`, generates `output/publication_review/assembled_grammar_review_preview.tex` through Pandoc plus natbib/BibTeX citation processing, and compiles `output/publication_review/assembled_grammar_review_preview.pdf` with XeLaTeX while routing publication-review example blocks through the shared analyzer and gb4e interlinear machinery.",
        "",
        "The assembly reuses current repository conventions where practical: the repository bibliography in `literature/bibliography.bib`, XeLaTeX compilation and the `Times New Roman` / `Helvetica` font pair already used in `scripts/export_interlinear.py`, the shared Bible/analyzer helpers in `scripts/interlinear_latex.py`, and the same 0.75-inch page-margin convention for generated TeX output.",
        "",
        "# Known narrow-slice limitations",
        "",
        "- VP structure / suffix stacking: currently anchored by `bawlzoding`.",
        "- derivation / valency: currently anchored by `-sak`.",
        "- prefix/agreement: currently anchored by `kanei / kainn`.",
        "- clause linkage: currently anchored by `ciangin`.",
        "- nominalization: currently anchored by `-na / bawlna`.",
        "- NP structure / possession: currently anchored by `hih mite`, `mi khat`, `mi khempeuh`.",
        "- noun domain: currently anchored by `gam` and `aksi / aksi-te`.",
        "- reduplication: currently anchored by `mahmah / taktak`, with `peuhpeuh` secondary.",
        "- transitivity: currently anchored by `sih / suak` versus `hawl / en`.",
        "",
        "# Major unresolved domains",
        "",
        "- [MAJOR GAP: phonology/tone remains blocked or theory-heavy.]",
        "- [MAJOR GAP: verb paradigms remain report-backed but not packet-shaped.]",
        "- [MAJOR GAP: broader discourse remains partly surfaced and boundary-heavy.]",
        "- [MAJOR GAP: analyzer-gap topics remain cross-cutting blockers.]",
        "",
        "Second-pass expansions such as `-pih`, `ki-`, hong-/kong-, switch reference, relative clauses, transparent compounds, wider reduplication, and labile or ambitransitive transitivity remain outside this first-pass assembled review preview.",
        "",
    ]

    for chapter in ASSEMBLY_SPEC:
        lines.extend([f"# {chapter['title']}", ""])
        for item in chapter["items"]:
            if item["type"] == "slice":
                lines.extend([f"## {item['title']}", "", f"*Source slice: `{item['path']}`*", ""])
                content = read_slice(item["path"])
                if content is None:
                    lines.extend([f"[REVIEW PREVIEW GAP: expected grammar slice not found: {item['path']}]", ""])
                else:
                    lines.extend([content.rstrip(), ""])
            else:
                if item.get("title"):
                    lines.extend([f"## {item['title']}", ""])
                lines.extend([item["text"], "", item["explanation"], ""])

    lines.extend(
        [
            "# End state of this preview",
            "",
            "This assembled review preview contains the actual prose of the current first-pass publication-review grammar slices in a single ordered draft. It does not claim that the whole grammar is finished, and the generated PDF is a review preview PDF rather than a final publication PDF.",
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
            source=(match.group(2) or "").strip(),
            tedim=tedim_match.group(1).strip(),
            segmentation=segmentation_match.group(1).strip(),
            gloss=gloss_match.group(1).strip(),
            translation=translation_match.group(1).strip(),
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


def render_example_source(source: str, bible: dict[str, str]) -> str:
    source = source.strip()
    if not source:
        return ""

    verse_id = reference_to_verse_id(source)
    if verse_id and verse_id in bible:
        return format_reference(verse_id)
    return source


def strip_terminal_source_parenthetical(translation: str, source: str) -> str:
    match = re.search(r"\(([^()]*)\)\s*$", translation)
    if not match:
        return translation

    parenthetical = normalize_for_comparison(match.group(1))
    if parenthetical != normalize_for_comparison(source):
        return translation

    return translation[: match.start()].rstrip()


def build_translation_line(translation: str, source: str) -> str:
    normalized_translation = strip_outer_quotes(translation)
    if source:
        normalized_translation = strip_terminal_source_parenthetical(normalized_translation, source)

    rendered = f"'{normalized_translation}'"
    if source:
        rendered = f"{rendered} ({source})"
    return escape_latex(rendered)


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
    source_display = render_example_source(example.source, bible)

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
        if example.label == "review-preview-warning" or not example.source:
            continue
        rendered_source = render_example_source(example.source, bible)
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


def transform_markdown_for_latex(markdown_text: str) -> str:
    bible = load_bible(BIBLE_PATH)
    tone_dict = load_tone_dictionary()
    source_audit_records = collect_source_audit_records(markdown_text, bible)
    transformed: list[str] = []
    lines = markdown_text.splitlines()
    index = 0
    abbreviations_inserted = False
    in_publication_slice = False

    while index < len(lines):
        line = lines[index]

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
            in_publication_slice = False

        if line.startswith("*Source slice: `"):
            in_publication_slice = True
            transformed.append(line)
            index += 1
            continue

        heading_match = re.match(r"^#\s+(.+?)\s*$", line)
        if heading_match:
            title = heading_match.group(1)
            if title == "Known narrow-slice limitations" and not abbreviations_inserted:
                transformed.extend(
                    [
                        "```{=latex}",
                        generate_abbreviations_section(),
                        "```",
                        "",
                    ]
                )
                abbreviations_inserted = True

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
\newcommand{{\frontmattersection}}[1]{{\section*{{#1}}\addcontentsline{{toc}}{{section}}{{#1}}}}
\newcommand{{\reviewwarning}}[1]{{\par\medskip\noindent\textbf{{#1}}\par\medskip}}
\newcommand{{\reviewwarninginline}}[1]{{\textbf{{#1}}\par\smallskip}}
\newcounter{{reviewchapter}}
\newcommand{{\reviewchapterbreak}}{{\stepcounter{{reviewchapter}}\setcounter{{xnumi}}{{0}}}}
\renewcommand{{\thexnumi}}{{\arabic{{reviewchapter}}.\arabic{{xnumi}}}}
\exewidth{{(4.99)}}
"""
    path.write_text(header.lstrip(), encoding="utf-8")


def generate_tex(markdown_text: str, markdown_path: Path, tex_path: Path) -> None:
    pandoc_cmd = find_executable("pandoc", PANDOC_FALLBACKS)
    if not pandoc_cmd:
        raise RuntimeError("pandoc not found; cannot generate LaTeX preview source")

    validate_citations(markdown_text, BIBLIOGRAPHY_PATH)
    latex_markdown = transform_markdown_for_latex(markdown_text)

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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="write Markdown and TeX only, without compiling the PDF",
    )
    args = parser.parse_args()

    PUBLICATION_REVIEW_DIR.mkdir(parents=True, exist_ok=True)

    markdown = build_markdown()
    MARKDOWN_OUTPUT.write_text(markdown, encoding="utf-8")
    print(f"Wrote Markdown preview: {MARKDOWN_OUTPUT}")

    generate_tex(markdown, MARKDOWN_OUTPUT, TEX_OUTPUT)
    print(f"Wrote LaTeX preview: {TEX_OUTPUT}")

    if not args.skip_pdf:
        compile_pdf(TEX_OUTPUT, PDF_OUTPUT)
        print(f"Wrote PDF preview: {PDF_OUTPUT}")


if __name__ == "__main__":
    main()
