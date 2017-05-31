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
        #first_punctuation = '.!?:;'
        second_punctuation = Word('.!?:,;-')
        nums = Word(pyparsing.nums)

        #first_case = real_word + first_punctuation + nums + second_punctuation
        self.escape_case = real_word + '-' + nums
        self.basic_case = real_word + nums
        #self.first_case = pyparsing.OneOrMore(real_word | first_punctuation | nums | second_punctuation)
        #self.second_case = pyparsing.OneOrMore(real_word | nums | second_punctuation)
        #self.foot_case = pyparsing.OneOrMore(real_word | nums | second_punctuation)
        #self.foot_case = real_word + pyparsing.OneOrMore(
        #    nums | second_punctuation)
        self.foot_case = real_word + second_punctuation + nums


        self.parse = lambda x: pattern.en.tokenize(
            x)

    def __call__(self, doc):
        sentences = self.parse(doc)

        new_doc = []
        for sentence in sentences:
            new_sentence = []
            for token in sentence.split():
                try:
                    x = self.escape_case.parseString(token)
                    new_sentence.append(token)
                    continue
                except:
                    try:
                        x = self.basic_case.parseString(token)
                        if x[0] not in self.english_words:
                            new_sentence.append(token)
                            continue
                    except:
                        try:
                            x = self.foot_case.parseString(token)
                            print
                        except:
                            new_sentence.append(token)
                            continue
                new_sentence.append(x[0])
            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc


