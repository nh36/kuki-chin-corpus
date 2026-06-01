#!/usr/bin/env python3
"""Assemble the publication-review grammar preview into Markdown, TeX, and PDF."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLICATION_REVIEW_DIR = ROOT / "output" / "publication_review"
MARKDOWN_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.md"
TEX_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.tex"
PDF_OUTPUT = PUBLICATION_REVIEW_DIR / "assembled_grammar_review_preview.pdf"

PANDOC_FALLBACKS = [
    "/opt/homebrew/bin/pandoc",
    "/usr/local/bin/pandoc",
]

XELATEX_FALLBACKS = [
    "/Library/TeX/texbin/xelatex",
    "/usr/local/texlive/2024/bin/universal-darwin/xelatex",
    "/usr/local/texlive/2025/bin/universal-darwin/xelatex",
]

EXPECTED_SLICES: list[tuple[str, str]] = [
    ("Demonstratives / deixis", "output/publication_review/grammar_demonstratives_print_slice.md"),
    ("Pronouns / clusivity", "output/publication_review/grammar_pronouns_print_slice.md"),
    ("NP structure / possession", "output/publication_review/grammar_np_possession_print_slice.md"),
    ("Noun domain", "output/publication_review/grammar_noun_domain_print_slice.md"),
    ("Case marking", "output/publication_review/grammar_case_marking_print_slice.md"),
    ("Relators / postpositions", "output/publication_review/grammar_relators_postpositions_print_slice.md"),
    ("Numerals", "output/publication_review/grammar_numerals_print_slice.md"),
    ("Quantifiers", "output/publication_review/grammar_quantifiers_print_slice.md"),
    ("Stem alternation", "output/publication_review/grammar_stem_alternation_print_slice.md"),
    ("Prefix / agreement", "output/publication_review/grammar_prefix_agreement_print_slice.md"),
    ("Transitivity", "output/publication_review/grammar_transitivity_print_slice.md"),
    ("VP structure / suffix stacking", "output/publication_review/grammar_vp_structure_stacking_print_slice.md"),
    ("TAM / aspect / modal", "output/publication_review/grammar_tam_print_slice.md"),
    ("Directionals", "output/publication_review/grammar_directionals_print_slice.md"),
    ("Derivation / valency", "output/publication_review/grammar_derivation_valency_print_slice.md"),
    ("Nominalization", "output/publication_review/grammar_nominalization_print_slice.md"),
    ("Clause linkage", "output/publication_review/grammar_clause_linkage_print_slice.md"),
    ("Negation", "output/publication_review/grammar_negation_print_slice.md"),
    ("Interrogatives", "output/publication_review/grammar_interrogatives_print_slice.md"),
    ("Sentence-final particles", "output/publication_review/grammar_sentence_final_particles_print_slice.md"),
    ("Coordinators", "output/publication_review/grammar_coordinators_print_slice.md"),
    ("Reduplication", "output/publication_review/grammar_reduplication_print_slice.md"),
]

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
        "This preview is reproducible from committed sources with `python3 scripts/assemble_publication_review_preview.py`. The script writes `output/publication_review/assembled_grammar_review_preview.md`, generates `output/publication_review/assembled_grammar_review_preview.tex` through Pandoc, and compiles `output/publication_review/assembled_grammar_review_preview.pdf` with XeLaTeX when the required tools are available.",
        "",
        "The assembly reuses current repository conventions where practical: XeLaTeX compilation and the `Times New Roman` / `Helvetica` font pair already used in `scripts/export_interlinear.py`, plus the same 0.75-inch page-margin convention for generated TeX output.",
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


def generate_tex(markdown_path: Path, tex_path: Path) -> None:
    pandoc_cmd = find_executable("pandoc", PANDOC_FALLBACKS)
    if not pandoc_cmd:
        raise RuntimeError("pandoc not found; cannot generate LaTeX preview source")

    command = [
        pandoc_cmd,
        str(markdown_path),
        "--from=gfm",
        "--to=latex",
        "--standalone",
        "--toc",
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
        "-o",
        str(tex_path),
    ]
    subprocess.run(command, check=True)


def compile_pdf(tex_path: Path, pdf_path: Path) -> None:
    xelatex_cmd = find_executable("xelatex", XELATEX_FALLBACKS)
    if not xelatex_cmd:
        raise RuntimeError("xelatex not found; cannot compile review preview PDF")

    for _ in range(2):
        result = subprocess.run(
            [
                xelatex_cmd,
                "-interaction=nonstopmode",
                "-halt-on-error",
                "-output-directory",
                str(tex_path.parent),
                str(tex_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "xelatex failed while compiling assembled review preview PDF:\n"
                f"{result.stdout}\n{result.stderr}"
            )

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

    generate_tex(MARKDOWN_OUTPUT, TEX_OUTPUT)
    print(f"Wrote LaTeX preview: {TEX_OUTPUT}")

    if not args.skip_pdf:
        compile_pdf(TEX_OUTPUT, PDF_OUTPUT)
        print(f"Wrote PDF preview: {PDF_OUTPUT}")


if __name__ == "__main__":
    main()
