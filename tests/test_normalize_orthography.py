#!/usr/bin/env python3
"""
Regression tests for the orthography normalization script.

These tests ensure that the normalize_orthography.py script correctly converts
IPA/scholarly notation to Bible-style practical orthography.

Run with: python -m pytest tests/test_normalize_orthography.py -v
Or: python tests/test_normalize_orthography.py
"""

import sys
import unittest
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from normalize_orthography import (
    normalize_to_bible,
    normalize_word,
    remove_tone_diacritics,
    add_bible_tier_to_examples,
)


class TestConsonantConversions(unittest.TestCase):
    """Test consonant mappings from IPA to Bible orthography."""
    
    def test_glottal_stop(self):
        """ʔ and Ɂ should become h in final position."""
        self.assertEqual(normalize_to_bible('muʔ'), 'muh')
        self.assertEqual(normalize_to_bible('kaɁ'), 'kah')
        self.assertEqual(normalize_to_bible('hɔìʔ'), 'hoih')
        self.assertEqual(normalize_to_bible('neìɁ'), 'neih')
    
    def test_velar_nasal(self):
        """ŋ should become ng."""
        self.assertEqual(normalize_to_bible('ŋa'), 'nga')
        self.assertEqual(normalize_to_bible('taŋ'), 'tang')
        self.assertEqual(normalize_to_bible('luŋtaŋ'), 'lungtang')
        self.assertEqual(normalize_to_bible('ŋèn'), 'ngen')
    
    def test_velar_fricative(self):
        """x should become kh."""
        self.assertEqual(normalize_to_bible('xa'), 'kha')
        self.assertEqual(normalize_to_bible('xat'), 'khat')
        self.assertEqual(normalize_to_bible('xuak'), 'khuak')
    
    def test_uvular_fricative(self):
        """χ (uvular) should also become kh."""
        self.assertEqual(normalize_to_bible('χa'), 'kha')
    
    def test_aspirated_bilabial(self):
        """pʰ should become ph."""
        self.assertEqual(normalize_to_bible('pʰat'), 'phat')
        self.assertEqual(normalize_to_bible('pʰúk'), 'phuk')
    
    def test_aspirated_alveolar(self):
        """tʰ should become th."""
        self.assertEqual(normalize_to_bible('tʰat'), 'that')
        self.assertEqual(normalize_to_bible('tʰàt'), 'that')
        self.assertEqual(normalize_to_bible('tʰām'), 'tham')
    
    def test_aspirated_velar(self):
        """kʰ should become kh."""
        self.assertEqual(normalize_to_bible('kʰa'), 'kha')
    
    def test_lateral_glottal_sequence(self):
        """lʔ and lɁ should become lh."""
        self.assertEqual(normalize_to_bible('silʔ'), 'silh')
        self.assertEqual(normalize_to_bible('hilɁ'), 'hilh')
        self.assertEqual(normalize_to_bible('valʔ'), 'valh')


class TestVowelConversions(unittest.TestCase):
    """Test vowel mappings from IPA to Bible orthography."""
    
    def test_open_mid_back_rounded(self):
        """ɔ should become aw (when not in diphthong)."""
        self.assertEqual(normalize_to_bible('mɔ'), 'maw')
        self.assertEqual(normalize_to_bible('xɔl'), 'khawl')
        self.assertEqual(normalize_to_bible('tɔŋ'), 'tawng')
    
    def test_alternative_open_mid_back(self):
        """ͻ (Greek omicron with hook) should also become aw."""
        self.assertEqual(normalize_to_bible('mͻ'), 'maw')
    
    def test_schwa(self):
        """ə and ǝ should become a."""
        self.assertEqual(normalize_to_bible('kə'), 'ka')
        self.assertEqual(normalize_to_bible('tǝ'), 'ta')
    
    def test_open_mid_front(self):
        """ɛ should become e."""
        self.assertEqual(normalize_to_bible('mɛ'), 'me')
    
    def test_dotless_i(self):
        """ı should become i."""
        self.assertEqual(normalize_to_bible('mı'), 'mi')
        self.assertEqual(normalize_to_bible('sıŋ'), 'sing')


