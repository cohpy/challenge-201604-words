# coding = utf-8
# __author__ = cwandrews


class WordCounter:
    """
    Read text from string or text file, counts words, and returns sorted list of tuples with the n most common words
    and their respective counts.
    """

    from types import GeneratorType

    @staticmethod
    def _char_counter(genexp_text_sanitized: GeneratorType, length: int):
        """
        Iterate through genexp provided by one of the read_in methods, counting all words passed and cross-checking
        results against the UNIX words file/dictionary and adding those that are to the output list until the list
        length meets passed length param or all English words if length=None. The list of valid English words is
        sorted in descending order before being returned.
        """

        from collections import Counter
        from types import GeneratorType

        # 230k+ words from the standard UNIX dict in a local text file ('/usr/share/dict/words')
        file_words_eng = './static/english_words.txt'

        assert isinstance(genexp_text_sanitized, GeneratorType)

        with open(file_words_eng, 'rt') as file_words_eng:
            dict_words_english = list(set([eng_word.lower().rstrip('\n') for eng_word in file_words_eng.readlines()]))

        count_words_master = Counter()

        for line_working in genexp_text_sanitized:
            count_words_master.update(Counter(line_working.split()))

        list_words_master = list()
        genexp_words_common_most = (word for word in count_words_master.most_common() if word[0] in dict_words_english)

        if length:
            while len(list_words_master) < length:
                try:
                    list_words_master.append(next(genexp_words_common_most))
                except StopIteration:
                    break
        else:
            for word in genexp_words_common_most:
                list_words_master.append(word)

        assert isinstance(list_words_master, list)
        list_words_master.sort(key=lambda counter_obj: counter_obj[1], reverse=True)
        return list_words_master

    @staticmethod
    def _sanitize(list_strings: (list, tuple)):
        """
        Performs additional processing (sanitization) of text. Will strip white space from start and end of string,
        remove special characters, downcase all letters, replace any white space w/single space. Private method
        utilized by class methods.
        """

        from types import GeneratorType
        import re

        assert isinstance(list_strings, (list, tuple))

        white_space_re = re.compile("\s+")
        special_chars_re = re.compile("[-\"\'|:;.?!,\(\)\d]+")

        text_trimmed = (line_working.strip() for line_working in list_strings if line_working)
        text_no_extra_ws = (white_space_re.sub(' ', line_working) for line_working in text_trimmed)
        text_no_spec_chars = (special_chars_re.sub('', line_working) for line_working in text_no_extra_ws)
        text_sanitized = (line_working.lower() for line_working in text_no_spec_chars)

        assert isinstance(text_sanitized, GeneratorType)
        for line_sanitized in text_sanitized:
            yield line_sanitized

    def read_in_file(self, filepath: str, length: int = 10):
        """
        return sorted list of the #length# most common words and their counts in a tuple.
        """

        from os.path import exists, isfile

        assert exists(filepath) and isfile(filepath)

        with open(filepath, 'rt') as infile:
            import re

            gberg_split_re = re.compile("\n{10}")
            neline_working_re = re.compile("[\n\r]")

            read_text = infile.read()

            if ("GUTENBERG" in read_text) and gberg_split_re.search(read_text):
                working_text = gberg_split_re.split(read_text)[1]
            else:
                working_text = read_text

            if neline_working_re.search(working_text):
                chunked_text = neline_working_re.split(working_text)
            else:
                chunked_text = [working_text]

        assert isinstance(chunked_text, list)
        return self._char_counter(self._sanitize(chunked_text), length)

    def read_in_string(self, string: str, length: int=10):
        """
        return a sorted list of the #length# most common words and their counts in a tuple.
        """

        import re

        assert isinstance(string, str)

        neline_working_re = re.compile("[\n\r]")

        if neline_working_re.search(string):
            chunked_text = neline_working_re.split(string)
        else:
            chunked_text = list(string)

        assert isinstance(chunked_text, list)
        return self._char_counter(self._sanitize(chunked_text), length)


class LetterCounter(WordCounter):
    """
    Letter counter object which counts letters instead of words like it's parent class wherein the only difference is
    the _char_counter method which has been overidden.
    """

    from types import GeneratorType

    @staticmethod
    def _char_counter(genexp_text_sanitized: GeneratorType, length: int):
        """
        Overridden method from parent class, WordCounter, which counts letters instead of words.
        """

        from collections import Counter
        from types import GeneratorType
        import re

        assert isinstance(genexp_text_sanitized, GeneratorType)

        english_ltrs = re.compile("[a-z]")

        master_ltr_count = Counter()

        for line_working in genexp_text_sanitized:
            ns_line_working = list(''.join(line_working))
            master_ltr_count.update(Counter(ns_line_working))

        master_ltr_list = list()
        common_ltrs_gen = (ltr for ltr in master_ltr_count.most_common() if english_ltrs.match(ltr[0]))

        if length:
            while len(master_ltr_list) < length:
                try:
                    master_ltr_list.append(next(common_ltrs_gen))
                except StopIteration:
                    break
        else:
            for ltr in common_ltrs_gen:
                master_ltr_list.append(ltr)

        master_ltr_list.sort(key=lambda counter_obj: counter_obj[1], reverse=True)
        assert isinstance(master_ltr_list, list)
        return master_ltr_list
