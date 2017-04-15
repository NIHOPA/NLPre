# -*- coding: utf-8 -*-
import unidecode


class unidecoder(object):

    """
    Converts a Unicode representation to a reasonable ASCII equivalent.

    Example:
        input = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
        output=  'a-Helix b-sheet Aa Nn Bb Ksx Gg Oo'
    """

    def __init__(self):
        """ Initialize the parser. """
        pass

    def __call__(self, unicode_text):
        '''
        Runs the parser.

        Args:
            unicode_text: a unicode document
        Returns:
            text: An ascii equivalent of unicode_text
        '''

        return unidecode.unidecode(unicode_text)

# if __name__ == "__main__":
#    text = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
#    parser = unidecoder()
#    print(parser(text))
