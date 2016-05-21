from word_count import WordCounter, frequency_plot

FRANKENSTEIN = './static/pg84.txt'

frequency_plot(WordCounter().read_in_file(FRANKENSTEIN, length=5))
