from nose.tools import assert_equal
from nlpre import identify_parenthetical_phrases


class Parenthetical_Phrases_Tests:
    @classmethod
    def setup_class(cls):
        cls.parser = identify_parenthetical_phrases()

    def OD_of_the_not_included_test(self):
        doc = "The Office of the Director (OD) is the best"
        counter = self.parser(doc)
        counter_od = counter[(("Office", "of", "the", "Director"), "OD")]
        assert_equal(counter_od, 1)

    def EPA_test(self):
        doc = "The Environmental Protection Agency (EPA) was created by Nixon"
        counter = self.parser(doc)
        counter_epa = counter[
            (("Environmental", "Protection", "Agency"), "EPA")
        ]
        assert_equal(counter_epa, 1)

    def EPA_multiple_words_in_parans_test(self):
        doc = "The Environmental Protection Agency (the EPA, founded in 1970) was created by Nixon"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def EPA_multiple_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) was created by Nixon "
            "who loved the Environmental Protection Agency (EPA)"
        )
        counter = self.parser(doc)
        counter_epa = counter[
            (("Environmental", "Protection", "Agency"), "EPA")
        ]
        assert_equal(counter_epa, 2)

    def EPA_nestedParans_test(self):
        doc = "The Environmental Protection Agency ((EPA)) was created by Nixon"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def EPA_nestedParans2_test(self):
        doc = "The Environmental Protection Agency ((EPA) is the abbreviation) was created by Nixon"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def EPA_curly_test(self):
        doc = "The Environmental Protection Agency {EPA} was created by Nixon"
        counter = self.parser(doc)
        counter_epa = counter[
            (("Environmental", "Protection", "Agency"), "EPA")
        ]
        assert_equal(counter_epa, 1)

    def EPA_bracket_test(self):
        doc = "The Environmental Protection Agency [EPA] was created by Nixon"
        counter = self.parser(doc)
        counter_epa = counter[
            (("Environmental", "Protection", "Agency"), "EPA")
        ]
        assert_equal(counter_epa, 1)

    def EPA_lowercase_test(self):
        doc = "The Environmental Protection Agency (epa) was created by Nixon"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def single_letter_test(self):
        doc = "The Environment (E) is beautiful"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def HHS_and_not_included_test(self):
        doc = (
            "A B C D E F G H I and Health and Human Services (HHS) is important"
        )
        counter = self.parser(doc)
        counter_hhs = counter[(("Health", "and", "Human", "Services"), "HHS")]
        assert_equal(counter_hhs, 1)

    def HHS_incomplete_phrase_test(self):
        doc = "A B C D E F G H I and and Human Services (HHS) is important"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def EPA_incomplete_phrase_test(self):
        doc = "Protection Agency (EPA) is incomplete"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def EPA_incomplete_phrase2_test(self):
        doc = "(EPA) is incomplete"
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def HHS_and_included_test(self):
        doc = "A B C D E F G H I and Health and Human Services (HaHS) is important"
        counter = self.parser(doc)
        counter_hhs = counter[(("Health", "and", "Human", "Services"), "HaHS")]
        assert_equal(counter_hhs, 1)

    def BIA_of_not_included_test(self):
        doc = "I love the Bureau of Indian Affairs (BIA)"
        counter = self.parser(doc)
        counter_bia = counter[(("Bureau", "of", "Indian", "Affairs"), "BIA")]
        assert_equal(counter_bia, 1)

    def ADA_with_not_included_test(self):
        doc = "I love the Americans with Disabilities Act (ADA)"
        counter = self.parser(doc)
        counter_ada = counter[
            (("Americans", "with", "Disabilities", "Act"), "ADA")
        ]
        assert_equal(counter_ada, 1)

    def CADE_for_not_included_test(self):
        doc = "I love the Center for Acute Disease Epidemiology (CADE)"
        counter = self.parser(doc)
        counter_cade = counter[
            (("Center", "for", "Acute", "Disease", "Epidemiology"), "CADE")
        ]
        assert_equal(counter_cade, 1)

    # def CDC_for_and_not_included_test(self):
    #    doc = 'I love the Centers for Disease Control and Prevention (CDC)'
    #    counter = self.parser(doc)
    #    counter_cdc = counter[(('Centers', 'for', 'Disease', 'Control', 'and', 'Prevention'), 'CDC')]
    #    assert_equal(counter_cdc, 1)

    # def CMS_ampersand_words_not_in_abr_test(self):
    #    doc = "The Centers for Medicare & Medicaid Services (CMS) is great"
    #    counter = self.parser(doc)
    #    counter_cms = counter[(('Centers', 'for', 'Medicare', '&', 'Medicaid', 'Services'), 'CMS')]
    #    assert_equal(counter_cms, 1)

    def HHS_comma_test(self):
        doc = "Health, Human Services (HHS) is a good agency"
        counter = self.parser(doc)
        counter_hhs = counter[
            (("Health,", "Human", "Services"), "HHS")
        ]  # health has comma
        assert_equal(counter_hhs, 1)

    def POC_of_included_test(self):
        doc = "We must focus on the point of care (POC)"
        counter = self.parser(doc)
        counter_poc = counter[(("point", "of", "care"), "POC")]
        assert_equal(counter_poc, 1)

    def ASDs_plural_test(self):
        doc = "autism spectrum disorders (ASDs) are stressful"
        counter = self.parser(doc)
        counter_asds = counter[(("autism", "spectrum", "disorders"), "ASDs")]
        assert_equal(counter_asds, 1)

    def eQTLs_multiple_lower_case_test(self):
        doc = "I love quantitative train loci (eQTLs)"
        counter = self.parser(doc)
        counter_eqtls = counter[(("quantitative", "train", "loci"), "eQTLs")]
        assert_equal(counter_eqtls, 1)

    def C5aR_letter_test(self):
        doc = "I love my C5a receptor (C5aR)"
        counter = self.parser(doc)
        counter_C5aR = counter[(("C5a", "receptor"), "C5aR")]
        assert_equal(counter_C5aR, 1)

    def AFB_dash_test(self):
        doc = "I hate acid-fast bacillus (AFB)"
        counter = self.parser(doc)
        counter_afb = counter[(("acid", "fast", "bacillus"), "AFB")]
        assert_equal(counter_afb, 1)

    # def GERD_word_has_multiple_letters_in_abbreviation_test(self):
    #    doc = 'I hate gastroesophageal reflux disease (GERD)'
    #    counter = self.parser(doc)
    #    counter_gerd = counter[(('gastroesophageal', 'reflux', 'disease'), 'GERD')]
    #    assert_equal(counter_gerd, 1)

    def SOCE_plus_sign_test(self):
        doc = "I want a store operated Ca2+ entry (SOCE)"
        counter = self.parser(doc)
        counter_soce = counter[(("store", "operated", "Ca2+", "entry"), "SOCE")]
        assert_equal(counter_soce, 1)

    def epa_od_hhs_test(self):
        doc = (
            "The Environmental Protection Agency (EPA) is not a government "
            "organization (GO) of Health and Human Services (HHS)."
        )

        counter = self.parser(doc)
        counter_epa = counter[
            (("Environmental", "Protection", "Agency"), "EPA")
        ]
        counter_go = counter[(("government", "organization"), "GO")]
        counter_hhs = counter[(("Health", "and", "Human", "Services"), "HHS")]

        assert_equal(counter_epa, 1)
        assert_equal(counter_go, 1)
        assert_equal(counter_hhs, 1)

    def bad_doc_test(self):
        doc = ""
        counter = self.parser(doc)
        assert_equal(len(counter), 0)

    def parser_error_with_two_mismatches(self):
        # Bugfix: Prior version would crash on this input string.

        # This test doesn't parse acronym's correctly. However, it should
        # not crash

        doc = (
            "A large region upstream ( ~ 30 kb ) of GATA 4. "
            "Small interfering RNA (siRNA) mediated depletion of EZH2."
        )
        counter = self.parser(doc)

        # replacer = replace_acronyms(counter, prefix='ABBR', underscore=True)
        # doc_new = replacer(doc)

        # doc_right = 'A large region upstream ( ~ 30 kb ) of GATA 4 .\n' \
        #      'Small interfering RNA ( siRNA ) mediated depletion of EZH2 .'

        # assert_equal(doc_new, doc_right)

    def iterating_over_parenthesis_crash_test(self):
        # This test doesn't parse acronym's correctly. However, it should
        # not crash
        doc = (
            "In Drosophila, the CK2 kinase phosphorylates and destabilizes"
            " the PERIOD (PER) and TIMELESS (TIM) proteins, which inhibit "
            "CLOCK (CLK) transcriptional activity."
        )

        counter = self.parser(doc)
