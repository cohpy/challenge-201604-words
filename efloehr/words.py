from __future__ import print_function
import os
import sys
import math
import codecs
import textwrap
from collections import Counter


def return_text_from_file(filename):
    with codecs.open(filename, encoding='utf-8') as f:
        return return_text(f)


def return_text(iterable_of_lines):
    text = ""
    
    for line in iterable_of_lines:
        text += cleaned_line(line)
        if 'START OF THIS PROJECT GUTENBERG' in line:
            text = ""
            break

    for line in iterable_of_lines:
       if 'Gutenberg' in line and 'End of' in line:
           break
       text += cleaned_line(line)

    return text


def return_words(text):
    return [cleaned_word(word) for word in text.split()]


def return_word_counts(words):
    return Counter(words)


def cleaned_line(line):
    line = line.replace('--',' ').strip()
    if len(line) and line[-1] == '-':
        line = line[:-1]
    else:
        line += ' '
    return ''.join([c for c in line if c.isalpha() or c.isnumeric() or c.isspace() or c in "'-"])


def cleaned_word(word):
    return word.strip("'").strip("-").strip("'").lower()


def return_barchart(word, count, x_axis_max_value, x_axis_max_chars=85, char_to_use=u'\u2588'):
    bar_length = int(math.ceil((float(count) / x_axis_max_value) * x_axis_max_chars))
    return u'{bar} {word} ({count:,})'.format(bar=char_to_use * bar_length, word=word, count=count)


def return_filename_and_words_to_show_from_args(args):
    filename = None
    num_words_to_show = -1

    if len(args) > 1:
        filename = args[1]

    if len(args) > 2:
        words_to_show_param = args[2]
        if not words_to_show_param.isdigit():
            num_words_to_show = None
        else:
            num_words_to_show = int(args[2])

    return filename, num_words_to_show


def print_summary(filename, word_counts, num_words, num_words_to_show, num_unique_words, terminal_width=None):
    if terminal_width is None:
        terminal_size = os.get_terminal_size()
        if terminal_size:
            terminal_width = terminal_size.columns - 2
            if terminal_width < 1:
                terminal_width = 1

    half_terminal_width = int(terminal_width / 2.0)

    border = '\n' + '/\\'*half_terminal_width + '\n' + '\\/'*half_terminal_width + '\n'
    
    print(border)
    
    print('There are {wc:,} words in file "{fn}".\n'.format(wc=num_words, fn=filename))
    print(
        textwrap.fill('Showing the top {top:,} out of {wc:,} unique words. Excludes Gutenberg text at top and bottom. '.format(top=num_words_to_show, wc=num_unique_words) + \
                      'Hyphenated words and contractions remain as written and all text is converted to lowercase. ' + \
                      'Punctuation and special characters are removed.', terminal_width), '\n')
    
    for word, count in word_counts.most_common(num_words_to_show):
        print(return_barchart(word, count, most_common_word_count, x_axis_max_chars=terminal_width-15, char_to_use='*'))
    
    print(border)
    

if __name__ == '__main__':
    filename, num_words_to_show = return_filename_and_words_to_show_from_args(sys.argv)

    if filename == None:
        print("\nPlease enter a filename of a Gutenberg text to count words.\n")
        exit(1)

    if num_words_to_show == None:
        print("\nPlease enter a positive integer for the number of the most common words to show, or leave empty to show all.\n")
        exit(1)
 
    text = return_text_from_file(filename)
    words = return_words(text)
    word_counts = return_word_counts(words)

    num_words = len(words)
    num_unique_words = len(word_counts)
    most_common_word_count = word_counts.most_common(1)[0][1]

    if num_words_to_show < 0:
        num_words_to_show = num_unique_words

    print_summary(filename, word_counts, num_words, num_words_to_show, num_unique_words)

