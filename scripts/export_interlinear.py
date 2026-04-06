#!/usr/bin/env python3
"""
Export interlinear Bible text to LaTeX/PDF.

Creates a multi-tier interlinear display using gb4e package:
  1. Tone-marked orthography (with morpheme boundaries)
  2. Leipzig-style glosses (auto-aligned via gb4e's gll command) - in small caps
  3. Free translation (KJV)

The tone restoration already runs the morphological analyzer internally
to disambiguate homophones, so tone and glosses are consistent.

Usage:
    python scripts/export_interlinear.py --book 41 --output output/mark_interlinear.tex
    python scripts/export_interlinear.py --book 41 --chapter 1 --output output/mark1.tex
    python scripts/export_interlinear.py --verses 41001001-41001010 --output output/mark_sample.tex
"""

import argparse
import os
import sys
import re
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from analyze_morphemes import analyze_word, analyze_sentence
from restore_tone import load_tone_dictionary, restore_word_tone


# =============================================================================
# ABBREVIATIONS LIST
# =============================================================================
# Standard Leipzig Glossing Rules abbreviations (https://www.eva.mpg.de/lingua/resources/glossing-rules.php)
# Plus Tedim Chin-specific extensions

STANDARD_LEIPZIG = {
    '1': 'first person',
    '2': 'second person',
    '3': 'third person',
    'ABL': 'ablative',
    'ABIL': 'abilitative',
    'ALL': 'allative',
    'APPL': 'applicative',
    'CAUS': 'causative',
    'COM': 'comitative',
    'COMPL': 'completive',
    'CONT': 'continuative',
    'CVB': 'converb',
    'DAT': 'dative',
    'DIMIN': 'diminutive',
    'ERG': 'ergative',
    'EXCL': 'exclusive',
    'EXP': 'experiential',
    'GEN': 'genitive',
    'HAB': 'habitual',
    'HORIZ': 'horizontal',
    'IMP': 'imperative',
    'IMM': 'immediate',
    'INCL': 'inclusive',
    'INS': 'instrumental',
    'INTENS': 'intensive',
    'IRR': 'irrealis',
    'ITER': 'iterative',
    'LOC': 'locative',
    'NEG': 'negative',
    'NMLZ': 'nominalizer',
    'PFV': 'perfective',
    'PL': 'plural',
    'POSS': 'possessive',
    'PROSP': 'prospective',
    'Q': 'question particle',
    'RECIP': 'reciprocal',
    'REFL': 'reflexive',
    'REL': 'relativizer',
    'RES': 'resultative',
    'SG': 'singular',
}

TEDIM_SPECIFIC = {
    'I': 'verb form I (citation form)',
    'II': 'verb form II (dependent form)',
    '1SG→3': 'first singular acting on third person',
    '3→1': 'third person acting on first person',
    '2→1': 'second person acting on first person',
    'AG': 'agent (nominalizer)',
    'AUG': 'augmentative (big/great)',
    'DOWN': 'downward directional',
    'UP': 'upward directional',
    'TOWARD': 'goal directional',
    'HAB.CONT': 'habitual continuative',
    'NEG.ABIL': 'negative abilitative (cannot)',
    'MORE': 'comparative (more X)',
}


# Book name mapping (numeric code to name)
BOOK_NAMES = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles",
    15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms",
    20: "Proverbs", 21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
    28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
    33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah", 37: "Haggai",
    38: "Zechariah", 39: "Malachi",
    40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts",
    45: "Romans", 46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians",
    49: "Ephesians", 50: "Philippians", 51: "Colossians", 52: "1 Thessalonians",
    53: "2 Thessalonians", 54: "1 Timothy", 55: "2 Timothy", 56: "Titus",
    57: "Philemon", 58: "Hebrews", 59: "James", 60: "1 Peter", 61: "2 Peter",
    62: "1 John", 63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation"
}


def load_bible(filepath):
    """Load Bible text as dict of verse_id -> text."""
    verses = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                verse_id = parts[0]
                text = parts[1]
                verses[verse_id] = text
    return verses


def load_kjv(filepath):
    """Load KJV translations from aligned verses file."""
    kjv = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        header = f.readline()
        cols = header.strip().split('\t')
        eng_idx = cols.index('eng_King James Version') if 'eng_King James Version' in cols else 2
        
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) > eng_idx:
                verse_id = parts[0]
                kjv[verse_id] = parts[eng_idx]
    return kjv


def parse_verse_id(verse_id):
    """Parse verse ID like '41001005' into (book, chapter, verse)."""
    book = int(verse_id[:2])
    chapter = int(verse_id[2:5])
    verse = int(verse_id[5:])
    return book, chapter, verse


