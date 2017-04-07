import pattern.en
from tokenizers import meta_text

_POS_shorthand = {
    "adjective": "ADJ",
    "noun": "N",
    "verb": "V",
    "modal_verb": "V",
    "adverb": "RB",
    "unknown": "UNK",
}


class pos_tokenizer(object):
    """
    Args:
        text: a string document
        
    Returns:
        Removes all words that are not nouns or adjectives from a document. This uses
        pattern.en to identify each word's POS.
    """

    def __init__(self, POS_blacklist):
        '''
        Uses pattern.en to remove POS terms on the blacklist
        '''

        self.parse = lambda x: pattern.en.parse(x, chunks=False, tags=True)

        # connectors = conjunction,determiner,infinitival to,
        #              interjection,predeterminer
        # w_word = which, what, who, whose, when, where & there ...

        POS = {
            "connector": ["CC", "IN", "DT", "TO", "UH", "PDT"],
            "cardinal": ["CD", "LS"],
            "adjective": ["JJ", "JJR", "JJS"],
            "noun": ["NN", "NNS", "NNP", "NNPS"],
            "pronoun": ["PRP", "PRP$"],
            "adverb": ["RB", "RBR", "RBS", "RP"],
            "symbol": ["SYM", '$', ],
            "punctuation": [".", ",", ":", ')', '('],
            "modal_verb": ["MD"],
            "verb": ["VB", "VBZ", "VBP", "VBD", "VBG", "VBN"],
            "w_word": ["WDT", "WP", "WP$", "WRB", "EX"],
            "unknown": ["FW", "``"],
        }

        self.filtered_POS = POS_blacklist

        '''
                set(("connector",
                     "cardinal",
                     "pronoun",
                     "adverb",
                     "symbol",
                     "verb",
                     "punctuation",
                     "modal_verb",
                     "w_word",))
        '''

        self.POS_map = {}
        for pos, L in POS.items():
            for y in L:
                self.POS_map[y] = pos

    def __call__(self, doc, force_lemma=True):

        pos_tags = []
        tokens = self.parse(doc)
        doc2 = []

        for sentence in tokens.split():
            sent2 = []

            for word, tag in sentence:

                if "PHRASE_" in word:
                    sent2.append(word)
                    pos_tags.append(_POS_shorthand["noun"])
                    continue

                if "MeSH_" in word:
                    sent2.append(word)
                    pos_tags.append(_POS_shorthand["noun"])
                    continue

                tag = tag.split('|')[0].split('-')[0].split("&")[0]

                # try:
                #    pos = self.POS_map[tag]
                # except BaseException:
                #    print("UNKNOWN POS *{}*".format(tag))
                #    pos = "unknown"
                pos = self.POS_map[tag]

                if pos in self.filtered_POS:
                    continue

                word = pattern.en.singularize(word, pos)

                if pos == "verb" or force_lemma:
                    lem = pattern.en.lemma(word, parse=False)
                    if lem is not None:
                        word = lem

                sent2.append(word)
                pos_tags.append(_POS_shorthand[pos])

            doc2.append(' '.join(sent2))

        doc2 = '\n'.join(doc2)

        # The number of POS tokens should match the number of word tokens
        assert(len(pos_tags) == len(doc2.split()))

        result = meta_text(doc2, POS=pos_tags)
        return result
