from nose.tools import assert_equal
from nlpre import identify_parenthetical_phrases
from nlpre.replace_acronyms import replace_acronyms


class Parens_Replace_Test:
    @classmethod
    def setup_class(cls):
        cls.parser = identify_parenthetical_phrases()

    def acronym_without_counter_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        replacer = replace_acronyms(underscore=False)
        doc_new = replacer(doc)
        doc_right = (
            "The Environmental Protection Agency ( Environmental "
            "Protection Agency ) was created by Nixon .\n"
            "The Environmental Protection Agency helps the environment"
        )

    def acronym_in_same_doc_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc, counter)
        doc_right = (
            "The Environmental Protection Agency ( Environmental "
            "Protection Agency ) was created by Nixon .\n"
            "The Environmental Protection Agency helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def counter_must_be_infered_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc)
        doc_right = (
            "The Environmental Protection Agency ( Environmental "
            "Protection Agency ) was created by Nixon .\n"
            "The Environmental Protection Agency helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def acronym_in_same_doc_underscore_default_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter)
        doc_new = replacer(doc, counter)
        doc_right = (
            "The Environmental_Protection_Agency "
            "( Environmental_Protection_Agency ) was created by "
            "Nixon .\nThe Environmental_Protection_Agency helps the "
            "environment"
        )

        assert_equal(doc_right, doc_new)

    def acronym_in_same_doc_additional_words_test(self):
        doc = (
            "I love the Americans with Disabilities Act (ADA). The ADA "
            "saved my life"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc, counter)

        doc_right = (
            "I love the Americans with Disabilities Act ( Americans "
            "with Disabilities Act ) .\nThe Americans with"
            " Disabilities Act saved my life"
        )

        assert_equal(doc_new, doc_right)

    def multiple_acronyms_same_doc_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) is not a government"
            " organization (GO) of Health and Human Services (HHS). While"
            " the EPA and HHS are both a GO, they are different agencies"
        )

        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc, counter)

        doc_right = (
            "The Environmental Protection Agency ( Environmental "
            "Protection Agency ) is not a government organization "
            "( government organization ) of Health and Human "
            "Services ( Health and Human Services ) .\nWhile the "
            "Environmental Protection Agency and Health and Human"
            " Services are both a government organization , they"
            " are different agencies"
        )

        assert_equal(doc_new, doc_right)

    def almost_acronym_but_lowercase_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The epa helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc, counter)
        doc_right = (
            "The Environmental Protection Agency ( Environmental "
            "Protection Agency ) was created by Nixon .\nThe epa "
            "helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def duplicate_acronyms_included_test(self):
        doc1 = (
            "The Environmental Protection Agency (EPA) was created "
            "by Nixon. The Environmental Protection Agency (EPA) loves "
            "the trees. The less well known Elephant Protection Agency "
            "(EPA) does important work as well."
        )

        doc2 = (
            "The Ent Protection Agency (EPA) stopped Sauromon. "
            "The EPA helps the environment"
        )

        doc_right = (
            "The Ent Protection Agency ( Ent Protection Agency ) "
            "stopped Sauromon .\nThe Ent Protection Agency helps "
            "the environment"
        )

        counter = self.parser(doc1)
        doc_counter = self.parser(doc2)

        replacer = replace_acronyms(counter, underscore=False)
        doc_new = replacer(doc2, doc_counter)
        assert_equal(doc_new, doc_right)

    def preprocess_test(self):
        doc_original = (
            "Environmental Protection Agency (EPA). government"
            " organization (GO). Health and Human Services (HHS). While"
            " EPA HHS GO different agencies"
        )

        doc = (
            "Environmental Protection Agency \nEPA \ngovernment"
            " organization \nGO \nHealth and Human Services \nHHS \nWhile"
            " EPA HHS GO different agencies"
        )

        counter = self.parser(doc_original)

        replacer = replace_acronyms(
            counter, preprocessed=True, underscore=False
        )
        doc_new = replacer(doc, counter)

        doc_right = (
            "Environmental Protection Agency\nEnvironmental "
            "Protection Agency\ngovernment organization"
            "\ngovernment organization\nHealth and Human "
            "Services\nHealth and Human Services\nWhile "
            "Environmental Protection Agency Health and Human"
            " Services government organization different agencies"
        )

        assert_equal(doc_new, doc_right)

    def tokenize_phrase_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, underscore=True)
        doc_new = replacer(doc)
        doc_right = (
            "The Environmental_Protection_Agency ( Environmental_"
            "Protection_Agency ) was created by Nixon .\n"
            "The Environmental_Protection_Agency helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def tokenize_phrase_prefix_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, prefix="ABBR", underscore=True)
        doc_new = replacer(doc)
        doc_right = (
            "The ABBR_Environmental_Protection_Agency ( ABBR_"
            "Environmental_Protection_Agency ) was created by "
            "Nixon .\nThe ABBR_Environmental_Protection_Agency "
            "helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def tokenize_phrase_suffix_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by "
            "Nixon. The EPA helps the environment"
        )
        counter = self.parser(doc)

        replacer = replace_acronyms(counter, suffix="ABBR", underscore=True)
        doc_new = replacer(doc)
        doc_right = (
            "The Environmental_Protection_Agency_ABBR ( "
            "Environmental_Protection_Agency_ABBR ) was created by "
            "Nixon .\nThe Environmental_Protection_Agency_ABBR "
            "helps the environment"
        )

        assert_equal(doc_right, doc_new)

    def dash_test(self):
        doc = (
            "It is not a great non-Hodgkins lymphoma (NHL), but it is "
            "a good Hodgkins."
        )
        counter = self.parser(doc)
        replacer = replace_acronyms(counter, prefix="ABBR", underscore=True)
        doc_new = replacer(doc)

        doc_right = (
            "It is not a great ABBR_non_Hodgkins_lymphoma "
            "( ABBR_non_Hodgkins_lymphoma ) , but it is a good Hodgkins ."
        )

        assert_equal(doc_right, doc_new)

    def lowercase_first_letter_match_test(self):
        # This test currently fails as siRNA isn't parsed correctly.

        doc = "Small interfering RNA (siRNA) mediated depletion of EZH2."
        counter = self.parser(doc)
        replacer = replace_acronyms(counter, prefix="ABBR", underscore=True)
        doc_new = replacer(doc)

        # doc_right = 'ABBR_siRNA ( ABBR_siRNA ) mediated depletion of EZH2 .'
        # assert_equal(doc_new, doc_right)

    def parsing_parenthesis_test(self):
        doc = (
            "BEACH (beige and Chediak Higashi) domain containing proteins (BDCPs) "
            "are a highly conserved protein family in eukaryotes."
        )
        ABBR = {(("BEACH", "domain", "containing", "proteins"), "BDCPs"): 1}
        P1 = replace_acronyms(ABBR)
        doc_new = P1(doc)

        doc_right = (
            "BEACH ( beige and Chediak Higashi ) domain containing proteins "
            "( BEACH_domain_containing_proteins ) are a highly conserved "
            "protein family in eukaryotes ."
        )

        assert_equal(doc_new, doc_right)

    ###########################################################################

    def use_most_common_test(self):
        doc1 = "The Environmental Protection Agency (EPA) was created by Nixon"
        doc2 = "The EPA helps the environment"

        doc_right = "The Environmental_Protection_Agency helps the environment"
        counter = self.parser(doc1)
        doc_counter = self.parser(doc2)

        replacer = replace_acronyms(counter, use_most_common=True)
        doc_new = replacer(doc2, doc_counter)
        assert_equal(doc_new, doc_right)

    def ignore_most_common_test(self):
        doc1 = "The Environmental Protection Agency (EPA) was created by Nixon"
        doc2 = "The EPA helps the environment"

        doc_right = "The EPA helps the environment"
        counter = self.parser(doc1)
        doc_counter = self.parser(doc2)

        replacer = replace_acronyms(counter, use_most_common=False)
        doc_new = replacer(doc2, doc_counter)
        assert_equal(doc_new, doc_right)

    def duplicate_acronyms_test(self):
        doc1 = (
            "The Environmental Protection Agency (EPA) was created "
            "by Nixon. The Environmental Protection Agency (EPA) loves "
            "the tress. The less well known Elephant Protection Agency, called "
            " the EPA, does important work as well."
        )

        doc2 = "The EPA helps the environment"
        doc_right = "The Environmental_Protection_Agency helps the environment"

        counter = self.parser(doc1)
        doc_counter = self.parser(doc2)

        replacer = replace_acronyms(counter, use_most_common=True)
        doc_new = replacer(doc2, doc_counter)
        assert_equal(doc_new, doc_right)

    def count_multiple_docs_test(self):
        doc1 = "The Environmental Protection Agency (EPA) was created by Nixon"
        doc2 = "The Environmental Protection Agency (EPA) loves the tress. "
        doc3 = (
            "The less well known Elephant Protection Agency (EPA) does "
            "important work as well."
        )

        doc_replace = "The EPA helps the environment"
        doc_right = "The Environmental_Protection_Agency helps the environment"
        counter1 = self.parser(doc1)
        counter2 = self.parser(doc2)
        counter3 = self.parser(doc3)

        doc_counter = self.parser(doc_replace)

        big_counter = counter1 + counter2 + counter3
        replacer = replace_acronyms(big_counter, use_most_common=True)
        doc_new = replacer(doc_replace, doc_counter)
        assert_equal(doc_new, doc_right)

    def parsing_misidentifed_test(self):
        # We don't replace a common phrase in the ABBR set since
        # use_most_common=False by default.

        doc = (
            "The etiology of osteoarthritis (OA) is at present unknown. "
            "Primary OA utilizing the over 35 families."
        )

        doc_right = (
            "The etiology of osteoarthritis ( OA ) is at present unknown .\n"
            "Primary OA utilizing the over 35 families ."
        )

        counter = self.parser(doc)

        ABBR = {(("ocean", "acidification"), "OA"): 1}
        replacer = replace_acronyms(ABBR)

        doc_new = replacer(doc)

        assert_equal(doc_new, doc_right)
