#!/usr/bin/env python3
"""Fail loudly when the grammar-facing assembled preview violates style gates."""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import assemble_publication_review_preview as assembler


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = ROOT / "output" / "publication_review" / "grammar_facing_quality_report.md"
FIRST_CHAPTER_TITLE = "Phonology and tone"
TARGET_SECTION_TITLES = {
    "Stem alternation",
    "Numerals",
    "Quantifiers",
    "NP structure / possession",
    "Noun domain",
    "Case marking",
    "Relators / postpositions",
    "Transitivity",
    "Derivation / valency",
    "VP structure / suffix stacking",
    "TAM / aspect / modal",
    "Directionals",
    "Nominalization",
    "Clause linkage",
}
GOSPEL_BOOKS = {
    "Matthew",
    "Mark",
    "Luke",
    "John",
}
NT_BOOKS = {
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
}
SUBSECTION_IGNORE_RE = re.compile(
    r"(overview|inventory|summary|deferred|boundary|controls|argument structure)$",
    re.IGNORECASE,
)
ONE_EXAMPLE_NOTE_RE = re.compile(
    r"(?:No equally (?:good|clean).{0,120}(?:example|row).{0,120}(?:is currently used|was found)(?: for this construction)?"
    r"|This construction is rare.{0,200}one example is used here"
    r"|broader source balancing remains outside the present account"
    r"|Gospel (?:row|example|comparandum).{0,200}(?:not used formally|remains prose-only))",
    re.IGNORECASE | re.DOTALL,
)
PDF_INTERNAL_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"(?:^|\n)\s*Scope\s*(?:\n|$)", re.IGNORECASE), "visible Scope heading"),
    (re.compile(r"(?:^|\n)\s*Editorial scope\s*(?:\n|$)", re.IGNORECASE), "visible Editorial scope heading"),
    (re.compile(r"source slice:", re.IGNORECASE), "source-slice marker"),
    (
        re.compile(
            r"candidate TSV|dossier|review notes|coverage normalization|print slice|packet(?:s| maturity)?|publication-review|current pass|normalized section|ready for human review|this section is now|this is no longer|controlling files|grammar_facing_quality_report\.md|draft argument plan|eventual prose|next commit|writing order|quotation-safe layer",
            re.IGNORECASE,
        ),
        "internal workflow term",
    ),
    (re.compile(r"(?:output|scripts|tests|docs)/[A-Za-z0-9_./\\-]+", re.IGNORECASE), "internal file path"),
    (re.compile(r"test_[A-Za-z0-9_]+\.py", re.IGNORECASE), "test-name reference"),
)
TEX_INTERNAL_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\\section\*?\{Scope\}", re.IGNORECASE), "visible Scope heading"),
    (re.compile(r"\\section\*?\{Editorial scope\}", re.IGNORECASE), "visible Editorial scope heading"),
    (re.compile(r"Source slice:", re.IGNORECASE), "source-slice marker"),
    (
        re.compile(
            r"candidate TSV|dossier|review notes|coverage normalization|print slice|packet(?:s| maturity)?|publication-review|current pass|normalized section|ready for human review|this section is now|this is no longer|controlling files|grammar_facing_quality_report\.md|draft argument plan|eventual prose|next commit|writing order|quotation-safe layer",
            re.IGNORECASE,
        ),
        "internal workflow term",
    ),
    (re.compile(r"(?:output|scripts|tests|docs)/[A-Za-z0-9_./\\-]+", re.IGNORECASE), "internal file path"),
)
GLOSSARY_REQUIREMENTS: dict[str, tuple[tuple[str, ...], str]] = {
    "gam": ((r"land(?: / country)?",), "land / country"),
    "aksi": ((r"star",), "star"),
    "aksi-te": ((r"stars",), "stars"),
    "mi": ((r"person",), "person"),
    "mite": ((r"people",), "people"),
    "mi khat": ((r"one person|a person",), "one person / a person"),
    "mi khempeuh": ((r"all people|everyone",), "all people"),
    "mi pawlkhat": ((r"some people",), "some people"),
    "mi tampi": ((r"many people",), "many people"),
    "kum": ((r"year",), "year"),
    "ni": ((r"day",), "day"),
    "kum sawm le nih": ((r"twelve years",), "twelve years"),
    "ni li": ((r"four days",), "four days"),
    "khat": ((r"one",), "one"),
    "nih": ((r"two",), "two"),
    "sawm": ((r"ten",), "ten"),
    "kua": ((r"nine|who",), "nine"),
    "khempeuh": ((r"all",), "all"),
    "pawlkhat": ((r"some(?: people)?|one group",), "some / one group"),
    "kuamah": ((r"nobody",), "nobody"),
    "bangmah": ((r"nothing|anything",), "nothing"),
    "tampi": ((r"many",), "many"),
    "hih": ((r"this",), "this"),
    "tua": ((r"that",), "that"),
    "-ah": ((r"locative / goal-like|locative|goal-like|LOC",), "locative / goal-like"),
    "-in": ((r"ergative / agentive|ergative|agentive|ERG",), "ergative / agentive"),
    "-pan": ((r"source / ablative|source|ablative",), "source / ablative"),
    "-panin": ((r"source / departure|source|departure|from",), "source / departure"),
    "-tawh": ((r"with",), "with"),
    "khua-ah": ((r"in the town",), "in the town"),
    "inn-ah": ((r"in(?:to)? the house|into the house",), "in / into the house"),
    "keima inn-ah": ((r"into my house",), "into my house"),
    "Kain in": ((r"Cain as transitive subject|Cain as agent",), "Cain as agent"),
    "Herod in": ((r"Herod as transitive subject|Herod as agent",), "Herod as agent"),
    "lakpan": ((r"from among",), "from among"),
    "sungah": ((r"inside|in",), "inside / in"),
    "tungah": ((r"on|upon",), "on / upon"),
    "kiangah": ((r"beside|near|side / vicinity|side|vicinity",), "beside / near"),
    "sung": ((r"inside|within",), "inside"),
    "tung": ((r"on|upon|above",), "on / upon"),
    "kiang": ((r"beside|near|side / vicinity|side|vicinity",), "beside / near"),
    "lak": ((r"among|midst|between",), "among / midst"),
    "pualam": ((r"outside|exterior",), "outside"),
    "tawh": ((r"with",), "with"),
    "na pa' inn-ah": ((r"in (?:thy|your father'?s) house",), "in your father's house"),
    "Abraham' suan David": ((r"David, descendant of Abraham",), "David, descendant of Abraham"),
    "minam": ((r"nation|people-group",), "nation / people-group"),
    "minam khat": ((r"one nation",), "one nation"),
    "-khia": ((r"outward|out",), "outward"),
    "-khiat": ((r"away|out of",), "away"),
    "-toh": ((r"upward|up",), "upward"),
    "-sawn": ((r"toward",), "toward"),
    "-suk": ((r"downward|down",), "downward"),
    "-lam": ((r"sideward|toward a side|side",), "sideward / toward a side"),
    "pokhia": ((r"grow out|grew out",), "grow out"),
    "nawhkhiat": ((r"drive out|hurry away",), "drive out / hurry away"),
    "hotkhiatna": ((r"salvation|saving away",), "salvation"),
    "kilaktoh": ((r"be taken up|was taken up",), "be taken up"),
    "kahtohna": ((r"going up|ascent",), "going up"),
    "paitoh": ((r"go-accompany|accompany",), "go-accompany"),
    "piasawn": ((r"give toward|extend to us",), "give toward"),
    "paisuk": ((r"go down|came down",), "go down"),
    "tawplam": ((r"toward the side|at the edge|side",), "toward the side / at the edge"),
    "-ta": ((r"completive / change-of-state|change-of-state|completive",), "completive / change-of-state"),
    "-zo": ((r"already / completive|completive|already",), "already / completive"),
    "-gige": ((r"habitually / always|habitually|always",), "habitually / always"),
    "-zel": ((r"continuative / keep doing|continuative|keep doing",), "continuative / keep doing"),
    "-ding": ((r"prospective / irrealis|prospective|irrealis|future-like",), "prospective / irrealis"),
    "-thei": ((r"can / be able|can|be able",), "can / be able"),
    "-kik": ((r"again / back|again|back",), "again / back"),
    "-ngei": ((r"ever / experiential|ever|experiential",), "ever / experiential"),
    "dingin": ((r"for .* to|clause-bound irrealis|purpose-like",), "for ... to / clause-bound irrealis"),
    "pailai": ((r"go-midst|prospective candidate|prospective",), "go-midst / prospective candidate"),
    "-sak": ((r"causative / benefactive|causative|benefactive|applicative-like",), "causative / benefactive"),
    "paisak": ((r"cause to go|go-CAUS",), "cause to go"),
    "muhsak": ((r"show / make see|show|make see|see\.II-BENF",), "show / make see"),
    "-pih": ((r"with / accompanying|with|accompanying",), "with / accompanying"),
    "paipih": ((r"go with|accompany",), "go with / accompany"),
    "mipihte": ((r"companions|associated people",), "companions / associated people"),
    "ki-": ((r"reflexive / middle / passive-like|reflexive|middle|passive-like",), "reflexive / middle / passive-like"),
    "kisep": ((r"REFL-work|do by oneself|self-directed",), "REFL-work / do by oneself"),
    "kigen": ((r"be said|it is said",), "be said / it is said"),
    "piangsak": ((r"cause to be born|create|cause\.birth",), "cause to be born / create"),
    "sih": ((r"die",), "die"),
    "suak": ((r"become",), "become"),
    "hawl": ((r"seek / steer|seek|steer|drive",), "seek / steer"),
    "en": ((r"look at / see|look at|see|watch",), "look at / see"),
    "ne / nek": ((r"eat",), "eat"),
    "nei / neih": ((r"have",), "have"),
    "pia / piak": ((r"give",), "give"),
    "nusia / nusiat": ((r"leave|forsake|abandon",), "leave"),
    "bia / biak": ((r"speak / worship / address|worship|speak|address",), "speak / worship / address"),
    "thei / theih": ((r"can / be able|can|be able|know",), "can / be able"),
    "piang / pian": ((r"be born / arise|be born|arise",), "be born / arise"),
    "zui / zuih": ((r"follow",), "follow"),
    "khial / khialh": ((r"err / sin|err|sin",), "err / sin"),
    "kia / kiak": ((r"fall",), "fall"),
    "sawlkhia / sawlkhiat": ((r"send out|send forth",), "send out"),
    "mu / muh": ((r"see",), "see"),
    "za / zak": ((r"hear / listen|hear|listen",), "hear / listen"),
    "ngai / ngaih": ((r"need / love / listen|need|love|listen",), "need / love / listen"),
    "pua / puak": ((r"carry.on.back|carry|spill",), "carry.on.back / spill"),
    "pai / paih": ((r"go",), "go"),
    "tua / tuah": ((r"do",), "do"),
    "tua / tuak": ((r"meet / receive|meet|receive",), "meet / receive"),
    "pia": ((r"give",), "give"),
    "gen": ((r"say|tell",), "say"),
    "tom": ((r"meet / accompany|meet|accompany",), "meet / accompany"),
    "hong": ((r"come / venitive|come|venitive",), "come / venitive"),
    "pia(k)sak": ((r"give-CAUS / cause to give|cause to give|give-CAUS",), "give-CAUS / cause to give"),
    "khia-ta": ((r"out-PFV|out plus completive|out",), "out-PFV"),
    "bawlzoding": ((r"make-COMPL-IRR|make plus completive plus irrealis",), "make-COMPL-IRR"),
    "bawlsakthei": ((r"make-CAUS-ABIL|make plus causative plus abilitative|can cause to make",), "make-CAUS-ABIL"),
    "ciahsakkik": ((r"send back|return-CAUS-ITER|return",), "send back"),
    "paikhiatsak": ((r"cause to go out|go-out-CAUS|go out",), "cause to go out"),
    "khiathei ding om lo": ((r"there is no one who can interpret it|cannot interpret|interpret",), "there is no one who can interpret it"),
    "bawlna": ((r"making / creation|making|creation",), "making / creation"),
    "bawl-na": ((r"make-NMLZ|making / creation",), "make-NMLZ"),
    "-pa": ((r"agentive / person|agentive|person",), "agentive / person"),
    "-mi": ((r"person / one who|person|one who",), "person / one who"),
    "hong pai mi": ((r"one who came|person who came",), "one who came"),
    "omna": ((r"place / being / existence|place|being|existence",), "place / being / existence"),
    "muhna-ah": ((r"in seeing|in the sight|before",), "in seeing / in the sight"),
    "kumpipa": ((r"king",), "king"),
    "Topa": ((r"Lord",), "Lord"),
    "ciangin": ((r"when|temporal subordination",), "when"),
    "tua ciangin": ((r"then / when|that when",), "then / when"),
    "ciang-in": ((r"when-ERG|when|then-ERG",), "when-ERG"),
    "dingin": ((r"in order to|for|purpose",), "in order to / for"),
    "ding-in": ((r"IRR-ERG|purpose-ERG",), "IRR-ERG"),
    "ngenin": ((r"pray-CVB|praying|speaking-CVB",), "pray-CVB"),
    "VERB-in": ((r"converb|clause chain marker",), "converb"),
    "ahih ciangin": ((r"when / when it was|when|temporal different-subject",), "when / when it was"),
    "a bawl mi": ((r"person who|one who makes|one who made|person who made",), "person who"),
    "omna": ((r"place / being / existence|being|nominalized relative",), "place / being / existence"),
    "om-na": ((r"be-NMLZ|exist-NMLZ",), "be-NMLZ"),
    "muhna-ah": ((r"in seeing|in the sight|before",), "in seeing / in the sight"),
    "mu-hna-ah": ((r"see-NMLZ-LOC|in the sight",), "see-NMLZ-LOC"),
    "leh": ((r"if / when|conditional",), "if / when"),
    "hangin": ((r"because|causal subordination",), "because"),
    "bangin": ((r"like / as|comparative",), "like / as"),
}


