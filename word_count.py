import re
from collections import Counter
from pprint import pprint


infile = 'C:/Users/chris.andrews/Documents/Other Documents/3918_USFreedomFinancing_SC_SetupQuery.sql'

with open(infile, 'rt') as fh:
    text = fh.read()
    lc_text = text.lower()

word_reg = re.compile("[a-zA-Z]+'?")
matches = word_reg.findall(lc_text)
counts = Counter(matches)
word_list = list(counts.items())
word_list.sort(key=lambda wc: wc[1], reverse=True)
pprint(word_list[:10])