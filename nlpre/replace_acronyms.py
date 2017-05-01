#Given a counter dictionary and a document, this class will replace all instances of acronyms in the document
import pattern
import six

class Replace_Acryonym():
    def __init__(self, counter):
        self.counter = counter

        self.parse = lambda x: pattern.en.tokenize(
            x)

        self.acronym_dict = {}

        for tuple in self.counter.iterkeys():
            self.acronym_dict[tuple(1)] = tuple(0)

    def check_acronym(self, token):
        if not isinstance(token, six.string_types):
            return False
        if len(token) == 1:
            return False

        if token.lower() == token:
            return False

        for acronyms in self.acronym_dict.iterkeys():






    def __call__(self, document):
        tokens = self.parse(document)

        for token in tokens:
            if self.check_acronym(token):




