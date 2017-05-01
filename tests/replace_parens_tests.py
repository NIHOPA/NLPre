from nose.tools import assert_equal
from nlpre import identify_parenthetical_phrases
from nlpre.replace_acronyms import Replace_Acronym

class Parens_Replace_Test():
    def __init__(self):
        self.phrases = identify_parenthetical_phrases()
        #self.replacer = Replace_Acronym()

    def acronym_in_same_doc_test(self):
        doc = "The Environmental Protection Agency (EPA) was created by Nixon. The EPA helps the environment"
        counter = self.phrases(doc)

        replacer = Replace_Acronym(counter)
        doc_new = replacer(doc)
        doc_right = "The Environmental Protection Agency ( Environmental Protection Agency ) was created by Nixon .\n" \
                    "The Environmental Protection Agency helps the environment"

        assert_equal(doc_right, doc_new)

    def acronym_in_same_doc_additional_words_test(self):
        doc = 'I love the Americans with Disabilities Act (ADA). The ADA saved my life'
        counter = self.phrases(doc)

        replacer = Replace_Acronym(counter)
        doc_new = replacer(doc)

        doc_right = 'I love the Americans with Disabilities Act ( Americans with Disabilities Act ) .\n' \
                    'The Americans with Disabilities Act saved my life'

        assert_equal(doc_new, doc_right)


    def multiple_acronyms_same_doc_test(self):
        doc = ("The Environmental Protection Agency (EPA) is not a government "
               "organization (GO) of Health and Human Services (HHS). While the EPA and HHS "
               "are both a GO, they are different agencies")

        counter = self.phrases(doc)

        replacer = Replace_Acronym(counter)
        doc_new = replacer(doc)

        doc_right = ("The Environmental Protection Agency ( Environmental Protection Agency ) is not a government "
               "organization ( government organization ) of Health and Human Services ( Health and Human Services ) .\nWhile the Environmental Protection Agency and "
               "Health and Human Services are both a government organization , they are different agencies")

        assert_equal(doc_new, doc_right)

    def different_docs_test(self):
        doc1 = 'The Environmental Protection Agency (EPA) was created by Nixon'
        doc2 = 'The EPA helps the environment'

        doc_right = 'The Environmental Protection Agency helps the environment'

        counter = self.phrases(doc1)

        replacer = Replace_Acronym(counter)
        doc_new = replacer(doc2)
        assert_equal(doc_new, doc_right)

    def duplicate_acronyms_test(self):
        doc1 = 'The Environmental Protection Agency (EPA) was created by Nixon. ' \
               'The Environmental Protection Agency (EPA) loves the tress. ' \
               'The less well known Elephant Protection Agency (EPA) does ' \
               'important work as well.'

        doc2 = 'The EPA helps the environment'

        doc_right = 'The Environmental Protection Agency helps the environment'

        counter = self.phrases(doc1)

        replacer = Replace_Acronym(counter)
        doc_new = replacer(doc2)
        assert_equal(doc_new, doc_right)


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







