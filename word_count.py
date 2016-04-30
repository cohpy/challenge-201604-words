# coding = utf-8
# author = cwandrews


# TODO Extract sanitization to separate function which processes and normalizes text from:
# text files
# strings
# urls *Maybe?

# TODO consider building into a class?


TARGET_STRING = 'This is my file.\nIt is alright I suppose.\nThis is really just a test.\nI hope it works'
# Target text to be read (Frankenstein)
TARGET_FILE = './pg83.txt'
TARGET_FILE2 = './pg84.txt'
TEST_TXT = './test.txt'
DOES_NOT_EXIST = './fake.txt'

# 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
ENGLISH_WORDS = './english_words.txt'


def read_in_file(filepath):
    from os.path import exists, isfile

    assert exists(filepath) and isfile(filepath)

    with open(filepath, 'rt') as infile:
        import re

        pre_post_re = re.compile("\n{10}")
        new_line_re = re.compile("[\n\r]")
        white_space_re = re.compile("\s+")
        special_chars_re = re.compile("[-\"\':;.?!,\(\)\d]+")

        read_text = infile.read()

        if ("GUTENBERG" in read_text) and pre_post_re.search(read_text):
            working_text = pre_post_re.split(read_text)[1]
        else:
            working_text = read_text

        if new_line_re.search(working_text):
            core_text = new_line_re.split(working_text)
            working_text = [w_line.strip() for w_line in core_text if w_line]
        else:
            working_text = list(working_text.strip())

        ews_processed_text = [white_space_re.sub(" ", w_line) for w_line in working_text]
        sck_processed_text = [special_chars_re.sub('', w_line) for w_line in ews_processed_text]
        processed_text = [w_line.lower() for w_line in sck_processed_text]

    assert isinstance(processed_text, list)
    for line in processed_text:
        yield line


def char_counter(processed_text, num_words=10):
    from types import GeneratorType
    from collections import Counter

    assert isinstance(processed_text, GeneratorType)

    with open(ENGLISH_WORDS, 'rt') as eng_dict:
        english_dict = list(set([eng_word.lower().rstrip('\n') for eng_word in eng_dict.readlines()]))

    master_word_count = Counter()

    for w_line in processed_text:
        master_word_count.update(Counter(w_line.split()))

    master_word_list = [word for word in master_word_count.most_common(num_words) if word[0] in english_dict]
    master_word_list.sort(key=lambda wc: wc[1], reverse=True)

    for word in master_word_list:
        wc_format = "'{0!s}' * {1!s}"
        print(wc_format.format(word[0], word[1]))


def main():

    text_gen = read_in_file(TARGET_FILE)
    char_counter(text_gen, 5)
    print('\n\n\n')
    text_gen2 = read_in_file(TARGET_FILE2)
    char_counter(text_gen2, 10)

if __name__ == "__main__":
    main()
