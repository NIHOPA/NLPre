from pyparsing import *
import pyparsing
import pattern.en
import os

__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class Remove_Footnotes:
    def __init__(self):
        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())


        real_word = Word(pyparsing.alphas)
        first_punctuation = Word('.!?:,;')
        second_punctuation = Word('.!?:,;-')
        nums = Word(pyparsing.nums)


        self.dash_word = real_word + Word('-') + nums + WordEnd()
        self.single_number = real_word + nums + WordEnd()

        self.number_then_punctuation = real_word + pyparsing.OneOrMore(nums | second_punctuation) + WordEnd()
        self.punctuation_then_number = real_word + pyparsing.OneOrMore(first_punctuation | nums) + WordEnd()

        self.parse = lambda x: pattern.en.tokenize(
            x)

    def __call__(self, doc):
        sentences = self.parse(doc)

        new_doc = []
        for sentence in sentences:
            new_sentence = []
            for token in sentence.split():
                try:
                    x = self.dash_word.parseString(token)
                    new_sentence.append(token)
                    continue
                except:
                    try:
                        x = self.single_number.parseString(token)
                        if x[0] not in self.english_words:
                            new_sentence.append(token)
                            continue
                    except:
                        try:
                            x = self.number_then_punctuation.parseString(token)
                            print
                        except:
                            try:
                                x = self.punctuation_then_number.parseString(token)
                                print
                            except:
                                new_sentence.append(token)
                                continue
                new_sentence.append(x[0])
            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc


