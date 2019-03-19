from nose.tools import *
from nlpre import pos_tokenizer


class POS_Tokenizer_Test:
    @classmethod
    def setup_class(cls):

        POS_blacklist = set(
            (
                "connector",
                "cardinal",
                "pronoun",
                "adverb",
                "symbol",
                "verb",
                "adjective",
                "punctuation",
                "possessive",
                "unknown",
            )
        )

        cls.parser = pos_tokenizer(POS_blacklist)

    def keep_nouns_test1(self):
        doc = "The boy threw the ball into the yard"
        doc_right = "boy ball yard"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_nouns_test2(self):
        doc = """The haploid set of chromosomes in a gamete 
        or microorganism, or in each cell of a multicellular organism."""

        doc_right = "set chromosome microorganism cell organism"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_nouns_test3(self):
        doc = """ A screaming comes across the sky. 
        It has happened before, but there is nothing to compare it to now. """
        doc_right = "screaming sky\nnothing"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_nouns_test4(self):
        doc = """
        Many years later, as he faced the firing squad, he was to remember 
        that distant afternoon when his father took him to discover ice.
        """
        doc_right = "year firing squad afternoon father ice"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_nouns_test5(self):
        doc = """
        The sky above the port was the color of television, 
        tuned to a dead channel """
        doc_right = "sky port color television channel"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_nouns_test6(self):
        doc = """
        In my younger and more vulnerable years my father gave me some 
        advice that I've been turning over in my mind ever since"""
        doc_right = "year father advice mind"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_mesh_test(self):
        doc = "The boy MeSH_Threw the ball into the yard"
        doc_right = "boy MeSH_Threw ball yard"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def keep_phrase_test(self):
        doc = "The boy PHRASE_Threw the ball into the yard"
        doc_right = "boy PHRASE_Threw ball yard"
        doc_new = self.parser(doc)

        assert_equal(doc_right, doc_new)

    def possesive_word_test(self):
        doc = "I am Jack's complete lack of surprise"
        doc_right = "i be Jack complete lack of surprise"
        doc_new = pos_tokenizer(["possessive"])(doc)

        assert_equal(doc_right, doc_new)

    def cardinal_word_test(self):
        doc = "There are two phases."
        doc_right = "there be phase ."
        doc_new = pos_tokenizer(["cardinal"])(doc)

        assert_equal(doc_right, doc_new)

    def symbol_test(self):
        doc = """I am #1."""
        doc_right = "i be 1 ."
        doc_new = pos_tokenizer(["symbol"])(doc)

        assert_equal(doc_right, doc_new)

    def unknown_POS_test(self):
        # It's 'adjective' not 'adjectives'
        assert_raises(ValueError, pos_tokenizer, ["adjectives"])

    def implied_verb_test(self):
        # snarfed is not a real word, but we are using like a verb
        doc = "The boy snarfed the ball into the yard"
        doc_right = "the boy the ball into the yard"
        doc_new = pos_tokenizer(["verb"])(doc)
        assert_equal(doc_right, doc_new)