def format_reference(verse_id):
    """Format verse ID as human-readable reference."""
    book, chapter, verse = parse_verse_id(verse_id)
    book_name = BOOK_NAMES.get(book, f"Book {book}")
    return f"{book_name} {chapter}:{verse}"


def analyze_verse(text, tone_dict):
    """
    Analyze a verse and return aligned word lists.
    
    Uses analyze_sentence() for context-aware disambiguation (e.g., ngen pray vs net).
    The tone restoration internally uses analyze_word() to disambiguate
    homophones, so the tone and gloss are consistent.
    
    Returns dict with parallel lists:
      - toned_words: tone-marked forms (preserving original capitalization)
      - gloss_words: Leipzig glosses (one per word)
    Plus:
      - kjv: will be added by caller
    """
    words = text.split()
    
    # Get sentence-level analysis for context-aware disambiguation
    sentence_analysis = analyze_sentence(text)
    
    toned_words = []
    gloss_words = []
    
    for i, word in enumerate(words):
        # Preserve and strip punctuation - BUT keep apostrophe as it's the genitive marker
        punct = ''
        clean_word = word
        if word and word[-1] in '.,;:!?"':  # Note: apostrophe removed from this list
            punct = word[-1]
            clean_word = word[:-1]
        
        # Track if original was capitalized
        was_capitalized = clean_word and clean_word[0].isupper()
        
        # Use sentence-level analysis if available (for context-aware disambiguation)
        if i < len(sentence_analysis):
            _, seg, gloss, _ = sentence_analysis[i]
        else:
            # Fallback to word-level
            result = analyze_word(clean_word.lower())
            if result:
                seg, gloss = result
            else:
                seg, gloss = clean_word, '??'
        
        # Get tone-marked form
        toned, conf, analysis = restore_word_tone(clean_word, tone_dict)
        # Restore capitalization if original was capitalized
        if was_capitalized and toned:
            toned = toned[0].upper() + toned[1:]
        toned_words.append(toned + punct)
        gloss_words.append(gloss)
    
    return {
        'toned_words': toned_words,
        'gloss_words': gloss_words,
    }


