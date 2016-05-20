from word_count import WordCounter

FRANKENSTEIN = './static/pg84.txt'

wc = WordCounter().read_in_file(FRANKENSTEIN, length=5)

print(wc)

F