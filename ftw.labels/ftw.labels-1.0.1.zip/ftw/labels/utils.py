import unicodedata


def make_sortable(text):
    """Converts a string to a sortable string by lowercasing
    it and removing diacritics.
    """
    if isinstance(text, str):
        text = text.decode('utf-8')
    if not isinstance(text, unicode):
        return text
    text = text.lower()
    normalized = unicodedata.normalize('NFKD', text)
    text = u''.join([c for c in normalized if not unicodedata.combining(c)])
    text = text.encode('utf-8')
    return text
