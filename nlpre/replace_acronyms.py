import pattern
import operator
import nlpre.identify_parenthetical_phrases as IPP


class replace_acronyms():

    """
    Replaces acronyms and abbreviations found in a document with their
    corresponding phrase. A counter dictionary is passed in __init__
    to determine phrases.

    If an acronym is explicitly identified with a phrase in a document, then
    all instances of that acronym in the document will be replaced with the
    given phrase.

    Example:
        input: "The Environmental Protection Agency (EPA) protects trees. The
                EPA was created by Nixon"
        output: "The Environmental Protection Agency
                 (Environmental_Protection_Agency) protects trees. The
                 Environmental_Protection_Agency was created by Nixon"

    If there is no explicit indication what the phrase is within the document,
    then the most common phrase associated with the acronym in the given
    counter is used.

    Example:
        input: "The EPA protects trees"
        output: "The Environmental_Protection_Agency protects trees"
    """

    def __init__(
            self,
            counter,
            prefix=None,
            underscore=True,
            preprocessed=False):
        '''
        Initialize the parser, the acronym dictionary, and flags

        Args:
            counter: A counter object of acronyms and their counts found in a
                     larger corpus
            underscore: A boolean to indicate whether to insert phrases
                        as a single underscored token
            preprocessed: A boolean to indicate if input text is raw,
                          or has been processed by other NLPre modules
        '''

        self.counter = counter
        self.prefix = prefix
        self.underscore = underscore
        self.preprocessed = preprocessed
        self.IPP = IPP.identify_parenthetical_phrases()

        self.parse = lambda x: pattern.en.tokenize(x)

        self.acronym_dict = {}

        for acronym_tuple, count in self.counter.iteritems():
            if acronym_tuple[1] in self.acronym_dict:
                self.acronym_dict[acronym_tuple[1]].append(
                    [acronym_tuple[0], count])
            else:
                self.acronym_dict[acronym_tuple[1]] = [(acronym_tuple[0],
                                                        count)]

    def check_self_counter(self, token, doc_counter):
        '''
        Check if an acronym token is defined within the document

        Args:
            token: a string token
            doc_counter: a counter object of acronyms defined within a document
        Returns:
            a boolean
        '''

        for acronym_tuple in doc_counter.iterkeys():
            if acronym_tuple[1] == token:
                highest_phrase = list(acronym_tuple[0])
                return highest_phrase
        return False

    # Return false if a word cannot belong to any abbreviated phrase
    # Since words with dashes are turned into a list of their
    # individual words, we must treat all words as a list. So, single
    # tokens are thus converted to single item lists.
    def word_belongs(self, word, acronym_phrases):
        for acronym_phrase in acronym_phrases:
            if isinstance(word, basestring):
                wordlist = [word]
            else:
                wordlist = list(word)
            for individual_word in wordlist:
                if individual_word not in acronym_phrase:
                    return False
        return True
    """
    def check_acronym(self, token):
        '''
        Check if a token is an acronym to be replaced

        Args:
            token: a string token
        Returns:
            a boolean
        '''

        if token.lower() == token:
            return False

        if token in self.acronym_dict:
            return True
        else:
            return False



    def check_phrase(self, token, pos, tokens, counter):
        if not self.underscore:
            return False

        acronym_phrases = []

        for acronym_tuple in counter.iterkeys():
            acronym_phrases.append(list(acronym_tuple[0]))

        # find length of longest phrase? worth it?
        phrase = []
        word = token
        length = 0
        while pos < len(tokens) - 1:
            length += 1
            if '-' in word:
                word = word.split('-')
                phrase.extend(word)
            else:
                phrase.append(word)

            if not self.word_belongs(word, acronym_phrases):
                return False

            if phrase in acronym_phrases:
                output = ('_'.join(phrase), length - 1)
                return output
            else:
                pos += 1
                word = tokens[pos]

        return False

    def __call__(self, document, doc_counter=None):
        '''
        Identify and replace all acronyms in the document

        Args:
            document: a string
            doc_counter: a counter object of acronyms defined within a
                         document. If missing, identify_parenthetical_phrases
                         is run.
        Returns:
            new_doc: a string
        '''

        if doc_counter is None:
            doc_counter = self.IPP(document)

        if self.preprocessed:
            sentences = document.split('\n')
        else:
            sentences = self.parse(document)

        new_doc = []

        for sentence in sentences:
            tokens = sentence.split()
            new_sentence = []

            index = -1
            while index < len(tokens) - 1:
                index += 1
                token = tokens[index]
                if self.check_acronym(token):
                    # check if acronym is used within document
                    highest_phrase = self.check_self_counter(
                        token, doc_counter)

                    if not highest_phrase:
                        acronym_counts = self.acronym_dict[token]
                        acronym_counts.sort(
                            key=operator.itemgetter(1), reverse=True)
                        highest_phrase = list(acronym_counts[0][0])
                    if self.underscore and self.prefix:
                        highest_phrase.insert(0, self.prefix)
                    if self.underscore:
                        new_sentence.append('_'.join(highest_phrase))
                    else:
                        new_sentence.extend(highest_phrase)
                    continue

                tokenized_phrase = self.check_phrase(
                    token, index, tokens, doc_counter)
                if tokenized_phrase:
                    phrase = tokenized_phrase[0]
                    if self.prefix:
                        phrase = '_'.join([self.prefix, phrase])
                    new_sentence.append(phrase)
                    index += tokenized_phrase[1]
                else:
                    new_sentence.append(token)
            new_doc.append(' '.join(new_sentence))

        new_doc = '\n'.join(new_doc)

        # if self.underscore:
        #    new_doc = self.tokenize_phrases(new_doc, doc_counter)

        return new_doc
    """

    def __call__(self, document, doc_counter=None):
        if doc_counter is None:
            doc_counter = self.IPP(document)

        if self.preprocessed:
            sentences = document.split('\n')
        else:
            sentences = self.parse(document)

        new_doc = []

        # This code is pretty hideous. Try to refactor it
        for sentence in sentences:
            tokens = sentence.split()
            new_sentence = []
            index = -1
            while index < len(tokens) - 1:
                index += 1
                token = tokens[index]
                mutable_index = [index]
                # Check if a token is an acronym and replace if so
                if self.check_acronym2(token, new_sentence, doc_counter):
                    pass

                # Check if a series of tokens is a phrase associated with
                # an abbreviated, and tokenize
                elif self.underscore and self.check_phrase2(token,
                                                            mutable_index,
                                                            tokens,
                                                            doc_counter,
                                                            new_sentence):
                    index = mutable_index[0]
                    pass
                else:
                    new_sentence.append(token)
            new_doc.append(' '.join(new_sentence))

        new_doc = '\n'.join(new_doc)
        return new_doc

    def check_acronym2(self, token, new_sentence, doc_counter):
        '''
        Check if a token is an acronym to be replaced

        Args:
            token: a string token
        Returns:
            a boolean
        '''

        if token.lower() == token:
            return False
        if token not in self.acronym_dict:
            return False
        else:
            # check if acronym is used within document
            highest_phrase = self.check_self_counter(
                token, doc_counter)
            # if not, then search the full counter dictionary and use the
            # most common phrase
            if not highest_phrase:
                acronym_counts = self.acronym_dict[token]
                acronym_counts.sort(
                    key=operator.itemgetter(1), reverse=True)
                highest_phrase = list(acronym_counts[0][0])

            if self.underscore and self.prefix:
                highest_phrase.insert(0, self.prefix)

            if self.underscore:
                new_sentence.append('_'.join(highest_phrase))
            else:
                new_sentence.extend(highest_phrase)

        return True

    def check_phrase2(self, token, index, tokens, counter, new_sentence):
        acronym_phrases = []
        pos = index[0]
        for acronym_tuple in counter.iterkeys():
            acronym_phrases.append(list(acronym_tuple[0]))

        phrase = []
        word = token
        length = 0
        tokenized_phrase = None

        # Check to see if proceeding tokens form an abbreviated phrase
        while pos < len(tokens) - 1:
            length += 1
            if '-' in word:
                word = word.split('-')
                phrase.extend(word)
            else:
                phrase.append(word)

            if not self.word_belongs(word, acronym_phrases):
                return False

            if phrase in acronym_phrases:
                tokenized_phrase = '_'.join(phrase)
                break
            else:
                pos += 1
                word = tokens[pos]

        if tokenized_phrase:
            if self.prefix:
                tokenized_phrase = '_'.join([self.prefix, tokenized_phrase])
            new_sentence.append(tokenized_phrase)
            index[0] += length - 1
            return True

        return False
    # """
