class Output:
    def __init__(self, refs):
        self.hasFilters = False
        self.actions = []
        self.filters = {}
        self.type = 'image/png'
        self.location = None
        self.tagName = None
        self.refs = refs

    def tag(self, tag):
        """
        Sets the tag for our input image
        """

        self.tagName = tag

        return self

    def resize(self, size):
        """
        Sets an action to our image to resize given the width and height given
        """

        self.actions.append({ 'method': 'resize', 'options': size })

        return self

    def filter(self, type, value):
        """
        Sets image filters to our image
        """

        self.hasFilters = True

        self.filters[type] = value

        return self

    def rotate(self, options):
        """
        Rotates our input image
        """

        self.actions.append({ 'method': 'rotate', 'options': options })

        return self

    def url(self, location):
        self.location = location

        return self

    def crop(self, position):
        """
        Crops our image to given coordinates or to the dominate face
        """

        self.actions.append({ 'method': 'crop', 'options': position })

        return self

    def export(self):
        """
        Generates the dictionary needed for this output
        """

        if self.hasFilters:
            self.actions.append({ 'method': 'filter', 'options': self.filters })

        output = {
            'ref': self.refs,
            'type': self.type,
            'tag': self.tagName,
            'methods': self.actions
        }

        if self.location:
            output['url'] = self.location

        return output;
