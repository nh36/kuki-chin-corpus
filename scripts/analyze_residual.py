#!/usr/bin/env python3
"""
Residual Word Analyzer for Tedim Chin

A comprehensive philological analyzer for the ~7,341 unknown tokens remaining
after primary morphological analysis. For each unknown word, this analyzer:

1. Collects all Bible verse contexts (Tedim + KJV English)
2. Infers likely semantics from verse content patterns
3. Analyzes morphological structure (prefixes, stems, suffixes)
4. Identifies potential base stems (even if not in lexicon)
5. Cross-references with related Kuki-Chin languages
6. Classifies: loan words, dialectal forms, archaic forms, compounds
7. Generates detailed per-word philological reports

Usage:
    python analyze_residual.py                 # Full analysis, generates reports
    python analyze_residual.py --word WORD    # Analyze single word
    python analyze_residual.py --category CAT # Analyze one category
    python analyze_residual.py --summary      # Summary statistics only
"""

import sys
import re
import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Tuple, Optional, Dict, Set
from dataclasses import dataclass, field
from datetime import datetime

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class VerseContext:
    """A single verse occurrence with both Tedim and English text."""
    verse_id: str
    reference: str  # e.g., "Genesis 1:1"
    tedim_text: str
    english_text: str
    
@dataclass
class MorphAnalysis:
    """Morphological analysis of a word form."""
    word: str
    prefix: Optional[str] = None
    prefix_gloss: Optional[str] = None
    stem: Optional[str] = None
    stem_gloss: Optional[str] = None
    suffix: Optional[str] = None
    suffix_gloss: Optional[str] = None
    reduplication: bool = False
    compound_parts: List[str] = field(default_factory=list)
    confidence: str = "low"  # low, medium, high
    notes: str = ""

@dataclass
class WordReport:
    """Complete philological report for a single word."""
    word: str
    frequency: int
    contexts: List[VerseContext]
    morph_analysis: MorphAnalysis
    semantic_inference: str
    classification: str  # loan, dialect, archaic, compound, unknown
    loan_source: Optional[str] = None
    related_forms: List[str] = field(default_factory=list)
    cross_kc_matches: Dict[str, str] = field(default_factory=dict)
    confidence: str = "low"
    notes: str = ""

# =============================================================================
# KNOWN MORPHOLOGY (from analyze_morphemes.py)
# =============================================================================

PRONOMINAL_PREFIXES = {
    'ka': '1SG', 'na': '2SG', 'a': '3SG', 'i': '1PL.INCL',
    'kong': '1SG.OBJ', 'hong': '3→1',
}

COMMON_PREFIXES = {
    'ki': 'REFL/RECIP',
    'kik': 'ITER',
    'hong': 'DIR',
}

COMMON_SUFFIXES = {
    'na': 'NMLZ', 'te': 'PL', 'uh': 'PL',
    'in': 'ERG/INST', 'ah': 'LOC', 'pan': 'ABL',
    'ding': 'PROSP', 'ta': 'PFV', 'zo': 'COMPL',
    'lo': 'NEG', 'khin': 'IMM', 'nawn': 'CONT',
    'sak': 'CAUS', 'pih': 'CAUS', 'khia': 'DIR.out',
    'toh': 'COM', 'tawh': 'COM', 'zaw': 'COMP',
    'pen': 'TOP', 'mah': 'EMPH',
}

# Known loan word markers (English/Burmese/Hindi patterns)
LOAN_PATTERNS = {
    r'^(dr|kr|br|pr|tr|gr|fr|sp|st|sk|sc|pl|bl|cl|fl|sl)': 'english_cluster',
    r'(tion|sion|ment|ness|able|ible)$': 'english_suffix',
    r'^(di|tri|bi|uni|multi|semi|anti|pre|post|re|de|un|in|im)': 'english_prefix',
    r'[fvz]': 'possibly_english',  # f, v, z rare in native KC
}

# =============================================================================
# FILE PATHS
# =============================================================================

BASE_DIR = Path(__file__).parent.parent
BIBLE_DIR = BASE_DIR / "bibles" / "extracted"
DATA_DIR = BASE_DIR / "data"
ANALYSIS_DIR = BASE_DIR / "analysis"
REPORTS_DIR = ANALYSIS_DIR / "residual_reports"

# =============================================================================
# CORPUS LOADING
# =============================================================================

class CorpusLoader:
    """Load and index Bible corpus data."""
    
    def __init__(self):
        self.tedim_verses: Dict[str, Tuple[str, str]] = {}  # verse_id -> (ref, text)
        self.english_verses: Dict[str, Tuple[str, str]] = {}
        self.word_index: Dict[str, List[str]] = defaultdict(list)  # word -> [verse_ids]
        self.kc_lexicons: Dict[str, Dict[str, int]] = {}  # lang -> word -> freq
        
    def load_tedim_bible(self) -> int:
        """Load Tedim Bible and build word index."""
        ctd_file = BIBLE_DIR / "ctd" / "ctd-x-bible.txt"
        if not ctd_file.exists():
            print(f"Error: {ctd_file} not found")
            return 0
            
        count = 0
        with open(ctd_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue
                verse_id, text = parts
                ref = self._verse_id_to_ref(verse_id)
                self.tedim_verses[verse_id] = (ref, text)
                
                # Index words
                words = re.findall(r"[a-zA-Z']+", text.lower())
                for word in words:
                    if len(word) >= 2:
                        self.word_index[word].append(verse_id)
                count += 1
        return count
    
    def load_english_bible(self) -> int:
        """Load KJV English Bible."""
        eng_file = BIBLE_DIR / "eng" / "eng-engkjv.txt"
        if not eng_file.exists():
            # Try alternate filename
            eng_files = list((BIBLE_DIR / "eng").glob("*.txt"))
            if eng_files:
                eng_file = eng_files[0]
            else:
                print("Warning: English Bible not found")
                return 0
                
        count = 0
        with open(eng_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split('\t', 1)
                if len(parts) != 2:
                    continue
                verse_id, text = parts
                ref = self._verse_id_to_ref(verse_id)
                self.english_verses[verse_id] = (ref, text)
                count += 1
        return count
    
    def load_kc_lexicons(self) -> int:
        """Load lexicons from related Kuki-Chin languages for cross-reference."""
        lexicon_dir = DATA_DIR / "lexicons"
        if not lexicon_dir.exists():
            return 0
            
        count = 0
        for lex_file in lexicon_dir.glob("*_lexicon.tsv"):
            lang = lex_file.stem.replace("_lexicon", "")
            if lang == "ctd":
                continue  # Skip Tedim itself
            self.kc_lexicons[lang] = {}
            with open(lex_file, 'r', encoding='utf-8') as f:
                next(f)  # Skip header
                for line in f:
                    parts = line.strip().split('\t')
                    if len(parts) >= 2:
                        word = parts[0].lower()
                        freq = int(parts[1]) if parts[1].isdigit() else 1
                        self.kc_lexicons[lang][word] = freq
            count += 1
        return count
    
    def _verse_id_to_ref(self, verse_id: str) -> str:
        """Convert verse ID like '01001001' to 'Genesis 1:1'."""
        books = {
            '01': 'Genesis', '02': 'Exodus', '03': 'Leviticus', '04': 'Numbers',
            '05': 'Deuteronomy', '06': 'Joshua', '07': 'Judges', '08': 'Ruth',
            '09': '1 Samuel', '10': '2 Samuel', '11': '1 Kings', '12': '2 Kings',
            '13': '1 Chronicles', '14': '2 Chronicles', '15': 'Ezra', '16': 'Nehemiah',
            '17': 'Esther', '18': 'Job', '19': 'Psalms', '20': 'Proverbs',
            '21': 'Ecclesiastes', '22': 'Song of Solomon', '23': 'Isaiah',
            '24': 'Jeremiah', '25': 'Lamentations', '26': 'Ezekiel', '27': 'Daniel',
            '28': 'Hosea', '29': 'Joel', '30': 'Amos', '31': 'Obadiah',
            '32': 'Jonah', '33': 'Micah', '34': 'Nahum', '35': 'Habakkuk',
            '36': 'Zephaniah', '37': 'Haggai', '38': 'Zechariah', '39': 'Malachi',
            '40': 'Matthew', '41': 'Mark', '42': 'Luke', '43': 'John',
            '44': 'Acts', '45': 'Romans', '46': '1 Corinthians', '47': '2 Corinthians',
            '48': 'Galatians', '49': 'Ephesians', '50': 'Philippians', '51': 'Colossians',
            '52': '1 Thessalonians', '53': '2 Thessalonians', '54': '1 Timothy',
            '55': '2 Timothy', '56': 'Titus', '57': 'Philemon', '58': 'Hebrews',
            '59': 'James', '60': '1 Peter', '61': '2 Peter', '62': '1 John',
            '63': '2 John', '64': '3 John', '65': 'Jude', '66': 'Revelation',
        }
        if len(verse_id) < 8:
            return verse_id
        book_num = verse_id[:2]
        chapter = int(verse_id[2:5])
        verse = int(verse_id[5:8])
        book_name = books.get(book_num, f"Book{book_num}")
        return f"{book_name} {chapter}:{verse}"
    
    def get_word_contexts(self, word: str, max_contexts: int = 20) -> List[VerseContext]:
        """Get all verse contexts for a word."""
        contexts = []
        verse_ids = self.word_index.get(word.lower(), [])
        
        for verse_id in verse_ids[:max_contexts]:
            if verse_id in self.tedim_verses:
                ref, tedim = self.tedim_verses[verse_id]
                eng_ref, english = self.english_verses.get(verse_id, (ref, ""))
                contexts.append(VerseContext(
                    verse_id=verse_id,
                    reference=ref,
                    tedim_text=tedim,
                    english_text=english
                ))
        return contexts
    
    def find_in_kc_languages(self, word: str) -> Dict[str, int]:
        """Find word in other Kuki-Chin language lexicons."""
        matches = {}
        word_lower = word.lower()
        for lang, lexicon in self.kc_lexicons.items():
            if word_lower in lexicon:
                matches[lang] = lexicon[word_lower]
        return matches

# =============================================================================
# MORPHOLOGICAL ANALYZER
# =============================================================================

class MorphAnalyzer:
    """Analyze morphological structure of unknown words."""
    
    def __init__(self, known_stems: Set[str]):
        self.known_stems = known_stems
        
    def analyze(self, word: str) -> MorphAnalysis:
        """Perform morphological analysis on a word."""
        analysis = MorphAnalysis(word=word)
        remaining = word.lower()
        
        # Check for reduplication (X~X pattern)
        if '~' in word or '-' in word:
            parts = re.split(r'[~-]', word)
            if len(parts) == 2 and parts[0] == parts[1]:
                analysis.reduplication = True
                analysis.stem = parts[0]
                analysis.notes = f"Reduplicated form of '{parts[0]}'"
                analysis.confidence = "high"
                return analysis
        
        # Check for ki- prefix
        if remaining.startswith('ki'):
            analysis.prefix = 'ki'
            analysis.prefix_gloss = 'REFL/RECIP'
            remaining = remaining[2:]
        
        # Check for other prefixes
        for prefix, gloss in PRONOMINAL_PREFIXES.items():
            if remaining.startswith(prefix) and len(remaining) > len(prefix):
                analysis.prefix = prefix
                analysis.prefix_gloss = gloss
                remaining = remaining[len(prefix):]
                break
        
        # Check for suffixes (work backwards)
        for suffix, gloss in sorted(COMMON_SUFFIXES.items(), key=lambda x: -len(x[0])):
            if remaining.endswith(suffix) and len(remaining) > len(suffix):
                analysis.suffix = suffix
                analysis.suffix_gloss = gloss
                remaining = remaining[:-len(suffix)]
                break
        
        # What remains is the stem
        analysis.stem = remaining
        
        # Check if stem is known
        if remaining in self.known_stems:
            analysis.stem_gloss = "[KNOWN]"
            analysis.confidence = "high"
        elif len(remaining) <= 4:
            # Short stem - likely a basic vocabulary item
            analysis.notes = f"Short stem '{remaining}' - possible basic vocabulary"
            analysis.confidence = "medium"
        else:
            # Check for compound structure
            compound_parts = self._find_compound_parts(remaining)
            if compound_parts:
                analysis.compound_parts = compound_parts
                analysis.notes = f"Possible compound: {' + '.join(compound_parts)}"
                analysis.confidence = "medium"
            else:
                analysis.confidence = "low"
        
        return analysis
    
    def _find_compound_parts(self, word: str) -> List[str]:
        """Try to decompose word into known stems."""
        if len(word) < 4:
            return []
        
        # Try splitting at each position
        for i in range(2, len(word) - 1):
            left = word[:i]
            right = word[i:]
            if left in self.known_stems and right in self.known_stems:
                return [left, right]
            # Also check with known morphemes
            for suffix in COMMON_SUFFIXES:
                if right.startswith(suffix) or right.endswith(suffix):
                    base = right.replace(suffix, '')
                    if left in self.known_stems and base in self.known_stems:
                        return [left, base, f"({suffix})"]
        return []

# =============================================================================
# SEMANTIC INFERENCER
# =============================================================================

class SemanticInferencer:
    """Infer semantics from verse contexts."""
    
    # Common semantic field keywords
    SEMANTIC_FIELDS = {
        'agriculture': ['seed', 'sow', 'reap', 'harvest', 'field', 'grain', 'wheat', 'barley', 'vineyard', 'fruit', 'plant', 'grow'],
        'body': ['hand', 'foot', 'eye', 'ear', 'mouth', 'head', 'heart', 'blood', 'flesh', 'bone', 'face', 'body'],
        'emotion': ['love', 'hate', 'fear', 'joy', 'sorrow', 'anger', 'peace', 'hope', 'grief', 'rejoice'],
        'motion': ['go', 'come', 'walk', 'run', 'return', 'enter', 'depart', 'follow', 'flee', 'journey'],
        'speech': ['say', 'speak', 'tell', 'ask', 'answer', 'call', 'cry', 'pray', 'praise', 'sing'],
        'perception': ['see', 'hear', 'know', 'understand', 'perceive', 'behold', 'witness'],
        'possession': ['give', 'take', 'receive', 'have', 'own', 'offer', 'bring', 'keep', 'lose'],
        'religion': ['god', 'lord', 'temple', 'priest', 'sacrifice', 'altar', 'worship', 'holy', 'sin', 'bless'],
        'kinship': ['father', 'mother', 'son', 'daughter', 'brother', 'sister', 'wife', 'husband', 'child'],
        'authority': ['king', 'servant', 'master', 'judge', 'rule', 'command', 'obey', 'govern'],
        'conflict': ['war', 'fight', 'enemy', 'battle', 'sword', 'kill', 'destroy', 'conquer', 'defeat'],
        'temporal': ['day', 'night', 'year', 'time', 'morning', 'evening', 'hour', 'season', 'forever'],
    }
    
    def infer_semantics(self, word: str, contexts: List[VerseContext]) -> Tuple[str, str]:
        """Infer likely meaning from verse contexts.
        
        Returns: (inferred_meaning, confidence)
        """
        if not contexts:
            return "No contexts available", "none"
        
        # Collect all English words from contexts
        all_english = ' '.join(ctx.english_text.lower() for ctx in contexts)
        english_words = re.findall(r'[a-z]+', all_english)
        word_freq = Counter(english_words)
        
        # Identify semantic fields
        field_scores = {}
        for field, keywords in self.SEMANTIC_FIELDS.items():
            score = sum(word_freq.get(kw, 0) for kw in keywords)
            if score > 0:
                field_scores[field] = score
        
        # Get most common content words (excluding function words)
        function_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                         'of', 'with', 'by', 'from', 'that', 'this', 'it', 'is', 'are', 'was',
                         'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 
                         'did', 'shall', 'will', 'would', 'could', 'should', 'may', 'might',
                         'must', 'can', 'he', 'she', 'they', 'him', 'her', 'them', 'his',
                         'their', 'i', 'you', 'we', 'me', 'us', 'my', 'your', 'our', 'as',
                         'not', 'no', 'so', 'if', 'then', 'when', 'which', 'who', 'whom',
                         'all', 'each', 'every', 'any', 'some', 'one', 'two', 'three',
                         'into', 'unto', 'upon', 'out', 'up', 'down', 'over', 'under'}
        
        content_words = [(w, c) for w, c in word_freq.most_common(50) 
                        if w not in function_words and len(w) > 2]
        
        # Build inference
        if len(contexts) >= 5:
            # More contexts = higher confidence
            if content_words:
                top_words = [w for w, _ in content_words[:5]]
                inference = f"Common context words: {', '.join(top_words)}"
                if field_scores:
                    top_field = max(field_scores, key=field_scores.get)
                    inference += f"; semantic field: {top_field}"
                confidence = "medium" if len(contexts) >= 10 else "low"
            else:
                inference = "No clear semantic pattern"
                confidence = "low"
        elif len(contexts) >= 2:
            if content_words:
                top_words = [w for w, _ in content_words[:3]]
                inference = f"Appears with: {', '.join(top_words)}"
                confidence = "low"
            else:
                inference = "Limited context"
                confidence = "very_low"
        else:
            # Single occurrence - hapax
            inference = f"Hapax legomenon in {contexts[0].reference}"
            if content_words:
                inference += f"; context: {', '.join(w for w, _ in content_words[:5])}"
            confidence = "very_low"
        
        return inference, confidence

# =============================================================================
# CLASSIFIER
# =============================================================================

class WordClassifier:
    """Classify unknown words into categories."""
    
    def classify(self, word: str, morph: MorphAnalysis, 
                 kc_matches: Dict[str, int]) -> Tuple[str, Optional[str]]:
        """Classify word and identify loan source if applicable.
        
        Returns: (classification, loan_source)
        """
        word_lower = word.lower()
        
        # Check for English loan patterns
        for pattern, marker in LOAN_PATTERNS.items():
            if re.search(pattern, word_lower):
                return "loan", "English"
        
        # Check for common English words
        english_words = {
            'amen', 'hallelujah', 'hosanna', 'sabbath', 'manna', 'alpha', 'omega',
            'pharisee', 'sadducee', 'synagogue', 'rabbi', 'talent', 'denarius',
        }
        if word_lower in english_words:
            return "loan", "Greek/Hebrew via English"
        
        # Check if found in other KC languages (not a loan)
        if kc_matches:
            if len(kc_matches) >= 3:
                return "pan-KC", None  # Common across KC languages
            else:
                langs = ', '.join(kc_matches.keys())
                return "dialect", f"shared with {langs}"
        
        # Check morphological structure
        if morph.reduplication:
            return "reduplication", None
        
        if morph.compound_parts:
            return "compound", None
        
        if morph.prefix == 'ki':
            return "ki-derivation", None
        
        # Check for archaic markers (rare words in specific books)
        # This would need more context
        
        return "unknown", None

# =============================================================================
# REPORT GENERATOR
# =============================================================================

class ReportGenerator:
    """Generate philological reports for unknown words."""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_word_report(self, report: WordReport) -> str:
        """Generate markdown report for a single word."""
        lines = [
            f"# Residual Word Analysis: `{report.word}`",
            "",
            f"**Frequency:** {report.frequency} occurrences",
            f"**Classification:** {report.classification}",
            f"**Confidence:** {report.confidence}",
        ]
        
        if report.loan_source:
            lines.append(f"**Loan Source:** {report.loan_source}")
        
        lines.extend(["", "## Morphological Analysis", ""])
        morph = report.morph_analysis
        if morph.prefix:
            lines.append(f"- **Prefix:** `{morph.prefix}` ({morph.prefix_gloss})")
        if morph.stem:
            lines.append(f"- **Stem:** `{morph.stem}`" + 
                        (f" ({morph.stem_gloss})" if morph.stem_gloss else ""))
        if morph.suffix:
            lines.append(f"- **Suffix:** `{morph.suffix}` ({morph.suffix_gloss})")
        if morph.reduplication:
            lines.append("- **Reduplication:** Yes")
        if morph.compound_parts:
            lines.append(f"- **Compound parts:** {' + '.join(morph.compound_parts)}")
        if morph.notes:
            lines.append(f"- **Notes:** {morph.notes}")
        
        lines.extend(["", "## Semantic Inference", ""])
        lines.append(report.semantic_inference)
        
        if report.cross_kc_matches:
            lines.extend(["", "## Cross-KC Attestations", ""])
            for lang, freq in report.cross_kc_matches.items():
                lines.append(f"- **{lang}:** {freq}x")
        
        if report.related_forms:
            lines.extend(["", "## Related Forms", ""])
            for form in report.related_forms:
                lines.append(f"- `{form}`")
        
        lines.extend(["", "## Verse Contexts", ""])
        for i, ctx in enumerate(report.contexts[:10], 1):
            lines.append(f"### {i}. {ctx.reference}")
            lines.append(f"**Tedim:** {ctx.tedim_text}")
            lines.append(f"**KJV:** {ctx.english_text}")
            lines.append("")
        
        if len(report.contexts) > 10:
            lines.append(f"*({len(report.contexts) - 10} more occurrences not shown)*")
        
        if report.notes:
            lines.extend(["", "## Additional Notes", ""])
            lines.append(report.notes)
        
        return '\n'.join(lines)
    
    def generate_category_report(self, category: str, reports: List[WordReport]) -> str:
        """Generate summary report for a category of words."""
        lines = [
            f"# Residual Words: {category.title()}",
            "",
            f"**Total words:** {len(reports)}",
            f"**Total tokens:** {sum(r.frequency for r in reports)}",
            "",
            "## Word List",
            "",
            "| Word | Freq | Stem | Inference | Confidence |",
            "|------|------|------|-----------|------------|",
        ]
        
        for r in sorted(reports, key=lambda x: -x.frequency)[:100]:
            stem = r.morph_analysis.stem or r.word
            inference = r.semantic_inference[:40] + "..." if len(r.semantic_inference) > 40 else r.semantic_inference
            lines.append(f"| `{r.word}` | {r.frequency} | `{stem}` | {inference} | {r.confidence} |")
        
        if len(reports) > 100:
            lines.append(f"\n*({len(reports) - 100} more words not shown)*")
        
        return '\n'.join(lines)
    
    def generate_summary_report(self, all_reports: Dict[str, List[WordReport]]) -> str:
        """Generate overall summary statistics."""
        lines = [
            "# Residual Word Analysis: Summary Report",
            "",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Category Breakdown",
            "",
            "| Category | Types | Tokens | % of Residual |",
            "|----------|-------|--------|---------------|",
        ]
        
        total_types = sum(len(reports) for reports in all_reports.values())
        total_tokens = sum(sum(r.frequency for r in reports) for reports in all_reports.values())
        
        for cat, reports in sorted(all_reports.items(), key=lambda x: -sum(r.frequency for r in x[1])):
            types = len(reports)
            tokens = sum(r.frequency for r in reports)
            pct = (tokens / total_tokens * 100) if total_tokens > 0 else 0
            lines.append(f"| {cat} | {types} | {tokens} | {pct:.1f}% |")
        
        lines.extend([
            "",
            f"**Total:** {total_types} types, {total_tokens} tokens",
            "",
            "## Confidence Distribution",
            "",
        ])
        
        # Count by confidence
        conf_counts = Counter()
        for reports in all_reports.values():
            for r in reports:
                conf_counts[r.confidence] += r.frequency
        
        lines.append("| Confidence | Tokens | % |")
        lines.append("|------------|--------|---|")
        for conf in ['high', 'medium', 'low', 'very_low', 'none']:
            if conf in conf_counts:
                pct = (conf_counts[conf] / total_tokens * 100) if total_tokens > 0 else 0
                lines.append(f"| {conf} | {conf_counts[conf]} | {pct:.1f}% |")
        
        lines.extend([
            "",
            "## Loan Words Identified",
            "",
        ])
        
        loans = [(r.word, r.loan_source, r.frequency) 
                 for reports in all_reports.values() 
                 for r in reports if r.classification == "loan"]
        if loans:
            lines.append("| Word | Source | Freq |")
            lines.append("|------|--------|------|")
            for word, source, freq in sorted(loans, key=lambda x: -x[2]):
                lines.append(f"| `{word}` | {source} | {freq} |")
        else:
            lines.append("*No clear loan words identified*")
        
        return '\n'.join(lines)
    
    def save_reports(self, all_reports: Dict[str, List[WordReport]]):
        """Save all reports to files."""
        # Summary
        summary = self.generate_summary_report(all_reports)
        (self.output_dir / "00_summary.md").write_text(summary)
        
        # Category reports
        for cat, reports in all_reports.items():
            cat_report = self.generate_category_report(cat, reports)
            (self.output_dir / f"category_{cat}.md").write_text(cat_report)
        
        # Individual word reports (top 100 by frequency)
        all_words = [(r, cat) for cat, reports in all_reports.items() for r in reports]
        all_words.sort(key=lambda x: -x[0].frequency)
        
        words_dir = self.output_dir / "words"
        words_dir.mkdir(exist_ok=True)
        
        for report, cat in all_words[:200]:
            word_report = self.generate_word_report(report)
            safe_name = re.sub(r'[^a-zA-Z0-9]', '_', report.word)
            (words_dir / f"{safe_name}.md").write_text(word_report)
        
        print(f"Reports saved to {self.output_dir}")

# =============================================================================
# MAIN ANALYZER
# =============================================================================

class ResidualAnalyzer:
    """Main analyzer orchestrating all components."""
    
    def __init__(self):
        self.corpus = CorpusLoader()
        self.known_stems = self._load_known_stems()
        self.morph_analyzer = MorphAnalyzer(self.known_stems)
        self.semantic_inferencer = SemanticInferencer()
        self.classifier = WordClassifier()
        self.reporter = ReportGenerator(REPORTS_DIR)
        self.unknown_words: Dict[str, int] = {}  # word -> frequency
        
    def _load_known_stems(self) -> Set[str]:
        """Load known stems from analyze_morphemes.py."""
        stems = set()
        morph_file = BASE_DIR / "scripts" / "analyze_morphemes.py"
        if morph_file.exists():
            content = morph_file.read_text()
            # Extract stems from dictionaries
            stem_patterns = re.findall(r"'(\w+)':\s*['\"]", content)
            stems.update(stem_patterns)
        return stems
    
    def _load_unknown_words(self) -> int:
        """Run morphological analysis to get current unknowns."""
        import subprocess
        result = subprocess.run(
            ['python3', 'scripts/analyze_morphemes.py', '--stats'],
            cwd=str(BASE_DIR),
            capture_output=True,
            text=True
        )
        
        # Parse unknown words from output
        # This is a fallback; ideally we'd import the module directly
        count = 0
        
        # Alternative: scan corpus directly and check against known morphemes
        for verse_id, (ref, text) in self.corpus.tedim_verses.items():
            words = re.findall(r"[a-zA-Z']+", text)
            for word in words:
                if len(word) >= 2:
                    word_lower = word.lower()
                    # Simple unknown check (would be replaced by actual analyzer)
                    if word_lower not in self.known_stems:
                        self.unknown_words[word_lower] = self.unknown_words.get(word_lower, 0) + 1
                        count += 1
        
        return count
    
    def run_from_wordlist(self, wordlist_file: Path) -> Dict[str, List[WordReport]]:
        """Run analysis on pre-computed unknown word list."""
        if not wordlist_file.exists():
            print(f"Error: {wordlist_file} not found")
            return {}
        
        # Load unknown words from file
        with open(wordlist_file, 'r') as f:
            header = next(f, None)  # Skip header
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 2:
                    word = parts[0]
                    try:
                        freq = int(parts[1])
                    except ValueError:
                        continue  # Skip malformed lines
                    self.unknown_words[word] = freq
        
        return self._analyze_all()
    
    def run_full_analysis(self) -> Dict[str, List[WordReport]]:
        """Run full analysis pipeline."""
        print("Loading corpora...")
        ctd_count = self.corpus.load_tedim_bible()
        eng_count = self.corpus.load_english_bible()
        kc_count = self.corpus.load_kc_lexicons()
        print(f"  Tedim verses: {ctd_count}")
        print(f"  English verses: {eng_count}")
        print(f"  KC lexicons: {kc_count}")
        
        print("Identifying unknown words...")
        self._load_unknown_words()
        print(f"  Unknown types: {len(self.unknown_words)}")
        print(f"  Unknown tokens: {sum(self.unknown_words.values())}")
        
        return self._analyze_all()
    
    def _analyze_all(self) -> Dict[str, List[WordReport]]:
        """Analyze all unknown words and categorize."""
        reports_by_category: Dict[str, List[WordReport]] = defaultdict(list)
        
        total = len(self.unknown_words)
        for i, (word, freq) in enumerate(self.unknown_words.items()):
            if i % 500 == 0:
                print(f"  Analyzing {i}/{total}...")
            
            report = self.analyze_word(word, freq)
            reports_by_category[report.classification].append(report)
        
        return dict(reports_by_category)
    
    def analyze_word(self, word: str, freq: int = 0) -> WordReport:
        """Generate complete analysis for a single word."""
        # Get contexts
        contexts = self.corpus.get_word_contexts(word)
        if freq == 0:
            freq = len(contexts)
        
        # Morphological analysis
        morph = self.morph_analyzer.analyze(word)
        
        # Semantic inference
        sem_inference, sem_confidence = self.semantic_inferencer.infer_semantics(word, contexts)
        
        # Cross-KC matches
        kc_matches = self.corpus.find_in_kc_languages(word)
        
        # Classification
        classification, loan_source = self.classifier.classify(word, morph, kc_matches)
        
        # Find related forms (same stem with different affixes)
        related = self._find_related_forms(word, morph.stem)
        
        # Combine confidence
        if morph.confidence == "high" and sem_confidence in ["medium", "high"]:
            overall_conf = "high"
        elif morph.confidence == "medium" or sem_confidence == "medium":
            overall_conf = "medium"
        elif sem_confidence == "very_low" or sem_confidence == "none":
            overall_conf = "very_low"
        else:
            overall_conf = "low"
        
        return WordReport(
            word=word,
            frequency=freq,
            contexts=contexts,
            morph_analysis=morph,
            semantic_inference=sem_inference,
            classification=classification,
            loan_source=loan_source,
            related_forms=related,
            cross_kc_matches=kc_matches,
            confidence=overall_conf,
        )
    
    def _find_related_forms(self, word: str, stem: Optional[str]) -> List[str]:
        """Find related forms sharing the same stem."""
        if not stem or len(stem) < 3:
            return []
        
        related = []
        for other_word in self.unknown_words:
            if other_word == word:
                continue
            if stem in other_word and len(other_word) < len(word) + 5:
                related.append(other_word)
                if len(related) >= 10:
                    break
        return related
    
    def generate_reports(self, reports_by_category: Dict[str, List[WordReport]]):
        """Generate and save all reports."""
        self.reporter.save_reports(reports_by_category)


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Residual Word Analyzer for Tedim Chin")
    parser.add_argument('--word', type=str, help="Analyze a single word")
    parser.add_argument('--wordlist', type=str, help="Path to unknown word list (word\\tfreq)")
    parser.add_argument('--category', type=str, help="Analyze one category only")
    parser.add_argument('--summary', action='store_true', help="Summary statistics only")
    parser.add_argument('--output', type=str, default=None, help="Output directory")
    
    args = parser.parse_args()
    
    analyzer = ResidualAnalyzer()
    
    if args.output:
        analyzer.reporter = ReportGenerator(Path(args.output))
    
    if args.word:
        # Single word analysis
        print(f"Loading corpora...")
        analyzer.corpus.load_tedim_bible()
        analyzer.corpus.load_english_bible()
        analyzer.corpus.load_kc_lexicons()
        
        report = analyzer.analyze_word(args.word)
        print(analyzer.reporter.generate_word_report(report))
        
    elif args.wordlist:
        # Analyze from pre-computed list
        print("Loading from wordlist...")
        analyzer.corpus.load_tedim_bible()
        analyzer.corpus.load_english_bible()
        analyzer.corpus.load_kc_lexicons()
        
        reports = analyzer.run_from_wordlist(Path(args.wordlist))
        
        if args.summary:
            print(analyzer.reporter.generate_summary_report(reports))
        else:
            analyzer.generate_reports(reports)
            
    else:
        # Full analysis
        reports = analyzer.run_full_analysis()
        
        if args.summary:
            print(analyzer.reporter.generate_summary_report(reports))
        else:
            analyzer.generate_reports(reports)


if __name__ == "__main__":
    main()
