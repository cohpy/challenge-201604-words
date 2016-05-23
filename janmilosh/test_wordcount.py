import pytest
import word_count as wc

data = {
    'gutenberg_filename': 'data/book.txt',
    'no_gutenberg_filename': 'data/no_gutenberg.txt',
    'file_without_gutenberg_text': "\n\n\n\ncan't \"Geneva, March 18th, 17--.\"\n\n\n\"Dear, (dear) Elizabeth!\" _I_ exclaimed, 'when' I had read jörg letter:  \"I\nwill write instantly and heart-sickeningly roses,--in relieve them from the anxiety they must feel-\ning?\"\n\n\n\n\n\n",
    'initial_list': ["can't", '"Geneva,', 'March', '18th,', '17', '."', '"Dear,', '(dear)', 'Elizabeth!"', '_I_', 'exclaimed,', "'when'", 'I', 'had', 'read', 'jörg', 'letter:', '"I', 'will', 'write', 'instantly', 'and', 'heart-sickeningly', 'roses,', 'in', 'relieve', 'them', 'from', 'the', 'anxiety', 'they', 'must', 'feeling?"'],
    'no_numbers_list': ["can't", "\"Geneva,", "March", ".\"", "\"Dear,", "(dear)", "Elizabeth!\"", "_I_", "exclaimed,", "'when'", "I", "had", "read", "jörg", "letter:", "\"I", "will", "write", "instantly", "and", "heart-sickeningly", "roses,", "in", "relieve", "them", "from", "the", "anxiety", "they", "must", "feeling?\""],
    'no_punctuation_list': ["can't", "geneva", "march", "", "dear", "dear", "elizabeth", "i", "exclaimed", "when", "i", "had", "read", "jörg", "letter", "i", "will", "write", "instantly", "and", "heart-sickeningly", "roses", "in", "relieve", "them", "from", "the", "anxiety", "they", "must", "feeling"],
    'word_list': ["can't", "geneva", "march", "dear", "dear", "elizabeth", "i", "exclaimed", "when", "i", "had", "read", "jörg", "letter", "i", "will", "write", "instantly", "and", "heart-sickeningly", "roses", "in", "relieve", "them", "from", "the", "anxiety", "they", "must", "feeling"],
    'word_dict': {"can't": 1, "geneva": 1, "march": 1, "dear": 2, "elizabeth": 1, "i": 3, "exclaimed": 1, "when": 1, "had": 1, "read": 1, "jörg": 1, "letter": 1, "will": 1, "write": 1, "instantly": 1, "and": 1, "heart-sickeningly": 1, "roses": 1, "in": 1, "relieve": 1, "them": 1, "from": 1, "the": 1, "anxiety": 1, "they": 1, "must": 1, "feeling": 1},
    'counted_word_list':  [('i', 3), ('dear', 2), ('and', 1), ('anxiety', 1), ("can't", 1), ('elizabeth', 1), ('exclaimed', 1), ('feeling', 1), ('from', 1), ('geneva', 1), ('had', 1), ('heart-sickeningly', 1), ('in', 1), ('instantly', 1), ('jörg', 1), ('letter', 1), ('march', 1), ('must', 1), ('read', 1), ('relieve', 1), ('roses', 1), ('the', 1), ('them', 1), ('they', 1), ('when', 1), ('will', 1), ('write', 1)],
    'total_unique_words': 27,
    'total_words': 30,
}

def test_it_reads_the_word_file_except_for_the_gutenberg_text():
    text = wc.read_file(data['gutenberg_filename'])
    assert text == data['file_without_gutenberg_text']

def test_it_reads_the_entire_word_file_if_no_gutenberg_text():
    text = wc.read_file(data['no_gutenberg_filename'])
    assert text == data['file_without_gutenberg_text']

def test_it_creates_a_list_of_words():
    list = wc.initial_word_list(data['file_without_gutenberg_text'])
    assert list == data['initial_list']

@pytest.mark.parametrize('word, cleaned_word', [
    ('_I_', 'i'),
    ('"Geneva,', 'geneva'),
    ('Jörg', 'jörg'),
    ("can't", "can't"),
    ('(Dear)...', 'dear'),
    ('heart-sickeningly-?', 'heart-sickeningly'),
    ('\'singlequoted\'', 'singlequoted'),
    ('."', ''),
    ('"Commaword,', 'commaword'),
])
def test_it_cleans_a_word(word, cleaned_word):
    assert wc.clean_word(word) == cleaned_word

def test_it_removes_words_with_numbers():
    list = wc.remove_number_words(data['initial_list'])
    assert list ==  data['no_numbers_list']

def test_it_removes_punctuation_from_words():
    list = wc.remove_punctuation(data['no_numbers_list'])
    assert list == data['no_punctuation_list']

def test_it_removes_empty_strings_from_word_list():
    list = wc.remove_empty_strings(data['no_punctuation_list'])
    assert list == data['word_list']

def test_it_counts_the_words_and_stores_results_in_a_list():
    results = wc.count(data['word_list'])
    assert results == data['word_dict']

def test_it_orders_the_words_in_an_array_by_count_from_high_to_low():
    sorted_list = wc.sort_list(data['word_dict'])
    assert sorted_list == data['counted_word_list']
    assert len(sorted_list) == data['total_unique_words']

@pytest.mark.parametrize('user_input, validation', [
    ('-5', False),
    ('0', False),
    (str(data['total_unique_words']), True),
    (str(data['total_unique_words'] + 1), False),
    ('1aa', False),
    ('1.55', False)
])
def test_it_input_validation(user_input, validation):
    assert wc.is_valid(user_input, data['total_unique_words']) == validation

def test_it_calculates_bar_width_for_graphing():
    width = wc.bar_width(4194, 1033)
    assert width == 22
    assert type(width) is int

def test_it_calculates_total_words():
    total_words = wc.total_words(data['counted_word_list'])
    assert total_words == data['total_words']
