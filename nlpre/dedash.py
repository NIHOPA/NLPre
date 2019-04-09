# -*- coding: utf-8 -*-
import nlpre
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Token


class dedash:
    """
    When importing documents, words are occasionally split apart and
    separated by a dash. For instance, "treatment" might be imported as
    "treat- ment". This class detects these splits and returns a version of
    the document with the words corrected.

    Standalone dedasher.
    """

    def __init__(self):
        # Build an empty tokenizer
        self.nlp = spacy.blank("en")

        # Add the custom pipe
        parser = dedash_spaCy(self.nlp)
        self.nlp.add_pipe(parser)

    def __call__(self, text):
        return self.nlp(text).text


class dedash_spaCy:

    name = "identify_dedash_tokens"

    def __init__(self, nlp):

        # Match to a word split with a dash. Like ex- ample.
        pattern = [
            {"TEXT": {"REGEX": r"^[a-zA-Z]+[\-]$"}},
            {"IS_SPACE": True, "OP": "*"},
            {"TEXT": {"REGEX": "^[a-zA-Z]+$"}},
        ]

        self.blank_nlp = spacy.blank("en")

        # Add the pattern to parser
        Token.set_extension("merge_dash", default=False, force=True)

        self.matcher = Matcher(nlp.vocab)
        self.matcher.add("dedash", None, pattern)

        self.load_vocab()

    def load_vocab(self):
        # Load a set of english words
        f_wordlist = nlpre.dictionary.wordlist_english
        self.vocab = set()

        with open(f_wordlist) as FIN:
            for word in FIN:
                self.vocab.add(word.strip().lower())

    def requires_merge(self, tokens):
        # Checks if the document will require a merge
        return any([x._.merge_dash for x in tokens])

    def __call__(self, doc):

        matches = self.matcher(doc)
        spans = []

        for _, start, end in matches:
            phrase = doc[start:end]

            # Examine the lowercase word w/o the dash
            word = phrase[0].text.lower().strip()[:-1]
            word += phrase[-1].text.lower().strip()

            # If the word doesn't match our wordlist, move on
            if word not in self.vocab:
                continue

            for token in phrase:
                token._.set("merge_dash", True)

            spans.append(phrase)

        # If we didn't find anything, return the document
        if not spans:
            return doc

        # Merge the tokens together
        for span in spans:
            span.merge()

        # Build a new document after merging
        text_new = []
        for token in doc:

            text = token.text_with_ws
            if token._.merge_dash:
                left, right = text.split()
                text = left[:-1] + right + token.whitespace_
            text_new.append(text)

        # Retokenize the document, but skip the identify step
        doc = self.blank_nlp("".join(text_new))

        return doc
