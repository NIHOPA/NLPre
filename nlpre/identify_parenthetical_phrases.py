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

        # if the subtokens don't provide a perfect match of the abbreviation, we must check
        # if there are filler words. Ie, "Health and Human Services (HHS)" doesn't provide
        # a match above because "and" isn't represented in the abbreviation. To account for this
        # we iterate backwards from the abbreviation, trying to reconstruct the abbreviation by ignoring
        # filler words.
        if subtoken_let != caps:
            tokens_to_remove = ['and', 'of', 'with', '&', 'or', 'for', 'the', 'to']
            subtokens = []
            x = k - 1
            while subtoken_let != caps:
                if x < 0:
                    return False
                token = tokens[x]
                subtokens.insert(0, token)
                subtoken_let = [let.upper()[0] for let in subtokens if let not in tokens_to_remove]
                x -= 1

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
    text = ("The Environmental Protection Agency (EPA) is not a government "
            "organization (GO) of Health and Human Services (HHS).")
    print(P(text))
