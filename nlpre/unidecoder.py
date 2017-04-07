# -*- coding: utf-8 -*-
import unidecode


class unidecoder(object):
    '''
    Args:
        doc: a unicode document
    
    Returns:
        Converts a Unicode representation to a reasonable ASCII equivalent.
    '''
    def __init__(self):
        pass

    def __call__(self, doc):
        return unidecode.unidecode(doc)


# if __name__ == "__main__":
#    text = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
#    parser = unidecoder()
#    print(parser(text))
