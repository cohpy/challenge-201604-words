import re
import pytest
import sys


def read_file(filename):
    text = ""
    with open(filename, 'r') as file:
        for line in file:
            text += line
            if 'START OF THIS PROJECT GUTENBERG' in line:
                text = ""
                break
        for line in file:
            if 'Gutenberg' in line and 'End of' in line:
                break
            text += line
    return text 

def initial_word_list(text):
    return text.replace("-\n", "").replace("--", " ").split()

def remove_number_words(word_list):
    return [word for word in word_list if not bool(re.search(r'\d', word))]

def clean_word(word):
    word = word.replace('_', '')
    p = re.compile(r'[^-\w\']', re.UNICODE)
    word = p.sub('', word).strip("'").strip("-").lower()
    return word

def remove_punctuation(word_list):
    return [clean_word(word) for word in word_list]

def remove_empty_strings(word_list):
    return [word for word in word_list if word != ""]

def count(word_list):
    word_dict = {}
    for word in word_list:
        if word_dict.get(word, None):
            word_dict[word] += 1 
        else:
            word_dict[word] = 1
    return word_dict

def sort_list(word_dict):
    alphabetical_list = sorted(word_dict.items(), key = lambda item: item[0])
    return sorted(alphabetical_list, key = lambda item: item[1], reverse = True)

def is_valid(input, total_unique_words):
    if bool(re.search(r'\D', input)):
        return False 
    if 0 < int(input) <= total_unique_words:
        return True
    return False

def bar_width(most_occurrences, occurrences):
    return round(89.0 * occurrences/most_occurrences)

def total_words(sorted_list):
    sum = 0
    for item in sorted_list:
        sum += item[1]
    return sum

def num_words_input(word_total):
    num_words = input("How many of them would you like to display? ")
    if is_valid(num_words, word_total):
        return num_words
    else:
        print("\nPlease input an integer between 1 and #{word_total}.")
        num_words_input(word_total)

def print_results(sorted_list, filename):
    word_total = total_words(sorted_list)
    total_unique_words = len(sorted_list)
    most_occurrences = sorted_list[0][1]
    print('\n\n' + '*-'*50 + '*\n' + '-*'*50 + '-\n\n')
    print("There are {:,} unique words out of {:,} total words in file {}.".format(total_unique_words, word_total, filename))
    num_words = int(num_words_input(total_unique_words))
    selected_words = sorted_list[:num_words]
    print("\nShowing the top {:,} out of {:,} unique words. Excludes Gutenberg text at top and bottom and words that\ncontain numbers. Hyphenated words and contractions remain as written and all text is converted to\nlowercase. Punctuation and special characters are removed.\n\n".format(num_words, total_unique_words))
    for word in selected_words:
        width = bar_width(most_occurrences, word[1])
        print("="*width + " {} ({:,})".format(word[0], word[1]))
    print('\n\n' + '*-'*50 + '*\n' + '-*'*50 + '-\n\n')


if __name__ == '__main__':
    filename = sys.argv[1]
    gutenberg_free_text = read_file(filename)
    initial_word_list = initial_word_list(gutenberg_free_text)
    no_numbers_list = remove_number_words(initial_word_list)
    no_punctuation_list = remove_punctuation(no_numbers_list)
    word_list = remove_empty_strings(no_punctuation_list)
    word_dict = count(word_list)
    sorted_list = sort_list(word_dict)
    print_results(sorted_list, filename)
