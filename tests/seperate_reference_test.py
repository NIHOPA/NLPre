from nose.tools import *
import pattern.en
from nlpre.seperate_reference import seperate_reference

class Footnotes_Test:
    def __init__(self):
        self.parse = lambda x: pattern.en.tokenize(
            x)

        self.footnotes = seperate_reference()

    def number_test(self):
        doc = "How is the treatment4 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def number_reference_token_test(self):
        footnotes = seperate_reference(reference_token=True)
        doc = "How is the treatment4 going. Pretty well"
        doc_right = "How is the treatment REF_4 going . Pretty well"
        doc_new = footnotes(doc)

        assert_equal(doc_right, doc_new)

    def period_test(self):
        doc = "How is the treatment4.5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def period_reference_token_test(self):
        footnotes = seperate_reference(reference_token=True)
        doc = "How is the treatment4.5 going. Pretty well"
        doc_right = "How is the treatment REF_4.5 going . Pretty well"
        doc_new = footnotes(doc)

        assert_equal(doc_right, doc_new)

    def period_one_number_test(self):
        doc = "How is the treatment.5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def dashed_word_period_one_number_test(self):
        doc = "How is the treat-ment.5 going. Pretty well"
        doc_right = "How is the treat-ment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def dash_test(self):
        doc = "How is the treatment4-5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def comma_test(self):
        doc = "How is the treatment4,5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def multiple_comma_test(self):
        doc = "How is the treatment4,5,35,24 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def period_dash_test(self):
        doc = "How is the treatment.4-5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def period_dash_reference_token_test(self):
        footnotes = seperate_reference(reference_token=True)

        doc = "How is the treatment.4-5 going. Pretty well"
        doc_right = "How is the treatment REF_.4-5 going . Pretty well"
        doc_new = footnotes(doc)

        assert_equal(doc_right, doc_new)

    def comma_dash_test(self):
        doc = "How is the treatment,4-5 going. Pretty well"
        doc_right = "How is the treatment going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def chemical_dash_test(self):
        doc = "How is the interlukin-1 going. Pretty well"
        doc_right = "How is the interlukin-1 going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def word_that_should_end_with_number_test(self):
        doc = "How is the XasdL1 going. Pretty well"
        doc_right = "How is the XasdL1 going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def word_that_begins_with_number_test(self):
        doc = "How is the 4XasdL going. Pretty well"
        doc_right = "How is the 4XasdL going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def pattern_in_middle_of_word_test(self):
        doc = "How is the CAMK2-2-dependent going. Pretty well"
        doc_right = "How is the CAMK2-2-dependent going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def non_word_with_reference_test(self):
        doc = "How is the CVD.70-73 going. Pretty well"
        doc_right = "How is the CVD going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def number_in_word_with_reference_test(self):
        doc = "How is the CV3D.70-73 going. Pretty well"
        doc_right = "How is the CV3D going . Pretty well"
        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def reference_in_parenthesis_test(self):
        doc = 'key feature in Drosophila3-5 and elegans(7).'
        doc_right = 'key feature in Drosophila and elegans .'

        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def standard_word_in_reference_in_parenthesis_test(self):
        doc = 'key feature in Drosophila3-5 and trees(7).'
        doc_right = 'key feature in Drosophila and trees .'

        doc_new = self.footnotes(doc)

        assert_equal(doc_right, doc_new)

    def standard_word_in_reference_in_parenthesis_token_test(self):
        footnotes = seperate_reference(reference_token=True)

        doc = 'key feature in Drosophila3-5 and trees(7).'
        doc_right = 'key feature in Drosophila REF_3-5 and trees REF_7 .'

        doc_new = footnotes(doc)

        assert_equal(doc_right, doc_new)