@dataclass(frozen=True)
class MarkdownBlock:
    level: int
    title: str
    parent_titles: tuple[str, ...]
    content: str
    start_line: int


@dataclass(frozen=True)
class TexBlock:
    level: int
    title: str
    parent_titles: tuple[str, ...]
    content: str
    start_line: int


@dataclass(frozen=True)
class ExampleRecord:
    label: str
    source: str
    header_source: str
    contextual_source: str
    supplement_sources: tuple[str, ...]
    inferred_source: str
    heading_path: tuple[str, ...]
    preceding_prose: str
    explicit_no_source: bool
    require_source: bool
    conflict_message: str


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def split_markdown_blocks(text: str) -> list[MarkdownBlock]:
    lines = text.splitlines()
    headings: list[tuple[int, int, str, tuple[str, ...]]] = []
    stack: list[tuple[int, str]] = []

    for index, line in enumerate(lines):
        match = assembler.MARKDOWN_HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_titles = tuple(title_text for _, title_text in stack)
        headings.append((index, level, title, parent_titles))
        stack.append((level, title))

    blocks: list[MarkdownBlock] = []
    for idx, (start_line, level, title, parent_titles) in enumerate(headings):
        end_line = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
        content = "\n".join(lines[start_line + 1 : end_line]).strip("\n")
        blocks.append(
            MarkdownBlock(
                level=level,
                title=title,
                parent_titles=parent_titles,
                content=content,
                start_line=start_line + 1,
            )
        )
    return blocks


