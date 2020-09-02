import unittest

from crawler.utils import parse_csv
from crawler.utils import match_hiragana
from crawler.utils import match_katakana
from crawler.utils import match_kanji
from crawler.utils import match_japanese
from crawler.utils import clean_lyrics


class TestUtils(unittest.TestCase):
    def test_parse_csv(self):
        csv_string = 'column_1,column_2,column_3\na,b,c'
        result = list(parse_csv(csv_string))
        self.assertEqual([{'column_1': 'a',
                           'column_2': 'b',
                           'column_3': 'c'}], result)

        csv_string = 'column_1,column_2,column_3\na,b,c\nd,e,f'
        result = list(parse_csv(csv_string))
        self.assertEqual([{'column_1': 'a',
                           'column_2': 'b',
                           'column_3': 'c'},
                          {'column_1': 'd',
                           'column_2': 'e',
                           'column_3': 'f'}], result)

        csv_string = 'column_1,column_2,column_3\na,b,c\nd,e,f\n'
        result = list(parse_csv(csv_string))
        self.assertEqual([{'column_1': 'a',
                           'column_2': 'b',
                           'column_3': 'c'},
                          {'column_1': 'd',
                           'column_2': 'e',
                           'column_3': 'f'}], result)

    def test_match_hiragana(self):
        jp_text = 'ひ'
        result = match_hiragana(jp_text)
        self.assertEqual(True, result)

        jp_text = 'カ'
        result = match_hiragana(jp_text)
        self.assertEqual(False, result)

        jp_text = 'R'
        result = match_hiragana(jp_text)
        self.assertEqual(False, result)

        jp_text = '字'
        result = match_hiragana(jp_text)
        self.assertEqual(False, result)

    def test_match_katakana(self):
        jp_text = 'ひ'
        result = match_katakana(jp_text)
        self.assertEqual(False, result)

        jp_text = 'カ'
        result = match_katakana(jp_text)
        self.assertEqual(True, result)

        jp_text = 'R'
        result = match_katakana(jp_text)
        self.assertEqual(False, result)

        jp_text = '字'
        result = match_katakana(jp_text)
        self.assertEqual(False, result)

    def test_match_kanji(self):
        jp_text = 'ひ'
        result = match_kanji(jp_text)
        self.assertEqual(False, result)

        jp_text = 'カ'
        result = match_kanji(jp_text)
        self.assertEqual(False, result)

        jp_text = 'R'
        result = match_kanji(jp_text)
        self.assertEqual(False, result)

        jp_text = '字'
        result = match_kanji(jp_text)
        self.assertEqual(True, result)

    def test_match_japanese(self):
        jp_text = 'ひ'
        result = match_japanese(jp_text)
        self.assertEqual('ひ', result)

        jp_text = 'カ'
        result = match_japanese(jp_text)
        self.assertEqual('カ', result)

        jp_text = 'R'
        result = match_japanese(jp_text)
        self.assertEqual(str(), result)

        jp_text = '字'
        result = match_japanese(jp_text)
        self.assertEqual('字', result)

    def test_clean_lyrics(self):
        jp_text = 'ひ'
        result = clean_lyrics(jp_text)
        self.assertEqual('ひ', result)

        jp_text = 'カ'
        result = clean_lyrics(jp_text)
        self.assertEqual('カ', result)

        jp_text = 'R'
        result = clean_lyrics(jp_text)
        self.assertEqual(str(), result)

        jp_text = '字'
        result = clean_lyrics(jp_text)
        self.assertEqual('字', result)

        jp_text = 'バカmitai 子供なのね'
        result = clean_lyrics(jp_text)
        self.assertEqual('バカ子供なのね', result)

        jp_text = 'Bakamitai Kodomo na no ne!'
        result = clean_lyrics(jp_text)
        self.assertEqual(str(), result)


if __name__ == '__main__':
    unittest.main()


# TODO CREATE MORE UNIT TESTS
