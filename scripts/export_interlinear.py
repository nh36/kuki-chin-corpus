#!/usr/bin/env python3
"""
Export interlinear Bible text to LaTeX/PDF.

Creates a multi-tier interlinear display using gb4e package:
  1. Tone-marked orthography
  2. Leipzig-style glosses (auto-aligned via gb4e's gll command) in small caps
  3. Free translation (KJV)

The tone restoration already runs the morphological analyzer internally
to disambiguate homophones, so tone and glosses are consistent.

Usage:
    python scripts/export_interlinear.py --book 41 --output output/mark_interlinear.tex
    python scripts/export_interlinear.py --book 41 --chapter 1 --output output/mark1.tex
    python scripts/export_interlinear.py --verses 41001001-41001010 --output output/mark_sample.tex
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from restore_tone import load_tone_dictionary

from interlinear_latex import (
    BOOK_NAMES,
    analyze_text,
    escape_latex,
    format_gloss_smallcaps,
    format_reference,
    generate_abbreviations_section,
    generate_gb4e_setup,
    load_bible,
    load_kjv,
    parse_verse_id,
)


def analyze_verse(text: str, tone_dict: dict[str, list[dict[str, str]]]) -> dict[str, list[str]]:
    """Backward-compatible wrapper around the shared analyzer/glossing helper."""
    return analyze_text(text, tone_dict)


def generate_latex(
    verses_data: dict[str, dict[str, list[str] | str]], title: str, output_path: Path
) -> Path:
    """Generate a LaTeX document with gb4e interlinear glosses."""
    latex_header = rf"""\documentclass[11pt,a4paper]{{article}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage{{fontspec}}
\usepackage{{geometry}}
\usepackage{{fancyhdr}}
\usepackage{{titlesec}}
\usepackage{{xcolor}}
{generate_gb4e_setup()}

\geometry{{margin=0.75in}}
\setmainfont{{Times New Roman}}
\setsansfont{{Helvetica}}
\definecolor{{kjvcolor}}{{RGB}}{{80,80,120}}
\titleformat{{\section}}{{\large\bfseries}}{{\thesection}}{{1em}}{{}}

\pagestyle{{fancy}}
\fancyhf{{}}
\fancyhead[L]{{\textit{{{escape_latex(title)}}}}}
\fancyhead[R]{{\thepage}}
\renewcommand{{\headrulewidth}}{{0.4pt}}

\title{{{escape_latex(title)} \\ \large Interlinear Edition with Tone Marking}}
\author{{Generated from Tedim Chin Bible Corpus}}
\date{{\today}}

\begin{{document}}

\maketitle

\section*{{Conventions}}
\begin{{itemize}}
\item Tone diacritics: \textbf{{á}} = High, \textbf{{ā}} = Mid, \textbf{{à}} = Low (unmarked = tone unknown)
\item Glosses use Leipzig Glossing Rules abbreviations in \textsc{{small caps}}
\item \textcolor{{kjvcolor}}{{\textit{{Italics}}}}: King James Version translation
\end{{itemize}}

\tableofcontents
\newpage
"""

    latex_footer = r"""
\end{document}
"""

    chapters: dict[int, list[tuple[str, int, dict[str, list[str] | str]]]] = {}
    for verse_id, data in verses_data.items():
        _book, chapter, verse = parse_verse_id(verse_id)
        chapters.setdefault(chapter, []).append((verse_id, verse, data))

    for chapter_rows in chapters.values():
        chapter_rows.sort(key=lambda row: row[1])

    body_parts = [generate_abbreviations_section()]
    for chapter in sorted(chapters):
        body_parts.append(f"\\section*{{Chapter {chapter}}}")
        body_parts.append(f"\\addcontentsline{{toc}}{{section}}{{Chapter {chapter}}}")
        body_parts.append("")
        body_parts.append("\\begin{exe}")

        for verse_id, verse_num, data in chapters[chapter]:
            toned_line = " ".join(escape_latex(word) for word in data["toned_words"])
            gloss_line = " ".join(format_gloss_smallcaps(word) for word in data["gloss_words"])
            kjv = escape_latex(str(data.get("kjv", "")))

            body_parts.append(f"\\exi{{{verse_num}}}")
            body_parts.append(f"\\gll {toned_line} \\\\")
            body_parts.append(f"     {gloss_line} \\\\")
            if kjv:
                body_parts.append(f"\\glt \\textcolor{{kjvcolor}}{{\\textit{{{kjv}}}}}")
            body_parts.append("")

        body_parts.append("\\end{exe}")
        body_parts.append("\\newpage")
        body_parts.append("")

    output_path.write_text(latex_header + "\n".join(body_parts) + latex_footer, encoding="utf-8")
    return output_path


def _find_xelatex() -> str | None:
    xelatex_cmd = shutil.which("xelatex")
    if xelatex_cmd:
        return xelatex_cmd

    home = os.path.expanduser("~")
    tex_paths = [
        f"{home}/TinyTeX/bin/universal-darwin/xelatex",
        f"{home}/Library/TinyTeX/bin/universal-darwin/xelatex",
        "/Library/TeX/texbin/xelatex",
        "/usr/local/texlive/2024/bin/universal-darwin/xelatex",
        "/usr/local/texlive/2025/bin/universal-darwin/xelatex",
    ]
    for candidate in tex_paths:
        if os.path.exists(candidate):
            return candidate
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Export interlinear Bible text to LaTeX")
    parser.add_argument("--book", type=int, help="Book number (e.g., 41 for Mark)")
    parser.add_argument("--chapter", type=int, help="Chapter number (optional)")
    parser.add_argument("--verses", type=str, help="Verse range (e.g., 41001001-41001010)")
    parser.add_argument("--output", type=str, required=True, help="Output .tex file path")
    parser.add_argument("--compile", action="store_true", help="Compile to PDF with xelatex")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    bible_path = base_dir / "bibles/extracted/ctd/ctd-x-bible.txt"
    aligned_path = base_dir / "data/verses_aligned.tsv"

    print("Loading resources...")
    bible = load_bible(bible_path)
    kjv = load_kjv(aligned_path)
    tone_dict = load_tone_dictionary()
    print(f"Loaded {len(bible)} verses, {len(kjv)} KJV translations, {len(tone_dict)} tone entries")

    if args.verses:
        if "-" in args.verses:
            start, end = args.verses.split("-", 1)
            verse_ids = [verse_id for verse_id in bible if start <= verse_id <= end]
        else:
            verse_ids = [args.verses] if args.verses in bible else []
    elif args.book:
        if args.chapter:
            chapter_prefix = f"{args.book:02d}{args.chapter:03d}"
            verse_ids = [verse_id for verse_id in bible if verse_id.startswith(chapter_prefix)]
        else:
            book_prefix = f"{args.book:02d}"
            verse_ids = [verse_id for verse_id in bible if verse_id.startswith(book_prefix)]
    else:
        parser.error("Must specify --book, --chapter, or --verses")

    verse_ids = sorted(verse_ids)
    print(f"Processing {len(verse_ids)} verses...")

    verses_data: dict[str, dict[str, list[str] | str]] = {}
    for index, verse_id in enumerate(verse_ids, start=1):
        if index % 50 == 0:
            print(f"  Processed {index}/{len(verse_ids)} verses...")
        data = analyze_verse(bible[verse_id], tone_dict)
        data["kjv"] = kjv.get(verse_id, "")
        verses_data[verse_id] = data

    if args.book:
        book_name = BOOK_NAMES.get(args.book, f"Book {args.book}")
        title = f"{book_name} Chapter {args.chapter}" if args.chapter else book_name
    else:
        title = "Tedim Chin Bible Selection"

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generate_latex(verses_data, title, output_path)
    print(f"Generated: {output_path}")

    if not args.compile:
        return

    xelatex_cmd = _find_xelatex()
    if not xelatex_cmd:
        print("Error: xelatex not found. Please install MacTeX or TeX Live:")
        print("  brew install --cask mactex-no-gui")
        print(f"\nLaTeX file ready for manual compilation: {output_path}")
        return

    print(f"Compiling with xelatex ({xelatex_cmd})...")
    for pass_num in (1, 2):
        result = subprocess.run(
            [
                xelatex_cmd,
                "-interaction=nonstopmode",
                "-output-directory",
                str(output_path.parent),
                str(output_path),
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f"LaTeX compilation failed (pass {pass_num}):")
            print(result.stdout[-2000:] if result.stdout else "")
            print(result.stderr[-2000:] if result.stderr else "")
            return

    pdf_path = output_path.with_suffix(".pdf")
    print(f"Generated PDF: {pdf_path}")


if __name__ == "__main__":
    main()
