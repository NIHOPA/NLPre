# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from nlpre import unidecoder

class Unidecoder_Test:
    def __init__(self):
        self.decoder = unidecoder()

    def greek_test(self):
        doc = u"α-Helix β-sheet Αα Νν Ββ Ξξ Γγ Οο"
        doc_right = 'a-Helix b-sheet Aa Nn Bb Ksx Gg Oo'
        doc_new = self.decoder(doc)
        assert_equal(doc_right, doc_new)

    def german_test(self):
        doc = u"Lëtzebuergesch"
        doc_right = 'Letzebuergesch'
        doc_new = self.decoder(doc)
        assert_equal(doc_right, doc_new)

    def dutch_test(self):
        doc = u"vóórkomen"
        doc_right = 'voorkomen'
        doc_new = self.decoder(doc)
        assert_equal(doc_right, doc_new)

    def more_greek_test(self):
        doc = u"perispōménē"
        doc_right = 'perispomene'
        doc_new = self.decoder(doc)
        assert_equal(doc_right, doc_new)
