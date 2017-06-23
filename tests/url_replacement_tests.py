# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from nlpre import url_replacement


class Unidecoder_Test:

    @classmethod
    def setup_class(cls):
        cls.parser = url_replacement()
        cls.parser_with_prefix = url_replacement(prefix="LINK")

    def HTTP_link_test_test(self):
        doc = u"Source code is http://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is  here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def HTTPS_link_test_test(self):
        doc = u"Source code is https://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is  here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def www_link_test_test(self):
        doc = u"Source code is www.github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is  here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def ftp_link_test_test(self):
        doc = u"Source code is ftp.github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is  here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def parens_around_link_test_test(self):
        doc = u"Source code is [(www.github.com/NIHOPA/NLPre/)] here."
        doc_right = u"Source code is [()] here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def HTTP_link_replacement_test_test(self):
        doc = u"Source code is http://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is LINK here."
        doc_new = self.parser_with_prefix(doc)
        assert_equal(doc_right, doc_new)

    def www_edu_link_test_test(self):
        doc = u"Learned everything I know at www.github.edu."
        doc_right = u"Learned everything I know at LINK."
        doc_new = self.parser_with_prefix(doc)
        assert_equal(doc_right, doc_new)
