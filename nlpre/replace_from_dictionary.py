import collections
import csv
import os
import logging
from flashtext import KeywordProcessor
from .dictionary import MeSH as f_MeSH


class replace_from_dictionary(object):

    """
    Replace phrases from an input dictionary. The replacement is done without
    regard to case, but punctuation is handled correctly.

    The MeSH (Medical Subject Headings) dictionary is built-in.

    Example (given the MeSH dictionary):
        input: '(11-Dimethylethyl)-4-methoxyphenol is great'
        output: 'MeSH_Butylated_Hydroxyanisole is great'
    """

    def __init__(self, f_dict=None, prefix="", suffix=""):
        """
        Initialize the parser.

        Args:
            f_dict: filename, location of the replacement dictionary.
            prefix: string, text to prefix each replacement.
            suffix: string, text to suffix each replacement.
        """
        self.logger = logging.getLogger(__name__)

        if f_dict is None:
            local_path = os.path.dirname(__file__)
            f_dict = os.path.join(local_path, f_MeSH)
            self.logger.debug("Using default dictionary: %s" % f_dict)

        if not os.path.exists(f_dict):
            msg = "Can't find dictionary {}".format(f_dict)
            self.logger.error(msg)
            raise IOError()

        self.prefix = prefix
        self.suffix = suffix
        terms = collections.defaultdict(list)

        with open(f_dict) as FIN:
            csvfile = csv.DictReader(FIN)
            for row in csvfile:
                terms[row["replacement"]].append(row["term"])

        self.FT = KeywordProcessor()
        self.FT.add_keywords_from_dict(terms)

    def __call__(self, doc):
        """
        Runs the parser.

        Args:
            text: a document string
        Returns:
            doc: a document string
        """

        keywords = self.FT.extract_keywords(doc, span_info=True)

        n = 0
        tokens = []

        for word, i, j in keywords:
            if n < i:
                tokens.append(doc[n:i])
            tokens.append("".join([self.prefix, word, self.suffix]))
            n = j
        tokens.append(doc[n : len(doc)])
        return "".join(tokens)
