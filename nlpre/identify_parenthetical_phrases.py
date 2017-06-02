import collections
import six
from Grammars import parenthesis_nester
import logging
import string


class identify_parenthetical_phrases(object):

    """
    Parser to identify abbreviations of phrases found in a parenthesis, ex.
    Health and Human Services (HHS) and Office of the Director (OD).
    """

    def __init__(self):
        """ Initialize the parser. """
        self.parser = parenthesis_nester()
        self.logger = logging.getLogger(__name__)

    def __call__(self, text):
        '''
        Runs the parser. Returns a count of how often the phrases are
        used in the document.

        Args:
            text: a string document
        Returns:
            results: A collections.counter object
        '''

        text = text.replace('-', ' ')
        text = text.replace("'", '')
        text = text.replace('"', '')

        tokens = self.parser(text)
        results = collections.Counter()

        for k, item in enumerate(tokens):
            word = self._is_valid_abbr(item)
            if word:
                subtokens = self._check_matching(word, k, tokens)
                if subtokens:
                    results[(tuple(subtokens), word)] += 1

        if results:
            self.logger.info('Counter: %s' % results)
        return results

    def _is_valid_abbr(self, item):
        '''
        Args:
            item: a list of tokens
        Returns:
            word: the abbreviation, a string token
        '''

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

    def _check_matching(self, word, k, tokens):
        '''
        Args:
            word: a string
            k: the position of the word in tokens, an int
            tokens: a list of strings"
        Returns:
            subtokens: a tuple of string tokens of the abbreviated phrase
        '''

        # Identify the capital letters
        caps = [let for let in word if
                let in string.ascii_uppercase.upper()]

        # Don't try to match with only a single letter (too noisy!)
        if len(caps) < 2:
            return False

        # This may fail if used too early in doc or if nested parens
        # this shouldn't be a match so it's OK!
        # try:
        #    subtokens = tokens[k - len(caps):k]
        #    subtoken_let = [let.upper()[0] for let in subtokens]
        # except:
        #    return False
        subtokens = tokens[k - len(caps):k]
        subtoken_let = [let.upper()[0]
                        for let in subtokens if isinstance(let, basestring)]

        '''
        If the subtokens don't provide a perfect match of the abbreviation,
        we must check if there are filler words. ie. "Health and Human
        Services (HHS)" doesn't provide a match above because "and" isn't
        represented in the abbreviation. To account for this we iterate
        backwards from the abbreviation, trying to reconstruct the
        abbreviation by ignoring filler words.
        '''

        if subtoken_let != caps:
            tokens_to_remove = [
                'and',
                'of',
                'with',
                '&',
                'or',
                'for',
                'the',
                'to']
            subtokens = []
            x = k - 1
            cutoff = x - len(caps) * 2
            while subtoken_let != caps:
                if x < 0 or x < cutoff:
                    return False
                token = tokens[x]
                if isinstance(token, basestring):
                    subtokens.insert(0, token)
                    subtoken_let = [
                        let.upper()[0] for let in subtokens if
                        let not in tokens_to_remove]
                    x -= 1
                else:
                    x -= 1
                    cutoff -= 1
                    continue

        return tuple(subtokens)


# if __name__ == "__main__":

    # Right now, two of of three of these phrases are correctly found.
    # P = identify_parenthetical_phrases()
    # text = ("The Environmental Protection Agency (EPA) is not a government "
    #        "organization (GO) of Health and Human Services (HHS).")
    # print(P(text))
