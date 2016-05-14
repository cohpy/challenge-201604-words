# coding = utf-8
# __author__ = cwandrews

import pytest


TARGET_STRING = 'This is? my file.\nIt is alright I suppose...\nThis is !really! just a test.\nI hope it, works'
TARGET_STRING2 = 'This is just another string but longer and with no newlines to test the read_in_string method. is is.'
# Target text to be read (Frankenstein)
TARGET_FILE = './static/pg83.txt'
TARGET_FILE2 = './static/pg84.txt'
TEST_TXT = './static/test.txt'
DOES_NOT_EXIST = './static/fake.txt'


class TestWordCounter:

    def test_char_counter_takes_str_gen_only(self):
        from word_count import WordCounter

        str_genexp = (word for word in 'This is just for a test..')
        not_str_gens = tuple(), list(), dict(), set(), int(), str(), bytes(), float(), complex()

        for not_gen in not_str_gens:
            with pytest.raises(AssertionError):
                WordCounter._char_counter(not_gen)

        assert WordCounter._char_counter(str_genexp)

    def test_char_counter_returns_list_of_tuples_of_strings_and_counts(self):
        from word_count import WordCounter

        str_genexp = (word for word in 'This is just for a test..')
        counted_list = WordCounter._char_counter(str_genexp)

        assert isinstance(counted_list, list)

        for obj in counted_list:
            assert isinstance(obj, tuple)
            assert isinstance(obj[0], str)
            assert isinstance(obj[1], int)

    def test_char_counter_returns_no_non_english_words(self):
        from word_count import WordCounter

        english_words = './static/english_words.txt'
        with open(english_words, 'rt') as eng_dict:
            english_dict = list(set([eng_word.lower().rstrip('\n') for eng_word in eng_dict.readlines()]))

        dirty_str_genexp = (word for word in '|This is just dfadfskj for a ?!%G1 test..')
        clean_counted_list = WordCounter._char_counter(dirty_str_genexp)
        words_only = [word[0] for word in clean_counted_list]

        assert 'dfadfskj' not in english_dict
        assert '?!%G1' not in english_dict

        for word in words_only:
            assert word in english_dict

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
