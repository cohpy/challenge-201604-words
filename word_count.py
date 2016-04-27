import re
from collections import Counter
from pprint import pprint


from nltk.corpus import wordnet


infile = '/Users/cwandrews/Downloads/pg84.txt'

with open(infile, 'rt') as fh:
    text = fh.read()
    lc_text = text.lower()

word_reg = re.compile("[a-zA-Z]+'?")
potential_matches = word_reg.findall(lc_text)

potential_match_count = Counter(potential_matches)

word_list = list(potential_match_count.items())
word_list.sort(key=lambda wc: wc[1], reverse=True)

verified_words = [word for word in word_list if wordnet.synsets(word[0])]

print(wordnet.synsets('i'))

word_gen = (word for word in verified_words)

for word in word_gen:
    wc_format = "'{0!s}' * {1!s}"
    print(wc_format.format(word[0], word[1]))