def split_tex_blocks(tex: str) -> list[TexBlock]:
    command_to_level = {"section": 1, "subsection": 2, "subsubsection": 3}
    matches = list(re.finditer(r"\\(section|subsection|subsubsection)\{([^}]+)\}", tex))
    blocks: list[TexBlock] = []
    stack: list[tuple[int, str]] = []

    for index, match in enumerate(matches):
        level = command_to_level[match.group(1)]
        title = match.group(2)
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_titles = tuple(text for _, text in stack)
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tex)
        blocks.append(
            TexBlock(
                level=level,
                title=title,
                parent_titles=parent_titles,
                content=tex[match.end() : end].strip(),
                start_line=tex[: match.start()].count("\n") + 1,
            )
        )
        stack.append((level, title))
    return blocks


def markdown_block_has_substance(block: MarkdownBlock) -> bool:
    prose_lines: list[str] = []
    for raw_line in block.content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("*Source slice:"):
            continue
        if line.startswith("(@ex:") or line.startswith("|") or line.startswith(">"):
            return True
        prose_lines.append(line)
    return prose_has_substance("\n".join(prose_lines))


def tex_block_has_substance(block: TexBlock) -> bool:
    content = block.content
    if not content:
        return False
    if any(
        marker in content
        for marker in (r"\begin{exe}", r"\begin{longtable}", r"\begin{itemize}", r"\begin{enumerate}", "Deferred and boundary material")
    ):
        return True
    return prose_has_substance(strip_tex_nonprose(content))


