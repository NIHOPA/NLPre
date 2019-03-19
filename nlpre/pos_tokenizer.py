import logging
from . import nlp


class pos_tokenizer(object):

    """
    Removes all words that are of a designated part-of-speech (POS) from
    a document. For example, when processing medical text, it is useful to
    remove all words that are not nouns or adjectives. POS detection is
    provided the spaCy module. Parts of speech that can be added
    to the blacklist.

        "noun": ["NOUN", "PROPN"],
        "pronoun": ["PRON"],
        "verb": ["VERB"],
        "adjective": ["ADJ"],
        "punctuation": ["PUNCT", ],
        "possessive": ["PART", ],
        "symbol": ["SYM", "SPACE"],
        "cardinal": ["NUM"],
        "connector": ["DET", "CONJ", "CCONJ", "ADP", "INTJ"],
        "adverb": ["ADV", "PART"],
        "unknown": ["X", ""],

    """

    def __init__(self, POS_blacklist):
        """
        Initialize the parser.

        Args:
            POS_blacklist: A list of parts of speech to remove from the text.

        Allowed forms of POS

        "noun": ["NOUN", "PROPN"],
        "pronoun": ["PRON"],
        "verb": ["VERB"],
        "adjective": ["ADJ"],
        "punctuation": ["PUNCT", ],
        "possessive": ["PART", ],
        "symbol": ["SYM", "SPACE"],
        "cardinal": ["NUM"],
        "connector": ["DET", "CONJ", "CCONJ", "ADP", "INTJ"],
        "adverb": ["ADV", "PART"],
        "unknown": ["X", ""],
        """
        self.logger = logging.getLogger(__name__)

        POS = {
            "noun": ["NOUN", "PROPN"],
            "pronoun": ["PRON"],
            "verb": ["VERB"],
            "adjective": ["ADJ"],
            "punctuation": ["PUNCT"],
            "possessive": ["PART"],
            "symbol": ["SYM", "SPACE"],
            "cardinal": ["NUM"],
            "connector": ["DET", "CONJ", "CCONJ", "ADP", "INTJ"],
            "adverb": ["ADV", "PART"],
            "unknown": ["X", ""],
        }

        # Verify all POS in the blacklist are known
        self.POS_blacklist = set()

        for name in POS_blacklist:
            msg = (
                "Part-of-speech %s unknown. " % name,
                "Use one of %s." % list(POS.keys()),
            )

            if name not in POS:
                self.logger.error(msg)
                raise ValueError(msg)

            self.POS_blacklist.update(POS[name])

    def _keep_root(self, token, word_order=0):
        # If it's the first word, keep any other letters are capped
        # Otherwise, keep if any letters are capped.
        shape = token.shape_
        if word_order == 0:
            shape = shape[1:]
        return "X" in shape

    def __call__(self, text, use_base=True):
        """
        Runs the parser.

        Args:
            text: a string document
            use_base: return the base form for the matched words not in
                      the POS blacklist.
        Returns:
            results: A string document
        """

        text = " ".join(text.strip().split())
        special_words = set(["PHRASE_", "MeSH_"])

        doc = []
        for sent in nlp(text).sents:
            sent_tokens = []
            for k, token in enumerate(sent):

                # If we have a special word, add it without modification
                if any(sw in token.text for sw in special_words):
                    sent_tokens.append(token.text)
                    continue

                if token.pos_ in self.POS_blacklist:
                    continue

                word = token.text

                if (
                    use_base
                    and not self._keep_root(token, k)
                    and token.pos_ != "PRON"
                ):

                    word = token.lemma_

                # If the word is a pronoun, we need to use the base form, see
                # https://github.com/explosion/spaCy/issues/962
                if token.lemma_ == "-PRON-":
                    word = token.text.lower()

                sent_tokens.append(word)

            doc.append(" ".join(sent_tokens))
        doc = "\n".join(doc)
        return doc
