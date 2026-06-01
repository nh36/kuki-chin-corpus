#!/usr/bin/env python3
"""Shared interlinear LaTeX helpers for Tedim Bible/example exports."""

from __future__ import annotations

import re
from pathlib import Path

from analyze_morphemes import analyze_sentence, analyze_word
from restore_tone import load_tone_dictionary, restore_word_tone


STANDARD_LEIPZIG = {
    "1": "first person",
    "2": "second person",
    "3": "third person",
    "ABL": "ablative",
    "ABIL": "abilitative",
    "ALL": "allative",
    "APPL": "applicative",
    "CAUS": "causative",
    "COM": "comitative",
    "COMPL": "completive",
    "CONT": "continuative",
    "CVB": "converb",
    "DAT": "dative",
    "DIMIN": "diminutive",
    "ERG": "ergative",
    "EXCL": "exclusive",
    "EXP": "experiential",
    "GEN": "genitive",
    "HAB": "habitual",
    "HORIZ": "horizontal",
    "IMP": "imperative",
    "IMM": "immediate",
    "INCL": "inclusive",
    "INS": "instrumental",
    "INTENS": "intensive",
    "IRR": "irrealis",
    "ITER": "iterative",
    "LOC": "locative",
    "NEG": "negative",
    "NMLZ": "nominalizer",
    "PFV": "perfective",
    "PL": "plural",
    "POSS": "possessive",
    "PROSP": "prospective",
    "PROX": "proximal",
    "Q": "question particle",
    "RECIP": "reciprocal",
    "REFL": "reflexive",
    "REL": "relativizer",
    "RES": "resultative",
    "SG": "singular",
    "TOP": "topic",
}

TEDIM_SPECIFIC = {
    "I": "verb form I (citation form)",
    "II": "verb form II (dependent form)",
    "1SG→3": "first singular acting on third person",
    "3→1": "third person acting on first person",
    "2→1": "second person acting on first person",
    "AG": "agent (nominalizer)",
    "AUG": "augmentative (big/great)",
    "DOWN": "downward directional",
    "UP": "upward directional",
    "TOWARD": "goal directional",
    "DIST": "distal/anaphoric demonstrative",
    "HAB.CONT": "habitual continuative",
    "NEG.ABIL": "negative abilitative (cannot)",
    "MORE": "comparative (more X)",
    "PROX": "proximal demonstrative",
}

BOOK_NAMES = {
    1: "Genesis",
    2: "Exodus",
    3: "Leviticus",
    4: "Numbers",
    5: "Deuteronomy",
    6: "Joshua",
    7: "Judges",
    8: "Ruth",
    9: "1 Samuel",
    10: "2 Samuel",
    11: "1 Kings",
    12: "2 Kings",
    13: "1 Chronicles",
    14: "2 Chronicles",
    15: "Ezra",
    16: "Nehemiah",
    17: "Esther",
    18: "Job",
    19: "Psalms",
    20: "Proverbs",
    21: "Ecclesiastes",
    22: "Song of Solomon",
    23: "Isaiah",
    24: "Jeremiah",
    25: "Lamentations",
    26: "Ezekiel",
    27: "Daniel",
    28: "Hosea",
    29: "Joel",
    30: "Amos",
    31: "Obadiah",
    32: "Jonah",
    33: "Micah",
    34: "Nahum",
    35: "Habakkuk",
    36: "Zephaniah",
    37: "Haggai",
    38: "Zechariah",
    39: "Malachi",
    40: "Matthew",
    41: "Mark",
    42: "Luke",
    43: "John",
    44: "Acts",
    45: "Romans",
    46: "1 Corinthians",
    47: "2 Corinthians",
    48: "Galatians",
    49: "Ephesians",
    50: "Philippians",
    51: "Colossians",
    52: "1 Thessalonians",
    53: "2 Thessalonians",
    54: "1 Timothy",
    55: "2 Timothy",
    56: "Titus",
    57: "Philemon",
    58: "Hebrews",
    59: "James",
    60: "1 Peter",
    61: "2 Peter",
    62: "1 John",
    63: "2 John",
    64: "3 John",
    65: "Jude",
    66: "Revelation",
}

