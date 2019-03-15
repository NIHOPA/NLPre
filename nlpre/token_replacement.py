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

    def __init__(self, remove=False):
        """ Initialize the parser. """

        self.replace_dict = {
            "&": " and ",
            "%": " percent ",
            ">": " greater-than ",
            "<": " less-than ",
            "=": " equals ",
            "#": " ",
            "~": " ",
            "/": " ",
            "\\": " ",
            "|": " ",
            "$": "",
            # Remove empty :
            " : ": " ",
            # Remove double dashes
            "--": " ",
            # Remove possesive splits
            " 's ": " ",
            # Remove quotes
            "'": "",
            '"': "",
        }

        if remove:
            for key in self.replace_dict:
                self.replace_dict[key] = ""

    def __call__(self, text):
        """
        Runs the parser.

        Args:
            text: A string document
        Returns:
            text: The document with common extraneous punctuation removed.
        """

        for key, val in self.replace_dict.items():
            text = text.replace(key, val)

        return text
