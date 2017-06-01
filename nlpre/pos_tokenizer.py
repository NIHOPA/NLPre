import pattern.en
from tokenizers import meta_text
import logging

_POS_shorthand = {
    "adjective": "ADJ",
    "noun": "N",
    "verb": "V",
    "modal_verb": "V",
    "adverb": "RB",
    "unknown": "UNK",
    "pronoun": "POS",
    "connector": "CC",
    "punctuation": "PUNC",
    "cardinal": "CD",
    "w_word": "WV",
    'quote': "QUOTE",
    "symbol": "SYM",
}


class pos_tokenizer(object):

    """
    Removes all words that are of a designated part-of-speech (POS) from
    a document. For example, when processing medical text, it is useful to
    remove all words that are not nouns or adjectives. POS detection is
    provided by the pattern.en.parse module. Parts of speech:

    POS = {
            "connector": ["CC", "IN", "DT", "TO", "UH", "PDT"],
            "cardinal": ["CD", "LS"],
            "adjective": ["JJ", "JJR", "JJS"],
            "noun": ["NN", "NNS", "NNP", "NNPS"],
            "pronoun": ["PRP", "PRP$", "PRO"],
            "adverb": ["RB", "RBR", "RBS", "RP"],
            "symbol": ["SYM", '$', '#'],
            "punctuation": [".", ",", ":", ')', '('],
            "modal_verb": ["MD"],
            "verb": ["VB", "VBZ", "VBP", "VBD", "VBG", "VBN"],
            "w_word": ["WDT", "WP", "WP$", "WRB", "EX"],
            "quote": ['"', "'", "``", "''"],
            "unknown": ["FW", "``"],
        }

    connectors -> conjunction, determiner, infinitival to,
                  interjection, predeterminer
    w_word     -> which, what, who, whose, when, where, there, that, ...

    """

    def __init__(self, POS_blacklist):
        """
        Initialize the parser.

        Args:
            POS_blacklist: A list of parts of speech to remove from the text.
        """
        self.logger = logging.getLogger(__name__)
        self.parse = lambda x: pattern.en.parse(x, chunks=False, tags=True)

        POS = {
            "connector": ["CC", "IN", "DT", "TO", "UH", "PDT"],
            "cardinal": ["CD", "LS"],
            "adjective": ["JJ", "JJR", "JJS"],
            "noun": ["NN", "NNS", "NNP", "NNPS"],
            "pronoun": ["PRP", "PRP$", "POS"],
            "adverb": ["RB", "RBR", "RBS", "RP"],
            "symbol": ["SYM", '$', '#'],
            "punctuation": [".", ",", ":", ')', '('],
            "modal_verb": ["MD"],
            "verb": ["VB", "VBZ", "VBP", "VBD", "VBG", "VBN"],
            "w_word": ["WDT", "WP", "WP$", "WRB", "EX"],
            "quote": ['"', "'", "``", "''"],
            "unknown": ["FW", ],
        }

        self.filtered_POS = POS_blacklist
        self.POS_map = {}
        for pos, L in POS.items():
            for y in L:
                self.POS_map[y] = pos

    def __call__(self, text, force_lemma=True):
        '''
        Runs the parser.

        Args:
            text: a string document
            force_lemma: bool, lemmitze the words prior to parsing
        Returns:
            results: A string document
        '''

        pos_tags = []
        tokens = self.parse(text)
        doc2 = []
        removedWords = []

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
                #    self.logger.info("UNKNOWN POS *{}*".format(tag))
                #    pos = "unknown"

                pos = self.POS_map[tag]

                if pos in self.filtered_POS:
                    removedWords.append(word)
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

        self.logger.info('Removed words: %s' % removedWords)

        # The number of POS tokens should match the number of word tokens
        assert(len(pos_tags) == len(doc2.split()))

        result = meta_text(doc2, POS=pos_tags)
        return result
