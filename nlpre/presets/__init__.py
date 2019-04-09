from .. import unidecoder, dedash, titlecaps, replace_acronyms
from .. import separated_parenthesis, replace_from_dictionary
from .. import token_replacement, decaps_text, pos_tokenizer
from .. import dictionary
import joblib


class Generic_Preprocessing_Pipeline:
    def __init__(self, n_cores=1):
        self.n_cores = n_cores
        self.pipeline = []

    pipeline = []

    def __call__(self, text):

        for clf in self.pipeline:
            text = clf(text)

        return text

    def batch(self, text_list):
        func = joblib.delayed(self)

        with joblib.Parallel(self.n_cores) as MP:
            output = MP(func(text) for text in text_list)

        return output


class Grants(Generic_Preprocessing_Pipeline):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        POS_BLACKLIST = [
            "pronoun",
            "verb",
            "adjective",
            "punctuation",
            "possessive",
            "symbol",
            "cardinal",
            "connector",
            "adverb",
            "unknown",
        ]

        self.pipeline = [
            unidecoder(),
            dedash(),
            # titlecaps(),
            # replace_acronyms(suffix="ABBR"),
            # separated_parenthesis(min_keep_length=10),
            # replace_from_dictionary(dictionary.MeSH, suffix="_MeSH"),
            # token_replacement(remove=True),
            # decaps_text(),
            # pos_tokenizer(POS_BLACKLIST),
        ]
