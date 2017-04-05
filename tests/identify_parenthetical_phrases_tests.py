from nose.tools import assert_equal
from nlpre import identify_parenthetical_phrases

class Parenthetical_Phrases_Tests():
    def __init__(self):
        self.phrases = identify_parenthetical_phrases()

    def EPA_test(self):
        doc = "The Environmental Protection Agency (EPA) was created by Nixon"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        assert_equal(counter_epa, 1)

    def EPA_multiple_test(self):
        doc = ("The Environmental Protection Agency (EPA) was created by Nixon "
               "who loved the Environmental Protection Agency (EPA)")
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        assert_equal(counter_epa, 2)

    def EPA_nestedParans_test(self):
        doc = "The Environmental Protection Agency ((EPA)) was created by Nixon"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        assert_equal(counter_epa, 0)

    def EPA_curly_test(self):
        doc = "The Environmental Protection Agency {EPA} was created by Nixon"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        assert_equal(counter_epa, 1)

    def EPA_bracket_test(self):
        doc = "The Environmental Protection Agency [EPA] was created by Nixon"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        assert_equal(counter_epa, 1)

    def EPA_lowercase_test(self):
        doc = "The Environmental Protection Agency (epa) was created by Nixon"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'epa')]
        assert_equal(counter_epa, 0)

    def single_letter_test(self):
        doc = "The Environment (E) is beautiful"
        counter = self.phrases(doc)
        counter_epa = counter[(('Environment'), 'E')]
        assert_equal(counter_epa, 0)

    def HHS_and_not_included_test(self):
        doc = 'A B C D E F G H I and Health and Human Services (HHS) is important'
        counter = self.phrases(doc)
        counter_hhs = counter[(('Health', 'and', 'Human', 'Services'), 'HHS')]
        assert_equal(counter_hhs, 1)

    def HHS_and_included_test(self):
        doc = 'A B C D E F G H I and Health and Human Services (HaHS) is important'
        counter = self.phrases(doc)
        counter_hhs = counter[(('Health', 'and', 'Human', 'Services'), 'HaHS')]
        assert_equal(counter_hhs, 1)

    def BIA_of_not_included_test(self):
        doc = 'I love the Bureau of Indian Affairs (BIA)'
        counter = self.phrases(doc)
        counter_bia = counter[(('Bureau', 'of', 'Indian', 'Affairs'), 'BIA')]
        assert_equal(counter_bia, 1)

    def ADA_with_not_included_test(self):
        doc = 'I love the Americans with Disabilities Act (ADA)'
        counter = self.phrases(doc)
        counter_ada = counter[(('Americans', 'with', 'Disabilities', 'Act'), 'ADA')]
        assert_equal(counter_ada, 1)

    def CADE_for_not_included_test(self):
        doc = 'I love the Center for Acute Disease Epidemiology (CADE)'
        counter = self.phrases(doc)
        counter_cade = counter[(('Center', 'for', 'Acute', 'Disease', 'Epidemiology'), 'CADE')]
        assert_equal(counter_cade, 1)

    #def CDC_for_and_not_included_test(self):
    #    doc = 'I love the Centers for Disease Control and Prevention (CDC)'
    #    counter = self.phrases(doc)
    #    counter_cdc = counter[(('Centers', 'for', 'Disease', 'Control', 'and', 'Prevention'), 'CDC')]
    #    assert_equal(counter_cdc, 1)

    #def CMS_ampersand_words_not_in_abr_test(self):
    #    doc = "The Centers for Medicare & Medicaid Services (CMS) is great"
    #    counter = self.phrases(doc)
    #    counter_cms = counter[(('Centers', 'for', 'Medicare', '&', 'Medicaid', 'Services'), 'CMS')]
    #    assert_equal(counter_cms, 1)

    def HHS_comma_test(self):
        doc = 'Health, Human Services (HHS) is a good agency'
        counter = self.phrases(doc)
        counter_hhs = counter[(('Health,', 'Human', 'Services'), 'HHS')]   #health has comma
        assert_equal(counter_hhs, 1)

    def POC_of_included_test(self):
        doc = 'We must focus on the point of care (POC)'
        counter = self.phrases(doc)
        counter_poc = counter[(('point', 'of', 'care'), 'POC')]
        assert_equal(counter_poc, 1)

    def ASDs_plural_test(self):
        doc = 'autism spectrum disorders (ASDs) are stressful'
        counter = self.phrases(doc)
        counter_asds = counter[(('autism', 'spectrum', 'disorders'), 'ASDs')]
        assert_equal(counter_asds, 1)

    def eQTLs_multiple_lower_case_test(self):
        doc = 'I love quantitative train loci (eQTLs)'
        counter = self.phrases(doc)
        counter_eqtls = counter[(('quantitative', 'train', 'loci'), 'eQTLs')]
        assert_equal(counter_eqtls, 1)

    def C5aR_letter_test(self):
        doc = 'I love my C5a receptor (C5aR)'
        counter = self.phrases(doc)
        counter_C5aR = counter[(('C5a', 'receptor'), 'C5aR')]
        assert_equal(counter_C5aR, 1)

    def AFB_dash_test(self):
        doc = 'I hate acid-fast bacillus (AFB)'
        counter = self.phrases(doc)
        counter_afb = counter[(('acid', 'fast', 'bacillus'), 'AFB')]
        assert_equal(counter_afb, 1)

    #def GERD_word_has_multiple_letters_in_abbreviation_test(self):
    #    doc = 'I hate gastroesophageal reflux disease (GERD)'
    #    counter = self.phrases(doc)
    #    counter_gerd = counter[(('gastroesophageal', 'reflux', 'disease'), 'GERD')]
    #    assert_equal(counter_gerd, 1)

    def SOCE_plus_sign_test(self):
        doc = 'I want a store operated Ca2+ entry (SOCE)'
        counter = self.phrases(doc)
        counter_soce = counter[(('store', 'operated', 'Ca2+', 'entry'), 'SOCE')]
        assert_equal(counter_soce, 1)

    def epa_od_hhs_test(self):
        doc = ("The Environmental Protection Agency (EPA) is not a government "
            "organization (GO) of Health and Human Services (HHS).")

        counter = self.phrases(doc)
        counter_epa = counter[(('Environmental', 'Protection', 'Agency'), 'EPA')]
        counter_go = counter[(('government', 'organization'), 'GO')]
        counter_hhs = counter[(('Health', 'and', 'Human', 'Services'), 'HHS')]

        assert_equal(counter_epa, 1)
        assert_equal(counter_go, 1)
        assert_equal(counter_hhs, 1)