def prose_has_substance(text: str) -> bool:
    for paragraph in re.split(r"\n\s*\n", text):
        cleaned = normalize_whitespace(paragraph)
        if not cleaned:
            continue
        if re.fullmatch(r"(?:[-*]\s*)?(?:TODO|TBD)[:.]?.*", cleaned, re.IGNORECASE):
            continue
        if re.fullmatch(r"(?:output|scripts|tests|docs)/[A-Za-z0-9_./\\-]+", cleaned, re.IGNORECASE):
            continue
        if len(re.findall(r"[A-Za-z]+", cleaned)) >= 10:
            return True
    return False


def strip_tex_nonprose(content: str) -> str:
    stripped = re.sub(r"\\begin\{exe\}.*?\\end\{exe\}", "", content, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{itemize\}.*?\\end\{itemize\}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{enumerate\}.*?\\end\{enumerate\}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\(?:label|hypertarget|protect|phantomsection)\{[^}]*\}", "", stripped)
    stripped = re.sub(r"\\glossquote\{([^}]*)\}", r"\1", stripped)
    stripped = re.sub(r"\\tdim\{([^}]*)\}", r"\1", stripped)
    stripped = re.sub(r"\\tdimword\{([^}]*)\}", r"\1", stripped)
    stripped = re.sub(r"\\(?:[A-Za-z@]+)(?:\[[^\]]*\])?(?:\{[^{}]*\})?", "", stripped)
    return stripped


