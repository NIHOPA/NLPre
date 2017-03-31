import os
import pandas as pd
from pattern.en import tokenize


def contains_sublist(lst, sublst):
    # Finds all cases of a sublist and lists where it happens
    n = len(sublst)
    idx = [(sublst == lst[i:i + n]) for i in range(len(lst) - n + 1)]
    return idx


class replace_from_dictionary(object):

    '''
    DOCSTRING: TO WRITE.
    '''

    def __init__(self, f_dict, input_data_directory):

        f_dict = os.path.join(input_data_directory, f_dict)

        if not os.path.exists(f_dict):
            msg = "Can't find dictionary {}".format(f_dict)
            raise IOError(msg)

        df = pd.read_csv(f_dict)
        items = df["SYNONYM"].str.lower(), df["replace_token"]
        self.X = dict(zip(*items))

    def __call__(self, org_doc):

        doc = org_doc

        tokens = doc.lower().split()
        ldoc = ' '.join([x for x in tokens if "_" not in x])

        # Identify which phrases were used
        keywords = [key for key in self.X if key in ldoc]
        punctuation = ".,;:!?()[]{}`''\"@#$^&*+-|=~"

        # Loop over the keywords and replace them one-by-one.
        # This is inefficient, but less error prone.

        parsed_sent = []

        for sent in tokenize(doc, punctuation=punctuation):

            for word in keywords:
                word_n_tokens = len(word.split())

                new_word = self.X[word]
                word_tokens = word.split()

                # Check if the substring tokens match
                tokens = sent.lower().split()
                mask = contains_sublist(tokens, word_tokens)
                while any(mask):
                    idx = mask.index(True)
                    sent = sent.split()
                    args = sent[:idx] + [new_word, ] + sent[
                        idx + word_n_tokens:]
                    sent = ' '.join(args)
                    tokens = sent.lower().split()
                    mask = contains_sublist(tokens, word_tokens)

            parsed_sent.append(sent)

        doc = ' '.join(parsed_sent)

        """
        # Change the punctuation to a more readable format for debugging
        punc_compress = ''').,?!':'''
        for punc in punc_compress:
            doc = doc.replace(' '+punc,punc)

        punc_compress = '''('''
        for punc in punc_compress:
            doc = doc.replace(punc+' ',punc)
        """

        return doc
