# -*- coding: utf-8 -*-
from tokenizers import sentence_tokenizer


def is_any_lowercase(tokens):
    """
    Checks if any letter in a token is lowercase
    
    Args:
        tokens: a string token
    Returns:
        a boolean
    """

    any_alpha = False
    for x in tokens:
        for letter in x:
            if letter.isalpha():
                any_alpha = True
                if letter == letter.lower():
                    return True
    if any_alpha:
        return False
    else:
        return True

# If any sentence is only capitalized, it changes every letter to lowercase


class titlecaps(object):

    """
    Some documents have sentences where every word is uppercase. This is 
    common with titles and abstracts. This class identifies sentences where
    every word is uppercase,and returns the document with these sentences 
    converted to lowercase.
    """

    def __init__(self, min_length=4):
        self.min_length = min_length
    '''
    Args:
        min_length: the minimum length of sentences to convert to lowercase
    '''

    def __call__(self, text):

        sents = sentence_tokenizer(text)

        doc2 = []
        for sent in sents:
            if not is_any_lowercase(sent):

                if len(sent) > self.min_length:
                    print("DECAPING: '{}'".format(' '.join(sent)))
                    sent = [x.lower() for x in sent]

            doc2.append(' '.join(sent))

        doc2 = ' '.join(doc2)
        return doc2
    '''
    Args:
        text: a string document
    Returns:
        doc2: a string document'''

# if __name__ == "__main__":
#    pass
