import pyparsing as pypar
import pattern.en
import six


'''
There's another python named pypar. I'd not renaming pyparsing under an alias
this class removes all words that are found within a parenthesis,
regardless of how nested they are. If an unbalanced amount of parens are
found, the parens are simply removed.
'''


class remove_parenthesis(object):

    def __init__(self):
        nest = pypar.nestedExpr
        g = pypar.Forward()  # is this necessary?
        nestedParens = nest('(', ')')
        nestedBrackets = nest('[', ']')
        nestedCurlies = nest('{', '}')
        nest_grammar = nestedParens | nestedBrackets | nestedCurlies

        parens = "(){}[]"
        letters = ''.join([x for x in pypar.printables
                           if x not in parens])
        word = pypar.Word(letters)
        # An allowable word is a sequence of any non
        # parenthesis character

        g = pypar.OneOrMore(word | nest_grammar)
        self.grammar = g

        # self.parse = lambda x:pattern.en.parse(x,chunks=False,tags=False)
        self.parse = lambda x: pattern.en.tokenize(
            x)  # ,chunks=False,tags=False)
        # Tags each word of a sentence with part of speech

    # is text different than doc, used in other pre-processing modules?


    def __call__(self, text):

        sentences = self.parse(text)

        doc_out = []
        for sent in sentences:

            # Count the number of left and right parens
            LP_Paran = sum(1 for a in sent if a == '(')
            RP_Paran = sum(1 for a in sent if a == ')')

            LP_Bracket = sum(1 for a in sent if a == '[')
            RP_Bracket = sum(1 for a in sent if a == ']')

            LP_Curl = sum(1 for a in sent if a == '{')
            RP_Curl = sum(1 for a in sent if a == '}')

            # If the count of the left paren doesn't match the right ignore
            FLAG_valid = (LP_Paran == RP_Paran) and (
                LP_Bracket == RP_Bracket) and (LP_Curl == RP_Curl)

            try:
                tokens = self.grammar.parseString(sent)
            except (pypar.ParseException, RuntimeError):
                FLAG_valid = False

            if not FLAG_valid:
                # On fail simply remove all parens
                # Should instead probably remove all parens in outermost
                # parens, while still removing words in completed inner parens
                sent = sent.replace('(', '')
                sent = sent.replace(')', '')
                sent = sent.replace('[', '')
                sent = sent.replace(']', '')
                sent = sent.replace('{', '')
                sent = sent.replace('}', '')
                tokens = sent.split()

                text = ' '.join(tokens)
                doc_out.append(text)

            else:
                # Remove nested parens

                text = self.paren_pop(tokens)
                doc_out.extend(text)

        return '\n'.join(doc_out)

    def paren_pop(self, tokens):
        if isinstance(tokens, pypar.ParseResults):
            tokens = tokens.asList()

        new_tokins = []
        tokenWords = [x for x in tokens if isinstance(x, six.string_types)]

        if len(tokenWords) == len(tokens):
            return [' '.join(tokenWords)]
        else:
            # must convert the ParseResult to a list, otherwise adding it to a list causes weird results.
            tokenParens = [x for x in tokens if isinstance(x, list)]
            #if there's only a single list in outer list, use it

            reorgedTokens = []
            for tokes in tokenParens:
                sents = self.paren_pop(tokes)
                reorgedTokens.extend(sents)

            new_tokins.append(' '.join(tokenWords))
            #new_tokins.extend(self.paren_pop(tokenParens))
            new_tokins.extend(reorgedTokens)


            #New tokins returns a list of strings
            return new_tokins





    def paren_pop_old(self, tokens):
        if isinstance(tokens, pypar.ParseResults):
            tokens = tokens.asList()

        new_tokins = []
        tokenWords = [x for x in tokens if isinstance(x, six.string_types)]

        if len(tokenWords) == len(tokens):
            return [' '.join(tokenWords)]
        else:
            # must convert the ParseResult to a list, otherwise adding it to a list causes weird results.
            tokenParens = [x for x in tokens if isinstance(x, list)]
            #if there's only a single list in outer list, use it
            if len(tokenParens) == 1:
                tokenParens = tokenParens[0]

            new_tokins.append(' '.join(tokenWords))
            new_tokins.extend(self.paren_pop(tokenParens))
            return new_tokins


"""
    def __call__(self, text):

        sentences = self.parse(text)

        doc_out = []
        for sent in sentences:

            # Count the number of left and right parens
            LP_Paran = sum(1 for a in sent if a == '(')
            RP_Paran = sum(1 for a in sent if a == ')')

            LP_Bracket = sum(1 for a in sent if a == '[')
            RP_Bracket = sum(1 for a in sent if a == ']')

            LP_Curl = sum(1 for a in sent if a == '{')
            RP_Curl = sum(1 for a in sent if a == '}')

            # If the count of the left paren doesn't match the right ignore
            FLAG_valid = (LP_Paran == RP_Paran) and (
                LP_Bracket == RP_Bracket) and (LP_Curl == RP_Curl)

            try:
                tokens = self.grammar.parseString(sent)
            except (pypar.ParseException, RuntimeError):
                FLAG_valid = False

            if not FLAG_valid:
                # On fail simply remove all parens
                # Should instead probably remove all parens in outermost
                # parens, while still removing words in completed inner parens
                sent = sent.replace('(', '')
                sent = sent.replace(')', '')
                sent = sent.replace('[', '')
                sent = sent.replace(']', '')
                sent = sent.replace('{', '')
                sent = sent.replace('}', '')
                tokens = sent.split()

            # Remove nested parens
            tokens = [x for x in tokens if isinstance(x, six.string_types)]
            text = ' '.join(tokens)

            doc_out.append(text)

        return '\n'.join(doc_out)

"""