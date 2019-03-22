from nose.tools import *
from nlpre import decaps_text


class Decaps_Text_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = decaps_text()

    def first_capital_single_sentence_test(self):
        doc = "Hello world"
        doc_right = "hello world"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def capital_in_middle_test(self):
        doc = "hellO world"
        doc_right = "hello world"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_capital_test(self):
        doc = "HEllo world"
        doc_right = "HEllo world"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def capital_multiple_sentence_test(self):
        doc = "Hello world. Goodnight world"
        doc_right = "hello world. goodnight world"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)
