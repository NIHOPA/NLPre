# -*- coding: utf-8 -*-
import unidecode


class unidecoder(object):

    '''
    Converts a Unicode representation to a reasonable ASCII equivalent.
    '''

    def __init__(self):
        pass

    def __call__(self, unicode_text):
        return unidecode.unidecode(unicode_text)
    '''
    Args:
        unicode_text: a unicode document
    Returns:
        An ascii equivalent of unicode_text
    '''


# if __name__ == "__main__":
#    text = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
#    parser = unidecoder()
#    print(parser(text))