BOOK_NAME_ALIASES = {
    "song of songs": 22,
    "psalm": 19,
}

LATEX_SPECIAL_REPLACEMENTS = [
    ("\\", r"\textbackslash{}"),
    ("&", r"\&"),
    ("%", r"\%"),
    ("$", r"\$"),
    ("#", r"\#"),
    ("_", r"\_"),
    ("{", r"\{"),
    ("}", r"\}"),
    ("~", r"\textasciitilde{}"),
    ("^", r"\textasciicircum{}"),
]

TRAILING_PUNCTUATION = '.,;:!?"'
FINAL_GLOSS_MAP = {
    "this": "PROX",
    "that": "DIST",
}
REFERENCE_RE = re.compile(
    r"^(?P<book>(?:[1-3]\s+)?[A-Za-z][A-Za-z .'-]*[A-Za-z])\s+(?P<chapter>\d+):(?P<verse>\d+)$"
)


def normalize_book_name(name: str) -> str:
    normalized = name.lower().replace("&", "and")
    normalized = re.sub(r"[^0-9a-z]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


BOOK_NAME_TO_NUMBER = {normalize_book_name(name): number for number, name in BOOK_NAMES.items()}
for alias, number in BOOK_NAME_ALIASES.items():
    BOOK_NAME_TO_NUMBER[normalize_book_name(alias)] = number


def load_bible(filepath: str | Path) -> dict[str, str]:
    verses: dict[str, str] = {}
    with Path(filepath).open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                verses[parts[0]] = parts[1]
    return verses


def load_kjv(filepath: str | Path) -> dict[str, str]:
    kjv: dict[str, str] = {}
    with Path(filepath).open("r", encoding="utf-8") as handle:
        cols = handle.readline().strip().split("\t")
        eng_idx = cols.index("eng_King James Version") if "eng_King James Version" in cols else 2
        for raw_line in handle:
            parts = raw_line.strip().split("\t")
            if len(parts) > eng_idx:
                kjv[parts[0]] = parts[eng_idx]
    return kjv


def parse_verse_id(verse_id: str) -> tuple[int, int, int]:
    return int(verse_id[:2]), int(verse_id[2:5]), int(verse_id[5:])


def format_reference(verse_id: str) -> str:
    book, chapter, verse = parse_verse_id(verse_id)
    return f"{BOOK_NAMES.get(book, f'Book {book}')} {chapter}:{verse}"


def reference_to_verse_id(reference: str) -> str | None:
    match = REFERENCE_RE.match(reference.strip())
    if not match:
        return None

    book_number = BOOK_NAME_TO_NUMBER.get(normalize_book_name(match.group("book")))
    if book_number is None:
        return None

    chapter = int(match.group("chapter"))
    verse = int(match.group("verse"))
    return f"{book_number:02d}{chapter:03d}{verse:03d}"


def normalize_text_for_matching(text: str) -> str:
    normalized = (
        text.replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("–", "-")
        .replace("—", "-")
    )
    normalized = normalized.lower()
    normalized = re.sub(r"[^0-9a-z' ]+", " ", normalized)
    return re.sub(r"\s+", " ", normalized).strip()


def escape_latex(text: str) -> str:
    for old, new in LATEX_SPECIAL_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def format_gloss_smallcaps(gloss: str) -> str:
    parts = re.split(r"([-.])", gloss)
    result: list[str] = []
    for part in parts:
        if part in {"-", "."}:
            result.append(part)
        elif part.lower() in FINAL_GLOSS_MAP:
            result.append(r"\textsc{" + FINAL_GLOSS_MAP[part.lower()].lower() + "}")
        elif re.match(r"^[A-Z0-9→]+$", part):
            result.append(r"\textsc{" + part.lower() + "}")
        else:
            result.append(escape_latex(part))
    return "".join(result)


def generate_abbreviations_section() -> str:
    lines = [
        r"\section*{Abbreviations}",
        r"\addcontentsline{toc}{section}{Abbreviations}",
        r"",
        r"\subsection*{Standard Leipzig Glossing Abbreviations}",
        r"\begin{tabular}{@{}ll@{\hspace{2em}}ll@{}}",
    ]

    abbrevs = sorted(STANDARD_LEIPZIG.items())
    mid = (len(abbrevs) + 1) // 2
    for i in range(mid):
        left = abbrevs[i]
        right = abbrevs[i + mid] if i + mid < len(abbrevs) else ("", "")
        left_fmt = f"\\textsc{{{left[0].lower()}}} & {left[1]}"
        right_fmt = f"\\textsc{{{right[0].lower()}}} & {right[1]}" if right[0] else "& "
        lines.append(f"{left_fmt} & {right_fmt} \\\\")

    lines.extend(
        [
            r"\end{tabular}",
            r"",
            r"\vspace{1em}",
            r"\subsection*{Tedim Chin-Specific Conventions}",
            r"\begin{tabular}{@{}ll@{}}",
        ]
    )

    for abbrev, meaning in sorted(TEDIM_SPECIFIC.items()):
        display = abbrev.replace("→", r"$\rightarrow$")
        lines.append(f"\\textsc{{{display.lower()}}} & {meaning} \\\\")

    lines.extend(
        [
            r"\end{tabular}",
            r"",
            r"\vspace{1em}",
            r"\noindent\textbf{Verb Forms:} Tedim Chin verbs have two conjugation forms.",
            r"\textsc{i} (Form I) is the citation/independent form; \textsc{ii} (Form II)",
            r"appears in dependent clauses and certain constructions.",
            r"",
        ]
    )
    return "\n".join(lines)


def generate_gb4e_setup() -> str:
    return r"""
\usepackage{gb4e}
\noautomath
\newcommand{\tdim}[1]{\textit{#1}}
\newcommand{\tdimword}[1]{\textit{#1}}
\let\oldeachwordone\eachwordone
\renewcommand{\eachwordone}{\oldeachwordone\hspace{0.3em}}
\let\oldeachwordtwo\eachwordtwo
\renewcommand{\eachwordtwo}{\oldeachwordtwo\hspace{0.3em}}
\renewcommand{\textsc}[1]{{\footnotesize\MakeUppercase{#1}}}
""".strip()


def analyze_text(text: str, tone_dict: dict[str, list[dict[str, str]]]) -> dict[str, list[str]]:
    words = text.split()
    sentence_analysis = analyze_sentence(text)
    toned_words: list[str] = []
    segmentation_words: list[str] = []
    gloss_words: list[str] = []

    for index, word in enumerate(words):
        punct = ""
        clean_word = word
        if word and word[-1] in TRAILING_PUNCTUATION:
            punct = word[-1]
            clean_word = word[:-1]

        was_capitalized = bool(clean_word) and clean_word[0].isupper()

        if index < len(sentence_analysis):
            _, segmentation, gloss, _ = sentence_analysis[index]
        else:
            result = analyze_word(clean_word.lower())
            if result:
                segmentation, gloss = result
            else:
                segmentation, gloss = clean_word, "??"

        toned, _confidence, _analysis = restore_word_tone(clean_word, tone_dict)
        if was_capitalized and toned:
            toned = toned[0].upper() + toned[1:]

        toned_words.append(toned + punct)
        segmentation_words.append(segmentation)
        gloss_words.append(gloss)

    return {
        "toned_words": toned_words,
        "segmentation_words": segmentation_words,
        "gloss_words": gloss_words,
    }


def format_object_language_token(token: str) -> str:
    return r"\tdimword{" + escape_latex(token) + "}"


def format_inline_tedim(text: str) -> str:
    return r"\tdim{" + escape_latex(text) + "}"


def build_gll_lines(analysis: dict[str, list[str]]) -> tuple[str, str]:
    object_line = " ".join(format_object_language_token(word) for word in analysis["toned_words"])
    gloss_line = " ".join(format_gloss_smallcaps(word) for word in analysis["gloss_words"])
    return object_line, gloss_line
