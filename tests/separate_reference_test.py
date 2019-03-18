from nose.tools import *
from nlpre.separate_reference import separate_reference


class References_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = separate_reference()
        cls.parser_with_ref = separate_reference(reference_token=True)

    def number_test(self):
        doc = "How is the treatment4 going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def number_in_parenthesis_test(self):
        doc = "How is (the treatment4) going. Pretty well"
        doc_right = "How is (the treatment) going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def number_with_letter_test(self):
        doc = "How is the treatment4a going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def number_with_multiple_letter_test(self):
        doc = "How is the treatment4a,b going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def number_reference_token_test(self):
        doc = "How is the treatment4 going. Pretty well"
        doc_right = "How is the treatment REF_4 going. Pretty well"
        doc_new = self.parser_with_ref(doc)

        assert_equal(doc_right, doc_new)

    def reference_in_parenthesis_test(self):
        doc = "key feature in Drosophila3-5 and elegans(7)."
        doc_right = "key feature in Drosophila and elegans."

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def parenthetical_reference_in_parenthesis_test(self):
        doc = "key feature in (Drosophila3-5 and elegans(7))."
        doc_right = "key feature in (Drosophila and elegans)."

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def parenthetical_reference_in_parenthesis_tokens_test(self):
        # BROKEN
        doc = "key feature in (Drosophila3-5 and elegans(7))."
        doc_right = "key feature in (Drosophila REF_3-5 and elegans REF_7)."
        doc_new = self.parser_with_ref(doc)

        assert_equal(doc_right, doc_new)

    def standard_word_in_reference_in_parenthesis_test(self):
        doc = "key feature in Drosophila3-5 and trees(7)."
        doc_right = "key feature in Drosophila and trees."

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def standard_word_in_reference_in_parenthesis_token_test(self):
        doc = "key feature in Drosophila3-5 and trees(7)."
        doc_right = "key feature in Drosophila REF_3-5 and trees REF_7."

        doc_new = self.parser_with_ref(doc)

        assert_equal(doc_right, doc_new)

    def parenthesis_with_dashes_test(self):
        doc = "key feature in Drosophila3-5 and trees(7-11)."
        doc_right = "key feature in Drosophila and trees."

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def parenthesis_with_dashes_period_test(self):
        doc = "key feature in Drosophila3-5 and trees.(7-11) its super helpful."
        doc_right = "key feature in Drosophila and trees. its super helpful."

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def parenthesis_with_dashes_period_token_test(self):
        doc = "key feature in Drosophila3-5 and trees.(7-11) its super helpful."
        doc_right = "key feature in Drosophila REF_3-5 and trees REF_7-11. its super helpful."

        doc_new = self.parser_with_ref(doc)

        assert_equal(doc_right, doc_new)

    def bracket_test(self):
        doc = (
            "There are at least eight distinct types of modifications found "
            "on histones (see the legend box on the top left of the "
            "figure). Enzymes have been identified for acetylation,[2] "
            "methylation,[3] demethylation,[4] phosphorylation,[5] "
            "ubiquitination,[6] sumoylation,[7] ADP-ribosylation,[8] "
            "deimination,[9][10] and proline isomerization.[11]"
        )

        doc_right = (
            "There are at least eight distinct types of "
            "modifications found on histones (see the legend box on "
            "the top left of the figure). Enzymes have been "
            "identified for acetylation, methylation, "
            "demethylation, phosphorylation, ubiquitination, "
            "sumoylation, ADP-ribosylation, "
            "deimination, and proline isomerization."
        )

        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def word_that_begins_with_number_parenthetical_reference_test(self):
        doc = "How is the 4XasdL(5) going. Pretty well"
        doc_right = "How is the 4XasdL going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def period_one_number_test(self):
        doc = "How is the treatment.5 pretty well"
        doc_right = "How is the treatment. pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def period_one_number_in_parens_test(self):
        doc = "How is (the treatment.5) pretty well"
        doc_right = "How is (the treatment.) pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dashed_word_period_one_number_test(self):
        doc = "How is the treat-ment.5 pretty well"
        doc_right = "How is the treat-ment. pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_with_letters_period_test(self):
        doc = "How is the treatment.4a-5 Pretty well"
        doc_right = "How is the treatment. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def period_dash_test(self):
        doc = "How is the treatment.4-5 pretty well"
        doc_right = "How is the treatment. pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def period_dash_reference_token_test(self):
        doc = "How is the treatment going.4-5 Pretty well"
        doc_right = "How is the treatment going. REF_4-5 Pretty well"
        doc_new = self.parser_with_ref(doc)

        assert_equal(doc_right, doc_new)

    def comma_dash_test(self):
        doc = "How is the treatment,4-5 my man"
        doc_right = "How is the treatment, my man"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_test(self):
        doc = "How is the treatment4-5 going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def dash_with_letters_test(self):
        doc = "How is the treatment4a-5 going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def comma_test(self):
        doc = "How is the treatment4,5 going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_comma_test(self):
        doc = "How is the treatment4,5,35,24 going. Pretty well"
        doc_right = "How is the treatment going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_comma_in_parens_test(self):
        doc = "How is (the treatment4,5,35,24) going. Pretty well"
        doc_right = "How is (the treatment) going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def chemical_dash_test(self):
        doc = "How is the interlukin-1 going. Pretty well"
        doc_right = "How is the interlukin-1 going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def word_that_should_end_with_number_test(self):
        doc = "How is the XasdL1 going. Pretty well"
        doc_right = "How is the XasdL1 going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def word_that_begins_with_number_test(self):
        doc = "How is the 4XasdL going. Pretty well"
        doc_right = "How is the 4XasdL going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def pattern_in_middle_of_word_test(self):
        doc = "How is the CAMK2-2-dependent going. Pretty well"
        doc_right = "How is the CAMK2-2-dependent going. Pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def non_word_with_reference_test(self):
        doc = "How is the CVD.70-73 pretty well"
        doc_right = "How is the CVD. pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def number_in_word_with_reference_test(self):
        doc = "How is the CV3D.70-73 pretty well"
        doc_right = "How is the CV3D. pretty well"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def single_letter_false_positive_test(self):
        doc = "In section A.3 we see that apple's are healthy"
        doc_right = "In section A.3 we see that apple's are healthy"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)
