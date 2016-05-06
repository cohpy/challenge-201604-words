# coding = utf-8
# author = cwandrews

import pytest

TARGET_FILE = './static_files/pg83.txt'


@pytest.mark.parametrize("num_words", (range(1, 21)))
def test_wordcounter_len(num_words):
    from word_count import WordCounter

    word_count = WordCounter().read_in_file(filepath=TARGET_FILE, length=num_words)
    print(len(word_count))
    assert len(word_count) == num_words


@pytest.mark.parametrize("num_letters", (range(1, 27)))
def test_lettercounter_len(num_letters):
    from word_count import LetterCounter

    letter_count = LetterCounter().read_in_file(filepath=TARGET_FILE, length=num_letters)
    assert len(letter_count) == num_letters


def test_lettercounter_letters_only(num_letters=27):
    from word_count import LetterCounter

    with pytest.raises(StopIteration):
        LetterCounter().read_in_file(filepath=TARGET_FILE, length=num_letters)
