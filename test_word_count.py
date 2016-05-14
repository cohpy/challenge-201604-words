# coding = utf-8
# __author__ = cwandrews

import pytest


TARGET_STRING = 'This is? my file.\nIt is alright I suppose...\nThis is !really! just a test.\nI hope it, works'
TARGET_STRING2 = 'This is just another string but longer and with no newlines to test the read_in_string method. is is.'
# Target text to be read (Frankenstein)
TARGET_FILE = './static_files/pg83.txt'
TARGET_FILE2 = './static_files/pg84.txt'
TEST_TXT = './static_files/test.txt'
DOES_NOT_EXIST = './static_files/fake.txt'


class TestWordCounter:

    def test_diff_n_words(self):
        from word_count import WordCounter

        n_words_tup = 15, 25, 35

        for n_words in n_words_tup:
            word_count = WordCounter().read_in_file(filepath=TARGET_FILE, length=n_words)
            assert len(word_count) == n_words


class TestLetterCounter:

    def test_diff_n_letters(self):
        from word_count import LetterCounter
        n_letters_tup = 1, 26

        for n_letters in n_letters_tup:
            letter_count = LetterCounter().read_in_file(filepath=TARGET_FILE, length=n_letters)
            assert len(letter_count) == n_letters

    def test_counts_letters_only(self):
        from word_count import LetterCounter
        n_letters = 27

        with pytest.raises(StopIteration):
            LetterCounter().read_in_file(filepath=TARGET_FILE, length=n_letters)
