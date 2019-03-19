from . import nlp


def sentence_tokenizer(text):
    """
    Uses spaCy to input text into a list sentences and word tokens.
    """

    # Remove extra whitespace, as we don't need to preserve it and
    # it confuses spaCy models sometimes.
    text = " ".join(text.split())

    return [[x.text for x in sentence] for sentence in nlp(text).sents]
