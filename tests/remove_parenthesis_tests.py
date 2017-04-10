from nose.tools import *
from nlpre import remove_parenthesis


class Remove_Parenthesis_Tests():
    def __init__(self):
        self.remove = remove_parenthesis()

    def single_parenthesis_pair_test(self):
        doc = 'hello (hello world1) world2.'
        doc_right = 'hello world2 .\nhello world1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_brackets_pair_test(self):
        doc = 'hello [world1] world2.'
        doc_right = 'hello world2 .\nworld1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_pair_test(self):
        doc = 'hello {world1} world2.'
        doc_right = 'hello world2 .\nworld1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multiple_brackets_pair_test(self):
        doc = 'hello [hello [world1] world2] world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multiple_curly_pair_test(self):
        doc = 'hello {hello {world1} world2} world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_test(self):
        doc = 'hello (hello (world1) world2) world3.'
        doc_right = 'hello world3 .\nhello world2 .\nworld1 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)


    def multiple_parenthesis_pair_expand_test(self):
        doc = 'Ad Ba Ca (Da Ed Ff (Ga Ha) In) Jo. Ka Le.'
        doc_right = 'Ad Ba Ca Jo .\nDa Ed Ff In .\nGa Ha .\nKa Le .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)
    
    def multiple_parenthesis_multiple_inner_pair_test(self):
        doc = 'Ad Ba Ca (Da (Ed Xa) Ff (Ga Ha) In) Jo. Ka Le.'
        doc_right = 'Ad Ba Ca Jo .\nDa Ff In .\nEd Xa .\nGa Ha .\nKa Le .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    # Code tests are not working at the moment
    def single_parenthesis_test(self):
        doc = 'hello (world1 (world2) one two.'
        doc_right = 'hello world1 world2 one two .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_bracket_test(self):
        doc = 'hello [world1 world2.'
        doc_right = 'hello world1 world2 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_test(self):
        doc = 'hello {world1 world2.'
        doc_right = 'hello world1 world2 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def unbalanced_parenthesis_test(self):
        doc = 'hello (((world1) world2) world3.'
        doc_right = 'hello world1 world2 world3 .'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    # Code doesn't account for multiple sentences within a parenthesis
    # I'm not sure when this case will be encountered, unless we're parsing DFW novels
    # def multisentence_paranthesis_test(self):
    #    doc = 'hello (hello world1. Goodnight moon) world2.'
    #    doc_right = 'hello world2 .\nhello world1 .\nGoodnight moon'
    #    doc_new = self.remove(doc)

    #    assert_equals(doc_right, doc_new)

    #def multisentence_bracket_test(self):
    #    doc = 'hello [world. Goodnight moon] world'
    #    doc_right = 'hello world'
    #    doc_new = self.remove(doc)

    #    assert_equals(doc_right, doc_new)

    #def multisentence_curly_test(self):
    #    doc = 'hello {world. Goodnight moon} world'
    #    doc_right = 'hello world'
    #    doc_new = self.remove(doc)

    #    assert_equals(doc_right, doc_new)
