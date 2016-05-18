# coding = utf-8
# __author__ = cwandrews
import pytest

from word_count import WordCounter, LetterCounter


MANU_STRING = 'This is?\r my |file.\nIt is alright\t 123 I suppose...\nThis is !really! just a test.\nI hope it, works'
MANU_STRING_2 = 'This is just another string but longer and with no newlines to test the read_in_string method. is is.'

FRANKEN_TEXT = './static/pg83.txt'
MOON_TEXT = './static/pg84.txt'
MANU_TEXT = './static/test.txt'


@pytest.fixture("class")
def generator_words_good():
    import re

    return (word for word in re.split("\s+", 'This is just for a test.. to see how well...'))


@pytest.fixture("class")
def generator_words_dirty():
    import re

    return (word for word in re.split(
        "\s+", 'This is just| test.. dfadfskj see 123 ?!%G1 is ?!%G1 will dfadfskj'))


@pytest.mark.usefixtures("generator_words_good", "generator_words_dirty")
class TestWordCounter:

    def test_char_counter_takes_str_gen_only(self):
        not_str_gens = tuple(), list(), dict(), set(), int(), str(), bytes(), float(), complex()

        for not_gen in not_str_gens:
            with pytest.raises(AssertionError):
                WordCounter._char_counter(not_gen, length=5)

        assert WordCounter._char_counter(generator_words_good(), length=5)

    def test_char_counter_returns_list_of_tuples_of_strings_and_counts_in_desc_order(self):
        counted_list = WordCounter._char_counter(generator_words_good(), length=5)
        counts_only = [obj[1] for obj in counted_list]

        assert isinstance(counted_list, list)

        for obj in counted_list:
            assert isinstance(obj, tuple)
            assert isinstance(obj[0], str)
            assert isinstance(obj[1], int)

        for i in range(len(counts_only) - 1):
            assert counts_only[i] >= counts_only[i + 1]

    def test_char_counter_returns_no_non_english_words(self):
        english_words = './static/english_words.txt'
        with open(english_words, 'rt') as eng_dict:
            english_dict = list(set([eng_word.lower().rstrip('\n') for eng_word in eng_dict.readlines()]))

        clean_counted_list = WordCounter._char_counter(generator_words_dirty(), length=3)
        words_only = [word[0] for word in clean_counted_list]

        assert 'dfadfskj' not in english_dict
        assert '?!%G1' not in english_dict

        for word in words_only:
            assert word in english_dict

    def test_diff_n_words(self):
        n_words_tup = 15, 35

        for n_words in n_words_tup:
            word_count = WordCounter().read_in_file(filepath=FRANKEN_TEXT, length=n_words)
            assert len(word_count) == n_words

    def test_return_all_if_len_gt_words_in_text(self):

        assert WordCounter().read_in_file(filepath=MANU_TEXT, length=500)

    def test_all_words(self):

            assert WordCounter().read_in_file(filepath=MANU_TEXT, length=None)

    def test_sanitizer_sanitizes(self):
        import re

        spec_chars_re = re.compile("[\d\t\r?|!]")

        strings = MANU_STRING.split('\n')
        sani_gen = WordCounter._sanitize(string_list=strings)

        for string in sani_gen:
            assert not spec_chars_re.findall(string)


class TestLetterCounter:

    def test_diff_n_letters(self):
        n_letters_tup = 1, 26

        for n_letters in n_letters_tup:
            letter_count = LetterCounter().read_in_file(filepath=FRANKEN_TEXT, length=n_letters)
            assert len(letter_count) == n_letters

    def test_all_letters(self):

        assert LetterCounter().read_in_file(filepath=FRANKEN_TEXT, length=None)

    def test_counts_letters_only(self):
        n_letters = 27

        letter_count = LetterCounter().read_in_file(filepath=FRANKEN_TEXT, length=n_letters)
        assert len(letter_count) == 26
