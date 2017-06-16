import pyparsing as pypar
import pattern.en
import six
import logging
from Grammars import parenthesis_nester


class separated_parenthesis(object):

    """
    Separates parenthetical content into new sentences. This is useful when
    creating word embeddings, as associations should only be made within the
    same sentence.

    This parser returns a document that is sentence chunked and appends
    parenthetical content as a new sentence to the sentence following the
    sentences it was found in. Terminal punctuation of a period is added to
    parenthetical sentences if necessary. Parenthetical sentences can be
    pruned by setting min_keep_length.

    Example:
        input = 'Hello (it is a beautiful day) world.'
        output = 'Hello world. it is a beautiful day .'
    """

    def __init__(self, min_keep_length=0):
        """
        Initialize the parser.

        Args:
            min_keep_length: if None keep everything, if 0 drop everything
              (default), for any other integer n, keep only if statment is
              at least n tokens long.
        """
        self.logger = logging.getLogger(__name__)

        self.min_keep_length = min_keep_length
        self.grammar = parenthesis_nester()
        self.parse = lambda x: pattern.en.tokenize(x)

    def __call__(self, text):
        '''
        Runs the parser.

        Args:
            text: a string document
        Returns:
            text: A string document with parenthetical content processed
        '''

        # Known issue - pattern will split on punctuation, even when found in
        # parenthetical content. So, the sentence "A A V (C D. A B) A." would
        # be split into sentences "A A V (C D." and " A B) A."
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

            try:
                tokens = self.grammar.grammar.parseString(sent)
            except (pypar.ParseException, RuntimeError):
                FLAG_valid = False

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

                text = self.paren_pop(tokens)
                doc_out.extend(text)

        return '\n'.join(doc_out)

    def paren_pop(self, parsed_tokens):
        '''
        Args:
            parsed_tokens: a ParseResult object
        Returns:
            content: a list of string sentences
        '''

        # must convert the ParseResult to a list, otherwise adding it to a list
        # causes weird results.
        if isinstance(parsed_tokens, pypar.ParseResults):
            parsed_tokens = parsed_tokens.asList()

        content = self.paren_pop_helper(parsed_tokens)

        return content

    def paren_pop_helper(self, tokens):
        '''
        Args:
            tokens: a list of string sentences and parenthetical content lists
        Returns:
            new_tokens: a list of string sentences
        '''

        # Check if token list is empty
        if not tokens:
            return tokens

        # Check if there is a single sentence in parenthetical content
        # if so, use the sentence as tokens
        if isinstance(tokens[0], list) and len(tokens) == 1:
            tokens = tokens[0]

        new_tokens = []
        token_words = [x for x in tokens if isinstance(x, six.string_types)]

        # If tokens don't include parenthetical content, return as string
        if len(token_words) == len(tokens) and len(token_words):
            if token_words[-1] not in ['.', '!', '?']:
                token_words.append('.')
            return [' '.join(token_words)]
        else:
            token_parens = [x for x in tokens if isinstance(x, list)]
            reorged_tokens = []

            # Iterate through all parenthetical content, recursing on them
            # This allows content in nested parenthesis to be captured
            for tokens in token_parens:
                sents = self.paren_pop_helper(tokens)

                for sent in sents:

                    # Only keep if the sentence is at least as long as the
                    # min_keep_length
                    n_tokens_sent = len(sent.split())
                    if (self.min_keep_length is None or
                            self.min_keep_length <= n_tokens_sent):

                        self.logger.info(
                            'Expanded parenthetical content: %s' %
                            sent)
                        reorged_tokens.append(sent)

            # Bundles outer sentence with inner parenthetical content
            if token_words:
                if token_words[-1] not in ['.', '!', '?']:
                    token_words.append('.')
                new_tokens.append(' '.join(token_words))

            new_tokens.extend(reorged_tokens)

            # New tokens returns a list of strings
            return new_tokens
