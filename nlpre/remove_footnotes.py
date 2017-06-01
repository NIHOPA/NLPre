from pyparsing import Word, WordEnd, WordStart, NoMatch, SkipTo, Combine
import pyparsing
import pattern.en
import os


__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class remove_footnotes_word:
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

        self.number_then_punctuation = WordStart() + real_word + nums + second_punctuation + pyparsing.ZeroOrMore(nums | second_punctuation) + WordEnd()
        self.punctuation_then_number = WordStart() + real_word + first_punctuation + nums + pyparsing.ZeroOrMore(second_punctuation | nums) + WordEnd()

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
                    pass

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
                    else:
                        new_sentence.append(parse_return[0])
                    continue
                except BaseException:
                    pass

                # Check if the word is of the form word.2,3,4
                try:
                    parse_return = \
                        self.number_then_punctuation.parseString(token)
                    new_sentence.append(parse_return[0])
                    continue
                except BaseException:
                    pass

                # Check if the word is of the form word2,3,4
                try:
                    parse_return = \
                        self.punctuation_then_number.parseString(token)
                    new_sentence.append(parse_return[0])
                    continue
                except BaseException:
                    pass

                # if not, append word to the new sentence
                new_sentence.append(token)

            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc


class remove_footnotes_punc:
    def __init__(self, reference_token=False):
        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

        self.reference_token = reference_token

        real_word = Word(pyparsing.alphas)
        first_punctuation = Word('.!?:,;')
        second_punctuation = Word('.!?:,;-')
        nums = Word(pyparsing.nums)
        letter = Word(pyparsing.alphas, exact=1)

        self.dash_word = WordStart() + real_word + Word('-') + nums + WordEnd()
        self.single_number = WordStart() + real_word + nums + WordEnd()

        self.number_then_punctuation = letter + nums + second_punctuation + pyparsing.ZeroOrMore(nums | second_punctuation) + WordEnd()
        self.punctuation_then_number = letter + first_punctuation + nums + pyparsing.ZeroOrMore(second_punctuation | nums) + WordEnd()

        self.parse = lambda x: pattern.en.tokenize(
            x)

    def __call__(self, doc):
        sentences = self.parse(doc)

        new_doc = []
        for sentence in sentences:
            new_sentence = []
            for token in sentence.split():
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
                    else:
                        word = parse_return[0]
                        reference = parse_return[1]

                        new_sentence.append(parse_return[0])

                        if self.reference_token:
                            new_sentence.append("REF_"+reference)
                    continue
                except BaseException:
                    pass

                # Check if the word is of the form word2,3,4

                parse_return = \
                        self.punctuation_then_number.searchString(token)
                if parse_return:
                    substring = ''.join(parse_return[0][1:])
                    index = token.find(substring)
                    word = token[:index]
                    reference = token[index:]
                    new_sentence.append(word)

                    if self.reference_token:
                        ref_token = "REF_" + reference
                        new_sentence.append(ref_token)
                    continue

                parse_return = \
                        self.number_then_punctuation.searchString(token)
                if parse_return:
                    substring = ''.join(parse_return[0][1:])
                    index = token.find(substring)
                    word = token[:index]
                    reference = token[index:]
                    new_sentence.append(word)

                    if self.reference_token:
                        new_sentence.append("REF_" + reference)
                    continue

                # if not, append word to the new sentence
                new_sentence.append(token)

            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc

if __name__ == '__main__':
    real_word = Word(pyparsing.alphas)
    first_punctuation = Word('.!?:,;')
    second_punctuation = Word('.!?:,;-')
    nums = Word(pyparsing.nums)

    dash_word = WordStart() + real_word + Word('-') + nums + WordEnd()
    single_number = WordStart() + real_word + nums + WordEnd()

    number_then_punctuation = nums + second_punctuation + pyparsing.ZeroOrMore(nums | second_punctuation) + WordEnd()
    punctuation_then_number = WordStart() + real_word + first_punctuation + nums + pyparsing.ZeroOrMore(
        second_punctuation | nums) + WordEnd()

    string_test = 'treatment4-5'
    x = number_then_punctuation.searchString(string_test)
    index = string_test.find(x)
    split = [string_test[:index], string_test[index:]]
    pass