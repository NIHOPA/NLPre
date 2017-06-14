from nose.tools import *
from nlpre import titlecaps


class Titlecaps_Test():

    @classmethod
    def setup_class(cls):
        cls.parser = titlecaps(min_length=1)

    def allcaps_test(self):
        doc = 'HELLO WORLD'
        doc_right = 'hello world'
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def mostlycaps_test(self):
        doc = 'HELLo WORLD'
        doc_right = 'HELLo WORLD'
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def multiple_sentance_test(self):
        doc = 'HELLO WORLD. All good'
        doc_right = 'hello world . All good'
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def numbers_test(self):
        doc = 'HELLO WORLD. 1111'
        doc_right = 'hello world . 1111'
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def long_enough_sentence_test(self):

        caps = titlecaps()
        doc = 'THIS SENTENCE SHORT'
        doc_right = 'THIS SENTENCE SHORT'
        doc_new = caps(doc)

        assert_equal(doc_new, doc_right)
