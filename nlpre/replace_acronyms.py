#Given a counter dictionary and a document, this class will replace all instances of acronyms in the document
import pattern
import six
from identify_parenthetical_phrases import identify_parenthetical_phrases
import operator
from Grammars import parenthesis_nester
import pyparsing as pypar


class Replace_Acronym():
    def __init__(self, counter):
        self.counter = counter

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
        if not isinstance(token, six.string_types):
            return False
        if len(token) == 1:
            return False

        if token.lower() == token:
            return False

        for acronym in self.acronym_dict.iterkeys():
            if token == acronym:
                return token

        return False






    def __call__(self, document):
        #tokens = self.parser(document)
        #if isinstance(tokens, pypar.ParseResults):
        #    tokens = tokens.asList()

        sentences = self.parse(document)
        tokens = document.split()
        #not really efficient to re-run the counter. I think saving counters
        #for each doc as meta-data might be the way to go
        ID_Phrases = identify_parenthetical_phrases()
        counter = ID_Phrases(document)



        new_doc = []

        for sentence in sentences:
            tokens = sentence.split()
            new_sentence = []
            for index, token in enumerate(tokens):
                continue_flag = False
                if self.check_acronym(token):
                    #check if acronym is used within document
                    for tuple in counter.iterkeys():
                        if tuple[1] == token:
                            #tokens[index] = tuple[0]
                            #tokens = tokens[:index] + list(tuple[0]) + tokens[index+1:]
                            continue_flag = True
                            new_sentence.extend(list(tuple[0]))
                            break
                    #if acronym has already been replaced

                    if not continue_flag:
                        acronym_counts = self.acronym_dict[token]
                        acronym_counts.sort(key=operator.itemgetter(1), reverse=True)
                        highest_phrase = acronym_counts[0][0]
                        new_sentence.extend(highest_phrase)
                        #token[index] = highest_phrase
                else:
                    new_sentence.append(token)
            new_doc.append(' '.join(new_sentence))

        return '\n'.join(new_doc)








