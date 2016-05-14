# coding = utf-8
# __author__ = cwandrews


class WordCounter:
    """
    Read text from string or text file, counts words, and returns sorted list of tuples with the n most common words
    and their respective counts.
    """

    from types import GeneratorType

    @staticmethod
    def _char_counter(sanitized_text_gen: GeneratorType, num_words: int=10):
        from collections import Counter
        from types import GeneratorType

        # 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
        english_words = './static/english_words.txt'

        assert isinstance(sanitized_text_gen, GeneratorType)

        with open(english_words, 'rt') as eng_dict:
            english_dict = list(set([eng_word.lower().rstrip('\n') for eng_word in eng_dict.readlines()]))

        master_word_count = Counter()

        for w_line in sanitized_text_gen:
            master_word_count.update(Counter(w_line.split()))

        if not num_words:
            master_word_list = [word for word in master_word_count.items() if word[0] in english_dict]
            master_word_list.sort(key=lambda wc: wc[1], reverse=True)
            return master_word_list
        else:
            master_word_list = []
            most_common_gen = (word for word in master_word_count.most_common() if word[0] in english_dict)
            while len(master_word_list) < num_words:
                master_word_list.append(next(most_common_gen))
            master_word_list.sort(key=lambda counter_obj: counter_obj[1], reverse=True)
            return master_word_list[:num_words]

    @staticmethod
    def __sanitize(string_list: list):
        """
        Performs additional processing (sanitzation) of text. Will strip white space from start and end of string,
        remove special characters, downcase all letters, replace any white space w/single space. Private method
        utilized by class methods.
        """

        import re

        assert isinstance(string_list, list)

        white_space_re = re.compile("\s+")
        special_chars_re = re.compile("[-\"\':;.?!,\(\)\d]+")

        trimmed_text = [w_line.strip() for w_line in string_list if w_line]
        extra_ws_processed_text = [white_space_re.sub(' ', w_line) for w_line in trimmed_text]
        spec_char_killer_processed_text = [special_chars_re.sub('', w_line) for w_line in extra_ws_processed_text]
        sanitized_text = [w_line.lower() for w_line in spec_char_killer_processed_text]

        assert isinstance(sanitized_text, list)
        for sanitized_line in sanitized_text:
            yield sanitized_line

    def read_in_string(self, string: str, length: int):
        """
        return a sorted list of the #length# most common words and their counts in a tuple.
        """

        import re

        assert isinstance(string, str)

        new_line_re = re.compile("[\n\r]")

        if new_line_re.search(string):
            chunked_text = new_line_re.split(string)
        else:
            chunked_text = [string]

        assert isinstance(chunked_text, list)
        return self._char_counter(self.__sanitize(chunked_text), length)

    def read_in_file(self, filepath: str, length: int):
        """
        return sorted list of the #length# most common words and their counts in a tuple.
        """

        from os.path import exists, isfile

        assert exists(filepath) and isfile(filepath)

        with open(filepath, 'rt') as infile:
            import re

            gberg_split_re = re.compile("\n{10}")
            new_line_re = re.compile("[\n\r]")

            read_text = infile.read()

            if ("GUTENBERG" in read_text) and gberg_split_re.search(read_text):
                working_text = gberg_split_re.split(read_text)[1]
            else:
                working_text = read_text

            if new_line_re.search(working_text):
                chunked_text = new_line_re.split(working_text)
            else:
                chunked_text = [working_text]

        assert isinstance(chunked_text, list)
        return self._char_counter(self.__sanitize(chunked_text), length)


class LetterCounter(WordCounter):
    """
    Letter counter object which counts letters instead of words like it's parent class wherein the only difference is
    the _char_counter method which has been overidden.
    """

    from types import GeneratorType

    @staticmethod
    def _char_counter(sanitized_text_gen: GeneratorType, num_letters: int=10):
        from collections import Counter
        from types import GeneratorType
        import re

        assert isinstance(sanitized_text_gen, GeneratorType)

        english_letters = re.compile("[a-z]")

        master_letter_count = Counter()

        for w_line in sanitized_text_gen:
            ns_w_line = list(''.join(w_line))
            master_letter_count.update(Counter(ns_w_line))

        if not num_letters:
            master_letter_list = [letter for letter in master_letter_count.items() if english_letters.match(letter[0])]
            master_letter_list.sort(key=lambda lc: lc[1], reverse=True)
            return master_letter_list
        else:
            master_letter_list = list()
            common_letters_gen = (letter for letter in master_letter_count.most_common() if english_letters.match(
                letter[0]))
            while len(master_letter_list) < num_letters:
                master_letter_list.append(next(common_letters_gen))
            master_letter_list.sort(key=lambda counter_obj: counter_obj[1], reverse=True)
            return master_letter_list[:num_letters]