from nose.tools import *
from word2vec_pipeline.preprocessing.decaps_text import decaps_text


class Decaps_Text_Test:
    def __init__(self):
        self.decaps = decaps_text()

    def first_capital_single_sentance_test(self):
        doc = "Hello world"
        doc_right = "hello world"
        doc_new = self.decaps(doc)

        assert_equal(doc_right, doc_new)

    def capital_in_middle_test(self):
        doc = "hellO world"
        doc_right = "hello world"
        doc_new = self.decaps(doc)

        assert_equal(doc_right, doc_new)

    def multiple_capital_test(self):
        doc = "HEllo world"
        doc_right = "HEllo world"
        doc_new = self.decaps(doc)

        assert_equal(doc_right, doc_new)

    def capital_multiple_sentance_test(self):
        doc = "Hello world. Goodnight world"
        doc_right = "hello world .\ngoodnight world"
        doc_new = self.decaps(doc)

        assert_equal(doc_right, doc_new)