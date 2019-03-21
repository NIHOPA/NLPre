import nlpre
import spacy
from spacy.matcher import Matcher
from spacy.tokens import Span, Token, Doc


class dedash:

    def __init__(self):

        # Build an empty tokenizer
        self.nlp = spacy.blank('en')

        # Match to a word split with a dash. Like ex- ample.
        pattern = [
            {"TEXT": {"REGEX": "^[a-zA-Z]+[\-]$"}},
            {"SPACE": True, "OP": "*"},
            {"TEXT": {"REGEX": "^[a-zA-Z]+"}},
        ]

        # Add the pattern to parser
        Token.set_extension('merge_dash', default=False)
        Doc.set_extension('requires_merge', getter=self.requires_merge)
        
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add("dedash", self.match_event, pattern)

        self.load_vocab()

    def load_vocab(self):
        # Load a set of english words
        f_wordlist = nlpre.dictionary.wordlist_english
        self.vocab = set()
        
        with open(f_wordlist) as FIN:
            for word in FIN:
                self.vocab.add(word.strip().lower())

    
    def match_event(self, matcher, doc, i, matches):
        # NOTE TO SELF, have to MERGE THEM AT ONCE
        # otherwise indices go a kilter
        
        # Extract the phrase we matched to
        match_id, start, end = matches[i]

        print("MATCHING", [x for x in doc], start, end)
        #print(doc[start:end])
        #exit()
        phrase = Span(doc, start, end)

        # Examine the lowercase word w/o the dash
        word  = phrase[0].text.lower().strip()[:-1]
        word += phrase[-1].text.lower().strip()

        # If the word doesn't match our wordlist, move on
        if word not in self.vocab:
            return

        # If so, tag the word as a custom attribute
        with doc.retokenize() as retokenizer:
            attrs = {"_": {'merge_dash': True}}
            retokenizer.merge(phrase, attrs=attrs)

    def requires_merge(self, tokens):
        # Checks if the document will require a merge
        return any([x._.merge_dash for x in tokens])

    def __call__(self, text):
        doc = self.nlp(text)
        self.matcher(doc)

        #if not doc._.requires_merge:
        #    return text

        doc_new = []
        for token in doc:
                        
            text = token.text_with_ws
            if token._.merge_dash:
                left, right = text.split()
                text = left[:-1] + right
            doc_new.append(text)

        doc_new = ''.join(doc_new)
        return doc_new

if __name__ == "__main__":
    text = "This is a SEN-  tence. And we should simply merge it!"
    #text = "This is a SEN-  tence."
    clf = dedash()
    print(text)
    print(clf(text))
    
