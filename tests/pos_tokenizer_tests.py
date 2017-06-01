from nose.tools import *
from nlpre import pos_tokenizer


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

    def keep_nouns_test4(self):
        doc = ("Many years later, as he faced the firing squad, he was to remember that distant"
               " afternoon when his father took him to discover ice")
        doc_right = "Many year fire squad distant afternoon father ice"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test5(self):
        doc = "The sky above the port was the color of television, tuned to a dead channel"
        doc_right = "sky port color television dead channel"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_nouns_test6(self):
        doc = ("In my younger and more vulnerable years my father gave me some advice that I've been "
               "turning over in my mind ever since")
        doc_right = "younger vulnerable year father advice mind"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_mesh_test(self):
        doc = "The boy MeSH_Threw the ball into the yard"
        doc_right = "boy MeSH_Threw ball yard"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def keep_phrase_test(self):
        doc = "The boy PHRASE_Threw the ball into the yard"
        doc_right = "boy PHRASE_Threw ball yard"
        doc_new = self.tokenizer(doc)

        assert_equal(doc_right, doc_new.text)

    def possesive_word_test(self):
        doc = "I am Jack's complete lack of surprise"
        doc_right = "be jack complete lack of surprise"
        doc_new = pos_tokenizer(["pronoun"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def cardinal_word_test(self):
        doc = "There are two phases."
        doc_right = "There be phase ."
        doc_new = pos_tokenizer(["cardinal"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def w_word_test(self):
        doc = "Transcriptions that are observed."
        doc_right = "Transcription be observe ."
        doc_new = pos_tokenizer(["w_word"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def quoted_word_test(self):
        doc = '''We find the answer is "not quite".'''
        doc_right = "We find the answer be not quite ."
        doc_new = pos_tokenizer(["quote"])(doc)
        
        assert_equal(doc_right, doc_new.text)

    def symbol_test(self):
        doc = '''I am #1.'''
        doc_right = "I be 1 ."
        doc_new = pos_tokenizer(["symbol"])(doc)
        
        assert_equal(doc_right, doc_new.text)    

    # def unknown_word_test(self):
    #    doc = 'The boy akjf45!naf the ball into the yard'
    #    doc_right = 'boy akjfnaf ball yard'
    #    doc_new = self.tokenizer(doc)
    #    assert_equal(doc_right, doc_new.text)
