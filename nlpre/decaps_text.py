from tokenizers import sentence_tokenizer

# Given a document, this class will convert all words that have only one capitalized letter to lowercase
class decaps_text(object):
    # Returns the number of different characters between two strings
    def diffn(self, s1, s2):
        return len([a for a, b in zip(s1, s2) if a != b])

    def __init__(self):
        pass

    # Converts a word to lowercase if only one letter in the word is capitalized.
    # We could make this a lot less complicated if we just check if the first word is capitalized. When
    # else would a word have only 1 capital letter? pH. Biology has a bunch
    def modify_word(self, org):

        lower = org.lower()

        if self.diffn(org, lower) > 1:
            return org
        else:
            return lower

    def __call__(self, doc):

        sentences = sentence_tokenizer(doc)

        doc2 = []

        for sent in sentences:

            sent = [self.modify_word(w) for w in sent]
            doc2.append(' '.join(sent))

        doc2 = '\n'.join(doc2)

        return doc2
