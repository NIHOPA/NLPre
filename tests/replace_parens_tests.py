from nose.tools import assert_equal
from nlpre import identify_parenthetical_phrases

class Parens_Replace_Test():
    def __init__(self):
        self.phrases = identify_parenthetical_phrases()
        self.replacer = replacer()

    def acronym_in_same_doc_test(self):
        doc = "The Environmental Protection Agency (EPA) was created by Nixon. The EPA helps the environment"
        counter = self.phrases(doc)

        doc_new = self.replacer(doc, counter)
        doc_right = "The Environmental Protection Agency (EPA) was created by Nixon ." \
                    " The Environmental Protection Agency helps the environment"

        assert_equal(doc_right, doc_new)

    def acronym_in_same_doc_additional_words_test(self):
        doc = 'I love the Americans with Disabilities Act (ADA). The ADA saved my life'
        counter = self.phrases(doc)

        doc_new = self.replacer(doc, counter)

        doc_right = 'I love the Americans with Disabilities Act (ADA) .' \
                    ' The Americans with Disabilities Act saved my life'

        assert_equal(doc_new, doc_right)


    def multiple_acronyms_same_doc_test(self):
        doc = ("The Environmental Protection Agency (EPA) is not a government "
               "organization (GO) of Health and Human Services (HHS). While the EPA and HHS "
               "are both a GO, they are different agencies")

        counter = self.phrases(doc)

        doc_new = self.replacer(doc, counter)

        doc_right = ("The Environmental Protection Agency (EPA) is not a government "
               "organization (GO) of Health and Human Services (HHS) . While the Environmental Protection Agency and "
               "Health and Human Services are both a government organization , they are different agencies")

        assert_equal(doc_new, doc_right)

    def different_docs_test(self):
        doc1 = 'The Environmental Protection Agency (EPA) was created by Nixon'
        doc2 = 'The EPA helps the environment'

        counter = self.phrases(doc1)

        doc_new = self.replacer(doc2, counter)
        assert_equal(doc1, doc2)



    #Need a class to compile all individual counters
    def count_multiple_docs(self):
        doc1 = "The Environmental Protection Agency (EPA) was created by Nixon"
        doc2 = 'I love the Americans with Disabilities Act (ADA). The ADA saved my life'
        doc3 = 'We must focus on the point of care (POC). POC is very important'

        doc_replace = 'The EPA helps the environment'

        counter1 = self.phrases(doc1)
        counter2 = self.phrases(doc2)
        counter3 = self.phrases(doc3)

        return




