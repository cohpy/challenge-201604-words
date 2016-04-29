import re
from collections import Counter


# TODO Trim pre and post book information (Gutenberg project information for example) from text to be analyzed

# Target text to be read (Frankenstein)
INFILE = './pg84.txt'
# 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
ENGLISH_WORDS = './english_words.txt'


def main():

    with open(INFILE, 'rt') as fh, open(ENGLISH_WORDS, 'rt') as ed:
        # Read the target text into a string translating all letters to lowercase

        blank_line_regex = re.compile("^\n$")
        # word_regex = re.compile("[a-z]+\'?[a-z]+")
        white_space_regex = re.compile("\s+")
        special_chars_regex = re.compile("[-\"\':;.?!,\(\)\d]+")

        # english_dict = sorted(list(set([eng_word.lower().rstrip('\n') for eng_word in ed.readlines()])))
        word_count = Counter()

        for line in enumerate(line.rstrip('\n').strip() for line in fh.readlines() if not blank_line_regex.match(line)):
            dcase_line = line[1].lower()
            dcase_line = special_chars_regex.sub('', dcase_line)

            line_matches = white_space_regex.split(dcase_line)

            word_count.update(Counter(line_matches))

    # Create a list from counter object
    word_list = list(word_count.items())
    # Sort list by word count in descending order
    word_list.sort(key=lambda wc: wc[1], reverse=True)

    # Check words against extensive list of English words, disregarding those not in the list
    # verified_words = [word for word in word_list if word[0] in english_dict]

    # Create a generator expression from list of verified words because I can
    word_gen = (word for word in word_list)

    # Use genexp to print a formatted string of a word and the number of occurrences of said word in the text
    for word in word_gen:
        wc_format = "'{0!s}' * {1!s}"
        print(wc_format.format(word[0], word[1]))

    word_list[:10]

if __name__ == '__main__':
    main()
