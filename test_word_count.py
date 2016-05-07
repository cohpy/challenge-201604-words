# coding = utf-8
# author = cwandrews

import pytest


TARGET_STRING = 'This is? my file.\nIt is alright I suppose...\nThis is !really! just a test.\nI hope it, works'
TARGET_STRING2 = 'This is just another string but longer and with no newlines to test the read_in_string method. is is.'
# Target text to be read (Frankenstein)
TARGET_FILE = './static_files/pg83.txt'
TARGET_FILE2 = './static_files/pg84.txt'
TEST_TXT = './static_files/test.txt'
DOES_NOT_EXIST = './static_files/fake.txt'


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
