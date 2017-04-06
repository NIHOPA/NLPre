from nose.tools import *
from nlpre.tokenizers import meta_text, split_tokenizer, sentence_tokenizer, word_tokenizer


class Tokenizer_Tests():
    def __init__(self):
        pass

    def meta_test(self):
        meta = meta_text('hello world', stuff='unicode')

        assert_equal('hello world', meta.text)
        assert_equal({'stuff':'unicode'}, meta.meta)
        assert_equal('hello world', meta.__unicode__())

    def word_tokenizer_blank_test(self):
        doc = word_tokenizer([])
        assert_equal(doc, [])

    def word_tokenizer_words_test(self):
        tokens = word_tokenizer('hello world')
        assert_equal(tokens, ['hello', 'world'])

    # def word_tokenizer_sentences_test(self):
    #    tokens = word_tokenizer('hello world. goodbye world')
    #    assert_equal(tokens, [['hello', 'world'], ['goodbye', 'world']])
