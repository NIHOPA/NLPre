# -*- coding: utf-8 -*-
from nlpre import *
from nlpre.replace_acronyms import replace_acronym
import os
import codecs
from nose.tools import assert_equal
import io


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

        f_MeSH = os.path.join(
            local_dir,
            MeSH_dict,
            'MeSH_two_word_lexicon.csv')

        self.unidecoder = unidecoder()

        self.dedash = dedash()
        self.titlecaps = titlecaps()
        self.replace_from_dict = replace_from_dictionary(f_MeSH)

        self.parenthetical = identify_parenthetical_phrases()

        self.separated_parenthesis = separated_parenthesis()
        self.token_replacement = token_replacement()
        self.decaps = decaps_text()
        self.pos_tokenizer = pos_tokenizer(POS_Blacklist)

        with codecs.open(self.location + '/tests/doc1', 'r', 'utf-8') as f1:
            self.doc1 = f1.read()

        with codecs.open(self.location + '/tests/doc2', 'r', 'utf-8') as f2:
            self.doc2 = f2.read()

        self.big_counter = self.acronym_counter()

        self.replace_abbreviation = replace_acronym(self.big_counter, preprocessed=True)


        print "done"

    def full_run(self, text):
        doc = text

        ascii_doc = self.unidecoder(doc)
        dedash_doc = self.dedash(ascii_doc)
        titlecaps_doc = self.titlecaps(dedash_doc)

        counter = self.parenthetical(titlecaps_doc)
        replace_from_dict_doc = self.replace_from_dict(titlecaps_doc)
        separated_parenthesis_doc = self.separated_parenthesis(replace_from_dict_doc)
        token_replacement_doc = self.token_replacement(separated_parenthesis_doc)
        decaps_doc = self.decaps(token_replacement_doc)
        pos_tokenizer_doc = self.pos_tokenizer(decaps_doc)

        replaced_abbrv_doc = self.replace_abbreviation(pos_tokenizer_doc.text, counter)

        return replaced_abbrv_doc, counter

    def acronym_counter(self):
        doc1 = self.doc1
        doc2 = self.doc2

        counter1 = self.parenthetical(doc1)
        counter2 = self.parenthetical(doc2)

        big_counter = counter1 + counter2
        return big_counter

    def document1_test(self):
        doc = self.doc1

        with open(self.location + '/tests/doc1_right', 'r') as f:
            doc_right = f.read()

        doc_new, counter = self.full_run(doc)

        counter_nhl = counter[(('non', 'Hodgkin', 'lymphoma'), 'NHL')]
        counter_HRQOL = counter[(('health', 'related', 'quality', 'of',
                                  'life'), 'HRQOL')]

        assert_equal(doc_new, doc_right)
        assert_equal(counter_nhl, 1)
        assert_equal(counter_HRQOL, 1)

    def document2_test(self):
        doc = self.doc2
        with open(self.location + '/tests/doc2_right', 'r') as f:
            doc_right = f.read()

        doc_new, counter = self.full_run(doc)

        counter_sle = counter[(('systemic', 'lupus', 'erythematosus'), 'SLE')]

        sent1 = doc_new.split('\n')
        sent2 = doc_right.split('\n')
        for x in range(0,len(sent1)):
            assert_equal(sent1[x], sent2[x])

        assert_equal(doc_new, doc_right)
        assert_equal(counter_sle, 1)
