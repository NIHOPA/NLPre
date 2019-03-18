from nose.tools import *
from nlpre import separated_parenthesis
from nlpre.separated_parenthesis import remove_trailing_space


class Separated_Parenthesis_Tests:
    @classmethod
    def setup_class(cls):
        cls.parser = separated_parenthesis(min_keep_length=0)

    def single_parenthesis_pair_test(self):
        doc = "hello (hello world1) world2."
        doc_right = "hello world2.\nhello world1."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_brackets_pair_test(self):
        doc = "hello [world1] world2."
        doc_right = "hello world2.\nworld1."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_pair_test(self):
        doc = "hello {world1} world2."
        doc_right = "hello world2.\nworld1."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_brackets_pair_test(self):
        doc = "Hello [and goodbye [no really]] everybody."
        doc_right = "Hello everybody.\nand goodbye.\nno really."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_curly_pair_test(self):
        doc = "Hello {and goodbye {no really}} everybody."
        doc_right = "Hello everybody.\nand goodbye.\nno really."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_test(self):
        doc = "Hello (and goodbye (no really)) everybody."
        doc_right = "Hello everybody.\nand goodbye.\nno really."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_expand_test(self):
        doc = "The boy and his ((really) big) dog."
        doc_right = "The boy and his dog.\nbig.\nreally."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_multiple_inner_pair_test(self):
        doc = "The boy and his ((really) big (like really big)) dog."
        doc_right = "The boy and his dog.\nbig.\nreally.\nlike really big."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    # Code tests are not working at the moment
    def single_parenthesis_test(self):
        doc = "hello (one two (three) four five."
        doc_right = "hello one two three four five."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_bracket_test(self):
        doc = "hello [world1 world2."
        doc_right = "hello world1 world2."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_test(self):
        doc = "hello {world1 world2."
        doc_right = "hello world1 world2."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def unbalanced_parenthesis_test(self):
        doc = "hello (((one) two) three."
        doc_right = "hello one two three."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_sentence_parens_test(self):
        doc = "hello world. (It is a beautiful day.) Goodbye world."
        doc_right = "hello world.\nIt is a beautiful day.\nGoodbye world."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def empty_parens_test(self):
        doc = "Hello () world."
        doc_right = "Hello world."
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_parens_single_sentence_test(self):
        doc = "Hello world. (Good Evening)(goodbye)"
        doc_right = "Hello world.\nGood Evening.\ngoodbye."
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def clipped_sentences_test(self):
        doc = "Sunday (the best day) is a day of the week."

        parser1 = separated_parenthesis(min_keep_length=None)
        parser2 = separated_parenthesis(min_keep_length=2)
        parser3 = separated_parenthesis(min_keep_length=5)

        doc2 = "Sunday is a day of the week.\nthe best day."
        doc3 = "Sunday is a day of the week."

        assert_equals(parser1(doc), doc2)
        assert_equals(parser2(doc), doc2)
        assert_equals(parser3(doc), doc3)

    def mixed_parens_with_punctuation_test(self):
        doc = "Superoxide anion (A[B?])."
        doc_right = "Superoxide anion.\nA[B?]."
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def mixed_parens_with_punctuation_expanded_test(self):
        doc = "These chemicals are (really really) great. Superoxide anion (A[B?])."
        doc_right = "These chemicals are great.\nreally really.\nSuperoxide anion.\nA[B?]."
        doc_new = self.parser(doc)
        assert_equals(doc_right, doc_new)

    def remove_trailing_space_with_small_n_test(self):
        # Make sure we get back what we put in
        doc = "x"
        doc_right = doc
        doc_new = remove_trailing_space(doc)

        assert_equals(doc_right, doc_new)

    # def two_parenthesis_with_punctuation_test(self):
    #    doc = 'Superoxide anion (A(B).).'
    #    doc_right = 'Superoxide anion .\nA .\nB ?'
    #    doc_new = self.parser(doc)
    #
    #    assert_equals(doc_right, doc_new)

    # def mixed_types_period_test(self):
    #    doc = 'hello world. (It {is a} beautiful day.) Goodbye world.'
    #    doc_right = 'hello world .\nIt  beautiful day .\nis a .\nGoodbye world .'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    # def mixed_types_no_period_test(self):
    #    doc = 'hello world (It {is a} beautiful day) goodbye world.'
    #    doc_right = 'hello world goodbye world .\nIt beautiful day .\nis a .'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    # def mixed_types_unbalanced_test(self):
    #    doc = 'hello world. (It {is a} beautiful day. Goodbye world.'
    #    doc_right = 'hello world .\nIt  beautiful day .\nis a .\nGoodbye world .'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    # Code doesn't account for multiple sentences within a parenthesis
    # I'm not sure when this case will be encountered, unless we're parsing DFW novels
    # def multisentence_paranthesis_test(self):
    #    doc = 'hello (hello world1. Goodnight moon) world2.'
    #    doc_right = 'hello world2 .\nhello world1 .\nGoodnight moon'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    # def multisentence_bracket_test(self):
    #    doc = 'hello [world. Goodnight moon] world'
    #    doc_right = 'hello world'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    # def multisentence_curly_test(self):
    #    doc = 'hello {world. Goodnight moon} world'
    #    doc_right = 'hello world'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)
