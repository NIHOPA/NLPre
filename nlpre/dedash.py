# -*- coding: utf-8 -*-
import os
import logging

__internal_wordlist = "dictionaries/english_wordlist.txt"
__local_dir = os.path.dirname(os.path.abspath(__file__))
_internal_wordlist = os.path.join(__local_dir, __internal_wordlist)


class dedash(object):

    """
    When importing documents, words are occasionally split apart and
    separated by a dash. For instance, "treatment" might be imported as
    "treat- ment". This class detects these splits and returns a version of
    the document with the words corrected.
    """

    def __init__(self):
        """ Initialize the parser. Preloads a fixed English dictionary. """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Loading wordlist from %s" % _internal_wordlist)

        self.english_words = set()
        with open(_internal_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

    def __call__(self, text):
        """ Runs the parser, takes and returns a string. """

        tokens = text.split()

        for i in range(len(tokens) - 1):
            if is_dash_word(tokens[i]):

                # Require the first character of the next word is an alpha
                if not tokens[i + 1][0].isalpha():
                    continue

                # Skip words with more than 2 caps
                if len([x for x in tokens[i + 1] if x == x.upper()]) >= 2:
                    continue

                word = "{}{}".format(tokens[i][:-1], tokens[i + 1])

                test_word = ''.join([x for x in word if x.isalpha()])

                # Only combine sensible english words
                if test_word.lower() not in self.english_words:
                    continue

                self.logger.info("Merging tokens %s %s %s"
                                 % (tokens[i], tokens[i + 1], word))

                tokens[i] = word
                tokens[i + 1] = ''

        doc = ' '.join(tokens)
        return doc


def is_dash_word(s):
    """
    Determines if a token might be the first portion of a dashed word

    Args:
        s: a string
    Return:
        A boolean indicating whether the token is potentially a dash word
    """

    # Skip words with more than 2 caps
    if len([x for x in s if x == x.upper() and x.isalpha()]) >= 2:
        return False
    if len(s) <= 1:
        return False
    if s[-1] != '-':
        return False

    # Require that at least one of the tokens is an alpha
    return any([x.isalpha() for x in s[:-1]])

# if __name__ == "__main__":
#    text = '''1.-
# One of the major obstacles to such studies is the lack of safe
# and effective treat- ment for fever in the critically ill. Ex- and
# post- ante.'''
#    D = dedash()
#    print(D(text))
