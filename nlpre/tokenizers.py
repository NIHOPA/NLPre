from . import nlp


def sentence_tokenizer(text):
    """
    Uses spaCy to input text into a list sentences and word tokens.
    """
    return [[x.text for x in sentence] for sentence in nlp(text).sents]
