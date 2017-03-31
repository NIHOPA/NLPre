from nose.tools import *
from word2vec_pipeline.preprocessing.remove_parenthesis import remove_parenthesis


class Remove_Parenthesis_Tests():
    def __init__(self):
        self.remove = remove_parenthesis()

    def single_parenthesis_pair_test(self):
        doc = 'hello (world) world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_brackets_pair_test(self):
        doc = 'hello [world] world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_pair_test(self):
        doc = 'hello {world} world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)


    def multiple_brackets_pair_test(self):
        doc = 'hello [[world] world] world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multiple_curly_pair_test(self):
        doc = 'hello {{world} world} world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multiple_parenthesis_pair_test(self):
        doc = 'hello ((world) world) world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)


    def single_parenthesis_test(self):
        doc = 'hello (world world'
        doc_right = 'hello world world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_bracket_test(self):
        doc = 'hello [world world'
        doc_right = 'hello world world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def single_curly_test(self):
        doc = 'hello {world world'
        doc_right = 'hello world world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def unbalanced_parenthesis_test(self):
        doc = 'hello (((world) world) world'
        doc_right = 'hello world world world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)


    # Code doesn't account for multiple sentances within a parenthesis
    # I'm not sure when this case will be encountered, unless we're parsing DFW novels
    def multisentance_paranthesis_test(self):
        doc = 'hello (world. Goodnight moon) world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multisentance_bracket_test(self):
        doc = 'hello [world. Goodnight moon] world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)

    def multisentance_curly_test(self):
        doc = 'hello {world. Goodnight moon} world'
        doc_right = 'hello world'
        doc_new = self.remove(doc)

        assert_equals(doc_right, doc_new)
