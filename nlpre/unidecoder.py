# -*- coding: utf-8 -*-
import unidecode


class unidecoder(object):

    def __init__(self):
        '''
        Converts a Unicode representation to a reasonable ASCII equivalent.
        '''
        pass

    def __call__(self, doc):
        return unidecode.unidecode(doc)

if __name__ == "__main__":
    text = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
    parser = unidecoder()
    print(parser(text))
