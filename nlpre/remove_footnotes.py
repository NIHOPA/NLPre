from pyparsing import Word, WordEnd, WordStart
import pyparsing
import pattern.en
import os


__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class remove_footnotes:
    def __init__(self):
        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

        real_word = Word(pyparsing.alphas)
        first_punctuation = Word('.!?:,;')
        second_punctuation = Word('.!?:,;-')
        nums = Word(pyparsing.nums)

        self.dash_word = WordStart() + real_word + Word('-') + nums + WordEnd()
        self.single_number = WordStart() + real_word + nums + WordEnd()

        self.number_then_punctuation = WordStart() + real_word + \
            pyparsing.OneOrMore(nums | second_punctuation) + WordEnd()
        self.punctuation_then_number = WordStart() + real_word + \
            pyparsing.OneOrMore(first_punctuation | nums) + WordEnd()

        self.parse = lambda x: pattern.en.tokenize(
            x)

    def __call__(self, doc):
        sentences = self.parse(doc)

        new_doc = []
        for sentence in sentences:
            new_sentence = []
            for token in sentence.split():
                # Check if a word is of the form word-4, which does not
                # indicate a footnote
                try:
                    self.dash_word.parseString(token)
                    new_sentence.append(token)
                    continue
                except BaseException:
                    # Check if word is of the form word4. This is an ambiguous
                    # case, because there could be words that end in a number
                    # that don't represent a footnote, as is the case for
                    # chemicals. The code looks up the characters that make
                    # up a word, and if they are not found in the dictionary,
                    # it is assumed it is a chemical name and the number is
                    # not pruned.
                    try:
                        parse_return = self.single_number.parseString(token)
                        if parse_return[0] not in self.english_words:
                            new_sentence.append(token)
                            continue
                    except BaseException:
                        # Check if the word is of the form word.2,3,4
                        try:
                            parse_return = \
                                self.number_then_punctuation.parseString(
                                token)
                        except BaseException:
                            # Check if the word is of the form word2,3,4
                            try:
                                parse_return = \
                                    self.punctuation_then_number.parseString(
                                    token)
                            # if not, append word to the new sentence
                            except BaseException:
                                new_sentence.append(token)
                                continue
                new_sentence.append(parse_return[0])
            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc
