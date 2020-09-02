import csv
import re


def parse_csv(csv_string):
    data = list(csv.reader(csv_string.split('\n')))
    labels = data[0]
    rows = data[1:]

    for row in rows:
        if row:
            yield dict(zip(labels, row))


def match_hiragana(char):
    # TODO PROTECT FROM ERRORS
    regex = u'[\u3040-\u309Fー]+'
    match = re.search(regex, char, re.U)
    return bool(match)


def match_katakana(char):
    # TODO PROTECT FROM ERRORS

    regex = u'[\u30A0-\u30FF]+'
    match = re.search(regex, char, re.U)
    return bool(match)


def match_kanji(char):
    # TODO PROTECT FROM ERRORS

    regex = u'[\u4E00-\u9FFF]+'
    match = re.search(regex, char, re.U)
    return bool(match)


def match_japanese(char):
    # TODO PROTECT FROM ERRORS

    if match_hiragana(char):
        return char

    elif match_katakana(char):
        return char

    elif match_kanji(char):
        return char

    return str()


def clean_lyrics(lyrics):
    # TODO PROTECT FROM ERRORS
    # http://www.rikai.com/library/kanjitables/kanji_codes.unicode.shtml
    # https://stackoverflow.com/questions/19899554/unicode-range-for-japanese
    # http://www.localizingjapan.com/kanji-concordance/

    japanese_filter = filter(lambda char: match_japanese(char), lyrics)
    lyrics = ''.join(japanese_filter).strip()
    return lyrics
