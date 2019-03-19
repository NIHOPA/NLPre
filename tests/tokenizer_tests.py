from nose.tools import *
from nlpre.tokenizers import sentence_tokenizer


class Tokenizer_Tests:
    def sentence_tokenizer_test(self):

        text = """
        Everyone had always said that John would be a preacher when he grew up,
        just like his father. It had been said so often that John, without 
        ever thinking about it, had come to believe it himself. 
        Not until the morning of his 14th birthday did he really begin to 
        think about it, and by then it was already too late.
        """

        sentences = sentence_tokenizer(text)
        assert_equal(len(sentences), 3)
