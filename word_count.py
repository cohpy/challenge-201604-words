import re
from collections import Counter
from io import StringIO


TARGET_STRING = StringIO('This is my file.\nIt is alright I suppose.\nThis is really just a test.\nI hope it works')
# Target text to be read (Frankenstein)
TARGET_FILE = './pg83.txt'
# 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
ENGLISH_WORDS = './english_words.txt'


def main(infile=TARGET_FILE, num_words=50):

    with open(infile, 'rt') as fh, open(ENGLISH_WORDS, 'rt') as ed:
        # Read the target text into a string translating all letters to lowercase

        pre_post_text = re.compile("\n{10}")
        blank_line_regex = re.compile("^\n$")
        white_space_regex = re.compile("\s+")
        special_chars_regex = re.compile("[-\"\':;.?!,\(\)\d]+")

        fh = pre_post_text.split(fh.read())[1]

        english_dict = sorted(list(set([eng_word.lower().rstrip('\n') for eng_word in ed.readlines()])))
        word_count = Counter()

        for line in enumerate(line.strip() for line in fh.split('\n') if not blank_line_regex.match(line)):
            dcase_line = line[1].lower()
            dcase_line = special_chars_regex.sub('', dcase_line)

            word_count.update(Counter(white_space_regex.split(dcase_line)))

    # Create a list from counter object
    word_list = [word for word in word_count.most_common(num_words) if word[0] in english_dict]

    # Sort list by word count in descending order
    word_list.sort(key=lambda wc: wc[1], reverse=True)

    # Use genexp to print a formatted string of a word and the number of occurrences of said word in the text
    for word in word_list:
        wc_format = "'{0!s}' * {1!s}"
        print(wc_format.format(word[0], word[1]))

if __name__ == '__main__':
    main()
