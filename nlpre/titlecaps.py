# -*- coding: utf-8 -*-
from tokenizers import sentence_tokenizer


def is_any_lowercase(tokens):

    any_alpha = False
    for x in tokens:
        for letter in x:
            if letter.isalpha():
                any_alpha = True
                if letter == letter.lower():
                    return True
    if any_alpha:
        return False
    else:
        return True

# if any sentance is only capitalized, it changes every letter to lowercase
class titlecaps(object):

    def __init__(self):
        pass

    def __call__(self, doc):

        sents = sentence_tokenizer(doc)

        doc2 = []
        for sent in sents:
            if not is_any_lowercase(sent):

                if len(sent) > 4:
                    print("DECAPING: '{}'".format(' '.join(sent)))

                sent = map(unicode.lower, sent)         #is this meant to fall under the if statement?

            doc2.append(' '.join(sent))

        doc2 = ' '.join(doc2)
        return doc2


if __name__ == "__main__":
    pass
