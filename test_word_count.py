# coding = utf-8
# __author__ = cwandrews
import pytest

from word_count import WordCounter, LetterCounter


MANU_STRING = 'This is?\r my |file.\nIt is alright\t 123 I suppose...\nThis is !really! just a test.\nI hope it, works'
MANU_STRING_2 = 'This is just another string but longer and with no newlines to test the read_in_string method. is is.'

FRANKEN_TEXT = './static/pg83.txt'
FRANKEN_TEXT_ABRIDGED = './static/pg84_super_abridged.txt'
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


@pytest.fixture("class")
def strings_list():

    return MANU_STRING.split('\n')


@pytest.mark.usefixtures("generator_words_good", "generator_words_dirty", "strings_list")
class TestWordCounter:

    def test_char_counter_io(self):
        not_str_gens = tuple(), list(), dict(), set(), int(), str(), bytes(), float(), complex()
        counted_list = WordCounter._char_counter(generator_words_good(), length=5)
        counts_only = [obj[1] for obj in counted_list]

        assert WordCounter._char_counter(generator_words_dirty(), 5)

        assert isinstance(counted_list, list)

        for obj in counted_list:
            assert isinstance(obj, tuple)
            assert isinstance(obj[0], str)
            assert isinstance(obj[1], int)

        for i in range(len(counts_only) - 1):
            assert counts_only[i] >= counts_only[i + 1]

        for not_gen in not_str_gens:
            with pytest.raises(AssertionError):
                WordCounter._char_counter(not_gen, length=5)

        assert WordCounter._char_counter(generator_words_good(), length=5)

    def test_char_counter_returns_only_english_words(self):
        english_words = './static/english_words.txt'
        with open(english_words, 'rt') as eng_dict:
            english_dict = list(set([eng_word.lower().rstrip('\n') for eng_word in eng_dict.readlines()]))

        clean_counted_list = WordCounter._char_counter(generator_words_dirty(), length=3)
        words_only = [word[0] for word in clean_counted_list]

        for not_word in ('dfadfskj', '?!%G1'):
            assert not_word not in english_dict

        for word in words_only:
            assert word in english_dict

    def test_length_matches_returned_word_count(self):

        for n_words in (15, 35):
            assert len(WordCounter().read_in_file(filepath=FRANKEN_TEXT, length=n_words)) == n_words

    def test_return_all_if_len_gt_words_in_text(self):

        assert WordCounter().read_in_file(filepath=MANU_TEXT, length=500)

    def test_length_none_returns_all_words(self):

        assert WordCounter().read_in_file(filepath=MANU_TEXT, length=None)

    def test_sanitizer_io(self):
        from types import GeneratorType

        for iterable_obj in (strings_list(), tuple(strings_list())):
            assert next(WordCounter()._sanitize(string_list=iterable_obj))
            assert isinstance(WordCounter()._sanitize(string_list=iterable_obj), GeneratorType)

        with pytest.raises(AssertionError):
            next(WordCounter()._sanitize(string_list=1))
            next(WordCounter()._sanitize(string_list='just a string'))

    def test_sanitizer_sanitizes(self):
        import re

        spec_chars_re = re.compile("[\d\t\r?|!]")

        for string in WordCounter._sanitize(string_list=strings_list()):
            assert not spec_chars_re.findall(string)

    def test_read_in_file_io(self):
        import re

        gutenberg_re = re.compile("(ebook|electronic|computer)")

        with pytest.raises(AssertionError):
            WordCounter().read_in_file(filepath='/Users/NONE/')
            WordCounter().read_in_file(filepath='/Users/cwandrews')

        assert isinstance(WordCounter().read_in_file(filepath=MANU_TEXT), list)

        for count_tuple in WordCounter().read_in_file(filepath=FRANKEN_TEXT_ABRIDGED, length=None):
            assert not gutenberg_re.findall(count_tuple[0])

    def test_read_in_string_io(self):

        with pytest.raises(AssertionError):
            WordCounter().read_in_string(string=strings_list())
            WordCounter().read_in_string(string=145)

        assert isinstance((WordCounter().read_in_string(string=MANU_STRING)), list)


class TestLetterCounter:

    def test_char_counter_io(self):

        with pytest.raises(AssertionError):
            LetterCounter()._char_counter(sanitized_text_gen=strings_list(), length=5)
            LetterCounter()._char_counter(sanitized_text_gen=MANU_STRING, length=5)

        assert isinstance(LetterCounter()._char_counter(sanitized_text_gen=generator_words_good(), length=5), list)

    def test_letter_counter_io(self):

        assert LetterCounter().read_in_file(filepath=FRANKEN_TEXT_ABRIDGED)
        assert isinstance(LetterCounter().read_in_file(filepath=FRANKEN_TEXT_ABRIDGED), list)

        assert LetterCounter().read_in_string(string=MANU_STRING)
        assert isinstance(LetterCounter().read_in_string(string=MANU_STRING), list)

    def test_diff_n_letters(self):
        n_letters_tup = 1, 26

        for n_letters in n_letters_tup:
            letter_count = LetterCounter().read_in_file(filepath=FRANKEN_TEXT, length=n_letters)
            assert len(letter_count) == n_letters

    def test_all_letters(self):

        assert LetterCounter().read_in_file(filepath=FRANKEN_TEXT_ABRIDGED, length=None)

    def test_counts_letters_only(self):

        assert len(LetterCounter().read_in_file(filepath=FRANKEN_TEXT, length=27)) == 26
