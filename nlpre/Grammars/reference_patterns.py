import pyparsing
from pyparsing import Word, WordStart, WordEnd, ZeroOrMore, Optional


class reference_patterns:
    def __init__(self):
        # real_word = Word(pyparsing.alphas)
        real_word_dashes = Word(pyparsing.alphas + '-')
        punctuation = Word('.!?:,;-')
        punctuation_no_dash = Word('.!?:,;')
        punctuation_reference_letter = Word('.:,;-')

        space = Word(' ')
        letter = Word(pyparsing.alphas, exact=1)
        letter_reference = punctuation_reference_letter + letter

        nums = Word(pyparsing.nums) + Optional(letter) + \
            ZeroOrMore(letter_reference)

        nest = pyparsing.nestedExpr
        nestedParens = nest('(', ')')
        nestedBrackets = nest('[', ']')
        nestedCurlies = nest('{', '}')
        nest_grammar = nestedParens | nestedBrackets | nestedCurlies

        word_end = pyparsing.ZeroOrMore(Word(')') | Word('}') | Word(']')) + \
            WordEnd()

        # self.dash_word = WordStart() + real_word + Word('-') + \
        #     Word(pyparsing.nums) + WordEnd()

        self.single_number = (
            WordStart() +
            real_word_dashes +
            nums +
            word_end
        )

        self.single_number_parens = (
            WordStart() +
            real_word_dashes +
            Optional(punctuation_no_dash) +
            pyparsing.OneOrMore(nums | nest_grammar | space) +
            word_end
        )

        self.number_then_punctuation = (
            letter +
            nums +
            punctuation +
            pyparsing.ZeroOrMore(nums | punctuation) +
            word_end
        )

        self.punctuation_then_number = (
            letter +
            punctuation_no_dash +
            nums +
            pyparsing.ZeroOrMore(punctuation | nums) +
            word_end
        )
