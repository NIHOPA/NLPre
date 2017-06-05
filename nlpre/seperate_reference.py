import pattern.en
import os
from Grammars import reference_patterns

__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class seperate_reference:
    """
    Detects if a reference number has been mistakenly concatenated to words in
    a document. This module will remove reference numbers, with the option
    to include them as a token representing the reference number. If these
    reference numbers wrap around a period at the end of the sentence, the
    module will identify this and properly split the sentences.


    Example:
        input: 'How is the treatment going.4-5 Pretty well'
        output: 'How is the treatment going . Pretty well'
    """

    def __init__(self, reference_token=False):
        '''
        Initialize the parser

        Args:
            reference_token: boolean, flag to decide to tokenize removed
                reference content
        '''
        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

        self.reference_token = reference_token

        self.reference_pattern = reference_patterns()

        """
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
        """
    def __call__(self, text):
        '''
        call the parser

        Args:
            text: a document string

        Returns:
             return_doc: a document string
        '''
        sentences = pattern.en.tokenize(
            text, punctuation=".,;:!?`''\"@#$^&*+-|=~_")

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
                    new_tokens = self.single_number_pattern(token)
                    new_sentence.extend(new_tokens)
                    continue
                except BaseException:
                    pass

                # check if word is of the form word(4)
                try:
                    new_tokens = self.single_number_parens_pattern(token)
                    new_sentence.extend(new_tokens)
                    continue
                except BaseException:
                    pass

                # Check if the word is of the form word.2,3,4
                new_tokens = self.identify_reference_punctuation_pattern(
                    token, self.reference_pattern.punctuation_then_number)
                if new_tokens:
                    new_sentence.extend(new_tokens)
                    continue

                # Check if the word is of the form word2,3,4
                new_tokens = self.identify_reference_punctuation_pattern(
                    token, self.reference_pattern.number_then_punctuation)
                if new_tokens:
                    new_sentence.extend(new_tokens)
                    continue

                # if no reference detected, append word to the new sentence
                new_sentence.append(token)

            join_sentence = ' '.join(new_sentence)
            new_doc.append(join_sentence)

        return_doc = ' '.join(new_doc)
        return return_doc

    def single_number_pattern(self, token):
        output = []
        parse_return = self.reference_pattern.single_number.parseString(token)

        if parse_return[0] not in self.english_words:
            output.append(token)
        else:
            word = parse_return[0]
            reference = parse_return[1]

            output.append(word)

            if self.reference_token:
                output.append("REF_" + reference)
        return output

    def single_number_parens_pattern(self, token):
        output = []
        parse_return = self.reference_pattern.single_number_parens.\
            parseString(token)
        word = parse_return[0]
        reference = parse_return[1][0]

        output.append(word)

        if self.reference_token:
            output.append("REF_" + reference)

        return output

    def identify_reference_punctuation_pattern(self, token, pattern):
        output = []
        parse_return = \
            pattern.searchString(token)
        if parse_return:
            substring = ''.join(parse_return[0][1:])
            index = token.find(substring)
            word = token[:index]
            reference = token[index:]
            output.append(word)

            if self.reference_token:
                ref_token = "REF_" + reference
                output.append(ref_token)

            if substring[0] == '.':
                output.append('.')
        else:
            output = False

        return output
