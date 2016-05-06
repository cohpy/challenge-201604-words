# coding = utf-8
# author = cwandrews

import pytest

TARGET_FILE = './static_files/pg83.txt'


@pytest.mark.parametrize("num_words", (range(1, 25)))
def test_wordcounter_len(num_words):
    from word_count import WordCounter

    word_count = WordCounter().read_in_file(filepath=TARGET_FILE, length=num_words)
    print(len(word_count))
    assert len(word_count) == num_words
