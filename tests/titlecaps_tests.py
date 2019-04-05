from nose.tools import *
from nlpre import titlecaps


class Titlecaps_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = titlecaps(min_length=1)

    def allcaps_test(self):
        doc = "HELLO WORLD."
        doc_right = "hello world."
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def mostlycaps_test(self):
        doc = "HELLo WORLD."
        doc_right = "HELLo WORLD."
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def multiple_sentance_test(self):
        doc = "HELLO WORLD! All good."
        doc_right = "hello world! All good."
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def numbers_test(self):
        doc = "HELLO WORLD. 1111."
        doc_right = "hello world. 1111."
        doc_new = self.parser(doc)

        assert_equal(doc_new, doc_right)

    def long_enough_sentence_test(self):

        caps = titlecaps(min_length=20)
        doc = "SENTENCE TOO SHORT"
        doc_right = "SENTENCE TOO SHORT"
        doc_new = caps(doc)

        assert_equal(doc_new, doc_right)


class Titlecaps_With_DeDash_Test:
    """ 
    Word tokenization shouldn't rely on the dash for a split in words,
    edge case found that when run together, this failed.
    """

    @classmethod
    def setup_class(cls):
        from nlpre import dedash

        cls.parser0 = titlecaps(min_length=1)
        cls.parser1 = dedash()

    def caps_before_dedash_test(self):
        doc = "THIS IS A TEST OF TREAT- MENT."
        doc_right = "this is a test of treatment."
        doc_new = self.parser1(self.parser0(doc))

        assert_equal(doc_new, doc_right)
