# Word Count Exercise

###From COhPy Meetup

This program will count and sort the unique words in a Gutenberg book (high to low) and display them in a graph on the command line.

The Gutenberg text at the top and bottom and words that contain numbers are excluded. Hyphenated words and contractions remain as written and all text is converted to lowercase. Punctuation and special characters are removed.

#### Create virtual environment in Python 3 and install requirements.

Run from the command line and give input when prompted:

```
$ python word_count.py frankenstein.txt
```
or
```
$ python word_count.py from_the_earth_to_the_moon.txt
```
or
```
python word_count.py sekunde_durch_hirn.txt
```

To run the tests:

```py.test -vv
```
