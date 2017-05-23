import itertools
import collections
import re
import csv
import os
import logging


class replace_from_dictionary(object):

    """
    Replace phrases from an input dictionary. The replacement is done without
    regard to case, but punctuation is handled correctly.

    The MeSH (Medical Subject Headings) dictionary is built-in.

    Example (given the MeSH dictionary):
        input: '(11-Dimethylethyl)-4-methoxyphenol is great'
        output: 'MeSH_Butylated_Hydroxyanisole is great'
    """

    f_MeSH = "dictionaries/MeSH_two_word_lexicon.csv"

    def __init__(self, f_dict=None, prefix=''):
        '''
        Initialize the parser.

        Args:
            f_dict: filename, location of the replacement dictionary.
            prefix: string, text to prefix each replacement.
        '''
        self.logger = logging.getLogger(__name__)

        if f_dict is None:
            local_path = os.path.dirname(__file__)
            f_dict = os.path.join(local_path, self.f_MeSH)
            self.logger.debug('Using default dictionary: %s' % f_dict)

        if not os.path.exists(f_dict):
            msg = "Can't find dictionary {}".format(f_dict)
            self.logger.error(msg)
            raise IOError()

        self.rdict = {}
        with open(f_dict) as FIN:
            csvfile = csv.DictReader(FIN)
            for row in csvfile:
                term = row["term"].lower()
                self.rdict[term] = '{}{}'.format(prefix, row["replacement"])

    def __call__(self, text):
        '''
        Runs the parser.

        Args:
            text: a document string
        Returns:
            doc: a document string
        '''

        doc = text
        ldoc = doc.lower()

        # Identify which phrases were used and possible replacements
        R = collections.defaultdict(list)
        for key, val in self.rdict.iteritems():
            if key in ldoc:
                R[val].append(key)

        # Remove replacements that are substrings of another
        # "5' exonuclease", vs "3' 5' exonuclease"
        all_replacements = [x for v in R.values() for x in v]
        ignore_tokens = set()
        for k1, k2 in itertools.combinations(all_replacements, r=2):
            if len(k1) < len(k2) and k1 in k2:
                ignore_tokens.add(k1)

        # For each term, make replacements based off size order
        for term, replacements in R.iteritems():
            replacements = sorted(replacements, key=lambda x: -len(x))
            for rval in replacements:
                if rval in ignore_tokens:
                    continue
                pattern = re.compile(re.escape(rval), re.IGNORECASE)
                doc = pattern.sub(' {} '.format(term), doc)
                self.logger.info('Replacing term %s with %s' % (rval, term))

        doc = ' '.join([x for x in doc.split(' ') if x])
        return doc


# if __name__ == "__main__":
#    P = replace_from_dictionary('MeSH_two_word_lexicon.csv',
#                                'nlpre/dictionaries')
#    text = '((11-Dimethylethyl)-4-methoxyphenol).'
#    print(P(text))
