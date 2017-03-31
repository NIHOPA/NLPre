from nose.tools import *
from word2vec_pipeline.preprocessing.titlecaps import titlecaps

class Titlecaps_Test():
    def __init__(self):
        self.titlecaps = titlecaps()

    def allcaps_test(self):
        doc = 'HELLO WORLD'
        doc_right = 'hello world'
        doc_new = self.titlecaps(doc)

        assert_equal(doc_new, doc_right)

    def mostlycaps_test(self):
        doc = 'HELLo WORLD'
        doc_right = 'HELLo WORLD'
        doc_new = self.titlecaps(doc)

        assert_equal(doc_new, doc_right)


    def multiple_sentance_test(self):
        doc = 'HELLO WORLD. All good'
        doc_right = 'hello world . All good'
        doc_new = self.titlecaps(doc)

        assert_equal(doc_new, doc_right)
