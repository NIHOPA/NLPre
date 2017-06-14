from nose.tools import *
from nlpre.tokenizers import meta_text, split_tokenizer, sentence_tokenizer, word_tokenizer


class Tokenizer_Tests():

    def meta_test(self):
        meta = meta_text('hello world', stuff='unicode')

        assert_equal('hello world', meta.text)
        assert_equal({'stuff': 'unicode'}, meta.meta)
        assert_equal('hello world', meta.__unicode__())

    def word_tokenizer_blank_test(self):
        doc = word_tokenizer([])
        assert_equal(doc, [])

    def word_tokenizer_words_test(self):
        tokens = word_tokenizer('hello world')
        assert_equal(tokens, ['hello', 'world'])

    def word_tokenizer_sentences_test(self):
        tokens = word_tokenizer('hello world. goodbye world')
        assert_equal(tokens, ['hello', 'world', '.', 'goodbye', 'world'])

    def split_tokenizer_test(self):
        def lowered(text):
            out = []
            for token in text:
                lower_token = token.lower()
                out.append(lower_token)
            return out

        string = ["HELlO", "WORLD"]
        lowerer = split_tokenizer(lowered)
        output = lowerer(string)
        output_right = 'hello world'
        assert_equal(output, output_right)
