
class Assignment:
    """ A class used for demo purposes.

    This class will be given a "codesignature" that can be used for comparing.
    """
    
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return u'Filename: {}'.format(self.filename)
