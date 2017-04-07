# -*- coding: utf-8 -*-
import unidecode


class unidecoder(object):
    '''
    Args:
        unicode_text: a unicode document
    
    Returns:
        Converts a Unicode representation to a reasonable ASCII equivalent.
    '''
    def __init__(self):
        pass

    def __call__(self, unicode_text):
        return unidecode.unidecode(unicode_text)


# if __name__ == "__main__":
#    text = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
#    parser = unidecoder()
#    print(parser(text))
