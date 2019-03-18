from . import nlp


class url_replacement(object):

    """
        Removes (or replaces) URLs and emails within a document.
        Uses spaCy to determine if like email or url.
    """

    def __init__(self, email_replacement="", url_replacement=""):
        """
        Initialize the parser.
        """
        self.email_replacement = email_replacement
        self.url_replacement = url_replacement

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: A string document
        Returns:
            text: The document with links removed or replaced
        """

        text = " ".join(text.strip().split())

        doc = []
        for token in nlp(text):

            if token.like_url:
                if self.url_replacement:
                    doc.append(self.url_replacement)
                    doc.append(token.whitespace_)

            elif token.like_email:
                if self.email_replacement:
                    doc.append(self.email_replacement)
                    doc.append(token.whitespace_)

            else:
                doc.append(token.text_with_ws)

        return "".join(doc)