def extract_pdf_text(pdf_path: Path) -> str:
    if not pdf_path.exists():
        return ""
    with tempfile.NamedTemporaryFile(suffix=".txt") as handle:
        result = subprocess.run(["pdftotext", str(pdf_path), handle.name], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pdftotext failed for {pdf_path}:\n{result.stderr}")
        return Path(handle.name).read_text(encoding="utf-8", errors="replace")


def tex_body(tex: str) -> str:
    marker = r"\section{" + FIRST_CHAPTER_TITLE + "}"
    if marker in tex:
        return tex.split(marker, 1)[1]
    return tex


def pdf_body(pdf_text: str) -> str:
    match = re.search(rf"\n1\s+{re.escape(FIRST_CHAPTER_TITLE)}\b", pdf_text)
    if match:
        return pdf_text[match.start() :]
    return pdf_text


def collect_example_records(markdown_text: str, bible: dict[str, str]) -> list[ExampleRecord]:
    lines = markdown_text.splitlines()
    records: list[ExampleRecord] = []
    stack: list[tuple[int, str]] = []
    supplement_rows = assembler.load_normalization_supplements()
    index = 0

    while index < len(lines):
        line = lines[index]
        heading_match = assembler.MARKDOWN_HEADING_RE.match(line)
        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, title))
            index += 1
            continue

        parsed_example, next_index = assembler.parse_example_at(lines, index)
        if parsed_example:
            heading_path = tuple(title for _, title in stack)
            resolution = assembler.resolve_example_source_metadata(
                parsed_example,
                lines,
                index,
                bible,
                supplement_rows,
                heading_path,
            )
            records.append(
                ExampleRecord(
                    label=parsed_example.label,
                    source=resolution.resolved_source,
                    header_source=resolution.header_source,
                    contextual_source=resolution.contextual_source,
                    supplement_sources=resolution.supplement_sources,
                    inferred_source=resolution.inferred_source,
                    heading_path=heading_path,
                    preceding_prose=assembler.extract_preceding_prose(lines, index),
                    explicit_no_source=resolution.explicit_no_source,
                    require_source=resolution.require_source,
                    conflict_message=resolution.conflict_message,
                )
            )
            index = next_index
            continue

        index += 1

    return records


