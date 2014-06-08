""" Module that provides some error classes.

Defines errors that can be used to control program flow
and error handling.

"""

class NoValidPluginTypeError(Exception):
    pass

class InvalidPluginTypeError(Exception):
    pass

class NoPluginPathsProvided(Exception):
    pass

class InvalidPluginPath(Exception):
    pass
