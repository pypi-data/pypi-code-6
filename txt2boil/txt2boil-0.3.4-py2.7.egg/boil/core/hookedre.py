"""A regex match object with a hook for generating output.

"""

import re


class HookedRegex(object):

    """A regex object with a hook that generates output from what it has
    matched.

    """

    def __new__(cls, match, template, text):
        if re.match(match, text, re.M) is None:
            return None
        return super(HookedRegex, cls).__new__(cls, match, template, text)

    def __init__(self, match, template, text):
        """Initialize the object as a clone of another regex, but add a hook
        to it this time.

        """

        self.regex = re.match(match, text, re.M)
        self.template = template

    def __bool__(self):
        return self.regex is not None

    def group(self, n=0):
        return self.regex.group(n)

    def output(self, match):
        return match.expand(self.template.format(self.regex.group(2)))
