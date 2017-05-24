from nose.tools import *
from nlpre import separated_parenthesis


class Separated_Parenthesis_Tests():

    def __init__(self):
        self.parser = separated_parenthesis()

    def single_parenthesis_pair_test(self):
        doc = 'hello (hello world1) world2.'
        doc_right = 'hello world2 .\nhello world1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_brackets_pair_test(self):
        doc = 'hello [world1] world2.'
        doc_right = 'hello world2 .\nworld1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_pair_test(self):
        doc = 'hello {world1} world2.'
        doc_right = 'hello world2 .\nworld1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_brackets_pair_test(self):
        doc = 'hello [hello [world1] world2] world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_curly_pair_test(self):
        doc = 'hello {hello {world1} world2} world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_test(self):
        doc = 'hello (hello (world1) world2) world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_expand_test(self):
        doc = 'Ad Ba Ca (Da Ed Ff (Ga Ha) In) Jo. Ka Le.'
        doc_right = 'Ad Ba Ca Jo .\nDa Ed Ff In .\nGa Ha .\nKa Le .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_multiple_inner_pair_test(self):
        doc = 'Ad Ba Ca (Da (Ed Xa) Ff (Ga Ha) In) Jo. Ka Le.'
        doc_right = 'Ad Ba Ca Jo .\nDa Ff In .\nEd Xa .\nGa Ha .\nKa Le .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    # Code tests are not working at the moment
    def single_parenthesis_test(self):
        doc = 'hello (world1 (world2) one two.'
        doc_right = 'hello world1 world2 one two .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_bracket_test(self):
        doc = 'hello [world1 world2.'
        doc_right = 'hello world1 world2 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_test(self):
        doc = 'hello {world1 world2.'
        doc_right = 'hello world1 world2 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def unbalanced_parenthesis_test(self):
        doc = 'hello (((world1) world2) world3.'
        doc_right = 'hello world1 world2 world3 .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def single_sentance_parens_test(self):
        doc = 'hello world. (It is a beautiful day.) Goodbye world.'
        doc_right = 'hello world .\nIt is a beautiful day .\nGoodbye world .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def empty_parens_test(self):
        doc = 'Hello () world.'
        doc_right = 'Hello world .'
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def multiple_parens_single_sentence_test(self):
        doc = "Hello world. (Good Evening)(goodbye)"
        doc_right = "Hello world .\nGood Evening .\ngoodbye ."
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def travis_example_two_parenthesis_test(self):
        doc = 'Superoxide anion (A(B?)).'
        doc_right = 'Superoxide anion .\nA .\nB ? .'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def travis_example_test(self):
        doc = 'Superoxide anion (A[B?]).'
        doc_right = 'Superoxide anion AB ?\n.'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    def travis_example_bigger_sentence_test(self):
        doc = 'These chemicals are great. Superoxide anion (A[B?]).'
        doc_right = 'These chemicals are great .\nSuperoxide anion AB ?\n.'
        doc_new = self.parser(doc)

        assert_equals(doc_right, doc_new)

    #def mixed_types_period_test(self):
    #    doc = 'hello world. (It {is a} beautiful day.) Goodbye world.'
    #    doc_right = 'hello world .\nIt  beautiful day .\nis a .\nGoodbye world .'
    #    doc_new = self.parser(doc)

    #    assert_equals(doc_right, doc_new)

    #def mixed_types_no_period_test(self):
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
    #def multisentence_paranthesis_test(self):
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
