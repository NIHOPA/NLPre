from tokenizers import sentence_tokenizer
import logging


class titlecaps(object):

    """
    Documents sometimes have sentences that are entirely in uppercase. This is
    commonly found in titles and abstracts of older documents. This class
    identifies sentences where every word is uppercase, and returns the
    document with these sentences converted to lowercase.
    """

    def __init__(self, min_length=4):
        '''
        Initialize the parser.

        Args:
            min_length: Minimum sentence length, otherwise sentence is returned
                        untouched.
        '''
        self.logger = logging.getLogger(__name__)
        self.min_length = min_length

    def __call__(self, text):
        '''
        Runs the parser.

        Args:
            text: a string document
        Returns:
            doc2: a string document
        '''

        sents = sentence_tokenizer(text)

        doc2 = []
        for sent in sents:
            if not is_any_lowercase(sent):

                if len(sent) > self.min_length:
                    self.logger.info("DECAPING: '{}'".format(' '.join(sent)))
                    sent = [x.lower() for x in sent]

            doc2.append(' '.join(sent))

        doc2 = ' '.join(doc2)
        return doc2


def is_any_lowercase(tokens):
    """
    Checks if any letter in a token is lowercase, return False if there
    are no alpha characters.

    Args:
        tokens: A list of string
    Returns:
        boolean: True if any letter in any token is lowercase
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


# if __name__ == "__main__":
#    pass
