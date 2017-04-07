# -*- coding: utf-8 -*-
from nlpre import *
import os
from nose.tools import assert_equal

class Full_Test:
    def __init__(self):
        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname('doc1')))

        POS_Blacklist = set(("connector",
                             "cardinal",
                             "pronoun",
                             "adverb",
                             "symbol",
                             "verb",
                             "punctuation",
                             "modal_verb",
                             "w_word",))

        MeSH_dict = "dictionaries/"
        local_dir = os.path.dirname(os.path.abspath('nlpre/dictionaries'))

        f_MeSH = os.path.join(local_dir, MeSH_dict, 'MeSH_two_word_lexicon.csv')


        self.unidecoder = unidecoder()

        self.dedash = dedash()
        self.titlecaps = titlecaps()
        self.replace_from_dict = replace_from_dictionary(f_MeSH)

        self.parenthetical = identify_parenthetical_phrases()

        self.remove_parenthesis = remove_parenthesis()
        self.token_replacement = token_replacement()
        self.decaps = decaps_text()
        self.pos_tokenizer = pos_tokenizer(POS_Blacklist)

        with open(self.location+'/tests/doc1','r') as f:
            self.doc1 = f.read()

    def full_run(self, text):
        doc = text

        ascii_doc = self.unidecoder(doc)
        dedash_doc = self.dedash(ascii_doc)
        titlecaps_doc = self.titlecaps(dedash_doc)

        counter = self.parenthetical(titlecaps_doc)

        replace_from_dict_doc = self.replace_from_dict(titlecaps_doc)
        remove_parenthesis_doc = self.remove_parenthesis(replace_from_dict_doc)
        token_replacement_doc = self.token_replacement(remove_parenthesis_doc)
        decaps_doc = self.decaps(token_replacement_doc)
        pos_tokenizer_doc = self.pos_tokenizer(decaps_doc)

        return pos_tokenizer_doc, counter

    def document1_test(self):
        doc = self.doc1

        with open(self.location+'/tests/doc1_right', 'r') as f:
            doc_right = f.read()

        doc_new, counter = self.full_run(doc)

        counter_nhl = counter[(('non', 'Hodgkin', 'lymphoma'), 'NHL')]
        counter_HRQOL = counter[(('health', 'related', 'quality', 'of',
                                  'life'),'HRQOL')]

        split1 = doc_new.text.split('\n')
        split2 = doc_right.split('\n')


        #assert_equal(doc_new.text, doc_right)
        assert_equal(counter_nhl, 1)
        assert_equal(counter_HRQOL, 1)