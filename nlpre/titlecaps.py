import logging
from . import nlp


class titlecaps(object):

    """
    Documents sometimes have sentences that are entirely in uppercase. This is
    commonly found in titles and abstracts of older documents. This class
    identifies sentences where every word is uppercase, and returns the
    document with these sentences converted to lowercase.
    """

    def __init__(self, min_length=4):
        """
        Initialize the parser.

        Args:
            min_length: Minimum sentence length, otherwise sentence is returned
                        untouched.
        """
        self.logger = logging.getLogger(__name__)
        self.min_length = min_length

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: a string document
        Returns:
            doc2: a string document
        """

        # Need to keep the parser for sentence detection
        sents = nlp(text, disable=["tagger"]).sents

        doc2 = []
        for sent in sents:

            line = sent.text

            if not is_any_lowercase(line):

                if len(line) > self.min_length:
                    line = line.lower()

            doc2.append(line + sent[-1].whitespace_)

        doc2 = "".join(doc2)
        return doc2


def is_any_lowercase(sentence):
    """
    Checks if any letter in a sentence is lowercase, return False if there
    are no alpha characters.

    Args:
        tokens: A list of string
    Returns:
        boolean: True if any letter in any token is lowercase
    """

    if any(x.isalpha() & (x == x.lower()) for x in sentence):
        return True

    return not any(x.isalpha() for x in sentence)