def parse_tex_examples(tex: str) -> dict[str, str]:
    examples: dict[str, str] = {}
    for match in re.finditer(r"\\begin\{exe\}(.*?)\\end\{exe\}", tex, re.DOTALL):
        block = match.group(1)
        label_match = re.search(r"\\ex\s+\\label\{([^}]+)\}", block)
        glt_match = re.search(r"\\glt\s+(.+)", block)
        if label_match and glt_match:
            examples[label_match.group(1)] = glt_match.group(1).strip()
    return examples


def strip_examples_and_tables(markdown_block: str) -> str:
    lines = markdown_block.splitlines()
    kept: list[str] = []
    index = 0

    while index < len(lines):
        parsed_example, next_index = assembler.parse_example_at(lines, index)
        if parsed_example:
            index = next_index
            continue
        line = lines[index]
        stripped = line.strip()
        if stripped.startswith("|") or stripped.startswith(">"):
            index += 1
            continue
        kept.append(line)
        index += 1

    return "\n".join(kept)


def first_prose_occurrence_has_gloss(section_text: str, form: str, allowed_glosses: tuple[str, ...]) -> bool:
    prose = strip_examples_and_tables(section_text)
    match = re.search(rf"`{re.escape(form)}`", prose)
    if not match:
        return True
    window = prose[match.end() : match.end() + 120]
    return any(re.search(rf"['`][^'\n`]*{gloss}[^'\n`]*['`]", window, re.IGNORECASE) for gloss in allowed_glosses)


def iter_tex_blocks_for_section(tex_blocks: list[TexBlock], section_title: str) -> list[TexBlock]:
    collected: list[TexBlock] = []
    in_section = False
    for block in tex_blocks:
        if block.level == 2 and block.title == section_title:
            in_section = True
            collected = [block]
            continue
        if in_section and block.level <= 2:
            break
        if in_section:
            collected.append(block)
    return collected


