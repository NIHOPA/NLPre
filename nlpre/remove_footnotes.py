from pyparsing import *
import pyparsing
import pattern.en



class Remove_Footnotes:
    def __init__(self):
        real_word = Word(pyparsing.alphas)
        first_punctuation = '.!?:;'
        second_punctuation = '.!?:;-'
        nums = Word(pyparsing.nums)

        #first_case = real_word + first_punctuation + nums + second_punctuation
        self.escape_case = real_word + '-' + nums
        self.basic_case = real_word + nums
        self.first_case = pyparsing.OneOrMore(real_word | first_punctuation | nums | second_punctuation)
        self.second_case = pyparsing.OneOrMore(real_word | nums | second_punctuation)


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
                        print
                    except:
                        try:
                            x = self.first_case.parseString(token)
                        except:
                            try:
                                x = self.second_case.parseString(token)
                            except:
                                new_sentence.append(token)
                                continue
                new_sentence.append(x[0])
            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc


