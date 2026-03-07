#!/usr/bin/env python3
"""
Henderson 1965 OCR Pipeline with Iterative Error Correction.

This script extracts text from Henderson's Tedim Chin grammar PDFs
and builds a self-improving OCR correction system by identifying
recurrent error patterns.

The pipeline:
1. Convert PDF pages to images
2. Run Tesseract OCR on each page
3. Analyze output for common OCR errors
4. Build pattern-based corrections
5. Apply corrections iteratively
6. Export cleaned vocabulary lists

Usage:
    python henderson_ocr.py --extract <pdf_file>
    python henderson_ocr.py --analyze <raw_text_dir>
    python henderson_ocr.py --correct <raw_text_dir>
    python henderson_ocr.py --vocab <corrected_dir>
"""

import sys
import os
import re
import subprocess
from pathlib import Path
from collections import Counter, defaultdict
import json
from typing import List, Dict, Tuple, Optional

# =============================================================================
# OCR ERROR PATTERNS
# =============================================================================

# Common Tesseract OCR errors for linguistic texts
# Format: (wrong_pattern, correct_pattern, description)
KNOWN_OCR_ERRORS = [
    # Character confusions
    (r'\bl\b', 'l', 'isolated l often misread'),
    (r'rn', 'm', 'rn → m confusion'),
    (r'cl', 'd', 'cl → d confusion'),
    (r'vv', 'w', 'vv → w confusion'),
    (r'ii', 'n', 'ii → n confusion (rare)'),
    
    # Diacritics and special characters
    (r"'", "'", 'curly apostrophe normalization'),
    (r'"', '"', 'left curly quote'),
    (r'"', '"', 'right curly quote'),
    
    # Linguistic notation
    (r'\s+', ' ', 'normalize whitespace'),
    (r'(?<=[a-z])\.(?=[a-z])', '-', 'period in morpheme breaks'),
]

# Tedim-specific patterns to watch for
TEDIM_PATTERNS = {
    # Common letter sequences in Tedim
    'valid_onsets': ['p', 't', 'k', 'c', 's', 'h', 'z', 'l', 'm', 'n', 'ng', 'v', 'th', 'kh', 'ph', 'g', 'b', 'd'],
    'valid_codas': ['p', 't', 'k', 'h', 'm', 'n', 'ng', 'l'],
    'vowels': ['a', 'e', 'i', 'o', 'u', 'aw', 'ai', 'au', 'ei', 'ia', 'ua', 'uo'],
}

# =============================================================================
# PDF EXTRACTION
# =============================================================================

def extract_pdf_text(pdf_path: Path, output_dir: Path) -> List[Path]:
    """
    Extract text from PDF using pdftotext (poppler).
    Returns list of output text files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Use pdftotext for initial extraction
    base_name = pdf_path.stem
    output_file = output_dir / f"{base_name}_raw.txt"
    
    cmd = ['pdftotext', '-layout', str(pdf_path), str(output_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error extracting {pdf_path}: {result.stderr}")
        return []
    
    print(f"Extracted: {output_file}")
    return [output_file]


def extract_pdf_with_ocr(pdf_path: Path, output_dir: Path, dpi: int = 300) -> List[Path]:
    """
    Convert PDF to images and OCR each page.
    More accurate for scanned documents.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_name = pdf_path.stem
    img_dir = output_dir / f"{base_name}_images"
    img_dir.mkdir(exist_ok=True)
    
    # Convert PDF to images using pdftoppm
    print(f"Converting {pdf_path} to images...")
    cmd = ['pdftoppm', '-png', '-r', str(dpi), str(pdf_path), str(img_dir / 'page')]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error converting PDF: {result.stderr}")
        return []
    
    # OCR each image
    output_files = []
    for img_file in sorted(img_dir.glob('*.png')):
        txt_file = output_dir / f"{base_name}_{img_file.stem}.txt"
        
        cmd = ['tesseract', str(img_file), str(txt_file.with_suffix('')), '-l', 'eng']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and txt_file.exists():
            output_files.append(txt_file)
            print(f"  OCR'd: {img_file.name} -> {txt_file.name}")
    
    return output_files


