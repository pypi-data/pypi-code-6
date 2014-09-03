"""
Rename SDL_* functions according to our rules.
"""

class Renamer(object):
    def __init__(self, lib, prefix, constant_re, whitelist=()):
        self.lib = lib
        self.prefix = prefix
        self.constant_re = constant_re
        self.whitelist = whitelist

    def rename(self, name, value):
        """
        Apply our renaming rules, given a name and its value.

        Return new name, or None if name is to be omitted from the API.
        """
        pretty_name = name
        match = self.constant_re.match(name)
        if name.startswith('SDLK'):
            pretty_name = name[3:]
        elif match:
            pretty_name = match.group('pretty_name')
        elif not name.startswith(self.prefix):
            if not name in self.whitelist:
                return None
        elif isinstance(value, type):
            pretty_name = name[4:]
        else:
            pretty_name = name[4].lower() + name[5:]
        return pretty_name