class TestDiphthongConversions(unittest.TestCase):
    """Test diphthong mappings - critical for correct output."""
    
    def test_oi_diphthong(self):
        """ɔi should become oi, NOT awi."""
        self.assertEqual(normalize_to_bible('hɔi'), 'hoi')
        self.assertEqual(normalize_to_bible('hɔiʔ'), 'hoih')
        self.assertEqual(normalize_to_bible('hɔìʔ'), 'hoih')  # With tone mark
        self.assertEqual(normalize_to_bible('melhɔiɁ'), 'melhoih')
    
    def test_oi_with_tone_marks(self):
        """ɔi with various tone marks should all become oi."""
        self.assertEqual(normalize_to_bible('hɔ́i'), 'hoi')
        self.assertEqual(normalize_to_bible('hɔ̄i'), 'hoi')
        self.assertEqual(normalize_to_bible('hɔ̀i'), 'hoi')
    
    def test_ou_diphthong(self):
        """ɔu should become o (Henderson: 'o' [ou])."""
        self.assertEqual(normalize_to_bible('lɔu'), 'lo')


class TestToneRemoval(unittest.TestCase):
    """Test that tone diacritics are correctly removed."""
    
    def test_acute_accent(self):
        """High tone (acute) should be removed."""
        self.assertEqual(normalize_to_bible('pá'), 'pa')
        self.assertEqual(normalize_to_bible('sám'), 'sam')
    
    def test_macron(self):
        """Mid tone (macron) should be removed."""
        self.assertEqual(normalize_to_bible('pā'), 'pa')
        self.assertEqual(normalize_to_bible('tēl'), 'tel')
    
    def test_grave_accent(self):
        """Low tone (grave) should be removed."""
        self.assertEqual(normalize_to_bible('pà'), 'pa')
        self.assertEqual(normalize_to_bible('kàp'), 'kap')
    
    def test_combining_diacritics(self):
        """Combining tone diacritics should be removed."""
        # These use combining characters rather than precomposed
        self.assertEqual(remove_tone_diacritics('pa\u0301'), 'pa')  # acute
        self.assertEqual(remove_tone_diacritics('pa\u0304'), 'pa')  # macron
        self.assertEqual(remove_tone_diacritics('pa\u0300'), 'pa')  # grave
    
    def test_multiple_tones_in_word(self):
        """Words with multiple toned syllables should have all tones removed."""
        self.assertEqual(normalize_to_bible('lūŋtáŋ'), 'lungtang')
        self.assertEqual(normalize_to_bible('mìttɔ̀'), 'mittaw')