# =============================================================================
# ERROR ANALYSIS
# =============================================================================

class OCRErrorAnalyzer:
    """Analyzes OCR output to identify recurring error patterns."""
    
    def __init__(self):
        self.word_counts = Counter()
        self.ngram_counts = defaultdict(Counter)
        self.potential_errors = []
        self.corrections = {}
        
    def add_text(self, text: str):
        """Add text for analysis."""
        words = re.findall(r"[A-Za-z']+", text)
        for word in words:
            self.word_counts[word.lower()] += 1
            
        # Analyze character n-grams
        for n in [2, 3]:
            for i in range(len(text) - n + 1):
                ngram = text[i:i+n].lower()
                if ngram.isalpha():
                    self.ngram_counts[n][ngram] += 1
    
    def find_suspicious_patterns(self) -> List[Tuple[str, int, str]]:
        """
        Find patterns that look like OCR errors.
        Returns list of (pattern, count, reason).
        """
        suspicious = []
        
        # Look for rare bigrams that might be OCR errors
        common_bigrams = set()
        for bigram, count in self.ngram_counts[2].most_common(500):
            common_bigrams.add(bigram)
        
        for bigram, count in self.ngram_counts[2].items():
            if count < 10:
                continue
            if bigram not in common_bigrams:
                # Check if it could be an OCR confusion
                if self._looks_like_ocr_error(bigram):
                    suspicious.append((bigram, count, 'rare bigram, possible OCR confusion'))
        
        # Look for words with unusual character sequences
        for word, count in self.word_counts.items():
            if count < 5:
                continue
            issues = self._check_word_validity(word)
            if issues:
                suspicious.append((word, count, issues))
        
        return sorted(suspicious, key=lambda x: -x[1])[:100]
    
    def _looks_like_ocr_error(self, bigram: str) -> bool:
        """Check if bigram looks like common OCR confusion."""
        error_pairs = [
            ('rn', 'm'), ('cl', 'd'), ('vv', 'w'),
            ('li', 'h'), ('ln', 'm'), ('il', 'h'),
        ]
        for wrong, _ in error_pairs:
            if wrong in bigram:
                return True
        return False
    
    def _check_word_validity(self, word: str) -> str:
        """Check if word has unusual patterns for Tedim."""
        issues = []
        
        # Check for unusual consonant clusters
        clusters = re.findall(r'[bcdfghjklmnpqrstvwxz]{3,}', word)
        if clusters:
            issues.append(f'unusual cluster: {clusters}')
        
        # Check for repeated characters that might be errors
        repeats = re.findall(r'(.)\1\1', word)
        if repeats:
            issues.append(f'triple chars: {repeats}')
        
        return '; '.join(issues) if issues else ''
    
    def suggest_corrections(self, known_words: set) -> Dict[str, str]:
        """
        Suggest corrections based on known word list.
        """
        corrections = {}
        
        for word, count in self.word_counts.items():
            if word in known_words:
                continue
            
            # Try simple substitutions
            for wrong, right in [('rn', 'm'), ('cl', 'd'), ('vv', 'w')]:
                candidate = word.replace(wrong, right)
                if candidate in known_words:
                    corrections[word] = candidate
                    break
        
        return corrections
    
    def export_analysis(self, output_path: Path):
        """Export analysis results to JSON."""
        data = {
            'top_words': dict(self.word_counts.most_common(1000)),
            'top_bigrams': dict(self.ngram_counts[2].most_common(500)),
            'suspicious_patterns': self.find_suspicious_patterns(),
            'suggested_corrections': self.corrections,
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Exported analysis to {output_path}")


# =============================================================================
# TEXT CORRECTION
# =============================================================================

def apply_corrections(text: str, corrections: Dict[str, str]) -> str:
    """Apply word-level corrections to text."""
    words = text.split()
    corrected = []
    
    for word in words:
        # Preserve punctuation
        prefix = ''
        suffix = ''
        core = word
        
        while core and not core[0].isalnum():
            prefix += core[0]
            core = core[1:]
        while core and not core[-1].isalnum():
            suffix = core[-1] + suffix
            core = core[:-1]
        
        # Apply correction
        if core.lower() in corrections:
            core = corrections[core.lower()]
            if word[0].isupper():
                core = core.capitalize()
        
        corrected.append(prefix + core + suffix)
    
    return ' '.join(corrected)


# =============================================================================
# VOCABULARY EXTRACTION
# =============================================================================

def extract_vocabulary(text_files: List[Path], output_path: Path):
    """
    Extract Tedim vocabulary from corrected Henderson texts.
    Looks for vocabulary lists, word definitions, and examples.
    """
    vocab = {}
    
    # Patterns for vocabulary entries
    patterns = [
        # Word : gloss format
        r"([a-z']+)\s*:\s*([^;\n]+)",
        # Word - gloss format
        r"([a-z']+)\s*-\s*([^;\n]+)",
        # Word "gloss" format
        r"([a-z']+)\s*['\"]([^'\"]+)['\"]",
    ]
    
    for text_file in text_files:
        with open(text_file, 'r') as f:
            text = f.read()
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for word, gloss in matches:
                word = word.lower().strip()
                gloss = gloss.strip()
                
                if len(word) > 1 and len(gloss) > 0:
                    if word not in vocab:
                        vocab[word] = []
                    vocab[word].append(gloss)
    
    # Deduplicate and sort
    vocab_list = []
    for word, glosses in sorted(vocab.items()):
        unique_glosses = list(dict.fromkeys(glosses))  # preserve order, remove dupes
        vocab_list.append({
            'word': word,
            'glosses': unique_glosses,
            'primary_gloss': unique_glosses[0] if unique_glosses else ''
        })
    
    # Export
    with open(output_path, 'w') as f:
        json.dump(vocab_list, f, indent=2)
    
    print(f"Extracted {len(vocab_list)} vocabulary entries to {output_path}")
    return vocab_list


# =============================================================================
# MAIN
# =============================================================================

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    path = Path(sys.argv[2])
    
    base_dir = Path(__file__).parent.parent / 'literature' / 'tedim-ctd'
    ocr_dir = base_dir / 'ocr'
    
    if command == '--extract':
        if path.suffix == '.pdf':
            # First try simple text extraction
            raw_dir = ocr_dir / 'raw'
            files = extract_pdf_text(path, raw_dir)
            
            if files:
                # Check quality
                with open(files[0], 'r') as f:
                    sample = f.read(1000)
                
                # If too little text, try OCR
                if len(sample.strip()) < 100:
                    print("Text extraction produced little content, trying OCR...")
                    files = extract_pdf_with_ocr(path, raw_dir)
            
            print(f"Extracted {len(files)} files")
    
    elif command == '--analyze':
        analyzer = OCRErrorAnalyzer()
        
        for txt_file in path.glob('*.txt'):
            with open(txt_file, 'r') as f:
                analyzer.add_text(f.read())
        
        # Show suspicious patterns
        print("\nSuspicious patterns found:")
        for pattern, count, reason in analyzer.find_suspicious_patterns()[:30]:
            print(f"  {count:5d}  {pattern:20s}  {reason}")
        
        # Export analysis
        analyzer.export_analysis(ocr_dir / 'analysis.json')
    
    elif command == '--correct':
        # Load known words from analyzer
        with open(ocr_dir / 'analysis.json', 'r') as f:
            analysis = json.load(f)
        
        corrections = analysis.get('suggested_corrections', {})
        
        corrected_dir = ocr_dir / 'corrected'
        corrected_dir.mkdir(exist_ok=True)
        
        for txt_file in path.glob('*.txt'):
            with open(txt_file, 'r') as f:
                text = f.read()
            
            corrected = apply_corrections(text, corrections)
            
            output_file = corrected_dir / txt_file.name
            with open(output_file, 'w') as f:
                f.write(corrected)
            
            print(f"Corrected: {txt_file.name}")
    
    elif command == '--vocab':
        text_files = list(path.glob('*.txt'))
        output_path = ocr_dir / 'henderson_vocabulary.json'
        extract_vocabulary(text_files, output_path)
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
