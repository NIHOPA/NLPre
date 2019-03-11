import pyparsing
from pyparsing import Word, WordStart, WordEnd, ZeroOrMore, Optional


class reference_patterns:
    def __init__(self):
        real_word_dashes = Word(pyparsing.alphas + "-")
        punctuation = Word(".!?:,;-")
        punctuation_no_dash = Word(".!?:,;")
        punctuation_reference_letter = Word(".:,;-")

        printable = Word(pyparsing.printables, exact=1)
        letter = Word(pyparsing.alphas, exact=1)
        letter_reference = punctuation_reference_letter + letter

        nums = (
            Word(pyparsing.nums)
            + Optional(letter)
            + ZeroOrMore(letter_reference)
        )

        word_end = (
            pyparsing.ZeroOrMore(Word(")") | Word("}") | Word("]"))
            + Optional(punctuation_no_dash)
            + WordEnd()
        )

        self.single_number = WordStart() + real_word_dashes + nums + word_end

        self.single_number_parens = (
            printable
            + letter
            + Optional(punctuation_no_dash)
            + pyparsing.OneOrMore(
                Word("([{", exact=1)
                + pyparsing.OneOrMore(nums | Word("-"))
                + Word(")]}", exact=1)
            )
            + Optional(punctuation_no_dash)
            + word_end
        )

        self.number_then_punctuation = (
            printable
            + letter
            + nums
            + punctuation
            + pyparsing.ZeroOrMore(nums | punctuation)
            + word_end
        )

        self.punctuation_then_number = (
            printable
            + letter
            + punctuation_no_dash
            + nums
            + pyparsing.ZeroOrMore(punctuation | nums)
            + word_end
        )