def escape_latex(text):
    """Escape special LaTeX characters."""
    replacements = [
        ('\\', r'\textbackslash{}'),
        ('&', r'\&'),
        ('%', r'\%'),
        ('$', r'\$'),
        ('#', r'\#'),
        ('_', r'\_'),
        ('{', r'\{'),
        ('}', r'\}'),
        ('~', r'\textasciitilde{}'),
        ('^', r'\textasciicircum{}'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def format_gloss_smallcaps(gloss):
    """
    Format a gloss string with grammatical abbreviations in small caps.
    
    Converts uppercase grammatical glosses (e.g., NMLZ, ERG, PL) to 
    LaTeX small caps while keeping lexical glosses lowercase.
    
    Examples:
        'word-NMLZ' -> 'word-\\textsc{nmlz}'
        '1SG→3-give.II' -> '\\textsc{1sg→3}-give.\\textsc{ii}'
    """
    # Pattern to match grammatical abbreviations (uppercase letters, numbers, arrows, periods)
    # These are: 1SG, 2PL, NMLZ, ERG, 1SG→3, etc.
    
    def replace_abbrev(match):
        abbrev = match.group(0)
        # Convert to lowercase for small caps
        return r'\textsc{' + abbrev.lower() + '}'
    
    # Match sequences of: uppercase letters, digits, arrows, that are grammatical
    # Grammatical glosses: sequences of caps/numbers/special chars
    # But NOT: proper nouns (we keep those as-is)
    
    # Split by hyphens and periods to process each morpheme
    parts = re.split(r'([-.])', gloss)
    result = []
    
    for part in parts:
        if part in ['-', '.']:
            result.append(part)
        elif re.match(r'^[A-Z0-9→]+$', part):
            # All caps/numbers - grammatical gloss -> small caps
            result.append(r'\textsc{' + part.lower() + '}')
        else:
            # Lexical item or mixed - keep as is, but escape
            result.append(escape_latex(part))
    
    return ''.join(result)


def generate_abbreviations_section():
    """Generate LaTeX for the abbreviations section."""
    
    lines = [
        r"\section*{Abbreviations}",
        r"\addcontentsline{toc}{section}{Abbreviations}",
        r"",
        r"\subsection*{Standard Leipzig Glossing Abbreviations}",
        r"\begin{tabular}{@{}ll@{\hspace{2em}}ll@{}}",
    ]
    
    # Sort and format standard abbreviations in two columns
    abbrevs = sorted(STANDARD_LEIPZIG.items())
    mid = (len(abbrevs) + 1) // 2
    
    for i in range(mid):
        left = abbrevs[i]
        right = abbrevs[i + mid] if i + mid < len(abbrevs) else ('', '')
        
        left_fmt = f"\\textsc{{{left[0].lower()}}} & {left[1]}"
        right_fmt = f"\\textsc{{{right[0].lower()}}} & {right[1]}" if right[0] else "& "
        
        lines.append(f"{left_fmt} & {right_fmt} \\\\")
    
    lines.append(r"\end{tabular}")
    lines.append(r"")
    lines.append(r"\vspace{1em}")
    lines.append(r"\subsection*{Tedim Chin-Specific Conventions}")
    lines.append(r"\begin{tabular}{@{}ll@{}}")
    
    for abbrev, meaning in sorted(TEDIM_SPECIFIC.items()):
        # Handle special arrow character
        abbrev_display = abbrev.replace('→', r'$\rightarrow$')
        lines.append(f"\\textsc{{{abbrev_display.lower()}}} & {meaning} \\\\")
    
    lines.append(r"\end{tabular}")
    lines.append(r"")
    lines.append(r"\vspace{1em}")
    lines.append(r"\noindent\textbf{Verb Forms:} Tedim Chin verbs have two conjugation forms.")
    lines.append(r"\textsc{i} (Form I) is the citation/independent form; \textsc{ii} (Form II)")
    lines.append(r"appears in dependent clauses and certain constructions.")
    lines.append(r"")
    lines.append(r"\newpage")
    
    return '\n'.join(lines)


def generate_latex(verses_data, title, output_path):
    """Generate LaTeX document with interlinear glosses using gb4e."""
    
    latex_header = r"""\documentclass[11pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{fontspec}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{gb4e}  % Standard linguistics interlinear package
\noautomath  % Prevent gb4e from messing with math mode

% Add horizontal spacing between word-gloss pairs for readability
\let\oldeachwordone\eachwordone
\renewcommand{\eachwordone}{\oldeachwordone\hspace{0.3em}}
\let\oldeachwordtwo\eachwordtwo  
\renewcommand{\eachwordtwo}{\oldeachwordtwo\hspace{0.3em}}

\geometry{margin=0.75in}

% Font setup - use system fonts with good Unicode support
\setmainfont{Times New Roman}
\setsansfont{Helvetica}

% Fake small caps: slightly smaller uppercase letters
% This ensures consistent rendering across systems
\renewcommand{\textsc}[1]{{\footnotesize\MakeUppercase{#1}}}

% Colors for translation line
\definecolor{kjvcolor}{RGB}{80,80,120}

% Title formatting
\titleformat{\section}{\large\bfseries}{\thesection}{1em}{}

% Header/footer
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\textit{""" + escape_latex(title) + r"""}}
\fancyhead[R]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}

\title{""" + escape_latex(title) + r""" \\ \large Interlinear Edition with Tone Marking}
\author{Generated from Tedim Chin Bible Corpus}
\date{\today}

\begin{document}

\maketitle

\section*{Conventions}
\begin{itemize}
\item Tone diacritics: \textbf{á} = High, \textbf{ā} = Mid, \textbf{à} = Low (unmarked = tone unknown)
\item Morpheme boundaries shown with hyphens
\item Glosses use Leipzig Glossing Rules abbreviations in \textsc{small caps}
\item \textcolor{kjvcolor}{\textit{Italics}}: King James Version translation
\end{itemize}

\tableofcontents
\newpage

"""

    latex_footer = r"""
\end{document}
"""

    # Group verses by chapter
    chapters = {}
    for verse_id, data in verses_data.items():
        book, chapter, verse = parse_verse_id(verse_id)
        if chapter not in chapters:
            chapters[chapter] = []
        chapters[chapter].append((verse_id, verse, data))
    
    # Sort
    for chapter in chapters:
        chapters[chapter].sort(key=lambda x: x[1])
    
    # Generate body
    body_parts = []
    
    # Add abbreviations section first
    body_parts.append(generate_abbreviations_section())
    
    for chapter in sorted(chapters.keys()):
        body_parts.append(f"\\section*{{Chapter {chapter}}}")
        body_parts.append(f"\\addcontentsline{{toc}}{{section}}{{Chapter {chapter}}}")
        body_parts.append("")
        body_parts.append("\\begin{exe}")
        
        for verse_id, verse_num, data in chapters[chapter]:
            # Format as gb4e example with interlinear gloss
            toned_line = ' '.join(escape_latex(w) for w in data['toned_words'])
            # Apply small caps to grammatical glosses
            gloss_line = ' '.join(format_gloss_smallcaps(w) for w in data['gloss_words'])
            kjv = escape_latex(data.get('kjv', ''))
            
            block = []
            # Use \exi for custom verse number label
            block.append(f"\\exi{{{verse_num}}}")
            block.append(f"\\gll {toned_line} \\\\")
            block.append(f"     {gloss_line} \\\\")
            if kjv:
                block.append(f"\\glt \\textcolor{{kjvcolor}}{{\\textit{{{kjv}}}}}")
            block.append("")
            
            body_parts.append('\n'.join(block))
        
        body_parts.append("\\end{exe}")
        body_parts.append("\\newpage")
        body_parts.append("")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(latex_header)
        f.write('\n'.join(body_parts))
        f.write(latex_footer)
    
    return output_path


def main():
    parser = argparse.ArgumentParser(description='Export interlinear Bible text to LaTeX')
    parser.add_argument('--book', type=int, help='Book number (e.g., 41 for Mark)')
    parser.add_argument('--chapter', type=int, help='Chapter number (optional)')
    parser.add_argument('--verses', type=str, help='Verse range (e.g., 41001001-41001010)')
    parser.add_argument('--output', type=str, required=True, help='Output .tex file path')
    parser.add_argument('--compile', action='store_true', help='Compile to PDF with xelatex')
    
    args = parser.parse_args()
    
    # Paths
    base_dir = Path(__file__).parent.parent
    bible_path = base_dir / 'bibles/extracted/ctd/ctd-x-bible.txt'
    aligned_path = base_dir / 'data/verses_aligned.tsv'
    
    print("Loading resources...")
    bible = load_bible(bible_path)
    kjv = load_kjv(aligned_path)
    tone_dict = load_tone_dictionary()
    
    print(f"Loaded {len(bible)} verses, {len(kjv)} KJV translations, {len(tone_dict)} tone entries")
    
    # Filter verses
    if args.verses:
        # Parse range like "41001001-41001010"
        if '-' in args.verses:
            start, end = args.verses.split('-')
            verse_ids = [v for v in bible.keys() if start <= v <= end]
        else:
            verse_ids = [args.verses] if args.verses in bible else []
    elif args.book:
        book_prefix = f"{args.book:02d}"
        if args.chapter:
            chapter_prefix = f"{args.book:02d}{args.chapter:03d}"
            verse_ids = [v for v in bible.keys() if v.startswith(chapter_prefix)]
        else:
            verse_ids = [v for v in bible.keys() if v.startswith(book_prefix)]
    else:
        parser.error("Must specify --book, --chapter, or --verses")
    
    verse_ids = sorted(verse_ids)
    print(f"Processing {len(verse_ids)} verses...")
    
    # Analyze verses
    verses_data = {}
    for i, verse_id in enumerate(verse_ids):
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{len(verse_ids)} verses...")
        
        text = bible[verse_id]
        data = analyze_verse(text, tone_dict)
        data['kjv'] = kjv.get(verse_id, '')
        verses_data[verse_id] = data
    
    # Generate title
    if args.book:
        book_name = BOOK_NAMES.get(args.book, f"Book {args.book}")
        if args.chapter:
            title = f"{book_name} Chapter {args.chapter}"
        else:
            title = book_name
    else:
        title = "Tedim Chin Bible Selection"
    
    # Generate LaTeX
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    generate_latex(verses_data, title, output_path)
    print(f"Generated: {output_path}")
    
    # Optionally compile
    if args.compile:
        import subprocess
        import shutil
        
        # Check for xelatex in standard locations
        xelatex_cmd = shutil.which('xelatex')
        if not xelatex_cmd:
            # Try standard locations including TinyTeX
            home = os.path.expanduser('~')
            tex_paths = [
                f'{home}/TinyTeX/bin/universal-darwin/xelatex',
                f'{home}/Library/TinyTeX/bin/universal-darwin/xelatex',
                '/Library/TeX/texbin/xelatex',
                '/usr/local/texlive/2024/bin/universal-darwin/xelatex',
                '/usr/local/texlive/2025/bin/universal-darwin/xelatex',
            ]
            for tex_path in tex_paths:
                if os.path.exists(tex_path):
                    xelatex_cmd = tex_path
                    break
        
        if not xelatex_cmd:
            print("Error: xelatex not found. Please install MacTeX or TeX Live:")
            print("  brew install --cask mactex-no-gui")
            print(f"\nLaTeX file ready for manual compilation: {output_path}")
            return
        
        print(f"Compiling with xelatex ({xelatex_cmd})...")
        # Run xelatex twice for TOC to be correct
        for pass_num in [1, 2]:
            result = subprocess.run(
                [xelatex_cmd, '-interaction=nonstopmode', '-output-directory', str(output_path.parent), str(output_path)],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"LaTeX compilation failed (pass {pass_num}):")
                # Print just the error lines
                for line in result.stdout.split('\n'):
                    if line.startswith('!') or 'Error' in line:
                        print(line)
                return
        
        pdf_path = output_path.with_suffix('.pdf')
        print(f"Generated PDF: {pdf_path}")


if __name__ == '__main__':
    main()
