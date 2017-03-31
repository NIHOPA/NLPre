from word2vec_pipeline.preprocessing.token_replacement import token_replacement
from nose.tools import *

# I'm not sure how ampersand's are typically used in the literature, but the replacement adds spaces to it



class Token_Test:
    def __init__(self):
        self.token_replacer = token_replacement()

    def ampersand_test(self):
        doc = "I like cats&dogs"
        doc_right = "I like cats and dogs"
        doc_new = self.token_replacer(doc)
        assert_equal(doc_new, doc_right)

    def percent_test(self):
        doc = "Working at 100% efficiency"
        doc_new = self.token_replacer(doc)
        doc_right = "Working at 100 percent  efficiency"
        assert_equal(doc_new, doc_right)

    def greater_test(self):
        doc = "dogs>cats"
        doc_new = self.token_replacer(doc)
        doc_right = "dogs greater-than cats"
        assert_equal(doc_new, doc_right)

    def less_test(self):
        doc = "cats<dogs"
        doc_new = self.token_replacer(doc)
        doc_right = "cats less-than dogs"
        assert_equal(doc_new, doc_right)

    def equal_test(self):
        doc = "dogs=dogs"
        doc_new = self.token_replacer(doc)
        doc_right = "dogs equals dogs"
        assert_equal(doc_new, doc_right)

    def pound_test(self):
        doc = "press the # key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    def tilde_test(self):
        doc = "press the ~ key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    def forwardslash_test(self):
        doc = "press the / key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    def backslash_test(self):
        doc = "press the \\ key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    def line_test(self):
        doc = "press the | key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    def dollar_test(self):
        doc = "press the $ key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the  key"
        assert_equal(doc_new, doc_right)

    def colon_test(self):
        doc = "press the : key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the key"
        assert_equal(doc_new, doc_right)

    def doubledash_test(self):
        doc = "press the -- key"
        doc_new = self.token_replacer(doc)
        doc_right = "press the   key"
        assert_equal(doc_new, doc_right)

    #I think the code on this one is wrong. it only replaces 's if it's surrounded by spaces
    def possesivesplit_test(self):
        doc = "what 's up doc?"
        doc_new = self.token_replacer(doc)
        doc_right = "what up doc?"
        assert_equal(doc_new, doc_right)

    def singlequote_test(self):
        doc = "'hello' he said"
        doc_new = self.token_replacer(doc)
        doc_right = "hello he said"
        assert_equal(doc_new, doc_right)

    def doublequote_test(self):
        doc = "\"hello\" he said"
        doc_new = self.token_replacer(doc)
        doc_right = "hello he said"
        assert_equal(doc_new, doc_right)