class TestComplexWords(unittest.TestCase):
    """Test complete word conversions with multiple features."""
    
    def test_verb_stems(self):
        """Common verb examples from literature."""
        self.assertEqual(normalize_to_bible('mù'), 'mu')
        self.assertEqual(normalize_to_bible('mùʔ'), 'muh')
        self.assertEqual(normalize_to_bible('ŋèn'), 'ngen')
        self.assertEqual(normalize_to_bible('ŋèt'), 'nget')
        self.assertEqual(normalize_to_bible('kàp'), 'kap')
        self.assertEqual(normalize_to_bible('kàʔ'), 'kah')
    
    def test_case_markers(self):
        """Case marker suffixes."""
        self.assertEqual(normalize_to_bible('-ìn'), '-in')
        self.assertEqual(normalize_to_bible('-àɁ'), '-ah')
        self.assertEqual(normalize_to_bible('-tɔ̀Ɂ'), '-tawh')
        self.assertEqual(normalize_to_bible('-pàn'), '-pan')
        self.assertEqual(normalize_to_bible('-ádíŋ'), '-ading')
    
    def test_aspect_markers(self):
        """Aspect/TAM suffixes."""
        self.assertEqual(normalize_to_bible('-tà'), '-ta')
        self.assertEqual(normalize_to_bible('-xín'), '-khin')
        self.assertEqual(normalize_to_bible('-dén'), '-den')
    
    def test_causative_pairs(self):
        """Suppletive causative pairs."""
        self.assertEqual(normalize_to_bible('sī'), 'si')
        self.assertEqual(normalize_to_bible('tʰàt'), 'that')
        self.assertEqual(normalize_to_bible('hìlɁ'), 'hilh')
    
    def test_compound_words(self):
        """Compound words with multiple morphemes."""
        self.assertEqual(normalize_to_bible('mēlhɔíɁ'), 'melhoih')
        self.assertEqual(normalize_to_bible('xɔ̀lmùn'), 'khawlmun')
        self.assertEqual(normalize_to_bible('lūŋdām'), 'lungdam')


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and potential problem areas."""
    
    def test_empty_string(self):
        """Empty string should return empty string."""
        self.assertEqual(normalize_to_bible(''), '')
    
    def test_plain_ascii(self):
        """Plain ASCII text should pass through unchanged."""
        self.assertEqual(normalize_to_bible('hello'), 'hello')
        self.assertEqual(normalize_to_bible('test'), 'test')
    
    def test_already_bible_orthography(self):
        """Text already in Bible orthography should be mostly unchanged."""
        self.assertEqual(normalize_to_bible('khat'), 'khat')
        self.assertEqual(normalize_to_bible('hoih'), 'hoih')
        self.assertEqual(normalize_to_bible('lungtang'), 'lungtang')
    
    def test_no_double_digraphs(self):
        """Should not create doubled digraphs like ngng or khkh."""
        # If input had ŋŋ it should become ngng, but not ngnggng
        result = normalize_to_bible('taŋŋa')
        self.assertNotIn('ngngng', result)
    
    def test_preserves_punctuation(self):
        """Punctuation should be preserved."""
        self.assertEqual(normalize_to_bible('pà.'), 'pa.')
        self.assertEqual(normalize_to_bible('kàp!'), 'kap!')
    
    def test_hyphenated_affixes(self):
        """Hyphenated affixes should be handled correctly."""
        self.assertEqual(normalize_to_bible('-sàk'), '-sak')
        self.assertEqual(normalize_to_bible('-pìɁ'), '-pih')


class TestReportProcessing(unittest.TestCase):
    """Test processing of literature review report content."""
    
    def test_add_bible_tier_basic(self):
        """Basic example annotation."""
        content = "| sī | 'die' |"
        result = add_bible_tier_to_examples(content)
        self.assertIn('[≈si]', result)
    
    def test_add_bible_tier_complex(self):
        """Complex example with multiple IPA words."""
        content = "| tʰàt | 'kill' |"
        result = add_bible_tier_to_examples(content)
        self.assertIn('[≈that]', result)
    
    def test_skip_headers(self):
        """Headers should not be modified."""
        content = "# Section with ɔ"
        result = add_bible_tier_to_examples(content)
        self.assertNotIn('[≈', result)
    
    def test_skip_already_annotated(self):
        """Already annotated lines should not be double-annotated."""
        content = "sī [≈si] 'die'"
        result = add_bible_tier_to_examples(content)
        # Should not have [≈[≈si]] or similar
        self.assertEqual(result.count('[≈'), 1)
    
    def test_skip_bibliographic_lines(self):
        """Lines with Source: should not be modified."""
        content = "**Source:** Henderson, Eugénie J.A. 1965."
        result = add_bible_tier_to_examples(content)
        self.assertNotIn('[≈', result)


class TestRealWorldExamples(unittest.TestCase):
    """Test with real examples from the literature reviews."""
    
    def test_znc_examples(self):
        """Examples from Zam Ngaih Cing's grammar."""
        # From verb stems - laú has high tone on u, not a diphthong
        self.assertEqual(normalize_to_bible('laú'), 'lau')
        self.assertEqual(normalize_to_bible('laùʔ'), 'lauh')
        
        # From aspect
        self.assertEqual(normalize_to_bible('paī-xín-tà'), 'pai-khin-ta')
        
        # From valency
        self.assertEqual(normalize_to_bible('púk'), 'puk')
        self.assertEqual(normalize_to_bible('pʰúk'), 'phuk')
    
    def test_henderson_examples(self):
        """Examples from Henderson (1965)."""
        # Henderson uses slightly different notation
        self.assertEqual(normalize_to_bible('hai'), 'hai')  # Already standard
        self.assertEqual(normalize_to_bible('ngai'), 'ngai')  # Already standard
    
    def test_sentence_examples(self):
        """Full sentence examples."""
        # Simplified sentence fragment
        sent = "keí paī-xín"
        result = normalize_to_bible(sent)
        self.assertEqual(result, "kei pai-khin")


