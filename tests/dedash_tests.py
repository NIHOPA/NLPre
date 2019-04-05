from nose.tools import *
from nlpre.dedash import dedash


class Dedash_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = dedash()

    def single_word_dash_test(self):
        doc = "How is the treat- ment going"
        doc_right = "How is the treatment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def single_word_multi_space_dash_test(self):
        doc = "How is the treat-    \nment going"
        doc_right = "How is the treatment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_not_word_test(self):
        doc = "Hello world- it feels like a good day"
        doc_right = "Hello world- it feels like a good day"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def firstword_not_alpha_test(self):
        doc = "How is the treat- 1ment going"
        doc_right = "How is the treat- 1ment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_caps_test(self):
        doc = "How is the TReat- ment going"
        doc_right = "How is the TReatment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_caps_second_word_test(self):
        doc = "How is the treat- MEnt going"
        doc_right = "How is the treatMEnt going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def one_letter_word_test(self):
        doc = "I love A- Trak!"
        doc_right = "I love A- Trak!"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def no_dash_test(self):
        doc = "How is the treat ment going"
        doc_right = "How is the treat ment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def no_alpha_dash_test(self):
        doc = "How is the 1234- 567890 going"
        doc_right = "How is the 1234- 567890 going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_no_space_test(self):
        doc = "How is the treat-ment going"
        doc_right = "How is the treat-ment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_capitalized_word_test(self):
        doc = "How is the Treat- ment going"
        doc_right = "How is the Treatment going"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)
