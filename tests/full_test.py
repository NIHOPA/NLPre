# -*- coding: utf-8 -*-
import nlpre
from nlpre import *
import os
import codecs
from collections import Counter
from nose.tools import assert_equal
import io


class Full_Test:
    def __init__(self):
        self.location = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname("doc1"))
        )

        POS_Blacklist = set(
            (
                "connector",
                "cardinal",
                "pronoun",
                "adverb",
                "symbol",
                "verb",
                "punctuation",
                "possessive",
                "unknown",
            )
        )

        f_MeSH = nlpre.dictionary.MeSH

        with codecs.open(self.location + "/tests/doc1", "r", "utf-8") as f1:
            self.doc1 = f1.read()

        with codecs.open(self.location + "/tests/doc2", "r", "utf-8") as f2:
            self.doc2 = f2.read()

        self.parenthetical = identify_parenthetical_phrases()
        self.shared_counter = self.acronym_counter(self.doc1, self.doc2)

        self.parsers0 = [
            unidecoder(),
            titlecaps(),
            dedash(),
            decaps_text(),
            replace_acronyms(
                self.shared_counter, prefix="ABBR", preprocessed=False
            ),
            replace_from_dictionary(f_MeSH),
            separated_parenthesis(),
            separate_reference(),
            pos_tokenizer(POS_Blacklist),
            token_replacement(remove=True),
        ]

    def full_run(self, text):

        for clf in self.parsers0:
            text = clf(text)

        return text

    def acronym_counter(self, *docs):
        return sum((self.parenthetical(text) for text in docs), Counter())

    def document1_test(self):
        doc = self.doc1

        with open(self.location + "/tests/doc1_right", "r") as f:
            doc_right = f.read()

        doc_new = self.full_run(doc)

        self.check_line_by_line(doc_new, doc_right)
        assert_equal(doc_new, doc_right)

    def document2_test(self):
        doc = self.doc2
        with open(self.location + "/tests/doc2_right", "r") as f:
            doc_right = f.read()

        doc_new = self.full_run(doc)

        self.check_line_by_line(doc_new, doc_right)
        assert_equal(doc_new, doc_right)

    def check_line_by_line(self, docA, docB):
        docA = docA.split("\n")
        docB = docB.split("\n")

        for x in range(len(docA)):
            assert_equal(docA[x], docB[x])


if __name__ == "__main__":
    tester = Full_Test()

    test_number = 2

    if test_number == 1:
        doc = tester.doc1
    elif test_number == 2:
        doc = tester.doc2

    with open(tester.location + f"/tests/doc{test_number}_right", "r") as f:
        doc_right = f.read()

    doc_new = tester.full_run(doc)

    print(doc_new)
