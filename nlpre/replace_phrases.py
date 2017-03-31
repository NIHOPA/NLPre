import os
import pandas as pd
from tokenizers import word_tokenizer


class replace_phrases(object):

    '''
    DOCSTRING: TO WRITE.
    '''

    def __init__(self, f_abbreviations, input_data_directory):

        f_abbr = os.path.join(input_data_directory, f_abbreviations)
        print(f_abbr)
        self.load_phrase_database(f_abbr)

    def load_phrase_database(self, f_abbreviations):

        df = pd.read_csv(f_abbreviations)

        counts = df.phrase.str.split().apply(len)
        self.max_n = counts.max()
        self.min_n = counts.min()

        self.P = {}

        for phrase, abbr in zip(df.phrase, df.abbr):
            phrase = tuple(phrase.split(' '))
            self.P[phrase] = abbr

    def ngram_tokens(self, tokens, n):

        for k in range(len(tokens) - n):
            block = tokens[k:k + n]
            lower_block = tuple([x.lower() for x in block])
            substring = ' '.join(block)
            yield lower_block, substring

    def phrase_sub(self, phrase):
        return '_'.join(["PHRASE"] + list(phrase))

    def __call__(self, org_doc):

        doc = org_doc
        tokens = word_tokenizer(doc)

        # First pass, identify which phrases are used
        iden_abbr = {}
        replacements = {}
        for n in range(self.min_n, self.max_n + 1):
            for phrase, substring in self.ngram_tokens(tokens, n):

                if phrase in self.P:
                    abbr = self.P[phrase]
                    iden_abbr[phrase] = abbr
                    replacements[substring] = self.phrase_sub(phrase)

        # Replace these with a phrase token
        for substring, newstring in replacements.items():
            doc = doc.replace(substring, newstring)

        # Now find any abbrs used in the document and replace them
        tokens = word_tokenizer(doc)

        for phrase, abbr in iden_abbr.items():
            tokens = [self.phrase_sub(phrase)
                      if x == abbr else x for x in tokens]

        # This returns word split phrase string
        doc = ' '.join(tokens)
        return doc
