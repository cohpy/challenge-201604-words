import pytest
import words

@pytest.mark.parametrize("word, cleaned_word", [
    ("Hello","hello"),
    ("Wonderful!","wonderful!"),
    ("i-am-legend-","i-am-legend"),
    ("Can't","can't"),
    ("'won't'","won't"),
    ("Überbald","überbald"),
    ("'Scallywag-'","scallywag"),
    ("'hedgeHog'-","hedgehog"),
#    ("",""),
])
def test_cleaned_word(word, cleaned_word):
    assert words.cleaned_word(word) == cleaned_word

@pytest.mark.parametrize("line, cleaned_line", [
    ("perpetual splendour.  There--for with your leave, my sister, I will put   ",
     "perpetual splendour  There for with your leave my sister I will put "),
    ("under-mate in a Greenland whaler, and acquitted myself to admiration. I\n",
     "under-mate in a Greenland whaler and acquitted myself to admiration I "),
    ("  R. Walton",
     "R Walton "),
    ("to her inclinations.  \"What a noble fellow!\" you will exclaim.  He is",
     "to her inclinations  What a noble fellow you will exclaim  He is "),
    ("But success SHALL crown my endeavours.  Wherefore not?  Thus far I have-",
     "But success SHALL crown my endeavours  Wherefore not  Thus far I have"),
    ("Last Monday (July 31st) we were nearly surrounded by ice, which closed-  ",
     "Last Monday July 31st we were nearly surrounded by ice which closed"),
    ("\"I thank you,\" he replied, \"for your sympathy, but it is useless; my\n",
     "I thank you he replied for your sympathy but it is useless my "),
    ("_Ein unheimlich schnell rotierender Roman_",
    "Ein unheimlich schnell rotierender Roman "),
    ("Traum, erhaben toll und toll erhaben, ganz närrisch: Fastnachtsspiel. Bei\n",
     "Traum erhaben toll und toll erhaben ganz närrisch Fastnachtsspiel Bei "),
    ("                                * * *\n",
     "   "),
    (""," "),
#    ("",""),
])
def test_cleaned_line(line, cleaned_line):
    assert words.cleaned_line(line) == cleaned_line

@pytest.mark.parametrize("args, filename, num_words_to_show", [
    ([],None,-1),
    (['words.py'],None,-1),
    (['words.py','pg84.txt','10~~'],'pg84.txt',None),
    (['','/tmp/pg38542.txt','25'],'/tmp/pg38542.txt',25),
    (['x','hello'],'hello',-1),
#    (,,),
])
def test_return_filename_and_words_to_show_from_args(args, filename, num_words_to_show):
    returned_filename, returned_num_words_to_show = words.return_filename_and_words_to_show_from_args(args)
    assert returned_filename == filename
    assert returned_num_words_to_show == num_words_to_show

@pytest.mark.parametrize("word_array, counts", [
     (['a','and','the','a','a','the','wizard','x','a'],
      (('a',4),('and',1),('the',2),('wizard',1),('x',1),('ruby',0))),
])
def test_return_word_counts(word_array, counts):
    word_count = words.return_word_counts(word_array)
    for word, count in counts:
        returned_count = word_count[word]
        assert returned_count == count, "Expected a count of {} for '{}' but got {}.".format(count, word, returned_count)

@pytest.mark.parametrize("text, word_array", [
    ("Last Monday (July 31st) we were nearly surrounded by ice, which closed",
     ["last","monday","july","31st","we","were","nearly","surrounded","by","ice","which","closed"]),
    ("foreign accent.  \"Before I come on board your vessel,\" said he, \"will\n\
      you have the kind-\n  ness to inform me whither you are bound?\"",
     ["foreign","accent","before","i","come","on","board","your","vessel","said","he","will","you","have","the","kindness",
      "to","inform","me","whither","you","are","bound"]),
])
def test_return_words(text, word_array):
    return words.return_words(text) == word_array