class TestPrecomposedTonedVowels(unittest.TestCase):
    """Test words with precomposed toned vowels (no IPA chars)."""
    
    def test_macron_vowels(self):
        """Words with macron (mid tone) should be normalized."""
        self.assertEqual(normalize_to_bible('paī'), 'pai')
        self.assertEqual(normalize_to_bible('laī'), 'lai')
        self.assertEqual(normalize_to_bible('sīŋ'), 'sing')
    
    def test_grave_vowels(self):
        """Words with grave accent (low tone) should be normalized."""
        self.assertEqual(normalize_to_bible('kià'), 'kia')
        self.assertEqual(normalize_to_bible('xià'), 'khia')
        self.assertEqual(normalize_to_bible('zàn'), 'zan')
    
    def test_acute_vowels(self):
        """Words with acute accent (high tone) should be normalized."""
        self.assertEqual(normalize_to_bible('siál'), 'sial')
        self.assertEqual(normalize_to_bible('púk'), 'puk')
        self.assertEqual(normalize_to_bible('múk'), 'muk')
    
    def test_mixed_tones(self):
        """Words with multiple different tones."""
        self.assertEqual(normalize_to_bible('lisàk'), 'lisak')
        self.assertEqual(normalize_to_bible('lisák'), 'lisak')
        self.assertEqual(normalize_to_bible('cīŋnɔ̄'), 'cingnaw')
    
    def test_hyphenated_with_tones(self):
        """Hyphenated words with tone marks."""
        self.assertEqual(normalize_to_bible('-laī'), '-lai')
        self.assertEqual(normalize_to_bible('-sàk'), '-sak')
        self.assertEqual(normalize_to_bible('pai-xín-tà'), 'pai-khin-ta')


class TestReportProcessingTonedWords(unittest.TestCase):
    """Test that report processing captures toned words."""
    
    def test_toned_words_in_text(self):
        """Words with only tones (no IPA) should be annotated."""
        content = "paī means 'stay'"
        result = add_bible_tier_to_examples(content)
        self.assertIn('[≈pai]', result)
    
    def test_toned_words_in_tables(self):
        """Toned words in tables should be annotated."""
        content = "| kià | low tone |"
        result = add_bible_tier_to_examples(content)
        self.assertIn('[≈kia]', result)
    
    def test_toned_words_in_code_spans(self):
        """Toned words in backticks should be annotated."""
        content = "`siál hǎn tʰàt` means ..."
        result = add_bible_tier_to_examples(content)
        self.assertIn('[≈sial]', result)
        self.assertIn('[≈that]', result)
    
    def test_words_inside_brackets_skipped(self):
        """Words inside phonetic brackets should not get nested annotations."""
        content = "The phoneme [ɔ] is written as 'aw'"
        result = add_bible_tier_to_examples(content)
        # Should not have [≈aw] inside the brackets
        self.assertNotIn('[ɔ [≈', result)


def run_tests():
    """Run all tests and report results."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestConsonantConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestVowelConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestDiphthongConversions))
    suite.addTests(loader.loadTestsFromTestCase(TestToneRemoval))
    suite.addTests(loader.loadTestsFromTestCase(TestComplexWords))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestReportProcessing))
    suite.addTests(loader.loadTestsFromTestCase(TestRealWorldExamples))
    suite.addTests(loader.loadTestsFromTestCase(TestPrecomposedTonedVowels))
    suite.addTests(loader.loadTestsFromTestCase(TestReportProcessingTonedWords))
    
    # Run with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
