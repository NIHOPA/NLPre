
class token_replacement(object):
    """
    Args:
        doc: a string document
    
    Returns
        Returns the document with common extraneous punctuation removed
    """

    def __init__(self):
        pass

    def __call__(self, doc):
        doc = doc.replace('&', ' and ')
        doc = doc.replace('%', ' percent ')
        doc = doc.replace('>', ' greater-than ')
        doc = doc.replace('<', ' less-than ')
        doc = doc.replace('=', ' equals ')
        doc = doc.replace('#', ' ')
        doc = doc.replace('~', ' ')
        doc = doc.replace('/', ' ')
        doc = doc.replace('\\', ' ')
        doc = doc.replace('|', ' ')
        doc = doc.replace('$', '')

        # Remove empty :
        doc = doc.replace(' : ', ' ')

        # Remove double dashes
        doc = doc.replace('--', ' ')

        # Remove possesive splits
        doc = doc.replace(" 's ", ' ')

        # Remove quotes
        doc = doc.replace("'", '')
        doc = doc.replace('"', '')

        return doc
