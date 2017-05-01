# Given a counter dictionary and a document, this class will replace all
# instances of acronyms in the document
import pattern
from identify_parenthetical_phrases import identify_parenthetical_phrases
import operator
from Grammars import parenthesis_nester


class Replace_Acronym():
    def __init__(self, counter, underscore=True):
        self.counter = counter
        self.underscore = underscore

        self.parse = lambda x: pattern.en.tokenize(
            x)

        self.parser = parenthesis_nester()

        self.acronym_dict = {}

        for tuple, count in self.counter.iteritems():
            if tuple[1] in self.acronym_dict:
                self.acronym_dict[tuple[1]].append([tuple[0], count])
            else:
                self.acronym_dict[tuple[1]] = [(tuple[0], count)]

    def check_acronym(self, token):
        # if len(token) == 1:
        #    return False
        if token.lower() == token:
            return False

        if token in self.acronym_dict:
            return True
        else:
            return False

    def __call__(self, document):
        # if isinstance(tokens, pypar.ParseResults):
        #    tokens = tokens.asList()

        sentences = self.parse(document)
        # not really efficient to re-run the counter. I think saving counters
        # for each doc as meta-data might be the way to go
        ID_Phrases = identify_parenthetical_phrases()
        counter = ID_Phrases(document)

        new_doc = []

        for sentence in sentences:
            tokens = sentence.split()
            new_sentence = []
            for index, token in enumerate(tokens):
                continue_flag = False
                if self.check_acronym(token):
                    # check if acronym is used within document
                    for tuple in counter.iterkeys():
                        if tuple[1] == token:
                            continue_flag = True
                            highest_phrase = list(tuple[0])
                            break
                    # if acronym has already been replaced
                    if not continue_flag:
                        acronym_counts = self.acronym_dict[token]
                        acronym_counts.sort(
                            key=operator.itemgetter(1), reverse=True)
                        highest_phrase = acronym_counts[0][0]

                    if self.underscore:
                        new_sentence.append('_'.join(highest_phrase))
                    else:
                        new_sentence.extend(highest_phrase)

                else:
                    new_sentence.append(token)
            new_doc.append(' '.join(new_sentence))

        return '\n'.join(new_doc)
