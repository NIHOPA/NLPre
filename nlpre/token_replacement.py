
class token_replacement(object):

    """
        Changes common tokens to standard replacements:

        ('&', ' and ')
        ('%', ' percent ')
        ('>', ' greater-than ')
        ('<', ' less-than ')
        ('=', ' equals ')
        ('#', ' ')
        ('~', ' ')
        ('/', ' ')
        ('\\', ' ')
        ('|', ' ')
        ('$', '')

        # Remove empty colons
        (' : ', ' ')

        # Remove double dashes
        ('--', ' ')

        # Remove possesive splits
        (" 's ", ' ')

        # Remove quotes
        ("'", '')
        ('"', '')
    """

    def __init__(self):
        """ Initialize the parser. """
        pass

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: A string document
        Returns:
            text: The document with common extraneous punctuation removed.
        """

        text = text.replace('&', ' and ')
        text = text.replace('%', ' percent ')
        text = text.replace('>', ' greater-than ')
        text = text.replace('<', ' less-than ')
        text = text.replace('=', ' equals ')
        text = text.replace('#', ' ')
        text = text.replace('~', ' ')
        text = text.replace('/', ' ')
        text = text.replace('\\', ' ')
        text = text.replace('|', ' ')
        text = text.replace('$', '')

        # Remove empty :
        text = text.replace(' : ', ' ')

        # Remove double dashes
        text = text.replace('--', ' ')

        # Remove possesive splits
        text = text.replace(" 's ", ' ')

        # Remove quotes
        text = text.replace("'", '')
        text = text.replace('"', '')

        return text
