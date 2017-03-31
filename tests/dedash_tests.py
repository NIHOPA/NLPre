from nose.tools import *
from word2vec_pipeline.preprocessing.dedash import dedash

class Dedash_Test:
    def __init__(self):
        self.dedash = dedash()

    def single_word_dash_test(self):
        doc = "How is the treat- ment going"
        doc_right = "How is the treatment  going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def dash_not_word_test(self):
        doc = "Hello world- it feels like a good day"
        doc_right = "Hello world- it feels like a good day"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def firstword_not_alpha_test(self):
        doc = "How is the treat- 1ment going"
        doc_right = "How is the treat- 1ment going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def multiple_caps_test(self):
        doc = "How is the TReat- ment going"
        doc_right = "How is the TReat- ment going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def one_letter_word_test(self):
        doc = "I love A- Trak!"
        doc_right = "I love A- Trak!"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def no_dash_test(self):
        doc = "How is the treat ment going"
        doc_right = "How is the treat ment going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)

    def no_alpha_dash_test(self):
        doc = "How is the 1234- 567890 going"
        doc_right = "How is the 1234- 567890 going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)


    #Does this ever happen?
    def dash_no_space(self):
        doc = "How is the treat-ment going"
        doc_right = "How is the treatment  going"
        doc_new = self.dedash(doc)

        assert_equal(doc_right, doc_new)