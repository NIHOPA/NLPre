import string
import collections
import six
import pyparsing as pypar


class parenthesis_nester(object):

    def __init__(self):
        nest = pypar.nestedExpr
        g = pypar.Forward()
        nestedParens = nest('(', ')')
        nestedBrackets = nest('[', ']')
        nestedCurlies = nest('{', '}')
        nest_grammar = nestedParens | nestedBrackets | nestedCurlies

        parens = "(){}[]"
        letters = ''.join([x for x in pypar.printables
                           if x not in parens])
        word = pypar.Word(letters)

        g = pypar.OneOrMore(word | nest_grammar)
        self.grammar = g

    def __call__(self, line):
        try:
            tokens = self.grammar.parseString(line)
        except:
            return []
        return tokens


class identify_parenthetical_phrases(object):

    def __init__(self):
        self.parser = parenthesis_nester()

    def is_valid_abbr(self, item):
        if isinstance(item, six.string_types):
            return False
        if len(item) != 1:
            return False

        word = item[0]

        # Break if we are doubly nested
        if not isinstance(word, six.string_types):
            return False

        # Check if there are any capital letters
        if word.lower() == word:
            return False

        return word

    def check_matching(self, word, k, tokens):
        # Identify the capital letters
        caps = [let for let in word if
                let in string.ascii_uppercase.upper()]

        # Don't try to match with only a single letter (too noisy!)
        if len(caps) < 2:
            return False

        # This may fail if used too early in doc or if nested parens
        # this shouldn't be a match so it's OK!

        try:
            subtokens = tokens[k - len(caps):k]
            subtoken_let = [let.upper()[0] for let in subtokens]
        except:
            return False

        if subtoken_let != caps:
            return False

        return tuple(subtokens)

    def __call__(self, text):

        text = text.replace('-', ' ')
        text = text.replace("'", '')
        text = text.replace('"', '')

        tokens = self.parser(text)
        results = collections.Counter()

        for k, item in enumerate(tokens):
            word = self.is_valid_abbr(item)
            if word:
                subtokens = self.check_matching(word, k, tokens)
                if subtokens:
                    results[(tuple(subtokens), word)] += 1

        return results


if __name__ == "__main__":

    # Right now, two of of three of these phrases are correctly found.
    P = identify_parenthetical_phrases()
    text = ("The Enviromental Protection Agency (EPA) is not a goverment "
            "organization (GO) of Health and Human Services (HHS).")
    print(P(text))