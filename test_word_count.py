# coding = utf-8
# author = cwandrews

import pytest


TARGET_FILE2 = './static_files/pg84.txt'

TARGET_STRING = 'This is? my file.\nIt is alright I suppose...\nThis is !really! just a test.\nI hope it, works'
TARGET_STRING2 = ('This is just another string but longer and with no newlines to test the read_in_string method. '
                  'is is.')


@pytest.fixture(scope="function", params=[10, 15, 35])
def test_create_wordcounter_with_read_infile(param):
    from word_count import WordCounter

    TARGET_FILE = './static_files/pg83.txt'
    word_count = WordCounter().read_in_file(TARGET_FILE, param)
    return word_count


@pytest.mark.usefixtures(test_create_wordcounter_with_read_infile)
def test_wordcounter(num_words):
    assert len(test_create_wordcounter_with_read_infile(num_words)) == num_words
