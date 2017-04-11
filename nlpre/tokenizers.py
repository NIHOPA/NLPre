import pattern.en


def split_tokenizer(func):
    ''' Splits a string from input as tokens, allows the function
    to act over the tokens and return a string
    '''
    def wrapper(text):
        # tokens = text.split()
        return ' '.join(func(text))
    return wrapper


def sentence_tokenizer(raw):
    '''
    Uses pattern.en to split input text into a list of word tokens.
    '''

    raw_tokens = pattern.en.parse(raw, chunks=False, tags=False)
    raw_sentences = raw_tokens.split()

    # Each token is now a list of elements, we only need the first one
    sentences = [[w[0] for w in s] for s in raw_sentences]
    return sentences


def word_tokenizer(raw):
    '''
    Uses pattern.en to split input text into a list of word tokens.
    '''
    if not raw:
        return []

    sentences = sentence_tokenizer(raw)

    # Return a list of word tokens
    tokens = [w for s in sentences for w in s]

    return tokens


class meta_text(object):

    '''
    Helper class to hold a unicode string with metadata.
    '''

    def __init__(self, text, **kwargs):
        self.text = text
        self.meta = kwargs
    '''
    Args:
        text: a string
        kwargs: other inputs
    '''

    def __unicode__(self):
        # Remove reference to unicode for now, need a python 2/3 way to do it
        # return unicode(self.text)
        return self.text
    '''
    Returns:
        self.text: a string
    '''
