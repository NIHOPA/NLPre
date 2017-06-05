from pyparsing import Word, WordEnd, WordStart
import pyparsing
import pattern.en
import os

__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class seperate_reference:
    def __init__(self, reference_token=False):
        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

        self.reference_token = reference_token

        real_word = Word(pyparsing.alphas)
        first_punctuation = Word('.!?:,;')
        second_punctuation = Word('.!?:,;-')
        space = Word(' ')
        nums = Word(pyparsing.nums)

        nest = pyparsing.nestedExpr
        nestedParens = nest('(', ')')
        nestedBrackets = nest('[', ']')
        nestedCurlies = nest('{', '}')
        nest_grammar = nestedParens | nestedBrackets | nestedCurlies

        letter = Word(pyparsing.alphas, exact=1)

        self.dash_word = WordStart() + real_word + Word('-') + nums + WordEnd()

        self.single_number = WordStart() + real_word + nums + WordEnd()

        self.single_number_parens = WordStart() + real_word + \
            pyparsing.OneOrMore(nums | nest_grammar | space) \
            + WordEnd()

        self.number_then_punctuation = letter + nums + second_punctuation + \
            pyparsing.ZeroOrMore(nums | second_punctuation) + WordEnd()
        self.punctuation_then_number = letter + first_punctuation + nums + \
            pyparsing.ZeroOrMore(second_punctuation | nums) + WordEnd()

    def __call__(self, doc):
        sentences = pattern.en.tokenize(
            doc, punctuation=".,;:!?`''\"@#$^&*+-|=~_")

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

                        new_sentence.append(word)

                        if self.reference_token:
                            new_sentence.append("REF_" + reference)
                    continue
                except BaseException:
                    pass

                # check if word is of the form word(4)
                try:
                    parse_return = self.single_number_parens.parseString(token)
                    word = parse_return[0]
                    reference = parse_return[1][0]

                    new_sentence.append(word)

                    if self.reference_token:
                        new_sentence.append("REF_" + reference)
                    continue
                except BaseException:
                    pass

                # Check if the word is of the form word.2,3,4

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

                    if substring[0] == '.':
                        join_sentence = ' '.join(new_sentence) + ' .'
                        new_doc.append(join_sentence)
                        new_sentence = []
                    continue

                # Check if the word is of the form word2,3,4

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
