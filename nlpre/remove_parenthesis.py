import pyparsing as pypar
import pattern.en
import six


class remove_parenthesis(object):

    """
    When creating word embeddings, we do not want parenthetical content
    to be associated with the sentences they are found in. This class
    returns the input document, and appends parenthetical content as a new
    sentence to the sentence they were found in.

    Example:
        input = 'Hello (it is a beautiful day) world.'
        output = 'Hello world. it is a beautiful day .'
    """

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

            # If the count of the left paren doesn't match the right, then
            # ignore all parenthesis
            FLAG_valid = (LP_Paran == RP_Paran) and (
                LP_Bracket == RP_Bracket) and (LP_Curl == RP_Curl)

            # try:
            #    tokens = self.grammar.parseString(sent)
            # except (pypar.ParseException, RuntimeError):
            #    FLAG_valid = False
            tokens = self.grammar.parseString(sent)

            if not FLAG_valid:
                # On fail simply remove all parenthesis
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
                # Append parenthetical sentences to end of sentence
                text = self.paren_pop(tokens)
                doc_out.extend(text)

        # doc_out.extend(content_list)
        return '\n'.join(doc_out)
    '''
    Args:
        text: a string document.
    Returns:
        doc_out: a string document with parenthetical content processed
    '''

    def paren_pop(self, parsed_tokens):
        # must convert the ParseResult to a list, otherwise adding it to a list
        # causes weird results.
        if isinstance(parsed_tokens, pypar.ParseResults):
            parsed_tokens = parsed_tokens.asList()

        content = self.paren_pop_helper(parsed_tokens)
        return content
    '''
    Args:
        parsed_tokens: a ParseResult object
    Returns:
        content: a list of string sentences
    '''

    def paren_pop_helper(self, tokens):

        # check if tokens is empty
        if not tokens:
            return tokens
        # Check if there is a single sentence in parenthetical content
        # if so, use the sentence as tokens
        if isinstance(tokens[0], list) and len(tokens) == 1:
            tokens = tokens[0]

        new_tokins = []
        token_words = [x for x in tokens if isinstance(x, six.string_types)]

        # If tokens don't include parenthetical content, return as string
        if len(token_words) == len(tokens):
            if token_words[-1] != '.':
                token_words.append('.')
            return [' '.join(token_words)]
        else:
            token_parens = [x for x in tokens if isinstance(x, list)]
            reorged_tokens = []

            # Iterate through all parenthetical content, recursing on them
            # This allows content in nested parenthesis to be captured
            for tokes in token_parens:
                sents = self.paren_pop_helper(tokes)
                reorged_tokens.extend(sents)

            # Bundles outer sentence with inner parenthetical content
            if token_words[-1] != '.':
                token_words.append('.')
            new_tokins.append(' '.join(token_words))
            new_tokins.extend(reorged_tokens)

            # New tokins returns a list of strings
            return new_tokins
    '''
    Args:
        tokens: a list of string sentences and parenthetical content lists
    Returns:
        new_tokins: a list of string sentences
    '''
