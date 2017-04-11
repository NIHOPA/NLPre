
class token_replacement(object):

    """
        Changes common tokens to standard replacements
    """

    def __init__(self):
        pass

    def __call__(self, text):
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
    '''
    Args:
        text: a string document
    Returns
        Returns the document with common extraneous punctuation removed.
    '''
