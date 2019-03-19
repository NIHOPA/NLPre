# -*- coding: utf-8 -*-
from nose.tools import assert_equal
from nlpre import url_replacement


class Unidecoder_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = url_replacement()
        cls.parser_with_email = url_replacement(email_replacement="EMAIL")
        cls.parser_with_url = url_replacement(url_replacement="URL")

    def HTTP_link_test(self):
        doc = u"Source code is http://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def HTTPS_link_test(self):
        doc = u"Source code is https://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def www_link_test(self):
        doc = u"Source code is www.github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def ftp_link_test(self):
        doc = u"Source code is ftp.github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def parens_around_link_test(self):
        doc = u"Source code is [(www.github.com/NIHOPA/NLPre/)] here."
        doc_right = u"Source code is [()] here."
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def HTTP_link_replacement_test(self):
        doc = u"Source code is http://github.com/NIHOPA/NLPre/ here."
        doc_right = u"Source code is URL here."
        doc_new = self.parser_with_url(doc)
        assert_equal(doc_right, doc_new)

    def www_edu_link_test(self):
        doc = u"Learned everything I know at www.github.edu."
        doc_right = u"Learned everything I know at URL."
        doc_new = self.parser_with_url(doc)
        assert_equal(doc_right, doc_new)

    def www_email_test(self):
        doc = u"This NLPre test was written by travis.hoppe@gmail.com"
        doc_right = u"This NLPre test was written by "
        doc_new = self.parser(doc)
        assert_equal(doc_right, doc_new)

    def www_email_replace_test(self):
        doc = u"This NLPre test was written by travis.hoppe@gmail.com"
        doc_right = u"This NLPre test was written by EMAIL"
        doc_new = self.parser_with_email(doc)
        assert_equal(doc_right, doc_new)
