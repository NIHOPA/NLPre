from nose.tools import *
from word2vec_pipeline.preprocessing.pos_tokenizer import pos_tokenizer

class POS_Tokenizer_Test:
    def __init__(self):
        POS_Blacklist = set(("connector",
                     "cardinal",
                     "pronoun",
                     "adverb",
                     "symbol",
                     "verb",
                     "punctuation",
                     "modal_verb",
                     "w_word",))

        self.tokenizer = pos_tokenizer(POS_Blacklist)

    def keep_nouns_test1(self):
        doc = "The boy threw the ball into the yard"
        doc_right = "boy ball yard"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test2(self):
        doc = "So we beat on, boats against the current, borne back ceaselessly into the past"
        doc_right = "boat current past"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test3(self):
        doc = " A screaming comes across the sky. It has happened before, but there is nothing to compare it to now."
        doc_right = "sky\nnothing"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    # Buendia gets singularized to "Buendium", for some reason
    def keep_nouns_test4(self):
        doc = ("Many years later, as he faced the firing squad, was to remember that distant"
               " afternoon when his father took him to discover ice")
        doc_right = "Many year fire squad distant afternoon father ice"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)




    def keep_mesh_test(self):
        doc = "The boy threw the ball into the yard"
        doc_right = "boy ball yard"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)


    #This passes, when it shouldn't. not sure if there's any way around it
    def ambiguous_verbs_test(self):
        doc = "The boy wanted to research the ball"
        doc_right = "boy research ball"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)