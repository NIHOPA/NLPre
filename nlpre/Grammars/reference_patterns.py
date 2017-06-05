import pyparsing
from pyparsing import Word, WordStart, WordEnd


class reference_patterns:
    def __init__(self):
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
