from .Grammars import reference_patterns
from .dictionary import wordlist_english
import logging
import re

REFERENCE_PREFIX = "REF_"
strip_table = str.maketrans("", "", "(){}<>[]")
strip_table = str.maketrans("", "", "(){}<>[].,!;?")


class separate_reference:

    """
    Detects if a reference number has been mistakenly concatenated to words in
    a document. This module will remove reference numbers, with the option
    to include them as a token representing the reference number. If these
    reference numbers wrap around a period at the end of the sentence, the
    module will identify this and properly split the sentences.


    Example:
        input: 'How is the treatment going.4-5 Pretty well'
        output: 'How is the treatment going . Pretty well'
    """

    def __init__(self, reference_token=False, f_wordlist=None):
        """
        Initialize the parser

        Args:
            reference_token: boolean, flag to decide to tokenize removed
                reference content
        """
        self.logger = logging.getLogger(__name__)

        if f_wordlist is None:
            f_wordlist = wordlist_english

        self.english_words = set()
        with open(f_wordlist) as FIN:
            for line in FIN:
                self.english_words.add(line.strip())

        self.reference_token = reference_token
        self.reference_pattern = reference_patterns()

    def __call__(self, text):
        """
        call the parser

        Args:
            text: a document string

        Returns:
             return_doc: a document string
        """

        new_doc = []
        tokens = text.strip().split()

        new_sentence = []
        for token in tokens:
            # Check if word is of the form word4.
            new_tokens = self.single_number_pattern(token)
            if new_tokens:
                new_sentence.extend(new_tokens)
                continue

            # Check if the word is of the form word(4)
            new_tokens = self.identify_reference_punctuation_pattern(
                token, self.reference_pattern.single_number_parens, parens=True
            )
            if new_tokens:
                new_sentence.extend(new_tokens)
                continue

            # Check if the word is of the form word,2,3,4
            new_tokens = self.identify_reference_punctuation_pattern(
                token, self.reference_pattern.punctuation_then_number, forward=3
            )
            if new_tokens:
                new_sentence.extend(new_tokens)
                continue

            # Check if the word is of the form word2,3,4
            new_tokens = self.identify_reference_punctuation_pattern(
                token, self.reference_pattern.number_then_punctuation
            )
            if new_tokens:
                new_sentence.extend(new_tokens)
                continue

            # if no reference detected, append word to the new sentence
            new_sentence.append(token)

        join_sentence = " ".join(new_sentence)
        new_doc.append(join_sentence)

        return_doc = " ".join(new_doc)
        return return_doc

    # This is an ambiguous  case, because there could be words that end in a
    # number that don't represent a footnote, as is the case for chemicals.
    # The code looks up the characters that make up a word, and if they are
    # not found in the dictionary, it is assumed it is a chemical name and
    # the number is not pruned.

    def single_number_pattern(self, token):
        """
        Detect the most basic case where a single number is concatenated to the
        word token

        Args:
            token: a string token

        Returns:
            output: a list of string tokens
        """
        output = []
        try:
            parse_return = self.reference_pattern.single_number.parseString(
                token
            )
        except BaseException:
            return False

        if parse_return[0] not in self.english_words:
            output.append(token)
        else:
            word = parse_return[0]
            reference = parse_return[1]

            output.append(word)

            if self.reference_token:
                output.append(REFERENCE_PREFIX + reference)

            if self.end_parens_match(parse_return):
                output[-1] = output[-1] + parse_return[-1]

        return output

    def identify_reference_punctuation_pattern(
        self, token, pattern, parens=False, forward=2
    ):
        """
        Identify whether the pyparsing pattern passed to the function is found
        in the token.

        Args:
            token: a string token
            pattern: a pyparsing grammar pattern
            parens: a boolean to flag whether the function should expect to
                recognize a reference in parenthesis
            forward: Number of characters to skip forward

        Return:
             Output: a list of string tokens
        """
        output = []
        parse_return = pattern.searchString(token)

        if parse_return:

            substring = "".join(parse_return[0][forward:])
            index = token.find(substring)
            word = token[:index]

            if self.end_parens_match(parse_return[0], parens=True):
                end_offset = len(parse_return[0][-1]) * -1
                reference = token[len(word) : end_offset]
            else:
                reference = token[len(word) :]

            output.append(word)

            if self.reference_token:
                ref_token = (REFERENCE_PREFIX + reference).translate(
                    strip_table
                )
                output.append(ref_token)

            # Handle nested parens
            if (
                len(substring) > 2
                and substring[-2] in "])}"
                and substring[-3] in "])}"
            ):
                output[-1] += substring[-2]

            # Reference tokens have stripped too much
            if self.reference_token:
                if substring[-1] in ".,?!;:":
                    output[-1] += substring[-1]

            # Replace any stripped punctuation
            if substring[0] in ".,?!;:":
                output[-1] += substring[0]

            if self.end_parens_match(parse_return[0], parens=parens):
                output[-1] = output[-1] + parse_return[0][-1]

        else:
            output = False

        if output and reference[-1] in ".,?!;:" and not self.reference_token:
            output[-1] += reference[-1]

        return output

    def end_parens_match(
        self, strlist, search=re.compile(r"[^)}\]]").search, parens=False
    ):
        """
        Check if the token ends in parenthesis, and thus needs to avoid
        removing them as part of the reference.

        Args:
            strlist: a list of string subtokens, parsed from the given grammar
            search: pattern to recognize. Defaults to ending parenthesis
            parens: boolean to flag whether the passed grammar is for
                references with parenthesis in them.

        Return:
            a boolean
        """
        # special case when parsing with the parenthetical content grammar.
        # We check to see if a token ends with a parenthesis to see if we need
        # to append one to the cleaned token. However, we do not want to do
        # this if the token ends with a parenthesis that holds a nested
        # reference
        if parens:
            LP_Paran = sum(1 for a in strlist if a == "(")
            RP_Paran = sum(1 for a in strlist if a == ")")

            LP_Bracket = sum(1 for a in strlist if a == "[")
            RP_Bracket = sum(1 for a in strlist if a == "]")

            LP_Curl = sum(1 for a in strlist if a == "{")
            RP_Curl = sum(1 for a in strlist if a == "}")

            # If the count of the left paren doesn't match the right, then
            # ignore all parenthesis
            FLAG_valid = (
                (LP_Paran == RP_Paran)
                and (LP_Bracket == RP_Bracket)
                and (LP_Curl == RP_Curl)
            )

            if FLAG_valid:
                return False

        return isinstance(strlist[-1], str) and not bool(search(strlist[-1]))
