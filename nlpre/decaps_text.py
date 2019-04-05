import logging
from . import nlp


class decaps_text(object):

    """
    Normalizes capitalization patterns. Words with only a single capital
    will be converted into lower case.
    """

    def __init__(self):
        """ Initialize the parser. """
        self.logger = logging.getLogger(__name__)

    def diffn(self, s1, s2):
        """ Returns the number of different characters between two strings."""
        return len([a for a, b in zip(s1, s2) if a != b])

    def modify_word(self, org):
        """
        Changes a word to lower case if it contains exactly one capital letter.

        Args:
            org: a string
        Returns:
            lower: the lowercase of org, a string
        """

        lower = org.lower()

        if self.diffn(org, lower) > 1:
            return org
        elif org != lower:
            self.logger.info("Decapitalizing word %s to %s" % (org, lower))
        return lower

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: a string document
        Returns:
            doc2: a string document
        """

        doc2 = []

        for token in nlp(text, disable=["parser", "tagger"]):
            new_token = self.modify_word(token.text)
            doc2.append(new_token)
            doc2.append(token.whitespace_)

        doc2 = "".join(doc2)
        return doc2
