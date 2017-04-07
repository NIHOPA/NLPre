# -*- coding: utf-8 -*-
from nlpre import *
import os
from nose.tools import assert_equal

class Full_Test:
    def __init__(self):
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

        self.doc1 = "TITLE: UNMET NEEDS OF NON-HODGKIN LYMPHOMA SURVIVORS IN" \
                    " KOREA: PREVALENCE, CORRELATES, AND ASSOCIATIONS WITH" \
                    " HEALTH-RELATED QUALITY OF LIFE." \
                    " OBJECTIVE: We aimed to describe the prevalence and" \
                    " correlates of unmet needs among non-Hodgkin lymphoma" \
                    " (NHL) surv- ivors in Korea and to identify their" \
                    " association with health-related quality of life" \
                    " (HRQOL). METHODS: Participants were 826 NHL survivors" \
                    " from three hospitals in South Korea diagnosed at" \
                    " least 24 months prior to participating (mean, 6.3" \
                    " years; range, 2.1-20.9 years). We used self-reported" \
                    " questionnaires, including the Need Scale for Cancer" \
                    " Patients Undergoing Follow-up Care (NS-C) developed" \
                    " in Korea and the EORTC QLQ-C30. We defined an unmet" \
                    " need as a moderate to high level of unmet need in the" \
                    " NS-C response scale. RESULTS: Among six domains, unmet" \
                    " need prevalence ranged from 1.7% to 38.3%. Most" \
                    " commonl- y reported domains with unmet needs were" \
                    " 'treatment and prognosis' (38.3%) and 'keeping mind" \
                    " under control' (30.5%). The three most frequently" \
                    " reported individual unmet needs were 'being informed" \
                    " about prevention of recurrence' (50.7%), 'being" \
                    " informed about prevention of metastasis' (49.7%), and" \
                    " 'having self-confidence of overcoming cancer'" \
                    " (42.7%). Multivariate logistic analyses revealed" \
                    " that younger age, being unm- arried, and low monthly" \
                    " income were associated with unmet needs of multiple" \
                    " domains. Participants with unmet needs demonstrated" \
                    " significantly poorer HRQOL, and the most clinically" \
                    " meaningful differences were found in social function" \
                    " and emotional function. CONCLUSIONS: Korean NHL" \
                    " survivors have substantial unmet needs, especially" \
                    " those who are younger, unmarried, and have a lower" \
                    " income. Initiating supportive care programs for" \
                    " meeting unmet needs may enhance their HRQOL." \
                    " Copyright 2016 John Wiley & Sons, Ltd."
        # ©

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

        doc_right = "title unmet need Lymphoma_Non-Hodgkin survivor" \
                    " korea prevalence correlate association" \
                    " health-related Quality_of_Life\n" \
                    "OBJECTIVE prevalence" \
                    " correlate unmet need Lymphoma_Non-Hodgkin" \
                    " survivor korea" \
                    " association health-related Quality_of_Life" \
                    "\nNHL HRQOL METHOD participant NHL survivor" \
                    " hospital Republic_of_Korea least" \
                    " month\nmean year range year questionnaire need scale cancer" \
                    " patient follow-up" \
                    " korea EORTC QLQ-C30\nNS-C unmet" \
                    " need moderate high level unmet need" \
                    " NS-C response scale\nresult domain unmet" \
                    " need prevalence percent percent\ndomain unmet need" \
                    " treatment prognosi mind control\npercent percent" \
                    " individual unmet need" \
                    " prevention recurrence prevention metastasi" \
                    " self-confidence cancer\npercent percent percent" \
                    " multivariate logistic analysis" \
                    " younger age unmarried low monthly" \
                    " income unmet need multiple domain\nparticipant unmet" \
                    " need poorer HRQOL meaningful difference social function" \
                    " emotional function\nCONCLUSION NHL" \
                    " survivor substantial unmet need" \
                    " younger unmarried lower income\nsupportive care program" \
                    " meet unmet need HRQOL\ncopyright john wiley son ltd"

        doc_new, counter = self.full_run(doc)

        counter_nhl = counter[(('non', 'Hodgkin', 'lymphoma'), 'NHL')]
        counter_HRQOL = counter[(('health', 'related', 'quality', 'of',
                                  'life'),'HRQOL')]

        split1 = doc_new.text.split()
        split2 = doc_right.split()

        #for x in range(len(split1)):
        #    assert_equal(split1[x],split2[x])

        assert_equal(doc_new.text, doc_right)