def strip_tex_examples_tables_and_lists(content: str) -> str:
    stripped = re.sub(r"\\begin\{exe\}.*?\\end\{exe\}", "", content, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{longtable\}.*?\\end\{longtable\}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{itemize\}.*?\\end\{itemize\}", "", stripped, flags=re.DOTALL)
    stripped = re.sub(r"\\begin\{enumerate\}.*?\\end\{enumerate\}", "", stripped, flags=re.DOTALL)
    return stripped


def find_first_missing_tex_gloss(
    section_title: str,
    section_blocks: list[TexBlock],
    form: str,
    allowed_glosses: tuple[str, ...],
    suggested_gloss: str,
) -> str | None:
    tdim_pattern = re.compile(rf"\\tdim\{{{re.escape(form)}\}}", re.IGNORECASE)
    for block in section_blocks:
        prose = strip_tex_examples_tables_and_lists(block.content)
        match = tdim_pattern.search(prose)
        if not match:
            continue
        window = prose[match.end() : match.end() + 140]
        if any(re.search(rf"\\glossquote\{{[^}}]*{gloss}[^}}]*\}}", window, re.IGNORECASE) for gloss in allowed_glosses):
            return None
        line_number = block.start_line + prose[: match.start()].count("\n")
        return (
            f"Unglossed running-prose form `{form}` in {section_title} near TeX line {line_number}; "
            f"suggested gloss `{suggested_gloss}`"
        )
    return None


def source_category(reference: str) -> str:
    for book in NT_BOOKS:
        if reference.startswith(book + " "):
            return "NT"
    return "OT"


def source_zone(reference: str) -> str:
    for book in GOSPEL_BOOKS:
        if reference.startswith(book + " "):
            return "Gospel"
    for book in NT_BOOKS:
        if reference.startswith(book + " "):
            return "OtherNT"
    return "OT"


def subsection_example_count(block: MarkdownBlock) -> int:
    return len(re.findall(r"^\(@ex:[^)]+\)", block.content, re.MULTILINE))


def gather_quality_issues(tex_path: Path) -> tuple[list[str], dict[str, object]]:
    markdown_path = tex_path.with_suffix(".md")
    pdf_path = tex_path.with_suffix(".pdf")
    markdown = markdown_path.read_text(encoding="utf-8")
    tex = tex_path.read_text(encoding="utf-8")
    pdf_text = extract_pdf_text(pdf_path)
    bible = assembler.load_bible(assembler.BIBLE_PATH)
    markdown_blocks = split_markdown_blocks(markdown)
    tex_blocks = split_tex_blocks(tex)
    examples = collect_example_records(markdown, bible)
    tex_examples = parse_tex_examples(tex)
    issues: list[str] = []

    body_tex = tex_body(tex).replace(r"\_", "_")
    body_pdf = pdf_body(pdf_text)

    for pattern, description in TEX_INTERNAL_PATTERNS:
        match = pattern.search(body_tex)
        if match:
            issues.append(f"Internal prose in TeX body ({description}): {match.group(0)!r}")
    for pattern, description in PDF_INTERNAL_PATTERNS:
        match = pattern.search(body_pdf)
        if match:
            issues.append(f"Internal prose in PDF body ({description}): {match.group(0)!r}")

    for example in examples:
        if example.label == "review-preview-warning":
            continue
        if example.conflict_message:
            issues.append(example.conflict_message)
        glt_line = tex_examples.get(example.label, "")
        if example.require_source and not example.source and not example.explicit_no_source:
            issues.append(f"Example {example.label} requires a source in grammar-facing mode but none was resolved.")
        if example.source and f"({example.source})" not in glt_line:
            issues.append(f"Example {example.label} is missing its source on the \\glt line: {example.source}")
        if example.contextual_source and not example.header_source and not example.source:
            issues.append(
                f"Example {example.label} has a preceding-prose source but no resolved source: {example.contextual_source}"
            )
        if example.contextual_source and not example.header_source and f"({example.contextual_source})" not in glt_line:
            issues.append(
                f"Example {example.label} still relies on preceding prose for its source instead of the \\glt line: {example.contextual_source}"
            )
        if example.supplement_sources and not any(f"({source})" in glt_line for source in example.supplement_sources):
            issues.append(
                f"Example {example.label} is missing its normalization-supplement source on the \\glt line: "
                + ", ".join(example.supplement_sources)
            )

    section_blocks = {
        block.title: block
        for block in markdown_blocks
        if block.level == 2 and block.title in TARGET_SECTION_TITLES
    }
    for block in markdown_blocks:
        if block.title in TARGET_SECTION_TITLES or (block.parent_titles and block.parent_titles[-1] in TARGET_SECTION_TITLES):
            if block.level in {2, 3} and not markdown_block_has_substance(block):
                issues.append(f"Blank Markdown section: {' > '.join((*block.parent_titles, block.title))}")

    for block in tex_blocks:
        if block.title == "References":
            continue
        if block.title in TARGET_SECTION_TITLES or (block.parent_titles and block.parent_titles[-1] in TARGET_SECTION_TITLES):
            if block.level in {2, 3} and not tex_block_has_substance(block):
                issues.append(f"Blank TeX section: {' > '.join((*block.parent_titles, block.title))}")

    for section_title, block in section_blocks.items():
        section_examples = [example for example in examples if section_title in example.heading_path]
        zones = {source_zone(example.source) for example in section_examples if example.source}
        if section_examples and not {"OT", "Gospel"}.issubset(zones):
            issues.append(f"Section {section_title} does not yet show both Old Testament and Gospel example coverage.")

        tex_section_blocks = iter_tex_blocks_for_section(tex_blocks, section_title)
        for form, (allowed_glosses, suggested_gloss) in GLOSSARY_REQUIREMENTS.items():
            missing_gloss_issue = find_first_missing_tex_gloss(
                section_title,
                tex_section_blocks,
                form,
                allowed_glosses,
                suggested_gloss,
            )
            if missing_gloss_issue:
                issues.append(missing_gloss_issue)

    for block in markdown_blocks:
        if block.level != 3 or not block.parent_titles:
            continue
        if block.parent_titles[-1] not in TARGET_SECTION_TITLES:
            continue
        if SUBSECTION_IGNORE_RE.search(block.title):
            continue
        example_count = subsection_example_count(block)
        if example_count == 1 and not ONE_EXAMPLE_NOTE_RE.search(block.content):
            issues.append(
                f"Subsection {block.parent_titles[-1]} > {block.title} has one formal example without an explicit note."
            )
        subsection_examples = [
            example
            for example in examples
            if len(example.heading_path) >= 2
            and example.heading_path[-1] == block.title
            and example.heading_path[-2] == block.parent_titles[-1]
            and example.source
        ]
        subsection_zones = {source_zone(example.source) for example in subsection_examples}
        if subsection_examples and "Gospel" not in subsection_zones:
            if not ONE_EXAMPLE_NOTE_RE.search(block.content):
                issues.append(
                    f"Subsection {block.parent_titles[-1]} > {block.title} uses no formal Gospel example without an explicit explanation."
                )
        if subsection_examples and "OT" not in subsection_zones and not ONE_EXAMPLE_NOTE_RE.search(block.content):
            issues.append(
                f"Subsection {block.parent_titles[-1]} > {block.title} uses no Old Testament example without an explicit explanation."
            )

    if r"\newcommand{\glossquote}[1]{`#1'}" not in tex:
        issues.append(r"Missing \glossquote macro in generated TeX.")
    if any(character in body_tex for character in "‘’“”"):
        issues.append("Generated TeX still contains smart quotes in the grammar-facing body.")
    quote_check_text = re.sub(r"\\tdimword\{[^}]*\}|\\tdim\{[^}]*\}|\\glossquote\{[^}]*\}", "", body_tex)
    quote_check_text = re.sub(r"``[^']+''", "", quote_check_text)
    if re.search(r"(?<![A-Za-z])'[^'\n{}\\]+'(?![A-Za-z])", quote_check_text):
        issues.append("Generated TeX still contains raw straight-quoted English glosses.")
    for preserved in ("pa' inn", "Abraham' suan", "Topa' inn", "na pa' inn-ah"):
        if preserved not in tex:
            issues.append(f"Generated TeX no longer preserves Tedim apostrophe material: {preserved}")

    summary = {
        "pages": next(
            (
                line.split(":", 1)[1].strip()
                for line in subprocess.check_output(["pdfinfo", str(pdf_path)], text=True).splitlines()
                if line.startswith("Pages:")
            ),
            "?",
        )
        if pdf_path.exists()
        else "?",
        "example_count": len([example for example in examples if example.label != "review-preview-warning"]),
        "issues": len(issues),
    }
    return issues, summary


def write_report(report_path: Path, tex_path: Path, issues: list[str], summary: dict[str, object]) -> None:
    tex_display_path = tex_path.resolve()
    if tex_display_path.is_relative_to(ROOT):
        tex_display = tex_display_path.relative_to(ROOT)
    else:
        tex_display = tex_path
    lines = [
        "# Grammar-facing quality report",
        "",
        f"- TeX: `{tex_display}`",
        f"- Issues: {summary['issues']}",
        f"- Pages: {summary['pages']}",
        f"- Formal examples checked: {summary['example_count']}",
        "",
    ]
    if issues:
        lines.extend(["## Failing checks", ""])
        lines.extend(f"- {issue}" for issue in issues)
    else:
        lines.extend(
            [
                "## Result",
                "",
                "- All configured grammar-facing quality gates passed.",
            ]
        )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tex_path", type=Path, help="Path to the generated grammar-facing TeX file.")
    parser.add_argument(
        "--report",
        type=Path,
        default=DEFAULT_REPORT_PATH,
        help="Write the quality report to this Markdown path.",
    )
    args = parser.parse_args()

    issues, summary = gather_quality_issues(args.tex_path)
    write_report(args.report, args.tex_path, issues, summary)
    if issues:
        raise SystemExit(
            "Grammar-facing PDF quality gate failed:\n- " + "\n- ".join(issues) + f"\n\nReport: {args.report}"
        )
    print(f"Grammar-facing PDF quality gate passed. Report: {args.report}")


if __name__ == "__main__":
    main()
