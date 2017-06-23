import string
import re


class url_replacement(object):

    """
        Removes (or replaces) URLs within a document. URLs must start with
        either http, https, www, or ftp but can be contained within strings.
    """

    def __init__(self, prefix=""):
        """ Initialize the parser. """
        self.patterns = {}
        for key in ["www", "ftp"]:
            self.patterns[key] = self.compile_pattern(key)

        self.prefix = prefix

    def compile_pattern(self, header):
        '''
        Source for regex pattern
        https://stackoverflow.com/a/1986151/249341
        '''
        pat = (
            r'\b(([\w-]+://?|{header}[.])[^\s()<>]+(?:\([\w\d]+\)|'
            r'([^%s\s]|/)))'
        ).format(header=header)
        pat = pat % re.sub(r'([-\\\]])', r'\\\1', string.punctuation)
        return re.compile(pat)

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: A string document
        Returns:
            text: The document with links remove or replaced with _prefix
        """

        for key, val in self.patterns.items():
            text = re.sub(val, self.prefix, text)
        return text
