from tokenizers import sentence_tokenizer

# Given a document, this class will convert all words that have only one
# capitalized letter to lowercase


class decaps_text(object):
    """
    Args: 
        text: a string document
    
    Returns:
        Returns the same document, but with all words that have only one 
        capital letter converted to lowercase.
    """
    # Returns the number of different characters between two string
    def diffn(self, s1, s2):
        return len([a for a, b in zip(s1, s2) if a != b])

    def __init__(self):
        pass

    def modify_word(self, org):

        lower = org.lower()

        if self.diffn(org, lower) > 1:
            return org
        else:
            return lower

    def __call__(self, text):

        sentences = sentence_tokenizer(text)

        doc2 = []

        for sent in sentences:

            sent = [self.modify_word(w) for w in sent]
            doc2.append(' '.join(sent))

        doc2 = '\n'.join(doc2)

        return doc2
