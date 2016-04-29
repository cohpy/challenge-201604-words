import re
from collections import Counter


# Target text to be read (Frankenstein)
INFILE = './pg84.txt'
# 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
ENGLISH_WORDS = './english_words.txt'


def main():

    with open(INFILE, 'rt') as fh, open(ENGLISH_WORDS, 'rt') as ed:
        # Read the target text into a string translating all letters to lowercase
        english_dict = sorted(list(set([eng_word.lower().rstrip('\n') for eng_word in ed.readlines()])))
        word_count = Counter()

        for line in fh:
            dcase_line = line.lower()
            

    '''
        # List comprehension which strips new lines from words, gets rid of duplicates (with set), and resorts them
        # alphabetically (for the sake of order)


    # Compile word regex to use for finding word-like structures
    word_regex = re.compile("[a-z]+\'?[a-z]+")

    # Find all matches of/for compiled regex
    potential_matches = word_regex.findall(downcase_text)

    # Reduce match list to any given match in the file and the number of instances determined
    potential_match_count = Counter(potential_matches)

    # Create a list from counter object
    word_list = list(potential_match_count.items())
    # Sort list by word count in descending order
    word_list.sort(key=lambda wc: wc[1], reverse=True)

    # Check words against extensive list of English words, disregarding those not in the list
    verified_words = [word for word in word_list if word[0] in english_dict]

    # Create a generator expression from list of verified words because I can
    word_gen = (word for word in verified_words)

    # Use genexp to print a formatted string of a word and the number of occurrences of said word in the text
    for word in word_gen:
        wc_format = "'{0!s}' * {1!s}"
        print(wc_format.format(word[0], word[1]))
    '''

if __name__ == '__main__':
    main()
